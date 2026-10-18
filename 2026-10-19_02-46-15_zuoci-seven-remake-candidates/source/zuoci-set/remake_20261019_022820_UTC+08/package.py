from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,hashlib,shutil
p=Path(__file__).parent
tiers=['黑铁','青铜','白银','黄金'];titles=['山脚一肩','牢中自若','池畔钓远鱼','山羊归路']
files=[]
for i,t in enumerate(tiers,1):
 f=p/'candidates'/f'左慈-卡{i:02}-{t}.png'
 shutil.copy2(p/'ui'/f'{i:02}-{t}-UI排版修复1190.png',f);files.append(f)
for i,t in enumerate(['问术入囚','筵间问所缺','一步入群羊'],1):
 f=p/'candidates'/f'左慈-传记{i:02}-{t}.png';shutil.copy2(p/'raw'/f'bio{i:02}.png',f);files.append(f)
font=ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',26)
sheet=Image.new('RGB',(1920,1260),'#21252b');d=ImageDraw.Draw(sheet)
for i,f in enumerate(files[:4]):
 im=Image.open(f).convert('RGBA');im.thumbnail((470,705));sheet.paste(im,(i*480+(480-im.width)//2,40),im);d.text((i*480+30,752),titles[i],font=font,fill='white')
for i,f in enumerate(files[4:]):
 im=Image.open(f);im.thumbnail((620,414));sheet.paste(im,(i*640+10,810));d.text((i*640+20,1225),f.stem.replace('左慈-',''),font=font,fill='white')
d.text((25,3),'左慈 · 四阶卡与三段关联传记 · 候选待审',font=font,fill='#dbc8a0')
overview=p/'candidates'/'左慈-七图总览.png';sheet.save(overview)
qa=Image.new('RGB',(1400,800),'#23272c')
for i in range(4):
 im=Image.open(p/'raw'/f'card{i+1:02}.png');im.crop([(290,100,570,380),(340,130,620,410),(280,100,560,380),(300,80,580,360)][i]).save(p/'qa'/f'face{i+1}.png');qa.paste(Image.open(p/'qa'/f'face{i+1}.png'),(i*350,30))
for i in range(3):
 im=Image.open(p/'raw'/f'bio{i+1:02}.png');im.crop((260,70,660,470)).resize((350,350)).save(p/'qa'/f'bioface{i+1}.png');qa.paste(Image.open(p/'qa'/f'bioface{i+1}.png'),(i*450,400))
qa.save(p/'qa'/'七图面部一致性.png')
manifest={'hero':'左慈','status':'candidate_pending_user_review','generator':'built-in image_gen','actual_native_cards':[1024,1536],'actual_native_stories':[1536,1024],'card_composite':[1190,1786],'no_4k_claim':True,'source':'https://zh.wikisource.org/zh-hant/三國演義/第068回','source_verified':'2026-10-18','original_adaptations':['左眼视损/右腿略跛的侧别为原创连续性，原文未指定','蜃壳幻潮、冠袍成长和技能为原创拟定','黄金止于羊群故事，不使用稍后的白鹤'],'skills_draft':{'active':'幻身：于身旁空位留下一个短时幻影，转承下一次可转移的单体普攻后消失','passives':{'留影':'未触发幻影保留时间提高','轻履':'移动速度提高','远映':'幻影放置距离提高'},'counts':[1,1,2,3],'numeric_levels':'展示草案非平衡定案'},'story_links':{'bio01':'card02','bio02':'card03','bio03':'card04'},'qa':{'all_seven_visually_inspected':True,'eye_side':'correct anatomical left clouded in all seven','hands':'yoke and fishing pole coherent; gestures readable','faces':'natural narrow elderly face consistent','UI':'group purple fixed; magic icon; anchors 961/1045/1129; independent frame and text; face/hands unobscured','minor_limitations':['近景羊毛和远山细节仍丰富，非全局虚化','原著神异情节仅作幻想视觉演绎']},'files':[]}
for f in files+[overview]:
 im=Image.open(f);manifest['files'].append({'path':str(f.resolve()),'size':list(im.size),'sha256':hashlib.sha256(f.read_bytes()).hexdigest()})
(p/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
(p/'sources-and-chronology.md').write_text('第68回线性取景：代挑柑担→被曹操疑忌入囚→枷落七日→宴问所缺、索钓竿→堂下池中取松江鲈→追捕入群羊→还羊离去。已重开维基文库繁体版本验证；原zh路径打不开，保留此失败说明。小说神异不作现实效验指导。蜃壳幻潮、阶级造型和技能为原创。\n')
(p/'failures'/'README.md').write_text('保留首轮偏写实图、眼侧错误图以及末传记无据法杖版本；均未作为最终候选交付。后续用内置imagegen纠正。\n')
(p/'progress.json').write_text(json.dumps({'status':'seven_candidates_QA_complete_ready_for_library','completed':7},ensure_ascii=False))
print(json.dumps([str(f.resolve()) for f in files+[overview]],ensure_ascii=False))
