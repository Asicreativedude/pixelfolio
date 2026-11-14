# The painted-light look brought into the pixel-art room (#65). Asi, on office-painted.png: "Can we somehow get
# the painted light style into our pixel art world?"
# What makes that painting is not the brush, it is the light: a dark cool room, a teal screen and an orange lamp
# as the only sources, light pools with hard ragged edges, and every cast shadow filled by the OTHER light.
# This script keeps the pixel art exactly as drawn (make_room.py's room, the pixel cast) and repaints only the
# light, with the painting's own recipe: colour = shadow + t * (teal-lit - shadow) + w * (lamp-lit - shadow),
# mixed in linear light, t and w stepped into four flat levels with a noisy edge.
# Writes painted-light-pixels.png: the room as drawn (left) and in painted light (right), both at 3x.
# The result is NOT ENDESGA 32: the light makes its own colours. It is cut to 64 colours at the end.
# usage (repo root): python3 -I art-tests/claude-drawn/make_painted_light.py
import math, os, sys
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import make_room as m

W, H, WALL = m.W, m.H, 64                       # WALL: where the back wall meets the floor
AMBIENT = (0.055, 0.06, 0.13)                    # the room with both lights off: cool, dark
TEAL, WARM, DUSK = (0.10, 1.00, 0.92), (1.55, 0.80, 0.30), (1.00, 0.42, 0.62)
SCREEN, LAMP = (184, 55), (220, 64)             # where the two lights sit
LEVELS, CUTS = (0, 0.3, 0.62, 1), (0.1, 0.38, 0.66)
PANES = [[(60, 98), (90, 98), (110, 142), (76, 142)], [(96, 98), (126, 98), (150, 142), (116, 142)]]


def clamp(v):
    return 0 if v < 0 else 1 if v > 1 else v


def noise(x, y, seed, s=16):                    # smooth value noise, so a level's edge wanders like a brushed one
    def h(ix, iy):
        n = (ix * 374761393 + iy * 668265263 + seed * 974711) & 0xffffffff
        n = ((n ^ (n >> 13)) * 1274126177) & 0xffffffff
        return ((n ^ (n >> 16)) & 0xffff) / 65535
    fx, fy = x / s, y / s
    ix, iy = math.floor(fx), math.floor(fy)
    tx, ty = fx - ix, fy - iy
    tx, ty = tx * tx * (3 - 2 * tx), ty * ty * (3 - 2 * ty)
    a, b = h(ix, iy) + (h(ix + 1, iy) - h(ix, iy)) * tx, h(ix, iy + 1) + (h(ix + 1, iy + 1) - h(ix, iy + 1)) * tx
    return a + (b - a) * ty


def step(v, x, y, seed):                        # four flat levels, never a gradient
    v += (noise(x, y, seed) - 0.5) * 0.16 * min(1, v * 5)      # no stray flecks out in the dark
    return LEVELS[sum(v > c for c in CUTS)]


def inside(poly, x, y):
    hit = False
    for (x0, y0), (x1, y1) in zip(poly, poly[1:] + poly[:1]):
        if (y0 > y) != (y1 > y) and x < x0 + (y - y0) * (x1 - x0) / (y1 - y0):
            hit = not hit
    return hit


def teal(x, y):                                 # the screen: a glow on the wall, a pool on the desk and floor
    wall = 0.8 * clamp(1 - math.hypot(max(abs(x - SCREEN[0]) - 20, 0), max(abs(y - SCREEN[1]) - 11, 0)) / 42) if y < WALL else 0
    pool = clamp(1.15 - math.hypot((x - 176) / 104, (y - 122) / 74)) if y >= WALL else 0
    return max(wall, pool)


def warm(x, y):                                 # the lamp: a cone on the wall, a pool to the right
    wall = clamp(1.15 - math.hypot((x - 224) / 56, (y - 50) / 44)) if y < WALL else 0
    pool = clamp(1.2 - math.hypot((x - 250) / 96, (y - 120) / 78)) if y >= WALL else 0
    return max(wall, pool)


def lin(p):
    return [(v / 255) ** 2.2 for v in p[:3]]


def out(v):
    return tuple(round(255 * clamp(c) ** (1 / 2.2)) for c in v) + (255,)


def light(albedo, t, w, d=0):
    a = lin(albedo)
    sh = [a[i] * AMBIENT[i] + 0.004 for i in range(3)]
    return out([sh[i] + t * (a[i] * TEAL[i] - sh[i]) + w * (a[i] * WARM[i] - sh[i]) + d * (a[i] * DUSK[i] - sh[i]) for i in range(3)])


