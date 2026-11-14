# One office corner drawn as illustration, not as pixel-art assets (#65). Asi's own references are not pixel art:
# Arcane, Scavengers Reign, PostHog, Disco Elysium (and Retool's old site art, which I could not find).
# Two families come out of them:
#   LINE  - one line weight, flat colour, no highlights, an odd limited palette (Scavengers Reign, PostHog)
#   PAINT - no line, light and colour do the work, visible brush marks (Arcane, Disco Elysium)
# The same drawing is rendered four ways into illustrated.png: each family smooth at high resolution (left) and
# as pixel art at the game's own scale (right). That is the fork to decide: keep pixels, or leave them.
# Nothing here uses ENDESGA 32: both palettes are made for the picture.
# usage (repo root): python3 -I art-tests/claude-drawn/make_illustrated.py
import math, os, random
from PIL import Image, ImageChops, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
W, H, VIEW = 320, 200, 3          # drawn in game pixels; every panel is shown at 3x

LINE = dict(ink='2a2330', wall='efe6d0', wall2='d9ccab', floor='c9b28a', floor2='a8916a', rug='d9705a', rug2='efe6d0',
            desk='e0a84f', desk2='b9793a', desk3='8f5a2c', mon='33303d', screen='2f7f86', code1='efe6d0', code2='f0562a',
            lamp='f0562a', metal='33303d', mug='efe6d0', mug2='d9705a', pot='6e7fb0', stalk='5e8a68', bulb='e8a0a8',
            frame='cdbf9c', sky='a9cfd0', town='7fa9ad', poster='33303d', p1='f0562a', p2='efe6d0', chair='5e8a68',
            chair2='46705a', shirt='2f7f86', skin='e9b98f', hair='33303d', grey='9a98a3', legs='3e4a63', beard='4a3b3a')
PAINT = dict(ink='15131c', wall='6d7f8a', wall2='56656f', floor='7a6a5c', floor2='5c4e44', rug='a8484f', rug2='d8a070',
             desk='b98952', desk2='7d5636', desk3='4f3524', mon='22222c', screen='59e0d0', code1='e8fff8', code2='ff9a5a',
             lamp='ffb060', metal='2c2c38', mug='d8d0c0', mug2='b04858', pot='8a5a48', stalk='4f8a6a', bulb='e070a0',
             frame='4a4a58', sky='f2a07a', town='5a4a6a', poster='2a2a38', p1='e070a0', p2='59e0d0', chair='3f6a70',
             chair2='2c4c54', shirt='2f9aa0', skin='e2b08a', hair='1c1c24', grey='8a8a98', legs='2c3040', beard='3a2c2c')


def rgb(c):
    return tuple(bytes.fromhex(c))


class Pen:
    """Draws in game pixels onto a canvas S times larger. S == 1 gives pixel art; S > 1 adds a hand wobble."""

    def __init__(self, S, pal, lined):
        self.S, self.pal, self.lined, self.n = S, pal, lined, 0
        self.im = Image.new('RGB', (W * S, H * S), rgb(pal['wall']))
        self.d = ImageDraw.Draw(self.im)
        self.strokes = []           # every outline drawn, so PAINT can put a few back after the brush pass

    def path(self, pts, closed):
        self.n += 1
        rng = random.Random(self.n)
        pts = [(x + rng.uniform(-1, 1), y + rng.uniform(-1, 1)) for x, y in pts]      # wonky shapes, both scales
        if closed:
            pts = pts + pts[:1]
        out = []
        for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
            k = max(1, int(math.hypot(x1 - x0, y1 - y0) / 7)) if self.S > 1 else 1
            for i in range(k):
                w = 0.45 if self.S > 1 and i else 0                                   # wobbly line, smooth only
                out.append((x0 + (x1 - x0) * i / k + rng.uniform(-w, w), y0 + (y1 - y0) * i / k + rng.uniform(-w, w)))
        out.append(pts[-1])
        return [(round(x * self.S), round(y * self.S)) for x, y in out]

    def poly(self, pts, fill, line=True):
        p = self.path(pts, True)
        self.d.polygon(p, fill=rgb(self.pal[fill]))
        if line:
            self.stroke(p)

    def ell(self, cx, cy, rx, ry, fill, line=True):
        self.poly([(cx + rx * math.cos(a * math.pi / 8), cy + ry * math.sin(a * math.pi / 8)) for a in range(16)], fill, line)

    def line(self, pts, col='ink', w=1):
        p = self.path(pts, False)
        self.d.line(p, fill=rgb(self.pal[col]), width=max(1, round(w * self.S)), joint='curve')

    def stroke(self, p):
        self.strokes.append(p)
        if self.lined:
            self.d.line(p, fill=rgb(self.pal['ink']), width=self.S, joint='curve')

    def hatch(self, x, y, n, length=6, col='ink'):   # a few short parallel strokes: the comic-book way to shade
        if self.lined:
            for i in range(n):
                self.line([(x + 3 * i, y), (x + 3 * i - length * 0.6, y + length)], col, 0.6 if self.S > 1 else 1)


