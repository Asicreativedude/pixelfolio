// Handles the transition effect between scenes
export default class SceneTransition {
  element: HTMLElement | null;

  constructor() {
    this.element = null;
  }
  createElement() {
    this.element = document.createElement('div');
    this.element.classList.add('SceneTransition');
  }
  fadeout() {
    if (!this.element) {
      throw new Error('Element not created. Call createElement() first.');
    }

    this.element.classList.add('fade-out');
    this.element.addEventListener(
      'animationend',
      () => {
        this.element!.remove();
      },
      { once: true }
    );
  }

  init(container: HTMLElement, callback: () => void) {
    this.createElement();
    container.appendChild(this.element!);

    this.element!.addEventListener(
      'animationend',
      () => {
        callback();
      },
      { once: true }
    );
  }
}
