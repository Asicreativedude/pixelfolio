# A desk and a small office room, drawn from nothing by code (#61 side test).
# v2: props use the characters' visual language: 1:1 pixels, a 1 px dark outline around every object, a base
# colour with one shade and one highlight. (v1 followed the #60 map rule, 16 px grid at 2x with no outlines;
# Asi: "not the same visual language as the characters". scene-v1.png keeps that version.)
# The floor and wall shell are still the 16 px grid at 2x: the floor is an open question.
# Writes desk.png, room.png and scene.png (room with the test cast, zoomed 3x). ENDESGA 32 only.
# usage (repo root): python3 -I art-tests/claude-drawn/make_room.py
import os
from PIL import Image, ImageChops, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
E32 = set(open(os.path.join(HERE, '../pixellab/e32.hex')).read().split())
INK, SL4, SL3, SL2, SL1, SL0, WHT = '181425', '262b44', '3a4466', '5a6988', '8b9bb4', 'c0cbdc', 'ffffff'
W1, W2, W3, W4, W5, W6, GRAIN = 'ead4aa', 'e4a672', 'd77643', 'b86f50', '733e39', '3e2731', 'c28569'
RED, DRED, GOLD, YEL, ORG, RUST, PINK, PLUM = 'e43b44', 'a22633', 'feae34', 'fee761', 'f77622', 'be4a2f', 'b55088', '68386c'
G1, G2, G3, BLU, CYA, NAVY = '63c74d', '3e8948', '265c42', '0099db', '2ce8f5', '124e89'
SHADE = {RED: DRED, BLU: NAVY, GOLD: ORG, G1: G2, G2: G3, WHT: SL0, PINK: PLUM, ORG: RUST, CYA: BLU, SL1: SL3}
W, H = 352, 240


def rgb(c):
    return tuple(bytes.fromhex(c)) + (255,)


class Canvas:
    def __init__(self, w=W, h=H, fill=None):
        self.im = Image.new('RGBA', (w, h), rgb(fill) if fill else (0, 0, 0, 0))

    def r(self, x, y, w, h, c):  # filled rectangle
        self.im.paste(rgb(c), (x, y, x + w, y + h))

    def ell(self, x, y, w, h, c):  # filled ellipse, hard edge
        ImageDraw.Draw(self.im).ellipse((x, y, x + w - 1, y + h - 1), fill=rgb(c))

    def prop(self, fn, *a):
        """Draw one object on its own layer and give it the cast's 1 px dark outline."""
        layer = Canvas(*self.im.size)
        fn(layer, *a)
        alpha = layer.im.getchannel('A')
        grown = Image.new('L', alpha.size)
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            s = Image.new('L', alpha.size); s.paste(alpha, (dx, dy)); grown = ImageChops.lighter(grown, s)
        self.im.paste(rgb(INK), mask=ImageChops.subtract(grown, alpha))
        self.im.alpha_composite(layer.im)

    def save(self, name, scale=1, check=True):
        used = {'%02x%02x%02x' % p[:3] for _, p in self.im.getcolors(99999) if p[3]}
        assert not check or used <= E32, used - E32  # the one check: every pixel is ENDESGA 32
        self.im.resize((self.im.width * scale, self.im.height * scale), Image.NEAREST).save(os.path.join(HERE, name))


# --- desk: 96 wide; (x, y) is the back-left corner of the desktop --------------------------------------------
def desk_body(c, x, y):
    c.r(x, y + 30, 6, 22, W4); c.r(x, y + 30, 2, 22, W5)                  # left leg panel
    c.r(x + 6, y + 30, 54, 10, W5); c.r(x + 6, y + 38, 54, 2, W6)         # panel behind the knees
    c.r(x + 60, y + 30, 36, 20, W4); c.r(x + 93, y + 30, 3, 20, W5)       # drawer unit
    c.r(x + 62, y + 50, 5, 2, W5); c.r(x + 88, y + 50, 5, 2, W5)          # feet
    for dy in (32, 41):                                                   # drawers
        c.r(x + 63, y + dy, 28, 8, INK); c.r(x + 64, y + dy + 1, 26, 6, W3); c.r(x + 64, y + dy + 1, 26, 1, W2)
        c.r(x + 73, y + dy + 3, 8, 2, GOLD); c.r(x + 73, y + dy + 3, 8, 1, YEL)
    c.r(x, y, 96, 26, W2); c.r(x, y, 96, 2, W1)                           # desktop, lit back edge
    for gx, gy, gw in ((8, 6, 22), (54, 10, 30), (20, 20, 40), (72, 22, 18), (4, 14, 12)):
        c.r(x + gx, y + gy, gw, 1, GRAIN)
    c.r(x, y + 26, 96, 4, W3); c.r(x, y + 29, 96, 1, W4)                  # front edge of the top


