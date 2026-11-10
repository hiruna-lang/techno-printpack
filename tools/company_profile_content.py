"""Apply the user-approved company profile as the packaging site's content source.

Loaded last by build_site.py, preserving the current page designs and Farm links.
Source: Technopack 2.pdf, 13 pages. See COMPANY-CONTENT-AUDIT.md.
"""
import re
from urllib.parse import quote as urlquote,unquote
profile=json.loads((R/'assets/data/company-profile.json').read_text(encoding='utf-8'))

def profile_photo(filename,alt):
 path=R/f'assets/media/profile/{filename}.webp'
 w,h=Image.open(path).size
 return f'<img src="assets/media/profile/{filename}.webp" alt="{alt}" width="{w}" height="{h}" loading="lazy" decoding="async">'

def facts_list(values):return '<ul>'+''.join(f'<li>{html.escape(v)}</li>' for v in values)+'</ul>'

def profile_cta():return '<section class="cta section"><div class="container"><div>'+label('PACKAGING FOR YOUR BUSINESS')+'<h2>Discuss your packaging requirements.</h2><p>Share your product, dimensions, quantity and print requirements.</p></div>'+btn('Request a quotation','quotation.html')+'</div></section>'

# Keep local company/Farm navigation changes in generated output.
dropdowns['industries']=[('index.html','Techno Industries'),(None,'Grand Techno'),('farm/index.html','Green Techno Farm')]
dropdowns['about']=[(url,'Vision & Commitments' if url=='about.html#principles' else label) for url,label in dropdowns['about']]
previous_brand=brand
def brand(white=False):
 return '<a class="brand profile-logo" href="index.html" aria-label="Techno Industries home"><img src="assets/media/profile/company-logo.png" width="525" height="66" alt="Techno Industries"></a>'
footer=footer.replace(previous_brand(True),brand(True))

# Products: every product on profile page 7, with PVC detail from page 11.
write('assets/media/wooden-box.svg','<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 320"><ellipse cx="205" cy="278" rx="125" ry="13" fill="#09283c" opacity=".06"/><g stroke="#805e3f" stroke-width="2" stroke-linejoin="round"><path d="m85 112 118-54 120 56-120 57Z" fill="#d9b787"/><path d="m85 112 118 59v101L85 213Z" fill="#bd9565"/><path d="m203 171 120-57v99l-120 59Z" fill="#a67c50"/><path d="m85 146 118 58 120-58m-238 33 118 58 120-58" fill="none"/><path d="m105 126 14 7v85l-14-7Zm61 30 14 7v85l-14-7Z" fill="#e2c297"/><path d="m223 161 13-6v85l-13 6Zm60-28 13-6v85l-13 6Z" fill="#c9a577"/></g></svg>')

def product_visual(product):
 visual=product['visual'];name=product['name']
 if isinstance(visual,int):return img(visual,f'{name} — company production photograph'),False,'Company production'
 if visual.startswith('diagram-'):
  return f'<img src="assets/media/carton-{visual[8:]}.svg" width="400" height="320" alt="Structure illustration for {name}" loading="lazy">',True,'Structure illustration'
 if visual=='material-wood':return '<img src="assets/media/wooden-box.svg" width="400" height="320" alt="Illustration of a wooden packing box" loading="lazy">',True,'Structure illustration'
 return profile_photo(visual,f'{name} example shown in the company profile'),True,'Company profile example'

def product_card(product):
 visual,contain,note=product_visual(product)
 categories=product['category']+(' printed' if product['name']=='Value-Added Corrugated Boxes' else '')
 return f'<article class="product-card catalogue-card" data-category="{product["category"]}" data-categories="{categories}"><a href="quotation.html?type={urlquote(product["name"])}" aria-label="Request a quotation for {product["name"]}"><div class="catalogue-card-image {"is-illustration" if contain else ""}">{visual}<span class="catalogue-image-note">{note}</span></div><div class="catalogue-card-copy"><i data-lucide="{product["icon"]}" aria-hidden="true"></i><div><h3>{product["name"]}</h3><p>{product["description"]}</p></div><span class="catalogue-arrow" aria-hidden="true">→</span></div></a></article>'

