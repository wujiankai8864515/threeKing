import json,csv,pathlib
p=pathlib.Path(__file__).parent
rows=[]
def add(id,platform,kind,date,source,url,names,method,averages=None,image=None,confidence='第三方，未经平台原始数据或审计验证'):
 rows.append(dict(id=id,platform=platform,kind=kind,data_date=date,published_date='2026-10-02' if source.startswith('DataEye') else '2026-10-12（页面数据日期，未单列发布时间）',source=source,source_url=url,collected_at='2026-10-12T09:18:00Z',method=method,confidence=confidence,image=image,top10=[dict(rank=i+1,name=n,average_rank=averages[i] if averages else None) for i,n in enumerate(names.split('|'))]))
u='https://www.10100.com/article/152896367'
s='DataEye×引力引擎月榜，经大数跨境转载；榜图人工核读'
m='2026年9月日排名平均值排序；不是整月收入加总。正文称微信畅销主要按IAP、新游有较高特殊加成。'
add('wx_sales_sep','微信','畅销','2026-09',s,u,'向僵尸开炮|三国：冰河时代|无尽冬日|疯狂水世界|浪漫餐厅|向往的生活|向末日开炮|梦幻消除战|永远的蔚蓝星球|我的花园世界',m,[1.5,2.0,4.8,6.1,6.9,7.5,8.4,8.7,10.0,10.8],'rankings/wx_sales_sep.png')
add('wx_play_sep','微信','畅玩','2026-09',s,u,'羊了个羊：星球|赵云与阿斗|一箭又一箭|抓大鹅|解压打毛线|解压闯一关|打个螺丝|猪了个猪|挪了下车|一找一个准','2026年9月日排名平均值排序；IAA导向的畅玩榜，不等于纯DAU榜或收入榜。',[1.1,1.9,3.4,3.8,5.9,7.1,7.6,10.0,11.3,12.0],'rankings/wx_play_sep.png')
add('dy_sales_sep','抖音','畅销','2026-09',s,u,'疯狂水世界|灵画师|造化仙府|时尚百货城|向僵尸开炮|三国：冰河时代|狱国争霸|镇邪人|梦幻消除战|向往的生活','2026年9月日排名平均值排序；页面没有披露抖音榜底层收入公式或权重，不可当审计收入排行。',[1.6,2.7,4.7,7.2,7.4,8.1,8.5,8.6,8.8,9.7],'rankings/dy_sales_sep.png')
s='MomoRank公开免费Top10快照'
c='低置信辅助快照：站点自述整理平台公开榜；未核平台原始榜、采集时点、覆盖率或权重'
add('wx_sales_daily','微信','畅销','2026-10-12',s,'https://www.momorank.com/rankings/bestseller','向僵尸开炮|三国：冰河时代|浪漫餐厅|疯狂水世界|永远的蔚蓝星球|向往的生活|灵画师|向末日开炮|下方了|永夜起源','站点称按用户活跃度与有效付费等指标综合计算、每天更新；涨跌优先采用微信后台官方涨跌。',confidence=c)
add('wx_popular_daily','微信','人气','2026-10-12',s,'https://www.momorank.com/rankings/popular','羊了个羊：星球|腾讯欢乐斗地主|指尖闯关大挑战|抓大鹅|QQ经典农场|闯关也疯狂|开心消消乐|肥鹅美食街|单车骑行挑战|一箭又一箭','站点称按用户活跃度等指标综合计算、每天更新；没有活跃人数数值。',confidence=c)
add('wx_play_daily','微信','畅玩','2026-10-12',s,'https://www.momorank.com/rankings/most_played','羊了个羊：星球|赵云与阿斗|抓大鹅|一箭又一箭|打个螺丝|上个了车|开车我贼6|解压闯一关|解压打毛线|看谁先上车','站点称按活跃度与有效广告等指标综合计算、每天更新。第6名按原文保留“上个了车”。',confidence=c)
add('dy_sales_daily','抖音','畅销','2026-10-12',s,'https://www.momorank.com/douyin/rankings/bestseller','疯狂水世界|灵画师|向僵尸开炮|狱国争霸|浪漫餐厅|镇邪人|造化仙府|向往的生活|时尚百货城|肥鹅美食街','站点称依据小游戏广告消耗与付费情况综合计算、每天更新。广告消耗不是开发者广告收入，公式未披露。',confidence=c)
add('dy_popular_daily','抖音','热门','2026-10-12',s,'https://www.momorank.com/douyin/rankings/popular','羊了个羊：星球|抓大鹅|疯狂水世界|赵云与阿斗|看谁先上车|肥鹅美食街|梦幻消除战|躺平发育|指尖快消|浪漫餐厅','站点称依据小游戏访问用户量综合计算、每天更新；非话题榜，无具体用户数量。',confidence=c)
(p/'rankings.json').write_text(json.dumps({'scope':'中国大陆微信和抖音小游戏；不含TikTok或海外市场','groups':rows,'warnings':['日榜与月均榜不得横向当作同一口径','热门/人气、畅玩、畅销是不同指标','所有榜单均不提供本作留存率、利润、ROI或净收入','未验证平台官方原始日榜；月榜来自行业机构的转载榜图','未找到可完整核验的2026年9月抖音热门Top10，不能用8月代替9月']},ensure_ascii=False,indent=2))
with (p/'rankings.csv').open('w',newline='',encoding='utf-8-sig') as f:
 w=csv.writer(f);w.writerow(['platform','kind','data_date','rank','game','average_rank','source','url','method','confidence'])
 for r in rows:
  for x in r['top10']:w.writerow([r['platform'],r['kind'],r['data_date'],x['rank'],x['name'],x['average_rank'],r['source'],r['source_url'],r['method'],r['confidence']])
print('Wrote',len(rows),'groups')
