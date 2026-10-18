from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,hashlib,shutil
P=Path(__file__).resolve().parent
names=['01-黑铁-剑对权臣','02-青铜-盟坛立旄','03-白银-冀州门开','04-黄金-黎阳旌羽','05-传记-众推一盟主','06-传记-冀州来书','07-传记-檄成而军动']
font=ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',23)
sheet=Image.new('RGB',(1800,1400),'#20262c');d=ImageDraw.Draw(sheet);d.text((25,12),'袁绍 · 四阶三传记 · 重做候选（原创百旒金翟／技能草案）',font=font,fill='white')
src=[P/'ui'/f'{i:02d}-{t}-UI排版修复1190.png' for i,t in enumerate(['黑铁','青铜','白银','黄金'],1)]+[P/'raw'/f'story{i:02d}.png' for i in range(1,4)]
m={'hero':'袁绍','faction':'群','status':'候选待审，非用户通过','engine':'built-in image_gen','sources':[f'https://zh.wikisource.org/zh/三國演義/第{n:03d}回' for n in [3,5,7,22]],'art_resampling':'none; cards 1024x1536 at1:1 offset84,145 on1190x1786','assets':[]}
for i,(name,s) in enumerate(zip(names,src)):
 dest=P/'candidates'/(name+'.png');shutil.copy2(s,dest);im=Image.open(dest).convert('RGBA');im.thumbnail((440,660) if i<4 else (585,390));x=10+i*448 if i<4 else 10+(i-4)*595;y=55 if i<4 else 770;sheet.paste(im,(x,y),im);d.text((x+5,y+im.height+8),name,font=font,fill='white')
 raw=P/'raw'/(f'card{i+1:02d}.png' if i<4 else f'story{i-3:02d}.png')
 m['assets'].append({'id':name,'raw':str(raw),'candidate':str(dest),'native_size':list(Image.open(raw).size),'candidate_size':list(Image.open(dest).size),'sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'target_card':None if i<4 else f'card{i-2:02d}'})
 Image.open(raw).crop((0,0,1024,700)).save(P/'qa'/f'{i+1:02d}-upper-100pct.png');Image.open(raw).crop((0,600,1024,min(1300,Image.open(raw).height))).save(P/'qa'/f'{i+1:02d}-hands-100pct.png')
for j,t in enumerate(['拔剑抗董 → 诸侯盟主 → 入主冀州 → 黎阳发军；三传记关联铜、银、金。','百旒金翟、旗羽纹、冠甲为原创神话设计，无原著神兵坐骑专名。','合射：单箭伤害提高；列旗：目标范围提高；余矢：主动能耗降低。','主动草案：最多三名不同敌人各射一次；余箭不转单体连射。']):d.text((25,1210+j*40),t,font=font,fill='white')
sheet.save(P/'袁绍-四阶三传记-重做总览.png');(P/'manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2))
(P/'research'/'核验说明.md').write_text('2026-10-19 UTC+08 核验原著第3回147行袁绍拔剑与董卓筵上对峙；第5回151行曹操提议、众推盟主，三层坛白旄黄钺，整衣佩剑登坛；第7回118行逢纪计、韩馥使者来请、袁绍入冀州夺权，韩馥悔去，不是幸福退隐；第22回121至123行议军三十万往黎阳，陈琳草檄。传记为事件压缩构图，礼节交接、手卷与地图为艺术具体化。黄金描写军势动员，绝非官渡或乌巢获胜。\n百旒金翟、旗羽纹、冠甲、仪杖与技能均原创游戏设定，非原著神兽或血统。无专名战马；不把袁绍本人画为百箭弓神。\n'+ '\n'.join(m['sources']))
(P/'qa'/'QA.md').write_text('七图逐张查看，4卡加UI再次查看；银金追加冠甲成长修正，黄金鸟头与左手内移。两张首版成长不足图保留failures。四卡原生1024×1536，三传记1536×1024；无4K宣称。独立UI 1190×1786，原画1:1未缩小，未覆盖像素差0。固定群紫徽、弓兵矢量icon、1至4星、锚点961/1045/1129，被动1/1/2/3条，姓名等级字形居中。三传记关联目标阶段而非装备已领取，最后传记甲仍为领取前。技能为候选草案。\n')
(P/'progress.json').write_text(json.dumps({'stage':'ready_for_library','raw_assets':7,'candidate_only':True}))
