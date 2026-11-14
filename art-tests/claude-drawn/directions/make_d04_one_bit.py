# Direction 4, "One-bit plus one accent" (reports/Pixel art style directions.md), as one still.
# Everything is redrawn; nothing comes from make_room.py but the layout of the office corner.
#   palette: off-black K, warm white P, one accent A. The accent is only on the hero and on things the player
#     can press: the screen, the pin board's notes, the door mat, the dog's collar.
#   line: the ground is black, so objects are black shapes with a white 2 px stroke, or solid white.
#     Characters are white fill with black line. No stroke or gap is thinner than 2 px.
#   no shading. One checker stands for one mid-tone, on the rug only (large, static), never on a sprite.
#   every object and character carries a 2 px black halo, so it cuts the lines behind it.
# usage (repo root): python3 -I art-tests/claude-drawn/directions/make_d04_one_bit.py
import os
from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
K, P, A = '16141c', 'f4ecd8', '1fd1bc'
W, H = 352, 240


def rgb(c):
    return tuple(bytes.fromhex(c)) + (255,)


class Layer:
    """One object. Every primitive strokes at 2 px."""
    def __init__(self):
        self.im = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        self.d = ImageDraw.Draw(self.im)

    def bar(self, x, y, w, h, c=P, r=0):  # solid shape
        self.d.rounded_rectangle((x, y, x + w - 1, y + h - 1), r, fill=rgb(c))

    def box(self, x, y, w, h, fill=K, line=P, r=0):  # stroked rectangle
        self.bar(x, y, w, h, line, r); self.bar(x + 2, y + 2, w - 4, h - 4, fill, max(r - 1, 0))

    def ring(self, x, y, w, h, fill=K, line=P):  # stroked ellipse
        self.d.ellipse((x, y, x + w - 1, y + h - 1), fill=rgb(line))
        self.d.ellipse((x + 2, y + 2, x + w - 3, y + h - 3), fill=rgb(fill))

    def poly(self, pts, fill=K, line=P):  # stroked polygon: the stroke is the shape minus itself shrunk by 2
        m = Image.new('L', (W, H)); ImageDraw.Draw(m).polygon(pts, fill=255)
        self.im.paste(rgb(line), mask=m); self.im.paste(rgb(fill), mask=m.filter(ImageFilter.MinFilter(5)))

    def art(self, rows, x, y, mirror=False):  # letter grid: W white, K black, A accent, . clear
        for j, row in enumerate(rows):
            row = row + row[::-1] if mirror and len(row) == 13 else row
            for i, ch in enumerate(row):
                if ch != '.':
                    self.im.putpixel((x + i, y + j), rgb({'W': P, 'K': K, 'A': A}[ch]))


scene = Image.new('RGBA', (W, H), rgb(K))
taken = Image.new('L', (W, H))  # where objects and their halos are; the floor dots stay clear of it


def put(fn, *a, halo=2):
    layer = Layer(); fn(layer, *a)
    if halo:
        mask = layer.im.getchannel('A').filter(ImageFilter.MaxFilter(2 * halo + 1))
        scene.paste(rgb(K), mask=mask); taken.paste(255, mask=mask)
    scene.alpha_composite(layer.im)


# --- room -----------------------------------------------------------------------------------------------------
def shell(c):
    c.box(14, 6, 324, 220)                                    # the room
    c.bar(16, 62, 320, 2)                                     # where the wall meets the floor
    c.bar(160, 222, 32, 6, K); c.bar(158, 224, 2, 16); c.bar(192, 224, 2, 16)     # doorway


def floor_dots(c):
    for ty in range(96, 224, 32):                             # floor tiles: one dot per corner, only whole ones
        for tx in range(48, 336, 32):
            if not taken.crop((tx - 2, ty - 2, tx + 4, ty + 4)).getbbox():
                c.bar(tx, ty, 2, 2)


