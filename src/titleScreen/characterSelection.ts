import TitleScreenSprite from './TitleScreenSprite';
import utils from '../utils/utils';
import { worldMaps } from '../world/maps';
import World from '../world/defineWorld';

export default class CharacterSelection {
  gameContainer: HTMLElement;
  charachterBG: TitleScreenSprite[];
  canvas: HTMLCanvasElement;
  ctx: CanvasRenderingContext2D;
  selectedChar: number;
  charImages: string[];
  charSprites: string[];

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
      worldMaps.Hall.gameObjects.hero.sprite.image.src =
        worldMaps.ProjectsPage.gameObjects.hero.sprite.image.src =
        worldMaps.OutsideWorld.gameObjects.hero.sprite.image.src =
        worldMaps.AboutPage.gameObjects.hero.sprite.image.src =
        worldMaps.ContactPage.gameObjects.hero.sprite.image.src =
        worldMaps.ThreedWorld.gameObjects.hero.sprite.image.src =
          String(`${this.charSprites[this.selectedChar]}`);
      this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
      this.gameInit(this.gameContainer);
      return;
    }
    this.drawTitleScreen();
  }
  drawTitleScreen() {
    this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
    this.charachterBG.forEach((bg) => {
      bg.draw(this.ctx, bg.x, bg.y);
    });
  }

  gameInit(gameContainer: HTMLElement) {
    const world = new World({
      element: gameContainer,
    });
    world.init();
  }

  init(): void {
    window.addEventListener('keydown', (e) => this.handleInput(e));
    this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
    this.charachterBG.forEach((bg, index) => {
      bg.draw(this.ctx, bg.x, bg.y);
      const charImage = new Image();
      charImage.src = this.charImages[index];
      this.ctx.drawImage(charImage, bg.x, bg.y);
    });
  }
}
