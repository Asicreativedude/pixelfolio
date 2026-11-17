# PROTOTYPE (wayfinder RadicalButton/asi-creative-dude#63), throwaway, lives on branch prototype/touch-controls only.
# The title's first option reads CONTINUE GAME once there is a save. title/menu.png (art/ui.py) is one drawn
# picture, so the line is set from its own glyphs. Their faces never touch, so only the faces are cut; the shadow is
# cast again after, the way the drawn lines have it: every face pixel shades the 1-3 px straight below it and
# diagonally down-left (checked against all three lines, below). The face has no C: it is the G without its spur.
# Writes public/prototype/title-continue.png, menu.png with the first line swapped, and prints where the line's face
# starts, for the arrow in TitleScreen.ts.
# usage (repo root): python3 -I art/prototype_title.py
import os
from PIL import Image

ART = os.path.dirname(os.path.abspath(__file__))
PUBLIC = os.path.join(ART, '..', 'public')
FACE = {(194, 237, 196), (108, 211, 178)}
SHADE = (18, 72, 85, 255)
CAST = [(-k, k) for k in (1, 2, 3)] + [(0, k) for k in (1, 2, 3)]
GAP, SPACE = 3, 15                  # next face's first column - this face's last: between letters, between words
H = 22                              # a line's height, shadow included
LINES = {1: 186, 2: 220, 3: 254}    # each line's top row
# letter -> (line, face x0, face x1), read off menu.png as runs of face-coloured columns
GLYPHS = {
    'S': (1, 245, 257), 'T': (1, 260, 275), 'A': (1, 278, 290), 'R': (1, 293, 305), 'G': (1, 338, 350),
    'M': (1, 368, 383), 'E': (1, 386, 398), 'V': (2, 170, 185), 'I': (2, 188, 191), 'W': (2, 209, 230),
    'B': (2, 245, 257), 'O': (2, 260, 275), 'N': (2, 299, 311), 'P': (2, 341, 353), 'F': (2, 407, 419),
    'L': (2, 440, 452), 'U': (3, 332, 344),
}


def face(src, ch):
    line, x0, x1 = GLYPHS[ch]
    g = Image.new('RGBA', (x1 - x0 + 1, H))
    for y in range(H):
        for x in range(x0, x1 + 1):
            p = src.getpixel((x, LINES[line] + y))
            if p[3] and p[:3] in FACE:
                g.putpixel((x - x0, y), p)
    return g


def letter_c(src):
    # the G without its spur: right of the stem, between the top and the bottom bar (rows 6-14)
    g = face(src, 'G')
    for y in range(6, 15):
        for x in range(4, g.width):          # the stem is face columns 0-3
            g.putpixel((x, y), (0, 0, 0, 0))
    return g


def line(src, text):
    # the line's faces, then their shadow; x 0 of the result is 3 px left of the first face, where its shadow reaches
    faces, x = [], 3
    for ch in text:
        if ch == ' ':
            x += SPACE - GAP
            continue
        g = letter_c(src) if ch == 'C' else face(src, ch)
        faces.append((g, x))
        x += g.width - 1 + GAP
    out = Image.new('RGBA', (x - GAP + 1, H))
    for g, gx in faces:
        out.alpha_composite(g, (gx, 0))
    lit = {(x, y) for y in range(H) for x in range(out.width) if out.getpixel((x, y))[3]}
    for x, y in lit:
        for dx, dy in CAST:
            p = (x + dx, y + dy)
            if p not in lit and 0 <= p[0] < out.width and p[1] < H:
                out.putpixel(p, SHADE)
    return out


if __name__ == '__main__':
    src = Image.open(os.path.join(PUBLIC, 'title', 'menu.png')).convert('RGBA')
    # the method, checked: each drawn line set again from the glyph table is that line, pixel for pixel
    for n, text, x0 in ((1, 'START GAME', 245), (2, 'VIEW BORING PORTFOLIO', 170), (3, 'ABOUT', 284)):
        again = line(src, text)
        drawn = src.crop((x0 - 3, LINES[n], x0 - 3 + again.width, LINES[n] + H))
        assert list(again.getdata()) == list(drawn.getdata()), f'{text} does not rebuild: the glyph table is off'
    new = line(src, 'CONTINUE GAME')
    top = LINES[1]
    out = src.copy()
    out.paste((0, 0, 0, 0), (0, top, src.width, top + H))
    x = round(320 - (new.width + 3) / 2)        # centred on x 320, as START GAME is: its face spans 245-398
    out.alpha_composite(new, (x, top))
    os.makedirs(os.path.join(PUBLIC, 'prototype'), exist_ok=True)
    out.save(os.path.join(PUBLIC, 'prototype', 'title-continue.png'))
    print('title: built prototype/title-continue.png, CONTINUE GAME face starts at x', x + 3)