product_hero=f'<section class="catalogue-hero"><div class="catalogue-hero-photo">{img(1529,"Corrugated materials at Techno Industries",eager=True)}</div><div class="catalogue-hero-angle"></div><div class="container"><div>{label("OUR PRODUCTS")}<h1>Corrugated Packaging.<br>And More.</h1><p>Explore our complete range of corrugated, handmade, recycled, gift, wooden and PVC packaging.</p><div class="catalogue-breadcrumb" aria-label="Breadcrumb"><a href="index.html"><i data-lucide="house" aria-hidden="true"></i>Home</a><span>›</span><span>Products</span></div></div></div></section>'
product_filters=[('all','package','All Products'),('corrugated','layers','Corrugated & Industrial'),('printed','printer','Printed Packaging'),('custom','scan-line','Die-Cut'),('food','carrot','Food & Produce'),('specialty','gift','Handmade, Gift & Wooden'),('pvc','box','PVC')]
product_body=product_hero+'<section class="catalogue-body"><div class="container"><div class="filters catalogue-filters" aria-label="Filter packaging categories">'+''.join(f'<button type="button" data-filter="{key}" aria-pressed="{str(key=="all").lower()}"><i data-lucide="{icon}" aria-hidden="true"></i>{title}</button>' for key,icon,title in product_filters)+'</div><div class="catalogue-heading"><div>'+label('OUR PACKAGING RANGE')+'<h2>Products for<br>Your Requirements</h2></div><p>Our company profile brings together ten product lines, supported by a range of board constructions, flute profiles and structural formats.</p></div><p class="result-count" aria-live="polite"></p><div class="product-grid catalogue-grid">'+''.join(product_card(p) for p in profile['products'])+'</div><p class="empty-state" hidden>No packaging matches this selection. Choose another category or contact the team.</p><p class="profile-image-note">Images show company production, examples from the company profile or labelled structure illustrations. Final specifications are agreed for your product.</p></div></section>'
product_body+='''<section class="profile-range-section"><div class="container"><div class="profile-section-heading">'''+label('CORRUGATED BOX TYPES')+'''<h2>Choose the right structure.</h2><p>From shipping cartons to display formats, the company profile lists these structures.</p></div><div class="profile-tag-grid">'''+''.join(f'<a href="quotation.html?type={urlquote(name)}">{name}<span aria-hidden="true">↗</span></a>' for name in profile['structures'])+'''</div></div></section>'''
product_body+='''<section class="profile-range-section soft"><div class="container"><div class="profile-section-heading">'''+label('PVC PACKAGING')+'''<h2>Clear formats for presentation.</h2><p>PVC packaging is listed as a new product line in the company profile. Applications include retail, gifts, cosmetics and confectionery.</p></div><div class="profile-two-column"><div>'''+facts_list(profile['pvc'])+'''<p class="small">Food-grade PVC options are available upon requirement for dry foods and selected consumables. Confirm suitability for your application.</p></div><div class="profile-pvc-example">'''+profile_photo('pvc-box','Transparent PVC box example from the company profile')+'''</div></div></div></section>'''+profile_cta()
pages['products']=('Products & Packaging','Explore the Techno Industries range: corrugated, handmade, die-cut, food-grade produce, industrial, recycled, gift, wooden and PVC boxes.',product_body)

