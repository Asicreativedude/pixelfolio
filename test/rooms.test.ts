// The rooms art/room.py exports (public/rooms/<name>.json), checked the way the game walks them: a figure moves
// a tile at a time and stops only on a key in walls, so a tile off the map that walls leaves out is walkable.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';

type Room = { size: number[]; walls: string[]; spots: Record<string, number[] | number[][]> };
const load = (name: string): Room =>
  JSON.parse(readFileSync(new URL(`../public/rooms/${name}.json`, import.meta.url), 'utf8'));

const key = ([c, r]: number[]) => `${(c + 1) * 32},${(r - 1) * 32}`; // the game's key for tile (col, row)
const tiles = (at: number[] | number[][]) => (Array.isArray(at[0]) ? (at as number[][]) : [at as number[]]);
const steps = ([c, r]: number[]) => [[c + 1, r], [c - 1, r], [c, r + 1], [c, r - 1]];

for (const name of ['studio', 'hall']) {
  const room = load(name);
  const walls = new Set(room.walls);
  const [cols, rows] = room.size.map((n) => n / 32);
  const onMap = ([c, r]: number[]) => c >= 0 && r >= 0 && c < cols && r < rows;

  test(`${name}: nothing walks off the map`, () => {
    const out = [];
    for (let r = 0; r < rows; r++)
      for (let c = 0; c < cols; c++)
        if (!walls.has(key([c, r])))
          out.push(...steps([c, r]).filter((t) => !onMap(t) && !walls.has(key(t))));
    assert.deepEqual(out, []);
  });

  test(`${name}: every spot can be walked to from the hero's`, () => {
    const seen = new Set([key(tiles(room.spots.hero)[0])]);
    const todo = [tiles(room.spots.hero)[0]];
    while (todo.length)
      for (const t of steps(todo.pop()!))
        if (onMap(t) && !walls.has(key(t)) && !seen.has(key(t))) seen.add(key(t)), todo.push(t);
    const all = Object.entries(room.spots).flatMap(([who, at]) => tiles(at).map((t) => [who, key(t)]));
    assert.deepEqual(all.filter(([, k]) => !seen.has(k)), []);
  });
}

test('the hall keeps its layout: the four doorways, and where its cast stands', () => {
  const { size, spots } = load('hall');
  assert.deepEqual(size, [1280, 736]);
  const span = (a: number, b: number, at: (i: number) => number[]) =>
    Array.from({ length: b - a + 1 }, (_, i) => at(a + i));
  assert.deepEqual(spots.doorTop, span(18, 21, (c) => [c, 0]));
  assert.deepEqual(spots.doorBottom, span(18, 21, (c) => [c, 22]));
  assert.deepEqual(spots.doorLeft, span(14, 17, (r) => [0, r]));
  assert.deepEqual(spots.doorRight, span(3, 6, (r) => [39, r]));
  // the old Hall's maps.ts placed these in game px; the tile is (x / 32 - 1, y / 32 + 1)
  assert.deepEqual(spots.hero, [9, 7]);
  assert.deepEqual(spots.npcA, [23, 10]);
  assert.deepEqual(spots.npcB, [2, 4]);
  assert.deepEqual(spots.npcC, span(4, 9, (c) => [c, 15])); // its walk, there and back
  assert.deepEqual(spots.hologram, [19, 10]);
});
