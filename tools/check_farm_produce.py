from playwright.sync_api import sync_playwright
with sync_playwright() as p:
 b=p.chromium.launch();page=b.new_page(viewport={'width':1440,'height':1000});page.goto('http://localhost:8000/farm/produce.html');page.locator('img').evaluate_all('(imgs)=>imgs.forEach(i=>i.loading="eager")');page.locator('img').evaluate_all('(imgs)=>Promise.all(imgs.map(i=>i.decode()))');assert page.locator('.fruit-detail').count()==4;assert page.locator('.produce-benefits>div').count()==4;assert page.locator('.hero-promises>div').count()==3;assert page.locator('.cta').count()==0
 for width in [1440,768,375]:
  page.set_viewport_size({'width':width,'height':1000});assert not page.evaluate('document.documentElement.scrollWidth>innerWidth');page.screenshot(path=f'tools/produce-farm-{width}.png',full_page=True)
 page.locator('#mango .button').click();page.wait_for_url('**/contact.html?produce=mango');assert page.locator('select').input_value()=='mango';print('PASS: produce layout at desktop, tablet and mobile sizes, four fruit cards, hero promises, and enquiry navigation.');b.close()
