# B0 实验运行日志 (run-log.md) — BrandDesign 底座 (`brand-studio`) × 半山烘焙 (B01)

## 1. 基本信息与耗时统计

| 项目 | 记录 |
| --- | --- |
| **实验编号与目录** | `runs/b0-BrandDesign-gemini4-b01/` |
| **测试底座** | `BrandDesign` (`skills/brand-studio/SKILL.md`，commit `177bb77`)，原样按流程执行至 Checkpoint 1 |
| **测试简报** | `test/briefs/b01-banshan.md`（半山烘焙 · 成都订阅制浅中烘精品咖啡豆工作室） |
| **主执行模型** | **Gemini 4 Argon (High)** |
| **独立评审子代理模型** | **Gemini 4 Argon (High)**（通过 `invoke_subagent` 启动只读 `research` 子代理，完全隔离设计偏好，跑满 2 轮独立评审） |
| **开始时间 (UTC)** | `2026-10-28T12:42:11Z` |
| **结束时间 (UTC)** | `2026-10-28T13:11:00Z` |
| **总耗时** | **约 28 分 49 秒**（含调研、4 个版本 SVG 迭代、中文字体排印消缺、2 轮独立子代理盲审及 PNG 渲染导出） |

---

## 2. 迭代轮次与底座工作流执行全记录

本次完全遵循 `BrandDesign` (`brand-studio/SKILL.md`) 的 **Step 1 (Intake) → Step 2 (Research) → Step 3 (Concepts → Checkpoint 1)** 流程，在生成并验证 `concepts.png` 与 Checkpoint 1 提案后按要求停下（未替用户做选择，未提前生成彩色/物料 Kit）。

### 2.1 图形与字标迭代轮数：**共 4 轮 SVG 迭代 (`v1` → `v2` → `v3` → `v4`) + 2 轮独立评审**

1. **Iteration 1 (`v1`：初稿构建与 `svg_audit.py` 首测)**
   - 构建 `concept-a-v1.svg`（腰线半山）、`concept-b-v1.svg`（半山退台 B）、`concept-c-v1.svg`（山谷一爆）。
   - **脚本与视觉自检发现的问题**：
     - `svg_audit.py` 在 `concept-a-v1.svg` 检出 4 处 `WARN [near-miss-angle]`（`半`字上两点角度为 `72.6°`，偏离 `75°` 清洁角），得分 92/100；且 `山` 字腰部断口仅 `6` 单位，在 16 px 下闭合。
     - `svg_audit.py` 在 `concept-c-v1.svg` 检出 2 处 `WARN [near-miss-angle]`（`102.1°`、`103.0°`），得分 92/100；且通过 `render_png.py` 渲染看图发现：**`concept-c-v1.svg` 出现了严重的 `fill-rule="evenodd"` 布尔翻转错误**——上方裁切矩形超出了外圆 `r=104` 的左右上角边界，导致圆外左上、右上角被反转为两个黑色直角三角形。
2. **Iteration 2 (`v2`：几何修正、100/100 审计通过与 `outline_text.py` 中文字标锁定)**
   - 将 A、B、C 所有斜线对齐至精确的 `45°` 整数坐标，将 Concept C 内部镂空改为 `r=82` 内圆弧与精确 `45°` 折线，三枚主标在 `svg_audit.py` 中全部达到 **100/100（0 FAIL, 0 WARN, 0 INFO）**。
   - 调用 `outline_text.py` 抓取 Google Fonts `Noto Serif SC` 与 `Noto Sans SC` 生成「半山烘焙」字标路径，并按 `SKILL.md` §3.2 要求叠加布尔负空间细节，触发了**可变中文字体 `evenodd` 笔画交叉白洞 Bug**（详见第 4 节），随后通过 `skia-pathops` 布尔并集（`pathops.simplify`）修复。
