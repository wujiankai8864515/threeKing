from PIL import Image, ImageDraw
from pathlib import Path
p=Path('./guanyu-mythic-set/wine_tailfix_20261018_184456_UTC+08');q=p/'qa-100pct';q.mkdir(exist_ok=True)
a=Image.open('./guanyu-mythic-set/rebuild_wine_retry_20261018_183817_UTC+08/温酒请战-v12-中段握持后拖源重绘候选.png').convert('RGB')
b=Image.open(p/'温酒请战-v13-尾帽局修候选.png').convert('RGB')
for name,box in {'tail-end':(790,290,970,440),'full-axis':(330,310,910,770),'grip-arm':(690,315,890,510),'face-reinhand':(895,65,1105,340),'horse':(850,215,1230,1024),'front-ground':(0,740,650,1024)}.items():
 ca,cb=a.crop(box),b.crop(box);w,h=ca.size;panel=Image.new('RGB',(2*w+8,h+26),'#181818');d=ImageDraw.Draw(panel);d.text((6,6),'SOURCE v12 @ 100%',fill='white');d.text((w+14,6),'CANDIDATE v13 @ 100%',fill='white');panel.paste(ca,(0,26));panel.paste(cb,(w+8,26));panel.save(q/(name+'.png'))
print(q)
