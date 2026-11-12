from playwright.sync_api import sync_playwright
with sync_playwright() as p:
 b=p.chromium.launch();page=b.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
 for width in [1440,1024,768,375]:
  page.set_viewport_size({'width':width,'height':950});page.goto('http://127.0.0.1:5173/grand-techno/index.html');page.locator('img').evaluate_all('(imgs)=>imgs.forEach(i=>i.loading="eager")');page.wait_for_function('Array.from(document.images).filter(i=>i.getAttribute("src")).every(i=>i.complete && i.naturalWidth>0)');page.wait_for_timeout(800)
  assert not page.evaluate('document.documentElement.scrollWidth>innerWidth'),width
  assert page.locator('main a.button').count()==0
  assert page.locator('.gallery-item:visible').count()==10
  if width == 1440:
   page.mouse.move(0,0)
   page.wait_for_function("document.querySelectorAll('.hero-slide')[1].classList.contains('is-active')", timeout=7000)
   assert page.locator('.hero-slideshow-toggle').count() == 0
   page.locator('.hero-image').hover()
   page.wait_for_function("document.querySelectorAll('.hero-slide')[2].classList.contains('is-active')", timeout=7000)
  page.screenshot(path=f'tools/grand-{width}.png',full_page=True)
  page.locator('.gallery-item').first.click();assert page.locator('dialog').is_visible();page.keyboard.press('Escape');assert not page.locator('dialog').is_visible()
  if width<=900:page.locator('.menu-toggle').click()
  page.locator('[aria-controls="dropdown-industries"]').focus();page.keyboard.press('Enter');assert page.locator('#dropdown-industries a[aria-current="page"]').inner_text()=='Grand Techno'
  page.locator('#dropdown-industries a',has_text='Techno Farm').click();page.wait_for_url('**/farm/index.html')
 assert not errors,errors
 print('PASS: desktop/tablet/mobile, all photos loaded, no overflow, no content CTA buttons, corporate dropdown navigation to farm, gallery and no JavaScript errors.')
 page.emulate_media(reduced_motion='reduce')
 page.goto('http://127.0.0.1:5173/grand-techno/index.html')
 page.wait_for_timeout(5500)
 assert 'is-active' in page.locator('.hero-slide').first.get_attribute('class')
 print('PASS: automatic hero crossfade without controls or hover interruption, and reduced-motion behavior.')
 b.close()
