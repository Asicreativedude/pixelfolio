# Direction 3, "Neon flat minimalism": the office corner as a still (reports/Pixel art style directions.md, section 3).
# Rules followed: 20 colours (a dark navy / slate / teal base plus the fixed accent pair, cyan and hot pink);
# no outlines, edges exist only where value or hue steps; every surface is one lit tone and one shadow tone
# with a hard edge (light from the upper left: tops and left sides lit, fronts and right sides in shadow, and
# every object throws a hard shadow down-right that turns what it covers into its shadow tone); furniture is
# geometric blocks; the cast is faceless, told apart by hair shape and one colour block; no texture.
# The one runtime effect is drawn openly, not pixelled: smooth radial glows (screen, lamp, moon) added on top
# of the 3x export. The palette check runs on the native picture before the glows.
# usage (repo root): python3 -I art-tests/claude-drawn/directions/make_d03_neon_flat.py
import os
from PIL import Image, ImageChops, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
W, H, Z = 352, 240, 3
VOID, NAVYD, NAVY, SLD, SL, SLL = '0c0f1f', '151b36', '1e2a4c', '2a3a60', '44598a', '8598bd'
TEALD, TEAL, TEALL, MINT, PALE = '10333f', '185360', '2c8a8c', '52d0bd', 'd6efe6'
CYAN, PINK = '5ef6ff', 'ff3f8e'                                 # the accent pair: screens, and the one pressable thing
SKIN, SKINS, BRICK, WARMS, SAND, ORNG, SAGE = 'd2ab98', '8f6c78', 'c45a5c', '6e3a5c', 'e6cc93', 'cf8350', '8cc47e'
PALETTE = {VOID, NAVYD, NAVY, SLD, SL, SLL, TEALD, TEAL, TEALL, MINT, PALE, CYAN, PINK, SKIN, SKINS, BRICK, WARMS,
           SAND, ORNG, SAGE}
# lit tone -> its one shadow tone
SH = {TEAL: TEALD, NAVY: NAVYD, SL: SLD, SLL: SL, PALE: SLL, MINT: TEALL, SKIN: SKINS, BRICK: WARMS, SAND: ORNG,
      ORNG: WARMS, SAGE: TEALL, NAVYD: VOID, TEALL: TEAL}


def rgb(c):
    return tuple(bytes.fromhex(c)) + (255,)


SH_RGB = {rgb(k): rgb(v) for k, v in SH.items()}


class Cv:
    def __init__(self, fill=None):
        self.im = Image.new('RGBA', (W, H), rgb(fill) if fill else (0, 0, 0, 0))
        self.d = ImageDraw.Draw(self.im)

    def r(self, x, y, w, h, c):
        self.d.rectangle((x, y, x + w - 1, y + h - 1), fill=rgb(c))

    def split(self, x, y, w, h, c, dark):  # a block: lit, with its right `dark` columns in the shadow tone
        self.r(x, y, w, h, c); self.r(x + w - dark, y, dark, h, SH[c])

    def e(self, x, y, w, h, c):
        self.d.ellipse((x, y, x + w - 1, y + h - 1), fill=rgb(c))

    def p(self, pts, c):
        self.d.polygon(pts, fill=rgb(c))

    def put(self, fn, n=0):
        """Draw one object on its own layer and let it throw a hard shadow n px down-right."""
        L = Cv(); fn(L)
        a = L.im.getchannel('A'); sh = Image.new('L', a.size)
        for k in range(1, n + 1):
            s = Image.new('L', a.size); s.paste(a, (k, k)); sh = ImageChops.lighter(sh, s)
        box = sh.getbbox()
        px, m = self.im.load(), sh.load()
        for y in range(box[1], box[3]) if box else ():
            for x in range(box[0], box[2]):
                if m[x, y] and px[x, y][3]:
                    px[x, y] = SH_RGB.get(px[x, y], px[x, y])
        self.im.alpha_composite(L.im)
        self.d = ImageDraw.Draw(self.im)


# --- room ------------------------------------------------------------------------------------------------------
def shell(c):
    c.r(16, 8, 320, 56, NAVY); c.r(16, 60, 320, 4, NAVYD)
    c.r(16, 64, 320, 160, TEAL); c.r(160, 224, 32, 16, TEAL)


