# Techno Industries colour balance

White and light-grey surfaces lead the current design. Navy structures the company sections and footer; gold is reserved for controls and small accents. Supporting information panels use neutral surfaces rather than solid yellow fills.

| Role | Colour | Use |
| --- | --- | --- |
| Dominant | White `#FFFFFF`, light neutral `#F5F6F8` | Navigation, catalogues, forms, image panels and reading areas |
| Secondary | Navy `#0F2A43` | Company story, structured information, selected headings/panels and footer |
| Accent | Gold `#D98A1F` | Primary actions, small rules, icons and details |

## Rendered coverage audit

These recorded measurements precede the content-action cleanup and neutral section redesign. Removing repeated quotation bands and replacing gold content panels changes page heights and colour coverage; rerun the optional audit for new measurements.

The figures below record the theme pass after the homepage strip colour refinement, combining all eight company pages weighted by their rendered UI area. Later navigation spacing refinements may slightly change these shares. Natural photography and image logos are masked for the audit; the decorative hero studio background and strongly tinted UI overlays remain part of the design. Light neutrals count with white, and text/borders count toward their nearest palette colour. Measurements use the static reduced-motion presentation to keep the comparison consistent.

| Viewport | Version | White/light | Navy | Gold |
| --- | --- | ---: | ---: | ---: |
| 1440px desktop | Before | 74.79% | 23.67% | 1.54% |
| 1440px desktop | Updated | 62.03% | 29.34% | 8.63% |
| 375px mobile | Before | 70.70% | 26.52% | 2.77% |
| 375px mobile | Updated | 60.60% | 30.59% | 8.81% |

These historical figures record the earlier white capability-strip refinement before the subsequent content cleanup and neutral section redesign. Individual pages, photography, viewport widths and animation frames naturally produce different pixel shares.

## Maintaining the theme

Edit `assets/css/brand-theme.css`, which loads after page styles on all eight main company pages. It keeps white reading areas, uses navy where a page needs more structure, and gives gold a visible supporting role. It does not change the independently branded Farm or Grand Techno sites.

The homepage quality marks use the same automatic 64-second rightward loop as the Quality page. The full-width white rail sits beneath a heading and outlined documentation action, aligned with the compact navy footer. Shared motion lives in `assets/css/quality-marks.css` and `assets/js/quality-marks.js`; reduced-motion users get a static group. No manual controls are added.

With a local server running, reproduce the audit using the development-only Python/Playwright/Pillow/NumPy tooling:

```powershell
python tools/audit_colour_balance.py review 1440,375 http://127.0.0.1:5500
```

Normal screenshots, media-mask screenshots, section inventories and raw counts are saved under `tmp/colour-audit/review/`. The audit modifies only its browser session and temporary output; original photographs and logos are untouched. These development files are not needed for static hosting.

An optional fourth argument selects pages, for example `index` or `index,quality`. The recorded homepage-only measurements are in `tmp/colour-audit/white-highlights/`; `combined-results.json` combines those counts with the seven-page measurements from that colour pass.
