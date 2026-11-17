# Techno Industries colour balance

The design targets approximately **60% white/light surfaces, 30% navy and 10% gold** across the main website. These proportions come from visible section, panel and action surfaces, rather than colour-variable declarations alone.

| Role | Colour | Use |
| --- | --- | --- |
| Dominant | White `#FFFFFF`, light neutral `#F5F6F8` | Navigation, catalogues, forms, image panels and reading areas |
| Secondary | Navy `#0F2A43` | Company story, structured information, selected headings/panels and footer |
| Accent | Gold `#D98A1F` | Enquiry bands, supporting information, primary actions and details |

## Rendered coverage audit

The figures below record the theme pass after the homepage strip colour refinement, combining all eight company pages weighted by their rendered UI area. Later navigation spacing refinements may slightly change these shares. Natural photography and image logos are masked for the audit; the decorative hero studio background and strongly tinted UI overlays remain part of the design. Light neutrals count with white, and text/borders count toward their nearest palette colour. Measurements use the static reduced-motion presentation to keep the comparison consistent.

| Viewport | Version | White/light | Navy | Gold |
| --- | --- | ---: | ---: | ---: |
| 1440px desktop | Before | 74.79% | 23.67% | 1.54% |
| 1440px desktop | Updated | 62.03% | 29.34% | 8.63% |
| 375px mobile | Before | 70.70% | 26.52% | 2.77% |
| 375px mobile | Updated | 60.60% | 30.59% | 8.81% |

This is an approximate allocation of branded UI surfaces. The latest figures include the homepage closing-area refinement and compact, aligned white capability strip with navy text and gold icons. White quality/enquiry rows replace the isolated gold blocks, keeping gold for the action and small accents. Individual pages, photography, viewport widths and animation frames naturally produce different pixel shares.

## Maintaining the theme

Edit `assets/css/brand-theme.css`, which loads after page styles on all eight main company pages. It keeps white reading areas, uses navy where a page needs more structure, and gives gold a visible supporting role. It does not change the independently branded Farm or Grand Techno sites.

The homepage quality marks use the same automatic 64-second rightward loop as the Quality page, on an open white surface with the fixed quality heading. The following white enquiry row uses navy text and one gold action; both rows align with the compact navy footer. Shared motion lives in `assets/css/quality-marks.css` and `assets/js/quality-marks.js`; reduced-motion users get a static group. No manual controls are added.

With a local server running, reproduce the audit using the development-only Python/Playwright/Pillow/NumPy tooling:

```powershell
python tools/audit_colour_balance.py review 1440,375 http://127.0.0.1:5500
```

Normal screenshots, media-mask screenshots, section inventories and raw counts are saved under `tmp/colour-audit/review/`. The audit modifies only its browser session and temporary output; original photographs and logos are untouched. These development files are not needed for static hosting.

An optional fourth argument selects pages, for example `index` or `index,quality`. The latest homepage-only measurements are in `tmp/colour-audit/white-highlights/`; `combined-results.json` combines those counts with the unchanged seven-page measurements from the preceding colour pass.
