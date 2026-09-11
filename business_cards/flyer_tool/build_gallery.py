"""The flyer gallery: every flyer, nothing else.

Same treatment as the card page — no headings, no captions. Sixteen rows, each
one style's front beside its back, on a quiet ground so sixteen loud designs can
sit together without fighting. The flyers are square, so every row is the same
shape and the page reads as one grid rather than a mixed set.
"""
import base64
import io
import os

from PIL import Image

SRC = '/home/user/sophia-austin-locating/business_cards/print_ready_flyers'
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'flyer_gallery.html')

STYLES = [
    'Cherry_Checkers', 'Marshmallow_Pink', 'Terracotta_Cobalt', 'Y2k_Sticker_Pop',
    'Sweet_Suite', 'Sage_Checkers', 'Groovy_Waves', 'Warped_Checkers',
    'Pink_Gingham', 'Exact_Green_Checks', 'Exact_Warped_Checks', 'Exact_Groovy_Social',
    'Social_Checks', 'Perfect_Place', 'Chunky_Diagonal', 'Exact_Gingham_Square',
]
W = 560


def embed(slug, face):
    im = Image.open(os.path.join(SRC, f'{slug}_{face}.png')).convert('RGB')
    im = im.resize((W, W), Image.LANCZOS).quantize(colors=200, method=Image.MEDIANCUT)
    buf = io.BytesIO()
    im.save(buf, format='PNG', optimize=True)
    return base64.b64encode(buf.getvalue()).decode()


rows = []
for slug in STYLES:
    faces = '\n      '.join(
        f'<img src="data:image/png;base64,{embed(slug, f)}" width="{W}" height="{W}" alt="">'
        for f in ('FRONT', 'BACK'))
    rows.append(f'    <div class="pair">\n      {faces}\n    </div>')

html = f'''<title>Sophia Sky Reddehase — Flyers</title>
<style>
  :root {{ --ground: #f4f1ec; --shadow: rgba(28,24,20,0.13); }}
  @media (prefers-color-scheme: dark) {{
    :root:not([data-theme="light"]) {{ --ground: #14131a; --shadow: rgba(0,0,0,0.5); }}
  }}
  :root[data-theme="dark"] {{ --ground: #14131a; --shadow: rgba(0,0,0,0.5); }}

  * {{ box-sizing: border-box; }}
  body {{ margin: 0; background: var(--ground); }}
  main {{
    max-width: 1300px;
    margin: 0 auto;
    padding-block: 72px 96px;
    padding-left: 28px;
    padding-right: 28px;
    display: flex;
    flex-direction: column;
    gap: 68px;
  }}
  .pair {{
    display: flex;
    flex-wrap: wrap;
    gap: 30px;
    justify-content: center;
    align-items: flex-start;
  }}
  .pair img {{
    display: block;
    max-width: 100%;
    height: auto;
    border-radius: 36px;
    box-shadow: 0 3px 10px var(--shadow), 0 14px 38px var(--shadow);
  }}
  @media (max-width: 720px) {{
    main {{ padding-block: 40px 60px; padding-left: 16px; padding-right: 16px; gap: 44px; }}
    .pair {{ gap: 20px; }}
    .pair img {{ border-radius: 24px; }}
  }}
</style>

<main>
{chr(10).join(rows)}
</main>
'''

open(OUT, 'w').write(html)
print(f'{OUT}  {len(html) / 1e6:.2f} MB  ({len(STYLES)} styles, {len(STYLES) * 2} faces)')
