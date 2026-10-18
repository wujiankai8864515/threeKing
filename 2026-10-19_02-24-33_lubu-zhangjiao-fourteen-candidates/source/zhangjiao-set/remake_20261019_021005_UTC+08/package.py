from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,hashlib,shutil
P=Path(__file__).resolve().parent
names=['卷中问风','疫路人来','期日已破']
(P/'candidates').mkdir(exist_ok=True)
for i,n in enumerate(['黑铁','青铜','白银','黄金'],1):shutil.copy2(P/f'ui/0{i}-{n}-UI排版修复1190.png',P/f'candidates/张角-0{i}-{n}.png')
for i,n in enumerate(names,1):shutil.copy2(P/f'raw/bio{i:02}.png',P/f'candidates/张角-0{i+4}-传记-{n}.png')
font=ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',24)
sheet=Image.new('RGB',(1920,1210),'#20252a');d=ImageDraw.Draw(sheet)
for i,n in enumerate(['黑铁','青铜','白银','黄金'],1):
 im=Image.open(P/f'candidates/张角-0{i}-{n}.png').convert('RGBA');im.thumbnail((465,698));sheet.paste(im,((i-1)*480+7,15),im);d.text(((i-1)*480+20,717),n,font=font,fill='white')
for i,n in enumerate(names,1):
 im=Image.open(P/f'raw/bio{i:02}.png');im.thumbnail((620,414));sheet.paste(im,((i-1)*640+10,755));d.text(((i-1)*640+20,1178),n+' → '+['青铜','白银','黄金'][i-1],font=font,fill='white')
sheet.save(P/'candidates/张角-08-完整七图总览.jpg',quality=94)
items=[]
for p in sorted((P/'candidates').iterdir()):
 im=Image.open(p);items.append({'file':str(p),'dimensions':list(im.size),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'status':'candidate awaiting user'})
raw=[]
for p in sorted((P/'raw').glob('*.png')):raw.append({'file':str(p),'native_dimensions':list(Image.open(p).size),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
(P/'index.json').write_text(json.dumps({'hero':'张角','built_in_image_gen':True,'no_native_4K_claim':True,'raw_sources':raw,'deliverables':items,'ui_manifest':'ui/composition-manifest.json','research':'RESEARCH.md','qa':'QA.md'},ensure_ascii=False,indent=2))
# Local inspection crops from each independent source, deliberately no sharpening.
for p in (P/'raw').glob('*.png'):
 im=Image.open(p);w,h=im.size
 if p.name.startswith('card'):box=(int(w*.22),int(h*.12),int(w*.88),int(h*.76))
 else:box=(int(w*.12),int(h*.10),int(w*.96),int(h*.78))
 im.crop(box).save(P/'qa'/f'{p.stem}-face-hands-props.png')
print(json.dumps(items,ensure_ascii=False))
