# Techno Printpack

Homepage hero photos now rotate automatically every five seconds with a one-second crossfade. Numbered slide controls have been removed. A small pause/play control is available on the photo; autoplay stops for reduced-motion preferences and hidden browser tabs. The original photo stays visible without JavaScript. Behavior is in `assets/js/main.js`, styles in `assets/css/homepage.css`; run `python tools/check_hero.py` for focused validation.

Eight connected, frontend-only HTML pages built directly in the existing workspace. No build step, backend, database or form storage is required. Gallery has been removed from the public pages, navigation, footer and sitemap; its homepage preview was also removed. Original company images remain untouched.

## Page directory

### Header dropdowns

About Us and the existing Industries item have dropdowns; no extra top-level navigation items were added. About Us contains Company Information, Why Choose Us, Vision/Mission/Values and certification documentation. Techno Group was removed from this submenu. Industries contains the requested Techno Industries, Grand Techno and Techno Farm buttons, intentionally without actions or additional pages. Products and Quality remain direct links. Dropdowns use white surfaces, navy text and light neutral dividers. One amber underline identifies the current top-level page. Desktop supports hover, click, Tab, arrow keys, Home/End and Escape. Mobile uses expandable sections; Escape closes the submenu before the main menu. Linked About details open automatically. Links remain available without JavaScript through hover/focus on desktop and expanded submenus on mobile.

Edit `tools/navigation.py` to update the link groups, and `assets/css/navigation.css` for appearance. Behavior lives in `assets/js/main.js`. Run `python tools/build_site.py` after editing navigation source. `python tools/check_navigation.py` tests the dropdown controls and category navigation. Only existing pages and real section anchors are linked; client, awards and career pages are not invented.

1. Home — `index.html`
2. About Us — `about.html`
3. Products & Packaging — `products.html`
4. Manufacturing Capabilities — `capabilities.html`
5. Industries We Serve — `industries.html`
6. Quality & Certifications — `quality.html`
7. Request a Quote — `quotation.html`
8. Contact Us — `contact.html`

The nine-page navigation and new page content are authored in `tools/additional_pages.py`, loaded by the shared builder. Short labels keep the header readable; full page names appear in the footer. Industries and Quality are independent pages, with homepage previews retained. The quality page explains how to request current certificates; no unverified certificate badge, validity date or downloadable certificate is presented as verified.

The About page follows the supplied About UI reference. Edit `tools/about_reference.py` for its composition and `assets/css/about.css` for styling. Its hero uses `111A1589`, production collage uses `111A1618` and `111A1529`, and printing banner uses `111A1563`, all from real converted packaging-company images. Group context is available in the expandable section at `about.html#group`. Social-media icons from the reference are omitted because official profile links have not been verified.

The Products page follows the supplied catalogue UI reference. Edit `tools/products_reference.py` and `assets/css/products.css` for its composition and styling. Five pill controls filter six product cards. Three visuals are actual company production photos, and three are labelled structure illustrations for formats without suitable packshots. Each card opens the quotation page with a supported packaging type selected. The navy custom-packaging banner links to the quotation builder. Mobile uses a single card column for readable descriptions and touch targets.

The Capabilities page follows the supplied manufacturing UI. Edit `tools/capabilities_reference.py` and `assets/css/capabilities.css`. It includes an angled photo hero, four strengths, four image-led capability cards and a custom-packaging consultation banner. Card arrows use native keyboard-accessible details controls, with enquiry links inside. Printing, die-cutting, custom structures and finishing are based on published offerings. Gluing machinery or an in-house gluing line is not claimed because it was not verified. The legacy `capabilities.html#quality-approach` anchor remains available and links to the dedicated quality page.

The Quality page follows the supplied quality UI. Edit `tools/quality_reference.py` and `assets/css/quality.css` (which reuses the capabilities hero and CTA styles). Actual company photos replace the reference's unverified testing-equipment images. Five specification checkpoints lead to the enquiry form; four keyboard-accessible documentation cards expand to explain what buyers can request. Generic document and material icons are used instead of certification logos. No in-house laboratory, testing equipment, inspection programme, ISO validity or environmental certification is asserted without verification.

