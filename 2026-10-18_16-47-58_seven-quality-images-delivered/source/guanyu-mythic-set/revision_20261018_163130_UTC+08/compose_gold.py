from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
p=Path(__file__).parent;r=p.parent
im=Image.open(r/'pure/gold-v5-frame-safe-20261018_163042.png').convert('RGBA');layer=Image.new('RGBA',im.size);d=ImageDraw.Draw(layer);font=ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc',27);d.text((985,817),'刘',font=font,fill='#ead18e',stroke_width=1,stroke_fill='#702b20',anchor='mm');layer.save(p/'刘旗独立字层.png');im=Image.alpha_composite(im,layer);im.save(p/'gold-pure-with-liu-flag.png')
a=im.resize((881,1321),Image.Resampling.LANCZOS);z=Image.new('RGBA',(1024,1536));z.paste(a,(72,125));b=Image.new('RGBA',z.size);b.paste(z,(0,0),Image.open(r/'art-clip-mask.png'));Image.alpha_composite(Image.alpha_composite(b,Image.open(r/'frames/gold.png')),Image.open(r/'frames/gold-stars-ui.png')).save(p/'04-黄金·护行拖刀.png')
