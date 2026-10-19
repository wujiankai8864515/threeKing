from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import math,json,hashlib,subprocess,argparse,html
P=Path(__file__).resolve().parent
W,H=1190,1786
F='/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc'
def star(cx,cy,r):
 return [(cx+math.cos(-math.pi/2+i*math.pi/5)*(r if i%2==0 else r*.43),cy+math.sin(-math.pi/2+i*math.pi/5)*(r if i%2==0 else r*.43)) for i in range(10)]
def points(ps):return ' '.join(f'{x:.2f},{y:.2f}' for x,y in ps)
def make_frame(tier):
 gold=tier==6
 light,mid,dark=('#fff2b2','#b97919','#38220a') if gold else ('#f4ffff','#8ab4c9','#253a59')
 crystal=('#dcacff','#744ac5','#20143e') if gold else ('#ffffff','#92d9e8','#385b91')
 s=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}"><defs>']
 s+=[f'<linearGradient id="metal" x1="0" y1="0" x2=".8" y2="1" gradientUnits="objectBoundingBox"><stop stop-color="{light}"/><stop offset=".12" stop-color="{mid}"/><stop offset=".22" stop-color="{light}"/><stop offset=".31" stop-color="{dark}"/><stop offset=".47" stop-color="{mid}"/><stop offset=".51" stop-color="{light}"/><stop offset=".60" stop-color="{mid}"/><stop offset=".80" stop-color="{dark}"/><stop offset=".92" stop-color="{mid}"/><stop offset="1" stop-color="{light}"/></linearGradient>']
 s+=[f'<linearGradient id="gem" x1="0" y1="0" x2="1" y2="1"><stop stop-color="{crystal[0]}"/><stop offset=".16" stop-color="{crystal[1]}"/><stop offset=".43" stop-color="{crystal[2]}"/><stop offset=".64" stop-color="{crystal[1]}"/><stop offset="1" stop-color="{crystal[2]}"/></linearGradient><linearGradient id="plate" x2="0" y2="1"><stop stop-color="{crystal[1]}"/><stop offset=".4" stop-color="{crystal[2]}"/><stop offset=".9" stop-color="{crystal[2]}"/><stop offset="1" stop-color="{crystal[1]}"/></linearGradient></defs>']
 # Continuous pierced frame: center is truly alpha, no colored rectangular backdrop.
 for inset,stroke,width in [(27,'#080c18',30),(29,'url(#metal)',22),(42,light,2),(51,dark,7),(57,'url(#metal)',5),(64,light,1.5)]:
  s.append(f'<rect x="{inset}" y="{inset+22}" width="{W-2*inset}" height="{H-2*inset-44}" rx="25" fill="none" stroke="{stroke}" stroke-width="{width}"/>')
 # Header / footer cut-facet structures.
 for d in ['M66 65 H1124 V139 H66 Z','M66 1687 H1124 V1737 H66 Z']:
  s.append(f'<path d="{d}" fill="url(#gem)" stroke="url(#metal)" stroke-width="12"/>')
 # Repeated engraving lines on header/footer, restrained connected geometry.
 for y in (77,1711):
  for x in range(310,960,70):
   s.append(f'<path d="M{x} {y} l22 -9 22 9 -22 9 Z M{x+9} {y} l13 -5 13 5 -13 5 Z" fill="none" stroke="{light}" stroke-opacity=".32" stroke-width="1.5"/>')
 # Crystal rib faceting along outer rails.
 for x in (58,1132):
  for y in range(270,1580,130):
   s.append(f'<path d="M{x} {y} l16 30 -16 66 -16 -30 Z" fill="url(#gem)" stroke="{mid}" stroke-width="2"/><path d="M{x} {y}v96 M{x-16} {y+66}l32 -36" fill="none" stroke="{light}" stroke-width="1" opacity=".8"/>')
 # Structured scroll corners with thick shared metal, no noise or sparkles.
 for x,y,rot in [(83,146,0),(1107,146,90),(1107,1680,180),(83,1680,270)]:
  s.append(f'<g transform="translate({x} {y}) rotate({rot})"><path d="M-30 105 V-34 H108 L72 4 H15 V70 Z" fill="url(#metal)" stroke="{dark}" stroke-width="5"/><path d="M-19 81 V-22 H80 L61 -4 H6 V56 Z" fill="url(#gem)" stroke="{light}" stroke-width="2"/><path d="M17 15h45l-17 18H17v24" fill="none" stroke="url(#metal)" stroke-width="7"/></g>')
 # faction medallion; blank until dynamic text layer.
 for cx,cy,r in [(159,146,102),(159,1635,94),(1052,1635,77)]:
  s.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#metal)" stroke="{dark}" stroke-width="5"/><circle cx="{cx}" cy="{cy}" r="{r-12}" fill="url(#gem)" stroke="{light}" stroke-width="3"/><circle cx="{cx}" cy="{cy}" r="{r-24}" fill="'+('#153d29' if cy==146 else 'url(#plate)')+f'" stroke="url(#metal)" stroke-width="7"/>')
 # Top-right level faceted cartouche.
 s.append(f'<path d="M1061 55 L1153 147 1061 239 969 147 Z" fill="url(#metal)" stroke="{dark}" stroke-width="5"/><path d="M1061 76 L1132 147 1061 218 990 147 Z" fill="url(#gem)" stroke="{light}" stroke-width="3"/>')
 # Five/six clearly separate sculpted five-point stars in narrow right rail.
 for i in range(tier):
  cx,cy,r=1130,330+i*104,37
  ps=star(cx,cy,r)
  s.append(f'<polygon points="{points(ps)}" fill="{dark}" stroke="{dark}" stroke-width="6"/>')
  for j in range(10):
   color=[light,mid,light,dark,mid][j%5]
   s.append(f'<polygon points="{points([(cx,cy),ps[j],ps[(j+1)%10]])}" fill="{color}"/>')
  s.append(f'<polygon points="{points(ps)}" fill="none" stroke="{light}" stroke-width="1.5"/>')
 # three bottom-anchored compact straight-connected rails; rounded corners no triangle hooks.
 for cy in (1180,1278,1376):
  s.append(f'<path d="M884 {cy-38} H1125 V{cy+38} H884 Q872 {cy+38} 872 {cy+26} V{cy-26} Q872 {cy-38} 884 {cy-38}Z" fill="url(#metal)" stroke="{dark}" stroke-width="4"/><path d="M889 {cy-28}H1128V{cy+28}H889Q882 {cy+28} 882 {cy+20}V{cy-20}Q882 {cy-28} 889 {cy-28}Z" fill="url(#plate)" stroke="{light}" stroke-width="1.5"/>')
 # small tier-specific cut gemstones, integrated in footer/header.
 for cx,cy in [(305,104),(926,104),(515,1711),(675,1711)]:
  ps=[(cx,cy-19),(cx+32,cy),(cx,cy+19),(cx-32,cy)]
  s.append(f'<polygon points="{points(ps)}" fill="url(#gem)" stroke="url(#metal)" stroke-width="4"/><path d="M{cx-32} {cy}H{cx+32}M{cx} {cy-19}V{cy+19}" stroke="{light}" opacity=".65"/>')
 s.append('</svg>')
 svg=P/f'frame-{tier}star.svg';svg.write_text(''.join(s));png=svg.with_suffix('.png')
 subprocess.run(['inkscape',str(svg),'--export-filename='+str(png)],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,check=True)
 return png

