#!/usr/bin/env python3
"""Apply international SEO optimizations without changing visual design."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

PUBLIC_PAGES = [
    "index.html",
    "404.html",
    "es/index.html",
    "nl/index.html",
    "about/index.html",
    "es/about/index.html",
    "nl/about/index.html",
    "services/index.html",
    "es/services/index.html",
    "nl/services/index.html",
    "contact/index.html",
    "contact/thanks.html",
    "es/contact/index.html",
    "es/contact/thanks.html",
    "nl/contact/index.html",
    "nl/contact/thanks.html",
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

FAVICON_ABS = "https://lissampuero.com/assets/home/logo-liss-ampuero-hero-mobile.webp"
GEO_BLOCK = """
        "geo": {
          "@type": "GeoCoordinates",
          "latitude": 51.1764,
          "longitude": 4.8364
        },"""

FAQ_EN = """
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "What illustration services does Liss Ampuero offer?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Children's book illustration, editorial layout, character design, brand and packaging illustration, fashion and magazine art, murals, and custom commissions for publishers, agencies, and brands."
      }
    },
    {
      "@type": "Question",
      "name": "Where is the studio based and do you work internationally?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "The studio is in Herentals, Belgium, and works with clients across Europe and worldwide in English, Spanish, and Dutch."
      }
    },
    {
      "@type": "Question",
      "name": "How do I start a commission?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Use the contact form, email lissampuero@outlook.com, or WhatsApp +32 472 12 05 50. Share your project scope, timeline, and budget for a quote or exploratory call."
      }
    }
  ]
}
</script>"""

FAQ_ES = """
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "¿Qué servicios de ilustración ofrece Liss Ampuero?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Ilustración infantil, maquetación editorial, diseño de personajes, ilustración de marca y packaging, moda y revista, murales y encargos a medida para editoriales, agencias y marcas."
      }
    },
    {
      "@type": "Question",
      "name": "¿Dónde está el estudio y trabajáis a nivel internacional?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "El estudio está en Herentals, Bélgica, y trabaja con clientes en Europa y en todo el mundo en inglés, español y neerlandés."
      }
    },
    {
      "@type": "Question",
      "name": "¿Cómo empiezo un encargo?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Usa el formulario de contacto, escribe a lissampuero@outlook.com o WhatsApp +32 472 12 05 50. Comparte alcance, plazos y presupuesto para recibir un presupuesto o una llamada exploratoria."
      }
    }
  ]
}
</script>"""

FAQ_NL = """
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "Welke illustratiediensten biedt Liss Ampuero aan?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Prentenboekillustratie, redactionele lay-out, personage-ontwerp, merk- en verpakkingsillustratie, mode- en magazinekunst, muurschilderingen en maatwerkopdrachten voor uitgevers, agencies en merken."
      }
    },
    {
      "@type": "Question",
      "name": "Waar is het atelier gevestigd en werk je internationaal?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Het atelier is in Herentals, België, en werkt met klanten in Europa en wereldwijd in het Engels, Spaans en Nederlands."
      }
    },
    {
      "@type": "Question",
      "name": "Hoe start ik een opdracht?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Gebruik het contactformulier, mail lissampuero@outlook.com of WhatsApp +32 472 12 05 50. Deel scope, timing en budget voor een offerte of verkennend gesprek."
      }
    }
  ]
}
</script>"""


def favicon_links_for(rel_path: str) -> str:
    depth = rel_path.count("/")
    prefix = "../" * depth if depth else ""
    href = f"{prefix}assets/home/logo-liss-ampuero-hero-mobile.webp"
    return (
        f'  <link rel="icon" href="{href}" type="image/webp">\n'
        f'  <link rel="apple-touch-icon" href="{href}">\n'
    )


def inject_favicon(html: str, rel_path: str) -> str:
    if 'rel="icon"' in html:
        return html
    block = favicon_links_for(rel_path)
    return html.replace(
        '<meta name="viewport" content="width=device-width, initial-scale=1.0">',
        '<meta name="viewport" content="width=device-width, initial-scale=1.0">\n\n' + block.rstrip(),
        1,
    )


def inject_geo_in_professional_service(html: str) -> str:
    if '"GeoCoordinates"' in html:
        return html
    marker = '"addressCountry": "BE"\n        },'
    if marker not in html:
        return html
    return html.replace(marker, '"addressCountry": "BE"\n        },' + GEO_BLOCK, 1)


def inject_faq(html: str, faq_block: str) -> str:
    if '"FAQPage"' in html:
        return html
    return html.replace("</head>", faq_block + "\n</head>", 1)


def main() -> None:
    global_replacements = [
        ("shop-front.png", "shop-front.webp"),
        (
            "logo-liss-ampuero-hero.png",
            "logo-liss-ampuero-hero.webp",
        ),
    ]

    file_replacements: dict[str, list[tuple[str, str]]] = {
        "index.html": [
            (
                "<title>Liss Ampuero | Digital Artist, Character Designer &amp; Editorial Illustrator</title>",
                "<title>Liss Ampuero | Illustrator &amp; Art Director · Belgium · Hire for Books &amp; Brands</title>",
            ),
            (
                'content="Portfolio of Liss Ampuero, digital artist and illustrator specializing in character design, children\'s book illustration, and editorial art."',
                'content="Hire Liss Ampuero, illustrator and art director in Belgium for children\'s books, character design, branding, editorial and fashion illustration. Publishers and agencies worldwide."',
            ),
            (
                '<meta property="og:title" content="Liss Ampuero | Digital Artist &amp; Character Designer">',
                '<meta property="og:title" content="Liss Ampuero | Illustrator &amp; Art Director · Belgium">',
            ),
            (
                'content="Explore the digital illustration portfolio, character design, and editorial projects of Liss Ampuero."',
                'content="Hire Liss Ampuero for children\'s books, character design, branding and editorial illustration from Belgium. Working with publishers and brands worldwide."',
            ),
            (
                '<meta name="twitter:title" content="Liss Ampuero | Digital Artist &amp; Character Designer">',
                '<meta name="twitter:title" content="Liss Ampuero | Illustrator &amp; Art Director · Belgium">',
            ),
            (
                'content="Official portfolio of Liss Ampuero. Specialist in character design and children\'s book illustration."',
                'content="Illustrator and art director in Belgium. Children\'s books, character design, branding and editorial for clients worldwide."',
            ),
            (
                '<h1 class="sr-only">Liss Ampuero — Digital Artist &amp; Character Designer</h1>',
                '<h1 class="sr-only">Liss Ampuero — Illustrator &amp; Art Director in Belgium</h1>',
            ),
            (
                '        "jobTitle": "Digital Artist & Illustrator",',
                '        "jobTitle": "Illustrator & Art Director",',
            ),
            (
                '        "telephone": "+32472120550",\n        "address": {',
                '        "telephone": "+32472120550",\n        "description": "Digital artist, illustrator and art director based in Herentals, Belgium. Children\'s books, character design, branding, packaging and editorial illustration for clients in Europe and worldwide.",\n        "knowsLanguage": ["en", "es", "nl"],\n        "workLocation": { "@type": "Place", "name": "Herentals, Belgium" },\n        "address": {',
            ),
            (
                '<p class="hm-hero__slogan">Worlds you can step into.</p>',
                '<p class="hm-hero__slogan">Worlds you can step into.</p>\n        <p class="hm-hero__tagline">Illustrator &amp; digital artist · Belgium · Worldwide</p>',
            ),
        ],
        "es/index.html": [
            (
                "<title>Liss Ampuero | Ilustradora y Directora de Arte, Bélgica</title>",
                "<title>Liss Ampuero | Ilustradora, Diseñadora y Directora de Arte · Bélgica</title>",
            ),
            (
                '<meta property="og:title" content="Liss Ampuero | Ilustradora y Directora de Arte, Bélgica">',
                '<meta property="og:title" content="Liss Ampuero | Ilustradora, Diseñadora y Directora de Arte · Bélgica">',
            ),
            (
                '<meta name="twitter:title" content="Liss Ampuero | Ilustradora y Directora de Arte, Bélgica">',
                '<meta name="twitter:title" content="Liss Ampuero | Ilustradora, Diseñadora y Directora de Arte · Bélgica">',
            ),
            (
                '<p class="hm-hero__slogan">Mundos en los que puedes entrar.</p>',
                '<p class="hm-hero__slogan">Mundos en los que puedes entrar.</p>\n        <p class="hm-hero__tagline">Ilustradora y artista digital · Bélgica · Todo el mundo</p>',
            ),
        ],
        "nl/index.html": [
            (
                "<title>Liss Ampuero | Illustrator &amp; Art Director, België</title>",
                "<title>Liss Ampuero | Illustrator &amp; Artdirecteur · België</title>",
            ),
            (
                'content="Huur Liss Ampuero, illustrator en art director in België voor prentenboeken, personage-ontwerp, branding en redactioneel werk. Uitgevers en agencies wereldwijd."',
                'content="Huur Liss Ampuero, illustrator en artdirecteur in België voor prentenboeken, personage-ontwerp, branding en redactioneel werk. Uitgevers en agencies wereldwijd."',
            ),
            (
                '<meta property="og:title" content="Liss Ampuero | Illustrator &amp; Art Director, België">',
                '<meta property="og:title" content="Liss Ampuero | Illustrator &amp; Artdirecteur · België">',
            ),
            (
                'content="Huur Liss Ampuero, illustrator en art director in België voor prentenboeken, personage-ontwerp, branding en redactioneel werk. Uitgevers en agencies wereldwijd."',
                'content="Huur Liss Ampuero, illustrator en artdirecteur in België voor prentenboeken, personage-ontwerp, branding en redactioneel werk. Uitgevers en agencies wereldwijd."',
            ),
            (
                '<meta name="twitter:title" content="Liss Ampuero | Illustrator &amp; Art Director, België">',
                '<meta name="twitter:title" content="Liss Ampuero | Illustrator &amp; Artdirecteur · België">',
            ),
            (
                'content="Huur Liss Ampuero, illustrator en art director in België voor prentenboeken, personage-ontwerp, branding en redactioneel werk. Uitgevers en agencies wereldwijd."',
                'content="Huur Liss Ampuero, illustrator en artdirecteur in België voor prentenboeken, personage-ontwerp, branding en redactioneel werk. Uitgevers en agencies wereldwijd."',
            ),
            (
                '        "jobTitle": "Illustrator & Art Director",',
                '        "jobTitle": "Illustrator & Artdirecteur",',
            ),
            (
                '<h1 class="sr-only">Liss Ampuero — Illustrator en Art Director in België</h1>',
                '<h1 class="sr-only">Liss Ampuero — Illustrator en Artdirecteur in België</h1>',
            ),
            (
                '<p class="hm-hero__slogan">Werelden waar je in kunt stappen.</p>',
                '<p class="hm-hero__slogan">Werelden waar je in kunt stappen.</p>\n        <p class="hm-hero__tagline">Illustrator &amp; digitaal kunstenaar · België · Wereldwijd</p>',
            ),
        ],
        "about/index.html": [
            (
                "<title>About Liss Ampuero | Illustrator &amp; Art Director Portfolio</title>",
                "<title>About Liss Ampuero | Illustrator &amp; Art Director · Belgium</title>",
            ),
            (
                '<meta property="og:title" content="About Liss Ampuero | Illustrator & Art Director Portfolio">',
                '<meta property="og:title" content="About Liss Ampuero | Illustrator &amp; Art Director · Belgium">',
            ),
            (
                '<meta name="twitter:title" content="About Liss Ampuero | Illustrator & Art Director Portfolio">',
                '<meta name="twitter:title" content="About Liss Ampuero | Illustrator &amp; Art Director · Belgium">',
            ),
        ],
        "nl/about/index.html": [
            (
                "<title>Over Liss Ampuero | Illustrator &amp; Art Director</title>",
                "<title>Over Liss Ampuero | Illustrator &amp; Artdirecteur · België</title>",
            ),
            (
                'content="Maak kennis met Liss Ampuero, illustrator en art director in België. Prentenboeken, personages, branding en redactioneel werk voor uitgevers en agencies."',
                'content="Maak kennis met Liss Ampuero, illustrator en artdirecteur in België. Prentenboeken, personages, branding en redactioneel werk voor uitgevers en agencies."',
            ),
            (
                '<meta property="og:title" content="Over Liss Ampuero | Illustrator &amp; Art Director">',
                '<meta property="og:title" content="Over Liss Ampuero | Illustrator &amp; Artdirecteur · België">',
            ),
            (
                'content="Maak kennis met Liss Ampuero, illustrator en art director in België. Prentenboeken, personages, branding en redactioneel werk voor uitgevers en agencies."',
                'content="Maak kennis met Liss Ampuero, illustrator en artdirecteur in België. Prentenboeken, personages, branding en redactioneel werk voor uitgevers en agencies."',
            ),
            (
                '<meta name="twitter:title" content="Over Liss Ampuero | Illustrator &amp; Art Director">',
                '<meta name="twitter:title" content="Over Liss Ampuero | Illustrator &amp; Artdirecteur · België">',
            ),
            (
                'content="Maak kennis met Liss Ampuero, illustrator en art director in België. Prentenboeken, personages, branding en redactioneel werk voor uitgevers en agencies."',
                'content="Maak kennis met Liss Ampuero, illustrator en artdirecteur in België. Prentenboeken, personages, branding en redactioneel werk voor uitgevers en agencies."',
            ),
            (
                '"jobTitle": "Illustrator & Art Director",',
                '"jobTitle": "Illustrator & Artdirecteur",',
            ),
        ],
        "es/services/index.html": [
            (
                "<title>Servicios de ilustración y dirección de arte | Liss Ampuero</title>",
                "<title>Servicios de ilustración, diseño y dirección de arte | Liss Ampuero</title>",
            ),
            (
                '<meta property="og:title" content="Servicios de ilustración y dirección de arte | Liss Ampuero">',
                '<meta property="og:title" content="Servicios de ilustración, diseño y dirección de arte | Liss Ampuero">',
            ),
            (
                '<meta name="twitter:title" content="Servicios de ilustración y dirección de arte | Liss Ampuero">',
                '<meta name="twitter:title" content="Servicios de ilustración, diseño y dirección de arte | Liss Ampuero">',
            ),
            (
                '"name": "Servicios de ilustración y dirección de arte",',
                '"name": "Servicios de ilustración, diseño y dirección de arte",',
            ),
        ],
        "nl/contact/index.html": [
            (
                '"jobTitle": "Illustrator & Art Director",',
                '"jobTitle": "Illustrator & Artdirecteur",',
            ),
        ],
        "es/contact/index.html": [
            (
                '"jobTitle": "Illustrator & Art Director",',
                '"jobTitle": "Ilustradora y Directora de Arte",',
            ),
        ],
    }

    faq_map = {
        "services/index.html": FAQ_EN,
        "es/services/index.html": FAQ_ES,
        "nl/services/index.html": FAQ_NL,
    }

    changed: list[str] = []

    for rel in PUBLIC_PAGES:
        path = ROOT / rel
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        original = text

        for old, new in global_replacements:
            text = text.replace(old, new)

        for old, new in file_replacements.get(rel, []):
            text = text.replace(old, new)

        text = inject_favicon(text, rel)

        if rel in ("index.html", "es/index.html", "nl/index.html"):
            text = inject_geo_in_professional_service(text)

        if rel in faq_map:
            text = inject_faq(text, faq_map[rel])

        if text != original:
            path.write_text(text, encoding="utf-8")
            changed.append(rel)

    print(f"Updated {len(changed)} files:")
    for name in changed:
        print(f"  - {name}")


if __name__ == "__main__":
    main()
