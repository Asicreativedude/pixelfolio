import type { SpriteConfig } from '../types';
import utils from './utils';

// Load a sprite sheet (image)
// Optionally load and draw a shadow
// Define and manage animations (walking, idling, etc.)
// Draw the correct frame at the correct screen position, adjusted for the camera

export default class Sprite {
  image: HTMLImageElement; // The sprite sheet image
  shadow: HTMLImageElement; // The shadow image
  useShadow: boolean; // Whether to use the shadow
  isLoaded: boolean = false; // Whether the sprite image is loaded
  isShadowLoaded: boolean = false; // Whether the shadow image is loaded
  animations: { [key: string]: number[][] }; // Animation frames for each state
  currentAnimation: string; // The current animation state
  currentAnimationFrame: number; // The current frame in the animation
  animationFrameLimit: number; // How many ticks before changing the animation frame
  animationFrameProgress: number; // Progress towards the next animation frame
  gameObject: any; // Reference to the game object this sprite belongs to

  constructor(config: SpriteConfig) {
    //Setup the image

    this.image = new Image();
    this.image.src = config.src;
    this.image.onload = () => {
      this.isLoaded = true;
    };

    //shadow
    this.shadow = new Image();
    this.useShadow = config.useShadow || false;

    if (this.useShadow) {
      this.shadow.src = '/images/shadow-demo.png';
    }
    this.shadow.onload = () => {
      this.isShadowLoaded = true;
    };

    // Defines a list of frame coordinates ([column, row]) for each animation state.
    // Defaults to idle-up.

    this.animations = config.animations || {
      'idle-down': [[0, 0]],
      'idle-up': [[0, 3]],
      'idle-left': [[0, 1]],
      'idle-right': [[0, 2]],
      'walk-down': [
        [1, 0],
        [0, 0],
        [2, 0],
        [0, 0],
      ],
      'walk-up': [
        [1, 3],
        [0, 3],
        [2, 3],
        [0, 3],
      ],
      'walk-left': [
        [1, 1],
        [0, 1],
        [2, 1],
        [0, 1],
      ],
      'walk-right': [
        [1, 2],
        [0, 2],
        [2, 2],
        [0, 2],
      ],
    };
    this.currentAnimation = config.currentAnimation || 'idle-up';
    this.currentAnimationFrame = 0;

    // Animation frame progress controls how fast the animation changes frames.

    this.animationFrameLimit = config.animationFrameLimit || 8;
    this.animationFrameProgress = this.animationFrameLimit;

    //Refrence the game object
    this.gameObject = config.gameObject;
  }

  // Returns the current frame of the current animation.
  get frame() {
    return this.animations[this.currentAnimation][this.currentAnimationFrame];
  }
  // Sets the current animation to a new key.
  setAnimation(key: string) {
    if (this.currentAnimation !== key) {
      this.currentAnimation = key;
      this.currentAnimationFrame = 0;
      this.animationFrameProgress = this.animationFrameLimit;
    }
  }
  // Slowly progresses to the next frame every animationFrameLimit ticks.
  // Loops animation if it reaches the end.
  updateAnimationProgress() {
    //Downtick frame progress
    if (this.animationFrameProgress > 0) {
      this.animationFrameProgress -= 1;
      return;
    }

    //Reset the counter
    this.animationFrameProgress = this.animationFrameLimit;
    this.currentAnimationFrame += 1;

    if (this.frame === undefined) {
      this.currentAnimationFrame = 0;
    }
  }

  // Computes the draw position by offsetting relative to the camera.
  // Draws shadow first (if loaded), then the correct sprite frame.
  // Calls updateAnimationProgress() to advance the animation.

  draw(ctx: CanvasRenderingContext2D, cameraPerson: { x: number; y: number }) {
    const x = this.gameObject.x + utils.withGrid(9.5) - cameraPerson.x;
    const y = this.gameObject.y + utils.withGrid(6) - cameraPerson.y;
    this.isShadowLoaded && ctx.drawImage(this.shadow, x - 4, y - 2);
    const [frameX, frameY] = this.frame;
    this.isLoaded &&
      ctx.drawImage(this.image, frameX * 64, frameY * 64, 64, 64, x, y, 64, 64);
    this.updateAnimationProgress();
  }
}
