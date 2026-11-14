# Direction 2, "Naive flat cartoon": the office corner as a still (reports/Pixel art style directions.md, section 2).
# Rules followed: 19 bright flat colours, one fill per material, no ramps, no shading, no highlights, no
# texture; one shadow tone, used only for cast shadows on the floor; a dark line round everything, 1 px inside
# and 2 px on a character's outer silhouette; shapes drawn slightly off (every long edge is nudged by a seeded
# wobble); props are icons; faces are dot eyes and a one-line mouth; heads take half the figure; the room
# floats on flat black with no outer walls; the monitor shows a doodle of code; one odd prop is the joke
# (the rubber duck has the chair).
# usage (repo root): python3 -I art-tests/claude-drawn/directions/make_d02_naive_flat.py
import math
import os
import random
from PIL import Image, ImageChops, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 352, 240
INK, FLOOR, SHADOW, WALL, WOOD, WOOD2, WHITE = '1a1423', 'c6c8d6', '8d90aa', 'f4e3b0', 'd89c56', 'a9683a', 'fff8ea'
RED, YELLOW, ORANGE, GREEN, TEAL, BLUE, NAVY = 'e8504a', 'f8d048', 'f28c3a', '5dbb63', '2bb0a8', '62aaf4', '3f4c8c'
GREY, SKIN, PINK, PURPLE, HAIR = '9aa0ad', 'f6c9a0', 'f48fb1', '9b6fd0', '3a3344'
PALETTE = {INK, FLOOR, SHADOW, WALL, WOOD, WOOD2, WHITE, RED, YELLOW, ORANGE, GREEN, TEAL, BLUE, NAVY, GREY, SKIN,
           PINK, PURPLE, HAIR}
R = random.Random(11)


def rgb(c):
    return tuple(bytes.fromhex(c)) + (255,)


def wob(pts, step=10):
    """The hand: every edge bows 1 px off the straight line and back, as a slow wave with its own phase."""
    out, n = [], len(pts)
    for i in range(n):
        (x0, y0), (x1, y1) = pts[i], pts[(i + 1) % n]
        d = math.hypot(x1 - x0, y1 - y0) or 1
        k, ph, fr = max(1, round(d / step)), R.uniform(0, 6.3), R.uniform(.5, .9)
        for j in range(k):
            t, o = j / k, round(1.2 * math.sin(ph + j * fr)) if j else 0
            out.append((round(x0 + (x1 - x0) * t - (y1 - y0) / d * o), round(y0 + (y1 - y0) * t + (x1 - x0) / d * o)))
    return out


def blob(cx, cy, rx, ry, p=2.0, n=18, j=.04):
    """A round shape drawn by hand: a superellipse (p=2 oval, higher = squarer) whose radius wanders a little."""
    pts = []
    for i in range(n):
        a = 2 * math.pi * i / n
        co, si, k = math.cos(a), math.sin(a), 1 + R.uniform(-j, j)
        pts.append((round(cx + rx * k * math.copysign(abs(co) ** (2 / p), co)),
                    round(cy + ry * k * math.copysign(abs(si) ** (2 / p), si))))
    return pts


class Cv:
    def __init__(self, fill=None):
        self.im = Image.new('RGBA', (W, H), rgb(fill) if fill else (0, 0, 0, 0))
        self.d = ImageDraw.Draw(self.im)

    def r(self, x, y, w, h, c):
        self.d.rectangle((x, y, x + w - 1, y + h - 1), fill=rgb(c))

    def e(self, x, y, w, h, c):
        self.d.ellipse((x, y, x + w - 1, y + h - 1), fill=rgb(c))

    def p(self, pts, c):
        self.d.polygon(pts, fill=rgb(c))

    def w(self, pts, c, step=10):
        self.p(wob(pts, step), c)

    def ln(self, pts, c=INK):
        self.d.line(pts, fill=rgb(c))

    def erase(self, x, y, w, h):
        self.im.paste((0, 0, 0, 0), (x, y, x + w, y + h))

    def part(self, fn, corners=False):
        """One drawn thing: its fill on a layer of its own, a 1 px dark line round it, laid over what is here."""
        L = Cv(); fn(L)
        a = L.im.getchannel('A'); solid = a
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)) + (((1, 1), (-1, 1), (1, -1), (-1, -1)) if corners else ()):
            s = Image.new('L', a.size); s.paste(a, (dx, dy)); solid = ImageChops.lighter(solid, s)
        out = Image.new('RGBA', a.size, (0, 0, 0, 0)); out.paste(rgb(INK), mask=solid); out.alpha_composite(L.im)
        self.im.alpha_composite(out)
        self.d = ImageDraw.Draw(self.im)


