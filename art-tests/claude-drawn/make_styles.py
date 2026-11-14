# Four takes on the same room, to find a style (#61). Asi on the detailed version: "It's nice. Everything feels a
# bit like 2012 freepik pixel art. We miss some style no?" Same drawing in every panel, ENDESGA 32 only; what
# changes is the palette, the light and the outline. Writes styles.png (2 x 2, each panel at 2x):
#   top left: as drawn                      top right: dusk, the lamp and the screen are the only light
#   bottom left: slate world, warm accents  bottom right: toned outlines instead of one dark ink
# usage (repo root): python3 -I art-tests/claude-drawn/make_styles.py
import colorsys, os, sys
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import make_room as m

SLATE = ['181425', '262b44', '3a4466', '5a6988', '8b9bb4', 'c0cbdc', 'ffffff']
WARM = ['3e2731', 'a22633', 'be4a2f', 'f77622', 'feae34', 'fee761']


def lum(p):
    return 0.3 * p[0] + 0.59 * p[1] + 0.11 * p[2]


def remap(im, fn):
    out = im.copy(); px = out.load(); cache = {}
    for y in range(out.height):
        for x in range(out.width):
            k = (px[x, y], x, y) if fn.__code__.co_argcount == 3 else px[x, y]
            if k not in cache:
                cache[k] = fn(*((px[x, y], x, y) if fn.__code__.co_argcount == 3 else (px[x, y],)))
            px[x, y] = cache[k]
    return out


def duotone(p):  # everything becomes slate blue, except strong reds, oranges and yellows
    if '%02x%02x%02x' % p[:3] in ('e8b796', 'c28569'):          # skin stays skin
        return p
    h, s, _ = colorsys.rgb_to_hsv(p[0] / 255, p[1] / 255, p[2] / 255)
    ramp = WARM if (s > 0.7 and (h < 0.17 or h > 0.93)) or p[:3] == (0xfe, 0xe7, 0x61) else SLATE
    return min((m.rgb(c) for c in ramp), key=lambda c: abs(lum(c) - lum(p)))


def dusk(p, x, y):  # hard-edged pools of light around the lamp and the screen, two steps darker elsewhere
    lamp = ((x - 219) ** 2 + ((y - 80) * 1.4) ** 2) ** 0.5
    screen = ((x - 184) ** 2 + ((y - 66) * 1.4) ** 2) ** 0.5
    lit = 164 <= x < 204 and 44 <= y < 66                      # the screen itself
    steps = 0 if lit or lamp < 36 else 1 if lamp < 66 or screen < 34 else 2
    return m.darker(p, steps)


base = m.people(m.room()).im
m.TONED = True
toned = m.people(m.room()).im
panels = [base, remap(base, dusk), remap(base, duotone), toned]
sheet = Image.new('RGBA', (m.W * 2 + 4, m.H * 2 + 4), m.rgb('181425'))
for i, p in enumerate(panels):
    used = {'%02x%02x%02x' % c[:3] for _, c in p.getcolors(99999)}
    assert used <= m.E32, used - m.E32
    sheet.paste(p, ((i % 2) * (m.W + 4), (i // 2) * (m.H + 4)))
sheet.resize((sheet.width * 2, sheet.height * 2), Image.NEAREST).save(os.path.join(m.HERE, 'styles.png'))
print('styles.png written; all ENDESGA 32')
