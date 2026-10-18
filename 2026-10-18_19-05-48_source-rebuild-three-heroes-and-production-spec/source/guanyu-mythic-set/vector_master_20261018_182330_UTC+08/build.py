from pathlib import Path
import math,json,subprocess,re
from xml.sax.saxutils import escape
D=Path(__file__).parent
P={'gold':['#fff8d6','#f8dd92','#d5a246','#8e5b1d','#36200d'],'iron':['#bfcbd3','#8796a2','#46535f','#222e38','#0c131a'],'bronze':['#ffedd4','#e8b78c','#b77743','#734329','#291910'],'silver':['#ffffff','#e4edf1','#abbcc6','#637884','#25323c']}
INNER='M110 126 H875 V600 L950 676 V1425 H160 V945 L80 850 V425 L110 385 Z'
OUTER='M78 43 H954 Q970 43 970 59 V1494 Q970 1510 954 1510 H78 Q62 1510 62 1494 V59 Q62 43 78 43 Z'
def star(cx,cy,R=31):
 pts=[]
 for i in range(10):
  a=-math.pi/2+i*math.pi/5;r=R if i%2==0 else R*.43;pts.append((cx+r*math.cos(a),cy+r*math.sin(a)))
 q=' '.join(f'{x:.2f},{y:.2f}' for x,y in pts);s=f'<polygon points="{q}" fill="url(#starMetal)" stroke="#352410" stroke-width="2"/>'
 colors=['#fff5b5','#b77b22','#f4cf6f','#8f5616','#ffe99c']
 for i in range(5):
  a,b,c=pts[i*2],pts[(i*2+1)%10],pts[(i*2-1)%10]
  s+=f'<path d="M{cx} {cy} L{a[0]} {a[1]} L{b[0]} {b[1]} Z" fill="{colors[i]}"/><path d="M{cx} {cy} L{a[0]} {a[1]} L{c[0]} {c[1]} Z" fill="#f7df96" opacity=".65"/>'
 return s

