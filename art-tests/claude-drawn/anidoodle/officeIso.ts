// RULED FIELD · "the office". Pixelfolio's test room, drawn in a hand adapted from the brand illustration
// set at hannah-meng.com/retool-brand (the "Build" tiles). The hand is borrowed, never a picture: the
// subject, the layout and every shape here are new (the reference shows abstract solids, no rooms, no people).
//
// MEDIUM RECIPE
// MARK: a closed flat plane on a true 2:1 isometric grid; a hairline in a tone of the field; a white solid.
// EDGE: vector-crisp. No contour line anywhere: tone meets tone.
// ORDER: one colour field edge to edge -> an iso grid ruled across the WHOLE field in a near tone ->
//   the dark mass (room shadow, walls) -> the light floor -> furniture in tonal steps of the field's hue ->
//   the white things (what matters: screen, paper, lamp, mug) -> one accent colour, used once (the hero's
//   shirt) -> a few hairline details.
// PAPER: none. A flat screen colour.
// PALETTE: one hue family per picture (field, two lighter, four darker), white, one accent. Frame 0 is the
//   orange family, frame 1 purple, frame 2 coral: one drawing, one map colour each.
// LIGHT: the cube rule only (top lightest, +y face middle, +x face darkest) plus flat cast shapes thrown to
//   the lower right. No gradients, no glow.
// NOT ITS NEIGHBOUR (isometric, "the night bake"): that plate uses material colours under a night ambient
//   with one warm light in distance bands. This one has no materials and no light source: the hue is the
//   picture, and the ruled hairline is the only texture.
// SUBJECT + REALISM: a 5 m x 4 m home office, 1 unit = 50 cm. Desk 75 cm high, 160 cm wide; monitor 55 cm;
//   chair seat 45 cm; shelf 170 cm; walls cut at 2.3 m. The man is authored in screen space over his foot
//   point, 4 heads tall (a cartoon canon, chosen to stay near his chunky game sprite): black quiff, grey
//   sides, glasses, beard, teal T-shirt, weight on both feet. The dog is a sitting shiba, head turned to him.
import type { Ctx, Env } from "./core";
import type { Film } from "./film";
import { Iso, type Mat, type P2, type P3 } from "./isometricKit";

type Fam = { F: string; L1: string; L2: string; D1: string; D2: string; D3: string; D4: string };
const FAMS: Fam[] = [
  { F: "#f0a23b", L1: "#f7c26b", L2: "#fde3b3", D1: "#dd8b25", D2: "#b9651c", D3: "#8c4717", D4: "#5a2c12" },
  { F: "#8f6fd6", L1: "#b29ae8", L2: "#e2d8f8", D1: "#7b5cc6", D2: "#5d42a3", D3: "#43307c", D4: "#2a1e52" },
  { F: "#ee7762", L1: "#f59d8c", L2: "#fbd3ca", D1: "#da614d", D2: "#b3463a", D3: "#86302c", D4: "#571d1f" },
];
const WHITE = "#ffffff", TEAL = "#1f8f93", TEAL_D = "#176d71", TEAL_L = "#3fb5b1";
const SKIN = "#f3c9a3", SKIN_D = "#dba57b", HAIR = "#1d1a22", GREY = "#a3a1ae", BEARD = "#3a2a26", TROUSER = "#2b2733", TROUSER_D = "#1c1921";

