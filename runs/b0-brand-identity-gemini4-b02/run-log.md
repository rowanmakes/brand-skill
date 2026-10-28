# 实验 B0 运行日志（b02-tool · AI 生图桌面工具）

## 1. 基本信息与耗时统计

| 项目 | 记录 |
| :--- | :--- |
| **实验编号** | B0（原样测底座 `brand-identity-skill`） |
| **测试简报** | `test/briefs/b02-tool.md`（AI 生图桌面工具，面向电商视觉和独立设计师，定位于无画布时代的快速迭代与多图对比桌面工具） |
| **使用模型** | Gemini 4 |
| **产物目录** | `runs/b0-brand-identity-gemini4-b02/` |
| **开始时间** | 2026-10-28 13:43:49 UTC |
| **完成时间** | 2026-10-28 14:04:00 UTC |
| **总耗时** | **约 20 分钟**（其中 CJK 可变字体首次实例化耗时约 3.5 分钟，竞品抓取含超时耗时约 1.5 分钟，2 轮 Logo 编译 + 2 轮 Board 渲染耗时约 3 分钟） |
| **迭代轮数** | **共 2 轮完整构建迭代**（`logos` 跑了 2 轮，`build` 跑了 2 轮，最终 `0 gate` 全部通过并停在 §5 检查点） |

### 分步耗时明细
1. **阅读底座文档与简报（§1–§5 及 `cohesion.md`/`type.md`/`logo.md`/`color.md`/`ai-defaults.md`/`discovery-brief.md`）**：约 3 分钟
2. **`brand.py check` + `brand.py init` + 目录修正**：约 30 秒
3. **`brand.py fonts search` & `brand.py fonts audit`（测试中文字体覆盖与 `--numbers` 门禁）**：约 2 分钟（含首次拉取与实例化 `Noto Serif SC` 700 等 CJK 可变字体，单字重耗时 40–60 秒）
4. **`brand.py site competitors`（抓取 5 个竞品站点的字体与配色）**：约 1.5 分钟
5. **编写 `sets.json` + 第 1 轮 `brand.py logos --full`**：约 5 分钟（含首次实例化 `Noto Sans SC` 300/600/700 字重，每个字重因对 65,535 个 CJK 字形执行 `OverlapMode.REMOVE` 耗时约 45 秒）
6. **修复 Logo 告警 + 第 2 轮 `brand.py logos --full`**：约 1.5 分钟（命中字体缓存后仅需 ~12 秒，实现 `0 gate · 0 warn`）
7. **第 1 轮 `brand.py build --full`（生成 `sets/A|B|C/card.png`、`board.html`、`board.png`、`review.png`、`table.md`）**：约 35 秒
8. **补充中文界面翻译 `i18n.json` + 第 2 轮 `brand.py build --full`**：约 25 秒

---

## 2. 简报未写项与「假设」记录（Intake Assumptions）

简报 `test/briefs/b02-tool.md` 仅给出行业品类、名字未定、竞品列表与开放式探索需求。按照底座 `SKILL.md` §1（「不要因为缺信息而停下，先写进 `intake.assumptions`」）及任务规则，所有未写项均记录为明确假设，写入 `sets.json` 的 `intake` 与 `copy` 字段：

1. **品牌名称（核心假设）**：
   - **底座情况**：`brand-identity` 底座**没有任何起名（naming）步骤或方法论**，`brand.py init NAME` 要求将品牌名作为必填的第一个位置参数传入（`discovery-brief.md` 也假设用户在第 1 步直接提供品牌名）。
   - **提议名称**：提议中文品牌名 **「光桌」**（英文对照意象：*Lighttable / Split Loupe*）。寓意摄影与印前时代用于快速检视、并排比对底片的透光看片台（Light Table），精准契合「砍掉节点流程图与无限画布、专注多批次快出与双栏游标比对」的桌面生图工具定位。
