#!/usr/bin/env python3
"""Build Round 2 (v2) SVGs and PNGs for B1-r1 (D1 腰线半山, D2 云阶半山, D3 等高风土).

Incorporates visual inspection fixes from Round 1 (v1):
1. D1 (腰线半山):
   - Restores pure 90° flat architectural terminals on all vertical and horizontal bars
     (removing the spiky 45° tips from v1), keeping 45° geometry strictly for the
     signature rectangular block dots (丷) and angled legs.
   - Fixes 「山」 by eliminating both B0's 2-row break (出/fence misreading) and v1's
     side bumps: 「山」 is 100% continuous and orthogonal, with its three peaks locked
     1-to-1 onto the three horizontal datum lines of 「半」:
       * Left Peak top at y = 122 (collinear with 「半」's Mid-Slope Waist Bar 下横 y = 122..140!)
       * Central Peak top at y = 32 (collinear with 「半」's Summit y = 32!)
       * Right Peak top at y = 78 (collinear with 「半」's Upper Bar 上横 y = 78..96!)
   - Unifies all 4 characters (半, 山, 烘, 焙) with 20-unit vertical stems, 18-unit
     horizontal bars, 45° rectangular dot blocks, and a locked y = 122..140 Mid-Slope Waist Line.
2. D2 (云阶半山):
   - Distinct typographic contrast: 15-unit sleek vertical stems paired with bold 17-unit
     chord-beveled Horizontal Cloud-Strata bars, smooth R=26..28 circular-arc bowl bases
     (matching the R=104 circular bowl of concept-c-v4.svg), and graceful curved 撇/捺 legs.
   - Removes fence-post spikes from vertical stems of 烘/焙; keeps subtle 45° twin-peak
     ridge bevels only on the main summits of 半 and 山.
   - Connects 火's right leg (捺) smoothly to the spine and makes 火's side dots horizontal
     cloud-strata bars.
   - Maintains the 12-unit Horizontal Cloud-Slice (水平切层缝) across all 4 characters.
3. D3 (等高风土):
   - Fixes 「山」's right stem so it is a balanced 18-unit contour stem (not a 32-unit club)
     with a crisp 8-unit dx/dy = -0.35 stepped contour offset at the y = 118 mid-waist.
   - Connects 火's right leg (捺) cleanly to the spine in 烘 and 焙.
   - All 4 characters share dx/dy = -0.35 (~70.7°) angled terminals, trapezoidal contour
     bars, parallelogram dot blocks, and the signature Mid-Waist Trapezoidal Cut Block (中腰切块).
4. Technical notes from docs/wordmark.md:
   - Uses skia-pathops boolean union + difference so overlapping CJK strokes never create
     white holes under fill-rule="evenodd".
   - Computes lockup icon height from actual Chinese ink height (180 units), NOT Latin cap-height.
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
    parts = [f"M {pts[0][0]:.2f} {pts[0][1]:.2f}"]
    for x, y in pts[1:]:
        parts.append(f"L {x:.2f} {y:.2f}")
    parts.append("Z")
    return " ".join(parts)


def rect_pts(x, y, w, h):
    return [(x, y), (x + w, y), (x + w, y + h), (x, y + h)]


def svg_to_skia_path(d_str):
    p = pathops.Path()
    pen = p.getPen()
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


def load_path_d_and_bbox(svg_path):
    raw = open(svg_path, encoding="utf-8").read()
    m_d = re.search(r'\bd="([^"]+)"', raw)
    d = m_d.group(1)
    p = svg_to_skia_path(d)
    p = pathops.simplify(p, fix_winding=True)
    b = p.bounds
    return p, b  # (x0, y0, x1, y1)


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
# DIRECTION 1: 腰线半山 (D1 造字路线) — Pure Orthogonal Architectural Grid
# ==============================================================================

def build_d1_wordmark_d():
    """4-character custom architectural wordmark 半山烘焙 (viewBox 0 0 848 240, ink y=32..212)."""
    add = []
    sub = []

    # --- 1. 半 (x = 16..188, width = 172, center = 102) ---
    # Central vertical stem (width 20, flat 90° top & bottom)
    add.append(rect_pts(92, 32, 20, 180))
    # Two 45° rectangular block dots (exact 45° rotated rectangles: 14*sqrt(2)x22*sqrt(2))
    add.append([(36, 52), (50, 38), (74, 62), (60, 76)])
    add.append([(168, 52), (154, 38), (130, 62), (144, 76)])
    # Upper horizontal bar (上横 y = 80..98, height 18)
    add.append(rect_pts(32, 80, 140, 18))
    # Mid-Slope Waist Horizon Bar (下横 y = 122..140, height 18, full width 172)
    add.append(rect_pts(16, 122, 172, 18))

    # --- 2. 山 (x = 224..396, width = 172, center = 310) ---
    # Unbroken 3-peak architectural 山 whose 3 peaks lock 1-to-1 onto 半's 3 horizontal datum lines:
    # - Left Peak (半山平顶峰): top at y = 122 (collinear with 半's 下横 Mid-Slope Waist Line y=122!)
    # - Central Peak (主峰): top at y = 32 (collinear with 半's Summit y=32!)
    # - Right Peak (高坡峰): top at y = 80 (collinear with 半's 上横 y=80!)
    # - Bottom Base (底横): y = 194..212 (height 18), connecting all 3 peaks continuously!
    add.append(rect_pts(224, 122, 20, 90))   # Left peak: y = 122..212 (90 units tall = half mountain!)
    add.append(rect_pts(300, 32, 20, 180))   # Central peak: y = 32..212 (180 units tall = full mountain!)
    add.append(rect_pts(376, 80, 20, 132))   # Right peak: y = 80..212 (132 units tall = 3/4 mountain!)
    add.append(rect_pts(224, 194, 172, 18))  # Bottom base: x = 224..396, y = 194..212

    # --- Helper for D1 architectural 火 radical (width 68) ---
    def add_d1_huo(ox):
        # Upper vertical spine (x = ox+26..ox+46, width 20) from y = 32 down to waist y = 140
        add.append(rect_pts(ox + 26, 32, 20, 108))
        # Left side stroke: vertical architectural bar at Mid-Upper zone (y = 80..122, locked between 上横 y=80 and 腰线 y=122!)
        add.append(rect_pts(ox + 0, 80, 16, 42))
        # Right side stroke: 45° rectangular block (matching 半's 丷 dots!)
        add.append([(ox + 70, 88), (ox + 58, 76), (ox + 42, 92), (ox + 54, 104)])
        # Bottom-left architectural leg (撇): from waist (ox+26..46, 136) down-left to flat foot at y=212
        add.append([(ox + 26, 136), (ox + 46, 136), (ox + 20, 212), (ox + 0, 212)])
        # Bottom-right architectural leg (捺): connected cleanly to spine at (ox+38, 144) down-right to (ox+68, 196)
        add.append([(ox + 36, 152), (ox + 46, 140), (ox + 70, 184), (ox + 54, 194)])

    # --- 3. 烘 (x = 432..616) ---
    add_d1_huo(432)
    # Right component 共 (x = 502..616)
    # Two vertical pillars (width 19, flat 90° top at y = 32, descending to waist y = 140)
    add.append(rect_pts(522, 32, 19, 108))
    add.append(rect_pts(569, 32, 19, 108))
    # Upper horizontal of 共 (y = 80..98, height 18 — locked on y=80 datum!)
    add.append(rect_pts(506, 80, 104, 18))
    # Mid-Slope Waist Bar of 共 (y = 122..140, height 18 — locked on y=122 Mid-Slope Waist datum!)
    add.append(rect_pts(498, 122, 118, 18))
    # Bottom two architectural legs of 共 (flat horizontal tops at y=150, flat horizontal feet at y=212)
    add.append([(524, 150), (544, 150), (518, 212), (498, 212)])
    add.append([(566, 150), (586, 150), (612, 212), (592, 212)])

    # --- 4. 焙 (x = 648..832) ---
    add_d1_huo(648)
    # Right component 咅 (立 + 口, x = 716..832)
    # Top vertical pillar of 立 (x = 764..784, y = 32..60)
    add.append(rect_pts(764, 32, 20, 28))
    # Upper horizontal of 立 (x = 720..828, y = 58..76, height 18)
    add.append(rect_pts(720, 58, 108, 18))
    # Two inner architectural pillars of 立 (y = 76..122)
    add.append([(734, 76), (752, 76), (758, 122), (740, 122)])
    add.append([(796, 76), (814, 76), (808, 122), (790, 122)])
    # Mid-Slope Waist Bar of 立 (x = 714..832, y = 122..140, height 18 — locked on y=122 Mid-Slope Waist datum!)
    add.append(rect_pts(714, 122, 118, 18))
    # Bottom architectural box 口 (x = 726..822, y = 152..212)
    add.append(rect_pts(726, 152, 96, 60))
    sub.append(rect_pts(745, 169, 58, 26))

    return union_polys(add, sub)


def build_d1_badge_2char_d():
    """2-character square badge 半山 for medium-small sizes (28-47px) on 256x256 canvas."""
    add = []
    # 半 (x = 16..114, y = 32..224)
    add.append(rect_pts(56, 32, 18, 192))
    add.append([(20, 52), (32, 40), (50, 58), (38, 70)])
    add.append([(110, 52), (98, 40), (80, 58), (92, 70)])
    add.append(rect_pts(22, 82, 86, 16))
    add.append(rect_pts(16, 124, 98, 16))  # Mid-slope waist line y=124..140

    # 山 (x = 136..240, y = 32..224) — Unbroken 3-peak architectural 山 locked to 半's 3 datum lines!
    add.append(rect_pts(136, 124, 18, 100))  # Left peak: top at y=124 (locked to 半's waist line!)
    add.append(rect_pts(179, 32, 18, 192))   # Center peak: top at y=32 (summit)
    add.append(rect_pts(222, 82, 18, 142))   # Right peak: top at y=82 (locked to 半's upper bar!)
    add.append(rect_pts(136, 206, 104, 18))  # Continuous bottom base
    return union_polys(add)


def build_d1_small_1char_d():
    """16px (<28px) dedicated small-size mark for D1: Single character 「半」 with bold 28-unit
    strokes, 32-unit counters, and an accentuated Mid-Slope Waist Horizon bar on 256x256."""
    add = []
    # Central vertical stem (width 28 = 1.75px at 16px, centered at x=128)
    add.append(rect_pts(114, 16, 28, 224))
    # Upper-left and upper-right 45° slope blocks (big, clear, 26 units thick)
    add.append([(36, 52), (56, 32), (92, 68), (72, 88)])
    add.append([(220, 52), (200, 32), (164, 68), (184, 88)])
    # Upper horizontal bar (y = 96..122, height 26)
    add.append(rect_pts(44, 96, 168, 26))
    # Mid-Slope Waist Horizon Bar (y = 152..180, height 28, full width x = 16..240, gap = 30 units = 1.88px at 16px!)
    add.append(rect_pts(16, 152, 224, 28))
    return union_polys(add)


# ==============================================================================
# DIRECTION 2: 云阶半山 (D2 图标路线) — Cloud-Strata & Curved Bowl Wordmark
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
    Deepens the twin-peak valley from 18 to 36 units (2.25px at 16px) so the twin peaks
    never flatten into a pixel staircase, and widens the horizontal cloud-slices to 28 units (1.75px)."""
    return (
        "M 22 104 L 98 20 L 142 64 L 172 34 L 234 104 H 22 Z "
        "M 21 132 H 235 A 108 108 0 0 1 222 172 H 34 A 108 108 0 0 1 21 132 Z "
        "M 52 200 H 204 A 108 108 0 0 1 52 200 Z"
    )


