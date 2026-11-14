# Direction 6, "Lived-in clutter" (reports/Pixel art style directions.md), as one still.
# The room is redrawn; only the layout of the office corner and the cast sheets come from the existing test.
#   palette: nine ramps of seven steps. Every ramp starts on the same deep teal (K) and ends on the same pale
#     amber (HI), so shadow is teal and light is amber whatever the material. 45 colours at most.
#   environment: no outlines. A pixel is a material and a level on that material's ramp; an object is told from
#     its neighbour by a lit top edge, a dark bottom edge and the shadow it casts down and right.
#   light is painted in: pools of level (window, lamp, fairy lights) are added before the ramp is looked up, and
#     a slow noise breaks the band edges so they read as brushwork, not as a gradient.
#   clutter: about fifty props (cables, notes, boxes, mugs, shoes, a fridge, a dog bed...), each drawn here.
#   characters stay as they are on the sheets, outlined, cut to two flat tones per part, and are not lit.
# usage (repo root): python3 -I art-tests/claude-drawn/directions/make_d06_lived_in_clutter.py
import os, random
from contextlib import contextmanager
from PIL import Image, ImageChops, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
W, H, U = 352, 240, 32          # U: one ramp step in the level image
K, HI = '131c2b', 'fff3c7'
RAMPS = [None,
         ['1c3a44', '46555a', '8a6a4a', 'c08a4a', 'eab760'],    # FLOOR  warm wood, also amber things
         ['2a3346', '5a4250', '9a5440', 'cc7a42', 'eea858'],    # DESK   red-brown furniture
         ['1e4149', '3a6468', '6f8f84', 'aab08c', 'e0cf9a'],    # WALL   plaster
         ['173f41', '28614f', '4f8a4c', '8fb04e', 'cfd66a'],    # GREEN
         ['22364c', '3e566c', '6c8794', 'a3b5ac', 'd9dcc0'],    # METAL  blue-grey
         ['124855', '14767c', '22a79b', '6cd3b2', 'c2edc4'],    # TEAL
         ['2d3a46', '6a5a55', 'a8845e', 'dba97c', 'f0d09c'],    # CARD   cardboard, cork, skin
         ['33294a', '6a2f4d', 'a8423f', 'd96a42', 'f4a25c'],    # RED
         ['22364c', '3e566c', '8fa6a0', 'c9cdb4', 'f0e6c0']]    # PAPER  white things; its darks are METAL's
RAMPS = [None] + [[K] + r + [HI] for r in RAMPS[1:]]
FLOOR, DESK, WALL, GREEN, METAL, TEAL, CARD, RED, PAPER = range(1, 10)
FLAT = 50                       # material + FLAT: not lit, not shadowed (screens, bulbs, the sky)

mat, lvl, shd = Image.new('L', (W, H)), Image.new('L', (W, H)), Image.new('L', (W, H))
dm, dl = ImageDraw.Draw(mat), ImageDraw.Draw(lvl)
lights = []                     # (image, steps of level it adds at full white)


def R(x, y, w, h, m, l):        # rectangle of material m at level l
    b = (x, y, x + w - 1, y + h - 1); dm.rectangle(b, fill=m); dl.rectangle(b, fill=round(l * U))


def E(x, y, w, h, m, l):        # ellipse
    b = (x, y, x + w - 1, y + h - 1); dm.ellipse(b, fill=m); dl.ellipse(b, fill=round(l * U))


def G(pts, m, l):               # polygon
    dm.polygon(pts, fill=m); dl.polygon(pts, fill=round(l * U))


def L(pts, m, l, w=1):          # line
    dm.line(pts, fill=m, width=w); dl.line(pts, fill=round(l * U), width=w)


def T(x, y, w, h, d):           # tone: whatever is there gets d steps lighter (or darker)
    b = (x, y, x + w, y + h); lvl.paste(lvl.crop(b).point(lambda v: max(0, min(255, v + round(d * U)))), b)


def shift(mask, dx, dy):
    out = Image.new('L', (W, H)); out.paste(mask, (dx, dy)); return out


@contextmanager
def prop(cast=(2, 3), rim=1.0):
    """What is drawn inside becomes one object: lit top edge, dark bottom edge, a cast shadow. No outline."""
    m0, l0 = mat.copy(), lvl.copy()
    yield
    mask = ImageChops.lighter(ImageChops.difference(mat, m0), ImageChops.difference(lvl, l0)).point(lambda v: 255 * (v > 0))
    if rim:
        step = Image.new('L', (W, H), round(rim * U))
        lvl.paste(ImageChops.add(lvl, step), mask=ImageChops.subtract(mask, shift(mask, 0, 1)))
        lvl.paste(ImageChops.subtract(lvl, step), mask=ImageChops.subtract(mask, shift(mask, 0, -1)))
    shd.paste(0, mask=mask)
    if cast:
        sweep = Image.new('L', (W, H))
        for i in range(1, max(cast) + 1):
            sweep = ImageChops.lighter(sweep, shift(mask, round(cast[0] * i / max(cast)), round(cast[1] * i / max(cast))))
        shd.paste(255, mask=ImageChops.subtract(sweep, mask))


def light(amp, blur, draw):
    im = Image.new('L', (W, H)); draw(ImageDraw.Draw(im))
    lights.append((im.filter(ImageFilter.GaussianBlur(blur)), amp))


# --- room shell -----------------------------------------------------------------------------------------------
def shell():
    rnd = random.Random(3)
    R(16, 8, 320, 56, WALL, 3.3)
    for _ in range(46):                                        # plaster in patches
        E(rnd.randrange(8, 330), rnd.randrange(4, 44), rnd.randrange(10, 36), rnd.randrange(4, 12), WALL,
          3.3 + rnd.choice((-.45, -.3, .3, .45)))
    E(22, 30, 30, 18, WALL, 2.6); E(300, 6, 40, 14, WALL, 2.6)  # damp
    for pts in ([(196, 8), (198, 14), (195, 19), (199, 26)], [(96, 56), (99, 60), (97, 63)], [(318, 30), (322, 38)]):
        L(pts, WALL, 1.6)                                      # cracks
    R(16, 8, 320, 2, WALL, 2)                                  # under the ceiling
    R(16, 45, 320, 12, WALL, 2.7); R(16, 44, 320, 1, WALL, 4); R(16, 45, 320, 1, WALL, 2)     # painted dado
    for x in range(20, 336, 9):
        R(x + rnd.randrange(3), 47 + rnd.randrange(8), 2, 1, WALL, 2.3)                        # scuffs
    R(16, 57, 320, 7, DESK, 2.8); R(16, 57, 320, 1, DESK, 4); R(16, 62, 320, 2, DESK, 1.6)    # skirting
    for i in range(20):                                        # floorboards
        y, x = 64 + 8 * i, 16 - rnd.randrange(40)
        while x < 336:
            n = rnd.randrange(34, 80)
            R(x, y, n, 8, FLOOR, 3 + rnd.choice((-.4, -.2, 0, 0, .2, .35)))
            R(x, y, 1, 8, FLOOR, 1.8)
            for _ in range(2):
                R(x + rnd.randrange(3, n - 16), y + rnd.randrange(2, 6), rnd.randrange(4, 14), 1, FLOOR, 2.5)
            R(x + 2, y + 3, 1, 1, FLOOR, 1.5); R(x + n - 3, y + 3, 1, 1, FLOOR, 1.5)             # nails
            x += n
        R(16, y + 7, 320, 1, FLOOR, 2)
    R(0, 0, W, 8, 0, 0); R(0, 0, 16, H, 0, 0); R(336, 0, 16, H, 0, 0); R(0, 224, 160, 16, 0, 0); R(192, 224, 160, 16, 0, 0)
    T(16, 64, 320, 3, -1); R(160, 224, 32, 1, FLOOR, 1.5)      # the wall's shadow, the door sill


