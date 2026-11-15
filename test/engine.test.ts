// node --test test/*.test.ts (npm test). Plain Node: no DOM, so only the engine's pure helpers are here.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import utils from '../src/utils/utils.ts';

const view: [number, number] = [640, 360];

test('camera follows the hero in the middle of a large room', () => {
  assert.deepEqual(utils.cameraFocus({ x: 448, y: 256 }, [896, 512], view), {
    x: 448,
    y: 256,
  });
});

test('camera stops at the edges of a large room', () => {
  // the room is drawn at (304 - x, 160 - y): x 304 puts its left edge on the screen's, x 560 its right
  assert.deepEqual(utils.cameraFocus({ x: 32, y: 0 }, [896, 512], view), {
    x: 304,
    y: 160,
  });
  assert.deepEqual(utils.cameraFocus({ x: 864, y: 480 }, [896, 512], view), {
    x: 560,
    y: 312,
  });
});

test('a room smaller than the screen sits centred on it', () => {
  // 352 x 240: left edge at 304 - 160 = 144 = (640 - 352) / 2, top at 160 - 100 = 60 = (360 - 240) / 2
  assert.deepEqual(utils.cameraFocus({ x: 32, y: 32 }, [352, 240], view), {
    x: 160,
    y: 100,
  });
});

test('a figure takes the lit sheet of the tile under it', () => {
  const light = { '64,96': 3, '96,96': 5 };
  assert.equal(utils.lightAt(light, 64, 96), 3);
  assert.equal(utils.lightAt(light, 78, 96), 3); // walking, under half a tile across
  assert.equal(utils.lightAt(light, 82, 96), 5); // past half way
  assert.equal(utils.lightAt(light, 32, 96), 0); // a tile the map does not light
  assert.equal(utils.lightAt(undefined, 64, 96), 0); // a map with no light grid (the Hall)
});
