# Direction 10, "Paper cut-out": the office corner as a still (reports/Pixel art style directions.md, section 10).
# Rules followed: 8 flat colours, each with exactly one shadow tone (16 on screen at most); no outlines at all;
# every piece is one flat fill and casts one flat shadow down and to the right onto whatever lies under it
# (the pixel under a shadow becomes that colour's shadow tone); geometry is circles, rounded rectangles and
# triangles; characters are a block head, a one-shape body and dots for a face.
# usage (repo root): python3 -I art-tests/claude-drawn/directions/make_d10_paper_cutout.py
import os
from PIL import Image, ImageChops, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 352, 240
#        fill      shadow
PAIRS = {'f6ead2': 'd9c7a4',   # CREAM  wall, paper, grey hair
         'cbbbe9': 'a694cf',   # LILAC  floor
         'c98b55': '9a6238',   # WOOD
         '2f3460': '1c1f40',   # NAVY   table, screens, black hair, trousers, rug
         '2a9d8f': '1c7470',   # TEAL
         'e8623f': 'b5432b',   # CORAL
         'f2b93b': 'c98f24',   # MUST
         'f5c29c': 'd69c78'}   # SKIN
CREAM, LILAC, WOOD, NAVY, TEAL, CORAL, MUST, SKIN = PAIRS
SH = PAIRS


def rgb(c):
    return tuple(bytes.fromhex(c)) + (255,)


SH_RGB = {rgb(k): rgb(v) for k, v in PAIRS.items()}


class Cv:
    def __init__(self, fill=None):
        self.im = Image.new('RGBA', (W, H), rgb(fill) if fill else (0, 0, 0, 0))
        self.d = ImageDraw.Draw(self.im)

    def r(self, x, y, w, h, c):
        self.d.rectangle((x, y, x + w - 1, y + h - 1), fill=rgb(c))

    def rr(self, x, y, w, h, rad, c):
        self.d.rounded_rectangle((x, y, x + w - 1, y + h - 1), rad, fill=rgb(c))

    def e(self, x, y, w, h, c):
        self.d.ellipse((x, y, x + w - 1, y + h - 1), fill=rgb(c))

    def p(self, pts, c):
        self.d.polygon(pts, fill=rgb(c))

    def put(self, fn, h=1):
        """One piece of paper: draw it on its own layer, drop its shadow (the silhouette swept h px down-right)
        onto what is already here, then lay the piece on top."""
        L = Cv(); fn(L)
        a = L.im.getchannel('A'); sh = Image.new('L', a.size)
        for k in range(1, h + 1):
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
    c.put(lambda L: L.rr(12, 56, 328, 176, 7, LILAC), 3)
    c.put(lambda L: L.rr(12, 8, 328, 58, 7, CREAM), 2)


def window(c):
    def frame(L):
        L.rr(52, 13, 68, 40, 4, WOOD)
        for px in (56, 88):
            L.rr(px, 17, 28, 32, 2, TEAL)
        L.e(60, 21, 11, 11, MUST)
        L.rr(93, 27, 17, 6, 3, CREAM); L.rr(97, 24, 9, 6, 3, CREAM)
        L.p([(56, 48), (66, 38), (76, 48)], CREAM); L.p([(68, 48), (75, 41), (83, 48)], CREAM)   # far hills
        L.r(56, 48, 28, 1, CREAM)
    c.put(frame, 2)
    c.put(lambda L: L.rr(48, 51, 76, 5, 2, WOOD), 2)


def board(c):
    c.put(lambda L: L.rr(143, 12, 46, 29, 3, WOOD), 2)
    c.put(lambda L: L.r(147, 16, 11, 12, CREAM))
    c.put(lambda L: L.r(161, 15, 9, 9, MUST))
    c.put(lambda L: L.r(159, 28, 10, 8, CORAL))
    def photo(L):
        L.r(173, 18, 13, 13, CREAM); L.r(175, 20, 9, 7, TEAL); L.e(179, 21, 4, 4, MUST)
    c.put(photo)
    c.put(lambda L: L.r(149, 32, 7, 5, TEAL))


