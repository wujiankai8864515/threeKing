from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,shutil,hashlib
D=Path(__file__).resolve().parent;(D/'candidates').mkdir(exist_ok=True)
names=['01-黑铁-河北枪锋','02-青铜-转旗受命','03-白银-瓦口寻径','04-黄金-街亭截援','05-传记-谗言断归路','06-传记-从败阵走出','07-传记-截住援路']
files=[]
for i,n in enumerate(names):
 src=sorted(D.glob('ui/*修复1190.png'))[i] if i<4 else D/f'raw/story{i-3:02d}.png'
 dst=D/'candidates'/f'张郃-{n}.png';shutil.copy2(src,dst);files.append(dst)
font=ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',25)
sheet=Image.new('RGB',(1800,1380),'#19212b');dr=ImageDraw.Draw(sheet)
for i,f in enumerate(files):
 im=Image.open(f).convert('RGBA');im.thumbnail((440,670) if i<4 else (585,400))
 x=i*450+(450-im.width)//2 if i<4 else (i-4)*600+(600-im.width)//2;y=25 if i<4 else 775
 sheet.paste(im,(x,y),im);dr.text((x,y+im.height+6),names[i],font=font,fill='white')
dr.text((25,1220),'张郃 · 全新四卡三传记候选｜折翼鹤阵为原创艺术演绎｜技能为草案',font=font,fill='#dfd3b3')
dr.text((25,1265),'第30回：袁营、归曹 → 第70回：瓦口败退 → 第95回：街亭截援',font=font,fill='white')
dr.text((25,1310),'插画原生：卡面1024×1536，传记1536×1024；UI1190×1786，无插画放大',font=font,fill='white')
sheet.save(D/'张郃-全套七图总览.png')
cropmap={}
for i in range(1,5):
 im=Image.open(D/f'raw/card{i:02d}.png')
 boxes={'face':(260,120,690,590),'grips':(0,620,850,1280),'beast':(0,0,1024,380)}
 for k,b in boxes.items():im.crop(b).save(D/f'qa/card{i:02d}-{k}.png')
 cropmap[f'card{i:02d}']=boxes
for i in range(1,4):
 im=Image.open(D/f'raw/story{i:02d}.png');im.resize((768,512)).save(D/f'qa/story{i:02d}-preview.png')
(D/'qa/crop-map.json').write_text(json.dumps(cropmap,indent=2))
gen=['exec-117e0d31-c88c-46ed-806f-fa4388d62326.png','exec-d4375d9c-bb65-4731-9d01-4c7d911a5e71.png','exec-c4ff2a52-c41b-4402-ae63-81d5739a5194.png','exec-16972f1b-7130-43b7-b193-7f44f7df1c96.png','exec-f0942e7f-86c0-44f7-85f8-8f53171dc948.png','exec-70f6d220-24c0-48f1-bf9e-431316f15369.png','exec-f221e7e2-eeca-4893-9beb-d090dae21685.png']
manifest={'hero':'张郃','status':'candidate_awaiting_user','tool':'built-in image_gen','faction':'收藏统一蓝底魏；事件旗袁→曹→魏','skills_draft':{'主动 巧变':'选一近旁友军移至身旁安全空位，然后向其原方向作一次防护枪击','轻履':'移动速度提高','应变':'主动冷却缩短','援途':'主动选择友军距离提高'},'failure':'银卡首版含错误水域战船，定向重绘远景为山地木寨，原图保留','files':[],'source_map':[]}
for i,f in enumerate(files):
 src=D/f'raw/card{i+1:02d}.png' if i<4 else D/f'raw/story{i-3:02d}.png'
 manifest['source_map'].append({'asset':names[i],'raw':str(src),'generated_original':'generated_images/'+gen[i],'native_size':list(Image.open(src).size),'output':str(f)})
for f in files+[D/'张郃-全套七图总览.png']:
 manifest['files'].append({'path':str(f),'size':list(Image.open(f).size),'sha256':hashlib.sha256(f.read_bytes()).hexdigest()})
(D/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
(D/'QA.md').write_text('七图逐张查看，卡面1024×1536、传记1536×1024均独立生成。原图和失败保留。\n清瘦长脸、细眼、薄髭窄颏须、烟紫灰衣保持身份；第一阶整体灰沉、后续升至紫白明亮；折羽→半翼→完整鹤→巨鹤成长。\n长枪轴贯通和握点清楚；徒步脱险不画成凯旋。银卡错误水域战船已定向修复为木寨山地。\nUI二字被动单效果草案，底部向上增长1/1/2/3，等级排版示例，四阶蓝底魏徽。原生图不放大，1190×1786只是UI画布。\n三传记中助卒镜头为原创合理演绎，鹤阵为原创神话象征，不宣称演义记载。当前全为待审候选。\n')
uploads={'uploads':[{'local_path':str(f.resolve()),'purpose':'create_library_file','library_artifact_type':'image_gen' if i<7 else 'image'} for i,f in enumerate(files+[D/'张郃-全套七图总览.png'])]}
(D/'library-request.json').write_text(json.dumps(uploads,ensure_ascii=False,indent=2))
