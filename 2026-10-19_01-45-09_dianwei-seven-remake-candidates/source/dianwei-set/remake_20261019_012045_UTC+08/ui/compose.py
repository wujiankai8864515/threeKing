from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,hashlib,shutil,subprocess
D=Path(__file__).resolve().parent.parent
B=Path('zhangfei-set/local-patches_2026-10-18_23-39-10_UTC+08/ui')
SZ=(1190,1786); SX=1190/1024;SY=1786/1536
F='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
def center(draw,text,x,y,size,fill='#fff7df'):
 f=ImageFont.truetype(F,size); b=draw.textbbox((0,0),text,font=f,stroke_width=0)
 draw.text((round(x-(b[0]+b[2])/2),round(y-(b[1]+b[3])/2)),text,font=f,fill=fill,stroke_width=2,stroke_fill='#302310')
manifest={'hero':'典韦','status':'all new candidates awaiting user review','native_cards':[1024,1536],'native_stories':[1536,1024],'UI_canvas':SZ,'art_scale':'1:1 at84,145; no upscale','beast':'上古巨巫祖影，原创美术设定，不是典籍血统或族群','skills_draft':{'护主':'为选定近旁一名友军承接下一次来袭的一部分伤害','巨躯':'最大生命提高','固骨':'承接给自己的伤害降低','拒关':'护卫期间受到的击退距离减少'},'slot_counts':[1,1,2,3],'cards':{},'stories':{}}
mask=Image.open(B/'art-native-slot-mask.png').convert('L');mask.save(D/'ui/art-mask.png')
for i,t in enumerate(['iron','bronze','silver','gold'],1):
 frame=Image.open(B/f'{t}-frame-layout-1190.png').convert('RGBA'); frame.save(D/f'ui/{t}-frame.png')
 tx=Image.new('RGBA',SZ);d=ImageDraw.Draw(tx)
 d.ellipse((144*SX-49,132*SY-49,144*SX+49,132*SY+49),fill='#153d67');center(d,'魏',144*SX,132*SY,65)
 center(d,'典韦',630*SX,90*SY,52);center(d,'LV',909*SX,105*SY,29);center(d,'1',909*SX,148*SY,52)
 center(d,['初','进','精','极'][i-1],155.5*SX,1384.5*SY,78)
 # Independent vector troop icon, no text substitution.
 iconpath=('M 0 -35 L 8 -20 L 4 -10 L 4 34 L -4 34 L -4 -10 L -8 -20 Z M -30 -10 L -14 -19 L -7 -10 L -7 20 L -18 30 L -30 20 Z' if True else 'M -28 30 L -24 7 L -15 -7 L -10 -25 L -2 -35 L 5 -22 L 19 -13 L 28 1 L 22 9 L 8 5 L 2 15 L 10 29 Z M -27 31 L 24 31 L 24 37 L -27 37 Z')
 svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="1190" height="1786"><g transform="translate({900*SX} {1424*SY})" fill="#fff7df" stroke="#302310" stroke-width="2.7"><path d="{iconpath}"/></g></svg>'
 sp=D/f'ui/{t}-troop-icon.svg';sp.write_text(svg);ip=D/f'ui/{t}-troop-icon.png'
 subprocess.run(['inkscape',str(sp),'--export-filename='+str(ip)],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
 tx.alpha_composite(Image.open(ip).convert('RGBA'))
 names=[['巨躯'],['巨躯'],['巨躯','固骨'],['巨躯','固骨','拒关']][i-1]
 for cy,n in zip([961,1045,1129][-len(names):],names):center(d,n+' +'+str(1 if i<3 else 2),980.8,cy*SY,43)
 tx.save(D/f'ui/{t}-text.png')
 art=Image.new('RGBA',SZ);raw=Image.open(D/f'clean/card0{i}.png').convert('RGBA');art.paste(raw,(84,145));clipped=Image.new('RGBA',SZ);clipped.paste(art,(0,0),mask)
 out=Image.alpha_composite(Image.alpha_composite(clipped,frame),tx);fn=f'card0{i}-{t}-典韦.png';out.save(D/'candidates'/fn)
 manifest['cards'][t]={'raw':f'clean/card0{i}.png','output':'candidates/'+fn,'sha256':hashlib.sha256((D/'candidates'/fn).read_bytes()).hexdigest(),'skills':names}
 # focused face/weapon/hands inspection crops are from native originals
 raw.crop((150,100,950,800)).save(D/f'qa/card0{i}-face-hands.png')
for i,title in enumerate(['夏侯引荐','再近五步','失戟赴门'],1):
 src=D/f'clean/bio0{i}.png'; fn=f'bio0{i}-{title}.png';shutil.copy2(src,D/'candidates'/fn)
 manifest['stories'][f'bio0{i}']={'raw':str(src.relative_to(D)),'output':'candidates/'+fn,'target_card':i+1,'event_chapter':[10,11,16][i-1]}
(D/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
sheet=Image.new('RGB',(1920,1310),'#1b2229');dr=ImageDraw.Draw(sheet)
for i,c in enumerate(manifest['cards'].values()):
 im=Image.open(D/c['output']);im.thumbnail((465,698));sheet.paste(im,(i*480+8,30),im);center(dr,['黑铁 · 逐鹿过涧','青铜 · 一手定旗','白银 · 五步飞戟','黄金 · 宛门不退'][i],i*480+240,751,24)
for i,c in enumerate(manifest['stories'].values()):
 im=Image.open(D/c['output']).convert('RGB');im.thumbnail((624,416));sheet.paste(im,(i*640+8,790));center(dr,['夏侯引荐 → 青铜','再近五步 → 白银','失戟赴门 → 黄金'][i],i*640+320,1240,25)
center(dr,'典韦 · 四阶三传记新候选｜巨巫祖影为原创神话演绎，技能与等级仅提案',960,1280,24)
sheet.save(D/'candidates/典韦-七图总览.png')
print('composed')
