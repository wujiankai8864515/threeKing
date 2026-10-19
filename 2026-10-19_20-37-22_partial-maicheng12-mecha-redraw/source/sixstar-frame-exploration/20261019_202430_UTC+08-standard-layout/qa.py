from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,hashlib
P=Path(__file__).resolve().parent
M=json.loads((P/'manifest.json').read_text());baseline=Image.open(P/'reference-standard-sixstar-frame.png');ba=np.array(baseline.getchannel('A'));u0=None;checks=[]
for r in M:
 f=Path(r['output']);folder=f.parent;ui=Image.open(r['text_layer']).convert('RGBA');ar=np.array(ui)
 if u0 is None:u0=ar
 name=Image.new('RGBA',ui.size);name.paste(ui.crop((540,60,920,150)),(540,60));name.save(folder/'dynamic-name-only.png')
 ui_without=ui.copy();ui_without.paste((0,0,0,0),(540,60,920,150));ui_without.save(folder/'dynamic-ui-without-name.png')
 checks.append({'id':r['frame_material']['id'],'frame_alpha_matches_standard':bool(np.array_equal(ba,np.array(Image.open(folder/'frame-6star.png').getchannel('A')))),'dynamic_ui_pixel_changes_vs_first':int(np.any(ar!=u0,axis=2).sum()),'uncovered_art_pixel_changes':r['uncovered_art_pixels_changed'],'original_art_offset':r['illustration_offset'],'all_glyph_anchors':r['glyph_centers']})
(P/'QA-layout.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2))
(P/'sha256.json').write_text(json.dumps({str(f.relative_to(P)):hashlib.sha256(f.read_bytes()).hexdigest() for f in P.rglob('*.png')},ensure_ascii=False,indent=2))
