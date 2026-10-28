#!/usr/bin/env python3
"""Build Round 3 (v3 — Final Polished Master) SVGs and PNGs for B1-r1 (D1, D2, D3).

Refinements in v3 after visual inspection of v2 PNGs:
1. XML & Arc Fixes:
   - Escapes all <title> strings with html.escape() (fixes broken PNG rendering when title contained '<28px').
   - Properly tessellates SVG 'A' (circular arc) commands in svg_to_skia_path() so D2's lockup
     renders all three layers of d2-symbol.svg accurately.
2. D1 (腰线半山) v3 Polish:
   - Eliminates the tiny white pinholes in the 火 radical of 烘 and 焙 by extending the inner
     join of the right 45° dot and bottom-right leg well inside the central vertical spine.
   - Tightens the kerning between 半 and 山 (from 36 to 22 units) and sets 山's Left Peak top
     at y = 122 (exact collinear extension of 半's Mid-Slope Waist Bar 下横 y = 122..140)
     so the waist horizon line visually bridges straight into 山's half-mountain terrace.
3. D2 (云阶半山) v3 Polish (Rule 3 Misreading Fix):
   - Fixes the v2 misreading where 半's horizontal top dots + mid-stem break + bottom hook
     made 半 look like 芋/平:
     * Restores 半's two upper strokes (丶 丿) to 45° mountain-slope angles (matching the D2 icon's 45° peaks).
     * Removes the bottom hook on 半's vertical stem (keeping it a pure straight stem).
     * Places the 12-unit Horizontal Cloud-Slice (水平切层缝) at y = 66..78 right between the
       upper mountain-peak crown (丶 + 中竖顶峰 + 丿, y=28..66) and the lower dual-band body
       (上横 + 下横 + 中竖, y=78..212) — creating a 1:1 structural match with the D2 icon
       (mountain peak on top + horizontal cloud gap + two horizontal contour bands below)!
   - In 烘 and 焙, gives 火's left and right side strokes 45°-sloped cloud-wedge tops with flat
     horizontal cloud-sliced bottoms.
4. D3 (等高风土) v3 Polish:
   - Smooths the inner-left edge of 山's right peak (x = 364 continuous from y=72 to 195) while
     keeping the crisp dx/dy = -0.35 Mid-Waist Contour Step on the outer-right mountain slope at y = 120.
   - Harmonizes the width (24 units) and ravine slash gap (11 units, dx/dy = -0.35) of the
     Mid-Waist Cut Block (中腰切块) across 半, 烘, and 焙.
"""
import html
import json
import math
import os
import re
import sys

BASE_SCRIPTS = "/workspaces/brand-skill/.bases/BrandDesign/skills/brand-studio/scripts"
sys.path.insert(0, BASE_SCRIPTS)
import kitlib  # noqa: E402
kitlib.ensure_deps({"pathops": "skia-pathops"})
import pathops  # noqa: E402
import render_png  # noqa: E402
import svg_audit  # noqa: E402

OUT_DIR = "/workspaces/brand-skill/runs/b1-r1-banshan"
WORK_DIR = os.path.join(OUT_DIR, "work")
os.makedirs(WORK_DIR, exist_ok=True)


def poly_d(pts):
    parts = [f"M {pts[0][0]:.2f} {pts[0][1]:.2f}"]
    for x, y in pts[1:]:
        parts.append(f"L {x:.2f} {y:.2f}")
    parts.append("Z")
    return " ".join(parts)


def rect_pts(x, y, w, h):
    return [(x, y), (x + w, y), (x + w, y + h), (x, y + h)]


def arc_to_pts(x1, y1, rx, ry, phi_deg, large_arc, sweep, x2, y2, steps=32):
    """Convert SVG endpoint arc (A rx ry phi large_arc sweep x2 y2) to a list of (x, y) points."""
    if rx == 0 or ry == 0 or (x1 == x2 and y1 == y2):
        return [(x2, y2)]
    phi = math.radians(phi_deg)
    cos_phi, sin_phi = math.cos(phi), math.sin(phi)
    dx2, dy2 = (x1 - x2) / 2.0, (y1 - y2) / 2.0
    x1p = cos_phi * dx2 + sin_phi * dy2
    y1p = -sin_phi * dx2 + cos_phi * dy2
    rx, ry = abs(rx), abs(ry)
    lam = (x1p**2) / (rx**2) + (y1p**2) / (ry**2)
    if lam > 1.0:
        sr = math.sqrt(lam)
        rx *= sr
        ry *= sr
    num = max(0.0, (rx**2) * (ry**2) - (rx**2) * (y1p**2) - (ry**2) * (x1p**2))
    den = (rx**2) * (y1p**2) + (ry**2) * (x1p**2)
    sq = math.sqrt(num / den) if den > 0 else 0.0
    if bool(large_arc) == bool(sweep):
        sq = -sq
    cxp = sq * (rx * y1p / ry)
    cyp = sq * (-ry * x1p / rx)
    cx = cos_phi * cxp - sin_phi * cyp + (x1 + x2) / 2.0
    cy = sin_phi * cxp + cos_phi * cyp + (y1 + y2) / 2.0

    def angle(u, v):
        dot = u[0] * v[0] + u[1] * v[1]
        n = math.hypot(*u) * math.hypot(*v)
        c = max(-1.0, min(1.0, dot / n)) if n else 1.0
        a = math.acos(c)
        return -a if (u[0] * v[1] - u[1] * v[0]) < 0 else a

    u = ((x1p - cxp) / rx, (y1p - cyp) / ry)
    v = ((-x1p - cxp) / rx, (-y1p - cyp) / ry)
    theta1 = angle((1.0, 0.0), u)
    dtheta = angle(u, v)
    if not sweep and dtheta > 0:
        dtheta -= 2 * math.pi
    elif sweep and dtheta < 0:
        dtheta += 2 * math.pi

    pts = []
    for k in range(1, steps + 1):
        t = theta1 + dtheta * (k / steps)
        xr = rx * math.cos(t)
        yr = ry * math.sin(t)
        px = cos_phi * xr - sin_phi * yr + cx
        py = sin_phi * xr + cos_phi * yr + cy
        pts.append((px, py))
    return pts


