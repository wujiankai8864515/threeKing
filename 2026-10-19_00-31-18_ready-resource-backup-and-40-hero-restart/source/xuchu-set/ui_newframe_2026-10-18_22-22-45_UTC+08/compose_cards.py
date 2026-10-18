from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,subprocess,hashlib,numpy as np
D=Path(__file__).parent;R=D.parent;size=(1190,1786);offset=(84,145)
sm=json.loads((D/'source-map.json').read_text())
poly=[(108,125),(868,125),(868,606),(945,684),(945,1430),(154,1430),(154,942),(77,852),(77,423),(108,385)]
mask=Image.new('L',(2380,3572));ImageDraw.Draw(mask).polygon([(round(x*2380/1024),round(y*3572/1536)) for x,y in poly],fill=255);mask=mask.resize(size,Image.Resampling.LANCZOS);mask.save(D/'art-native-slot-mask.png')
# Independent text generator fields; screen artwork untouched.
base=(D/'build_text.py').read_text();prefix=base[:base.index("(D/'text-config.json')")];func=base[base.index("head="):base.index("txt(fields['country']")]
manifest={'canvas':size,'illustration_native_size':[1024,1536],'illustration_resampling':'none: pasted 1:1 at84,145','frame_native_size':[1024,1536],'frame_resampling':'Lanczos enlargement to1190x1786; newly generated raster, not vector or true higher-resolution','text':'SVG rasterized directly1190x1786, independent name and level fields','values':'All UI values and counts are examples, not final progression mechanics','cards':{}}
for tier,label,num,level in [('iron','01-黑铁',1,'+1'),('bronze','02-青铜',1,'+1'),('silver','03-白银',2,'+2'),('gold','04-黄金',3,'+2')]:
 fields=json.loads((D/'ui-config.json').read_text())[tier];ns={'fields':fields};exec('import html\n'+func,ns);a=ns['a'];txt=ns['txt'];a[0]=a[0].replace('width="2048" height="3072"','width="1190" height="1786"');a.append('<defs><radialGradient id="shuGreen" cx="36%" cy="28%" r="85%"><stop stop-color="#285c85"/><stop offset="1" stop-color="#071c35"/></radialGradient></defs><circle cx="144" cy="132" r="43" fill="url(#shuGreen)"/>');txt(fields['country'],144,132,62);txt(fields['title'],630,90,45);txt('LV',909,105,26,'sans');txt(fields['level'],909,148,48,'sans');txt(fields['advancement'],148,1385,78)
 for y,sk in zip([962,1048,1132][-num:],fields['skills']):txt(sk['name'],730,y+90 if tier=='bronze' else y,min(38,100/len(sk['name'])),'sans','start');txt(sk['level'],903,y+90 if tier=='bronze' else y,35,'sans','end')
 troop=base[base.index("a.append('<g"):base.index("(D/'text-overlay.svg')")];exec(troop,ns)
 svg=D/f'{tier}-text-overlay.svg';svg.write_text(''.join(a));textpng=D/f'{tier}-text-overlay-1190.png';subprocess.run(['inkscape',str(svg),'--export-filename='+str(textpng)],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
 sk='blackiron' if tier=='iron' else tier;src=Path(sm[sk]['path']);pure=Image.open(src).convert('RGBA');assert pure.size==(1024,1536)
 canvas=Image.new('RGBA',size);canvas.paste(pure,offset);art=Image.new('RGBA',size);art.paste(canvas,(0,0),mask)
 frame=Image.open(D/('silver-empty-cleanalpha-1024.png' if tier=='silver' else f'{tier}-empty-generated-1024.png')).convert('RGBA').resize(size,Image.Resampling.LANCZOS);tx=Image.open(textpng).convert('RGBA');out=Image.alpha_composite(Image.alpha_composite(art,frame),tx);out.save(D/f'{label}-新框完整UI候选1190.png');out.resize((480,720),Image.Resampling.LANCZOS).save(D/f'{tier}-complete-480.png')
 x,y=offset;reg=(slice(y,y+1536),slice(x,x+1024));valid=(np.array(mask)[reg]==255)&(np.array(frame.getchannel('A'))[reg]==0)&(np.array(tx.getchannel('A'))[reg]==0);changed=(np.any(np.array(out)[reg]!=np.array(pure),axis=2)&valid).sum();assert changed==0
 manifest['cards'][tier]={'source':str(src),'source_status':sm[sk]['status'],'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'uncovered_native_pixels_checked':int(valid.sum()),'changed_native_pixels':int(changed),'fields':fields,'output':f'{label}-新框完整UI候选1190.png'}
(D/'composition-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2));sheet=Image.new('RGB',(1920,775),'#20252a');draw=ImageDraw.Draw(sheet);f=ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',18)
for i,t in enumerate(['iron','bronze','silver','gold']):im=Image.open(D/f'{t}-complete-480.png');sheet.paste(im,(480*i,0),im)
draw.text((30,728),'1190×1786画布；插画1024×1536原像素入框，框原生1024×1536放大插值，文字独立原生渲染。UI数值仅示意。',font=f,fill='white');draw.text((30,751),'角色插画技术检查通过；框覆盖待终审，技能拟名未定案，数值与条数仅UI示意。',font=f,fill='#eec68a');sheet.save(D/'四阶新框完整UI-候选总览.png')
print('complete')