from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,shutil,hashlib
D=Path(__file__).resolve().parent
font=ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',25)
names=['01-黑铁-天水识阵','02-青铜-择途归蜀','03-白银-灯下承书','04-黄金-洮西返阵','05-传记-山路受知','06-传记-一卷千钧','07-传记-背水回锋']
files=[]
for i,n in enumerate(names):
 src=sorted(D.glob('ui/*修复1190.png'))[i] if i<4 else D/f'raw/story{i-3:02d}.png'
 dst=D/'candidates'/f'姜维-{n}.png';shutil.copy2(src,dst);files.append(dst)
sheet=Image.new('RGB',(1800,1460),'#182126');dr=ImageDraw.Draw(sheet)
for i,f in enumerate(files):
 im=Image.open(f).convert('RGBA'); im.thumbnail((440,670) if i<4 else (585,400))
 x=i*450+(450-im.width)//2 if i<4 else (i-4)*600+(600-im.width)//2;y=50 if i<4 else 820
 sheet.paste(im,(x,y),im);dr.text((x,y+im.height+8),names[i],font=font,fill='white')
dr.text((25,1270),'姜维 · 全新七图候选｜玄甲麒麟为原创艺术演绎｜技能为草案',font=font,fill='#d5c7a1')
dr.text((25,1310),'第93回：识阵、归蜀 → 第104回：承书 → 第110回：洮西回军',font=font,fill='white')
dr.text((25,1350),'原生插画：卡面1024×1536，传记1536×1024；UI画布1190×1786，无插画放大',font=font,fill='white')
sheet.save(D/'姜维-全套七图总览.png')
for i in range(1,5):
 im=Image.open(D/f'raw/card{i:02d}.png'); im.crop((200,150,800,750)).save(D/f'qa/card{i:02d}-face-region.png')
manifest={'hero':'姜维','status':'candidate_awaiting_user','tool':'built-in image_gen','files':[],'mythic':'玄甲麒麟为原创艺术解释，非史实/原著神兽','chronology':'收藏四阶统一蜀，黑铁事件服属魏；青铜归蜀；白银承书；黄金洮西胜利，不宣称狄道攻克或北伐完成','skills_draft':{'主动 破阵':'对指定一敌作一次枪击','识阵':'对被标记目标主动伤害提高','继志':'释放主动后恢复自身少量能量','整旅':'相邻友军防御提高'},'failures':['card01-too-photographic.png：初版偏写实，使用认可关羽风格定向重绘','card02-zhuge-too-old.png：青铜诸葛亮过老，定向修改为中年黑发须'],'qa':'逐图已查看；脸骨相稳定，持枪长杆直线贯通，传记03双手分握与武器贯通；银阶双手承卷；远景降对比；无金粉。黄金仍为战马，麒麟为后方权能。'}
for f in files+[D/'姜维-全套七图总览.png']:
 im=Image.open(f);manifest['files'].append({'path':str(f),'size':list(im.size),'sha256':hashlib.sha256(f.read_bytes()).hexdigest()})
(D/'index.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
(D/'QA.md').write_text('全部七图逐一查看。四阶成长与三传记阶段关联见research.json；原图逐张独立生成。原生尺寸与SHA256见index.json。\nUI沿用认可紧凑组件，技能名二字，底部固定向上增长，名字等级按字形居中。一二三四为阶级圆章。LV1为排版示例。\n两次失败与修订均保留。当前全部为用户待审候选，不代表用户认可。\n')
