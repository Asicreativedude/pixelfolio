# Draws new NPCs by code on an existing character's body (#61 side test: "can Claude just build the px chars?").
# Body, poses and walk frames come from a cast sheet (read only), recoloured to ENDESGA 32. The head is drawn
# here, pixel by pixel, for front, side and back, and stamped at each frame's head offset. Left = right mirrored.
#   visitor: the hero's body, short sleeves made long.
#   dana: Saruli's body (dress), long straight hair instead of curls.
#   hero-detailed: Asi's own hero, nothing redrawn, recoloured to ENDESGA 32 (his sheet is read only).
# Every frame then gets detail(): a wider shadow on the far side, a hem, a shadow under the chin, a third hair
# tone, a belt with a buckle, cuffs, a shine on the shoes. (Asi on the flat versions: "they need a bit more
# details / shading / touch ups. It applies to characters as well (also ones I did already)".)
#
# usage (repo root): python3 -I art-tests/claude-drawn/make_char.py
# Rows are run-length: "6. # 4H 2L" = 6 clear, 1 outline, 4 hair, 2 hair light. "_" keeps the template pixel.
import os
from PIL import Image, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__))
E32 = set(open(os.path.join(HERE, '../pixellab/e32.hex')).read().split())
# letter -> colour. T/t = top or dress, d = trousers, c = shoes, B = iris, M = mouth.
PAL = {'#': '181425', 'H': 'f77622', 'h': 'be4a2f', 'L': 'feae34', 's': 'e8b796', 'k': 'c28569',
       'e': '3e2731', 'W': 'ffffff', 'M': 'b86f50', 'T': '3e8948', 't': '265c42', 'd': '3a4466',
       # detail pass: U/u = top highlight / deep shade, D/f = trousers highlight / shade, j = hair deep shade,
       # b/g = belt and buckle, o = shine on black shoes, C = shine on coloured shoes
       'U': '63c74d', 'u': '193c3e', 'D': '5a6988', 'f': '262b44', 'j': 'a22633', 'b': '733e39', 'g': 'feae34',
       'o': '3a4466', 'C': '5a6988'}
# template colour -> letter. Colours not listed (old hair, earrings) are dropped.
HERO_ROLE = {'000000': '#', '150908': '#', '513407': '#', '191919': 'd', '121212': 'd', 'ebbf96': 's',
             'cba582': 'k', '0989a0': 'T', '076a7c': 't', '6c6c6c': 't', '4c4c4c': 't', '373737': 't',
             'ffffff': 't'}
# the hero whole, head included: G/q/Q = grey hair, n = glasses tint
HERO_FULL = {**HERO_ROLE, '6c6c6c': 'G', '4c4c4c': 'q', '373737': 'Q', 'ffffff': 'W', '150908': 'e', '513407': 'n'}
SARULI_ROLE = {'000000': '#', 'e3ab7e': 's', 'edb384': 's', 'b18562': 'k', '3a4d8a': 'T', '27325b': 't',
               'a83e3e': 'c'}

FRONT = {13: '10. 11#', 14: '8. 3# 2H 3L 5H 3#', 15: '7. 2# 3H 3L 7H h 2#', 16: '6. # 4H 2L 9H 2h #',
         17: '6. # 15H 2h #', 18: '6. # 16H h #', 19: '6. # H h 6k 2h 6H h #', 20: '6. # H k 7s k 2h 4H h #',
         21: '6. # h k 10s k h 2H h #', 22: '5. 2# h 2s 3h 5s 3h 2s h 2#',
         23: '4. # k s # 3s e W 5s e W 3s # s k #', 24: '4. # k s # 3s 2e 5s 2e 3s # s k #',
         25: '4. # 2s # 15s # 2s #', 26: '5. # s # 15s # s #', 27: '6. 2# 15s 2#', 28: '7. # 6s 3M 6s #',
         29: '7. # k 13s k #', 30: '8. # 2k 9s 2k #', 31: '11_ # 7k #', 32: '11_ 9#', 33: '13_ 5t'}
