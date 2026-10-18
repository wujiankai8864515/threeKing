from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import math
p=Path(__file__).parent
art=Image.open(p/'A-黑铁关羽校准底图.png').convert('RGBA')
w,h=art.size
ui=Image.new('RGBA',art.size)
d=ImageDraw.Draw(ui)
font='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
f=lambda s:ImageFont.truetype(font,s)
# Independent temporary UI overlay. Original art is never modified.
d.rectangle((9,9,w-10,h-10),outline='#161c20',width=20)
d.rectangle((24,24,w-25,h-25),outline='#6c7775',width=3)
d.rectangle((29,29,w-30,142),fill=(22,30,32,235))
d.line((30,143,w-30,143),fill='#4c8676',width=4)
d.text((w//2,80),'关羽',font=f(63),fill='#e4e5dd',anchor='mm')
d.ellipse((46,47,113,114),fill='#29584a',outline='#719284',width=3)
d.text((80,79),'蜀',font=f(38),fill='#f4f0d9',anchor='mm')
# Narrow right-side information strip, visually separate from illustration.
x0=int(w*.865)
d.rectangle((x0,145,w-30,int(h*.86)),fill=(20,29,31,195),outline='#596a63',width=2)
cx=(x0+w-30)/2;cy=205
points=[]
for i in range(10):
 a=-math.pi/2+i*math.pi/5;r=25 if i%2==0 else 11
 points.append((cx+math.cos(a)*r,cy+math.sin(a)*r))
d.polygon(points,fill='#b7c4b8',outline='#eef2dc')
d.rectangle((29,int(h*.9),w-30,h-29),fill=(20,29,31,220))
d.line((29,int(h*.9),w-30,int(h*.9)),fill='#4c8676',width=3)
ui.save(p/'UI-overlay.png')
Image.alpha_composite(art,ui).convert('RGB').save(p/'黑铁关羽-带框校准稿.png')
