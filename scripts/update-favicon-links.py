#!/usr/bin/env python3
"""Normalize favicon links for local preview and production."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FAVICON_VERSION = "20260906b"


def favicon_block() -> str:
    v = FAVICON_VERSION
    return f"""  <link rel="icon" type="image/png" sizes="32x32" href="/assets/brand/liss-stamp-32.png?v={v}">
  <link rel="icon" type="image/png" sizes="16x16" href="/assets/brand/liss-stamp-16.png?v={v}">
  <link rel="icon" href="/favicon.ico?v={v}" sizes="any">
  <link rel="icon" type="image/png" sizes="48x48" href="/assets/brand/liss-stamp-48.png?v={v}">
  <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png?v={v}">
  <link rel="manifest" href="/site.webmanifest?v={v}">
  <meta name="msapplication-TileColor" content="#d6338f">
  <meta name="msapplication-config" content="/browserconfig.xml?v={v}">
  <meta name="theme-color" content="#d6338f">"""


PATTERN = re.compile(
    r"  <link rel=\"icon\"[^>]+>\n"
    r"(?:  <link rel=\"icon\"[^>]+>\n)*"
    r"  <link rel=\"apple-touch-icon\"[^>]+>\n"
    r"(?:  <link rel=\"manifest\" href=\"[^\"]+\">?\n)?"
    r"(?:  <meta name=\"msapplication-TileColor\"[^>]+>\n)?"
    r"(?:  <meta name=\"msapplication-config\"[^>]+>\n)?"
    r"(?:  <meta name=\"theme-color\"[^>]+>\n)?",
    re.MULTILINE,
)


def main() -> None:
    for path in ROOT.rglob("*.html"):
        if "node_modules" in path.parts:
            continue
        text = path.read_text(encoding="utf-8")
        if "favicon" not in text and "liss-" not in text:
            continue
        block = favicon_block()
        new_text, n = PATTERN.subn(block + "\n", text, count=1)
        if n:
            path.write_text(new_text, encoding="utf-8")
            print(f"updated {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