def clock(c):
    def body(L):
        L.e(211, 15, 23, 23, CORAL); L.e(214, 18, 17, 17, CREAM)
        L.r(222, 21, 2, 7, NAVY); L.r(222, 26, 6, 2, NAVY)
    c.put(body, 2)


def bookshelf(c):
    def body(L):
        L.rr(266, 12, 60, 80, 4, WOOD)
        for s in range(3):
            L.rr(270, 17 + 24 * s, 52, 20, 2, SH[WOOD])
    c.put(body, 6)
    def stand(L, x, base, books):
        for w, h, col in books:
            L.rr(x, base - h, w, h, 1, col); x += w + 1
    c.put(lambda L: stand(L, 272, 37, ((5, 15, TEAL), (4, 12, CORAL), (5, 16, MUST), (5, 13, CREAM), (4, 15, NAVY))))
    def trophy(L):
        L.p([(304, 22), (316, 22), (310, 31)], MUST); L.r(309, 30, 3, 4, MUST); L.rr(306, 34, 9, 3, 1, NAVY)
    c.put(trophy)
    c.put(lambda L: stand(L, 272, 61, ((4, 13, CORAL), (6, 16, CREAM), (5, 12, TEAL), (4, 15, MUST))))
    def globe(L):
        L.e(303, 45, 13, 13, TEAL); L.e(306, 47, 5, 4, CREAM); L.rr(305, 58, 9, 3, 1, NAVY)
    c.put(globe)
    def stack(L):
        for i, col in enumerate((NAVY, MUST, CORAL)):
            L.rr(272, 81 - 4 * i, 17 - 2 * i, 4, 1, col)
    c.put(stack)
    c.put(lambda L: stand(L, 296, 85, ((5, 14, TEAL), (4, 16, CREAM), (5, 13, CORAL), (5, 15, MUST))))


def plant(c):
    def all_(L):
        for x, y, d in ((27, 44, 15), (15, 54, 14), (38, 50, 16), (22, 60, 17), (10, 68, 14), (41, 64, 15), (28, 70, 15)):
            L.put(lambda M: M.e(x, y, d, d, TEAL), 2)
        L.put(lambda M: M.p([(22, 88), (47, 88), (44, 110), (25, 110)], CORAL))
        L.put(lambda M: M.rr(20, 84, 29, 7, 2, CORAL))
    c.put(all_, 6)


def bin_(c):
    c.put(lambda L: L.e(262, 92, 6, 6, CREAM))
    def body(L):
        L.e(245, 68, 7, 7, CREAM); L.put(lambda M: M.e(250, 66, 7, 7, CREAM))
        L.put(lambda M: M.p([(243, 76), (259, 76), (257, 96), (245, 96)], NAVY))
        L.put(lambda M: M.rr(241, 73, 20, 5, 2, NAVY))
    c.put(body, 5)


def desk(c):
    def body(L):
        L.r(136, 94, 96, 7, SH[WOOD]); L.rr(136, 94, 8, 28, 1, SH[WOOD]); L.rr(196, 94, 36, 28, 1, SH[WOOD])
        for y in (102, 111):
            L.rr(199, y, 30, 8, 2, WOOD); L.e(212, y + 2, 4, 4, MUST)
        L.rr(133, 67, 102, 29, 4, WOOD)
    c.put(body, 6)
    def paper(L):
        L.r(139, 71, 11, 14, CREAM)
        for i, w in enumerate((7, 5, 7, 4)):
            L.r(141, 73 + 3 * i, w, 1, SH[CREAM])
    c.put(paper)
    def mug(L):
        L.rr(153, 76, 9, 11, 2, CORAL); L.r(162, 79, 3, 1, CORAL); L.r(164, 79, 1, 6, CORAL); L.r(162, 84, 3, 1, CORAL)
        L.e(154, 76, 7, 4, NAVY)
    c.put(mug, 2)
    def monitor(L):
        L.rr(173, 76, 22, 5, 2, NAVY); L.r(181, 68, 6, 9, NAVY)
        L.rr(160, 38, 48, 32, 3, NAVY); L.rr(163, 41, 42, 24, 2, TEAL)
        for x, y, w, col in ((166, 45, 9, CREAM), (177, 45, 6, MUST), (169, 49, 14, CREAM), (169, 53, 7, CORAL),
                             (178, 53, 11, CREAM), (172, 57, 9, MUST), (166, 61, 5, CREAM)):
            L.r(x, y, w, 2, col)
    c.put(monitor, 4)
    def keyboard(L):
        L.rr(164, 83, 37, 9, 2, CREAM)
        for y in (85, 87, 89):
            L.r(166, y, 33, 1, SH[CREAM])
    c.put(keyboard)
    c.put(lambda L: L.rr(205, 84, 6, 8, 3, CREAM))
    def lamp(L):
        L.rr(213, 85, 15, 5, 2, NAVY); L.r(219, 66, 3, 20, NAVY)
        L.p([(213, 54), (227, 54), (233, 69), (207, 69)], MUST)
    c.put(lamp, 4)


