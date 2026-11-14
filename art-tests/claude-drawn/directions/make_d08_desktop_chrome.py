# Direction 8, desktop chrome: the office seen through the windows of an invented operating system.
# (rule sheet: reports/Pixel art style directions.md, "### 8. Desktop chrome")
#   chrome   drawn here from nothing: windows, title bars, menu and status rows, buttons, icons, a taskbar, a cursor
#            and a 5 x 7 bitmap font. 1 px bevels, light on the top and left, dark on the bottom and right.
#            One title-bar colour (the hero's teal). 16 to 20 system colours, checked below.
#   world    the room is make_room.py's props in a tighter layout, reduced to 16 flat colours; cast shadows are a
#            1 px stipple instead of a darker tone, as a 16-colour machine would do it. The sheet says the world
#            "can stay simple because the frame carries the identity", so the room is not redrawn.
# usage (repo root): python3 -I art-tests/claude-drawn/directions/make_d08_desktop_chrome.py
import os, sys
from PIL import Image, ImageChops, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
import make_room as m

W, H = 352, 240
# system colours
K, WH, P1, P2, P3 = '16141f', 'ffffff', 'ddd6c6', 'aaa392', '6f6a60'      # ink, white, three putty bevel greys
TL, TD, D1, D2 = '189a9c', '0f5e6a', '463a6e', '5b4d8a'                    # title bar and its dark, desktop
# world colours (icons borrow from them)
N1, N2, N3 = '2e3350', '5c6688', 'a6b1cc'
B1, B2, B3, SK = 'e9c592', 'c4884f', '7a4838', 'f0c29c'
GR, GD, RD, YL, OR, BL, CY = '58a85a', '2c6a4c', 'd84840', 'f6cb4c', 'e8852e', '2c84c6', '86d6e8'
WORLD = {K, WH, N1, N2, N3, B1, B2, B3, SK, GR, GD, RD, YL, OR, BL, CY}
# ENDESGA 32 (what make_room draws in) -> world. Highlights and grain fold into the base tone: flat on purpose.
ROOM = {'181425': K, '262b44': N1, '3a4466': N1, '5a6988': N2, '8b9bb4': N3, 'c0cbdc': N3, 'ffffff': WH,
        'ead4aa': B1, 'e4a672': B1, 'c28569': B1, 'd77643': B2, 'b86f50': B2, '733e39': B3, '3e2731': B3,
        'e43b44': RD, 'a22633': B3, 'f6757a': RD, 'b55088': RD, '68386c': B3, 'feae34': YL, 'fee761': YL,
        'f77622': OR, 'be4a2f': B3, '63c74d': GR, '3e8948': GR, '265c42': GD, '193c3e': GD, '0099db': BL,
        '2ce8f5': CY, '124e89': N1}
# the cast: skin keeps a shade, and the hero's shirt is the title-bar teal
CAST = {**ROOM, 'e8b796': SK, 'c28569': B2, '0099db': TL, '2ce8f5': TL, '124e89': TD, 'd77643': OR, 'ead4aa': WH}

FONT = {  # 5 x 7, drawn here
    'A': '.###./#...#/#...#/#####/#...#/#...#/#...#', 'B': '####./#...#/#...#/####./#...#/#...#/####.',
    'C': '.###./#...#/#..../#..../#..../#...#/.###.', 'D': '####./#...#/#...#/#...#/#...#/#...#/####.',
    'E': '#####/#..../#..../####./#..../#..../#####', 'F': '#####/#..../#..../####./#..../#..../#....',
    'G': '.###./#...#/#..../#.###/#...#/#...#/.###.', 'H': '#...#/#...#/#...#/#####/#...#/#...#/#...#',
    'I': '###/.#./.#./.#./.#./.#./###', 'J': '..###/...#./...#./...#./...#./#..#./.##..',
    'K': '#...#/#..#./#.#../##.../#.#../#..#./#...#', 'L': '#..../#..../#..../#..../#..../#..../#####',
    'M': '#...#/##.##/#.#.#/#.#.#/#...#/#...#/#...#', 'N': '#...#/##..#/#.#.#/#..##/#...#/#...#/#...#',
    'O': '.###./#...#/#...#/#...#/#...#/#...#/.###.', 'P': '####./#...#/#...#/####./#..../#..../#....',
    'Q': '.###./#...#/#...#/#...#/#.#.#/#..#./.##.#', 'R': '####./#...#/#...#/####./#.#../#..#./#...#',
    'S': '.####/#..../#..../.###./....#/....#/####.', 'T': '#####/..#../..#../..#../..#../..#../..#..',
    'U': '#...#/#...#/#...#/#...#/#...#/#...#/.###.', 'V': '#...#/#...#/#...#/#...#/#...#/.#.#./..#..',
    'W': '#...#/#...#/#...#/#.#.#/#.#.#/##.##/#...#', 'X': '#...#/#...#/.#.#./..#../.#.#./#...#/#...#',
    'Y': '#...#/#...#/.#.#./..#../..#../..#../..#..', 'Z': '#####/....#/...#./..#../.#.../#..../#####',
    '0': '.###./#...#/#..##/#.#.#/##..#/#...#/.###.', '1': '.#./##./.#./.#./.#./.#./###',
    '2': '.###./#...#/....#/...#./..#../.#.../#####', '4': '...#./..##./.#.#./#..#./#####/...#./...#.',
    '6': '.###./#..../#..../####./#...#/#...#/.###.', ':': './#/././#/./.', '!': '#/#/#/#/#/./#',
    '/': '..#/..#/.#./.#./.#./#../#..', ' ': '../../../../../../..'}


