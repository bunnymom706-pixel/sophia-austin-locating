"""Square flyer versions of all sixteen business cards.

A flyer is not a scaled-up card. The card is 3.75 x 2.25 and the flyer is
square, so the stack has to be recomposed rather than stretched — but every
style keeps its own ground, palette, display face and sticker build, so the
two sets read as one family.

  trim   5.5 x 5.5 in
  file   5.75 x 5.75 in with 0.125in bleed  ->  1725 x 1725 px at 300 DPI
  corner 110px radius, printed as a rounded die-cut

Type scales with the format: the name runs 150px against a 700px logo, a 84px
SPIRIT cap, which is 1.79x — the same ratio the cards carry and inside the
half-size floor in 22 TAC 535.155(a)(2).
"""
import os

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'flyers')
FULL, BLEED, RADIUS = 1725, 37.5, 110
MARGIN = 150                 # content inset from the trim edge
NAME_PX, LOGO_W = 150, 700   # 700 * 0.1194 = 83.6 cap -> 150/83.6 = 1.79x

STAR = ('M20 1 C21.6 12 28 18.4 39 20 C28 21.6 21.6 28 20 39 '
        'C18.4 28 12 21.6 1 20 C12 18.4 18.4 12 20 1 Z')
BURST = ('M50.0,0.0 L59.1,10.0 L71.7,5.0 L75.6,17.9 L89.1,18.8 L86.9,32.2 L98.7,38.9 L91.0,50.0 '
         'L98.7,61.1 L86.9,67.8 L89.1,81.2 L75.6,82.1 L71.7,95.0 L59.1,90.0 L50.0,100.0 L40.9,90.0 '
         'L28.3,95.0 L24.4,82.1 L10.9,81.2 L13.1,67.8 L1.3,61.1 L9.0,50.0 L1.3,38.9 L13.1,32.2 '
         'L10.9,18.8 L24.4,17.9 L28.3,5.0 L40.9,10.0 Z')


# ─────────────────────────────────────────────────────────── grounds
def checks(a, b, cell):
    return f'''  .ground {{
    position: absolute; inset: 0;
    background-color: {b};
    background-image:
      linear-gradient(45deg, {a} 25%, transparent 25%, transparent 75%, {a} 75%),
      linear-gradient(45deg, {a} 25%, transparent 25%, transparent 75%, {a} 75%);
    background-size: {cell * 2}px {cell * 2}px;
    background-position: 0 0, {cell}px {cell}px;
  }}'''


def dots(bg, dot, cell, r):
    return f'''  .ground {{
    position: absolute; inset: 0;
    background-color: {bg};
    background-image: radial-gradient(circle at 50% 50%, {dot} {r}px, rgba(0,0,0,0) {r + 1}px);
    background-size: {cell}px {cell}px;
  }}'''


def gingham(a, b, cell):
    return f'''  /* gingham: two translucent bands crossing, so the overlap reads darker */
  .ground {{
    position: absolute; inset: 0;
    background-color: {b};
    background-image:
      linear-gradient(90deg, {a} 50%, rgba(0,0,0,0) 50%),
      linear-gradient({a} 50%, rgba(0,0,0,0) 50%);
    background-size: {cell * 2}px {cell * 2}px, {cell * 2}px {cell * 2}px;
    opacity: 1;
  }}'''


def plain(bg):
    return f'  .ground {{ position: absolute; inset: 0; background: {bg}; }}'


WARP_SVG = '''    <svg class="ground" width="{F}" height="{F}" viewBox="0 0 {F} {F}" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <pattern id="ck" width="{c2}" height="{c2}" patternUnits="userSpaceOnUse">
          <rect width="{c2}" height="{c2}" fill="{pink}"/>
          <rect width="{c1}" height="{c1}" fill="{orange}"/>
          <rect x="{c1}" y="{c1}" width="{c1}" height="{c1}" fill="{orange}"/>
        </pattern>
        <filter id="wp" x="-25%" y="-25%" width="150%" height="150%"
                filterUnits="objectBoundingBox" primitiveUnits="userSpaceOnUse">
          <feTurbulence type="fractalNoise" baseFrequency="0.0026 0.0034" numOctaves="2" seed="11" result="n"/>
          <feDisplacementMap in="SourceGraphic" in2="n" scale="105" xChannelSelector="R" yChannelSelector="G"/>
        </filter>
      </defs>
      <g filter="url(#wp)"><rect x="-300" y="-300" width="{big}" height="{big}" fill="url(#ck)"/></g>
    </svg>'''

