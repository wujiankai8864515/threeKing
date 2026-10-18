from PIL import Image,ImageDraw,ImageFilter,ImageChops
from pathlib import Path
import numpy as np, math, json, hashlib
P=Path(__file__).parent; S=(1024,1536)
original=Image.open(P/'黄金-用户认可旧底图-原样.png').convert('RGBA')
# The cut is below the preserved original hand, bare rod, and heavy gold grip cuffs.
head_poly=[(397,750),(424,760),(417,786),(411,809),(407,834),(400,868),(377,884),(349,911),(323,948),(292,986),(262,1023),(220,1070),(175,1118),(120,1163),(53,1196),(0,1210),(0,1092),(20,1070),(40,1055),(70,1042),(62,1020),(65,995),(90,970),(125,950),(145,920),(165,883),(210,858),(227,830),(260,809),(293,792),(324,783),(350,780),(375,769)]
def poly_mask(points,scale=4):
 m=Image.new('L',(S[0]*scale,S[1]*scale));ImageDraw.Draw(m).polygon([(round(x*scale),round(y*scale)) for x,y in points],fill=255)
 return m.resize(S,Image.Resampling.LANCZOS)
head_mask=poly_mask(head_poly).filter(ImageFilter.GaussianBlur(2.0))
# Restrict feather to a small support around the weapon footprint only.
removal_mask=head_mask.filter(ImageFilter.MaxFilter(5)).filter(ImageFilter.GaussianBlur(1.0))
# Never allow broad repair at the hand/cuffs or beyond weapon vicinity.
rm=np.array(removal_mask); yy,xx=np.indices((1536,1024));rm[yy<748]=0
removal_mask=Image.fromarray(rm)
head_mask.save(P/'old-blade-selection-mask.png');removal_mask.save(P/'old-blade-removal-mask.png')
head_patch=original.copy();head_patch.putalpha(head_mask);head_patch.save(P/'original-blade-pixels-patch.png')
# Original blade pixels are translated by one integer vector with no resampling.
shift=(-88,160)
moved=Image.new('RGBA',S);moved.alpha_composite(head_patch,shift);moved.save(P/'translated-original-blade-patch.png')
# AI-generated local background is used only inside the vacated weapon footprint.
bg=Image.open(P/'generated-background-patch.png').convert('RGBA').resize((512,768),Image.Resampling.LANCZOS)
bgfull=Image.new('RGBA',S);bgfull.paste(bg,(0,640));bgfull.putalpha(removal_mask);bgfull.save(P/'masked-background-patch.png')
base=Image.alpha_composite(original,bgfull)
# A generated, isolated metal cylinder is mapped onto one exact line.
a=Image.open(P/'generated-shaft-asset.png').convert('RGBA');arr=np.array(a);arr[:,:,3][arr[:,:,3]<8]=0;a=Image.fromarray(arr);bbox=a.getchannel('A').getbbox();a=a.crop(bbox);a.save(P/'shaft-asset-alpha-cleaned.png')
start=np.array([318.5,911.0]);end=np.array([646.25,315.0]);vec=end-start;length=float(np.linalg.norm(vec));u=vec/length;n=np.array([-u[1],u[0]])
# Match old narrow metal shaft at 20px diameter; preserve original existing middle segment.
thick=20.0;aw,ah=a.size
coef=(u[0]*(aw-1)/length,u[1]*(aw-1)/length,-float(np.dot(start,u))*(aw-1)/length,n[0]*(ah-1)/thick,n[1]*(ah-1)/thick,(ah-1)/2-float(np.dot(start,n))*(ah-1)/thick)
rod=a.transform(S,Image.Transform.AFFINE,coef,Image.Resampling.BICUBIC)
rodalpha=np.array(rod.getchannel('A'));rodalpha[(yy>535)&(yy<755)]=0
hand_poly=[(495,495),(531,497),(542,517),(541,544),(530,568),(510,584),(489,572),(479,549),(485,519)]
hand_mask=poly_mask(hand_poly);rodalpha[np.array(hand_mask)>0]=0
rod.putalpha(Image.fromarray(rodalpha));rod.save(P/'shaft-continuation-patch.png');hand_mask.save(P/'protected-original-hand-mask.png')
base=Image.alpha_composite(base,rod);final=Image.alpha_composite(base,moved)
# Precise support mask covers all and only editable patch alpha support.
support=(np.array(removal_mask)>0)|(rodalpha>0)|(np.array(moved.getchannel('A'))>0)
mask=Image.fromarray(np.uint8(support)*255);mask.save(P/'edit-support-mask.png')
final.save(P/'关羽-黄金-旧源长柄遮罩保真修复-候选3.png')
# Transparent merged replacement pixels, sufficient to reconstruct the final over the old source.
f=np.array(final);o=np.array(original);changed=np.any(f!=o,axis=2)
patch=final.copy();patch.putalpha(Image.fromarray(np.uint8(support)*255));patch.save(P/'combined-repair-patch.png')
assert np.count_nonzero(changed&~support)==0
for key,box in {'grip':(440,470,590,650),'upper-shaft':(480,290,690,580),'lower-join':(230,700,450,1050),'blade':(0,930,350,1450),'hoof':(500,885,750,1220),'face-armor':(410,180,710,500),'tail':(0,430,470,700)}.items():final.crop(box).save(P/f'QA-{key}-native.png')
final.resize((256,384),Image.Resampling.LANCZOS).save(P/'QA-thumbnail.png')
# Check conserved non-weapon areas separately. The upper rod's narrow occlusion of armor is intentional.
rois={'hoof':(500,885,750,1220),'face':(535,205,632,300),'horse-head':(690,380,850,660),'tail-interior':(0,430,470,690),'dragon':(670,0,1024,340),'background-right':(900,370,1024,1000)}
roi={}
for k,(x0,y0,x1,y1) in rois.items():roi[k]=int(changed[y0:y1,x0:x1].sum())
meta={'source':'黄金-用户认可旧底图-原样.png','source_sha256':hashlib.sha256((P/'黄金-用户认可旧底图-原样.png').read_bytes()).hexdigest(),'size':S,'blade_translation_integer_pixels':shift,'shaft_axis_start':start.tolist(),'shaft_axis_end':end.tolist(),'shaft_diameter_px':thick,'mask_support_pixels':int(support.sum()),'changed_pixels':int(changed.sum()),'outside_mask_changed_pixels':int(np.count_nonzero(changed&~support)),'roi_changed_pixels':roi,'generation':'builtin: isolated steel shaft asset and vacated-blade background only; final deterministic masked composite','status':'candidate: awaiting actual full/native visual QA'}
(P/'pixel-QA.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(meta,ensure_ascii=False,indent=2))
