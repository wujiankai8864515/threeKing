from pathlib import Path
from PIL import Image,ImageDraw
D=Path(__file__).parent;Q=D/'qa-100pct';Q.mkdir(exist_ok=True);a=Image.open(D/'黄忠-青铜-v1-一箭报义候选.png').convert('RGB');b=Image.open(D/'黄忠-青铜传记-v1-受义还义候选.png').convert('RGB')
def cr(im,box,name):
 c=im.crop(box);o=Image.new('RGB',(c.width,c.height+26),'#222222');o.paste(c,(0,26));ImageDraw.Draw(o).text((3,7),'HUANG BRONZE NATIVE 100%',fill='white');o.save(Q/name)
for box,name in [((235,230,455,430),'card-face-drawhand-nock.png'),((735,340,985,510),'card-bowhand-arrow.png'),((310,15,880,845),'card-full-string-bow.png'),((625,15,730,135),'card-upper-nock.png'),((555,735,655,850),'card-lower-nock.png'),((775,870,1024,1190),'card-guan-target.png'),((80,470,620,1100),'card-cloth-armor.png'),((300,1280,840,1536),'card-feet-ground.png')]:cr(a,box,name)
for box,name in [((815,50,1050,300),'bio-huang-face.png'),((805,320,950,455),'bio-release-hand.png'),((1285,530,1445,775),'bio-bow-hand.png'),((1330,120,1510,990),'bio-full-bow-string.png'),((1400,125,1510,235),'bio-upper-nock.png'),((1350,865,1445,990),'bio-lower-nock.png'),((175,190,445,425),'bio-arrow-plume-guan.png'),((245,300,465,570),'bio-guan-face-hands.png'),((100,365,635,935),'bio-guan-horse.png'),((715,420,1275,1024),'bio-cloth-armor.png')]:cr(b,box,name)
print('QA',len(list(Q.glob('*.png'))),a.size,b.size)
