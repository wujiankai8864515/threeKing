from pathlib import Path
from PIL import Image
p=Path(__file__).parent
art=Image.open(p/'illustration.png').convert('RGBA')
mask=Image.open(p/'art-clip-mask.png').convert('L')
frame=Image.open(p/'frame.png').convert('RGBA')
labels=Image.open(p/'dynamic-labels.png').convert('RGBA')
base=Image.new('RGBA',art.size)
base.paste(art,(0,0),mask)
# Explicit invocation creates a local rebuilt copy; never changes Library.
Image.alpha_composite(Image.alpha_composite(base,frame),labels).save(p/'rebuilt-card.png')
