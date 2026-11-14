import { Gfx, rng, fractal, type Ctx, type Env, type Medium, type P } from "./core";
import type { Film } from "./film";
import { clamp, inside, mix, polyLen, resample, smooth } from "./gallery";
import { fill, oilStroke, weave, type OStroke } from "./paintedOilKit";

// ONE MORE COMMIT · a home office at dusk, painted light.
//
// THE IDEA: the working day is over outside the window, the screen still holds him, and the dog
// waits in the lamp light. One focal subject: the man, standing between two lights.
// THE LIGHTS (named, and nothing else lights the room):
//   SCREEN, the monitor on the desk: a cool teal that reaches the keyboard, the chair's rim, the
//     floor in front of the desk and every plane of the man that turns to the upper left.
//   LAMP, the desk lamp at the right end of the desk: a warm orange pool on the desk and on the
//     floor to the right, and every plane that turns to the upper right. The dog sits in it.
//   (the dusk window is an accent, not a light: a pink reveal on the wall round it and two dim
//   panes of rose on the boards below it. It models nothing.)
//   Each cast shadow is filled by the OTHER light: the man's lamp shadow is teal, his screen shadow orange.
//
// MEDIUM RECIPE (the hand adapted from two references Asi named: the painted backgrounds of the
// series Arcane, and the oil handling of the game Disco Elysium. No character, room or frame of
// either is drawn; only the way the marks are made crosses over):
//   MARK: opaque paint and a flat bristle brush (the painted-oil kit's stroke). One unit mark is a
//     short loaded stroke that keeps to ONE plane of ONE object and runs the way that plane runs:
//     along the floor boards, down a book spine, round a leaf, up and back through the hair. A big
//     flat for wall and floor, a medium one for furniture, a small one for the figures.
//   EDGE: hard where a form turns or one thing stands in front of another (every object's paint is
//     clipped to its own silhouette, every plane to its own facet); lost in shadow, where a form's
//     dark is keyed to the dark behind it. Nothing is blended across an object's edge.
//   ORDER: a dark toned ground; the room back to front, each thing blocked in its shadow colour
//     then built in planes; cast shadows cut back into the lit floor; the figures; rim lights fat
//     and last; then a few broken, slightly shaky near-black accent lines; then the brightest dabs.
//   PAPER: primed linen toned dark violet-brown, the weave showing where the paint is lean.
//   PALETTE: a dark, cool, low-saturation room (blue-violet wall, violet-brown boards) against two
//     saturated lights (teal, orange) and three accents (the pink-orange sky, the shiba, the teal
//     shirt). Shadows cool, lights warm or teal, the darkest note a violet near-black, not black.
//   NOT: nearest is `paintedOil` (same bristle mark, same kit). It differs in three things: two
//     coloured lights instead of one window (colour, not value, turns the form); form is built in
//     flat facets with hard edges instead of wet-into-wet modelling; and a broken dark line is laid
//     last over the paint, which paintedOil never does. No gradient tool, no uniform noise, no
//     stroke scattered across an object's edge.
//
// REALISM (from knowledge, no reference image opened):
//   VIEW: one oblique projection for everything, the RPG room view: screen x = world x, depth runs
//     down the screen, height runs up it, no convergence. Every piece of furniture is a front face
//     plus a top face drawn with the same two factors, so the pieces agree.
//   THE MAN: about 5 heads tall (a declared stylised canon: big head, short legs), three-quarter
//     view facing screen-left toward the desk and the screen, weight on both feet, far foot a
//     little forward. Black quiff standing up, short grey sides, dark-framed glasses, full dark
//     beard with the lower lip showing, teal T-shirt, dark trousers and shoes. Far hand wraps a
//     mug (four fingers and a thumb), near hand hangs open (four fingers and a thumb).
//   THE DOG: a shiba inu sitting in profile, head thrown back to look up at him: blunt short
//     muzzle, small thick pricked ears, cream cheeks, throat and chest (urajiro), a tail curled
//     up onto the back, straight short forelegs, a collar. Each of those is what a fox is not.

const W = 1920, H = 1080, FL = 396; // FL: where the back wall meets the floor
const OIL: Medium = { nib: 1, taper: 1, pressure: 1, retrace: false, wobble: 0, rough: 0 };
const INK = "#0e0c14";

// ---------------------------------------------------------------- small helpers
const rect = (x0: number, y0: number, x1: number, y1: number): P[] => [[x0, y0], [x1, y0], [x1, y1], [x0, y1]];
const ell = (cx: number, cy: number, rx: number, ry: number, n = 24, rot = 0): P[] => Array.from({ length: n }, (_, i) => { const a = (i / n) * Math.PI * 2, x = Math.cos(a) * rx, y = Math.sin(a) * ry, c = Math.cos(rot), s = Math.sin(rot); return [cx + x * c - y * s, cy + x * s + y * c] as P; });
const sm = (pts: P[]) => smooth(pts, true, 6);
const rrect = (x0: number, y0: number, x1: number, y1: number, r: number): P[] => { const o: P[] = []; [[x1 - r, y0 + r, -90], [x1 - r, y1 - r, 0], [x0 + r, y1 - r, 90], [x0 + r, y0 + r, 180]].forEach(([cx, cy, a0]) => { for (let k = 0; k <= 6; k++) { const a = ((a0 + k * 15) * Math.PI) / 180; o.push([cx + Math.cos(a) * r, cy + Math.sin(a) * r]); } }); return o; };
const dRect = (x: number, y: number, x0: number, y0: number, x1: number, y1: number) => Math.hypot(Math.max(x0 - x, 0, x - x1), Math.max(y0 - y, 0, y - y1));
const deg = (d: number) => (d * Math.PI) / 180;

// ---------------------------------------------------------------- colour: two lights, mixed in linear light
// A material is three painted notes: in shadow, under the SCREEN alone, under the LAMP alone. Where
// both lights land the notes are added in linear light, so teal + orange on wood comes out a pale
// tan (as it does in a room) instead of a green.
type Mat = { sh: number[]; te: number[]; wa: number[] };
const lin = (c: string) => [1, 3, 5].map((i) => Math.pow(parseInt(c.slice(i, i + 2), 16) / 255, 2.2));
const hexOf = (v: number[]) => "#" + v.map((x) => Math.round(255 * Math.pow(clamp(x), 1 / 2.2)).toString(16).padStart(2, "0")).join("");
const mat = (sh: string, te: string, wa: string): Mat => ({ sh: lin(sh), te: lin(te), wa: lin(wa) });
const lit = (m: Mat, t: number, w: number, k = 1) => hexOf(m.sh.map((s, i) => (s + t * (m.te[i] - s) + w * (m.wa[i] - s)) * k));
// light falls in a few flat steps with a wandering edge: shapes of light, never a ramp
const LV = [0, 0.3, 0.62, 1], TH = [0.1, 0.38, 0.66];
const post = (v: number, x: number, y: number, seed: number) => { const n = v + (fractal(seed, x, y, 0.004, 0.006, 2) - 0.5) * 0.07; let o = 0; for (let i = 0; i < 3; i++) o += (LV[i + 1] - LV[i]) * clamp((n - TH[i]) / 0.07 + 0.5); return o; };
// one object's own colour, drifting a little warm-light or cool-dark from stroke to stroke
const vary = (c: string, seed: number, amt = 0.13) => (x: number, y: number) => { const n = fractal(seed, x, y, 0.045, 0.045, 2) - 0.5; return n > 0 ? mix(c, "#ffd9a8", n * amt * 2) : mix(c, "#12122a", -n * amt * 2.4); };

// ---------------------------------------------------------------- the room, in one projection
const MX = 975;                                           // the monitor's centre line
const DESK = { x0: 610, x1: 1380, top: 226, front: 376, foot: 546 };
const RUG = rrect(770, 612, 1650, 1004, 26);
const WIN = { x0: 296, y0: 46, x1: 556, y1: 276 }, GLASS = rect(308, 58, 544, 264);

const WALL = mat("#242838", "#2a858a", "#cf8a52");
const FLOOR = mat("#272030", "#1e6e69", "#d78c46");
const RUGM = mat("#2b1b2b", "#4e5e6a", "#ba5747");
const RUGB = mat("#3b3038", "#86bdb2", "#f4c888");
const DESKM = mat("#30242a", "#287d76", "#f0aa5f");
const PAPERM = mat("#6a6272", "#a8e0d4", "#ffe6b4");

const wallT = (x: number, y: number) => post(0.66 * clamp(1 - dRect(x, y, MX - 124, 84, MX + 124, 238) / 105), x, y, 41);          // the glow round the screen
// the lamp on the wall: a cone opening downward from the shade, and a low bounce off the lit floor to the right
const wallW = (x: number, y: number) => post(clamp(clamp(1.2 - Math.hypot((x - 1268) / 330, (y - 290) / 210)) * clamp(((y - 150) * 1.5 - Math.abs(x - 1275)) / 34) + 0.55 * clamp(1 - Math.hypot((x - 1580) / 400, (y - 440) / 300))), x, y, 42);
const wallCol = (x: number, y: number) => { const far = clamp(Math.hypot((x - 1100) / 1250, (y - 340) / 560)), c = lit(WALL, wallT(x, y), wallW(x, y), 1.15 - 0.62 * far), p = 0.55 * clamp(1 - dRect(x, y, WIN.x0, WIN.y0, WIN.x1, WIN.y1) / 120); return p > 0 ? mix(c, "#9a5878", p) : c; };

// the floor: the desk stands between the lights and the boards, so both pools begin a way out from it
const floorT = (x: number, y: number) => post(clamp(1.1 - Math.hypot((x - 965) / 610, (y - 860) / 310)) * clamp((y - 612) / 140), x, y, 51);
const floorW = (x: number, y: number) => post(clamp(1.18 - Math.hypot((x - 1410) / 440, (y - 720) / 265)) * Math.max(clamp((y - 596) / 40), clamp((x - 1490) / 40)), x, y, 52);
// cast shadows on the floor, each from ONE light (so each is filled by the other)
const MCX = 1210, MGY = 848, MK = 1.1;                    // the man: where he stands, and his size
const mp = (a: number[][]): P[] => a.map(([x, h]) => [MCX + x * MK, MGY - h * MK] as P);
const DCX = 1466, DGY = 858, DK = 1;                      // the dog
const SH_LAMP: P[][] = [
  [[1120, 834], [1160, 846], [1180, 882], [1204, 852], [1264, 852], [1220, 1090], [968, 1090]],   // the man
  [[1418, 860], [1528, 854], [1600, 992], [1562, 1036], [1468, 1016]],                            // the dog
  [[1780, 438], [1930, 426], [1930, 502], [1782, 486]],                                           // the plant's pot
];
const SH_SCREEN: P[][] = [
  [[1128, 852], [1180, 846], [1214, 886], [1220, 848], [1266, 838], [1440, 1090], [1268, 1090]],  // the man
  smooth([[866, 646], [1008, 646], [1018, 740], [1012, 850], [984, 892], [852, 890], [824, 850], [840, 740]], true, 5), // the chair, leaning a little left of the screen
];
const onRug = (x: number, y: number) => inside(RUG, x, y);
const DUSK: P[][] = [[[338, 470], [452, 470], [530, 632], [392, 632]], [[474, 470], [588, 470], [690, 632], [552, 632]]];
const ground = (x: number, y: number, killT = false, killW = false) => {
  const t = killT ? 0 : floorT(x, y), w = killW ? 0 : floorW(x, y);
  if (onRug(x, y)) return lit(RUGM, t, w, 0.9 + 0.2 * fractal(57, x, y, 0.03, 0.05, 2));
  const row = Math.floor((y - FL) / 44), k = 0.82 + 0.36 * fractal(70 + row * 3, x, 0, 0.0035, 1, 1);
  return lit(FLOOR, t, w, k);
};
const groundAt = (x: number, y: number) => ground(x, y, SH_SCREEN.some((s) => inside(s, x, y)), SH_LAMP.some((s) => inside(s, x, y)));
// the desk top: the lamp's pool, and the screen's spill on the keyboard side
const deskT = (x: number, y: number) => post(0.9 * clamp(1.12 - Math.hypot((x - MX) / 250, (y - 318) / 86)), x, y, 53);
const deskW = (x: number, y: number) => post(clamp(1.14 - Math.hypot((x - 1240) / 190, (y - 312) / 74)), x, y, 54);
const deskCol = (x: number, y: number) => lit(DESKM, deskT(x, y), deskW(x, y), 0.88 + 0.24 * fractal(58, x, y, 0.004, 0.08, 2));