def rug(c, x, y, w, h):
    for fy in range(y + 2, y + h - 2, 4):                     # fringe
        c.bar(x - 5, fy, 5, 2); c.bar(x + w, fy, 5, 2)
    c.box(x, y, w, h)
    for py in range(y + 4, y + h - 4):                        # the one mid-tone: a checker
        for px in range(x + 4, x + w - 4):
            if (px + py) % 2:
                c.im.putpixel((px, py), rgb(P))
    for cx in range(x + 34, x + w - 50, 52):                  # diamonds
        cy = y + h // 2
        for r, col in ((13, K), (11, P), (7, K), (3, P)):
            c.d.polygon([(cx - r, cy), (cx, cy - r), (cx + r, cy), (cx, cy + r)], fill=rgb(col))


def doormat(c, x, y):
    c.bar(x, y, 30, 12, A, 2); c.box(x + 3, y + 3, 24, 6, A, K)


def window(c, x, y):
    c.box(x, y, 68, 40, r=2); c.bar(x + 33, y, 2, 40)
    for bx, by, bw in ((4, 22, 8), (14, 16, 9), (25, 26, 6), (37, 24, 9), (48, 14, 8), (58, 22, 6)):   # skyline
        c.bar(x + bx, y + by, bw, 38 - by)
        for wy in range(by + 3, 34, 5):
            c.bar(x + bx + 2, y + wy, 2, 2, K)
            if bw > 8:
                c.bar(x + bx + 5, y + wy, 2, 2, K)
    c.ring(x + 20, y + 5, 9, 9, P); c.d.ellipse((x + 23, y + 4, x + 30, y + 11), fill=rgb(K))          # moon
    for sx, sy in ((7, 8), (12, 14), (42, 7), (56, 6), (44, 16)):                                      # stars
        c.bar(x + sx, y + sy, 2, 2)
    c.bar(x - 4, y + 40, 76, 4)                                                                         # sill


def board(c, x, y):
    c.box(x, y, 46, 28)
    c.bar(x + 5, y + 5, 10, 9, A); c.bar(x + 18, y + 4, 8, 8, A); c.bar(x + 30, y + 6, 11, 12, A)
    c.bar(x + 15, y + 15, 11, 8, A)
    c.bar(x + 5, y + 17, 7, 6); c.bar(x + 7, y + 19, 3, 2, K)                                          # a white card
    for px, py in ((9, 6), (21, 5), (35, 7), (20, 16)):                                                # pins
        c.bar(x + px, y + py, 2, 2, K)
    c.bar(x + 32, y + 11, 7, 2, K); c.bar(x + 32, y + 14, 5, 2, K)


def clock(c, x, y):
    c.ring(x, y, 22, 22)
    c.bar(x + 10, y + 5, 2, 7); c.bar(x + 10, y + 10, 6, 2)
    for tx, ty in ((10, 3), (10, 17), (3, 10), (17, 10)):
        c.bar(x + tx, y + ty, 2, 2)


def bookshelf(c, x, y):
    c.box(x, y, 66, 82); c.bar(x - 2, y, 70, 4)
    for s in range(3):
        top = y + 6 + 25 * s
        c.bar(x + 2, top + 21, 62, 2)
        bx, seed = x + 5, 11 + 5 * s
        while bx < x + (36, 44, 32)[s]:
            seed = (seed * 73 + 41) % 997
            w, h = 4 + 2 * (seed % 2), 12 + 2 * (seed % 4)
            if seed % 3:
                c.bar(bx, top + 21 - h, w, h); c.bar(bx, top + 25 - h, w, 2, K)      # a white book
            else:
                c.box(bx, top + 21 - h, 6, h); w = 6                                 # a black one
            bx += w + 2
    c.bar(x + 44, y + 25, 14, 2); c.bar(x + 49, y + 20, 4, 5)                        # trophy: foot, stem,
    c.ring(x + 41, y + 9, 20, 8); c.bar(x + 45, y + 8, 12, 12, P, 4); c.bar(x + 45, y + 8, 12, 4)   # ears, cup
    c.poly([(x + 49, y + 52), (x + 54, y + 33), (x + 60, y + 34), (x + 56, y + 52)], P)      # a book that leans
    for i in range(3):                                                                       # a flat stack
        c.bar(x + 38 + 2 * (i % 2), y + 72 - 5 * i, 20 - 2 * i, 3)