def fig(c, fn):
    """A character: parts carry the 1 px line, then the whole figure gets one more, so its silhouette is 2 px."""
    c.part(lambda L: L.part(fn), corners=True)


# --- room: a floor and one inside wall, on black ----------------------------------------------------------------
def shell(c):
    c.w([(17, 62), (335, 61), (337, 225), (193, 226), (194, 240), (159, 240), (160, 225), (16, 224)], FLOOR, 40)
    c.part(lambda L: L.w([(18, 9), (334, 7), (336, 60), (16, 61)], WALL, 40))
    c.part(lambda L: L.w([(16, 61), (336, 60), (336, 66), (16, 67)], WOOD2, 60))


def rug(c):
    for y in range(168, 204, 5):
        c.part(lambda L: (L.r(46, y, 6, 2, WHITE), L.r(299, y - 1, 6, 2, WHITE)))
    c.part(lambda L: L.w([(52, 165), (299, 163), (301, 205), (51, 206)], RED, 30))
    c.ln(wob([(57, 170), (294, 168), (296, 200), (56, 201)], 30) + [(57, 170)])
    for cx in range(88, 270, 44):
        c.part(lambda L: L.w([(cx - 10, 185), (cx, 175), (cx + 10, 184), (cx + 1, 195)], YELLOW, 7))
    c.part(lambda L: L.w([(162, 210), (190, 209), (191, 220), (162, 221)], GREEN, 14))


def window(c):
    c.part(lambda L: L.w([(52, 14), (120, 13), (121, 52), (51, 53)], WHITE, 30))
    for x in (56, 89):
        c.part(lambda L: L.w([(x, 18), (x + 28, 17), (x + 28, 48), (x, 49)], BLUE, 30))
    c.part(lambda L: (L.e(59, 25, 9, 7, WHITE), L.e(64, 22, 11, 10, WHITE), L.e(71, 26, 9, 6, WHITE)))   # cloud
    c.part(lambda L: L.p(blob(108, 27, 5, 5), YELLOW))                                                    # sun
    c.part(lambda L: L.w([(48, 52), (124, 51), (125, 56), (47, 57)], WHITE, 30))
    c.part(lambda L: (L.e(95, 36, 7, 15, GREEN), L.e(100, 41, 6, 5, GREEN), L.r(103, 38, 3, 6, GREEN)))   # cactus
    c.part(lambda L: L.w([(93, 46), (104, 46), (103, 52), (94, 52)], ORANGE, 20))


def board(c):
    c.part(lambda L: L.w([(144, 13), (188, 12), (189, 38), (143, 37)], WOOD, 25))
    c.part(lambda L: L.p([(148, 17), (157, 16), (158, 27), (149, 28)], WHITE))
    c.ln([(151, 20), (155, 20)], GREY); c.ln([(151, 23), (154, 23)], GREY)
    c.part(lambda L: L.p([(161, 16), (169, 15), (170, 23), (162, 24)], YELLOW))
    c.part(lambda L: L.p([(159, 28), (167, 27), (168, 34), (160, 35)], PINK))
    c.part(lambda L: (L.p([(173, 17), (185, 18), (184, 30), (172, 29)], WHITE)))
    c.r(175, 20, 8, 4, BLUE); c.r(175, 24, 8, 3, GREEN)
    for x, y in ((152, 16), (165, 15), (178, 17)):
        c.r(x, y, 2, 2, RED)


def clock(c):
    c.part(lambda L: L.p(blob(222, 27, 11, 11), RED))
    c.part(lambda L: L.p(blob(222, 27, 7, 7), WHITE))
    c.ln([(222, 27), (221, 22)]); c.ln([(222, 27), (226, 29)])


