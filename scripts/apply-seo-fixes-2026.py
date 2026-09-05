#!/usr/bin/env python3
"""Apply technical SEO fixes across indexable pages (head/meta/schema only)."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITEMAP_LINK = (
    '<link rel="sitemap" type="application/xml" title="Sitemap" '
    'href="https://lissampuero.com/sitemap.xml">'
)
VERIFY_BLOCK = """  <meta name="google-site-verification" content="HoA3JzgoWFfzQ6P51l2lKd_LVTM4MmmfI_slk0oHNiw">
  <meta name="msvalidate.01" content="E8AADEEBCD1E6F51026CE250E8E03B71">
"""

INDEXABLE = [
    "index.html",
    "nl/index.html",
    "es/index.html",
    "about/index.html",
    "nl/about/index.html",
    "es/about/index.html",
    "services/index.html",
    "nl/services/index.html",
    "es/services/index.html",
    "portfolio/editorial/index.html",
    "nl/portfolio/editorial/index.html",
    "es/portfolio/editorial/index.html",
    "portfolio/narrative/index.html",
    "nl/portfolio/narrative/index.html",
    "es/portfolio/narrative/index.html",
    "portfolio/stationery/index.html",
    "nl/portfolio/stationery/index.html",
    "es/portfolio/stationery/index.html",
    "contact/index.html",
    "nl/contact/index.html",
    "es/contact/index.html",
]

NL_OFFER_CATALOG = """
  "hasOfferCatalog": {
    "@type": "OfferCatalog",
    "name": "Studiodiensten",
    "itemListElement": [
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Redactioneel" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Verhalend" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Commercieel" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Samenwerkingen & klassieke kunst" } }
    ]
  },
"""

ES_OFFER_CATALOG = """
  "hasOfferCatalog": {
    "@type": "OfferCatalog",
    "name": "Servicios del estudio",
    "itemListElement": [
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Editorial" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Narrativo" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Comercial" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Colaboraciones y arte clásico" } }
    ]
  },
"""


def add_sitemap_link(html: str) -> str:
    if 'rel="sitemap"' in html:
        return html
    return re.sub(
        r'(<link rel="canonical" href="[^"]+">)',
        r"\1\n" + SITEMAP_LINK,
        html,
        count=1,
    )


def add_verification(html: str) -> str:
    if "google-site-verification" in html:
        return html
    return re.sub(
        r'(<meta name="viewport" content="width=device-width, initial-scale=1\.0">)',
        r"\1\n" + VERIFY_BLOCK.rstrip("\n"),
        html,
        count=1,
    )


def add_twitter_image_alt(html: str) -> str:
    if "twitter:image:alt" in html:
        return html
    m = re.search(
        r'<meta property="og:image:alt" content="([^"]+)">',
        html,
    )
    if not m:
        return html
    alt = m.group(1)
    return re.sub(
        r'(<meta name="twitter:image" content="[^"]+">)',
        rf'\1\n  <meta name="twitter:image:alt" content="{alt}">',
        html,
        count=1,
    )


def add_twitter_url(html: str) -> str:
    if "twitter:url" in html:
        return html
    m = re.search(r'<meta property="og:url" content="([^"]+)">', html)
    if not m:
        return html
    url = m.group(1)
    insert_after = re.search(r'<meta name="twitter:card" content="[^"]+">', html)
    if not insert_after:
        return html
    pos = insert_after.end()
    return (
        html[:pos]
        + f'\n  <meta name="twitter:url" content="{url}">'
        + html[pos:]
    )


def add_offer_catalog_nl(html: str) -> str:
    if "hasOfferCatalog" in html:
        return html
    return html.replace(
        '  "serviceType": ["Prentenboekillustratie"',
        NL_OFFER_CATALOG.strip() + '\n  "serviceType": ["Prentenboekillustratie"',
    )


def add_offer_catalog_es(html: str) -> str:
    if "hasOfferCatalog" in html:
        return html
    return html.replace(
        '  "serviceType": ["Ilustración de libros infantiles"',
        ES_OFFER_CATALOG.strip() + '\n  "serviceType": ["Ilustración de libros infantiles"',
    )


def main() -> None:
    for rel in INDEXABLE:
        path = ROOT / rel
        if not path.exists():
            print(f"skip missing {rel}")
            continue
        text = path.read_text(encoding="utf-8")
        original = text
        text = add_sitemap_link(text)
        text = add_twitter_image_alt(text)
        text = add_twitter_url(text)
        if rel in ("nl/index.html", "es/index.html"):
            text = add_verification(text)
        if rel == "nl/services/index.html":
            text = add_offer_catalog_nl(text)
        if rel == "es/services/index.html":
            text = add_offer_catalog_es(text)
        if text != original:
            path.write_text(text, encoding="utf-8")
            print(f"updated {rel}")

    sitemap = ROOT / "sitemap.xml"
    sm = sitemap.read_text(encoding="utf-8")
    sm_new = sm.replace("<lastmod>2026-08-23</lastmod>", "<lastmod>2026-09-05</lastmod>")
    if sm_new != sm:
        sitemap.write_text(sm_new, encoding="utf-8")
        print("updated sitemap.xml lastmod")


if __name__ == "__main__":
    main()
