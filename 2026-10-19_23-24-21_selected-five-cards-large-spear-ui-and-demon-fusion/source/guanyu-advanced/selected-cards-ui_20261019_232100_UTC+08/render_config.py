from pathlib import Path
import argparse,importlib.util,json
P=Path(__file__).resolve().parent
ap=argparse.ArgumentParser();ap.add_argument('--config',required=True);a=ap.parse_args();cfg=json.loads(Path(a.config).read_text())
spec=importlib.util.spec_from_file_location('standard',P/'render.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
if cfg['tier']==6:m.P=Path('/workspace/scratch/3f82ff2b3f81/sixstar-frame-exploration/20261019_221150_UTC+08-enhance-03-04/03-象牙金釉·御铸')
r=m.compose(cfg);print(json.dumps(r,ensure_ascii=False))
