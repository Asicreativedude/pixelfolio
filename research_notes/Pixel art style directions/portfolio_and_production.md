# Playable portfolios and the production cost of 2D art styles (for Pixelfolio)

Research date: 2026-11-14. Conventions: every bullet under "Cited Findings" carries its source. Anything labelled **Observation** is my inference, not a sourced fact. "(search summary)" means the fact came from a search-result digest of the linked page and the page itself was not read in full, so treat it as lower confidence.

## 1. Which playable / game-like portfolio sites are well known, what art style did each use, and what did reviewers single out? Are there pixel-art RPG portfolios, and how did they differentiate?

### Takeaway
The portfolios that became reference points (Bruno Simon's car, Robby Leonardi's résumé, Jesse Zhou's ramen shop) each committed to one tightly bounded, personal visual idea (a toy car on an orange floor, a hand-illustrated platformer starring the author) and reviewers praised personality and play, not fidelity. Top-down pixel-art RPG portfolios exist in numbers, including a freeCodeCamp tutorial and commercial templates, so the format alone no longer differentiates; the ones with write-ups stand out through hand-made art, a personal setting (own room, own cat) and world feedback, not through the RPG framing.

### Cited Findings

**Bruno Simon, 3D car portfolio (2019 version)**
- Launched October 24, 2019, "After 3 months of work"; more than 400,000 visitors by January 23, 2020; built with Blender (modelling), Three.js (rendering), Cannon.js (physics) — [Pastel blog, Jan 2020](https://usepastel.com/blog/how-a-design-portfolio-got-the-attention-of-400-000-visitors)
- His stated reasons were personal: "physics isn't used enough in web" and "I loved Micro Machine on Playstation when I was a kid" — [Pastel blog](https://usepastel.com/blog/how-a-design-portfolio-got-the-attention-of-400-000-visitors)
- Awwwards Site of the Month for November 2019 (post dated Dec 17, 2019), described as a "3D WebGL playful portfolio". Art notes from that article: everything modelled low-poly in Blender 2.8; most materials are custom shaders; a blur at top and bottom of the screen to suggest smallness (tilt-shift); "a huge glow on the left to imitate sun flare"; captions show a toy car on an orange background. He tested on a phone, then added touch controls and adjusted layout for small portrait screens — [Awwwards SOTM article](https://awwwards.com/bruno-simon-portfolio-wins-site-of-the-month-november.html)
- Awwwards lists it as Site of the Year and Developer Site of the Year in the 2019 annual awards — [Awwwards annual awards 2019](https://awwwards.com/annual-awards-2019); Creative Bloq dates the Site of the Year win to 2020 — [Creative Bloq](https://www.creativebloq.com/news/3d-car-portfolio) (search summary; likely the same award announced in 2020, unresolved)

**Bruno Simon, 2025/2026 version**
- Awwwards case study dated March 11, 2026; project took "a little over a year". Still a car game, now with racetrack, leaderboard, achievements that unlock vehicle skins, shared day–night cycle, weather and seasons ("everyone experiences the same conditions at the same time") — [Awwwards case study](https://www.awwwards.com/brunos-portfolio-case-study.html)
- Visual direction: he has "always been fascinated by stylized 3D nature"; grass is one triangle per blade (~78,400 blades); UI is built as 3D models in the world instead of HTML; all scene colour comes from one palette texture ("The palette is a texture that contains all the scene's colors") — [Awwwards case study](https://www.awwwards.com/brunos-portfolio-case-study.html)
- Performance stance: "if the experience runs at 10 FPS, no one will stick around"; "On mobile devices, the experience automatically switches to a lower quality preset" (no water blur, no depth of field, smaller shadow maps). Stack: Three.js with TSL, WebGPU when available — [Awwwards case study](https://www.awwwards.com/brunos-portfolio-case-study.html)
- Awwwards also lists "Bruno's Portfolio" with a Site of the Month tag dated Jan 2026 — [Awwwards listing](https://www.awwwards.com/sites/brunos-portfolio) (search summary)

**Robby Leonardi, interactive résumé (2013)**
- Published October 2013 as a résumé in the form of a Mario-style side-scrolling platformer; you "level-up" as you progress; works with arrow keys, touchscreen or scroll wheel — [The Next Web, Oct 24, 2013](https://thenextweb.com/news/guys-resume-style-super-mario-world-probably-best-youll-see-long-time)
- Reviewer (Liv Siddall, It's Nice That, Oct 21, 2013) singled out that people like finishing small games so they read the whole CV, that his personality "comes straight through", and ended with "Robby, you're hired" — [It's Nice That](https://www.itsnicethat.com/articles/animation-robby-leonardi)
- He chose illustration as the main style because he likes to draw, and added the game element to make it unique; nominee for Best Online Portfolio in the 2014 net Awards — [Business Insider India](https://www.businessinsider.in/need-inspiration-for-a-new-resume-this-super-mario-inspired-interactive-cv-will-pump-you-up/articleshow/52397229.cms), [Creative Bloq / net magazine](https://creativebloq.com/netmag/robby-leonardi-his-zigzagging-path-success-31410874) (both search summary; Creative Bloq page would not load)
- A 2024 academic paper treats it as the model for "game resumes" and notes it still draws praise eleven years on — [Press Start journal](https://press-start.gla.ac.uk/index.php/press-start/article/download/317/152) (search summary)

**Jesse Zhou, "Jesse's Ramen" portfolio (2022)**
- Awwwards Honorable Mention, March 22, 2022; listing describes it as the portfolio of Jesse Zhou, a management consultant in Toronto — [Awwwards listing](https://www.awwwards.com/sites/jesses-ramen-portfolio)
- Source is public (repo "Jesse's Ramen Shop Portfolio", about 1.0k stars, 155 commits) — [GitHub enderh3art/Ramen-Shop](https://github.com/enderh3art/Ramen-Shop)
- Other developers reuse and credit his 3D ramen-shop model for their own portfolios — [Medium tutorial](https://medium.com/@harshadwani/quickly-create-a-3-d-interactive-responsive-portfolio-website-c1c6ef6c715d) (search summary)

**Pixel-art and RPG-style portfolios**
- Chris Simmons (endigodesign.com, Aug 6, 2022): built to look and feel like "a traditional 2D top-down RPG game". 16x16 tiles; "several uniquely styled biomes" group the projects; NPC dialog boxes modelled on old 2D Pokémon games; project pillars animate once visited; "Layla the Cat" follows the cursor. Rendered with Pixi.js inside Svelte/SvelteKit. Mobile: tap-and-drag camera, tap to interact; a traditional site is kept as fallback — [DEV post](https://dev.to/endigo9740/my-new-portfolio-3ke6)
- Larissa Cristina "Mewmew" (Feb 2026, DEV portfolio challenge): top-down walkable version of her own room; "Most of the pixel art you see was handcrafted by me"; a "consistent color palette"; Windows 95/XP and PlayStation 2 nostalgia; objects (computer, console, backpack) open projects, mini-games, résumé; entry choices include Full Experience, Résumé, Desktop, Video Game. React 18 + Vite + TypeScript, XState, i18n in three languages — [DEV post](https://dev.to/mewmewdevart/i-built-a-retro-gamified-portfolio-yes-with-pixel-art-games-windows-95-vibes-589k)
- JSLegendDev / freeCodeCamp course (April 3, 2024): "Build a Dev Portfolio as a 2D Game" using Kaboom.js and Tiled; pitch is "showing is better than telling" — [freeCodeCamp](https://www.freecodecamp.org/news/create-a-developer-portfolio-as-a-2d-game/). The video links a shared spritesheet, map file and the Monogram font; repo at github.com/JSLegendDev/2d-portfolio-kaboom — [search summary of course listing](https://classcentral.com/course/freecodecamp-build-a-dev-portfolio-as-a-2d-game-javascript-course-288285)
- Commercial templates now sell the format: Draftbit "8-Bit Quest" (pixel "Player One" developer portfolio) — [Draftbit](https://draftbit.com/website-templates/8-bit-quest/); Framer "WorldLegion" (portfolio explored as a map, content edited via CMS) — [Framer](https://www.framer.com/marketplace/templates/worldlegion/) (both search summary)
- Studio brand game: Basement Studio, "Basement Chronicles: The Internet Needs You" (2023), a "pixel-packed, point-and-click adventure"; FWA Site of the Day, Awwwards Site of the Day and Developer Award; described as "a love letter to old-school gaming, but with a basement twist" — [basement.studio](https://basement.studio/showcase/basement-chronicles-the-internet-needs-you.md)

### Inferences
- **Observation:** The award-level examples are 3D (Bruno, Jesse Zhou) or illustrated (Leonardi). I found no top-down pixel-art RPG personal portfolio with a top Awwwards or FWA award; the only awarded pixel-art example found is a studio point-and-click (Basement). A well-art-directed pixel RPG portfolio is therefore under-represented at award level, while being common at tutorial level.
- **Observation:** The freeCodeCamp course ships one shared spritesheet and font, and templates exist. A Pixelfolio built on stock tiles would read as "that tutorial". Custom, visibly authored art is the differentiator, which matches what the two documented pixel portfolios did (hand-made art, own room, own cat).
- **Observation:** Recurring pattern across all the famous ones: one object or avatar that is the author (car, cartoon self, own room), one dominant background colour or light condition (orange floor, bright sky), and the UI folded into the world. Both documented pixel portfolios and Bruno keep a non-game fallback or quality preset for mobile.
- **Observation:** Bruno's single palette texture for a whole 3D world is the same idea as a locked indexed palette for 2D: colour decisions are made once and assets only reference them.

### Gaps
- Jesse Zhou's art style (commonly described as a neon-lit night-time ramen shop) and build method are not described in any page I could read; his README and any write-up were not retrievable. Treat style claims about it as unverified.
- Bruno Simon's own 2019 Medium case study returned HTTP 403, so matcap/shadow details are not confirmed here.
- No jury commentary text was available for any Awwwards/FWA entry; "what reviewers singled out" rests on press articles.
- I did not find a reliable, dated list of FWA winners that are personal game portfolios.

## 2. Per-asset production effort and helpful tooling for each style family

### Takeaway
Sourced developer accounts consistently say that tight colour constraints (1-bit, or 4–16 colours with fixed roles) make assets fast and automatically cohesive, with the cost shifting to readability design; full-colour detailed pixel art, runtime-lit pixel art and hand-drawn art cost the most per asset or per iteration. For a scripted plus AI plus Aseprite pipeline, restricted-palette pixel art with a small, role-assigned palette is the cheapest style to keep consistent across many maps.

### Cited Findings

**Full-colour detailed pixel art**
- Raymond Schlitter (Slynyrd) builds large palettes from ramps: "9 swatches per ramp with 20 degrees of positive hue shift between each swatch", totalling "128 colors"; he used a 160-colour palette on one game — [Slynyrd Pixelblog 1](https://www.slynyrd.com/blog/2018/1/10/pixelblog-1-color-palettes)
- He warns that over-detailing comes from an artist "massaging the clusters", and that the work "becomes digital illustration when the pixels become irrelevant" — [Slynyrd Pixelblog 47](https://www.slynyrd.com/blog/2023/11/26/pixelblog-47-tiny-pixels)
- Dead Cells' sole artist for the first year judged hand-drawn pixel animation too slow and built a 3D pipeline to get "great looking pixel art, without having to hand draw each and every retake" — [Game Developer, Jan 25, 2018](https://www.gamedeveloper.com/production/art-design-deep-dive-using-a-3d-pipeline-for-2d-animation-in-i-dead-cells-i-)
- Mobile art director Valeria Getman (Playkot, Oct 13, 2026): "On a mobile screen, many beautifully rendered micro-details will simply never be visible"; "Quality does not mean maximum detail" — [Mobidictum](https://mobidictum.com/?p=410027)

**Restricted-palette pixel art (4 to 16 colours)**
- Shovel Knight kept the NES palette ("only capable of spitting out 54 different colors") plus four added "cheater" colours, with "4-5 colors to work with in addition to transparency" per sprite; limiting colours and detail kept characters clear and easy to animate — [Game Developer, June 25, 2014](https://www.gamedeveloper.com/design/breaking-the-nes-for-shovel-knight)
- Bloodless caps the screen at 12 colours (seven lit environment shades plus five unlit accents). The team began with black, white and red specifically for fast art production; later "each color added had to be thoroughly discussed"; palette limits were "very useful for building a visual hierarchy" — [Game Developer, Aug 20, 2024](https://gamedeveloper.com/art/deep-dive-behind-the-starkly-stylish-art-direction-of-bloodless)
- A shared fixed palette "will ensure everything in your game has consistent colors", and with hue-shifted ramps "every color is surrounded by colors that can work together" — [Slynyrd Pixelblog 1](https://www.slynyrd.com/blog/2018/1/10/pixelblog-1-color-palettes)
- Tooling: Lospec's palette list shows 4,547 palettes, filterable by exact/min/max colour count, downloadable as PNG, JASC PAL, Photoshop ASE, Paint.net TXT, GIMP GPL and HEX. Most downloaded shown: Lospec500 (42 colours, 106,358 downloads) and CC-29 (29 colours, 94,827 downloads) — [Lospec palette list](https://lospec.com/palette-list)

**1-bit / two-colour**
- Solo developer Jamie Rowan (Lelu, interview dated June 8, 2026): two colours are "a great limitation for a solo developer" that let him make assets "relatively quickly", but "a lot of thought and time had to go into shading and making sure that all the assets are readable". Tools: Aseprite, Blender with Rigify, GameMaker, LDtk. He accepts the look will not appeal to everyone — [80.lv](https://80.lv/articles/solo-developer-on-creating-a-black-and-white-adventure-game-about-a-clockwork-toy/)
- Return of the Obra Dinn runs at 640 by 360 in 1-bit; Lucas Pope found telling 80 characters apart in 1-bit harder than expected and cut the crew to 60; face readability and dither flicker were the main problems — [Game Developer](https://www.gamedeveloper.com/design/lucas-pope-and-the-rise-of-the-1-bit-dither-punk-aesthetic), [PlayStation Blog](https://blog.playstation.com/archive/2019/10/17/lucas-pope-on-return-of-the-obra-dinns-art-style), [PC Gamer](https://www.pcgamer.com/lucas-pope-on-the-challenge-of-creating-obra-dinns-1-bit-aesthetic/) (search summary; pages not read in full)

**Flat, no-outline shapes**
- Sable's team wanted a style "quick to produce, quick to iterate on, and visually consistent"; the cost was readability: "One big issue with making a flat shaded world with characters and backgrounds is reading depth". Fixes were outlines, cast shadows (including a moonlight shadow so the player nearly always casts one) and distance fog, which had "the biggest impact overall" — [Game Developer, GDC 2022 report](https://www.gamedeveloper.com/marketing/how-shedworks-refined-the-art-of-sable-in-pursuit-of-readability)
- Bruno Simon's 2026 world assigns all colour from one palette texture via UVs — [Awwwards case study](https://www.awwwards.com/brunos-portfolio-case-study.html)

**Pixel art with runtime lighting or colour grading**
- Bloodless: moving from a fixed palette to a lit, dithered palette made production more iterative, with palettes, shaders and light parameters adjusted late; water took over a month; the author says they should have tested performance sooner and that normal maps in Unity's 2D pipeline are costly. Lighting had to be consistent across all objects or mismatches stood out — [Game Developer](https://gamedeveloper.com/art/deep-dive-behind-the-starkly-stylish-art-direction-of-bloodless)
- Phaser's Light2D pipeline only lights objects that have a normal map; sprites without one disappear unless given a flat default — [Phaser forum](https://phaser.discourse.group/t/phaser3-webgl-lights-light2d-am-i-missing-something-or-are-they-broken/3016), [Phaser docs](https://docs.phaser.io/phaser/concepts/gameobjects/light) (search summary)
- PixelLab's API lists a normal-map utility among its endpoints — [PixelLab API llms.txt](https://api.pixellab.ai/v2/llms.txt)

**Hand-drawn line art**
- Hollow Knight's Ari Gibson photographed hand-drawn sketches with a phone and cleaned them up on computer; characters were animated by hand in traditional 2D; the team "decided to go for simplicity when possible" because the world was large — [Game Informer](https://www.gameinformer.com/2018/10/16/the-making-of-hollow-knight), [MCV](https://mcvuk.com/when-we-made-hollow-knight/) (search summary; low confidence on details)

**Low-res 3D rendered to pixels**
- Dead Cells pipeline: a basic 2D pixel model sheet, then a 3D model and skeleton (3DS Max, FBX), rendered by a homebrew tool "in a very small size and without antialiasing, giving us that pixelated look"; each frame exported with a normal map and lit by "a basic toon shader" — [Game Developer](https://www.gamedeveloper.com/production/art-design-deep-dive-using-a-3d-pipeline-for-2d-animation-in-i-dead-cells-i-)
- Payoff: "we can adjust the timing of the animations dozens of times in minutes"; reusing models for new monsters saved "hundred of hours of work" — [Game Developer](https://www.gamedeveloper.com/production/art-design-deep-dive-using-a-3d-pipeline-for-2d-animation-in-i-dead-cells-i-)
- Drawbacks: "we still haven't found any solution for flickering pixels"; "The disappointing level of details is and always will be an issue in my eyes" — [Game Developer](https://www.gamedeveloper.com/production/art-design-deep-dive-using-a-3d-pipeline-for-2d-animation-in-i-dead-cells-i-)

**General**
- Mixing asset packs produces an inconsistent look because each pack has its own palette and detail level; advice is to pick a constrained set of colours with roles (dominant neutrals, support colours, one accent) and write a style guide — [Wayline blog](https://www.wayline.io/blog/indie-game-visual-identity-design), [Bugnet blog](https://bugnet.io/blog/art-direction-beats-art-budget) (search summary; vendor blogs, practitioner opinion)

### Inferences
Ranking for Pixelfolio's constraints (640×360, 64×64 frames, 4 directions × 2 walk frames, many maps, scripted and AI-assisted drawing, Aseprite touch-up). All **Observation**:

| Style family | Per-asset effort | Consistency across maps | Distinctiveness | Fit with script/AI + Aseprite |
|---|---|---|---|---|
| Restricted palette, 8–16 colours with fixed roles | Low to medium | High; palette lock enforces it mechanically | Medium to high, depends on palette and shape language | Best: any generated asset can be quantised to the palette, then fixed by hand |
| 1-bit / 2–4 colours | Low per asset, high readability-design cost | Very high | High, but polarising and hard for telling many characters apart | Good for scripts; AI output needs heavy cleanup after thresholding |
| Flat no-outline shapes | Low | High if palette is fixed | Medium; depth and grounding need shadows or outlines added back | Excellent for script-drawn assets; weak fit for AI pixel generators |
| Restricted palette + cheap runtime grading (per-map tint, light masks) | Low to medium plus a one-off engine cost | High; grading unifies imperfect assets | High; gives each career "era" map a mood from the same assets | Good on canvas 2D if grading is baked or done with compositing |
| Full-colour detailed pixel art | High | Low without strict rules; AI drift shows most here | Low to medium (the default look of AI generators and asset packs) | Tempting with AI, expensive to fix by hand |
| Normal-mapped lit pixel art | High (two maps per asset, engine work) | Medium; mismatches are obvious | High | Needs WebGL; poor fit today |
| Hand-drawn line art | High per frame | Depends on one hand | High | Poor fit for scripts and pixel AI tools |
| Low-res 3D rendered to pixels | High setup, low per extra animation | Very high for characters | Medium to high | Only pays off with many animations; 2-frame walks do not justify it |

- **Observation:** With only 8 frames per character (4 directions × 2 frames), animation volume is small, so the consistency problem is mostly props, tiles and palette, not animation. That favours a palette-and-rules solution over a pipeline solution like Dead Cells'.
- **Observation:** Obra Dinn used exactly 640×360, the same logical resolution as Pixelfolio, and still needed special care for face readability in 1-bit. Full 1-bit is risky for a portfolio where distinct people and logos must be recognisable; a 1-bit base plus one or two accent colours (as Bloodless did with unlit accents) keeps most of the speed.
- **Observation:** The recommended direction from this evidence is a locked palette of roughly 12–16 colours with assigned roles, flat or two-step shading, and identity carried by one signature accent plus per-map grading done at runtime.

### Gaps
- No source gives measured hours per asset by style; all effort claims are developer testimony.
- Evidence for hand-drawn line art cost is thin (search summaries only).
- No sourced account of flat no-outline 2D top-down production specifically; Sable is 3D and used as the nearest documented case.

## 3. Runtime techniques that cheaply add style on canvas / WebGL 2D, with libraries and mobile cost

### Takeaway
Most cheap style wins (per-map palette swap, day/night tint, hard-edged light masks, baked outlines and drop shadows, parallax, small particles) are achievable on a plain 2D canvas if work is pre-rendered to offscreen canvases and compositing is kept to a few full-screen operations per frame. Per-pixel effects every frame (LUT grading, CRT curvature, normal-mapped lighting, live outline shaders) need WebGL, and `ctx.filter` cannot be relied on because Safari has not shipped it.

### Cited Findings

**Palette swap and look-up tables**
- WebGL technique: store the image as a single-channel index texture and the palette as a 256×1 RGBA texture; fragment shader does `float index = texture2D(u_image, v_texcoord).a * 255.0;` then `texture2D(u_palette, vec2((index + 0.5) / 256.0, 0.5))`. Both textures must use `gl.NEAREST`. Palette cycling or swapping is done by re-uploading the tiny palette texture — [WebGL2 Fundamentals](https://webgl2fundamentals.org/webgl/lessons/webgl-qna-emulating-palette-based-graphics-in-webgl.html)
- For non-indexed PNGs, a LUT texture maps any RGB colour to a replacement at render time — [Yanrishatum gist](https://gist.github.com/Yanrishatum/86794e9e663a7e343f9ef66e8b0f38ae) (search summary)
- Canvas 2D precedent: Joseph Huckaby's HTML5 colour-cycling engine renders 8-bit indexed images with cycling palettes into a canvas in real time. Naively, 640×480 means "drawing 307,200 pixels per frame, in JavaScript"; the optimisation is to precompute which pixels reference animated colours so "only the pixels that change are refreshed onscreen". With that it ran "at a pretty decent speed on my iPhone 3GS and iPad". Artwork by Mark Ferrari; code LGPL v3 — [Effect Games](http://www.effectgames.com/effect/article-Old_School_Color_Cycling_with_HTML5.html)
- A pre-processing alternative is to recolour sprites once on the CPU instead of in a per-pixel shader loop — [GameDev.net thread](https://gamedev.net/forums/topic/634725-hlsl-pixel-shader-that-does-palette-swap/5004829/) (search summary)
- Library: `pixi-filters` (v6.x for PixiJS v8.x) includes ColorMapFilter, ColorReplaceFilter, MultiColorReplaceFilter, ColorOverlayFilter, AdjustmentFilter, HslAdjustmentFilter — [pixi-filters docs](https://pixijs.io/filters/docs/)

**Colour grading, day/night tint, light masks on canvas 2D**
- `globalCompositeOperation` provides blend and compositing modes on a 2D context (including `multiply` and `destination-out`) — [MDN](https://developer.mozilla.org/docs/Web/API/CanvasRenderingContext2D/globalCompositeOperation)
- Darkness with light holes: fill an offscreen layer dark, set `destination-out`, draw each light shape, then draw the layer over the scene — [Phaser devlog "Creating a night map"](https://noobongames.itch.io/noob-detective/devlog/176581/beginners-devlog-3-creating-a-night-map-in-phaser-3-its-getting-dark), [html5gamedevs thread](https://html5gamedevs.com/topic/56469-dark-overlay-with-multiple-dynamically-changing-gradient-holes) (search summary)
- Safari caveat: a WebKit bug reports roughly a 10× performance penalty for `destination-in`, `source-in`, `source-out` and `source-atop` relative to other modes (seen in Safari 12, 13 and Technology Preview) — [WebKit bug 209802](https://auto-bugs.webkit.org/show_bug.cgi?id=209802) (search summary; `destination-out` and `multiply` are not in that list)
- `CanvasRenderingContext2D.filter` (blur, brightness, contrast, drop-shadow, grayscale, hue-rotate, saturate, sepia, url()) is flagged "Limited availability ... not Baseline because it does not work in some of the most widely-used browsers" — [MDN](https://developer.mozilla.org/en-US/docs/Web/API/CanvasRenderingContext2D/filter). MDN's compatibility data lists Safari desktop and iOS as unsupported; caniuse shows the OffscreenCanvas variant unsupported on iOS Safari through 26.5; a polyfill exists — [caniuse](https://caniuse.com/mdn-api_canvasrenderingcontext2d_filter), [caniuse OffscreenCanvas filter](https://caniuse.com/mdn-api_offscreencanvasrenderingcontext2d_filter), [context-filter-polyfill](https://npmjs.org/package/context-filter-polyfill) (search summary); WebKit bug 198416 is titled as fixed but no shipping release was confirmed — [WebKit bug 198416](https://bugs.webkit.org/show_bug.cgi?id=198416) (search summary; conflicting signals)
- Shared-world day–night, weather and seasons are a headline feature of Bruno Simon's 2026 portfolio — [Awwwards case study](https://www.awwwards.com/brunos-portfolio-case-study.html); Sable used per-biome fog as "the framework" for its day–night cycle — [Game Developer](https://www.gamedeveloper.com/marketing/how-shedworks-refined-the-art-of-sable-in-pursuit-of-readability)

**Normal-mapped lighting (WebGL only)**
- Phaser Light2D: requires a normal map per texture; LightsManager exposes `maxLights`; no built-in occlusion by obstacles — [Phaser docs](https://docs.phaser.io/phaser/concepts/gameobjects/light), [LightsManager API](https://docs.phaser.io/api-documentation/3.88.2/class/gameobjects-lightsmanager), [Phaser forum](https://phaser.discourse.group/t/lights-in-phaser-3-and-obstacles/14228) (search summary)
- Phaser 3.60 added an automatic Mobile Pipeline using a single bound texture for mobile GPUs; an earlier dev log notes branching shaders cost more on low-end mobile — [Phaser 3.60 changelog](https://cdn.jsdelivr.net/npm/phaser@4.1.0/changelog/v3/3.60/WebGLRenderer.md), [Phaser dev log 242](https://phaser.io/devlogs/242) (search summary)
- Dead Cells lights pre-rendered sprites through per-frame normal maps and a toon shader — [Game Developer](https://www.gamedeveloper.com/production/art-design-deep-dive-using-a-3d-pipeline-for-2d-animation-in-i-dead-cells-i-); Bloodless found normal maps costly and wished it had tested performance earlier — [Game Developer](https://gamedeveloper.com/art/deep-dive-behind-the-starkly-stylish-art-direction-of-bloodless)

**CRT, scanline, dither, outline, shadow filters (WebGL via PixiJS)**
- `pixi-filters` lists CRTFilter, OldFilmFilter, DotFilter, PixelateFilter, OutlineFilter, DropShadowFilter, GlowFilter, BloomFilter/AdvancedBloomFilter, RGBSplitFilter, SimpleLightmapFilter, TiltShiftFilter, GodrayFilter — [pixi-filters docs](https://pixijs.io/filters/docs/)
- Cost guidance from PixiJS: "Filters are expensive, using too many will start to slow things down!"; set `filterArea` when size is known; sprite masks "are really expensive"; "Different blend modes break batches"; on mobile, `antialias: false` and `backgroundAlpha: 1` help; "On older devices use smaller low-resolution textures" — [PixiJS performance tips](https://pixijs.com/8.x/guides/concepts/performance-tips)
- Bloodless uses Bayer-pattern dithering as part of its lit palette look and keeps accent colours unaffected by lighting — [Game Developer](https://gamedeveloper.com/art/deep-dive-behind-the-starkly-stylish-art-direction-of-bloodless)
- Bruno Simon's 2019 site used a top-and-bottom blur to suggest smallness and a large glow as sun flare — [Awwwards SOTM article](https://awwwards.com/bruno-simon-portfolio-wins-site-of-the-month-november.html)

**Drop shadows, parallax, particles**
- Slynyrd draws drop shadows as separate layers or bakes them into the tile where there is room — [Slynyrd Pixelblog 47](https://www.slynyrd.com/blog/2023/11/26/pixelblog-47-tiny-pixels)
- Sable added shadows specifically so players can judge position on a surface — [Game Developer](https://www.gamedeveloper.com/marketing/how-shedworks-refined-the-art-of-sable-in-pursuit-of-readability)
- Shovel Knight used five to six parallax background layers, which made the gameplay layer more readable, and deliberately limited particle effects to avoid clutter — [Game Developer](https://www.gamedeveloper.com/design/breaking-the-nes-for-shovel-knight)

**Canvas 2D performance rules (MDN)**
- Pre-render repeated drawing to an offscreen canvas; round coordinates ("Sub-pixel rendering occurs when you render objects on a canvas without whole values"); do not scale in `drawImage`; layer multiple canvases; put static backgrounds in CSS; "have a smaller canvas and scale up rather than a bigger canvas and scale down" using CSS transforms; pass `alpha: false`; "Avoid the `shadowBlur` property whenever possible"; "Avoid text rendering whenever possible" — [MDN Optimizing canvas](https://developer.mozilla.org/en-US/docs/Web/API/Canvas_API/Tutorial/Optimizing_canvas)
- Chris Simmons chose Pixi.js over raw canvas for his RPG portfolio and moves the world container as the camera — [DEV post](https://dev.to/endigo9740/my-new-portfolio-3ke6)

### Inferences
Which techniques work on the current plain 2D canvas, and which need WebGL. All **Observation**:

| Technique | Plain canvas 2D | Needs WebGL | Expected mobile cost |
|---|---|---|---|
| Palette swap, baked at map load (getImageData once per sheet, cache result) | Yes | No | Load-time only; zero per frame |
| Palette swap / LUT every frame | Only for small regions | Yes for full screen | One extra texture fetch per pixel in WebGL; too slow in JS for full frames beyond simple cases |
| Per-map colour grade | Yes if baked into cached sheets, or one `multiply` fillRect per frame | LUT version needs WebGL | One full-screen composite at 640×360 (230,400 px) |
| Day/night tint | Yes (`multiply` or semi-transparent overlay) | No | Same as above |
| Hard-edged light masks | Yes (offscreen dark layer + `destination-out` shapes) | No | One offscreen fill, N small shapes, one drawImage; hard edges avoid gradients and suit pixel art |
| Normal-mapped sprite lighting | No | Yes | Doubles texture authoring; per-light shader cost |
| Scanlines | Yes as a pre-rendered pattern overlay or a CSS overlay above the canvas | Curvature/bloom need WebGL | Near zero as CSS overlay |
| Ordered dither transitions | Yes with a pre-rendered Bayer pattern and compositing | No | Low |
| Sprite outline | Yes if baked at load (draw sprite silhouette offset in 4 directions, then sprite) | Live shader needs WebGL | Load-time only |
| Drop shadows | Yes as a shared ellipse sprite or baked into tiles; avoid `shadowBlur` | No | One extra drawImage per character |
| Parallax | Yes (extra layers or CSS background layers) | No | Low |
| Particles | Yes for tens of small integer-aligned sprites | Hundreds or more need batching | Low if capped |

- **Observation:** Because the logical canvas is 640×360 and is scaled up by CSS, every full-screen composite touches 230,400 pixels regardless of the phone's physical resolution. That is fewer pixels than the 307,200 the 2010-era canvas colour-cycling engine pushed on an iPhone 3GS, so one or two full-screen composites per frame should be safe on current phones. This needs a real-device test; no current benchmark was found.
- **Observation:** Do not build the look on `ctx.filter`. Use baked sheets plus compositing so iOS Safari renders identically.
- **Observation:** The cheapest high-impact combination for Pixelfolio is: one locked palette, per-map palette remap or tint baked at map load, a hard-edged light mask for interiors or night maps, a shared drop-shadow sprite, and a signature accent colour excluded from tinting (mirroring Bloodless's unlit accents). None of it needs WebGL.
- **Observation:** If a move to WebGL is ever wanted, PixiJS is the lowest-friction route since `pixi-filters` already contains LUT, CRT, outline and lightmap filters; filters should be applied once to the whole scene container, not per sprite.

### Gaps
- No current (2025–2026) benchmark of canvas 2D `multiply` or `destination-out` on iOS Safari or low-end Android was found; the WebKit bug data is old (Safari 12–13).
- Safari's exact status for `ctx.filter` in late 2026 is unresolved (MDN/caniuse say unsupported; a WebKit bug is marked fixed).
- No documented default for Phaser's `maxLights` or measured Light2D mobile frame rates was retrieved.
- No source measured CRT/scanline shader cost on mobile browsers.

## 4. What Aseprite offers for enforcing a style, and documented scripted or AI-assisted pixel-art workflows (2025–2026)

### Takeaway
Aseprite can mechanically enforce a palette (indexed mode, palette files, CLI conversion with optional ordered dithering, shading ink that only moves along chosen ramps) and can be driven headlessly with Lua, so a "generate, quantise to the locked palette, export sheet" step can be scripted. PixelLab (API, hosted MCP server, Aseprite export, 4/8-direction characters, tilesets) and Retro Diffusion (local Aseprite extension, palettize and repair tools) are the two documented pixel-specific AI options; independent 2026 reviews warn that AI output still has inconsistent pixel sizes, fuzzy edges and frame-to-frame drift that require hand cleanup.

### Cited Findings

**Aseprite**
- Three colour modes: RGB, Indexed, Grayscale. In Indexed mode each pixel points to a palette entry (up to 256 colours), so editing a palette colour changes every pixel that uses it — [Aseprite docs: Color Mode](https://www.aseprite.org/docs/color-mode/)
- Shading ink: paint a base colour, choose the "Shading" ink, select a set of palette colours that includes the base; left click will "move colors to the left of the gradient" and right click "move colors to the right" — [Aseprite docs: Shading](https://www.aseprite.org/docs/shading/). It only affects colours that are part of the selected gradient — [Aseprite community](https://community.aseprite.org/t/shading-layer-and-how-it-works/657) (search summary)
- Tilemaps: "Since Aseprite v1.3 you can create tilemaps with tilesets". Draw Pixels has three tileset modes: Manual (edit tile content, tileset order fixed), Auto (default; creates/reuses tiles and removes unused ones), Stack (creates a new tile for each change, originals untouched) — [Aseprite docs: Tilemap](https://www.aseprite.org/docs/tilemap/)
- CLI for batch pipelines: `--batch`, `--palette` (apply a palette file), `--color-mode` (`rgb`, `grayscale`, `indexed`), `--dithering-algorithm` (`none`, `ordered`, `old`), `--dithering-matrix` (`bayer8x8`, `bayer4x4`, `bayer2x2` or an extension's matrix), `--sheet`, `--data` (JSON), `--sheet-pack`, `--split-layers`, `--split-tags`, `--split-slices`, `--scale`, `--trim`, `--tag`, `--export-tileset` (v1.3-beta21+), `--script`, `--script-param`. Headless script example: `aseprite -b -script-param key1=value1 -script test.lua` — [Aseprite docs: CLI](https://www.aseprite.org/docs/cli/)
- Lua scripting API (Lua 5.3) exposes Sprite, Image, Palette, Tileset, Tile, Cel, Layer, Tag, Slice, Dialog, Events, Plugin, Timer, WebSocket, plus `app.command`, `app.pixelColor` and `json` — [Aseprite API](https://www.aseprite.org/api/)
- Commands callable from scripts include ChangePixelFormat, ColorQuantization ("Creates a palette from the current sprite"), LoadPalette, ReplaceColor, Outline, HueSaturation, BrightnessContrast, ColorCurve, InvertColor, Despeckle, CanvasSize, ExportSpriteSheet; parameters are passed as `app.command.CommandName { ["param-name"]="value" }` and are documented only in the source (`gui.xml`, `src/app/commands/`) — [Aseprite API: app.command](https://www.aseprite.org/api/app_command)

**Lospec**
- Palette list of 4,547 palettes with colour-count filters and downloads in PNG, PAL, ASE, TXT, GPL, HEX — [Lospec](https://lospec.com/palette-list)

**PixelLab (as of November 2026)**
- API v2 covers: text-to-image with several models (pixen, pixflux, bitforge, Pro, Pro Flash); style-based generation; image-to-pixel-art; characters with 4 or 8 directions, animation and states; objects; skeleton animation, interpolation, outfit transfer; inpainting and editing; top-down and sidescroller tilesets, isometric tiles, map objects, rooms; UI panels, portraits, pixel fonts; utilities for colour reduction, pixel-art correction, background removal, normal maps, resize — [PixelLab API llms.txt](https://api.pixellab.ai/v2/llms.txt)
- Exports include ZIP, spritesheet, GIF and Aseprite files via `/characters/{character_id}/aseprite` and `/objects/{object_id}/aseprite`; Python and JS/TS SDKs; a hosted MCP server at api.pixellab.ai/mcp for Claude, Cursor and Windsurf — [PixelLab API llms.txt](https://api.pixellab.ai/v2/llms.txt)
- Site lists style-consistent generation ("Create characters and objects that match your game's style"), 4 and 8 directional views, one-click and skeleton animation, "True inpainting", and an editor built on Pixelorama — [pixellab.ai](https://www.pixellab.ai/)
- Pricing (third-party, official page did not render): entry tier $12/month for 2,000 images ($8.25/month billed yearly), $50/month "Architect" tier with 10,000 images, free trial of 40 fast generations then 5 slower per day; commercial use allowed; an Aseprite extension is listed — [Ludo.ai comparison, "checked November 2026"](https://ludo.ai/compare/ludo-vs-pixellab) (competitor's page). G2 names the $12 tier "Pixel Apprentice" and the next "Pixel Artisan" — [G2](https://ai.g2.com/marketplace/tools/pixellab) (search summary)

**Retro Diffusion (as of November 2026)**
- Aseprite extension is a one-time purchase: $65 full, $20 Lite; runs locally; version 15.0.0; future patches free to buyers — [itch.io listing](https://astropulse.itch.io/retrodiffusion)
- Features: text-to-pixel-art with a built-in model, smart colour reduction, text-guided palette creation, Palettize and Color Style Transfer, Neural Pixelate / Resize / Detail, Tiling modifier, background removal, PixFix cleanup filter, more than a dozen styles. The extension does not do animation or sprite sheets (website only) — [itch.io listing](https://astropulse.itch.io/retrodiffusion); docs include Palettize ("can reduce and re-map image colors to fit color requirements"), K-Centroid Resize and Repair Pixel Art menus — [Retro Diffusion docs index](https://astropulse.gitbook.io/retro-diffusion/llms.txt)
- Reported speeds for 64×64 at quality 5: RTX 3090 under 2 s, RTX 3060 about 5 s, M1 Pro 26 s; an M1 with 8 GB was called below minimum — [itch.io listing](https://astropulse.itch.io/retrodiffusion)
- The developer says the extension is being phased out in favour of a standalone editor and updates have slowed; website and extension "use different models" — [itch.io listing](https://astropulse.itch.io/retrodiffusion), [Cinevva guide](https://app.cinevva.com/guides/ai-pixel-art-generators)
- Web app pricing is credit-based, quoted as $5 for 250 credits up to $50 for 3,500 credits — [SpriteCook comparison](https://www.spritecook.ai/compare/retro-diffusion) (competitor's page, search summary)
- Model trained on licensed assets from Astropulse and consenting artists; buyers own generated images (developer comment) — [itch.io listing](https://astropulse.itch.io/retrodiffusion)

**Known limits of AI pixel art (independent 2026 guide, updated Nov 8, 2026)**
- Images can "resemble pixel art while containing inconsistent pixel sizes, fuzzy edges or details that disappear" at game scale; downscaling "alone cannot repair poor silhouettes, inconsistent frames or missing details"; a posed skeleton does not guarantee consistent pixels; check palettes for drift between frames — [Cinevva guide](https://app.cinevva.com/guides/ai-pixel-art-generators)
- Other tools and prices in that guide: Scenario Starter $15/month, Pro $45/month with custom model training; Sprite-AI Creator $8/month for 100 tokens; Ludo Indie $20/month — [Cinevva guide](https://app.cinevva.com/guides/ai-pixel-art-generators)

**Scripted pipelines**
- Dead Cells is the best-documented scripted pixel pipeline: models rendered small without antialiasing by a homebrew tool, with normal maps exported per frame — [Game Developer](https://www.gamedeveloper.com/production/art-design-deep-dive-using-a-3d-pipeline-for-2d-animation-in-i-dead-cells-i-)
- Lelu's solo developer combines Aseprite with Blender and Rigify — [80.lv](https://80.lv/articles/solo-developer-on-creating-a-black-and-white-adventure-game-about-a-clockwork-toy/)

### Inferences
- **Observation:** A style gate can be fully automated: keep one palette file in the repo; run every generated or script-drawn PNG through `aseprite -b in.png --palette pixelfolio.gpl --color-mode indexed --dithering-algorithm none --save-as out.aseprite`, then export sheets with `--sheet` and `--data`. Whether `--palette` followed by `--color-mode indexed` remaps to nearest palette colours exactly as wanted should be verified with one test file; if not, a short Lua script using Image and Palette can do nearest-colour mapping. `--save-as` is standard Aseprite CLI but was not in the excerpt I retrieved.
- **Observation:** Indexed mode plus shading ink means hand touch-up cannot introduce off-palette colours, and a later palette tweak recolours every asset at once. That is the main reason a small locked palette is cheap to keep consistent.
- **Observation:** A CI-style check is trivial: a script that fails if any exported PNG contains a colour not in the palette, or if a character sheet is not 64×64 × (4×2) frames.
- **Observation:** Asset roles split naturally: script-drawn for geometric props, tiles and UI (deterministic, always on-palette); PixelLab for characters where 4-direction consistency is the hard part; Aseprite for final cleanup. Retro Diffusion's extension is a weaker bet in late 2026 given the stated phase-out and Apple Silicon speed.
- **Observation:** AI generators default to full-colour, heavily shaded pixel art. Forcing output through a 12–16 colour palette removes much of the "AI look" and the drift between assets, at the cost of manual fixes where quantisation breaks a shape.

### Gaps
- PixelLab's official pricing page would not render; all prices come from a competitor's comparison page and a marketplace listing. Confirm on pixellab.ai before budgeting.
- PixelLab's maximum canvas sizes and whether it supports forcing a specific input palette were not found in the pages read.
- Retro Diffusion's current web model line-up and palette-input options were not retrieved.
- Aseprite's price and whether error-diffusion dithering is available from the CLI were not confirmed (CLI docs list only `none`, `ordered`, `old`).
- Parameter names for `ChangePixelFormat` and `ColorQuantization` are only in Aseprite's source, not the docs page.

## 5. Readability rules for small sprites on phone screens

### Takeaway
The consistent rule across sources is that readability is decided by value (light/dark) separation between characters, walkable ground and background, then by silhouette, and only then by colour and detail; contrast must be rationed so only what matters has it. On phones, art directors test at real in-game size with a squint or desaturation test, exaggerate key features, and stop adding detail once shape and focal points read.

### Cited Findings
- Check values by desaturating: "Take a screenshot, desaturate it, and see if you can immediately and easily understand the image" — Peter Angstadt, [Game Developer, Mar 12, 2015](https://gamedeveloper.com/design/how-to-reduce-visual-confusion-in-your-game)
- Organise values by role: in DOTA 2 the ground uses darker greys than heroes and units, heroes are the brightest and highest-contrast areas, and the ground "has detail but its difference between it's light and dark values is small so as not to draw attention". Limbo inverts this (light background, very dark gameplay elements). "The key idea is to come up with a plan for organizing your values within the scene" — [Game Developer](https://gamedeveloper.com/design/how-to-reduce-visual-confusion-in-your-game)
- Ration contrast: "Too much contrast in too many places is equally confusing"; "Contrast draws attention, and if everything is drawing attention, nothing will" — [Game Developer](https://gamedeveloper.com/design/how-to-reduce-visual-confusion-in-your-game)
- A worked failure: background, enemies and walkable surfaces were all the same grey; the fix was to darken the background, brighten walkable surfaces and brighten the character — [Game Developer](https://gamedeveloper.com/design/how-to-reduce-visual-confusion-in-your-game)
- Mobile art director Valeria Getman (Playkot, Oct 13, 2026): squint at the image to see which elements survive; judge at "actual in-game size"; exaggerate ("Sometimes a dagger has to become almost as large as a sword simply so that players can see"); "Spend your art budget where the player's attention is"; stop when shape, silhouette and focal points work — [Mobidictum](https://mobidictum.com/?p=410027)
- Shovel Knight: large characters are placed over black or very dark backgrounds; dark purple and dark red were added as bridges from black so colours separate from the background; sprites use 4–5 colours; simplifying a design (King Knight) improved readability; alpha transparency replaced by flashing — [Game Developer](https://www.gamedeveloper.com/design/breaking-the-nes-for-shovel-knight)
- Bloodless: characters are flat black and white with accent colours only on details; environment objects use up to five of seven shades; accent colours are exempt from lighting — [Game Developer](https://gamedeveloper.com/art/deep-dive-behind-the-starkly-stylish-art-direction-of-bloodless)
- Saturation budgeting: saturation "peaks around the middle and never fully goes to 100, or 0"; "The biggest mistake is combining high saturation and brightness"; lighter colours need less saturation — [Slynyrd Pixelblog 1](https://www.slynyrd.com/blog/2018/1/10/pixelblog-1-color-palettes)
- Tiny sprites: Slynyrd's typical character is 16×32 px and he can halve tile size to 8×8 "with little compromise" while keeping "everything ... there for basic readability"; missing detail is part of the appeal because viewers fill gaps — [Slynyrd Pixelblog 47](https://www.slynyrd.com/blog/2023/11/26/pixelblog-47-tiny-pixels)
- Grounding and depth: Sable added cast shadows so players can judge position, used outlines to show overlap and scale, and fog for distance — [Game Developer](https://www.gamedeveloper.com/marketing/how-shedworks-refined-the-art-of-sable-in-pursuit-of-readability)
- Faces in very low colour depth: Obra Dinn needed players to recognise faces across scenes, which was hard in 1-bit and led to a smaller cast — [Game Developer](https://www.gamedeveloper.com/design/lucas-pope-and-the-rise-of-the-1-bit-dither-punk-aesthetic) (search summary)
- Practitioner blogs (lower authority): "most readability failures are value failures"; prefer a single outer silhouette with interior shapes suggested by value steps because interior outlines break the outer read; test in motion at 1× — [Bugnet](https://bugnet.io/blog/readable-game-art-why-clarity-beats-detail), [Gamine AI](https://gamineai.com/blog/10-pixel-art-composition-rules-readability-in-game-2026) (search summary)

### Inferences
All **Observation**, applied to Pixelfolio's numbers:
- A 640×360 canvas fitted to a 390×844 CSS-pixel phone in portrait scales by about 0.61, so a 64×64 frame shows at roughly 39 CSS px and one art pixel is about 0.6 CSS px (under 2 device pixels at 3× density). In landscape the height limits scale to about 1.08, so a frame is about 69 CSS px. Portrait is the stress case: any feature under 2 art pixels wide will blur or vanish.
- Non-integer scaling will soften pixel edges unless the canvas uses `image-rendering: pixelated` and accepts uneven pixel widths; thin 1-px interior lines are the first casualty. This favours chunky shapes, 2-px minimum features and a dark outer outline on characters.
- Value plan to adopt: reserve the darkest value and the brightest value for characters and interactive props; keep floor and wall tiles within a narrow mid-value band with low internal contrast; let the signature accent colour appear only on things the player can interact with.
- Saturation budget: desaturated environment, one saturated accent per screen region. Per-map tinting must not touch the accent or the character's outline value, or readability will vary by map.
- Because the character occupies only part of its 64×64 frame, design the body silhouette to read as a blob at roughly 20–24 px tall (the size it will appear in portrait) and treat faces as 2–4 px features. Distinguish NPCs by silhouette and one colour block, not facial detail.
- Add a drop-shadow sprite under every character and movable prop; it is the cheapest grounding cue and survives any tint.
- Build the test into the workflow: a script that renders a screenshot at 0.6× and in greyscale for each map is the automated version of the squint test.

### Gaps
- No source addressed phone-specific pixel-art readability (viewing distance, sub-integer scaling) directly; the mobile guidance is from a 3D/2D mobile RPG art director and generalised.
- Valve's Dota 2 Character Art Guide (the usual primary source for value-gradient and saturation rules) returned HTTP 403; its rules are cited only second-hand via the Game Developer article.
- No GDC talk specifically on small-sprite readability was retrieved; no Supercell source was found.
- No quantified contrast thresholds (for example a minimum luminance ratio between sprite and ground) were found.

## 6. What makes a personal or brand game feel authored rather than generic

### Takeaway
In the documented cases, "authored" comes from a small number of personal, repeated decisions: a self-avatar or object that stands for the maker, props and settings from the maker's real life, one dominant colour or light condition, a deliberately limited palette where each colour was argued for, and UI that lives inside the world. Brand designers describe the same thing as a system (colour, shape language, texture, motion) that stays constant while mood changes.

### Cited Findings
- Personality is what reviewers reward: It's Nice That said Leonardi's personality "comes straight through" his résumé-game and that you get a sense of what he looks like — [It's Nice That](https://www.itsnicethat.com/articles/animation-robby-leonardi)
- Leonardi chose illustration because he likes to draw and added the game to be unique — [Business Insider India](https://www.businessinsider.in/need-inspiration-for-a-new-resume-this-super-mario-inspired-interactive-cv-will-pump-you-up/articleshow/52397229.cms) (search summary)
- Bruno Simon's concept came from personal taste: "I loved Micro Machine on Playstation when I was a kid"; "you cannot work on a project for months if you don't enjoy yourself"; the writer called the site "a playground where you can see his craft and creativity in full display" — [Pastel blog](https://usepastel.com/blog/how-a-design-portfolio-got-the-attention-of-400-000-visitors), [Awwwards SOTM article](https://awwwards.com/bruno-simon-portfolio-wins-site-of-the-month-november.html)
- A consistent scale cue and light: toy car on an orange backdrop, tilt-shift blur to suggest smallness, a glow imitating sun flare — [Awwwards SOTM article](https://awwwards.com/bruno-simon-portfolio-wins-site-of-the-month-november.html)
- UI inside the world: in the 2026 version he avoided HTML UI and built the interface as 3D models; a single palette texture colours the whole scene; achievements unlock skins — [Awwwards case study](https://www.awwwards.com/brunos-portfolio-case-study.html)
- Self-referential props in pixel portfolios: Chris Simmons' "Layla the Cat" who watches the cursor, pillars that animate after you visit a project, biomes that group projects — [DEV post](https://dev.to/endigo9740/my-new-portfolio-3ke6); Mewmew's portfolio is her own room with her computer, console and backpack as the menu, in hand-made art with a consistent palette and Windows 95/XP and PS2 references — [DEV post](https://dev.to/mewmewdevart/i-built-a-retro-gamified-portfolio-yes-with-pixel-art-games-windows-95-vibes-589k)
- Studio voice on top of genre: Basement Chronicles is "a love letter to old-school gaming, but with a basement twist" — [basement.studio](https://basement.studio/showcase/basement-chronicles-the-internet-needs-you.md)
- Named influences plus constraints: Sable's look draws on Moebius, Studio Ghibli and architect Carlo Scarpa and grew from the limits of a small team — [Game Developer](https://www.gamedeveloper.com/marketing/how-shedworks-refined-the-art-of-sable-in-pursuit-of-readability)
- A recognisable constraint as identity: Shovel Knight kept the NES palette because it gives the look its distinctiveness and added only four colours for specific needs — [Game Developer](https://www.gamedeveloper.com/design/breaking-the-nes-for-shovel-knight)
- Colour as a debated resource: Bloodless capped the screen at 12 colours and "each color added had to be thoroughly discussed"; accents are exempt from lighting so they always read — [Game Developer](https://gamedeveloper.com/art/deep-dive-behind-the-starkly-stylish-art-direction-of-bloodless)
- Consistent light is part of the look: in Bloodless, lighting had to be consistent across objects or details that broke it stood out — [Game Developer](https://gamedeveloper.com/art/deep-dive-behind-the-starkly-stylish-art-direction-of-bloodless)
- Brand-system view: a game brand is typography, colour palettes, shape language, texture, motion and tone working together; recurring motifs can be embedded in key art; you can "change the mood without having to change the identity" — PlayStation brand designers reported at [Thumbsticks](https://www.thumbsticks.com/how-playstation-built-a-brand-system-for-the-horizon-franchise/) (search summary; attribution of individual quotes between speakers not verified)
- What reads as generic: mixing asset packs, each with its own palette and detail level, produces a jarring, inconsistent look — [Wayline blog](https://www.wayline.io/blog/indie-game-visual-identity-design) (search summary; vendor blog)
- The tutorial route supplies a shared spritesheet, map and font to every follower — [freeCodeCamp course listing](https://classcentral.com/course/freecodecamp-build-a-dev-portfolio-as-a-2d-game-javascript-course-288285) (search summary)

### Inferences
All **Observation**:
- An "authored" checklist that falls out of these cases: (1) a self-avatar drawn in the same hand as everything else; (2) a signature accent colour that appears on the avatar and on every interactive object and nowhere else; (3) one light direction and one shadow shape used on every asset; (4) three to five recurring motifs tied to the developer's real career (a specific keyboard, mug, pet, framework logos reinterpreted as in-world objects); (5) in-world UI (dialog boxes, signs, menus drawn with the same palette and pixel font); (6) a named, limited set of influences rather than "generic RPG".
- Era maps can change mood through per-map tint or palette remap while the avatar, accent colour, outline value and UI stay constant. That is the "change mood without changing identity" principle and it is nearly free at runtime.
- The famous examples each have one sentence that describes them ("the toy car on orange", "the Mario résumé", "the ramen shop"). Pixelfolio needs an equivalent that is not "a pixel RPG portfolio", since that sentence already describes a tutorial and two templates.
- AI-assisted assets are where generic-ness will leak in. Routing every asset through the locked palette, a fixed outline rule and a hand pass in Aseprite is what makes them read as one author's work.
- World feedback (objects that change after being visited, a pet that reacts) was called out in the pixel portfolio write-ups and costs little art; it signals authorship through behaviour rather than through more drawing.

### Gaps
- No art director or designer source was found that speaks specifically about personal-brand games; the brand-system quotes are about large franchises, and the personal cases are developer self-reports and press reactions.
- No data links any specific style choice to outcomes (traffic, job offers); Bruno Simon's 400,000 visits are attributed to the concept as a whole.
- The Thumbsticks/gamescom brand-system quotes were not read in the original article.
- No source explicitly names "signature colour" or "consistent light" as rules for personal games; those are inferred from Bruno Simon's, Bloodless's and Shovel Knight's documented choices.
