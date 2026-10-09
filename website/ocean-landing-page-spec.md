# Word Ocean Landing Page — Codex Implementation Specification

## 1. Task and scope

Build a working, locally runnable landing page in the user's VS Code project. The hero is an interactive ocean made from readable words in varying shades of blue. A fishing vessel floats on the words. Moving the pointer disturbs the water; those disturbances also affect the vessel.

Implement the page, rather than only proposing an approach. Inspect existing project files and instructions first. Preserve the existing framework and unrelated features. If the directory is empty, use Vite, TypeScript and plain HTML/CSS. No backend, account system, paid service or deployment is required. Make reasonable implementation decisions and document them.

This document specifies a future website implementation; the current task is to write the specification only. Build the eventual app inside `website/`, preserving the repository's research data and other folders.

Required local inputs (paths relative to this specification):

- Visual reference: [An ocean of words.png](<An ocean of words.png>). Inspect this image before implementation.
- Exclusive water vocabulary: [ejf_word_freq.csv](../text/EJF/ejf_word_freq.csv). The actual repository folder is `EJF`, not `EFJ`. The file has `word,count` columns and currently contains 500 vocabulary entries.

The reference shows a midnight navy page, large ivory heading at upper left, a dense blue typographic ocean across the lower two thirds, and a fishing trawler right of center. Match its composition, depth, rolling text rows, sparse bright crests and restrained boat lighting. The image is a visual target, not a flat background asset. Its example water words are not an authorized vocabulary source.

## 2. Required experience

- Water is built from actual words, not random symbols, isolated letters, a water photograph or solid blue wave shapes.
- Repeated words follow curving rows, forming rolling crests and troughs with a sense of depth.
- The ocean moves gently without interaction.
- Pointer movement produces local ripples that spread and fade. Fast movements have a stronger, capped effect.
- The vessel responds to the same water field: it rises, tilts and drifts slightly as disturbances reach it.
- Heading, navigation and buttons stay still and readable.
- Deliver a polished interactive scene, not just a static recreation of the image.

## 3. Visual direction

Desktop composition, approximately 1440 × 900 as an initial design reference:

| Element | Starting direction |
| --- | --- |
| Background | Midnight navy, #03152D |
| Water palette | Deep blue #0752A3, cobalt #087CEC, azure #16A5EB, cyan #45D7EE, pale crest #C5F3FF |
| Main text | Warm ivory #F4F1E8 |
| Secondary text | Pale blue #B3CCEB |
| Horizon | Roughly 34–38% down the hero |
| Ocean | Full width, extending beyond the bottom and side edges |
| Vessel | Right of center, about 66–72% across; near the middle distance |
| Vessel width | Approximately 180–260 CSS px on desktop; tune to composition |
| Heading | Large editorial serif, responsive rather than fixed |
| Water words | Crisp monospace, larger in foreground and smaller toward horizon |

Use a restrained palette; reserve the brightest tones for sparse crests. Avoid uniform neon brightness, excessive glow, bloom, or a crowded sky. Maintain dark gaps between word rows so the ocean is recognizably typographic. Foreground words must remain readable. Distant words may blend into texture but must not flicker.

### Water vocabulary: mandatory data contract

Use **only values from the `word` column of `../text/EJF/ejf_word_freq.csv`** for every word drawn in the water, including distant texture, crests, ripples and any static text-water fallback. Do not copy the reference image's vocabulary, add generic ocean words, or use `ejf_bigram_freq.csv`, `ejf_full_text.csv`, `ejf_statistics.csv` or another dataset. Heading, navigation and other ordinary interface copy are outside this restriction.

- Parse the CSV with a CSV-aware parser, treating the first row as headers. Read `count` as a positive numeric frequency; never draw counts or column names.
- Preserve each source word's spelling and case. Strip field-boundary whitespace only; do not stem, translate, split, truncate, hyphenate or invent tokens. Join complete words with spaces. If a word cannot fit, move it to another row or choose another allowed word.
- Make all valid entries eligible. Use a seeded sampler weighted by `count` so frequent source words recur more often. Examples verified in the file include `squid`, `fishing`, `vessels`, `fisheries`, `vessel` and `china`; these illustrate the source, not a hardcoded replacement list.
- Generate stable word sequences at scene initialization or a deliberate layout change, never randomly every frame. Frequency controls recurrence; perspective controls size and waves control color and position.
- Keep this CSV as the source of truth. For a Vite app in `website/`, prefer a build-time raw import such as `../text/EJF/ejf_word_freq.csv?raw` where supported, or generate a bundled vocabulary asset from that exact file. Do not assume a production browser can fetch an arbitrary parent-directory path. Document the chosen bundling approach.
- Validate headers, nonempty words and positive counts. If input is missing or invalid, report the issue clearly and show a quiet non-text fallback; never substitute an invented vocabulary.
- Add a meaningful vocabulary integrity check: every emitted water token must belong to the parsed source-word set, including after resize and quality changes. Verify packaged production assets include the vocabulary.

