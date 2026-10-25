"""Drawing primitives for the revision-pack diagrams (reportlab.graphics)."""
import math
from reportlab.graphics.shapes import (Drawing, Rect, Line, String, Polygon, Circle,
                                       Ellipse, Group, PolyLine)
from reportlab.lib import colors
from reportlab.pdfbase.pdfmetrics import stringWidth

W = 482  # usable width in points (170 mm)

h = colors.HexColor
NAVY, BLUE, LBLUE = h("#1f3a5f"), h("#2e6fb7"), h("#dce8f7")
TEAL, LTEAL = h("#14897a"), h("#d4efea")
ORANGE, LOR = h("#e0861a"), h("#fdebd3")
RED, LRED = h("#c0392b"), h("#f8d7d3")
GREEN, LGREEN = h("#2f9a4f"), h("#dcf1e2")
PURPLE, LPURP = h("#6c4fa3"), h("#e9e2f6")
YEL, LYEL = h("#c9a100"), h("#fff4bf")
GREY, LGREY, MGREY = h("#7f8c8d"), h("#eef1f4"), h("#c5ccd4")
INK, WHITE = h("#222222"), colors.white
# OSI layer fills 7..1
LAYER = {7: h("#f6c9c4"), 6: h("#fbdcb0"), 5: h("#fbefa6"), 4: h("#bfe5cf"),
         3: h("#b8d7f5"), 2: h("#cfc8f0"), 1: h("#dcdcdc")}

F, FB, FI = "Arial", "Arial-B", "Arial-I"


def fit(s, font, fs, maxw):
    while fs > 5 and stringWidth(s, font, fs) > maxw:
        fs -= 0.25
    return fs


def T(d, x, y, s, fs=8, anchor="middle", color=INK, bold=False, italic=False, maxw=None):
    font = FB if bold else (FI if italic else F)
    for i, line in enumerate(s.split("\n")):
        f2 = fit(line, font, fs, maxw) if maxw else fs
        d.add(String(x, y - i * fs * 1.22, line, fontName=font, fontSize=f2,
                     fillColor=color, textAnchor=anchor))


def VT(d, x, y, s, fs=8, color=INK, bold=False):
    """vertical text reading bottom-to-top, centred on (x, y)"""
    g = Group(String(0, 0, s, fontName=FB if bold else F, fontSize=fs, fillColor=color,
                     textAnchor="middle"))
    g.transform = (0, 1, -1, 0, x + fs * 0.35, y)
    d.add(g)


def box(d, x, y, w, hh, text="", fill=LBLUE, stroke=NAVY, fs=8, bold=False, tc=INK,
        r=4, sw=0.8, dash=None, italic=False):
    d.add(Rect(x, y, w, hh, rx=r, ry=r, fillColor=fill, strokeColor=stroke,
               strokeWidth=sw, strokeDashArray=dash))
    if text:
        lines = text.split("\n")
        font = FB if bold else (FI if italic else F)
        f2 = min(fit(l, font, fs, w - 5) for l in lines)
        f2 = min(f2, fit("x", font, fs, w))
        lead = f2 * 1.2
        while len(lines) * lead > hh - 2 and f2 > 5:
            f2 -= 0.25
            lead = f2 * 1.2
        y0 = y + hh / 2 + (len(lines) - 1) * lead / 2 - f2 * 0.35
        for i, l in enumerate(lines):
            d.add(String(x + w / 2, y0 - i * lead, l, fontName=font, fontSize=f2,
                         fillColor=tc, textAnchor="middle"))


def cbox(d, cx, cy, w, hh, text="", **kw):
    box(d, cx - w / 2, cy - hh / 2, w, hh, text, **kw)


def line(d, x1, y1, x2, y2, color=NAVY, w=1, dash=None):
    d.add(Line(x1, y1, x2, y2, strokeColor=color, strokeWidth=w, strokeDashArray=dash))


def poly(d, pts, color=NAVY, w=1, dash=None):
    d.add(PolyLine(pts, strokeColor=color, strokeWidth=w, strokeDashArray=dash))


def _head(d, x, y, a, color, hs):
    p = [x, y,
         x - hs * math.cos(a) + hs * 0.45 * math.sin(a), y - hs * math.sin(a) - hs * 0.45 * math.cos(a),
         x - hs * math.cos(a) - hs * 0.45 * math.sin(a), y - hs * math.sin(a) + hs * 0.45 * math.cos(a)]
    d.add(Polygon(p, fillColor=color, strokeColor=color, strokeWidth=0.3))


