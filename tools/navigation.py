"""One company-information dropdown; other navigation items are direct links."""
dropdowns={
 'about':[('about.html#company-information','Company Information'),('about.html#why-us','Why Choose Us'),('about.html#principles','Vision, Mission & Values'),('quality.html#certifications','Certifications & Documentation')],
 'industries':[('index.html','Techno Industries'),(None,'Grand Techno'),(None,'Techno Farm')]}
short_labels['about']='About Us'
def header(page):
 links=[]
 for key,title in page_labels:
  if key=='quotation':continue
  active=' aria-current="page"' if key==page else ''
  anchor=f'<a href="{key}.html" title="{title}"{active}>{short_labels[key]}</a>'
  if key in dropdowns:
   children=''.join((f'<button type="button" class="company-option">{label}</button>' if url is None else '<a '+('class="company-option" ' if key=='industries' else '')+f'href="{url}"'+(' aria-current="page"' if page==key and url==key+'.html' else '')+f'>{label}</a>') for url,label in dropdowns[key])
   links.append(f'<div class="nav-dropdown"><div class="nav-dropdown-heading">{anchor}<button class="dropdown-toggle" type="button" aria-expanded="false" aria-controls="dropdown-{key}" aria-label="Show {short_labels[key]} pages"><svg viewBox="0 0 16 16" aria-hidden="true"><path d="m4 6 4 4 4-4"/></svg></button></div><div class="dropdown-panel" id="dropdown-{key}" aria-label="{short_labels[key]} pages">{children}</div></div>')
  else:links.append(anchor)
 return '<a class="skip" href="#main">Skip to content</a><div class="utility-bar"><div class="container"><span>Packaging Manufacturing · Sri Lanka</span><div><a href="mailto:info@technoind.biz"><i data-lucide="mail" aria-hidden="true"></i>info@technoind.biz</a><a href="tel:+94382257170"><i data-lucide="phone" aria-hidden="true"></i>+94 38 225 7170</a></div></div></div><header class="header"><div class="header-inner">'+brand()+'<button class="menu-toggle" aria-controls="navigation" aria-expanded="false">Menu <i data-lucide="menu" aria-hidden="true"></i></button><nav id="navigation" aria-label="Main navigation">'+''.join(links)+f'<a class="button" href="quotation.html"'+(' aria-current="page"' if page=='quotation' else '')+'>Request a Quote <span aria-hidden="true">↗</span></a></nav></div></header>'
title,desc,body=pages['about']
body=body.replace('<div class="about-principles">','<div class="about-principles" id="principles">').replace('<div class="about-story">','<div class="about-story" id="company-information">')
body=body.replace('<details class="about-group" id="group">','<details class="about-group" id="why-us"><summary>Why Choose Techno Printpack <span aria-hidden="true">+</span></summary><p>Explore corrugated cartons, printed packaging, die-cut structures and PVC options with one team. Share your dimensions, artwork and handling requirements to review the structure, materials and finish together.</p><a class="text-link" href="capabilities.html">Explore our manufacturing capabilities <span>↗</span></a></details><details class="about-group" id="group">')
pages['about']=(title,desc,body)
