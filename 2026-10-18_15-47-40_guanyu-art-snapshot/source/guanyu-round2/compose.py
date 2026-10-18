from PIL import Image,ImageDraw,ImageFont,ImageFilter
from pathlib import Path
import json,numpy as np
p=Path(__file__).parent
frame=Image.open('./generated_images/exec-83dd3673-11eb-44d0-9d62-997077f06ee0.png').convert('RGBA')
mask=Image.new('L',frame.size,0)
ImageDraw.Draw(mask).rectangle((80,125,943,1425),fill=255)
mask.save(p/'card-outer-mask.png');frame.save(p/'shared-blackiron-frame.png')
labels=Image.new('RGBA',frame.size);d=ImageDraw.Draw(labels)
f='/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc'
d.text((605,85),'天·关羽',font=ImageFont.truetype(f,43),fill='#f4f1e9',stroke_width=2,stroke_fill='#18201d',anchor='mm')
labels.save(p/'shared-dynamic-labels.png')
manifest=json.loads((p/'manifest.json').read_text())
for item in manifest:
 art=Image.open(item['path']).convert('RGBA')
 if art.size != frame.size:art=art.resize(frame.size,Image.Resampling.LANCZOS)
 art.save(p/'pure'/f"{item['number']:02}.png")
 placed=art
 if item['number'] in (1,6):
  placed=Image.new('RGBA',frame.size)
  placed.paste(art.resize((881,1321),Image.Resampling.LANCZOS),(72,125))
 base=Image.new('RGBA',frame.size);base.paste(placed,(0,0),mask)
 out=Image.alpha_composite(Image.alpha_composite(base,frame),labels)
 out.save(p/'cards'/f"{item['number']:02}-黑铁关羽-第二轮.png")
# Five columns x two rows, captions outside card art.
w,h=360,540;pad=22;header=48;cap=43
sheet=Image.new('RGB',(pad+5*(w+pad),header+pad+2*(h+cap+pad)), '#222c33');sd=ImageDraw.Draw(sheet)
sd.text((pad,10),'黑铁关羽 · 第二轮自由构思',font=ImageFont.truetype(f,25),fill='#f4f1e6')
for k,item in enumerate(manifest):
 x=pad+(k%5)*(w+pad);y=header+pad+(k//5)*(h+cap+pad)
 card=Image.open(p/'cards'/f"{item['number']:02}-黑铁关羽-第二轮.png").resize((w,h),Image.Resampling.LANCZOS)
 sheet.paste(card,(x,y),card)
 sd.text((x+w//2,y+h+8),f"{item['number']:02}  {item['label']}",font=ImageFont.truetype(f,19),fill='#eee9da',anchor='mt')
sheet.save(p/'00-第二轮总览.png')
