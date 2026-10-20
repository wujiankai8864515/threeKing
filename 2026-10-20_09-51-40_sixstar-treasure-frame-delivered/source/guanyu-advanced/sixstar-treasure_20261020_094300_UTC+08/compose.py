from pathlib import Path
from PIL import Image,ImageDraw
import importlib.util,json,numpy as np
P=Path(__file__).resolve().parent
old=P.parent/'frame-hierarchy_20261020_000010_UTC+08'
a=Image.open(P/'generated-frame-source.png').convert('RGBA').resize((1310,1966),Image.Resampling.LANCZOS)
# Normalize generated transparency and reposition the empty title plate to the locked standard anchor.
arr=np.array(a);alpha=arr[:,:,3];alpha[alpha<16]=0;alpha[alpha>240]=255;arr[:,:,3]=alpha;arr[alpha==0,:3]=0;a=Image.fromarray(arr)
original=a.copy();title=a.crop((300,222,1044,342));a.paste((0,0,0,0),(300,222,1044,342));a.alpha_composite(title,(300,188));a.paste((0,0,0,0),(333,308,984,342))
# Preserve the overlapping level diamond above the moved title rail.
protected=Image.new('L',a.size);pd=ImageDraw.Draw(protected);pd.polygon([(1116,158),(1254,307),(1116,431),(984,308)],fill=255);pd.polygon([(0,0),(333,0),(333,210),(337,235),(344,285),(333,334),(382,342),(382,406),(333,418),(333,480),(0,480)],fill=255)
a.paste(original,(0,0),protected)
a.save(P/'frame-6star-expanded.png');a.crop((60,140,1250,1926)).save(P/'frame-6star.png')
spec=importlib.util.spec_from_file_location('standard',P/'render.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);m.P=P
cfg=json.loads((old/'mecha6-config.json').read_text());cfg['outdir']=str(P/'card');cfg['branch_id']='selected08-treasure';cfg['source']=str(P/'source-08-unchanged.png')
(P/'card-config.json').write_text(json.dumps(cfg,ensure_ascii=False,indent=2))
r=m.compose(cfg)
card=Image.new('RGBA',(1310,1966));core=Image.open(r['output']);card.alpha_composite(a);card.paste(core,(60,140));card.save(P/'六星机甲关羽-立体宝物框.png')
bg=Image.new('RGBA',card.size,(29,34,39,255));bg.alpha_composite(card);bg.convert('RGB').save(P/'QA-card-neutral.jpg')
(P/'manifest-draft.json').write_text(json.dumps(r,ensure_ascii=False,indent=2))
