# The touch controls in the arcade style (RadicalButton/asi-creative-dude#63, built in #71), drawn in the rooms' ramps
# (draw.py) the way the rooms are: no outlines, a lit top edge, a dark bottom edge, a K shadow cast down and right.
#   base, knob   the stick: a bat-top red ball in a recessed metal gate
#   a, a-on      the A button: a red dome in a metal bezel, and its pressed frame (pushed in a pixel, no shadow)
#   start        the menu button: a small round amber start button in a metal bezel, the lamps' colour
# Writes public/controls/<name>.png at 1 px per art pixel; src/styles/touchControls.css scales them.
# usage (repo root): npm run controls     or: python3 -I art/controls.py
# Needs Pillow at the version in art/requirements.txt: other versions may move pixels.
import os, sys
from PIL import Image
ART = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ART)                                             # python3 -I leaves the script's folder out
from draw import FLOOR, METAL, RED, RAMPS, K, rgb

OUT = os.path.join(ART, '..', 'public', 'controls')
SH = 2                          # room of the cast shadow, right and down

GLYPH_A = ['.###.', '#...#', '#...#', '#####', '#...#', '#...#', '#...#']


def disc(cx, cy, r):
    return lambda x, y: (x + .5 - cx) ** 2 + (y + .5 - cy) ** 2 <= r * r


def rect(x0, y0, w, h):
    return lambda x, y: x0 <= x < x0 + w and y0 <= y < y0 + h


def glyph(rows, x0, y0, s=1):
    return lambda x, y: (0 <= (x - x0) // s < len(rows[0]) and 0 <= (y - y0) // s < len(rows)
                         and rows[(y - y0) // s][(x - x0) // s] == '#')


class Pic:
    def __init__(self, w, h):
        self.w, self.h, self.px = w + SH, h + SH, {}

    def shape(self, inside, m, body, lit=None, dark=None, shadow=True, recess=False):
        # m is a ramp (draw.py), body/lit/dark its levels 0 (K) to 6 (HI). Lit top edge and dark bottom edge,
        # swapped for a recess (a hole is lit at the bottom)
        pts = [(x, y) for y in range(self.h) for x in range(self.w) if inside(x, y)]
        if shadow:
            for x, y in pts:
                for sx, sy in ((x + 1, y + SH), (x + SH, y + 1), (x + 1, y + 1)):
                    if not inside(sx, sy) and (sx, sy) not in self.px:
                        self.px[(sx, sy)] = K
        top, bot = (dark, lit) if recess else (lit, dark)
        for x, y in pts:
            c = body
            if top is not None and not inside(x, y - 1): c = top
            elif bot is not None and not inside(x, y + 1): c = bot
            self.px[(x, y)] = RAMPS[m][c]
        return self

    def save(self, name, dy=0):         # dy=1 and no shadow: the pressed button, pushed into the screen
        im = Image.new('RGBA', (self.w, self.h + 1))
        for (x, y), c in self.px.items():
            if 0 <= x < self.w and 0 <= y + dy < self.h + 1: im.putpixel((x, y + dy), (*rgb(c), 255))
        im.save(os.path.join(OUT, name + '.png')); print('controls: built', name)


def a(shadow):
    p = Pic(38, 38)
    p.shape(disc(19, 19, 19), METAL, 3, 4, 1, shadow=shadow)
    p.shape(disc(19, 19, 14), RED, 4, 5, 2, shadow=False)
    p.shape(disc(14, 13, 4), RED, 5, shadow=False)
    return p.shape(glyph(GLYPH_A, 14, 12, 2), RED, 2, shadow=False)


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    base = Pic(48, 48).shape(disc(24, 24, 24), METAL, 3, 4, 1)
    base.shape(disc(24, 24, 17), METAL, 1, 2, 0, shadow=False, recess=True)
    base.save('base')
    knob = Pic(22, 22).shape(disc(11, 11, 11), RED, 4, 5, 2)
    knob.shape(disc(7, 7, 3), RED, 6, shadow=False)            # the bat-top's shine
    knob.save('knob')
    a(True).save('a')
    a(False).save('a-on', dy=1)
    start = Pic(26, 26).shape(disc(13, 13, 13), METAL, 3, 4, 1)
    start.shape(disc(13, 13, 9), FLOOR, 4, 5, 2, shadow=False)
    start.shape(disc(10, 10, 3), FLOOR, 5, shadow=False)
    for y in (9, 12, 15): start.shape(rect(9, y, 9, 2), FLOOR, 0, shadow=False)
    start.save('start')
