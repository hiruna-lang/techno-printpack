from playwright.sync_api import sync_playwright
with sync_playwright() as p:
 browser=p.chromium.launch()
 page=browser.new_page()
 page.goto('http://localhost:8000/farm/our-farm.html')
 page.locator('img[src]').evaluate_all('(images)=>Promise.all(images.map(image=>{image.loading="eager";return image.decode()}))')
 for width in [1440,768,375]:
  page.set_viewport_size({'width':width,'height':1000})
  assert not page.evaluate('document.documentElement.scrollWidth>innerWidth'),width
  page.screenshot(path=f'tools/farm-story-{width}.png',full_page=True)
 for category,count in [('farm',1),('cultivation',1),('produce',4),('activities',1),('all',7)]:
  page.locator(f'[data-gallery-filter="{category}"]').click()
  assert page.locator('.story-photo:visible').count()==count
 page.locator('.story-photo').first.click()
 assert page.locator('dialog').is_visible()
 page.keyboard.press('Escape')
 assert not page.locator('dialog').is_visible()
 page.locator('.farming-approach summary').click()
 assert page.locator('.farming-approach').get_attribute('open') is not None
 page.locator('.story-visit a').click()
 page.wait_for_url('**/farm/contact.html')
 browser.close()
 print('PASS: images load; no overflow at desktop, tablet or mobile; all filters, photo viewer, farming approach and contact link work.')