def svg_to_skia_path(d_str):
    p = pathops.Path()
    pen = p.getPen()
    tokens = re.findall(r"[MLHVQCAZmlhvqcaz]|[-+]?\d*\.?\d+", d_str)
    i = 0
    cx, cy = 0.0, 0.0
    sx, sy = 0.0, 0.0
    cmd = None
    while i < len(tokens):
        t = tokens[i]
        if t.isalpha():
            cmd = t
            i += 1
            if cmd in ("Z", "z"):
                pen.closePath()
                cx, cy = sx, sy
                cmd = None
            continue
        if cmd == "M":
            cx, cy = float(tokens[i]), float(tokens[i + 1])
            sx, sy = cx, cy
            pen.moveTo((cx, cy))
            i += 2
            cmd = "L"
        elif cmd == "L":
            cx, cy = float(tokens[i]), float(tokens[i + 1])
            pen.lineTo((cx, cy))
            i += 2
        elif cmd == "H":
            cx = float(tokens[i])
            pen.lineTo((cx, cy))
            i += 1
        elif cmd == "V":
            cy = float(tokens[i])
            pen.lineTo((cx, cy))
            i += 1
        elif cmd == "Q":
            x1, y1 = float(tokens[i]), float(tokens[i + 1])
            cx, cy = float(tokens[i + 2]), float(tokens[i + 3])
            pen.qCurveTo((x1, y1), (cx, cy))
            i += 4
        elif cmd == "C":
            x1, y1 = float(tokens[i]), float(tokens[i + 1])
            x2, y2 = float(tokens[i + 2]), float(tokens[i + 3])
            cx, cy = float(tokens[i + 4]), float(tokens[i + 5])
            pen.curveTo((x1, y1), (x2, y2), (cx, cy))
            i += 6
        elif cmd == "A":
            rx, ry = float(tokens[i]), float(tokens[i + 1])
            phi = float(tokens[i + 2])
            large_arc = int(float(tokens[i + 3]))
            sweep = int(float(tokens[i + 4]))
            nx, ny = float(tokens[i + 5]), float(tokens[i + 6])
            for px, py in arc_to_pts(cx, cy, rx, ry, phi, large_arc, sweep, nx, ny, steps=36):
                pen.lineTo((px, py))
            cx, cy = nx, ny
            i += 7
        else:
            raise ValueError(f"Unsupported SVG path token {cmd} at {i}")
    return p


def skia_to_svg_d(path):
    cmds = []
    for verb, pts in path:
        if verb == pathops.PathVerb.MOVE:
            cmds.append(f"M {pts[0][0]:.2f} {pts[0][1]:.2f}")
        elif verb == pathops.PathVerb.LINE:
            cmds.append(f"L {pts[0][0]:.2f} {pts[0][1]:.2f}")
        elif verb == pathops.PathVerb.QUAD:
            cmds.append(f"Q {pts[0][0]:.2f} {pts[0][1]:.2f} {pts[1][0]:.2f} {pts[1][1]:.2f}")
        elif verb == pathops.PathVerb.CUBIC:
            cmds.append(
                f"C {pts[0][0]:.2f} {pts[0][1]:.2f} {pts[1][0]:.2f} {pts[1][1]:.2f} {pts[2][0]:.2f} {pts[2][1]:.2f}"
            )
        elif verb == pathops.PathVerb.CLOSE:
            cmds.append("Z")
    return " ".join(cmds)


