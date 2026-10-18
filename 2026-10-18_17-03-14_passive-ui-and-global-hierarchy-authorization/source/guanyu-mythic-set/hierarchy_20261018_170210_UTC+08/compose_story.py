from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
p=Path(__file__).parent;r=p.parent
im=Image.open(r/'stories/03-千里护行-hierarchy_20261018_170217_UTC+08.png').convert('RGBA');z=Image.new('RGBA',im.size);d=ImageDraw.Draw(z);font=ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc',57);d.text((333,534),'刘',font=font,fill='#39231c',anchor='mm');z.save(p/'刘旗独立字层.png');Image.alpha_composite(im,z).save(p/'03-千里护行.png')
