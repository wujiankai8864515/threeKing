from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,hashlib,shutil
P=Path(__file__).resolve().parent
names=['01-黑铁-南阳督粮','02-青铜-玉玺入掌','03-白银-仲氏僭号','04-黄金-七军帝胄','05-传记-印换江东兵','06-传记-一意称尊','07-传记-七路发兵']
font=ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',23)
sheet=Image.new('RGB',(1800,1400),'#20262c');d=ImageDraw.Draw(sheet);d.text((25,12),'袁术 · 四阶三传记 · 重做候选（原创鎏甲金蟾／技能草案）',font=font,fill='white')
src=[P/'ui'/f'{i:02d}-{t}-UI排版修复1190.png' for i,t in enumerate(['黑铁','青铜','白银','黄金'],1)]+[P/'raw'/f'story{i:02d}.png' for i in range(1,4)]
m={'hero':'袁术','faction':'群','status':'候选待审，非用户通过','engine':'built-in image_gen','sources':[f'https://zh.wikisource.org/zh/三國演義/第{n:03d}回' for n in [5,15,17]],'art_resampling':'none; cards 1024x1536 at1:1 offset84,145 on1190x1786','assets':[]}
for i,(name,s) in enumerate(zip(names,src)):
 dest=P/'candidates'/(name+'.png');shutil.copy2(s,dest);im=Image.open(dest).convert('RGBA');im.thumbnail((440,660) if i<4 else (585,390));x=10+i*448 if i<4 else 10+(i-4)*595;y=55 if i<4 else 770;sheet.paste(im,(x,y),im);d.text((x+5,y+im.height+8),name,font=font,fill='white')
 raw=P/'raw'/(f'card{i+1:02d}.png' if i<4 else f'story{i-3:02d}.png')
 m['assets'].append({'id':name,'raw':str(raw),'candidate':str(dest),'native_size':list(Image.open(raw).size),'candidate_size':list(Image.open(dest).size),'sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'target_card':None if i<4 else f'card{i-2:02d}'})
 Image.open(raw).crop((0,0,1024,700)).save(P/'qa'/f'{i+1:02d}-upper-100pct.png');Image.open(raw).crop((0,600,1024,min(1300,Image.open(raw).height))).save(P/'qa'/f'{i+1:02d}-hands-100pct.png')
for j,t in enumerate(['南阳督粮 → 玉玺入掌 → 仲氏僭号 → 七军帝胄；三传记关联铜、银、金。','鎏甲金蟾、玉印纹、冠甲为原创神话设计，无原著神兵坐骑专名。','蓄资：初始储备增加；厚赏：增益持续延长；虚盛：有储备时防御提高。','主动草案：消耗自身储备，为一名友军短时提高攻击。']):d.text((25,1210+j*40),t,font=font,fill='white')
sheet.save(P/'袁术-四阶三传记-重做总览.png');(P/'manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2))
(P/'research'/'核验说明.md').write_text('原著第5回总督粮草，第15回孙策以玉玺质借兵，第17回拒阎象之谏称仲氏、乘龙凤辇，随后七路出兵且本人接应；本套不画获胜，不用已撤回江亭残梦。黄金金甲有原文依据，双刀改作鞘中佩饰。玉玺并非本命神兵；鎏甲金蟾、权能和冠服造型均项目原创神话解释。传记为同一事件前因与转折的压缩构图，第三传记仍处黄金装备领取前。\n'+'\n'.join(m['sources']))
(P/'qa'/'QA.md').write_text('7张原图均逐张查看，4卡UI预览再次查看。黑铁首版照片感弃用，重绘为清晰动画；黄金原冠成长不足，内置imagegen局部修冠，失败版保留。脸与短须身份统一，手指与盒印结构清楚，未遮脸手。冠服和神兽逐级成长，未撒金粉。4卡原生1024×1536，3传记1536×1024；UI1190×1786原画1:1不缩小。群紫徽固定，盾形君主支援兵种图标，1至4星，槽位961/1045/1129，1/1/2/3被动，二字单效果草案。所有结果候选待用户审核。\n')
(P/'progress.json').write_text(json.dumps({'stage':'ready_for_library','raw_assets':7,'candidate_only':True}))
