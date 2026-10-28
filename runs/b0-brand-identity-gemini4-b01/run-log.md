# B0 实验运行记录 · `brand-identity-skill` 原样测底座（简报 B01：半山烘焙）

## 1. 运行概况

| 项目 | 记录 |
| --- | --- |
| **任务 ID / Dispatch ID** | `task_324220a72bea` / `ctx_47c800a7e421` |
| **执行模型** | Gemini 4 Argon (High) |
| **测试底座** | `.bases/brand-identity-skill/skills/brand-identity`（Commit `532742d`，未修改任何底座文件） |
| **测试简报** | `test/briefs/b01-banshan.md`（成都精品咖啡豆订阅工作室「半山烘焙」） |
| **开始 / 结束时间** | `2026-10-28 12:41:57Z` → `2026-10-28 13:04:30Z` |
| **总耗时** | **约 22.5 分钟**（其中脚本耗时：`site competitors` 55s、`logos` R1 135s、`logos` R2 8s、`build` R1 190s、`build` R2 69s） |
| **总轮次（Turns）** | **14 轮模型调用**（低于 `SKILL.md` 预估的 16–20 轮），包含 **2 轮 `logos` + 2 轮 `build`** |
| **最终状态** | 到达 `SKILL.md` §5 检查点（Checkpoint）并停下；**3 套方向全部 `0 gate` 通过** |

---

## 2. 简报缺省项假设（Intake Assumptions）与真实竞品来源

按照实验要求，简报未写明且底座流程（`SKILL.md` §1 & `references/discovery-brief.md`）要求确认的事项，全部按合理假设写入 `brief.json` 与记录，未向用户提问：

### 2.1 简报参数与假设
- **组件状态（`--state`）**：`logo=new`、`type=new`、`palette=new`（简报明言“没有 Logo、没有字体、没有颜色，什么都没有”）。
- **方向数量（`--sets`）**：`3` 套（底座默认推荐值）。
- **品牌语言与文档语言**：`--langs zh,en --doc-lang zh`（中文为主，英文为辅；提议英文副标/全称为 **Banshan Roasters**）。
- **数字显示（`--numbers`）**：开启 `--numbers`（简报要求“页面会显示价格和烘焙日期（有数字）”）。
- **行业领域（`--sector`）**：`精品咖啡豆订阅与浅中烘焙工作室`
- **目标受众（`--audience`，假设）**：`在家手冲、看重产区风味与烘焙新鲜度的独立咖啡订阅订户`（25–40 岁城市手冲爱好者，关注海拔、处理法与烘焙日期，反感过度包装与商业连锁腔调）。
- **三个核心属性词（`--attributes`，假设）**：`风土本位,清透克制,诚实溯源`（不做“深烘油脂厚重感”或“网红潮流甜品风”）。
- **品牌语气与真实界面文案（`--sentence` / `--nav` / `--cta`，假设）**：
  - **语气定位**：像生豆批次溯源卡与烘焙师实验日志一样克制、平实、准确，用产地海拔、处理法与日期说话，不用浮夸形容词。
  - **中文样本句（`zh`）**：`埃塞俄比亚古吉日晒，海拔 2150 米，浅度烘焙于 10 月 28 日，¥88 / 200g。`
  - **英文样本句（`en`）**：`Guji Uraga Natural, 2150 MASL, light roast on 2026-10-28, ¥88 / 200g.`
  - **顶栏导航（`--nav`）**：`本期豆单,订阅计划,烘焙日志,产区故事`
  - **行动按钮（`--cta`）**：`开启每月鲜豆订阅`

### 2.2 真实同类竞品（5 个）及来源
简报竞品栏为空，按底座流程（`search_library.py` + `brand.py site competitors`）选取了 **3 个国内同类精品咖啡烘焙/订阅品牌 + 3 个国际浅烘订阅标杆品牌** 进行对照与实测：