Lay out complete words with spaces, varying their order deterministically. The rendered water conveys the EJF corpus rather than reproducing the reference's literal text.

Placeholder copy, editable in one content/configuration file:

- Brand: OCEAN
- Navigation: About, Explore
- Heading: An ocean of words.
- Supporting copy: Move your cursor. Make a little wave.
- Primary button: Explore
- Mobile hint: Touch the water to make a wave.

Keep supporting page content minimal. Make Explore scroll to a short real section below the hero and About link to a short description. Do not create dead buttons or invent a commercial product.

## 4. Rendering architecture and Pretext

Use a Canvas 2D renderer with a lightweight perspective projection as the initial implementation. Render semantic content and controls in HTML/CSS above it. A WebGL implementation is acceptable if profiling shows that it is necessary, but do not introduce a large 3D stack before establishing the basic scene.

Use @chenglou/pretext meaningfully for cached text measurement/layout that informs the word rows. Verify the installed package's actual public API against its official documentation/types before coding. Do not assume community demo snippets match the installed version. Official API reference: [Pretext README](https://github.com/chenglou/pretext#readme). Use the official documentation and installed types as the implementation authority.

Pretext is a text layout library. The wave simulation, perspective, interaction and boat motion must be implemented separately. Preparing text should happen after fonts are ready and when text/font configuration changes, never for every word on every animation frame. Canvas text metrics may supplement per-word placement; document the division of responsibilities. Do not include Pretext as an unused dependency.

Concrete integration plan, based on the official README (recheck against the installed version):

1. After fonts are ready, form stable strings using the validated CSV words. Use `prepareWithSegments(text, font)` and cache the resulting handles by text and font configuration.
2. Use `layoutWithLines(prepared, rowWidth, lineHeight)` to produce cached row strings for each depth/width band. Reuse prepared handles on resize when text and fonts are unchanged. Keep words intact; do not render line fragments from emergency wrapping. Validate resulting tokens against the source set.
3. Split those complete row strings at their joining spaces into word anchors. Cache individual word advances and spacing with Canvas metrics if required for curved placement. The renderer projects each anchor onto the shared wave field; it does not draw each row as a rigid flat line.
4. Recompute layout when the viewport/quality requires it, not during each animation frame. Pretext determines actual row packing; removing it must change the layout path, so it cannot be a decorative dependency.

Suggested modules, adapting to the existing project:

- Hero/page component: HTML content, navigation and motion control.
- Ocean renderer: canvas lifecycle, resize, projection and draw order.
- Text layout: cached word strings, metrics and row placement; Pretext integration.
- Wave field: ambient waves and transient ripple contributions.
- Pointer input: coordinate conversion, velocity and disturbance creation.
- Vessel: water sampling, spring motion, hull placement and drawing.
- Vocabulary loader: CSV parsing, validation, seeded frequency sampling and source-set integrity checks.
- Scene configuration: colors, vocabulary source/seed, wave parameters and quality presets. No alternate water-word list.

Keep the renderer outside framework reactive state updates. Store animation state in ordinary objects/refs. Dispose of listeners, observers and animation callbacks on unmount.

## 5. Ocean geometry and animation

Choose and document one consistent water-plane coordinate system: x across the ocean, z from foreground toward horizon, and h for surface elevation. Keep pointer disturbances, text positions and boat samples in that same coordinate system.

Build rows of word anchors on this plane. Use a perspective projection to make distant rows closer together and smaller. Evaluate water height at each anchor and project the resulting position onto the screen. Add limited tangent rotation if it improves wave readability; do not distort words so severely that they become unreadable.

