"""Verify shared navigation, page preservation and accessible interaction states."""
from pathlib import Path
import re
import sys
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
URL=(sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:5173').rstrip('/')
PAGES=['index','about','products','capabilities','industries','quality','quotation','contact']
OUT=ROOT/'tmp/navigation-refresh';OUT.mkdir(parents=True,exist_ok=True)

def without_navigation(text):
    text=re.sub(r'<header class="header">.*?</header>','',text,count=1,flags=re.S)
    return text.replace('<link rel="stylesheet" href="assets/css/navigation.css">','').replace('<script defer src="assets/js/navigation.js"></script>','')

for name in PAGES:
    current=(ROOT/f'{name}.html').read_text(encoding='utf-8')
    baseline=OUT/f'{name}.html'
    if baseline.exists():
        assert without_navigation(current)==without_navigation(baseline.read_text(encoding='utf-8')),f'Page content changed outside navigation: {name}'
    assert current.count('assets/css/navigation.css')==1,name
    assert current.count('assets/js/navigation.js')==1,name
    assert current.index('assets/css/navigation.css')>current.index('assets/css/brand-theme.css'),name
print('PASS: eight shared headers; page content, metadata and footer preserved.',flush=True)

with sync_playwright() as p:
    browser=p.chromium.launch()
    page=browser.new_page(reduced_motion='reduce',viewport={'width':1440,'height':1000})
    errors=[]
    page.on('pageerror',lambda error:errors.append(str(error)))

    def visit(name='index'):
        page.goto(f'{URL}/{name}.html',wait_until='domcontentloaded')
        page.locator('.header.nav-ready').wait_for(state='attached')

    def expanded(key,open=True):
        toggle=page.locator(f'[aria-controls="dropdown-{key}"]')
        page.wait_for_function('(args)=>document.querySelector(args[0]).getAttribute("aria-expanded")===args[1]',arg=[f'[aria-controls="dropdown-{key}"]',str(open).lower()])
        inert=page.locator(f'#dropdown-{key}').evaluate('(e)=>e.inert')
        assert inert==(not open),(key,page.viewport_size,toggle.get_attribute('aria-expanded'),inert,open)
        return toggle

    for name in PAGES:
        for width in [320,375,430,768,1024,1440,1920]:
            page.set_viewport_size({'width':width,'height':1000})
            visit(name)
            data=page.evaluate('''()=>{const rect=e=>{const r=e.getBoundingClientRect();return {x:r.x,right:r.right,y:r.y,bottom:r.bottom,width:r.width,height:r.height}},header=document.querySelector('.header'),logo=header.querySelector('.brand'),nav=header.querySelector('#navigation');return {overflow:document.documentElement.scrollWidth>innerWidth,header:rect(header),logo:rect(logo),active:nav.querySelectorAll('[aria-current="page"]').length,transform:getComputedStyle(header.querySelector('.header-inner')).transform,links:[...nav.querySelectorAll(':scope>.nav-link,:scope>.nav-dropdown,:scope>.button')].map(rect)};}''')
            assert not data['overflow'],(name,width,'overflow')
            assert data['active']==1,(name,width,'active marker')
            assert abs(data['header']['height']-(69 if width<=600 else 79))<1,(name,width,data['header'])
            assert 0<=data['logo']['x']<data['logo']['right']<=width,(name,width,'logo')
            assert data['transform']=='none',(name,width,'header scaling')
            if width>1100:
                assert all(r['x']>=data['logo']['right'] and r['right']<=width for r in data['links']),(name,width,'desktop link fit')
                assert all(data['links'][i]['right']<=data['links'][i+1]['x']+1 for i in range(len(data['links'])-1)),(name,width,'overlap')
            else:
                assert page.locator('#navigation').evaluate('(e)=>e.inert')
                page.locator('.menu-toggle').click()
                assert not page.locator('#navigation').evaluate('(e)=>e.inert')
                nav=page.locator('#navigation').bounding_box()
                assert nav and nav['x']>=0 and nav['x']+nav['width']<=width+1 and nav['y']+nav['height']<=1001,(name,width,nav)
                controls=page.locator('#navigation>.nav-link,#navigation>.nav-dropdown>.nav-dropdown-heading>.nav-link,#navigation>.button,.dropdown-toggle').evaluate_all('(els)=>els.map(e=>e.getBoundingClientRect().height)')
                assert min(controls)>=44,(name,width,controls)
            for key in ['about','industries']:
                toggle=page.locator(f'[aria-controls="dropdown-{key}"]')
                toggle.click()
                expanded(key)
                panel=page.locator(f'#dropdown-{key}').bounding_box()
                assert panel and panel['x']>=-1 and panel['x']+panel['width']<=width+1,(name,width,key,panel)
                if width>1100:assert panel['y']+panel['height']<=1000,(name,width,key,panel)
                page.keyboard.press('Escape');expanded(key,False)
            if width<=1100:
                page.keyboard.press('Escape')
                assert page.locator('#navigation').evaluate('(e)=>e.inert')
            assert not page.evaluate('document.documentElement.scrollWidth>innerWidth'),(name,width,'open overflow')
        print(f'PASS: {name}, seven responsive widths, panel bounds and one active marker.',flush=True)

    page.set_viewport_size({'width':1440,'height':1000});visit()
    about=page.locator('[aria-controls="dropdown-about"]')
    about.focus();page.keyboard.press('ArrowDown');expanded('about')
    assert page.locator('#dropdown-about .dropdown-item').first.evaluate('(e)=>e===document.activeElement')
    page.keyboard.press('End');assert page.locator('#dropdown-about .dropdown-item').last.evaluate('(e)=>e===document.activeElement')
    page.keyboard.press('Home');assert page.locator('#dropdown-about .dropdown-item').first.evaluate('(e)=>e===document.activeElement')
    page.keyboard.press('ArrowUp');assert page.locator('#dropdown-about .dropdown-item').last.evaluate('(e)=>e===document.activeElement')
    page.keyboard.press('Escape');expanded('about',False)
    assert about.evaluate('(e)=>e===document.activeElement')
    assert about.evaluate('(e)=>getComputedStyle(e).outlineStyle')=='solid'

    page.locator('.brand').focus();page.mouse.move(10,500)
    page.locator('.nav-dropdown').first.hover();expanded('about')
    page.locator('#dropdown-about .dropdown-item').first.hover();assert about.get_attribute('aria-expanded')=='true'
    page.mouse.move(10,500);expanded('about',False)
    page.locator('.nav-dropdown').first.hover();expanded('about')
    page.screenshot(path=str(OUT/'navigation-desktop.png'))
    page.keyboard.press('Escape')

    page.set_viewport_size({'width':375,'height':850});visit()
    menu=page.locator('.menu-toggle');menu.click()
    page.locator('[aria-controls="dropdown-about"]').click();expanded('about')
    page.locator('[aria-controls="dropdown-industries"]').click();expanded('industries');expanded('about',False)
    assert page.locator('#dropdown-industries .dropdown-item strong').all_text_contents()==['Techno Industries','Grand Techno','Green Techno Farm']
    assert page.locator('#dropdown-industries a[href="farm/index.html"]').count()==1
    before=page.url;page.locator('#dropdown-industries button').click();assert page.url==before
    page.keyboard.press('Escape');expanded('industries',False)
    assert menu.get_attribute('aria-expanded')=='true'
    menu.focus();page.keyboard.press('Shift+Tab')
    assert page.locator('#navigation>.button').evaluate('(e)=>e===document.activeElement')
    page.keyboard.press('Tab');assert menu.evaluate('(e)=>e===document.activeElement')
    page.locator('[aria-controls="dropdown-about"]').click();expanded('about')
    page.screenshot(path=str(OUT/'navigation-mobile.png'))
    page.keyboard.press('Escape');expanded('about',False)
    page.keyboard.press('Escape');assert menu.get_attribute('aria-expanded')=='false'
    assert page.locator('#navigation').evaluate('(e)=>e.inert')
    assert menu.evaluate('(e)=>e===document.activeElement')
    menu.click();page.locator('[aria-controls="dropdown-about"]').click();expanded('about')
    page.locator('#dropdown-about a[href="about.html#why-us"]').click()
    page.wait_for_url('**/about.html#why-us')
    assert page.locator('#why-us').get_attribute('open') is not None
    page.locator('.menu-toggle').click();page.mouse.click(3,840)
    assert page.locator('.menu-toggle').get_attribute('aria-expanded')=='false'

    page.set_viewport_size({'width':1440,'height':1000});visit()
    height=page.locator('.header').bounding_box()['height']
    page.evaluate('window.scrollTo({top:600,behavior:"instant"})')
    page.locator('.header.stuck').wait_for(state='attached')
    assert abs(page.locator('.header').bounding_box()['height']-height)<1
    assert page.locator('.header-inner').evaluate('(e)=>getComputedStyle(e).transform')=='none'

    # The opening hero must still reserve room for the complete capability strip.
    for width,height in [(1536,729),(1280,600)]:
        page.set_viewport_size({'width':width,'height':height});visit()
        page.evaluate('async()=>{await document.fonts.ready;window.scrollTo({top:0,behavior:"instant"})}')
        assert page.locator('.packaging-highlights>.container').evaluate('(e)=>e.getBoundingClientRect().bottom<=innerHeight'),(width,height,'opening fold')

    # Initial load events must not dismiss an interaction; BFCache restoration resets it.
    page.set_viewport_size({'width':375,'height':850});visit()
    page.locator('.menu-toggle').click();page.locator('[aria-controls="dropdown-about"]').click();expanded('about')
    page.evaluate('window.dispatchEvent(new PageTransitionEvent("pageshow",{persisted:false}))')
    assert page.locator('.menu-toggle').get_attribute('aria-expanded')=='true'
    expanded('about')
    page.evaluate('window.dispatchEvent(new PageTransitionEvent("pageshow",{persisted:true}))')
    assert page.locator('.menu-toggle').get_attribute('aria-expanded')=='false'
    expanded('about',False)

    # Reduced-motion transitions are disabled; normal motion has a real fade.
    page.set_viewport_size({'width':1440,'height':1000});visit()
    assert page.locator('#dropdown-about').evaluate('(e)=>getComputedStyle(e).transitionDuration')=='0s'
    page.emulate_media(reduced_motion='no-preference');visit()
    page.locator('[aria-controls="dropdown-about"]').focus();page.keyboard.press('ArrowDown');expanded('about')
    page.wait_for_timeout(70)
    opacity=page.locator('#dropdown-about').evaluate('(e)=>Number(getComputedStyle(e).opacity)')
    assert 0<opacity<1,('dropdown fade',opacity)
    page.wait_for_timeout(300)
    assert page.locator('#dropdown-about').evaluate('(e)=>Number(getComputedStyle(e).opacity)')==1
    page.emulate_media(reduced_motion='reduce')

    for width in [375,1440]:
        context=browser.new_context(java_script_enabled=False,viewport={'width':width,'height':1000})
        fallback=context.new_page();fallback.goto(URL+'/index.html',wait_until='domcontentloaded')
        if width>1100:fallback.locator('.nav-dropdown').first.hover()
        assert fallback.locator('#dropdown-about .dropdown-item').first.is_visible(),width
        assert not fallback.evaluate('document.documentElement.scrollWidth>innerWidth'),width
        assert not fallback.locator('#navigation').evaluate('(e)=>e.inert'),width
        context.close()

    assert not errors,errors
    browser.close()
print('PASS: keyboard, pointer, mobile accordion, local links, no-JS fallback, stable sticky header and no JS errors.',flush=True)
