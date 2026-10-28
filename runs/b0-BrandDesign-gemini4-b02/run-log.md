# B0 实验运行记录（run-log.md）— BrandDesign × Gemini 4 × B02（AI 生图桌面工具）

## 1. 基本信息与耗时

| 项目 | 记录 |
| --- | --- |
| **实验编号** | B0（原样测底座 `BrandDesign` / `brand-studio`） |
| **测试简报** | `test/briefs/b02-tool.md`（AI 生图桌面工具，中英并用，含大量数字，名字未定） |
| **输出目录** | `/workspaces/brand-skill/runs/b0-BrandDesign-gemini4-b02/` |
| **使用模型** | 主模型：`Gemini 4`；独立评审子代理（`research` sub-agent）：`Gemini 4` |
| **底座版本** | `.bases/BrandDesign`（commit `177bb77`），全程未修改 `.bases/` 下任何文件 |
| **开始时间** | `2026-10-28T13:43:57Z` |
| **完成时间** | `2026-10-28T14:14:30Z` |
| **总耗时** | 约 **30.5 分钟** |

---

## 2. 跑了多少轮（设计迭代与评审轮次）

本次严格按 `.bases/BrandDesign/skills/brand-studio/SKILL.md` 的 Step 1（Intake & Assumptions）→ Step 2（Research & Word Map）→ Step 3（Concepts → 3 Greyscale Sketches → Audit & Preview Loop → Independent Review → Checkpoint 1）执行，在 Checkpoint 1 并排展示页停下。共跑了 **4 轮矢量迭代（`v1` → `v2` → `v3` → `v4`）** 与 **2 轮独立子代理评审（`review/round-1`、`review/round-2`）**：

1. **命名与假设处理（Step 1）**：
   - `BrandDesign` 底座无独立起名步骤或脚本（`SKILL.md` §1 仅将名称作为 Intake 输入或 Fast-track 假设）。按任务规则提议 1 个中英双语品牌名 **「矩台 · KADR」**（矩=曲尺/画幅矩阵，台=暗房看片台/精修工作台；KADR=画幅/取景框），与受众、定位等一并写入 `brief.md` 的假设清单。
2. **行业调研与构思（Step 2 & Step 3.1）**：
   - 调用 `search_library.py --industry design-creative --summary`、`--industry ai-ml --summary` 及 `palette/search_palettes.py --industry saas --summary`、`--industry agency --summary`，分析品类惯例并列出 4 类行业陈词滥调（四芒星/魔法棒、放射旋涡/六边形节点、蓝紫霓虹渐变球、具象画笔/光圈叶片）。
   - 完成词汇映射（Word Map）与 10 个一句话概念快评，选出三套不同标识类型的方向：
     - **方向 A（Calibrated K · 曲尺看片台）**：字母负空间标（Letterform / Negative Space）
     - **方向 B（Queue & Lock · 队列比对窗）**：抽象/工具图形标（Abstract / Pictorial Instrument）
     - **方向 C（Crop-Rule · 矩尺造字）**：定制中英双语字标与「矩」字印记（Custom Wordmark / Monogram）
3. **第 1 轮矢量构建与渲染自检（`v1`）**：
   - 产出 `concept-{a,b,c}-v1.svg` 及 `concept-{a,b,c}-lockup-v1.svg`，运行 `svg_audit.py`（3 个主图形均得 `100/100`）与 `preview_sheet.py`（`preview-v1.html`）。
   - **渲染自检发现问题**（验证了底座 `bi-logo.md` 所说“损坏的图形能通过全部自动检查，唯有肉眼查看 PNG 能抓出”）：
     - A 初稿右上与右下模块在中心重叠，吃掉了对角负空间通道，且左竖干上的 3 个 8px 刻度孔在 16px 下糊死；
     - B 初稿中间带箭头横条伸入右侧 C 形框（`[->`），酷似通用 UI“登录/导入”图标；
     - C 初稿为外框包 `K`（`[K]`），与 A 撞型，且字标直接用 `Noto Serif SC` 转曲，未体现中文字标定制造字。