Use a shared function such as sampleWater(x, z, time) that returns height and, where useful, slope/current information. A suitable ambient height field is a sum of a few sine waves with different directions, wavelengths, amplitudes and speeds:

    H(x,z,t) = sum(A_i * sin(kx_i*x + kz_i*z - omega_i*t + phase_i))

Add damped traveling ripple contributions from pointer events. Each disturbance stores its origin, creation time and strength. A possible radial term is:

    R = strength * exp(-decay*age) * exp(-((distance-speed*age)/width)^2)
        * sin(frequency*(distance-speed*age))

This is a visual wave model, not a full fluid solver. Parameters and units must be consistent. Retire disturbances after their visible lifetime and cap the active count. Use the same H + sum(R) for the water and vessel.

Draw distant rows before near rows. Derive word color from depth and smooth wave/crest information, with gradual changes. Avoid abrupt palette switching. Keep enough bounds outside the viewport to prevent gaps during movement and resizing.

## 6. Pointer and touch interaction

- Use Pointer Events for mouse, pen and touch.
- Convert client coordinates to canvas-local CSS coordinates; keep device-pixel ratio out of input math.
- Map the pointer onto the underlying water plane using the inverse base-plane projection or a documented approximation. Keep this mapping aligned with the rendered water.
- Only create ripples within the visible ocean, not over navigation or hero text.
- Estimate velocity using elapsed time, smooth it and cap disturbance strength.
- Emit at controlled time/distance intervals, not once per raw pointer event.
- On pointer exit or cancellation, stop emitting; existing ripples continue fading.
- Moving near a boat should affect it through the water field, not directly attach the boat to the cursor.
- Support touch movement without disabling vertical page scrolling. Do not apply touch-action: none to the whole page. If a dedicated drag mode is needed, make it explicit; tapping the water must still create a ripple.
- Use the normal cursor initially. A custom cursor is optional and must not obscure controls.

Starting tuning targets: about 12–24 active disturbances maximum; visible ripple lifetime roughly 2–4 seconds. These are adjustable visual targets, not fixed requirements.

## 7. Fishing vessel

Use a recognizable fishing trawler with hull, cabin, mast, antenna and fishing rigging. It must not look like a sailboat or generic emoji. Prefer an existing appropriate transparent project asset. If none exists, create a well-detailed local SVG illustration in ivory, muted blue and restrained dark accents. A licensed or user-provided transparent illustration may replace it later. Do not hotlink assets or use the entire reference mockup as a boat image.

Define the sprite's waterline anchor and bow/stern sample offsets explicitly. Sample the shared water field beneath the bow and stern (or equivalent water-plane points). Use their projected heights/slope to derive target elevation and pitch. Tune the sample direction to match the visible hull orientation.

Use frame-rate-independent damped motion so the boat has some inertia. A spring/damping integrator with capped time steps or a stable exponential smoothing approach is suitable. Start with a rotation clamp around ±6–8 degrees. Add small bounded horizontal drift driven by wave/current information and a spring toward its home position. The boat should remain visible and never slide across the page chasing the cursor.

Draw order must embed the vessel in the water:

1. Far water rows behind the boat.
2. Boat at its sampled waterline.
3. Selected near-water words over the very bottom of the hull.

Use a waterline mask or depth split if needed. Do not cover the cabin with foreground words or expose an empty gap beneath the hull. Avoid a floating rectangular shadow. Boat rotation, translation and occlusion must share the same waterline anchor.

## 8. Responsive behavior and accessibility

- Desktop: broad ocean, heading upper left, boat right of center.
- Tablet: reduce heading and boat size, retain ample visible word-water.
- Mobile: keep heading above the busiest waves, reposition boat within visible bounds and reduce word density. Preserve readable foreground text. Avoid horizontal overflow.
- Use a responsive hero height with a sensible minimum; account for mobile browser viewport changes.
- Expose a keyboard-operable Pause animation / Resume animation control. Pause freezes ambient waves, ripples and boat motion and stops disturbance creation. Resume without a large time jump.
- Respect prefers-reduced-motion: begin with a static composed ocean, disable pointer-driven movement, and let the user explicitly enable motion if desired.
- Mark the decorative canvas aria-hidden. Convey the concept through ordinary visible page text; do not expose thousands of repeated words to assistive technology.
- Use semantic headings, navigation, links and buttons, visible focus states, sufficient contrast and practical touch targets.
- Keep the page usable if canvas initialization fails: show the normal page content and a quiet fallback background.

## 9. Performance and reliability