def union_polys(polys_or_d_list, subtract_list=None):
    u = pathops.Path()
    for item in polys_or_d_list:
        d = poly_d(item) if isinstance(item, list) else item
        p = pathops.simplify(svg_to_skia_path(d), fix_winding=True)
        u = pathops.op(u, p, pathops.PathOp.UNION, fix_winding=True)
    if subtract_list:
        sub = pathops.Path()
        for item in subtract_list:
            d = poly_d(item) if isinstance(item, list) else item
            p = pathops.simplify(svg_to_skia_path(d), fix_winding=True)
            sub = pathops.op(sub, p, pathops.PathOp.UNION, fix_winding=True)
        u = pathops.op(u, sub, pathops.PathOp.DIFFERENCE, fix_winding=True)
    return skia_to_svg_d(u)


def load_path_d_and_bbox(svg_path):
    raw = open(svg_path, encoding="utf-8").read()
    m_d = re.search(r'\bd="([^"]+)"', raw)
    d = m_d.group(1)
    p = svg_to_skia_path(d)
    p = pathops.simplify(p, fix_winding=True)
    b = p.bounds
    return p, b


def transform_skia_path(p, sx, sy, tx, ty):
    out = pathops.Path()
    pen = out.getPen()
    for verb, pts in p:
        tpts = [(x * sx + tx, y * sy + ty) for (x, y) in pts]
        if verb == pathops.PathVerb.MOVE:
            pen.moveTo(tpts[0])
        elif verb == pathops.PathVerb.LINE:
            pen.lineTo(tpts[0])
        elif verb == pathops.PathVerb.QUAD:
            pen.qCurveTo(tpts[0], tpts[1])
        elif verb == pathops.PathVerb.CUBIC:
            pen.curveTo(tpts[0], tpts[1], tpts[2])
        elif verb == pathops.PathVerb.CLOSE:
            pen.closePath()
    return out


# ==============================================================================
# DIRECTION 1: 腰线半山 (D1 造字路线) — Pure Orthogonal Architectural Grid (v3)
# ==============================================================================

def build_d1_wordmark_d():
    """4-character custom architectural wordmark 半山烘焙 (ink y = 32..212).
    - 20-unit vertical stems, 18-unit horizontal bars, flat 90° terminals, 45° rectangular dots.
    - Collinear Mid-Slope Waist Line (y = 122..140) across all 4 characters:
      * 半's extended lower bar (下横 y = 122..140) leads straight across a tight 22-unit gap
        into 山's half-mountain Left Peak (top at y = 122), while 山's Central Peak rises to
        y = 32 (summit) and Right Peak rises to y = 80 (collinear with 半's 上横 y = 80).
      * All 3 vertical stems of 山 are 100% continuous to the base (zero 出/fence misreading!).
      * 烘 and 焙 are 100% custom-drawn with the exact same 20/18 architectural grid and
        locked y = 122..140 Mid-Slope Waist Bar, with solid internal overlaps in 火 (zero pinholes).
    """
    add = []
    sub = []

    # --- 1. 半 (x = 16..188, width = 172, center = 102) ---
    add.append(rect_pts(92, 32, 20, 180))
    add.append([(36, 52), (50, 38), (74, 62), (60, 76)])
    add.append([(168, 52), (154, 38), (130, 62), (144, 76)])
    add.append(rect_pts(32, 80, 140, 18))
    add.append(rect_pts(16, 122, 172, 18))  # Mid-Slope Waist Bar y = 122..140

    # --- 2. 山 (x = 210..382, width = 172, tight 22-unit bridge from 半!) ---
    add.append(rect_pts(210, 122, 20, 90))   # Left peak: top at y = 122 (half-mountain waist datum!)
    add.append(rect_pts(286, 32, 20, 180))   # Central peak: top at y = 32 (summit datum!)
    add.append(rect_pts(362, 80, 20, 132))   # Right peak: top at y = 80 (upper bar datum!)
    add.append(rect_pts(210, 194, 172, 18))  # Continuous bottom base y = 194..212

    # --- Helper for D1 architectural 火 radical (zero pinholes!) ---
    def add_d1_huo(ox):
        # Upper vertical spine (x = ox+26..ox+46, width 20) from y = 32 down to y = 142
        add.append(rect_pts(ox + 26, 32, 20, 110))
        # Left side stroke: vertical architectural bar at y = 80..122 (locked between 上横 y=80 and 腰线 y=122)
        add.append(rect_pts(ox + 0, 80, 16, 42))
        # Right side stroke: 45° rectangular block overlapping well inside the spine (ox+36) so 0 pinholes!
        add.append([(ox + 70, 88), (ox + 58, 76), (ox + 34, 100), (ox + 46, 112)])
        # Bottom-left architectural leg (撇): from waist (ox+26..46, 136) down-left to flat foot at y=212
        add.append([(ox + 26, 136), (ox + 46, 136), (ox + 20, 212), (ox + 0, 212)])
        # Bottom-right architectural leg (捺): overlaps deeply into spine (ox+30..46, 136) down-right to (ox+68, 194)
        add.append([(ox + 30, 144), (ox + 46, 136), (ox + 70, 184), (ox + 54, 194)])

    # --- 3. 烘 (x = 414..598) ---
    add_d1_huo(414)
    add.append(rect_pts(504, 32, 19, 108))
    add.append(rect_pts(551, 32, 19, 108))
    add.append(rect_pts(488, 80, 104, 18))   # Upper horizontal locked on y = 80 datum
    add.append(rect_pts(480, 122, 118, 18))  # Mid-Slope Waist Bar locked on y = 122 datum
    add.append([(506, 150), (526, 150), (500, 212), (480, 212)])
    add.append([(548, 150), (568, 150), (594, 212), (574, 212)])

    # --- 4. 焙 (x = 628..812) ---
    add_d1_huo(628)
    add.append(rect_pts(744, 32, 20, 28))
    add.append(rect_pts(700, 58, 108, 18))
    add.append([(714, 76), (732, 76), (738, 122), (720, 122)])
    add.append([(776, 76), (794, 76), (788, 122), (770, 122)])
    add.append(rect_pts(694, 122, 118, 18))  # Mid-Slope Waist Bar locked on y = 122 datum
    add.append(rect_pts(706, 152, 96, 60))
    sub.append(rect_pts(725, 169, 58, 26))

    return union_polys(add, sub)