def window(c):
    def body(L):
        L.r(50, 12, 72, 42, SL); L.r(120, 12, 2, 42, SLD); L.r(50, 52, 72, 2, SLD)
        for n, px in enumerate((54, 88)):
            L.r(px, 16, 30, 34, NAVYD); L.r(px, 38, 30, 12, SLD)
            for bx, bw, bh in ((1, 6, 9), (8, 5, 15), (14, 7, 6), (22, 6, 12)):
                bx = bx if n == 0 else 30 - bx - bw
                L.r(px + bx, 50 - bh, bw, bh, VOID)
        L.e(99, 19, 11, 11, PALE)
        for sx, sy in ((60, 21), (72, 27), (66, 33), (92, 31), (111, 34)):
            L.r(sx, sy, 1, 1, SLL)
    c.put(body, 2)
    c.put(lambda L: L.split(47, 54, 78, 3, SLL, 20), 2)


def board(c):
    c.put(lambda L: (L.r(144, 12, 44, 26, SL), L.r(186, 12, 2, 26, SLD), L.r(144, 36, 44, 2, SLD)), 2)
    for x, y, w, h, col in ((148, 16, 9, 10, PALE), (160, 15, 8, 8, SLL), (171, 17, 12, 10, TEALL), (159, 26, 8, 7, MINT)):
        c.put(lambda L: L.r(x, y, w, h, col), 1)


def clock(c):
    def body(L):
        L.e(211, 16, 21, 21, SLL); L.e(213, 18, 17, 17, PALE)
        L.r(221, 21, 1, 6, VOID); L.r(221, 26, 5, 1, VOID)
    c.put(body, 2)


def bookshelf(c):
    def body(L):
        L.split(264, 12, 62, 80, SL, 8)
        for s in range(3):
            L.r(268, 17 + 24 * s, 46, 20, NAVYD)
        def stand(x, base, books):
            for w, h, col in books:
                L.r(x, base - h, w, h, col); x += w + 1
        stand(270, 37, ((5, 15, SLL), (4, 12, TEALL), (5, 16, SL), (4, 13, WARMS), (5, 14, SLL)))
        L.p([(305, 27), (309, 21), (313, 27), (309, 36)], PALE); L.p([(309, 21), (313, 27), (309, 36)], SLL)  # a crystal
        stand(270, 61, ((4, 13, TEALL), (6, 16, SLL), (5, 12, SL), (4, 15, TEALL), (5, 13, WARMS), (4, 16, SLL)))
        for i, col in enumerate((SLL, SL, TEALL)):
            L.r(270, 81 - 4 * i, 17 - 2 * i, 4, col)
        stand(292, 85, ((5, 14, SL), (4, 16, SLL), (5, 13, TEALL)))
    c.put(body, 9)


def plant(c):
    def body(L):
        bx, by = 35, 87
        for tx, ty, w in ((9, 76, 5), (61, 76, 5), (13, 58, 6), (57, 58, 6), (23, 44, 6), (48, 44, 6), (35, 37, 6)):
            mx, my = (bx + tx) / 2, (by + ty) / 2
            dx, dy = tx - bx, ty - by
            ln = (dx * dx + dy * dy) ** .5
            nx, ny = -dy / ln * w, dx / ln * w
            a, b = (mx + nx, my + ny), (mx - nx, my - ny)
            up, down = (a, b) if a[1] + a[0] < b[1] + b[0] else (b, a)   # the half that faces the upper left is lit
            L.p([(bx, by), up, (tx, ty)], MINT); L.p([(bx, by), down, (tx, ty)], TEALL)
        L.p([(23, 89), (47, 89), (44, 109), (26, 109)], SL); L.p([(39, 89), (47, 89), (44, 109), (38, 109)], SLD)
        L.split(21, 85, 28, 4, SLL, 9)
    c.put(body, 8)


def bin_(c):
    c.put(lambda L: L.split(263, 92, 4, 3, PALE, 1), 1)
    def body(L):
        L.r(245, 70, 4, 4, PALE); L.split(250, 69, 5, 5, PALE, 2)
        L.p([(242, 74), (258, 74), (256, 94), (244, 94)], SL); L.p([(252, 74), (258, 74), (256, 94), (251, 94)], SLD)
    c.put(body, 6)


