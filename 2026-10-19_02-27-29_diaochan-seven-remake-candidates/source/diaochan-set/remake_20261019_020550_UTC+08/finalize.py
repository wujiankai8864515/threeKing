from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,hashlib,shutil
p=Path(__file__).parent
font=ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',26)
labels=['庭月闻乱','席前定意','入府藏心','凤亭裂盟','画阁受计','车帘隔旧门','一柄戟转向']
files=[]
for i,tier in enumerate(['黑铁','青铜','白银','黄金'],1):
 f=p/'candidates'/f'貂蝉-card{i:02d}-{tier}.png';shutil.copy2(p/'ui'/f'{i:02d}-{tier}-UI排版修复1190.png',f);files.append(f)
for i in range(1,4):
 f=p/'candidates'/f'貂蝉-bio{i:02d}.png';shutil.copy2(p/'raw'/f'bio{i:02d}.png',f);files.append(f)
sheet=Image.new('RGB',(1800,1200),'#171d2b');d=ImageDraw.Draw(sheet)
for i,f in enumerate(files):
 im=Image.open(f).convert('RGBA')
 if i<4:im.thumbnail((440,660));pos=(i*450+(450-im.width)//2,40)
 else:im.thumbnail((580,390));pos=((i-4)*600+(600-im.width)//2,770)
 sheet.paste(im,pos,im);d.text((pos[0]+10,pos[1]-34),labels[i],font=font,fill='#eee9df')
d.text((20,1160),'貂蝉 · 四阶三传记候选 · 成年化原创改编 / 银蛾为原创象征 / 技能为草案',font=font,fill='#d1bedf');sheet.save(p/'貂蝉-七图总览.png')
qa=Image.new('RGB',(1600,900),'#1d1d26')
for i in range(4):
 im=Image.open(p/'raw'/f'card{i+1:02d}.png');box=[(285,100,650,465),(300,120,665,485),(220,130,585,495),(100,70,465,435)][i];qa.paste(im.crop(box),(i*400,20));ui=Image.open(files[i]);qa.paste(ui.crop((760,1020,1130,1390)).convert('RGB'),(i*400,480))
qa.save(p/'qa/face-and-passive-100percent.png')
assets=[]
for i,f in enumerate(files):
 raw=p/'raw'/(f'card{i+1:02d}.png' if i<4 else f'bio{i-3:02d}.png')
 assets.append({'title':labels[i],'candidate':str(f),'raw':str(raw),'native_dimensions':list(Image.open(raw).size),'delivery_dimensions':list(Image.open(f).size),'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'target_stage':None if i<4 else i-2,'status':'candidate_awaiting_user_review'})
manifest={'hero':'貂蝉','collection_faction':'群','faction_badge':'fixed purple four cards','adult_adaptation_age':26,'generator':'built-in image_gen','raw_count':7,'not_upscaled':True,'card_ui':'native 1024x1536 art placed 1:1 into 1190x1786 frame; configurable independent frame and text layers','source':'https://zh.wikisource.org/zh/三國演義/第008回','mythology':'original lunar silver moth and split moon symbolism; not canonical spells','skills':'research/skills.json; proposed simple single effects','assets':assets,'qa':{'all_seven_viewed':True,'all_four_composites_viewed':True,'adult_face_and_natural_hands':True,'no_UI_face_hand_overlap':True,'no_photo_or_gold_dust':True,'bio03_halberd_head_corrected':True,'failures_retained':2,'remaining_review_notes':['服饰成长相对克制，以镜头、月影与黄金完整银蛾增强阶位；候选待用户审阅。']}}
(p/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
(p/'qa/progress.json').write_text(json.dumps({'status':'seven_complete_QA_library_pending','raw_count':7,'ui_count':4},indent=2))
(p/'failures/log.md').write_text('1. card01-too-semi-realistic.png：初版半写实倾向，依据认可关张画风重绘为动画块面。\n2. bio03-wrong-glaive-head.png：原图持偃月刀头不符画戟，已单独修复为直尖与双月牙戟头。\n')
print(json.dumps([str(f.resolve()) for f in files]+[str((p/'貂蝉-七图总览.png').resolve())],ensure_ascii=False))
