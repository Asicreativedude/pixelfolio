# Direction 1, "Muted world, loud clickables" (reports/Pixel art style directions.md), as one still.
# The drawings are make_room.py's (the rule sheet: "proportions and shapes stay as they are"). What changes:
#   palette: 13 colours with roles. A cool neutral ramp (N0..N6), a short warm ramp for wood and skin that
#     starts and ends on the neutral ramp (N1, W1..W4, N6), one accent in two steps (A1, A2).
#   reserved: N0 (darkest) and N6 (brightest) only on characters and things the player can press.
#     The accent only on the hero and on things the player can press: screen, pin board, door mat, dog.
#   outline: characters and clickables get N0; inert furniture gets a tone two steps darker than its fill.
#   shading: flat. Every object is cut down to three shades at most, grain and gloss are dropped.
#   floor and walls are redrawn 1:1 (make_room's shell is a 16 px grid at 2x).
# usage (repo root): python3 -I art-tests/claude-drawn/directions/make_d01_muted_world.py
import os, sys
from PIL import Image, ImageChops

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.dont_write_bytecode = True  # this script writes nothing outside directions/
import make_room as mr  # noqa: E402  (read only: prop drawings and the E32 names they use)

N0, N1, N2, N3, N4, N5, N6 = '14121f', '2b2a41', '3f4561', '596a80', '7b9494', 'a7bdad', 'f5f1dc'
W1, W2, W3, W4 = '5c4254', '8d6259', 'bb8c6d', 'e4bf96'
A1, A2 = '0e8c9b', '2ae6c6'
PALETTE = {N0, N1, N2, N3, N4, N5, N6, W1, W2, W3, W4, A1, A2}
CAST = {N5: N4, N4: N3, N3: N2, N2: N1, W4: W3, W3: W2, W2: W1, W1: N1, N6: N5, A2: A1}   # one shadow step
OUTLINE = {N5: N3, N4: N2, N3: N1, N2: N1, N1: N1, W4: W2, W3: W1, W2: N1, W1: N1}           # inert furniture
m = mr
WOOD = {m.W1: W3, m.W2: W3, m.GRAIN: W3, m.W3: W2, m.W4: W2, m.W5: W1, m.W6: W1, m.INK: N1,
        m.GOLD: W3, m.YEL: W3, m.ORG: W2, m.RUST: W1, m.DRED: W1}
GREY = {m.WHT: N5, m.SL0: N5, m.SL1: N4, m.SL2: N3, m.SL3: N2, m.SL4: N1, m.INK: N1,
        m.GOLD: N4, m.YEL: N5, m.ORG: N3, m.RUST: N2, m.RED: N3, m.DRED: N2, m.ROSE: N4, m.BLU: N3, m.NAVY: N2,
        m.CYA: N4, m.G1: N4, m.G2: N3, m.G3: N2, m.G4: N1, m.PINK: N3, m.PLUM: N2,
        m.W1: N5, m.W2: N4, m.W3: N3, m.W4: N2, m.W5: W1, m.W6: N1, m.GRAIN: N3}
CHAIR = {**GREY, m.SL4: N3, m.SL3: N3, m.SL2: N4, m.SL1: N4, m.W5: N2}
POT = {**GREY, m.ORG: W2, m.GOLD: W3, m.RUST: W1, m.DRED: W1, m.W6: N1, m.W4: W1, m.W2: W2}
SHELF = {**WOOD, m.W2: W2, m.W1: W3, m.GRAIN: W2, m.W4: W1, m.W6: N1,    # books: greys and woods, no rainbow
         m.RED: W2, m.DRED: W1, m.ROSE: W3, m.BLU: N3, m.NAVY: N2, m.CYA: N4, m.GOLD: W3, m.YEL: W3, m.ORG: W2,
         m.RUST: W1, m.G1: N4, m.G2: N3, m.G3: N2, m.WHT: N5, m.SL0: N4, m.SL1: N4, m.SL2: N3, m.SL3: N2,
         m.PINK: W2, m.PLUM: W1}
