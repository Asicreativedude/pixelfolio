# Light, fourth try (#65), after reading how shipped pixel games and pixel artists do it
# (research_notes/Pixel art lighting/). What the third version did that no documented game does: rings of light,
# dither on the rings, one dark blue multiplied over everything, sprite-shaped shadows, colours snapped to a
# palette after blending, and no response to where the lamp is. This script drops all of that and shows the dusk
# office and the Hall two ways:
#   soft  (left):  what most games do (Stardew Valley, Graveyard Keeper, Celeste). Smooth light at screen
#                  resolution over untouched pixel art, a little bloom round the lamp and the screen.
#   pixel (right): light kept on the pixel grid, by the craft rules. One hard-edged shape per light, no rings,
#                  no dither. Characters get a rim of light on the lamp side and stay dark on the far side.
# Shared by both:
#   Night is a table, not a wash: every drawn colour has one dusk colour (darker, turned towards blue-violet,
#     saturation kept) and one colour per light. A lit area returns the art to nearly its own colours.
#   Shadows are a blob under each character. Props keep the contact shadows drawn into the art.
# The pixel version only ever uses table colours, so its palette is fixed: drawn colours x (dusk, shade, lights).
# Writes light-two-ways.png, light-soft.png, light-pixel.png and directions/d05-lamp-lit-dusk.png (the soft one).
# usage (repo root): python3 -I art-tests/claude-drawn/make_light_two_ways.py
import math, os, sys
import numpy as np
from PIL import Image, ImageFilter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import make_room as m


# ---------------------------------------------------------------- colour (OKLab, as in make_painted_light.py)
def oklab(p):
    c = [(v / 255) ** 2.2 for v in p[:3]]
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
    return tuple(round(255 * min(1, max(0, v)) ** (1 / 2.2)) for v in c)


# state: (brightness kept, brightness added, colour kept, hue of the tint in degrees, amount of tint)
STATES = {'dusk': (0.60, 0.035, 0.85, 275, 0.035), 'shade': (0.47, 0.03, 0.85, 275, 0.035),
          'lamp': (0.97, 0.02, 0.92, 65, 0.022), 'screen': (0.78, 0.03, 0.80, 195, 0.045),
          'sun': (0.74, 0.04, 0.85, 15, 0.04), 'door': (0.84, 0.03, 0.90, 235, 0.02)}
TABLE = {}


def grade(p, state):
    """The colour table: what a drawn colour becomes in a state. One entry per colour and state, nothing else."""
    key = (p[:3], state)
    if key not in TABLE:
        k, add, keep, hue, tint = STATES[state]
        L, a, b = oklab(p)
        TABLE[key] = from_oklab(L * k + add, a * keep + tint * math.cos(math.radians(hue)), b * keep + tint * math.sin(math.radians(hue)))
    return TABLE[key]


RIM = (255, 226, 160)


def graded(im, state):
    out = im.convert('RGB'); px = out.load()
    for y in range(out.height):
        for x in range(out.width):
            px[x, y] = grade(px[x, y], state)
    return out


def ease(t):
    t = np.clip(t, 0, 1)
    return t * t * (3 - 2 * t)


def ell(cx, cy, rx, ry):                # distance from the centre of an ellipse, 1 at its edge
    return lambda x, y: np.hypot((x - cx) / rx, (y - cy) / ry)


def feet_of(s, x, y):
    b = s.getbbox()
    return x + (b[0] + b[2]) // 2, y + b[3] - 2


