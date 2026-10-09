import { measureNaturalWidth, prepareWithSegments } from '@chenglou/pretext';
import type { Entry } from './vocabulary';

export interface CloudWord { word: string; count: number; x: number; y: number; width: number; height: number; size: number }

// Largest first; deterministic spiral packing with padded, measured rectangles.
// Coordinates are centers, local to the cloud stage. No layout work runs on scroll.
export function packCloud(entries: Entry[], width: number, height: number): CloudWord[] {
  const ranked = [...entries].sort((a, b) => b.count - a.count || a.word.localeCompare(b.word));
  const words: CloudWord[] = [];
  const mobile = width < 600;
  const limit = mobile ? 38 : 80;
  const maximum = ranked[0]?.count || 1;
  for (const entry of ranked.slice(0, limit)) {
    const size = (mobile ? 13 : 14) + Math.sqrt(entry.count / maximum) * (mobile ? 29 : 49);
    const wordWidth = measureNaturalWidth(prepareWithSegments(entry.word, `${size}px "DM Mono", monospace`));
    const boxWidth = wordWidth + 12, boxHeight = size * 1.22 + 8;
    for (let step = 0; step < 5000; step++) {
      const angle = step * .18;
      const radius = step * .19;
      const x = width / 2 + Math.cos(angle) * radius * (mobile ? .85 : 1.8);
      const y = height / 2 + Math.sin(angle) * radius;
      if (x - boxWidth / 2 < 4 || x + boxWidth / 2 > width - 4 || y - boxHeight / 2 < 4 || y + boxHeight / 2 > height - 4) continue;
      if (words.some(w => Math.abs(w.x - x) < (w.width + boxWidth) / 2 && Math.abs(w.y - y) < (w.height + boxHeight) / 2)) continue;
      words.push({ ...entry, x, y, width: boxWidth, height: boxHeight, size });
      break;
    }
  }
  return words;
}
