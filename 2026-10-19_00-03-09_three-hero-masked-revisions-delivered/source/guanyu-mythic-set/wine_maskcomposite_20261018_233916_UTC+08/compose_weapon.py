from PIL import Image, ImageDraw, ImageFilter
from pathlib import Path
import numpy as np, json, hashlib
p=Path(__file__).parent
orig_full=Image.open(p/'source-v13-frozen.png').convert('RGB'); orig=Image.open(p/'weapon-edit-crop-1024x768.png').convert('RGB'); patch=Image.open(p/'generated-patch-native-crop.png').convert('RGB')
a=np.array(orig)
poly=[(650,251),(660,265),(640,280),(616,297),(586,317),(575,339),(558,369),(531,405),(498,435),(462,461),(421,482),(393,491),(365,486),(345,472),(340,454),(368,452),(399,442),(432,424),(461,402),(482,378),(493,354),(508,351),(529,331),(537,317),(555,305),(574,296),(588,282),(612,269),(631,259)]
tassel=[(572,322),(585,335),(581,356),(581,380),(576,407),(570,422),(547,422),(528,412),(522,402),(539,376),(549,348),(559,329)]
mask=Image.new('L',(1024,768),0);d=ImageDraw.Draw(mask);d.polygon(poly,fill=255);d.polygon(tassel,fill=255);m=np.array(mask)
Image.fromarray(m).save(p/'old-head-extraction-mask.png')
rgba=orig.convert('RGBA');rgba.putalpha(Image.fromarray(m));rgba.save(p/'original-head-extracted.png')
# Preview only; final compositing follows after mask validation.
checker=np.zeros((768,1024,3),np.uint8)
for y in range(768):
 for x in range(1024):checker[y,x]=[75,75,75] if ((x//12+y//12)%2) else [160,160,160]
prev=Image.fromarray(checker);prev.paste(orig,(0,0),Image.fromarray(m));prev.crop((330,245,665,505)).resize((670,520)).save(p/'qa-head-extraction-checker.png')
