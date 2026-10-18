from pathlib import Path
import json
P=Path(__file__).resolve().parent
src=Path('zhangfei-set/ui-compact_2026-10-18_23-03-30_UTC+08/compose_layout.py').read_text()
a=src.index('P=Path(');b=src.index('# Title is')
head='''P=Path(__file__).resolve().parent
R=P.parent
BASE=Path('/workspace/scratch/3f82ff2b3f81/zhangfei-set/ui_newframe_2026-10-18_19-32-00_UTC+08')
D=P/'ui';D.mkdir(exist_ok=True)
SIZE=(1190,1786);SX=1190/1024;SY=1786/1536;OFFSET=(84,145)
fields={};sources={};original_titles={t:'张飞' for t in ['iron','bronze','silver','gold']}
passives=['锐意','敏枪','开疆']
for i,t in enumerate(['iron','bronze','silver','gold']):
 fields[t]={'country':'吴','title':'孙策','level':'1','advancement':['初','勇','烈','雄'][i],'skills':[{'name':n,'level':'+'+str(max(1,i))} for n in passives[:[1,1,2,3][i]]],'status':'拟定技能，非正式平衡值'}
 sources['blackiron' if t=='iron' else t]={'path':str(P/'raw'/f'card{i+1:02}.png')}
overrides={t:Path(sources[t]['path']) for t in ['bronze','silver','gold']}
'''
src=src[:a]+head+src[b:]
src=src.replace(".replace(html.escape(original_titles[tier]),html.escape(f['title']))", ".replace(html.escape(original_titles[tier]),html.escape(f['title'])).replace('蜀','吴').replace('#285b31','#bf4b19').replace('#072413','#61200d')")
src=src.replace("'title remains current user-facing 张飞; all other example fields unchanged'","'孙策；吴橘红；被动锐意/敏枪/开疆均为拟定单效果'" )
src=src.replace("'张飞-四阶UI排版修复总览.png'","'孙策-四阶UI总览.png'")
# Remove inherited summary claims and write specific ones below.
src=src[:src.index("(D/'修复说明.txt')")]
(P/'compose_layout.py').write_text(src)