3. **Iteration 3 (`v3`：响应独立评审 Round 1 的 8 项发现)**
   - 调用 `review_pack.py --round 1` 并派发独立评审子代理，返回 **2 项 Blocker、5 项 Major、1 项 Minor**（见 `review/round-1/REVIEW-REPLY.md`）：
     - **[Blocker 1 — Concept C 负空间蘑菇云歧义]**：评审指出 `concept-c-v2.svg` 的上方白色半圆天穹加上下方垂直裂口，在 16–32 px 下完全变成一朵"白色蘑菇 / 蘑菇云 / 雨伞"。**修复**：在 `concept-c-v3.svg` 中彻底移除上方外环与垂直裂口，重构为「云阶半山」（上方开放式双峰陵线 + 正中 24 单位水平云雾切层 + 下方两级水平等高线梯田）。
     - **[Blocker 2 & Major — Concept A 尖刺感与锁定组合断层]**：评审指出 `concept-a-v2.svg` 的 45° 箭头和尖峰显得激进工业化（像半山别墅地产或武术潮牌），且 `concept-a-lockup-v2.svg` 在宋体「山」字上切一道 10 单位白条"100% 像热敏打印机坏了一行针头的断线故障"。**修复**：移除所有 45° 箭头与尖刺，改为平头建筑感笔画；将「山」字内白从 `20` 扩至 `25` 单位、中腰云雾切口扩至 `24` 单位；重做双语锁定组合（含 `BANSHAN ROASTERS`）。
     - **[Major — Concept B 粗野主义电竞感与笔画膨胀]**：评审指出 `45°` 切角的 `B` 斜边法向厚度达 `33.9`（比 `28` 横画肿胀），且风格偏冷酷硬件/电竞。**修复**：在 `concept-b-v3.svg` 中改为温润的 `28` 单位恒定线宽半圆拱窗 `B`（`半山拱窗 B`），中腰峡谷扩至 `24` 单位，并在锁定组合中将图标比例降至 `1.12×` 以突出中文主体。
     - **[Minor — `concept_sheet.py` 中文长句不换行导致出界截断]**：利用零宽空格（`\u200b`）补偿字节长度，使 `concept_sheet.py` 在不改底座脚本的前提下将中文说明整齐折为 2 行。
4. **Iteration 4 (`v4`：响应独立评审 Round 2 的 2 项 Minor 精修并定稿)**
   - 调用 `review_pack.py --round 2` 进行第 2 轮独立复审，返回 **0 Blocker、0 Major、2 Minor**，A/B/C 三套方向全部获批 **`ship`**（见 `review/round-2/REVIEW-REPLY.md`）。
   - 顺手修复 Round 2 指出的 2 项 Minor 细节：
     1. 在 `concept-a-lockup-v4.svg` 中将定制的「半」「山」二字展宽至 `168` 单位全宽（20 单位主干），与后方 `Noto Sans SC Medium` 的「烘」「焙」二字达成 1:1 视觉字宽与灰度平衡。
     2. 在 `concept-c-v4.svg` 中将上半山体底边在 `y=108` 处从 `x=28..228` 外扩至 `x=26..230`，严丝合缝贴合 `R=104` 外圆弦宽（`25.94..230.06`）。

---

## 3. 哪一步报错 / 脚本异常清单

在遵循底座流程运行 `.bases/BrandDesign/skills/brand-studio/scripts/` 时，遇到以下脚本报错或非预期行为：

