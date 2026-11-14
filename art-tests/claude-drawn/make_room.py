# A desk and a small office room, drawn from nothing by code (#61 side test). ENDESGA 32 only.
# v1 (scene-v1.png): #60's map rule, 16 px grid at 2x, no outlines. Asi: "not the same visual language as the
#     characters".
# v2 (scene-v2.png): props drawn like the cast: 1:1 pixels, 1 px dark outline per object, one shade, one highlight.
#     Asi: "much better", but "they need a bit more details / shading / touch ups".
# v3 (this file): same language, more of it. Light comes from the upper left: every object casts a shadow down
#     and right onto whatever is under it, surfaces get a lit and a dark edge, and props carry small details.
# The floor and wall shell are still the 16 px grid at 2x: the floor is an open question.
# Writes desk.png, room.png and scene.png (room with the test cast, zoomed 3x).
# usage (repo root): python3 -I art-tests/claude-drawn/make_room.py
import os
from PIL import Image, ImageChops, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
E32 = set(open(os.path.join(HERE, '../pixellab/e32.hex')).read().split())
INK, SL4, SL3, SL2, SL1, SL0, WHT = '181425', '262b44', '3a4466', '5a6988', '8b9bb4', 'c0cbdc', 'ffffff'
W1, W2, W3, W4, W5, W6, GRAIN = 'ead4aa', 'e4a672', 'd77643', 'b86f50', '733e39', '3e2731', 'c28569'
RED, DRED, GOLD, YEL, ORG, RUST, PINK, PLUM = 'e43b44', 'a22633', 'feae34', 'fee761', 'f77622', 'be4a2f', 'b55088', '68386c'
G1, G2, G3, G4, BLU, CYA, NAVY, ROSE = '63c74d', '3e8948', '265c42', '193c3e', '0099db', '2ce8f5', '124e89', 'f6757a'
SHADE = {RED: DRED, BLU: NAVY, GOLD: ORG, G1: G2, G2: G3, WHT: SL0, PINK: PLUM, ORG: RUST, CYA: BLU, SL1: SL3}
LIGHT = {RED: ROSE, BLU: CYA, GOLD: YEL, G1: YEL, G2: G1, WHT: WHT, PINK: ROSE, ORG: GOLD, CYA: WHT, SL1: SL0}
# one step darker, for cast shadows
DARK = {W1: W2, W2: GRAIN, GRAIN: W4, W3: W4, W4: W5, W5: W6, W6: INK, WHT: SL0, SL0: SL1, SL1: SL2, SL2: SL3,
        SL3: SL4, SL4: INK, RED: DRED, DRED: W6, ROSE: RED, GOLD: ORG, YEL: GOLD, ORG: RUST, RUST: DRED, G1: G2,
        G2: G3, G3: G4, BLU: NAVY, CYA: BLU, NAVY: SL4, PINK: PLUM, PLUM: W6}
W, H = 352, 240


def rgb(c):
    return tuple(bytes.fromhex(c)) + (255,)


DARK_RGB = {rgb(k): rgb(v) for k, v in DARK.items()}
TONED = False  # make_styles.py turns this on


def darker(p, steps):
    for _ in range(steps):
        p = DARK_RGB.get(p, p)
    return p


