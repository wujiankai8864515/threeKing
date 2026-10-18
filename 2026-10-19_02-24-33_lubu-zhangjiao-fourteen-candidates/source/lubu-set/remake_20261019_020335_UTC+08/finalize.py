from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,hashlib,shutil
D=Path(__file__).resolve().parent
F=D/'candidates';F.mkdir(exist_ok=True)
labels=['01-黑铁-并州戟锋','02-青铜-虎牢独挡','03-白银-诏出戟定','04-黄金-辕门一箭','05-传记-关前三路合围','06-传记-司徒密议','07-传记-两军共看一枝']
paths=[D/'ui'/x for x in ['01-黑铁-UI排版修复1190.png','02-青铜-UI排版修复1190.png','03-白银-UI排版修复1190.png','04-黄金-UI排版修复1190.png']]+[D/'raw'/f'bio0{i}.png' for i in [1,2,3]]
assets=[]
for i,(p,l) in enumerate(zip(paths,labels)):
 dest=F/(l+'.png');shutil.copy2(p,dest)
 raw=D/'raw'/(f'card0{i+1}.png' if i<4 else f'bio0{i-3}.png')
 assets.append({'id':raw.stem,'label':l,'source':str(raw),'native_dimensions':list(Image.open(raw).size),'source_sha256':hashlib.sha256(raw.read_bytes()).hexdigest(),'candidate':str(dest),'candidate_dimensions':list(Image.open(dest).size),'candidate_sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'destination_card':None if i<4 else f'card0{i-2}','status':'candidate_pending_user_review'})
font=ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',24)
sheet=Image.new('RGB',(1920,1275),'#20252a');dr=ImageDraw.Draw(sheet)
for i,a in enumerate(assets):
 im=Image.open(a['candidate']).convert('RGBA')
 if i<4: im.thumbnail((465,710));x=i*480+(480-im.width)//2;y=20
 else: im.thumbnail((625,417));x=(i-4)*640+(640-im.width)//2;y=800
 sheet.paste(im,(x,y),im);dr.text((x,y+im.height+8),a['label'],font=font,fill='white')
dr.text((25,760),'吕布 · 方天画戟与赤兔 / 兵主戟魂为原创提案 / 技能与阶名待审',font=font,fill='#dec793')
sheet.save(F/'08-吕布-四卡三传记总览.png')
manifest={'hero':'吕布','status':'ready_candidate_pending_user_review','generator':'built-in image_gen only','raw_generated_count':7,'art_status':'all seven newly generated, four cards locally polished; old iterations preserved','mythic_beast':'兵主戟魂，原创武器神相，非演义或史传设定','research':str(D/'research/verified.md'),'qa':str(D/'qa/QA.md'),'assets':assets,'overview':str(F/'08-吕布-四卡三传记总览.png'),'prompts':[str(p) for p in (D/'prompts').glob('*.txt')],'ui_compositor':str(D/'ui/compose_layout.py'),'ui_manifest':str(D/'ui/composition-manifest.json'),'no_upscale_claim':'native portrait 1024x1536, landscape1536x1024; card UI1190x1786 is composition canvas, not native 4K','limitations':['四卡阶段、被动名称和等级均待审游戏设定','兵主戟魂、双月牙定型和低阶简化双翎为原创视觉解释','各事件按演义，不宣称历史准确复原']}
(D/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
(D/'status.json').write_text(json.dumps({'status':'ready','approval':'candidate_pending','assets_ready':7,'overview_ready':True},ensure_ascii=False,indent=2))
print(json.dumps([a['candidate'] for a in assets]+[str(F/'08-吕布-四卡三传记总览.png')],ensure_ascii=False))
