# 四十英雄完整候选交付

Git保留280张现行交付图的完整字节及原始素材、历史版本、规范与反馈。全部40人每人7张，魏蜀吴群各10人，状态为候选待用户验收。CURRENT40.json是准确交付映射。旧20大包保留历史，因聊天大小限制不作当前聊天交付；现行52包均小于19MB。Library上传成功不等于聊天最终交付。

Library和本地52个小ZIP仅为便捷下载副本，不重复纳入Git。rebuild-downloads.py可从Git LFS还原后的资源重建52小包，并逐图核验SHA256及原ZIP哈希。

用法：python rebuild-downloads.py --repo /path/to/threeKing --output /path/to/downloads
仅校验并逐包临时重建：加 --verify-only。