class Canvas:
    def __init__(self, w=W, h=H, fill=None):
        self.im = Image.new('RGBA', (w, h), rgb(fill) if fill else (0, 0, 0, 0))

    def r(self, x, y, w, h, c):  # filled rectangle
        self.im.paste(rgb(c), (x, y, x + w, y + h))

    def bevel(self, x, y, w, h, c, hi, sh):  # rectangle lit on its top and left edge, dark on bottom and right
        self.r(x, y, w, h, c); self.r(x, y, w, 1, hi); self.r(x, y, 1, h, hi)
        self.r(x, y + h - 1, w, 1, sh); self.r(x + w - 1, y, 1, h, sh)

    def ell(self, x, y, w, h, c):  # filled ellipse, hard edge
        ImageDraw.Draw(self.im).ellipse((x, y, x + w - 1, y + h - 1), fill=rgb(c))

    def prop(self, fn, *a, cast=(2, 2)):
        """Draw one object on its own layer, give it the cast's 1 px dark outline, and let it cast a shadow:
        whatever lies `cast` pixels down-right of it gets one step darker."""
        layer = Canvas(*self.im.size)
        fn(layer, *a)
        alpha = layer.im.getchannel('A')
        solid = alpha
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            s = Image.new('L', alpha.size); s.paste(alpha, (dx, dy)); solid = ImageChops.lighter(solid, s)
        if cast:
            sh = Image.new('L', alpha.size); sh.paste(solid, cast)
            sh = ImageChops.subtract(sh, solid)
            box = sh.getbbox()
            px, m = self.im.load(), sh.load()
            for y in range(box[1], box[3]) if box else ():
                for x in range(box[0], box[2]):
                    if m[x, y]:
                        px[x, y] = DARK_RGB.get(px[x, y], px[x, y])
        edge = ImageChops.subtract(solid, alpha)
        self.im.paste(rgb(INK), mask=edge)
        if TONED and edge.getbbox():  # outline in a dark tone of the object instead of one ink for everything
            px, m, lay, box = self.im.load(), edge.load(), layer.im.load(), edge.getbbox()
            for y in range(box[1], box[3]):
                for x in range(box[0], box[2]):
                    if m[x, y]:
                        near = [lay[q] for q in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1))
                                if 0 <= q[0] < W and 0 <= q[1] < H and lay[q][3]]
                        px[x, y] = darker(near[0], 2)
        self.im.alpha_composite(layer.im)

    def save(self, name, scale=1, check=True):
        used = {'%02x%02x%02x' % p[:3] for _, p in self.im.getcolors(99999) if p[3]}
        assert not check or used <= E32, used - E32  # the one check: every pixel is ENDESGA 32
        self.im.resize((self.im.width * scale, self.im.height * scale), Image.NEAREST).save(os.path.join(HERE, name))


# --- desk: 96 wide; (x, y) is the back-left corner of the desktop --------------------------------------------
def desk_body(c, x, y):
    c.r(x, y + 30, 6, 22, W4); c.r(x, y + 30, 1, 22, W3); c.r(x + 4, y + 30, 2, 22, W5)      # left leg panel
    c.r(x + 6, y + 30, 54, 10, W5); c.r(x + 6, y + 30, 54, 3, W6); c.r(x + 6, y + 39, 54, 1, W6)   # knee panel
    c.r(x + 60, y + 30, 36, 20, W4); c.r(x + 60, y + 30, 36, 2, W5); c.r(x + 93, y + 30, 3, 20, W5)  # drawer unit
    c.r(x + 60, y + 32, 1, 18, W3)
    c.r(x + 62, y + 50, 5, 2, W5); c.r(x + 88, y + 50, 5, 2, W5)                              # feet
    for dy in (32, 41):                                                                       # drawers
        c.r(x + 63, y + dy, 28, 8, INK); c.bevel(x + 64, y + dy + 1, 26, 6, W3, W2, W4)
        c.r(x + 73, y + dy + 3, 8, 2, GOLD); c.r(x + 73, y + dy + 3, 7, 1, YEL); c.r(x + 80, y + dy + 4, 1, 1, ORG)
    c.r(x + 86, y + 35, 1, 2, INK)                                                            # keyhole
    c.r(x, y, 96, 26, W2); c.r(x, y, 96, 2, W1); c.r(x + 93, y + 2, 3, 24, GRAIN)             # desktop
    c.ell(x + 66, y + 8, 28, 15, W1)                                                          # pool of lamp light
    for gx, gy, gw in ((8, 6, 22), (54, 10, 30), (20, 20, 40), (72, 22, 18), (4, 14, 12), (40, 4, 14), (26, 12, 9)):
        c.r(x + gx, y + gy, gw, 1, GRAIN)
    c.r(x + 14, y + 9, 3, 1, W4); c.r(x + 60, y + 21, 2, 1, W4)                               # knots
    c.r(x, y + 26, 96, 4, W3); c.r(x, y + 26, 96, 1, W1); c.r(x, y + 29, 96, 1, W4)           # front edge


