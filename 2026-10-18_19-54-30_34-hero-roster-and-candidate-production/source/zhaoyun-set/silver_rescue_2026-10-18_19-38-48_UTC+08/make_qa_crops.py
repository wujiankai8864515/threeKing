from pathlib import Path
from PIL import Image,ImageDraw
D=Path(__file__).parent;Q=D/'qa-100pct';Q.mkdir(exist_ok=True)
a=Image.open(D/'赵云-白银-v1-长坂扶危候选.png').convert('RGB');b=Image.open(D/'赵云-白银传记-v1-乱军寻主候选.png').convert('RGB')
def crop(im,box,name,label):
 c=im.crop(box);o=Image.new('RGB',(c.width,c.height+26),'#222222');o.paste(c,(0,26));ImageDraw.Draw(o).text((5,7),label,fill='white');o.save(Q/name)
for box,name in [((530,195,750,405),'card-face.png'),((425,370,680,620),'card-child-support.png'),((220,470,425,820),'card-spear-hand-tail.png'),((535,500,740,720),'card-rein-hand.png'),((0,0,420,850),'card-full-spear.png'),((280,640,745,1240),'card-rider-horse-contact.png'),((700,500,1024,1030),'card-horse-head.png'),((520,1050,1024,1536),'card-horse-forelegs.png'),((300,340,850,790),'card-cloth-armor.png')]:crop(a,box,name,'ZHAO YUN SILVER CARD NATIVE 100%')
for box,name in [((550,130,740,350),'bio-zhao-face.png'),((450,325,800,570),'bio-child-two-arms-support.png'),((170,280,440,505),'bio-caregiver-face.png'),((250,645,490,780),'bio-caregiver-hands.png'),((65,0,205,775),'bio-full-spear.png'),((930,150,1245,775),'bio-horse.png'),((425,510,1040,920),'bio-kneel-cloth-sheath.png'),((0,755,635,1024),'bio-near-rubble.png'),((1155,395,1536,725),'bio-civilians.png')]:crop(b,box,name,'ZHAO YUN SILVER BIOGRAPHY NATIVE 100%')
print(len(list(Q.glob('*.png'))),a.size,b.size)
