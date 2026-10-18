from PIL import Image,ImageDraw,ImageFont,ImageEnhance,ImageFilter,ImageChops
from pathlib import Path
import json,numpy as np
D=Path(__file__).parent;BASE=D.parent/'qualitylocalized_20261018_165240_UTC+08/04-黄金·护行拖刀.png';card=Image.open(BASE).convert('RGBA');S=3;W,H=card.size
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
def plate():
 w,h=277,76
 a=np.zeros((h*S,w*S,4),dtype=np.uint8);rng=np.random.default_rng(9)
 stops=[(0,(255,246,176)),(.09,(247,197,73)),(.22,(255,214,101)),(.48,(235,161,32)),(.65,(242,174,43)),(.86,(203,121,13)),(1,(122,56,5))]
 for y in range(h*S):
  t=y/(h*S-1)
  for (p,c),(q,e) in zip(stops,stops[1:]):
   if p<=t<=q:
    u=(t-p)/(q-p);color=np.array(c)*(1-u)+np.array(e)*u;break
  for x in range(w*S):
   sheen=11*np.exp(-((x/w/S-.28)/.24)**2)-7*(x/w/S)
   a[y,x,:3]=np.clip(color+sheen+rng.normal(0,1.7),0,255);a[y,x,3]=255
 im=Image.fromarray(a)
 tx=card.crop((390,1450,667,1510)).convert('RGB').resize(im.size,Image.Resampling.LANCZOS)
 im=Image.blend(im.convert('RGB'),tx,.12).convert('RGBA');d=ImageDraw.Draw(im)
 def p(q,fill):d.polygon([(int(x*S),int(y*S)) for x,y in q],fill=fill)
 def l(q,fill,n=1):d.line([(int(x*S),int(y*S)) for x,y in q],fill=fill,width=int(n*S),joint='curve')
 # Clean rectangular metal strip; no triangle, arrow, or wedge ornaments.
 p([(0,0),(277,0),(271,6),(6,6)],'#fff0ad')
 p([(0,0),(6,6),(6,69),(0,76)],'#e4ba61')
 p([(0,76),(277,76),(271,69),(6,69)],'#71400c')
 p([(277,0),(277,76),(271,69),(271,6)],'#9a621a')
 l([(1,1),(276,1)],'#fff9d6',1)
 l([(6,7),(270,7)],'#c38a25',1)
 l([(6,68),(270,68)],'#f9d581',1)
 l([(1,74),(276,74)],'#deb057',1)
 l([(6,8),(6,67)],'#f4d581',1)
 l([(270,8),(270,67)],'#89540f',1)
 # Broken specular reflections, restrained at thumbnail size.
 l([(26,2),(88,2)],'#fffef0',1)
 l([(185,2),(235,2)],'#fffce0',1)
 l([(22,69),(68,69)],'#ffeab6',1)
 return im
P=plate()
def color_plate(source, material):
 if material=='gold': return source.copy()
 aa=np.array(source);lum=(aa[:,:,:3].astype(float)@np.array([.299,.587,.114]))/255
 palettes={'iron':[(22,29,35),(81,94,103),(211,224,229)],'bronze':[(46,23,14),(153,87,48),(255,219,169)],'silver':[(39,48,57),(143,161,174),(246,252,255)]}
 lo,mi,hi=[np.array(c) for c in palettes[material]]
 t=np.clip(lum,0,1);low=t<.56
 rgb=np.where(low[:,:,None],lo+(mi-lo)*(t/.56)[:,:,None],mi+(hi-mi)*((t-.56)/.44)[:,:,None])
 aa[:,:,:3]=np.clip(rgb,0,255).astype('uint8');return Image.fromarray(aa)
def compose(skills, material='gold'):
 P=color_plate(globals()['P'],material)
 ui=Image.new('RGBA',(W*S,H*S))
 for i,row in enumerate(skills):
  x,y=665,1018+(3-len(skills)+i)*91
  # 3px depth below face, inside the same compact footprint.
  shadow=Image.new('RGBA',P.size);shadow.putalpha(P.getchannel('A').point(lambda v:int(v*.8)))
  ui.alpha_composite(shadow,(x*S,(y+3)*S));ui.alpha_composite(P,(x*S,y*S))
  d=ImageDraw.Draw(ui);name,level=row['name'],row['level'];suffix=f'+{level}'
  size=43 if len(name)<=2 else 36 if len(name)==3 else 30
  f=ImageFont.truetype(FONT,size*S);lf=ImageFont.truetype(FONT,(size+1)*S)
  nw=d.textlength(name,font=f);lw=d.textlength(suffix,font=lf);gap=5*S
  start=(x+138.5)*S-(nw+gap+lw)/2
  # White lettering, dark keyline and slight lower shadow, like reference.
  for text,xx,ff in [(name,start,f),(suffix,start+nw+gap,lf)]:
   yy=(y+36)*S
   d.text((xx,yy+2*S),text,font=ff,anchor='lm',fill='#52310b',stroke_width=2*S,stroke_fill=('#192027' if material in ['iron','silver'] else '#52310b'))
   d.text((xx,yy),text,font=ff,anchor='lm',fill='#fffdf3',stroke_width=int(1.35*S),stroke_fill=('#202930' if material in ['iron','silver'] else '#4c3719'))
 return ui.resize((W,H),Image.Resampling.LANCZOS)

