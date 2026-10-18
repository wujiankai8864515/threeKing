from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from scipy import ndimage
import json, hashlib, html, subprocess
D=Path(__file__).resolve().parent/'ui';D.mkdir(exist_ok=True)
P=D.parent
BASE=Path('guojia-set/ui_newframe_2026-10-18_21-43-45_UTC+08')
SIZE=(1190,1786);SX=1190/1024;SY=1786/1536;OFFSET=(84,145)
PANEL_BOX_X=(666,944);PANEL_WIDTH=202;PANEL_HEIGHT=86
LEFT_CAP=40;RIGHT_CAP=22
SLOT_CENTERS=[961,1045,1129]
PLATE_TOP=1086;PLATE_BOTTOM=1172
FONT_GAP=12
cache={}
def text_tile(t,size,serif=False):
 key=(t,size,serif)
 if key in cache:return cache[key]
 tag=f'text-{len(cache):02d}';font='Noto Serif CJK SC' if serif else 'Noto Sans CJK SC';weight='700' if serif else '500'
 body=f'<text x="20" y="120" font-family="{font}" font-weight="{weight}" font-size="{size:.6f}">{{}}</text>'
 head='<svg xmlns="http://www.w3.org/2000/svg" width="520" height="180" viewBox="0 0 520 180">'
 txt=html.escape(t)
 # Outline and shadow retain the prior colors and scales. The centering mask measures real filled glyphs.
 vis=head+f'<g transform="translate(0 {2*SY})" fill="#080808" stroke="#080808" stroke-width="{3.2*SX}" paint-order="stroke">'+body.format(txt)+'</g>'+f'<g fill="#fff7df" stroke="#302310" stroke-width="{1.8*SX}" paint-order="stroke">'+body.format(txt)+'</g></svg>'
 ink=head+'<g fill="white">'+body.format(txt)+'</g></svg>'
 images=[]
 for suffix,svg in [('visible',vis),('ink',ink)]:
  sp=D/f'{tag}-{suffix}.svg';ip=D/f'{tag}-{suffix}.png';sp.write_text(svg)
  subprocess.run(['inkscape',str(sp),'--export-filename='+str(ip)],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
  images.append(Image.open(ip).convert('RGBA'))
 vb=images[0].getbbox();ib=images[1].getbbox()
 result=(images[0],images[1],ib,vb);cache[key]=result;return result

def place_glyph(tx,inkmap,t,size,cx,cy,serif=False):
 vis,ink,ib,vb=text_tile(t,size,serif)
 x=round(cx-(ib[0]+ib[2])/2);y=round(cy-(ib[1]+ib[3])/2)
 tx.alpha_composite(vis,(x,y));inkmap.alpha_composite(ink,(x,y))
 return {'text':t,'ink_bbox':[ib[0]+x,ib[1]+y,ib[2]+x,ib[3]+y],'ink_center':[(ib[0]+ib[2])/2+x,(ib[1]+ib[3])/2+y],'target_center':[cx,cy],'max_center_error_px':max(abs((ib[0]+ib[2])/2+x-cx),abs((ib[1]+ib[3])/2+y-cy))}

def rebuild_frame(orig):
 patch=orig.crop((PANEL_BOX_X[0],PLATE_TOP,PANEL_BOX_X[1],PLATE_BOTTOM))
 # Remove disconnected one-pixel alpha flecks from the existing component, preserving its silhouette.
 ar=np.array(patch);lab,n=ndimage.label(ar[:,:,3]>0);counts=np.bincount(lab.ravel());counts[0]=0;keep=lab==counts.argmax();ar[~keep]=0;patch=Image.fromarray(ar)
 mid=patch.crop((LEFT_CAP,0,patch.width-RIGHT_CAP,patch.height)).resize((PANEL_WIDTH-LEFT_CAP-RIGHT_CAP,PANEL_HEIGHT),Image.Resampling.LANCZOS)
 short=Image.new('RGBA',(PANEL_WIDTH,PANEL_HEIGHT));short.paste(patch.crop((0,0,LEFT_CAP,PANEL_HEIGHT)),(0,0));short.paste(mid,(LEFT_CAP,0));short.paste(patch.crop((patch.width-RIGHT_CAP,0,patch.width,PANEL_HEIGHT)),(PANEL_WIDTH-RIGHT_CAP,0))
 clean=orig.copy();clean.paste((0,0,0,0),(630,890,938,1190))
 return clean,short


mask=Image.open(BASE/'art-native-slot-mask.png').convert('L');mask.save(D/'art-native-slot-mask.png')
config={};manifest={'native_card_art':[1024,1536],'native_stories':[1536,1024],'canvas':SIZE,'resampling':'Art pasted 1:1; existing 1024x1536 frame enlarged; typography rendered at output size. Not 4K.','status':'candidate awaiting user','cards':{}}
passives=[('达识','自身术伤提高'),('深谋','谋记存在时间延长'),('远虑','主动施放距离提高')]
for i,t in enumerate(['iron','bronze','silver','gold']):
 n=[1,1,2,3][i];skills=[{'name':a,'level':'+1' if i<2 else '+2','effect':b} for a,b in passives[:n]]
 config[t]={'country':'魏','title':'郭嘉','level':'1','stars':i+1,'advancement':['初','策','谋','真'][i],'skills':skills,'troop_icon':'原创卷册与令旗图标（谋士兵种草案）','active':{'name':'谋记','effect':'目标下次主动完成后结算一次术伤并消失'},'status':'全部技能与数值为草案'}
 orig=Image.open(BASE/('silver-empty-cleanalpha-1024.png' if t=='silver' else f'{t}-empty-generated-1024.png')).convert('RGBA')
 frame,short=rebuild_frame(orig)
 for cy in SLOT_CENTERS[-n:]:frame.alpha_composite(short,(944-PANEL_WIDTH,round(cy-PANEL_HEIGHT/2)))
 frame.paste(orig.crop((938,890,1024,1190)),(938,890));frame=frame.resize(SIZE,Image.Resampling.LANCZOS);frame.save(D/f'{t}-frame.png')
 tx=Image.new('RGBA',SIZE);ink=Image.new('RGBA',SIZE);draw=ImageDraw.Draw(tx)
 draw.ellipse((101*SX,89*SY,187*SX,175*SY),fill='#123b64',outline='#719bb8',width=2)
 metrics=[]
 for txt,size,cx,cy,serif in [('魏',62,144,132,True),('郭嘉',45,630,90,True),('LV',26,909,105,False),('1',48,909,148,False),(config[t]['advancement'],78,155,1384,True)]:
  metrics.append(place_glyph(tx,ink,txt,size*SX,cx*SX,cy*SY,serif))
 for cy,sk in zip(SLOT_CENTERS[-n:],skills):
  a=text_tile(sk['name'],38*SX);b=text_tile(sk['level'],35*SX);aw=a[2][2]-a[2][0];bw=b[2][2]-b[2][0];cx=((944-PANEL_WIDTH+13)+933)/2*SX;left=cx-(aw+12+bw)/2
  metrics.append(place_glyph(tx,ink,sk['name'],38*SX,left+aw/2,cy*SY))
  metrics.append(place_glyph(tx,ink,sk['level'],35*SX,left+aw+12+bw/2,cy*SY))
 # Code-native icon: rolled scroll with upright command pennant. No text substitute.
 svg='<svg xmlns="http://www.w3.org/2000/svg" width="1190" height="1786" viewBox="0 0 1024 1536"><g transform="translate(900 1424)" fill="#fff7df" stroke="#302310" stroke-width="2.5"><path d="M-25,-8 Q-31,-15 -25,-20 L13,-20 L13,18 L-25,18 Q-18,12 -25,6 Z"/><path d="M-25,-20 Q-17,-14 -25,-8 M-25,6 Q-32,12 -25,18 M17,26 L17,-40 L40,-33 L17,-23" fill="none"/><path d="M-14,-10 L4,-10 M-14,-2 L4,-2 M-14,6 L4,6" fill="none"/></g></svg>'
 (D/f'{t}-troop-icon.svg').write_text(svg);subprocess.run(['inkscape',str(D/f'{t}-troop-icon.svg'),'--export-filename='+str(D/f'{t}-troop-icon.png')],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
 tx.alpha_composite(Image.open(D/f'{t}-troop-icon.png').convert('RGBA'));tx.save(D/f'{t}-text.png');ink.save(D/f'{t}-ink-mask.png')
 src=P/'raw'/f'card{i+1:02d}.png';im=Image.open(src).convert('RGBA');assert im.size==(1024,1536)
 canvas=Image.new('RGBA',SIZE);canvas.paste(im,OFFSET);art=Image.new('RGBA',SIZE);art.paste(canvas,(0,0),mask)
 out=Image.alpha_composite(Image.alpha_composite(art,frame),tx);dest=P/'candidates'/f'card{i+1:02d}.png';out.save(dest)
 region=(slice(145,1681),slice(84,1108));valid=(np.array(mask)[region]==255)&(np.array(frame.getchannel('A'))[region]==0)&(np.array(tx.getchannel('A'))[region]==0)
 changed=int(np.count_nonzero(np.any(np.array(out)[region]!=np.array(im),axis=2)&valid));assert changed==0
 manifest['cards'][t]={'source':str(src),'sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'candidate':str(dest),'fields':config[t],'glyph_metrics':metrics,'art_pixels_changed':changed}
 out.crop((720,1020,1130,1390)).save(P/'qa'/f'{t}-passives.png')
(D/'ui-config.json').write_text(json.dumps(config,ensure_ascii=False,indent=2));(P/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
for j in [2,3,4]:(P/'candidates'/f'story{j:02d}.png').write_bytes((P/'raw'/f'story{j:02d}.png').read_bytes())
font=ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',24)
sheet=Image.new('RGB',(1920,1460),'#172431');d=ImageDraw.Draw(sheet)
for i in range(4):
 im=Image.open(P/'candidates'/f'card{i+1:02d}.png').convert('RGBA');im.thumbnail((480,720));sheet.paste(im,(480*i,40),im)
for i in range(3):
 im=Image.open(P/'candidates'/f'story{i+2:02d}.png').convert('RGB');im.thumbnail((640,427));sheet.paste(im,(640*i,830))
for i,t in enumerate(['初入谋席 · 第10回','十胜开局 · 第18回','下邳观流 · 第19回','易州遗筹 · 第33回']):d.text((480*i+35,765),t,font=font,fill='white')
for i,t in enumerate(['袁书到时 → 青铜十胜','两河可用 → 白银观流','封书托后事 → 黄金遗筹']):d.text((640*i+35,1280),t,font=font,fill='white')
d.text((25,6),'郭嘉｜四阶三传记｜全新候选',font=font,fill='white')
d.text((25,1350),'插画原生：竖1024×1536，横1536×1024；卡片合成1190×1786。未冒充4K。',font=font,fill='#bdd0dc')
d.text((25,1390),'烛影玄鸦、服饰、具体镜头为原创演绎；事件锚定《三国演义》。技能/UI数值为草案。',font=font,fill='#bdd0dc')
sheet.save(P/'candidates'/'郭嘉-四阶三传记-总览.png')
print(P)
