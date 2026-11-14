# PROTOTYPE (wayfinder #60, branch prototype/style-lock): throwaway, never merge.
# Cuts a Hall strip + one character frame from COPIES of the art, remaps them into each
# candidate palette with the Aseprite CLI, and writes out/ for index.html.
# Run from repo root: python3 -I prototypes/style-lock/build.py
import subprocess, pathlib
from PIL import Image

ASE = '/Applications/Aseprite.app/Contents/MacOS/aseprite'
HERE = pathlib.Path(__file__).parent
OUT = HERE / 'out'
OUT.mkdir(exist_ok=True)

# Lospec ENDESGA 32 (26 of these are exact entries in public/pixelfolio.aseprite).
E32 = ('be4a2f d77643 ead4aa e4a672 b86f50 733e39 3e2731 a22633 e43b44 f77622 feae34 '
       'fee761 63c74d 3e8948 265c42 193c3e 124e89 0099db 2ce8f5 ffffff c0cbdc 8b9bb4 '
       '5a6988 3a4466 262b44 181425 ff0044 68386c b55088 f6757a e8b796 c28569').split()


def colours(*paths):
    s = set()
    for p in paths:
        s |= {'%02x%02x%02x' % px[:3] for px in Image.open(p).convert('RGBA').getdata() if px[3]}
    return sorted(s)


hall2 = Image.open('public/Hall2.png').convert('RGBA')
chars = [f'public/characters/{n}.png' for n in ('chich', 'iluz', 'saruli', 'alien')]
PALETTES = {
    'e32': E32,
    'hall41': colours('public/Hall2.png'),
    'asis': colours('public/Hall2.png', *chars),  # lock what already exists
}
for name, cols in PALETTES.items():
    # Index 0 becomes the transparent index in indexed mode, so give it a duplicate slot.
    (OUT / f'{name}.hex').write_text('\n'.join([cols[0]] + cols) + '\n')
    print(name, len(cols), 'colours')

# Sources (copies only). Hall2 is an exact 2x of the 16 px source, so halve it back to 1x.
hall1x = hall2.resize((640, 360), Image.NEAREST)
hall1x.crop((248, 216, 616, 360)).save(OUT / "src-scene.png")        # 368x144 source px
frame = Image.open(chars[0]).convert('RGBA').crop((0, 0, 64, 64))     # chich, idle down
frame.save(OUT / 'src-char64.png')
# ponytail: mechanical half-size, not a redraw. Shows the pixel-size match, not 32 px quality.
frame.resize((32, 32), Image.NEAREST).save(OUT / 'src-char32.png')

for pal in PALETTES:
    for src in ('scene', 'char64', 'char32'):
        subprocess.run([ASE, '-b', str(OUT / f'src-{src}.png'),
                        '--palette', str(OUT / f'{pal}.hex'),
                        '--dithering-algorithm', 'none', '--color-mode', 'indexed',
                        '--save-as', str(OUT / f'{pal}-{src}.png')], check=True)

# Check: the as-is palette must leave the art untouched.
for src in ('scene', 'char64'):
    seen = lambda p: [px if px[3] else 0 for px in Image.open(p).convert('RGBA').getdata()]
    assert seen(OUT / f'src-{src}.png') == seen(OUT / f'asis-{src}.png'), f'asis remap changed {src}'
print('ok')

# Swatches for index.html (a script tag, so the page works from file://).
import json
(OUT / 'palettes.js').write_text('window.PALETTES = ' + json.dumps(PALETTES) + ';\n')
