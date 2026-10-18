from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from scipy import ndimage
import argparse, json, hashlib, html, subprocess, shutil, re

P=Path(__file__).resolve().parent
R=Path('/workspace/scratch/3f82ff2b3f81/pangtong-set')
BASE=R/'ui_newframe_2026-10-18_20-53-40_UTC+08'
ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,default=P)
for tier in ('bronze','silver','gold'):ap.add_argument(f'--{tier}-source',type=Path)
args=ap.parse_args()
D=args.out.resolve();D.mkdir(parents=True,exist_ok=True)
if D!=P:shutil.copy2(__file__,D/'compose_layout.py')
SIZE=(1190,1786);SX=1190/1024;SY=1786/1536;OFFSET=(84,145)
fields=json.loads((BASE/'ui-config.json').read_text());sources={}
original_titles={tier:f['title'] for tier,f in fields.items()}
for f in fields.values():f['title']='魏延'
for tier,f in fields.items():
 names={'iron':['破甲'],'bronze':['破甲'],'silver':['破甲','偏锋'],'gold':['破甲','偏锋','守隘']}[tier]
 f['skills']=[{'name':n,'level':('+1' if tier in ('iron','bronze') else '+2')} for n in names]
 f['skill_status']='proposed one-effect passives, not approved gameplay'
for tier in fields: fields[tier]['advancement']={'iron':'一','bronze':'二','silver':'三','gold':'四'}[tier]
sources={key:{'path':str(P.parent/'raw'/f'card{i:02}.png')} for i,key in enumerate(['blackiron','bronze','silver','gold'],1)}
overrides={}
# Title is the user's current name field, independent of the existing advancement badge.
# All other existing fields remain unchanged layout examples, not game-rule changes.
for f in fields.values():f['advancement_status']='temporary tier placeholder only; 一二三四 are not user-approved advancement names'
(D/'ui-config.json').write_text(json.dumps(fields,ensure_ascii=False,indent=2))
mask=Image.open(BASE/'art-native-slot-mask.png').convert('L')
mask.save(D/'art-native-slot-mask.png')
# Existing metallic panel is sliced; only its central repeatable body changes length.
PANEL_BOX_X=(666,944);PANEL_WIDTH=202;PANEL_HEIGHT=86
LEFT_CAP=40;RIGHT_CAP=22
SLOT_CENTERS=[961,1045,1129]
PLATE_TOP=1086;PLATE_BOTTOM=1172
# Fitted center of each existing inner circular border. No new advancement field.
BADGE_CENTERS={'iron':(155.5,1384.5),'bronze':(155.5,1384.0),'silver':(155.0,1384.5),'gold':(155.0,1384.0)}
FONT_GAP=12 # output pixels; fixed visual-ink gap between name and +level
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

