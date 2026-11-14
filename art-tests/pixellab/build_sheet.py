# Pack PixelLab direction frames into Pixelfolio's 256x256 sheet (4x4 grid of 64x64 frames).
# Rows: down, left, right, up. Columns: idle, walk-a, walk-b (column 3 unused), as sprite.ts expects.
# Each frame is scaled (nearest) then centred on its canvas centre, so frames of different canvas
# sizes (32 idle vs 40 walk) line up. The whole sheet is shifted so the south idle's art sits where
# the existing characters' art sits: horizontal centre x=16, feet y=61.
#
# usage: python3 -I build_sheet.py OUT.png SCALE DIR/{south,west,east,north}: idle walkA walkB ...
#   python3 -I build_sheet.py out.png 2 s_idle.png s_a.png s_b.png w_idle.png ... (12 paths, row order)
import sys
from PIL import Image

out, scale, *paths = sys.argv[1:]
scale = int(scale)
assert len(paths) == 12, 'need 12 frames: 4 rows x (idle, walkA, walkB)'
frames = [Image.open(p).convert('RGBA') for p in paths]
frames = [f.resize((f.width * scale, f.height * scale), Image.NEAREST) for f in frames]

def centred(f):
    c = Image.new('RGBA', (128, 128))
    c.alpha_composite(f, ((128 - f.width) // 2, (128 - f.height) // 2))
    return c

frames = [centred(f) for f in frames]
x0, _, x1, y1 = frames[0].getbbox()  # south idle
dx, dy = 16 - (x0 + x1) // 2, 61 - y1

sheet = Image.new('RGBA', (256, 256))
for i, f in enumerate(frames):
    row, col = divmod(i, 3)
    cell = Image.new('RGBA', (64, 64))
    cell.alpha_composite(f.crop((-dx, -dy, -dx + 64, -dy + 64)))
    sheet.alpha_composite(cell, (col * 64, row * 64))
sheet.save(out)
print(out, 'offset', dx, dy)
