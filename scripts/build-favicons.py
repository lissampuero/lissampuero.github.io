#!/usr/bin/env python3
"""Build favicon assets from the 512px glitter stamp master."""

from __future__ import annotations

import io
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
MASTER = ROOT / "assets" / "brand" / "liss-stamp-512.png"
BRAND = ROOT / "assets" / "brand"

SIZES = {
    "tab-icon-16.png": 16,
    "tab-icon-32.png": 32,
    "tab-icon-48.png": 48,
    "tab-icon-180.png": 180,
    "tab-icon-192.png": 192,
    "tab-icon-512.png": 512,
}

ROOT_COPIES = {
    "favicon-16x16.png": 16,
    "favicon-32x32.png": 32,
    "favicon-48x48.png": 48,
    "apple-touch-icon.png": 180,
    "apple-touch-icon-precomposed.png": 180,
    "liss-apple-touch.png": 180,
}


def resize(master: Image.Image, size: int) -> Image.Image:
    return master.resize((size, size), Image.Resampling.LANCZOS)


def build_ico(master: Image.Image, path: Path) -> None:
    frames = [resize(master, size) for size in (16, 32, 48)]
    frames[0].save(
        path,
        format="ICO",
        sizes=[(frame.width, frame.height) for frame in frames],
        append_images=frames[1:],
    )


def main() -> None:
    master = Image.open(MASTER).convert("RGBA")
    BRAND.mkdir(parents=True, exist_ok=True)

    for name, size in SIZES.items():
        out = BRAND / name
        resize(master, size).save(out, format="PNG", optimize=True)
        print(f"wrote {out.relative_to(ROOT)}")

    build_ico(master, BRAND / "tab-icon.ico")
    print(f"wrote {BRAND.relative_to(ROOT) / 'tab-icon.ico'}")

    build_ico(master, ROOT / "favicon.ico")
    print(f"wrote favicon.ico")

    for name, size in ROOT_COPIES.items():
        out = ROOT / name
        resize(master, size).save(out, format="PNG", optimize=True)
        print(f"wrote {name}")


if __name__ == "__main__":
    main()