def build_d2_wordmark_d():
    """4-character custom Cloud-Strata wordmark 半山烘焙 (viewBox 0 0 848 240, ink y=30..212).
    Shared rule with D2 icon:
    - Sleek 15-unit vertical stems paired with bold 17-unit chord-beveled Horizontal Cloud-Strata bars
    - 12-unit Horizontal Cloud-Slice (水平切层缝) detaching the horizontal layer transition in all 4 chars
    - Smooth R=26..28 circular-arc bowl bases (圆弧底托) and curved 撇/捺 sweeps
    - Asymmetric 45° mountain-peak bevels on main summits of 半 and 山
    """
    add = []
    sub = []

    def chord_bar(x0, x1, y0, h=17, inset=7):
        """Horizontal cloud-terrace band with circular-chord sloped ends matching the D2 icon."""
        return [
            (x0, y0),
            (x1, y0),
            (x1 - inset, y0 + h),
            (x0 + inset, y0 + h),
        ]

    # --- 1. 半 (x = 16..188) ---
    # Upper central stem (width 16, x=94..110) with 45° mountain-peak top (y=30..108),
    # stopping at y=108 for the 12-unit Horizontal Cloud-Slice (y=108..120)!
    add.append([(94, 42), (106, 30), (110, 34), (110, 108), (94, 108)])
    # Upper two dots sculpted as horizontal cloud-strata bars (horizontal top & bottom, chord-cut outer ends!)
    add.append(chord_bar(34, 78, 48, 15, 5))
    add.append(chord_bar(126, 170, 48, 15, 5))
    # Upper horizontal contour band (上横 y = 77..94, height 17)
    add.append(chord_bar(30, 174, 77, 17, 6))
    # [Horizontal Cloud-Slice Gap at y = 108..120 (12 units)]
    # Lower horizontal contour band (下横 y = 120..137, height 17)
    add.append(chord_bar(16, 188, 120, 17, 7))
    # Lower central stem (y = 120..212) with smooth R=16 curved-bowl bottom hook
    add.append(
        "M 94 120 L 110 120 L 110 196 Q 110 212 94 212 L 88 212 L 88 198 L 94 198 Z"
    )

    # --- 2. 山 (x = 224..396) ---
    # Continuous outer U-cradle (凵) with R=28 circular-arc bottom-left and bottom-right bowl corners!
    # Left stem (x=228..244, flat cloud-sliced top at y=76), Right stem (x=376..392, 45° secondary-peak top at y=60)
    add.append(
        "M 228 76 L 244 76 L 244 194 L 376 194 L 376 68 L 386 58 L 392 64 "
        "L 392 184 Q 392 211 365 211 L 255 211 Q 228 211 228 184 Z"
    )
    # Tall Central Peak (x=302..318, 45° main peak top at y=30), stopping at y=182
    # -> 12-unit Horizontal Cloud-Slice (y = 182..194) above the curved bottom bowl!
    add.append([(302, 42), (314, 30), (318, 34), (318, 182), (302, 182)])

    # --- Helper for D2 Cloud-Strata + Curved-Bowl 火 radical ---
    def add_d2_huo(ox):
        # Graceful central vertical-to-left-curve spine (竖撇, flat top at y=32, curving smoothly to ox+0 at y=212)
        add.append(
            f"M {ox + 27:.2f} 32 L {ox + 43:.2f} 32 L {ox + 43:.2f} 122 "
            f"Q {ox + 43:.2f} 174 {ox + 16:.2f} 212 L {ox + 0:.2f} 212 "
            f"Q {ox + 27:.2f} 170 {ox + 27:.2f} 120 Z"
        )
        # Connected curved right leg (捺, branching smoothly from spine at y=126 down to flat horizontal foot at y=196)
        add.append(
            f"M {ox + 34:.2f} 126 L {ox + 43:.2f} 126 "
            f"Q {ox + 52:.2f} 162 {ox + 68:.2f} 194 L {ox + 52:.2f} 194 "
            f"Q {ox + 38:.2f} 164 {ox + 34:.2f} 126 Z"
        )
        # Left & Right side dots sculpted as Horizontal Cloud-Strata Bars (y = 82..96, height 14)
        add.append(chord_bar(ox - 2, ox + 20, 82, 14, 3))
        add.append(chord_bar(ox + 49, ox + 71, 82, 14, 3))

    # --- 3. 烘 (x = 432..616) ---
    add_d2_huo(432)
    # Right component 共 (x = 500..616)
    # Upper two vertical pillars (width 15, flat tops at y=32, stopping at y=108 for the 12-unit Horizontal Cloud-Slice!)
    add.append(rect_pts(524, 32, 15, 76))
    add.append(rect_pts(571, 32, 15, 76))
    # Upper horizontal contour band (上横 y = 76..93, height 17)
    add.append(chord_bar(504, 606, 76, 17, 6))
    # [Horizontal Cloud-Slice Gap at y = 108..120 (12 units)]
    # Lower horizontal contour band (下横 y = 120..137, height 17)
    add.append(chord_bar(496, 616, 120, 17, 7))
    # Bottom two curved-bowl legs (八字底托, flat horizontal feet at y=211)
    add.append(
        "M 526 146 L 543 146 Q 535 186 514 211 L 496 211 Q 518 182 526 146 Z"
    )
    add.append(
        "M 567 146 L 584 146 Q 592 182 614 211 L 596 211 Q 575 186 567 146 Z"
    )

    # --- 4. 焙 (x = 648..832) ---
    add_d2_huo(648)
    # Right component 咅 (立 + 口, x = 714..832)
    # Top pillar of 立 (x=765..781, flat top at y=30..58) + 上横 (y=58..75, height 17)
    add.append(rect_pts(765, 30, 16, 30))
    add.append(chord_bar(720, 826, 58, 17, 6))
    # Two inner pillars of 立 descending from y=75 and stopping at y=108
    # -> 12-unit Horizontal Cloud-Slice (y = 108..120) above 立's 下横 (y = 120..137)!
    add.append([(736, 75), (751, 75), (756, 108), (741, 108)])
    add.append([(795, 75), (810, 75), (805, 108), (790, 108)])
    # [Horizontal Cloud-Slice Gap at y = 108..120 (12 units)]
    add.append(chord_bar(714, 832, 120, 17, 7))
    # Lower 口 (x=726..820, y=149..211) with R=26 circular-arc bottom-left and bottom-right bowl corners!
    add.append(
        "M 726 149 L 820 149 L 820 185 Q 820 211 794 211 L 752 211 Q 726 211 726 185 Z"
    )
    sub.append(
        "M 742 165 L 804 165 L 804 185 Q 804 195 794 195 L 752 195 Q 742 195 742 185 Z"
    )

    return union_polys(add, sub)


