from pathlib import Path
from PIL import Image
import json,shutil,importlib.util,numpy as np
P=Path(__file__).resolve().parent;root=P.parent
raw=Path('/workspace/scratch/3f82ff2b3f81/generated_images/exec-9d3ffd90-0ff0-4903-b191-d02b10a80878.png');shutil.copy2(raw,P/'generated-transparent-assets.png');im=Image.open(raw).convert('RGBA')
for name,box,size in [('tian-metal-calligraphy',(0,0,1100,732),(150,145)),('spearhead',(1100,0,2149,732),(120,115))]:
 a=im.crop(box);a=a.crop(a.getchannel('A').getbbox());a.save(P/(name+'-source.png'));a.thumbnail(size,Image.Resampling.LANCZOS);canvas=Image.new('RGBA',size);canvas.alpha_composite(a,((size[0]-a.width)//2,(size[1]-a.height)//2));canvas.save(P/(name+'.png'))
shutil.copy2(root/'ui-calligraphy_20261019_191150_UTC+08/render.py',P/'render.py')
s=importlib.util.spec_from_file_location('r',P/'render.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
results=[]
for key in ['mecha','demon']:
 cp=root/'branch-skills_20261019_192400_UTC+08'/key/'config.json';c=json.loads(cp.read_text());old=Path(c['outdir'])/f"{c['hero']}-{c['branch_id']}-5star.png";c['outdir']=str(P/key);(P/key).mkdir(exist_ok=True);(P/key/'config.json').write_text(json.dumps(c,ensure_ascii=False,indent=2));r=m.compose(c)
 a=np.array(Image.open(old));b=np.array(Image.open(r['output']));diff=np.any(a!=b,axis=2);allow=np.zeros(diff.shape,bool);allow[1500:1710,60:320]=1;allow[1540:1720,950:1150]=1;assert not (diff&~allow).any();r['outside_rank_and_troop_UI_changed']=0;results.append(r)
(P/'manifest.json').write_text(json.dumps(results,ensure_ascii=False,indent=2))
shutil.copy2(root/'branch-skills_20261019_192400_UTC+08/技能说明草案.md',P/'技能说明草案.md')
