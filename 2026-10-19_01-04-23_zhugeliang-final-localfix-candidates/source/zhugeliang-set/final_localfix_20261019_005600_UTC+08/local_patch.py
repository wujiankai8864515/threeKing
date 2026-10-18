from PIL import Image,ImageDraw,ImageFilter
from pathlib import Path
import numpy as np,json,shutil
D=Path(__file__).resolve().parent;P=D.parent/'full_remake_20261019_003250_UTC+08'
# Preserve all old sources for consistent rebuild paths; unchanged ones copied byte-for-byte.
for f in (P/'raw').glob('*.png'):shutil.copy2(f,D/'raw'/f.name)
checks=[]
for n,box in [('card03',(560,60,810,420)),('card04',(700,180,880,420))]:
 a=Image.open(P/'raw'/f'{n}-safe.png').convert('RGB');b=Image.open(D/'raw'/f'{n}-generated-edit.png').convert('RGB')
 mask=Image.new('L',a.size);dr=ImageDraw.Draw(mask);dr.rectangle(box,fill=255);mask=mask.filter(ImageFilter.GaussianBlur(10))
 # Entire lightning area sky only; no face, hands or costume enters mask.
 out=Image.composite(b,a,mask);out.save(D/'raw'/f'{n}-safe.png');mask.save(D/'qa'/f'{n}-edit-mask.png')
 ar=np.array(a);o=np.array(out);m=np.array(mask);checks.append({'asset':n,'outside_mask_changed':int(np.any(ar!=o,2)[m==0].sum()),'mask_box':box})
a=Image.open(P/'raw/bio01.png').convert('RGB');b=Image.open(D/'raw/bio01-generated-edit.png').convert('RGB')
mask=Image.new('L',a.size);dr=ImageDraw.Draw(mask)
# Clothing silhouette only: left shoulder/sleeve, right shoulder/sleeve and ivory lapels.
dr.polygon([(1050,680),(1070,587),(1120,489),(1193,418),(1284,383),(1337,402),(1280,455),(1240,500),(1328,530),(1365,563),(1374,499),(1410,480),(1449,385),(1535,403),(1535,680)],fill=255)
dr.polygon([(1220,450),(1295,420),(1310,450),(1280,515),(1220,520)],fill=255)
mask=mask.filter(ImageFilter.GaussianBlur(2))
out=Image.composite(b,a,mask);out.save(D/'raw/bio01.png');mask.save(D/'qa/bio01-edit-mask.png')
checks.append({'asset':'bio01','outside_mask_changed':int(np.any(np.array(a)!=np.array(out),2)[np.array(mask)==0].sum()),'scope':'Liu Bei clothing only; Zhuge entire figure, map and fan preserved'})
(D/'qa/local-preservation-checks.json').write_text(json.dumps(checks,indent=2))
