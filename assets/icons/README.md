# Icon library — drop-in SVGs

Drop `.svg` files into these folders and run `python3 build/build.py`. Each file
becomes one icon in that brand's **Icons** section (with copy + download + search).

## Where files go

```
assets/icons/
  common/       ← icons shown for EVERY brand (shared UI glyphs)
  tiugo/        ← icons shown only on the Tiugo page
  ckeditor/     ← …CKEditor
  tiny/         ← …Tiny
  buttercms/    ← …ButterCMS
  uploadcare/   ← …Uploadcare
```

Folder names match the brand `id` in `build/brands.json`. A brand shows
`common/` icons first, then its own folder. Duplicate names (case-insensitive)
are de-duplicated, with the brand-specific file winning.

## Naming

The **file name** becomes the icon name and its search keywords:

| File                  | Icon name     | Searchable by            |
| --------------------- | ------------- | ------------------------ |
| `arrow-right.svg`     | `Arrow Right` | arrow, right             |
| `cloud_upload.svg`    | `Cloud Upload`| cloud, upload            |
| `search.svg`          | `Search`      | search                   |

Hyphens and underscores become spaces; words are Title-Cased.

## Tips

- Author glyphs with `stroke="currentColor"` or `fill="currentColor"` so they
  automatically retint for light/dark themes. Hard-coded colors are kept as-is.
- Keep a consistent `viewBox` (e.g. `0 0 24 24`) for even sizing.
- No build chain or optimization runs on these files — the raw SVG is embedded
  verbatim, so what you drop in is exactly what users copy/download.
- The download filename is `{brand}-icon-{name}.svg`.
