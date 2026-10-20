from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import importlib.util,json,numpy as np,hashlib,argparse
P=Path(__file__).resolve().parent;src=P/'source-08-unchanged.png';jobs=json.loads((P/'jobs.json').read_text())
spec=importlib.util.spec_from_file_location('standard',P/'render.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);m.MASK=P/'art-native-slot-mask.png'
basecfg=json.loads((P/'standard-config.json').read_text());oldmeta=json.loads((P/'standard-glyph-anchors.json').read_text());art=np.array(Image.open(src).convert('RGBA'));mask=np.array(Image.open(m.MASK).convert('L'))
parser=argparse.ArgumentParser();parser.add_argument('--ids',default='01,02,03,04,05,06,07,08,09,10');args=parser.parse_args();ids=args.ids.split(',')
for job in jobs:
 if job['id'] not in ids:continue
 d=P/job['id'];native=d/'generated-frame-source.png'
 if not native.exists():continue
 frame=Image.open(native).convert('RGBA').resize((1310,1966),Image.Resampling.LANCZOS);a=np.array(frame);alpha=a[:,:,3];alpha[alpha<16]=0;alpha[alpha>240]=255;a[:,:,3]=alpha;a[alpha==0,:3]=0;frame=Image.fromarray(a)
 if job['id']=='07':
  # Remove a stray inherited title construction line in the transparent opening.
  frame.paste((0,0,0,0),(347,330,973,365))
 frame.save(d/'frame-6star-expanded.png');frame.crop((60,140,1250,1926)).save(d/'frame-6star.png')
 cfg={**basecfg,'source':str(src),'outdir':str(d/'card'),'branch_id':'holy-explore-'+job['id']};(d/'card-config.json').write_text(json.dumps(cfg,ensure_ascii=False,indent=2));m.P=d;r=m.compose(cfg)
 core=Image.open(r['output']).convert('RGBA');full=frame.copy();full.paste(core,(60,140));out=d/(job['id']+'-'+job['name']+'-六星机甲关羽.png');full.save(out)
 ui=Image.new('RGBA',full.size);ui.alpha_composite(Image.open(r['text_layer']),(60,140));ui.save(d/'dynamic-ui-expanded.png')
 mask2=Image.new('L',full.size);mask2.paste(Image.fromarray(mask),(60,140));reg=(slice(285,1821),slice(144,1168));valid=(np.array(mask2)[reg]==255)&(np.array(frame)[:,:,3][reg]==0)&(np.array(ui)[:,:,3][reg]==0);changed=int((np.any(np.array(full)[reg]!=art,axis=2)&valid).sum());assert changed==0;assert r['glyph_centers']==oldmeta['glyph_centers']
 result={**r,'variant_id':job['id'],'variant_name':job['name'],'output':str(out),'frame':str(d/'frame-6star-expanded.png'),'text_layer':str(d/'dynamic-ui-expanded.png'),'canvas_size':[1310,1966],'core_canvas_size':[1190,1786],'core_offset':[60,140],'illustration_offset':[144,285],'uncovered_art_pixels_checked':int(valid.sum()),'uncovered_art_pixels_changed':changed,'dynamic_glyph_anchors_match_standard':True,'native_frame_size':list(Image.open(native).size),'status':'composed_pending_visual_review','output_sha256':hashlib.sha256(out.read_bytes()).hexdigest()};(d/'manifest.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
 print(json.dumps({'id':job['id'],'output':str(out),'checked':int(valid.sum()),'changed':changed},ensure_ascii=False))
 # Intermediate renderer whole-core preview is not a second deliverable; keep UI/config only.
 Path(r['output']).unlink();Path(r['output'].replace('.png','-preview.png')).unlink()
ready=[j for j in jobs if (Path(j['directory'])/'manifest.json').exists()]
for subset,label in [(ready[:5],'01-05'),(ready[5:],'06-10')]:
 if not subset:continue
 thumbw,thumbh=360,540;sheet=Image.new('RGB',(thumbw*len(subset),thumbh+44),(25,31,39));dd=ImageDraw.Draw(sheet);font=ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',21)
 for n,j in enumerate(subset):
  rr=json.loads((Path(j['directory'])/'manifest.json').read_text());im=Image.open(rr['output']).convert('RGBA');im.thumbnail((thumbw,thumbh));sheet.paste(im,(n*thumbw+(thumbw-im.width)//2,0),im);dd.text((n*thumbw+20,548),j['id']+' '+j['name'],font=font,fill='white')
 sheet.save(P/('QA-cards-'+label+'.jpg'),quality=92)
