from PIL import Image,ImageDraw,ImageFont,ImageFilter
from pathlib import Path
import numpy as np,json
p=Path(__file__).parent;r=p.parent
im=Image.open(p/'silver-blank-plaque-pure.png').convert('RGBA')
plate=Image.new('RGBA',(800,240),(0,0,0,0));d=ImageDraw.Draw(plate)
d.text((400,116),'汜水關',font=ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc',172,index=2),fill=(198,158,101,215),anchor='mm')
xy=[(744,544),(890,503),(901,550),(750,590)];uv=[(0,0),(800,0),(800,240),(0,240)]
A=[];b=[]
for (x,y),(u,v) in zip(xy,uv):
 A += [[x,y,1,0,0,0,-u*x,-u*y],[0,0,0,x,y,1,-v*x,-v*y]];b += [u,v]
layer=plate.transform(im.size,Image.Transform.PERSPECTIVE,np.linalg.solve(A,b),Image.Resampling.BICUBIC)
# Subpixel edge softness on lettering ONLY, not on source art.
layer=layer.filter(ImageFilter.GaussianBlur(.38));layer.save(p/'silver-transparent-lettering.png')
a=Image.alpha_composite(im,layer);a.save(p/'silver-pure-lettering.png');a.crop((725,475,925,615)).resize((800,560)).save(p/'plaque-QA.png')
a=a.resize((881,1321),Image.Resampling.LANCZOS);z=Image.new('RGBA',(1024,1536));z.paste(a,(72,125));b=Image.new('RGBA',z.size);b.paste(z,(0,0),Image.open(r/'art-clip-mask.png'))
Image.alpha_composite(Image.alpha_composite(b,Image.open(r/'frames/silver.png')),Image.open(r/'frames/silver-stars-ui.png')).save(p/'03-白银·关前扬威.png')
json.dump({'source':'pure/silver-qualityhierarchy-20261018_170456.png','edit':'transparent lettering only; no opaque plaque fill','text':'汜水關','letter_alpha':215,'letter_edge_softness_px':.38,'source_art_filters':'none','frames':'unchanged','status':'pending root QA'},open(p/'manifest.json','w'),ensure_ascii=False,indent=2)
