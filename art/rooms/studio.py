# The studio: an open-plan room of 896x512 px (28x16 tiles of 32 px, one art pixel per game pixel), by day and
# in the evening. The style, the palette and most of the props are draw.py's (read its header first). What is
# new here:
#   layout: furniture stands in zones along the walls and in a few islands, each piece inside whole tiles, so a
#     tile is clearly taken or clearly free. Aisles between zones are two tiles or more.
#   every piece of furniture is drawn inside `with thing():`, so draw.tiles() can turn it into free tiles and
#     the upper layer.
#   light: by day two windows and their sun patches; in the evening the room is dark between separate pools.
# Rebuild: python3 -I art/room.py studio
import random
import draw as m
from draw import (R, E, G, L, T, prop, light, note, thing, TILE, FLOOR, DESK, WALL, GREEN, METAL, TEAL, CARD, RED, PAPER,
                  FLAT)

W, H = 896, 512
X0, X1, Y0, Y1 = 16, W - 16, 64, H - 16     # the floor
DOOR = 13                                   # the door gap is this column of the bottom edge
SPOTS = {'hero': [DOOR, 14], 'dana': [18, 2], 'visitor': [2, 3], 'dog': [[24, 14], [25, 14]]}   # where the cast starts


def sh(pts, dx, dy=0):
    return [(x + dx, y + dy) for x, y in pts]


# --- room shell -----------------------------------------------------------------------------------------------
def shell():
    rnd = random.Random(3)
    fw = X1 - X0
    R(X0, 8, fw, 56, WALL, 3.1)
    for _ in range(130):                                       # plaster in patches
        E(rnd.randrange(8, X1 - 6), rnd.randrange(4, 44), rnd.randrange(10, 36), rnd.randrange(4, 12), WALL,
          3.1 + rnd.choice((-.45, -.3, .3, .45)))
    for x, y, w, h in ((22, 30, 30, 18), (300, 6, 40, 14), (452, 28, 26, 16), (604, 5, 44, 12), (846, 26, 30, 20)):
        E(x, y, w, h, WALL, 2.6)                               # damp
    for pts in ([(288, 8), (290, 14), (287, 19), (291, 26)], [(96, 56), (99, 60), (97, 63)], [(470, 30), (474, 38)],
                [(640, 8), (637, 15), (641, 21)], [(868, 40), (872, 47), (870, 56)], [(566, 50), (570, 57)]):
        L(pts, WALL, 1.6)                                      # cracks
    R(X0, 8, fw, 2, WALL, 2)                                   # under the ceiling
    R(X0, 45, fw, 12, WALL, 2.7); R(X0, 44, fw, 1, WALL, 4); R(X0, 45, fw, 1, WALL, 2)        # painted dado
    for x in range(20, X1, 9):
        R(x + rnd.randrange(3), 47 + rnd.randrange(8), 2, 1, WALL, 2.3)                        # scuffs
    R(X0, 57, fw, 7, DESK, 2.8); R(X0, 57, fw, 1, DESK, 4); R(X0, 62, fw, 2, DESK, 1.6)       # skirting
    m.boards(X0, X1, Y0, Y1, rnd)
    R(0, 0, W, 8, 0, 0); R(0, 0, X0, H, 0, 0); R(X1, 0, W - X1, H, 0, 0)
    R(0, Y1, DOOR * TILE, H - Y1, 0, 0); R(DOOR * TILE + TILE, Y1, W, H - Y1, 0, 0)
    T(X0, Y0, fw, 3, -1); R(DOOR * TILE, Y1, TILE, 1, FLOOR, 1.5)                               # the wall's shadow, the door sill


def pipes():
    with prop(cast=(1, 2)):
        R(16, 11, 602, 3, METAL, 3.4); R(16, 11, 602, 1, METAL, 4.4); R(16, 13, 602, 1, METAL, 2)
        for x in (40, 130, 200, 292, 380, 470, 566):
            R(x, 10, 3, 5, METAL, 2.6)
    with prop(cast=(1, 2)):                                     # it turns into the wall
        R(616, 10, 5, 12, METAL, 3.2); R(616, 10, 1, 12, METAL, 4.2); R(620, 10, 1, 12, METAL, 2); R(614, 21, 9, 3, METAL, 2.4)
    with prop(cast=(1, 2)):
        R(19, 12, 4, 51, METAL, 3.2); R(19, 12, 1, 51, METAL, 4.2); R(22, 12, 1, 51, METAL, 2)
        R(18, 34, 6, 3, METAL, 2.4); R(17, 26, 8, 4, RED, 3.4); R(17, 26, 8, 1, RED, 4.4)      # joint, valve
    R(20, 38, 1, 20, WALL, 1.8); R(21, 44, 1, 10, WALL, 1.8)                                  # a rust run under it
    R(618, 24, 1, 14, WALL, 1.8)


# --- flat things ----------------------------------------------------------------------------------------------
def mat(x, y, w, h, a, b, la=3, lb=4.2):
    """A woven mat: stripes across, a fringe at both ends."""
    with thing(False), prop(cast=None, rim=0):
        for fy in range(y + 1, y + h - 1, 2):
            R(x - 3, fy, 3, 1, PAPER, 4); R(x + w, fy, 3 + (fy % 5 == 0), 1, PAPER, 4)
        R(x, y, w, h, a, la)
        for i, sx in enumerate(range(x + 4, x + w - 5, 7)):
            R(sx, y, 3 + (i % 3 == 0) * 2, h, b, lb)
        R(x, y, w, 1, a, la - .8); R(x, y + h - 1, w, 1, a, la - .8)


def scraps(rnd, n):
    """Small flat litter on the floor: paper, a coin, a leaf."""
    for _ in range(n):
        x, y = rnd.randrange(X0 + 8, X1 - 12), rnd.randrange(Y0 + 40, Y1 - 6)
        k = rnd.randrange(4)
        with prop(cast=(1, 1), rim=0):
            if k == 0:
                R(x, y, 5, 4, PAPER, 5); R(x + 3, y + 1, 2, 3, PAPER, 3.6)
            elif k == 1:
                R(x, y, 4, 3, FLOOR, 5.2); R(x + 1, y + 2, 3, 1, FLOOR, 3.8)
            elif k == 2:
                R(x, y, 3, 2, GREEN, 3); R(x + 1, y + 1, 2, 1, GREEN, 2)
            else:
                R(x, y, 6, 1, PAPER, 4.4); R(x + 1, y + 1, 4, 3, PAPER, 5)


def wear(rnd):
    """What use has left on the floor: a few scratches along the boards, and a court taped out for the table
    tennis, its tape worn through in places."""
    for _ in range(10):
        x, y = rnd.randrange(X0 + 10, X1 - 40), rnd.randrange(Y0 + 30, Y1 - 6)
        L([(x, y), (x + rnd.randrange(8, 22), y + rnd.randrange(-1, 2))], FLOOR, 2.3)
    x0, y0, x1, y1 = 200, 270, 346, 362
    for x in range(x0, x1, 4):
        for y in (y0, y1):
            if rnd.random() < .8:
                R(x, y, 4, 2, PAPER, 4.6)
    for y in range(y0, y1, 4):
        for x in (x0, x1 - 2):
            if rnd.random() < .8:
                R(x, y, 2, 4, PAPER, 4.6)


def aquarium(x, y):
    """A fish tank on a low cabinet, 60 wide and 56 high. The tank is lit from its lid; pools in room_lights()."""
    with prop(cast=(3, 4)):
        R(x, y + 38, 60, 18, DESK, 3); R(x, y + 38, 60, 2, DESK, 4.2); R(x + 29, y + 41, 2, 14, DESK, 2)       # cabinet, two doors
        R(x + 13, y + 46, 5, 1, DESK, 4.6); R(x + 42, y + 46, 5, 1, DESK, 4.6); R(x, y + 55, 60, 1, DESK, 1.6)
        R(x + 2, y, 56, 38, METAL, 1.6); R(x + 2, y, 56, 3, METAL, 3)                                           # frame, lid
        R(x + 4, y + 3, 52, 32, TEAL + FLAT, 2); R(x + 4, y + 3, 52, 12, TEAL + FLAT, 3); R(x + 4, y + 3, 52, 2, TEAL + FLAT, 5)
        R(x + 4, y + 31, 52, 4, CARD + FLAT, 4); R(x + 9, y + 30, 9, 2, CARD + FLAT, 4); R(x + 38, y + 30, 12, 1, CARD + FLAT, 4)     # sand
        for px, h in ((8, 16), (11, 10), (14, 20), (41, 22), (45, 13), (50, 8)):                                # weed
            R(x + px, y + 31 - h, 2, h, GREEN + FLAT, 4); R(x + px + 1, y + 31 - h + 2, 1, h - 2, GREEN + FLAT, 3)
        R(x + 22, y + 26, 9, 5, METAL + FLAT, 3); R(x + 24, y + 24, 5, 2, METAL + FLAT, 4); R(x + 25, y + 28, 3, 3, METAL + FLAT, 1)  # a rock with a hole
        for px, py, c, back in ((19, 9, RED, 1), (31, 15, FLOOR, 0), (26, 20, RED, 0), (46, 8, FLOOR, 1), (36, 23, PAPER, 1)):       # fish
            R(x + px, y + py, 5, 3, c + FLAT, 5); R(x + px + (5 if back else -2), y + py - 1 + (px % 2), 2, 4 - (px % 2), c + FLAT, 4)
            R(x + px + (0 if back else 4), y + py + 1, 1, 1, METAL + FLAT, 0)
        for bx, by in ((34, 8), (35, 12), (33, 17), (16, 6)):                                                   # bubbles
            R(x + bx, y + by, 1, 1, PAPER + FLAT, 6)
    with prop(cast=(1, 1)):                                     # on the lid: fish food, a net
        R(x + 6, y - 5, 5, 5, RED, 4); R(x + 6, y - 5, 5, 1, PAPER, 5); R(x + 40, y - 2, 12, 2, METAL, 3.4); R(x + 50, y - 4, 5, 4, GREEN, 3.4)
    if m.EVE:                                                   # the tank is the middle of the room's lamp
        light(1, 3, [(x - 6, y - 8), (x + 64, y - 10), (x + 72, y + 30), (x + 66, y + 66), (x - 4, y + 70), (x - 12, y + 26)])
        light(.8, 5, [(x - 22, y + 30), (x + 30, y + 22), (x + 84, y + 36), (x + 90, y + 84), (x + 26, y + 98), (x - 30, y + 80)])
        light(.5, 8, [(x - 50, y + 4), (x + 40, y - 26), (x + 112, y + 16), (x + 120, y + 96), (x + 30, y + 124), (x - 56, y + 96)])
    else:
        light(.5, 3, [(x - 6, y + 50), (x + 66, y + 50), (x + 72, y + 70), (x - 10, y + 72)])