4. **第 2 轮矢量修正与第 1 轮独立评审（`v2` → `review/round-1`）**：
   - 修复 `v1` 缺陷：A 拉开 20 单位垂直通道并去掉细孔；B 改为左侧 3 个队列方格 + 右侧主取景框；C 改为网格定制几何汉字「矩」印记 + 全路径定制「矩台·KADR」双语字标，并在 A/B 字标上用 `skia-pathops` 做布尔切口。
   - 生成 `concepts-r1.png` 并调用 `review_pack.py` 生成 `review/round-1/REVIEW-PACKET.md`，启动独立 `research` 子代理评审。
   - **独立评审第 1 轮返回 7 项问题（3 Blocker、3 Major、1 Minor）**：
     - `[blocker][C]`：`concept-c-lockup-v2.svg` 中「台」字上部「厶」未留内腔变成实心黑三角；`A` 字左腿路径自相交断裂（且 `svg_audit.py` 报 3 处 `72.3°` 近邻角警告）。
     - `[blocker][B]`：`concept-b-lockup-v2.svg` 布尔切口切偏，在 `A` 左腿与「台」底边啃出锯齿缺口。
     - `[blocker][A]`：`concept-a-lockup-v2.svg` 在 `KADR` 的 `K` 竖干内切出空洞并留下 `0.67` 单位极细碎边。
     - `[major][B]`：`concept-b-v2.svg` 左三格+右方框构图在中文里极易误读为三点水汉字 **「泪」「泊」** 或 **「旧」**，且内部 18 单位间隙在 16px 下粘连。
     - `[major][C]`：`concept-c-v2.svg` 「矩」字左上撇呈实心楔形块，「矢/巨」间距仅 16 单位，16px 下易糊。
     - `[major][A]`：`concept-a-v2.svg` 立柱（48）、顶梁（40）、斜臂（50.9）粗细不一，且曲尺内侧水平折角仅 16 单位（16px 下退化为斜切角）。
     - `[minor][A,B,C]`：`concepts-r1.png` 底部三张卡片的中文说明全部冲出卡片右边界被截断。
5. **第 3 轮矢量修正与第 2 轮独立评审（`v3` → `review/round-2`）**：
   - 针对性修复第 1 轮全部 7 项问题（其中在自检 `v3` 初稿 PNG 时，还主动发现并修正了 C 字标中对称三角形「厶」导致「矩台」误读为「矩合」的问题，改为右上开口的真实「厶」笔势；同时将 B 改为递进画框 `⌜ ⌜ □` 结构，彻底消除「泪/旧」与 `:D` 表情包误读）。
   - 生成 `concepts-r2.png` 与 `review/round-2/REVIEW-PACKET.md`，发回同一独立评审子代理进行第 2 轮复审。
   - **独立评审第 2 轮返回 3 项发现（0 Blocker、1 Major、2 Minor），A 与 C 获评 `ship`**：
     - `[major][B]`：`concept-b-v3.svg` 递进 L 画框间距为 16 单位（16px 下偏紧），且纯直角层叠框接近通用“复制图层”图标。
     - `[minor][C]`：`concept-c-lockup-v3.svg` 中 `K` 顶部内折角仅 4 单位，且「巨」中腔 24 单位略紧。
     - `[minor][A]`：`concept-a-lockup-v3.svg` 中 `Noto Sans SC 700` 汉字笔画（~13.5 单位）比拉丁 `700` 竖干（~19.4 单位）视觉偏细。
