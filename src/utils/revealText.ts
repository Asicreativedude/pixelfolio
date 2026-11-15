const CHAR_WIDTH = 16;
const CHAR_HEIGHT = 16;
const CHAR_SPACING = 11;
const LINE_HEIGHT = 32;
const CHAR_MAP = "ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!?@$.,'";
const LINEMARGIN = 8;

export default class RevealingText {
  canvas: HTMLCanvasElement;
  ctx: CanvasRenderingContext2D;
  text: string;
  speed: number;
  timeout: number | undefined;
  isDone: boolean;
  fontImage: HTMLImageElement;
  currentX: number = LINEMARGIN * 2;
  currentY: number = 0;
  maxWidth: number;
  lineHeight: number = LINE_HEIGHT;
  distanceFromTop: number;
  instant = false;

  constructor(config: {
    canvas: HTMLCanvasElement;
    text: string;
    speed?: number;
    fontImage: HTMLImageElement;
    distanceFromTop?: number;
  }) {
    this.canvas = config.canvas;
    this.ctx = this.canvas.getContext('2d')!;
    this.text = config.text;
    this.speed = config.speed || 80;
    this.fontImage = config.fontImage;
    this.isDone = false;
    this.maxWidth = this.canvas.width - LINEMARGIN * 2;
    this.currentX = LINEMARGIN * 2;
    this.distanceFromTop = config.distanceFromTop || LINEMARGIN;
  }

  revealOneCharacter(
    words: string[],
    wordIndex: number = 0,
    charIndex: number = 0
  ) {
    const next = (w: number, c: number, ms: number) => {
      if (this.instant) this.revealOneCharacter(words, w, c);
      else this.timeout = setTimeout(() => this.revealOneCharacter(words, w, c), ms);
    };
    if (wordIndex >= words.length) {
      this.isDone = true;
      return;
    }

    const word = words[wordIndex];
    const wordPixelLength = word.length * CHAR_SPACING;

    // If the word can't fit on the current line, move to next line first
    if (
      charIndex === 0 &&
      this.currentX + wordPixelLength > this.canvas.width - LINEMARGIN
    ) {
      this.currentX = LINEMARGIN;
      this.currentY += this.lineHeight;

      // Prevent leading space on new line
      if (word[0] === ' ') {
        next(wordIndex + 1, 0, this.speed);
        return;
      }
    }

    const char = word[charIndex];
    const { x, y } = this.getCharCoords(char);

    this.ctx.drawImage(
      this.fontImage,
      x,
      y,
      CHAR_WIDTH,
      CHAR_HEIGHT,
      this.currentX,
      this.currentY,
      CHAR_WIDTH,
      CHAR_HEIGHT
    );

    this.currentX += CHAR_SPACING;

    if (charIndex < word.length - 1) {
      next(wordIndex, charIndex + 1, char === ' ' ? 0 : this.speed);
    } else {
      // Add space after word
      this.currentX += 8;
      next(wordIndex + 1, 0, this.speed);
    }
  }

  getCharCoords(char: string) {
    const index = CHAR_MAP.indexOf(char.toUpperCase());
    return {
      x: index * CHAR_WIDTH,
      y: 0,
    };
  }

  // Skipping ahead redraws through revealOneCharacter with no delays, so the text lands where the reveal puts it.
  warpToDone() {
    clearTimeout(this.timeout);
    this.instant = true;
    this.init();
  }

  init() {
    this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
    this.currentX = LINEMARGIN;
    this.currentY = this.distanceFromTop;
    const words = this.text.split(' ');
    this.revealOneCharacter(words);
  }
}
