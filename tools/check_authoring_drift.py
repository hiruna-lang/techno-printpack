from pathlib import Path
import difflib
root=Path(__file__).resolve().parents[1]
out=root/'tmp/content-audit'
out.mkdir(parents=True,exist_ok=True)
source=(root/'tools/build_site.py').read_text(encoding='utf-8')
source=source.replace("def write(p,s): (R/p).write_text(s,encoding='utf-8')","def write(p,s): outputs[p]=s")
scope={'__file__':str(root/'tools/build_site.py'),'outputs':{}}
exec(compile(source,str(root/'tools/build_site.py'),'exec'),scope)
for name,text in scope['outputs'].items():
 if not name.endswith('.html'):continue
 current=(root/name).read_text(encoding='utf-8')
 if current!=text:
  diff='\n'.join(difflib.unified_diff(current.splitlines(),text.splitlines(),fromfile='current',tofile='generated'))
  (out/(name+'.diff')).write_text(diff,encoding='utf-8')
  print(name,'differs:',len(current),'current characters /',len(text),'generated')
 else:print(name,'matches source')
