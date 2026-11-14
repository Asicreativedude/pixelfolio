# Direction 6 (lived-in clutter) as a room the game can load: ../game/
#   clutter-day.png, clutter-evening.png   the room without its cast, 352x240, one screen pixel per art pixel
#   hero.png, dana.png, visitor.png, dog.png   the cast's full sheets in the room's colours. Each file stacks one
#     256x256 sheet per light (LEVELS x light from the left or the right); the game picks the sheet for the tile
#     the figure stands on, so the cast is lit by the room as in the still. The contact shadow is in the sheet.
#   clutter.json   walls, and for day and evening which sheet to use on each tile
# The game puts a figure at x = (col + 1) * 32, y = (row - 1) * 32 for the tile (col, row) under its feet, and
# draws its 64 px frame with the top left at (col * 32, row * 32 - 36).
# usage (repo root): python3 -I art-tests/claude-drawn/directions/make_d06_game.py
import json, os, sys
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))     # python3 -I leaves the script's folder out
import make_d06_lived_in_clutter as m

OUT = os.path.join(m.HERE, '..', 'game')
WALK = {3: (1, 2, 8), 4: (2, 3, 6, 7, 8), 5: (2, 3, 4, 5, 6, 7, 8), 6: (2, 3, 5)}       # row: columns free to stand on
LEVELS = [-1, -.5, 0, .5, 1, 1.5]
SHADOW = bytes.fromhex(m.K)


def key(col, row):
    return '%d,%d' % ((col + 1) * 32, (row - 1) * 32)


def sheets(src, table):
    s = Image.open(os.path.join(m.HERE, '..', src)).convert('RGBA')
    out = Image.new('RGBA', (256, 256 * len(LEVELS) * 2))
    for v in range(len(LEVELS) * 2):
        for fy in range(4):
            x0, _, x1, _ = s.crop((0, fy * 64, 64, fy * 64 + 64)).getbbox()
            for fx in range(4):
                frame = Image.new('RGBA', (64, 64))
                d = ImageDraw.Draw(frame)
                d.ellipse((x0 - 2, 57, x1 + 1, 65), fill=(*SHADOW, 60)); d.ellipse((x0 + 2, 59, x1 - 3, 64), fill=(*SHADOW, 120))
                px = s.crop((fx * 64, fy * 64, fx * 64 + 64, fy * 64 + 64)).load()
                for sx, sy, c in m.figure(px, table, LEVELS[v // 2], v % 2, w=64):
                    frame.putpixel((sx, sy), (*c, 255))
                out.paste(frame, (fx * 64, v * 256 + fy * 64))
    return out


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    people, light = list(m.PEOPLE), {}
    m.PEOPLE.clear()                                            # the room alone: no figures, no shadows under them
    for name, evening in (('day', False), ('evening', True)):
        room = m.build(evening)
        room.save(os.path.join(OUT, 'clutter-%s.png' % name))
        light[name] = {}
        for row, cols in WALK.items():
            for col in cols:
                here, from_right = m.standing(room.light, col * 32, row * 32 - 36)
                level = min(range(len(LEVELS)), key=lambda i: abs(LEVELS[i] - here))
                assert abs(LEVELS[level] - here) <= .5, (name, col, row, here)      # LEVELS covers every tile
                light[name][key(col, row)] = level * 2 + from_right
    for src, _, _, _, table in people:
        sheets(src, table).save(os.path.join(OUT, src.replace('-detailed', '')))
    walls = [key(c, r) for r in range(1, 8) for c in range(11) if c not in WALK.get(r, ())]
    json.dump({'walls': walls, 'light': light}, open(os.path.join(OUT, 'clutter.json'), 'w'), indent=1)
    print('written to', os.path.normpath(OUT), '; sheets per figure:', len(LEVELS) * 2)
    for name in light:
        print(name, sorted(set(light[name].values())))
