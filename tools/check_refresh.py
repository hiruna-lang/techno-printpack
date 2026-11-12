from pathlib import Path
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
 b=p.chromium.launch()
 page=b.new_page(viewport={'width':375,'height':850},reduced_motion='reduce')
 page.goto('http://127.0.0.1:5173/',wait_until='networkidle')
 assert page.locator('#navigation a[href="gallery.html"]').count()==0
 page.set_viewport_size({'width':1440,'height':1000})
 page.goto('http://127.0.0.1:5173/products.html')
 assert page.locator('.catalogue-card').count()==10
 assert page.locator('.catalogue-card-image.is-illustration').count()==6
 assert page.locator('.catalogue-card-image.is-illustration img').evaluate_all('(imgs)=>imgs.every(i=>i.complete && i.naturalWidth>0)')
 page.goto('http://127.0.0.1:5173/capabilities.html#quality-approach')
 assert page.locator('#quality-approach').count()==1
 assert page.locator('.capability-card').count()==4
 page.locator('.capability-card summary').first.click()
 assert page.locator('.capability-card details').first.get_attribute('open') is not None
 page.locator('.capability-card summary').first.focus();page.keyboard.press('Enter')
 assert page.locator('.capability-card details').first.get_attribute('open') is None
 page.goto('http://127.0.0.1:5173/quality.html')
 assert page.locator('.quality-process-steps li').count()==5
 assert page.locator('.quality-document-grid details').count()==4
 page.locator('.quality-document-grid summary').first.focus();page.keyboard.press('Enter')
 assert page.locator('.quality-document-grid details').first.get_attribute('open') is not None
 assert page.locator('#navigation > a[href="quality.html"]').get_attribute('aria-current')=='page'
 page.goto('http://127.0.0.1:5173/about.html')
 assert page.locator('.nav-dropdown-heading a[href="about.html"]').get_attribute('aria-current')=='page'
 page.locator('#group summary').click()
 assert page.locator('#group').get_attribute('open') is not None
 assert page.locator('.about-hero-photo img').get_attribute('src').endswith('factory-111A1589-1600.webp')
 context=b.new_context(java_script_enabled=False,viewport={'width':320,'height':800})
 page=context.new_page();page.goto('http://127.0.0.1:5173/')
 assert page.locator('#navigation').is_visible()
 assert not page.evaluate('document.documentElement.scrollWidth>innerWidth')
 b.close()
print('PASS: Gallery removed; catalogue cards, capability controls, quality documents, About group section, and no-JavaScript navigation.')
