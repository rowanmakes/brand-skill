# Independent design review — round 1 (concepts stage)

You are a senior brand designer and a sceptical, informed member of the client's own audience. You have NOT seen
the design process and you do not know which option the designer prefers. Judge the work against the business below,
not against taste. Do not rewrite the brief and do not redesign: report what is wrong and why, and say what to change.

## The business (the client's words)
# Design Brief — 半山烘焙 (BANSHAN ROASTERS)

## 1. 客户原始简报 (Verbatim Client Brief)

> 我在成都开了一家做精品咖啡豆的小型烘焙工作室，叫"半山烘焙"，只做订阅制卖豆，浅中烘，相信"豆子的产地和处理法自己会说话"。没有 Logo、没有字体、没有颜色，什么都没有。帮我做一套品牌：Logo、字体、颜色，以及说话的语气。
>
> - 品牌语言：中文为主，英文为辅（英文名可以由你提议）
> - 页面会显示价格和烘焙日期（有数字）
> - 竞品：{请填 3–5 个真实的同类品牌；空着则让 agent 自己找并写明}
>
> 说明：这个品牌的官网已经在 UI Skill 的实验里做过（无 Logo 版本），品牌做好后可以回到 UI Skill 验证"品牌 → 界面"的衔接。

---

## 2. 结构化设计简报 (Structured Design Brief)

- **品牌名称 (Name)**：
  - 中文主名称：**半山烘焙**（简称：**半山**）
  - 英文副名称（提议）：**BANSHAN ROASTERS**（短标：**BANSHAN**）
- **一句话定位 (Summary)**：位于成都的独立精品咖啡烘焙工作室，仅通过线上订阅制提供浅中烘单品咖啡豆，以透明、克制的方式呈现咖啡豆原本的产地风土与处理法。
- **核心理念 / 承诺 (Promise / Big Idea)**："豆子的产地和处理法自己会说话"——烘焙师不喧宾夺主，只把生长在半山海拔的豆子风味诚实地交给饮用者。
- **目标受众 (Audience)**：
  - 核心受众：25–40 岁一二线城市手冲咖啡玩家、家庭咖啡角（Home Barista）爱好者、独立审美从业者；习惯按月/双周订阅新鲜烘焙咖啡豆，看重生豆批次、海拔、处理法与烘焙日期。
  - 首要触点：订阅制官网（PC/移动端网页、16 px/32 px 浏览器标签页 Favicon、顶部导航栏）、咖啡豆包装袋与热敏批次信息标贴、随箱冲煮风味卡、微信/小红书社交头像。
- **品牌性格形容词 (Brand Adjectives)**：
  - 应该像：**克制 (Restrained)**、**通透 (Transparent / Clear)**、**风土感 (Terroir-rooted)**、**精准 (Precise)**、**温润手作 (Warm Craft)**
  - 绝不能像 (**Avoid feeling**)：**绝不像廉价商业连锁快消咖啡 (No commercial fast-food chain vibe)**、**绝不像过度做旧的美式复古徽章或浮夸网红风 (No faux-vintage rustic badges or loud trendy gimmicks)**
- **组件状态 (Components)**：
  - Logo：`new`（全新设计）
  - 字体 (Type)：`new`（全新设定，中文为主、英文为辅，需兼顾价格与烘焙日期的数字排版）
  - 色板 (Colour)：`new`（全新设定）
  - 方案方向数 (Sets)：默认 `3` 套不同类型方向（Checkpoint 1 先出黑白/灰度草图并排供选择）