def chair(c):
    def body(L):
        L.rr(159, 153, 26, 4, 2, NAVY)
        for x in (157, 169, 181):
            L.e(x, 155, 6, 6, NAVY)
        L.r(170, 144, 4, 10, NAVY)
        L.rr(159, 116, 26, 12, 4, SH[MUST])
        L.rr(156, 122, 32, 25, 6, MUST)
    c.put(body, 6)


def rug(c):
    def body(L):
        L.rr(52, 164, 248, 42, 6, NAVY); L.rr(56, 168, 240, 34, 4, CREAM); L.rr(58, 170, 236, 30, 3, NAVY)
        for i, cx in enumerate(range(83, 210, 62)):
            if i % 2:
                L.p([(cx - 9, 193), (cx, 177), (cx + 9, 193)], MUST)
            else:
                L.e(cx - 8, 177, 17, 17, CORAL)
    c.put(body)
    c.put(lambda L: (L.rr(162, 212, 28, 12, 3, TEAL), L.r(166, 217, 20, 2, CREAM)))


# --- cast: (cx, fy) is the middle of the feet --------------------------------------------------------------------
def legs(L, cx, fy, col):
    L.rr(cx - 8, fy - 13, 7, 13, 2, col); L.rr(cx + 1, fy - 13, 7, 13, 2, col)


def hero(c, cx, fy):
    def fig(L):
        legs(L, cx, fy, NAVY)
        L.put(lambda M: (M.rr(cx - 16, fy - 26, 5, 12, 2, SKIN), M.rr(cx + 11, fy - 26, 5, 12, 2, SKIN)))
        L.put(lambda M: (M.rr(cx - 17, fy - 30, 8, 9, 3, TEAL), M.rr(cx + 9, fy - 30, 8, 9, 3, TEAL),
                         M.rr(cx - 11, fy - 31, 22, 21, 5, TEAL)))
        def head(M):
            M.rr(cx - 11, fy - 52, 22, 24, 7, SKIN)
            M.rr(cx - 11, fy - 40, 22, 12, 7, NAVY); M.r(cx - 11, fy - 40, 22, 3, SKIN)       # beard
            M.r(cx - 11, fy - 44, 2, 6, NAVY); M.r(cx + 9, fy - 44, 2, 6, NAVY)               # ... up to the ears
            M.r(cx - 2, fy - 34, 4, 1, SKIN)
            M.rr(cx - 8, fy - 46, 7, 6, 2, CREAM); M.rr(cx + 1, fy - 46, 7, 6, 2, CREAM)       # glasses
            M.r(cx - 1, fy - 44, 2, 1, NAVY); M.r(cx - 5, fy - 44, 2, 2, NAVY); M.r(cx + 3, fy - 44, 2, 2, NAVY)
        L.put(head)
        L.put(lambda M: (M.r(cx - 11, fy - 50, 3, 6, CREAM), M.r(cx + 8, fy - 50, 3, 6, CREAM)))   # grey sides
        L.put(lambda M: (M.rr(cx - 9, fy - 56, 18, 9, 4, NAVY), M.e(cx - 3, fy - 61, 13, 11, NAVY)))  # quiff
    c.put(fig, 7)


