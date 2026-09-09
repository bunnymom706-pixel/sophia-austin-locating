# Flyers — Sophia Sky Reddehase · Spirit Real Estate Group

Four print-ready US Letter flyers, one editorial design system, all built to pass TREC advertising rules.

| # | Folder | Use it for | Print files |
|---|--------|-----------|-------------|
| 1 | `1_tearoff/` | Bulletin boards — coffee shops, gyms, laundromats, UT/ACC campus boards. Ten tear-off tabs with the phone number. | `print_ready/tearoff_*` |
| 2 | `2_free_locating/` | General "free apartment locating" hand-out. Why it's free + how it works in three steps. | `print_ready/free_locating_*` |
| 3 | `3_relocation/` | Relocation / corporate — HR contacts, coworking spaces, hotels, property managers. Neighborhood index. | `print_ready/relocation_*` |
| 4 | `4_move_season/` | Lease-ending season — renters whose renewal just went up. | `print_ready/move_season_*` |

## Design system

One editorial system across all four so they read as a set: **Instrument Serif** for display, **Inter** for text, a strict
left-aligned grid with 60 px margins, hairline rules, and the same footer (contact, broker line, compliance) on every sheet.
No photography — the type carries it. Colorways: cream/navy (1), navy/cream with gold (2), white/navy (3), signal red/cream (4).
Shared styles live in `shared/editorial.css`; each flyer only sets its palette and layout on top.

## Print specs

- **Trim size:** 8.5 × 11 in (US Letter). **With bleed:** 8.75 × 11.25 in (0.125 in each side).
- **PNG:** `*_LETTER_BLEED_300dpi.png` — 2625 × 3375 px, bleed included. Upload to Canva Print, Vistaprint, Moo, or a local shop; tell them the file **includes a 1/8 in bleed**.
- **PDF:** `*_LETTER_BLEED.pdf` — same artwork as a single-page PDF at 8.75 × 11.25 in. Preferred by most print shops.
- **Safe zone:** all text and logos sit ≥ 0.25 in inside the trim line.
- **Home / office printing:** print the PDF at 100 % (not "fit to page") on Letter and it will simply crop the bleed, or choose "fit" and accept a small white border.
- **Paper suggestion:** 100 lb uncoated or silk text for hand-outs (the serif/cream look wants matte, not gloss); 80 lb uncoated for the tear-off flyer so the tabs tear cleanly.
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

`shared/brand.js` looks for `assets/brand/spirit_logo.png` (the official file). If it's missing it rebuilds the logo from HTML/SVG (Montserrat wordmark + flame) so the flyer still renders. Drop the real PNG in `assets/brand/` and re-export to use the official artwork.

## Editing

Each flyer is a single self-contained `flyer.html`. QR codes are SVG in `shared/qr/` (navy, cream, ink, red) and point to
`https://sparkapt.com/inquiry/sophia-reddehase859` — the same link as the website's "Start Free Search" button. Regenerate with
`python3 -c "import segno; ..."` (see git history) if the link changes.
