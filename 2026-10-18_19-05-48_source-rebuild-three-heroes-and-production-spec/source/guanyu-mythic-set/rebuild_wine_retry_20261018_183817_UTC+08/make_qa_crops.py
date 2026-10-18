from PIL import Image, ImageDraw
from pathlib import Path
p=Path('./guanyu-mythic-set/rebuild_wine_retry_20261018_183817_UTC+08');q=p/'qa-100pct';q.mkdir(exist_ok=True)
a=Image.open('./guanyu-mythic-set/rebuild_peach_wine_20261018_183105_UTC+08/温酒请战-v11-神话拖刀源重绘候选.png').convert('RGB')
b=Image.open(p/'温酒请战-v12-中段握持后拖源重绘候选.png').convert('RGB')
for name,box in {
'full-weapon-axis':(300,240,1040,790),'grip-tail-rein-contact':(675,255,1025,515),'weapon-arm':(670,175,935,495),'horse-anatomy':(785,210,1235,1024),'front-rock-grass':(0,720,690,1024),'ground-path':(570,780,1536,1024),'supporting-cast':(25,340,545,705),'face-armor':(750,60,1090,340)}.items():
 c=b.crop(box);canvas=Image.new('RGB',(c.width,c.height+26),'#181818');canvas.paste(c,(0,26));ImageDraw.Draw(canvas).text((6,6),'v12 @ NATIVE 100%',fill='white');canvas.save(q/(name+'.png'))
for name,ba,bb in [('face-identity',(690,100,880,330),(900,75,1090,305)),('support-cast',(70,440,520,805),(40,345,490,710))]:
 ca,cb=a.crop(ba),b.crop(bb);assert ca.size==cb.size
 w,h=ca.size;panel=Image.new('RGB',(w*2+8,h+26),'#181818');d=ImageDraw.Draw(panel);d.text((6,6),'SOURCE v11 @ 100%',fill='white');d.text((w+14,6),'CANDIDATE v12 @ 100%',fill='white');panel.paste(ca,(0,26));panel.paste(cb,(w+8,26));panel.save(q/(name+'-comparison.png'))
print(q)