# About: the supplied company vision replaces the previous group paraphrase.
title,desc,body=pages['about']
company_copy='<div class="about-story" id="company-information">'+label('WHO WE ARE')+'<h2>Techno Industries</h2><p>'+profile['overview']+'</p><p>We serve exporters, manufacturers, supermarkets, plantations, retailers and logistics companies, with a commitment to continuous improvement, sustainability and strict quality control.</p>'+btn('Our Capabilities','capabilities.html')+'<p class="group-context">A strategic arm of <a href="#group">Techno Group.</a></p></div></div>'
body=re.sub(r'<div class="about-story"[^>]*>.*?</div></div>',lambda _:company_copy,body,count=1,flags=re.S)
principles='<div class="about-principles" id="principles"><article><i data-lucide="goal" aria-hidden="true"></i><div><h3>Our Vision</h3><p>'+profile['vision']+'</p></div></article><article><i data-lucide="layers" aria-hidden="true"></i><div><h3>Our Focus</h3><p>Quality, innovation and customer service underpin our value-added corrugated packaging solutions.</p></div></article><article><i data-lucide="gem" aria-hidden="true"></i><div><h3>Our Commitment</h3><ul>'+''.join(f'<li><i data-lucide="check" aria-hidden="true"></i>{item}</li>' for item in profile['commitments'])+'</ul></div></article></div>'
body=re.sub(r'<div class="about-principles"[^>]*>.*?(?=<details class="about-group")',lambda _:principles,body,count=1,flags=re.S)
body=re.sub(r'(<details class="about-group" id="why-us">).*?</details>',lambda m:m[1]+'<summary>Why Choose Techno Industries <span aria-hidden="true">+</span></summary><p>Our strength lies in combining technical expertise, advanced manufacturing technology and food-grade certified materials. The product range covers corrugated and die-cut packaging as well as handmade, recycled, gift, wooden and PVC boxes.</p><a class="text-link" href="products.html">Explore the product range <span>↗</span></a></details>',body,count=1,flags=re.S)
body=re.sub(r'(<details class="about-group" id="group">).*?</details>',lambda m:m[1]+'<summary>Part of Techno Group <span aria-hidden="true">+</span></summary><p>The corporate group comprises Techno Industries, Grand Techno and Green Techno Farm.</p><a class="text-link" href="farm/index.html">Explore Green Techno Farm <span>↗</span></a></details>',body,count=1,flags=re.S)
body=body.replace('From material selection to printing and finishing, define the details that matter for your product. Discuss dimensions, structure and quality requirements with our team.','Technical expertise, manufacturing technology, food-grade certified materials and strict quality control support the durability, structural integrity and presentation of our packaging.')
pages['about']=('About Us','Techno Industries is an ISO-certified manufacturer of value-added corrugated packaging and a strategic arm of Techno Group.',body)

# Industries: replace previous generic sectors with the profile's exact list.
industry_details=[
 ('tea','leaf','Tea','Packaging for tea producers and exporters.',['Carton and board structure','Print and brand presentation','Storage and distribution needs']),
 ('garments','shirt','Garments','Packaging for garments and apparel products.',['Product arrangement and dimensions','Carton opening and handling','Branding and product information']),
 ('porcelain','coffee','Porcelain','Packaging for porcelain products and fragile items.',['Internal supports and partitions','Product weight and arrangement','Handling requirements']),
 ('automobile','car','Automobile','Packaging for automobile products and components.',['Component dimensions and weight','Structural strength','Dividers and protective arrangements']),
 ('foods-beverages','utensils','Foods & Beverages','Packaging for food and beverage applications.',['Food-grade material requirements','Product-contact suitability','Moisture and storage conditions']),
 ('medicine-fertilizer','flask-conical','Medicine & Fertilizer','Packaging requirements for medicine and fertilizer sectors.',['Material suitability for the contents','Product identification and printing','Specific handling requirements']),
 ('dairy-livestock','milk','Dairy & Livestock','Packaging for dairy and livestock-related products.',['Material and board selection','Moisture and storage conditions','Transport and handling']),
 ('seafood','fish','Seafood','Packaging for seafood and associated distribution needs.',['Moisture-resistant board options','Cold-chain requirements','Transit and storage conditions'])]
industry_body=hero('INDUSTRIES WE SERVE','Packaging across industries.','Purpose-built packaging for the sectors named in our company profile.',1554)
industry_body+='<section class="section"><div class="container"><div class="section-heading"><div>'+label('INDUSTRIES WE SERVE')+'<h2>Eight sectors.<br>Product-specific requirements.</h2></div><p>Discuss the product, environment and handling conditions with our team to identify suitable materials and structures.</p></div><div class="sector-grid">'
for key,icon,name,description,points in industry_details:
 industry_body+=f'<article id="{key}"><i data-lucide="{icon}" aria-hidden="true"></i><h3>{name}</h3><p>{description}</p><h4>What to discuss</h4>'+facts_list(points)+'<a class="text-link" href="quotation.html">Discuss your requirements <span>↗</span></a></article>'
industry_body+='</div></div></section>'+profile_cta()
pages['industries']=('Industries We Serve','Techno Industries serves tea, garments, porcelain, automobile, foods and beverages, medicine and fertilizer, dairy and livestock, and seafood sectors.',industry_body)