def complete_ui(ui, title='真·关羽', country='蜀', level=1, stage='真'):
 out=ui.resize((W*S,H*S),Image.Resampling.LANCZOS);d=ImageDraw.Draw(out)
 serif='/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc'
 def ellipse(box,fill,outline=None,width=1):d.ellipse(tuple(int(v*S) for v in box),fill=fill,outline=outline,width=width*S)
 def polygon(points,fill):d.polygon([(int(x*S),int(y*S)) for x,y in points],fill=fill)
 def text(pos,value,size,font=serif,fill='#fff7dd',stroke='#141410',sw=2):
  ff=ImageFont.truetype(font,size*S);x,y=pos
  d.text((x*S,(y+3)*S),value,font=ff,anchor='mm',fill='#0b0c0b',stroke_width=(sw+1)*S,stroke_fill='#0b0c0b')
  d.text((x*S,y*S),value,font=ff,anchor='mm',fill=fill,stroke_width=sw*S,stroke_fill=stroke)
 # Country medallion sits inside the existing upper-left socket.
 ellipse((109,89,194,174),'#10391a','#0b170b',1)
 for rr in range(41,0,-1):
  t=1-rr/41;c=(int(22+25*t),int(68+45*t),int(26+12*t));ellipse((151.5-rr,131.5-rr,151.5+rr,131.5+rr),c)
 text((151,130),country,61,sw=2)
 # Clean original-style title; never copy screenshot chat/rank text.
 text((635,86),title,48,fill='#fffdf3',sw=2)
 # Level label has an independent value field.
 text((914,100),'LV',29,font=serif,fill='#f6efcc',sw=1)
 text((914,140),str(level),53,font=serif,fill='#fff8dd',sw=2)
 # Advancement example inside lower-left existing medallion.
 box=(83,1318,219,1454);mask=Image.new('L',(136*S,136*S));ImageDraw.Draw(mask).ellipse((0,0,136*S-1,136*S-1),fill=255)
 grad=Image.new('RGBA',mask.size);gd=ImageDraw.Draw(grad)
 for yy in range(136*S):
  t=yy/(136*S);a=(255,160,26) if t<.45 else (183,45,40);b=(195,42,41) if t<.45 else (65,22,139);v=t/.45 if t<.45 else (t-.45)/.55;c=tuple(int(x+(y-x)*v) for x,y in zip(a,b));gd.line((0,yy,136*S,yy),fill=(*c,255))
 grad.putalpha(mask);out.alpha_composite(grad,(83*S,1318*S));d=ImageDraw.Draw(out)
 ellipse(box,None,'#f5df9b',2);text((151,1387),stage,91,fill='#fff4d5',stroke='#17140f',sw=4)
 # Example troop type: compact white polearms, independent of illustration.
 ellipse((838,1361,956,1479),'#080b0c','#af9560',1)
 polygon([(895,1376),(903,1397),(901,1439),(889,1439),(887,1397)],'#fff6ce')
 polygon([(891,1437),(900,1437),(900,1459),(891,1459)],'#f9ebbd')
 polygon([(865,1402),(874,1417),(874,1438),(884,1443),(884,1454),(871,1448),(863,1439)],'#fff9dc')
 polygon([(925,1402),(917,1417),(917,1438),(907,1443),(907,1454),(920,1448),(928,1439)],'#fff9dc')
 polygon([(878,1452),(914,1452),(909,1460),(883,1460)],'#e9d69a')
 return out.resize((W,H),Image.Resampling.LANCZOS)

MATERIALS={'iron':[{'name':'蓄势','level':1}],'bronze':[{'name':'蓄势','level':1}],'silver':[{'name':'蓄势','level':2},{'name':'斩将','level':2}],'gold':[{'name':'蓄势','level':2},{'name':'斩将','level':2},{'name':'武圣','level':2}]}
if __name__=='__main__':
 import argparse
 ap=argparse.ArgumentParser();ap.add_argument('--sources');args=ap.parse_args()
 sources=json.loads(Path(args.sources).read_text()) if args.sources else {}
 config={'status':'visual presentation only; skill names, levels, and counts are not final mechanics','materials':{},'source_cards_preserved':True,'display_fields':{'country':'蜀','title':'真·关羽','level':1,'advancement':'真','troop_icon':'example polearm infantry; not inferred from mounted art'},'note':'All added fields are independent display placeholders, not a mapping from rarity to advancement.'}
 for material,skills in MATERIALS.items():
  ui=complete_ui(compose(skills,material));ui.save(D/f'{material}-overlay.png')
  config['materials'][material]={'skills':skills,'overlay':f'{material}-overlay.png','source':sources.get(material)}
  if material in sources:
   im=Image.open(sources[material]).convert('RGBA')
   if im.size!=(W,H):raise ValueError(f'{material} unexpected canvas {im.size}')
   out=Image.alpha_composite(im,ui);name={'iron':'01-黑铁','bronze':'02-青铜','silver':'03-白银','gold':'04-黄金'}[material]+'-完整UI示意.png'
   out.save(D/name);out.resize((480,720),Image.Resampling.LANCZOS).save(D/f'{material}-480.png')
 (D/'config.json').write_text(json.dumps(config,ensure_ascii=False,indent=2))
