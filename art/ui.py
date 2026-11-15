# The title screen and the dialogue box in the lived-in clutter style (#70): Asi's art in the rooms' ramps (draw.py),
# the way cast.py takes the cast. Asi's files are only read; each of their colours is a (ramp, level). Writes:
#   public/title/logo.png, arrow.png, menu.png   titleSprite.png, arrowSprite.png and titleScreenText.png recoloured,
#     same size and frames. The logo is amber, the lamps' colour; the menu teal; the arrow red, the fairy lights'.
#     TitleScreen.ts draws them on K.
#   public/dialogue/letters.png   Letters.png, the dialogue font, in K: the dialogue box (textMessage.css) is paper.
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
