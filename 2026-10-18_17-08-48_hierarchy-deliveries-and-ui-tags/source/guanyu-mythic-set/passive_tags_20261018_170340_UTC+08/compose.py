from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageFilter
import json,hashlib
D=Path(__file__).parent
base=D.parent/'qualitylocalized_20261018_165240_UTC+08/04-黄金·护行拖刀.png'
S=3;W,H=1024,1536
ui=Image.new('RGBA',(W*S,H*S))
font=ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',44*S)
placements=[]
for i,name in enumerate(['蓄势','斩将','武圣']):
 x,y,w,h=665,1018+i*91,277,76
 shape=[(x+66,y),(x+w,y),(x+w,y+h),(x,y+h)]
 pts=[(int(a*S),int(b*S)) for a,b in shape]
 mask=Image.new('L',ui.size);md=ImageDraw.Draw(mask);md.polygon(pts,fill=255)
 layer=Image.new('RGBA',ui.size);ld=ImageDraw.Draw(layer)
 for yy in range(h*S+1):
  t=yy/(h*S)
  if t<.43:
   v=t/.43;c=tuple(round(a+(b-a)*v) for a,b in zip((250,211,111),(235,168,49)))
  else:
   v=(t-.43)/.57;c=tuple(round(a+(b-a)*v) for a,b in zip((235,168,49),(155,84,17)))
  ld.line([(x*S,(y*S)+yy),((x+w)*S,(y*S)+yy)],fill=(*c,248),width=1)
 layer.putalpha(mask)
 ui=Image.alpha_composite(ui,layer);d=ImageDraw.Draw(ui)
 d.line(pts+[pts[0]],fill='#8f550f',width=3*S,joint='curve')
 inset=[((x+69)*S,(y+3)*S),((x+w-2)*S,(y+3)*S),((x+w-2)*S,(y+h-3)*S),((x+6)*S,(y+h-3)*S),((x+69)*S,(y+3)*S)]
 d.line(inset,fill='#ffe697',width=2*S,joint='curve')
 d.line([((x+76)*S,(y+9)*S),((x+29)*S,(y+h-8)*S)],fill='#f7dc8e',width=2*S)
 # Short passive name only; no level or numerical gameplay claim.
 d.text(((x+175)*S,(y+37)*S),name,font=font,anchor='mm',fill='#fffdf2',stroke_width=2*S,stroke_fill='#514017')
 placements.append({'name':name,'bounds':[x,y,w,h]})
ui=ui.resize((W,H),Image.Resampling.LANCZOS);ui.save(D/'passive-overlay.png')
card=Image.open(base).convert('RGBA');out=Image.alpha_composite(card,ui);out.save(D/'关羽-黄金-被动技能上卡预览.png');out.resize((480,720),Image.Resampling.LANCZOS).save(D/'review-480.png')
(D/'config.json').write_text(json.dumps({'status':'mockup-only, all skill names are placeholders','base_sha256':hashlib.sha256(base.read_bytes()).hexdigest(),'layout_reference':'user-images-1018/image(20261018-044056).png','placements':placements,'library_file_id':'libfile_9cde671bbad08191b7ce7f59a234cfdc','rejected_v0':'../passive_ui_20261018_170000_UTC+08/'},ensure_ascii=False,indent=2))
(D/'README.txt').write_text('被动技能布局示意 v1\n对照用户提供《啪啪三国2》参考图：右下三条斜切金色横标签，右对齐，无大图标。\n蓄势／斩将／武圣仅占位示例，非最终技能。\n从黄金 v7 原图重新合成，旧底部徽章已移除；底图文件完全未修改。\n透明层 passive-overlay.png；重建源 compose.py；位置与版本映射 config.json。\n')
