import './styles/global.css';
import './styles/contactDetails.css';
import './styles/projectReveal.css';
import './styles/sceneTransition.css';
import './styles/textMessage.css';

import Stats from 'stats.js';
import TitleScreen from './titleScreen/TitleScreen';

window.addEventListener('DOMContentLoaded', () => {
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

  const gameContainer = document.querySelector(
    '.game-container'
  ) as HTMLElement;
  console.log('Game container:', gameContainer);

  if (!gameContainer) {
    console.error('game-container not found');
    return;
  }
  setTimeout(() => {
    gameContainer.style.display = 'block';

    const titleScreen = new TitleScreen(gameContainer);
    titleScreen.init();
    gameContainer.classList.add('fade-in');
  }, 1000);
});
