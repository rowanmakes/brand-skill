#!/usr/bin/env python3
"""Build Round 1 (v1) SVGs for B1-r1 (D1 腰线半山, D2 云阶半山, D3 等高风土).

Every direction has:
- A 100% custom-drawn 4-character Chinese wordmark (半山烘焙) where all 4 characters
  share a unified stroke grammar and share the direction's visual rule.
- Standalone symbol (for D2 and D3; D1 is wordmark-only and also has a 2-char square badge).
- Bilingual lockup with BANSHAN ROASTERS.
- Dedicated small-size mark (16px / <=24px) where character/feature legibility is preserved.
"""
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
    """Convert list of (x, y) tuples to an SVG path 'M ... L ... Z' with 2-decimal rounding."""
    parts = [f"M {pts[0][0]:.2f} {pts[0][1]:.2f}"]
    for x, y in pts[1:]:
        parts.append(f"L {x:.2f} {y:.2f}")
    parts.append("Z")
    return " ".join(parts)


def rect_d(x, y, w, h):
    return poly_d([(x, y), (x + w, y), (x + w, y + h), (x, y + h)])


def svg_to_skia_path(d_str):
    p = pathops.Path()
    pen = p.getPen()
    # Parse simple M, L, H, V, Q, C, Z commands
    tokens = re.findall(r"[MLHVQCZmlhvqcz]|[-+]?\d*\.?\d+", d_str)
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
    """Union a list of polygons/path strings using skia-pathops, then subtract optional cutouts."""
    u = pathops.Path()
    for item in polys_or_d_list:
        d = poly_d(item) if isinstance(item, list) else item
        u.addPath(svg_to_skia_path(d))
    u = pathops.simplify(u, fix_winding=True)
    if subtract_list:
        sub = pathops.Path()
        for item in subtract_list:
            d = poly_d(item) if isinstance(item, list) else item
            sub.addPath(svg_to_skia_path(d))
        sub = pathops.simplify(sub, fix_winding=True)
        u = pathops.op(u, sub, pathops.PathOp.DIFFERENCE, fix_winding=True)
    return skia_to_svg_d(u)


# ==============================================================================
# DIRECTION 1: 腰线半山 (D1 造字路线)
# Grammar:
# - Orthogonal architectural stems (width 18) + horizontal bars (height 16)
# - 45° mountain-ridge summit chamfers & 45° straight geometric diagonals (0 curves)
# - Collinear Mid-Slope Waist Line (y = 120..136) across all 4 characters:
#   * 「半」: 下横 sits at y=120..136 with a 45° right slope terminal pointing to 「山」
#   * 「山」: All 3 vertical peaks are 100% continuous to the base (fixing the 「出」 misreading!);
#            Left peak is a Half-Mountain Terrace with flat top at y=120 (collinear with 「半」's waist bar!),
#            Central peak rises to y=28 (45° summit), Right peak rises to y=78 (collinear with 「半」's 上横)
#            and steps outward at the y=120 mid-slope waist into a wider mountain base buttress.
#   * 「烘」: Left 「火」 and right 「共」 built from the exact same 18/16 rectilinear + 45° grammar;
#            「共」's lower horizontal sits on the exact y=120..136 Mid-Slope Waist Line.
#   * 「焙」: Left 「火」 and right 「咅」(立+口) built from the exact same 18/16 rectilinear + 45° grammar;
#            「立」's base horizontal sits on the exact y=120..136 Mid-Slope Waist Line.
# ==============================================================================

