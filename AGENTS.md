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
- Fonts: Aspekta (all UI text, embedded from `assets/fonts/AspektaVF.woff2`),
  JetBrains Mono (values, labels). Brand specimen text uses each brand's real typefaces.
- **Tokens first.** The top of the stylesheet defines every design value; component
  rules reference tokens instead of raw numbers:
  - Color roles: `--paper` `--card` `--line` `--line-strong` `--ink` `--ink-2`
    `--ink-3` `--accent` `--on-accent` `--danger` `--pass` `--fail` (dark mode
    overrides them on `body.theme-dark`).
  - Type: `--text-micro` 11 · `caption` 12 · `footnote` 13 · `subhead` 14 · `body`
    15 · `callout` 17 · `title3` 20 · `title2` 24 · `title1` 28 · `large` 32 ·
    `display`; tracking `--track-display/title/head` (tighter as size grows).
  - Spacing: `--sp-N` = N × 4px (`--sp-0h` 2px, `--sp-1h` 6px), plus
    `--section-gap`, `--grid-gap`, `--grid-gap-sm`, `--card-pad`.
  - Shape `--r-xs/sm/md/lg/xl/pill`; motion `--ease`, `--dur-press/fast/move/theme`;
    elevation `--shadow-1/2`, `--material`, `--blur`.
  Add a token before adding a new one-off value.
- **Components:** `.btn` (+ `.primary`), the shared card surface, `.seg` segmented
  control, `.sec-h` section header, `.sub-h` / `.sub-note`, `.ftags` file metadata,
  `.toc-float` / `.toc-inline`, `.toast`. Reuse them before inventing new ones.
- **UI icons are Lucide** (https://lucide.dev, ISC), inlined in the `LUCIDE` map in
  `template.html` and rendered with `icon(name)`. Copy new icons verbatim from the
  `lucide-static` package; never hand-draw UI icons. Brand icons and logos are
  separate and stay untouched.
- UI copy stays plain: no eyebrow labels (small mono uppercase kickers above
  headings), no pill-chip clusters, no filler hints or em-dash taglines. Sub-labels
  are sentence-case Aspekta; JetBrains Mono is for values only (hex, sizes, files).
- Motion: press feedback on `:active` (scale .97), hover styles only inside
  `@media (hover:hover)`, and keep the reduced-motion / reduced-transparency /
  high-contrast blocks at the end of the stylesheet.
- The "On this page" menu floats in a sticky rail right of the sidebar (≥1100px),
  sits under the active brand on medium screens, and is hidden ≤840px. It is built from the rendered `#overview` and
  `section[id]` elements (label = the section's `h3`), so new sections appear there
  automatically.
- Preserve the accessibility floor: visible `:focus-visible` styles,
  `prefers-reduced-motion` handling, semantic buttons, `aria-live` toast,
  responsive layout down to ~390px.

## Verification checklist before declaring a task done

1. `python3 build/build.py` runs clean and `index.html` size looks sane (~90 KB+).
2. Open `index.html`: all five brands switch correctly, Uploadcare goes dark.
3. Copy SVG, swatch copy, HEX/RGB toggle, and both token exports still work.
4. No console errors; no external requests besides Google Fonts.
5. Mobile viewport (≤840px): sidebar collapses to a horizontal brand strip.