SIDE = {15: '11. 9#', 16: '9. 3# 3H 3L 2H 3#', 17: '7. 3# 4H 3L 5H h 2#', 18: '6. 2# 16H h #',
        19: '6. # 17H h #', 20: '6. # h 15H 2h #', 21: '6. # h 11H 2h 2k 2s #', 22: '6. # h 8H 2h k 6s #',
        23: '6. # h 7H h k 8s #', 24: '6. # h 6H h k 3s 3h 3s #', 25: '6. # h 6H h k 3s W e 4s #',
        26: '6. # h 5H h k 4s 2e 3s #', 27: '6. # h 4H h k 10s #', 28: '7. # h 2H h k 11s #',
        29: '7. # 2h k 13s #', 30: '8. 2# k 10s 2M s #', 31: '9. # 2k 12s #', 32: '10. # 3k 7s 2k #',
        33: '11. # 2t 9#', 34: '11. # 6t #'}
BACK = {16: '10. 11#', 17: '8. 3# 4H 3L 3H 3#', 18: '7. 2# 6H 3L 4H h 2#', 19: '6. # 9H 2L 4H 2h #',
        20: '6. # h 14H 2h #', 21: '6. # h 3H h 10H 2h #', 22: '6. # h 14H 2h #', 23: '6. # h 9H h 4H 2h #',
        24: '6. # h 14H 2h #', 25: '5. 2# h 14H 2h 2#', 26: '4. # 2s h 14H 2h 2s #', 27: '4. # 2s h 14H 2h 2s #',
        28: '4. # 2s h 14H 2h 2s #', 29: '5. # s 2h 13H 2h s #', 30: '6. 2# 2h 11H 2h 2#',
        31: '7. # 3h 9H 3h #', 32: '7. # 4h 7H 4h #', 33: '8. # 13h #', 34: '11_ 9#', 35: '11_ 2# 5t 2#',
        36: '13_ 5t'}

D_FRONT = {16: '10. 11#', 17: '8. 3# 3H 3L 4H 3#', 18: '7. 2# 4H 3L 6H h 2#', 19: '6. # 16H h #',
           20: '5. # 18H h #', 21: '5. # 9H h 8H h #', 22: '5. # 7H h k s k h 6H h #',
           23: '5. # 5H h k 5s k h 4H h #', 24: '5. # 3H h k 9s k h 2H h #',
           25: '5. # H h 2s 4# 3s 4# 2s h H #', 26: '5. # H h 3s B W 5s B W 3s h H #',
           27: '5. # H h 3s 2B 5s 2B 3s h H #', 28: '5. # H h 15s h H #', 29: '5. # H h 15s h H #',
           30: '5. # H 2h 13s 2h H #', 31: '5. # H 2h 5s 3M 5s 2h H #', 32: '5. # 2H 2h k 9s k 2h 2H #',
           33: '5. # 2H 3h k 7s k 3h 2H #', 34: '5. # 3H 3# 3s k 3s 3# 3H #', 35: '5. # 3H 13_ 3H #',
           36: '5. # 2H h 13_ h 2H #', 37: '5. # H 2h 13_ 2h H #', 38: '6. 3# 13_ 3#'}
D_SIDE = {18: '11. 9#', 19: '9. 3# 3H 3L 2H 3#', 20: '7. 3# 4H 3L 5H h 2#', 21: '6. 2# 16H h #',
          22: '6. # 17H h #', 23: '6. # h 15H 2h #', 24: '6. # h 12H 2h k s #', 25: '6. # h 9H 2h k 4s #',
          26: '6. # h 7H 2h k 6s #', 27: '6. # h 6H 2h k s 3# 2s 2#', 28: '6. # h 5H 2h k 2s W B 4s #',
          29: '6. # h 5H 2h k 2s 2B 3s #', 30: '6. # h 5H 2h k 7s #', 31: '6. # h 5H 2h k 7s #',
          32: '6. # h 5H 2h k 7s #', 33: '6. # h 5H 2h k 7s #', 34: '6. # h 5H 2h k 3s 3M s #',
          35: '6. # h 5H 2h k 6s #', 36: '6. # h 5H 2h # 4s 2#', 37: '6. # h 4H h 2k 5#',
          38: '6. # h 3H h', 39: '7. # h 2H h', 40: '7. # h 2H h', 41: '8. 4#'}
