// PROTOTYPE (wayfinder RadicalButton/asi-creative-dude#52), throwaway, lives on
// branch prototype/mobile-controls only. Answers: how does Pixelfolio play on a phone?
//
//   ?controls=dpad   fixed d-pad (roll your thumb) + A button       (default)
//   ?controls=stick  floating joystick: touch anywhere, drag + A button
//   ?controls=tap    tap a tile to walk there, tap a person to talk; no buttons.
//                    Menus: swipe to move, tap to pick.
//   ?layout=fit      16:9 game scaled to fit; portrait = game on top, controls below (default)
//   ?layout=tall     portrait gets a taller camera (360 px wide world view) once in the world
//   ?layout=rotate   portrait shows "turn your phone"; Android tries fullscreen + landscape lock
//
// Every control is turned into the same synthetic keyboard events the game already
// listens for (arrows + Enter), so no game logic changes for dpad/stick.
import './mobileControls.css';

const q = new URLSearchParams(location.search);
const CONTROLS = ['dpad', 'stick', 'tap'];
const LAYOUTS = ['fit', 'tall', 'rotate'];
const controls = CONTROLS.includes(q.get('controls')!) ? q.get('controls')! : 'dpad';
const layout = LAYOUTS.includes(q.get('layout')!) ? q.get('layout')! : 'fit';
const PANEL = controls === 'tap' ? 0 : 230; // portrait space reserved under the game for buttons

const KEYS: Record<string, string> = { up: 'ArrowUp', down: 'ArrowDown', left: 'ArrowLeft', right: 'ArrowRight', a: 'Enter' };
const key = (type: 'keydown' | 'keyup', name: string) =>
  document.dispatchEvent(new KeyboardEvent(type, { key: KEYS[name], code: KEYS[name], bubbles: true }));
const press = (name: string) => (key('keydown', name), key('keyup', name));

const world = () => (window as any).__world as any;
const container = document.querySelector('.game-container') as HTMLElement;
const canvas = container.querySelector('canvas') as HTMLCanvasElement;

document.body.classList.add(`mode-${controls}`, `layout-${layout}`);

// ---------- layout ----------
function fit() {
  const W = innerWidth, H = innerHeight;
  const portrait = H > W;
  const avail = portrait ? H - PANEL : H;
  let cw = 640, ch = 360;
  if (layout === 'tall' && portrait && world()) {
    cw = 360;
    ch = Math.max(360, Math.min(800, Math.round((360 * avail) / W / 2) * 2));
  }
  if (canvas.width !== cw || canvas.height !== ch) {
    canvas.width = cw;
    canvas.height = ch;
  }
  const s = Math.min(W / cw, avail / ch);
  Object.assign(container.style, {
    position: 'fixed',
    margin: '0',
    width: `${cw}px`,
    height: `${ch}px`,
    left: `${(W - cw * s) / 2}px`,
    top: `${(avail - ch * s) / 2}px`,
    transformOrigin: '0 0',
    transform: `scale(${s})`,
  });
  state();
}
addEventListener('resize', fit);
addEventListener('load', fit);
// ponytail: polls for World start/stop so `tall` can swap canvas size; an event if this survives
let hadWorld = false;
setInterval(() => {
  if (!!world() !== hadWorld) (hadWorld = !!world()), fit();
}, 250);

// ---------- shared hold logic (dpad + stick) ----------
let held: string | null = null;
function hold(d: string | null) {
  if (d === held) return;
  if (held) key('keyup', held);
  held = d;
  if (d) key('keydown', d);
  pad.dataset.held = d ?? '';
  state();
}
const dirFrom = (dx: number, dy: number, dead: number) =>
  Math.hypot(dx, dy) < dead ? null : Math.abs(dx) > Math.abs(dy) ? (dx > 0 ? 'right' : 'left') : dy > 0 ? 'down' : 'up';

const el = (cls: string, html = '') => {
  const e = document.createElement('div');
  e.className = `proto-ui ${cls}`;
  e.innerHTML = html;
  document.body.appendChild(e);
  return e;
};