6. **第 4 轮定稿与检查点输出（`v4` → Checkpoint 1）**：
   - 将 B 框线缩至 24 单位、层间距扩至 24 单位，并在递进框右上角加入统一的 45° 校准切角；
   - 将 C 字标 `K` 顶梁内折角扩至 20 单位、「巨」中腔扩至 28 单位；
   - 将 A、B 组合标中的中文字重提升至 `Noto Sans SC 900 (Black)` 以匹配拉丁 `700` 字干粗细；
   - 导出最终检查点文件 `concepts.svg`、`concepts.png`、`preview.html`、`preview.png` 与 `checkpoint-1.md`（四个 `v4` 核心 SVG 审计得分：`100/100`、`100/100`、`100/100`、`99/100`）。

---

## 3. 哪一步报错（执行报错与工具问题）

1. **`render_png.py` 单传 `--width` 渲染宽扁 SVG 时底部被 Chrome 截断**：
   - **现象**：首次用 `python3 render_png.py test-zh.svg -o test-zh.png --width 600` 渲染宽扁双语字标时，`render_png.py` 按宽高比算出高度 `120`，向 Chrome 传入 `--window-size=600,120`。在 Linux 容器内 Chrome 156 `--headless=new` 模式下，`--window-size` 含约 87px 虚拟窗口顶栏，导致实际网页视口仅剩 `600×33`，字标下半部 70% 被截断。
   - **解决**：调用 `render_png.py` 预览字标或概念卡时，使用 `--size 600`（正方形画布 contain 居中包装）或保证窗口高度 `>= 300px`，渲染即完全正常。
2. **自定义辅助脚本直接调用系统 `python3` 时缺少 `skia-pathops` 报错**：
   - **现象**：运行 `build_v2.py` 时，首次直接使用系统环境 `import pathops` 报 `ModuleNotFoundError: No module named 'pathops'`；随后接入 `kitlib.ensure_deps({"pathops": "skia-pathops"})` 自动切入 `uv` 缓存环境后，因将枚举 `pathops.FillType.WINDING` 误写为 `Winding` 报了一次 `AttributeError`。
   - **解决**：修正为 `pathops.FillType.WINDING` 并通过 `kitlib.ensure_deps()` 调起 `uv` 环境，后续全部一次通过。
3. **系统 `file` 命令缺失**：
   - 容器未安装 `file` 命令（退出码 127），改用 Python 读取 PNG 头或直接用 `read_file` 查看图片。

---

## 4. 中文哪里出问题（底座在中文/双语场景下的核心痛点）

这是本次 B0 实验在双语简报（B02）下暴露最清晰的 5 个底座级中文问题：

1. **底座缺少“品牌起名”模块，且 `slug` 逻辑对纯中文名不兼容**：
   - B02 简报明确提出“名字还没定……帮我做品牌：名字建议”，但 `BrandDesign` 底座默认用户已有名称，无任何起名探索、字形结构评估或双语配对指南。
   - 此外，底座按 `re.sub(r"[^a-z0-9]+", "-", name.lower())` 生成工作目录名，若只用纯中文名会导致目录名为空字符串。
2. **`concept_sheet.py` 的文本折行函数 `wrap()` 完全基于英文空格与 ASCII 字符宽度假设，导致中文说明必截断**：
   - `concept_sheet.py` 第 45–54 行 `wrap(text, int(inner_w / 9.6))` 用 `text.split()` 按空格分词，并假设每个字符仅占 `9.6 px`（每行上限约 44 个字符）。
   - 中文句子无空格，`text.split()` 会把整句中文当成 1 个单词；且 `font-size="19"` 下每个汉字实际宽 `19 px`（约为 `9.6 px` 的两倍），401 px 宽的卡片内部最多容纳 20 个汉字。即便在中文里手动加空格分词，只要总字符数 `len <= 44`，`wrap()` 依然把两句中文拼在同一行，导致第 21 个字以后的内容全部冲出卡片右边界（见 `concepts/concepts-r1.png`）。
   - **临时绕过方案**：在不改 `.bases/` 脚本的前提下，通过在每句 16–17 字的中文末尾拼接零宽空格（`\u200b`，Python `len` 计为 1、视觉宽度为 0、且不被 `split()` 剥离）凑满 40 字符计数，才强制触发 `concept_sheet.py` 正常换行（见最终 `concepts.png`）。
