from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
D=Path(__file__).parent;q=D/'qa-100pct';q.mkdir(exist_ok=True)
im=Image.open(D/'张辽-黑铁-v1-濮阳横锋身份候选.png')
boxes={'face':(410,180,615,365),'hand-left':(465,475,580,575),'hand-right':(750,580,850,680),'blade-root':(0,365,380,525),'full-weapon':(0,365,1024,765),'tailcap':(935,675,1024,775),'saddle-reins':(435,560,720,925),'horse-face':(35,485,350,890),'horse-legs':(160,1100,1024,1536),'cloth-armor':(340,335,870,630),'myth-feathers':(290,0,800,155)}
for n,b in boxes.items():
 c=im.crop(b);o=Image.new('RGB',(c.width,c.height+26),'#252525');o.paste(c,(0,26));ImageDraw.Draw(o).text((5,5),'ZHANG LIAO NATIVE 100%',fill='white');o.save(q/(n+'.png'))
# Read-only diagnostic axis: not an edited asset.
a=im.copy();dr=ImageDraw.Draw(a);dr.line([(325,479),(995,730)],fill=(20,255,255),width=2);dr.rectangle((200,150,790,850),outline=(255,60,100),width=2);dr.text((200,160),'SAFE REGION + ROOT-TAIL STRAIGHT CHORD (diagnostic)',fill=(255,60,100));a.save(q/'axis-safe-region-diagnostic.png');im.resize((480,720)).save(q/'thumbnail-review-only.png')
print('11 native crops + diagnostic + thumbnail')
