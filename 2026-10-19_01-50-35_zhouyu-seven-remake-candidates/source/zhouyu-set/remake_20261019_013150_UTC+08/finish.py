from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,hashlib,shutil
p=Path(__file__).parent
names=['01-黑铁-历阳知交','02-青铜-江东新托','03-白银-受剑立令','04-黄金-赤壁总攻','05-黑铜传记-灵前再受重托','06-铜银传记-四忌决战','07-银金传记-六路与火船']
ui=['01-黑铁','02-青铜','03-白银','04-黄金']
assets=[]
for i,n in enumerate(names):
 src=p/'ui'/f'{ui[i]}-UI排版修复1190.png' if i<4 else p/'raw'/f'story0{i-2}.png'
 dest=p/'candidates'/f'周瑜-{n}-重制候选.png';shutil.copy2(src,dest)
 im=Image.open(dest)
 assets.append({'id':i+1,'file':str(dest),'dimensions':list(im.size),'sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'status':'candidate_awaiting_user','target_stage':None if i<4 else i-2})
font=ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',24)
sheet=Image.new('RGB',(1920,1190),'#20252a');d=ImageDraw.Draw(sheet)
for i,a in enumerate(assets):
 im=Image.open(a['file']).convert('RGBA')
 if i<4:
  im=im.resize((480,720));xy=(480*i,35)
 else:
  im=im.resize((640,427));xy=(640*(i-4),763)
 sheet.paste(im,xy,im)
 d.text((xy[0]+15,xy[1]+5), names[i],font=font,fill='#fff5dc',stroke_width=2,stroke_fill='#20252a')
d.text((20,0),'周瑜 · 四阶三传记 · 原创神话改编候选 · 技能/等级为示意',font=font,fill='white')
sheet.save(p/'candidates/周瑜-七图重制总览.png')
# Native crops, no interpolation
boxes={'card01':[(340,160,630,430),(330,680,570,920),(730,870,930,1080)],'card02':[(300,130,600,430),(220,650,580,950)],'card03':[(360,170,620,430),(650,420,860,640),(140,820,310,1020)],'card04':[(330,210,620,490),(55,300,230,510),(740,650,930,830)],'story02':[(370,90,680,380),(400,430,660,650)],'story03':[(720,60,1050,350),(420,680,630,900),(1240,720,1480,930)],'story04':[(430,70,680,350),(850,440,1170,630)]}
for k,bs in boxes.items():
 im=Image.open(p/'raw'/f'{k}.png')
 for j,b in enumerate(bs):im.crop(b).save(p/'qa'/f'{k}-native100-{j}.png')
manifest={'hero':'周瑜','faction':'吴','created':'2026-10-19 01:47 UTC+08','tool':'built-in image_gen only','status':'7 candidate images awaiting user review','native_portraits':[1024,1536],'native_stories':[1536,1024],'composite_canvas':[1190,1786],'native_art_scaling':'none: pasted 1:1 at84,145','mythology':'离火朱雀为原创象征映射，非演义史实；火源仍为实际火船','assets':assets,'overview':str(p/'candidates/周瑜-七图重制总览.png'),'UI':'separate configurable compact layers anchors961/1045/1129. 吴固定橘红徽；1/1/2/3被动槽，1-4星。','skills_draft':{'英略':'主动伤害提高','远筹':'施法距离提高','整备':'主动冷却缩短'},'active_draft':'指定圆形区域一次有预警的范围火攻法术伤害，无永久火场；不采用旧草案炎余以免引入额外灼烧机制。','qa':'All 7 originals viewed. Silver and gold arm placement locally regenerated to avoid UI; previous sources preserved. All final UI cards viewed at overview; anatomy and hand crops saved. Some fine cloth texture remains, no gold particle atmosphere. Supporting Sun Quan identity is provisional original design.','failures':['card03-frame-hand-risk.png','card04-hand-low-before-local-fix.png']}
(p/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
(p/'sources.md').write_text('演义事件核对：第15回历阳相见与荐二张；第29回孙策死后周瑜奔丧，吴太夫人转告遗言，随后荐鲁肃；第44回主战受命、列将发令；第49回分六路、令黄盖备火船、与程普在大艨艟督战。\n'+ '\n'.join('https://zh.wikisource.org/zh/三國演義/第'+c+'回' for c in ['015','029','044','049'])+'\n原创项：服装、具体动作与镜头、佩剑外形、军令木牌、青骢马毛色、朱雀及其成长。无固定名马/名剑宣称。\n')
(p/'progress.md').write_text('七图生成、两次局部避让修正、四卡UI合成与核对完成。全部候选待用户审阅。Library上传记录另存library-result.json。没有执行Git。\n')
print(json.dumps([a['file'] for a in assets]+[manifest['overview']],ensure_ascii=False))
