"""Retro pop flyer suite: four US Letter artboards (816 x 1056) for Sophia's Claude Design canvas.

Settled with Sophia on 2026-09-10: polished retro pop, full color, one color pairing per flyer,
a mix of eras, patterns, letterforms and headline shapes, a mix of tones, property photos only,
QR to her public intake form (sparkapt.com/inquiry/sophia-reddehase859, verified by decode).

House rules: no em dashes; brokerage is exactly "Spirit Real Estate Group".
TREC 22 TAC 535.155: the phone (34 px) is the largest contact line; the broker line is 20 px and
the Spirit wordmark inside the 70 px logo reads about 33 px, so both clear the half-size rule.
"""
import json, math, os

HERE = os.path.dirname(os.path.abspath(__file__))
QR_D = open(os.path.join(HERE, 'qr_path.txt'), encoding='utf-8').read().strip()
BODY = "'DM Sans', 'Helvetica Neue', Arial, sans-serif"


# ------------------------------------------------------------------ shared pieces
def fonts_link(families):
    return ('<link rel="stylesheet" href="https://fonts.googleapis.com/css2?'
            + '&amp;'.join('family=' + f for f in families) + '&amp;display=swap">')


def artboard(families, link_color, body_html):
    return ('<!doctype html>\n<html>\n<head>\n  <meta charset="utf-8">\n'
            '  <script src="./support.js"></script>\n</head>\n<body>\n<x-dc>\n'
            '<helmet>\n  ' + fonts_link(families) + '\n  <style>\n'
            '    body { margin: 0; }\n'
            '    a { color: ' + link_color + '; text-decoration: none; }\n'
            '    a:hover { color: ' + link_color + '; text-decoration: underline; }\n'
            '  </style>\n</helmet>\n'
            + body_html +
            '\n</x-dc>\n'
            '<script data-dc-script data-props=\'{"$preview":{"width":816,"height":1056}}\'>\n'
            'class Component extends DCLogic {}\n</script>\n</body>\n</html>\n')


def qr(size):
    return ('<svg viewBox="-40 -40 410 410" width="' + str(size) + '" height="' + str(size) + '" '
            'xmlns="http://www.w3.org/2000/svg" role="img" aria-label="QR code to Sophia\'s free search form" '
            'style="display:block"><rect x="-40" y="-40" width="410" height="410" fill="#FFFFFF"></rect>'
            '<path transform="scale(10)" fill="none" stroke="#1E1A17" stroke-width="1" d="' + QR_D + '"></path></svg>')


def eho(color):
    return ('<svg viewBox="0 0 64 64" width="22" height="22" xmlns="http://www.w3.org/2000/svg" role="img" '
            'aria-label="Equal Housing Opportunity" style="display:block;flex:none">'
            '<path fill="' + color + '" d="M32 4 2 28h8v30h44V28h8L32 4zm0 8.5L47 25v27H17V25l15-12.5z"></path>'
            '<rect fill="' + color + '" x="22" y="31" width="20" height="5"></rect>'
            '<rect fill="' + color + '" x="22" y="41" width="20" height="5"></rect></svg>')


def scallop(bumps, amp, radius, n=288):
    pts = []
    for i in range(n):
        a = 2 * math.pi * i / n
        r = radius + amp * math.cos(bumps * a)
        pts.append('%.2f%% %.2f%%' % (50 + r * math.cos(a), 50 + r * math.sin(a)))
    return 'polygon(' + ','.join(pts) + ')'


def burst_points(n, ro, ri):
    pts = []
    for i in range(2 * n):
        r = ro if i % 2 == 0 else ri
        a = math.pi * i / n - math.pi / 2
        pts.append('%.2f,%.2f' % (50 + r * math.cos(a), 50 + r * math.sin(a)))
    return ' '.join(pts)


def daisy(size, petal, center):
    petals = ''.join('<ellipse cx="50" cy="25" rx="11" ry="22" fill="%s" transform="rotate(%d 50 50)"></ellipse>'
                     % (petal, i * 45) for i in range(8))
    return ('<svg viewBox="0 0 100 100" width="%d" height="%d" xmlns="http://www.w3.org/2000/svg" aria-hidden="true" '
            'style="display:block">%s<circle cx="50" cy="50" r="15" fill="%s"></circle></svg>'
            % (size, size, petals, center))


