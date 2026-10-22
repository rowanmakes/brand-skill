# 测试手册

## 角色

| 角色 | 谁 |
| --- | --- |
| 协调 | GLM（OMP 加载） |
| 做品牌 | Gemini 4；需要模型对比时再加一个 GLM |
| 独立评审 | 和做品牌不同的、能看图的模型 |
| 裁判 | 用户 |

## 开跑前

- 底座需要 Python 3.10+、Chromium 内核浏览器、联网取字体，推荐装 [uv](https://docs.astral.sh/uv/)。装好后先跑 `python3 skills/brand-identity/scripts/brand.py check`（BrandDesign 是 `python skills/brand-studio/scripts/check_setup.py`）。
- 安装：把 `skills/brand-identity`（或 `skills/brand-studio`）整个目录复制到 agent 的 skills 文件夹，开新会话。
- 无人值守时 agent 要免授权启动。

## 实验 B0 提示词

```
开始前阅读 {底座 skill 目录}/SKILL.md，完全按它的流程工作，不要加别的设计规则。
任务：test/briefs/{简报}。简报里没写的，按"假设"写进记录，不要问我。
做到它的检查点（并排展示几套方向）就停下，不要替我选。
产物写到 runs/b0-{底座}-{模型}-{简报}/，只提交这个目录。写 run-log.md：用了什么模型、跑了多少轮、哪一步报错、中文哪里出问题、耗时。
```

## 用户评判时看什么

- 有没有一套让你眼前一亮；三套是不是真的不同。
- 换成同品类别的品牌，这套还成立吗？
- 中文字标好不好看、对不对。
- Logo 缩到浏览器标签那么小还认得出吗？
