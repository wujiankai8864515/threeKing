from pathlib import Path
from PIL import Image, ImageDraw
import numpy as np, math, json, hashlib, shutil

D=Path("/workspace/scratch/3f82ff2b3f81/guanyu-mythic-set/bronze_tail_masked_20261018_233859_UTC+08")
basepath=Path("/workspace/scratch/3f82ff2b3f81/guanyu-mythic-set/bronze_rebuild_researched_20261018_231529_UTC+08/青铜-骑乘结构重建-候选1.png")
srcpath=Path("/workspace/scratch/3f82ff2b3f81/guanyu-mythic-set/bronze_tail_local_20261018_232717_UTC+08/青铜-骑乘重建尾杆局修-候选2.png")
base=Image.open(basepath).convert("RGB"); src=Image.open(srcpath).convert("RGB")
W,H=base.size; S=8

def poly_mask(poly):
    m=Image.new("L",(W*S,H*S),0)
    ImageDraw.Draw(m).polygon([(round(x*S),round(y*S)) for x,y in poly],fill=255)
    return m.resize((W,H),Image.Resampling.LANCZOS)

# Extract only the existing builtin-generated aft pole and its butt cap.
source_a=1.0261563041964252
source_b=-16.903007005421363
def sx(y): return source_a*y+source_b
half=8.7
shaft=poly_mask([(sx(211)-half,211),(sx(354)-half,354),(sx(354)+half,354),(sx(211)+half,211)])
cap_poly=[(170,189),(174,184),(181,181),(188,181),(193,183),(193,190),(195,198),(199,203),(205,205),(210,209),(214,214),(213,219),(207,223),(200,220),(194,215),(190,211),(185,209),(178,208),(173,204),(170,199),(169,194)]
cap_geo=np.asarray(poly_mask(cap_poly),dtype=float)/255
rgb=np.asarray(src,dtype=float)
# Blue background edge removal only on the extracted golden butt cap.
gold_alpha=np.clip((rgb[:,:,0]-rgb[:,:,2]-2)/17,0,1)
cap_alpha=cap_geo*gold_alpha
source_alpha=np.maximum(np.asarray(shaft,dtype=float)/255,cap_alpha)
source_alpha=np.clip(source_alpha,0,1)
source_mask=Image.fromarray(np.uint8(np.round(source_alpha*255)),"L")
source_mask.save(D/"patch-source-mask.png")
patch=src.convert("RGBA"); patch.putalpha(source_mask); patch.crop((160,170,370,365)).save(D/"patch-builtin-尾杆尾帽.png")

# Rigid rotation and translation only: align with the already-existing main pole.
# Main pole center axis through (427,470) and (575,630).
target_a=(575-427)/(630-470)
target_b=427-target_a*470
source_anchor=np.array([sx(193),193.0])
target_anchor=np.array([190.0,(190.0-target_b)/target_a])
theta=math.atan2(1,target_a)-math.atan2(1,source_a)
R=np.array([[math.cos(theta),-math.sin(theta)],[math.sin(theta),math.cos(theta)]])
offset=source_anchor-R.T@target_anchor
coeff=tuple(R.T[0])+tuple([offset[0]])+tuple(R.T[1])+tuple([offset[1]])
warped_rgb=src.transform((W,H),Image.Transform.AFFINE,coeff,Image.Resampling.BICUBIC)
warped_mask=source_mask.transform((W,H),Image.Transform.AFFINE,coeff,Image.Resampling.BICUBIC)

# Forearm, hand and armor occlusion: preserve the base pixels exactly.
arm_poly=[(318,369),(332,364),(352,369),(370,374),(385,390),(399,411),(411,426),(422,450),(411,469),(390,475),(369,466),(352,450),(331,452),(307,444),(300,427),(305,405),(307,384)]
locked=Image.new("L",(W,H),0)
ld=ImageDraw.Draw(locked)
ld.polygon(arm_poly,fill=255)
for box in [(475,310,665,575),(735,395,885,570),(120,300,245,420),(130,275,220,315),(550,610,635,695)]:
    ld.rectangle(box,fill=255)
