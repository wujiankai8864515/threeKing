from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json
p=Path(__file__).parent;r=p.parent
files=['blackiron-qualityrevision_20261018_163911_UTC+08.png','bronze-qualityrevision_20261018_163739_UTC+08.png','silver-qualityrevision-20261018_164052.png','gold-qualityrevision-20261018_163847.png'];keys=['blackiron','bronze','silver','gold'];names=['黑铁·市井潜龙','青铜·三骑追黄巾','白银·关前扬威','黄金·护行拖刀'];sheet=Image.new('RGB',(1560,640),'#242c36');font=ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc',23)
for n,(f,k) in enumerate(zip(files,keys)):
 im=Image.open(r/'pure'/f).convert('RGBA')
 if k=='silver':im=Image.alpha_composite(im,Image.open(r/'revision_20261018_155650_UTC+08/silver-plaque-layer.png'))
 if k=='gold':im=Image.alpha_composite(im,Image.open(r/'revision_20261018_163130_UTC+08/刘旗独立字层.png'))
 im.save(p/f'{k}-pure-with-independent-label.png');a=im.resize((881,1321),Image.Resampling.LANCZOS);z=Image.new('RGBA',(1024,1536));z.paste(a,(72,125));b=Image.new('RGBA',z.size);b.paste(z,(0,0),Image.open(r/'art-clip-mask.png'));card=Image.alpha_composite(Image.alpha_composite(b,Image.open(r/'frames'/f'{k}.png')),Image.open(r/'frames'/f'{k}-stars-ui.png'));card.save(p/f'{n+1:02}-{names[n]}.png');th=card.resize((360,540),Image.Resampling.LANCZOS);sheet.paste(th,(24+384*n,30),th);ImageDraw.Draw(sheet).text((204+384*n,590),names[n],font=font,fill='#f2eee3',anchor='mt')
sheet.save(p/'00-四阶质量修订总览.png');json.dump({'timezone':'UTC+08','card_sources':files,'card_pixels':[1024,1536],'story_pixels':[1536,1024],'no_upscale':True,'status':'pending root QA and user acceptance','frames':'same approved separate frame/star/labels, no name or faction text','process':'builtin imagegen quality-only edits; Hua story additionally integrated latest hierarchy/identity/pose corrections; pass story blue dragon corrected green and distant narrative softened. All original versions retained.'},open(p/'manifest.json','w'),ensure_ascii=False,indent=2)
