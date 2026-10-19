import json,hashlib,zipfile,re,io,os
from pathlib import Path
from PIL import Image
ROOT=Path.cwd();OUT=ROOT/'output/高阶完整交付/2026-10-19_14-41-43';OUT.mkdir(exist_ok=True,parents=True)
H={'liubei':'刘备','guanyu':'关羽','zhangfei':'张飞'};B={'traditional':'传承','divine':'神','demonic':'魔','mecha':'机甲'};K={'card':'01-装框卡','biography':'02-独立传记','portrait':'03-透明头像','cutin':'04-透明技能立绘','vfx':'05-透明独立特效'}
config=json.load(open(OUT/'ready-manifests.json')); cards=json.load(open('advanced-card-ui/2026-10-19_13-57-00_UTC+08/card-manifest.json'))['cards'];C={(r['hero'],r['branch_id'],r['tier']):r for r in cards}
forms={};sources=[]
def walk(x):
 if isinstance(x,dict):
  if x.get('library_file_id'):yield x
  for v in x.values():yield from walk(v)
 elif isinstance(x,list):
  for v in x:yield from walk(v)
def checksum(p):return hashlib.sha256(p.read_bytes()).hexdigest()
for cfg in config:
 mp=Path(cfg['manifest']);data=json.load(open(mp));data=data if isinstance(data,list) else data.get('assets',data.get('files',[]));libs={}
 if cfg.get('library'):
  for r in walk(json.load(open(cfg['library']))):libs[Path(r.get('file_name',r.get('path',''))).name]=r['library_file_id']
 for r in data:
  p=Path(r.get('local_path',r.get('path','')))
  if not p.is_file():p=mp.parent/r.get('file_name',p.name)
  assert p.is_file(),p
  name=p.name;hero=cfg['hero'];branch=r.get('branch',cfg.get('branch'));tier=r.get('tier')
  if tier is None:tier=int(re.search(r'[56]',name).group())
  kind=r.get('kind')
  if not kind:
   kind=next(k for t,k in [('card','card'),('story','biography'),('bio','biography'),('avatar','portrait'),('portrait','portrait'),('cutin','cutin'),('cast','cutin'),('vfx','vfx'),('fx','vfx')] if t in name)
  branch={'legacy':'traditional','heritage':'traditional','demon':'demonic'}.get(branch,branch)
  kind={'avatar':'portrait','bio':'biography','story':'biography','cast':'cutin','fx':'vfx'}.get(kind,kind)
  sha=checksum(p);assert sha==r['sha256'],(p,'SHA mismatch')
  lid=r.get('library_file_id',libs.get(name));assert lid,(p,'no LibraryID')
  im=Image.open(p);dims=list(im.size);assert dims==r['size'],(p,dims,r['size'])
  row={'hero':hero,'branch':branch,'tier':tier,'kind':kind,'source_path':str(p.resolve()),'sha256':sha,'dimensions':dims,'library_file_id':lid,'bytes':p.stat().st_size,'alpha_extrema':list(im.getchannel('A').getextrema()) if 'A' in im.getbands() else None}
  if kind=='card':sources.append(row);continue
  if kind in ['portrait','cutin','vfx']:assert row['alpha_extrema'][0]==0 and row['alpha_extrema'][1]>0
  forms.setdefault((hero,branch,tier),{})[kind]=row
for key,items in forms.items():
 assert set(items)=={'biography','portrait','cutin','vfx'},(key,items.keys())
 c=C[key];p=Path(c['output']);assert checksum(p)==c['output_sha256'];assert c.get('library_file_id')
 source=next(r for r in sources if (r['hero'],r['branch'],r['tier'])==key);assert source['sha256']==c['source_sha256'],(key,'card source mismatch')
 items['card']={'hero':key[0],'branch':key[1],'tier':key[2],'kind':'card','source_path':str(p),'sha256':c['output_sha256'],'dimensions':list(Image.open(p).size),'library_file_id':c['library_file_id'],'bytes':p.stat().st_size,'alpha_extrema':None}
