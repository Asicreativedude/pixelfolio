# Builds a room (rooms/<name>.py) for the game, into public/rooms/:
#   <name>-day.png, <name>-evening.png   the room without its cast, one screen pixel per art pixel
#   <name>-upper-day.png, <name>-upper-evening.png   what the game draws over the figures: the parts of the
#     furniture that stand in front of a figure on a free tile (draw.tiles() has the rule)
#   <name>.json   size; walls, the blocked tiles; light, for day and evening the cast's sheet on each free tile
#     (light level index * 2 + 1 when the light comes from the right, draw.LEVELS); spots, the tiles
#     (col, row) where the cast starts
# and art/check/<name>.png, not committed: the room at 2x with the grid, free tiles green, blocked red, upper
# layer magenta.
# The game puts a figure at x = (col + 1) * 32, y = (row - 1) * 32 for the tile (col, row) under its feet, and
# draws its 64 px frame with the top left at (col * 32, row * 32 - 36). walls and light are keyed that way.
# usage (repo root): npm run room -- studio     or: python3 -I art/room.py [name ...]   (no name: every room)
# Needs Pillow and numpy at the versions in art/requirements.txt: other versions may move pixels.
import importlib, json, os, sys
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))     # python3 -I leaves the script's folder out
import draw

ART = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ART, '..', 'public', 'rooms')
LEVELS = draw.LEVELS


def key(col, row):
    return '%d,%d' % ((col + 1) * 32, (row - 1) * 32)


def variants(room, free):
    """Which sheet a figure takes on each free tile: light level index * 2 + from the right."""
    out = {}
    for col, row in sorted(free, key=lambda t: t[::-1]):
        here, from_right = draw.standing(room.light, col * 32, row * 32 - 36)
        level = min(range(len(LEVELS)), key=lambda i: abs(LEVELS[i] - here))
        assert abs(LEVELS[level] - here) <= .5, (col, row, here)        # LEVELS covers every tile
        out[key(col, row)] = level * 2 + from_right
    return out


def export(name):
    os.makedirs(OUT, exist_ok=True); os.makedirs(os.path.join(ART, 'check'), exist_ok=True)
    room_mod = importlib.import_module('rooms.' + name)
    used, rooms, light, frees = set(), {}, {}, []
    for when, evening in (('day', False), ('evening', True)):
        room = rooms[when] = room_mod.build(evening)
        free, mask = draw.tiles()
        frees.append(free)
        room.save(os.path.join(OUT, '%s-%s.png' % (name, when)))
        used |= {c for _, c in room.getcolors(99999)}
        upper = Image.new('RGBA', room.size)
        upper.paste(room, mask=mask)
        upper.save(os.path.join(OUT, '%s-upper-%s.png' % (name, when)))
        light[when] = variants(room, free)
    assert frees[0] == frees[1], 'day and evening block different tiles: walls is one list for both'
    cols, rows = draw.W // draw.TILE, draw.H // draw.TILE
    spots = [tuple(t) for at in room_mod.SPOTS.values() for t in (at if isinstance(at[0], list) else [at])]
    assert all(t in free for t in spots), [t for t in spots if t not in free]
    assert draw.reach(free, spots[0]) == free, 'some free tiles cannot be walked to'
    assert len(free) >= .55 * (cols - 2) * (rows - 3), len(free)
    assert len(used) <= 48, len(used)                           # day and evening together
    walls = [key(c, r) for r in range(rows) for c in range(cols) if (c, r) not in free]
    with open(os.path.join(OUT, name + '.json'), 'w') as f:
        json.dump({'size': [draw.W, draw.H], 'walls': walls, 'light': light, 'spots': room_mod.SPOTS}, f, indent=1)
    draw.check(rooms['day'], free, mask, room_mod.SPOTS).save(os.path.join(ART, 'check', name + '.png'))
    print('%s: %d of %d floor tiles free, %d colours; light variants day %s, evening %s' % (
        name, len(free), (cols - 2) * (rows - 3), len(used), sorted(set(light['day'].values())),
        sorted(set(light['evening'].values()))))


if __name__ == '__main__':
    for name in sys.argv[1:] or sorted(f[:-3] for f in os.listdir(os.path.join(ART, 'rooms')) if f.endswith('.py')):
        export(name)
