from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,shutil,hashlib
D=Path(__file__).resolve().parent
(D/'candidates').mkdir(exist_ok=True)
f=ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',23)
names=['01-黑铁-箕关护行','02-青铜-夜别旧营','03-白银-截断粮道','04-黄金-沔水拆垒','05-传记-不以弑主换新途','06-传记-细作与粮车','07-传记-借旗绕沔水']
sources=[D/'ui'/x for x in ['01-黑铁-UI排版修复1190.png','02-青铜-UI排版修复1190.png','03-白银-UI排版修复1190.png','04-黄金-UI排版修复1190.png']]+[D/'raw'/f'bio{i:02}.png' for i in range(1,4)]
sheet=Image.new('RGB',(1600,1080),'#1e242c');dr=ImageDraw.Draw(sheet);manifest=[]
for i,(name,src) in enumerate(zip(names,sources)):
 dst=D/'candidates'/f'徐晃-{name}.png';shutil.copy2(src,dst);im=Image.open(src)
 manifest.append(dict(asset=name,output=str(dst.relative_to(D)),source=str(src.relative_to(D)),dimensions=list(im.size),sha256=hashlib.sha256(dst.read_bytes()).hexdigest(),status='candidate_awaiting_user',promotion_target=(i-2 if i>=4 else None)))
 p=im.convert('RGBA');p.thumbnail((390,590) if i<4 else (520,350));x=400*i+(400-p.width)//2 if i<4 else (i-4)*535;y=34 if i<4 else 690;sheet.paste(p,(x,y),p);dr.text((x+12,630 if i<4 else 1040),name,font=f,fill='white')
sheet.save(D/'徐晃-四阶三传记-新候选总览.png')
(D/'manifest.json').write_text(json.dumps({'hero':'徐晃','generator':'built-in image_gen','native_portraits':[1024,1536],'native_stories':[1536,1024],'ui_canvas':[1190,1786],'art_resampling':'none; native art 1:1 independent UI','myth':'断路玄獬为原创獬豸联想象征，非原著神兽','assets':manifest},ensure_ascii=False,indent=2))

boxes={'card01':(380,260,640,510),'card02':(370,270,650,540),'card03':(300,200,750,600),'card04':(300,200,750,600),'bio01':(350,100,850,500),'bio02':(350,100,850,500),'bio03':(500,120,1050,620)}
for n,b in boxes.items():Image.open(D/'raw'/f'{n}.png').crop(b).save(D/'qa'/f'{n}-face-native.png')
for n in ['card01','card02','card03','card04','bio01','bio02','bio03']:
 im=Image.open(D/'raw'/f'{n}.png')
 box=(150,450,850,1100) if n.startswith('card') else (200,350,1300,900)
 im.crop(box).save(D/'qa'/f'{n}-hands-native.png')
