from playwright.sync_api import sync_playwright
with sync_playwright() as p:
 b=p.chromium.launch()
 page=b.new_page()
 for width in [320,375,768,1440,1920]:
  page.set_viewport_size({'width':width,'height':1000})
  page.goto('http://127.0.0.1:5173/index.html')
  page.wait_for_function('document.querySelector(".hero-video").currentTime > 0')
  assert page.locator('.hero-slide').count()==0
  assert page.locator('.hero-pagination').count()==0
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
  v=page.locator('.hero-video')
  assert v.evaluate('(v)=>v.muted && v.loop && v.playsInline && v.videoWidth===1920')
  page.locator('.hero-video-toggle').click()
  assert v.evaluate('(v)=>v.paused')
  page.locator('.hero-video-toggle').click()
  page.wait_for_function('!document.querySelector(".hero-video").paused')
  if width in [375,1440]:page.locator('.ref-hero').screenshot(path=f'tmp/hero-video-{width}.png')
 page.emulate_media(reduced_motion='reduce')
 page.reload()
 page.wait_for_timeout(500)
 assert page.locator('.hero-video').evaluate('(v)=>v.paused')
 b.close()
print('PASS: video playback, mute/loop, pause/play, reduced motion and five responsive widths')
