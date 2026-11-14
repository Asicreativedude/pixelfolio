# Art styles of distinctive top-down / three-quarter pixel art games (and close relatives)

Reading notes for the report writer:

- Research date: November 2026.
- "Observation" = my own description from looking at the games, not taken from a source. Treat as unverified art-direction notes.
- "Snippet" = the claim came from a search-result summary of the linked page; the page itself was not opened (or returned 403/404). Lower confidence.
- Developer statements are paraphrased, not quoted (one short quote only in the whole file). Follow the link for exact wording.
- Developer and year lines are standard credits (consistent with Wikipedia) and were not individually re-verified in this pass.
- Sprite pixel sizes are poorly documented by developers. Most sprite-height figures below are observations or come from modding communities.

## For each game, what are the three or four choices that make its look instantly recognisable?

### Takeaway
Each recognisable game commits to one dominant constraint (a tiny canvas, a restricted palette, one lighting system, or one proportion rule) and applies it everywhere, then breaks period-accurate rules only where it buys readability or atmosphere. Very few developers document sprite sizes; canvas resolution is documented for roughly a third of the list.

### Cited Findings

#### Action-adventure and RPG, top-down or three-quarter

**Hyper Light Drifter** (Heart Machine, 2016)
- Canvas: Alx Preston described the pixel art as 480p and deliberately low resolution; in his words, "it is pixel style, so why would we make it 1080p?" — [GamingBolt, Nov 2014](https://gamingbolt.com/our-game-is-480p-yeah-its-low-resolution-and-very-intentionally-so). An earlier interview has him refer to working within a 240p area — [Game Developer](https://gamedeveloper.com/business/the-ultra-modern-stylings-of-hyper-light-drifter). The two figures conflict; the 480x270 figure often repeated by fans was not confirmed by any source found.
- Preston first planned an HD illustrated look, dropped it as unworkable for one person, and moved to pixel art; he said he did not want boring or ugly pixel art and had to put his own personal style into it — [Game Developer](https://gamedeveloper.com/business/the-ultra-modern-stylings-of-hyper-light-drifter).
- Preston says colour and silhouette are what he cares about most, that readability at low resolution was the top priority (the player must never lose their character), and that the dense dark palette supports an unreal, dreamlike feel — [Automaton (JP interview, 2017)](https://automaton-media.com/articles/interviewsjp/20170525-47328/).
- Soft gradients are used for depth and colour shifts instead of dithering, with pastel colour against hard pixel edges, rich blues and greens, recurring glowing red accents, and two-tone light/shadow splits — [The A.V. Club (Nick Wanserski)](https://avclub.com/hyper-light-drifter-blended-past-and-present-to-become-1798255620).
- Influences named by Preston: A Link to the Past (simple but elegant), Miyazaki films, older anime, Sword & Sworcery, Fez, Super Time Force, Paul Robertson — [Game Developer](https://gamedeveloper.com/business/the-ultra-modern-stylings-of-hyper-light-drifter).
- CrossCode's Felix Klein characterises HLD's base sprites as minimalist, few-colour and not really 16-bit — [Game Developer](https://gamedeveloper.com/design/designing-i-crosscode-i-to-stand-out-in-the-retro-rpg-market).
- Observation: no outlines on characters or tiles; shapes are flat colour blocks separated by value and hue. Signature accent pair is hot magenta/pink against cyan/teal over desaturated mid-tones. Characters are small, caped, faceless silhouettes; environments are large geometric slabs with very little texture noise, plus smooth (non-pixel) gradient and glow overlays. Recognisable in four choices: no outlines, flat shapes, neon accent pair, smooth gradient light over hard pixels.

**Eastward** (Pixpil, published by Chucklefish, 2021)
- The game is 3D under the hood with a 2D view. Hong Moran draws assets in Aseprite; assets are split into parts by physical structure (roof, wall), rebuilt in a 3D scene, and given hand-painted bump maps so they light correctly. Shaders and lights carry atmosphere, weather and time of day, with fog layers and sunbeams at dawn and dusk — [Game Developer (Tommo Zhou)](https://www.gamedeveloper.com/art/eastward-s-creators-share-insights-on-making-pixel-art-adventures).
- Elevation and layered structures are used to make areas feel dense; the fixed camera forces layouts to be adjusted so the player is not hidden — [Game Developer](https://www.gamedeveloper.com/art/eastward-s-creators-share-insights-on-making-pixel-art-adventures).
- The style came first: Moran had drawn an RPG mock-up and sketches of monsters in a Kowloon Walled City-like setting, and the design was built around that look. The intent was urban decay that still feels full of life — [Nintendo](https://nintendo.com/us/whatsnew/how-the-developers-began-making-then-remaking-eastward).
- Colours are softened with a LUT (colour grading) pass; the engine can simulate ambient occlusion and CRT blur; named influences are Mother 3, Ghibli films and Tekkonkinkreet — [80.lv, 2016](https://80.lv/articles/eastward-charming-chinese-pixel-art-adventure). (80.lv says art was done in Photoshop in 2016; the later Game Developer piece says Aseprite.)
- Other cited inspirations: Dragon Quest, EarthBound, Zelda — [Game Developer](https://www.gamedeveloper.com/art/eastward-s-creators-share-insights-on-making-pixel-art-adventures).
- Observation: characters are flat-shaded with thin dark outlines and roughly 3-heads-tall cartoon proportions; environments are far more rendered (painterly texture, clutter, signage, cables) and mostly outline-free, so characters pop by being simpler than the world. Warm amber interior light against teal shadow is the default grade. Four choices: clutter-dense lived-in props, normal-mapped real-time light on hand pixels, colour-graded warm/teal palette, simple outlined characters on painterly backgrounds.

**Sea of Stars** (Sabotage Studio, 2023)
- Dynamic lighting was the starting idea in 2018; one developer (Jeakim Hamel) worked on it for about five years, and every asset in production has to meet the technical needs of the lighting — [MobileSyrup (Thierry Boulanger)](https://mobilesyrup.com/2023/09/11/sea-of-stars-level-design-sabotage-studio-thierry-boulanger-interview/).
- Sabotage describes a custom render pipeline and full dynamic lighting as key features — [PlayStation Blog](https://blog.playstation.com/?p=366730).
- Light adds coloured highlights to characters and scenery, and time of day can be switched in play; reference points are Chrono Trigger and Super Mario RPG without copying either — [Mega Visions](https://megavisions.net/the-art-of-sea-of-stars-a-sea-of-pixels).
- A hands-on preview describes objects casting real shadows as light moves instead of using palette swaps (snippet; outlet not pinned down, likely [Nintendo Life 2020](https://www.nintendolife.com/news/2020/03/hands_on_first_impressions_of_sea_of_stars_the_next_project_from_the_messenger_dev_sabotage)).
- Level design adds verticality (climbing, jumping, swimming) rather than grid movement — [MobileSyrup](https://mobilesyrup.com/2023/09/11/sea-of-stars-level-design-sabotage-studio-thierry-boulanger-interview/).
- Observation: Chrono Trigger-like proportions (about 3 to 3.5 heads), dark coloured outlines on characters, high colour count, heavily rendered tiles. Four choices: 16-bit JRPG sprite grammar, real-time day/night light with cast shadows, saturated tropical palette, vertical layered terrain.

**Chained Echoes** (Matthias Linda, 2022)
- Asked about the art style, Linda's answer was simply that it is the style he is capable of — [Lords of Gaming](https://lordsofgaming.net/2023/01/interview-chained-echoes-developer-matthias-linda) (snippet).
- In 2018 he said pixel art's vagueness leaves room for the player's imagination, not just nostalgia — [Game Pilgrim](https://gamepilgrim.com/2018/08/27/developer-interview-ark-heiral/) (snippet).
- Named inspirations: Xenogears, Chrono Trigger, Final Fantasy VI, Suikoden II — [RPGFan](https://www.rpgfan.com/feature/interview-with-matthias-linda-on-chained-echoes) (snippet).
- He prioritised work that could be shown as GIFs (animations, the map) — [Game Developer](https://gamedeveloper.com/production/matthias-linda-s-seven-year-quest-to-make-retro-jrpg-chained-echoes).
- Observation: late-SNES/early-PS1 look; small 2.5 to 3 head sprites, dark outlines, no dynamic lighting; richness comes from large hand-drawn set-piece backgrounds and big mech/enemy sprites.

**CrossCode** (Radical Fish Games, 2018)
- Native resolution 568x320 with integer scaling — [PCGamingWiki mirror](https://gamecytus.netlify.app/host-https-www.pcgamingwiki.com/wiki/CrossCode) (snippet). 16x16 tiles per a third-party tutorial — [FreeGameSprites](https://freegamesprites.com/news/tile-size-2d-game-pixel-art-guide) (snippet, secondary).
- Felix Klein: only the pixel art style itself stays true to SNES; the canvas is 16:9 and far larger than SNES, and lighting effects and alpha-blended shadow maps are layered on. Reference games are Seiken Densetsu 3, Terranigma and Chrono Trigger — [Game Developer](https://gamedeveloper.com/design/designing-i-crosscode-i-to-stand-out-in-the-retro-rpg-market).
- Players had depth-perception problems with CrossCode's stacked heights; the studio's next game mixes pixel art with 3D and slight perspective to make terrain read better — [The Avocado interview](https://the-avocado.org/2021/05/07/indie-developer-interview-radical-fish) (snippet).
- Observation: sharp dark outlines on characters and on platform edges, bright saturated colour, clean anime-style sprites about 3 heads tall, strongly stepped cliff faces to show height.

**Stardew Valley** (ConcernedApe / Eric Barone, 2016)
- Map tiles are 16x16; NPC overworld sprites are 16x32; portraits are 64x64 — [Stardew modding wiki](https://stardewmodding.wiki.gg/wiki/So_You_Want_To_Be_a_Map_Modder:_Preparations) and [official forum](https://forums.stardewvalley.net/threads/sprite-size-first-time-modding-sv.7128/latest) (snippets).
- Barone had never done pixel art before and considers the earliest versions poor — [PC Gamer](https://www.pcgamer.com/stardew-valley-interview/) (snippet). He based the natural environment partly on the Pacific Northwest — [NPR, 2025](https://www.npr.org/2025/01/24/g-s1-44510/the-legacy-and-future-of-the-farming-game-stardew-valley) (snippet).
- Observation: 2-heads-tall characters exactly one tile wide and two tall; dark brown (not black) outlines on everything; high-saturation palette that is fully re-keyed per season; chunky, slightly irregular hand-placed pixels; no dynamic lighting beyond a day/night tint and simple light sprites.

**Moonlighter** (Digital Sun, 2018)
- Influences are 16-bit pixel art plus modern indies, specifically Hyper Light Drifter and The Minish Cap; small environmental life details were inspired by Ghibli; made in Aseprite — [80.lv (Javier Giménez)](https://80.lv/articles/moonlighter-building-pixel-art-preparing-for-switch/), [Game World Observer](https://gameworldobserver.com/2019/05/06/1417) (snippet).
- No dynamic lighting: light is faked by layering sprites. Unity is used for shaders, pixel-looking mesh deformation and post-processing. Every weapon or armour needs sprites in four views, which limited content — [80.lv](https://80.lv/articles/moonlighter-building-pixel-art-preparing-for-switch/).
- Observation: soft, rounded, outline-light sprites with high frame counts; pastel palette; closer to HLD's flat shapes than to SNES outlines but cuter.

**Titan Souls** (Acid Nerve, 2015)
- Artist Andrew Gleeson used pixel art because it is his usual medium and the fastest for a jam; inspirations for the game are Shadow of the Colossus and Dark Souls — [GameCloud](https://gamecloud.net.au/features/interviews/titan-souls-developer-interview-with-andrew-gleeson).
- Observation: the entire identity is scale contrast: a hero only about a dozen pixels tall against screen-filling bosses, in empty, muted, naturalistic ruins with minimal outlines.

**Minit** (JW Nijman, Kitty Calis, Jukio Kallio, Dominik Johann, 2018)
- Black-and-white art is listed by Calis as one of the game's founding constraints, alongside the time limit and simple controls; tools were GameMaker, Aseprite and MS Paint — [Game Developer](https://www.gamedeveloper.com/disciplines/road-to-the-igf-calis-nijman-kallio-and-johann-s-i-minit-i-).
- Nijman says the simple art lets the team try a new idea in minutes — [itch.io interview](https://itch.io/blog/34973/a-minute-with-the-minit-devs-what-they-learned-developing-2018s-hottest-zelda-like) (snippet).
- Observation: strictly two colours (no greys, no dithering as shading), very low resolution, thick blobby shapes, characters are white fill with black line, world is black line on white or inverted.

**Superbrothers: Sword & Sworcery EP** (Superbrothers, Capy, Jim Guthrie, 2011; side view)
- Craig Adams calls the style as much an engineering decision as an artistic one, and looked at Wind Waker, Mignola's Hellboy, Cézanne, Klimt, Hokusai and Hiroshige for colours, shapes and compositions that work in pixels. Environments are essentially paintings at 512x512 or 1024x512 with many separate entities layered on; drawn in Cosmigo ProMotion — [CDM](https://cdm.link/inside-handheld-game-art-the-art-style-and-making-of-swords-sworcery-superbrothers-pixel-cinema/).
- Adams has said the look works because players complete it with their imagination — [Exclaim](https://exclaim.ca/music/article/sworcerers_apprentices) (snippet).
- Observation: characters are tall and thin with one-pixel-wide limbs, tiny heads and no faces; no outlines; large flat colour fields with soft atmospheric gradients; muted teal/olive/gold palette. This is the direct ancestor of the HLD family.

**Undertale** (Toby Fox, 2015) and **Deltarune** (2018 onward)
- Asked whether the naive art was a budget choice, Fox said he probably would not change it even with a hundred artists, and that visual gags benefit from funny, expressive drawings — [Kill Screen](https://killscreen.com/behind-humor-toby-foxs-undertale).
- Fox used GameMaker and MS Paint for sprites — [Undertale Wiki](https://undertale.wiki/w/Toby_Fox) (snippet). The default window is 640x480 — [Gamer Journalist](https://gamerjournalist.com/how-to-make-undertale-fullscreen/) (snippet).
- Deltarune: Temmie Chang is credited as main artist and animator; Fox considered a Chrono Trigger-like look before returning to the Undertale style — [Deltarune Wiki credits](https://deltarune.wiki/w/Credits), [TCRF concept art](https://tcrf.net/Prerelease:Deltarune/Concept_Art/Chapter_1:_The_Beginning) (snippets).
- Observation: 320x240 logical canvas doubled; overworld characters have hard black outlines and two or three flat colours with almost no shading; rooms float in black voids; battles are white-on-black monochrome line art in a boxed UI. Deltarune keeps the grammar but splits palettes: muted earthy "light world" versus saturated neon-on-dark "dark world", with larger, more animated sprites.

**EarthBound / Mother 2** (Ape and HAL Laboratory, 1994) and **Mother 3** (Brownie Brown and HAL, 2006)
- Itoi called the game's visual style a kind of video drug, and one specialist produced nearly 200 distinct battle backgrounds — [Mother 4ever interview archive](https://mother4ever.net/interviews-about-mother-2/) (snippet, fan translation).
- The look is routinely compared with Peanuts; Toby Fox described it as resembling an off-brand Charlie Brown game that still evokes many emotions — [Kill Screen](https://killscreen.com/behind-humor-toby-foxs-undertale); see also [RPGFan review](https://www.rpgfan.com/review/earthbound-2/) (snippet).
- Art director Kouichi Oyama reportedly prefers Mother 1's look to Mother 2's — [Mother 4ever](https://mother4ever.net/his-her-mother-feeling-kouichi-oyamas-opinion/) (snippet; page 404 on fetch).
- Mother 3 started as a polygon N64 game. Miyamoto suggested pixel art could make it achievable; Itoi later said pixel art is what matches Mother and flashy CG is not an option for him — [Mother 4ever, Nintendo Dream 2006](https://mother4ever.net/nindori-62006/) (snippet; page 404 on fetch), [Brownie Brown interview](https://mother4ever.net/release-brownies-interview) (snippet).
- Mother 3's art director Nobuhiro Imagawa sketched each character on paper to find expressions before converting to sprites — [Mother 4ever](https://mother4ever.net/musicart-mother3/) (snippet).
- Observation: modern suburban towns drawn in oblique projection with streets running on diagonals; flat cel colours, black outlines, almost no texture; characters about 2 heads tall (roughly 16x24 pixels) with dot eyes; battle screens use abstract animated psychedelic backgrounds instead of scenery. Mother 3 keeps the grammar on GBA with many more bespoke animation frames per character.

**The Legend of Zelda: Link's Awakening** (Nintendo, 1993; DX 1998) and **The Minish Cap** (Capcom/Flagship and Nintendo, 2004)
- Game Boy canvas is 160x144 — [Yacht Club Games](https://www.yachtclubgames.com/blog/the-art-of-the-game). Original hardware shows four shades; Game Boy Color can show up to 56 colours at once; GBC sprites get 3 colours plus transparency — [Wikipedia, Link's Awakening DX](https://en.wikipedia.org/wiki/The_Legend_of_Zelda:_Link%27s_Awakening_DX) and a pixel-art blog (snippets).
- Link's Awakening DX uses yellow as a main highlight colour — [Yacht Club Games](https://www.yachtclubgames.com/blog/the-art-of-the-game).
- Minish Cap uses a modified Four Swords style pulled toward The Wind Waker — [Zelda Dungeon Wiki](https://www.zeldadungeon.net/wiki/Minish_Cap) (snippet). It is widely described as Wind Waker shrunk to 16-bit sprites and a high point of 2D pixel art — [Kotaku](https://kotaku.com/legend-of-zelda-art-totk-botw-link-tears-of-the-kingdom-1850579660/12) (snippet).
- Observation: Link's Awakening is 16x16 sprites on a 16x16 tile grid, a 10x8-tile room per screen, black outlines carrying all form because there are only four values. Minish Cap (GBA, 240x160): bright, high-saturation palette, outlines tinted to the local colour rather than pure black, big-head toon proportions, and very high animation density; the shrinking mechanic redraws ordinary props (boots, leaves, barrels) at giant scale.

**Pokemon generations 3 to 5** (Game Freak, 2002 to 2012)
- Gen 3 front battle sprites are 64x64 (8x8 tiles); early Gen 3 sprites are static, Emerald adds animation — [Bulbapedia](https://bulbapedia.bulbagarden.net/wiki/Pok%C3%A9mon_sprites) (snippet). Gen 4 battle sprites are 80x80 and Gen 5 are 96x96 — [PokeBase](https://pokemondb.net/pokebase/418580/what-are-the-dimensions-all-the-sizes-the-gen-battle-sprites) (snippet; another answer on the same site says 96x96 for both, so Gen 4 is disputed).
- Observation: overworld is a 16x16 tile grid with 16x32 trainer sprites about 2 heads tall, hard black outlines, flat bright colour and two-tone shading. Gen 3 is fully 2D. Gen 4 renders terrain and buildings as low-poly 3D with pixel textures and keeps characters as 2D sprites. Gen 5 adds a moving camera, large 3D set pieces and constantly animated battle sprites. Constant across all three: characters and world share one tile density and one outline rule.

**Octopath Traveler** (Square Enix and Acquire, 2018; HD-2D)
- The first tests added dramatic lighting to Final Fantasy VI-style 2D art; producer Tomoya Asano judged that insufficient for a full-price game, so 3D environments were added for depth. Asano wanted light and shadow on pixels to be the emphasis — [Nintendo Everything (Nintendo Dream translation)](https://nintendoeverything.com/octopath-traveler-devs-on-character-origins-visual-style-initial-hd-rumble-plans-much-more/).
- Producer Masashi Takahashi: a plain pixel game would not feel modern enough; adding too much detail turns it into just a pretty picture; simply making pixels chunkier is nostalgia overcompensation. An even more pixelated version existed briefly and was dropped — [Nintendo Everything](https://nintendoeverything.com/octopath-traveler-devs-on-character-origins-visual-style-initial-hd-rumble-plans-much-more/).
- For Triangle Strategy, Acquire judged that studios who made photoreal images and reduced them got HD-2D wrong; only Artdink's approach was accurate — [Nintendo Life](https://www.nintendolife.com/news/2022/05/triangle-strategy-producers-talk-hd-2d-and-why-other-devs-havent-used-it) (snippet).
- Observation: SNES-proportioned sprites (about 3 heads) standing in 3D dioramas textured with pixel art, under heavy depth of field (tilt-shift), bloom, vignette, point lights and particles. Characters and world do not share pixel density on screen once the camera blurs and scales the scene.

#### Everyday and modern settings (rooms, bars, apartments, towns)

**Unpacking** (Witch Beam, 2021; isometric rooms)
- Creative director Wren Brier chose pixel art because it is a core skill and isometric because it suits grid-based placement. Rooms were grey-boxed in Aseprite with placement grids drawn on floors, shelves and cupboards; art was adjusted so grids had no awkward gaps; furniture was split into pieces for depth and rebuilt in Unity; 35 rooms — [Game Developer](https://gamedeveloper.com/design/intimacy-from-the-inanimate-in-house-moving-puzzler-unpacking).
- Lead pixel artist Angus Doolan: the whole game's scale derives from how small a recognisable mug could be drawn; items are deliberately mis-proportioned for recognition (nail clippers drawn giant and short); because items rotate, isometric errors are immediately visible — [mirror of an interview by Diane Lowe](https://eugames.pages.dev/posts/how-unpacking-s-art-combines-beauty-with-clarity) (mirror site; original outlet not identified).
- Context changes recognition: a dark bottle read as wine until it was unpacked after olive oil; a red outline marks a misplaced item — [Game Developer](https://gamedeveloper.com/design/intimacy-from-the-inanimate-in-house-moving-puzzler-unpacking).
- Witch Beam later said 2D pixel art suited Unpacking because objects map precisely to placement — [Nintendo Life](https://www.nintendolife.com/features/how-lemmings-chuchu-rocket-and-nintendo-inspired-unpacking-devs-next-game) (snippet).
- Observation: no characters appear at all; the props are the cast. Soft pastel room palettes with one slightly darker, hue-shifted outline per object (never black), gentle top-left light, small contact shadows, and consistent 2:1 isometric lines. Rooms are quiet and low-contrast so that colourful objects carry attention.

**Coffee Talk** (Toge Productions, 2020; side-on bar)
- Lead artist Dio Mahesa: references are Cowboy Bebop, Ghost in the Shell and Evangelion for a 90s feel; intro cutscenes take cues from PC-98 games (small frame on black); the colour scheme is brownish and low saturation, and character palettes are tied to the overall palette so everything sits together; workflow is sketch, pixel render, then Spine animation, about 3 to 4 days per character — [Toge devlog #2](https://togeproductions.itch.io/coffee-talk-demo/devlog/66764/coffee-talk-devlog-2-bringing-doodles-to-life).
- The studio positions the look as 90s anime plus classic pixel adventure games plus lo-fi chillhop imagery — [Toge Productions](https://www.togeproductions.com/project/coffee-talk) (snippet).
- Observation: large waist-up character sprites (anime proportions, not chibi) seated at a counter, single fixed interior, rain and neon through the window as the only strong colour, skeletal animation for breathing and blinking rather than frame redraws.

**VA-11 HALL-A** (Sukeban Games, 2016; bar, visual-novel framing)
- Artist Christopher Ortiz: the main influence is the look of old PC-98 games, chosen because it looked futuristic rather than just retro; the game should look as if it came from a parallel world where Japan's technology won; vaporwave also fed in; named references include Blade Runner, Ghost in the Shell and Bubblegum Crisis — [Siliconera, 2014](https://www.siliconera.com/va-11-hall-designer-japanese-cyberpunk-influenced-game/).
- It follows PC-98 presentation closely, including ornate decorative menus, with visual references to Snatcher and Policenauts — [Infinite Rainy Day (Jonathan Kaharl)](https://infiniterainyday.blogspot.com/2016/11/va-11-hall-and-japanese-pc-cyberpunk.html). An optional scanline mode imitates a PC-98 CRT — [ASCII.jp](https://weekly.ascii.jp/elem/000/001/627/1627325/) (snippet).
- Observation: the screen is a multi-window UI frame (portrait window, text, drink-mixing panel); characters are high-detail anime bust portraits with dithered gradients and hard pixel highlights; purple/magenta/teal bias on dark backgrounds.

**Norco** (Geography of Robots, 2022; first-person point-and-click)
- Yuts: visuals come directly from suburban New Orleans landscapes after years of photographing and painting the region; the industrial landscape, cypress swamps and suburbs are the subject; sci-fi elements should feel banal; drawn in Aseprite; traditional painter Jesse Jacobi joined and adapted his skills to pixels — [Game Developer](https://www.gamedeveloper.com/road-to-igf-2023/-i-norco-i-and-capturing-the-spirit-of-louisiana-through-sci-fi-storytelling).
- Yuts on the medium: pixel art imposes stylistic restrictions, and limiting palette or canvas adds more, which forces creativity; dithering and anti-aliasing are its distinctive techniques — [Carbon Copy](https://carboncopy.world/yutsi).
- Early builds capped canvases at 600x400 — [Wikiwand](https://www.wikiwand.com/en/articles/Norco_(video_game)) (snippet).
- Observation: full-screen painted scenes, not tiles; heavy dithering for skies and haze; dusk palettes (orange, magenta, deep blue) with refinery lights as points; characters shown as detailed portraits or small silhouettes within the scene.

**Papers, Please** (Lucas Pope, 2013; desk view)
- Pope planned mid-res pixel art because it is easier, faster and more enjoyable for him; rather than one global palette he limits each object or background to roughly three shades; he switched from 16:9 to 3:2 for more room; walking figures started as a one-colour 8x18 pixel character with a deliberately rotoscoped feel; faces are assembled from parts sheets (head/shoulders, eyes, mouth/nose), eight sheets giving 32,768 faces — [Pope's TIGSource devlog, Nov 2012](https://dukope.com/devlogs/papers-please/tig-00).
- Described as stark Soviet-style graphics with a highly limited palette — [Cooper Hewitt](https://exhibitions.cooperhewitt.org/designing-peace/?p=452) (snippet).
- Observation: drab olive, brown and grey with a single saturated red for the state; three distinct scales on one screen (tiny silhouettes outside, mid-size bust in the booth, large documents on the desk).

**A Space for the Unbound** (Mojiken, 2023; side view, 1990s Indonesian town)
- Marketed as Makoto Shinkai-inspired anime pixel art; setting drawn from Surabaya — [PC Gamer](https://www.pcgamer.com/au/a-space-for-the-unbound-is-a-slice-of-life-adventure-in-rural-indonesia), [Wikiwand](https://www.wikiwand.com/en/articles/A_Space_for_the_Unbound) (snippets).
- Observation: small simple characters against very detailed everyday street scenes with large painterly skies and strong time-of-day colour.

**Until Then** (Polychroma Games, 2024; side view, modern Philippines)
- Director Mickole Klein Nulud says The Last Night's use of pixel art in 3D space fixed the look they wanted — [GamingBolt](https://gamingbolt.com/until-then-interview-art-style-setting-characters-and-more). Reviews describe hand-drawn pixel characters inside 3D environments, compared to HD-2D remakes — [GameSkinny](https://gameskinny.com/reviews/until-then-review-a-narrative-adventure-that-finds-beauty-in-the-little-things) (snippet).

#### Lighting-led, horror and side-view relatives

**Signalis** (rose-engine, 2022)
- Uses low-poly 3D models with 2D sprites; the team always wanted 3D elements, though early prototypes were mostly 2D for technical reasons. The interviewer highlights the term "retrotech" for the look — [Indiegraze, 2018](https://indiegraze.com/?p=989) (snippet; page 404 on fetch).
- Press describes it as a pixel-art anime aesthetic with a 1990s feel — [80.lv](https://80.lv/articles/signalis-a-classic-horror-with-unique-aesthetics); and as 90s cyberpunk anime — [PC Gamer](https://www.pcgamer.com/arctic-horror-signalis-is-oozing-with-retro-anime-chills) (snippet).
- Observation: low-resolution 3D rendered to look like pixel art, viewed from a high fixed angle; near-monochrome cold rooms with a single saturated red accent; CRT noise and chromatic artefacts; hard-edged technical UI with German and Chinese text; hand-drawn anime close-ups in cutscenes.

**Animal Well** (Shared Memory / Billy Basso, 2024; side view)
- Renders at 320x180; on a 4K display that leaves 144 times the computing budget per pixel. Background art has normal maps, which Basso draws by hand alongside the art, with heavy dynamic lighting — [Game Developer, 2022](https://gamedeveloper.com/art/creature-feature-the-surreal-pixel-art-and-animation-of-animal-well), [PlayStation Blog](https://blog.playstation.com/?p=367113).
- Many layers composited; a fluid simulation layer for water and smoke whose colours are thresholded to match the pixel art; raymarched background shapes lit by foreground lights — [PlayStation Blog](https://blog.playstation.com/?p=367113).
- He deliberately skipped common indie juice such as squash-and-stretch and screen shake, and disliked the smooth gradients of stock engine lighting because they clash with pixel art — [Game Developer](https://gamedeveloper.com/art/creature-feature-the-surreal-pixel-art-and-animation-of-animal-well), [Wikipedia](https://en.wikipedia.org/wiki/Animal_Well) (snippet).
- Observation: mostly dark screens with small saturated light sources, scanline/CRT finish, blue-green-violet bias, tiny blob protagonist.

**Katana Zero** (Askiisoft, 2019; side view)
- Justin Stander used a large neon lighting effect that covered inconsistencies between assets made by many different artists, so the common glow makes the art read as one style — [MCV/Develop](https://www.mcvuk.com/business-news/askiisoft-katana-zero/).
- Presentation adds VHS artefacts over 1980s neon — [Red Bull](https://www.redbull.com/int-en/katana-zero-developer-justin-stander-interview) (snippet).

**Celeste** (Maddy Makes Games / EXOK, 2018; side view)
- The whole game renders to 320x180 and is scaled up, so pixels stay uniform — [Noel Berry](https://www.noelberry.ca/posts/celeste_lighting). Lights are masked by wall geometry so they stop at walls rather than acting as plain spotlights — [Noel Berry](https://www.noelberry.ca/posts/celeste_lighting).
- Madeline's sprite uses about twelve colours including transparency — [Adafruit pixel art guide](https://learn.adafruit.com/makecode-arcade-pixel-art-sprites/pixel-art-fundamentals) (snippet). Her hair is not in the sprite; it is drawn in real time from a small circle texture — [Noel Berry, Reddit](https://axebps-redlib.hf.space/r/gamedev/comments/9a0cfr/how_is_the_hair_in_celeste_made/e4sgcdc/?context=3) (snippet).
- Observation: 8x8 tiles; a very small big-headed character with no facial detail in play, with emotion carried by separate large hand-drawn dialogue portraits; one dominant hue per chapter.

**Loop Hero** (Four Quarters, 2021; top-down board)
- Reviews consistently single out the very limited palette and a deliberately noisy, CRT-era look; artist is Dmitry "Deceiver" Karimov — [PC Gamer](https://pcgamer.com/best-design-2021-loop-hero), [Destructoid](https://destructoid.com/?p=265570). The claim that the palette targets 1980s PC games comes only from a fan-run guide and is unverified.
- Observation: tiny sprites on a black void, dithered portraits, optional CRT filter, bitmap fonts; looks like an early-90s DOS/Amiga game.

#### Notable 2023 to 2026 additions

**Mina the Hollower** (Yacht Club Games; 80.lv describes it as a 2026 release) — the best-documented rule set found:
- Canvas 256x144 (widescreen take on Game Boy's 160x144); custom 64-colour palette arranged in ramps; sprites limited to 4 colours per 8x8 tile including black and transparency, so most sprite regions have about 2 working colours; more colours allowed only when a sprite is split on the 8x8 grid (for example a helmet or weapon) — [Yacht Club Games](https://www.yachtclubgames.com/blog/the-art-of-the-game).
- Tilesets use earthy, cool, muted tones; saturated colours are reserved for sprites and interactable objects; HUD is predominantly black; eggshell replaces yellow as the highlight; portraits sit on black to gain one colour — [Yacht Club Games](https://www.yachtclubgames.com/blog/the-art-of-the-game).
- Rules broken on purpose: 60 fps, parallax, scanline effects, limited scaling and rotation; avoided: 3D, anti-aliasing shaders, anything anachronistic — [Yacht Club Games](https://www.yachtclubgames.com/blog/the-art-of-the-game). (Article is a 2022 update; final game may differ.)

**Fields of Mistria** (NPC Studio, early access 2024): art direction draws on 90s shoujo anime — [Substack analysis](https://andrealmo.substack.com/p/optimising-the-farm-life-sim-equation) (snippet, secondary).

**Dave the Diver** (Mintrocket, 2023): pixel characters and fish over higher-resolution painted/3D underwater scenes with flat modern UI — [unofficial analysis](https://halabaojia.pages.dev/collection/20251124-dave-the-diver-pixel-hd-hybrid-visual-design) (snippet, third-party interpretation).

### Inferences

Style families (my grouping, based on the findings and observations above):

1. **Flat-shape, no-outline minimalism** — Sword & Sworcery, Hyper Light Drifter, Titan Souls, Moonlighter (softer), Minit (1-bit extreme). Small faceless or near-faceless figures, large flat colour fields, colour and silhouette doing the work, smooth gradients or glows allowed on top. Best when the world should feel vast and quiet.
2. **16-bit JRPG revival with outlines** — Chained Echoes, CrossCode, Stardew Valley, Pokemon Gen 3 to 5, Minish Cap, Sea of Stars (base art). About 2 to 3.5 head characters, dark tinted outlines, saturated palettes, characters and tiles on the same grid.
3. **Hand pixels plus real-time light** — Eastward, Sea of Stars, Animal Well, Celeste, Katana Zero, CrossCode (lightly). Pixel assets are authored for a lighting system (normal or bump maps, cast shadows, glow, colour grading). The light is the identity.
4. **HD-2D / pixels in 3D space** — Octopath Traveler, Until Then, Signalis (inverted: 3D made to look like pixels), Pokemon Gen 4 to 5 (mild), Dave the Diver. Camera effects and 3D depth around sprite characters.
5. **Naive flat cartoon** — EarthBound, Mother 3, Undertale, Deltarune. Black outlines, two or three flat colours, 2-head characters, mundane modern settings, expressive rather than polished.
6. **Hardware-palette discipline** — Link's Awakening, Mina the Hollower, Loop Hero, Papers Please, Minit. Explicit colour-count rules per sprite or object are the style.
7. **PC-98 and anime portrait interiors** — VA-11 HALL-A, Coffee Talk, Signalis cutscenes. Large detailed bust or waist-up characters in a fixed room, dithering, UI framing as part of the art.
8. **Painterly scene pixel art of real places** — Norco, A Space for the Unbound, Eastward's towns, Unpacking's rooms. Reference-driven depictions of ordinary places, with props carrying the storytelling.

For a small top-down game in an everyday setting (office, apartment), the most transferable recipes are: Unpacking (props as cast, tinted outlines, pastel rooms, scale derived from the smallest recognisable object); EarthBound/Undertale (flat colour, black outline, 2-head figures, very cheap to produce); Eastward (clutter density and warm light, but needs a lighting pipeline); and Mina-style explicit palette rules (muted world, saturated interactables).

### Gaps
- Developer-stated sprite dimensions were found only for Papers Please (8x18 test figure), Stardew (via modding community) and Pokemon battle sprites. Everything else on sprite height is observation.
- Hyper Light Drifter canvas: Preston's "480p" and "240p" statements conflict and neither gives width; 480x270 is unconfirmed.
- No primary source found for Eastward, Sea of Stars, Chained Echoes, Moonlighter, Titan Souls or Undertale internal resolutions.
- Unpacking: no source found for palette, outline or shadow rules, or total item count; the Doolan interview was only available on a mirror.
- Signalis: the Indiegraze interview and the Vice interview yielded nothing concrete on palette or render resolution.
- Loop Hero: no developer statement on palette found.
- Link's Awakening, Minish Cap and Pokemon: no developer art-direction statements found in this pass; entries rely on hardware facts and observation.

## Which games use strong restricted palettes or colour grading, and which use lighting as the main style driver?

### Takeaway
The list splits cleanly: one group gets identity from colour rules (few colours, fixed accent, graded palette), another from a lighting system that the assets are built to serve. A few (Eastward, Animal Well) do both.

### Cited Findings
Palette or grading as the driver:
- Minit: black-and-white only, as a founding constraint — [Game Developer](https://www.gamedeveloper.com/disciplines/road-to-the-igf-calis-nijman-kallio-and-johann-s-i-minit-i-).
- Mina the Hollower: 64-colour master palette, 4 colours per 8x8 sprite tile, muted world versus saturated interactables — [Yacht Club Games](https://www.yachtclubgames.com/blog/the-art-of-the-game).
- Papers Please: about three shades per object rather than a global palette — [Pope devlog](https://dukope.com/devlogs/papers-please/tig-00).
- Coffee Talk: brownish, low-saturation scheme with character palettes subordinate to it — [Toge devlog](https://togeproductions.itch.io/coffee-talk-demo/devlog/66764/coffee-talk-devlog-2-bringing-doodles-to-life).
- Hyper Light Drifter: colour and silhouette first; dark dense palette with soft gradients and red accents — [Automaton](https://automaton-media.com/articles/interviewsjp/20170525-47328/), [A.V. Club](https://avclub.com/hyper-light-drifter-blended-past-and-present-to-become-1798255620).
- Eastward: LUT colour grading softens the palette — [80.lv](https://80.lv/articles/eastward-charming-chinese-pixel-art-adventure).
- Link's Awakening: four shades on original hardware; 3 colours plus transparency per sprite on GBC — (snippets, see game entry).
- Loop Hero: limited palette noted by reviewers — [PC Gamer](https://pcgamer.com/best-design-2021-loop-hero).
- Norco: palette and canvas limits treated as creative constraints — [Carbon Copy](https://carboncopy.world/yutsi).

Lighting as the driver:
- Sea of Stars: dynamic lighting was the founding idea and dictates the asset pipeline — [MobileSyrup](https://mobilesyrup.com/2023/09/11/sea-of-stars-level-design-sabotage-studio-thierry-boulanger-interview/).
- Eastward: 3D scene, hand-painted bump maps, fog and sunbeams by time of day — [Game Developer](https://www.gamedeveloper.com/art/eastward-s-creators-share-insights-on-making-pixel-art-adventures).
- Animal Well: hand-drawn normal maps, layered dynamic lights, fluid sim, at 320x180 — [Game Developer](https://gamedeveloper.com/art/creature-feature-the-surreal-pixel-art-and-animation-of-animal-well), [PlayStation Blog](https://blog.playstation.com/?p=367113).
- Octopath Traveler: light and shadow on pixels was the producer's stated goal; 3D added for depth — [Nintendo Everything](https://nintendoeverything.com/octopath-traveler-devs-on-character-origins-visual-style-initial-hd-rumble-plans-much-more/).
- Katana Zero: neon glow as the unifier across mismatched assets — [MCV/Develop](https://www.mcvuk.com/business-news/askiisoft-katana-zero/).
- Celeste: wall-occluded lights at 320x180 — [Noel Berry](https://www.noelberry.ca/posts/celeste_lighting).
- CrossCode: lighting effects and alpha shadow maps over SNES-style art — [Game Developer](https://gamedeveloper.com/design/designing-i-crosscode-i-to-stand-out-in-the-retro-rpg-market).

Explicitly not lighting-driven:
- Moonlighter has no dynamic lighting; it fakes light with layered sprites — [80.lv](https://80.lv/articles/moonlighter-building-pixel-art-preparing-for-switch/).

### Inferences
- Lighting can substitute for art consistency (Katana Zero) and for palette discipline, but it has a pipeline cost: Sea of Stars needed one specialist for about five years and Eastward needed assets rebuilt in 3D with bump maps. For a small game, a baked colour grade (LUT) plus a few sprite-based light overlays (Moonlighter's approach) gets much of the mood at low cost.
- The cheapest strong identity on the list is a hard palette rule (Minit, Papers Please, Mina), because it constrains every future asset automatically.
- Basso's and HLD's cases point the same way: if you add smooth light to pixel art, either threshold it back to the palette (Animal Well) or commit to visibly smooth gradients as a deliberate contrast (HLD). Half-measures read as an engine default.
- Mina's rule of muted environment plus saturated interactables is a general readability device and applies directly to offices and apartments where everything is a prop.

### Gaps
- No numbers found for palette size in HLD, Eastward, Stardew, Unpacking, Coffee Talk or VA-11 HALL-A.
- No source describes Sea of Stars' lighting technically (normal maps versus height maps versus shadow geometry).
- Stardew Valley's seasonal palette swaps and Deltarune's light/dark world palettes are observation only.

## How do they treat outlines on characters versus on props and environment tiles? Do characters and environment share pixel density?

### Takeaway
Developers almost never talk about outlines, so this section is mostly observation. The reliable pattern is that characters are made simpler or more outlined than the world so they separate from it, and that true pixel-density matching is the norm except in the HD-2D and portrait-led families.

### Cited Findings
- Hyper Light Drifter's base sprites are minimalist and few-colour compared with 16-bit norms — [Game Developer (Felix Klein)](https://gamedeveloper.com/design/designing-i-crosscode-i-to-stand-out-in-the-retro-rpg-market).
- Celeste renders everything to one 320x180 target so all pixels are uniform — [Noel Berry](https://www.noelberry.ca/posts/celeste_lighting).
- Animal Well composites everything at 320x180 and thresholds simulated fluid colours to fit the pixel art — [PlayStation Blog](https://blog.playstation.com/?p=367113).
- Mina the Hollower forbids anti-aliasing shaders and 3D, and keeps sprites on the 8x8 tile colour grid — [Yacht Club Games](https://www.yachtclubgames.com/blog/the-art-of-the-game).
- Octopath Traveler deliberately mixes pixel sprites with 3D environments, and the producers rejected both a plain pixel look and a chunkier-pixel look — [Nintendo Everything](https://nintendoeverything.com/octopath-traveler-devs-on-character-origins-visual-style-initial-hd-rumble-plans-much-more/).
- Sword & Sworcery environments are single large paintings (512x512 or 1024x512) with separate entities layered on — [CDM](https://cdm.link/inside-handheld-game-art-the-art-style-and-making-of-swords-sworcery-superbrothers-pixel-cinema/).
- Unpacking uses a red outline as a UI signal for a misplaced item, and all items share one grid and scale — [Game Developer](https://gamedeveloper.com/design/intimacy-from-the-inanimate-in-house-moving-puzzler-unpacking).
- Stardew Valley characters and tiles share a 16-pixel grid (16x16 tiles, 16x32 NPCs), while portraits are a separate 64x64 asset — [official forum](https://forums.stardewvalley.net/threads/sprite-size-first-time-modding-sv.7128/latest) (snippet).
- Papers Please intentionally shows three different scales on screen (tiny walkers, booth portrait, documents) — [Pope devlog](https://dukope.com/devlogs/papers-please/tig-00).

### Inferences
Observed outline treatments (all observation):

| Treatment | Characters | Props / tiles | Games |
|---|---|---|---|
| None anywhere | flat shapes | flat shapes | Hyper Light Drifter, Sword & Sworcery, Titan Souls |
| Black on everything | black | black | EarthBound, Mother 3, Undertale, Pokemon Gen 3 to 5, Link's Awakening |
| Dark tinted on everything | dark hue-shifted | dark hue-shifted | Stardew Valley, Minish Cap, CrossCode, Unpacking (props only, no characters) |
| Characters outlined, world not | thin dark | painterly, mostly none | Eastward, Sea of Stars, Chained Echoes, A Space for the Unbound |
| 1-bit line | line only | line only | Minit |

- Density: nearly every game on the list keeps characters and environment at the same pixel size. Exceptions are intentional and structural: HD-2D (Octopath, Until Then), portrait-led interiors (Coffee Talk, VA-11 HALL-A, Papers Please, Celeste's dialogue portraits) where a larger-scale character image sits in a UI frame, and Signalis, where 3D is down-sampled to match sprite density.
- When outline rules differ between characters and world, the characters are always the more outlined and less textured element. No game on the list does the reverse.
- Mixing densities inside the play field (as opposed to in UI frames) is rare enough that doing it accidentally will read as an error.

### Gaps
- No developer source found that states an outline rule for any game on the list.
- Outline colour (pure black versus tinted) for Sea of Stars, Chained Echoes and CrossCode should be confirmed against sprite sheets before relying on the table.

## What character proportions do they use (head-to-body ratio, sprite height in pixels)?

### Takeaway
Top-down games cluster at 2 to 3.5 heads tall on a 16-pixel-wide body; the minimalist family goes smaller and drops faces; the everyday-interior games either remove characters (Unpacking) or show them as large portraits. Hard numbers from developers are scarce.

### Cited Findings
- Stardew Valley: NPC overworld sprites 16x32 on 16x16 tiles; portraits 64x64 — [official forum](https://forums.stardewvalley.net/threads/sprite-size-first-time-modding-sv.7128/latest), [modding wiki](https://stardewmodding.wiki.gg/wiki/So_You_Want_To_Be_a_Map_Modder:_Preparations) (snippets).
- Pokemon battle sprites: 64x64 (Gen 3), 80x80 (Gen 4, disputed), 96x96 (Gen 5) — [Bulbapedia](https://bulbapedia.bulbagarden.net/wiki/Pok%C3%A9mon_sprites), [PokeBase](https://pokemondb.net/pokebase/418580/what-are-the-dimensions-all-the-sizes-the-gen-battle-sprites) (snippets).
- Papers Please: walking figures prototyped as a one-colour 8x18 pixel character — [Pope devlog](https://dukope.com/devlogs/papers-please/tig-00).
- Celeste: Madeline's sprite has about twelve colours and her hair is rendered separately — [Adafruit](https://learn.adafruit.com/makecode-arcade-pixel-art-sprites/pixel-art-fundamentals), [Noel Berry, Reddit](https://axebps-redlib.hf.space/r/gamedev/comments/9a0cfr/how_is_the_hair_in_celeste_made/e4sgcdc/?context=3) (snippets).
- Mina the Hollower: sprites built on 8x8 tiles at 256x144 — [Yacht Club Games](https://www.yachtclubgames.com/blog/the-art-of-the-game).
- Unpacking: the scale of every object derives from the smallest recognisable mug; some items are deliberately off-proportion to stay readable — [interview mirror](https://eugames.pages.dev/posts/how-unpacking-s-art-combines-beauty-with-clarity).
- Canvas sizes that bound sprite scale: Celeste and Animal Well 320x180 — [Noel Berry](https://www.noelberry.ca/posts/celeste_lighting), [Game Developer](https://gamedeveloper.com/art/creature-feature-the-surreal-pixel-art-and-animation-of-animal-well); CrossCode 568x320 — [PCGamingWiki mirror](https://gamecytus.netlify.app/host-https-www.pcgamingwiki.com/wiki/CrossCode) (snippet); Game Boy 160x144 and Mina 256x144 — [Yacht Club Games](https://www.yachtclubgames.com/blog/the-art-of-the-game).

### Inferences
Approximate proportions (all observation unless cited above):

| Proportion | Typical sprite | Games |
|---|---|---|
| About 2 heads, big head, dot eyes | 16x16 to 16x24 | Link's Awakening, EarthBound, Mother 3, Undertale (roughly 19x29 in a 320x240 canvas) |
| About 2 heads on a 1x2 tile body | 16x32 | Stardew Valley, Pokemon Gen 3 to 5 overworld |
| 2.5 to 3.5 heads, JRPG | roughly 24 to 40 tall | Chained Echoes, CrossCode, Sea of Stars, Octopath, Eastward, Minish Cap (toon, big head) |
| Small faceless figure | roughly 12 to 30 tall | Titan Souls (smallest), Hyper Light Drifter, Celeste, Animal Well |
| Elongated, 1-pixel limbs, no face | tall and thin | Sword & Sworcery |
| Large anime bust or waist-up | hundreds of pixels | Coffee Talk, VA-11 HALL-A, Papers Please booth portraits |
| No characters on screen | n/a | Unpacking |

- The 16-wide by 32-tall figure on a 16-pixel tile is the most common and most forgiving top-down standard: it gives room for hair, outfit colour and a readable 4-direction walk without needing a face.
- Below about 20 pixels tall, every game on the list removes facial features and relies on silhouette, a cape/hair/hat shape and one signature colour.
- Games that want emotional acting from tiny sprites add a second, larger representation: portraits (Stardew, Celeste, Deltarune, Mina) or bespoke animation frames (Mother 3, Minish Cap).

### Gaps
- No developer-stated overworld sprite sizes for HLD, Eastward, Sea of Stars, Chained Echoes, CrossCode, Moonlighter, Titan Souls, EarthBound, Mother 3, Minish Cap or Undertale. The Undertale and Pokemon overworld figures are recollection and should be checked against sprite rips.
- Head-to-body ratios in the table are eyeballed.

## What have the artists said about how they found the style and what they avoided?

### Takeaway
Three recurring stories: the style came from a practical limit that the developer then turned into a rule; the style existed as an image before the game did; or the style was found by adding one modern system to an old grammar and rejecting both pure nostalgia and over-polish.

### Cited Findings
Constraint turned into a rule:
- Preston abandoned an HD illustrated look as too much for one person, then insisted the pixel art be neither boring nor ugly and carry his personal style; he says constraints produce creative solutions and clear goals — [Game Developer](https://gamedeveloper.com/business/the-ultra-modern-stylings-of-hyper-light-drifter), [Automaton](https://automaton-media.com/articles/interviewsjp/20170525-47328/).
- Pope chose pixel art because it is faster and more enjoyable for him, and planned to copy the limited palettes he admired in good pixel games — [Pope devlog](https://dukope.com/devlogs/papers-please/tig-00).
- Adams calls the Superbrothers look an engineering decision as much as an artistic one — [CDM](https://cdm.link/inside-handheld-game-art-the-art-style-and-making-of-swords-sworcery-superbrothers-pixel-cinema/).
- Linda says it is simply the style he is capable of — [Lords of Gaming](https://lordsofgaming.net/2023/01/interview-chained-echoes-developer-matthias-linda) (snippet).
- Gleeson: pixel art was the fastest route in a jam and his normal medium — [GameCloud](https://gamecloud.net.au/features/interviews/titan-souls-developer-interview-with-andrew-gleeson).
- Stander could not retain pixel artists, drew much himself, and used neon glow to hide the seams — [MCV/Develop](https://www.mcvuk.com/business-news/askiisoft-katana-zero/).
- Yuts: palette and canvas limits force creativity — [Carbon Copy](https://carboncopy.world/yutsi).
- Basso: limitations encourage creativity; early on the game looked like an NES game and rendering systems were layered on over time — [Game Developer](https://gamedeveloper.com/art/creature-feature-the-surreal-pixel-art-and-animation-of-animal-well).
- Digital Sun thought pixel art would be easier than 3D and say they were wrong; four-direction sprites for every item limited content — [80.lv](https://80.lv/articles/moonlighter-building-pixel-art-preparing-for-switch/).

Image before game:
- Eastward's team fell for Hong Moran's mock-up and built the design around it — [Nintendo](https://nintendo.com/us/whatsnew/how-the-developers-began-making-then-remaking-eastward).
- Norco grew out of years of photographing and painting suburban New Orleans, and pixel art slowly became a game — [Game Developer](https://www.gamedeveloper.com/road-to-igf-2023/-i-norco-i-and-capturing-the-spirit-of-louisiana-through-sci-fi-storytelling), [Carbon Copy](https://carboncopy.world/yutsi).
- Until Then's look was fixed by one reference (The Last Night) — [GamingBolt](https://gamingbolt.com/until-then-interview-art-style-setting-characters-and-more).
- VA-11 HALL-A's premise for the look: a parallel world where Japanese PC aesthetics became the future — [Siliconera](https://www.siliconera.com/va-11-hall-designer-japanese-cyberpunk-influenced-game/).

Old grammar plus one modern system; what was rejected:
- Octopath: rejected plain pixel art (not modern enough), over-detailing (becomes merely a pretty picture) and chunkier pixels (nostalgia overcompensation) — [Nintendo Everything](https://nintendoeverything.com/octopath-traveler-devs-on-character-origins-visual-style-initial-hd-rumble-plans-much-more/).
- Sea of Stars: keep what worked in old JRPGs, drop what aged badly; all assets answer to the lighting — [MobileSyrup](https://mobilesyrup.com/2023/09/11/sea-of-stars-level-design-sabotage-studio-thierry-boulanger-interview/).
- CrossCode: authentic only in sprite style; resolution, lighting and shadows are openly modern — [Game Developer](https://gamedeveloper.com/design/designing-i-crosscode-i-to-stand-out-in-the-retro-rpg-market).
- Animal Well: avoided squash-and-stretch and screen shake, and avoided stock engine lighting — [Game Developer](https://gamedeveloper.com/art/creature-feature-the-surreal-pixel-art-and-animation-of-animal-well), [Wikipedia](https://en.wikipedia.org/wiki/Animal_Well) (snippet).
- Mina the Hollower: avoided 3D, anti-aliasing and saturated Zelda-style environment hues; allowed parallax, 60 fps and widescreen — [Yacht Club Games](https://www.yachtclubgames.com/blog/the-art-of-the-game).
- Mother 3: Itoi rejected flashy CG as not an option and concluded pixel art is what suits Mother — [Mother 4ever](https://mother4ever.net/nindori-62006/) (snippet).
- Undertale: Fox would keep the naive look even with a large art team — [Kill Screen](https://killscreen.com/behind-humor-toby-foxs-undertale).
- Coffee Talk: palette decided first (brown, low saturation), characters fitted to it; one character was redesigned because the rushed version did not sell the personality — [Toge devlog](https://togeproductions.itch.io/coffee-talk-demo/devlog/66764/coffee-talk-devlog-2-bringing-doodles-to-life).
- Unpacking: pixel art from day one as the director's core skill; isometric was new and a steep learning curve; art, level design and narrative could not be separated — [Game Developer](https://gamedeveloper.com/design/intimacy-from-the-inanimate-in-house-moving-puzzler-unpacking).

### Inferences
- None of the artists describe choosing pixel art for nostalgia alone; several explicitly distance themselves from it (Ortiz, Takahashi, Linda, Preston).
- The most reusable process lessons for a small team: decide the palette before the characters (Coffee Talk); derive world scale from the smallest object that must be recognisable (Unpacking); pick one unifying layer, such as a glow, grade or palette rule, that makes inconsistent assets cohere (Katana Zero, Eastward's LUT, Mina's 64 colours); and write down which period rules you break and which you keep (Mina, CrossCode).
- Statements about what was avoided cluster around three things: default engine smoothness (Basso, Yacht Club), nostalgia for its own sake (Takahashi, Ortiz), and detail that hurts readability (Preston, Doolan).

### Gaps
- No art-direction statements found from Nintendo/Capcom staff on Link's Awakening or Minish Cap, from Game Freak on Gen 3 to 5 overworld art, or from Kouichi Oyama on EarthBound's projection and flat colour (the relevant translated interview pages returned 404).
- Eric Barone's widely reported repeated redrawing of Stardew Valley's art could not be confirmed with a primary source in this pass; only his statement that he started with no pixel art experience was found.
- No direct statements from Wren Brier on Unpacking's colour or outline rules, from rose-engine on Signalis's palette, or from Four Quarters on Loop Hero's palette.
- Chucklefish's "Eastward: Design Works" book and documentary likely contain Hong Moran's own account; only the announcement page was accessible.
