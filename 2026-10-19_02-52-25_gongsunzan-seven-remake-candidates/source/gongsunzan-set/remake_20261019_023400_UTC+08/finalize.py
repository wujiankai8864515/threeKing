from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,hashlib,shutil
P=Path(__file__).resolve().parent
names=['01-黑铁-北平赴盟','02-青铜-磐河问盟','03-白银-白马回阵','04-黄金-借兵济徐','05-传记-桥上决裂','06-传记-重整白骑','07-传记-二千兵相助']
font=ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',23)
sheet=Image.new('RGB',(1800,1400),'#20262c');d=ImageDraw.Draw(sheet);d.text((25,12),'公孙瓒 · 四阶三传记 · 重做候选（北风白泽为原创／技能草案）',font=font,fill='white')
src=[P/'ui'/f'{i:02d}-{t}-UI排版修复1190.png' for i,t in enumerate(['黑铁','青铜','白银','黄金'],1)]+[P/'raw'/f'story{i:02d}.png' for i in range(1,4)]
m={'hero':'公孙瓒','faction':'群','status':'候选待审，非用户通过','engine':'built-in image_gen','sources':[f'https://zh.wikisource.org/wiki/三國演義/第{n:03d}回' for n in [5,7,11]],'art_resampling':'none; cards1024x1536 at1:1 offset84,145 on1190x1786','assets':[]}
for i,(name,s) in enumerate(zip(names,src)):
 dest=P/'candidates'/(name+'.png');shutil.copy2(s,dest);im=Image.open(dest).convert('RGBA');im.thumbnail((440,660) if i<4 else (585,390));x=10+i*448 if i<4 else 10+(i-4)*595;y=55 if i<4 else 770;sheet.paste(im,(x,y),im);d.text((x+5,y+im.height+8),name,font=font,fill='white')
 raw=P/'raw'/(f'card{i+1:02d}.png' if i<4 else f'story{i-3:02d}.png')
 m['assets'].append({'id':name,'raw':str(raw),'candidate':str(dest),'native_size':list(Image.open(raw).size),'candidate_size':list(Image.open(dest).size),'sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'target_card':None if i<4 else f'card{i-2:02d}'})
 Image.open(raw).crop((0,0,Image.open(raw).width,700)).save(P/'qa'/f'{i+1:02d}-upper-100pct.png')
for j,t in enumerate(['北平赴盟 → 磐河问盟 → 白马回阵 → 借兵济徐；三传记关联铜、银、金。','北风白泽、冠甲与长枪造型为原创；白马无专名，非赵云银龙或马超西凉。','整骑：附近骑兵移速提高；引弦：首次远程普攻伤害提高；复阵：移动后短时防御提高。','主动草案：近旁骑兵短时加速；黄金事件是借刘备两千马步军，不是三千白骑。']):d.text((25,1210+j*40),t,font=font,fill='white')
sheet.save(P/'公孙瓒-四阶三传记-重做总览.png');(P/'manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2))
(P/'progress.json').write_text(json.dumps({'stage':'ready_for_library','raw_assets':7,'candidate_only':True}))
