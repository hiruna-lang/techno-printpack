from pathlib import Path
from urllib.parse import urlparse,unquote
from html.parser import HTMLParser
import json
from playwright.sync_api import sync_playwright
root=Path(__file__).resolve().parents[1]
# Update the selected farm photo after visual asset inspection.
p=root/'tools/build_site.py';s=p.read_text(encoding='utf-8');s=s.replace('farm-07f7e1dc-9e69-475e-abd7-b1261aec65c1','farm-IMG_3243');p.write_text(s,encoding='utf-8')
exec(compile(s,str(p),'exec'),{'__file__':str(p)})
class Audit(HTMLParser):
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  for attr in ['href','src']:
   v=a.get(attr,'');u=urlparse(v)
   if v and not u.scheme and not v.startswith('#'):
    assert (root/unquote(u.path)).exists(),v
for page in root.glob('*.html'):Audit().feed(page.read_text(encoding='utf-8'))
results=[];errors=[]
with sync_playwright() as pw:
 browser=pw.chromium.launch()
 page=browser.new_page()
 page.on('pageerror',lambda e: errors.append(str(e)))
 for width in [320,375,430,768,1024,1440,1920]:
  page.set_viewport_size({'width':width,'height':950})
  for file in root.glob('*.html'):
   page.goto('http://127.0.0.1:5173/'+file.name,wait_until='domcontentloaded')
   page.wait_for_timeout(200)
   overflow=page.evaluate('document.documentElement.scrollWidth > innerWidth')
   assert not overflow,f'Overflow {file.name} {width}'
   assert page.locator('h1').count()==1
   results.append(f'{file.name} @ {width}: pass')
 page.set_viewport_size({'width':1440,'height':1000})
 page.goto('http://127.0.0.1:5173/',wait_until='networkidle');page.wait_for_timeout(1800)
 for y in range(0,page.evaluate('document.body.scrollHeight'),650):
  page.evaluate('(y)=>window.scrollTo({top:y,behavior:"instant"})',y);page.wait_for_timeout(220)
 page.wait_for_timeout(1000);page.evaluate('window.scrollTo({top:0,behavior:"instant"})');page.wait_for_timeout(300)
 assert page.locator('img').evaluate_all('(imgs)=>imgs.filter(i=>!i.complete || !i.naturalWidth).length')==0
 page.screenshot(path=str(root/'tools/home-desktop.png'),full_page=True)
 page.set_viewport_size({'width':375,'height':850});page.reload(wait_until='networkidle');page.wait_for_timeout(1000)
 for y in range(0,page.evaluate('document.body.scrollHeight'),650):
  page.evaluate('(y)=>window.scrollTo({top:y,behavior:"instant"})',y);page.wait_for_timeout(200)
 page.wait_for_timeout(800);page.evaluate('window.scrollTo({top:0,behavior:"instant"})');page.wait_for_timeout(300)
 page.screenshot(path=str(root/'tools/home-mobile.png'),full_page=True)
 page.locator('.menu-toggle').click();assert page.locator('#navigation').is_visible();page.keyboard.press('Escape');assert not page.locator('#navigation').is_visible()
 assert page.locator('.hero-pagination').count()==0
 assert page.locator('.nav-dropdown-heading a[href="industries.html"]').count()==1
 assert page.locator('#navigation > a[href="quality.html"]').count()==1
 page.goto('http://127.0.0.1:5173/products.html');page.locator('[data-filter=pvc]').click();assert page.locator('.product-card:visible').count()==1
 page.goto('http://127.0.0.1:5173/quotation.html');page.locator('button[type=submit]').click();assert page.locator('[aria-invalid=true]').count()>0
 for n,v in {'name':'Website QA','email':'qa@example.com','phone':'+94 11 234 5678','quantity':'500','dimensions':'20 × 30 × 40 cm'}.items():page.locator('#'+n).fill(v)
 page.locator('#type').select_option(label='Regular Slotted Cartons (RSC)');page.locator('button[type=submit]').click();assert page.locator('#enquiry-preview').is_visible();assert page.locator('#send-whatsapp').is_disabled();assert 'Nothing has been sent' in page.locator('#form-status').inner_text()
 page.evaluate("window.TECHNO_CONFIG={whatsappNumber:'94700000000',enquiryEmail:'info@technoind.biz'}")
 page.locator('button[type=submit]').click();assert page.locator('#send-whatsapp').is_enabled()
 page.locator('#name').fill('Changed');assert not page.locator('#enquiry-preview').is_visible()
 # Check content remains usable without scripts or CDN dependencies.
 context=browser.new_context(java_script_enabled=False);nojs=context.new_page();nojs.goto('http://127.0.0.1:5173/');assert nojs.locator('h1').is_visible();assert nojs.locator('.corp-solutions article').count()==3
 browser.close()
assert not errors,errors
(root/'tools/qa-results.json').write_text(json.dumps({'layout_checks':results,'interaction_checks':'Passed menu, products, quote validation and configurable WhatsApp availability, no-JS content','javascript_errors':errors},indent=2))
print(f'PASS: {len(results)} page/viewport checks, local links and assets, interactive controls, no-JS content; no JavaScript exceptions.')
