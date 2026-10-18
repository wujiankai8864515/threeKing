from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
p=Path(__file__).parent
keys=['blackiron','bronze','silver','gold'];names=['黑铁·市井潜龙','青铜·桃园初征','白银·天降龙斩','黄金·神路寻兄']
f=ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc',23)
s=Image.open(p/'frames/star-source.png').convert('RGBA');s=s.crop(s.getbbox());s.thumbnail((64,64),Image.Resampling.LANCZOS);s.save(p/'frames/star-icon.png')
mask=Image.new('L',(1024,1536));ImageDraw.Draw(mask).rectangle((80,125,943,1425),fill=255);mask.save(p/'art-clip-mask.png')
card_sheet=Image.new('RGB',(1560,640),'#242c36');frame_sheet=Image.new('RGB',(1560,640),'#32343a')
for n,k in enumerate(keys):
 frame=Image.open(p/'frames'/f'{k}.png').convert('RGBA');print(k,'alpha',frame.getpixel((0,0))[3],frame.getpixel((500,700))[3])
 art=Image.open(p/'pure'/f'{k}.png').convert('RGBA').resize((881,1321),Image.Resampling.LANCZOS);placed=Image.new('RGBA',(1024,1536));placed.paste(art,(72,125));base=Image.new('RGBA',placed.size);base.paste(placed,(0,0),mask)
 ui=Image.new('RGBA',(1024,1536))
 for j in range(n+1):ui.alpha_composite(s,(880,250+85*j))
 ui.save(p/'frames'/f'{k}-stars-ui.png')
 card=Image.alpha_composite(Image.alpha_composite(base,frame),ui);card.save(p/'cards'/f'{n+1:02}-{names[n]}.png')
 preview=Image.alpha_composite(frame,ui);preview.save(p/'frames'/f'{k}-star-preview.png')
 for sheet,img in [(card_sheet,card),(frame_sheet,preview)]:
  img=img.resize((360,540),Image.Resampling.LANCZOS);sheet.paste(img,(24+384*n,30),img);ImageDraw.Draw(sheet).text((204+384*n,590),names[n] if sheet is card_sheet else ['黑铁','青铜','白银','黄金'][n],font=f,fill='#f2eee3',anchor='mt')
card_sheet.save(p/'00-神话四阶总览.png');frame_sheet.save(p/'00-四材质通用框预览.png')