1. **明谦咖啡 Mingqian Coffee**（国内行业认知来源：上海老牌精品咖啡烘焙工坊与天猫/独立站订阅豆先驱，典型黑灰工业风+产区编号视觉）。
2. **少数派咖啡 Minority Coffee**（国内行业认知来源：合肥/全国知名独立精品咖啡烘焙品牌，主打浅中烘单一产区熟豆，视觉偏干净几何与浅色卡片）。
3. **治光师 Beam Timer**（国内行业认知来源：国内代表性精品咖啡烘焙工作室，多用牛皮纸暖棕、大地色与复古标签排版）。
4. **Tim Wendelboe**（挪威奥斯陆，全球浅烘精品咖啡与按月订阅制鼻祖；通过 `brand.py site competitors` 实测 `https://timwendelboe.no`，抓取出主色 `#0073d5`、字体 `FedraSerifA-Medium / Fedra Sans L`）。
5. **La Cabra**（丹麦奥胡斯，全球浅烘订阅代表品牌；通过 `brand.py site competitors` 实测 `https://lacabra.com`，抓取出主色 `#34352a`、字体 `anth / Gotham`）与 **Sey Coffee**（美国纽约，当代浅烘微批次订阅标杆；通过 `brand.py site competitors` 实测 `https://www.seycoffee.com`，抓取出主色 `#000000`、字体 `GT-America-Condens / GT-Super-Text-Book`）。
   - *注：同时尝试抓取 `https://bluebottlecoffee.com`，被 Cloudflare Challenge 拦截（脚本返回 `blocked, skipped: page title "Attention Required! | Cloudflare"`），其余 3 个国际竞品站点实测数据已写入 `site/competitors.json`。*

---

## 3. 分步执行与报错 / 门禁修复记录

