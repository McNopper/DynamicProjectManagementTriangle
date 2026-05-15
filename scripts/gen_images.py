import os

import cairosvg

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(os.path.dirname(SCRIPT_DIR), "figures")

W, H = 340, 330
R = 34
STROKE_W = 2.5

# Padding from SVG edge = 10px; minimum cx = R + stroke/2 + padding = 34+1.25+10 = ~46
# Maximum cx = W - 46 = 294

UP_TOP    = (170, 56)
UP_BOT_L  = (46,  256)
UP_BOT_R  = (294, 256)

INV_TOP_L = (46,  56)
INV_TOP_R = (294, 56)
INV_BOT   = (170, 256)

TOP_LABEL_Y = 12
BOT_LABEL_Y = 310

# Centroids
UP_CX  = (UP_TOP[0]    + UP_BOT_L[0]  + UP_BOT_R[0])  // 3   # 170
UP_CY  = (UP_TOP[1]    + UP_BOT_L[1]  + UP_BOT_R[1])  // 3   # 189
INV_CX = (INV_TOP_L[0] + INV_TOP_R[0] + INV_BOT[0])   // 3   # 170
INV_CY = (INV_TOP_L[1] + INV_TOP_R[1] + INV_BOT[1])   // 3   # 122

FIXED_FILL,  FIXED_STROKE  = "#1e3a8a", "#3b82f6"
VAR_FILL,    VAR_STROKE    = "#14532d", "#22c55e"
NEUT_FILL,   NEUT_STROKE   = "#374151", "#6b7280"
EDGE_COLOR   = "#6b7280"
WHITE        = "#ffffff"
FIXED_LABEL_COLOR = "#3b82f6"
VAR_LABEL_COLOR   = "#22c55e"
INVALID_FILL,    INVALID_STROKE    = "#7f1d1d", "#ef4444"   # red = not viable
INVALID_LABEL_COLOR = "#ef4444"
CENTER_COLOR      = "#9ca3af"

def node(cx, cy, fill, stroke, label):
    return (
        f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="{fill}" stroke="{stroke}" stroke-width="{STROKE_W}"/>'
        f'<text x="{cx}" y="{cy}" text-anchor="middle" dominant-baseline="middle" '
        f'font-family="Arial,Helvetica,sans-serif" font-size="12" font-weight="bold" fill="{WHITE}">{label}</text>'
    )

def center_label(cx, cy, text):
    return (
        f'<text x="{cx}" y="{cy}" text-anchor="middle" dominant-baseline="middle" '
        f'font-family="Arial,Helvetica,sans-serif" font-size="11" font-style="italic" '
        f'fill="{CENTER_COLOR}">{text}</text>'
    )

def edge(x1, y1, x2, y2):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{EDGE_COLOR}" stroke-width="{STROKE_W}"/>'

def band_label(text, y, color):
    return (
        f'<text x="{W//2}" y="{y}" text-anchor="middle" dominant-baseline="middle" '
        f'font-family="Arial,Helvetica,sans-serif" font-size="12" font-weight="bold" '
        f'letter-spacing="1" fill="{color}">{text}</text>'
    )

def svg(nodes_data, top_label=None, bot_label=None, inner_cx=UP_CX, inner_cy=UP_CY, inner_text="Quality"):
    pts = [(d[0], d[1]) for d in nodes_data]
    parts = []
    if top_label:
        parts.append(band_label(top_label, TOP_LABEL_Y, VAR_LABEL_COLOR))
    parts += [edge(*pts[0], *pts[1]), edge(*pts[1], *pts[2]), edge(*pts[2], *pts[0])]
    parts.append(center_label(inner_cx, inner_cy, inner_text))
    parts += [node(*d) for d in nodes_data]
    if bot_label:
        parts.append(band_label(bot_label, BOT_LABEL_Y, FIXED_LABEL_COLOR))
    content = "\n  ".join(parts)
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">\n'
        f'  {content}\n</svg>\n'
    )

def svg_line(labels, fill, stroke, label_color, caption):
    CY = H // 2
    xs = [46, W // 2, 294]
    parts = [
        band_label(caption, TOP_LABEL_Y, label_color),
        f'<line x1="{xs[0]}" y1="{CY}" x2="{xs[2]}" y2="{CY}" stroke="{EDGE_COLOR}" stroke-width="{STROKE_W}"/>',
    ]
    for x, lbl in zip(xs, labels):
        parts.append(node(x, CY, fill, stroke, lbl))
    content = "\n  ".join(parts)
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">\n'
        f'  {content}\n</svg>\n'
    )

