# Direction 6 (lived-in clutter) as rooms the game can load: ../game/
#   clutter-day.png, clutter-evening.png   the small room without its cast, 352x240, one screen pixel per art pixel
#   clutter.json   its walls, and for day and evening which sheet to use on each tile
#   studio-day.png, studio-evening.png   the studio (make_d06_studio.py) without a cast, 896x512
#   studio-upper-day.png, studio-upper-evening.png   what the game draws over the figures: the parts of the
#     furniture that stand in front of a figure on a free tile (make_d06_studio.tiles() has the rule)
#   studio.json   size, walls, light as in clutter.json, and spots: the tiles (col, row) where the cast starts
#   studio-check.png   the studio at 2x with the grid: free tiles green, blocked red, upper layer magenta
#   studio-preview-day.png, studio-preview-evening.png   the studio as the game draws it, cast on their spots
#   hero.png, dana.png, visitor.png, dog.png   the cast's full sheets in the rooms' colours. Each file stacks one
#     256x256 sheet per light (LEVELS x light from the left or the right); the game picks the sheet for the tile
#     the figure stands on, so the cast is lit by the room as in the still. The contact shadow is in the sheet.
# The game puts a figure at x = (col + 1) * 32, y = (row - 1) * 32 for the tile (col, row) under its feet, and
# draws its 64 px frame with the top left at (col * 32, row * 32 - 36).
# usage (repo root): python3 -I art-tests/claude-drawn/directions/make_d06_game.py
import json, os, sys
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))     # python3 -I leaves the script's folder out
import make_d06_lived_in_clutter as m
import make_d06_studio as studio

OUT = os.path.join(m.HERE, '..', 'game')
WALK = {3: (1, 2, 8), 4: (2, 3, 6, 7, 8), 5: (2, 3, 4, 5, 6, 7, 8), 6: (2, 3, 5)}       # small room, row: columns free to stand on
LEVELS = [-1, -.5, 0, .5, 1, 1.5]
SHADOW = bytes.fromhex(m.K)


def key(col, row):
    return '%d,%d' % ((col + 1) * 32, (row - 1) * 32)


def variants(room, name, free):
    """Which sheet a figure takes on each free tile of a room just built: light level index * 2 + from the right."""
    out = {}
    for col, row in sorted(free, key=lambda t: t[::-1]):
        here, from_right = m.standing(room.light, col * 32, row * 32 - 36)
        level = min(range(len(LEVELS)), key=lambda i: abs(LEVELS[i] - here))
        assert abs(LEVELS[level] - here) <= .5, (name, col, row, here)      # LEVELS covers every tile
        out[key(col, row)] = level * 2 + from_right
    return out


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


def preview(room, upper, light, cast):
    """The studio as the game draws it: room, the cast on their spots (facing down), the upper layer."""
    im = room.convert('RGBA')
    spots = {**studio.SPOTS, 'dog': studio.SPOTS['dog'][0]}
    for name, (col, row) in sorted(spots.items(), key=lambda s: s[1][1]):      # the ones further back first
        v = light[key(col, row)]
        im.alpha_composite(cast[name].crop((0, v * 256, 64, v * 256 + 64)), (col * 32, row * 32 - 36))
    im.alpha_composite(upper)
    return im.convert('RGB')


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    people = list(m.PEOPLE)
    m.PEOPLE.clear()                                            # the rooms alone: no figures, no shadows under them
    used, light = set(), {}
    for name, evening in (('day', False), ('evening', True)):  # the small room first: the studio resizes m's canvas
        room = m.build(evening)
        room.save(os.path.join(OUT, 'clutter-%s.png' % name))
        used |= {c for _, c in room.getcolors(99999)}
        light[name] = variants(room, name, [(col, row) for row, cols in WALK.items() for col in cols])
    walls = [key(c, r) for r in range(1, 8) for c in range(11) if c not in WALK.get(r, ())]
    json.dump({'walls': walls, 'light': light}, open(os.path.join(OUT, 'clutter.json'), 'w'), indent=1)

    rooms, uppers, slight = {}, {}, {}
    for name, evening in (('day', False), ('evening', True)):
        room = rooms[name] = studio.build(evening)
        free, mask = studio.tiles()
        room.save(os.path.join(OUT, 'studio-%s.png' % name))
        used |= {c for _, c in room.getcolors(99999)}
        uppers[name] = Image.new('RGBA', room.size)
        uppers[name].paste(room, mask=mask)
        uppers[name].save(os.path.join(OUT, 'studio-upper-%s.png' % name))
        slight[name] = variants(room, name, free)
    connected = studio.report(free)
    assert connected and len(free) >= .55 * (studio.COLS - 2) * (studio.ROWS - 3)
    walls = [key(c, r) for r in range(studio.ROWS) for c in range(studio.COLS) if (c, r) not in free]
    json.dump({'size': [studio.W, studio.H], 'walls': walls, 'light': slight, 'spots': studio.SPOTS},
              open(os.path.join(OUT, 'studio.json'), 'w'), indent=1)
    studio.check(rooms['day'], free, mask).save(os.path.join(OUT, 'studio-check.png'))
    assert len(used) <= 48, len(used)                           # both rooms, day and evening
    print('colours over both rooms, day and evening:', len(used))

    cast = {}
    for src, _, _, _, table in people:
        cast[src.split('.')[0].split('-')[0]] = sheet = sheets(src, table)
        sheet.save(os.path.join(OUT, src.replace('-detailed', '')))
    for name in rooms:
        preview(rooms[name], uppers[name], slight[name], cast).save(os.path.join(OUT, 'studio-preview-%s.png' % name))
    print('written to', os.path.normpath(OUT), '; sheets per figure:', len(LEVELS) * 2)
    for room, l in (('clutter', light), ('studio', slight)):
        for name in l:
            print(room, name, 'light variants', sorted(set(l[name].values())))
