from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,shutil,hashlib
D=Path(__file__).resolve().parent
f=ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',24)
names=['01-黑铁-隆中高卧','02-青铜-出庐定策','03-白银-七星借风','04-黄金-空城定局','05-传记-三顾定志','06-传记-风起江上','07-传记-虚实之间']
sources=[D/'ui'/x for x in ['01-黑铁-UI排版修复1190.png','02-青铜-UI排版修复1190.png','03-白银-UI排版修复1190.png','04-黄金-UI排版修复1190.png']]+[D/'raw'/f'bio{i:02}.png' for i in range(1,4)]
sheet=Image.new('RGB',(1600,1080),'#1e242c');dr=ImageDraw.Draw(sheet)
manifest=[]
for i,(name,src) in enumerate(zip(names,sources)):
 dst=D/'candidates'/f'诸葛亮-{name}.png';shutil.copy2(src,dst)
 im=Image.open(src);manifest.append(dict(asset=name,output=str(dst.relative_to(D)),source=str(src.relative_to(D)),dimensions=list(im.size),sha256=hashlib.sha256(dst.read_bytes()).hexdigest(),status='candidate_awaiting_user'))
 if i<4:
  p=im.convert('RGBA');p.thumbnail((390,590));sheet.paste(p,(400*i+(400-p.width)//2,34),p);dr.text((400*i+30,630),name,font=f,fill='white')
 else:
  p=im.convert('RGB');p.thumbnail((520,350));x=(i-4)*535;sheet.paste(p,(x,690));dr.text((x+20,1040),name,font=f,fill='white')
sheet.save(D/'诸葛亮-四阶三传记-新候选总览.png')
(D/'manifest.json').write_text(json.dumps({'hero':'诸葛亮','generator':'built-in image_gen','native_portraits':[1024,1536],'native_stories':[1536,1024],'ui_canvas':[1190,1786],'art_resampling':'none; native portrait 1:1 under independent UI','assets':manifest},ensure_ascii=False,indent=2))
# Native QA crops, no resampling
boxes={'card01final':(310,240,650,550),'card02':(330,140,650,460),'card03':(440,240,760,560),'card04':(330,320,650,640),'bio01':(300,130,620,450),'bio02':(980,120,1300,440),'bio03':(430,90,750,410)}
for n,b in boxes.items():Image.open(D/'raw'/f'{n}.png').crop(b).save(D/'qa'/f'{n}-face-native.png')
for n,b in [('card01final',(280,900,900,1280)),('card03',(180,330,450,590)),('card04',(330,900,1000,1180)),('bio01',(500,620,1020,840)),('bio03',(870,350,1050,530))]:Image.open(D/'raw'/f'{n}.png').crop(b).save(D/'qa'/f'{n}-hands-native.png')
(D/'index.html').write_text('<meta charset="utf-8"><title>诸葛亮全新候选</title><style>body{background:#222;color:white;font-family:sans-serif}img{max-width:95vw;max-height:95vh}</style><h1>诸葛亮四阶三传记 · 待审候选</h1><p>四卡原生1024×1536，三传记1536×1024；UI画布1190×1786，插画不放大。</p>'+''.join(f'<h2>{x["asset"]}</h2><img src="{x["output"]}">' for x in manifest))
