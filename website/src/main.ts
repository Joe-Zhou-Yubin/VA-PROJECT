import '@fontsource/dm-mono/latin-400.css';
import '@fontsource/dm-mono/latin-500.css';
import '@fontsource/libre-caslon-display/latin-400.css';
import './style.css';
import csv from '../../text/EJF/ejf_word_freq.csv?raw';
import { parseVocabulary } from './vocabulary';
import { startOcean } from './ocean';

const canvas = document.querySelector<HTMLCanvasElement>('#ocean')!;
const toggle = document.querySelector<HTMLButtonElement>('#motion-toggle')!;
const status = document.querySelector<HTMLParagraphElement>('#scene-status')!;
let ocean: Awaited<ReturnType<typeof startOcean>> | undefined;
let disposed = false;

function updateMotion(paused: boolean) {
  toggle.setAttribute('aria-pressed', String(paused));
  toggle.querySelector('.motion-icon')!.textContent = paused ? '▷' : 'Ⅱ';
  toggle.querySelector('.motion-label')!.textContent = paused ? 'Resume animation' : 'Pause animation';
}

async function initialize() {
  try {
    const entries = parseVocabulary(csv);
    const top = [...entries].sort((a, b) => b.count - a.count).slice(0, 15);
    const list = document.querySelector('#cloud-summary')!;
    top.forEach(entry => {
      const item = document.createElement('li');
      item.textContent = `${entry.word}: ${entry.count.toLocaleString('en')} occurrences`;
      list.append(item);
    });
    document.querySelector('#vocabulary-count')!.textContent = new Set(entries.map(e => e.word)).size.toLocaleString('en');
    ocean = await startOcean(canvas, entries, updateMotion);
    if (disposed) { ocean.dispose(); return; }
    document.querySelector('.ocean-story')!.classList.add('scene-ready');
    toggle.addEventListener('click', onToggle);
  } catch (error) {
    console.error('The word ocean could not start:', error);
    status.textContent = 'The ocean is resting. You can still explore the words below.';
    status.hidden = false; toggle.hidden = true;
  }
}
function onToggle() { ocean?.toggle(); }
void initialize();
if (import.meta.hot) import.meta.hot.dispose(() => { disposed = true; ocean?.dispose(); toggle.removeEventListener('click', onToggle); });
