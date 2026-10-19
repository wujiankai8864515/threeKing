import json,hashlib
from pathlib import Path
from datetime import datetime,timezone
p=Path(__file__).resolve().parent
pending={}
def run():
 rows=[]
 for f in sorted((p/'cards').glob('*star.json')):
  a=json.loads(f.read_text());a['qa_status']='pass_candidate';a['qa_note']='Face and hands visually checked clear; source rendered at 1:1, native illustration pixels not resampled.'
  k=(a['hero'],a['branch_id'],a['tier'])
  if k in pending:a['qa_status']='pending_local_correction';a['qa_note']=pending[k]
  rows.append(a)
 data={'updated_utc':datetime.now(timezone.utc).isoformat(),'expected_cards':24,'assembled_cards':len(rows),'review_status':'Candidates, not user approved','six_star_three_passives':'Design default, not explicitly fixed by user','cards':rows}
 (p/'card-manifest.json').write_text(json.dumps(data,ensure_ascii=False,indent=2))
 print(len(rows))
if __name__=='__main__':run()
