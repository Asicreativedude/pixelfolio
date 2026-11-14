# A desk and a small office room, drawn from nothing by code (#61 side test).
# Map rule from #60: drawn on a 16 px grid, exported at 2x, no outlines (like the Hall). ENDESGA 32 only.
# Writes desk.png / desk@2x.png, room.png / room@2x.png and scene.png (room at 2x with the test cast at 1:1).
# usage (repo root): python3 -I art-tests/claude-drawn/make_room.py
import os
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
E32 = set(open(os.path.join(HERE, '../pixellab/e32.hex')).read().split())
INK, SL4, SL3, SL2, SL1, SL0, WHT = '181425', '262b44', '3a4466', '5a6988', '8b9bb4', 'c0cbdc', 'ffffff'
W1, W2, W3, W4, W5, W6 = 'ead4aa', 'e4a672', 'd77643', 'b86f50', '733e39', '3e2731'
RED, DRED, GOLD, YEL, ORG, PINK = 'e43b44', 'a22633', 'feae34', 'fee761', 'f77622', 'b55088'
G1, G2, G3, BLU, CYA, NAVY = '63c74d', '3e8948', '265c42', '0099db', '2ce8f5', '124e89'


class Canvas:
    def __init__(self, w, h, fill=None):
        self.im = Image.new('RGBA', (w, h), self.rgb(fill) if fill else (0, 0, 0, 0))

    @staticmethod
    def rgb(c):
        return tuple(bytes.fromhex(c)) + (255,)

    def r(self, x, y, w, h, c):  # filled rectangle
        self.im.paste(self.rgb(c), (x, y, x + w, y + h))

    def grid(self, x, y, rows, legend):  # small hand-drawn stamp, '.' = clear
        for j, row in enumerate(rows):
            for i, ch in enumerate(row):
                if ch != '.':
                    self.im.putpixel((x + i, y + j), self.rgb(legend[ch]))

    def save(self, name, scale=1):
        used = {'%02x%02x%02x' % p[:3] for _, p in self.im.getcolors(9999) if p[3]}
        assert used <= E32, used - E32
        im = self.im.resize((self.im.width * scale, self.im.height * scale), Image.NEAREST)
        im.save(os.path.join(HERE, name))
        return im


def desk(c, x, y, shadow=True):
    """48 wide. y is the back edge of the desktop; the monitor rises 12 px above it."""
    if shadow:
        c.r(x + 1, y + 26, 47, 2, SL3)
    # legs, drawer unit and the dark panel behind the knee space
    c.r(x, y + 15, 3, 11, W4); c.r(x, y + 15, 1, 11, W5)
    c.r(x + 3, y + 15, 27, 5, W5); c.r(x + 3, y + 20, 27, 1, W6)
    c.r(x + 30, y + 15, 18, 10, W4); c.r(x + 47, y + 15, 1, 10, W5)
    c.r(x + 31, y + 25, 2, 1, W5); c.r(x + 45, y + 25, 2, 1, W5)
    for dy in (16, 21):  # two drawers
        c.r(x + 32, y + dy, 14, 4, W3); c.r(x + 32, y + dy + 3, 14, 1, W5); c.r(x + 37, y + dy + 1, 4, 1, GOLD)
    # desktop: lit back edge, surface, front edge
    c.r(x, y, 48, 13, W2); c.r(x, y, 48, 1, W1); c.r(x, y + 13, 48, 2, W3)
    # monitor
    c.r(x + 20, y + 4, 8, 2, SL3); c.r(x + 23, y, 2, 4, SL3)
    c.r(x + 13, y - 12, 22, 13, SL4); c.r(x + 14, y - 11, 20, 11, BLU)
    c.r(x + 16, y - 9, 8, 1, WHT); c.r(x + 16, y - 7, 12, 1, CYA); c.r(x + 16, y - 5, 6, 1, CYA)
    c.r(x + 16, y - 3, 10, 1, WHT); c.r(x + 30, y - 9, 2, 2, YEL)
    # keyboard, mouse, mug, lamp
    c.r(x + 15, y + 8, 16, 4, SL0); c.r(x + 15, y + 11, 16, 1, SL1)
    for i in range(7):
        c.r(x + 16 + 2 * i, y + 9, 1, 1, SL1)
    c.r(x + 33, y + 8, 2, 3, WHT); c.r(x + 33, y + 10, 2, 1, SL0)
    c.r(x + 5, y + 4, 4, 5, WHT); c.r(x + 5, y + 6, 4, 1, RED); c.r(x + 6, y + 4, 2, 1, W5); c.r(x + 9, y + 5, 1, 2, SL0)
    c.r(x + 39, y + 9, 6, 2, SL4); c.r(x + 41, y + 2, 2, 7, SL3)
    c.r(x + 37, y - 3, 10, 5, GOLD); c.r(x + 38, y - 3, 8, 1, YEL); c.r(x + 37, y + 1, 10, 1, ORG)


