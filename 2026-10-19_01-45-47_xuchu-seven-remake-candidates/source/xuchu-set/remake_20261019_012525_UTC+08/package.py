from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,shutil,hashlib
D=Path(__file__).resolve().parent
names=['01-黑铁-葛陂压阵','02-青铜-初刀入军','03-白银-举鞍渡险','04-黄金-虎痴裸衣','05-传记-解缚入帐','06-传记-一跃上舟','07-传记-卸甲再战']
files=[]
for i,n in enumerate(names):
 src=sorted(D.glob('ui/*修复1190.png'))[i] if i<4 else D/f'raw/story{i-3:02d}.png'
 dst=D/'deliverables'/f'许褚-{n}.png';shutil.copy2(src,dst);files.append(dst)
font=ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',25)
sheet=Image.new('RGB',(1800,1380),'#19212b');dr=ImageDraw.Draw(sheet)
for i,f in enumerate(files):
 im=Image.open(f).convert('RGBA');im.thumbnail((440,670) if i<4 else (585,400))
 x=i*450+(450-im.width)//2 if i<4 else (i-4)*600+(600-im.width)//2;y=25 if i<4 else 775
 sheet.paste(im,(x,y),im);dr.text((x,y+im.height+6),names[i],font=font,fill='white')
dr.text((25,1220),'许褚 · 全新四卡三传记候选｜白额厚鬃重虎为原创神话意象｜技能草案',font=font,fill='#dfd3b3')
dr.text((25,1265),'第12回：葛陂、归曹 → 第58回：护主渡险 → 第59回：裸衣斗超',font=font,fill='white')
dr.text((25,1310),'原生：卡面1024×1536，传记1536×1024；UI1190×1786，未放大插画',font=font,fill='white')
sheet.save(D/'deliverables/许褚-全套七图总览.png');files.append(D/'deliverables/许褚-全套七图总览.png')
for i in range(1,5):
 im=Image.open(D/f'raw/card{i:02d}.png')
 for k,b in {'face':(280,80,760,530),'grips':(100,250,1024,900),'body':(0,600,1024,1536)}.items():im.crop(b).save(D/f'QA/card{i:02d}-{k}.png')
sourceids=['67540921-bc8b-4b29-bff5-3ae376c67ce8','e2849a50-c2dc-4936-9cb4-1b8b1447409a','4e9cfefa-3a22-40eb-aab9-554e81d1b93c','f328fb8d-fec0-4382-a993-b23be93b2da5','04b46a4f-f056-4724-9752-49e837037774','d1118612-fe32-4167-b0cf-5dbb288dafdb','9d0a2b6c-fbf9-4181-9f05-cdb98df7fe22']
manifest={'hero':'许褚','status':'candidate_awaiting_user','tool':'built-in image_gen','faction':'四阶收藏统一蓝底魏，黑铁为乡勇事件','skills_draft':{'主动 重斩':'短暂明示蓄力后对当前近身单体作一次高伤刀斩；蓄力时防御降低，结束恢复','蛮力':'攻击力提高','虎骨':'最大生命提高','凝力':'主动蓄力时间缩短'},'source_map':[],'files':[],'failures':['黑铁和青铜首版脸型接近典韦，已改为圆阔脸包头短平髭，原稿保留','story03首次工具读取参考图传输中断，同范围重试成功'],'notes':['神虎、护甲纹样及刀外形为原创演绎；不虚构刀马专名','黑铁投石画为大石视觉夸张，非声称原著石块规格','青铜与金卡自然坐骑握持，长刀轴连续，刀尖允许出画','金卡选择弃刀夺枪之前，不画马超战败','白银虎体大部隐于雾，不虚称完整清晰全兽','兵种图标为暂用重装近战UI符号，非演义军制证据']}
for i,f in enumerate(files):
 manifest['files'].append({'path':str(f),'size':list(Image.open(f).size),'sha256':hashlib.sha256(f.read_bytes()).hexdigest()})
 if i<7:
  raw=D/f'raw/card{i+1:02d}.png' if i<4 else D/f'raw/story{i-3:02d}.png'
  manifest['source_map'].append({'asset':names[i],'raw':str(raw),'generated_original':'generated_images/exec-'+sourceids[i]+'.png','native_size':list(Image.open(raw).size),'output':str(f)})
(D/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
(D/'library-request.json').write_text(json.dumps({'uploads':[{'file_name':f.name,'file_size_bytes':f.stat().st_size,'workspace_path':str(f),'purpose':'create_library_file','mime_type':'image/png','library_artifact_type':'image_gen' if i<7 else 'image'} for i,f in enumerate(files)]},ensure_ascii=False,indent=2))
(D/'research/sources.md').write_text('核验：2026-10-19 UTC+08。\n第12回 https://zh.wikisource.org/zh/三國演義/第012回 ：葛陂许褚、大刀、飞石、曹操解缚、初战斩李封。\n第58回 https://zh.wikisource.org/zh/三國演義/第058回 ：负曹跃船、撑篙、左手举鞍遮护、两腿夹舵。\n第59回 https://zh.wikisource.org/zh/三國演義/第059回 ：先换马，再久斗、卸甲裸衣再战，之后才弃刀夺枪。\n神虎为依据虎痴/虎侯原创设计，无原著实兽或神兽坐骑证据。马仅用高大深褐军马，不设专名。\n')
(D/'QA.md').write_text('全部七张逐张查看。原生竖1024×1536/横1536×1024。脸型统一圆阔脸、厚颈、平短髭、黄褐包头低结，区别典韦方脸整圈短须高髻。双手抱石、双手直柄刀、举鞍撑篙、背人跃舟均结构清晰。\n黑铁、青铜首版因身份撞脸淘汰，留failures。后续不沿用该旧脸。神虎黄褐白额低伏，与张飞黑红断喝虎区别。\nUI独立金属框和字层，1/1/2/3被动底向上锚定961/1045/1129，名字许褚、魏蓝收藏徽、1至4星、兵种图标；数值为排版示例、技能为草案。黄金继承脚本误染徽边圈已去除。插画在UI内1:1，无遮挡原像素差异0。\n主角脸手未被被动UI遮挡；黄金被动板在马脸右部有重叠，属当前固定UI与骑战构图的待审折衷，未缩小主角。\n所有图片候选待用户审核，不等于用户通过。\n')
print(len(files))