def monitor(c, x, y):
    c.r(x + 39, y + 8, 18, 4, SL3); c.r(x + 39, y + 8, 18, 1, SL1); c.r(x + 39, y + 11, 18, 1, SL4)   # foot
    c.r(x + 45, y + 2, 6, 6, SL3); c.r(x + 48, y + 2, 3, 6, SL4)                                       # neck
    c.bevel(x + 26, y - 26, 44, 28, SL3, SL1, SL4); c.r(x + 47, y - 1, 2, 1, SL1); c.r(x + 66, y - 1, 1, 1, G1)
    sx, sy = x + 28, y - 24                                               # screen: a code editor, 40 x 22
    c.r(sx, sy, 40, 22, SL4); c.r(sx, sy, 40, 3, NAVY); c.r(sx, sy + 3, 8, 19, INK)
    for i, col in enumerate((RED, GOLD, G1)):
        c.r(sx + 1 + 2 * i, sy + 1, 1, 1, col)
    for i, w in enumerate((5, 4, 6, 3, 5)):
        c.r(sx + 1, sy + 5 + 3 * i, w, 1, SL2)
    for i, (ind, parts) in enumerate(((0, ((4, PINK), (7, CYA))), (2, ((6, WHT), (3, YEL))), (2, ((3, PINK), (9, G1))),
                                      (4, ((8, WHT),)), (4, ((5, CYA), (4, YEL))), (2, ((2, PINK),)),
                                      (0, ((6, CYA), (3, WHT))), (2, ((10, G1),)))):
        lx = sx + 10 + ind
        for w, col in parts:
            c.r(lx, sy + 5 + 2 * i, w, 1, col); lx += w + 1
    for i in range(7):                                                    # glare
        c.r(sx + 33 + i, sy + 9 - i, 1, 1, SL3); c.r(sx + 36 + i // 2, sy + 12 - i // 2, 1, 1, SL3)


def keyboard(c, x, y):
    c.r(x + 30, y + 15, 34, 9, SL1); c.r(x + 30, y + 15, 34, 1, SL0); c.r(x + 30, y + 23, 34, 1, SL3)
    for row in range(3):
        for i in range(11):
            c.r(x + 31 + 3 * i, y + 16 + 2 * row, 2, 1, WHT)
    c.r(x + 31, y + 22, 5, 1, WHT); c.r(x + 37, y + 22, 17, 1, WHT); c.r(x + 55, y + 22, 8, 1, WHT)


def mouse(c, x, y):
    c.r(x + 68, y + 16, 5, 7, WHT); c.r(x + 68, y + 21, 5, 2, SL0); c.r(x + 72, y + 16, 1, 7, SL0)
    c.r(x + 68, y + 18, 5, 1, SL0); c.r(x + 70, y + 16, 1, 2, SL3)


def mug(c, x, y):
    c.r(x + 9, y + 8, 9, 11, WHT); c.r(x + 16, y + 8, 2, 11, SL0); c.r(x + 9, y + 18, 9, 1, SL0)
    c.r(x + 10, y + 8, 7, 2, W5); c.r(x + 10, y + 8, 7, 1, W6); c.r(x + 11, y + 9, 2, 1, W4)
    c.r(x + 9, y + 13, 9, 2, RED); c.r(x + 16, y + 13, 2, 2, DRED); c.r(x + 10, y + 13, 1, 2, ROSE)
    c.r(x + 18, y + 11, 3, 1, WHT); c.r(x + 20, y + 11, 1, 6, SL0); c.r(x + 18, y + 16, 3, 1, SL0)


def paper(c, x, y):
    c.r(x + 2, y + 4, 10, 13, WHT); c.r(x + 11, y + 4, 1, 13, SL0); c.r(x + 2, y + 16, 10, 1, SL0)
    for i, w in enumerate((6, 7, 4, 7, 5)):
        c.r(x + 3, y + 6 + 2 * i, w, 1, SL1)
    c.r(x + 3, y + 6, 3, 1, RED)


def pen(c, x, y):
    c.r(x + 3, y + 21, 9, 2, BLU); c.r(x + 3, y + 22, 9, 1, NAVY); c.r(x + 12, y + 21, 2, 2, SL0); c.r(x + 14, y + 22, 1, 1, SL3)


def lamp(c, x, y):
    c.r(x + 76, y + 17, 14, 4, SL4); c.r(x + 76, y + 17, 14, 1, SL2); c.r(x + 77, y + 18, 3, 1, SL3)
    c.r(x + 82, y + 2, 2, 15, SL3); c.r(x + 82, y + 2, 1, 15, SL1)
    c.r(x + 88, y + 2, 1, 3, SL1); c.r(x + 88, y + 5, 1, 1, GOLD)                              # pull chain
    for i in range(10):
        w = 12 + 2 * (i // 2); lx = x + 83 - w // 2
        c.r(lx, y - 8 + i, w, 1, GOLD); c.r(lx + 1, y - 8 + i, w // 3, 1, YEL); c.r(lx + w - w // 4, y - 8 + i, w // 4, 1, ORG)
    c.r(x + 74, y + 1, 20, 1, ORG); c.r(x + 90, y + 1, 4, 1, RUST); c.r(x + 77, y - 8, 12, 1, YEL)


def desk(c, x, y):
    c.prop(desk_body, x, y, cast=(3, 3))
    for part in (monitor, paper, pen, keyboard, mouse, lamp):
        c.prop(part, x, y)
    c.prop(mug, x + 7, y)


# --- other props ----------------------------------------------------------------------------------------------
def chair(c, x, y):  # office chair seen from behind, 28 wide
    def base(c):
        c.r(x + 12, y + 32, 4, 5, SL3); c.r(x + 12, y + 32, 1, 5, SL1)
        c.r(x + 3, y + 37, 22, 3, SL4); c.r(x + 3, y + 37, 22, 1, SL2)
        for wx in (1, 11, 22):
            c.r(x + wx, y + 39, 5, 4, SL4); c.r(x + wx + 1, y + 40, 2, 1, SL2)
    def seat(c):
        c.r(x + 3, y, 22, 10, GOLD); c.r(x + 3, y, 22, 2, YEL); c.r(x + 22, y + 2, 3, 8, ORG)
    def back(c):
        c.r(x + 1, y + 8, 26, 24, W3); c.r(x, y + 10, 28, 20, W3)
        c.r(x + 2, y + 9, 24, 2, GOLD); c.r(x + 2, y + 9, 20, 1, YEL)
        c.r(x + 1, y + 11, 24, 1, W2); c.r(x + 1, y + 12, 1, 15, W2)
        c.r(x + 25, y + 11, 3, 16, W4); c.r(x, y + 27, 28, 3, W4); c.r(x + 1, y + 30, 26, 2, W5)
        for sx in (8, 14, 20):
            c.r(x + sx, y + 13, 1, 13, W4); c.r(x + sx - 1, y + 13, 1, 13, W2)
        for sx in (4, 11, 17, 23):
            c.r(x + sx, y + 19, 1, 1, W5)
    for part in (base, seat, back):
        c.prop(part, cast=(3, 3))


def window(c, x, y):
    def frame(c):
        c.r(x, y, 68, 38, WHT); c.r(x + 66, y, 2, 38, SL0); c.r(x, y + 36, 68, 2, SL0)
        for n, px in enumerate((x + 4, x + 36)):
            c.r(px - 1, y + 3, 30, 32, INK); c.r(px, y + 4, 28, 30, BLU); c.r(px, y + 26, 28, 8, CYA)
            for bx, by, bw, col in ((1, 25, 5, SL1), (7, 21, 6, SL2), (14, 27, 4, SL1), (19, 23, 7, SL2)):   # skyline
                bx = bx if n == 0 else 26 - bx - bw
                c.r(px + bx, y + by, bw, 34 - by, col); c.r(px + bx, y + by, 1, 34 - by, SL0 if col == SL1 else SL1)
                for wy in range(by + 2, 33, 3):
                    c.r(px + bx + 2, y + wy, 1, 1, YEL if (wy + bx) % 2 else WHT)
            cx = px + (3 if n == 0 else 12)                                                # cloud
            c.r(cx + 2, y + 8, 7, 2, WHT); c.r(cx, y + 10, 12, 3, WHT); c.r(cx + 1, y + 12, 10, 1, SL0)
            c.r(px, y + 4, 28, 1, NAVY); c.r(px, y + 4, 1, 30, NAVY)                           # frame shadow on the glass
            for i in range(6):                                                             # glare
                c.r(px + 18 + i, y + 14 - i, 1, 1, WHT); c.r(px + 21 + i, y + 14 - i, 1, 1, CYA)
            c.r(px, y + 18, 28, 1, INK); c.r(px, y + 19, 28, 2, WHT); c.r(px, y + 20, 28, 1, SL0); c.r(px, y + 21, 28, 1, INK)
    def sill(c):
        c.r(x - 4, y + 38, 76, 4, SL1); c.r(x - 4, y + 38, 76, 1, WHT); c.r(x - 4, y + 41, 76, 1, SL2)
    def cactus(c):
        c.r(x + 55, y + 23, 5, 11, G2); c.r(x + 55, y + 23, 1, 11, G1); c.r(x + 59, y + 24, 1, 10, G3)
        c.r(x + 60, y + 29, 3, 2, G2); c.r(x + 62, y + 26, 2, 4, G2); c.r(x + 63, y + 26, 1, 4, G3)
        c.r(x + 57, y + 25, 1, 1, YEL); c.r(x + 57, y + 29, 1, 1, YEL)
    def pot(c):
        c.r(x + 53, y + 33, 9, 5, ORG); c.r(x + 53, y + 33, 9, 1, GOLD); c.r(x + 60, y + 34, 2, 4, RUST)
    c.prop(frame, cast=(2, 3)); c.prop(cactus, cast=(1, 1)); c.prop(pot, cast=(1, 1)); c.prop(sill, cast=(2, 3))


def clock(c, x, y):
    def body(c):
        c.ell(x, y, 19, 19, RED); c.ell(x + 2, y + 2, 15, 15, WHT); c.ell(x + 4, y + 4, 12, 12, WHT)
        for tx, ty in ((9, 3), (9, 15), (3, 9), (15, 9)):
            c.r(x + tx, y + ty, 1, 1, SL2)
        c.r(x + 9, y + 5, 1, 5, INK); c.r(x + 9, y + 9, 4, 1, INK); c.r(x + 9, y + 9, 1, 1, RED)
        for i in range(5):                                                  # dark side of the rim
            c.r(x + 14 + i // 2, y + 15 - i // 2 + (i > 2), 1, 1, DRED)
    c.prop(body, cast=(2, 3))


def board(c, x, y):
    def cork(c):
        c.bevel(x, y, 44, 24, W5, W4, W6); c.r(x + 2, y + 2, 40, 20, W3); c.r(x + 2, y + 2, 40, 1, W4); c.r(x + 2, y + 2, 1, 20, W4)
        for i in range(22):
            c.r(x + 3 + (i * 11) % 38, y + 3 + (i * 7) % 18, 1, 1, W4 if i % 3 else W2)
    def notes(c):
        c.r(x + 5, y + 5, 9, 8, WHT); c.r(x + 13, y + 5, 1, 8, SL0); c.r(x + 6, y + 8, 6, 1, SL1); c.r(x + 6, y + 10, 4, 1, SL1)
        c.r(x + 9, y + 4, 2, 2, RED); c.r(x + 9, y + 4, 1, 1, ROSE)
    def photo(c):
        c.r(x + 28, y + 6, 11, 10, WHT); c.r(x + 29, y + 7, 9, 6, CYA); c.r(x + 29, y + 11, 9, 2, G2); c.r(x + 31, y + 10, 3, 1, G1)
        c.r(x + 35, y + 8, 2, 2, YEL); c.r(x + 33, y + 5, 2, 2, BLU)
    def stickies(c):
        c.r(x + 17, y + 4, 7, 7, YEL); c.r(x + 17, y + 10, 7, 1, GOLD); c.r(x + 22, y + 9, 2, 2, GOLD)
        c.r(x + 18, y + 6, 4, 1, ORG); c.r(x + 18, y + 8, 3, 1, ORG)
    def sticky2(c):
        c.r(x + 15, y + 14, 8, 6, PINK); c.r(x + 15, y + 19, 8, 1, PLUM); c.r(x + 16, y + 16, 5, 1, ROSE)
    def ticket(c):
        c.r(x + 27, y + 18, 12, 3, G1); c.r(x + 27, y + 20, 12, 1, G2); c.r(x + 30, y + 18, 1, 3, G2)
    c.prop(cork, cast=(2, 3))
    for part in (notes, photo, stickies, sticky2, ticket):
        c.prop(part, cast=(1, 1))


def bookshelf(c, x, y):  # 64 wide, 74 tall
    def body(c):
        c.r(x, y, 64, 8, W2); c.r(x, y, 64, 1, W1); c.r(x, y + 7, 64, 1, W3); c.r(x + 60, y + 1, 4, 6, GRAIN)
        c.r(x + 6, y + 3, 20, 1, GRAIN); c.r(x + 34, y + 5, 16, 1, GRAIN)
        c.r(x, y + 8, 64, 66, W5); c.r(x + 61, y + 8, 3, 66, W6); c.r(x, y + 8, 2, 66, W4)
        seed = 7
        for s in range(3):
            top = y + 11 + 21 * s
            c.r(x + 3, top, 58, 17, W6); c.r(x + 3, top, 58, 2, INK)                # shelf above shades the back
            c.r(x + 3, top + 17, 58, 3, W4); c.r(x + 3, top + 17, 58, 1, W2); c.r(x + 3, top + 19, 58, 1, W5)
            bx = x + 4
            while bx < x + (44, 54, 45)[s]:
                seed = (seed * 73 + 41) % 997
                w, h = 3 + seed % 4, 10 + seed % 6
                col = (RED, BLU, GOLD, G2, WHT, PINK, ORG, G1, SL1, CYA)[seed % 10]
                by = top + 17 - h
                c.r(bx, by, w, h, col); c.r(bx + w - 1, by, 1, h, SHADE[col]); c.r(bx, by, 1, h, LIGHT[col])
                c.r(bx, by + 2, w, 2, WHT if col not in (WHT, CYA) else SL2)        # label
                c.r(bx + w - 1, by + 2, 1, 2, SL0 if col not in (WHT, CYA) else SL3)
                c.r(bx, by + h - 3, w, 1, SHADE[col])                               # band near the foot
                if w > 4:
                    c.r(bx + 2, by + 6, 1, h - 10, LIGHT[col])                      # title
                c.r(bx + w, by, 1, h, INK); c.r(bx - 1, by, 1, h, INK); c.r(bx, by - 1, w, 1, INK)
                bx += w + 1 + (seed % 7 == 0) * 3
            if s == 2:  # a stack lying flat
                for i, col in enumerate((BLU, RED, GOLD)):
                    c.r(x + 46, top + 13 - 4 * i, 13, 4, INK); c.r(x + 47, top + 14 - 4 * i, 11, 3, col)
                    c.r(x + 47, top + 14 - 4 * i, 11, 1, LIGHT[col]); c.r(x + 47, top + 16 - 4 * i, 11, 1, SHADE[col])
                    c.r(x + 55, top + 14 - 4 * i, 2, 3, WHT)
    def trophy(c):
        tx, ty = x + 49, y + 15
        c.r(tx, ty, 8, 6, GOLD); c.r(tx, ty, 8, 1, YEL); c.r(tx + 1, ty + 1, 2, 4, YEL); c.r(tx + 6, ty + 1, 2, 5, ORG)
        c.r(tx + 1, ty + 6, 6, 1, ORG); c.r(tx + 3, ty + 7, 2, 3, ORG); c.r(tx + 1, ty + 10, 6, 3, W4); c.r(tx + 1, ty + 10, 6, 1, W2)
    c.prop(body, cast=(3, 3)); c.prop(trophy, cast=(1, 1))


def plant(c, x, y):  # (x, y) is the top-left of the pot, 24 wide
    def pot(c):
        c.r(x, y, 24, 4, ORG); c.r(x, y, 24, 1, GOLD); c.r(x + 20, y + 1, 4, 3, RUST); c.r(x, y + 3, 24, 1, RUST)
        for i in range(16):
            ins = 1 + i // 6
            band = i in (4, 5, 10, 11)
            c.r(x + ins, y + 4 + i, 24 - 2 * ins, 1, DRED if band else ORG)
            c.r(x + 20 - ins, y + 4 + i, 4, 1, W6 if band else RUST)
            c.r(x + ins + 2, y + 4 + i, 2, 1, RUST if band else GOLD)
        c.r(x + 1, y + 20, 22, 2, W4); c.r(x + 1, y + 20, 22, 1, W2)                    # saucer
    def stems(c):
        c.r(x + 11, y - 10, 2, 10, G3); c.r(x + 6, y - 6, 2, 6, G3); c.r(x + 16, y - 7, 2, 7, G3)
    def leaf(c, lx, ly, w, h):
        c.ell(lx, ly, w, h, G3); c.ell(lx, ly, w - 1, h - 1, G2); c.ell(lx + 2, ly + 1, w // 2, h // 2, G1)
        c.r(lx + 3, ly + h // 2, w - 5, 1, G3)                                           # midrib
        c.r(lx + 3, ly + 2, 2, 1, YEL)
    c.prop(stems, cast=None)
    for dx, dy, w, h in ((-9, -24, 14, 10), (17, -25, 14, 10), (3, -34, 13, 11), (-12, -12, 14, 9),
                         (20, -13, 15, 9), (-3, -22, 13, 10), (10, -19, 13, 10), (4, -10, 14, 9)):
        c.prop(leaf, x + dx, y + dy, w, h, cast=(2, 3))
    c.prop(pot, cast=(3, 3))


def bin_(c, x, y):
    def body(c):
        c.r(x, y + 3, 14, 15, SL1); c.r(x + 1, y + 18, 12, 1, SL2); c.r(x, y + 3, 2, 15, SL0); c.r(x + 10, y + 3, 4, 15, SL2)
        for sx in (3, 6, 9, 12):
            c.r(x + sx, y + 5, 1, 12, SL3)
        c.r(x, y + 2, 14, 2, SL0); c.r(x, y + 2, 14, 1, WHT)
    def paper(c, px, py):
        c.r(px, py, 5, 4, WHT); c.r(px + 3, py + 1, 2, 3, SL0); c.r(px + 1, py + 2, 1, 1, SL1)
    c.prop(paper, x + 2, y - 1, cast=None); c.prop(paper, x + 7, y - 2, cast=None); c.prop(body, cast=(3, 3))
    c.prop(paper, x + 18, y + 14, cast=(1, 1))                                          # one that missed


def rug(c, x, y, w, h):
    def body(c):
        for fy in range(y + 1, y + h - 1, 2):                     # fringe
            c.r(x - 4, fy, 4, 1, W1); c.r(x + w, fy, 4, 1, W1)
        c.r(x, y, w, h, DRED); c.r(x + 3, y + 3, w - 6, h - 6, GOLD); c.r(x + 4, y + 4, w - 8, h - 8, DRED)
        c.r(x + 7, y + 7, w - 14, h - 14, GOLD); c.r(x + 8, y + 8, w - 16, h - 16, RED)
        for bx in range(x + 6, x + w - 6, 4):                     # beads in the border
            c.r(bx, y + 5, 1, 1, YEL); c.r(bx, y + h - 6, 1, 1, YEL)
        for by in range(y + 9, y + h - 8, 4):
            c.r(x + 5, by, 1, 1, YEL); c.r(x + w - 6, by, 1, 1, YEL)
        for wy in range(y + 10, y + h - 9, 3):                    # weave
            for wx in range(x + 10 + (wy % 2) * 3, x + w - 10, 6):
                c.r(wx, wy, 2, 1, DRED)
        for cx in range(x + 28, x + w - 20, 32):                  # diamonds
            for i in range(-9, 10):
                for j in range(-9, 10):
                    d = abs(i) + abs(j)
                    if d <= 9:
                        c.r(cx + i, y + h // 2 + j, 1, 1, (RED if d in (2, 3) else DRED) if d in (6, 7, 2, 3)
                            else GOLD if d in (8, 9, 0, 1) else YEL)
    c.prop(body, cast=None)


def doormat(c, x, y):
    def body(c):
        c.r(x, y, 28, 12, G2); c.r(x, y, 28, 1, G1); c.r(x + 2, y + 2, 24, 8, G3); c.r(x + 3, y + 3, 22, 6, G2)
        for i in range(5):
            c.r(x + 5 + 4 * i, y + 5, 2, 2, G1); c.r(x + 6 + 4 * i, y + 6, 1, 1, YEL)
        c.r(x, y + 11, 28, 1, G3)
    c.prop(body, cast=None)


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
    window(c, 52, 14); board(c, 144, 12); clock(c, 212, 18)
    bookshelf(c, 264, 12); plant(c, 22, 86); bin_(c, 242, 72)
    desk(c, 136, 68); chair(c, 156, 118)
    return c


PEOPLE = [('hero-detailed.png', 3, 0, 222, 96), ('dana.png', 0, 0, 252, 122), ('dog.png', 1, 0, 206, 130),
          ('visitor.png', 2, 0, 60, 100), ('dog.png', 0, 0, 96, 62)]


def people(r):
    """The test cast standing in the room, as the game would draw them."""
    for src, row, col, x, y in PEOPLE:
        s = Image.open(os.path.join(HERE, src)).convert('RGBA').crop((col * 64, row * 64, col * 64 + 40, row * 64 + 64))
        if TONED:  # the outer outline takes a dark tone of what it wraps
            px = s.load()
            for sy in range(64):
                for sx in range(40):
                    if px[sx, sy] == rgb(INK):
                        q4 = [(sx + 1, sy), (sx - 1, sy), (sx, sy + 1), (sx, sy - 1)]
                        near = [px[q] for q in q4 if 0 <= q[0] < 40 and 0 <= q[1] < 64]
                        inside = [p for p in near if p[3] and p != rgb(INK)]
                        if inside and (len(near) < 4 or any(not p[3] for p in near)):
                            px[sx, sy] = darker(inside[0], 2)
        r.im.alpha_composite(s, (x, y))
    return r


if __name__ == '__main__':
    d = Canvas(100, 84); desk(d, 2, 28); d.save('desk.png')
    r = room(); r.save('room.png')
    people(r).save('scene.png', 3)
    print('desk, room, scene written; all ENDESGA 32')
