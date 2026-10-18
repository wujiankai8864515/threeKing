from PIL import Image,ImageDraw,ImageFilter
import numpy as np
from scipy.cluster.vq import kmeans2
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import maximum_flow,breadth_first_order
from pathlib import Path
p=Path(__file__).parent
im=Image.open(p/'weapon-edit-crop-1024x768.png').convert('RGB');box=(325,240,670,510);rgb=np.array(im.crop(box),dtype=np.float64);h,w=rgb.shape[:2];N=h*w
old=Image.open(p/'old-head-extraction-mask.png');support=np.array(old.filter(ImageFilter.MaxFilter(41)).crop(box))>0
fgim=Image.new('L',im.size);d=ImageDraw.Draw(fgim)
d.line([(358,464),(395,466),(433,449),(470,421),(505,386),(541,348),(565,326),(590,304),(616,283),(647,262)],fill=255,width=7)
d.line([(566,344),(559,374),(550,403)],fill=255,width=11)
d.line([(351,455),(375,451),(401,438),(425,420),(442,405),(448,393),(448,383),(461,387),(478,381),(493,370),(504,359)],fill=255,width=3)
d.line([(355,463),(377,478),(410,482),(444,470),(475,450),(505,423)],fill=255,width=3)
fgseed=np.array(fgim.crop(box))>0;bgseed=~support
X=rgb.reshape(-1,3);fg=fgseed.reshape(-1).copy();fg|=(np.array(old.crop(box)).reshape(-1)>0)
def costs(select,k=6):
 Y=X[select]
 if len(Y)>30000:Y=Y[np.random.default_rng(10).choice(len(Y),30000,replace=False)]
 centers,labels=kmeans2(Y.astype(float),k,iter=20,minit='++',seed=10)
 ds=[]
 for j in range(k):
  group=Y[labels==j]
  if len(group)<3:continue
  var=np.maximum(group.var(axis=0),30)
  weight=len(group)/len(Y)
  ds.append(.5*((X-centers[j])**2/var).sum(axis=1)+.5*np.log(var).sum()-np.log(weight))
 return np.min(ds,axis=0)
ids=np.arange(N).reshape(h,w)
p1=np.concatenate([ids[:,:-1].ravel(),ids[:-1,:].ravel()]);p2=np.concatenate([ids[:,1:].ravel(),ids[1:,:].ravel()]);sq=((X[p1]-X[p2])**2).sum(axis=1);beta=1/(2*sq.mean());ew=np.maximum(1,np.rint((35*np.exp(-beta*sq)+.5)*100)).astype(np.int32)
for it in range(3):
 df=costs(fg);db=costs(~fg);mi=np.minimum(df,db);df=np.rint((df-mi)*100).astype(np.int32);db=np.rint((db-mi)*100).astype(np.int32)
 df[bgseed.ravel()]=100000000;db[fgseed.ravel()]=100000000
 s=N;t=N+1;nodes=np.arange(N)
 rows=np.concatenate([p1,p2,np.full(N,s),nodes]);cols=np.concatenate([p2,p1,nodes,np.full(N,t)]);data=np.concatenate([ew,ew,db,df])
 cap=csr_matrix((data,(rows,cols)),shape=(N+2,N+2),dtype=np.int32)
 flow=maximum_flow(cap,s,t,method='dinic').flow
 residual=cap-flow;residual.data=(residual.data>0).astype(np.int8);residual.eliminate_zeros()
 reachable=breadth_first_order(residual,s,directed=True,return_predecessors=False);fg=np.zeros(N,bool);fg[reachable[reachable<N]]=True
 print('iteration',it,'foreground',fg.sum(),flush=True)
mask=np.zeros((768,1024),np.uint8);mask[box[1]:box[3],box[0]:box[2]]=fg.reshape(h,w)*255
Image.fromarray(mask).save(p/'old-head-extraction-mask-refined.png')
# black-and-gray checker preview
Y,Xgrid=np.indices((768,1024));chk=np.where(((Xgrid//12+Y//12)%2)[...,None],75,160).astype(np.uint8);chk=np.repeat(chk,3,axis=2)
prev=Image.fromarray(chk);prev.paste(im,(0,0),Image.fromarray(mask));prev.crop((330,245,665,505)).resize((670,520)).save(p/'qa-head-extraction-refined.png')
