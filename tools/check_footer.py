"""Verify shared footer links, preservation, responsive layout and keyboard behaviour."""
from pathlib import Path
import hashlib
import json
import re
import sys
from urllib.parse import urlsplit, unquote
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
PAGES = ['index', 'about', 'products', 'capabilities', 'industries', 'quality', 'quotation', 'contact']
URL = (sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:5173').rstrip('/')
template = (ROOT/'tools/templates/footer.html').read_text(encoding='utf-8').strip()

for name in PAGES:
    html = (ROOT/f'{name}.html').read_text(encoding='utf-8')
    assert html.count(template)==1, name
    assert html.count('assets/css/footer.css')==1, name
    assert html.count('id="year"')==1, name
    assert 'Website developed by <span>Nexora Digital Solutions</span>' in template
    assert 'Techno Industries. All rights reserved.</p>' in template
    for href in re.findall(r'href="([^"]+)"', template):
        parsed = urlsplit(href)
        if parsed.scheme:
            continue
        destination = ROOT/unquote(parsed.path)
        assert destination.is_file(), (name,href)
        if parsed.fragment:
            target_html = destination.read_text(encoding='utf-8')
            # Product category hashes are handled by the existing catalogue JS.
            assert (f'id="{parsed.fragment}"' in target_html or
                    (parsed.path=='products.html' and f'data-filter="{parsed.fragment}"' in target_html)), href
baseline = ROOT/'tmp/footer-page-baseline.json'
if baseline.exists():
    for name,digest in json.loads(baseline.read_text()).items():
        path = ROOT/name
        if name in ['farm/index.html','grand-techno/index.html']:
            content = path.read_bytes()
        else:
            content = re.sub(r'<footer\b[^>]*>.*?</footer>', '',path.read_text(encoding='utf-8'),flags=re.S)
            content = content.replace('<link rel="stylesheet" href="assets/css/footer.css">','').rstrip().encode()
        assert hashlib.sha256(content).hexdigest()==digest, f'Unrelated content changed: {name}'
print('PASS: identical footer on eight pages; internal links and fragment targets exist; unrelated content and independently branded sites preserved.')

with sync_playwright() as p:
    browser=p.chromium.launch()
    page=browser.new_page(reduced_motion='reduce')
    errors=[]
    page.on('pageerror',lambda error:errors.append(str(error)))
    for name in PAGES:
        for width in [320,375,430,768,1024,1440,1920]:
            page.set_viewport_size({'width':width,'height':1000})
            page.goto(f'{URL}/{name}.html',wait_until='domcontentloaded')
            footer=page.locator('.site-footer')
            footer.scroll_into_view_if_needed()
            footer.locator('img').evaluate('(i)=>i.decode()')
            assert not page.evaluate('document.documentElement.scrollWidth>innerWidth'), (name,width)
            assert footer.evaluate('(e)=>getComputedStyle(e).backgroundColor')=='rgb(15, 42, 67)',(name,width)
            assert footer.locator('nav').evaluate_all('(items)=>items.every(n=>getComputedStyle(n).display!=="none"&&getComputedStyle(n).position==="static")'),(name,width)
            assert footer.locator('a,button').evaluate_all('''(items)=>items.every(e=>{
                const r=e.getBoundingClientRect();return r.width>0&&r.height>0&&r.left>=-1&&r.right<=innerWidth+1;
            })'''),(name,width)
            assert footer.locator('.sf-bottom a, .sf-bottom button, .sf-bottom svg, .sf-copyright br').count()==0
            assert footer.locator('.sf-credit').inner_text()=='Website developed by Nexora Digital Solutions'
            if width>=1024:
                assert footer.bounding_box()['height']<410,(name,width,footer.bounding_box())
            if width<=600:
                assert footer.locator('a:not(.sf-logo),button').evaluate_all('(items)=>items.every(e=>e.getBoundingClientRect().height>=44)'),(name,width)
        page.locator('.sf-quote').focus()
        assert page.locator('.sf-quote').evaluate('(e)=>getComputedStyle(e).outlineStyle')=='solid'
        assert page.locator('#year').inner_text()==page.evaluate('String(new Date().getFullYear())')
    nojs=browser.new_context(java_script_enabled=False,viewport={'width':320,'height':900})
    basic=nojs.new_page();basic.goto(f'{URL}/contact.html',wait_until='domcontentloaded')
    assert basic.locator('.site-footer nav').evaluate_all('(items)=>items.every(n=>getComputedStyle(n).display!=="none")')
    for category in ['corrugated','printed','custom']:
        page.goto(f'{URL}/index.html',wait_until='domcontentloaded')
        page.locator(f'.site-footer a[href="products.html#{category}"]').click()
        page.wait_for_url(f'**/products.html#{category}')
        page.locator(f'[data-filter="{category}"][aria-pressed="true"]').wait_for()
        assert page.locator('.product-card:not([hidden])').count()>0, category
    for pseudo in ['::before','::after']:
        assert page.locator('.site-footer').evaluate('(e,p)=>getComputedStyle(e,p).pointerEvents',pseudo)=='none'
    assert not errors, errors
    browser.close()
print('PASS: 56 responsive page/width combinations, compact desktop height, updated credit/copyright, removed lower controls, keyboard focus, no-JS links and no JavaScript exceptions.')
