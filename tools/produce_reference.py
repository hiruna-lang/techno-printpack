from pathlib import Path
import re
root=Path(__file__).resolve().parents[1]
p=root/'farm/produce.html';s=p.read_text(encoding='utf-8')
leaf='<svg viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M16 29V14m0 7C5 21 3 10 3 5c9 0 13 6 13 13m0 0C16 8 22 4 29 3c0 10-4 16-13 17"/></svg>'
hero='''<section class="produce-hero"><img src="../images/Farm/farm-2.jpg" alt="Lush fruit trees across our plantation in Thanamalwila" fetchpriority="high"><div class="container"><div class="produce-hero-copy"><p class="produce-breadcrumb"><a href="index.html" aria-label="Home">&#8962;</a><span>/</span> Our Produce</p><h1>Our <em>Produce</em></h1><p>A diverse range of premium, naturally grown<br>fruits from our own plantations in Sri Lanka.</p></div><div class="fresh-seal">'''+leaf+'''<strong>FARM<br>FRESH</strong><span>NATURALLY<br>GROWN</span></div></div><svg class="produce-wave" viewBox="0 0 1440 80" preserveAspectRatio="none" aria-hidden="true"><path d="M0 30C210 100 330 2 610 32S1080 92 1440 0V80H0Z" fill="#91b862"/><path d="M0 49C210 112 330 15 610 43S1080 103 1440 21V80H0Z" fill="#fcfbf7"/></svg></section>'''
def benefit_icon(content):
 return '<svg viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'+content+'</svg>'
benefit_icons=[
 benefit_icon('<path d="M16 29V15M16 22C7 22 4 15 4 7c8 0 12 5 12 12M16 18C16 9 22 5 28 4c0 9-4 15-12 16M7 29h18"/>'),
 benefit_icon('<path d="m11 20-3 10 8-4 8 4-3-10"/><path d="m16 2 3 2 4 .5 1 4 2 3-2 3-1 4-4 .5-3 2-3-2-4-.5-1-4-2-3 2-3 1-4 4-.5Z"/><path d="m12 11 3 3 5-6"/>'),
 benefit_icon('<path d="M3 21h5l5-4h5a3 3 0 0 1 0 6h-4m-6-2 4 7h10l7-8a2 2 0 0 0-3-3l-5 4M3 19v10h5V19ZM18 17V9m0 4C11 13 10 8 10 4c6 0 8 4 8 7m0-2c0-5 4-7 9-7 0 6-3 10-9 10"/>'),
 benefit_icon('<path d="M2 7h17v17H2ZM19 13h6l5 6v5H19M25 13v7h5M5 12h9M5 16h6"/><circle cx="8" cy="25" r="3" fill="var(--cream)"/><circle cx="25" cy="25" r="3" fill="var(--cream)"/>')
]
features='<section class="produce-why"><h2>Why Choose Our Produce?</h2><div class="produce-benefits container">'+''.join('<div>'+icon+'<span>'+label+'</span></div>' for icon,label in zip(benefit_icons,['Grown on Our<br>Own Plantation','Consistent<br>Quality','Sustainable<br>Farming','Reliable<br>Supply']))+'</div></section>'
items=[('mango','TJC Mango','../assets/media/farm-IMG_4602-1600.webp','Our signature and most demanded fruit.',['Rich, sweet flavour','Deep golden colour','Carefully harvested']),('banana','Banana','../assets/media/farm-e08deeab-45b5-410c-91d2-98eb3c74b2b3-1600.webp','High demand in both local and export markets.',['Fresh from our plantation','Carefully selected bunches','Grown under monitored conditions']),('woodapple','Woodapple','../images/Farm/farm-6.jpg','A naturally grown Sri Lankan favourite with a unique flavour.',['Fresh and natural','Ideal for juice and processing','Distinctive flavour and aroma']),('papaya','Papaya','../assets/media/farm-fc7a4243-c253-4005-9ec3-8fcb1f105234-1600.webp','Quality papaya grown with care on our plantation.',['Vibrant colour','Naturally sweet flavour','For fresh markets and processing'])]
items.sort(key=lambda item: ['banana','mango','woodapple','papaya'].index(item[0]))
cards=''
for id,title,img,desc,points in items:
 cards+=f'<article class="fruit-detail" id="{id}"><img src="{img}" alt="{title} from Green Techno Farm" loading="lazy" decoding="async"><div class="fruit-detail-copy"><h3>{leaf}{title}</h3><p>{desc}</p><ul>'+''.join(f'<li>{point}</li>' for point in points)+f'</ul><a class="button" href="contact.html?produce={id}">Request Product Details <span aria-hidden="true">&#8594;</span></a></div></article>'
main='<section class="premium-produce container"><div class="produce-title"><p class="eyebrow">OUR RANGE</p><h2>Premium Fruits from <em>Our Plantations</em></h2><p>Nutritious, flavor-rich and responsibly cultivated fruits, grown with care across our 100+ acre farm.</p></div><div class="fruit-detail-grid">'+cards+'</div></section>'
extra='<section class="additional-produce"><h2>Additional Produce</h2><div class="additional-grid">'+''.join(f'<article><img src="{img}" alt="{title}" loading="lazy" decoding="async"><div>{leaf}<h3>{title}</h3><p>{desc}</p></div></article>' for title,img,desc in [('Capsicum / Pepper','../images/Farm/07f7e1dc-9e69-475e-abd7-b1261aec65c1.jpeg','Fresh, quality produce from our plantation.'),('Citrus (Lime)','../images/Farm/farm-8.jpg','Naturally grown with refreshing flavour.'),('Tamarind','../images/Farm/3fb493d3-c47f-4b1f-b84f-c0d8c3741d56.jpeg','Farm-fresh tamarind with natural quality.')])+'</div></section>'
cta='<section class="produce-enquiry"><div class="enquiry-leaf">'+leaf+'</div><div><h2>Partner With Us for Fresh Produce</h2><p>Connect with our team to discuss availability, supply and collaboration opportunities.</p></div><a class="button yellow" href="contact.html">Get in Touch <span aria-hidden="true">&#8594;</span></a></section>'
s=re.sub(r'<main id="main">.*?</main>', '<main id="main">'+hero+main+features+cta+'</main>',s,flags=re.S)
s=re.sub(r'</main><section class="cta">.*?</section><footer>','</main><footer>',s,flags=re.S)
s=s.replace('<body>','<body class="page-farm-produce">')
if 'farm-produce.css' not in s:s=s.replace('</head>','<link rel="stylesheet" href="../assets/css/farm-produce.css"></head>')
# Keep the hero promises within the image, as in the supplied reference.
hero_points='<div class="hero-promises">'+''.join('<div>'+leaf+'<span>'+label+'</span></div>' for label in ['Naturally<br>Grown','Premium<br>Quality','Farm<br>Fresh'])+'</div>'
s=s.replace('</p></div><div class="fresh-seal">', '</p>'+hero_points+'</div><div class="fresh-seal">')
p.write_text(s,encoding='utf-8')
