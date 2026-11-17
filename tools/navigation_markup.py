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
