from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
p=Path(__file__).parent;names=['黑铁·市井潜龙','青铜·三骑追黄巾','白银·关前扬威','黄金·护行拖刀'];z=Image.new('RGB',(1560,640),'#242c36');d=ImageDraw.Draw(z);font=ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc',23)
for n,name in enumerate(names):
 im=Image.open(p/f'{n+1:02}-{name}.png').resize((360,540),Image.Resampling.LANCZOS);z.paste(im,(24+384*n,30),im);d.text((204+384*n,590),name,font=font,fill='#f2eee3',anchor='mt')
z.save(p/'00-四阶层级总览.png')