2. **定位语（Tagline）**：`无画布桌面生图台 — 多批次快出、多图并排比对、像素级即时定稿`
3. **目标受众（Audience）**：每日需高频产出并比对上百张商品图与视觉稿的电商视觉团队与独立设计师（厌倦 ComfyUI 节点连线与网页端无限画布卡顿，追求本地桌面快捷键流与確定性出图）。
4. **品牌性格词（Attributes）**：`利落 (crisp)`、`高频迭代 (iterative)`、`可信赖 (dependable)`、`克制专业 (editorial-precision)`（避开 AI 行业泛滥的电光紫/霓虹发光与「赋能/颠覆/魔法」黑话）。
5. **色彩偏好与禁区（Color Preferences / Avoid）**：
   - 偏好：暗室工作台石墨深底或印前校样纸张浅底，配合高辨识度比对游标色（青色、校样朱红、批次信号红）。
   - 禁区：拒绝 `#6366f1` / `#8b5cf6` 电光靛紫、蓝紫霓虹渐变、通用 SaaS 皇家蓝。
6. **展示面与界面文案假设（Surfaces & Copy）**：
   - 交付展示面：`web`、`app`（桌面端工作台界面与比对栏）。
   - 标题：`砍掉无限画布，把算力留给并排比对。`
   - 副标题：`光桌专为电商视觉与独立设计师打造：同一组提示词并发生成四路批次，毫秒级双栏游标比对，选中即导出印刷级图层。`
   - 导航栏：`批次队列` / `双栏比对` / `光线预设`
   - 行动号召（CTA）：主按钮 `新建比对批次` · 次按钮 `导入参考图`

---

## 3. 运行轮次与各步报错/告警记录

### 步骤 1：`brand.py check`
- **结果**：通过（`fontTools`、`brotli`、`uharfbuzz`、`pathops` 均就绪，浏览器 `/home/dev/.local/bin/google-chrome` 可用）。

### 步骤 2：`brand.py init "光桌" --sets 3 --langs zh,en --numbers ... --root runs/b0-brand-identity-gemini4-b02`
- **异常现象（中文目录名退化）**：
  - `brand.py` 中的 `slugify(name)` 使用 `unicodedata.normalize("NFKD", name)` 后通过正则 `re.sub(r"[^a-z0-9]+", "-", ...)` 过滤非 ASCII 字符，最后 `or "brand"` 兜底。
  - 传入纯中文名 `"光桌"` 时，`slugify("光桌")` 变为空字符串并回退为 `"brand"`，导致脚本在 `runs/b0-brand-identity-gemini4-b02/brand/` 下创建了子目录。
- **处理**：立即将 `runs/b0-brand-identity-gemini4-b02/brand/` 下的全部文件与 `.cache` 上移到 `runs/b0-brand-identity-gemini4-b02/` 根目录，并删除 `brand/` 子目录，确保产物直接位于指定目录且无重复副本。

### 步骤 3：`brand.py fonts search` 与 `brand.py fonts audit`
- **报错（门禁拦截 `GATE type.tnum`）**：
  - 当测试 `uv run .../brand.py fonts audit "Noto Serif SC" "WDXL Lubrifont SC" "LXGW Marker Gothic" --langs zh,en --numbers` 时，`Noto Serif SC`、`WDXL Lubrifont SC`、`LXGW Marker Gothic` **全部触发 `GATE type.tnum: lacks tabular figures ('tnum' feature)`**。
  - **原因**：`pipeline.py` 的 `build_type()` 仅对 `text`（正文）角色检查 `need_tnum`。而在 Google Fonts 所有支持简体中文（`zh-hans`）的字体中，**只有 `Noto Sans SC` 一款字体具备 OpenType `tnum`（等宽表格数字）特性**。
  - 同时，`build_type()` 对 `display`、`text`、`mono` 三个角色都强制校验 `--langs zh,en` 的完整字符覆盖率（`check_coverage(path, langs)`），因此 `mono` 角色也不能使用 `JetBrains Mono` 或 `IBM Plex Mono` 等西文等宽字体（否则触发 `GATE type.mono.coverage.zh_Hans`）。
- **处理**：三套方案的 `text` 与 `mono` 均采用通过 `zh,en` + `tnum` 校验的 `Noto Sans SC`，通过 `display` 标题字体（`Noto Sans SC` 300 极细无衬线 vs `Noto Serif SC` 700 粗衬线 vs `WDXL Lubrifont SC` 400 工业刻字黑体）拉开三套方向的字型骨骼差异。

