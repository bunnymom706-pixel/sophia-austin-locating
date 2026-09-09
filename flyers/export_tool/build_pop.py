"""One-shot rewrite of the four flyers: pop style (pink / orange / yellow, Anton) for the tear-off and
free-locating sheets, and the ivory / charcoal editorial sheets with bigger type, photo, QR and logo."""
import os
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
def w(rel, html):
    with open(os.path.join(ROOT, rel), 'w', encoding='utf-8') as f: f.write(html)
    print('ok', rel)

HEAD = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>{title}</title>
<link rel="stylesheet" href="../shared/fonts.css">
<link rel="stylesheet" href="../shared/base.css">
<link rel="stylesheet" href="../shared/{system}.css">
<style>
{css}
</style>
</head>
<body>
<div class="sheet">
'''
END = '''
</div>
<script src="../shared/brand.js"></script>
</body>
</html>
'''
COMPLIANCE = '''    <div class="compliance">
      <p><strong>Sophia Sky Reddehase</strong>, sales agent, TREC License #831516, sponsored by <strong>Spirit Real Estate Group</strong>. <strong>Information About Brokerage Services</strong> and the <strong>TREC Consumer Protection Notice</strong>: trec.texas.gov. Locating is free to you; the property pays the agent. Pricing and availability subject to change daily; specials subject to property terms and leasing approval.</p>
    </div>'''
def broker(dark=False):
    return '''    <div class="broker">
      <div class="txt" data-trec="broker">Brokered by Spirit Real Estate Group<small>Licensed sales agent sponsored by this broker</small></div>
      <div class="spirit-logo{d}"></div>
      <div class="eho">Equal Housing<br>Opportunity</div>
    </div>'''.format(d=' on-dark' if dark else '')
def cta(qr):
    return '''    <div class="cta"><img src="../shared/qr/{qr}" alt="QR code: begin your free search"><div class="t"><div class="k">Free apartment locating</div><div class="h">Scan, text or call.</div><div class="p" data-trec="contact" data-label="phone">(512) 676-1215</div><div class="u" data-trec="contact" data-label="web">sparkapt.com/inquiry/sophia-reddehase859 &nbsp;&middot;&nbsp; sophia.reddehase@spiritre.com</div></div></div>'''.format(qr=qr)
def contact():
    return '''    <div class="contact">
      <div class="name" data-trec="contact" data-label="name">Sophia Sky Reddehase</div>
      <div class="role">Apartment Locator &middot; Austin, Texas &middot; TREC #831516</div>
    </div>'''
STAR = '<svg class="star {cls}" viewBox="0 0 40 40"><path d="M20 0c2 11 7 16 20 20-13 4-18 9-20 20-2-11-7-16-20-20 13-4 18-9 20-20z"/></svg>'
def stars(spec):
    return ''.join(STAR.format(cls=c) for c in spec)

# ============ POP SYSTEM (shared/pop.css) ============
POP_CSS = '''/* Pop system for the colorful flyers: hot pink / orange / butter yellow, Anton display, Fredoka body.
   Tokens on .sheet: --pink --orange --yellow --plum --paper --ink */
.sheet { --pink:#F48AD9; --orange:#F4531C; --yellow:#F8CF5A; --plum:#6E1140; --cream:#FFF4E6;
  background: var(--paper); color: var(--ink); font-family: 'Fredoka', 'Baloo 2', system-ui, sans-serif; font-size: 13px; line-height: 1.4; font-weight: 500; }
