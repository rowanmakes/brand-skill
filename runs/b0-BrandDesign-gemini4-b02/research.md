# Step 2 & 3.1 Research, Word Map & Concept Selection — 矩台 · KADR

## 1. Category Conventions (from Bundled Library & Palette Library)

### 1.1 Logo Library (`search_library.py`)
- **`--industry design-creative --summary` (35 logos)**:
  - **Mark types**: wordmark 25.7%, abstract 20.0%, pictorial 17.1%, letterform 14.3%, combination 11.4%, lettermark 8.6%.
  - **Primary colour**: mono 31.4%, multi 28.6%, blue 20.0%, red 8.6%. 63% use 1–2 colours; gradients in only 6%.
  - **Dominant techniques**: containment (28.6%), color-segments (20.0%), dimensional-shading (17.1%), geometric-construction (14.3%), negative-space (14.3%).
  - **Exemplary**: `framer.svg` (modular triangles/squares forming F), `precursor.svg` (open arc + bar forming P), `figma.svg`, `sketch.svg`, `squarespace.svg`.
- **`--industry ai-ml --summary` (12 logos)**:
  - **Mark types**: abstract 33.3%, pictorial 16.7%, letterform 16.7%, combination 16.7%.
  - **Dominant techniques**: line-monoline (33.3%), dimensional-shading (25.0%), radial-symmetry (25.0%), modular-repetition (25.0%), negative-space (25.0%).
  - **Geometry**: circle (33.3%), hexagon (25.0%).

### 1.2 Brand Palette Library (`palette/search_palettes.py`)
- **`--industry saas --summary` (23 brands)** & **`--industry agency --summary` (14 brands)**:
  - SaaS is heavily crowded in **blue (65.2% presence)**, **red (34.8%)**, and **purple (30.4%)**.
  - Design agencies strongly favour **neutral monochrome (42.9%)** with 50% using a dark ground (`Linear`, `Vercel`, `Figma`).
  - **Open space**: neutral carbon/slate workbench ground paired with a single high-visibility instrument accent (e.g. darkroom safelight amber/vermilion or calibration teal/chartreuse), strictly avoiding AI indigo/violet gradients.

---

## 2. Category Clichés & AI Defaults to Avoid (`bi-ai-defaults.md`)

### Category Clichés (Human & Sector)
1. **Four-point AI sparkle / magic wand / stars（四芒星与魔法棒）**：泛 AI 工具最泛滥的视觉陈词滥调，暗示“玄学抽卡/一键魔法”，与专业创作者看重的“可控工作台、精修”完全相悖。
2. **Radial swirl / hexagonal neural nodes（放射旋涡与六边形神经节点）**：模仿 OpenAI 或通用算力节点的套路图形，缺乏“图像画幅、排版裁切、看片对比”的行业属性。
3. **Blue-to-purple neon gradients & glowing orbs（蓝紫霓虹渐变与发光球）**：Leonardo、即梦等消费级生成工具常见，视觉花哨且干扰设计师对色彩与明度的判断。
4. **Literal paintbrush / palette / camera shutter blades（具象画笔、调色盘或密集光圈叶片）**：传统修图软件陈旧套路，且密集叶片在 16 px 极小尺寸下会糊成一团。

### Model AI Defaults (`bi-ai-defaults.md`)
- Avoid `Fraunces` + `Inter` + cream/terracotta/gold cluster.
- Avoid `Space Grotesk` / `Sora` + indigo/violet tech cliché without justification.
- Do not make all 3 concepts the same "symbol + wordmark" formula — include truly different mark types (a negative-space letterform, a geometric instrument/abstract symbol, and a custom-crafted bilingual wordmark/monogram).

---

## 3. Word Map (`discovery-brief.md` §6)