def plant(c, x, y):
    for tx, ty in ((-4, -8), (-2, -22), (12, -20), (26, -22), (28, -8)):             # stems
        c.d.line([(x + 12, y + 2), (x + tx, y + ty)], fill=rgb(P), width=2)
    for dx, dy, w, h, solid in ((-14, -14, 16, 10, 1), (22, -14, 16, 10, 1), (-13, -32, 16, 15, 0),
                                (21, -32, 16, 15, 0), (4, -44, 16, 26, 1)):
        c.d.ellipse((x + dx - 2, y + dy - 2, x + dx + w + 1, y + dy + h + 1), fill=rgb(K))
        if solid:
            c.d.ellipse((x + dx, y + dy, x + dx + w - 1, y + dy + h - 1), fill=rgb(P))
            c.bar(x + dx + w // 2 - 1, y + dy + h // 2 - 2, 2, h // 2 + 2, K) if h > w else \
                c.bar(x + dx + 4, y + dy + h // 2 - 1, w - 4 if dx > 0 else w - 8, 2, K)
        else:
            c.ring(x + dx, y + dy, w, h)
    c.poly([(x + 1, y + 4), (x + 22, y + 4), (x + 19, y + 22), (x + 4, y + 22)])
    c.bar(x - 1, y, 26, 5)


def bin_(c, x, y):
    c.ring(x, y - 6, 9, 9, P, K); c.ring(x + 6, y - 7, 9, 9, P, K)                   # paper balls
    c.poly([(x, y + 3), (x + 15, y + 3), (x + 13, y + 20), (x + 2, y + 20)])
    c.bar(x + 5, y + 6, 2, 12); c.bar(x + 9, y + 6, 2, 12); c.bar(x - 1, y + 1, 18, 3)


def desk(c, x, y):
    c.box(x, y + 26, 10, 28); c.box(x + 58, y + 26, 38, 26)                          # leg, drawer unit
    for dy in (30, 40):
        c.box(x + 62, y + dy, 30, 9); c.bar(x + 73, y + dy + 4, 8, 2)
    c.box(x, y, 96, 28); c.bar(x, y + 26, 96, 4)                                     # top, thick front edge


def monitor(c, x, y):
    c.bar(x + 13, y + 34, 18, 4, P, 1); c.bar(x + 20, y + 28, 4, 6)                  # foot, neck
    c.box(x, y, 44, 30, A, P, 3)
    for i, (ind, w) in enumerate(((0, 12), (4, 18), (4, 10), (8, 14), (4, 16), (0, 8))):
        c.bar(x + 6 + ind, y + 5 + 4 * i, w, 2, K)
    c.bar(x + 34, y + 5, 4, 2, K)


def desk_things(c, x, y):
    c.bar(x + 4, y + 5, 11, 15); c.bar(x + 6, y + 8, 7, 2, K); c.bar(x + 6, y + 12, 7, 2, K); c.bar(x + 6, y + 16, 4, 2, K)
    c.box(x + 30, y + 15, 36, 10, r=1)                                               # keyboard
    for kx in range(x + 33, x + 63, 4):
        c.bar(kx, y + 18, 2, 4)
    c.bar(x + 70, y + 16, 6, 8, P, 2)                                                # mouse
    c.ring(x + 23, y + 10, 8, 8); c.box(x + 17, y + 8, 10, 12, r=1)                  # mug: handle, body
    c.bar(x + 19, y + 2, 2, 2); c.bar(x + 21, y + 4, 2, 2); c.bar(x + 19, y + 6, 2, 2)                # steam


def lamp(c, x, y):
    c.bar(x, y + 26, 14, 3, P, 1); c.bar(x + 6, y + 10, 2, 16)
    c.d.polygon([(x - 3, y + 11), (x + 2, y), (x + 11, y), (x + 16, y + 11)], fill=rgb(P))


def chair(c, x, y):
    for wx in (0, 12, 24):                                                           # wheels
        c.ring(x + wx, y + 40, 6, 6, P)
    c.bar(x + 2, y + 38, 26, 2); c.bar(x + 13, y + 30, 4, 9)
    c.bar(x + 3, y, 24, 5, P, 1)                                                     # seat, seen over the back
    c.box(x, y + 6, 30, 26, r=4)
    for sx in (8, 14, 20):
        c.bar(x + sx, y + 12, 2, 14)


# --- cast: letter grids, the left half of each figure, mirrored ------------------------------------------------
LEGS = ['.......WWWWWK'] * 8 + ['.......KKKKKK', '.....WWWWWWWK', '.....WWWWWWWK', '.....WWWWWWWK']
HERO = ['.............WWWWWW.......', '...........WWWKKKKWW......', '.........WWWKKKKKKKWW.....',
        '........WWKKKKKKKKKKWW....', '.......WWKKKKKKKKKKKWW....', '......WWKKKKKKKKKKKKWW....',
        '....WWWWKKKKKKKKKKKKWWW...', '...WWKKKKKKKKKKKKKKKKKWW..', '..WWKKKKKKKKKKKKKKKKKKWW..',
        '..WWKKWWKKKKKKKKKKWWKKWW..', '..WWKKWWKKKKKKKKKKWWKKWW..', '..WWKKWWWKKKKKKKKWWWKKWW..',
        '..WWKKWWWWWWWWWWWWWWKKWW..', '..WWKKWWWWWWWWWWWWWWKKWW..',
        '..WWKKKKKKKKW', 'WWWWKKKKKKKKK', 'WWWWKKWWWWKKK', 'WWWWKKWKKWKKW', 'WWWWKKWKKWKKW',
        '..WWKKWWWWKKW', '..WWKKKKKKKKW', '..WWKKKKKKKKW', '..WWWWWWWWWWW', '..WWWWWWWWWWW', '..WWKKKKKKKKK',
        '..WWKKKKKKKKK', '..WWKKKKKKWWW', '...WWKKKKKWWW', '...WWKKKKKKKK', '....WWKKKKKKK', '.....WWWKKKKK',
        '.......WWWWWW',
        '......AAAAAAA', '...AAAAAAAAAA', '..AAAAAAAAAAA', '.AAAAAAAAAAAA', '.AAAAKKAAAAAA', '.AAAAKKAAAAAA',
        '.WWWWKKAAAAAA', '.WWWWKKAAAAAA', '.WWWWKKAAAAAA', '.WWWWKKAAAAAA', '.WWWWKKAAAAAA', '.WWWW.KKKKKKK',
        '..WW..KKKKKKK'] + LEGS
DANA = ['........WWWWW', '......WWWWWWW', '....WWWWWWWWW', '...WWWWWWWWWW', '..WWWWWWWWWWW', '..WWWWWWWWWWW',
        '.WWWWWWWKKKKK', '.WWWWWKKKKWWW', '.WWWWKKKWWWWW', '.WWWWKKWWWWWW', '.WWWWKKWWWWWW', '.WWWWKKWWKKWW',
        '.WWWWKKWWKKWW', '.WWWWKKWWWWWW', '.WWWWKKWWWWWW', '.WWWWKKWWWWKK', '.WWWWKKWWWWKK', '.WWWWKKKWWWWW',
        '.WWWWWKKKKWWW', '.WWWWWWWKKKKK', '.WWWWWW.KKWWW', '.WWWWWW.KKWWW', '.WWWWWKKWWWWW', '..WWWWKKWWWWW',
        '..WWW.KKWWWWW', '......KKWWWWW', '...WWWKKWWWWW', '...WWWKKWWWWW', '...WWWKKWWWWW', '...WWWKKKKKKK',
        '...WWWKKKKKKK', '...WWWKKWWWWW', '...WWW.KWWWWW', '.......WWWWWW', '......WWWWWWW', '.....WWWWWWWW',
        '.....WWWWWWWW', '....WWWWWWWWW', '....WWWWWWWWW', '...WWWWWWWWWW', '...WWWWWWWWWW', '.............',
        '.............', '.........WWWK', '.........WWWK', '.........WWWK', '.........WWWK', '.........KKKK',
        '.......WWWWWK', '.......WWWWWK']
VISITOR = ['.......W....W', '......WWW..WW', '.....WWWWWWWW', '....WWWWWWWWW', '...WWWWWWWWWW', '..WWWWWWWWWWW',
           '..WWWWWWWWWWW', '..WWWWWWWWWWW', '..WWWWWWWWWWWWWWWWKKKKWW..', '..WWWWWWWWWWWWKKKKKKWWWW..',
           '..WWWWWWWWKKKKKKWWWWWWWW..', '..WWWWKKKKKKWWWWWWWWWWWW..', '..WWKKKKWWWWWWWWWWWWWWWW..',
           '..WWWWWWWWWWW', 'WWWWWWWKKWWWW', 'WWWWWWWKKWWWW', 'WWWWWWWWWWWWW', '..WWWWWWWWWWW', '..WWWWWWWWWKK',
           '..WWWWWWWWWKK', '...WWWWWWWWWW', '....WWWWWWWWW', '......WWWWWWW', '.......KKKKKK', '.....WWWWWWWW',
           '...WWWWWWWWWW', '..WWKKKKKKKKK', '.WWKKKKKKKKKK', '.WWKKWWKKKKKK', '.WWKKWWKKKKKK', '.WWKKWWKKKKKK',
           '.WWKKWWKKKKKK', '.WWKKWWKKKKKK', '.WWKKWWKKKKKK', '.WWWWWWKKKKKK', '.WWWWWWWWWWWW', '..WWW.WWWWWWW',
           '..WWW..KKKKKK'] + LEGS
DOG = ['..........................WW....WW', '.........................WWWW..WWWW', '..WWW....................WWWW..WWWW',
       '.WWWWW..................WWWWWWWWWWWW', '.WW.WW..................WWWWWWWWWWWW', '.WW.....................WWWKKWWWWWWWWW',
       '.WWW..................AAAWWKKWWWWWWWKK', '..WWWWWWWWWWWWWWWWWWWWAAAWWWWWWWWWWWKK', '...WWWWWWWWWWWWWWWWWWWAAAWWWWWWWWWWW',
       '...WWWWWWWWWWWWWWWWWWWAAAWWWWWWWW', '...WWWWWWWWWWWWWWWWWWWAAAAA', '...WWWWWWWWWWWWWWWWWWWWWAAA',
       '...WWWWWWWWWWWWWWWWWWWWWW', '...WWWWWWWWWWWWWWWWWWWWWW'] + ['...WWWW.KWWWW....WWWW.KWWWW'] * 6


def figure(c, rows, x, feet, mirror=True):
    c.art(rows, x, feet - len(rows), mirror)


if __name__ == '__main__':
    put(shell, halo=0); put(rug, 52, 164, 248, 40); put(doormat, 161, 209)
    put(window, 52, 14); put(board, 142, 12); put(clock, 208, 16); put(bookshelf, 264, 10)
    put(plant, 24, 88); put(bin_, 242, 74)
    put(desk, 136, 68); put(monitor, 162, 40); put(desk_things, 136, 68); put(lamp, 214, 60)
    put(chair, 155, 116)
    put(figure, VISITOR, 54, 162); put(figure, DOG, 98, 158, False)
    put(figure, HERO, 234, 160); put(figure, DANA, 270, 180)
    put(floor_dots, halo=0)
    used = {'%02x%02x%02x' % p[:3] for _, p in scene.getcolors()}
    assert used == {K, P, A}, used                              # the one check: two colours and the accent
    scene.resize((W * 3, H * 3), Image.NEAREST).save(os.path.join(HERE, 'd04-one-bit.png'))
    print('d04-one-bit.png written,', len(used), 'colours')
