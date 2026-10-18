from pathlib import Path
from PIL import Image, ImageDraw
D=Path(__file__).parent
Q=D/'qa-100pct';Q.mkdir(exist_ok=True)
a=Image.open(D/'刘备-青铜-v1-聚义护众候选.png').convert('RGB')
b=Image.open(D/'刘备-青铜传记-v1-城中调停候选.png').convert('RGB')
def crop(im,box,name,label):
 c=im.crop(box);out=Image.new('RGB',(c.width,c.height+26),'#222222');out.paste(c,(0,26));ImageDraw.Draw(out).text((8,7),label,fill='white');out.save(Q/name)
for box,name in [((330,180,565,425),'card-face.png'),((700,390,1010,565),'card-open-hand.png'),((60,790,680,1360),'card-sword-full-axis.png'),((175,340,750,800),'card-cloth-metal.png'),((0,1260,1024,1536),'card-foreground.png'),((100,0,500,310),'card-dragon.png'),((660,570,1024,1250),'card-protected-people.png')]: crop(a,box,name,'BRONZE CARD @ NATIVE 100%')
for box,name in [((670,140,860,365),'bio-liu-face.png'),((245,90,440,360),'bio-guan-face.png'),((1160,150,1390,385),'bio-zhang-face.png'),((320,335,750,565),'bio-liu-left-chain.png'),((860,335,1185,575),'bio-liu-right-chain.png'),((0,580,175,765),'bio-guan-outer-hand.png'),((350,610,485,840),'bio-guan-inner-hand.png'),((1050,625,1190,840),'bio-zhang-inner-hand.png'),((1290,575,1500,720),'bio-zhang-belt-hand.png'),((440,820,1080,1024),'bio-foreground-cloth-stone.png'),((0,850,255,1024),'bio-near-basket.png')]:crop(b,box,name,'BRONZE BIOGRAPHY @ NATIVE 100%')
print(len(list(Q.glob('*.png'))),'native crops',Q)
