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
  make_previews.py    ← one-off: regenerates WebP previews for assets/media (needs Pillow)
assets/logos/         ← standalone SVG masters (reference copies; the app embeds
                        its own copies inside brands.json)
  <pack>/             ← optional per-brand asset pack, wired up via "assetDir"
                        or "assetPacks" (see "Logo asset packs" below)
assets/fonts/         ← brand fonts embedded as @font-face data URIs (OFL, unmodified)
assets/media/<brand>/ ← full-res wallpapers, backgrounds, covers. NOT embedded:
                        deploy this folder next to index.html for the downloads
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

A brand with several packs uses `"assetPacks": [{"dir", "title", "hint", "compact"}]`
instead; each pack renders as its own section with its own "Download all" zip.
Filenames containing `favicon` and a size (`favicon-32-orange.svg`) get favicon labels.
A logo card can point at a pack file with `"asset": "<stem>"` instead of inline `svg`,
which is how PNG-only artwork is shown until an SVG master exists.

## Sidebar glyphs

`"glyph": {"light": "<file stem>", "dark": "<file stem>"}` names files from the
brand's asset pack to show in the sidebar, one per sidebar theme. Brands without a
glyph file fall back to a two-color tile made from `accent` / `accent2`.

## Media packs (full-res downloads)

`"mediaPacks": [{"dir": "tiugo/gradients", "title", "hint", "note"}]` lists every
PNG/JPG in `assets/media/<dir>/`. Only a small WebP preview is embedded; the card's
**Full-res** button links to the original file, so `assets/media/` must be deployed
alongside `index.html`. After adding or changing media, run
`python3 build/make_previews.py` (requires Pillow) before `build/build.py`.

## Brand fonts

A font entry with `"file"` (in `assets/fonts/`) and `"weightRange"` is embedded into
`index.html` as an `@font-face` data URI, so specimens render in the real typeface
with no external request. Aspekta and Lab Mono are SIL OFL 1.1 with Reserved Font
Names, so they ship **unmodified** (no subsetting) with their license files.

## Data provenance (important)

All design tokens were extracted from the **"Tiugo Brands Guidelines" Figma file**
(figma.com/design/gqUI3NDZ0TwPY24VrYEQYn) via the Figma MCP server, page by page:

| Brand      | Figma page        | Typefaces               | Notes |
|------------|-------------------|-------------------------|-------|
| Tiugo      | **Tiugo brand guidelines v1.0 (2026) PDF** — not Figma | Aspekta + Lab Mono (subs: Geist / Geist Mono) | Full rebrand: Orange 500 + warm neutrals, CMYK, color roles, contrast guide, logo rules, media |
| CKEditor   | `ckeditor.com` (0:1) | Mulish               | Palette incl. Lime/Deep Purple tint scales |
| Tiny       | `tiny.cloud` (4:696) | Inter + Fira Code    | Full heading/body/code scale, Navy tints |
| ButterCMS  | `buttercms.com` (27:9374) | Neuton + Open Sans | Token-scale palette (010–090) |
| Uploadcare | `uploadcare.com` (11:1199) | Inter Variable + Commit Mono | Only brand with a full written guide; dark identity |

Logo SVGs were taken **verbatim from the official brand websites** and verified
visually against the Figma logo sections. The Uploadcare glyph and lockups were
generated from the brand guide's own `LOGO_GRID` definition (8×8 cells,
pixel-to-cell ratio 0.85) and match the official lockups.

Tiugo (rebrand, Oct 2026): every hex, CMYK value, type style and guideline sentence
comes from the brandbook PDF text. Color roles, the usage scale and the contrast-guide
backgrounds were read from the PDF's vector fills, so they're exact. Logo files come
from the official logo pack (`Tiugo-logo-pack.zip`). The wordmark is PNG-only until
SVG masters are supplied.

Known gaps: CKEditor's Figma brandbook (gradient + icon rules) and Tiny's logo
variant frames were not fully extracted (their Figma pages exceeded the MCP metadata
size limit). Colors and typography for both are complete; only the deeper written
usage rules are missing.

## Editing rules (summary — see AGENTS.md)

1. Brand data lives in `build/brands.json` only. Never hand-edit the data blob
   inside `index.html`; run the build instead.
2. Logo SVGs are brand assets: never alter their paths, colors, or proportions.
3. Hex values come from Figma variables — they are facts, not suggestions.