RUG = {m.DRED: W1, m.RED: W1, m.GOLD: W2, m.YEL: W2, m.W1: W2}
# things the player can press: darkest outline, brightest paper, the accent
SCREEN = {m.SL3: N1, m.SL1: N3, m.SL4: A1, m.NAVY: N0, m.INK: N0, m.SL2: A2, m.G1: A2, m.RED: A2, m.GOLD: A2,
          m.PINK: A2, m.CYA: N6, m.WHT: N6, m.YEL: A2}
BOARD = {m.W5: W1, m.W4: W1, m.W6: N1, m.W3: W2, m.W2: W2, m.WHT: N6, m.SL0: N5, m.SL1: N3, m.RED: A2,
         m.ROSE: A2, m.CYA: A2, m.G2: A1, m.G1: A2, m.YEL: A2, m.BLU: A1, m.GOLD: A1, m.ORG: A1,
         m.PINK: N6, m.PLUM: N5}
MAT = {m.G2: A1, m.G1: A2, m.G3: A1, m.YEL: N6}
CLICK = {'monitor', 'cork', 'notes', 'photo', 'stickies', 'sticky2', 'ticket', 'mat'}
BY_PART = {'desk_body': WOOD, 'monitor': SCREEN, 'pot': POT}

# cast sheets: E32 colour -> palette, per character (existing characters need a recolour, not a redraw)
BODY = {'181425': N0, '262b44': N1, '3a4466': N2, '5a6988': N3, 'c28569': W3, 'e8b796': W4, 'ffffff': N6,
        '3e2731': N0, '733e39': W1}
PEOPLE = [
    ('hero-detailed.png', 0, 214, 104, {**BODY, '0099db': A2, '2ce8f5': A2, '124e89': A1, '8b9bb4': N4, 'feae34': W3}),
    ('dana.png', 1, 256, 118, {**BODY, 'fee761': N6, 'feae34': N6, 'd77643': W3, 'be4a2f': W2, 'e43b44': W2,
                               'f6757a': W2, 'a22633': W1, '124e89': N1}),
    ('dog.png', 2, 92, 146, {**BODY, 'd77643': W3, 'be4a2f': W2, 'ead4aa': N6, 'feae34': W4, 'e43b44': A2}),
    ('visitor.png', 2, 50, 104, {**BODY, 'f77622': W2, 'be4a2f': W1, 'feae34': W3, '3e8948': N4, '265c42': N3,
                                 '63c74d': N5, '193c3e': N2, 'a22633': W1, 'b86f50': W2}),
]


def rgb(c):
    return tuple(bytes.fromhex(c)) + (255,)


def hexof(p):
    return '%02x%02x%02x' % p[:3]


class Canvas(mr.Canvas):
    role = GREY

    def prop(self, fn, *a, cast=(2, 2)):
        """make_room's prop(), with this direction's rules: recolour by role, flat cast shadow, role outline."""
        layer = mr.Canvas(*self.im.size)
        fn(layer, *a)
        table = BY_PART.get(fn.__name__, self.role)
        click = fn.__name__ in CLICK
        lay, box = layer.im.load(), layer.im.getbbox()
        for y in range(box[1], box[3]):
            for x in range(box[0], box[2]):
                if lay[x, y][3]:
                    lay[x, y] = rgb(table[hexof(lay[x, y])])
        alpha = layer.im.getchannel('A')
        solid = alpha
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            s = Image.new('L', alpha.size); s.paste(alpha, (dx, dy)); solid = ImageChops.lighter(solid, s)
        px = self.im.load()
        if cast:
            sh = Image.new('L', alpha.size); sh.paste(solid, cast)
            sh, sbox = ImageChops.subtract(sh, solid), None
            sm, sbox = sh.load(), sh.getbbox()
            for y in range(sbox[1], sbox[3]) if sbox else ():
                for x in range(sbox[0], sbox[2]):
                    if sm[x, y]:
                        px[x, y] = rgb(CAST.get(hexof(px[x, y]), hexof(px[x, y])))
        edge = ImageChops.subtract(solid, alpha)
        em, ebox = edge.load(), edge.getbbox()
        for y in range(ebox[1], ebox[3]):
            for x in range(ebox[0], ebox[2]):
                if em[x, y]:
                    near = [lay[q] for q in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1))
                            if 0 <= q[0] < mr.W and 0 <= q[1] < mr.H and lay[q][3]]
                    px[x, y] = rgb(N0 if click else OUTLINE.get(hexof(near[0]), N1))
        self.im.alpha_composite(layer.im)


