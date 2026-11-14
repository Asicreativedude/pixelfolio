# Light as a layer over the pixel art (#65). The art stays exactly as drawn; a scene only says where its lights
# are. Third version. The second left three weak points, and Asi asked to work on them:
#   "warm light on the blue floor turns grey": light no longer only multiplies. Where multiplying drains a
#     surface's colour (orange light on a blue floor gives grey), the surface keeps its colour, gains a little,
#     and its hue turns part of the way towards the light's hue. The blue floor goes violet under the lamp.
#   "only characters cast shadows": every prop casts one now. A prop stands on a footprint and has a height;
#     a pixel is in shadow when the way from it to the light crosses the footprint of something tall enough.
#     The shadows that make_room.py bakes into the art are switched off here, so light is the only source.
#     The Hall is one flat picture, so there everything that is not floor counts as 8 px tall.
#   "lit colours are not held to a palette": every pixel is snapped to one fixed palette of 64 colours:
#     ENDESGA 32 as it is, plus 32 colours fitted here to what these lit scenes ask for
#     (palettes/endesga-32-plus-light.hex). One drawn colour under one light level always becomes the same
#     palette colour, so lit areas stay flat. ENDESGA 32 alone and three ready-made 64-colour palettes were
#     tried too; the script prints how far each is from what was asked.
# Light is still three flat steps with a checker band at each edge, and characters still lay their sprite down.
# Writes painted-light-pixels.png (office by day, at dusk, at night; the Hall as drawn and lit),
# painted-light-zoom.png (6x crop), painted-light-palettes.png (the dusk office held to ENDESGA 32, ENDESGA 64
# and the fitted palette, then in free colours) and directions/d05-lamp-lit-dusk.png.
# usage (repo root): python3 -I art-tests/claude-drawn/make_painted_light.py
import math, os, sys
from PIL import Image, ImageChops
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import make_room as m

MAIN = 'endesga-32-plus-light'          # the palette the main sheet is held to: ENDESGA 32 and 32 added here
LEVELS, CUTS, BAND = (0, 0.34, 0.67, 1), (0.12, 0.42, 0.72), 0.022
HMAX = 11
RICH = 0.5                              # lit by a coloured light, a surface gains this much colour
TURN = 0.42                             # how far a coloured light turns a surface's hue towards its own


def clamp(v):
    return 0 if v < 0 else 1 if v > 1 else v


def step(v, x, y):
    """Three flat steps of light. Next to an edge, a checker of the two neighbouring steps."""
    for i, c in enumerate(CUTS):
        if abs(v - c) < BAND:
            return LEVELS[i + ((x + y) & 1)]
    return LEVELS[sum(v > c for c in CUTS)]


def pool(cx, cy, rx, ry, k=1.15):       # an ellipse of light on the ground
    return lambda x, y: clamp(k - math.hypot((x - cx) / rx, (y - cy) / ry))


def inside(poly, x, y):
    hit = False
    for (x0, y0), (x1, y1) in zip(poly, poly[1:] + poly[:1]):
        if (y0 > y) != (y1 > y) and x < x0 + (y - y0) * (x1 - x0) / (y1 - y0):
            hit = not hit
    return hit


def patches(*polys):                    # flat shapes of light, like sun through window panes
    return lambda x, y: 1.0 if any(inside(p, x, y) for p in polys) else 0.0


# ---------------------------------------------------------------- colour: light that keeps hue, then a palette
def lin(p):
    return [(v / 255) ** 2.2 for v in p[:3]]


def oklab(c):
    l, a, s = (0.4122214708 * c[0] + 0.5363325363 * c[1] + 0.0514459929 * c[2],
               0.2119034982 * c[0] + 0.6806995451 * c[1] + 0.1073969566 * c[2],
               0.0883024619 * c[0] + 0.2817188376 * c[1] + 0.6299787005 * c[2])
    l, a, s = l ** (1 / 3), a ** (1 / 3), s ** (1 / 3)
    return (0.2104542553 * l + 0.7936177850 * a - 0.0040720468 * s,
            1.9779984951 * l - 2.4285922050 * a + 0.4505937099 * s,
            0.0259040371 * l + 0.7827717662 * a - 0.8086757660 * s)


