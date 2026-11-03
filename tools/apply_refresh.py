from pathlib import Path
p=Path(__file__).with_name('build_site.py')
s=p.read_text(encoding='utf-8')
hook="exec(compile((R/'tools/site_design.py').read_text(encoding='utf-8'),str(R/'tools/site_design.py'),'exec'),globals())\n"
if hook not in s:s=s.replace('pages={',hook+'pages={')
s=s.replace('<link rel="stylesheet" href="assets/css/animations.css">','<link rel="stylesheet" href="assets/css/animations.css"><link rel="stylesheet" href="assets/css/corporate.css">')
# The identity module owns the favicon; remove the obsolete T icon generation.
s='\n'.join(line for line in s.split('\n') if not line.startswith("write('assets/icons/favicon.svg'"))
p.write_text(s,encoding='utf-8')