def bookshelf(c):
    c.r(268, 90, 64, 5, SHADOW)
    c.part(lambda L: L.w([(265, 12), (325, 11), (327, 90), (264, 91)], WOOD, 30))
    for s in range(3):
        c.part(lambda L: L.w([(269, 17 + 24 * s), (321, 16 + 24 * s), (322, 35 + 24 * s), (269, 36 + 24 * s)], WOOD2, 30))
    def stand(x, base, books):
        for w, h, col in books:
            c.part(lambda L: L.r(x, base - h, w, h, col)); x += w + 1
    stand(271, 36, ((5, 14, TEAL), (4, 11, RED), (5, 15, YELLOW), (4, 12, WHITE), (5, 14, PURPLE)))
    c.part(lambda L: (L.p([(304, 21), (315, 21), (312, 29), (307, 29)], YELLOW), L.r(308, 29, 3, 4, YELLOW),
                      L.r(305, 33, 9, 3, YELLOW)))                                                  # trophy
    stand(271, 60, ((4, 12, RED), (6, 15, BLUE), (4, 11, GREEN), (5, 14, ORANGE)))
    c.part(lambda L: L.p([(294, 60), (299, 45), (304, 46), (299, 60)], PINK))                        # one leans
    stand(306, 60, ((5, 13, WHITE), (5, 15, TEAL)))
    for i, col in enumerate((BLUE, RED, YELLOW)):
        c.part(lambda L: L.r(271 + i, 80 - 4 * i, 16 - 2 * i, 4, col))
    stand(293, 84, ((5, 13, GREEN), (4, 15, WHITE), (5, 12, PURPLE), (5, 14, ORANGE)))


def plant(c):
    c.e(20, 102, 36, 10, SHADOW)
    bx, by = 35, 87
    w = 7
    for tx, ty in ((10, 66), (60, 68), (17, 47), (54, 50), (35, 38)):
        dx, dy = tx - bx, ty - by
        ln = math.hypot(dx, dy); nx, ny = -dy / ln * w, dx / ln * w
        at = lambda t, s: (round(bx + dx * t + nx * s), round(by + dy * t + ny * s))
        c.part(lambda L: L.p([at(.15, 0), at(.4, .8), at(.75, 1), at(1, 0), at(.75, -1), at(.4, -.8)], GREEN))
        c.ln([at(.3, 0), at(.85, 0)])
    c.part(lambda L: L.w([(23, 88), (48, 87), (45, 108), (26, 108)], ORANGE, 12))
    c.part(lambda L: L.w([(20, 84), (50, 83), (50, 89), (20, 90)], ORANGE, 30))


def bin_(c):
    c.e(241, 89, 22, 8, SHADOW)
    c.part(lambda L: L.p(blob(249, 71, 4, 3), WHITE)); c.part(lambda L: L.p(blob(254, 69, 4, 4), WHITE))
    c.part(lambda L: L.w([(242, 74), (259, 73), (257, 94), (244, 95)], GREY, 10))
    for x in (247, 251, 255):
        c.ln([(x, 77), (x, 91)])
    c.part(lambda L: L.p(blob(266, 92, 3, 3), WHITE))


def desk(c):
    c.p([(140, 119), (236, 119), (240, 125), (146, 125)], SHADOW); c.r(145, 101, 52, 20, SHADOW)
    c.part(lambda L: L.w([(136, 92), (232, 92), (233, 120), (196, 121), (196, 101), (144, 101), (144, 121), (136, 121)],
                         WOOD, 16))
    for y in (99, 109):
        c.ln([(200, y), (228, y), (228, y + 7), (200, y + 7), (200, y)]); c.r(213, y + 3, 3, 2, INK)
    c.part(lambda L: L.w([(134, 68), (234, 67), (235, 94), (133, 95)], WOOD, 16))
    c.part(lambda L: L.p([(139, 72), (149, 71), (150, 84), (140, 85)], WHITE))                       # paper
    for i, w in enumerate((6, 4, 6)):
        c.ln([(142, 75 + 3 * i), (142 + w, 75 + 3 * i)], GREY)
    c.ln([(162, 79), (165, 80), (165, 84), (162, 85)])                                               # mug handle
    c.part(lambda L: L.w([(153, 76), (161, 76), (161, 87), (154, 87)], PINK, 20)); c.r(155, 77, 5, 2, WOOD2)
    c.part(lambda L: (L.r(181, 70, 6, 6, GREY), L.w([(173, 76), (195, 75), (196, 80), (172, 80)], GREY, 20)))
    c.part(lambda L: L.w([(160, 38), (207, 36), (208, 69), (159, 70)], GREY, 20))                    # monitor
    c.part(lambda L: L.w([(164, 42), (203, 40), (204, 65), (164, 66)], NAVY, 20))
    for x, y, n, col in ((167, 45, 9, PINK), (178, 45, 13, WHITE), (170, 49, 16, GREEN), (170, 53, 7, YELLOW),
                         (179, 53, 9, WHITE), (173, 57, 12, GREEN), (167, 61, 6, PINK)):             # a doodle of code
        for i in range(n):
            c.r(x + i, y + (i % 4 == 1) - (i % 4 == 3), 1, 1, col)
    c.r(194, 57, 1, 2, YELLOW); c.r(198, 57, 1, 2, YELLOW); c.ln([(193, 61), (195, 63), (197, 63), (199, 61)], YELLOW)
    c.part(lambda L: L.w([(164, 82), (200, 81), (201, 91), (164, 92)], WHITE, 18))                   # keyboard
    for y in (84, 86, 88):
        for x in range(166, 199, 3):
            c.r(x, y, 2, 1, GREY)
    c.part(lambda L: L.e(205, 83, 6, 8, WHITE)); c.r(207, 83, 1, 3, INK)
    c.part(lambda L: (L.e(212, 84, 15, 6, GREY), L.r(219, 68, 2, 17, GREY)))                         # lamp
    c.part(lambda L: L.w([(213, 55), (226, 54), (232, 69), (207, 70)], YELLOW, 10))


