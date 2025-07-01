export default class CharacterSelection {
  element: HTMLElement | null;

  constructor() {
    this.element = null;
  }
  createElement() {
    this.element = document.createElement('div');
    this.element.classList.add('CharacterSelection');
    this.element.innerHTML = ` <h1 class="characterSelectionTitle">Choose Your Character  </h1><div class=btn-wrapper><button class="charBtn" id="firstChar" data-button=./characters/chich.png autofocus></button>
    <button class="charBtn" id="secondChar" data-button=./characters/iluz.png></button>
    <button class="charBtn" id="lastChar" data-button=./characters/alien.png></button>`;
  }
  init(container: HTMLElement) {
    this.createElement();
    if (!this.element) {
      throw new Error('Character selection element not created');
    }
    container.appendChild(this.element);
  }
}
