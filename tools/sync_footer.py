"""Update only the shared footer and its stylesheet; preserve direct page edits."""
from pathlib import Path
import argparse
import re

ROOT = Path(__file__).resolve().parents[1]
PAGES = ['index', 'about', 'products', 'capabilities', 'industries', 'quality', 'quotation', 'contact']
STYLESHEET = '<link rel="stylesheet" href="assets/css/footer.css">'

def sync(check=False):
    footer = (ROOT / 'tools/templates/footer.html').read_text(encoding='utf-8').strip()
    differences = []
    for name in PAGES:
        path = ROOT / f'{name}.html'
        original = path.read_text(encoding='utf-8')
        updated, count = re.subn(r'<footer\b[^>]*>.*?</footer>', lambda _: footer, original, flags=re.S)
        if count != 1:
            raise ValueError(f'{path.name}: expected one footer, found {count}')
        if STYLESHEET not in updated:
            updated = updated.replace('</head>', STYLESHEET + '</head>', 1)
        if updated != original:
            differences.append(path.name)
            if not check:
                path.write_text(updated, encoding='utf-8')
    if check and differences:
        raise SystemExit('Footer differs from template: ' + ', '.join(differences))
    print(('Checked' if check else 'Updated') + f' shared footer across {len(PAGES)} pages.')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    sync(parser.parse_args().check)
