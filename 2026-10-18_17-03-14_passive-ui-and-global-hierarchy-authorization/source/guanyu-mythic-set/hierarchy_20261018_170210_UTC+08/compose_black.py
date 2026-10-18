from PIL import Image
from pathlib import Path
p=Path(__file__).parent;r=p.parent
im=Image.open(p/'blackiron-pure.png').convert('RGBA').resize((881,1321),Image.Resampling.LANCZOS)
z=Image.new('RGBA',(1024,1536));z.paste(im,(72,125));b=Image.new('RGBA',z.size);b.paste(z,(0,0),Image.open(r/'art-clip-mask.png'))
Image.alpha_composite(Image.alpha_composite(b,Image.open(r/'frames/blackiron.png')),Image.open(r/'frames/blackiron-stars-ui.png')).save(p/'01-黑铁·市井潜龙.png')
