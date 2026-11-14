# Pixel art lighting: craft rules and why computed light looks "off"

Research date: 2026-11-14. Scope: craft rules pixel artists follow for light and shadow, and documented failure modes of computed light on pixel art, read against our test (640×360, 64 px outlined characters, ENDESGA 32 art with upper-left daylight baked in, scripted relight with concentric flat steps, checker-dithered edges, sprite-shaped cast shadows, dark blue ambient, hue turned to the light colour, snap to 64 colours).

How to read the labels:
- **[read]** = I fetched the page and the claim is paraphrased from its text.
- **[snippet]** = the claim comes from a search-result summary only; the page itself refused the fetch (HTTP 403/404) or was not opened. Treat as weaker.
- Everything under "Inferences" is mine, not the source's.
- Claims are paraphrased, not quoted, unless in quotation marks.

Sources I could not read, so nothing below rests on them directly: Pedro Medeiros' Medium articles (403; his own site hosts the tutorials as GIFs with no text), Michael Azzi's *Pixel Logic* (paid book; reached only through a thesis that cites it), AdamCYounis and MortMort videos (no transcripts found), pixelation.org threads, Lucas Pope's TIGSource devlog (403), gamedev.net and ModDB threads (403).

---

## 1. How do pixel artists show a light source at night or dusk (contrast, shadow colour, hue shift, steps, glowing source)?

### Takeaway
The sources agree on three things: value and saturation are designed per ramp (not derived by darkening), shadows shift hue and keep their saturation, and night is produced by an authored colour mapping plus a few light sources that are themselves tinted and dimmed. I found no primary pixel-art source that spells out a recipe for a glowing lamp at night; that part is a gap.

