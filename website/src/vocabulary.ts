import Papa from 'papaparse';

export interface Entry { word: string; count: number }

export function parseVocabulary(csv: string): Entry[] {
  const parsed = Papa.parse<Record<string, string>>(csv, { header: true, skipEmptyLines: 'greedy', transformHeader: h => h.trim() });
  if (parsed.errors.length || parsed.meta.fields?.join(',') !== 'word,count') throw new Error('Expected a valid word,count CSV.');
  const entries = parsed.data.map(row => ({ word: row.word?.trim(), count: Number(row.count) }));
  if (!entries.length || entries.some(e => !e.word || /\s/u.test(e.word) || !Number.isFinite(e.count) || e.count <= 0)) {
    throw new Error('The vocabulary must contain complete words and positive frequencies.');
  }
  return entries;
}

export function createSampler(entries: Entry[], seed = 241) {
  let state = seed >>> 0;
  const cumulative: number[] = [];
  let total = 0;
  for (const entry of entries) cumulative.push(total += entry.count);
  return () => {
    state = (Math.imul(state, 1664525) + 1013904223) >>> 0;
    const target = state / 4294967296 * total;
    let lo = 0, hi = cumulative.length - 1;
    while (lo < hi) { const mid = (lo + hi) >>> 1; if (target < cumulative[mid]) hi = mid; else lo = mid + 1; }
    return entries[lo].word;
  };
}

export function assertSourceWords(words: string[], allowed: Set<string>) {
  for (const word of words) if (!allowed.has(word)) throw new Error(`Water word is not in the source: ${word}`);
}
