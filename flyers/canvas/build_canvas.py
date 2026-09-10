"""Builds the four Design Component artboards for Sophia's flyer canvas.

Editorial system, US Letter trim at 96 px/in (816 x 1056).
Type: Instrument Serif (display) + Archivo (labels/body), Google Fonts, with close fallbacks.
Palette: warm cream / warm white paper, deep pine and espresso fields, clay and brass accents.
No em dashes anywhere (house rule). TREC: broker line and Spirit wordmark both well above
half the largest contact size (the phone at 34 px).
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
QR_PATH = open(os.path.join(HERE, 'qr_path.txt'), encoding='utf-8').read().strip()

W, H = 816, 1056
PHONE_PX = 34          # largest contact info
BROKER_PX = 22         # 0.65 of the phone
LOGO_H = 78            # wordmark = 47.6% => 37.1 px, 1.09 of the phone

THEMES = {
    'tearoff':  dict(paper='#F5F0E6', ink='#231F1B', accent='#A85B38', stone='#7A7062',
                     rule='#D8D0C0', tint='#EDE6D8', logo='spirit_logo.png', dark=False),
    'free':     dict(paper='#2F5148', ink='#F5F0E6', accent='#C9A961', stone='#A9B8B1',
                     rule='#46655C', tint='#3A5F55', logo='spirit_logo_white.png', dark=True),
    'reloc':    dict(paper='#FCFAF6', ink='#231F1B', accent='#A98A55', stone='#7A7062',
                     rule='#E2DBCC', tint='#F4EFE4', logo='spirit_logo.png', dark=False),
    'move':     dict(paper='#2B2521', ink='#F5F0E6', accent='#B99A5B', stone='#9A9086',
                     rule='#453D36', tint='#332C27', logo='spirit_logo_white.png', dark=True),
}

DISPLAY = "'Instrument Serif', Georgia, 'Times New Roman', serif"
SANS = "Archivo, 'Helvetica Neue', Arial, sans-serif"

HELMET = """<helmet>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&amp;family=Archivo:wght@400;500;600&amp;display=swap">
  <style>
    body { margin: 0; }
    a { color: %s; text-decoration: none; }
    a:hover { color: %s; }
  </style>