def desk(c):
    def body(L):
        L.r(136, 94, 96, 6, SLD); L.r(136, 94, 8, 26, SLD); L.r(196, 94, 36, 26, SLD)
        L.r(200, 103, 28, 1, NAVYD); L.r(200, 111, 28, 1, NAVYD)
        L.r(134, 68, 100, 26, SL)
    c.put(body, 7)
    c.put(lambda L: L.r(139, 71, 10, 13, PALE), 1)
    c.put(lambda L: (L.split(152, 77, 7, 9, PALE, 2), L.r(159, 79, 2, 1, SLL), L.r(160, 79, 1, 5, SLL), L.r(159, 83, 2, 1, SLL)), 2)
    def monitor(L):
        L.r(172, 74, 22, 4, NAVYD); L.r(179, 70, 8, 4, NAVYD)
        L.r(160, 36, 48, 34, NAVYD); L.r(206, 36, 2, 34, VOID); L.r(160, 68, 48, 2, VOID)
        L.r(163, 39, 42, 27, CYAN)
        for x, y, w, col in ((166, 43, 10, PALE), (178, 43, 8, TEALL), (169, 47, 16, TEALL), (169, 51, 9, PALE),
                             (180, 51, 12, TEALL), (169, 55, 12, TEALL), (166, 59, 7, PALE)):
            L.r(x, y, w, 2, col)
    c.put(monitor, 4)
    c.put(lambda L: (L.r(164, 82, 36, 8, SLL), L.r(164, 88, 36, 2, SL)), 1)
    c.put(lambda L: L.split(204, 83, 5, 7, SLL, 2), 1)
    def lamp(L):
        L.r(213, 85, 14, 4, NAVYD); L.r(219, 68, 2, 17, NAVYD)
        L.p([(213, 54), (226, 54), (232, 69), (207, 69)], PINK)
    c.put(lamp, 3)


def chair(c):
    def body(L):
        L.r(160, 154, 24, 3, NAVYD); L.r(170, 146, 4, 8, NAVYD)
        for x in (158, 170, 181):
            L.r(x, 156, 5, 4, NAVYD)
        L.r(159, 116, 26, 5, SLL); L.split(157, 120, 30, 26, SL, 9)
    c.put(body, 7)


def rug(c):
    c.r(52, 164, 248, 40, NAVY)
    for x, y, w, h in ((56, 168, 240, 2), (56, 198, 240, 2), (56, 168, 2, 32), (294, 168, 2, 32)):
        c.r(x, y, w, h, SL)
    for cx in (100, 150, 200):
        for rad, col in ((12, SL), (9, NAVY), (5, TEALL)):
            c.p([(cx - rad, 184), (cx, 184 - rad), (cx + rad, 184), (cx, 184 + rad)], col)
    c.r(162, 209, 28, 11, SL); c.r(164, 211, 24, 7, NAVY)


# --- cast: faceless; (cx, fy) is the middle of the feet. Left of each figure is lit, right is in shadow -----------
def man(L, cx, fy, top, top_s, leg, leg_s, long_sleeves):
    L.r(cx - 5, fy - 14, 4, 14, leg); L.r(cx + 1, fy - 14, 4, 14, leg_s)
    L.r(cx - 10, fy - 29, 3, 16, SKIN); L.r(cx + 7, fy - 29, 3, 16, SKINS)                 # arms
    n = 13 if long_sleeves else 7
    L.r(cx - 10, fy - 29, 3, n, top); L.r(cx + 7, fy - 29, 3, n, top_s)
    L.r(cx - 9, fy - 30, 2, 1, top); L.r(cx + 7, fy - 30, 2, 1, top_s)
    L.r(cx - 7, fy - 31, 14, 18, top); L.r(cx + 2, fy - 31, 5, 18, top_s)
    L.r(cx - 6, fy - 44, 12, 12, SKIN); L.r(cx + 2, fy - 44, 4, 12, SKINS)                 # head
    L.r(cx - 5, fy - 32, 10, 1, SKIN); L.r(cx + 2, fy - 32, 3, 1, SKINS)


def hero(c, cx, fy):
    def fig(L):
        man(L, cx, fy, MINT, TEALL, NAVYD, VOID, False)
        L.r(cx - 6, fy - 37, 12, 5, NAVYD); L.r(cx + 2, fy - 37, 4, 5, VOID)               # beard
        L.r(cx - 5, fy - 32, 10, 1, NAVYD); L.r(cx + 2, fy - 32, 3, 1, VOID)
        L.r(cx - 5, fy - 40, 4, 2, CYAN); L.r(cx + 1, fy - 40, 4, 2, CYAN)                 # glasses catch the screen
        q = [(cx - 5, fy - 44), (cx - 5, fy - 47), (cx - 1, fy - 53), (cx + 2, fy - 51), (cx + 5, fy - 47), (cx + 5, fy - 44)]
        L.p(q, NAVYD); L.p([(cx - 1, fy - 53), (cx + 2, fy - 51), (cx + 5, fy - 47), (cx + 5, fy - 44), (cx + 1, fy - 44)], VOID)
        L.r(cx - 7, fy - 46, 2, 6, SLL); L.r(cx + 5, fy - 46, 2, 6, SL)                    # grey sides
    c.put(fig, 10)


def visitor(c, cx, fy):
    def fig(L):
        man(L, cx, fy, SAGE, TEALL, SLD, NAVYD, True)
        L.r(cx - 7, fy - 47, 14, 6, ORNG); L.r(cx + 2, fy - 47, 5, 6, WARMS)
        L.p([(cx - 7, fy - 41), (cx + 1, fy - 41), (cx - 7, fy - 36)], ORNG)                # side-swept fringe
    c.put(fig, 10)