| 阶段 | 执行命令 / 动作 | 退出码 | 报错 / Gate / Warn 详情 | 处理与修复 |
| --- | --- | --- | --- | --- |
| **Step 1: Check & Init** | `brand.py check` + `brand.py init "半山烘焙" --root runs/b0-brand-identity-gemini4-b01 --sets 3 --langs zh,en --doc-lang zh --numbers ...` | `0` | 无报错，但 `slugify("半山烘焙")` 将纯中文名折叠为空串并回退生成 `brand/` 子目录 | 记录该中文路径折叠问题；后续将产物同步至 `runs/b0-brand-identity-gemini4-b01/` 根目录与 `brand/` 下 |
| **Step 2: Read References** | 读取 `cohesion.md`, `type.md`, `logo.md`, `ai-defaults.md`, `color.md`, `discovery-brief.md` | - | 无 | 按规范提炼 4 条决策轴（`warm_cool`, `classic_contemporary`, `quiet_loud`, `premium_accessible`） |
| **Step 3: Fonts & Competitors** | `search_library.py --industry food --summary`<br>`brand.py fonts search --langs zh,en --exclude-defaults`<br>`brand.py fonts search --langs zh,en --numbers`<br>`brand.py site competitors ...` | `0` | **发现严重中文+数字搜字 Bug**：`fonts search --langs zh,en` 返回 10 款，但加 `--numbers` 后只剩 `Adobe Blank` 1 款！单独跑 `fonts audit` 发现 `Noto Serif SC`、`LXGW Marker Gothic`、`WDXL Lubrifont SC`、`ZCOOL XiaoWei` 均触发 `GATE type.tnum`，唯有 `Noto Sans SC`（默认等宽数字）PASS | 确认 `pipeline.py:189` 仅对 `text` 正文角色检查 `numbers=True`；因此三套方案 `text` 统一用 `Noto Sans SC`，`display` 分别用 `Noto Serif SC`（A）、`Noto Sans SC 800`（B）、`LXGW Marker Gothic`（C）以绕开 `type.tnum` Gate 并拉开字体差异 |
| **Step 5 (R1): Logos Round 1** | 编写 `sets.json`（A 图形+字标、B 纯字标含 `wordmark_detail_svg`、C 图形+字标），运行 `brand.py logos` | `0` | **0 Gate**，但有警告：<br>• **B**：`WARN logo.small-size`（`symbol-small` 用 `data-glyphs="半"` 在 16px 下笔画粘连 1.11 px²）<br>• **C**：`WARN logo.contrast`（`#d4841c` 在 `#f7f1e6` 浅底上对比度仅 2.62:1 < 3:1）及 `WARN logo.small-size`（16px 粘连 0.99 px²） | 查看 `logo-sheet.png` 与 `wordmark-glyphs.json`：<br>• **A**：统一三层山体左右外坡斜率使轮廓共线；<br>• **B**：保留“半”字左点、改在右横做模具切口，将底部生豆青标尺拉齐四字全宽（`x=6..539`），并将 16px 小图标重构为宽孔隙几何图形；<br>• **C**：加大半拱中缝与圆点间距至 14 单位，加深琥珀色至 `#b85414` |
| **Step 5 (R2): Logos Round 2** | 更新 `sets.json`（写入 `logo.defect`）并重跑 `brand.py logos` | `0` | **A / B / C 全部 `0 gate · 0 warn`！** | 复查 `logo-sheet.png`，16px / 32px / 单色正反白全部清晰可辨 |
| **Step 6 (R1): Build Round 1** | 运行 `brand.py build ... --full` | `1` | • **B & C 触发 Gate**：`GATE text-overflow: section.band-wrap > div.band > div:nth-of-type(2) > span.bn`（色板比例条第 2 格强调色宽度仅约 8%，中英双语色名如 `水洗生豆青 Washed Green Bean` 超出容器宽度）<br>• **全局 Warn**：`WARN i18n.missing: no zh translation of the tool text; 40 label(s) shown in English`<br>• **色板 Warn**：A/C 报 `structure.lightness-range`（主辅色 `Delta L* < 25`）；B 报 `default.navy-primary`（`#182836` 落入 navy 区间） | 保留 R1 评审图备份为 `review-round1.png`；<br>1) 将 `brand[].name` 精简为 4 字中文色名（`高山松绿`、`红果朱砂`、`烘焙炭黑`、`水洗豆青`、`浅烘深褐`、`日晒铜珀`）；<br>2) 按 `i18nlib.py` 提示将 `assets/i18n/en.json` 翻译为 `<work>/i18n.json`（`"_lang": "zh"`）；<br>3) 拉大主辅色明度跨度至 `Delta L* >= 28`，并将 B 主色改为低色度炭黑 `#1c2321` |
| **Step 6 (R2): Build Round 2** | 运行 `brand.py build ... --full` | `0` | **A / B / C 全部 `0 gate`（✔）！** `i18n.missing` 与 `text-overflow` 完全清零 | 复查 `review.png` 与 `board.png`，按 `SKILL.md` §5 停在检查点 |

---

## 4. 中文支持深度诊断（字体可选、中文字标、排版与国际化）

本次原样测试暴露出 `brand-identity-skill` 底座在中文品牌场景下的 **5 个结构性问题**（按严重程度排序）：

### 4.1 【最大问题】开源中文字体极度匮乏 + `--numbers` 搜索过滤 Bug，导致含数字简报的正文字体只剩 1 款可用
1. **目录内中文字体基数极小**：
   - `brand.py fonts search --langs zh,en` 仅返回 **10 款**（扣除测试空字体 `Adobe Blank` 仅 **9 款**：`Noto Sans SC`、`Noto Serif SC`、`LXGW Marker Gothic`、`WDXL Lubrifont SC`、`ZCOOL KuaiLe`、`Zhi Mang Xing`、`Ma Shan Zheng`、`Long Cang`、`Liu Jian Mao Cao`）。
   - 其中衬线体仅 **1 款**（`Noto Serif SC`），无衬线体 **4 款**，其余 **4 款** 全是书法/手写草书。
