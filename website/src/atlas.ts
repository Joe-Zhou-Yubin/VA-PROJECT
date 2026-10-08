import type { Entry } from './vocabulary';
import { scene } from './config';

// Rasterize the finite vocabulary once instead of asking the font engine to paint
// thousands of transformed words every frame. Six tones blend into smooth crests.
export function createWordAtlas(entries: Entry[]) {
  const atlas = document.createElement('canvas');
  const ctx = atlas.getContext('2d')!;
  const width = 2048, lineHeight = 29, tones = 6;
  ctx.font = scene.font;
  const words = new Map<string, { x: number; y: number; width: number }[]>();
  let x = 0, y = 0;
  for (let tone = 0; tone < tones; tone++) for (const { word } of entries) {
    const wordWidth = Math.ceil(ctx.measureText(word).width) + 6;
    if (x + wordWidth > width) { x = 0; y += lineHeight; }
    const locations = words.get(word) || [];
    locations.push({ x, y, width: wordWidth }); words.set(word, locations);
    x += wordWidth;
  }
  atlas.width = width; atlas.height = y + lineHeight;
  ctx.font = scene.font; ctx.textBaseline = 'alphabetic';
  for (const [word, locations] of words) locations.forEach((location, tone) => {
    const crest = tone / (tones - 1);
    ctx.fillStyle = `rgb(${Math.round(10 + crest * crest * 184)} ${Math.round(100 + crest * 133)} ${Math.round(205 + crest * 47)})`;
    ctx.fillText(word, location.x + 3, location.y + 22);
  });
  return { image: atlas, words, lineHeight, tones };
}
