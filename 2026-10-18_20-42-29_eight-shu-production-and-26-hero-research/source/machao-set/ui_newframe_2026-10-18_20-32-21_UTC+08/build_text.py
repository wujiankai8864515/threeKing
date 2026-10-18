from pathlib import Path
import json,html,subprocess
from PIL import Image
D=Path(__file__).parent
fields={'country':'蜀','title':'马超','level':'1','advancement':'','skills':[{'name':'先驱','level':'+2'},{'name':'摧锋','level':'+2'},{'name':'震阵','level':'+2'}],'status':'All values are layout examples only, not final mechanics'}
(D/'text-config.json').write_text(json.dumps(fields,ensure_ascii=False,indent=2))
head='<svg xmlns="http://www.w3.org/2000/svg" width="2048" height="3072" viewBox="0 0 1024 1536"><defs><style>.cn{font-family:Noto Serif CJK SC;font-weight:700}.sans{font-family:Noto Sans CJK SC;font-weight:500}</style></defs>'
a=[head]
def txt(t,x,y,size,cls='cn',anchor='middle'):
 t=html.escape(t);base=f'x="{x}" y="{y}" font-size="{size}" class="{cls}" text-anchor="{anchor}" dominant-baseline="central"';a.append(f'<text {base} transform="translate(0 2)" fill="#080808" stroke="#080808" stroke-width="3.2" paint-order="stroke">{t}</text><text {base} fill="#fff7df" stroke="#302310" stroke-width="1.8" paint-order="stroke">{t}</text>')
txt(fields['country'],144,132,62);txt(fields['title'],630,90,45);txt('LV',909,105,26,'sans');txt(fields['level'],909,148,48,'sans');txt(fields['advancement'],148,1385,78)
for y,sk in zip([962,1048,1132],fields['skills']):txt(sk['name'],730,y,38,'sans','start');txt(sk['level'],903,y,35,'sans','end')
# Simple replaceable polearm-infantry layout icon, separate from rank and illustration.
a.append('<g transform="translate(900 1424)" fill="#fff7df" stroke="#302310" stroke-width="2.4"><path d="M -3 30 L -3 -33 L 2 -43 L 7 -29 L 4 -7 L 4 30 Z M -8 -32 L -22 -18 L -23 15 L -10 21 L -10 10 L -15 6 L -14 -12 L -6 -20 Z M 9 -24 L 22 -12 L 23 15 L 11 22 L 11 11 L 16 7 L 15 -7 L 8 -14 Z"/><path d="M -18 31 L 18 31 L 18 37 L -18 37 Z"/></g></svg>')
(D/'text-overlay.svg').write_text(''.join(a));subprocess.run(['inkscape',str(D/'text-overlay.svg'),'--export-filename='+str(D/'text-overlay-native-2048.png')],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
im=Image.open(D/'gold-empty-generated-1024.png').convert('RGBA');im.alpha_composite(Image.open(D/'text-overlay-native-2048.png').resize(im.size,Image.Resampling.LANCZOS));im.save(D/'gold-frame-with-ui-native-1024.png');bg=Image.new('RGBA',im.size,'#19242a');bg.alpha_composite(im);bg.resize((512,768),Image.Resampling.LANCZOS).save(D/'gold-frame-with-ui-preview-512.png')