def chair(c):
    c.e(153, 151, 38, 10, SHADOW)
    c.part(lambda L: (L.r(170, 146, 4, 9, GREY), L.w([(158, 154), (186, 154), (186, 157), (158, 157)], GREY, 30)))
    for x in (157, 170, 183):
        c.e(x, 156, 5, 5, INK)
    c.part(lambda L: L.e(157, 113, 30, 13, PURPLE))                                                  # seat
    c.part(lambda L: L.p([(181, 108), (188, 102), (187, 112)], YELLOW))                              # the duck: tail,
    c.part(lambda L: L.p(blob(173, 113, 12, 9, 2.4), YELLOW))                                        # body,
    c.part(lambda L: L.p([(154, 101), (163, 96), (164, 104)], ORANGE))                               # beak,
    c.part(lambda L: L.p(blob(169, 100, 7, 7), YELLOW)); c.r(165, 98, 2, 2, INK)                     # head
    c.ln([(172, 112), (176, 115), (181, 112)])                                                       # wing
    c.part(lambda L: L.p(blob(172, 134, 15, 13, 4, 22, .02), PURPLE))                                # chair back


# --- cast: (cx, fy) is the middle of the feet; about two heads tall ---------------------------------------------
def body(L, cx, fy, top, legs, shoes, long_sleeves):
    L.part(lambda M: (M.e(cx - 9, fy - 4, 9, 5, shoes), M.e(cx, fy - 4, 9, 5, shoes)))
    L.part(lambda M: M.r(cx - 6, fy - 11, 12, 8, legs)); L.r(cx, fy - 8, 1, 5, INK)
    for sx in (cx - 14, cx + 8):
        L.part(lambda M: M.e(sx, fy - 22, 6, 12, top if long_sleeves else SKIN))
        L.part(lambda M: M.e(sx, fy - 23, 6, 6, top) if not long_sleeves else M.e(sx, fy - 13, 5, 5, SKIN))
    L.part(lambda M: M.w([(cx - 8, fy - 23), (cx + 8, fy - 23), (cx + 9, fy - 10), (cx - 9, fy - 10)], top, 7))


def head(L, cx, fy):
    hp = blob(cx, fy - 33, 12, 11, 2.7, 22, .025)
    L.part(lambda M: (M.e(cx - 15, fy - 36, 5, 6, SKIN), M.e(cx + 10, fy - 36, 5, 6, SKIN)))         # ears
    L.part(lambda M: M.p(hp, SKIN))
    return hp


def face(L, cx, fy):
    L.r(cx - 6, fy - 35, 2, 3, INK); L.r(cx + 4, fy - 35, 2, 3, INK)
    L.r(cx - 2, fy - 28, 4, 1, INK); L.r(cx - 3, fy - 29, 1, 1, INK); L.r(cx + 2, fy - 29, 1, 1, INK)


def hero(c, cx, fy):
    def draw(L):
        body(L, cx, fy, TEAL, HAIR, WHITE, False)
        hp = head(L, cx, fy)
        L.part(lambda M: (M.p(hp, GREY), M.erase(cx - 14, fy - 36, 30, 20)))                         # grey sides
        L.part(lambda M: (M.p(hp, HAIR), M.erase(cx - 14, fy - 46, 30, 17), M.r(cx - 12, fy - 33, 2, 5, HAIR),
                          M.r(cx + 10, fy - 33, 2, 5, HAIR)))                                        # beard
        L.r(cx - 2, fy - 26, 4, 1, PINK)
        L.part(lambda M: (M.e(cx - 9, fy - 38, 8, 8, WHITE), M.e(cx + 1, fy - 38, 8, 8, WHITE)))     # glasses
        L.r(cx - 6, fy - 35, 2, 2, INK); L.r(cx + 4, fy - 35, 2, 2, INK)
        L.part(lambda M: M.p([(cx - 5, fy - 40), (cx - 6, fy - 46), (cx - 3, fy - 51), (cx + 3, fy - 53), (cx + 8, fy - 49),
                              (cx + 5, fy - 46), (cx + 5, fy - 40)], HAIR))                       # quiff
    c.e(cx - 13, fy - 4, 28, 8, SHADOW); fig(c, draw)


