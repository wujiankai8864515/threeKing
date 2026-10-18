'use strict';
const $=s=>document.querySelector(s);
const groups=window.RESEARCH_DATA.groups;
let currentGroup=null;
function addText(parent,tag,text){const el=document.createElement(tag);el.textContent=text;parent.append(el);return el;}
function renderRank(){
 const platform=$('#platform').value,kind=$('#kind').value,date=$('#rank-date').value;
 const g=groups.find(x=>x.platform===platform&&x.kind===kind&&x.data_date===date);currentGroup=g;
 const body=$('#rank-body');body.replaceChildren();$('#rank-source').replaceChildren();$('#rank-image').hidden=!g?.image;
 $('#rank-caption').textContent=`${platform} · ${kind} · ${date}`;
 if(!g){$('#rank-status').textContent='此组合暂无可完整核验的榜单。为避免混用日期与口径，不以其他榜单补位。';$('#rank-method').textContent='可切换平台、榜种或日期。微信提供畅销/畅玩/人气，抖音提供畅销/热门；月榜只收录已核读的三个组合。';const tr=addText(body,'tr','');const td=addText(tr,'td','未收录可靠完整榜单');td.colSpan=3;return;}
 $('#rank-status').textContent=g.confidence;$('#metric-title').textContent=date==='2026-09'?'月平均排名':'统计数值';
 for(const r of g.top10){const tr=document.createElement('tr');addText(tr,'td',String(r.rank));addText(tr,'td',r.name);addText(tr,'td',r.average_rank==null?'来源未披露':r.average_rank.toFixed(1));body.append(tr);}
 $('#rank-method').textContent=`口径：${g.method}`;
 const a=addText($('#rank-source'),'a',g.source+' ↗');a.href=g.source_url;a.target='_blank';a.rel='noopener';addText($('#rank-source'),'span',` ｜ 发布：${g.published_date} ｜ 采集：2026-10-12（UTC）`);
}
for(const id of ['platform','kind','rank-date'])$('#'+id).addEventListener('change',renderRank);renderRank();
const dialog=$('#lightbox');let lastFocus=null;
function openImage(src,caption){lastFocus=document.activeElement;$('#lightbox-image').src=src;$('#lightbox-image').alt=caption;$('#lightbox-caption').textContent=caption;dialog.showModal();$('#close-lightbox').focus();}
function closeImage(){dialog.close();lastFocus?.focus();}
for(const b of document.querySelectorAll('[data-image]'))b.addEventListener('click',()=>openImage(b.dataset.image,b.dataset.caption));
$('#rank-image').addEventListener('click',()=>{if(currentGroup?.image)openImage(currentGroup.image,`${currentGroup.platform}${currentGroup.kind}榜原图；数据${currentGroup.data_date}，来源${currentGroup.source}，发布${currentGroup.published_date}。`);});
$('#close-lightbox').addEventListener('click',closeImage);dialog.addEventListener('click',e=>{if(e.target===dialog)closeImage();});dialog.addEventListener('close',()=>lastFocus?.focus());
let step=0,timer=null;const states=[['弓','弓','盾','·','·','·','枪','·'],['弓','弓','盾','·','·','·','枪','·'],['弓²','·','盾','·','·','·','枪','·'],['弓²','·','盾','兵','·','·','枪','·']];
const messages=['① 招募：棋盘出现可识别的单位。','② 选择：是否合并，还是保留更多单位？','③ 结果：示意合成反馈，真实配方以游戏内规则为准。','④ 再决策：新的单位与空间压力，开启下一轮。'];
function renderDemo(){document.querySelectorAll('.tile').forEach((el,i)=>{el.textContent=states[step][i];el.classList.toggle('active',step===1&&i<2||step===2&&i===0||step===3&&i===3);});$('#demo-status').textContent=messages[step];}
function pause(){clearInterval(timer);timer=null;$('#demo-play').textContent='自动演示';$('#demo-play').setAttribute('aria-pressed','false');}
$('#demo-next').addEventListener('click',()=>{pause();step=(step+1)%4;renderDemo();});$('#demo-reset').addEventListener('click',()=>{pause();step=0;renderDemo();});$('#demo-play').addEventListener('click',()=>{if(timer)return pause();timer=setInterval(()=>{step=(step+1)%4;renderDemo();},2200);$('#demo-play').textContent='暂停演示';$('#demo-play').setAttribute('aria-pressed','true');});document.addEventListener('visibilitychange',()=>{if(document.hidden)pause();});
