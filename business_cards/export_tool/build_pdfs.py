"""Review PDFs of the card and flyer suites, for the broker.

The published galleries came back "Page not found" — the artifact links are
private unless sharing is switched on — so the broker asked for PDFs or images
instead. This builds what he can open with no account and no link:

  Business_Cards_Sophia_Reddehase.pdf   16 pages, one style per page
  Flyers_Sophia_Reddehase.pdf           16 pages, one style per page
  All_Designs_Sophia_Reddehase.pdf      both suites in one document

Every page is US Letter landscape so it prints on ordinary paper, with the
front beside the back at the same scale, the style named, and the trim size
stated — the three things someone approving a print run needs to see at once.

Resolution is a deliberate compromise: 150 DPI pages, which is past what a
screen or an office printer resolves, and keeps all three files inside the
25 MB an email will carry. The 300 DPI press files are unchanged on disk.
"""
import io
import os

from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
CARDS = os.path.join(ROOT, 'print_ready_images', 'v2')
FLYERS = os.path.join(ROOT, 'print_ready_flyers')
OUT = os.path.join(ROOT, 'pdf')

DPI = 150
PAGE = (int(11 * DPI), int(8.5 * DPI))        # Letter landscape: 1650 x 1275
INK, GREY, HAIR = (26, 22, 24), (122, 112, 116), (208, 200, 202)
PAPER = (255, 255, 255)

# slug, display name, trim size as printed
CARD_STYLES = [
    ('Cherry_Checkers', 'Cherry Checkers', '3.5 x 2 in'),
    ('Marshmallow_Pink', 'Marshmallow Pink', '3.5 x 2 in'),
    ('Terracotta_Cobalt', 'Terracotta Cobalt', '3.5 x 2 in'),
    ('Y2K_Sticker_Pop', 'Y2K Sticker Pop', '3.5 x 2 in'),
    ('Sweet_Suite', 'Sweet Suite', '3.5 x 2 in'),
    ('Sage_Checkers', 'Sage Checkers', '3.5 x 2 in'),
    ('Groovy_Waves', 'Groovy Waves', '3.5 x 2 in'),
    ('Warped_Checkers', 'Warped Checkers', '3.5 x 2 in'),
    ('Pink_Gingham', 'Pink Gingham', '3.5 x 2 in'),
    ('Exact_Green_Checks', 'Green Checks', '3.5 x 2 in'),
    ('Exact_Warped_Checks', 'Warped Checks', '3.5 x 2 in'),
    ('Exact_Groovy_Social', 'Groovy Social', '2 x 3.5 in (vertical)'),
    ('Social_Checks', 'Social Checks', '2 x 3.5 in (vertical)'),
    ('Perfect_Place', 'Perfect Place', '2 x 3.5 in (vertical)'),
    ('Chunky_Diagonal', 'Chunky Diagonal', '2 x 3.5 in (vertical)'),
    ('Exact_Gingham_Square', 'Gingham Square', '2.5 x 2.5 in (square)'),
]
FLYER_STYLES = [(s, n, '5.5 x 5.5 in (square)') for s, n, _ in CARD_STYLES]
# the flyer renders de-slug the Y2K style with a lowercase k
FLYER_FILE = {'Y2K_Sticker_Pop': 'Y2k_Sticker_Pop'}

FONT_DIR = os.path.join(ROOT, 'assets', 'fonts')


def font(size, weight='Bold'):
    for name in (f'Poppins-{weight}.ttf', f'Poppins-{weight}.otf'):
        p = os.path.join(FONT_DIR, name)
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    for p in ('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',
              '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'):
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


F_TITLE = font(46, 'Bold')
F_LABEL = font(20, 'Bold')
F_META = font(21, 'Regular')
F_FOOT = font(18, 'Regular')
F_COVER = font(74, 'Bold')
F_COVER_SUB = font(27, 'Regular')

FOOTER = ('Sophia Sky Reddehase  ·  TREC #831516  ·  '
          'Spirit Real Estate Group  ·  Broker: Bryan Bjerke')


def centred(d, y, text, f, fill):
    w = d.textlength(text, font=f)
    d.text(((PAGE[0] - w) / 2, y), text, font=f, fill=fill)


