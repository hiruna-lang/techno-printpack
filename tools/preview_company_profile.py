from pathlib import Path
from playwright.sync_api import sync_playwright
root=Path(__file__).resolve().parents[1];out=root/'tmp/content-audit';out.mkdir(exist_ok=True,parents=True)
with sync_playwright() as p:
 b=p.chromium.launch();page=b.new_page(reduced_motion='reduce')
 for width in [1440,375]:
  page.set_viewport_size({'width':width,'height':950})
  for name in ['index','about','products','industries','capabilities','quality','quotation','contact']:
   page.goto('http://127.0.0.1:5173/'+name+'.html',wait_until='domcontentloaded')
   page.locator('img').evaluate_all('(images)=>images.forEach(i=>i.loading="eager")')
   for y in range(0,page.evaluate('document.body.scrollHeight'),850):
    page.evaluate('(y)=>window.scrollTo({top:y,behavior:"instant"})',y);page.wait_for_timeout(70)
   page.wait_for_timeout(250);page.evaluate('window.scrollTo({top:0,behavior:"instant"})')
   page.wait_for_function('Array.from(document.images).every(i=>i.complete&&i.naturalWidth>0)')
   assert not page.evaluate('document.documentElement.scrollWidth>innerWidth'),(name,width)
   page.screenshot(path=str(out/f'{name}-{width}.png'),full_page=True)
 b.close()
print('Visual previews and image/overflow checks complete at 1440px and 375px.')
