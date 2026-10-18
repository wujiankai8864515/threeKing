from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,hashlib,shutil
P=Path(__file__).resolve().parent
names=['01-黑铁-北海赴义','02-青铜-神亭相持','03-白银-日中践诺','04-黄金-合肥争锋','05-传记-神亭两锋','06-传记-赴约而归','07-传记-阵前迎刀']
raws=[P/'raw'/f'card{i:02d}.png' for i in range(1,5)]+[P/'raw'/f'bio{i:02d}.png' for i in range(1,4)]
src=[P/'ui'/f'{i:02d}-{t}-UI排版修复1190.png' for i,t in enumerate(['黑铁','青铜','白银','黄金'],1)]+raws[4:]
f=ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',24)
sheet=Image.new('RGB',(1800,1450),'#20262c');d=ImageDraw.Draw(sheet);d.text((30,10),'太史慈 · 四阶三传记 · 重做候选／原创赤背神猿／技能草案',font=f,fill='white')
m={'hero':'太史慈','faction':'吴','status':'候选待审，非用户通过','engine':'built-in image_gen','card_native':[1024,1536],'story_native':[1536,1024],'ui_canvas':[1190,1786],'art_resampling':'none; native 1:1 at (84,145)','myth':'赤背神猿为原创美术解释，非原著神兽','weapons':'铁枪、弓矢、背上短戟有原文依据；造型原创，无神兵专名','mount':'赭栗马为原创造型，无原著专名','sources':['https://zh.wikisource.org/zh-hant/三國演義/第011回','https://zh.wikisource.org/zh-hant/三國演義/第015回','https://zh.wikisource.org/zh-hant/三國演義/第053回'],'assets':[]}
for i,(name,s,r) in enumerate(zip(names,src,raws)):
 dest=P/'candidates'/(name+'.png');shutil.copy2(s,dest);im=Image.open(dest).convert('RGBA');im.thumbnail((440,660) if i<4 else (585,390));x=10+i*448 if i<4 else 10+(i-4)*595;y=55 if i<4 else 780;sheet.paste(im,(x,y),im);d.text((x+5,y+im.height+10),name,font=f,fill='white')
 m['assets'].append({'id':name,'raw':str(r),'candidate':str(dest),'native_size':list(Image.open(r).size),'candidate_size':list(Image.open(dest).size),'sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'story_target':None if i<4 else f'card{i-2:02d}'})
 im=Image.open(r);im.crop((0,0,im.width,min(850,im.height))).save(P/'qa'/f'{i+1:02d}-face-hands-weapon.png')
d.text((30,1240),'北海赴义 → 神亭相持 → 日中践诺 → 合肥阵前争锋（不改写后续败局）',font=f,fill='#e2b792')
d.text((30,1290),'被动：连刺＝第二次普攻增伤；酬义＝友军受击后下次普攻增伤；劲臂＝命中率提高。',font=f,fill='white')
d.text((30,1340),'主动草案：向单一目标连续两次枪刺。四阶收藏强度并非四次胜利。',font=f,fill='white')
sheet.save(P/'太史慈-四阶三传记-重做总览.png');(P/'manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2))
(P/'research'/'核验与制作说明.md').write_text('第11回：奉母意助孔融，腰带弓矢、手持铁枪突围求刘备。第15回：神亭与孙策相持，互挟枪落马后弃枪厮打；背上短戟被夺。青铜卡斜枪立姿是此事件动作提炼的原创卡面，非逐字复现下马弃枪瞬间。日中按约归来，原文一千余众；银卡与传记以信义归营衔接。第53回：太史慈抢先迎张辽，七八十合不分胜负，后方变故导致吴军败退；其后夜袭中伏受伤而亡。金卡/传记仅取日间阵前交战，不暗示凯旋。\n原文2026-10-18核验Wikisource第11、15、53回。赤背神猿、面貌服装、赭栗马色、技能皆原创候选。无原著武器坐骑专名冒称。黑铁淡猿云影、青铜首肩、白银厚肩实体、黄金巨臂增长。四卡吴橘红徽、弓骑兵图标、1至4星，技能数量1/1/2/3，统一底部槽位961/1045/1129。\n')
(P/'qa'/'QA.md').write_text('逐张查看七原图及四UI。人物面貌一致；长枪轴连续、两握点可读；银卡开放手五指、移入边框以内。黑铁过亮猿首已用内置生成天空局部修复、遮罩回贴；银卡手臂按局部遮罩回贴，其余保留原图。无全幅像素平滑或锐化。人物不被UI遮脸手；金后手靠右但完整位于边框内。原图1024x1536和1536x1024，不宣称4K。UI未覆盖区差0见composition-manifest。武器和马头部分可自然出画。待用户审阅；配角孙策、张辽是本套原创配角表现，非调用其正式资产。\n')
(P/'failures'/'log.txt').write_text('card01-guardian-too-visible.png：初版猿首过显，已局部淡化。card03-hand-under-frame.png：初版右手被UI遮，已折肘修复。\n')
(P/'progress.json').write_text(json.dumps({'stage':'ready_for_library','seven_images':7,'candidate_only':True},ensure_ascii=False))
print(json.dumps([{'file_name':s.name,'workspace_path':str(s),'file_size_bytes':s.stat().st_size,'purpose':'create_library_file','library_artifact_type':'image'} for s in [*(P/'candidates').glob('*.png'),P/'太史慈-四阶三传记-重做总览.png']],ensure_ascii=False))
