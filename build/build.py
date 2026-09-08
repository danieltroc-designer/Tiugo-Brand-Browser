#!/usr/bin/env python3
"""Build index.html from template.html + brands.json.

Usage:  python3 build/build.py
Output: ./index.html (repo root) — a single self-contained static file.

Icons are file-driven: any .svg dropped into assets/icons/<brand-id>/ (or
assets/icons/common/ for all brands) is embedded into that brand's `icons`
data field at build time. See assets/icons/README.md for the convention.

Logo asset packs are file-driven too: set "assetDir": "<folder>" on a brand (or
on one of its variants) and every .svg/.png in assets/logos/<folder>/ is
embedded into an `assetFiles` field, grouped by filename, ready to download.
"""
import base64
import json
import pathlib
import re
import struct

ROOT = pathlib.Path(__file__).resolve().parent.parent
BUILD = ROOT / "build"
ICONS_DIR = ROOT / "assets" / "icons"
LOGOS_DIR = ROOT / "assets" / "logos"

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


def _dim(value: float) -> str:
    """1024.0 -> '1024', 92.7758 -> '92.78'."""
    return str(int(value)) if float(value).is_integer() else f"{value:.2f}".rstrip("0")


def _svg_size(svg: str):
    """Read intrinsic size from viewBox, falling back to width/height."""
    box = re.search(r'viewBox="([^"]+)"', svg)
    if box:
        parts = box.group(1).replace(",", " ").split()
        if len(parts) == 4:
            return f"{_dim(float(parts[2]))}×{_dim(float(parts[3]))}"
    w = re.search(r'\bwidth="([\d.]+)"', svg)
    h = re.search(r'\bheight="([\d.]+)"', svg)
    return f"{_dim(float(w.group(1)))}×{_dim(float(h.group(1)))}" if w and h else ""


def _png_size(data: bytes) -> str:
    """Read width/height out of the PNG IHDR chunk."""
    if len(data) >= 24 and data[:8] == b"\x89PNG\r\n\x1a\n":
        w, h = struct.unpack(">II", data[16:24])
        return f"{w}×{h}"
    return ""


def _asset_meta(stem: str):
    """Derive a display label, stage background and note from a filename."""
    parts = [p for p in re.split(r"[-_]+", stem.lower()) if p]
    kind = next((k for k in ("lockup", "glyph", "wordmark", "symbol") if k in parts), "")
    kind = kind.capitalize() if kind else _title(stem)
    bg = "dark" if "dark" in parts else "light"
    traits = [t for t in ("padded", "transparent") if t in parts]

    label = f"{kind} · {bg} backgrounds"
    if traits:
        label += " · " + ", ".join(traits)

    note = f"{kind} artwork tuned for {bg} surfaces."
    if "padded" in traits:
        note += " Ships with clear space baked in."
    if "transparent" in traits:
        note += " Transparent background."
    return label, bg, note


def _asset_order(entry: dict):
    parts = re.split(r"[-_]+", entry["name"].lower())
    return (
        0 if "lockup" in parts else 1,
        0 if "dark" in parts else 1,
        1 if "padded" in parts else 0,
        1 if "transparent" in parts else 0,
        entry["name"],
    )


def load_logo_assets(folder_name: str) -> list:
    """Embed every .svg/.png in assets/logos/<folder_name>/ as a download entry.

    Files sharing a stem (foo.svg + foo.png) collapse into one entry offering
    both formats, so each card hands over the original bytes rather than a
    re-rendered approximation.
    """
    folder = LOGOS_DIR / folder_name
    if not folder.is_dir():
        return []

    grouped: dict = {}
    for path in sorted(folder.iterdir(), key=_natkey):
        suffix = path.suffix.lower()
        if suffix not in (".svg", ".png"):
            continue
        entry = grouped.setdefault(path.stem, {"name": path.stem})
        if suffix == ".svg":
            svg = _clean_svg(path.read_text(encoding="utf-8"))
            if not svg:
                continue
            entry["svg"] = svg
            entry["svgSize"] = _svg_size(svg)
            entry["svgBytes"] = path.stat().st_size
        else:
            data = path.read_bytes()
            entry["png"] = "data:image/png;base64," + base64.b64encode(data).decode("ascii")
            entry["pngSize"] = _png_size(data)
            entry["pngBytes"] = len(data)

    assets = []
    for stem, entry in grouped.items():
        if "svg" not in entry and "png" not in entry:
            continue
        entry["label"], entry["bg"], entry["note"] = _asset_meta(stem)
        assets.append(entry)
    assets.sort(key=_asset_order)
    return assets


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

    # Embed logo asset packs for any brand/variant that names an assetDir.
    asset_total = 0
    for brand in brands:
        targets = [brand] + list((brand.get("variants") or {}).values())
        for target in targets:
            folder = target.get("assetDir")
            if not folder:
                continue
            target["assetFiles"] = load_logo_assets(folder)
            asset_total += len(target["assetFiles"])

    # Compact JSON; escape "</" so inline <script> can never be closed early.
    payload = json.dumps(brands, ensure_ascii=False, separators=(",", ":"))
    payload = payload.replace("</", "<\\/")

    out = template.replace("__BRANDS_JSON__", payload)
    (ROOT / "index.html").write_text(out, encoding="utf-8")
    print(
        f"index.html written ({len(out):,} bytes, {len(brands)} brands, "
        f"{icon_total} icons, {asset_total} logo files)"
    )


if __name__ == "__main__":
    main()
