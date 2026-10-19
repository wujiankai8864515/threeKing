from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import importlib.util,json,hashlib,argparse,shutil
P=Path(__file__).resolve().parent
BASE=Path('/workspace/scratch/3f82ff2b3f81/guanyu-advanced/ui-reference-fit_20261019_200600_UTC+08/render.py')
ap=argparse.ArgumentParser();ap.add_argument('--source',required=True);args=ap.parse_args()
spec=importlib.util.spec_from_file_location('standard',BASE);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
recs=json.loads((P/'material-config.json').read_text());results=[]
for r in recs:
 folder=P/(r['id']+'-'+r['name']);m.P=folder
 cfg={'hero':'guanyu','name':'机甲·关羽','branch':'封侯','branch_id':r['id'],'tier':6,'level':1,'source':str(Path(args.source).resolve()),'outdir':str(folder),'skills':[{'name':'重甲','level':2},{'name':'蓄能','level':2},{'name':'反制','level':2}]}
 res=m.compose(cfg);res['frame_material']=r;results.append(res)
thumbs=Image.new('RGB',(2050,680),'#182128');d=ImageDraw.Draw(thumbs);f=ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc',25)
for i,(r,v) in enumerate(zip(recs,results)):
 im=Image.open(v['output']);im.thumbnail((400,600));thumbs.paste(im,(i*410,60),im);d.text((i*410+15,12),r['id']+' '+r['name'],font=f,fill='#eee5cf')
thumbs.save(P/'00-六星标准布局五材质总览.png');(P/'manifest.json').write_text(json.dumps(results,ensure_ascii=False,indent=2));shutil.copy2(BASE,P/'reference-standard-render.py');shutil.copy2(args.source,P/'reference-main-art.png')
(P/'sha256.json').write_text(json.dumps({str(f.relative_to(P)):hashlib.sha256(f.read_bytes()).hexdigest() for f in P.rglob('*.png')},ensure_ascii=False,indent=2))
