from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,hashlib
R=Path(__file__).resolve().parents[1];D=R/'QA'
boxes={
'card01':{'face':(230,90,470,300),'hands':(210,470,530,660)},
'card02':{'face':(260,180,510,420),'hands':(610,650,900,840)},
'card03':{'face':(240,150,450,340),'grip':(40,300,210,470),'palm':(650,370,830,540),'shaft':(20,0,170,1450)},
'card04':{'face':(290,250,540,450),'grip':(40,260,210,460),'reins':(370,580,560,770),'horse':(630,700,900,1120)},
'bio01':{'face':(360,120,650,370),'hands':(430,580,760,830)},
'bio02':{'face':(820,130,1040,370),'baton':(890,460,1060,720),'palm':(300,470,510,620)},
'bio03':{'face':(420,100,640,330),'handoff':(720,500,970,790)}
}
for asset,regions in boxes.items():
 im=Image.open(R/'raw'/f'{asset}.png')
 for k,b in regions.items():im.crop(b).save(D/f'{asset}-{k}-native100.png')
for t in ['iron','bronze','silver','gold']:
 im=Image.open(R/f'于禁-卡{["iron","bronze","silver","gold"].index(t)+1}-{t}.png')
 im.crop((850,1030,1120,1390)).save(D/f'{t}-UI-native100.png')
notes={'status':'Self-reviewed candidate, user approval pending','passes':['Seven outputs individually viewed','Same rectangular face, helmet and short beard across set','Four poses distinct: roster / rear-quarter survey / open-palm fortification / mounted command','Silver spear continuous rigid straight axis, single natural grip, spearhead naturally reaches top edge','Gold reins and command baton separated in different hands','Biography3 messenger tablet handoff readable','No frame on three landscape biographies','UI texts deterministic independent layer, two-character single-effect proposed passives','魏 blue collection badge fixed all four tiers','Compact passive plates bottom anchored; title/rank centered by actual font bbox','All uncovered art pixels identical to original after composition'],'caveats':['Rhinoceros visual and flags bearing rhino emblem are original symbolic adaptation, not novel fact','Blackiron hint is a visible rock rhino head rather than horn only; parent accepted this first-stage motif','Creature body is mostly mist-obscured intentionally','Gold passive plates overlap small section of horse muzzle flank but never hero face or grip','Cao Cao in biography scenes is supporting illustrative design, not reuse of another character production asset'],'skills':[{'name':'整列','effect':'自身驻守时受到的伤害降低'},{'name':'镇足','effect':'自身受到的击退距离减少'},{'name':'坚壁','effect':'驻守给予的减伤幅度提高'}],'active_draft':{'name':'驻守','effect':'驻守期间降低附近少量友军受到的伤害，移动结束'},'failures':[{'file':'failures/card01-too-realistic.png','reason':'first render too photographic and helmet ponytail; repaired to clean animated style and tucked hair'}]}
(D/'self-inspection.json').write_text(json.dumps(notes,ensure_ascii=False,indent=2))
(R/'failures/failure-records.json').write_text(json.dumps(notes['failures'],ensure_ascii=False,indent=2))
files=[p for p in R.rglob('*') if p.is_file()]
(R/'checksums.json').write_text(json.dumps({str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files},ensure_ascii=False,indent=2))