# Capabilities: retain the approved four-card layout and publish the actual options.
title,desc,body=pages['capabilities']
capability_updates={
 'Explore printing, die-cutting, custom structures and finishing options for your packaging requirements.':'From flexographic and offset printing to die-cutting, OP varnish and UV lamination: explore our packaging capabilities.',
 'Flexographic printing is listed in one to four colours. Share your artwork, colour requirements and print placement so the team can review a suitable approach.':'Our printing capabilities include flexographic printing in 1–4 colours, offset printing, high-quality line printing and retail-grade multi-colour printing. Food-safe inks are available for produce and FMCG packaging.',
 'Printing options for your brand and product information.':'Flexographic, offset, line and multi-colour printing.',
 'Die-cut packaging can be discussed around the product and opening style. Include your dimensions, assembly preferences and any handle or ventilation requirements.':'Die-cut corrugated boxes, custom shapes, perforations, ventilation holes and punch / handle structures support a range of packaging applications.',
 'Explore carton structures, dividers and custom inserts. Share the internal arrangement, product weight and handling requirements to define the packaging brief.':'Explore RSC and HSC cartons, wrap-arounds, telescopic and self-locking boxes, partitioned boxes, punch / handle boxes, pallet / bulk boxes and display boxes / racks.',
 'The published offering includes coatings, perforations and finish options. Availability and suitability are confirmed for the selected materials and application.':'Surface options include OP varnish, UV lamination and UV matte lamination. Structural enhancements include die-cutting, perforations, ventilation holes and reinforced edges and corners.',
 'Presentation and functional details for the final package.':'OP varnish, UV lamination and structural enhancements.',
 'A Complete<br>Packaging Conversation':'Corrugated Materials.<br>Print. Structure. Finish.'}
for old,new in capability_updates.items():body=body.replace(old,new)
technical='<section class="profile-technical" id="materials"><div class="profile-section-heading">'+label('FLUTE TYPES')+'<h2>Six flute options.</h2><p>Flute profiles listed in the company profile for print, cushioning and structural requirements.</p></div><div class="profile-spec-grid">'+''.join(f'<article><h3>{p["name"]}</h3><p>{p["description"]}</p></article>' for p in profile['flutes'])+'</div><div class="profile-section-heading profile-heading-space">'+label('BOARD TYPES')+'<h2>Board construction and materials.</h2></div><div class="profile-spec-grid">'+''.join(f'<article><h3>{p["name"]}</h3><p>{p["description"]}</p></article>' for p in profile['boards'])+'</div><div class="profile-finishing-grid profile-heading-space"><div>'+label('SURFACE FINISHES')+'<h3>Protect and present.</h3>'+facts_list(profile['surface_finishes'])+'</div><div>'+label('STRUCTURAL ENHANCEMENTS')+'<h3>Function and strength.</h3>'+facts_list(profile['structural_finishes'])+'</div></div></section>'
body=body.replace('<section class="capability-cta">',technical+'<section class="capability-cta">')
pages['capabilities']=('Manufacturing Capabilities','Techno Industries offers F, E, B, C, BC and EB flutes; 3-, 5- and 7-ply boards; flexographic and offset printing; OP varnish and UV lamination.',body)

