#!/usr/bin/env python3
"""Normalize favicon links for local preview and production."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def favicon_prefix(html_path: Path) -> str:
    depth = len(html_path.relative_to(ROOT).parts) - 1
    return "../" * depth


def favicon_block(prefix: str) -> str:
    p = prefix
    return f"""  <link rel="icon" href="{p}liss-icon.svg" type="image/svg+xml">
  <link rel="icon" type="image/png" sizes="48x48" href="{p}liss-icon-48.png">
  <link rel="icon" href="{p}liss-icon.ico" sizes="any">
  <link rel="icon" type="image/png" sizes="32x32" href="{p}liss-icon-32.png">
  <link rel="icon" type="image/png" sizes="16x16" href="{p}liss-icon-16.png">
  <link rel="icon" type="image/png" sizes="96x96" href="{p}liss-icon-96.png">
  <link rel="apple-touch-icon" sizes="180x180" href="{p}liss-apple-touch.png">
  <link rel="manifest" href="{p}site.webmanifest">
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
        if "favicon" not in text and "liss-icon" not in text:
            continue
        block = favicon_block(favicon_prefix(path))
        new_text, n = PATTERN.subn(block + "\n", text, count=1)
        if n:
            path.write_text(new_text, encoding="utf-8")
            print(f"updated {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
