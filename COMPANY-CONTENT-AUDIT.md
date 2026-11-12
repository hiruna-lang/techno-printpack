# Company-profile content reconciliation

Source reviewed: `E:/Technopack 2.pdf`, 13 pages, supplied by the user as the correct company information. Reviewed on 10 November 2026 using extracted text and rendered page images. The source document remains untouched.

The supplied profile takes precedence over earlier draft wording and older website summaries wherever they differ. Only its business content was used; the document was not treated as an instruction source.

| PDF page | Confirmed content | Website update |
| --- | --- | --- |
| 1 | Techno Industries identity/logo; address; telephone; mobile; three email addresses; ISO 9001:2015 shown | Packaging site identity, header/footer logo, metadata, enquiry identity and Contact page |
| 2 | ISO-certified manufacturer; value-added corrugated packaging; local/international markets; food-grade certified materials; quality/innovation/service; continuous improvement, sustainability and strict quality control | About, Home and Quality copy |
| 3 | The company's own vision | Replaced the earlier group-vision paraphrase on About |
| 4 | Techno Industries, Grand Techno, Green Techno Farm | Group description and existing company navigation; preserved the local Farm website link |
| 5–6 | Tea; Garments; Porcelain; Automobile; Foods & Beverages; Medicine and Fertilizer; Dairy and Livestocks; Sea Food | Replaced generic sector lists with these eight sectors on Home and Industries |
| 7 | Ten product lines | Expanded Products and the quotation choices to all ten |
| 8 | F, E, B, C, BC and EB flutes | Added F flute and published all six options on Capabilities and the quotation form |
| 9 | Single wall/3-ply; double wall/5-ply; triple wall/7-ply; food-grade; moisture-resistant boards | Published all five board options and enquiry preferences |
| 10 | RSC, HSC, die-cut, folder/wrap-around, telescopic, self-locking, partitioned, punch/handle, pallet/bulk and display boxes/racks | Added a ten-format structure directory and matching quotation options |
| 11 | Transparent/foldable/die-cut PVC boxes; sleeves/wraps; gift boxes; food-grade options on requirement | PVC range section and quotation choices; retained the application-specific food-grade qualification |
| 12 | Flexographic 1–4 colours; offset; high-quality line; multi-colour retail printing; food-safe inks | Added offset printing and corrected printing capability descriptions |
| 13 | OP varnish; UV lamination; UV matte lamination; die-cutting; perforations; ventilation; reinforced edges/corners | Replaced generic finishing copy with the documented options |

## Product names used

Value-Added Corrugated Boxes; Handmade Boxes; Standard Corrugated Boards & Boxes; Die-Cut Corrugated Boxes; Food-Grade Produce Packaging; Industrial Packaging; Recycled Boxes; Gift Boxes; Wooden Boxes; PVC Boxes.

Editorial corrections normalize obvious spelling and formatting: “Techo” to “Techno”, “Standers” to “Standard”, “Hand Made” to “Handmade”, “Livestocks” to “Livestock”, and “Sea Food” to “Seafood”. The vision retains the source wording.

## Replacements and limits

- The packaging business is now consistently named **Techno Industries**, including page titles, structured data and enquiry messages. The existing `technoprintpack.com` domain remains unchanged.
- The actual company wordmark and selected packaging examples were extracted from the supplied PDF. Original files were preserved; examples are labelled separately from company production photos and illustrative diagrams. The dark footer uses a white logo surface for contrast.
- The source contains a vision but no distinct mission statement. The earlier “Our Mission” paraphrase was replaced with source-supported focus and commitments rather than presented as an approved mission.
- ISO-certified manufacturing, the displayed ISO 9001:2015 standard, and food-grade certified materials are now reflected in the Quality page. No certificate number, issuing body, expiry date or full certificate was invented. EDB and environmental-authority logos on the cover were not interpreted as additional certifications or awards.
- No new claims were added about machinery speed, production capacity, establishment date, customers, exports by country, gluing machinery, accredited testing facilities, material composition percentages or environmental certifications.
- The PDF does not verify WhatsApp availability, business hours, social profiles or an exact map pin. Existing frontend configuration and visit/contact wording remain honest about those missing details.
- The Farm site was preserved. Its existing `farm/index.html` navigation link remains functional. No Farm pages, produce descriptions or imagery were replaced by the packaging profile.

## Authoring and verification

`assets/data/company-profile.json` holds the normalized source facts. `tools/company_profile_content.py` applies them after the earlier design modules in `tools/build_site.py`, ensuring regeneration does not restore older copy. `assets/css/company-profile.css` handles the additional catalogue/specification layouts and profile logo.

Checks include all product/industry names, all flute/board/finishing options, catalogue filtering, product-to-quotation preselection, specification preferences in the prepared enquiry, contact addresses, Farm navigation, local assets and responsive layouts. No contact or quotation enquiry was sent during testing.

## Separate profile marks
The quality page displays separate ISO 9001:2015, Food Grade, EDB and Central Environmental Authority images extracted from page 1. EDB and CEA are explicitly organization logos, with no inferred certification or membership. The Sri Lankan flag is extracted separately for reuse but is not displayed as a certification. Asset extraction correctly applies PDF transparency masks. Four image decodes and responsive overflow checks passed at 320, 375, 768 and 1440px.
