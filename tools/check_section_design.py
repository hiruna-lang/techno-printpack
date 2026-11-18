"""Validate the neutral/navy section refinement without rebuilding or sending enquiries."""
from pathlib import Path
import colorsys
import hashlib
import json
import re
import sys
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
URL=(sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:8765').rstrip('/')
PAGES=['index','about','products','capabilities','industries','quality','quotation','contact']
REVIEW_PAGES=next((arg.split('=',1)[1].split(',') for arg in sys.argv[2:] if arg.startswith('--pages=')),PAGES)
if '--motion-only' in sys.argv:REVIEW_PAGES=[]
assert all(name in PAGES for name in REVIEW_PAGES),REVIEW_PAGES
BASE=ROOT/'tmp/section-refinement/before'
OUT=ROOT/'tmp/section-refinement/review';OUT.mkdir(parents=True,exist_ok=True)
for name,digest in json.loads((BASE/'hashes.json').read_text(encoding='utf-8')).items():
    if Path(name).as_posix()=='index.html':continue
    assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==digest,f'Protected source changed: {name}'
for name in PAGES:
    before=BeautifulSoup((BASE/f'{name}.html').read_text(encoding='utf-8'),'html.parser')
    after=BeautifulSoup((ROOT/f'{name}.html').read_text(encoding='utf-8'),'html.parser')
    if name=='index':
        wrapper=after.select('.home-quality-heading');assert len(wrapper)==1
        wrapper[0].unwrap()
    assert str(after)==str(before),f'Content or navigation changed: {name}'
print('PASS: only the intended homepage wrapper changed; facts, headings, links, forms, images, navigation/footer, scripts, Farm and Grand Techno preserved.',flush=True)

def rgb(value):return tuple(float(x) for x in re.findall(r'[\d.]+',value)[:3])
def contrast(first,second):
    def lum(values):
        linear=[v/255/12.92 if v/255<=.04045 else ((v/255+.055)/1.055)**2.4 for v in values]
        return sum(x*y for x,y in zip(linear,[.2126,.7152,.0722]))
    pair=sorted([lum(rgb(first)),lum(rgb(second))])
    return (pair[1]+.05)/(pair[0]+.05)

with sync_playwright() as p:
    browser=p.chromium.launch()
    page=browser.new_page(reduced_motion='reduce',viewport={'width':1440,'height':1100})
    errors=[];missing=[]
    page.on('pageerror',lambda error:errors.append(str(error)))
    page.on('response',lambda response:missing.append(response.url) if response.url.startswith(URL) and response.status>=400 else None)

    def visit(name):
        page.goto(f'{URL}/{name}.html',wait_until='domcontentloaded')
        page.evaluate('''async()=>{const images=[...document.querySelectorAll('main img[src]')];images.forEach(i=>i.loading='eager');await Promise.all(images.map(i=>i.decode().catch(()=>{})));await document.fonts.ready;}''')
        assert page.locator('main img[src]').evaluate_all('(images)=>images.every(i=>i.complete&&i.naturalWidth>0)'),name

    def colour(selector,background,foreground_selector=None):
        target=page.locator(selector)
        actual=target.evaluate('(e)=>getComputedStyle(e).backgroundColor')
        assert actual==background,(selector,actual,background)
        if foreground_selector:
            texts=target.locator(foreground_selector).evaluate_all('(els)=>els.map(e=>({text:e.textContent,color:getComputedStyle(e).color}))')
            assert texts,selector
            for text in texts:assert contrast(text['color'],background)>=4.5,(selector,text,'contrast')

    def capture(selector,name,width):
        target=page.locator(selector)
        target.evaluate('(e)=>e.scrollIntoView({block:"center",behavior:"instant"})')
        # Component-only reviews exclude the sticky header; application styles are restored immediately.
        style=page.add_style_tag(content='.header{visibility:hidden!important}')
        target.screenshot(path=str(OUT/f'{name}-{width}.png'))
        style.evaluate('(e)=>e.remove()')

    for name in REVIEW_PAGES:
        for width in [320,375,430,768,1024,1440,1920]:
            page.set_viewport_size({'width':width,'height':1100});visit(name)
            assert not page.evaluate('document.documentElement.scrollWidth>innerWidth'),(name,width,'overflow')
            # Gold remains available for actions/icons; broad informational slabs should be neutral or navy.
            panels=page.locator('main :is(section,article,aside,div)').evaluate_all('''els=>els.map(e=>{const r=e.getBoundingClientRect(),s=getComputedStyle(e);return {cls:e.className,bg:s.backgroundColor,width:r.width,height:r.height}}).filter(e=>e.width>180&&e.height>70&&e.width*e.height>18000)''')
            for panel in panels:
                values=rgb(panel['bg'])
                if len(values)<3 or panel['bg']=='rgba(0, 0, 0, 0)':continue
                hue,light,sat=colorsys.rgb_to_hls(*(x/255 for x in values))
                assert not(.055<hue<.16 and sat>.5 and .18<light<.8),(name,width,panel,'Large gold panel')
            if name=='index':
                colour('.corp-section.corp-soft:has(.corp-about)','rgb(15, 42, 67)')
                colour('.corp-photo-caption','rgb(243, 246, 248)')
                colour('.corp-marks','rgb(255, 255, 255)','h2,.corp-link')
                layout=page.locator('.corp-marks').evaluate('''e=>{const c=e.querySelector('.container').getBoundingClientRect(),h=e.querySelector('.home-quality-copy').getBoundingClientRect(),rail=e.querySelector('.marks-viewport').getBoundingClientRect(),a=e.querySelector('.corp-link').getBoundingClientRect();return {container:c.width,heading:h.width,rail:rail.width,headingBottom:h.bottom,railTop:rail.top,button:{x:a.x,right:a.right,height:a.height}}}''')
                assert abs(layout['rail']-layout['container'])<1 and abs(layout['heading']-layout['container'])<1,(width,layout)
                assert layout['headingBottom']<=layout['railTop'] and layout['button']['height']>=44,(width,layout)
                assert page.locator('.home-quality-copy a').count()==1 and page.locator('.corp-marks button').count()==0
                if width in [375,1440]:
                    capture('.corp-section.corp-soft:has(.corp-about)','home-about',width)
                    capture('.corp-marks','home-quality',width)
            elif name=='about':
                colour('.corp-leadership-focus','rgb(243, 246, 248)','h3,li')
                colour('.about-approach','rgb(15, 42, 67)','h2,p,a')
                assert page.locator('.about-approach h2').evaluate('(e)=>getComputedStyle(e).color')=='rgb(255, 255, 255)'
                overlay=page.locator('.about-approach').evaluate('(e)=>getComputedStyle(e,"::after").backgroundImage')
                assert 'linear-gradient' in overlay and '217, 138, 31' not in overlay,overlay
                if width in [375,1440]:
                    capture('.corp-leadership-focus','about-focus',width)
                    capture('.about-approach','about-approach',width)
            elif name=='products':
                colour('.profile-two-column > div:first-child','rgb(243, 246, 248)','p,li')
            elif name=='capabilities':
                colour('.capability-strengths','rgb(243, 246, 248)','h2,h3,p')
                colour('.capability-cta','rgb(255, 255, 255)','h2,p')
                colour('.capability-cta .button','rgb(15, 42, 67)')
                assert page.locator('.capability-cta .button').evaluate('(e)=>getComputedStyle(e).color')=='rgb(255, 255, 255)'
                assert page.locator('.capability-cta-photo').evaluate('(e)=>getComputedStyle(e).display!=="none"&&getComputedStyle(e).opacity==="1"'),(width,'Factory photo visibility')
                geometry=page.locator('.capability-cta').evaluate('''e=>{const r=e.getBoundingClientRect(),s=getComputedStyle(e),photo=e.querySelector('.capability-cta-photo').getBoundingClientRect(),a=e.querySelector('.button').getBoundingClientRect();return {rect:{x:r.x,right:r.right,bottom:r.bottom},innerWidth:r.width-parseFloat(s.paddingLeft)-parseFloat(s.paddingRight)-2,photo:{width:photo.width,height:photo.height},button:{x:a.x,right:a.right,width:a.width,height:a.height,bottom:a.bottom}}}''')
                assert geometry['button']['x']>=geometry['rect']['x'] and geometry['button']['right']<=geometry['rect']['right'] and geometry['button']['bottom']<=geometry['rect']['bottom'],(width,geometry)
                assert geometry['button']['height']>=44
                if width>1000:assert abs(geometry['photo']['width']-180)<1 and abs(geometry['photo']['height']-140)<1,(width,geometry)
                elif width>700:assert abs(geometry['photo']['width']-140)<1 and abs(geometry['photo']['height']-160)<1,(width,geometry)
                else:
                    assert abs(geometry['photo']['height']-180)<1,(width,geometry)
                    assert abs(geometry['button']['width']-geometry['innerWidth'])<1,(width,geometry,'Mobile button width')
                assert page.locator('.capability-cta-box').is_hidden()
                if width in [375,1440]:
                    capture('.capability-cta','capability-consultation',width)
                    capture('.capability-strengths','capability-strengths',width)
            elif name=='quality':
                colour('.quality-themes','rgb(243, 246, 248)','h2,h3,p')
                colour('.quality-standards-layout > div:first-child','rgb(243, 246, 248)','h2,p')
                if width in [375,1440]:capture('.quality-themes','quality-themes',width)
            elif name=='quotation':
                colour('.quote-grid > aside','rgb(243, 246, 248)','h2,h3,p,li,a')
        print(f'PASS: {name}, seven responsive widths, neutral/navy panels, readable text and intact assets.',flush=True)

    # The full-width rail must be seamless at desktop, stacked tablet and mobile widths.
    page.emulate_media(reduced_motion='no-preference')
    for width in [375,768,900,1440,1920]:
        page.set_viewport_size({'width':width,'height':1100});visit('index')
        section=page.locator('.corp-marks')
        section.evaluate('(e)=>e.scrollIntoView({block:"center",behavior:"instant"})')
        page.wait_for_function('document.querySelector(".corp-marks").dataset.marksRunning==="true"')
        values=section.evaluate('''e=>{const t=e.querySelector('.marks-track'),groups=[...t.children],r=e.querySelector('.home-quality-copy').getBoundingClientRect(),origin=e.getBoundingClientRect(),s=getComputedStyle(t);return {groups:groups.map(g=>g.getBoundingClientRect().width),rail:e.querySelector('.marks-viewport').getBoundingClientRect().width,duration:s.animationDuration,easing:s.animationTimingFunction,x:new DOMMatrix(s.transform).m41,copy:[r.x-origin.x,r.y-origin.y,r.width,r.height],clones:e.querySelectorAll('.marks-clone[aria-hidden="true"][inert]').length}}''')
        assert abs(values['groups'][0]-values['groups'][1])<1 and values['groups'][0]+1>=values['rail'],(width,values)
        assert values['duration']=='64s' and values['easing']=='linear' and values['clones']==1,(width,values)
        page.wait_for_timeout(500)
        after=section.evaluate('''e=>{const r=e.querySelector('.home-quality-copy').getBoundingClientRect(),origin=e.getBoundingClientRect();return {x:new DOMMatrix(getComputedStyle(e.querySelector('.marks-track')).transform).m41,copy:[r.x-origin.x,r.y-origin.y,r.width,r.height]}}''')
        assert after['x']>values['x'] and all(abs(a-b)<.01 for a,b in zip(after['copy'],values['copy'])),(width,values,after)
        assert section.locator('button').count()==0
        print(f'PASS: {width}px, equal full-width loop groups, 64-second rightward motion and fixed copy.',flush=True)

    # Pause through CSS playback state, without manually overriding the Animation object.
    section=page.locator('.corp-marks')
    page.evaluate('''()=>{window.qaHidden=true;Object.defineProperty(document,'hidden',{configurable:true,get:()=>window.qaHidden});document.dispatchEvent(new Event('visibilitychange'));}''')
    page.wait_for_function('document.querySelector(".corp-marks").dataset.marksRunning==="false"')
    page.wait_for_timeout(60)
    frozen=section.locator('.marks-track').evaluate('(e)=>getComputedStyle(e).transform')
    page.wait_for_timeout(400)
    assert frozen==section.locator('.marks-track').evaluate('(e)=>getComputedStyle(e).transform')
    page.evaluate('window.qaHidden=false;document.dispatchEvent(new Event("visibilitychange"))')
    page.wait_for_function('document.querySelector(".corp-marks").dataset.marksRunning==="true"')
    page.evaluate('window.scrollTo({top:0,behavior:"instant"})')
    page.wait_for_function('document.querySelector(".corp-marks").dataset.marksRunning==="false"')
    page.wait_for_timeout(60)
    frozen=section.locator('.marks-track').evaluate('(e)=>getComputedStyle(e).transform')
    page.wait_for_timeout(400)
    assert frozen==section.locator('.marks-track').evaluate('(e)=>getComputedStyle(e).transform')

    page.emulate_media(reduced_motion='reduce')
    for width in [375,1440]:
        page.set_viewport_size({'width':width,'height':1100});visit('index')
        assert page.locator('.corp-marks .corp-mark-images').first.locator('figure:visible').count()==4
        assert page.locator('.corp-marks .marks-clone:visible').count()==0
        nojs=browser.new_context(java_script_enabled=False,viewport={'width':width,'height':1100})
        fallback=nojs.new_page();fallback.goto(URL+'/index.html',wait_until='domcontentloaded')
        assert fallback.locator('.corp-marks figure:visible').count()==4
        assert not fallback.evaluate('document.documentElement.scrollWidth>innerWidth')
        nojs.close()
    assert not errors,errors
    assert not missing,missing
    browser.close()
print('PASS: hidden/offscreen pause, reduced-motion/no-JS four-mark fallback, no manual controls, no JS exceptions or missing local assets.',flush=True)
