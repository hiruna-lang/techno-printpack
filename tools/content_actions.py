"""Keep purposeful enquiries and navigation; render product/process facts as information.

This authoring pass changes main content only. Headers, footers, forms, verified
company facts, images and product enquiry destinations remain authoritative.
"""
import re
from urllib.parse import urlsplit
from bs4 import BeautifulSoup

def information(element, name='div', extra_class=None):
    element.name=name
    for attribute in ('href','target','rel','role','tabindex','aria-label'):
        element.attrs.pop(attribute,None)
    if extra_class:
        element['class']=[*element.get('class',[]),extra_class]

def refine_actions(page, content):
    soup=BeautifulSoup(content,'html.parser')

    if page=='index':
        quality=soup.select_one('.home-quality-copy')
        if quality and not quality.select_one('.home-quality-heading'):
            heading=soup.new_tag('div')
            heading['class']=['home-quality-heading']
            for element in list(quality.select(':scope > .eyebrow, :scope > h2')):
                heading.append(element.extract())
            quality.insert(0,heading)
        for link in soup.select('.corp-about-links .corp-link, .corp-solutions article .corp-link, .corp-process-layout > div > .corp-link'):
            link.decompose()
        for photo in soup.select('a.corp-solution-photo'):
            information(photo)
        for section in soup.select('.home-enquiry'):
            section.decompose()

    elif page=='about':
        for link in soup.select('.corp-leadership-copy > a[href="quality.html"]'):
            link.decompose()

    elif page=='products':
        for grid in soup.select('.profile-tag-grid'):
            grid.name='ul'
            grid['class']=['profile-tag-grid','profile-structure-list']
            grid['aria-label']='Corrugated box structures'
            for item in grid.select(':scope > a'):
                for arrow in item.select('[aria-hidden="true"]'):
                    arrow.decompose()
                information(item,'li')
        for section in soup.select('.cta.section'):
            section.decompose()

    elif page=='capabilities':
        for item in soup.select('.capability-strengths > .container > a'):
            information(item,'article','capability-strength')
        for link in soup.select('.capability-card-detail a[href*="quotation.html"]'):
            link.decompose()
        for toggle in soup.select('.capability-expand'):
            toggle.string='+'

    elif page=='industries':
        for link in soup.select('.sector-grid article a[href="quotation.html"]'):
            link.decompose()
        for section in soup.select('.cta.section'):
            section.decompose()

    elif page=='quality':
        for item in soup.select('.quality-themes > .container > a'):
            information(item,'article','quality-theme')
        for item in soup.select('.quality-process-steps li > a'):
            information(item,'div','quality-step')
        for arrow in soup.select('.quality-process-steps li > b[aria-hidden="true"]'):
            arrow.decompose()
        for link in soup.select('.quality-document-grid details a[href="contact.html"]'):
            link.decompose()
        intro=soup.select_one('.quality-standards-layout > div:first-child')
        if intro and not intro.select_one('.quality-document-link'):
            link=soup.new_tag('a',href='contact.html')
            link['class']=['text-link','quality-document-link']
            link.string='Request documentation'
            intro.append(link)
        for section in soup.select('.quality-cta-section'):
            section.decompose()

    elif page=='contact':
        for section in soup.select('.contact-quote-banner'):
            section.decompose()

    # Retained actions use their labels; an external-map arrow still signals a new site.
    for link in soup.select('a[href]'):
        if urlsplit(link['href']).scheme in ('http','https'):
            continue
        for arrow in link.select('span, b, .catalogue-arrow, [aria-hidden="true"]'):
            if arrow.parent is not None and arrow.get_text(strip=True) in ('↗','→','⟶','➜'):
                arrow.decompose()
        if 'banner-button' in link.get('class',[]):
            for arrow in link.select('svg'):
                arrow.decompose()
        for text in list(link.find_all(string=True,recursive=False)):
            cleaned=re.sub(r'\s*[↗→⟶➜]\s*$','',str(text))
            if cleaned!=str(text):text.replace_with(cleaned)

    return str(soup)
