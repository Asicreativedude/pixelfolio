import './styles/global.css';
import './styles/contactDetails.css';
import './styles/projectReveal.css';
import './styles/sceneTransition.css';
import './styles/textMessage.css';

import TitleScreen from './titleScreen/TitleScreen';

// PROTOTYPE (#63): touchControls owns fitting the game to the screen; stats.js is off, it sat under the menu tab
import './prototype/touchControls';

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
