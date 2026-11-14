# Direction 9, portrait-led PC-98: a plain world and one large dithered portrait in an ornate frame.
# (rule sheet: reports/Pixel art style directions.md, "### 9. Portrait-led PC-98")
#   palette   chosen first, 16 colours for the whole screen as on a PC-98: one low-saturation plum-to-bone family,
#             three slate violets, and one neon teal (with its two darker steps) that is also the rim light.
#   world     make_room.py's room and the cast sheets folded down to flat two-tone sprites; neon only on the
#             screen and on the hero's shirt.
#   portrait  the hero's bust, about 140 px tall, drawn here from shapes: each material is a light value pushed through
#             a short ramp with a 4 x 4 ordered dither, then hard pixel features, a dark line and a neon rim.
#   frame     ornate and part of the art: double line, dithered band, corner studs, name plate, command menu.
# Native size is 528 x 360 at 2x (not 352 x 240 at 3x): the sheet sizes the bust against the game's 640 x 360
# canvas, and a PC-98 screen is fine-grained. Every pixel in the still is the same size. No scanline layer: the
# sheet makes it an optional CSS overlay.
# usage (repo root): python3 -I art-tests/claude-drawn/directions/make_d09_portrait_pc98.py
import colorsys, math, os, sys
from PIL import Image, ImageChops, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
import make_room as m