def pipes():
    with prop(cast=(1, 2)):
        R(16, 11, 248, 3, METAL, 3.4); R(16, 11, 248, 1, METAL, 4.4); R(16, 13, 248, 1, METAL, 2)
        for x in (40, 130, 200, 252):
            R(x, 10, 3, 5, METAL, 2.6)
    with prop(cast=(1, 2)):
        R(19, 12, 4, 51, METAL, 3.2); R(19, 12, 1, 51, METAL, 4.2); R(22, 12, 1, 51, METAL, 2)
        R(18, 34, 6, 3, METAL, 2.4); R(17, 26, 8, 4, RED, 3.4); R(17, 26, 8, 1, RED, 4.4)      # joint, valve
    R(20, 38, 1, 20, WALL, 1.8); R(21, 44, 1, 10, WALL, 1.8)                                  # a rust run under it


def sign(x, y):
    with prop(cast=(1, 2)):
        R(x, y, 20, 15, METAL, 1.4); R(x + 9, y - 3, 1, 3, METAL, 2)
        R(x + 4, y + 5, 9, 7, TEAL + FLAT, 4); R(x + 6, y + 5, 5, 5, METAL + FLAT, 1); R(x + 13, y + 6, 3, 1, TEAL + FLAT, 4)       # a cup,
        R(x + 15, y + 6, 1, 4, TEAL + FLAT, 4); R(x + 13, y + 9, 3, 1, TEAL + FLAT, 4)
        R(x + 6, y + 2, 1, 2, RED + FLAT, 5); R(x + 9, y + 1, 1, 3, RED + FLAT, 5)                                                 # steaming
    light(.8, 4, lambda d: d.rectangle((x - 3, y - 2, x + 23, y + 20), fill=255))


def fairy_lights():
    pts, bulbs = [], []
    for x0, y0, x1, y1, sag in ((120, 14, 144, 16, 7), (190, 16, 212, 19, 6), (232, 20, 264, 15, 8)):
        seg = [(round(x0 + (x1 - x0) * t / 12), round(y0 + (y1 - y0) * t / 12 + sag * (1 - (t / 6 - 1) ** 2))) for t in range(13)]
        L(seg, METAL, 1.2); bulbs += seg[1:-1:2]
    for i, (x, y) in enumerate(bulbs):
        R(x, y + 1, 2, 2, (FLOOR, RED, FLOOR, TEAL)[i % 4] + FLAT, (6, 5, 5, 5)[i % 4])
    light(.9, 3, lambda d: [d.ellipse((x - 4, y - 3, x + 5, y + 6), fill=255) for x, y in bulbs])


def window(x, y):
    with prop(cast=(2, 3)):
        R(x, y, 68, 40, PAPER, 4.2); R(x + 66, y, 2, 40, PAPER, 3); R(x + 4, y + 30, 5, 1, PAPER, 3); R(x + 50, y + 2, 7, 1, PAPER, 3)
        for n, px in enumerate((x + 3, x + 36)):
            R(px - 1, y + 2, 31, 36, PAPER, 2)
            R(px, y + 3, 29, 12, TEAL + FLAT, 3); R(px, y + 13, 29, 6, TEAL + FLAT, 4); R(px, y + 18, 29, 5, TEAL + FLAT, 5)
            R(px, y + 22, 29, 15, FLOOR + FLAT, 5); R(px, y + 30, 29, 7, RED + FLAT, 5)                     # low sun
            for bx, by, bw, m in ((0, 26, 5, 2), (4, 21, 6, 1), (11, 28, 5, 2), (15, 19, 6, 1), (22, 25, 7, 2)):
                bx = bx if n == 0 else 29 - bx - bw
                R(px + bx, y + by, bw, 37 - by, METAL + FLAT, m)
                for wy in range(by + 2, 36, 3):
                    if (wy + bx) % 2:
                        R(px + bx + 1 + (wy % 2) * 2, y + wy, 1, 1, FLOOR + FLAT, 5)
        E(x + 8, y + 16, 9, 9, FLOOR + FLAT, 6)                                                       # the sun
        for i in range(5):                                      # a blind, half down and not level
            R(x + 3, y + 3 + 3 * i, 29, 2, PAPER, 4.4 - (i % 2) * .6)
        for i in range(3):
            R(x + 36, y + 3 + 3 * i, 29, 2, PAPER, 4.4 - (i % 2) * .6)
        R(x + 36, y + 12, 14, 1, PAPER, 3.6); R(x + 61, y + 12, 1, 14, PAPER, 4); R(x + 60, y + 26, 3, 2, PAPER, 4.6)
    with prop(cast=(1, 1)):                                     # on the sill: cactus, mug, two books
        R(x + 54, y + 27, 4, 9, GREEN, 3.4); R(x + 54, y + 27, 1, 9, GREEN, 4.4); R(x + 58, y + 31, 2, 2, GREEN, 3); R(x + 59, y + 29, 2, 3, GREEN, 3)
        R(x + 52, y + 35, 8, 5, RED, 3.6); R(x + 58, y + 36, 2, 4, RED, 2.6)
    with prop(cast=(1, 1)):
        R(x + 8, y + 35, 12, 3, TEAL, 3); R(x + 9, y + 32, 11, 3, RED, 3.6); R(x + 8, y + 37, 12, 1, PAPER, 5); R(x + 9, y + 34, 11, 1, PAPER, 5)
        R(x + 24, y + 33, 5, 7, PAPER, 5); R(x + 28, y + 33, 1, 7, PAPER, 3.6); R(x + 29, y + 35, 2, 3, PAPER, 4)
    with prop(cast=(2, 3)):
        R(x - 4, y + 40, 76, 4, PAPER, 4.4); R(x - 4, y + 43, 76, 1, PAPER, 2.4)


def note(x, y, w, h, m, l, lines=2, cast=(1, 1)):
    with prop(cast=cast, rim=0):
        R(x, y, w, h, m, l); R(x, y + h - 1, w, 1, m, l - 1)
        for i in range(lines):
            R(x + 1, y + 2 + 2 * i, w - 2 - (i % 2) * 2, 1, m, l - 2)


