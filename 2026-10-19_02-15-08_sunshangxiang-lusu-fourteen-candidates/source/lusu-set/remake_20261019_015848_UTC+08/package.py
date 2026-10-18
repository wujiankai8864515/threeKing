from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,hashlib,shutil
D=Path(__file__).resolve().parent; O=D/'deliverables';O.mkdir(exist_ok=True)
labels=['01-黑铁-江东献策','02-青铜-渡江联刘','03-白银-力主拒曹','04-黄金-临江守议','05-传记-两岸相通','06-传记-独陈战策','07-传记-席前陈理']
sources=[D/'ui'/f'{x}-UI排版修复1190.png' for x in ['01-黑铁','02-青铜','03-白银','04-黄金']]+[D/'raw'/f'bio0{i}.png' for i in range(1,4)]
manifest={'hero':'鲁肃','status':'全新候选，待用户审核','generator':'built-in imagegen','native_cards':[1024,1536],'native_stories':[1536,1024],'ui_canvas':[1190,1786],'art_resampling':'none; 1:1 at84,145','myth':'双首比翼鹭：原创艺术解释，不是原著人物神兽；银金明确单一双首构形','active_draft':'使两名友军链接，分担下一次伤害，触发一次后结束','passives_draft':{'合援':'降低链接分担的一次伤害','笃盟':'延长链接等待触发的持续时间','安众':'缩短相邻友军受控时长'},'chronology':[29,42,43,66],'source_urls':[f'https://zh.wikisource.org/wiki/三國演義/第{x}回' for x in ['029','042','043','066']],'story_links':{'bio01':'card02','bio02':'card03','bio03':'card04'},'repairs':['黑铁将手收回中央，旧稿保留','白银双鹭修为双首单体','黄金手收回中央、双首单体强化'],'files':[]}
for label,src in zip(labels,sources):
 p=O/(label+'.png');shutil.copy2(src,p)
 manifest['files'].append({'file':str(p),'source':str(src),'dimensions':Image.open(p).size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
F='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc';font=ImageFont.truetype(F,24)
sheet=Image.new('RGB',(1680,1300),'#20262d');draw=ImageDraw.Draw(sheet)
for i in range(4):
 im=Image.open(sources[i]).convert('RGBA');im.thumbnail((410,630));sheet.paste(im,(i*420+(420-im.width)//2,10),im);draw.text((i*420+32,650),labels[i],font=font,fill='white')
for i in range(3):
 im=Image.open(sources[4+i]).convert('RGB');im.thumbnail((550,400));sheet.paste(im,(i*560,710));draw.text((i*560+20,1090),labels[4+i],font=font,fill='white')
draw.text((30,1170),'鲁肃｜四卡三传记 · 原创神话候选，待审核',font=font,fill='#e9c998')
draw.text((30,1210),'29回献策 → 42回联刘 → 43回拒曹 → 66回席间交涉',font=font,fill='white')
draw.text((30,1250),'双首鹭灵、冠服与技能为艺术/玩法拟案；第66回不改写演义会谈胜负。',font=font,fill='#c8c9cd')
sheet.save(O/'08-鲁肃-七图总览.jpg',quality=94)
qa=Image.new('RGB',(1600,800),'#20262d')
for i in range(4):
 im=Image.open(D/'raw'/f'card0{i+1}.png');cr=im.crop((230,100,630,500));cr.save(D/'qa'/f'card0{i+1}-face.png');qa.paste(cr,(i*400,0))
 im=Image.open(sources[i]);qa.paste(im.crop((760,1030,1160,1430)),(i*400,400))
qa.save(D/'qa'/'face-ui-native-crops.jpg',quality=94)
(D/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
(D/'research'/'verified-notes.md').write_text('核验日期2026-10-19 UTC+08。\n29回：周瑜荐鲁肃，夜半同榻议江东与长江。黑铁日景木图为该阶段艺术凝练，非原著夜半逐镜复刻。\n42回：鲁肃主动求联刘，与孔明登舟往柴桑。\n43回：张昭等退出，鲁肃入见力劝，孙权仍沉吟。\n66回：临江亭赴会索荆州，原著鲁肃后来受制于关羽；本组只画席间陈理，绝不宣称鲁肃获胜或擒关羽。\n四条原文链接见manifest source_urls。冠服递增与双首比翼鹭均原创；无原著专名兵器/名马。')
(D/'QA.md').write_text('四张原生1024×1536，三张原生1536×1024；全部逐张目检。脸型短须与宽厚身形连续；银金单体双首鹭连接明确。黑铁黄金手势已移离右下被动。船上与席间手势自然，黄金会谈无俘虏与胜利改写。固定吴橘红收藏徽。UI沿用紧凑金属框，961/1045/1129共同锚点，被动1/1/2/3，姓名和等级动态字层。舰船兵种图标为江东水路外交支援拟案。所有技能等级均拟案。黑铁首图与银金修前图存failures。全部候选待审核。')
print(O)