### Cited Findings
- A ramp is built with a hue shift between every step; one working example uses 9 swatches per ramp with 20° of hue shift per swatch, which the author calls about the most he uses. [read] — [Slynyrd, Pixelblog 1: Color Palettes](https://www.slynyrd.com/blog/2018/1/10/pixelblog-1-color-palettes)
- Shifting hue in the positive direction makes colours warm as they brighten, which the author finds more natural; the direction can be reversed. [read] — [Slynyrd, Pixelblog 1](https://www.slynyrd.com/blog/2018/1/10/pixelblog-1-color-palettes)
- Across a ramp, saturation peaks near the middle and never reaches 0 or 100; it must drop at the bright end to avoid eye-burning colour; darker colours generally carry more saturation, but very dark and very saturated colours get heavy. Brightness rarely starts at 0. [read] — [Slynyrd, Pixelblog 1](https://www.slynyrd.com/blog/2018/1/10/pixelblog-1-color-palettes)
- Ramps with no hue shift lack interest and are hard to harmonise with ramps of other hues. [read] — [Slynyrd, Pixelblog 1](https://www.slynyrd.com/blog/2018/1/10/pixelblog-1-color-palettes)
- Hue-shifting adds subtle colour contrast inside a ramp; straight ramps are dull. A palette should span a wide range of values, and too little contrast is a common beginner fault. [read] — [Pixel Joint tutorial by cure](https://pixeljoint.com/forum/forum_posts.asp?TID=11299)
- For shadows: darker, with saturation kept or raised for depth; lowering saturation looks muddy; under warm light the shadows lean blue. Number of shadow stages scales with canvas size: 2 at 16×16, 3 at 32×32, 4 to 5 at 64×64 and above. [read; publisher is a pixel-art tool site with no named author, so mid-weight] — [Pixnote, Shading & Lighting](https://pixnote.net/en/learn/shading)
- The same page reports a measurement on its own sample set: between adjacent ramp steps lightness drops by a median of about 16.5 HSL points, saturation is left almost alone, and hue moves 8° or more in only 2% of pairs; hue shift pays off once a ramp has three or more steps. [read; method not shown, treat as indicative] — [Pixnote](https://pixnote.net/en/learn/shading)
- Light is one of the biggest factors in mood; a light source should be fixed at the very start, usually from above; a simple approach works best; pixel art tends to look flat when light is not handled with care. [read] — [Slynyrd, Pixelblog 6: Light and Shadow](https://www.slynyrd.com/blog/2018/6/15/pixelblog-6-light-and-shadow)
- In a shipped pixel-art game, time of day is done with a colour lookup table that the artist paints: the artist is handed a screenshot and asked to make it look like evening, and ten such tables cover the day. Ambient light is dimmer at night with its colour set by a gradient, and by nightfall each light source itself becomes darker and bluer. [read] — [Graveyard Keeper: how the graphics effects are made](https://www.gamedeveloper.com/programming/graveyard-keeper-how-the-graphics-effects-are-made)
- Pedro Medeiros' shading article covers the terminator, highlights, rim light and bounce light, and recommends sharp transitions in pixel art to avoid banding. [snippet] — [Pixel Grimoire, How to start making pixel art #4](https://medium.com/pixel-grimoire/how-to-start-making-pixel-art-4-f57f51dcfa02)
- A Pixel Joint thread states that on a neutral surface, shadows tend towards the complement of the light's colour. [snippet] — [Pixel Joint thread](https://pixeljoint.com/forum/printer_friendly_posts.asp?TID=11423)

### Inferences
- Our "hue turned towards the light colour" is in line with the ramp rule (lit colours warm under a warm lamp), but the rule is two-sided: the unlit side should move the other way (cooler, and not less saturated). A single hue turn applied only where light falls gives half of the relationship.
- 20° per step is described as an upper bound by one artist and the Pixnote measurement suggests real ramps often shift much less. A strong global hue turn can therefore overshoot what a hand-made ramp would do.
- With 64 px characters, the Pixnote scale suggests 4 to 5 value stages on a form; a light layer that adds several more stages on top of the baked ones puts more steps on a character than the art style has anywhere else.
- Where value contrast goes at night: none of the sources I could read states it outright. The Graveyard Keeper approach implies the answer is "wherever the artist put it in the lookup table", i.e. it is authored, not computed.

### Gaps
- No primary source read on how to draw the lamp itself glowing (halo size, number of halo steps, whether the fixture goes to near-white). Medeiros' "Illumination Techniques", "Shine" and "Darkness" tutorials exist as GIFs at [saint11.art](https://saint11.art/blog/pixel-art-tutorials/) but carry no extractable text; they should be looked at by eye.
- No readable AdamCYounis or MortMort material.

---

## 2. Banding and concentric rings; when is dithering advised, and when does it read as dated or noisy?

### Takeaway
Bands of colour that run parallel and follow each other's shape are the textbook fault in pixel art (banding; in its strongest form, pillow-shading), because the eye locks onto the lines between colours and the form goes flat. Dithering is advised only as a narrow taper between two low-contrast colours; as a field it becomes texture and noise, and several sources call it rarely needed on modern displays.

### Cited Findings
- Banding in its simplest description is pixels lining up; it reveals the grid. Variants include an outline and its inner shape lining up ("hugging"), fat pixels and staircase bands, and "skip-one" banding where a gap between two bands does not help because the mind fills it in. [read] — [Pixel Joint tutorial by cure](https://pixeljoint.com/forum/forum_posts.asp?TID=11299)
- Banding makes the eye attend to the lines where colours meet instead of the colours. [read] — [Derek Yu, Pixel Art Tutorial](https://www.derekyu.com/makegames/pixelart.html)
- Pillow-shading is wrong because it ignores the light source and follows flat shapes instead of how three-dimensional form is lit. [read] — [Pixel Joint tutorial by cure](https://pixeljoint.com/forum/forum_posts.asp?TID=11299)
- A 2025 TU Delft bachelor thesis (Rares Bites, "Pixel Fixer"), whose banding heuristic and examples are taken from Azzi's *Pixel Logic*, defines pillow-shading as shading organised in concentric colour layers that follow the outline almost perfectly; it causes banding across nearly all segments and makes objects look flat by suppressing volume. Its fix is to break the concentric layers and re-place them according to a light direction. [read, PDF text extracted] — [TU Delft repository](https://repository.tudelft.nl/file/File_65d43acd-9779-4eab-999b-9bcd4f0a96a9)
- The same thesis: banding in pixel art is not a shortage of colours (as in photographs) but a spatial alignment problem, so dithering offers little benefit for correcting it. [read] — [TU Delft repository](https://repository.tudelft.nl/file/File_65d43acd-9779-4eab-999b-9bcd4f0a96a9)
- Dithering is for easing a transition between two colours without adding one. It works when it tapers the ends and edges of a solid field. With too much, the dithered area becomes a field of its own; if it adds texture instead of buffering, it is not working. The lower the contrast between the two colours (hue or value), the less harsh it is. If dithering covers half a sprite, add a colour instead. [read] — [Pixel Joint tutorial by cure](https://pixeljoint.com/forum/forum_posts.asp?TID=11299)
- Derek Yu uses dithering sparingly, a little for texture. [read] — [Derek Yu](https://www.derekyu.com/makegames/pixelart.html)
- Pixel Parmesan: dithering is rarely if ever necessary in modern contexts; patterns were less visible on CRTs than on modern displays, so it no longer has the same effect; extra dithering creates visual noise or an unwanted illusion of texture; it is not recommended for most character sprites, especially animated ones; the higher the contrast between the two colours, the more dither steps (and the more resolution) are needed; the first alternative is to add in-between colours; "dithering adds texture" is called a cliché. [read; author not named on the page] — [Pixel Parmesan, Dithering for Pixel Artists](https://pixelparmesan.com/dithering-for-pixel-artists)
- A practical test from a general guide: view at display size, and if the dithered area looks like static, it is over-dithered. [snippet; vendor blog, low weight] — [Divoom blog](https://divoom.com/blogs/setup-ideas/pixel-art-dithering-when-to-use-and-stop)

### Inferences
- Our light pools are, structurally, pillow-shading applied to the floor: concentric flat steps where every ring follows the shape of the next. On a flat floor this is physically defensible (falloff really is radial), but the eye reads the parallel ring edges the way it reads banding: it sees the contour lines, and the pool flattens into a painted target.
- "Skip-one" banding predicts that putting a checker-dither strip between two rings does not remove the ring; the mind still joins the bands. The dither strip also becomes a ring of its own, so the number of visible concentric contours roughly doubles.
- Our rings span a large value jump (night ambient to lamp-lit) in few steps, so adjacent rings are high-contrast pairs. The sources say checker dither is harshest exactly there and needs more steps and more resolution than 640×360 offers. On a modern screen at integer upscale each checker cell is several physical pixels wide, so it reads as a mesh texture laid on the floor, not as a blend.
- What the sources point to instead: fewer steps (two or three), step edges that do not run parallel to each other (vary the ring shapes: offset centres, elongate with perspective, let furniture and walls cut them), lower contrast between neighbouring steps by putting real in-between colours in the palette, and dither reserved, if used at all, for the single outermost edge.

### Gaps
- No source addresses radial light pools on floors by name; the link from pillow-shading and banding to ring-shaped light is my inference.
- Could not read *Pixel Logic* itself or the Pixel Joint/pixelation "ramblethread" on clusters and banding.

---

## 3. Form: how should objects under a light be shaded, and what happens when baked shading meets a light from another direction?

### Takeaway
Artists pick one light direction per scene and shade form (lit side, shadow side, rim and bounce light) against it; mixed directions are named as a source of visual dissonance. Games that add dynamic light to pixel art do not treat sprites as flat: they add normal maps, front/behind logic, or a rim-light pass, and keep hand-painted shading as the base.

### Cited Findings
- Keep the light direction consistent within a work or a game scene; mismatched light sources on characters, backgrounds and items create visual dissonance. Shadows concentrate opposite the light. [read] — [Pixnote, Shading & Lighting](https://pixnote.net/en/learn/shading)
- Shading is sculpting a form, not adding colour; check by desaturating the art to see whether the shading still reads. Derek Yu's example assumes one light above and slightly in front. [read] — [Derek Yu](https://www.derekyu.com/makegames/pixelart.html)
- Selective outlining: replace much of the black outline with lighter colours, and use dark shadow colours instead of pure black, so the outline responds to the light. [read] — [Derek Yu](https://www.derekyu.com/makegames/pixelart.html)
- For top-down style sprites, critique on Pixel Joint recommends a top light: it hits surfaces that face the sky (top of head, shoulders, upper chest, possibly forearms); reflected light fills the rest but less in creases and on down-facing surfaces; body parts may cast small shadows on the body. Side light is discouraged if sprites are mirrored. [read] — [Pixel Joint WIP thread](https://pixeljoint.com/forum/forum_posts.asp?TID=26189)
- Graveyard Keeper gives each sprite a normal map made by the artist roughly painting light from four sides, merged by script; it uses Unity lights on top. It also treats whether a sprite is in front of or behind a light as very important: a shader compares vertical positions and fades the lighting quickly but gradually when the sprite stands between the camera and the light. [read] — [Graveyard Keeper effects article](https://www.gamedeveloper.com/programming/graveyard-keeper-how-the-graphics-effects-are-made)
- A top-down pixel game found its art looked flat even with lights, and added: a shader that finds the outermost pixels of sprites and lights them as a rim, hand-painted shadows on sprites, drop shadows, and normal maps on some pieces. It states that painting shadows directly onto sprites is still the most efficient way to light a 2D game. [read] — [XDasher devlog](https://pixel-beef.itch.io/xdasher/devlog/192949/4-things-we-did-to-add-light-and-depth-to-our-pixel-art-game)
- Elsinore paints every room twice, once fully lit and once in shadow with hints of ambient, and blends between the two paintings using the dynamic shadow map, so the computed light only chooses between two authored states. Characters initially clashed with backdrops and were fixed by lighting them with the same sources. [read; painted 2D, not pixel art] — [Elsinore lighting article](https://gamedeveloper.com/programming/walking-in-a-painting-interior-daytime-lighting-in-elsinore)
- Pixel art used with dynamic light needs a normal map, either made by the artist or estimated. [snippet] — [DynaPix, SIGGRAPH 2022](https://yaksoy.github.io/papers/SIG22b-DynaPix.pdf)

### Inferences
- Our art has upper-left daylight baked in. A lamp to the right of a desk then brightens a desk whose painted highlight is still on its left and whose painted shadow is still on its right: the light says one direction, the form says another. This is the "mismatched light sources" dissonance, and it is probably a large part of "something feels off", because it is felt before it is identified.
- Because the relight has no notion of form, the lit result is the flat art multiplied by a pool: objects under the lamp get brighter all over instead of gaining a lit side and a shadow side. The sources that ship this (Graveyard Keeper, XDasher) all add at least one form cue.
- Cheapest form cues in the order the sources suggest: (a) front/behind fade by y-position, so things standing between camera and lamp go dark instead of bright; (b) a 1 px rim on the lamp-facing edge, which for us means lightening the dark outline on that side (selective outlining); (c) hand-painted four-direction light passes for the few hero objects.
- The Elsinore pattern transfers directly: author a night-lit variant of the colours and let the computed mask pick between "day art" and "lit-at-night art", instead of arithmetic on pixels.

### Gaps
- No source discusses re-lighting art that already has a different baked direction and says what viewers perceive; the dissonance claim is from a general consistency rule.

---

## 4. Cast shadows in top-down three-quarter view: shape, softness, colour, contact

### Takeaway
Shipping games keep cast shadows simple, hard-edged and few: reusable blob-like shadow sprites anchored at the object's base, rotated away from the nearest lights, unfiltered to match the pixel grid. Shadows of one movable object falling on another, and shadows of long thin objects, are documented as looking wrong.

### Cited Findings
- Graveyard Keeper: shadows are sprites rotating around a point at the base; each object gets at most four (sun plus the three nearest lights); about ten reusable shadow sprites cover most objects, with some drawn per object; the source sprite is roughly a circle, heavily squashed vertically; skewing was tried and dropped as unnecessary; all shadows are black with strength stored in a channel; elongated objects such as fences do not look right. [read] — [Graveyard Keeper effects article](https://www.gamedeveloper.com/programming/graveyard-keeper-how-the-graphics-effects-are-made)
- A top-down Godot tutorial keeps the shadow filter off, because smooth shadows do not suit a low-resolution pixel style; it declares the light high enough to shine over movable objects, since objects shadowing each other does not look good; it reports phantom shadows when objects sit on non-integer coordinates and fixes them by rounding positions. [read] — [Catlike Coding, True Top-Down 2D: Light and Shadow](https://catlikecoding.com/godot/true-top-down-2d/4-light-and-shadow/)
- Clear atmosphere gives hard, crisp, dark cast shadows; haze or cloud makes them soft and less defined; shadows can be stylised for expression. [read] — [Slynyrd, Pixelblog 6](https://www.slynyrd.com/blog/2018/6/15/pixelblog-6-light-and-shadow)
- Drop shadows under characters are listed as one of four depth fixes for a flat top-down pixel game. [read] — [XDasher devlog](https://pixel-beef.itch.io/xdasher/devlog/192949/4-things-we-did-to-add-light-and-depth-to-our-pixel-art-game)
- A Pixel Joint reply suggests lowering the light so shadows lengthen and placing it to one side so they fall at an angle, for drama. [snippet] — [Pixel Joint thread](https://pixeljoint.com/forum/printer_friendly_posts.asp?TID=16861)

### Inferences
- Our sprite-shaped cast shadows are more literal than what the shipped example uses. A full character silhouette projected on the floor carries the sprite's front-view detail (hair, arms) into a plane where it does not belong in three-quarter view; a squashed ellipse reads as "shadow" with less to get wrong. This supports hard edges and argues against silhouette fidelity.
- Contact: none of the sources separates a contact shadow from a cast shadow, but the base-anchored blob does both jobs. A sprite-shaped shadow that leaves a gap at the feet, or that is the same darkness along its whole length, loses the grounding the blob gives.
- Shadow colour: Graveyard Keeper uses black with variable strength; the palette sources say darks should shift hue and keep saturation. For a palette-snapped game the consistent choice is to map shadowed floor to the next darker colour in that floor's own ramp, not to a blended black.
- Several lamps in an office each throwing a silhouette is the "max four per object" situation; overlap of several sprite-shaped shadows is likely to look busy.

### Gaps
- Nothing found from Slynyrd on top-down scenes specifically, and no pixel-art source on shadow softness steps (penumbra as one extra tone) or on shadows climbing walls.

---

## 5. Night scenes: darkening without mud, ambient colour, readable characters, selective lighting

### Takeaway
The documented way to make night from day art is an authored colour mapping, not a uniform multiply; the documented pitfalls of blend-mode night are light objects popping unnaturally, and saturated or extreme light colours drowning the art. Darks should keep saturation and shift hue.

### Cited Findings
- Graveyard Keeper's night is a set of artist-painted lookup tables, with ambient set by a gradient and light sources themselves dimmed and blue-shifted at night. [read] — [Graveyard Keeper effects article](https://www.gamedeveloper.com/programming/graveyard-keeper-how-the-graphics-effects-are-made)
- Gleaner Heights' developer wanted a truly dark night instead of a blue tint. Additive light cannot darken and overexposes. Overlay made lighter objects unnaturally pronounced at night, worst on white (snow) scenes, which then barely looked like night. Hard light gave a duller, softer result and was chosen. A mid-grey lightmap leaves the image unchanged, and very saturated or very bright or dark light colours can drown the original; light sources should not be too strong or clustered. [read] — [Gleaner Heights devlog](https://gleanerheights.blogspot.com/2017/05/lighting-in-2d-games-shader-glsl.html)
- A Godot top-down tutorial darkens with a multiply by a dark bluish colour (hex 24293b), chosen so the unlit scene stays visible, and exempts the player sprite and its particles from the darkening by giving them unshaded materials; it adds a light that follows the player. [read] — [Catlike Coding](https://catlikecoding.com/godot/true-top-down-2d/4-light-and-shadow/)
- Lowering saturation in shadows looks muddy. [read] — [Pixnote](https://pixnote.net/en/learn/shading)
- Darker ramp colours generally carry more saturation and a shifted hue. [read] — [Slynyrd, Pixelblog 1](https://www.slynyrd.com/blog/2018/1/10/pixelblog-1-color-palettes)
- One developer reported that a subtract-style darkness layer gave darker colours and more contrast than their earlier look; another found a subtractive system less washed out than a multiplicative one but touchier in dark areas. [snippet] — [ModDB devlog](https://www.moddb.com/news/lighting-break-it-down-now), [Sidescroller Lighting](https://expiredpopsicle.com/articles/2010-10-15-Sidescroller_Lighting/2010-10-15-Sidescroller_Lighting.html)

### Inferences
- Multiplying by dark blue is the standard quick method (Catlike uses it), so it is not wrong in itself, but it does three things the palette rules warn against: it scales every channel so warm colours lose red and green and go grey-blue (mud), it compresses all values so the art's own contrast collapses, and it moves every hue the same way instead of along each material's ramp.
- Snapping the multiplied result to the nearest of 64 colours then picks whatever palette entry happens to be closest to that mud; different materials fall onto the same few dark blues, so the room's local colour disappears at night.
- A lookup table per time of day is the same idea as our palette snap, done on purpose: for each of the 32 art colours an artist chooses its dusk colour, its night colour and its lamp-lit colour. That keeps saturation, lets each ramp shift its own way, and guarantees every output is a palette colour without a nearest-colour search.
- Character readability: the Catlike exemption (player unshaded) and the selective-outline rule suggest keeping characters a step lighter than the room and never letting the outline and the floor land on the same dark colour.
- The Gleaner Heights "light objects pop" problem applies to our white desks, paper and screens: at night they should be held down or they read as daylight leaking through.

### Gaps
- No pixel-art tutorial read that is specifically about painting night interiors; gamedev.net thread on turning daylight assets into night could not be opened.

---

## 6. Light on walls versus floors, light shapes, and what makes a pool read as light instead of a painted disc

### Takeaway
I found little that addresses this directly. What exists says: light must respect whether a surface is in front of, behind or beside the source, interiors need a second soft source so lit patches do not sit on a dead-flat dark, and light should be matched to the low resolution of the art.

### Cited Findings
- Graveyard Keeper treats the vertical relation between sprite and light as essential: things behind the light are lit, things in front of it darken progressively. [read] — [Graveyard Keeper effects article](https://www.gamedeveloper.com/programming/graveyard-keeper-how-the-graphics-effects-are-made)
- Elsinore: real sunlit interiors are lit diffusely, so beside the window sun they add a second, low-intensity light from above to suggest soft overlapping shadows near floors and walls; rooms with no window in the sun's path lose depth; where light is always blocked, the lit and shadow paintings are identical. [read] — [Elsinore lighting article](https://gamedeveloper.com/programming/walking-in-a-painting-interior-daytime-lighting-in-elsinore)
- XDasher masks spotlights with cookie textures so the light has a shape and breaks across the scene. [read] — [XDasher devlog](https://pixel-beef.itch.io/xdasher/devlog/192949/4-things-we-did-to-add-light-and-depth-to-our-pixel-art-game)
- Light is hard in clear air and soft in haze; pick by context. [read] — [Slynyrd, Pixelblog 6](https://www.slynyrd.com/blog/2018/6/15/pixelblog-6-light-and-shadow)

### Inferences
- A pool reads as a painted disc when nothing interrupts it. Signals that it is light: objects inside it cast shadows away from the centre, objects cut its outline, it changes shape where floor meets wall (a ceiling lamp makes an ellipse on the floor and a scallop or cone on the wall, not one continuous ring across both), and lit surfaces change along their own ramps so different materials respond differently.
- Concentric rings drawn across the floor/wall seam as one shape tell the eye the picture is flat; breaking the shape at the seam is the cheapest depth cue available.
- The source being visibly the brightest thing, with the pool dimmer than the fixture, is standard painting practice but I have no pixel-art source for it here.

### Gaps
- No source found on window patches, cones versus pools, or wall scallops in pixel art. This question is mostly unanswered by the literature I could reach; visual study of reference games is needed.

---

## 7. Computed light on pixel art: known failure modes and recommended fixes

### Takeaway
The well-documented failures are grid mismatch (light computed at a finer grid than the art), smooth light over hard-edged art, posterising after the fact, and light that ignores form. The recommended fixes are: compute light on the art's own pixel grid, turn off filtering, quantise the light input (not the output), give sprites normals or at least a rim, and prefer authored colour mappings over arithmetic.

### Cited Findings
- Resolution mismatch: normal-mapped light on pixel art comes out as smooth gradients that do not follow the pixel grid. Fixes reported: turn off texture filtering on the normal map; render at low resolution and upscale (the poster judged this not a full solution for many independent objects); aligning the light itself to the texture grid remained unsolved in that thread. [read] — [Godot forum, pixel-perfect 2D normal map shading](https://forum.godotengine.org/t/pixel-perfect-2d-normal-map-shading-now-with-working-images/7967)
- Same problem with cel-shaded normal-map light: suggested fixes are nearest filtering on every sampled texture and snapping UVs to the sprite's pixel grid before sampling. The thread does not confirm the fix. [read] — [Godot forum, pixel perfect cell shading](https://forum.godotengine.org/t/pixel-perfect-cell-shading-with-normal-maps/103199)
- Posterising after per-fragment lighting produces jagged patches that break up the pixel grid. Working fix: move the position used for lighting to the centre of the nearest texel so that falloff, shadows and reflectance all snap to the art's grid; simpler variant: quantise world position to a fixed grid when texel density is uniform and surfaces are axis-aligned. [read] — [Unity Discussions, The Quest for Efficient Per-Texel Lighting](https://discussions.unity.com/t/the-quest-for-efficient-per-texel-lighting/700574)
- Smooth lights and straight shadow edges look out of place on pixelated scenes; developers ask for a way to pixelate only the light pass. Rendering the whole scene to a low-resolution target made movement look jerky for one developer. [snippet] — [Unity Discussions thread](https://discussions.unity.com/t/add-a-postprocess-effect-on-just-the-2d-lighting/927683)
- Posterising to a fixed palette is suggested by one commenter as a help when pixel lighting is too smooth. [snippet] — [itch.io post](https://itch.io/post/12032716)
- Snapping lit colours so they move to the nearest darker or lighter variant of a set is suggested as the technique to look for ("colour stepping", "palette reducer"). [snippet] — [Unreal forum thread](https://forums.unrealengine.com/t/flat-colour-shading-for-foliage/1551167)
- Light ignoring form: addressed with artist-made four-direction normal maps and front/behind fading (Graveyard Keeper), a rim-light shader plus hand-painted shadows (XDasher), or authored lit and shadow versions blended by the shadow mask (Elsinore). [read] — [Graveyard Keeper](https://www.gamedeveloper.com/programming/graveyard-keeper-how-the-graphics-effects-are-made), [XDasher](https://pixel-beef.itch.io/xdasher/devlog/192949/4-things-we-did-to-add-light-and-depth-to-our-pixel-art-game), [Elsinore](https://gamedeveloper.com/programming/walking-in-a-painting-interior-daytime-lighting-in-elsinore)
- Dither crawl: in Return of the Obra Dinn, screen-fixed dither "swims" and flickers when the view moves and becomes uncomfortable at full screen; the fix was to make the dither pattern move with the scene and to tone down flickering dots; aliasing still causes some swimming. [snippet; the devlog itself returned 403] — [Lucas Pope devlog, TIGSource](https://forums.tigsource.com/index.php?topic=40832.msg1363742#msg1363742)
- Phantom shadows appear when occluders sit on non-integer positions; rounding positions fixes it. [read] — [Catlike Coding](https://catlikecoding.com/godot/true-top-down-2d/4-light-and-shadow/)

### Inferences
- Resolution mismatch probably does not apply to us if the relight is computed on the 640×360 canvas; that choice is supported by every thread above. It would apply the moment light is drawn at display resolution over upscaled art.
- Palette snapping is our version of "posterise after lighting". The Unity thread's lesson generalises: quantising the output of a continuous computation puts step edges wherever the arithmetic crosses a threshold, and those places differ per underlying colour. A ring edge will sit at a different radius on carpet than on desk, and a single material can flip between two palette entries along a noisy line. Quantising the input instead (decide the light level per pixel as an integer step first, then look up each art colour's entry for that step) keeps edges where the artist-style shapes are.
- Uniform multiply then nearest-colour is also where hue goes wrong: nearest in RGB is not nearest in the ramp, so a lit orange can snap to a pink or a yellow from another ramp. A per-colour ramp table removes this.
- Dither crawl: our checker is fixed to the canvas grid. A static lamp is safe. Anything that moves a dithered edge (a flickering lamp, a carried light, a shadow edge following a walking character) will make the checker boil along the edge, and a scrolling camera will make world-anchored and screen-anchored checkers disagree. Keep dither out of anything that moves, or anchor it to world pixels.
- Light ignoring form is the one failure in the list that our test has in full: nothing in the relight knows a desk has a top and a side.

### Gaps
- No source found that discusses nearest-palette snapping artefacts of lit pixel art by name; the reasoning above is extrapolated from the posterise-after-lighting thread.
- Mixels as a term did not surface in any readable source in this pass.
- Lucas Pope's own text not read; only a search summary.

---

## Summary against our choices (all inference, built on the findings above)

| Our choice | Verdict from the sources | Main sources |
|---|---|---|
| Light pools as concentric flat steps | Speaks against: parallel bands that follow each other are banding/pillow-shading and flatten | cure (Pixel Joint), TU Delft thesis citing *Pixel Logic*, Derek Yu |
| Checker-dithered step edges | Speaks against at this contrast and resolution: becomes texture and extra rings; rarely needed on modern displays; risk of crawl if anything moves | cure, Pixel Parmesan, Obra Dinn (snippet) |
| Sprite-shaped cast shadows | Mixed: hard edges supported; literal silhouettes and many overlapping shadows not what shipped games do (blobs, max four, no object-on-object) | Graveyard Keeper, Catlike Coding |
| Dark blue ambient (multiply) | Common, but causes mud, value collapse and uniform hue move; authored lookup table is the documented better route | Graveyard Keeper, Pixnote, Slynyrd, Gleaner Heights |
| Hue turned to light colour | Supported in direction (lit side warms), but should be per ramp and paired with cooler, still-saturated darks; keep the amount modest | Slynyrd Pixelblog 1, Pixnote |
| Snap every lit pixel to 64 colours | Goal supported (stay on palette, on grid); method (quantise after arithmetic) is the documented source of patchy edges; use per-colour ramp lookup | Unity per-texel thread, Unreal snippet, Graveyard Keeper LUT |
| Relighting art with upper-left daylight baked in, with no form information | Speaks against: mismatched light directions cause dissonance; shipped games add normals, front/behind fade or rim | Pixnote, Graveyard Keeper, XDasher, Elsinore |