def arrow(d, x1, y1, x2, y2, color=NAVY, w=1.2, hs=6, both=False, dash=None):
    a = math.atan2(y2 - y1, x2 - x1)
    sx, sy = (x1 + hs * 0.8 * math.cos(a), y1 + hs * 0.8 * math.sin(a)) if both else (x1, y1)
    d.add(Line(sx, sy, x2 - hs * 0.8 * math.cos(a), y2 - hs * 0.8 * math.sin(a),
               strokeColor=color, strokeWidth=w, strokeDashArray=dash))
    _head(d, x2, y2, a, color, hs)
    if both:
        _head(d, x1, y1, a + math.pi, color, hs)


def parrow(d, pts, color=NAVY, w=1.2, hs=6, dash=None):
    """poly-line ending in an arrow head"""
    if len(pts) > 4:
        poly(d, pts[:-2], color, w, dash)
    arrow(d, pts[-4], pts[-3], pts[-2], pts[-1], color, w, hs, dash=dash)


def xmark(d, x, y, s=6, color=RED):
    line(d, x - s, y - s, x + s, y + s, color, 2.2)
    line(d, x - s, y + s, x + s, y - s, color, 2.2)


def diamond(d, cx, cy, w, hh, text, fill=LOR, stroke=ORANGE, fs=8):
    d.add(Polygon([cx, cy + hh / 2, cx + w / 2, cy, cx, cy - hh / 2, cx - w / 2, cy],
                  fillColor=fill, strokeColor=stroke, strokeWidth=1))
    T(d, cx, cy + (len(text.split("\n")) - 1) * fs * 0.6 - fs * 0.35, text, fs, bold=True,
      maxw=w * 0.62)


# ---------------------------------------------------------------- icons
def pc(d, x, y, label="", s=1.0, fill=LBLUE, lc=INK, lfs=7):
    """computer icon centred on monitor (x, y)"""
    w, hh = 22 * s, 15 * s
    d.add(Rect(x - w / 2, y - hh / 2, w, hh, rx=1.5, ry=1.5, fillColor=fill, strokeColor=NAVY, strokeWidth=0.9))
    d.add(Rect(x - w / 2 + 2 * s, y - hh / 2 + 2 * s, w - 4 * s, hh - 4 * s, fillColor=WHITE, strokeColor=None))
    d.add(Rect(x - 2 * s, y - hh / 2 - 4 * s, 4 * s, 4 * s, fillColor=NAVY, strokeColor=None))
    d.add(Rect(x - 7 * s, y - hh / 2 - 5.5 * s, 14 * s, 2 * s, fillColor=NAVY, strokeColor=None))
    if label:
        T(d, x, y - hh / 2 - 6 * s - lfs, label, lfs, color=lc)


def router(d, x, y, label="", r=12, lfs=7):
    d.add(Circle(x, y, r, fillColor=NAVY, strokeColor=WHITE, strokeWidth=1))
    k = r * 0.55
    for ax, ay in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        arrow(d, x + ax * k * 0.15, y + ay * k * 0.15, x + ax * k, y + ay * k, WHITE, 1, 3)
    if label:
        T(d, x, y - r - lfs - 1, label, lfs, bold=True)


