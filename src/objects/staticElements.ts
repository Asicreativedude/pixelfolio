import type { StaticElementConfig } from '../types';
import GameObject from './gameObject';
import Sprite from '../utils/sprite';

// Collectable class extends gameObject to represent items that can be collected in the game.
// It initializes with a sprite and has logic to update its appearance based on whether it has been used or not.

export default class StaticElement extends GameObject {
  animationSchedule?: {
    primary: string;
    alternate: string;
    interval: number; // in ms
    lastSwitch?: number;
    isInAlternate?: boolean;
  };

  constructor(config: StaticElementConfig) {
    super(config);

    this.sprite = new Sprite({
      gameObject: this,
      src: config.src,
      frameWidth: config.frameWidth,
      frameHeight: config.frameHeight,
      animations: config.animations,
      animationSchedule: config.animationSchedule,
    });
  }

  update() {
    this.sprite.updateAnimationProgress();
  }
}
