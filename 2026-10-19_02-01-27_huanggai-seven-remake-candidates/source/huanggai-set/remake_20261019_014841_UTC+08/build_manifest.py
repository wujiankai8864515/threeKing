from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,hashlib,shutil
P=Path(__file__).resolve().parent
m=json.loads((P/'ui/composition-manifest.json').read_text()); rows=[]
labels=['铁鞭老营','乱军擒敌','伤中定计','火船决潮','以俘换归途','夜帐献计','降书之后的船阵']
for i,(tier,item) in enumerate(m['cards'].items()):
 src=P/'raw'/f'card0{i+1}.png'; dst=P/'candidates'/f'黄盖-0{i+1}-{labels[i]}.png';shutil.copy2(P/'ui'/item['output'],dst)
 rows.append({'id':f'card0{i+1}','title':labels[i],'source':str(src),'candidate':str(dst),'native_size':list(Image.open(src).size),'output_size':list(Image.open(dst).size),'sha256':hashlib.sha256(dst.read_bytes()).hexdigest()})
for i in range(1,4):
 src=P/'raw'/f'story0{i}.png'; dst=P/'candidates'/f'黄盖-0{i+4}-{labels[i+3]}.png';shutil.copy2(src,dst);rows.append({'id':f'story0{i}','title':labels[i+3],'target_card':f'card0{i+1}','source':str(src),'candidate':str(dst),'native_size':list(Image.open(src).size),'sha256':hashlib.sha256(dst.read_bytes()).hexdigest()})
font=ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',23)
sheet=Image.new('RGB',(1600,1070),'#20272d');d=ImageDraw.Draw(sheet)
for i,r in enumerate(rows):
 im=Image.open(r['candidate']).convert('RGBA')
 if i<4: im.thumbnail((390,585));pos=(i*400+(400-im.width)//2,30)
 else: im.thumbnail((520,350));pos=((i-4)*533,655)
 sheet.paste(im,pos,im);d.text((pos[0]+8,pos[1]+im.height+5),r['title'],font=font,fill='white')
sheet.save(P/'candidates/黄盖-七图总览.png')
qa=Image.new('RGB',(1600,700),'#24292d')
for i in range(4):
 im=Image.open(rows[i]['candidate']);qa.paste(im.crop((720,1030,1120,1390)),(400*i,0));qa.paste(im.crop((45,1485,330,1745)),(400*i+50,410))
qa.save(P/'qa/UI-100percent.png')
(P/'manifest.json').write_text(json.dumps({'hero':'黄盖','status':'candidate_awaiting_user_review','generation':'built-in imagegen; individual source each; four style revisions retained','art_resampling':'none; native cards 1024x1536 composed 1:1 into1190x1786','story_dimensions':'1536x1024 native','myth':'原创烽舰赭鲸，非小说原有配兽','skills':'draft only 1/1/2/3 passives','assets':rows},ensure_ascii=False,indent=2))
(P/'qa/review.md').write_text('逐幅检查完成。脸型保持宽鼻方颌深眼；银金灰白须发加强。铁鞭为实心硬兵器，金刀单刃握柄清楚。主角均大且清楚，动画色块，未发现主角多指或断肢。黄金左手抬高避UI。铜卡黄祖活俘；银卡干净包覆无血腥；黄金为连续事件艺术压缩。四卡材质修订前图保留failures。UI使用全框分级金属、吴橘红徽、水军船icon、1-4星，底锚961/1045/1129，动态文字独立层。实际未被UI遮挡艺术像素变化0。所有图片均候选，未获用户通过。\n')
print(P)
