"""Verify the suite before it ships.  Run:  python verify_trec.py

Reports, per face, the largest type size against the broker-name size. TREC
22 TAC 535.155(a)(2) wants the broker name at no less than half the largest
agent contact item, so the ratio column must read 2.00 or lower.

Where the broker name is carried by the logo rather than by text, the measured
quantity is the cap height of "SPIRIT" inside the logo -- 0.1153 x its rendered
width -- because TREC measures the name, not the logo box. The constant was
measured on the flat-topped T of the official artwork as placed in
assets/v2/spirit_logo_navy.png (1665 x 494 canvas, 192 px cap).

Checks, per face, across cards and flyers: the QR resolves to the intake form;
the Instagram handle is gone; the brokerage string is the licensed name; and
every style carries the broker name.

The licensed name is "Spirit Real Estate Group", the registered DBA of the
sponsoring broker Bryan Keith Bjerke, #562021-B. "Spirit Real Estate Group,
LLC" is license #9003398-BB, a different broker company, and must not appear.
"""
import glob
import os
import re
import sys

try:
    import cv2
except ImportError:
    cv2 = None

HERE = os.path.dirname(os.path.abspath(__file__))
BC = os.path.normpath(os.path.join(HERE, '..'))
FACE_DIRS = [os.path.join(BC, 'cards_v2'), os.path.join(BC, 'flyers')]
ASSETS = os.path.join(BC, 'assets', 'v2')
FORM = 'https://sparkapt.com/inquiry/sophia-reddehase859'
BROKER = 'Spirit Real Estate Group'
WRONG_ENTITY = re.compile(r'Spirit Real Estate Group,?\s+LLC', re.I)
CAP_PER_WIDTH = 0.1153
MAX_RATIO = 2.00


def read(path):
    with open(path, encoding='utf-8') as f:
        return f.read()


def style_key(d):
    return int(os.path.basename(d).split('_')[0])


problems = []

# --- QR payloads ---
qr_cache = {}
if cv2 is None:
    print('cv2 not installed: QR payloads not checked')
else:
    det = cv2.QRCodeDetector()
    for p in sorted(glob.glob(os.path.join(ASSETS, 'qr_*.png'))):
        data, _, _ = det.detectAndDecode(cv2.imread(p))
        qr_cache[os.path.basename(p)] = data
        if data != FORM:
            problems.append(f'QR {os.path.basename(p)} -> {data or "UNREADABLE"}')

tightest = None
for root in FACE_DIRS:
    kind = os.path.basename(root)
    files = sorted(glob.glob(os.path.join(root, '*', '*.html')),
                   key=lambda p: (style_key(os.path.dirname(p)), os.path.basename(p)))

    print(f'\n== {kind}: per-face ==')
    print(f'{"face":40s} {"name":>6s} {"broker":>7s} {"ratio":>6s}  qr')
    for path in files:
        style = os.path.basename(os.path.dirname(path))
        face = os.path.basename(path).replace('.html', '')
        src = read(path)
        label = f'{kind}/{style}/{face}'

        # largest display font-size = the agent name on faces that show it
        # ignore the decorative monogram watermark: a letterform, not a name
        scrubbed = re.sub(r'\.monogram \{[^}]*\}', '', src, flags=re.S)
        sizes = [float(x) for x in re.findall(r'font-size[:=]\s*"?\s*([0-9.]+)(?:px)?"?', scrubbed)]
        name_px = max(sizes) if sizes else 0

        # The broker name appears either as text (a .compliance / SVG line) or
        # inside the logo. For the logo, what counts is the cap height of "SPIRIT".
        broker_px = 0.0
        m = re.search(r'\.brokermark img \{[^}]*width:\s*([0-9.]+)px', src, re.S)
        if m:
            broker_px = float(m.group(1)) * CAP_PER_WIDTH

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
        flag = '' if (not has_broker or broker_px == 0 or ratio <= MAX_RATIO) else '  <== RATIO'
        print(f'{label:40s} {name_px:6.0f} {broker_px:7.1f} {ratio:6.2f}  {qrname}{flag}')
        if has_broker and broker_px and (tightest is None or ratio > tightest[0]):
            tightest = (ratio, label)

        if 'sophiasky.atx' in src:
            problems.append(f'{label}: Instagram handle still present')
        if WRONG_ENTITY.search(src):
            problems.append(f'{label}: names Spirit Real Estate Group, LLC (#9003398-BB), not the sponsoring broker')
        if qr and cv2 is not None and qr_cache.get(qrname) != FORM:
            problems.append(f'{label}: QR {qrname} does not resolve to the form')
        if broker_px and ratio > MAX_RATIO:
            problems.append(f'{label}: broker {broker_px:g}px vs name {name_px:g}px = {ratio:.2f}x (needs <= 2x)')

    # a front with no broker name is the most-cited TREC violation; call it out
    print(f'\n== {kind}: fronts with no broker name ==')
    none = [f for f in sorted(glob.glob(os.path.join(root, '*', 'front.html')))
            if BROKER.lower() not in read(f).lower()]
    for f in none:
        rel = f'{kind}/{os.path.basename(os.path.dirname(f))}/front.html'
        print('  ' + rel)
        problems.append(f'{rel}: front carries no broker name')
    if not none:
        print('  none')

    # every style must carry the broker name on at least one face
    print(f'\n== {kind}: per-style broker presence ==')
    for d in sorted(os.listdir(root), key=style_key):
        faces = glob.glob(os.path.join(root, d, '*.html'))
        hits = [os.path.basename(f) for f in faces if BROKER.lower() in read(f).lower()]
        print(f'  {d:26s} {", ".join(sorted(hits)) or "NONE"}')
        if not hits:
            problems.append(f'{kind}/{d}: no face carries the broker name')

if tightest:
    print(f'\ntightest face: {tightest[1]} at {tightest[0]:.2f}x '
          f'(broker name is {1 / tightest[0]:.2f}x the largest type; floor 0.50x)')
print()
if problems:
    print('\n'.join('FAIL ' + p for p in problems))
    sys.exit(1)
print('ALL CHECKS PASS')
