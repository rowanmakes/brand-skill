# Step 2 & Step 3.1 — 品类调研、陈词滥调排查、词图与概念发散

## 1. 品类惯例与自带库调研 (Category Conventions & Library Research)

### 1.1 Logo 库检索 (`search_library.py`)
- `search_library.py --query "coffee" --summary`：自带库（1,432 枚 Logo，偏科技行业）仅匹配 4 枚，75% 为具象图形（pictorial），25% 为徽章（emblem）；100% 使用 1–2 色、0% 渐变。
- `search_library.py --subject "mountain" --limit 10`：匹配 `rocky-linux-icon.svg`（圆内单刀切出山峰负空间，★ 教学范例）、`snowpack.svg`（三角形山体+山腰雪线负空间切口，★ 教学范例）、`atlassian.svg`、`nuxt.svg` 等。
- `search_library.py --technique negative-space --exemplary`：参考了 `kotlin-icon.svg`、`patreon.svg`、`rocky-linux-icon.svg`、`npm-icon.svg` 的极简布尔减法与单一负空间切口手法。
- `search_library.py --type wordmark --exemplary`：参考了 `adyen.svg`、`nextjs.svg`、`fastly.svg` 的字形局部结构改造手法。

### 1.2 行业色板库检索 (`palette/search_palettes.py`)
- `search_palettes.py --industry "food" --summary`（映射到 `food-beverage`，17 个品牌样本）：
  - 主色分布：红（41.2%）、绿（17.6%）、蓝（11.8%），棕色、中性色、粉色、黄色、紫色各 5.9%。
  - 明度结构：100% 浅色背景（64.7% 浅底+中明度主色，23.5% 浅底+深主色）。
  - 空白色相区（Open space）：青绿/冷杉色段（174°–226° teal）、紫红段（319°–18°）。
- `search_palettes.py --query "coffee"`：匹配土耳其咖啡品牌 Kahve Dünyası（主色深青绿 `#005e5b` + 浆果紫红 `#6c0c33` + 白底，走差异化策略）。

### 1.3 中文字体检索 (`live_sources.py fonts --subset chinese-simplified`)
Google Fonts（Fontsource API）支持简体中文且为 OFL-1.1 开源协议的字体共 **10 款**：
- **衬线体 (serif)**：仅 **1 款** —— `Noto Serif SC`（可变字重 200–900）
- **无衬线体 (sans-serif)**：共 **5 款** —— `Noto Sans SC`（可变字重 100–900）、`ZCOOL XiaoWei`（站酷小薇体，实为带喇叭口的衬线/展示混血，仅 400 单字重）、`ZCOOL QingKe HuangYou`（站酷庆科黄油体，圆角几何展示体，仅 400 单字重）、`WDXL Lubrifont SC`（窄体圆角黑体，仅 400 单字重）、`ZCOOL KuaiLe`（站酷快乐体，卡通风格，不适合精品烘焙）
- **手写体 (handwriting)**：共 **4 款** —— `Ma Shan Zheng`、`Zhi Mang Xing`、`Liu Jian Mao Cao`、`Long Cang`（均仅 400 单字重，毛笔/硬笔手写风，不适合现代精品咖啡的参数与数字排版）

---

## 2. 品类陈词滥调与 AI 默认套路清单 (Category Clichés & AI Defaults)

### 2.1 精品咖啡/烘焙品类陈词滥调（设计中严格规避）
1. **写实咖啡豆椭圆 + S 形中缝**：最泛滥的咖啡视觉符号，无法区分商业豆与精品浅烘。
2. **冒三道热气的咖啡杯 / 手冲壶 / 拉花心形**：代表的是线下咖啡馆堂食出杯，而非"专注生豆风土与浅中烘订阅"的烘焙工作室。
3. **美式复古徽章 / 齿轮 / 麦穗绶带 ("Fresh Roasted Since...")**：过度装饰、16 px 缩略图完全糊死，且违背"克制、让豆子自己说话"的品牌理念。
4. **普通等边三角形山峰 + 圆太阳**：户外与山系品牌的通用模板，缺乏"半山（Mid-slope）"与"烘焙/生豆"的专属扭转（Ownable Twist）。

### 2.2 AI 默认套路排查 (`bi-ai-defaults.md`)
1. **配色套路**：奶油底 + 赤陶红（Terracotta）+ 金铜色 + Fraunces 软衬线（Claude 在餐饮/烘焙简报中高达 47%–50% 的默认组合）。
2. **图形套路**：圆圈内塞入首字母 + 具象物体的生硬拼接。
3. **版式套路**：97%–100% 全部做成「左侧图标 + 右侧无修改标准字」，缺乏以汉字构造为核心的纯字标（Custom Wordmark）方向。

---

## 3. 词图发散 (Word Mapping — `discovery-brief.md` §6)

- **半山 (Mid-Slope / Half-Mountain)**
  - 具象名词与几何：山腰横切线（Horizon cut at 1/2 height）、等高线台地（Contour terrace）、云雾分界线（Cloud line）、梯田退台（Stepped slope）、汉字「半」（二分对称、两横一竖）与「山」（三峰并立）。
- **浅中烘 (Light-to-Medium Roast)**
  - 具象名词与几何：一爆裂口（First Crack seam）、烘焙滚筒观察窗（Sightglass circle）、半程刻度（Half-arc stop）、取样勺（Trier）。