.block { position: absolute; }
.star { position: absolute; width: 34px; height: 34px; fill: var(--yellow); }
.star.o { fill: var(--orange); } .star.p { fill: var(--pink); } .star.c { fill: var(--cream); } .star.pl { fill: var(--plum); }
.star.s { width: 20px; height: 20px; } .star.l { width: 52px; height: 52px; }
.page { position: absolute; top: 48px; left: 52px; right: 52px; bottom: 44px; display: flex; flex-direction: column; align-items: center; text-align: center; }
.page > * { flex: none; }
h1 { margin: 0; font-family: 'Anton', 'Impact', sans-serif; font-weight: 400; text-transform: uppercase; line-height: .9; letter-spacing: 0.005em; text-wrap: balance; }
.kick { font-family: 'Lilita One', 'Fredoka', sans-serif; font-size: 22px; letter-spacing: 0.02em; line-height: 1.05; }
.kick i { font-style: normal; }
.tilt { transform: rotate(-3deg); }
.photo-card { overflow: hidden; border-radius: 26px; border: 8px solid var(--cream); box-shadow: 0 14px 0 rgba(110,17,64,.18); }
.photo-card img { width: 100%; height: 100%; object-fit: cover; display: block; }
.cap { font-family: 'Lilita One', sans-serif; font-size: 13px; letter-spacing: 0.06em; text-transform: uppercase; }
.pills { display: flex; gap: 10px; justify-content: center; flex-wrap: wrap; }
.pill { font-family: 'Lilita One', sans-serif; font-size: 15px; letter-spacing: 0.04em; text-transform: uppercase; padding: 7px 16px; border-radius: 999px; background: var(--plum); color: var(--cream); }
.pill.y { background: var(--yellow); color: var(--plum); } .pill.o { background: var(--orange); color: var(--cream); } .pill.c { background: var(--cream); color: var(--plum); }