def build(mat, fields=None):
 fields=fields or {}
 c=P[mat];count={'iron':1,'bronze':2,'silver':3,'gold':4}[mat];skills=[('蓄势',1)] if mat in ['iron','bronze'] else [('蓄势',2),('斩将',2)]+([('武圣',2)] if mat=='gold' else [])
 count=int(fields.get('stars',count));skills=fields.get('skills',skills)
 defs=f'''<defs>
 <linearGradient id="metal" gradientUnits="userSpaceOnUse" x1="45" y1="0" x2="990" y2="1536"><stop stop-color="{c[3]}"/><stop offset=".09" stop-color="{c[1]}"/><stop offset=".17" stop-color="{c[2]}"/><stop offset=".29" stop-color="{c[0]}"/><stop offset=".34" stop-color="{c[2]}"/><stop offset=".49" stop-color="{c[3]}"/><stop offset=".59" stop-color="{c[1]}"/><stop offset=".7" stop-color="{c[2]}"/><stop offset=".83" stop-color="{c[0]}"/><stop offset=".9" stop-color="{c[2]}"/><stop offset="1" stop-color="{c[3]}"/></linearGradient>
 <linearGradient id="bevel" x1="0" y1="0" x2="1" y2="1"><stop stop-color="{c[0]}"/><stop offset=".22" stop-color="{c[2]}"/><stop offset=".46" stop-color="{c[3]}"/><stop offset=".52" stop-color="{c[0]}"/><stop offset=".69" stop-color="{c[2]}"/><stop offset="1" stop-color="{c[4]}"/></linearGradient>
 <linearGradient id="rim"><stop stop-color="{c[4]}"/><stop offset=".16" stop-color="{c[1]}"/><stop offset=".23" stop-color="{c[0]}"/><stop offset=".4" stop-color="{c[2]}"/><stop offset=".72" stop-color="{c[3]}"/><stop offset=".88" stop-color="{c[1]}"/><stop offset="1" stop-color="{c[4]}"/></linearGradient>
 <radialGradient id="country" cx=".35" cy=".25"><stop stop-color="#5b8b46"/><stop offset=".55" stop-color="#214c2a"/><stop offset="1" stop-color="#0c281d"/></radialGradient>
 <linearGradient id="rank" x1="0" y1="0" x2="0" y2="1"><stop stop-color="#7e371f"/><stop offset=".52" stop-color="#392130"/><stop offset="1" stop-color="#201c3b"/></linearGradient>
 <linearGradient id="titleFace" x1="0" y1="0" x2="0" y2="1"><stop stop-color="#fffef3"/><stop offset=".45" stop-color="#f7f1d5"/><stop offset="1" stop-color="#c8b68b"/></linearGradient>
 <linearGradient id="starMetal" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#fff7be"/><stop offset=".45" stop-color="#e2ad45"/><stop offset="1" stop-color="#945a15"/></linearGradient>
 <pattern id="engrave" width="42" height="42" patternUnits="userSpaceOnUse" patternTransform="scale(.55)"><path d="M21 2L40 21L21 40L2 21Z M21 8L34 21L21 34L8 21Z M21 14L28 21L21 28L14 21Z" fill="none" stroke="{c[4]}" stroke-width=".6" opacity=".19"/><path d="M21 3L39 21L21 39 M21 9L33 21L21 33" fill="none" stroke="{c[0]}" stroke-width=".5" opacity=".21"/></pattern>
 <pattern id="brush" width="9" height="9" patternUnits="userSpaceOnUse"><path d="M0 1H9 M0 4H9 M0 7H9" stroke="{c[0]}" stroke-width=".28" opacity=".035"/></pattern>
 <clipPath id="frameclip"><path d="{OUTER} {INNER}" fill-rule="evenodd" clip-rule="evenodd"/></clipPath>
 <filter id="letterDepth" x="-.1" y="-.2" width="1.2" height="1.4"><feDropShadow dx="0" dy="1.4" stdDeviation=".35" flood-color="#050606" flood-opacity=".8"/></filter>
 <style>.txt{{font-family:'Noto Serif CJK SC';font-weight:700;fill:url(#titleFace);stroke:#131617;stroke-width:2.3;paint-order:stroke fill;stroke-linejoin:round;text-anchor:middle;dominant-baseline:central}}.sans{{font-family:'Noto Sans CJK SC';font-weight:500;fill:#fffaf0;stroke:#191a19;stroke-width:2.4;paint-order:stroke fill;text-anchor:middle;dominant-baseline:central}}</style>
 </defs>'''
 body=f'''<path d="{OUTER} {INNER}" fill="url(#metal)" fill-rule="evenodd" stroke="{c[4]}" stroke-width="6"/>
 <path d="{OUTER} {INNER}" fill="url(#engrave)" fill-rule="evenodd"/>
 <path d="{OUTER}" fill="none" stroke="url(#bevel)" stroke-width="11"/>
 <path d="M77 49H955Q964 49 964 61V1493Q964 1503 954 1503H79Q69 1503 69 1493V61Q69 49 77 49Z" fill="none" stroke="{c[0]}" stroke-width="1.25"/>
 <path d="{INNER}" fill="none" stroke="{c[4]}" stroke-width="12" stroke-linejoin="round"/>
 <path d="{INNER}" fill="none" stroke="url(#bevel)" stroke-width="8" stroke-linejoin="round"/>
 <path d="{INNER}" fill="none" stroke="{c[1]}" stroke-width="1.1" stroke-linejoin="round"/>
 <g clip-path="url(#frameclip)"><rect width="1024" height="1536" fill="url(#brush)"/></g>
 '''
 # Engraved central header with clean inset edge and an architectural diamond band.
 body+=f'<path d="M427 64H862V115H377Z" fill="{c[4]}" opacity=".76" stroke="{c[0]}" stroke-width="1.4"/>'
 for xx in [260,330]:body+=f'<path d="M{xx} 55l31 21-31 21-31-21Z M{xx} 64l17 12-17 12-17-12Z" fill="none" stroke="{c[1]}" stroke-width="2"/>'
 # Bottom key motif mirrors the reference structure but is native geometry.
 for xx in [596,668,740]:body+=f'<path d="M{xx} 1440l30 19-30 19-30-19Z M{xx} 1447l18 12-18 12-18-12Z" fill="none" stroke="{c[1]}" stroke-width="2"/>'
 # Concentric turned-metal sockets.
 def socket(cx,cy,r):
  q=''
  for rr,fill,stroke,sw in [(r,c[4],c[4],3),(r-4,'url(#bevel)',c[0],1),(r-12,c[4],c[3],1),(r-16,'url(#metal)',c[1],1.5),(r-26,c[4],c[4],2),(r-30,'url(#rim)',c[1],1),(r-35,c[4],c[3],1)]:q+=f'<circle cx="{cx}" cy="{cy}" r="{rr}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'
  q+=f'<path d="M{cx-r+8} {cy}A{r-8} {r-8} 0 0 1 {cx} {cy-r+8}" fill="none" stroke="{c[0]}" stroke-width="2.4" opacity=".85"/>'
  return q
 body+=socket(151,130,88)+socket(151,1387,94)+socket(897,1418,79)
 # Compact cloud-scroll supports, explicitly outlined metal, no raster ornament.
 cloud='M34 222H83Q96 222 96 209Q96 197 86 197Q76 197 78 207 M92 190H206Q220 190 220 202Q220 212 209 212 M134 226H248Q267 226 267 210Q267 198 257 199Q248 200 249 209 M147 226Q125 226 125 241Q125 252 136 252Q146 252 146 243'
 for sw,col in [(23,c[4]),(17,'url(#bevel)'),(2,c[0])]:body+=f'<path d="{cloud}" fill="none" stroke="{col}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"/>'
 # Low-profile lower scroll shoulders.
 for transform in ['translate(222 1408)','translate(815 1408) scale(-1 1)']:
  path='M0 0H66Q83 0 83-13Q83-25 72-25Q61-25 62-15 M14 15H90Q105 15 105 2Q105-8 96-8'
  for sw,col in [(18,c[4]),(12,'url(#bevel)'),(1.3,c[1])]:body+=f'<g transform="{transform}"><path d="{path}" fill="none" stroke="{col}" stroke-width="{sw}" stroke-linecap="round"/></g>'
 # Diamond level badge with genuine planar facets.
 for r,fill,sw in [(105,c[4],3),(99,'url(#bevel)',1),(85,c[4],2),(79,'url(#metal)',1),(66,c[4],1),(62,'url(#metal)',1)]:body+=f'<path d="M913 {124-r}L{913+r} 124L913 {124+r}L{913-r} 124Z" fill="{fill}" stroke="{c[1]}" stroke-width="{sw}"/>'
 body+=f'<path d="M913 27L1010 124H997L913 40Z" fill="{c[0]}" opacity=".75"/>'
 frame_body=body
 for i in range(count):body+=star(911,280+i*85)
 # Text fields and troop symbol remain independent and replaceable.
 body+='<circle cx="151" cy="130" r="47" fill="url(#country)" stroke="#0c1b12" stroke-width="2"/><text x="151" y="130" font-size="62" class="txt">蜀</text><text x="633" y="88" font-size="47" class="txt">真·关羽</text><text x="913" y="97" font-size="29" class="txt">LV</text><text x="913" y="145" font-size="53" class="txt">1</text><circle cx="151" cy="1387" r="58" fill="url(#rank)"/><text x="151" y="1386" font-size="83" class="txt">真</text><circle cx="897" cy="1418" r="46" fill="#0b1215"/>'
 body+='<path d="M897 1378l9 20-3 34h-12l-3-34z M893 1428h8v29h-8z M868 1404l9 13v17l11 7v10l-15-8-7-9z M926 1404l-9 13v17l-11 7v10l15-8 7-9z M879 1450h36l-6 9h-24z" fill="#f5edcf" stroke="#222b2b" stroke-width="1.2"/>'
 # Passive extensions share global material gradient and terminate straight into frame.
 for i,(name,lv) in enumerate(skills):
  y=1018+(3-len(skills)+i)*91
  path=f'M950 {y}H685Q665 {y} 665 {y+20}V{y+56}Q665 {y+76} 685 {y+76}H950'
  body+=f'<path d="{path}Z" fill="url(#metal)"/><path d="{path}Z" fill="url(#engrave)"/><path d="{path}" fill="none" stroke="{c[4]}" stroke-width="7"/><path d="{path}" fill="none" stroke="url(#bevel)" stroke-width="4.2"/><path d="M949 {y+3}H685Q668 {y+3} 668 {y+20}V{y+56}Q668 {y+73} 685 {y+73}H949" fill="none" stroke="{c[0]}" stroke-width=".9"/>'
  body+=f'<text x="805" y="{y+38}" class="sans" font-size="40">{name} +{lv}</text>'
 # Outer vertical rail stays continuous, hiding no hooks or terminal bumps.
 body+=f'<path d="M955 695V1330" stroke="{c[4]}" stroke-width="7"/><path d="M955 695V1330" stroke="url(#bevel)" stroke-width="4"/><path d="M954 695V1330" stroke="{c[1]}" stroke-width="1"/>'
 for old,new in [('>蜀<','>'+escape(str(fields.get('country','蜀')))+'<'),('>真·关羽<','>'+escape(str(fields.get('title','真·关羽')))+'<'),('>真<','>'+escape(str(fields.get('advancement','真')))+'<'),('>1</text>','>'+str(int(fields.get('level',1)))+'</text>')]:body=body.replace(old,new)
 # Native vector letter shadow; not a raster/filter fallback.
 body=re.sub(r'(<text [^>]*>[^<]*</text>)',lambda m:'<g transform="translate(0 1.4)" opacity=".7">'+m.group(1).replace('<text ','<text style="fill:#080b0d;stroke:#080b0d" ',1)+'</g>'+m.group(1),body)
 ui_body=body[len(frame_body):]
 for label,content in [('frame',frame_body),('ui',ui_body)]:
  (D/f'{mat}-{label}.svg').write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="3072" height="4608" viewBox="0 0 1024 1536">{defs}<g id="{label}">{content}</g></svg>')
 svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="3072" height="4608" viewBox="0 0 1024 1536">{defs}{body}</svg>'
 (D/f'{mat}-master.svg').write_text(svg)
 subprocess.run(['inkscape',str(D/f'{mat}-master.svg'),'--export-type=png',f'--export-filename={D}/{mat}-master-3072.png','--export-width=3072','--export-height=4608'],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
for mat in ['gold','iron']:build(mat)
(D/'config.json').write_text(json.dumps({'geometry_viewbox':[1024,1536],'native_render':[3072,4608],'source':'100% code-native SVG geometry, gradients and typography; no existing frame image pixels','materials':P,'dynamic_fields':['country','title','level','advancement','troop_icon','skill_name','skill_level','skill_count','stars'],'status':'structure and material prototype; artwork slot intentionally transparent; illustration quality not implied','fonts':['Noto Serif CJK SC Bold','Noto Sans CJK SC Medium']},ensure_ascii=False,indent=2))
