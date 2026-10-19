from pathlib import Path
import argparse,importlib.util,json
P=Path(__file__).resolve().parent
ap=argparse.ArgumentParser();ap.add_argument('--config',required=True);a=ap.parse_args();cfg=json.loads(Path(a.config).read_text())
spec=importlib.util.spec_from_file_location('standard',P/'render.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
m.P=P
r=m.compose(cfg);print(json.dumps(r,ensure_ascii=False))
