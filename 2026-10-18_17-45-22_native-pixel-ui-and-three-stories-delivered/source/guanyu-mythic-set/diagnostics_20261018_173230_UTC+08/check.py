from PIL import Image
from pathlib import Path
import numpy as np,json
r=Path(__file__).resolve().parent.parent;o=Path(__file__).parent;u=r/'ui_display_20261018_171500_UTC+08'
sources=json.load(open(u/'sources.json'))
pures={'iron':r/'qualitylocalized_20261018_170920_UTC+08/blackiron-pure.png','bronze':r/'pure/bronze-v8-frame-safe-depth-20261018_172023.png','silver':r/'silver-natural-depth_20261018_171734_UTC+08/silver-pure-lettering.png','gold':r/'pure/gold-local-depth-finish-20261018_172405.png'}
names={'iron':'01-黑铁','bronze':'02-青铜','silver':'03-白银','gold':'04-黄金'}
boxes={'iron':(400,320,590,510),'bronze':(540,310,720,490),'silver':(500,430,680,610),'gold':(500,180,680,360)}
mask=np.array(Image.open(r/'art-clip-mask.png').convert('L'));out={}
for k,s in sources.items():
 a=Image.open(pures[k]).convert('RGBA');b=Image.open(s).convert('RGBA');c=Image.open(u/(names[k]+'-完整UI示意.png')).convert('RGBA');ov=Image.open(u/(k+'-overlay.png')).convert('RGBA')
 arrb=np.array(b);arrc=np.array(c);zero=np.array(ov)[:,:,3]==0;diff=np.any(arrb!=arrc,axis=2)
 box=boxes[k];a.crop(box).save(o/(k+'-pure-face-100.png'))
 cb=(round(72+box[0]*881/1024),round(125+box[1]*1321/1536),round(72+box[2]*881/1024),round(125+box[3]*1321/1536))
 b.crop(cb).save(o/(k+'-card-face-100.png'));c.crop(cb).save(o/(k+'-ui-face-100.png'))
 expected=a.resize((881,1321),Image.Resampling.LANCZOS);patch=np.array(b)[125:1446,72:953];exp=np.array(expected);reg=mask[125:1446,72:953]==255
 frame=Image.open(r/'frames'/({'iron':'blackiron'}.get(k,k)+'.png')).convert('RGBA');stars=Image.open(r/'frames'/({'iron':'blackiron'}.get(k,k)+'-stars-ui.png')).convert('RGBA')
 reg&=(np.array(frame)[125:1446,72:953,3]==0)&(np.array(stars)[125:1446,72:953,3]==0)
 out[k]={'pure':str(pures[k]),'pure_size':a.size,'card_size':b.size,'ui_size':c.size,'thumbnail_size':Image.open(u/(k+'-480.png')).size,'ui_uncovered_changed_pixels':int(np.count_nonzero(diff&zero)),'ui_uncovered_total_pixels':int(zero.sum()),'mask_at_face_crop_values':np.unique(mask[cb[1]:cb[3],cb[0]:cb[2]]).tolist(),'card_vs_resized_pure_uncovered_differing_pixels':int(np.count_nonzero(np.any(patch!=exp,axis=2)&reg)),'face_pure_crop':box,'face_card_crop':cb}
json.dump(out,open(o/'evidence.json','w'),ensure_ascii=False,indent=2);print(json.dumps(out,ensure_ascii=False,indent=2))