def build_d1_badge_2char_d():
    """2-character square badge 半山 for medium sizes (28-47px) on 256x256 canvas."""
    add = []
    # 半 (x = 16..118, y = 32..224)
    add.append(rect_pts(58, 32, 18, 192))
    add.append([(20, 52), (32, 40), (50, 58), (38, 70)])
    add.append([(114, 52), (102, 40), (84, 58), (96, 70)])
    add.append(rect_pts(22, 82, 90, 16))
    add.append(rect_pts(16, 124, 102, 16))  # Mid-slope waist line y=124..140

    # 山 (x = 136..240, y = 32..224) — Unbroken 3-peak architectural 山 locked to 半's 3 datum lines!
    add.append(rect_pts(136, 124, 18, 100))  # Left peak: top at y=124 (locked to 半's waist line!)
    add.append(rect_pts(179, 32, 18, 192))   # Center peak: top at y=32 (summit)
    add.append(rect_pts(222, 82, 18, 142))   # Right peak: top at y=82 (locked to 半's upper bar!)
    add.append(rect_pts(136, 206, 104, 18))  # Continuous bottom base
    return union_polys(add)


def build_d1_small_1char_d():
    """16px (<28px) dedicated small-size mark for D1: Single character 「半」 with bold 28-unit
    strokes and 30-unit counters on 256x256."""
    add = []
    add.append(rect_pts(114, 16, 28, 224))
    add.append([(36, 52), (56, 32), (92, 68), (72, 88)])
    add.append([(220, 52), (200, 32), (164, 68), (184, 88)])
    add.append(rect_pts(44, 96, 168, 26))
    add.append(rect_pts(16, 152, 224, 28))
    return union_polys(add)


# ==============================================================================
# DIRECTION 2: 云阶半山 (D2 图标路线) — Cloud-Strata & Curved Bowl Wordmark (v3)
# ==============================================================================

def build_d2_symbol_d():
    """Preserved B0 concept-c-v4.svg icon (Twin peaks + horizontal cloud-sliced circular terraces)."""
    return (
        "M 26 108 L 110 24 L 146 60 L 164 42 L 230 108 H 26 Z "
        "M 24.08 132 H 231.92 A 104 104 0 0 1 224 168 H 32 A 104 104 0 0 1 24.08 132 Z "
        "M 46.02 192 H 209.98 A 104 104 0 0 1 46.02 192 Z"
    )


def build_d2_small_d():
    """16px (<=24px) dedicated small-size icon for D2:
    Exact 45° twin peaks (valley depth 40 units = 2.5px at 16px) + widened 28-unit horizontal cloud-slices."""
    return (
        "M 20 104 L 104 20 L 144 60 L 168 36 L 236 104 H 20 Z "
        "M 19.65 132 H 236.35 A 108 108 0 0 1 224.27 172 H 31.73 A 108 108 0 0 1 19.65 132 Z "
        "M 49.02 200 H 206.98 A 108 108 0 0 1 49.02 200 Z"
    )


