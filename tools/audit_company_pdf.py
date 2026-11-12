from pathlib import Path
import json
import pymupdf
from PIL import Image,ImageDraw
root=Path(__file__).resolve().parents[1]
out=root/'tmp/pdfs/company-profile'
out.mkdir(parents=True,exist_ok=True)
doc=pymupdf.open('E:/Technopack 2.pdf')
pages=[];tiles=[]
for i,page in enumerate(doc):
 text=page.get_text(sort=True)
 pages.append({'page':i+1,'text':text,'images':len(page.get_images())})
 pix=page.get_pixmap(matrix=pymupdf.Matrix(1,1),alpha=False)
 pix.save(str(out/f'page-{i+1:02}.png'))
 im=Image.frombytes('RGB',[pix.width,pix.height],pix.samples)
 im.thumbnail((300,400))
 tile=Image.new('RGB',(320,430),'#e5e5e5');tile.paste(im,((320-im.width)//2,10))
 ImageDraw.Draw(tile).text((12,410),f'PAGE {i+1}',fill='black');tiles.append(tile)
sheet=Image.new('RGB',(320*4,430*((len(tiles)+3)//4)),'#ddd')
for i,tile in enumerate(tiles):sheet.paste(tile,((i%4)*320,(i//4)*430))
sheet.save(out/'contact-sheet.jpg')
(out/'extracted.json').write_text(json.dumps(pages,indent=2,ensure_ascii=False),encoding='utf-8')
(out/'extracted.txt').write_text('\n\n'.join(f'--- PAGE {p["page"]} ---\n{p["text"]}' for p in pages),encoding='utf-8')
print('Pages:',len(doc));print('Text characters:',sum(len(p['text']) for p in pages));print(out)
