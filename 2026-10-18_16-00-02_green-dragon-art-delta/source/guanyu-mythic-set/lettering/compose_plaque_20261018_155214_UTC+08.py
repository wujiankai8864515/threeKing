from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
p=Path('./guanyu-mythic-set')
s=p/'stories/02-天降斩华雄-v3-刀具修正_20261018_155105.png'
im=Image.open(s).convert('RGBA');layer=Image.new('RGBA',im.size);d=ImageDraw.Draw(layer)
# Independent precisely typeset architectural plaque; retain existing outer bevel.
d.polygon([(589,687),(680,682),(681,712),(589,717)],fill=(39,43,48,255))
font=ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc',25,index=2)
for i,c in enumerate('汜水關'):
 d.text((593+i*29,684-i*1.4),c,font=font,fill=(220,207,178,255),stroke_width=0)
layer.save(p/'lettering/汜水關-label_20261018_155214_UTC+08.png')
Image.alpha_composite(im,layer).convert('RGB').save(p/'stories/02-天降斩华雄-v3-汜水關_20261018_155214_UTC+08.png')
