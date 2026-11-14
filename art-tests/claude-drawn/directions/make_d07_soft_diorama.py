# Direction 7, soft diorama: the office corner redrawn to that rule sheet (reports/Pixel art style directions.md).
#   palette   32 pastel colours in hue-shifted ramps, shadows lean cool (mauve, slate, teal), saturation capped
#   outline   no global ink: every outline pixel is the colour it wraps, two steps darker, one step on the lit edge
#   light     upper left; every prop darkens what is down-right of it one step, characters share one drop shadow
#   shapes    corners cut round, props at icon proportions (mug, keyboard, sticky notes, clock larger than true)
#   shell     walls and floor in a narrow mid-value band, drawn 1:1 (no 16 px grid)
# The cast is the existing sheets, recoloured per material by rule (thin ink lines take a dark tone of what they
# wrap; thick ink masses such as the quiff, beard and shoes become the darkest slate).
# usage (repo root): python3 -I art-tests/claude-drawn/directions/make_d07_soft_diorama.py
import colorsys, os
from PIL import Image, ImageChops, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 352, 240
A1 = 'fdf6e7'                                                      # cream white
S1, S2, S3 = 'd6e2cd', 'bfd0bd', '9db7a8'                          # sage wall
F1, F2, F3 = 'dccbbd', 'cbb5ab', 'b29c9f'                          # floor, shadows go mauve
W1, W2, W3, W4, W5 = 'f0cf9c', 'dfae7c', 'c08663', '94625a', '684658'   # honey wood down to plum
G1, G2, G3, G4 = 'cfe3a0', '98c88d', '64a388', '417479'            # leaf, darkest is shared with teal
T1, T2, T3 = 'cdeeea', '94d6d0', '5ab4b3'                          # sky and the hero's teal
L1, L2, L3, L4 = 'c3cadb', '98a2c0', '6c7699', '4a4f72'            # slate, L4 is the darkest colour there is
R1, R2, R3, R4 = 'f9cfc3', 'f0a39b', 'd5758a', 'a3567a'            # coral to berry
Y1, Y2, Y3 = 'fdeeb0', 'f7cf7f', 'e79f68'                          # butter to terracotta
K1, K2 = 'f8d7bd', 'e3ad95'                                        # skin
PAL = [A1, S1, S2, S3, F1, F2, F3, W1, W2, W3, W4, W5, G1, G2, G3, G4, T1, T2, T3, L1, L2, L3, L4,
       R1, R2, R3, R4, Y1, Y2, Y3, K1, K2]
DARK = {A1: F2, S1: S2, S2: S3, S3: G4, F1: F2, F2: F3, F3: L3, W1: W2, W2: W3, W3: W4, W4: W5, W5: W5,
        G1: G2, G2: G3, G3: G4, G4: L4, T1: T2, T2: T3, T3: G4, L1: L2, L2: L3, L3: L4, L4: L4,
        R1: R2, R2: R3, R3: R4, R4: W5, Y1: Y2, Y2: Y3, Y3: W3, K1: K2, K2: W4}
LIGHT = {R2: R1, R3: R2, T3: T2, T2: T1, Y2: Y1, Y3: Y2, G2: G1, G3: G2, L1: A1, L2: L1, A1: A1, W2: W1}


def rgb(c):
    return tuple(bytes.fromhex(c)) + (255,)


DARK_RGB = {rgb(k): rgb(v) for k, v in DARK.items()}


def darker(p, n=1):
    for _ in range(n):
        p = DARK_RGB.get(p, p)
    return p


