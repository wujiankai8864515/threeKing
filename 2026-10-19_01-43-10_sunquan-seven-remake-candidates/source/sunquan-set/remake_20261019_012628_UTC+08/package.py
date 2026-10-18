from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,hashlib,shutil
d=Path(__file__).parent
out=d/'deliverables';out.mkdir(exist_ok=True)
labels=['01-黑铁-印绶初承','02-青铜-江夏纳策','03-白银-一剑定战','04-黄金-濡须持衡','05-传记-不记旧怨','06-传记-把剑交给周郎','07-传记-春水与书信']
sources=[d/'ui'/f'{x}-UI排版修复1190.png' for x in ['01-黑铁','02-青铜','03-白银','04-黄金']]+[d/'raw'/f'bio0{i}.png' for i in range(1,4)]
manifest={'hero':'孙权','status':'新候选待用户审核','generator':'built-in imagegen','native_cards':[1024,1536],'native_stories':[1536,1024],'ui_canvas':[1190,1786],'art_resampling':'none; 1:1','myth':'负日赑屃是原创神话组合，不是演义配兽','skills_status':'全部拟案','active':'消耗自身一份能量，将一名友军可转换的短期攻击增益转为等价值护盾','passives':{'筹度':'主动能量消耗降低','审势':'主动选择友军距离提高','固业':'本主动护盾容量提高'},'files':[],'repairs':['青铜手从右下栏杆移至中央腰带避开UI','授剑传记去除左端多余剑柄，保留单柄带鞘剑'],'sources':[f'https://zh.wikisource.org/zh/三國演義/第{x}回' for x in ['029','038','044','061']]}
for label,src in zip(labels,sources):
 p=out/(label+'.png');shutil.copy2(src,p)
 manifest['files'].append({'file':str(p),'source':str(src),'dimensions':Image.open(p).size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
font=ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',24)
sheet=Image.new('RGB',(1680,1300),'#20262d');draw=ImageDraw.Draw(sheet)
for i in range(4):
 im=Image.open(sources[i]).convert('RGBA');im.thumbnail((410,650));sheet.paste(im,(i*420+(420-im.width)//2,15),im)
 draw.text((i*420+35,660),labels[i],font=font,fill='white')
for i in range(3):
 im=Image.open(sources[4+i]).convert('RGB');im.thumbnail((550,400));sheet.paste(im,(i*560,720))
 draw.text((i*560+20,1110),labels[4+i],font=font,fill='white')
draw.text((30,1190),'孙权｜四卡三传记 · 全新候选，待审核',font=font,fill='#e9c998')
draw.text((30,1230),'29回承印 → 38回纳策 → 44回定战授剑 → 61回濡须交书',font=font,fill='white')
sheet.save(out/'08-孙权-七图总览.jpg',quality=94)
qa=Image.new('RGB',(1600,800),'#20262d')
for i in range(4):
 im=Image.open(d/'raw'/f'card0{i+1}.png')
 im.crop((250,100,650,500)).save(d/'qa'/f'card0{i+1}-face.png')
 qa.paste(im.crop((250,100,650,500)),(i*400,0))
 im=Image.open(sources[i]);crop=im.crop((760,1030,1160,1430));qa.paste(crop,(i*400,400))
qa.save(d/'qa'/'face-ui-native-crops.jpg',quality=94)
(d/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
(d/'QA.md').write_text('七张独立图均目检。脸与手可读；碧眼、自然肤色同一身份；吴徽橘红固定；UI 961/1045/1129 共用槽位，1/1/2/3 个两字单效果被动，船形兵种图标。原生插画未放大。初稿及两次修复前图保存 failures。神兽与冠服为原创设计。所有技能、等级、圆章均为界面拟案。全套待用户审核。')
print(str(out))