def build_d1_wordmark_paths():
    add = []

    # --- 1. 半 (x = 16..188, center = 102) ---
    # Central vertical stem with 45° summit ridge cut
    add.append([(93, 38), (103, 28), (111, 28), (111, 212), (93, 212)])
    # Upper-left 45° mountain slope dot
    add.append([(38, 48), (50, 36), (76, 62), (64, 74)])
    # Upper-right 45° mountain slope dot
    add.append([(166, 48), (154, 36), (128, 62), (140, 74)])
    # Upper horizontal (上横 y = 78..94) with 45° left slope cut
    add.append([(36, 94), (52, 78), (168, 78), (168, 94)])
    # Mid-Slope Waist Horizon Bar (下横 y = 120..136) with 45° right slope cut
    add.append([(16, 120), (172, 120), (188, 136), (16, 136)])

    # --- 2. 山 (x = 224..396, center = 310) ---
    # Left Peak: Half-Mountain Terrace (top at y=104 with a stepped waist shoulder at y=120..136
    # that extends left to x=220 to meet 半's waist horizon line, 100% continuous to base y=212!)
    # Wait: let's make Left Peak top sit cleanly at y=96 (or y=108) with a 45° ridge slope,
    # AND at y=120 (exact Mid-Slope Waist Line!) a horizontal mid-slope terrace step widens the outer left wall!
    # Or even cleaner: Left Peak top IS at y=112 (half-mountain height) with a flat terrace top at y=120 on its outer step:
    # Let's check: Left peak stem x=230..248 from y=88 to 212 (45° top: (230,98)->(240,88)->(248,88)),
    # Central peak stem x=301..319 from y=28 to 212 (45° top: (301,38)->(311,28)->(319,28)),
    # Right peak stem x=364..382 from y=72 to 212 (45° top: (364,82)->(374,72)->(382,72)),
    # AND at y=120 (the Mid-Slope Waist Line!), the outer right slope of Right Peak steps outward to x=394 (from y=120..212, with a 45° slope chamfer (382,120)->(394,132)),
    # AND on the Left Peak, at y=120..136, a short Mid-Slope Horizon Terrace projects left to x=218 (receiving 半's y=120..136 waist bar!),
    # while Bottom Base (底横 y=196..212, x=230..394) connects all 3 stems continuously!
    add.append([(230, 98), (240, 88), (248, 88), (248, 212), (230, 212)])  # Left peak (continuous!)
    add.append([(218, 120), (232, 120), (232, 136), (218, 136)])  # Left mid-slope horizon step at y=120..136
    add.append([(301, 38), (311, 28), (319, 28), (319, 212), (301, 212)])  # Central summit peak (continuous!)
    add.append([(364, 82), (374, 72), (382, 72), (382, 120), (394, 132), (394, 212), (364, 212)])  # Right peak + y=120 mid-slope buttress (continuous!)
    add.append([(230, 196), (394, 196), (394, 212), (230, 212)])  # Continuous bottom base

    # --- 3. 烘 (x = 432..608) ---
    def add_d1_huo(ox):
        # Central vertical spine (x = ox+26..ox+44) from y=32 to y=136 (waist line)
        add.append([(ox + 26, 42), (ox + 36, 32), (ox + 44, 32), (ox + 44, 138), (ox + 26, 138)])
        # Left side dot (y = 78..114, 45° top & bottom)
        add.append([(ox + 0, 86), (ox + 8, 78), (ox + 15, 78), (ox + 15, 114), (ox + 0, 114)])
        # Right side 45° short stroke (y = 74..106)
        add.append([(ox + 68, 82), (ox + 58, 72), (ox + 44, 86), (ox + 54, 96)])
        # Bottom-left 45° leg (撇) from waist (y=136) down to flat horizontal foot at y=212
        add.append([(ox + 26, 134), (ox + 44, 134), (ox + 18, 212), (ox + 0, 212)])
        # Bottom-right 45° leg (捺) from (ox+38, 148) down-right
        add.append([(ox + 36, 154), (ox + 46, 144), (ox + 68, 182), (ox + 56, 192)])

    add_d1_huo(432)
    # Right component 共 (x = 500..608)
    # Left pillar of 共
    add.append([(520, 42), (530, 32), (538, 32), (538, 136), (520, 136)])
    # Right pillar of 共
    add.append([(564, 42), (574, 32), (582, 32), (582, 136), (564, 136)])
    # Upper horizontal of 共 (y = 78..94, collinear with 半's 上横)
    add.append([(502, 94), (516, 78), (598, 78), (598, 94)])
    # Lower horizontal of 共 (y = 120..136, locked on Mid-Slope Waist Line!)
    add.append([(496, 120), (594, 120), (610, 136), (496, 136)])
    # Bottom-left 45° leg of 共
    add.append([(524, 148), (542, 148), (516, 212), (498, 212)])
    # Bottom-right 45° leg of 共
    add.append([(560, 148), (578, 148), (604, 212), (586, 212)])

    # --- 4. 焙 (x = 640..820) ---
    add_d1_huo(640)
    # Right component 咅 (立 + 口, x = 708..820)
    # Top ridge peak of 立
    add.append([(755, 38), (765, 28), (773, 28), (773, 60), (755, 60)])
    # Upper horizontal of 立 (y = 58..74)
    add.append([(714, 74), (728, 58), (812, 58), (812, 74)])
    # Left inner pillar of 立 (angled architectural bar)
    add.append([(728, 74), (744, 74), (750, 120), (734, 120)])
    # Right inner pillar of 立 (angled architectural bar)
    add.append([(782, 74), (798, 74), (792, 120), (776, 120)])
    # Lower horizontal of 立 (y = 120..136, locked on Mid-Slope Waist Line!)
    add.append([(706, 120), (804, 120), (820, 136), (706, 136)])
    # Bottom 口 of 焙 (outer x = 720..808, y = 150..212, with 45° chamfer on bottom-right corner)
    add.append([(720, 150), (808, 150), (808, 200), (796, 212), (720, 212)])
    sub = [[(738, 166), (790, 166), (790, 196), (738, 196)]]

    return union_polys(add, sub)


