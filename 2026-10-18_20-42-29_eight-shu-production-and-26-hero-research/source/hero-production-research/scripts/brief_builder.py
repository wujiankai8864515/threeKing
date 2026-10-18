import json, datetime, pathlib, fcntl, os
TZ=datetime.timezone(datetime.timedelta(hours=8))
STAMP=datetime.datetime.now(TZ).strftime('%Y-%m-%d_%H-%M-%S_UTC+08')
OUT=pathlib.Path('hero-production-research')/STAMP
OUT.mkdir(parents=True,exist_ok=True)
(pathlib.Path('/tmp/production_outpath')).write_text(str(OUT))
N=lambda c:f'https://zh.wikisource.org/zh/三國演義/第{c:03d}回'
COMMON={
 'scope':'研究文本制作包，不含生成图片、成图验收、UI实现或仓库同步；10英雄×4卡+3传记=70张规划主图。',
 'canon':'以本包逐章核验的毛本《三国演义》文本为故事主轴。只证明小说叙述，不自动等同三国史实。现代游戏玩法另列，不用于证明原著事件。',
 'status':'所有神话象征、面貌造型、第一人称短词、技能名和机制均为本项目原创提案，未获用户最终批准。',
 'style':'原创英雄化神话插画，地面世界有具体营地、城池、山路、木石泥土；不摄影写实、不统一天宫，不以绿色/蓝色滤镜制造幻想感。',
 'faction':'魏只在独立UI徽章和少量衣带/结饰/内衬使用蓝色。各人的袍甲主色独立；早期吕布、袁绍、杨奉部队按事件旗号，不把魏字战旗塞入前期场景。',
 'materials':'皮肤自然骨相；布哑光大褶；马毛定向与肌肉面；木土各自纹理；金属只在有形体依据处反光。禁随机金粉、白黄针点、满脸闪粒和跨材质金属化。',
 'tiers':'1黑铁、2青铜、3白银、4黄金；黄金是收藏成熟表现，不等同称帝或道德无瑕，也不强制画到人物晚年。属性1/2/4/8仅沿用未平衡的基础属性方向，不扩张为技能、攻速和控制一起翻倍。',
 'skill_rules':'暂拟每星累计1/2/3/4条被动，每条两汉字且一个关键效果；主动保留同一核心操作，最多添加一个直接辅助效果；所有数值、冷却、持续、容量与敌人豁免规则待系统验证。无五星、复杂连锁、复活树或全能技能。',
 'reference_gate':'本轮没有新英雄获批身份样图。每图actual_reference_files为空是诚实缺口；生成前须先做身份/材质样并获检查，再实际附身份、动作兵器与场景参考，不能靠一句“沿用参考”假装已附。',
 'structural_qa':'长杆各可见段共一直轴；刀斧头、杆、双手和尾帽有真实连接；拇指对向包握、腕肘肩受力可行。骑乘须查鞍位、人马重心、缰绳与兵器不穿插；不可为装入框把长兵缩短。',
 'delivery_gate':'七主图、四阶UI与总览分计；插画不烧文字；脸、手、武器轴、坐骑、材质保存100%裁切。原生尺寸按实际记录，不把放大标原生4K。技术通过不等于用户审美批准。',
 'generation_specs':{'card':'竖幅2:3，无字；暂按可得1024×1536源，不承诺原生4K','biography':'横幅3:2，无字；暂按1536×1024源','composition':'脸手兵器在UI安全区内，长杆和坐骑允许合理出画；传记前清后柔，关键配角不能糊成无身份。'},
}
heroes=[]
def ev(id,chapter,title,fact,selection,why,misread=''):
 return dict(event_id=id,chapter=chapter,chronology_key=f'{chapter:03d}-{id}',title=title,source_url=N(chapter),source_class='novel_text_verified',verified_on='2026-10-18',evidence=fact,selection=selection,selection_reason=why,misreading_to_avoid=misread)
def sc(t,event,title,camera,action,environment,myth,structure,retain,avoid):
 return dict(stage=t,event_id=event,title=title,camera=camera,action=action,environment=environment,myth_growth=myth,structure_check=structure,must_retain=retain,must_not_inherit=avoid,actual_reference_files=[],status='text_brief_ready_identity_sample_pending')