def rgb(c):
    return tuple(bytes.fromhex(c)) + (255,)


def text(im, x, y, s, c):
    for ch in s:
        rows = FONT[ch].split('/')
        for j, row in enumerate(rows):
            for i, bit in enumerate(row):
                if bit == '#':
                    im.putpixel((x + i, y + j), rgb(c))
        x += len(rows[0]) + 1
    return x


def width(s):
    return sum(len(FONT[ch].split('/')[0]) + 1 for ch in s) - 1


def r(im, x, y, w, h, c):
    im.paste(rgb(c), (x, y, x + w, y + h))


def raised(im, x, y, w, h, face=P1):  # ink line round it, light top and left, dark bottom and right
    r(im, x, y, w, h, K); r(im, x + 1, y + 1, w - 2, h - 2, face)
    r(im, x + 1, y + 1, w - 2, 1, WH); r(im, x + 1, y + 1, 1, h - 2, WH)
    r(im, x + 1, y + h - 2, w - 2, 1, P2); r(im, x + w - 2, y + 1, 1, h - 2, P2)


def sunken(im, x, y, w, h, face=P1):
    r(im, x, y, w, h, face); r(im, x, y, w, 1, P3); r(im, x, y, 1, h, P3)
    r(im, x, y + h - 1, w, 1, WH); r(im, x + w - 1, y, 1, h, WH)


def window(im, x, y, w, h, title, boxes=3):
    """A window: hard 2 px shadow, bevelled frame, striped teal title bar with a close box. Returns the client box."""
    r(im, x + 2, y + 2, w, h, K)
    raised(im, x, y, w, h)
    tx, ty, tw = x + 3, y + 3, w - 6
    r(im, tx, ty, tw, 11, TL)
    for sy in range(ty + 2, ty + 10, 2):                                 # pinstripes
        r(im, tx + 13, sy, tw - 15 - 11 * (boxes - 1), 1, TD)
    tl = width(title)
    px = tx + (tw - tl) // 2
    r(im, px - 4, ty, tl + 8, 11, TL); text(im, px, ty + 2, title, WH)
    raised(im, tx + 1, ty + 1, 9, 9); r(im, tx + 4, ty + 4, 3, 3, K)      # close box
    for i in range(boxes - 1):                                           # zoom and shade boxes
        bx = tx + tw - 10 - 11 * i
        raised(im, bx, ty + 1, 9, 9)
        if i == 0:
            r(im, bx + 2, ty + 3, 5, 5, K); r(im, bx + 3, ty + 5, 3, 2, P1)
        else:
            r(im, bx + 2, ty + 6, 5, 2, K)
    r(im, tx, ty + 11, tw, 1, K)
    return tx, ty + 12, tw, h - 18


