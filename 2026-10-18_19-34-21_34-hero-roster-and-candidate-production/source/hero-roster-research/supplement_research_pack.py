import json,hashlib,datetime,pathlib
p=pathlib.Path('hero-roster-research/2026-10-18_19-19-26_UTC+08')
now=datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8))).isoformat()
def read(n):return json.loads((p/n).read_text())
def write(n,o):(p/n).write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n')
s=read('sources.json'); ids={r['id'] for r in s['sources']}
def src(i,title,url,cls='modern_game_primary',scope='仅作游戏名单、版本和玩法参照；不作史实或原著情节证据。'):
 if i not in ids:s['sources'].append(dict(id=i,title=title,url=url,source_class=cls,verified_on='2026-10-18',use_scope=scope));ids.add(i)
for r in s['sources']:
 if r['id']=='G_ROSTER':r['url']='https://x.sanguosha.com/';r['use_scope']='2026年10月8日站内将池公告可核验所选阵营名单；动态首页会更新，不单独证明早期扩展包归属或旧版技能。'
for i,title,url in [
('G_GUO2013','2013国战官方武将牌目录与乐进骁果','https://guozhan.sanguosha.com/a/kapaiyilan/wujiangpai/wei/2013/0126/47.html'),
('G_ZHANGLIAO','三国杀OL张辽：突袭','https://www.sanguosha.com/hero/18'),
('G_YUJIN2014','2014于禁调整：毅重改为节钺','https://www.sanguosha.com/news/20141113_6631_0514'),
('G_YUJIN_NOW','三国杀OL于禁现行介绍页：镇军','https://www.sanguosha.com/hero/160'),
('G_ZHANGHE','三国杀OL张郃：巧变','https://www.sanguosha.com/hero/50'),
('G_XUHUANG2016','2016林包徐晃：断粮','https://www.sanguosha.com/news/20161026_4323_2512'),
('G_FIVEZI2016','2016官方列传讨论五子玩法差异','https://www.sanguosha.com/news/20160217_9678_2311'),
('G_SUNCE2016','2016山包孙策攻略','https://www.sanguosha.com/news/20161026_5541_3812'),
('G_JIAXU2016','2016林包贾诩攻略','https://www.sanguosha.com/news/20161026_1482_3412'),
('G_ZUOCI2014','2014山包左慈攻略','https://www.sanguosha.com/news/20140521_8678_1419'),
('G_POOL2021','2021官方排位将池：标准、神话再临及其他扩展','https://sanguosha.com/news/20210527_1480_2517')]:src(i,title,url)
novels={1:'张角太平要术与黄巾起事',3:'董卓入京、吕布与赤兔',8:'王允与貂蝉连环计',9:'董卓败亡及贾诩建言',15:'孙策江东创业与神亭争斗',16:'吕布辕门射戟、宛城与于禁整军立营',30:'官渡与乌巢',44:'孙权定抗曹、周瑜督军',54:'孙夫人婚姻与持械侍婢',68:'甘宁百骑劫营、左慈戏曹操',75:'华佗刮骨疗毒与吕蒙白衣渡江',78:'华佗治曹操与青囊书',84:'陆逊火烧连营'}
for n,t in novels.items():src(f'N{n:03d}',f'《三国演义》第{n}回：{t}',f'https://zh.wikisource.org/{"wiki" if n==68 else "zh"}/三國演義/第{n:03d}回','novel_text','只证明演义情节与本版本文字，不等同史实。公版原著，现代校录载于维基文库。')
s['updated_at']=now;write('sources.json',s)
wei=[
 dict(hero_id='zhangliao',name='张辽',reference_version='官网标准张辽页面，核验2026-10-18',game_reading='突袭以改变摸牌方式取得他人手牌，侧重资源与节奏控制。',original_role='切入后排，压制关键敌人的下一次行动；精兵奇袭，不做纯厚甲前排。',visual='紧凑束发、折线披风，前倾快切；少量精锐而非铺满骑兵。',boundary='与马超正面开阵区分；不把三国杀抽牌规则直接搬到即时战斗。',source_ids=['G_ZHANGLIAO','G_FIVEZI2016']),
 dict(hero_id='yuejin',name='乐进',reference_version='国战2013骁果；不冒称所有版本通用',game_reading='回合外施压，迫使对方付装备成本或受伤。',original_role='短周期主动压迫、追着敌人进攻间隙补击；小体型也有正面锐气。',visual='紧身短甲、低重心、短促步伐；第68回持枪与凌统交战可作兵器考证起点。',boundary='不开局一次冲完，不与马超抢同一种骑阵爆发；不把身材画成儿童。',source_ids=['G_GUO2013','N068']),
 dict(hero_id='yujin',name='于禁',reference_version='2014毅重→节钺；现官网镇军，分开记录',game_reading='早版重防守，节钺加入控制与防御转换，现页面镇军偏控制辅助。',original_role='整队守阵、抑制敌方突破；以第16回先筑营后辩谤的纪律为主轴。',visual='方正闭合甲片、竖直旗令、沉稳正面；营寨和队列秩序清楚。',boundary='守阵是本项目选择，不称为现版三国杀技能原样；不以水淹败降作唯一人格。',source_ids=['G_YUJIN2014','G_YUJIN_NOW','N016']),
 dict(hero_id='zhanghe',name='张郃',reference_version='官网巧变页面，核验2026-10-18',game_reading='牺牲或跳过阶段来转移场上牌，强调位置、时机和弹性。',original_role='变阵移位，扰乱敌方阵形或把队友调离危险；操作空间区别于直接伤害。',visual='修长、转身观察、横向衣摆，脚下山地斜线；原创军阵纹而非现代游戏蝶翼。',boundary='不照搬无双张郃的爪刃、蝶舞造型；专属兵器名未考证前不写。',source_ids=['G_ZHANGHE','G_FIVEZI2016']),
 dict(hero_id='xuhuang',name='徐晃',reference_version='2016林包断粮；后版新增内容不混入',game_reading='干扰敌方获取资源，克制持续依赖补给的对手。',original_role='持续压制恢复或能量补给，稳步拆防线；具体只选一个资源轴定稿。',visual='宽肩厚实、横向受力、粗大斧形轮廓可作待核造型方向；粮道、辎重断面构图。',boundary='不默认同时减疗、减能、减攻速；斧与演义具体阶段需个人考证后定。',source_ids=['G_XUHUANG2016','G_FIVEZI2016'])]
