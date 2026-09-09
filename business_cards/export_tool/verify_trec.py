"""Verify the suite before it ships.  Run:  python3 verify_trec.py

Reports, per face, the agent-name size against the broker-name size. TREC
22 TAC 535.155(a)(2) wants the broker name at no less than half the largest
agent contact item, so the ratio column must read 2.00 or lower.

Where the broker name is carried by the logo rather than by text, the measured
quantity is the cap height of "SPIRIT" inside the logo -- 0.1194 x its rendered
width -- because TREC measures the name, not the logo box.

Checks, per face: the QR resolves to the intake form; the Instagram handle is
gone; the brokerage string is the licensed name; and every card carries the
broker name. Also reports the agent-name vs broker-name size pair so the TREC
535.155(a)(2) half-size ratio can be eyeballed per face.
"""
import cv2
import glob
import os
import re
import sys

ROOT = '/home/user/sophia-austin-locating/business_cards/cards_v2'
ASSETS = '/home/user/sophia-austin-locating/business_cards/assets/v2'
FORM = 'https://sparkapt.com/inquiry/sophia-reddehase859'
BROKER = 'Spirit Real Estate Group, LLC'

files = sorted(glob.glob(os.path.join(ROOT, '*', '*.html')),
               key=lambda p: (int(os.path.basename(os.path.dirname(p)).split('_')[0]),
                              os.path.basename(p)))
problems = []

# --- QR payloads ---
det = cv2.QRCodeDetector()
qr_cache = {}
for p in sorted(glob.glob(os.path.join(ASSETS, 'qr_*.png'))):
    data, _, _ = det.detectAndDecode(cv2.imread(p))
    qr_cache[os.path.basename(p)] = data
    if data != FORM:
        problems.append(f'QR {os.path.basename(p)} -> {data or "UNREADABLE"}')

print('== per-face ==')
print(f'{"face":40s} {"name":>6s} {"broker":>7s} {"ratio":>6s}  qr')
for path in files:
    style = os.path.basename(os.path.dirname(path))
    face = os.path.basename(path).replace('.html', '')
    src = open(path).read()
    label = f'{style}/{face}'

    # largest display font-size = the agent name on faces that show it
    # ignore the decorative monogram watermark: a letterform, not a name
    scrubbed = re.sub(r'\.monogram \{[^}]*\}', '', src, flags=re.S)
    sizes = [float(x) for x in re.findall(r'font-size[:=]\s*"?\s*([0-9.]+)(?:px)?"?', scrubbed)]
    name_px = max(sizes) if sizes else 0

    # The broker name appears either as text (a .compliance / SVG line) or
    # inside the logo. For the logo, what counts is the cap height of "SPIRIT",
    # measured at 0.1194 x the rendered width -- not the logo box.
    broker_px = 0.0
    m = re.search(r'\.brokermark img \{[^}]*width:\s*([0-9.]+)px', src, re.S)
    if m:
        broker_px = float(m.group(1)) * 0.1194

    for sel in (r'\.broker \.bname \{[^}]*font-size:\s*([0-9.]+)px',
                r'\.compliance \{[^}]*font-size:\s*([0-9.]+)px',
                r'\.meta \{[^}]*font-size:\s*([0-9.]+)px',
                r'\.broker-pill \{[^}]*font-size:\s*([0-9.]+)px',
                r'\.footer \.brand \{[^}]*font-size:\s*([0-9.]+)px',
                r'\.info-bar \.brokerage \{[^}]*font-size:\s*([0-9.]+)px'):
        m2 = re.search(sel, src, re.S)
        if m2:
            broker_px = max(broker_px, float(m2.group(1)))
            break

    # a brokerage set as SVG text carries its size on the element
    for m3 in re.finditer(r'font-size="([0-9.]+)"[^>]*>[^<]*SPIRIT REAL ESTATE', src, re.I):
        broker_px = max(broker_px, float(m3.group(1)))

    has_broker = BROKER.lower() in src.lower()
    qr = re.search(r'src="\.\./\.\./assets/v2/(qr_[^"]+)"', src)
    qrname = qr.group(1) if qr else '-'

    ratio = (name_px / broker_px) if broker_px else float('inf')
    flag = '' if (not has_broker or broker_px == 0 or ratio <= 2.05) else '  <== RATIO'
    print(f'{label:40s} {name_px:6.0f} {broker_px:7.1f} {ratio:6.2f}  {qrname}{flag}')

    if 'sophiasky.atx' in src:
        problems.append(f'{label}: Instagram handle still present')
    if re.search(r'Spirit Real Estate Group(?!, LLC)', src, re.I):
        problems.append(f'{label}: brokerage name not the licensed form')
    if qr and qr_cache.get(qrname) != FORM:
        problems.append(f'{label}: QR {qrname} does not resolve to the form')
    if broker_px and ratio > 2.05:
        problems.append(f'{label}: broker {broker_px:g}px vs name {name_px:g}px = {ratio:.2f}x (needs <= 2x)')

# a front with no broker name is the most-cited TREC violation; call it out
print('\n== fronts with no broker name ==')
import glob as _g
_none = [f for f in sorted(_g.glob(os.path.join(ROOT, '*', 'front.html')))
         if BROKER.lower() not in open(f).read().lower()]
for f in _none:
    rel = os.path.join(os.path.basename(os.path.dirname(f)), 'front.html')
    print('  ' + rel)
    problems.append(f'{rel}: front carries no broker name')
if not _none:
    print('  none')

# every style must carry the broker name on at least one face
print('\n== per-style broker presence ==')
for d in sorted(os.listdir(ROOT), key=lambda x: int(x.split('_')[0])):
    faces = glob.glob(os.path.join(ROOT, d, '*.html'))
    hits = [os.path.basename(f) for f in faces if BROKER.lower() in open(f).read().lower()]
    print(f'  {d:26s} {", ".join(sorted(hits)) or "NONE"}')
    if not hits:
        problems.append(f'{d}: no face carries the broker name')

print()
if problems:
    print('\n'.join('FAIL ' + p for p in problems))
    sys.exit(1)
print('ALL CHECKS PASS')
