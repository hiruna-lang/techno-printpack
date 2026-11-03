from playwright.sync_api import sync_playwright
with sync_playwright() as p:
 b=p.chromium.launch();page=b.new_page()
 page.goto('http://127.0.0.1:5173/',wait_until='networkidle')
 assert page.locator('.hero-pagination').count()==0
 assert page.locator('.hero-slide').count()==3
 page.wait_for_function('document.querySelector(".ref-hero-photo").dataset.slide === "1"',timeout=9000)
 assert page.locator('.hero-slide.is-active').count()==1
 page.locator('.hero-autoplay-toggle').click()
 current=page.locator('.ref-hero-photo').get_attribute('data-slide')
 page.wait_for_timeout(5200)
 assert page.locator('.ref-hero-photo').get_attribute('data-slide')==current
 page.emulate_media(reduced_motion='reduce');page.locator('.hero-autoplay-toggle').wait_for(state='hidden')
 b.close()
print('PASS: automatic photo rotation, single active image, pause control, removed numbered buttons and reduced-motion state.')
