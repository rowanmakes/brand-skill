# Design Brief — 矩台 · KADR（暂定名）

## 客户原始简报（Verbatim from Brief B02）
一款给设计师和插画师用的 AI 生图桌面工具，有手机端和桌面端。核心是工作台：排队生成、对比、精修。用户是专业创作者，讨厌花哨。名字还没定，先叫“{待定}”。帮我做品牌：名字建议、Logo、字体、颜色、语气。

- **品牌语言**：中英并用
- **产品界面特征**：界面里有大量数字（参数、队列、耗时）
- **对标竞品**：Midjourney、Krea、Leonardo、Lovart、即梦

---

## 结构化简报（Structured Brief）

- **Summary（一句话概述）**：面向专业设计师与插画师的跨端（桌面端 + 手机端）AI 图像生成与精修工作台，以高密度的排队生成、并排对比与像素级精修为核心工作流。
- **Audience（目标受众）**：视觉设计师、商业插画师、艺术指导、概念设计师。他们在日常高强度生产中使用该工具，最先在桌面端 Dock/任务栏图标、应用工作台顶栏、手机端 App 图标及导出水印/规范文档中接触品牌标识。
- **Brand adjectives（品牌气质形容词）**：精准（Precise）、克制（Restrained）、可靠（Dependable）、专业工具感（Instrumental）、干练（Crisp）。
- **Avoid feeling（绝不能像什么）**：绝不能花哨炫技（No flashy/gimmicky AI magic）、绝不能廉价玩具感或玄学感（No toy-like/mystical sci-fi tropes）。
- **Promise / Big idea（核心承诺）**：把不可控的生成变成可控的精修工作台（Turn stochastic generation into a calibrated workbench）。
- **Competitors（竞品与行业现状）**：
  - **Midjourney**：帆船具象线描图标 + 深色 Discord/Web 极简界面，偏探索与艺术幻想。
  - **Krea**：高对比几何抽象色块/节点图形 + 现代无衬线字标，偏实时生成与潮流创意。
  - **Leonardo**：狮头/奇幻插画感徽标 + 蓝紫霓虹渐变，偏游戏资产与大众创作者，视觉较花哨。
  - **Lovart**：偏设计代理/画布协作感。
  - **即梦（Jimeng）**：字节系 AI 创作平台，偏大众娱乐与轻快渐变色彩。
- **Must work on（核心应用场景）**：桌面端应用图标（macOS Dock / Windows 任务栏 16 px–32 px）、手机端 App 图标、深色工作台 UI 顶栏（Dark mode）、网站 Favicon、参数面板与队列状态栏。
- **Constraints（硬性约束）**：
  - 中英双语并行（需要同时考量中文品牌字形与英文名称的识别度与排印匹配）。
  - 界面含大量实时数字（Seed、CFG、步数、队列编号、毫秒耗时），字体系统需支持等宽/表格数字（Tabular figures）且数字 0/O、1/l/I 严格区分。
  - 图形必须在 16 px 极小尺寸、纯黑单色与深色背景反白下清晰可辨，不依赖渐变、阴影或发光。

---

## 假设清单（Assumptions Made — 简报未明确项）

1. **品牌命名假设（Naming Assumption）**：底座 `BrandDesign`（`brand-studio`）流程无独立起名阶段，按规则提议 1 个中英双语名称并作为本次设计输入：**矩台 · KADR**。
   - **中文名「矩台」**：「矩」取规矩、曲尺、画幅裁切框与矩阵之意，代表精准尺度与参数控制；「台」取暗房看片台、印前校样台与桌面工作台之意，直指排队、对比、精修的核心场景。
   - **英文名「KADR」**：源自法/俄/波兰语 *cadre / kadr*（电影画幅、取景框、结构骨架），4 字母短词，发音干脆，字母骨架（K、A、D、R）几何特征鲜明，适合桌面工具与快捷键式专业语境。
2. **组件范围（Per-part scope）**：Logo = `new`、字体（Type）= `new`、色板（Colour）= `new`，无既有品牌资产约束。
3. **价格与定位（Price & Positioning）**：面向专业创作者与工作室的 Pro 级订阅制生产力工具（Premium / Professional tool），非免费娱乐应用。
4. **市场与语言（Markets & Languages）**：中国大陆及全球专业设计市场，界面与品牌物料采用简体中文（`zh-Hans`）与英文（`en-Latn`）双语并行。
5. **色彩底色倾向（Ground preference）**：专业修图与生图工作台以中性深灰/炭黑暗房底色（Dark UI ground）与高显色性浅灰看片台底色为主，严格避开泛滥的“AI 蓝紫渐变”与魔法星芒。
6. **决策与交付阶段（Checkpoint scope）**：当前阶段仅执行至 `BrandDesign` Checkpoint 1（三套不同标识类型的黑白/灰阶方向并排展示 + 独立子代理评审），停下等待用户选择，不在用户选择前提前产出彩色定稿与物料包。
