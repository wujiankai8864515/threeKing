from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
import json,hashlib,shutil
P=Path(__file__).resolve().parent
font=ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',24)
# Preserve native hand pixels above the right rail without regenerating art.
src=Image.open(P/'raw/card01.png').convert('RGBA');mask=Image.new('L',src.size);d=ImageDraw.Draw(mask);d.polygon([(905,418),(931,420),(954,435),(956,494),(940,508),(906,501),(889,478),(892,442)],fill=255)
layer=Image.new('RGBA',(1190,1786));tmp=src.copy();tmp.putalpha(mask);layer.alpha_composite(tmp,(84,145));layer.save(P/'ui/iron-hand-foreground-preservation.png');mask.save(P/'ui/iron-hand-preservation-mask.png')
f=P/'ui/01-黑铁-UI排版修复1190.png';im=Image.open(f).convert('RGBA');im.alpha_composite(layer);im.save(f)
labels=['黑铁·父阵初锋','青铜·借兵渡江','白银·神亭争锋','黄金·孙郎开疆'];files=[]
for i,(tier,label) in enumerate(zip(['黑铁','青铜','白银','黄金'],labels),1):
 src=P/'ui'/f'{i:02}-{tier}-UI排版修复1190.png';dest=P/f'孙策-{i:02}-{label}.png';shutil.copy2(src,dest);files.append(dest)
for i,title in enumerate(['质玺换前路','十三骑上神亭','日中归约'],1):
 dest=P/f'孙策-传记{i:02}-{title}.png';shutil.copy2(P/f'raw/bio{i:02}.png',dest);files.append(dest)
sheet=Image.new('RGB',(1600,1290),'#1c2327');d=ImageDraw.Draw(sheet)
for i,f in enumerate(files[:4]):
 im=Image.open(f).convert('RGBA');im.thumbnail((390,585));sheet.paste(im,(i*400+5,35),im);d.text((i*400+18,625),labels[i],font=font,fill='white')
for i,f in enumerate(files[4:]):
 im=Image.open(f).convert('RGB');im.thumbnail((520,347));sheet.paste(im,(i*533,690));d.text((i*533+12,1055),['传记→青铜：质玺换前路','传记→白银：十三骑上神亭','传记→黄金：日中归约'][i],font=font,fill='white')
d.text((25,1120),'孙策七图候选｜四卡三关联传记｜全部待用户审阅',font=font,fill='#f1cc91');d.text((25,1160),'原生卡画1024×1536，传记1536×1024；卡框1190×1786，无4K声明',font=font,fill='white');d.text((25,1200),'腾潮狻猊、盔甲和技能为原创提案；成年面貌属于明确年龄调整',font=font,fill='white')
sheet.save(P/'孙策-七图总览.png');files.append(P/'孙策-七图总览.png')
qa=Image.new('RGB',(1600,640),'#20252a')
for i in range(4):
 im=Image.open(P/f'raw/card{i+1:02}.png');box=[(340,170,740,810),(90,160,490,800),(40,230,440,870),(100,160,500,800)][i];qa.paste(im.crop(box),(i*400,0))
qa.save(P/'qa/四卡脸手与武器原像素.png')
manifest={'hero':'孙策','status':'candidate_awaiting_user_review','tool':'built-in image_gen','source_urls':['https://zh.wikisource.org/zh/三國演義/第007回','https://zh.wikisource.org/zh/三國演義/第015回'],'story_links':{'bio01':'card02','bio02':'card03','bio03':'card04'},'native_sizes':{'cards':[1024,1536],'stories':[1536,1024],'ui':[1190,1786]},'ui':{'faction':'吴','badge':'fixed orange-red','slots':[961,1045,1129],'counts':[1,1,2,3],'troop_icon':'cavalry horse silhouette','passives':{'锐意':'首次伤害新目标提高','敏枪':'换目标后短时攻速提高','开疆':'对新目标主动能量消耗降低'},'active_draft':'对近身单敌直刺一次；本场首次伤害该目标时提高威力。'},'adaptations':['22岁以上统一成年面貌，非原文当时年龄','腾潮狻猊为原创神兽，不是演义典故','黄骠战马和宽叶枪为原创造型，无原著专名','金卡最终竖枪迎归以保证刚体连续'],'assets':[]}
for f in files:manifest['assets'].append({'path':str(f),'size':list(Image.open(f).size),'sha256':hashlib.sha256(f.read_bytes()).hexdigest()})
(P/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2));(P/'deliverable-paths.json').write_text(json.dumps([str(f) for f in files],ensure_ascii=False))
(P/'research-and-QA.md').write_text('孙策全套候选，未获用户通过。\n第7回：孙策随父，按枪射陈生，未将张虎误作射杀对象。\n第15回：玉玺质借三千兵五百马在渡江前；神亭先十三骑探岭，后枪战太史慈；释放赠袍后约次日日中，立竿候影，太史慈纳众归约，再安民。\n原文核查：维基文库第007回132段、第015回128—143及160—163段。\n艺术改编：成年统一脸；波潮狻猊；甲、马、枪形制。\nQA：七图已逐张目检，脸身份连续；未把神亭画为归降；日中归约双方平立。首图弓弦两次修，去掉肩后伪线并连上下梢；银枪三次修至水平双手同轴；金枪两次修至竖枪完整长杆。失败版本保留。\nUI采用既有金属框独立层，固定橘红吴徽；星1—4、骑兵马首icon、被动两字单效果，1/1/2/3条向上扩展。手部像素遮罩恢复在框上独立层。\n所有图为候选，母版不是4K；水花高光属于水而不是金粉，仍可按用户偏好局部减弱。\n')
print(json.dumps([str(f) for f in files],ensure_ascii=False))
