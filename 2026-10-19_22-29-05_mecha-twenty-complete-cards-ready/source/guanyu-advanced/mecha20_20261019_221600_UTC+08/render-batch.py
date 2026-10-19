import json,os,subprocess
from pathlib import Path
p=Path('/workspace/scratch/3f82ff2b3f81/guanyu-advanced/mecha20_20261019_221600_UTC+08'); jobs={j['id']:j for j in json.loads((p/'actual-plan.json').read_text())}
for n,f in json.loads(Path('/tmp/mecha20paths.json').read_text()).items():
 d=p/n;d.mkdir(exist_ok=True);src=Path('/workspace/scratch/3f82ff2b3f81/generated_images')/f; dest=d/'source.png'
 if not dest.exists():os.link(src,dest)
 cfg={'hero':'guanyu','name':'机甲·关羽','branch':'封侯','branch_id':'explore-'+n,'tier':6,'level':1,'source':str(dest),'outdir':str(d/'card'),'skills':[{'name':s,'level':2} for s in ['重甲','蓄能','反制']]}
 (d/'config.json').write_text(json.dumps(cfg,ensure_ascii=False,indent=2));(d/'actual-args.json').write_text(json.dumps(dict(jobs[n],original_output=str(src)),ensure_ascii=False,indent=2))
 if not (d/'card').exists():subprocess.run(['python','/workspace/scratch/3f82ff2b3f81/sixstar-frame-exploration/20261019_221150_UTC+08-enhance-03-04/render_config.py','--config',str(d/'config.json')],stdout=subprocess.DEVNULL,check=True)
print('rendered',len(list(p.glob('*/card/*.json'))))