def dana(c, cx, fy):
    def fig(L):
        L.r(cx - 4, fy - 10, 3, 10, SKIN); L.r(cx + 1, fy - 10, 3, 10, SKINS)
        L.r(cx - 4, fy - 2, 3, 2, VOID); L.r(cx + 1, fy - 2, 3, 2, VOID)
        L.r(cx - 9, fy - 30, 3, 13, SKIN); L.r(cx + 6, fy - 30, 3, 13, SKINS)
        L.p([(cx - 8, fy - 44), (cx + 7, fy - 44), (cx + 7, fy - 27), (cx + 9, fy - 22), (cx - 10, fy - 22), (cx - 8, fy - 27)], SAND)
        L.p([(cx + 3, fy - 44), (cx + 7, fy - 44), (cx + 7, fy - 27), (cx + 9, fy - 22), (cx + 3, fy - 22)], ORNG)
        L.p([(cx - 5, fy - 31), (cx + 4, fy - 31), (cx + 10, fy - 9), (cx - 11, fy - 9)], BRICK)
        L.p([(cx + 1, fy - 31), (cx + 4, fy - 31), (cx + 10, fy - 9), (cx + 2, fy - 9)], WARMS)
        L.r(cx - 5, fy - 40, 10, 10, SKIN); L.r(cx + 2, fy - 40, 3, 10, SKINS)
    c.put(fig, 10)


def dog(c, cx, fy):
    def fig(L):
        L.r(cx - 4, fy - 7, 3, 6, ORNG); L.r(cx + 5, fy - 7, 3, 6, ORNG)                    # far legs
        L.r(cx - 8, fy - 7, 3, 7, SAND); L.r(cx + 8, fy - 7, 3, 7, SAND)
        L.r(cx - 9, fy - 15, 21, 6, SAND); L.r(cx - 9, fy - 9, 21, 2, ORNG)
        L.p([(cx + 9, fy - 14), (cx + 11, fy - 23), (cx + 14, fy - 23), (cx + 12, fy - 14)], SAND)   # tail up
        L.r(cx - 16, fy - 22, 10, 9, SAND); L.r(cx - 20, fy - 17, 4, 4, SAND); L.r(cx - 20, fy - 14, 13, 1, ORNG)
        L.p([(cx - 16, fy - 22), (cx - 15, fy - 27), (cx - 12, fy - 22)], SAND)
        L.p([(cx - 11, fy - 22), (cx - 9, fy - 27), (cx - 7, fy - 22)], ORNG)
    c.put(fig, 6)


def glow(im, cx, cy, rad, col, strength):
    """A smooth radial light, screen-blended over the upscaled picture. Not pixel art, on purpose."""
    g = Image.new('L', (128, 128))
    g.putdata([int(255 * strength * max(0, 1 - ((x - 63.5) ** 2 + (y - 63.5) ** 2) ** .5 / 64) ** 1.8)
               for y in range(128) for x in range(128)])
    g = g.resize((2 * rad, 2 * rad), Image.BICUBIC)
    a = Image.new('L', im.size); a.paste(g, (cx - rad, cy - rad))
    light = Image.merge('RGB', [a.point(lambda v, k=k: v * k // 255) for k in bytes.fromhex(col)])
    return ImageChops.screen(im, light)


if __name__ == '__main__':
    c = Cv(VOID)
    shell(c); rug(c); window(c); board(c); clock(c); bookshelf(c); plant(c); bin_(c); desk(c); chair(c)
    visitor(c, 80, 160); hero(c, 240, 160); dog(c, 234, 194); dana(c, 276, 186)
    used = {'%02x%02x%02x' % p[:3] for _, p in c.im.getcolors(99999)}
    assert used <= PALETTE and len(used) <= 20, used - PALETTE          # before the glows: 20 colours at most
    big = c.im.convert('RGB').resize((W * Z, H * Z), Image.NEAREST)
    big = glow(big, 184 * Z, 54 * Z, 84 * Z, CYAN, .55)
    big = glow(big, 184 * Z, 52 * Z, 34 * Z, CYAN, .35)
    big = glow(big, 220 * Z, 72 * Z, 64 * Z, PINK, .7)
    big = glow(big, 220 * Z, 63 * Z, 22 * Z, PINK, .4)
    big = glow(big, 104 * Z, 24 * Z, 30 * Z, PALE, .3)
    out = os.path.join(HERE, 'd03-neon-flat.png')
    big.save(out)
    assert Image.open(out).size == (1056, 720)
    print('d03-neon-flat.png written,', len(used), 'colours before the glows')
