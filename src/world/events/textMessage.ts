import RevealingText from '../../utils/revealText';
import KeyPressListener from '../../utils/keyPressListener';

// const mButtons = document.querySelector(
//   '.mobileButtons-container'
// ) as HTMLElement;

export default class TextMessage {
  text: string;
  onComplete: () => void;
  element: HTMLElement | null;
  revealingText: RevealingText;
  actionListener: KeyPressListener;

  constructor({ text, onComplete }: { text: string; onComplete: () => void }) {
    this.text = text;
    this.onComplete = onComplete;
    this.element = null;
    this.revealingText = null as any;
    this.actionListener = null as any;
  }

  createElement() {
    const fontImage = new Image();
    fontImage.src = '/Letters.png';

    this.element = document.createElement('div');
    this.element.classList.add('TextMessage');

    const canvas = document.createElement('canvas');
    canvas.width = 500;
    canvas.height = 48;
    canvas.classList.add('TextMessage_canvas');
    this.element.appendChild(canvas);

    const button = document.createElement('button');
    button.classList.add('TextMessage_button');
    button.textContent = 'Next';
    this.element.appendChild(button);

    // Wait until font image is loaded
    fontImage.onload = () => {
      this.revealingText = new RevealingText({
        canvas,
        text: this.text,
        speed: 80,
        fontImage,
      });
      this.revealingText.init(); // Only initialize when image is ready
    };

    button.addEventListener('click', () => {
      this.done();
    });

    this.actionListener = new KeyPressListener('Enter', () => {
      this.done();
    });
  }

  done() {
    if (this.revealingText.isDone && this.element) {
      // if (mButtons!.style.display != 'flex') {
      //   mButtons!.classList.add('fade-in');
      // }
      this.element.remove();
      this.actionListener.unbind();
      this.onComplete();
    } else {
      this.revealingText.warpToDone();
    }
  }

  init(container: HTMLElement) {
    this.createElement();
    container.appendChild(this.element!);
  }
}
