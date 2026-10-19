from pathlib import Path
import subprocess,json,importlib.util
from PIL import Image
import numpy as np
P=Path(__file__).resolve().parent
# Authored vector strokes following the viewed reference's bold oblique calligraphic silhouette.
strokes='M25 24 Q55 23 92 12 L105 19 Q102 29 88 30 L36 39 Q27 38 25 24 Z M13 51 Q58 42 108 35 L119 44 L111 56 Q67 55 23 67 Z M65 23 L81 30 Q72 63 61 80 Q48 106 15 121 L9 112 Q39 91 49 69 Q59 47 65 23 Z M65 62 L77 59 Q89 83 119 100 L129 117 Q110 122 94 104 Q74 86 65 62 Z'
def svg(path,body,w,h):
 path.write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">'+body+'</svg>');subprocess.run(['inkscape',str(path),'--export-filename='+str(path.with_suffix('.png'))],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
defs='<defs><linearGradient id="gold" x1="0" y1="0" x2="0.18" y2="1"><stop stop-color="#fffef1"/><stop offset=".32" stop-color="#ffeaa6"/><stop offset=".48" stop-color="#c18a32"/><stop offset=".55" stop-color="#fff0bb"/><stop offset="1" stop-color="#dcaa55"/></linearGradient></defs>'
body=defs+f'<g transform="translate(6 8)"><path d="{strokes}" fill="#422117" stroke="#251712" stroke-width="10" stroke-linejoin="round"/><path d="{strokes}" fill="url(#gold)" stroke="#fff1b3" stroke-width="1.5" transform="translate(-2 -4)"/></g>'
svg(P/'tian-metal-calligraphy.svg',body,150,145)
# Readable central spear leaf, two curving side blades, short socket. Not a generic diamond.
spear='M60 9 L76 47 L68 70 L66 93 L54 93 L52 70 L44 47 Z M37 45 L38 65 L48 74 L48 85 L30 77 L26 54 Z M83 45 L82 65 L72 74 L72 85 L90 77 L94 54 Z M48 92 L72 92 L72 104 L48 104 Z'
svg(P/'spearhead.svg',defs+f'<path d="{spear}" fill="url(#gold)" stroke="#261d18" stroke-width="4" stroke-linejoin="round"/><path d="M60 17 L60 89" stroke="#fffce7" stroke-width="3"/>',120,115)
base=Path('/workspace/scratch/3f82ff2b3f81/guanyu-advanced/shared-ui_20261019_190000_UTC+08/render_guanyu.py').read_text()
base=base.replace(" measures.append(center(d,(155*SX,1384*SY),cfg['branch'],int(44*SX)))", " badge=Image.open(str(ASSET/'tian-metal-calligraphy.png')).convert('RGBA');layer.alpha_composite(badge,(round(155*SX-75),round(1384*SY-72.5)))")
a=base.index(' # Troop class remains');b=base.index(' canvas.alpha_composite(layer)',a)
base=base[:a]+" icon=Image.open(str(ASSET/'spearhead.png')).convert('RGBA');layer.alpha_composite(icon,(round(901*SX-60),round(1411*SY-57.5)))\n"+base[b:]
base="ASSET=__import__('pathlib').Path(__file__).resolve().parent\n"+base
(P/'render.py').write_text(base)
s=importlib.util.spec_from_file_location('r',P/'render.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
configs=[Path('guanyu-advanced/piloted-dragon-mecha_20261019_184125_UTC+08/ui-final_20261019_190350_UTC+08/config.json'),Path('guanyu-advanced/demon-asura_20261019_185502_UTC+08/revision_20261019_190247_UTC+08/config.json')]
results=[]
for i,cp in enumerate(configs):
 c=json.loads(cp.read_text());old=Path(c['outdir'])/(f"{c['hero']}-{c['branch_id']}-{c['tier']}star.png");c['outdir']=str(P/('mecha' if i==0 else 'demon'));c['branch']='天';r=m.compose(c);a=np.array(Image.open(old));b=np.array(Image.open(r['output']));diff=np.any(a!=b,axis=2);allow=np.zeros(diff.shape,bool);allow[1500:1710,60:320]=1;allow[1540:1720,950:1150]=1;assert not(diff&~allow).any();r['compared_to']=str(old);r['outside_two_UI_regions_changed']=int((diff&~allow).sum());results.append(r)
(P/'manifest.json').write_text(json.dumps(results,ensure_ascii=False,indent=2))