# --- on the wall ----------------------------------------------------------------------------------------------
def wall_shelf(x, y):
    """A plank over the counter: jars, bowls, a plant; mugs on hooks and a light strip under it."""
    with prop(cast=(1, 2)):
        R(x, y, 84, 3, DESK, 3.6); R(x, y + 2, 84, 1, DESK, 2.2)
        R(x + 6, y + 3, 2, 5, METAL, 2); R(x + 76, y + 3, 2, 5, METAL, 2)
    R(x + 12, y + 3, 60, 1, FLOOR + FLAT, 6)                    # the strip
    with prop(cast=(1, 1)):
        for jx, lid, body, fill in ((2, RED, PAPER, CARD), (10, RED, PAPER, DESK), (18, TEAL, PAPER, PAPER)):
            R(x + jx, y - 10, 6, 10, body, 4.4); R(x + jx + 1, y - 6, 4, 5, fill, 3.2 if fill != PAPER else 5.4)
            R(x + jx, y - 11, 6, 2, lid, 4); R(x + jx + 5, y - 10, 1, 10, body, 3.2)
    with prop(cast=(1, 1)):                                     # bowls, a tin, a bottle
        for i in range(4):
            R(x + 28 + i // 2, y - 3 - 2 * i, 12 - 2 * (i // 2), 2, PAPER, 5 - (i % 2) * .8)
        R(x + 44, y - 9, 8, 9, TEAL, 3.2); R(x + 50, y - 9, 2, 9, TEAL, 2.2); R(x + 45, y - 6, 5, 3, PAPER, 5)
        R(x + 55, y - 12, 4, 12, GREEN, 2.8); R(x + 56, y - 15, 2, 3, GREEN, 2.8); R(x + 55, y - 7, 4, 4, PAPER, 4.6); R(x + 55, y - 12, 1, 12, GREEN, 4)
    with prop(cast=(1, 1)):                                     # a plant that hangs over the end
        R(x + 66, y - 7, 10, 7, RED, 3.4); R(x + 66, y - 7, 10, 2, RED, 4.2)
        for lx, ly in ((64, -11), (69, -13), (74, -11), (78, -8), (80, -3), (79, 3), (81, 8), (62, -8), (71, -10)):
            R(x + lx, y + ly, 3, 3, GREEN, 3.4 + (lx % 2) * .8); R(x + lx + 1, y + ly + 2, 2, 1, GREEN, 2.4)
    for i, (mx, c) in enumerate(((20, RED), (30, PAPER), (40, TEAL), (52, FLOOR))):               # mugs on hooks
        with prop(cast=(1, 1)):
            R(x + mx + 2, y + 4, 1, 2, METAL, 2); R(x + mx, y + 6, 6, 6, c, 4.2 if c != TEAL else 3.4); R(x + mx + 5, y + 6, 1, 6, c, 3)
            R(x + mx + 6, y + 8, 2, 1, c, 3.6); R(x + mx + 7, y + 8, 1, 3, c, 3.6)
    light(1 if m.EVE else .5, 2.5, [(x + 8, y + 2), (x + 76, y + 2), (x + 84, y + 30), (x + 2, y + 32)])
    if m.EVE:
        light(.8, 2, [(x + 16, y + 4), (x + 68, y + 4), (x + 74, y + 24), (x + 40, y + 28), (x + 12, y + 22)])
        light(.8, 4, [(x - 6, y + 22), (x + 90, y + 20), (x + 96, y + 64), (x + 60, y + 84), (x - 2, y + 74)])
        light(.5, 6, [(x - 10, y + 50), (x + 80, y + 46), (x + 110, y + 80), (x + 70, y + 110), (x - 4, y + 98)])


def whiteboard(x, y):
    with prop(cast=(2, 3)):
        R(x, y, 52, 31, METAL, 3.6); R(x + 2, y + 2, 48, 26, PAPER, 5.2); R(x + 2, y + 2, 48, 1, PAPER, 4); R(x + 2, y + 2, 1, 26, PAPER, 4)
        R(x + 2, y + 29, 48, 2, METAL, 2.4)
        for bx, by, bw, bh, c in ((6, 6, 11, 7, RED), (22, 5, 11, 7, TEAL), (37, 8, 10, 7, GREEN), (20, 18, 12, 7, RED)):
            R(x + bx, y + by, bw, bh, c, 4); R(x + bx + 1, y + by + 1, bw - 2, bh - 2, PAPER, 5.2)
            R(x + bx + 2, y + by + 3, bw - 5, 1, METAL, 2.4)
        for pts in ([(17, 9), (22, 9)], [(33, 9), (37, 11)], [(27, 12), (26, 18)], [(11, 13), (14, 21), (20, 21)]):
            L(sh(pts, x, y), METAL, 1.6)
        for i, w in enumerate((9, 6, 8)):
            R(x + 36, y + 18 + 3 * i, w, 1, TEAL, 2.6)
        R(x + 6, y + 18, 9, 1, RED, 3.6); R(x + 6, y + 20, 6, 1, RED, 3.6)
        for i, c in enumerate((RED, TEAL, METAL)):               # markers in the tray
            R(x + 8 + 8 * i, y + 28, 6, 2, c, 4 if c != METAL else 1.6)
        R(x + 38, y + 27, 8, 3, PAPER, 4.2)                       # the eraser
    note(x + 44, y + 3, 6, 6, FLOOR, 5.4, 1); note(x + 53, y + 8, 6, 6, RED, 5, 1)


def hooks(x, y):
    """A rail of hooks: a coat, a tote bag, a scarf, a cap."""
    with prop(cast=(1, 2)):
        R(x, y, 40, 3, DESK, 3.6); R(x, y + 2, 40, 1, DESK, 2.2)
        for hx in (4, 15, 26, 35):
            R(x + hx, y + 2, 2, 3, METAL, 4)
    with prop(cast=(2, 3)):                                     # coat
        G([(x + 2, y + 6), (x + 8, y + 4), (x + 12, y + 7), (x + 13, y + 34), (x - 1, y + 34), (x - 2, y + 12)], METAL, 2.6)
        R(x + 5, y + 5, 1, 29, METAL, 1.6); R(x + 10, y + 8, 3, 26, METAL, 2); R(x, y + 10, 2, 22, METAL, 3.4)
        R(x + 3, y + 5, 2, 4, PAPER, 4.4); R(x + 6, y + 5, 2, 4, PAPER, 4.4); R(x + 6, y + 14, 1, 1, FLOOR, 5.2); R(x + 6, y + 20, 1, 1, FLOOR, 5.2)
        R(x + 7, y + 25, 4, 1, METAL, 1.6)
    with prop(cast=(1, 2)):                                     # tote bag
        L([(x + 14, y + 16), (x + 16, y + 5), (x + 20, y + 16)], PAPER, 3.6)
        R(x + 13, y + 15, 10, 13, PAPER, 4.8); R(x + 21, y + 15, 2, 13, PAPER, 3.6); E(x + 15, y + 18, 6, 6, RED, 4)
    with prop(cast=(1, 2)):                                     # scarf
        R(x + 26, y + 4, 3, 26, TEAL, 3.2); R(x + 28, y + 6, 3, 19, TEAL, 2.4)
        for i in range(4):
            R(x + 26, y + 8 + 5 * i, 5, 1, PAPER, 5)
        R(x + 26, y + 30, 1, 2, TEAL, 3.2); R(x + 28, y + 25, 1, 2, TEAL, 2.4); R(x + 30, y + 25, 1, 2, TEAL, 2.4)
    with prop(cast=(1, 1)):                                     # cap
        E(x + 32, y + 4, 9, 7, RED, 3.6); R(x + 32, y + 9, 11, 2, RED, 2.6); R(x + 34, y + 5, 3, 2, RED, 4.6)


def frames(x, y):
    with prop(cast=(1, 2), rim=0):
        R(x, y, 15, 19, PAPER, 5); R(x + 2, y + 2, 11, 15, TEAL, 2.6); E(x + 4, y + 5, 7, 7, FLOOR, 5.4); R(x + 2, y + 13, 11, 4, GREEN, 3)
    with prop(cast=(1, 2), rim=0):
        R(x + 19, y + 3, 19, 14, DESK, 3); R(x + 21, y + 5, 15, 10, PAPER, 5); G([(x + 22, y + 14), (x + 27, y + 7), (x + 31, y + 11), (x + 33, y + 9), (x + 35, y + 14)], METAL, 2.6)
    with prop(cast=(1, 2), rim=0):
        R(x + 41, y - 1, 11, 11, METAL, 2); R(x + 43, y + 1, 7, 7, RED, 3.6); R(x + 45, y + 3, 3, 3, FLOOR, 5.4)


def radiator(x, y):
    with prop(cast=(1, 2)):
        R(x + 2, y + 14, 2, 4, METAL, 2); R(x + 34, y + 14, 2, 4, METAL, 2)
        for i in range(9):
            R(x + 4 * i, y, 3, 15, PAPER, 4.4); R(x + 4 * i + 2, y, 1, 15, PAPER, 3.2); R(x + 4 * i, y, 3, 1, PAPER, 5.2)
        R(x + 36, y + 2, 3, 2, METAL, 3); R(x + 38, y + 1, 3, 4, RED, 3.6)


# --- furniture ------------------------------------------------------------------------------------------------
def counter(x, y):
    """The kitchenette: a worktop on painted cupboards against the wall; sink, dish rack, coffee machine, microwave."""
    with prop(cast=(3, 4)):
        R(x, y, 96, 14, PAPER, 4.3); R(x + 94, y, 2, 14, PAPER, 3.4); R(x, y + 13, 96, 2, PAPER, 3)
        R(x + 1, y + 15, 94, 21, TEAL, 2.4); R(x + 92, y + 15, 3, 21, TEAL, 1.6); R(x + 1, y + 15, 94, 1, TEAL, 1.4)
        for i in range(3):
            dx = x + 3 + 31 * i
            R(dx, y + 17, 28, 18, TEAL, 2.9); R(dx, y + 17, 28, 1, TEAL, 3.8); R(dx + 27, y + 17, 1, 18, TEAL, 2.2)
            R(dx + (22 if i != 1 else 3), y + 20, 3, 1, PAPER, 5.2); R(dx + (22 if i != 1 else 3), y + 21, 3, 1, PAPER, 3)
        R(x + 34, y + 23, 28, 1, TEAL, 1.6)                       # the middle one is two drawers
        R(x + 2, y + 36, 92, 2, METAL, 1.2)
    with prop(cast=None, rim=0):                                # sink, tap
        R(x + 4, y + 2, 26, 10, METAL, 4); R(x + 6, y + 4, 22, 7, METAL, 2.2); R(x + 6, y + 4, 22, 2, METAL, 1.4); R(x + 15, y + 8, 2, 2, METAL, 1)
        E(x + 8, y + 6, 9, 5, PAPER, 5); E(x + 10, y + 7, 5, 3, PAPER, 4)
    with prop(cast=(1, 2)):
        R(x + 20, y - 6, 2, 9, METAL, 4.4); R(x + 15, y - 6, 6, 2, METAL, 4.4); R(x + 15, y - 4, 2, 2, METAL, 3); R(x + 23, y + 1, 3, 2, METAL, 4.6)
    with prop(cast=(1, 2)):                                     # dish rack
        R(x + 33, y + 4, 15, 7, METAL, 2.6); R(x + 33, y + 10, 15, 1, METAL, 1.6)
        for i in range(4):
            R(x + 34 + 3 * i, y - 3, 2, 10, PAPER, 5.2 - (i % 2) * .8)
        R(x + 46, y, 1, 6, TEAL, 4)
    with prop(cast=(2, 3)):                                     # coffee machine
        R(x + 51, y - 18, 16, 4, METAL, 2.8); R(x + 51, y - 14, 16, 20, METAL, 1.8); R(x + 65, y - 14, 2, 20, METAL, 1.2)
        R(x + 53, y - 7, 11, 10, METAL, .8); R(x + 50, y + 4, 18, 3, METAL, 2.6)
        R(x + 54, y - 5, 8, 8, PAPER, 4.2); R(x + 54, y - 2, 8, 5, DESK, 1.6); R(x + 54, y - 5, 1, 8, PAPER, 5.6); R(x + 62, y - 3, 2, 1, PAPER, 4.2); R(x + 63, y - 3, 1, 4, PAPER, 4.2)
        R(x + 53, y - 12, 3, 2, PAPER, 4.6); R(x + 57, y - 12, 3, 2, PAPER, 4.6); R(x + 62, y - 12, 2, 2, RED + FLAT, 5)
    with prop(cast=(2, 3)):                                     # microwave
        R(x + 71, y - 14, 24, 4, PAPER, 4.8); R(x + 71, y - 10, 24, 14, PAPER, 4); R(x + 93, y - 10, 2, 14, PAPER, 3)
        R(x + 73, y - 8, 14, 10, METAL, 1.2); R(x + 74, y - 7, 4, 1, METAL, 3); R(x + 74, y - 5, 2, 1, METAL, 3)
        R(x + 89, y - 8, 4, 2, TEAL + FLAT, 4); R(x + 89, y - 4, 4, 1, PAPER, 2.6); R(x + 89, y - 2, 4, 1, PAPER, 2.6); R(x + 89, y, 4, 1, PAPER, 2.6)
    with prop(cast=(1, 1)):                                     # a mug, a banana, a paper cup
        R(x + 71, y + 6, 6, 6, RED, 3.8); R(x + 76, y + 6, 1, 6, RED, 2.8); R(x + 72, y + 6, 4, 1, DESK, 1.6); R(x + 77, y + 8, 2, 1, RED, 3.4); R(x + 78, y + 8, 1, 3, RED, 3.4)
    with prop(cast=(1, 1)):
        R(x + 82, y + 8, 9, 2, FLOOR, 5.4); R(x + 81, y + 6, 3, 2, FLOOR, 5.4); R(x + 89, y + 6, 3, 2, FLOOR, 4.6); R(x + 80, y + 5, 1, 1, DESK, 2)
    with prop(cast=(1, 2)):                                     # a tea towel over a door
        R(x + 10, y + 15, 8, 12, RED, 3.8); R(x + 10, y + 19, 8, 1, PAPER, 5); R(x + 10, y + 23, 8, 1, PAPER, 5); R(x + 16, y + 15, 2, 12, RED, 2.8)
    note(x + 70, y + 19, 6, 6, FLOOR, 5.2, 1)


def stool(x, y, top=FLOOR, l=4.4):
    with prop(cast=(2, 3)):
        R(x + 3, y + 7, 2, 18, METAL, 2.2); R(x + 15, y + 7, 2, 18, METAL, 1.6); R(x + 7, y + 7, 1, 14, METAL, 1.2); R(x + 12, y + 7, 1, 14, METAL, 1.2)
        R(x + 4, y + 18, 12, 1, METAL, 2.8)
        E(x, y + 2, 20, 10, top, l - 1.4); E(x, y, 20, 10, top, l); E(x + 3, y + 1, 11, 5, top, l + .6)


def table(x, y):
    """The big table: a light wooden top on dark legs, with what a morning leaves on it."""
    with prop(cast=(3, 4)):
        R(x + 3, y + 42, 4, 13, DESK, 2.6); R(x + 85, y + 42, 4, 13, DESK, 2.2); R(x + 9, y + 42, 3, 8, DESK, 1.4); R(x + 79, y + 42, 3, 8, DESK, 1.4)
        R(x, y, 92, 38, FLOOR, 4.5); R(x + 90, y + 2, 2, 36, FLOOR, 3.7)
        for i, py in enumerate((9, 19, 29)):
            R(x, y + py, 92, 1, FLOOR, 3.8); R(x + 20 + 23 * i, y + py - 9, 1, 9, FLOOR, 3.8)
        for gx, gy, gw in ((6, 4, 18), (50, 14, 26), (14, 24, 30), (60, 33, 20), (30, 6, 12)):
            R(x + gx, y + gy, gw, 1, FLOOR, 4.1)
        E(x + 60, y + 21, 8, 6, FLOOR, 3.9); E(x + 61, y + 22, 6, 4, FLOOR, 4.5)                    # a mug ring
        R(x, y + 38, 92, 4, FLOOR, 3.6); R(x, y + 41, 92, 1, FLOOR, 2.4)
    T(x + 7, y + 43, 78, 12, -1.3)
    with prop(cast=(2, 2)):                                     # laptop, open towards us
        R(x + 34, y + 3, 24, 16, METAL, 2.2); R(x + 34, y + 3, 24, 1, METAL, 3.4)
        R(x + 35, y + 4, 22, 13, TEAL + FLAT, 1); R(x + 35, y + 4, 22, 2, METAL + FLAT, 1)
        for i, (ind, w, c) in enumerate(((0, 8, PAPER), (2, 12, TEAL), (2, 7, FLOOR), (0, 10, PAPER), (2, 6, RED))):
            R(x + 37 + ind, y + 7 + 2 * i, w, 1, c + FLAT, 5)
        R(x + 33, y + 19, 26, 11, METAL, 3.6); R(x + 33, y + 29, 26, 1, METAL, 2.4)
        for row in range(3):
            R(x + 35, y + 21 + 2 * row, 22, 1, METAL, 2.4)
        R(x + 42, y + 27, 8, 2, METAL, 4.2)
    with prop(cast=(1, 2)):                                     # a plate with what is left, a knife
        E(x + 8, y + 22, 15, 10, PAPER, 5); E(x + 10, y + 23, 11, 7, PAPER, 4.2); R(x + 12, y + 25, 5, 3, FLOOR, 4.9); R(x + 13, y + 24, 3, 1, DESK, 3)
        R(x + 25, y + 23, 1, 8, PAPER, 5.4)
    with prop(cast=(2, 3)):                                     # cereal box, milk
        R(x + 12, y + 2, 10, 14, RED, 3.6); R(x + 20, y + 2, 2, 14, RED, 2.6); R(x + 13, y + 5, 7, 5, FLOOR, 5.2); R(x + 14, y + 12, 5, 1, PAPER, 5)
        R(x + 24, y + 6, 6, 10, PAPER, 5); R(x + 28, y + 6, 2, 10, PAPER, 3.8); R(x + 25, y + 4, 4, 2, PAPER, 4.4); R(x + 24, y + 10, 6, 3, TEAL, 3.4)
    with prop(cast=(1, 2)):                                     # two mugs
        R(x + 63, y + 22, 7, 7, TEAL, 3.4); R(x + 68, y + 22, 2, 7, TEAL, 2.4); R(x + 64, y + 22, 5, 2, DESK, 1.6); R(x + 70, y + 24, 2, 1, TEAL, 3); R(x + 71, y + 24, 1, 3, TEAL, 3)
    with prop(cast=(1, 2)):
        R(x + 4, y + 8, 6, 7, PAPER, 5); R(x + 9, y + 8, 1, 7, PAPER, 3.6); R(x + 5, y + 8, 4, 2, DESK, 1.6)
    with prop(cast=(1, 2)):                                     # a bowl of fruit
        E(x + 66, y + 4, 18, 11, CARD, 2.8); E(x + 66, y + 3, 18, 10, CARD, 4.2); E(x + 68, y + 4, 14, 7, CARD, 3)
        E(x + 69, y + 3, 6, 6, RED, 4); E(x + 74, y + 4, 6, 6, FLOOR, 5.2); E(x + 72, y + 1, 6, 5, GREEN, 3.8); R(x + 70, y + 4, 2, 1, RED, 5)
    with prop(cast=(1, 1), rim=0):                              # a sketchbook, a pencil, a phone
        G([(x + 73, y + 20), (x + 88, y + 22), (x + 86, y + 36), (x + 71, y + 34)], PAPER, 5.2)
        L([(x + 75, y + 24), (x + 84, y + 25)], PAPER, 3.4); L([(x + 75, y + 27), (x + 82, y + 28)], PAPER, 3.4); L([(x + 74, y + 30), (x + 84, y + 31)], PAPER, 3.4)
        E(x + 78, y + 28, 6, 4, RED, 4.4)
    with prop(cast=(1, 2)):                                     # a lantern
        R(x + 49, y + 1, 7, 2, METAL, 2); R(x + 50, y - 9, 5, 10, FLOOR + FLAT, 6); R(x + 53, y - 9, 2, 10, FLOOR + FLAT, 5); R(x + 49, y - 11, 7, 2, METAL, 2.6); R(x + 51, y - 14, 3, 3, METAL, 2)
    with prop(cast=(1, 1), rim=0):
        L([(x + 60, y + 32), (x + 69, y + 35)], FLOOR, 5.4); R(x + 60, y + 32, 1, 1, RED, 4)
        R(x + 4, y + 30, 5, 7, METAL, 1.4); R(x + 5, y + 31, 3, 5, TEAL + FLAT, 3)


def sofa(x, y):
    with prop(cast=(3, 4)):
        R(x + 3, y + 48, 5, 3, DESK, 1.6); R(x + 88, y + 48, 5, 3, DESK, 1.6)
        R(x + 10, y, 76, 6, GREEN, 3.9); R(x + 10, y + 6, 76, 12, GREEN, 2.6)                  # the back: top, front
        for i in range(3):
            cx = x + 11 + 25 * i
            R(cx, y + 6, 24, 11, GREEN, 3.1); R(cx, y + 6, 24, 1, GREEN, 3.7); R(cx + 23, y + 6, 1, 11, GREEN, 2.3)
            R(cx, y + 17, 24, 20, GREEN, 3.6); R(cx, y + 17, 24, 2, GREEN, 2.3); R(cx + 23, y + 17, 1, 20, GREEN, 2.6)   # seat: top,
            R(cx + 4, y + 24, 12, 1, GREEN, 3.2); R(cx + 8, y + 30, 10, 1, GREEN, 3.2)                                 # creases
            R(cx, y + 37, 24, 5, GREEN, 2.9); R(cx, y + 37, 24, 1, GREEN, 4.2)                                         # front
        R(x + 10, y + 42, 76, 6, GREEN, 2.1)
        for ax, d in ((x, 0), (x + 86, -.4)):                                                  # arms: top, front
            R(ax, y + 4, 10, 32, GREEN, 4 + d); R(ax, y + 36, 10, 12, GREEN, 2.9 + d); R(ax, y + 36, 10, 1, GREEN, 4.4 + d)
        R(x + 8, y + 6, 2, 30, GREEN, 2.4); R(x + 94, y + 4, 2, 44, GREEN, 2.2); R(x + 86, y + 6, 1, 30, GREEN, 4.2)
    with prop(cast=(2, 2)):                                     # cushions
        G([(x + 13, y + 7), (x + 26, y + 5), (x + 28, y + 19), (x + 14, y + 21)], RED, 3.6)
        L([(x + 15, y + 9), (x + 25, y + 17)], RED, 4.6); L([(x + 25, y + 7), (x + 16, y + 18)], RED, 2.6)
    with prop(cast=(2, 2)):
        G([(x + 64, y + 8), (x + 78, y + 7), (x + 80, y + 20), (x + 65, y + 22)], FLOOR, 4.6)
        for i in range(3):
            R(x + 66, y + 10 + 4 * i, 13, 1, RED, 4)
    with prop(cast=(2, 2)):                                     # a blanket over the arm
        G([(x + 84, y + 12), (x + 97, y + 11), (x + 98, y + 44), (x + 92, y + 46), (x + 87, y + 43), (x + 83, y + 34)], PAPER, 4.4)
        for i in range(6):
            R(x + 84, y + 15 + 5 * i, 14, 2, TEAL, 3.2)
        R(x + 96, y + 12, 2, 32, PAPER, 3.2)
        for fx in range(86, 97, 2):
            R(x + fx, y + 45, 1, 3, PAPER, 4.4)
    with prop(cast=(1, 1), rim=0):                              # a book left open, face down
        G([(x + 41, y + 26), (x + 49, y + 25), (x + 57, y + 26), (x + 57, y + 33), (x + 49, y + 32), (x + 41, y + 33)], TEAL, 3.4)
        R(x + 49, y + 25, 1, 8, TEAL, 2); R(x + 42, y + 33, 15, 1, PAPER, 5)


def low_table(x, y):
    with prop(cast=(3, 4)):
        R(x + 2, y + 18, 3, 9, DESK, 2.4); R(x + 55, y + 18, 3, 9, DESK, 2); R(x + 8, y + 18, 2, 5, DESK, 1.2); R(x + 50, y + 18, 2, 5, DESK, 1.2)
        R(x, y, 60, 16, DESK, 3.8); R(x + 58, y + 1, 2, 15, DESK, 3)
        for gx, gy, gw in ((5, 3, 20), (30, 8, 22), (12, 12, 26), (40, 4, 12)):
            R(x + gx, y + gy, gw, 1, DESK, 3.3)
        R(x, y + 16, 60, 3, DESK, 2.9); R(x, y + 18, 60, 1, DESK, 2)
    T(x + 5, y + 19, 50, 8, -1.2)
    with prop(cast=(1, 2)):                                     # magazines
        R(x + 4, y + 4, 14, 10, PAPER, 4.6); R(x + 5, y + 2, 14, 10, RED, 3.6); R(x + 6, y + 3, 12, 4, FLOOR, 5.2); R(x + 7, y + 9, 8, 1, PAPER, 5.2)
    with prop(cast=(1, 1)):                                     # remote, controller
        R(x + 22, y + 6, 4, 9, METAL, 1.6); R(x + 23, y + 7, 2, 2, RED, 4.4); R(x + 23, y + 10, 2, 1, METAL, 3.4); R(x + 23, y + 12, 2, 1, METAL, 3.4)
    with prop(cast=(1, 1)):
        R(x + 30, y + 9, 13, 5, PAPER, 4.8); R(x + 30, y + 12, 3, 3, PAPER, 4.8); R(x + 40, y + 12, 3, 3, PAPER, 4.8); R(x + 32, y + 10, 2, 2, METAL, 2); R(x + 39, y + 10, 2, 2, RED, 4.4)
    with prop(cast=(1, 2)):                                     # mug, a small plant
        R(x + 47, y + 7, 6, 7, FLOOR, 5); R(x + 52, y + 7, 1, 7, FLOOR, 3.8); R(x + 48, y + 7, 4, 2, DESK, 1.6); R(x + 53, y + 9, 2, 1, FLOOR, 4.4); R(x + 54, y + 9, 1, 3, FLOOR, 4.4)
    with prop(cast=(1, 2)):
        R(x + 32, y, 7, 6, PAPER, 4.6); R(x + 37, y, 2, 6, PAPER, 3.6); E(x + 30, y - 6, 6, 6, GREEN, 3.6); E(x + 35, y - 7, 6, 7, GREEN, 3); E(x + 33, y - 4, 5, 5, GREEN, 4.2)


def floor_lamp(x, y):
    """x, y: the middle of its foot. The shade glows; the pools are in room_lights()."""
    with prop(cast=(3, 3)):
        E(x - 8, y - 5, 16, 8, METAL, 2); E(x - 7, y - 6, 14, 7, METAL, 3); E(x - 4, y - 5, 7, 3, METAL, 4)
        R(x - 1, y - 52, 2, 49, METAL, 3.2); R(x, y - 52, 1, 49, METAL, 2)
        for i in range(13):
            w = 14 + i - i // 3
            R(x - w // 2, y - 65 + i, w, 1, FLOOR + FLAT, 6); R(x - w // 2 + w - w // 3, y - 65 + i, w // 3, 1, FLOOR + FLAT, 5)
        R(x - 11, y - 52, 22, 1, RED + FLAT, 5)


def armchair(x, y):
    with prop(cast=(3, 4)):
        R(x + 2, y + 43, 4, 3, DESK, 1.6); R(x + 34, y + 43, 4, 3, DESK, 1.6)
        R(x + 7, y, 26, 6, TEAL, 3.7); R(x + 7, y + 6, 26, 15, TEAL, 2.3)                       # the back: top, front
        R(x + 9, y + 6, 22, 14, TEAL, 2.8); R(x + 9, y + 6, 22, 1, TEAL, 3.5); R(x + 14, y + 11, 2, 2, TEAL, 2); R(x + 24, y + 11, 2, 2, TEAL, 2)
        R(x + 8, y + 20, 24, 14, TEAL, 3.3); R(x + 8, y + 20, 24, 2, TEAL, 2); R(x + 8, y + 34, 24, 4, TEAL, 2.6); R(x + 8, y + 34, 24, 1, TEAL, 3.9)
        R(x + 7, y + 38, 26, 5, TEAL, 1.8)
        for ax, d in ((x, 0), (x + 32, -.4)):
            R(ax, y + 5, 8, 27, TEAL, 3.7 + d); R(ax, y + 32, 8, 11, TEAL, 2.6 + d); R(ax, y + 32, 8, 1, TEAL, 4 + d)
        R(x + 7, y + 7, 1, 25, TEAL, 2); R(x + 38, y + 5, 2, 38, TEAL, 1.8); R(x + 32, y + 7, 1, 25, TEAL, 3.9)
    with prop(cast=(2, 2)):                                     # a cushion, an open book on the arm
        G([(x + 10, y + 8), (x + 21, y + 7), (x + 22, y + 19), (x + 11, y + 20)], FLOOR, 4.6); L([(x + 12, y + 10), (x + 20, y + 17)], FLOOR, 3.6)
    with prop(cast=(1, 1), rim=0):
        R(x + 32, y + 12, 9, 12, PAPER, 5.2); R(x + 36, y + 12, 1, 12, PAPER, 3.4)
        for i in range(4):
            R(x + 33, y + 14 + 2 * i, 3, 1, PAPER, 3.6); R(x + 38, y + 14 + 2 * i, 2, 1, PAPER, 3.6)


def cube_shelf(x, y):
    """A white shelf of eight cubes against the wall: records, boxes, games, a speaker; a record player on top."""
    with prop(cast=(3, 4)):
        R(x, y, 96, 7, PAPER, 4.6); R(x, y + 7, 96, 51, PAPER, 3.6); R(x + 93, y + 7, 3, 51, PAPER, 2.6); R(x, y + 57, 96, 1, PAPER, 2.2)
        R(x + 3, y + 58, 4, 2, METAL, 1.2); R(x + 89, y + 58, 4, 2, METAL, 1.2)
        for row in range(2):
            for col in range(4):
                cx, cy = x + 3 + 23 * col, y + 9 + 24 * row
                R(cx, cy, 21, 22, PAPER, 1.3); R(cx, cy, 21, 2, PAPER, .6)
        rnd = random.Random(4)
        for cx, cy in ((x + 3, y + 9), (x + 26, y + 33)):                                       # records
            px = cx + 1
            while px < cx + 19:
                c = rnd.choice((RED, TEAL, PAPER, METAL, FLOOR, GREEN, DESK, CARD)); w = rnd.choice((1, 1, 2))
                R(px, cy + 3, w, 19, c, rnd.choice((3, 3.6, 4.2))); px += w
            R(cx + 1, cy + 3, 18, 1, PAPER, 2.2)
        for cx, cy, c, l in ((x + 26, y + 9, CARD, 3.4), (x + 3, y + 33, TEAL, 2.8), (x + 72, y + 33, CARD, 3)):   # boxes
            R(cx + 1, cy + 4, 19, 18, c, l); R(cx + 1, cy + 4, 19, 1, c, l + .9); R(cx + 18, cy + 4, 2, 18, c, l - .8)
            R(cx + 6, cy + 9, 9, 5, PAPER, 4.8); R(cx + 8, cy + 11, 5, 1, PAPER, 3)
        cx, cy = x + 49, y + 9                                                                 # books, a small plant
        m.book_row(cx + 1, cy + 22, cx + 13, rnd, 12, 17)
        R(cx + 14, cy + 16, 6, 6, RED, 3.4); E(cx + 13, cy + 10, 6, 6, GREEN, 3.4); E(cx + 16, cy + 9, 5, 6, GREEN, 4.2)
        cx, cy = x + 72, y + 9                                                                 # a speaker
        R(cx + 3, cy + 3, 15, 19, METAL, 1.8); R(cx + 3, cy + 3, 15, 1, METAL, 2.8); E(cx + 6, cy + 5, 9, 7, METAL, 1); E(cx + 8, cy + 7, 5, 3, METAL, 2.6)
        E(cx + 8, cy + 14, 6, 5, METAL, 1); R(cx + 10, cy + 16, 2, 1, METAL, 2.6)
        cx, cy = x + 49, y + 33                                                                # board games, in a pile
        for i, (c, w) in enumerate(((RED, 19), (TEAL, 17), (FLOOR, 19), (PAPER, 15), (GREEN, 18))):
            R(cx + 1 + i % 2, cy + 18 - 4 * i, w, 4, c, 3.6); R(cx + 1 + i % 2, cy + 21 - 4 * i, w, 1, c, 2.4); R(cx + 4, cy + 19 - 4 * i, 6, 1, PAPER, 5)
    with prop(cast=(2, 2)):                                     # on top: the record player,
        R(x + 4, y - 4, 30, 6, DESK, 3); R(x + 4, y - 9, 30, 6, DESK, 3.9); E(x + 7, y - 9, 16, 6, METAL, 1); E(x + 13, y - 7, 4, 2, RED, 4.4)
        L([(x + 30, y - 8), (x + 24, y - 5)], PAPER, 5); R(x + 29, y - 9, 3, 2, METAL, 3.6)
    with prop(cast=(1, 2)):                                     # a lamp,
        R(x + 44, y - 2, 8, 3, METAL, 2); R(x + 47, y - 8, 2, 6, METAL, 3)
        for i in range(8):
            w = 8 + i
            R(x + 48 - w // 2, y - 16 + i, w, 1, FLOOR + FLAT, 6); R(x + 48 - w // 2 + w - w // 3, y - 16 + i, w // 3, 1, FLOOR + FLAT, 5)
    with prop(cast=(1, 2)):                                     # a plant, a photo
        R(x + 62, y - 6, 9, 8, PAPER, 4.6); R(x + 69, y - 6, 2, 8, PAPER, 3.4)
        for lx, ly, l in ((60, -13, 3.4), (66, -16, 4.2), (70, -12, 3), (63, -19, 3.8), (68, -21, 3.2), (58, -9, 3)):
            E(x + lx, y + ly, 6, 7, GREEN, l)
    with prop(cast=(1, 1)):
        R(x + 78, y - 10, 12, 12, DESK, 3.4); R(x + 80, y - 8, 8, 8, PAPER, 5); R(x + 82, y - 6, 4, 6, RED, 3.6); R(x + 83, y - 7, 2, 2, CARD, 4.6)


def desk2(x, y):
    """A second desk: a white top on a trestle and a painted drawer unit; laptop, tablet, sketchbook, an arm lamp."""
    with prop(cast=(3, 4)):
        L([(x + 5, y + 27), (x + 3, y + 50)], METAL, 2.6, 2); L([(x + 24, y + 27), (x + 27, y + 50)], METAL, 2, 2); R(x + 4, y + 39, 22, 2, METAL, 2.4)
        R(x + 30, y + 27, 32, 9, PAPER, 1.1)
        R(x + 62, y + 27, 32, 22, TEAL, 2.5); R(x + 91, y + 27, 3, 22, TEAL, 1.6); R(x + 62, y + 27, 32, 2, TEAL, 1.4)
        for i in range(3):
            R(x + 64, y + 30 + 6 * i, 26, 5, TEAL, 3); R(x + 64, y + 30 + 6 * i, 26, 1, TEAL, 3.8); R(x + 74, y + 32 + 6 * i, 6, 1, PAPER, 5)
        R(x + 64, y + 49, 4, 2, METAL, 1.2); R(x + 88, y + 49, 4, 2, METAL, 1.2)
        R(x + 82, y + 37, 5, 4, FLOOR, 5.4); R(x + 66, y + 43, 4, 3, RED, 4.4)                     # stickers
        R(x, y, 96, 24, PAPER, 4); R(x + 93, y + 2, 3, 22, PAPER, 3.3)
        E(x + 44, y + 16, 8, 6, PAPER, 3.7); E(x + 45, y + 17, 6, 4, PAPER, 4.3)
        R(x, y + 24, 96, 3, PAPER, 3.3); R(x, y + 26, 96, 1, PAPER, 2.2)
    T(x + 7, y + 36, 54, 15, -1.3)
    with prop(cast=(2, 3)):                                     # a bag under it
        R(x + 34, y + 36, 20, 14, CARD, 3); R(x + 34, y + 36, 20, 2, CARD, 3.8); R(x + 51, y + 36, 3, 14, CARD, 2.2); L([(x + 38, y + 36), (x + 43, y + 30), (x + 49, y + 36)], CARD, 2.2)
        R(x + 39, y + 42, 9, 4, RED, 3.6)
    with prop(cast=(3, 3)):                                     # laptop on a stand: a drawing, not code
        R(x + 30, y + 6, 26, 3, METAL, 2.4); R(x + 28, y - 13, 30, 19, METAL, 2.2); R(x + 28, y - 13, 30, 1, METAL, 3.4); R(x + 57, y - 13, 1, 19, METAL, 1.4)
        sx, sy = x + 29, y - 12
        R(sx, sy, 28, 17, PAPER + FLAT, 4); R(sx, sy, 28, 2, METAL + FLAT, 1); R(sx, sy + 2, 4, 15, METAL + FLAT, 2)
        E(sx + 8, sy + 5, 9, 9, RED + FLAT, 4); R(sx + 15, sy + 8, 9, 7, TEAL + FLAT, 4); G([(sx + 6, sy + 15), (sx + 12, sy + 9), (sx + 16, sy + 15)], FLOOR + FLAT, 5)
        for i, c in enumerate((RED, FLOOR, TEAL, GREEN)):
            R(sx + 1, sy + 4 + 3 * i, 2, 2, c + FLAT, 4)
    with prop(cast=(2, 2)):                                     # keyboard, tablet and pen
        R(x + 30, y + 12, 26, 8, METAL, 3.8); R(x + 30, y + 19, 26, 1, METAL, 2.4)
        for row in range(3):
            R(x + 31, y + 13 + 2 * row, 24, 1, METAL, 2.6)
    with prop(cast=(2, 2)):
        R(x + 61, y + 6, 24, 15, METAL, 1.6); R(x + 63, y + 8, 18, 11, METAL, 2.8); R(x + 82, y + 9, 2, 2, METAL, 3.4); R(x + 82, y + 13, 2, 2, METAL, 3.4)
        L([(x + 66, y + 16), (x + 74, y + 10)], PAPER, 5.4)
    with prop(cast=(1, 2)):                                     # sketchbook, colour chips
        R(x + 4, y + 7, 17, 14, METAL, 2); R(x + 5, y + 6, 16, 14, PAPER, 5.2); R(x + 5, y + 6, 2, 14, METAL, 2.4)
        E(x + 9, y + 8, 8, 6, FLOOR, 5); L([(x + 9, y + 16), (x + 18, y + 15)], PAPER, 3.4); L([(x + 9, y + 18), (x + 15, y + 18)], PAPER, 3.4); R(x + 12, y + 10, 3, 3, RED, 4)
    with prop(cast=(1, 1), rim=0):
        for i, c in enumerate((RED, FLOOR, GREEN, TEAL)):
            R(x + 21 + 2 * i, y + 15 + i, 5, 7, c, 4.2 if c != TEAL else 3.6)
    with prop(cast=(1, 2)):                                     # a jar of brushes, a mug
        R(x + 6, y - 4, 7, 8, PAPER, 4.4); R(x + 11, y - 4, 2, 8, PAPER, 3.4)
        for i, c in enumerate((DESK, RED, FLOOR)):
            R(x + 7 + 2 * i, y - 11 + i % 2, 1, 7, c, 3.6); R(x + 7 + 2 * i, y - 12 + i % 2, 1, 2, (PAPER, TEAL, RED)[i], 4.4)
    with prop(cast=(1, 2)):
        R(x + 87, y + 13, 7, 8, GREEN, 3.4); R(x + 92, y + 13, 2, 8, GREEN, 2.4); R(x + 88, y + 13, 5, 2, DESK, 1.6); R(x + 85, y + 15, 2, 4, GREEN, 3)
    with prop(cast=(2, 3)):                                     # an arm lamp: the head glows underneath
        R(x + 84, y + 1, 9, 3, METAL, 2); L([(x + 88, y + 1), (x + 91, y - 11)], METAL, 3.4); L([(x + 91, y - 11), (x + 80, y - 19)], METAL, 3.4)
        R(x + 90, y - 12, 2, 2, METAL, 2)
        for i in range(6):
            R(x + 76 - i, y - 22 + i, 6 + 2 * i, 1, RED, 3.6 - (i > 3) * .8)
        R(x + 70, y - 16, 18, 1, FLOOR + FLAT, 6)
    note(x + 59, y - 10, 6, 6, FLOOR, 5.4, 1)


def cabinet(x, y):
    """A low cabinet with the printer on it, by the right wall."""
    with prop(cast=(3, 4)):
        R(x, y, 56, 11, DESK, 3.9); R(x, y + 11, 56, 19, DESK, 2.8); R(x + 53, y + 11, 3, 19, DESK, 2); R(x, y + 11, 56, 1, DESK, 2)
        for i in range(2):
            R(x + 3 + 26 * i, y + 13, 24, 15, DESK, 3.2); R(x + 3 + 26 * i, y + 13, 24, 1, DESK, 4); R(x + 23 - 18 * i + 26 * i, y + 19, 2, 4, METAL, 4.2)
        R(x + 2, y + 30, 4, 2, DESK, 1.6); R(x + 50, y + 30, 4, 2, DESK, 1.6)
    with prop(cast=(2, 3)):                                     # the printer, a sheet half out
        R(x + 5, y - 12, 30, 5, PAPER, 4.8); R(x + 5, y - 7, 30, 12, PAPER, 3.9); R(x + 33, y - 7, 2, 12, PAPER, 3)
        R(x + 8, y - 3, 22, 2, METAL, 1.2); R(x + 10, y - 2, 18, 9, PAPER, 5.4); R(x + 12, y + 1, 12, 1, PAPER, 3.6); R(x + 12, y + 3, 9, 1, PAPER, 3.6)
        R(x + 30, y - 11, 2, 2, GREEN + FLAT, 5); R(x + 9, y - 15, 18, 3, PAPER, 5.4)
    with prop(cast=(1, 2)):                                     # a ream of paper, a stapler
        R(x + 39, y - 3, 14, 4, PAPER, 5.2); R(x + 39, y + 1, 14, 5, PAPER, 4.2); R(x + 39, y + 3, 14, 1, TEAL, 3.4)
        R(x + 41, y - 6, 8, 3, RED, 3.8)


def amp(x, y):
    """A guitar amp with the guitar leaning on it."""
    with prop(cast=(3, 4)):
        R(x, y, 26, 7, METAL, 2.6); R(x, y + 7, 26, 21, METAL, 1.6); R(x + 24, y + 7, 2, 21, METAL, 1)
        R(x + 2, y + 13, 21, 13, CARD, 2.6)
        for gy in range(14, 26, 2):
            R(x + 3, y + gy, 19, 1, CARD, 3.4)
        R(x + 2, y + 9, 21, 3, FLOOR, 4.6)
        for i in range(5):
            R(x + 4 + 4 * i, y + 10, 2, 1, METAL, 1)
        R(x + 21, y + 10, 1, 1, RED + FLAT, 5); R(x + 8, y + 2, 10, 2, METAL, 1)
    with prop(cast=(2, 3)):                                     # the guitar
        L([(x + 37, y + 12), (x + 31, y - 22)], DESK, 2.4, 3); L([(x + 37, y + 12), (x + 31, y - 22)], PAPER, 5)
        R(x + 28, y - 28, 5, 7, DESK, 3.4); R(x + 27, y - 26, 1, 1, PAPER, 5); R(x + 33, y - 24, 1, 1, PAPER, 5)
        E(x + 30, y + 4, 14, 12, RED, 3.2); E(x + 28, y + 12, 18, 16, RED, 3.2); E(x + 31, y + 14, 12, 11, FLOOR, 4.8); E(x + 34, y + 16, 6, 6, FLOOR, 5.6)
        E(x + 35, y + 17, 4, 4, DESK, 1.2); R(x + 34, y + 23, 6, 2, DESK, 2); L([(x + 37, y + 6), (x + 37, y + 23)], PAPER, 5)


def paint_cans(x, y):
    for i, (dx, dy, c) in enumerate(((0, 4, RED), (11, 6, TEAL), (5, -5, FLOOR))):
        with prop(cast=(2, 2)):
            R(x + dx, y + dy, 10, 3, METAL, 4.2); R(x + dx, y + dy + 3, 10, 9, METAL, 3); R(x + dx + 8, y + dy + 3, 2, 9, METAL, 2)
            R(x + dx + 1, y + dy + 5, 7, 4, PAPER, 4.6); R(x + dx + 2, y + dy + 6, 4, 2, c, 4); R(x + dx + 3, y + dy, 5, 2, c, 4)
            R(x + dx + 6, y + dy + 3, 2, 5, c, 3.6)                # a run down the side


def pingpong(x, y):
    with prop(cast=(3, 4)):
        for lx in (6, 83):
            R(x + lx, y + 41, 3, 13, METAL, 2.6); R(x + lx - 2, y + 53, 7, 2, METAL, 1.4)
        R(x + 14, y + 41, 2, 8, METAL, 1.4); R(x + 76, y + 41, 2, 8, METAL, 1.4); R(x + 8, y + 46, 76, 1, METAL, 1.8)
        R(x, y, 92, 38, GREEN, 2.3); R(x, y + 38, 92, 3, METAL, 2.6); R(x, y + 40, 92, 1, METAL, 1.4)
        R(x, y, 92, 1, PAPER, 5); R(x, y + 37, 92, 1, PAPER, 5); R(x, y, 1, 38, PAPER, 5); R(x + 91, y, 1, 38, PAPER, 5); R(x, y + 18, 92, 1, PAPER, 4.4)
        for sx, sy, sw in ((10, 6, 14), (58, 27, 18), (66, 9, 10)):     # scuffs
            R(x + sx, y + sy, sw, 1, GREEN, 2.8)
    T(x + 9, y + 42, 74, 12, -1.2)
    with prop(cast=(2, 1)):                                     # the net
        R(x + 45, y - 5, 2, 44, PAPER, 3.6); R(x + 45, y - 5, 1, 44, PAPER, 5.2)
        for ny in range(y - 3, y + 38, 2):
            R(x + 46, ny, 1, 1, METAL, 1.6)
        R(x + 44, y - 7, 4, 3, METAL, 2); R(x + 44, y + 38, 4, 4, METAL, 2)
    with prop(cast=(1, 1)):                                     # bats, the ball, a mug that should not be there
        E(x + 14, y + 22, 9, 10, RED, 3.6); E(x + 16, y + 23, 4, 4, RED, 4.6); R(x + 22, y + 30, 5, 2, CARD, 4.4)
    with prop(cast=(1, 1)):
        E(x + 68, y + 5, 9, 10, METAL, 1.8); R(x + 65, y + 3, 4, 3, CARD, 4.4)
    with prop(cast=(1, 1)):
        R(x + 60, y + 21, 2, 2, PAPER, 6)
    with prop(cast=(1, 2)):
        R(x + 80, y + 26, 7, 7, PAPER, 5); R(x + 85, y + 26, 2, 7, PAPER, 3.6); R(x + 81, y + 26, 5, 2, DESK, 1.6); R(x + 78, y + 28, 2, 4, PAPER, 4)


def beanbag(x, y):
    with prop(cast=(3, 3), rim=.6):
        E(x, y + 7, 28, 19, FLOOR, 3.8); E(x + 1, y + 2, 26, 19, FLOOR, 4.6); E(x + 4, y + 3, 10, 6, FLOOR, 5.4)
        E(x + 6, y + 7, 17, 9, FLOOR, 3.8); E(x + 7, y + 8, 15, 6, FLOOR, 4.2)            # where someone sat
        L([(x + 3, y + 17), (x + 9, y + 22), (x + 19, y + 23)], FLOOR, 3.6); L([(x + 24, y + 9), (x + 26, y + 17)], FLOOR, 3.6)
    with prop(cast=(1, 1), rim=0):                              # and left a comic
        G([(x + 9, y + 8), (x + 17, y + 7), (x + 18, y + 13), (x + 10, y + 14)], PAPER, 5.2); R(x + 11, y + 9, 3, 3, RED, 4); R(x + 15, y + 9, 2, 3, TEAL, 3.4)


def cushion(x, y, c, l):
    with prop(cast=(2, 2)):
        E(x, y + 2, 20, 11, c, l - 1); E(x, y, 20, 11, c, l); E(x + 3, y + 1, 9, 4, c, l + .8); R(x + 9, y + 5, 2, 2, c, l - 1.2)


def round_rug(x, y, w, h):
    with thing(False), prop(cast=None, rim=0):
        for i, (c, l) in enumerate(((CARD, 3.4), (TEAL, 2.6), (CARD, 4.2), (RED, 3.3), (CARD, 3.8), (PAPER, 4.6), (TEAL, 2.8))):
            d = (0, 3, 5, 12, 14, 22, 30)[i]
            if w - 2 * d > 4 and h - 1.4 * d > 3:
                E(x + d, y + round(d * .7), w - 2 * d, h - round(d * 1.4), c, l)
        rnd = random.Random(9)
        for _ in range(8):
            T(x + 10 + rnd.randrange(w - 30), y + 6 + rnd.randrange(h - 14), rnd.randrange(4, 10), 1, .7)


def banner(x, y):
    """A banner being painted on the floor: two letters done, the rest in pencil; brush, drips."""
    with thing(False):
        with prop(cast=(1, 1), rim=0):
            G([(x, y + 4), (x + 118, y), (x + 121, y + 39), (x + 3, y + 44)], PAPER, 4.7)
            G([(x + 108, y + 40), (x + 121, y + 39), (x + 120, y + 30)], PAPER, 3.6)             # a corner that curls
            for i, ch in enumerate('HELLO'):
                lx, ly = x + 9 + 21 * i, y + 9 - i // 2
                c, l = ((RED, 3.5), (TEAL, 3), (FLOOR, 4.9), (PAPER, 3.9), (PAPER, 3.9))[i]
                R(lx, ly, 5, 26, c, l)
                if ch == 'H':
                    R(lx + 11, ly, 5, 26, c, l); R(lx, ly + 10, 16, 5, c, l)
                elif ch == 'E':
                    R(lx, ly, 16, 5, c, l); R(lx, ly + 10, 12, 5, c, l); R(lx, ly + 21, 16, 5, c, l)
                elif ch == 'L':
                    R(lx, ly + 21, 16 if i == 3 else 9, 5, c, l)                                # the third is half done
                else:
                    R(lx + 11, ly, 5, 26, c, l); R(lx, ly, 16, 5, c, l); R(lx, ly + 21, 16, 5, c, l)
            for dx, dy, c in ((6, 38, RED), (30, 5, RED), (47, 40, TEAL), (60, 37, FLOOR), (58, 30, FLOOR), (-6, 20, RED), (40, 48, TEAL)):
                R(x + dx, y + dy, 2, 2, c, 4 if c != TEAL else 3.2)                               # drips
        with prop(cast=(1, 1)):                                 # the brush, a saucer of paint
            L([(x + 62, y + 22), (x + 72, y + 30)], DESK, 3.4, 2); R(x + 60, y + 20, 4, 3, FLOOR, 5.4)
            E(x + 74, y + 34, 10, 7, PAPER, 5.2); E(x + 76, y + 35, 6, 4, FLOOR, 5)


def drafting(x, y):
    """A drawing table, the board tipped towards us: a plan taped to it, a T-square, a lamp clamped on."""
    with prop(cast=(3, 4)):
        R(x + 4, y + 36, 3, 16, METAL, 2.6); R(x + 53, y + 36, 3, 16, METAL, 2); R(x + 7, y + 45, 46, 2, METAL, 1.8)
        R(x + 1, y + 51, 9, 2, METAL, 1.4); R(x + 50, y + 51, 9, 2, METAL, 1.4)
        R(x, y, 60, 33, DESK, 3.5); R(x + 58, y + 1, 2, 32, DESK, 2.6); R(x, y + 33, 60, 2, DESK, 4.3); R(x, y + 35, 60, 3, DESK, 2.4)
        R(x + 3, y + 3, 53, 27, PAPER, 5.1)
        for bx, by, bw, bh in ((7, 6, 20, 12), (27, 6, 14, 8), (27, 14, 14, 11), (7, 18, 12, 7)):       # a plan
            R(x + bx, y + by, bw, bh, METAL, 2.2); R(x + bx + 1, y + by + 1, bw - 2, bh - 2, PAPER, 5.1)
        R(x + 13, y + 17, 4, 2, PAPER, 5.1); R(x + 33, y + 13, 3, 2, PAPER, 5.1); R(x + 19, y + 21, 2, 3, PAPER, 5.1)   # doors
        E(x + 44, y + 7, 9, 8, RED, 4.2); R(x + 45, y + 19, 8, 1, METAL, 2.6); R(x + 45, y + 22, 6, 1, METAL, 2.6); R(x + 45, y + 25, 8, 1, TEAL, 3)
        for tx, ty in ((2, 2), (54, 2), (2, 28), (54, 28)):
            R(x + tx, y + ty, 3, 3, FLOOR, 5.4)                   # tape
    with prop(cast=(1, 1)):                                     # T-square, pencils on the ledge
        R(x + 1, y + 12, 3, 12, TEAL, 2.6); R(x + 4, y + 17, 40, 2, TEAL, 3.6); R(x + 4, y + 18, 40, 1, TEAL, 2.6)
    with prop(cast=(1, 1), rim=0):
        R(x + 10, y + 33, 9, 1, FLOOR, 5.6); R(x + 24, y + 33, 7, 1, RED, 4.2); R(x + 36, y + 32, 4, 2, PAPER, 5.4)
    with prop(cast=(2, 3)):                                     # the lamp
        R(x + 50, y - 2, 4, 4, METAL, 2); L([(x + 52, y - 2), (x + 55, y - 14)], METAL, 3.4); L([(x + 55, y - 14), (x + 44, y - 20)], METAL, 3.4)
        for i in range(5):
            R(x + 40 - i, y - 23 + i, 6 + 2 * i, 1, TEAL, 3.4 - (i > 2) * .8)
        R(x + 35, y - 18, 16, 1, FLOOR + FLAT, 6)
    light(1 if m.EVE else .5, 2.5, [(x + 30, y - 16), (x + 56, y - 16), (x + 62, y + 8), (x + 50, y + 26), (x + 26, y + 22), (x + 22, y + 2)])
    if m.EVE:
        light(.8, 4, [(x + 6, y - 6), (x + 60, y - 12), (x + 78, y + 20), (x + 64, y + 50), (x + 20, y + 54), (x - 2, y + 26)])
        light(.5, 6, [(x - 14, y + 30), (x + 50, y + 22), (x + 84, y + 44), (x + 70, y + 84), (x + 4, y + 88)])


def cable(pts, c=METAL, l=.8, tape=()):
    with prop(cast=(1, 1), rim=0):
        L(pts, c, l)
    for tx, ty in tape:
        with prop(cast=None, rim=0):
            R(tx, ty, 7, 3, PAPER, 5); R(tx, ty + 2, 7, 1, PAPER, 4)


def tall_plant(x, y):
    """A snake plant: blades straight up out of a white pot. x, y: the pot."""
    for i, (dx, h, l) in enumerate(((1, 30, 3), (5, 41, 3.8), (8, 34, 3.2), (11, 44, 4), (13, 27, 3), (-1, 22, 3.4), (15, 23, 2.8))):
        tip = x + dx + 1 + (i % 3 - 1) * 2
        with prop(cast=(2, 3), rim=0):
            G([(x + dx, y + 3), (x + dx + 3, y + 3), (tip, y - h)], GREEN, l)
            L([(x + dx, y + 2), (tip, y - h + 3)], GREEN, l + 1.2)
            for by in range(y - h + 6, y, 5):
                R(x + dx + 1, by, 2, 1, GREEN, l - .8)
    with prop(cast=(3, 4)):
        R(x, y, 16, 3, PAPER, 4.8); R(x + 1, y + 3, 14, 11, PAPER, 4); R(x + 12, y + 3, 3, 11, PAPER, 3); R(x + 1, y + 13, 14, 1, PAPER, 2.4)
        R(x + 3, y + 7, 8, 1, TEAL, 3.2)


def arcade(x, y):
    """An arcade cabinet by the wall: marquee and screen are lit, day and evening."""
    with prop(cast=(3, 4)):
        R(x, y, 30, 6, METAL, 2.8); R(x, y + 6, 30, 52, METAL, 1.7); R(x + 27, y + 6, 3, 52, METAL, 1)
        R(x + 2, y + 7, 26, 7, RED + FLAT, 4)
        for mx, mw in ((5, 3), (10, 5), (17, 3), (22, 3)):
            R(x + mx, y + 9, mw, 3, FLOOR + FLAT, 6)
        R(x + 2, y + 15, 26, 18, METAL, .8); R(x + 4, y + 17, 22, 14, TEAL + FLAT, 1)
        for i in range(4):
            R(x + 6 + 5 * i, y + 19, 3, 2, GREEN + FLAT, 4); R(x + 7 + 5 * i, y + 22, 3, 2, RED + FLAT, 4)
        R(x + 13, y + 28, 4, 2, PAPER + FLAT, 5); R(x + 15, y + 25, 1, 2, FLOOR + FLAT, 6); R(x + 21, y + 26, 2, 2, FLOOR + FLAT, 5)
        R(x, y + 33, 30, 6, METAL, 3); R(x, y + 38, 30, 1, METAL, 1.2)
        R(x + 7, y + 32, 2, 4, PAPER, 4.4); R(x + 6, y + 30, 4, 3, RED, 4.4)
        R(x + 16, y + 35, 3, 2, FLOOR, 5.4); R(x + 21, y + 34, 3, 2, TEAL, 4.4)
        R(x + 3, y + 41, 24, 3, FLOOR, 4.6); R(x + 3, y + 45, 24, 2, RED, 3.6)
        R(x + 10, y + 49, 10, 7, METAL, 1); R(x + 13, y + 51, 2, 3, RED + FLAT, 5); R(x + 17, y + 51, 1, 3, METAL, 3)
        R(x + 1, y + 58, 28, 2, METAL, .8)
    light(.9 if m.EVE else .4, 3, [(x - 2, y + 36), (x + 30, y + 36), (x + 30, y + 62), (x + 22, y + 78), (x - 14, y + 80), (x - 12, y + 56)])
    if m.EVE:
        light(.6, 5, [(x - 22, y + 46), (x + 30, y + 44), (x + 30, y + 96), (x - 4, y + 110), (x - 40, y + 92)])


def rack(x, y):
    """Metal shelving in the storage corner: boxes, tins, a toolbox."""
    with prop(cast=(3, 4)):
        R(x, y, 60, 5, METAL, 3.8); R(x, y + 5, 60, 60, METAL, 1); R(x, y + 5, 2, 61, METAL, 3.2); R(x + 58, y + 5, 2, 61, METAL, 2.2)
        for i in range(3):
            R(x, y + 22 + 20 * i, 60, 3, METAL, 3.6); R(x, y + 24 + 20 * i, 60, 1, METAL, 2.2)
        b = y + 22                                               # top bay: two boxes, tubes
        for bx, w, h, t in ((4, 18, 13, 0), (24, 14, 10, .4)):
            R(x + bx, b - h, w, h, CARD, 3.2 + t); R(x + bx, b - h, w, 1, CARD, 4.2 + t); R(x + bx + w - 2, b - h, 2, h, CARD, 2.4 + t); R(x + bx + 3, b - h + 4, 7, 4, PAPER, 5)
        for i, c in enumerate((PAPER, TEAL, PAPER)):
            R(x + 42 + 5 * i, b - 15 + 2 * i, 4, 15 - 2 * i, c, 4.4 if c == PAPER else 3.4); R(x + 45 + 5 * i, b - 15 + 2 * i, 1, 15 - 2 * i, c, 3)
        b = y + 42                                               # middle bay: tins, a toolbox
        for i, c in enumerate((RED, FLOOR, TEAL)):
            R(x + 4 + 9 * i, b - 11, 8, 11, METAL, 3.2); R(x + 4 + 9 * i, b - 11, 8, 2, METAL, 4.2); R(x + 5 + 9 * i, b - 7, 6, 4, c, 4); R(x + 10 + 9 * i, b - 9, 2, 9, METAL, 2.2)
        R(x + 34, b - 10, 22, 10, RED, 3.2); R(x + 34, b - 10, 22, 2, RED, 4.2); R(x + 54, b - 8, 2, 8, RED, 2.2); R(x + 41, b - 13, 8, 2, METAL, 3.6); R(x + 43, b - 6, 4, 2, METAL, 4)
        b = y + 62                                               # bottom bay: a big box, a coil of cable
        R(x + 4, b - 15, 30, 15, CARD, 3); R(x + 4, b - 15, 30, 1, CARD, 4); R(x + 31, b - 15, 3, 15, CARD, 2.2); R(x + 17, b - 15, 4, 8, PAPER, 4.4); R(x + 7, b - 8, 8, 5, PAPER, 5)
        E(x + 38, b - 14, 17, 14, METAL, 1.8); E(x + 41, b - 11, 11, 8, METAL, 1); E(x + 44, b - 9, 5, 4, METAL, 2.6)
    with prop(cast=(2, 3)):                                     # on top: a box, a hard hat
        R(x + 6, y - 14, 24, 7, CARD, 4.2); R(x + 6, y - 7, 24, 10, CARD, 3.2); R(x + 28, y - 7, 2, 10, CARD, 2.4); R(x + 16, y - 14, 4, 11, PAPER, 4.6)
    with prop(cast=(1, 2)):
        E(x + 38, y - 9, 15, 11, FLOOR, 4.8); R(x + 36, y - 2, 19, 3, FLOOR, 4); E(x + 41, y - 8, 6, 4, FLOOR, 5.6)


def drying_rack(x, y):
    """A clothes horse with the week's washing."""
    with prop(cast=(3, 4)):
        for ex in (x + 2, x + 51):
            L([(ex, y + 2), (ex + 3, y + 38)], PAPER, 3.6); L([(ex + 3, y + 2), (ex, y + 38)], PAPER, 3); R(ex - 1, y + 37, 6, 2, METAL, 1.6)
        for i in range(4):
            R(x, y + 3 * i, 56, 1, PAPER, 4.8 - i * .2)
    with prop(cast=(1, 2)):                                     # a shirt on the far rail
        R(x + 6, y - 3, 14, 6, GREEN, 3.4); R(x + 6, y - 3, 14, 1, GREEN, 4.2); R(x + 12, y - 3, 2, 3, GREEN, 2.4)
    with prop(cast=(2, 3)):                                     # tee
        R(x + 5, y + 8, 14, 17, RED, 3.3); R(x + 3, y + 8, 2, 6, RED, 3.3); R(x + 19, y + 8, 2, 6, RED, 2.5); R(x + 3, y + 7, 18, 2, RED, 4.2)
        R(x + 9, y + 9, 6, 2, RED, 2.3); R(x + 17, y + 12, 2, 13, RED, 2.5); R(x + 8, y + 15, 6, 4, PAPER, 5)
    with prop(cast=(2, 3)):                                     # towel
        R(x + 23, y + 3, 11, 28, TEAL, 3); R(x + 23, y + 3, 11, 2, TEAL, 4); R(x + 32, y + 5, 2, 26, TEAL, 2.2); R(x + 23, y + 24, 11, 1, PAPER, 5); R(x + 23, y + 27, 11, 1, PAPER, 5)
    with prop(cast=(2, 3)):                                     # jeans
        R(x + 36, y + 6, 12, 26, METAL, 2.4); R(x + 36, y + 6, 12, 2, METAL, 3.4); R(x + 41, y + 10, 1, 22, METAL, 1.4); R(x + 46, y + 8, 2, 24, METAL, 1.6); R(x + 37, y + 30, 4, 1, METAL, 3.4)
    with prop(cast=(1, 2)):                                     # socks
        R(x + 50, y + 3, 3, 10, PAPER, 5); R(x + 50, y + 11, 3, 2, RED, 4); R(x + 54, y + 3, 3, 9, PAPER, 5); R(x + 54, y + 10, 3, 2, TEAL, 3.6)


def bench(x, y):
    """The bench by the door: shoes under it, a bag and a helmet on it."""
    with prop(cast=(2, 3)):
        R(x + 3, y + 11, 3, 12, DESK, 2.6); R(x + 50, y + 11, 3, 12, DESK, 2.2); R(x + 6, y + 14, 44, 1, DESK, 1.6)
        for i, c in enumerate((PAPER, PAPER, RED, RED, METAL, METAL)):       # shoes
            sx = x + 9 + 7 * i + (i // 2) * 2
            R(sx, y + 16, 6, 6, c, 4.4 if c == PAPER else 3.2 if c == RED else 2); R(sx, y + 21, 6, 1, PAPER, 5)
        R(x, y, 56, 9, FLOOR, 4.5); R(x, y + 4, 56, 1, FLOOR, 3.8); R(x, y + 9, 56, 3, FLOOR, 3.6); R(x, y + 11, 56, 1, FLOOR, 2.4)
    with prop(cast=(2, 2)):                                     # a bag
        L([(x + 9, y - 3), (x + 13, y - 11), (x + 18, y - 3)], METAL, 2)
        R(x + 6, y - 5, 16, 11, TEAL, 3); R(x + 6, y - 5, 16, 2, TEAL, 3.9); R(x + 19, y - 3, 3, 9, TEAL, 2.2); R(x + 10, y - 1, 7, 4, PAPER, 5)
    with prop(cast=(1, 2)):                                     # a helmet
        E(x + 34, y - 6, 16, 12, RED, 3.4); E(x + 36, y - 5, 8, 5, RED, 4.4); R(x + 34, y + 1, 16, 3, RED, 2.4)
        for i in range(3):
            R(x + 39 + 4 * i, y - 3, 2, 3, METAL, 1.2)


def shoe_rack(x, y):
    with prop(cast=(2, 3)):
        R(x, y + 2, 2, 18, DESK, 3); R(x + 26, y + 2, 2, 18, DESK, 2.2); R(x, y + 2, 28, 3, DESK, 3.8); R(x, y + 11, 28, 2, DESK, 3.2); R(x + 2, y + 5, 24, 6, DESK, 1); R(x + 2, y + 13, 24, 6, DESK, 1)
        for i, c in enumerate((PAPER, PAPER, METAL, METAL)):
            R(x + 3 + 6 * i, y + 6, 5, 5, c, 4.6 if c == PAPER else 2.4); R(x + 3 + 6 * i, y + 10, 5, 1, PAPER, 5.2)
        for i, c in enumerate((FLOOR, FLOOR, GREEN, GREEN)):
            R(x + 3 + 6 * i, y + 14, 5, 5, c, 4.6 if c == FLOOR else 3.2); R(x + 3 + 6 * i, y + 18, 5, 1, PAPER, 5.2)
    with prop(cast=(1, 2)):                                     # boots on top
        R(x + 4, y - 7, 6, 9, RED, 3.2); R(x + 4, y - 1, 9, 3, RED, 3.2); R(x + 15, y - 6, 6, 8, RED, 3.2); R(x + 15, y - 1, 9, 3, RED, 2.6); R(x + 4, y - 7, 6, 1, RED, 4.2)
    with prop(cast=(1, 2)):                                     # an umbrella against the wall
        L([(x + 32, y + 18), (x + 34, y - 18)], TEAL, 2.6, 2); R(x + 33, y - 22, 4, 2, DESK, 3); R(x + 36, y - 22, 1, 5, DESK, 3)


def kilim(x, y, w, h):
    """The runner by the door: tan, with teal bands and a row of lozenges."""
    with thing(False), prop(cast=None, rim=0):
        for fy in range(y + 1, y + h - 1, 2):
            R(x - 4, fy, 4, 1, PAPER, 4 - (fy % 4) * .2); R(x + w, fy, 4 + (fy % 5 == 0), 1, PAPER, 4)
        R(x, y, w, h, CARD, 3.6); R(x, y, w, 4, TEAL, 2.6); R(x, y + h - 4, w, 4, TEAL, 2.6)
        R(x, y + 5, w, 1, PAPER, 4.8); R(x, y + h - 6, w, 1, PAPER, 4.8); R(x, y, 3, h, TEAL, 2.6); R(x + w - 3, y, 3, h, TEAL, 2.6)
        mid = y + h // 2
        for sx in range(x + 6, x + w - 6, 4):
            R(sx, y + 8 + (sx // 4) % 2, 2, 1, RED, 3.4); R(sx, y + h - 10 + (sx // 4) % 2, 2, 1, RED, 3.4)
        for i, cx in enumerate(range(x + 17, x + w - 12, 22)):
            c, l = ((RED, 3.3), (TEAL, 2.8))[i % 2]
            for j in range(-9, 10):
                a = 9 - abs(j)
                R(cx - a, mid + j, 2 * a + 1, 1, c, l)
                if a >= 4:
                    R(cx - a + 4, mid + j, 2 * a - 7, 1, CARD, 4.5)
                if a >= 8:
                    R(cx - 1, mid + j, 3, 1, c, l)
        rnd = random.Random(7)
        for _ in range(10):                                     # threadbare streaks
            T(x + 8 + rnd.randrange(w - 30), y + 8 + rnd.randrange(h - 17), rnd.randrange(5, 13), 1, .7)


# --- light ----------------------------------------------------------------------------------------------------
def sun(x):
    """Sun through the two panes of a window at x: a patch on the floor, hotter near the glass."""
    for x0 in (x + 3, x + 36):
        light(1, 1.2, [(x0, 66), (x0 + 28, 66), (x0 + 98, 166), (x0 + 60, 166)])
        light(.6, 2.5, [(x0 + 4, 66), (x0 + 24, 66), (x0 + 50, 112), (x0 + 30, 106)])
    light(.5, 2, [(x - 2, 56), (x + 72, 56), (x + 72, 66), (x - 2, 66)])


def room_lights():
    if not m.EVE:
        light(.95, 40, lambda d: d.ellipse((-30, -60, W + 30, H + 40), fill=255))                  # daylight, weaker in the corners
        sun(196); sun(494)
        light(.8, 2.5, sh([(196, 70), (232, 68), (240, 84), (236, 100), (214, 104), (192, 94), (186, 80)], 184))   # lamp, on the desk
        light(.6, 3, sh([(200, 40), (216, 32), (236, 36), (242, 52), (238, 63), (202, 63)], 184))                  # and on the wall
        light(.5, 2, sh([(164, 80), (204, 80), (208, 94), (160, 94)], 184))                                        # the screen
        light(.5, 2, [(506, 78), (540, 78), (544, 92), (502, 92)])                              # the laptop
        light(.5, 2, [(130, 216), (158, 216), (162, 230), (126, 230)])
    else:
        for x in (196, 494):                                                                    # the last of the dusk
            light(.5, 3, [(x, 56), (x + 68, 56), (x + 78, 82), (x - 6, 80)])
        light(.4, 9, [(210, 90), (280, 84), (330, 140), (318, 200), (250, 214), (214, 160)])
        light(.4, 9, [(590, 96), (640, 100), (662, 150), (630, 190), (584, 170)])
        light(1, 2.5, sh([(190, 66), (234, 64), (250, 84), (246, 112), (222, 124), (196, 112), (180, 90)], 184))   # desk lamp: three pools,
        light(1, 4, sh([(186, 74), (244, 60), (276, 96), (270, 150), (242, 174), (214, 158), (204, 124)], 184))    # each its own shape
        light(.8, 2, sh([(202, 70), (230, 70), (236, 88), (208, 94)], 184))
        light(1, 3, sh([(196, 44), (214, 30), (238, 34), (248, 52), (244, 63), (196, 63)], 184))
        light(.7, 4, sh([(184, 52), (206, 22), (246, 24), (260, 60), (186, 63)], 184))
        light(1, 3, sh([(160, 80), (206, 80), (212, 96), (196, 122), (160, 120), (152, 96)], 184))                 # the screen
        light(.6, 4, sh([(150, 98), (200, 98), (190, 142), (154, 138)], 184))
        # the second desk: the arm lamp, the laptop
        light(1, 2.5, [(536, 58), (560, 54), (572, 70), (566, 92), (540, 96), (528, 78)])
        light(.8, 4, [(520, 66), (566, 50), (592, 76), (588, 120), (556, 140), (522, 118)])
        light(1, 3, [(500, 78), (544, 76), (548, 96), (532, 126), (502, 124), (494, 98)])
        light(.5, 4, [(496, 104), (540, 102), (534, 150), (498, 146)])
        # the floor lamp by the sofa: a hot spot under the shade, a wide pool over sofa and rug, a wash beyond
        light(1, 2.5, [(596, 222), (628, 218), (638, 240), (630, 262), (604, 264), (590, 244)])
        light(1, 4, [(566, 232), (632, 214), (668, 250), (664, 300), (628, 330), (574, 322), (544, 280)])
        light(.8, 6, [(520, 226), (610, 196), (690, 232), (706, 310), (660, 372), (560, 376), (500, 318)])
        light(.5, 8, [(480, 240), (560, 180), (700, 190), (740, 300), (690, 400), (540, 410), (470, 340)])
        # the reading lamp
        light(1, 2.5, [(842, 104), (868, 102), (874, 124), (862, 140), (842, 138), (834, 120)])
        light(1, 4, [(800, 118), (856, 100), (878, 130), (874, 180), (838, 200), (796, 176)])
        light(.7, 6, [(760, 120), (830, 88), (878, 110), (878, 216), (820, 240), (756, 204)])
        # the lamp on the cube shelf, on the wall behind it
        light(1, 2.5, [(772, 12), (796, 10), (804, 30), (790, 38), (770, 34)])
        light(.7, 4, [(756, 8), (806, 4), (822, 34), (800, 52), (760, 46)])
        # the big table: the laptop, the lantern
        light(1, 3, [(124, 214), (164, 212), (170, 232), (156, 262), (124, 260), (116, 234)])
        light(.5, 4, [(112, 236), (166, 234), (160, 284), (118, 280)])
        light(1, 2.5, [(140, 186), (160, 184), (168, 200), (162, 216), (142, 218), (134, 202)])
        light(.8, 5, [(110, 182), (172, 172), (202, 204), (196, 250), (150, 262), (104, 240)])
        light(.5, 8, [(70, 170), (180, 150), (230, 200), (226, 270), (160, 300), (76, 280)])


# --- the room -------------------------------------------------------------------------------------------------
def draw():
    rnd = random.Random(11)
    shell(); pipes(); wear(rnd)
    # flat: rugs, mats
    with thing(False):
        m.rug(486, 228, 180, 122)
    mat(70, 100, 68, 20, TEAL, PAPER, 2.6, 4.4)
    kilim(306, 392, 252, 44)
    round_rug(776, 136, 102, 62)
    banner(134, 374)
    with thing(False):
        m.socket(572, 46)
        cable([(300, 72), (298, 100), (300, 128), (286, 150), (256, 158), (226, 186), (204, 192), (192, 214), (190, 240)], RED, 3,
              tape=((294, 112), (268, 152), (212, 186)))
        cable([(575, 54), (577, 66), (588, 98), (598, 104), (610, 150), (640, 190), (646, 250), (632, 278)], tape=((600, 120), (638, 214)))
        cable([(96, 330), (120, 336), (170, 330), (200, 340), (232, 338)], tape=((150, 331),))
    with thing(False):
        m.doormat(418, 481, door=(DOOR * TILE, Y1), stuff=False)
    with thing(False):
        scraps(rnd, 22)
    with thing(False):                                          # sheets that left the drawing table, balls that left theirs
        for x, y, c, l in ((684, 300, PAPER, 5), (676, 322, PAPER, 4.6), (742, 330, FLOOR, 5.2), (400, 236, PAPER, 5), (446, 318, PAPER, 4.8)):
            with prop(cast=(1, 1), rim=0):
                G([(x, y + 2), (x + 11, y), (x + 13, y + 9), (x + 2, y + 11)], c, l)
                L([(x + 3, y + 4), (x + 9, y + 3)], c, l - 1.6); L([(x + 3, y + 7), (x + 10, y + 6)], c, l - 1.6)
        for x, y in ((330, 322), (214, 352), (344, 300)):
            with prop(cast=(1, 1), rim=0):
                R(x, y, 2, 2, PAPER, 6)
    # the back wall, left to right
    m.sign(36, 16); wall_shelf(70, 30)
    with thing():
        m.window(196, 14)
    m.board(328, 12); m.clock(396, 18); m.poster(422, 14, sock=(308, 46))
    radiator(452, 40)
    with thing():
        m.window(494, 14, blind=(2, 6), sun=False, sill=False, town=((0, 22, 7, 1), (7, 29, 4, 2), (12, 24, 5, 2), (18, 17, 5, 1), (24, 27, 5, 2)))
    whiteboard(580, 14); hooks(638, 20); frames(770, 8)
    m.fairy_lights(((304, 14, 328, 16, 7), (374, 16, 396, 19, 6), (416, 20, 448, 15, 8), (448, 15, 492, 17, 9),
                    (700, 12, 740, 14, 8), (740, 14, 770, 11, 6), (826, 12, 878, 16, 9)))
    # along the back wall
    with thing():
        m.fridge(34, 52)
    with thing():
        counter(64, 56)
    with thing():
        m.pizza(226, 57)
    with thing():
        m.plant(166, 70)
    with thing(False):
        m.power_strip(292, 66)
        for pts in ([(311, 54), (313, 60), (308, 66)], [(310, 69), (315, 74), (320, 72)], [(296, 68), (288, 73), (282, 66)],
                    [(292, 68), (284, 66), (274, 70), (268, 82), (270, 92), (262, 96), (236, 94), (212, 98), (196, 94)]):
            with prop(cast=(1, 1), rim=0):
                L(pts, METAL, .8)
        with prop(cast=(1, 1), rim=0):
            L([(304, 71), (308, 82), (304, 92), (312, 104), (320, 124), (334, 126)], RED, 3)       # the one red cable
    with thing():
        m.bin_(426, 70, pile=False)
    with thing():
        m.bookshelf(672, 20)
    with thing():
        cube_shelf(736, 34)
    with thing():
        m.plant(838, 70, extras=False)
    with thing():
        shoe_rack(642, 74)
    with thing():
        m.desk(320, 68)
    with thing():
        m.backpack(301, 98)
    with thing():
        m.chair(354, 116)
    with thing():
        desk2(480, 70)
    with thing():
        m.chair(516, 116, hoodie=False)
    # the reading corner
    with thing():
        armchair(802, 142)
    with thing(tall=True):
        floor_lamp(854, 186)
    with thing():
        m.book_pile(770, 128)
    # the big table and its stools
    with thing():
        stool(102, 164, RED, 3.6)
    with thing():
        stool(166, 165)
    with thing():
        table(98, 198)
    with thing():
        stool(70, 226, TEAL, 3.2)
    with thing():
        stool(104, 260)
    with thing():
        stool(164, 259, METAL, 3.4)
    # the lounge
    with thing():
        sofa(512, 233)
    with thing(tall=True):
        tall_plant(488, 272)
    with thing(tall=True):
        floor_lamp(624, 284)
    with thing():
        beanbag(610, 292)
    with thing():
        low_table(514, 322)
    with thing():
        cushion(486, 326, TEAL, 3.2); cushion(490, 336, RED, 3.6)
    # the middle of the room
    with thing():
        pingpong(226, 292)
    with thing(tall=True):
        aquarium(354, 232)
    # right wall
    with thing(tall=True):
        arcade(834, 226)
    with thing():
        cabinet(822, 320)
    with thing():
        drafting(706, 262)
    with thing():
        stool(712, 324, TEAL, 3.2)
    with thing():
        drying_rack(706, 438)
    # left wall: amp, storage corner
    with thing():
        amp(34, 290)
    with thing(tall=True):
        rack(34, 350)
    with thing():
        m.box(35, 420, 28, 9, 17, -.2, 12)
    with thing():
        m.crate(66, 416)
    with thing():
        m.box(34, 452, 30, 10, 24, .2, 3); m.box(38, 440, 20, 7, 10, .3, 10)
    with thing():
        m.box(67, 456, 26, 9, 22, -.1, 14)
    with thing():
        paint_cans(102, 390)
    with thing():
        m.box(100, 454, 24, 8, 18, .1, 3)
    # the dog's corner, the door
    mat(812, 458, 60, 24, CARD, RED, 3.4, 3.4)
    with thing():
        m.dog_corner(838, 454)
    with thing(False):
        with prop(cast=(1, 1)):                                 # a rope toy, a chewed slipper
            L([(800, 440), (808, 444), (816, 441)], PAPER, 4.6, 2); R(798, 438, 3, 4, RED, 4); R(815, 439, 3, 4, TEAL, 3.4)
        with prop(cast=(1, 1)):
            R(782, 470, 10, 6, TEAL, 3); R(782, 470, 4, 6, TEAL, 2); R(789, 471, 3, 2, PAPER, 5)
    with thing():
        bench(324, 454)
    with thing(tall=True):
        tall_plant(488, 462)
    with thing(False):
        for sx, sy, c in ((392, 482, RED), (401, 484, RED), (454, 481, METAL), (463, 483, METAL)):
            m.shoe(sx, sy, c)
    with thing():
        m.skateboard(500, 482)


def build(evening):
    m.canvas(W, H, evening)
    draw()
    room_lights()
    return m.render()