def build_d2_wordmark_d():
    """4-character custom Cloud-Strata wordmark 半山烘焙 (v3 — fixes v2 芋/平 misreading on 半!).
    In v3:
    - 「半」:
      * Top section (y = 28..66): 45° mountain-ridge central peak (x=94..110) flanked by two
        45°-angled mountain-slope wedges (丶 and 丿) whose bottom edges are sliced horizontally
        at y = 66!
      * Horizontal Cloud-Slice (水平切层缝) at y = 66..78 (12 units) right above 上横!
      * Lower section (y = 78..212): Two parallel chord-beveled Horizontal Cloud-Strata bands
        (上横 y=78..95 and 下横 y=122..139) crossed by a continuous straight central stem
        (x=94..110, y=78..212, no bottom hook!) — 100% unmistakable as 「半」 and a 1:1
        structural match with the D2 icon!
    - 「山」:
      * Continuous outer U-cradle (凵) with R=28 circular-arc bowl bottom corners + tall central
        peak floating on a 12-unit Horizontal Cloud-Slice (y = 182..194) above the bottom bar.
    - 「烘」 & 「焙」:
      * Graceful curved 竖撇 + connected curved 捺 in 火, flanked by 45°-sloped cloud wedges
        with flat horizontal cloud-sliced bottoms.
      * 12-unit Horizontal Cloud-Slice (y = 108..120) separating the upper pillars of 共 and 立
        from their wide lower Horizontal Cloud-Strata band (下横 y = 120..137), paired with
        curved-bowl bottom legs/口!
    """
    add = []
    sub = []

    def chord_bar(x0, x1, y0, h=17, inset=7):
        return [
            (x0, y0),
            (x1, y0),
            (x1 - inset, y0 + h),
            (x0 + inset, y0 + h),
        ]

    # --- 1. 半 (x = 16..188) ---
    # Upper peak crown (y = 28..66):
    # Central summit peak (45° ridge top at y=28, flat cloud-sliced bottom at y=66)
    add.append([(94, 40), (106, 28), (110, 32), (110, 66), (94, 66)])
    # Left 45° mountain-slope dot (丶: slopes down-right from y=36 to flat horizontal cloud-sliced bottom at y=66)
    add.append([(38, 46), (50, 34), (76, 60), (70, 66), (52, 66)])
    # Right 45° mountain-slope dot (丿: slopes down-left from y=36 to flat horizontal cloud-sliced bottom at y=66)
    add.append([(166, 46), (154, 34), (128, 60), (134, 66), (152, 66)])
    # [12-unit Horizontal Cloud-Slice at y = 66..78!]
    # Two parallel Horizontal Cloud-Strata bands (上横 y=78..95, 下横 y=122..139) + straight central stem (y=78..212)
    add.append(chord_bar(32, 172, 78, 17, 6))
    add.append(chord_bar(16, 188, 122, 17, 7))
    add.append(rect_pts(94, 78, 16, 134))

    # --- 2. 山 (x = 220..388) ---
    add.append(
        "M 224 76 L 240 76 L 240 194 L 372 194 L 372 68 L 382 58 L 388 64 "
        "L 388 184 Q 388 211 361 211 L 251 211 Q 224 211 224 184 Z"
    )
    # Tall Central Peak floating on 12-unit Horizontal Cloud-Slice (y = 182..194)
    add.append([(298, 40), (310, 28), (314, 32), (314, 182), (298, 182)])

    # --- Helper for D2 Cloud-Strata + Curved-Bowl 火 radical ---
    def add_d2_huo(ox):
        # Central spine with 45° peak top + smooth curved left leg (竖撇)
        add.append(
            f"M {ox + 27:.2f} 40 L {ox + 39:.2f} 28 L {ox + 43:.2f} 32 L {ox + 43:.2f} 122 "
            f"Q {ox + 43:.2f} 174 {ox + 16:.2f} 212 L {ox + 0:.2f} 212 "
            f"Q {ox + 27:.2f} 170 {ox + 27:.2f} 120 Z"
        )
        # Connected curved right leg (捺)
        add.append(
            f"M {ox + 34:.2f} 126 L {ox + 43:.2f} 126 "
            f"Q {ox + 52:.2f} 162 {ox + 68:.2f} 194 L {ox + 52:.2f} 194 "
            f"Q {ox + 38:.2f} 164 {ox + 34:.2f} 126 Z"
        )
        # Left 45°-sloped cloud-wedge dot (flat horizontal bottom at y=104)
        add.append([(ox + 0, 84), (ox + 10, 74), (ox + 18, 82), (ox + 18, 104), (ox + 0, 104)])
        # Right 45°-sloped cloud-wedge dot (flat horizontal bottom at y=104)
        add.append([(ox + 50, 86), (ox + 62, 74), (ox + 70, 82), (ox + 58, 104), (ox + 50, 104)])

    # --- 3. 烘 (x = 424..608) ---
    add_d2_huo(424)
    add.append(rect_pts(516, 30, 15, 78))
    add.append(rect_pts(563, 30, 15, 78))
    add.append(chord_bar(496, 598, 76, 17, 6))
    # [12-unit Horizontal Cloud-Slice at y = 108..120]
    add.append(chord_bar(488, 608, 120, 17, 7))
    add.append("M 518 146 L 535 146 Q 527 186 506 211 L 488 211 Q 510 182 518 146 Z")
    add.append("M 559 146 L 576 146 Q 584 182 606 211 L 588 211 Q 567 186 559 146 Z")

    # --- 4. 焙 (x = 638..822) ---
    add_d2_huo(638)
    add.append([(755, 40), (767, 28), (771, 32), (771, 60), (755, 60)])
    add.append(chord_bar(710, 816, 58, 17, 6))
    add.append([(726, 75), (741, 75), (746, 108), (731, 108)])
    add.append([(785, 75), (800, 75), (795, 108), (780, 108)])
    # [12-unit Horizontal Cloud-Slice at y = 108..120]
    add.append(chord_bar(704, 822, 120, 17, 7))
    add.append("M 716 149 L 810 149 L 810 185 Q 810 211 784 211 L 742 211 Q 716 211 716 185 Z")
    sub.append("M 732 165 L 794 165 L 794 185 Q 794 195 784 195 L 742 195 Q 732 195 732 185 Z")

    return union_polys(add, sub)


