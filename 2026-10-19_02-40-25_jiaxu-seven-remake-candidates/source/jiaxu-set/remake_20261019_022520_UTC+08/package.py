from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,hashlib,shutil
p=Path(__file__).parent;d=p/'delivery';d.mkdir(exist_ok=True)
tiers=['iron','bronze','silver','gold'];names=['黑铁-乱军一言','青铜-宛城暗门','白银-东南藏锋','黄金-缄书断盟']; storynames=['盛宴外的迟疑','三日看城','旧话后的新疑'];files=[]; records=[]
cm=json.loads((p/'ui/composition-manifest.json').read_text())
for i,t in enumerate(tiers):
 src=p/'ui'/cm['cards'][t]['output'];out=d/f'贾诩-{i+1:02d}-{names[i]}.png';shutil.copy2(src,out);files.append(out)
for i,n in enumerate(storynames,1):
 out=d/f'贾诩-传记{i:02d}-{n}.png';shutil.copy2(p/'raw'/f'story{i:02d}.png',out);files.append(out)
fnt=ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',24)
ov=Image.new('RGB',(1600,1120),'#161820');dr=ImageDraw.Draw(ov)
for i,f in enumerate(files[:4]):
 im=Image.open(f).convert('RGBA');im.thumbnail((370,555));ov.paste(im,(15+i*400,40),im);dr.text((30+i*400,610),names[i],font=fnt,fill='white')
for i,f in enumerate(files[4:]):
 im=Image.open(f).convert('RGB');im.thumbnail((510,340));ov.paste(im,(15+i*530,690));dr.text((20+i*530,1045),f'传记{i+1} · '+storynames[i],font=fnt,fill='white')
ov.save(d/'贾诩-七图总览.jpg',quality=94)
for f in (p/'raw').glob('*.png'):
 im=Image.open(f);w,h=im.size;records.append({'asset':f.stem,'path':str(f),'native_size':[w,h],'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'source':(p/'raw'/f'{f.stem}.source.txt').read_text().strip() if (p/'raw'/f'{f.stem}.source.txt').exists() else 'generated_images/exec-25357b25-f308-43b7-b924-477a5007155b.png'})
 im.crop((int(w*.15),int(h*.1),int(w*.8),int(h*.7))).save(p/'qa'/f'{f.stem}-face-hands.png')
manifest={'hero':'贾诩','status':'seven_new_candidates_pending_user_review','raw_assets':records,'delivery':[str(f) for f in files],'overview':str(d/'贾诩-七图总览.jpg'),'ui_canvas':[1190,1786],'native_card':[1024,1536],'native_story':[1536,1024],'upscale':False,'native_art_placement':'1:1 (84,145), only UI frame resized','source_research':'research/brief.json and verification.md','passives':'审隙：封援时间提高；远谋：选取距离提高；敛息：范围伤害降低。1/1/2/3技能条；LV1均为示例。','collection_faction':'群，四阶固定紫徽','myth_proposal':'原创缄影玄蛛，非原著法术','qa':'全部七原图及四卡UI已逐图观察；脸手可读，UI不遮主角脸手，无金粉照片皮肤。金卡神蛛/疏网生成在帐外远景上方而非原计划远地；低对比，主角保持最清晰。黑铁初版照片感退件保留。','tool':'built-in image_gen','git':'not touched'}
(p/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2));(p/'progress.json').write_text(json.dumps({'status':'packaged_pending_library','primary':7,'overview':1},indent=2))
(p/'qa/QA.md').write_text('''# 贾诩七图候选 QA
七张单独内置生图，未用总览替代。四卡1024×1536、三传记1536×1024。UI1190×1786中原画1:1。
逐图检查：黑铁举指、铜卡托颏移签、银卡袖前调度、金卡案前指书；四卡脸部稳定。神话线索一线、三线、街角半网、帐外玄蛛全网。金卡网位于远景天空而非原计划地面，记录为构图偏差，但不挡人物，不作历史事实。黑铁初版照片感已废弃保存。
群收藏紫徽固定；剧情未错误显示统一群旗。独立谋士兵种icon与动态文字，未复用张角人名技能。被动条1/1/2/3，锚点961/1045/1129，字墨中心与阶章由脚本计量。UI没有遮贾诩面部或手。全部新候选待用户审阅。
''')
