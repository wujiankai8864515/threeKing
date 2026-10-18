from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
import math,shutil
p=Path(__file__).parent
art=Image.open('./generated_images/exec-8b362efa-4128-4e3f-9272-613b0ca1226f.png').convert('RGBA')
frame=Image.open('./generated_images/exec-dc53777c-36e7-4034-982a-45b5b4f2b85b.png').convert('RGBA')
art.save(p/'illustration.png'); frame.save(p/'frame.png')
text=Image.new('RGBA',art.size);d=ImageDraw.Draw(text)
f='/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc'
font=lambda n:ImageFont.truetype(f,n)
d.text((510,107),'关羽',font=font(64),fill='#e5e1c9',stroke_width=2,stroke_fill='#151c1b',anchor='mm')
d.text((119,125),'蜀',font=font(70),fill='#e6e8cb',stroke_width=2,stroke_fill='#17352d',anchor='mm')
pts=[]
for i in range(10):
 a=-math.pi/2+i*math.pi/5;r=27 if i%2==0 else 12
 pts.append((939+math.cos(a)*r,143+math.sin(a)*r))
d.polygon(pts,fill='#c3c9b4',outline='#586359')
text.save(p/'dynamic-labels.png')
Image.alpha_composite(Image.alpha_composite(art,frame),text).convert('RGB').save(p/'黑铁关羽-装饰框校准稿.png')
