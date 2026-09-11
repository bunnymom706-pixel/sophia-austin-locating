"""Print-ready PDFs: one file per design, front and back as its two pages.

Each page is the 300 DPI render placed losslessly at its true physical size,
trim plus 0.125 in bleed on every side, so a print shop can use it unscaled:

  landscape card  3.75 x 2.25 in      vertical card  2.25 x 3.75 in
  square card     2.75 x 2.75 in      square flyer   5.75 x 5.75 in

Writes business_cards/pdf/print/cards/ and business_cards/pdf/print/flyers/.
"""
import io
import os

import pymupdf
from PIL import Image

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
JOBS = [
    (os.path.join(ROOT, 'print_ready_images', 'v2'), os.path.join(ROOT, 'pdf', 'print', 'cards'), 'Card'),
    (os.path.join(ROOT, 'print_ready_flyers'), os.path.join(ROOT, 'pdf', 'print', 'flyers'), 'Flyer'),
]
DPI = 300


def flat_png(path):
    im = Image.open(path)
    if im.mode != 'RGB':
        im = im.convert('RGBA')
        bg = Image.new('RGB', im.size, (255, 255, 255))
        bg.paste(im, mask=im.split()[3])
        im = bg
    buf = io.BytesIO()
    im.save(buf, 'PNG')
    return im.size, buf.getvalue()


if __name__ == '__main__':
    for src, out, kind in JOBS:
        os.makedirs(out, exist_ok=True)
        styles = sorted({f[:-len('_FRONT.png')] for f in os.listdir(src) if f.endswith('_FRONT.png')})
        for style in styles:
            doc = pymupdf.open()
            for face in ('FRONT', 'BACK'):
                (w, h), data = flat_png(os.path.join(src, f'{style}_{face}.png'))
                page = doc.new_page(width=w / DPI * 72, height=h / DPI * 72)
                page.insert_image(page.rect, stream=data)
            name = f'{style.replace("Y2k", "Y2K")}_{kind}_Sophia_Reddehase.pdf'
            doc.save(os.path.join(out, name), deflate=True, garbage=3)
            doc.close()
            print(f'  {name:54s} {w / DPI:.2f} x {h / DPI:.2f} in')