### 步骤 4：`brand.py site competitors`
- **命令**：抓取简报列出的 5 个竞品（`midjourney.com`、`krea.ai`、`leonardo.ai`、`lovart.ai`、`jimeng.jianying.com`）。
- **部分报错**：
  - `https://www.midjourney.com` 与 `https://leonardo.ai`：被 Cloudflare 403/Bot Wall 拦截（页面标题返回 `Just a moment...`）。
  - `https://jimeng.jianying.com`：无头 Chrome 等待 `networkidle` 超过 45 秒触发 `TimeoutExpired: Command '...google-chrome...' timed out after 45 seconds`。
  - `https://www.krea.ai` 与 `https://www.lovart.ai`：抓取成功，产出 `site/competitors.json`。脚本优雅容错，未中断流程。

### 步骤 5：`brand.py logos`（共跑 2 轮）
- **第 1 轮告警（`0 gate · 4 warn`）**：
  1. `Set A: WARN logo.contrast: mark element #00b5c4 has 2.30:1 contrast on light ground #f3f6f7 (< 3.0:1)` —— 青色比对游标在浅色背景上对比度不足 3.0:1。
  2. `Set B: WARN logo.small-size: symbol-small loses ~1.38 px² of thin strokes at 16px` —— 第 1 轮在 `symbol_small_svg` 中使用了 `data-glyphs="光"`（`Noto Serif SC` 700 的「光」字），在 16×16 px 下汉字横画与撇捺间距不足 1.5 px，被 1 px 形态学腐蚀测试判定为笔画粘连/丢失。
  3. `Set C: INFO logo.palette: mark colour #c21806 resolved to UI tone 'accent'` —— 提示朱红色落在了 UI 强调色而非 `brand-2`。
- **第 2 轮修复与结果（`0 gate · 0 warn`）**：
  1. 将 Set A 的 `brand-2` 游标青加深为 `#007d8a`，浅底对比度提升至 `> 4.5:1`，深底上自动解析为高明度 `#00b5c4`。
  2. 将 Set B 的 `symbol_small_svg` 改为专为 16–48 px 设计的印前裁切角标 + 中心朱红校样框（线宽 14 units），彻底解决 16 px 汉字笔画粘连问题。
  3. 为 Set C 显式配置 `"brand-2": "#c21806"`，并将激活取景框内孔扩大至 `18×18`。
  4. 为三套方向显式标注 `logo.defect`（遵循 `logo.md` 诚实自检原则）并设置 `lockup.symbol_scale: 1.3`。第 2 轮运行 `brand.py logos --full` **三套全部 `0 gate · 0 warn` 通过**。

### 步骤 6：`brand.py build`（共跑 2 轮）
- **第 1 轮告警**：
  1. `WARN i18n.missing: no zh translation of the tool text; 39 label(s) shown in English. Copy .../assets/i18n/en.json to runs/b0-brand-identity-gemini4-b02/i18n.json and translate values to localise.` —— 底座未内置中文界面翻译。
  2. `Set A: WARN palette.distinct.dark.primary-accent: primary and accent share hue in dark mode (#0b3d44 vs #007d8a)` —— Set A 采用青色系同色相工作台方案，仅触发非阻断告警（`0 gate`）。
- **第 2 轮修复与结果**：
  - 在 `runs/b0-brand-identity-gemini4-b02/i18n.json` 创建完整的 39 项中文界面翻译表（`"_lang": "zh"`），重新运行 `brand.py build --full`，`i18n.missing` 告警消除，所有展示板（`board.html`、`board.png`、`review.png`、`table.md`、`sets/A|B|C/card.png`）全部更新为原生中文标签，`0 gate` 通过。

---

## 4. 中文支持问题深度剖析（实验核心发现）

在完全不修改底座代码的前提下原样跑通流程，暴露出 `brand-identity` 底座在中文品牌场景下的 **8 个系统性问题**：

### 问题 1：`slugify()` 剥离全部中文字符，导致纯中文品牌名目录名变成 `"brand"`
- **位置**：`scripts/brand.py` 第 40–43 行：
  ```python
  def slugify(name: str) -> str:
      s = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode("ascii")
      s = re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
      return s or "brand"
  ```
- **表现**：传入纯中文名 `"光桌"` 时，`encode("ascii", "ignore")` 直接清空字符串并回退到 `"brand"`，使 `brand.py init "光桌" --root <dir>` 额外创建 `<dir>/brand/` 子目录。

