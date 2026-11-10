from pathlib import Path
import pymupdf
from PIL import Image,ImageDraw
from io import BytesIO
root=Path(__file__).resolve().parents[1]
doc=pymupdf.open('E:/Technopack 2.pdf')
out=root/'assets/media/profile';out.mkdir(parents=True,exist_ok=True)
assets=[('company-logo',204),('flute-guide',81),('box-samples',91),('display-rack',107),('produce-carton',109),('pvc-box',123),('iso-mark',298),('food-grade-mark',302),('edb-mark',299),('cea-mark',300),('sri-lanka-flag',296)]
tiles=[]
for name,xref in assets:
 data=doc.extract_image(xref)
 mask=next((item[1] for page in doc for item in page.get_images() if item[0]==xref),0)
 if mask:
  pix=pymupdf.Pixmap(pymupdf.Pixmap(doc,xref),pymupdf.Pixmap(doc,mask))
  im=Image.open(BytesIO(pix.tobytes('png'))).convert('RGBA')
 else:im=Image.open(BytesIO(data['image'])).convert('RGBA')
 if name=='company-logo':
  im.save(out/f'{name}.png')
 else:
  im.thumbnail((1000,1000));im.save(out/f'{name}.webp','WEBP',quality=88)
 tile=Image.new('RGB',(300,250),'#eee');preview=im.copy();preview.thumbnail((280,215));tile.paste(preview,((300-preview.width)//2,10),preview.getchannel('A'));ImageDraw.Draw(tile).text((10,230),name,fill='black');tiles.append(tile)
sheet=Image.new('RGB',(1200,750),'#ddd')
for i,t in enumerate(tiles):sheet.paste(t,((i%4)*300,(i//4)*250))
sheet.save(root/'tmp/pdfs/company-profile/extracted-assets.jpg')
