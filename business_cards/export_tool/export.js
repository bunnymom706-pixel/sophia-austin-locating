const fs = require('fs');
const path = require('path');
const puppeteer = require('puppeteer-core');

const CHROME = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
const REPO = path.resolve(__dirname, '..', '..');
const CARDS_DIR = path.join(REPO, 'business_cards', 'cards_v2');
const OUT_DIR = path.join(REPO, 'business_cards', 'print_ready_images', 'v2');
const DESKTOP_OUT = 'C:\\Users\\sophi\\Desktop\\Sophia_Business_Cards_HQ\\v2';

const W = 1125, H = 675; // 3.75in x 2.25in @300dpi (incl. 0.125in bleed each side)

const STYLES = [
  { dir: '1_cherry_checkers', name: 'Cherry_Checkers' },
  { dir: '2_marshmallow_pink', name: 'Marshmallow_Pink' },
  { dir: '3_terracotta_cobalt', name: 'Terracotta_Cobalt' },
  { dir: '4_y2k_sticker_pop', name: 'Y2K_Sticker_Pop' },
];

async function shot(browser, htmlPath, outPng) {
  const page = await browser.newPage();
  await page.setViewport({ width: W, height: H, deviceScaleFactor: 1 }); // exact 1125x675px = 300dpi at 3.75x2.25in
  await page.goto('file:///' + htmlPath.replace(/\\/g, '/'), { waitUntil: 'networkidle0', timeout: 30000 });
  await page.evaluate(() => document.fonts && document.fonts.ready);
  await new Promise(r => setTimeout(r, 300));
  const body = await page.$('body');
  const box = await body.boundingBox();
  if (Math.abs(box.width - W) > 2 || Math.abs(box.height - H) > 2) {
    console.warn(`  ! SIZE MISMATCH ${outPng}: body is ${box.width}x${box.height}, expected ${W}x${H}`);
  }
  await page.screenshot({ path: outPng, clip: { x: 0, y: 0, width: W, height: H } });
  await page.close();
}

(async () => {
  fs.mkdirSync(OUT_DIR, { recursive: true });
  fs.mkdirSync(DESKTOP_OUT, { recursive: true });

  const browser = await puppeteer.launch({ executablePath: CHROME, headless: 'new' });

  for (const style of STYLES) {
    const frontHtml = path.join(CARDS_DIR, style.dir, 'front.html');
    const backHtml = path.join(CARDS_DIR, style.dir, 'back.html');
    const frontPng = path.join(OUT_DIR, `${style.name}_FRONT.png`);
    const backPng = path.join(OUT_DIR, `${style.name}_BACK.png`);
    console.log(`rendering ${style.dir} ...`);
    await shot(browser, frontHtml, frontPng);
    await shot(browser, backHtml, backPng);
    fs.copyFileSync(frontPng, path.join(DESKTOP_OUT, path.basename(frontPng)));
    fs.copyFileSync(backPng, path.join(DESKTOP_OUT, path.basename(backPng)));
    console.log(`  -> ${frontPng}`);
    console.log(`  -> ${backPng}`);
  }

  await browser.close();
  console.log('DONE');
})().catch(err => { console.error(err); process.exit(1); });
