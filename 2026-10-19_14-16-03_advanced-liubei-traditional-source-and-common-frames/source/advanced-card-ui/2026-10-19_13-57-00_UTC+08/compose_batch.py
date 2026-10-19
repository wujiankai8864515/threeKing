import json,importlib.util
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
P=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('rc',P/'render_cards.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
def batch(hero,name,branch,bid,srcs,names):
 results=[]
 for t,source in zip([5,6],srcs):
  cfg=dict(hero=hero,name=name,branch=branch,branch_id=bid,tier=t,source=str(Path(source).resolve()),skills=[dict(name=n,level=t-4) for n in names])
  (P/f'{hero}-{bid}-{t}-config.json').write_text(json.dumps(cfg,ensure_ascii=False,indent=2));results.append(m.compose(cfg))
 im=Image.new('RGB',(800,650),'#20222a');d=ImageDraw.Draw(im);font=ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',19)
 for i,r in enumerate(results):
  a=Image.open(r['output']);a.thumbnail((400,600));im.paste(a,(i*400,0),a)
 d.text((15,610),name+' · '+branch+' · 五星 → 六星 / 候选',font=font,fill='white');im.save(P/'cards'/f'{hero}-{bid}-pair.png');return results
if __name__=='__main__':
 import sys
 c=json.loads(Path(sys.argv[1]).read_text());print(json.dumps(batch(**c),ensure_ascii=False))