2. **`fonts search --numbers` 存在代码级漏判 Bug**：
   - 当简报带有 `--numbers`（如本题要求显示价格与烘焙日期）时，运行 `brand.py fonts search --langs zh,en --numbers` **只返回 `Adobe Blank`（真实字体为 0 款）**。
   - **根因定位**：`scripts/font_audit.py` 第 941 行在 `search()` 中写的是 `if numbers: fams = [r for r in fams if (r.get("features") or {}).get("tnum")]`，只认 OpenType `tnum` 特性标签；而 `Noto Sans SC` 的数字本身就是默认等宽（`info["tabular"] == "default"`，无 `tnum` 特性标签）。因此 `fonts audit "Noto Sans SC" --langs zh,en --numbers` 能 PASS（0 gate），但 `fonts search --numbers` 却把它过滤掉了。
3. **正文角色（`text`）100% 撞车 + 不支持中英复合字体栈（Font Stack）**：
   - 除 `Noto Sans SC` 外，其余所有中文字体（含 `Noto Serif SC`、`LXGW Marker Gothic`、`WDXL Lubrifont SC`、`ZCOOL XiaoWei`）的数字均为比例字宽且无 `tnum`，一旦放在 `text` 角色就会触发 `GATE type.text.tnum` 阻断门禁。
   - 更严格的是，`scripts/pipeline.py` 第 189 行对 `display`、`text`、`mono` 每个角色都用完整的 `brand.languages`（`["zh", "en"]`）跑字表覆盖门禁（`100% base exemplars`）。如果为 `mono` 角色指定 `IBM Plex Mono` 或 `JetBrains Mono` 来专门显示价格数字，会因为等宽西文字体不含汉字而直接触发 `GATE type.mono.coverage.zh_Hans`！
   - **后果**：在“中文 + 数字”简报下，三套方向的 `text` 正文字体被迫 100% 绑定 `Noto Sans SC`，只能利用 `pipeline.py`“仅对 `text` 角色做 `numbers` 门禁、不对 `display` 角色做 `numbers` 门禁”的规则，在 `display` 标题字上分别选用 `Noto Serif SC`（A）、`Noto Sans SC 800`（B）、`LXGW Marker Gothic`（C）来拉开三套方案的性格差距。

### 4.2 中文字标（Chinese Wordmark）坐标系与笔画检测假设基于拉丁字母
底座的字标定制能力（`wordmark_detail_svg` + `wordmark-glyphs.json`）在概念上非常适合做“画出来的中文字标”，但底层 `scripts/logolib.py` 的几何测量完全按拉丁字母编写，实操中遇到三个具体障碍：
1. **`wordmark-glyphs.json` 的竖笔检测（`stems`）对汉字失效**：
   - `logolib.py` 第 1016–1027 行在 `y_stem = 100.0 - 0.5 * x_height`（约 `y = 64`）处做单条水平线扫描，且硬编码过滤宽度 `< 35.0` 单位的线段作为竖笔（`stems`）。
   - 汉字在 `y ≈ 64` 处极易穿过长横画——例如本题首字「半」（`Noto Sans SC 800` 与 `Noto Serif SC 600`）的下半横刚好落在 `y ≈ 64`（宽度约 122 单位 > 35），导致输出的 `wordmark-glyphs.json` 中「半」字的 `"stems": []` **直接为空数组**！模型无法依赖 `wordmark-glyphs.json` 的 `stems` 自动定位汉字主竖笔，必须根据 `x0 / x1` 字框边界人工推算笔画坐标。
2. **汉字字面框（Ideographic Em-Box）上下溢出 `0..100` 坐标系**：
   - `logolib.py` 将拉丁大写字母 `H` 的高度归一化为 `100`（`cap_top: 0, baseline: 100`）。
   - 但汉字在 CJK 字体中上沿到达约 `y = -14`（高出拉丁 cap-top），下沿延伸到约 `y = +112`（低于拉丁 baseline），单字宽度约 `132–136` 单位（4 个汉字总宽约 `543–558` 单位）。
   - 如果照搬 `templates/sets.example.json` 里拉丁字标的做法在 `y = 107` 画下划线，横线会直接切进汉字底部笔画；本次在方案 B 中将批次标尺下移至 `y = 122`、宽度设为 `496`（配合 `cx = 530` 的圆孔），才实现与「半山烘焙」四字底部的精准对齐。
