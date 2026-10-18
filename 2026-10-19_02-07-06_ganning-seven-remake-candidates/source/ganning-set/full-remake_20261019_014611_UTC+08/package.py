from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,hashlib,shutil
P=Path(__file__).resolve().parent
labels=['锦帆旧客','江夏追影','铁练攀城','百翎入夜']; tiers=['黑铁','青铜','白银','黄金']; manifest={'hero':'甘宁','faction':'吴','status':'new candidates awaiting user review','art_native_cards':[1024,1536],'art_native_stories':[1536,1024],'ui_canvas':[1190,1786],'no_4k_claim':True,'ui':{'anchors':[961,1045,1129],'troop_icon':'水军','passive_counts':[1,1,2,3],'values':'草案','illustration':'native 1:1 at 84,145; no resizing for frame'},'assets':[]}
for i,(l,t) in enumerate(zip(labels,tiers),1):
 src=P/'ui'/f'{i:02d}-{t}-UI排版修复1190.png';dst=P/'candidates'/f'甘宁-0{i}-{t}-{l}.png';shutil.copy2(src,dst)
 manifest['assets'].append({'id':f'card{i:02d}','file':str(dst),'raw':str(P/'raw'/f'card{i:02d}.png'),'sha256':hashlib.sha256(dst.read_bytes()).hexdigest(),'size':list(Image.open(dst).size)})
for i,l in zip(range(2,5),['立功不忘旧恩','鼓下争先','一百根白翎']):
 src=P/'raw'/f'story{i:02d}.png';dst=P/'candidates'/f'甘宁-传记{i-1:02d}-{l}.png';shutil.copy2(src,dst)
 manifest['assets'].append({'id':f'story{i:02d}','target_card':f'card{i:02d}','file':str(dst),'raw':str(src),'sha256':hashlib.sha256(dst.read_bytes()).hexdigest(),'size':list(Image.open(dst).size)})
f=ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',25)
sheet=Image.new('RGB',(1600,1090),'#18232f');d=ImageDraw.Draw(sheet)
for i,a in enumerate(manifest['assets'][:4]):
 im=Image.open(a['file']).convert('RGBA');im.thumbnail((390,585));sheet.paste(im,(i*400+5,35),im);d.text((i*400+20,620),tiers[i]+' · '+labels[i],font=f,fill='white')
for j,a in enumerate(manifest['assets'][4:]):
 im=Image.open(a['file']).convert('RGB');im.thumbnail((516,344));sheet.paste(im,(j*533+8,672));d.text((j*533+15,1020),['立功不忘旧恩 → 青铜','鼓下争先 → 白银','一百根白翎 → 黄金'][j],font=f,fill='white')
d.text((20,1060),'甘宁七图候选｜墨鳍浪鲨为原创神话演绎｜技能、阶级为拟案',font=f,fill='#e9c89c')
sheet.save(P/'candidates/甘宁-完整七图总览.png')
qa=Image.new('RGB',(1400,1000),'#202832')
for i in range(1,5):
 im=Image.open(P/'raw'/f'card{i:02d}.png');im.crop((270,140,970,640)).resize((350,250)).save(P/'qa'/f'card{i:02d}-face-context.png')
 qa.paste(im.crop((270,140,970,640)).resize((350,250)),((i-1)*350,0))
 ui=Image.open(manifest['assets'][i-1]['file']);qa.paste(ui.crop((750,1030,1100,1410)).resize((350,380)),((i-1)*350,270))
qa.save(P/'qa/face-and-ui.png')
(P/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
(P/'qa/review.md').write_text('逐张看图：原画四卡和三传记均已检查；四卡另检UI。首轮四张微纹过密已进入failures，最终四卡完成清晰动画风格修正。铜卡弓弦连通，箭离弦不粘弦；银卡链条弯垂，不假作刚杆。金卡刀刃连续、骑姿与缰绳合理。脸与人手未被UI遮挡；马额局部由右侧技能板覆盖但主眼鼻仍可辨。水军图标统一；四阶1–4星。全部候选未用户通过。\n')
print(json.dumps({'files':[a['file'] for a in manifest['assets']]+[str(P/'candidates/甘宁-完整七图总览.png')]},ensure_ascii=False))
