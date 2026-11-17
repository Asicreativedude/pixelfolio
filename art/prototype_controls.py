# PROTOTYPE (wayfinder RadicalButton/asi-creative-dude#63), throwaway, lives on branch prototype/touch-controls only.
# Three skins for the touch controls #52 settled on (floating stick, A button) plus a menu button, drawn in the rooms'
# ramps (draw.py) the way the rooms are: no outlines, a lit top edge, a dark bottom edge, a shadow cast down and right.
#   paper   the dialogue box's paper card and its amber Next button
#   arcade  the Hall's metal and red: a bat-top stick in a recessed gate, a domed arcade button in a bezel
#   ghost   pale amber marks and their shadows only, nearly nothing over the game
# Writes public/prototype/controls/<skin>-{base,knob,a,a-on,menu}.png at 1 px per art pixel; touchControls.css scales
# them. usage (repo root): python3 -I art/prototype_controls.py
import os, sys
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from draw import FLOOR, METAL, RED, PAPER, RAMPS, K, HI, rgb

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'public', 'prototype', 'controls')
SH = 2                          # room of the cast shadow, right and down

GLYPH_A = ['.###.', '#...#', '#...#', '#####', '#...#', '#...#', '#...#']


def disc(cx, cy, r):
    return lambda x, y: (x + .5 - cx) ** 2 + (y + .5 - cy) ** 2 <= r * r


def ring(cx, cy, r0, r1):
    return lambda x, y: r0 * r0 < (x + .5 - cx) ** 2 + (y + .5 - cy) ** 2 <= r1 * r1


def rect(x0, y0, w, h):
    return lambda x, y: x0 <= x < x0 + w and y0 <= y < y0 + h


def glyph(rows, x0, y0, s=1):
    return lambda x, y: (0 <= (x - x0) // s < len(rows[0]) and 0 <= (y - y0) // s < len(rows)
                         and x >= x0 and y >= y0 and rows[(y - y0) // s][(x - x0) // s] == '#')


class Pic:
    def __init__(self, w, h):
        self.w, self.h, self.px = w + SH, h + SH, {}

    def shape(self, inside, m, body, lit=None, dark=None, shadow=True, recess=False):
        # lit top edge and dark bottom edge, swapped for a recess (a hole is lit at the bottom)
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
            self.px[(x, y)] = RAMPS[m][c] if isinstance(c, int) else c

    def save(self, name, dy=0):         # dy=1 and no shadow: the pressed button, pushed into the screen
        im = Image.new('RGBA', (self.w, self.h + 1))
        for (x, y), c in self.px.items():
            if 0 <= x < self.w and 0 <= y + dy < self.h + 1: im.putpixel((x, y + dy), (*rgb(c), 255))
        im.save(os.path.join(OUT, name)); print('controls: built', name)


def chevrons(p, cx, cy, r, m, l, shadow=True):
    # four little arrowheads pointing out, at radius r
    for dx, dy in ((0, -1), (0, 1), (-1, 0), (1, 0)):
        tip = (cx + dx * r, cy + dy * r)
        pts = set()
        for i in range(4):
            for j in range(-i, i + 1):
                x = tip[0] - dx * i + (j if dy else 0)
                y = tip[1] - dy * i + (j if dx else 0)
                pts.add((int(x), int(y)))
        p.shape(lambda x, y, s=frozenset(pts): (x, y) in s, m, l, shadow=shadow)


def paper():
    base = Pic(48, 48)
    base.shape(ring(24, 24, 15, 23), PAPER, 5, 6, 3)
    chevrons(base, 24, 24, 21, PAPER, 2, shadow=False)
    knob = Pic(20, 20)
    knob.shape(disc(10, 10, 10), FLOOR, 4, 5, 3)

    def a(shadow):
        p = Pic(34, 34)
        p.shape(disc(17, 17, 17), FLOOR, 4, 5, 3, shadow=shadow)
        p.shape(glyph(GLYPH_A, 12, 10, 2), FLOOR, 0, shadow=False)
        return p
    menu = Pic(22, 18)
    menu.shape(rect(0, 0, 22, 18), PAPER, 5, 6, 3)
    for y in (5, 8, 11): menu.shape(rect(5, y, 12, 2), PAPER, 0, shadow=False)
    return base, knob, a, menu


def arcade():
    base = Pic(48, 48)
    base.shape(disc(24, 24, 24), METAL, 3, 4, 1)
    base.shape(disc(24, 24, 17), METAL, 1, 2, 0, shadow=False, recess=True)
    knob = Pic(22, 22)
    knob.shape(disc(11, 11, 11), RED, 4, 5, 2)
    knob.shape(disc(7, 7, 3), RED, 6, shadow=False)          # the bat-top's shine

    def a(shadow):
        p = Pic(38, 38)
        p.shape(disc(19, 19, 19), METAL, 3, 4, 1, shadow=shadow)
        p.shape(disc(19, 19, 14), RED, 4, 5, 2, shadow=False)
        p.shape(disc(14, 13, 4), RED, 5, shadow=False)
        p.shape(glyph(GLYPH_A, 14, 12, 2), RED, 2, shadow=False)
        return p
    menu = Pic(28, 18)
    menu.shape(lambda x, y: rect(4, 0, 20, 18)(x, y) or disc(5, 9, 5)(x, y) or disc(23, 9, 5)(x, y)
               or rect(0, 4, 28, 10)(x, y), METAL, 3, 4, 1)
    for x in (10, 16): menu.shape(rect(x, 4, 3, 10), RED, 4, 5, 2, shadow=False)
    return base, knob, a, menu


def ghost():
    base = Pic(48, 48)
    chevrons(base, 24, 24, 22, PAPER, 6)
    knob = Pic(12, 12)
    knob.shape(disc(6, 6, 6), PAPER, 6)

    def a(shadow):
        p = Pic(34, 34)
        p.shape(ring(17, 17, 14, 17), PAPER, 6, shadow=shadow)
        p.shape(glyph(GLYPH_A, 12, 10, 2), PAPER, 6, shadow=shadow)
        return p
    menu = Pic(16, 14)
    for y in (2, 6, 10): menu.shape(rect(1, y, 14, 2), PAPER, 6)
    return base, knob, a, menu


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    for name, skin in (('paper', paper), ('arcade', arcade), ('ghost', ghost)):
        base, knob, a, menu = skin()
        base.save(f'{name}-base.png'); knob.save(f'{name}-knob.png'); menu.save(f'{name}-menu.png')
        a(True).save(f'{name}-a.png')
        a(False).save(f'{name}-a-on.png', dy=1)
