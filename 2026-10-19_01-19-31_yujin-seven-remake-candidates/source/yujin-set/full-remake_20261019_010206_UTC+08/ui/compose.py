from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,shutil,hashlib
import numpy as np
D=Path(__file__).parent;R=D.parent
BASE=Path('/workspace/scratch/3f82ff2b3f81/guanyu-mythic-set/ui-local-composite-candidates_2026-10-18_23-55-42_UTC+08')
S=(1190,1786); sx=1190/1024; sy=1786/1536
fontpath='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
mask=Image.open(BASE/'art-native-slot-mask.png').convert('L');mask.save(D/'art-native-slot-mask.png')
cfg={};manifest={'status':'candidate_pending_user_review','generator':'built-in image_gen','cards':{},'stories':{},'art_native':{'cards':[1024,1536],'stories':[1536,1024]},'frame_canvas':list(S),'resampling':'art 1:1 at84,145; frame reused existing 1190x1786','original_designs':['identity','clothes','stone rhinoceros','blue energy','unnamed spear','baton','all skills']}
def put(draw,t,cx,cy,fs):
 f=ImageFont.truetype(fontpath,fs); b=draw.textbbox((0,0),t,font=f,stroke_width=0); x=round(cx-(b[0]+b[2])/2); y=round(cy-(b[1]+b[3])/2)
 draw.text((x,y),t,font=f,fill='#fff7df',stroke_width=2,stroke_fill='#302310')
 return {'text':t,'ink_bbox':[x+b[0],y+b[1],x+b[2],y+b[3]],'center':[cx,cy]}
names=['整列','镇足','坚壁']
for i,tier in enumerate(['iron','bronze','silver','gold'],1):
 frame=Image.open(BASE/f'{tier}-frame-layout-1190.png').convert('RGBA');frame.save(D/f'{tier}-frame.png')
 tx=Image.new('RGBA',S);dr=ImageDraw.Draw(tx)
 cx,cy=144*sx,132*sy;rr=43*sx
 dr.ellipse((cx-rr,cy-rr,cx+rr,cy+rr),fill='#143c62',outline='#75a4c0',width=2)
 rows=[put(dr,'魏',cx,cy,round(62*sx)),put(dr,'于禁',630*sx,90*sy,round(45*sx)),put(dr,'LV',909*sx,105*sy,round(26*sx)),put(dr,'1',909*sx,148*sy,round(48*sx)),put(dr,'真',155.5*sx,1384.5*sy,round(78*sx))]
 n=[1,1,2,3][i-1];skills=[]
 for name,cy in zip(names[:n],[961,1045,1129][-n:]):
  level='+1' if i<3 else '+2';f1=ImageFont.truetype(fontpath,round(38*sx));f2=ImageFont.truetype(fontpath,round(35*sx))
  b1=dr.textbbox((0,0),name,font=f1);b2=dr.textbbox((0,0),level,font=f2);w1=b1[2]-b1[0];w2=b2[2]-b2[0];w=w1+w2+12;cent=((944-202+13)+933)/2*sx;left=cent-w/2
  rows.append(put(dr,name,left+w1/2,cy*sy,round(38*sx))); rows.append(put(dr,level,left+w1+12+w2/2,cy*sy,round(35*sx)));skills.append({'name':name,'level':level})
 # compact shield/pole troop icon inside lower right circular socket
 x,y=round(900*sx),round(1424*sy)
 dr.polygon([(x-22,y-19),(x+22,y-19),(x+20,y+15),(x,y+31),(x-20,y+15)],fill='#fff7df',outline='#302310',width=3)
 dr.line((x,y-34,x,y+28),fill='#302310',width=5);dr.polygon([(x,y-46),(x-7,y-30),(x+7,y-30)],fill='#fff7df',outline='#302310')
 tx.save(D/f'{tier}-text.png')
 pure=Image.open(R/'raw'/f'card0{i}.png').convert('RGBA');can=Image.new('RGBA',S);can.paste(pure,(84,145));art=Image.new('RGBA',S);art.paste(can,(0,0),mask)
 out=Image.alpha_composite(Image.alpha_composite(art,frame),tx);out.save(R/f'于禁-卡{i}-{tier}.png')
 reg=(slice(145,1681),slice(84,1108));valid=(np.array(mask)[reg]==255)&(np.array(frame.getchannel('A'))[reg]==0)&(np.array(tx.getchannel('A'))[reg]==0)
 change=int(np.sum(np.any(np.array(out)[reg]!=np.array(pure),axis=2)&valid));assert change==0
 cfg[tier]={'country':'魏','title':'于禁','level':'1','advancement':'真','skills':skills,'draft':True}
 manifest['cards'][tier]={'source':f'raw/card0{i}.png','output':f'于禁-卡{i}-{tier}.png','source_sha256':hashlib.sha256((R/'raw'/f'card0{i}.png').read_bytes()).hexdigest(),'native_size':list(pure.size),'uncovered_native_pixels_changed':change,'text_alignment':rows}
for i,title in enumerate(['西寨可取','军务在前','号令入阵'],1):
 src=R/'raw'/f'bio0{i}.png';out=R/f'于禁-传记{i}-{title}.png';shutil.copy2(src,out);manifest['stories'][str(i)]={'source':str(src.relative_to(R)),'output':out.name,'native_size':list(Image.open(src).size),'destination_stage':i+1}
(D/'ui-config.json').write_text(json.dumps(cfg,ensure_ascii=False,indent=2))
(R/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
# Overview only is resized; delivered seven assets preserve original artwork pixels.
sheet=Image.new('RGB',(1680,1240),'#17212c');dd=ImageDraw.Draw(sheet);f=ImageFont.truetype(fontpath,23)
for i,t in enumerate(['iron','bronze','silver','gold'],1):
 im=Image.open(R/f'于禁-卡{i}-{t}.png').convert('RGBA');im.thumbnail((420,650));sheet.paste(im,((i-1)*420,20),im)
for i,title in enumerate(['西寨可取','军务在前','号令入阵'],1):
 im=Image.open(R/f'于禁-传记{i}-{title}.png');im.thumbnail((550,367));sheet.paste(im,((i-1)*560,720));dd.text(((i-1)*560+15,1095),title+' → '+['青铜','白银','黄金'][i-1],font=f,fill='white')
dd.text((20,665),'于禁 · 四阶三传记 · 全部为候选 / 魏收藏蓝徽固定',font=f,fill='white')
dd.text((20,1150),'原画：四卡1024×1536 / 三传记1536×1024；UI画布1190×1786，插画原像素合成。',font=f,fill='#c2c9d4')
dd.text((20,1190),'镇阵石犀、能量和技能为原创设计；演义第10、11、16、30回事件。',font=f,fill='#c2c9d4')
sheet.save(R/'于禁-七图总览.png')
print('done')
