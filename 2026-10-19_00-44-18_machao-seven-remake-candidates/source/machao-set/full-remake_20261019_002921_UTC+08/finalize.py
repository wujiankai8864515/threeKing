from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,hashlib,shutil
D=Path(__file__).resolve().parent
F=D/'candidates';F.mkdir(exist_ok=True)
labels=['01-黑铁-西凉少锋','02-青铜-潼关怒骑','03-白银-葭萌夜烈','04-黄金-归蜀定锋','05-传记-西凉起兵','06-传记-挑灯争锋','07-传记-雾开有归']
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
dr.text((25,760),'马超 · 西凉披发骑将 / 天狼为原创提案 / 技能与阶名待审',font=font,fill='#dec793')
sheet.save(F/'08-马超-四卡三传记总览.png')
manifest={'hero':'马超','status':'ready_candidate_pending_user_review','generator':'built-in image_gen only','raw_generated_count':7,'art_status':'all seven newly generated, four cards locally polished; old iterations preserved','mythic_beast':'西凉天狼，原创提案，非演义或史传设定','research':str(D/'research.md'),'qa':str(D/'qa/QA.md'),'assets':assets,'overview':str(F/'08-马超-四卡三传记总览.png'),'prompts':[str(p) for p in (D/'prompts').glob('*.txt')],'ui_compositor':str(D/'ui/compose_layout.py'),'ui_manifest':str(D/'ui/composition-manifest.json'),'no_upscale_claim':'native portrait 1024x1536, landscape1536x1024; card UI1190x1786 is composition canvas, not native 4K','limitations':['四卡视线多数朝右，但姿势/摄像/时间不同；不得扩散为其他武将固定模板','青铜蹄部保留逆光土尘，非金粉；脸/双握点更清楚','技能、阶名、天狼象征均为待审提案']}
(D/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
(D/'status.json').write_text(json.dumps({'status':'ready','approval':'candidate_pending','assets_ready':7,'overview_ready':True},ensure_ascii=False,indent=2))
with (D/'qa/QA.md').open('a') as f:f.write('\n根审提示已记录：四卡大多朝右，不得将此模板扩散至其他英雄。三传记分别帐内站立报难、营外换马夜战、帐内坐谈归属，镜头及叙事有区别。最后传记误生实体狼，已修复移除并保留失败图。所有最终源图均已逐张查看。\n')
print(json.dumps([a['candidate'] for a in assets]+[str(F/'08-马超-四卡三传记总览.png')],ensure_ascii=False))
