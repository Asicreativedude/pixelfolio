# Light as a layer over the pixel art (#65). The art stays exactly as drawn; a scene only says where its lights
# are. Second version, after Asi on the first: "it looks a bit forced", "works in this specific scene", and
# "lights and shadow don't seem pixelated at all".
#   pixelated: a light is three flat steps. Each step ends on a clean one-pixel edge with a two-pixel checker
#     band, the way a pixel artist blends two tones. No noise, no smooth edge. A figure's shadow is its own
#     sprite laid down on the floor away from the light, pixel for pixel.
#   less forced: the dusk is calmer, and the same room is shown by day and at night with other settings.
#   not one scene: the same code lights the existing Hall map, which was drawn long before this test.
# Writes painted-light-pixels.png (office by day, at dusk, at night; the Hall as drawn and lit) and
# painted-light-zoom.png (a 6x crop, to check the pixels). Lit colours are not ENDESGA 32.
# usage (repo root): python3 -I art-tests/claude-drawn/make_painted_light.py
import math, os, sys
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import make_room as m

LEVELS, CUTS, BAND = (0, 0.34, 0.67, 1), (0.12, 0.42, 0.72), 0.022


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


def lin(p):
    return [(v / 255) ** 2.2 for v in p[:3]]


def out(v):
    return tuple(round(255 * clamp(c) ** (1 / 2.2)) for c in v) + (255,)