# ---------------------------------------------------------------- the two ways
def soft(sc, scale):
    """Smooth light at screen resolution, the way most pixel games do it."""
    art = sc['art'].copy()
    for s, x, y in sc['sprites']:
        art.alpha_composite(s, (x, y))
    W, H = art.size
    big = lambda im: np.asarray(im.resize((W * scale, H * scale), Image.NEAREST), dtype=float)
    out = big(graded(art, 'dusk'))
    yy, xx = np.mgrid[0:H * scale, 0:W * scale] / scale
    for s, x, y in sc['sprites']:                                   # blob shadows, soft
        fx, fy = feet_of(s, x, y)
        w = ease(1.25 - ell(fx, fy + 1, 13, 5)(xx, yy))[..., None] * 0.55
        out = out * (1 - w) + big(graded(art, 'shade')) * w
    for L in sc['lights']:
        w = (ease(L['soft'](xx, yy)) * L.get('strength', 1))[..., None]
        out = out * (1 - w) + big(graded(art, L['state'])) * w
    glow = Image.new('RGB', (W, H))
    gp, ap = glow.load(), art.load()
    for y in range(H):
        for x in range(W):
            g = sc['emits'](x, y, ap[x, y])
            if g:
                gp[x, y] = g
    g1 = np.asarray(glow.resize((W * scale, H * scale), Image.NEAREST), dtype=float)
    out = np.where(g1.sum(2, keepdims=True) > 0, g1, out)
    bloom = np.asarray(glow.resize((W * scale, H * scale), Image.NEAREST).filter(ImageFilter.GaussianBlur(7 * scale)), dtype=float)
    out = 255 - (255 - out) * (255 - bloom * 0.9) / 255              # screen blend: light only adds
    return Image.fromarray(np.clip(out, 0, 255).astype('uint8'))


