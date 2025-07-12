import RevealingText from '../utils/revealText';
import { ScreenController } from '../utils/screenContorller';
import utils from '../utils/utils';
import TitleScreenSprite from './titleScreenSprite';

export default class AboutScreen {
  gameContainer: HTMLElement;
  textEffect: RevealingText;
  canvas: HTMLCanvasElement;
  textCanvas: HTMLCanvasElement;
  ctx: CanvasRenderingContext2D;
  fontImage: HTMLImageElement;
  arrowSprite: TitleScreenSprite;
  boundHandleInput!: (e: KeyboardEvent) => void;
  private animationFrameId: number | null = null;

  constructor(gameContainer: HTMLElement) {
    this.gameContainer = gameContainer;
    this.canvas = gameContainer.querySelector('canvas')!;
    this.ctx = this.canvas.getContext('2d')!;
    this.fontImage = new Image();
    this.fontImage.src = '/Letters.png';

    // Add a new canvas for text
    const textCanvas = document.createElement('canvas');
    textCanvas.width = this.canvas.width * 0.8;
    textCanvas.height = this.canvas.height;
    textCanvas.style.position = 'absolute';
    textCanvas.style.top = '0';
    textCanvas.style.left = '0';
    gameContainer.appendChild(textCanvas);
    this.textCanvas = textCanvas;

    this.textEffect = new RevealingText({
      canvas: textCanvas,
      text: "Hi, I'm Asi, the creator of this game. I love building nostalgic, interactive experiences like this one. Hope you're enjoying the journey!",
      speed: 120,
      fontImage: this.fontImage,
      distanceFromTop: 32,
    });
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
  }
  startAboutLoop() {
    let previousMs: number;
    const step = 1 / 60;
    const stepFn = (timestampMs: number) => {
      if (previousMs === undefined) {
        previousMs = timestampMs;
      }
      let delta = (timestampMs - previousMs) / 1000;
      while (delta > step) {
        this.ctx.fillStyle = 'white';
        this.ctx.fillRect(
          32,
          256,
          this.arrowSprite.frameWidth,
          this.arrowSprite.frameHeight
        );
        this.arrowSprite.draw(this.ctx, 32, 256);
        delta -= step;
      }
      previousMs = timestampMs - delta * 1000;
      this.animationFrameId = requestAnimationFrame(stepFn);
    };

    // First call to kick off the loop
    this.animationFrameId = requestAnimationFrame(stepFn);
  }
  drawTitleScreen() {
    this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
    this.ctx.fillStyle = 'white';
    this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
    const myImage = new Image();
    myImage.src = '/characters/choosingPosAlien.png';
    myImage.onload = () => {
      this.ctx.drawImage(
        myImage,
        this.canvas.width - 256,
        this.canvas.height - 256,
        256,
        256
      );
    };
  }
  handleInput(e: KeyboardEvent) {
    // optional split input handling

    if (e.key === 'Enter') {
      ScreenController.showTitle();
    }
  }
  init() {
    this.boundHandleInput = (e: KeyboardEvent) => {
      this.handleInput(e);
    };
    window.addEventListener('keydown', this.boundHandleInput);

    if (this.fontImage.complete) {
      this.drawTitleScreen();
      this.textEffect.init();
      this.startAboutLoop();
    } else {
      this.textEffect.fontImage.onload = () => {
        this.startAboutLoop();
        this.drawTitleScreen();
        this.textEffect.init();
      };
    }
  }

  destroy() {
    this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
    if (this.textCanvas && this.textCanvas.parentNode) {
      this.textCanvas.parentNode.removeChild(this.textCanvas);
    }
    // Remove key listener
    window.removeEventListener('keydown', this.boundHandleInput);
    if (this.animationFrameId !== null) {
      cancelAnimationFrame(this.animationFrameId);
      this.animationFrameId = null;
    }
  }
}