def wave_path(y0, amp, wavelength, thickness=26, width=860):
    top, bot = [], []
    steps = width // 6
    for i in range(steps + 1):
        x = -22 + i * width / steps
        y = y0 + amp * math.sin(2 * math.pi * x / wavelength)
        top.append((x, y))
        bot.append((x, y + thickness))
    return ('M' + ' L'.join('%.1f %.1f' % p for p in top) + ' L'
            + ' L'.join('%.1f %.1f' % p for p in reversed(bot)) + ' Z')


COMPLIANCE = ('Sophia Sky Reddehase is a Texas real estate sales agent, TREC License #831516, sponsored by '
              'Spirit Real Estate Group. The <strong style="font-weight:700">Information About Brokerage Services</strong> '
              'form and the <strong style="font-weight:700">TREC Consumer Protection Notice</strong> are at trec.texas.gov '
              'and on request. Locating is free to you; the property pays the agent. Pricing and availability subject '
              'to change daily. All specials and effective rents subject to property terms and leasing approval.')


def legal_band(bg, ink, muted):
    return (
        '<div style="flex:none;background:' + bg + ';color:' + ink + ';padding:16px 52px 18px;display:flex;flex-direction:column;gap:10px">'
        '<div style="display:flex;align-items:center;justify-content:space-between;gap:22px">'
        '<div style="display:flex;flex-direction:column;gap:3px">'
        '<div style="font-family:' + BODY + ';font-size:20px;font-weight:700;line-height:1.1;white-space:nowrap">Brokered by Spirit Real Estate Group</div>'
        '<div style="font-family:' + BODY + ';font-size:10px;font-weight:700;letter-spacing:0.16em;text-transform:uppercase;color:' + muted + '">Sponsored sales agent</div>'
        '</div>'
        '<img src="spirit_logo.png" alt="Spirit Real Estate Group" style="height:70px;width:auto;flex:none;display:block">'
        '<div style="display:flex;align-items:center;gap:7px;flex:none">' + eho(muted) +
        '<div style="font-family:' + BODY + ';font-size:9.5px;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;line-height:1.3;color:' + muted + '">Equal Housing<br>Opportunity</div>'
        '</div></div>'
        '<div style="font-family:' + BODY + ';font-size:12px;font-weight:500;line-height:1.42;color:' + muted + ';text-wrap:pretty">' + COMPLIANCE + '</div>'
        '</div>')


def cta(bg, ink, accent, pitch):
    return (
        '<div style="display:flex;align-items:center;gap:26px;background:' + bg + ';color:' + ink + ';border-radius:22px;padding:12px 26px 12px 12px">'
        '<div style="background:#FFFFFF;border-radius:14px;padding:8px;flex:none">' + qr(148) + '</div>'
        '<div style="display:flex;flex-direction:column;gap:6px;min-width:0;text-align:left">'
        '<div style="font-family:' + BODY + ';font-size:14px;font-weight:700;letter-spacing:0.16em;text-transform:uppercase;color:' + accent + '">' + pitch + '</div>'
        '<div style="font-family:' + BODY + ';font-size:34px;font-weight:700;line-height:1;letter-spacing:-0.01em">(512) 676-1215</div>'
        '<div style="display:flex;flex-direction:column;gap:2px;margin-top:4px">'
        '<div style="font-family:' + BODY + ';font-size:24px;font-weight:700;line-height:1.1">Sophia Sky Reddehase</div>'
        '<div style="font-family:' + BODY + ';font-size:11px;font-weight:700;letter-spacing:0.14em;text-transform:uppercase">Apartment Locator &middot; Austin, Texas &middot; TREC #831516</div>'
        '<div style="font-family:' + BODY + ';font-size:12px;font-weight:500;white-space:nowrap">sparkapt.com/inquiry/sophia-reddehase859 &middot; sophia.reddehase@spiritre.com</div>'
        '</div></div></div>')


DMS = 'DM+Sans:wght@500;700'

# ------------------------------------------ 1 TEAR-OFF: cherry red + cream, 60s mod, checker trim
RED, CREAM, BUTTER, CHOC = '#D7263D', '#FFF1DC', '#F6C94C', '#3A1F17'
BLOCK = "'Big Shoulders Display', Impact, 'Arial Narrow', sans-serif"
tabs = []
for i in range(10):
    border = '' if i == 9 else 'border-right:1.5px dashed ' + CHOC + '66;'
    tabs.append(
        '<div style="display:flex;align-items:center;justify-content:center;' + border + '">'
        '<div style="writing-mode:vertical-rl;transform:rotate(180deg);display:flex;flex-direction:column;align-items:center;gap:4px">'
        '<span style="font-family:' + BODY + ';font-size:16px;font-weight:700;color:' + CHOC + ';white-space:nowrap">(512) 676-1215</span>'
        '<span style="font-family:' + BODY + ';font-size:8px;font-weight:700;letter-spacing:0.08em;text-transform:uppercase;color:#B01E30;white-space:nowrap">Sophia Reddehase</span>'
        '<span style="font-family:' + BODY + ';font-size:8px;font-weight:500;letter-spacing:0.06em;text-transform:uppercase;color:' + CHOC + ';white-space:nowrap">Spirit Real Estate Group</span>'
        '</div></div>')