// d-pad
const pad = el('proto-pad', '<i class="u"></i><i class="d"></i><i class="l"></i><i class="r"></i>');
const padDir = (e: PointerEvent) => {
  const r = pad.getBoundingClientRect();
  hold(dirFrom(e.clientX - r.left - r.width / 2, e.clientY - r.top - r.height / 2, 10));
};
pad.addEventListener('pointerdown', (e) => (e.preventDefault(), pad.setPointerCapture(e.pointerId), padDir(e)));
pad.addEventListener('pointermove', (e) => pad.hasPointerCapture(e.pointerId) && padDir(e));
pad.addEventListener('pointerup', () => hold(null));
pad.addEventListener('pointercancel', () => hold(null));

// A button
const a = el('proto-a', 'A');
a.addEventListener('pointerdown', (e) => (e.preventDefault(), a.classList.add('on'), key('keydown', 'a')));
const aUp = () => (a.classList.remove('on'), key('keyup', 'a'));
a.addEventListener('pointerup', aUp);
a.addEventListener('pointercancel', aUp);

// floating stick
const stick = el('proto-stick', '<b></b>');
const knob = stick.firstElementChild as HTMLElement;
let stickId: number | null = null, sx = 0, sy = 0;

// taps on the game area (stick + tap modes); ignore our UI and DOM buttons (TextMessage "Next")
const isFree = (e: PointerEvent) => !(e.target as HTMLElement).closest('.proto-ui, button, a');
let tapStart: { id: number; x: number; y: number } | null = null;

addEventListener('pointerdown', (e) => {
  if (!isFree(e)) return;
  if (controls === 'stick' && stickId === null) {
    stickId = e.pointerId;
    sx = e.clientX;
    sy = e.clientY;
    Object.assign(stick.style, { left: `${sx}px`, top: `${sy}px`, display: 'block' });
    knob.style.transform = '';
  }
  if (controls === 'tap') tapStart = { id: e.pointerId, x: e.clientX, y: e.clientY };
});
addEventListener('pointermove', (e) => {
  if (e.pointerId !== stickId) return;
  const dx = e.clientX - sx, dy = e.clientY - sy, len = Math.hypot(dx, dy), k = Math.min(1, 40 / (len || 1));
  knob.style.transform = `translate(${dx * k}px, ${dy * k}px)`;
  hold(dirFrom(dx, dy, 14));
});
const pointerEnd = (e: PointerEvent) => {
  if (e.pointerId === stickId) {
    stickId = null;
    stick.style.display = 'none';
    hold(null);
  }
  if (tapStart && e.pointerId === tapStart.id) {
    const dx = e.clientX - tapStart.x, dy = e.clientY - tapStart.y;
    tapStart = null;
    const w = world();
    if (Math.hypot(dx, dy) > 30) {
      if (!w) press(dirFrom(dx, dy, 0)!); // menus: swipe = arrow
    } else if (w && !w.map.isCutscenePlaying) walkTo(e.clientX, e.clientY);
    else press('a'); // menus pick, dialogue advances
  }
};
addEventListener('pointerup', pointerEnd);
addEventListener('pointercancel', pointerEnd);

// ---------- tap to walk ----------
type Goal = { x: number; y: number; act: boolean };
let goal: Goal | null = null;
let stuck: ReturnType<typeof setTimeout>;
const DIRS: [string, number, number][] = [['up', 0, -32], ['down', 0, 32], ['left', -32, 0], ['right', 32, 0]];
const FEET_Y = 16; // hero feet sit this far below the sprite centre; calibrate by tapping NPCs

function walkTo(cx: number, cy: number) {
  const w = world(), hero = w.map.gameObjects.hero, cam = w.cameraPerson ?? hero;
  const r = canvas.getBoundingClientRect();
  const px = ((cx - r.left) * canvas.width) / r.width, py = ((cy - r.top) * canvas.height) / r.height;
  // same maths as Sprite.draw: the hero's feet on screen
  const hx = hero.x + canvas.width / 2 - 16 - cam.x, hy = hero.y + canvas.height / 2 + 8 - cam.y + FEET_Y;
  goal = { x: hero.x + Math.round((px - hx) / 32) * 32, y: hero.y + Math.round((py - hy) / 32) * 32, act: false };
  const m = el('proto-tap');
  Object.assign(m.style, { left: `${cx}px`, top: `${cy}px` });
  setTimeout(() => m.remove(), 450);
  if (!hero.isWalking) step();
}