/* footer */
.foot { margin-top: auto; width: 100%; display: flex; flex-direction: column; align-items: center; }
.contact { display: flex; flex-direction: column; align-items: center; gap: 2px; padding: 10px 0 4px; }
.contact .name { font-family: 'Anton', sans-serif; font-size: 40px; letter-spacing: 0.03em; text-transform: uppercase; line-height: 1; }
.contact .role { font-family: 'Lilita One', sans-serif; font-size: 12px; letter-spacing: 0.16em; text-transform: uppercase; }
.cta { width: 100%; display: flex; align-items: center; gap: 22px; margin-top: 10px; padding: 14px 20px; background: var(--cta-bg); color: var(--cta-ink); border-radius: 22px; text-align: left; }
.cta img { width: 124px; height: 124px; background: #FFFFFF; padding: 7px; border-radius: 14px; flex: none; }
.cta .t { flex: 1; display: flex; flex-direction: column; gap: 1px; }
.cta .k { font-family: 'Lilita One', sans-serif; font-size: 12px; letter-spacing: 0.22em; text-transform: uppercase; opacity: .9; }
.cta .h { font-family: 'Anton', sans-serif; font-size: 32px; line-height: 1; text-transform: uppercase; }
.cta .p { font-family: 'Anton', sans-serif; font-size: 38px; letter-spacing: 0.02em; line-height: 1; margin-top: 4px; }
.cta .u { font-size: 11.5px; font-weight: 600; margin-top: 3px; }
.broker { width: 100%; display: flex; align-items: center; justify-content: space-between; gap: 18px; padding: 12px 22px; margin-top: 10px; background: var(--cream); color: var(--plum); border-radius: 18px; }
.broker .txt { font-family: 'Anton', sans-serif; font-weight: 400; font-size: 23px; letter-spacing: 0.01em; line-height: 1.05; text-align: left; text-transform: uppercase; white-space: nowrap; }
.broker .txt small { display: block; font-family: 'Fredoka', sans-serif; font-size: 9.5px; font-weight: 600; letter-spacing: 0.16em; text-transform: uppercase; margin-top: 3px; opacity: .8; }
.broker .spirit-logo { --logo-size: 48px; --navy: #0F2D5C; }
.broker .eho { display: inline-flex; align-items: center; gap: 6px; font-size: 9px; font-weight: 700; letter-spacing: 0.04em; text-transform: uppercase; white-space: nowrap; }
.broker .eho svg { height: 1.9em; width: auto; }
.compliance { margin-top: 8px; font-size: 8.6px; line-height: 1.45; font-weight: 500; }
.compliance p { margin: 0; }
.compliance strong { font-weight: 700; }
'''
with open(os.path.join(ROOT, 'shared', 'pop.css'), 'w', encoding='utf-8') as f: f.write(POP_CSS)
print('ok shared/pop.css')

# ============ 1 TEAR-OFF (pink paper, orange headline, yellow diagonal, tabs) ============
css1 = '''
  .sheet { --paper: var(--pink); --ink: var(--plum); --cta-bg: var(--plum); --cta-ink: var(--cream); }
  .block.y { left: -40px; right: -40px; bottom: 130px; height: 420px; background: var(--yellow); clip-path: polygon(0 34%, 100% 0, 100% 100%, 0 100%); }
  .page { bottom: 168px; }
  h1 { font-size: 88px; color: var(--orange); }
  .cta { padding: 10px 18px; }
  .cta img { width: 104px; height: 104px; }
  .broker { padding: 8px 20px; margin-top: 8px; }
  .compliance { margin-top: 6px; }
  .kick { margin-top: 6px; color: var(--plum); }
  .photo-card { width: 560px; height: 236px; margin-top: 10px; }
  .photo-card img { object-position: center 78%; }
  .pills { margin-top: 12px; }
  .contact { padding-top: 6px; }
  .tabs { position: absolute; left: 44px; right: 44px; bottom: 44px; height: 100px; display: grid; grid-template-columns: repeat(10, 1fr); border-top: 2px dashed var(--plum); }
  .tab { position: relative; min-width: 0; overflow: hidden; border-right: 2px dashed var(--plum); }
  .tab:last-child { border-right: 0; }
  .tab .v { position: absolute; left: 50%; top: 50%; width: 90px; transform: translate(-50%, -50%) rotate(-90deg); white-space: nowrap; display: flex; flex-direction: column; align-items: flex-start; gap: 2px; }
  .tab .v b { font-family: 'Anton', sans-serif; font-weight: 400; font-size: 13.5px; letter-spacing: 0.04em; color: var(--plum); }
  .tab .v small { font-family: 'Lilita One', sans-serif; font-size: 8px; letter-spacing: 0.18em; text-transform: uppercase; color: var(--orange); }
'''
tab = '<div class="tab"><div class="v"><b>(512) 676-1215</b><small>Sophia · Locating</small></div></div>'
body1 = '''  <div class="block y"></div>
  <div style="position:absolute;left:52px;top:44px">''' + stars(['o l']) + '''</div>
  <div style="position:absolute;right:70px;top:120px">''' + stars(['c']) + '''</div>
  <div style="position:absolute;left:96px;top:300px">''' + stars(['c s']) + '''</div>
  <div style="position:absolute;right:52px;top:330px">''' + stars(['o']) + '''</div>
  <div class="page">
    <div class="kick tilt" style="color:var(--cream)">Austin, Texas &nbsp;&#9733;&nbsp; It's free</div>
    <h1>Apartment<br>Locating</h1>
    <div class="kick">The property pays. You just move in.</div>
    <div class="photo-card"><img src="../shared/photos/sophia_pool_clubhouse.jpg" alt=""></div>
    <div class="pills"><span class="pill">Search</span><span class="pill o">Video tours</span><span class="pill c">Specials</span><span class="pill">Move in</span></div>
  <div class="foot">
''' + contact() + '\n' + cta('qr_navy.svg') + '\n' + broker() + '\n' + COMPLIANCE + '''
  </div>
  </div>
  <div class="tabs">''' + tab * 10 + '</div>\n'
w('1_tearoff/flyer.html', HEAD.format(title='Apartment Locating — tear-off', system='pop', css=css1) + body1 + END)

# ============ 2 FREE LOCATING (orange paper, pink diagonal, big photo top) ============
css2 = '''
  .sheet { --paper: var(--orange); --ink: var(--cream); --cta-bg: var(--yellow); --cta-ink: var(--plum); }
  .block.p { left: -40px; right: -40px; top: 410px; height: 720px; background: var(--pink); clip-path: polygon(0 12%, 100% 0, 100% 100%, 0 100%); }
  .hero { position: absolute; left: 0; right: 0; top: 0; height: 450px; overflow: hidden; }
  .hero img { width: 100%; height: 100%; object-fit: cover; object-position: center 62%; }
  .hero::after { content: ""; position: absolute; inset: 0; background: linear-gradient(180deg, rgba(110,17,64,0) 30%, rgba(110,17,64,.55) 100%); }
  .page { top: 450px; bottom: 44px; }
  h1 { margin-top: -96px; font-size: 80px; color: var(--cream); position: relative; z-index: 2; text-shadow: 0 6px 0 rgba(110,17,64,.25); }
  h1 i { font-style: normal; color: var(--yellow); }
  .kick { margin-top: 8px; color: var(--plum); font-size: 22px; }
  .pills { margin-top: 12px; }
  .contact { color: var(--plum); }
  .foot { color: var(--plum); }
  .compliance { color: var(--plum); }
'''
body2 = '''  <div class="hero"><img src="../shared/photos/sophia_pool_sunset_courtyard.jpg" alt=""></div>
  <div class="block p"></div>
  <div style="position:absolute;left:60px;top:560px">''' + stars(['c l']) + '''</div>
  <div style="position:absolute;right:64px;top:520px">''' + stars(['y']) + '''</div>
  <div style="position:absolute;right:110px;top:640px">''' + stars(['c s']) + '''</div>
  <div class="page">
    <h1>The property<br><i>pays.</i> You just<br>move in.</h1>
    <div class="kick">Free apartment locating &nbsp;&#9733;&nbsp; Austin</div>
    <div class="pills"><span class="pill">Search</span><span class="pill o">Video tours</span><span class="pill c">Specials</span></div>
  <div class="foot">
''' + contact() + '\n' + cta('qr_red.svg') + '\n' + broker() + '\n' + COMPLIANCE + '''
  </div>
  </div>
'''
w('2_free_locating/flyer.html', HEAD.format(title='The property pays — free locating', system='pop', css=css2) + body2 + END)

# ============ 3 RELOCATION (ivory editorial, bigger) ============
css3 = '''
  .sheet { --paper:#FFFFFF; --ink:#1C1B1A; --gold:#B99A5B; --muted:#6F6A62; --line:#D9D2C6; --cta-bg:#1C1B1A; --cta-ink:#F7F4EE; }
  .head { display: flex; flex-direction: column; align-items: center; gap: 10px; }
  h1 { font-size: 44px; }
  .sub { font-family: 'Cormorant Garamond', serif; font-style: italic; font-weight: 300; font-size: 30px; line-height: 1; color: var(--muted); }
  .photo.wide { width: 100%; height: 330px; margin-top: 14px; }
  .lede { margin-top: 12px; font-size: 20px; max-width: 620px; }
  .hoods { width: 100%; margin-top: 12px; display: grid; grid-template-columns: repeat(4, 1fr); gap: 0 16px; }
  .hoods div { font-family: 'Cormorant Garamond', serif; font-size: 18px; line-height: 1; padding: 7px 0; border-bottom: 1px solid var(--line); text-align: center; }
'''
FRAME = '  <div class="frame"></div><div class="corners"><span></span><span></span><span></span><span></span></div>\n'
body3 = FRAME + '''  <div class="page">
    <div class="head">
      <div class="eyebrow">Relocation concierge &nbsp;&middot;&nbsp; Austin, Texas</div>
      <h1 class="caps">Relocating to Austin</h1>
      <div class="sub">Sight unseen, never blind.</div>
      <div class="orn"></div>
    </div>
    <div class="photo wide"><img src="../shared/photos/sophia_clubhouse_lobby.jpg" alt=""></div>
    <div class="cap">Clubhouse lobby &middot; Resident lounge</div>
    <p class="lede">I tour it, film it, negotiate it. <i>You arrive with keys. Free; the property pays.</i></p>
    <div class="hoods"><div>Downtown</div><div>East Austin</div><div>South Congress</div><div>Zilker</div><div>Mueller</div><div>The Domain</div><div>Cedar Park</div><div>Round Rock</div></div>
  <div class="foot">
''' + contact() + '\n' + cta('qr_ink.svg') + '\n' + broker() + '\n' + COMPLIANCE + '''
  </div>
  </div>
'''
w('3_relocation/flyer.html', HEAD.format(title='Relocating to Austin — concierge', system='luxury', css=css3) + body3 + END)

# ============ 4 MOVE SEASON (charcoal / gold, bigger) ============
css4 = '''
  .sheet { --paper:#1C1B1A; --ink:#F7F4EE; --gold:#C9AD6E; --muted:#A79F92; --line:#4A453E; --logo:#F7F4EE; --cta-bg:#C9AD6E; --cta-ink:#1C1B1A; }
  .head { display: flex; flex-direction: column; align-items: center; gap: 12px; }
  h1 { font-size: 54px; }
  h1 i { color: var(--gold); }
  .arch { width: 340px; height: 344px; margin-top: 12px; }
  .lede { margin-top: 12px; font-size: 21px; max-width: 600px; }
  .services { margin-top: 10px; font-size: 11px; }
  .compliance strong { color: var(--ink); }
'''
body4 = FRAME + '''  <div class="page">
    <div class="head">
      <div class="eyebrow gold">Lease ending soon &nbsp;&middot;&nbsp; Austin, Texas</div>
      <h1>Your lease is ending.<br><i>Your options aren't.</i></h1>
      <div class="orn"></div>
    </div>
    <div class="arch"><img src="../shared/photos/sophia_arched_facade.jpg" alt=""></div>
    <div class="cap">Arched facade &middot; Resident courtyard</div>
    <p class="lede">See what the same rent gets you across Austin. <i>Shortlist by tomorrow.</i></p>
    <div class="services"><span>Renewal review</span><i></i><span>Shortlist</span><i></i><span>Specials</span></div>
  <div class="foot">
''' + contact() + '\n' + cta('qr_charcoal.svg') + '\n' + broker(True) + '\n' + COMPLIANCE + '''
  </div>
  </div>
'''
w('4_move_season/flyer.html', HEAD.format(title='Your lease is ending — move season', system='luxury', css=css4) + body4 + END)

# ============ luxury.css size bump ============
p = os.path.join(ROOT, 'shared', 'luxury.css'); s = open(p, encoding='utf-8').read()
rep = [
(".contact { display: flex; flex-direction: column; align-items: center; gap: 6px; padding: 22px 0 14px; }", ".contact { display: flex; flex-direction: column; align-items: center; gap: 6px; padding: 16px 0 4px; }"),
(".contact .name { font-family: 'Italiana', 'Cormorant Garamond', serif; font-size: 30px;", ".contact .name { font-family: 'Italiana', 'Cormorant Garamond', serif; font-size: 40px;"),
(".contact .role { font-size: 9px;", ".contact .role { font-size: 11px;"),
(".broker { width: 100%; display: flex; align-items: center; justify-content: center; gap: 28px; padding: 12px 0;", ".broker { width: 100%; display: flex; align-items: center; justify-content: center; gap: 30px; padding: 12px 0; margin-top: 12px;"),
(".broker .txt { font-family: 'Cormorant Garamond', serif; font-weight: 500; font-size: 16px;", ".broker .txt { font-family: 'Cormorant Garamond', serif; font-weight: 500; font-size: 23px;"),
(".broker .txt small { display: block; font-family: 'Plus Jakarta Sans', sans-serif; font-size: 8px;", ".broker .txt small { display: block; font-family: 'Plus Jakarta Sans', sans-serif; font-size: 9px;"),
(".broker .spirit-logo { --logo-size: 28px;", ".broker .spirit-logo { --logo-size: 48px;"),
(".broker .eho { font-size: 7.5px;", ".broker .eho { font-size: 9px;"),
(".compliance { margin-top: 9px; font-size: 7.8px;", ".compliance { margin-top: 9px; font-size: 8.6px;"),
(".cap { margin-top: 8px; font-size: 8px;", ".cap { margin-top: 8px; font-size: 10px;"),
(".cta img { width: 76px; height: 76px;", ".cta img { width: 124px; height: 124px;"),
(".cta .k { font-size: 8.5px;", ".cta .k { font-size: 10px;"),
(".cta .h { font-family: 'Cormorant Garamond', serif; font-size: 23px;", ".cta .h { font-family: 'Cormorant Garamond', serif; font-size: 34px;"),
(".cta .p { font-size: 25px;", ".cta .p { font-size: 38px;"),
(".cta .u { font-size: 9.5px;", ".cta .u { font-size: 11px;"),
(".cta { width: 100%; display: flex; align-items: center; gap: 18px; margin-top: 12px; padding: 13px 18px;", ".cta { width: 100%; display: flex; align-items: center; gap: 22px; margin-top: 10px; padding: 14px 20px;"),
("so the broker name in the logo reads ~22.7px cap height, above 1/2 of the 30px name (TREC 22 TAC 535.155).", "so the SPIRIT wordmark reads ~38.9px cap height against the 40px name (TREC 22 TAC 535.155 needs >= 1/2)."),
]
for a, b in rep:
    if a in s: s = s.replace(a, b)
    else: print('  (already applied)', a[:50])
open(p, 'w', encoding='utf-8').write(s); print('ok shared/luxury.css')
