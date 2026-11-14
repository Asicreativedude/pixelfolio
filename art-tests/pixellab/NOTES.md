# PixelLab test run (#61, PixelLab half)

Run on 2026-11-14 in the pixellab.ai web Character Creator, on Asi's **Free** account (40 fast generations,
1 job at a time). Branch `prototype/pixellab-test`. Never merge.

## Free tier (checked on pixellab.ai pricing + docs, 2026-11-14)

| | Free | Needed for |
|---|---|---|
| Generations | 40 fast, then 5/day (store 20) | |
| Max image | 200×200 | |
| Concurrency | 1 job at a time. A second job is refused ("Maximum 1 concurrent background jobs (Tier 0)") | |
| Characters, rotations, text animation | yes | |
| Map tools (Create map, Map Workshop) | **no**. The Maps nav is locked | Tier 1, $12/mo |
| Create tileset, Create texture | **no** (docs: "requires at least Tier 1") | Tier 1, $12/mo |
| Create walking character (32×32 instant walk) | **no** (docs: experimental, Tier 2) | Tier 2, $24/mo |

So **no tileset could be generated**, and the tileset remap/cleanup step wasn't run on PixelLab output.

## Attempts

Times are wall clock from submit to done, on the Free queue.

| # | What | Settings | Time | Gens | Result |
|---|---|---|---|---|---|
| A1 | 32 px character from text | v3, low top-down, highly detailed, black outline, 8 rotations | 2 min 15 s | 2 | Reads as "a guy with glasses and a beard": 17×28 px of art, 31 colours, not ENDESGA 32. Doesn't look like Pixelfolio's cast. At 2× it's **56 px tall vs the hero's 50**, too big |
| A1w | Walk on A1 | Free motion, PixMiniMax, **palette ENDESGA 32**, 8 frames/direction, 40×40 canvas | ≈2.5 min per direction: S, E, N generated; W mirrored from E (instant, free) | 3 | 100% ENDESGA 32 (15 colours), so the palette lock works. It chose green for the shirt. The stride is subtle |
| A2 | 64 px character from text | same as A1 at 64 px | ≈3 min | 2 | 41 colours, 34×62 px, painterly shading. Asi: "too high fidelity, almost no pixel art". Walk skipped |
| A3 | **From reference: Asi's own hero south frame** (`public/Hero/Sprite-Hero.png`, frame 0,0) | v3 rotation, 4 dir, auto skeleton | ≈3 min | 1 | South kept exactly as drawn. E/N/W match his size, outline and flat colours (9–20 colours). Misses: the hair is reinvented (side-swept quiff, whole back of the head grey) and the side-view face is softer |
| A3w | Walk on A3 | PixMiniMax, ENDESGA 32, 8 frames/direction, 80×80 canvas | ≈2 min per direction: S, E, N generated; W mirrored | 3 | Keeps his chunky style and size, 7–9 colours, all ENDESGA 32 (teal → `#0099db`). The side view inherits A3's wrong hair and face. Asi: "the side view of the character is off" |

Total: about 25 minutes of wall clock for 5 assets, almost all of it queue time (Free runs one job at a time).
13 of 40 generations used.

## Asi's verdict so far

- Text-to-character (A1, A2) doesn't look like any Pixelfolio character.
- 64 px from text is "too high fidelity, almost no pixel art".
- 32 px drawn 2× is "super big" next to the hero (56 px vs 50 px tall).
- From-reference (A3) is closest, but the side view is off.

## Seeing it

- `lineup-hall.png`: the sheets drawn onto `Hall2.png` exactly as the engine places them, at 3×. Columns: current hero,
  A3 (from Asi's hero), A1 (32 px at 2×), A2 (64 px). Rows: idle down, walk right, idle up.
- In game: `npm run dev` on this branch, then walk down from the spawn. Four test NPCs on row 8 loop through
  down/right/up/left. If Start Game throws `Cannot read properties of null (reading 'x')`, clear the
  `pixelDudeProgress` localStorage key: a pre-existing title-screen bug with a stale save.

Palette remap of A1's idle rotations (no PixelLab palette option exists at character creation):
- Aseprite `--palette e32.hex --color-mode indexed --dithering-algorithm none`: shirt → green, hair → navy (`a1-32-v3/e32/`).
- Nearest colour in Lab: shirt → bright cyan (`a1-32-v3/e32-lab/`).
- Neither is right. ENDESGA 32 has no mid teal, so the shirt ramp needs a hand pick (#60 found the same on the Hall).

## Files

- `aN-*/export.zip`: PixelLab's own export. Unzipped next to it: `Idle/rotations/*.png`, `Idle/animations/Walking/<dir>/frame_00N.png`, `metadata.json`.
- `build_sheet.py`: packs frames into Pixelfolio's 256×256 sheet (4×4 of 64 px frames, rows down/left/right/up, columns idle/walk-a/walk-b), scaling and anchoring feet like the existing characters.
- `sheet-*.png`: the sheets the Hall lineup uses (`src/world/maps.ts`, `testHero`/`testPx*`).
- `e32.hex`: the #60 palette file.