D_BACK = {15: '10. 11#', 16: '8. 3# 3H 3L 4H 3#', 17: '7. 2# 5H 3L 5H h 2#', 18: '6. # 16H h #',
          19: '5. # 18H h #',
          **{y: '5. # h 7H L h 8H h #' for y in range(20, 24)},
          **{y: '5. # h 8H h 3H h 4H h #' for y in range(24, 26)},
          **{y: '5. # h 4H h 3H h 3H h 4H h #' for y in range(26, 34)},
          34: '6. # h 3H h 3H h 3H h 3H h #', 35: '7. # h 2H h 3H h 3H h 2H h #',
          36: '8. # h H h 3H h 3H h H h #', 37: '8. # 3h 3H h 3H 3h #', 38: '9. # 11h #', 39: '10. 11#'}

# views: sheet row -> (stamp, last template row that is all head, head offset per column idle/walk-a/walk-b)
# mirror: where the template's own left frames sit relative to its right frames, per column
CHARS = {
    'visitor': dict(sheet='public/Hero/Sprite-Hero.png', role=HERO_ROLE, pal={}, long_sleeves=True,
                    views={0: (FRONT, 30, [(0, 0), (0, 0), (-2, 0)]),
                           2: (SIDE, 34, [(0, 0), (-1, 1), (-3, 0)]),
                           3: (BACK, 33, [(0, 0), (-1, 0), (-2, 0)])},
                    mirror=[31, 28, 24]),
    'dana': dict(sheet='public/characters/saruli.png', role=SARULI_ROLE, long_sleeves=False,
                 pal={'H': 'feae34', 'h': 'd77643', 'L': 'fee761', 'T': 'e43b44', 't': 'a22633',
                      'c': '3a4466', 'B': '124e89', 'M': 'a22633', 'U': 'f6757a', 'u': '3e2731', 'j': 'be4a2f'},
                 views={0: (D_FRONT, 34, [(0, 0), (-1, 1), (-3, 0)]),
                        2: (D_SIDE, 37, [(0, 0), (-1, 0), (-4, 0)]),
                        3: (D_BACK, 34, [(0, 0), (-1, 1), (-3, 0)])},
                    mirror=[30, 25, 23]),
    # Asi's own hero, nothing redrawn: recoloured to ENDESGA 32, then the same detail pass as the others
    'hero-detailed': dict(sheet='public/Hero/Sprite-Hero.png', role=HERO_FULL, long_sleeves=False,
                          pal={'T': '0099db', 't': '124e89', 'U': '2ce8f5', 'u': '262b44', 'd': '262b44',
                               'D': '3a4466', 'f': '181425', 'G': '8b9bb4', 'q': '5a6988', 'Q': '262b44',
                               'n': '733e39'},
                          views={r: ({}, -1, [(0, 0)] * 3) for r in range(4)}, mirror=None),
}
TOP, HAIR, SKIN = 'TtUu', 'HhLj', 'sk'


