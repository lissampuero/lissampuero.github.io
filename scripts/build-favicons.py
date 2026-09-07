#!/usr/bin/env python3
"""Install favicon assets from the curated favicon package."""

from __future__ import annotations

import shutil
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
PACKAGE = Path.home() / "Downloads" / "favicon-package 3"
BRAND = ROOT / "assets" / "brand"
MASTER = ROOT / "assets" / "brand" / "liss-stamp-512.png"


def copy_package_file(name: str, dest: Path) -> None:
    src = PACKAGE / name
    if not src.exists():
        raise FileNotFoundError(f"Missing package file: {src}")
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dest)
    print(f"copied {name} -> {dest.relative_to(ROOT)}")


def resize_copy(src: Path, dest: Path, size: int) -> None:
    image = Image.open(src).convert("RGBA")
    image.resize((size, size), Image.Resampling.LANCZOS).save(dest, format="PNG", optimize=True)
    print(f"wrote {dest.relative_to(ROOT)} ({size}x{size})")


def main() -> None:
    if not PACKAGE.exists() and not MASTER.exists():
        raise SystemExit("Favicon package or master PNG not found.")

    source = PACKAGE if PACKAGE.exists() else None

    if source:
        for name in (
            "favicon.ico",
            "favicon-16x16.png",
            "favicon-32x32.png",
            "favicon-48x48.png",
            "favicon-96x96.png",
            "apple-touch-icon.png",
            "android-chrome-192x192.png",
            "android-chrome-512x512.png",
            "mstile-150x150.png",
        ):
            copy_package_file(name, ROOT / name)

        touch = source / "apple-touch-icon.png"
        for name in (
            "apple-touch-icon-precomposed.png",
            "apple-touch-icon-180x180.png",
            "liss-apple-touch.png",
        ):
            shutil.copy2(touch, ROOT / name)
            print(f"copied apple-touch-icon.png -> {name}")

        for src_name, dest_name in (
            ("favicon-16x16.png", "tab-icon-16.png"),
            ("favicon-32x32.png", "tab-icon-32.png"),
            ("favicon-48x48.png", "tab-icon-48.png"),
            ("apple-touch-icon.png", "tab-icon-180.png"),
            ("android-chrome-192x192.png", "tab-icon-192.png"),
            ("android-chrome-512x512.png", "tab-icon-512.png"),
            ("favicon.ico", "tab-icon.ico"),
        ):
            shutil.copy2(ROOT / src_name, BRAND / dest_name)
            print(f"copied {src_name} -> assets/brand/{dest_name}")
    else:
        master = Image.open(MASTER).convert("RGBA")
        BRAND.mkdir(parents=True, exist_ok=True)

        def save(size: int, *paths: Path) -> None:
            image = master.resize((size, size), Image.Resampling.LANCZOS)
            for path in paths:
                path.parent.mkdir(parents=True, exist_ok=True)
                image.save(path, format="PNG", optimize=True)

        save(16, ROOT / "favicon-16x16.png", BRAND / "tab-icon-16.png")
        save(32, ROOT / "favicon-32x32.png", BRAND / "tab-icon-32.png")
        save(48, ROOT / "favicon-48x48.png", BRAND / "tab-icon-48.png")
        save(180, ROOT / "apple-touch-icon.png", ROOT / "apple-touch-icon-precomposed.png",
             ROOT / "apple-touch-icon-180x180.png", ROOT / "liss-apple-touch.png",
             BRAND / "tab-icon-180.png")
        save(192, BRAND / "tab-icon-192.png")
        save(512, BRAND / "tab-icon-512.png")

        frames = [master.resize((size, size), Image.Resampling.LANCZOS) for size in (16, 32, 48)]
        frames[0].save(
            ROOT / "favicon.ico",
            format="ICO",
            sizes=[(frame.width, frame.height) for frame in frames],
            append_images=frames[1:],
        )
        shutil.copy2(ROOT / "favicon.ico", BRAND / "tab-icon.ico")

    touch = ROOT / "apple-touch-icon.png"
    resize_copy(touch, ROOT / "apple-touch-icon-152x152.png", 152)
    resize_copy(touch, ROOT / "apple-touch-icon-120x120.png", 120)


if __name__ == "__main__":
    main()
