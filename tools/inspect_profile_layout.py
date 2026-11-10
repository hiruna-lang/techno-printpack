from playwright.sync_api import sync_playwright
import json
with sync_playwright() as p:
 b=p.chromium.launch();page=b.new_page(viewport={'width':768,'height':950})
 page.goto('http://127.0.0.1:5173/quality.html')
 print(json.dumps(page.evaluate('''()=>Array.from(document.querySelectorAll('main *')).map(el=>({tag:el.tagName,cls:el.className,width:el.getBoundingClientRect().width,right:el.getBoundingClientRect().right})).filter(x=>x.right>innerWidth+1).slice(0,20)'''),indent=2))
 b.close()
