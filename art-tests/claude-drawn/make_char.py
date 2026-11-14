# Draws a new NPC by code on the hero's body template (#61 side test: "can Claude just build the px chars?").
# Body, poses and walk frames come from public/Hero/Sprite-Hero.png (read only): recoloured to ENDESGA 32,
# short sleeves turned into long ones. The head is drawn here, pixel by pixel, for front, side and back,
# and stamped at each frame's head offset. Left = right mirrored.
#
# usage (repo root): python3 -I art-tests/claude-drawn/make_char.py
# Rows are run-length: "6. # 4H 2L" = 6 clear, 1 outline, 4 hair, 2 hair light. "_" keeps the template pixel.
import os
from PIL import Image, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__))
E32 = set(open(os.path.join(HERE, '../pixellab/e32.hex')).read().split())
PAL = {'#': '181425', 'H': 'f77622', 'h': 'be4a2f', 'L': 'feae34', 's': 'e8b796', 'k': 'c28569',
       'e': '3e2731', 'W': 'ffffff', 'M': 'b86f50', 'T': '3e8948', 't': '265c42', 'd': '3a4466'}
assert set(PAL.values()) <= E32
# hero colour -> role. Leftover beard/hair pixels below the neck become shirt shade.
ROLE = {'000000': '#', '150908': '#', '513407': '#', '191919': 'd', '121212': 'd', 'ebbf96': 's',
        'cba582': 'k', '0989a0': 'T', '076a7c': 't', '6c6c6c': 't', '4c4c4c': 't', '373737': 't', 'ffffff': 't'}

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
# sheet row -> (stamp, last template row that is all head, head offset per column idle/walk-a/walk-b)
VIEWS = {0: (FRONT, 30, [(0, 0), (0, 0), (-2, 0)]),
         2: (SIDE, 34, [(0, 0), (-1, 1), (-3, 0)]),
         3: (BACK, 33, [(0, 0), (-1, 0), (-2, 0)])}
MIRROR_AXIS = [31, 28, 24]  # where the hero's own left frames sit relative to his right frames

def rle(s):
    return ''.join(t[-1] * int(t[:-1] or 1) for t in s.split())

hero = Image.open(os.path.join(HERE, '../../public/Hero/Sprite-Hero.png')).convert('RGBA')

def frame(r, c):
    stamp, head_end, offs = VIEWS[r]
    dx, dy = offs[c]
    src = hero.crop((c * 64, r * 64, c * 64 + 64, r * 64 + 64)).load()
    g = {(x, y): ROLE['%02x%02x%02x' % src[x, y][:3]]
         for y in range(head_end + dy + 1, 64) for x in range(64) if src[x, y][3]}
    # long sleeves: each arm is one blob of skin; its bottom 4 rows stay a hand
    skin = {p for p, v in g.items() if v in 'sk'}
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
                g[p] = 'T' if g[p] == 's' else 't'
    for y, row in stamp.items():
        for x, ch in enumerate(rle(row)):
            if ch == '.':
                g.pop((x + dx, y + dy), None)
            elif ch != '_':
                g[x + dx, y + dy] = ch
    out = Image.new('RGBA', (64, 64))
    for p, v in g.items():
        out.putpixel(p, tuple(bytes.fromhex(PAL[v])) + (255,))
    return out

sheet = Image.new('RGBA', (256, 256))
for r in VIEWS:
    for c in range(3):
        f = frame(r, c)
        sheet.paste(f, (c * 64, r * 64))
        if r == 2:  # left row
            m = Image.new('RGBA', (64, 64))
            m.paste(ImageOps.mirror(f), (MIRROR_AXIS[c] - 63, 0))
            sheet.paste(m, (c * 64, 64))
used = {'%02x%02x%02x' % p[:3] for _, p in sheet.getcolors() if p[3]}
assert used <= E32, used - E32  # the one check: every pixel is ENDESGA 32
sheet.save(os.path.join(HERE, 'visitor.png'))
print('visitor.png', len(used), 'colours, all ENDESGA 32')