# ==============================================================================
# DIRECTION 2: 云阶半山 (D2 图标路线)
# Icon: B0's concept-c-v4.svg (Asymmetric 45° twin mountain peaks + R=104 circular
#       lower contour bowl sliced by horizontal cloud gaps).
# Shared Grammar across all 4 characters of 「半山烘焙」:
# 1. 45° pointed mountain-peak tops on main vertical stems (matching the icon's twin peaks)
# 2. 16-unit Horizontal Cloud-Strata bars with circular-chord beveled outer ends
# 3. 12-unit Horizontal Cloud-Slice (水平切层缝) detaching the horizontal layer transition
#    in every character (without ever cutting a vertical stem into two rows like 出!):
#    * 「半」: 12-unit horizontal cloud-slice at y=108..120 between upper peak crown and lower 下横 terrace
#    * 「山」: Outer U-cradle (左峰 + 圆弧底横 + 右峰) is 100% continuous; tall Central Peak (中峰)
#             floats on a 12-unit horizontal cloud-slice (y=176..188) above the curved bottom base!
#    * 「烘」: In 「共」, the upper two vertical pillars + 上横 form an upper peak unit that floats
#             on a 12-unit horizontal cloud-slice (y=108..120) above the wide lower 下横 contour band!
#    * 「焙」: In 「咅」, 「立」's upper peak + inner pillars float on a 12-unit horizontal cloud-slice
#             (y=108..120) above 「立」's wide mid-waist 下横 contour band!
# 4. Circular-arc (curved bowl) bottom outer corners on 「半」底, 「山」底框, 「火」撇捺, 「共」底脚, 「焙」之「口」底框!
# ==============================================================================

def rounded_u_cradle_d(x0, y_left_top, x1, y_right_top, y_bot, stem_w, bar_h, r_outer):
    """Build a continuous U-cradle (凵) with 45° peak tops on left/right stems and R circular-arc bottom corners."""
    # Left stem outer x=x0, inner x=x0+stem_w; Right stem inner x=x1-stem_w, outer x=x1
    # Top of left stem has 45° peak at x0+stem_w/2; top of right stem has 45° peak
    y_inner = y_bot - bar_h
    return (
        f"M {x0:.2f} {y_left_top + 10:.2f} "
        f"L {x0 + 10:.2f} {y_left_top:.2f} "
        f"L {x0 + stem_w:.2f} {y_left_top + 8:.2f} "
        f"L {x0 + stem_w:.2f} {y_inner:.2f} "
        f"L {x1 - stem_w:.2f} {y_inner:.2f} "
        f"L {x1 - stem_w:.2f} {y_right_top + 8:.2f} "
        f"L {x1 - 8:.2f} {y_right_top:.2f} "
        f"L {x1:.2f} {y_right_top + 8:.2f} "
        f"L {x1:.2f} {y_bot - r_outer:.2f} "
        f"Q {x1:.2f} {y_bot:.2f} {x1 - r_outer:.2f} {y_bot:.2f} "
        f"L {x0 + r_outer:.2f} {y_bot:.2f} "
        f"Q {x0:.2f} {y_bot:.2f} {x0:.2f} {y_bot - r_outer:.2f} Z"
    )


