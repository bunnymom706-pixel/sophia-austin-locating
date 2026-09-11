# Sophia Sky Reddehase — brand suite handoff

Everything built for the apartment-locating business: 16 business card styles,
16 matching square flyers, review PDFs, and a website. This file is the state
of play so another session can pick up without re-deriving any of it.

## Who

| | |
|---|---|
| Agent | Sophia Sky Reddehase |
| License | TREC #831516 |
| Brokerage | Spirit Real Estate Group, LLC |
| Broker | Bryan Bjerke (bryan.bjerke@spiritre.com), TREC Lic. 9003398 & 562021 |
| Phone | (512) 676-1215 |
| Email | sophia.reddehase@spiritre.com |
| Profile | sparkapt.com/sophia-reddehase |
| Intake form | https://sparkapt.com/inquiry/sophia-reddehase859 |
| Market | Austin & surrounding areas |
| Services | Relocation · second chance (eviction / broken lease) · first-time renters · luxury |
| Offer | Free to renters; the property pays the locator fee |

## What exists

| Where | What |
|---|---|
| `business_cards/cards_v2/{1..16}_*/` | 32 card faces as HTML |
| `business_cards/print_ready_images/v2/` | 32 card PNGs, 300 DPI |
| `business_cards/flyers/{1..16}_*/` | 32 flyer faces as HTML |
| `business_cards/print_ready_flyers/` | 32 flyer PNGs, 1725×1725 |
| `business_cards/pdf/` | 3 review PDFs for the broker |
| `website/index.html` | One-page site, self-contained |
| `business_cards/flyer_tool/gen_flyers.py` | Generates all 32 flyer faces |
| `business_cards/export_tool/build_pdfs.py` | Builds the 3 review PDFs |
| `business_cards/export_tool/verify_trec.py` | Broker-name ratio checker |

### Print geometry

| Format | File px @300 DPI | Trim | Bleed |
|---|---|---|---|
| Landscape card | 1125 × 675 | 3.5 × 2.0 in | 37.5 px |
| Vertical card | 675 × 1125 | 2.0 × 3.5 in | 37.5 px |
| Square card | 825 × 825 | 2.5 × 2.5 in | 37.5 px |
| Square flyer | 1725 × 1725 | 5.5 × 5.5 in | 37.5 px, 110 px corner radius |

## TREC compliance

22 TAC §535.155(a)(2): the broker's name must be **at least half the size** of
the largest agent contact information on the piece. Contact information counts
name, phone, email, website and scan code.

The load-bearing constant: in `assets/v2/spirit_logo.svg`, the **"SPIRIT" cap
height is 0.1194 × the logo's rendered width**. All sizing derives from that.

Verified across all 64 faces. Cards and flyers both pass with margin; the
tightest is 0.56× against a 0.50× floor. Re-run after any type change:

```
python3 business_cards/export_tool/build_pdfs.py   # also re-exports review PDFs
```

A website has a **stricter** requirement than print. 22 TAC §531.20 wants the
IABS notice and the TREC Consumer Protection Notice linked on the homepage.
Both are in `website/index.html`, but **the IABS link is still a placeholder**
pointing at TREC's blank form. It must be swapped for Spirit's completed IABS
PDF (the one carrying Bryan's name and license numbers) before the site is used.

## Open items

1. **Spirit logo is a redrawing, not the official asset.** `assets/v2/spirit_logo.svg`
   was traced from a screenshot over three passes; the wordmark is Montserrat
   standing in for the original's geometric sans. This container's network
   reaches only `raw.githubusercontent.com` and `s3.amazonaws.com` — 18 hosts
   were tested, including every Google Images CDN — so the real file could not
   be downloaded. **Every one of the 64 faces references the same path**, so
   dropping the official artwork in at `business_cards/assets/v2/` updates the
   whole suite in one move.
2. **Spirit's completed IABS PDF** for the website footer (see above).
3. **Confirm the licensed brokerage name** is "Spirit Real Estate Group, LLC"
   and that "Sky" is registered with TREC if the license reads "Sophia Reddehase".

## Broker approval status

Sent 2026-09-10, both returned "Page not found" — artifact links are private
until sharing is switched on. Bryan replied: *"Please send me pdf's or images."*

Re-sent 2026-09-11 as direct PDF download links off this public repo (verified
HTTP 200, no sign-in). **Awaiting his approval.** He has not approved any design
yet, so nothing should go to print.
