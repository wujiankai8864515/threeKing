ASSET=__import__('pathlib').Path(__file__).resolve().parent
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import numpy as np
from scipy import ndimage
import json,hashlib,argparse
P=Path('/workspace/scratch/3f82ff2b3f81/advanced-card-ui/2026-10-19_13-57-00_UTC+08')
W,H=1190,1786;SX=W/1024;SY=H/1536
F='/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc'
MASK=Path('/workspace/scratch/3f82ff2b3f81/guanyu-mythic-set/ui-local-composite-candidates_2026-10-18_23-55-42_UTC+08/art-native-slot-mask.png')
def make_frame(tier):
 orig=Image.open(P/f'generated-frame-{tier}star.png').convert('RGBA');a=np.array(orig)
 # Remove disconnected alpha dust while retaining original connected frame relief.
 lab,n=ndimage.label(a[:,:,3]>128);c=np.bincount(lab.ravel());c[0]=0;solid=lab==c.argmax();keep=ndimage.binary_dilation(solid,iterations=2);a[~keep]=0
 clean=Image.fromarray(a)
 outer=Image.new('L',(1024,1536));od=ImageDraw.Draw(outer)
 od.polygon([(54,39),(876,39),(907,9),(944,40),(975,40),(975,89),(1020,131),(987,169),(975,183),(975,1508),(54,1508),(54,1452),(40,1418),(40,1344),(54,1290),(54,245),(15,245),(15,203),(54,183)],fill=255)
 clean.putalpha(Image.fromarray(np.minimum(np.array(clean.getchannel('A')),np.array(outer))))
 # Each generated compact rail is shortened by three-slice, not stretched text.
 boxes={5:[(672,919,942,1001),(672,1005,942,1086),(672,1089,942,1173)],6:[(673,926,938,1009),(673,1011,938,1095),(673,1096,938,1180)]}[tier]
 clean.paste((0,0,0,0),(645,895,933,1200))
 for box,cy in zip(boxes,(961,1045,1129)):
  tile=orig.crop(box);tile=tile.resize((tile.width,82),Image.Resampling.LANCZOS);tw=202
  small=Image.new('RGBA',(tw,82));small.alpha_composite(tile.crop((0,0,29,82)),(0,0));small.alpha_composite(tile.crop((29,0,tile.width-16,82)).resize((tw-45,82),Image.Resampling.LANCZOS),(29,0));small.alpha_composite(tile.crop((tile.width-16,0,tile.width,82)),(tw-16,0));clean.alpha_composite(small,(940-tw,cy-41))
 # original right rail covers the butt joint for visually seamless straight continuation.
 clean.alpha_composite(orig.crop((930,895,975,1200)),(930,895))
 clean.save(P/f'frame-{tier}star-native.png');clean.resize((W,H),Image.Resampling.LANCZOS).save(P/f'frame-{tier}star.png')

def center(draw,xy,text,size,fill='#fff7e1',stroke=2):
 font=ImageFont.truetype(F,size);b=draw.textbbox((0,0),text,font=font)
 draw.text((xy[0]-(b[0]+b[2])/2,xy[1]-(b[1]+b[3])/2+2),text,font=font,fill='#08080d',stroke_width=stroke+1,stroke_fill='#08080d')
 draw.text((xy[0]-(b[0]+b[2])/2,xy[1]-(b[1]+b[3])/2),text,font=font,fill=fill,stroke_width=stroke,stroke_fill='#2c2331')
 return {'text':text,'target_center':list(xy),'glyph_bbox':list(b)}
