from pathlib import Path
from playwright.sync_api import sync_playwright
root=Path(__file__).resolve().parents[1]
with sync_playwright() as p:
 b=p.chromium.launch()
 page=b.new_page(viewport={'width':1440,'height':1000},reduced_motion='reduce')
 for name in ['contact']:
  page.goto('http://127.0.0.1:5173/'+name+'.html',wait_until='networkidle')
  page.locator('img').evaluate_all('(imgs)=>imgs.forEach(i=>i.loading="eager")')
  for y in range(0,page.evaluate('document.body.scrollHeight'),600):
   page.evaluate('(y)=>window.scrollTo({top:y,behavior:"instant"})',y);page.wait_for_timeout(180)
  page.wait_for_timeout(700);page.evaluate('window.scrollTo({top:0,behavior:"instant"})');page.wait_for_timeout(300)
  page.wait_for_function('Array.from(document.images).every(i=>i.complete && i.naturalWidth > 0)')
  page.screenshot(path=str(root/f'tools/redesign-{name}-desktop.png'),full_page=True)
 page.set_viewport_size({'width':375,'height':850})
 page.goto('http://127.0.0.1:5173/contact.html',wait_until='networkidle')
 page.locator('img').evaluate_all('(imgs)=>imgs.forEach(i=>i.loading="eager")')
 for y in range(0,page.evaluate('document.body.scrollHeight'),600):
  page.evaluate('(y)=>window.scrollTo({top:y,behavior:"instant"})',y);page.wait_for_timeout(180)
 page.wait_for_timeout(700);page.evaluate('window.scrollTo({top:0,behavior:"instant"})');page.wait_for_timeout(300)
 page.screenshot(path=str(root/'tools/redesign-contact-mobile.png'),full_page=True)
 b.close()
