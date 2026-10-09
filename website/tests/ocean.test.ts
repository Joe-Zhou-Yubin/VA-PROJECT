import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { parseVocabulary, createSampler, assertSourceWords } from '../src/vocabulary.ts';
import { addRipple, expireRipples, sampleWater, project, unprojectBase, MAX_RIPPLES, RIPPLE_LIFETIME } from '../src/waves.ts';

const csv = readFileSync(new URL('../../text/EJF/ejf_word_freq.csv', import.meta.url), 'utf8');

test('real source parses and seeded frequency sampling emits only exact source words', () => {
  const entries = parseVocabulary(csv);
  assert.equal(entries.length, 500);
  const allowed = new Set(entries.map(e => e.word));
  const a = createSampler(entries), b = createSampler(entries);
  const words = Array.from({ length: 50000 }, a);
  assertSourceWords(words, allowed);
  assert.deepEqual(words, Array.from({ length: 50000 }, b));
  const squid = words.filter(w => w === 'squid').length;
  const expected = 50000 * entries.find(e => e.word === 'squid')!.count / entries.reduce((sum, e) => sum + e.count, 0);
  assert.ok(Math.abs(squid - expected) < expected * .12, 'frequencies should affect recurrence');
  assert.throws(() => assertSourceWords(['imaginary-water-word'], allowed));
});

test('CSV-aware parsing preserves quoted punctuation and rejects corrupt input', () => {
  assert.deepEqual(parseVocabulary('word,count\n"sea,fish",2\nsquid,3\n'), [{ word: 'sea,fish', count: 2 }, { word: 'squid', count: 3 }]);
  for (const input of ['word,frequency\nsquid,2', 'word,count\nsquid,0', 'word,count\nsquid,NaN', 'word,count\n,2', 'word,count\n']) {
    assert.throws(() => parseVocabulary(input));
  }
});

test('base-plane projection round trips across responsive dimensions', () => {
  for (const width of [390, 768, 1440]) for (const z of [0, 80, 380, 900, 1100]) for (const x of [-800, 0, 800]) {
    const point = project(x, z, 0, width, 300, 600);
    const restored = unprojectBase(point.x, point.y, width, 300, 600);
    assert.ok(Math.abs(restored.x - x) < .00001);
    assert.ok(Math.abs(restored.z - z) < .00001);
  }
});

test('ripples travel, expire and remain bounded during sustained input', () => {
  const ripples: {x: number; z: number; born: number; strength: number}[] = [];
  for (let i = 0; i < 100; i++) addRipple(ripples, { x: 0, z: 400, born: i / 100, strength: 50 });
  assert.equal(ripples.length, MAX_RIPPLES);
  const ripple = [{ x: 0, z: 400, born: 0, strength: 50 }];
  assert.notEqual(sampleWater(130, 400, .5, ripple), sampleWater(130, 400, .5, []));
  assert.equal(sampleWater(130, 400, 5, ripple), sampleWater(130, 400, 5, []));
  expireRipples(ripples, 1 + RIPPLE_LIFETIME);
  assert.equal(ripples.length, 0);
});
