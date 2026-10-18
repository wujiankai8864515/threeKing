from pathlib import Path
import argparse,base64,hashlib,json,tempfile,zipfile
ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--output',type=Path);ap.add_argument('--verify-only',action='store_true');a=ap.parse_args()
manifest=json.loads(Path(__file__).with_name('CURRENT40.json').read_text());total=0
for pkg in manifest['packages']:
 with tempfile.TemporaryDirectory(prefix='threeKing-zip-check-') as temp:
  folder=Path(temp) if a.verify_only else a.output
  if folder is None:raise SystemExit('--output required unless --verify-only')
  folder.mkdir(parents=True,exist_ok=True);target=folder/pkg['filename']
  with zipfile.ZipFile(target,'w') as z:
   z.comment=base64.b64decode(pkg['comment'])
   for e in pkg['entries']:
    data=(a.repo/e['repository_path']).read_bytes() if 'repository_path' in e else base64.b64decode(e['embedded_base64'])
    assert hashlib.sha256(data).hexdigest()==e['sha256'],e['filename']
    info=zipfile.ZipInfo(e['filename'],tuple(e['date_time']))
    for field in ['compress_type','create_system','create_version','extract_version','external_attr','internal_attr','flag_bits']:setattr(info,field,e[field])
    for field in ['extra','comment']:setattr(info,field,base64.b64decode(e[field]))
    z.writestr(info,data)
    total+='repository_path' in e
  assert hashlib.file_digest(target.open('rb'),'sha256').hexdigest()==pkg['original_sha256'],pkg['filename']
print(json.dumps({'packages_verified':len(manifest['packages']),'images_verified':total,'original_zip_bytes_reproduced':True}))