# Quality: the profile supplies the certification/material statements that were missing.
title,desc,body=pages['quality']
quality_updates={
 'Quality Packaging<br>Starts with the Details':'ISO-Certified<br>Packaging Manufacturing',
 'Define the materials, structure, dimensions and print requirements for packaging that suits your product.':'Quality, innovation and customer service support our value-added corrugated packaging for local and international markets.',
 'Consistent Requirements':'Strict Quality Control',
 'Material Suitability':'Food-Grade Materials',
 'Clear Specifications':'Technical Expertise',
 'Responsible Choices':'Sustainability',
 'A Structured Quality Conversation':'Quality, Materials and Continuous Improvement',
 'Agree what matters before production: the board, fit, artwork and functional requirements. Use the following checkpoints to build your packaging specification with our team.':'Our company profile identifies strict quality control, continuous improvement and food-grade certified materials as part of our manufacturing approach. Discuss the following specification checkpoints with our team.',
 'Test methods, tolerances and acceptance criteria are confirmed for your project; no particular test or inspection programme is assumed.':'Confirm the test methods, tolerances and acceptance criteria required for your particular product and order.',
 'Certification Documents':'ISO 9001:2015',
 'The company website describes Techno Industries as ISO-certified. Request current certificates and confirm the covered entity, site, scope and validity. Current documents have not been verified for publication here.':'Techno Industries is described as an ISO-certified manufacturer in the company profile, which displays ISO 9001:2015. Request the applicable certificate and its scope from our team.',
 'Share product-contact, moisture, handling or other material requirements. Ask for documentation applicable to the selected material and intended use.':'The company profile states that food-grade certified materials are used in production. Food-grade boards, produce packaging and food-safe inks are included in the range. Food-grade PVC options are available upon requirement.',
 'Discuss the dimensions, artwork, structural requirements and acceptance criteria for your order. Confirm any required test methods and supporting results directly.':'Strict quality control and continuous improvement are stated commitments. Discuss dimensions, structural integrity, artwork and product presentation requirements for your order.',
 'Discuss material selection and resource considerations with the team. Request product-specific evidence for any environmental claim required by your project.':'The company profile includes a commitment to sustainability and lists recycled boxes among its products. Discuss the material choice and any required product-specific documentation with the team.',
 'Certification and compliance documents are available to request from the team. No certification badge, test result or environmental certification is presented as verified on this page.':'ISO 9001:2015 and food-grade material statements are presented in the supplied company profile. Contact the team for the applicable certificates, scope and product-specific documentation.',
 'Confirm the Standards<br>for Your Project':'Certification and<br>Material Standards'}
for old,new in quality_updates.items():body=body.replace(old,new)
profile_marks=[('iso-mark','ISO 9001:2015','Quality management'),('food-grade-mark','Food Grade','Food-grade material mark'),('edb-mark','Export Development Board','Organization logo'),('cea-mark','Central Environmental Authority','Organization logo')]
marks_section='<section class="profile-marks-section" aria-labelledby="profile-marks-title"><div class="container">'+label('COMPANY PROFILE MARKS')+'<div class="profile-marks-heading"><h2 id="profile-marks-title">Quality &amp; industry marks</h2><p>Marks featured in our company profile. Contact our team for current certificates and supporting documentation.</p></div><div class="profile-marks-grid">'+''.join('<figure><div>'+profile_photo(filename,title+' mark from the company profile')+'</div><figcaption><strong>'+title+'</strong><span>'+description+'</span></figcaption></figure>' for filename,title,description in profile_marks)+'</div><p class="profile-marks-note">The EDB and Central Environmental Authority logos identify organizations shown in the profile; they are not presented as certification or membership claims.</p></div></section>'
body=body.replace('<section class="quality-standards"',marks_section+'<section class="quality-standards"',1)
body=body.replace('Certification and documentation','Certification and documentation')
pages['quality']=('Quality & Certifications','Techno Industries company profile identifies ISO-certified manufacturing, ISO 9001:2015, food-grade certified materials, strict quality control and continuous improvement.',body)

# Homepage: preserve the reference design, replace generic sectors and options.
title,desc,body=pages['index']
body=body.replace('Corrugated boxes, custom packaging and print solutions for a wide range of industries.','Value-added corrugated packaging, printed boxes and custom solutions for local and international markets.')
body=body.replace('From concept to<br>production.','From corrugated board<br>to finished packaging.')
body=body.replace('Bring structure, print and finishing into one conversation. Explore the options for your packaging requirements.','Flexographic and offset printing, die-cutting, OP varnish and UV lamination support your packaging requirements.')
body=body.replace('Agree the board, dimensions, print and quality criteria for your application with our team.','ISO-certified manufacturing, food-grade certified materials and strict quality control support our packaging solutions.')
industry_preview='<section class="ref-industries" id="industries"><div class="container industries-layout profile-industry-preview"><div class="ref-section-intro">'+label('INDUSTRIES WE SERVE')+'<h2>Packaging across<br>eight sectors.</h2><a class="ref-text-link" href="industries.html">Explore industries <span>→</span></a><span class="accent-rule"></span></div>'+''.join(f'<article><i data-lucide="{icon}" aria-hidden="true"></i><h3>{name}</h3></article>' for _,icon,name,_,_ in industry_details)+'</div></section>'
body=re.sub(r'<section class="ref-industries".*?</section>',lambda _:industry_preview,body,count=1,flags=re.S)
body=body.replace('Board and carton options for transport applications.','Standard corrugated boards and boxes for packaging and transport.').replace('Export Packaging</h3>','Standard Corrugated</h3>')
hero_video='<div class="ref-hero-photo"><video class="hero-video" autoplay muted loop playsinline preload="metadata" poster="assets/video/techno-industries-hero-poster.webp" aria-label="Techno Industries manufacturing and packaging"><source src="assets/video/techno-industries-hero.mp4" type="video/mp4">Your browser does not support background video.</video><button class="hero-autoplay-toggle hero-video-toggle" type="button" aria-label="Pause manufacturing video" hidden>?</button></div>'
body=re.sub(r'<div class="ref-hero-photo">.*?</div>',lambda _:hero_video,body,count=1,flags=re.S)
pages['index']=('Value-Added Corrugated Packaging','Techno Industries manufactures value-added corrugated packaging, with food-grade materials, flexographic and offset printing, custom structures and finishing options.',body)