</helmet>"""


def qr(size=112):
    """QR to sparkapt.com/inquiry/sophia-reddehase859, with a 4 module quiet zone."""
    return (
        '<svg viewBox="-40 -40 410 410" width="{s}" height="{s}" xmlns="http://www.w3.org/2000/svg" '
        'role="img" aria-label="QR code to Sophia\'s free search form" style="display:block">'
        '<rect x="-40" y="-40" width="410" height="410" fill="#FFFFFF"></rect>'
        '<path transform="scale(10)" fill="none" stroke="#231F1B" stroke-width="1" d="{d}"></path>'
        '</svg>'
    ).format(s=size, d=QR_PATH)


def eho(color):
    return (
        '<svg viewBox="0 0 64 64" width="21" height="21" xmlns="http://www.w3.org/2000/svg" '
        'role="img" aria-label="Equal Housing Opportunity" style="display:block;flex:none">'
        '<path fill="{c}" d="M32 4 2 28h8v30h44V28h8L32 4zm0 8.5L47 25v27H17V25l15-12.5z"></path>'
        '<rect fill="{c}" x="22" y="31" width="20" height="5"></rect>'
        '<rect fill="{c}" x="22" y="41" width="20" height="5"></rect>'
        '</svg>'
    ).format(c=color)


def label(text, t, color=None, size=10.5):
    return (
        '<div style="font-family:{sans};font-size:{sz}px;font-weight:600;letter-spacing:0.26em;'
        'text-transform:uppercase;color:{c}">{t}</div>'
    ).format(sans=SANS, sz=size, c=color or t_get(t, 'accent'), t=text)


def t_get(t, k):
    return THEMES[t][k]


def footer(t):
    th = THEMES[t]
    return """  <div style="margin-top:auto;display:flex;flex-direction:column;gap:0">

    <div style="height:1px;background:{rule}"></div>

    <div style="display:flex;align-items:flex-end;justify-content:space-between;gap:32px;padding:12px 0 10px">
      <div style="display:flex;flex-direction:column;gap:10px;text-align:left">
        <div style="display:flex;flex-direction:column;gap:5px">
          <div style="font-family:{display};font-size:30px;line-height:1;letter-spacing:0.03em;color:{ink}">Sophia Sky Reddehase</div>
          <div style="font-family:{sans};font-size:10px;font-weight:600;letter-spacing:0.24em;text-transform:uppercase;color:{stone}">Apartment Locator &middot; Austin, Texas &middot; TREC #831516</div>
        </div>
        <div style="display:flex;flex-direction:column;gap:3px">
          <div style="font-family:{display};font-size:{phone}px;line-height:1;letter-spacing:0.01em;color:{accent}">(512) 676-1215</div>
          <div style="font-family:{sans};font-size:12px;font-weight:400;letter-spacing:0.005em;color:{stone};white-space:nowrap">sparkapt.com/inquiry/sophia-reddehase859 &nbsp;&middot;&nbsp; sophia.reddehase@spiritre.com</div>
        </div>
      </div>
      <div style="display:flex;flex-direction:column;align-items:center;gap:7px;flex:none">
        <div style="padding:8px;background:#FFFFFF">{qr}</div>
        <div style="font-family:{sans};font-size:9px;font-weight:600;letter-spacing:0.2em;text-transform:uppercase;color:{stone}">Scan to start</div>
      </div>
    </div>

    <div style="height:1px;background:{rule}"></div>

    <div style="display:flex;align-items:center;justify-content:space-between;gap:24px;padding:10px 0 8px">
      <div style="display:flex;flex-direction:column;gap:4px;text-align:left">
        <div style="font-family:{display};font-size:{broker}px;line-height:1.05;letter-spacing:0.015em;color:{ink}">Brokered by Spirit Real Estate Group</div>
        <div style="font-family:{sans};font-size:9.5px;font-weight:600;letter-spacing:0.2em;text-transform:uppercase;color:{stone}">Sponsored sales agent</div>
      </div>
      <img src="{logo}" alt="Spirit Real Estate Group" style="height:{logoh}px;width:auto;flex:none;display:block">
      <div style="display:flex;align-items:center;gap:7px;flex:none">
        {eho}
        <div style="font-family:{sans};font-size:9px;font-weight:600;letter-spacing:0.14em;text-transform:uppercase;line-height:1.35;color:{stone};text-align:left">Equal Housing<br>Opportunity</div>
      </div>
    </div>

    <div style="font-family:{sans};font-size:12px;font-weight:400;line-height:1.45;color:{stone};text-align:left;text-wrap:pretty">Sophia Sky Reddehase is a Texas real estate sales agent, TREC License #831516, sponsored by Spirit Real Estate Group. The <strong style="font-weight:600;color:{ink}">Information About Brokerage Services</strong> form and the <strong style="font-weight:600;color:{ink}">TREC Consumer Protection Notice</strong> are at trec.texas.gov and on request. Locating is free to you; the property pays the agent. Pricing and availability subject to change daily. All specials and effective rents subject to property terms and leasing approval.</div>

  </div>""".format(display=DISPLAY, sans=SANS, ink=th['ink'], stone=th['stone'], rule=th['rule'],
                   accent=th['accent'], phone=PHONE_PX, broker=BROKER_PX, logo=th['logo'],
                   logoh=LOGO_H, qr=qr(160), eho=eho(th['stone']))


def page(t, title, inner, root_extra='', pad='48px 60px 44px'):
    th = THEMES[t]
    return """<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <script src="./support.js"></script>
</head>
<body>
<x-dc>
{helmet}
<div style="position:relative;width:{w}px;height:{h}px;background:{paper};color:{ink};font-family:{sans};overflow:hidden;box-sizing:border-box">
{root_extra}  <div style="position:relative;z-index:2;display:flex;flex-direction:column;height:100%;padding:{pad};box-sizing:border-box">
{inner}
{footer}
  </div>
