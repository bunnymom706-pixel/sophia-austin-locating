"""Canva Print prep: stamp 300 DPI metadata on the print PNGs and write JPG copies into print_ready/canva/.
Canva reads the DPI tag to size the upload to 8.75 x 11.25 in (US Letter + 0.125 in bleed) automatically.
Run after export.js:  python flyers/export_tool/canva_prep.py
"""
import os, glob
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
PR = os.path.join(HERE, '..', 'print_ready')
OUT = os.path.join(PR, 'canva'); os.makedirs(OUT, exist_ok=True)
for png in sorted(glob.glob(os.path.join(PR, '*_LETTER_BLEED_300dpi.png'))):
    im = Image.open(png)
    assert im.size == (2625, 3375), (png, im.size)
    im.save(png, dpi=(300, 300), optimize=True)
    jpg = os.path.join(OUT, os.path.basename(png).replace('_300dpi.png', '_300dpi.jpg'))
    im.convert('RGB').save(jpg, quality=95, dpi=(300, 300), subsampling=0)
    print(os.path.basename(png), '-> 300 dpi tag set;', os.path.relpath(jpg, PR), os.path.getsize(jpg) // 1024, 'KB')