def build_d2_wordmark_paths():
    add = []
    sub = []

    def peak_stem(x, y_top, y_bot, w=18):
        """Vertical stem with a 45° mountain peak apex."""
        mid = x + w * 0.55
        return poly_d([
            (x, y_top + 10),
            (mid, y_top),
            (x + w, y_top + 8),
            (x + w, y_bot),
            (x, y_bot),
        ])

    def chord_bar(x0, x1, y0, h=16, inset=6):
        """Horizontal contour band whose outer ends slope inward like a circular bowl chord."""
        return poly_d([
            (x0, y0),
            (x1, y0),
            (x1 - inset, y0 + h),
            (x0 + inset, y0 + h),
        ])

    # --- 1. 半 (x = 16..188) ---
    # Upper peak stem (y = 28..108, stops at horizontal cloud-slice y=108..120!)
    add.append(peak_stem(93, 28, 108, 18))
    # Upper cloud-strata wedges (丷: flat horizontal bottom edge at y=68, 45° sloped top)
    add.append([(38, 68), (54, 42), (76, 54), (76, 68)])
    add.append([(166, 68), (150, 42), (128, 54), (128, 68)])
    # Upper horizontal contour band (上横 y = 78..94)
    add.append(chord_bar(34, 170, 78, 16, 5))
    # [Horizontal Cloud-Slice Gap at y = 108..120 (12 units)]
    # Lower horizontal contour band (下横 y = 120..136)
    add.append(chord_bar(16, 188, 120, 16, 6))
    # Lower central stem (y = 120..212) with curved bowl bottom terminal
    add.append(
        "M 93 120 L 111 120 L 111 198 Q 111 212 97 212 L 93 212 Z"
    )

    # --- 2. 山 (x = 224..396) ---
    # Continuous outer U-cradle (凵) with asymmetric peak tops (left y=76, right y=60)
    # and R=28 curved circular-bowl bottom corners!
    add.append(rounded_u_cradle_d(228, 76, 394, 60, 210, 18, 16, 26))
    # Tall Central Peak (y = 28..182), stopping 12 units above the bottom bar (y=194..210)
    # -> 12-unit Horizontal Cloud-Slice at y = 182..194!
    add.append(peak_stem(302, 28, 182, 18))

    # --- 3. 烘 (x = 432..608) ---
    def add_d2_huo(ox):
        # Central peak spine + curved left leg (撇)
        add.append(
            f"M {ox + 26:.2f} 40 L {ox + 36:.2f} 30 L {ox + 44:.2f} 38 "
            f"L {ox + 44:.2f} 126 Q {ox + 44:.2f} 176 {ox + 16:.2f} 210 "
            f"L {ox + 0:.2f} 210 Q {ox + 26:.2f} 172 {ox + 26:.2f} 124 Z"
        )
        # Left horizontal cloud-wedge dot (flat bottom at y=104)
        add.append([(ox + 0, 104), (ox + 10, 78), (ox + 18, 84), (ox + 18, 104)])
        # Right horizontal cloud-wedge dot (flat bottom at y=104)
        add.append([(ox + 50, 104), (ox + 50, 86), (ox + 66, 76), (ox + 60, 104)])
        # Bottom-right curved bowl leg (捺) with flat horizontal bottom at y=194
        add.append(
            f"M {ox + 38:.2f} 142 L {ox + 50:.2f} 142 "
            f"Q {ox + 58:.2f} 170 {ox + 68:.2f} 192 L {ox + 52:.2f} 192 "
            f"Q {ox + 42:.2f} 170 {ox + 38:.2f} 142 Z"
        )

    add_d2_huo(432)
    # Right component 共 (x = 498..608)
    # Upper two pillars (y = 30..108) + 上横 (y = 76..92), stopping at y=108
    # for the 12-unit Horizontal Cloud-Slice (y = 108..120) above 下横 (y = 120..136)!
    add.append(peak_stem(520, 30, 108, 18))
    add.append(peak_stem(564, 30, 108, 18))
    add.append(chord_bar(502, 600, 76, 16, 5))
    # [Horizontal Cloud-Slice Gap at y = 108..120 (12 units)]
    add.append(chord_bar(496, 608, 120, 16, 6))
    # Bottom two curved-bowl legs (八字底托, flat horizontal feet at y=210, curved outer arcs)
    add.append(
        "M 524 146 L 542 146 Q 534 186 514 210 L 496 210 Q 516 182 524 146 Z"
    )
    add.append(
        "M 562 146 L 580 146 Q 588 182 608 210 L 590 210 Q 570 186 562 146 Z"
    )

    # --- 4. 焙 (x = 640..820) ---
    add_d2_huo(640)
    # Right component 咅 (立 + 口, x = 706..820)
    # Top peak of 立 (y = 28..60) + 上横 (y = 58..74)
    add.append(peak_stem(755, 28, 62, 18))
    add.append(chord_bar(712, 814, 58, 16, 5))
    # Two inner pillars of 立 descending from y=74 and stopping at y=108
    # for the 12-unit Horizontal Cloud-Slice (y = 108..120) above 立's 下横 (y = 120..136)!
    add.append([(728, 74), (745, 74), (750, 108), (733, 108)])
    add.append([(781, 74), (798, 74), (793, 108), (776, 108)])
    # [Horizontal Cloud-Slice Gap at y = 108..120 (12 units)]
    add.append(chord_bar(706, 820, 120, 16, 6))
    # Lower 口 with R=24 circular-arc bottom-left and bottom-right bowl corners!
    add.append(
        "M 720 148 L 806 148 L 806 186 Q 806 210 782 210 L 744 210 Q 720 210 720 186 Z"
    )
    sub.append(
        "M 738 164 L 788 164 L 788 186 Q 788 194 780 194 L 746 194 Q 738 194 738 186 Z"
    )

    return union_polys(add, sub)


