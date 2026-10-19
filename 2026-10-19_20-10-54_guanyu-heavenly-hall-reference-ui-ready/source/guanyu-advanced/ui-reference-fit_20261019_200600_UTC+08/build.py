from pathlib import Path
from PIL import Image,ImageFilter
import numpy as np
from scipy import ndimage
P=Path(__file__).resolve().parent;R=P.parent
src=Image.open(R/'ui-calligraphy_20261019_191150_UTC+08/user-original-gold-reference.png').convert('RGB');crop=src.crop((65,860,169,947));a=np.array(crop);sel=(a[:,:,0]>190)&(a[:,:,1]>175)&(a[:,:,2]>125)&(a[:,:,0]-a[:,:,2]<100)
lab,n=ndimage.label(sel);sizes=np.bincount(lab.ravel());sizes[0]=0;mask=lab==sizes.argmax();mask=ndimage.binary_fill_holes(mask);m=Image.fromarray((mask*255).astype('uint8'));m=m.crop(m.getbbox());m=m.resize((720,620),Image.Resampling.LANCZOS).filter(ImageFilter.GaussianBlur(7.0));m=m.point(lambda x:255 if x>=120 else 0).filter(ImageFilter.GaussianBlur(.7));m.save(P/'reference-tian-silhouette.png')
# Restrained warm ivory-gold metal face, broad smooth highlight rather than noisy gold filter.
a=np.array(m)/255;dist=ndimage.distance_transform_edt(a>.5);h=np.minimum(dist/9,1);dy,dx=np.gradient(ndimage.gaussian_filter(h,1.6));light=np.clip(1.-1.0*dx-1.3*dy,.65,1.13);yy=np.arange(620)[:,None]/620
colors=np.stack([np.broadcast_to(255-15*yy,a.shape),np.broadcast_to(248-34*yy,a.shape),np.broadcast_to(218-50*yy,a.shape)],axis=-1);rgb=np.clip(colors*light[:,:,None],0,255).astype('uint8')
canvas=Image.new('RGBA',(760,670));border=m.filter(ImageFilter.MaxFilter(23));canvas.paste((47,27,15,255),(18,25),border);canvas.paste((130,82,29,255),(23,31),m);canvas.alpha_composite(Image.fromarray(np.dstack((rgb,(a*255).astype('uint8')))),(18,20));canvas.thumbnail((170,150),Image.Resampling.LANCZOS);out=Image.new('RGBA',(180,160));out.alpha_composite(canvas,((180-canvas.width)//2,(160-canvas.height)//2));out.save(P/'tian-metal-calligraphy.png')
# Source spear: reference occupies ~half its roundel height. Use crisp 94px high emblem in current ~160px roundel, with transparent margins.
s=Image.open(R/'ui-metal-assets_20261019_192445_UTC+08/spearhead-source.png').convert('RGBA');s=s.crop(s.getchannel('A').getbbox());s.thumbnail((72*4,94*4),Image.Resampling.LANCZOS);out=Image.new('RGBA',(120*4,120*4));edge=s.getchannel('A').filter(ImageFilter.MaxFilter(15));xy=((480-s.width)//2,(480-s.height)//2);out.paste((42,34,25,255),xy,edge);out.alpha_composite(s,xy);out.resize((120,120),Image.Resampling.LANCZOS).save(P/'spearhead.png')
old=R/'ui-verified-glyph_20261019_195200_UTC+08';import shutil
shutil.copy2(old/'fenghou-metal.png',P/'fenghou-metal.png');text=(old/'render.py').read_text();text=text.replace("layer.alpha_composite(badge,(round(155*SX-75),round(1384*SY-72.5)))","layer.alpha_composite(badge,(round(155*SX-badge.width/2),round(1384*SY-badge.height/2)))").replace('round(1411*SY-70)','round(1411*SY-60)');(P/'render.py').write_text(text)