WAVE_SVG = '''    <svg class="ground" width="{F}" height="{F}" viewBox="0 0 {F} {F}" xmlns="http://www.w3.org/2000/svg">
      <rect width="{F}" height="{F}" fill="{bg}"/>
      <path fill="{wave}" d="M0,0 L{F},0 L{F},250 C 1330,360 1000,150 660,270 C 360,376 180,210 0,300 Z"/>
      <path fill="{wave}" d="M0,{F} L{F},{F} L{F},1470 C 1330,1360 1000,1570 660,1450 C 360,1344 180,1510 0,1420 Z"/>
    </svg>'''

DIAG_SVG = '''    <svg class="ground" width="{F}" height="{F}" viewBox="0 0 {F} {F}" xmlns="http://www.w3.org/2000/svg">
      <rect width="{F}" height="{F}" fill="{pink}"/>
      <path fill="{orange}" d="M0,0 L{F},0 L{F},1010 L0,720 Z"/>
      <path fill="{yellow}" d="M0,{F} L0,1480 L400,{F} Z"/>
    </svg>'''

FRAME_SVG = '''    <svg class="ground" width="{F}" height="{F}" viewBox="0 0 {F} {F}" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <pattern id="fr" width="{c2}" height="{c2}" patternUnits="userSpaceOnUse">
          <rect width="{c2}" height="{c2}" fill="{b}"/>
          <rect width="{c1}" height="{c1}" fill="{a}"/>
          <rect x="{c1}" y="{c1}" width="{c1}" height="{c1}" fill="{a}"/>
        </pattern>
      </defs>
      <rect width="{F}" height="{F}" fill="url(#fr)"/>
      <rect x="185" y="185" width="{inner}" height="{inner}" rx="26" fill="{panel}"/>
    </svg>'''

CITY_SVG = '''    <svg class="ground" width="{F}" height="{F}" viewBox="0 0 {F} {F}" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <linearGradient id="sky" x1="0" y1="0" x2="0.3" y2="1">
          <stop offset="0" stop-color="#fff6ea"/><stop offset="1" stop-color="{bg}"/>
        </linearGradient>
      </defs>
      <rect width="{F}" height="{F}" fill="url(#sky)"/>
      <circle cx="1430" cy="250" r="150" fill="#ffe08a" opacity="0.85"/>
      <g fill="{b1}">{blocks}</g>
      <rect x="0" y="1560" width="{F}" height="165" fill="#ffffff" opacity="0.7"/>
    </svg>'''


def city_blocks():
    out, x = [], 40
    hs = [190, 260, 150, 300, 210, 170, 250, 200, 140]
    for i, h in enumerate(hs):
        w = 150 + (i % 3) * 34
        out.append(f'<rect x="{x}" y="{1560 - h}" width="{w}" height="{h}" rx="10"/>')
        x += w + 22
    return ''.join(out)


