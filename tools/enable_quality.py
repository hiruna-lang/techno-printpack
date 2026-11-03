from pathlib import Path
p=Path(__file__).with_name('build_site.py')
s=p.read_text(encoding='utf-8')
hook="exec(compile((R/'tools/quality_reference.py').read_text(encoding='utf-8'),str(R/'tools/quality_reference.py'),'exec'),globals())\n"
if hook not in s:s=s.replace('for page,(title,desc,body) in pages.items():',hook+'for page,(title,desc,body) in pages.items():')
old='<link rel="stylesheet" href="assets/css/corporate.css">'
new=old+'{\'<link rel="stylesheet" href="assets/css/quality.css">\' if page==\'quality\' else \'\'}'
if 'href="assets/css/quality.css"' not in s:s=s.replace(old,new)
p.write_text(s,encoding='utf-8')
