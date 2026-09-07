#!/usr/bin/env python3
"""Normalize favicon links for local preview and production."""

from __future__ import annotations

import base64
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ICON_32 = ROOT / "favicon-32x32.png"


def inline_icon_href() -> str:
    payload = base64.b64encode(ICON_32.read_bytes()).decode("ascii")
    return f"data:image/png;base64,{payload}"


def favicon_block() -> str:
    inline_href = inline_icon_href()
    return f"""  <link rel="icon" type="image/png" href="{inline_href}">
  <link rel="icon" href="/favicon.ico" sizes="any">
  <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
  <link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png">
  <link rel="icon" type="image/png" sizes="48x48" href="/favicon-48x48.png">
  <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
  <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon-180x180.png">
  <link rel="manifest" href="/site.webmanifest">
  <meta name="msapplication-TileColor" content="#d6338f">
  <meta name="msapplication-config" content="/browserconfig.xml">
  <meta name="theme-color" content="#d6338f">"""


PATTERN = re.compile(
    r"  <link rel=\"icon\"[^>]+>\n"
    r"(?:  <link rel=\"icon\"[^>]+>\n)*"
    r"(?:  <link rel=\"apple-touch-icon\"[^>]+>\n)?"
    r"(?:  <link rel=\"apple-touch-icon\"[^>]+>\n)?"
    r"(?:  <link rel=\"manifest\" href=\"[^\"]+\">?\n)?"
    r"(?:  <meta name=\"msapplication-TileColor\"[^>]+>\n)?"
    r"(?:  <meta name=\"msapplication-config\"[^>]+>\n)?"
    r"(?:  <meta name=\"theme-color\"[^>]+>\n)?",
    re.MULTILINE,
)


def main() -> None:
    if not ICON_32.exists():
        raise SystemExit("Run scripts/build-favicons.py first.")

    block = favicon_block()
    for path in ROOT.rglob("*.html"):
        if "node_modules" in path.parts:
            continue
        text = path.read_text(encoding="utf-8")
        if "favicon" not in text and "apple-touch-icon" not in text:
            continue
        new_text, n = PATTERN.subn(block + "\n", text, count=1)
        if n:
            path.write_text(new_text, encoding="utf-8")
            print(f"updated {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