class Canvas:
    def __init__(self, w=W, h=H, fill=None):
        self.im = Image.new('RGBA', (w, h), rgb(fill) if fill else (0, 0, 0, 0))

    def r(self, x, y, w, h, c):
        self.im.paste(rgb(c), (x, y, x + w, y + h))

    def rr(self, x, y, w, h, c, cut=1):  # rectangle with its corners cut round
        for i in range(cut):
            self.r(x + cut - i, y + i, w - 2 * (cut - i), 1, c)
            self.r(x + cut - i, y + h - 1 - i, w - 2 * (cut - i), 1, c)
        self.r(x, y + cut, w, h - 2 * cut, c)

    def ell(self, x, y, w, h, c):
        ImageDraw.Draw(self.im).ellipse((x, y, x + w - 1, y + h - 1), fill=rgb(c))

    def shade(self, mask):  # everything under the mask gets one step darker
        box = mask.getbbox()
        px, m = self.im.load(), mask.load()
        for y in range(box[1], box[3]) if box else ():
            for x in range(box[0], box[2]):
                if m[x, y]:
                    px[x, y] = darker(px[x, y])

    def ground(self, x, y, w, h):  # soft contact shadow on the floor
        m = Image.new('L', self.im.size)
        ImageDraw.Draw(m).ellipse((x, y, x + w - 1, y + h - 1), fill=255)
        self.shade(m)

    def prop(self, fn, *a, cast=(2, 2)):
        """One object on its own layer. Its outline is toned: each outline pixel takes the colour it touches, two
        steps darker, or one step where it sits on the lit (top or left) side. Then it shades what is down-right."""
        layer = Canvas(*self.im.size)
        fn(layer, *a)
        alpha = layer.im.getchannel('A')
        solid = alpha
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            s = Image.new('L', alpha.size); s.paste(alpha, (dx, dy)); solid = ImageChops.lighter(solid, s)
        if cast:
            sh = Image.new('L', alpha.size); sh.paste(solid, cast)
            self.shade(ImageChops.subtract(sh, solid))
        edge = ImageChops.subtract(solid, alpha)
        box = edge.getbbox()
        px, m, lay = self.im.load(), edge.load(), layer.im.load()
        w, h = self.im.size
        for y in range(box[1], box[3]) if box else ():
            for x in range(box[0], box[2]):
                if m[x, y]:
                    for (qx, qy), steps in (((x + 1, y), 1), ((x, y + 1), 1), ((x - 1, y), 2), ((x, y - 1), 2)):
                        if 0 <= qx < w and 0 <= qy < h and lay[qx, qy][3]:
                            px[x, y] = darker(lay[qx, qy], steps)
                            break
        self.im.alpha_composite(layer.im)


# --- shell ----------------------------------------------------------------------------------------------------
def shell():
    c = Canvas(fill=L1)
    def floor(c):
        c.r(18, 10, 316, 214, F1)
        for i, y in enumerate(range(80, 224, 16)):                      # long boards, 1:1, few joints
            c.r(18, y, 316, 1, F2)
            for x in range(60 + (i * 83) % 130, 334, 130):
                c.r(x, y - 15, 1, 15, F2)
        c.r(18, 64, 316, 3, F2); c.r(18, 64, 3, 160, F2)                # the walls shade the floor beside them
    def wall(c):
        c.r(18, 10, 316, 51, S1); c.r(18, 10, 316, 2, S2)
        for x in range(26, 334, 14):                                    # wallpaper: one quiet stripe
            c.r(x, 12, 1, 45, S2)
        c.r(18, 57, 316, 1, S3); c.r(18, 58, 316, 5, A1); c.r(18, 62, 316, 1, F2); c.r(18, 63, 316, 1, S3)
    def rim(c):                                                         # the top of the walls: the box's edge
        c.rr(13, 5, 326, 222, S2, 2)
        c.r(14, 6, 324, 1, S1); c.r(14, 6, 1, 220, S1)
        c.im.paste((0, 0, 0, 0), (18, 10, 334, 222)); c.im.paste((0, 0, 0, 0), (160, 222, 192, 228))
    c.prop(floor, cast=None); c.prop(wall, cast=None); c.prop(rim, cast=(3, 3))
    c.r(161, 222, 30, 18, F1); c.r(161, 222, 30, 2, F2); c.r(160, 227, 1, 13, S3); c.r(191, 227, 1, 13, S3)
    return c