export const drawOfficeIso = (ctx: Ctx, frame: number, env: Env) => {
  const C = FAMS[frame % FAMS.length];
  ctx.setTransform(env.scale, 0, 0, env.scale, 0, 0);
  ctx.fillStyle = C.F; ctx.fillRect(0, 0, env.W, env.H);
  const iso = new Iso(ctx, 56, 912, 452);
  const box = (x0: number, y0: number, z0: number, x1: number, y1: number, z1: number, m: Mat) => iso.boxFaces(x0, y0, z0, x1, y1, z1, m).forEach((f) => iso.poly(f.pts, f.fill));
  const hair = (a: P3, b: P3, color: string, w = 1.5, alpha = 1) => iso.line(iso.p(...a), iso.p(...b), color, w, alpha);
  const white: Mat = { top: WHITE, left: C.L2, right: C.L1 };
  const dark: Mat = { top: C.D2, left: C.D3, right: C.D4 };
  const mid: Mat = { top: C.D1, left: C.D2, right: C.D3 };
  const shape = (pts: P2[], fill: string, alpha = 1) => iso.poly(pts, fill, alpha);
  const stroke = (pts: P2[], color: string, w: number, close = false) => { ctx.strokeStyle = color; ctx.lineWidth = w; ctx.lineJoin = "round"; ctx.lineCap = "round"; ctx.beginPath(); pts.forEach(([x, y], i) => (i ? ctx.lineTo(x, y) : ctx.moveTo(x, y))); if (close) ctx.closePath(); ctx.stroke(); };

  // 1. the field, ruled: an iso grid across everything, then one larger construction plate with its nodes
  for (let i = -30; i <= 42; i++) { hair([i, -30, 0], [i, 42, 0], C.D1, 1.25, 0.55); hair([-30, i, 0], [42, i, 0], C.D1, 1.25, 0.55); }
  const plate: P3[] = [[-2, -2, 0], [12, -2, 0], [12, 10, 0], [-2, 10, 0]];
  plate.forEach((a, i) => hair(a, plate[(i + 1) % 4], C.L1, 2));
  plate.forEach((a) => { const q = iso.p(...a); ctx.fillStyle = WHITE; ctx.beginPath(); ctx.arc(q[0], q[1], 6, 0, Math.PI * 2); ctx.fill(); });

  // 2. the dark mass: the room's shadow thrown lower right, the slab, the two cut walls
  iso.face([[10, 0, -0.4], [11.1, 0.9, -0.4], [11.1, 8.9, -0.4], [0.9, 8.9, -0.4], [0, 8, -0.4], [10, 8, -0.4]], C.D2, 0.75);
  box(0, 0, -0.4, 10, 8, 0, { top: C.L1, left: C.D2, right: C.D3 });
  for (let i = 1; i < 10; i++) hair([i, 0, 0], [i, 8, 0], C.F, 1.25, 0.9);
  for (let i = 1; i < 8; i++) hair([0, i, 0], [10, i, 0], C.F, 1.25, 0.9);
  box(-0.4, -0.4, -0.4, 10, 0, 4.6, { top: C.D4, left: C.D2, right: C.D4 });
  box(-0.4, 0, -0.4, 0, 8, 4.6, { top: C.D4, left: C.D4, right: C.D3 });
  for (let z = 1; z < 4.6; z += 1) { hair([0, 0, z], [10, 0, z], C.D3, 1.25, 0.8); hair([0, 0, z], [0, 8, z], C.D2, 1.25, 0.6); }

  // 3. on the walls: a window (white, the flat light it throws on the floor) and a framed print
  iso.face([[5.9, 0, 1.8], [8.3, 0, 1.8], [8.3, 0, 4.1], [5.9, 0, 4.1]], C.D4);
  iso.face([[6.02, 0, 1.92], [8.18, 0, 1.92], [8.18, 0, 3.98], [6.02, 0, 3.98]], WHITE);
  [[6.2, 0.45, 0.7], [6.72, 0.4, 1.25], [7.3, 0.5, 0.55], [7.85, 0.3, 0.95]].forEach(([x, w, h]) => iso.face([[x, 0, 1.92], [x + w, 0, 1.92], [x + w, 0, 1.92 + h], [x, 0, 1.92 + h]], C.L2));
  hair([7.1, 0, 1.92], [7.1, 0, 3.98], C.D4, 3); hair([6.02, 0, 3.0], [8.18, 0, 3.0], C.D4, 3);
  box(5.8, 0, 1.68, 8.4, 0.22, 1.8, white);
  iso.face([[6.5, 2.3, 0], [8.6, 2.3, 0], [9.5, 5.2, 0], [7.4, 5.2, 0]], WHITE, 0.45);
  iso.face([[0, 0.9, 2.3], [0, 2.7, 2.3], [0, 2.7, 4.2], [0, 0.9, 4.2]], WHITE);
  iso.face([[0, 1.05, 2.45], [0, 2.55, 2.45], [0, 2.55, 4.05], [0, 1.05, 4.05]], C.L2);
  iso.face([[0, 1.25, 2.6], [0, 2.35, 2.6], [0, 1.8, 3.5]], C.D2);
  { const q = iso.p(0, 2.05, 3.62); ctx.fillStyle = TEAL; ctx.beginPath(); ctx.ellipse(q[0], q[1], 13, 15, 0, 0, Math.PI * 2); ctx.fill(); }

  // 4. on the floor: the rug, ruled
  iso.face([[2.4, 3.7, 0], [7.4, 3.7, 0], [7.4, 6.9, 0], [2.4, 6.9, 0]], C.D2);
  const rb: P3[] = [[2.65, 3.95, 0], [7.15, 3.95, 0], [7.15, 6.65, 0], [2.65, 6.65, 0]];
  rb.forEach((a, i) => hair(a, rb[(i + 1) % 4], C.L1, 2));
  for (let k = 0; k < 5; k++) { const x = 3.3 + k * 0.8; iso.face([[x, 4.35, 0], [x + 0.5, 4.35, 0], [x + 0.5, 4.85, 0], [x, 4.85, 0]], C.L1); }

  // 5. the shelf against the left wall, open toward us
  iso.face([[0.7, 3.5, 0], [1.25, 4.0, 0], [1.25, 6.9, 0], [0.7, 6.4, 0]], C.D2, 0.55);
  box(0, 3.5, 0, 0.7, 6.4, 3.4, dark);
  iso.face([[0.7, 3.62, 0.15], [0.7, 6.28, 0.15], [0.7, 6.28, 3.28], [0.7, 3.62, 3.28]], C.D4);
  const books: [number, string][][] = [
    [[0.22, C.L1], [0.16, WHITE], [0.24, C.D1], [0.18, C.L2], [0.26, C.D2], [0.16, C.L1], [0.3, WHITE]],
    [[0.26, C.D1], [0.18, C.L2], [0.2, TEAL], [0.24, C.L1], [0.16, WHITE], [0.22, C.D2]],
    [[0.2, WHITE], [0.28, C.L1], [0.18, C.D1], [0.24, C.L2]],
  ];
  books.forEach((row, s) => {
    const z = 0.2 + s * 1.04; let y = 3.72;
    row.forEach(([w, col], k) => { const h = 0.62 + ((k * 7 + s * 3) % 5) * 0.06; iso.face([[0.7, y, z], [0.7, y + w, z], [0.7, y + w, z + h], [0.7, y, z + h]], col); y += w + 0.05; });
    hair([0.7, 3.62, z - 0.05], [0.7, 6.28, z - 0.05], C.D2, 4);
  });
  box(0.12, 5.3, 2.33, 0.6, 5.9, 2.75, white);                                   // a box file on the top shelf

  // 6. the desk and what is on it
  iso.face([[3.0, 2.0, 0], [6.4, 2.0, 0], [6.95, 2.5, 0], [3.55, 2.5, 0]], C.D2, 0.55);
  box(3.05, 0.55, 0, 3.2, 0.7, 1.38, dark); box(3.05, 1.8, 0, 3.2, 1.95, 1.38, dark);
  box(5.3, 0.6, 0.1, 6.15, 1.95, 1.38, mid);
  [0.5, 0.95].forEach((z) => { iso.face([[5.4, 1.95, z], [6.05, 1.95, z], [6.05, 1.95, z + 0.36], [5.4, 1.95, z + 0.36]], C.D1); hair([5.62, 1.95, z + 0.18], [5.84, 1.95, z + 0.18], WHITE, 3); });
  box(2.9, 0.45, 1.38, 6.3, 2.05, 1.5, white);
  iso.face([[5.2, 0.6, 1.5], [6.2, 0.6, 1.5], [6.2, 1.5, 1.5], [5.2, 1.5, 1.5]], C.L2);   // the lamp's pool, one flat shape
  box(4.55, 0.85, 1.5, 4.95, 1.15, 1.54, dark); box(4.7, 0.96, 1.54, 4.8, 1.04, 1.95, dark);   // monitor foot and neck
  box(4.05, 0.9, 1.9, 5.45, 1.0, 2.8, { top: C.D3, left: C.D4, right: C.D4 });
  iso.face([[4.12, 1.0, 1.97], [5.38, 1.0, 1.97], [5.38, 1.0, 2.73], [4.12, 1.0, 2.73]], WHITE);
  [[0, 0.5, C.D2], [0.12, 0.8, C.L1], [0.12, 0.45, TEAL], [0.24, 0.6, C.L1], [0.12, 0.7, C.D1], [0, 0.3, C.D2]].forEach(([ind, w, col], k) =>
    hair([4.22 + (ind as number), 1.0, 2.62 - k * 0.11], [4.22 + (ind as number) + (w as number), 1.0, 2.62 - k * 0.11], col as string, 3));
  box(4.2, 1.35, 1.5, 5.3, 1.72, 1.54, { top: C.L2, left: C.L1, right: C.D1 });       // keyboard
  for (let r = 0; r < 3; r++) hair([4.26, 1.43 + r * 0.1, 1.54], [5.24, 1.43 + r * 0.1, 1.54], WHITE, 2.5);
  iso.face([[3.2, 0.75, 1.5], [3.75, 0.7, 1.5], [3.8, 1.4, 1.5], [3.25, 1.45, 1.5]], C.L2);  // paper, and its lines
  [0.12, 0.24, 0.36, 0.48].forEach((d) => hair([3.3, 0.78 + d, 1.5], [3.68, 0.75 + d, 1.5], C.D1, 2));
  box(3.4, 1.62, 1.5, 3.62, 1.84, 1.78, white);                                       // mug, with its band
  iso.face([[3.4, 1.84, 1.6], [3.62, 1.84, 1.6], [3.62, 1.84, 1.68], [3.4, 1.84, 1.68]], TEAL);
  box(5.6, 0.85, 1.5, 5.95, 1.2, 1.55, dark); box(5.75, 1.0, 1.55, 5.8, 1.05, 2.2, dark);     // lamp
  const sh = (r: number, z: number): P3[] => [[5.775 - r, 1.025 - r, z], [5.775 + r, 1.025 - r, z], [5.775 + r, 1.025 + r, z], [5.775 - r, 1.025 + r, z]];
  const lo = sh(0.42, 2.15), hi = sh(0.22, 2.62);
  iso.face([lo[3], lo[2], hi[2], hi[3]], C.L2); iso.face([lo[1], lo[2], hi[2], hi[1]], C.L1); iso.face(hi, WHITE);

  // 7. a snake plant in the far corner: blades authored in screen space over the pot
  iso.face([[9.4, 0.5, 0], [9.9, 1.0, 0], [9.9, 1.9, 0], [9.4, 1.4, 0]], C.D2, 0.55);
  box(8.6, 0.6, 0, 9.4, 1.4, 0.85, white);
  { const [px, py] = iso.p(9.0, 1.0, 0.85);
    const blade = (dx: number, lean: number, h: number, w: number, a: string, b: string) => {
      const tip: P2 = [px + dx + lean, py - h], l: P2 = [px + dx - w, py - h * 0.45], r: P2 = [px + dx + w, py - h * 0.5];
      shape([[px + dx - w * 0.6, py], l, tip, [px + dx + lean * 0.5, py - h * 0.5], [px + dx, py]], a);
      shape([[px + dx, py], [px + dx + lean * 0.5, py - h * 0.5], tip, r, [px + dx + w * 0.6, py]], b);
    };
    blade(-20, -26, 150, 13, C.D1, C.D3); blade(16, 24, 170, 14, C.L1, C.D2); blade(-4, -6, 215, 15, C.D1, C.D3); blade(4, 12, 120, 12, C.L1, C.D1); blade(-12, -18, 95, 11, C.L2, C.D1);
  }

  // 8. the chair, seen from behind
  iso.face([[4.3, 3.45, 0], [5.3, 3.45, 0], [5.75, 3.85, 0], [4.75, 3.85, 0]], C.D2, 0.55);
  box(4.2, 2.92, 0.05, 5.3, 3.02, 0.12, dark); box(4.7, 2.45, 0.05, 4.8, 3.5, 0.12, dark);
  box(4.7, 2.92, 0.12, 4.8, 3.02, 0.82, dark);
  box(4.3, 2.55, 0.82, 5.2, 3.4, 0.98, mid);
  box(4.3, 3.3, 0.98, 5.2, 3.42, 2.05, mid);
  hair([4.4, 3.42, 1.25], [5.1, 3.42, 1.25], C.D1, 2); hair([4.4, 3.42, 1.6], [5.1, 3.42, 1.6], C.D1, 2);

  // 9. the dog, sitting on the rug, head turned up to the man
  { const [fx, fy] = iso.p(6.5, 6.0, 0), k = 1.25, q = (pts: number[][]): P2[] => pts.map(([x, y]) => [fx + x * k, fy + y * k]);
    iso.face([[6.15, 5.85, 0], [6.9, 5.85, 0], [7.15, 6.25, 0], [6.4, 6.25, 0]], C.D4, 0.45);
    shape(q([[-24, -18], [-38, -28], [-41, -45], [-31, -53], [-25, -43], [-30, -34], [-22, -28]]), C.D1);                 // tail
    shape(q([[-22, 0], [-28, -22], [-20, -46], [-4, -55], [10, -46], [15, -22], [17, 0]]), C.D1);                          // body
    shape(q([[-22, 0], [-28, -22], [-20, -46], [-12, -51], [-16, -24], [-10, 0]]), C.D2);                                  // its shade side
    shape(q([[2, -50], [11, -44], [15, -20], [17, 0], [5, 0], [1, -22]]), WHITE);                                          // chest and foreleg
    shape(q([[-22, 0], [-9, 0], [-7, -6], [-20, -8]]), C.D2); shape(q([[4, 0], [19, 0], [20, -5], [6, -6]]), C.L2);       // paws
    shape(q([[-2, -53], [-7, -70], [1, -83], [17, -86], [30, -77], [38, -68], [29, -59], [14, -53]]), C.D1);               // head
    shape(q([[20, -73], [38, -68], [29, -59], [16, -61]]), WHITE);                                                         // muzzle
    shape(q([[-2, -80], [0, -98], [9, -85]]), C.D2); shape(q([[11, -86], [18, -101], [25, -82]]), C.D1);                  // ears
    shape(q([[14, -84], [18, -95], [22, -83]]), C.L2);
    ctx.fillStyle = HAIR; ctx.beginPath(); ctx.arc(fx + 36.5 * k, fy - 68.5 * k, 2.6, 0, Math.PI * 2); ctx.fill();       // nose
    ctx.beginPath(); ctx.arc(fx + 16 * k, fy - 75 * k, 2.2, 0, Math.PI * 2); ctx.fill();                                 // eye
    stroke(q([[27, -62], [31, -61], [34, -63]]), HAIR, 1.6);                                                               // mouth
  }

  // 10. the man, on the rug: the one accent in the picture is his shirt
  { const [fx, fy] = iso.p(8.6, 5.0, 0), k = 1.0, q = (pts: number[][]): P2[] => pts.map(([x, y]) => [fx + x * k, fy + y * k]);
    iso.face([[8.1, 4.75, 0], [9.1, 4.75, 0], [9.55, 5.35, 0], [8.55, 5.35, 0]], C.D4, 0.45);                          // his shadow, thrown lower right
    shape(q([[-34, -5], [-9, -8], [-6, 2], [-22, 7], [-38, 3]]), HAIR); shape(q([[5, -8], [29, -5], [36, 3], [22, 8], [4, 2]]), HAIR);   // shoes
    shape(q([[-31, -106], [-2, -106], [-7, -7], [-30, -5]]), TROUSER); shape(q([[-2, -106], [28, -106], [29, -5], [6, -7]]), TROUSER_D);  // legs
    shape(q([[-55, -141], [-42, -137], [-41, -100], [-53, -98]]), SKIN); shape(q([[-54, -99], [-41, -101], [-38, -86], [-44, -77], [-52, -79]]), SKIN);
    shape(q([[-41, -98], [-35, -92], [-38, -84]]), SKIN_D);                                                               // left thumb
    shape(q([[42, -137], [55, -141], [53, -98], [41, -100]]), SKIN_D); shape(q([[41, -101], [54, -99], [52, -79], [44, -77], [38, -86]]), SKIN_D);
    shape(q([[-36, -178], [-51, -169], [-56, -140], [-41, -136], [-35, -151]]), TEAL_L);                                  // sleeves
    shape(q([[36, -178], [51, -169], [56, -140], [41, -136], [35, -151]]), TEAL_D);
    shape(q([[-37, -178], [-14, -186], [14, -186], [37, -178], [33, -102], [-33, -102]]), TEAL);                          // shirt
    shape(q([[16, -186], [37, -178], [33, -102], [19, -102]]), TEAL_D);                                                   // its shade side
    shape(q([[-10, -186], [10, -186], [0, -174]]), SKIN_D);                                                               // neck in the collar
    shape(q([[-9, -194], [9, -194], [10, -184], [-10, -184]]), SKIN_D);
    shape(q([[-31, -229], [-27, -233], [-27, -214], [-31, -217]]), SKIN_D); shape(q([[27, -233], [31, -229], [31, -217], [27, -214]]), SKIN_D);   // ears
    shape(q([[-27, -254], [27, -254], [28, -222], [24, -204], [14, -192], [0, -188], [-14, -192], [-24, -204], [-28, -222]]), SKIN);            // head
    shape(q([[10, -246], [27, -246], [28, -222], [24, -204], [14, -192], [10, -200], [14, -220]]), SKIN_D);                // the face's shade side
    shape(q([[-28, -217], [-20, -212], [-9, -214], [0, -211], [9, -214], [20, -212], [28, -217], [24, -203], [14, -191], [0, -187], [-14, -191], [-24, -203]]), BEARD);
    stroke(q([[-6, -203], [0, -201], [6, -203]]), SKIN_D, 2.4);                                                           // mouth, in the beard
    shape(q([[-2, -224], [4, -213], [-3, -213]]), SKIN_D);                                                                // nose
    shape(q([[-29, -222], [-28, -240], [-21, -245], [-22, -227]]), GREY); shape(q([[29, -222], [28, -240], [21, -245], [22, -227]]), GREY);
    shape(q([[-28, -238], [-25, -252], [-15, -264], [1, -272], [16, -264], [25, -252], [28, -238], [18, -246], [4, -250], [-10, -248], [-20, -244]]), HAIR);
    stroke(q([[-12, -262], [0, -267], [10, -262]]), GREY, 1.6);                                                           // one light on the quiff
    [[-22, -5], [5, 22]].forEach(([a, b]) => { ctx.fillStyle = "rgba(255,255,255,0.35)"; ctx.fillRect(fx + a * k, fy - 233 * k, (b - a) * k, 13 * k); stroke(q([[a, -233], [b, -233], [b, -220], [a, -220]]), HAIR, 2.6, true); });
    stroke(q([[-5, -228], [5, -228]]), HAIR, 2.6);
    ctx.fillStyle = HAIR; [[-13, -226], [13, -226]].forEach(([x, y]) => { ctx.beginPath(); ctx.arc(fx + x * k, fy + y * k, 2.4, 0, Math.PI * 2); ctx.fill(); });
  }
};

export const officeIso: Film = {
  meta: { title: "officeIso", W: 1920, H: 1080, fps: 30, bpm: 60, durationFrames: 3 },
  assets: { images: {} },
  shots: [{ id: "officeIso", start: 0, end: 3, draw: drawOfficeIso }],
};