def bio(t,event,title,camera,action,relation,line,structure):
 return dict(target_stage=t,event_id=event,title=title,camera=camera,action=action,target_connection=relation,first_person_line_original=line,line_status='原创假设性过场短词，不是原著引文或人物历史原话',structure_check=structure,actual_reference_files=[],status='text_brief_ready_identity_sample_pending')
def skills(hid,active,core,extra,passives,visual):
 ps=[]
 for i,(name,effect,trigger,target) in enumerate(passives,1):
  assert len(name)==2
  ps.append(dict(skill_id=f'{hid}_p{i}',name=name,type='passive',unlocked_at=i,core_effect=effect,trigger=trigger,target=target,duration_or_cooldown='见触发；时长/上限/系数待平衡',basis='仅该效果对应的基础属性或状态，不推定真实伤害',visual=visual,growth='随进阶提高该单一效果的幅度；不附加无关效果',status='original_proposal_not_final'))
 return dict(core_loop=core,active=dict(skill_id=f'{hid}_a1',name=active,type='active',stages=[1,2,3,4],core_effect=core,extra_effect=extra,trigger='玩家指令或简明自动策略；两者由战斗系统定稿',target='见核心循环',duration_or_cooldown='待定，不预填伪精确数值',basis='攻击/防御/资源轴依角色定义；不默认真伤、秒杀或无敌',visual=visual,growth='1星可用核心，2星稳定幅度，3星最多加入所列单一辅助，4星扩大该能力熟练度；不新增职业',status='original_proposal_not_final'),passives=ps,stages=[dict(star=i,passive_ids=[p['skill_id'] for p in ps[:i]],count=i) for i in range(1,5)],not_final=['技能拟名','机制','星级被动条数方案','持续/冷却/倍率','控制与首领豁免'])
def hero(hid,name,personality,symbol,distinct,identity,game,events,cards,bios,mechanics):
 h=dict(hero_id=hid,name=name,faction='wei',core_personality=personality,myth_symbol_proposal=symbol,differentiation=distinct,identity=identity,modern_game_reference=game,event_candidates=events,cards=cards,biographies=bios,gameplay=mechanics,status='source_research_ready',production_status='not_generated_not_approved')
 for i,c in enumerate(cards,1):
  c.update(asset_id=f'{hid}_card_{i}',asset_type='card',tier=['黑铁','青铜','白银','黄金'][i-1],event_source_url=next(e['source_url'] for e in events if e['event_id']==c['event_id']),design_class='原著事件上的原创神话构图与服装提案')
 for i,b in enumerate(bios,1):
  b.update(asset_id=f'{hid}_bio_{i}',asset_type='biography',target_card_id=f'{hid}_card_{b["target_stage"]}',event_source_url=next(e['source_url'] for e in events if e['event_id']==b['event_id']),design_class='原著关系与转折上的原创镜头')
 assert len(cards)==4 and len(bios)==3
 heroes.append(h)
