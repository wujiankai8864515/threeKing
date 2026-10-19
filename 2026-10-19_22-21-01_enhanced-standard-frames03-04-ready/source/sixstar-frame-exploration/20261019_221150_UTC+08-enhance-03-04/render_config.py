"""Reusable complete-card renderer. Never repaints the clean illustration."""
from pathlib import Path
import argparse,importlib.util,json
P=Path(__file__).resolve().parent
BASE=Path('/workspace/scratch/3f82ff2b3f81/guanyu-advanced/ui-reference-fit_20261019_200600_UTC+08/render.py')
ap=argparse.ArgumentParser();ap.add_argument('--config',required=True);args=ap.parse_args();cfg=json.loads(Path(args.config).read_text())
spec=importlib.util.spec_from_file_location('standard',BASE);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
if cfg['tier']==6:m.P=P/'03-象牙金釉·御铸'
# Five-star retains original diamond frame; tian/fenghou choice is tier-driven by standard renderer.
r=m.compose(cfg);print(json.dumps(r,ensure_ascii=False))
