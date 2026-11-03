from pathlib import Path
p=Path(__file__).with_name('build_site.py')
s=p.read_text(encoding='utf-8')
old='<link rel="stylesheet" href="assets/css/corporate.css">'
new=old+'{\'<link rel="stylesheet" href="assets/css/homepage.css">\' if page==\'index\' else \'\'}'
if 'href="assets/css/homepage.css"' not in s:s=s.replace(old,new)
p.write_text(s,encoding='utf-8')
