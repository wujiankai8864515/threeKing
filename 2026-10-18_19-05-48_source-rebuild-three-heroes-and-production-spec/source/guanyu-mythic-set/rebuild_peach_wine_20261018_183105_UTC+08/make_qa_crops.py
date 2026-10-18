from PIL import Image, ImageDraw
from pathlib import Path
root=Path('./guanyu-mythic-set')
out=root/'rebuild_peach_wine_20261018_183105_UTC+08';qa=out/'qa-100pct';qa.mkdir(exist_ok=True)
sources={
 'taoyuan':(root/'materialclean_20261018_180135_UTC+08/桃园结义-v10-分材质清理候选.png',out/'桃园结义-v11-神话源重绘候选.png'),
 'wine':(root/'materialclean_20261018_180135_UTC+08/温酒请战-v10-分材质清理候选.png',out/'温酒请战-v11-神话拖刀源重绘候选.png')}
regions={
 'taoyuan':{'liu-face-hand':(265,270,555,480),'guan-face-hand':(655,225,870,490),'zhang-face-hand':(980,295,1305,515),'root-stone-grass':(350,805,1000,1024),'bark-trunk':(490,0,1040,240),'stone-metal-cloth':(380,535,970,850)},
 'wine':{'guan-face-reinhand':(650,95,875,360),'liu-zhang-cao':(85,440,515,805),'new-full-blade-shaft-hand':(170,405,595,980),'weapon-arm':(440,190,720,560),'horse':(635,240,1015,1024),'cloth':(960,420,1265,860),'ground-stone-grass':(0,765,660,1024)}}
for name,pair in sources.items():
 a,b=[Image.open(p).convert('RGB') for p in pair];assert a.size==b.size==(1536,1024)
 for label,rect in regions[name].items():
  ca,cb=a.crop(rect),b.crop(rect);w,h=ca.size
  panel=Image.new('RGB',(w*2+8,h+26),'#181818');d=ImageDraw.Draw(panel)
  d.text((6,6),'DESIGN SOURCE v10 @ 100%',fill='white');d.text((w+14,6),'NEW CANDIDATE v11 @ 100%',fill='white')
  panel.paste(ca,(0,26));panel.paste(cb,(w+8,26));panel.save(qa/f'{name}-{label}.png')
print(qa)
