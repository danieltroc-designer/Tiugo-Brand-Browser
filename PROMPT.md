# PROMPT.md — kickoff prompt for the Cursor agent

Copy everything below the line into the Cursor agent chat with this folder open
as the workspace. Delete backlog items you don't want; add your own.

---

You're taking over the **Tiugo Brand Browser** — a finished, working v1 that I want
to iterate on. Before writing any code:

1. Read `README.md` (architecture + where the data came from) and `AGENTS.md`
   (hard rules — especially: never edit `index.html` directly, never touch logo
   SVGs or brand token values).
2. Run `python3 build/build.py`, open the generated `index.html`, and click through
   all five brands so you understand the current behavior: accent retint on brand
   switch, Uploadcare's dark theme, Copy SVG, swatch copy with HEX/RGB toggle,
   live type specimens, CSS/JSON token export.
3. Give me a one-paragraph summary of how the app works and confirm the build runs,
   then start on the backlog. Work one item at a time, show me the result after
   each, and don't start the next item until I confirm.

## Backlog (in priority order)

1. **Deploy readiness.** Add a favicon and social/OG meta (use the Tiugo icon —
   derive the favicon from `assets/logos/tiugo-logo.svg` without altering the
   original file). Add a `vercel.json` or `netlify.toml` so the repo deploys
   as a static site with `index.html` at the root.
2. **PNG export.** Next to "Copy SVG" / "Download", add "PNG" with 1×/2×/4×
   options, rendered client-side from the embedded SVG via canvas. Transparent
   background; keep the exact SVG geometry.
3. **Quick search.** A `⌘K` command palette that jumps to any brand, color
   (searchable by name or hex), or section. Keyboard shortcuts 1–5 switch brands.
4. **Logo background preview toggle.** On each logo card, let the viewer flip the
   stage between light / dark / checkerboard to judge contrast — display only,
   never changing the SVG itself.
5. **Copy improvements.** Swatch right-click (or a small menu) offering the value
   as HEX, RGB, HSL, or a CSS custom property line.
6. **Print/PDF one-pager per brand.** A print stylesheet so each brand page prints
   as a clean single-page brand sheet.

## Constraints (repeated because they matter)

- Single self-contained `index.html`; no framework, no bundler, no npm.
- Source of truth is `build/brands.json` + `build/template.html`; always rebuild
  with `python3 build/build.py`.
- Logo SVGs and all brand token values are immutable facts from the brand
  guidelines. If something looks inconsistent, ask me instead of changing it.
- Keep the accessibility floor: focus styles, reduced motion, mobile layout.
