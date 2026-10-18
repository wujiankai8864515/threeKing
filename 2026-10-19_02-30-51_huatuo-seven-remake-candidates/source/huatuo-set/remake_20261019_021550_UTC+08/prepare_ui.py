from pathlib import Path
P=Path(__file__).resolve().parent
src=Path('xunyu-set/remake_20261019_011235_UTC+08/ui/compose_layout.py').read_text()
src=src.replace("for f in fields.values():f['title']='荀彧'", "for f in fields.values():f['title']='华佗';f['country']='群'")
src=src.replace("['济用','节用','广援']", "['仁术','缓脉','济急']").replace("{'济用':'主动补充的能量量提高','节用':'主动冷却缩短','广援':'主动施放距离提高'}", "{'仁术':'单次治疗量提高','缓脉':'主动治疗能量消耗降低','济急':'对低生命友军治疗量提高'}")
src=src.replace("base_svg=re.sub(r'<g transform", "base_svg=base_svg.replace('魏','群').replace('#285c85','#70458c').replace('#071c35','#241334')\n base_svg=re.sub(r'<g transform",1)
a=src.index(" '<g transform=\"translate(900 1424)\"")
b=src.index(",base_svg)",a)
src=src[:a]+''' '<g transform="translate(900 1424)" fill="none" stroke="#fff7df" stroke-width="5"><path d="M -30 12 Q -25 38 0 38 Q 25 38 30 12 Z" fill="#b7ccaa"/><path d="M -15 10 L 20 -29 Q 28 -34 32 -25 L 5 10"/><path d="M -25 -9 Q -43 -24 -28 -38 Q -6 -33 -11 -14 Z" fill="#b7ccaa"/></g>' '''+src[b:]
src=src.replace('荀彧四阶','华佗四阶').replace('荀彧-四阶','华佗-四阶').replace('「荀彧」','「华佗」')
(P/'ui/compose_layout.py').write_text(src)