# ─────────────────────────────────────────────────────────── styles
# key, halo, face -> sticker build | plate, ink, drop -> pills | cream -> logo plate
S = {
 '1_cherry_checkers': dict(
    title='Cherry Checkers', ground=checks('#d91635', '#fff8ee', 143),
    font='Bagel Fat One', caps=False, key='#3a0b14', halo='#fff8ee', face='#a80f27',
    plate='#a30f28', ink='#fff8ee', drop='#6e0819', cream='#fff8ee',
    qr='qr_cherry.png', bfill='#a30f28', bink='#fff8ee', head='#fff8ee', body='#fff8ee', hg='#d91635'),
 '2_marshmallow_pink': dict(
    title='Marshmallow Pink', ground=dots('#ffb8d9', '#fff1f8', 230, 46),
    font='Bagel Fat One', caps=False, key='#5c0c2b', halo='#fff1f8', face='#a3164e',
    plate='#a3164e', ink='#fff1f8', drop='#6d0e34', cream='#fff1f8',
    qr='qr_marshmallow_whitebg.png', bfill='#a3164e', bink='#fff1f8', head='#a3164e', body='#a3164e', hg='#ffb8d9'),
 '3_terracotta_cobalt': dict(
    title='Terracotta Cobalt', ground=checks('#c1502e', '#f3e6d2', 143),
    font='Bagel Fat One', caps=False, key='#0d1730', halo='#f3e6d2', face='#1b2a6b',
    plate='#1b2a6b', ink='#f3e6d2', drop='#0d1730', cream='#f3e6d2',
    qr='qr_terracotta.png', bfill='#1b2a6b', bink='#f3e6d2', head='#f3e6d2', body='#f3e6d2', hg='#c1502e'),
 '4_y2k_sticker_pop': dict(
    title='Y2K Sticker Pop', ground=checks('#e8123c', '#ff8fb3', 115),
    font='Bagel Fat One', caps=False, key='#3d0512', halo='#fff6f0', face='#7a0b24',
    plate='#7d0f2b', ink='#fff6f0', drop='#55071c', cream='#fff6f0',
    qr='qr_y2k.png', bfill='#7d0f2b', bink='#fff6f0', head='#fff6f0', body='#fff6f0', hg='#e8123c'),
 '5_sweet_suite': dict(
    title='Sweet Suite', ground=('city', '#ffd9ec', '#ffc2dd'),
    font='Bagel Fat One', caps=False, key='#5c0c2b', halo='#fff6ea', face='#a3164e',
    plate='#6b2140', ink='#fff6ea', drop='#421327', cream='#fff6ea',
    qr='qr_marshmallow_whitebg.png', bfill='#6b2140', bink='#fff6ea', head='#6b2140', body='#6b2140', hg='#ffd9ec'),
 '6_sage_checkers': dict(
    title='Sage Checkers', ground=checks('#4d6b46', '#f2ebd9', 143),
    font='Bagel Fat One', caps=False, key='#42182f', halo='#f2ebd9', face='#a8386b',
    plate='#33492e', ink='#f2ebd9', drop='#22321f', cream='#f2ebd9',
    qr='qr_sage_dark_on_cream.png', bfill='#a8386b', bink='#f2ebd9', head='#f2ebd9', body='#f2ebd9', hg='#4d6b46'),
 '7_groovy_waves': dict(
    title='Groovy Waves', ground=('waves', '#e8532e', '#f6b4d0'),
    font='Shrikhand', caps=False, flat='#fff6ef',
    plate='#a82d12', ink='#fff6ef', drop='#741e0b', cream='#fff6ef',
    qr='qr_marshmallow_whitebg.png', bfill='#a82d12', bink='#fff6ef', head='#fff6ef', body='#8f2408', hg='#f6b4d0'),
 '8_warped_checkers': dict(
    title='Warped Checkers', ground=('warp', '#f2a3d4', '#e8542c'),
    font='Bagel Fat One', caps=False, key='#2b3d1e', halo='#f7e6c9', face='#7a9b52',
    plate='#2b3d1e', ink='#f7e6c9', drop='#1b2712', cream='#f7e6c9',
    qr='qr_warped_dark_on_pink.png', bfill='#3f5a2c', bink='#f7e6c9', head='#f7e6c9', body='#3f5a2c', hg='#f2a3d4'),
 '9_pink_gingham': dict(
    title='Pink Gingham', ground=gingham('rgba(214,120,134,0.55)', '#f8f3ea', 96),
    font='Alfa Slab One', caps=True, key='#631812', halo='#f8f3ea', face='#b8332a',
    plate='#8a231a', ink='#fbf6ee', drop='#5e1610', cream='#f8f3ea',
    qr='qr_gingham_red_on_cream.png', bfill='#b8332a', bink='#fbf6ee', head='#b8332a', body='#8a231a', hg='#f8f3ea'),
 '10_exact_green_checks': dict(
    title='Green Checks', ground=checks('#4d6b46', '#f2ebd9', 190),
    font='Bagel Fat One', caps=False, key='#42182f', halo='#f2ebd9', face='#a8386b',
    plate='#33492e', ink='#f2ebd9', drop='#22321f', cream='#f2ebd9',
    qr='qr_sage_dark_on_cream.png', bfill='#a8386b', bink='#f2ebd9', head='#f2ebd9', body='#f2ebd9', hg='#4d6b46'),
 '11_exact_groovy_social': dict(
    title='Groovy Social', ground=('waves', '#e8532e', '#f6b4d0'),
    font='Shrikhand', caps=False, flat='#fff6ef',
    plate='#a82d12', ink='#fff6ef', drop='#741e0b', cream='#fff6ef',
    qr='qr_marshmallow_whitebg.png', bfill='#a82d12', bink='#fff6ef', head='#fff6ef', body='#8f2408', hg='#f6b4d0'),
 '12_exact_warped_checks': dict(
    title='Warped Checks', ground=('warp', '#f2a3d4', '#e8542c'),
    font='Bagel Fat One', caps=False, key='#2b3d1e', halo='#f7e6c9', face='#7a9b52',
    plate='#2b3d1e', ink='#f7e6c9', drop='#1b2712', cream='#f7e6c9',
    qr='qr_warped_dark_on_pink.png', bfill='#3f5a2c', bink='#f7e6c9', head='#f7e6c9', body='#3f5a2c', hg='#f2a3d4'),
 '13_exact_gingham_square': dict(
    title='Gingham Square', ground=gingham('rgba(214,120,134,0.55)', '#f8f3ea', 125),
    font='Alfa Slab One', caps=True, key='#631812', halo='#f8f3ea', face='#b8332a',
    plate='#8a231a', ink='#fbf6ee', drop='#5e1610', cream='#f8f3ea',
    qr='qr_gingham_red_on_cream.png', bfill='#b8332a', bink='#fbf6ee', head='#b8332a', body='#8a231a', hg='#f8f3ea'),
 '14_social_checks': dict(
    title='Social Checks', ground=('frame', '#c8102e', '#f9b8cf', '#c8102e'),
    font='Anton', caps=True, flat='#f9b8cf',
    plate='#f9b8cf', ink='#7a0a1e', drop='#560716', cream='#fff3f5',
    qr='qr_cherry.png', bfill='#c8102e', bink='#fff3f5', head='#f9b8cf', body='#fff3f5', hg='#c8102e',
    # this is the one inverted style: its pills are pale pink on a red ground, which
    # works, but the same pale pink as the brokermark's ring and caption sits on a
    # cream plate and vanishes — the mark keeps the red instead
    bmc='#c8102e', bmd='#7a0a1e',
    back=dict(plate='#c8102e', ink='#fff3f5', drop='#7a0a1e')),
 '15_perfect_place': dict(
    title='Perfect Place', ground=plain('#fbd3e2'),
    font='Alfa Slab One', caps=False, flat='#e8532e',
    plate='#a82d12', ink='#fff6ef', drop='#741e0b', cream='#fff6ef',
    qr='qr_marshmallow_whitebg.png', bfill='#e8532e', bink='#fff6ef', head='#e8532e', body='#a82d12', hg='#fbd3e2'),
 '16_chunky_diagonal': dict(
    title='Chunky Diagonal', ground=('diag', '#e8532e', '#f79ad3', '#f5c84a'),
    font='Bagel Fat One', caps=False, key='#8f2408', halo='#fff6ef', face='#f79ad3',
    plate='#8f2408', ink='#fff6ef', drop='#5e1806', cream='#fff6ef',
    qr='qr_marshmallow_whitebg.png', bfill='#8f2408', bink='#fff6ef', head='#fff6ef', body='#8f2408', hg='#f79ad3'),
}


