# How shipped pixel-art games implement and art-direct lighting

Researched 2026-11-14. Every bullet under "Cited Findings" comes from the linked page as read in this session. Anything marked **(inference)** is my reasoning, not a developer statement. Where a page could not be opened and only a search excerpt was seen, the bullet says "search excerpt". Developer-authored sources are preferred; critic or wiki sources are labelled.

Our prototype, for comparison: ground-plane light mask over flat pixel art; light pools as concentric flat steps with checker-dithered edges; sprite-shaped shadows; dark blue ambient for dusk; every lit pixel snapped to a 64-colour palette.

---

## 1. Graveyard Keeper (Lazy Bear Games, Unity, top-down, day/night) — best-documented close relative

### Takeaway
Full-colour, smooth lighting stacked from five separate tricks: ambient gradient, artist-made time-of-day LUTs, Unity lights on hand-painted normal maps, a "light is in front of / behind the sprite" shader, and generic rotating shadow sprites. Nothing is palette-snapped or dithered.

### Cited Findings
- Ambient: "Darker at night, lighter in the daytime. The light's color set with a gradient." Night light also gets a blue tint. — [Game Developer, article by the developer](https://www.gamedeveloper.com/programming/graveyard-keeper-how-the-graphics-effects-are-made)
- Time of day is colour-graded with LUTs: the artist made 10 LUTs (night, twilight, evening, …); LUTs also vary by world zone. — [developer's own copy](https://slava.lazybeargames.com/graveyard-keeper-how-the-graphics-effects-are-made)
- Light sources are "the default ones provided by Unity"; intensity of light sprites varies with time of day. — [same](https://slava.lazybeargames.com/graveyard-keeper-how-the-graphics-effects-are-made)
- Every sprite has a normal map. "An artist roughly paints the light on all four sides using a brush", and a script merges the four paintings into a normal map. — [same](https://slava.lazybeargames.com/graveyard-keeper-how-the-graphics-effects-are-made)
- "3D light simulation": a shader compares the light's and the sprite's vertical position; a sprite standing in front of a light is not lit by it, with a fast but smooth falloff ("There is a rate, not just 'not to illuminate'"). — [Game Developer](https://www.gamedeveloper.com/programming/graveyard-keeper-how-the-graphics-effects-are-made)
- Shadows are separate sprites that rotate around a point, up to four per object (sun + three nearest dynamic lights), drawn from about ten generic shadow shapes (thin, thick, oval…). Rotation runs in a vertex shader. — [Game Developer](https://www.gamedeveloper.com/programming/graveyard-keeper-how-the-graphics-effects-are-made)
- Tried and rejected: skewing the shadow ("it turned out to be unnecessary"); hand-animating wind frames ("not possible considering how much art we have"). Admitted weakness: long objects such as fences get poor shadows. — [Game Developer](https://www.gamedeveloper.com/programming/graveyard-keeper-how-the-graphics-effects-are-made)

### Inferences
- Light falloff is smooth at screen resolution: default Unity lights plus LUT grading give continuous colour; the article never mentions pixel-snapping, dithering, or a palette. **(inference)**
- The shadows are not sprite-silhouette shaped; they are generic blobs chosen per object. **(inference from "ten universal shadow sprites")**

### Gaps
- Blend mode of light onto art is not stated. How LUTs are cross-faded between times of day is not stated.

---

## 2. Stardew Valley (ConcernedApe, XNA/MonoGame, top-down, interiors at night)

### Takeaway
No developer write-up exists; the mechanism is readable in the game's (unofficially decompiled) code. A low-resolution lightmap is filled with a "darkness colour", light textures are drawn into it, and it is bilinearly upscaled and **subtracted** from the finished scene. Sprites are flat; light is smooth.

### Cited Findings
- A separate `lightmap` render target is allocated at a fraction of screen size (`screen / (lightingQuality/2)`), i.e. lower resolution than the picture. — [decompiled Game1.cs, unofficial](https://github.com/veywrn/StardewValley/blob/master/StardewValley/Game1.cs)
- Each frame the lightmap is filled with one colour (`outdoorLight`, the map's `ambientLight`, or a mine colour), then every light source's texture is drawn into it, scaled by radius and tinted by the light's colour. — [same](https://github.com/veywrn/StardewValley/blob/master/StardewValley/Game1.cs)
- The lightmap is drawn over the scene with `SamplerState.LinearClamp` (bilinear smoothing) and a custom blend `lightingBlend` = `ReverseSubtract`, destination ×1, source × source colour. — [same](https://github.com/veywrn/StardewValley/blob/master/StardewValley/Game1.cs)
- Night colour: `outdoorLight = eveningColor * transparency`, where `eveningColor` is (255,255,0) and transparency ramps from 0.3 at "starting to get dark" to a cap of 0.93 when "truly dark". In rain it uses `ambientLight` instead. — [same](https://github.com/veywrn/StardewValley/blob/master/StardewValley/Game1.cs)
- Light sources use a small fixed set of pre-drawn textures (lantern, window light, sconce, cauldron, indoor window light, projector, fish tank). — [decompiled LightSource.cs](https://github.com/veywrn/StardewValley/blob/master/StardewValley/LightSource.cs)
- A `BloomComponent` exists and its threshold is adjusted approaching dusk. — [Game1.cs](https://github.com/veywrn/StardewValley/blob/master/StardewValley/Game1.cs)
- The official modding wiki documents the map property `AmbientLight` as RGB values that the game subtracts from white (example: 95 95 95 for normal indoor daytime), and a separate `AmbientNightLight`. — [Stardew Valley Wiki, Modding:Maps (search excerpt; page blocked direct fetch)](https://stardewvalleywiki.com/Modding:Maps)

### Inferences
- Because the blend subtracts and the night colour is yellow (red+green), night removes red and green and leaves the blue channel untouched. Night is therefore blue, but blue-channel detail and local contrast survive; it is not a multiply by dark blue. **(inference from the blend state and colour values)**
- Lights work by reducing the subtraction locally, so a lit pool returns the art to its own daytime colours rather than adding a new colour on top. **(inference)**
- Light edges are soft gradients, unrelated to the art's pixel grid, since the lightmap is lower resolution and bilinearly filtered. **(inference from sampler state)**
- No normal maps or directional response; characters and furniture are flat under the lightmap. **(inference: nothing in the draw path references normals)**

### Gaps
- No statement from the developer about why this approach was chosen. The decompiled repository is unofficial and reflects an older game version. Character shadows (a small blob sprite, from memory) were not verified in this session.

---

## 3. Eastward (Pixpil, custom MOAI-based engine, top-down, many night interiors)

### Takeaway
Eastward is built as a 3D scene seen from a 2D viewpoint; every asset is rebuilt in 3D and given a hand-painted bump map so engine lights shade it correctly. Colour is softened with a LUT. Detailed internals are not published.

### Cited Findings
- Lead programmer Tommo Zhou: "Interestingly Eastward is a 3D game with a 2D perspective!" — [Game Developer interview](https://www.gamedeveloper.com/art/eastward-s-creators-share-insights-on-making-pixel-art-adventures)
- Assets are rebuilt "in a 3D environment, ready to be hand painted in the bump map one by one" "to ensure they have the correct lighting performance in-game". — [same](https://www.gamedeveloper.com/art/eastward-s-creators-share-insights-on-making-pixel-art-adventures)
- "we use shader textures and lighting systems in our custom engine … to help convey atmosphere"; fog layers and sunlight beams at dawn and dusk. — [same](https://www.gamedeveloper.com/art/eastward-s-creators-share-insights-on-making-pixel-art-adventures)
- The framework supports simulated SSAO, blurry CRT filters and "a LUT texture method that softens colours" (journalist's description, 2016). — [80.lv](https://80.lv/articles/eastward-charming-chinese-pixel-art-adventure)

### Inferences
- Light is smooth and full-colour (SSAO, LUT, light beams are all continuous-tone techniques); no palette constraint. **(inference)**

### Gaps
- No primary source on shadow method, blend modes, or rejected approaches. Forum claims that Eastward does or does not use normal maps contradict each other and are guesses; the developer quote about hand-painted bump maps settles it.

---

## 4. Sea of Stars (Sabotage, Unity, custom render pipeline)

### Takeaway
Fully dynamic lighting with moving time of day and real shadows, achieved by a bespoke pipeline that took one engineer five years and dictated how every asset was made. The technique itself is not published.

### Cited Findings
- "all of the assets that we make have to answer to the technical needs of the dynamic lighting"; Jeakim Hamel was one of the first two people on the project and it was "a full-time job for him for five years straight". — [MobileSyrup interview with Thierry Boulanger](https://mobilesyrup.com/2023/09/11/sea-of-stars-level-design-sabotage-studio-thierry-boulanger-interview/)
- Official feature line: "Full-on dynamic lighting. Our custom-made render pipeline…" — [Sabotage press kit (search excerpt)](https://sabotagestudio.com/presskits/sea-of-stars/)
- Press hands-on: time-of-day system with dynamically rendered shadows; character sprites "also dynamically lit" and reflected in puddles. — [Nintendo Life (search excerpt; page blocked)](https://www.nintendolife.com/news/2020/03/hands_on_first_impressions_of_sea_of_stars_the_next_project_from_the_messenger_dev_sabotage)

### Inferences
- Smooth, full-colour, direction-aware lighting; not palette-held. **(inference from press descriptions and screenshots, not a developer statement)**

### Gaps
- I found no GDC talk or technical article. Whether it uses normal maps, height maps or hidden 3D geometry is undocumented; treat any such claim as unverified.

---

## 5. Celeste (Maddy Makes Games, 320×180, side view)

### Takeaway
Lights are spotlight textures drawn into a mask, cut by wall-shadow quads, then the light's colour is drawn multiplied by the mask. Occlusion comes from level geometry only; sprites are flat.

### Cited Findings
- Screen is 320×180. All lights are packed into one 2048×2048 texture (256×256 cells, one colour channel per light), drawn in one mask pass and one screen pass. — [Noel Berry, "Remaking Celeste's Lighting"](https://noelberry.ca/posts/celeste_lighting)
- Each light is drawn as a spotlight texture, then each wall draws its shadow projection ("just a single quad") on top to cut the light. The shader then draws the light's colour "multiplied by the mask". — [same](https://noelberry.ca/posts/celeste_lighting)
- Rejected: a per-light mesh built by raycasting wall edges, used for over a year, dropped for "a lot of edge cases, bugs, and floating point precision problems" and CPU cost. Plain spotlights with no occlusion were also not acceptable because lights "need to actually hit walls". — [same](https://noelberry.ca/posts/celeste_lighting)

### Inferences
- Light is at the art's resolution (the game renders at 320×180) but uses a gradient spotlight texture, so falloff is smooth in value, not stepped or dithered. **(inference; the post does not state falloff shape)**

### Gaps
- No statement on palette, dithering, or directional sprite lighting.

---

## 6. Animal Well (Billy Basso, custom engine) — the one developer who says smooth light clashes with pixel art

### Takeaway
Basso rejected off-the-shelf engine lighting because smooth point-light gradients clash with pixel art. His answer was not flat stepped pools; it was hand-drawn normal maps, a rim-light shader, posterisation, and thresholding effect colours so they sit with the art.

### Cited Findings
- On Unity-style lighting: "they have point lights and stuff, they have a smooth gradient, and that clashes with pixel art." — [Game Developer](https://www.gamedeveloper.com/design/why-animal-well-s-home-brewed-engine-was-key-to-its-success)
- The rim-light shader made the look: before it the game "looked like an NES game, where the art wasn't that striking"; after, "Everything was now kind of in shadow, but the edges were highlighted." He also added highlights and posterisation over backgrounds and sprites. — [same](https://www.gamedeveloper.com/design/why-animal-well-s-home-brewed-engine-was-key-to-its-success)
- The game "is rendered in many different layers that all get composited together". Background lighting reacts to light direction via normal maps: "I manually draw the normal maps, right alongside the rest of the game's art." — [PlayStation Blog, written by Basso](https://blog.playstation.com/?p=367113)
- Fluid simulation layer for smoke and water: "special care is also taken to threshold the colors to fit in with the rest of the pixel art." — [same](https://blog.playstation.com/?p=367113)

### Inferences
- This is the closest documented precedent for quantising light to suit pixel art, but the quantisation is applied to form (rim light, posterised shading on normal-mapped surfaces), not to a flat ground-plane pool. **(inference)**

### Gaps
- Render resolution of the light buffers, bloom, and final upscale filter are not described in these sources.

---

## 7. Dead Cells (Motion Twin, side view)

### Takeaway
Backgrounds and decorations are drawn as pixel art, then redrawn as normal maps, so a dynamic light can tint and model them while keeping base colours. This also lets one set of art serve several biome moods.

### Cited Findings
- Backgrounds and decorations are done in pixel art and then redrawn as normal maps for use with a dynamic 3D lighting system; a torch next to a statue lights it from the correct side while it keeps its base colours. — [80.lv interview with Motion Twin](https://80.lv/articles/interview-with-the-developers-of-dead-cells)
- This lets the team change a level's mood without redrawing each decor element in a new palette for each biome. — [same](https://80.lv/articles/interview-with-the-developers-of-dead-cells)
- Stated goal: a classic base with "very modern effects". — [same](https://80.lv/articles/interview-with-the-developers-of-dead-cells)

### Gaps
- The artist's own article on the 3D-to-sprite character pipeline could not be opened in this session; my recollection that character frames are exported with normal maps for a toon shader is **unverified**.

---

## 8. Octopath Traveler / HD-2D (Square Enix + Acquire, Unreal Engine)

### Takeaway
Pixel sprites live in a real 3D scene lit by a modern engine (point lights, shadows, depth of field). The team's documented struggle was keeping pixel-art appeal, not keeping light pixel-sized.

### Cited Findings
- Rejected iterations: "At first, they didn't add enough depth to the view, and it was uninteresting." "Another time, they went too far on the resolution and saturation, losing the appeal of pixel art." A hard call was "whether water should be pixel or photoreal". — [Siliconera, summarising a developer interview](https://www.siliconera.com/project-octopath-traveler-developers-answer-project-started-troubles-developing-hd-2d/)
- Sprites "looked lonely and simple in the context of a larger screen"; the fix was more tile variation and colour density. — [same](https://www.siliconera.com/project-octopath-traveler-developers-answer-project-started-troubles-developing-hd-2d/)
- A point light is placed in the scene so that characters and objects cast shadows; point lights were also added at the moment of battle effects. — [Unreal Engine spotlight (search excerpt; page blocked)](https://www.unrealengine.com/en-US/spotlights/octopath-traveler-s-hd-2d-art-style-and-story-make-for-a-jrpg-dream-come-true)

### Gaps
- Could not open the Unreal Engine pages directly (HTTP 403). No source on whether sprites use normal maps.

---

## 9. Children of Morta (Dead Mage, Unity, top-down)

### Takeaway
The team deliberately decoupled light resolution from art resolution: pixel art is scaled about 4× so lighting runs at full HD.

### Cited Findings
- Pixel animations are stretched "about 4 times to fit the full HD screen"; "By doing this, our lighting could have a resolution as high as other normal 2D games." — [TechRaptor interview (search excerpt; page blocked)](https://techraptor.net/content/how-dead-mage-created-the-art-for-children-of-morta)
- "a customized rendering pipeline that helped us integrate some unique lighting techniques with a standard 2D pixel art pipeline"; "advanced lighting techniques, post-process effects". — [Game Developer postmortem](https://gamedeveloper.com/design/postmortem-children-of-morta)

### Gaps
- The Unity interview with the lead programmer that the postmortem points to was not found. Normal maps not confirmed.

---

## 10. Moonlighter (Digital Sun, Unity, top-down, night town)

### Takeaway
No dynamic lighting at all. Night and light are hand-made sprites layered over the scene.

### Cited Findings
- "There is no dynamic lighting"; the team "use the superposition of sprites to give the impression of light", "for example in Rynoka during the night". It is supplemented by "custom shaders, mesh deformations that look like pixel art, camera post-processing". — [80.lv interview](https://80.lv/articles/moonlighter-building-pixel-art-preparing-for-switch/)

### Gaps
- Shadows and palette not discussed.

---

## 11. Katana Zero (Askiisoft, GameMaker)

### Takeaway
A pervasive neon glow is used as an art-direction glue, not as physically placed light.

### Cited Findings
- "I used this big neon lighting effect, and that pretty much covered every single blemish…"; "because everything has this cohesive neon glow, you can't really tell that it's all from different artists." — [MCV/Develop interview with Justin Stander](https://mcvuk.com/business-news/askiisoft-katana-zero/)

### Gaps
- No technical description (blend mode, resolution, normal maps) found.

---

## 12. Signalis (rose-engine, Unity)

### Cited Findings
- Everything is rendered at 640×360 and then upscaled to the output resolution; the game mixes pixel art with rendered 3D. — [Indiegraze interview with a co-developer, 2018 (search excerpt; page returned 404 on fetch)](https://indiegraze.com/?p=989)

### Inferences
- Lighting therefore lives at the art's pixel resolution (same canvas size as ours), but as 3D-rendered continuous shading, not stepped pools. **(inference)**

### Gaps
- No source on dithering, palette, or how light is composited.

---

## 13. Games that deliberately keep light pixel-sized, stepped, dithered or palette-held

### Takeaway
Every documented example is a game whose whole picture is already in very few colours (16 or fewer shades), where the lit ramp is hand-authored per colour. Even there, the developers treat visible rings and dither as problems to manage.

### Cited Findings — Dank Tomb (PICO-8, 16 colours, top-down dungeon)
- Light is "a series of concentric discs centered on the light", each mapped through a darker hand-made palette; six levels including full bright and black. Palette 1 "does nothing, since it represents 'fully-lit'". — [Lighting by Hand, part 1, by the developer](https://www.hackernoon.com/pico-8-lighting-part-1-thin-dark-line-8ea15d21fed7)
- The author disliked the result of plain rings: "the artificial-feeling ringed circle", "all the warmth and hospitality of an office fluorescent light", "When you know what to look for, you can actually count the distinct bands." — [part 3](https://hackernoon.com/lighting-by-hand-3-breath-of-life-7a775617697e)
- Fix: temporal dithering. The band edges are randomly rescaled per frame and per vertical line, giving "a fuzzy, warm glow". Uniform scaling was rejected ("blinking incessantly"). Spatial dithering was rejected because it did not fit his scanline algorithm. A static light was a problem in itself: "if the character stops moving, not a single pixel on the screen will change, making the whole thing feel artificial." — [part 3](https://hackernoon.com/lighting-by-hand-3-breath-of-life-7a775617697e)
- Walls that face away from the light are darkened gradually ("one level darker for every 2 pixels behind"), so vertical surfaces respond to light direction. — [part 3](https://hackernoon.com/lighting-by-hand-3-breath-of-life-7a775617697e)
- Shadows come from wall line segments attached to objects, drawn as black polygons; back faces only, with masks to stop a base shadowing its own top. — [part 4](https://hackernoon.com/lighting-by-hand-4-into-the-shadows-a92bc8bc6d97)

### Cited Findings — Bloodless (Point N' Sheep, 2024, Unity)
- Scenery is lit within seven shades; five accent colours are exempt from lighting; characters stay flat black and white. Dither between shades uses "a classic Bayer pattern". — [Game Developer deep dive by the lead programmer](https://www.gamedeveloper.com/art/deep-dive-behind-the-starkly-stylish-art-direction-of-bloodless)
- Rejected: coloured light through separate RGB channels ("A lot of those ended up looking pretty bad"). — [same](https://www.gamedeveloper.com/art/deep-dive-behind-the-starkly-stylish-art-direction-of-bloodless)

### Cited Findings — Return of the Obra Dinn (1-bit, 3D)
- "the most important part of using dithering was to use it as little as possible." Large dithered pixels were uncomfortable full-screen; "Grid-like Bayer patterns reproduce a range more accurately, and random-like Blue Noise patterns feel more organic." — [PlayStation Blog, written by Lucas Pope](https://blog.playstation.com/archive/2019/10/17/lucas-pope-on-return-of-the-obra-dinns-art-style)

### Cited Findings — Terraria
- The original lighting was per tile (now the "Retro" mode, reproducing the pre-1.1 look). The default "Color" mode computes light on clusters smaller than tiles so that "light transitions more smoothly". — [Terraria Wiki (community wiki)](https://terraria.wiki.gg/wiki/Lighting_mode)

### Inferences
- In palette-held games the lit colours come from a designed ramp per source colour (a lookup table), not from computing a lit RGB value and snapping it to the nearest palette entry. Nearest-colour snapping of a tinted image is not described by any developer here. **(inference)**
- Terraria is a case of a shipped game moving its default from stepped to smooth light and keeping stepped only as a retro option. **(inference from the wiki's description)**

### Gaps
- Loop Hero, Minit: searched; no reliable source on lighting found (Minit is strict black and white with no light layer that I could document). Nothing reliable for Unsighted either.

---

## 14. Games searched with too little reliable material

### Cited Findings
- Hyper Light Drifter: developer interviews cover resolution and influences only (Preston began in HD, found it "ludicrous for one person", moved to low-resolution pixel art). — [Game Developer](https://www.gamedeveloper.com/business/the-ultra-modern-stylings-of-hyper-light-drifter). A critic notes the game's "broad swaths of soft gradient" give depth that dithering could not. — [AV Club (critic, not developer)](https://www.avclub.com/hyper-light-drifter-blended-past-and-present-to-become-1798255620)
- Kingdom: the developer names the water shader and clouds as favourite work and traces the water reflection to a Flixel forum method. — [Game Developer interview](https://www.gamedeveloper.com/audio/dev-interview-thomas-van-den-berg)

### Gaps
- Hyper Light Drifter: no developer description of the light layer. Kingdom: no source on time-of-day colour. Unsighted: nothing technical found. Loop Hero, Minit: nothing on lighting.

---

## 15. Closing comparison

### Takeaway
Among games with a normal full-colour pixel-art look, the documented norm is: smooth light that freely makes new colours, time of day done by colour grading rather than one flat tint, and some form of directional response on sprites. Stepped, dithered, palette-held light is documented only in games whose entire art is 16 colours or fewer, and their developers still fight the ringed look.

### Near-universal choices (each supported above)
- **Light is not held to a palette.** Graveyard Keeper (LUTs + Unity lights), Stardew (bilinear subtractive lightmap), Dead Cells, Eastward, Octopath, Children of Morta, Sea of Stars all let lighting create colours outside the art's palette. **(inference across the cited findings)**
- **Falloff is smooth, and often at higher resolution than the art.** Children of Morta upscales art 4× specifically for this; Stardew filters a low-res lightmap; Terraria moved its default from per-tile to smooth.
- **Darkness is colour-graded, not a single multiply.** Graveyard Keeper uses ten artist LUTs plus an ambient gradient; Stardew subtracts a yellow so the blue channel and its contrast survive.
- **When light is dynamic, surfaces respond to direction.** Hand-painted normal or bump maps (Graveyard Keeper, Eastward, Dead Cells, Animal Well backgrounds) or a rim light (Animal Well). Games that keep sprites flat (Stardew, Celeste, Moonlighter) keep the light layer soft and subordinate, or paint the light by hand.
- **Shadows are cheap and generic.** Graveyard Keeper rotates about ten stock shadow shapes and dropped skewing; Celeste and Dank Tomb cast shadows from level geometry only, not from sprites.
- **A lit area returns the art to its own colours.** Stardew's lights cancel the darkness; Dank Tomb's brightest palette is the identity; Dead Cells stresses that normal-mapped light keeps base colours. **(inference)**

### Our choices that no documented game makes
- **Snapping every lit pixel to a fixed palette in a full-colour game.** Not found anywhere. Palette-held light appears only as hand-authored per-colour ramps in 16-colour-or-fewer games (Dank Tomb, Bloodless).
- **Static concentric flat steps as the finished look.** Only Dank Tomb starts there, and its developer called it artificial and "office fluorescent", then broke the rings up with per-frame jitter.
- **Checker-dithered step edges on a ground light.** Not found. Bloodless uses Bayer dither inside a seven-shade world; Obra Dinn's author advises using dither as little as possible.
- **Sprite-silhouette shadows.** Not found in this set; the closest relative (Graveyard Keeper) uses stock shapes and found skew unnecessary.
- **A flat dark blue ambient.** The two documented top-down night games grade instead (LUTs; subtractive yellow). **(inference that ours is a flat tint)**
- **Not unique:** flat sprites under a light mask is what Stardew and Celeste do; in both it is paired with soft, low-contrast light.

### Gaps
- Sample bias: developers who use modern smooth lighting write about it more; quiet palette-strict games may be under-represented.
- Several pages were blocked (Unreal Engine, TechRaptor, Nintendo Life, Stardew wiki, Indiegraze); those bullets rest on search excerpts and are labelled.
