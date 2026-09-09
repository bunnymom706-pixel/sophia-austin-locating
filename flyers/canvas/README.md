# Flyer design canvas

Four US Letter flyers as Design Component artboards, published as a Claude Design canvas.

- `build_canvas.py` generates the four `*.dc.html` artboards and `canvas.json`. Edit the script,
  re-run it, then re-seed and republish the canvas.
- Trim 816 x 1056 px = 8.5 x 11 in at 96 px/in. No bleed on the artboards; add 0.125 in in Canva.
- Type: Instrument Serif (display) + Archivo (labels), Google Fonts. PNG/PDF export from the canvas
  falls back to Georgia / Helvetica, so headlines carry ~10% slack.
- Palette: warm cream and warm white paper, deep pine and espresso fields, clay and brass accents.
- Photos are Sophia's own iPhone 17 captures, cropped to each slot (see `../shared/photos/SOURCES.json`).
- No em dashes anywhere (house rule).
- The QR is drawn inline from `qr_path.txt` at 160 px (1.67 in) with a 4 module quiet zone. It decodes
  to https://sparkapt.com/inquiry/sophia-reddehase859, verified with an OpenCV decode of the rendered code.

## TREC

Measured in the rendered artboards: largest contact info is the phone at 34 px; the broker line
"Brokered by Spirit Real Estate Group" is 22 px (0.65) and the Spirit wordmark inside the logo is
about 37 px (1.09). Both clear the half-size rule in 22 TAC 535.155. Every sheet also carries the
sponsored-agent line, TREC #831516, the IABS and Consumer Protection Notice reference, the
explanation that locating is free because the property pays, the daily-pricing disclaimer, and the
Equal Housing Opportunity mark.
