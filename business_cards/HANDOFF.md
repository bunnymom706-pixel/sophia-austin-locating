# Sophia Sky Reddehase: brand suite handoff

Everything built for the apartment-locating business: 16 business card styles,
16 matching square flyers, review PDFs, and a website. This file is the state
of play so another session can pick up without re-deriving any of it.

## Who

Checked against the TREC License Holder Search on 2026-09-11.

| | |
|---|---|
| Agent | Sophia Sky Reddehase (licensed as "Reddehase, Sophia Sky") |
| License | TREC #831516-SA, active, expires 11/30/2026 |
| Brokerage, as printed | **Spirit Real Estate Group** (no "LLC") |
| Sponsoring broker | Bryan Keith Bjerke, TREC #562021-B, individual broker, sponsor date 08/19/2026 |
| Broker contact | bryan.bjerke@spiritre.com · (214) 396-3888 · 1701 N Collins Blvd Ste 231, Richardson TX 75080 |
| Phone | (512) 676-1215 |
| Email | sophia.reddehase@spiritre.com |
| Profile / intake form | https://sparkapt.com/inquiry/sophia-reddehase859 (printed and in every QR) |
| Dead link, never print | sparkapt.com/sophia-reddehase returns 404. It was on every back until 2026-09-11 |
| Market | Austin & surrounding areas |
| Services | Relocation · second chance (eviction / broken lease) · first-time renters · luxury |
| Offer | Free to renters; the property pays the locator fee |

### Never print "Spirit Real Estate Group, LLC"

It is a real license, but not Sophia's broker. On TREC:

