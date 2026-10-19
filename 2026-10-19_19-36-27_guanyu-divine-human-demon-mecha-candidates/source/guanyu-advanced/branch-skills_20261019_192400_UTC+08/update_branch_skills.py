from pathlib import Path
import json,importlib.util,numpy as np,hashlib
from PIL import Image
root=Path('/workspace/scratch/3f82ff2b3f81/guanyu-advanced'); ui=root/'ui-calligraphy_20261019_191150_UTC+08'; out=root/'branch-skills_20261019_192400_UTC+08';out.mkdir(exist_ok=True)
s=importlib.util.spec_from_file_location('r',ui/'render.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
records=[]
for key,cp,names in [('mecha',ui/'mecha/guanyu-piloted-dragon-mecha-5star.json',['重甲','蓄能','反制']),('demon',ui/'demon-safe_20261019_191935_UTC+08/config.json',['嗜血','戮魂','追命'])]:
 c=json.loads(cp.read_text());old=Path(c['outdir'])/f"{c['hero']}-{c['branch_id']}-5star.png"
 c={k:c[k] for k in ['hero','name','branch','branch_id','tier','source']};c.update(outdir=str(out/key),skills=[{'name':n,'level':1} for n in names],troop_class='长枪兵',advancement_placeholder=True,skill_values_status='draft_not_balanced')
 (out/key).mkdir(exist_ok=True);(out/key/'config.json').write_text(json.dumps(c,ensure_ascii=False,indent=2));r=m.compose(c)
 a=np.array(Image.open(old));b=np.array(Image.open(r['output']));d=np.any(a!=b,axis=2);allowed=np.zeros(d.shape,bool);allowed[1050:1350,820:1110]=1
 assert not (d&~allowed).any(),np.where(d&~allowed)
 r['outside_passive_name_region_changes']=int((d&~allowed).sum());r['previous_card']=str(old);records.append(r)
(out/'manifest.json').write_text(json.dumps(records,ensure_ascii=False,indent=2))
(out/'技能说明草案.md').write_text('''# 2026-10-19 19:24:00 UTC+08 分支技能修订\n\n状态：候选设计，不含已定数值。只修改三条被动UI名称，插画、框、其他UI不动。卡面+1沿用原展示占位，并非平衡值。\n\n## 五星机甲关羽：防御与反击\n主动「青龙壁垒」：展开护盾承接攻击，随后挥动巨型青龙偃月刀反击。具体触发时机与数值待定。\n- 重甲：降低自身受到的伤害。\n- 蓄能：承受攻击积累能量，增强下一次主动反击。\n- 反制：受到攻击后触发反击。触发冷却待定。\n\n## 五星魔关羽：极端杀伐\n主动「修罗戮斩」：三头六臂发动猛烈连续杀招。\n- 嗜血：造成伤害时回复自身生命。\n- 戮魂：击败敌人后提高自身攻击。\n- 追命：对低生命敌人造成更高伤害。\n\n## 五星神关羽：团队辅助（待神卡任务制作）\n主动「义薄云天」：庇护友军，具体群体增益待确定。\n候选被动：义护（保护友军）、同心（增强团队协同）、佑众（治疗或生存支持，单条最终只保留一个关键效果）。\n\n各分支不再强制相同残血收割体系；仍保持青龙身份语言。\n''')
print(json.dumps(records,ensure_ascii=False))
