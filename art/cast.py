# The cast in the lived-in clutter style (#69), a first pass by script for Asi to touch up in Aseprite:
#   public/cast/<name>.png   Asi's sheet (public/characters/, public/Hero/) in the rooms' colours, one 256x256 sheet
#     per light, stacked: sheet level index * 2 + 1 when the light comes from the right (draw.LEVELS, as room.py
#     writes the rooms' light grids). Sprite.draw picks the sheet for the tile under the figure's feet.
# and art/check/cast.png, not committed: every figure's front frame on every sheet, at 4x.
# The drawing and the thin outline stay Asi's. Each colour of a sheet is a part, (ramp, level in daylight); the
# light where the figure stands moves every part by the same steps, so the sheet's own shading stays one step
# apart, and the side of the figure away from the light is one step darker. None is the outline: K, never lit.
# Asi's files are only read. A frame is read from its left 40 px: the figures are 31 px wide, and saruli.png has
# 9 stray pixels at the right edge of three frames, which this leaves out.
# usage (repo root): npm run cast     or: python3 -I art/cast.py
import os, sys
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))     # python3 -I leaves the script's folder out
import draw
from draw import CARD, DESK, FLOOR, GREEN, METAL, PAPER, RED, TEAL, LEVELS, RAMPS, K, rgb

ART = os.path.dirname(os.path.abspath(__file__))
PUBLIC = os.path.join(ART, '..', 'public')
OUT = os.path.join(PUBLIC, 'cast')
FRAME, READ = 64, 40

WHITE, EYES, SKIN, SKIN_SHADE = (PAPER, 5), (DESK, 2), (CARD, 4), (CARD, 3)
LINE = {'000000': None, '150908': None}
CAST = {
    'hero': ('Hero/Sprite-Hero.png', {**LINE, '191919': (METAL, 1), '121212': (METAL, 1), '373737': (METAL, 2),
             '4c4c4c': (METAL, 2.4), '6c6c6c': (METAL, 3.4),                            # beard, trousers; grey hair
             '513407': EYES, 'ffffff': WHITE, 'ebbf96': SKIN, 'cba582': SKIN_SHADE,
             '0989a0': (TEAL, 3), '076a7c': (TEAL, 2)}),                                 # the teal tee
    'saruli': ('characters/saruli.png', {**LINE, '4e2f0a': (DESK, 2.6), '402708': (DESK, 1.6), '663d0d': (DESK, 3.6),
               'ffcf4f': (FLOOR, 5), 'a44545': (RED, 3), 'a83e3e': (RED, 3),          # earrings; lips, shoes
               'edb384': SKIN, 'e3ab7e': SKIN, 'b18562': SKIN_SHADE, 'ffffff': WHITE,
               '3a4d8a': (METAL, 2.4), '27325b': (METAL, 1.4)}),                        # the dress
    'chich': ('characters/chich.png', {**LINE, '191919': None, '767676': (METAL, 3), 'cecece': (PAPER, 4.5),
              '392505': EYES, '513407': EYES, 'ffffff': WHITE, 'ebbf96': SKIN, 'cba582': SKIN_SHADE,
              'f8f8f8': (PAPER, 5), 'd6d6d6': (PAPER, 4),                              # the white tee and its print:
              '87f1f8': (TEAL, 4.5), '58d652': (GREEN, 4), 'e487f8': (RED, 2), '4538f5': (METAL, 2), 'f53838': (RED, 3),
              '402b21': (DESK, 1.8)}),                                                  # shorts
    'iluz': ('characters/iluz.png', {**LINE, '731f76': (RED, 2), '6c6c6c': (METAL, 3), '191919': (METAL, 1),
             'ffffff': WHITE, 'ae8054': (CARD, 3), '8f6945': (CARD, 2),
             '777777': (METAL, 3), 'd8d8d8': (PAPER, 5), '4bb5a2': (TEAL, 4), '3659cc': (METAL, 2),   # chain, pendant
             'ac4bb5': (RED, 2.6), '8b3d92': (RED, 1.6),                                # the purple shirt
             '31426e': (METAL, 1.8), '253253': (METAL, .8)}),                           # jeans
    'alien': ('characters/alien.png', {**LINE, '191919': None, '20a967': (GREEN, 3.4), '18814f': (GREEN, 2.4),
              '7a20a9': (RED, 2)}),
}


def figure(src, table, here, from_right):
    """One frame (src: its pixels) in the room's colours for the light where the figure stands, as (x, y, colour)."""
    for sy in range(FRAME):
        xs = [sx for sx in range(READ) if src[sx, sy][3]]
        for sx in xs:
            part = table['%02x%02x%02x' % src[sx, sy][:3]]
            if part is None:
                yield sx, sy, rgb(K); continue
            far = (sx - xs[0]) < .3 * (xs[-1] - xs[0]) if from_right else (xs[-1] - sx) < .3 * (xs[-1] - xs[0])
            step = max(2 if part[1] >= 2.5 else 1, min(6, int(part[1] + here + .5)))
            yield sx, sy, rgb(RAMPS[part[0]][step - far])


def sheets(src, table):
    s = Image.open(os.path.join(PUBLIC, src)).convert('RGBA')
    assert s.size == (4 * FRAME, 4 * FRAME), (src, s.size)
    px = s.load()
    out = Image.new('RGBA', (4 * FRAME, 4 * FRAME * len(LEVELS) * 2))
    for v in range(len(LEVELS) * 2):
        for fy in range(4):
            for fx in range(4):
                frame = Image.new('RGBA', (FRAME, FRAME))
                crop = s.crop((fx * FRAME, fy * FRAME, fx * FRAME + FRAME, fy * FRAME + FRAME)).load()
                for x, y, c in figure(crop, table, LEVELS[v // 2], v % 2):
                    frame.putpixel((x, y), (*c, 255))
                out.paste(frame, (fx * FRAME, v * 4 * FRAME + fy * FRAME))
    return out


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True); os.makedirs(os.path.join(ART, 'check'), exist_ok=True)
    built = {}
    for name, (src, table) in CAST.items():
        built[name] = sheets(src, table)
        built[name].save(os.path.join(OUT, name + '.png'))
    n = len(LEVELS) * 2
    check = Image.new('RGBA', (n * 36, len(built) * FRAME), rgb(RAMPS[draw.WALL][3]))
    for i, im in enumerate(built.values()):
        for v in range(n):
            check.alpha_composite(im.crop((0, v * 4 * FRAME, 32, v * 4 * FRAME + FRAME)), (v * 36 + 2, i * FRAME))
    check.resize((check.width * 4, check.height * 4), Image.NEAREST).save(os.path.join(ART, 'check', 'cast.png'))
    print('cast: %s, %d sheets each, into %s' % (', '.join(built), n, os.path.normpath(OUT)))