| 步骤 / 脚本 | 报错或异常现象 | 根因分析 | 解决方式（未改动 `.bases/`） |
| --- | --- | --- | --- |
| 1. `search_library.py --industry food-beverage --summary` | 报错退出：`unknown --industry 'food-beverage'. Did you mean: ai-ml, cloud-infrastructure...` | `search_library.py`（Logo 库）与 `palette/search_palettes.py`（色板库）的 `--industry` 枚举词表不统一：色板库有 `food-beverage`，而 Logo 库几乎全是科技分类，无餐饮/食品分类。 | 先跑 `--list-values` 查词表，改用 `--query "coffee"`、`--subject "mountain"` 及 `--industry ecommerce-retail`。 |
| 2. `outline_text.py` 输出直接喂给 `svg_audit.py` | 报 `INFO [fractional-viewbox]`、`INFO [precision]`，且在 4 个汉字（如站酷小薇体/黄油体）上直接报 `▲ WARN [complex] 438/480 anchor points` 与 `▲ WARN [near-miss-angle] 89.6° (→90°)`，得分跌至 82/100 | `outline_text.py` 输出高达 15 位小数的未取整浮点坐标和小数 `viewBox`；而 `svg_audit.py` 的复杂度分位数（中位数 75 锚点、`p95` 约 350 锚点）完全基于拉丁字母 Logo 标定，未考虑汉字天然的多笔画特征。 | 在工作流中对生成的路径坐标做 2 位小数舍入，并在 `run-log.md` 记录底座审计阈值对中文字标的系统性误判。 |
| 3. `outline_text.py` 生成的中文字标按 `SKILL.md` 改为 `fill-rule="evenodd"` 叠加负空间切口 | 渲染出的 PNG 中，**「半山烘焙」四个汉字的所有横竖笔画十字交汇处全部变成白色方格破洞**（已留存证据图 `concepts/debug-evenodd-cjk-overlap-bug.png`） | Google Fonts 的可变中文字体（`Noto Serif SC`、`Noto Sans SC`）为了支持字重插值，字形内部由**未合并的独立重叠笔画轮廓**构成；`outline_text.py` 未执行 `removeOverlaps` / `pathops.simplify`，一旦按文档使用 `evenodd` 挖孔，笔画重叠处缠绕数为偶数（2），全部被镂空。 | 使用 `uv` 缓存环境已有的 `skia-pathops`（`pathops.simplify` 先合并汉字内部重叠笔画，再用 `pathops.PathOp.DIFFERENCE` 做真布尔减法），完美解决。 |
| 4. `concept_sheet.py` 传入中文 `--notes` 概念说明 | 中文说明完全不换行，单行冲出卡片右边界并被截断（已留存证据图 `concepts/debug-concept-sheet-unspaced-zh.png`） | `concept_sheet.py` 的 `wrap(text, limit)` 函数存在两处英文中心主义假设：① 用 `text.split()` 按空格分词，中文无空格则整句视为 1 个词，永不触发换行；② 用 `int(inner_w / 9.6) = 43` 字符作为每行上限（假设 19px 字体平均字宽 9.6px），但全角汉字宽 19px，每行最多只能容纳约 21 个汉字，即便加空格在 35 字时 `len <= 43` 仍不换行。 | 在不修改 `concept_sheet.py` 的前提下，在中文前半句末尾附加零宽空格（`"\u200b" * 26 + " "`），使 Python `len()` 超过 43 触发 `wrap()` 分两行，同时零宽空格在 Chrome 渲染中宽度为 0，完美实现卡片内双行排版。 |

---

## 4. 中文支持深度诊断（尤其字体可选与中文字标）

这是本次 B0 实验最核心的观察项，结论如下：

### 4.1 中文字体可选性：极度匮乏，难以单靠字体拉开三套方向差距
通过底座 `live_sources.py fonts --subset chinese-simplified` 实测，Google Fonts（Fontsource API）中带 `chinese-simplified` 子集且允许商用转曲（OFL-1.1）的字体仅有 **10 款**：
- **衬线体（Serif）仅 1 款**：`Noto Serif SC`（可变字重 200–900）。
- **无衬线体（Sans-serif）共 5 款**：真正能用于严肃正文与现代品牌排版的只有 **`Noto Sans SC`**（可变字重 100–900）1 款；其余 4 款均为单字重（400）展示/标题体——`ZCOOL XiaoWei`（站酷小薇体，实为带喇叭口的仿宋/衬线展示体却被归入 sans-serif）、`ZCOOL QingKe HuangYou`（站酷庆科黄油体，圆角综艺风）、`WDXL Lubrifont SC`（窄体圆角黑体）、`ZCOOL KuaiLe`（站酷快乐体，低幼卡通风）。
- **手写体（Handwriting）共 4 款**：`Ma Shan Zheng`、`Zhi Mang Xing`、`Liu Jian Mao Cao`、`Long Cang`（全部为单字重毛笔/硬笔手写风，不适合精品咖啡与数字价格排版）。
- **结论**：在不自建字体库的前提下，中文品牌在底座里实际上只有 **`Noto Serif SC` + `Noto Sans SC`** 两大家族可用。三套方向若直接打字，必然撞在同一两款字体上，必须依靠**汉字图形化造字（Custom Chinese Wordmark）、字重对比（Weight 300 vs 500 vs 700）、字距（Tracking）以及配套英文字体**来拉开差异。