lockarr=np.asarray(locked)>0
ma=np.array(warped_mask); ma[lockarr]=0
# Strict work corridor. Other areas cannot receive even interpolation residue.
yy,xx=np.indices((H,W)); corridor=(xx>=155)&(xx<=360)&(yy>=180)&(yy<=400)
ma[~corridor]=0
mask=Image.fromarray(ma,"L"); mask.save(D/"mask-applied.png")
locked.save(D/"mask-protected-faces-arm-hand.png")
warped=warped_rgb.convert("RGBA"); warped.putalpha(mask); warped.save(D/"patch-aligned-fullcanvas.png")
final=Image.composite(warped_rgb,base,mask)
final.save(D/"青铜-骑乘重建-尾杆共轴遮罩修复.png")
shutil.copy2(basepath,D/"original-重建候选1.png")
shutil.copy2(srcpath,D/"patch-source-builtin局修2.png")

ba=np.asarray(base); fa=np.asarray(final); changed=np.any(ba!=fa,axis=2)
assert np.array_equal(ba[ma==0],fa[ma==0]),"Changed outside mask"
assert not changed[lockarr].any(),"Protected face/arm/hand changed"
regions={"关羽脸":(475,310,665,575),"刘备脸":(735,395,885,570),"张飞脸":(120,300,245,420),"关羽全刀":(145,175,1024,1085),"尾杆遮挡轴":(150,175,640,705)}
for name,box in regions.items():
    out=final.crop(box); out.save(D/("QA-native-"+name+".png"))
    if name.endswith("脸"):
        old=base.crop(box)
        both=Image.new("RGB",(old.width*2,old.height),(225,225,225)); both.paste(old,(0,0));both.paste(out,(old.width,0))
        both.save(D/("QA-"+name+"-前左后右-像素一致.png"))
final.crop((140,170,630,705)).resize((980,1070),Image.Resampling.NEAREST).save(D/"QA-尾杆连接-2x.png")
ys,xs=np.where(changed)
report={
"base":str(basepath),"builtin_patch_source":str(srcpath),
"method":"Extract only builtin-generated aft shaft and butt-cap; rigid transform; explicit mask composite over original researched rebuild candidate 1. No generated faces or armor from failed candidate 2 are used.",
"source_axis_x_equals_a_y_plus_b":[source_a,source_b],
"target_main_axis_x_equals_a_y_plus_b":[target_a,target_b],
"source_anchor":source_anchor.tolist(),"target_anchor":target_anchor.tolist(),"rotation_degrees":math.degrees(theta),
"outside_mask_changed_pixels":int(changed[ma==0].sum()),
"locked_faces_arm_hand_changed_pixels":int(changed[lockarr].sum()),
"total_changed_pixels":int(changed.sum()),
"changed_bbox":[int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1)],
"face_exact_pixel_equal":{n:bool(np.array_equal(np.asarray(base.crop(b)),np.asarray(final.crop(b)))) for n,b in regions.items() if n.endswith("脸")},
"source_generation_prompt_record":"/workspace/scratch/3f82ff2b3f81/guanyu-mythic-set/bronze_tail_local_20261018_232717_UTC+08/局修记录.json",
"files":{}
}
for p in D.glob("*.png"): report["files"][p.name]={"sha256":hashlib.sha256(p.read_bytes()).hexdigest(),"size_bytes":p.stat().st_size}
(D/"geometry-and-pixel-QA.json").write_text(json.dumps(report,ensure_ascii=False,indent=2))
print(json.dumps({k:report[k] for k in ["target_main_axis_x_equals_a_y_plus_b","rotation_degrees","outside_mask_changed_pixels","locked_faces_arm_hand_changed_pixels","total_changed_pixels","changed_bbox","face_exact_pixel_equal"]},ensure_ascii=False,indent=2))

