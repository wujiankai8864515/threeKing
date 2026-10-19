from pathlib import Path
import os,json
p=Path(__file__).resolve().parent
rows={}
for f in sorted(p.glob('library-*.json')):
 if f.name=='library-card-index.json':continue
 r=json.loads(f.read_text());s=r.get('structuredContent',{})
 for a in s.get('results',[]):
  if a.get('status')=='succeeded':
   rows[a['file_name']]=a
   for x in a.get('xattrs',[]):
    path=p/'cards'/a['file_name']
    if path.exists():os.setxattr(path,x['name'],x['value'].encode())
(p/'library-card-index.json').write_text(json.dumps(list(rows.values()),ensure_ascii=False,indent=2))
print('successful indexed files',len(rows),'cards',len([n for n in rows if n.endswith('star.png')]))