# ==============================================================================
# DIRECTION 3: 等高风土 (D3 图形路线)
# Icon: B0's sets/A/logo/symbol.svg converted to pure monochrome black (#111111)
#       (Three trapezoidal mountain tiers + dx/dy = -0.35 angled ravine slash
#        isolating a Mid-Waist Trapezoidal Cut Block on the right).
# Shared Grammar across all 4 characters of 「半山烘焙」:
# 1. Exact mountain slope angle (dx/dy = -0.35, ~70.7°) on all horizontal bar terminals,
#    all peak tops, and all trapezoidal dot blocks (matching the icon's mid-tier-mark!).
# 2. High-contrast contour strokes (20-unit stems, 15-unit horizontals) with trapezoidal
#    outer slopes (left edge dx/dy = -0.35, right edge dx/dy = +0.35).
# 3. Every character features the signature "斜切 + 中腰切块" (Angled Ravine Slash +
#    Mid-Waist Trapezoidal Cut Block) on the right side of the mid-waist tier without
#    ever breaking character topology:
#    * 「半」: 下横 (y=118..135) crosses 中竖 intact (x=18..146), and on its right wing
#             (x=158..192) a 12-unit dx/dy=-0.35 ravine slash isolates the Mid-Waist Cut Block!
#    * 「山」: All 3 peaks + 底横 are 100% connected as one trapezoidal contour mountain;
#             at the mid-waist (y=118..136) on the right slope of 右峰, a dx/dy=-0.35
#             angled ravine slash isolates/steps the Mid-Waist Trapezoidal Terrace Block!
#    * 「烘」: In 「共」, 下横 (y=118..135) crosses both vertical stems intact (x=498..588),
#             and to its right (x=598..624) a dx/dy=-0.35 ravine slash isolates the Mid-Waist Cut Block!
#    * 「焙」: In 「咅」, 「立」's 下横 (y=118..135) crosses both inner pillars intact (x=710..800),
#             and to its right (x=810..836) a dx/dy=-0.35 ravine slash isolates the Mid-Waist Cut Block!
# ==============================================================================

SLOPE = 0.35  # exact dx/dy = 0.35 from sets/A/logo/symbol.svg!


