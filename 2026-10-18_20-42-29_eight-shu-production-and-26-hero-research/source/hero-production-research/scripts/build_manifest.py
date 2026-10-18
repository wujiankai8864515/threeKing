import json, pathlib, datetime, hashlib, collections
root=pathlib.Path('hero-production-research')
tz=datetime.timezone(datetime.timedelta(hours=8)); now=datetime.datetime.now(tz)
out=root/now.strftime('%Y-%m-%d_%H-%M-%S_UTC+08');out.mkdir(exist_ok=True)
paths={
'wei':root/'2026-10-18_20-02-02_UTC+08/魏十将_四卡三传记_完整研究制作包_v2.json',
'wu':root/'2026-10-18_20-31-08_UTC+08/吴八将_四卡三传记_完整研究制作包_v3.json',
'qun':root/'2026-10-18_20-31-10_UTC+08/群八将_四卡三传记_完整研究制作包_v2.json'}
allh=[];packs={};sources={};cards=[];bios=[];checks=[]
for faction,p in paths.items():
 d=json.loads(p.read_text());packs[faction]={'json':str(p),'markdown':str(p.with_suffix('.md')),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'count':len(d['heroes']),'common_requirements':d['common_requirements']}
 for h in d['heroes']:
  assert h['faction']==faction
  assert len(h['cards'])==4 and len(h['biographies'])==3
  es={e['event_id']:e for e in h['event_candidates']}
  chronology=[es[x['event_id']]['chapter'] for x in h['cards']]
  assert chronology==sorted(chronology)
  assert [x['target_stage'] for x in h['biographies']]==[2,3,4]
  for b,c in zip(h['biographies'],h['cards'][1:]):
   assert b['target_card_id']==c['asset_id']
   if b['event_id']!=c['event_id']:
    assert h['hero_id']=='xuchu' and b['event_id']=='b' and c['event_id']=='c'
    assert es[b['event_id']]['chapter']==es[c['event_id']]['chapter']==12  # 解缚归军直接引出初战，并非跨题故事
  assert [x['count'] for x in h['gameplay']['stages']]==[1,2,3,4]
  assert len(h['gameplay']['passives'])==4
  for x in h['gameplay']['passives']:assert len(x['name'])==2
  for x in h['cards']+h['biographies']:
   assert es[x['event_id']]['source_class']=='novel_text_verified'
   assert x['actual_reference_files']==[]
  for e in h['event_candidates']:
   url=e['source_url']; s=sources.setdefault(url,{'url':url,'source_class':'primary_novel_text','work':'毛本三国演义','chapter':e['chapter'],'checked_on':'2026-10-18','supports':[]})
   s['supports'].append({'hero_id':h['hero_id'],'event_id':e['event_id'],'title':e['title'],'evidence_paraphrase':e['evidence'],'selection':e['selection']})
  g=h['modern_game_reference']
  for k in ['url','secondary_version_url','crosscheck_url']:
   if k in g:
    s=sources.setdefault(g[k],{'url':g[k],'source_class':'modern_official_game_not_novel','checked_on':'2026-10-18','supports':[]})
    s['supports'].append({'hero_id':h['hero_id'],'version':g['version'],'evidence_paraphrase':g['verified'],'use_boundary':g['use'],'reference_field':k})
  allh.append(h)
  for c in h['cards']:cards.append({'hero_id':h['hero_id'],'name':h['name'],**c})
  for b in h['biographies']:bios.append({'hero_id':h['hero_id'],'name':h['name'],**b})
  checks.append({'hero_id':h['hero_id'],'name':h['name'],'faction':faction,'card_chapters':chronology,'count_4_cards_3_bios':True,'bio_direct_target_connection':True,'relation_exception':('12回解缚归军是同回斩李封初战的直接前因；非要求镜头完全同一事件' if h['hero_id']=='xuchu' else None),'source_class_selected_verified':True,'two_char_passives':True,'passive_counts':[1,2,3,4],'actual_identity_reference_supplied':False,'images_generated':0,'user_art_approved':False})
assert len(allh)==26 and len(cards)==104 and len(bios)==78
assert len({h['hero_id'] for h in allh})==26
assert len({x['asset_id'] for x in cards+bios})==182
queue=json.loads(pathlib.Path('hero-roster-research/2026-10-18_19-19-26_UTC+08/roster_status_queue.json').read_text())
qd={x['hero_id']:x for x in queue['roster']}
for h in allh:
 assert qd[h['hero_id']]['status']=='source_research_ready'
 assert qd[h['hero_id']]['research_brief_path']==str(paths[h['faction']])
