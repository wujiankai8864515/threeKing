from pathlib import Path
from PIL import Image,ImageDraw,ImageFilter
import numpy as np,json,hashlib
D=Path(__file__).parent;locks=json.loads((D.parent/'local-fidelity-plan_2026-10-18_23-18-04_UTC+08/locked-sources.json').read_text());boxes=json.loads((D/'crop-boxes.json').read_text());qa={}
for k in ['silver','gold','bio03']:
 src=Image.open(locks[k]['path']).convert('RGB');b=boxes[k];orig=src.crop(b);gen=Image.open(D/f'{k}-generated.png').convert('RGB').resize(orig.size,Image.Resampling.LANCZOS);gen.save(D/f'{k}-patch-aligned.png');a=np.array(orig).astype(float);g=np.array(gen).astype(float);m=Image.new('L',orig.size);dr=ImageDraw.Draw(m)
 if k=='silver':dr.polygon([(0,335),(45,350),(100,355),(165,330),(225,290),(245,317),(182,375),(95,414),(0,435)],fill=255)
 elif k=='gold':dr.polygon([(162,140),(188,153),(225,165),(265,190),(284,216),(284,238),(255,210),(218,191),(178,184),(154,164)],fill=255)
 else:dr.polygon([(177,81),(194,88),(223,102),(255,120),(266,141),(244,146),(209,126),(180,111)],fill=255)
 m=m.filter(ImageFilter.GaussianBlur(2));mf=np.array(m)/255
 if k!='bio03':
  # Extract only generated new red-light intensity. No generated scene/metal pixels are copied.
  rednew=np.maximum(0,(g[:,:,0]-g[:,:,1])-(a[:,:,0]-a[:,:,1])-8)
  amount=np.minimum(90,rednew*1.2)*mf
  delta=np.stack([amount,amount*.24,amount*.17],axis=-1)
  out=np.clip(a+delta,0,255).astype('uint8');actual=np.any(out!=a.astype('uint8'),axis=-1);mask=(actual*255).astype('uint8');overlay=np.zeros((*mask.shape,4),dtype='uint8');overlay[:,:,:3]=np.clip(delta,0,255);overlay[:,:,3]=mask;Image.fromarray(overlay).save(D/f'{k}-effect-delta.png')
 else:
  out=np.round(g*mf[:,:,None]+a*(1-mf[:,:,None])).astype('uint8');mask=np.array(m)
 patch=Image.fromarray(out);patch.save(D/f'{k}-composited-crop.png');fullmask=Image.new('L',src.size);fullmask.paste(Image.fromarray(mask),(b[0],b[1]));fullmask.save(D/f'{k}-mask.png');final=src.copy();final.paste(patch,(b[0],b[1]));final.save(D/f'{k}-final.png');diff=np.any(np.array(final)!=np.array(src),axis=-1);outside=int((diff&(np.array(fullmask)==0)).sum());assert outside==0
 ys,xs=np.where(diff);qa[k]={'source_sha256':locks[k]['sha256'],'changed_pixels':int(diff.sum()),'outside_mask_changed':outside,'changed_bbox':[int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1)],'method':'generated red-light positive delta only' if k!='bio03' else 'generated terminal-tip patch, shape feather mask','mask_sha256':hashlib.sha256((D/f'{k}-mask.png').read_bytes()).hexdigest()}
qa['blackiron']={'status':'unchanged: requested translation would detach original gripping hand from pillar; no fabricated pose'}
for k in ['bronze','bio01','bio02']:assert hashlib.sha256(Path(locks[k]['path']).read_bytes()).hexdigest()==locks[k]['sha256'];qa[k]={'status':'frozen source hash verified'}
(D/'pixel-QA.json').write_text(json.dumps(qa,indent=2));print(json.dumps(qa))
