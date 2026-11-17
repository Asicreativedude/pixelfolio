// PROTOTYPE (wayfinder RadicalButton/asi-creative-dude#63), throwaway, lives on branch prototype/touch-controls only.
// Answers: what should the touch controls #52 settled on look like, and how does touch get back to the title?
// #52's floating stick + A button + rotate prompt (prototype/mobile-controls, ?controls=stick&layout=rotate), redrawn
// in three skins by art/prototype_controls.py, plus a menu button that only shows in the world.
//
// Round 1, Asi on a phone: arcade, menu top left; the menu button needs work; the stick should show itself.
//   ?skin=arcade   the Hall's metal and red: bat-top stick in a gate, domed arcade A                (default)
//   ?skin=paper    the dialogue box's paper and amber Next button
//   ?skin=ghost    pale amber marks and their shadows, nearly nothing over the game
//   ?menu=card     the menu button pauses the game under a card: Resume / Title screen            (default)
//   ?menu=direct   the menu button goes straight to the title, like Escape
//   ?pos=left|centre|right   where the menu button sits along the top edge                       (default left)
//   ?btn=pill|start|coin     the arcade menu button: a pause pill, a round start button, a coin door (default pill)
//   ?stick=flash   the stick blinks at its rest spot (bottom left) when the world first opens, then hides (default)
//   ?stick=rest    the stick always sits at its rest spot, dimmed; it jumps under the thumb and comes back
// The title's first option reads CONTINUE GAME once there is a save (TitleScreen.ts, art/prototype_title.py).
//
// The switcher at the bottom has a button per param: a tap moves it on, live, no reload.
// On a phone: npm run dev -- --host, then open the Network URL it prints, in landscape.
// Every control is a synthetic key event the game already listens for (arrows, Enter, Escape): no game logic changes.
import './touchControls.css';

// each param's options, the first the default
const OPTIONS: Record<string, string[]> = {
  skin: ['arcade', 'paper', 'ghost'],
  menu: ['card', 'direct'],
  pos: ['left', 'centre', 'right'],
  btn: ['pill', 'start', 'coin'],
  stick: ['flash', 'rest'],
};
const q = new URLSearchParams(location.search);
const opt: Record<string, string> = {};
for (const [name, options] of Object.entries(OPTIONS)) opt[name] = options.includes(q.get(name)!) ? q.get(name)! : options[0];

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
  img.src = `/prototype/controls/${opt.skin}-${part}.png`;
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
// at rest (CSS places it bottom left), under the thumb (inline left/top), or hidden
function stickAt(where: 'rest' | 'thumb' | 'hidden') {
  for (const s of [base, knob]) {
    s.classList.toggle('at-rest', where === 'rest');
    s.classList.remove('flash');
    Object.assign(s.style, where === 'thumb' ? { left: `${sx}px`, top: `${sy}px`, display: 'block' } : { left: '', top: '', display: '' });
    s.style.translate = '';
  }
}
const stickIdle = () => stickAt(opt.stick === 'rest' ? 'rest' : 'hidden');
// ?stick=flash: the first time the world opens, the stick blinks at its rest spot, then hides
let flashed = false;
function flashStick() {
  if (flashed || opt.stick !== 'flash' || stickId !== null) return;
  flashed = true;
  stickAt('rest');
  for (const s of [base, knob]) s.classList.add('flash');
  base.addEventListener('animationend', () => stickId === null && stickIdle(), { once: true });
}
addEventListener('pointerdown', (e) => {
  if (!isFree(e) || paused() || stickId !== null) return;
  stickId = e.pointerId;
  sx = e.clientX;
  sy = e.clientY;
  stickAt('thumb');
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
  stickIdle();
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
menu.addEventListener('click', () => (opt.menu === 'card' ? setPaused(true) : press('menu')));
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
    else flashStick();
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

// ---------- switcher: a button per param, a tap moves it on ----------
const bar = el(
  'div',
  'proto-switch',
  Object.keys(OPTIONS).map((name) => `<button data-opt="${name}"></button>`).join('') + '<span></span>'
);
const label = bar.querySelector('span')!;
bar.addEventListener('click', (e) => {
  const name = (e.target as HTMLElement).dataset.opt;
  if (!name) return;
  const options = OPTIONS[name];
  opt[name] = options[(options.indexOf(opt[name]) + 1) % options.length];
  apply();
});
function readout() {
  label.textContent = `${held ?? ''}${paused() ? ' paused' : ''}`;
}
function apply() {
  for (const [name, options] of Object.entries(OPTIONS))
    for (const o of options) document.body.classList.toggle(`${name}-${o}`, o === opt[name]);
  for (const b of bar.querySelectorAll<HTMLElement>('[data-opt]')) b.textContent = opt[b.dataset.opt!];
  sprite(base, 'base');
  sprite(knob, 'knob');
  sprite(a, 'a');
  sprite(menu, opt.skin === 'arcade' && opt.btn !== 'pill' ? `menu-${opt.btn}` : 'menu');
  if (stickId === null) stickIdle();
  // keeps the game's own dev params (?map=, ?time=) in the URL
  for (const name of Object.keys(OPTIONS)) q.set(name, opt[name]);
  history.replaceState(null, '', `?${q}`);
  readout();
}
apply();
fit();