</div>
</x-dc>
<script data-dc-script data-props='{{"$preview":{{"width":{w},"height":{h}}}}}'>
class Component extends DCLogic {{}}
</script>
</body>
</html>
""".format(helmet=HELMET % (th['accent'], th['ink']), w=W, h=H, paper=th['paper'], ink=th['ink'],
           sans=SANS, pad=pad, inner=inner, footer=footer(t), root_extra=root_extra,
           title=title)


# ---------------------------------------------------------------- 1 tear-off
th = THEMES['tearoff']
tabs = ''.join(
    '<div style="display:flex;align-items:center;justify-content:center;{br}">'
    '<div style="writing-mode:vertical-rl;transform:rotate(180deg);display:flex;flex-direction:column;align-items:center;gap:5px">'
    '<span style="font-family:{d};font-size:16px;letter-spacing:0.01em;color:{ink}">(512) 676-1215</span>'
    '<span style="font-family:{s};font-size:8px;font-weight:600;letter-spacing:0.09em;text-transform:uppercase;color:{ac}">Sophia Reddehase</span>'
    '<span style="font-family:{s};font-size:8px;font-weight:500;letter-spacing:0.07em;text-transform:uppercase;color:{st}">Spirit Real Estate Group</span>'
    '</div></div>'.format(br='' if i == 9 else 'border-right:1px dashed ' + th['rule'],
                          d=DISPLAY, s=SANS, ink=th['ink'], ac=th['accent'], st=th['stone'])
    for i in range(10))

inner1 = """    <div style="display:flex;flex-direction:column;align-items:flex-start;gap:16px">
      {label}
      <h1 style="margin:0;font-family:{display};font-weight:400;font-size:66px;line-height:0.98;letter-spacing:-0.005em;color:{ink};text-wrap:balance">I find it.<br><span style="font-style:italic;color:{accent}">You move in.</span></h1>
    </div>

    <div style="height:1px;background:{rule};margin:22px 0 0"></div>

    <div style="margin-top:20px;overflow:hidden"><img src="pool_clubhouse.jpg" alt="Resort pool and clubhouse deck" style="width:100%;height:168px;object-fit:cover;display:block"></div>

    <p style="margin:22px 0 0;font-family:{display};font-size:23px;line-height:1.35;color:{ink};max-width:660px;text-wrap:pretty">Your search, your tours, your negotiation. <span style="font-style:italic;color:{accent}">Free to you.</span></p>
""".format(label=label('Austin apartment locating', 'tearoff'), display=DISPLAY, sans=SANS,
           ink=th['ink'], accent=th['accent'], rule=th['rule'], stone=th['stone'])

tabs_block = """  <div style="position:absolute;z-index:3;left:60px;right:60px;bottom:30px;height:150px;display:grid;grid-template-columns:repeat(10,minmax(0,1fr));border-top:1px dashed {rule}">{tabs}</div>
""".format(rule=th['rule'], tabs=tabs)

open(os.path.join(HERE, 'TearOff.dc.html'), 'w', encoding='utf-8').write(
    page('tearoff', 'Tear-off flyer', inner1, root_extra=tabs_block, pad='48px 60px 198px'))

# ------------------------------------------------------- 2 free locating (Main)
th = THEMES['free']
hero = """  <div style="position:absolute;left:0;right:0;top:0;height:396px;overflow:hidden">
    <img src="courtyard_pool.jpg" alt="Resort courtyard pool at dusk" style="width:100%;height:100%;object-fit:cover;display:block">
    <div style="position:absolute;inset:0;background:linear-gradient(180deg, rgba(47,81,72,0) 40%, rgba(47,81,72,0.55) 74%, {paper} 100%)"></div>
    <div style="position:absolute;left:60px;right:60px;bottom:34px;display:flex;flex-direction:column;gap:12px">
      {label}
      <h1 style="margin:0;font-family:{display};font-weight:400;font-size:62px;line-height:0.98;letter-spacing:-0.005em;color:#F5F0E6;text-wrap:balance;text-shadow:0 2px 26px rgba(18,32,28,0.55)">Your next place,<br><span style="font-style:italic;color:{accent}">found for you.</span></h1>
    </div>
  </div>