def finalize(batch):
 now=datetime.datetime.now(TZ).isoformat()
 data=dict(schema_version='1.1',created_at=now,output_directory=str(OUT),batch=batch,common_requirements=COMMON,counts={'heroes':len(heroes),'cards':len(heroes)*4,'biographies':len(heroes)*3,'primary_images_planned':len(heroes)*7,'images_generated':0},heroes=heroes)
 p=OUT/f'{batch}.json';p.write_text(json.dumps(data,ensure_ascii=False,indent=2))
 lines=[f'# 英雄逐人制作研究：{batch}',f'生成时间：{now}','',f'本文件含{len(heroes)}名英雄、{len(heroes)*7}个逐图场景。仅文本研究，不是成图完成。','## 全局放行边界']
 for k,v in COMMON.items():lines.append(f'- {k}：{v if isinstance(v,str) else json.dumps(v,ensure_ascii=False)}')
 for h in heroes:
  lines += ['',f'## {h["name"]}',f'核心：{h["core_personality"]}',f'差异：{h["differentiation"]}',f'神话提案：{json.dumps(h["myth_symbol_proposal"],ensure_ascii=False)}','### 形象与武器证据']
  for k,v in h['identity'].items():lines.append(f'- {k}：{v}')
  lines += ['### 现代游戏参照（与原著证据分开）',json.dumps(h['modern_game_reference'],ensure_ascii=False),'### 事件候选、顺序与取舍']
  for e in h['event_candidates']:
   lines += [f'- 第{e["chapter"]}回「{e["title"]}」：{e["evidence"]} [{e["source_class"]}]({e["source_url"]})',f'  取舍：{e["selection"]}；{e["selection_reason"]}；误读边界：{e["misreading_to_avoid"]}']
  lines += ['### 四张卡']
  for c in h['cards']:
   lines += [f'#### {c["stage"]}星{c["tier"]}：{c["title"]}（{c["asset_id"]}）',f'原著：[对应回目]({c["event_source_url"]})；以下镜头和神话为原创。']
   for k in ['camera','action','environment','myth_growth','structure_check','must_retain','must_not_inherit']:lines.append(f'- {k}：{c[k]}')
  lines += ['### 三段目标卡传记']
  for b in h['biographies']:
   lines += [f'#### {b["title"]} → {b["target_card_id"]}',f'原著：[对应回目]({b["event_source_url"]})']
   for k in ['camera','action','target_connection','first_person_line_original','structure_check']:lines.append(f'- {k}：{b[k]}')
   lines.append('- 短词为本项目原创，非引文。')
  lines += ['### 玩法提案（未定稿）',json.dumps(h['gameplay'],ensure_ascii=False,indent=2)]
 (OUT/f'{batch}.md').write_text('\n'.join(lines))
 # Atomic locked queue update protects sibling faction workers. Read current file under lock.
 qpath=pathlib.Path('hero-roster-research/2026-10-18_19-19-26_UTC+08/roster_status_queue.json')
 lockpath=pathlib.Path('/tmp/hero_roster_queue.lock')
 with lockpath.open('w') as lock:
  fcntl.flock(lock,fcntl.LOCK_EX)
  q=json.loads(qpath.read_text())
  q['status_definitions']['source_research_ready']='该英雄四卡三传记的事件证据、细化场景与技能提案已齐；不代表身份样、成图或用户批准。'
  for item in q['roster']:
   matches=[h for h in heroes if h['hero_id']==item['hero_id']]
   if matches:
    h=matches[0];item.update(status='source_research_ready',research_brief_path=str(p),research_verified_on='2026-10-18',role_direction_draft=h['gameplay']['core_loop'],generated_in_this_batch=0,art_final_approved=False)
  q['updated_at']=now
  temp=qpath.with_suffix('.tmp.research');temp.write_text(json.dumps(q,ensure_ascii=False,indent=2));os.replace(temp,qpath)
 return data

def finish(batch, faction):
 for h in heroes: h['faction']=faction
 data=finalize(batch)
 checks=[]
 for h in heroes:
  events={e['event_id']:e for e in h['event_candidates']}
  chapters=[events[c['event_id']]['chapter'] for c in h['cards']]
  assert chapters==sorted(chapters)
  assert [c['stage'] for c in h['cards']]==[1,2,3,4]
  assert [b['target_stage'] for b in h['biographies']]==[2,3,4]
  for i,b in enumerate(h['biographies'],1): assert b['event_id']==h['cards'][i]['event_id']
  for x in h['cards']+h['biographies']: assert events[x['event_id']]['source_class']=='novel_text_verified'
  assert all(len(p['name'])==2 for p in h['gameplay']['passives'])
  assert [s['count'] for s in h['gameplay']['stages']]==[1,2,3,4]
  d=OUT/h['hero_id']; d.mkdir(exist_ok=True);(d/'brief.json').write_text(json.dumps(h,ensure_ascii=False,indent=2))
  checks.append({'hero_id':h['hero_id'],'four_cards_three_direct_bios':True,'selected_source_verified':True,'chronology_order':chapters,'passive_two_characters':True,'passive_counts':[1,2,3,4],'images_generated':0,'identity_sample_approved':False})
 (OUT/(batch+'_QA.json')).write_text(json.dumps({'checks':checks,'scope':'文本结构与来源人工核查后的结构校验；不是成图验收','counts':data['counts']},ensure_ascii=False,indent=2))
 return data
