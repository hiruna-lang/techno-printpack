from playwright.sync_api import sync_playwright
from pathlib import Path
with sync_playwright() as p:
 b=p.chromium.launch()
 page=b.new_page(viewport={'width':1440,'height':1000})
 errors=[]
 page.on('pageerror',lambda e:errors.append(str(e)))
 for route in ['farm/index.html','farm/produce.html','farm/our-farm.html','farm/contact.html']:
  page.goto('http://127.0.0.1:5173/'+route)
  assert page.locator('h1').count()==1
  page.locator('img').evaluate_all('(imgs)=>imgs.forEach(i=>i.loading="eager")')
  page.wait_for_function('Array.from(document.images).every(i=>i.complete)')
  assert page.locator('img').evaluate_all('(imgs)=>imgs.every(i=>i.complete && i.naturalWidth>0)')
  assert not page.evaluate('document.documentElement.scrollWidth>innerWidth')
 page.goto('http://127.0.0.1:5173/farm/index.html')
 page.locator('img').evaluate_all('(imgs)=>imgs.forEach(i=>i.loading="eager")')
 page.wait_for_function('Array.from(document.images).every(i=>i.complete)')
 page.locator('img').evaluate_all('(imgs)=>Promise.all(imgs.map(i=>i.decode()))')
 page.screenshot(path='tools/farm-desktop.png',full_page=True)
 page.mouse.move(0,0)
 page.wait_for_function('document.querySelectorAll(".slide-dots button")[1].getAttribute("aria-pressed")==="true"',timeout=8000)
 page.wait_for_function('document.querySelectorAll(".slide-dots button")[2].getAttribute("aria-pressed")==="true"',timeout=8000)
 page.wait_for_function('document.querySelectorAll(".slide-dots button")[0].getAttribute("aria-pressed")==="true"',timeout=8000)
 assert page.locator('.hero-pause').count()==0
 page.locator('.slide-dots button').nth(1).click()
 page.locator('.hero-images img').nth(1).wait_for(state='visible')
 assert page.locator('.hero-images img').nth(1).is_visible()
 page.set_viewport_size({'width':375,'height':850})
 page.screenshot(path='tools/farm-mobile.png',full_page=True)
 assert not page.evaluate('document.documentElement.scrollWidth>innerWidth')
 page.locator('.menu-toggle').click()
 assert page.locator('#farm-nav').is_visible()
 page.keyboard.press('Escape')
 assert not page.locator('#farm-nav').is_visible()
 page.goto('http://127.0.0.1:5173/farm/contact.html?produce=mango')
 page.wait_for_function('document.querySelector("select").value === "mango"')
 page.goto('http://127.0.0.1:5173/index.html')
 page.locator('.menu-toggle').click()
 page.locator('[aria-controls="dropdown-industries"]').click()
 page.locator('#dropdown-industries a').click()
 page.wait_for_url('**/farm/index.html')
 assert not errors,errors
 print('PASS: four farm pages, images, desktop/mobile overflow, mobile navigation, slideshow, produce enquiry selection and parent dropdown integration.')
 b.close()