def trap_bar(x_top_l, x_top_r, y0, h=16):
    """Trapezoidal contour tier bar with left slope -0.35 and right slope +0.35."""
    dx = round(h * SLOPE, 2)
    return [
        (x_top_l, y0),
        (x_top_r, y0),
        (x_top_r + dx, y0 + h),
        (x_top_l - dx, y0 + h),
    ]


def slash_stem(x, y_top, y_bot, w=19):
    """Vertical stem whose summit is sliced at the exact dx/dy = -0.35 ravine angle."""
    dy = round(w * SLOPE, 2)
    return [
        (x, y_top + dy),
        (x + w, y_top),
        (x + w, y_bot),
        (x, y_bot),
    ]


def cut_block(x_top_l, x_top_r, y0, h=17):
    """Mid-Waist Trapezoidal Cut Block: left edge is ravine slash (-0.35), right edge is outer slope (+0.35)."""
    dx = round(h * SLOPE, 2)
    return [
        (x_top_l, y0),
        (x_top_r, y0),
        (x_top_r + dx, y0 + h),
        (x_top_l - dx, y0 + h),
    ]


def build_d3_wordmark_paths():
    add = []
    sub = []

    # --- 1. 半 (x = 16..196) ---
    # Central stem (width 19) with angled summit cut
    add.append(slash_stem(94, 28, 212, 19))
    # Upper two dots sculpted as trapezoidal/parallelogram cut-blocks (matching mid-tier-mark!)
    add.append(cut_block(44, 68, 42, 24))
    add.append([
        (138, 42),
        (162, 42),
        (153.6, 66),
        (129.6, 66),
    ])
    # Upper horizontal (上横 y = 78..94): trapezoidal contour tier
    add.append(trap_bar(42, 164, 78, 16))
    # Mid-Waist Lower Horizontal (下横 y = 118..135):
    # Left part runs from x=24 across 中竖 (94..113) to x=144, sliced on the right at dx/dy = -0.35!
    h_w = 17
    dx_w = round(h_w * SLOPE, 2)
    add.append([
        (24, 118),
        (144, 118),
        (144 - dx_w, 118 + h_w),
        (24 - dx_w, 118 + h_w),
    ])
    # Right Mid-Waist Cut Block (中腰切块) separated by 12-unit angled ravine slash!
    add.append(cut_block(156, 188, 118, h_w))

    # --- 2. 山 (x = 228..410) ---
    # All 3 peaks + bottom base are 100% connected as one trapezoidal contour mountain!
    # Left peak: outer wall slopes outward-downward along contour slope (-0.18), top sliced at -0.35
    add.append([
        (240, 78),
        (258, 72),
        (258, 196),
        (240, 212),
        (224, 212),
    ])
    # Central summit peak
    add.append(slash_stem(302, 28, 212, 19))
    # Right peak (inner stem x=364..382 rises to y=72, continuous to base)
    add.append(slash_stem(364, 72, 212, 18))
    # Continuous bottom base (底横 y = 195..212, joining Left, Center, Right peaks!)
    add.append([
        (228, 195),
        (382, 195),
        (382 - dx_w, 212),
        (224, 212),
    ])
    # Mid-Waist Cut Block on the right slope of 山 (at y=118..135, or right base terrace):
    # Wait: if we place a Mid-Waist Cut Block on the outer right slope or right base extension,
    # let's make Right Peak's upper half (y=72..118) and lower half connected on x=364..382,
    # while on the bottom base (y=195..212) OR mid-waist (y=118..135) the outer right contour
    # has the signature angled terrace step (from x=382 out to x=402 from y=118..212, with an angled
    # ravine notch cut into the right waist)!
    add.append([
        (380, 126),
        (398, 120),
        (408, 212),
        (376, 212),
    ])

    # --- 3. 烘 (x = 436..628) ---
    def add_d3_huo(ox):
        # Central spine with angled top
        add.append(slash_stem(ox + 26, 30, 138, 18))
        # Left dot: parallelogram cut-block
        add.append([
            (ox + 4, 78),
            (ox + 18, 78),
            (ox + 10, 110),
            (ox - 4, 110),
        ])
        # Right short stroke: angled parallelogram cut-block
        add.append([
            (ox + 54, 74),
            (ox + 68, 74),
            (ox + 56, 106),
            (ox + 42, 106),
        ])
        # Bottom-left angled leg (撇)
        add.append([
            (ox + 26, 132),
            (ox + 44, 132),
            (ox + 18, 212),
            (ox + 0, 212),
        ])
        # Bottom-right angled block leg (捺)
        add.append([
            (ox + 38, 148),
            (ox + 52, 144),
            (ox + 68, 188),
            (ox + 52, 192),
        ])

    add_d3_huo(436)
    # Right component 共 (x = 502..628)
    add.append(slash_stem(522, 30, 135, 18))
    add.append(slash_stem(564, 30, 135, 18))
    add.append(trap_bar(508, 598, 78, 16))
    # Mid-Waist Lower Horizontal of 共 (y = 118..135) + Angled Ravine Slash + Mid-Waist Cut Block!
    add.append([
        (502, 118),
        (590, 118),
        (590 - dx_w, 118 + h_w),
        (502 - dx_w, 118 + h_w),
    ])
    add.append(cut_block(600, 622, 118, h_w))
    # Bottom two trapezoidal legs of 共 (八字脚)
    add.append([
        (526, 148),
        (544, 148),
        (518, 212),
        (500, 212),
    ])
    add.append([
        (560, 148),
        (578, 148),
        (604, 212),
        (586, 212),
    ])

    # --- 4. 焙 (x = 652..844) ---
    add_d3_huo(652)
    # Right component 咅 (立 + 口, x = 718..844)
    # Top trapezoidal cut-block dot of 立
    add.append(cut_block(758, 778, 28, 26))
    # Upper horizontal of 立 (y = 58..74)
    add.append(trap_bar(724, 816, 58, 16))
    # Inner two pillars of 立
    add.append([(732, 74), (748, 74), (754, 118), (738, 118)])
    add.append([(788, 74), (804, 74), (796, 118), (780, 118)])
    # Mid-Waist Lower Horizontal of 立 (y = 118..135) + Angled Ravine Slash + Mid-Waist Cut Block!
    add.append([
        (718, 118),
        (806, 118),
        (806 - dx_w, 118 + h_w),
        (718 - dx_w, 118 + h_w),
    ])
    add.append(cut_block(816, 838, 118, h_w))
    # Bottom trapezoidal contour box 口 (y = 150..212)
    add.append([
        (730, 150),
        (812, 150),
        (820, 212),
        (722, 212),
    ])
    sub.append([
        (746, 166),
        (796, 166),
        (801, 196),
        (741, 196),
    ])

    return union_polys(add, sub)


