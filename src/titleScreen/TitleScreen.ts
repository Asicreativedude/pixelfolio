import utils from '../utils/utils';
// import CharacterSelection from './characterSelection';
import TitleScreenSprite from './TitleScreenSprite';

type TitleOption = {
  label: string;
  x: number;
  y: number;
  action: () => void;
};

export default class TitleScreen {
  selectedOption: number;
  titleOptions: TitleOption[];
  arrowSprite: TitleScreenSprite;
  titleSprite: TitleScreenSprite;
  titleTexts: HTMLImageElement;
  canvas: HTMLCanvasElement;
  ctx: CanvasRenderingContext2D;
  gameStarted: boolean;
  // charSelect: CharacterSelection;

  constructor(gameContainer: HTMLElement) {
    this.gameStarted = false;
    this.canvas = gameContainer.querySelector('canvas')!;
    this.ctx = this.canvas.getContext('2d')!;
    this.selectedOption = 0;
    this.titleOptions = [
      {
        label: 'Start Game',
        x: 204,
        y: 187,
        action: async () => {
          console.log('Start Game selected!');
          this.gameStarted = true;
          try {
            const module = await import('./characterSelection');
            console.log('CharacterSelection module loaded');
            const CharacterSelection = module.default;
            const charSelect = new CharacterSelection(gameContainer);
            charSelect.init();
          } catch (err) {
            console.error(
              'Failed to load character selection:',
              err instanceof Error ? err.stack : err
            );
          }
        },
      },
      {
        label: 'View Boring Portfolio',
        x: 128,
        y: 222,
        action: () => window.open('https:/asicreativedude.com', '_blank'),
      },
      {
        label: 'About',
        x: 244,
        y: 257,
        action: () => window.open('https:/asicreativedude.com', '_blank'),
      },
    ];
    this.arrowSprite = new TitleScreenSprite({
      x: utils.withGrid(0),
      y: utils.withGrid(0),
      src: '../../arrowSprite.png',
      frameWidth: 27,
      frameHeight: 16,
      animations: {
        arrowLoop: {
          frames: [
            [0, 0],
            [1, 0],
            [2, 0],
            [3, 0],
            [4, 0],
            [5, 0],
            [6, 0],
            [7, 0],
            [8, 0],
            [9, 0],
          ],
        },
      },
    });
    this.titleSprite = new TitleScreenSprite({
      x: utils.withGrid(4.5),
      y: utils.withGrid(1),
      src: '../../titleSprite.png',
      frameWidth: 351,
      frameHeight: 51,
      animations: {
        arrowLoop: {
          frames: [
            [0, 0],
            [1, 0],
            [2, 0],
            [3, 0],
            [4, 0],
            [5, 0],
            [6, 0],
            [7, 0],
            [8, 0],
          ],
        },
      },
    });
    this.titleTexts = new Image();
    this.titleTexts.src = '../../titleScreenText.png';
  }

  drawTitleScreen() {
    this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
    const { x, y } = this.titleOptions[this.selectedOption];
    this.arrowSprite.draw(this.ctx, x, y);
    this.titleSprite.draw(this.ctx, this.titleSprite.x, this.titleSprite.y);
    this.ctx.drawImage(this.titleTexts, 0, 0);
  }
  startTitleLoop() {
    let previousMs: number;
    const step = 1 / 60;
    const stepFn = (timestampMs: number) => {
      if (previousMs === undefined) {
        previousMs = timestampMs;
      }
      let delta = (timestampMs - previousMs) / 1000;
      while (delta > step) {
        !this.gameStarted && this.drawTitleScreen();
        // : this.charSelect.drawTitleScreen();
        delta -= step;
      }
      previousMs = timestampMs - delta * 1000;
      requestAnimationFrame(stepFn);
    };

    // First call to kick off the loop
    requestAnimationFrame(stepFn);
  }

  handleInput(e: KeyboardEvent, titleOptions: TitleOption[]) {
    // optional split input handling
    if (e.key === 'ArrowDown') {
      this.selectedOption = (this.selectedOption + 1) % titleOptions.length;
    } else if (e.key === 'ArrowUp') {
      this.selectedOption =
        (this.selectedOption - 1 + titleOptions.length) % titleOptions.length;
    } else if (e.key === 'Enter') {
      titleOptions[this.selectedOption].action();
    }
  }

  init(): void {
    this.startTitleLoop();
    window.addEventListener('keydown', (e) => {
      if (this.gameStarted) return;
      this.handleInput(e, this.titleOptions);
    });
  }

  //   destroy(): void {
  //     this.remove();
  //   }
}
