from PIL import Image
from pathlib import Path
D=Path(__file__).parent
im=Image.open(D/'gold-metal-native-2048.png').convert('RGBA');tx=Image.open(D/'text-overlay-2048.png');im=Image.alpha_composite(im,tx);im.save(D/'gold-complete-native-2048.png');bg=Image.new('RGBA',im.size,'#162025');bg.alpha_composite(im);bg.resize((512,768),Image.Resampling.LANCZOS).save(D/'gold-preview.png');bg.crop((40,20,670,570)).save(D/'gold-corner-100pct.png');bg.crop((1280,1980,1970,2600)).save(D/'gold-passive-100pct.png');bg.crop((1680,450,1920,1110)).save(D/'gold-stars-100pct.png')
