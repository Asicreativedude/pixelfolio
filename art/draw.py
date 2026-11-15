# The lived-in clutter style (#65): the palette, the drawing primitives, the props, the light and the tile grid.
# A room (rooms/<name>.py) calls canvas(), draws on it with these, adds its room lights and calls render();
# room.py exports it for the game.
#   palette: ten ramps of seven steps. Every ramp starts on the same deep teal (K) and ends on the same pale
#     amber (HI), so shadow is teal and light is amber whatever the material. 48 colours at most.
#   no outlines. A pixel is a material and a level on that material's ramp; an object is told from its
#     neighbour by a lit top edge, a dark bottom edge and the shadow it casts down and right (prop()).
#   light is painted in: pools of level (window, lamp, fairy lights) are added before the ramp is looked up, and
#     a slow noise breaks the band edges so they read as brushwork, not as a gradient. On the boards a plank takes
#     its light whole, read at its middle row a few pixels off, so a pool's edge steps along the planks (#68). Deck plates (plates()) are lit
#     the same way, a plate at a time.
#   the same drawing is built twice, by day and in the evening: only the level of the room and the list of pools
#     change, there is no light layer over the picture.
# Taken from art-tests/claude-drawn/directions/make_d06_lived_in_clutter.py and make_d06_studio.py on the
# prototype/pixellab-test branch; the studio built from it is pixel for pixel the prototype's.
import random
from contextlib import contextmanager
import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFilter

W, H, U, TILE = 352, 240, 32, 32   # U: one ramp step in the level image. canvas() sets W and H
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
         ['22364c', '3e566c', '8fa6a0', 'c9cdb4', 'f0e6c0'],    # PAPER  white things; its darks are METAL's
         ['1c3a44', '655f52', 'a57a4a', 'd5a055', 'eab760']]    # WOOD   the floor's second wood: half a step off FLOOR
RAMPS = [None] + [[K] + r + [HI] for r in RAMPS[1:]]
FLOOR, DESK, WALL, GREEN, METAL, TEAL, CARD, RED, PAPER, WOOD = range(1, 11)
FLAT = 50                       # material + FLAT: not lit, not shadowed (screens, bulbs, the sky)
lights = []                     # (image, steps of level it adds at full white)
THINGS = []                     # (mask, solid, tall) of every thing() since canvas()
SHIFT = [0]                     # per plank of boards(), how far off its light is read; plank 0 is no plank


def canvas(w, h, evening):
    """Start a room of w x h px, by day or in the evening."""
    global W, H, EVE, mat, lvl, shd, dm, dl, plank
    W, H, EVE = w, h, evening
    mat, lvl, shd = (Image.new('L', (W, H)) for _ in range(3))
    dm, dl = ImageDraw.Draw(mat), ImageDraw.Draw(lvl)
    lights.clear(); THINGS.clear(); del SHIFT[1:]
    plank = {k: np.zeros((H, W), np.int32) for k in ('id', 'top', 'mat', 'lvl')}   # boards() fills it


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
    """A pool of light. No pool adds more than one step, and pools that overlap have different outlines, so the
    edges of the steps never run in rings."""
    assert abs(amp) <= 1
    if callable(draw):
        im = Image.new('L', (W, H)); draw(ImageDraw.Draw(im))
    else:
        im = Image.new('L', (W, H)); ImageDraw.Draw(im).polygon(draw, fill=255)
    lights.append((im.filter(ImageFilter.GaussianBlur(blur)), amp))


# --- props ------------------------------------------------------------------------------------------------------
def boards(x0, x1, y0, y1, rnd):
    """Floorboards. A plank is one of two woods half a step apart, and it is that wood from end to end: the
    floor's tone changes at plank edges only, never in patches across them. render() lights a plank whole.
    Nothing is drawn outside x0..x1, y0..y1: the first and last plank of a row are cut there."""
    def cut(x, y, w, h, m, l):
        xa, xb, yb = max(x, x0), min(x + w, x1), min(y + h, y1)
        if xb > xa and yb > y:
            R(xa, y, xb - xa, yb - y, m, l)
    for y in range(y0, y1, 8):
        x = x0 - rnd.randrange(40)
        while x < x1:
            n = rnd.randrange(40, 96)
            a, b = (FLOOR, WOOD) if rnd.random() < .55 else (WOOD, FLOOR)
            cut(x, y, n, 8, a, 3.3)
            if rnd.random() < .6:                               # one streak of grain, in the other wood
                g = rnd.randrange(10, n - 12)
                cut(x + rnd.randrange(4, n - g - 2), y + rnd.randrange(2, 6), g, 1, b, 3.3)
            cut(x, y, 1, 8, FLOOR, 2.3)                         # the joint at its end
            rows, cols = slice(y, min(y + 8, y1)), slice(max(x, x0), max(min(x + n, x1), x0))
            plank['id'][rows, cols] = len(SHIFT); plank['top'][rows, cols] = y
            SHIFT.append(random.Random(len(SHIFT)).randrange(-4, 5))
            x += n
        cut(x0, y + 7, x1 - x0, 1, FLOOR, 2.3)
    # what the boards look like now: a pixel drawn over later (a rug, a shadow toned in) is no longer plank
    plank['mat'][y0:y1, x0:x1] = np.asarray(mat)[y0:y1, x0:x1]; plank['lvl'][y0:y1, x0:x1] = np.asarray(lvl)[y0:y1, x0:x1]


