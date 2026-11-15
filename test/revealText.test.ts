// RevealingText with a fake canvas that records where each letter lands.
import { test, mock } from 'node:test';
import assert from 'node:assert/strict';
import RevealingText from '../src/utils/revealText.ts';

function letters(skip: boolean) {
  const drawn: number[][] = [];
  const ctx = { filter: 'none', clearRect: () => (drawn.length = 0), drawImage: (...a: number[]) => drawn.push(a.slice(1)) };
  const canvas = { width: 500, height: 48, getContext: () => ctx } as unknown as HTMLCanvasElement;
  const text = new RevealingText({ canvas, text: 'Hello there, this line is long enough to wrap onto a second', fontImage: {} as HTMLImageElement });
  mock.timers.enable({ apis: ['setTimeout'] });
  text.init();
  const wait = (ms: number) => { for (let t = 0; t < ms; t += 10) mock.timers.tick(10); }; // a timer set during a tick waits for the next
  wait(400);
  if (skip) text.warpToDone();
  wait(10_000);
  mock.timers.reset();
  return { drawn, filter: ctx.filter, done: text.isDone };
}

test('pressing Enter mid-reveal shows the text where the reveal would have put it', () => {
  const revealed = letters(false);
  const skipped = letters(true);
  assert.ok(revealed.done && skipped.done);
  assert.deepEqual(skipped.drawn, revealed.drawn);
  assert.equal(skipped.filter, 'none');
});