wu=[
('sunquan','孙权','标准核心；早期国战目录可核验','主君组织与资源调度','第44回定抗曹与用周瑜：取决断、用人，不套刘备治疗。',['G_GUO2013','G_POOL2021','N044']),
('sunce','孙策','山包，官方2016攻略明示','短程强攻与进取成长','第15回小霸王创业和神亭交锋，保留吴阵营前期创业线。',['G_SUNCE2016','N015']),
('zhouyu','周瑜','标准核心；早期国战目录可核验','大范围火攻与统军','第44、49回督军、赤壁火攻；大面水战焰幕，与庞统火印、陆逊推进火线分开。',['G_GUO2013','N044','N049']),
('lumeng','吕蒙','标准核心；早期国战目录可核验','隐藏意图后的定点突破','第75回白衣渡江，伪装、纪律和突然控制；不与甘宁夜袭混成同一镜头。',['G_GUO2013','N075']),
('luxun','陆逊','标准核心；早期国战目录可核验','耐心部署后推进火线','第84回等待敌疲与连营火攻，清俊书生将领；火线按地形推进，不做凤凰。',['G_GUO2013','N084']),
('ganning','甘宁','标准核心；早期国战目录可核验','高速袭扰与冒险切入','第68回百骑劫营有白鹅翎标记；锦帆、水盗背景作为后续四阶段考证方向。',['G_GUO2013','N068']),
('huanggai','黄盖','标准核心；早期国战目录可核验','主动付代价后突破','第47、49回苦肉与火船，老将船战；与黄忠弓手区分，不复制低血斩杀。',['G_GUO2013','N047','N049']),
('sunshangxiang','孙尚香','标准核心，通名来自现代人物传统/三国杀','轻装机动与武装协同','第54回孙夫人及持械侍婢提供尚武背景。小说称孙夫人，不能把孙尚香当原文姓名；弓/双刃专名另待核。',['G_GUO2013','G_POOL2021','N054'])]
qun=[
('lubu','吕布','用户明确；标准核心','正面极强武勇与单挑压制','第3回赤兔与戟、第16回辕门射戟。后续避免只复制关羽横刀姿态。',['G_GUO2013','N003','N016']),
('diaochan','貂蝉','用户明确；标准核心','离间目标关系与受击转移','第8、9回连环计，心计与抉择而非单纯美人肖像。技能转移是原创提案。',['G_GUO2013','N008','N009']),
('zhangjiao','张角','用户明确；经典风包方向','黄天符法与广域灾变','第1回太平要术、符水与起事。借书卷符箓轴，和诸葛亮谨慎布局的风雷分开。',['G_GUO2013','N001']),
('huatuo','华佗','用户明确；标准核心','专职救治与解除异常','第75、78回治疗与青囊书；诊治手势、青囊器物，避免套刘备君主加益。传记只讲小说，不提供现实医疗做法。',['G_GUO2013','N075','N078']),
('dongzhuo','董卓','补入；经典神话再临人物','高耐久与有代价的暴烈力量','第3、9回权势建立和败亡；宽大笼罩性剪影。暴政不包装成正义功绩。',['G_ROSTER','G_POOL2021','N003','N009']),
('yuanshao','袁绍','补入；经典神话再临人物','兵势压制与群体齐射','第30回官渡与乌巢，名门阵列、众军与秩序。群射为原创战斗方向，不能把史实成败机械转成数值。',['G_GUO2013','G_POOL2021','N030']),
('jiaxu','贾诩','补入；林包官方攻略明示','封锁救援与风险控制','第9回劝李傕郭汜返攻、第68回继嗣建言展示谋局跨度；药毒绿雾只是比喻，非原著职业毒师。',['G_JIAXU2016','N009','N068']),
('zuoci','左慈','补入；山包官方攻略明示','幻影误导与有限变换','第68回左慈戏曹操已有幻术叙事，适配神话层。低阶仅一种清晰幻影机制，避免复制任意技能的复杂规则。',['G_ZUOCI2014','N068'])]
selection=dict(created_at=now,status='selection_and_differentiation_brief_complete_not_full_individual_production_briefs',wei_five=wei,wu_selection=[dict(hero_id=i,name=n,classic_basis=b,original_role=r,novel_anchor=a,source_ids=so)for i,n,b,r,a,so in wu],qun_selection=[dict(hero_id=i,name=n,classic_basis=b,original_role=r,novel_anchor=a,source_ids=so)for i,n,b,r,a,so in qun],limits=['吴、群各8人固定边界；候补本批不自动加入。','经典名单不等于2026当前强度排名。','玩法总结只抽象借鉴，战斗机制、技能名和视觉均需原创。','本表不是21人的四卡三传记完成证明；下一阶段仍需逐人完整考证。','网页攻略为官方发布/收录资料，其中历史评语不作为小说或史实的证据。'])
write('wei_wu_qun_selection_briefs.json',selection)
r=read('roster_status_queue.json');r['updated_at']=now;r['scope']='已授权的34英雄全素材范围；本包交付研究与排期，尚未生成新图。';r['authorization']=dict(roster_scope='authorized',production_scope='four_stage_cards_and_three_biographies_per_hero',wu_qun_choice='selection_delegated_within_approximately_eight_each',detail_direction='project_proposals_for_review',image_generation_this_research='not_started')
for h in r['roster']:
 h.pop('user_final_approved',None);h['art_final_approved']=False
 if h['faction'] in ['wu','qun']:h['selection_research_file']='wei_wu_qun_selection_briefs.json'
 if h['hero_id'] in [x['hero_id'] for x in wei]:h['differentiation_research_file']='wei_wu_qun_selection_briefs.json'