3. **16px 极小尺寸下汉字笔画密集易粘连（`logo.small-size`）**：
   - 方案 B 的 `symbol_small_svg` 在第一轮使用 `data-glyphs="半"` 直接提取字体轮廓做小图标，尽管「半」字仅 5 画，在 16×16 px 的形态学开闭运算测试（`logo_audit.py:thin_features`）中仍因横画间距小于 1px 触发 `WARN logo.small-size (lost 0.88 px², clogged 1.11 px²)`。
   - 第二轮改用 100×100 网格的几何矩形重构「半」字模具骨架（将笔画间距控制在 10–12 单位，即 16px 下 ≥ 1.6px），才彻底消除 16px 小尺寸粘连警告。

### 4.3 其他中文与本地化问题
1. **纯中文品牌名 `slugify()` 退化**：`brand.py:71` 的 `slugify("半山烘焙")` 剥离所有非 ASCII 字母数字，纯中文名退化为默认的 `brand/` 文件夹名。
2. **未内置中文界面翻译（`assets/i18n/zh.json` 缺失）**：底座仅内置 `en.json` 和 `tr.json`。首次运行 `build` 会触发 `WARN i18n.missing`（40 个界面标签回退为英文），需由 agent 按提示生成 `<work>/i18n.json` 后重跑才能获得全中文展板。
3. **卡片色板条（`div.band`）对长色名容忍度低 + 字体大样固定为 `"Aa"`**：
   - 色板比例条中的强调色（Accent）色块宽度仅占约 8%，第一轮写入中英双语色名（如 `水洗生豆青 Washed Green Bean`）立即触发 `GATE text-overflow` 门禁，改为四字中文名（`水洗豆青`）后通过。
   - 卡片左下角字体排印区的超大字形样本在 `identity_card.py` 中硬编码为拉丁字母 `"Aa"`，即使在 `--langs zh,en --doc-lang zh` 下也不会展示汉字大样（如「永」或「半」），削弱了中文标题字体在卡片上的第一眼辨识度。

---

## 5. 检查点输出（Checkpoint Presentation · `SKILL.md` §5）

以下为停在检查点时的三套并排方向摘要（对应展板大图：`runs/b0-brand-identity-gemini4-b01/board.png` 与评审合图 `runs/b0-brand-identity-gemini4-b01/review.png`）：

### A — 等高风土 · Contour Terroir   ← recommended
半山海拔 1800–2200 米的等高线截面：三层阶梯山体与斜切溪谷构成符号，搭配人文衬线标题与高山冷松绿调色板。明谦、少数派与 La Cabra、Sey 多用黑灰白或牛皮纸暖棕；本方案跳出熟豆褐色定式，以产区高海拔冷松绿与地理等高截面直接呼应“产地自己会说话”。
Logo: 三层共线等高阶梯构成“半山”截面，中层右侧以咖啡红果色标定“半山腰”的海拔坐标与豆芯裂纹 · Type: Noto Serif SC 600 / Noto Sans SC 400, 600 · Colour: 高山松绿 (`#0c332c`), 红果朱砂 (`#d1323e`), 冷雾白底 (`#f4f7f5`)
Checks: All gates passed (0 gates) · 1 heuristic warning (`palette.structure.mid-lightness.brand-2`: 红果朱砂 `#d1323e` 属中等明度高饱和强调色，仅用于符号切块与按钮填充，不作长文底色) · AI-default flags: none

