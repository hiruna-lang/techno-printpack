from pathlib import Path
from PIL import Image
p=Path(__file__).with_name('build_site.py')
s=p.read_text(encoding='utf-8')
s=s.replace('return f\'<img class=', 'dimensions=Image.open(R/f"assets/media/{k}-1600.webp").size\n return f\'<img class=')
s=s.replace('import json,html','import json,html\nfrom PIL import Image')
s=s.replace('width="1600" height="1067" alt="{alt}"','width="{dimensions[0]}" height="{dimensions[1]}" alt="{alt}"')
s=s.replace('{header(page)}<main','{header(page)}<noscript><link rel="stylesheet" href="assets/css/noscript.css"></noscript><main')
p.write_text(s,encoding='utf-8')
