import type { TitleSpriteConfig } from '../types';

// Load a sprite sheet (image)
// Optionally load and draw a shadow
// Define and manage animations (walking, idling, etc.)
// Draw the correct frame at the correct screen position, adjusted for the camera

type AnimationObj = {
  frames: [number, number][];
  frameLimit?: number;
  frameHoldTicks?: number;
};

export default class TitleScreenSprite {
  x: number;
  y: number;
  image: HTMLImageElement; // The sprite sheet image
  isLoaded: boolean = false; // Whether the sprite image is loaded
  animations: { [key: string]: AnimationObj }; // Animation frames for each state
  currentAnimation: string; // The current animation state
  frameIndex: number; // The current frame in the animation
  frameProgress: number; // Progress towards the next animation frame
  frameWidth: number;
  frameHeight: number;
  feetOffsetY: number;
  animationSchedule?: {
    primary: string;
    alternate: string;
    interval: number; // in ms
    lastSwitch?: number;
    isInAlternate?: boolean;
  };

  constructor(config: TitleSpriteConfig) {
    //Setup the image
    this.x = config.x;
    this.y = config.y;
    this.image = new Image();
    this.image.src = config.src;
    this.image.onload = () => {
      this.isLoaded = true;
    };
    // Enhanced: normalize animations to objects with frames, frameLimit, etc
    // Accept both new (AnimationObj) and old ([[number, number], ...]) animation formats
    this.animations = {};
    const animations = config.animations || {};

    for (const key in animations) {
      const anim = animations[key];
      if (Array.isArray(anim)) {
        this.animations[key] = { frames: anim };
      } else {
        this.animations[key] = anim;
      }
    }
    this.currentAnimation =
      config.currentAnimation || Object.keys(this.animations)[0];
    this.frameIndex = 0;
    const initialAnim = this.animations[this.currentAnimation];
    const frameLimit = initialAnim?.frameLimit || 8;
    this.frameProgress = frameLimit;

    this.frameWidth = config.frameWidth || 64;
    this.frameHeight = config.frameHeight || 64;
    this.feetOffsetY = config.feetOffsetY ?? this.frameHeight;

    // Optionally copy animationSchedule from config
    if (config.animationSchedule) {
      this.animationSchedule = { ...config.animationSchedule };
    }
  }

  // Returns the current frame of the current animation.
  get frame() {
    return this.animations[this.currentAnimation].frames[this.frameIndex];
  }

  // Sets the current animation to a new key.
  setAnimation(key: string) {
    if (this.currentAnimation !== key) {
      this.currentAnimation = key;
      this.frameIndex = 0;
      const anim = this.animations[this.currentAnimation];
      const frameLimit = anim.frameLimit || 8;
      this.frameProgress = frameLimit;
    }
  }

  // Animation update with frameLimit support per animation
  updateAnimationProgress() {
    const animation = this.animations[this.currentAnimation];
    if (!animation) return;

    const frameLimit = animation.frameLimit || 8;
    this.frameProgress = (this.frameProgress || frameLimit) - 1;
    if (this.frameProgress > 0) return;

    this.frameProgress = frameLimit;
    this.frameIndex++;
    const isLastFrame = this.frameIndex >= animation.frames.length;
    if (isLastFrame) {
      this.frameIndex = 0;

      // 🔁 Handle scheduled alternates
      if (
        this.animationSchedule &&
        this.currentAnimation === this.animationSchedule.alternate
      ) {
        // If switching back to primary, always reset frameIndex and schedule state.
        if (this.currentAnimation !== this.animationSchedule.primary) {
          this.currentAnimation = this.animationSchedule.primary;
          this.frameIndex = 0;
          this.animationSchedule.isInAlternate = false;
          this.animationSchedule.lastSwitch = Date.now();
        } else {
          this.currentAnimation = this.animationSchedule.primary;
          this.animationSchedule.isInAlternate = false;
          this.animationSchedule.lastSwitch = Date.now(); // reset after alternate finishes
        }
      }
    }
  }

  // Switches animation on a schedule between primary and alternate
  updateScheduledAnimation() {
    if (!this.animationSchedule) return;

    const now = Date.now();
    const { lastSwitch = 0, interval, isInAlternate } = this.animationSchedule;

    // Only trigger alternate if not already in it, and time has passed
    if (!isInAlternate && now - lastSwitch >= interval) {
      this.currentAnimation = this.animationSchedule.alternate;
      this.frameIndex = 0;
      this.animationSchedule.isInAlternate = true;
      // Do not set lastSwitch yet
    }
  }

  // Computes the draw position by offsetting relative to the camera.
  // Draws shadow first (if loaded), then the correct sprite frame.
  // Calls updateScheduledAnimation and updateAnimationProgress to advance the animation.
  draw(ctx: CanvasRenderingContext2D, x: number, y: number) {
    // Center the sprite within its tile by offsetting by half the frame size
    const animation = this.animations[this.currentAnimation];
    if (!animation) {
      this.isLoaded && ctx.drawImage(this.image, x, y);
      return;
    }
    const [frameX, frameY] = animation.frames[this.frameIndex];

    this.isLoaded &&
      ctx.drawImage(
        this.image,
        frameX * this.frameWidth,
        frameY * this.frameHeight,
        this.frameWidth,
        this.frameHeight,
        x,
        y,
        this.frameWidth,
        this.frameHeight
      );
    this.updateScheduledAnimation();
    this.updateAnimationProgress();
  }
}
