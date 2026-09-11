"""Render every card and flyer face to PNG with desktop Chrome (Playwright, channel="chrome").
usage: python render_faces.py <business_cards dir> <out dir> [<reference business_cards dir>]
Out dir mirrors print_ready_images/v2 and print_ready_flyers. With a reference dir, each render is
diffed against the reference PNG of the same name and the largest differences are printed."""
import os, re, sys
from PIL import Image, ImageChops, ImageStat
from playwright.sync_api import sync_playwright

BC, OUT = sys.argv[1], sys.argv[2]
REF = sys.argv[3] if len(sys.argv) > 3 else None
KINDS = [('cards_v2', 'print_ready_images/v2', False), ('flyers', 'print_ready_flyers', True)]

def slug(d, flyer):
    s = '_'.join(p.capitalize() for p in d.split('_')[1:])
    return s if flyer else s.replace('Y2k', 'Y2K')

jobs = []
for sub, outsub, flyer in KINDS:
    for d in sorted(os.listdir(os.path.join(BC, sub)), key=lambda x: int(x.split('_')[0])):
        for face in ('front', 'back'):
            html = os.path.join(BC, sub, d, face + '.html')
            m = re.search(r'html,\s*body\s*\{[^}]*?width:\s*(\d+)px;\s*height:\s*(\d+)px', open(html, encoding='utf-8').read())
            name = f'{slug(d, flyer)}_{face.upper()}.png'
            jobs.append((os.path.abspath(html), os.path.join(OUT, outsub, name),
                         os.path.join(REF, outsub, name) if REF else None, int(m.group(1)), int(m.group(2))))

worst = []
with sync_playwright() as p:
    b = p.chromium.launch(channel='chrome')
    for html, out, ref, w, h in jobs:
        os.makedirs(os.path.dirname(out), exist_ok=True)
        transparent = False
        if ref and os.path.exists(ref):
            r = Image.open(ref)
            transparent = r.mode == 'RGBA' and r.getpixel((0, 0))[3] == 0
        pg = b.new_page(viewport={'width': w, 'height': h}, device_scale_factor=1)
        pg.goto(__import__('pathlib').Path(html).as_uri(), wait_until='networkidle')
        pg.evaluate('document.fonts.ready')
        pg.wait_for_timeout(400)
        pg.screenshot(path=out, clip={'x': 0, 'y': 0, 'width': w, 'height': h}, omit_background=transparent)
        pg.close()
        if ref and os.path.exists(ref):
            a, r = Image.open(out).convert('RGB'), Image.open(ref).convert('RGB')
            if a.size != r.size:
                worst.append((999, os.path.basename(out), f'size {a.size} vs {r.size}'))
                continue
            diff = ImageChops.difference(a, r)
            mad = sum(ImageStat.Stat(diff).mean) / 3
            worst.append((mad, f'{os.path.basename(os.path.dirname(out))}/{os.path.basename(out)}', diff.getbbox()))
    b.close()
print(f'rendered {len(jobs)} faces -> {OUT}')
for mad, n, bbox in sorted(worst, reverse=True)[:12]:
    print(f'  mean abs diff {mad:7.3f}  {n}  bbox {bbox}')
