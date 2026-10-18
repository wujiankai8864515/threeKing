from pathlib import Path
from PIL import Image,ImageDraw
D=Path(__file__).parent;Q=D/'qa-100pct';Q.mkdir(exist_ok=True);im=Image.open(D/'黄忠-黑铁-v3-外侧持弓重构候选.png').convert('RGB')
for name,box in [('full-bow-string.png',(730,180,950,1385)),('upper-nock.png',(845,190,930,340)),('lower-nock.png',(835,1235,945,1385)),('grip-forearm.png',(575,545,825,855)),('right-hand-arrow.png',(115,260,430,540)),('face-beard.png',(300,125,490,380)),('cloth-armor.png',(175,335,650,1010)),('boots-clear-gap.png',(525,1170,960,1480))]:
 c=im.crop(box);o=Image.new('RGB',(c.width,c.height+26),'#222222');o.paste(c,(0,26));ImageDraw.Draw(o).text((3,7),'HUANG v3 NATIVE 100%',fill='white');o.save(Q/name)
s=Image.open('/workspace/scratch/3f82ff2b3f81/huangzhong-set/blackiron_fix_2026-10-18_19-43-00_UTC+08/黄忠-黑铁-v2-弦端与材质局修候选.png').convert('RGB');a=s.crop((345,130,535,385));b=im.crop((300,125,490,380));o=Image.new('RGB',(380,281),'#222222');o.paste(a,(0,26));o.paste(b,(190,26));dr=ImageDraw.Draw(o);dr.text((3,7),'v2 IDENTITY 100%',fill='white');dr.text((193,7),'v3 NEW POSE 100%',fill='white');o.save(Q/'identity-native-pair.png');print(len(list(Q.glob('*.png'))),im.size)
