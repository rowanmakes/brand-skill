# B0 环境准备记录

- 日期：2026-10-28
- 执行：GLM（后端/脚本 worker，task_a5dd1bfb313f）
- 机器：Linux aarch64（arm64）容器，Python 3.13.5
- 结论：两个底座的环境检查全部通过，B0 可以开跑。字体方面确认中文衬线只有 1 款（Noto Serif SC），与 docs/basics.md 已知风险一致。

## 1. 底座提交号

两个指定提交都存在，无回退到默认分支：

| 底座 | 仓库 | 指定提交 | 实际检出 |
| --- | --- | --- | --- |
| brand-identity | https://github.com/fatihaydost/brand-identity-skill | `532742d` | `532742d7477dba3b744433adf92845642953dc28`（"Keep palette names on one line in the GIMP palette export"） |
| brand-studio | https://github.com/shadowtor/BrandDesign | `177bb77` | `177bb771bfac4ad737f9eb154379485f2f7dd9f8`（"Copy pass on README and agent install doc (#3)"） |

克隆位置：`.bases/brand-identity-skill`、`.bases/BrandDesign`（`.bases/` 已在 `.gitignore`）。两个底座的文件一律未改动，`git status` 均为空。

## 2. 装了什么

```bash
# uv（brand-identity README 推荐；两个底座靠它在首次运行时自装 Python 包）
curl -LsSf https://astral.sh/uv/install.sh | sh   # → ~/.local/bin/uv，版本 0.13.6

# Chromium：无需安装。本机已有 Playwright 缓存的 Chromium（Linux arm64）
#   /home/dev/.cache/ms-playwright/chromium-1248/chrome-linux-arm64/chrome
#   Google Chrome for Testing 156.0.8078.4
# 任务描述里"本机目前没有"已过时；实测该二进制可直接运行。

# BrandDesign 需要 PATH 上有 Chromium 内核命令名（google-chrome / chromium 等），
# 且容器里必须加 --no-sandbox。底座不支持环境变量指定浏览器，
# 所以在仓库外建了一个包装脚本（未改任何底座文件）：
mkdir -p ~/.local/bin
cat > ~/.local/bin/google-chrome <<'EOF'
#!/bin/sh
# Wrapper: Playwright Chromium (arm64) with --no-sandbox for container use.
exec /home/dev/.cache/ms-playwright/chromium-1248/chrome-linux-arm64/chrome --no-sandbox "$@"
EOF
chmod +x ~/.local/bin/google-chrome
```

Python 包（fontTools、brotli、uharfbuzz、skia-pathops 等）没有手动 pip install：两个底座都通过 uv 在缓存环境里自装，`brand.py check` 首跑即完成。BrandDesign 的 pillow/pypdf/fonttools 等同样按需自装（check 输出里是 INFO，不是 FAIL）。

## 3. 检查结果

### 3.1 brand-identity `brand.py check` — 全部通过

```text
python3 .bases/brand-identity-skill/skills/brand-identity/scripts/brand.py check
[ok] python: fontTools
[ok] python: brotli
[ok] python: uharfbuzz
[ok] python: pathops
[ok] python packages from uv (cached environment)
[ok] browser: /home/dev/.cache/ms-playwright/chromium-1248/chrome-linux-arm64/chrome
     (started in 0.8 s; started only with --no-sandbox: this system has no usable
      Chrome sandbox (typical in a container), so the skill runs the browser without it)
```

brand-identity 自带 Playwright 缓存探测和自动 `--no-sandbox`，浏览器一次通过。注：建了 `~/.local/bin/google-chrome` 包装脚本后（见第 2、4 节），它改从 PATH 解析到包装脚本——末次复跑输出 `[ok] browser: /home/dev/.local/bin/google-chrome (started in 1 s)`；两者等价，均通过。

### 3.2 BrandDesign `check_setup.py` — 通过（Ready，exit 0）

```text
python3 .bases/BrandDesign/skills/brand-studio/scripts/check_setup.py
PASS  Python 3.13.5
PASS  uv found
PASS  Chromium-based browser /home/dev/.local/bin/google-chrome
INFO  pillow / pypdf / fonttools / uharfbuzz / psd-tools / pymupdf not installed
      （均注明 "installed on demand through uv"，按需自装，非阻断）
PASS  network: Google Fonts
PASS  network: Fontsource API
PASS  network: mockups-design.com (optional photo mockups)

Ready.
```

注意：浏览器一行最初是 `FAIL ... not found`。原因见第 4 节，用 `~/.local/bin/google-chrome` 包装脚本解决后重跑通过。网络三项第一次跑就全 PASS，字体取的是 Google Fonts 合法来源，未自建字体库。