def pixel(sc, scale):
    """Light on the pixel grid: one hard-edged shape per light, colours only from the table."""
    art = sc['art']
    W, H = art.size
    src = art.load()

    def state_at(x, y):
        st = 'dusk'
        for L in sc['lights']:
            if L['soft'](x, y) > L.get('edge', 0.42):
                st = L['state']
        return st

    st = [[state_at(x, y) for x in range(W)] for y in range(H)]
    for s, x, y in sc['sprites']:                                   # blob shadows: a flat ellipse
        fx, fy = feet_of(s, x, y)
        for by in range(fy - 3, fy + 5):
            for bx in range(fx - 12, fx + 13):
                if 0 <= bx < W and 0 <= by < H and ell(fx, fy + 1, 12, 4)(bx, by) <= 1:
                    st[by][bx] = 'shade'
    out = Image.new('RGB', (W, H)); px = out.load()
    for y in range(H):
        for x in range(W):
            px[x, y] = sc['emits'](x, y, src[x, y]) or grade(src[x, y], st[y][x])
    for s, x, y in sc['sprites']:
        fx, fy = feet_of(s, x, y)
        base, sp = state_at(fx, fy), s.load()
        at = next((L['at'] for L in sc['lights'] if L['state'] == base and 'at' in L), None)
        side = 0 if not at or abs(at[0] - fx) < 8 else (1 if at[0] > fx else -1)     # which way the light is
        clear = lambda qx, qy: not (0 <= qx < s.width and 0 <= qy < s.height) or not sp[qx, qy][3]
        for sy in range(s.height):
            for sx in range(s.width):
                if not sp[sx, sy][3] or not (0 <= x + sx < W and 0 <= y + sy < H):
                    continue
                c = grade(sp[sx, sy], base)
                if side:
                    if clear(sx + side, sy):                         # the edge facing the light: a rim
                        c = tuple((a + 2 * b) // 3 for a, b in zip(c, RIM))
                    elif clear(sx - side, sy) or clear(sx - 2 * side, sy) or clear(sx - 3 * side, sy):
                        c = grade(sp[sx, sy], 'dusk')                # the far side stays in the dark
                px[x + sx, y + sy] = c
    return out.resize((W * scale, H * scale), Image.NEAREST)


def sprite(src, row, col):
    return Image.open(os.path.join(m.HERE, src)).convert('RGBA').crop((col * 64, row * 64, col * 64 + 40, row * 64 + 64))


# ---------------------------------------------------------------- the office at dusk
SKY = {m.BLU: (236, 128, 112), m.CYA: (250, 178, 110), m.WHT: (255, 214, 160), m.NAVY: (150, 84, 120), m.SL1: (70, 52, 92), m.SL2: (52, 40, 76), m.SL0: (86, 62, 104)}


def office_emits(x, y, p):
    h = '%02x%02x%02x' % p[:3]
    if 56 <= x < 116 and 18 <= y < 48 and h in SKY and not (h == m.WHT and y >= 30):
        return SKY[h]
    if 164 <= x < 204 and 44 <= y < 66:                             # the screen
        return (38, 132, 128) if h == m.SL4 else from_oklab(*[v * k for v, k in zip(oklab(p), (1.25, 1, 1))])
    if 208 <= x < 232 and 58 <= y < 71 and p[0] > 200:              # the lamp shade
        return from_oklab(*[v * k for v, k in zip(oklab(p), (1.08, 1, 1))])


def in_panes(x, y):                     # last daylight through the window, two slanted patches on the floor
    x, y = np.asarray(x, dtype=float), np.asarray(y, dtype=float)
    t = (y - 98) / 44
    hit = lambda x0, x1, d0, d1: (x > x0 + d0 * t) & (x < x1 + d1 * t)
    return np.where((t > 0) & (t < 1) & (hit(60, 90, 16, 20) | hit(96, 126, 20, 24)), 1.0, 0.0)


def lamp_shape(x, y):                   # a cone up the wall from the shade, a pool on the desk and floor below it
    x, y = np.asarray(x, dtype=float), np.asarray(y, dtype=float)
    wall = np.where(y < 64, (1 - np.abs(x - 220) / (16 + (64 - y) * 0.95)) * 0.7, 0)
    return np.maximum(wall, 1.12 - ell(246, 124, 92, 62)(x, y))


def screen_shape(x, y):                 # spills forward from the screen over the keyboard, the chair and the floor
    x, y = np.asarray(x, dtype=float), np.asarray(y, dtype=float)
    return np.where((y >= 60) & (y < 168), (1 - np.abs(x - 182) / (26 + (y - 60) * 0.42)) * (1 - (y - 60) / 150), 0)


OFFICE = dict(art=m.room().im, sprites=[(sprite(src, row, col), x, y) for src, row, col, x, y in m.PEOPLE], emits=office_emits, lights=[
    dict(state='sun', soft=in_panes, strength=0.8, edge=0.5),
    dict(state='screen', soft=screen_shape, at=(184, 96), strength=0.9, edge=0.22),
    dict(state='lamp', soft=lamp_shape, at=(222, 104), edge=0.3)])

# ---------------------------------------------------------------- the existing Hall
X0, Y0, HW, HH = 700, 423, 528, 297
HALL = dict(art=Image.open(os.path.join(m.HERE, '../../public/Hall2.png')).convert('RGBA').crop((X0, Y0, X0 + HW, Y0 + HH)),
            sprites=[(sprite('../../public/Hero/Sprite-Hero.png', 2, 0), 190, 120), (sprite('../../public/characters/saruli.png', 0, 0), 330, 96),
                     (sprite('dog.png', 1, 0), 236, 150), (sprite('visitor.png', 0, 0), 60, 60)],
            emits=lambda x, y, p: None, lights=[
    dict(state='door', soft=lambda x, y: 1.1 - ell(-40, 310, 200, 190)(x, y), at=(-60, 330), strength=0.9, edge=0.35),
    dict(state='lamp', soft=lambda x, y: 1.15 - ell(452, 150, 160, 128)(x, y), at=(452, 150), edge=0.3)])

if __name__ == '__main__':
    panels = [soft(OFFICE, 3), pixel(OFFICE, 3), soft(HALL, 2), pixel(HALL, 2)]
    panels[0].save(os.path.join(m.HERE, 'light-soft.png')); panels[1].save(os.path.join(m.HERE, 'light-pixel.png'))
    panels[0].save(os.path.join(m.HERE, 'directions/d05-lamp-lit-dusk.png'))
    used = {c for im in (panels[1], panels[3]) for _, c in im.getcolors(99999)}
    drawn = {k[0] for k in TABLE}
    print('pixel way:', len(used), 'colours, from', len(drawn), 'drawn colours in', len(STATES), 'states')
    sheet = Image.new('RGB', (1056 * 2 + 8, 720 + 8 + HH * 2), (14, 12, 20))
    for i, im in enumerate(panels):
        sheet.paste(im, (i % 2 * 1064, i // 2 * 728))
    sheet.save(os.path.join(m.HERE, 'light-two-ways.png'))