def visitor(c, cx, fy):
    def draw(L):
        body(L, cx, fy, GREEN, NAVY, HAIR, True)
        hp = head(L, cx, fy)
        L.part(lambda M: (M.p(hp, ORANGE), M.erase(cx - 14, fy - 39, 30, 20),
                          M.p([(cx - 3, fy - 43), (cx + 2, fy - 49), (cx + 5, fy - 43)], ORANGE)))    # hair and a tuft
        face(L, cx, fy)
    c.e(cx - 13, fy - 4, 28, 8, SHADOW); fig(c, draw)


def dana(c, cx, fy):
    def draw(L):
        L.part(lambda M: (M.e(cx - 7, fy - 3, 7, 4, RED), M.e(cx, fy - 3, 7, 4, RED)))
        L.part(lambda M: (M.r(cx - 5, fy - 8, 4, 6, SKIN), M.r(cx + 1, fy - 8, 4, 6, SKIN)))
        L.part(lambda M: M.p(blob(cx, fy - 30, 14, 14, 2.6, 22, .02), YELLOW))                        # hair behind
        L.part(lambda M: (M.e(cx - 12, fy - 22, 5, 12, SKIN), M.e(cx + 7, fy - 22, 5, 12, SKIN)))
        L.part(lambda M: M.w([(cx - 6, fy - 23), (cx + 6, fy - 23), (cx + 11, fy - 7), (cx - 11, fy - 7)], RED, 8))
        hp = blob(cx, fy - 33, 11, 10, 2.7, 22, .02)
        L.part(lambda M: M.p(hp, SKIN))
        L.part(lambda M: (M.p(hp, YELLOW), M.erase(cx - 14, fy - 38, 30, 20), M.r(cx - 11, fy - 38, 3, 7, YELLOW),
                          M.r(cx + 9, fy - 38, 3, 7, YELLOW)))                                       # fringe
        face(L, cx, fy)
    c.e(cx - 13, fy - 4, 28, 8, SHADOW); fig(c, draw)


def dog(c, cx, fy):
    def draw(L):
        L.part(lambda M: M.e(cx + 9, fy - 22, 9, 9, ORANGE)); L.r(cx + 13, fy - 18, 2, 2, INK)       # curled tail
        for x in (cx - 4, cx + 5, cx - 9, cx + 10):
            L.part(lambda M: M.r(x, fy - 6, 4, 6, ORANGE))
        L.part(lambda M: M.p(blob(cx + 2, fy - 11, 13, 6, 3), ORANGE))
        L.part(lambda M: (M.p([(cx - 18, fy - 21), (cx - 17, fy - 28), (cx - 12, fy - 22)], ORANGE),
                          M.p([(cx - 10, fy - 22), (cx - 6, fy - 28), (cx - 5, fy - 20)], ORANGE)))
        L.part(lambda M: M.r(cx - 18, fy - 11, 3, 4, PINK))                                          # tongue
        L.part(lambda M: M.p(blob(cx - 11, fy - 17, 8, 7, 2.6), ORANGE))
        L.part(lambda M: M.e(cx - 23, fy - 18, 10, 7, WHITE))
        L.r(cx - 23, fy - 17, 2, 2, INK); L.r(cx - 13, fy - 21, 2, 2, INK)
    c.e(cx - 16, fy - 4, 34, 8, SHADOW); fig(c, draw)


if __name__ == '__main__':
    c = Cv(INK)
    shell(c); rug(c); window(c); board(c); clock(c); bookshelf(c); plant(c); bin_(c); desk(c); chair(c)
    visitor(c, 80, 160); hero(c, 246, 160); dog(c, 232, 197); dana(c, 280, 188)
    used = {'%02x%02x%02x' % p[:3] for _, p in c.im.getcolors(99999)}
    assert used <= PALETTE and 16 <= len(used) <= 24, used - PALETTE      # the sheet: 16 to 24 flat colours
    out = os.path.join(HERE, 'd02-naive-flat.png')
    c.im.resize((W * 3, H * 3), Image.NEAREST).save(out)
    assert Image.open(out).size == (1056, 720)
    print('d02-naive-flat.png written,', len(used), 'colours')
