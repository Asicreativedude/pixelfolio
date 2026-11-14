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
11 of 40 generations used (account page).

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

## Side test: drawn by Claude, no PixelLab (`art-tests/claude-drawn/`)

Asi asked whether Claude can run Aseprite or just build the characters itself. Both work:

- `make_char.py` draws a new NPC by code. The body, poses and walk frames are the hero's own sheet, recoloured to
  ENDESGA 32 with long sleeves. The head (front, side, back) is drawn pixel by pixel in the script. Left is the
  right view mirrored. Result: `visitor.png`, 12 colours, 100% ENDESGA 32, same size and outline weight as the cast.
  About 15 minutes for the first character; a second one on the same template is a new head and a colour table.
- `to_aseprite.lua` runs in Aseprite's batch mode and turns a sheet into `visitor.aseprite`: 12 frames, tags
  down/left/right/up, indexed in ENDESGA 32. Aseprite runs headless only; Claude doesn't drive its window.
- `lineup-hall.png`: Saruli, Dana, hero, visitor on the Hall at 3×. Rows: idle down, walk
  right, idle up, idle left. In game the visitor is the fifth test NPC (column 19).
- Second test, a woman "like Saruli": `dana.png` / `dana.aseprite`. Saruli's body and walk (dress recoloured red),
  with a new head drawn in the script: long straight blonde hair instead of curls, blue eyes. 11 colours, all
  ENDESGA 32. About 20 minutes, most of it reading Saruli's frames, because her frames sit at different offsets
  from the hero's. In game: Saruli at column 22, Dana at column 25.
- Third test, nothing reused ("a dog, a desk, a part of a map"):
  - `make_dog.py` → `dog.png` / `dog.aseprite`: a dog in the cast's sheet layout (4 directions, idle + 2 walk
    frames), drawn pixel by pixel in the script at character density with a dark outline. 8 colours. In game:
    column 28. `dog-preview.png` is the sheet at 7×.
  - `make_room.py` → `desk.png`, `room.png` (+ `.aseprite`): a desk and an 11 × 7.5 tile office room (window, pin
    board, bookshelf, plant, chair, rug, doormat). `scene.png` is the room with the test cast, zoomed 3×.
    - v1 (`scene-v1.png`) followed #60's map rule: 16 px grid exported at 2×, no outlines. Asi: the dog looks
      great, but the desk and other props are "not the same visual language as the characters".
    - v2 redraws every prop the way the cast is drawn: 1:1 pixels, a 1 px dark outline per object, one shade and
      one highlight per colour. `desk-compare.png` shows v1 and v2 of the desk side by side. The floor and wall
      shell are still 16 px at 2× (Asi: "floor we can figure it out").
    - This goes against #60's "maps drawn at 16 px, exported 2×" for props. It is evidence for the open question
      of drawing maps at the characters' density.
    - Asi on v2: "Yessss much better. I do think they need a bit more details / shading / touch ups. It applies
      to characters as well (also ones I did already)."
    - v3 (`scene.png`; v2 kept as `scene-v2.png`): same language, more of it. Light from the upper left, and
      every object casts a shadow down-right onto what is under it (`Canvas.prop(cast=...)` darkens by one palette
      step). Surfaces get a lit and a dark edge. New details: a code editor on the monitor, keys, paper and pen,
      a lamp light pool, a city view in the window, a cactus, a clock, a bin, a trophy, book labels.
      `desk-compare.png` is v2 left, v3 right.
  - Characters, same feedback: `make_char.py` now runs a rule-based detail pass on every frame (wider far-side
    shadow, hem, shadow under the chin, third hair tone, belt and buckle, cuffs, shoe shine). It also writes
    `hero-detailed.png`: Asi's own hero recoloured to ENDESGA 32 with the same pass, his sheet untouched.
    `cast-compare.png` shows before (top) and after (bottom). The change on characters is small: rules can
    shade a silhouette, but faces and hair need hand work. The hero's teal shirt becomes blue and his grey hair
    turns blue-grey, because ENDESGA 32 has no teal and no neutral grey. In game: the detailed hero is column 31.
  - About 35 minutes for all three, plus 15 for the v2 props and 30 for v3. Everything is 100% ENDESGA 32.
  - Open points it shows: ENDESGA 32 has one mid slate blue, so the Hall's soft two-tone checker floor can't be
    kept; the room marks tile corners instead. The room isn't wired into the game (no walls, no map entry).
- Asi on the detailed version: "It's nice. Everything feels a bit like 2012 freepik pixel art. We miss some
  style no?" First probe: `make_styles.py` → `styles.png`, the same room four ways (as drawn; dusk with the lamp
  and screen as the only light; slate world with warm accents; toned outlines instead of one dark ink). These
  change palette, light and outline only. Shapes, proportions and what is in the room are the same drawing.
- Limits: the two people reuse an existing body, so a character gets the hero's or Saruli's build and walk. A new body
  (a child, the alien, a coat) means drawing that body once by hand or by code.
