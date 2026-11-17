"""Rendered UI colour coverage; photography/logos are masked, original files untouched."""
from pathlib import Path
import json,sys
import numpy as np
from PIL import Image
from playwright.sync_api import sync_playwright

root=Path(__file__).resolve().parents[1]
label=sys.argv[1] if len(sys.argv)>1 else 'review'
out=root/'tmp/colour-audit'/label;out.mkdir(parents=True,exist_ok=True)
pages=['index','about','products','capabilities','industries','quality','quotation','contact']
if len(sys.argv)>4:pages=sys.argv[4].split(',')
widths=[1440,375]
if len(sys.argv)>2:widths=[int(w) for w in sys.argv[2].split(',')]
url=(sys.argv[3] if len(sys.argv)>3 else 'http://127.0.0.1:5500').rstrip('/')
palette=np.array([[255,255,255],[15,42,67],[217,138,31]],dtype=np.int32)
results={}
with sync_playwright() as p:
    browser=p.chromium.launch()
    page=browser.new_page(reduced_motion='reduce')
    for width in widths:
        for name in pages:
            page.set_viewport_size({'width':width,'height':1000})
            page.goto(f'{url}/{name}.html',wait_until='domcontentloaded')
            page.evaluate('''async()=>{const imgs=[...document.images].filter(i=>i.getAttribute('src'));imgs.forEach(i=>i.loading='eager');await Promise.all(imgs.map(i=>i.decode().catch(()=>{})));await document.fonts.ready;}''')
            inventory=page.evaluate('''()=>[...document.querySelectorAll('.utility-bar,.header,main>section,.site-footer')].map(e=>({tag:e.tagName,cls:e.className,id:e.id,height:Math.round(e.getBoundingClientRect().height),bg:getComputedStyle(e).backgroundColor,heading:e.querySelector('h1,h2')?.textContent}))''')
            (out/f'{name}-{width}-sections.json').write_text(json.dumps(inventory,indent=2),encoding='utf-8')
            page.screenshot(path=str(out/f'{name}-{width}.png'),full_page=True)
            page.evaluate('''()=>{const node=document.createElementNS('http://www.w3.org/2000/svg','svg');node.setAttribute('width','0');node.setAttribute('height','0');node.style.position='fixed';node.innerHTML='<defs><filter id="theme-audit-media" color-interpolation-filters="sRGB"><feFlood flood-color="#ff00ff"/><feComposite in2="SourceAlpha" operator="in"/></filter></defs>';document.body.append(node);}''')
            page.add_style_tag(content='img:not(.banner-studio),video,iframe,canvas{filter:url(#theme-audit-media)!important}')
            audit_path=out/f'{name}-{width}-ui-mask.png'
            page.screenshot(path=str(audit_path),full_page=True)
            pixels=np.asarray(Image.open(audit_path).convert('RGB')).reshape(-1,3).astype(np.int32)
            # Exclude visible photography and image logos; strong navy overlays remain UI paint.
            mask=(pixels[:,0]>pixels[:,1]+35)&(pixels[:,2]>pixels[:,1]+35)&(pixels[:,0]>70)&(pixels[:,2]>70)
            selected=pixels[~mask]
            # Chunk to avoid large intermediate arrays on long mobile pages.
            counts=np.zeros(3,dtype=np.int64)
            for offset in range(0,len(selected),250000):
                sample=selected[offset:offset+250000]
                nearest=((sample[:,None,:]-palette[None,:,:])**2).sum(axis=2).argmin(axis=1)
                counts+=np.bincount(nearest,minlength=3)
            shares=(counts/counts.sum()*100).round(2).tolist()
            results[f'{name}-{width}']={'white':shares[0],'navy':shares[1],'gold':shares[2],'pixels':counts.tolist(),'photo_excluded_percent':round(float(mask.mean()*100),2),'height':Image.open(audit_path).height}
            print(name,width,shares,'page height',results[f'{name}-{width}']['height'],flush=True)
    browser.close()
(out/'results.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
for width in widths:
    totals=np.sum([v['pixels'] for key,v in results.items() if key.endswith('-'+str(width))],axis=0)
    print('AGGREGATE',width,(totals/totals.sum()*100).round(2).tolist(),flush=True)
