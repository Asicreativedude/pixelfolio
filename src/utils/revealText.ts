// Rveals text one character at a time, with a delay between each character.

export default class RevealingText {
  element: HTMLElement;
  text: string;
  speed: number;
  timeout: number | undefined;
  isDone: boolean;

  constructor(config: { element: HTMLElement; text: string; speed: number }) {
    this.element = config.element;
    this.text = config.text;
    this.speed = config.speed || 80;

    this.timeout = undefined;
    this.isDone = false;
  }
  revealOneCharacter(list: any[]) {
    const next = list.splice(0, 1)[0];
    next.span.classList.add('revealed');

    if (list.length > 0) {
      this.timeout = setTimeout(() => {
        this.revealOneCharacter(list);
      }, next.delayAfter);
    } else {
      this.isDone = true;
    }
  }

  warpToDone() {
    clearTimeout(this.timeout);
    this.isDone = true;
    this.element.querySelectorAll('span').forEach((s) => {
      s.classList.add('revealed');
    });
  }
  init() {
    let characters: { span: HTMLSpanElement; delayAfter: number }[] = [];
    this.text.split('').forEach((character) => {
      //Create each span, add to element in DOM
      let span = document.createElement('span');
      span.textContent = character;
      this.element.appendChild(span);

      //Add this span to our internal state Array
      characters.push({
        span,
        delayAfter: character === ' ' ? 0 : this.speed,
      });
    });

    this.revealOneCharacter(characters);
  }
}
