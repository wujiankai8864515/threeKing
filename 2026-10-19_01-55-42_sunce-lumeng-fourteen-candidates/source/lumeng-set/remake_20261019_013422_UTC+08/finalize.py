from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import json,hashlib,shutil
P=Path(__file__).resolve().parent
names=['01-黑铁-江夏自棹','02-青铜-皖城催鼓','03-白银-藏锋称病','04-黄金-白衣断烽','05-传记-等不起土山','06-传记-病帐听良策','07-传记-烽台未燃']
src=[P/'ui'/f'{i:02d}-{t}-UI排版修复1190.png' for i,t in enumerate(['黑铁','青铜','白银','黄金'],1)]+[P/'raw'/f'story{i:02d}.png' for i in range(1,4)]
font=ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',24)
sheet=Image.new('RGB',(1800,1530),'#20262c');d=ImageDraw.Draw(sheet);d.text((30,10),'吕蒙 · 四阶三传记 · 重做候选（原创白鼍象征／技能草案）',font=font,fill='white')
manifest={'hero':'吕蒙','faction':'吴','status':'候选，等待用户审阅；非通过','engine':'built-in image_gen','raw_native_card_size':[1024,1536],'raw_native_story_size':[1536,1024],'ui_card_canvas':[1190,1786],'art_resampling':'none, raw at 1:1 offset (84,145)','sources':['https://zh.wikisource.org/zh/三國演義/第038回','https://zh.wikisource.org/zh/三國演義/第067回','https://zh.wikisource.org/zh/三國演義/第075回'],'assets':[]}
for i,(name,s) in enumerate(zip(names,src)):
 dest=P/'candidates'/(name+'.png');shutil.copy2(s,dest);im=Image.open(dest).convert('RGBA')
 if i<4:
  im.thumbnail((440,660));x=10+i*448;y=55
 else:
  im.thumbnail((585,390));x=10+(i-4)*595;y=780
 sheet.paste(im,(x,y),im);d.text((x+5,y+im.height+10),name,font=font,fill='white')
 raw=P/'raw'/(f'card{i+1:02d}.png' if i<4 else f'story{i-3:02d}.png')
 manifest['assets'].append({'id':name,'raw':str(raw),'candidate':str(dest),'native_size':list(Image.open(raw).size),'candidate_size':list(Image.open(dest).size),'sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'story_target':None if i<4 else f'card{i-2:02d}'})
 for label,box in [('upper',(0,0,min(1024,Image.open(raw).width),700)),('lower',(0,600,min(1024,Image.open(raw).width),min(1400,Image.open(raw).height)))]:Image.open(raw).crop(box).save(P/'qa'/f'{i+1:02d}-{label}.png')
d.text((30,1240),'黑铁：亲棹进击 → 青铜：乘锐擂鼓 → 白银：虚心纳计 → 黄金：白衣断烽',font=font,fill='#e2b792')
d.text((30,1290),'第38、67、75回事件；白鼍、面貌、甲胄、镜头均属原创美术设计。无原著名马或神兵冒称。',font=font,fill='white')
d.text((30,1340),'敛息：整备时间缩短；伏甲：整备期间减伤；缴刃：缴械时间延长。每项只有一个主效果。',font=font,fill='white')
d.text((30,1390),'主动草案：短时整备后近身刀击并缴械，移动或强制位移中止整备。无额外连锁组合。',font=font,fill='white')
sheet.save(P/'吕蒙-四阶三传记-重做总览.png');(P/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
(P/'research'/'核验与制作说明.md').write_text('## 原文核验\n第38回：吕蒙自举橹棹入船队，继而持刀追斩陈就；不混用甘宁斩邓龙。\n第67回：吕蒙反对耗时土山、虹桥，主张乘初到锐气速攻，后亲自擂鼓。\n第75回：吕蒙托病，陆逊指出烽火戒备，建议托疾辞职以骄关羽；白衣扮商人、伏精兵，控制烽台后进军。\n三传记依次引出铜卡擂鼓、银卡称病、金卡断烽。读书卷是学习成长的原创视觉线索，不把孙权劝学硬塞入第75回。\n潜渊白鼍是原创象征非原著神兽、坐骑。黑铁潜背、青铜半首、白银静伏、黄金冠脊巨首伏水。\n四卡均吴橘红收藏徽；兵种图标沿用通用步兵。技能三项画面解锁数量1/1/2/3，两字名称、单效果；归鞘保留研究备选但本套未装入UI。\n所有图均独立内置image_gen，未经放大宣称4K。首轮写实漂移、两张靠边手姿留存failures。图像修复提示均存prompts。\n')
(P/'qa'/'QA.md').write_text('已逐幅查看七张原图。动画式哑光色面、身份一致、无金粉密点、主角突出。黑铁双手共轴直棹；铜双槌抓握和鼓面关系可读；银持书听计；金止令和扶舱手在图内。金黑两张因边框遮手风险重做局部手姿，保留前版。四卡原图不缩放，合成检查未被UI覆盖处原生像素差0；统一槽位961/1045/1129，技能板底锚1172。UI曾误用模板许褚文字已修正，最终必须检查吕蒙/吴/敛息伏甲缴刃。传记02陆逊为原创配角形象，后续可与陆逊正式资产统一。\n')
(P/'progress.json').write_text(json.dumps({'stage':'ready_for_library','seven_images':7,'candidate_only':True},ensure_ascii=False))
