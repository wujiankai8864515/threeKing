from pathlib import Path
from PIL import Image,ImageFilter
import numpy as np,json,hashlib,shutil
P=Path(__file__).resolve().parent
S=Path('/workspace/scratch/3f82ff2b3f81/advanced-card-ui/2026-10-19_13-57-00_UTC+08/frame-6star.png')
im=Image.open(S).convert('RGBA');a=np.array(im);rgb=a[:,:,:3].astype(float)/255;r,g,b=np.moveaxis(rgb,-1,0);h,w=a.shape[:2];yy,xx=np.mgrid[:h,:w]
# Preserve exact native alpha and sculpted original metal architecture. Replace only material.
purple=np.clip((np.minimum(r,b)-g-.015)*10,0,1)
purple=np.maximum(purple, np.clip((b-g-.04)*6,0,1)*(r>g))
purple=np.array(Image.fromarray((purple*255).astype('uint8')).filter(ImageFilter.GaussianBlur(.65)))/255
lum=.299*r+.587*g+.114*b
# Original structural engraving stays; crystal facet lighting is replaced by broad satin reflections.
broad=np.clip(.48+.23*np.sin(xx/120+yy/520)+.13*np.cos(yy/240)+.10*np.sin(xx/33),.12,.95)
palettes=[
('01','白金鎏金',[(70,79,84),(189,201,204),(255,255,250)],[(67,43,16),(207,157,73),(255,244,197)]),
('02','玄钛银刃',[(8,15,23),(43,60,74),(113,139,152)],[(34,48,61),(172,195,207),(250,255,255)]),
('03','象牙金釉',[(110,100,78),(220,217,193),(255,255,236)],[(61,39,15),(191,142,61),(255,240,174)]),
('04','赤铜鎏银',[(55,20,15),(169,76,43),(250,174,111)],[(50,48,45),(180,183,180),(255,255,240)]),
('05','墨玉铂金',[(5,23,24),(22,74,66),(86,151,126)],[(45,57,58),(182,204,198),(250,255,249)])]
def ramp(v,stops):
 return np.stack([np.interp(v,[0,.58,1],[c[k] for c in stops]) for k in range(3)],-1)
records=[]
for ident,name,base,edge in palettes:
 reflection=np.exp(-(((xx-yy*.28+200)%950-475)/90)**2)*.48
 field=ramp(broad,base);field=field*(1-reflection[:,:,None])+np.array(base[-1])[None,None,:]*reflection[:,:,None]
 metal=ramp(np.clip(lum**.8,0,1),edge);out=metal*(1-purple[:,:,None])+field*purple[:,:,None]
 arr=np.dstack([np.clip(out,0,255).astype('uint8'),a[:,:,3]]);folder=P/(ident+'-'+name);folder.mkdir(exist_ok=True);Image.fromarray(arr).save(folder/'frame-6star.png')
 records.append({'id':ident,'name':name,'frame':str(folder/'frame-6star.png'),'material_base':base,'material_edge':edge,'alpha_identical':bool(np.array_equal(arr[:,:,3],a[:,:,3]))})
shutil.copy2(S,P/'reference-standard-sixstar-frame.png');(P/'material-config.json').write_text(json.dumps(records,ensure_ascii=False,indent=2))
print(P)