- **Spirit Real Estate Group, LLC** is broker company #9003398-BB, designated
  broker Thomas Edward Birdwell (#586207-B).
- **Bryan Keith Bjerke** is individual broker #562021-B. His registered DBAs
  include "Spirit Real Estate Group". Sophia's license names him as her
  sponsoring broker.

Every face, flyer, PDF, and the website said "Spirit Real Estate Group, LLC"
until 2026-09-11. All of it now reads "Spirit Real Estate Group", and
`verify_trec.py` fails any file that brings the LLC form back. spiritre.com
itself says "Spirit Real Estate Group, LLC" and lists both license numbers
together, which is how the wrong name got in. Go by TREC, not the website.

## What exists

| Where | What |
|---|---|
| `business_cards/cards_v2/{1..16}_*/` | 32 card faces as HTML |
| `business_cards/print_ready_images/v2/` | 32 card PNGs, 300 DPI |
| `business_cards/flyers/{1..16}_*/` | 32 flyer faces as HTML |
| `business_cards/print_ready_flyers/` | 32 flyer PNGs, 1725×1725 |
| `business_cards/pdf/` | 3 review PDFs for the broker |
| `business_cards/pdf/print/` | 32 print-ready PDFs, one per design, front and back at full bleed size |
| `business_cards/export_tool/build_print_pdfs.py` | Builds the 32 print PDFs from the PNGs |
| `website/index.html` | One-page site, self-contained (logo embedded as base64) |
| `business_cards/flyer_tool/gen_flyers.py` | Generates all 32 flyer faces |
| `business_cards/export_tool/render_faces.py` | Renders all 64 faces to PNG with desktop Chrome |
| `business_cards/export_tool/build_pdfs.py` | Builds the 3 review PDFs from the PNGs |
| `business_cards/export_tool/verify_trec.py` | Broker name, size ratio and QR checker, cards and flyers |
| `business_cards/export_tool/export.js` | Older Puppeteer exporter. Covers only card styles 1 to 13; use `render_faces.py` |

### Print geometry

| Format | File px @300 DPI | Trim | Bleed |
|---|---|---|---|
| Landscape card | 1125 × 675 | 3.5 × 2.0 in | 37.5 px |
| Vertical card | 675 × 1125 | 2.0 × 3.5 in | 37.5 px |
| Square card | 825 × 825 | 2.5 × 2.5 in | 37.5 px |
| Square flyer | 1725 × 1725 | 5.5 × 5.5 in | 37.5 px, 110 px corner radius |

Safe zone: all small type sits at least 1/16 in inside the trim, which is 56 px
or more from the file edge. Cards that needed moving carry a
`<style id="print-safe">` block just before `</head>` holding the nudges.

## The Spirit logo

**The logo is now the official artwork**, from Spirit's
`Spirit_logo_BlueTransparent_2.png` (1020 × 420). The originals are kept as
`assets/v2/spirit_logo_official_blue.png` and `spirit_logo_official_white.png`.

Every one of the 64 faces loads **`assets/v2/spirit_logo_navy.png`**, not the SVG.
That file is the official artwork placed on the old tracing's canvas shape
(1665 × 494, the same 3.37:1 ratio), with the "SPIRIT" cap height matched. So
no face's layout moved. Only the mark itself changed.

`assets/v2/spirit_logo.svg` and `spirit_logo_cream.png` are the old hand
tracing. No face uses them. Do not bring them back. For a dark background use
`spirit_logo_official_white.png`.

## TREC compliance

22 TAC §535.155(a)(2): the broker's name must be **at least half the size** of
the largest agent contact information on the piece. Contact information counts
name, phone, email, website and scan code.

The load-bearing constant: in `assets/v2/spirit_logo_navy.png`, the **"SPIRIT"
cap height is 0.1153 × the logo's rendered width**. It is measured on the
flat-topped T (192 px on the 1665 px canvas). All logo sizing derives from it.

The earlier constant, 0.1194, overstated the cap by 3.5%, and the checker let
ratios through up to 2.05×. Together those hid one real failure. The Warped
Checks card back had its broker name at 0.49× the 92 px agent name. Its logo
is now 410 px wide, which gives 0.51×. That face is the tightest in the suite.
Everything else has more room.

Re-run after any type or logo change:

```
python business_cards/export_tool/verify_trec.py
python business_cards/export_tool/render_faces.py business_cards <out dir> business_cards
python business_cards/export_tool/build_pdfs.py
```

`render_faces.py` writes to a separate out dir so you can compare before
copying over the committed PNGs. It needs Playwright and desktop Chrome.

A website has a **stricter** requirement than print. 22 TAC §531.20 wants the
IABS notice and the TREC Consumer Protection Notice linked on the homepage.
Both are in `website/index.html`, and the IABS link now opens `website/IABS_Spirit_Real_Estate_Group_Sophia_Reddehase.pdf`,
TREC's current IABS 1-2 form filled in from the TREC records (awaiting Bryan's OK).
The site mentions specials, so its footer carries the required disclaimer:
"Pricing and availability subject to change daily. All specials and effective
rents subject to property terms and leasing approval."

## Open items

1. **IABS form, confirm with Bryan.** Filled in from TREC: sponsoring broker Bryan Keith Bjerke
   dba Spirit Real Estate Group, #562021; sales agent Sophia Sky Reddehase, #831516. The designated
   broker and supervisor rows are blank because he is licensed as an individual. The old
   `IABSSophia.pdf` on Sophia's computer is the One Place Locators form. **Never use it.**
2. **Broker approval.** See below.
3. The root-level v1 pages (`index.html`, `pinterest_modern_business_cards.html`,
   `all_business_cards_showcase.html`, `app.js`, `styles.css`) had the brokerage
   name corrected but were not otherwise reviewed.

## Broker approval status

Sent 2026-09-10. Both links returned "Page not found", because artifact links
are private until sharing is switched on. Bryan replied: *"Please send me pdf's
or images."*

Re-sent 2026-09-11 as direct PDF download links off this repo. **The PDFs he
received show the old traced logo and "Spirit Real Estate Group, LLC".** The
PDFs in `business_cards/pdf/` have been rebuilt with the official logo and the
corrected name. He needs to look at the rebuilt set. **He has not approved any
design, so nothing goes to print.**