def scene(p):
    # wall and floor
    p.poly([(-4, 62), (324, 62), (324, 204), (-4, 204)], 'floor', False)
    p.line([(-4, 62), (324, 62)]); p.poly([(-4, 62), (324, 62), (324, 67), (-4, 67)], 'wall2', False); p.line([(-4, 67), (324, 67)])
    for x, y, n in ((8, 30, 3), (268, 14, 4), (104, 44, 3), (296, 46, 3)):
        p.hatch(x, y, n, col='wall2')
    for x, y, n in ((20, 150, 4), (280, 120, 3), (190, 176, 4), (84, 92, 3)):
        p.hatch(x, y, n, col='floor2')
    # window, with a town outside
    p.poly([(22, 8), (94, 8), (94, 52), (22, 52)], 'frame')
    p.poly([(27, 13), (89, 13), (89, 47), (27, 47)], 'sky')
    for x0, x1, y in ((29, 39, 30), (41, 50, 24), (52, 64, 33), (66, 74, 21), (76, 87, 29)):
        p.poly([(x0, y), (x1, y), (x1, 47), (x0, 47)], 'town', False)
    p.ell(72, 20, 4, 4, 'rug2', False)
    p.line([(58, 13), (58, 47)], w=1.5); p.line([(27, 30), (89, 30)], w=1.5)
    p.poly([(18, 52), (98, 52), (98, 56), (18, 56)], 'frame')
    # poster
    p.poly([(226, 12), (262, 12), (262, 50), (226, 50)], 'poster')
    p.ell(244, 26, 9, 9, 'p1', False); p.poly([(230, 46), (240, 32), (250, 46)], 'p2', False); p.poly([(244, 46), (252, 36), (259, 46)], 'p1', False)
    # rug
    p.poly([(60, 150), (270, 146), (280, 188), (52, 190)], 'rug')
    p.line([(70, 157), (262, 153), (270, 181), (64, 183), (70, 157)], 'rug2', 1.5)
    for i in range(6):
        cx = 88 + 31 * i
        p.poly([(cx, 160), (cx + 8, 168), (cx, 176), (cx - 8, 168)], 'rug2', False)
    # shadows on the floor: flat shapes, one tone
    p.poly([(118, 128), (224, 126), (232, 136), (124, 138)], 'floor2', False)
    p.ell(60, 136, 20, 5, 'floor2', False); p.ell(246, 154, 16, 4, 'floor2', False); p.ell(168, 142, 20, 5, 'floor2', False)
    # plant: a strange one
    for sx, sy, bx, by, r in ((50, 112, 34, 70, 9), (54, 112, 56, 58, 11), (58, 112, 76, 78, 8), (52, 112, 44, 92, 6)):
        p.line([(sx, sy), ((sx + bx) / 2 + 4, (sy + by) / 2), (bx, by)], 'stalk', 2.5)
        p.ell(bx, by, r, r * 0.9, 'bulb'); p.ell(bx - r * 0.3, by - r * 0.3, r * 0.3, r * 0.25, 'rug2', False)
    p.poly([(38, 110), (70, 110), (66, 136), (42, 136)], 'pot'); p.line([(40, 117), (68, 117)])
    # desk
    p.poly([(108, 104), (118, 104), (118, 130), (108, 130)], 'desk2')
    p.poly([(176, 104), (218, 104), (218, 128), (176, 128)], 'desk2')
    p.poly([(118, 104), (176, 104), (176, 112), (118, 112)], 'desk3')
    for y in (108, 118):
        p.poly([(180, y), (214, y), (214, y + 7), (180, y + 7)], 'desk'); p.line([(192, y + 3.5), (202, y + 3.5)], w=1.5)
    p.poly([(110, 68), (214, 68), (220, 98), (104, 98)], 'desk')
    p.poly([(104, 98), (220, 98), (220, 104), (104, 104)], 'desk2')
    p.hatch(112, 74, 3, 5, 'desk2'); p.hatch(160, 90, 4, 5, 'desk2')
    # cable, monitor, mug, lamp
    p.line([(162, 70), (168, 60), (176, 66), (186, 62)], 'metal', 1.2)
    p.poly([(152, 86), (176, 86), (178, 91), (150, 91)], 'mon'); p.poly([(160, 72), (168, 72), (168, 87), (160, 87)], 'mon')
    p.poly([(132, 30), (196, 28), (198, 74), (130, 76)], 'mon'); p.poly([(136, 34), (192, 33), (194, 70), (134, 71)], 'screen')
    for i, (ind, w, col) in enumerate(((0, 18, 'code2'), (4, 26, 'code1'), (4, 14, 'code1'), (8, 22, 'code2'), (4, 30, 'code1'), (0, 10, 'code1'))):
        p.line([(140 + ind, 40 + 5 * i), (140 + ind + w, 40 + 5 * i)], col, 1.6)
    p.poly([(118, 78), (130, 78), (129, 92), (119, 92)], 'mug'); p.poly([(118, 83), (130, 83), (130, 87), (118, 87)], 'mug2', False)
    p.line([(130, 81), (135, 82), (135, 88), (130, 89)], w=1.4)
    p.line([(121, 74), (123, 70), (120, 66), (123, 62)], 'mug', 1.2); p.line([(127, 74), (129, 69), (126, 65)], 'mug', 1.2)
    p.poly([(196, 90), (212, 90), (214, 95), (194, 95)], 'metal'); p.line([(204, 90), (204, 70)], 'metal', 2)
    p.poly([(194, 50), (214, 50), (222, 70), (186, 70)], 'lamp')
    # chair, seen from behind
    p.line([(160, 138), (160, 146)], 'metal', 2); p.line([(176, 138), (176, 146)], 'metal', 2); p.line([(152, 146), (184, 146)], 'metal', 2)
    p.poly([(150, 110), (186, 110), (188, 138), (148, 138)], 'chair'); p.poly([(150, 131), (188, 131), (188, 138), (148, 138)], 'chair2', False)
    p.line([(148, 138), (188, 138)]); p.hatch(156, 116, 3, 6, 'chair2')
    # the hero
    hx = 246
    for dx in (-7, 1):
        p.poly([(hx + dx, 132), (hx + dx + 6, 132), (hx + dx + 6, 150), (hx + dx, 150)], 'legs')
        p.poly([(hx + dx - 2, 148), (hx + dx + 7, 148), (hx + dx + 7, 153), (hx + dx - 2, 153)], 'hair')
    for s in (-1, 1):
        p.poly([(hx + s * 11, 122), (hx + s * 18, 123), (hx + s * 18, 136), (hx + s * 12, 136)], 'skin')
        p.poly([(hx + s * 10, 112), (hx + s * 18, 114), (hx + s * 19, 124), (hx + s * 11, 123)], 'shirt')
    p.poly([(hx - 11, 112), (hx + 11, 112), (hx + 13, 134), (hx - 13, 134)], 'shirt')
    p.ell(hx - 13, 99, 3, 4, 'skin'); p.ell(hx + 13, 99, 3, 4, 'skin')
    p.ell(hx, 98, 12, 11.5, 'skin')
    p.poly([(hx - 10, 103), (hx + 10, 103), (hx + 8, 110), (hx, 113), (hx - 8, 110)], 'beard')
    p.line([(hx - 3, 106), (hx + 3, 106)], 'skin', 1.4)
    for s in (-1, 1):
        p.poly([(hx + s * 12, 97), (hx + s * 10, 88), (hx + s * 6, 89), (hx + s * 9, 97)], 'grey', False)
    p.poly([(hx - 9, 91), (hx - 6, 82), (hx, 77), (hx + 6, 82), (hx + 9, 91), (hx + 5, 88), (hx, 87), (hx - 5, 88)], 'hair')
    for s in (-1, 1):
        cx = hx + s * 5.5
        p.line([(cx - 3.5, 95), (cx + 3.5, 95), (cx + 3.5, 100.5), (cx - 3.5, 100.5), (cx - 3.5, 95)], w=1)
        p.ell(cx, 98, 1, 1, 'hair', False)
    p.line([(hx - 2, 97), (hx + 2, 97)], w=1)
    return p


