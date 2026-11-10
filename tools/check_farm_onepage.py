from pathlib import Path
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
 b=p.chromium.launch()
 page=b.new_page()
 errors=[]
 page.on('pageerror',lambda e:errors.append(str(e)))
 page.goto(Path('farm/index.html').resolve().as_uri())
 for width in [1440,768,375]:
  page.set_viewport_size({'width':width,'height':950})
  page.locator('img').evaluate_all('(xs)=>xs.forEach(x=>x.loading="eager")')
  page.wait_for_function('Array.from(document.images).every(x=>x.complete)')
  assert page.locator('img[src]').evaluate_all('(xs)=>xs.every(x=>x.naturalWidth>0)')
  assert not page.evaluate('document.documentElement.scrollWidth>innerWidth'),width
  page.locator('img[src]').evaluate_all('(xs)=>Promise.all(xs.map(x=>x.decode()))')
  assert page.locator('h1').count()==1
  page.screenshot(path=f'tools/farm-onepage-{width}.png',full_page=True)
 assert page.locator('header').count()==0
 assert page.locator('img[alt="Techno Industries"]').count()==0
 page.locator('[data-produce="banana"]').click()
 assert page.locator('select').input_value()=='banana'
 page.locator('.gallery-photo').first.click()
 assert page.locator('dialog').is_visible()
 page.keyboard.press('Escape')
 assert not page.locator('dialog').is_visible()
 assert not errors,errors
 print('PASS: images, three viewport sizes, anchors, header removal, text encoding, produce selection, gallery, JavaScript errors')
 b.close()
