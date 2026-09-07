#!/usr/bin/env python3
"""Normalize favicon links for local preview and production."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def favicon_block() -> str:
    return """  <link rel="icon" type="image/png" sizes="32x32" href="/favicon-2026-32.png">
  <link rel="shortcut icon" type="image/png" href="/favicon-2026-32.png">
  <link rel="icon" href="/favicon-2026.ico" sizes="any">
  <link rel="icon" type="image/png" sizes="16x16" href="/favicon-2026-16.png">
  <link rel="icon" type="image/png" sizes="48x48" href="/favicon-2026-48.png">
  <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon-2026.png">
  <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
  <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon-180x180.png">
  <link rel="apple-touch-icon" sizes="152x152" href="/apple-touch-icon-152x152.png">
  <link rel="apple-touch-icon" sizes="120x120" href="/apple-touch-icon-120x120.png">
  <link rel="manifest" href="/site.webmanifest">
  <meta name="msapplication-TileColor" content="#d6338f">
  <meta name="msapplication-config" content="/browserconfig.xml">
  <meta name="theme-color" content="#d6338f">
  <script>
  (function(){var i="/favicon-2026-32.png",l=document.querySelector('link[rel~="icon"]');if(!l||l.href.indexOf("favicon-2026-32")===-1){l=document.createElement("link");l.rel="icon";l.type="image/png";l.href=i;document.head.appendChild(l);}else{l.href=i;}})();
  </script>"""


PATTERN = re.compile(
    r"  <link rel=\"icon\"[^>]+>\n"
    r"(?:  <link rel=\"(?:shortcut )?icon\"[^>]+>\n)*"
    r"(?:  <link rel=\"apple-touch-icon\"[^>]+>\n)*"
    r"(?:  <link rel=\"manifest\" href=\"[^\"]+\">?\n)?"
    r"(?:  <meta name=\"msapplication-TileColor\"[^>]+>\n)?"
    r"(?:  <meta name=\"msapplication-config\"[^>]+>\n)?"
    r"(?:  <meta name=\"theme-color\"[^>]+>\n)?"
    r"(?:  <script>\n"
    r"  \(function\(\)\{var i=\"/favicon-2026-32\.png\"[^\n]+\n"
    r"  </script>\n)?",
    re.MULTILINE,
)


def main() -> None:
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
