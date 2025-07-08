import World from './world/defineWorld';

/* ADD SFX */

// import { Howl } from 'howler';

// let worldMusic = new Howl({
// 	src: ['/audio/jazz the rabbit.mp3'],
// 	sprite: {
// 		action: [9000, 60000],
// 	},
// 	volume: 0.2,
// });

function startGame(gameContainer: HTMLElement) {
  setTimeout(() => {
    gameContainer.style.display = 'block';

    const world = new World({
      element: gameContainer,
    });
    world.init();

    gameContainer.classList.add('fade-in');
  }, 1000);
}

function chooseCharacter(titleScreen: HTMLElement, gameContainer: HTMLElement) {
  titleScreen.classList.add('fade-out');
  setTimeout(() => {
    titleScreen.style.display = 'none';
  }, 1000);

  startGame(gameContainer);
}

const titleScreen = document.querySelector(
  '.titleScreen-wrapper'
) as HTMLElement;

const startCTA = document.querySelector('.startgame') as HTMLElement;
if (!titleScreen) {
  throw new Error('Title screen element not found');
}
const gameContainer = document.querySelector('.game-container') as HTMLElement;

const keys = [
  'w',
  'a',
  's',
  'd',
  'ArrowUp',
  'ArrowLeft',
  'ArrowDown',
  'ArrowRight',
  'Enter',
];

document.addEventListener('keydown', (e) => {
  if (!titleScreen.classList.contains('fade-out')) {
    console.log(e.key);
    if (e.code === 'Space') {
      // music.worldMusic.play();
      chooseCharacter(titleScreen, gameContainer);
    }

    for (const key of keys) {
      if (e.key === key) {
        const element = document.querySelector(
          `.keyboardBtn[data-btn="${key}"]`
        ) as HTMLElement;
        if (element) {
          element.style.transform = 'translateY(5px)';
        }
      }
    }
  }
});
document.addEventListener('keyup', (e) => {
  if (!titleScreen.classList.contains('fade-out')) {
    if (e.code === 'Space') {
      chooseCharacter(titleScreen, gameContainer);
    }

    for (const key of keys) {
      if (e.key === key) {
        const element = document.querySelector(
          `.keyboardBtn[data-btn="${key}"]`
        ) as HTMLElement;
        if (element) {
          element.style.transform = 'translateY(-5px)';
        }
      }
    }
  }
});

startCTA.addEventListener('click', () => {
  // worldMusic.play('action');
  chooseCharacter(titleScreen, gameContainer);
});