# ==============================================================================
# DIRECTION 3: 等高风土 (D3 图形路线) — Angled Slash & Mid-Waist Cut Block (v3)
# ==============================================================================

SLOPE = 0.35


def build_d3_symbol_d():
    def sc(pts):
        return [(round(128 + (x - 50) * 2.4, 2), round(128 + (y - 51) * 2.4, 2)) for x, y in pts]

    polys = [
        sc([(32, 12), (68, 12), (75.7, 34), (24.3, 34)]),
        sc([(21.5, 42), (54, 42), (46.3, 64), (13.8, 64)]),
        sc([(64, 42), (78.5, 42), (86.2, 64), (56.3, 64)]),
        sc([(11, 72), (89, 72), (95.3, 90), (4.7, 90)]),
    ]
    return union_polys(polys)


def build_d3_small_d():
    """16px (<=24px) dedicated small-size icon for D3 using exact dx/dy = ±0.35 contour slope
    and widened 28-unit tier & ravine gaps."""
    polys = [
        [(74, 24), (182, 24), (200.2, 76), (55.8, 76)],            # Top tier (h=52, dx=18.2)
        [(46, 104), (126, 104), (106.4, 160), (26.4, 160)],        # Mid-left tier (h=56, dx=19.6)
        [(154, 104), (210, 104), (229.6, 160), (134.4, 160)],      # Mid-right cut block (h=56, dx=19.6)
        [(20, 188), (236, 188), (251.4, 232), (4.6, 232)],         # Base tier (h=44, dx=15.4)
    ]
    return union_polys(polys)


def trap_bar(x_top_l, x_top_r, y0, h=16):
    dx = round(h * SLOPE, 2)
    return [
        (x_top_l, y0),
        (x_top_r, y0),
        (x_top_r + dx, y0 + h),
        (x_top_l - dx, y0 + h),
    ]


def slash_stem(x, y_top, y_bot, w=18):
    dy = round(w * SLOPE, 2)
    return [
        (x, y_top + dy),
        (x + w, y_top),
        (x + w, y_bot),
        (x, y_bot),
    ]


def cut_block(x_top_l, x_top_r, y0, h=17):
    dx = round(h * SLOPE, 2)
    return [
        (x_top_l, y0),
        (x_top_r, y0),
        (x_top_r + dx, y0 + h),
        (x_top_l - dx, y0 + h),
    ]