### B — 生豆批次单 · Origin Lot Tag
烘焙工坊的生豆批次吊牌（Lot Tag）：以字标笔画裁切与底栏打孔刻度线直接把“半山烘焙”做成一张产地溯源卡，配单字族黑体与生豆翠青色。彻底摒弃行业常见的图形徽章，用纯字标定制（wordmark-only）+ 实验室批次卡语言，在浅中烘订阅场景中凸显烘焙日期与处理法数据。
Logo: 纯中文字标定制，以重黑体“半山烘焙”为基底，首字“半”右横做批次模具切口，字标下方贯穿四字全宽的水洗生豆青批次标尺与吊牌圆孔（配专属几何“半”字小图标用于 16–48 px） · Type: Noto Sans SC 800 / Noto Sans SC 400, 600 · Colour: 烘焙炭黑 (`#1c2321`), 水洗豆青 (`#1d8558`), 浅灰青底 (`#f1f4f3`)
Checks: All gates passed (0 gates) · Warnings (uncalibrated heuristics): `palette.contrast.light.link-on-text` (2.67:1，链接需加下划线), `palette.distinct.light.success-accent` (生豆青与语义成功色相近), `cohesion.competitor-colour` (深炭黑 `#1c2321` 与 La Cabra `#34352a` / Sey `#000000` 的深色文字主色接近，靠水洗豆青强调色区分) · AI-default flags: none

### C — 浅烘日晒记 · Light-Roast Parchment
浅中烘梅纳反应的焦糖暖调与手写豆袋笔记：圆拱半山/半豆剖面符号、温润马克笔感标题字与日晒羊皮纸色板。相比国际精品咖啡（Sey、La Cabra）的冷淡几何风，保留独立烘焙工坊的温暖亲和力，但以干净的半圆拱切口取代俗套的咖啡杯具象图标。
Logo: 圆润的半山拱体被一道偏心竖缝切分为高低两瓣，右侧半山腰落下一枚日晒铜珀圆点，兼具“半山”与“咖啡豆剖面”双重阅读 · Type: LXGW Marker Gothic 400 / Noto Sans SC 400, 600 · Colour: 浅烘深褐 (`#461b0c`), 日晒铜珀 (`#b85414`), 日晒羊皮纸底 (`#f7f1e6`)
Checks: All gates passed (0 gates) · Warnings (uncalibrated heuristics): `palette.contrast.light.link-on-text`, `palette.cvd.dark.tritan.primary-accent` (蓝黄色盲模拟下深色模式主辅色接近), `palette.structure.mid-lightness.brand-2` · AI-default flags (justified from brief): `cream-ground` (对应日晒带壳豆羊皮纸 Parchment 真实物料底色), `terracotta-clay` (对应浅中烘咖啡豆焦糖化阶段的真实红棕琥珀色，区别于深烘焦黑)

Pick a set (or ask for parts of different sets). I'll build the guidelines kit for it.

---

## 6. 产物文件清单（`runs/b0-brand-identity-gemini4-b01/`）

- `board.html` / `board.png`：三套方向并排对比展板（HTML 源码与高分 PNG 导出）
- `review.png`：供设计师/评审查看的四宫格总览图（含 A/B/C 三张品牌卡 + 方案对比总览）
- `review-round1.png`：第一轮 `build` 备份图（保留了修复前的英文回退标签与 B/C 色板名称溢出 Gate 现场）
- `logo-sheet.png`：三套标志在全彩、单色浅底/深底、32px、16px（1× 与 4× 像素放大）及最小尺寸下的联系表
- `table.md`：三套方向的 Markdown 结构化对比表
- `brief.json` / `sets.json` / `i18n.json`：简报配置、三套方案完整定义（含内联 SVG）与中文界面翻译表
- `sets/A/`、`sets/B/`、`sets/C/`：各方向的独立构建产物（`card.png`、`identity.json`、`palette.json`、`type/fonts.json`、`logo/symbol.svg`、`logo/wordmark-detail.svg`、`logo/build/` 全套衍生 SVG/PNG 与 `wordmark-glyphs.json`）
- `site/competitors.json`：实测竞品站点色彩与字体抓取记录