def text_center(draw,xy,text,size,fill='#fff9e8',stroke=2):
 font=ImageFont.truetype(F,size);b=draw.textbbox((0,0),text,font=font,stroke_width=stroke)
 draw.text((xy[0]-(b[0]+b[2])/2,xy[1]-(b[1]+b[3])/2),text,font=font,fill=fill,stroke_width=stroke,stroke_fill='#1a1321')
 return list(b)
def compose(cfg):
 outdir=Path(cfg.get('outdir',P/'cards'));outdir.mkdir(parents=True,exist_ok=True)
 tier=int(cfg['tier']);source=Path(cfg['source']);im=Image.open(source).convert('RGBA');assert im.size==(1024,1536),im.size
 canvas=Image.new('RGBA',(W,H));canvas.alpha_composite(im,(83,145));frame=Image.open(P/f'frame-{tier}star.png').convert('RGBA');canvas.alpha_composite(frame)
 layer=Image.new('RGBA',(W,H));d=ImageDraw.Draw(layer)
 text_center(d,(160,145),'蜀',72);text_center(d,(612,105),cfg['name'],56)
 text_center(d,(1061,120),'LV',24);text_center(d,(1061,165),str(cfg.get('level',1)),43)
 # branch at center badge: two-char readable and fully centered.
 text_center(d,(159,1635),cfg['branch'],41)
 for cy,sk in zip((1180,1278,1376),cfg['skills']):
  assert len(sk['name'])==2,sk
  text_center(d,(995,cy),sk['name']+' +'+str(sk.get('level',1)),37)
 # troop icon, native vector-like independent transparent glyph.
 d.polygon([(1052,1588),(1076,1613),(1072,1658),(1052,1675),(1032,1658),(1028,1613)],fill='#eee4c4',outline='#211723',width=4)
 d.line([(1052,1597),(1052,1667)],fill='#5b3e31',width=5)
 canvas.alpha_composite(layer)
 stem=f"{cfg['hero']}-{cfg['branch_id']}-{tier}star";path=outdir/(stem+'.png');canvas.save(path)
 layer.save(outdir/(stem+'-dynamic-ui.png'))
 preview=canvas.copy();preview.thumbnail((400,600));preview.save(outdir/(stem+'-preview.png'))
 result={**cfg,'output':str(path.resolve()),'text_layer':str((outdir/(stem+'-dynamic-ui.png')).resolve()),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'output_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'native_art_size':list(im.size),'canvas_size':[W,H],'source_scale':1,'illustration_offset':[83,145],'status':'candidate_pending_user_review','three_passives_bottom_anchored':True,'stars':tier}
 (outdir/(stem+'.json')).write_text(json.dumps(result,ensure_ascii=False,indent=2));return result
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--config');ap.add_argument('--frames',action='store_true');a=ap.parse_args()
 if a.frames:
  for t in (5,6):make_frame(t)
 if a.config:print(json.dumps(compose(json.loads(Path(a.config).read_text())),ensure_ascii=False))
