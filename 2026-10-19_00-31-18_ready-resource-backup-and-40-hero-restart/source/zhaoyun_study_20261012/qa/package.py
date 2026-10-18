from pathlib import Path
import json,hashlib,base64,mimetypes,zipfile
r=Path('zhaoyun_study_20261012');s=r/'site';out=r/'deliverables';out.mkdir(exist_ok=True)
html=(s/'index.html').read_text().replace('<link rel="stylesheet" href="style.css">','<style>'+(s/'style.css').read_text()+'</style>').replace('<script src="data.js" defer></script>','').replace('<script src="app.js" defer></script>','')
html=html.replace('</body>','<script>'+(s/'data.js').read_text()+'</script><script>'+(s/'app.js').read_text()+'</script></body>')
for f in (s/'assets').iterdir():html=html.replace('assets/'+f.name,'data:'+mimetypes.guess_type(f.name)[0]+';base64,'+base64.b64encode(f.read_bytes()).decode())
(out/'zhaoyun-research-offline.html').write_text(html)
with zipfile.ZipFile(out/'zhaoyun-research-site.zip','w',zipfile.ZIP_DEFLATED)as z:
 for f in sorted(s.rglob('*')):
  if f.is_file():z.write(f,f.relative_to(s))
manifest=[{'path':str(f.relative_to(s)),'bytes':f.stat().st_size,'sha256':hashlib.sha256(f.read_bytes()).hexdigest()}for f in sorted(s.rglob('*'))if f.is_file()]
(out/'file-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2));print(len(manifest),'files;',sum(x['bytes']for x in manifest),'bytes')