""".format(paper=th['paper'], display=DISPLAY, accent=th['accent'],
           label=label('Free apartment locating &middot; Austin', 'free', color='#F1E4BE'))

inner2 = """    <p style="margin:0;font-family:{display};font-size:24px;line-height:1.35;color:{ink};max-width:700px;text-wrap:pretty">The property pays the locator. <span style="font-style:italic;color:{accent}">My work costs you nothing.</span></p>

    <div style="display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px;margin-top:22px">
      <figure style="margin:0;display:flex;flex-direction:column;gap:9px">
        <div style="overflow:hidden"><img src="kitchen.jpg" alt="Kitchen with quartz island" style="width:100%;height:120px;object-fit:cover;display:block"></div>
        <figcaption style="font-family:{sans};font-size:9.5px;font-weight:600;letter-spacing:0.2em;text-transform:uppercase;color:{stone}">Chef's kitchen</figcaption>
      </figure>
      <figure style="margin:0;display:flex;flex-direction:column;gap:9px">
        <div style="overflow:hidden"><img src="living_room.jpg" alt="Furnished model living room" style="width:100%;height:120px;object-fit:cover;display:block"></div>
        <figcaption style="font-family:{sans};font-size:9.5px;font-weight:600;letter-spacing:0.2em;text-transform:uppercase;color:{stone}">Model residence</figcaption>
      </figure>
      <figure style="margin:0;display:flex;flex-direction:column;gap:9px">
        <div style="overflow:hidden"><img src="lounge.jpg" alt="Resident lounge" style="width:100%;height:120px;object-fit:cover;display:block"></div>
        <figcaption style="font-family:{sans};font-size:9.5px;font-weight:600;letter-spacing:0.2em;text-transform:uppercase;color:{stone}">Resident lounge</figcaption>
      </figure>
    </div>
""".format(display=DISPLAY, sans=SANS, ink=th['ink'], accent=th['accent'], stone=th['stone'])

open(os.path.join(HERE, 'Main.dc.html'), 'w', encoding='utf-8').write(
    page('free', 'Free locating flyer', inner2, root_extra=hero, pad='418px 60px 44px'))

# ------------------------------------------------------------- 3 relocation
th = THEMES['reloc']
hoods = ' &nbsp;&middot;&nbsp; '.join(
    ['Downtown', 'Rainey', 'East Austin', 'South Congress', 'Zilker',
     'Mueller', 'The Domain', 'Cedar Park', 'Round Rock'])

inner3 = """    <div style="display:flex;flex-direction:column;align-items:flex-start;gap:16px">
      {label}
      <h1 style="margin:0;font-family:{display};font-weight:400;font-size:70px;line-height:0.96;letter-spacing:-0.008em;color:{ink};text-wrap:balance">Sight unseen.<br><span style="font-style:italic;color:{accent}">Never blind.</span></h1>
    </div>

    <p style="margin:20px 0 0;font-family:{display};font-size:23px;line-height:1.38;color:{ink};max-width:600px;text-wrap:pretty">I tour the unit, film it, and negotiate the terms before you land. <span style="font-style:italic;color:{accent}">You arrive with keys, not doubts.</span></p>

    <div style="margin-top:24px;overflow:hidden"><img src="clubhouse_lobby.jpg" alt="Clubhouse lobby and resident lounge" style="width:100%;height:228px;object-fit:cover;display:block"></div>

    <div style="display:flex;align-items:baseline;justify-content:space-between;gap:24px;margin-top:12px">
      <div style="font-family:{sans};font-size:9.5px;font-weight:600;letter-spacing:0.22em;text-transform:uppercase;color:{stone}">Clubhouse lobby &middot; Resident lounge</div>
      <div style="font-family:{sans};font-size:9.5px;font-weight:600;letter-spacing:0.22em;text-transform:uppercase;color:{stone}">Remote tours seven days a week</div>
    </div>

    <div style="height:1px;background:{rule};margin-top:22px"></div>
    <div style="margin-top:14px;font-family:{sans};font-size:11px;font-weight:500;letter-spacing:0.15em;text-transform:uppercase;color:{stone};line-height:1.9;text-wrap:balance">{hoods}</div>
