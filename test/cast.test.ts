// The cast's lit sheets (art/cast.py, public/cast/<name>.png) against the rooms' light grids: Sprite.draw falls back
// to the top sheet when an image has fewer sheets than a tile asks for, so a short sheet fails quietly in the game.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';

const file = (path: string) => new URL(`../public/${path}`, import.meta.url);
const size = (png: Buffer) => [png.readUInt32BE(16), png.readUInt32BE(20)]; // IHDR width, height

const asked = Math.max(
  ...['studio', 'hall'].flatMap((name) => {
    const { light } = JSON.parse(readFileSync(file(`rooms/${name}.json`), 'utf8'));
    return Object.values(light).flatMap((grid) => Object.values(grid as Record<string, number>));
  })
);

for (const name of ['hero', 'saruli', 'chich', 'iluz', 'alien'])
  test(`cast/${name}.png has a sheet for every light the rooms ask for`, () => {
    const [w, h] = size(readFileSync(file(`cast/${name}.png`)));
    assert.equal(w, 256);
    assert.equal(h % 256, 0);
    assert.ok(h / 256 > asked, `${h / 256} sheets, the rooms ask for sheet ${asked}`);
  });
