# The title screen and the dialogue box in the lived-in clutter style (#70): Asi's art in the rooms' ramps (draw.py),
# the way cast.py takes the cast. Asi's files are only read; each of their colours is a (ramp, level). Writes:
#   public/title/logo.png, arrow.png, menu.png   titleSprite.png, arrowSprite.png and titleScreenText.png recoloured,
#     same size and frames. The logo is amber, the lamps' colour; the menu teal; the arrow red, the fairy lights'.
#     TitleScreen.ts draws them on K.
#   public/dialogue/letters.png   Letters.png, the dialogue font, in K: the dialogue box (textMessage.css) is paper.
#   public/title/menu-continue.png   menu.png with its first line reading CONTINUE GAME, for a player with a save
#     (#71). Set from menu.png's own glyphs; prints where the line's face starts, for the arrow in TitleScreen.ts.
# usage (repo root): npm run ui     or: python3 -I art/ui.py
# Needs Pillow at the version in art/requirements.txt: other versions may move pixels.
import os, sys
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))     # python3 -I leaves the script's folder out
from draw import FLOOR, DESK, METAL, TEAL, RED, RAMPS, K, rgb

ART = os.path.dirname(os.path.abspath(__file__))
PUBLIC = os.path.join(ART, '..', 'public')
TOP = (FLOOR, 6)                # draw.HI: every ramp ends on the same pale amber

SPRITES = {
    'title/logo.png': ('titleSprite.png', {'4192c3': (FLOOR, 4), '61d3e3': (FLOOR, 5), 'a2fff3': TOP, '305182': (DESK, 2)}),
    'title/menu.png': ('titleScreenText.png', {'61d3e3': (TEAL, 4), 'a2fff3': (TEAL, 5), '305182': (TEAL, 1),
                                               '797979': (METAL, 3)}),
    'title/arrow.png': ('arrowSprite.png', {'ff61b2': (RED, 4), 'ffbaeb': (RED, 5), 'b21030': (RED, 2)}),
    'dialogue/letters.png': ('Letters.png', {'000000': None}),
}


# CONTINUE GAME (#71). menu.png is one drawn picture, so the line is set from its own glyphs. Their faces never touch,
# so only the faces are cut; the shadow is cast again after, the way the drawn lines have it: every face pixel shades
# the 1-3 px straight below it and diagonally down-left (checked against all three lines in continue_line). The face
# has no C: it is the G without its spur.
MENU = SPRITES['title/menu.png'][1]
FACE = {rgb(RAMPS[m][l]) for m, l in (MENU['61d3e3'], MENU['a2fff3'])}
SHADE = (*rgb(RAMPS[MENU['305182'][0]][MENU['305182'][1]]), 255)
DROP = [(-k, k) for k in (1, 2, 3)] + [(0, k) for k in (1, 2, 3)]
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


def letter(src, ch):
    if ch != 'C':
        return face(src, ch)
    g = face(src, 'G')                  # C: the G without its spur, right of the stem (face columns 0-3), rows 6-14
    for y in range(6, 15):
        for x in range(4, g.width):
            g.putpixel((x, y), (0, 0, 0, 0))
    return g


def set_line(src, text):
    # the line's faces, then their shadow; x 0 of the result is 3 px left of the first face, where its shadow reaches
    faces, x = [], 3
    for ch in text:
        if ch == ' ':
            x += SPACE - GAP
            continue
        g = letter(src, ch)
        faces.append((g, x))
        x += g.width - 1 + GAP
    out = Image.new('RGBA', (x - GAP + 1, H))
    for g, gx in faces:
        out.alpha_composite(g, (gx, 0))
    lit = {(x, y) for y in range(H) for x in range(out.width) if out.getpixel((x, y))[3]}
    for x, y in lit:
        for dx, dy in DROP:
            p = (x + dx, y + dy)
            if p not in lit and 0 <= p[0] < out.width and p[1] < H:
                out.putpixel(p, SHADE)
    return out


def continue_line(src):
    # the method, checked: each drawn line set again from the glyph table is that line, pixel for pixel
    for n, text, x0 in ((1, 'START GAME', 245), (2, 'VIEW BORING PORTFOLIO', 170), (3, 'ABOUT', 284)):
        again = set_line(src, text)
        drawn = src.crop((x0 - 3, LINES[n], x0 - 3 + again.width, LINES[n] + H))
        assert list(again.getdata()) == list(drawn.getdata()), f'{text} does not rebuild: the glyph table is off'
    new, top = set_line(src, 'CONTINUE GAME'), LINES[1]
    out = src.copy()
    out.paste((0, 0, 0, 0), (0, top, src.width, top + H))
    x = round(320 - (new.width + 3) / 2)        # centred on x 320, as START GAME is: its face spans 245-398
    out.alpha_composite(new, (x, top))
    print('ui: CONTINUE GAME face starts at x', x + 3)
    return out


def recolour(src, table):
    im = Image.open(os.path.join(PUBLIC, src)).convert('RGBA')
    px = im.load()
    for y in range(im.height):
        for x in range(im.width):
            r, g, b, a = px[x, y]
            if a:
                part = table['%02x%02x%02x' % (r, g, b)]            # a colour the table lacks is an error, not a guess
                px[x, y] = (*rgb(RAMPS[part[0]][part[1]] if part else K), 255)       # None is K, as in cast.py
    return im


if __name__ == '__main__':
    for out, (src, table) in SPRITES.items():
        os.makedirs(os.path.dirname(os.path.join(PUBLIC, out)), exist_ok=True)
        recolour(src, table).save(os.path.join(PUBLIC, out)); print('ui: built', out)
    continue_line(Image.open(os.path.join(PUBLIC, 'title', 'menu.png')).convert('RGBA')).save(
        os.path.join(PUBLIC, 'title', 'menu-continue.png')); print('ui: built title/menu-continue.png')
