from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
p=Path(__file__).parent
art=Image.open('./generated_images/exec-8b362efa-4128-4e3f-9272-613b0ca1226f.png').convert('RGBA')
frame=Image.open('./generated_images/exec-83dd3673-11eb-44d0-9d62-997077f06ee0.png').convert('RGBA')
print(frame.mode,frame.size,'center alpha',frame.getpixel((512,768))[3])
art.save(p/'illustration.png');frame.save(p/'original-style-blackiron-frame.png')
base=Image.new('RGBA',art.size,(27,34,39,255))
# Keep art at original dimensions; only clip to actual card bounds, no zoom.
mask=Image.new('L',art.size,0);ImageDraw.Draw(mask).rectangle((65,49,965,1499),fill=255)
base.paste(art,(0,0),mask)
labels=Image.new('RGBA',art.size);d=ImageDraw.Draw(labels)
f='/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc'
d.text((608,85),'关羽',font=ImageFont.truetype(f,46),fill='#ecebdf',stroke_width=1,stroke_fill='#101918',anchor='mm')
d.text((151,136),'蜀',font=ImageFont.truetype(f,49),fill='#e7ecd9',stroke_width=1,stroke_fill='#12251c',anchor='mm')
labels.save(p/'dynamic-labels.png')
Image.alpha_composite(Image.alpha_composite(base,frame),labels).convert('RGB').save(p/'黑铁关羽-原游戏框校准.png')
