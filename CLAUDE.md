# pixelfolio

Asi's career as a playable pixel-art game: Vite + TypeScript, one 640x360 canvas, served at `/play` on
asicreativedude.com. Tickets live in **RadicalButton/asi-creative-dude** (map #46), not here.

## Where things are

- `src/main.ts`: boot. Shows the title after 1 s. Screens switch through `src/utils/screenContorller.ts`
  (sic): title, character pick, about, world.
- `src/world/defineWorld.ts`: `World`. `init()`, `startMap()`, the loop (`startGameLoop` → `gameLoopStepWork`).
- `src/world/maps.ts`: room data. `worldMaps` (`Studio`, `Hall`), the hero and NPC configs, the dev switches.
- `src/world/worldMap.ts`: `WorldMap`. Walls, cutscenes, action and footstep triggers.
- `src/world/events/`: cutscene event types (`worldEvents.ts` dispatches on `event.type`) and their DOM overlays.
- `src/objects/`: `gameObject.ts` base, `person.ts` (walking, `startBehavior`), `mapElements.ts`, `collectables.ts`.
- `src/utils/`: `sprite.ts` (drawing, lit sheets), `directionInput.ts`, `keyPressListener.ts`,
  `progressTracker.ts` (the save), `touchControls.ts` (touch UI and the fit-to-window scaling), `utils.ts`.
- `src/titleScreen/`: title, character selection, about.
- `art/`: Python that draws the art into `public/`. `art/draw.py` holds the palette (`K`, `HI`, `RAMPS`) and the
  primitives; `art/rooms/<name>.py` are the rooms. Every script's header says what it writes.
- `public/rooms/<name>.json` + `<name>[-upper]-{day,evening}.png`: built by `art/room.py`, imported by `maps.ts`.

## Commands

- `npm run dev` (Vite). `npm test`: `node --test test/*.test.ts`, plain Node, no DOM. `npm run build`: `tsc`
  then `vite build`, the typecheck. Run both after a code change.
- Art: `npm run room [-- studio]` (no name: every room), `npm run cast [-- name]`, `npm run ui`,
  `npm run controls`. Each is `python3 -I art/<x>.py`. Pin Pillow/numpy to `art/requirements.txt`: other
  versions move pixels. `cast.py` only writes missing sheets (Asi touches them up); name one to overwrite it.
  `art/check/` is a local preview, gitignored.
- Vite warns "Assets in public directory cannot be imported" for `maps.ts`'s room JSON. It works; leave it.

## Driving the game in a browser

- Dev-only URL switches (`maps.ts`): `?map=Studio` or `?map=Hall` (exact key; it starts the hero on the room's
  entrance tile; an unknown name falls back to the Hall) and `?time=day` or `?time=evening` (default: the clock, evening 18:00 to 06:00).
  They apply when the world starts, not on the title.
- The save is localStorage `pixelDudeProgress`. Seed it to skip the character pick:
  `{"isFirst":false,"selectedCharacter":"/cast/iluz.png","gameProgress":{"asiConversation":0},"collectables":{},"lastMap":"","lastPosition":null}`
  then reload. The title still shows: wait over 1 s, then one Enter ("Continue Game") enters the world.
  Every finished step writes `lastPosition` (pixels), so the next load starts there unless `?map=` is set.
- `window.__world` (dev only, set in `World.init()`) is the live `World`: `__world.map.gameObjects.hero`,
  `__world.map.walls`, `__world.map.isCutscenePlaying`.
- Synthetic keys: dispatch on `document` with both `key` and `code`, `bubbles: true`, as `touchControls.ts`
  does. Movement reads `code` (`ArrowUp`, `KeyW`…); the title reads `key` on `window`; Enter in the world reads
  `code` on `document`. A keydown and keyup in the same task is gone before the loop reads it: hold the key
  across a frame, or call `hero.startBehavior({ map: __world.map }, { type: 'walk', direction: 'up' })`.
- A hidden or background browser pane does not run requestAnimationFrame (`document.hidden` still says
  false), so nothing moves. Read state through `__world` instead of watching for motion, or step frames
  yourself: `__world.gameLoopStepWork()` (16 steps walk one tile).
- An edit to a `.ts` file full-reloads the page, and the live modules then load as `/src/...?t=<n>`. A bare
  `import('/src/...')` from the console gets a separate fresh instance, not the game's. Use `__world`.
- The game scales to fit the window (`fit()` in `touchControls.ts`) on load and on `resize`. A preview
  viewport change may not fire `resize`: reload after one.

## Workflow

- Worktrees are siblings: `git worktree add ../pixelfolio-<n> -b <branch> origin/main`, then `npm ci` in it
  (or symlink the main clone's `node_modules`). `~/pixelfolio` is a stale clone; never use it.
- PR body: `Closes RadicalButton/asi-creative-dude#<n>`. A bare `#n` links this repo's own numbers.
  PRs merge with a merge commit.
- Commit subjects: `<feat|fix|art|refactor|docs>: <what is now true, in plain words> (#<ticket>)`.

## Code standards

- Imports match file case exactly (Vercel builds on Linux; PR #2). Type-only imports use `import type`
  (`verbatimModuleSyntax`). Tests import with the `.ts` extension; `src` imports without one.
- A class is its file's default export, one per file. Data and helpers are plain objects and functions.
- 2-space indent, single quotes, semicolons.
- New comments say why, citing the ticket (`(#69)`, `RadicalButton/asi-creative-dude#52`). A deliberate
  shortcut gets a `ponytail:` comment naming its limit.
- Tests are `node:test` + `node:assert/strict` on pure helpers and on the exported `public/` data, no DOM.
- Asi's own art files are only read. Scripts write new files; never overwrite his source images.
