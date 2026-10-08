import { chromium } from '@playwright/test';
import assert from 'node:assert/strict';
import { mkdir, readFile, writeFile } from 'node:fs/promises';
import Papa from 'papaparse';

const base = process.env.PREVIEW_URL || 'http://127.0.0.1:4173';
const browser = await chromium.launch({ channel: process.env.BROWSER_CHANNEL || 'msedge', headless: true });
await mkdir('.checks', { recursive: true });
const source = await readFile(new URL('../../text/EJF/ejf_word_freq.csv', import.meta.url), 'utf8');
const allowed = new Set(Papa.parse(source, { header: true, skipEmptyLines: true }).data.map(e => e.word));
const reports = [];

try {
  for (const viewport of [{ width: 1440, height: 900 }, { width: 768, height: 1024 }, { width: 390, height: 844 }]) {
    const context = await browser.newContext({ viewport, deviceScaleFactor: 1, hasTouch: viewport.width === 390 });
    const page = await context.newPage();
    const errors = [];
    page.on('pageerror', e => errors.push(e.message));
    page.on('console', m => { if (m.type() === 'error') errors.push(m.text()); });
    page.on('response', r => { if (r.status() >= 400) errors.push(`${r.status()} ${r.url()}`); });
    await page.addInitScript(() => {
      const original = CanvasRenderingContext2D.prototype.fillText;
      window.drawnWaterWords = new Set();
      CanvasRenderingContext2D.prototype.fillText = function(text, ...rest) {
        window.drawnWaterWords.add(text);
        return original.call(this, text, ...rest);
      };
    });
    await page.goto(base, { waitUntil: 'networkidle' });
    await page.waitForFunction(() => document.querySelector('#ocean').sceneDiagnostics?.wordCount > 0);
    await page.waitForTimeout(600);
    const overflow = await page.evaluate(() => document.documentElement.scrollWidth > innerWidth);
    assert.equal(overflow, false, `horizontal overflow at ${viewport.width}`);
    const diagnostics = () => page.evaluate(() => ({ ...document.querySelector('#ocean').sceneDiagnostics }));
    const before = await diagnostics();
    await page.mouse.move(viewport.width * .70, viewport.height * .60);
    await page.mouse.move(viewport.width * .55, viewport.height * .70, { steps: 12 });
    await page.waitForTimeout(80);
    const interacted = await diagnostics();
    assert.ok(interacted.rippleCount > 0, 'pointer should disturb water');
    await page.getByRole('button', { name: 'Pause animation' }).click();
    const frozen = await diagnostics();
    await page.waitForTimeout(250);
    const still = await diagnostics();
    assert.equal(still.time, frozen.time);
    assert.equal(still.boatY, frozen.boatY);
    assert.equal(still.boatAngle, frozen.boatAngle);
    await page.mouse.move(20, 20);
    await page.screenshot({ path: `.checks/ocean-${viewport.width}.png`, fullPage: true });
    const words = await page.evaluate(() => [...window.drawnWaterWords]);
    assert.ok(words.length > 50, 'water should display a varied vocabulary');
    for (const word of words) assert.ok(allowed.has(word), `unexpected rendered token: ${word}`);
    await page.getByRole('button', { name: 'Resume animation' }).click();
    await page.waitForTimeout(150);
    assert.ok((await diagnostics()).time > frozen.time);
    await page.locator('.header nav a[href="#findings"]').click();
    await page.waitForTimeout(700);
    assert.equal(new URL(page.url()).hash, '#findings');
    assert.ok(await page.locator('#findings').evaluate(el => Math.abs(el.getBoundingClientRect().top) < 100));
    const cloudLayout = await page.evaluate(() => document.querySelector('#ocean').cloudLayout);
    assert.ok(cloudLayout.length >= 25, 'cloud must contain a useful set of source words');
    const stageBounds = await page.locator('#cloud-stage').boundingBox();
    for (let i = 0; i < cloudLayout.length; i++) {
      const word = cloudLayout[i];
      assert.ok(allowed.has(word.word));
      assert.ok(word.x - word.width / 2 >= 0 && word.x + word.width / 2 <= stageBounds.width);
      assert.ok(word.y - word.height / 2 >= 0 && word.y + word.height / 2 <= stageBounds.height);
      for (const other of cloudLayout.slice(i + 1)) {
        assert.ok(Math.abs(word.x - other.x) >= (word.width + other.width) / 2 || Math.abs(word.y - other.y) >= (word.height + other.height) / 2, `${word.word} overlaps ${other.word}`);
      }
    }
    const cloudScroll = await page.locator('#cloud-stage').evaluate(el => el.getBoundingClientRect().top + scrollY + el.clientHeight / 2 - innerHeight / 2);
    await page.evaluate(top => scrollTo({ top, behavior: 'instant' }), cloudScroll / 2);
    await page.waitForTimeout(150);
    const midway = await diagnostics();
    assert.ok(midway.scrollProgress > .2 && midway.scrollProgress < .8);
    await page.screenshot({ path: `.checks/flow-${viewport.width}.png` });
    await page.evaluate(top => scrollTo({ top: top + 2, behavior: 'instant' }), cloudScroll);
    await page.waitForTimeout(150);
    assert.equal((await diagnostics()).scrollProgress, 1);
    await page.screenshot({ path: `.checks/cloud-${viewport.width}.png` });
    await page.evaluate(() => scrollTo({ top: 0, behavior: 'instant' }));
    await page.waitForTimeout(150);
    assert.equal((await diagnostics()).scrollProgress, 0);
    assert.equal((await diagnostics()).cloudWordCount, cloudLayout.length);
    await page.getByRole('link', { name: 'Explore', exact: true }).click();
    await page.waitForTimeout(600);
    assert.equal(new URL(page.url()).hash, '#findings');
    await page.setViewportSize({ width: viewport.width + 20, height: viewport.height });
    await page.waitForTimeout(100);
    const resizedWords = await page.evaluate(() => [...window.drawnWaterWords]);
    for (const word of resizedWords) assert.ok(allowed.has(word));
    assert.deepEqual(errors, []);
    reports.push({ viewport, initial: before, interacted, cloudWords: cloudLayout.length, scrollReversal: 'passed', cloudBoundsAndCollisions: 'passed', distinctRasterizedSourceWords: resizedWords.length, errors });
    await context.close();
  }

  const reducedContext = await browser.newContext({ viewport: { width: 390, height: 844 }, reducedMotion: 'reduce', hasTouch: true, isMobile: true });
  const reduced = await reducedContext.newPage();
  await reduced.goto(base, { waitUntil: 'networkidle' });
  await reduced.waitForFunction(() => document.querySelector('#ocean').sceneDiagnostics?.wordCount > 0);
  const timeBefore = await reduced.evaluate(() => document.querySelector('#ocean').sceneDiagnostics.time);
  await reduced.touchscreen.tap(200, 650);
  await reduced.waitForTimeout(200);
  assert.deepEqual(await reduced.evaluate(() => ({ time: document.querySelector('#ocean').sceneDiagnostics.time, ripples: document.querySelector('#ocean').sceneDiagnostics.rippleCount })), { time: timeBefore, ripples: 0 });
  await reduced.getByRole('button', { name: 'Resume animation' }).click();
  await reduced.touchscreen.tap(240, 640);
  await reduced.waitForTimeout(100);
  assert.ok(await reduced.evaluate(() => document.querySelector('#ocean').sceneDiagnostics.rippleCount > 0));
  const touch = await reducedContext.newCDPSession(reduced);
  await touch.send('Input.dispatchTouchEvent', { type: 'touchStart', touchPoints: [{ x: 80, y: 710 }] });
  for (let y = 690; y >= 430; y -= 20) {
    await touch.send('Input.dispatchTouchEvent', { type: 'touchMove', touchPoints: [{ x: 80, y }] });
    await reduced.waitForTimeout(25);
  }
  await touch.send('Input.dispatchTouchEvent', { type: 'touchEnd', touchPoints: [] });
  await reduced.waitForTimeout(150);
  assert.ok(await reduced.evaluate(() => scrollY > 80), 'touch water should allow vertical page scrolling');
  await reducedContext.close();
  reports.push({ reducedMotion: 'passed', touchTap: 'passed', touchScroll: 'passed' });

  const perfPage = await browser.newPage({ viewport: { width: 1440, height: 900 } });
  await perfPage.goto(base, { waitUntil: 'networkidle' });
  await perfPage.waitForFunction(() => document.querySelector('#ocean').sceneDiagnostics?.wordCount > 0);
  const performance = await perfPage.evaluate(() => new Promise(resolve => {
    const intervals = []; let last = 0;
    function frame(now) {
      if (last) intervals.push(now - last);
      last = now;
      if (intervals.length < 100) requestAnimationFrame(frame);
      else resolve({ meanFps: Math.round(1000 / (intervals.reduce((a, b) => a + b, 0) / intervals.length)), p95FrameMs: Math.round([...intervals].sort((a, b) => a - b)[95]), scene: { ...document.querySelector('#ocean').sceneDiagnostics } });
    }
    requestAnimationFrame(frame);
  }));
  reports.push({ headlessEdgePerformance: performance });
  await perfPage.close();

  const fallbackPage = await browser.newPage();
  await fallbackPage.addInitScript(() => {
    const original = HTMLCanvasElement.prototype.getContext;
    HTMLCanvasElement.prototype.getContext = function(...args) { return this.id === 'ocean' ? null : original.apply(this, args); };
  });
  await fallbackPage.goto(base, { waitUntil: 'networkidle' });
  assert.equal(await fallbackPage.locator('#scene-status').isVisible(), true);
  assert.equal(await fallbackPage.locator('#cloud-summary li').count(), 15);
  await fallbackPage.close();
  reports.push({ canvasFailureFallback: 'passed' });
  await writeFile('.checks/report.json', JSON.stringify(reports, null, 2));
  console.log(JSON.stringify(reports, null, 2));
} finally { await browser.close(); }