compare=[
 {'heroes':['张辽','乐进','于禁','张郃','徐晃'],'boundary':'五子依次为侧面切后、近身持续压力、驻阵减伤、友军移位、敌人能量抑制；尖翼刀骑/矮壮短枪/方整镇阵/细长转身枪/重斧断路，神相与轮廓不共享。'},
 {'heroes':['许褚','张飞','典韦'],'boundary':'许褚白额重虎、横厚低身、可见蓄力舍防重斩；张飞既定虎形断喝与当前生命压血；典韦巨巫祖影、双短戟、一次部分替伤，不给典韦虎头或真实族属断言。'},
 {'heroes':['吕蒙','许褚'],'boundary':'吴v3已纠正：吕蒙停手整备的收益是单体短缴械，刀击仅普通威力；许褚蓄力收益是高伤且蓄时降防。两者不得重新同化为蓄力高伤+减防。'},
 {'heroes':['孙策','马超','吕布'],'boundary':'吴v2起已纠正：孙策对未曾伤害的新目标接战，奖励换敌；马超既定开局正面骑阵破盾；吕布固定目标正面格挡压制，不给三人同一个开局冲锋。'},
 {'heroes':['周瑜','陆逊','黄盖','庞统'],'boundary':'周瑜一次广域火击；陆逊有限相邻地面火段；黄盖消耗自身盾的短扇火浪；庞统既定少量火印后引燃。不同资源、时空结构和剪影。'},
 {'heroes':['张角','诸葛亮','郭嘉'],'boundary':'张角原地可打断风暴持续伤害；诸葛亮既定布局迟滞后定点雷；郭嘉单敌主动后结算谋记，不用同一雷球法阵。'},
 {'heroes':['典韦','赵云','张郃','左慈','董卓'],'boundary':'典韦部分替伤不反击；赵云既定刺击护救再回锋；张郃直接移动友军；左慈一个不可攻击的幻影替本体挡一次普攻；董卓单敌嘲讽并消耗本战生命上限。共同有防护含义，但触发对象、代价与操作不同。'},
 {'heroes':['曹操','荀彧','孙权','刘备','华佗','孙尚香'],'boundary':'曹操承压积令强化一人下一普攻；荀彧直接补一人能量；孙权把己方可转换攻击增益换盾；刘备既定群体增益治疗；华佗一人治疗并有限清持续伤害；孙尚香伙伴命中后一次补箭。'},
 {'heroes':['徐晃','贾诩','甘宁','貂蝉'],'boundary':'徐晃只压能量恢复；贾诩只禁他人提供的治疗；甘宁移除一个可驱散正增益；貂蝉仅改向一次普攻。资源轴和干预类型互不偷换。'},
 {'heroes':['袁绍','黄忠','孙尚香'],'boundary':'袁绍有限不同敌人各一箭，不把缺额叠单体；黄忠既定远距锁定精射；孙尚香单伙伴一次追随射击。'},
]
corrections=[
'魏v2：典韦第10回逐鹿过涧，动物是鹿；第16回守门未着甲、双戟被盗，临时用步卒腰刀后刀毁。',
'魏v2：第68回曹休射凌统马，甘宁射乐进面；并非许褚射箭救乐进。',
'魏v2：张辽合肥第67回所核小说桥战为二千余骑，不把史传八百强塞这一镜。张郃街亭拦王平，断水部署归司马懿命申耽申仪。',
'魏v2：许褚第12回拖两牛尾，第59回裸衣斗马超未分胜负；徐晃第30回与史涣截粮，韩猛逃走不是被斩。',
'吴完整包：甘宁斩黄祖在39回，孙夫人撤武在55回，吕蒙75回退职换将计由陆逊提出。',
'吴v2/v3：孙策删除开局冲锋，改换新目标接战；吕蒙删除准备高伤降防，改整备后短缴械，保持与马超、许褚差异。',
'群完整包：吕布赤兔始于第3回李肃赠马后；诛董时李肃割首、吕布刺戟；辕门射戟150步。',
'群完整包：张角第1回完整早期递进；第2回纸人草马是张宝，不移给张角。华佗初治周泰15回，关羽75回，曹操与青囊托付78回；23回医者为吉平。',
'群完整包：袁绍22回黎阳军步骑各15万合30万，檄文陈琳作；左慈68回堂下鱼池钓鱼，铜盘不能冒充本章。',
'年龄改编：貂蝉原著8回二八，本项目20+；孙策父死后8回称17，本项目统一20+面貌，均明确原创年龄改编。',
'左慈视损眼与跛足原著不定左右；项目固定左眼/右腿仅为连续性原创，不能进阶换侧或自动治好。'
]
counts={'heroes':26,'wei':10,'wu':8,'qun':8,'cards':104,'biographies':78,'planned_primary_images':182,'active_proposals':26,'passive_proposals':104,'images_generated':0}
manifest={'schema_version':'1.0','created_at':now.isoformat(),'scope':'魏10吴8群8文本研究；不包含蜀8生产成果，也不证明182张已生成','counts':counts,'authoritative_packages':packs,'hero_index':[{'hero_id':h['hero_id'],'name':h['name'],'faction':h['faction'],'package':str(paths[h['faction']]),'per_hero_brief':str(paths[h['faction']].parent/h['hero_id']/'brief.json'),'symbol':h['myth_symbol_proposal']['name'],'core_loop':h['gameplay']['core_loop'],'chapters':[es for es in next(c['card_chapters'] for c in checks if c['hero_id']==h['hero_id'])],'status':h['status']} for h in allh],'source_registry':str(out/'来源核验登记_v1.json'),'qa':str(out/'26将文本研究QA_v1.json'),'cross_hero_differentiation':compare,'source_and_revision_corrections':corrections,'remaining_gates':['机制、技能拟名、神话象征与角色造型均属提案待定稿','先制身份样并审查；生成时须实际附身份、武器、事件参考','逐图检查脸手兵器轴、骑乘、材质和叙事后，才进入UI及用户审美验收','本轮不负责生成、上传、Git同步或图库发布']}
(out/'魏吴群26将_总索引_v1.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
(out/'魏吴群26将_合并研究包_v1.json').write_text(json.dumps({'schema_version':'1.1','created_at':now.isoformat(),'counts':counts,'faction_requirements':{f:d['common_requirements'] for f,d in packs.items()},'heroes':allh},ensure_ascii=False,indent=2))
(out/'逐图生产清单182场景_v1.json').write_text(json.dumps({'cards':cards,'biographies':bios,'images_generated':0},ensure_ascii=False,indent=2))
(out/'来源核验登记_v1.json').write_text(json.dumps({'checked_on':'2026-10-18','note':'主事件逐章人工核验后登记；现代官方游戏仅作版本明确的参考，来源未用作神话设定证据。官方页面直接打开失败时使用可读的官方索引正文并在个人条目披露。','count':len(sources),'sources':list(sources.values())},ensure_ascii=False,indent=2))
(out/'26将文本研究QA_v1.json').write_text(json.dumps({'counts':counts,'structure_checks':checks,'cross_hero_manual_review':compare,'queue_current_paths_match':True,'unique_asset_ids':182,'single_effect_passives_manual_review':True,'limitations':'单效果与人物差异为文本人工审阅结论，不等于平衡、实现或成图验收。所有真实参考文件仍待制作附入。'},ensure_ascii=False,indent=2))
lines=['# 魏吴群26将制作研究总索引',f'时间：{now.isoformat()}','', '已完成：26名英雄，104张卡、78张目标卡传记，共182个逐图文本场景。实际生成图像0张。','', '## 使用这一组版本']
for f,d in packs.items():lines.append(f'- {f}：[可读制作包](../{pathlib.Path(d["markdown"]).relative_to(root)})；[结构化包](../{pathlib.Path(d["json"]).relative_to(root)})。')
lines+=['','每个英雄均附：候选事件与来源、四卡三传记的直接关系、脸发体衣甲兵器坐骑、逐图镜头与结构要求、神话力量成长、原创第一人称短词、四阶单效果两字被动、主动核心与待定边界。','', '## 26人速查']
for h in manifest['hero_index']:lines += [f'### {h["name"]}｜{h["symbol"]}',f'- 四卡回目：{h["chapters"]}。',f'- 核心：{h["core_loop"]}',f'- [逐人 brief](../{pathlib.Path(h["per_hero_brief"]).relative_to(root)})。']
lines+=['','## 跨角色边界']
for x in compare:lines.append('- '+'、'.join(x['heroes'])+'：'+x['boundary'])
lines+=['','## 已纠正的易错来源与版本']+['- '+x for x in corrections]
lines+=['','## 仍需制作的内容']+['- '+x for x in manifest['remaining_gates']]+['','## 同目录文件','- 魏吴群26将_合并研究包_v1.json：全部26人完整结构化内容。','- 逐图生产清单182场景_v1.json：104卡与78传记的资产ID、来源、镜头、结构与限制。','- 来源核验登记_v1.json：逐章小说与独立官方游戏来源。','- 26将文本研究QA_v1.json：结构、路径、唯一ID与人工差异审阅结果。','', '较早同名v1、v2文件保留用于追溯，不再作为当前生产输入；以本总索引所列三个权威包为准。']
(out/'魏吴群26将_总索引_v1.md').write_text('\n'.join(lines))
(root/'LATEST.json').write_text(json.dumps({'updated_at':now.isoformat(),'manifest':str(out/'魏吴群26将_总索引_v1.json'),'readme':str(out/'魏吴群26将_总索引_v1.md'),'packages':{f:{k:v for k,v in d.items() if k!='common_requirements'} for f,d in packs.items()}},ensure_ascii=False,indent=2))
(root/'README.md').write_text('# 当前制作研究入口\n\n[魏吴群26将总索引]('+str((out/'魏吴群26将_总索引_v1.md').relative_to(root))+')\n\n26人、182个文本场景；无新图生成或成图批准。机器入口见 LATEST.json。当前权威版本：魏v2、吴v3、群v2。\n')
print(out);print(counts);print('unique sources',len(sources))