tear = f'''<div style="position:relative;width:816px;height:1056px;overflow:hidden;background:{RED};display:flex;flex-direction:column;font-family:{BODY}">
  <div style="height:26px;flex:none;background:repeating-conic-gradient({CREAM} 0% 25%, {RED} 0% 50%) 0 0 / 52px 52px"></div>
  <div style="position:relative;flex:1;min-height:0;display:flex;flex-direction:column;padding:28px 52px 22px">
    <div style="display:flex;gap:28px;align-items:flex-start">
      <div style="flex:1;min-width:0;display:flex;flex-direction:column;gap:10px">
        <div style="font-size:14px;font-weight:700;letter-spacing:0.24em;text-transform:uppercase;color:{CREAM}">Austin, Texas</div>
        <h1 style="margin:0;font-family:{BLOCK};font-weight:900;text-transform:uppercase;line-height:0.86;letter-spacing:0.004em;color:{CREAM}"><span style="display:block;font-size:146px;color:{BUTTER}">Free</span><span style="display:block;font-size:84px">Apartment</span><span style="display:block;font-size:84px">Locating</span></h1>
      </div>
      <div style="flex:none;width:300px;height:340px;border-radius:150px 150px 0 0;overflow:hidden;border:8px solid {CREAM};box-sizing:border-box"><img src="tear_arch.jpg" alt="Poolside lounge chairs" style="width:100%;height:100%;object-fit:cover;display:block"></div>
    </div>
    <p style="margin:34px 0 0;font-size:24px;font-weight:500;line-height:1.3;color:{CREAM};text-wrap:pretty">Tell me what you want. I'll send a shortlist.</p>
    <div style="margin-top:auto">{cta(BUTTER, CHOC, '#B01E30', 'Scan for your free search')}</div>
  </div>
  {legal_band(CREAM, CHOC, '#6B4A3C')}
  <div style="flex:none;height:146px;display:grid;grid-template-columns:repeat(10,minmax(0,1fr));border-top:1.5px dashed {CHOC}66;background:{CREAM}">{''.join(tabs)}</div>
</div>'''

# ------------------------------------ 2 FREE LOCATING (Main): pink + orange, 70s groovy, stripes
PINK, PINK2, TANG, CREAM2, PLUM = '#F6A6D6', '#F9BFE2', '#F05A22', '#FFF3E2', '#5B1433'
GROOVY = "Shrikhand, 'Cooper Black', Georgia, serif"
SQUIG = 'M8 58 C 38 6, 74 6, 96 46 S 146 104, 176 58 S 222 4, 252 42 S 300 96, 330 52'

free = f'''<div style="position:relative;width:816px;height:1056px;overflow:hidden;background:repeating-linear-gradient(90deg, {PINK} 0px 36px, {PINK2} 36px 72px);display:flex;flex-direction:column;font-family:{BODY}">
  <div style="position:relative;flex:1;min-height:0;display:flex;flex-direction:column;padding:42px 52px 22px">
    <div style="font-size:14px;font-weight:700;letter-spacing:0.22em;text-transform:uppercase;color:{PLUM}">Free apartment locating &middot; Austin</div>
    <h1 style="margin:14px 0 0;font-family:{GROOVY};font-weight:400;line-height:0.98;transform:rotate(-4deg);transform-origin:0 60%"><span style="display:block;font-size:90px;color:{TANG};text-shadow:5px 5px 0 {PLUM}">Pad hunting?</span><span style="display:block;font-size:64px;color:{PLUM};margin-left:64px">Let me do it.</span></h1>
    <div style="position:relative;height:372px;margin-top:26px;flex:none">
      <div style="position:absolute;right:14px;top:4px;width:390px;background:#FFFFFF;padding:12px 12px 40px;box-sizing:border-box;transform:rotate(4deg);box-shadow:0 10px 0 rgba(91,20,51,0.2)">
        <img src="free_pool.jpg" alt="Courtyard pool" style="width:100%;height:316px;object-fit:cover;display:block">
        <div style="position:absolute;left:0;right:0;bottom:13px;text-align:center;font-size:12px;font-weight:700;letter-spacing:0.18em;text-transform:uppercase;color:{PLUM}">Courtyard pool</div>
      </div>
      <div style="position:absolute;left:36px;top:64px;width:270px;background:#FFFFFF;padding:10px 10px 36px;box-sizing:border-box;transform:rotate(-6deg);box-shadow:0 10px 0 rgba(91,20,51,0.2)">
        <img src="free_kitchen.jpg" alt="Kitchen with island" style="width:100%;height:250px;object-fit:cover;display:block">
        <div style="position:absolute;left:0;right:0;bottom:11px;text-align:center;font-size:12px;font-weight:700;letter-spacing:0.18em;text-transform:uppercase;color:{PLUM}">Chef's kitchen</div>
      </div>
    </div>
    <div style="margin-top:auto">{cta(TANG, CREAM2, PLUM, 'Free for you. Scan to start.')}</div>
  </div>
  {legal_band(CREAM2, PLUM, '#7A3A55')}
</div>'''

