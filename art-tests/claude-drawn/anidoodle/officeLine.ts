// OFFICE · line and flat colour. A small home office seen like a room in a 2D RPG: back wall
// across the top third, floor below, every piece of furniture showing its top and its front.
//
// MEDIUM RECIPE (written before any drawing code; the hand, not a picture)
// MARK    One technical pen, ONE weight everywhere (LW), round-ended, no swelling, no taper: the
//         contour of a figure, a book spine, a finger join and a hatch stroke are the same line.
//         Colour is a flat cel laid inside the line: no gradient, no highlight, no rim light.
//         The only texture is a handful of short parallel hatch strokes.
// EDGE    Hard. Every form is closed by its contour; a shadow is one flat shape with a hard edge,
//         at most one per form, all in a single tone. Nothing blends across a line.
// ORDER   Back to front. Per form: the flat, then its one shadow shape, then the contour last.
//         Floor shadows go down as ONE layer before the furniture stands on them.
// PAPER   Solid warm cream, no tooth, no vignette. The wall is the paper left bare.
// PALETTE Ten flats, slightly muted: cream, dark warm ink, sand, ochre, terracotta rose, sage,
//         teal, warm grey, skin, and one loud red-orange (#F54E00) kept to a few small spots.
//         One shadow tone, multiplied over whatever flat it falls on.
// NOT     Nearest plate is the marker comic (koi.ts): flat cel fills with a hard shadow edge under
//         a contour. It differs in the mark: koi's brush-pen ribbon thickens away from the light
//         and tapers; this pen never changes weight, there are no gel-pen whites and no marker
//         streaks. Kit reused: Gfx surface and groups (core.ts), smooth / fillShape / clipped /
//         trace / bounds (gallery.ts). The hand's wander is displaced GEOMETRY (core displace).
//
// REALISM, stated. View: oblique three-quarter top-down, no convergence: heights at full scale,
// floor depth at about 0.6. Light: daylight from the window, upper left; shadows fall down-right.
// The man: about four heads tall, weight on both feet, right foot a little forward, head tipped
// toward the dog, one hand hanging open (four fingers and a thumb), one wrapped round a mug.
// The dog: a sitting shiba in three-quarter profile: short blunt muzzle, small thick triangular
// ears, cream cheeks, chest and socks (urajiro), a tail curled tight over the back, a collar.
import { Gfx, PENCIL, displace, rng, type Ctx, type Env, type P } from "./core";
import type { Film } from "./film";
import { bounds, clipped, fillShape, lerpP, smooth, trace } from "./gallery";

const INK = "#2a201e", CREAM = "#f5ebd7", SAND = "#e9d5ab", OCHRE = "#d9a548", ROSE = "#c97c64", SAGE = "#a5b593", TEAL = "#2c7f83", HOT = "#f54e00", SKIN = "#e9b78f", GREY = "#978f88";
const SHADE = "#cdb9ad"; // the one shadow tone, multiplied
const LW = 3.2; // the one line weight

type K = [number, number] | [number, number, 1]; // a control point; a third element makes it a corner
type XY = [number, number];