# The quote builder uses the same approved product and structure names as the catalogue.
approved_types=[p['name'] for p in profile['products']]+profile['structures']+['Printed Packaging']+profile['pvc']
options='<option value="">Select packaging type</option>'+''.join(f'<option>{html.escape(name)}</option>' for name in approved_types)+'<option>Other / need advice</option>'
title,desc,body=pages['quotation']
body=re.sub(r'(<select id="type"[^>]*>).*?(</select>)',lambda m:m[1]+options+m[2],body,count=1,flags=re.S)
preferences='<div class="field full"><label for="flute">Preferred flute (optional)</label><select id="flute" name="flute"><option value="">Please advise</option>'+''.join(f'<option>{p["name"]}</option>' for p in profile['flutes'])+'</select></div><div class="field full"><label for="board">Preferred board (optional)</label><select id="board" name="board"><option value="">Please advise</option>'+''.join(f'<option>{p["name"]}</option>' for p in profile['boards'])+'</select></div><div class="field full"><label for="finish">Preferred surface finish (optional)</label><select id="finish" name="finish"><option value="">Please advise</option>'+''.join(f'<option>{name}</option>' for name in profile['surface_finishes'])+'</select></div>'
body=body.replace('<div class="field full"><label for="printing">',preferences+'<div class="field full"><label for="printing">')
pages['quotation']=('Request a Quote','Prepare a Techno Industries enquiry with product type, quantity, dimensions, flute, board, printing and finishing requirements.',body)

# Contact: all three profile email addresses, retaining the existing verified numbers.
title,desc,body=pages['contact']
body=body.replace('<a href="mailto:info@technoind.biz">info@technoind.biz</a></div></div>', '<a href="mailto:info@technoind.biz">info@technoind.biz</a><a class="contact-secondary" href="mailto:sampath@technoind.biz">sampath@technoind.biz</a><a class="contact-secondary" href="mailto:gayani@technoind.biz">gayani@technoind.biz</a></div></div>')
pages['contact']=(title,'Contact Techno Industries at 227/1, Ghanarathana Mw, Raigama, Bandaragama. Telephone +94 38 225 7170; mobile +94 777 777 648.',body)

# Correct legacy enquiry links to the profile's product and structure names.
legacy_types={'Regular slotted cartons':'Regular Slotted Cartons (RSC)','Printed corrugated packaging':'Printed Packaging','Die-cut boxes':'Die-Cut Corrugated Boxes','Double-wall cartons':'Standard Corrugated Boards & Boxes','Partitioned packaging':'Partitioned Boxes','PVC packaging':'PVC Boxes'}
def correct_quote_link(match):
 value=unquote(html.unescape(match[1]));return 'href="quotation.html?type='+urlquote(legacy_types.get(value,value))+'"'
# Correct the company identity consistently while preserving the deployed domain.
for key,(title,desc,body) in list(pages.items()):
 for old,new in [('Techno Printpack','Techno Industries'),('TECHNO PRINTPACK','TECHNO INDUSTRIES')]:
  title=title.replace(old,new);desc=desc.replace(old,new);body=body.replace(old,new)
 body=re.sub(r'href="quotation\.html\?type=([^"]+)"',correct_quote_link,body)
 pages[key]=(title,desc,body)
footer=footer.replace('Techno Printpack','Techno Industries')
footer=footer.replace('<p>Corrugated, printed and custom packaging<br>for the products your business makes.</p>','<p>Value-added corrugated packaging<br>for local and international markets.</p>')
