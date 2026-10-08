import type { Entry } from './vocabulary';
import { createTextLayout, type Row, type Anchor } from './layout';
import { addRipple, clamp, expireRipples, project, sampleWater, unprojectBase, type Ripple } from './waves';
import { scene } from './config';
import { createWordAtlas } from './atlas';
import { packCloud, type CloudWord } from './cloud';

export interface SceneDiagnostics {
  wordCount: number; rowCount: number; rippleCount: number; time: number;
  paused: boolean; boatAngle: number; boatY: number; lowQuality: boolean;
  scrollProgress: number; cloudWordCount: number;
}

export async function startOcean(canvas: HTMLCanvasElement, entries: Entry[], onState: (paused: boolean) => void) {
  const ctx = canvas.getContext('2d', { alpha: true });
  if (!ctx) throw new Error('Canvas 2D is unavailable.');
  await document.fonts.ready;
  const layout = createTextLayout(entries, ctx);
  const atlas = createWordAtlas(entries);
  const story = canvas.closest<HTMLElement>('.ocean-story')!;
  const hero = story.querySelector<HTMLElement>('.hero')!;
  const stage = story.querySelector<HTMLElement>('#cloud-stage')!;
  const boat = new Image();
  boat.src = `${import.meta.env.BASE_URL}trawler.svg`;
  await boat.decode();
  const reducedMotion = matchMedia('(prefers-reduced-motion: reduce)');
  let paused = reducedMotion.matches, visible = true, disposed = false;
  let width = 0, height = 0, horizon = 0, range = 0, rows: Row[] = [];
  let dpr = 1;
  let canvasHeight = 0, progress = 0, scrollStart = 0, scrollDistance = 1;
  let cloudX = 0, cloudY = 0;
  let cloud: CloudWord[] = [];
  let particles: { anchor: Anchor; z: number; target: CloudWord }[] = [];
  const selected = new Set<Anchor>();
  let time = 0, lastFrame = 0, raf = 0, boatY = 0, boatAngle = 0, boatDrift = 0, initialized = false;
  let lowQuality = false, slowFrames = 0, measuredFrames = 0;
  let lastPointer: { x: number; y: number; at: number } | null = null;
  let lastEmission = -Infinity, velocity = 0;
  const ripples: Ripple[] = [];
  const diagnostics: SceneDiagnostics = { wordCount: 0, rowCount: 0, rippleCount: 0, time: 0, paused, boatAngle: 0, boatY: 0, lowQuality, scrollProgress: 0, cloudWordCount: 0 };
  // Exposed for local QA; this contains scene measurements, never DOM nodes or dataset copies.
  Object.defineProperty(canvas, 'sceneDiagnostics', { value: diagnostics, configurable: true });
  Object.defineProperty(canvas, 'cloudLayout', { get: () => cloud.map(word => ({ ...word })), configurable: true });

  function resize() {
    const bounds = story.getBoundingClientRect();
    const cloudBounds = stage.getBoundingClientRect();
    width = bounds.width; height = hero.getBoundingClientRect().height;
    canvasHeight = bounds.height;
    cloudX = cloudBounds.left - bounds.left; cloudY = cloudBounds.top - bounds.top;
    scrollStart = bounds.top + window.scrollY;
    scrollDistance = Math.max(1, cloudY + cloudBounds.height / 2 - window.innerHeight / 2);
    horizon = height * (width < 600 ? .46 : .365);
    range = height - horizon + 45;
    dpr = Math.min(window.devicePixelRatio || 1, scene.maxDpr);
    canvas.width = Math.round(width * dpr); canvas.height = Math.round(canvasHeight * dpr);
    ctx!.setTransform(dpr, 0, 0, dpr, 0, 0);
    rows = layout(width, lowQuality);
    rebuildCloud(cloudBounds.width, cloudBounds.height);
    diagnostics.wordCount = rows.reduce((n, row) => n + row.anchors.length, 0);
    diagnostics.rowCount = rows.length;
    initialized = false;
    updateProgress();
    draw(0);
  }

  function rebuildCloud(stageWidth: number, stageHeight: number) {
    const available = new Set(rows.flatMap(row => row.anchors.map(anchor => anchor.word)));
    cloud = packCloud(entries.filter(entry => available.has(entry.word)), stageWidth, stageHeight);
    selected.clear(); particles = [];
    for (const target of cloud) {
      let best: { anchor: Anchor; z: number; score: number } | undefined;
      for (const row of rows) for (const anchor of row.anchors) {
        if (anchor.word !== target.word) continue;
        const pos = project(anchor.x, row.z, 0, width, horizon, range);
        if (pos.x < 0 || pos.x + anchor.width * pos.scale > width || pos.y > height - 25) continue;
        const score = Math.abs(pos.x - (cloudX + target.x)) + Math.abs(pos.y - height * .7) * .6;
        if (!best || score < best.score) best = { anchor, z: row.z, score };
      }
      if (best) { selected.add(best.anchor); particles.push({ anchor: best.anchor, z: best.z, target }); }
    }
    cloud = particles.map(particle => particle.target);
    diagnostics.cloudWordCount = cloud.length;
  }

  function updateProgress() {
    const raw = clamp((window.scrollY - scrollStart) / scrollDistance, 0, 1);
    progress = raw * raw * (3 - 2 * raw);
    diagnostics.scrollProgress = progress;
  }

  function drawCloud() {
    const staticView = paused;
    if (!staticView && progress === 0) return;
    ctx!.textAlign = 'center';
    ctx!.textBaseline = 'middle';
    for (let index = 0; index < particles.length; index++) {
      const { anchor, z, target } = particles[index];
      const delay = (index % 7) * .018;
      const t = staticView ? 1 : clamp((progress - delay) / (1 - delay), 0, 1);
      if (!staticView && t === 0) continue;
      const elevation = sampleWater(anchor.x + anchor.width / 2, z, time, ripples);
      const start = project(anchor.x + anchor.width / 2, z, elevation, width, horizon, range);
      const x = start.x + (cloudX + target.x - start.x) * t + Math.sin(t * Math.PI) * Math.sin(index * 2.4) * 65;
      const y = start.y + (cloudY + target.y - start.y) * t;
      const size = 21 * start.scale + (target.size - 21 * start.scale) * t;
      ctx!.font = `${size}px "DM Mono", monospace`;
      const prominence = Math.sqrt(target.count / cloud[0].count);
      ctx!.fillStyle = `rgb(${Math.round(42 + prominence * 150)} ${Math.round(145 + prominence * 94)} ${Math.round(216 + prominence * 35)})`;
      ctx!.fillText(anchor.word, x, y);
    }
    ctx!.textAlign = 'start'; ctx!.textBaseline = 'alphabetic';
  }

  function drawBoat(dt: number) {
    const depth = width < 600 ? .45 : scene.boatDepth;
    const z = depth * 1000;
    const boatWidth = width < 600 ? 190 : clamp(width * .195, 220, 310);
    const homeX = width * (width < 600 ? .66 : .70);
    const p = unprojectBase(homeX, horizon + Math.pow(depth, 1.65) * range, width, horizon, range);
    const sampleOffset = boatWidth * .34 / (.16 + .84 * depth);
    const left = sampleWater(p.x - sampleOffset, z, time, ripples);
    const right = sampleWater(p.x + sampleOffset, z, time, ripples);
    const water = sampleWater(p.x, z, time, ripples);
    const center = project(p.x, z, water, width, horizon, range);
    const targetAngle = clamp(Math.atan2((left - right) * center.scale, boatWidth * .68), -.12, .12);
    const blend = initialized ? 1 - Math.exp(-scene.boatDamping * dt) : 1;
    boatY += (center.y - boatY) * blend;
    boatAngle += (targetAngle - boatAngle) * blend;
    boatDrift += (clamp(water * .14, -9, 9) - boatDrift) * blend;
    initialized = true;
    const scale = boatWidth / 400;
    ctx!.save();
    ctx!.globalAlpha = paused ? 1 : 1 - clamp(progress * 2, 0, 1);
    ctx!.translate(homeX + boatDrift, boatY);
    ctx!.rotate(boatAngle);
    ctx!.drawImage(boat, -200 * scale, -264 * scale, boatWidth, 290 * scale);
    ctx!.restore();
  }

  function draw(dt: number) {
    ctx!.clearRect(0, 0, width, canvasHeight);
    ctx!.font = scene.font;
    ctx!.textBaseline = 'alphabetic';
    let boatDrawn = false;
    const boatZ = (width < 600 ? .45 : scene.boatDepth) * 1000;
    const flow = paused ? 0 : progress;
    for (const row of rows) {
      if (!boatDrawn && row.z > boatZ + 12) { drawBoat(dt); boatDrawn = true; }
      for (const anchor of row.anchors) {
        if (flow > 0 && selected.has(anchor)) continue;
        const elevation = sampleWater(anchor.x + anchor.width / 2, row.z, time, ripples);
        const pos = project(anchor.x, row.z, elevation, width, horizon, range);
        pos.y += Math.pow(flow, 1.4) * height * .65;
        if (pos.x < -anchor.width * pos.scale || pos.x > width + 20 || pos.y > height + 35) continue;
        const nextHeight = sampleWater(anchor.x + anchor.width / 2 + 12, row.z, time, ripples);
        const rotation = clamp(-(nextHeight - elevation) / 12, -.28, .28);
        const crest = clamp((elevation - 15) / 49, 0, 1);
        // Smooth crest colors: deep blue -> cyan -> pale ice. No frame-random color changes.
        const tone = crest * (atlas.tones - 1), lower = Math.floor(tone);
        const blend = tone - lower;
        const locations = atlas.words.get(anchor.word)!;
        const sprite = locations[lower];
        const scale = pos.scale * dpr, cos = Math.cos(rotation), sin = Math.sin(rotation);
        ctx!.setTransform(cos * scale, sin * scale, -sin * scale, cos * scale, pos.x * dpr, pos.y * dpr);
        ctx!.globalAlpha = (.65 + Math.min(row.z / 1000, 1) * .35) * (1 - flow);
        ctx!.drawImage(atlas.image, sprite.x, sprite.y, sprite.width, atlas.lineHeight, -3, -22, sprite.width, atlas.lineHeight);
        if (blend > .02 && lower < atlas.tones - 1) {
          const next = locations[lower + 1];
          ctx!.globalAlpha *= blend;
          ctx!.drawImage(atlas.image, next.x, next.y, next.width, atlas.lineHeight, -3, -22, next.width, atlas.lineHeight);
        }
        ctx!.setTransform(dpr, 0, 0, dpr, 0, 0);
        ctx!.globalAlpha = 1;
      }
    }
    if (!boatDrawn) drawBoat(dt);
    drawCloud();
    diagnostics.time = time; diagnostics.rippleCount = ripples.length;
    diagnostics.boatAngle = boatAngle; diagnostics.boatY = boatY;
  }

  function frame(stamp: number) {
    raf = 0;
    if (disposed || paused || !visible || document.hidden) { lastFrame = 0; return; }
    const elapsed = lastFrame ? (stamp - lastFrame) / 1000 : 0;
    const dt = Math.min(elapsed, .04);
    lastFrame = stamp;
    time += dt;
    expireRipples(ripples, time);
    draw(dt);
    // One-way density reduction after sustained slow rendering; foreground remains readable.
    if (elapsed > 0 && measuredFrames < 180) {
      measuredFrames++;
      if (elapsed > .037) slowFrames++;
      if (measuredFrames === 180 && slowFrames > 90 && !lowQuality) {
        lowQuality = true; diagnostics.lowQuality = true;
        rows = layout(width, true);
        rebuildCloud(stage.getBoundingClientRect().width, stage.getBoundingClientRect().height);
        diagnostics.rowCount = rows.length;
        diagnostics.wordCount = rows.reduce((n, row) => n + row.anchors.length, 0);
      }
    }
    if (progress < 1) raf = requestAnimationFrame(frame);
    else lastFrame = 0;
  }
  function schedule() {
    if (!disposed && !paused && visible && !document.hidden && !raf) raf = requestAnimationFrame(frame);
  }
  function setPaused(value: boolean) {
    paused = value; diagnostics.paused = paused; lastFrame = 0; lastPointer = null;
    if (raf) cancelAnimationFrame(raf);
    raf = 0; onState(paused); draw(0); schedule();
  }

  function pointer(event: PointerEvent) {
    if (paused || progress > .1 || !visible || document.hidden || (event.target as HTMLElement).closest('a,button') || (event.pointerType === 'touch' && event.type === 'pointermove' && !event.isPrimary)) return;
    const rect = canvas.getBoundingClientRect();
    const x = event.clientX - rect.left, y = event.clientY - rect.top;
    if (y < horizon + 8 || y > height) { lastPointer = null; return; }
    const now = performance.now();
    const speed = lastPointer ? Math.hypot(x - lastPointer.x, y - lastPointer.y) / Math.max(8, now - lastPointer.at) : 0;
    velocity = velocity * .55 + speed * .45;
    const moved = !lastPointer || Math.hypot(x - lastPointer.x, y - lastPointer.y) > 5;
    lastPointer = { x, y, at: now };
    if (event.type !== 'pointerdown' && (!moved || now - lastEmission < 65)) return;
    const origin = unprojectBase(x, y, width, horizon, range);
    addRipple(ripples, { ...origin, born: time, strength: scene.rippleStrength + clamp(velocity, 0, 2.5) * 19 });
    lastEmission = now;
  }
  const resetPointer = () => { lastPointer = null; velocity = 0; };
  const visibilityChange = () => { lastFrame = 0; if (document.hidden && raf) { cancelAnimationFrame(raf); raf = 0; } else schedule(); };
  const motionChange = () => setPaused(reducedMotion.matches);
  let scrollRaf = 0;
  const scrollChange = () => {
    if (scrollRaf || disposed) return;
    scrollRaf = requestAnimationFrame(() => {
      scrollRaf = 0; updateProgress();
      if (paused) draw(0); else schedule();
    });
  };
  const observer = new ResizeObserver(resize);
  const intersection = new IntersectionObserver(([entry]) => {
    visible = entry.isIntersecting; lastFrame = 0;
    if (!visible && raf) { cancelAnimationFrame(raf); raf = 0; } else schedule();
  });
  hero.addEventListener('pointermove', pointer, { passive: true });
  hero.addEventListener('pointerdown', pointer, { passive: true });
  hero.addEventListener('pointerleave', resetPointer);
  hero.addEventListener('pointercancel', resetPointer);
  window.addEventListener('scroll', scrollChange, { passive: true });
  window.addEventListener('resize', resize);
  document.addEventListener('visibilitychange', visibilityChange);
  reducedMotion.addEventListener('change', motionChange);
  resize(); observer.observe(story); intersection.observe(story); onState(paused); schedule();
  return {
    toggle: () => setPaused(!paused),
    dispose: () => {
      disposed = true; cancelAnimationFrame(raf); cancelAnimationFrame(scrollRaf); observer.disconnect(); intersection.disconnect();
      hero.removeEventListener('pointermove', pointer); hero.removeEventListener('pointerdown', pointer);
      hero.removeEventListener('pointerleave', resetPointer); hero.removeEventListener('pointercancel', resetPointer);
      window.removeEventListener('scroll', scrollChange); window.removeEventListener('resize', resize);
      document.removeEventListener('visibilitychange', visibilityChange); reducedMotion.removeEventListener('change', motionChange);
    },
  };
}
