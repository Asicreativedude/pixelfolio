// src/ScreenController.ts

import CharacterSelection from '../titleScreen/characterSelection';
import TitleScreen from '../titleScreen/TitleScreen';
import World from '../world/defineWorld';

let currentScreen: any = null;

export const ScreenController = {
  element: document.querySelector('.game-container')! as HTMLElement,

  showTitle() {
    currentScreen?.destroy?.();
    currentScreen = new TitleScreen(this.element);
    currentScreen.init();
  },

  showCharacterSelection() {
    currentScreen?.destroy?.();
    currentScreen = new CharacterSelection(this.element);
    currentScreen.init();
  },

  showWorld() {
    currentScreen?.destroy?.();
    currentScreen = new World({ element: this.element });
    currentScreen.init();
  },
};