manifest={'canvas':list(SIZE),'illustration_native_size':[1024,1536],'illustration_resampling':'none; 1:1 at (84,145)','ui_scope':'existing metallic panel 3-slice shortening, shared bottom-up slots, measured glyph centering only','ui_values':'魏延; passive name/levels and rank placeholders are draft; troop icon war dao','native_panel_width_before':278,'native_panel_width_after':PANEL_WIDTH,'fixed_name_level_ink_gap_px':FONT_GAP,'slot_centers_native':SLOT_CENTERS,'bottom_anchor_native':1172,'replacement_source_status':{tier:(('approved native illustration plus existing approved plaque lettering' if tier=='silver' else 'approved complete new native illustration; used as-is') if src else 'previous source') for tier,src in overrides.items()},'cards':{}}
for tier,label in [('iron','01-黑铁'),('bronze','02-青铜'),('silver','03-白银'),('gold','04-黄金')]:
 f=fields[tier];n=len(f['skills']);src=Path(sources['blackiron' if tier=='iron' else tier]['path']);pure=Image.open(src).convert('RGBA');assert pure.size==(1024,1536)



 orig=Image.open(BASE/('silver-empty-cleanalpha-1024.png' if tier=='silver' else f'{tier}-empty-generated-1024.png')).convert('RGBA')
 frame,short=rebuild_frame(orig)
 rows=[]
 for cy in SLOT_CENTERS[-n:]:
  top=round(cy-PANEL_HEIGHT/2);frame.alpha_composite(short,(944-PANEL_WIDTH,top));rows.append({'center_native':cy,'component_box_native':[944-PANEL_WIDTH,top,944,top+PANEL_HEIGHT]})
 # The original rail is the top-most join cover; all unchanged frame areas retain exact source pixels.
 rail=orig.crop((938,890,1024,1190));frame.paste(rail,(938,890))
 frame=frame.resize(SIZE,Image.Resampling.LANCZOS);frame.save(D/f'{tier}-frame-layout-1190.png')
 # Leave all unrelated independent typography unchanged.
 base_svg=(BASE/f'{tier}-text-overlay.svg').read_text().replace(html.escape(original_titles[tier]),html.escape(f['title']))
 base_svg=re.sub(r'<g transform="translate\(900 1424\)".*?</g>', '<g transform="translate(900 1424)" fill="#fff7df" stroke="#302310" stroke-width="2.4"><path d="M -5 37 L -5 -10 L 3 -39 Q 33 -30 27 -9 L 5 2 L 5 37 Z"/><path d="M -22 8 L 22 8" stroke-width="5"/></g>',base_svg)
 base_svg=re.sub(r'<text[^>]*>(?:伏焰|引燎|凤策|\+1|\+2)</text>', '', base_svg)
 svg_path=D/f'{tier}-base-text-title.svg';svg_path.write_text(base_svg)
 base_png=D/f'{tier}-base-text-title.png'
 subprocess.run(['inkscape',str(svg_path),'--export-filename='+str(base_png)],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
 tx=Image.open(base_png).convert('RGBA');tx.paste((0,0,0,0),(760,1010,1100,1390));tx.paste((0,0,0,0),(70,1480,300,1720))
 inkmap=Image.new('RGBA',SIZE);measured=[]
 for row,sk in zip(rows,f['skills']):
  cy=row['center_native']*SY
  name=text_tile(sk['name'],min(38,100/len(sk['name']))*SX);level=text_tile(sk['level'],35*SX)
  nw=name[2][2]-name[2][0];lw=level[2][2]-level[2][0];width=nw+FONT_GAP+lw
  # Interior is bounded by the round left endcap and the straight right rail.
  cx=((944-PANEL_WIDTH+13)+933)/2*SX
  left=cx-width/2
  a=place_glyph(tx,inkmap,sk['name'],min(38,100/len(sk['name']))*SX,left+nw/2,cy)
  b=place_glyph(tx,inkmap,sk['level'],35*SX,left+nw+FONT_GAP+lw/2,cy)
  row.update({'text_name':a,'text_level':b,'actual_ink_gap_px':b['ink_bbox'][0]-a['ink_bbox'][2],'group_target_center_px':[cx,cy]});measured.append(row)
 bx,by=BADGE_CENTERS[tier];badge=place_glyph(tx,inkmap,f['advancement'],78*SX,bx*SX,by*SY,True) if f['advancement'] else {'text':'','status':'existing empty field retained'}
 tx.save(D/f'{tier}-text-overlay-1190.png');inkmap.save(D/f'{tier}-centering-ink-mask-1190.png')
 canvas=Image.new('RGBA',SIZE);canvas.paste(pure,OFFSET);art=Image.new('RGBA',SIZE);art.paste(canvas,(0,0),mask)
 out=Image.alpha_composite(Image.alpha_composite(art,frame),tx);filename=f'{label}-UI排版修复1190.png';out.save(D/filename)
 out.resize((480,720),Image.Resampling.LANCZOS).save(D/f'{tier}-preview480.png')
 x,y=OFFSET;reg=(slice(y,y+1536),slice(x,x+1024));valid=(np.array(mask)[reg]==255)&(np.array(frame.getchannel('A'))[reg]==0)&(np.array(tx.getchannel('A'))[reg]==0)
 changed=int((np.any(np.array(out)[reg]!=np.array(pure),axis=2)&valid).sum());assert changed==0
 unchanged_check='all four newly generated sources; uncovered native illustration pixels preserved'
 edges=np.array(out.getchannel('A'));edgecount=int(np.count_nonzero(edges[0])+np.count_nonzero(edges[-1])+np.count_nonzero(edges[:,0])+np.count_nonzero(edges[:,-1]));assert edgecount==0
 manifest['cards'][tier]={'source':str(src),'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'output':filename,'fields':f,'rows':measured,'advancement':badge,'uncovered_art_native_pixels_checked':int(valid.sum()),'changed_art_native_pixels':changed,'changed_pixels_outside_authorized_UI_regions':unchanged_check,'canvas_edge_nontransparent_pixels':edgecount}
(D/'composition-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
sheet=Image.new('RGB',(1920,775),'#20252a');draw=ImageDraw.Draw(sheet);font=ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',18)
for i,t in enumerate(['iron','bronze','silver','gold']):
 im=Image.open(D/f'{t}-preview480.png');sheet.paste(im,(480*i,0),im)
draw.text((28,730),'魏延四阶 UI 局部排版修复：被动板收短、技能名与 +等级紧凑、字形居中、底部固定向上排。',font=font,fill='white')
draw.text((28,754),'圆章显示一至四阶；技能/等级为草案；'+('已替换准源：'+ '、'.join({'bronze':'青铜','silver':'白银','gold':'黄金'}[t] for t,s in overrides.items() if s)+'。' if any(overrides.values()) else '四张独立生成新原图；非原生4K。'),font=font,fill='#d6c38b')
sheet.save(D/'魏延-四阶UI排版修复总览.png')
# Full native-resolution local-detail contact sheet, no resizing of its crops.
qa=Image.new('RGB',(4*410,670),'#24292d');qd=ImageDraw.Draw(qa)
for i,(t,l) in enumerate([('iron','黑铁'),('bronze','青铜'),('silver','白银'),('gold','黄金')]):
 im=Image.open(D/manifest['cards'][t]['output']).convert('RGBA');crop=im.crop((720,1035,1130,1380));qa.paste(crop,(410*i,28),crop);b=im.crop((45,1485,330,1745));qa.paste(b,(410*i+55,390),b);qd.text((410*i+15,4),l+' · 100% 实际像素',font=font,fill='white')
qa.save(D/'四阶-被动板与圆章-100percent像素QA.png')
(D/'修复说明.txt').write_text('标题保持用户当前名称「魏延」，不由圆章「真」拼接前缀。其余仅改既有 UI 排版，不改材质风格、技能定义或数值。\n既有金属板保留左端帽与右侧直连边，仅缩短中段。\n技能名和 +等级按真实字形边界组成紧凑一组；组内视觉间隔固定为 12 输出像素。\n所有条目共用最低槽位，增加条目从底部向上填充；原有内容顺序保持。\n进阶圆章一二三四是本轮排版草案，以实字形中心居中。\n插画 1024×1536 原生像素以 1:1 合成进 1190×1786；无锐化或缩放。\n具体像素检查见 composition-manifest.json。\n')
print(D)
