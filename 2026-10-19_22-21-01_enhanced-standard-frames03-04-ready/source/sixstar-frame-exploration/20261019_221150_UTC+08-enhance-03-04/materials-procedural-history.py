from pathlib import Path
from PIL import Image,ImageDraw,ImageFilter
import numpy as np,json,hashlib,shutil
from scipy import ndimage as ndi
P=Path(__file__).resolve().parent
S=Path('/workspace/scratch/3f82ff2b3f81/advanced-card-ui/2026-10-19_13-57-00_UTC+08/frame-6star.png')
im=Image.open(S).convert('RGBA');a=np.array(im);rgb=a[:,:,:3].astype(float)/255;r,g,b=np.moveaxis(rgb,-1,0);h,w=a.shape[:2];yy,xx=np.mgrid[:h,:w]
raw=((np.minimum(r,b)-g)>.035)&(a[:,:,3]>128)
# Fill only tiny isolated bright blemishes; large stars/ornaments remain untouched.
filled=ndi.binary_fill_holes(raw);holes=filled&~raw;lab,n=ndi.label(holes);counts=np.bincount(lab.ravel());ids=np.where((counts<1100)&(counts>0))[0];ids=ids[ids!=0];panel=raw|np.isin(lab,ids)
panel=ndi.binary_closing(panel,iterations=2)&(a[:,:,3]>128)
weight=ndi.gaussian_filter(panel.astype(float),.8)
dist=ndi.distance_transform_edt(panel);height=np.minimum(dist/10,1);gy,gx=np.gradient(ndi.gaussian_filter(height,1.1));bevel=np.clip(1+4.5*(-gx-gy),.35,1.55)
edgeLight=np.clip(.299*r+.587*g+.114*b,0,1)
# Smooth broad light bands and coherent polished bevels. No random/noise textures.
wide=np.exp(-((xx-yy*.24-140)/180)**2);sweep=np.exp(-((xx+yy*.17-970)/75)**2)
light=np.clip(.42+.32*wide+.26*sweep+.08*np.cos(yy/500),.15,1)
palettes=[('03','象牙金釉·御铸',[(118,107,75),(222,219,196),(255,255,246)],[(55,29,8),(196,137,44),(255,249,205)]),('04','赤铜鎏银·天锻',[(48,12,8),(143,57,29),(250,178,119)],[(30,43,53),(174,197,209),(255,255,255)])]
def ramp(v,stops):return np.stack([np.interp(v,[0,.56,1],[c[k] for c in stops]) for k in range(3)],-1)
# Shallow geometric guilloche, confined to existing plate interiors; continuous lines, never dots.
engr=Image.new('L',(w,h));d=ImageDraw.Draw(engr)
for x0,y0,x1,y1 in [(420,78,975,132),(90,1090,163,1475),(405,1680,945,1728)]:
 if x1-x0>y1-y0:
  cy=(y0+y1)/2
  for x in range(x0,x1,70):d.line([(x,cy),(x+18,cy-12),(x+38,cy),(x+18,cy+12),(x,cy)],fill=170,width=2)
 else:
  cx=(x0+x1)/2
  for y in range(y0,y1,85):d.line([(cx,y),(cx-15,y+23),(cx,y+47),(cx+15,y+23),(cx,y)],fill=170,width=2)
etch=np.array(engr)/255*(dist>10)
records=[]
for ident,name,base,edge in palettes:
 field=ramp(light,base)*bevel[:,:,None]
 # Inner lip adds depth around every panel, ring and star socket without moving them.
 lip=np.exp(-((dist-5)/1.8)**2)*panel*.45
 field=field*(1-lip[:,:,None])+np.array(edge[-1])[None,None,:]*lip[:,:,None]
 field*=1-etch[:,:,None]*.18
 embossed=np.roll(etch,1,axis=0)*.16;field+=embossed[:,:,None]*np.array(edge[-1])[None,None,:]
 metal=ramp(np.clip(edgeLight**.66,0,1),edge)
 out=metal*(1-weight[:,:,None])+field*weight[:,:,None]
 arr=np.dstack([np.clip(out,0,255).astype('uint8'),a[:,:,3]]);folder=P/(ident+'-'+name);folder.mkdir(exist_ok=True);Image.fromarray(arr).save(folder/'frame-6star.png')
 records.append({'id':ident,'name':name,'frame':str(folder/'frame-6star.png'),'material_base':base,'material_edge':edge,'alpha_identical':bool(np.array_equal(arr[:,:,3],a[:,:,3])),'bevel_width_px':10,'tiny_blemish_fill_max_area':1100,'reflection':'continuous wide bands; no random particles','engraving':'subtle continuous geometric inlay confined to original plates'})
shutil.copy2(S,P/'reference-standard-sixstar-frame.png');(P/'material-config.json').write_text(json.dumps(records,ensure_ascii=False,indent=2))
