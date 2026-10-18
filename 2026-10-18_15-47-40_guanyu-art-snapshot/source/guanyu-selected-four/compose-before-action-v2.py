from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import numpy as np,json
p=Path(__file__).parent
keys=['blackiron','bronze','silver','gold'];titles=['黑铁·市井心志','青铜·桃园初征','白银·阵前扬名','黄金·千里寻兄']
mask=Image.new('L',(1024,1536));ImageDraw.Draw(mask).rectangle((80,125,943,1425),fill=255);mask.save(p/'art-clip-mask.png')
f='/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc'
star=Image.open(p/'frames/blackiron.png').convert('RGBA').crop((878,250,948,320));a=np.array(star);rgb=a[:,:,:3].astype(float);a[:,:,3]=np.where((rgb[:,:,0]>rgb[:,:,1]*1.04)&(rgb[:,:,1]>rgb[:,:,2]*1.15),a[:,:,3],0);star=Image.fromarray(a);star.save(p/'frames/star-icon.png')
for n,k in enumerate(keys):
 art=Image.open(p/'pure'/f'{k}.png').convert('RGBA');fr=Image.open(p/'frames'/f'{k}.png').convert('RGBA')
 if n:
  placed=Image.new('RGBA',art.size);placed.paste(art.resize((881,1321),Image.Resampling.LANCZOS),(72,125));art=placed
 if k=='bronze':
  original=Image.open(p/'pure/bronze.png').convert('RGBA')
  art=Image.new('RGBA',original.size)
  # Layout-only backdrop uses sky/peach-canopy crop; hero image is proportionally fitted below badge.
  fit=original.resize((881,1321),Image.Resampling.LANCZOS)
  art.paste(fit.crop((0,0,881,120)).transpose(Image.Transpose.FLIP_TOP_BOTTOM),(72,125))
  art.paste(fit,(72,245))
 base=Image.new('RGBA',art.size);base.paste(art,(0,0),mask)
 labels=Image.new('RGBA',art.size);d=ImageDraw.Draw(labels);d.text((605,85),'天·关羽',font=ImageFont.truetype(f,43),fill='#f4f1e9',stroke_width=2,stroke_fill='#18201d',anchor='mm')
 if n:
  for j in range(n+1):labels.alpha_composite(star,(878,250+85*j))
 labels.save(p/'frames'/f'{k}-dynamic-ui.png')
 Image.alpha_composite(Image.alpha_composite(base,fr),labels).save(p/'cards'/f'{n+1:02}-{titles[n]}.png')
w,h=360,540;pad=24
sheet=Image.new('RGB',(4*(w+pad)+pad,650),'#222c33');d=ImageDraw.Draw(sheet)
d.text((24,10),'关羽 · 四阶成长',font=ImageFont.truetype(f,27),fill='#f5f0e4')
for n,k in enumerate(keys):
 card=Image.open(p/'cards'/f'{n+1:02}-{titles[n]}.png').resize((w,h),Image.Resampling.LANCZOS);x=pad+n*(w+pad);sheet.paste(card,(x,60),card);d.text((x+w//2,610),titles[n],font=ImageFont.truetype(f,21),fill='#f5f0e4',anchor='mt')
sheet.save(p/'00-关羽四阶总览.png')
