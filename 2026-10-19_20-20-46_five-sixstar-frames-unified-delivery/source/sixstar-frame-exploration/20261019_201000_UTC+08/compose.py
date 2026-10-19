from PIL import Image,ImageDraw,ImageFont,ImageFilter
import numpy as np, json,math,hashlib,shutil
from pathlib import Path
P=Path(__file__).resolve().parent
W,H=1536,2304
font='/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc'
source=Path('/workspace/scratch/3f82ff2b3f81/guanyu-advanced/wing-cannon-mecha_20261019_200940_UTC+08/六星机甲关羽-巨翼光盾偃月炮-原图.png')
art=Image.open(source).convert('RGBA'); cfg=json.loads((P/'config.json').read_text())
shutil.copy2(source,P/'reference-main-art.png')
def metal(mask, colors):
 arr=np.zeros((H,W,4),dtype=np.uint8); yy=np.arange(H)
 stops=[(0,colors[0]),(.28,colors[1]),(.45,colors[0]),(.51,colors[2]),(.68,colors[1]),(1,colors[0])]
 box=mask.getbbox(); top,bottom=box[1],box[3]; vals=np.clip((yy-top)/max(1,bottom-top),0,1)
 for k in range(3):arr[:,:,k]=np.interp(vals,[v[0] for v in stops],[v[1][k] for v in stops])[:,None]
 arr[:,:,3]=np.asarray(mask);return Image.fromarray(arr)
def textmask(txt,xy,size):
 m=Image.new('L',(W,H));d=ImageDraw.Draw(m);f=ImageFont.truetype(font,size);b=d.textbbox((0,0),txt,font=f);d.text((xy[0]-(b[0]+b[2])/2,xy[1]-(b[1]+b[3])/2),txt,font=f,fill=255);return m
colors=[(104,74,27),(255,237,180),(255,255,247)]
def emboss(layer,m,cs=colors):
 edge=m.filter(ImageFilter.MaxFilter(7));shadow=Image.new('RGBA',(W,H),(26,24,22,0));shadow.putalpha(edge);layer.alpha_composite(shadow);layer.alpha_composite(metal(m,cs))
for c in cfg:
 frame=Image.open(c['source']).convert('RGBA').resize((W,H),Image.Resampling.LANCZOS);fa=frame.getchannel('A');ImageDraw.Draw(fa).rectangle((256,350,1279,1885),fill=0);frame.putalpha(fa);frame.save(P/f"{c['id']}-frame-transparent.png")
 base=Image.new('RGBA',(W,H),(12,22,27,255));base.alpha_composite(art,(256,350));d=ImageDraw.Draw(base)
 d.rectangle((252,346,1284,1890),outline='#ad9972',width=3)
 # Original hero art is never rescaled or repainted; decorative frame only surrounds it.
 base.alpha_composite(frame)
 ui=Image.new('RGBA',(W,H));d=ImageDraw.Draw(ui)
 # Small dark-metal backing is reserved for title, never behind spear icon.
 d.rounded_rectangle((495,254,1041,344),radius=18,fill='#142c32',outline='#c7b885',width=3)
 emboss(ui,textmask('机甲·关羽',(768,299),65))
 # Six separate beveled star silhouettes.
 for i in range(6):
  cx=533+i*94;cy=1934;r=34; pts=[(cx+math.cos(-math.pi/2+k*math.pi/5)*(r if k%2==0 else r*.44),cy+math.sin(-math.pi/2+k*math.pi/5)*(r if k%2==0 else r*.44)) for k in range(10)]
  m=Image.new('L',(W,H));ImageDraw.Draw(m).polygon(pts,fill=255);emboss(ui,m)
  ImageDraw.Draw(ui).line([pts[0],(cx,cy),pts[2]],fill='#fffbe1',width=2)
 # Two-character rank glyphs, centered as one unit, separate replaceable layer.
 emboss(ui,textmask('封侯',(367,2072),100))
 # One broad spearhead with socket and short shaft: silver face, warm contrasting bevel, no rectangle.
 m=Image.new('L',(W,H));md=ImageDraw.Draw(m);x,y=1180,2090
 md.polygon([(x,y-70),(x-34,y-7),(x-24,y+19),(x-8,y+26),(x-8,y+60),(x+8,y+60),(x+8,y+26),(x+24,y+19),(x+34,y-7)],fill=255)
 emboss(ui,m,[(63,92,100),(219,246,250),(255,255,255)])
 dd=ImageDraw.Draw(ui);dd.line([(x,y-58),(x,y+18)],fill='#ffffff',width=4);dd.line([(x-17,y+27),(x+17,y+27)],fill='#d6b065',width=5)
 base.alpha_composite(ui);ui.save(P/f"{c['id']}-ui-transparent.png");base.save(P/f"{c['id']}-{c['name']}-六星机甲关羽.png")
 c.update({'art_source':str(source),'art_offset':[256,350],'art_scale':1,'canvas':[W,H],'title':'机甲·关羽','rank':'封侯','star_count':6,'unit':'spearhead_icon_only','file':f"{c['id']}-{c['name']}-六星机甲关羽.png"})
thumbs=Image.new('RGB',(2000,720),'#111d24');d=ImageDraw.Draw(thumbs)
for i,c in enumerate(cfg):
 im=Image.open(P/c['file']);im.thumbnail((390,615));thumbs.paste(im,(i*400+(400-im.width)//2,55));f=ImageFont.truetype(font,25);d.text((i*400+20,10),c['id']+' '+c['name'],font=f,fill='#ecdfbd')
thumbs.save(P/'00-六星卡框五款总览.png')
(P/'manifest.json').write_text(json.dumps(cfg,ensure_ascii=False,indent=2))
(P/'sha256.json').write_text(json.dumps({p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in P.glob('*.png')},ensure_ascii=False,indent=2))