The Contact page follows the supplied Contact UI. Edit `tools/contact_reference.py`, `assets/css/contact.css` and `assets/js/contact.js`. The static form validates and prepares an enquiry for review, then offers a mailto draft or clipboard copy. It does not send, store or claim successful submission of a message. Opening email requires a configured mail app. WhatsApp uses the same verified-number configuration as the quotation form and is disabled while that number is empty. Business hours remain unconfirmed. The map is a company-name/address search, not a verified exact place pin. `python tools/check_contact.py` validates the enquiry flow without sending messages.

## Preview

Open `index.html` directly, use VS Code Live Server, or run:

```powershell
python -m http.server 5173 --bind 127.0.0.1
```

Then visit http://127.0.0.1:5173/. Internet access loads Google Fonts, GSAP/ScrollTrigger, Swiper and Lucide from pinned CDN versions. Content remains readable when those libraries fail. Fonts have local fallbacks.

## Files

### Corporate design refresh

The refined composition uses a 1200px maximum content width, a 24px core grid gap and an 8px spacing rhythm. `assets/css/corporate.css` contains the shared corporate layout and responsive refinements. The homepage has a compact company navigation, manufacturing hero, practical service navigation, company introduction, illustrated carton range, manufacturing overview, packaging brief guide and a Swiper company-photo preview.

The latest homepage follows the user's supplied UI image, implemented in `tools/home_reference.py` and `assets/css/homepage.css`: angled navy/amber hero, photographic solution cards, manufacturing process banner, industry overview, quality approach, gallery and compact quotation strip. The 1320px content grid adapts to stacked layouts on mobile. This stylesheet loads only on `index.html`. `tools/site_design.py` loads the reference composition during generation. The hero's three numbered buttons select real company photographs; there is no forced autoplay. Industry and quality navigation links target actual homepage sections. Certification badges are excluded because current certification documents have not been verified.

`tools/site_design.py` contains the current shared identity, homepage composition and inner-page refinements. It is loaded by `tools/build_site.py`; edit these files before regenerating HTML. `tools/apply_refresh.py` is an idempotent migration helper and is not needed for normal authoring.

Logo assets: `assets/icons/logo-primary.svg`, `logo-white.svg` and `logo-symbol.svg`. The original folded-carton mark uses navy and amber. All versions are editable vector files; header and footer use the appropriate contrast variant. The favicon uses the same symbol. Logo wordmark typography uses Arial/Helvetica inside the SVG.

Original SVG carton diagrams are in `assets/media/carton-*.svg`. These are explicitly labelled structure illustrations, not representations of photographed stock or exact technical specifications. The catalogue now uses these drawings to explain product categories; real company photography remains throughout the manufacturing, company, gallery, contact and quotation pages.