def from_oklab(L, a, b):
    l, q, s = (L + 0.3963377774 * a + 0.2158037573 * b) ** 3, (L - 0.1055613458 * a - 0.0638541728 * b) ** 3, \
              (L - 0.0894841775 * a - 1.2914855480 * b) ** 3
    c = (4.0767416621 * l - 3.3077115913 * q + 0.2309699292 * s, -1.2684380046 * l + 2.6097574011 * q - 0.3413193965 * s,
         -0.0041960863 * l - 0.7034186147 * q + 1.7076147010 * s)
    return tuple(round(255 * clamp(v) ** (1 / 2.2)) for v in c)


def target(p, k):
    """The colour a drawn pixel p should have under light k, in OKLab. Multiplying gives the brightness. Where
    it also drains the surface's own colour (orange light on a blue floor would give grey), the surface keeps
    its colour at the new brightness and its hue turns part of the way towards the light's hue instead."""
    a = lin(p)
    M, A = oklab([min(1, a[i] * k[i]) for i in range(3)]), oklab(a)
    cm, ca = math.hypot(M[1], M[2]), math.hypot(A[1], A[2])
    if A[0] < 1e-4 or ca < 1e-4:
        return M
    K = oklab([v / max(k) for v in k])
    lit = clamp(math.hypot(K[1], K[2]) / 0.08)        # 0 under white light, 1 under a clearly coloured one
    c = ca * min(1.25, M[0] / A[0]) * (0.9 + RICH * lit)
    g = clamp(1.5 * (1 - cm / c))                     # how much of its colour multiplying took away
    hA = math.atan2(A[2], A[1])
    h = hA + ((math.atan2(K[2], K[1]) - hA + math.pi) % (2 * math.pi) - math.pi) * TURN * lit
    return (M[0], M[1] * (1 - g) + c * math.cos(h) * g, M[2] * (1 - g) + c * math.sin(h) * g)


class Palette:
    def __init__(self, name, cols=None):
        path = '../pixellab/e32.hex' if name == 'endesga-32' else 'palettes/%s.hex' % name
        self.name, self.lut = name, {}
        self.cols = cols if cols is not None else [tuple(bytes.fromhex(h)) for h in open(os.path.join(m.HERE, path)).read().split()]
        self.labs = [oklab(lin(c)) for c in self.cols]

    def snap(self, lab):                # nearest palette colour; hue counts a little more than brightness
        if not self.cols:
            return from_oklab(*lab), 0
        d, i = min(((lab[0] - q[0]) ** 2 + 1.5 * ((lab[1] - q[1]) ** 2 + (lab[2] - q[2]) ** 2), i) for i, q in enumerate(self.labs))
        return self.cols[i], d ** 0.5

    def colour(self, p, k):
        key = (p, k)
        if key not in self.lut:
            self.lut[key] = self.snap(target(p, k) if k else oklab(lin(p)))
        return self.lut[key]


# ---------------------------------------------------------------- which light reaches which pixel
def footprints(masks, heights, W, H):
    """Where each prop stands on the ground. A prop is drawn `height` pixels taller than its footprint, so the
    footprint is every column of its mask without the top `height` pixels."""
    foot = [[-1] * W for _ in range(H)]
    for i, (mask, h) in enumerate(zip(masks, heights)):
        box = mask.getbbox()
        if not h or not box:
            continue
        px = mask.load()
        for x in range(box[0], box[2]):
            y = box[1]
            while y < box[3]:
                if px[x, y]:
                    y0 = y
                    while y < box[3] and px[x, y]:
                        y += 1
                    for fy in range(min(y0 + h, y - 1), y):
                        foot[fy][x] = i
                else:
                    y += 1
    return foot