# ------------------------------------------ 3 RELOCATION: orange + lilac, groovy waves, soft serif
LILAC, TANG3, CREAM3, INDIGO = '#C9A7EB', '#F26B21', '#FFF4E6', '#2E2359'
SERIF = "'Young Serif', Georgia, 'Times New Roman', serif"

reloc = f'''<div style="position:relative;width:816px;height:1056px;overflow:hidden;background:{LILAC};display:flex;flex-direction:column;font-family:{BODY}">
  <svg viewBox="0 0 816 220" width="816" height="220" xmlns="http://www.w3.org/2000/svg" aria-hidden="true" style="position:absolute;left:0;top:222px;display:block"><path d="{wave_path(34, 18, 272)}" fill="{TANG3}"></path><path d="{wave_path(84, 18, 272)}" fill="{CREAM3}"></path><path d="{wave_path(134, 18, 272)}" fill="{TANG3}"></path></svg>
  <div style="position:relative;z-index:2;flex:1;min-height:0;display:flex;flex-direction:column;align-items:center;padding:30px 52px 22px;text-align:center">
    <div style="position:relative;width:460px;height:440px;flex:none">
      <svg viewBox="0 0 460 116" width="460" height="116" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Relocating to Austin" style="position:absolute;left:0;top:-36px;display:block"><path id="relocArc" d="M 40 110 A 260 260 0 0 1 420 110" fill="none"></path><text style="font-family:{BODY};font-size:22px;font-weight:700;letter-spacing:6px" fill="{INDIGO}"><textPath href="#relocArc" startOffset="50%" text-anchor="middle">RELOCATING TO AUSTIN</textPath></text></svg>
      <div style="position:absolute;left:45px;top:70px;width:370px;height:370px;border-radius:50%;overflow:hidden;border:12px solid {CREAM3};box-sizing:border-box"><img src="reloc_circle.jpg" alt="Furnished model living room" style="width:100%;height:100%;object-fit:cover;display:block"></div>
      <div style="position:absolute;left:0px;top:302px;transform:rotate(-14deg)">{daisy(124, TANG3, CREAM3)}</div>
    </div>
    <h1 style="margin:14px 0 0;font-family:{SERIF};font-weight:400;font-size:60px;line-height:1.02;color:{INDIGO};text-wrap:balance">Moving to Austin?<br><span style="color:{TANG3}">I've got you.</span></h1>
    <p style="margin:12px 0 0;font-size:21px;font-weight:500;line-height:1.3;color:{INDIGO}">Video tours, local advice, keys when you land.</p>
    <div style="margin-top:auto;width:100%">{cta(INDIGO, CREAM3, TANG3, 'Relocating? Scan to start.')}</div>
  </div>
  {legal_band(CREAM3, INDIGO, '#5A4F7A')}
</div>'''

# ------------------------------------ 4 MOVE SEASON: tomato red + hot pink, scalloped badge, fat type
RED4, HOT, BLUSH, MAROON = '#E8332A', '#F25CA2', '#FFE3EC', '#5A0F24'
FAT = "'Titan One', 'Arial Black', Impact, sans-serif"

