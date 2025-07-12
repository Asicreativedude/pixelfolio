import TitleScreenSprite from './TitleScreenSprite';
import utils from '../utils/utils';
import { heroInitialState } from '../world/maps';
import { ScreenController } from '../utils/screenContorller';
import { getPlayerData, setPlayerData } from '../utils/progressTracker';

export default class CharacterSelection {
  gameContainer: HTMLElement;
  charachterBG: TitleScreenSprite[];
  canvas: HTMLCanvasElement;
  ctx: CanvasRenderingContext2D;
  selectedChar: number;
  charImages: string[];
  charSprites: string[];
  boundHandleInput!: (e: KeyboardEvent) => void;
  preloadedImages: HTMLImageElement[] = [];

  constructor(gameContainer: HTMLElement) {
    this.gameContainer = gameContainer;
    this.selectedChar = 0;
    this.canvas = gameContainer.querySelector('canvas')!;
    this.ctx = this.canvas.getContext('2d')!;
    this.charachterBG = [
      new TitleScreenSprite({
        x: utils.withGrid(0),
        y: utils.withGrid(2),
        src: '../../charachterSelectBG.png',
        frameWidth: 225,
        frameHeight: 225,
        animations: {
          charBG: { frames: [[1, 0]] },
        },
      }),
      new TitleScreenSprite({
        x: utils.withGrid(6.5),
        y: utils.withGrid(2),
        src: '../../charachterSelectBG.png',
        frameWidth: 225,
        frameHeight: 225,
        animations: {
          charBG: { frames: [[0, 0]] },
        },
      }),
      new TitleScreenSprite({
        x: utils.withGrid(13),
        y: utils.withGrid(2),
        src: '../../charachterSelectBG.png',
        frameWidth: 225,
        frameHeight: 225,
        animations: {
          charBG: { frames: [[0, 0]] },
        },
      }),
    ];
    this.charImages = [
      '/characters/choosingPosIluz.png',
      '/characters/choosingPos.png',
      '/characters/choosingPosAlien.png',
    ];
    this.charSprites = [
      '/characters/iluz.png',
      '/characters/chich.png',
      '/characters/saruli.png',
    ];
  }
  handleInput(e: KeyboardEvent) {
    // optional split input handling
    if (e.key === 'ArrowRight') {
      this.selectedChar = (this.selectedChar + 1) % this.charachterBG.length;
      this.charachterBG.forEach((bg, index) => {
        index === this.selectedChar
          ? (bg.animations.charBG.frames = [[1, 0]])
          : (bg.animations.charBG.frames = [[0, 0]]);
      });
    } else if (e.key === 'ArrowLeft') {
      this.selectedChar =
        (this.selectedChar - 1 + this.charachterBG.length) %
        this.charachterBG.length;
      this.charachterBG.forEach((bg, index) => {
        index === this.selectedChar
          ? (bg.animations.charBG.frames = [[1, 0]])
          : (bg.animations.charBG.frames = [[0, 0]]);
      });
    } else if (e.key === 'Enter') {
      heroInitialState.src = String(`${this.charSprites[this.selectedChar]}`);
      const player = getPlayerData();
      player.selectedCharacter = this.charSprites[this.selectedChar];
      player.isFirst = false;
      setPlayerData(player);
      this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
      ScreenController.showWorld();
      return;
    }
    this.drawTitleScreen();
  }
  drawTitleScreen() {
    this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
    this.charachterBG.forEach((bg, index) => {
      bg.draw(this.ctx, bg.x, bg.y);
      const charImage = this.preloadedImages[index];

      if (charImage.complete) {
        this.ctx.drawImage(charImage, bg.x, bg.y);
      }
    });
  }

  init(): void {
    this.boundHandleInput = this.handleInput.bind(this);
    window.addEventListener('keydown', this.boundHandleInput);

    const promises = this.charImages.map((src, index) => {
      return new Promise<void>((resolve) => {
        const img = new Image();
        img.src = src;
        img.onload = () => resolve();
        this.preloadedImages[index] = img;
      });
    });

    Promise.all(promises).then(() => {
      this.drawTitleScreen();
    });
  }

  destroy(): void {
    if (this.boundHandleInput) {
      window.removeEventListener('keydown', this.boundHandleInput);
    }
    this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
  }
}