// ---------------------------------------------------------------- stages
type Stage = { clip?: P[][]; within?: P[]; base?: [P[], string][]; strokes: OStroke[] };
type Pl = { p?: P[]; c: string; a?: number; w?: number; len?: number; amt?: number; imp?: number };
type PaintO = { w: number; len: number; seed: number; a?: number; imp?: number; dry?: number; step?: number };

const build = (): Stage[] => {
  const S: Stage[] = [];
  const add = (strokes: OStroke[], clip?: P[][], within?: P[], base?: [P[], string][]) => { S.push({ strokes, clip, within, base }); };
  // a single deliberate stroke
  const st = (ctrl: P[], w: number, c0: string, seed: number, c1 = c0, imp = 0.3, dry = 0.12, load = 1.2): OStroke => ({ ctrl, w, c0, c1, load, dry, impasto: imp, jit: 0.07, soft: 0.1, seed });
  // an object built in planes: each plane clipped to its facet AND to the object's silhouette,
  // blocked in flat, then worked over with strokes that share that plane's direction
  const paint = (shape: P[], planes: Pl[], o: PaintO) => planes.forEach((pl, i) => {
    const reg = pl.p ?? shape, w = pl.w ?? o.w, len = pl.len ?? o.len, a = pl.a ?? o.a ?? 0;
    add(fill({ region: reg, step: o.step ?? Math.max(4.5, w * 0.72), len, w, dir: () => a, seed: o.seed + i * 7, dry: o.dry ?? 0.26, impasto: pl.imp ?? o.imp ?? 0.2, jit: 0.07, soft: 0.15, bend: 0.25, color: vary(pl.c, o.seed + i, pl.amt ?? 0.13) }), [reg], pl.p ? shape : undefined, [[reg, pl.c]]);
  });
  // a line walked in short strokes with gaps: the broken accent, and the rim lights
  const broken = (path: P[], w: number, seed: number, c = INK, skip = 0.18, imp = 0.12, c1 = c): OStroke[] => {
    const r = rng(seed), pts = resample(path, Math.max(4, Math.round(polyLen(path) / 5))), out: OStroke[] = [];
    let i = 0;
    while (i < pts.length - 2) { const n = 5 + Math.floor(r() * 9), seg = pts.slice(i, Math.min(pts.length, i + n + 1)); i += n; if (seg.length < 3 || r() < skip) continue; const j = seg.map(([x, y]) => [x + (r() - 0.5) * 1.6, y + (r() - 0.5) * 1.6] as P); out.push(st([j[0], j[Math.floor(j.length / 2)], j[j.length - 1]], w * (0.7 + 0.6 * r()), c, seed * 50 + out.length, c1, imp, 0.3, 1.1)); }
    return out;
  };

  // ============================================================ 1. the wall, with a big flat
  const WALLR = rect(-40, -40, W + 40, FL + 6);
  add(fill({ region: WALLR, step: 48, len: 165, w: 60, dir: (x, y) => -0.95 + (fractal(31, x, y, 0.003, 0.003, 2) - 0.5) * 1.8, seed: 100, dry: 0.3, impasto: 0.1, jit: 0.05, soft: 0.25, bend: 0.2, color: wallCol }), undefined, undefined, [[WALLR, "#1d1f2b"]]);

  // ============================================================ 2. the window: dusk, and a skyline
  const SKY = ["#343a72", "#5b4a8c", "#a2588f", "#e06c80", "#f58c66", "#fbb868", "#fdd58a"];
  const skyCol = (x: number, y: number) => { const t = clamp((y - 58) / 165) + (fractal(61, x, y, 0.01, 0.03, 2) - 0.5) * 0.16, f = clamp(t) * (SKY.length - 1), i = Math.min(SKY.length - 2, Math.floor(f)); return mix(SKY[i], SKY[i + 1], clamp((f - i - 0.5) * 3 + 0.5)); };
  add(fill({ region: GLASS, step: 15, len: 105, w: 19, dir: () => -0.06, seed: 110, dry: 0.2, impasto: 0.35, jit: 0.05, soft: 0.2, bend: 0.1, color: skyCol }), [GLASS], undefined, [[GLASS, "#d9727f"]]);
  add([ // clouds: violet bars with the last sun under them
    st([[312, 92], [372, 86], [436, 94]], 11, "#4b417c", 120, "#7a4f8a", 0.3, 0.3), st([[330, 100], [384, 96], [430, 101]], 4, "#f08a78", 121, "#f6a070", 0.5),
    st([[452, 122], [500, 114], [548, 120]], 12, "#7c4c86", 122, "#b25c8e", 0.3, 0.3), st([[462, 130], [504, 125], [544, 129]], 4, "#ffb072", 123, "#ffc887", 0.55),
    st([[318, 146], [360, 141], [404, 146]], 7, "#c0607f", 124, "#e87a78", 0.3, 0.35), st([[500, 164], [524, 160], [546, 163]], 5, "#ffd9a0", 125, "#ffc27a", 0.6),
  ], [GLASS]);
  const FAR_CITY: P[] = [[308, 266], [308, 206], [322, 206], [322, 188], [344, 188], [344, 212], [362, 212], [362, 176], [384, 176], [384, 200], [410, 200], [410, 184], [432, 184], [432, 208], [458, 208], [458, 172], [470, 160], [482, 172], [482, 204], [506, 204], [506, 186], [530, 186], [530, 202], [544, 202], [544, 266]];
  const CITY: P[] = [[308, 266], [308, 222], [334, 222], [334, 204], [352, 204], [352, 230], [374, 230], [374, 196], [380, 196], [380, 186], [392, 186], [392, 196], [400, 196], [400, 234], [430, 234], [430, 214], [454, 214], [454, 238], [478, 238], [478, 202], [500, 202], [500, 226], [522, 226], [522, 210], [544, 210], [544, 266]];
  paint(FAR_CITY, [{ c: "#6a4a7c", a: 1.57 }], { w: 11, len: 26, seed: 130, imp: 0.15 });
  paint(CITY, [{ c: "#1f1b33", a: 1.57 }], { w: 12, len: 30, seed: 135, imp: 0.12 });
  const wr = rng(140), wins: OStroke[] = [];
  for (let i = 0; i < 15; i++) { const x = 314 + wr() * 224, y = 216 + wr() * 44; if (!inside(CITY, x, y) || !inside(CITY, x, y - 7)) continue; wins.push(st([[x, y], [x + 3.5, y]], 3.4, i % 5 === 0 ? "#7fe0d8" : i % 3 === 0 ? "#ff9e5e" : "#ffd27a", 141 + i, undefined, 0.7, 0, 1.4)); }
  add(wins, [GLASS]);
  // the frame: dark wood, its inner edges and the sill's top taking the pink of the sky
  const fr = (a: P, b: P, w: number, c: string, seed: number, c1 = c) => st([a, [(a[0] + b[0]) / 2, (a[1] + b[1]) / 2], b], w, c, seed, c1, 0.2, 0.08, 1.3);
  add([
    fr([302, 46], [302, 276], 13, "#2a2231", 150, "#1d1824"), fr([550, 46], [550, 276], 13, "#231c2a", 151, "#1a1622"), fr([296, 52], [556, 52], 13, "#2c2433", 152), fr([296, 270], [556, 270], 13, "#2c2433", 153),
    fr([426, 58], [426, 264], 7, "#221b29", 154), fr([308, 152], [544, 152], 7, "#221b29", 155),
    fr([310, 58], [310, 264], 2.2, "#d98aa0", 156, "#f0a078"), fr([430.5, 60], [430.5, 262], 1.8, "#b06a88", 157, "#e89070"), fr([310, 156.5], [542, 156.5], 1.8, "#c87a90", 158),
  ]);
  const SILL = [[284, 276], [568, 276], [574, 292], [278, 292]] as P[];
  paint(SILL, [{ c: "#b87088", a: 0 }, { p: rect(278, 287, 574, 294), c: "#2a2030", a: 0 }], { w: 9, len: 60, seed: 160, imp: 0.3 });

  // ============================================================ 3. the framed print, right of the desk
  const PR = { x0: 1440, y0: 70, x1: 1580, y1: 236 }, MATR = rect(1452, 82, 1568, 224), ARTR = rect(1468, 100, 1552, 206);
  paint(rect(PR.x0, PR.y0, PR.x1, PR.y1), [{ c: "#2a1e22", a: 1.57 }], { w: 10, len: 40, seed: 170, imp: 0.15 });
  paint(MATR, [{ c: "#a98f86", a: 1.3 }, { p: [[1452, 82], [1532, 82], [1488, 224], [1452, 224]], c: "#d6ac80", a: 1.3 }], { w: 10, len: 30, seed: 174, imp: 0.2 });
  paint(ARTR, [{ c: "#1f4a5c", a: 0.1 }], { w: 9, len: 34, seed: 178, imp: 0.2 });
  paint(sm(ell(1512, 138, 21, 21, 12)), [{ c: "#e0654a", a: 0.6 }, { p: rect(1488, 112, 1510, 160), c: "#f28a5c", a: 0.6 }], { w: 7, len: 18, seed: 180, imp: 0.4 });
  paint([[1468, 206], [1468, 168], [1492, 158], [1516, 170], [1540, 160], [1552, 166], [1552, 206]], [{ c: "#2f8580", a: 0.2 }], { w: 8, len: 30, seed: 184, imp: 0.25 });
  paint([[1468, 206], [1468, 186], [1496, 180], [1522, 190], [1552, 182], [1552, 206]], [{ c: "#143040", a: 0.1 }], { w: 8, len: 30, seed: 186, imp: 0.2 });
  add([fr([1441, 72], [1441, 234], 3, "#c8824a", 190, "#8a5634"), fr([1442, 71], [1578, 71], 2.4, "#9a6238", 191, "#4a3028"), ...broken([[1580, 72], [1580, 236], [1442, 236]], 3, 192, INK, 0.2)]);

  // ============================================================ 4. the bookshelf, far left, kept quiet
  const BX0 = 30, BX1 = 250;
  paint(rect(BX0, 66, BX1, 150), [{ c: "#3d3040", a: 0.05 }, { p: [[196, 66], [BX1, 66], [BX1, 150], [228, 150]], c: "#6a475e", a: 0.05 }], { w: 18, len: 70, seed: 200, imp: 0.2 });
  paint(rect(BX0, 150, BX1, 480), [{ c: "#1a151e", a: 1.57 }], { w: 16, len: 60, seed: 204, imp: 0.08 });
  const br = rng(700), BOOKC = ["#6a3340", "#2f5063", "#77643c", "#3d436b", "#573f66", "#864f36", "#2f5f58", "#948470", "#34344a"], books: OStroke[] = [];
  for (let s = 0; s < 4; s++) { const y1 = 231 + s * 80; let x = 46; while (x < 228) { const bw = 10 + br() * 13, bh = 42 + br() * 24, c = mix(BOOKC[Math.floor(br() * BOOKC.length)], "#14111a", 0.12 + 0.1 * s + 0.2 * clamp((150 - x) / 120)); if (br() < 0.1) { x += bw * 0.8; continue; } const lean = br() < 0.12 ? 6 : 0; books.push(st([[x + bw / 2 + lean, y1], [x + bw / 2 + lean * 0.4, y1 - bh / 2], [x + bw / 2, y1 - bh]], bw - 1.2, c, 710 + books.length, mix(c, "#d08aa2", 0.16), 0.22, 0.05, 1.3)); if (br() < 0.4) books.push(st([[x + 2, y1 - bh * 0.72], [x + bw - 2, y1 - bh * 0.72]], 2, mix(c, "#f0d0a0", 0.45), 760 + books.length, undefined, 0.3, 0, 1.3)); x += bw + 0.6; } }
  add(books, [rect(40, 160, 240, 472)]);
  add([0, 1, 2, 3, 4].map((s) => fr([BX0, 155 + s * 80.5 - (s === 4 ? 1 : 0)], [BX1, 155 + s * 80.5 - (s === 4 ? 1 : 0)], 10, "#33283a", 780 + s, "#4a3548")).concat([fr([35, 150], [35, 480], 10, "#2a2130", 786), fr([245, 150], [245, 480], 10, "#3d2c40", 787)]));
  add([st([[86, 118], [130, 116], [176, 118]], 15, "#5a3b52", 790, "#7a4a60", 0.3), st([[96, 105], [132, 103], [166, 105]], 12, "#35506a", 791, "#4a6a80", 0.3), ...broken([[BX0, 150], [BX1, 150]], 2.4, 792, INK, 0.25)]);

  // ============================================================ 5. the floor: boards along the room
  const FLOORR = rect(-40, FL, W + 40, H + 40);
  add(fill({ region: FLOORR, step: 34, len: 180, w: 40, dir: () => 0.004, seed: 300, dry: 0.3, impasto: 0.14, jit: 0.06, soft: 0.2, bend: 0.03, color: (x, y) => ground(x, y) }), [FLOORR], undefined, [[FLOORR, "#1c161f"]]);
  // the cast shadows, cut back into the lit boards with hard edges
  SH_LAMP.forEach((s, i) => add(fill({ region: s, step: 26, len: 120, w: 32, dir: () => 0.004, seed: 320 + i, dry: 0.25, impasto: 0.1, jit: 0.05, soft: 0.2, color: (x, y) => ground(x, y, SH_SCREEN.some((q) => inside(q, x, y)), true) }), [s]));
  SH_SCREEN.forEach((s, i) => add(fill({ region: s, step: 26, len: 120, w: 32, dir: () => 0.004, seed: 330 + i, dry: 0.25, impasto: 0.1, jit: 0.05, soft: 0.2, color: (x, y) => ground(x, y, true, SH_LAMP.some((q) => inside(q, x, y))) }), [s]));
  DUSK.forEach((s, i) => add(fill({ region: s, step: 24, len: 110, w: 30, dir: () => 0.004, seed: 336 + i, dry: 0.3, impasto: 0.12, jit: 0.05, soft: 0.2, color: (x, y) => mix(ground(x, y), "#93587a", 0.34 + 0.16 * fractal(338, x, y, 0.01, 0.02, 2)) }), [s]));
  // board seams: thin, broken, darker than whatever light they cross
  const sr = rng(340), seams: OStroke[] = [];
  for (let row = 1; row < 16; row++) { const y = FL + row * 44; let x = -20 + sr() * 80; while (x < W) { const L = 90 + sr() * 240; if (sr() > 0.16) seams.push(st([[x, y + (sr() - 0.5) * 2], [x + L / 2, y + (sr() - 0.5) * 2], [x + L, y + (sr() - 0.5) * 2]], 1.8, mix(groundAt(x + L / 2, y), INK, 0.62), 341 + seams.length, undefined, 0.05, 0.3, 1)); if (sr() < 0.3 && !(row === 4 && x + L > 600 && x + L < 1400)) seams.push(st([[x + L, y], [x + L + 1, y + 44]], 1.6, mix(groundAt(x + L, y + 20), INK, 0.6), 600 + seams.length, undefined, 0.05, 0.3, 1)); x += L + 6 + sr() * 30; } }
  add(seams, [FLOORR]);
  // the skirting board
  add(fill({ region: rect(-40, FL - 17, W + 40, FL + 1), step: 13, len: 110, w: 16, dir: () => 0, seed: 350, dry: 0.2, impasto: 0.15, jit: 0.05, color: (x) => mix(wallCol(x, FL - 30), "#0f0d16", 0.42) }), [rect(-40, FL - 17, W + 40, FL + 1)]);

  // ============================================================ 6. the rug
  add(fill({ region: RUG, step: 17, len: 64, w: 21, dir: (x, y) => (fractal(360, x, y, 0.02, 0.02, 1) - 0.5) * 0.5, seed: 361, dry: 0.3, impasto: 0.16, jit: 0.07, soft: 0.2, color: (x, y) => ground(x, y) }), [RUG], undefined, [[RUG, "#241824"]]);
  SH_LAMP.forEach((s, i) => add(fill({ region: s, step: 17, len: 56, w: 20, dir: () => 0.05, seed: 370 + i, dry: 0.25, impasto: 0.12, jit: 0.06, color: (x, y) => (onRug(x, y) ? ground(x, y, SH_SCREEN.some((q) => inside(q, x, y)), true) : null) }), [s], RUG));
  SH_SCREEN.forEach((s, i) => add(fill({ region: s, step: 17, len: 56, w: 20, dir: () => 0.05, seed: 380 + i, dry: 0.25, impasto: 0.12, jit: 0.06, color: (x, y) => (onRug(x, y) ? ground(x, y, true, SH_LAMP.some((q) => inside(q, x, y))) : null) }), [s], RUG));
  // its border: two woven lines walked round the rug, each short stroke taking the light it lies in
  const borderCol = (x: number, y: number) => lit(RUGB, SH_SCREEN.some((q) => inside(q, x, y)) ? 0 : floorT(x, y), SH_LAMP.some((q) => inside(q, x, y)) ? 0 : floorW(x, y));
  const walk = (path: P[], w: number, seed: number): OStroke[] => { const pts = resample([...path, path[0]], Math.round(polyLen([...path, path[0]]) / 11)), out: OStroke[] = []; for (let i = 0; i + 2 < pts.length; i += 2) out.push(st([pts[i], pts[i + 1], pts[i + 2]], w, borderCol(pts[i][0], pts[i][1]), seed + i, borderCol(pts[i + 2][0], pts[i + 2][1]), 0.35, 0.25, 1.1)); return out; };
  add([...walk(rrect(800, 640, 1620, 976, 12), 9, 4000), ...walk(rrect(822, 660, 1598, 956, 6), 3, 5000)]);
  // its fringe at the two short ends, and a dark lip where it lies on the boards
  const fringe: OStroke[] = [];
  for (let y = 628; y < 992; y += 8) { fringe.push(st([[772, y], [760, y + 1.5]], 2.6, mix(groundAt(778, y), "#f4e4c8", 0.35), 390 + fringe.length, undefined, 0.3, 0.2, 1.1)); fringe.push(st([[1648, y], [1660, y + 1.5]], 2.6, mix(groundAt(1642, y), "#f4e4c8", 0.35), 390 + fringe.length, undefined, 0.3, 0.2, 1.1)); }
  add(fringe);
  add(broken([[790, 1005], [1630, 1005]], 3, 396, "#120e16", 0.2));

  // ============================================================ 7. the plant, far right
  const POT = [[1694, 388], [1786, 388], [1778, 470], [1768, 481], [1712, 481], [1702, 470]] as P[];
  paint(POT, [{ c: "#272d3c", a: 1.57 }, { p: rect(1690, 388, 1722, 484), c: "#b9794a", a: 1.5 }, { p: rect(1722, 388, 1740, 484), c: "#6a5048", a: 1.5 }], { w: 13, len: 50, seed: 400, imp: 0.25 });
  paint(ell(1740, 388, 49, 13, 20), [{ c: "#16131a", a: 0 }], { w: 9, len: 40, seed: 404, imp: 0.1 });
  add([st(ell(1740, 388, 49, 13, 20).slice(8, 15), 3.2, "#e0935a", 406, "#7a5a50", 0.5), st([[1741, 388], [1736, 300], [1739, 210], [1736, 138]], 7, "#3a2a26", 407, "#2a2420", 0.2), st([[1738, 386], [1733, 300], [1736, 220]], 2, "#b8764a", 408, "#6a4a38", 0.4)]);
  // a rubber plant: big ovate leaves, each one two planes about its midrib, painted along its length
  const leaf = (bx: number, by: number, ang: number, L: number, wd: number, k: number, seed: number) => {
    const c = Math.cos(deg(ang)), s = Math.sin(deg(ang)), at = (u: number, v: number): P => [bx + u * L * c - v * wd * s, by + u * L * s + v * wd * c];
    const out = sm([at(0, 0), at(0.18, -0.42), at(0.5, -0.52), at(0.82, -0.3), at(1, 0), at(0.84, 0.3), at(0.5, 0.5), at(0.16, 0.38)]);
    const up = c >= 0 ? 1 : -1;                       // which half of the leaf faces up the screen
    const litHalf = [at(-0.05, 0), at(1.05, 0), at(1.05, -up * 0.7), at(-0.05, -up * 0.7)];
    paint(out, [{ c: mix("#15302c", "#0e1c22", 1 - k), a: deg(ang) }, { p: litHalf, c: mix("#2c5a44", "#8a9a4c", k), a: deg(ang) }], { w: wd * 0.3, len: L * 0.42, seed, imp: 0.3 });
    add([st([at(0.04, 0), at(0.5, -up * 0.03), at(0.97, 0)], 2, mix("#5a8a5a", "#d8c878", k), seed + 3, "#3a6a4c", 0.4), ...broken(resample([at(0, 0), at(0.16, up * 0.38), at(0.5, up * 0.5), at(0.84, up * 0.3), at(1, 0)], 14), 2, seed + 4, INK, 0.3)]);
  };
  ([[1742, 346, 22, 92, 40, 0.2, 410], [1734, 352, 202, 84, 38, 0.75, 416], [1740, 300, -28, 100, 44, 0.3, 422], [1736, 330, -152, 104, 46, 0.9, 428], [1740, 238, -6, 106, 44, 0.25, 434], [1736, 264, 172, 110, 46, 1, 440], [1738, 180, -52, 98, 42, 0.4, 446], [1736, 202, -132, 102, 44, 0.95, 452], [1737, 146, -98, 92, 40, 0.8, 458], [1739, 150, -70, 66, 28, 0.6, 464]] as number[][]).forEach(([bx, by, ang, L, wd, k, seed]) => leaf(bx, by, ang, L, wd, k, seed));

  // ============================================================ 8. the desk
  const D = DESK;
  paint(rect(D.x0, D.front, D.x1, D.foot), [{ c: "#130f16", a: 0 }, { p: rect(812, 470, 1356, D.foot), c: "#19131c", a: 0 }, { p: rect(622, 392, 812, D.foot), c: "#281d25", a: 1.57 }, { p: rect(1356, 392, D.x1, D.foot), c: "#2a1f27", a: 1.57 }, { p: rect(D.x0, 392, 622, D.foot), c: "#2a1f27", a: 1.57 }], { w: 22, len: 80, seed: 500, imp: 0.08 });
  add([...broken([[626, 443], [808, 443]], 2.4, 506, INK, 0.1), ...broken([[626, 494], [808, 494]], 2.4, 507, INK, 0.1), ...broken([[812, 392], [812, D.foot]], 2.6, 508, INK, 0.12), ...[417, 468, 520].map((y, i) => st([[703, y], [731, y]], 3.4, "#3f7f80", 509 + i, "#57a39c", 0.5, 0, 1.3))]);
  // the top: wood laid along its grain, the two pools of light meeting on it
  const TOP = rect(D.x0, D.top, D.x1, D.front);
  add(fill({ region: TOP, step: 21, len: 135, w: 26, dir: () => 0.004, seed: 520, dry: 0.28, impasto: 0.25, jit: 0.06, soft: 0.2, bend: 0.03, color: deskCol }), [TOP], undefined, [[TOP, "#2a1f25"]]);
  add(fill({ region: rect(D.x0, D.front, D.x1, 392), step: 12, len: 120, w: 15, dir: () => 0, seed: 524, dry: 0.2, impasto: 0.15, jit: 0.05, color: (x) => mix(deskCol(x, D.front - 6), "#120e15", 0.5) }), [rect(D.x0, D.front, D.x1, 392)]);
  add([...broken([[D.x0, 392.5], [D.x1, 392.5]], 2.6, 526, INK, 0.12), ...broken([[D.x0, D.top], [D.x1, D.top]], 2, 527, "#120e15", 0.3)]);

  // the monitor: a dark slab with the one cool light in the room
  paint(ell(MX, 277, 52, 12, 20), [{ c: "#161720", a: 0 }], { w: 9, len: 40, seed: 530, imp: 0.1 });
  add([st(ell(MX, 277, 50, 11, 20).slice(11, 20), 2.6, "#3fb5aa", 532, "#2a7f80", 0.5), st([[MX, 272], [MX, 236]], 17, "#14151d", 533), st([[MX - 60, 290], [MX, 293], [MX + 60, 290]], 6, "#1b151c", 534, undefined, 0.05, 0.4)]);
  paint(rect(MX - 124, 84, MX + 124, 238), [{ c: "#111219", a: 0 }, { p: rect(MX - 124, 84, MX + 124, 91), c: "#30364a", a: 0 }], { w: 12, len: 60, seed: 536, imp: 0.1 });
  const SCR = rect(MX - 116, 98, MX + 116, 230);
  add(fill({ region: SCR, step: 11, len: 64, w: 14, dir: () => 0, seed: 540, dry: 0.15, impasto: 0.3, jit: 0.05, soft: 0.15, bend: 0.05, color: (x, y) => (x < MX - 72 ? "#157d80" : y < 113 ? "#3ccabb" : mix("#1fa29b", "#38c6b6", fractal(541, x, y, 0.02, 0.05, 2))) }), [SCR], undefined, [[SCR, "#1f9c96"]]);
  const cr = rng(545), code: OStroke[] = [];
  for (let row = 0; row < 10; row++) { const y = 123 + row * 10.6; let x = MX - 62 + Math.floor(cr() * 3) * 14; const n = 1 + Math.floor(cr() * 4); for (let k = 0; k < n && x < MX + 96; k++) { const L = 12 + cr() * 38, q = cr(); code.push(st([[x, y], [Math.min(MX + 108, x + L), y]], 4.2, q < 0.6 ? "#c4fff2" : q < 0.75 ? "#ffd690" : q < 0.88 ? "#ffa4bc" : "#86ecff", 546 + code.length, undefined, 0.55, 0, 1.4)); x += L + 7; } if (row % 2 === 0) code.push(st([[MX - 108, y], [MX - 108 + 10 + cr() * 18, y]], 3, "#5fd4c8", 580 + row, undefined, 0.4, 0, 1.3)); }
  add(code, [SCR]);
  add([fr([MX - 115, 229], [MX + 115, 229], 1.6, "#d8fff6", 590), fr([MX - 115, 99], [MX - 115, 229], 1.4, "#a8f0e4", 591)]);
  // the keyboard, its keys picked out by the screen
  const KB = [[890, 311], [1060, 311], [1066, 346], [884, 346]] as P[];
  paint(KB, [{ c: "#18272e", a: 0 }], { w: 9, len: 40, seed: 594, imp: 0.1 });
  const keys: OStroke[] = []; for (let r = 0; r < 4; r++) for (let k = 0; k < 14; k++) { if (r === 3 && k > 3 && k < 9) continue; const x = 894 - r * 1.3 + k * (11.6 + r * 0.2), y = 316.5 + r * 8; keys.push(st([[x, y], [x + 7, y]], 5.4, mix("#8fe8d8", "#3f9f98", r / 3.5 + (k % 3) * 0.08), 596 + keys.length, undefined, 0.45, 0, 1.4)); }
  keys.push(st([[941, 340.5], [989, 340.5]], 5.4, "#4fb0a6", 660, undefined, 0.45, 0, 1.4));
  add([...keys, ...broken([[884, 347], [1066, 347]], 2.4, 661, INK, 0.1)]);
  // yesterday's mug, and a sheet of notes with a pen
  add([st([[790, 327], [768, 331], [750, 335]], 10, "#1a1c22", 662, "#20252a", 0.05, 0.4)]);
  const MUG = [[774, 288], [806, 288], [804, 320], [798, 327], [782, 327], [776, 320]] as P[];
  add([st([[776, 296], [763, 298], [763, 312], [777, 315]], 4, "#3d4858", 663, "#2c3442", 0.3)]);
  paint(MUG, [{ c: "#3a4556", a: 1.57 }, { p: rect(790, 284, 810, 330), c: "#8fd8cc", a: 1.57 }, { p: rect(800, 284, 810, 330), c: "#c8f6ea", a: 1.57 }], { w: 7, len: 26, seed: 664, imp: 0.3 });
  paint(ell(790, 288, 16, 5.5, 16), [{ c: "#241a1a", a: 0 }], { w: 5, len: 14, seed: 668, imp: 0.1 });
  add([st(ell(790, 288, 16, 5.5, 16).slice(0, 9), 2, "#d8fff4", 669, "#8fd8cc", 0.5), st(ell(790, 288, 16, 5.5, 16).slice(8, 16).concat([[806, 288]]), 1.6, "#56687a", 670, undefined, 0.3)]);
  const PAPER = [[1068, 292], [1132, 286], [1142, 332], [1076, 340]] as P[];
  add(fill({ region: PAPER, step: 8, len: 32, w: 11, dir: () => -0.1, seed: 672, dry: 0.15, impasto: 0.4, jit: 0.04, color: (x, y) => lit(PAPERM, deskT(x, y), Math.max(0.3, deskW(x, y))) }), [PAPER], undefined, [[PAPER, "#b9ad9c"]]);
  add([[298, 0], [306, 4], [314, 1], [322, 6]].map(([y, dx], i) => st([[1078 + dx, y + 2], [1100, y - 1], [1126 - dx * 2, y - 4]], 1.7, "#4a4658", 674 + i, undefined, 0.1, 0.2, 1)).concat([st([[1098, 306], [1128, 326]], 3.4, "#15131a", 679, "#2a2630"), st([[1099, 305], [1114, 315]], 1.2, "#ffc27a", 680, undefined, 0.5), ...broken([[1076, 341], [1142, 333]], 2, 681, "#2a1d20", 0.2)]));
  // the lamp: base, two arms, a cone shade, the glow of its mouth
  paint(ell(1332, 292, 30, 10, 18), [{ c: "#191a22", a: 0 }], { w: 7, len: 30, seed: 684, imp: 0.1 });
  add([st(ell(1332, 292, 29, 9.5, 18).slice(8, 15), 2.6, "#f0a860", 686, "#9a6238", 0.5), st([[1304, 300], [1332, 304], [1362, 300]], 5, "#3a2420", 687, undefined, 0.05, 0.4),
    st([[1332, 288], [1344, 240], [1354, 200]], 6, "#20242e", 688, "#262b36", 0.2), st([[1330, 284], [1341, 242], [1351, 204]], 1.6, "#e09a58", 689, "#8a5a3a", 0.5),
    st([[1354, 200], [1328, 174], [1302, 152]], 6, "#20242e", 690, "#262b36", 0.2), st([[1352, 197], [1328, 171], [1305, 150]], 1.4, "#5a7f88", 691, undefined, 0.4),
    st([[1352, 199], [1356, 201]], 9, "#2c313c", 692), st([[1300, 151], [1304, 153]], 9, "#2c313c", 693)]);
  const MOUTH = ell(1280, 196, 37, 11, 20, -0.12);
  paint(MOUTH, [{ c: "#ffd27a", a: 0 }, { p: ell(1280, 198, 24, 6, 14, -0.12), c: "#fff3c8", a: 0 }], { w: 6, len: 22, seed: 694, imp: 0.6 });
  const SHADE = sm([[1296, 139], [1311, 147], [1319, 172], [1317, 192], [1300, 190], [1262, 190], [1243, 190], [1250, 172], [1272, 148]]);
  paint(SHADE, [{ c: "#1b3438", a: 1.2 }, { p: [[1240, 130], [1284, 130], [1270, 196], [1236, 196]], c: "#2f7a78", a: 1.2 }, { p: [[1240, 130], [1262, 130], [1250, 196], [1236, 196]], c: "#4fb5aa", a: 1.2 }], { w: 9, len: 34, seed: 698, imp: 0.3 });
  add([st([[1244, 192], [1280, 200], [1316, 193]], 2.4, "#ffb868", 702, "#ffe0a0", 0.7), ...broken(resample(SHADE.slice(2, 18), 16), 2, 703, INK, 0.25)]);

  // ============================================================ 9. the office chair, seen from behind
  const CX = 935;
  ([[CX, 704], [CX + 74, 674], [CX - 74, 674], [CX - 46, 626], [CX + 46, 626]] as P[]).forEach(([x, y], i) => add([st([[CX, 658], [(CX + x) / 2, (658 + y) / 2 - 3], [x, y - 4]], 8, "#191a22", 800 + i, "#12121a", 0.15), st([[CX + (x - CX) * 0.2, 656 + (y - 658) * 0.2], [x, y - 8]], 1.6, "#3a9a94", 806 + i, "#1f5a5e", 0.4, 0.3), st([[x - 3, y], [x + 4, y + 1]], 10, "#0b0b10", 812 + i, undefined, 0.1)]));
  add([st([[CX, 656], [CX, 594]], 11, "#14151c", 820, "#1a1c26", 0.15), st([[CX - 4, 650], [CX - 4, 600]], 1.8, "#3fa8a0", 821, undefined, 0.5)]);
  const SEAT = sm(ell(CX, 568, 82, 30, 16));
  paint(SEAT, [{ c: "#0f1017", a: 0 }, { p: rect(CX - 90, 536, CX + 90, 566), c: "#2a7078", a: 0 }], { w: 10, len: 44, seed: 824, imp: 0.15 });
  [-1, 1].forEach((sd, i) => { const x = CX + sd * 93; add([st([[x - sd * 6, 566], [x - sd * 2, 520], [x, 480]], 6, "#13141b", 830 + i), st([[x, 498], [x + sd * 1, 462], [x + sd * 1, 430]], 13, "#1c2530", 832 + i, "#232c3a", 0.2), st([[x - 1, 494], [x, 462], [x, 432]], 6.5, sd < 0 ? "#43b8ac" : "#3a9a94", 834 + i, "#63d8c8", 0.55)]); });
  const BACK = sm([[868, 441], [880, 428], [CX, 423], [990, 428], [1002, 441], [1007, 520], [996, 552], [CX, 560], [874, 552], [863, 520]]);
  paint(BACK, [{ c: "#14141c", a: 0.02, amt: 0.08 }, { p: rect(860, 418, 1010, 452), c: "#1f2534", a: 0.02 }], { w: 15, len: 62, seed: 838, imp: 0.1 });
  add([...[462, 478, 494, 510, 526, 540].map((y, i) => st([[874, y], [CX, y + 3], [996, y]], 1.6, "#242a3a", 842 + i, undefined, 0.15, 0.5, 0.9)), st([[CX, 556], [CX, 592]], 12, "#101117", 849)], [BACK, rect(CX - 8, 552, CX + 8, 594)]);
  add([st([[870, 436], [884, 428], [CX, 423.5], [986, 428], [1000, 436]], 4.2, "#4fd6c8", 850, "#8ff0e0", 0.7), st([[865, 446], [863, 484], [864, 520]], 2.2, "#3aa8a0", 851, "#1f6a6c", 0.5, 0.35), st([[1005, 448], [1008, 492], [1006, 524]], 2, "#c9703c", 852, "#7a4630", 0.5, 0.35), ...broken([[870, 553], [CX, 561], [1000, 553]], 2.4, 853, INK, 0.15)]);

  // ============================================================ 10. the man
  const ms = (a: number[][], w: number, c0: string, seed: number, c1 = c0, imp = 0.3, dry = 0.1, load = 1.25) => st(mp(a), w * MK, c0, seed, c1, imp, dry, load);
  const mpl = (a: number[][]) => sm(mp(a));
  const SKIN = { tl: "#aacdb6", tm: "#7fa99a", td: "#557f7e", core: "#4c2f3c", sh: "#6a4148", wl: "#ffc98f", wm: "#e89a5f", wd: "#b2603f" };
  const TEE = { tl: "#48c8ba", tm2: "#30b0a4", tm: "#1f9a92", td: "#157a78", core: "#0e3c46", wm: "#8a8458", wl: "#e8aa62" };
  const TROU = { d: "#151722", m: "#1d2534", t: "#1b3d4a", w: "#5c3830" };
  // contact shadows first: he stands ON the rug
  add([st(mp([[-92, 6], [-54, -3], [-16, 8]]), 13, "#120d16", 900, undefined, 0.05, 0.3), st(mp([[-16, -5], [18, -13], [54, -1]]), 14, "#120d16", 901, undefined, 0.05, 0.3)]);
  // legs: dark trousers. Weight on the near leg; the far leg a half step forward, its knee easy.
  const FAR_LEG = mpl([[-54, 210], [-2, 206], [4, 184], [-8, 150], [-16, 116], [-22, 76], [-24, 38], [-50, 36], [-58, 76], [-62, 116], [-62, 160]]);
  paint(FAR_LEG, [{ c: TROU.d }, { p: mpl([[-50, 208], [-30, 208], [-34, 160], [-38, 124], [-52, 120], [-54, 160]]), c: TROU.m }, { p: mpl([[-48, 110], [-34, 108], [-34, 70], [-36, 40], [-46, 40], [-49, 76]]), c: TROU.m },
    { p: mpl([[-62, 210], [-69, 160], [-69, 116], [-64, 76], [-55, 32], [-48, 36], [-55, 76], [-58, 116], [-57, 160], [-54, 210]]), c: TROU.t }], { w: 10, len: 40, seed: 904, a: 1.5, imp: 0.15 });
  const NEAR_LEG = mpl([[-6, 208], [52, 212], [56, 172], [52, 124], [50, 106], [48, 62], [46, 28], [16, 26], [12, 64], [10, 106], [4, 150], [-2, 186]]);
  paint(NEAR_LEG, [{ c: TROU.d }, { p: mpl([[8, 206], [26, 208], [28, 160], [26, 114], [13, 112], [9, 160]]), c: TROU.m },
    { p: mpl([[62, 216], [65, 172], [61, 124], [59, 106], [57, 62], [55, 22], [43, 26], [44, 62], [45, 106], [47, 124], [50, 172], [47, 216]]), c: TROU.w }], { w: 10, len: 40, seed: 910, a: 1.56, imp: 0.15 });
  add([ms([[-58, 121], [-48, 116], [-38, 118]], 1.2, "#0b0b12", 912, undefined, 0.05, 0.3), ms([[-56, 112], [-46, 106]], 1.4, "#3a7f88", 913, undefined, 0.4), ms([[16, 111], [28, 106], [42, 110]], 1.2, "#0b0b12", 914, undefined, 0.05, 0.3), ms([[-48, 46], [-38, 42], [-28, 45]], 1.2, "#0b0b12", 915, undefined, 0.05, 0.3), ms([[18, 36], [30, 32], [44, 35]], 1.2, "#0b0b12", 916, undefined, 0.05, 0.3)], [FAR_LEG, NEAR_LEG]);
  // shoes
  const FAR_SHOE = mpl([[-24, 41], [-22, 18], [-34, 8], [-62, 3], [-84, 5], [-88, 15], [-74, 26], [-50, 39]]);
  paint(FAR_SHOE, [{ c: "#101016", a: 0.1 }, { p: mpl([[-92, 28], [-64, 32], [-66, 14], [-90, 10]]), c: "#1f5560", a: 0.1 }], { w: 8, len: 24, seed: 918, imp: 0.15 });
  const NEAR_SHOE = mpl([[46, 31], [48, 9], [40, -1], [12, -9], [-8, -7], [-12, 3], [0, 13], [16, 28]]);
  paint(NEAR_SHOE, [{ c: "#101016", a: 0.25 }, { p: mpl([[32, 34], [52, 34], [52, -4], [38, -6]]), c: "#6a3e30", a: 1.4 }], { w: 8, len: 24, seed: 922, imp: 0.15 });
  add([ms([[-86, 6], [-62, 3], [-34, 8]], 2, "#56606e", 924, "#2a2c38", 0.3), ms([[-10, -6], [12, -9], [40, -2]], 2, "#56606e", 925, "#7a5040", 0.3), ms([[-82, 17], [-74, 23]], 3, "#4fc4bd", 926, undefined, 0.6), ms([[-8, 3], [0, 10]], 2.6, "#3a8a8c", 927, undefined, 0.5), ms([[-60, 26], [-48, 32], [-36, 34]], 1.4, "#3a4452", 928, undefined, 0.2), ms([[4, 16], [14, 23], [28, 27]], 1.4, "#3a4452", 929, undefined, 0.2)]);
  // the T-shirt: planes that go round the trunk, not down it. Teal where the screen finds the
  // shoulder, chest and belly; a dark core; olive-gold where the lamp reaches round the near side.
  const TOR = mpl([[-22, 347], [-46, 343], [-61, 334], [-66, 312], [-62, 290], [-60, 262], [-60, 238], [-56, 208], [-22, 203], [20, 205], [52, 210], [54, 240], [56, 270], [60, 300], [67, 318], [65, 333], [44, 344], [24, 350], [2, 344], [-12, 343]]);
  paint(TOR, [{ c: TEE.tm },
    { p: mpl([[-72, 342], [-40, 350], [-16, 348], [-25, 320], [-20, 292], [-30, 262], [-25, 232], [-32, 198], [-72, 198]]), c: TEE.tm2 },
    { p: mpl([[-64, 338], [-40, 348], [-24, 342], [-31, 318], [-50, 311], [-66, 320]]), c: TEE.tl, a: 0.4 },
    { p: mpl([[-62, 238], [-42, 240], [-35, 224], [-40, 204], [-60, 206]]), c: TEE.tl, a: 1.2 },
    { p: mpl([[12, 354], [22, 322], [15, 290], [24, 258], [17, 228], [26, 196], [76, 196], [76, 354]]), c: TEE.td },
    { p: mpl([[33, 354], [39, 318], [33, 288], [41, 256], [36, 226], [43, 196], [76, 196], [76, 354]]), c: TEE.core }], { w: 11, len: 36, seed: 930, a: 1.45, imp: 0.25 });
  add([ms([[-40, 306], [-24, 296], [-10, 300]], 2.4, "#1a8c86", 940, TEE.td, 0.15, 0.4), ms([[-56, 209], [-22, 203], [20, 205], [52, 210]], 3, "#0c3038", 943, "#3a3a30", 0.1), ms([[-22, 348], [-10, 342], [4, 343], [24, 350]], 4.5, "#0f5a5c", 944, "#0c3a40", 0.2), ms([[-48, 228], [-30, 222], [-8, 226]], 2, TEE.td, 945, undefined, 0.1, 0.4)], [TOR]);
  // far arm (his right): sleeve, upper arm, the forearm brought forward with the mug
  const F_SLEEVE = mpl([[-46, 344], [-64, 336], [-76, 316], [-81, 291], [-62, 283], [-55, 302]]);
  paint(F_SLEEVE, [{ c: TEE.tl, a: 1.2 }, { p: mpl([[-62, 346], [-48, 346], [-52, 280], [-68, 282], [-62, 312]]), c: TEE.tm2, a: 1.2 }], { w: 9, len: 26, seed: 950, imp: 0.3 });
  const F_UPPER = mpl([[-80, 292], [-61, 285], [-57, 262], [-63, 244], [-83, 250]]);
  paint(F_UPPER, [{ c: SKIN.tm, a: 1.4 }, { p: mpl([[-88, 296], [-74, 296], [-71, 266], [-74, 240], [-88, 244]]), c: SKIN.tl, a: 1.4 }, { p: mpl([[-66, 290], [-54, 286], [-54, 240], [-66, 240], [-62, 264]]), c: SKIN.td, a: 1.4 }], { w: 7, len: 20, seed: 954, imp: 0.3 });
  const F_FORE = mpl([[-59, 264], [-64, 243], [-96, 254], [-100, 275], [-82, 277]]);
  paint(F_FORE, [{ c: SKIN.tm, a: 0.2 }, { p: mpl([[-104, 280], [-58, 282], [-60, 268], [-82, 268], [-104, 264]]), c: SKIN.tl, a: 0.2 }, { p: mpl([[-104, 254], [-58, 250], [-58, 240], [-104, 246]]), c: SKIN.td, a: 0.2 }], { w: 7, len: 20, seed: 958, imp: 0.3 });
  add([ms([[-81, 290], [-62, 284]], 2.6, "#0f5a5c", 962, undefined, 0.1)]);
  // the mug in his hand
  const HMUG = mp([[-127, 292], [-95, 292], [-96, 254], [-101, 247], [-121, 247], [-126, 254]]);
  paint(HMUG, [{ c: "#55687a", a: 1.57 }, { p: mp([[-130, 296], [-108, 296], [-108, 244], [-130, 244]]), c: "#bfeee0", a: 1.57 }, { p: mp([[-130, 296], [-121, 296], [-121, 244], [-130, 244]]), c: "#e8fff8", a: 1.57 }], { w: 7, len: 26, seed: 964, imp: 0.35 });
  paint(mp(ell(-111, 292, 16, 5.2, 16)), [{ c: "#1d232c", a: 0 }], { w: 5, len: 14, seed: 968, imp: 0.1 });
  add([st(mp(ell(-111, 292, 16, 5.2, 16)).slice(4, 13), 1.8, "#e8fff8", 970, "#9fd8cc", 0.5)]);
  // the hand round it: the back of the hand at the mug's right, four fingers across the front, the thumb on the rim
  paint(mpl([[-101, 278], [-88, 282], [-85, 264], [-90, 250], [-100, 252]]), [{ c: SKIN.tm, a: 1.3 }, { p: mp([[-104, 284], [-84, 286], [-84, 272], [-104, 270]]), c: SKIN.tl, a: 0.3 }], { w: 6, len: 14, seed: 972, imp: 0.3 });
  add([0, 1, 2, 3].flatMap((i) => { const h = 281.5 - i * 8.6; return [ms([[-91, h + 1], [-103, h + 1.5], [-115 + i * 1.5, h - 0.5]], 7.6, mix(SKIN.tl, SKIN.tm, i * 0.3), 976 + i, mix(SKIN.tl, "#e0f4e4", 0.4 - i * 0.1), 0.35, 0.02, 1.4), ms([[-92, h - 3.4], [-104, h - 3], [-113 + i * 1.5, h - 4.4]], 1.3, "#274650", 982 + i, undefined, 0.05, 0.1, 1)]; }).concat([ms([[-90, 287], [-98, 293.5], [-107, 294.5]], 7, SKIN.tl, 988, "#d8f0e0", 0.4, 0.02, 1.4), ms([[-91, 283.5], [-100, 289.5], [-108, 290.5]], 1.2, "#274650", 989, undefined, 0.05, 0.1, 1)]));
  // near arm (his left): sleeve, the forearm hanging with an easy elbow, the open hand
  const N_SLEEVE = mpl([[44, 345], [64, 337], [78, 318], [85, 290], [64, 279], [55, 300]]);
  paint(N_SLEEVE, [{ c: TEE.core, a: 1.4 }, { p: mpl([[64, 350], [92, 350], [92, 276], [74, 276], [68, 312]]), c: TEE.wm, a: 1.4 }], { w: 9, len: 26, seed: 990, imp: 0.3 });
  const N_FORE = mpl([[64, 287], [85, 291], [92, 262], [87, 232], [78, 205], [63, 205], [63, 232], [65, 262]]);
  paint(N_FORE, [{ c: SKIN.wm, a: 1.5 }, { p: mpl([[56, 294], [69, 294], [71, 262], [69, 232], [66, 200], [56, 200]]), c: "#8a5244", a: 1.5 }, { p: mpl([[83, 296], [96, 296], [96, 236], [87, 240], [86, 266]]), c: SKIN.wl, a: 1.5 }], { w: 8, len: 26, seed: 994, imp: 0.3 });
  add([ms([[64, 281], [85, 290]], 2.6, "#0a2c34", 998, "#5a5238", 0.1), ms([[80, 266], [87, 262], [90, 256]], 1.3, "#a05a3c", 999, undefined, 0.1, 0.3), ms([[64, 207], [71, 204.5], [78, 206.5]], 1.2, "#a05a3c", 996, undefined, 0.1, 0.3)]);
  const N_HAND = mpl([[58, 207], [81, 206], [86, 187], [83, 168], [63, 164], [56, 182]]);
  paint(N_HAND, [{ c: SKIN.wm, a: 1.5 }, { p: mpl([[52, 212], [65, 212], [66, 186], [63, 158], [52, 160]]), c: "#8a5244", a: 1.5 }], { w: 7, len: 16, seed: 1000, imp: 0.3 });
  const FING: [number[][], number, string, string][] = [
    [[[57, 197], [48, 183], [47, 167]], 8.4, "#7a463e", "#8a5244"],                     // thumb
    [[[60, 169], [55.5, 153], [54, 138]], 7.4, "#8a5244", "#9a5c48"],                   // index
    [[[67, 166], [64, 149], [63, 132]], 7.6, "#c27a54", "#cc8258"],                     // middle
    [[[74, 167], [73.5, 151], [73.5, 135]], 7.4, SKIN.wm, "#d98a58"],                   // ring
    [[[81, 171], [82.5, 158], [84, 146]], 6.6, SKIN.wm, SKIN.wl],                       // little
  ];
  add(FING.map(([a, w, c0, c1], i) => ms(a, w, c0, 1004 + i, c1, 0.3, 0.02, 1.4)));
  add([ms([[63.5, 160], [61, 150], [59.5, 141]], 1, "#3a1c22", 1010, undefined, 0.05, 0.1, 1), ms([[70.5, 160], [69.5, 148], [68.5, 138]], 1, "#4a2424", 1011, undefined, 0.05, 0.1, 1), ms([[77.6, 163], [77.8, 154], [78.4, 147]], 1, "#5a2c26", 1012, undefined, 0.05, 0.1, 1), ms([[53.5, 192], [52.5, 182], [52.5, 174]], 1, "#2e1820", 1013, undefined, 0.05, 0.1, 1),
    ms([[85, 168], [86.5, 154], [86, 148]], 1.4, "#ffd2a0", 1015, undefined, 0.6), ms([[61, 167.5], [62, 166.5]], 2.2, "#b87458", 1014, undefined, 0.4), ms([[68, 164.5], [69, 164]], 2.2, "#e8a06a", 1016, undefined, 0.4), ms([[75, 165.5], [76, 165.5]], 2.2, "#ffc088", 1017, undefined, 0.4)]);
  // neck
  paint(mpl([[-6, 356], [22, 374], [27, 352], [22, 340], [-8, 340]]), [{ c: "#55343c", a: 1.3 }, { p: mp([[17, 378], [30, 378], [30, 338], [19, 338]]), c: "#c97f52", a: 1.3 }], { w: 7, len: 16, seed: 1020, imp: 0.25 });
  // the grey short sides: cropped hair, painted down the skull
  const SIDES = mpl([[14, 414], [4, 428], [-10, 436], [0, 441], [18, 443], [33, 437], [39, 424], [40, 408], [37, 392], [31, 379], [24, 372], [22, 384], [18, 392], [16, 402]]);
  paint(SIDES, [{ c: "#716f76", a: 1.35 }, { p: mpl([[-12, 446], [8, 446], [20, 404], [14, 398], [2, 426]]), c: "#4d4b54", a: 1.2 }, { p: mpl([[30, 446], [46, 446], [46, 370], [28, 372], [33, 408]]), c: "#c79a78", a: 1.5 }], { w: 5, len: 11, seed: 1026, imp: 0.25 });
  // the face: a teal front, a plum core that follows brow and cheekbone, a lamp-lit cheek
  const FACE = mpl([[-44, 438], [-51, 426], [-54, 415], [-52, 408], [-55, 400], [-54, 392], [-50, 384], [-36, 383], [-22, 380], [-6, 384], [8, 392], [16, 402], [14, 414], [4, 428], [-10, 436], [-28, 440]]);
  paint(FACE, [{ c: SKIN.tm, a: 1.2 },
    { p: mpl([[-56, 442], [-18, 444], [-13, 426], [-28, 417], [-56, 418]]), c: SKIN.tl, a: -0.1 },
    { p: mpl([[-34, 399], [-13, 400], [-11, 388], [-23, 380], [-37, 383]]), c: SKIN.tl, a: 1.0 },
    { p: mpl([[-56, 402], [-46, 402], [-46, 384], [-56, 384]]), c: SKIN.tl, a: 1.2 },
    { p: mpl([[-12, 446], [-2, 446], [3, 424], [0, 410], [7, 398], [3, 378], [-9, 378], [-4, 396], [-9, 409], [-7, 424]]), c: SKIN.td, a: 1.45 },
    { p: mpl([[-3, 446], [26, 446], [26, 378], [2, 379], [6.5, 398], [-0.5, 410], [2.5, 424]]), c: SKIN.wm, a: 1.5 },
    { p: mpl([[9, 446], [26, 446], [26, 380], [10, 386], [13, 410]]), c: SKIN.wl, a: 1.5 },
    { p: mpl([[-4.5, 412], [-0.5, 410], [6.5, 398], [2.5, 380], [-3.5, 380], [1, 397], [-4, 407]]), c: "#5a3d48", a: 1.3 }], { w: 5.5, len: 13, seed: 1032, imp: 0.3 });
  // far eye and far lens go down before the nose crosses them
  add([ms([[-54, 404.5], [-50, 405.5], [-46.5, 404]], 4.6, "#d2ede2", 1040, undefined, 0.2, 0, 1.4), ms([[-52.5, 404.3], [-50.5, 404.3]], 4, "#17121c", 1041, undefined, 0.1, 0, 1.4), ms([[-55, 407], [-50, 408.6], [-46, 407]], 1.5, INK, 1042, undefined, 0.05, 0, 1.2)]);
  add([ms([[-44, 412.5], [-54, 413], [-57.5, 409], [-58, 403]], 2.6, INK, 1043, undefined, 0.1, 0, 1.3), ms([[-58, 403], [-57, 396], [-53, 393.5], [-45, 393.5]], 2.6, INK, 1045, undefined, 0.1, 0, 1.3), ms([[-55, 418], [-45, 419]], 3.6, "#15121a", 1044, undefined, 0.1, 0, 1.3)]);
  // the ear, lamp-lit, its rim glowing where the light comes through
  const EAR = mpl([[18, 412], [24, 418], [31, 414], [32.5, 403], [28, 393], [21, 390], [18, 397]]);
  paint(EAR, [{ c: SKIN.wm, a: 1.4 }, { p: mp([[25, 420], [36, 420], [36, 388], [27, 388]]), c: "#ff9a62", a: 1.4 }], { w: 5, len: 12, seed: 1054, imp: 0.3 });
  add([ms([[22, 411], [27, 409], [28, 400], [24, 396]], 2.2, "#7a3a34", 1058, "#8a4438", 0.1), ms([[24, 417.5], [31, 414], [32.5, 403]], 1.6, "#ffd8a4", 1059, undefined, 0.6)]);
  // the beard: dark and full, painted the way it grows; teal on the chin and moustache, lamp on the jaw
  const BEARD = mpl([[17, 405], [9, 393], [-5, 385], [-20, 381], [-34, 384], [-44, 384.5], [-53, 383], [-56, 376], [-55, 364], [-50, 350], [-38, 342], [-20, 341], [0, 346], [14, 356], [23, 370], [24, 388], [19, 393]]);
  paint(BEARD, [{ c: "#15131b", a: 1.25 }, { p: mpl([[-60, 388], [-36, 388], [-27, 372], [-30, 352], [-42, 338], [-60, 348]]), c: "#183940", a: 1.4 }, { p: mpl([[-60, 380], [-49, 380], [-47, 366], [-51, 348], [-60, 352]]), c: "#22565e", a: 1.4 }, { p: mpl([[12, 372], [28, 392], [28, 362], [16, 350], [6, 348], [10, 360]]), c: "#3c2620", a: 0.9 }], { w: 4.5, len: 12, seed: 1062, imp: 0.25 });
  add([ms([[-55, 376.5], [-48, 375], [-40, 376.5]], 2.2, "#08070c", 1070, undefined, 0.05, 0, 1.3), ms([[-52, 371.5], [-47, 370.5], [-42, 372]], 3.4, "#98b4a4", 1071, "#84a094", 0.3, 0, 1.4), ms([[-54, 380], [-47, 381.5], [-40, 380], [-34, 381]], 2.6, "#1a2f38", 1072, undefined, 0.1, 0.1), ms([[14, 360], [22, 372], [23.5, 386]], 2, "#c9783f", 1073, "#8a5030", 0.5, 0.2),
    ms([[-20, 378], [-16, 364], [-18, 350]], 1.4, "#2c2a36", 1074, undefined, 0.2, 0.4), ms([[-6, 380], [-2, 366], [-4, 352]], 1.4, "#2a2630", 1075, undefined, 0.2, 0.4), ms([[-44, 364], [-42, 354], [-36, 346]], 1.3, "#3f8a90", 1076, undefined, 0.4, 0.3)], [BEARD]);
  // the nose: lit ridge, shadowed near side, dark underside
  const NOSE = mpl([[-40, 411], [-50, 399], [-59, 389], [-57, 383], [-47, 381], [-41, 385], [-37, 397], [-34, 409]]);
  paint(NOSE, [{ c: SKIN.td, a: 1.0 }, { p: mpl([[-42, 414], [-52, 400], [-62, 388], [-58, 380], [-52, 384], [-45, 398], [-37, 412]]), c: SKIN.tl, a: 0.9 }], { w: 5, len: 12, seed: 1046, imp: 0.3 });
  add([ms([[-56, 383.5], [-49, 381.5], [-43, 385]], 2, "#2a2030", 1050, undefined, 0.05, 0, 1.2), ms([[-45, 407], [-51, 398], [-57, 390]], 1.8, "#def6ea", 1051, undefined, 0.6)]);
  // the quiff: black hair standing up off the forehead and swept back, drawn strand by strand;
  // the screen is only a sheen on its front, the lamp only an edge along its back
  const QUIFF = mpl([[-46, 437], [-54, 452], [-50, 468], [-36, 480], [-14, 482], [8, 476], [26, 466], [38, 452], [42, 436], [34, 437], [18, 443], [0, 441], [-10, 437], [-28, 441]]);
  paint(QUIFF, [{ c: "#121118", a: -0.8, amt: 0.06 }], { w: 6, len: 22, seed: 1078, imp: 0.25 });
  add([ms([[-45, 440], [-50, 460], [-36, 477]], 4, "#1c444e", 1080, "#18303a", 0.3, 0.2), ms([[-36, 441], [-40, 462], [-20, 479]], 4, "#17333c", 1081, "#14141c", 0.3, 0.25), ms([[-24, 442], [-24, 462], [-2, 477]], 4, "#16161f", 1082, "#1a1a24", 0.3, 0.25), ms([[-10, 440], [-6, 458], [14, 471]], 4, "#191820", 1083, "#16161f", 0.3, 0.25), ms([[6, 443], [12, 456], [28, 462]], 4, "#1f1a20", 1084, "#2c1e1c", 0.3, 0.25), ms([[20, 444], [30, 451], [38, 449]], 3.6, "#2c1e1c", 1085, "#4a2c22", 0.3, 0.25),
    ms([[-47, 442], [-51, 458], [-41, 471]], 1.6, "#4fc4bd", 1086, "#2a8088", 0.6, 0.2), ms([[-40, 444], [-43, 460], [-30, 474]], 1.2, "#3aa0a0", 1087, "#1b4f58", 0.5, 0.3), ms([[-30, 446], [-30, 462], [-14, 476]], 1, "#2a7078", 1088, "#16323a", 0.4, 0.4), ms([[10, 475], [26, 465], [38, 451], [41, 438]], 2, "#f09a50", 1089, "#c06a34", 0.6, 0.15), ms([[-10, 437], [0, 441], [18, 443], [33, 437]], 1.6, "#0a090e", 1077, undefined, 0.05, 0.2)], [QUIFF]);
  // near eye, brows, the glasses last
  add([ms([[-25.5, 404], [-19, 405.6], [-11.5, 403.6]], 5.6, "#d8f0e4", 1090, "#bcd6c8", 0.2, 0, 1.4), ms([[-24, 404.4], [-20.4, 404.4]], 5, "#17121c", 1091, undefined, 0.1, 0, 1.4), ms([[-26.5, 407.4], [-19, 409.2], [-11, 406.6]], 1.7, INK, 1092, undefined, 0.05, 0, 1.2), ms([[-25, 401.4], [-18, 400.6], [-12, 401.8]], 1, "#4a6a70", 1093, undefined, 0.05, 0, 1.1), ms([[-23.4, 405.6], [-22.6, 405.8]], 1.5, "#f4fffb", 1094, undefined, 0.8, 0, 1.5), ms([[-52.4, 405.4], [-51.8, 405.5]], 1.2, "#f4fffb", 1095, undefined, 0.8, 0, 1.5)]);
  add([ms([[-34, 418], [-20, 420.5], [-7, 418.5]], 4.4, "#14111a", 1096, "#1c1820", 0.15, 0.05, 1.3)]);
  const LENS = mp([[-32, 413], [-19, 414], [-6, 413], [-5, 403], [-7, 394], [-19, 392.5], [-31, 394], [-33, 403]]);
  add([...broken([...sm(LENS), sm(LENS)[0]], 3, 1100, INK, 0, 0.12), ms([[-44, 408], [-38, 409.5], [-32, 408]], 2.6, INK, 1101, undefined, 0.1, 0, 1.3), ms([[-5, 409], [8, 410], [21, 409]], 2.6, INK, 1102, "#2a1c1c", 0.1, 0, 1.3),
    ms([[-29, 410.5], [-25, 400]], 1.4, "#c8fff4", 1103, undefined, 0.5, 0.3), ms([[-55, 410.5], [-53, 401]], 1.2, "#c8fff4", 1104, undefined, 0.5, 0.3), ms([[-32, 413.8], [-19, 414.8], [-6, 413.8]], 1.1, "#5fd0c8", 1105, undefined, 0.5, 0.2)]);
  // rim lights, fat and last: the screen down his left contour, the lamp down his right
  add([ms([[-62, 334], [-76, 316], [-81, 292]], 2.6, "#9ff5e6", 1110, undefined, 0.7, 0.15), ms([[-84, 286], [-86, 266], [-83, 252]], 2.2, "#d4f6e8", 1111, undefined, 0.7, 0.2), ms([[-61, 204], [-64, 160], [-63.5, 118]], 2.2, "#48b8b4", 1112, "#2f8088", 0.6, 0.3), ms([[-61, 108], [-58, 76], [-51, 40]], 2, "#48b8b4", 1113, "#2f8088", 0.6, 0.3),
    ms([[66, 334], [78, 318], [85, 292]], 2.6, "#ffc27a", 1114, undefined, 0.7, 0.15), ms([[88.5, 286], [90, 262], [86, 232], [81, 208]], 2.2, "#ffd8a4", 1115, undefined, 0.7, 0.2), ms([[53, 210], [56, 172], [52, 124]], 2.2, "#e89a52", 1116, "#b06a3a", 0.6, 0.3), ms([[50, 106], [48, 62], [46, 32]], 2, "#e89a52", 1117, "#b06a3a", 0.6, 0.3),
    ms([[39.5, 426], [40.5, 408], [37.5, 392], [31, 380]], 2.2, "#ffc27a", 1118, "#f0a060", 0.7, 0.15), ms([[-50, 428], [-53.5, 416]], 1.8, "#def6ea", 1119, undefined, 0.6)]);
  // the broken dark line, where forms overlap in shadow
  add([...broken(mp([[4, 184], [-6, 150], [-14, 116], [-20, 76], [-23, 40]]), 2.2, 1120, INK, 0.2), ...broken(mp([[-60, 262], [-60, 238], [-56, 210]]), 1.8, 1121, "#0c3038", 0.3), ...broken(mp([[56, 300], [55, 262], [54, 236], [52, 212]]), 2.2, 1122, INK, 0.2), ...broken(mp([[-100, 252], [-90, 250], [-86, 264]]), 1.6, 1123, "#1f3a44", 0.2),
    ...broken(mp([[-56, 364], [-50, 350], [-38, 342], [-20, 341], [0, 346]]), 2, 1124, INK, 0.25), ...broken(mp([[-127, 292], [-126, 254], [-121, 247], [-101, 247]]), 1.6, 1125, "#33495a", 0.3), ...broken(mp([[58, 206], [56, 182], [61, 166]]), 1.5, 1126, "#2e1820", 0.3)]);

  // ============================================================ 11. the dog
  const dp = (a: number[][]): P[] => a.map(([x, h]) => [DCX + x * DK, DGY - h * DK] as P);
  const ds = (a: number[][], w: number, c0: string, seed: number, c1 = c0, imp = 0.3, dry = 0.08, load = 1.25) => st(dp(a), w * DK, c0, seed, c1, imp, dry, load);
  const COAT = { l: "#f6a44c", m: "#cf6f2c", s: "#7a3c30", d: "#4c2a32" }, CREAM = { l: "#ffe4ba", m: "#dcb894", s: "#93797a" };
  // the head's own frame: forward to the nose, up through the crown, thrown back 40 degrees to look up
  const TH0 = deg(40), HX = -14, HH = 160, HS = 1.16, hp = (a: number[][]): number[][] => a.map(([f, v]) => [HX + HS * (-f * Math.cos(TH0) + v * Math.sin(TH0)), HH + HS * (f * Math.sin(TH0) + v * Math.cos(TH0))]);
  add([ds([[-48, 2], [-10, -5], [30, -3], [62, 2]], 13, "#1a1014", 1200, undefined, 0.05, 0.3)]);
  // far foreleg and far ear, behind everything
  paint(sm(dp([[-36, 66], [-23, 64], [-25, 30], [-26, 9], [-30, 2], [-45, 2], [-47, 10], [-39, 30]])), [{ c: CREAM.s, a: 1.5 }, { p: dp([[-50, 70], [-40, 70], [-36, 0], [-50, 0]]), c: "#b89a8c", a: 1.5 }], { w: 6, len: 20, seed: 1204, imp: 0.2 });
  paint(sm(dp(hp([[10, 20], [-4, 23], [0, 44]]))), [{ c: "#9a4c2c", a: -1.2 }], { w: 5, len: 14, seed: 1208, imp: 0.2 });
  // the body: one sitting mass, a lit plane down the back, a shadow plane under the belly and haunch
  const BODY = sm(dp([[-30, 120], [-39, 100], [-37, 78], [-30, 58], [-10, 50], [8, 36], [12, 12], [40, 3], [70, 6], [83, 26], [81, 50], [67, 78], [42, 104], [16, 122], [-6, 128]]));
  paint(BODY, [{ c: COAT.m, a: 0.95 }, { p: dp([[-10, 134], [16, 128], [44, 110], [70, 82], [86, 50], [70, 44], [56, 70], [34, 94], [12, 110], [-10, 116]]), c: COAT.l, a: 0.85 }, { p: dp([[-34, 56], [8, 44], [22, 28], [50, 22], [86, 26], [86, -4], [-34, -4]]), c: COAT.s, a: 0.2 }, { p: dp([[-44, 126], [-28, 124], [-16, 118], [-20, 90], [-20, 56], [-34, 54], [-44, 78]]), c: CREAM.m, a: 1.4 }, { p: dp([[-44, 126], [-30, 124], [-33, 96], [-34, 54], [-44, 78]]), c: CREAM.l, a: 1.4 }], { w: 9, len: 26, seed: 1212, imp: 0.3 });
  add([...broken(dp([[4, 54], [22, 66], [44, 64], [62, 44], [66, 22]]), 2.2, 1220, "#5a2a26", 0.15), ds([[10, 50], [28, 60], [46, 58]], 3, COAT.l, 1221, COAT.m, 0.5, 0.3)], [BODY]);
  // the tail: a curl sitting up on the back
  const TAIL = sm(dp([[62, 74], [80, 78], [94, 96], [90, 116], [74, 128], [56, 122], [48, 106], [54, 90]]));
  paint(TAIL, [{ c: COAT.m, a: 0.6 }, { p: dp([[44, 132], [78, 132], [66, 100], [44, 96]]), c: COAT.l, a: -0.6 }, { p: dp([[80, 90], [98, 90], [98, 70], [60, 70]]), c: COAT.s, a: 0.3 }], { w: 7, len: 18, seed: 1224, imp: 0.3 });
  add([ds([[62, 98], [72, 108], [82, 100], [78, 90]], 5.5, CREAM.l, 1230, CREAM.m, 0.45), ...broken(dp([[60, 96], [70, 107], [82, 102], [80, 90], [68, 86]]), 1.8, 1231, "#5a2a26", 0.2)]);
  // hind foot, flat on the ground, and the near foreleg, straight
  paint(sm(dp([[6, 13], [8, 2], [46, 2], [55, 9], [30, 15]])), [{ c: CREAM.s, a: 0 }, { p: dp([[4, 18], [34, 18], [34, 8], [4, 8]]), c: CREAM.m, a: 0 }], { w: 5, len: 16, seed: 1234, imp: 0.25 });
  paint(sm(dp([[-19, 64], [-2, 62], [-4, 30], [-5, 10], [-2, 2], [-24, 2], [-26, 10], [-20, 30]])), [{ c: COAT.m, a: 1.5 }, { p: dp([[-28, 68], [-15, 68], [-16, 0], [-28, 0]]), c: CREAM.l, a: 1.5 }, { p: dp([[-8, 68], [0, 68], [0, 0], [-8, 0]]), c: COAT.s, a: 1.5 }], { w: 6, len: 20, seed: 1238, imp: 0.3 });
  add([ds([[-19, 9], [-19, 3]], 1.3, "#5a3a34", 1244, undefined, 0.05), ds([[-13, 9], [-13, 3]], 1.3, "#5a3a34", 1245, undefined, 0.05), ds([[-7.5, 9], [-7.5, 3]], 1.3, "#5a3a34", 1246, undefined, 0.05), ds([[-41, 9], [-41, 4]], 1.2, "#4a2f30", 1247, undefined, 0.05), ds([[-35, 9], [-35, 4]], 1.2, "#4a2f30", 1248, undefined, 0.05), ds([[14, 10], [14, 4]], 1.2, "#4a2f30", 1249, undefined, 0.05), ds([[20, 11], [20, 4]], 1.2, "#4a2f30", 1250, undefined, 0.05),
    ...broken(dp([[-2, 62], [-4, 30], [-5, 10]]), 1.8, 1251, "#5a2a26", 0.2), ...broken(dp([[-19, 62], [-21, 30], [-26, 10]]), 1.4, 1252, "#8a6a5c", 0.3)]);
  // the neck, thick, carrying the head back
  const NECK = sm(dp([[-32, 122], [-8, 130], [16, 124], [12, 150], [-2, 166], [-30, 152], [-40, 136]]));
  paint(NECK, [{ c: COAT.m, a: 1.1 }, { p: dp([[0, 172], [20, 172], [20, 120], [4, 122]]), c: COAT.l, a: 1.2 }, { p: dp([[-46, 160], [-24, 160], [-20, 118], [-46, 118]]), c: CREAM.m, a: 1.2 }], { w: 8, len: 22, seed: 1254, imp: 0.3 });
  // the head: broad skull, full cream cheek, a short blunt muzzle
  const SKULL = sm(dp(hp([[20, 11], [8, 22], [-10, 24], [-24, 12], [-25, -8], [-14, -23], [6, -27], [22, -19], [27, -4]])));
  paint(SKULL, [{ c: COAT.m, a: -0.7 }, { p: dp(hp([[30, 30], [-30, 30], [-30, 8], [30, 6]])), c: COAT.l, a: -0.7 }, { p: dp(hp([[30, -4], [8, -2], [-8, -10], [-14, -30], [30, -30]])), c: CREAM.m, a: -0.5 }, { p: dp(hp([[30, -4], [10, -3], [0, -10], [0, -30], [30, -30]])), c: CREAM.l, a: -0.5 }], { w: 6.5, len: 16, seed: 1260, imp: 0.3 });
  const MUZ = sm(dp(hp([[14, 12], [28, 11], [37, 8.5], [41, 2.5], [39.5, -6], [30, -12], [14, -15]])));
  paint(MUZ, [{ c: CREAM.m, a: -0.7 }, { p: dp(hp([[10, 17], [46, 13], [46, 3.5], [10, 5]])), c: COAT.l, a: -0.7 }, { p: dp(hp([[10, -4], [46, -2], [46, -19], [10, -19]])), c: CREAM.l, a: -0.7 }], { w: 5, len: 14, seed: 1268, imp: 0.3 });
  const JAW = sm(dp(hp([[16, -12], [30, -10.5], [37, -8.5], [36.5, -14], [27, -19.5], [14, -21]])));
  paint(JAW, [{ c: CREAM.m, a: -0.7 }], { w: 4, len: 10, seed: 1272, imp: 0.2 });
  // near ear: small, thick, pricked, its cream inside toward the front
  const EARN = sm(dp(hp([[6, 20], [-6, 24], [-18, 17], [-13, 46], [-9, 47]])));
  paint(EARN, [{ c: COAT.m, a: -1.2 }, { p: dp(hp([[8, 18], [-2, 24], [-9, 50], [4, 50]])), c: COAT.l, a: -1.2 }], { w: 5, len: 14, seed: 1276, imp: 0.3 });
  add([ds(hp([[0, 25], [-7, 27], [-9, 40]]), 3.4, "#e8b094", 1280, "#c98a72", 0.3), ...broken(dp(hp([[-18, 17], [-14, 34], [-11, 46.5]])), 1.6, 1281, "#5a2a26", 0.15)]);
  // the collar
  add([ds([[-39, 139], [-22, 138], [-4, 146], [13, 153]], 8, "#168a86", 1284, "#37cdbd", 0.4, 0.02, 1.4), ds([[-39, 142.5], [-22, 141.5], [-4, 149.5], [12, 156]], 1.6, "#8ff0e0", 1285, undefined, 0.6, 0.2), ds([[-33, 132], [-32, 128]], 5, "#ffd27a", 1286, "#c98a3a", 0.7, 0, 1.4), ...broken(dp([[-39, 134.5], [-22, 133.5], [-4, 141.5], [13, 148.5]]), 1.6, 1287, "#0c3a40", 0.15)]);
  // eye, brow spot, nose, the mouth line with a turned-up corner
  add([ds(hp([[9.5, 9.5], [13.5, 10.5], [17.5, 9]]), 5, INK, 1290, undefined, 0.15, 0, 1.4), ds(hp([[11, 15.5], [15, 15.5]]), 3.4, CREAM.l, 1291, undefined, 0.4, 0, 1.3), ds(hp([[14.6, 10.8], [15.2, 10.9]]), 1.4, "#fff8e8", 1292, undefined, 0.8, 0, 1.5),
    ds(hp([[36.5, 7], [40.5, 4.5], [40.5, -0.5]]), 8, INK, 1293, undefined, 0.3, 0, 1.4), ds(hp([[38, 7.6], [40, 6.2]]), 1.4, "#8a9ab0", 1294, undefined, 0.6, 0, 1.3),
    ds(hp([[39, -6.5], [31, -10.5], [22, -11.5], [15.5, -8]]), 1.7, "#2a1820", 1295, undefined, 0.05, 0.05, 1.2), ds(hp([[40, -1.5], [39, -6.5]]), 1.5, "#2a1820", 1296, undefined, 0.05, 0, 1.2),
    ...broken(dp(hp([[14, 12.5], [27, 11.5], [36, 9]])), 1.5, 1297, "#8a4428", 0.3), ...broken(dp(hp([[-24, -8], [-12, -22], [8, -24]])), 1.6, 1298, "#5a2a26", 0.35)]);
  // lamp light on him, fat and last: crown, nape, the back's edge, the top of the tail
  add([ds(hp([[16, 12], [4, 23.5], [-10, 25]]), 2.4, "#ffd49a", 1300, undefined, 0.7, 0.2), ds([[16, 124], [42, 105], [60, 86]], 2.4, "#ffd49a", 1301, "#ffb866", 0.7, 0.25), ds([[50, 108], [58, 122.5], [74, 128.5]], 2.2, "#ffd49a", 1302, undefined, 0.7, 0.2), ds(hp([[6, 21], [-4, 36], [-9, 47]]), 1.8, "#ffd49a", 1303, undefined, 0.7, 0.2), ds([[-40, 100], [-38.5, 80], [-32, 60]], 1.8, "#fff0d0", 1304, undefined, 0.6, 0.3)]);

  // ============================================================ 12. the last and brightest dabs
  add([st([[1270, 198.5], [1281, 200], [1292, 198.5]], 6, "#fffbe8", 1400, "#fff3c8", 1, 0, 1.5), st([[MX - 100, 104], [MX - 60, 103]], 2.6, "#e8fff8", 1401, undefined, 0.8, 0.3), st([[MX + 60, 106], [MX + 104, 105]], 3, "#f0fffa", 1402, undefined, 0.9, 0.2)]);
  return S;
};

