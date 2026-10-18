from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,hashlib,shutil
P=Path(__file__).resolve().parent
names=['01-黑铁-武阁自持','02-青铜-一笑撤锋','03-白银-出吴自主','04-黄金-卷帘护路','05-传记-兵器可收主意未改','06-传记-这一程我同行','07-传记-车前自解危局']
font=ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',23)
sheet=Image.new('RGB',(1800,1400),'#20262c');d=ImageDraw.Draw(sheet);d.text((25,12),'孙尚香 · 四阶三传记 · 重做候选（原创月刃灵猞／技能草案）',font=font,fill='white')
src=[P/'ui'/f'{i:02d}-{t}-UI排版修复1190.png' for i,t in enumerate(['黑铁','青铜','白银','黄金'],1)]+[P/'raw'/f'story{i:02d}.png' for i in range(1,4)]
m={'hero':'孙尚香','faction':'吴','status':'候选待审，非用户通过','engine':'built-in image_gen','source':'https://zh.wikisource.org/zh/三國演義/第055回','art_resampling':'none; cards 1024x1536 at1:1 offset84,145 on1190x1786','assets':[]}
for i,(name,s) in enumerate(zip(names,src)):
 dest=P/'candidates'/(name+'.png');shutil.copy2(s,dest);im=Image.open(dest).convert('RGBA');im.thumbnail((440,660) if i<4 else (585,390));x=10+i*448 if i<4 else 10+(i-4)*595;y=55 if i<4 else 770;sheet.paste(im,(x,y),im);d.text((x+5,y+im.height+8),name,font=font,fill='white')
 raw=P/'raw'/(f'card{i+1:02d}.png' if i<4 else f'story{i-3:02d}.png')
 m['assets'].append({'id':name,'raw':str(raw),'candidate':str(dest),'native_size':list(Image.open(raw).size),'candidate_size':list(Image.open(dest).size),'sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'target_card':None if i<4 else f'card{i-2:02d}'})
 Image.open(raw).crop((0,0,1024,700)).save(P/'qa'/f'{i+1:02d}-upper-100pct.png');Image.open(raw).crop((0,600,1024,min(1300,Image.open(raw).height))).save(P/'qa'/f'{i+1:02d}-hands-100pct.png')
for j,t in enumerate(['严毅武阁 → 自主撤锋 → 决意随行 → 卷帘护路。三传记分别关联铜、银、金。','第55回有据事件；短弓、耳簇簪、护甲、月刃灵猞为原创，不是原著神兵坐骑。','轻装：移动速度提高；稳弦：补射伤害提高；应援：伙伴选择距离提高。','主动草案：选友军，其下一次普攻命中时补射一箭，仅一次。无多层连锁。']):d.text((25,1210+j*40),t,font=font,fill='white')
sheet.save(P/'孙尚香-四阶三传记-重做总览.png');(P/'manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2))
(P/'research'/'核验说明.md').write_text('第55回原文核验：115行武阁兵器、侍婢佩剑及笑令撤去；122至123行决意随行、祭祖借口、乘车出城；127行卷帘斥徐盛丁奉放行；128行与赵云当后，再斥陈武潘璋，四将拱手退去。三传记依次解释青铜撤锋、白银出吴、黄金护行。未画她开弓射杀吴将。所用通用游戏名孙尚香不冒称原著实名。四阶全为成年人，耳簇是金属簪不是猫耳人体。短弓与短剑为无专名原创游戏装备。月刃灵猞为原创神话象征，非原著神兽坐骑。\n来源：https://zh.wikisource.org/zh/三國演義/第055回\n')
(P/'qa'/'QA.md').write_text('逐幅查看7张原图和4卡UI。首轮写实漂移已2D风格修复；撤剑传记男性管家婆改为年长女性；黄金抬帘手内移、猞首下移避开星栏。首版与修复失败风险图保存在failures。无手握弓剑战斗，此选段武器收鞘或背负，未虚构杀敌。四卡1024×1536，三传记1536×1024；不声称4K。UI独立可配置，卡画1:1，未覆盖处像素差0；技能锚点961/1045/1129，底1172；弓兵独立矢量icon；吴橘红徽固定。\n')
(P/'progress.json').write_text(json.dumps({'stage':'ready_for_library','raw_assets':7,'candidate_only':True}))
