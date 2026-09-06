#!/usr/bin/env python3
"""Normalize favicon links for local preview and production."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FAVICON_VERSION = "20260906h"


def favicon_prefix(html_path: Path) -> str:
    depth = len(html_path.relative_to(ROOT).parts) - 1
    return "../" * depth


def favicon_block(prefix: str) -> str:
    p = prefix
    return f"""  <link rel="icon" href="{p}favicon.svg?v={FAVICON_VERSION}" type="image/svg+xml">
  <link rel="icon" type="image/png" sizes="48x48" href="{p}favicon-48x48.png?v={FAVICON_VERSION}">
  <link rel="icon" href="{p}favicon.ico?v={FAVICON_VERSION}" sizes="any">
  <link rel="icon" type="image/png" sizes="32x32" href="{p}favicon-32x32.png?v={FAVICON_VERSION}">
  <link rel="icon" type="image/png" sizes="16x16" href="{p}favicon-16x16.png?v={FAVICON_VERSION}">
  <link rel="icon" type="image/png" sizes="96x96" href="{p}favicon-96x96.png?v={FAVICON_VERSION}">
  <link rel="apple-touch-icon" sizes="180x180" href="{p}apple-touch-icon.png?v={FAVICON_VERSION}">
  <link rel="manifest" href="{p}site.webmanifest?v={FAVICON_VERSION}">
  <meta name="msapplication-TileColor" content="#d6338f">
  <meta name="msapplication-config" content="{p}browserconfig.xml">
  <meta name="theme-color" content="#d6338f">"""


PATTERN = re.compile(
    r"  <link rel=\"icon\"[^>]+>\n"
    r"(?:  <link rel=\"icon\"[^>]+>\n)*"
    r"  <link rel=\"apple-touch-icon\"[^>]+>\n"
    r"(?:  <link rel=\"icon\" href=\"[^\"]+\">?\n)?"
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
        if "favicon.ico" not in text and "favicon.svg" not in text:
            continue
        block = favicon_block(favicon_prefix(path))
        new_text, n = PATTERN.subn(block + "\n", text, count=1)
        if n:
            path.write_text(new_text, encoding="utf-8")
            print(f"updated {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