// ---------------------------------------------------------------- the picture
let STAGES: Stage[] | null = null;
const ring = (c: Ctx, p: P[]) => { c.moveTo(p[0][0], p[0][1]); for (let i = 1; i < p.length; i++) c.lineTo(p[i][0], p[i][1]); c.closePath(); };
export const drawOfficePaint = (ctx: Ctx, _frame: number, env: Env) => {
  const g = new Gfx(ctx, env, 0, OIL), c = g.cur, k = env.W / W;
  c.setTransform(env.scale, 0, 0, env.scale, 0, 0);
  c.fillStyle = "#2b2029"; c.fillRect(0, 0, env.W, env.H);   // the toned ground
  weave(g, 0.5);
  g.push(0, 0, k);
  for (const s of (STAGES ??= build())) {
    c.save();
    if (s.clip) { c.beginPath(); s.clip.forEach((p) => ring(c, p)); c.clip("nonzero"); if (s.within) { c.beginPath(); ring(c, s.within); c.clip(); } }
    s.base?.forEach(([p, col]) => { c.fillStyle = col; c.beginPath(); ring(c, p); c.fill(); });
    for (const x of s.strokes) oilStroke(g, x);
    c.restore();
  }
  g.pop();
  weave(g, 0.2);
};

export const officePaint: Film = {
  meta: { title: "officePaint", W, H, fps: 30, bpm: 60, durationFrames: 1, raster: "cpu" },
  assets: { images: {} },
  shots: [{ id: "officePaint", start: 0, end: 1, draw: drawOfficePaint }],
};