def F(pos, label): return (*pos, FIXED_FILL, FIXED_STROKE, label)
def V(pos, label): return (*pos, VAR_FILL,   VAR_STROKE,   label)
def N(pos, label): return (*pos, NEUT_FILL,  NEUT_STROKE,  label)

os.makedirs(OUT_DIR, exist_ok=True)

files = {
    "classic": svg(
        [N(UP_TOP,"Scope"), N(UP_BOT_L,"Time"), N(UP_BOT_R,"Cost")],
        inner_cx=UP_CX, inner_cy=UP_CY, inner_text="Quality"
    ),
    "perm1_FFV": svg(
        [V(UP_TOP,"Cost"), F(UP_BOT_L,"Scope"), F(UP_BOT_R,"Time")],
        top_label="Variable", bot_label="Fixed",
        inner_cx=UP_CX, inner_cy=UP_CY
    ),
    "perm2_FVF": svg(
        [V(UP_TOP,"Time"), F(UP_BOT_L,"Scope"), F(UP_BOT_R,"Cost")],
        top_label="Variable", bot_label="Fixed",
        inner_cx=UP_CX, inner_cy=UP_CY
    ),
    "perm3_VFF": svg(
        [V(UP_TOP,"Scope"), F(UP_BOT_L,"Time"), F(UP_BOT_R,"Cost")],
        top_label="Variable", bot_label="Fixed",
        inner_cx=UP_CX, inner_cy=UP_CY
    ),
    "perm4_FVV": svg(
        [V(INV_TOP_L,"Time"), V(INV_TOP_R,"Cost"), F(INV_BOT,"Scope")],
        top_label="Variable", bot_label="Fixed",
        inner_cx=INV_CX, inner_cy=INV_CY
    ),
    "perm5_VFV": svg(
        [V(INV_TOP_L,"Scope"), V(INV_TOP_R,"Cost"), F(INV_BOT,"Time")],
        top_label="Variable", bot_label="Fixed",
        inner_cx=INV_CX, inner_cy=INV_CY
    ),
    "perm6_VVF": svg(
        [V(INV_TOP_L,"Scope"), V(INV_TOP_R,"Time"), F(INV_BOT,"Cost")],
        top_label="Variable", bot_label="Fixed",
        inner_cx=INV_CX, inner_cy=INV_CY
    ),
    "degen_FFF": svg_line(
        ["Scope","Time","Cost"],
        INVALID_FILL, INVALID_STROKE, INVALID_LABEL_COLOR, "All Fixed — Not Viable"
    ),
    "degen_VVV": svg_line(
        ["Scope","Time","Cost"],
        INVALID_FILL, INVALID_STROKE, INVALID_LABEL_COLOR, "All Variable — Not Viable"
    ),
}

for name, content in files.items():
    svg_path = os.path.join(OUT_DIR, f"{name}.svg")
    pdf_path = os.path.join(OUT_DIR, f"{name}.pdf")
    with open(svg_path, "w", encoding="utf-8") as fh:
        fh.write(content)
    print(f"wrote {svg_path}")
    cairosvg.svg2pdf(bytestring=content.encode("utf-8"), write_to=pdf_path)
    print(f"wrote {pdf_path}")

# Verify no clipping
print("\n--- Clipping check ---")
for name, pts in {
    "UP_TOP": UP_TOP, "UP_BOT_L": UP_BOT_L, "UP_BOT_R": UP_BOT_R,
    "INV_TOP_L": INV_TOP_L, "INV_TOP_R": INV_TOP_R, "INV_BOT": INV_BOT,
}.items():
    cx, cy = pts
    left = cx - R - STROKE_W/2
    right = cx + R + STROKE_W/2
    top_ = cy - R - STROKE_W/2
    bot_ = cy + R + STROKE_W/2
    ok = left >= 0 and right <= W and top_ >= TOP_LABEL_Y+8 and bot_ <= BOT_LABEL_Y-8
    print(f"{name}: x=[{left:.1f},{right:.1f}] y=[{top_:.1f},{bot_:.1f}] {'OK' if ok else 'CLIPPED!'}")
print(f"Canvas: {W}x{H}, BOT_LABEL_Y={BOT_LABEL_Y}")
