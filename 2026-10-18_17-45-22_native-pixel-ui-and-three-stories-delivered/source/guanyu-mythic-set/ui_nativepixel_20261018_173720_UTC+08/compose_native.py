from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import numpy as np,json,hashlib
D=Path(__file__).parent;R=D.parent;U=R/'ui_frame_extension_20261018_173100_UTC+08';size=(1190,1786);offset=(84,145)
sources={'iron':R/'qualitylocalized_20261018_170920_UTC+08/blackiron-pure.png','bronze':R/'pure/bronze-v8-frame-safe-depth-20261018_172023.png','silver':R/'silver-natural-depth_20261018_171734_UTC+08/silver-pure-lettering.png','gold':R/'pure/gold-local-depth-finish-20261018_172405.png'}
labels={'iron':'01-黑铁','bronze':'02-青铜','silver':'03-白银','gold':'04-黄金'}
manifest={'status':'candidate; UI values are demonstration only','canvas':size,'native_art':[1024,1536],'native_art_offset':offset,'art_resampling':'NONE; source pixels pasted at 1:1 before normal edge masking/overlays','frame_resampling':'Original 1024×1536 frame, stars, and mask enlarged with Lanczos; frame is not native higher-resolution art','ui_resampling':'Text drawn at 3072×4608 and reduced once to target canvas; frame-derived UI metal uses original frame detail','original_art_ratio_note':'Original insertion was 881×1321 at72,125; new1190×1786 canvas fits native1024×1536 at84,145; subpixel rounding under1px. No 4K or newly generated art-detail claim.','cards':{}}
for k,path in sources.items():
 pure=Image.open(path).convert('RGBA');assert pure.size==(1024,1536)
 if k=='gold':pure=Image.alpha_composite(pure,Image.open(R/'revision_20261018_163130_UTC+08/刘旗独立字层.png').convert('RGBA'))
 z=Image.new('RGBA',size);z.paste(pure,offset)
 mask=Image.open(R/'art-clip-mask.png').resize(size,Image.Resampling.LANCZOS)
 art=Image.new('RGBA',size);art.paste(z,(0,0),mask)
 mat='blackiron' if k=='iron' else k
 frame=Image.open(R/f'frames/{mat}.png').convert('RGBA').resize(size,Image.Resampling.LANCZOS)
 stars=Image.open(R/f'frames/{mat}-stars-ui.png').convert('RGBA').resize(size,Image.Resampling.LANCZOS)
 base=Image.alpha_composite(Image.alpha_composite(art,frame),stars);base.save(D/f'{labels[k]}-保源像素无UI.png')
 ui=Image.open(U/f'{k}-overlay-3x.png').resize(size,Image.Resampling.LANCZOS);ui.save(D/f'{k}-UI-overlay-1190.png')
 final=Image.alpha_composite(base,ui);final.save(D/f'{labels[k]}-完整UI保源像素候选.png');final.resize((1024,1536),Image.Resampling.LANCZOS).save(D/f'{k}-preview-1024.png');final.resize((480,720),Image.Resampling.LANCZOS).save(D/f'{k}-480.png')
 # Check every unmasked, uncovered pixel in the original native insertion.
 x,y=offset;region=(slice(y,y+1536),slice(x,x+1024));mm=np.array(mask.convert('L'))[region];fa=np.array(frame.getchannel('A'))[region];sa=np.array(stars.getchannel('A'))[region];ua=np.array(ui.getchannel('A'))[region];valid=(mm==255)&(fa==0)&(sa==0)&(ua==0)
 before=np.array(pure);after=np.array(final)[region];bad=np.any(before!=after,axis=2)&valid
 manifest['cards'][k]={'source':str(path),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'checked_uncovered_native_pixels':int(valid.sum()),'changed_pixels_in_checked_region':int(bad.sum()),'output':f'{labels[k]}-完整UI保源像素候选.png'}
 assert bad.sum()==0
(D/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
font='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc';sheet=Image.new('RGB',(1536,670),'#1c1d20');d=ImageDraw.Draw(sheet)
for i,k in enumerate(sources):
 img=Image.open(D/f'{k}-480.png').resize((384,576),Image.Resampling.LANCZOS);sheet.paste(img,(i*384,38),img);d.text((i*384+192,18),labels[k][3:],font=ImageFont.truetype(font,22),fill='#eadfbf',anchor='mm')
d.text((768,628),'1190×1786 保源像素合成 · 原插画1024×1536直接入框，框体放大插值',font=ImageFont.truetype(font,18),fill='#ccc',anchor='mm');d.text((768,653),'完整UI示意：名称、等级、进阶、兵种、技能数量均未定案',font=ImageFont.truetype(font,18),fill='#ccc',anchor='mm');sheet.save(D/'四阶关羽-框延伸UI保源像素总览.png')
print(json.dumps(manifest,ensure_ascii=False,indent=2))
