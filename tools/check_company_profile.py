from pathlib import Path
import json
from urllib.parse import urlparse,unquote,parse_qs
from html.parser import HTMLParser
from playwright.sync_api import sync_playwright
root=Path(__file__).resolve().parents[1]
data=json.loads((root/'assets/data/company-profile.json').read_text(encoding='utf-8'))
class Links(HTMLParser):
 def __init__(self):super().__init__();self.links=[]
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  for key in ['src','href']:
   value=a.get(key,'');parsed=urlparse(value)
   if value and not parsed.scheme and parsed.path:
    assert (root/unquote(parsed.path)).exists(),value
  if tag=='a' and 'href' in a:self.links.append(a['href'])
for p in root.glob('*.html'):
 s=p.read_text(encoding='utf-8');Links().feed(s)
 assert 'Techno Printpack' not in s,p.name
 assert 'Techno Industries' in s,p.name
assert not (root/'gallery.html').exists()
with sync_playwright() as p:
 b=p.chromium.launch();page=b.new_page(viewport={'width':1440,'height':1000},reduced_motion='reduce')
 errors=[];page.on('pageerror',lambda error:errors.append(str(error)))
 page.goto('http://127.0.0.1:5173/products.html')
 assert page.locator('.catalogue-card h3').all_text_contents()==[x['name'] for x in data['products']]
 assert page.locator('.profile-tag-grid>a').count()==10
 for cat,count in [('specialty',3),('corrugated',4),('printed',1),('food',1),('custom',1),('pvc',1)]:
  page.locator(f'[data-filter={cat}]').click();assert page.locator('.product-card:visible').count()==count
 page.locator('[data-filter=all]').click()
 catalogue_links=page.locator('.catalogue-card>a').evaluate_all('(items)=>items.map(i=>i.getAttribute("href"))')
 for link in catalogue_links:
  name=parse_qs(urlparse(link).query)['type'][0]
  page.goto('http://127.0.0.1:5173/'+link)
  assert page.locator('#type').input_value()==name,name
 page.locator('#name').fill('Content QA');page.locator('#email').fill('qa@example.com');page.locator('#phone').fill('+94 11 234 5678');page.locator('#quantity').fill('250')
 page.locator('#flute').select_option(label='F Flute');page.locator('#board').select_option(label='Double Wall (5-Ply)');page.locator('#finish').select_option(label='UV Matte Lamination')
 page.locator('#quote-form button[type=submit]').click()
 preview=page.locator('#message-preview').inner_text()
 assert all(x in preview for x in ['Techno Industries','F Flute','Double Wall (5-Ply)','UV Matte Lamination'])
 assert 'Nothing has been sent' in page.locator('#form-status').inner_text()
 page.goto('http://127.0.0.1:5173/industries.html');assert page.locator('.sector-grid h3').all_text_contents()==data['industries']
 page.goto('http://127.0.0.1:5173/capabilities.html');text=page.locator('main').inner_text()
 for required in ['F Flute','Offset','OP varnish','UV lamination','UV Matte Lamination','Moisture-Resistant Boards']:assert required.lower() in text.lower(),required
 page.goto('http://127.0.0.1:5173/about.html');assert data['vision'] in page.locator('main').inner_text()
 page.goto('http://127.0.0.1:5173/quality.html');assert 'ISO 9001:2015' in page.locator('main').inner_text()
 page.goto('http://127.0.0.1:5173/contact.html')
 for email in data['contact']['emails']:assert page.locator('.contact-information a[href="mailto:'+email+'"]').count()==1
 assert page.locator('#contact-whatsapp').is_disabled()
 assert page.locator('#dropdown-industries a[href="farm/index.html"]').count()==1
 b.close();assert not errors,errors
print('PASS: all 10 products, 8 industries, 10 structures, specification options, enquiry preselection and preference encoding, vision, contacts, certification statements, local assets and preserved Farm navigation.')