def switch(d, x, y, label="", w=44, fill=TEAL, lfs=7, inside=None):
    hh = 15
    d.add(Rect(x - w / 2, y - hh / 2, w, hh, rx=2, ry=2, fillColor=fill, strokeColor=NAVY, strokeWidth=0.8))
    if inside:
        T(d, x, y - 2.6, inside, 6.5, color=WHITE, bold=True)
    else:
        n = int(w // 7)
        for i in range(n):
            d.add(Rect(x - w / 2 + 3 + i * (w - 6) / n, y - 2, (w - 6) / n - 2, 4, fillColor=WHITE, strokeColor=None))
    if label:
        T(d, x, y - hh / 2 - lfs - 1, label, lfs, bold=True)


def firewall(d, x, y, label="Firewall", w=34, hh=22, lfs=7):
    d.add(Rect(x - w / 2, y - hh / 2, w, hh, fillColor=h("#d35c3c"), strokeColor=h("#8e2f1a"), strokeWidth=0.8))
    for i in range(1, 3):
        line(d, x - w / 2, y - hh / 2 + i * hh / 3, x + w / 2, y - hh / 2 + i * hh / 3, WHITE, 0.8)
    for row in range(3):
        off = 0 if row % 2 == 0 else w / 4
        for k in range(1, 3):
            xx = x - w / 2 + off + k * w / 3
            if xx < x + w / 2:
                line(d, xx, y - hh / 2 + row * hh / 3, xx, y - hh / 2 + (row + 1) * hh / 3, WHITE, 0.8)
    if label:
        T(d, x, y - hh / 2 - lfs - 1, label, lfs, bold=True)


def server(d, x, y, label="", lfs=7):
    w, hh = 18, 30
    d.add(Rect(x - w / 2, y - hh / 2, w, hh, rx=2, ry=2, fillColor=h("#4a5d73"), strokeColor=NAVY))
    for i in range(3):
        d.add(Rect(x - w / 2 + 3, y + hh / 2 - 8 - i * 8, w - 6, 4, fillColor=h("#a9c4e0"), strokeColor=None))
        d.add(Circle(x + w / 2 - 4, y + hh / 2 - 6 - i * 8, 0.9, fillColor=h("#7cf08a"), strokeColor=None))
    if label:
        T(d, x, y - hh / 2 - lfs - 1, label, lfs, bold=True)


def cloud(d, cx, cy, w, hh, label="", fill=LBLUE, stroke=BLUE, fs=9):
    parts = [(-0.28, -0.05, 0.27, 0.36), (0.0, 0.12, 0.3, 0.42), (0.27, -0.02, 0.27, 0.36),
             (0.0, -0.18, 0.42, 0.3)]
    for dx, dy, rx, ry in parts:
        d.add(Ellipse(cx + dx * w, cy + dy * hh, rx * w, ry * hh, fillColor=fill, strokeColor=stroke, strokeWidth=0.9))
    for dx, dy, rx, ry in parts:  # second pass hides inner outlines
        d.add(Ellipse(cx + dx * w, cy + dy * hh, rx * w - 1, ry * hh - 1, fillColor=fill, strokeColor=None))
    if label:
        T(d, cx, cy - fs * 0.35, label, fs, bold=True, color=NAVY)


def node(d, x, y, label="", r=7, fill=BLUE):
    d.add(Circle(x, y, r, fillColor=fill, strokeColor=WHITE, strokeWidth=1))
    if label:
        T(d, x, y - 2.4, label, 6.5, color=WHITE, bold=True)


def panel(d, x, y, w, hh, title, fill=LGREY, tfill=NAVY):
    d.add(Rect(x, y, w, hh, rx=5, ry=5, fillColor=fill, strokeColor=MGREY, strokeWidth=0.8))
    d.add(Rect(x, y + hh - 16, w, 16, rx=5, ry=5, fillColor=tfill, strokeColor=None))
    d.add(Rect(x, y + hh - 16, w, 8, fillColor=tfill, strokeColor=None))
    T(d, x + w / 2, y + hh - 11.5, title, 8.5, color=WHITE, bold=True)


def key(d, x, y, color=ORANGE, s=1.0):
    d.add(Circle(x, y, 5 * s, fillColor=WHITE, strokeColor=color, strokeWidth=2.2 * s))
    d.add(Rect(x + 5 * s, y - 1.2 * s, 13 * s, 2.6 * s, fillColor=color, strokeColor=None))
    d.add(Rect(x + 13 * s, y - 5 * s, 2.4 * s, 4 * s, fillColor=color, strokeColor=None))
    d.add(Rect(x + 16.5 * s, y - 4 * s, 2.4 * s, 3 * s, fillColor=color, strokeColor=None))


def lock(d, x, y, color=GREEN, s=1.0):
    d.add(Rect(x - 6 * s, y - 6 * s, 12 * s, 9 * s, rx=1.5, ry=1.5, fillColor=color, strokeColor=None))
    d.add(Rect(x - 4 * s, y + 3 * s, 8 * s, 6 * s, rx=4 * s, ry=4 * s, fillColor=None, strokeColor=color, strokeWidth=1.8 * s))
    d.add(Circle(x, y - 2 * s, 1.4 * s, fillColor=WHITE, strokeColor=None))


def brace_h(d, x1, x2, y, label, up=False, color=NAVY, fs=7.5):
    """horizontal bracket under (or over) a span, with label"""
    k = 5 if up else -5
    poly(d, [x1, y, x1, y + k, x2, y + k, x2, y], color, 1)
    line(d, (x1 + x2) / 2, y + k, (x1 + x2) / 2, y + 2 * k, color, 1)
    T(d, (x1 + x2) / 2, y + 2 * k + (3 if up else -fs - 1), label, fs, color=color, bold=True)


# ---------------------------------------------------------------- composite helpers
def seq(parts, msgs, gap=27, states=None, colors_=None, top_pad=10, width=W):
    """Sequence (timeline) diagram.
    parts  : participant names
    msgs   : (i, j, label[, kind]) kind in {None, 'lost', 'dash'} or ('note', text)
    states : {row_index: (left_text, right_text)} shown beside the outer lifelines
    """
    n = len(parts)
    margin = 105 if states else 70
    xs = [margin + k * (width - 2 * margin) / (n - 1) for k in range(n)]
    rows = sum(0.85 if m[0] == "note" else 1 for m in msgs)
    hh = 34 + top_pad + rows * gap + 14
    d = Drawing(width, hh)
    top = hh - top_pad
    for k, (x, p) in enumerate(zip(xs, parts)):
        cbox(d, x, top - 11, 118 if n < 4 else 100, 22, p, fill=(colors_ or [NAVY] * n)[k], stroke=None,
             tc=WHITE, bold=True, fs=8.5)
        line(d, x, top - 22, x, 6, MGREY, 1.2, dash=[3, 2])
    y = top - 22 - gap * 0.85
    for r, m in enumerate(msgs):
        if m[0] == "note":
            tw = min(stringWidth(m[1], FI, 7.5) + 14, xs[-1] - xs[0] + 60)
            cbox(d, (xs[0] + xs[-1]) / 2, y + 2, tw, 15, m[1], fill=LYEL, stroke=YEL, fs=7.5, italic=True)
            y -= gap * 0.85
            continue
        i, j, lab = m[:3]
        kind = m[3] if len(m) > 3 else None
        x1, x2 = xs[i], xs[j]
        col = BLUE if j > i else TEAL
        y2 = y - 7
        if kind == "lost":
            xm = x1 + (x2 - x1) * 0.62
            ym = y + (y2 - y) * 0.62
            arrow(d, x1, y, xm, ym, RED, 1.3)
            xmark(d, xm + (5 if j > i else -5), ym, 4.5)
            T(d, xm + (14 if j > i else -14), ym - 3, "lost", 7, anchor="start" if j > i else "end", color=RED, bold=True)
        else:
            arrow(d, x1, y, x2, y2, col, 1.3, dash=[4, 2] if kind == "dash" else None)
        T(d, (x1 + x2) / 2, y + 3.5, lab, 7.6, bold=True, color=INK, maxw=abs(x2 - x1) - 10)
        if states and r in states:
            lt, rt = states[r]
            if lt:
                cbox(d, xs[0] - 52, y - 3, 86, 13, lt, fill=LGREEN, stroke=GREEN, fs=6.8, bold=True)
            if rt:
                cbox(d, xs[-1] + 52, y - 3, 86, 13, rt, fill=LGREEN, stroke=GREEN, fs=6.8, bold=True)
        y -= gap
    return d


def fields(rows, ruler=(0, 4, 8, 16, 19, 31), rowh=21, note=None):
    """packet-header bit-field diagram; rows = [(height_units, [(label, bits, fill), ...]), ...]"""
    x0 = 34
    wb = (W - 2 * x0) / 32
    total = sum(r[0] for r in rows) * rowh
    hh = total + 26 + (14 if note else 0)
    d = Drawing(W, hh)
    top = hh - 18
    for b in ruler:
        T(d, x0 + b * wb + wb / 2, top + 5, str(b), 7, color=GREY, bold=True)
    line(d, x0, top + 1, x0 + 32 * wb, top + 1, GREY, 0.6)
    y = top
    for hu, fl in rows:
        x = x0
        for lab, bits, fill in fl:
            box(d, x, y - hu * rowh, bits * wb, hu * rowh, lab, fill=fill, stroke=WHITE, sw=1.6, r=0, fs=7.8, bold=True)
            x += bits * wb
        y -= hu * rowh
    T(d, x0 - 6, top - total / 2, "", 7)
    if note:
        T(d, W / 2, 4, note, 7.5, italic=True, color=GREY)
    return d
