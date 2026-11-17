// Fits the game to the screen, and on a touch device adds the touch controls (#71), as decided in
// RadicalButton/asi-creative-dude#52 and #63 and picked by Asi on a phone:
//   - a stick that rests at the bottom left, dimmed, moves under the thumb wherever it touches, and goes back on
//     release: 4 directions, a 14 px dead zone (utils.stickDirection);
//   - an A button at the bottom right (Enter); it captures its pointer, so a thumb sliding off still lets go;
//   - a start button at the top left, only in the world (World sets body.in-world), straight to the title (Escape);
//   - landscape only: a "turn your phone sideways" screen in portrait.
// Every control is a synthetic key event the game already listens for, so no game logic knows about touch.
// The sprites are art/controls.py's; one art pixel is two game pixels, snapped to whole device pixels (--px).
import '../styles/touchControls.css';
import utils from './utils';

// ponytail: read once; a device that gains a touchscreen mid-visit gets the controls on its next load
export const isTouch = matchMedia('(any-pointer: coarse)').matches;

const container = document.querySelector('.game-container') as HTMLElement;
let artPx = 2; // one art pixel in CSS px, as --px

// The game stays 640x360, scaled to fit and centred, with position: fixed so no page CSS stretches it (#52).
function fit() {
  const W = innerWidth, H = innerHeight;
  const s = Math.min(W / 640, H / 360);
  Object.assign(container.style, {
    position: 'fixed', margin: '0', left: `${(W - 640 * s) / 2}px`, top: `${(H - 360 * s) / 2}px`,
    transformOrigin: '0 0', transform: `scale(${s})`,
  });
  const dpr = devicePixelRatio || 1;
  artPx = Math.max(1, Math.round(s * 2 * dpr)) / dpr;
  document.body.style.setProperty('--px', `${artPx}px`);
}
addEventListener('resize', fit);
fit();

const key = (type: 'keydown' | 'keyup', k: string) =>
  // dispatched on document, it bubbles to window too: World hears Escape there, the rest listen on document
  document.dispatchEvent(new KeyboardEvent(type, { key: k, code: k, bubbles: true }));
const KEYS: Record<string, string> = { up: 'ArrowUp', down: 'ArrowDown', left: 'ArrowLeft', right: 'ArrowRight' };

function el<T extends HTMLElement>(tag: string, cls: string, parent: HTMLElement = document.body) {
  const e = document.createElement(tag) as T;
  e.className = cls;
  parent.appendChild(e);
  return e;
}
function sprite(cls: string, name: string, parent?: HTMLElement) {
  const img = el<HTMLImageElement>('img', `touch-sprite ${cls}`, parent);
  img.alt = '';
  img.onload = () => img.style.setProperty('--w', String(img.naturalWidth));
  img.src = `/controls/${name}.png`;
  return img;
}

if (isTouch) {
  document.documentElement.classList.add('touch');

  // ---------- stick ----------
  const stick = el<HTMLDivElement>('div', 'touch-ui touch-stick');
  sprite('', 'base', stick);
  const knob = sprite('', 'knob', stick);
  let held: string | null = null;
  const hold = (d: string | null) => {
    if (d === held) return;
    if (held) key('keyup', KEYS[held]);
    held = d;
    if (d) key('keydown', KEYS[d]);
  };
  let stickId: number | null = null, sx = 0, sy = 0;
  addEventListener('pointerdown', (e) => {
    // any-pointer: coarse is true on a touchscreen laptop too: its mouse keeps clicking, it never drags a stick
    if (e.pointerType === 'mouse' || stickId !== null || (e.target as HTMLElement).closest('.touch-ui, button, a'))
      return;
    stickId = e.pointerId;
    sx = e.clientX;
    sy = e.clientY;
    stick.classList.add('held');
    Object.assign(stick.style, { left: `${sx}px`, top: `${sy}px` });
  });
  addEventListener('pointermove', (e) => {
    if (e.pointerId !== stickId) return;
    const dx = e.clientX - sx, dy = e.clientY - sy;
    const k = Math.min(1, (14 * artPx) / (Math.hypot(dx, dy) || 1)); // the knob stays in the gate, 14 art px
    knob.style.translate = `${dx * k}px ${dy * k}px`;
    hold(utils.stickDirection(dx, dy));
  });
  const release = (e: PointerEvent) => {
    if (e.pointerId !== stickId) return;
    stickId = null;
    stick.classList.remove('held');
    stick.style.left = stick.style.top = knob.style.translate = '';
    hold(null);
  };
  addEventListener('pointerup', release);
  addEventListener('pointercancel', release);

  // ---------- A button ----------
  const a = sprite('touch-ui touch-a', 'a');
  new Image().src = '/controls/a-on.png'; // the pressed frame, ready before the first press
  a.addEventListener('pointerdown', (e) => {
    e.preventDefault();
    a.src = '/controls/a-on.png';
    key('keydown', 'Enter');
    a.setPointerCapture(e.pointerId); // last: it throws on a pointer that is no longer down
  });
  const aUp = () => {
    a.src = '/controls/a.png';
    key('keyup', 'Enter');
  };
  a.addEventListener('pointerup', aUp);
  a.addEventListener('pointercancel', aUp);

  // ---------- start button: straight to the title ----------
  const start = sprite('touch-ui touch-start', 'start');
  start.addEventListener('click', () => (key('keydown', 'Escape'), key('keyup', 'Escape')));

  // ---------- portrait: turn your phone ----------
  const turn = el<HTMLDivElement>('div', 'touch-ui touch-turn');
  turn.innerHTML = '<div>↻<br>Turn your phone sideways</div>';
  turn.addEventListener('click', async () => {
    try {
      await document.documentElement.requestFullscreen();
      await (screen.orientation as ScreenOrientation & { lock(o: string): Promise<void> }).lock('landscape');
    } catch {
      /* iOS has neither: the player turns the phone */
    }
  });
}
