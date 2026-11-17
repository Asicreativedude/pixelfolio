// PROTOTYPE (wayfinder RadicalButton/asi-creative-dude#63), throwaway, lives on branch prototype/touch-controls only.
// Answers: what should the touch controls #52 settled on look like, and how does touch get back to the title?
// #52's floating stick + A button + rotate prompt (prototype/mobile-controls, ?controls=stick&layout=rotate), redrawn
// in three skins by art/prototype_controls.py, plus a menu button that only shows in the world.
//
//   ?skin=paper    the dialogue box's paper and amber Next button; the menu is a paper tab          (default)
//   ?skin=arcade   the Hall's metal and red: bat-top stick in a gate, domed arcade A; the menu a pause pill
//   ?skin=ghost    pale amber marks and their shadows, nearly nothing over the game; the menu three bars
//   ?menu=card     the menu button pauses the game under a card: Resume / Title screen            (default)
//   ?menu=direct   the menu button goes straight to the title, like Escape
//   ?pos=left|centre|right   where the menu button sits along the top edge                       (default left)
//
// The switcher at the bottom flips all three live, no reload, so you can compare in the middle of a room:
// the arrows step through skin x menu, the third button moves the menu button.
// On a phone: npm run dev -- --host, then open the Network URL it prints, in landscape.
// Every control is a synthetic key event the game already listens for (arrows, Enter, Escape): no game logic changes.
import './touchControls.css';

const SKINS = ['paper', 'arcade', 'ghost'];
const MENUS = ['card', 'direct'];
const POSITIONS = ['left', 'centre', 'right'];
const q = new URLSearchParams(location.search);
const pick = (name: string, options: string[]) => (options.includes(q.get(name)!) ? q.get(name)! : options[0]);
let skin = pick('skin', SKINS);
let menuMode = pick('menu', MENUS);
let pos = pick('pos', POSITIONS);

const KEYS: Record<string, string> = {
  up: 'ArrowUp', down: 'ArrowDown', left: 'ArrowLeft', right: 'ArrowRight', a: 'Enter', menu: 'Escape',
};
const key = (type: 'keydown' | 'keyup', name: string) =>
  document.dispatchEvent(new KeyboardEvent(type, { key: KEYS[name], code: KEYS[name], bubbles: true }));
// World listens for Escape on window, the rest on document: dispatched on document, it bubbles to both
const press = (name: string) => (key('keydown', name), key('keyup', name));

const world = () => (window as any).__world as any;
const container = document.querySelector('.game-container') as HTMLElement;

const el = <T extends HTMLElement = HTMLDivElement>(tag: string, cls: string, html = '') => {
  const e = document.createElement(tag) as T;
  e.className = `proto-ui ${cls}`;
  e.innerHTML = html;
  document.body.appendChild(e);
  return e;
};
const sprite = (img: HTMLImageElement, part: string) => {
  img.onload = () => img.style.setProperty('--w', String(img.naturalWidth));
  img.src = `/prototype/controls/${skin}-${part}.png`;
};

// ---------- layout: #52's fit, landscape only ----------
function fit() {
  const W = innerWidth, H = innerHeight;
  const s = Math.min(W / 640, H / 360);
  Object.assign(container.style, {
    position: 'fixed', margin: '0', left: `${(W - 640 * s) / 2}px`, top: `${(H - 360 * s) / 2}px`,
    transformOrigin: '0 0', transform: `scale(${s})`,
  });
  // one art pixel = two game pixels, snapped to whole device pixels so the sprites stay crisp
  const dpr = devicePixelRatio || 1;
  document.body.style.setProperty('--px', `${Math.max(1, Math.round(s * 2 * dpr)) / dpr}px`);
}
addEventListener('resize', fit);
addEventListener('load', fit);

// ---------- floating stick ----------
const base = el<HTMLImageElement>('img', 'proto-base');
const knob = el<HTMLImageElement>('img', 'proto-knob');
let held: string | null = null;
function hold(d: string | null) {
  if (d === held) return;
  if (held) key('keyup', held);
  held = d;
  if (d) key('keydown', d);
  readout();
}
const dirFrom = (dx: number, dy: number, dead: number) =>
  Math.hypot(dx, dy) < dead ? null : Math.abs(dx) > Math.abs(dy) ? (dx > 0 ? 'right' : 'left') : dy > 0 ? 'down' : 'up';
const px = () => parseFloat(document.body.style.getPropertyValue('--px')) || 2;

