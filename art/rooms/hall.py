# The Hall: the room the world starts in, 1280x736 px (40x23 tiles of 32 px, one art pixel per game pixel), by day
# and in the evening. The style, the palette and the primitives are draw.py's (read its header first), and how a
# room is laid out on the tile grid is the studio's (rooms/studio.py).
# Its look is atomic-age retro-futurist, to sit with the hologram, and warm: a deck of khaki steel plates, a
# two-tone cream and oxblood enamel wall with pipes and portholes, the top doorway a bulkhead, terminals, a
# jukebox, a soda machine, lockers, vinyl and chrome; in the evening the ceiling lights are on. Nothing in it is
# any game's own (no maker's names, marks or mascots).
# What the Hall keeps from the old one (Hall.aseprite): its size, the four doorways (top and bottom in columns 18
# to 21, left in rows 14 to 17, right in rows 3 to 6), the two lounges by the right wall, the plate (once a
# carpet) that says CHECKPOINT REACHED, the hologram in the middle and where its cast stands. The back wall is
# three rows high, so the first row anyone stands on is row 3, as before.
# Its furniture is its own: nothing here is the studio's drawing (#68: the test rooms shared a desk and plants).
# Rebuild: python3 -I art/room.py hall
import math
import random
import draw as m
from draw import (R, E, G, L, T, prop, light, thing, TILE, FLOOR, DESK, WALL, GREEN, METAL, TEAL, CARD, RED, PAPER,
                  FLAT)

W, H = 1280, 736
X0, X1, Y0, Y1 = 16, W - 16, 96, H - 16     # the floor
COLS, ROWS = W // TILE, H // TILE
DOOR_X = (18 * TILE, 22 * TILE)             # the top and bottom doorways, in px
DOOR_LEFT = (14 * TILE, 18 * TILE)          # the side doorways
DOOR_RIGHT = (3 * TILE, 7 * TILE)
# The tiles through the doorways that draw.tiles() would keep as wall (rows 0 and 1, the bottom row, the first and
# last columns). The outermost of them are where the cutscenes that leave the Hall go: doorTop and the rest.
DOORS = ([(c, r) for c in range(18, 22) for r in (0, 1, ROWS - 1)] + [(0, r) for r in range(14, 18)] +
         [(COLS - 1, r) for r in range(3, 7)])
SPOTS = {'hero': [9, 7], 'npcA': [23, 10], 'npcB': [2, 4], 'npcC': [[c, 15] for c in range(4, 10)],
         'hologram': [19, 10],
         'doorTop': [[c, 0] for c in range(18, 22)], 'doorBottom': [[c, ROWS - 1] for c in range(18, 22)],
         'doorLeft': [[0, r] for r in range(14, 18)], 'doorRight': [[COLS - 1, r] for r in range(3, 7)]}

# The carpet's two lines, as woven on the old Hall's carpet (Hall.aseprite, layer CarpetTExt): one cell, 2x2 px here.
TEXT = ('.####..#..##.#####...####.##..#..####....####..#..#...#.#######......####...#####...##....####..#...#.#####..####',
        '#......#..##.#......#.....##.#...#...#.##....#.#..##..#....#.........##..##.#......#..##.#......#...#.##.....#...#',
        '#......#..##.#......#.....##.#...#...#.##....#.#..##..#....#.........##..##.#......#..##.#......#...#.##.....#...#',
        '#......#####.####...#.....###....#...#.##....#.#..#.###....#.........##..##.####...#..##.#......#####.####...#...#',
        '#......#..##.#......#.....###....####..##....#.#..#...#....#.........####...#......#####.#......#...#.##.....#...#',
        '#......#..##.#......#.....##.#...#.....##....#.#..#...#....#.........##..##.#......#..##.#......#...#.##.....#...#',
        '.####..#..##.#####...####.##..#..#.......####..#..#...#....#.........##..##.#####..#..##..####..#...#.#####..####',
        '.####..#..##.#####...####.##..#..#.......####..#..#...#....#.........##..##.#####..#..##..####..#...#.#####..####',
        '', '', '', '', '', '', '',
        '....#...#...####........#....#.####............#..#...#...####.######.......####...#.#....##.#####..#......####',
        '....#...#...####........#....#.####............#..#...#...####.######.......####...#.#....##.#####..#......####',
        '....###.#.##....#........#..#..##..##..........#..#...#.##........#.........#...#..#..##.#...#......#.....#',
        '....#..##.##....#.........##...##..##..........#..#...#...##......#.........#...#..#....#....####...#......###',
        '....#...#.##....#.........##...####............#..#...#.....##....#.........####...#....#....#......#.........#',
        '....#...#.##....#........#..#..##..............#..#...#.....##....#.........#......#..##.#...#......#.........#',
        '....#...#.##....#........#..#..##..............#..#...#.....##....#.........#......#..##.#...#......#.........#',
        '....#...#...####........#....#.##.....#.......#....###..####......#.........#......#.#....##.#####..#####.####...#')


