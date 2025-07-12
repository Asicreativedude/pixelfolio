import './styles/global.css';
import './styles/contactDetails.css';
import './styles/projectReveal.css';
import './styles/sceneTransition.css';
import './styles/textMessage.css';

import Stats from 'stats.js';
import TitleScreen from './titleScreen/titleScreen';

const stats = new Stats();
stats.showPanel(0); // 0: fps, 1: ms, 2: mb, 3+: custom
document.body.appendChild(stats.dom);

// Fit game to screen
function scaleGameContainer() {
  const container = document.querySelector('.game-container') as HTMLElement;
  const gameWidth = 640;
  const gameHeight = 360;

  const scaleX = window.innerWidth / gameWidth;
  const scaleY = window.innerHeight / gameHeight;
  const scale = Math.min(scaleX, scaleY);

  container.style.transform = `scale(${scale})`;
  container.style.display = 'block'; // ensure it's visible
}

window.addEventListener('load', scaleGameContainer);
window.addEventListener('resize', scaleGameContainer);

const gameContainer = document.querySelector('.game-container') as HTMLElement;

let activeTitleScreen: TitleScreen | null = null;

setTimeout(() => {
  gameContainer.style.display = 'block';

  activeTitleScreen = new TitleScreen(gameContainer);
  activeTitleScreen.init();

  gameContainer.classList.add('fade-in');
}, 1000);

window.addEventListener('keydown', (e) => {
  if (e.key === 'Escape' && !activeTitleScreen) {
    activeTitleScreen = new TitleScreen(gameContainer);
    activeTitleScreen.init();
  }
});