def detail(g, front):
    """More shading and small details, by rule, so every walk frame gets the same treatment. Light: upper left.
    Only the silhouette is shaded; fold lines inside a shape are left as drawn."""
    def sil(x, y, dx, dy, n=1):  # is the silhouette within n pixels in this direction?
        for i in range(1, n + 1):
            v = g.get((x + dx * i, y + dy * i))
            if v is None or (v == '#' and g.get((x + dx * (i + 1), y + dy * (i + 1))) is None):
                return True
            if v == '#':
                return False
        return False

    def shoe(x, y):  # inside a black shoe
        return y >= 56 and all(g.get(q) == '#' for q in ((x, y), (x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)))
    new = {}
    for (x, y), v in g.items():
        up, up2 = g.get((x, y - 1)), g.get((x, y - 2))
        if v == 'T':
            if sil(x, y, 1, 0, 2) or sil(x, y, 0, 1) or (up == '#' and up2 and up2 in SKIN + HAIR):
                new[x, y] = 't'                                         # far side, hem, shadow under the chin
            elif sil(x, y, 0, -1):
                new[x, y] = 'U'                                         # top of the shoulders
        elif v == 't' and (sil(x, y, 1, 0) or sil(x, y, 0, 1)):
            new[x, y] = 'u'
        elif v == 'd':
            if (up and up in TOP) or (up == '#' and up2 and up2 in TOP):
                new[x, y] = 'b'                                         # belt
            elif sil(x, y, 1, 0):
                new[x, y] = 'f'
            elif sil(x, y, -1, 0):
                new[x, y] = 'D'
        elif v == 's' and (sil(x, y, 1, 0) or (up and up in HAIR)):     # far side, shadow under the hair
            new[x, y] = 'k'
        elif v == 'h' and (sil(x, y, 1, 0) or sil(x, y, 0, 1)):
            new[x, y] = 'j'
        elif v == 'c' and g.get((x, y - 1), '#') == '#' and g.get((x + 1, y)) == 'c':
            new[x, y] = 'C'
        elif shoe(x, y) and not shoe(x, y - 1) and shoe(x + 1, y):
            new[x, y] = 'o'
    g.update(new)
    belt = [p for p, v in g.items() if v == 'b']
    if front and belt:
        mid = (min(x for x, _ in belt) + max(x for x, _ in belt)) // 2
        for p in belt:
            if p[0] in (mid, mid + 1):
                g[p] = 'g'


def rle(s):
    return ''.join(t[-1] * int(t[:-1] or 1) for t in s.split())

def frame(cfg, pal, tpl, r, c):
    stamp, head_end, offs = cfg['views'][r]
    dx, dy = offs[c]
    src = tpl.crop((c * 64, r * 64, c * 64 + 64, r * 64 + 64)).load()
    g = {}
    for y in range(head_end + dy + 1, 64):
        for x in range(40):  # art sits in the left of the frame; Saruli's sheet has stray pixels at x=63
            v = src[x, y][3] and cfg['role'].get('%02x%02x%02x' % src[x, y][:3])
            if v:
                g[x, y] = v
    # long sleeves: each arm is one blob of skin; its bottom 4 rows stay a hand
    skin = {p for p, v in g.items() if v in 'sk'} if cfg['long_sleeves'] else set()
    while skin:
        arm, todo = set(), [next(iter(skin))]
        while todo:
            p = todo.pop()
            if p in skin:
                skin.remove(p); arm.add(p)
                todo += [(p[0] + 1, p[1]), (p[0] - 1, p[1]), (p[0], p[1] + 1), (p[0], p[1] - 1)]
        hand = max(y for _, y in arm) - 3
        for p in arm:
            if p[1] < hand:
                g[p] = 'T' if g[p] == 's' and p[1] < hand - 1 else 't'   # last sleeve row is a cuff
    for y, row in stamp.items():
        for x, ch in enumerate(rle(row)):
            if ch == '.':
                g.pop((x + dx, y + dy), None)
            elif ch != '_':
                g[x + dx, y + dy] = ch
    detail(g, r == 0)
    out = Image.new('RGBA', (64, 64))
    for p, v in g.items():
        if 0 <= p[0] < 64 and 0 <= p[1] < 64:
            out.putpixel(p, tuple(bytes.fromhex(pal[v])) + (255,))
    return out

for name, cfg in CHARS.items():
    pal = {**PAL, **cfg['pal']}
    tpl = Image.open(os.path.join(HERE, '../..', cfg['sheet'])).convert('RGBA')
    sheet = Image.new('RGBA', (256, 256))
    for r in cfg['views']:
        for c in range(3):
            f = frame(cfg, pal, tpl, r, c)
            sheet.paste(f, (c * 64, r * 64))
            if r == 2 and cfg['mirror']:  # left row
                m = Image.new('RGBA', (64, 64))
                m.paste(ImageOps.mirror(f), (cfg['mirror'][c] - 63, 0))
                sheet.paste(m, (c * 64, 64))
    used = {'%02x%02x%02x' % p[:3] for _, p in sheet.getcolors() if p[3]}
    assert used <= E32, used - E32  # the one check: every pixel is ENDESGA 32
    sheet.save(os.path.join(HERE, name + '.png'))
    print(name + '.png', len(used), 'colours, all ENDESGA 32')