- **矩 (Rule / Carpenter's Square / Matrix / Crop Frame)**
  → 鲁班曲尺（L-square, 90° precision angle）、裁切框角标（crop marks `⌜ ⌟`）、画幅比例框（aspect frame）、游标卡尺（caliper）、基准线（datum line）。
- **台 (Workbench / Lightbox / Platen / Galley)**
  → 暗房透光看片台（lightbox platen）、印前校样盘（galley tray）、压印平板（platen）、分屏对照槽（split comparison bay）。
- **排队 · 对比 · 精修 (Queue · Compare · Retouch)**
  → 胶片接触印相条（contact strip / queue slots）、A/B 垂直分屏滑块（split-wipe comparator）、放大目镜（loupe）、精修手术刀斜面（45° chisel / scalpel bevel）。
- **KADR / 矩台 字形几何交集 (Letter & Character Intersections)**
  → `K` 的左竖直立柱 = 90° 曲尺基准尺（`矩` 的左竖与L折角）；`K` 的右侧上下两道 45° 斜臂 = 从看片台投射出的上下对比视场 / 裁切切角。
  → `矩` 右部「巨」与 `台` 下部「口」皆为严整的方框内腔结构，可与拉丁字母 `K / A / D / R` 的直角内腔建立统一的「曲尺折角缺口」视觉机制。

---

## 4. Ten One-Sentence Concepts & Fast Scoring (`SKILL.md` §3.1)

| # | Name | Mark Type | One-sentence concept | Clarity | Distinction | Simplicity | Relevance | 16px Scale | Total (/25) |
|---|---|---|---|---|---|---|---|---|---|
| 1 | **Calibrated K（曲尺看片台 K）** | Letterform / Negative Space | A solid square lightbox platen split by a 90° carpenter's L-rule and two 45° comparison channels so the positive tiles and negative seam simultaneously form a **K** and a carpenter's square (**矩**). | 5 | 5 | 5 | 5 | 5 | **25** ★ (Pick A) |
| 2 | **Queue-to-Lock（排队比对窗）** | Abstract / Instrument Symbol | Three stepped generation queue bars on the left feed across a vertical comparison split into one locked square master frame on the right: queue, compare, commit. | 5 | 5 | 4 | 5 | 5 | **24** ★ (Pick B) |
| 3 | **Crop-Rule Wordmark（裁切曲尺字标）** | Custom Wordmark / Monogram | A custom bilingual wordmark (`矩台 KADR`) where `矩` and `KADR` are constructed with matching 90° crop-frame bracket cuts and a 45° chisel terminal, paired with a compact `矩K` stencil monogram for 16 px slots. | 5 | 4 | 5 | 5 | 4 | **23** ★ (Pick C) |
| 4 | **Loupe Stand（目镜校样台）** | Pictorial | A top-down draftsman's loupe resting on a square platen base with a 45° measurement notch. | 4 | 3 | 4 | 4 | 4 | 19 |
| 5 | **Split Wipe（分屏滑块）** | Abstract | Two overlapping square frames divided by a vertical wipe bar with opposing arrowheads. | 4 | 3 | 4 | 5 | 3 | 19 |
| 6 | **Galley Tray（排样匣）** | Emblem | Four contact-sheet cells inside a heavy printer's chase with the bottom-right cell lifted out. | 3 | 4 | 3 | 4 | 3 | 17 |
| 7 | **Vernier K（游标卡尺 K）** | Letterform | A letter K built from two sliding caliper jaws clamping a square canvas. | 4 | 4 | 3 | 4 | 3 | 18 |
| 8 | **Prism Platen（棱镜台）** | Pictorial | An isometric glass block splitting a vertical line into three parallel tracks on a flat table. | 3 | 3 | 3 | 4 | 3 | 16 |
| 9 | **Reticle R-K（准星单字）** | Lettermark | Interlocked K and R sharing a crosshair centre inside a crop bracket. | 3 | 3 | 3 | 3 | 3 | 15 |
| 10 | **Scalpel Frame（精修刀框）** | Negative Space | A square picture frame whose bottom-right corner is sliced by a 45° retouching blade. | 4 | 3 | 5 | 3 | 4 | 19 |

---

## 5. Three Selected Concepts & Their Mechanisms (`bi-cohesion.md`)

1. **Direction A — Calibrated K / 曲尺看片台 (`Letterform / Negative Space`)**
   - **Library precedents studied**: `kotlin-icon.svg`, `framer.svg`, `pagekit.svg` (solid geometric mass carved by exact 45°/90° negative channels).
   - **Mechanism**: *The carpenter's L-square & 45° calibration seam* — one structural rule yields a bold square-footprint `K` platen mark, stencil-notched terminals in the bilingual wordmark, and a darkroom carbon + safelight vermilion palette.
2. **Direction B — Queue & Lock / 队列比对窗 (`Abstract / Pictorial Instrument Symbol`)**
   - **Library precedents studied**: `squarespace.svg`, `microsoft.svg`, `unocss.svg` (modular geometric units expressing workflow structure without fine hairlines).
   - **Mechanism**: *Three queued strips → one locked frame* — visualising the product's core workflow (queued generations on the left, vertical comparison split in the middle, locked final canvas on the right) in solid architectural blocks.
3. **Direction C — Crop-Rule Wordmark / 矩尺造字字标 (`Custom Wordmark + Monogram Avatar`)**
   - **Library precedents studied**: `pagekit.svg`, `npm-icon.svg`, `precursor.svg` (typographic architecture where the letterforms themselves carry the framing device).
   - **Mechanism**: *The 90° crop-bracket (`⌜ ⌟`) & 45° chisel cut* — custom-drawn and modified glyph geometry uniting Chinese `矩台` and Latin `KADR` into a single precision instrument nameplate, with a companion `K·矩` crop-frame monogram for 16 px app/favicon use.