W, H = 528, 360
C0, C1, C2, C3, C4 = '100c18', '231a2e', '3a2a41', '573b4f', '7a505a'   # the family, dark half
C5, C6, C7, C8, C9 = 'a06a62', 'c48d74', 'e2b594', 'f3dcc0', 'fdf6e6'   # light half: skin, wood, bone
V1, V2, V3 = '4a4a66', '74748f', 'a3a2b5'                               # slate violets: walls, metal, grey hair
NEON, TEAL, DTEAL = '19f0d8', '0e9aa0', '0b5566'                        # the one accent and its two darker steps
PAL = [C0, C1, C2, C3, C4, C5, C6, C7, C8, C9, V1, V2, V3, NEON, TEAL, DTEAL]
BAYER = [[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]


def rgb(c):
    return tuple(bytes.fromhex(c)) + (255,)


def dith(x, y, v, ramp, sharp=2.0):
    """A light value 0..1 -> one ramp colour, ordered dither between neighbours. sharp > 1 narrows the dithered
    band so most of a tone stays flat."""
    p = min(max(v, 0.0), 0.999) * (len(ramp) - 1)
    i = int(p)
    f = min(max((p - i - 0.5) * sharp + 0.5, 0.0), 1.0)
    return ramp[i + (f > (BAYER[y % 4][x % 4] + 0.5) / 16)]


def r(im, x, y, w, h, c):
    im.paste(rgb(c), (x, y, x + w, y + h))


FONT = {  # 5 x 7, drawn here
    'A': '.###./#...#/#...#/#####/#...#/#...#/#...#', 'B': '####./#...#/#...#/####./#...#/#...#/####.',
    'C': '.###./#...#/#..../#..../#..../#...#/.###.', 'D': '####./#...#/#...#/#...#/#...#/#...#/####.',
    'E': '#####/#..../#..../####./#..../#..../#####', 'F': '#####/#..../#..../####./#..../#..../#....',
    'G': '.###./#...#/#..../#.###/#...#/#...#/.###.', 'H': '#...#/#...#/#...#/#####/#...#/#...#/#...#',
    'I': '###/.#./.#./.#./.#./.#./###', 'K': '#...#/#..#./#.#../##.../#.#../#..#./#...#',
    'L': '#..../#..../#..../#..../#..../#..../#####', 'M': '#...#/##.##/#.#.#/#.#.#/#...#/#...#/#...#',
    'N': '#...#/##..#/#.#.#/#..##/#...#/#...#/#...#', 'O': '.###./#...#/#...#/#...#/#...#/#...#/.###.',
    'R': '####./#...#/#...#/####./#.#../#..#./#...#', 'S': '.####/#..../#..../.###./....#/....#/####.',
    'T': '#####/..#../..#../..#../..#../..#../..#..', 'U': '#...#/#...#/#...#/#...#/#...#/#...#/.###.',
    'V': '#...#/#...#/#...#/#...#/#...#/.#.#./..#..', 'W': '#...#/#...#/#...#/#.#.#/#.#.#/##.##/#...#',
    'Y': '#...#/#...#/.#.#./..#../..#../..#../..#..', '.': '././././././#', ',': '../../../../../.#/#.',
    ' ': '../../../../../../..'}


def width(s):
    return sum(len(FONT[ch].split('/')[0]) + 1 for ch in s) - 1


def text(im, x, y, s, c, shadow=C0):
    for ch in s:
        rows = FONT[ch].split('/')
        for j, row in enumerate(rows):
            for i, bit in enumerate(row):
                if bit == '#':
                    if shadow:
                        im.putpixel((x + i + 1, y + j + 1), rgb(shadow))
                    im.putpixel((x + i, y + j), rgb(c))
        x += len(rows[0]) + 1


# --- world tier: flat two-tone ------------------------------------------------------------------------------------
# ENDESGA 32 -> the 16. Every material keeps a base and one shade; highlights, grain and weave fold into the base.
ROOM = {'181425': C0, '262b44': C1, '3a4466': V1, '5a6988': V1, '8b9bb4': V2, 'c0cbdc': V3, 'ffffff': C8,
        'ead4aa': C6, 'e4a672': C6, 'c28569': C6, 'd77643': C5, 'b86f50': C5, '733e39': C4, '3e2731': C2,
        'e43b44': C5, 'a22633': C4, 'f6757a': C5, 'b55088': C5, '68386c': C3, 'feae34': C7, 'fee761': C7,
        'f77622': C6, 'be4a2f': C4, '63c74d': TEAL, '3e8948': TEAL, '265c42': DTEAL, '193c3e': DTEAL,
        '0099db': V1, '2ce8f5': V2, '124e89': C1}
CAST = {**ROOM, 'e8b796': C7, 'c28569': C6, '0099db': NEON, '2ce8f5': NEON, '124e89': TEAL, '8b9bb4': V3,
        '5a6988': V2, 'ffffff': C9, 'd77643': C6, 'be4a2f': C5, 'ead4aa': C8, 'f77622': C6,
        '63c74d': V2, '3e8948': V2, '265c42': V1, '193c3e': C1, 'fee761': C8}
SHADOW = {rgb(C3): rgb(C2), rgb(V2): rgb(V1), rgb(V1): rgb(C2), rgb(C2): rgb(C1), rgb(V3): rgb(V2), rgb(C8): rgb(V3)}


class Flat(m.Canvas):
    """make_room's canvas on a clear ground. Cast shadows are only collected, so they can be laid flat on the
    shell later and never shade another prop."""
    shadow = None

    def prop(self, fn, *a, cast=(2, 2)):
        layer = m.Canvas(*self.im.size)
        fn(layer, *a)
        alpha = layer.im.getchannel('A')
        solid = alpha
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            s = Image.new('L', alpha.size); s.paste(alpha, (dx, dy)); solid = ImageChops.lighter(solid, s)
        if cast:
            sh = Image.new('L', alpha.size); sh.paste(solid, cast)
            Flat.shadow = ImageChops.lighter(Flat.shadow, sh)
        self.im.paste(m.rgb(m.INK), mask=ImageChops.subtract(solid, alpha))
        self.im.alpha_composite(layer.im)


def remap(im, table):
    px = im.load()
    for y in range(im.height):
        for x in range(im.width):
            if px[x, y][3]:
                px[x, y] = rgb(table['%02x%02x%02x' % px[x, y][:3]])
    return im


PEOPLE = [('visitor.png', 2, 0, 60, 100), ('hero-detailed.png', 0, 0, 226, 98), ('dog.png', 1, 0, 196, 136),
          ('dana.png', 0, 0, 262, 124)]


def room():
    im = Image.new('RGBA', (352, 240), rgb(C1))
    r(im, 16, 8, 320, 216, C3); r(im, 160, 224, 32, 16, C3)                # floor
    for ty in range(80, 224, 16):                                          # one dot where tiles meet
        for tx in range(32, 336, 16):
            r(im, tx, ty, 1, 1, C2)
    r(im, 16, 8, 320, 48, V2); r(im, 16, 8, 320, 2, V1); r(im, 16, 56, 320, 7, V1); r(im, 16, 55, 320, 1, V3)
    for a in ((16, 7, 320, 1), (16, 63, 320, 1), (15, 7, 1, 218), (336, 7, 1, 218), (15, 224, 145, 1),
              (192, 224, 145, 1), (159, 224, 1, 16), (192, 224, 1, 16)):
        r(im, *a, C0)
    Flat.shadow = Image.new('L', (352, 240))
    c = Flat(352, 240)
    m.rug(c, 52, 164, 248, 40); m.doormat(c, 162, 208)
    m.window(c, 52, 14); m.board(c, 144, 12); m.clock(c, 212, 18)
    m.bookshelf(c, 264, 12); m.plant(c, 22, 86); m.bin_(c, 242, 72)
    m.desk(c, 136, 68); m.chair(c, 156, 118)
    props = remap(c.im, ROOM)
    sprites = Image.new('RGBA', (352, 240))
    for src, row, col, x, y in PEOPLE:
        s = Image.open(os.path.join(HERE, '..', src)).convert('RGBA').crop((col * 64, row * 64, col * 64 + 40, row * 64 + 64))
        box = s.getbbox()
        ImageDraw.Draw(Flat.shadow).ellipse((x + box[0], y + box[3] - 4, x + box[2] + 2, y + box[3] + 1), fill=255)
        sprites.alpha_composite(remap(s, CAST), (x, y))
    px, sh = im.load(), Flat.shadow.load()
    for y in range(240):
        for x in range(352):
            if sh[x, y]:
                px[x, y] = SHADOW.get(px[x, y], px[x, y])
    im.alpha_composite(props)
    # the screen is the one neon thing in the room: redraw its code in the accent
    sx, sy = 164, 44
    r(im, sx, sy, 40, 22, C1); r(im, sx, sy, 40, 3, C2); r(im, sx, sy + 3, 8, 19, C0)
    for i, (ind, w, col) in enumerate(((0, 12, NEON), (2, 16, TEAL), (2, 9, NEON), (4, 14, TEAL), (4, 7, NEON),
                                       (2, 11, TEAL), (0, 6, NEON))):
        r(im, sx + 10 + ind, sy + 5 + 2 * i + (i > 3), w, 1, col)
    for i in range(4):
        r(im, sx + 1, sy + 5 + 3 * i, 5 - i % 2, 1, V1)
    im.alpha_composite(sprites)
    return im


# --- portrait tier ------------------------------------------------------------------------------------------------
PW, PH, OY, SS = 140, 150, 16, 4   # the figure is laid out in its own space; OY is where its y = 0 sits in the picture


def chaikin(pts, n=3):  # round a closed polygon
    for _ in range(n):
        out = []
        for i, (ax, ay) in enumerate(pts):
            bx, by = pts[(i + 1) % len(pts)]
            out += [(0.75 * ax + 0.25 * bx, 0.75 * ay + 0.25 * by), (0.25 * ax + 0.75 * bx, 0.25 * ay + 0.75 * by)]
        pts = out
    return pts


def mask(*shapes):
    """Shapes (('e', cx, cy, rx, ry) or a point list) drawn 4x and brought down hard: clean pixel curves."""
    big = Image.new('L', (PW * SS, PH * SS))
    d = ImageDraw.Draw(big)
    for s in shapes:
        if s[0] == 'e':
            _, cx, cy, rx, ry = s
            d.ellipse(((cx - rx) * SS, (cy + OY - ry) * SS, (cx + rx) * SS, (cy + OY + ry) * SS), fill=255)
        else:
            d.polygon([(x * SS, (y + OY) * SS) for x, y in s], fill=255)
    return big.resize((PW, PH), Image.BOX).point(lambda v: 255 if v >= 128 else 0)


def lam(x, y, cx, cy, rx, ry):  # light on a ball, from the upper left
    nx, ny = (x - cx) / rx, (y - cy) / ry
    nz = math.sqrt(max(0.0, 1 - nx * nx - ny * ny))
    return max(0.0, -0.50 * nx - 0.42 * ny + 0.76 * nz)


def mirror(pts):
    return [(140 - x, y) for x, y in pts]


def portrait():
    im = Image.new('RGBA', (PW, PH))
    px = im.load()
    # background: a dusk gradient and a neon ring, the source of the rim light
    rx_, ry_, R = 101, 62, 44
    for y in range(PH):
        for x in range(PW):
            d = math.hypot(x - rx_, y - ry_)
            c = dith(x, y, 0.12 + 0.75 * y / PH, [C0, C1, C2, C3], 1.0)
            if d < R - 1:
                slat = y > ry_ - 6 and (y - ry_ + 6) % 8 < 1 + (y - ry_ + 6) // 14
                c = C1 if slat else dith(x, y, 0.15 + 0.85 * (d / R) ** 2, [C1, C2, DTEAL, TEAL], 1.0)
            elif d < R + 1:
                c = NEON
            elif d < R + 9 and dith(x, y, 0.75 - (d - R) / 12, [C0, C9], 1.0) == C9:
                c = DTEAL
            px[x, y] = rgb(c)
    head = mask(chaikin([(42, 44), (46, 31), (57, 25), (70, 23), (83, 25), (94, 31), (98, 44), (99, 62), (96, 78),
                         (88, 92), (78, 99), (70, 100), (62, 99), (52, 92), (44, 78), (41, 62)]))
    ears = mask(('e', 40, 67, 5, 8), ('e', 100, 67, 5, 8))
    neck = mask([(57, 92), (83, 92), (85, 104), (89, 116), (51, 116), (55, 104)])
    shirt = mask(chaikin([(16, 140), (20, 124), (33, 114), (54, 106), (62, 111), (70, 113), (78, 111), (86, 106),
                          (107, 114), (120, 124), (124, 140)], 2), [(17, 130), (123, 130), (123, 140), (17, 140)])
    side_l = [(41, 63), (38, 50), (40, 36), (47, 27), (56, 23), (55, 31), (50, 40), (47, 50), (47, 63)]
    sides = mask(chaikin(side_l, 2), chaikin(mirror(side_l), 2))
    beard_o = [(40, 58), (40, 72), (44, 87), (53, 98), (63, 104), (70, 105), (77, 104), (87, 98), (96, 87),
               (100, 72), (100, 58)]
    beard_i = [(93, 58), (91, 70), (85, 81), (78, 79), (70, 78), (62, 79), (55, 81), (49, 70), (47, 58)]
    beard = mask(chaikin(beard_o + beard_i, 2))
    quiff = mask(chaikin([(48, 40), (42, 29), (41, 13), (46, -1), (55, -9), (61, -11), (66, -16), (72, -11),
                          (83, -8), (93, 1), (98, 14), (98, 28), (94, 40), (85, 34), (75, 36), (64, 33), (55, 36)]))
    hm, em, nm, sm, dm, bm, qm = (i.load() for i in (head, ears, neck, shirt, sides, beard, quiff))
    SKIN = [C4, C5, C6, C7, C8]
    opening = lambda x, y: ((x - 70) / 14) ** 2 + ((y - 104) / 9) ** 2 < 1      # the neck inside the collar
    band = lambda x, y: ((x - 70) / 18) ** 2 + ((y - 105) / 13) ** 2 < 1        # the collar band
    for cy in range(PH):
        y = cy - OY
        for x in range(PW):
            c = None
            if sm[x, cy]:
                v = 0.92 - 0.55 * (x - 22) / 96 - 0.30 * (y - 106) / 28
                c = dith(x, cy, v, [C1, DTEAL, TEAL, TEAL])
                if band(x, y):
                    c = dith(x, cy, 0.8 - 0.7 * (x - 52) / 36, [C1, DTEAL, DTEAL], 1.0)
            if nm[x, cy] and (not sm[x, cy] or opening(x, y)):
                c = dith(x, cy, 0.36 + 0.35 * lam(x, y, 66, 106, 16, 16) - (0.22 if y < 104 else 0), SKIN)
            if em[x, cy]:
                c = dith(x, cy, 0.62 if x < 70 else 0.3, SKIN)
            if hm[x, cy]:
                v = 0.18 + 0.74 * lam(x, y, 70, 60, 34, 44)
                if any(cy - k >= 0 and qm[x - k // 2, cy - k] for k in (1, 2, 3, 4)):   # the quiff shades the brow
                    v -= 0.28
                c = dith(x, cy, min(v, 0.80), SKIN)
            if bm[x, cy]:
                s = 0.5 + 0.5 * math.sin(x * 1.9 + y * 0.35)
                c = dith(x, cy, 0.06 + lam(x, y, 70, 72, 36, 40) * (0.45 + 0.5 * s), [C0, C1, C2, C3], 1.4)
            if dm[x, cy]:
                s = 0.5 + 0.5 * math.sin(x * 2.3 + y * 0.5)
                c = dith(x, cy, 0.22 + lam(x, y, 70, 48, 38, 40) * (0.7 + 0.3 * s), [C2, V1, V2, V3], 1.4)
            if qm[x, cy]:
                a, rr = math.atan2(y - 44, x - 66), math.hypot(x - 66, y - 44)
                s = 0.5 + 0.5 * math.sin(a * 34 + rr * 0.12)
                c = dith(x, cy, 0.05 + lam(x, y, 68, 14, 31, 34) * (0.35 + 0.75 * s), [C0, C1, C2, V1], 1.2)
            if c:
                px[x, cy] = rgb(c)
    ft = Image.new('RGBA', (PW, PH - OY))                                  # hard pixel features, in figure space
    d = ImageDraw.Draw(ft)
    P = lambda pts, c: d.polygon(pts, fill=rgb(c))
    L = lambda pts, c, w=1: d.line(pts, fill=rgb(c), width=w)
    L([(38, 63), (37, 67), (39, 71)], C5); L([(102, 63), (103, 67), (101, 71)], C4)                  # ears
    # nose: a shadow plane on the far side, nostrils, one hard highlight
    P([(72, 62), (75, 71), (77, 75), (73, 77), (71, 74)], C5)
    L([(64, 74), (65, 77), (68, 78), (72, 78), (75, 77)], C4); r(ft, 66, 76, 2, 1, C3); r(ft, 72, 76, 2, 1, C3)
    r(ft, 68, 70, 2, 3, C8); r(ft, 68, 70, 1, 1, C9)
    for sgn in (1, -1):                                                    # eyes: big iris under a heavy lid
        X = lambda x: x if sgn == 1 else 140 - x
        P([(X(50), 62), (X(53), 60), (X(59), 60), (X(62), 62), (X(59), 65), (X(53), 65)], C8)
        ix = 56 if sgn == 1 else 84
        d.ellipse((ix - 3, 59, ix + 3, 65), fill=rgb(C3)); r(ft, ix - 1, 61, 3, 3, C0); r(ft, ix - 2, 60, 2, 2, C9)
        L([(X(50), 62), (X(52), 60), (X(60), 60), (X(62), 62)], C0); L([(X(52), 59), (X(60), 59)], C0)
        L([(X(53), 58), (X(59), 58)], C0)
        L([(X(52), 66), (X(54), 67), (X(58), 67), (X(60), 66)], C5)                                   # cheek pushes up
        P([(X(47), 50), (X(50), 46), (X(57), 44), (X(64), 45), (X(65), 48), (X(57), 47), (X(51), 49)], C0)   # brow
    for x0 in (45, 74):                                                    # glasses: thick frames, hard reflections
        d.rounded_rectangle((x0, 52, x0 + 21, 69), radius=5, outline=rgb(C0), width=2)
        L([(x0 + 3, 58), (x0 + 6, 55)], C9); L([(x0 + 5, 59), (x0 + 9, 55)], C9)
    L([(66, 58), (68, 56), (72, 56), (74, 58)], C0); L([(66, 59), (68, 57), (72, 57), (74, 59)], C0)
    L([(45, 57), (40, 58)], C0, 2); L([(95, 57), (100, 58)], C0, 2)
    r(ft, 93, 58, 1, 7, NEON); r(ft, 92, 56, 1, 2, TEAL); r(ft, 92, 65, 1, 2, TEAL)                   # the ring in the far lens
    # mouth: a grin inside the beard
    P([(61, 85), (79, 85), (77, 90), (70, 92), (63, 90)], C0)
    r(ft, 63, 86, 14, 2, C9); r(ft, 64, 88, 12, 1, C8); r(ft, 69, 86, 1, 2, V3)
    L([(64, 92), (70, 94), (76, 92)], C4); L([(65, 91), (70, 93), (75, 91)], C5)
    # one hard highlight along the lit shoulder
    L([(40, 113), (30, 118), (24, 124)], NEON); L([(47, 110), (42, 112)], NEON)
    im.alpha_composite(ft, (0, OY))
    # dark line round the whole figure, then the neon rim on the side facing the ring
    fig = head
    for part in (ears, neck, shirt, sides, beard, quiff):
        fig = ImageChops.lighter(fig, part)
    grown = fig
    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        s = Image.new('L', fig.size); s.paste(fig, (dx, dy)); grown = ImageChops.lighter(grown, s)
    im.paste(rgb(C0), mask=ImageChops.subtract(grown, fig))
    f = fig.load()
    for y in range(PH):
        for x in range(60, PW - 2):
            if f[x, y] and not f[x + 1, y]:
                px[x, y] = rgb(NEON)
                if f[x - 1, y] and (x + y) % 2 == 0:
                    px[x - 1, y] = rgb(TEAL)
            elif f[x, y] and y > 0 and not f[x, y - 1] and x > 78:
                px[x, y] = rgb(NEON)
    return im


# --- the frame ----------------------------------------------------------------------------------------------------
def frame(im, x, y, w, h, fill=C1):
    """Ornate border, 6 px: bone line, dithered band, bone line, with a neon stud in each corner."""
    r(im, x, y, w, h, C0); r(im, x + 1, y + 1, w - 2, h - 2, C7)
    for yy in range(y + 2, y + h - 2):
        for xx in range(x + 2, x + w - 2):
            im.putpixel((xx, yy), rgb(C4 if (xx + yy) % 2 else C2))
    r(im, x + 4, y + 4, w - 8, h - 8, C8); r(im, x + 4, y + h - 5, w - 8, 1, C5); r(im, x + w - 5, y + 4, 1, h - 8, C5)
    r(im, x + 5, y + 5, w - 10, h - 10, C0); r(im, x + 6, y + 6, w - 12, h - 12, fill)
    for cx, cy in ((x, y), (x + w - 9, y), (x, y + h - 9), (x + w - 9, y + h - 9)):
        r(im, cx, cy, 9, 9, C0); r(im, cx + 1, cy + 1, 7, 7, C7); r(im, cx + 2, cy + 2, 5, 5, C1)
        diamond(im, cx + 4, cy + 4, 2, NEON)
    for xx in range(x + 28, x + w - 20, 24):                               # small bone studs along top and bottom
        for yy in (y + 2, y + h - 4):
            r(im, xx, yy, 2, 2, C8)
    for yy in range(y + 28, y + h - 20, 24):
        for xx in (x + 2, x + w - 4):
            r(im, xx, yy, 2, 2, C8)


def diamond(im, cx, cy, n, c):
    for i in range(-n, n + 1):
        r(im, cx - (n - abs(i)), cy + i, 2 * (n - abs(i)) + 1, 1, c)


def braces(im, x, y, w, h):
    """A small dithered brace with a bone edge in each inner corner of a panel."""
    for sx, sy, ox, oy in ((1, 1, x, y), (-1, 1, x + w - 1, y), (1, -1, x, y + h - 1), (-1, -1, x + w - 1, y + h - 1)):
        for i in range(9):
            for j in range(9 - i):
                c = C7 if i + j == 8 else C0 if i + j == 7 else C4 if (i + j) % 2 else C2
                im.putpixel((ox + sx * i, oy + sy * j), rgb(c))
        im.putpixel((ox + sx * 2, oy + sy * 2), rgb(NEON))


def plate(im, cx, y):  # a cartouche set into the top edge of a frame
    r(im, cx - 21, y - 1, 43, 9, C0); r(im, cx - 20, y, 41, 7, C7); r(im, cx - 19, y + 1, 39, 5, C1)
    for dx in (-12, 0, 12):
        diamond(im, cx + dx, y + 3, 2, NEON if dx == 0 else C5)


def rule(im, x, y, w):  # the double line between parts of a panel
    r(im, x, y, w, 1, C0); r(im, x, y + 1, w, 1, C8); r(im, x, y + 2, w, 1, C5); r(im, x, y + 3, w, 1, C0)


def scene():
    im = Image.new('RGBA', (W, H), rgb(C0))
    # the view
    frame(im, 4, 4, 364, 252)
    im.paste(room(), (10, 10))
    braces(im, 10, 10, 352, 240); plate(im, 186, 4)
    # the portrait panel: picture, name plate, command menu
    frame(im, 372, 4, 152, 252)
    im.paste(portrait(), (378, 10))
    braces(im, 378, 10, 140, 150); plate(im, 448, 4)
    rule(im, 378, 160, 140)
    for y in range(164, 180):                                             # name plate: a dithered bar
        for x in range(378, 518):
            im.putpixel((x, y), rgb(dith(x, y, 0.75 - abs(x - 448) / 110, [C1, DTEAL, TEAL], 1.0)))
    text(im, 448 - width('HERO') // 2, 168, 'HERO', C9)
    for cx in (424, 472):
        diamond(im, cx, 171, 3, NEON); diamond(im, cx, 171, 1, C0)
    rule(im, 378, 180, 140)
    for y in range(184, 250):
        for x in range(378, 518):
            im.putpixel((x, y), rgb(dith(x, y, 0.1 + 0.5 * (y - 184) / 66, [C1, C2, C3], 1.0)))
    for i, word in enumerate(('TALK', 'LOOK', 'WORK', 'LEAVE')):
        y = 191 + 15 * i
        if i == 0:                                                        # the chosen command
            r(im, 386, y - 4, 124, 15, C0); r(im, 387, y - 3, 122, 13, TEAL); r(im, 387, y - 3, 122, 1, NEON)
            r(im, 387, y + 9, 122, 1, DTEAL)
            for k in range(4):                                            # pointer
                r(im, 392 + k, y + k, 1, 7 - 2 * k, C9)
        else:
            diamond(im, 394, y + 3, 2, C5)
        text(im, 406, y, word, C9 if i == 0 else C8)
    # the dialogue window
    frame(im, 4, 260, 520, 96)
    for y in range(266, 350):
        for x in range(10, 518):
            im.putpixel((x, y), rgb(dith(x, y, 0.05 + 0.5 * (y - 266) / 84, [C1, C2, C3], 1.0)))
    braces(im, 10, 266, 508, 84); plate(im, 264, 260)
    for n, col in ((34, C3), (27, C4), (20, C3), (13, TEAL)):              # an emblem of nested diamonds
        for i in range(-n, n + 1):
            for sx in (-1, 1):
                im.putpixel((440 + sx * (n - abs(i)), 308 + i), rgb(col))
    diamond(im, 440, 308, 5, NEON); diamond(im, 440, 308, 2, C0)
    for i, line in enumerate(('WELCOME TO THE OFFICE.', 'LOOK AROUND, ASK ME ANYTHING.', 'THE COFFEE IS STILL WARM.')):
        text(im, 30, 282 + 19 * i, line, C9)
    for k in range(4):                                                    # "more" marker
        r(im, 496 + k, 336 + k, 9 - 2 * k, 1, NEON)
    return im


if __name__ == '__main__':
    im = scene()
    used = {'%02x%02x%02x' % p[:3] for _, p in im.getcolors(99999)}
    assert used <= set(PAL) and len(used) <= 16, used - set(PAL)          # the one rule: 16 colours on screen
    sat = lambda c: colorsys.rgb_to_hsv(*(b / 255 for b in bytes.fromhex(c)))[1]
    assert max(sat(c) for c in PAL[2:13]) < 0.45 < sat(NEON)              # a low-saturation family, one neon
    out = im.resize((W * 2, H * 2), Image.NEAREST)
    assert out.size == (1056, 720)
    out.save(os.path.join(HERE, 'd09-portrait-pc98.png'))
    print('d09-portrait-pc98.png', len(used), 'colours')
