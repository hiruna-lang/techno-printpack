from pathlib import Path
p=Path(__file__).with_name('build_site.py');s=p.read_text(encoding='utf-8')
hook="exec(compile((R/'tools/navigation.py').read_text(encoding='utf-8'),str(R/'tools/navigation.py'),'exec'),globals())\n"
if hook not in s:s=s.replace('for page,(title,desc,body) in pages.items():',hook+'for page,(title,desc,body) in pages.items():')
old='<script type="application/ld+json">'
if 'href="assets/css/navigation.css"' not in s:s=s.replace(old,'<link rel="stylesheet" href="assets/css/navigation.css">'+old)
p.write_text(s,encoding='utf-8')