### 4.2 中文字标的四大技术痛点（底座升级必须解决的地方）
1. **「打字 + 局部挖孔」模式在中文上容易变成"打印机断线故障"**：
   - 底座 `SKILL.md` §3.2 推荐的拉丁字标做法是：`用 outline_text.py 打出真实字体轮廓，再在上面加一个布尔细节`。
   - 但在中文里（尤其是笔画繁复的高对比宋体 `Noto Serif SC`），直接在标准印刷体汉字上切一刀负空间（如我们在 `v2` 中对宋体「山」字做的水平切口），独立评审一针见血地指出：**在中文阅读习惯中，标准宋体被横切一条白道，看起来不像设计，而像热敏标签打印机坏了一根针头（Scanline Glitch）**！
   - 相反，只有当汉字本身被几何化重构（如 `concept-a-v3.svg` / `concept-a-lockup-v4.svg` 中将「半山」二字提炼为横平竖直的建筑感骨架构件，让「半」的下横与「山」的 24 单位腰部断口形成正负形接力），中文字标才真正具备"设计感"而非"故障感"。
2. **可变中文字体（Noto CJK）的未合并重叠笔画陷阱**：
   - 如第 3 节所述，`outline_text.py` 直接用 `SVGPathPen` 导出 `glyf` 表轮廓，而 Google Fonts 的 `Noto Sans SC` / `Noto Serif SC` 是可变字体，每个汉字内部有大量十字重叠的笔画闭合路径。不经 `pathops.simplify()`（布尔并集）就无法做任何 `evenodd` 或负空间布尔减法。
3. **西文基线与 Cap-Height 度量体系对汉字失真**：
   - `outline_text.py` 用拉丁字母大写高度 `sCapHeight`（约 `0.70–0.73 em`）将字高归一化为 `100`（`cap_top_y = 0, baseline_y = 100`）。但汉字是全字身框（Full-em box），占满 `-18.87` 到 `112.76`（总高约 `131.6` 单位，字宽 `137.17` 单位）。
   - 这导致下游 `compose_lockup.py` 在读取 `.meta.json` 的 `cap_height: 100` 计算图标缩放比（`sym_h = sym_scale * cap`）时，图标相对于汉字实际墨迹高度被缩小了约 **24%**。
4. **审计脚本与展示板脚本的拉丁中心主义**：
   - `svg_audit.py` 的锚点复杂度阈值（`p75 = 155, p95 ≈ 350`）与 `89.6° → 90°` 近邻角警告，会把正常 4 字中文字标（动辄 320–480 个锚点、传统汉字笔画自带微斜收笔）误判为"过度复杂"或"角度失误"。
   - `concept_sheet.py` 的 `wrap()` 按空格分词且按半角宽度 `9.6 px` 折行，导致中文说明必然单行溢出卡片。

---

## 5. 产物文件清单 (`runs/b0-BrandDesign-gemini4-b01/`)

- `brief.md`：客户原始简报 + 结构化设计简报 + 5 个真实同类竞品及来源 + 5 条明确假设清单
- `research-and-concepts.md`：品类库检索、色板库检索、中文字体检索、品类俗套与 AI 默认套路排查、词图（Word Map）及 10 个概念打分表
- `concepts.svg` / `concepts.png`：**Checkpoint 1 最终并排展示页（含 A/B/C 三套方向主标、中英双语锁定组合、64/32/16 px 实寸缩放测试、推荐标记与双行中文说明）**
- `preview-sheet.html` / `preview-sheet.png`：**完整视觉压力测试页及导出 PNG（含 16–256 px 阶梯、16/32/48 px 像素级渲染放大对比、深浅背景反转、高斯模糊眯眼测试、镜像/180°旋转测试、同类货架对比测试）**
- `checkpoint-message.md`：按 `SKILL.md` 规范撰写的 Checkpoint 1 停靠消息（不替用户选，等待用户决策）
- `concepts/`：保存了完整的迭代历史文件（`concept-{a,b,c}-v1..v4.svg/png`、`concept-{a,b,c}-lockup-v2..v4.svg/png` 以及记录中文 Bug 的 `debug-evenodd-cjk-overlap-bug.png` 和 `debug-concept-sheet-unspaced-zh.png`）
- `review/round-1/` & `review/round-2/`：两轮独立子代理盲审的完整 `REVIEW-PACKET.md`、无推荐标记评审图 `concepts-for-review-r1/r2.png` 及子代理评审回复 `REVIEW-REPLY.md`
- `run-log.md`：本实验运行日志