def plates(x0, x1, y0, y1, size, draw):
    """Deck plates: draw(px, py) paints the size x size plate at px, py. Like a plank, render() lights a plate
    whole, at its middle, with no brushwork: the light steps from plate to plate."""
    for py in range(y0, y1, size):
        for px in range(x0, x1, size):
            draw(px, py)
            rows, cols = slice(py, min(py + size, y1)), slice(px, min(px + size, x1))
            plank['id'][rows, cols] = len(SHIFT); plank['top'][rows, cols] = py + size // 2 - 3
            SHIFT.append(0)
    plank['mat'][y0:y1, x0:x1] = np.asarray(mat)[y0:y1, x0:x1]; plank['lvl'][y0:y1, x0:x1] = np.asarray(lvl)[y0:y1, x0:x1]


def sign(x, y):
    with prop(cast=(1, 2)):
        R(x, y, 20, 15, METAL, 1.4); R(x + 9, y - 3, 1, 3, METAL, 2)
        R(x + 4, y + 5, 9, 7, TEAL + FLAT, 4); R(x + 6, y + 5, 5, 5, METAL + FLAT, 1); R(x + 13, y + 6, 3, 1, TEAL + FLAT, 4)       # a cup,
        R(x + 15, y + 6, 1, 4, TEAL + FLAT, 4); R(x + 13, y + 9, 3, 1, TEAL + FLAT, 4)
        R(x + 6, y + 2, 1, 2, RED + FLAT, 5); R(x + 9, y + 1, 1, 3, RED + FLAT, 5)                                                 # steaming
    light(1 if EVE else .7, 3, [(x - 4, y - 3), (x + 24, y - 2), (x + 25, y + 19), (x - 3, y + 21)])
    if EVE:
        light(.6, 4, [(x - 6, y + 12), (x + 22, y + 10), (x + 32, y + 42), (x - 8, y + 44)])


def fairy_lights(strands=((120, 14, 144, 16, 7), (190, 16, 212, 19, 6), (232, 20, 264, 15, 8))):
    bulbs = []
    for x0, y0, x1, y1, sag in strands:
        seg = [(round(x0 + (x1 - x0) * t / 12), round(y0 + (y1 - y0) * t / 12 + sag * (1 - (t / 6 - 1) ** 2))) for t in range(13)]
        L(seg, METAL, 1.2); bulbs += seg[1:-1:2]
        if EVE:                                                 # a wash on the wall under each strand
            light(.6, 4, [(x0 - 4, y0 + 2), (x1 + 4, y1 + 2), (x1 + 8, y1 + 26), (x0 + 2, y0 + 30)])
    for i, (x, y) in enumerate(bulbs):
        R(x, y + 1, 2, 2, (FLOOR, RED, FLOOR, TEAL)[i % 4] + FLAT, (6, 5, 5, 5)[i % 4])
    light(1 if EVE else .7, 2.5, lambda d: [d.ellipse((x - 4, y - 3, x + 5, y + 6), fill=255) for x, y in bulbs])


TOWN = ((0, 26, 5, 2), (4, 21, 6, 1), (11, 28, 5, 2), (15, 19, 6, 1), (22, 25, 7, 2))    # the skyline: x, top, width, tone


