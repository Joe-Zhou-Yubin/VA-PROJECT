# An ocean of words

A local, interactive landing page based on [An ocean of words.png](<An ocean of words.png>). Blue word rows form a gently moving ocean. Mouse, pen and touch input create traveling ripples; an illustrated fishing trawler samples that same water field.

Scroll into Explore to let words leave the water and gather into a frequency-sized word cloud, replacing the former frequency cards. Scroll back up to reverse the transformation. The cloud comes before its introduction so flowing words have an uninterrupted path, without opaque text panels covering them. Your current hero heading and copy are preserved.

The ocean and cloud share one canvas spanning both sections. A subset of existing ocean anchors maps to matching cloud words; remaining ocean words fade downstream. The cloud uses up to 80 frequent source words on wide screens and a smaller selection on mobile, depending on available space. Pretext measures each word at its frequency-based size, and a deterministic spiral packs padded rectangles without overlaps. These targets are calculated on resize, not on scroll. The boat fades as the ocean leaves view, and animation stops once the cloud settles.

Reduced-motion preferences and the Pause control show separate static ocean/cloud compositions without the flowing transition. The cloud has an accessible list of the 15 most frequent words and their counts, which also remains visible if canvas initialization fails.

## Run locally

Requires Node.js 22.19 or newer. From the repository root:

```powershell
cd website
npm.cmd install
npm.cmd run dev
```

Open the Local URL printed by Vite (normally `http://127.0.0.1:5173`). On macOS/Linux, use `npm` instead of `npm.cmd`.

```powershell
npm.cmd run build
npm.cmd run preview
```

The production output is `website/dist/`. The website is local only; no hosting or backend is needed. Build from this repository, since the source vocabulary lives in its sibling `text/` directory. The resulting `dist/` is self-contained.

## Vocabulary and Pretext

The sole water-word source is [`../text/EJF/ejf_word_freq.csv`](../text/EJF/ejf_word_freq.csv). `EJF` is the actual folder name. Vite's raw import embeds the CSV in the production JavaScript; the browser never fetches a parent directory. Papa Parse handles CSV quoting and headers. Invalid data produces a quiet fallback rather than alternate words.

A seeded sampler uses the `count` column to weight recurrence. All 500 source entries are eligible. Spelling and case are preserved. Each word emitted by Pretext layout is checked against the source-word set. Word order stays stable through animation, and resizing deterministically repacks it. No other text dataset contributes to the water.

[`@chenglou/pretext`](https://github.com/chenglou/pretext#readme), installed at 0.0.9, prepares the sampled text after fonts are ready. `prepareWithSegments` caches segmentation and measurement; `layoutWithLines` packs the actual strings used by depth bands. The prepared handle is reused on resize. Canvas metrics supply individual word advances for curved placement. Pretext does not simulate waves.

## Architecture and tuning

- `index.html`: page copy, semantic navigation, About/Explore sections and animation control.
- `src/style.css`: palette, typography and responsive composition.
- `src/config.ts`: seed, word font, row counts, DPR cap, boat depth, damping and ripple strength.
- `src/vocabulary.ts`: parsing, validation and deterministic frequency sampling.
- `src/layout.ts`: cached Pretext layout and complete-word anchors.
- `src/cloud.ts`: frequency sizing and cached, collision-free cloud packing.
- `src/atlas.ts`: one-time rasterization of the exact source vocabulary into six blended color tones, avoiding thousands of font operations per frame. Adjust crest colors here.
- `src/waves.ts`: shared ambient/ripple field, projection and inverse base-plane mapping. Adjust wave amplitudes/speeds here.
- `src/ocean.ts`: rendering, input, boat motion, resize and lifecycle cleanup. Boat size and responsive position are set in `drawBoat`; horizon placement is in `resize`.
- `public/trawler.svg`: original local fishing-vessel illustration, with waterline anchor `(200, 264)` in its `400 × 290` viewBox.

Water coordinates use lateral `x` in world pixels, `z` from 0 at the horizon to 1000 in the foreground, and positive-up elevation. Depth controls scale and projected baseline. Pointer coordinates invert the undeformed plane, an approximation rather than a raycast against the animated surface. The boat samples bow/stern elevations, follows with exponential damping, and limits rotation to about ±7°. Its lower hull is occluded by nearer word rows.

Animation pauses when the hero is offscreen or the document is hidden. Explicit pause freezes scene time, ripples and vessel motion. Reduced-motion preferences start with a composed static view; Resume animation explicitly enables motion. Passive touch input retains vertical scrolling. Ripple count and lifetime are bounded. A density reduction activates after sustained slow frames.

## Checks

```powershell
npm.cmd test
npm.cmd run build
# In another terminal, while preview is running:
npm.cmd run check:browser
```

Browser checks use installed Microsoft Edge through Playwright. Set `BROWSER_CHANNEL=chrome` to use installed Chrome; set `PREVIEW_URL` if preview uses another address. Playwright does not download a browser for this project. Screenshots and the JSON report are saved in ignored `.checks/`.

Verified on Windows with headless Microsoft Edge:

- TypeScript and production build passed; four focused source/sampling, CSV, projection and ripple tests passed.
- Browser checks passed at 1440 × 900, 768 × 1024 and 390 × 844: no horizontal overflow, no unexpected console/page/HTTP errors, local assets loaded, and source vocabulary guards passed.
- Pointer disturbances, frozen scene/boat during pause, resume, navigation, resize, reduced-motion startup, touch taps, actual touch scrolling and canvas-failure fallback passed.
- Ocean-to-cloud progress, reverse scrolling, exact source membership, cloud bounds and pairwise non-overlap passed at all three viewport sizes. Intermediate-flow and settled-cloud screenshots are also saved in `.checks/`.
- The atlas renderer averaged 59?60 fps with a 17 ms 95th-percentile frame interval across 100 sampled desktop frames. This is a headless desktop observation, not a physical mobile-device performance claim.
- Desktop and mobile screenshots were inspected against the supplied reference. The trawler is an SVG interpretation rather than the reference's realistic vessel. Dense distant text intentionally forms texture; foreground words remain larger. Physical-device Safari and Firefox have not been tested.

## Assets and licenses

- `An ocean of words.png`: user-supplied reference, used for visual direction; it is not shipped in the production page.
- `public/trawler.svg` and `public/favicon.svg`: original illustrations created for this project; no external image services or hotlinks.
- DM Mono and Libre Caslon Display: bundled via Fontsource, SIL Open Font License 1.1. Copies are shipped in `public/licenses/` and `dist/licenses/`.
- Pretext: MIT; Papa Parse: MIT. Dependency licenses are included in their installed packages.
- EJF vocabulary: existing project data; no new licensing assertions are made about the corpus. Refer to the repository's source documentation for provenance.
