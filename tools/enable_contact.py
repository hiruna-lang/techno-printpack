from pathlib import Path
p=Path(__file__).with_name('build_site.py');s=p.read_text(encoding='utf-8')
hook="exec(compile((R/'tools/contact_reference.py').read_text(encoding='utf-8'),str(R/'tools/contact_reference.py'),'exec'),globals())\n"
if hook not in s:s=s.replace('for page,(title,desc,body) in pages.items():',hook+'for page,(title,desc,body) in pages.items():')
old='<link rel="stylesheet" href="assets/css/corporate.css">'
if 'href="assets/css/contact.css"' not in s:s=s.replace(old,old+'{\'<link rel="stylesheet" href="assets/css/contact.css">\' if page==\'contact\' else \'\'}')
if 'src="assets/js/contact.js"' not in s:s=s.replace('</head><body','{\'<script defer src="assets/js/config.js"></script><script defer src="assets/js/contact.js"></script>\' if page==\'contact\' else \'\'}</head><body')
p.write_text(s,encoding='utf-8')