def board(x, y):
    rnd = random.Random(5)
    with prop(cast=(2, 3)):
        R(x, y, 46, 28, DESK, 3.4); R(x + 2, y + 2, 42, 24, CARD, 3.2)
        for _ in range(50):
            R(x + 2 + rnd.randrange(42), y + 2 + rnd.randrange(24), 1, 1, CARD, rnd.choice((2.5, 3.8)))
        R(x + 2, y + 2, 42, 1, CARD, 2.2); R(x + 2, y + 2, 1, 24, CARD, 2.2)
    note(x + 4, y + 4, 9, 9, PAPER, 5.2, 3); note(x + 15, y + 3, 7, 7, FLOOR, 5.4); note(x + 13, y + 12, 8, 7, RED, 5)
    note(x + 6, y + 15, 6, 8, TEAL, 4.4); note(x + 34, y + 15, 9, 8, PAPER, 5, 3); note(x + 23, y + 17, 8, 6, FLOOR, 5.2, 1)
    with prop(cast=(1, 1), rim=0):                               # two photos
        R(x + 24, y + 4, 11, 10, PAPER, 5.4); R(x + 25, y + 5, 9, 6, TEAL + FLAT, 4); R(x + 25, y + 9, 9, 2, GREEN + FLAT, 3); R(x + 31, y + 6, 2, 2, FLOOR + FLAT, 6)
        R(x + 36, y + 3, 8, 9, PAPER, 5.2); R(x + 37, y + 4, 6, 5, RED + FLAT, 3); R(x + 39, y + 5, 2, 3, CARD + FLAT, 5)
    for px, py, m in ((8, 4, RED), (18, 3, TEAL), (29, 4, RED), (16, 12, FLOOR), (38, 15, TEAL), (9, 15, RED), (40, 3, FLOOR)):
        R(x + px, y + py, 2, 2, m + FLAT, 5); R(x + px + 1, y + py + 1, 1, 1, m + FLAT, 3)          # pins
    L([(x + 9, y + 5), (x + 17, y + 13), (x + 30, y + 5)], RED + FLAT, 4)                           # a thread between pins
    # notes that no longer fit on the board
    note(x - 9, y + 4, 7, 7, FLOOR, 5.2); note(x - 12, y + 13, 8, 7, TEAL, 4.4); note(x - 6, y + 22, 7, 6, RED, 5)
    note(x + 48, y + 20, 7, 7, FLOOR, 5.4); note(x + 49, y + 29, 6, 6, PAPER, 5, 1)


def clock(x, y):
    with prop(cast=(2, 3)):
        E(x, y, 20, 20, RED, 3.4); E(x + 2, y + 2, 16, 16, PAPER, 5); E(x + 4, y + 5, 13, 12, PAPER, 5.5)
        for tx, ty in ((9, 3), (9, 16), (3, 9), (16, 9)):
            R(x + tx, y + ty, 1, 1, PAPER, 2.4)
        R(x + 9, y + 5, 1, 5, METAL, .6); R(x + 10, y + 9, 4, 1, METAL, .6); R(x + 9, y + 9, 1, 1, RED + FLAT, 4)


