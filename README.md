# Tiugo Brand Browser

A single-file static web app where anyone can browse and copy brand assets for the
Tiugo Technologies family of brands: **Tiugo Technologies, CKEditor, Tiny (TinyMCE),
ButterCMS, and Uploadcare**.

Features per brand: logo cards with **Copy SVG / Download**, click-to-copy color
swatches with a **HEX / RGB** toggle, live typography specimens set in the real
typefaces, written usage guidelines, and one-click export of the whole token set as
**CSS variables** or **JSON**. The UI chrome retints itself in the selected brand's
accent colors; Uploadcare renders in its native dark theme.

## Repo layout

```
index.html            ← the entire app, built. Deploy this file, nothing else.
build/
  template.html       ← app source: all markup, CSS, and JS (data injected at build)
  brands.json         ← single source of truth for all brand data
  build.py            ← injects brands.json into template.html → ../index.html
assets/logos/         ← standalone SVG masters (reference copies; the app embeds
                        its own copies inside brands.json)
  <pack>/             ← optional per-brand asset pack, wired up via "assetDir"
                        (see "Logo asset packs" below)
AGENTS.md             ← working rules for AI agents (Cursor picks this up)
PROMPT.md             ← kickoff prompt for the Cursor agent
```

## Build & run

```bash
python3 build/build.py   # regenerates index.html
open index.html          # no server, no dependencies, no build chain
```

Deploy = upload `index.html` anywhere static (Netlify Drop, Vercel, S3, GitHub Pages).
The only external requests are Google Fonts.

## Logo asset packs

To publish a set of ready-made logo exports, drop the files into
`assets/logos/<pack>/` and point a brand — or one of its variants — at the folder:

```json
{ "assetDir": "uploadcare-new" }
```

The build embeds every `.svg` and `.png` in that folder into an `assetFiles` field
and the app renders an **Asset files** section, so downloads hand back the original
bytes instead of a re-render. Files sharing a stem (`lockup-dark.svg` +
`lockup-dark.png`) collapse into one card offering both formats.

Filenames drive the presentation, so name them in kebab-case using these keywords:

| Keyword                        | Effect |
|--------------------------------|--------|
| `lockup` / `glyph` / `wordmark` | Sets the card title |
| `dark` / `light`               | Which surface the artwork is *for* — picks the preview stage |
| `padded`                       | Noted as shipping with clear space baked in |
| `transparent`                  | Noted as having a transparent background |

PNGs are embedded as base64, so a pack of any size grows `index.html` — keep exports
reasonably sized to protect the single-file deliverable.

## Data provenance (important)

All design tokens were extracted from the **"Tiugo Brands Guidelines" Figma file**
(figma.com/design/gqUI3NDZ0TwPY24VrYEQYn) via the Figma MCP server, page by page:

| Brand      | Figma page        | Typefaces               | Notes |
|------------|-------------------|-------------------------|-------|
| Tiugo      | `Tiugo` (8:1457)  | Poppins                 | Full type scale + 3 color tiers |
| CKEditor   | `ckeditor.com` (0:1) | Mulish               | Palette incl. Lime/Deep Purple tint scales |
| Tiny       | `tiny.cloud` (4:696) | Inter + Fira Code    | Full heading/body/code scale, Navy tints |
| ButterCMS  | `buttercms.com` (27:9374) | Neuton + Open Sans | Token-scale palette (010–090) |
| Uploadcare | `uploadcare.com` (11:1199) | Inter Variable + Commit Mono | Only brand with a full written guide; dark identity |

Logo SVGs were taken **verbatim from the official brand websites** and verified
visually against the Figma logo sections. The Uploadcare glyph and lockups were
generated from the brand guide's own `LOGO_GRID` definition (8×8 cells,
pixel-to-cell ratio 0.85) and match the official lockups.

Known gaps: CKEditor's Figma brandbook (gradient + icon rules) and Tiny's logo
variant frames were not fully extracted (their Figma pages exceeded the MCP metadata
size limit). Colors and typography for both are complete; only the deeper written
usage rules are missing.

## Editing rules (summary — see AGENTS.md)

1. Brand data lives in `build/brands.json` only. Never hand-edit the data blob
   inside `index.html`; run the build instead.
2. Logo SVGs are brand assets: never alter their paths, colors, or proportions.
3. Hex values come from Figma variables — they are facts, not suggestions.
