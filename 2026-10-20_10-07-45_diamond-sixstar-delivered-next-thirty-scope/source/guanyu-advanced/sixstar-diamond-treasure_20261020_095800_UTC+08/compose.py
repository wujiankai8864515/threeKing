from pathlib import Path
from PIL import Image
import importlib.util,json,numpy as np
P=Path(__file__).resolve().parent
old=P.parent/'frame-hierarchy_20261020_000010_UTC+08'
# Preserve the already-approved entire structural footprint including crown and floating ornaments.
reference=Image.open(P/'reference-approved-structure.png').convert('RGBA')
generated=Image.open(P/'generated-frame-source.png').convert('RGBA').resize(reference.size,Image.Resampling.LANCZOS)
a=np.array(generated);a[:,:,3]=np.array(reference)[:,:,3];a[a[:,:,3]==0,:3]=0;frame=Image.fromarray(a)
frame.save(P/'frame-6star-expanded.png');frame.crop((60,140,1250,1926)).save(P/'frame-6star.png')
spec=importlib.util.spec_from_file_location('standard',P/'render.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);m.P=P
cfg=json.loads((old/'mecha6-config.json').read_text());cfg['outdir']=str(P/'card');cfg['branch_id']='selected08-diamond-treasure';cfg['source']=str(P/'source-08-unchanged.png')
(P/'card-config.json').write_text(json.dumps(cfg,ensure_ascii=False,indent=2))
r=m.compose(cfg)
card=frame.copy();card.paste(Image.open(r['output']),(60,140));card.save(P/'六星机甲关羽-钻石立体宝物框.png')
bg=Image.new('RGBA',card.size,(29,34,39,255));bg.alpha_composite(card);bg.convert('RGB').save(P/'QA-card-neutral.jpg')
ui=Image.new('RGBA',card.size);ui.alpha_composite(Image.open(r['text_layer']),(60,140));ui.save(P/'dynamic-ui-expanded.png')
(P/'manifest-draft.json').write_text(json.dumps(r,ensure_ascii=False,indent=2))
card.crop((45,120,1275,470)).save(P/'QA-top.png');card.crop((800,1160,1190,1510)).save(P/'QA-passives.png')
