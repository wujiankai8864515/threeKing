from pathlib import Path
import importlib.util,json
root=Path('/workspace/scratch/3f82ff2b3f81');p=Path('/tmp/liubei-complete_20261020_160600_UTC');base=root/'guanyu-advanced/frame-hierarchy_20261020_000010_UTC+08'
spec=importlib.util.spec_from_file_location('m',base/'render.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);m.P=base
entries=[]
for form,title,img,skills in [
('heritage5','传承·刘备','exec-308be7be-096d-4c60-86a2-0ce69934dd10.png',['仁德','同袍','匡汉']),
('divine5','神·刘备','exec-3f0c61d0-bb8c-4976-aabb-b5446099e06a.png',['慈照','玉佑','济世']),
('demon5','魔·刘备','exec-20890c90-25b2-469c-a9a7-da78b0caf133.png',['孤誓','冥护','返魂']),
('mecha5','机甲·刘备','exec-b5f63696-5310-4f2d-aa6d-f0a0cd4f08c8.png',['双驱','玉核','城卫'])]:
 cfg={'hero':'liubei','name':title,'tier':5,'branch_id':form,'source':str(root/'generated_images'/img),'outdir':str(p/form),'skills':[{'name':s,'level':1} for s in skills],'skill_values_status':'draft_not_balanced','troop_class':'长枪兵'}
 r=m.compose(cfg);entries.append({'hero':'liubei','form':form,'tier':5,'kind':'card','local_path':r['output'],'source':cfg['source'],'status':'candidate_pending_review','qa':'uncovered source pixels unchanged','passives':skills})
json.dump({'entries':entries},open(p/'five-star-cards-manifest.json','w'),ensure_ascii=False,indent=2)
