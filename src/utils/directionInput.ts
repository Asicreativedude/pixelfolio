// A utility class in your game that handles keyboard and touch-based directional input.
// It allows both desktop and mobile users to control movement using arrow keys, WASD, or on-screen d-pad buttons.

export default class DirectionInput {
  heldDirections: string[]; // Array to hold currently pressed directions
  map: Record<string, string>; // Mapping of key codes to directions
  mobileDirections: Record<string, string>; // Mapping of mobile d-pad buttons to directions
  isPressed: boolean; // Flag to check if a d-pad button is pressed

  constructor() {
    // An array that stores currently held directions (['up'], ['down'], etc.) — the first item is considered the active direction.
    this.heldDirections = [];

    // define the mapping of keyboard inputs to directions
    this.map = {
      ArrowUp: 'up',
      KeyW: 'up',
      ArrowDown: 'down',
      KeyS: 'down',
      ArrowLeft: 'left',
      KeyA: 'left',
      ArrowRight: 'right',
      KeyD: 'right',
    };

    this.mobileDirections = {
      up: 'up',
      down: 'down',
      left: 'left',
      right: 'right',
    };
    this.isPressed = false;
  }

  // Returns the current input direction, or undefined if none is held.
  // Used by the game engine to determine which direction the player wants to move.

  get direction() {
    return this.heldDirections[0];
  }

  init() {
    // Bind keyboard events to update heldDirections based on key presses.
    document.addEventListener('keydown', (e) => {
      const dir = this.map[e.code];
      if (dir && this.heldDirections.indexOf(dir) === -1) {
        this.heldDirections.unshift(dir);
      }
    });
    document.addEventListener('keyup', (e) => {
      const dir = this.map[e.code];
      const index = this.heldDirections.indexOf(dir);
      if (index > -1) {
        this.heldDirections.splice(index, 1);
      }
    });
    document
      .querySelector('.dpad-button')!
      .addEventListener('contextmenu', (e) => {
        e.preventDefault();
      });
    const removePressedAll = () => {
      document.querySelectorAll('.dpad-button').forEach((d) => {
        d.classList.remove('pressed');
      });
    };

    const handleDpadPress = (mobileDirections: string, click: boolean) => {
      if (click) {
        this.isPressed = true;
      }
      this.heldDirections = this.isPressed ? [mobileDirections] : [];

      if (this.isPressed) {
        removePressedAll();
        document
          .querySelector('.dpad-' + mobileDirections)!
          .classList.add('pressed');
      }
    };
    document.body.addEventListener('mouseup', () => {
      this.isPressed = false;
      this.heldDirections = [];
      removePressedAll();
    });

    //Bind a ton of events for the dpad
    document.querySelector('.dpad-left')!.addEventListener('touchstart', () => {
      handleDpadPress(this.mobileDirections.left, true);
    });

    document
      .querySelector('.dpad-up')!
      .addEventListener('touchstart', () =>
        handleDpadPress(this.mobileDirections.up, true)
      );
    document
      .querySelector('.dpad-right')!
      .addEventListener('touchstart', () =>
        handleDpadPress(this.mobileDirections.right, true)
      );
    document
      .querySelector('.dpad-down')!
      .addEventListener('touchstart', () =>
        handleDpadPress(this.mobileDirections.down, true)
      );
  }
}
