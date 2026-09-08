const fs = require('fs');
const path = require('path');
const puppeteer = require('puppeteer-core');

const CHROME = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
const REPO = path.resolve(__dirname, '..', '..');
const CARDS_DIR = path.join(REPO, 'business_cards', 'cards_v2');
const OUT_DIR = path.join(REPO, 'business_cards', 'print_ready_images', 'v2');
const DESKTOP_OUT = 'C:\\Users\\sophi\\Desktop\\Sophia_Business_Cards_HQ\\v2';

// All sizes are 300dpi and include 0.125in bleed on each side.
const LANDSCAPE = { w: 1125, h: 675 };  // trims to 3.5 x 2.0in
const PORTRAIT  = { w: 675, h: 1125 };  // trims to 2.0 x 3.5in
const SQUARE    = { w: 825, h: 825 };   // trims to 2.5 x 2.5in

const STYLES = [
  { dir: '1_cherry_checkers', name: 'Cherry_Checkers', size: LANDSCAPE },
  { dir: '2_marshmallow_pink', name: 'Marshmallow_Pink', size: LANDSCAPE },
  { dir: '3_terracotta_cobalt', name: 'Terracotta_Cobalt', size: LANDSCAPE },
  { dir: '4_y2k_sticker_pop', name: 'Y2K_Sticker_Pop', size: LANDSCAPE },
  { dir: '5_sweet_suite', name: 'Sweet_Suite', size: LANDSCAPE },
  { dir: '6_sage_checkers', name: 'Sage_Checkers', size: LANDSCAPE },
  { dir: '7_groovy_waves', name: 'Groovy_Waves', size: LANDSCAPE },
  { dir: '8_warped_checkers', name: 'Warped_Checkers', size: LANDSCAPE },
  { dir: '9_pink_gingham', name: 'Pink_Gingham', size: LANDSCAPE },
  { dir: '10_exact_green_checks', name: 'Exact_Green_Checks', size: LANDSCAPE },
  { dir: '11_exact_groovy_social', name: 'Exact_Groovy_Social', size: PORTRAIT },
  { dir: '12_exact_warped_checks', name: 'Exact_Warped_Checks', size: LANDSCAPE },
  { dir: '13_exact_gingham_square', name: 'Exact_Gingham_Square', size: SQUARE },
];

async function shot(browser, htmlPath, outPng, size) {
  const { w: W, h: H } = size;
  const page = await browser.newPage();
  await page.setViewport({ width: W, height: H, deviceScaleFactor: 1 });
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
    await shot(browser, frontHtml, frontPng, style.size);
    await shot(browser, backHtml, backPng, style.size);
    fs.copyFileSync(frontPng, path.join(DESKTOP_OUT, path.basename(frontPng)));
    fs.copyFileSync(backPng, path.join(DESKTOP_OUT, path.basename(backPng)));
    console.log(`  -> ${frontPng}`);
    console.log(`  -> ${backPng}`);
  }

  await browser.close();
  console.log('DONE');
})().catch(err => { console.error(err); process.exit(1); });
