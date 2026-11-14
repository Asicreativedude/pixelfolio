# Distinctive game art styles outside mainstream colourful pixel art, for a 640×360 top-down 2D browser game

Reading notes for the report writer:

- Source confidence is tagged on every finding. **[fetched]** means I opened the page and the claim was read from it. **[snippet]** means the claim came from a search-result summary of that page and the page itself was not opened (or returned 403/404). Treat [snippet] items as leads that need a second look before quoting.
- Anything labelled **observation** is my inference, not a sourced fact.
- Release years in the "Reference games" lines are from general knowledge and were not individually sourced in this pass unless a link follows them. Check against Wikipedia before publishing.
- One correction to the brief: Return of the Obra Dinn was prototyped at 640×360 but shipped at 800×450 (see 1.1).

---

## Key question 1: What are the concrete rules that make each style read as itself?

### Takeaway

Each of these styles is defined by a short list of hard constraints (number of colours, whether outlines exist, whether light is drawn or computed, what a shape is allowed to be), and the creators consistently say the constraint came first and legibility work came second. The styles with the clearest written-down rules, and the best fit for 640×360, are 1-bit with outlines (Obra Dinn, Playdate), the fixed-palette handhelds and fantasy consoles (Game Boy, PICO-8), flat-shape illustration (Sable, Night in the Woods, Wilmot's Warehouse), and the desktop/OS interface styles (Hypnospace Outlaw, Kingsway, Emily is Away).

### Cited Findings

#### 1.1 1-bit and two-colour

Reference games: Return of the Obra Dinn (Lucas Pope, 2018), Minit (JW Nijman, Kitty Calis, Jukio Kallio, Dominik Johann, 2018), Downwell (Ojiro Fumoto / Moppin, 2015), World of Horror (Paweł Koźmiński / panstasz, early access 2020, 1.0 in 2023), Gato Roboto (doinksoft, 2019), Playdate titles (Panic hardware, 2022), Rogue Invader (Squishy Games), and the 1980s Mac precedents Dark Castle (1986) and The Colony (1987).

Obra Dinn rules and intent:

- Pope's own summary of the style: "One bit per pixel. Two colours. 800×450 pixels of high resolution 3D rendering." **[fetched]** — [PlayStation Blog, Lucas Pope, 17 Oct 2019](https://blog.playstation.com/archive/2019/10/17/lucas-pope-on-return-of-the-obra-dinns-art-style)
- Resolution: the game was "originally 640×360" and shipped after "a slight resolution increase to 800×450". **[fetched]** — [PlayStation Blog](https://blog.playstation.com/archive/2019/10/17/lucas-pope-on-return-of-the-obra-dinns-art-style). A 2015 article written during development gives 640×360, which matches the prototype figure, not the shipped one. **[fetched]** — [Game Developer, 30 Nov 2015](https://www.gamedeveloper.com/design/lucas-pope-and-the-rise-of-the-1-bit-dither-punk-aesthetic)
- Reference hardware: the Macintosh Plus, "a tiny but crisp 9″ black and white monitor with 512×342 square pixels." **[fetched]** — [PlayStation Blog](https://blog.playstation.com/archive/2019/10/17/lucas-pope-on-return-of-the-obra-dinns-art-style)
- Priority order: "For the 3D style, I decided to prioritise legibility above all else", which "basically meant two things: 1) outlines on geometry and 2) careful dithering." **[fetched]** — [PlayStation Blog](https://blog.playstation.com/archive/2019/10/17/lucas-pope-on-return-of-the-obra-dinns-art-style)
- Dither rule: "the most important part of using dithering was to use it as little as possible." Two pattern families were used: grid-like Bayer patterns (more accurate tone) and blue noise (more organic). **[fetched]** — [PlayStation Blog](https://blog.playstation.com/archive/2019/10/17/lucas-pope-on-return-of-the-obra-dinns-art-style)
- Surface rule: objects are mostly solid black or solid white, with pattern dither only for shading; outlines invert (black on light areas, white on dark), a device taken from The Colony. **[fetched]** — [Game Developer, 2015](https://www.gamedeveloper.com/design/lucas-pope-and-the-rise-of-the-1-bit-dither-punk-aesthetic)
- The fullscreen problem: the look worked in a small window but strained the eyes on a large monitor; dither flickered when the camera moved. The fix was a dither technique that tied the 3D camera to the 2D pattern (reported elsewhere as sphere-mapped dither) plus the resolution bump. **[fetched]** — [PlayStation Blog](https://blog.playstation.com/archive/2019/10/17/lucas-pope-on-return-of-the-obra-dinns-art-style); sphere-mapping detail **[snippet]** — [PC Gamer](https://www.pcgamer.com/lucas-pope-on-the-challenge-of-creating-obra-dinns-1-bit-aesthetic)
- Intent: Pope on the Mac Plus look, "there's something about the missing color. You had to fill it in with your imagination". **[fetched]** — [Game Developer, 2015](https://www.gamedeveloper.com/design/lucas-pope-and-the-rise-of-the-1-bit-dither-punk-aesthetic)
- Fidelity ceiling: past a certain resolution dithering stops being visible and reads as plain greyscale; Rogue Invader's artists found 720p to be the upper limit where dither still shows. **[fetched]** — [Game Developer, 2015](https://www.gamedeveloper.com/design/lucas-pope-and-the-rise-of-the-1-bit-dither-punk-aesthetic)
- Video compression (YouTube, Twitch) blurs 1-bit dither and introduces grey pixels. **[fetched]** — [Game Developer, 2015](https://www.gamedeveloper.com/design/lucas-pope-and-the-rise-of-the-1-bit-dither-punk-aesthetic)
- Rogue Invader's 1-bit separation rule: soldiers mostly white, aliens mostly black, ground white. **[fetched]** — [Game Developer, 2015](https://www.gamedeveloper.com/design/lucas-pope-and-the-rise-of-the-1-bit-dither-punk-aesthetic)

Playdate (official 1-bit design guidance, the most rule-like source found):

- 400×240, 1-bit, 173 ppi, reflective with no backlight. **[fetched]** — [Playdate, Designing for Playdate](https://help.play.date/developer/designing-for-playdate/)
- Player sprites about 32×32 px or larger; avoid 8×8 tiles; 32×32 is a comfortable tile size. **[fetched]** — [Playdate](https://help.play.date/developer/designing-for-playdate/)
- Strokes at least 2 px thick; thinner lines look "wispy". **[fetched]** — [Playdate](https://help.play.date/developer/designing-for-playdate/)
- Text by cap height: dialogue at least 12 px and preferably 14 px, HUD at least 10 px, everything else at least 8 px. **[fetched]** — [Playdate](https://help.play.date/developer/designing-for-playdate/)
- Dither: clean up machine-dithered art by hand because automatic dither looks "fuzzy"; do not scroll a 2×2 checkerboard one pixel at a time because it flashes; scroll in multiples of 2 px. **[fetched]** — [Playdate](https://help.play.date/developer/designing-for-playdate/)
- Avoid runtime rotation and scaling of sprites; pre-render the variants. **[fetched]** — [Playdate](https://help.play.date/developer/designing-for-playdate/)
- 30 fps is the target; 20 fps is acceptable for "chunky" animation. **[fetched]** — [Playdate](https://help.play.date/developer/designing-for-playdate/)

Minit:

- The team lists black and white art among the limits it added deliberately: "The biggest growth was adding limitations. Everything from a time limit and simple controls to black and white art." Tools: GameMaker, Aseprite, Ableton, MS Paint. **[fetched]** — [Game Developer, Joel Couture, 6 Mar 2019](https://www.gamedeveloper.com/disciplines/road-to-the-igf-calis-nijman-kallio-and-johann-s-i-minit-i-)
- Kitty Calis on constraints: "it's nearly impossible to not get something original if you do things that way." **[fetched]** — [Game Developer](https://www.gamedeveloper.com/disciplines/road-to-the-igf-calis-nijman-kallio-and-johann-s-i-minit-i-)
- JW Nijman is reported as saying the black-and-white style makes iteration very fast (new ideas tested in minutes) but makes it "really hard to make the art clear"; Calis calls one-bit "super fun and quick to work in". **[snippet]**, from a Minit Fun Racer interview reposted on a mirror site, original outlet not identified — [mirror](https://arucoppu.pages.dev/posts/minit-fun-racer-devs-discuss-the-fun-and-challenge-of-making-the-game)

Downwell:

- Default look is a black background with white outlines, red reserved for gems, enemies and other important items, and blue for water; the colours can be swapped through unlockable palettes. Wikipedia counts four colours, not three. **[snippet]** — [Wikipedia, Downwell](https://www.wikipedia.org/wiki/Moppin)
- "Red and white character models" against solid black. **[snippet]** — [Kill Screen](https://www.killscreen.com/the-story-behind-downwell-one-of-this-years-most-delightful-surprises/)

World of Horror:

- All art drawn in MS Paint with a mouse by one developer. **[snippet]** — [Engadget, 20 Sep 2019](https://www.engadget.com/2019/09/20/world-of-horror-junji-ito-hp-lovecraft-hypercard-game/)
- Why 1-bit: the palette "was an obvious choice to represent black and white art of the comic pages" (Junji Ito manga); on MS Paint, "its limitations force you to get creative." **[snippet]** — [itch.io blog interview](https://itch.io/blog/1060/world-of-horror-is-polands-bloody-tribute-to-junji-ito-and-hp-lovecraft)
- The player can choose 1-bit or 2-bit art and then randomise the colour palette for a playthrough. **[snippet]** — [VideoGamesGood, PAX West 2023](https://videogamesgood.com/post/world-of-horror-developed-low-and-slow-heads-to-1-0-release-pax-west-2023-hands-on-interview)

Gato Roboto:

- Britt Brady started the game to practise programming and "thought that the 1-bit limitation would help him save time when making assets". **[snippet]** — [Game Developer Q&A](https://gamedeveloper.com/design/q-a-exploring-the-design-of-cat-in-a-mech-metroidvania-i-gato-roboto-i-)
- Alternate two-colour palettes are found as collectible cartridges. **[snippet]** — [GameWatcher review](https://gamewatcher.com/reviews/gato-roboto-review/13132)

#### 1.2 Extreme limited palettes: Game Boy, GB Studio, PICO-8

Reference: Game Boy DMG library (Nintendo, 1989 onward), GB Studio (Chris Maltby, 2019 onward), PICO-8 (Lexaloffle / Joseph White, 2015), Celeste Classic (Maddy Thorson and Noel Berry, 2015), GBJam entries.

- Game Boy screen: 160×144, which is 20×18 tiles of 8×8. **[snippet]** — [GBJam 5 "the actual GB limits" thread](https://itch.io/jam/gbjam-5/topic/41384/the-actual-gb-limits)
- Four shades on a green-tinted STN LCD; the whole background shares one palette register. **[snippet]** — [bitmapped Game Boy preset](https://martink-rsa.github.io/bitmapped/presets/gameboy)
- Sprites get three colours plus transparency; 10 sprites per scanline. **[snippet]** — [GBJam thread](https://itch.io/jam/gbjam-5/topic/41384/the-actual-gb-limits)
- GBJam's actual rule set is looser than hardware: four colours on screen in total (sprites included, black counts), 160×144, palette may change between screens but not mid-scanline; the 8×8 grid is advice, not a rule. **[snippet]** — [GBJam thread](https://itch.io/jam/gbjam-5/topic/41384/the-actual-gb-limits)
- GB Studio: a background can hold at most 192 unique 8×8 tiles in most scene types; minimum background is 160×144, so even the smallest scene must repeat about half its tiles. **[snippet]** — [GB Studio docs, Backgrounds](https://gbstudio.dev/docs/assets/backgrounds)
- GB Studio: 384 tiles fit in VRAM at once across background, sprites and text; sprite budget is 96 tiles when the background uses 128 or fewer. **[snippet]** — [GB Studio docs, Scene limits](https://gbstudio.dev/docs/project-editor/scenes/limits)
- GB Studio actors are built from 8×16 units; 16×16 is the standard actor size. **[snippet]** — [GB Studio Central cheat sheet](https://gbstudiocentral.com/?p=3654)
- PICO-8: 128×128 display, fixed 16-colour palette, 4-channel sound, 32 KB cartridges; the palette was inspired by the Commodore 64. **[snippet]** — [Wikipedia, PICO-8](https://en.wikipedia.org/wiki/PICO-8)
- Celeste was first made in PICO-8 in four days at a game jam; that version survives as Celeste Classic. **[snippet]** — [Wikipedia, PICO-8](https://en.wikipedia.org/wiki/PICO-8); Thorson quoted on the four days in [Edge, 21 Jul 2016](https://www.pressreader.com/australia/edge/20160721/283218737511529)

#### 1.3 Flat vector and minimalist geometric

Reference: Monument Valley (ustwo, 2014), Alto's Adventure (Snowman / Harry Nesbitt, 2015), Thomas Was Alone (Mike Bithell, 2012), Mini Metro (Dinosaur Polo Club, 2015), Kentucky Route Zero (Cardboard Computer, 2013 to 2020), Limbo (Playdead, 2010), Inside (Playdead, 2016).

Monument Valley:

- Goal, Ken Wong: "We wanted every level in the game to be a piece of art that you could literally print out and frame". **[snippet]** — [TechCrunch](https://techcrunch.com/?p=913415)
- Rule attributed to producer Dan Gray: "Every screen in Monument Valley needs to work in three different ways - as a puzzle, as an architectural structure, and as a piece of graphic composition". **[snippet]**, exact page not verified — likely [Creative Bloq, The making of Monument Valley](https://creativebloq.com/computer-arts/making-monument-valley-71412213)
- Composition device: "little worlds", forms floating in a frame of negative space. Influences named: M. C. Escher, Japanese prints, minimalist 3D design, Middle Eastern architecture, Japanese flower arrangement, low-poly 3D. **[snippet]** — [Wikipedia](https://en.wikipedia.com/wiki/Monument_Valley_(game)); GDC 2015 talk listing at [GDC Vault, The Art of Monument Valley](https://gdcvault.com/play/1022299/The-Art-of-Monument)

Thomas Was Alone:

- Began as a 24-hour Flash prototype in 2010; the blocky abstract look was chosen as a time-saver. **[snippet]** — [Game Developer](https://gamedeveloper.com/business/-i-thomas-was-alone-i-from-24-hour-prototype-to-fully-fledged-game)
- Bithell: "I can't draw, so I'll make a game about rectangles. I can't code AI, so I'll make a game that doesn't have any AI". **[snippet]** — [NME, 2023](https://www.nme.com/features/boss-level-2023-mike-bithell-3432006)
- The rectangles were placeholders; replacing them with something more complex "lost something". Piet Mondrian is cited as inspiration for keeping them. **[snippet]** — [Wikipedia](https://en.wikipedia.org/wiki/Thomas_Was_Alone)

Mini Metro:

- Visual style is taken from Harry Beck's London Underground diagram: system clarity over geographic accuracy; the whole network can be scanned at a glance. **[snippet]** — [Pocket Gamer](https://www.pocketgamer.com/mini-metro/mini-metro-challenges-you-to-provide-subway-services-for-a-rapidly-growing-city/); [HERE, on Beck](https://here.com/learn/blog/expert-takes-beck-meaning-underground)
- Credits: Jamie Churchman (art), Peter and Robert Curry (design, programming). **[snippet]** — [Wikipedia](https://en.wikipedia.org/wiki/Mini_Metro_(video_game))

Kentucky Route Zero:

- Tamas Kemenczy's GDC 2014 talk frames the art direction through scenography (set design, architecture, film). **[snippet]** — [Game Developer, The Scenography of Kentucky Route Zero](https://gamedeveloper.com/design/video-the-scenography-of-i-kentucky-route-zero-i-)
- Scenes are built like stage sets from overlapping flat cut-outs with forced perspective. **[snippet]** — [Inverse](https://inverse.com/gaming/video-games-drama-final-fantasy-kentucky-route-zero)
- The final look is described as low-poly in the manner of Another World, so "flat vector" is only partly accurate. **[snippet]** — [USgamer](https://www.usgamer.net/articles/kentucky-route-zeros-creators-at-the-end-of-the-road-it-feels-like-we-made-10-games)
- Kemenczy says the art style was rigid and he was stubborn about keeping to it. **[snippet]** — [Vice](https://www.vice.com/en/article/kentucky-route-zero-creators-on-finding-hope-and-the-burden-of-4k-gaming/)

Limbo and Inside:

- Limbo: monochrome, "essentially only silhouettes for characters, enemies and backgrounds". **[snippet]** — [Hardcore Gaming 101](https://www.hardcoregaming101.net/limbo/)
- Director Arnt Jensen drew on film noir; graphic artist Morten Bramsen is credited with realising the style. **[snippet]** — [Wikipedia mirror, Limbo](https://cavac.at/cavacopedia/Limbo_%28video_game%29)
- Inside is mostly, but not entirely, monochrome. **[snippet]** — [Giant Bomb user essay](https://www.giantbomb.com/profile/gamer_152/blog/detached-the-design-of-inside/114715/)

#### 1.4 Print and illustration inspired

Reference: Sable (Shedworks, 2021), Hohokum (Honeyslug and Richard Hogg, 2014), Gris (Nomada Studio / Conrad Roset, 2018), Old Man's Journey (Broken Rules, 2017), Saturnalia (Santa Ragione, 2022), Chicory: A Colorful Tale (Greg Lobanov and team, 2021), Wilmot's Warehouse (Hollow Ponds and Richard Hogg, 2019).

Sable (Moebius, ligne claire):

- Flat shading everywhere. Kythreotis: "One big issue with making a flat shaded world with characters and backgrounds is reading depth in 3D space". Depth is rebuilt in layers: lighting, then fog, then lines. **[fetched]** — [Game Developer, Chris Kerr, 25 Mar 2022, reporting the GDC 2022 talk](https://www.gamedeveloper.com/marketing/how-shedworks-refined-the-art-of-sable-in-pursuit-of-readability)
- Cast shadows are a readability tool: "Having light and shadows helps players figure out where they sit on a surface"; a shadow was even added to moonlight so the player nearly always casts one. **[fetched]** — [Game Developer](https://www.gamedeveloper.com/marketing/how-shedworks-refined-the-art-of-sable-in-pursuit-of-readability)
- Outlines are a "really useful tool" for depth, scale and texture; they fade in opacity with distance, which also hides object pop-in. **[fetched]** — [Game Developer](https://www.gamedeveloper.com/marketing/how-shedworks-refined-the-art-of-sable-in-pursuit-of-readability)
- Distance fog is tuned per biome and drives the day and night palette. **[fetched]** — [Game Developer](https://www.gamedeveloper.com/marketing/how-shedworks-refined-the-art-of-sable-in-pursuit-of-readability)
- Why this style: it had to be quick to produce, quick to iterate on, consistent and distinctive for a very small team; the desert was chosen because a dense world was not feasible. **[fetched]** — [Game Developer](https://www.gamedeveloper.com/marketing/how-shedworks-refined-the-art-of-sable-in-pursuit-of-readability)
- Shedworks was a two-person studio working from a garden shed in North London; Moebius is the main named influence, with Studio Ghibli and architect Carlo Scarpa also cited. **[snippet]** — [Cook and Becker, 2019](https://www.cookandbecker.com/en/article/170/exploration-through-line-art.html)
- The look depends on post-processing that cannot be previewed in Maya, so assets are only judged in-engine. **[snippet]** — [Creative Bloq](https://www.creativebloq.com/how-to/mix-procreate-and-unity-to-make-game-art-sable)
- Community recreations use posterised two-tone shading with Sobel edge detection for the lines. **[snippet]** — [Maxime Heckel, Moebius-style post-processing](https://blog.maximeheckel.com/posts/moebius-style-post-processing)

Hohokum:

- Described as Richard Hogg's "slightly wonky vector style"; a "jolly riot of colour" with a deliberately bittersweet edge. Hogg: "Some of my favourite parts of the game are ones that are a little bit sad, or depressing, almost." **[fetched]** — [Grafik, Anna Lisa Reynolds, 3 Nov 2014](https://grafik.net/game-changer)
- Process was "very emergent, ad-hoc"; Sony mostly removed "the more videogame-y ideas". **[fetched]** — [Grafik](https://grafik.net/game-changer)

Wilmot's Warehouse:

- Hogg drew "hundreds of square tiles representing different things" before any game existed, then tuned difficulty by editing the image set. **[fetched]** — [Game Developer deep dive, written by Richard Hogg, 23 Oct 2019](https://www.gamedeveloper.com/design/game-design-deep-dive-the-creative-camaraderie-behind-i-wilmot-s-warehouse-i-)
- Grouping rules: some tiles form "clear groups, linked by color or some kind of obvious motif", some share "oblique, esoteric connections", and "Inconsistencies and contradictions were embraced and nurtured." **[fetched]** — [Game Developer](https://www.gamedeveloper.com/design/game-design-deep-dive-the-creative-camaraderie-behind-i-wilmot-s-warehouse-i-)
- Over five hundred stock types; design questions were answered by asking "what happens in a real warehouse?" **[snippet]** — [Game Developer, Road to the IGF](https://gamedeveloper.com/business/road-to-the-igf-richards-hogg-haggett-s-i-wilmot-s-warehouse-i-)
- The icons had been doodled for a different project; Ricky Haggett built the prototype from them over a Christmas break. **[snippet]** — [Epic Games Store feature](https://store.epicgames.com/news/hollow-ponds-talk-about-their-journey-from-stocking-shelves-to-launching-wilmot-works-it-out); prototype detail **[fetched]** — [Game Developer](https://www.gamedeveloper.com/design/game-design-deep-dive-the-creative-camaraderie-behind-i-wilmot-s-warehouse-i-)

Chicory:

- Lobanov: "Once we settled into an art style it wasn't too hard to just make everything in black and white. I have to say it was hardest on the UI." **[snippet]** — [Sportskeeda interview](https://sportskeeda.com/esports/news-something-personal-meaningful-greg-lobanov-talks-creativity-imagination-chicory-a-colorful-tale)
- Each screen reads as a monochrome page with heavy outlines, compared by a reviewer to adult colouring books. **[snippet]** — [VideoGamesGood review](https://www.videogamesgood.com/post/review-chicory-colorful-tale-paints-masterful-picture)
- Character consistency method: Alexis Dean-Jones checks every new design against one large file holding all existing characters (about sixty) to confirm it "fits in with the world"; proportions and scale were set from the main character first. Tools: Clip Studio Paint, Adobe Animate. **[fetched]** — [Wacom Community](https://community.wacom.com/en-pe/designing-chicorys-creatures-with-alexis-dean-jones)

Gris:

- Conrad Roset is a watercolour and ink illustrator whose gallery style (simple lines, delicate forms, watercolour washes) carried directly into the game. **[snippet]** — [Beautiful Bizarre](https://beautifulbizarre.net/conrad-roset-illustrative-paintings/)

#### 1.5 Hand-drawn and paper

Reference: Paper Mario (Intelligent Systems, 2000), Cuphead (Studio MDHR, 2017), Hollow Knight (Team Cherry, 2017), Night in the Woods (Infinite Fall, 2017), A Short Hike (Adam Robinson-Yu, 2019), Tunic (Andrew Shouldice, 2022).

Cuphead (1930s rubber hose):

- Every frame was drawn on paper first, then inked on paper (not on cels), then coloured digitally; a cel test made little visible difference and digital colour saved significant time. The team estimates more than 60,000 frames. **[fetched]** — [Game Developer, interview with Chad Moldenhauer, 1 Nov 2017](https://www.gamedeveloper.com/art/how-i-cuphead-i-nailed-the-look-and-feel-of-classic-1930s-cartoons)
- Imperfection is a rule: line weight and taper vary frame to frame as in period cartoons ("nothing was perfect"); the whole image is slightly blurred to mimic soft film focus; grain and scratches are "actually scanned from film, it's not digital." **[fetched]** — [Game Developer](https://www.gamedeveloper.com/art/how-i-cuphead-i-nailed-the-look-and-feel-of-classic-1930s-cartoons)
- Backgrounds are watercolour paintings. **[snippet]** — [GameSpot](https://www.gamespot.com/articles/how-cupheads-devs-gambled-on-a-dream/1100-6454860/)

Night in the Woods:

- Scott Benson is a self-taught animator and illustrator whose earlier motion work was built almost entirely from After Effects shape layers ("Just about everything onscreen is a humble shape layer"), with only texture overlays added. This is the best sourced evidence for the flat-shape construction; it describes his short "The Murf", not the game pipeline. **[snippet]** — [Motionographer, 7 Sep 2011](https://motionographer.com/2011/09/07/scott-benson-rendezvous-the-murph-interview/)
- Engine: Unity. Richard Scarry is listed as an influence on Benson's work on the game. **[snippet]** — [Wikipedia mirror](https://wiki.krisyotam.com/content/wikipedia_en_all_nopic_2026-03/Gregg_Lee)
- Edge credits Night in the Woods as an influence on Thank Goodness You're Here, "especially its willingness to switch compositions". **[snippet]** — [Edge, 30 Nov 2023](https://www.pressreader.com/australia/edge/20231130/282226605469845)

A Short Hike (low-resolution 3D):

- Robinson-Yu: "3D games have been working to hide pixels as much as possible"; "I wanted to see if I could make a beautiful (and readable) 3D world using as few pixels as possible." **[fetched]** — [PlayStation Blog](https://blog.playstation.com/?p=351732)
- "I feel like the low-resolution can help the world feel lush, and let your imagination fill in the details." **[fetched]** — [PlayStation Blog](https://blog.playstation.com/?p=351732)
- Rules: flat cohesive shading, no anti-aliasing, a soft outline on objects so they stay readable at low resolution; pixel size is a player option because some players disliked the chunkiness. **[fetched]** — [PlayStation Blog](https://blog.playstation.com/?p=351732)
- Palette sampled from autumn photographs of the Canadian Shield. **[snippet]** — [Uppercut](https://uppercutcrit.com/how-a-short-hike-captures-the-feeling-of-fall/)
- Technique: render to a small texture, then scale up with point filtering through a second camera. **[snippet]**, secondary transcript of the GDC talk — [Glasp](https://glasp.co/youtube/ZW8gWgpptI8)

Tunic:

- Shouldice: "The original intent was to develop a really simple and straightforward art style that would be visually cohesive, and easy to build on"; "It took a lot of iteration." **[snippet]** — [TheXboxHub interview](https://www.thexboxhub.com/the-tunic-interview-an-exclusive-chat-with-polymath-designer-andrew-shouldice/)

Paper Mario:

- Started in 1996 as Super Mario RPG 2; the team struggled with the move from sprites to polygons, rejected a polygon approach, and landed on flat 2D characters in 3D backgrounds. **[snippet]** — [The Avocado, Franchise Festival](https://the-avocado.org/2021/05/28/franchise-festival-101-paper-mario/?amp=1); developer interviews at [shmuplations](https://shmuplations.com/?p=8702)

Hollow Knight:

- Characters are "relatively clean and simple" against complex backgrounds, in "a mostly monotone dark color palette". **[snippet]**, reviewer description — [Wikipedia mirror, Ari Gibson](https://cavac.at/cavacopedia/Ari%20Gibson)

#### 1.6 Retro 3D and hybrid

Reference: PS1 revival (Crow Country, SFB Games, 2024), HD-2D (Octopath Traveler, Square Enix and Acquire, 2018), Eastward (Pixpil, 2021), Signalis (rose-engine, 2022), The Last Night (Odd Tales, unreleased).

Signalis:

- Alex Zwerger: "One way we do this is by strictly sticking to a 640 x 360 pixel resolution. Everything in the game is rendered at this resolution before it's upscaled to final game resolution." The look mixes low-poly 3D models with 2D sprites. **[snippet]**, page returned 404 when opened — [Indie Graze interview](https://indiegraze.com/?p=989)

Eastward:

- Pipeline: base pixel art in Aseprite, split into layers by structure (a roof and its wall are separate), rebuilt in a 3D scene, with a bump map hand-painted for each asset so it lights correctly. The developers call it "a 3D game with a 2D perspective". **[fetched]** — [Game Developer, Bryant Francis, 11 Oct 2021](https://www.gamedeveloper.com/art/eastward-s-creators-share-insights-on-making-pixel-art-adventures)
- Fog layers and light shafts carry time of day and weather. The fixed top-down camera means level layout must stop the player being hidden behind scenery; stairs and height changes are used for density. **[fetched]** — [Game Developer](https://www.gamedeveloper.com/art/eastward-s-creators-share-insights-on-making-pixel-art-adventures)
- Development took more than six years. **[fetched]** — [Game Developer](https://www.gamedeveloper.com/art/eastward-s-creators-share-insights-on-making-pixel-art-adventures)

HD-2D:

- Definition: pixel-art billboard sprites in fully 3D environments with detailed textures and dynamic shading; Square Enix holds the trademark on the name, not the style. **[snippet]** — [Wikipedia, HD-2D](https://en.wikipedia.org/wiki/HD-2D)
- Producer Masashi Takahashi: an all-pixel version "felt fake and low-quality", which is why the 3D environment and effects were added. **[snippet]** — [Twinfinite, quoting Game Informer](https://twinfinite.net/features/dear-square-enix-octopath-traveler-is-how-every-nostalgic-jrpg-should-look/)
- Modern lighting, depth of field and particles produce a diorama look. **[snippet]** — [Unreal Engine spotlight, 25 Oct 2019](https://www.unrealengine.com/en-US/spotlights/octopath-traveler-s-hd-2d-art-style-and-story-make-for-a-jrpg-dream-come-true)

PS1 revival:

- Signature artefacts: visible pixels, wobbling geometry from low-precision vertex snapping, warped textures from affine mapping, short draw distance hidden by fog or darkness. **[snippet]** — [GamesRadar](https://www.gamesradar.com/exploring-the-resurgence-of-the-low-fi-3d-visual-style-of-the-ps1-era)
- Crow Country's characters resemble Final Fantasy VII field models because the developer began without modelling tools and built figures from spheres and capsules. **[snippet]** — [Stealth Optional](https://stealthoptional.com/news/crow-country-horror-game-mixes-ps1-final-fantasy-vii-resident-evil/)
- Dissent: former Final Fantasy programmer Koji Sugimoto has criticised deliberate recreation of affine warping, which his generation worked to remove. **[snippet]** — [Automaton](https://automaton-media.com/en/news/final-fantasy-x-programmer-doesnt-get-why-devs-want-to-replicate-low-poly-ps1-era-games-we-worked-so-hard-to-avoid-warping-but-now-they-say-its-charming/)

The Last Night:

- Hand-drawn pixel sprites placed in 3D space with modern lighting, post effects and 3D camera work; every element hand-drawn, down to non-repeating floor tiles. **[snippet]** — [Famitsu, 22 Dec 2017](https://www.famitsu.com/news/201712/22148711.html); [4Gamer, 16 Jun 2017](https://www.4gamer.net/games/385/G038505/20170616108/)

#### 1.7 Retro computer and interface aesthetics

Reference: Hypnospace Outlaw (Tendershoot / Jay Tholen, 2019), Emily is Away (Kyle Seeley, 2015), Papers, Please (Lucas Pope, 2013), Kingsway (Andrew Morrish, 2017), Stone Story RPG (Martian Rex / Gabriel Santos, early access 2019), Dwarf Fortress (Bay 12 Games, 2006).

Hypnospace Outlaw (1990s web):

- Many graphics were reduced to a "Hypnospace-safe" palette using Floyd-Steinberg dithering; audio was compressed to 64 kbps with a 1999-era MP3 encoder. **[fetched]** — [Game Developer, Joel Couture, 8 Feb 2019](https://www.gamedeveloper.com/business/road-to-the-igf-tholen-lasch-nelson-jr-and-cochran-s-i-hypnospace-outlaw-i-)
- When processing made things hard to tell apart, the team "erred on the side of readability". **[fetched]** — [Game Developer](https://www.gamedeveloper.com/business/road-to-the-igf-tholen-lasch-nelson-jr-and-cochran-s-i-hypnospace-outlaw-i-)
- Tholen wrote a "design bible" covering art, audio and writing to keep a deliberately rough, mixed-quality world cohesive. **[fetched]** — [Game Developer](https://www.gamedeveloper.com/business/road-to-the-igf-tholen-lasch-nelson-jr-and-cochran-s-i-hypnospace-outlaw-i-)
- Tools: GIMP, Krita, Aseprite, Bryce 5.5, Wings 3D, SketchUp, CorelDraw, PageMaker; built in Construct 2. **[fetched]** — [Game Developer](https://www.gamedeveloper.com/business/road-to-the-igf-tholen-lasch-nelson-jr-and-cochran-s-i-hypnospace-outlaw-i-)
- The operating-system art draws from a custom 20-colour palette; pre-rendered 3D GIFs were converted to a 64-colour version. **[snippet]** — [TechRaptor interview](https://techraptor.net/content/indie-interview-hypnospace-outlaw); [PC PowerPlay, 13 May 2019](https://www.pressreader.com/australia/pcpowerplay/20190513/281530817456717)
- No real brands or celebrities appear; genres and movements are invented. Tholen: "This game isn't for people who grew up in the 1990s." **[fetched]** — [Game Developer](https://www.gamedeveloper.com/business/road-to-the-igf-tholen-lasch-nelson-jr-and-cochran-s-i-hypnospace-outlaw-i-)

Emily is Away and Kingsway:

- Emily is Away imitates a Windows XP chat client modelled on early-2000s ICQ and AIM. **[snippet]** — [Wikipedia](https://www.wikipedia.org/wiki/Emily_Is_Away)
- Kingsway maps RPG mechanics onto a Windows 95-style desktop; Morrish found players needed little instruction because they already understood operating-system interfaces. **[snippet]** — [Wikipedia mirror, Kingsway](https://wiki.riteme.site/wiki/Kingsway_(video_game))

Papers, Please:

- Pope calls it a "design first project" that "wasn't really art-focused", in contrast to Obra Dinn, where he started with the visuals. **[snippet]** — [Game Developer](https://gamedeveloper.com/design/for-lucas-pope-i-return-of-the-obra-dinn-i-was-a-bunch-of-appealing-design-problems)

Home computer palettes:

- ZX Spectrum: 8 base colours with a bright variant (15 distinct), colour stored per 8×8 attribute cell with only two colours per cell, which produces attribute clash. **[snippet]** — [Wikipedia, Attribute clash](https://www.wikipedia.com/wiki/Attribute_clash)
- Commodore 64: hires mode uses 8×8 attribute cells, multicolour mode 4×8 cells. **[snippet]** — [bitmapped, Attribute clash](https://martink-rsa.github.io/bitmapped/concepts/attribute-clash)
- Teletext: 40×25 character cells; block graphics are 2×3 mosaics per cell (64 patterns); a colour change costs one blank cell, so differently coloured blocks cannot normally touch. **[snippet]** — [RISC OS teletext documentation](https://www.riscos.com/support/developers/riscos6/graphics/teletext.html)

ASCII and text mode:

- Stone Story RPG: Gabriel Santos typed more than 10,000 frames of ASCII animation frame by frame in a plain text editor, rendered in Unity through custom shaders; the idea came from the browser game Candy Box. **[snippet]** — [Wikipedia](https://en.wikipedia.org/wiki/Stone_Story_RPG); [Indienova interview](https://indienova.com/en/indie-game-news/stone-story-rpg-dev-interview/)

#### 1.8 Diorama and isometric miniatures

Reference: Unpacking (Witch Beam, 2021), Townscaper (Oskar Stålberg, 2021), Habbo Hotel (Sulake, 2000), eBoy pixoramas (Kai Vermehr, Steffen Sauerteig, Svend Smital, from 1997).

- Unpacking, Wren Brier: "We decided to go with an isometric style because it lent itself well to the grid-based gameplay we had in mind." She had never made isometric art before and called it "a steep learning curve". **[fetched]** — [Game Developer, Chris Kerr, 16 Nov 2021](https://www.gamedeveloper.com/design/intimacy-from-the-inanimate-in-house-moving-puzzler-unpacking)
- Unpacking workflow: each room greyboxed in Aseprite with grids marking where items can sit; furniture split into pieces for depth and rebuilt in Unity; 35 rooms. **[fetched]** — [Game Developer](https://www.gamedeveloper.com/design/intimacy-from-the-inanimate-in-house-moving-puzzler-unpacking)
- Unpacking's scale was set by how small a mug could be drawn and still read as a mug; over 1,000 items. **[snippet]**, first claim from a mirror of an unidentified article — [mirror](https://eugames.pages.dev/posts/how-unpacking-s-art-combines-beauty-with-clarity); item count from [GCAP 2021 session listing](https://gcap2021.sched.com/event/mGZX/cohesion-is-key-art-direction-for-indies)
- Isometric pixel art convention: lines step 2 px across for 1 px up (about 26.5 degrees), because a true 30 degree line produces an uneven stair pattern. **[snippet]** — [Slynyrd Pixelblog 41](https://www.slynyrd.com/blog/2022/11/28/pixelblog-41-isometric-pixel-art); [Pixel Parmesan](https://pixelparmesan.com/fundamentals-of-isometric-pixel-art/)
- Townscaper: Stålberg describes the palette as a rainbow set plus a couple of greys and white; buildings are assembled from hand-made pieces by a wave function collapse solver. **[snippet]** — [MCV, When We Made Townscaper](https://mcvuk.com/business-news/when-we-made-townscaper); [XR AI Spotlight interview](https://xraispotlight.substack.com/p/how-to-make-procedural-generation)

#### 1.9 Notable 2023 to 2026 releases

- Animal Well (Billy Basso, 2024): rendered at 320×180. Basso says it "truly did look like an NES game" early on, then gained "more and more rendering systems": normal-mapped backgrounds with "a ton of dynamic lighting stuff", and a fluid simulation layer for water and smoke that sprites can draw into. He treats pixel art as "sort of native to the medium of video games" and deliberately avoided squash and stretch and screen shake. **[fetched]** — [Game Developer, Chris Kerr, 22 Feb 2022](https://www.gamedeveloper.com/art/creature-feature-the-surreal-pixel-art-and-animation-of-animal-well)
- MOUSE: P.I. For Hire (Fumi Games, 2026): pillars fixed early as dark, noir, black and white, rubber hose. All art was made in greyscale. Without colour as a cue, "We had to rely more on lighting", foreground and background were separated strongly so interactive props stand out, and wall decals (footprints) replace the usual painted markers because "we can't really paint over anything". **[fetched]** — [Final Weapon, interview with Mateusz Michalak and Mateusz Lechowski, 8 Sep 2026](https://finalweapon.net/2026/09/08/interview-mouse-pi-for-hire-devs-on-the-challenges-of-black-and-white/). Announced launch date 19 March 2026. **[snippet]** — [GamingTrend](https://gamingtrend.com/news/mouse-p-i-for-hire-will-release-march-19-2026/); another outlet lists 16 April 2026 **[snippet]** — [Insider Gaming](https://insider-gaming.com/mouse-pi-for-hire-release-date-times/)
- Thank Goodness You're Here (Coal Supper, 2024): a Yorkshire studio "focusing on playful hand-drawn experiences"; cited influences are Reeves and Mortimer, Aardman and Night in the Woods, with Simpsons-style sign gags. **[snippet]** — [Game Republic](https://gamerepublic.net/?p=8322); [Edge, 30 Nov 2023](https://www.pressreader.com/australia/edge/20231130/282226605469845)
- Crow Country (SFB Games, 2024): PS1-style survival horror, covered in 1.6.

### Inferences

All items here are **observation**.

- The rule sets that survive a move to a 640×360 top-down canvas are the ones that are about colour count, line and shape, because those are resolution-independent decisions. The rule sets that are about rendering (depth of field, vertex wobble, sphere-mapped dither, distance fog, real film grain) either need a 3D pipeline or need to be faked as overlays.
- A workable 1-bit rule set for this project can be lifted almost directly from Pope plus Playdate: two colours only; every object is solid black or solid white first; outlines everywhere and inverted against their ground; dither used for at most one or two mid-tones and never on small moving sprites; no dithered surface scrolls by an odd number of pixels; strokes at least 2 px; characters at least 32 px (the project's 64 px characters are comfortably above this); body text cap height 12 to 14 px.
- Obra Dinn's hard problem (dither that swims under a moving 3D camera) does not exist in a 2D top-down game with pre-drawn tiles. The remaining 2D version of the problem is scroll shimmer, which Playdate's even-pixel scrolling rule addresses.
- Game Boy rules translated to this canvas: four shades total, 8×8 tile discipline, sprites using three shades. 160×144 scaled ×2 is 320×288, which fits inside 640×360 with side borders; a faithful version would letterbox, a loose version would keep the palette and tile discipline at the full canvas. A 64 px character is four Game Boy actors tall, so the result reads as "Game Boy palette" rather than "Game Boy game".
- PICO-8 translated: the 16-colour palette is the recognisable part; 128×128 is too small a field for 64 px characters (a character would be half the screen height), so only the palette and chunky pixel scale transfer.
- A flat-shape rule set in the Night in the Woods and Sable family, as it would be written for this project: no outlines or a single uniform-weight line (choose one and never mix), one flat fill per surface, one flat shadow tone per surface, cast shadows under every character for grounding (Sable's reason), a palette fixed per room or per time of day, and geometry simplified to circles, rounded rectangles and triangles. At 64 px tall, shapes this simple remain readable; at lower sizes ligne claire's uniform line starts to consume the character.
- Wilmot's Warehouse is effectively already a top-down game on a square grid with flat-colour icon tiles, so it is the closest existing proof that an abstract flat style works for a top-down work-themed game.
- The interface styles (Hypnospace, Kingsway, Emily is Away) are not ways of drawing a room; they are frames. They translate to this project as chrome around or over the top-down view: windows, title bars, dialogs, cursors, system fonts.
- Cuphead's rules (per-frame hand inking, film grain, soft focus) are about high-resolution line quality and frame count. At 640×360 the line wobble that sells the style is below the pixel grid, so what would survive is only the shape language (pie eyes, tube limbs, gloves) and a greyscale or sepia palette.
- Relative difficulty for a solo developer, easiest first: Thomas Was Alone or Mini Metro abstraction; 1-bit sprite art (Minit, Gato Roboto); fixed-palette handheld styles; flat-shape illustration; isometric pixel dioramas; lit pixel art (Eastward, Animal Well); frame-by-frame hand-drawn (Cuphead, Hollow Knight). The cited evidence behind this ordering: Thomas Was Alone was a 24-hour prototype, Celeste Classic four days, Gato Roboto chose 1-bit to save asset time, Brier found isometric a steep learning curve, Eastward took six years with hand-painted bump maps per asset, Cuphead needed 60,000 frames.

### Gaps

- Lucas Pope's TIGSource dithering devlog could not be opened (HTTP 403 at https://forums.tigsource.com/index.php?topic=40832.msg1363742). The dithering findings come from Pope's own PlayStation Blog article and press coverage. The sphere-mapping detail is from a PC Gamer snippet only.
- Night in the Woods: I found no primary source for the specific rules in the brief (flat shapes, no outlines, strict autumn palette). Benson's GDC 2018 talk and the Unwinnable feature "The Making of a Weird Autumn" (HTTP 403) are the likely sources. The rules as stated in the brief match what the game looks like but are unsourced here.
- Ligne claire as a formal rule set (uniform line weight, flat colour, no hatching) is not stated in any Sable source I opened; the Game Developer report covers outlines but not line weight.
- No primary creator statements found for Alto's Adventure, Old Man's Journey, Saturnalia, Gris (beyond artist background), Hollow Knight's drawing process, Inside's colour rules, Habbo Hotel's house style, eBoy's method, Dwarf Fortress, CGA and EGA specifics, Vectrex, or Lospec palette jams. These are named in the brief but remain uncovered.
- Downwell: no primary statement from Ojiro Fumoto on why the palette is restricted; sources disagree on whether it is three colours or four.
- Signalis's 640×360 statement is from a search snippet of an interview page that returned 404 when opened.
- Cuphead's frame rate (often stated as 24 fps) was not confirmed by any reliable source found.
- Release years in the reference lines were not individually sourced.

---

## Key question 2: Which of these styles have been done at low resolution or in pixel form, and with what results?

### Takeaway

Several of the most distinctive non-mainstream looks were built at or near this project's resolution: Obra Dinn was prototyped at 640×360 and shipped at 800×450, Signalis renders everything at 640×360, Animal Well at 320×180 (exactly half), Playdate at 400×240, and A Short Hike is a deliberately low-resolution 3D render. The recurring result is that the style holds but legibility has to be bought back with outlines, larger sprites and restrained dithering, and that some players reject very chunky pixels.

### Cited Findings

- Obra Dinn at 640×360 worked in a small window but was uncomfortable fullscreen on a large monitor; Pope raised it to 800×450 and stabilised the dither before shipping. **[fetched]** — [PlayStation Blog](https://blog.playstation.com/archive/2019/10/17/lucas-pope-on-return-of-the-obra-dinns-art-style)
- In Obra Dinn, faces only work up close, "the only way there are enough pixels for dithering to work"; Pope said the restrictions were "working directly against the game mechanics." **[fetched]** — [Game Developer, 2015](https://www.gamedeveloper.com/design/lucas-pope-and-the-rise-of-the-1-bit-dither-punk-aesthetic)
- Above roughly 720p, 1-bit dither blends into grey and the style disappears. **[fetched]** — [Game Developer, 2015](https://www.gamedeveloper.com/design/lucas-pope-and-the-rise-of-the-1-bit-dither-punk-aesthetic)
- Signalis is rendered strictly at 640×360 and upscaled, combining low-poly 3D with 2D sprites. **[snippet]** — [Indie Graze](https://indiegraze.com/?p=989)
- Animal Well renders at 320×180 and layers normal-mapped lighting and fluid simulation on top of simple pixel art; Basso notes a 4K display gives "144x more computing power to render each pixel." **[fetched]** — [Game Developer, 2022](https://www.gamedeveloper.com/art/creature-feature-the-surreal-pixel-art-and-animation-of-animal-well)
- A Short Hike: low-resolution 3D with flat shading, no anti-aliasing and a soft outline for readability; some players disliked the pixelation, so pixel size became an option. **[fetched]** — [PlayStation Blog](https://blog.playstation.com/?p=351732)
- Playdate's 400×240 1-bit guidance (32×32 sprites, 2 px strokes, 12 to 14 px text) exists because small sprites, thin lines and small text failed on the device. **[fetched]** — [Playdate](https://help.play.date/developer/designing-for-playdate/)
- Octopath Traveler: an all-pixel-art version "felt fake and low-quality" to its producer; the 3D environment and effects were the fix. **[snippet]** — [Twinfinite](https://twinfinite.net/features/dear-square-enix-octopath-traveler-is-how-every-nostalgic-jrpg-should-look/)
- Eastward keeps hand-drawn pixel art but lights it through hand-painted bump maps in a 3D scene. **[fetched]** — [Game Developer, 2021](https://www.gamedeveloper.com/art/eastward-s-creators-share-insights-on-making-pixel-art-adventures)
- The Siege and the Sandfox found normal maps work best on large shapes; the stronger the lighting effect, the more the "purity" of the pixel art was lost. **[snippet]** — [Game Developer](https://gamedeveloper.com/art/adding-depth-to-2d-with-hand-drawn-normal-maps-in-i-the-siege-and-the-sandfox-i-)
- Minit, Gato Roboto and Downwell are all low-resolution pixel games built on one-bit or near one-bit palettes; their developers report speed of iteration as the gain and clarity as the cost. **[fetched]** for Minit's limitation statement — [Game Developer](https://www.gamedeveloper.com/disciplines/road-to-the-igf-calis-nijman-kallio-and-johann-s-i-minit-i-); **[snippet]** for the clarity cost — [mirror](https://arucoppu.pages.dev/posts/minit-fun-racer-devs-discuss-the-fun-and-challenge-of-making-the-game)
- World of Horror was drawn at low resolution in MS Paint in 1-bit and 2-bit. **[snippet]** — [Engadget](https://www.engadget.com/2019/09/20/world-of-horror-junji-ito-hp-lovecraft-hypercard-game/)
- Unpacking is isometric pixel art whose scale was set by the smallest recognisable mug. **[snippet]** — [mirror](https://eugames.pages.dev/posts/how-unpacking-s-art-combines-beauty-with-clarity)
- Hypnospace Outlaw reproduces low-resolution, low-colour 1990s web graphics through palette reduction and Floyd-Steinberg dithering. **[fetched]** — [Game Developer, 2019](https://www.gamedeveloper.com/business/road-to-the-igf-tholen-lasch-nelson-jr-and-cochran-s-i-hypnospace-outlaw-i-)
- Stone Story RPG renders hand-typed ASCII frames through shaders. **[snippet]** — [Wikipedia](https://en.wikipedia.org/wiki/Stone_Story_RPG)

### Inferences

All **observation**.

- 640×360 is a proven canvas for exactly the styles in question: it is Obra Dinn's prototype resolution and Signalis's shipping resolution, and it is an integer multiple of Animal Well's. Pope's fullscreen discomfort was specific to high-contrast 1-bit dither covering the whole screen; a browser game shown in a window or with integer scaling is closer to the "small window" case he said worked.
- Styles that will not survive the translation without a 3D renderer: HD-2D (depends on depth of field, perspective camera and volumetric light), PS1 revival (the signature is vertex wobble and texture warp on moving 3D geometry), Monument Valley (impossible geometry needs a 3D isometric camera; only its palette and "little world on negative space" composition transfer), Tunic and A Short Hike (the charm is a 3D world seen through low resolution), Townscaper (procedural 3D), Inside (3D lighting and depth).
- Styles that depend on high resolution and would not survive at 640×360: Cuphead (line wobble, grain and soft focus), Gris (watercolour gradients and fine line), Hollow Knight (fine hand-drawn line and soft glows), Old Man's Journey (textured illustration), Sable's fine distant linework (though its flat fills and near-field outline survive).
- Styles that survive or improve at 640×360 in 2D: 1-bit with outlines, Game Boy and PICO-8 palettes, Downwell's black plus white plus one accent colour, flat-shape illustration without gradients (Night in the Woods, Wilmot's Warehouse, Hohokum-like wonky vector), Chicory-style thick black line on white (needs a line of 2 px or more), Limbo-style silhouette (trivial in 2D but removes the detail a portfolio needs to show), ASCII and teletext grids, desktop-interface chrome, and isometric pixel dioramas (though isometric conflicts with a top-down or three-quarter camera already in use).
- Lit pixel art in the Eastward and Animal Well manner is achievable in a 2D canvas with normal maps and a WebGL shader, but it is a rendering feature added to pixel art, so it sits closer to "mainstream pixel art, upgraded" than to a different style, and it multiplies asset work (one extra map per asset).
- A teletext version fits the canvas neatly: 40 columns of 16 px is exactly 640 px wide, and 16 px rows give 22 full rows in 360 px (teletext proper has 25). A 2×3 mosaic per cell gives an effective 80×66 block grid, which is too coarse for 64 px characters to carry detail, so teletext works as a screen or menu treatment, not as the main world.

### Gaps

- No source found that documents a ligne claire or Moebius look executed as low-resolution pixel art by a named developer.
- No source found for a Night in the Woods-like flat style executed at 640×360; the claim that it survives is inference.
- Signalis's resolution statement needs a working link.
- I did not find player-reception data (reviews, sales) broken down by art style, so "with what results" is answered only through creator testimony.

---

## Key question 3: Which styles suit a career or office themed, humorous, personal portfolio game, and which evoke a specific era of computing or design that matches a web developer's history (1990s to 2020s)?

### Takeaway

The sourced evidence points to two groups: styles already used for work-themed or comedic games (Wilmot's Warehouse, Papers Please, Unpacking, Thank Goodness You're Here, Night in the Woods, Hypnospace Outlaw), and styles that are a recognisable piece of computing history (Mac Plus 1-bit, Game Boy, 1990s web, Windows 95 and XP interfaces). Matching an era to each stage of a web developer's career is my inference, but the anchor dates and the creators' stated intent support it.

### Cited Findings

Work and personal-history themes already carried by these styles:

- Wilmot's Warehouse is a game about stocking and categorising a warehouse; its flat icon tiles were designed around the question "what happens in a real warehouse?" **[snippet]** — [Game Developer, Road to the IGF](https://gamedeveloper.com/business/road-to-the-igf-richards-hogg-haggett-s-i-wilmot-s-warehouse-i-)
- Unpacking tells a life story through possessions placed in rooms; Game Developer titled its interview "Intimacy from the inanimate". **[fetched]** — [Game Developer, 2021](https://www.gamedeveloper.com/design/intimacy-from-the-inanimate-in-house-moving-puzzler-unpacking)
- Papers, Please grew from a prototype of moving documents around a desk. **[snippet]** — [Denfaminicogamer interview](https://news.denfaminicogamer.jp/interview/240424b)
- Kingsway shows that players immediately understand a game presented as a desktop operating system. **[snippet]** — [Wikipedia mirror](https://wiki.riteme.site/wiki/Kingsway_(video_game))
- Minit's team ties minimal art to humour and personality carried by small details such as a single line of NPC dialogue. **[fetched]** — [Game Developer, 2019](https://www.gamedeveloper.com/disciplines/road-to-the-igf-calis-nijman-kallio-and-johann-s-i-minit-i-)
- Thank Goodness You're Here is a hand-drawn comedy whose jokes sit in sign gags and incidental dialogue, with British comedy and Night in the Woods as influences. **[snippet]** — [Edge, 30 Nov 2023](https://www.pressreader.com/australia/edge/20231130/282226605469845)
- Hohokum's bright wonky vector look was deliberately paired with a "slightly bittersweet" tone. **[fetched]** — [Grafik, 2014](https://grafik.net/game-changer)
- Thomas Was Alone's rectangles were read as more "artistic and edgy" than intended; Bithell says the minimal art was a budget and skill decision. **[snippet]** — [NME, 2023](https://www.nme.com/features/boss-level-2023-mike-bithell-3432006)

Era anchors:

- Mac Plus: 9 inch black and white display, 512×342 square pixels; the direct reference for Obra Dinn. **[fetched]** — [PlayStation Blog](https://blog.playstation.com/archive/2019/10/17/lucas-pope-on-return-of-the-obra-dinns-art-style)
- Pope and the Rogue Invader team doubted 1-bit would become a broad trend because developer nostalgia for 8-bit and 16-bit consoles is stronger than for early Macs. **[fetched]** — [Game Developer, 2015](https://www.gamedeveloper.com/design/lucas-pope-and-the-rise-of-the-1-bit-dither-punk-aesthetic)
- Hypnospace Outlaw's subject, per Tholen, is the period when computers became accessible to everyday people "but before the homogenization of the social media era"; the network is described as a mix of GeoCities and MySpace. **[snippet]** — [Game Developer, 2019](https://www.gamedeveloper.com/business/road-to-the-igf-tholen-lasch-nelson-jr-and-cochran-s-i-hypnospace-outlaw-i-)
- Tholen's references include 3D fly-throughs in 1990s dot-com adverts and the disappointment of dial-up. **[fetched]** — [Game Developer, 2019](https://www.gamedeveloper.com/business/road-to-the-igf-tholen-lasch-nelson-jr-and-cochran-s-i-hypnospace-outlaw-i-)
- Tholen on audience: "This game isn't for people who grew up in the 1990s", which is why no real brands appear. **[fetched]** — [Game Developer, 2019](https://www.gamedeveloper.com/business/road-to-the-igf-tholen-lasch-nelson-jr-and-cochran-s-i-hypnospace-outlaw-i-)
- Emily is Away: Windows XP desktop with an AIM and ICQ style chat client from the early 2000s, including away messages and buddy info. **[snippet]** — [Wikipedia](https://www.wikipedia.org/wiki/Emily_Is_Away); [Trend Hunter](https://www.trendhunter.com/trends/emily-is-away)
- Kingsway: Windows 95-style interface. **[snippet]** — [Wikipedia mirror](https://wiki.riteme.site/wiki/Kingsway_(video_game))
- PICO-8 (2015): a fantasy console whose 16-colour palette references the Commodore 64 and whose sound references Amiga trackers. **[snippet]** — [Wikipedia](https://en.wikipedia.org/wiki/PICO-8)
- ZX Spectrum and teletext constraints (attribute cells, 40×25 text grid) are documented hardware facts usable as period signatures. **[snippet]** — [Wikipedia, Attribute clash](https://www.wikipedia.com/wiki/Attribute_clash); [RISC OS teletext documentation](https://www.riscos.com/support/developers/riscos6/graphics/teletext.html)

### Inferences

All **observation**. Hardware and software dates below are from general knowledge, not from sources opened in this pass.

- Best fits for a humorous office or career game, in my judgement:
  - Flat-shape illustration (Night in the Woods, Wilmot's Warehouse, Hohokum family). Friendly, reads as editorial and tech-industry illustration, carries deadpan humour well, and the simple shapes suit 64 px characters.
  - Desktop-interface framing (Kingsway, Emily is Away, Hypnospace). A web developer's actual workplace is a screen, so OS chrome is on-theme, cheap to produce, and funny through familiarity.
  - 1-bit with an accent colour (Minit, Downwell, Gato Roboto). Strong identity, fast to draw, and Minit shows it supports comedy; the risk is that portfolio content (screenshots of real projects) would have to be shown in colour inside a monochrome world, which could be turned into a feature.
  - Colouring-book line art (Chicory). Black line on white is office-stationery adjacent (whiteboard, sticky note, wireframe), and colour can be used as a reward or progress signal.
- Weaker fits: Limbo and Inside silhouettes, Signalis, World of Horror and PS1 horror (their creators chose the constraints to produce dread); Cuphead and Gris (resolution dependent); HD-2D (earnest, epic register and 3D dependent).
- An era-per-career-stage mapping a web developer would recognise:
  - 1980s home computing prologue: ZX Spectrum or C64 attribute-cell colour, teletext, Mac Plus 1-bit.
  - Late 1980s to 1990s childhood gaming: Game Boy four shades.
  - Mid to late 1990s first web pages: Hypnospace-style web-safe palette, dithered GIFs, tiled backgrounds, bevelled Windows 95 chrome.
  - Early 2000s: Windows XP and instant-messenger chrome (Emily is Away), pixel-isometric web communities (Habbo Hotel, eBoy).
  - Late 2000s: glossy gradients and skeuomorphism (no game reference found in this pass).
  - 2013 onward: flat design (Monument Valley, Mini Metro, Alto's Adventure were released in the same years flat UI design took over mobile).
  - Late 2010s to 2020s: tech-company flat illustration (closest game reference: Night in the Woods, Wilmot's Warehouse), plus the retro-revival tools a developer would actually use today (PICO-8, GB Studio, Playdate).
- This mapping suggests one structural option the report writer may want to raise: a single consistent world style, with era styles used as per-room or per-chapter treatments or as interface frames. The project's recent commit history ("four style takes on the same room") suggests the room-level comparison is already being prototyped.
- Tholen's remark that the game is not for people who grew up in the 1990s is a useful caution: an era pastiche should be legible to a recruiter or client who never used the original, so invented or generic period detail is safer than in-jokes.

### Gaps

- No source found that directly evaluates art styles for portfolio or career-themed games; the suitability ranking is entirely inference.
- No game reference found for late-2000s glossy, skeuomorphic web design.
- Habbo Hotel and eBoy are named as early-2000s references from general knowledge; I found no primary source on their style rules.
- Dates for hardware and design eras are uncited.

---

## Key question 4: What do the creators say they avoided, and what production shortcuts made the style feasible for small teams?

### Takeaway

Across unrelated games the same pattern repeats: the constraint was chosen partly because the creator could not afford, or could not draw, the alternative, and then defended as a rule. The most reusable shortcuts are removing colour (faster asset creation and iteration), removing texture and shading (flat fills), writing the rules down (design bible, master character sheet), and drawing the asset set before designing the game around it.

### Cited Findings

What creators said they avoided:

- Pope: dithering wherever possible ("use it as little as possible"); stylised dither patterns that strayed from the original vision; outlines where long draw distances would clutter the view. **[fetched]** — [PlayStation Blog](https://blog.playstation.com/archive/2019/10/17/lucas-pope-on-return-of-the-obra-dinns-art-style)
- Playdate guidance: unedited machine dithering, 1 px strokes, 8×8 tiles, text under 8 px, runtime sprite rotation and scaling, one-pixel scrolling of checkerboard dither. **[fetched]** — [Playdate](https://help.play.date/developer/designing-for-playdate/)
- A Short Hike: anti-aliasing. **[fetched]** — [PlayStation Blog](https://blog.playstation.com/?p=351732)
- Animal Well: squash and stretch and screen shake, because Basso sees them in almost every indie game. **[fetched]** — [Game Developer, 2022](https://www.gamedeveloper.com/art/creature-feature-the-surreal-pixel-art-and-animation-of-animal-well)
- Cuphead: "the digital crispness we're used to"; digital grain (theirs is scanned film). **[fetched]** — [Game Developer, 2017](https://www.gamedeveloper.com/art/how-i-cuphead-i-nailed-the-look-and-feel-of-classic-1930s-cartoons)
- Hypnospace Outlaw: real brands, celebrities and historical figures; also true period codecs, which Tholen called "nightmarish" at the game's content volume. **[fetched]** — [Game Developer, 2019](https://www.gamedeveloper.com/business/road-to-the-igf-tholen-lasch-nelson-jr-and-cochran-s-i-hypnospace-outlaw-i-)
- Hohokum: "the more videogame-y ideas". **[fetched]** — [Grafik, 2014](https://grafik.net/game-changer)
- MOUSE: P.I. For Hire: colour-coded affordances such as painted yellow markers, because "we can't really paint over anything". **[fetched]** — [Final Weapon, 2026](https://finalweapon.net/2026/09/08/interview-mouse-pi-for-hire-devs-on-the-challenges-of-black-and-white/)
- Octopath Traveler: an all-pixel presentation, judged "fake and low-quality". **[snippet]** — [Twinfinite](https://twinfinite.net/features/dear-square-enix-octopath-traveler-is-how-every-nostalgic-jrpg-should-look/)
- Paper Mario: conventional polygon characters, tried and rejected. **[snippet]** — [The Avocado](https://the-avocado.org/2021/05/28/franchise-festival-101-paper-mario/?amp=1)
- Sable: a dense detailed open world, judged infeasible for the team; object pop-in, described as "ugly and a real problem" and hidden by fading outlines. **[fetched]** — [Game Developer, 2022](https://www.gamedeveloper.com/marketing/how-shedworks-refined-the-art-of-sable-in-pursuit-of-readability)

Production shortcuts:

- 1-bit simplifies rendering, shaders and texture memory, and makes a noir look achievable with broad lighting (Pope). **[fetched]** — [Game Developer, 2015](https://www.gamedeveloper.com/design/lucas-pope-and-the-rise-of-the-1-bit-dither-punk-aesthetic)
- 1-bit chosen specifically to save asset time (Gato Roboto). **[snippet]** — [Game Developer Q&A](https://gamedeveloper.com/design/q-a-exploring-the-design-of-cat-in-a-mech-metroidvania-i-gato-roboto-i-)
- Black and white lets new ideas be tested in minutes (Minit, JW Nijman). **[snippet]** — [mirror](https://arucoppu.pages.dev/posts/minit-fun-racer-devs-discuss-the-fun-and-challenge-of-making-the-game)
- MS Paint and a mouse as the entire art pipeline (World of Horror). **[snippet]** — [Engadget](https://www.engadget.com/2019/09/20/world-of-horror-junji-ito-hp-lovecraft-hypercard-game/)
- Rectangles instead of characters; no AI because the developer could not write it (Thomas Was Alone). **[snippet]** — [NME, 2023](https://www.nme.com/features/boss-level-2023-mike-bithell-3432006)
- A style that is "quick to produce, quick to iterate on, visually consistent", in a setting (desert) chosen for low density (Sable). **[fetched]** — [Game Developer, 2022](https://www.gamedeveloper.com/marketing/how-shedworks-refined-the-art-of-sable-in-pursuit-of-readability)
- Low-resolution rendering so a mostly solo developer could do the art himself and let "imagination fill in the details" (A Short Hike). **[fetched]** — [PlayStation Blog](https://blog.playstation.com/?p=351732)
- Digital colour over paper ink instead of painted cels, after a test showed no visible difference (Cuphead). **[fetched]** — [Game Developer, 2017](https://www.gamedeveloper.com/art/how-i-cuphead-i-nailed-the-look-and-feel-of-classic-1930s-cartoons)
- Batch processing art through a fixed palette and dither instead of authoring in period software; a written design bible to keep disparate assets cohesive (Hypnospace Outlaw). **[fetched]** — [Game Developer, 2019](https://www.gamedeveloper.com/business/road-to-the-igf-tholen-lasch-nelson-jr-and-cochran-s-i-hypnospace-outlaw-i-)
- One master file of every character, checked for each new design (Chicory). **[fetched]** — [Wacom Community](https://community.wacom.com/en-pe/designing-chicorys-creatures-with-alexis-dean-jones)
- Draw the tile set first and build the game from it; adjust difficulty by editing images (Wilmot's Warehouse). **[fetched]** — [Game Developer, 2019](https://www.gamedeveloper.com/design/game-design-deep-dive-the-creative-camaraderie-behind-i-wilmot-s-warehouse-i-)
- Greybox each room on a grid in Aseprite before drawing; split furniture into pieces and reassemble in engine (Unpacking). **[fetched]** — [Game Developer, 2021](https://www.gamedeveloper.com/design/intimacy-from-the-inanimate-in-house-moving-puzzler-unpacking)
- Build characters from primitive shapes when no modelling tool is available (Crow Country). **[snippet]** — [Stealth Optional](https://stealthoptional.com/news/crow-country-horror-game-mixes-ps1-final-fantasy-vii-resident-evil/)
- Mix sprite-sheet animation with procedural, code-driven animation in a custom engine (Animal Well). **[fetched]** — [Game Developer, 2022](https://www.gamedeveloper.com/art/creature-feature-the-surreal-pixel-art-and-animation-of-animal-well)
- A shared reference pool and "a common language for those working on the game" set before production (MOUSE: P.I. For Hire). **[fetched]** — [Final Weapon, 2026](https://finalweapon.net/2026/09/08/interview-mouse-pi-for-hire-devs-on-the-challenges-of-black-and-white/)
- A fixed-spec fantasy console that removes decisions: Celeste Classic took four days in PICO-8. **[snippet]** — [Wikipedia, PICO-8](https://en.wikipedia.org/wiki/PICO-8)

Costs the creators reported:

- 1-bit works against any mechanic that needs fine recognition (faces in Obra Dinn). **[fetched]** — [Game Developer, 2015](https://www.gamedeveloper.com/design/lucas-pope-and-the-rise-of-the-1-bit-dither-punk-aesthetic)
- Monochrome makes clarity hard (Minit). **[snippet]** — [mirror](https://arucoppu.pages.dev/posts/minit-fun-racer-devs-discuss-the-fun-and-challenge-of-making-the-game)
- Black-and-white art was hardest on the interface (Chicory). **[snippet]** — [Sportskeeda](https://sportskeeda.com/esports/news-something-personal-meaningful-greg-lobanov-talks-creativity-imagination-chicory-a-colorful-tale)
- Without colour, lighting and foreground and background separation must do the work of signalling what is interactive (MOUSE). **[fetched]** — [Final Weapon, 2026](https://finalweapon.net/2026/09/08/interview-mouse-pi-for-hire-devs-on-the-challenges-of-black-and-white/)
- Flat shading removes depth cues, which then have to be rebuilt with shadow, fog and line (Sable). **[fetched]** — [Game Developer, 2022](https://www.gamedeveloper.com/marketing/how-shedworks-refined-the-art-of-sable-in-pursuit-of-readability)
- Isometric is a steep learning curve even for an experienced pixel artist (Unpacking). **[fetched]** — [Game Developer, 2021](https://www.gamedeveloper.com/design/intimacy-from-the-inanimate-in-house-moving-puzzler-unpacking)
- Hand-lit pixel art and hand-drawn animation are slow: Eastward took over six years; Cuphead needed over 60,000 frames. **[fetched]** — [Game Developer, Eastward](https://www.gamedeveloper.com/art/eastward-s-creators-share-insights-on-making-pixel-art-adventures); [Game Developer, Cuphead](https://www.gamedeveloper.com/art/how-i-cuphead-i-nailed-the-look-and-feel-of-classic-1930s-cartoons)

### Inferences

All **observation**.

- The cheapest consistent styles for a solo developer share three properties: few colours, no rendered lighting, and a shape vocabulary that can be written as a one-page rule sheet. 1-bit sprite art, fixed-palette handheld styles and flat-shape illustration all qualify. Lit pixel art and frame-by-frame hand-drawn animation do not.
- Every monochrome or flat style in this set had to solve the same problem a top-down office game will have: signalling which objects are interactive without colour or shading. The sourced answers are transferable as written: inverted outlines (Obra Dinn), a single reserved accent colour for important items (Downwell), strong figure and ground separation plus decals (MOUSE), and a drop shadow under every character (Sable).
- Hypnospace's shortcut (author normally, then batch-reduce to a fixed palette with dither) and A Short Hike's shortcut (author normally, then render small) are both "filter" approaches. A 2D canvas game can use the same idea: draw assets in one base style and apply a palette-quantise or 1-bit pass per era or per room. This would make several era looks affordable from one asset set, at the cost of each look being less hand-tuned; Playdate's warning about uncleaned machine dither applies.
- For assets produced partly by code or by generative tools, a written rule sheet in the manner of Tholen's design bible or Dean-Jones's master character file is the control that the sourced teams relied on for consistency.
- Chicory's finding that monochrome was hardest on the UI is a warning for a portfolio game, where the interface (project cards, links, contact details) is the part that must work.

### Gaps

- No source gives hours or cost per asset for any of these styles, so difficulty comparisons are qualitative.
- No creator statements found on shortcuts for Monument Valley, Mini Metro, Limbo, Inside, Hollow Knight, Gris, Old Man's Journey, Alto's Adventure, Saturnalia, Tunic (beyond "simple and easy to build on"), Habbo Hotel or eBoy.
- I found no source on producing these styles with generative or procedural tooling, which matters for a project whose assets are partly drawn by code.
