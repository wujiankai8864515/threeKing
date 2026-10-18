from pathlib import Path
import json,hashlib
from PIL import Image
R=Path('/workspace/scratch/3f82ff2b3f81');D=Path(__file__).parent
heroes={'liubei':'刘备','zhangfei':'张飞','zhaoyun':'赵云','machao':'马超','huangzhong':'黄忠','zhugeliang':'诸葛亮','pangtong':'庞统'}
receipts=list((R/'hero-production-spec').rglob('*results*.json'))
for h in heroes:receipts+=list((R/(h+'-set')).rglob('*results*.json'))
latest={}
for p in sorted(receipts,key=lambda p:p.stat().st_mtime):
 try:j=json.loads(p.read_text())
 except:continue
 rows=j.get('results',[]) if isinstance(j,dict) else j
 if not isinstance(rows,list):continue
 for a in rows:
  if not isinstance(a,dict) or a.get('status')!='succeeded' or not a.get('library_file_id'):continue
  k=a['library_file_id'];old=latest.get(k)
  if old and old.get('current_version_number',0)>a.get('current_version_number',0):continue
  latest[k]={**a,'receipt':str(p)}
index={'created_local':'2026-10-18T21:05:20+08:00','scope':'蜀八套；关羽新尾整合等待，其他七人已存','approval':'technical_candidates_not_user_final','pixel_statement':'pure cards1024x1536, biographies1536x1024; UI1190x1786 art1:1 frame enlarged','heroes':{}}
for h,name in heroes.items():
 rows=[]
 for a in latest.values():
  p=Path(a.get('local_path',''))
  if '/'+h+'-set/' not in str(p) or p.suffix.lower()!='.png':continue
  sz=Image.open(p).size
  kind='overview' if '总览' in p.name else 'complete_ui' if '完整UI' in p.name else 'pure_card' if sz==(1024,1536) else 'biography'
  rows.append({'type':kind,'file':str(p),'native_or_composite_pixels':sz,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'library_file_id':a['library_file_id'],'library_version':a.get('current_version_number'),'receipt':a['receipt'],'status':'root_and_independent_technical_candidate_pass','user_final_approval':False})
 counts={t:sum(x['type']==t for x in rows) for t in ['pure_card','biography','complete_ui','overview']}
 index['heroes'][h]={'name':name,'counts':counts,'files':rows}
 print(name,counts)
(D/'CURRENT_SHU_CANDIDATE_INDEX.json').write_text(json.dumps(index,ensure_ascii=False,indent=2))