r['roster_decisions'][-1]='吴与群新增人选在用户授权自选的范围内；细化造型与成图验收不因范围授权自动通过。'
r['next_actions']=['赵云身份/材质样准备包已完成，先交方向审阅，再按该包准备实际引用图与一张样；未生成。','通过样张后逐人扩成四卡三传记，每图原生100%裁切检查，再做UI落地与清单。','已有刘关张QA由现制作线继续；后续批次按bounded_batches逐组推进，不混报完成。']
r['bounded_batches']=[]
for bid,label,hs in [
('B0','刘关张既有素材复检',['liubei','guanyu','zhangfei']),
('B1','下一组五蜀',['zhaoyun','machao','huangzhong','zhugeliang','pangtong']),
('B2','魏五子',['zhangliao','yuejin','yujin','zhanghe','xuhuang']),
('B3','魏主君谋士护卫',['caocao','xunyu','guojia','dianwei','xuchu']),
('B4','吴主君都督',['sunquan','sunce','zhouyu','lumeng']),
('B5','吴水战与机动',['luxun','ganning','huanggai','sunshangxiang']),
('B6','群明确四人',['lubu','diaochan','zhangjiao','huatuo']),
('B7','群补选四人',['dongzhuo','yuanshao','jiaxu','zuoci'])]:
 r['bounded_batches'].append(dict(batch_id=bid,label=label,hero_ids=hs,planned_primary_images=7*len(hs),status='existing_qa_external_to_research'if bid=='B0'else('research_complete_identity_sample_prepared'if bid=='B1'else'scoped_next_research'),completion_criteria='每人四阶段源图+三张目标星级传记源图、技能文案与来源、实际引用图版本、原生尺寸/逐图裁切QA、UI总览、manifest与交付备份记录；不以样张或拼图替代源图。'))