- **产地与处理法自己说话 (Terroir & Processing Speak)**
  - 具象名词与几何：咖啡果横切面（Cherry cross-section）、水洗渠道（Washed channel）、日晒高架床（Raised drying bed）、标本留白窗（Specimen window）。
- **订阅制与成都基因 (Subscription & Chengdu)**
  - 具象名词与几何：批次封口签（Batch seal）、邮戳切角（Stamp notch）、盆地边缘半山云雾（Mist over the basin slope）。

---

## 4. 10 个单句概念草思与快速评分 (8–12 Concepts & Fast Scoring)

评分维度（1–5 分）：清晰度 (Clarity) · 独特性 (Distinction) · 简洁度 (Simplicity) · 相关性 (Relevance) · 小尺寸表现 (Small-Size)

| 编号 | 概念名称与标志类型 | 单句视觉概念 (One-Sentence Concept) | 清晰 | 独特 | 简洁 | 相关 | 小图 | 总分 |
| --- | --- | --- | :---: | :---: | :---: | :---: | :---: | :---: |
| **C01** | **腰线半山** · `wordmark`（汉字定制字标） | 将「半山」二字重构为几何连体字标，「半」字下横延伸化作一道水平云雾负空间切口，恰好在半山腰处将「山」字三峰拦腰切开。 | 5 | 5 | 5 | 5 | 4 | **24** ★ |
| C02 | 半山方印 · `lettermark`（汉字合文印） | 将「半」字上两点化为山间双豆，中竖与「山」字中峰合一，嵌入一枚切角几何方印。 | 4 | 4 | 4 | 4 | 4 | 20 |
| **C03** | **半山退台 B** · `letterform`（字母符号+组合） | 字母 `B`（Banshan）右侧上下双环化作两级45°山地退台（梯田），正腰处一道水平峡谷切口将山体上下二分，内留平行等高线负空间。 | 5 | 4 | 5 | 5 | 5 | **24** ★ |
| **C04** | **山谷一爆** · `pictorial/negative-space`（负空间符号+组合） | 一枚代表烘焙观察窗与果实截面的实心圆，在正腰处被45°双峰陵线与一道垂直折角山谷裂口切开——既是半山峡谷，又是浅烘豆"一爆"（First Crack）的清脆开口。 | 5 | 5 | 5 | 5 | 5 | **25** ★ |
| C05 | 日晒高架床 · `pictorial` | 45°山坡斜线上托起一座水平日晒床与半轮圆豆。 | 3 | 4 | 4 | 5 | 3 | 19 |
| C06 | 半程刻度弧 · `abstract` | 停在半圈（180°）位置的烘焙温控圆弧与指针，寓意在浅中烘停火。 | 3 | 3 | 5 | 4 | 4 | 19 |
| C07 | 产区标本签 · `emblem` | 切角豆袋吊牌外框内嵌山腰横线与「半山」文字。 | 4 | 3 | 3 | 4 | 2 | 16 |
| C08 | 取样勺 b · `letterform` | 小写字母 `b` 化作烘焙取样勺（Trier），勺肚负空间留出一座山尖。 | 4 | 4 | 4 | 4 | 3 | 19 |
| C09 | 双峰滤杯 · `pictorial` | 正看是手冲滤杯折线、倒看是双峰山脊的几何图形。 | 3 | 3 | 4 | 3 | 3 | 16 |
| C10 | BAN/SHAN 断层 · `wordmark` | 英文 `BANSHAN` 腰部水平错位切割（因简报要求中文为主，纯英文字标不选为主方向）。 | 4 | 3 | 4 | 3 | 2 | 16 |

---

## 5. 选定的三套核心方向及其单一机制 (The Three Chosen Directions & Mechanisms)

按 `mark-types.md` §12 与 `bi-cohesion.md`，选出得分最高、标志类型完全不同（**纯汉字构造字标** vs **几何首字母符号** vs **负空间双关图形**）的三套方向进入 SVG 绘制与迭代测试：

1. **方向 A — 「腰线半山」(Mid-Slope Cut) · 定制汉字字标 (`wordmark`)**
   - **单一机制 (Mechanism)**：*半山腰的一道水平云雾切线*——「半」字横画化作贯穿「山」字半腰的负空间断口；搭配高对比人文衬线中文字体与纤细无衬线英文参数；后续若选定可延展为云雾留白与生豆青褐的风土视觉。
2. **方向 B — 「半山退台 B」(Terrace B) · 几何字母符号 (`letterform`)**
   - **单一机制 (Mechanism)**：*高海拔咖啡梯田的等高线退台*——用 45° 山体切角与正腰峡谷断口构造首字母 `B`；搭配现代几何无衬线中文字标（`半`字首笔呼应 45° 退台切角）；后续若选定可延展为秩序感极强的实验室参数豆袋标签。
3. **方向 C — 「山谷一爆」(Valley Crack) · 负空间图形符号 (`pictorial` / `negative-space`)**
   - **单一机制 (Mechanism)**：*浅中烘"一爆"与半山峡谷的同构裂口*——圆盘内用单一 `evenodd` 复合路径同时切出半山双峰陵线与豆心一爆裂隙；搭配端庄宋刻感衬线字标（`山`字中峰呼应 45° 裂口尖角）；在 16 px 至包装印章尺寸下均有极强剪影辨识度。
