"""Update shared headers, footers and responsive/navigation asset links across all 10 pages."""
from pathlib import Path
import re, sys
from navigation_markup import render_header, render_footer

ROOT = Path(__file__).resolve().parents[1]
PAGES = ['index', 'about', 'products', 'capabilities', 'industries', 'quality', 'quotation', 'contact']
ASSET_VERSION = '6'
check = '--check' in sys.argv

# 1. Main company pages
for name in PAGES:
    path = ROOT / f'{name}.html'
    before = path.read_text(encoding='utf-8')
    after, count = re.subn(r'<header class="header">.*?</header>', lambda _: render_header(name), before, count=1, flags=re.S)
    assert count == 1, name
    after, f_count = re.subn(r'<footer class="site-footer".*?</footer>', lambda _: render_footer(), after, count=1, flags=re.S)
    assert f_count == 1, f"Footer missing in {name}"

    # Cache-bust footer.css
    footer_css = f'<link rel="stylesheet" href="assets/css/footer.css?v={ASSET_VERSION}">'
    after = re.sub(r'<link rel="stylesheet" href="assets/css/footer\.css(?:\?v=[^"]*)?">', footer_css, after)

    # Cache-bust and order navigation.css
    nav_css = f'<link rel="stylesheet" href="assets/css/navigation.css?v={ASSET_VERSION}">'
    after = re.sub(r'<link rel="stylesheet" href="assets/css/navigation\.css(?:\?v=[^"]*)?">', '', after)
    after = after.replace('<link rel="stylesheet" href="assets/css/brand-theme.css">', '<link rel="stylesheet" href="assets/css/brand-theme.css">' + nav_css, 1)

    # Cache-bust and place mobile-responsive.css last in <head>
    mobile_css = f'<link rel="stylesheet" href="assets/css/mobile-responsive.css?v={ASSET_VERSION}">'
    after = re.sub(r'<link rel="stylesheet" href="assets/css/mobile-responsive\.css(?:\?v=[^"]*)?">', '', after)
    after = after.replace('</head>', mobile_css + '</head>', 1)

    # Cache-bust navigation.js
    script = f'<script defer src="assets/js/navigation.js?v={ASSET_VERSION}"></script>'
    after = re.sub(r'<script defer src="assets/js/navigation\.js(?:\?v=[^"]*)?"></script>', '', after)
    first_library = '<script defer src="https://cdn.jsdelivr.net/npm/gsap@3.13.0/dist/gsap.min.js"></script>'
    assert first_library in after, name
    after = after.replace(first_library, script + first_library, 1)

    if check:
        assert after == before, f'Navigation or footer out of sync: {name}'
    elif after != before:
        path.write_text(after, encoding='utf-8')

# 2. Industry Destinations (Grand Techno & Green Techno Farm)
for page_key, rel_dir in [('grand-techno', 'grand-techno'), ('farm', 'farm')]:
    dest_path = ROOT / rel_dir / 'index.html'
    if not dest_path.exists():
        continue
    before = dest_path.read_text(encoding='utf-8')
    header_html = render_header(page_key, base_path='../')
    after, count = re.subn(r'<header class="header">.*?</header>', lambda _: header_html, before, count=1, flags=re.S)
    assert count == 1, page_key

    # Remove legacy farm-navigation assets
    after = re.sub(r'<link rel="stylesheet" href="[^"]*farm-navigation\.css[^"]*">\s*', '', after)
    after = re.sub(r'<script defer src="[^"]*farm-navigation\.js[^"]*"></script>\s*', '', after)

    # Replace footer with unified corporate site-footer
    footer_html = render_footer(base_path='../')
    after, f_count = re.subn(r'<footer.*?</footer\s*>', lambda _: footer_html, after, count=1, flags=re.S)
    assert f_count == 1, f'{page_key} footer replacement failed'

    # Strip old links and insert versioned footer.css, navigation.css, mobile-responsive.css in order
    for css_name in ['footer.css', 'navigation.css', 'mobile-responsive.css']:
        after = re.sub(rf'<link rel="stylesheet" href="\.\./assets/css/{re.escape(css_name)}(?:\?v=[^"]*)?">', '', after)
        tag = f'<link rel="stylesheet" href="../assets/css/{css_name}?v={ASSET_VERSION}">'
        after = after.replace('</head>', tag + '</head>', 1)

    script = f'<script defer src="../assets/js/navigation.js?v={ASSET_VERSION}"></script>'
    after = re.sub(r'<script defer src="\.\./assets/js/navigation\.js(?:\?v=[^"]*)?"></script>', '', after)
    after = after.replace('</body>', script + '</body>', 1)

    if check:
        assert after == before, f'Navigation or footer out of sync: {page_key}'
    elif after != before:
        dest_path.write_text(after, encoding='utf-8')

print(('Checked' if check else 'Synced') + ' shared navigation, footer, and responsive assets across all 10 pages.')