3. **`outline_text.py` 中英混排的字面框高度、基线与字重严重不匹配**：
   - `outline_text.py` 按西文大写字高（`sCapHeight -> 100`，基线 `y=100`，顶线 `y=0`）归一化。直接传入中英混排字符串（如 `"矩台 KADR"`）时，汉字实际字面框为 `y = -18.14 .. 112.41`（总高 `130.55`），比同字号英文大写（`0..100`）视觉大出约 30%，且底部下沉到基线以下 `12.4` 单位，导致中英并排时高低错位。
   - 同时，由于汉字笔画远多于拉丁字母，相同字重（如 `Noto Sans SC 700` 配 `Chakra Petch 700`）下，汉字笔画粗细（~13.5 单位）比西文竖干（~19.4 单位）细约 30%。必须将汉字单独转曲、按 `~0.80×` 缩放并对齐视觉中心线（`y=50`），且将中文字重升一档（如中文用 `900 Black` 配英文 `700 Bold`）才能达到视觉平衡。
4. **Google Fonts 合法开源中文字体极度匮乏**：
   - `live_sources.py fonts --subset chinese-simplified` 仅能检索到 10 款 OFL 中文字体，除去毛笔/手写体和卡通体后，严肃工具品牌可用的现代无衬线/衬线仅 `Noto Sans SC` 与 `Noto Serif SC` 两款，三套方向极易撞同一款中文字体。
5. **中文字标“直接转曲加切口”与“纯代码手绘造字”两难**：
   - 按底座 `SKILL.md` §3.2 建议“用 `outline_text.py` 转曲再加一处细节”，由于缺乏汉字部件级坐标定位，盲目做布尔减法极易切伤相邻笔画（如 `v2` 中切出 `0.67` 单位碎边）；
   - 而若用纯 SVG 路径从零拼写汉字（如方向 C 的「矩台」），模型若无汉字字形结构约束，极易出现**部件拓扑错误或形近字误读**（如 `v2` 中把「台」的「厶」画成实心黑三角，`v3` 初稿把「厶」画成对称封顶的 `△` 导致「矩台」变成了「**矩合**」，以及方向 B `v2` 左三格+右框在中文语境下被读成三点水汉字「**泪 / 泊**」），且多笔画汉字在 16 px 下极易粘连，必须经过渲染自检与独立评审多轮打磨才能修正。

---

## 5. 产出文件清单（位于 `/workspaces/brand-skill/runs/b0-BrandDesign-gemini4-b02/`）

- `brief.md`：客户原始简报、结构化简报与假设清单（含提议品牌名「矩台 · KADR」）。
- `research.md`：Step 2 行业库/色板库调研、行业陈词滥调清单、词汇映射（Word Map）与 10 个候选概念评分表。
- `concepts.svg` / `concepts.png`：**Checkpoint 1 最终三套灰阶方向并排展示页（SVG + PNG）**。
- `preview.html` / `preview.png`：**三套方向在 16px–256px、像素级 Favicon、深色反白、模糊眯眼、镜像、竞品货架下的完整测试页（HTML + PNG）**。
- `checkpoint-1.md`：按 `SKILL.md` §3.5 规范撰写的检查点汇报正文（含每套方向的 Idea、Why it fits、Honest risk、独立评审统计与推荐结论）。
- `concepts/`：保留了 `v1`、`v2`、`v3`、`v4` 全部 4 轮迭代的独立图标与双语组合字标 SVG，以及 `concepts-r1.png`、`concepts-r2.png`、`preview-v1..v3.html`。
- `review/round-1/` 与 `review/round-2/`：两轮 `review_pack.py` 生成的 `REVIEW-PACKET.md` 与独立子代理返回的 `REVIEW-RESPONSE.md`。
- `run-log.md`：本运行记录文件。
