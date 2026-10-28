#!/usr/bin/env python3
"""Build concepts.png (equal weight, no recommendation border/label) and per-direction
scale ladder PNGs (d1-scale-ladder.png, d2-scale-ladder.png, d3-scale-ladder.png).
"""
import html
import os
import re
import subprocess
import sys

BASE_SCRIPTS = "/workspaces/brand-skill/.bases/BrandDesign/skills/brand-studio/scripts"
sys.path.insert(0, BASE_SCRIPTS)
import kitlib  # noqa: E402
kitlib.ensure_deps({"PIL": "Pillow"})
from PIL import Image, ImageDraw, ImageFont  # noqa: E402
import concept_sheet  # noqa: E402
import render_png  # noqa: E402
import svglib  # noqa: E402

OUT_DIR = "/workspaces/brand-skill/runs/b1-r1-banshan"
WORK_DIR = os.path.join(OUT_DIR, "work")


def pad_zh_note(line1, line2):
    """Compensate for concept_sheet.py's English-centric wrap(text, 43) by padding line1
    to length 42 with zero-width spaces so line2 wraps cleanly without overflowing."""
    pad_len = max(1, 42 - len(line1))
    return line1 + ("\u200b" * pad_len) + " " + line2


def build_concepts_sheet():
    """Run concept_sheet.py without --recommend (so all 3 directions have equal weight),
    and embed the dedicated 16px small-size marks at the 16px slot with clear threshold labels."""
    f1 = os.path.join(OUT_DIR, "d1-badge-2char.svg")
    f2 = os.path.join(OUT_DIR, "d2-symbol.svg")
    f3 = os.path.join(OUT_DIR, "d3-symbol.svg")

    l1 = os.path.join(OUT_DIR, "d1-lockup.svg")
    l2 = os.path.join(OUT_DIR, "d2-lockup.svg")
    l3 = os.path.join(OUT_DIR, "d3-lockup.svg")

    s1 = os.path.join(OUT_DIR, "d1-small.svg")
    s2 = os.path.join(OUT_DIR, "d2-small.svg")
    s3 = os.path.join(OUT_DIR, "d3-small.svg")

    n1 = pad_zh_note(
        "四字全用正交建筑骨架与45°方点重绘，",
        "「半」下横接力「山」左峰；<28px切单字「半」。",
    )
    n2 = pad_zh_note(
        "保留双峰圆弧水平切层图标，四字共用12单位",
        "水平云缝与R=28圆弧底托；≤24px切小图标。",
    )
    n3 = pad_zh_note(
        "三层斜切山体转纯黑白，四字共用dx/dy=-0.35",
        "溪谷斜切角与中腰切块；≤24px切加宽层缝图标。",
    )

    out_png = os.path.join(OUT_DIR, "concepts.png")
    cmd = [
        sys.executable,
        os.path.join(BASE_SCRIPTS, "concept_sheet.py"),
        f1, f2, f3,
        "--lockups", l1, l2, l3,
        "--names",
        "D1 · 腰线半山 · 造字路线",
        "D2 · 云阶半山 · 图标路线",
        "D3 · 等高风土 · 图形路线",
        "--notes", n1, n2, n3,
        "--title", "半山烘焙 BANSHAN ROASTERS — B1-r1 中文字标与三方向并排对比",
        "--subtitle", "三套黑白方向等权并排（无推荐标记/边框）— 每套均含专属重绘四字中文字标与小尺寸切换版本。",
        "--greyscale",
        "-o", out_png,
    ]
    subprocess.run(cmd, check=True)

    # Now update concepts.svg so the 16px small-size slot embeds the dedicated 16px small-size SVG
    # (s016 -> d1-small.svg, s116 -> d2-small.svg, s216 -> d3-small.svg) and labels the switch!
    svg_path = os.path.join(OUT_DIR, "concepts.svg")
    raw = open(svg_path, encoding="utf-8").read()
    for idx, sp in enumerate([s1, s2, s3]):
        # Find the existing s{idx}16 embed tag to get its x, y coordinates
        m = re.search(
            rf'<svg[^>]*id="s{idx}16"[^>]*x="([^"]+)"\s+y="([^"]+)"\s+width="16"\s+height="16"[^>]*>.*?</svg>',
            raw,
            flags=re.S,
        )
        if not m:
            # concept_sheet.embed doesn't put id="s016" on root <svg>, it prefixes inner ids;
            # let's match by width="16" height="16" in order!
            pass

    # Replace the three width="16" height="16" nested <svg> blocks in order with embeds of s1, s2, s3
    matches = list(
        re.finditer(
            r'<svg\b[^>]*\bx="([^"]+)"\s+y="([^"]+)"\s+width="16"\s+height="16"\s+preserveAspectRatio="xMidYMid meet">.*?</svg>',
            raw,
            flags=re.S,
        )
    )
    if len(matches) == 3:
        for idx in reversed(range(3)):
            m = matches[idx]
            x_val = float(m.group(1))
            y_val = float(m.group(2))
            sp = [s1, s2, s3][idx]
            new_embed = concept_sheet.embed(sp, f"sm{idx}", x_val, y_val, 16, 16)
            raw = raw[: m.start()] + new_embed + raw[m.end() :]

    # Update the 16px caption text to "16px*"
    raw = raw.replace(">16px</text>", ">16px*</text>")
    with open(svg_path, "w", encoding="utf-8") as fh:
        fh.write(raw)

    # Re-render concepts.png from updated concepts.svg
    vb = svglib.view_box(svglib.load_svg(svg_path)[1])
    render_png.render(svg_path, out_png, int(vb[2]), int(vb[3]))
    print("updated", out_png)