def ground_html(g):
    if isinstance(g, str):
        # a CSS ground still needs an element to paint on
        return '    <div class="ground"></div>', g
    kind = g[0]
    if kind == 'warp':
        return WARP_SVG.format(F=FULL, pink=g[1], orange=g[2], c1=143, c2=286, big=FULL + 600), ''
    if kind == 'waves':
        return WAVE_SVG.format(F=FULL, bg=g[1], wave=g[2]), ''
    if kind == 'diag':
        return DIAG_SVG.format(F=FULL, orange=g[1], pink=g[2], yellow=g[3]), ''
    if kind == 'frame':
        return FRAME_SVG.format(F=FULL, a=g[1], b=g[2], panel=g[3], c1=115, c2=230, inner=FULL - 370), ''
    if kind == 'city':
        return CITY_SVG.format(F=FULL, bg=g[1], b1=g[2], blocks=city_blocks()), ''
    raise ValueError(kind)


def wordmark(d, size, lines, x, ys):
    """Sticker build where the style has one, flat fill where it doesn't."""
    txt = lambda fill: '\n'.join(
        f'          <text x="{x}" y="{y}">{t}</text>' for t, y in zip(lines, ys))
    if 'flat' in d:
        return (f'        <g font-family="{d["font"]}" font-size="{size}" text-anchor="middle" fill="{d["flat"]}">\n'
                f'{txt(d["flat"])}\n        </g>')
    k, h, f = d['key'], d['halo'], d['face']
    sw, hw = round(size * 0.24), round(size * 0.135)
    layers = []
    for stroke, fill, extra in ((k, k, ' opacity="0.22" transform="translate(7,10)"'),
                                (k, k, ''), (h, h, ''), (None, f, '')):
        attrs = f'fill="{fill}"' if stroke is None else \
            f'stroke="{stroke}" stroke-width="{sw if fill == k else hw}" fill="{fill}"'
        layers.append(f'        <g {attrs}{extra}>\n{txt(fill)}\n        </g>')
    return (f'      <g font-family="{d["font"]}" font-size="{size}" text-anchor="middle"\n'
            f'         stroke-linejoin="round" paint-order="stroke">\n' + '\n'.join(layers) + '\n      </g>')


