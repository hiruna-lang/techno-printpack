from pathlib import Path
from PIL import Image,ImageOps,ImageDraw
import rawpy,json
root=Path(__file__).resolve().parents[1]
out=root/'assets/media'
inventory=[]
for folder in ['packaging company','Farm']:
    tiles=[]
    for n,p in enumerate(sorted((root/'images'/folder).rglob('*'))):
        if not p.is_file():continue
        item={'source':str(p.relative_to(root)).replace('\\','/'),'bytes':p.stat().st_size}
        try:
            if p.suffix.lower()=='.cr3':
                with rawpy.imread(str(p)) as raw:
                    im=Image.fromarray(raw.postprocess(use_camera_wb=True,half_size=True))
            elif p.suffix.lower() in ['.jpg','.jpeg','.png','.webp']:
                im=ImageOps.exif_transpose(Image.open(p)).convert('RGB')
            else:
                item['status']='original video, not used';inventory.append(item);continue
            key=('factory-' if folder=='packaging company' else 'farm-')+p.stem.replace(' ','').replace('(','').replace(')','')
            item.update({'key':key,'width':im.width,'height':im.height,'status':'converted'})
            for size in [640,1600]:
                copy=im.copy();copy.thumbnail((size,size));copy.save(out/f'{key}-{size}.webp','WEBP',quality=83)
            tile=ImageOps.fit(im,(240,160)); canvas=Image.new('RGB',(260,200),'white');canvas.paste(tile,(10,5));ImageDraw.Draw(canvas).text((10,172),p.stem[:31],fill='black');tiles.append(canvas)
        except Exception as e:item['status']=str(e)
        inventory.append(item)
    sheet=Image.new('RGB',(260*4,200*((len(tiles)+3)//4)),'#dddddd')
    for i,t in enumerate(tiles):sheet.paste(t,((i%4)*260,(i//4)*200))
    sheet.save(root/'tools'/f'{folder.replace(" ","-")}-contact-sheet.jpg')
(root/'assets/media/inventory.json').write_text(json.dumps(inventory,indent=2))
print('Processed',len(inventory),'assets')