move = f'''<div style="position:relative;width:816px;height:1056px;overflow:hidden;background:{RED4};display:flex;flex-direction:column;font-family:{BODY}">
  <div style="position:relative;flex:1;min-height:0;display:flex;flex-direction:column;padding:38px 52px 22px">
    <div style="position:relative;height:410px;flex:none">
      <div style="position:absolute;left:0;top:0;width:410px;height:410px;background:{HOT};clip-path:{scallop(20, 3.0, 46.5)};display:flex;align-items:center;justify-content:center;padding-right:80px;box-sizing:border-box">
        <div style="transform:rotate(-6deg);display:flex;flex-direction:column;align-items:center;gap:8px;text-align:center">
          <div style="font-family:{BODY};font-size:14px;font-weight:700;letter-spacing:0.22em;text-transform:uppercase;color:{MAROON}">Austin, Texas</div>
          <div style="font-family:{FAT};font-size:56px;line-height:0.92;color:{MAROON};text-transform:uppercase">Lease<br>ending?</div>
        </div>
      </div>
      <div style="position:absolute;right:0;top:14px;width:382px;height:382px">
        <div style="position:absolute;left:0;top:0;width:382px;height:382px;background:{BLUSH};clip-path:{scallop(22, 2.6, 47.5)}"></div>
        <img src="move_scallop.jpg" alt="Arched facade over a resident courtyard" style="position:absolute;left:16px;top:16px;width:350px;height:350px;object-fit:cover;display:block;clip-path:{scallop(22, 2.6, 46.0)}">
        <div style="position:absolute;right:-8px;top:-8px;width:114px;height:114px;transform:rotate(12deg)">
          <svg viewBox="0 0 100 100" width="114" height="114" xmlns="http://www.w3.org/2000/svg" aria-hidden="true" style="position:absolute;left:0;top:0;display:block"><polygon points="{burst_points(14, 50, 40)}" fill="{MAROON}"></polygon></svg>
          <div style="position:absolute;left:0;top:0;width:114px;height:114px;display:flex;align-items:center;justify-content:center;font-family:{FAT};font-size:26px;color:{BLUSH}">FREE</div>
        </div>
      </div>
    </div>
    <h1 style="margin:62px 0 0;font-family:{FAT};font-weight:400;font-size:58px;line-height:1;color:{BLUSH};text-shadow:4px 4px 0 {MAROON}">Don't just renew.</h1>
    <p style="margin:12px 0 0;font-size:22px;font-weight:500;line-height:1.3;color:{BLUSH}">See what your rent gets you across Austin this month.</p>
    <div style="margin-top:auto">{cta(MAROON, BLUSH, HOT, 'Before you renew, scan here')}</div>
  </div>
  {legal_band(BLUSH, MAROON, '#8A3B53')}
</div>'''

# ------------------------------------------------------------------ write
OUT = {
    'TearOff.dc.html': artboard(['Big+Shoulders+Display:wght@900', DMS], '#B01E30', tear),
    'Main.dc.html': artboard(['Shrikhand', DMS], PLUM, free),
    'Relocation.dc.html': artboard(['Young+Serif', DMS], INDIGO, reloc),
    'MoveSeason.dc.html': artboard(['Titan+One', DMS], MAROON, move),
}
for name, html in OUT.items():
    assert '—' not in html and '&mdash;' not in html, 'em dash in ' + name
    assert 'Spirit Real Estate Group,' not in html and 'LLC' not in html, 'brokerage name in ' + name
    assert 'sparkapt.com/inquiry/sophia-reddehase859' in html and 'TREC #831516' in html
    assert 'Information About Brokerage Services' in html and 'Consumer Protection Notice' in html
    with open(os.path.join(HERE, name), 'w', encoding='utf-8') as f:
        f.write(html)
    print('  ok', name, len(html), 'chars')

canvas = {
    "artboards": [
        {"file": "TearOff.dc.html", "x": 0, "y": 0, "w": 816, "h": 1056, "title": "Tear-off", "print": "fixed"},
        {"file": "Main.dc.html", "x": 916, "y": 0, "w": 816, "h": 1056, "title": "Free locating", "print": "fixed"},
        {"file": "Relocation.dc.html", "x": 1832, "y": 0, "w": 816, "h": 1056, "title": "Relocation", "print": "fixed"},
        {"file": "MoveSeason.dc.html", "x": 2748, "y": 0, "w": 816, "h": 1056, "title": "Move season", "print": "fixed"},
    ],
    "annotations": [
        {"id": "print-spec", "x": 0, "y": -150, "w": 760,
         "text": "US Letter trim, 8.5 x 11 in at 96 px per inch. Export PDF prints each artboard as one page. For Canva Print add a 0.125 in bleed on all four sides. The QR on every flyer opens sparkapt.com/inquiry/sophia-reddehase859."}
    ],
    "launch": {"view": "canvas"},
}
with open(os.path.join(HERE, 'canvas.json'), 'w', encoding='utf-8') as f:
    json.dump(canvas, f, indent=2)
print('wrote canvas.json')