def relight(art, sprites, scene):
    """art: the map as drawn. sprites: (image, x, y). scene: ambient, lights, and pixels that give light."""
    W, H = art.size
    src, res = art.load(), Image.new('RGBA', (W, H)); px = res.load()
    feet = []
    for s, x, y in sprites:
        b = s.getbbox(); feet.append((x + (b[0] + b[2]) // 2, y + b[3] - 2))
    shade = []                          # per light: the pixels its light cannot reach
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
                        gx, gy = x + sx + dx / n * h * 0.8, fy + dy / n * h * 0.55
                        cut.add((round(gx), round(gy))); cut.add((round(gx) + 1, round(gy)))
        shade.append(cut)
    glow = scene.get('glow', lambda x, y, p: None)
    for y in range(H):
        for x in range(W):
            p = src[x, y]
            g = glow(x, y, p)
            if g:
                px[x, y] = g; continue
            a, k = lin(p), list(scene['ambient'])
            for L, cut in zip(scene['lights'], shade):
                if (x, y) not in cut:
                    v = step(L['field'](x, y), x, y)
                    k = [k[i] + v * L['col'][i] for i in range(3)]
            px[x, y] = out([a[i] * k[i] for i in range(3)])
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
                    px[x + sx, y + sy] = out([c * q for c, q in zip(lin(sp[sx, sy]), k)])
    return res.convert('RGB')


def sprite(src, row, col):
    return Image.open(os.path.join(m.HERE, src)).convert('RGBA').crop((col * 64, row * 64, col * 64 + 40, row * 64 + 64))


# ---------------------------------------------------------------- the office (make_room.py), three times of day
WALL = 64
office = m.room().im
cast = [(sprite(src, row, col), x, y) for src, row, col, x, y in m.PEOPLE]
SKY_DUSK = {m.BLU: (236, 128, 112), m.CYA: (250, 178, 110), m.WHT: (255, 214, 160), m.NAVY: (150, 84, 120), m.SL1: (70, 52, 92), m.SL2: (52, 40, 76), m.SL0: (86, 62, 104)}
SKY_NIGHT = {m.BLU: (26, 32, 66), m.CYA: (40, 50, 92), m.WHT: (50, 58, 100), m.NAVY: (18, 22, 48), m.SL1: (14, 16, 34), m.SL2: (10, 12, 28), m.SL0: (20, 22, 44), m.YEL: (255, 220, 120)}
PANES = [[(60, 98), (90, 98), (110, 142), (76, 142)], [(96, 98), (126, 98), (150, 142), (116, 142)]]
on_wall = lambda f: (lambda x, y: f(x, y) if y < WALL else 0)
on_floor = lambda f: (lambda x, y: f(x, y) if y >= WALL else 0)
both = lambda f, g: (lambda x, y: max(f(x, y), g(x, y)))
screen_f = both(on_wall(pool(184, 55, 62, 50)), on_floor(pool(178, 120, 100, 70)))
lamp_f = both(on_wall(pool(224, 52, 54, 42)), on_floor(pool(248, 118, 94, 74, 1.2)))


def office_glow(sky, screen, lamp):
    def glow(x, y, p):
        h = '%02x%02x%02x' % p[:3]
        if sky and 56 <= x < 116 and 18 <= y < 48 and h in sky and not (h == m.WHT and y >= 30):
            return sky[h] + (255,)
        if screen and 164 <= x < 204 and 44 <= y < 66:
            return (38, 132, 128, 255) if h == m.SL4 else out([c * k for c, k in zip(lin(p), (0.9, 2.2, 2.1))])
        if lamp and 208 <= x < 232 and 58 <= y < 71 and p[0] > 200:
            return out([c * 1.25 for c in lin(p)])
    return glow


SCREEN, LAMP = dict(col=(0.06, 0.50, 0.47), field=screen_f, at=(184, 96)), dict(col=(0.95, 0.52, 0.20), field=lamp_f, at=(222, 104))
OFFICE = {
    'day': dict(ambient=(0.80, 0.82, 0.90), glow=office_glow(None, False, False), lights=[
        dict(col=(0.34, 0.30, 0.18), field=on_floor(patches(*PANES))),
        dict(col=(0.14, 0.14, 0.12), field=lambda x, y: 1.0, dir=(0.62, 0.78))]),          # open sky: only its shadows show
    'dusk': dict(ambient=(0.20, 0.20, 0.33), glow=office_glow(SKY_DUSK, True, True), lights=[
        SCREEN, LAMP, dict(col=(0.50, 0.20, 0.30), field=on_floor(patches(*PANES)))]),
    'night': dict(ambient=(0.11, 0.12, 0.22), glow=office_glow(SKY_NIGHT, True, False), lights=[
        dict(col=(0.08, 0.72, 0.68), field=screen_f, at=(184, 96)),
        dict(col=(0.14, 0.18, 0.30), field=on_floor(patches(*PANES)))]),
}
rooms = {k: relight(office, cast, s) for k, s in OFFICE.items()}

# ---------------------------------------------------------------- the existing Hall, as it is in the game
X0, Y0, HW, HH = 700, 423, 528, 297
hall = Image.open(os.path.join(m.HERE, '../../public/Hall2.png')).convert('RGBA').crop((X0, Y0, X0 + HW, Y0 + HH))
hall_cast = [(sprite('../../public/Hero/Sprite-Hero.png', 2, 0), 190, 120), (sprite('../../public/characters/saruli.png', 0, 0), 300, 90),
             (sprite('dog.png', 1, 0), 236, 150), (sprite('visitor.png', 0, 0), 60, 60)]
HALL = dict(ambient=(0.30, 0.31, 0.46), lights=[
    dict(col=(0.95, 0.55, 0.22), field=pool(452, 150, 150, 120), at=(452, 150)),                 # a lamp over the lounge
    dict(col=(0.30, 0.42, 0.50), field=pool(-60, 297, 190, 200), at=(-60, 330))])                # daylight from the lower door
hall_before = hall.copy()
for s, x, y in hall_cast:
    hall_before.alpha_composite(s, (x, y))
hall_lit = relight(hall, hall_cast, HALL)

# ---------------------------------------------------------------- the sheet and the zoom
RW, RH = office.size
sheet = Image.new('RGB', (RW * 6 + 16, RH * 2 + HH * 2 + 8), (14, 12, 20))
for i, k in enumerate(('day', 'dusk', 'night')):
    sheet.paste(rooms[k].resize((RW * 2, RH * 2), Image.NEAREST), (i * (RW * 2 + 8), 0))
for i, im in enumerate((hall_before.convert('RGB'), hall_lit)):
    sheet.paste(im.resize((HW * 2, HH * 2), Image.NEAREST), (i * (HW * 2 + 8), RH * 2 + 8))
sheet.save(os.path.join(m.HERE, 'painted-light-pixels.png'))
rooms['dusk'].crop((150, 100, 310, 200)).resize((960, 600), Image.NEAREST).save(os.path.join(m.HERE, 'painted-light-zoom.png'))
print('painted-light-pixels.png and painted-light-zoom.png written; colours per panel:',
      {k: len(v.getcolors(99999)) for k, v in rooms.items()}, 'hall', len(hall_lit.getcolors(99999)))
