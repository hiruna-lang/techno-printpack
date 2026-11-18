"""Shared navigation markup.
Identical light floating capsule navbar across ALL pages (root, farm, grand-techno).
The navbar always features the Techno Industries logo and standard navigation.
Destination logos for Grand Techno and Green Techno Farm belong inside their page bodies.
"""
from html import escape

NAV_ITEMS = [
    ('index', 'Home'),
    ('about', 'About Us'),
    ('products', 'Products'),
    ('capabilities', 'Capabilities'),
    ('industries', 'Industries'),
    ('quality', 'Quality'),
    ('contact', 'Contact')
]

SUBMENUS = {
    'about': [
        ('about.html#company-information', 'Company Information'),
        ('about.html#why-us', 'Why Choose Us'),
        ('about.html#principles', 'Vision & Commitments'),
        ('quality.html#certifications', 'Certifications & Documentation'),
    ],
    'industries': [
        ('index.html', 'Techno Industries'),
        ('grand-techno/index.html', 'Grand Techno'),
        ('farm/index.html', 'Green Techno Farm'),
    ]
}

def render_header(page, base_path=""):
    items = []
    for key, label in NAV_ITEMS:
        current = ' aria-current="page"' if page == key or (key == 'industries' and page in ('grand-techno', 'farm')) else ''
        anchor = f'<a class="nav-link" href="{base_path}{key}.html"{current}>{escape(label)}</a>'
        if key not in SUBMENUS:
            items.append(anchor)
            continue
        
        children = SUBMENUS[key]
        rows = []
        for href, title in children:
            item_current = ''
            if page == 'grand-techno' and 'grand-techno' in href:
                item_current = ' aria-current="page"'
            elif page == 'farm' and 'farm' in href:
                item_current = ' aria-current="page"'
            elif page == 'index' and href == 'index.html':
                item_current = ' aria-current="page"'

            full_href = base_path + href if base_path else href
            cls = 'dropdown-item' + (' company-option' if key == 'industries' else '')
            rows.append(f'<a class="{cls}" href="{full_href}"{item_current}>{escape(title)}</a>')
        
        items.append(
            f'<div class="nav-dropdown" data-dropdown="{key}">'
            f'<div class="nav-dropdown-heading">'
            f'{anchor}'
            f'<button class="dropdown-toggle" type="button" aria-expanded="false" aria-controls="dropdown-{key}" aria-label="Toggle {escape(label)} submenu">'
            f'<svg class="dropdown-chevron" viewBox="0 0 12 12" aria-hidden="true"><path d="m3 4.5 3 3 3-3"/></svg>'
            f'</button>'
            f'</div>'
            f'<div class="dropdown-panel" id="dropdown-{key}" aria-label="{escape(label)} menu">'
            f'<div class="dropdown-content">'
            + ''.join(rows) +
            f'</div>'
            f'</div>'
            f'</div>'
        )

    current_quote = ' aria-current="page"' if page == 'quotation' else ''
    logo_path = base_path + 'assets/media/profile/company-logo.png'
    home_link = base_path + 'index.html'

    return (
        '<header class="header">'
        '<div class="header-inner">'
        f'<a class="brand profile-logo" href="{home_link}" aria-label="Techno Industries home">'
        f'<img src="{logo_path}" width="525" height="66" alt="Techno Industries">'
        '</a>'
        '<nav id="navigation" aria-label="Main navigation">'
        + ''.join(items) +
        f'<a class="button nav-quote mobile-quote" href="{base_path}quotation.html"{current_quote}>Request a Quote</a>'
        '</nav>'
        '<div class="header-actions">'
        f'<a class="button nav-quote" href="{base_path}quotation.html"{current_quote}>Request a Quote</a>'
        '<button class="menu-toggle" type="button" aria-controls="navigation" aria-expanded="false" aria-label="Toggle menu">'
        '<span class="menu-icon" aria-hidden="true"><span></span><span></span><span></span></span>'
        '</button>'
        '</div>'
        '</div>'
        '</header>'
    )