- **真实同类竞品分析 (Competitive Landscape & Sources)**：
  1. **Goût & Co（味蕾与同伴）** — 成都本土代表性独立精品烘焙品牌（来源：[goutandco.com](https://goutandco.com) 及 Lightmist 报道）。主打极浅焙（Ultra-light roast）与产区透明风味；视觉采用法式极简无衬线英文标识（`GOÛT & CO`）、高对比黑白留白与实验室风格参数标贴。
  2. **少数派咖啡（Minority Coffee Roasters）** — 国内先锋独立精品咖啡烘焙厂牌（来源：BrandStar 品牌星球精品咖啡专题及天猫少数派旗舰店）。专注手冲单品与 SOE；视觉采用现代几何符号、克制的单色/双色体系与高秩序感的信息排版。
  3. **AOKKA（澳咖）** — 上海/全国知名独立精品烘焙品牌（来源：Around The Bean、GDC Award / low-key Design 包装档案）。主打"Coffee for Rawmance"户外旷野概念；视觉采用粗犷无衬线字标、高饱和大地色系以及帐篷、等高线、路标等户外图形符号。
  4. **治光师（Beamtimer / Light-Up Coffee Roasters）** — 国内头部线上独立咖啡烘焙厂牌（来源：BrandStar 品牌星球、淘宝治光师官方店）。主打干净度与高甜感；视觉采用现代感中英混排字标、明亮风味色卡与高辨识度贴纸系统。
  5. **明谦咖啡（MingQian Coffee）** — 上海老牌精品咖啡烘焙代表（来源：FoodTalks 品牌库、京东/天猫明谦旗舰店）。以茶语"明前"命名，视觉走东方极简水墨留白与科学化产地参数表结合路线。
- **必过场景与生产约束 (Must Work On & Constraints)**：
  - 网页端：16 px / 32 px 浏览器 Favicon、导航栏横版组合标、深色与浅色背景。
  - 实体包装：牛皮纸/哑光白豆袋单色印章或热敏标签（必须支持纯黑白单色印刷，无渐变依赖，最细间隙在缩小印刷时不糊死）。
  - 合规约束：字体仅限 Google Fonts 开源商用字体（OFL-1.1 / Apache），不自建未授权字体库；不编造 Pantone、CMYK 或商标检索结论。

---

## 3. 假设清单 (Assumptions Made)

以下信息原简报未明确写出，按快速通道（Fast Track）作合理假设并记录，后续可根据反馈修正：

1. **英文名称假设**：假设英文副名为 **BANSHAN ROASTERS**（主锁定组合用 **BANSHAN** 与 **半山烘焙** 搭配），发音直接对应"半山"拼音，符合中国独立精品烘焙（如 MingQian、AOKKA）的命名惯例，便于在豆袋参数表及小尺寸图形中作为结构元素。
2. **价格带与经营规模假设**：定位为中高端精品微批次与日常口粮订阅（Premium Small-Batch，单袋 200g 约 ¥68–¥168），小团队工作室运营，包装依赖低成本高质感的单色丝网印/印章 + 按批次打印的热敏标签。
3. **受众画像假设**：受众具备一定精品咖啡认知（认识水洗、日晒、厌氧处理法与产区海拔），厌恶"咖啡豆+冒热气咖啡杯"的俗套符号，偏好有耐看细节、安静不吵闹的视觉语言。
4. **避免项（Exclusions）假设**：排斥典型咖啡馆陈词滥调（冒热气的咖啡杯、写实咖啡豆裂纹、手写拉花爱心、美式复古绶带徽章）及 AI 默认套路（圆圈套隐藏字母、无理由渐变）。
5. **决策人与交付阶段假设**：由工作室主理人一人拍板；当前阶段仅推进至 **Checkpoint 1（三套黑白/灰度草图方向并排展示与独立评审）**，待确认方向后再进入上色、字体定稿与全套物料（Kit）制作。

## Look at these files (open every image; read the SVG source where it matters)
- /workspaces/brand-skill/runs/b0-BrandDesign-gemini4-b01/review/concepts-for-review-r1.png
- /workspaces/brand-skill/runs/b0-BrandDesign-gemini4-b01/concepts/concept-a-v2.svg
- /workspaces/brand-skill/runs/b0-BrandDesign-gemini4-b01/concepts/concept-b-v2.svg
- /workspaces/brand-skill/runs/b0-BrandDesign-gemini4-b01/concepts/concept-c-v2.svg
- /workspaces/brand-skill/runs/b0-BrandDesign-gemini4-b01/concepts/concept-a-lockup-v2.svg
- /workspaces/brand-skill/runs/b0-BrandDesign-gemini4-b01/concepts/concept-b-lockup-v2.svg
- /workspaces/brand-skill/runs/b0-BrandDesign-gemini4-b01/concepts/concept-c-lockup-v2.svg

## Automated audit output (measured; heuristics are labelled as such)
### concept-a-v2.svg
```
=== concept-a-v2.svg  (684 bytes)
viewBox 0 0 256 256 · aspect 1.0 (square)
colours 1: #111111 · gradients 0 · anchors 63
margins L16.0 R16.0 T32.0 B32.0 · bbox fill 0.656
✔ no issues found
production-readiness score: 100/100 (heuristic)
```

### concept-b-v2.svg
```
=== concept-b-v2.svg  (388 bytes)
viewBox 0 0 256 256 · aspect 1.0 (square)
colours 1: #111111 · gradients 0 · anchors 21
margins L40.0 R36.0 T24.0 B24.0 · bbox fill 0.571
✔ no issues found
production-readiness score: 100/100 (heuristic)
```

### concept-c-v2.svg
```
=== concept-c-v2.svg  (462 bytes)
viewBox 0 0 256 256 · aspect 1.0 (square)
colours 1: #111111 · gradients 0 · anchors 16
margins L24.0 R24.0 T24.0 B24.0 · bbox fill 0.66
✔ no issues found
production-readiness score: 100/100 (heuristic)
```

## Review checklist
1. **Fit**: does each mark feel like this business, this audience and the stated adjectives? What would a stranger
   guess the business is from the mark alone (answer BEFORE reading the idea lines)?
2. **Idea**: one sentence, relevant, ownable? Literal clip-art or category cliché? Anything that needs a paragraph?
3. **Distinction**: does it look like a known brand or a competitor in this sector? Name them if so.
4. **Craft**: letter test (every modified letter reads as intended), junctions, near-equal radii/angles, lumpy curves,
   tiny details, optical balance, spacing/kerning of the wordmark.
5. **Scale and versions**: 16 px, one colour, reversed, greyscale; favicon/avatar crop; what breaks first?
6. **Unintended readings**: rotated, mirrored, tiny, by someone who has not read the idea (body parts, letters,
   offensive or sacred symbols, hazard signs, political marks, a different word).
7. **Colour/type (when present)**: contrast, ownability in the category, licence, legibility, cultural meaning in the
   markets named in the brief.
8. **System**: does it extend to patterns, merchandise, signage, social and stationery?
9. **Honesty**: anything claimed that was not tested?

## Reply format (exactly this; be specific and short)
```
FIRST IMPRESSION (before reading the ideas): <per concept: what a stranger sees / guesses it is>
VERDICT PER CONCEPT: A: ship / fix / drop — one line why · B: … · C: …
FINDINGS (most severe first):
- [severity: blocker|major|minor] [concept] <what is wrong> — <why it matters for THIS business> — <concrete fix, e.g. "open the counter of the e from 6 to 12 units">
STRONGEST CONCEPT AND WHY: <one paragraph, include the main risk>
WHAT I COULD NOT JUDGE: <e.g. no trademark search, no print proof>
```
Do not edit files. Do not ask questions; state assumptions.
