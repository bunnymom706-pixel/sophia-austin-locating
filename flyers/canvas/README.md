# Flyer design canvas

Four US Letter flyers as Design Component artboards, published as a Claude Design canvas.

**Current design: retro pop** (`build_retro.py`). Settled with Sophia on 2026-09-10 through a question
round: polished retro pop, full color, one color pairing per flyer, a mix of eras, patterns, letterforms
and headline shapes, a mix of headline tones, property photos only.

| Artboard | Pairing | Look |
|---|---|---|
| Tear-off | cherry red + cream | 60s mod, checker trim, Big Shoulders Display block letters, arch photo, 10 pull tabs |
| Free locating (Main) | pink + orange | 70s groovy, candy stripes, Shrikhand tilted headline, two polaroids |
| Relocation | orange + lilac | wave bands, Young Serif, curved eyebrow, circle photo, daisy |
| Move season | tomato red + hot pink | Titan One in a scalloped badge, scalloped photo, FREE burst |

Body and contact type is DM Sans on every sheet.

`build_canvas.py` is the earlier editorial design. Running it overwrites the same artboard files,
so only run `build_retro.py` unless you want the old look back.

## Rebuild

1. `python build_retro.py` writes the four `*.dc.html` files and `canvas.json`.
2. Re-seed the canvas with the images `tear_arch.jpg`, `free_pool.jpg`, `free_kitchen.jpg`,
   `reloc_circle.jpg`, `move_scallop.jpg` and `spirit_logo.png`, then republish.

## Print

- Trim 816 x 1056 px = 8.5 x 11 in at 96 px/in. Add a 0.125 in bleed in Canva.
- Canvas PNG/PDF export falls back to Georgia / Impact / Arial Black, so headlines keep slack.
- Photos are Sophia's own iPhone 17 captures cropped per frame (see `../shared/photos/SOURCES.json`).
- The QR is drawn inline from `qr_path.txt` at 148 px with a 4 module quiet zone and decodes to
  https://sparkapt.com/inquiry/sophia-reddehase859 (checked with an OpenCV decode of the render).
  app.sparkapt.com/guest-cards was considered and rejected: logged-out renters are redirected to the
  SparkAPT sign-in page.
- No em dashes anywhere (house rule).

## TREC

Measured in the rendered artboards: the phone is the largest contact line at 34 px; the broker line
"Brokered by Spirit Real Estate Group" is 20 px and the Spirit wordmark inside the 70 px logo reads
about 33 px, so both clear the half-size rule in 22 TAC 535.155. Every sheet carries the sponsored-agent
line, TREC #831516, the IABS and Consumer Protection Notice reference, the explanation that locating is
free because the property pays, the daily pricing and specials disclaimer, and the Equal Housing
Opportunity mark. Each tear-off tab names Spirit Real Estate Group.
