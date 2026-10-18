from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib,datetime
D=Path(__file__).parent;q=D/'qa-100pct';q.mkdir(exist_ok=True)
boxes={'iron':{'face':(310,220,610,530),'hands-bow':(220,450,1010,1000)},'bronze':{'face-drawhand':(310,350,650,650),'bowhand':(790,480,1030,700)},'silver':{'face-drawhand':(310,320,650,640),'bowhand':(770,550,1035,760)},'gold':{'face':(380,235,640,490),'bow-grip':(570,770,840,1000),'sunwheel':(580,145,1000,570)}}
files={'iron':'01-黑铁-新框完整UI候选1190.png','bronze':'02-青铜-新框完整UI候选1190.png','silver':'03-白银-新框完整UI候选1190.png','gold':'04-黄金-新框完整UI候选1190.png'}
for tier,fn in files.items():
 im=Image.open(D/fn).convert('RGBA')
 for name,box in boxes[tier].items():
  c=im.crop(box);o=Image.new('RGBA',(c.width,c.height+26),(30,30,30,255));o.alpha_composite(c,(0,26));ImageDraw.Draw(o).text((5,5),tier.upper()+' UI NATIVE 100%',fill='white');o.save(q/f'{tier}-{name}.png')
# Rendered text and slot positions in one diagnostic, without resizing.
ims=[]
for tier,fn in files.items():
 im=Image.open(D/fn).convert('RGBA');box=(780,1070,1100,1370);c=im.crop(box);o=Image.new('RGBA',(320,330),(30,30,30,255));o.alpha_composite(c,(0,30));ImageDraw.Draw(o).text((5,5),tier.upper()+' UI SLOTS',fill='white');ims.append(o)
out=Image.new('RGBA',(1280,330),(30,30,30,255))
for i,im in enumerate(ims):out.alpha_composite(im,(i*320,0))
out.save(q/'four-skill-slots-native100.png')
(D/'output-hashes.json').write_text(json.dumps([{'file':f,'sha256':hashlib.sha256((D/f).read_bytes()).hexdigest(),'size':list(Image.open(D/f).size),'mode':Image.open(D/f).mode} for f in list(files.values())+['四阶新框完整UI-候选总览.png']],ensure_ascii=False,indent=2))
print('10 native crop files and output hashes saved')
