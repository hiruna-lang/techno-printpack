"""Remove the Gallery route and all public links to it."""
import re
pages.pop('gallery',None)
page_labels[:]=[(key,title) for key,title in page_labels if key!='gallery']
footer=re.sub(r'<a href="gallery\.html">.*?</a>','',footer)
for key,(title,desc,body) in list(pages.items()):
 if key=='index':body=re.sub(r'<section class="ref-gallery">.*?</section>','',body,flags=re.S)
 body=body.replace('href="gallery.html"','href="capabilities.html#capability-range"')
 body=body.replace('Explore our company and group photographs','Explore our manufacturing capabilities')
 pages[key]=(title,desc,body)
(R/'gallery.html').unlink(missing_ok=True)