def dana(c, cx, fy):
    def fig(L):
        L.rr(cx - 6, fy - 11, 4, 9, 1, SKIN); L.rr(cx + 2, fy - 11, 4, 9, 1, SKIN)
        L.rr(cx - 7, fy - 3, 6, 3, 1, NAVY); L.rr(cx + 1, fy - 3, 6, 3, 1, NAVY)
        L.rr(cx - 12, fy - 54, 24, 31, 9, MUST)                                               # hair behind
        L.put(lambda M: (M.rr(cx - 13, fy - 28, 4, 13, 2, SKIN), M.rr(cx + 9, fy - 28, 4, 13, 2, SKIN)))
        L.put(lambda M: M.p([(cx - 7, fy - 31), (cx + 6, fy - 31), (cx + 13, fy - 9), (cx - 14, fy - 9)], CORAL))
        def face(M):
            M.rr(cx - 8, fy - 47, 16, 18, 5, SKIN)
            M.r(cx - 5, fy - 39, 2, 2, NAVY); M.r(cx + 3, fy - 39, 2, 2, NAVY); M.r(cx - 1, fy - 34, 3, 1, CORAL)
        L.put(face)
        L.put(lambda M: M.rr(cx - 9, fy - 51, 18, 8, 4, MUST))                                # fringe
    c.put(fig, 7)


def visitor(c, cx, fy):
    def fig(L):
        legs(L, cx, fy, NAVY)
        L.put(lambda M: (M.e(cx - 17, fy - 18, 6, 6, SKIN), M.e(cx + 11, fy - 18, 6, 6, SKIN)))
        L.put(lambda M: (M.rr(cx - 17, fy - 30, 8, 15, 3, TEAL), M.rr(cx + 9, fy - 30, 8, 15, 3, TEAL),
                         M.rr(cx - 11, fy - 31, 22, 21, 5, TEAL)))
        def head(M):
            M.rr(cx - 10, fy - 51, 20, 22, 6, SKIN)
            M.r(cx - 5, fy - 41, 2, 2, NAVY); M.r(cx + 3, fy - 41, 2, 2, NAVY); M.r(cx - 2, fy - 35, 4, 1, NAVY)
        L.put(head)
        L.put(lambda M: (M.rr(cx - 11, fy - 54, 22, 10, 5, CORAL), M.p([(cx - 11, fy - 49), (cx + 2, fy - 49),
                                                                        (cx - 11, fy - 41)], CORAL)))
    c.put(fig, 7)


def dog(c, cx, fy):
    def fig(L):
        for x in (cx - 8, cx - 3, cx + 7, cx + 12):
            L.rr(x, fy - 8, 4, 8, 1, MUST)
        L.e(cx + 11, fy - 26, 10, 10, MUST); L.e(cx + 14, fy - 23, 4, 4, CREAM)                 # curled tail
        L.put(lambda M: M.rr(cx - 10, fy - 18, 27, 12, 5, MUST))
        def head(M):
            M.p([(cx - 19, fy - 23), (cx - 17, fy - 31), (cx - 13, fy - 23)], MUST)
            M.p([(cx - 11, fy - 23), (cx - 7, fy - 31), (cx - 5, fy - 23)], MUST)
            M.rr(cx - 20, fy - 26, 16, 14, 5, MUST); M.rr(cx - 23, fy - 19, 9, 7, 3, CREAM)
            M.r(cx - 22, fy - 18, 2, 2, NAVY); M.r(cx - 13, fy - 21, 2, 2, NAVY)
        L.put(head)
    c.put(fig, 4)


if __name__ == '__main__':
    c = Cv(NAVY)
    shell(c); rug(c); window(c); board(c); clock(c); bookshelf(c); plant(c); bin_(c); desk(c); chair(c)
    visitor(c, 80, 160); hero(c, 240, 162); dog(c, 238, 195); dana(c, 281, 186)
    used = {'%02x%02x%02x' % p[:3] for _, p in c.im.getcolors(99999)}
    assert used <= set(PAIRS) | set(PAIRS.values()) and len(used) <= 16, used   # 8 fills + their 8 shadow tones
    out = os.path.join(HERE, 'd10-paper-cutout.png')
    c.im.resize((W * 3, H * 3), Image.NEAREST).save(out)
    assert Image.open(out).size == (1056, 720)
    print('d10-paper-cutout.png written,', len(used), 'colours')
