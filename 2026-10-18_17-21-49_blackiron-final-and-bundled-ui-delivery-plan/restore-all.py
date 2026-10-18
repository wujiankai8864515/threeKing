from pathlib import Path
import json,hashlib,argparse,shutil
p=argparse.ArgumentParser();p.add_argument('--output',type=Path);a=p.parse_args();repo=Path(__file__).resolve().parents[1];latest=json.loads((repo/'LATEST.json').read_text());items={}
for e in json.loads((repo/latest['snapshot']/'asset-index.json').read_text())['entries']:items[e['original_path']]={'repository_path':latest['snapshot']+'/'+e['stored_path'],**e}
for delta in latest.get('asset_deltas',[]):
 for e in json.loads((repo/delta/'asset-index.json').read_text())['entries']:items[e['original_path']]=e
for name,e in items.items():
 src=repo/e['repository_path']
 assert src.resolve().is_relative_to(repo)
 assert hashlib.sha256(src.read_bytes()).hexdigest()==e['sha256'],name
print('Verified',len(items),'resolved source paths')
if a.output:
 if a.output.exists():raise SystemExit('Output must not exist')
 a.output.mkdir(parents=True)
 for name,e in items.items():
  target=a.output/name
  assert target.resolve().is_relative_to(a.output.resolve())
  target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(repo/e['repository_path'],target)
 print('Restored',a.output)
