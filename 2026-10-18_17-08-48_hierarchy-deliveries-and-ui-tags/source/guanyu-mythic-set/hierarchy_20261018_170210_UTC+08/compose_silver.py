from PIL import Image
from pathlib import Path
p=Path(__file__).parent;r=p.parent
im=Image.open(r/'pure/silver-qualityhierarchy-20261018_170456.png').convert('RGBA')
im=Image.alpha_composite(im,Image.open(r/'revision_20261018_155650_UTC+08/silver-plaque-layer.png')).resize((881,1321),Image.Resampling.LANCZOS)
z=Image.new('RGBA',(1024,1536));z.paste(im,(72,125));b=Image.new('RGBA',z.size);b.paste(z,(0,0),Image.open(r/'art-clip-mask.png'))
Image.alpha_composite(Image.alpha_composite(b,Image.open(r/'frames/silver.png')),Image.open(r/'frames/silver-stars-ui.png')).save(p/'03-白银·关前扬威.png')
