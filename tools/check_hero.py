"""Verify the automatic image-only hero (run a local static server on port 5173)."""
import sys
from playwright.sync_api import sync_playwright
url=(sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:5173').rstrip('/')+'/index.html'
with sync_playwright() as p:
 browser=p.chromium.launch()
 errors=[]
 page=browser.new_page(reduced_motion='reduce')
 page.on('pageerror',lambda error:errors.append(str(error)))
 for width in [320,375,430,768,1024,1440,1920]:
  page.set_viewport_size({'width':width,'height':1000});page.goto(url)
  assert not page.evaluate('document.documentElement.scrollWidth>innerWidth'),width
  assert page.locator('.banner-product').count()==6
  page.locator('.banner-product.is-active').evaluate('(i)=>i.decode()')
  assert page.locator('.packaging-banner button, .hero-pagination, [data-hero-photo]').count()==0
  assert page.locator('.banner-product').evaluate_all('(imgs)=>imgs.every(i=>getComputedStyle(i).objectFit==="contain")')
  dimensions=page.locator('.banner-product').evaluate_all('(imgs)=>imgs.map(i=>[i.offsetLeft,i.offsetTop,i.offsetWidth,i.offsetHeight].join(","))')
  assert len(set(dimensions))==1,(width,dimensions)
 print('PASS: seven responsive widths, contain, identical image dimensions and no carousel controls.')
 page.set_viewport_size({'width':1440,'height':1000});page.emulate_media(reduced_motion='no-preference');page.goto(url)
 page.evaluate('''()=>{
  window.carouselEvents=[];
  new MutationObserver(()=>{
   const items=[...document.querySelectorAll('.banner-product')];
   const index=items.findIndex(i=>i.classList.contains('is-active'));
   if(window.carouselEvents.at(-1)?.index!==index)window.carouselEvents.push({index,time:performance.now()});
  }).observe(document.querySelector('.banner-product-stage'),{subtree:true,attributes:true,attributeFilter:['class']});
 }''')
 page.wait_for_timeout(1200)
 def stable_content():
  return page.locator('.banner-copy').evaluate('(e)=>({html:e.innerHTML,rect:[e.offsetLeft,e.offsetTop,e.offsetWidth,e.offsetHeight]})')
 fixed=stable_content()
 assert page.locator('.banner-product').first.evaluate('(e)=>getComputedStyle(e).transitionDuration')=='1.2s, 5s'
 page.wait_for_function('carouselEvents.length>=1',timeout=8000)
 page.wait_for_timeout(550)
 opacities=page.locator('.banner-product').evaluate_all('(imgs)=>imgs.map(i=>Number(getComputedStyle(i).opacity))')
 assert sum(0.01<opacity<0.99 for opacity in opacities)==2,opacities
 page.wait_for_function('carouselEvents.length>=6',timeout=30000)
 events=page.evaluate('carouselEvents.slice(0,6)')
 assert [event['index'] for event in events]==[1,2,3,4,5,0],events
 gaps=[events[i]['time']-events[i-1]['time'] for i in range(1,6)]
 assert all(abs(gap-5000)<200 for gap in gaps),gaps
 assert stable_content()==fixed
 print('PASS: all six images loop in order, 5-second cadence, 1.2-second overlapping fades, fixed hero copy/CTA layout.')
 # Simulate a visibility change, including freezing the current CSS fade and zoom.
 page.evaluate('''()=>{window.testHidden=true;Object.defineProperty(document,'hidden',{configurable:true,get:()=>window.testHidden});document.dispatchEvent(new Event('visibilitychange'));}''')
 page.wait_for_timeout(100)
 frozen=page.locator('.banner-product').evaluate_all('(imgs)=>imgs.map(i=>[i.className,getComputedStyle(i).opacity,getComputedStyle(i).transform])')
 page.wait_for_timeout(5500)
 assert page.locator('.banner-product').evaluate_all('(imgs)=>imgs.map(i=>[i.className,getComputedStyle(i).opacity,getComputedStyle(i).transform])')==frozen
 page.evaluate('window.testHidden=false;document.dispatchEvent(new Event("visibilitychange"))')
 page.wait_for_timeout(1300)
 page.emulate_media(reduced_motion='reduce');page.wait_for_timeout(100)
 reduced=page.locator('.banner-product.is-active').get_attribute('src')
 page.wait_for_timeout(5500);assert page.locator('.banner-product.is-active').get_attribute('src')==reduced
 context=browser.new_context(java_script_enabled=False,viewport={'width':375,'height':900})
 nojs=context.new_page();nojs.goto(url);nojs.locator('.banner-product').first.evaluate('(i)=>i.decode()');assert nojs.locator('#home-title').is_visible()
 browser.close();assert not errors,errors
print('PASS: simulated inactive-tab freeze/resume, reduced motion, no-JS fallback and no JavaScript exceptions.')