def window(x, y, blind=(5, 3), sun=True, sill=True, town=TOWN):
    sky = ((0, 12, TEAL, 3), (10, 6, TEAL, 4), (15, 5, TEAL, 5), (19, 15, FLOOR, 5), (27, 7, RED, 5)) if not EVE else \
          ((0, 10, METAL, 1), (9, 8, TEAL, 1), (16, 7, TEAL, 2), (22, 5, RED, 2), (26, 4, RED, 3), (29, 5, RED, 4))     # dusk
    with prop(cast=(2, 3)):
        R(x, y, 68, 40, PAPER, 4.2); R(x + 66, y, 2, 40, PAPER, 3); R(x + 4, y + 30, 5, 1, PAPER, 3); R(x + 50, y + 2, 7, 1, PAPER, 3)
        for n, px in enumerate((x + 3, x + 36)):
            R(px - 1, y + 2, 31, 36, PAPER, 2)
            for dy, h, m, l in sky:
                R(px, y + 3 + dy, 29, h, m + FLAT, l)
            for bx, by, bw, m in town:
                bx = bx if n == 0 else 29 - bx - bw
                R(px + bx, y + by, bw, 37 - by, METAL + FLAT, m - EVE)
                for wy in range(by + 2, 36, 3 - EVE):           # more windows are lit in the evening
                    if (wy + bx) % 2:
                        R(px + bx + 1 + (wy % 2) * 2, y + wy, 1, 1, FLOOR + FLAT, 5)
        if sun and not EVE:
            E(x + 8, y + 16, 9, 9, FLOOR + FLAT, 6)                                                   # the sun
        for i in range(blind[0]):                               # a blind, half down and not level
            R(x + 3, y + 3 + 3 * i, 29, 2, PAPER, 4.4 - (i % 2) * .6)
        for i in range(blind[1]):
            R(x + 36, y + 3 + 3 * i, 29, 2, PAPER, 4.4 - (i % 2) * .6)
        cord = 3 + 3 * blind[1]
        R(x + 36, y + cord, 14, 1, PAPER, 3.6); R(x + 61, y + cord, 1, 14, PAPER, 4); R(x + 60, y + cord + 14, 3, 2, PAPER, 4.6)
    if sill:
        with prop(cast=(1, 1)):                                 # on the sill: cactus, mug, two books
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
    with prop(cast=(1, 1)):                                      # a picture light: the board is a thing to press
        R(x + 21, y - 5, 2, 4, METAL, 2); R(x + 13, y - 2, 18, 2, FLOOR, 4.6); R(x + 14, y, 16, 1, FLOOR + FLAT, 6)
    light(1 if EVE else .7, 2, [(x + 10, y), (x + 34, y), (x + 48, y + 29), (x - 3, y + 30)])
    with prop(cast=(1, 1), rim=0):                               # two photos
        R(x + 24, y + 4, 11, 10, PAPER, 5.4); R(x + 25, y + 5, 9, 6, TEAL, 4.5); R(x + 25, y + 9, 9, 2, GREEN, 3.5); R(x + 31, y + 6, 2, 2, FLOOR, 6.5)
        R(x + 36, y + 3, 8, 9, PAPER, 5.2); R(x + 37, y + 4, 6, 5, RED, 3.5); R(x + 39, y + 5, 2, 3, CARD, 5.5)
    for px, py, m in ((8, 4, RED), (18, 3, TEAL), (29, 4, RED), (16, 12, FLOOR), (38, 15, TEAL), (9, 15, RED), (40, 3, FLOOR)):
        R(x + px, y + py, 2, 2, m, 5.5); R(x + px + 1, y + py + 1, 1, 1, m, 3.5)          # pins
    L([(x + 9, y + 5), (x + 17, y + 13), (x + 30, y + 5)], RED, 4.5)                           # a thread between pins
    # notes that no longer fit on the board
    note(x - 9, y + 4, 7, 7, FLOOR, 5.2); note(x - 12, y + 13, 8, 7, TEAL, 4.4); note(x - 6, y + 22, 7, 6, RED, 5)
    note(x + 48, y + 20, 7, 7, FLOOR, 5.4); note(x + 49, y + 29, 6, 6, PAPER, 5, 1)


def clock(x, y):
    with prop(cast=(2, 3)):
        E(x, y, 20, 20, RED, 3.4); E(x + 2, y + 2, 16, 16, PAPER, 5); E(x + 4, y + 5, 13, 12, PAPER, 5.5)
        for tx, ty in ((9, 3), (9, 16), (3, 9), (16, 9)):
            R(x + tx, y + ty, 1, 1, PAPER, 2.4)
        R(x + 9, y + 5, 1, 5, METAL, .6); R(x + 10, y + 9, 4, 1, METAL, .6); R(x + 9, y + 9, 1, 1, RED, 4.5)


def socket(x, y):
    with prop(cast=(1, 1)):                                      # socket and switch
        R(x, y, 7, 8, PAPER, 4.6); R(x + 2, y + 2, 1, 2, PAPER, 2); R(x + 4, y + 2, 1, 2, PAPER, 2); R(x + 2, y + 5, 3, 1, PAPER, 2)