export const drawOfficeLine = (ctx: Ctx, _frame: number, env: Env) => {
  const g = new Gfx(ctx, env, 0, PENCIL);
  ctx.setTransform(env.scale, 0, 0, env.scale, 0, 0);
  ctx.fillStyle = CREAM; ctx.fillRect(0, 0, env.W, env.H);

  // ------------------------------------------------------------ the pen and the flats
  let TF = (x: number, y: number): P => [x, y];
  // place a part: local (x, y) about pivot (px, py), turned, scaled, moved to (ox, oy)
  const at = (ox: number, oy: number, s: number, rot: number, fn: () => void, px = 0, py = 0) => {
    const prev = TF, c = Math.cos(rot), sn = Math.sin(rot);
    TF = (x, y) => prev(ox + s * ((x - px) * c - (y - py) * sn), oy + s * ((x - px) * sn + (y - py) * c));
    fn(); TF = prev;
  };
  // a curve through hand-placed points; the curve is cut and restarted at a corner
  const crv = (pts: K[], closed = true): P[] => {
    const q = pts.map((p) => ({ p: TF(p[0], p[1]), c: !!p[2] })), ci = q.findIndex((k) => k.c);
    if (ci < 0) return smooth(q.map((k) => k.p), closed, 8);
    const seq = closed ? [...q.slice(ci), ...q.slice(0, ci), q[ci]] : q, out: P[] = []; let run: P[] = [];
    seq.forEach((k, i) => { run.push(k.p); if ((k.c && run.length > 1) || i === seq.length - 1) { if (run.length > 1) { const s = run.length === 2 ? run : smooth(run, false, 8); out.push(...(out.length ? s.slice(1) : s)); } run = [k.p]; } });
    return out;
  };
  const box = (...c: XY[]): P[] => crv(c.map(([x, y]) => [x, y, 1] as K));
  const ln = (...c: XY[]): P[] => crv(c.map(([x, y]) => [x, y, 1] as K), false);
  const arc = (...c: XY[]): P[] => crv(c as K[], false);
  const rbox = (c: XY[], r: number): P[] => crv(c.flatMap((p, i) => {
    const a = c[(i + c.length - 1) % c.length], b = c[(i + 1) % c.length];
    const u = (q: XY): XY => { const d = Math.hypot(q[0] - p[0], q[1] - p[1]); return [p[0] + ((q[0] - p[0]) / d) * r, p[1] + ((q[1] - p[1]) / d) * r]; };
    const A = u(a), B = u(b);
    return Array.from({ length: 7 }, (_, k) => { const t = k / 6, m = 1 - t; return [m * m * A[0] + 2 * m * t * p[0] + t * t * B[0], m * m * A[1] + 2 * m * t * p[1] + t * t * B[1], 1] as K; });
  }));
  const dense = (s: P[], step = 9): P[] => { const o: P[] = []; for (let i = 0; i < s.length - 1; i++) { const a = s[i], b = s[i + 1], n = Math.max(1, Math.ceil(Math.hypot(b[0] - a[0], b[1] - a[1]) / step)); for (let k = 0; k < n; k++) o.push(lerpP(a, b, k / n)); } o.push(s[s.length - 1]); return o; };
  // the hand: one slow wander over the whole sheet, so shared edges stay registered
  const hand = (s: P[]) => displace(dense(s), 5.5, 0.0065, 2, 41);
  const pen = (s: P[], col = INK, closed = false) => { const q = hand(s), b = bounds(q), c = g.cur; g.touch(b.x0 - 4, b.y0 - 4, b.x1 + 4, b.y1 + 4); c.strokeStyle = col; c.lineWidth = LW; c.lineJoin = "round"; c.lineCap = "round"; trace(c, q, closed); c.stroke(); };
  const flat = (s: P[], col: string) => fillShape(g, hand(s), col);
  const shade = (clip: P[] | null, s: P[]) => g.group("plain", () => { const f = () => fillShape(g, hand(s), SHADE); if (clip) clipped(g, hand(clip), f); else f(); }, { blend: "multiply" });
  const form = (s: P[], col: string, sh?: P[] | true) => { flat(s, col); if (sh) shade(s, sh === true ? s : sh); pen(s, INK, true); };
  const inside = (clip: P[], fn: () => void) => clipped(g, hand(clip), fn);
  const dot = (x: number, y: number, r: number, col = INK, seed = 1) => { const q = rng(seed * 7 + 3); flat(crv(Array.from({ length: 7 }, (_, i) => { const a = (i / 7) * 6.283 + 0.4, k = r * (0.88 + q() * 0.24); return [x + Math.cos(a) * k, y + Math.sin(a) * k] as K; })), col); };
  const hatch = (x: number, y: number, n: number, len: number, seed: number, col = INK) => { const q = rng(seed); for (let i = 0; i < n; i++) { const l = len * (0.75 + q() * 0.5), x0 = x + i * 9 + (q() - 0.5) * 2, y0 = y + (q() - 0.5) * 4; pen(ln([x0, y0], [x0 + l * 0.57, y0 - l * 0.82]), col); } };

  // ------------------------------------------------------------ the room
  const WALL = box([100, 62], [1822, 58], [1826, 351], [98, 349]);
  const FLOOR = box([98, 349], [1826, 351], [1830, 1022], [94, 1018]);
  flat(FLOOR, SAND);
  // floorboards: a few broken lines in ochre, with bare rests
  ([[566, [[170, 410], [1050, 1180]]], [690, [[112, 330], [540, 770]]], [822, [[310, 560], [1700, 1806]]], [944, [[610, 900]]]] as [number, XY[]][])
    .forEach(([y, runs]) => runs.forEach(([a, b]) => pen(ln([a, y], [b, y + 1]), OCHRE)));
  // daylight through the four panes, lying on the floor: the light is paper left lighter
  const sun = (x: number, y: number): XY => [x + 52 + (280 - y) * 0.6, 392 + (280 - y) * 0.93];
  ([[314, 111, 436, 184], [449, 110, 572, 183], [314, 196, 436, 271], [449, 195, 572, 270]] as number[][]).forEach(([x0, y0, x1, y1]) => flat(box(sun(x0, y0), sun(x1, y0), sun(x1, y1), sun(x0, y1)), CREAM));
  pen(FLOOR, INK, true); pen(WALL, INK, true);
  pen(ln([98, 334], [1826, 336])); // skirting

  // the rug
  const RUG = rbox([[962, 728], [1648, 722], [1664, 958], [950, 966]], 30);
  { const q = rng(9); for (let i = 0; i < 15; i++) { const t = (i + 0.5) / 15, yl = 750 + t * 196, yr = 744 + t * 194; pen(ln([958 - t * 10, yl], [958 - t * 10 - 13 - q() * 6, yl + (q() - 0.5) * 5])); pen(ln([1650 + t * 14, yr], [1650 + t * 14 + 13 + q() * 6, yr + (q() - 0.5) * 5])); } }
  form(RUG, ROSE);
  pen(rbox([[990, 748], [1622, 743], [1636, 938], [980, 945]], 18), CREAM, true);
  ([[1552, 792, 15], [1596, 858, 12], [1530, 900, 10]] as number[][]).forEach(([x, y, r]) => { form(box([x, y - r], [x + r * 1.5, y], [x, y + r], [x - r * 1.5, y]), CREAM); dot(x, y, 2.6, INK, x); });

  // ------------------------------------------------------------ every floor and wall shadow, one layer
  const MAN: [number, number, number] = [1300, 905, 1.05], DOG: [number, number, number] = [1112, 908, 0.92];
  g.group("plain", () => {
    const s = (p: P[]) => fillShape(g, hand(p), SHADE);
    s(box([292, 304], [601, 301], [608, 314], [304, 317])); // sill
    s(box([1256, 113], [1402, 110], [1405, 267], [1254, 270])); // print
    s(crv([[170, 470], [220, 478], [262, 462], [330, 480], [352, 500], [320, 512], [250, 500], [190, 490]])); // plant
    s(box([690, 447], [1180, 444], [1180, 300], [1208, 324], [1208, 468], [716, 472])); // desk
    s(box([713, 305], [1014, 304], [1015, 421], [1150, 419], [1150, 446], [713, 448])); // under the desk
    s(box([1482, 392], [1752, 390], [1752, 112], [1778, 134], [1780, 412], [1506, 414])); // shelf
    s(crv([[856, 566], [900, 596], [960, 592], [1030, 600], [1050, 622], [1000, 636], [920, 628], [864, 600]])); // chair
    at(DOG[0], DOG[1], DOG[2], 0, () => s(crv([[-60, 0], [0, 8], [50, 6], [110, 30], [140, 48], [120, 60], [60, 50], [-10, 30], [-56, 14]])));
    at(MAN[0], MAN[1], MAN[2], 0, () => s(crv([[-44, 0], [-20, 10], [30, 14], [90, 34], [150, 58], [170, 76], [150, 88], [90, 78], [20, 48], [-30, 24]])));
  }, { blend: "multiply" });

  // ------------------------------------------------------------ the window
  form(box([297, 97], [584, 94], [587, 283], [295, 286]), OCHRE);
  const PANES = [box([314, 111], [436, 110], [436, 184], [314, 185]), box([449, 110], [571, 109], [572, 183], [449, 184]), box([314, 196], [436, 195], [437, 271], [315, 272]), box([449, 195], [572, 194], [573, 270], [449, 271])];
  const cloud = crv([[352, 150], [372, 134], [398, 138], [410, 126], [440, 124], [462, 138], [492, 140], [506, 154], [480, 162], [430, 160], [380, 162]]);
  const hills = crv([[300, 276, 1], [300, 238], [340, 224], [376, 240], [410, 216], [450, 208], [482, 230], [520, 218], [556, 234], [590, 228], [590, 276, 1]]);
  PANES.forEach((p) => { flat(p, SAGE); inside(p, () => { form(cloud, CREAM); form(hills, GREY); }); pen(p, INK, true); });
  form(box([285, 286], [597, 283], [601, 301], [282, 304]), OCHRE);

  // ------------------------------------------------------------ the framed print
  form(box([1248, 104], [1392, 101], [1395, 256], [1246, 259]), OCHRE);
  form(box([1260, 116], [1380, 114], [1383, 244], [1258, 246]), CREAM);
  { const art = box([1272, 128], [1369, 126], [1371, 232], [1270, 234]); flat(art, SAGE); inside(art, () => { form(crv([[1276, 236], [1280, 204], [1300, 180], [1326, 172], [1350, 182], [1366, 206], [1368, 236]]), ROSE); pen(arc([1262, 214], [1296, 200], [1340, 204], [1380, 196])); pen(arc([1288, 222], [1320, 214], [1356, 218])); }); dot(1346, 150, 6.5, HOT, 3); pen(art, INK, true); }

  // ------------------------------------------------------------ the plant: an invented thing
  // a jointed bottle-trunk on a three-legged pot, fan fronds, hanging drops, one loud bud
  form(crv([[166, 448, 1], [160, 475, 1], [176, 477, 1], [181, 454, 1]]), ROSE); form(crv([[232, 452, 1], [236, 477, 1], [250, 475, 1], [248, 446, 1]]), ROSE);
  form(crv([[150, 372, 1], [146, 400], [154, 436], [176, 456], [206, 461], [236, 455], [256, 432], [262, 398], [258, 370, 1], [238, 381], [204, 386], [172, 382]]), ROSE, crv([[262, 366], [264, 398], [258, 434], [236, 458], [204, 464], [226, 440], [240, 412], [243, 382]]));
  form(crv([[150, 372], [170, 361], [204, 357], [238, 360], [258, 370], [238, 381], [204, 385], [170, 381]]), GREY);
  pen(arc([150, 408], [170, 424], [190, 414], [210, 428], [232, 416], [258, 410]));
  const TR: [number, number, number][] = [[204, 374, 30], [209, 318, 25], [215, 268, 22], [217, 224, 19], [213, 186, 16], [207, 154, 12]];
  for (let i = TR.length - 2; i >= 0; i--) { const [x0, y0, w0] = TR[i], [x1, y1, w1] = TR[i + 1], ym = y0 * 0.68 + y1 * 0.32, seg = (dx: number) => crv([[x0 - w0 / 2 + 3 + dx, y0, 1], [x0 - w0 / 2 - 4 + dx, ym], [x1 - w1 / 2 + dx, y1, 1], [x1 + w1 / 2 + dx, y1, 1], [x0 + w0 / 2 + 4 + dx, ym], [x0 + w0 / 2 - 3 + dx, y0, 1]]); form(seg(0), SAGE, seg(w0 * 0.5)); }
  const FAN: K[] = [[0, 0, 1], [0.2, -0.12], [0.42, -0.4], [0.6, -0.5], [0.7, -0.36], [0.8, -0.44], [0.97, -0.26], [0.92, -0.08], [1.05, 0.04], [0.98, 0.26], [0.82, 0.28], [0.74, 0.46], [0.5, 0.42], [0.22, 0.16]];
  const SPLIT: K[] = [[0, 0, 1], [0.24, -0.2], [0.58, -0.27], [0.88, -0.15], [1.06, 0.02, 1], [0.86, 0.07], [0.93, 0.21], [0.6, 0.27], [0.26, 0.17]];
  const frond = (kind: "fan" | "split", root: XY, bx: number, by: number, len: number, rot: number, flip: number) => {
    pen(arc(root, [(root[0] + bx) / 2, (root[1] + by) / 2 - 8], [bx, by]));
    at(bx, by, len, rot, () => {
      const f = (p: K[]) => p.map(([x, y, c]) => (c ? [x, y * flip, 1] : [x, y * flip]) as K);
      if (kind === "fan") { const s = crv(f(FAN)); form(s, SAGE, crv(f([[0, 0.02], [0.5, 0.06], [1.06, 0.1], [1.0, 0.5], [0.3, 0.5]]))); [[0.6, -0.38], [0.88, -0.2], [0.96, 0.12], [0.7, 0.36]].forEach(([x, y]) => pen(arc([0.1, 0], [x * 0.55, y * flip * 0.4], [x, y * flip]))); }
      else { const s = crv(f(SPLIT)); form(s, SAGE, crv(f([[0, 0.03], [0.5, 0.05], [1.0, 0.06], [0.9, 0.3], [0.3, 0.3]]))); pen(arc([0.08, 0], [0.5, -0.02 * flip], [0.9, 0.0])); pen(arc([0.36, -0.01], [0.48, -0.12 * flip], [0.62, -0.18 * flip])); pen(arc([0.5, 0], [0.6, 0.1 * flip], [0.7, 0.17 * flip])); }
    });
  };
  frond("fan", [206, 270], 170, 262, 74, -2.25, 1);
  frond("split", [208, 226], 170, 200, 68, -2.5, -1);
  frond("fan", [222, 224], 262, 222, 88, -0.62, -1);
  frond("split", [218, 186], 250, 168, 72, -0.9, 1);
  pen(arc([222, 270], [238, 272], [242, 286])); form(crv([[242, 284], [233, 298], [239, 313], [250, 305], [248, 290]]), ROSE);
  pen(arc([194, 318], [180, 322], [176, 334])); form(crv([[176, 332], [168, 346], [174, 358], [184, 351], [182, 337]]), ROSE);
  pen(arc([226, 318], [250, 310], [262, 324], [254, 336], [244, 330], [247, 322]));
  form(crv([[198, 158], [188, 140], [195, 121], [206, 112], [217, 122], [221, 141], [213, 158]]), HOT);
  pen(arc([203, 150], [201, 136], [206, 124]));
  ([[198, 116, 186, 96], [206, 112, 208, 88], [214, 118, 228, 100]] as number[][]).forEach(([a, b, c, d], i) => { pen(arc([a, b], [(a + c) / 2 + 2, (b + d) / 2], [c, d])); dot(c, d, 3.6, INK, 20 + i); });

  // ------------------------------------------------------------ the bookshelf
  form(box([1478, 86], [1747, 84], [1750, 126], [1476, 128]), OCHRE);
  form(box([1476, 128], [1750, 126], [1752, 390], [1474, 392]), OCHRE);
  form(crv([[1560, 100, 1], [1562, 116], [1570, 121], [1588, 121], [1596, 115], [1598, 99, 1]]), CREAM, crv([[1584, 96], [1600, 96], [1600, 124], [1580, 124]]));
  form(crv([[1570, 101, 1], [1566, 92], [1572, 84, 1], [1586, 83, 1], [1591, 91], [1587, 101, 1]]), SAGE); form(crv([[1573, 84, 1], [1571, 76], [1577, 70, 1], [1584, 70, 1], [1588, 77], [1585, 84, 1]]), SAGE);
  pen(arc([1588, 90], [1600, 84], [1606, 90])); dot(1608, 93, 4.4, ROSE, 91);
  const book = (x: number, yb: number, w: number, h: number, col: string, lean = 0, band = 0) => { form(box([x + lean, yb - h], [x + w + lean, yb - h + (lean ? 3 : 0)], [x + w, yb], [x, yb]), col); if (band) pen(ln([x + lean * (1 - band / h) + 2, yb - h + band], [x + w + lean * (1 - band / h) - 2, yb - h + band + (lean ? 2 : 0)])); };
  ([[142, 212], [226, 298], [312, 378]] as XY[]).forEach(([y0, y1]) => form(box([1490, y0], [1736, y0 - 1], [1737, y1], [1490, y1 + 1]), OCHRE, true));
  book(1497, 212, 16, 57, TEAL, 0, 12); book(1513, 212, 12, 62, CREAM); book(1525, 212, 19, 51, ROSE, 0, 10); book(1544, 212, 11, 60, SAGE); book(1555, 212, 15, 55, GREY, 0, 14); book(1584, 212, 14, 58, CREAM, 13);
  form(box([1648, 199], [1728, 198], [1729, 212], [1648, 213]), TEAL); form(box([1656, 186], [1722, 185], [1722, 198], [1656, 199]), ROSE); form(box([1650, 175], [1716, 173], [1717, 185], [1651, 186]), CREAM);
  book(1502, 298, 14, 50, SAGE, 0, 9); book(1562, 298, 18, 62, ROSE, 0, 13); book(1580, 298, 12, 57, TEAL); book(1592, 298, 16, 64, CREAM, 0, 11); book(1608, 298, 12, 54, HOT); book(1620, 298, 17, 60, GREY); book(1650, 298, 13, 60, SAGE, -11);
  book(1497, 378, 20, 54, GREY, 0, 12); book(1517, 378, 14, 58, TEAL); book(1531, 378, 12, 50, ROSE, 0, 8);
  form(box([1596, 334], [1688, 333], [1689, 378], [1596, 379]), CREAM); pen(ln([1626, 352], [1658, 352])); pen(ln([1596, 344], [1688, 343]));
  book(1702, 378, 14, 56, SAGE, 0, 10); book(1716, 378, 12, 51, CREAM);

  // ------------------------------------------------------------ the desk and what is on it
  const band = box([672, 303], [1190, 300], [1190, 318], [672, 321]);
  form(box([684, 304], [713, 304], [714, 447], [683, 449]), OCHRE, band);
  form(box([1150, 302], [1178, 302], [1180, 444], [1149, 446]), OCHRE, band);
  form(box([1014, 303], [1150, 302], [1150, 419], [1015, 421]), OCHRE, band);
  pen(ln([1015, 362], [1150, 361])); pen(ln([1070, 337], [1096, 337])); pen(ln([1070, 392], [1096, 392]));
  form(box([676, 192], [1184, 189], [1189, 287], [671, 290]), OCHRE);
  form(box([671, 290], [1189, 287], [1189, 303], [672, 306]), OCHRE, true);
  hatch(700, 284, 3, 15, 61);
  // lamp
  form(crv([[696, 246], [708, 236], [726, 234], [744, 238], [751, 248], [740, 257], [720, 259], [702, 255]]), ROSE);
  pen(ln([724, 244], [704, 160], [738, 118])); dot(704, 160, 5, INK, 31); dot(724, 244, 4.5, INK, 32);
  form(crv([[728, 114, 1], [742, 100, 1], [770, 108], [786, 130, 1], [762, 162, 1], [742, 142]]), ROSE, crv([[742, 142], [760, 126], [786, 130], [762, 164]]));
  form(crv([[786, 130], [782, 150], [762, 162], [765, 142]]), CREAM);
  // monitor: a dark editor, lines of code
  form(crv([[868, 236], [880, 226], [915, 223], [952, 226], [962, 236], [950, 246], [915, 249], [880, 246]]), GREY);
  form(box([905, 196], [925, 196], [927, 234], [903, 234]), GREY);
  form(rbox([[806, 86], [1022, 83], [1025, 201], [804, 204]], 10), GREY);
  form(rbox([[816, 95], [1013, 93], [1015, 189], [815, 191]], 5), INK);
  ([[104, [[826, 858, HOT], [866, 908, CREAM]]], [115, [[840, 870, SAGE], [878, 930, CREAM], [938, 952, OCHRE]]], [126, [[854, 900, CREAM], [908, 958, SAGE]]], [137, [[854, 876, OCHRE], [884, 944, CREAM], [952, 988, ROSE]]], [148, [[840, 854, CREAM]]], [159, [[826, 846, SAGE], [854, 918, CREAM]]], [170, [[840, 894, CREAM], [902, 930, OCHRE]]], [181, [[826, 838, CREAM]]]] as [number, [number, number, string][]][])
    .forEach(([y, runs]) => runs.forEach(([a, b, col]) => pen(ln([a, y], [b, y]), col)));
  form(box([996, 190], [1018, 187], [1021, 210], [999, 212]), ROSE); pen(ln([1003, 198], [1014, 197]));
  // keyboard, mouse
  form(rbox([[836, 257], [1001, 255], [1003, 280], [834, 282]], 5), GREY);
  for (let r = 0; r < 2; r++) for (let x = 846; x < 990; x += 13) pen(ln([x, 264.5 + r * 8.5], [x + 6, 264.5 + r * 8.5]), CREAM);
  form(crv([[1018, 262], [1028, 256], [1040, 260], [1044, 272], [1036, 281], [1024, 280], [1017, 272]]), CREAM); pen(ln([1030, 258], [1031, 266]));
  // a sheet of paper, a mug
  form(box([1066, 242], [1136, 234], [1149, 275], [1076, 283]), CREAM);
  pen(ln([1080, 252], [1124, 247])); pen(ln([1083, 261], [1132, 255])); pen(ln([1086, 270], [1116, 267]));
  { const body = crv([[1122, 204, 1], [1124, 230], [1132, 238], [1150, 238], [1158, 230], [1160, 203, 1]]); pen(arc([1160, 210], [1171, 212], [1172, 224], [1160, 229])); flat(body, CREAM); inside(body, () => flat(box([1116, 218], [1166, 217], [1166, 226], [1116, 227]), ROSE)); pen(body, INK, true); form(crv([[1122, 204], [1130, 198], [1141, 196], [1152, 198], [1160, 203], [1152, 209], [1141, 211], [1130, 209]]), INK); }

  // ------------------------------------------------------------ the chair, from behind, left a little turned
  ([[856, 560], [884, 584], [942, 586], [972, 558]] as XY[]).forEach(([x, y], i) => { pen(ln([912, 546], [x, y])); dot(x, y + 3, 7, INK, 40 + i); });
  form(box([905, 488], [919, 488], [920, 548], [904, 548]), GREY);
  form(crv([[846, 468], [862, 452], [912, 447], [962, 451], [980, 466], [972, 486], [912, 493], [852, 488]]), SAGE, true);
  form(box([822, 424], [846, 422], [848, 434], [822, 436]), GREY); pen(arc([834, 436], [830, 456], [846, 472]));
  form(box([980, 422], [1004, 424], [1004, 436], [980, 434]), GREY); pen(arc([992, 436], [994, 456], [978, 470]));
  form(box([903, 440], [921, 440], [922, 474], [902, 474]), GREY);
  form(crv([[974, 350], [986, 358], [990, 402], [983, 440], [970, 446], [980, 400]]), GREY);
  { const back = crv([[852, 352], [868, 334], [912, 328], [958, 333], [976, 350], [980, 400], [972, 440], [950, 452], [912, 455], [874, 452], [852, 440], [846, 398]]); form(back, SAGE, crv([[930, 320], [990, 330], [990, 460], [880, 462], [930, 440], [952, 400], [950, 350]])); pen(arc([860, 420], [912, 428], [966, 420])); }

  // ------------------------------------------------------------ the dog: a sitting shiba, looking up
  at(DOG[0], DOG[1], DOG[2], 0, () => {
    { const far = crv([[44, -62, 1], [53, -36], [54, -12], [59, -4, 1], [53, 2, 1], [40, 2, 1]]); flat(far, OCHRE); inside(far, () => flat(box([36, -18], [62, -20], [62, 6], [36, 6]), CREAM)); pen(far, INK, true); } // far foreleg
    const body = crv([[42, -116], [50, -92], [46, -62], [40, -36], [41, -12], [49, -4, 1], [42, 2, 1], [22, 2, 1], [19, -8], [14, -3], [10, 1, 1], [-20, 3], [-46, 2], [-62, -10], [-68, -34], [-64, -62], [-52, -90], [-36, -112], [-18, -128], [14, -134]]);
    flat(body, OCHRE);
    inside(body, () => { flat(crv([[40, -124], [56, -92], [50, -62], [46, -34], [34, -40], [28, -70], [24, -108]]), CREAM); flat(crv([[36, -20], [44, -12], [52, -4], [44, 5], [18, 5], [17, -10], [24, -18]]), CREAM); flat(crv([[14, 4], [-16, 6], [-14, -7], [8, -9]]), CREAM); });
    shade(body, crv([[-72, -36], [-44, -26], [-18, -22], [-6, -34], [-2, -10], [12, 6], [-72, 8]]));
    pen(body, INK, true);
    pen(arc([-46, -72], [-22, -64], [-6, -44], [-4, -22], [-10, -8])); pen(arc([-10, -8], [2, -10], [10, -3]));
    pen(arc([22, -54], [20, -34], [20, -12])); pen(arc([30, -98], [24, -84], [26, -72]));
    pen(ln([33, 2], [32, -5])); pen(ln([41, 1], [41, -5])); pen(ln([-2, 2], [-1, -4]));
    // tail, curled tight over the back
    { const t = crv([[-50, -58], [-70, -58], [-86, -72], [-88, -94], [-76, -110], [-56, -114], [-40, -103], [-36, -86], [-44, -73]]); flat(t, OCHRE); inside(t, () => flat(crv([[-66, -80], [-68, -92], [-60, -99], [-51, -94], [-53, -83]]), CREAM)); pen(t, INK, true); pen(arc([-44, -73], [-56, -70], [-68, -78], [-70, -92], [-60, -100], [-50, -94], [-52, -84])); }
    // collar
    form(box([-22, -120], [44, -104], [46, -93], [-25, -108]), HOT); dot(32, -88, 5, CREAM, 51); pen(crv([[32, -93], [37, -88], [32, -83], [27, -88]]), INK, true);
    // head, tipped up toward him: broad skull, short blunt muzzle, thick little ears
    at(12, -152, 1.22, -0.62, () => {
      form(crv([[10, -27, 1], [25, -45], [33, -16, 1]]), OCHRE);
      const head = crv([[46, 8], [43, -3], [31, -9], [22, -14], [15, -25], [7, -31, 1], [-5, -53], [-12, -53], [-27, -26, 1], [-32, -10], [-33, 8], [-29, 20], [-22, 31, 1], [-10, 28], [-4, 35, 1], [6, 30], [20, 27], [34, 23], [43, 17]]);
      flat(head, OCHRE);
      inside(head, () => { flat(crv([[50, 10], [38, 1], [26, 1], [12, 9], [0, 17], [-14, 20], [-34, 24], [-20, 44], [10, 38], [40, 28]]), CREAM); flat(crv([[-3, -33, 1], [-8, -48], [-20, -30, 1]]), ROSE); });
      shade(head, crv([[-36, 12], [-10, 18], [10, 24], [38, 28], [30, 44], [-36, 44]]));
      pen(head, INK, true);
      dot(14, -18, 3.4, CREAM, 52);
      flat(crv([[8, -7], [15, -13], [23, -9], [16, -4]]), INK);
      flat(crv([[39, -2], [45, -4], [50, 2], [47, 10], [41, 7]]), INK);
      pen(arc([44, 11], [36, 16], [27, 15], [21, 9]));
    });
  });

  // ------------------------------------------------------------ the man
  at(MAN[0], MAN[1], MAN[2], 0, () => {
    // shoes: dark uppers, a grey toe; the right foot a little forward and turned out
    const shoe = (s: K[], toe: K[]) => { const o = crv(s); flat(o, INK); inside(o, () => flat(crv(toe), GREY)); pen(o, INK, true); };
    shoe([[-54, -12], [-52, -30], [-35, -36], [-17, -30], [-14, -10], [-17, 6], [-34, 13], [-50, 7]], [[-58, 3], [-34, -2], [-10, 3], [-14, 18], [-54, 18]]);
    shoe([[10, -8], [13, -26], [31, -32], [50, -26], [55, -6], [52, 10], [34, 18], [14, 12]], [[6, 8], [34, 3], [60, 8], [52, 24], [12, 24]]);
    pen(ln([-44, -14], [-26, -15]), GREY); pen(ln([22, -9], [42, -10]), GREY);
    // trousers
    form(crv([[-56, -166, 1], [-61, -120], [-58, -74], [-54, -28, 1], [-16, -27, 1], [-12, -70], [1, -112, 1], [13, -68], [15, -22, 1], [53, -22, 1], [58, -70], [61, -120], [58, -166, 1]]), INK);
    pen(arc([2, -158], [3, -136], [1, -114]), GREY); pen(arc([-50, -156], [-40, -144], [-35, -130]), GREY); pen(arc([-45, -78], [-37, -73], [-29, -75]), GREY); pen(arc([24, -76], [32, -72], [42, -77]), GREY); pen(ln([-50, -38], [-20, -37]), GREY); pen(ln([19, -32], [49, -33]), GREY);
    // everything above the belt leans a touch toward the dog
    at(0, -160, 1, -0.03, () => {
      // the hanging arm and its open hand: fingers in length order, thumb toward the body
      flat(crv([[-82, -266, 1], [-91, -240], [-95, -214], [-93, -190], [-90, -156, 1], [-68, -155, 1], [-70, -186], [-70, -212], [-64, -250, 1]]), SKIN);
      pen(arc([-82, -266], [-91, -240], [-95, -214], [-93, -190], [-90, -160])); pen(arc([-68, -159], [-70, -186], [-70, -212], [-64, -250]));
      pen(ln([-91, -208], [-85, -204]));
      at(-79, -158, 1.1, 0.16, () => {
        { const h: K[] = [[-90, -160, 1], [-94, -146], [-95, -134], [-94, -120], [-90, -114], [-87, -117], [-87, -124, 1], [-85, -110], [-82, -106], [-79, -109], [-79, -121, 1], [-77, -105], [-74, -101], [-71, -104], [-71, -119, 1], [-69, -108], [-66, -105], [-63, -109], [-62, -126, 1], [-58, -122], [-54, -116], [-52, -122], [-55, -136], [-60, -148], [-68, -158, 1]]; flat(crv(h), SKIN); pen(crv(h, false)); }
        pen(ln([-87, -124], [-88, -136])); pen(ln([-79, -121], [-80, -135])); pen(ln([-71, -119], [-72, -134])); pen(arc([-62, -126], [-63, -136], [-66, -142]));
      }, -79, -158);
      // T-shirt
      form(crv([[-22, -322, 1], [22, -322, 1], [24, -312], [12, -303], [0, -300], [-12, -303], [-24, -312]]), SKIN);
      const shirt = crv([[-24, -313, 1], [-50, -304, 1], [-58, -262], [-53, -214], [-56, -160, 1], [-28, -155], [0, -153], [30, -154], [60, -158, 1], [58, -214], [60, -262], [50, -304, 1], [24, -313, 1], [12, -303], [0, -300], [-12, -303]]);
      form(shirt, TEAL, crv([[6, -230], [30, -222], [64, -228], [68, -204], [58, -184], [30, -188], [12, -204]]));
      pen(arc([-23, -307], [-12, -297], [0, -294], [12, -297], [23, -307]));
      pen(arc([-52, -236], [-44, -230], [-40, -220])); pen(arc([-50, -176], [-38, -170], [-26, -172])); pen(arc([34, -178], [44, -172], [54, -175]));
      { const sl: K[] = [[-50, -304, 1], [-66, -296], [-78, -284], [-86, -262, 1], [-64, -246, 1], [-57, -262, 1]]; flat(crv(sl), TEAL); pen(crv(sl, false)); }
      // the mug, then the arm that holds it
      pen(arc([13, -258], [2, -256], [0, -246], [4, -236], [14, -234]));
      form(crv([[10, -268, 1], [11, -232], [18, -224], [42, -224], [49, -232], [50, -268, 1]]), HOT);
      form(crv([[10, -268], [18, -273], [30, -274], [42, -273], [50, -268], [42, -263], [30, -262], [18, -263]]), INK);
      { const fa = crv([[88, -268, 1], [101, -246], [107, -224], [102, -207], [86, -210], [58, -229, 1], [58, -259, 1], [72, -252, 1]]); flat(fa, SKIN); shade(fa, crv([[110, -230], [100, -200], [56, -224], [80, -222]])); pen(arc([88, -268], [101, -246], [107, -224], [102, -207], [86, -210], [62, -228])); pen(ln([62, -260], [72, -252])); }
      pen(ln([84, -238], [92, -231]));
      { const sr: K[] = [[50, -304, 1], [68, -296], [82, -284], [92, -266, 1], [68, -248, 1], [59, -262, 1]]; flat(crv(sr), TEAL); pen(crv(sr, false)); }
      { const h: K[] = [[62, -264, 1], [44, -267], [33, -265], [27, -260], [29, -256], [34, -255, 1], [26, -253], [24, -248], [27, -245], [33, -245, 1], [26, -242], [25, -237], [28, -234], [34, -234, 1], [29, -231], [29, -227], [33, -224], [46, -223], [62, -226, 1]]; flat(crv(h), SKIN); pen(crv(h, false)); }
      pen(ln([34, -255], [50, -256])); pen(ln([33, -245], [51, -245])); pen(ln([34, -234], [50, -235]));
      // the head, tipped a little further
      at(-3, -320, 1, -0.06, () => {
        form(crv([[-48, -394], [-58, -398], [-62, -386], [-58, -372], [-49, -368]]), SKIN); pen(arc([-55, -392], [-58, -384], [-54, -376]));
        form(crv([[48, -394], [59, -399], [64, -386], [59, -371], [49, -367]]), SKIN); pen(arc([56, -393], [59, -384], [55, -375]));
        form(crv([[-47, -412], [-36, -430], [0, -437], [36, -430], [47, -412], [51, -388], [49, -362], [40, -338], [22, -322], [0, -318], [-22, -322], [-40, -338], [-49, -362], [-51, -388]]), SKIN);
        // grey short sides
        form(crv([[-50, -384], [-53, -408], [-46, -428], [-34, -437], [-32, -422], [-40, -410], [-43, -392]]), GREY);
        form(crv([[50, -384], [54, -408], [47, -428], [35, -438], [33, -422], [41, -410], [44, -392]]), GREY);
        // a full dark beard, the lower lip showing in it
        form(crv([[-50, -380], [-54, -358], [-48, -332], [-36, -315], [-24, -312], [-14, -303], [-4, -305], [6, -300], [18, -306], [28, -310], [46, -331], [54, -357], [51, -380], [44, -376], [40, -362], [28, -355], [14, -361], [-2, -359], [-18, -361], [-30, -355], [-40, -362], [-44, -376]]), INK);
        form(crv([[-16, -346, 1], [-3, -343], [10, -346, 1], [6, -339], [-3, -337], [-11, -339]]), SKIN);
        pen(arc([-3, -380], [-8, -371], [-4, -365], [4, -367]));
        pen(arc([-14, -354], [-21, -351], [-26, -345]), GREY); pen(arc([9, -354], [17, -351], [22, -345]), GREY);
        // glasses with dark frames, the eyes behind them
        const lens = (o: K[]) => { const cx = o.reduce((a, p) => a + p[0], 0) / o.length, cy = o.reduce((a, p) => a + p[1], 0) / o.length; flat(crv(o), INK); pen(crv(o), INK, true); flat(crv(o.map(([x, y]) => [cx + (x - cx) * 0.7, cy + (y - cy) * 0.68] as K)), SKIN); };
        lens([[-40, -400], [-30, -404], [-16, -403], [-9, -396], [-9, -382], [-16, -375], [-30, -375], [-39, -381]]);
        lens([[4, -397], [11, -404], [26, -405], [37, -400], [38, -382], [30, -375], [14, -375], [5, -381]]);
        pen(arc([-9, -394], [-2, -397], [5, -394])); pen(ln([-40, -394], [-50, -392])); pen(ln([38, -394], [50, -392]));
        dot(-28, -387, 3.6, INK, 71); dot(17, -387, 3.6, INK, 72);
        pen(arc([-39, -414], [-28, -418], [-15, -414])); pen(arc([7, -415], [22, -420], [38, -413]));
        // the quiff: black, standing up, swept back and to one side
        form(crv([[-40, -420], [-47, -438], [-45, -458], [-36, -474], [-27, -471, 1], [-20, -486], [-6, -494], [6, -488, 1], [14, -497], [28, -491], [40, -478], [48, -460], [46, -440], [40, -424], [28, -436], [10, -432], [-8, -437], [-26, -432]]), INK);
        pen(arc([-30, -442], [-22, -462], [-8, -478]), GREY); pen(arc([-4, -444], [8, -462], [24, -476]), GREY); pen(arc([24, -442], [34, -452], [40, -464]), GREY);
      }, -3, -320);
    }, 0, -160);
  });

  // ------------------------------------------------------------ the only texture: a few hatch strokes
  hatch(176, 946, 5, 20, 81); hatch(336, 534, 4, 16, 83); hatch(1420, 316, 3, 16, 84); hatch(1492, 1004, 4, 15, 85); hatch(1056, 646, 3, 14, 86);
};

export const officeLine: Film = {
  meta: { title: "officeLine", W: 1920, H: 1080, fps: 30, bpm: 60, durationFrames: 1 },
  assets: { images: {} },
  shots: [{ id: "officeLine", start: 0, end: 1, draw: drawOfficeLine }],
};
