from PIL import Image,ImageDraw,ImageFilter
from pathlib import Path
import numpy as np,json,hashlib
from scipy.ndimage import map_coordinates
p=Path(__file__).parent
full=Image.open(p/'source-v13-frozen.png').convert('RGB');orig=Image.open(p/'weapon-edit-crop-1024x768.png').convert('RGB');gen=Image.open(p/'generated-patch-native-crop.png').convert('RGB')
m=np.array(Image.open(p/'old-head-extraction-mask-refined.png')).copy();yy,xx=np.indices(m.shape)
# Trim only residual background above the actual original blade edge.
edge=np.array([(345,454),(365,454),(385,449),(404,438),(425,421),(441,405),(447,392)])
bound=np.interp(xx,edge[:,0],edge[:,1]);m[(xx<447)&(yy<bound-1.5)]=0
# The top cut is restricted to the original shaft silhouette.
normaldist=np.abs(yy-(720.833333333-.7166666667*xx))/np.sqrt(1+.7166666667**2)
m[(xx>630)&((normaldist>6.5)|((xx-650)*.812+(yy-257)*(-.582)>0))]=0
head_alpha=Image.fromarray(m).filter(ImageFilter.GaussianBlur(.45));head_alpha=np.array(head_alpha);head_alpha[head_alpha<3]=0;head_alpha=Image.fromarray(head_alpha)
head_alpha.save(p/'head-alpha-trimmed.png')
# A small feather is confined to the approved old-weapon removal footprint.
erase=Image.fromarray(m).filter(ImageFilter.MaxFilter(5)).filter(ImageFilter.GaussianBlur(1.1));e=np.array(erase);e[e<3]=0;erase=Image.fromarray(e)
clean=orig.copy();clean.paste(Image.open(p/'cleanplate-native.png').convert('RGB'),(325,240));base=orig.copy();base.paste(clean,(0,0),erase)
# Relocate the original approved blade, collar and tassel together, without scaling.
shift=(-240,172);new_head_alpha=Image.new('L',orig.size);new_head_alpha.paste(head_alpha,shift)
head_rgb=Image.new('RGB',orig.size);head_rgb.paste(orig,shift);base.paste(head_rgb,(0,0),new_head_alpha)
# A rigid pole texture strip fills the extension and joins the untouched original pole below the hand.
A=np.array([403.,431.5]);B=np.array([721.,204.1]);v=B-A;length=np.linalg.norm(v);u=v/length;n=np.array([-u[1],u[0]])
t=((xx-A[0])*u[0]+(yy-A[1])*u[1])/length;d=(xx-A[0])*n[0]+(yy-A[1])*n[1]
As=np.array([460.,391.]);Bs=np.array([715.,208.]);vs=Bs-As;us=vs/np.linalg.norm(vs);ns=np.array([-us[1],us[0]])
sx=As[0]+t*vs[0]+d*ns[0];sy=As[1]+t*vs[1]+d*ns[1]
g=np.array(gen,dtype=float);tex=np.stack([map_coordinates(g[:,:,c],[sy,sx],order=1,mode='nearest') for c in range(3)],axis=2).clip(0,255).astype(np.uint8)
a=np.clip((5.5-np.abs(d))/1.0,0,1)*np.clip(t*length/2,0,1)*np.clip((1-t)*length/7,0,1)
a[(t<0)|(t>1)]=0
rod_alpha=Image.fromarray(np.rint(a*255).astype(np.uint8));base.paste(Image.fromarray(tex),(0,0),rod_alpha)
# Exact original pixels everywhere outside the union mask.
union=np.maximum.reduce([np.array(erase),np.array(new_head_alpha),np.array(rod_alpha)])
mask_full=np.zeros((1024,1536),np.uint8);mask_full[256:1024,:1024]=union
mask_img=Image.fromarray(mask_full);mask_img.save(p/'edit-mask-1536x1024.png')
out=np.array(full);edited=np.array(base);support=union>0;out_crop=out[256:1024,:1024];out_crop[support]=edited[support]
final=Image.fromarray(out);final.save(p/'温酒请战-v17-原图冻结-武器局部合成.png')
base.save(p/'composited-weapon-patch-native.png');rod_alpha.save(p/'shaft-alpha.png');new_head_alpha.save(p/'new-head-alpha.png');erase.save(p/'old-weapon-removal-mask.png')
patch_rgba=base.convert('RGBA');patch_rgba.putalpha(Image.fromarray(union));patch_rgba.save(p/'final-patch-RGBA.png')
final.crop((65,325,910,950)).save(p/'qa-complete-weapon-100pct.png');final.crop((670,365,820,490)).resize((600,500)).save(p/'qa-grip-4x.png')
orig_full=np.array(full);delta=np.max(np.abs(out.astype(np.int16)-orig_full.astype(np.int16)),axis=2);outside=mask_full==0
rois={'GuanYu_face':[880,65,1125,270],'left_hand_and_forearm':[726,300,825,464],'LiuBei_face':[125,365,185,435],'ZhangFei_face':[240,395,310,470],'CaoCao_face':[405,430,465,500],'horse':[850,200,1450,1024],'dragon':[180,0,1536,280]}
qa={'method':'Built-in generated a lower-left crop patch; deterministic masked composite onto untouched v13. Original blade/collar/tassel translated together (-240,+172), original arm/hand/upper pole left untouched. Generated patch supplies only local old-weapon background restoration and shaft texture.','full_size':[1536,1024],'source_sha256':hashlib.sha256((p/'source-v13-frozen.png').read_bytes()).hexdigest(),'final_sha256':hashlib.sha256((p/'温酒请战-v17-原图冻结-武器局部合成.png').read_bytes()).hexdigest(),'generated_size':[1448,1086],'generated_patch_native_size':[1024,768],'crop_bbox':[0,256,1024,1024],'mask_nonzero_pixels':int((mask_full>0).sum()),'outside_mask_changed_pixels':int((delta[outside]>0).sum()),'roi_changes':{k:int((delta[b[1]:b[3],b[0]:b[2]]>0).sum()) for k,b in rois.items()},'status':'awaiting visual QA; not yet uploaded'}
(p/'qa.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2)+'\n');print(json.dumps(qa,ensure_ascii=False,indent=2))
