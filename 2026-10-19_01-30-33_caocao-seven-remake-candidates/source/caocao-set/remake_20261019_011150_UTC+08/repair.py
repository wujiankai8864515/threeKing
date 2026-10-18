from pathlib import Path
from PIL import Image,ImageDraw,ImageFilter
import shutil,json,numpy as np
D=Path(__file__).parent
jobs=[('card03','exec-f5900242-b91a-4945-ad01-dd74b17aba6a.png',[(0,0),(1024,0),(1024,330),(710,350),(690,280),(645,275),(630,200),(505,190),(470,285),(480,385),(300,400),(0,325)]),('card04','exec-d708036c-7824-4e11-be15-a08b00af6aee.png',[(365,0),(1024,0),(1024,490),(790,470),(700,395),(600,385),(590,300),(535,260),(520,185),(375,180)]),('bio02','exec-d5203a92-f01b-4247-a391-e90911c758ab.png',[(0,150),(245,150),(250,390),(0,390)])]
log=[]
for key,fn,poly in jobs:
 src=D/'raw'/f'{key}.png';shutil.copy2(src,D/'failures'/f'{key}-before-local-fix.png')
 fix=Image.open(Path('generated_images')/fn).convert('RGB');fix.save(D/'raw'/f'{key}-imagegen-repair.png');orig=Image.open(src).convert('RGB')
 mask=Image.new('L',orig.size);ImageDraw.Draw(mask).polygon(poly,fill=255);mask=mask.filter(ImageFilter.GaussianBlur(3));mask.save(D/'qa'/f'{key}-repair-mask.png')
 out=Image.composite(fix,orig,mask);out.save(src)
 a=np.array(orig);b=np.array(out);outside=np.array(mask)==0
 log.append({'asset':key,'repair_source':fn,'outside_mask_changed_pixels':int(np.any(a!=b,axis=2)[outside].sum()),'scope':'creature only' if key!='bio02' else 'remove anachronistic background figure'})
(D/'qa/repair-log.json').write_text(json.dumps(log,indent=2))
