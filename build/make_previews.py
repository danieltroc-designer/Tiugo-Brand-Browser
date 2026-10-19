#!/usr/bin/env python3
"""Generate small WebP previews for full-resolution media under assets/media/.

Usage:  python3 build/make_previews.py        (requires Pillow: pip install pillow)

Every .png/.jpg in assets/media/<brand>/<pack>/ gets a sibling
_previews/<stem>.webp, which build.py embeds into index.html. The full-res
originals are never touched; they ship next to index.html for download.
Run this only when media files change — build.py itself has no dependencies.
"""
import pathlib

from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent.parent
MEDIA = ROOT / "assets" / "media"
MAX_W, MAX_H, QUALITY = 640, 400, 72


def main() -> None:
    count = 0
    for src in sorted(MEDIA.rglob("*")):
        if src.suffix.lower() not in (".png", ".jpg", ".jpeg") or "_previews" in src.parts:
            continue
        out = src.parent / "_previews" / f"{src.stem}.webp"
        if out.exists() and out.stat().st_mtime >= src.stat().st_mtime:
            continue
        out.parent.mkdir(exist_ok=True)
        with Image.open(src) as im:
            im = im.convert("RGBA") if im.mode in ("RGBA", "LA", "P") else im.convert("RGB")
            im.thumbnail((MAX_W, MAX_H), Image.LANCZOS)
            im.save(out, "WEBP", quality=QUALITY, method=6)
        count += 1
        print(f"{out.relative_to(ROOT)}  ({out.stat().st_size // 1024} KB)")
    print(f"{count} preview(s) written")


if __name__ == "__main__":
    main()
