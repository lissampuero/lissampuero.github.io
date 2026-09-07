#!/usr/bin/env python3
"""Install favicon assets from the curated favicon package."""

from __future__ import annotations

import shutil
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
PACKAGE = Path.home() / "Downloads" / "favicon-package 3"
BRAND = ROOT / "assets" / "brand"


def copy_file(src: Path, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dest)
    print(f"copied -> {dest.relative_to(ROOT)}")


def resize_copy(src: Path, dest: Path, size: int) -> None:
    image = Image.open(src).convert("RGBA")
    image.resize((size, size), Image.Resampling.LANCZOS).save(dest, format="PNG", optimize=True)
    print(f"wrote {dest.relative_to(ROOT)} ({size}x{size})")


def main() -> None:
    if not PACKAGE.exists():
        raise SystemExit(f"Missing favicon package: {PACKAGE}")

    package_files = (
        "favicon.ico",
        "favicon-16x16.png",
        "favicon-32x32.png",
        "favicon-48x48.png",
        "favicon-96x96.png",
        "apple-touch-icon.png",
        "android-chrome-192x192.png",
        "android-chrome-512x512.png",
        "mstile-150x150.png",
    )
    for name in package_files:
        copy_file(PACKAGE / name, ROOT / name)

    touch = ROOT / "apple-touch-icon.png"
    for name in (
        "apple-touch-icon-precomposed.png",
        "apple-touch-icon-180x180.png",
        "liss-apple-touch.png",
        "favicon-180x180.png",
    ):
        copy_file(touch, ROOT / name)

    brand_copies = (
        ("favicon-16x16.png", "tab-icon-16.png"),
        ("favicon-32x32.png", "tab-icon-32.png"),
        ("favicon-48x48.png", "tab-icon-48.png"),
        ("apple-touch-icon.png", "tab-icon-180.png"),
        ("android-chrome-192x192.png", "tab-icon-192.png"),
        ("android-chrome-512x512.png", "tab-icon-512.png"),
        ("favicon.ico", "tab-icon.ico"),
    )
    for src_name, dest_name in brand_copies:
        copy_file(ROOT / src_name, BRAND / dest_name)

    # Fresh filenames Safari has never cached for this domain.
    copy_file(ROOT / "favicon-32x32.png", ROOT / "favicon-2026-32.png")
    copy_file(ROOT / "favicon-16x16.png", ROOT / "favicon-2026-16.png")
    copy_file(ROOT / "favicon-48x48.png", ROOT / "favicon-2026-48.png")
    copy_file(ROOT / "favicon.ico", ROOT / "favicon-2026.ico")
    copy_file(touch, ROOT / "apple-touch-icon-2026.png")

    copy_file(ROOT / "android-chrome-192x192.png", ROOT / "favicon-192x192.png")
    copy_file(ROOT / "android-chrome-512x512.png", ROOT / "favicon-512x512.png")

    resize_copy(touch, ROOT / "apple-touch-icon-152x152.png", 152)
    resize_copy(touch, ROOT / "apple-touch-icon-120x120.png", 120)
    resize_copy(touch, ROOT / "touch-icon-ipad.png", 152)
    resize_copy(touch, ROOT / "touch-icon-iphone.png", 120)


if __name__ == "__main__":
    main()
