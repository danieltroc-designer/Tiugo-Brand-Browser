#!/usr/bin/env python3
"""Build index.html from template.html + brands.json.

Usage:  python3 build/build.py
Output: ./index.html (repo root) — a single self-contained static file.

Icons are file-driven: any .svg dropped into assets/icons/<brand-id>/ (or
assets/icons/common/ for all brands) is embedded into that brand's `icons`
data field at build time. See assets/icons/README.md for the convention.
"""
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
BUILD = ROOT / "build"
ICONS_DIR = ROOT / "assets" / "icons"

_XML_PROLOG = re.compile(r"^\s*<\?xml[^>]*\?>\s*", re.IGNORECASE)
_DOCTYPE = re.compile(r"^\s*<!DOCTYPE[^>]*>\s*", re.IGNORECASE)


def _title(stem: str) -> str:
    """Turn a filename stem into a display name: arrow-right -> 'Arrow Right'."""
    words = [w for w in re.split(r"[-_\s]+", stem.strip()) if w]
    return " ".join(w[:1].upper() + w[1:] for w in words)


def _clean_svg(text: str) -> str:
    text = _XML_PROLOG.sub("", text)
    text = _DOCTYPE.sub("", text)
    return text.strip()


def _natkey(path: pathlib.Path):
    """Natural sort: 'x-2' before 'x-10' (not lexicographic)."""
    return [int(t) if t.isdigit() else t.lower() for t in re.split(r"(\d+)", path.name)]


def load_icons(brand_id: str) -> list:
    """Collect icons for a brand: common/ folder first, then the brand folder."""
    icons, seen = [], set()
    for folder in (ICONS_DIR / "common", ICONS_DIR / brand_id):
        if not folder.is_dir():
            continue
        for svg_file in sorted(folder.glob("*.svg"), key=_natkey):
            name = _title(svg_file.stem)
            key = name.lower()
            svg = _clean_svg(svg_file.read_text(encoding="utf-8"))
            if not svg or key in seen:
                seen.add(key)
                continue
            seen.add(key)
            keywords = re.sub(r"[-_]+", " ", svg_file.stem).lower()
            icons.append({"name": name, "keywords": keywords, "svg": svg})
    return icons


def main() -> None:
    template = (BUILD / "template.html").read_text(encoding="utf-8")
    brands = json.loads((BUILD / "brands.json").read_text(encoding="utf-8"))

    # Merge file-driven icons into each brand's `icons` field. Any icons already
    # authored in brands.json are kept and take precedence over file duplicates.
    icon_total = 0
    for brand in brands:
        authored = brand.get("icons", []) or []
        authored_names = {ic.get("name", "").lower() for ic in authored}
        file_icons = [ic for ic in load_icons(brand["id"]) if ic["name"].lower() not in authored_names]
        brand["icons"] = authored + file_icons
        icon_total += len(brand["icons"])

    # Compact JSON; escape "</" so inline <script> can never be closed early.
    payload = json.dumps(brands, ensure_ascii=False, separators=(",", ":"))
    payload = payload.replace("</", "<\\/")

    out = template.replace("__BRANDS_JSON__", payload)
    (ROOT / "index.html").write_text(out, encoding="utf-8")
    print(f"index.html written ({len(out):,} bytes, {len(brands)} brands, {icon_total} icons)")


if __name__ == "__main__":
    main()
