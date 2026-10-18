from PIL import Image
from pathlib import Path
p=Path(__file__).parent;r=p.parent
im=Image.open(r/'pure/gold-local-depth-finish-20261018_172405.png').convert('RGBA')
im=Image.alpha_composite(im,Image.open(r/'revision_20261018_163130_UTC+08/刘旗独立字层.png')).resize((881,1321),Image.Resampling.LANCZOS)
z=Image.new('RGBA',(1024,1536));z.paste(im,(72,125));b=Image.new('RGBA',z.size);b.paste(z,(0,0),Image.open(r/'art-clip-mask.png'))
Image.alpha_composite(Image.alpha_composite(b,Image.open(r/'frames/gold.png')),Image.open(r/'frames/gold-stars-ui.png')).save(p/'04-黄金·护行拖刀.png')
