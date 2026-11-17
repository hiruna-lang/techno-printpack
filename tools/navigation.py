"""Shared header renderer, with compatibility hooks for the content layers."""
dropdowns={
 'about':[('about.html#company-information','Company Information'),('about.html#why-us','Why Choose Us'),('about.html#principles','Vision, Mission & Values'),('quality.html#certifications','Certifications & Documentation')],
 'industries':[('index.html','Techno Industries'),(None,'Grand Techno'),(None,'Techno Farm')]}
short_labels['about']='About Us'
exec(compile((R/'tools/navigation_markup.py').read_text(encoding='utf-8'),str(R/'tools/navigation_markup.py'),'exec'),globals())

def header(page):
 return '<a class="skip" href="#main">Skip to content</a><div class="utility-bar"><div class="container"><span>Packaging Manufacturing · Sri Lanka</span><div><a href="mailto:info@technoind.biz"><i data-lucide="mail" aria-hidden="true"></i>info@technoind.biz</a><a href="tel:+94382257170"><i data-lucide="phone" aria-hidden="true"></i>+94 38 225 7170</a></div></div></div>'+render_header(page)
title,desc,body=pages['about']
body=body.replace('<div class="about-principles">','<div class="about-principles" id="principles">').replace('<div class="about-story">','<div class="about-story" id="company-information">')
body=body.replace('<details class="about-group" id="group">','<details class="about-group" id="why-us"><summary>Why Choose Techno Printpack <span aria-hidden="true">+</span></summary><p>Explore corrugated cartons, printed packaging, die-cut structures and PVC options with one team. Share your dimensions, artwork and handling requirements to review the structure, materials and finish together.</p><a class="text-link" href="capabilities.html">Explore our manufacturing capabilities <span>↗</span></a></details><details class="about-group" id="group">')
pages['about']=(title,desc,body)