HEAD = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>{title} — Flyer {face}</title>
<link rel="stylesheet" href="../../assets/fonts/fonts.css">
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  /* square flyer: 5.5 x 5.5in trim, 5.75 x 5.75in with bleed, 300 DPI */
  html, body {{ width: {F}px; height: {F}px; overflow: hidden; background: #ffffff; }}
  .flyer {{
    position: relative; width: {F}px; height: {F}px; overflow: hidden;
    border-radius: {R}px; background: {base};
    font-family: 'Poppins', sans-serif;
  }}
  .ground {{ position: absolute; inset: 0; }}
{groundcss}

  .pill {{
    display: inline-block;
    font-family: 'Poppins', sans-serif; font-weight: 700; text-transform: uppercase;
    white-space: nowrap; color: {ink}; background: {plate};
    box-shadow: 0 8px 0 {drop};
  }}
  .role {{ font-size: 38px; letter-spacing: 11px; padding: 19px 46px 21px; border-radius: 22px; }}
  .services {{ font-size: 23px; letter-spacing: 3.6px; padding: 13px 34px 14px; border-radius: 999px; }}

  .brokermark {{
    position: absolute; left: 50%; transform: translateX(-50%); bottom: {bm}px;
    display: flex; flex-direction: column; align-items: center; gap: 8px;
    background: {cream}; border-radius: 28px; padding: 22px 44px 17px;
    box-shadow: 0 0 0 5px {bmc}, 0 9px 0 {bmd};
  }}
  /* {logo}px wide gives an {cap:.0f}px "SPIRIT" cap against the {name}px name — {ratio:.2f}x,
     inside the half-size floor in 22 TAC 535.155(a)(2) */
  .brokermark img {{ width: {logo}px; height: auto; display: block; }}
  .brokermark .line {{
    font-family: 'Poppins', sans-serif; font-weight: 700; font-size: 23px;
    letter-spacing: 1.4px; color: {bmc}; white-space: nowrap;
  }}

  .free {{
    position: absolute; width: 200px; height: 200px; transform: rotate(-12deg);
    display: flex; align-items: center; justify-content: center; text-align: center;
    font-family: 'Poppins', sans-serif; font-weight: 800; font-size: 23px;
    line-height: 1.05; letter-spacing: 0.9px; color: {bink};
    filter: drop-shadow(0 6px 0 rgba(0,0,0,0.18));
  }}
  .free svg {{ position: absolute; inset: 0; width: 100%; height: 100%; fill: {bfill}; }}
  .free span {{ position: relative; }}
  .free b {{ display: block; font-size: 41px; line-height: 1; }}
'''

BM = '''    <div class="brokermark">
      <img src="../../assets/v2/spirit_logo_navy.png" alt="Spirit Real Estate Group, LLC">
      <span class="line">{line}</span>
    </div>
'''
FREE = f'''    <div class="free">
      <svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg"><path d="{BURST}"/></svg>
      <span><b>FREE</b>for renters</span>
    </div>
'''


def head(d, face, extra=''):
    if face == 'back':
        d = {**d, **d.get('back', {})}
    gcss, base = ground_html(d['ground'])[1], ''
    css_ground = d['ground'] if isinstance(d['ground'], str) else ''
    cap = LOGO_W * 0.1194
    return HEAD.format(
        title=d['title'], face=face, F=FULL, R=RADIUS, base=d['hg'],
        groundcss=css_ground, ink=d['ink'], plate=d['plate'], drop=d['drop'],
        cream=d['cream'], logo=LOGO_W, cap=cap, name=NAME_PX, ratio=NAME_PX / cap,
        bm=118, bfill=d['bfill'], bink=d['bink'],
        bmc=d.get('bmc', d['plate']), bmd=d.get('bmd', d['drop'])) + extra


def build_front(k, d):
    gsvg, _ = ground_html(d['ground'])
    lines = (['SOPHIA SKY', 'REDDEHASE'] if d['caps'] else ['sophia sky', 'reddehase'])
    wm = wordmark(d, NAME_PX, lines, 700, [186, 372])
    # the flyer is a wall-and-table read, so the half of the sheet the card never
    # had gets the thing a card can't carry: the offer, then one number to act on
    tag = ['FREE FOR RENTERS'] if d['caps'] else ['free for renters']
    tagline = wordmark(d, 96, tag, 700, [112])
    css = head(d, 'front', '''
  .stack {
    position: absolute; left: 0; right: 0; top: 240px;
    display: flex; flex-direction: column; align-items: center; gap: 28px;
  }
  .stack svg { display: block; }
  .tagline { margin-top: 30px; }
  .cta {
    font-family: 'Poppins', sans-serif; font-weight: 800; font-size: 44px;
    letter-spacing: 3.4px; text-transform: uppercase; white-space: nowrap;
    color: {ink}; background: {plate};
    padding: 25px 54px 27px; border-radius: 26px; box-shadow: 0 9px 0 {drop};
  }
</style>
</head>
'''.replace('{ink}', d['ink']).replace('{plate}', d['plate']).replace('{drop}', d['drop']))
    spark = ''
    if isinstance(d['ground'], str) or d['ground'][0] in ('warp', 'diag', 'waves'):
        spark = (f'    <svg width="{FULL}" height="{FULL}" viewBox="0 0 {FULL} {FULL}" '
                 f'xmlns="http://www.w3.org/2000/svg" style="position:absolute; inset:0;">\n'
                 f'      <g fill="{d["halo"] if "halo" in d else d["flat"]}">\n'
                 f'        <path transform="translate(190,250) scale(2.4)" d="{STAR}"/>\n'
                 f'        <path transform="translate(1420,300) scale(1.7)" d="{STAR}"/>\n'
                 f'        <path transform="translate(1350,1180) scale(2.0)" d="{STAR}"/>\n'
                 f'      </g>\n    </svg>\n\n')
    return css + f'''<body>
  <div class="flyer">
{gsvg}
{spark}    <div class="stack">
      <svg width="1400" height="430" viewBox="0 0 1400 430" xmlns="http://www.w3.org/2000/svg">
{wm}
      </svg>
      <div class="pill role">{'Austin' if k in ('14_social_checks', '15_perfect_place', '16_chunky_diagonal') else 'Texas'} Apartment Locator</div>
      <div class="pill services">Relocation &#183; Second Chance &#183; First-Time Renters &#183; Luxury</div>

      <svg class="tagline" width="1400" height="152" viewBox="0 0 1400 152" xmlns="http://www.w3.org/2000/svg">
{tagline}
      </svg>
      <div class="cta">Call or text (512) 676-1215</div>
    </div>

{BM.format(line='TREC #831516 &nbsp;&#183;&nbsp; SPIRIT REAL ESTATE GROUP, LLC')}  </div>
</body>
</html>
'''


def build_back(k, d):
    d = {**d, **d.get('back', {})}
    gsvg, _ = ground_html(d['ground'])
    css = head(d, 'back', f'''
  /* every back sets its type on one panel rather than on the pattern — the
     grounds here are checks, gingham and warped boards, and small type laid
     straight on those disappears wherever the squares go light */
  .panel {{
    position: absolute; left: 120px; top: 120px; right: 120px; bottom: 120px;
    background: {d['cream']}; border-radius: 60px;
    box-shadow: 0 0 0 6px {d['plate']}, 0 12px 0 {d['drop']};
  }}
  .head {{
    position: absolute; left: 0; right: 0; top: 266px; text-align: center;
    font-family: '{d["font"]}', sans-serif; font-size: 96px; color: {d['plate']};
    letter-spacing: {'2px' if d['caps'] else '0'};
  }}
  .qr {{
    position: absolute; left: 50%; transform: translateX(-50%); top: 398px;
    width: 540px; height: 540px; background: #ffffff; border-radius: 34px;
    display: flex; align-items: center; justify-content: center;
    box-shadow: 0 0 0 5px {d['plate']}, 0 10px 0 {d['drop']};
  }}
  .qr img {{ width: 462px; height: 462px; display: block; }}
  .cta {{
    position: absolute; left: 50%; transform: translateX(-50%); top: 986px;
    font-family: 'Poppins', sans-serif; font-weight: 800; font-size: 31px; letter-spacing: 1.6px;
    text-transform: uppercase; white-space: nowrap; color: {d['ink']}; background: {d['plate']};
    padding: 19px 40px 21px; border-radius: 22px; box-shadow: 0 8px 0 {d['drop']};
  }}
  .contacts {{
    position: absolute; left: 0; right: 0; top: 1104px; text-align: center;
    font-family: 'Poppins', sans-serif; font-weight: 700; font-size: 33px;
    line-height: 1.52; color: {d['plate']};
  }}
  .brokermark {{ bottom: 158px; background: transparent; box-shadow: none; padding: 0; }}
  .free {{ left: 196px; top: 366px; }}
</style>
</head>
''')
    return css + f'''<body>
  <div class="flyer">
{gsvg}
    <div class="panel"></div>

    <div class="head">{'LET&#39;S CONNECT' if d['caps'] else "let's connect"}</div>

    <div class="qr">
      <img src="../../assets/v2/{d['qr']}" alt="QR code linking to Sophia Reddehase&#39;s intake form">
    </div>
    <div class="cta">Fill out my form to get started</div>

    <div class="contacts">
      (512) 676-1215<br>
      sophia.reddehase@spiritre.com<br>
      sparkapt.com/sophia-reddehase
    </div>

{FREE}{BM.format(line='SOPHIA SKY REDDEHASE &nbsp;&#183;&nbsp; TREC #831516')}  </div>
</body>
</html>
'''


count = 0
for k, d in S.items():
    out = os.path.normpath(os.path.join(ROOT, k))
    os.makedirs(out, exist_ok=True)
    open(os.path.join(out, 'front.html'), 'w').write(build_front(k, d))
    open(os.path.join(out, 'back.html'), 'w').write(build_back(k, d))
    count += 2
    print(f'  {k}')

cap = LOGO_W * 0.1194
print(f'\n{count} flyer faces at {FULL}x{FULL} px  (5.5in trim + 0.125in bleed, {RADIUS}px corner)')
print(f'name {NAME_PX}px / SPIRIT cap {cap:.1f}px = {NAME_PX / cap:.2f}x')