def render_footer(base_path=""):
    return (
        '<footer class="site-footer" id="site-footer" aria-label="Company information">\n'
        '  <div class="container sf-directory">\n'
        '    <div class="sf-brand">\n'
        f'      <a class="sf-logo" href="{base_path}index.html" aria-label="Techno Industries home">\n'
        f'        <img src="{base_path}assets/media/profile/company-logo.png" width="525" height="66" alt="Techno Industries" loading="lazy" decoding="async">\n'
        '      </a>\n'
        '      <p class="sf-summary">Value-added corrugated packaging for local and international markets.</p>\n'
        '      <p class="sf-affiliation">A strategic arm of Techno Group.</p>\n'
        '    </div>\n'
        '    <section class="sf-column sf-company" aria-labelledby="sf-company-title">\n'
        '      <h2 id="sf-company-title">Company</h2>\n'
        '      <nav class="sf-links" aria-labelledby="sf-company-title">\n'
        '        <ul>\n'
        f'          <li><a href="{base_path}index.html">Home</a></li>\n'
        f'          <li><a href="{base_path}about.html">About Us</a></li>\n'
        f'          <li><a href="{base_path}industries.html">Industries We Serve</a></li>\n'
        f'          <li><a href="{base_path}quality.html">Quality &amp; Certifications</a></li>\n'
        f'          <li><a href="{base_path}contact.html">Contact Us</a></li>\n'
        '        </ul>\n'
        '      </nav>\n'
        '    </section>\n'
        '    <section class="sf-column sf-packaging" aria-labelledby="sf-packaging-title">\n'
        '      <h2 id="sf-packaging-title">Packaging solutions</h2>\n'
        '      <nav class="sf-links" aria-labelledby="sf-packaging-title">\n'
        '        <ul>\n'
        f'          <li><a href="{base_path}products.html">Products &amp; Packaging</a></li>\n'
        f'          <li><a href="{base_path}products.html#corrugated">Corrugated Packaging</a></li>\n'
        f'          <li><a href="{base_path}products.html#printed">Printed Packaging</a></li>\n'
        f'          <li><a href="{base_path}products.html#custom">Custom Structures</a></li>\n'
        f'          <li><a href="{base_path}capabilities.html">Manufacturing Capabilities</a></li>\n'
        '        </ul>\n'
        '      </nav>\n'
        '    </section>\n'
        '    <section class="sf-column sf-contacts" aria-labelledby="sf-contact-title">\n'
        '      <h2 id="sf-contact-title">Get in touch</h2>\n'
        '      <div class="sf-contact-row">\n'
        '        <svg viewBox="0 0 24 24" aria-hidden="true"><path d="m7 3 3 5-2.5 2.5a15 15 0 0 0 6 6L16 14l5 3v3a1 1 0 0 1-1 1C10.6 21 3 13.4 3 4a1 1 0 0 1 1-1h3Z"/></svg>\n'
        '        <div><a href="tel:+94382257170">+94 38 225 7170</a><a href="tel:+94777777648">+94 777 777 648</a></div>\n'
        '      </div>\n'
        '      <div class="sf-contact-row">\n'
        '        <svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="1"/><path d="m3 6 9 7 9-7"/></svg>\n'
        '        <a href="mailto:info@technoind.biz">info@technoind.biz</a>\n'
        '      </div>\n'
        '      <address class="sf-contact-row sf-address">\n'
        '        <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M20 10c0 6-8 12-8 12S4 16 4 10a8 8 0 1 1 16 0Z"/><circle cx="12" cy="10" r="3"/></svg>\n'
        '        <span>227/1, Ghanarathana Mw,<br>Raigama, Bandaragama,<br>Sri Lanka.</span>\n'
        '      </address>\n'
        '    </section>\n'
        '  </div>\n'
        '  <div class="sf-bottom">\n'
        '    <div class="container sf-bottom-layout">\n'
        '      <p class="sf-copyright">© <span id="year">2026</span> Techno Industries. All rights reserved.</p>\n'
        '      <p class="sf-credit">Website developed by <span>Nexora Digital Solutions</span></p>\n'
        '    </div>\n'
        '  </div>\n'
        '</footer>'
    )