# --- room shell -----------------------------------------------------------------------------------------------
def deck(x0, x1, y0, y1, rnd):
    """Deck plates, 32 px, khaki enamel: a soft seam, a rivet each corner, some with tread, a few patched in
    darker steel or rust-brown, the odd oil stain. Each plate is lit whole (m.plates)."""
    def plate(px, py):
        k = rnd.random()
        mt, l = (CARD, 2.4) if k < .015 else (WALL, 3.1) if k < .04 else (WALL, 3.6 + rnd.choice((0, 0, 0, .12)))
        R(px, py, 32, 32, mt, l); R(px, py, 32, 1, mt, l + .7); R(px, py, 1, 32, mt, l + .5); R(px, py + 31, 32, 1, mt, l - .8); R(px + 31, py, 1, 32, mt, l - .8)
        for rx, ry in ((3, 3), (27, 3), (3, 27), (27, 27)):
            R(px + rx, py + ry, 2, 1, mt, l + 1); R(px + rx, py + ry + 1, 2, 1, mt, l - .9)
        if mt == WALL and rnd.random() < .3:
            for i in range(7, 25, 4):
                for j in range(7, 25, 4):
                    R(px + i + (j // 4) % 2 * 2, py + j, 2, 1, mt, l + .6)
        if rnd.random() < .06:
            ox, oy = px + rnd.randrange(4, 14), py + rnd.randrange(6, 18)
            E(ox, oy, rnd.randrange(10, 16), rnd.randrange(4, 6), mt, l - .7); R(ox + 3, oy + 1, 3, 1, mt, l + .6)
    m.plates(x0, x1, y0, y1, 32, plate)


def worn(pts, w, rnd):
    """A way everyone walks, rubbed shiny: light scuffs along it."""
    for (ax, ay), (bx, by) in zip(pts, pts[1:]):
        n = max(abs(bx - ax), abs(by - ay)) // 3
        for i in range(n):
            x, y = ax + (bx - ax) * i // n, ay + (by - ay) * i // n
            T(x - w // 2 + rnd.randrange(-3, 4), y + rnd.randrange(-2, 3), rnd.randrange(w // 2, w), 1, .45)


def stripes(x, y, w, h, l=4.4):
    """Hazard stripes, amber on the dark, cut square to x, y, w, h."""
    R(x, y, w, h, METAL, 1.2)
    for j in range(h):
        for i in range(w):
            if (i + j) % 12 < 6:
                R(x + i, y + j, 1, 1, FLOOR, l)


def wall(x0, x1, rnd):
    """A stretch of the back wall, two-tone: cream enamel panels above a chrome strip, oxblood below, riveted seams,
    rust running down, a kick plate, a red pipe and a steel one under the ceiling."""
    w = x1 - x0
    R(x0, 8, w, 88, PAPER, 3.9)
    for sx in range(x0 + 24, x1, 48):
        R(sx, 8, 1, 88, PAPER, 2.8); R(sx + 1, 8, 1, 88, PAPER, 4.6)
        for ry in range(30, 54, 8):
            R(sx + 4, ry, 1, 1, PAPER, 2.6); R(sx - 3, ry, 1, 1, PAPER, 2.6)
    R(x0, 58, w, 28, RED, 2.9); R(x0, 58, w, 1, RED, 1.9)
    for sx in range(x0 + 24, x1, 48):
        R(sx, 58, 1, 28, RED, 2)
    for _ in range(w // 40):
        rx = rnd.randrange(x0, x1 - 16)
        E(rx, rnd.randrange(60, 80), rnd.randrange(8, 18), rnd.randrange(3, 6), CARD, 2.6)                   # rust
        if rnd.random() < .4:
            R(rx + 4, 58, 1, rnd.randrange(6, 20), CARD, 2.8)                                                  # a run of it
    R(x0, 55, w, 3, METAL, 4.6); R(x0, 55, w, 1, PAPER, 5.6); R(x0, 57, w, 1, METAL, 2.6)                     # chrome strip
    R(x0, 86, w, 10, METAL, 2.2); R(x0, 86, w, 1, METAL, 4); R(x0, 94, w, 2, METAL, 1.4)                     # kick plate
    for py, c, l in ((11, METAL, 3.4), (18, RED, 3.2)):                                                         # pipes
        R(x0, py, w, 5, c, l); R(x0, py, w, 1, c, l + 1.2); R(x0, py + 4, w, 1, c, l - 1.2)
        for bx in range(x0 + 20, x1 - 4, 96):
            R(bx, py - 1, 4, 7, METAL, 2.6); R(bx, py - 1, 4, 1, METAL, 3.8)


def shell():
    rnd = random.Random(3)
    deck(X0, X1, Y0, Y1, rnd)
    x0, x1 = DOOR_X
    with thing():                               # the back wall is a thing: no one stands in row 2
        wall(X0, x0 - 10, rnd); wall(x1 + 10, X1, rnd)
        for jx in (x0 - 10, x1):                                                                   # the bulkhead's frame
            R(jx, 8, 10, 88, METAL, 2.8); R(jx, 8, 10, 1, METAL, 4); R(jx + (9 if jx < 640 else 0), 8, 1, 88, METAL, 1.8)
            for ry in range(16, 90, 9):
                R(jx + 4, ry, 2, 2, METAL, 4.2); R(jx + 5, ry + 1, 1, 1, METAL, 1.6)
        with prop(cast=(3, 4)):                                                                    # its hatch, swung open
            E(x1 + 12, 20, 30, 72, METAL, 3.2); E(x1 + 15, 24, 22, 64, METAL, 2.6); E(x1 + 18, 28, 4, 56, METAL, 3.6)
            E(x1 + 17, 46, 16, 16, RED, 3.4); E(x1 + 20, 49, 10, 10, METAL, 2.2)
            R(x1 + 24, 47, 2, 14, RED, 4); R(x1 + 18, 53, 14, 2, RED, 4)
    corridor()
    R(0, 0, W, 8, 0, 0); R(0, 0, X0, H, 0, 0); R(X1, 0, W - X1, H, 0, 0); R(0, Y1, W, H - Y1, 0, 0)
    # the side and bottom doorways: the deck runs on through the gap, the wall's ends either side
    m.plates(0, X0, DOOR_LEFT[0], DOOR_LEFT[1], 16, lambda px, py: (R(px, py, 16, 16, WALL, 3.4), R(px, py + 15, 16, 1, WALL, 2.6)))
    m.plates(X1, W, DOOR_RIGHT[0], DOOR_RIGHT[1], 16, lambda px, py: (R(px, py, 16, 16, WALL, 3.4), R(px, py + 15, 16, 1, WALL, 2.6)))
    m.plates(x0, x1, Y1, H, 16, lambda px, py: (R(px, py, 16, 16, WALL, 3.4), R(px + 15, py, 1, 16, WALL, 2.6)))
    for x, (y0, y1) in ((0, DOOR_LEFT), (X1, DOOR_RIGHT)):
        R(x, y0 - 6, X0, 6, METAL, 3.4); R(x, y0 - 6, X0, 1, METAL, 4.4); R(x, y1, X0, 6, METAL, 2.4)
    R(x0 - 8, Y1, 8, H - Y1, METAL, 3); R(x1, Y1, 8, H - Y1, METAL, 2.4)
    side_pipes(18, Y0, DOOR_LEFT[0] - 8); side_pipes(18, DOOR_LEFT[1] + 8, Y1, valve=False)
    T(X0, Y0, X1 - X0, 3, -1)                    # the wall's shadow


def corridor():
    """Through the top doorway: an arch, the corridor's deck going away, a closed bulkhead at its end, lit."""
    x0, x1 = DOOR_X
    rnd = random.Random(21)
    m.plates(x0, x1, 32, Y0, 16, lambda px, py: (R(px, py, 16, 16, WALL, 3.3 + rnd.choice((0, .2))), R(px, py + 15, 16, 1, WALL, 2.4)))
    R(x0, 12, x1 - x0, 20, TEAL, 3.4)
    for i in range(4):
        R(x0, 15 + 4 * i, x1 - x0, 1, TEAL, 2.4)
    with prop(cast=(1, 2)):                     # the far bulkhead, shut
        R(x0 + 46, 12, 36, 19, METAL, 2.6); R(x0 + 48, 14, 32, 17, METAL, 3.2); E(x0 + 57, 16, 14, 12, RED, 3.4); E(x0 + 60, 19, 8, 6, METAL, 2)
    cx, cy, rx, ry = (x0 + x1) / 2, 44, (x1 - x0) / 2 - 2, 36
    for y in range(8, 44):                      # the arch: the frame closes over the top corners
        for x in range(x0, x1):
            if ((x + .5 - cx) / rx) ** 2 + ((y + .5 - cy) / ry) ** 2 > 1:
                R(x, y, 1, 1, METAL, 2.8)
    R(x0 + 46, 8, 36, 7, METAL, 1.4); R(x0 + 48, 9, 32, 4, FLOOR + FLAT, 5)                   # a lit sign over it
    R(x0 + 2, 32, 2, Y0 - 32, METAL, 1.6); R(x1 - 4, 32, 2, Y0 - 32, METAL, 1.6)


def side_pipes(x, y0, y1, valve=True):
    """Pipes down the left wall, a steel run and a red one, bracketed; a valve wheel and a gauge on one stretch."""
    for px, c, l in ((x, METAL, 3.2), (x + 7, RED, 3)):
        R(px, y0, 5, y1 - y0, c, l); R(px, y0, 1, y1 - y0, c, l + 1.3); R(px + 4, y0, 1, y1 - y0, c, l - 1.2)
        for by in range(y0 + 20, y1 - 4, 64):
            R(px - 1, by, 7, 4, METAL, 2.4); R(px - 1, by, 7, 1, METAL, 3.6)
    if valve:
        cy = y0 + 70
        E(x + 5, cy - 7, 14, 14, RED, 3.6); E(x + 8, cy - 4, 8, 8, RED, 1.6)
        L([(x + 12, cy - 6), (x + 12, cy + 6)], RED, 3.6); L([(x + 6, cy), (x + 18, cy)], RED, 3.6)
        E(x - 1, cy + 160, 12, 12, METAL, 3.4); E(x, cy + 161, 10, 10, PAPER, 5); L([(x + 5, cy + 166), (x + 8, cy + 163)], RED, 3)


# --- on the wall ----------------------------------------------------------------------------------------------
def porthole(cx, cy, r=22):
    """A round window in a bolted ring: the sky and the town's roofs, by day or at dusk."""
    with prop(cast=(2, 3)):
        E(cx - r - 5, cy - r - 5, 2 * r + 10, 2 * r + 10, METAL, 3.4); E(cx - r - 3, cy - r - 3, 2 * r + 6, 2 * r + 6, METAL, 4.2)
        E(cx - r, cy - r, 2 * r, 2 * r, TEAL + FLAT, 2 if m.EVE else 4)
        E(cx - r, cy - 2, 2 * r, r + 2, (RED if m.EVE else FLOOR) + FLAT, 3 if m.EVE else 5)
        for bx, top, bw in ((-r + 4, 4, 6), (-r + 12, -2, 5), (-2, 6, 8), (8, 0, 6), (15, 8, 5)):
            R(cx + bx, cy + top, bw, r - top, METAL + FLAT, 1)
            if m.EVE:
                R(cx + bx + 2, cy + top + 3, 1, 1, FLOOR + FLAT, 5)
        if not m.EVE:
            E(cx + 6, cy - 14, 6, 6, PAPER + FLAT, 6)                                            # the sun
        for i in range(12):
            a = i * math.pi / 6
            R(round(cx + (r + 2) * math.cos(a)), round(cy + (r + 2) * math.sin(a)), 1, 1, METAL, 1.6)
        L([(cx - 12, cy - 10), (cx - 4, cy - 16)], PAPER + FLAT, 6)


def sconce(x, y):
    """A caged bulkhead light by the doorway: a steel plate, a glass dome glowing behind bars. x, y: the plate."""
    with prop(cast=(1, 2)):
        R(x - 2, y - 14, 10, 18, METAL, 3.2); R(x - 2, y - 14, 10, 1, METAL, 4.2)
        E(x - 4, y - 12, 14, 14, FLOOR + FLAT, 6); E(x - 1, y - 9, 6, 6, PAPER + FLAT, 6)
        for bx in (-3, 2, 7):
            R(x + bx, y - 12, 1, 14, METAL, 2.2)
        R(x - 4, y - 6, 14, 1, METAL, 2.2)
    light(1 if m.EVE else .5, 2.5, [(x - 8, y - 18), (x + 14, y - 18), (x + 18, y + 4), (x + 3, y + 14), (x - 12, y + 4)])
    if m.EVE:
        light(.7, 5, [(x - 20, y - 14), (x + 26, y - 16), (x + 34, y + 30), (x + 3, y + 46), (x - 28, y + 28)])
        light(.6, 6, [(x - 14, y + 70), (x + 22, y + 66), (x + 36, y + 110), (x - 2, y + 128), (x - 30, y + 104)])


def posters(x, y):
    """Posters taped up close together: a rocket climbing, an atom, a ringed planet over a dome town. 84 x 54."""
    with prop(cast=(1, 2), rim=0):
        R(x, y, 26, 40, TEAL, 3.6); R(x + 1, y + 1, 24, 38, TEAL, 4.2)
        for i in range(5):
            R(x + 3 + 4 * i, y + 30 - i * 3, 2, 1, PAPER, 5)                                    # its trail
        G([(x + 13, y + 6), (x + 17, y + 14), (x + 17, y + 26), (x + 9, y + 26), (x + 9, y + 14)], PAPER, 5)
        R(x + 7, y + 22, 3, 6, RED, 4); R(x + 16, y + 22, 3, 6, RED, 4); R(x + 11, y + 26, 4, 4, FLOOR, 5.4); E(x + 11, y + 13, 4, 4, RED, 4)
        R(x + 3, y + 33, 20, 2, PAPER, 5); R(x + 6, y + 36, 14, 1, PAPER, 4.6)
    with prop(cast=(1, 2), rim=0):
        R(x + 29, y + 4, 24, 30, PAPER, 4.8); R(x + 30, y + 5, 22, 28, PAPER, 5.2)
        orbit(x + 41, y + 17, 9, 4, 0, RED, 3.6); orbit(x + 41, y + 17, 9, 4, 1, TEAL, 3.4); orbit(x + 41, y + 17, 9, 4, 2, METAL, 2.6)
        E(x + 39, y + 15, 5, 5, RED, 4.2); R(x + 32, y + 29, 18, 2, METAL, 2.4)
    with prop(cast=(1, 2), rim=0):
        R(x + 56, y + 2, 28, 34, RED, 3); R(x + 57, y + 3, 26, 32, METAL + FLAT, 1)
        for sx, sy in ((60, 6), (78, 9), (66, 12), (81, 4)):
            R(x + sx, y + sy, 1, 1, PAPER + FLAT, 6)
        E(x + 62, y + 9, 14, 14, FLOOR, 4.6); L([(x + 58, y + 18), (x + 80, y + 13)], PAPER, 5)
        E(x + 58, y + 26, 10, 10, TEAL, 3.4); E(x + 70, y + 24, 12, 12, TEAL, 3.8); R(x + 57, y + 31, 26, 4, TEAL, 2.6)
    for tx, ty in ((-1, -1), (22, -1), (54, 0), (80, 0), (27, 32)):
        R(x + tx, y + ty, 5, 3, PAPER, 5.4)


def orbit(cx, cy, rx, ry, k, c, l):
    """One of an atom's three orbits, the k-th turned by 60 degrees."""
    t = k * math.pi / 3
    L([(round(cx + rx * math.cos(a) * math.cos(t) - ry * math.sin(a) * math.sin(t)),
        round(cy + rx * math.cos(a) * math.sin(t) + ry * math.sin(a) * math.cos(t))) for a in [i * math.pi / 10 for i in range(21)]], c, l)


def starburst(cx, cy):
    """An atomic clock: brass rays round a cream face, two hands."""
    with prop(cast=(1, 2)):
        for i in range(12):
            a = i * math.pi / 6
            L([(cx, cy), (round(cx + 15 * math.cos(a)), round(cy + 15 * math.sin(a)))], FLOOR, 4.4 + (i % 2) * .6)
            E(round(cx + 15 * math.cos(a)) - 1, round(cy + 15 * math.sin(a)) - 1, 3, 3, FLOOR, 5.2)
        E(cx - 7, cy - 7, 14, 14, PAPER, 5); L([(cx, cy), (cx, cy - 5)], METAL, 1.4); L([(cx, cy), (cx + 4, cy + 2)], METAL, 1.4)


def intercom(x, y):
    """A wall panel by the corner: a speaker grille, two gauges, a red call button, a green lamp. 30 x 50."""
    with prop(cast=(2, 3)):
        R(x, y, 30, 50, METAL, 3.2); R(x, y, 30, 2, METAL, 4.4); R(x + 28, y, 2, 50, METAL, 2.2)
        for gy in range(y + 6, y + 22, 3):
            R(x + 5, gy, 20, 1, METAL, 1.6)
        for gx in (5, 16):
            E(x + gx, y + 26, 10, 10, PAPER, 5); L([(x + gx + 5, y + 31), (x + gx + 7 + (gx > 10) * -3, y + 28)], RED, 3)
        E(x + 6, y + 39, 7, 7, RED, 4); R(x + 8, y + 40, 2, 1, RED, 5.4); R(x + 20, y + 41, 4, 3, GREEN + FLAT, 5)
        L([(x + 15, y + 50), (x + 15, y + 56), (x + 22, y + 60)], METAL, 1.6)                  # its handset cord


# --- furniture ------------------------------------------------------------------------------------------------
def wall_bench(x, y):
    """A bench along the wall under the porthole: a channel-tufted teal vinyl back, a seat, chrome legs, a
    magazine left on it. 72 x 39."""
    with prop(cast=(3, 4)):
        R(x, y + 2, 72, 16, TEAL, 3.2); R(x, y + 2, 72, 1, TEAL, 4.2)
        for i in range(7):
            R(x + 5 + 10 * i, y + 4, 1, 13, TEAL, 2.2); R(x + 6 + 10 * i, y + 4, 1, 13, TEAL, 4)
        R(x - 2, y + 18, 76, 10, TEAL, 3.9); R(x - 2, y + 18, 76, 1, TEAL, 4.8); R(x - 2, y + 27, 76, 3, TEAL, 2.4)
        R(x - 2, y + 26, 76, 1, PAPER, 5.6)
        for lx in (4, 64):
            R(x + lx, y + 30, 2, 9, METAL, 4.6); R(x + lx - 2, y + 38, 6, 1, METAL, 3.4)
    with prop(cast=(1, 1), rim=0):
        G([(x + 40, y + 19), (x + 56, y + 18), (x + 57, y + 25), (x + 41, y + 26)], RED, 3.8); R(x + 43, y + 20, 8, 3, PAPER, 5)


def terminal(x, y):
    """A bank of beige terminals: two rounded screens with green lines, a long desk of keys and lamps, a stool's
    worth of cable under it. x, y: the desk's back edge. 104 x 60."""
    with prop(cast=(3, 4)):
        R(x + 4, y + 26, 4, 34, METAL, 2.4); R(x + 96, y + 26, 4, 34, METAL, 1.8)
        R(x, y + 18, 104, 10, CARD, 3.6); R(x, y + 18, 104, 2, CARD, 4.6); R(x + 100, y + 18, 4, 10, CARD, 2.6); R(x, y + 27, 104, 1, CARD, 2.2)
        for i in range(8):
            R(x + 6 + 12 * i, y + 21, 8, 2, CARD, 4.6)
            R(x + 6 + 12 * i, y + 24, 3, 2, (RED, FLOOR, TEAL, GREEN)[i % 4] + FLAT, 4 + (i % 2))
        for k in range(2):
            sx = x + 6 + 50 * k
            R(sx, y - 14, 42, 32, CARD, 4.1); R(sx + 38, y - 14, 4, 32, CARD, 3); R(sx, y - 14, 42, 2, CARD, 5)
            E(sx + 4, y - 10, 30, 22, METAL, 1); E(sx + 5, y - 9, 28, 20, GREEN + FLAT, 2.6)
            for j in range(4):
                R(sx + 9, y - 5 + 4 * j, 6 + (j * 7 + k * 5) % 13, 1, GREEN + FLAT, 5)
            R(sx + 34, y + 10, 2, 2, RED + FLAT, 5)
    T(x + 8, y + 28, 88, 30, -1.2)
    with prop(cast=(1, 1)):
        L([(x + 60, y + 28), (x + 58, y + 50), (x + 70, y + 58)], METAL, 1.2, 2)
    for k in range(2):
        sx = x + 6 + 50 * k
        light(.7 if m.EVE else .2, 3, [(sx, y - 14), (sx + 40, y - 14), (sx + 46, y + 30), (sx - 4, y + 30)])
    if m.EVE:
        light(.6, 6, [(x - 10, y + 20), (x + 114, y + 20), (x + 130, y + 90), (x - 26, y + 90)])


def extinguisher(x, y):
    """A fire extinguisher on its bracket, a hose curled round it. x, y: its foot."""
    with prop(cast=(2, 3)):
        R(x - 2, y - 30, 14, 3, METAL, 2.6)
        R(x, y - 26, 10, 26, RED, 3.6); R(x, y - 26, 3, 26, RED, 4.6); R(x + 8, y - 26, 2, 26, RED, 2.4)
        E(x, y - 30, 10, 6, RED, 4); R(x + 3, y - 34, 4, 5, METAL, 3.8); R(x + 1, y - 18, 8, 6, PAPER, 5)
        L([(x + 7, y - 33), (x + 13, y - 30), (x + 13, y - 10), (x + 10, y - 4)], METAL, 1.4)


def footlocker(x, y):
    """A steel footlocker under the posters: ribbed, bolted corners, a hasp; a folded blanket and magazines on
    the lid. 64 x 32."""
    with prop(cast=(3, 4)):
        R(x, y, 64, 9, GREEN, 3.4); R(x, y + 9, 64, 21, GREEN, 2.6); R(x + 61, y + 9, 3, 21, GREEN, 1.8)
        R(x, y + 9, 64, 1, GREEN, 1.6)
        for ry in (14, 20, 26):
            R(x + 3, ry + y, 58, 1, GREEN, 3.2)
        for bx in (0, 58):
            R(x + bx, y, 6, 30, METAL, 3.6); R(x + bx, y, 6, 1, METAL, 4.6)
        R(x + 28, y + 8, 8, 8, METAL, 4.2); R(x + 31, y + 12, 2, 2, METAL, 1.4)
        R(x + 2, y + 30, 5, 2, METAL, 1.6); R(x + 57, y + 30, 5, 2, METAL, 1.6)
    with prop(cast=(2, 2)):
        R(x + 8, y - 4, 26, 10, RED, 3.6); R(x + 8, y + 4, 26, 2, RED, 2.6)
        for i in range(3):
            R(x + 11 + 8 * i, y - 4, 3, 10, PAPER, 4.8)
    with prop(cast=(1, 2)):
        for i, (c, w) in enumerate(((PAPER, 18), (TEAL, 16), (RED, 17))):
            R(x + 40 + i % 2, y + 3 - 3 * i, w, 3, c, 4); R(x + 40 + i % 2, y + 5 - 3 * i, w, 1, c, 2.8)


def lockers(x, y, n=2, ajar=1):
    """A row of steel lockers by the left wall: vents, a handle, a name card each; one ajar on a red jacket."""
    with prop(cast=(3, 4)):
        for i in range(n):
            lx = x + 22 * i
            R(lx, y, 22, 70, TEAL, 3); R(lx, y, 22, 2, TEAL, 4.2); R(lx + 21, y, 1, 70, TEAL, 1.8); R(lx, y + 68, 22, 2, TEAL, 1.8)
            for v in range(4):
                R(lx + 5, y + 6 + 3 * v, 12, 1, TEAL, 1.6)
            R(lx + 16, y + 32, 2, 8, METAL, 4.4); R(lx + 7, y + 22, 8, 4, PAPER, 4.8)
            if i == ajar:
                R(lx + 1, y + 2, 20, 66, METAL, .8)
                G([(lx + 4, y + 8), (lx + 16, y + 8), (lx + 18, y + 40), (lx + 2, y + 40)], RED, 2.8)
                G([(lx + 20, y + 2), (lx + 28, y + 6), (lx + 28, y + 66), (lx + 20, y + 70)], TEAL, 3.6)
        R(x, y + 70, 22 * n, 3, METAL, 1.4)
    with prop(cast=(1, 2)):                                     # a hard hat left on top
        E(x + 4, y - 7, 16, 9, FLOOR, 4.4); R(x + 2, y - 1, 20, 2, FLOOR, 3.6); E(x + 7, y - 6, 5, 3, FLOOR, 5.4)


def jukebox(x, y):
    """An arched jukebox: bands of coloured light round the record window, a chrome grille. 44 x 74."""
    with prop(cast=(3, 4)):
        R(x, y + 18, 44, 56, DESK, 2.8); E(x, y, 44, 40, DESK, 3.2); R(x + 40, y + 18, 4, 56, DESK, 2)
        E(x + 3, y + 3, 38, 34, FLOOR + FLAT, 5); R(x + 3, y + 20, 38, 50, FLOOR + FLAT, 5)
        E(x + 6, y + 6, 32, 28, RED + FLAT, 4); R(x + 6, y + 20, 32, 48, RED + FLAT, 4)
        E(x + 9, y + 9, 26, 22, TEAL + FLAT, 4.4); R(x + 9, y + 20, 26, 46, TEAL + FLAT, 4.4)
        E(x + 12, y + 12, 20, 16, METAL, 1.4); E(x + 15, y + 15, 14, 10, METAL + FLAT, 1); E(x + 19, y + 18, 6, 4, RED + FLAT, 3)
        R(x + 12, y + 30, 20, 14, PAPER, 4.6)
        for j in range(3):
            R(x + 14, y + 32 + 4 * j, 16, 1, METAL, 2.4)
        R(x + 12, y + 46, 20, 18, METAL, 3.6)
        for gx in range(x + 13, x + 31, 3):
            R(gx, y + 47, 1, 16, METAL, 1.6)
        R(x + 2, y + 72, 6, 2, METAL, 1.6); R(x + 36, y + 72, 6, 2, METAL, 1.6)
    light(1 if m.EVE else .4, 5, [(x - 10, y + 4), (x + 54, y + 4), (x + 70, y + 110), (x - 26, y + 110)])
    if m.EVE:
        light(.6, 9, [(x - 40, y + 60), (x + 84, y + 60), (x + 110, y + 170), (x - 60, y + 170)])


def vending(x, y):
    """A soda machine: a rounded red top with a bottle cap on it (no maker's name), the bottles lit behind
    glass, a coin slot. 40 x 76."""
    with prop(cast=(3, 4)):
        R(x, y + 8, 40, 66, RED, 3.4); E(x, y, 40, 18, RED, 3.8); R(x + 36, y + 8, 4, 66, RED, 2.4)
        R(x + 4, y + 14, 24, 40, PAPER + FLAT, 4.6)
        for r in range(3):
            for c in range(4):
                R(x + 6 + 6 * c, y + 17 + 12 * r, 3, 9, TEAL + FLAT, 4 + (c + r) % 2); R(x + 7 + 6 * c, y + 15 + 12 * r, 1, 2, TEAL + FLAT, 3)
        E(x + 12, y + 2, 16, 10, PAPER, 5); E(x + 15, y + 4, 10, 6, RED, 4.2)
        R(x + 31, y + 18, 3, 8, METAL, 1.6); R(x + 31, y + 30, 3, 3, FLOOR, 5)
        R(x + 4, y + 60, 26, 8, METAL, 1.2); R(x + 4, y + 74, 4, 2, METAL, 1.6); R(x + 32, y + 74, 4, 2, METAL, 1.6)
    with prop(cast=(1, 1)):                                     # an empty bottle on the floor
        R(x + 44, y + 68, 3, 6, TEAL, 4.4); R(x + 45, y + 66, 1, 2, TEAL, 3.6)
    light(.8 if m.EVE else .3, 4, [(x - 4, y + 10), (x + 36, y + 10), (x + 50, y + 90), (x - 10, y + 90)])


def atom_lamp(x, y):
    """A floor lamp on a tripod: three cone shades on one stem. x, y: the middle of its feet."""
    with prop(cast=(3, 3)):
        for dx in (-8, 0, 8):
            L([(x, y - 30), (x + dx, y)], METAL, 1.6)
        L([(x, y - 30), (x, y - 56)], METAL, 3.4, 2)
        for dx, dy in ((-10, -64), (8, -60), (-2, -76)):
            L([(x, y - 54), (x + dx, y + dy + 4)], METAL, 3)
            G([(x + dx - 5, y + dy), (x + dx + 5, y + dy - 2), (x + dx + 2, y + dy + 7)], FLOOR + FLAT, 6)
    light(1 if m.EVE else .4, 4, [(x - 24, y - 84), (x + 22, y - 84), (x + 26, y - 50), (x - 26, y - 50)])
    if m.EVE:
        light(.8, 7, [(x - 50, y - 60), (x + 50, y - 60), (x + 66, y + 20), (x - 66, y + 20)])


def sculpture(x, y):
    """An atom on a white plinth: a red nucleus, three orbits in brass, teal and steel. x, y: the plinth's top
    left."""
    with prop(cast=(3, 4)):
        R(x, y, 26, 5, PAPER, 5); R(x, y + 5, 26, 34, PAPER, 4.2); R(x + 22, y + 5, 4, 34, PAPER, 3.2); R(x, y + 38, 26, 1, PAPER, 2.6)
        R(x + 8, y + 22, 10, 4, FLOOR, 4.6); R(x + 9, y + 23, 8, 1, FLOOR, 3.2)                   # a brass plate
    with prop(cast=(2, 3)):
        R(x + 12, y - 8, 2, 9, METAL, 3.4)
        for k, (c, l) in enumerate(((FLOOR, 4.6), (TEAL, 3.8), (METAL, 3.6))):
            orbit(x + 13, y - 20, 13, 5, k, c, l)
        E(x + 9, y - 24, 9, 9, RED, 3.8); E(x + 10, y - 23, 4, 4, RED, 5)


def bench_seat(x, y):
    """A backless bench in the open floor: red vinyl, channel-tufted, on chrome hairpin legs; a paper left on
    it. 80 x 26."""
    with prop(cast=(3, 4)):
        for lx, d in ((6, -2), (72, 2)):
            L([(x + lx, y + 14), (x + lx + d, y + 26)], METAL, 4.4); L([(x + lx + 3, y + 14), (x + lx + 3 + d, y + 26)], METAL, 3.4)
        R(x, y, 80, 12, RED, 3.6); R(x, y, 80, 1, RED, 4.6); R(x, y + 12, 80, 3, RED, 2.4); R(x + 78, y, 2, 15, RED, 2.4)
        R(x, y + 11, 80, 1, PAPER, 5.6)
        for i in range(7):
            R(x + 10 + 10 * i, y + 2, 1, 9, RED, 2.6)
    with prop(cast=(1, 1), rim=0):
        G([(x + 44, y + 2), (x + 62, y + 1), (x + 64, y + 11), (x + 45, y + 12)], PAPER, 4.8)
        for i in range(3):
            R(x + 47, y + 4 + 2 * i, 14, 1, PAPER, 3.6)


def butler(x, y):
    """A house robot by the front door, switched off: a capsule body, a domed head with a dark visor, arms down,
    on a wheeled base, a dust sheet half off it. x, y: the middle of its base."""
    with prop(cast=(3, 4)):
        E(x - 14, y - 8, 28, 10, METAL, 1.8); R(x - 12, y - 14, 24, 8, METAL, 2.6); R(x - 12, y - 14, 24, 1, METAL, 3.6)
        E(x - 13, y - 56, 26, 46, PAPER, 4.2); E(x - 10, y - 52, 10, 34, PAPER, 5); R(x + 8, y - 46, 4, 28, PAPER, 3.4)
        R(x - 6, y - 40, 12, 8, METAL, 2.2)
        for i in range(3):
            R(x - 4 + 4 * i, y - 38, 2, 2, (RED, FLOOR, TEAL)[i], 2.4)                          # dark lamps: it is off
        for sx in (-1, 1):
            L([(x + sx * 13, y - 46), (x + sx * 17, y - 30), (x + sx * 16, y - 20)], METAL, 3.4, 2)
            E(x + sx * 16 - 3, y - 22, 6, 6, METAL, 2.6)
        R(x - 3, y - 60, 6, 5, METAL, 2.6)
        E(x - 11, y - 78, 22, 20, METAL, 3.6); E(x - 9, y - 77, 8, 6, METAL, 5); R(x - 8, y - 70, 16, 5, METAL, 1)
        L([(x + 6, y - 77), (x + 9, y - 86)], METAL, 3); R(x + 8, y - 88, 3, 3, RED, 3)
    with prop(cast=(1, 2)):                                     # the dust sheet slipping off one shoulder
        G([(x - 14, y - 50), (x - 4, y - 58), (x + 2, y - 50), (x - 6, y - 24), (x - 16, y - 18)], PAPER, 4.8)
        L([(x - 10, y - 50), (x - 12, y - 24)], PAPER, 3.8)


def robot(x, y):
    """A cleaning robot doing its rounds: a dome, an eye, a whip antenna, brushes, a shine behind it. 22 x 16."""
    with prop(cast=None, rim=0):
        T(x - 34, y + 9, 32, 5, .6)
    with prop(cast=(2, 2)):
        E(x, y + 6, 22, 10, METAL, 2.4); E(x + 1, y + 2, 20, 10, METAL, 3.8); E(x + 4, y + 3, 7, 3, METAL, 5)
        R(x + 14, y + 6, 4, 2, RED + FLAT, 5); L([(x + 6, y + 3), (x + 2, y - 10)], METAL, 3); R(x + 1, y - 12, 3, 3, RED + FLAT, 5)
        for bx in (-2, 20):
            R(x + bx, y + 12, 4, 2, FLOOR, 4)


# --- the lounges ----------------------------------------------------------------------------------------------
def checker(x, y, w, h, a, la):
    """Diner linoleum: squares of a colour and cream, a chrome edge, scuffed."""
    with thing(False), prop(cast=None, rim=0):
        R(x - 2, y - 2, w + 4, h + 4, METAL, 4.4); R(x - 2, y + h + 1, w + 4, 1, METAL, 2.4)
        for j in range(0, h, 16):
            for i in range(0, w, 16):
                c, l = (a, la) if (i + j) // 16 % 2 else (PAPER, 4.2)
                R(x + i, y + j, min(16, w - i), min(16, h - j), c, l)
        rnd = random.Random(x + y)
        for _ in range(w * h // 900):
            T(x + rnd.randrange(w - 12), y + rnd.randrange(h), rnd.randrange(4, 12), 1, -.6)


def booth(x, y, c):
    """A curved vinyl sofa, channel-tufted, chrome piping, on stick legs, a cushion in a corner. 96 x 44."""
    with prop(cast=(3, 4)):
        for lx in (8, 86):
            L([(x + lx, y + 34), (x + lx + (-4 if lx < 40 else 4), y + 44)], METAL, 4.6, 2)
        G([(x, y + 8), (x + 10, y), (x + 86, y), (x + 96, y + 8), (x + 96, y + 22), (x, y + 22)], c, 3.4)
        for i in range(8):
            R(x + 9 + 11 * i, y + 3, 1, 18, c, 2.4); R(x + 10 + 11 * i, y + 3, 1, 18, c, 4.2)
        R(x - 2, y + 20, 100, 12, c, 4); R(x - 2, y + 20, 100, 1, c, 5); R(x - 2, y + 31, 100, 3, c, 2.4)
        R(x - 2, y + 30, 100, 1, PAPER, 5.6)
    with prop(cast=(1, 2)):
        G([(x + 14, y + 6), (x + 30, y + 4), (x + 31, y + 18), (x + 15, y + 19)], FLOOR, 4.4)


def tulip(x, y, c):
    """A tulip chair: a moulded cup on one chrome stem and a round foot. 28 x 40."""
    with prop(cast=(3, 3)):
        E(x + 2, y + 34, 24, 6, METAL, 3.6); R(x + 13, y + 20, 3, 16, METAL, 4.6)
        E(x, y, 28, 26, c, 3.2); E(x + 3, y + 2, 22, 18, c, 2); E(x + 4, y + 10, 20, 12, c, 4.2); E(x + 6, y + 11, 8, 4, c, 5.2)


def kidney(x, y, things):
    """A boomerang table on hairpin legs. things: 'tea' (an ashtray, a soda, a magazine) or 'game' (a chess
    board mid-game). 60 x 30."""
    with prop(cast=(3, 4)):
        for lx, dx in ((8, -3), (30, 0), (52, 3)):
            L([(x + lx, y + 10), (x + lx + dx, y + 28)], METAL, 4.4)
        G([(x, y + 4), (x + 18, y), (x + 30, y + 6), (x + 44, y), (x + 60, y + 4), (x + 56, y + 14), (x + 30, y + 12), (x + 4, y + 14)], PAPER, 4.6)
        G([(x, y + 4), (x + 4, y + 14), (x + 30, y + 12), (x + 56, y + 14), (x + 60, y + 4), (x + 60, y + 7), (x + 56, y + 17), (x + 30, y + 15), (x + 4, y + 17), (x, y + 7)], TEAL, 3.4)
    with prop(cast=(1, 2)):
        if things == 'tea':
            E(x + 10, y + 3, 9, 5, METAL, 3.6); R(x + 13, y + 3, 2, 1, RED + FLAT, 5)
            R(x + 40, y - 6, 4, 9, TEAL, 4.4); R(x + 41, y - 9, 2, 3, TEAL, 3.6); R(x + 40, y - 2, 4, 3, RED, 4)
            G([(x + 22, y + 5), (x + 34, y + 4), (x + 35, y + 10), (x + 23, y + 11)], FLOOR, 4.8); R(x + 24, y + 6, 6, 2, RED, 3.6)
        else:
            R(x + 20, y + 2, 16, 9, PAPER, 5)
            for i in range(4):
                for j in range(2):
                    R(x + 20 + 4 * i + 2 * ((j + i) % 2), y + 3 + 4 * j, 2, 2, METAL, 1.8)
            R(x + 23, y - 2, 2, 4, RED, 3.6); R(x + 31, y - 1, 2, 3, METAL, 1.6); R(x + 42, y + 4, 3, 3, RED, 4)


def arc_lamp(x, y, reach):
    """A floor lamp on a tall chrome arc: a spiked globe hangs out over the seats. x, y: the middle of its foot;
    reach: how far the globe is from the pole, left or right."""
    sx, sy = x + reach, y - 66
    with prop(cast=(3, 3)):
        E(x - 8, y - 6, 16, 8, METAL, 3.4); E(x - 7, y - 7, 14, 6, METAL, 4.6)
        L([(x, y - 5), (x, y - 40), (x + reach // 4, y - 66), (x + reach // 2, y - 76), (x + reach * 3 // 4, y - 76), (sx, y - 70)], METAL, 4, 2)
        for i in range(8):
            a = i * math.pi / 4 + .3
            L([(sx, sy + 4), (round(sx + 9 * math.cos(a)), round(sy + 4 + 9 * math.sin(a)))], METAL, 3.6)
        E(sx - 5, sy - 1, 10, 10, FLOOR + FLAT, 6); E(sx - 3, sy + 1, 4, 4, PAPER + FLAT, 6)
    fy = y - 12                                                 # under the globe, on the floor
    light(1 if m.EVE else .5, 2.5, [(sx - 12, sy - 8), (sx + 12, sy - 8), (sx + 16, sy + 14), (sx - 16, sy + 14)])
    if m.EVE:
        light(1, 3, [(sx - 22, fy - 18), (sx + 24, fy - 20), (sx + 34, fy + 6), (sx + 18, fy + 24), (sx - 20, fy + 22), (sx - 32, fy + 2)])
        light(.8, 5, [(sx - 48, fy - 34), (sx + 30, fy - 46), (sx + 64, fy - 6), (sx + 50, fy + 40), (sx - 10, fy + 56), (sx - 60, fy + 26)])
        light(.5, 8, [(sx - 80, fy - 50), (sx + 40, fy - 80), (sx + 100, fy - 10), (sx + 80, fy + 70), (sx - 20, fy + 96), (sx - 96, fy + 40)])


def lounge(x, y, c, floor, things):
    """A booth, a boomerang table, a tulip chair each side, on a square of diner linoleum, and a lamp over them.
    x, y: the linoleum's top left. c: the vinyl; floor: (colour, level) of the dark squares."""
    checker(x, y, 172, 108, *floor)
    with thing():
        booth(x + 38, y - 6, c)
    with thing():
        tulip(x + 8, y + 34, RED if c == TEAL else TEAL)
    with thing():
        tulip(x + 136, y + 34, RED if c == TEAL else TEAL)
    with thing():
        kidney(x + 56, y + 52, things)


# --- the floor ------------------------------------------------------------------------------------------------
def runner(x, y, w, h):
    """The rubber walkway from the top doorway to the hologram: grey ribs between amber edge lines, worn
    pale down the middle."""
    with thing(False), prop(cast=None, rim=0):
        R(x, y, w, h, METAL, 2.2); R(x + 3, y, 3, h, FLOOR, 4.2); R(x + w - 6, y, 3, h, FLOOR, 4.2)
        for ry in range(y + 2, y + h, 4):
            R(x + 9, ry, w - 18, 1, METAL, 2.9)
        rnd = random.Random(8)
        for _ in range(h // 5):
            T(x + w // 2 - 14 + rnd.randrange(24), y + 4 + rnd.randrange(h - 8), rnd.randrange(3, 8), 1, .8)


def deck_ring(cx, cy, w, h):
    """The ring set in the deck round the hologram's plinth: a chrome rim, a hazard band, a dark plate, and a
    teal light pointing to each doorway."""
    with thing(False), prop(cast=None, rim=0):
        for y in range(cy - h // 2, cy + h // 2 + 1):
            for x in range(cx - w // 2, cx + w // 2 + 1):
                r = math.hypot((x - cx) / (w / 2), (y - cy) / (h / 2))
                if r > 1:
                    continue
                if r > .95:
                    R(x, y, 1, 1, METAL, 4.4 if y < cy else 2.6)
                elif r > .8:
                    R(x, y, 1, 1, *((FLOOR, 4.2) if int((math.atan2((y - cy) * w / h, x - cx) + math.pi) * 24 / math.pi) % 2 else (METAL, 1.2)))
                elif r > .76:
                    R(x, y, 1, 1, METAL, 4)
                else:
                    R(x, y, 1, 1, METAL, 2.2)
        for px, py in ((0, -1), (0, 1), (-1, 0), (1, 0)):
            tip = (cx + px * (w // 2 + 12), cy + py * (h // 2 + 10))
            G([tip, (cx + py * 10 + px * (w // 2 + 2), cy - px * 6 + py * (h // 2 + 1)),
               (cx - py * 10 + px * (w // 2 + 2), cy + px * 6 + py * (h // 2 + 1))], TEAL + FLAT, 4.4)


def plate(x, y, w=256, h=96):
    """The checkpoint: a steel plate bolted into the deck, a hazard border, its two lines raised in amber."""
    with thing(False), prop(cast=None, rim=0):
        stripes(x, y, w, h, 4.2)
        R(x + 6, y + 6, w - 12, h - 12, METAL, 2.6); R(x + 6, y + 6, w - 12, 1, METAL, 3.8); R(x + 6, y + h - 7, w - 12, 1, METAL, 1.2)
        for bx in (10, w - 13):
            for by in (10, h - 13):
                E(x + bx, y + by, 4, 4, METAL, 4.4)
        tx, ty = x + (w - 2 * max(map(len, TEXT))) // 2, y + (h - 2 * len(TEXT)) // 2
        for r, row in enumerate(TEXT):
            for c, ch in enumerate(row):
                if ch == '#':
                    R(tx + 2 * c, ty + 2 * r + 1, 2, 2, METAL, 1); R(tx + 2 * c, ty + 2 * r, 2, 2, FLOOR, 4.8)
        rnd = random.Random(9)
        for _ in range(14):
            T(x + 8 + rnd.randrange(w - 30), y + 8 + rnd.randrange(h - 16), rnd.randrange(4, 12), 1, .6)


def sill(x, y, w, h):
    """Hazard stripes on the deck at a doorway."""
    with thing(False), prop(cast=None, rim=0):
        stripes(x, y, w, h)


# --- light ----------------------------------------------------------------------------------------------------
def sun(cx):
    """Sun through a porthole at cx: a round patch under it on the wall, and a long oval out across the deck."""
    light(.5, 2, [(cx - 22, 74), (cx + 22, 74), (cx + 26, 96), (cx - 26, 96)])
    light(1, 2, [(cx - 14, 100), (cx + 14, 100), (cx + 46, 150), (cx + 40, 184), (cx + 16, 190), (cx + 2, 160)])
    light(.5, 4, [(cx - 20, 98), (cx + 20, 98), (cx + 60, 160), (cx + 50, 206), (cx + 6, 206), (cx - 10, 160)])


def room_lights():
    doorways()
    if not m.EVE:
        light(.95, 60, lambda d: d.ellipse((-40, -90, W + 40, H + 60), fill=255))                 # daylight, weaker in the corners
        for cx in PORTHOLES:
            sun(cx)
    else:
        for px in range(200, W, 320):                                                              # the ceiling lights, on
            for py in (230, 520):
                light(.9, 30, lambda d, px=px, py=py: d.ellipse((px - 150, py - 110, px + 150, py + 110), fill=255))
        for cx in PORTHOLES:                                                                       # the last of the dusk
            light(.5, 3, [(cx - 22, 74), (cx + 22, 74), (cx + 28, 96), (cx - 28, 96)])
            light(.4, 9, [(cx - 16, 110), (cx + 40, 106), (cx + 70, 170), (cx + 30, 196), (cx - 16, 170)])




# --- kept from the cosy Hall: they sit as well in this one ------------------------------------------------------
def house_map(x, y):
    """A framed map of the house, drawn by hand: the Hall in the middle, a door on each side, a path to each
    room, a red dot where you stand. 96 x 52."""
    rnd = random.Random(12)
    with prop(cast=(2, 3)):
        R(x, y, 96, 52, DESK, 3.2); R(x + 94, y, 2, 52, DESK, 2.4); R(x + 2, y + 2, 92, 1, DESK, 4)
        R(x + 3, y + 3, 90, 46, CARD, 4.8)
        for _ in range(40):                                                     # old paper
            R(x + 3 + rnd.randrange(88), y + 3 + rnd.randrange(44), rnd.randrange(1, 4), 1, CARD, 4.3)

        def room(rx, ry, rw, rh, l=2.2):
            R(x + rx, y + ry, rw, 1, METAL, l); R(x + rx, y + ry + rh - 1, rw, 1, METAL, l)
            R(x + rx, y + ry, 1, rh, METAL, l); R(x + rx + rw - 1, y + ry, 1, rh, METAL, l)
        room(36, 17, 24, 17, 1.6)                                               # the Hall
        room(40, 5, 16, 8); room(7, 19, 18, 13); room(72, 18, 17, 14); room(38, 39, 20, 8)
        for (ax, ay), (bx, by) in (((48, 17), (48, 13)), ((36, 25), (25, 25)), ((60, 25), (72, 25)), ((48, 34), (48, 39))):
            n = max(abs(bx - ax), abs(by - ay))
            for i in range(0, n + 1, 2):                                        # dotted paths
                R(x + ax + (bx - ax) * i // n, y + ay + (by - ay) * i // n, 1, 1, RED, 3.6)
        E(x + 46, y + 24, 4, 4, RED, 4.2)                                       # you are here
        L([(x + 77, y + 21), (x + 83, y + 28)], RED, 3.6); L([(x + 83, y + 21), (x + 77, y + 28)], RED, 3.6)   # an X
        R(x + 12, y + 23, 8, 1, METAL, 3); R(x + 12, y + 26, 6, 1, METAL, 3); R(x + 42, y + 8, 10, 1, METAL, 3)
        R(x + 84, y + 40, 1, 7, METAL, 2.2); R(x + 81, y + 43, 7, 1, METAL, 2.2); R(x + 84, y + 39, 1, 2, RED, 3.6)   # north
    for tx, ty in ((-1, -1), (90, -1), (-1, 47), (90, 47)):
        R(x + tx, y + ty, 6, 4, PAPER, 5.4)                                     # tape: it was never framed
    R(x, y + 46, 7, 4, CARD, 4)                                                 # a corner that curls


def key_box(x, y):
    """A key cabinet, its door left open: keys on hooks, a tag on each."""
    with prop(cast=(1, 2)):
        R(x, y, 22, 26, DESK, 3.6); R(x + 20, y, 2, 26, DESK, 2.6); R(x + 2, y + 2, 17, 22, DESK, 1.4)
        for i in range(6):
            kx, ky = x + 4 + (i % 3) * 6, y + 4 + (i // 3) * 10
            R(kx, ky, 1, 2, METAL, 4); R(kx - 1, ky + 2, 3, 3, METAL, 4.4 if i % 2 else 3.6); R(kx, ky + 5, 1, 3, METAL, 4)
            R(kx + 1, ky + 3, 2, 3, (RED, TEAL, FLOOR)[i % 3], 4.2)
    with prop(cast=(1, 2)):
        G([(x + 23, y), (x + 30, y + 3), (x + 30, y + 23), (x + 23, y + 26)], DESK, 3); R(x + 27, y + 12, 1, 3, FLOOR, 5)


def monstera(x, y):
    """A monstera in a woven basket: big split leaves on long stems. x, y: the basket's rim."""
    for dx, dy, w, h, l in ((-12, -42, 22, 16, 3.4), (12, -50, 24, 18, 3.8), (-2, -32, 20, 14, 3), (16, -28, 20, 14, 3.2),
                            (-14, -20, 18, 12, 2.8), (2, -60, 18, 14, 4.2), (20, -14, 16, 11, 2.9)):
        with prop(cast=(2, 3), rim=0):
            L([(x + 11, y), (x + dx + w // 2, y + dy + h // 2)], GREEN, 2.4)
            E(x + dx, y + dy, w, h, GREEN, l); E(x + dx + 2, y + dy + 1, w // 2, h // 2, GREEN, l + .8)
            L([(x + dx + w // 2, y + dy + 2), (x + dx + w // 2, y + dy + h - 2)], GREEN, l - 1.2)
            for k in range(3):                                  # the splits
                sy = y + dy + 3 + k * (h - 6) // 2
                L([(x + dx + 1, sy), (x + dx + w // 2 - 3, sy + 1)], GREEN, l - 1.8)
                L([(x + dx + w - 2, sy + 1), (x + dx + w // 2 + 3, sy + 2)], GREEN, l - 1.8)
    with prop(cast=(3, 4)):
        R(x, y, 22, 3, CARD, 4.6); R(x + 1, y + 3, 20, 16, CARD, 3.6); R(x + 18, y + 3, 3, 16, CARD, 2.6)
        for wy in range(y + 4, y + 18, 2):
            for wx in range(x + 1 + (wy // 2) % 2 * 2, x + 18, 4):
                R(wx, wy, 2, 1, CARD, 3)                        # the weave
        R(x + 1, y + 18, 20, 1, CARD, 2.2)


def fig(x, y):
    """A fiddle-leaf fig: a thin trunk, big glossy leaves up it, a concrete pot. x, y: the pot's rim."""
    with prop(cast=(2, 3), rim=0):
        L([(x + 9, y), (x + 10, y - 30), (x + 8, y - 60)], DESK, 2.4, 2)
    for dx, dy, l in ((-9, -34, 3), (10, -30, 3.2), (-11, -50, 3.4), (10, -46, 3.8), (-9, -66, 4), (8, -62, 3.6),
                      (-1, -76, 4.2), (-7, -18, 2.8), (12, -14, 2.9)):
        with prop(cast=(2, 3), rim=0):
            cx = x + 9 + dx
            E(cx - 6, y + dy, 13, 15, GREEN, l); E(cx - 5, y + dy + 5, 11, 12, GREEN, l)
            E(cx - 4, y + dy + 2, 5, 5, GREEN, l + 1); L([(cx, y + dy + 2), (cx, y + dy + 14)], GREEN, l - 1.2)
    with prop(cast=(3, 4)):
        R(x, y, 18, 3, METAL, 4.2); R(x + 1, y + 3, 16, 15, METAL, 3.2); R(x + 14, y + 3, 3, 15, METAL, 2.2); R(x + 1, y + 17, 16, 1, METAL, 1.8)
        for px, py in ((4, 8), (9, 12), (6, 14), (12, 6)):
            R(x + px, y + py, 1, 1, METAL, 2.6)


def vitrine(x, y):
    """A glass cabinet of what the studio is proud of: a trophy, a printed head, a rocket, a camera, records,
    books. Lit inside. 56 x 86."""
    with prop(cast=(3, 4)):
        R(x, y, 56, 6, DESK, 3.8); R(x, y + 6, 56, 78, DESK, 2.8); R(x + 53, y + 6, 3, 78, DESK, 2)
        R(x + 3, y + 8, 50, 72, METAL, 1.2); R(x + 3, y + 8, 50, 2, PAPER + FLAT, 5)
        for sy in (32, 56):
            R(x + 3, y + sy, 50, 2, PAPER, 3.8); R(x + 3, y + sy, 50, 1, PAPER, 4.6)
        E(x + 7, y + 14, 12, 8, FLOOR, 5); E(x + 9, y + 15, 8, 4, FLOOR, 3.6); R(x + 12, y + 21, 2, 6, FLOOR, 4.4); R(x + 9, y + 27, 8, 5, DESK, 3.2)   # trophy
        E(x + 23, y + 12, 13, 15, PAPER, 4.6); R(x + 27, y + 26, 5, 6, PAPER, 4)                                                       # a head,
        for i, c in enumerate((TEAL, RED, FLOOR)):
            R(x + 24, y + 15 + 4 * i, 11, 2, c, 3.8); R(x + 34, y + 15 + 4 * i, 1, 2, c, 5)                                           # tubes for a face
        R(x + 43, y + 14, 5, 15, RED, 3.8); G([(x + 43, y + 14), (x + 45, y + 9), (x + 47, y + 14)], PAPER, 5); R(x + 41, y + 25, 9, 4, RED, 2.8)   # rocket
        R(x + 6, y + 44, 15, 12, METAL, 2.6); E(x + 9, y + 46, 9, 9, METAL, 1); E(x + 11, y + 48, 5, 5, TEAL + FLAT, 3); R(x + 17, y + 42, 3, 2, METAL, 3.6)   # camera
        for i, c in enumerate((RED, PAPER, TEAL)):
            G([(x + 25 + 6 * i, y + 56), (x + 25 + 6 * i, y + 40), (x + 38 + 6 * i, y + 38), (x + 38 + 6 * i, y + 56)], c, 3.4 + (i == 1))  # records
        E(x + 28, y + 43, 7, 7, METAL, 1)
        m.book_row(x + 5, y + 80, x + 50, random.Random(31), 9, 18)
        R(x + 27, y + 8, 2, 72, DESK, 2.4)                                                                                               # the doors
        G([(x + 6, y + 78), (x + 20, y + 10), (x + 23, y + 10), (x + 9, y + 78)], PAPER, 3.2)                                           # glass
        R(x + 2, y + 84, 5, 2, DESK, 1.6); R(x + 49, y + 84, 5, 2, DESK, 1.6)
    light(.8 if m.EVE else .3, 3, [(x + 2, y + 6), (x + 54, y + 6), (x + 56, y + 84), (x, y + 84)])
    if m.EVE:
        light(.5, 5, [(x - 8, y + 80), (x + 64, y + 80), (x + 74, y + 120), (x - 12, y + 122)])


def coat_stand(x, y):
    """A coat stand by the side door: a long coat, a hat, a scarf, a bag. x, y: the middle of its foot."""
    with prop(cast=(3, 3)):
        E(x - 10, y - 4, 20, 7, DESK, 2.4); E(x - 9, y - 5, 18, 5, DESK, 3.2)
        R(x - 1, y - 72, 3, 68, DESK, 3.2); R(x + 1, y - 72, 1, 68, DESK, 2.2)
        for hx, hy in ((-8, -70), (8, -70), (-6, -62), (7, -62)):
            L([(x, y - 66 + (hy + 66) // 2), (x + hx, y + hy)], DESK, 3.4)
        E(x - 2, y - 77, 6, 5, DESK, 4)
    with prop(cast=(2, 3)):                                     # a long coat
        G([(x - 9, y - 68), (x - 2, y - 66), (x, y - 26), (x - 5, y - 20), (x - 15, y - 22), (x - 14, y - 52)], GREEN, 2.8)
        L([(x - 7, y - 64), (x - 9, y - 24)], GREEN, 2); L([(x - 3, y - 60), (x - 2, y - 28)], GREEN, 3.6)
        R(x - 6, y - 52, 1, 1, FLOOR, 5); R(x - 6, y - 44, 1, 1, FLOOR, 5); R(x - 14, y - 50, 2, 26, GREEN, 3.4)
    with prop(cast=(2, 2)):                                     # a bag on the low hook
        L([(x + 4, y - 62), (x + 8, y - 50), (x + 14, y - 58)], CARD, 2.4); R(x + 4, y - 52, 13, 13, CARD, 3.4); R(x + 4, y - 52, 13, 2, CARD, 4.2)
        R(x + 14, y - 50, 3, 11, CARD, 2.4); R(x + 7, y - 47, 6, 4, RED, 4)
    with prop(cast=(1, 2)):                                     # a scarf
        R(x + 5, y - 70, 3, 26, TEAL, 3.2); R(x + 8, y - 68, 3, 20, TEAL, 2.4)
        for i in range(4):
            R(x + 5, y - 66 + 6 * i, 6, 1, PAPER, 5)
    with prop(cast=(1, 2)):                                     # a hat on top
        E(x - 7, y - 78, 16, 6, RED, 3.4); E(x - 4, y - 83, 10, 7, RED, 3.9); R(x - 4, y - 79, 10, 1, METAL, 1.8)


def boots(x, y):
    """A tray of boots by the side door: wellies, trainers, a puddle off them. 44 x 20."""
    with prop(cast=(1, 2)):
        R(x, y + 14, 44, 5, METAL, 2); R(x, y + 14, 44, 1, METAL, 3); R(x + 2, y + 18, 9, 1, TEAL, 3.4)
        for bx, l in ((3, 3.2), (12, 2.8)):
            R(x + bx, y, 7, 15, GREEN, l); R(x + bx, y + 11, 10, 4, GREEN, l); R(x + bx, y, 7, 2, GREEN, l + 1); R(x + bx + 5, y + 2, 2, 9, GREEN, l - .8)
        for bx, c in ((25, PAPER), (33, RED)):
            R(x + bx, y + 7, 9, 7, c, 4.4 if c == PAPER else 3.4); R(x + bx, y + 12, 9, 2, PAPER, 5.2); R(x + bx + 2, y + 8, 4, 1, METAL, 2.2)


def water_cooler(x, y):
    """A water cooler: a blue bottle upside down, a red tap and a blue one, paper cups. x, y: the bottle's top."""
    with prop(cast=(3, 4)):
        E(x + 2, y, 18, 8, TEAL, 4.6); R(x + 2, y + 4, 18, 18, TEAL, 4); R(x + 16, y + 4, 4, 18, TEAL, 3.2); R(x + 4, y + 6, 2, 14, TEAL, 5.4)
        R(x + 2, y + 8, 18, 1, TEAL, 5); R(x + 8, y + 22, 6, 3, TEAL, 3)
        R(x, y + 25, 22, 41, PAPER, 4.2); R(x + 19, y + 25, 3, 41, PAPER, 3.2); R(x, y + 25, 22, 2, PAPER, 5)
        R(x + 4, y + 32, 4, 4, RED, 4); R(x + 13, y + 32, 4, 4, TEAL, 4); R(x + 5, y + 36, 2, 2, METAL, 2); R(x + 14, y + 36, 2, 2, METAL, 2)
        R(x + 3, y + 40, 16, 3, METAL, 2.4); R(x + 2, y + 46, 16, 18, PAPER, 3.8); R(x + 2, y + 46, 16, 1, PAPER, 2.6)
        R(x + 1, y + 66, 20, 1, PAPER, 2)
    with prop(cast=(1, 1)):
        R(x + 22, y + 30, 5, 12, PAPER, 5); R(x + 22, y + 30, 5, 1, PAPER, 5.6); R(x + 26, y + 30, 1, 12, PAPER, 3.8)
    with prop(cast=(1, 1)):
        R(x - 4, y + 64, 3, 4, PAPER, 5); R(x - 2, y + 63, 2, 1, PAPER, 4)    # a cup on the floor


def pedestal(cx, y):
    """The plinth the hologram stands on: a low drum of dark metal, a ring of teal lights, a lens in the middle.
    The hologram over it is the game's (hallHologram.png). cx, y: its middle, its top edge."""
    with prop(cast=(3, 4)):
        E(cx - 42, y + 8, 84, 36, METAL, 1.4); E(cx - 42, y, 84, 36, METAL, 2.6); E(cx - 38, y + 3, 76, 30, METAL, 3.2)
        for i in range(16):
            a = i * math.pi / 8
            R(round(cx + 33 * math.cos(a)), round(y + 18 + 13 * math.sin(a)), 2, 1, TEAL + FLAT, 5)
        E(cx - 16, y + 9, 32, 18, METAL, 2); E(cx - 14, y + 8, 28, 15, METAL, 3.8)
        E(cx - 7, y + 10, 14, 8, TEAL + FLAT, 4); E(cx - 4, y + 11, 8, 5, TEAL + FLAT, 5); R(cx - 1, y + 12, 2, 1, PAPER + FLAT, 6)
        for i in range(9):
            R(cx - 26 + 6 * i, y + 38 - abs(i - 4) // 2, 3, 2, METAL, .8)
    if m.EVE:                                                   # the middle of the hall's light
        light(1, 3, [(cx - 50, y - 8), (cx + 50, y - 8), (cx + 60, y + 30), (cx + 44, y + 54), (cx - 44, y + 54), (cx - 60, y + 30)])
        light(.8, 5, [(cx - 84, y - 22), (cx + 20, y - 40), (cx + 90, y - 10), (cx + 96, y + 60), (cx + 30, y + 90), (cx - 80, y + 76)])
        light(.6, 8, [(cx - 130, y - 30), (cx + 70, y - 60), (cx + 150, y + 10), (cx + 120, y + 120), (cx - 60, y + 140), (cx - 150, y + 70)])
    else:
        light(.5, 3, [(cx - 44, y - 2), (cx + 44, y - 2), (cx + 52, y + 30), (cx - 52, y + 30)])


def ring(cx, cy, r, c, l):
    L([(round(cx + r * math.cos(a * math.pi / 12)), round(cy + r * math.sin(a * math.pi / 12))) for a in range(25)], c, l, 2)


def guest_table(x, y):
    """A round table by the way in: the guest book open with a pen, flowers, a small lamp. x, y: the top's left."""
    with prop(cast=(3, 4)):
        E(x + 14, y + 38, 28, 8, DESK, 2.2); R(x + 26, y + 20, 5, 20, DESK, 2.2); R(x + 28, y + 20, 1, 20, DESK, 1.4)
        E(x, y + 4, 56, 22, DESK, 2.6); E(x, y, 56, 22, DESK, 3.9); E(x + 6, y + 3, 22, 8, DESK, 4.4)
        E(x + 2, y + 14, 52, 14, RED, 3.2); E(x + 4, y + 13, 48, 11, RED, 3.8)                    # a cloth over the front
        for i in range(6):
            R(x + 8 + 8 * i, y + 24 + (i in (0, 5)) * -2, 2, 3, RED, 2.6)
    with prop(cast=(1, 1), rim=0):                              # the guest book, open, and a pen
        G([(x + 20, y + 5), (x + 29, y + 4), (x + 38, y + 5), (x + 38, y + 14), (x + 29, y + 13), (x + 20, y + 14)], PAPER, 5.2)
        R(x + 29, y + 4, 1, 10, PAPER, 3.6)
        for i in range(3):
            R(x + 22, y + 7 + 2 * i, 5 - i % 2, 1, METAL, 2.6); R(x + 31, y + 7 + 2 * i, 4 + i % 2, 1, METAL, 2.6)
        L([(x + 36, y + 13), (x + 42, y + 9)], RED, 3.6)
    with prop(cast=(1, 2)):                                     # flowers
        R(x + 42, y - 6, 6, 10, TEAL, 3.4); R(x + 46, y - 6, 2, 10, TEAL, 2.4)
        for fx, fy, c in ((40, -12, RED), (45, -15, FLOOR), (49, -11, PAPER), (43, -18, RED), (48, -19, FLOOR)):
            R(x + fx, y + fy + 3, 1, 4, GREEN, 3); E(x + fx - 1, y + fy, 4, 4, c, 4.4)
    with prop(cast=(2, 3)):                                     # a small lamp
        R(x + 6, y + 1, 8, 3, METAL, 2.6); R(x + 9, y - 10, 2, 11, METAL, 3.4)
        for i in range(7):
            R(x + 3 + i // 2, y - 18 + i, 14 - i // 2 * 2 + i, 1, FLOOR + FLAT, 6 if i < 5 else 5)
    lx, ly = x + 10, y - 14
    light(1 if m.EVE else .4, 2.5, [(lx - 14, ly - 8), (lx + 14, ly - 8), (lx + 22, ly + 16), (lx - 20, ly + 18)])
    if m.EVE:
        light(1, 3, [(x - 6, y - 4), (x + 50, y - 6), (x + 62, y + 16), (x + 40, y + 34), (x + 4, y + 34), (x - 10, y + 14)])
        light(.8, 5, [(x - 34, y - 6), (x + 40, y - 30), (x + 90, y + 6), (x + 84, y + 58), (x + 20, y + 76), (x - 40, y + 44)])
        light(.5, 8, [(x - 70, y - 30), (x + 50, y - 60), (x + 130, y), (x + 120, y + 100), (x + 20, y + 124), (x - 80, y + 70)])


def vase_plinth(x, y):
    """A lower plinth with a tall glazed vase, beside the sculpture. x, y: the plinth's top left."""
    with prop(cast=(3, 4)):
        R(x, y, 24, 4, PAPER, 5); R(x, y + 4, 24, 22, PAPER, 4.2); R(x + 20, y + 4, 4, 22, PAPER, 3.2); R(x, y + 25, 24, 1, PAPER, 2.6)
    with prop(cast=(2, 3)):
        E(x + 6, y - 20, 12, 18, TEAL, 3.4); E(x + 8, y - 18, 4, 9, TEAL, 4.6); R(x + 9, y - 25, 6, 6, TEAL, 3)
        R(x + 8, y - 26, 8, 2, TEAL, 4); R(x + 7, y - 12, 10, 1, FLOOR, 4.6)


def lost_found(x, y):
    """A crate of what visitors left behind: a ball, a cap, an umbrella, a glove. x, y: the crate's top left."""
    with prop(cast=(2, 3)):
        L([(x + 28, y + 4), (x + 31, y - 18)], METAL, 2.4, 2); R(x + 30, y - 21, 4, 3, RED, 3.6)
        E(x + 4, y - 6, 12, 12, RED, 3.8); E(x + 6, y - 5, 4, 4, RED, 5); L([(x + 5, y - 1), (x + 15, y + 1)], PAPER, 5)
        E(x + 15, y - 3, 12, 8, TEAL, 3.4); R(x + 13, y + 2, 9, 2, TEAL, 2.6)
        R(x, y + 2, 38, 6, DESK, 1.4); R(x, y + 8, 38, 18, DESK, 3.2); R(x, y + 13, 38, 1, DESK, 2); R(x, y + 19, 38, 1, DESK, 2)
        R(x + 35, y + 8, 3, 18, DESK, 2.4); R(x + 12, y + 14, 14, 4, PAPER, 5); R(x + 14, y + 15, 9, 1, METAL, 2.6)
    with prop(cast=(1, 1)):
        R(x + 40, y + 20, 7, 5, CARD, 3.4); R(x + 44, y + 18, 2, 3, CARD, 3.4); R(x + 40, y + 24, 7, 1, CARD, 2.4)


def cable(pts, tape=()):
    with prop(cast=(1, 1), rim=0):
        L(pts, METAL, .8)
    for tx, ty in tape:
        with prop(cast=None, rim=0):
            R(tx, ty, 7, 3, PAPER, 5); R(tx, ty + 2, 7, 1, PAPER, 4)


def litter(rnd, n):
    """What a hall collects: a leaflet, a coin, a leaf off a plant, a receipt, an elastic band."""
    for _ in range(n):
        x, y = rnd.randrange(X0 + 40, X1 - 40), rnd.randrange(Y0 + 40, Y1 - 10)
        k = rnd.randrange(5)
        with prop(cast=(1, 1), rim=0):
            if k == 0:
                R(x, y, 7, 9, PAPER, 5); R(x + 1, y + 1, 5, 3, (RED, TEAL)[x % 2], 4); R(x + 1, y + 6, 4, 1, PAPER, 3.4)
            elif k == 1:
                R(x, y, 3, 2, FLOOR, 5.4); R(x + 1, y + 1, 2, 1, FLOOR, 4)
            elif k == 2:
                R(x, y, 4, 2, GREEN, 3.2); R(x + 1, y + 1, 3, 1, GREEN, 2.2)
            elif k == 3:
                R(x, y, 4, 8, PAPER, 5.2); R(x + 1, y + 2, 2, 1, PAPER, 3.6); R(x + 1, y + 4, 2, 1, PAPER, 3.6)
            else:
                ring(x, y, 2, RED, 3.6)


def doorways():
    """The light that comes in through the four doorways: by day the next rooms are bright, in the evening lit."""
    a, b = (1, .7) if not m.EVE else (.9, .7)
    x0, x1 = DOOR_X
    light(a, 1.5, [(x0 + 2, 18), (x1 - 2, 18), (x1 - 2, 96), (x0 + 2, 96)])                                         # the corridor,
    light(b, 5, [(x0, 96), (x1, 96), (x1 + 20, 156), (x0 - 20, 156)])                             # out of it
    light(a, 2, [(x0, Y1), (x1, Y1), (x1, H), (x0, H)])                                           # the front door
    light(b, 5, [(x0 - 16, Y1 - 60), (x1 + 16, Y1 - 60), (x1, Y1), (x0, Y1)])
    y0, y1 = DOOR_LEFT
    light(a, 2, [(0, y0), (X0, y0), (X0, y1), (0, y1)])
    light(b, 5, [(X0, y0), (X0 + 60, y0 - 14), (X0 + 60, y1 + 14), (X0, y1)])
    y0, y1 = DOOR_RIGHT
    light(a, 2, [(X1, y0), (W, y0), (W, y1), (X1, y1)])
    light(b, 5, [(X1, y0), (X1 - 60, y0 - 8), (X1 - 60, y1 + 14), (X1, y1)])


# --- the room -------------------------------------------------------------------------------------------------
PORTHOLES = (86, 356, 926)


def draw():
    rnd = random.Random(11)
    shell()
    worn([(640, 100), (640, 340)], 60, rnd); worn([(640, 440), (640, 700)], 60, rnd)
    worn([(20, 512), (300, 470), (540, 410)], 40, rnd); worn([(1260, 160), (1000, 260), (740, 370)], 40, rnd)
    # flat: what is on the floor, then the walkway, the ring and the plate over it
    with thing(False):
        litter(rnd, 24)
    runner(612, 108, 56, 228)
    deck_ring(640, 394, 176, 100)
    plate(512, 512)
    sill(DOOR_X[0] - 10, 98, DOOR_X[1] - DOOR_X[0] + 20, 10); sill(20, 486, 16, 54); sill(1244, 134, 16, 54); sill(592, 696, 96, 10)
    with thing(False):
        m.socket(846, 77)
        cable([(682, 402), (720, 404), (760, 396), (800, 380), (830, 340), (846, 280), (850, 200), (850, 120), (849, 96), (849, 84)],
              tape=((716, 402), (836, 330), (846, 220), (847, 150)))
    # the back wall, left to right
    for cx in PORTHOLES:
        with thing():
            porthole(cx, 36)
    house_map(190, 14)
    key_box(424, 26)
    sconce(540, 44); sconce(770, 44)
    posters(784, 14)
    starburst(976, 30)
    intercom(1066, 18)
    # along the back wall
    with thing(tall=True):
        monstera(26, 104)
    with thing():
        wall_bench(52, 86)
    with thing(tall=True):
        atom_lamp(156, 124)
    with thing():
        terminal(410, 78)
    with thing():
        extinguisher(546, 122)
    with thing():
        footlocker(780, 92)
    with thing(tall=True):
        fig(862, 106)
    with thing(tall=True):
        vitrine(1000, 38)
    with thing(tall=True):
        jukebox(1104, 40)
    with thing(tall=True):
        vending(1160, 40)
    # the left wall: lockers, coats, the side door's boots, the boxes in the corner
    with thing(tall=True):
        lockers(36, 212)
    with thing(tall=True):
        coat_stand(48, 348)
    with thing():
        boots(36, 600)
    with thing():
        m.box(38, 668, 30, 10, 26, 0, 10)
    with thing():
        m.box(70, 680, 26, 9, 18, .2, 4); m.box(40, 650, 22, 7, 12, .3, 6)
    # the right wall
    with thing(tall=True):
        water_cooler(1234, 280)
    with thing(tall=True):
        fig(1236, 388)
    # the open floor: a bench by the hero's first steps, the atom, the hologram's plinth, the cleaning robot
    with thing():
        bench_seat(200, 384)
    with thing():
        guest_table(160, 268)
    with thing(tall=True):
        sculpture(900, 210)
    with thing(tall=True):
        vase_plinth(944, 226)
    with thing():
        lost_found(112, 676)
    with thing():
        pedestal(640, 372)
    with thing():
        robot(330, 600)
    # the lounges by the right wall
    lounge(1082, 470, TEAL, (RED, 3.1), 'tea')
    lounge(1082, 598, RED, (TEAL, 3.2), 'game')
    with thing(tall=True):
        arc_lamp(1064, 566, 64)
    with thing(tall=True):
        arc_lamp(1064, 662, 64)
    # by the front door
    with thing(tall=True):
        butler(470, 700)
    with thing():
        m.box(740, 668, 32, 10, 28, 0, 12); m.box(748, 650, 22, 7, 12, .3, 6)
    with thing():
        m.box(776, 684, 28, 9, 16, -.2, 8)


def build(evening):
    m.canvas(W, H, evening)
    draw()
    room_lights()
    return m.render()