### 问题 2：Google Fonts 中文字体池极小 + `tnum` 门禁导致正文（`text`）字型被锁死为唯一解
- **位置**：`scripts/fontlib.py` 与 `scripts/pipeline.py`（`build_type`）。
- **表现**：
  1. Google Fonts 收录的 `zh-hans` 字体共仅 9 款（扣除 4 款手写体后仅剩 `Noto Sans SC`、`Noto Serif SC`、`WDXL Lubrifont SC`、`LXGW Marker Gothic`、`ZCOOL KuaiLe`）。
  2. 当简报启用 `--numbers`（工具类产品含分辨率、种子号、耗时等数字界面）时，`build_type()` 强制要求 `text` 字体含 OpenType `tnum` 特性。在全部 9 款中文字体中，**仅有 `Noto Sans SC` 含 `tnum`**，`Noto Serif SC` 等全部触发 `GATE type.tnum` 报错阻断。
  3. 同时 `build_type()` 要求 `mono` 角色也必须通过 `--langs zh,en` 的 `zh-hans` 字符集校验，导致无法在 `mono` 角色使用 `JetBrains Mono` / `IBM Plex Mono` 等专业代码/参数字体，只能退回用 `Noto Sans SC` 充当 `mono`。

### 问题 3：CJK 可变字体首次实例化（`OverlapMode.REMOVE`）性能瓶颈严重
- **位置**：`scripts/fontlib.py` 第 137–156 行（`resolve_font` 调用 `instantiateVariableFont(tt, ..., overlap=OverlapMode.REMOVE)`）。
- **表现**：`Noto Sans SC` 与 `Noto Serif SC` 是包含 65,535 个字形的超大 CJK 可变字体（单文件约 17 MB）。底座在固定字重时对全字库执行 `OverlapMode.REMOVE` 布尔去重，**每个字重首次运行需耗时 40–60 秒**（4 个字重首次运行累计耗时近 3 分钟），期间无进度输出，极易被误判为进程卡死。

### 问题 4：Wordmark 坐标系与主副标组合（Lockup）按拉丁字母大写高度（Cap Height）硬编码，与汉字方块框失配
- **位置**：`scripts/logolib.py`（`shape_to_svg_paths` 与 `lockup`）。
- **表现**：
  1. `shape_to_svg_paths()` 将拉丁大写字母 `H` 的高度归一化为 `100` 单位（`y = 0..100`）。但汉字（Ideographic Em-box）在字体中上下均超出 `H` 的高度：例如「光桌」二字在归一化后实际占据 `y = -13.9 .. +115.6`（总高约 `129.5` 单位），单字宽 `112..137` 单位。
  2. `lockup()` 默认将图形标（Symbol）高度设为 `1.25 × 100 = 125` 单位，并以拉丁大写中心 `y = 50` 垂直居中对齐（`sym_y = 50 - sym_h / 2`）。这导致默认 `symbol_scale=1.0` 时，图形标比旁边的汉字还矮，且在 `Noto Serif SC` 等字重下存在微小的视觉重心偏差，必须手动调大 `logo.lockup.symbol_scale`（如 `1.3`）。

### 问题 5：`wordmark-glyphs.json` 的竖画（Stem）检测算法在复杂汉字上失效
- **位置**：`scripts/logolib.py` 第 145–160 行（`_stems`）。
- **表现**：`_stems()` 仅在 `y = 100 - 0.5 * xh`（约 `y = 63`）处做一条水平扫描线，且过滤条件写死 `3 < w < 35`。当该高度恰好穿过汉字的横画或扁平框结构（如 `WDXL Lubrifont SC` 的「桌」字在 `y = 63` 处穿过日字框横画，截距宽 `> 35`）时，`_stems()` 直接返回空数组 `stems: []`，导致依赖 `stems` 坐标来对齐切口或延长线的自动化技巧失灵。

### 问题 6：底座字标改造机制（`wordmark_detail_svg`）仅支持字体转曲 + 简单布尔叠加，无法做真正的汉字造字，且 16 px 小尺寸汉字必败
- **位置**：`scripts/logolib.py`（`compose_wordmark` 与 `check_small_size`）。
- **表现**：
  1. 底座的字标流程是「HarfBuzz 直接排版现有字库字形 → `pathops` 合并外轮廓 → 叠加 `wordmark_detail_svg` 矩形切口或标尺」。对于拉丁字母，切一刀（Stencil cut）或改一个字母局部即可改变性格；但汉字笔画密集、结构严谨，直接拿开源字库转曲加小切口很难达到专业中文字标的间架重构水准。
  2. 当尝试在 `symbol_small_svg` 使用 `data-glyphs="光"` 提取汉字单字作为 16 px 小图标时，汉字多笔画结构在 16×16 px 光栅化 + 1 px 腐蚀测试下必然发生内白坍塌（`WARN logo.small-size: loses ~1.38 px² of thin strokes at 16px`），证明中文品牌在 16 px 下必须单独设计抽象几何小标，不能直接缩印汉字。

