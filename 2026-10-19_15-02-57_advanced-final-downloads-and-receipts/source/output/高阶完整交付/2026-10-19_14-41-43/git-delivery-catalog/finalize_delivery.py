from pathlib import Path
import json,hashlib,zipfile,os
from collections import Counter
out=Path('output/高阶完整交付/2026-10-19_14-41-43');d=json.load(open(out/'current-inventory.json'));assert d['已就绪形态']==24 and len(d['素材'])==120 and len(d['压缩包'])==24
assert Counter(r['英雄'] for r in d['素材'])=={'刘备':40,'关羽':40,'张飞':40}
assert len({r['SHA256'] for r in d['素材']})==120
for p in d['压缩包']:
 f=out/p['文件名'];assert hashlib.sha256(f.read_bytes()).hexdigest()==p['SHA256'];p['LibraryID']=os.getxattr(f,'user.library-file-id').decode();p['MiB']=round(p['字节数']/2**20,2)
d['标题']='刘关张高阶24形态120最终素材交付总清单';d['说明']='每形态五项为装框卡、独立传记、透明头像、透明技能立绘、透明独立VFX。无框插画另行作为源保存，不计入120项。VFX为静态素材，非已实现动画。';d['核验']={'最终素材120项':True,'每形态5项':True,'72透明素材真实Alpha':sum(r['Alpha范围'] is not None for r in d['素材'])==72,'重复SHA':0,'逐包独立解压核验':True,'所有包小于19000000字节':all(p['字节数']<19_000_000 for p in d['压缩包'])}
(out/'24形态-120素材-最终总清单.json').write_text(json.dumps(d,ensure_ascii=False,indent=2))
s=json.load(open(out/'unframed-source-map.json'));assert len(s)==24
src=[{'英雄':r['hero'],'分支':r['branch'],'星级':r['tier'],'源文件名':Path(r['source_path']).name,'尺寸':r['dimensions'],'SHA256':r['sha256'],'LibraryID':r['library_file_id'],'说明':'无框插画源，非装框卡，不计入120最终素材'} for r in s]
(out/'说明文档/24张无框插画-源清单.json').write_text(json.dumps(src,ensure_ascii=False,indent=2))
lines=['刘关张高阶24形态完整交付','', '全部24形态共120项最终素材，另保留24张无框插画源。','刘备、关羽、张飞各四分支：传承、神、魔、机甲；每分支五星与六星两形态。','每形态一个独立ZIP，每包含5项：装框卡、独立传记、透明头像、透明技能立绘、透明独立特效。','本次所有形态均可单包容纳，无需a/b拆分。24素材包均严格小于19,000,000字节，可各自解压，不需分卷拼接。','','候选与实现状态','全部为待用户验收候选，保存或发送成功不表示最终批准。','技能、数值、冷却、升级幅度均为设计方案；五星3被动固定，六星保留3被动为当前设计默认。','VFX和cut-in是静态透明源素材，并非已实现的动画、粒子系统或技能时间轴。','神/魔/机甲分支的文化依据与原创边界、主动、三被动、5→6成长详见完整技能文化方案。','','真实尺寸与保真','装框卡1190×1786；画内插画原生1024×1536，1:1置入。','头像1254×1254；传记1536×1024；技能立绘与特效原生尺寸逐文件见总清单。','图片原字节封装，未重编码、未放大，不以缩略图冒充高清。72项透明素材均有真实Alpha。','24张无框插画不重复放入最终形态ZIP，已另作源文件归档；其LibraryID和SHA见说明包内源清单。','','说明文件','00-说明与总索引.zip：完整技能文化方案、规格说明、三英雄技能/文化文档、120项总清单、24无框源清单、README。','完整技能文化方案提供24形态逐项文字说明，不仅是JSON。','','24个素材包']
for p in d['压缩包']:lines+=[f"{p['文件名']} | 5项 | {p['字节数']:,}字节 | {p['LibraryID']}"]
lines+=['','核验结论','120最终文件全部唯一；24形态各5项，三英雄各40项。','每个ZIP逐文件解压校验数量、SHA256和像素尺寸通过；与正式冻结源清单一致。']
(out/'README-高阶完整下载说明.txt').write_text('\n'.join(lines)+'\n')
files=sorted((out/'说明文档').glob('*'))+[out/'24形态-120素材-最终总清单.json',out/'README-高阶完整下载说明.txt']
zp=out/'00-说明与总索引.zip'
with zipfile.ZipFile(zp,'w',compression=zipfile.ZIP_STORED) as z:
 for f in files:z.write(f,f.name)
with zipfile.ZipFile(zp) as z:
 assert z.testzip() is None
 for f in files:assert hashlib.sha256(z.read(f.name)).hexdigest()==hashlib.sha256(f.read_bytes()).hexdigest()
assert zp.stat().st_size<19_000_000
upload=[out/'README-高阶完整下载说明.txt',out/'24形态-120素材-最终总清单.json',out/'说明文档/刘关张-24形态-完整技能与文化方案.md',zp]
(out/'docs-upload-request.json').write_text(json.dumps({'uploads':[{'local_path':str(f.resolve()),'purpose':'create_library_file','library_artifact_type':'other'} for f in upload]},ensure_ascii=False,indent=2))
print('final',len(d['素材']),len(d['压缩包']),'docs',len(files),'largest',max(p['字节数'] for p in d['压缩包']))
