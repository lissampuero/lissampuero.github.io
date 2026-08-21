# Global Navigation — Relative Path Matrix

## English (EN)

| Page | HOME | ABOUT | SERVICES | EDITORIAL | NARRATIVE | STATIONERY | CONTACT | NL | ES |
|---|---|---|---|---|---|---|---|---|---|
| index.html | ./ | about/ | services/ | portfolio/editorial/ | portfolio/narrative/ | portfolio/stationery/ | contact/ | nl/ | es/ |
| about/ | ../ | about.html | ../services/ | ../portfolio/editorial/ | ../portfolio/narrative/ | ../portfolio/stationery/ | ../contact/ | ../nl/about/ | ../es/about/ |
| services/ | ../ | ../about/ | services.html | ../portfolio/editorial/ | ../portfolio/narrative/ | ../portfolio/stationery/ | ../contact/ | ../nl/services/ | ../es/services/ |
| portfolio/editorial/ | ../../ | ../../about/ | ../../services/ | ./ | ../narrative/ | ../stationery/ | ../../contact/ | ../../nl/portfolio/editorial/ | ../../es/portfolio/editorial/ |
| portfolio/narrative/ | ../../ | ../../about/ | ../../services/ | ../editorial/ | ./ | ../stationery/ | ../../contact/ | ../../nl/portfolio/narrative/ | ../../es/portfolio/narrative/ |
| portfolio/stationery/ | ../../ | ../../about/ | ../../services/ | ../editorial/ | ../narrative/ | ./ | ../../contact/ | ../../nl/portfolio/stationery/ | ../../es/portfolio/stationery/ |
| contact/ | ../ | ../about/ | ../services/ | ../portfolio/editorial/ | ../portfolio/narrative/ | ../portfolio/stationery/ | ./ | ../nl/contact/ | ../es/contact/ |

## Dutch (NL)

| Page | HOME | ABOUT | SERVICES | EDITORIAL | NARRATIVE | STATIONERY | CONTACT | EN | ES |
|---|---|---|---|---|---|---|---|---|---|
| nl/index.html | ./ | about/ | services/ | portfolio/editorial/ | portfolio/narrative/ | portfolio/stationery/ | contact/ | ../ | ../es/ |
| nl/about/ | ../ | about.html | ../services/ | ../portfolio/editorial/ | ../portfolio/narrative/ | ../portfolio/stationery/ | ../contact/ | ../../about/ | ../../es/about/ |
| nl/services/ | ../ | ../about/ | services.html | ../portfolio/editorial/ | ../portfolio/narrative/ | ../portfolio/stationery/ | ../contact/ | ../../services/ | ../../es/services/ |
| nl/portfolio/editorial/ | ../../ | ../../about/ | ../../services/ | ./ | ../narrative/ | ../stationery/ | ../../contact/ | ../../../portfolio/editorial/ | ../../../es/portfolio/editorial/ |
| nl/portfolio/narrative/ | ../../ | ../../about/ | ../../services/ | ../editorial/ | ./ | ../stationery/ | ../../contact/ | ../../../portfolio/narrative/ | ../../../es/portfolio/narrative/ |
| nl/portfolio/stationery/ | ../../ | ../../about/ | ../../services/ | ../editorial/ | ../narrative/ | ./ | ../../contact/ | ../../../portfolio/stationery/ | ../../../es/portfolio/stationery/ |
| nl/contact/ | ../ | ../about/ | ../services/ | ../portfolio/editorial/ | ../portfolio/narrative/ | ../portfolio/stationery/ | ./ | ../../contact/ | ../../es/contact/ |

## Spanish (ES)

| Page | HOME | ABOUT | SERVICES | EDITORIAL | NARRATIVE | STATIONERY | CONTACT | EN | NL |
|---|---|---|---|---|---|---|---|---|---|
| es/index.html | ./ | about/ | services/ | portfolio/editorial/ | portfolio/narrative/ | portfolio/stationery/ | contact/ | ../ | ../nl/ |
| es/about/ | ../ | about.html | ../services/ | ../portfolio/editorial/ | ../portfolio/narrative/ | ../portfolio/stationery/ | ../contact/ | ../../about/ | ../../nl/about/ |
| es/services/ | ../ | ../about/ | services.html | ../portfolio/editorial/ | ../portfolio/narrative/ | ../portfolio/stationery/ | ../contact/ | ../../services/ | ../../nl/services/ |
| es/portfolio/editorial/ | ../../ | ../../about/ | ../../services/ | ./ | ../narrative/ | ../stationery/ | ../../contact/ | ../../../portfolio/editorial/ | ../../../nl/portfolio/editorial/ |
| es/portfolio/narrative/ | ../../ | ../../about/ | ../../services/ | ../editorial/ | ./ | ../stationery/ | ../../contact/ | ../../../portfolio/narrative/ | ../../../nl/portfolio/narrative/ |
| es/portfolio/stationery/ | ../../ | ../../about/ | ../../services/ | ../editorial/ | ../narrative/ | ./ | ../../contact/ | ../../../portfolio/stationery/ | ../../../nl/portfolio/stationery/ |
| es/contact/ | ../ | ../about/ | ../services/ | ../portfolio/editorial/ | ../portfolio/narrative/ | ../portfolio/stationery/ | ./ | ../../contact/ | ../../nl/contact/ |

Shared assets: `shared/site-chrome.css` + `shared/site-nav.js` (adjust depth prefix per page).
EN CSS/JS/art reused by NL/ES via relative paths — no duplication.

Contact is now a dedicated page (`/contact/`, `/nl/contact/`, `/es/contact/`) instead of an
in-page anchor — it no longer appears embedded on Home, Services, or the Portfolio pages.
