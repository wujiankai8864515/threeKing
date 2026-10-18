# 神话三国：关羽美术生产备份

这是可恢复的项目美术快照，包含源图、透明框、星级 UI、合成卡、故事插图、候选/旧版、生成提示词、已有 Python 制作脚本与阶段决策。它不是已实现的卡牌游戏。

## 从哪里开始
- `docs/STATUS.md`：已批准、待审、部分批准、旧版的边界。
- `docs/DECISIONS.md`：当前创作与技术决定。
- `docs/HERO-PRODUCTION-SOP.md`：可复用英雄制作流程。
- `asset-index.json`：每个原文件到完整二进制对象的映射、SHA-256、原文件名、Library 历史与状态。
- `source/`：实际存在的脚本、提示词、历史 manifest/QA（旧文档不代表当前决策）。
- `assets/sha256/`：完整二进制文件，按内容哈希去重；多个原路径可以引用同一对象。
- `coverage.json`：覆盖范围与排除范围。

所有本次文件都位于 YYYY-MM-DD_HH-mm-ss_topic 时间目录下，时区 UTC+08:00。原始名字在索引中保留；生成时间没有可靠证据时为 null，不用归档时间或文件 mtime 冒充生成时间。仓库根目录 LATEST.json 是稳定入口，latest 不等于 approved。

## 检查与恢复
在本目录运行：

    python tools/restore.py --verify-only
    python tools/restore.py --output /path/to/new-empty-restored-folder

恢复会建立原始目录结构。文字中的旧工作区绝对路径已改为相对路径；索引保留原文字 SHA-256 和归档文字 SHA-256。旧脚本是历史来源，不保证全部可直接运行。当前合成脚本使用 Pillow，以及 NotoSerifCJK-Bold.ttc（原路径 /usr/share/fonts/opentype/noto/）。没有假造依赖锁文件。先恢复到独立目录，再运行合成；它会覆盖恢复副本内的卡图和 UI 派生文件，不应覆盖已冻结的归档对象。

## Git / LFS 与恢复保障
约 525 MiB 完整二进制、最大单文件约 3.6 MiB。根目录 .gitattributes 已声明 PNG/PDF/DOCX 使用 Git LFS，；本机已确认 git-lfs/3.6.1。此备份尚未初始化 Git、创建仓库、提交或推送。实际发布前需要确认远端权限、LFS 可用性与配额；必须先正确安装 LFS，再 git add，否则图片可能进入普通 Git 历史。普通 clone 可能仅有 LFS 指针，须取回 LFS 对象并执行校验才算恢复成功。索引或 Library ID 单独不构成完整备份。

后续同步应创建新的时间戳快照，并保留旧版本；按哈希复用已有对象，更新 LATEST 和状态。每次收到用户批准才更新 approved 标记。上传结束需要在另一检出目录校验所有实际二进制，不只检查 commit。当前快照没有后台定时器或自动推送凭据；持续远端同步尚待配置和验证。

## 尚未纳入
另一环境中的 Godot 空白 starter 尚待提取；这里没有可玩的卡牌游戏代码。旧 Cocos/旅行木鱼、赵云项目和身份不明的生成图不属于本次范围。未包含凭据、缓存、私人笔记或原始聊天记录。
