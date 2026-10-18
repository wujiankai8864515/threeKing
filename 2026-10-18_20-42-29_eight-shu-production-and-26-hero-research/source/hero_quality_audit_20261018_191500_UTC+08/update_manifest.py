from pathlib import Path
from PIL import Image
import json,hashlib,datetime
root=Path('.'); out=Path('hero_quality_audit_20261018_191500_UTC+08/candidate_sources_sha256.json');d=json.loads(out.read_text());current={(v['hero'],v['asset']):v for v in d['candidates']}
rows='''liubei|gold|liubei-set/gold-royal-regalia-local_2026-10-18_19-42-09_UTC+08/刘备-黄金*.png
zhaoyun|silver|zhaoyun-set/silver_rescue_2026-10-18_19-38-48_UTC+08/赵云-白银-v1*.png
zhaoyun|gold|zhaoyun-set/gold-upright-spear_2026-10-18_20-09-38_UTC+08/赵云-黄金*.png
zhaoyun|story_bronze|zhaoyun-set/bronze-biography_2026-10-18_19-36-53_UTC+08/赵云-黑铜传记*.png
zhaoyun|story_silver|zhaoyun-set/silver_rescue_2026-10-18_19-38-48_UTC+08/赵云-白银传记*.png
zhaoyun|story_gold|zhaoyun-set/story-hanshui-rescue_2026-10-18_19-57-59_UTC+08/赵云-银金传记*.png
machao|bronze|machao-set/bronze_pair_2026-10-18_19-41-20_UTC+08/马超-青铜*.png
machao|silver|machao-set/silver-newpose_2026-10-18_20-00-38_UTC+08/马超-白银*.png
machao|gold|machao-set/gold-cloak-local_2026-10-18_20-26-20_UTC+08/马超-黄金*.png
machao|story_bronze|machao-set/bronze_pair_2026-10-18_19-41-20_UTC+08/马超-传记*.png
machao|story_silver|machao-set/silver-night_2026-10-18_19-51-38_UTC+08/马超-铜银传记*.png
machao|story_gold|machao-set/story-lihui_2026-10-18_20-21-02_UTC+08/马超-银金传记*.png
huangzhong|blackiron|huangzhong-set/blackiron_repose_2026-10-18_19-53-53_UTC+08/黄忠-黑铁-v3*.png
huangzhong|bronze|huangzhong-set/bronze_pair_2026-10-18_20-02-06_UTC+08/黄忠-青铜-v1*.png
huangzhong|silver|huangzhong-set/silver_pair_2026-10-18_20-17-05_UTC+08/黄忠-白银-v1*.png
huangzhong|gold|huangzhong-set/gold-pair_2026-10-18_20-13-24_UTC+08/黄忠-黄金*.png
huangzhong|story_bronze|huangzhong-set/bronze_bio_arrowfix_2026-10-18_20-12-53_UTC+08/黄忠-青铜传记-v2*.png
huangzhong|story_silver|huangzhong-set/silver_bio_linefix_2026-10-18_20-23-23_UTC+08/黄忠-白银传记-v2*.png
huangzhong|story_gold|huangzhong-set/gold-pair_2026-10-18_20-13-24_UTC+08/黄忠-银金传记*.png
zhugeliang|blackiron|zhugeliang-set/blackiron-first_2026-10-18_19-53-24_UTC+08/诸葛亮-黑铁*.png
zhugeliang|bronze|zhugeliang-set/bronze_pair_2026-10-18_20-04-00_UTC+08/诸葛亮-青铜*.png
zhugeliang|silver|zhugeliang-set/silver_flagfix_2026-10-18_20-23-00_UTC+08/诸葛亮-白银*.png
zhugeliang|gold|zhugeliang-set/gold_pair_2026-10-18_20-14-00_UTC+08/诸葛亮-黄金*.png
zhugeliang|story_bronze|zhugeliang-set/bronze_pair_2026-10-18_20-04-00_UTC+08/诸葛亮-传记*.png
zhugeliang|story_silver|zhugeliang-set/silver_pair_2026-10-18_20-10-00_UTC+08/诸葛亮-传记*.png
zhugeliang|story_gold|zhugeliang-set/gold_pair_2026-10-18_20-14-00_UTC+08/诸葛亮-传记*.png
pangtong|blackiron|pangtong-set/blackiron-first_2026-10-18_19-58-00_UTC+08/庞统-黑铁*.png
pangtong|bronze|pangtong-set/bronze_pair_2026-10-18_20-19-00_UTC+08/庞统-青铜*.png
pangtong|silver|pangtong-set/silver-pair_2026-10-18_20-24-02_UTC+08/庞统-白银*.png
pangtong|gold|pangtong-set/gold_pair_2026-10-18_20-27-00_UTC+08/庞统-黄金*.png
pangtong|story_bronze|pangtong-set/bronze_pair_2026-10-18_20-19-00_UTC+08/庞统-传记*.png
pangtong|story_silver|pangtong-set/silver-pair_2026-10-18_20-24-02_UTC+08/庞统-铜银传记*.png
pangtong|story_gold|pangtong-set/gold_pair_2026-10-18_20-27-00_UTC+08/庞统-传记*.png'''
for row in rows.splitlines():
 h,a,g=row.split('|');matches=list(root.glob(g));assert len(matches)==1,(g,matches);p=matches[0];w,he=Image.open(p).size
 v={'hero':h,'asset':a,'path':str(p),'width':w,'height':he,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'qa_status':'candidate_passed','residual_or_scope':'Content and native crops reviewed; final frame coverage and user approval separate. See INDEPENDENT_QA.md for residuals.'}
 if (h,a)==('machao','story_gold'): v['qa_status']='structure_passed_material_pending';v['residual_or_scope']='Low-contrast random pale points on hanging red cloth x1150–1290,y690–850; local correction pending.'
 if (h,a)==('pangtong','story_silver'):v['qa_status']='structure_passed_foreground_decision_pending';v['residual_or_scope']='Foreground petitioner occupies lower-right ~1/3 and is soft; root decision pending.'
 old=current.get((h,a))
 if old and old['path']!=str(p):
  old=old.copy();old['superseded_by']=str(p);d['superseded_candidates'].append(old)
 current[(h,a)]=v
order=['blackiron','bronze','silver','gold','story_bronze','story_silver','story_gold']
d['candidates']=sorted(current.values(),key=lambda x:(x['hero'],order.index(x['asset'])))
d['updated_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat();d['scope']='Independent artwork and native-crop QA only. Candidate status is not user final approval, final-frame approval, or a claim of new higher-resolution detail.'
out.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n');print('current:',len(d['candidates']),'superseded:',len(d['superseded_candidates']))
