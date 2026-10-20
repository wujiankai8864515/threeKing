from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,hashlib
P=Path(__file__).resolve().parent
names=['玉玺天诏','六曜星盘','晶翼破界','双阙封侯','圣谕长卷','侯印悬章','玄晶碑铭','龙鳞战旗','天书折页','天穹棱镜','星阶神座','圣莲琉璃','侯爵册封令','乾坤双环','破晓晶舰','浮空六曜','天命折扇','封禅玉璧','神域界门','无界神藏']
rows=[]
for n,name in enumerate(names,1):
 d=P/f'{n:02}'; f=d/('card.png' if n<=7 else 'final.png' if n in [16,17] else 'native.png')
 im=Image.open(f)
 rows.append(dict(id=f'{n:02}',name=name,path=str(f),size=list(im.size),bytes=f.stat().st_size,sha256=hashlib.sha256(f.read_bytes()).hexdigest(),six_stars_visually_checked=True,all_required_semantic_fields_present=True,status='candidate_pending_user_review',typography_note='Some calligraphic traditional Chinese glyphs are retained.'))
font=ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',26)
def sheet(sub,filename,cols,w):
 h=int(w*1.5); rowh=h+60; out=Image.new('RGB',(cols*w,((len(sub)+cols-1)//cols)*rowh),(19,26,32));dr=ImageDraw.Draw(out)
 for i,r in enumerate(sub):
  im=Image.open(r['path']).convert('RGB'); im.thumbnail((w-12,h)); x=(i%cols)*w+(w-im.width)//2;y=(i//cols)*rowh;out.paste(im,(x,y));dr.text(((i%cols)*w+14,y+h+10),r['id']+' '+r['name'],font=font,fill='#f3ead5')
 out.save(P/filename,quality=94)
sheet(rows,'00-六星全新构思20款总览.jpg',5,360)
sheet(rows[:10],'00A-六星全新构思01-10.jpg',5,420)
sheet(rows[10:],'00B-六星全新构思11-20.jpg',5,420)
manifest=dict(status='local_complete_upload_blocked',count=20,source_illustration='/workspace/scratch/3f82ff2b3f81/guanyu-advanced/sixstar-diamond10_20261020_100400_UTC+08/source-08-unchanged.png',identity_note='Generated layout concepts preserve recognizable selected character identity; they are not pixel-identical deterministic inserts.',method='built-in imagegen',overview=str(P/'00-六星全新构思20款总览.jpg'),detail_overviews=[str(P/'00A-六星全新构思01-10.jpg'),str(P/'00B-六星全新构思11-20.jpg')],variants=rows,library_status='not_uploaded; Library upload blocked by HTTP403 before upload',corrections={'05':'Initial seven-star candidate retained; card.png is corrected six-star final.','16':'native.png incorrect first passive glyph; final.png correct 镇岳, repaired bottom passive panel.','17':'native.png and three edit attempts have five stars; final.png regenerated fan layout with six stars in horizontal middle rating rail.'})
(P/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
print(json.dumps({'manifest':str(P/'manifest.json'),'count':20,'bytes':sum(r['bytes'] for r in rows)},ensure_ascii=False))
