from pathlib import Path
import json
out=Path('output/高阶完整交付/2026-10-19_14-41-43/说明文档')
L=json.load(open('liubei-set/advanced_20261019_135505_UTC+08/skills.json'));Z=json.load(open('zhangfei-set/advanced_20261019_135505_UTC+08/skills.json'))['branches']
G={
 'traditional':{'active':'青龙断江：积蓄后一次宽弧重斩，对低血目标额外伤害。','growth':'强化蓄势层数收益与斩击范围，不能无限斩杀首领。','passives':[('蓄势','交战递增武力，上限5层。'),('武勇','普攻命中低血敌，缩短下一次蓄势间隔。'),('断流','伤害随目标已损生命比例增长，上限约30%。')]},
 'divine':{'active':'关圣镇邪：短时蓄力后龙印斩落，给予自己护佑屏障。','growth':'延长屏障并强化同一标记机制。','passives':[('香火','交战积累武力。'),('镇邪','攻击标记一个敌人，降低其输出。'),('神裁','被标记低血敌受到终结加伤。')]},
 'demonic':{'active':'冥龙索命：压低身姿凶猛横斩，低血敌受到额外伤害。','growth':'扩大斩击并延长受击蓄势窗口，不无限续命。','passives':[('怨煞','受击积累武力，有上限。'),('索命','对低血敌加伤。'),('不屈','首次致命伤触发短暂保命，受长冷却限制。')]},
 'mecha':{'active':'龙核超载：机械关节锁稳后释放一记能源长刃。','growth':'增大刃幅，返还部分命中充能，返还有上限。','passives':[('蓄能','交战充能。'),('锁定','连续攻击同一敌人提高穿透，有上限。'),('终式','低血目标受到能源刃额外伤害。')]}}
B={'traditional':'传承','divine':'神','demonic':'魔','mecha':'机甲'}
lines=['# 刘关张高阶24形态技能方案','', '状态：全部为设计候选，未获用户最终批准，尚未完成游戏实装与数值平衡验证。','五星固定三条两字被动；六星默认沿用同分支三条并强化，是制作默认，并非用户额外锁定六星数量。卡面+1/+2是预览等级，不代表已验证的最终数值。','所有VFX和cut-in均为独立静态源素材，不表示已实现动画、粒子系统或技能时间轴。','']
for hero in ['刘备','关羽','张飞']:
 lines+=['# '+hero,'']
 for branch,bn in B.items():
  for tier in [5,6]:
   lines+=['## '+f'{hero}·{bn}·{tier}星','']
   if hero=='刘备':
    x=L[branch];active=x[f'active{tier}'];passives=[(p['name'],p['effect']) for p in x['passives']];growth=x['active6']+' 被动默认同三条强化数值；具体幅度尚未定稿。'
   elif hero=='关羽':
    x=G[branch];active=x['active']+(' 六星强化：'+x['growth'] if tier==6 else '');passives=x['passives'];growth=x['growth']+' 三被动沿用同分支机制，具体六星数值待验证。'
   else:
    x=Z[{'traditional':'legacy','demonic':'demon'}.get(branch,branch)];active=x['active']['name']+'：'+x['active']['effect'];passives=x['passives'];growth=x['active']['effect'].split('六星',1)[1] if '六星' in x['active']['effect'] else '同分支强化';growth='六星'+growth+' 三被动仍沿用同分支机制，数值待验证。'
   lines+=['主动：'+active,'','三条被动：']+[f'- {name}：{effect}' for name,effect in passives]+['','五→六成长：'+growth,'']
 lines+=['战斗边界：'+({'刘备':'治疗、护盾、清除和增益均有次数、持续时间或上限约束；魔化不代表无限复活。','关羽':'蓄势和终结能力有层数及伤害上限，不将首领描述为可无限斩杀。','张飞':'百分比伤害按目标当前生命值而非最大生命值；首领伤害有武力倍率上限，抗控规则待平衡验证。'}[hero]),'']
lines+=['# 文化依据与原创边界','']
for f in ['刘备-文化来源与原创边界.md','关羽-技能与文化来源.md','张飞-文化来源与原创边界.md']:
 text=(out/f).read_text()
 if f.startswith('关羽'):text=text.split('## 技能设计')[0]
 lines+=[text,'']
lines+=['# 文件与使用说明','每形态最终下载内容为装框卡、独立传记、透明头像、透明技能立绘、透明独立VFX五项。','无框插画另行作为源文件保存，未重复计入最终120项。','精确像素尺寸、文件字节数、SHA256、LibraryID和包内位置以最终总清单为准。']
(out/'刘关张-24形态-完整技能与文化方案.md').write_text('\n'.join(lines)+'\n')
print('sections',sum(l.startswith('## ') and '星' in l for l in lines))
