from pathlib import Path
from PIL import Image,ImageDraw
D=Path(__file__).parent;Q=D/'qa-100pct';Q.mkdir(exist_ok=True);im=Image.open(D/'黄忠-黑铁-v1-长沙老将身份候选.png').convert('RGB')
for box,name in [((345,130,555,380),'face-white-beard.png'),((175,260,490,540),'right-hand-full-arrow.png'),((700,575,900,890),'left-grip-arm.png'),((690,125,985,1370),'complete-bow-string.png'),((860,130,975,285),'upper-tip-string.png'),((700,1190,795,1370),'lower-tip-string.png'),((250,350,730,800),'armor-cloth.png'),((140,820,725,1190),'lower-cloth.png'),((0,630,225,1290),'wood-rack-stone.png'),((0,1290,1024,1536),'near-ground-feet.png'),((580,0,1024,295),'distant-sun-arc.png')]:
 c=im.crop(box);o=Image.new('RGB',(c.width,c.height+26),'#222222');o.paste(c,(0,26));ImageDraw.Draw(o).text((5,7),'HUANG ZHONG v1 NATIVE 100%',fill='white');o.save(Q/name)
print(len(list(Q.glob('*.png'))))