let stickId: number | null = null, sx = 0, sy = 0;
const isFree = (e: PointerEvent) => !(e.target as HTMLElement).closest('.proto-ui, button, a');
const paused = () => document.body.classList.contains('proto-paused');
addEventListener('pointerdown', (e) => {
  if (!isFree(e) || paused() || stickId !== null) return;
  stickId = e.pointerId;
  sx = e.clientX;
  sy = e.clientY;
  for (const s of [base, knob]) Object.assign(s.style, { left: `${sx}px`, top: `${sy}px`, display: 'block', translate: '' });
});
addEventListener('pointermove', (e) => {
  if (e.pointerId !== stickId || paused()) return;
  const dx = e.clientX - sx, dy = e.clientY - sy, reach = 14 * px(), k = Math.min(1, reach / (Math.hypot(dx, dy) || 1));
  knob.style.translate = `${dx * k}px ${dy * k}px`;
  hold(dirFrom(dx, dy, 14));
});
const stickEnd = (e: PointerEvent) => {
  if (e.pointerId !== stickId) return;
  stickId = null;
  base.style.display = knob.style.display = 'none';
  hold(null);
};
addEventListener('pointerup', stickEnd);
addEventListener('pointercancel', stickEnd);

// ---------- A button ----------
const a = el<HTMLImageElement>('img', 'proto-a');
a.addEventListener('pointerdown', (e) => {
  e.preventDefault();
  sprite(a, 'a-on');
  key('keydown', 'a');
  a.setPointerCapture(e.pointerId); // a thumb sliding off still lets go of Enter. Last: it throws on a pointer that is not down
});
const aUp = () => (sprite(a, 'a'), key('keyup', 'a'));
a.addEventListener('pointerup', aUp);
a.addEventListener('pointercancel', aUp);

// ---------- menu button + pause card ----------
const menu = el<HTMLImageElement>('img', 'proto-menu');
const card = el(
  'div',
  'proto-card',
  '<div><p>Paused</p><button data-do="resume">Resume</button><button data-do="title">Title screen</button></div>'
);
const setPaused = (on: boolean) => {
  if (on === paused()) return;
  document.body.classList.toggle('proto-paused', on);
  if (on) hold(null);
  // a real pause: World's loop stops on isGameRunning and is started again on resume
  const w = world();
  if (w?.map) {
    w.isGameRunning = !on;
    if (!on) w.startGameLoop();
  }
  readout();
};
menu.addEventListener('click', () => (menuMode === 'card' ? setPaused(true) : press('menu')));
card.addEventListener('click', (e) => {
  const act = (e.target as HTMLElement).closest('button')?.dataset.do;
  if (!act && e.target !== card) return;
  setPaused(false);
  if (act === 'title') press('menu');
});
// ponytail: polls for the World so the menu button only shows there; an event if this survives
setInterval(() => {
  const inWorld = !!world()?.map;
  if (inWorld !== document.body.classList.contains('proto-in-world')) {
    document.body.classList.toggle('proto-in-world', inWorld);
    if (!inWorld) setPaused(false);
  }
}, 250);

// ---------- rotate prompt (#52) ----------
const rot = el('div', 'proto-rotate', '<div>↻<br>Turn your phone sideways</div>');
rot.addEventListener('click', async () => {
  try {
    await document.documentElement.requestFullscreen();
    await (screen.orientation as any).lock('landscape');
  } catch {
    /* iOS: no fullscreen or orientation lock, the player has to rotate */
  }
});

// ---------- switcher: flips skin and menu live ----------
const COMBOS = SKINS.flatMap((s) => MENUS.map((m) => [s, m]));
const bar = el(
  'div',
  'proto-switch',
  '<button data-d="-1">◀</button><span></span><button data-d="1">▶</button><button data-pos>pos</button>'
);
const label = bar.querySelector('span')!;
bar.addEventListener('click', (e) => {
  const t = e.target as HTMLElement;
  if (t.dataset.pos !== undefined) {
    pos = POSITIONS[(POSITIONS.indexOf(pos) + 1) % POSITIONS.length];
    return apply();
  }
  const d = Number(t.dataset.d);
  if (!d) return;
  const i = COMBOS.findIndex(([s, m]) => s === skin && m === menuMode);
  [skin, menuMode] = COMBOS[(i + d + COMBOS.length) % COMBOS.length];
  apply();
});
function readout() {
  label.textContent = `${skin} · menu ${menuMode} ${pos}${held ? ` · ${held}` : ''}${paused() ? ' · paused' : ''}`;
}
function apply() {
  for (const s of SKINS) document.body.classList.toggle(`skin-${s}`, s === skin);
  for (const p of POSITIONS) document.body.classList.toggle(`pos-${p}`, p === pos);
  sprite(base, 'base');
  sprite(knob, 'knob');
  sprite(a, 'a');
  sprite(menu, 'menu');
  // keeps the game's own dev params (?map=, ?time=) in the URL
  q.set('skin', skin);
  q.set('menu', menuMode);
  q.set('pos', pos);
  history.replaceState(null, '', `?${q}`);
  readout();
}
apply();
fit();
