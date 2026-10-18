from PIL import Image, ImageDraw
from pathlib import Path
p=Path('./liubei-set/blackiron_redraw_20261018_190120_UTC+08');q=p/'qa-100pct';q.mkdir(exist_ok=True)
a=Image.open('./liubei-set/blackiron_identity_20261018_185301_UTC+08/刘备-黑铁-v1-织席编履身份候选.png').convert('RGB');b=Image.open(p/'刘备-黑铁-v2-清爽神话重绘候选.png').convert('RGB')
for name,box in {'face':(450,185,710,465),'hands-work-sandal':(315,585,820,960),'robe-material':(330,440,950,780),'faint-dragon':(10,0,470,290)}.items():
 ca,cb=a.crop(box),b.crop(box);w,h=ca.size;panel=Image.new('RGB',(2*w+8,h+26),'#181818');d=ImageDraw.Draw(panel);d.text((6,6),'REJECTED v1 @ 100%',fill='white');d.text((w+14,6),'REDRAW v2 @ 100%',fill='white');panel.paste(ca,(0,26));panel.paste(cb,(w+8,26));panel.save(q/(name+'-comparison.png'))
for name,box in {'finished-sandals':(0,1200,440,1430),'woven-mat-wall':(845,20,1024,700),'stool-wood-reed':(700,970,1024,1360),'foreground-ground':(0,1360,1024,1536),'lower-robe':(450,880,780,1250)}.items():
 c=b.crop(box);panel=Image.new('RGB',(c.width,c.height+26),'#181818');panel.paste(c,(0,26));ImageDraw.Draw(panel).text((6,6),'LIU BEI v2 @ NATIVE 100%',fill='white');panel.save(q/(name+'.png'))
source=Image.open('./guanyu-mythic-set/materialclean_20261018_180135_UTC+08/桃园结义-v10-分材质清理候选.png').convert('RGB');ca=source.crop((270,285,460,485));cb=b.crop((470,225,660,425));w,h=ca.size;panel=Image.new('RGB',(w*2+8,h+26),'#181818');d=ImageDraw.Draw(panel);d.text((6,6),'DELIVERED LIU FACE @ 100%',fill='white');d.text((w+14,6),'REDRAW v2 @ 100%',fill='white');panel.paste(ca,(0,26));panel.paste(cb,(w+8,26));panel.save(q/'identity-native-comparison.png')
print(q)
