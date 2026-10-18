from PIL import Image,ImageDraw,ImageFont,ImageFilter
from pathlib import Path
import math,json,hashlib
D=Path(__file__).parent; base= D.parent/'qualitylocalized_20261018_165240_UTC+08/04-黄金·护行拖刀.png'
S=3; W,H=1024,1536
ui=Image.new('RGBA',(W*S,H*S)); d=ImageDraw.Draw(ui)
def poly(p,fill,outline=None,width=1):
 p=[(round(x*S),round(y*S)) for x,y in p];d.polygon(p,fill=fill)
 if outline:d.line(p+[p[0]],fill=outline,width=round(width*S),joint='curve')
def line(p,fill,width=1):d.line([(int(x*S),int(y*S)) for x,y in p],fill=fill,width=int(width*S),joint='curve')
def ellipse(box,fill,outline=None,width=1):d.ellipse(tuple(int(v*S) for v in box),fill=fill,outline=outline,width=int(width*S))
def arc(box,start,end,fill,width=1):d.arc(tuple(int(v*S) for v in box),start,end,fill=fill,width=int(width*S))
def curve(pts,n=35):
 p0,p1,p2,p3=pts;return [((1-t)**3*p0[0]+3*(1-t)**2*t*p1[0]+3*(1-t)*t*t*p2[0]+t**3*p3[0],(1-t)**3*p0[1]+3*(1-t)**2*t*p1[1]+3*(1-t)*t*t*p2[1]+t**3*p3[1]) for t in [i/n for i in range(n+1)]]
# Independent bottom-center passive-skill plaque. Canvas outside it stays transparent.
poly([(386,1324),(638,1324),(663,1342),(695,1368),(663,1394),(638,1410),(386,1410),(352,1367)],'#31250fff','#d7ac51ff',2)
poly([(389,1329),(636,1329),(660,1347),(684,1368),(660,1389),(636,1405),(389,1405),(358,1367)],'#0a241eff','#8c743bff',1)
poly([(407,1334),(633,1334),(672,1368),(633,1400),(407,1400)],'#0b3028f8')
# Fine geometric leaf/dragon-scale trim: ornament kept away from name.
for x in range(488,628,20):
 line([(x,1338),(x+7,1334),(x+14,1338)],'#4a674eff',1)
 line([(x,1396),(x+7,1400),(x+14,1396)],'#4a674eff',1)
line([(436,1331),(632,1331),(656,1350)],'#f2d591ff',1)
line([(435,1403),(632,1403),(655,1384)],'#bb9250ff',1)
poly([(649,1368),(659,1359),(668,1368),(659,1377)],'#257d55ff','#d8b663ff',1)
poly([(654,1368),(659,1363),(664,1368),(659,1373)],'#82d69aff')
# Gold-rimmed emerald talisman with a jade crescent glaive.
ellipse((346,1317,450,1421),'#131b15ff','#836120ff',2)
ellipse((350,1321,446,1417),'#bf8c32ff','#ffe9a5ff',2)
ellipse((355,1326,441,1412),'#123c2bff','#533a18ff',2)
ellipse((359,1330,437,1408),'#08251eff','#d3b76aff',1)
arc((364,1335,432,1403),25,155,'#53a16aff',2);arc((364,1335,432,1403),198,325,'#74ba7eff',2)
# Curl motif, echoing a dragon's tail.
line(curve([(378,1392),(348,1372),(396,1341),(410,1352)]),'#286744ff',3)
line(curve([(376,1388),(365,1373),(382,1358),(389,1361)]),'#65985aff',1)
# Shaft, wrapping, and blade. Readable even as a small game icon.
line([(377,1395),(410,1349)],'#06170fff',7);line([(377,1395),(410,1349)],'#e5b95fff',4)
line([(379,1393),(411,1349)],'#ffebadff',1)
for y in range(1373,1387,4):
 x=377+(1395-y)*33/46
 line([(x-2,y-2),(x+3,y+1)],'#315b3eff',2)
blade=curve([(405,1353),(387,1347),(391,1332),(424,1338)])+curve([(424,1338),(416,1343),(425,1358),(402,1370)])+[(406,1359)]
poly(blade,'#9cdb9dff','#e7cf79ff',1.3)
line(curve([(398,1344),(411,1338),(417,1348),(406,1363)]),'#27734bff',2)
poly([(401,1358),(407,1351),(412,1354),(407,1362)],'#dfae48ff','#fff0a8ff',1)
ellipse((397,1356,401,1360),'#e9fcbaff')
# Compact tassel.
line(curve([(391,1375),(401,1381),(394,1387),(403,1388)]),'#88b469ff',2)
# Type uses a proper CJK font; no generated lettering.
font='/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc'
sans='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
def text(pos,s,size,color,font):d.text((int(pos[0]*S),int(pos[1]*S)),s,font=ImageFont.truetype(font,int(size*S)),fill=color,anchor='lt')
text((468,1337),'被 动',13,'#b5c7a5ff',sans)
text((467,1360),'蓄 势',34,'#061b15ff',font)
text((467,1358),'蓄 势',34,'#f8e6b4ff',font)
# A restrained shadow is also part of the UI overlay.
mask=ui.getchannel('A'); shadow=Image.new('RGBA',ui.size,(0,0,0,0));shadow.putalpha(mask.filter(ImageFilter.GaussianBlur(4*S)).point(lambda a:int(a*.7)))
out=Image.alpha_composite(shadow,ui).resize((W,H),Image.Resampling.LANCZOS)
out.save(D/'passive-overlay.png')
im=Image.open(base).convert('RGBA');Image.alpha_composite(im,out).save(D/'关羽-黄金-被动技能上卡预览.png')
config={'status':'UI mockup only; skill name is example, not final gameplay data','skill_name':'蓄势','type':'被动','canvas':[W,H],'overlay':'passive-overlay.png','base':str(base),'base_sha256':hashlib.sha256(base.read_bytes()).hexdigest(),'placement':'bottom center; independent overlay, original base unchanged'}
(D/'config.json').write_text(json.dumps(config,ensure_ascii=False,indent=2))
(D/'README.txt').write_text('被动技能上卡示意\n示例名：蓄势。仅作版式预览，未定义最终技能数值。\n独立透明 UI 层；未改动原卡面或框体。\ncompose.py 可重复生成透明图层与合成预览。\n')
print(D.resolve())
