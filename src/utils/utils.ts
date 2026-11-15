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

  // The point the camera centres on for a map of the given size (px) on a view (the canvas, px). It follows
  // focus but stops at the map's edges; a map smaller than the view on an axis sits centred on that axis.
  // The map is drawn at (withGrid(9.5) - x, withGrid(5) - y), see WorldMap.drawImageLayer.
  cameraFocus(
    focus: { x: number; y: number },
    [w, h]: [number, number],
    [viewW, viewH]: [number, number]
  ) {
    const axis = (at: number, size: number, view: number, offset: number) => {
      const lo = offset; // the map's near edge on the view's
      const hi = size - view + offset; // its far edge on the view's
      return hi < lo
        ? Math.round((lo + hi) / 2)
        : Math.min(Math.max(at, lo), hi);
    };
    return {
      x: axis(focus.x, w, viewW, utils.withGrid(9.5)),
      y: axis(focus.y, h, viewH, utils.withGrid(5)),
    };
  },

  // Which lit sheet a figure at (x, y) takes: the map's light grid, keyed like walls, for the tile the figure
  // is mostly on. 0, the top sheet, where the map has no grid or leaves the tile out.
  lightAt(light: Record<string, number> | undefined, x: number, y: number) {
    const tile = (n: number) => Math.round(n / 32) * 32;
    return light?.[`${tile(x)},${tile(y)}`] ?? 0;
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
