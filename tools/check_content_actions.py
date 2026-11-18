"""Review purposeful content actions without sending any enquiries or rebuilding pages."""
from pathlib import Path
import json
import re
import sys
from urllib.parse import unquote,parse_qs,urlsplit
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
URL=(sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:5173').rstrip('/')
WIDTHS=[375,1440] if '--focused' in sys.argv else [320,375,430,768,1024,1440,1920]
PAGES=['index','about','products','capabilities','industries','quality','quotation','contact']
ALL=PAGES+['farm/index','grand-techno/index']
OUT=ROOT/'tmp/action-cleanup/review';OUT.mkdir(parents=True,exist_ok=True)
BASE=ROOT/'tmp/action-cleanup/before'
STYLE='<link rel="stylesheet" href="assets/css/content-actions.css">'
PROFILE=json.loads((ROOT/'assets/data/company-profile.json').read_text(encoding='utf-8'))
REMOVED={'index':'.home-enquiry','products':'.cta.section','industries':'.cta.section','quality':'.quality-cta-section','contact':'.contact-quote-banner'}
ARROWS='\u2197\u2192\u27f6\u279c'

def normal(text):return re.sub(r'\s+',' ',text).strip()
def controls(form):
    if form is None:return None
    return {'attrs':form.attrs,'controls':[(tag.name,tag.attrs,normal(tag.get_text(' ',strip=True))) for tag in form.select('input,select,textarea,button,label')],'options':[(option.attrs,normal(option.text)) for option in form.select('option')]}
def shell(text):
    return re.sub(r'(<main\b[^>]*>).*?(</main>)',r'\1__MAIN__\2',text,flags=re.S).replace(STYLE,'')

for name in ALL:
    before=(BASE/f'{name}.html').read_text(encoding='utf-8')
    after=(ROOT/f'{name}.html').read_text(encoding='utf-8')
    assert shell(before)==shell(after),f'Header, footer, metadata or scripts changed: {name}'
    if name=='grand-techno/index':assert before==after,'Grand Techno changed'
    old=BeautifulSoup(before,'html.parser');new=BeautifulSoup(after,'html.parser')
    assert [controls(f) for f in old.select('main form')]==[controls(f) for f in new.select('main form')],f'Form fields/options changed: {name}'
    for section in old.select(REMOVED.get(name,'__no_removed_section__')):section.decompose()
    for selector in ['main h1','main h2','main h3','main p']:
        assert [normal(x.get_text(' ',strip=True)) for x in old.select(selector)]==[normal(x.get_text(' ',strip=True)) for x in new.select(selector)],(name,selector,'Company content changed')
    assert [str(x) for x in old.select('main img')]==[str(x) for x in new.select('main img')],f'Company image attributes changed: {name}'
    for image in new.select('img[src]'):
        for source in [image['src']]+[part.strip().rsplit(' ',1)[0] for part in image.get('srcset','').split(',') if part.strip()]:
            if urlsplit(source).scheme or source.startswith('data:'):continue
            assert ((ROOT/f'{name}.html').parent/unquote(urlsplit(source).path)).is_file(),(name,source)
    if name!='grand-techno/index':
        for link in new.select('main a[href]'):
            if urlsplit(link['href']).scheme in ['http','https']:continue
            assert not any(arrow in link.get_text() for arrow in ARROWS),(name,link.get('href'),'Decorative action arrow')

product_soup=BeautifulSoup((ROOT/'products.html').read_text(encoding='utf-8'),'html.parser')
old_products=BeautifulSoup((BASE/'products.html').read_text(encoding='utf-8'),'html.parser')
assert [x.get_text(' ',strip=True) for x in product_soup.select('.catalogue-card h3')]==[p['name'] for p in PROFILE['products']]
assert [normal(x.get_text(' ',strip=True)) for x in product_soup.select('.profile-structure-list > li')]==PROFILE['structures']
assert not product_soup.select('.profile-structure-list a,.profile-structure-list button,.profile-structure-list [tabindex]')
assert [x['href'] for x in product_soup.select('.catalogue-card > a')]==[x['href'] for x in old_products.select('.catalogue-card > a')]
assert len(product_soup.select('.catalogue-card'))==10 and not product_soup.select('.catalogue-arrow,.cta.section')
sector_soup=BeautifulSoup((ROOT/'industries.html').read_text(encoding='utf-8'),'html.parser')
assert [x.get_text(' ',strip=True) for x in sector_soup.select('.sector-grid article h3')]==PROFILE['industries']
assert not sector_soup.select('.sector-grid article a[href="quotation.html"],.cta.section')
capability=BeautifulSoup((ROOT/'capabilities.html').read_text(encoding='utf-8'),'html.parser')
assert len(capability.select('.capability-strengths article.capability-strength'))==4
assert not capability.select('.capability-strengths a,.capability-card-detail a[href*="quotation.html"]')
assert len(capability.select('.capability-card details'))==4 and len(capability.select('.capability-cta a'))==1
quality=BeautifulSoup((ROOT/'quality.html').read_text(encoding='utf-8'),'html.parser')
assert len(quality.select('.quality-themes article.quality-theme'))==4
assert len(quality.select('.quality-process-steps .quality-step'))==5
assert not quality.select('.quality-themes a,.quality-process-steps a,.quality-process-steps li > b,.quality-document-grid a,.quality-cta-section')
assert len(quality.select('.quality-document-grid details'))==4
assert len(quality.select('a.quality-document-link[href="contact.html"]'))==1
home=BeautifulSoup((ROOT/'index.html').read_text(encoding='utf-8'),'html.parser')
assert not home.select('.corp-about-links .corp-link,.corp-solutions .corp-link,.corp-process-layout > div > .corp-link,.home-enquiry,a.corp-solution-photo')
assert len(home.select('.corp-solutions h3 a'))==3 and len(home.select('.corp-solutions a'))==3
assert len(home.select('.corp-sector-list a'))==8 and len(home.select('.banner-actions a'))==2 and len(home.select('.packaging-highlights a'))==4
farm=BeautifulSoup((ROOT/'farm/index.html').read_text(encoding='utf-8'),'html.parser')
assert len(farm.select('[data-produce]'))==4
print('PASS: ten products/structures, eight sectors, useful enquiry destinations, informational steps, disclosures and source facts preserved.',flush=True)

with sync_playwright() as p:
    browser=p.chromium.launch()
    context=browser.new_context(reduced_motion='reduce',permissions=['clipboard-read','clipboard-write'])
    page=context.new_page();errors=[];missing=[]
    page.on('pageerror',lambda error:errors.append(str(error)))
    page.on('response',lambda response:missing.append(response.url) if response.url.startswith(URL) and response.status>=400 else None)
    def visit(name):
        page.goto(f'{URL}/{name}.html',wait_until='domcontentloaded')
        page.evaluate('''async()=>{const images=[...document.querySelectorAll('main img[src]')];images.forEach(i=>i.loading='eager');await Promise.all(images.map(i=>i.decode().catch(()=>{})));await document.fonts.ready;}''')
        assert page.locator('main img[src]').evaluate_all('(images)=>images.every(i=>i.complete&&i.naturalWidth>0)'),name

    for name in PAGES:
        for width in WIDTHS:
            page.set_viewport_size({'width':width,'height':1000});visit(name)
            assert not page.evaluate('document.documentElement.scrollWidth>innerWidth'),(name,width,'overflow')
            assert page.locator('main :is(.corp-link,.text-link)').evaluate_all('''els=>els.every(e=>{
                if(e.closest('[hidden]'))return true;
                const detail=e.closest('details:not([open])');
                if(detail&&!e.closest('summary'))return true;
                return getComputedStyle(e).display!=='none'&&e.getBoundingClientRect().height>0;
            })'''),(name,width,'Retained action hidden')
            if name=='products':
                assert page.locator('.catalogue-card').count()==10
                assert page.locator('.profile-structure-list > li').count()==10
                assert page.locator('.profile-structure-list').evaluate('(e)=>getComputedStyle(e).listStyleType')=='none'
                if width in [375,1440]:page.locator('.profile-structure-list').screenshot(path=str(OUT/f'product-structures-{width}.png'))
            if name=='industries':assert page.locator('.sector-grid article').count()==8
            if name=='capabilities' and width in [375,1440]:page.locator('.capability-strengths').screenshot(path=str(OUT/f'capability-strengths-{width}.png'))
            if name=='quality' and width in [375,1440]:page.locator('.quality-process-steps').screenshot(path=str(OUT/f'quality-steps-{width}.png'))
            if name=='contact':
                assert page.locator('.contact-quote-banner').count()==0
                dims=page.locator('.contact-lower-layout').evaluate('(e)=>({parent:e.getBoundingClientRect().width,map:e.querySelector(".contact-location").getBoundingClientRect().width})')
                assert abs(dims['parent']-dims['map'])<1,(width,dims)
                if width in [375,1440]:page.locator('.contact-location').screenshot(path=str(OUT/f'contact-location-{width}.png'))
        print(f'PASS: {name}, {len(WIDTHS)} widths, intact content and no overflow/missing company images.',flush=True)

    page.set_viewport_size({'width':1440,'height':1000});visit('products')
    filters=page.locator('[data-filter]').evaluate_all('(els)=>els.map(e=>({value:e.dataset.filter,text:e.textContent}))')
    for item in filters:
        page.locator(f'[data-filter="{item["value"]}"]').click()
        assert page.locator('.product-card:visible').count()>0,item
        assert page.locator(f'[data-filter="{item["value"]}"]').get_attribute('aria-pressed')=='true'
    first=page.locator('.product-card:visible a').first
    expected=parse_qs(urlsplit(first.get_attribute('href')).query)['type'][0]
    first.click();page.wait_for_url('**/quotation.html?type=*')
    assert page.locator('#type').input_value()==expected

    # Validation and prepared drafts are local; never click email or WhatsApp send controls.
    page.locator('#quote-form button[type="submit"]').click()
    assert 'highlighted' in page.locator('#form-status').inner_text()
    for name,value in {'name':'Website QA','company':'Preview test','phone':'+94 777 123 456','email':'qa@example.com','quantity':'100','dimensions':'100 x 80 x 60 mm'}.items():page.locator(f'#quote-form [name="{name}"]').fill(value)
    page.locator('#quote-form button[type="submit"]').click()
    assert page.locator('#enquiry-preview').is_visible()
    assert 'Nothing has been sent' in page.locator('#form-status').inner_text()
    assert expected in page.locator('#message-preview').inner_text()
    assert page.locator('#email-enquiry').get_attribute('href').startswith('mailto:info@technoind.biz?')
    assert page.locator('#send-whatsapp').is_disabled()
    page.locator('#copy-enquiry').click()
    page.wait_for_function('document.querySelector("#form-status").textContent.toLowerCase().includes("copied")')
    page.locator('#quote-form [name="dimensions"]').fill('120 x 80 x 60 mm')
    assert page.locator('#enquiry-preview').is_hidden()

    visit('contact');page.locator('#contact-form button[type="submit"]').click()
    assert 'highlighted' in page.locator('#contact-status').inner_text()
    for name,value in {'name':'Website QA','company':'Preview test','email':'qa@example.com','phone':'+94 777 123 456','message':'Local preview test; do not send.'}.items():page.locator(f'#contact-form [name="{name}"]').fill(value)
    page.locator('#contact-form button[type="submit"]').click()
    assert page.locator('#contact-preview').is_visible()
    assert 'Nothing has been sent' in page.locator('#contact-status').inner_text()
    assert page.locator('#contact-email-draft').get_attribute('href').startswith('mailto:info@technoind.biz?')
    assert page.locator('#contact-whatsapp').is_disabled()
    page.locator('#contact-copy').click()
    page.wait_for_function('document.querySelector("#contact-status").textContent.toLowerCase().includes("copied")')
    page.locator('#contact-form [name="message"]').fill('Updated local preview test.')
    assert page.locator('#contact-preview').is_hidden()

    for name,selector in [('capabilities','.capability-card details'),('quality','.quality-document-grid details')]:
        visit(name)
        for details in page.locator(selector).all():
            summary=details.locator('summary');summary.click();assert details.get_attribute('open') is not None
            assert details.locator('p').first.is_visible();summary.click();assert details.get_attribute('open') is None

    for width in [375,1440]:
        page.set_viewport_size({'width':width,'height':1000});visit('farm/index')
        assert not page.evaluate('document.documentElement.scrollWidth>innerWidth'),('farm',width)
        for item in page.locator('[data-produce]').all():
            expected=item.get_attribute('data-produce');item.click()
            assert page.locator('#enquiry-form [name="produce"]').input_value()==expected
    print('PASS: product filtering/preselection, local validation/prepare/copy drafts, native disclosures and Farm produce preselection; no enquiry sent.',flush=True)

    # Informational lists and native disclosures remain usable without JavaScript.
    nojs=browser.new_context(java_script_enabled=False,viewport={'width':375,'height':1000})
    fallback=nojs.new_page()
    fallback.goto(URL+'/products.html',wait_until='domcontentloaded')
    assert fallback.locator('.catalogue-card').count()==10 and fallback.locator('.profile-structure-list li').count()==10
    fallback.goto(URL+'/capabilities.html',wait_until='domcontentloaded')
    detail=fallback.locator('.capability-card details').first;detail.locator('summary').click()
    assert detail.get_attribute('open') is not None and detail.locator('p').first.is_visible()
    nojs.close()
    assert not errors,errors
    assert not missing,missing
    browser.close()
print('PASS: static no-JS content, preserved company assets, no JavaScript exceptions or missing local responses.',flush=True)
