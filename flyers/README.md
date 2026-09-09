# Flyers — Sophia Sky Reddehase · Spirit Real Estate Group

Four print-ready US Letter flyers, one editorial design system, all built to pass TREC advertising rules.

| # | Folder | Use it for | Print files |
|---|--------|-----------|-------------|
| 1 | `1_tearoff/` | Bulletin boards — coffee shops, gyms, laundromats, UT/ACC campus boards. Ten tear-off tabs with the phone number. | `print_ready/tearoff_*` |
| 2 | `2_free_locating/` | General "free apartment locating" hand-out. Why it's free + how it works in three steps. | `print_ready/free_locating_*` |
| 3 | `3_relocation/` | Relocation / corporate — HR contacts, coworking spaces, hotels, property managers. Neighborhood index. | `print_ready/relocation_*` |
| 4 | `4_move_season/` | Lease-ending season — renters whose renewal just went up. | `print_ready/move_season_*` |

## Design system

Luxury-real-estate treatment, built from the website's own faces so print and web match: **Cormorant Garamond**
(light, for headlines), **Italiana** (the name wordmark), **Plus Jakarta Sans** (letter-spaced labels and body).
Ivory / charcoal / champagne-gold palette, a thin double-line frame inset from the trim, centered composition,
arch-framed or full-bleed interior photography, and the same footer (contact, broker line, compliance) on every sheet.
Shared styles live in `shared/luxury.css`; each flyer only sets its palette and layout on top. Photos in `shared/photos/`
are Sophia's own tour photography (exported from her iCloud camera roll, HEIC converted to JPG at up to 2400 px). The
captions name the feature only (pool, kitchen, model residence), not a property or neighborhood, so nothing on the sheet
has to be re-verified when a community changes hands. Every file was shot on Sophia's own phone: her selfies from May through September 2026 are all iPhone 17, so only iPhone 17
captures are allowed here (iPhone 13 and iPhone 15 files in the roll were shared in by other people and are rejected).
`shared/photos/SOURCES.json` records the source file and camera for each photo. Sources: clubhouse pool IMG_4145,
sunset courtyard pool IMG_4324, kitchen IMG_4169, model living room IMG_4102, clubhouse lounge IMG_4323, clubhouse
lobby IMG_4321, arched facade IMG_4247.

## Print specs

- **Trim size:** 8.5 × 11 in (US Letter). **With bleed:** 8.75 × 11.25 in (0.125 in each side).
- **PNG:** `*_LETTER_BLEED_300dpi.png` — 2625 × 3375 px, bleed included, tagged 300 dpi. Upload to Canva Print, Vistaprint, Moo, or a local shop; tell them the file **includes a 1/8 in bleed**.
- **Canva Print:** `print_ready/canva/*.jpg` — same artwork as JPG (quality 95, 300 dpi tag). In Canva: Create a design → Custom size → 8.75 × 11.25 in → Upload → drag the JPG to fill the page → Share → Print your design → Flyers, Letter. Canva's bleed lines will sit exactly on the artwork's 0.125 in margin; nothing needs to be moved. Run `python flyers/export_tool/canva_prep.py` after `export.js` to regenerate.
- **PDF:** `*_LETTER_BLEED.pdf` — same artwork as a single-page PDF at 8.75 × 11.25 in. Preferred by most print shops.
- **Safe zone:** all text and logos sit ≥ 0.25 in inside the trim line.
- **Home / office printing:** print the PDF at 100 % (not "fit to page") on Letter and it will simply crop the bleed, or choose "fit" and accept a small white border.
- **Paper suggestion:** 100 lb silk or soft-touch for hand-outs (matte finish, never gloss — it fights the ivory); 80 lb uncoated for the tear-off flyer so the tabs tear cleanly.
- **Layout guard:** the export fails if a flyer's content overflows the page box (footer would leave the safe zone).
- **Screen previews:** `preview/*.png` (840 × 1080) — for the showcase page and quick checks, not for print.

## TREC compliance (22 TAC §535.154 / §535.155)

Every flyer carries, and `export_tool/export.js` verifies on each render:

- **Broker's name** — "Brokered by Spirit Real Estate Group", in a readily noticeable location, at **≥ ½ the font size of the largest contact info** (name, phone, email, Instagram, URL). Elements are tagged `data-trec="contact"` / `data-trec="broker"` so the check is automatic. Change the sizes and the check will fail the build if the ratio breaks.
- **Sales agent identified** — Sophia Sky Reddehase, TREC License #831516, described as a *sales agent sponsored by* the broker (never as owner, broker, or "realty").
- **IABS + Consumer Protection Notice** referenced with where to get them (trec.texas.gov). Required on your website homepage; on print it's best practice and reassures property managers.
- **"Free" claim explained** — "free to you; the agent is compensated by the property you lease", so the ad is not materially misleading.
- **Pricing / specials disclaimer** — no specific rents or "X weeks free" promised.
- **Equal Housing Opportunity** mark.

Things the flyers deliberately avoid: referral-fee offers (paying unlicensed people for referrals is prohibited), rebate offers (must disclose full terms), any team/company name that could imply Sophia is the broker.

> Confirm with your broker that **"Spirit Real Estate Group"** is exactly the broker name / assumed name registered with TREC. If TREC has it as something else (e.g. with "LLC"), change the text in the `.broker .txt` element and the compliance paragraph in each flyer.

## Rebuilding

```bash
node flyers/export_tool/export.js        # all four → print_ready/ + preview/, runs TREC checks
node flyers/export_tool/export.js 1 4    # only flyers 1 and 4
```

Needs Node and Playwright with Chromium (`npm i -g playwright && npx playwright install chromium`). Fonts are bundled in `shared/fonts/` so rendering works offline; `export_tool/fetch_fonts.py` re-downloads them if you add a family.

While designing, add `class="guides"` to `<body>` to show the trim (red) and safe (blue) lines. The export fails if you forget to remove it.

## Spirit logo

`shared/brand.js` loads the official lockup from `assets/brand/spirit_logo.png` (navy) or `spirit_logo_white.png` on the
dark flyer. The footer sizes it so the SPIRIT wordmark reads about 22.7 px against the 30 px name, and `export.js` fails the
build if the PNG did not load or the wordmark drops under half the largest contact line. If the PNGs are missing the logo is
rebuilt from HTML/SVG so the flyer still renders.

## Editing

Each flyer is a single self-contained `flyer.html`. QR codes are SVG in `shared/qr/` (navy, cream, ink, red) and point to
`https://sparkapt.com/inquiry/sophia-reddehase859` — the same link as the website's "Start Free Search" button. Regenerate with
`python3 -c "import segno; ..."` (see git history) if the link changes.