allrows=[];packrows=[];internal=[]
for key in sorted(forms,key=lambda k:(list(H).index(k[0]),list(B).index(k[1]),k[2])):
 hero,branch,tier=key;title=f'{H[hero]}-{B[branch]}-{tier}星';items=[forms[key][k] for k in K];batches=[];batch=[];size=0
 for a in items:
  if batch and size+a['bytes']>18_800_000:batches.append(batch);batch=[];size=0
  batch.append(a);size+=a['bytes']
 if batch:batches.append(batch)
 for n,batch in enumerate(batches):
  pack=title+('-'+chr(97+n) if len(batches)>1 else '')+'.zip';zp=OUT/pack;public=[]
  for a in batch:
   arc=f'{H[hero]}/{B[branch]}/{tier}星/{K[a["kind"]]}.png'
   row={'英雄':H[hero],'分支':B[branch],'星级':tier,'素材类型':K[a['kind']],'包内路径':arc,'压缩包':pack,'像素尺寸':a['dimensions'],'字节数':a['bytes'],'SHA256':a['sha256'],'LibraryID':a['library_file_id'],'Alpha范围':a['alpha_extrema'],'状态':'候选待用户验收','特效说明':'静态透明素材，非已实现动画' if a['kind']=='vfx' else None}
   public.append(row);allrows.append(row);internal.append({'source_path':a['source_path'],**row})
  if not zp.exists():
   with zipfile.ZipFile(zp,'w',compression=zipfile.ZIP_STORED) as z:
    for a,row in zip(batch,public):z.write(a['source_path'],row['包内路径'])
    z.writestr('文件清单.json',json.dumps(public,ensure_ascii=False,indent=2))
    z.writestr('README.txt','本包为'+title+'候选素材。每形态完整内容为装框卡、独立传记、透明头像、透明技能立绘、透明独立特效五项；若文件名含a/b，请分别下载两包，各自可独立解压。原字节未重编码、未放大。全部待用户验收，技能/数值为设计草案。VFX为静态透明图片，不代表已实现动画。无框卡插画源另行保留，不计入五项。')
  assert zp.stat().st_size<19_000_000
  with zipfile.ZipFile(zp) as z:
   assert z.testzip() is None;assert len([n for n in z.namelist() if n.endswith('.png')])==len(public)
   for row in public:
    raw=z.read(row['包内路径']);assert hashlib.sha256(raw).hexdigest()==row['SHA256'];assert list(Image.open(io.BytesIO(raw)).size)==row['像素尺寸']
  packrows.append({'文件名':pack,'字节数':zp.stat().st_size,'SHA256':checksum(zp),'素材数':len(batch),'形态':title,'验证':'独立解压、数量、像素尺寸及SHA256通过'})
assert len(allrows)==5*len(forms);assert len({r['SHA256'] for r in allrows})==len(allrows)
(OUT/'current-inventory.json').write_text(json.dumps({'已就绪形态':len(forms),'目标形态':24,'已就绪素材':len(allrows),'目标素材':120,'候选状态':'待用户验收','压缩包':packrows,'素材':allrows},ensure_ascii=False,indent=2))
(OUT/'rebuild-source-map.json').write_text(json.dumps(internal,ensure_ascii=False,indent=2))
(OUT/'unframed-source-map.json').write_text(json.dumps(sources,ensure_ascii=False,indent=2))
req=[]
for r in packrows:
 p=OUT/r['文件名']
 if 'user.library-file-id' not in os.listxattr(p):req.append({'local_path':str(p),'purpose':'create_library_file','library_artifact_type':'other'})
(OUT/'pending-upload-request.json').write_text(json.dumps({'uploads':req},ensure_ascii=False,indent=2))
print(json.dumps({'forms':len(forms),'assets':len(allrows),'packages':len(packrows),'new_packages':len(req),'max_bytes':max(r['字节数'] for r in packrows)},ensure_ascii=False))
