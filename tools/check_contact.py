from playwright.sync_api import sync_playwright
from urllib.parse import unquote
with sync_playwright() as p:
 b=p.chromium.launch();page=b.new_page(viewport={'width':375,'height':850},reduced_motion='reduce')
 page.goto('http://127.0.0.1:5173/contact.html',wait_until='domcontentloaded')
 assert page.locator('#contact-whatsapp').is_disabled()
 page.locator('#contact-form button[type="submit"]').click()
 assert page.locator('#contact-form [aria-invalid=true]').count()==4
 for key,value in {'name':'Website QA','company':'Example Company','email':'qa@example.com','phone':'+94 11 234 5678','message':'Please discuss a packaging enquiry & artwork requirements.'}.items():page.locator('#contact-'+key).fill(value)
 page.locator('#contact-form button[type="submit"]').click()
 assert page.locator('#contact-preview').is_visible()
 assert 'Nothing has been sent' in page.locator('#contact-status').inner_text()
 draft=unquote(page.locator('#contact-email-draft').get_attribute('href'))
 assert draft.startswith('mailto:info@technoind.biz?') and 'Example Company' in draft and 'packaging enquiry & artwork' in draft
 page.locator('#contact-message').fill('Updated enquiry')
 assert not page.locator('#contact-preview').is_visible()
 page.locator('#contact-phone').fill('........')
 page.locator('#contact-form button[type="submit"]').click()
 assert page.locator('#contact-phone').get_attribute('aria-invalid')=='true'
 b.close()
print('PASS: contact required fields, phone validation, draft preview and encoding, edit invalidation, and unconfigured WhatsApp state. No message was sent.')
