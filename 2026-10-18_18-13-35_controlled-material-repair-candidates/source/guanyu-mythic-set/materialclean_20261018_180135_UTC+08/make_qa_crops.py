from PIL import Image, ImageDraw
from pathlib import Path
root=Path('./guanyu-mythic-set')
out=root/'materialclean_20261018_180135_UTC+08'
qa=out/'qa-100pct';qa.mkdir(exist_ok=True)
sources={
 'taoyuan':(root/'pure/story-taoyuan-frontclear-20261018_174122.png',out/'桃园结义-v10-分材质清理候选.png'),
 'wine':(root/'weaponrepair_20261018_174725_UTC+08/温酒请战-v9-长柄修复候选.png',out/'温酒请战-v10-分材质清理候选.png')}
regions={
 'taoyuan':{'liu-face':(265,270,445,470),'guan-face':(655,225,855,445),'zhang-face':(1095,295,1305,495),'bark-roots':(365,845,1015,1024),'bark-trunk':(490,0,1040,240),'stone-and-metal':(350,660,950,970),'cloth':(940,470,1400,850)},
 'wine':{'guan-face':(650,95,875,325),'liu-zhang-cao':(85,440,515,805),'full-blade-shaft-hand':(195,15,610,810),'horse':(635,240,1015,1024),'cloth':(960,420,1265,860)}}
for name,pair in sources.items():
 a,b=[Image.open(p).convert('RGB') for p in pair]
 assert a.size==b.size==(1536,1024)
 for label,rect in regions[name].items():
  ca,cb=a.crop(rect),b.crop(rect)
  w,h=ca.size;panel=Image.new('RGB',(w*2+8,h+26),'#181818');d=ImageDraw.Draw(panel)
  d.text((6,6),'SOURCE @ 100%',fill='white');d.text((w+14,6),'CANDIDATE @ 100%',fill='white')
  panel.paste(ca,(0,26));panel.paste(cb,(w+8,26));panel.save(qa/f'{name}-{label}.png')
print(qa)