def design_page(src_dir, slug, name, trim, n, total):
    """One style per page: front beside back, matched scale, named and measured."""
    page = Image.new('RGB', PAGE, PAPER)
    d = ImageDraw.Draw(page)

    centred(d, 74, name, F_TITLE, INK)
    centred(d, 137, trim + '  ·  full bleed included', F_META, GREY)

    faces = []
    for suffix in ('FRONT', 'BACK'):
        im = Image.open(os.path.join(src_dir, f'{slug}_{suffix}.png')).convert('RGB')
        faces.append((suffix, im))

    # one scale for both faces so the pair is honestly comparable
    box_w, box_h = 700, 700
    scale = min(min(box_w / im.width, box_h / im.height) for _, im in faces)
    sized = [(lbl, im.resize((max(1, round(im.width * scale)),
                              max(1, round(im.height * scale))), Image.LANCZOS))
             for lbl, im in faces]

    gap = 72
    total_w = sum(im.width for _, im in sized) + gap
    x = (PAGE[0] - total_w) // 2
    band_top, band_bot = 200, PAGE[1] - 132
    for lbl, im in sized:
        y = band_top + (band_bot - band_top - im.height) // 2
        page.paste(im, (x, y))
        d.rectangle([x - 1, y - 1, x + im.width, y + im.height], outline=HAIR, width=1)
        lw = d.textlength(lbl, font=F_LABEL)
        d.text((x + (im.width - lw) / 2, y + im.height + 16), lbl, font=F_LABEL, fill=GREY)
        x += im.width + gap

    d.line([(112, PAGE[1] - 92), (PAGE[0] - 112, PAGE[1] - 92)], fill=HAIR, width=1)
    d.text((112, PAGE[1] - 74), FOOTER, font=F_FOOT, fill=GREY)
    pn = f'{n} of {total}'
    d.text((PAGE[0] - 112 - d.textlength(pn, font=F_FOOT), PAGE[1] - 74), pn, font=F_FOOT, fill=GREY)
    return page


def cover(title, lines):
    page = Image.new('RGB', PAGE, PAPER)
    d = ImageDraw.Draw(page)
    centred(d, 392, title, F_COVER, INK)
    y = 500
    for ln in lines:
        centred(d, y, ln, F_COVER_SUB, GREY)
        y += 46
    d.line([(560, 352), (PAGE[0] - 560, 352)], fill=INK, width=3)
    d.text((112, PAGE[1] - 74), FOOTER, font=F_FOOT, fill=GREY)
    return page


def build(path, pages):
    os.makedirs(OUT, exist_ok=True)
    pages[0].save(path, 'PDF', save_all=True, append_images=pages[1:],
                  resolution=DPI, quality=88, optimize=True)
    return os.path.getsize(path) / 1e6


def suite(src, styles, label):
    n = len(styles)
    return [design_page(src, FLYER_FILE.get(s, s) if src == FLYERS else s, name, trim, i, n)
            for i, (s, name, trim) in enumerate(styles, 1)]


if __name__ == '__main__':
    card_pages = suite(CARDS, CARD_STYLES, 'cards')
    flyer_pages = suite(FLYERS, FLYER_STYLES, 'flyers')

    jobs = [
        ('Business_Cards_Sophia_Reddehase.pdf',
         [cover('Business Card Designs', [
             'Sixteen styles, front and back',
             'Sophia Sky Reddehase  ·  TREC #831516',
             'Spirit Real Estate Group'])] + card_pages),
        ('Flyers_Sophia_Reddehase.pdf',
         [cover('Flyer Designs', [
             'Sixteen styles, front and back',
             '5.5 x 5.5 in square, rounded corners',
             'Sophia Sky Reddehase  ·  TREC #831516'])] + flyer_pages),
        ('All_Designs_Sophia_Reddehase.pdf',
         [cover('Business Cards & Flyers', [
             'Thirty-two designs, front and back',
             'Sophia Sky Reddehase  ·  TREC #831516',
             'Spirit Real Estate Group'])] + card_pages + flyer_pages),
    ]
    for fname, pages in jobs:
        mb = build(os.path.join(OUT, fname), pages)
        print(f'  {fname:44s} {len(pages):3d} pages  {mb:5.2f} MB')
