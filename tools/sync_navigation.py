"""Update shared headers and navigation stylesheet order across all pages including industry destinations."""
from pathlib import Path
import re, sys
from navigation_markup import render_header

ROOT = Path(__file__).resolve().parents[1]
PAGES = ['index', 'about', 'products', 'capabilities', 'industries', 'quality', 'quotation', 'contact']
check = '--check' in sys.argv

# 1. Main company pages
for name in PAGES:
    path = ROOT / f'{name}.html'
    before = path.read_text(encoding='utf-8')
    after, count = re.subn(r'<header class="header">.*?</header>', lambda _: render_header(name), before, count=1, flags=re.S)
    assert count == 1, name
    css = '<link rel="stylesheet" href="assets/css/navigation.css">'
    assert after.count(css) == 1, name
    after = after.replace(css, '').replace('<link rel="stylesheet" href="assets/css/brand-theme.css">', '<link rel="stylesheet" href="assets/css/brand-theme.css">' + css, 1)
    script = '<script defer src="assets/js/navigation.js"></script>'
    after = after.replace(script, '')
    first_library = '<script defer src="https://cdn.jsdelivr.net/npm/gsap@3.13.0/dist/gsap.min.js"></script>'
    assert first_library in after, name
    after = after.replace(first_library, script + first_library, 1)
    if check:
        assert after == before, f'Navigation out of sync: {name}'
    elif after != before:
        path.write_text(after, encoding='utf-8')

# 2. Industry Destination: Grand Techno
grand_path = ROOT / 'grand-techno' / 'index.html'
if grand_path.exists():
    grand_before = grand_path.read_text(encoding='utf-8')
    grand_header = render_header('grand-techno', base_path='../')
    grand_after, count = re.subn(r'<header class="header">.*?</header>', lambda _: grand_header, grand_before, count=1, flags=re.S)
    if count == 1:
        # Remove legacy farm-navigation assets
        grand_after = re.sub(r'<link rel="stylesheet" href="[^"]*farm-navigation\.css[^"]*">\s*', '', grand_after)
        grand_after = re.sub(r'<script defer src="[^"]*farm-navigation\.js[^"]*"></script>\s*', '', grand_after)
        
        css = '<link rel="stylesheet" href="../assets/css/navigation.css">'
        if css in grand_after:
            grand_after = grand_after.replace(css, '')
        grand_after = grand_after.replace('</head>', css + '</head>', 1)
        script = '<script defer src="../assets/js/navigation.js"></script>'
        if script in grand_after:
            grand_after = grand_after.replace(script, '')
        grand_after = grand_after.replace('</body>', script + '</body>', 1)
        if not check and grand_after != grand_before:
            grand_path.write_text(grand_after, encoding='utf-8')

# 3. Industry Destination: Green Techno Farm
farm_path = ROOT / 'farm' / 'index.html'
if farm_path.exists():
    farm_before = farm_path.read_text(encoding='utf-8')
    farm_header = render_header('farm', base_path='../')
    farm_after, count = re.subn(r'<header class="header">.*?</header>', lambda _: farm_header, farm_before, count=1, flags=re.S)
    if count == 1:
        # Remove legacy farm-navigation assets
        farm_after = re.sub(r'<link rel="stylesheet" href="[^"]*farm-navigation\.css[^"]*">\s*', '', farm_after)
        farm_after = re.sub(r'<script defer src="[^"]*farm-navigation\.js[^"]*"></script>\s*', '', farm_after)

        css = '<link rel="stylesheet" href="../assets/css/navigation.css">'
        if css in farm_after:
            farm_after = farm_after.replace(css, '')
        farm_after = farm_after.replace('</head>', css + '</head>', 1)
        script = '<script defer src="../assets/js/navigation.js"></script>'
        if script in farm_after:
            farm_after = farm_after.replace(script, '')
        farm_after = farm_after.replace('</body>', script + '</body>', 1)
        if not check and farm_after != farm_before:
            farm_path.write_text(farm_after, encoding='utf-8')

print(('Checked' if check else 'Synced') + ' shared navigation across all pages including industry destinations.')
