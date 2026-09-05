#!/usr/bin/env python3
"""Normalize favicon links for Google Search and browser compatibility."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

FAVICON_BLOCK = """  <link rel="icon" href="/favicon.ico" sizes="any">
  <link rel="icon" type="image/png" sizes="48x48" href="/favicon-48x48.png">
  <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
  <link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png">
  <link rel="icon" type="image/svg+xml" href="/favicon.svg">
  <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
  <link rel="manifest" href="/site.webmanifest">"""

PATTERN = re.compile(
    r"  <link rel=\"icon\"[^>]+>\n"
    r"(?:  <link rel=\"icon\"[^>]+>\n)*"
    r"  <link rel=\"apple-touch-icon\"[^>]+>\n"
    r"(?:  <link rel=\"icon\" href=\"/favicon\.ico\">?\n)?"
    r"(?:  <link rel=\"manifest\" href=\"/site\.webmanifest\">?\n)?",
    re.MULTILINE,
)


def main() -> None:
    for path in ROOT.rglob("*.html"):
        if "node_modules" in path.parts:
            continue
        text = path.read_text(encoding="utf-8")
        if 'href="/favicon' not in text and "href=\"/favicon" not in text:
            continue
        if "favicon.ico" not in text:
            continue
        new_text, n = PATTERN.subn(FAVICON_BLOCK + "\n", text, count=1)
        if n:
            path.write_text(new_text, encoding="utf-8")
            print(f"updated {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