def make_reversed_svg(src_svg, dst_svg):
    raw = open(src_svg, encoding="utf-8").read()
    raw = raw.replace('fill="#111111"', 'fill="#ffffff"')
    with open(dst_svg, "w", encoding="utf-8") as fh:
        fh.write(raw)


def render_exact_square_png(svg_path, size_px, bg_rgb=(255, 255, 255)):
    """Render an SVG at exact size_px x size_px via Chrome (render_png.py) and composite over bg_rgb."""
    tmp_png = os.path.join(WORK_DIR, f"_tmp_{os.path.basename(svg_path)}_{size_px}.png")
    render_png.render(svg_path, tmp_png, size_px, size_px)
    im = Image.open(tmp_png).convert("RGBA")
    bg = Image.new("RGBA", (size_px, size_px), bg_rgb + (255,))
    bg.alpha_composite(im)
    return bg.convert("RGB")


def enlarge_nearest_with_grid(im_rgb, factor):
    w, h = im_rgb.size
    big = im_rgb.resize((w * factor, h * factor), resample=Image.Resampling.NEAREST)
    if factor >= 4:
        draw = ImageDraw.Draw(big)
        for x in range(0, w * factor, factor):
            draw.line([(x, 0), (x, h * factor)], fill=(228, 228, 224), width=1)
        for y in range(0, h * factor, factor):
            draw.line([(0, y), (w * factor, y)], fill=(228, 228, 224), width=1)
    return big