def shell():
    """Walls and floor at 1:1. Wall N4, floor N2; nothing here is darker than N1 or lighter than N5."""
    c = Canvas(mr.W, mr.H, N1)
    c.r(16, 8, 320, 56, N4); c.r(16, 8, 320, 2, N3)                      # wall, shadow under the ceiling
    c.r(16, 56, 320, 2, N5); c.r(16, 58, 320, 6, N3); c.r(16, 63, 320, 1, N1)   # skirting board
    c.r(16, 64, 320, 160, N2); c.r(160, 224, 32, 16, N2)                 # floor, doorway
    c.r(16, 64, 320, 3, N1)                                              # the wall's shadow on the floor
    for ty in range(96, 224, 32):                                        # tile corners, 1 px
        for tx in range(48, 336, 32):
            c.r(tx - 2, ty, 5, 1, N1); c.r(tx, ty - 2, 1, 5, N1)
    return c


def mat(c, x, y):
    def mat(c):  # named so the prop is a clickable
        c.r(x, y, 28, 12, m.G2); c.r(x + 2, y + 2, 24, 8, m.G1); c.r(x + 4, y + 4, 20, 4, m.G2)
        for i in range(5):
            c.r(x + 5 + 4 * i, y + 5, 2, 2, m.YEL)
    c.prop(mat, cast=None)


def room():
    c = shell()
    for role, fn, a in ((RUG, mr.rug, (52, 164, 248, 40)), (MAT, mat, (162, 208)), (GREY, mr.window, (52, 14)),
                        (BOARD, mr.board, (144, 12)), (GREY, mr.clock, (212, 18)), (SHELF, mr.bookshelf, (264, 12)),
                        (GREY, mr.plant, (22, 86)), (GREY, mr.bin_, (242, 72)), (GREY, mr.desk, (136, 68)),
                        (CHAIR, mr.chair, (156, 118))):
        c.role = role
        fn(c, *a)
    return c


def people(c):
    px = c.im.load()
    for src, row, x, y, table in PEOPLE:
        s = Image.open(os.path.join(HERE, '..', src)).convert('RGBA').crop((0, row * 64, 40, row * 64 + 64))
        sp = s.load()
        for sy in range(64):
            for sx in range(40):
                if sp[sx, sy][3]:
                    sp[sx, sy] = rgb(table[hexof(sp[sx, sy])])
        if src == 'dog.png':                                             # the dog's collar grows into a bandana
            for q in ((15, 50), (15, 51), (15, 52), (16, 53), (17, 53), (16, 54)):
                sp[q] = rgb(A1 if q[1] > 52 else A2)
        for sx in range(8, 32):                                          # a flat shadow under the feet
            for sy in range(60, 64):
                q = (x + sx + 2, y + sy)
                if abs(sx - 20) + 3 * abs(sy - 62) < 14:
                    px[q] = rgb(CAST.get(hexof(px[q]), hexof(px[q])))
        c.im.alpha_composite(s, (x, y))
    return c


if __name__ == '__main__':
    c = people(room())
    used = {hexof(p) for _, p in c.im.getcolors(99999)}
    assert used <= PALETTE and len(PALETTE) <= 16, used - PALETTE      # the one check: 13 colours, all assigned
    c.im.resize((mr.W * 3, mr.H * 3), Image.NEAREST).save(os.path.join(HERE, 'd01-muted-world.png'))
    print('d01-muted-world.png written,', len(used), 'colours')