def build_d3_wordmark_d():
    """4-character custom Contour-Slash wordmark 半山烘焙 (v3)."""
    add = []
    sub = []
    h_w = 17
    dx_w = round(h_w * SLOPE, 2)

    # --- 1. 半 (x = 16..190) ---
    add.append(slash_stem(94, 28, 212, 19))
    add.append(cut_block(44, 68, 42, 24))
    add.append([(138, 42), (162, 42), (153.6, 66), (129.6, 66)])
    add.append(trap_bar(42, 164, 78, 16))
    add.append([
        (24, 118),
        (147, 118),
        (147 - dx_w, 118 + h_w),
        (24 - dx_w, 118 + h_w),
    ])
    add.append(cut_block(158, 184, 118, h_w))

    # --- 2. 山 (x = 222..388) ---
    # Left peak: trapezoidal contour slope
    add.append([
        (234, 78.3),
        (252, 72),
        (242, 212),
        (222, 212),
    ])
    # Central summit peak
    add.append(slash_stem(296, 28, 212, 19))
    # Right peak: inner-left edge (x=358) is 100% straight and smooth from y=78 down to y=195;
    # outer-right edge has a crisp dx/dy = -0.35 Mid-Waist Contour Step at y=118 (vertical 90° outer wall below)!
    add.append([
        (358, 78.3),
        (376, 72),
        (376, 121.5),
        (386, 118),
        (386, 212),
        (358, 212),
    ])
    # Continuous bottom base
    add.append([
        (224, 195),
        (386, 195),
        (386, 212),
        (222, 212),
    ])

    # --- Helper for D3 Contour-Slash 火 radical ---
    def add_d3_huo(ox):
        add.append(slash_stem(ox + 26, 30, 140, 18))
        add.append([(ox + 4, 78), (ox + 18, 78), (ox + 6.8, 110), (ox - 7.2, 110)])
        add.append([(ox + 54, 74), (ox + 68, 74), (ox + 56.8, 106), (ox + 42.8, 106)])
        add.append([(ox + 26, 132), (ox + 44, 132), (ox + 16, 212), (ox - 2, 212)])
        add.append([(ox + 34, 138), (ox + 44, 134), (ox + 63.6, 190), (ox + 53.6, 194)])

    # --- 3. 烘 (x = 424..616) ---
    add_d3_huo(424)
    add.append(slash_stem(512, 30, 135, 18))
    add.append(slash_stem(554, 30, 135, 18))
    add.append(trap_bar(498, 588, 78, 16))
    add.append([
        (492, 118),
        (579, 118),
        (579 - dx_w, 118 + h_w),
        (492 - dx_w, 118 + h_w),
    ])
    add.append(cut_block(590, 614, 118, h_w))
    add.append([(516, 148), (534, 148), (511.6, 212), (493.6, 212)])
    add.append([(550, 148), (568, 148), (590.4, 212), (572.4, 212)])

    # --- 4. 焙 (x = 642..834) ---
    add_d3_huo(642)
    add.append(cut_block(748, 768, 28, 26))
    add.append(trap_bar(714, 806, 58, 16))
    add.append([(722, 74), (738, 74), (746, 118), (730, 118)])
    add.append([(778, 74), (794, 74), (786, 118), (770, 118)])
    add.append([
        (708, 118),
        (795, 118),
        (795 - dx_w, 118 + h_w),
        (708 - dx_w, 118 + h_w),
    ])
    add.append(cut_block(806, 830, 118, h_w))
    add.append([(720, 150), (802, 150), (812, 212), (710, 212)])
    sub.append([(736, 166), (786, 166), (792, 196), (730, 196)])

    return union_polys(add, sub)


# ==============================================================================
# LOCKUP BUILDER
# ==============================================================================

def build_bilingual_wordmark_d(zh_d, en_svg_path, target_en_h=28.0, gap_y=28.0):
    zh_p = svg_to_skia_path(zh_d)
    zh_p = pathops.simplify(zh_p, fix_winding=True)
    zx0, zy0, zx1, zy1 = zh_p.bounds
    zh_cx = (zx0 + zx1) / 2.0

    en_p, (ex0, ey0, ex1, ey1) = load_path_d_and_bbox(en_svg_path)
    en_h = ey1 - ey0
    scale = target_en_h / en_h
    tx = zh_cx - ((ex0 + ex1) / 2.0) * scale
    ty = zy1 + gap_y - ey0 * scale
    en_p_trans = transform_skia_path(en_p, scale, scale, tx, ty)

    combined = pathops.Path()
    combined.addPath(zh_p)
    combined.addPath(en_p_trans)
    combined = pathops.simplify(combined, fix_winding=True)
    return skia_to_svg_d(combined), combined.bounds, (zx0, zy0, zx1, zy1)


def build_symbol_plus_bilingual_lockup_d(sym_d, zh_d, en_svg_path, sym_to_zh_ink_ratio=1.18, gap_x=52.0):
    bilingual_d, (bx0, by0, bx1, by1), (zx0, zy0, zx1, zy1) = build_bilingual_wordmark_d(
        zh_d, en_svg_path, target_en_h=28.0, gap_y=28.0
    )
    zh_ink_h = zy1 - zy0
    sym_p = svg_to_skia_path(sym_d)
    sym_p = pathops.simplify(sym_p, fix_winding=True)
    sx0, sy0, sx1, sy1 = sym_p.bounds
    sym_h = sy1 - sy0
    target_sym_h = sym_to_zh_ink_ratio * zh_ink_h
    s_scale = target_sym_h / sym_h

    b_cy = (by0 + by1) / 2.0
    s_cy = (sy0 + sy1) / 2.0
    ty = b_cy - s_cy * s_scale
    tx = 20.0 - sx0 * s_scale
    sym_trans = transform_skia_path(sym_p, s_scale, s_scale, tx, ty)
    nsx0, nsy0, nsx1, nsy1 = sym_trans.bounds

    b_p = svg_to_skia_path(bilingual_d)
    b_shift_x = (nsx1 + gap_x) - bx0
    b_trans = transform_skia_path(b_p, 1.0, 1.0, b_shift_x, 0.0)

    out = pathops.Path()
    out.addPath(sym_trans)
    out.addPath(b_trans)
    out = pathops.simplify(out, fix_winding=True)
    return skia_to_svg_d(out), out.bounds


