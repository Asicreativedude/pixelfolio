const utils = {
  // Converts a grid index to pixel units.
  // Since each tile is 32×32 pixels, withGrid(5) returns 160, which is 5 tiles over.
  withGrid(n: number) {
    return n * 32;
  },

  // Converts tile coordinates into a string-based pixel position like "64,96".
  // Useful for keys in maps (e.g., for walls or cutscene triggers).

  asGridCoord(x: number, y: number) {
    return `${x * 32},${y * 32}`;
  },

  // Given a direction ('up', 'down', etc.), returns the next pixel-based position on the map.
  // Moves exactly 1 tile (32 pixels) in the specified direction.

  nextPosition(initialX: number, initialY: number, direction: string) {
    let x = initialX;
    let y = initialY;
    const size = 32;
    if (direction === 'left') {
      x -= size;
    } else if (direction === 'right') {
      x += size;
    } else if (direction === 'up') {
      y -= size;
    } else if (direction === 'down') {
      y += size;
    }
    return { x, y };
  },

  // Returns the reverse of a given direction string.
  // Example: 'left' → 'right', 'up' → 'down'

  oppositeDirection(direction: string) {
    if (direction === 'left') {
      return 'right';
    }
    if (direction === 'right') {
      return 'left';
    }
    if (direction === 'up') {
      return 'down';
    }
    return 'up';
  },

  // Simple async sleep function.
  // Used in cutscenes or behavior loops to pause for dramatic effect or simulate wait time.

  wait(ms: number) {
    return new Promise<void>((resolve) => {
      setTimeout(() => {
        resolve();
      }, ms);
    });
  },

  // Emits a custom DOM event globally with optional details.
  // Used for things like:
  // - Emitting 'PersonWalkingComplete'
  // - Signaling the UI to update
  // - Communicating between components (non-reactively)

  emitEvent(name: string, detail: any = {}) {
    const event = new CustomEvent(name, {
      detail,
    });
    document.dispatchEvent(event);
  },
};
export default utils;