### 问题 7：未内置中文界面翻译（`i18n.missing`）与中文排版样张句子（`SAMPLES`）
- **位置**：`assets/i18n/`（仅含 `en.json` 和 `tr.json`）与 `scripts/presentlib.py`（`SAMPLES` 字典仅含 `en, tr, de, fr, es, ja, ko, ar, ru`，**唯独漏了 `zh`**）。
- **表现**：
  1. 当 `langs` 以 `zh` 开头时，`brand.py build` 报 `WARN i18n.missing: no zh translation of the tool text; 39 label(s) shown in English`，需要工作流手动创建 `i18n.json` 翻译 39 个标签。
  2. 因为 `presentlib.SAMPLES` 有 `ja` 和 `ko` 却没有 `zh`，若未在 `sets.json` 完整覆盖所有样张字段，回退句子会直接退化为英文 `The quick brown fox jumps over the lazy dog`。

### 问题 8：Identity Card 的字体大样张（Specimen）硬编码为拉丁字母 `"Aa"`
- **位置**：`scripts/identity_card.py` 第 142–150 行：
  ```python
  <div class="specimen-aa">Aa</div>
  ```
- **表现**：即便品牌语言设为 `zh`、品牌名为全中文，每套方向的 Identity Card（`sets/A|B|C/card.png`）左侧字体展示区依然硬编码渲染硕大的拉丁字母 **`Aa`**，而不是汉字代表字（如「永」或品牌首字「光」），导致无法在卡片大样张上直观检视中文字体的笔形、中宫与衬线特征。

---

## 5. 检查点并排方向总结（共 3 套方向）

已严格按照底座 `SKILL.md` §5 要求停在并排对比检查点（未运行 `kit`，未替用户做最终选择）：

1. **Set A — 双栏游标 · Split Loupe（推荐方向 `★`）**
   - **定位**：暗室级高对比桌面工作台（默认暗色底 `#0b1114` + 游标青 `#007d8a`/`#00b5c4` + 对照琥珀 `#d97706`）。
   - **标志结构**：`symbol+wordmark`（双栏取景括号 + 穿透式青色游标中轴 + 「光」字中竖分栏缺口）。
   - **字体组合**：`Noto Sans SC` 300（标题紧凑负字距）+ `Noto Sans SC` 400/600（正文与等宽参数）。
2. **Set B — 印前校样 · Proof Table**
   - **定位**：高精度印前看片台与电商商品修图（温润校样纸白 `#f8f5ef` + 碳黑 `#262322` + 校样朱砂红 `#b8291c`）。
   - **标志结构**：`wordmark` 纯字标（「光」字竖笔微距切口 + 底部朱红校样基线标尺，配合 16 px 专用印前裁切角标 `symbol-small`）。
   - **字体组合**：`Noto Serif SC` 700（粗衬线标题）+ `Noto Sans SC` 400/600（正文与参数）。
3. **Set C — 批次矩阵 · Batch Matrix**
   - **定位**：高吞吐并发出图与多图网格快选（冷灰金属底 `#f3f4f5` + 森林绿 `#174d38` + 激活帧信号红 `#c21806`）。
   - **标志结构**：`symbol+wordmark`（2×2 并发批次矩阵：3 枚实心就绪格 + 右上角信号红镂空取景框）。
   - **字体组合**：`WDXL Lubrifont SC` 400（工业刻字感窄黑体标题）+ `Noto Sans SC` 400/700（正文与参数）。

### 产物清单（`runs/b0-brand-identity-gemini4-b02/`）
- **并排检查点总览**：`board.html`、`board.png`、`review.png`、`table.md`、`logo-sheet.png`
- **单套方向卡片与矢量标志**：
  - `sets/A/card.png`、`sets/A/logo/build/*.svg` & `*.png`
  - `sets/B/card.png`、`sets/B/logo/build/*.svg` & `*.png`
  - `sets/C/card.png`、`sets/C/logo/build/*.svg` & `*.png`
- **配置与数据文件**：`sets.json`、`i18n.json`、`site/competitors.json`、`run-log.md`
