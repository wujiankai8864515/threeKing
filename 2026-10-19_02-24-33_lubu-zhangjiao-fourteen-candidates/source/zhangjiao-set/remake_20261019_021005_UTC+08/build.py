from pathlib import Path
P=Path(__file__).resolve().parent
src=Path('diaochan-set/remake_20261019_020550_UTC+08/ui/compose_layout.py').read_text()
src=src.replace('貂蝉','张角').replace('第8回','第1回').replace("['察隙','持计','藏锋']","['聚霆','持咒','天幕']")
src=src.replace('M 0 30 L -32 -15 Q 0 -52 32 -15 Z','M -9 34 L -9 -30 L -16 -40 L 0 -46 L 16 -40 L 9 -30 L 9 34 Z').replace('M 0 30 L -16 -27 M 0 30 L 0 -34 M 0 30 L 16 -27','M -26 -14 L 27 -14 L 27 13 L -26 13 Z M -17 -5 L 17 -5 M -17 5 L 9 5')
(P/'ui/compose_layout.py').write_text(src)
