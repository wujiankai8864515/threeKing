from pathlib import Path
from PIL import Image
import shutil,json,importlib.util,numpy as np
P=Path(__file__).resolve().parent;R=P.parent;old=R/'ui-metal-assets_20261019_192445_UTC+08'
for name,src in [('tian-metal-calligraphy','exec-8ac24f6a-cd7e-4651-927a-6f55dc3ead8c.png'),('fenghou-metal','exec-18908bc3-a7f3-4bc0-bcf0-81206236394d.png')]:
 path=R.parent/'generated_images'/src;shutil.copy2(path,P/(name+'-source.png'));im=Image.open(path).convert('RGBA');im=im.crop(im.getchannel('A').getbbox());im.thumbnail((150,145),Image.Resampling.LANCZOS);c=Image.new('RGBA',(150,145));c.alpha_composite(im,((150-im.width)//2,(145-im.height)//2));c.save(P/(name+'.png'))
shutil.copy2(old/'spearhead.png',P/'spearhead.png');s=(old/'render.py').read_text();s='\n'.join(x for x in s.split('\n') if 'd.ellipse((901*SX-58' not in x);s=s.replace("ASSET/'tian-metal-calligraphy.png'","ASSET/('fenghou-metal.png' if tier==6 else 'tian-metal-calligraphy.png')");(P/'render.py').write_text(s)
spec=importlib.util.spec_from_file_location('r',P/'render.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
configs=[('mecha',old/'mecha/config.json'),('divine',R/'divine-devotion_20261019_192400_UTC+08/config.json'),('heritage',R/'heritage-water-command_20261019_193312_UTC+08/config.json')];results=[]
for key,cp in configs:
 c=json.loads(cp.read_text());prev=Path(c['outdir'])/f"{c['hero']}-{c['branch_id']}-{c['tier']}star.png";c['outdir']=str(P/key)
 if key=='heritage': c['skills']=[{'name':x,'level':1} for x in ['龙骧','震夏','武圣']];c['active_skill']={'name':'水淹七军','status':'draft_no_fixed_values'}
 (P/key).mkdir(exist_ok=True);(P/key/'config.json').write_text(json.dumps(c,ensure_ascii=False,indent=2));r=m.compose(c)
 if prev.exists():
  a=np.array(Image.open(prev));b=np.array(Image.open(r['output']));d=np.any(a!=b,axis=2);mask=np.zeros(d.shape,bool);mask[1500:1710,60:320]=1;mask[1540:1720,950:1150]=1
  if key=='heritage':mask[1050:1350,820:1110]=1
  assert not(d&~mask).any();r['outside_authorized_UI_changed']=0
 results.append(r)
(P/'manifest.json').write_text(json.dumps(results,ensure_ascii=False,indent=2))