def build_direction_scale_ladder(
    code,
    title,
    rule_summary,
    switch_rule,
    wordmark_svg,
    lockup_svg,
    primary_mark_svg,
    small_mark_svg,
    switch_px,
):
    """Build a comprehensive SVG+PNG Scale Ladder for one direction (1600x1080) with:
    1. Top section: Custom 4-char Wordmark (主字标) & Bilingual Lockup (中英锁定组合) + 64/32/16px wordmark test
       (showing honestly where the 4-char wordmark loses character legibility at 16px).
    2. Middle section: Responsive Scale Ladder (256 -> 128 -> 96 -> 64 -> 48 -> 32 -> 24 -> 16 px)
       with explicit switching boundary marked at switch_px.
    3. Bottom section: True rasterized 16px / 32px / 64px nearest-neighbor pixel grid enlargements
       comparing un-switched 16px vs dedicated small-size version at 16px on both #ffffff and #111111!
    """
    W, H = 1600, 1130
    font = "font-family=\"system-ui,-apple-system,'Segoe UI',Helvetica,Arial,sans-serif\""
    parts = [
        f'<rect width="{W}" height="{H}" fill="#f7f7f4"/>',
        f'<rect x="0" y="0" width="{W}" height="108" fill="#ffffff"/>',
        f'<line x1="0" y1="108" x2="{W}" y2="108" stroke="#e4e4e0" stroke-width="1"/>',
        f'<text x="48" y="50" {font} font-size="28" font-weight="700" fill="#161616">{html.escape(title)}</text>',
        f'<text x="48" y="84" {font} font-size="16" fill="#555555">{html.escape(rule_summary)}  |  {html.escape(switch_rule)}</text>',
    ]

    # --- Section 1: Wordmark & Lockup + 64/32/16px Wordmark Legibility Check (y = 128..420) ---
    parts.append(f'<rect x="48" y="128" width="1504" height="284" rx="14" fill="#ffffff" stroke="#e4e4e0" stroke-width="1"/>')
    parts.append(f'<text x="72" y="160" {font} font-size="14" font-weight="700" fill="#6b6b6b" letter-spacing="1">1. 定制四字主字标 (WORDMARK) 与中英锁定组合 (LOCKUP) 及字标直接缩小实测</text>')

    # Left box: Custom 4-char Wordmark large
    parts.append(concept_sheet.embed(wordmark_svg, f"{code}wm", 72, 180, 440, 140))
    parts.append(f'<text x="292" y="352" {font} font-size="13" fill="#6b6b6b" text-anchor="middle">四字定制主字标 ({os.path.basename(wordmark_svg)})</text>')

    # Middle box: Bilingual Lockup large
    parts.append(concept_sheet.embed(lockup_svg, f"{code}lk", 548, 180, 520, 140))
    parts.append(f'<text x="808" y="352" {font} font-size="13" fill="#6b6b6b" text-anchor="middle">中英锁定组合 ({os.path.basename(lockup_svg)})</text>')

    # Right box: Wordmark at 64px / 32px / 16px tall (honest test showing 16px wordmark illegibility)
    _, wm_root = svglib.load_svg(wordmark_svg)
    wm_vb = svglib.view_box(wm_root)
    wm_aspect = wm_vb[2] / wm_vb[3]
    parts.append(f'<line x1="1104" y1="152" x2="1104" y2="390" stroke="#ecece8" stroke-width="1"/>')
    parts.append(f'<text x="1128" y="182" {font} font-size="13" font-weight="700" fill="#444">四字主字标直缩测试（验证为何小尺寸需独立做）：</text>')

    wy = 200
    for s_h, note_txt in [
        (48, "48px 高：四字笔画与切口规则清晰可读"),
        (32, "32px 高：四字轮廓尚可认，但内白趋紧"),
        (16, "16px 高：单字宽仅15px，四字语义失效 → 必须切换小尺寸版"),
    ]:
        s_w = round(s_h * wm_aspect, 1)
        parts.append(concept_sheet.embed(wordmark_svg, f"{code}wms{s_h}", 1128, wy, s_w, s_h))
        parts.append(f'<text x="{1128 + s_w + 16:g}" y="{wy + s_h / 2 + 5:g}" {font} font-size="12" fill="#555">{html.escape(note_txt)}</text>')
        wy += s_h + 22

    # --- Section 2: Responsive Scale Ladder 256 -> 16px (y = 432..760) ---
    parts.append(f'<rect x="48" y="432" width="1504" height="332" rx="14" fill="#ffffff" stroke="#e4e4e0" stroke-width="1"/>')
    parts.append(f'<text x="72" y="464" {font} font-size="14" font-weight="700" fill="#6b6b6b" letter-spacing="1">2. 响应式尺寸阶梯 (SCALE LADDER: 16PX – 256PX) — 标明小尺寸切换阈值 ({switch_px}PX)</text>')

    ladder_sizes = [16, 20, 24, 32, 48, 64, 96, 128, 220]
    lx = 76
    base_y = 716
    for s in ladder_sizes:
        use_small = s < switch_px
        svg_to_use = small_mark_svg if use_small else primary_mark_svg
        box_s = max(36, s + 16)
        bx = lx
        by = base_y - box_s
        stroke_c = "#161616" if use_small else "#dcdcd6"
        stroke_d = ' stroke-dasharray="4 3"' if use_small else ""
        parts.append(f'<rect x="{bx}" y="{by}" width="{box_s}" height="{box_s}" rx="8" fill="#ffffff" stroke="{stroke_c}" stroke-width="1"{stroke_d}/>')
        ix = bx + (box_s - s) / 2.0
        iy = by + (box_s - s) / 2.0
        parts.append(concept_sheet.embed(svg_to_use, f"{code}lad{s}", ix, iy, s, s))
        lbl = f"{s}px*" if use_small else f"{s}px"
        parts.append(f'<text x="{bx + box_s / 2:g}" y="{base_y + 20}" {font} font-size="12" font-weight="{"700" if use_small else "400"}" fill="{"#161616" if use_small else "#6b6b6b"}" text-anchor="middle">{lbl}</text>')
        if s == 24:
            # Draw vertical switching threshold divider between 24px and 32px
            div_x = bx + box_s + 16
            parts.append(f'<line x1="{div_x}" y1="482" x2="{div_x}" y2="744" stroke="#161616" stroke-width="1.5" stroke-dasharray="5 4"/>')
            parts.append(f'<text x="{div_x}" y="496" {font} font-size="12" font-weight="700" fill="#161616" text-anchor="middle">◀ 小尺寸版 (&lt;{switch_px}px)  |  常规模版 (≥{switch_px}px) ▶</text>')
            lx = div_x + 20
        else:
            lx += box_s + 22

    # --- Section 3: Pixel Grid Enlargement placeholder box (y = 784..1090) ---
    parts.append(f'<rect x="48" y="784" width="1504" height="306" rx="14" fill="#ffffff" stroke="#e4e4e0" stroke-width="1"/>')
    parts.append(f'<text x="72" y="816" {font} font-size="14" font-weight="700" fill="#6b6b6b" letter-spacing="1">3. 16 / 32 / 64 PX 真实栅格化像素级放大实测 (PIXEL TEST: 含未切换原标 16PX 对比、1:1实寸与深底反白实测)</text>')

    cap_parts = []
    cx = 76
    cases = [
        (primary_mark_svg, 16, 8, (255, 255, 255), "未切换原标 16px (对比)"),
        (small_mark_svg, 16, 8, (255, 255, 255), "小尺寸版 16px (白底)"),
        (None, 16, 8, (17, 17, 17), "小尺寸版 16px (黑底反白)"),
        (primary_mark_svg, 32, 4, (255, 255, 255), "常规版 32px (白底)"),
        (None, 32, 4, (17, 17, 17), "常规版 32px (黑底反白)"),
        (small_mark_svg, 32, 4, (255, 255, 255), "小尺寸版 32px (白底)"),
        (primary_mark_svg, 64, 2, (255, 255, 255), "常规版 64px (白底)"),
        (None, 64, 2, (17, 17, 17), "常规版 64px (黑底反白)"),
    ]
    for _, sz, fac, _, cap in cases:
        cap_parts.append(
            f'<text x="{cx + 64}" y="1056" {font} font-size="12" font-weight="600" fill="#333333" text-anchor="middle">{html.escape(cap)}</text>'
            f'<text x="{cx + 64}" y="1074" {font} font-size="11" fill="#888888" text-anchor="middle">{sz}×{sz}px (×{fac}放大 + 1:1实寸)</text>'
        )
        cx += 182
    parts.extend(cap_parts)

    doc = (
        f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
        f'width="{W}" height="{H}" viewBox="0 0 {W} {H}">{"".join(parts)}</svg>\n'
    )
    ladder_svg = os.path.join(OUT_DIR, f"{code}-scale-ladder.svg")
    ladder_png = os.path.join(OUT_DIR, f"{code}-scale-ladder.png")
    with open(ladder_svg, "w", encoding="utf-8") as fh:
        fh.write(doc)
    render_png.render(ladder_svg, ladder_png, W, H)

    # Prepare reversed white SVGs for dark background testing
    rev_small_svg = os.path.join(WORK_DIR, f"{code}-small-white.svg")
    rev_prim_svg = os.path.join(WORK_DIR, f"{code}-prim-white.svg")
    make_reversed_svg(small_mark_svg, rev_small_svg)
    make_reversed_svg(primary_mark_svg, rev_prim_svg)

    render_cases = [
        (primary_mark_svg, 16, 8, (255, 255, 255)),
        (small_mark_svg, 16, 8, (255, 255, 255)),
        (rev_small_svg, 16, 8, (17, 17, 17)),
        (primary_mark_svg, 32, 4, (255, 255, 255)),
        (rev_prim_svg, 32, 4, (17, 17, 17)),
        (small_mark_svg, 32, 4, (255, 255, 255)),
        (primary_mark_svg, 64, 2, (255, 255, 255)),
        (rev_prim_svg, 64, 2, (17, 17, 17)),
    ]

    # Paste the pixel-enlarged tiles onto the Chrome-rendered PNG with Chinese captions
    base_im = Image.open(ladder_png).convert("RGB")
    draw = ImageDraw.Draw(base_im)
    px_x = 76
    px_y = 834
    for svg_p, sz, fac, bg_c in render_cases:
        raw_im = render_exact_square_png(svg_p, sz, bg_c)
        big_im = enlarge_nearest_with_grid(raw_im, fac)
        draw.rectangle([px_x - 1, px_y - 1, px_x + 128, px_y + 128], outline=(210, 210, 206), width=1)
        base_im.paste(big_im, (px_x, px_y))
        # Paste 1:1 true-size badge centered below the 128x128 tile
        by_1to1 = px_y + 134 + (64 - sz) // 2
        draw.rectangle([px_x + 64 - sz // 2 - 1, by_1to1 - 1, px_x + 64 - sz // 2 + sz, by_1to1 + sz], outline=(210, 210, 206), width=1)
        base_im.paste(raw_im, (px_x + 64 - sz // 2, by_1to1))
        px_x += 182
    base_im.save(ladder_png)
    print("wrote scale ladder:", ladder_png)


def main():
    build_concepts_sheet()

    build_direction_scale_ladder(
        code="d1",
        title="D1 · 腰线半山（造字路线）— 尺寸阶梯与小尺寸切换实测",
        rule_summary="规则：四字统一20/18正交建筑骨架+45°方点，半山腰线(y=122)贯通四字，「山」三峰不切断",
        switch_rule="切换阈值：≥48px 四字主字标「半山烘焙」 | 28–47px 双字简标「半山」 | <28px(含16px) 单字小尺寸版「半」",
        wordmark_svg=os.path.join(OUT_DIR, "d1-wordmark.svg"),
        lockup_svg=os.path.join(OUT_DIR, "d1-lockup.svg"),
        primary_mark_svg=os.path.join(OUT_DIR, "d1-badge-2char.svg"),
        small_mark_svg=os.path.join(OUT_DIR, "d1-small.svg"),
        switch_px=28,
    )

    build_direction_scale_ladder(
        code="d2",
        title="D2 · 云阶半山（图标路线）— 尺寸阶梯与小尺寸切换实测",
        rule_summary="规则：保留水平切层图标，四字共用12单位水平云缝+17单位弦切云带+R=28圆弧底托",
        switch_rule="切换阈值：≥48px 中英锁定组合/主字标 | 28–47px 标准云阶图标 | ≤24px(含16px) 加深双峰谷底与切层缝小尺寸图标",
        wordmark_svg=os.path.join(OUT_DIR, "d2-wordmark.svg"),
        lockup_svg=os.path.join(OUT_DIR, "d2-lockup.svg"),
        primary_mark_svg=os.path.join(OUT_DIR, "d2-symbol.svg"),
        small_mark_svg=os.path.join(OUT_DIR, "d2-small.svg"),
        switch_px=28,
    )

    build_direction_scale_ladder(
        code="d3",
        title="D3 · 等高风土（图形路线）— 尺寸阶梯与小尺寸切换实测",
        rule_summary="规则：三层斜切山体转黑白，四字共用dx/dy=-0.35溪谷斜切端头+中腰右侧梯形切块",
        switch_rule="切换阈值：≥48px 中英锁定组合/主字标 | 28–47px 标准等高图标 | ≤24px(含16px) 加宽层缝与斜切谷小尺寸图标",
        wordmark_svg=os.path.join(OUT_DIR, "d3-wordmark.svg"),
        lockup_svg=os.path.join(OUT_DIR, "d3-lockup.svg"),
        primary_mark_svg=os.path.join(OUT_DIR, "d3-symbol.svg"),
        small_mark_svg=os.path.join(OUT_DIR, "d3-small.svg"),
        switch_px=28,
    )

    # Also generate preview-sheet.html via BrandDesign's preview_sheet.py
    subprocess.run(
        [
            sys.executable,
            os.path.join(BASE_SCRIPTS, "preview_sheet.py"),
            os.path.join(OUT_DIR, "d1-wordmark.svg"),
            os.path.join(OUT_DIR, "d1-badge-2char.svg"),
            os.path.join(OUT_DIR, "d1-small.svg"),
            os.path.join(OUT_DIR, "d2-symbol.svg"),
            os.path.join(OUT_DIR, "d2-wordmark.svg"),
            os.path.join(OUT_DIR, "d2-small.svg"),
            os.path.join(OUT_DIR, "d3-symbol.svg"),
            os.path.join(OUT_DIR, "d3-wordmark.svg"),
            os.path.join(OUT_DIR, "d3-small.svg"),
            "--name", "半山烘焙 BANSHAN ROASTERS",
            "-o", os.path.join(OUT_DIR, "preview-sheet.html"),
        ],
        check=True,
    )


if __name__ == "__main__":
    main()
