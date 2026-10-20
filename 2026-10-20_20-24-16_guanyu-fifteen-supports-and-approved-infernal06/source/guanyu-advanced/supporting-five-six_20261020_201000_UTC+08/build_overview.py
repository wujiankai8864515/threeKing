from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
import json,hashlib
b=Path(__file__).resolve().parent; d=json.loads((b/'complete-supporting-manifest.json').read_text())
font='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
f=ImageFont.truetype(font,30);sm=ImageFont.truetype(font,23);title=ImageFont.truetype(font,40)
w=1576;rowh=415; im=Image.new('RGB',(w,2205),(24,29,35)); draw=ImageDraw.Draw(im)
draw.text((34,20),'关羽全套配套 · 五形态 / 十五张',font=title,fill='white')
draw.text((34,78),'左：场景传记　　中：透明放招 CG（静态）　　右：透明头像　｜　候选待审',font=sm,fill=(190,200,210))
forms=[('mecha5','01 五星机甲 · 青龙启甲'),('heritage5','02 五星传承 · 江汉承威'),('divine5','03 五星神 · 万军同心'),('demon5','04 五星魔 · 握旗噬天'),('mecha6','05 六星封侯机甲 · 空域护城')]
for ri,(form,name) in enumerate(forms):
 y=126+ri*rowh;draw.text((34,y),name,font=f,fill=(230,221,185));es=[e for e in d['entries'] if e['form']==form]
 for ci,e in enumerate(es):
  x=24+ci*520;py=y+49;tile=Image.new('RGBA',(508,338),(110,110,110,255));src=Image.open(e['path']).convert('RGBA');src.thumbnail((498,328),Image.Resampling.LANCZOS);tile.alpha_composite(src,((508-src.width)//2,(338-src.height)//2));im.paste(tile.convert('RGB'),(x,py))
p=b/'关羽全套配套-15图总览.jpg';im.save(p,quality=89,optimize=True)
d['overview']={'path':str(p),'size_bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'generation':'Contact sheet of existing assets; originals unchanged; alpha displayed over middle gray.'};(b/'complete-supporting-manifest.json').write_text(json.dumps(d,ensure_ascii=False,indent=2))
u=json.loads((b/'upload-all-request.json').read_text());u['uploads'].append({'local_path':str(p),'purpose':'create_library_file','library_artifact_type':'image'});(b/'upload-all-request.json').write_text(json.dumps(u,ensure_ascii=False,indent=2))
print(p,p.stat().st_size)
