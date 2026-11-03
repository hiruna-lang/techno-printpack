from pathlib import Path
p=Path(__file__).with_name('build_site.py')
s=p.read_text(encoding='utf-8')
hook="exec(compile((R/'tools/additional_pages.py').read_text(encoding='utf-8'),str(R/'tools/additional_pages.py'),'exec'),globals())\n"
if hook not in s:s=s.replace('for page,(title,desc,body) in pages.items():',hook+'for page,(title,desc,body) in pages.items():')
p.write_text(s,encoding='utf-8')