""".format(label=label('Relocation concierge &middot; Austin, Texas', 'reloc'), display=DISPLAY,
           sans=SANS, ink=th['ink'], accent=th['accent'], stone=th['stone'], rule=th['rule'],
           hoods=hoods)

open(os.path.join(HERE, 'Relocation.dc.html'), 'w', encoding='utf-8').write(
    page('reloc', 'Relocation flyer', inner3))

# ------------------------------------------------------------ 4 move season
th = THEMES['move']
inner4 = """    <div style="display:flex;gap:40px;align-items:flex-start">
      <div style="flex:1;min-width:0;display:flex;flex-direction:column;gap:16px">
        {label}
        <h1 style="margin:0;font-family:{display};font-weight:400;font-size:63px;line-height:0.98;letter-spacing:-0.008em;color:{ink};text-wrap:balance">Your lease<br>is ending.<br><span style="font-style:italic;color:{accent}">Your options<br>aren't.</span></h1>
      </div>
      <div style="flex:none;width:340px;overflow:hidden"><img src="arched_facade.jpg" alt="Arched facade over a resident courtyard" style="width:100%;height:418px;object-fit:cover;display:block"></div>
    </div>

    <div style="display:flex;align-items:baseline;justify-content:space-between;gap:24px;margin-top:12px">
      <div style="font-family:{sans};font-size:9.5px;font-weight:600;letter-spacing:0.22em;text-transform:uppercase;color:{stone}">Renewal review &middot; Video tours &middot; Specials</div>
      <div style="font-family:{sans};font-size:9.5px;font-weight:600;letter-spacing:0.22em;text-transform:uppercase;color:{stone};white-space:nowrap">Resident courtyard</div>
    </div>

    <div style="height:1px;background:{rule};margin-top:22px"></div>

    <p style="margin:22px 0 0;font-family:{display};font-size:24px;line-height:1.38;color:{ink};max-width:640px;text-wrap:pretty">Before you sign the renewal, see what the same rent secures across Austin this month. <span style="font-style:italic;color:{accent}">One message to get started.</span></p>
""".format(label=label('Lease ending soon &middot; Austin, Texas', 'move'), display=DISPLAY,
           sans=SANS, ink=th['ink'], accent=th['accent'], stone=th['stone'], rule=th['rule'])

open(os.path.join(HERE, 'MoveSeason.dc.html'), 'w', encoding='utf-8').write(
    page('move', 'Move season flyer', inner4))

# ------------------------------------------------------------------- canvas
canvas = {
    "artboards": [
        {"file": "TearOff.dc.html",    "x": 0,    "y": 0, "w": W, "h": H, "title": "Tear-off",      "print": "fixed"},
        {"file": "Main.dc.html",       "x": 916,  "y": 0, "w": W, "h": H, "title": "Free locating", "print": "fixed"},
        {"file": "Relocation.dc.html", "x": 1832, "y": 0, "w": W, "h": H, "title": "Relocation",    "print": "fixed"},
        {"file": "MoveSeason.dc.html", "x": 2748, "y": 0, "w": W, "h": H, "title": "Move season",   "print": "fixed"},
    ],
    "annotations": [
        {"id": "print-spec", "x": 0, "y": -150, "w": 700,
         "text": "US Letter trim, 8.5 x 11 in, drawn at 96 px per inch. Export PDF prints each artboard as one page. For Canva Print add a 0.125 in bleed on all four sides and keep type inside the current margins."}
    ],
    "launch": {"view": "canvas"},
}
json.dump(canvas, open(os.path.join(HERE, 'canvas.json'), 'w', encoding='utf-8'), indent=2)
print('wrote artboards + canvas.json')

for f in ('TearOff.dc.html', 'Main.dc.html', 'Relocation.dc.html', 'MoveSeason.dc.html'):
    src = open(os.path.join(HERE, f), encoding='utf-8').read()
    assert '—' not in src and '&mdash;' not in src, ('em dash in ' + f)
    assert 'Spirit Real Estate Group,' not in src and 'Spirit Real Estate LLC' not in src
    print('  ok', f, len(src), 'chars')