Econopack (https://econopackltd.com/) was reviewed for its manufacturing-site information hierarchy and product discovery pattern. Its branding, photography, customer logos, testimonials and certification claims were not reused.

- `index.html`, `about.html`, `products.html`, `capabilities.html`, `gallery.html`, `quotation.html`, `contact.html`: deployable pages.
- `assets/css/`: design tokens and shared styling, responsive rules, motion preferences.
- `assets/js/`: navigation, filters, GSAP animation, Swiper gallery preview, accessible dialog gallery, enquiry generation and contact configuration.
- `assets/media/`: optimized 640px and 1600px WebP derivatives and complete source inventory.
- `images/`: untouched original company assets. These are not required on the public web server.
- `tools/build_site.py`: optional authoring generator for common header/footer, page content and metadata. Python is a development convenience, never a hosting requirement.
- `tools/prepare_images.py`: optional RAW and JPEG conversion script (requires `Pillow` and `rawpy`). Contact sheets are in `tools/`.
- `tools/qa.py` and `tools/qa-results.json`: local Playwright QA script and results. QA uses the local server at port 5173. It never sends enquiries.

## Update content and products

The delivered HTML can be edited directly. For reusable authoring, edit `tools/build_site.py`, then run `python tools/build_site.py` to regenerate all pages. This overwrites HTML, sitemap and favicon, so keep changes in the generator if using that route. CSS and JavaScript are maintained directly.

The `products` list defines category, product name, concise description, published options and a related factory-photo reference. `tools/site_design.py` maps the catalogue to labelled SVG structure illustrations. Update that mapping if adding products. Add a matching option to the quotation selector if changing the list manually. `data-category` values match the filter buttons. Approved product packshots can replace the illustrations when supplied; keep accurate alt text and remove the illustration caption for actual photographs.

## Update images

Preserve originals in `images/`. Run `python tools/prepare_images.py` to create derivatives, or export a real photo in WebP at 640px and 1600px into `assets/media/`. Reference both variants in `srcset` and set accurate dimensions and descriptive alt text. All 28 CR3 images were developed using LibRaw via rawpy, with camera white balance, then encoded as real WebP images. They were not renamed to a browser extension. The 19 farm JPEGs also have web derivatives. The original MOV is not embedded. Visually duplicated farm photos are retained but not repeated in the gallery.

See `ASSET-AUDIT.md` and `assets/media/inventory.json` for the original-to-web mapping.

## Configure WhatsApp

The official website publishes a mobile telephone number, but does not establish that it is an official WhatsApp enquiry channel. Therefore `assets/js/config.js` intentionally has an empty `whatsappNumber`.

After company confirmation, set that value to the official international number using digits only, including the country code, with no plus sign, spaces or leading local zero. The quotation page will then enable WhatsApp after validation and message review. It opens `wa.me` with a URL-encoded enquiry. Nothing is sent until the visitor sends it inside WhatsApp.

While unconfigured, the page offers a copyable enquiry and an email draft to the published company inbox. Neither claims to have submitted an enquiry. Fields are processed in memory only and not stored in browser storage or any database. The clipboard action requires a secure context or localhost; a manual selection fallback is provided. Email draft opening requires a configured email handler.

## Verified information and editorial boundaries

Sources reviewed on 3 November 2026:

- https://www.technoprintpack.com/
- https://www.technoprintpack.com/techno-industries.php
- https://www.technoprintpack.com/about-us.php

Those pages establish corrugated and PVC offerings, structural and material options, printing/finishing categories, the group businesses and published company contacts. The original contact page could not be fetched. Placeholder footer contacts on the original site were excluded. The original Grand Techno reference website could not be retrieved for visual comparison.

The public source calls the packaging division **Techno Industries**, while the brief requests **Techno Printpack** and a supplied photograph shows **TECHNO PRINT PACK** signage. The About page makes the naming relationship explicit. Confirm the final trading/legal name and approve copy before launch.

No dates of establishment, capacities, customer names, awards, employee counts, quantified achievements, business hours, social profiles or certification badges have been invented. No statistics counters appear because there are no verified packaging-business figures worth publishing. Group vision, mission and values are paraphrased and labeled as group statements. Specific application suitability, compliance, material availability and test documentation should be agreed with the company; this site makes no universal food-contact or environmental promise.

The map embeds a Google Maps search using the published company name and location, not a verified place ID. Confirm the exact pin and replace the iframe with a company-approved embed when available. Maps and CDN/font providers receive normal network requests. Include an approved privacy policy or consent handling if required for your final deployment context.

## Deploy to standard hosting

Upload the seven HTML files, `assets/`, `sitemap.xml` and `robots.txt` to the document root using your hosting file manager or SFTP. Do not upload `.git`, original RAW photos or development `tools/`. Keep directory names and file casing unchanged.

Canonical, Open Graph, structured data and sitemap URLs use the requested existing domain `https://www.technoprintpack.com/`. Change all of them if deploying to another final domain. Hosting must serve `index.html` as the home document and enable HTTPS. Configure permanent redirects from legacy PHP URLs to the appropriate new HTML pages through the hosting control panel. Never redirect unrelated pages to a misleading destination. Social previews use a real company factory photo.

For strict Content Security Policy, allow the listed CDN/font/map origins and account for the inline JSON-LD. Configure caching and compression through the host. Serve HTML with short cache lifetimes and static assets with appropriate caching. No hosting was changed or public site deployed as part of this local workspace implementation.

## Validation

Run `python tools/qa.py` with Playwright installed and the preview server running. It checks 7 pages at 320, 375, 430, 768, 1024, 1440 and 1920px; local links and assets; console exceptions; menu controls; catalogue filters; gallery filtering, next image and Escape; form validation; default disabled and configured WhatsApp availability; and readable no-JavaScript homepage content. Generated screenshots support visual inspection. Performance and Lighthouse scores depend on the final host and connection and are not guaranteed or represented as measured.