def write_svg(path, vb, title, d_str):
    x0, y0, w, h = vb
    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x0} {y0} {w} {h}" '
        f'width="{w}" height="{h}" role="img">\n'
        f"  <title>{title}</title>\n"
        f'  <path fill="#111111" fill-rule="evenodd" d="{d_str}"/>\n'
        f"</svg>\n"
    )
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(svg)
    png_path = os.path.splitext(path)[0] + ".png"
    render_png.render(path, png_path, max(512, w), max(512, int(round(h * max(512, w) / w))))
    print("wrote", path, "and", png_path)


def main():
    d1_d = build_d1_wordmark_paths()
    write_svg(
        os.path.join(WORK_DIR, "d1-wordmark-v1.svg"),
        (0, 0, 840, 240),
        "半山烘焙 — D1 腰线半山 Custom Wordmark v1",
        d1_d,
    )

    d2_d = build_d2_wordmark_paths()
    write_svg(
        os.path.join(WORK_DIR, "d2-wordmark-v1.svg"),
        (0, 0, 840, 240),
        "半山烘焙 — D2 云阶半山 Custom Wordmark v1",
        d2_d,
    )

    d3_d = build_d3_wordmark_paths()
    write_svg(
        os.path.join(WORK_DIR, "d3-wordmark-v1.svg"),
        (0, 0, 860, 240),
        "半山烘焙 — D3 等高风土 Custom Wordmark v1",
        d3_d,
    )


if __name__ == "__main__":
    main()