def write_tight_svg(path, title, d_str, pad=16, square_vb=None):
    p = svg_to_skia_path(d_str)
    x0, y0, x1, y1 = p.bounds
    if square_vb:
        vb_x, vb_y, vb_w, vb_h = 0, 0, square_vb, square_vb
    else:
        w = int(math.ceil((x1 - x0) + 2 * pad))
        h = int(math.ceil((y1 - y0) + 2 * pad))
        if w % 2:
            w += 1
        if h % 2:
            h += 1
        tx = round((w - (x1 - x0)) / 2.0 - x0, 2)
        ty = round((h - (y1 - y0)) / 2.0 - y0, 2)
        p = transform_skia_path(p, 1.0, 1.0, tx, ty)
        d_str = skia_to_svg_d(p)
        vb_x, vb_y, vb_w, vb_h = 0, 0, w, h

    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb_x} {vb_y} {vb_w} {vb_h}" '
        f'width="{vb_w}" height="{vb_h}" role="img">\n'
        f"  <title>{html.escape(title)}</title>\n"
        f'  <path fill="#111111" fill-rule="evenodd" d="{d_str}"/>\n'
        f"</svg>\n"
    )
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(svg)
    png_path = os.path.splitext(path)[0] + ".png"
    rw = max(512, vb_w)
    rh = int(round(vb_h * rw / vb_w))
    render_png.render(path, png_path, rw, rh)
    print(f"wrote {os.path.basename(path)} ({vb_w}x{vb_h}) and PNG")


def main():
    en_grotesk = os.path.join(WORK_DIR, "en-grotesk.svg")
    en_sans = os.path.join(WORK_DIR, "en-sans.svg")

    # --- D1: 腰线半山 ---
    d1_wm = build_d1_wordmark_d()
    write_tight_svg(os.path.join(OUT_DIR, "d1-wordmark.svg"), "半山烘焙 — D1 腰线半山 主字标", d1_wm, pad=20)
    d1_badge = build_d1_badge_2char_d()
    write_tight_svg(os.path.join(OUT_DIR, "d1-badge-2char.svg"), "半山 — D1 腰线半山 双字简标 (28-47px)", d1_badge, square_vb=256)
    d1_small = build_d1_small_1char_d()
    write_tight_svg(os.path.join(OUT_DIR, "d1-small.svg"), "半 — D1 腰线半山 小尺寸单字版 (under 28px / 16px)", d1_small, square_vb=256)
    d1_lock, _, _ = build_bilingual_wordmark_d(d1_wm, en_grotesk, target_en_h=28.0, gap_y=28.0)
    write_tight_svg(os.path.join(OUT_DIR, "d1-lockup.svg"), "半山烘焙 BANSHAN ROASTERS — D1 腰线半山 中英锁定组合", d1_lock, pad=20)

    # --- D2: 云阶半山 ---
    d2_sym = build_d2_symbol_d()
    write_tight_svg(os.path.join(OUT_DIR, "d2-symbol.svg"), "半山烘焙 — D2 云阶半山 图标", d2_sym, square_vb=256)
    d2_wm = build_d2_wordmark_d()
    write_tight_svg(os.path.join(OUT_DIR, "d2-wordmark.svg"), "半山烘焙 — D2 云阶半山 主字标", d2_wm, pad=20)
    d2_small = build_d2_small_d()
    write_tight_svg(os.path.join(OUT_DIR, "d2-small.svg"), "半山烘焙 — D2 云阶半山 小尺寸图标 (24px and under / 16px)", d2_small, square_vb=256)
    d2_lock, _ = build_symbol_plus_bilingual_lockup_d(d2_sym, d2_wm, en_sans, sym_to_zh_ink_ratio=1.18, gap_x=52.0)
    write_tight_svg(os.path.join(OUT_DIR, "d2-lockup.svg"), "半山烘焙 BANSHAN ROASTERS — D2 云阶半山 中英锁定组合", d2_lock, pad=20)

    # --- D3: 等高风土 ---
    d3_sym = build_d3_symbol_d()
    write_tight_svg(os.path.join(OUT_DIR, "d3-symbol.svg"), "半山烘焙 — D3 等高风土 图标 (黑白)", d3_sym, square_vb=256)
    d3_wm = build_d3_wordmark_d()
    write_tight_svg(os.path.join(OUT_DIR, "d3-wordmark.svg"), "半山烘焙 — D3 等高风土 主字标", d3_wm, pad=20)
    d3_small = build_d3_small_d()
    write_tight_svg(os.path.join(OUT_DIR, "d3-small.svg"), "半山烘焙 — D3 等高风土 小尺寸图标 (24px and under / 16px)", d3_small, square_vb=256)
    d3_lock, _ = build_symbol_plus_bilingual_lockup_d(d3_sym, d3_wm, en_sans, sym_to_zh_ink_ratio=1.18, gap_x=52.0)
    write_tight_svg(os.path.join(OUT_DIR, "d3-lockup.svg"), "半山烘焙 BANSHAN ROASTERS — D3 等高风土 中英锁定组合", d3_lock, pad=20)


if __name__ == "__main__":
    main()