def compose(cfg):
 outdir=Path(cfg.get('outdir',P/'cards'));outdir.mkdir(parents=True,exist_ok=True)
 tier=int(cfg['tier']);source=Path(cfg['source']);im=Image.open(source).convert('RGBA');assert im.size==(1024,1536),im.size
 raw=Image.new('RGBA',(W,H));raw.alpha_composite(im,(84,145));mask=Image.open(MASK).convert('L');canvas=Image.new('RGBA',(W,H));canvas.paste(raw,(0,0),mask)
 frame=Image.open(P/f'frame-{tier}star.png').convert('RGBA');canvas.alpha_composite(frame)
 layer=Image.new('RGBA',(W,H));d=ImageDraw.Draw(layer);measures=[]
 # Opaque matte green inset on faction medallion remains an independently replaceable layer.
 cx,cy=147*SX,133*SY;r=62*SX;d.ellipse((cx-r,cy-r,cx+r,cy+r),fill='#163e2a',outline='#a7c89a',width=2)
 measures.append(center(d,(cx,cy),'蜀',int(70*SX)))
 if '·' in cfg['name']:
  left,right=cfg['name'].split('·',1);size=int(47*SX);font=ImageFont.truetype(F,size)
  lb=d.textbbox((0,0),left,font=font);rb=d.textbbox((0,0),right,font=font);lw=lb[2]-lb[0];rw=rb[2]-rb[0];gap=22;cx,cy=625*SX,92*SY;start=cx-(lw+rw+gap)/2
  measures.append(center(d,(start+lw/2,cy),left,size));measures.append(center(d,(start+lw+gap+rw/2,cy),right,size))
  px=start+lw+gap/2;d.ellipse((px-5,cy-5,px+5,cy+5),fill='#fff7e1',outline='#2c2331',width=2)
  measures.append({'text':'·','target_center':[px,cy],'geometric_centered':True})
 else:
  measures.append(center(d,(625*SX,92*SY),cfg['name'],int(47*SX)))
 center(d,(909*SX,105*SY),'LV',24);center(d,(909*SX,151*SY),str(cfg.get('level',1)),44)
 # Progression branch is a dynamic two-character medallion, not baked into source art.
 badge=Image.open(str(ASSET/('fenghou-metal.png' if tier==6 else 'tian-metal-calligraphy.png'))).convert('RGBA');layer.alpha_composite(badge,(round(155*SX-75),round(1384*SY-72.5)))
 assert len(cfg['skills'])==3
 for y,sk in zip((961,1045,1129),cfg['skills']):
  assert len(sk['name'])==2,sk
  measures.append(center(d,(838*SX,y*SY),sk['name']+' +'+str(sk.get('level',1)),int(33*SX)))
 icon=Image.open(str(ASSET/'spearhead.png')).convert('RGBA');layer.alpha_composite(icon,(round(901*SX-60),round(1411*SY-57.5)))
 canvas.alpha_composite(layer)
 stem=f"{cfg['hero']}-{cfg['branch_id']}-{tier}star";path=outdir/(stem+'.png');canvas.save(path);layer.save(outdir/(stem+'-dynamic-ui.png'))
 preview=canvas.copy();preview.thumbnail((400,600));preview.save(outdir/(stem+'-preview.png'))
 reg=(slice(145,1681),slice(84,1108));valid=(np.array(mask)[reg]==255)&(np.array(frame.getchannel('A'))[reg]==0)&(np.array(layer.getchannel('A'))[reg]==0)
 changed=int((np.any(np.array(canvas)[reg]!=np.array(im),axis=2)&valid).sum());assert changed==0
 result={**cfg,'output':str(path.resolve()),'text_layer':str((outdir/(stem+'-dynamic-ui.png')).resolve()),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'output_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'native_art_size':list(im.size),'canvas_size':[W,H],'source_scale':1,'illustration_offset':[84,145],'status':'candidate_pending_user_review','three_passives_bottom_anchored':True,'six_star_passive_count':'design default of three, not a user-fixed count' if tier==6 else None,'stars':tier,'glyph_centers':measures,'uncovered_art_pixels_checked':int(valid.sum()),'uncovered_art_pixels_changed':changed}
 (outdir/(stem+'.json')).write_text(json.dumps(result,ensure_ascii=False,indent=2));return result
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--config');ap.add_argument('--frames',action='store_true');a=ap.parse_args()
 if a.frames:
  for t in (5,6):make_frame(t)
 if a.config:print(json.dumps(compose(json.loads(Path(a.config).read_text())),ensure_ascii=False))
