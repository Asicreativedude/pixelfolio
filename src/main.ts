import './styles/global.css';
import './styles/contactDetails.css';
import './styles/projectReveal.css';
import './styles/sceneTransition.css';
import './styles/textMessage.css';

import Stats from 'stats.js';
import TitleScreen from './titleScreen/TitleScreen';
import { isTouch } from './utils/touchControls'; // also fits the game to the screen

// not on a touch device: the panel sits over the start button, top left
if (!isTouch) {
  const stats = new Stats();
  stats.showPanel(0); // 0: fps, 1: ms, 2: mb, 3+: custom
  document.body.appendChild(stats.dom);
}

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
