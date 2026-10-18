from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
import json,hashlib
D=Path(__file__).parent;C=D/'candidates';U=D/'ui';Q=D/'qa'
font=ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',26)
can=Image.new('RGB',(1800,1500),'#20242b');dr=ImageDraw.Draw(can)
for i,label in enumerate(['黑铁·长沙老将','青铜·报义神射','白银·老骥出关','黄金·定军神射']):
 p=list(U.glob(f'0{i+1}-*.png'))[0];im=Image.open(p).convert('RGBA');im.thumbnail((440,690));can.paste(im,(i*450+(450-im.width)//2,45),im);dr.text((i*450+25,750),label,font=font,fill='white')
for i,(id,label) in enumerate([('bio01','第53回·射缨报义'),('bio02','第70回·天荡山'),('bio03','第71回·定军乘势')]):
 im=Image.open(C/(id+'.png'));im.thumbnail((580,400));can.paste(im,(i*600+10,830));dr.text((i*600+25,1240),label,font=font,fill='white')
dr.text((35,1320),'黄忠全套重制候选｜四阶卡面 + 三段独立传记｜技能与神鹰意象为拟案',font=font,fill='#ddd3bd')
dr.text((35,1370),'原画 1024×1536 / 1536×1024；卡面合成 1190×1786；待用户审核',font=font,fill='#ddd3bd');can.save(D/'黄忠-七图总览.png')
qa=Image.new('RGB',(1400,1100),'#20242b')
for i,id in enumerate(['card01','card02','card03','card04']):
 im=Image.open(C/(id+'.png'));box=[(200,370,700,850),(160,450,700,780),(200,480,780,760),(210,450,750,730)][i];crop=im.crop(box);qa.paste(crop,((i%2)*700,(i//2)*550))
qa.save(Q/'final-face-hand-arrow-native-crops.png')
manifest={'status':'candidate_awaiting_user_review','tool':'built-in image_gen','files':[],'source_map':'source-map.json','chronology':[53,70,71],'notes':'UI troop icon bow; skill/rank labels proposed; no 4K claim. Four card sources reframed by built-in imagegen to clear right star rail.'}
for p in list(C.glob('*.png'))+list(U.glob('0*-*.png'))+[D/'黄忠-七图总览.png']:
 manifest['files'].append({'path':str(p),'dimensions':list(Image.open(p).size),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
(D/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