def poster(x, y, sock=(124, 46)):
    with prop(cast=(1, 2), rim=0):
        R(x, y, 22, 30, PAPER, 5); R(x + 1, y + 1, 20, 28, RED, 2.5); E(x + 6, y + 5, 11, 11, FLOOR, 5.5)
        G([(x + 1, y + 28), (x + 8, y + 15), (x + 13, y + 22), (x + 17, y + 17), (x + 20, y + 23), (x + 20, y + 28)], TEAL, 2.5)
        G([(x + 1, y + 28), (x + 5, y + 22), (x + 10, y + 28)], TEAL, 3.5)
        G([(x + 16, y + 29), (x + 21, y + 29), (x + 21, y + 24)], PAPER, 3.4)                      # a corner that curls
    R(x + 9, y - 1, 4, 3, PAPER, 5.6); R(x - 1, y + 26, 3, 3, PAPER, 5.6)                             # tape
    with prop(cast=(1, 1)):                                      # calendar
        R(x - 46, y + 12, 13, 15, PAPER, 5.2); R(x - 46, y + 12, 13, 4, RED, 4)
        for i in range(9):
            R(x - 44 + 4 * (i % 3), y + 18 + 3 * (i // 3), 2, 1, PAPER, 3)
        R(x - 40, y + 21, 2, 1, RED, 4.5)
    if sock:
        socket(*sock)


def book_row(x, base, end, rnd, lo=9, hi=16):
    while x < end:
        w, h, m, l = rnd.randrange(3, 6), rnd.randrange(lo, hi), rnd.choice((RED, TEAL, GREEN, CARD, PAPER, METAL, FLOOR, RED, DESK)), rnd.choice((3, 3.4, 4))
        R(x, base - h, w, h, m, l); R(x + w - 1, base - h, 1, h, m, l - 1.2); R(x, base - h, w, 1, m, l + .8)
        if w > 3:
            R(x + 1, base - h + 2, w - 2, 2, m, l + 1.6)
        x += w


def bookshelf(x, y, seed=8):
    rnd = random.Random(seed)
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


def plant(x, y, extras=True):
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
    if not extras:
        return
    with prop(cast=(1, 2)):                                      # a small pot beside it, a watering can
        R(x + 30, y + 12, 9, 8, PAPER, 4.4); R(x + 37, y + 12, 2, 8, PAPER, 3.4); E(x + 29, y + 5, 7, 6, GREEN, 3.8); E(x + 34, y + 4, 7, 7, GREEN, 3); E(x + 32, y + 8, 6, 5, GREEN, 4.2)
    with prop(cast=(2, 2)):
        R(x + 42, y + 8, 11, 11, TEAL, 3.2); R(x + 50, y + 8, 3, 11, TEAL, 2.2); L([(x + 53, y + 14), (x + 59, y + 9)], TEAL, 3.2, 2); R(x + 58, y + 7, 4, 3, TEAL, 3.8)
        L([(x + 42, y + 10), (x + 39, y + 12), (x + 42, y + 16)], TEAL, 2.4)
    R(x + 30, y + 26, 5, 3, GREEN, 3); R(x + 31, y + 27, 3, 1, GREEN, 2); R(x - 3, y + 24, 4, 2, GREEN, 2.6)   # fallen leaves


def fridge(x, y):
    with prop(cast=(3, 4)):
        R(x, y, 26, 10, PAPER, 4.4); R(x, y + 10, 26, 32, PAPER, 3.6); R(x + 23, y + 10, 3, 32, PAPER, 2.6); R(x, y + 21, 26, 1, PAPER, 2.2)
        R(x + 19, y + 13, 2, 6, METAL, 2); R(x + 19, y + 24, 2, 11, METAL, 2); R(x + 1, y + 40, 24, 2, METAL, 1.4)
        for mx, my, m in ((3, 13, RED), (9, 15, TEAL), (4, 25, FLOOR), (13, 26, RED), (5, 35, GREEN)):          # magnets
            R(x + mx, y + my, 3, 3, m, 4.5)
        R(x + 9, y + 29, 7, 8, PAPER, 5.4); R(x + 10, y + 31, 5, 1, PAPER, 3); R(x + 10, y + 33, 4, 1, PAPER, 3); R(x + 11, y + 29, 2, 1, TEAL, 4.5)
    with prop(cast=(1, 2)):                                      # kettle and two mugs on top
        R(x + 2, y - 6, 9, 10, METAL, 4); R(x + 9, y - 6, 2, 10, METAL, 3); R(x + 3, y - 8, 6, 2, METAL, 2.4); R(x + 11, y - 3, 3, 1, METAL, 2.4); R(x + 13, y - 3, 1, 5, METAL, 2.4); R(x + 3, y - 4, 1, 6, METAL, 5.4)
    with prop(cast=(1, 1)):
        R(x + 16, y, 6, 6, RED, 4); R(x + 16, y - 4, 6, 4, TEAL, 4); R(x + 20, y - 4, 2, 10, METAL, 2)


def box(x, y, w, d, h, tone=0, label=None):
    with prop(cast=(3, 4)):
        R(x, y, w, d, CARD, 4.2 + tone); R(x, y + d, w, h, CARD, 3.2 + tone); R(x + w - 2, y + d, 2, h, CARD, 2.4 + tone)
        R(x + 2, y + d + h - 3, 6, 1, CARD, 2.4 + tone)
        R(x + w // 2 - 2, y, 4, d + 5, PAPER, 4.6); R(x, y + d // 2, w, 1, CARD, 3)               # tape
        if label:
            R(x + label, y + d + 3, 8, 6, PAPER, 5); R(x + label + 1, y + d + 5, 5, 1, PAPER, 3); R(x + label + 1, y + d + 7, 3, 1, RED, 4.5)


def crate(x, y):
    with prop(cast=(2, 3)):                                      # a crate of rolled paper
        R(x, y + 8, 22, 6, DESK, 1.4); R(x, y + 14, 22, 14, DESK, 3.2); R(x, y + 18, 22, 1, DESK, 2); R(x, y + 23, 22, 1, DESK, 2)
        for i, (m, l) in enumerate(((PAPER, 5), (PAPER, 4.4), (TEAL, 3.6), (PAPER, 5), (RED, 3.6))):
            R(x + 2 + 4 * i, y + (i * 5) % 7, 3, 12 - (i * 5) % 7, m, l); R(x + 4 + 4 * i, y + (i * 5) % 7, 1, 12 - (i * 5) % 7, m, l - 1.2)



def pizza(x, y):
    """An open pizza box on the floor by the wall: the lid stands against the skirting, two slices are gone."""
    with prop(cast=(2, 2)):
        R(x, y, 28, 11, CARD, 3.2); R(x, y + 10, 28, 1, CARD, 2.2); E(x + 9, y + 2, 10, 7, RED, 3.8); E(x + 12, y + 4, 4, 3, PAPER, 5)
        R(x, y + 11, 28, 20, CARD, 3); R(x + 1, y + 12, 26, 18, CARD, 2.2)
        E(x + 3, y + 12, 22, 18, DESK, 3); E(x + 5, y + 14, 18, 14, FLOOR, 3.8)
        for px, py in ((8, 17), (15, 15), (11, 23), (18, 22), (7, 21)):
            R(x + px, y + py, 3, 2, RED, 2.6)
        G([(x + 14, y + 21), (x + 27, y + 14), (x + 27, y + 29), (x + 19, y + 30)], CARD, 2.2)          # the missing slices
        L([(x + 14, y + 21), (x + 5, y + 16)], DESK, 2.8); L([(x + 14, y + 21), (x + 11, y + 28)], DESK, 2.8)
    with prop(cast=(1, 2)):                                      # a paper cup beside it
        R(x + 33, y + 16, 6, 8, PAPER, 5); R(x + 38, y + 16, 1, 8, PAPER, 3.6); R(x + 33, y + 19, 6, 2, RED, 4); R(x + 32, y + 15, 8, 1, PAPER, 5.6)


def rug(x, y, w, h):
    rnd = random.Random(2)
    with prop(cast=None, rim=0):
        for fy in range(y + 1, y + h - 1, 2):
            R(x - 4, fy, 4, 1, PAPER, 4 - (fy % 4) * .2); R(x + w, fy + (fy % 3 == 0), 4 + (fy % 5 == 0), 1, PAPER, 4)
        R(x, y, w, h, RED, 2.25); R(x + 3, y + 3, w - 6, h - 6, FLOOR, 3.3); R(x + 4, y + 4, w - 8, h - 8, RED, 2.25)
        R(x + 7, y + 7, w - 14, h - 14, FLOOR, 3.3); R(x + 8, y + 8, w - 16, h - 16, RED, 3.35)
        for wy in range(y + 10, y + h - 9, 3):
            for wx in range(x + 10 + (wy % 2) * 3, x + w - 10, 6):
                R(wx, wy, 2, 1, RED, 2.25)
        for cx in range(x + 28, x + w - 20, 32):
            for i in range(-9, 10):
                for j in range(-9, 10):
                    d = abs(i) + abs(j)
                    if d <= 9:
                        m, l = ((RED, 2.25) if d in (6, 7) else (RED, 4.2) if d in (2, 3) else (FLOOR, 3.3) if d in (8, 9, 0, 1) else (FLOOR, 4.3))
                        R(cx + i, y + h // 2 + j, 1, 1, m, l)
        for _ in range(12):                                     # threadbare streaks
            T(x + 10 + rnd.randrange(w - 34), y + 9 + rnd.randrange(h - 19), rnd.randrange(5, 13), 1, .8)
    G([(x + w - 13, y + h - 1), (x + w, y + h - 1), (x + w, y + h - 12)], CARD, 3.4); L([(x + w - 13, y + h - 1), (x + w, y + h - 12)], RED, 1.6)     # a corner folded over


def shoe(sx, sy, m):
    with prop(cast=(1, 2)):
        R(sx, sy, 7, 11, m, 3.4 if m == RED else 2); R(sx + 1, sy + 2, 5, 5, m, 1.4); R(sx, sy + 9, 7, 2, PAPER, 4.6); R(sx + 5, sy, 2, 11, m, 2.4 if m == RED else 1.4)


def skateboard(x, y):
    with prop(cast=(2, 2)):
        R(x, y + 3, 34, 8, DESK, 3.4); R(x + 2, y + 2, 30, 10, DESK, 3.4); R(x + 3, y + 4, 28, 6, METAL, 1.6); R(x + 12, y + 5, 6, 4, FLOOR, 5.5); R(x + 22, y + 6, 4, 3, TEAL, 4.5)
        for wx in (x + 5, x + 26):
            R(wx, y, 4, 2, PAPER, 4.6); R(wx, y + 12, 4, 2, PAPER, 4.6)


def doormat(x, y, door=(160, 224), stuff=True):
    """door: the left end of the door gap and the floor's bottom edge."""
    dx, dy = door
    with prop(cast=(1, 1), rim=0):                               # coir, lighter than anything near it: it is a thing to press
        R(x, y, 28, 12, RED, 3.3); R(x + 2, y + 2, 24, 8, FLOOR, 4.3)
        for i in range(24):
            R(x + 2 + i, y + 2 + (i * 3) % 7, 1, 2, FLOOR, 3.5)
        for i in range(-3, 4):
            R(x + 14 + i, y + 3 + abs(i), 1, 7 - 2 * abs(i), RED, 3.6)
    light(1 if EVE else .8, 2, [(dx, dy), (dx + 32, dy), (dx + 40, dy - 20), (dx - 8, dy - 20)])  # light from the corridor
    if EVE:
        light(.7, 4, [(dx - 4, dy - 16), (dx + 36, dy - 16), (dx + 54, dy - 46), (dx - 14, dy - 50)])
    if stuff:
        for sx, sy, m in ((132, 209, RED), (141, 211, RED), (196, 207, METAL), (205, 206, METAL)):      # shoes left at the door
            shoe(sx, sy, m)
        skateboard(254, 210)                                    # along the wall


def desk(x, y):
    with prop(cast=(3, 4)):
        R(x, y + 30, 6, 22, DESK, 2.6); R(x + 4, y + 30, 2, 22, DESK, 1.8)                         # left leg panel
        R(x + 6, y + 30, 54, 10, DESK, 1.2); R(x + 6, y + 30, 54, 3, DESK, .4)                     # knee panel, far back
        R(x + 60, y + 30, 36, 20, DESK, 2.8); R(x + 93, y + 30, 3, 20, DESK, 2); R(x + 60, y + 30, 36, 2, DESK, 1.8)
        R(x + 62, y + 50, 5, 2, DESK, 1.6); R(x + 88, y + 50, 5, 2, DESK, 1.6)
        for dy in (32, 41):
            R(x + 63, y + dy, 28, 8, DESK, 1.4); R(x + 64, y + dy + 1, 26, 6, DESK, 3.2); R(x + 64, y + dy + 1, 26, 1, DESK, 4)
            R(x + 73, y + dy + 3, 8, 2, METAL, 4.4); R(x + 73, y + dy + 4, 8, 1, METAL, 2.6)
        R(x + 66, y + 34, 5, 4, FLOOR, 5.5); R(x + 84, y + 43, 4, 4, TEAL, 4.5); R(x + 67, y + 44, 3, 3, RED, 4.5)    # stickers
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
        R(x + 3, y + 6, 3, 1, RED, 4.5)
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
    with prop(cast=(1, 2)):                                      # pen pot
        R(x + 16, y - 2, 7, 8, TEAL, 2.8); R(x + 21, y - 2, 2, 8, TEAL, 1.8)
        for i, m in enumerate((RED, FLOOR, PAPER)):
            R(x + 17 + 2 * i, y - 8 + i % 2, 1, 6, m, 4.4)
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


def power_strip(x, y):
    with prop(cast=(1, 2)):
        R(x, y, 18, 4, PAPER, 4.6); R(x, y + 4, 18, 2, PAPER, 3.2)
        for i in range(4):
            R(x + 2 + 4 * i, y + 1, 2, 2, METAL, 1)
        R(x + 15, y + 1, 2, 2, RED + FLAT, 4)



def backpack(x, y):
    with prop(cast=(3, 3)):                                      # leans on the side of the desk
        R(x + 2, y, 14, 3, METAL, 3.6); R(x, y + 2, 18, 21, METAL, 3); R(x + 15, y + 2, 3, 21, METAL, 2)
        R(x + 6, y - 3, 6, 1, METAL, 1.6); R(x + 6, y - 3, 1, 3, METAL, 1.6); R(x + 11, y - 3, 1, 3, METAL, 1.6)        # grab handle
        R(x + 1, y + 6, 16, 1, METAL, 1.4)                                                                           # zip
        R(x + 3, y + 11, 12, 10, METAL, 3.7); R(x + 3, y + 11, 12, 1, METAL, 1.4); R(x + 13, y + 12, 1, 3, FLOOR, 5.2)  # pocket, zip pull
        R(x + 6, y + 15, 5, 4, RED, 4.2); R(x - 1, y + 4, 2, 16, METAL, 1.6); R(x + 17, y + 4, 2, 16, METAL, 1.6)       # patch, straps


def chair(x, y, hoodie=True):
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
    if not hoodie:
        return
    with prop(cast=(2, 2)):                                      # a hoodie over the back
        G([(x - 2, y + 8), (x + 30, y + 8), (x + 31, y + 15), (x + 22, y + 14), (x + 12, y + 17), (x + 9, y + 28), (x - 3, y + 29)], RED, 3.2)
        R(x - 2, y + 8, 33, 2, RED, 4); L([(x + 3, y + 12), (x + 4, y + 27)], RED, 2.2); L([(x + 9, y + 11), (x + 8, y + 22)], RED, 2.2); L([(x + 20, y + 10), (x + 21, y + 13)], RED, 2.2)
        R(x + 13, y + 11, 1, 5, PAPER, 5); R(x + 16, y + 11, 1, 3, PAPER, 5)


def bin_(x, y, pile=True):
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
    if pile:
        book_pile(x + 66, y + 16)


def book_pile(x, y):
    with prop(cast=(2, 3)):                                      # a pile of books that never made it to the shelf
        for i, (m, w) in enumerate(((GREEN, 20), (RED, 18), (PAPER, 19), (TEAL, 16), (CARD, 18))):
            R(x + i % 2, y + 26 - 4 * i, w, 4, m, 3.2); R(x + i % 2, y + 29 - 4 * i, w, 1, m, 2)
        R(x + 1, y + 3, 16, 7, CARD, 4.2); R(x + 3, y + 5, 6, 3, PAPER, 5); R(x + 11, y, 6, 6, PAPER, 5); R(x + 12, y + 1, 4, 2, DESK, 1.4)


def dog_corner(x, y):
    with prop(cast=(2, 2)):
        E(x, y, 38, 22, RED, 2.6); E(x + 1, y, 36, 19, RED, 3.4); E(x + 5, y + 3, 28, 13, CARD, 4.2); E(x + 8, y + 5, 20, 9, CARD, 3.6)
        R(x + 12, y + 8, 8, 2, PAPER, 5.2); E(x + 10, y + 7, 4, 4, PAPER, 5.2); E(x + 18, y + 7, 4, 4, PAPER, 5.2)    # a bone
    with prop(cast=(1, 2)):
        E(x + 4, y - 14, 14, 9, METAL, 4); E(x + 6, y - 13, 10, 6, CARD, 2.6); R(x + 5, y - 9, 12, 2, METAL, 2.6)
    with prop(cast=(1, 1)):
        E(x + 24, y - 10, 6, 6, TEAL, 4); R(x + 25, y - 9, 2, 2, TEAL, 5.2)                        # a ball


# --- light and render ---------------------------------------------------------------------------------------------
def rgb(c):
    return tuple(bytes.fromhex(c))


LEVELS = [-1, -.5, 0, .5, 1, 1.5]       # the light levels a figure has a sheet for; its sheet on a tile is
                                        # level index * 2 + 1 when the light comes from the right


def standing(total, x, y):
    """The light a figure reads where it stands (x, y: top left of its frame): how bright, and from which side."""
    def mean(x0, y0, x1, y1):
        v = [total[yy * W + xx] for yy in range(max(y0, 0), min(y1, H)) for xx in range(max(x0, 0), min(x1, W))]
        return sum(v) / len(v)
    return mean(x + 8, y + 50, x + 32, y + 64) + .35, mean(x + 26, y + 20, x + 46, y + 64) > mean(x - 6, y + 20, x + 14, y + 64) + .05


def render():
    """The room as drawn since canvas(), lit by every light() so far. -> RGB image; its .light is the light
    level of each pixel, which standing() reads."""
    ambient = -1.65 if EVE else -.85
    rnd = random.Random(6)
    slow = Image.new('L', (W // 18 + 2, H // 5 + 2))            # slow noise, stretched along the boards
    slow.putdata([rnd.randrange(256) for _ in range(slow.width * slow.height)])
    N = slow.resize((W, H), Image.BICUBIC).getdata()
    total = np.full(W * H, ambient)
    for im, amp in lights:
        total += np.asarray(im, np.float64).ravel() * amp / 255
    total = total.tolist()
    M, V, S = mat.getdata(), lvl.getdata(), shd.getdata()
    # a pixel still as boards() drew it is lit as its plank is: at the plank's middle row, SHIFT px along
    on = (plank['id'] > 0) & (plank['mat'] == np.asarray(mat)) & (plank['lvl'] == np.asarray(lvl))
    xs = np.clip(np.arange(W) + np.array(SHIFT)[plank['id']], 0, W - 1)
    lit = np.where(on, np.clip(plank['top'] + 3, 0, H - 1) * W + xs, np.arange(W * H).reshape(H, W)).ravel().tolist()
    on = on.ravel().tolist()
    out = []
    for i in range(W * H):
        m, v = M[i], V[i] / U
        if m and m < FLAT:
            v += total[lit[i]] - S[i] / 255 + (N[i] - 128) / 128 * (0 if on[i] or m in (FLOOR, WOOD) else .3 if m == WALL else .12)   # brushwork on the plaster; planks and plates stay whole
        out.append(rgb(RAMPS[m % FLAT][max(0, min(6, int(v + .5)))] if m else K))
    im = Image.new('RGB', (W, H)); im.putdata(out)
    im.light = total
    return im


# --- the tile grid ------------------------------------------------------------------------------------------------
@contextmanager
def thing(solid=True, tall=False):
    """What is drawn inside is one thing on the tile grid (a desk with all that is on it, a rug): its mask is
    kept, with whether it is solid or flat (may be stood on). What hangs on the wall above the floor is not
    wrapped: rows 0 and 1 are never free. tall: it stands on the tile row of its foot and all of it above
    that row is height, not depth (a lamp, a cabinet seen from the front), so a figure can stand behind it."""
    m0, l0 = mat.copy(), lvl.copy()
    yield
    d = ImageChops.lighter(ImageChops.difference(mat, m0), ImageChops.difference(lvl, l0))
    THINGS.append((d.point(lambda v: 255 * (v > 0)), solid, tall))


def tiles():
    """-> (free tiles as a set of (col, row), upper layer mask), from the things of the last build.
    A figure on a tile has its feet in the tile's lower 20 rows. A floor tile is blocked when solid things cover
    more than half of it, or more than 20% of those rows, or when things that end in the tile (they stand on it,
    a figure would stand on them) cover more than 10% of those rows. The top two rows, the bottom row and the
    first and last columns are wall.
    Upper layer: in a free tile, the pixels of solid things that go on below the tile's bottom edge. Such a thing
    stands in front of a figure on that tile (a chair back, the top of a monitor, a lamp shade), so the game
    draws those pixels over the figures. What a tall thing has above the row of its foot blocks nothing and is
    upper layer wherever the tile is free."""
    COLS, ROWS = W // TILE, H // TILE
    solids, high = [], np.zeros((H, W), bool)
    for mk, solid, tall in THINGS:
        if solid and mk.getbbox():
            a, bottom = np.asarray(mk) > 0, mk.getbbox()[3]
            if tall:
                cut = (bottom - 1) // TILE * TILE
                high[:cut] |= a[:cut]; a = a.copy(); a[:cut] = False
            solids.append((a, bottom))
    free, upper = set(), np.zeros((H, W), bool)
    for row in range(2, ROWS - 1):
        y0, y1 = row * TILE, row * TILE + TILE
        stand, over = np.zeros((TILE, W), bool), np.zeros((TILE, W), bool)
        for a, bottom in solids:
            if bottom > y1:
                over |= a[y0:y1]
            else:
                stand |= a[y0:y1]
        for col in range(1, COLS - 1):
            s, o = stand[:, col * TILE:col * TILE + TILE], over[:, col * TILE:col * TILE + TILE]
            if (s | o).mean() > .5 or (s | o)[12:].mean() > .2 or s[12:].mean() > .1:
                continue
            free.add((col, row)); upper[y0:y1, col * TILE:col * TILE + TILE] = o | high[y0:y1, col * TILE:col * TILE + TILE]
    return free, Image.fromarray(upper.astype(np.uint8) * 255)


def reach(free, start):
    """The free tiles that can be walked to from start."""
    seen, todo = {start}, [start]
    while todo:
        c, r = todo.pop()
        for t in ((c + 1, r), (c - 1, r), (c, r + 1), (c, r - 1)):
            if t in free and t not in seen:
                seen.add(t); todo.append(t)
    return seen


def check(room, free, upper, spots):
    """The room at 2x for review: free tiles green, blocked red, upper layer magenta, the grid, the spots."""
    COLS, ROWS = W // TILE, H // TILE
    tint = Image.new('RGB', (W, H), (200, 40, 40))
    d = ImageDraw.Draw(tint)
    for c, r in free:
        d.rectangle((c * TILE, r * TILE, c * TILE + 31, r * TILE + 31), fill=(40, 200, 80))
    im = Image.blend(room.convert('RGB'), tint, .32)
    im.paste(Image.blend(im, Image.new('RGB', (W, H), (255, 0, 255)), .6), mask=upper)
    im = im.resize((W * 2, H * 2), Image.NEAREST)
    d = ImageDraw.Draw(im)
    for c in range(COLS):
        d.line((c * 64, 0, c * 64, H * 2), fill=(0, 0, 0))
    for r in range(ROWS):
        d.line((0, r * 64, W * 2, r * 64), fill=(0, 0, 0))
        for c in range(COLS):
            d.text((c * 64 + 3, r * 64 + 2), '%d,%d' % (c, r), fill=(255, 255, 255))
    for name, at in spots.items():
        for c, r in (at if isinstance(at[0], list) else [at]):
            d.ellipse((c * 64 + 14, r * 64 + 30, c * 64 + 50, r * 64 + 60), outline=(255, 255, 0), width=3)
            d.text((c * 64 + 16, r * 64 + 38), name, fill=(255, 255, 0))
    return im

