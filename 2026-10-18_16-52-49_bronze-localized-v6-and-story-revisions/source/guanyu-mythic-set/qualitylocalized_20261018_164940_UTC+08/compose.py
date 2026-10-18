from PIL import Image
from pathlib import Path
p=Path(__file__).parent;r=p.parent
im=Image.open(p/'bronze-pure.png').convert('RGBA').resize((881,1321),Image.Resampling.LANCZOS)
z=Image.new('RGBA',(1024,1536));z.paste(im,(72,125));b=Image.new('RGBA',z.size);b.paste(z,(0,0),Image.open(r/'art-clip-mask.png'))
Image.alpha_composite(Image.alpha_composite(b,Image.open(r/'frames/bronze.png')),Image.open(r/'frames/bronze-stars-ui.png')).save(p/'02-青铜·三骑追黄巾.png')
