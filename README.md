# Liss Ampuero Portfolio — Code Handoff Package

This package contains all HTML/CSS components built so far in design
sessions, organized by page/purpose. **Read this alongside
`lissampuero-master-spec-v4-FINAL.md`** — that document is the source
of truth for content, copy, SEO, and architecture; these files are the
working visual/interaction code that already implements parts of it.

## How to use this in Cursor

1. Drop the master spec `.md` file into `.cursor/rules/` at your project
   root first — this gives Cursor persistent context.
2. Use the files below as a **starting point**, not a finished site —
   they need to be:
   - Ported into your actual framework/build setup (Tailwind classes
     should replace the hand-written CSS where the spec calls for it)
   - Split into the `/`, `/nl/`, `/es/` folder structure defined in the
     spec (these files are currently English-only, single-version)
   - Connected to the asset paths defined in Section 12 of the spec
     (current `<img src="...">` paths use working names from the design
     phase — rename per the spec's asset map before final upload)

## Folder contents

### `/about/`
`about.html` + `about-styles.css` — the complete About Me page: arch
hero (fuchsia band + cream arch), oval slogan badge, portrait offset
block, storytelling artwork with click-to-expand lightbox (vanilla JS,
included inline in the HTML), and a full persuasive contact section
(heading + intro line + working form fields + direct contact info).
**Fully synced with spec Sections 5.2/5.3/5.9 (EN) as of this version —
bio, slogan, and contact-form copy all match verbatim.**

### `/services/`
`services.html` + `services-styles.css` — the complete Services page:
yellow hero band (title + slogan + studio illustration), turquoise band
with the **final six-category service taxonomy** (Editorial & Book
Design, Character Design & Narrative Worlds, Branding & Identity,
Fashion Illustration, Stationery & Custom Products, Classic Art &
Commissions), the deliverables line, the "Drop an idea / Get a full
universe" process diagram, and the closing CTA with two buttons that
open floating contact-method menus (Email/WhatsApp/Form). **Fully
synced with spec Sections 5.4-5.7 (EN) as of this version** — this
replaces the earlier draft's incomplete 3-column service list.

### `/fashion/`
`fashion-editorial.html` — the full-bleed magazine-style Fashion page:
citrus color bands, glassmorphism text cards, script-font micro-titles
for each piece (Tropical Call, Gilded Hour, Palazzo Bloom, Flamenco
Noir). **This is the "magazine total" approved version** — note there
were two earlier draft directions (a numbered-card grid, and a compact
mosaic) that were explicitly rejected in favor of this one; don't revert
to those patterns if regenerating this page.

### `/children-books/`
`component-cloud-transition.html` — the reusable SVG "organic cloud"
band-transition component (curved Bézier path, ~1.2° rotation,
color-matched to the following section). This is a **pattern to apply
across the whole Children's Books page**, not a complete page itself —
that full page was never built, only this transition component.

### `/shared/`
- `color-system-citrus-palette.css` — the `:root` CSS custom properties
  for the full citrus palette (vibrant + pastel variants). This should
  become the single source of color tokens site-wide (or be ported into
  `tailwind.config.js` theme colors).
- `component-portrait-offset-block.html` — reusable "photo with offset
  color block behind it" pattern, used in About, reusable anywhere a
  portrait needs the same editorial treatment.
- `component-fullwidth-banner-strip.html` — reusable 3-layer banner
  pattern (solid background + floating illustration + top-layer
  typography), used as the base pattern for several full-bleed sections
  across the site.

## What's NOT in this package (not yet built)

- Home page (`index.html`) — only specified in the master spec
  (Section 4), never coded
- Editorial page — layout pattern specified (spec Section 7 references
  "illustration-as-background-band"), never coded
- Narrative & Character Universes page (Marquise de Croac + LoLo
  sections) — never coded
- Children's Books full page — only the cloud-transition component
  exists; the page itself was never assembled
- Stationery & Products page — never coded
- Contact page as a standalone route (currently only exists as a
  section embedded in About/Services)
- Any `/nl/` or `/es/` language folder — all current files are
  English-only single-version drafts

## Known technical debt to resolve during Cursor build

1. **Inline `<style>` blocks** — every file currently has CSS embedded
   directly in `<style>` tags within the HTML rather than properly
   separated, OR in a same-purpose external `.css` file with
   hand-written rules (not Tailwind utility classes). Section 10/13 of
   the master spec calls for a real Tailwind implementation — treat
   these files as a design reference to convert, not code to keep as-is.
2. **No build pipeline** — no bundler, no image optimization, no WebP
   conversion has been applied to anything yet. Spec Section 3 defines
   the performance budget this needs to hit.
3. **Vanilla JS only** — lightbox and contact-menu toggle scripts are
   plain JS, inline in each HTML file. Fine to keep as vanilla per spec
   Section 10, but should be extracted into shared `.js` files instead
   of duplicated inline in every page that needs a lightbox.
