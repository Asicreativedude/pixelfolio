// // Rveals text one character at a time, with a delay between each character.

// export default class RevealingText {
//   element: HTMLElement;
//   text: string;
//   speed: number;
//   timeout: number | undefined;
//   isDone: boolean;

//   constructor(config: { element: HTMLElement; text: string; speed: number }) {
//     this.element = config.element;
//     this.text = config.text;
//     this.speed = config.speed || 80;

//     this.timeout = undefined;
//     this.isDone = false;
//   }
//   revealOneCharacter(list: any[]) {
//     const next = list.splice(0, 1)[0];
//     next.span.classList.add('revealed');

//     if (list.length > 0) {
//       this.timeout = setTimeout(() => {
//         this.revealOneCharacter(list);
//       }, next.delayAfter);
//     } else {
//       this.isDone = true;
//     }
//   }

//   warpToDone() {
//     clearTimeout(this.timeout);
//     this.isDone = true;
//     this.element.querySelectorAll('span').forEach((s) => {
//       s.classList.add('revealed');
//     });
//   }
//   init() {
//     let characters: { span: HTMLSpanElement; delayAfter: number }[] = [];
//     this.text.split('').forEach((character) => {
//       //Create each span, add to element in DOM
//       let span = document.createElement('span');
//       span.textContent = character;
//       this.element.appendChild(span);

//       //Add this span to our internal state Array
//       characters.push({
//         span,
//         delayAfter: character === ' ' ? 0 : this.speed,
//       });
//     });

//     this.revealOneCharacter(characters);
//   }
// }
const CHAR_WIDTH = 16;
const CHAR_HEIGHT = 16;
const CHAR_SPACING = 12;
const CHAR_MAP = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!?@$.,';

export default class RevealingText {
  canvas: HTMLCanvasElement;
  ctx: CanvasRenderingContext2D;
  text: string;
  speed: number;
  timeout: number | undefined;
  isDone: boolean;
  fontImage: HTMLImageElement;

  constructor(config: {
    canvas: HTMLCanvasElement;
    text: string;
    speed?: number;
    fontImage: HTMLImageElement;
  }) {
    this.canvas = config.canvas;
    this.ctx = this.canvas.getContext('2d')!;
    this.text = config.text;
    this.speed = config.speed || 80;
    this.fontImage = config.fontImage;
    this.isDone = false;
  }

  revealOneCharacter(chars: string[], index: number = 0) {
    const char = chars[index];
    const { x, y } = this.getCharCoords(char);

    this.ctx.drawImage(
      this.fontImage,
      x,
      y,
      CHAR_WIDTH,
      CHAR_HEIGHT,
      index * CHAR_SPACING,
      0,
      CHAR_WIDTH,
      CHAR_HEIGHT
    );

    if (index < chars.length - 1) {
      this.timeout = setTimeout(
        () => this.revealOneCharacter(chars, index + 1),
        char === ' ' ? 0 : this.speed
      );
    } else {
      this.isDone = true;
    }
  }

  getCharCoords(char: string) {
    const index = CHAR_MAP.indexOf(char.toUpperCase());
    return {
      x: index * CHAR_WIDTH,
      y: 0,
    };
  }

  warpToDone() {
    clearTimeout(this.timeout);
    this.isDone = true;
    this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
    this.text.split('').forEach((char, i) => {
      const { x, y } = this.getCharCoords(char);
      this.ctx.drawImage(
        this.fontImage,
        x,
        y,
        CHAR_WIDTH,
        CHAR_HEIGHT,
        i * CHAR_SPACING,
        0,
        CHAR_WIDTH,
        CHAR_HEIGHT
      );
    });
  }

  init() {
    this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
    const chars = this.text.split('');
    this.revealOneCharacter(chars);
  }
}
