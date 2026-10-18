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
 im=Image.fromarray(a);mask=Image.new('L',im.size);d=ImageDraw.Draw(mask);pts=[(66*S,0),(277*S,0),(277*S,76*S),(0,76*S)];d.polygon(pts,fill=255)
 # A restrained embossed-metal texture from the approved frame itself.
 tx=card.crop((390,1450,667,1510)).convert('RGB').resize(im.size,Image.Resampling.LANCZOS)
 im=Image.blend(im.convert('RGB'),tx,.14).convert('RGBA');im.putalpha(mask);d=ImageDraw.Draw(im)
 def p(q,fill):d.polygon([(int(x*S),int(y*S)) for x,y in q],fill=fill)
 def l(q,fill,n=1):d.line([(int(x*S),int(y*S)) for x,y in q],fill=fill,width=int(n*S),joint='curve')
 # Real geometry: bright chamfer, a recessed inset face, and extruded lower edge.
 p([(66,0),(277,0),(277,8),(70,8),(17,68),(0,76)],'#fff0ad')
 p([(70,8),(277,8),(271,12),(73,12),(29,63),(17,68)],'#e7ac3c')
 p([(0,76),(277,76),(277,68),(18,68)],'#6d3408')
 p([(18,68),(277,68),(271,62),(29,62)],'#c9821b')
 p([(277,0),(277,76),(270,68),(270,8)],'#9a5210')
 l([(66,1),(276,1)],'#fff9d6',1)
 l([(4,74),(274,74)],'#e9b74e',1)
 l([(71,10),(270,10)],'#f8dc8f',1)
 l([(29,63),(269,63)],'#f6cd6a',1)
 # Triangular sloping shoulder like the reference's diagonal gold facet.
 p([(65,15),(24,62),(89,62)],'#f7d576')
 p([(65,15),(71,13),(96,62),(89,62)],'#fff1b8')
 p([(24,62),(89,62),(87,58),(30,58)],'#e8bc58')
 l([(68,15),(88,55)],'#c28a2d',1)
 # Small specular breaks instead of an even outlined rectangle.
 l([(74,2),(116,2)],'#ffffff',1)
 l([(27,69),(97,69)],'#ffe9a3',1)
 return im
P=plate()
def compose(skills):
 ui=Image.new('RGBA',(W*S,H*S))
 for i,row in enumerate(skills):
  x,y=665,1018+i*91
  # 3px depth below face, inside the same compact footprint.
  shadow=Image.new('RGBA',P.size);shadow.putalpha(P.getchannel('A').point(lambda v:int(v*.8)))
  ui.alpha_composite(shadow,(x*S,(y+3)*S));ui.alpha_composite(P,(x*S,y*S))
  d=ImageDraw.Draw(ui);name,level=row['name'],row['level'];suffix=f'+{level}'
  size=43 if len(name)<=2 else 36 if len(name)==3 else 30
  f=ImageFont.truetype(FONT,size*S);lf=ImageFont.truetype(FONT,(size+1)*S)
  nw=d.textlength(name,font=f);lw=d.textlength(suffix,font=lf);gap=5*S
  right=(x+258)*S;start=right-nw-gap-lw
  # White lettering, dark keyline and slight lower shadow, like reference.
  for text,xx,ff in [(name,start,f),(suffix,start+nw+gap,lf)]:
   yy=(y+36)*S
   d.text((xx,yy+2*S),text,font=ff,anchor='lm',fill='#52310b',stroke_width=2*S,stroke_fill='#52310b')
   d.text((xx,yy),text,font=ff,anchor='lm',fill='#fffdf3',stroke_width=int(1.35*S),stroke_fill='#4c3719')
 return ui.resize((W,H),Image.Resampling.LANCZOS)
skills=[{'name':n,'level':2} for n in ['蓄势','斩将','武圣']]
ui=compose(skills);ui.save(D/'passive-overlay.png');out=Image.alpha_composite(card,ui);out.save(D/'关羽-黄金-被动技能上卡预览.png');out.resize((480,720),Image.Resampling.LANCZOS).save(D/'review-480.png')
test=compose([{'name':'蓄','level':2},{'name':'青龙蓄势','level':12},{'name':'武圣','level':12}]);Image.alpha_composite(card,test).crop((655,1008,950,1295)).save(D/'layout-stress-test.png')
ref=Image.open('user-images-1018/image(20261018-044056).png').crop((455,635,650,826)).resize((390,382));ours=out.crop((655,1008,950,1295)).resize((390,382));check=Image.new('RGB',(800,410),'#202020');check.paste(ref,(0,28));check.paste(ours,(410,28));d=ImageDraw.Draw(check);d.text((5,7),'REFERENCE',fill='white');d.text((415,7),'NEW METAL + LEVEL',fill='white');check.save(D/'reference-comparison.png')
(D/'config.json').write_text(json.dumps({'status':'visual mockup only; names and levels not final','skills':skills,'supports':'1–4 character name, separate numeric level, variable skill count','bounds':[665,1018,277,76],'vertical_step':91,'rejected_v1':'../passive_tags_20261018_170340_UTC+08/','base':str(BASE),'material':'layered bevels with restrained approved-frame gold texture'},ensure_ascii=False,indent=2))
(D/'README.txt').write_text('v2 材质与等级占位预览\n白字暗描边，独立技能名与等级后缀，三行仅示例。\n可配置技能列表、1–4字名称及+2/+12；已输出排版压力检查图。\n金属板包含高光斜面、内凹面、下沿厚度与框体纹理。原画与原框文件未改动。\n旧 v1 已保留并在配置中标记拒绝版本。\n')
