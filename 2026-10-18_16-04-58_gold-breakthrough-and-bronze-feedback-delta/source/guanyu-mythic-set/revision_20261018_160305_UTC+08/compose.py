from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
p=Path(__file__).parent;root=p.parent;prev=root/'revision_20261018_155650_UTC+08'
a=Image.open(p/'gold-pure-breakthrough.png').convert('RGBA').resize((881,1321),Image.Resampling.LANCZOS);placed=Image.new('RGBA',(1024,1536));placed.paste(a,(72,125));base=Image.new('RGBA',placed.size);base.paste(placed,(0,0),Image.open(root/'art-clip-mask.png'));card=Image.alpha_composite(Image.alpha_composite(base,Image.open(root/'frames/gold.png')),Image.open(root/'frames/gold-stars-ui.png'));card.save(p/'04-黄金·过关寻兄.png')
names=['黑铁·市井潜龙','青铜·黄巾初征','白银·关前扬威','黄金·过关寻兄'];paths=[root/'cards/01-黑铁·市井潜龙.png',prev/'02-青铜·黄巾初征.png',prev/'03-白银·关前扬威.png',p/'04-黄金·过关寻兄.png'];sheet=Image.new('RGB',(1560,640),'#242c36');font=ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc',23)
for n,s in enumerate(paths):
 im=Image.open(s).convert('RGBA').resize((360,540),Image.Resampling.LANCZOS);sheet.paste(im,(24+384*n,30),im);ImageDraw.Draw(sheet).text((204+384*n,590),names[n],font=font,fill='#f2eee3',anchor='mt')
sheet.save(p/'00-四阶总览.png')
