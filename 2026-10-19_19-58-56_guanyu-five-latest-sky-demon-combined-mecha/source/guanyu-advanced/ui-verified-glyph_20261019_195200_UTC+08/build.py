from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageFilter
import numpy as np
from scipy.ndimage import distance_transform_edt, gaussian_filter
import shutil
P=Path(__file__).resolve().parent;old=P.parent/'ui-refined_20261019_194245_UTC+08';S=4
font='/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc'
def glyph(text):
 mask=Image.new('L',(600,580));d=ImageDraw.Draw(mask);f=ImageFont.truetype(font,500 if len(text)==1 else 245);b=d.textbbox((0,0),text,font=f);d.text(((600-(b[2]-b[0]))/2-b[0],(580-(b[3]-b[1]))/2-b[1]),text,font=f,fill=255)
 mask.save(P/(text+'-verified-font-mask.png'))
 a=np.array(mask)/255;dist=distance_transform_edt(a>0);height=np.minimum(dist/10,1);dy,dx=np.gradient(gaussian_filter(height,1));light=np.clip(.95-2.4*dx-3.1*dy,.15,1.3);yy=np.arange(580)[:,None]/580
 metal=np.stack([np.broadcast_to(210+35*np.cos(yy*8),a.shape),np.broadcast_to(165+45*np.cos(yy*8),a.shape),np.broadcast_to(73+48*np.cos(yy*8),a.shape)],axis=-1)*light[:,:,None];metal=np.clip(metal,0,255).astype('uint8')
 canvas=Image.new('RGBA',(600,580));outline=mask.filter(ImageFilter.MaxFilter(17));canvas.paste((46,32,14,255),(0,0),outline)
 canvas.paste((86,55,20,255),(5,9),mask);face=Image.fromarray(np.dstack((metal,(a*255).astype('uint8'))));canvas.alpha_composite(face);canvas.resize((150,145),Image.Resampling.LANCZOS).save(P/('tian-metal-calligraphy.png' if len(text)==1 else 'fenghou-metal.png'))
glyph('天');glyph('封侯')
# Transparent spear: preserve generated silhouette, increase scale and intrinsic dark steel edge, never paint a background disk.
src=Image.open(P.parent/'ui-metal-assets_20261019_192445_UTC+08/spearhead-source.png').convert('RGBA');src=src.crop(src.getchannel('A').getbbox());src.thumbnail((100*4,130*4));can=Image.new('RGBA',(120*4,140*4));a=src.getchannel('A');edge=a.filter(ImageFilter.MaxFilter(15));can.paste((36,42,52,255),((480-src.width)//2,(560-src.height)//2),edge);can.alpha_composite(src,((480-src.width)//2,(560-src.height)//2));can.resize((120,140),Image.Resampling.LANCZOS).save(P/'spearhead.png')
s=(old/'render.py').read_text().replace('round(1411*SY-57.5)','round(1411*SY-70)');(P/'render.py').write_text(s)
