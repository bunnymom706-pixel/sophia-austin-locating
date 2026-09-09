# Flyers — Sophia Sky Reddehase · Spirit Real Estate Group

Four print-ready US Letter flyers, one per business-card style, all built to pass TREC advertising rules.

| # | Folder | Use it for | Print files |
|---|--------|-----------|-------------|
| 1 | `1_cherry_tearoff/` | Bulletin boards — coffee shops, gyms, laundromats, UT/ACC campus boards. Ten tear-off tabs with the phone number. | `print_ready/cherry_tearoff_*` |
| 2 | `2_marshmallow_free_locating/` | General "free apartment locating" hand-out. Matches the website palette. | `print_ready/marshmallow_free_locating_*` |
| 3 | `3_terracotta_relocation/` | Relocation / corporate — HR contacts, coworking spaces, hotels, property managers. More editorial. | `print_ready/terracotta_relocation_*` |
| 4 | `4_y2k_move_season/` | Lease-ending season — students, renters whose rent went up. Loudest of the four. | `print_ready/y2k_move_season_*` |

## Print specs

- **Trim size:** 8.5 × 11 in (US Letter). **With bleed:** 8.75 × 11.25 in (0.125 in each side).
- **PNG:** `*_LETTER_BLEED_300dpi.png` — 2625 × 3375 px, bleed included. Upload to Canva Print, Vistaprint, Moo, or a local shop; tell them the file **includes a 1/8 in bleed**.
- **PDF:** `*_LETTER_BLEED.pdf` — same artwork as a single-page PDF at 8.75 × 11.25 in. Preferred by most print shops.
- **Safe zone:** all text and logos sit ≥ 0.25 in inside the trim line.
- **Home / office printing:** print the PDF at 100 % (not "fit to page") on Letter and it will simply crop the bleed, or choose "fit" and accept a small white border.
- **Paper suggestion:** 100 lb gloss or silk text for hand-outs; 80 lb uncoated for the tear-off flyer so the tabs tear cleanly and people can write on it.
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

`shared/brand.js` looks for `assets/brand/spirit_logo.png` (the official file). If it's missing it rebuilds the logo from HTML/SVG (Montserrat wordmark + flame) so the flyer still renders. Drop the real PNG in `assets/brand/` and re-export to use the official artwork.

## Editing

Each flyer is a single self-contained `flyer.html`. Photos and QR codes are shared with the business cards (`business_cards/assets/v2/`). The QR codes point to `sparkapt.com/sophia-reddehase`.