def rug(c, x, y, w, h):
    def body(c):
        for fy in range(y + 2, y + h - 2, 3):                           # tassels
            c.r(x - 4, fy, 4, 2, A1); c.r(x + w, fy, 4, 2, A1)
        c.rr(x, y, w, h, R2, 2); c.r(x + 2, y + 2, 4, h - 4, R3); c.r(x + w - 6, y + 2, 4, h - 4, R3)
        c.r(x + 9, y + 4, w - 18, 2, R1); c.r(x + 9, y + h - 6, w - 18, 2, R1)
        c.r(x + 9, y + 4, 2, h - 8, R1); c.r(x + w - 11, y + 4, 2, h - 8, R1)
        n = 5
        for k in range(n):                                              # big diamonds
            cx, cy = x + w * (2 * k + 1) // (2 * n), y + h // 2
            for i in range(-10, 11):
                for j in range(-10, 11):
                    d = abs(i) + abs(j)
                    if d <= 10:
                        c.r(cx + i, cy + j, 1, 1, A1 if d >= 9 else R1 if d >= 5 else R3 if d >= 2 else Y1)
    c.prop(body, cast=None)


def doormat(c, x, y):
    def body(c):
        c.rr(x, y, 28, 11, G3); c.r(x + 2, y + 2, 24, 7, G2)
        for i in range(4):
            c.r(x + 5 + 5 * i, y + 4, 3, 3, A1)
    c.prop(body, cast=None)


# --- on the wall ----------------------------------------------------------------------------------------------
def window(c, x, y):
    def frame(c):
        c.rr(x, y, 72, 42, A1); c.r(x + 70, y + 1, 2, 40, F1); c.r(x + 1, y + 40, 70, 2, F1)
        for n, px in enumerate((x + 5, x + 38)):
            c.r(px - 1, y + 4, 31, 33, F3)                              # recess
            c.r(px, y + 5, 29, 31, T1); c.r(px, y + 22, 29, 14, T2)
            for bx, bw, bh, col in ((1, 7, 9, L1), (9, 6, 14, L2), (16, 8, 7, L1), (24, 5, 11, L2)):   # town
                bx = bx if n == 0 else 29 - bx - bw
                c.r(px + bx, y + 36 - bh, bw, bh, col); c.r(px + bx, y + 36 - bh, 1, bh, LIGHT[col])
                for wy in range(y + 38 - bh, y + 34, 4):
                    c.r(px + bx + 2, wy, 2, 2, Y1)
            c.r(px, y + 33, 29, 3, G2); c.r(px, y + 33, 29, 1, G1)      # treetops
            cx = px + (3 if n == 0 else 13)                             # one fat cloud
            c.rr(cx, y + 10, 13, 5, A1); c.rr(cx + 3, y + 8, 7, 3, A1)
            c.r(px, y + 5, 29, 1, T2); c.r(px, y + 5, 1, 31, T2)        # the frame shades the glass
            for i in range(5):                                          # glare
                c.r(px + 20 + i, y + 16 - i, 1, 1, A1); c.r(px + 23 + i, y + 16 - i, 1, 1, A1)
            c.r(px - 1, y + 19, 31, 1, F3); c.r(px - 1, y + 20, 31, 2, A1); c.r(px - 1, y + 22, 31, 1, F2)
    def sill(c):
        c.rr(x - 4, y + 42, 80, 5, A1); c.r(x - 3, y + 45, 78, 1, F1)
    def cactus(c):
        c.rr(x + 53, y + 20, 7, 16, G2); c.r(x + 54, y + 21, 1, 13, G1); c.r(x + 58, y + 22, 1, 14, G3)
        c.r(x + 60, y + 28, 3, 3, G2); c.rr(x + 62, y + 24, 3, 6, G2); c.r(x + 64, y + 25, 1, 4, G3)
        c.r(x + 55, y + 18, 3, 3, R2); c.r(x + 56, y + 18, 1, 1, R1)    # flower
    def pot(c):
        c.rr(x + 50, y + 35, 13, 3, Y3); c.r(x + 51, y + 35, 9, 1, Y2)
        c.r(x + 51, y + 38, 11, 5, Y3); c.r(x + 59, y + 38, 3, 5, W3); c.r(x + 52, y + 38, 2, 4, Y2)
    c.prop(frame, cast=(2, 3)); c.prop(sill, cast=(2, 3)); c.prop(cactus, cast=(1, 1)); c.prop(pot, cast=(1, 1))