def poster(x, y):
    with prop(cast=(1, 2), rim=0):
        R(x, y, 22, 30, PAPER, 5); R(x + 1, y + 1, 20, 28, RED + FLAT, 2); E(x + 6, y + 5, 11, 11, FLOOR + FLAT, 5)
        G([(x + 1, y + 28), (x + 8, y + 15), (x + 13, y + 22), (x + 17, y + 17), (x + 20, y + 23), (x + 20, y + 28)], TEAL + FLAT, 2)
        G([(x + 1, y + 28), (x + 5, y + 22), (x + 10, y + 28)], TEAL + FLAT, 3)
        G([(x + 16, y + 29), (x + 21, y + 29), (x + 21, y + 24)], PAPER, 3.4)                      # a corner that curls
    R(x + 9, y - 1, 4, 3, PAPER, 5.6); R(x - 1, y + 26, 3, 3, PAPER, 5.6)                             # tape
    with prop(cast=(1, 1)):                                      # calendar
        R(x - 46, y + 12, 13, 15, PAPER, 5.2); R(x - 46, y + 12, 13, 4, RED, 4)
        for i in range(9):
            R(x - 44 + 4 * (i % 3), y + 18 + 3 * (i // 3), 2, 1, PAPER, 3)
        R(x - 40, y + 21, 2, 1, RED + FLAT, 4)
    with prop(cast=(1, 1)):                                      # socket and switch
        R(124, 46, 7, 8, PAPER, 4.6); R(126, 48, 1, 2, PAPER, 2); R(128, 48, 1, 2, PAPER, 2); R(126, 51, 3, 1, PAPER, 2)
        R(318, 36, 6, 8, PAPER, 4.6); R(320, 38, 2, 4, PAPER, 3.4)


def book_row(x, base, end, rnd, lo=9, hi=16):
    while x < end:
        w, h, m, l = rnd.randrange(3, 6), rnd.randrange(lo, hi), rnd.choice((RED, TEAL, GREEN, CARD, PAPER, METAL, FLOOR, RED, DESK)), rnd.choice((3, 3.4, 4))
        R(x, base - h, w, h, m, l); R(x + w - 1, base - h, 1, h, m, l - 1.2); R(x, base - h, w, 1, m, l + .8)
        if w > 3:
            R(x + 1, base - h + 2, w - 2, 2, m, l + 1.6)
        x += w


def bookshelf(x, y):
    rnd = random.Random(8)
    with prop(cast=(3, 4)):
        R(x, y + 8, 64, 66, DESK, 2.8); R(x, y, 64, 8, DESK, 3.9); R(x + 61, y + 8, 3, 66, DESK, 2); R(x, y + 8, 2, 66, DESK, 3.4)
        R(x + 6, y + 3, 22, 1, DESK, 3.3); R(x + 34, y + 5, 18, 1, DESK, 3.3)
        for s in range(3):
            top = y + 11 + 21 * s
            R(x + 3, top, 58, 17, DESK, 1); R(x + 3, top, 58, 2, DESK, .4); R(x + 3, top + 17, 58, 3, DESK, 3.6); R(x + 3, top + 19, 58, 1, DESK, 2.2)
        book_row(x + 4, y + 28, x + 40, rnd)
        G([(x + 41, y + 28), (x + 46, y + 13), (x + 49, y + 14), (x + 45, y + 28)], RED, 3.4)        # one that leans
        book_row(x + 22, y + 49, x + 60, rnd)
        for i, (m, w) in enumerate(((TEAL, 15), (RED, 13), (PAPER, 14), (FLOOR, 11))):               # a flat pile
            R(x + 5 + i % 2, y + 46 - 3 * i, w, 3, m, 3.4); R(x + 5 + i % 2, y + 48 - 3 * i, w, 1, m, 2.2); R(x + 15, y + 46 - 3 * i, 3, 2, PAPER, 5)
        book_row(x + 4, y + 70, x + 30, rnd, 10, 14)
    with prop(cast=(1, 1)):                                      # trophy, camera, a jar of pens, a small radio
        tx, ty = x + 51, y + 16
        R(tx, ty, 8, 6, FLOOR, 5); R(tx + 1, ty + 1, 2, 4, FLOOR, 6); R(tx + 6, ty + 1, 2, 5, FLOOR, 4); R(tx + 3, ty + 6, 2, 3, FLOOR, 4); R(tx + 1, ty + 9, 6, 3, DESK, 3)
    with prop(cast=(1, 1)):
        R(x + 33, y + 60, 12, 10, METAL, 3); R(x + 34, y + 62, 6, 6, METAL, 1.4); R(x + 35, y + 63, 4, 4, METAL, 2.4); R(x + 42, y + 62, 2, 2, RED + FLAT, 4)
        R(x + 34, y + 55, 1, 5, METAL, 4)
    with prop(cast=(1, 1)):
        R(x + 49, y + 61, 9, 9, TEAL, 3); R(x + 56, y + 61, 2, 9, TEAL, 2)
        for i, m in enumerate((RED, FLOOR, PAPER, GREEN)):
            R(x + 50 + 2 * i, y + 55 - (i % 2) * 2, 1, 6 + (i % 2) * 2, m, 4.4)
    with prop(cast=(2, 2)):                                      # on top: two boxes, a rolled poster
        R(x + 4, y - 9, 22, 6, CARD, 4); R(x + 4, y - 3, 22, 8, CARD, 3); R(x + 13, y - 9, 3, 14, PAPER, 4.6); R(x + 18, y, 5, 3, PAPER, 5)
        R(x + 28, y - 5, 14, 4, CARD, 4.2); R(x + 28, y - 1, 14, 6, CARD, 3.2); R(x + 30, y + 1, 4, 2, RED, 4)
    with prop(cast=(1, 2)):
        R(x + 44, y - 2, 18, 4, PAPER, 4.6); R(x + 44, y + 1, 18, 1, PAPER, 3); R(x + 60, y - 2, 2, 4, PAPER, 2)
    with prop(cast=(1, 1)):                                      # a plant that trails down the side
        R(x - 1, y - 4, 9, 7, RED, 3.4); R(x - 1, y - 4, 9, 2, RED, 4.2)
        for lx, ly in ((0, -8), (4, -9), (7, -7), (-3, -5), (-4, 0), (-3, 5), (-5, 10), (-3, 15), (-4, 21), (-2, 26), (8, -3), (2, -6)):
            R(x + lx, y + ly, 3, 3, GREEN, 3.4 + (lx % 2) * .8); R(x + lx + 1, y + ly + 2, 2, 1, GREEN, 2.4)


def plant(x, y):
    with prop(cast=None, rim=0):
        for sx, sh in ((11, 14), (6, 8), (16, 10)):
            R(x + sx, y - sh, 2, sh, GREEN, 2)
    for dx, dy, w, h, l in ((-9, -24, 14, 10, 3.6), (17, -25, 14, 10, 3), (3, -36, 13, 12, 4), (-13, -12, 14, 9, 3.2),
                            (20, -13, 15, 9, 2.8), (-3, -22, 13, 10, 3.6), (10, -19, 13, 10, 3), (4, -10, 14, 9, 3.4),
                            (-6, -34, 10, 8, 4), (22, -34, 9, 8, 3)):
        with prop(cast=(2, 3), rim=0):
            E(x + dx, y + dy, w, h, GREEN, l - .9); E(x + dx, y + dy, w - 2, h - 2, GREEN, l); E(x + dx + 2, y + dy + 1, w // 2, h // 2, GREEN, l + .9)
            R(x + dx + 3, y + dy + h // 2, w - 6, 1, GREEN, l - .9)
    with prop(cast=(3, 4)):
        R(x, y, 24, 4, RED, 3.8); R(x + 20, y + 1, 4, 3, RED, 2.8)
        for i in range(16):
            ins = 1 + i // 6
            R(x + ins, y + 4 + i, 24 - 2 * ins, 1, RED, 3.2 - (i in (4, 5, 10, 11)) * .8); R(x + 19 - ins, y + 4 + i, 5, 1, RED, 2.2); R(x + ins + 2, y + 4 + i, 2, 1, RED, 4)
        R(x + 1, y + 20, 22, 2, DESK, 3)
    with prop(cast=(1, 2)):                                      # a small pot beside it, a watering can
        R(x + 30, y + 12, 9, 8, PAPER, 4.4); R(x + 37, y + 12, 2, 8, PAPER, 3.4); E(x + 29, y + 5, 7, 6, GREEN, 3.8); E(x + 34, y + 4, 7, 7, GREEN, 3); E(x + 32, y + 8, 6, 5, GREEN, 4.2)
    with prop(cast=(2, 2)):
        R(x + 42, y + 8, 11, 11, TEAL, 3.2); R(x + 50, y + 8, 3, 11, TEAL, 2.2); L([(x + 53, y + 14), (x + 59, y + 9)], TEAL, 3.2, 2); R(x + 58, y + 7, 4, 3, TEAL, 3.8)
        L([(x + 42, y + 10), (x + 39, y + 12), (x + 42, y + 16)], TEAL, 2.4)
    R(x + 30, y + 26, 5, 3, GREEN, 3); R(x + 31, y + 27, 3, 1, GREEN, 2); R(x - 3, y + 24, 4, 2, GREEN, 2.6)   # fallen leaves


def fridge(x, y):
    with prop(cast=(3, 4)):
        R(x, y, 24, 10, PAPER, 4.4); R(x, y + 10, 24, 28, PAPER, 3.6); R(x + 21, y + 10, 3, 28, PAPER, 2.6); R(x, y + 19, 24, 1, PAPER, 2.2)
        R(x + 18, y + 12, 2, 5, METAL, 2); R(x + 18, y + 22, 2, 8, METAL, 2); R(x + 1, y + 36, 22, 2, METAL, 1.4)
        for mx, my, m in ((3, 12, RED), (8, 14, TEAL), (4, 23, FLOOR), (11, 24, RED), (7, 29, GREEN)):
            R(x + mx, y + my, 3, 3, m + FLAT, 4)
        R(x + 10, y + 27, 6, 7, PAPER, 5.4); R(x + 11, y + 29, 4, 1, PAPER, 3); R(x + 11, y + 31, 3, 1, PAPER, 3); R(x + 12, y + 27, 2, 1, TEAL + FLAT, 4)
    with prop(cast=(1, 2)):                                      # kettle, mugs, a banana
        R(x + 2, y - 6, 9, 10, METAL, 4); R(x + 9, y - 6, 2, 10, METAL, 3); R(x + 3, y - 8, 6, 2, METAL, 2.4); R(x + 11, y - 3, 3, 1, METAL, 2.4); R(x + 13, y - 3, 1, 5, METAL, 2.4); R(x + 3, y - 4, 1, 6, METAL, 5.4)
    with prop(cast=(1, 1)):
        R(x + 15, y - 1, 6, 6, RED, 4); R(x + 15, y - 5, 6, 4, TEAL, 4); R(x + 19, y - 5, 2, 10, METAL, 2)
        L([(x + 6, y + 7), (x + 10, y + 8), (x + 13, y + 6)], FLOOR, 5.4, 2)


def boxes():
    def box(x, y, w, d, h, tone=0, tape=True, label=None):
        with prop(cast=(3, 4)):
            R(x, y, w, d, CARD, 4.2 + tone); R(x, y + d, w, h, CARD, 3.2 + tone); R(x + w - 2, y + d, 2, h, CARD, 2.4 + tone)
            R(x + 2, y + d + h - 3, 6, 1, CARD, 2.4 + tone)
            if tape:
                R(x + w // 2 - 2, y, 4, d + 5, PAPER, 4.6); R(x, y + d // 2, w, 1, CARD, 3)
            if label:
                R(x + label, y + d + 3, 8, 6, PAPER, 5); R(x + label + 1, y + d + 5, 5, 1, PAPER, 3); R(x + label + 1, y + d + 7, 3, 1, RED + FLAT, 4)
    box(18, 190, 30, 10, 22, 0, True, 3); box(21, 172, 22, 8, 14, .3, True, 12)
    with prop(cast=(2, 3)):                                      # an open one on top, things sticking out
        R(24, 158, 18, 6, CARD, 1.4); R(24, 164, 18, 9, CARD, 3.4); R(22, 157, 3, 8, CARD, 4.4); R(41, 156, 4, 7, CARD, 4)
        R(28, 150, 3, 12, PAPER, 4.8); R(32, 153, 3, 9, TEAL, 3.6); R(36, 155, 4, 6, RED, 3.6); R(30, 150, 1, 12, PAPER, 3.4)
    box(306, 196, 28, 9, 20, -.2, True, 14)
    with prop(cast=(2, 3)):                                      # a crate of rolled paper
        R(308, 176, 22, 6, DESK, 1.4); R(308, 182, 22, 14, DESK, 3.2); R(308, 186, 22, 1, DESK, 2); R(308, 191, 22, 1, DESK, 2)
        for i, (m, l) in enumerate(((PAPER, 5), (PAPER, 4.4), (TEAL, 3.6), (PAPER, 5), (RED, 3.6))):
            R(310 + 4 * i, 168 + (i * 5) % 7, 3, 12 - (i * 5) % 7, m, l); R(312 + 4 * i, 168 + (i * 5) % 7, 1, 12 - (i * 5) % 7, m, l - 1.2)
    with prop(cast=(1, 1)):                                      # a pizza box against the wall, a paper cup
        R(52, 66, 20, 3, CARD, 4.2); R(52, 69, 20, 16, CARD, 3.4); E(57, 72, 10, 9, RED, 3.6); E(60, 75, 4, 3, FLOOR, 5)
    with prop(cast=(1, 2)):
        R(77, 78, 5, 7, PAPER, 5); R(81, 78, 1, 7, PAPER, 3.6); R(77, 80, 5, 2, RED, 4); R(76, 77, 7, 1, PAPER, 5.6)


def rug(x, y, w, h):
    rnd = random.Random(2)
    with prop(cast=None, rim=0):
        for fy in range(y + 1, y + h - 1, 2):
            R(x - 4, fy, 4, 1, PAPER, 4 - (fy % 4) * .2); R(x + w, fy + (fy % 3 == 0), 4 + (fy % 5 == 0), 1, PAPER, 4)
        R(x, y, w, h, RED, 2.6); R(x + 3, y + 3, w - 6, h - 6, FLOOR, 3.6); R(x + 4, y + 4, w - 8, h - 8, RED, 2.6)
        R(x + 7, y + 7, w - 14, h - 14, FLOOR, 3.4); R(x + 8, y + 8, w - 16, h - 16, RED, 3.2)
        for wy in range(y + 10, y + h - 9, 3):
            for wx in range(x + 10 + (wy % 2) * 3, x + w - 10, 6):
                R(wx, wy, 2, 1, RED, 2.6)
        for cx in range(x + 28, x + w - 20, 32):
            for i in range(-9, 10):
                for j in range(-9, 10):
                    d = abs(i) + abs(j)
                    if d <= 9:
                        m, l = ((RED, 2.4) if d in (6, 7) else (RED, 3.8) if d in (2, 3) else (FLOOR, 3.6) if d in (8, 9, 0, 1) else (FLOOR, 4.4))
                        R(cx + i, y + h // 2 + j, 1, 1, m, l)
        for _ in range(9):                                      # worn patches
            ex, ey, ew = x + rnd.randrange(w - 30), y + rnd.randrange(h - 8), rnd.randrange(12, 34)
            T(ex, ey, ew, rnd.randrange(3, 7), -.5)
    G([(x + w - 13, y + h - 1), (x + w, y + h - 1), (x + w, y + h - 12)], CARD, 3.4); L([(x + w - 13, y + h - 1), (x + w, y + h - 12)], RED, 1.6)     # a corner folded over


def doormat(x, y):
    with prop(cast=(1, 1), rim=0):
        R(x, y, 28, 12, GREEN, 2.6); R(x + 2, y + 2, 24, 8, GREEN, 2)
        for i in range(24):
            R(x + 2 + i, y + 3 + (i * 3) % 6, 1, 2, GREEN, 3.2)
    for sx, sy, m in ((132, 209, RED), (141, 211, RED), (196, 207, METAL), (205, 206, METAL)):          # shoes left at the door
        with prop(cast=(1, 2)):
            R(sx, sy, 7, 11, m, 3.4 if m == RED else 2); R(sx + 1, sy + 2, 5, 5, m, 1.4); R(sx, sy + 9, 7, 2, PAPER, 4.6); R(sx + 5, sy, 2, 11, m, 2.4 if m == RED else 1.4)
    with prop(cast=(2, 2)):                                      # skateboard
        R(214, 213, 34, 8, DESK, 3.4); R(216, 212, 30, 10, DESK, 3.4); R(217, 214, 28, 6, METAL, 1.6); R(226, 215, 6, 4, FLOOR + FLAT, 5); R(236, 216, 4, 3, TEAL + FLAT, 4)
        for wx in (219, 240):
            R(wx, 210, 4, 2, PAPER, 4.6); R(wx, 222, 4, 2, PAPER, 4.6)


def desk(x, y):
    with prop(cast=(3, 4)):
        R(x, y + 30, 6, 22, DESK, 2.6); R(x + 4, y + 30, 2, 22, DESK, 1.8)                         # left leg panel
        R(x + 6, y + 30, 54, 10, DESK, 1.2); R(x + 6, y + 30, 54, 3, DESK, .4)                     # knee panel, far back
        R(x + 60, y + 30, 36, 20, DESK, 2.8); R(x + 93, y + 30, 3, 20, DESK, 2); R(x + 60, y + 30, 36, 2, DESK, 1.8)
        R(x + 62, y + 50, 5, 2, DESK, 1.6); R(x + 88, y + 50, 5, 2, DESK, 1.6)
        for dy in (32, 41):
            R(x + 63, y + dy, 28, 8, DESK, 1.4); R(x + 64, y + dy + 1, 26, 6, DESK, 3.2); R(x + 64, y + dy + 1, 26, 1, DESK, 4)
            R(x + 73, y + dy + 3, 8, 2, METAL, 4.4); R(x + 73, y + dy + 4, 8, 1, METAL, 2.6)
        R(x + 66, y + 34, 5, 4, FLOOR + FLAT, 5); R(x + 84, y + 43, 4, 4, TEAL + FLAT, 4); R(x + 67, y + 44, 3, 3, RED + FLAT, 4)    # stickers
        R(x, y, 96, 26, DESK, 3.8); R(x + 93, y + 2, 3, 24, DESK, 3)                               # top
        for gx, gy, gw in ((8, 6, 22), (54, 10, 30), (20, 20, 40), (72, 22, 18), (4, 14, 12), (40, 4, 14), (26, 12, 9)):
            R(x + gx, y + gy, gw, 1, DESK, 3.3)
        for cx, cy in ((26, 18), (70, 4)):                         # mug rings
            E(x + cx, y + cy, 8, 6, DESK, 3.2); E(x + cx + 1, y + cy + 1, 6, 4, DESK, 3.8)
        R(x, y + 26, 96, 4, DESK, 3); R(x, y + 29, 96, 1, DESK, 2)                                 # front edge
    T(x + 6, y + 40, 54, 14, -1.4)                               # the dark under the desk
    with prop(cast=(1, 2)):                                      # PC tower and its cables, in the knee space
        R(x + 9, y + 31, 13, 4, METAL, 2.4); R(x + 9, y + 35, 13, 18, METAL, 2); R(x + 20, y + 35, 2, 18, METAL, 1.2)
        R(x + 11, y + 38, 2, 2, TEAL + FLAT, 5); R(x + 11, y + 42, 8, 1, METAL, 1); R(x + 11, y + 44, 8, 1, METAL, 1); R(x + 15, y + 38, 3, 1, RED + FLAT, 4)
    with prop(cast=(2, 2)):                                      # mouse mat, monitor
        R(x + 64, y + 13, 14, 12, METAL, 2.4); R(x + 64, y + 13, 14, 1, METAL, 3)
    with prop(cast=(3, 3)):
        R(x + 39, y + 8, 18, 4, METAL, 2.6); R(x + 45, y + 2, 6, 6, METAL, 2.2); R(x + 48, y + 2, 3, 6, METAL, 1.4)
        R(x + 26, y - 26, 44, 28, METAL, 2.2); R(x + 26, y - 26, 44, 1, METAL, 3.4); R(x + 69, y - 26, 1, 28, METAL, 1.4)
        sx, sy = x + 28, y - 24
        R(sx, sy, 40, 22, TEAL + FLAT, 1); R(sx, sy, 40, 3, METAL + FLAT, 1); R(sx, sy + 3, 8, 19, METAL + FLAT, 0)
        for i, m in enumerate((RED, FLOOR, GREEN)):
            R(sx + 1 + 2 * i, sy + 1, 1, 1, m + FLAT, 4)
        for i, w in enumerate((5, 4, 6, 3, 5)):
            R(sx + 1, sy + 5 + 3 * i, w, 1, METAL + FLAT, 2)
        code = ((0, ((4, RED), (7, TEAL))), (2, ((6, PAPER), (3, FLOOR))), (2, ((3, RED), (9, GREEN))), (4, ((8, PAPER),)),
                (4, ((5, TEAL), (4, FLOOR))), (2, ((2, RED),)), (0, ((6, TEAL), (3, PAPER))), (2, ((10, GREEN),)))
        for i, (ind, parts) in enumerate(code):
            lx = sx + 10 + ind
            for w, m in parts:
                R(lx, sy + 5 + 2 * i, w, 1, m + FLAT, 5 if m != GREEN else 4); lx += w + 1
    note(x + 22, y - 22, 6, 6, FLOOR, 5.4, 1); note(x + 67, y - 8, 6, 6, RED, 5, 1); note(x + 68, y - 27, 5, 5, TEAL, 4.6, 1)    # notes on the bezel
    with prop(cast=(1, 2)):                                      # paper pile, pen, phone
        R(x + 3, y + 6, 11, 13, PAPER, 4.4); R(x + 2, y + 4, 10, 13, PAPER, 5.2); R(x + 11, y + 4, 1, 13, PAPER, 4)
        for i, w in enumerate((6, 7, 4, 7, 5)):
            R(x + 3, y + 6 + 2 * i, w, 1, PAPER, 3.4)
        R(x + 3, y + 6, 3, 1, RED + FLAT, 4)
    with prop(cast=(1, 1)):
        R(x + 4, y + 20, 7, 5, METAL, 1.4); R(x + 5, y + 21, 5, 3, TEAL + FLAT, 3)
    with prop(cast=(2, 2)):                                      # keyboard, mouse
        R(x + 30, y + 15, 34, 9, PAPER, 4); R(x + 30, y + 23, 34, 1, PAPER, 2.6)
        for row in range(3):
            for i in range(11):
                R(x + 31 + 3 * i, y + 16 + 2 * row, 2, 1, PAPER, 5.4)
        R(x + 31, y + 22, 5, 1, PAPER, 5.4); R(x + 37, y + 22, 17, 1, PAPER, 5.4); R(x + 55, y + 22, 8, 1, PAPER, 5.4)
    with prop(cast=(1, 2)):
        R(x + 68, y + 16, 5, 7, PAPER, 5); R(x + 72, y + 16, 1, 7, PAPER, 3.6); R(x + 68, y + 21, 5, 2, PAPER, 4); R(x + 70, y + 16, 1, 2, METAL, 1.6)
    with prop(cast=(2, 3)):                                      # two mugs, one of them old
        R(x + 16, y + 9, 9, 11, RED, 3.6); R(x + 23, y + 9, 2, 11, RED, 2.6); R(x + 17, y + 9, 7, 2, DESK, 1.4); R(x + 25, y + 12, 3, 1, RED, 3.6); R(x + 27, y + 12, 1, 6, RED, 2.6); R(x + 25, y + 17, 3, 1, RED, 2.6)
        R(x + 16, y + 14, 9, 2, PAPER, 5)
    with prop(cast=(1, 2)):
        R(x + 62, y + 3, 7, 8, PAPER, 5); R(x + 67, y + 3, 2, 8, PAPER, 3.6); R(x + 63, y + 3, 5, 2, DESK, 1.4); R(x + 60, y + 5, 2, 4, PAPER, 4)
    with prop(cast=(1, 2)):                                      # pen pot, headphones
        R(x + 16, y - 2, 7, 8, TEAL, 2.8); R(x + 21, y - 2, 2, 8, TEAL, 1.8)
        for i, m in enumerate((RED, FLOOR, PAPER)):
            R(x + 17 + 2 * i, y - 8 + i % 2, 1, 6, m, 4.4)
    with prop(cast=(1, 1)):
        L([(x + 82, y + 23), (x + 83, y + 19), (x + 86, y + 18), (x + 89, y + 18), (x + 91, y + 20), (x + 92, y + 23)], METAL, 1.2)
        R(x + 80, y + 21, 3, 5, RED, 3.6); R(x + 91, y + 21, 3, 5, RED, 3.6); R(x + 91, y + 21, 1, 5, RED, 2.4)
    with prop(cast=(2, 3)):                                      # lamp: the shade glows
        R(x + 76, y + 13, 12, 3, METAL, 1.6); R(x + 81, y, 2, 13, METAL, 2.4)
        for i in range(10):
            w = 12 + 2 * (i // 2); lx = x + 82 - w // 2
            R(lx, y - 10 + i, w, 1, FLOOR + FLAT, 6); R(lx + w - w // 3, y - 10 + i, w // 3, 1, FLOOR + FLAT, 5)
        R(x + 73, y - 1, 18, 1, RED + FLAT, 5)
    for pts in ([(x + 48, y + 2), (x + 44, y - 4), (x + 20, y - 5), (x + 12, y - 2), (x - 6, y - 4), (x - 9, y - 12)],
                [(x + 88, y + 14), (x + 97, y + 12), (x + 100, y + 2), (x + 96, y - 6)]):
        with prop(cast=(1, 1), rim=0):                           # cables off the back of the desk, up to the socket
            L(pts, METAL, .8)


def floor_cables(x, y):
    with prop(cast=(1, 2)):                                      # power strip
        R(x, y, 18, 4, PAPER, 4.6); R(x, y + 4, 18, 2, PAPER, 3.2)
        for i in range(4):
            R(x + 2 + 4 * i, y + 1, 2, 2, METAL, 1)
        R(x + 15, y + 1, 2, 2, RED + FLAT, 4)
    for pts in ([(x, y + 2), (x - 6, y - 2), (x - 4, y - 14), (x + 6, y - 30), (x + 12, y - 44), (x + 13, y - 54)],
                [(x + 4, y + 1), (x + 10, y - 6), (x + 20, y - 4), (x + 26, y + 6), (x + 34, y + 8)],
                [(x + 9, y + 1), (x + 16, y - 9), (x + 30, y - 10), (x + 35, y - 2)],
                [(x + 3, y + 5), (x - 8, y + 12), (x - 30, y + 8), (x - 52, y + 14), (x - 68, y + 26), (x - 74, y + 34)]):
        with prop(cast=(1, 1), rim=0):
            L(pts, METAL, .8)
    with prop(cast=(1, 1), rim=0):
        L([(x + 20, y + 3), (x + 24, y + 14), (x + 18, y + 20), (x + 26, y + 26)], RED, 3)       # the one red cable


def backpack(x, y):
    with prop(cast=(3, 3)):
        R(x + 1, y, 15, 5, TEAL, 3.4); R(x, y + 4, 17, 17, TEAL, 2.6); R(x + 14, y + 4, 3, 17, TEAL, 1.8); R(x + 3, y + 11, 11, 8, TEAL, 3); R(x + 3, y + 11, 11, 1, METAL, 1.2)
        R(x + 6, y - 2, 5, 2, METAL, 1.6); R(x + 5, y + 14, 3, 3, FLOOR + FLAT, 5); R(x + 12, y + 6, 1, 4, PAPER, 5)
        R(x + 2, y + 5, 2, 15, METAL, 1.6); R(x + 2, y + 8, 13, 1, TEAL, 1.6)


def chair(x, y):
    with prop(cast=(3, 3)):
        R(x + 12, y + 32, 4, 5, METAL, 2.6); R(x + 3, y + 37, 22, 3, METAL, 1.6)
        for wx in (1, 11, 22):
            R(x + wx, y + 39, 5, 4, METAL, 1.2); R(x + wx + 1, y + 40, 2, 1, METAL, 2.6)
    with prop(cast=(3, 3)):
        R(x + 3, y, 22, 10, METAL, 3.6); R(x + 22, y + 2, 3, 8, METAL, 2.6)
    with prop(cast=(3, 3)):
        R(x + 1, y + 8, 26, 24, METAL, 2.8); R(x, y + 10, 28, 20, METAL, 2.8); R(x + 25, y + 11, 3, 16, METAL, 2); R(x, y + 27, 28, 3, METAL, 2)
        for sx in range(3, 26, 3):
            R(x + sx, y + 12, 1, 14, METAL, 2.3)
    with prop(cast=(2, 2)):                                      # a hoodie over the back
        G([(x - 2, y + 8), (x + 30, y + 8), (x + 31, y + 15), (x + 22, y + 14), (x + 12, y + 17), (x + 9, y + 28), (x - 3, y + 29)], RED, 3.2)
        R(x - 2, y + 8, 33, 2, RED, 4); L([(x + 3, y + 12), (x + 4, y + 27)], RED, 2.2); L([(x + 9, y + 11), (x + 8, y + 22)], RED, 2.2); L([(x + 20, y + 10), (x + 21, y + 13)], RED, 2.2)
        R(x + 13, y + 11, 1, 5, PAPER, 5); R(x + 16, y + 11, 1, 3, PAPER, 5)


def bin_(x, y):
    with prop(cast=None):
        R(x + 2, y - 1, 5, 4, PAPER, 5); R(x + 5, y, 2, 3, PAPER, 3.6); R(x + 7, y - 3, 5, 5, PAPER, 4.6); R(x + 10, y - 2, 2, 4, PAPER, 3.4); R(x + 4, y - 5, 4, 4, FLOOR, 5)
    with prop(cast=(3, 4)):
        R(x, y + 3, 14, 15, METAL, 3); R(x + 1, y + 18, 12, 1, METAL, 2); R(x, y + 3, 2, 15, METAL, 4); R(x + 10, y + 3, 4, 15, METAL, 2)
        for sx in (3, 6, 9, 12):
            R(x + sx, y + 5, 1, 12, METAL, 1.6)
        R(x, y + 2, 14, 2, METAL, 4.4)
    for px, py, m, l in ((18, 14, PAPER, 5), (-7, 17, PAPER, 4.6), (21, 22, FLOOR, 5), (12, 24, PAPER, 5)):
        with prop(cast=(1, 1)):
            R(x + px, y + py, 5, 4, m, l); R(x + px + 3, y + py + 1, 2, 3, m, l - 1.4); R(x + px + 1, y + py + 2, 1, 1, m, l - 1)
    with prop(cast=(2, 3)):                                      # a pile of books that never made it to the shelf
        for i, (m, w) in enumerate(((GREEN, 20), (RED, 18), (PAPER, 19), (TEAL, 16), (CARD, 18))):
            R(x + 66 + i % 2, y + 42 - 4 * i, w, 4, m, 3.2); R(x + 66 + i % 2, y + 45 - 4 * i, w, 1, m, 2)
        R(x + 67, y + 19, 16, 7, CARD, 4.2); R(x + 69, y + 21, 6, 3, PAPER, 5); R(x + 77, y + 16, 6, 6, PAPER, 5); R(x + 78, y + 17, 4, 2, DESK, 1.4)


def dog_corner(x, y):
    with prop(cast=(2, 2)):
        E(x, y, 38, 22, RED, 2.6); E(x + 1, y, 36, 19, RED, 3.4); E(x + 5, y + 3, 28, 13, CARD, 4.2); E(x + 8, y + 5, 20, 9, CARD, 3.6)
        R(x + 12, y + 8, 8, 2, PAPER, 5.2); E(x + 10, y + 7, 4, 4, PAPER, 5.2); E(x + 18, y + 7, 4, 4, PAPER, 5.2)    # a bone
    with prop(cast=(1, 2)):
        E(x + 4, y - 14, 14, 9, METAL, 4); E(x + 6, y - 13, 10, 6, CARD, 2.6); R(x + 5, y - 9, 12, 2, METAL, 2.6)
    with prop(cast=(1, 1)):
        E(x + 24, y - 10, 6, 6, TEAL, 4); R(x + 25, y - 9, 2, 2, TEAL, 5.2)                        # a ball


# --- light, cast, render ----------------------------------------------------------------------------------------
AMBIENT = -.85
SKIN = {'e8b796': RAMPS[CARD][4], 'c28569': RAMPS[CARD][3], 'ffffff': RAMPS[PAPER][5], '181425': K}
PEOPLE = [
    ('hero-detailed.png', 0, 214, 100, {**SKIN, '0099db': RAMPS[TEAL][3], '2ce8f5': RAMPS[TEAL][3], '124e89': RAMPS[TEAL][2],
                                        '262b44': RAMPS[METAL][1], '3a4466': RAMPS[METAL][1], '5a6988': RAMPS[METAL][2],
                                        '8b9bb4': RAMPS[METAL][3], '3e2731': K, '733e39': RAMPS[DESK][2], 'feae34': RAMPS[FLOOR][5]}),
    ('dana.png', 1, 256, 120, {**SKIN, 'fee761': RAMPS[FLOOR][5], 'feae34': RAMPS[FLOOR][5], 'd77643': RAMPS[FLOOR][4],
                               'be4a2f': RAMPS[FLOOR][4], 'e43b44': RAMPS[RED][3], 'f6757a': RAMPS[RED][3], 'a22633': RAMPS[RED][2],
                               '124e89': RAMPS[METAL][1], '3a4466': RAMPS[METAL][2], '5a6988': RAMPS[METAL][2], '3e2731': K}),
    ('dog.png', 2, 98, 134, {**SKIN, 'd77643': RAMPS[DESK][4], 'feae34': RAMPS[DESK][4], 'be4a2f': RAMPS[DESK][3],
                             '733e39': RAMPS[DESK][3], 'ead4aa': RAMPS[PAPER][5], 'e43b44': RAMPS[TEAL][3]}),
    ('visitor.png', 2, 50, 104, {**SKIN, 'f77622': RAMPS[RED][4], 'feae34': RAMPS[RED][4], 'be4a2f': RAMPS[RED][3], 'a22633': RAMPS[RED][3],
                                 '3e8948': RAMPS[GREEN][3], '63c74d': RAMPS[GREEN][3], '265c42': RAMPS[GREEN][2], '193c3e': RAMPS[GREEN][2],
                                 '3a4466': RAMPS[METAL][2], '5a6988': RAMPS[METAL][2], '262b44': RAMPS[METAL][1], '3e2731': K,
                                 '733e39': RAMPS[DESK][2], 'b86f50': RAMPS[RED][3]}),
]


def rgb(c):
    return tuple(bytes.fromhex(c))


def render():
    light(.8, 30, lambda d: d.ellipse((40, 50, 320, 225), fill=255))                             # the middle of the room
    for x0 in (55, 88):                                                                          # sun through two panes
        light(1.5, 2.5, lambda d, x0=x0: d.polygon([(x0, 66), (x0 + 28, 66), (x0 + 88, 150), (x0 + 52, 150)], fill=255))
    light(.5, 2, lambda d: d.rectangle((50, 56, 124, 66), fill=255))
    light(1.2, 7, lambda d: d.ellipse((188, 62, 254, 102), fill=255))                            # lamp on the desk
    light(.7, 8, lambda d: d.ellipse((198, 32, 242, 62), fill=255))                             # and on the wall behind it
    light(.6, 5, lambda d: d.ellipse((160, 78, 206, 96), fill=255))                              # the screen
    for _, _, x, y, _ in PEOPLE:                                                                 # shadows at the feet
        ImageDraw.Draw(shd).ellipse((x + 9, y + 58, x + 34, y + 65), fill=255)
    rnd = random.Random(6)
    slow = Image.new('L', (W // 18 + 2, H // 5 + 2))    # stretched along the boards; slow.putdata([rnd.randrange(256) for _ in range(slow.width * slow.height)])
    slow = slow.resize((W, H), Image.BICUBIC)
    M, V, S, N = mat.getdata(), lvl.getdata(), shd.getdata(), slow.getdata()
    Ls = [(im.getdata(), amp / 255) for im, amp in lights]
    out = []
    for i in range(W * H):
        m, v = M[i], V[i] / U
        if not m:
            out.append(rgb(K)); continue
        if m < FLAT:
            v += AMBIENT + sum(d[i] * a for d, a in Ls) - S[i] / 255 + (N[i] - 128) / 128 * .3
        out.append(rgb(RAMPS[m % FLAT][max(0, min(6, int(v + .5)))]))
    im = Image.new('RGB', (W, H)); im.putdata(out); im = im.convert('RGBA')
    for src, row, x, y, table in PEOPLE:
        s = Image.open(os.path.join(HERE, '..', src)).convert('RGBA').crop((0, row * 64, 40, row * 64 + 64))
        sp = s.load()
        for sy in range(64):
            for sx in range(40):
                if sp[sx, sy][3]:
                    sp[sx, sy] = rgb(table['%02x%02x%02x' % sp[sx, sy][:3]]) + (255,)
        im.alpha_composite(s, (x, y))
    return im


if __name__ == '__main__':
    shell(); pipes(); rug(52, 164, 248, 40); doormat(162, 208)
    sign(28, 16); window(52, 14); board(144, 12); clock(212, 18); poster(238, 14); fairy_lights(); bookshelf(264, 12)
    plant(22, 86); fridge(18, 118); boxes(); bin_(242, 72); dog_corner(296, 132)
    floor_cables(108, 104); desk(136, 68); backpack(116, 118); chair(156, 118)
    im = render()
    used = {'%02x%02x%02x' % p[:3] for _, p in im.getcolors(99999)}
    assert 32 <= len(used) <= 48, len(used)                     # the one check: the rule sheet's 32 to 48 colours
    im.resize((W * 3, H * 3), Image.NEAREST).save(os.path.join(HERE, 'd06-lived-in-clutter.png'))
    print('d06-lived-in-clutter.png written,', len(used), 'colours')
