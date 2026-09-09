/*
 * Renders every flyer to a print-ready PNG (2625x3375 = 8.75x11.25in @ 300dpi, bleed included)
 * and a PDF (8.75x11.25in), then runs a TREC advertising check on each page.
 *
 *   node flyers/export_tool/export.js            # all flyers
 *   node flyers/export_tool/export.js 1 3        # only flyers whose folder starts with 1_ or 3_
 *
 * Needs Playwright with Chromium. If `playwright` is installed globally, it is picked up from `npm root -g`.
 */
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

function loadPlaywright() {
  try { return require('playwright'); } catch (_) {}
  const g = execSync('npm root -g').toString().trim();
  return require(path.join(g, 'playwright'));
}
const { chromium } = loadPlaywright();

const REPO = path.resolve(__dirname, '..', '..');
const FLYERS_DIR = path.join(REPO, 'flyers');
const OUT_DIR = path.join(FLYERS_DIR, 'print_ready');
const PREVIEW_DIR = path.join(FLYERS_DIR, 'preview');   // 840x1080 screen-size previews for the showcase page

const W = 840, H = 1080;           // CSS px @96/in  -> 8.75 x 11.25 in
const SCALE = 300 / 96;            // 3.125 -> 2625 x 3375 px = 300 dpi

const only = process.argv.slice(2);
const flyers = fs.readdirSync(FLYERS_DIR)
  .filter((d) => /^\d+_/.test(d) && fs.existsSync(path.join(FLYERS_DIR, d, 'flyer.html')))
  .filter((d) => only.length === 0 || only.some((p) => d.startsWith(p + '_')))
  .sort();

// TREC 22 TAC §535.155: every ad must show the broker's name in a readily noticeable place,
// at least half the size of the largest contact information for the sales agent.
// Flyers mark contact info with data-trec="contact" and the broker line with data-trec="broker".
async function trecCheck(page) {
  return page.evaluate(() => {
    const px = (el) => parseFloat(getComputedStyle(el).fontSize);
    const contacts = [...document.querySelectorAll('[data-trec="contact"]')]
      .map((el) => ({ label: el.dataset.label || el.textContent.trim().slice(0, 30), size: px(el) }));
    const brokers = [...document.querySelectorAll('[data-trec="broker"]')]
      .map((el) => ({ text: el.textContent.trim().replace(/\s+/g, ' ').slice(0, 60), size: px(el) }));
    const text = document.body.innerText;
    const maxContact = Math.max(0, ...contacts.map((c) => c.size));
    const maxBroker = Math.max(0, ...brokers.map((b) => b.size));
    return {
      contacts, brokers, maxContact, maxBroker,
      brokerNamed: brokers.some((b) => /Spirit Real Estate Group/i.test(b.text)),
      brokerHalfSize: maxBroker >= maxContact / 2,
      hasLicense: /TREC\s*(License\s*)?#?\s*831516/i.test(text),
      hasIabs: /Information About Brokerage Services/i.test(text),
      hasCpn: /Consumer Protection Notice/i.test(text),
      hasEho: /Equal Housing\s+Opportunity/i.test(text),
      impliesBroker: /\b(Sophia[^.\n]{0,40}\b(Realty|Brokerage|Company|Owner|Broker)\b)/i.test(text),
      guidesOn: document.body.classList.contains('guides'),
    };
  });
}

(async () => {
  fs.mkdirSync(OUT_DIR, { recursive: true });
  fs.mkdirSync(PREVIEW_DIR, { recursive: true });
  const browser = await chromium.launch();
  const ctx = await browser.newContext({ viewport: { width: W, height: H }, deviceScaleFactor: SCALE });
  const previewCtx = await browser.newContext({ viewport: { width: W, height: H }, deviceScaleFactor: 1 });
  let failures = 0;

  for (const dir of flyers) {
    const name = dir.replace(/^\d+_/, '');
    const html = path.join(FLYERS_DIR, dir, 'flyer.html');
    const png = path.join(OUT_DIR, `${name}_LETTER_BLEED_300dpi.png`);
    const pdf = path.join(OUT_DIR, `${name}_LETTER_BLEED.pdf`);
    console.log(`rendering ${dir} ...`);

    const page = await ctx.newPage();
    page.on('pageerror', (e) => console.warn('  ! page error:', e.message));
    await page.goto('file://' + html, { waitUntil: 'networkidle', timeout: 60000 });
    await page.evaluate(() => document.fonts && document.fonts.ready);
    await page.waitForTimeout(400);

    const box = await (await page.$('body')).boundingBox();
    if (Math.abs(box.width - W) > 1 || Math.abs(box.height - H) > 1) {
      console.warn(`  ! SIZE MISMATCH: body is ${box.width}x${box.height}, expected ${W}x${H}`);
    }

    await page.screenshot({ path: png, clip: { x: 0, y: 0, width: W, height: H } });
    const preview = await previewCtx.newPage();
    await preview.goto('file://' + html, { waitUntil: 'networkidle', timeout: 60000 });
    await preview.evaluate(() => document.fonts && document.fonts.ready);
    await preview.waitForTimeout(300);
    await preview.screenshot({ path: path.join(PREVIEW_DIR, `${name}.png`), clip: { x: 0, y: 0, width: W, height: H } });
    await preview.close();

    await page.pdf({ path: pdf, width: '8.75in', height: '11.25in', printBackground: true, pageRanges: '1', margin: { top: 0, right: 0, bottom: 0, left: 0 } });

    const r = await trecCheck(page);
    const rows = [
      ['broker named (Spirit Real Estate Group)', r.brokerNamed],
      [`broker >= 1/2 largest contact (${r.maxBroker.toFixed(1)}px vs ${r.maxContact.toFixed(1)}px max)`, r.brokerHalfSize],
      ['TREC license # shown', r.hasLicense],
      ['IABS referenced', r.hasIabs],
      ['Consumer Protection Notice referenced', r.hasCpn],
      ['Equal Housing Opportunity', r.hasEho],
      ['does not imply agent is the broker', !r.impliesBroker],
      ['design guides off', !r.guidesOn],
    ];
    for (const [label, ok] of rows) {
      console.log(`  ${ok ? 'PASS' : 'FAIL'}  ${label}`);
      if (!ok) failures++;
    }
    console.log(`  -> ${path.relative(REPO, png)}\n  -> ${path.relative(REPO, pdf)}`);
    await page.close();
  }

  await browser.close();
  if (failures) { console.error(`\n${failures} TREC check(s) failed`); process.exit(1); }
  console.log('\nDONE — all flyers rendered and passed TREC checks');
})().catch((err) => { console.error(err); process.exit(1); });
