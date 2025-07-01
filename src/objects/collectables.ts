import type { CollectableConfig } from '../types';
import GameObject from './gameObject';
import Sprite from '../utils/sprite';

// Collectable class extends gameObject to represent items that can be collected in the game.
// It initializes with a sprite and has logic to update its appearance based on whether it has been used or not.

export default class Collectable extends GameObject {
  useShadow: boolean; // Whether the collectable uses a shadow
  isUsed: boolean; // Whether the collectable has been used

  constructor(config: CollectableConfig) {
    super(config);
    this.sprite = new Sprite({
      gameObject: this,
      src: '/images/shroom-test.png',
      animations: {
        'not-used': [[0, 0]],
        'used-shroom': [[1, 0]],
      },
      currentAnimation: 'not-used',
      useShadow: false,
    });
    this.useShadow = config.useShadow || false;
    this.isUsed = config.isUsed || false;
  }

  update() {
    this.sprite.currentAnimation = this.isUsed ? 'used-shroom' : 'not-used';
    this.sprite.useShadow = false;
  }
}
