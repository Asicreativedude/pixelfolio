# All ten direction stills on one labelled sheet: directions.png, two columns, each still at full size.
# usage (repo root): python3 -I art-tests/claude-drawn/directions/make_sheet.py
import glob, os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
NAMES = ['Muted world, loud clickables', 'Naive flat cartoon', 'Neon flat minimalism', 'One-bit plus one accent',
         'Lamp-lit dusk', 'Lived-in clutter', 'Soft diorama', 'Desktop chrome', 'Portrait-led PC-98', 'Paper cut-out']
W, H, BAR, GAP = 1056, 720, 44, 12
files = sorted(glob.glob(os.path.join(HERE, 'd[0-9][0-9]-*.png')))
assert [int(os.path.basename(f)[1:3]) for f in files] == list(range(1, 11)), [os.path.basename(f) for f in files]
sheet = Image.new('RGB', (2 * W + GAP, 5 * (H + BAR + GAP) - GAP), (14, 12, 20))
font = ImageFont.load_default()
for i, f in enumerate(files):
    im = Image.open(f).convert('RGB')
    assert im.size == (W, H), (f, im.size)
    x, y = i % 2 * (W + GAP), i // 2 * (H + BAR + GAP)
    label = Image.new('RGB', (W // 3, BAR // 3), (14, 12, 20))          # small text, enlarged 3x with hard edges
    ImageDraw.Draw(label).text((3, 2), '%d. %s' % (i + 1, NAMES[i]), fill=(255, 255, 255), font=font)
    sheet.paste(label.resize((W, BAR // 3 * 3), Image.NEAREST), (x, y))
    sheet.paste(im, (x, y + BAR))
sheet.save(os.path.join(HERE, 'directions.png'))
print('directions.png', sheet.size)