def monitor(c, x, y):
    c.r(x + 39, y + 8, 18, 4, SL3); c.r(x + 39, y + 8, 18, 1, SL1); c.r(x + 45, y + 2, 6, 6, SL3)
    c.r(x + 26, y - 26, 44, 28, SL4); c.r(x + 28, y - 24, 40, 22, BLU); c.r(x + 28, y - 24, 40, 1, NAVY)
    c.r(x + 31, y - 21, 14, 2, WHT); c.r(x + 31, y - 17, 22, 2, CYA); c.r(x + 31, y - 13, 10, 2, CYA)
    c.r(x + 31, y - 9, 18, 2, WHT); c.r(x + 58, y - 21, 6, 6, YEL); c.r(x + 58, y - 16, 6, 1, GOLD)
    c.r(x + 46, y, 4, 1, SL1); c.r(x + 26, y - 26, 44, 1, SL3)


def keyboard(c, x, y):
    c.r(x + 30, y + 15, 34, 9, SL0); c.r(x + 30, y + 23, 34, 1, SL1)
    for row in range(3):
        for i in range(15):
            c.r(x + 32 + 2 * i, y + 16 + 2 * row, 1, 1, SL1)
    c.r(x + 40, y + 22, 12, 1, SL1)


def mouse(c, x, y):
    c.r(x + 68, y + 16, 5, 7, WHT); c.r(x + 68, y + 21, 5, 2, SL0); c.r(x + 70, y + 16, 1, 3, SL0)


def mug(c, x, y):
    c.r(x + 9, y + 8, 9, 11, WHT); c.r(x + 16, y + 8, 2, 11, SL0); c.r(x + 10, y + 8, 7, 2, W5)
    c.r(x + 9, y + 13, 9, 2, RED); c.r(x + 16, y + 13, 2, 2, DRED)
    c.r(x + 18, y + 11, 3, 1, WHT); c.r(x + 20, y + 11, 1, 6, WHT); c.r(x + 18, y + 16, 3, 1, WHT)