r['stage_order']=['individual_research','direction_review','identity_material_sample','sample_quality_review','four_cards_three_biographies_expansion','native_crop_qa','ui_composition_qa','manifest_delivery_backup']
r['stop_conditions']=['当前研究交付至完整五蜀+名单索引+差异表+赵云身份样准备；本研究不启动图像工具。','后续制作的完成以各batch明确交付清单为准；需方向决定或工具授权时报告具体阻塞，不无期限空转。']
write('roster_status_queue.json',r)
prep=dict(created_at=now,hero_id='zhaoyun',asset_id='zhaoyun_identity_material_sample_v01',status='prepared_awaiting_direction_review_no_generation',counts_as_primary=False,purpose='先锁原创脸体、白布/银甲/枪杆材质，验证放大后结构；不是四卡之一，不占7张正式源图。',requested_canvas={'orientation':'portrait','requested_pixels':[1024,1536],'actual_pixels':None,'note':'生成后填工具实际输出，不把请求尺寸或后期放大写成原生尺寸。'},composition='大腿以上、三分之二正面站姿，目光安静坚定，双手完整露出。一手稳握近垂直枪杆、一手自然落在腰侧；枪刃与枪尾不必同时入画，但可见轴线不能折弯。简洁中性营地灰底，柔和侧光。暂不加入马匹、阿斗、群像、复杂腾龙。',face='成年初期，端正阔面、明确颌骨、清亮眼神、自然皮肤；原创面孔。保持修长但有肩背力量，不做少女脸或消瘦少年。',hair='整洁束发，几束自然发丝；无马超式披散长发。',costume='银灰分片金属护甲、低饱和深蓝内衬、哑光白袍。金属只在转折面出现连续反射，白布依折痕受光；无镶满宝石、无碎金点、无全身发亮。',weapon='项目原创亮银枪：笔直等径枪杆、明确握持、细长柳叶形钢刃；可有一束克制白缨。样张不携青釭剑，避免时间线误导。',symbol='本样以脸体材质为主，银白龙仅可作为背景极淡单一云弧，不与角色轮廓相交。完整神兽另做后续可读性验证。',prompt_draft='为原创神话三国卡牌建立赵云身份与材质样张。年轻成年的同一位中国将领，沉静、坚毅、阔面清目、结实修长；束发整洁。三分之二正面站姿，大腿以上，双手完整，持一杆笔直的项目原创亮银枪。银灰甲片为清晰大块金属结构，深蓝内衬，哑光白袍。白布、金属、皮革和皮肤各自材质明确。简洁灰色营地背景与柔和侧光。脸部细节清晰自然，边缘锐利而不过度锐化，宽阔干净的明暗面。原创脸，不参考任何演员或商业游戏角色的相貌。无文字、无边框、无水印、无星级、无UI。不要碎金点、随机银粉、密集花纹、塑料皮肤、额外手指、弯折枪杆、悬空握持、飘浮甲片、披散长发、黄金重甲、青釭剑。',reference_policy={'style_material_anchor':'可引用当前项目已审核的材质样，引用其结构清晰度与材料控制，不继承刘关张面孔。','new_identity_bootstrap':'本次是新角色身份建立，若无已批准赵云脸图则以文字定脸；样张通过后才成为后续6+素材的实际脸图参考。','actual_reference_files':[],'identity_reference_file':None,'not_reference':'旧目录中的赵云与阿斗小游戏研究截图不是当前英雄身份图；不自动使用。','execution_record_required':'真正执行时记录传入image工具的每个本地图路径与版本，不能只在文字中写参考了。'},qa_checks=['原生100%脸部：两眼视线、鼻口透视、脸部无随机高光颗粒。','原生100%双手与握持：手指数、枪杆穿握、手腕和前臂关节正确。','原生100%甲片与白袍：金属平面与织物折痕各自成立，无均匀撒点。','全图枪轴与身体重心正确，枪刃连接处完整。','灰度和缩略图可分出脸、甲、衣、枪四个主块。','与马超文字轮廓对照：束发/披发、冷白/暗灰沙红、护救/正面冲阵不重叠。'],after_sample=['记录实际尺寸、生成工具输出与引用图清单。','保存脸、手枪、甲布三个原生裁切，分别标通过/退回及可见理由。','只有样张通过后才将真实文件路径填入五蜀brief，并开始赵云正式四卡三传记。'])
write('zhaoyun_identity_sample_preparation.json',prep)
links={x['id']:f"[{x['title']}]({x['url']})"for x in s['sources']}
md=['# 魏五子差异与吴群选角补充',f'更新：{now}','','共34人不变。已有刘关张素材仍由原制作线复检；本文件为后续选角和研究提案，不宣称新素材完成。','', '## 魏五子：五个可辨认的战斗职责','']
for h in wei:
 md += [f"### {h['name']}",f"版本参照：{h['reference_version']}。{h['game_reading']}",f"原创方向：{h['original_role']}",f"视觉：{h['visual']}",f"边界：{h['boundary']}",'来源：'+'；'.join(links[i]for i in h['source_ids']), '']