def lightmap(S):
    """PAINT: a cool dark room, a warm lamp, a teal screen, pink dusk through the window. Stored at half strength."""
    m = Image.new('RGB', (W, H)); px = m.load()
    for y in range(H):
        for x in range(W):
            lamp = max(0, 1 - math.hypot(x - 204, (y - 78) * 1.3) / 95) ** 2
            scr = max(0, 1 - math.hypot(x - 164, (y - 62) * 1.2) / 70) ** 2
            win = max(0, 1 - abs((x - 58) - (y - 30) * 0.55) / 44) * max(0, 1 - abs(y - 70) / 90)
            r = 0.56 + 1.05 * lamp + 0.08 * scr + 0.55 * win
            g = 0.60 + 0.62 * lamp + 0.42 * scr + 0.22 * win
            b = 0.80 + 0.25 * lamp + 0.42 * scr + 0.34 * win
            px[x, y] = tuple(min(255, int(v * 127)) for v in (r, g, b))
    return m.resize((W * S, H * S), Image.BICUBIC)


def painted(S):
    p = scene(Pen(S, PAINT, False))
    lit = ImageChops.multiply(p.im, lightmap(S)).point(lambda v: min(255, v * 2))
    for box in ((134, 33, 195, 72), (27, 13, 90, 48)):                        # the screen and the sky give light
        box = tuple(v * S for v in box); lit.paste(p.im.crop(box), box)
    out = lit.copy(); d = ImageDraw.Draw(out); src = lit.load(); rng = random.Random(3)
    def at(x, y):
        return src[min(W * S - 1, max(0, int(x * S))), min(H * S - 1, max(0, int(y * S)))]
    for _ in range(W * H // 3):                                                # brush marks, kept inside a shape
        x, y = rng.uniform(0, W - 1), rng.uniform(0, H - 1)
        a = math.radians(-25 + rng.uniform(-40, 40))
        ln, wd = rng.uniform(1.5, 4), rng.uniform(0.7, 1.4)
        ux, uy, vx, vy = math.cos(a) * ln, math.sin(a) * ln, -math.sin(a) * wd, math.cos(a) * wd
        c = at(x, y)
        if any(sum(abs(i - j) for i, j in zip(c, at(x + e * ux, y + e * uy))) > 40 for e in (-1.2, 1.2)):
            continue                                                           # would smear across an edge
        k = rng.uniform(0.86, 1.14)
        d.polygon([((x + sx * ux + sy * vx) * S, (y + sx * uy + sy * vy) * S) for sx, sy in ((-1, -1), (1, -1), (1, 1), (-1, 1))],
                  fill=tuple(min(255, int(v * k)) for v in c))
    for s in p.strokes:                                                        # a few broken dark lines back on top
        for a, b in zip(s, s[1:]):
            if rng.random() < 0.3:
                d.line([a, b], fill=rgb(PAINT['ink']), width=S)
    return out


def smooth(make):          # draw large, shrink: an anti-aliased picture
    return make(VIEW * 2).resize((W * VIEW, H * VIEW), Image.LANCZOS)


def pixels(make, colours=None):
    im = make(1)
    if colours:
        im = im.quantize(colours, method=Image.MEDIANCUT, dither=Image.NONE).convert('RGB')
    return im.resize((W * VIEW, H * VIEW), Image.NEAREST), len(im.getcolors(99999))


if __name__ == '__main__':
    lined = lambda S: scene(Pen(S, LINE, True)).im
    a_px, a_n = pixels(lined)
    b_px, b_n = pixels(painted, 32)
    panels = [smooth(lined), a_px, smooth(painted), b_px]
    sheet = Image.new('RGB', (W * VIEW * 2 + 6, H * VIEW * 2 + 6), rgb('15131c'))
    for i, im in enumerate(panels):
        sheet.paste(im, ((i % 2) * (W * VIEW + 6), (i // 2) * (H * VIEW + 6)))
    sheet.save(os.path.join(HERE, 'illustrated.png'))
    assert a_n <= 40 and b_n <= 32, (a_n, b_n)        # the pixel versions stay small-palette
    print('illustrated.png written; pixel panels use', a_n, 'and', b_n, 'colours')
