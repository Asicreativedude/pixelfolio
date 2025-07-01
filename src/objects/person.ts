import GameObjects from './gameObject';
import utils from '../utils/utils';
import type { PersonConfig } from '../types';

export default class Person extends GameObjects {
  // Inherits from gameObject and adds:

  movingProgressRemaining: number; // How many pixels left to move during a walk
  isStanding: boolean; // Whether the object is currently standing (idle)
  isWalking: boolean; // Whether the object is currently walking
  isPlayerControlled: boolean; // Whether the object is controlled by the player
  directionUpdate: { [key: string]: ['x' | 'y', number] }; // Maps directions to positional axis updates
  // Holds the timeout ID for standing behavior
  standBehaviorTimeout: ReturnType<typeof setTimeout> | undefined;

  constructor(config: PersonConfig) {
    super(config);
    this.movingProgressRemaining = 0;
    this.isStanding = false;
    this.isWalking = false;
    this.isPlayerControlled = config.isPlayerControlled || false;
    this.directionUpdate = {
      up: ['y', -2],
      down: ['y', 2],
      left: ['x', -2],
      right: ['x', 2],
    };
    this.standBehaviorTimeout;
  }

  // Called each frame to update this character’s state:
  // - If the character is currently walking, it continues animating the position via updatePosition().
  // - Otherwise, if:
  // - the game is not in a cutscene
  // - the character is player-controlled
  // - an arrow key is being pressed (state.arrow)

  update(state?: any) {
    if (this.movingProgressRemaining > 0) {
      this.updatePosition();
    } else {
      //more cases for starting to walk

      // case: keyboard ready and have an arrow pressed
      if (
        !state.map.isCutscenePlaying &&
        this.isPlayerControlled &&
        state.arrow
      ) {
        this.startBehavior(state, {
          type: 'walk',
          direction: state.arrow,
        });
      }
      this.updateSprite();
    }
  }

  // Starts a behavior based on the provided config:
  // { type: 'walk', direction: 'left' }
  // { type: 'stand', direction: 'down', time: 1000 }

  startBehavior(
    state: any,
    behavior: {
      type: string;
      direction: string;
      time?: number;
      retry?: boolean;
    }
  ) {
    //Set character direction to whatever behavior has
    this.direction = behavior.direction;

    if (behavior.type === 'walk' && this.isWalking === false) {
      //Stop here if space is not free
      if (state.map.isSpaceTaken(this.x, this.y, this.direction)) {
        behavior.retry &&
          setTimeout(() => {
            this.startBehavior(state, behavior);
          }, 10);

        return;
      }

      //Ready to walk!

      this.isWalking = true;
      state.map.moveWall(this.x, this.y, this.direction);
      this.movingProgressRemaining = 16;
      this.updateSprite();
    }

    if (behavior.type === 'stand') {
      this.isStanding = true;
      this.standBehaviorTimeout = setTimeout(() => {
        utils.emitEvent('PersonStandComplete', {
          whoId: this.id,
        });
        this.isStanding = false;
      }, behavior.time);
    }
  }

  // Executes 1 step of a walk animation

  updatePosition() {
    const [property, change] = this.directionUpdate[this.direction];
    (this as any)[property] += change; // Explicitly cast to 'any' to allow dynamic property access
    this.movingProgressRemaining -= 1;

    if (this.movingProgressRemaining === 0) {
      //We finished the walk!
      utils.emitEvent('PersonWalkingComplete', {
        whoId: this.id,
      });
      this.isWalking = false;
    }
  }

  // Sets the correct animation based on the direction and movement state:
  // - If moving: walk-left, walk-down, etc.
  // - If idle: idle-up, idle-right, etc.

  updateSprite() {
    if (this.movingProgressRemaining > 0) {
      this.sprite.setAnimation('walk-' + this.direction);
      return;
    }
    this.sprite.setAnimation('idle-' + this.direction);
  }
}
