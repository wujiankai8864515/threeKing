from pathlib import Path
from PIL import Image,ImageDraw
import cv2,numpy as np,json
D=Path(__file__).parent;s=Image.open(D.parent/'scoped-revision_2026-10-18_22-51-10_UTC+08/card01-blackiron.png').convert('RGB');a=np.array(s);m=Image.new('L',s.size);dr=ImageDraw.Draw(m)
body=[(80,140),(112,135),(126,169),(126,213),(111,241),(131,280),(166,299),(215,290),(251,294),(284,296),(322,300),(350,277),(356,239),(371,208),(390,167),(400,133),(418,119),(444,121),(468,140),(466,152),(495,155),(519,176),(518,200),(529,215),(516,251),(530,281),(518,305),(560,320),(604,334),(636,362),(654,398),(672,425),(693,458),(718,497),(720,535),(704,579),(690,604),(664,627),(613,642),(543,652),(555,683),(575,704),(600,743),(607,768),(585,790),(608,829),(634,876),(644,931),(651,981),(667,1031),(679,1072),(691,1098),(688,1122),(664,1149),(664,1183),(645,1210),(608,1214),(611,1269),(625,1308),(649,1333),(661,1360),(672,1390),(669,1412),(638,1423),(598,1418),(556,1410),(546,1382),(511,1341),(499,1305),(493,1270),(490,1221),(456,1212),(420,1195),(409,1157),(395,1121),(383,1072),(357,1062),(351,1090),(330,1111),(300,1126),(285,1170),(279,1215),(282,1247),(268,1273),(235,1284),(207,1276),(180,1270),(139,1270),(104,1262),(106,1238),(138,1225),(171,1226),(189,1193),(196,1158),(181,1122),(155,1094),(132,1075),(124,1034),(133,994),(127,964),(140,939),(158,903),(169,867),(187,821),(202,768),(222,721),(232,686),(246,650),(257,601),(252,560),(249,509),(242,486),(209,499),(169,495),(143,492),(125,469),(112,433),(107,391),(92,372),(81,344)]
dr.polygon(body,fill=255)
# Hair ribbons and waist streamers remain original foreground pixels.
for poly in [[(413,159),(352,138),(354,153),(329,164),(346,176),(371,178),(405,170)],[(390,186),(350,195),(294,200),(272,221),(303,213),(315,218),(319,238),(340,224),(364,216)],[(530,727),(602,793),(637,840),(675,871),(701,902),(707,938),(694,963),(733,981),(762,998),(787,1030),(759,1016),(732,1009),(713,1005),(686,985),(677,956),(660,921),(626,902),(602,871),(569,855)]]:dr.polygon(poly,fill=255)
raw=np.array(m);fg=raw.copy()
# Pole is translated as the same group, maintaining original grip relation and vertical continuity.
pm=Image.fromarray(fg);pd=ImageDraw.Draw(pm);pd.polygon([(0,0),(112,0),(108,62),(141,72),(140,94),(105,86),(97,136),(88,233),(76,399),(71,512),(56,742),(43,930),(28,1130),(28,1268),(0,1268)],fill=255)
fg=np.array(pm)
# Refine blue-sky contamination at hand/coat and flyaway contours without classifying cloth highlights.
from scipy.ndimage import binary_fill_holes
rr=a[:,:,0].astype(float);gg=a[:,:,1].astype(float);bb=a[:,:,2].astype(float)
sky=((bb>rr+8)&(bb>gg*.94))|((bb>=rr)&(bb>190)&(gg>185)&(rr>175))
boundary=(fg>0)&(cv2.erode(fg,np.ones((35,35),np.uint8))==0)
yy,xx=np.indices(fg.shape);region=((yy<350)&(xx>130))|((yy>565)&(yy<685)&(xx>520))
fg[sky&region]=0
fg=fg.astype('uint8')
shift=np.zeros_like(fg);shift[:,24:]=fg[:,:-24];moved=np.zeros_like(a);moved[:,24:]=a[:,:-24]
from scipy.ndimage import distance_transform_edt,gaussian_filter
# Refine only the outer contour; keep every interior original pixel exactly.
alpha=gaussian_filter(shift.astype(float)/255,.8);alpha[shift==255]=1
clear=cv2.dilate(fg,np.ones((9,9),np.uint8))>0
dist=distance_transform_edt(~clear);repair=np.clip(1-dist/16,0,1);repair[clear]=1
bg=np.array(Image.open(D/'blackiron-background-generated.png').convert('RGB').resize(s.size))
# Match low-frequency background color at the repair edge to avoid rectangular sky seams.
base=a.astype(float)*(1-repair[:,:,None])+bg.astype(float)*repair[:,:,None]
out=np.round(base*(1-alpha[:,:,None])+moved.astype(float)*alpha[:,:,None]).clip(0,255).astype('uint8')
union=(repair>0)|(alpha>0);holes=(repair>0)&(alpha<1)
Image.fromarray(out).save(D/'blackiron-final.png');Image.fromarray(fg).save(D/'blackiron-original-foreground-mask.png');Image.fromarray(np.round(alpha*255).astype('uint8')).save(D/'blackiron-moved-foreground-mask.png');Image.fromarray(np.round(repair*255).astype('uint8')).save(D/'blackiron-background-repair-mask.png');Image.fromarray((union*255).astype('uint8')).save(D/'blackiron-mask.png')
diff=np.any(a!=out,axis=-1);assert not np.any(diff&~union);interior=alpha==1;assert np.array_equal(out[interior],moved[interior]);q=json.loads((D/'pixel-QA.json').read_text());q['blackiron']={'translation_px':[24,0],'resampling':'none; contour alpha only','moved_interior_pixel_mismatch':0,'outside_mask_changed':0,'changed_pixels':int(diff.sum()),'background_repair_pixels':int(holes.sum()),'grip':'pillar and hero translated together','visual_status':'pending manual review'};(D/'pixel-QA.json').write_text(json.dumps(q,indent=2));print(q['blackiron'])
