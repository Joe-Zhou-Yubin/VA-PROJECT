import { prepareWithSegments, layoutWithLines } from '@chenglou/pretext';
import { assertSourceWords, createSampler, type Entry } from './vocabulary';
import { depthScale } from './waves';
import { scene } from './config';

export interface Anchor { word: string; x: number; width: number }
export interface Row { z: number; anchors: Anchor[] }

export function createTextLayout(entries: Entry[], ctx: CanvasRenderingContext2D) {
  const allowed = new Set(entries.map(e => e.word));
  const sample = createSampler(entries, scene.seed);
  const text = Array.from({ length: 900 }, sample).join(' ');
  const prepared = prepareWithSegments(text, scene.font);
  const metrics = new Map<string, number>();
  ctx.font = scene.font;
  const space = ctx.measureText(' ').width;
  for (const { word } of entries) metrics.set(word, ctx.measureText(word).width);
  // The handle and word advances survive resizes. Pretext repacks only on resize/quality changes.
  return (width: number, lowQuality = false): Row[] => {
    const mobile = width < 600;
    const count = Math.round((mobile ? scene.mobileRowCount : scene.rowCount) * (lowQuality ? .74 : 1));
    const bands = new Map<number, string[][]>();
    const rows: Row[] = [];
    for (let index = 0; index <= count; index++) {
      const depth = index / count * 1.13;
      const band = Math.min(15, Math.floor(depth * 14));
      const scale = depthScale(band / 14);
      const rowWidth = (width + 400) / scale;
      let lines = bands.get(band);
      if (!lines) {
        lines = layoutWithLines(prepared, rowWidth, 26).lines.map(line => {
          const words = line.text.trim().split(/\s+/u).filter(Boolean);
          assertSourceWords(words, allowed);
          return words;
        }).filter(words => words.length);
        bands.set(band, lines);
      }
      const words = lines[(index * 7 + band * 3) % lines.length];
      const anchors: Anchor[] = [];
      let x = -(width / 2 + 180) / depthScale(depth);
      // Repeat only intact, validated Pretext-packed words to cover the overscan edges.
      let wordIndex = 0;
      const end = (width / 2 + 240) / depthScale(depth);
      while (x < end) {
        const word = words[wordIndex++ % words.length];
        const advance = metrics.get(word)!;
        anchors.push({ word, x, width: advance });
        x += advance + space;
      }
      rows.push({ z: depth * 1000, anchors });
    }
    return rows;
  };
}