def button(im, x, y, w, h, label, default=False):
    if default:
        r(im, x - 1, y - 1, w + 2, h + 2, K)
    raised(im, x, y, w, h)
    text(im, x + (w - width(label)) // 2, y + (h - 7) // 2, label, K)


# --- icons, 24 x 18 each, drawn here ----------------------------------------------------------------------------
def icon_disk(im, x, y):
    r(im, x + 1, y + 3, 22, 14, K); r(im, x + 2, y + 4, 20, 12, P1); r(im, x + 2, y + 4, 20, 1, WH)
    r(im, x + 2, y + 15, 20, 1, P2); r(im, x + 4, y + 7, 12, 2, K); r(im, x + 4, y + 11, 16, 1, P2)
    r(im, x + 18, y + 7, 2, 2, GR); r(im, x + 4, y + 12, 8, 3, BL); r(im, x + 5, y + 13, 5, 1, CY)


def icon_folder(im, x, y):
    r(im, x + 1, y + 2, 10, 4, K); r(im, x + 2, y + 3, 8, 3, OR)                       # tab
    r(im, x + 1, y + 5, 22, 13, K); r(im, x + 2, y + 6, 20, 11, YL); r(im, x + 2, y + 6, 20, 1, WH)
    r(im, x + 2, y + 15, 20, 2, OR); r(im, x + 20, y + 7, 2, 10, OR)


def icon_mail(im, x, y):
    r(im, x + 1, y + 3, 22, 15, K); r(im, x + 2, y + 4, 20, 13, WH); r(im, x + 2, y + 15, 20, 2, N3)
    for i in range(10):                                                                 # flap
        im.putpixel((x + 2 + i, y + 4 + i * 7 // 10), rgb(K)); im.putpixel((x + 21 - i, y + 4 + i * 7 // 10), rgb(K))
    r(im, x + 17, y + 12, 3, 3, RD)


def icon_trash(im, x, y):
    r(im, x + 5, y + 2, 14, 3, K); r(im, x + 6, y + 3, 12, 1, N3); r(im, x + 10, y, 4, 2, K)
    r(im, x + 6, y + 5, 12, 13, K); r(im, x + 7, y + 5, 10, 12, N3); r(im, x + 7, y + 5, 2, 12, WH)
    for sx in (10, 13):
        r(im, x + sx, y + 7, 1, 8, N2)
    r(im, x + 15, y + 5, 2, 12, N2)


def desktop_icon(im, x, y, draw, label, selected=False):
    draw(im, x, y)
    lw = width(label)
    lx = x + 12 - lw // 2
    if selected:
        r(im, lx - 2, y + 20, lw + 4, 9, TL)
    else:
        text(im, lx + 1, y + 22, label, K)
    text(im, lx, y + 21, label, WH)


def cursor(im, x, y):
    shape = ['#', '##', '#o#', '#oo#', '#ooo#', '#oooo#', '#ooooo#', '#oooooo#', '#ooooooo#', '#oooo####', '#oo#oo#',
             '#o# #oo#', '##  #oo#', '     #oo#', '     ###']
    for j, row in enumerate(shape):
        for i, ch in enumerate(row):
            if ch != ' ':
                im.putpixel((x + i, y + j), rgb(K if ch == '#' else WH))


# --- the world inside the window ----------------------------------------------------------------------------------
class Stipple(m.Canvas):
    """make_room's canvas, but a prop's cast shadow is ink on every other pixel instead of one tone darker."""
    def prop(self, fn, *a, cast=(2, 2)):
        layer = m.Canvas(*self.im.size)
        fn(layer, *a)
        alpha = layer.im.getchannel('A')
        solid = alpha
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            s = Image.new('L', alpha.size); s.paste(alpha, (dx, dy)); solid = ImageChops.lighter(solid, s)
        if cast:
            sh = Image.new('L', alpha.size); sh.paste(solid, cast)
            self.stipple(ImageChops.subtract(sh, solid))
        self.im.paste(m.rgb(m.INK), mask=ImageChops.subtract(solid, alpha))
        self.im.alpha_composite(layer.im)

    def stipple(self, mask):
        box = mask.getbbox()
        px, mk = self.im.load(), mask.load()
        for y in range(box[1], box[3]) if box else ():
            for x in range(box[0], box[2]):
                if mk[x, y] and (x + y) % 2 == 0:
                    px[x, y] = m.rgb(m.INK)


RW, RH = 264, 172
PEOPLE = [('visitor.png', 2, 0, 28, 76), ('hero-detailed.png', 0, 0, 158, 82), ('dog.png', 1, 0, 54, 104),
          ('dana.png', 0, 0, 198, 98)]


def remap(im, table):
    px = im.load()
    for y in range(im.height):
        for x in range(im.width):
            if px[x, y][3]:
                px[x, y] = rgb(table['%02x%02x%02x' % px[x, y][:3]])
    return im


def room():
    c = Stipple(RW, RH, m.SL2)
    for ty in range(64, RH, 16):                                          # floor: a dot where tiles meet
        for tx in range(8, RW, 16):
            c.r(tx, ty, 1, 1, m.SL3)
    c.r(0, 0, RW, 44, m.SL0); c.r(0, 43, RW, 1, m.WHT); c.r(0, 44, RW, 4, m.SL1); c.r(0, 48, RW, 1, m.INK)
    for x in range(0, RW, 2):                                             # the wall's shadow on the floor
        c.r(x, 49, 1, 1, m.INK); c.r(x + 1, 50, 1, 1, m.INK)
    m.rug(c, 26, 134, 214, 34)
    m.window(c, 10, 3); m.board(c, 86, 5); m.clock(c, 140, 9); m.bookshelf(c, 196, 3)
    m.plant(c, 14, 74); m.bin_(c, 178, 58); m.desk(c, 78, 54); m.chair(c, 98, 102)
    im = remap(c.im, ROOM)
    for src, row, col, x, y in PEOPLE:
        s = Image.open(os.path.join(HERE, '..', src)).convert('RGBA').crop((col * 64, row * 64, col * 64 + 40, row * 64 + 64))
        box = s.getbbox()
        for sy in range(y + box[3] - 3, y + box[3] + 2):                  # stippled drop shadow
            for sx in range(x + box[0] + 2, x + box[2] + 3):
                if (sx + sy) % 2 == 0 and 0 <= sx < RW and 0 <= sy < RH:
                    im.putpixel((sx, sy), rgb(K))
        im.alpha_composite(remap(s, CAST), (x, y))
    return im


def scene():
    im = Image.new('RGBA', (W, H), rgb(D1))
    for y in range(0, H, 4):                                              # desktop pattern
        for x in range(0, W, 4):
            im.putpixel((x, y), rgb(D2)); im.putpixel((x + 2, y + 2), rgb(D2))
    # desktop icons, right column
    desktop_icon(im, 304, 8, icon_disk, 'DISK'); desktop_icon(im, 304, 46, icon_folder, 'WORK', selected=True)
    desktop_icon(im, 304, 84, icon_mail, 'MAIL'); desktop_icon(im, 304, 122, icon_trash, 'TRASH')
    # the game window
    cx, cy, cw, ch = window(im, 4, 3, 272, 213, 'OFFICE')
    mx = cx + 4
    for word in ('GAME', 'MAP', 'HELP'):                                  # menu row
        mx = text(im, mx, cy + 1, word, K) + 7
    r(im, cx, cy + 9, cw, 1, P2)
    sunken(im, cx, cy + 10, cw, RH + 2)
    world = room()
    im.paste(world, (cx + 1, cy + 11))
    sy = cy + 10 + RH + 2 + 1                                             # status row
    sunken(im, cx, sy, 58, 10); text(im, cx + 4, sy + 2, 'ROOM 1/6', K)
    sunken(im, cx + 60, sy, 44, 10); sunken(im, cx + 106, sy, cw - 106, 10)
    for i, col in enumerate((RD, RD, RD, P2)):                            # three hearts and an empty one
        hx = cx + 65 + 9 * i
        r(im, hx, sy + 3, 2, 3, col); r(im, hx + 3, sy + 3, 2, 3, col); r(im, hx + 1, sy + 4, 3, 3, col)
        r(im, hx + 2, sy + 7, 1, 1, col)
    for i in range(3):                                                    # resize grip
        r(im, cx + cw - 3 - 3 * i, sy + 6 + 0 * i, 1, 1, P3)
    # a message window on top: a dialog is a window too
    dx, dy = 236, 158
    ax, ay, aw, ah = window(im, dx, dy, 108, 60, 'DOG', boxes=1)
    sunken(im, ax + 4, ay + 4, 37, 28, WH)
    dog = Image.open(os.path.join(HERE, '../dog.png')).convert('RGBA').crop((0, 64, 64, 128))
    im.alpha_composite(remap(dog.crop((1, 42, 30, 62)), CAST), (ax + 8, ay + 8))
    text(im, ax + 48, ay + 7, 'WOOF!', K)
    button(im, ax + 58, ay + 23, 34, 13, 'OK', default=True)
    cursor(im, ax + 82, ay + 31)
    # taskbar
    r(im, 0, 225, W, 1, K); r(im, 0, 226, W, 14, P1); r(im, 0, 226, W, 1, WH)
    raised(im, 2, 228, 40, 11)
    for i in range(4):                                                    # the system mark: a teal diamond
        r(im, 8 - i, 230 + i, 1 + 2 * i, 1, TL); r(im, 8 - i, 236 - i, 1 + 2 * i, 1, TD)
    text(im, 15, 230, 'MENU', K)
    sunken(im, 46, 228, 50, 11, WH); text(im, 50, 230, 'OFFICE', K)
    raised(im, 99, 228, 34, 11); text(im, 104, 230, 'DOG', K)
    sunken(im, 312, 228, 38, 11); text(im, 317, 230, '10:42', K)
    return im, world


if __name__ == '__main__':
    im, world = scene()
    used = lambda i: {'%02x%02x%02x' % p[:3] for _, p in i.getcolors(99999)}
    chrome = im.copy(); chrome.paste(rgb(K), (8, 30, 8 + RW, 30 + RH))    # the picture without the room
    assert 16 <= len(used(chrome)) <= 20, len(used(chrome))               # the system palette rule
    assert used(world) <= WORLD | {TL, TD}, used(world) - WORLD
    out = im.resize((W * 3, H * 3), Image.NEAREST)
    assert out.size == (1056, 720)
    out.save(os.path.join(HERE, 'd08-desktop-chrome.png'))
    print('d08-desktop-chrome.png', len(used(im)), 'colours:', len(used(chrome)), 'in the chrome,', len(used(world)), 'in the room')
