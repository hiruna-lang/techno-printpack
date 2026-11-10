from pathlib import Path
root=Path(__file__).resolve().parents[1]
p=root/'tools/build_site.py';s=p.read_text(encoding='utf-8')
hook="exec(compile((R/'tools/company_profile_content.py').read_text(encoding='utf-8'),str(R/'tools/company_profile_content.py'),'exec'),globals())\n"
if hook not in s:s=s.replace('for page,(title,desc,body) in pages.items():',hook+'for page,(title,desc,body) in pages.items():')
if 'href="assets/css/company-profile.css"' not in s:s=s.replace('<link rel="stylesheet" href="assets/css/navigation.css">','<link rel="stylesheet" href="assets/css/navigation.css"><link rel="stylesheet" href="assets/css/company-profile.css">')
s=s.replace("'name':'Techno Printpack'","'name':'Techno Industries'").replace('| Techno Printpack','| Techno Industries')
p.write_text(s,encoding='utf-8')
# Keep the outgoing enquiry identity and added preference fields consistent.
for filename in ['assets/js/quotation.js','assets/js/contact.js']:
 p=root/filename;s=p.read_text(encoding='utf-8').replace('Techno Printpack','Techno Industries')
 if filename.endswith('quotation.js'):
  s=s.replace("['dimensions','Dimensions'],['printing'","['dimensions','Dimensions'],['flute','Preferred flute'],['board','Preferred board'],['finish','Preferred surface finish'],['printing'")
 p.write_text(s,encoding='utf-8')
