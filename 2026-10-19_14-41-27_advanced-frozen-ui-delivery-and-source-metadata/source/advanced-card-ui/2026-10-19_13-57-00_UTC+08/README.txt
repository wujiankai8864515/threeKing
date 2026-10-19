高阶卡框：五星钻石切面镶铂金/六星深紫晶体镶厚鎏金。两框均真实RGBA，中心透明。
人物插画1024×1536以1:1置入1190×1786，UI框独立。文字/蜀徽底色/等级/分支/兵种标识均动态层，不能烘焙到人物插画。
被动板三切片压短202源px，三条固定自底向上槽位961/1045/1129，字按字形bbox垂直中心对齐，姓名与等级合为紧凑一组。
五星3被动是用户明确要求；六星默认沿用并强化3被动，是制作默认，可后续调整。
layout-tests和layout-vector-draft为内部构图验证旧黄金人物测试，不是新高阶卡面，不纳入正式交付。
两框生成调用builtin imagegen，以已认可金框为结构参考；未用API。原始生成图、短板重组图及最终alpha框全部保留。

复现：python render_cards.py --config <hero>-<branch>-<tier>-config.json
仅重建公共框：python render_cards.py --frames
插画源文件路径、SHA256、成卡SHA256、原生像素校验及UI字形中心均在cards/同名.json；卡图像素和UI独立导出。
候选状态：全部24张装框完成，用户尚未验收。交付回执与Library映射独立，不以发出即批准。
Library客户端create_library_file在2026-10-19约14:16至14:35出现blob超时，连小于1MB预览也失败；官方prepare_uploads(workspace_path)→finalize_uploads成功，原图无损，不通过缩图伪装高清。
