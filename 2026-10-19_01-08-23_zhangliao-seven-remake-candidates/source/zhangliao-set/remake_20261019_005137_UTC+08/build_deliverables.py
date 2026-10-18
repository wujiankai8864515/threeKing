from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,shutil,hashlib
D=Path(__file__).resolve().parent
(D/'candidates').mkdir(exist_ok=True)
f=ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',23)
names=['01-黑铁-濮阳横锋','02-青铜-解缚新途','03-白银-合肥定乱','04-黄金-逍遥夺势','05-传记-白门解缚','06-传记-胜夜不卸甲','07-传记-解嫌出奇兵']
sources=[D/'ui'/x for x in ['01-黑铁-UI排版修复1190.png','02-青铜-UI排版修复1190.png','03-白银-UI排版修复1190.png','04-黄金-UI排版修复1190.png']]+[D/'raw'/f'bio{i:02}.png' for i in range(1,4)]
sheet=Image.new('RGB',(1600,1080),'#1e242c');dr=ImageDraw.Draw(sheet);manifest=[]
for i,(name,src) in enumerate(zip(names,sources)):
 dst=D/'candidates'/f'张辽-{name}.png';shutil.copy2(src,dst);im=Image.open(src)
 manifest.append(dict(asset=name,output=str(dst.relative_to(D)),source=str(src.relative_to(D)),dimensions=list(im.size),sha256=hashlib.sha256(dst.read_bytes()).hexdigest(),status='candidate_awaiting_user',promotion_target=(i-2 if i>=4 else None)))
 p=im.convert('RGBA');p.thumbnail((390,590) if i<4 else (520,350));x=400*i+(400-p.width)//2 if i<4 else (i-4)*535;y=34 if i<4 else 690;sheet.paste(p,(x,y),p);dr.text((x+12,630 if i<4 else 1040),name,font=f,fill='white')
sheet.save(D/'张辽-四阶三传记-新候选总览.png')
(D/'manifest.json').write_text(json.dumps({'hero':'张辽','generator':'built-in image_gen','native_portraits':[1024,1536],'native_stories':[1536,1024],'ui_canvas':[1190,1786],'art_resampling':'none; native art 1:1 independent UI','myth':'苍隼为原创象征，非原著神兽','assets':manifest},ensure_ascii=False,indent=2))
boxes={'card01':(480,260,700,510),'card02':(430,250,660,500),'card03':(380,250,620,490),'card04':(420,290,650,520),'bio01':(480,80,760,350),'bio02':(400,110,660,370),'bio03':(790,120,1050,380)}
for n,b in boxes.items():Image.open(D/'raw'/f'{n}.png').crop(b).save(D/'qa'/f'{n}-face-native.png')
for n,b in [('card01',(250,350,900,900)),('card02',(170,440,590,700)),('card03',(160,330,830,690)),('card04',(130,330,810,850)),('bio01',(500,570,1060,880)),('bio02',(580,520,850,700)),('bio03',(780,480,1180,840))]:Image.open(D/'raw'/f'{n}.png').crop(b).save(D/'qa'/f'{n}-hands-native.png')