# ==============================================================================
# DIRECTION 3: 等高风土 (D3 图形路线) — Angled Slash & Mid-Waist Cut Block
# ==============================================================================

SLOPE = 0.35  # exact dx/dy = 0.35 from sets/A/logo/symbol.svg


def build_d3_symbol_d():
    """B0 Set A symbol (sets/A/logo/symbol.svg) scaled cleanly from 100x100 to 256x256 integer/2-dec canvas
    in pure monochrome black (#111111).
    Original 100x100 polygons:
      peak-tier:     32,12  68,12  75.7,34  24.3,34
      mid-tier-left: 21.5,42  54,42  46.3,64  13.8,64
      mid-tier-mark: 64,42  78.5,42  86.2,64  56.3,64
      base-tier:     11,72  89,72  95.3,90  4.7,90
    Scaled by 2.4x around center (50, 51) -> fits x=19..237, y=26..214 on 256x256.
    """
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
    """16px (<=24px) dedicated small-size icon for D3:
    Widens the horizontal tier gaps from 19.2 to 28 units (1.75px at 16px) and widens the
    angled ravine slash to 28 units so the 3 tiers + mid-waist cut block remain distinct at 16x16px."""
    polys = [
        [(72, 20), (184, 20), (202, 72), (54, 72)],          # Top tier (height 52)
        [(44, 100), (126, 100), (108, 156), (24, 156)],     # Mid-left tier (height 56)
        [(154, 100), (212, 100), (232, 156), (136, 156)],   # Mid-right cut block (gap = 28 units)
        [(16, 184), (240, 184), (252, 232), (4, 232)],      # Base tier (height 48)
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
    """4-character custom Contour-Slash wordmark 半山烘焙 (viewBox 0 0 860 240, ink y=28..212).
    Fixes from v1:
    - 「山」 right stem is now a balanced 18-unit stem with an 8-unit stepped contour offset at
      the y=118 mid-waist (upper right peak x=364..382, lower right slope x=372..390, joined
      continuously with a crisp dx/dy=-0.35 shoulder at y=118..135 — zero heavy club!).
    - 「火」 right leg (捺) connects cleanly into the central spine in both 烘 and 焙.
    """
    add = []
    sub = []
    h_w = 17
    dx_w = round(h_w * SLOPE, 2)

    # --- 1. 半 (x = 16..196) ---
    add.append(slash_stem(94, 28, 212, 19))
    add.append(cut_block(44, 68, 42, 24))
    add.append([(138, 42), (162, 42), (153.6, 66), (129.6, 66)])
    add.append(trap_bar(42, 164, 78, 16))
    # Mid-Waist Lower Horizontal (下横 y=118..135) + 12-unit angled ravine slash + Mid-Waist Cut Block!
    add.append([
        (24, 118),
        (144, 118),
        (144 - dx_w, 118 + h_w),
        (24 - dx_w, 118 + h_w),
    ])
    add.append(cut_block(156, 188, 118, h_w))

    # --- 2. 山 (x = 228..396) ---
    # Left peak: trapezoidal contour slope (top x=238..256 at y=72, bottom x=228..246 at y=212)
    add.append([
        (238, 78.3),
        (256, 72),
        (246, 212),
        (228, 212),
    ])
    # Central summit peak (x=301..320, y=28..212)
    add.append(slash_stem(301, 28, 212, 19))
    # Right peak with balanced 18-unit width and Mid-Waist Angled Step at y=118..135:
    # Upper segment (y=72..135, x=362..380) steps outward by 8 units at y=118 to lower segment (y=118..212, x=370..388)
    add.append(slash_stem(362, 72, 135, 18))
    add.append(slash_stem(370, 118, 212, 18))
    # Continuous bottom base (底横 y=195..212, x=228..388)
    add.append([
        (230, 195),
        (388, 195),
        (388, 212),
        (228, 212),
    ])

    # --- Helper for D3 Contour-Slash 火 radical ---
    def add_d3_huo(ox):
        add.append(slash_stem(ox + 26, 30, 140, 18))
        # Left dot: parallelogram cut-block
        add.append([(ox + 4, 78), (ox + 18, 78), (ox + 10, 110), (ox - 4, 110)])
        # Right short stroke: angled parallelogram cut-block
        add.append([(ox + 54, 74), (ox + 68, 74), (ox + 56, 106), (ox + 42, 106)])
        # Bottom-left angled leg (撇)
        add.append([(ox + 26, 132), (ox + 44, 132), (ox + 18, 212), (ox + 0, 212)])
        # Bottom-right angled leg (捺) — connected solidly to spine at (ox+34..44, 138)!
        add.append([(ox + 34, 138), (ox + 44, 134), (ox + 68, 190), (ox + 52, 194)])

    # --- 3. 烘 (x = 434..626) ---
    add_d3_huo(434)
    add.append(slash_stem(522, 30, 135, 18))
    add.append(slash_stem(564, 30, 135, 18))
    add.append(trap_bar(508, 598, 78, 16))
    # Mid-Waist Lower Horizontal of 共 + Angled Ravine Slash + Mid-Waist Cut Block
    add.append([
        (502, 118),
        (590, 118),
        (590 - dx_w, 118 + h_w),
        (502 - dx_w, 118 + h_w),
    ])
    add.append(cut_block(600, 622, 118, h_w))
    add.append([(526, 148), (544, 148), (518, 212), (500, 212)])
    add.append([(560, 148), (578, 148), (604, 212), (586, 212)])

    # --- 4. 焙 (x = 652..844) ---
    add_d3_huo(652)
    add.append(cut_block(758, 778, 28, 26))
    add.append(trap_bar(724, 816, 58, 16))
    add.append([(732, 74), (748, 74), (754, 118), (738, 118)])
    add.append([(788, 74), (804, 74), (796, 118), (780, 118)])
    # Mid-Waist Lower Horizontal of 立 + Angled Ravine Slash + Mid-Waist Cut Block
    add.append([
        (718, 118),
        (806, 118),
        (806 - dx_w, 118 + h_w),
        (718 - dx_w, 118 + h_w),
    ])
    add.append(cut_block(816, 838, 118, h_w))
    # Bottom trapezoidal contour box 口
    add.append([(730, 150), (812, 150), (820, 212), (722, 212)])
    sub.append([(746, 166), (796, 166), (801, 196), (741, 196)])

    return union_polys(add, sub)


# ==============================================================================
# LOCKUP BUILDER (Fixes BrandDesign CJK cap-height undersizing bug!)
# ==============================================================================

def build_bilingual_wordmark_d(zh_d, en_svg_path, target_en_h=30.0, gap_y=28.0):
    """Combine a custom 4-char Chinese wordmark path with an outlined English BANSHAN ROASTERS
    subtitle centered underneath it."""
    zh_p = svg_to_skia_path(zh_d)
    zh_p = pathops.simplify(zh_p, fix_winding=True)
    zx0, zy0, zx1, zy1 = zh_p.bounds
    zh_w = zx1 - zx0
    zh_cx = (zx0 + zx1) / 2.0

    en_p, (ex0, ey0, ex1, ey1) = load_path_d_and_bbox(en_svg_path)
    en_h = ey1 - ey0
    scale = target_en_h / en_h
    en_w_scaled = (ex1 - ex0) * scale
    tx = zh_cx - ((ex0 + ex1) / 2.0) * scale
    ty = zy1 + gap_y - ey0 * scale
    en_p_trans = transform_skia_path(en_p, scale, scale, tx, ty)

    combined = pathops.Path()
    combined.addPath(zh_p)
    combined.addPath(en_p_trans)
    combined = pathops.simplify(combined, fix_winding=True)
    return skia_to_svg_d(combined), combined.bounds, (zx0, zy0, zx1, zy1)


def build_symbol_plus_bilingual_lockup_d(sym_d, zh_d, en_svg_path, sym_to_zh_ink_ratio=1.18, gap_x=56.0):
    """Build horizontal lockup: Symbol on left + (Chinese wordmark + English subtitle) on right.
    CRITICAL FIX per docs/wordmark.md: Symbol height is scaled relative to actual Chinese ink height
    (zy1 - zy0 = 180 units), NOT Latin cap-height (100 units), avoiding the 22% undersizing bug!
    """
    bilingual_d, (bx0, by0, bx1, by1), (zx0, zy0, zx1, zy1) = build_bilingual_wordmark_d(
        zh_d, en_svg_path, target_en_h=30.0, gap_y=28.0
    )
    zh_ink_h = zy1 - zy0
    # Target symbol ink height = sym_to_zh_ink_ratio * zh_ink_h (approx equal to total bilingual height)
    sym_p = svg_to_skia_path(sym_d)
    sym_p = pathops.simplify(sym_p, fix_winding=True)
    sx0, sy0, sx1, sy1 = sym_p.bounds
    sym_h = sy1 - sy0
    target_sym_h = sym_to_zh_ink_ratio * zh_ink_h
    s_scale = target_sym_h / sym_h

    # Center symbol vertically against the full bilingual block (by0..by1)
    b_cy = (by0 + by1) / 2.0
    s_cy = (sy0 + sy1) / 2.0
    ty = b_cy - s_cy * s_scale
    tx = 20.0 - sx0 * s_scale
    sym_trans = transform_skia_path(sym_p, s_scale, s_scale, tx, ty)
    nsx0, nsy0, nsx1, nsy1 = sym_trans.bounds

    # Shift bilingual wordmark to start at nsx1 + gap_x
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
        # Shift path so top-left is at (pad, pad) and viewBox is integer (0, 0, W, H)
        w = int(math.ceil((x1 - x0) + 2 * pad))
        h = int(math.ceil((y1 - y0) + 2 * pad))
        # Make width and height even integers
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
        f"  <title>{title}</title>\n"
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
    en_serif = os.path.join(WORK_DIR, "en-serif.svg")

    # --- D1: 腰线半山 ---
    d1_wm = build_d1_wordmark_d()
    write_tight_svg(os.path.join(OUT_DIR, "d1-wordmark.svg"), "半山烘焙 — D1 腰线半山 主字标", d1_wm, pad=20)
    d1_badge = build_d1_badge_2char_d()
    write_tight_svg(os.path.join(OUT_DIR, "d1-badge-2char.svg"), "半山 — D1 腰线半山 双字简标 (28-47px)", d1_badge, square_vb=256)
    d1_small = build_d1_small_1char_d()
    write_tight_svg(os.path.join(OUT_DIR, "d1-small.svg"), "半 — D1 腰线半山 小尺寸单字版 (<28px / 16px)", d1_small, square_vb=256)
    d1_lock, _, _ = build_bilingual_wordmark_d(d1_wm, en_grotesk, target_en_h=28.0, gap_y=28.0)
    write_tight_svg(os.path.join(OUT_DIR, "d1-lockup.svg"), "半山烘焙 BANSHAN ROASTERS — D1 腰线半山 中英锁定组合", d1_lock, pad=20)

    # --- D2: 云阶半山 ---
    d2_sym = build_d2_symbol_d()
    write_tight_svg(os.path.join(OUT_DIR, "d2-symbol.svg"), "半山烘焙 — D2 云阶半山 图标", d2_sym, square_vb=256)
    d2_wm = build_d2_wordmark_d()
    write_tight_svg(os.path.join(OUT_DIR, "d2-wordmark.svg"), "半山烘焙 — D2 云阶半山 主字标", d2_wm, pad=20)
    d2_small = build_d2_small_d()
    write_tight_svg(os.path.join(OUT_DIR, "d2-small.svg"), "半山烘焙 — D2 云阶半山 小尺寸图标 (<=24px / 16px)", d2_small, square_vb=256)
    d2_lock, _ = build_symbol_plus_bilingual_lockup_d(d2_sym, d2_wm, en_sans, sym_to_zh_ink_ratio=1.18, gap_x=52.0)
    write_tight_svg(os.path.join(OUT_DIR, "d2-lockup.svg"), "半山烘焙 BANSHAN ROASTERS — D2 云阶半山 中英锁定组合", d2_lock, pad=20)

    # --- D3: 等高风土 ---
    d3_sym = build_d3_symbol_d()
    write_tight_svg(os.path.join(OUT_DIR, "d3-symbol.svg"), "半山烘焙 — D3 等高风土 图标 (黑白)", d3_sym, square_vb=256)
    d3_wm = build_d3_wordmark_d()
    write_tight_svg(os.path.join(OUT_DIR, "d3-wordmark.svg"), "半山烘焙 — D3 等高风土 主字标", d3_wm, pad=20)
    d3_small = build_d3_small_d()
    write_tight_svg(os.path.join(OUT_DIR, "d3-small.svg"), "半山烘焙 — D3 等高风土 小尺寸图标 (<=24px / 16px)", d3_small, square_vb=256)
    d3_lock, _ = build_symbol_plus_bilingual_lockup_d(d3_sym, d3_wm, en_sans, sym_to_zh_ink_ratio=1.18, gap_x=52.0)
    write_tight_svg(os.path.join(OUT_DIR, "d3-lockup.svg"), "半山烘焙 BANSHAN ROASTERS — D3 等高风土 中英锁定组合", d3_lock, pad=20)


if __name__ == "__main__":
    main()
