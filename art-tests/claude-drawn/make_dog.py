# A dog drawn from nothing, by code (#61 side test). No template: every pixel is specified here.
# Same sheet layout as the cast (256x256, rows down/left/right/up, columns idle/walk-a/walk-b), so the engine
# can walk it as a Person. Drawn at character density (1:1), dark outline, ENDESGA 32.
# usage (repo root): python3 -I art-tests/claude-drawn/make_dog.py
import os
from PIL import Image, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__))
E32 = set(open(os.path.join(HERE, '../pixellab/e32.hex')).read().split())
PAL = {'#': '181425', 'B': 'd77643', 'b': 'be4a2f', 'c': 'ead4aa', 'e': '733e39', 'n': '181425',
       'W': 'ffffff', 'r': 'e43b44', 'g': 'feae34'}
assert set(PAL.values()) <= E32

SIDE = [  # facing right, 30 wide. Legs are added below row 14.
    '...................##...##....',
    '..................#ee#.#ee#...',
    '..##.............##eeB##eeB#..',
    '.#cc#............#BBBBBBBBB#..',
    '.#BBB#...........#BBBBBBBBB#..',
    '..#BB#...........#BBBBBnWBB##.',
    '..#BB#...........#BBBBBnnBccn#',
    '..#BB############BBBBBBBccccc#',
    '...#BBBBBBBBBBBrrBBBBBBBcccc#.',
    '...#BBBBBBBBBBBrrBBBBBBccc##..',
    '...#BBBBBBBBBBBrrccccc####....',
    '...#bbBBBBBBBBBrgcccc#........',
    '...#bbbBBBBBBBBBccccc#........',
    '...#bbbbBBBcccccBBBB#.........',
    '...#bbbBBBccccccBBB#..........',
    '....###############...........',
]
FRONT = [  # facing the camera, 16 wide
    '..##........##..',
    '.#ee#......#ee#.',
    '.#eeB######Bee#.',
    '.#BBBBBBBBBBBB#.',
    '.#BBBBBBBBBBBB#.',
    '.#BBnWBBBBnWBB#.',
    '.#BBnnBccBnnBB#.',
    '.#BBBccnnccBBB#.',
    '.#BBBccccccBBB#.',
    '..#BBBc##cBBB#..',
    '..##rrrrrrrr##..',
    '..#BBcccgccBB#..',
    '..#BBccccccBB#..',
    '..#BBccccccBB#..',
    '..#BBBbbbbBBB#..',
    '..############..',
]
BACK = [  # facing away, tail up
    '..##........##..',
    '.#BB#......#BB#.',
    '.#BBB######BBB#.',
    '.#BBBBBBBBBBBB#.',
    '.#BBBBBBBBBBBB#.',
    '.#BBBBBBBBBBBB#.',
    '.#bBBBBBBBBBBb#.',
    '.#bBBBB##BBBBb#.',
    '.##bBB#cc#BBb##.',
    '..#rrr#cc#rrr#..',
    '..#BBB#BB#BBB#..',
    '..#BBB#BB#BBB#..',
    '..#BBBB##BBBB#..',
    '..#bBBBBBBBBb#..',
    '..#bbBBbbBBbb#..',
    '..############..',
]
# legs: (x, width, fill, paw), far legs first. Per frame and leg: (sideways shift, lift), or None = hidden.
SIDE_LEGS = [(8, 2, 'b', 'b'), (13, 2, 'b', 'b'), (4, 3, 'B', 'c'), (16, 3, 'B', 'c')]
SIDE_STEP = [[(0, 0)] * 4,
             [(1, 1), (-1, 1), (-1, 0), (1, 0)],   # near legs apart, far legs meet in the middle
             [None, None, (1, 0), (-1, 0)]]        # near legs together, far legs behind them
FB_LEGS = [(3, 3, 'B', 'c'), (10, 3, 'B', 'c')]
FB_STEP = [[(0, 0)] * 2, [(0, 1), (0, 0)], [(0, 0), (0, 1)]]
LEG = 3  # rows from the belly line down to the paw

def draw(body, legs, step):
    g = {(x, y): ch for y, row in enumerate(body) for x, ch in enumerate(row) if ch != '.'}
    top = len(body) - 1  # the belly outline row; legs start here
    for (x, w, fill, paw), st in zip(legs, step):
        if st is None:
            continue
        dx, lift = st
        end = top + LEG - lift  # paw row
        for y in range(top, end + 2):
            sx = x + (dx if y > top else 0)
            for i in range(-1, w + 1):
                edge = i in (-1, w) or y == end + 1
                g[sx + i, y] = '#' if edge else (paw if y == end else fill)
    return g

def frame(g, x0, y0, mirror=False):
    out = Image.new('RGBA', (64, 64))
    for (x, y), ch in g.items():
        out.putpixel((x0 + x, y0 + y), tuple(bytes.fromhex(PAL[ch])) + (255,))
    if mirror:  # mirror inside the 32 px tile column
        m = Image.new('RGBA', (64, 64)); m.paste(ImageOps.mirror(out), (-32, 0)); out = m
    return out

sheet = Image.new('RGBA', (256, 256))
for c in range(3):
    feet = 61 - (len(SIDE) + LEG)  # paw outline lands on y=61, where the cast's feet are
    side = draw(SIDE, SIDE_LEGS, SIDE_STEP[c])
    sheet.paste(frame(draw(FRONT, FB_LEGS, FB_STEP[c]), 8, feet), (c * 64, 0))
    sheet.paste(frame(side, 1, feet, mirror=True), (c * 64, 64))
    sheet.paste(frame(side, 1, feet), (c * 64, 128))
    sheet.paste(frame(draw(BACK, FB_LEGS, FB_STEP[c]), 8, feet), (c * 64, 192))
used = {'%02x%02x%02x' % p[:3] for _, p in sheet.getcolors() if p[3]}
assert used <= E32, used - E32
sheet.save(os.path.join(HERE, 'dog.png'))
print('dog.png', len(used), 'colours, all ENDESGA 32')
