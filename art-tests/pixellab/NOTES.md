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
- Asi then named what he likes, none of it pixel art: Arcane, Scavengers Reign, Retool's old site art, PostHog,
  Disco Elysium. `make_illustrated.py` → `illustrated.png` draws one office corner as illustration in the two
  families those fall into: line and flat colour (top), painted light with brush marks (bottom), each smooth at
  high resolution (left) and as pixel art at game scale (right). Custom palettes, not ENDESGA 32. The line family
  holds up in both; the painted family only works smooth, its pixel version turns to noise. About 40 minutes.
  Retool's old art could not be found online, so it is not represented.
- Asi on `illustrated.png`: "The drawings look baddd. Maybe try /anidoodle". He also sent Retool's art:
  hannah-meng.com/retool-brand (flat colour fields, isometric solids, thin tone-on-tone grid lines, white objects).
  `office-iso.png`: the office redrawn with the anidoodle skill's isometric kit in a hand adapted from that set:
  one hue family per picture, a ruled iso grid across the field, three tones per form, no outlines, white for
  what matters, one accent (the hero's teal shirt). Orange large, purple and coral below: one drawing, one map
  colour each. Source: `anidoodle/officeIso.ts` (needs the anidoodle engine to render; 1920×1080, vector, not
  pixel art, not ENDESGA 32). About 45 minutes. Known flaws: hands are mittens, the man stands stiff and
  symmetrical, the dog reads close to a fox.
- Asi: "Maybe use anidoodle for the other drawings as well". Two more stills of the same office, each drawn with
  anidoodle in a three-quarter top-down view (the game's own view), 1920×1080:
  - `office-line.png` (`anidoodle/officeLine.ts`): line and flat colour, built on the marker-comic plate. One pen
    weight, flat fills, one shadow tone, ten colours on cream, #F54E00 as the accent. About 25 minutes, 5 rounds.
    Weak: stiff legs, plain box furniture, a static layout.
  - `office-painted.png` (`anidoodle/officePaint.ts`): painted light, built on the oil-paint plate. Strokes stay
    on one plane of one object; a dark cool room lit by a teal screen and an orange lamp. About 40 minutes,
    5 rounds. Weak: a stiff blocky figure, fork-like fingers, ragged light pools.
  Both are vector or painted stills, not pixel art, and not game assets yet (no walk frames, no tiles).
- Asi on the painted still: "Can we somehow get the painted light style into our pixel art world?" Two ways,
  both from `make_painted_light.py`:
  - `painted-light-pixels.png`: the pixel room and pixel cast exactly as drawn, with only the light repainted by
    the painting's recipe (dark cool ambient, a teal screen and an orange lamp, four flat light levels with a
    wandering edge, each figure's shadow filled by the other light). Left as drawn, right in painted light.
    64 colours, not ENDESGA 32.
  - `painted-baked-pixels.png`: the painting itself shrunk to 640×360 (left) and 320×180 (right), 64 colours.
    It keeps the look, but the man is about 180 px tall at 640×360 against the game's 50 px hero, so it is a
    close-up. At the game's real scale most painted detail would be gone and mainly the light would remain.
  About 30 minutes. Neither runs in the game: the light is baked into a picture by the script.
- Asi on the first painted-light pixels: "Nice it looks a bit forced. And works in this specific scene though.
  Also lights and shadow don't seem pixelated at all." Second version of `make_painted_light.py` (it replaces
  `painted-light-pixels.png`; `painted-baked-pixels.png` is from the first version and is no longer generated):
  - Pixelated: a light is three flat steps, each ending on a clean edge with a two-pixel checker band. No noise.
    A figure's shadow is its own sprite laid on the floor away from the light. `painted-light-zoom.png` is a 6×
    crop to check this.
  - Less forced: the dusk is calmer, and the same office is shown by day and at night from other settings.
  - Another scene: the same code lights a crop of the existing Hall (lamp over the lounge, daylight from the door).
  - Open: lit colours are not palette-locked (51 colours by day, 358 at dusk). Warm light on the Hall's blue
    floor turns grey. Furniture casts no shadow from the new lights, only figures do. About 30 minutes.
- Asi on the second version: "lets work on those - if we need to re-adjust the color palette we can consider
  this", about its three open points. Third version of `make_painted_light.py`:
  - Grey floor: light no longer only multiplies. Where multiplying drains a surface's colour, the surface keeps
    its colour, gains a little, and its hue turns part of the way towards the light's hue. The Hall's blue floor
    goes violet under the warm lamp instead of grey.
  - Furniture shadows: every prop has a footprint and a height (taken from the cast offset `make_room.py`
    already gives it), and a pixel is in shadow when the way to the light crosses a tall enough footprint. The
    shadows baked into the room art are switched off for this, so light is the only source of shadow. The Hall
    is one flat picture, so there everything that is not floor counts as 8 px tall.
  - Palette: every lit pixel is snapped to a fixed palette. Tried on the dusk office (mean distance in OKLab
    from the colour asked for; lower is better): ENDESGA 32 alone 0.047, ENDESGA 64 0.035, Resurrect 64 0.049,
    AAP-64 0.050, and ENDESGA 32 plus 32 colours fitted to these scenes 0.027 (Hall: 0.039, 0.041, 0.040,
    0.052, 0.015). ENDESGA 32 alone loses the light (the floor stays one tone, the rug blotches). The
    ready-made 64s lose faces and turn the floor pool grey. The fitted one is close to free colour, so the
    sheet uses it: `palettes/endesga-32-plus-light.hex`, 64 colours, all five pictures use only these.
    `painted-light-palettes.png` shows ENDESGA 32, ENDESGA 64, the fitted palette and free colour side by side.
  - So the palette change this light needs: drawing stays in ENDESGA 32 (#60 holds), and the game gets 32
    more colours that only light may use. They are fitted to one warm lamp, one teal screen, one dusk and one
    night; other light colours would need the fit run again.
  - Open: still a picture made by a script, not light in the game. The Hall's art is not ENDESGA 32, so its
    unlit colours are snapped too. Heights are guesses. About 50 minutes.
- Asi on the ten researched directions: "lets preview a still image of each one cause from text I cant
  understand really how it looks". Done: `art-tests/claude-drawn/directions/`, one script and one 1056x720 still
  per direction, the same office corner each time, and `directions.png` with all ten labelled. Nine were drawn
  by three helper agents (17 to 23 minutes each for three stills); number 5 comes from the light work.
  What each still is, honestly:
  - 1 Muted world, loud clickables: 13 colours. `make_room.py`'s drawings recoloured, so it sits close to the
    current art; teal only on the hero, screen, notes, mat and the dog's bandana.
  - 2 Naive flat cartoon: 19 colours, room and cast redrawn. Wobble is a seeded 1 px wave, not a hand.
  - 3 Neon flat minimalism: 20 colours plus smooth glows. Figures are stiff and the hero's likeness is weak.
  - 4 One-bit plus one accent: 3 colours, all redrawn. Faces are crude icons; the hero's grey sides cannot exist.
  - 5 Lamp-lit dusk: the soft-light dusk office from `make_light_two_ways.py` (see below). The report's rule
    sheet asked for stepped rings; the light research says not to, so the still does not follow that rule.
  - 6 Lived-in clutter: 44 colours, about fifty new props, light drawn into the room as irregular patches.
    Busy; some small props are hard to read; the cast is not lit.
  - 7 Soft diorama: 32 low-saturation colours, room redrawn. Close to the cosy farming-game look.
  - 8 Desktop chrome: 23 colours. The frame is new; the room inside is still the old drawing, flattened.
  - 9 Portrait-led PC-98: 16 colours, native 528x360. The portrait is geometric, not hand-drawn quality.
  - 10 Paper cut-out: 16 colours (8 fills and their shadows). Leans towards flat tech illustration.
- Asi on the third light version: "i think we should research a bit how pixel art games deal with lights.
  something feels off and im not sure what". Research: `research_notes/Pixel art lighting/games.md` and
  `craft.md` (claims marked sourced or inference; several pages were blocked). What our light did that no
  documented game does: static rings of light (banding; the one game that had them, Dank Tomb, called them
  artificial), dither on the rings, one dark blue multiplied over everything, sprite-shaped shadows (Graveyard
  Keeper tried skewed ones and dropped them), colours snapped to a palette after blending, and no response to
  where the lamp is. What games do: smooth light at screen resolution over the pixel art (Stardew Valley,
  Graveyard Keeper, Celeste), night as a per-colour table or grade, lit areas back in the art's own colours,
  blob or stock shadows, and rim light or painted normal maps when light should show form (Animal Well,
  Eastward, Dead Cells). Moonlighter has no computed light at all: night is hand-made sprites.
- `make_light_two_ways.py` applies that: `light-two-ways.png` shows the dusk office and the Hall with soft
  light (left) and with light kept on the pixel grid (right: one hard-edged shape per light, a rim on the lamp
  side of characters). Both use a table (each drawn colour has one dusk colour and one colour per light) and
  blob shadows. My read: the soft one looks right; the hard-edged one reads as a spotlight painted on the
  floor. The pixel one uses 226 colours for 91 drawn colours in 6 states, so a fixed palette is possible there
  but large. This contradicts the earlier aim of pixel-stepped light ("lights and shadow don't seem pixelated
  at all" was said about the noisy first version). Waiting for Asi's reaction.
- Asi on the ten stills: "lived in clutter is nice direction" (direction 6). Second pass on that still by the
  same helper agent (about 10 minutes), first render kept as `directions/d06-lived-in-clutter-v1.png`:
  - The cast takes its colours from the room's ramps and is lit by where it stands (darker on the side away
    from the light), with contact shadows. Outline kept. Cost: faces are flatter than on the sheets.
  - A walking path is clear from the door to the desk and along the rug; cables, backpack and skateboard moved
    to walls. Unreadable props (headphones, banana, open box) removed; pizza box, backpack, fridge redrawn.
  - Light: no pool adds more than one ramp step and overlapping pools have different outlines, so no rings.
    The rug's diagonal edge in v1 was a bug (the noise that breaks band edges was switched off).
  - `d06-lived-in-clutter-evening.png`: the same drawing with the room's levels lowered, a dusk sky and no sun
    patches; lamp, screen, fairy lights and sign stay. Day and evening together use 44 colours (asserted 32 to
    48). So in this direction light is part of the drawing and stays on the palette, with no light layer.
  - `d06-lived-in-clutter-game-size.png` and `-evening-game-size.png`: the 352x240 room on the 640x360 canvas at
    2x, to judge how small the detail is in the game.
  - Still weak: the evening floor away from the lamp is nearly one tone; the hero's grey sides are 2 to 3 px;
    light direction on figures is left or right only. Not tested: more than this one room, walking in the game,
    a phone. The report's warning stands: this is the most expensive direction and the hardest to keep
    consistent. Waiting for Asi's reaction.
- Lived-in clutter in the game (Asi: "lets try putting it in the game"). Open `/?map=Clutter` or
  `/?map=ClutterEvening` on the dev server; it skips the title screen and saves nothing, so the real save is untouched.
  `art-tests/claude-drawn/directions/make_d06_game.py` exports to `art-tests/claude-drawn/game/`: the room without its
  cast (day and evening, 352x240, one screen pixel per art pixel), the four cast sheets in the room's colours, and
  `clutter.json` (walls, and which light each tile gives). Frames taken from the game's canvas: `game/in-game-*.png`.
  - Works: walking, collisions, the dog walking, talking to the three characters, day and evening.
  - Characters are lit by the room: each sheet holds 12 versions (6 light levels x light from left or right) and the
    game picks one by the tile under the feet. The change is per tile, so it snaps when a figure crosses a tile edge.
  - The room is 352x240 on a 640x360 screen, about 30% of it. The camera is fixed for this map, so the room sits
    centred with dark teal around it.
  - Only 18 of the 45 floor tiles are free to stand on. The clutter that makes the still look good takes the rest.
  - The shadow under the feet is a see-through dark teal blob in the sheet, so it is not held to the palette: a frame
    has 49 to 56 colours, the art has 44.
  - The dialogue box and the title screen are still in the old style and clash with the room.
  - Nothing can walk behind furniture: the room is one flat image, so every tile a prop touches is blocked.
  - Not tested: a phone (no touch controls on this branch; under 992 px wide the page stretches the canvas), a second
    room, a room larger than the screen with a moving camera.
  - Engine changes are small and marked `#65 test`: a map can bring its own objects, a fixed camera, a background
    colour and a light table (`maps.ts`, `defineWorld.ts`, `worldMap.ts`, `sprite.ts`, `gameObject.ts`, `main.ts`,
    `progressTracker.ts`). The red wall outlines are hidden on test maps.
- Larger room in the game (Asi: "Yes, larger room"): `/?map=Studio` and `/?map=StudioEvening`. A studio of 896x512 (28x16 tiles) in
  the lived-in clutter style, drawn for the tile grid by `claude-drawn/directions/make_d06_studio.py` and exported by
  `make_d06_game.py` (`game/studio-*.png`, `studio.json`, tile check in `game/studio-check.png`). It fills the 640x360 screen and
  the camera follows the hero and stops at the room's edges. 240 of 338 floor tiles are free (71%), all reachable from the door.
  45 colours over both rooms, day and evening. Walked in the preview by day and in the evening through seven stops with no
  errors; frames in `game/in-game-studio-*.png`. Weak points: the evening floor away from the lamps is dark, busy two-tone noise;
  the middle of the room is plain boards; the desk corner, plants and window view repeat the small room; the walk-behind layer
  is only lamp shades and was not seen working in a frame; a figure standing right below another covers it with its head;
  dialogue box still in the old style; no phone test.
- Studio, second pass (Asi: "The floor looks very much repetitive and like a bit broken. Let's work on that and the other weak
  points"). Floor: the blotches came from a blob noise and from wear patches that crossed the boards; now a plank is one of two
  woods half a step apart (new ramp WOOD, 3 colours, 48 in all) and tone changes at plank edges only, in both rooms, day and
  evening. Middle of the room: a fish tank on a cabinet (it is the middle's lamp in the evening) and a court taped round the
  table tennis. Walk-behind: `thing(tall=True)` marks what is height, not depth; the hero now stands behind the tank, the metal
  shelving and the arcade, seen in the game (`game/in-game-studio-*behind*.png`). The second window has its own skyline.
  Still open: light pools in the evening have smooth outlines now that the floor has no noise; the desk corner and the two
  potted plants are still the small room's drawings; a figure right below another covers it with its head (the engine's
  sorting, same in the Hall); the small room's `in-game-*.png` frames show the old floor; dialogue box, title screen, phone.
- Limits: the two people reuse an existing body, so a character gets the hero's or Saruli's build and walk. A new body
  (a child, the alien, a coat) means drawing that body once by hand or by code.