def lamp(c, x, y):
    c.r(x + 76, y + 17, 14, 4, SL4); c.r(x + 76, y + 17, 14, 1, SL3); c.r(x + 82, y + 2, 2, 15, SL3)
    for i in range(10):
        w = 12 + 2 * (i // 2)
        c.r(x + 83 - w // 2, y - 8 + i, w, 1, ORG if i == 9 else GOLD); c.r(x + 84 - w // 2, y - 8 + i, 3, 1, YEL)


def desk(c, x, y):
    for part in (desk_body, monitor, keyboard, mouse, mug, lamp):
        c.prop(part, x, y)


# --- other props ----------------------------------------------------------------------------------------------
def chair(c, x, y):  # office chair seen from behind, 28 wide
    def base(c):
        c.r(x + 12, y + 32, 4, 5, SL3); c.r(x + 3, y + 37, 22, 3, SL4); c.r(x + 3, y + 37, 22, 1, SL3)
        for wx in (1, 11, 22):
            c.r(x + wx, y + 39, 5, 4, SL4)
    def seat(c):
        c.r(x + 3, y, 22, 10, GOLD); c.r(x + 3, y, 22, 2, YEL)
    def back(c):
        c.r(x + 1, y + 8, 26, 24, W3); c.r(x, y + 10, 28, 20, W3)
        c.r(x + 2, y + 9, 24, 2, GOLD); c.r(x, y + 27, 28, 3, W4); c.r(x + 1, y + 30, 26, 2, W4)
        c.r(x + 25, y + 11, 3, 16, W4)
        for sx in (8, 14, 20):
            c.r(x + sx, y + 13, 1, 13, W4)
    for part in (base, seat, back):
        c.prop(part)


def window(c, x, y):
    def frame(c):
        c.r(x, y, 68, 38, WHT); c.r(x + 66, y, 2, 38, SL0); c.r(x, y + 36, 68, 2, SL0)
        for px in (x + 4, x + 36):
            c.r(px - 1, y + 3, 30, 32, INK); c.r(px, y + 4, 28, 30, BLU)
            c.r(px, y + 4, 28, 1, NAVY); c.r(px, y + 4, 1, 30, NAVY)
            for i in range(9):
                c.r(px + 5 + i, y + 17 - i, 1, 1, CYA); c.r(px + 9 + i, y + 17 - i, 1, 1, CYA)
            for i in range(5):
                c.r(px + 18 + i, y + 29 - i, 1, 1, CYA)
            c.r(px, y + 18, 28, 1, INK); c.r(px, y + 19, 28, 2, WHT); c.r(px, y + 21, 28, 1, INK)
    def sill(c):
        c.r(x - 4, y + 38, 76, 4, SL1); c.r(x - 4, y + 38, 76, 1, SL0)
    c.prop(frame); c.prop(sill)


def board(c, x, y):
    def cork(c):
        c.r(x, y, 44, 24, W5); c.r(x + 2, y + 2, 40, 20, W3); c.r(x, y, 44, 1, W4)
        for i in range(14):
            c.r(x + 3 + (i * 11) % 38, y + 3 + (i * 7) % 18, 1, 1, W4)
    def notes(c):
        c.r(x + 5, y + 5, 9, 8, WHT); c.r(x + 6, y + 8, 6, 1, SL1); c.r(x + 6, y + 10, 4, 1, SL1); c.r(x + 9, y + 5, 2, 2, RED)
    def photo(c):
        c.r(x + 28, y + 6, 11, 10, WHT); c.r(x + 29, y + 7, 9, 6, CYA); c.r(x + 29, y + 11, 9, 2, G2); c.r(x + 35, y + 8, 2, 2, YEL)
    def stickies(c):
        c.r(x + 17, y + 4, 7, 7, YEL); c.r(x + 17, y + 10, 7, 1, GOLD)
    def sticky2(c):
        c.r(x + 15, y + 14, 8, 6, PINK); c.r(x + 15, y + 19, 8, 1, PLUM)
    for part in (cork, notes, photo, stickies, sticky2):
        c.prop(part)


def bookshelf(c, x, y):  # 64 wide, 74 tall
    def body(c):
        c.r(x, y, 64, 8, W2); c.r(x, y, 64, 1, W1); c.r(x, y + 7, 64, 1, W3)
        c.r(x, y + 8, 64, 66, W5); c.r(x + 61, y + 8, 3, 66, W6); c.r(x, y + 8, 2, 66, W4)
        seed = 7
        for s in range(3):
            top = y + 11 + 21 * s
            c.r(x + 3, top, 58, 17, W6); c.r(x + 3, top + 17, 58, 3, W4); c.r(x + 3, top + 17, 58, 1, W3)
            bx = x + 4
            while bx < x + 54 - 9 * (s == 2):
                seed = (seed * 73 + 41) % 997
                w, h = 3 + seed % 4, 10 + seed % 6
                col = (RED, BLU, GOLD, G2, WHT, PINK, ORG, G1, SL1, CYA)[seed % 10]
                c.r(bx, top + 17 - h, w, h, col); c.r(bx + w - 1, top + 17 - h, 1, h, SHADE[col])
                c.r(bx, top + 17 - h + 3, w - 1, 1, WHT if col != WHT else SL1)
                c.r(bx + w, top + 17 - h, 1, h, INK); c.r(bx - 1, top + 17 - h, 1, h, INK); c.r(bx, top + 16 - h, w, 1, INK)
                bx += w + 1 + (seed % 7 == 0) * 3
            if s == 2:  # a stack lying flat
                for i, col in enumerate((BLU, RED, GOLD)):
                    c.r(x + 46, top + 13 - 4 * i, 13, 4, INK); c.r(x + 47, top + 14 - 4 * i, 11, 3, col)
                    c.r(x + 47, top + 16 - 4 * i, 11, 1, SHADE[col])
    c.prop(body)


def plant(c, x, y):  # (x, y) is the top-left of the pot, 24 wide
    def pot(c):
        c.r(x, y, 24, 4, W3); c.r(x, y, 24, 1, W2)
        for i in range(16):
            ins = 1 + i // 6
            c.r(x + ins, y + 4 + i, 24 - 2 * ins, 1, DRED if i in (4, 5, 10, 11) else ORG)
            c.r(x + 21 - ins, y + 4 + i, 3, 1, DRED if i in (4, 5, 10, 11) else RUST)
    def stems(c):
        c.r(x + 11, y - 10, 2, 10, G3); c.r(x + 6, y - 6, 2, 6, G3); c.r(x + 16, y - 7, 2, 7, G3)
    def leaf(c, lx, ly, w, h):
        c.ell(lx, ly, w, h, G2); c.ell(lx + 1, ly + 1, w * 2 // 3, h * 2 // 3, G1)
        c.ell(lx + 2, ly + 2, w * 2 // 3, h * 2 // 3, G2); c.r(lx + w // 4, ly + h // 2, w // 2, 1, G3)
    c.prop(stems)
    for dx, dy, w, h in ((-9, -24, 14, 10), (17, -25, 14, 10), (3, -34, 13, 11), (-12, -12, 14, 9),
                         (20, -13, 15, 9), (-3, -22, 13, 10), (10, -19, 13, 10), (4, -10, 14, 9)):
        c.prop(leaf, x + dx, y + dy, w, h)
    c.prop(pot)


def rug(c, x, y, w, h):
    def body(c):
        for fy in range(y + 1, y + h - 1, 2):                     # fringe
            c.r(x - 4, fy, 4, 1, W1); c.r(x + w, fy, 4, 1, W1)
        c.r(x, y, w, h, DRED); c.r(x + 3, y + 3, w - 6, h - 6, GOLD); c.r(x + 4, y + 4, w - 8, h - 8, DRED)
        c.r(x + 7, y + 7, w - 14, h - 14, GOLD); c.r(x + 8, y + 8, w - 16, h - 16, RED)
        for cx in range(x + 28, x + w - 20, 32):                  # diamonds
            for i in range(-9, 10):
                for j in range(-9, 10):
                    d = abs(i) + abs(j)
                    if d <= 9 and d not in (6, 7, 2, 3):
                        c.r(cx + i, y + h // 2 + j, 1, 1, GOLD if d in (8, 9, 0, 1) else YEL)
    c.prop(body)


def doormat(c, x, y):
    def body(c):
        c.r(x, y, 28, 12, G2); c.r(x + 2, y + 2, 24, 8, G3); c.r(x + 3, y + 3, 22, 6, G2)
        for i in range(5):
            c.r(x + 5 + 4 * i, y + 5, 2, 2, G1)
    c.prop(body)


def shell():
    """Walls and floor: still the 16 px grid at 2x. Only the edge lines are 1:1 dark lines."""
    c = Canvas(176, 120, SL1)
    c.r(8, 32, 160, 80, SL2)
    for ty in range(48, 112, 16):                                 # tile corners, a light hint of the grid
        for tx in range(24, 168, 16):
            c.r(tx - 2, ty, 5, 1, SL3); c.r(tx, ty - 2, 1, 5, SL3)
    c.r(8, 4, 160, 24, SL0); c.r(8, 28, 160, 4, SL1); c.r(8, 27, 160, 1, WHT)
    c.r(0, 0, 176, 1, SL3); c.r(8, 32, 160, 2, SL3)
    c.r(80, 112, 16, 8, SL2)                                      # doorway
    big = Canvas()
    big.im = c.im.resize((W, H), Image.NEAREST)
    big.r(16, 7, 320, 1, INK); big.r(16, 63, 320, 1, INK); big.r(15, 7, 1, 218, INK); big.r(336, 7, 1, 218, INK)
    big.r(15, 224, 145, 1, INK); big.r(192, 224, 145, 1, INK); big.r(159, 224, 1, 16, INK); big.r(192, 224, 1, 16, INK)
    return big


def room():
    c = shell()
    rug(c, 52, 164, 248, 40); doormat(c, 162, 208)
    window(c, 52, 14); board(c, 144, 12)
    c.r(266, 87, 62, 3, SL3); bookshelf(c, 264, 12)
    c.ell(18, 104, 32, 8, SL3); plant(c, 22, 86)
    c.r(137, 121, 96, 3, SL3); desk(c, 136, 68)
    c.ell(152, 158, 36, 8, SL3); chair(c, 156, 118)
    return c


d = Canvas(100, 84); desk(d, 2, 28); d.save('desk.png')
r = room(); r.save('room.png')
# scene.png: the test cast standing in the room, as the game would draw them
cast = [('../../public/Hero/Sprite-Hero.png', 3, 0, 222, 96), ('dana.png', 0, 0, 252, 122),
        ('dog.png', 1, 0, 206, 130), ('visitor.png', 2, 0, 60, 100), ('dog.png', 0, 0, 96, 62)]
for src, row, col, x, y in cast:
    s = Image.open(os.path.join(HERE, src)).convert('RGBA')
    r.im.alpha_composite(s.crop((col * 64, row * 64, col * 64 + 40, row * 64 + 64)), (x, y))
r.save('scene.png', 3, check=False)  # the hero's own sheet isn't ENDESGA 32 yet
print('desk, room, scene written; all ENDESGA 32')