def states(art, sprites, scene, owner, heights, foot):
    """For every pixel: the drawn colour, and the light that reaches it (None for pixels that give light).
    owner[y][x] is the prop a pixel belongs to (-1: floor and walls); props are numbered in drawing order."""
    W, H = art.size
    src = art.load()
    feet = []
    for s, x, y in sprites:
        b = s.getbbox(); feet.append((x + (b[0] + b[2]) // 2, y + b[3] - 2))
    flat = lambda x, y: owner[y][x] < 0 or not heights[owner[y][x]]
    cuts = []                           # per light: floor pixels in the shadow of a character
    for L in scene['lights']:
        cut = set()
        for (s, x, y), (fx, fy) in zip(sprites, feet):
            if 'dir' in L:
                dx, dy = L['dir']
            elif 'at' in L:
                dx, dy = fx - L['at'][0], fy - L['at'][1]
            else:
                continue
            n = math.hypot(dx, dy) or 1
            sp = s.load()
            for sy in range(s.height):
                for sx in range(s.width):
                    if sp[sx, sy][3]:
                        h = fy - (y + sy)             # how high this pixel is above the feet
                        gx, gy = round(x + sx + dx / n * h * 0.8), round(fy + dy / n * h * 0.55)
                        for q in ((gx, gy), (gx + 1, gy)):
                            if 0 <= q[0] < W and 0 <= q[1] < H and flat(*q):
                                cut.add(q)
        cuts.append(cut)

    def blocked(L, x, y):               # is there a tall enough prop between this pixel and the light?
        if 'dir' in L:
            dx, dy = -L['dir'][0], -L['dir'][1]
        elif 'at' in L:
            dx, dy = L['at'][0] - x, L['at'][1] - y
        else:
            return False
        n, o = math.hypot(dx, dy) or 1, owner[y][x]
        for t in range(1, HMAX + 1):
            gx, gy = round(x + dx / n * t * 0.8), round(y + dy / n * t * 0.55)
            if not (0 <= gx < W and 0 <= gy < H):
                return False
            i = foot[gy][gx]
            if i > o and heights[i] >= t:
                return True
        return False

    glow = scene.get('glow', lambda x, y, p: None)
    grid = [[None] * W for _ in range(H)]
    for y in range(H):
        for x in range(W):
            p = src[x, y][:3]
            g = glow(x, y, src[x, y])
            if g:
                grid[y][x] = (g[:3], None); continue
            k = list(scene['ambient'])
            for L, cut in zip(scene['lights'], cuts):
                v = step(L['field'](x, y), x, y)
                if v and (x, y) not in cut and not blocked(L, x, y):
                    k = [k[i] + v * L['col'][i] for i in range(3)]
            grid[y][x] = (p, tuple(round(v, 3) for v in k))
    for (s, x, y), (fx, fy) in zip(sprites, feet):          # figures: lit by what reaches their feet
        sp, cx = s.load(), fx - x
        lv = [step(L['field'](fx, fy), fx, fy) for L in scene['lights']]
        for sy in range(s.height):
            for sx in range(s.width):
                if sp[sx, sy][3] and 0 <= x + sx < W and 0 <= y + sy < H:
                    k = list(scene['ambient'])
                    for L, v in zip(scene['lights'], lv):
                        side = 1 if 'at' not in L or abs(L['at'][0] - fx) < 20 or (sx - cx) * (L['at'][0] - fx) > 0 else 0.34
                        k = [k[i] + v * side * L['col'][i] for i in range(3)]
                    grid[y + sy][x + sx] = (sp[sx, sy][:3], tuple(round(v, 3) for v in k))
    return grid


def render(grid, pal):
    """Hold a lit scene to a palette. Returns the picture and how far the palette is from what was asked for."""
    H, W = len(grid), len(grid[0])
    im = Image.new('RGB', (W, H)); px = im.load()
    err = 0
    for y in range(H):
        for x in range(W):
            px[x, y], d = pal.colour(*grid[y][x])
            err += d
    asked = {g for row in grid for g in row}
    return im, dict(error=round(err / (W * H), 4), asked=len(asked), colours=len({pal.colour(*g)[0] for g in asked}))


def sprite(src, row, col):
    return Image.open(os.path.join(m.HERE, src)).convert('RGBA').crop((col * 64, row * 64, col * 64 + 40, row * 64 + 64))


# ---------------------------------------------------------------- the office (make_room.py), three times of day
# Draw the room without its baked shadows, and note for each prop where it is and how tall it is.
CAST_H = {1: 2, 2: 5, 3: HMAX}          # make_room's cast offset says how far a prop stands out
masks, heights = [], []
_prop = m.Canvas.prop


def prop(self, fn, *a, cast=(2, 2)):
    before = self.im.copy()
    _prop(self, fn, *a, cast=None)
    if self.im.size == (m.W, m.H):
        masks.append(ImageChops.difference(before, self.im).convert('L').point(lambda v: 255 if v else 0))
        heights.append(CAST_H[cast[0]] if cast else 0)


m.Canvas.prop = prop
office = m.room().im
m.Canvas.prop = _prop
owner = [[-1] * m.W for _ in range(m.H)]
for i, mask in enumerate(masks):
    box, px = mask.getbbox(), mask.load()
    for y in range(box[1], box[3]) if box else ():
        for x in range(box[0], box[2]):
            if px[x, y]:
                owner[y][x] = i
foot = footprints(masks, heights, m.W, m.H)

WALL = 64
cast = [(sprite(src, row, col), x, y) for src, row, col, x, y in m.PEOPLE]
SKY_DUSK = {m.BLU: (236, 128, 112), m.CYA: (250, 178, 110), m.WHT: (255, 214, 160), m.NAVY: (150, 84, 120), m.SL1: (70, 52, 92), m.SL2: (52, 40, 76), m.SL0: (86, 62, 104)}
SKY_NIGHT = {m.BLU: (26, 32, 66), m.CYA: (40, 50, 92), m.WHT: (50, 58, 100), m.NAVY: (18, 22, 48), m.SL1: (14, 16, 34), m.SL2: (10, 12, 28), m.SL0: (20, 22, 44), m.YEL: (255, 220, 120)}
PANES = [[(60, 98), (90, 98), (110, 142), (76, 142)], [(96, 98), (126, 98), (150, 142), (116, 142)]]
on_wall = lambda f: (lambda x, y: f(x, y) if y < WALL else 0)
on_floor = lambda f: (lambda x, y: f(x, y) if y >= WALL else 0)
both = lambda f, g: (lambda x, y: max(f(x, y), g(x, y)))
screen_f = both(on_wall(pool(184, 55, 62, 50)), on_floor(pool(178, 120, 100, 70)))
lamp_f = both(on_wall(pool(224, 52, 54, 42)), on_floor(pool(248, 118, 94, 74, 1.2)))
SUN = (0.45, 0.9)                       # the way light falls in through the window


def office_glow(sky, screen, lamp):
    def glow(x, y, p):
        h = '%02x%02x%02x' % p[:3]
        if sky and 56 <= x < 116 and 18 <= y < 48 and h in sky and not (h == m.WHT and y >= 30):
            return sky[h]
        if screen and 164 <= x < 204 and 44 <= y < 66:
            return (38, 132, 128) if h == m.SL4 else from_oklab(*oklab([min(1, c * k) for c, k in zip(lin(p), (0.9, 2.2, 2.1))]))
        if lamp and 208 <= x < 232 and 58 <= y < 71 and p[0] > 200:
            return from_oklab(*oklab([min(1, c * 1.25) for c in lin(p)]))
    return glow


SCREEN, LAMP = dict(col=(0.06, 0.50, 0.47), field=screen_f, at=(184, 96)), dict(col=(0.95, 0.52, 0.20), field=lamp_f, at=(222, 104))
OFFICE = {
    'day': dict(ambient=(0.72, 0.72, 0.76), glow=office_glow(None, False, False), lights=[
        dict(col=(0.34, 0.30, 0.18), field=on_floor(patches(*PANES)), dir=SUN),
        dict(col=(0.28, 0.28, 0.24), field=lambda x, y: 1.0, dir=(0.62, 0.78))]),          # open sky: only its shadows show
    'dusk': dict(ambient=(0.20, 0.20, 0.33), glow=office_glow(SKY_DUSK, True, True), lights=[
        SCREEN, LAMP, dict(col=(0.50, 0.20, 0.30), field=on_floor(patches(*PANES)), dir=SUN)]),
    'night': dict(ambient=(0.11, 0.12, 0.22), glow=office_glow(SKY_NIGHT, True, False), lights=[
        dict(col=(0.08, 0.72, 0.68), field=screen_f, at=(184, 96)),
        dict(col=(0.14, 0.18, 0.30), field=on_floor(patches(*PANES)), dir=SUN)]),
}
grids = {k: states(office, cast, s, owner, heights, foot) for k, s in OFFICE.items()}

# ---------------------------------------------------------------- the existing Hall, as it is in the game
# The Hall is one flat picture, so there are no props to ask. Everything that is not floor counts as 8 px tall.
X0, Y0, HW, HH = 700, 423, 528, 297
hall = Image.open(os.path.join(m.HERE, '../../public/Hall2.png')).convert('RGBA').crop((X0, Y0, X0 + HW, Y0 + HH))
is_floor = lambda p: p[0] < p[1] < p[2] and 60 <= p[0] <= 110 and 20 <= p[2] - p[0] <= 60
hp = hall.load()
hall_owner = [[-1 if is_floor(hp[x, y]) else 0 for x in range(HW)] for y in range(HH)]
hall_mask = Image.new('L', (HW, HH)); hall_mask.putdata([255 * (o + 1) for row in hall_owner for o in row])
hall_foot = footprints([hall_mask], [8], HW, HH)
hall_cast = [(sprite('../../public/Hero/Sprite-Hero.png', 2, 0), 190, 120), (sprite('../../public/characters/saruli.png', 0, 0), 300, 90),
             (sprite('dog.png', 1, 0), 236, 150), (sprite('visitor.png', 0, 0), 60, 60)]
HALL = dict(ambient=(0.30, 0.31, 0.46), lights=[
    dict(col=(0.95, 0.55, 0.22), field=pool(452, 150, 150, 120), at=(452, 150)),                 # a lamp over the lounge
    dict(col=(0.30, 0.42, 0.50), field=pool(-60, 297, 190, 200), at=(-60, 330))])                # daylight from the lower door
hall_before = hall.copy()
for s, x, y in hall_cast:
    hall_before.alpha_composite(s, (x, y))
hall_grid = states(hall, hall_cast, HALL, hall_owner, [8], hall_foot)

# ---------------------------------------------------------------- a palette made for this light
def dist(p, q):
    return (p[0] - q[0]) ** 2 + 1.5 * ((p[1] - q[1]) ** 2 + (p[2] - q[2]) ** 2)


def extend(base, asked, n):
    """ENDESGA 32 stays as it is. n colours are added for what the lit scenes ask for. asked maps each asked
    colour to a weight (large flat areas such as a floor count more, so they get a colour of their own). Each
    new colour starts at the asked colour that is worst served so far, then the new ones settle (k-means,
    with the base held still)."""
    centres = [oklab(lin(c)) for c in base]
    for _ in range(n):
        centres.append(max(asked, key=lambda t: asked[t] * min(dist(t, c) for c in centres)))
    for _ in range(12):
        groups = [[] for _ in centres]
        for t in asked:
            groups[min(range(len(centres)), key=lambda i: dist(t, centres[i]))].append(t)
        for i in range(len(base), len(centres)):
            w = sum(asked[t] for t in groups[i])
            if w:
                centres[i] = tuple(sum(t[j] * asked[t] for t in groups[i]) / w for j in range(3))
    return base + [from_oklab(*c) for c in centres[len(base):]]


E32 = Palette('endesga-32')
asked = {}
for g in list(grids.values()) + [hall_grid]:
    for row in g:
        for p, k in row:
            t = target(p, k) if k else oklab(lin(p))
            asked[t] = asked.get(t, 0) + 1
asked = {t: asked[t] ** 0.5 for t in sorted(asked)}
own = Palette(MAIN, extend(E32.cols, asked, 32))
open(os.path.join(m.HERE, 'palettes/%s.hex' % MAIN), 'w').write(''.join('%02x%02x%02x\n' % c for c in own.cols))

# ---------------------------------------------------------------- the palettes compared, the sheet and the zoom
RW, RH = m.W, m.H
pals = [E32, Palette('endesga-64'), Palette('resurrect-64'), Palette('aap-64'), own, Palette('free', [])]
print('palette              dusk office: error, colours used of asked | hall: error, colours')
compare = Image.new('RGB', (RW * 4 + 8, RH * 4 + 8), (14, 12, 20))
shown = 0
for p in pals:
    im, st = render(grids['dusk'], p)
    _, sh = render(hall_grid, p)
    print('%-20s %.4f  %3d of %d | %.4f  %3d of %d' % (p.name, st['error'], st['colours'], st['asked'], sh['error'], sh['colours'], sh['asked']))
    if p.name in ('endesga-32', 'endesga-64', MAIN, 'free'):    # the sheet: ENDESGA 32, ENDESGA 64, ours, free colours
        compare.paste(im.resize((RW * 2, RH * 2), Image.NEAREST), (shown % 2 * (RW * 2 + 8), shown // 2 * (RH * 2 + 8)))
        shown += 1
compare.save(os.path.join(m.HERE, 'painted-light-palettes.png'))

pal = own
rooms = {k: render(g, pal)[0] for k, g in grids.items()}
hall_lit = render(hall_grid, pal)[0]
used = {c for im in list(rooms.values()) + [hall_lit] for _, c in im.getcolors(99999)}
assert used <= set(pal.cols) and len(set(pal.cols)) == 64, (len(used - set(pal.cols)), len(set(pal.cols)))      # the one check
sheet = Image.new('RGB', (RW * 6 + 16, RH * 2 + HH * 2 + 8), (14, 12, 20))
for i, k in enumerate(('day', 'dusk', 'night')):
    sheet.paste(rooms[k].resize((RW * 2, RH * 2), Image.NEAREST), (i * (RW * 2 + 8), 0))
for i, im in enumerate((hall_before.convert('RGB'), hall_lit)):
    sheet.paste(im.resize((HW * 2, HH * 2), Image.NEAREST), (i * (HW * 2 + 8), RH * 2 + 8))
sheet.save(os.path.join(m.HERE, 'painted-light-pixels.png'))
rooms['dusk'].crop((150, 100, 310, 200)).resize((960, 600), Image.NEAREST).save(os.path.join(m.HERE, 'painted-light-zoom.png'))
os.makedirs(os.path.join(m.HERE, 'directions'), exist_ok=True)
rooms['dusk'].resize((RW * 3, RH * 3), Image.NEAREST).save(os.path.join(m.HERE, 'directions/d05-lamp-lit-dusk.png'))
print('main sheet held to', MAIN, '-', len(used), 'of 64 colours used over all five pictures')
