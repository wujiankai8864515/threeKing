from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
import json
r=Path(__file__).parent.parent;p=Path(__file__).parent
src=[('approved gold source',r/'pure/gold-v7-silver-lineage-dragon-20261018_165224.png'),('latest gold pure',r/'pure/gold-local-depth-finish-20261018_172405.png'),('framed gold',r/'naturalhierarchy_20261018_171620_UTC+08/04-黄金·护行拖刀.png'),('UI gold',r/'ui_display_20261018_171500_UTC+08/04-黄金-完整UI示意.png')]
boxes={'face':(520,180,665,355),'dragon':(650,145,895,375),'horse':(635,365,875,665),'blade':(20,735,325,1100)}
sizes=[]
for label,f in src:
 im=Image.open(f);sizes.append({'label':label,'path':str(f),'size':im.size})
 for part,b in boxes.items():
  if label in ('framed gold','UI gold'):b=tuple(round(v*.8603515625+(72 if n%2==0 else 125)) for n,v in enumerate(b))
  im.crop(b).save(p/f'{label}-{part}-100percent.png')
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',16)
for part in boxes:
 z=Image.new('RGB',(1300,430),'#333333');d=ImageDraw.Draw(z)
 for n,(label,f) in enumerate(src):
  c=Image.open(p/f'{label}-{part}-100percent.png').convert('RGB');z.paste(c,(n*325,35));d.text((n*325+3,5),label,font=font,fill='white')
 z.save(p/f'{part}-native100-comparison.png')
(p/'dimensions.json').write_text(json.dumps(sizes,indent=2))