for title,key in [('吴8人','wu_selection'),('群8人','qun_selection')]:
 md += ['## '+title,'']
 for h in selection[key]:md += [f"- **{h['name']}**：{h['classic_basis']}。提案职责：{h['original_role']}。{h['novel_anchor']}",'  来源：'+'；'.join(links[i]for i in h['source_ids'])]
 md+=['']
md+=['## 赵云身份样准备','只准备一张脸体与材质样，不计四卡三传记。竖版、大腿以上、站姿、双手与直枪可验；先去掉骑马、婴儿和复杂腾龙，以免多个难点掩盖身份问题。身份样通过后，其真实文件才作为扩量的脸部参考。完整提示、尺寸记录与六项QA见同目录 zhaoyun_identity_sample_preparation.json。','', '## 有界队列','每位仍是四卡三传记。B0=刘关张复检；B1=五蜀；B2=魏五子；B3=曹操/荀彧/郭嘉/典韦/许褚；B4=孙权/孙策/周瑜/吕蒙；B5=陆逊/甘宁/黄盖/孙尚香；B6=吕布/貂蝉/张角/华佗；B7=董卓/袁绍/贾诩/左慈。每批结束条件已写入 roster_status_queue.json。','',*['- '+x for x in selection['limits']]]
(p/'魏五子差异与吴群选角补充.md').write_text('\n'.join(md)+'\n')
# Correct attribution URL in the original human-facing brief, retaining all novel/design distinctions.
a=p/'下一批英雄名单与五名蜀将制作提案.md';t=a.read_text().replace('https://x.sanguosha.com/?from=AppAgg.com','https://x.sanguosha.com/');a.write_text(t)
m=read('manifest.json');m['updated_at']=now;m['files']=[]
for f in sorted(p.iterdir()):
 if f.name=='manifest.json' or not f.is_file():continue
 b=f.read_bytes();m['files'].append(dict(path=f.name,bytes=len(b),sha256=hashlib.sha256(b).hexdigest()))
m['checks'] += ['8 bounded batches cover all 34 heroes exactly once','Wei five role versions separated; Wu/Qun selection sources linked','Zhao identity sample text prepared; no image generated']
write('manifest.json',m)
# Validate all source IDs recursively, primary counts, batch coverage, and manifests.
def validate_sources(obj):
 if isinstance(obj,dict):
  for k,v in obj.items():
   if k=='source_ids':assert all(i in ids for i in v),(k,v)
   validate_sources(v)
 elif isinstance(obj,list):
  for x in obj:validate_sources(x)
for name in ['wei_wu_qun_selection_briefs.json','next_five_shu_briefs.json']:validate_sources(read(name))
rosterids=[h['hero_id']for h in r['roster']];batchids=[h for b in r['bounded_batches']for h in b['hero_ids']]
assert sorted(rosterids)==sorted(batchids),[set(rosterids)-set(batchids),set(batchids)-set(rosterids)]
assert len(rosterids)==len(set(rosterids))==34
assert sum(b['planned_primary_images']for b in r['bounded_batches'])==238
for f in m['files']:assert hashlib.sha256((p/f['path']).read_bytes()).hexdigest()==f['sha256']
print(json.dumps({'directory':str(p.resolve()),'files':len(m['files']),'heroes':34,'batches':8,'planned_primary_images':238,'new_images':0,'source_records':len(ids),'validation':'passed'},ensure_ascii=False))