def shadow(feet, src, length=64):               # the streak a standing figure throws away from one light
    dx, dy = feet[0] - src[0], feet[1] - (src[1] + 40)
    n = math.hypot(dx, dy) or 1
    dx, dy = dx / n, dy / n
    px, py = -dy, dx
    f, e = feet, (feet[0] + dx * length, feet[1] + dy * length * 0.8)
    return [(f[0] + px * 6, f[1] + py * 3), (e[0] + px * 11, e[1] + py * 6), (e[0] - px * 11, e[1] - py * 6), (f[0] - px * 6, f[1] - py * 3)]


room = m.room().im
cast = []
for src, row, col, x, y in m.PEOPLE:
    s = Image.open(os.path.join(m.HERE, src)).convert('RGBA').crop((col * 64, row * 64, col * 64 + 40, row * 64 + 64))
    box = s.getbbox()
    cast.append((s, x, y, (x + (box[0] + box[2]) / 2, y + box[3] - 2)))
no_lamp = [shadow(f, LAMP) for _, _, _, f in cast]          # the lamp cannot reach here: only teal is left
no_screen = [shadow(f, SCREEN) for _, _, _, f in cast]

lit = Image.new('RGBA', (W, H)); px, src = lit.load(), room.load()
SKY = {m.rgb(m.BLU): (236, 128, 112), m.rgb(m.CYA): (250, 178, 110), m.rgb(m.WHT): (255, 214, 160), m.rgb(m.NAVY): (150, 84, 120),
       m.rgb(m.SL1): (70, 52, 92), m.rgb(m.SL2): (52, 40, 76), m.rgb(m.SL0): (86, 62, 104)}
for y in range(H):
    for x in range(W):
        p = src[x, y]
        if 164 <= x < 204 and 44 <= y < 66:                                     # the screen gives light
            px[x, y] = out([c * k for c, k in zip(lin(p), (0.9, 2.2, 2.1))]) if p != m.rgb(m.SL4) else (38, 132, 128, 255)
        elif 56 <= x < 116 and 18 <= y < 48 and p in SKY and p != m.rgb(m.WHT) or (56 <= x < 116 and 18 <= y < 30 and p == m.rgb(m.WHT)):
            px[x, y] = SKY[p] + (255,)                                           # dusk outside
        elif 208 <= x < 232 and 58 <= y < 71 and p[0] > 200:                    # the lamp shade glows
            px[x, y] = out([c * 1.25 for c in lin(p)])
        else:
            t = 0 if any(inside(q, x, y) for q in no_screen) else step(teal(x, y), x, y, 41)
            w = 0 if any(inside(q, x, y) for q in no_lamp) else step(warm(x, y), x, y, 43)
            d = 0.8 if y >= WALL and any(inside(q, x, y) for q in PANES) else 0
            px[x, y] = light(p, t, w, d)
for s, x, y, feet in cast:                                                       # each figure: lit on the side that faces a light
    sp, cx = s.load(), feet[0] - x
    t0, w0 = step(teal(*feet), feet[0], feet[1], 41), step(warm(*feet), feet[0], feet[1], 43)
    for sy in range(64):
        for sx in range(40):
            if sp[sx, sy][3]:
                t = t0 * (1 if (sx - cx) * (SCREEN[0] - feet[0]) > 0 else 0.3)
                w = w0 * (1 if (sx - cx) * (LAMP[0] - feet[0]) > 0 or abs(LAMP[0] - feet[0]) < 24 else 0.3)
                px[x + sx, y + sy] = light(sp[sx, sy], max(t, 0.12 * t0), max(w, 0.12 * w0))
lit = lit.convert('RGB').quantize(64, method=Image.MEDIANCUT, dither=Image.NONE).convert('RGB')

before = m.people(m.room()).im.convert('RGB')
sheet = Image.new('RGB', (W * 2 + 4, H), (14, 12, 20))
sheet.paste(before, (0, 0)); sheet.paste(lit, (W + 4, 0))
sheet.resize((sheet.width * 3, sheet.height * 3), Image.NEAREST).save(os.path.join(m.HERE, 'painted-light-pixels.png'))
# second way in: the painting itself, shrunk to the game's 640x360 canvas and to half of it, 64 colours each
paint = Image.open(os.path.join(m.HERE, 'office-painted.png')).convert('RGB')
baked = Image.new('RGB', (1280 * 2 + 4, 720), (14, 12, 20))
for i, (w, h) in enumerate(((640, 360), (320, 180))):
    small = paint.resize((w, h), Image.BOX).quantize(64, method=Image.MEDIANCUT, dither=Image.NONE).convert('RGB')
    baked.paste(small.resize((1280, 720), Image.NEAREST), (i * 1284, 0))
baked.save(os.path.join(m.HERE, 'painted-baked-pixels.png'))
n = len(lit.getcolors(99999))
assert n <= 64, n
print('painted-light-pixels.png written;', n, 'colours in the lit room')