### 3.3 字体 audit：`fonts audit "Noto Serif SC" --langs zh,en` — PASS

```text
Noto Serif SC · google · OFL-1.1 · variable wght
x/H 0.703 · contrast 0.345 · I/l/1 IoU 0.766 · figures proportional only · langs zh_Hans,en_Latn
INFO  type.coverage.en_Latn.extended: lacks English auxiliary/punctuation characters: Ĕ Ĭ Ÿ ĕ ĭ
INFO  type.coverage.gf-latin-core: misses 96/319 GF Latin Core codepoints (reach beyond the brief's languages)
INFO  type.web-weight: ~968 KB WOFF2 for the brief's characters (one variable file, all weights; estimate)
result: PASS (0 gate, 0 warn, 3 info)
```

许可 OFL-1.1，可商用；数字为比例字宽（正文可用，表格数字需注意）。3 条 INFO 不阻断。

### 3.4 字体 search：`fonts search --class serif --langs zh,en` — 只返回 1 款

```text
1 families
Noto Serif SC · serif · wght 200-900 · #168
```

**serif + 中文 + 英文只有 1 款**，与 10-22 云端预检和 docs/basics.md 风险记录一致：三套方向会撞同一款中文字体。按既定原则不建字体库，跑 B0 时记录，靠字重（200–900 可变，够拉开层次）、字宽、标题排法和英文字体区分。

补充实测（供 B0 排方向时参考）：

| 查询 | 返回 |
| --- | --- |
| `--class serif --langs zh,en` | 1 款（Noto Serif SC） |
| `--class sans --langs zh,en` | 4 款（Noto Sans SC、ZCOOL KuaiLe、WDXL Lubrifont SC、LXGW Marker Gothic） |
| `--langs zh,en`（全部类别） | 10 款 |

### 3.5 冒烟测试：BrandDesign 真渲染一次 PNG — 成功

检查通过不等于渲染可用，所以用 `render_png.py` 实渲染了一张 SVG：

```text
python3 .bases/BrandDesign/skills/brand-studio/scripts/render_png.py wrap-test.svg -o wrap-test2.png --width 120 --height 60
→ wrote wrap-test2.png  120×60  via chrome        （输出 1011 字节，真实生成）
python3 .../render_png.py --which
→ available backends: chrome
```

## 4. 过程中的失败项与解决

| 问题 | 原因 | 解决 |
| --- | --- | --- |
| 直接运行 Chromium 崩溃（stack trace，exit 2） | 容器无 user namespace sandbox，Chrome 沙箱初始化失败 | 必须加 `--no-sandbox`。brand-identity 自动处理；BrandDesign 不会加 |
| BrandDesign `check_setup.py` 首跑 `FAIL Chromium-based browser not found` | 它的 `find_chrome()` 只认固定 macOS/Windows 路径和 PATH 上的命令名（google-chrome、chromium 等），不认 Playwright 缓存路径，也没有环境变量 | 建 `~/.local/bin/google-chrome` 包装脚本（`exec .../chrome --no-sandbox "$@"`），加 `--no-sandbox` 一并解决；重跑全 PASS。脚本在仓库外，未改底座 |

## 5. B0 开跑前需要设置/确认的环境

- **uv**：已在 `~/.local/bin/uv`（uv 0.13.6）。确认 `~/.local/bin` 在 PATH 里。
- **浏览器**：brand-identity 不用设置（自动探测）；如自动探测失效，用 `BRAND_IDENTITY_BROWSER=/home/dev/.cache/ms-playwright/chromium-1248/chrome-linux-arm64/chrome` 指定。
- **BrandDesign**：没有环境变量可用，必须保证 `~/.local/bin/google-chrome` 包装脚本存在且在 PATH 上。新开终端/换机器要重建这个脚本（第 2 节有完整命令）。
- **联网**：需要能访问 `fonts.googleapis.com` / `raw.githubusercontent.com`（字体）、`api.fontsource.org`（BrandDesign）、`mockups-design.com`（可选照片样机，可不用）。当前容器全部可达。
- Python 包不用手动装；首次跑某个脚本时 uv 自动装到缓存环境。

## 6. 未做 / 交接

- 未跑任何品牌生成流程（B0 由 Gemini 做）。
- 未安装 psd-tools 等可选照片样机依赖；BrandDesign 首次 `--photo-mockups` 时会从 mockups-design.com 下载 PSD（约 5 分钟），B0 不需要可以不装。
- 简报 `test/briefs/b01-banshan.md` 的竞品按 docs/basics.md 由 agent 自己找并写明。
