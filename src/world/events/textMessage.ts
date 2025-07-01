import RevealingText from '../../utils/revealText';
import KeyPressListener from '../../utils/keyPressListener';

const mButtons = document.querySelector(
  '.mobileButtons-container'
) as HTMLElement;

export default class TextMessage {
  text: string;
  onComplete: () => void;
  element: HTMLElement | null;
  revealingText: RevealingText;
  actionListener: KeyPressListener;

  constructor({ text, onComplete }) {
    this.text = text;
    this.onComplete = onComplete;
    this.element = null;
  }

  createElement() {
    //Create the Element

    this.element = document.createElement('div');
    this.element.classList.add('TextMessage');

    this.element.innerHTML = `<p class="TextMessage_p"></p>
    <button class="TextMessage_button">Next</button>`;

    //Init the typewriter effect
    this.revealingText = new RevealingText({
      element: this.element.querySelector('.TextMessage_p')!,
      text: this.text,
      speed: 80,
    });

    this.element.querySelector('button')!.addEventListener('click', () => {
      //Close the text message
      this.done();
    });

    this.actionListener = new KeyPressListener('Enter', () => {
      this.done();
    });
  }

  done() {
    if (this.revealingText.isDone && this.element) {
      if (mButtons!.style.display != 'flex') {
        mButtons!.classList.add('fade-in');
      }
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
    this.revealingText.init();
  }
}
