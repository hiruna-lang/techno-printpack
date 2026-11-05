from pathlib import Path
from playwright.sync_api import sync_playwright
root=Path(__file__).resolve().parents[1]
with sync_playwright() as p:
 b=p.chromium.launch()
 page=b.new_page()
 response=page.goto('https://www.technoprintpack.com/images/logo-1.png',wait_until='load',timeout=30000)
 print('Logo response:',response.status,response.headers.get('content-type'))
 if response.ok and 'image/' in response.headers.get('content-type',''):
  (root/'assets/icons/techno-group-original.png').write_bytes(response.body())
  print('Saved company logo')
 b.close()