Use requestAnimationFrame with elapsed-time-based animation. Cap elapsed time after tab suspension. Pause rendering when the page is hidden or the hero is offscreen. Resize without restarting the scene or attaching duplicate loops. Recompute static layout only when dimensions, fonts, vocabulary or quality change.

Cap effective device-pixel ratio, initially at 1.5–2. Cache repeated text metrics and, if useful, glyph/word rasterization. Avoid DOM nodes per word, layout reads inside drawing loops, unbounded ripple arrays and large object allocations every frame.

Aim for smooth motion around 60 fps on a typical desktop and at least roughly 30 fps on a representative mobile device, with an adaptive lower-density preset if necessary. These are targets to measure, not claims to make without testing. Lower distant text density first, preserving readable foreground words and boat quality. Document the actual test environment and observed limitations.

## 10. Implementation sequence

1. Inspect the repository and its instructions; identify framework and start commands.
2. Build semantic responsive hero content and the static word ocean. Integrate and verify Pretext layout here.
3. Add ambient waves, perspective and restrained depth-based color.
4. Add pointer/touch disturbances using the shared water field.
5. Add the vessel, shared wave sampling, inertia and waterline occlusion.
6. Add responsive density, pause/reduced-motion behavior and lifecycle cleanup.
7. Run the build and relevant existing checks. Test the actual page, refine the composition, and report what was verified.

Do not spend the entire task on scaffolding. Reach a working end-to-end scene, then tune its typography and interaction. Do not deploy unless the user separately requests deployment.

## 11. Acceptance criteria

- [ ] The page starts locally using documented commands and builds without errors.
- [ ] Water visibly consists of complete words in several coordinated blue shades.
- [ ] Every water token belongs to the `word` column of `text/EJF/ejf_word_freq.csv`; counts, invented words and other CSV sources never appear in the water.
- [ ] Sampling uses source frequencies, stays stable during animation and preserves complete source words through Pretext layout.
- [ ] The production build includes CSV-derived vocabulary and does not rely on fetching outside its served root.
- [ ] Composition has been visually compared with the local `An ocean of words.png` reference.
- [ ] Foreground words are readable and distant rows create convincing depth.
- [ ] Waves move calmly without pointer input.
- [ ] Pointer movement creates local traveling disturbances, not whole-canvas translation.
- [ ] Disturbances fade and the ocean settles back to its ambient state.
- [ ] The fishing trawler bobs and tilts in response to the same disturbances.
- [ ] The vessel stays at the waterline, with credible partial hull occlusion.
- [ ] Text content and buttons remain steady, readable and clickable.
- [ ] About and Explore lead to real content.
- [ ] Layout works around 1440 × 900, 768 × 1024 and 390 × 844 without horizontal overflow.
- [ ] Touch interaction works while vertical page scrolling remains possible.
- [ ] Pause/resume and reduced-motion behavior cover all scene motion.
- [ ] Resize, tab switching and component remount do not create jumps or duplicate loops.
- [ ] Pretext has a real, documented text measurement/layout role.
- [ ] No missing assets, console errors or unbounded animation state.

Prioritize manual visual checks for composition and animation. If adding automated tests, target meaningful math/lifecycle risks such as projection round trips, expired ripple removal or bounded boat response. Do not add tests that simply mirror constants. Report browser checks truthfully; if a browser is unavailable, distinguish build verification from visual verification.

## 12. Deliverables from the coding agent

- Complete source integrated into the existing project, or a clean starter when empty.
- Local boat asset and any required fonts/assets, with sources/licenses recorded where applicable.
- Central scene configuration with brief notes for tuning word density, palette, wave strength, ripple strength, boat size and damping.
- README with install, development and production build commands; architecture summary; Pretext's role; any limitations.
- A concise completion message listing changes, commands/checks performed and any remaining visual differences from the reference.

## Suggested prompt to start the agent

Read ocean-landing-page-spec.md and implement the landing page in this project. Follow the repository's existing instructions and framework. Inspect `website/An ocean of words.png` as the visual target. Use only words from `text/EJF/ejf_word_freq.csv` for all water text, sampled using its counts, and use Pretext for cached row layout. Build a functioning word-based ocean with cursor ripples and a fishing vessel responding to the same waves. Continue through implementation and verification; make reasonable decisions for unspecified details. Do not deploy. Document how I can run it locally and tune its appearance.