def room():
    c = Canvas(176, 120, SL1)                      # walls seen from above
    c.r(8, 32, 160, 80, SL2)                       # floor, 10 x 5 tiles
    for ty in range(32, 113, 16):                  # tile corners, a light hint of the grid
        for tx in range(8, 169, 16):
            c.r(max(tx - 2, 8), ty, min(tx + 3, 168) - max(tx - 2, 8), 1, SL3) if 32 < ty < 112 else None
            c.r(tx, max(ty - 2, 32), 1, min(ty + 3, 112) - max(ty - 2, 32), SL3) if 8 < tx < 168 else None
    c.r(8, 4, 160, 24, SL0); c.r(8, 28, 160, 4, SL1); c.r(8, 27, 160, 1, WHT)   # north wall face, skirting
    c.r(0, 0, 176, 4, SL1); c.r(0, 0, 176, 1, SL3)
    c.r(8, 32, 160, 2, SL3)                        # shade where the wall meets the floor
    c.r(7, 4, 1, 108, SL3); c.r(168, 4, 1, 108, SL3); c.r(8, 112, 160, 1, SL3)
    c.r(80, 112, 16, 8, SL2); c.r(80, 112, 16, 1, SL3)                           # doorway
    c.r(81, 104, 14, 6, G2); c.r(82, 105, 12, 4, G3); c.r(84, 106, 8, 2, G2)     # doormat
    # window
    c.r(26, 7, 34, 19, WHT); c.r(28, 9, 30, 15, BLU); c.r(42, 9, 2, 15, WHT); c.r(28, 16, 30, 1, WHT)
    for i in range(5):
        c.r(31 + i, 14 - i, 1, 1, CYA); c.r(34 + i, 14 - i, 1, 1, CYA); c.r(47 + i, 22 - i, 1, 1, CYA)
    c.r(24, 26, 38, 2, SL1)
    # pin board
    c.r(72, 6, 22, 12, W5); c.r(73, 7, 20, 10, W3)
    c.r(75, 9, 4, 4, WHT); c.r(81, 8, 3, 4, YEL); c.r(86, 10, 5, 3, WHT); c.r(80, 13, 4, 3, PINK); c.r(76, 9, 1, 1, RED)
    # bookshelf
    c.r(133, 42, 31, 2, SL3)
    c.r(132, 6, 32, 4, W2); c.r(132, 6, 32, 1, W1); c.r(132, 10, 32, 32, W5)
    books = [RED, BLU, GOLD, G2, WHT, PINK, ORG, NAVY, G1, DRED]
    for s, y in enumerate((12, 22, 32)):
        c.r(134, y, 28, 8, W6)
        x, i = 134, s * 3
        while x < 160 - s * 5:
            w, h = 2 + (i * 7) % 3 % 2 + (i % 4 == 0), 5 + (i * 5) % 3
            c.r(x, y + 8 - h, w, h, books[i % len(books)]); c.r(x, y + 8 - h, w, 1, WHT if i % 3 == 0 else books[i % len(books)])
            x += w + (i % 5 == 2); i += 1
    # plant in the corner
    c.r(12, 54, 10, 1, SL3)
    c.r(12, 45, 10, 9, ORG); c.r(11, 44, 12, 2, W3); c.r(12, 48, 10, 1, DRED); c.r(12, 51, 10, 1, DRED)
    c.grid(9, 31, ['.....G..g.....', '..g..GG.gG.g..', '..GgGGGgGG.gG.', '.gGGGgGGGgGGG.', '.GdGGGGgGGGGd.',
                   '..GGdGGGGdGG..', '...dGGdGGGd...', '....dGGGGd....', '.....dGGd.....', '......dd......'],
           {'G': G2, 'g': G1, 'd': G3})
    desk(c, 68, 34)
    # office chair, seen from behind
    c.r(79, 82, 12, 1, SL3)
    c.r(84, 76, 2, 4, SL4); c.r(80, 79, 10, 2, SL4); c.r(79, 80, 2, 2, INK); c.r(89, 80, 2, 2, INK)
    c.r(79, 60, 12, 6, GOLD)
    c.r(78, 64, 14, 12, W3); c.r(79, 63, 12, 1, W3); c.r(79, 64, 12, 1, GOLD); c.r(78, 74, 14, 2, W4)
    for x in (81, 84, 87):
        c.r(x, 66, 1, 7, W4)
    # rug
    c.r(24, 82, 2, 20, W1); c.r(150, 82, 2, 20, W1)
    for y in range(83, 102, 2):
        c.r(24, y, 2, 1, SL2); c.r(150, y, 2, 1, SL2)
    c.r(26, 82, 124, 20, DRED); c.r(28, 84, 120, 16, GOLD); c.r(29, 85, 118, 14, DRED); c.r(32, 87, 112, 10, RED)
    for x in range(40, 140, 16):
        c.grid(x, 88, ['...gg...', '..gddg..', '.gdggdg.', 'gdg..gdg', 'gdg..gdg', '.gdggdg.', '..gddg..', '...gg...'],
               {'g': GOLD, 'd': DRED})
    return c


d = Canvas(48, 40); desk(d, 0, 12, shadow=False)
d.save('desk.png'); d.save('desk@2x.png', 2)
r = room(); r.save('room.png'); scene = r.save('room@2x.png', 2).copy()

# scene.png: the test cast standing in the room at 1:1, as the game would draw them
cast = [('../../public/Hero/Sprite-Hero.png', 3, 0, 152, 100), ('dana.png', 0, 0, 236, 120),
        ('dog.png', 1, 0, 190, 128), ('visitor.png', 2, 0, 44, 96), ('dog.png', 0, 0, 96, 60)]
for src, row, col, x, y in cast:
    s = Image.open(os.path.join(HERE, src)).convert('RGBA')
    scene.alpha_composite(s.crop((col * 64, row * 64, col * 64 + 40, row * 64 + 64)), (x, y))
scene.resize((scene.width * 3, scene.height * 3), Image.NEAREST).save(os.path.join(HERE, 'scene.png'))
print('desk, room, scene written; all ENDESGA 32')
