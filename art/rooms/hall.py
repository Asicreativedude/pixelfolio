# The Hall: the room the world starts in, 1280x736 px (40x23 tiles of 32 px, one art pixel per game pixel), by day
# and in the evening. The style, the palette and the primitives are draw.py's (read its header first), and how a
# room is laid out on the tile grid is the studio's (rooms/studio.py).
# What the Hall keeps from the old one (Hall.aseprite): its size, the four doorways (top and bottom in columns 18
# to 21, left in rows 14 to 17, right in rows 3 to 6), the two lounges by the right wall, the carpet that says
# CHECKPOINT REACHED, the hologram in the middle and where its cast stands. The back wall is three rows high, so
# the first row anyone stands on is row 3, as before.
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
def wall(x0, x1, rnd):
    """A stretch of the back wall: plaster in patches, a picture rail, a dado, the skirting."""
    w = x1 - x0
    R(x0, 8, w, 88, WALL, 3.1)
    for _ in range(w // 7):
        pw = rnd.randrange(10, 36)
        E(rnd.randrange(x0, x1 - pw), rnd.randrange(4, 60), pw, rnd.randrange(4, 12), WALL, 3.1 + rnd.choice((-.45, -.3, .3, .45)))
    for _ in range(w // 160):
        E(rnd.randrange(x0, x1 - 40), rnd.randrange(6, 50), rnd.randrange(24, 44), rnd.randrange(12, 20), WALL, 2.6)      # damp
    for _ in range(w // 120):
        cx, cy = rnd.randrange(x0 + 4, x1 - 8), rnd.randrange(10, 56)
        L([(cx, cy), (cx + 2, cy + 6), (cx - 1, cy + 11), (cx + 3, cy + 17)], WALL, 1.6)                                 # cracks
    R(x0, 8, w, 2, WALL, 2)                                                                     # under the ceiling
    R(x0, 22, w, 3, DESK, 3.6); R(x0, 22, w, 1, DESK, 4.4); R(x0, 24, w, 1, DESK, 2.2)          # picture rail
    R(x0, 75, w, 11, WALL, 2.7); R(x0, 74, w, 1, WALL, 4); R(x0, 75, w, 1, WALL, 2)            # dado
    for x in range(x0 + 4, x1 - 2, 9):
        R(x + rnd.randrange(3), 77 + rnd.randrange(8), 2, 1, WALL, 2.3)                         # scuffs
    R(x0, 86, w, 10, DESK, 2.8); R(x0, 86, w, 1, DESK, 4); R(x0, 94, w, 2, DESK, 1.6)          # skirting


def shell():
    rnd = random.Random(3)
    fw = X1 - X0
    m.boards(X0, X1, Y0, Y1, rnd)
    with thing():                               # the back wall is a thing: no one stands in row 2
        wall(X0, DOOR_X[0] - 8, rnd); wall(DOOR_X[1] + 8, X1, rnd)
        for jx, l in ((DOOR_X[0] - 8, 3.2), (DOOR_X[1], 2.6)):                                  # the doorway's jambs
            R(jx, 8, 8, 88, DESK, l); R(jx, 8, 8, 1, DESK, l + 1); R(jx + (7 if jx < 640 else 0), 8, 1, 88, DESK, l - 1)
        R(DOOR_X[0] - 8, 8, 144, 8, DESK, 3.6); R(DOOR_X[0] - 8, 15, 144, 1, DESK, 2.2)          # the lintel
    corridor()
    R(0, 0, W, 8, 0, 0); R(0, 0, X0, H, 0, 0); R(X1, 0, W - X1, H, 0, 0); R(0, Y1, W, H - Y1, 0, 0)
    # the side and bottom doorways: the boards run on through the gap, a sill, the wall's ends either side
    m.boards(0, X0, DOOR_LEFT[0], DOOR_LEFT[1], rnd); m.boards(X1, W, DOOR_RIGHT[0], DOOR_RIGHT[1], rnd)
    m.boards(DOOR_X[0], DOOR_X[1], Y1, H, rnd)
    for x, (y0, y1), sill in ((0, DOOR_LEFT, X0 - 1), (X1, DOOR_RIGHT, X1)):
        R(x, y0 - 6, X0, 6, DESK, 3.4); R(x, y0 - 6, X0, 1, DESK, 4.4); R(x, y1, X0, 6, DESK, 2.4)
        R(sill, y0, 1, y1 - y0, FLOOR, 1.5)
    R(DOOR_X[0] - 8, Y1, 8, H - Y1, DESK, 3); R(DOOR_X[1], Y1, 8, H - Y1, DESK, 2.4); R(DOOR_X[0], Y1, DOOR_X[1] - DOOR_X[0], 1, FLOOR, 1.5)
    T(X0, Y0, fw, 3, -1)                        # the wall's shadow


def corridor():
    """Through the top doorway: the corridor's boards going away, its far wall and the light of the room beyond."""
    x0, x1 = DOOR_X
    rnd = random.Random(21)
    m.boards(x0, x1, 32, Y0, rnd)
    R(x0, 16, x1 - x0, 16, WALL, 2.4); R(x0, 30, x1 - x0, 2, DESK, 1.8)
    with prop(cast=(1, 2)):                     # the far door, ajar: light round it
        R(x0 + 46, 16, 36, 15, DESK, 2.6); R(x0 + 49, 18, 30, 13, DESK, 1.6); R(x0 + 76, 18, 3, 13, FLOOR + FLAT, 5)
    R(x0 + 2, 32, 2, Y0 - 32, DESK, 1.6); R(x1 - 4, 32, 2, Y0 - 32, DESK, 1.6)               # the corridor's skirting


# --- on the wall ----------------------------------------------------------------------------------------------
def sky(x, y, w, h, town):
    """Glass: the sky in bands and a street's roofs, by day or at dusk. town: (x, top, width, tone) a building."""
    bands = (((0, .3, TEAL, 3), (.3, .25, TEAL, 4), (.55, .2, TEAL, 5), (.75, .25, FLOOR, 5)) if not m.EVE else
             ((0, .3, METAL, 1), (.3, .2, TEAL, 1), (.5, .2, TEAL, 2), (.7, .15, RED, 2), (.85, .15, RED, 3)))
    for f, g, c, l in bands:
        R(x, y + round(f * h), w, min(round(g * h) + 1, h - round(f * h)), c + FLAT, l)
    for bx, top, bw, tone in town:
        R(x + bx, y + top, bw, h - top, METAL + FLAT, tone - m.EVE)
        for wy in range(top + 2, h - 1, 3 - m.EVE):                     # more windows are lit at dusk
            if (wy + bx) % 2:
                R(x + bx + 1 + (wy % 2) * 2, y + wy, 1, 1, FLOOR + FLAT, 5)


def hall_window(x, y, town, curtain=RED, cl=3.2):
    """A tall sash window, two panes over two, with a curtain tied back on each side. 52 x 62, the sill included."""
    with prop(cast=(2, 3)):
        R(x, y, 52, 58, PAPER, 4.2); R(x + 50, y, 2, 58, PAPER, 3)
        sky(x + 3, y + 3, 45, 52, town)
        if not m.EVE:
            E(x + 33, y + 10, 8, 8, FLOOR + FLAT, 6)                    # the sun
        R(x + 24, y + 3, 3, 52, PAPER, 4.4); R(x + 26, y + 3, 1, 52, PAPER, 3.2)                  # the bars
        R(x + 3, y + 27, 45, 3, PAPER, 4.6); R(x + 3, y + 29, 45, 1, PAPER, 3.2)
        R(x + 10, y + 31, 6, 1, PAPER, 4.8); R(x + 35, y + 31, 6, 1, PAPER, 4.8)                  # the lifts
    with prop(cast=(2, 3)):
        R(x - 4, y + 58, 60, 4, PAPER, 4.4); R(x - 4, y + 61, 60, 1, PAPER, 2.4)                  # the sill
    with prop(cast=(1, 2)):
        R(x - 12, y - 4, 76, 2, METAL, 3); R(x - 13, y - 5, 3, 4, METAL, 4.2); R(x + 62, y - 5, 3, 4, METAL, 4.2)   # the rod
    for side in (1, -1):
        mid = x + 26
        fx = (lambda px: px) if side == 1 else (lambda px: 2 * mid - px)
        with prop(cast=(2, 3)):
            G([(fx(x - 12), y - 3), (fx(x + 5), y - 3), (fx(x + 3), y + 16), (fx(x - 2), y + 30), (fx(x + 1), y + 46),
               (fx(x + 3), y + 68), (fx(x - 12), y + 68)], curtain, cl)
            for px, top in ((x - 8, -2), (x - 4, 32), (x + 1, -2)):
                L([(fx(px), y + top), (fx(px + (1 if top else 0)), y + (24 if top < 0 else 66))], curtain, cl - .9)
            L([(fx(x - 11), y - 2), (fx(x - 11), y + 66)], curtain, cl + .8)
            R(min(fx(x - 7), fx(x - 1)), y + 28, 7, 3, FLOOR, 4.6)                                  # the tie


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


def sconce(x, y):
    """A wall light by the doorway: a brass plate and arm, a glowing shade. x, y: the plate."""
    with prop(cast=(1, 2)):
        R(x, y, 6, 10, FLOOR, 4.2); R(x + 2, y + 3, 2, 4, FLOOR, 2.6); L([(x + 3, y + 2), (x + 3, y - 4)], FLOOR, 4.4)
        for i in range(8):
            w = 6 + i
            R(x + 3 - w // 2, y - 12 + i, w, 1, FLOOR + FLAT, 6); R(x + 3 - w // 2 + w - w // 3, y - 12 + i, w // 3, 1, FLOOR + FLAT, 5)
    light(1 if m.EVE else .5, 2.5, [(x - 8, y - 18), (x + 14, y - 18), (x + 18, y + 4), (x + 3, y + 14), (x - 12, y + 4)])
    if m.EVE:
        light(.7, 5, [(x - 20, y - 14), (x + 26, y - 16), (x + 34, y + 30), (x + 3, y + 46), (x - 28, y + 28)])
        light(.6, 6, [(x - 14, y + 70), (x + 22, y + 66), (x + 36, y + 110), (x - 2, y + 128), (x - 30, y + 104)])


def gallery(x, y):
    """Frames hung close together: a portrait, a hill, the hero drawn small, a sun, a strip of photos, one
    crooked. 82 x 54."""
    with prop(cast=(1, 2), rim=0):
        R(x, y + 4, 20, 26, DESK, 3); R(x + 2, y + 6, 16, 22, PAPER, 5); E(x + 5, y + 10, 10, 12, CARD, 4.2)
        E(x + 5, y + 8, 10, 6, DESK, 2.2); R(x + 4, y + 21, 12, 7, TEAL, 3)
    with prop(cast=(1, 2), rim=0):
        R(x + 24, y, 30, 20, METAL, 2.4); R(x + 26, y + 2, 26, 16, TEAL, 4)
        G([(x + 26, y + 17), (x + 33, y + 9), (x + 38, y + 13), (x + 44, y + 7), (x + 51, y + 14), (x + 51, y + 17)], GREEN, 3)
        E(x + 43, y + 3, 5, 5, FLOOR, 5.6)
    with prop(cast=(1, 2), rim=0):                              # the hero, drawn small
        R(x + 24, y + 24, 18, 26, PAPER, 4.6); R(x + 26, y + 26, 14, 22, CARD, 5)
        R(x + 30, y + 29, 6, 6, CARD, 4); R(x + 30, y + 28, 6, 2, METAL, 2.6); R(x + 29, y + 35, 8, 6, TEAL, 3.4)
        R(x + 30, y + 41, 2, 4, METAL, 2.2); R(x + 34, y + 41, 2, 4, METAL, 2.2)
    with prop(cast=(1, 2), rim=0):
        R(x + 58, y + 2, 16, 16, RED, 3); R(x + 59, y + 3, 14, 14, PAPER, 5.2); E(x + 61, y + 5, 10, 10, FLOOR, 5); E(x + 64, y + 8, 4, 4, RED, 4)
    with prop(cast=(1, 2), rim=0):
        R(x + 46, y + 24, 12, 30, PAPER, 5.2)
        for i, c in enumerate((TEAL, RED, GREEN)):
            R(x + 48, y + 26 + 9 * i, 8, 7, c, 3.6); R(x + 50, y + 28 + 9 * i, 3, 3, CARD, 4.6)
    with prop(cast=(1, 2), rim=0):
        G([(x + 62, y + 24), (x + 80, y + 27), (x + 77, y + 45), (x + 59, y + 42)], DESK, 3.4)
        G([(x + 64, y + 27), (x + 77, y + 29), (x + 75, y + 42), (x + 62, y + 40)], FLOOR, 4.6)
        G([(x + 65, y + 39), (x + 69, y + 31), (x + 74, y + 40)], RED, 3.6)


def mirror(x, y):
    """A tall mirror in a brass frame: the window across the hall in it, and streaks. 30 x 58."""
    with prop(cast=(2, 3)):
        R(x, y, 30, 58, FLOOR, 4.4); R(x + 28, y, 2, 58, FLOOR, 3.4); R(x, y + 56, 30, 2, FLOOR, 3)
        R(x + 3, y + 3, 24, 52, METAL, 3.4); R(x + 3, y + 3, 24, 18, TEAL, 3.6); R(x + 3, y + 21, 24, 2, PAPER, 4)
        G([(x + 5, y + 44), (x + 15, y + 18), (x + 19, y + 18), (x + 9, y + 44)], PAPER, 4.6)
        G([(x + 13, y + 52), (x + 26, y + 24), (x + 26, y + 30), (x + 16, y + 52)], PAPER, 4.4)
        R(x + 13, y - 4, 4, 4, FLOOR, 4.6)


# --- furniture ------------------------------------------------------------------------------------------------
def settle(x, y):
    """A wooden settle under the window: a high back, two cushions, a book and a scarf left on it. 72 x 39."""
    with prop(cast=(3, 4)):
        R(x, y, 72, 4, DESK, 3.8); R(x, y + 4, 72, 14, DESK, 2.6)
        for i in range(4):
            R(x + 4 + 17 * i, y + 6, 13, 10, DESK, 3.1); R(x + 4 + 17 * i, y + 6, 13, 1, DESK, 3.7); R(x + 16 + 17 * i, y + 6, 1, 10, DESK, 2.2)
        R(x, y + 18, 72, 10, DESK, 3.6); R(x, y + 28, 72, 3, DESK, 2.8); R(x, y + 30, 72, 1, DESK, 1.8)
        R(x + 2, y + 31, 4, 8, DESK, 2.2); R(x + 66, y + 31, 4, 8, DESK, 1.8); R(x + 6, y + 31, 60, 5, DESK, 1)
    with prop(cast=(2, 2)):
        G([(x + 5, y + 8), (x + 22, y + 6), (x + 24, y + 21), (x + 6, y + 23)], TEAL, 3.4); L([(x + 8, y + 10), (x + 21, y + 19)], TEAL, 4.4)
        G([(x + 44, y + 7), (x + 62, y + 8), (x + 61, y + 22), (x + 43, y + 21)], GREEN, 3.6)
        for i in range(3):
            R(x + 46, y + 10 + 4 * i, 14, 1, PAPER, 4.6)
    with prop(cast=(1, 1), rim=0):
        R(x + 28, y + 20, 12, 7, RED, 3.4); R(x + 29, y + 21, 10, 5, PAPER, 5); R(x + 33, y + 20, 1, 7, RED, 2.6)
        L([(x + 50, y + 26), (x + 56, y + 22), (x + 66, y + 27)], FLOOR, 4.6, 2)


def console(x, y):
    """The hall table: a lamp, a bowl for keys, the post, a succulent in a bowl. x, y: the top's back edge."""
    with prop(cast=(3, 4)):
        R(x + 3, y + 18, 4, 22, DESK, 2.6); R(x + 89, y + 18, 4, 22, DESK, 2); R(x + 10, y + 18, 3, 16, DESK, 1.4); R(x + 83, y + 18, 3, 16, DESK, 1.4)
        R(x + 7, y + 31, 82, 2, DESK, 2.4)
        R(x, y, 96, 12, DESK, 3.9); R(x + 94, y + 1, 2, 11, DESK, 3)
        for gx, gy, gw in ((6, 3, 22), (40, 7, 30), (70, 4, 14)):
            R(x + gx, y + gy, gw, 1, DESK, 3.4)
        R(x, y + 12, 96, 6, DESK, 3.1); R(x, y + 17, 96, 1, DESK, 2)
        for dx in (8, 50):
            R(x + dx, y + 13, 38, 4, DESK, 3.5); R(x + dx + 17, y + 14, 4, 1, FLOOR, 5)
    T(x + 7, y + 19, 82, 12, -1.2)
    with prop(cast=(1, 2)):                                     # under it: a basket of slippers
        R(x + 30, y + 22, 26, 9, CARD, 3.6); R(x + 30, y + 22, 26, 1, CARD, 4.4); R(x + 33, y + 20, 8, 3, RED, 3.8); R(x + 44, y + 20, 8, 3, TEAL, 3.4)
    with prop(cast=(2, 3)):                                     # a lamp: a ginger jar, a drum shade
        E(x + 6, y - 7, 14, 14, TEAL, 3.4); E(x + 8, y - 5, 6, 6, TEAL, 4.6); R(x + 12, y - 12, 2, 6, FLOOR, 4.4)
        for i in range(10):
            R(x + 4, y - 23 + i, 18, 1, FLOOR + FLAT, 6 if i < 8 else 5); R(x + 16, y - 23 + i, 6, 1, FLOOR + FLAT, 5)
    with prop(cast=(1, 2)):                                     # the bowl, keys in it
        E(x + 30, y + 1, 16, 8, CARD, 3.4); E(x + 31, y + 1, 14, 5, CARD, 2.4); R(x + 34, y + 2, 4, 2, METAL, 4.6); R(x + 39, y + 1, 3, 3, RED, 4)
    with prop(cast=(1, 1)):                                     # the post, a parcel
        R(x + 50, y + 2, 14, 8, PAPER, 5); R(x + 52, y + 1, 14, 8, PAPER, 4.4); R(x + 53, y + 3, 6, 1, PAPER, 3); R(x + 62, y + 2, 3, 3, RED, 4)
        R(x + 68, y - 6, 15, 12, CARD, 3.6); R(x + 68, y - 6, 15, 3, CARD, 4.4); R(x + 74, y - 6, 2, 12, PAPER, 4.6)
    with prop(cast=(1, 2)):                                     # a succulent
        E(x + 85, y, 10, 7, PAPER, 4.2)
        for i, (dx, h, l) in enumerate(((1, 4, 3.2), (3, 7, 3.8), (5, 6, 3.4), (7, 4, 3))):
            R(x + 85 + dx, y - h + 1, 2, h, GREEN, l); R(x + 85 + dx, y - h + 1, 1, 1, GREEN, l + 1)
    lx, ly = x + 13, y - 18                                     # the lamp's light
    light(1 if m.EVE else .5, 2.5, [(lx - 14, ly - 12), (lx + 14, ly - 12), (lx + 20, ly + 10), (lx - 18, ly + 12)])
    if m.EVE:
        light(1, 3, [(lx - 16, ly + 10), (lx + 34, ly + 10), (lx + 40, ly + 28), (lx - 18, ly + 30)])
        light(.8, 4, [(lx - 26, ly + 22), (lx + 40, ly + 16), (lx + 58, ly + 56), (lx + 20, ly + 84), (lx - 30, ly + 64)])
        light(.5, 7, [(lx - 50, ly + 30), (lx + 50, ly + 8), (lx + 90, ly + 70), (lx + 30, ly + 120), (lx - 46, ly + 96)])


def umbrella_stand(x, y):
    """A tin of umbrellas by the door: a red crook, a black one, a folded teal one. x, y: the tin's rim."""
    with prop(cast=(2, 3)):
        L([(x + 4, y + 2), (x + 3, y - 16)], RED, 3.6, 2); R(x, y - 19, 5, 2, RED, 4); R(x - 1, y - 18, 2, 4, RED, 3.6)
        L([(x + 10, y + 2), (x + 12, y - 20)], METAL, 2.4, 2); R(x + 11, y - 23, 4, 3, DESK, 3.4)
        G([(x + 6, y + 1), (x + 9, y + 1), (x + 8, y - 12), (x + 7, y - 12)], TEAL, 3.4); R(x + 7, y - 15, 1, 3, METAL, 2.6)
        R(x, y, 14, 3, METAL, 4); R(x + 1, y + 3, 12, 17, METAL, 3); R(x + 10, y + 3, 3, 17, METAL, 2); R(x + 1, y + 9, 12, 1, METAL, 2.2)


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


def chest(x, y):
    """A wooden chest under the gallery: a folded blanket and a pile of magazines on the lid. 64 x 32."""
    with prop(cast=(3, 4)):
        R(x, y, 64, 9, DESK, 3.9); R(x, y + 9, 64, 21, DESK, 2.9); R(x + 61, y + 9, 3, 21, DESK, 2.1)
        R(x, y + 9, 64, 1, DESK, 2); R(x + 4, y + 13, 56, 1, DESK, 2.4); R(x + 4, y + 25, 56, 1, DESK, 2.4)
        for bx in (6, 54):
            R(x + bx, y + 9, 4, 21, METAL, 2.6); R(x + bx, y + 9, 1, 21, METAL, 3.6)                  # straps
        R(x + 28, y + 12, 8, 7, FLOOR, 4.6); R(x + 31, y + 15, 2, 2, DESK, 1.4)                     # the lock
        R(x + 2, y + 30, 5, 2, DESK, 1.6); R(x + 57, y + 30, 5, 2, DESK, 1.6)
    with prop(cast=(2, 2)):
        R(x + 4, y - 4, 30, 10, RED, 3.6); R(x + 4, y + 4, 30, 2, RED, 2.6)
        for i in range(4):
            R(x + 6 + 7 * i, y - 4, 3, 10, PAPER, 4.8)
    with prop(cast=(1, 2)):
        for i, (c, w) in enumerate(((PAPER, 20), (TEAL, 18), (RED, 19))):
            R(x + 40 + i % 2, y + 3 - 3 * i, w, 3, c, 4); R(x + 40 + i % 2, y + 5 - 3 * i, w, 1, c, 2.8)


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


def pigeonholes(x, y):
    """The post: a pigeonhole each on a cupboard by the left wall. Letters, a parcel, a magazine, a scarf. 40 x 70."""
    rnd = random.Random(14)
    with prop(cast=(3, 4)):
        R(x, y, 40, 4, DESK, 3.9); R(x, y + 4, 40, 34, DESK, 2.8); R(x + 37, y + 4, 3, 34, DESK, 2)
        for row in range(3):
            for col in range(3):
                cx, cy = x + 3 + 11 * col, y + 6 + 11 * row
                R(cx, cy, 10, 9, DESK, 1); R(cx, cy, 10, 1, DESK, .4)
                k = rnd.randrange(5)
                if k < 2:
                    R(cx + 1, cy + 4, 8, 5, PAPER, 5 - k * .6); R(cx + 2, cy + 3, 6, 6, PAPER, 4.4)
                elif k == 2:
                    R(cx + 1, cy + 3, 8, 6, CARD, 3.8); R(cx + 4, cy + 3, 2, 6, PAPER, 4.6)
                elif k == 3:
                    R(cx + 2, cy + 2, 6, 7, RED, 3.6); R(cx + 3, cy + 3, 4, 2, PAPER, 5)
        L([(x + 26, y + 18), (x + 28, y + 32)], TEAL, 3.4, 2)                   # a scarf hangs out of one
        R(x, y + 38, 40, 32, DESK, 3.2); R(x, y + 38, 40, 2, DESK, 4.2); R(x + 37, y + 38, 3, 32, DESK, 2.2)
        R(x + 19, y + 41, 2, 27, DESK, 2); R(x + 15, y + 52, 2, 3, FLOOR, 5); R(x + 23, y + 52, 2, 3, FLOOR, 5)
        R(x + 2, y + 70, 4, 2, DESK, 1.6); R(x + 34, y + 70, 4, 2, DESK, 1.6)
    with prop(cast=(1, 2)):                                     # a plant on top
        R(x + 26, y - 6, 9, 7, PAPER, 4.4); R(x + 33, y - 6, 2, 7, PAPER, 3.4)
        for lx, ly in ((24, -10), (28, -13), (32, -11), (36, -8), (37, -2), (38, 4), (36, 10)):
            R(x + lx, y + ly, 3, 3, GREEN, 3.4 + (lx % 2) * .8)


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


def sculpture(x, y):
    """A head on a white plinth, tubes for a face. x, y: the plinth's top left."""
    with prop(cast=(3, 4)):
        R(x, y, 26, 5, PAPER, 5); R(x, y + 5, 26, 34, PAPER, 4.2); R(x + 22, y + 5, 4, 34, PAPER, 3.2); R(x, y + 38, 26, 1, PAPER, 2.6)
        R(x + 8, y + 22, 10, 4, FLOOR, 4.6); R(x + 9, y + 23, 8, 1, FLOOR, 3.2)                   # a brass plate
    with prop(cast=(2, 3)):
        R(x + 10, y - 6, 6, 7, CARD, 3.4); E(x + 4, y - 31, 18, 27, CARD, 3.8); E(x + 6, y - 29, 8, 10, CARD, 4.6)
        E(x + 5, y - 33, 16, 7, METAL, 2.4)
        for i, c in enumerate((TEAL, RED, FLOOR, TEAL)):
            R(x + 4, y - 24 + 4 * i, 18, 2, c, 3.6); R(x + 21, y - 24 + 4 * i, 2, 2, c, 5)


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


# --- the lounges ----------------------------------------------------------------------------------------------
def club_chair(x, y, c, l=0, flip=False):
    """A club chair seen from the side, turned to the low table: the back is the slab on its far side, then the
    seat between two arms. flip: it faces left. 36 x 46."""
    def r(dx, dy, w, h, lv, mt=c):
        R(x + (36 - dx - w if flip else dx), y + dy, w, h, mt, lv + l)
    with prop(cast=(3, 4)):
        r(2, 41, 4, 4, 1.6, DESK); r(30, 41, 4, 4, 1.6, DESK)
        r(0, 0, 12, 41, 2.8); r(0, 0, 12, 4, 3.9); r(10, 4, 2, 37, 3.4)
        for i in range(4):
            r(4, 8 + 8 * i, 2, 1, 2); r(8, 12 + 8 * i, 1, 1, 2)                                 # buttons
        r(10, 6, 26, 8, 3.9); r(10, 13, 26, 2, 2.8)                                             # the far arm
        r(10, 15, 24, 14, 3.5); r(14, 20, 14, 1, 3.1)                                           # the seat
        r(10, 27, 26, 8, 4.1); r(10, 35, 26, 6, 2.6); r(10, 35, 26, 1, 3.4)                     # the near arm
    with prop(cast=(1, 2)):
        r(14, 15, 11, 10, 4.6, PAPER); r(15, 17, 9, 1, 3.6, PAPER); r(15, 20, 6, 1, 3.6, PAPER)  # a cushion


def side_table(x, y, things):
    """A round low table, 36 wide. things: what is on it, 'tea' or 'game'."""
    with prop(cast=(3, 4)):
        E(x + 8, y + 26, 20, 6, DESK, 2.2); R(x + 16, y + 14, 4, 14, DESK, 2); R(x + 18, y + 14, 1, 14, DESK, 1.4)
        E(x, y + 3, 36, 16, DESK, 2.6); E(x, y, 36, 16, DESK, 3.9); E(x + 5, y + 3, 14, 6, DESK, 4.3)
    if things == 'tea':
        with prop(cast=(1, 2)):
            R(x + 8, y + 2, 6, 6, PAPER, 5); R(x + 13, y + 3, 2, 2, PAPER, 4.4); R(x + 9, y + 2, 4, 1, DESK, 1.6)
            R(x + 20, y - 4, 6, 9, PAPER, 4.4); R(x + 21, y - 8, 4, 5, GREEN, 3.6); E(x + 19, y - 12, 4, 4, RED, 4.4); E(x + 23, y - 13, 4, 4, FLOOR, 5.2)
            R(x + 16, y + 9, 12, 4, RED, 3.6); R(x + 17, y + 8, 12, 4, PAPER, 4.8)
    else:
        with prop(cast=(1, 1)):
            R(x + 9, y + 2, 16, 10, PAPER, 5)
            for i in range(4):
                for j in range(2):
                    R(x + 9 + 4 * i + 2 * ((j + i) % 2), y + 3 + 4 * j, 2, 2, METAL, 1.8)
            R(x + 12, y - 2, 2, 4, RED, 3.6); R(x + 20, y - 1, 2, 3, METAL, 1.6); R(x + 27, y + 4, 3, 3, RED, 4)


def loveseat(x, y, c, l=0):
    """A two-seat sofa with rolled arms and a buttoned back, facing us. 80 x 46."""
    with prop(cast=(3, 4)):
        R(x + 3, y + 42, 4, 4, DESK, 2); R(x + 73, y + 42, 4, 4, DESK, 1.6)
        R(x + 8, y, 64, 5, c, 3.9 + l); R(x + 8, y + 5, 64, 13, c, 2.7 + l)
        for i in range(7):
            R(x + 13 + 9 * i, y + 9 + (i % 2) * 4, 1, 1, c, 1.8 + l)
        for i in range(2):
            cx = x + 9 + 31 * i
            R(cx, y + 17, 31, 14, c, 3.6 + l); R(cx, y + 17, 31, 1, c, 2.4 + l); R(cx + 30, y + 17, 1, 14, c, 2.8 + l)
            R(cx, y + 31, 31, 7, c, 2.9 + l); R(cx, y + 31, 31, 1, c, 4 + l)
        R(x + 8, y + 38, 64, 4, c, 2 + l)
        for ax, d in ((x, 0), (x + 70, -.4)):
            E(ax, y + 3, 10, 9, c, 4.2 + l + d); R(ax, y + 8, 10, 28, c, 3.6 + l + d); R(ax, y + 36, 10, 6, c, 2.6 + l + d); E(ax + 1, y + 34, 8, 5, c, 3.2 + l + d)
    with prop(cast=(2, 2)):
        G([(x + 12, y + 8), (x + 26, y + 6), (x + 28, y + 19), (x + 13, y + 21)], FLOOR, 4.6); L([(x + 14, y + 10), (x + 26, y + 18)], FLOOR, 3.6)


def arc_lamp(x, y, reach):
    """A floor lamp on a tall arc: the shade hangs out over the seats. x, y: the middle of its foot; reach: how far
    the shade is from the pole, left or right."""
    sx, sy = x + reach, y - 66
    with prop(cast=(3, 3)):
        E(x - 8, y - 6, 16, 8, PAPER, 3.4); E(x - 7, y - 7, 14, 6, PAPER, 4.6)
        L([(x, y - 5), (x, y - 40), (x + reach // 4, y - 66), (x + reach // 2, y - 76), (x + reach * 3 // 4, y - 76), (sx, y - 70)], METAL, 3.4, 2)
        for i in range(7):
            w = 6 + 2 * i
            R(sx - w // 2, sy + i, w, 1, FLOOR + FLAT, 6); R(sx - w // 2 + w - w // 3, sy + i, w // 3, 1, FLOOR + FLAT, 5)
        R(sx - 9, sy + 7, 18, 1, RED + FLAT, 5)
    fy = y - 12                                                 # under the shade, on the floor
    light(1 if m.EVE else .5, 2.5, [(sx - 10, sy - 6), (sx + 10, sy - 6), (sx + 16, sy + 12), (sx - 16, sy + 12)])
    if m.EVE:
        light(1, 3, [(sx - 22, fy - 18), (sx + 24, fy - 20), (sx + 34, fy + 6), (sx + 18, fy + 24), (sx - 20, fy + 22), (sx - 32, fy + 2)])
        light(.8, 5, [(sx - 48, fy - 34), (sx + 30, fy - 46), (sx + 64, fy - 6), (sx + 50, fy + 40), (sx - 10, fy + 56), (sx - 60, fy + 26)])
        light(.5, 8, [(sx - 80, fy - 50), (sx + 40, fy - 80), (sx + 100, fy - 10), (sx + 80, fy + 70), (sx - 20, fy + 96), (sx - 96, fy + 40)])


def lattice_rug(x, y, w, h, a, b, la=3, lb=4.2):
    """A rug with a plain border and a lattice in the field, fringed at both ends."""
    with thing(False), prop(cast=None, rim=0):
        for fy in range(y + 1, y + h - 1, 2):
            R(x - 4, fy, 4, 1, PAPER, 4 - (fy % 4) * .2); R(x + w, fy, 4 + (fy % 5 == 0), 1, PAPER, 4)
        R(x, y, w, h, a, la - .6); R(x + 4, y + 4, w - 8, h - 8, b, lb); R(x + 6, y + 6, w - 12, h - 12, a, la)
        for i in range(x + 6, x + w - 6):
            for j in range(y + 6, y + h - 6):
                if (i - x + j - y) % 12 == 0 or (i - x - (j - y)) % 12 == 0:
                    R(i, j, 1, 1, b, lb - .6)
        rnd = random.Random(x + y)
        for _ in range(w * h // 1200):
            T(x + 8 + rnd.randrange(w - 30), y + 8 + rnd.randrange(h - 17), rnd.randrange(5, 13), 1, .7)


def lounge(x, y, c, cl, things):
    """A sofa, a low table, a chair each side, on a rug, and a lamp over them. x, y: the rug's top left."""
    lattice_rug(x, y, 172, 108, cl[0], cl[1])
    with thing():
        loveseat(x + 46, y - 12, c)
    with thing():
        club_chair(x + 6, y + 28, c, -.3)
    with thing():
        club_chair(x + 134, y + 28, c, -.6, flip=True)
    with thing():
        side_table(x + 68, y + 46, things)


# --- by the doors, and the floor ------------------------------------------------------------------------------
def coir(x, y, w, h):
    """A coir mat: lighter than the boards round it, a darker border, the weave in rows."""
    with thing(False), prop(cast=(1, 1), rim=0):
        R(x, y, w, h, RED, 3.3); R(x + 2, y + 2, w - 4, h - 4, FLOOR, 4.3)
        for i in range(w - 4):
            R(x + 2 + i, y + 2 + (i * 3) % max(h - 6, 1), 1, 2, FLOOR, 3.5)


def runner(x, y, w, h):
    """The runner from the top doorway to the hologram: teal, a paper band each side, chevrons down the middle,
    worn pale where everyone walks."""
    with thing(False), prop(cast=None, rim=0):
        for fx in range(x + 1, x + w - 1, 2):
            R(fx, y - 4, 1, 4, PAPER, 4 - (fx % 4) * .2); R(fx, y + h, 1, 4 + (fx % 5 == 0), PAPER, 4)
        R(x, y, w, h, TEAL, 2.4); R(x + 4, y, 3, h, PAPER, 4.4); R(x + w - 7, y, 3, h, PAPER, 4.4)
        R(x + 9, y, w - 18, h, TEAL, 3)
        mid = x + w // 2
        for cy in range(y + 6, y + h - 10, 14):
            for i in range(-14, 15):
                R(mid + i, cy + abs(i) // 2, 1, 2, CARD, 4)
        rnd = random.Random(8)
        for _ in range(h // 6):
            T(mid - 14 + rnd.randrange(24), y + 4 + rnd.randrange(h - 8), rnd.randrange(3, 8), 1, .8)


def compass_rug(cx, cy, w, h):
    """The round rug the hologram stands on: rings, and a point to each doorway."""
    with thing(False), prop(cast=None, rim=0):
        for (px, py), c in (((0, -1), RED), ((0, 1), RED), ((-1, 0), PAPER), ((1, 0), PAPER)):
            tip = (cx + px * (w // 2 + 12), cy + py * (h // 2 + 10))
            G([tip, (cx + py * 14 + px * (w // 2 - 10), cy - px * 9 + py * (h // 2 - 8)),
               (cx - py * 14 + px * (w // 2 - 10), cy + px * 9 + py * (h // 2 - 8))], c, 4 if c == RED else 4.4)
        for i, (c, l) in enumerate(((METAL, 2.4), (CARD, 4), (METAL, 3), (CARD, 3.4), (TEAL, 2.8))):
            d = (0, 4, 8, 18, 22)[i]
            E(cx - w // 2 + d, cy - h // 2 + round(d * h / w), w - 2 * d, h - 2 * round(d * h / w), c, l)
        for i in range(24):
            a = i * math.pi / 12
            R(round(cx + (w // 2 - 13) * math.cos(a)), round(cy + (h // 2 - 8) * math.sin(a)), 2, 1, PAPER, 4.6)


def checkpoint(x, y, w=256, h=96):
    """The carpet in front of the bottom doorway: rust red, an amber band, fringed, and its two lines woven in."""
    with thing(False), prop(cast=None, rim=0):
        for fy in range(y + 1, y + h - 1, 2):
            R(x - 5, fy, 5, 1, PAPER, 4 - (fy % 4) * .2); R(x + w, fy, 5 + (fy % 5 == 0), 1, PAPER, 4)
        R(x, y, w, h, RED, 2.2); R(x + 3, y + 3, w - 6, h - 6, FLOOR, 3.7); R(x + 5, y + 5, w - 10, h - 10, RED, 2.8)
        for sx in range(x + 8, x + w - 8, 6):                   # a row of stitches inside the band
            R(sx, y + 8, 3, 1, FLOOR, 3.7); R(sx, y + h - 9, 3, 1, FLOOR, 3.7)
        tx, ty = x + (w - 2 * max(map(len, TEXT))) // 2, y + (h - 2 * len(TEXT)) // 2
        rnd = random.Random(4)
        for i in range(10):                                     # threadbare, above and below the words
            T(x + 10 + rnd.randrange(w - 34), (y + 11, ty + 2 * len(TEXT) + 3)[i % 2] + rnd.randrange(ty - y - 14), rnd.randrange(5, 13), 1, .7)
        for r, row in enumerate(TEXT):
            for c, ch in enumerate(row):
                if ch == '#':
                    R(tx + 2 * c, ty + 2 * r, 2, 2, FLOOR, 4.9)


def ring(cx, cy, r, c, l):
    L([(round(cx + r * math.cos(a * math.pi / 12)), round(cy + r * math.sin(a * math.pi / 12))) for a in range(25)], c, l, 2)


def bike(x, y):
    """A bike on its stand by the front door, a helmet hung on the bars. 72 x 48."""
    with prop(cast=(3, 3)):
        ring(x + 14, y + 32, 13, METAL, 1.4); ring(x + 58, y + 32, 13, METAL, 1.4)
        R(x + 13, y + 31, 3, 3, METAL, 3.6); R(x + 57, y + 31, 3, 3, METAL, 3.6)
        L([(x + 14, y + 32), (x + 30, y + 14), (x + 54, y + 14), (x + 58, y + 32)], RED, 3.6, 2)
        L([(x + 14, y + 32), (x + 34, y + 33), (x + 30, y + 14)], RED, 3.2, 2); L([(x + 34, y + 33), (x + 54, y + 14)], RED, 3.2, 2)
        L([(x + 30, y + 14), (x + 28, y + 6)], METAL, 3, 2); R(x + 22, y + 4, 12, 3, METAL, 1.8)
        L([(x + 54, y + 14), (x + 52, y + 4)], METAL, 3, 2); R(x + 47, y + 3, 12, 2, METAL, 2.4)
        E(x + 30, y + 29, 8, 8, METAL, 3.4); R(x + 34, y + 38, 5, 2, METAL, 2); L([(x + 36, y + 34), (x + 40, y + 46)], METAL, 2.4)
    with prop(cast=(1, 2)):
        E(x + 49, y - 6, 14, 10, TEAL, 3.4); E(x + 51, y - 5, 7, 4, TEAL, 4.6); R(x + 49, y + 1, 14, 2, TEAL, 2.4)


def bench_seat(x, y):
    """A backless bench in the open floor, buttoned on top: a newspaper left on it. 80 x 26."""
    with prop(cast=(3, 4)):
        R(x + 3, y + 18, 4, 8, DESK, 2.2); R(x + 73, y + 18, 4, 8, DESK, 1.8); R(x + 7, y + 18, 66, 3, DESK, 1)
        R(x, y, 80, 12, GREEN, 3.6); R(x, y, 80, 1, GREEN, 4.4); R(x, y + 12, 80, 6, GREEN, 2.6); R(x + 78, y, 2, 18, GREEN, 2.4)
        for i in range(8):
            R(x + 5 + 10 * i, y + 4 + (i % 2) * 4, 1, 1, GREEN, 2.4)
    with prop(cast=(1, 1), rim=0):
        G([(x + 44, y + 2), (x + 62, y + 1), (x + 64, y + 11), (x + 45, y + 12)], PAPER, 4.8)
        for i in range(3):
            R(x + 47, y + 4 + 2 * i, 14, 1, PAPER, 3.6)
        R(x + 54, y + 3, 6, 4, METAL, 3)


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


def wear(rnd):
    """Scratches along the boards, more of them on the way between the doors."""
    for _ in range(26):
        x, y = rnd.randrange(X0 + 10, X1 - 40), rnd.randrange(Y0 + 20, Y1 - 6)
        L([(x, y), (x + rnd.randrange(8, 22), y + rnd.randrange(-1, 2))], FLOOR, 2.3)


# --- light ----------------------------------------------------------------------------------------------------
def sun(x):
    """Sun through a hall window at x: a patch down the wall under it and out across the boards."""
    for x0 in (x + 3, x + 27):
        light(1, 1.2, [(x0, 96), (x0 + 21, 96), (x0 + 84, 200), (x0 + 52, 200)])
        light(.6, 2.5, [(x0 + 4, 96), (x0 + 17, 96), (x0 + 44, 146), (x0 + 28, 142)])
    light(.5, 2, [(x - 2, 74), (x + 54, 74), (x + 56, 96), (x - 2, 96)])


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


def room_lights():
    doorways()
    if not m.EVE:
        light(.95, 60, lambda d: d.ellipse((-40, -90, W + 40, H + 60), fill=255))                 # daylight, weaker in the corners
        for x in (60, 330, 900):
            sun(x)
    else:
        for x in (60, 330, 900):                                                                   # the last of the dusk
            light(.5, 3, [(x, 74), (x + 52, 74), (x + 60, 96), (x - 6, 96)])
            light(.4, 9, [(x + 10, 110), (x + 70, 106), (x + 100, 170), (x + 60, 196), (x + 14, 170)])


# --- the room -------------------------------------------------------------------------------------------------
def draw():
    rnd = random.Random(11)
    shell(); wear(rnd)
    # flat: what is on the floor, then rugs and mats over it
    with thing(False):
        litter(rnd, 30)
    runner(604, 100, 72, 236)
    compass_rug(640, 394, 176, 100)
    checkpoint(512, 512)
    coir(20, 486, 24, 54); coir(1236, 134, 24, 54); coir(592, 692, 96, 22)
    with thing(False):
        m.socket(846, 77)
        cable([(682, 402), (720, 404), (760, 396), (800, 380), (830, 340), (846, 280), (850, 200), (850, 120), (849, 96), (849, 84)],
              tape=((716, 402), (836, 330), (846, 220), (847, 150)))
    # the back wall, left to right
    with thing():
        hall_window(60, 12, ((0, 30, 6, 2), (6, 24, 8, 1), (15, 33, 6, 2), (22, 27, 9, 1), (32, 20, 6, 1), (38, 30, 7, 2)))
    house_map(190, 14)
    with thing():
        hall_window(330, 12, ((0, 26, 9, 1), (9, 33, 5, 2), (14, 22, 7, 1), (22, 30, 8, 2), (30, 25, 6, 1), (37, 34, 8, 2)), TEAL, 3)
    key_box(424, 32)
    sconce(540, 42); sconce(734, 42)
    gallery(766, 14)
    with thing():
        hall_window(900, 12, ((0, 34, 7, 2), (7, 26, 6, 1), (13, 30, 9, 2), (23, 21, 6, 1), (29, 28, 8, 2), (38, 32, 7, 1)), GREEN, 3.4)
    m.clock(972, 22)
    mirror(1072, 14)
    m.fairy_lights(((20, 12, 56, 13, 5), (126, 12, 188, 14, 6), (288, 12, 328, 13, 5), (392, 12, 448, 14, 6),
                    (712, 12, 766, 14, 6), (850, 12, 898, 14, 5), (1000, 12, 1068, 14, 7), (1104, 12, 1180, 15, 8), (1180, 15, 1250, 12, 7)))
    # along the back wall
    with thing(tall=True):
        monstera(26, 104)
    with thing():
        settle(48, 86)
    with thing(tall=True):
        arc_lamp(150, 124, -22)
    with thing():
        console(440, 84)
    with thing():
        umbrella_stand(546, 104)
    with thing():
        chest(774, 92)
    with thing(tall=True):
        fig(856, 106)
    with thing(tall=True):
        vitrine(1000, 38)
    # the left wall: the post, coats, the side door's boots, the boxes in the corner
    with thing(tall=True):
        pigeonholes(18, 212)
    with thing(tall=True):
        coat_stand(36, 348)
    with thing():
        boots(20, 600)
    with thing():
        m.box(22, 668, 30, 10, 26, 0, 10)
    with thing():
        m.box(54, 680, 26, 9, 18, .2, 4); m.box(24, 650, 22, 7, 12, .3, 6)
    # the right wall
    with thing(tall=True):
        water_cooler(1234, 280)
    with thing(tall=True):
        fig(1236, 388)
    # the open floor: a bench by the hero's first steps, a sculpture, the hologram's plinth
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
    # the lounges by the right wall
    lounge(1082, 470, RED, (CARD, RED), 'tea')
    lounge(1082, 598, TEAL, (METAL, TEAL), 'game')
    with thing(tall=True):
        arc_lamp(1064, 566, 64)
    with thing(tall=True):
        arc_lamp(1064, 662, 64)
    # by the front door
    with thing():
        bike(452, 664)
    with thing():
        m.box(740, 668, 32, 10, 28, 0, 12); m.box(748, 650, 22, 7, 12, .3, 6)
    with thing():
        m.box(776, 684, 28, 9, 16, -.2, 8)


def build(evening):
    m.canvas(W, H, evening)
    draw()
    room_lights()
    return m.render()