// ponytail: BFS capped at 3000 tiles, re-run every step so moving NPCs are handled
function bfs(walls: Record<string, boolean>, sx: number, sy: number, g: Goal): string[] | null {
  const k = (x: number, y: number) => `${x},${y}`;
  const start = k(sx, sy), gk = k(g.x, g.y);
  const blocked = gk !== start && !!walls[gk];
  g.act = blocked || gk === start; // tapped a person/thing, or yourself: interact on arrival
  const isGoal = (x: number, y: number) =>
    blocked ? Math.abs(x - g.x) + Math.abs(y - g.y) === 32 : x === g.x && y === g.y;
  const prev = new Map<string, [string, string] | null>([[start, null]]);
  const queue: [number, number][] = [[sx, sy]];
  while (queue.length && prev.size < 3000) {
    const [x, y] = queue.shift()!;
    if (isGoal(x, y)) {
      const path: string[] = [];
      for (let c = prev.get(k(x, y)); c; c = prev.get(c[0])) path.unshift(c[1]);
      return path;
    }
    for (const [d, dx, dy] of DIRS) {
      const nk = k(x + dx, y + dy);
      if (prev.has(nk) || walls[nk]) continue;
      prev.set(nk, [k(x, y), d]);
      queue.push([x + dx, y + dy]);
    }
  }
  return null;
}

function stop() {
  goal = null;
  if (world()) world().directionInput.heldDirections = [];
  state();
}

function step() {
  const w = world();
  if (!w || !goal || w.map.isCutscenePlaying) return stop();
  const hero = w.map.gameObjects.hero;
  const path = bfs(w.map.walls, hero.x, hero.y, goal);
  if (!path) return stop();
  if (!path.length) {
    if (goal.act) {
      const d = DIRS.find(([, dx, dy]) => hero.x + dx === goal!.x && hero.y + dy === goal!.y);
      if (d) hero.direction = d[0];
      w.map.checkForActionCutscene();
    }
    return stop();
  }
  w.directionInput.heldDirections = [path[0]];
  const at = `${hero.x},${hero.y}`;
  clearTimeout(stuck);
  stuck = setTimeout(() => !hero.isWalking && `${hero.x},${hero.y}` === at && stop(), 300);
  state();
}
// sync: the game loop runs several updates per frame, so a deferred step overshoots a tile.
// If a footstep cutscene starts right after, the hero can't walk and the stuck timer stops us.
document.addEventListener('PersonWalkingComplete', (e: any) => {
  if (e.detail.whoId === 'hero' && goal) step();
});

// ---------- rotate prompt ----------
const rot = el('proto-rotate', '<div>↻<br>Turn your phone sideways</div>');
rot.addEventListener('click', async () => {
  try {
    await document.documentElement.requestFullscreen();
    await (screen.orientation as any).lock('landscape');
  } catch {
    /* iOS: no fullscreen / orientation lock, user must rotate */
  }
});

// ---------- variant switcher + state readout ----------
const link = (c: string, l: string, label: string, on: boolean) =>
  `<a href="?controls=${c}&layout=${l}" class="${on ? 'on' : ''}">${label}</a>`;
const sw = el(
  'proto-switch',
  `<button class="chip">${controls} · ${layout} ▾</button><div class="menu">
  <p>controls</p>${CONTROLS.map((c) => link(c, layout, c, c === controls)).join('')}
  <p>layout</p>${LAYOUTS.map((l) => link(controls, l, l, l === layout)).join('')}
  <pre></pre></div>`
);
sw.querySelector('.chip')!.addEventListener('click', () => sw.classList.toggle('open'));
const readout = sw.querySelector('pre')!;
function state() {
  if (!sw.classList.contains('open')) return;
  readout.textContent = `canvas ${canvas.width}×${canvas.height}  scale ${container.style.transform.replace(/[^\d.]/g, '').slice(0, 4)}
held ${held ?? '-'}  goal ${goal ? `${goal.x},${goal.y}${goal.act ? ' act' : ''}` : '-'}
world ${world() ? 'yes' : 'no'}  ${innerWidth}×${innerHeight}`;
}
setInterval(state, 300);
fit();
