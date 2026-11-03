from pathlib import Path
from playwright.sync_api import sync_playwright
root=Path(__file__).resolve().parents[1]
with sync_playwright() as p:
 b=p.chromium.launch();page=b.new_page(viewport={'width':1440,'height':950},reduced_motion='reduce')
 page.goto('http://127.0.0.1:5173/',wait_until='networkidle')
 about=page.locator('.nav-dropdown').filter(has=page.locator('#dropdown-about'))
 about.hover();assert page.locator('#dropdown-about').is_visible()
 assert about.locator('button').get_attribute('aria-expanded')=='true'
 page.screenshot(path=str(root/'tools/dropdown-desktop.png'))
 page.locator('h1').hover();assert not page.locator('#dropdown-about').is_visible()
 about.locator('button').focus();page.keyboard.press('ArrowDown')
 assert page.locator('#dropdown-about>a').first.evaluate('(el)=>el===document.activeElement')
 page.keyboard.press('End');assert page.locator('#dropdown-about>a').last.evaluate('(el)=>el===document.activeElement')
 page.keyboard.press('Escape');assert not page.locator('#dropdown-about').is_visible()
 assert about.locator('button').evaluate('(el)=>el===document.activeElement')
 page.set_viewport_size({'width':375,'height':850});page.locator('.menu-toggle').click()
 about.locator('button').click();assert page.locator('#dropdown-about').is_visible()
 assert page.locator('.nav-dropdown').count()==2
 assert page.locator('#navigation>a[href="products.html"]').count()==1
 assert page.locator('#navigation>a[href="quality.html"]').count()==1
 page.screenshot(path=str(root/'tools/dropdown-mobile.png'))
 page.keyboard.press('Escape');assert not page.locator('#dropdown-about').is_visible();assert page.locator('#navigation').is_visible()
 page.keyboard.press('Escape');assert not page.locator('#navigation').is_visible()
 page.locator('.menu-toggle').click();page.locator('[aria-controls="dropdown-about"]').click();page.locator('#dropdown-about a[href="about.html#why-us"]').click()
 page.wait_for_url('**/about.html#why-us');assert page.locator('#why-us').get_attribute('open') is not None
 page.locator('.menu-toggle').click();page.locator('[aria-controls="dropdown-industries"]').click()
 assert page.locator('#dropdown-industries button').all_text_contents()==['Techno Industries','Grand Techno','Techno Farm']
 before=page.url
 page.locator('#dropdown-industries button').nth(1).click();assert page.url==before
 assert page.locator('#dropdown-about').inner_text().find('Techno Group')==-1
 page.set_viewport_size({'width':1440,'height':950});page.locator('[aria-controls="dropdown-industries"]').hover()
 page.screenshot(path=str(root/'tools/industries-dropdown.png'))
 context=b.new_context(java_script_enabled=False,viewport={'width':375,'height':850});fallback=context.new_page();fallback.goto('http://127.0.0.1:5173/')
 assert fallback.locator('#dropdown-about').is_visible()
 assert not fallback.evaluate('document.documentElement.scrollWidth>innerWidth')
 b.close()
print('PASS: desktop hover, keyboard arrows/Home/End/Escape, mobile accordion, submenu navigation/filtering, and no-JavaScript fallback.')
