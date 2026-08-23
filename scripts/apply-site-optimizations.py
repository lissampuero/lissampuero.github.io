#!/usr/bin/env python3
"""Apply site-wide optimization patches without changing visual design."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
V = "20260823"

PUBLIC_PAGES = [
    "index.html",
    "es/index.html",
    "nl/index.html",
    "about/index.html",
    "es/about/index.html",
    "nl/about/index.html",
    "services/index.html",
    "es/services/index.html",
    "nl/services/index.html",
    "contact/index.html",
    "es/contact/index.html",
    "nl/contact/index.html",
    "portfolio/editorial/index.html",
    "es/portfolio/editorial/index.html",
    "nl/portfolio/editorial/index.html",
    "portfolio/narrative/index.html",
    "es/portfolio/narrative/index.html",
    "nl/portfolio/narrative/index.html",
    "portfolio/stationery/index.html",
    "es/portfolio/stationery/index.html",
    "nl/portfolio/stationery/index.html",
]

TAILWIND_BLOCK = re.compile(
    r'\n  <script src="https://cdn\.tailwindcss\.com"></script>\n  <script>\n    tailwind\.config = \{.*?\n    \};\n  </script>',
    re.DOTALL,
)

LINK_REPLACEMENTS = [
    (re.compile(r'href="index\.html"'), 'href="./"'),
    (re.compile(r'href="\.\./index\.html"'), 'href="../"'),
    (re.compile(r'href="\.\./\.\./index\.html"'), 'href="../../"'),
    (re.compile(r'href="\.\./\.\./\.\./index\.html"'), 'href="../../../"'),
    (re.compile(r'href="about/index\.html"'), 'href="about/"'),
    (re.compile(r'href="\.\./about/index\.html"'), 'href="../about/"'),
    (re.compile(r'href="\.\./\.\./about/index\.html"'), 'href="../../about/"'),
    (re.compile(r'href="\.\./\.\./\.\./about/index\.html"'), 'href="../../../about/"'),
    (re.compile(r'href="services/index\.html"'), 'href="services/"'),
    (re.compile(r'href="\.\./services/index\.html"'), 'href="../services/"'),
    (re.compile(r'href="\.\./\.\./services/index\.html"'), 'href="../../services/"'),
    (re.compile(r'href="\.\./\.\./\.\./services/index\.html"'), 'href="../../../services/"'),
    (re.compile(r'href="contact/index\.html"'), 'href="contact/"'),
    (re.compile(r'href="\.\./contact/index\.html"'), 'href="../contact/"'),
    (re.compile(r'href="\.\./\.\./contact/index\.html"'), 'href="../../contact/"'),
    (re.compile(r'href="\.\./\.\./\.\./contact/index\.html"'), 'href="../../../contact/"'),
    (re.compile(r'href="portfolio/editorial/index\.html"'), 'href="portfolio/editorial/"'),
    (re.compile(r'href="\.\./portfolio/editorial/index\.html"'), 'href="../portfolio/editorial/"'),
    (re.compile(r'href="\.\./\.\./portfolio/editorial/index\.html"'), 'href="../../portfolio/editorial/"'),
    (re.compile(r'href="\.\./\.\./\.\./portfolio/editorial/index\.html"'), 'href="../../../portfolio/editorial/"'),
    (re.compile(r'href="portfolio/narrative/index\.html"'), 'href="portfolio/narrative/"'),
    (re.compile(r'href="\.\./portfolio/narrative/index\.html"'), 'href="../portfolio/narrative/"'),
    (re.compile(r'href="\.\./\.\./portfolio/narrative/index\.html"'), 'href="../../portfolio/narrative/"'),
    (re.compile(r'href="\.\./\.\./\.\./portfolio/narrative/index\.html"'), 'href="../../../portfolio/narrative/"'),
    (re.compile(r'href="portfolio/stationery/index\.html"'), 'href="portfolio/stationery/"'),
    (re.compile(r'href="\.\./portfolio/stationery/index\.html"'), 'href="../portfolio/stationery/"'),
    (re.compile(r'href="\.\./\.\./portfolio/stationery/index\.html"'), 'href="../../portfolio/stationery/"'),
    (re.compile(r'href="\.\./\.\./\.\./portfolio/stationery/index\.html"'), 'href="../../../portfolio/stationery/"'),
    (re.compile(r'href="\.\./es/index\.html"'), 'href="../es/"'),
    (re.compile(r'href="\.\./nl/index\.html"'), 'href="../nl/"'),
    (re.compile(r'href="\.\./\.\./es/index\.html"'), 'href="../../es/"'),
    (re.compile(r'href="\.\./\.\./nl/index\.html"'), 'href="../../nl/"'),
    (re.compile(r'href="\.\./\.\./\.\./es/index\.html"'), 'href="../../../es/"'),
    (re.compile(r'href="\.\./\.\./\.\./nl/index\.html"'), 'href="../../../nl/"'),
    (re.compile(r'href="\.\./es/contact/index\.html"'), 'href="../es/contact/"'),
    (re.compile(r'href="\.\./nl/contact/index\.html"'), 'href="../nl/contact/"'),
    (re.compile(r'href="\.\./\.\./es/contact/index\.html"'), 'href="../../es/contact/"'),
    (re.compile(r'href="\.\./\.\./nl/contact/index\.html"'), 'href="../../nl/contact/"'),
    (re.compile(r'href="\.\./\.\./\.\./es/contact/index\.html"'), 'href="../../../es/contact/"'),
    (re.compile(r'href="\.\./\.\./\.\./nl/contact/index\.html"'), 'href="../../../nl/contact/"'),
]


def shared_prefix(path: Path) -> str:
    depth = len(path.relative_to(ROOT).parts) - 1
    return "../" * depth + "shared/"


def patch_html(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    orig = text
    sp = shared_prefix(path)

    text = TAILWIND_BLOCK.sub(
        f'\n  <link rel="stylesheet" href="{sp}utilities.css?v={V}">',
        text,
    )

    if "utilities.css" not in text and "site-chrome.css" in text:
        text = text.replace(
            f'href="{sp}site-chrome.css"',
            f'href="{sp}utilities.css?v={V}">\n  <link rel="stylesheet" href="{sp}site-chrome.css?v={V}"',
            1,
        )
    else:
        text = re.sub(
            rf'href="{re.escape(sp)}site-chrome\.css(?:\?v=[^"]*)?"',
            f'href="{sp}site-chrome.css?v={V}"',
            text,
        )

    text = re.sub(
        rf'href="{re.escape(sp)}artbook\.css(?:\?v=[^"]*)?"',
        f'href="{sp}artbook.css?v={V}"',
        text,
    )

    text = re.sub(r'\n  <meta name="keywords" content="[^"]*">\n', "\n", text)
    text = re.sub(r'\n<meta name="keywords" content="[^"]*">\n', "\n", text)

    if "site-skip-link" not in text:
        if re.search(r"<body[^>]*>", text):
            skip = {
                "en": "Skip to content",
                "es": "Saltar al contenido",
                "nl": "Ga naar inhoud",
            }
            lang = re.search(r'<html lang="([^"]+)"', text)
            label = skip.get(lang.group(1) if lang else "en", skip["en"])
            text = re.sub(
                r"(<body[^>]*>)",
                rf'\1\n  <a class="site-skip-link" href="#main">{label}</a>',
                text,
                count=1,
            )

    text = re.sub(r"<main(?![^>]*\bid=)", '<main id="main"', text, count=1)

    # Keep explicit index.html paths — required for local file:// preview.
    # Do NOT rewrite to clean directory URLs (contact/, ./, etc.).

    analytics = f'<script src="{sp}site-analytics.js?v={V}" defer></script>'
    nav_js = f'<script src="{sp}site-nav.js?v={V}" defer></script>'
    if "site-analytics.js" not in text and "</body>" in text:
        text = text.replace("</body>", f"{analytics}\n{nav_js}\n</body>" if "site-nav.js" not in text else f"{analytics}\n</body>")

    # Ensure site-nav has version if already present
    text = re.sub(
        rf'src="{re.escape(sp)}site-nav\.js(?:\?v=[^"]*)?"',
        f'src="{sp}site-nav.js?v={V}"',
        text,
    )
    text = re.sub(
        rf'src="{re.escape(sp)}js/lightbox\.js(?:\?v=[^"]*)?"',
        f'src="{sp}js/lightbox.js?v={V}"',
        text,
    )

    return text if text != orig else orig


def patch_editorial_spreads(text: str) -> str:
    for n in range(1, 17):
        nn = f"{n:02d}"
        old = (
            f'<img src="art/spreads/page-{nn}.webp" alt="'
        )
        if old not in text or f"page-{nn}-750.webp" in text:
            continue
        text = text.replace(
            f'src="art/spreads/page-{nn}.webp"',
            f'src="art/spreads/page-{nn}-750.webp"\n'
            f'                srcset="art/spreads/page-{nn}-750.webp 750w, art/spreads/page-{nn}@2x.webp 1100w"\n'
            f'                sizes="(min-width: 64rem) 45vw, 92vw"',
            1,
        )
    for letter in "abcd":
        single = f'src="art/magazine/fashion-{letter}.webp"'
        if single in text and f"fashion-{letter}-1024.webp" not in text:
            text = text.replace(
                single,
                f'src="art/magazine/fashion-{letter}-1024.webp"\n'
                f'                    srcset="art/magazine/fashion-{letter}-1024.webp 1024w, art/magazine/fashion-{letter}@2x.webp 2048w"\n'
                f'                    sizes="(min-width: 64rem) 28vw, 88vw"',
                1,
            )
    text = text.replace(
        'src="art/placeholder-book-cover.svg" alt="" class="ed-lightbox__image"',
        'src="art/spreads/page-01@2x.webp" alt="" class="ed-lightbox__image"',
    )
    text = text.replace(
        'content="https://lissampuero.com/portfolio/editorial/art/illustration-editorial-feature@2x.jpg"',
        'content="https://lissampuero.com/portfolio/editorial/art/illustration-editorial-feature@2x.webp"',
    )
    return text


def main() -> None:
    for rel in PUBLIC_PAGES:
        path = ROOT / rel
        if not path.exists():
            print("skip missing", rel)
            continue
        text = patch_html(path)
        if "portfolio/editorial" in rel:
            text = patch_editorial_spreads(text)
        path.write_text(text, encoding="utf-8")
        print("patched", rel)

    # ES/NL editorial use relative paths to EN art folder
    for rel in ["es/portfolio/editorial/index.html", "nl/portfolio/editorial/index.html"]:
        path = ROOT / rel
        text = path.read_text(encoding="utf-8")
        for n in range(1, 17):
            nn = f"{n:02d}"
            prefix = "../../../portfolio/editorial/"
            if f"page-{nn}-750.webp" in text:
                continue
            text = text.replace(
                f'src="{prefix}art/spreads/page-{nn}.webp"',
                f'src="{prefix}art/spreads/page-{nn}-750.webp"\n'
                f'                srcset="{prefix}art/spreads/page-{nn}-750.webp 750w, {prefix}art/spreads/page-{nn}@2x.webp 1100w"\n'
                f'                sizes="(min-width: 64rem) 45vw, 92vw"',
                1,
            )
        for letter in "abcd":
            prefix = "../../../portfolio/editorial/"
            single = f'src="{prefix}art/magazine/fashion-{letter}.webp"'
            if single in text:
                text = text.replace(
                    single,
                    f'src="{prefix}art/magazine/fashion-{letter}-1024.webp"\n'
                    f'                    srcset="{prefix}art/magazine/fashion-{letter}-1024.webp 1024w, {prefix}art/magazine/fashion-{letter}@2x.webp 2048w"\n'
                    f'                    sizes="(min-width: 64rem) 28vw, 88vw"',
                    1,
                )
        text = text.replace(
            'src="../../../portfolio/editorial/art/placeholder-book-cover.svg" alt="" class="ed-lightbox__image"',
            'src="../../../portfolio/editorial/art/spreads/page-01@2x.webp" alt="" class="ed-lightbox__image"',
        )
        text = text.replace(
            'content="https://lissampuero.com/portfolio/editorial/art/illustration-editorial-feature@2x.jpg"',
            'content="https://lissampuero.com/portfolio/editorial/art/illustration-editorial-feature@2x.webp"',
        )
        path.write_text(text, encoding="utf-8")
        print("patched editorial i18n", rel)


if __name__ == "__main__":
    main()
