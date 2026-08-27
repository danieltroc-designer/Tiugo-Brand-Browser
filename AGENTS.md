# AGENTS.md — working rules for this repo

You are working on the **Tiugo Brand Browser**: a single-file static brand-asset hub
for five brands (Tiugo Technologies, CKEditor, Tiny, ButterCMS, Uploadcare).
Read `README.md` first for architecture and data provenance.

## Architecture invariants

- **Single-file output.** The deliverable is one self-contained `index.html` with no
  build chain at runtime, no framework, no bundler, and no external dependencies
  except Google Fonts. Do not introduce npm, React, or a dev server unless the user
  explicitly asks.
- **Source vs. artifact.** `build/template.html` + `build/brands.json` are the
  source; `index.html` is generated. After any source change, run
  `python3 build/build.py` and verify the output. Never edit `index.html` directly.
- **Data-driven rendering.** All brand content renders from the `BRANDS` array.
  New content types (e.g. gradients, icon rules) should be added as data fields in
  `brands.json` plus a renderer in `template.html`, never hardcoded per brand.

## Brand-integrity rules (non-negotiable)

- **Never modify logo SVGs** — no recoloring, no path edits, no proportion changes,
  no "optimization" that alters geometry. They are verbatim brand assets.
- **Never invent or adjust brand colors, type sizes, or guideline text.** Every
  token in `brands.json` was extracted from the Tiugo Brands Guidelines Figma file.
  If a value seems wrong, flag it to the user; do not "fix" it.
- The Uploadcare glyph is generated from `LOGO_GRID` (8×8 cells, ratio 0.85 for
  general use). If glyph code is ever regenerated, keep that exact grid and ratio.
- Uploadcare is a dark-identity brand: its page must keep `theme-dark`.

## Design system of the app itself

- Chrome is deliberately neutral (paper `#FAFAF8`, ink `#16161A`, hairlines) so the
  brands' own colors carry the personality. The signature interaction is the
  accent retint on brand switch (`--accent` / `--accent-2` on `document.body`).
- Fonts: Archivo (display/UI headings), Inter (UI body), JetBrains Mono (values,
  labels). Brand specimen text uses each brand's real typefaces.
- Preserve the accessibility floor: visible `:focus-visible` styles,
  `prefers-reduced-motion` handling, semantic buttons, `aria-live` toast,
  responsive layout down to ~390px.

## Verification checklist before declaring a task done

1. `python3 build/build.py` runs clean and `index.html` size looks sane (~90 KB+).
2. Open `index.html`: all five brands switch correctly, Uploadcare goes dark.
3. Copy SVG, swatch copy, HEX/RGB toggle, and both token exports still work.
4. No console errors; no external requests besides Google Fonts.
5. Mobile viewport (≤840px): sidebar collapses to a horizontal brand strip.
