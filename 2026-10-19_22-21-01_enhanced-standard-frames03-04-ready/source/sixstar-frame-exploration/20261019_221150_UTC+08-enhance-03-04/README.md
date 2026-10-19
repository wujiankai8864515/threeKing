# 六星 03 / 04 精工升级候选
时间：2026-10-19 22:19 UTC+08

仅升级象牙金釉、赤铜鎏银两种材质方向，均为候选，尚未获最终批准。完整成卡保留同一机甲插画和标准 UI 布局。

## 当前交付
- 00-六星03与04精工升级对照.png
- 03-象牙金釉·御铸-六星机甲关羽.png
- 04-赤铜鎏银·天锻-六星机甲关羽.png

透明框、独立动态姓名层、其他动态 UI 层分别保存。Library 回执见 library-receipts.json。

## 真实制作与复现
actual-args.json 保存两次材质生成的真实参数。生成源保存为 03/04-generated-frame-original.png。normalize_frames.py 将材质归一至标准尺寸并应用原框透明度；compose.py 调用标准 renderer 装卡；qa.py 验证覆盖范围与 UI 和插画。render_config.py 是给其他批次使用的完整卡牌合成入口，传入 example-config.json 格式配置。六星使用本轮 03 框，五星沿用既有钻石框。

## QA
逐张目检完整卡、缩略对照与被动/圆章放大细节。QA-layout.json 验证标准框 alpha 完全一致、动态 UI 完全一致、无覆盖插画区域像素改变数量为零。星槽、材质浮雕在固定容器内升级，不声称所有雕刻内纹位置相同。

## 历史说明
procedural-rejected 及 materials-procedural-history.py 是被自检否决的早期程序材质方案，不是当前成品。00-六星标准布局五材质总览.png 是沿用旧脚本产生的宽画布检查图，不是此次交付图。