def board(c, x, y):  # 52 x 32, the notes are far too big for a real board: that is the rule
    def cork(c):
        c.rr(x, y, 52, 32, W2); c.r(x + 49, y + 2, 2, 28, W3); c.r(x + 2, y + 29, 48, 2, W3)
        c.r(x + 3, y + 3, 46, 26, W1); c.r(x + 3, y + 3, 46, 1, W3); c.r(x + 3, y + 3, 1, 26, W3)
        for i in range(16):
            c.r(x + 5 + (i * 11) % 42, y + 5 + (i * 7) % 22, 1, 1, W2)
    def sticky(c, sx, sy, s, col, line):
        c.r(sx, sy, s, s, col); c.r(sx, sy + s - 1, s, 1, DARK[col]); c.r(sx + s - 3, sy + s - 3, 3, 3, DARK[col])
        c.r(sx + 2, sy + 3, s - 4, 1, line); c.r(sx + 2, sy + 5, s - 6, 1, line)
        c.r(sx + s // 2 - 1, sy - 1, 2, 2, R3)                          # pin
    def photo(c):
        c.r(x + 32, y + 6, 15, 13, A1); c.r(x + 34, y + 8, 11, 7, T1); c.r(x + 34, y + 12, 11, 3, G2)
        c.r(x + 36, y + 11, 4, 1, G2); c.r(x + 41, y + 9, 2, 2, Y2); c.r(x + 38, y + 5, 2, 2, T3)
    def ticket(c):
        c.r(x + 32, y + 22, 14, 5, G2); c.r(x + 32, y + 26, 14, 1, G3); c.r(x + 35, y + 22, 1, 5, G3)
        c.r(x + 37, y + 24, 7, 1, G1)
    c.prop(cork, cast=(2, 3))
    c.prop(sticky, x + 6, y + 6, 11, Y1, Y3, cast=(1, 1)); c.prop(sticky, x + 19, y + 5, 10, T2, G4, cast=(1, 1))
    c.prop(sticky, x + 14, y + 17, 10, R1, R3, cast=(1, 1)); c.prop(photo, cast=(1, 1)); c.prop(ticket, cast=(1, 1))


def clock(c, x, y):  # 25 px: a wall clock the size of a head
    def body(c):
        c.ell(x, y, 25, 25, R2); c.ell(x + 2, y + 2, 22, 22, R3); c.ell(x, y, 24, 24, R2)
        c.ell(x + 3, y + 3, 19, 19, A1)
        for tx, ty in ((12, 4), (12, 19), (4, 12), (19, 12)):
            c.r(x + tx, y + ty, 2, 2, L2)
        c.r(x + 12, y + 7, 2, 7, L4); c.r(x + 12, y + 12, 6, 2, L4); c.r(x + 12, y + 12, 2, 2, R3)
    c.prop(body, cast=(2, 3))


def bookshelf(c, x, y):  # 68 wide, 78 tall; books are fat so each one reads
    shelves = [[(6, 14, R2), (5, 12, T3), (7, 15, Y2), (5, 13, G2), (6, 11, L1), (5, 14, R3)],
               [(7, 13, T2), (5, 15, Y3), (6, 12, A1), (6, 14, G3), (5, 13, R2), (7, 11, L2), (5, 15, T3),
                (6, 13, Y2)],
               [(5, 14, G2), (7, 12, R3), (6, 15, L1), (5, 13, Y2), (6, 14, T3)]]
    def body(c):
        c.rr(x, y, 68, 9, W1); c.r(x + 1, y + 7, 66, 2, W2); c.r(x + 62, y + 1, 5, 6, W2)
        c.r(x + 1, y + 9, 66, 69, W2); c.r(x + 1, y + 9, 2, 69, W1); c.r(x + 64, y + 9, 3, 69, W3)
        for s, books in enumerate(shelves):
            top = y + 12 + 22 * s
            c.r(x + 4, top, 60, 18, W3); c.r(x + 4, top, 60, 2, W4); c.r(x + 4, top + 2, 1, 16, W4)
            c.r(x + 4, top + 18, 60, 3, W1); c.r(x + 4, top + 20, 60, 1, W2)
            bx = x + 6
            for w, h, col in books:
                by = top + 18 - h
                c.r(bx - 1, by - 1, w + 2, h + 1, DARK[DARK[col]])       # toned line round each book
                c.r(bx, by, w, h, col); c.r(bx + w - 1, by, 1, h, DARK[col]); c.r(bx, by, 1, h, LIGHT[col])
                c.r(bx + 1, by + 3, w - 2, 2, A1 if col != A1 else R2)
                c.r(bx + 1, by + h - 3, w - 2, 1, DARK[col])
                bx += w + 1
            if s == 2:                                                  # a stack lying flat
                for i, col in enumerate((T2, R2, Y2)):
                    sy = top + 13 - 5 * i
                    c.r(x + 39, sy - 1, 22 - 2 * i, 6, DARK[DARK[col]]); c.r(x + 40, sy, 20 - 2 * i, 5, col)
                    c.r(x + 40, sy, 20 - 2 * i, 1, LIGHT[col]); c.r(x + 40, sy + 4, 20 - 2 * i, 1, DARK[col])
                    c.r(x + 54 - 2 * i, sy + 1, 3, 3, A1)
    def trophy(c):
        tx, ty = x + 46, y + 13
        c.rr(tx + 2, ty, 11, 8, Y2); c.r(tx + 3, ty + 1, 3, 5, Y1); c.r(tx + 10, ty + 1, 2, 6, Y3)
        c.r(tx, ty + 1, 2, 4, Y2); c.r(tx + 13, ty + 1, 2, 4, Y3)                                   # handles
        c.r(tx + 6, ty + 8, 3, 4, Y3); c.rr(tx + 2, ty + 12, 11, 5, W3); c.r(tx + 3, ty + 12, 9, 1, W2)
    c.prop(body, cast=(3, 3)); c.prop(trophy, cast=(1, 1))


# --- on the floor ---------------------------------------------------------------------------------------------
def plant(c, x, y):  # (x, y) is the top-left of the pot, 26 wide; six big leaves, not a bush of small ones
    def pot(c):
        c.rr(x, y, 26, 5, Y3); c.r(x + 2, y + 1, 16, 1, Y2); c.r(x + 21, y + 1, 4, 3, W3)
        for i in range(16):
            ins = 2 + i // 5
            c.r(x + ins, y + 5 + i, 26 - 2 * ins, 1, Y3)
            c.r(x + 21 - ins, y + 5 + i, 5, 1, W3); c.r(x + ins + 2, y + 5 + i, 3, 1, Y2)
        c.r(x + 4, y + 11, 18, 2, A1); c.r(x + 17, y + 11, 5, 2, F1)                                # painted band
        c.rr(x + 2, y + 21, 22, 3, W2); c.r(x + 3, y + 21, 18, 1, W1)                               # saucer
    def stems(c):
        c.r(x + 12, y - 12, 2, 12, G3); c.r(x + 6, y - 6, 2, 6, G3); c.r(x + 18, y - 7, 2, 7, G3)
    def leaf(c, lx, ly, w, h):
        c.ell(lx, ly, w, h, G3); c.ell(lx, ly, w - 2, h - 2, G2); c.ell(lx + 2, ly + 1, w // 2, h // 2, G1)
        c.r(lx + 4, ly + h // 2, w - 7, 1, G3)
    c.ground(x - 4, y + 16, 40, 12)
    c.prop(stems, cast=None)
    for dx, dy, w, h in ((-12, -24, 18, 13), (18, -26, 18, 13), (2, -38, 18, 14), (-14, -9, 17, 11),
                         (22, -11, 17, 11), (4, -21, 18, 13)):
        c.prop(leaf, x + dx, y + dy, w, h, cast=(2, 3))
    c.prop(pot, cast=(2, 2))


def bin_(c, x, y):
    def body(c):
        for i in range(16):
            ins = i // 6
            c.r(x + ins, y + 4 + i, 16 - 2 * ins, 1, L1); c.r(x + 12 - ins, y + 4 + i, 4, 1, L2)
            c.r(x + ins + 1, y + 4 + i, 2, 1, A1)
        for sx in (5, 8, 11):
            c.r(x + sx, y + 7, 1, 11, L2)
        c.rr(x - 1, y + 2, 18, 3, L1); c.r(x, y + 2, 14, 1, A1)
    def ball(c, px, py):
        c.rr(px, py, 6, 5, A1); c.r(px + 3, py + 2, 2, 2, F1); c.r(px + 1, py + 3, 1, 1, F2)
    c.ground(x - 2, y + 14, 24, 9)
    c.prop(ball, x + 2, y - 2, cast=None); c.prop(ball, x + 8, y - 3, cast=None); c.prop(body, cast=(2, 2))
    c.prop(ball, x + 21, y + 15, cast=(1, 1))                           # one that missed


def chair(c, x, y):  # 30 wide, seen from behind
    def base(c):
        c.r(x + 13, y + 32, 4, 6, L2); c.r(x + 13, y + 32, 1, 6, L1)
        c.rr(x + 3, y + 37, 24, 4, L2); c.r(x + 4, y + 37, 22, 1, L1)
        for wx in (1, 12, 24):
            c.rr(x + wx, y + 40, 5, 4, L3)
    def seat(c):
        c.rr(x + 3, y, 24, 11, Y2, 2); c.r(x + 5, y + 1, 18, 2, Y1)
    def back(c):
        c.rr(x, y + 8, 30, 25, Y2, 3); c.r(x + 26, y + 12, 3, 18, Y3); c.r(x + 3, y + 30, 24, 2, Y3)
        c.rr(x + 3, y + 10, 22, 3, Y1); c.r(x + 1, y + 13, 2, 14, Y1)
        for sx in (10, 19):                                             # two soft seams
            c.r(x + sx, y + 15, 1, 13, Y3)
    c.ground(x - 1, y + 36, 34, 10)
    for part in (base, seat, back):
        c.prop(part, cast=(2, 2))


def desk(c, x, y):  # 112 wide; (x, y) is the back-left corner of the top
    def body(c):
        c.r(x + 1, y + 30, 8, 24, W2); c.r(x + 1, y + 30, 2, 24, W1); c.r(x + 7, y + 30, 2, 24, W3)   # left leg
        c.r(x + 9, y + 30, 58, 11, W3); c.r(x + 9, y + 30, 58, 3, W4)                                 # knee panel
        c.r(x + 67, y + 30, 44, 23, W2); c.r(x + 67, y + 30, 44, 2, W3); c.r(x + 108, y + 30, 3, 23, W3)
        c.r(x + 69, y + 53, 6, 2, W3); c.r(x + 103, y + 53, 6, 2, W3)                                 # feet
        for dy in (33, 43):                                                                           # drawers
            c.rr(x + 70, y + dy, 36, 9, W3); c.r(x + 71, y + dy + 1, 34, 7, W1); c.r(x + 71, y + dy + 7, 34, 1, W2)
            c.rr(x + 83, y + dy + 3, 10, 3, Y2); c.r(x + 84, y + dy + 3, 8, 1, Y1)
        c.rr(x, y, 112, 30, W1, 2); c.r(x + 108, y + 3, 3, 23, W2)                                    # top
        c.ell(x + 76, y + 6, 34, 18, Y1)                                                              # lamp light
        for gx, gy, gw in ((10, 7, 20), (44, 4, 16), (24, 22, 30), (62, 23, 14)):
            c.r(x + gx, y + gy, gw, 1, W2)
        c.r(x, y + 26, 112, 3, W2); c.r(x + 1, y + 29, 110, 1, W3); c.r(x + 1, y + 26, 110, 1, W1)    # front edge
    def monitor(c):
        c.rr(x + 44, y + 9, 24, 5, L2); c.r(x + 46, y + 9, 20, 1, L1)                                 # foot
        c.r(x + 53, y + 3, 6, 6, L2); c.r(x + 57, y + 3, 2, 6, L3)                                    # neck
        c.rr(x + 30, y - 30, 52, 34, L1, 2); c.r(x + 32, y - 29, 48, 1, A1); c.r(x + 79, y - 27, 2, 29, L2)
        c.r(x + 32, y + 1, 48, 2, L2); c.r(x + 75, y, 2, 1, G1)
        sx, sy = x + 34, y - 26                                         # screen 44 x 25: code as fat blocks
        c.rr(sx - 1, sy - 1, 46, 27, L3); c.r(sx, sy, 44, 25, L4); c.r(sx, sy, 44, 4, L3)
        for i, col in enumerate((R2, Y2, G2)):
            c.r(sx + 2 + 4 * i, sy + 1, 2, 2, col)
        for i, (ind, parts) in enumerate(((0, ((8, R2), (12, T2))), (4, ((14, A1), (6, Y1))), (4, ((6, R2), (16, G1))),
                                          (8, ((12, T2),)), (4, ((9, Y1), (9, A1))), (0, ((5, R2),)))):
            lx = sx + 3 + ind
            for w, col in parts:
                c.r(lx, sy + 6 + 3 * i, w, 2, col); lx += w + 2
        for i in range(6):
            c.r(sx + 36 + i, sy + 12 - i, 1, 1, L3); c.r(sx + 38 + i, sy + 15 - i, 1, 1, L3)
    def note(c):                                                        # a sticky note hanging off the bezel
        c.r(x + 24, y - 8, 9, 9, Y1); c.r(x + 24, y, 9, 1, Y2); c.r(x + 26, y - 5, 5, 1, Y3); c.r(x + 26, y - 3, 3, 1, Y3)
    def keyboard(c):
        c.rr(x + 33, y + 15, 46, 11, L1); c.r(x + 34, y + 25, 44, 1, L2)
        for row in range(2):
            for i in range(14):
                c.r(x + 35 + 3 * i, y + 16 + 3 * row, 2, 2, R2 if (row, i) == (1, 13) else A1)
        c.r(x + 35, y + 22, 5, 2, A1); c.r(x + 41, y + 22, 23, 2, A1); c.r(x + 65, y + 22, 5, 2, A1)
        c.r(x + 71, y + 22, 6, 2, T2)
    def mouse(c):
        c.rr(x + 83, y + 15, 8, 10, A1, 2); c.r(x + 84, y + 19, 6, 1, F2); c.r(x + 86, y + 16, 2, 3, L2)
        c.r(x + 89, y + 18, 1, 5, F1)
    def mug(c):                                                         # as wide as the keyboard is deep
        mx, my = x + 6, y + 4
        c.rr(mx, my, 13, 14, R2, 2); c.r(mx + 10, my + 3, 2, 10, R3); c.r(mx + 1, my + 4, 2, 7, R1)
        c.rr(mx + 1, my + 1, 11, 4, A1); c.r(mx + 2, my + 2, 9, 2, W4); c.r(mx + 3, my + 2, 3, 1, W3)   # coffee
        c.r(mx + 4, my + 8, 3, 2, A1); c.r(mx + 3, my + 7, 2, 2, A1); c.r(mx + 6, my + 7, 2, 2, A1)     # a heart
        c.r(mx + 5, my + 10, 1, 1, A1)
        c.r(mx + 13, my + 5, 3, 2, R2); c.r(mx + 15, my + 5, 2, 7, R2); c.r(mx + 13, my + 10, 3, 2, R3)
    def pad(c):
        c.r(x + 21, y + 14, 10, 10, Y1); c.r(x + 21, y + 14, 10, 2, Y2); c.r(x + 23, y + 18, 6, 1, Y3)
        c.r(x + 23, y + 20, 4, 1, Y3); c.r(x + 30, y + 16, 1, 8, Y2)
    def lamp(c):
        c.rr(x + 91, y + 17, 17, 5, L3); c.r(x + 93, y + 17, 13, 1, L2)
        c.r(x + 98, y + 2, 3, 15, L3); c.r(x + 98, y + 2, 1, 15, L2)
        for i in range(13):
            w = 13 + i; lx = x + 99 - w // 2
            c.r(lx, y - 12 + i, w, 1, Y2); c.r(lx + 1, y - 12 + i, w // 3, 1, Y1); c.r(lx + w - w // 4, y - 12 + i, w // 4, 1, Y3)
        c.r(x + 87, y + 1, 25, 1, Y3); c.r(x + 94, y - 12, 11, 1, Y1)
    c.ground(x + 2, y + 46, 112, 12)
    c.prop(body, cast=(3, 3))
    for part in (monitor, note, pad, keyboard, mouse, lamp, mug):
        c.prop(part)
    def steam(c):
        for sx, sy in ((11, 0), (12, -2), (11, -4), (12, -6)):
            c.r(x + sx, y + sy, 2, 2, A1)
    c.prop(steam, cast=None)


# --- cast: the existing sheets, recoloured per material ---------------------------------------------------------
INK = rgb('181425')
SKIN = {'e8b796': K1, 'c28569': K2}
CAST = {'0099db': T3, '124e89': G4, '2ce8f5': T2, '262b44': L4, '3a4466': L3, '5a6988': L2, '8b9bb4': L1,
        '3e2731': W5, '733e39': W4, 'feae34': Y2, 'fee761': Y1, 'ffffff': A1, 'e43b44': R3, 'a22633': R4,
        'f6757a': R2, 'be4a2f': W3, 'd77643': Y3, 'f77622': Y3, 'ead4aa': A1, '3e8948': G3, '265c42': G4,
        '63c74d': G2, '193c3e': L4, 'b86f50': R3, **SKIN}


def person(c, src, row, col, x, y, dark=L4):
    s = Image.open(os.path.join(HERE, '..', src)).convert('RGBA').crop((col * 64, row * 64, col * 64 + 40, row * 64 + 64))
    px = s.load()
    get = lambda q: px[q] if 0 <= q[0] < 40 and 0 <= q[1] < 64 else (0, 0, 0, 0)
    ink = {(sx, sy) for sx in range(40) for sy in range(64) if px[sx, sy] == INK}
    mass = set()                                                        # ink two pixels thick is a material
    for sx, sy in ink:
        block = [(sx, sy), (sx + 1, sy), (sx, sy + 1), (sx + 1, sy + 1)]
        if all(q in ink for q in block):
            mass.update(block)
    out = {}
    for sx in range(40):
        for sy in range(64):
            p = px[sx, sy]
            if not p[3]:
                continue
            if (sx, sy) not in ink:
                out[sx, sy] = rgb(CAST['%02x%02x%02x' % p[:3]])
            elif (sx, sy) in mass:
                out[sx, sy] = rgb(dark)
            else:                                                       # a thin line: a dark tone of what it wraps
                near = [(q, lit) for q, lit in (((sx + 1, sy), 1), ((sx, sy + 1), 1), ((sx - 1, sy), 0), ((sx, sy - 1), 0))
                        if get(q)[3] and q not in ink]
                rim = any(not get(q)[3] for q in ((sx + 1, sy), (sx - 1, sy), (sx, sy + 1), (sx, sy - 1)))
                if not near:
                    out[sx, sy] = rgb(L4)
                else:
                    q, lit = near[0]
                    base = rgb(CAST['%02x%02x%02x' % px[q][:3]])
                    out[sx, sy] = darker(base, (2 if lit else 3) if rim else 3)
    for q, v in out.items():
        px[q] = v
    box = s.getbbox()
    c.ground(x + box[0] + 1, y + box[3] - 4, box[2] - box[0] + 1, 7)    # the shared drop shadow
    c.im.alpha_composite(s, (x, y))


PEOPLE = [('visitor.png', 2, 0, 62, 102), ('hero-detailed.png', 0, 0, 230, 100), ('dog.png', 1, 0, 196, 136, W5),
          ('dana.png', 0, 0, 268, 128)]


def scene():
    c = shell()
    rug(c, 60, 170, 236, 38); doormat(c, 162, 211)
    window(c, 46, 14); board(c, 136, 13); clock(c, 204, 16); bookshelf(c, 262, 12)
    plant(c, 31, 92); bin_(c, 242, 78); desk(c, 124, 75); chair(c, 160, 124)
    for p in PEOPLE:
        person(c, *p)
    return c


if __name__ == '__main__':
    im = scene().im
    used = {'%02x%02x%02x' % p[:3] for _, p in im.getcolors(99999)}
    assert used <= set(PAL) and 24 <= len(used) <= 32, (len(used), used - set(PAL))   # the palette rule
    assert max(colorsys.rgb_to_hsv(*bytes.fromhex(p))[1] for p in PAL) < 0.6          # the saturation ceiling
    out = im.resize((W * 3, H * 3), Image.NEAREST)
    assert out.size == (1056, 720)
    out.save(os.path.join(HERE, 'd07-soft-diorama.png'))
    print('d07-soft-diorama.png', len(used), 'colours')
