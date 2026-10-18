# 批准与版本状态

## 已批准并冻结
- guanyu-mythic-set/frames/ 四种黑铁、青铜、白银、黄金通用框与独立星级系统。预览图属于此系统的派生展示。
- guanyu-mythic-set/stories/01-桃园神誓-v2-桃林.png。

## 已交付，等待用户审阅
- guanyu-mythic-set/cards/ 下当前四张地面场景卡片；对应 pure/*-grounded-v2.png。
- guanyu-mythic-set/stories/03-过关寻兄-v2-古道.png。
- 四阶总览属于上述待审交付，不是批准凭证。
- 本次地面卡片与过关故事交付时间：2026-10-18T07:45:32Z；对应 Library receipt 中 current_version_number=1。

## 部分方向通过，仍须修改
- guanyu-mythic-set/stories/02-天降斩华雄-v2-叙事聚焦.png：仅华雄体态方向通过。武器、三人温酒副线和清晰“汜水关”仍需修正。
- prompts/silver-story-focus-v3.json 为修订提示词，存在提示词不等于已经生成/完成；新结果须另行查看、校验与交付。

## 旧版和探索
history-v0、早期 pure/stories、selected-four、round2/3/4、ten-options、calibration 等保留供追溯。历史 manifest 内的 QA、pending=false 或过去 selected 命名不等于本阶段最终批准。asset-index 的 status 才是本快照状态覆盖层。supersedes 只在可明确对应的当前资产上填写，其余不臆造版本链。

## 待办
1. 完成华雄定点修订并检查，再交用户审阅。
2. 等待四阶地面卡与过关古道故事的用户反馈。
3. 提取独立环境的 Godot starter；确认代码与美术接入计划后再建立可运行版本。
4. 经授权配置远端仓库与 LFS，上传并独立恢复校验；当前本地快照不是已完成云端备份。
