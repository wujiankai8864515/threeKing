from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
import numpy as np,json,shutil
p=Path(__file__).parent;o=p/'revision_20261018_155650_UTC+08';o.mkdir(exist_ok=True)
font='/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc'
# Independent perspective plaque on silver art.
src=p/'pure/silver-green-dynamic-20261018_155216.png';im=Image.open(src).convert('RGBA')
plate=Image.new('RGBA',(200,60),(42,35,29,255));d=ImageDraw.Draw(plate);d.text((100,29),'汜水關',font=ImageFont.truetype(font,43,index=2),fill='#edb466',anchor='mm')
xy=[(744,544),(890,503),(901,550),(750,590)];uv=[(0,0),(200,0),(200,60),(0,60)]
A=[];b=[]
for (x,y),(u,v) in zip(xy,uv):A += [[x,y,1,0,0,0,-u*x,-u*y],[0,0,0,x,y,1,-v*x,-v*y]];b += [u,v]
coeff=np.linalg.solve(A,b);layer=plate.transform(im.size,Image.Transform.PERSPECTIVE,coeff,Image.Resampling.BICUBIC);layer.save(o/'silver-plaque-layer.png');Image.alpha_composite(im,layer).save(o/'silver-pure-with-plaque.png')
# Reuse exact story plaque layer, corrected hand image.
h=Image.open(p.parent/'generated_images/exec-3b949c44-2533-4e3b-820a-1b85b2306346.png').convert('RGBA');h.save(o/'hua-pure-corrected-hilt.png');hl=Image.open(p/'lettering/汜水關-label_20261018_155214_UTC+08.png');Image.alpha_composite(h,hl).save(o/'02-汜水關斩华雄.png')
keys=['blackiron','bronze','silver','gold'];names=['黑铁·市井潜龙','青铜·黄巾初征','白银·关前扬威','黄金·过关寻兄'];sources=[p/'pure/blackiron-grounded-v2.png',p/'pure/bronze-grounded-puregreen_20261018_155320_UTC+08.png',o/'silver-pure-with-plaque.png',p/'pure/gold-green-dragon-20261018_155405.png']
mask=Image.open(p/'art-clip-mask.png');sheet=Image.new('RGB',(1560,640),'#242c36');f=ImageFont.truetype(font,23)
for n,(k,s) in enumerate(zip(keys,sources)):
 if n==0:card=Image.open(p/'cards/01-黑铁·市井潜龙.png').convert('RGBA')
 else:
  art=Image.open(s).convert('RGBA').resize((881,1321),Image.Resampling.LANCZOS);placed=Image.new('RGBA',(1024,1536));placed.paste(art,(72,125));base=Image.new('RGBA',placed.size);base.paste(placed,(0,0),mask);card=Image.alpha_composite(Image.alpha_composite(base,Image.open(p/'frames'/f'{k}.png')),Image.open(p/'frames'/f'{k}-stars-ui.png'));card.save(o/f'{n+1:02}-{names[n]}.png')
 th=card.resize((360,540),Image.Resampling.LANCZOS);sheet.paste(th,(24+384*n,30),th);ImageDraw.Draw(sheet).text((204+384*n,590),names[n],font=f,fill='#f2eee3',anchor='mt')
sheet.save(o/'00-四阶总览.png');json.dump({'timezone':'UTC+08','sources':[str(s) for s in sources],'blackiron':'frozen unchanged','frames':'frozen unchanged','status':'pending root QA','story':'hilt two hands behind guard; independent exact 汜水關 label'},open(o/'manifest.json','w'),ensure_ascii=False,indent=2)
print(o)
