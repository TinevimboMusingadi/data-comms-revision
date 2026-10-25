"""Diagrams for Topics 1-2."""
import math
from dg import *


def components():
    d = Drawing(W, 175)
    # protocol bracket
    box(d, 30, 128, 120, 38, "PROTOCOL\nRule 1, Rule 2 ... Rule n", fill=LPURP, stroke=PURPLE, fs=8, bold=True)
    box(d, W - 150, 128, 120, 38, "PROTOCOL\nRule 1, Rule 2 ... Rule n", fill=LPURP, stroke=PURPLE, fs=8, bold=True)
    arrow(d, 152, 147, W - 152, 147, PURPLE, 1, both=True, dash=[4, 2])
    T(d, W / 2, 152, "both sides must follow the SAME rules", 7.5, italic=True, color=PURPLE)
    # sender / receiver
    pc(d, 90, 78, "", s=2.0)
    T(d, 90, 38, "1. SENDER", 9, bold=True, color=NAVY)
    T(d, 90, 28, "e.g. PC, phone, camera", 7.5, color=GREY)
    pc(d, W - 90, 78, "", s=2.0, fill=LGREEN)
    T(d, W - 90, 38, "2. RECEIVER", 9, bold=True, color=NAVY)
    T(d, W - 90, 28, "e.g. server, printer, TV", 7.5, color=GREY)
    # medium
    d.add(Rect(130, 70, W - 260, 12, rx=6, ry=6, fillColor=h("#ffd27f"), strokeColor=ORANGE))
    arrow(d, 136, 76, W - 134, 76, ORANGE, 1.8)
    T(d, W / 2, 56, "4. TRANSMISSION MEDIUM", 9, bold=True, color=ORANGE)
    T(d, W / 2, 46, "twisted pair, coaxial, fibre optic, radio waves", 7.5, color=GREY)
    # message envelope
    ex, ey = W / 2 - 34, 92
    d.add(Rect(ex, ey, 68, 26, fillColor=LYEL, strokeColor=YEL, strokeWidth=1))
    poly(d, [ex, ey + 26, ex + 34, ey + 10, ex + 68, ey + 26], YEL, 1)
    T(d, W / 2, 121, "3. MESSAGE", 9, bold=True, color=YEL)
    T(d, W / 2, 8, "text  |  numbers  |  images  |  audio  |  video", 7.5, color=GREY)
    T(d, W / 2, 18, "5. PROTOCOL = the rules (top boxes)", 7.5, bold=True, color=PURPLE)
    return d


def topologies():
    d = Drawing(W, 300)
    pw, ph, g = 152, 140, 13
    pos = [(0, 1), (1, 1), (2, 1), (0, 0), (1, 0), (2, 0)]
    titles = ["BUS", "STAR", "RING", "MESH (full)", "TREE (hierarchical)", "HYBRID (star-bus)"]
    O = []
    for (cx, cy), t in zip(pos, titles):
        x, y = cx * (pw + g), cy * (ph + 12) + 4
        panel(d, x, y, pw, ph, t)
        O.append((x, y))
    # bus
    x, y = O[0]
    line(d, x + 14, y + 62, x + pw - 14, y + 62, NAVY, 3)
    d.add(Rect(x + 8, y + 57, 6, 10, fillColor=RED, strokeColor=None))
    d.add(Rect(x + pw - 14, y + 57, 6, 10, fillColor=RED, strokeColor=None))
    for k, xx in enumerate([30, 62, 94, 126]):
        up = k % 2 == 0
        line(d, x + xx, y + 62, x + xx, y + (88 if up else 36), NAVY, 1)
        pc(d, x + xx, y + (96 if up else 28), "")
    T(d, x + pw / 2, y + 8, "one backbone + terminators", 7, italic=True, color=GREY)
    # star
    x, y = O[1]
    cx, cy = x + pw / 2, y + 64
    for k in range(6):
        a = math.radians(90 + k * 60)
        px, py = cx + 50 * math.cos(a), cy + 42 * math.sin(a)
        line(d, cx, cy, px, py, NAVY, 1)
        pc(d, px, py + 3, "")
    switch(d, cx, cy, "", w=36, inside="SWITCH")
    T(d, x + pw / 2, y + 8, "all nodes to a central hub/switch", 7, italic=True, color=GREY)
    # ring
    x, y = O[2]
    cx, cy = x + pw / 2, y + 66
    d.add(Circle(cx, cy, 42, fillColor=None, strokeColor=NAVY, strokeWidth=1.5))
    for k in range(6):
        a = math.radians(90 + k * 60)
        node(d, cx + 42 * math.cos(a), cy + 42 * math.sin(a), "ABCDEF"[k], r=8)
    a1, a2 = math.radians(60), math.radians(40)
    arrow(d, cx + 27 * math.cos(a1), cy + 27 * math.sin(a1), cx + 27 * math.cos(a2), cy + 27 * math.sin(a2), ORANGE, 1.4, 5)
    T(d, cx, cy - 3, "token", 7, color=ORANGE, bold=True)
    T(d, x + pw / 2, y + 8, "closed loop, data one direction", 7, italic=True, color=GREY)
    # mesh
    x, y = O[3]
    cx, cy = x + pw / 2, y + 64
    pts = [(cx + 46 * math.cos(math.radians(90 + k * 72)), cy + 44 * math.sin(math.radians(90 + k * 72))) for k in range(5)]
    for i in range(5):
        for j in range(i + 1, 5):
            line(d, pts[i][0], pts[i][1], pts[j][0], pts[j][1], BLUE, 0.9)
    for k, (px, py) in enumerate(pts):
        node(d, px, py, "ABCDE"[k], r=8, fill=NAVY)
    T(d, x + pw / 2, y + 8, "links = n(n-1)/2  (5 nodes = 10)", 7, italic=True, color=GREY)
    # tree
    x, y = O[4]
    root = (x + pw / 2, y + 102)
    mids = [(x + 42, y + 68), (x + pw - 42, y + 68)]
    for m in mids:
        line(d, root[0], root[1], m[0], m[1], NAVY, 1)
        for dx in (-20, 20):
            line(d, m[0], m[1], m[0] + dx, y + 36, NAVY, 1)
            pc(d, m[0] + dx, y + 32, "", s=0.85)
    switch(d, root[0], root[1], "", w=40, fill=NAVY, inside="CORE")
    for m in mids:
        switch(d, m[0], m[1], "", w=34, inside="SW")
    T(d, x + pw / 2, y + 8, "hierarchy of stars on a root", 7, italic=True, color=GREY)
    # hybrid
    x, y = O[5]
    line(d, x + 12, y + 92, x + pw - 12, y + 92, NAVY, 3)
    for sx in (x + 40, x + pw - 40):
        line(d, sx, y + 92, sx, y + 66, NAVY, 1)
        for dx in (-24, 0, 24):
            line(d, sx, y + 66, sx + dx, y + 38, NAVY, 1)
            pc(d, sx + dx, y + 34, "", s=0.8)
        switch(d, sx, y + 66, "", w=30, inside="SW")
    T(d, x + pw / 2, y + 100, "bus backbone", 7, bold=True, color=NAVY)
    T(d, x + pw / 2, y + 8, "mix of two topologies", 7, italic=True, color=GREY)
    return d


def building():
    d = Drawing(W, 250)
    fx, fw, fh = 8, 268, 36
    for k in range(5):
        y = 46 + k * (fh + 4)
        box(d, fx, y, fw, fh, "", fill=LGREY if k % 2 else WHITE, stroke=MGREY)
        T(d, fx + 6, y + fh / 2 - 3, "Floor %d" % (k + 1), 8, anchor="start", bold=True, color=NAVY)
        switch(d, fx + 76, y + fh / 2, "", w=40, inside="24-port")
        for i in range(6):
            px = fx + 116 + i * 22
            line(d, fx + 96, y + fh / 2, px, y + fh / 2 + 4, MGREY, 0.6)
            pc(d, px, y + fh / 2 + 6, "", s=0.7)
        T(d, fx + 256, y + fh / 2 - 3, "x20", 8, anchor="end", bold=True, color=ORANGE)
        T(d, fx + 186, y + 3.5, "VLAN %d0 - 192.168.%d0.0/27" % (k + 1, k + 1), 6.3, italic=True, color=GREY)
    # riser
    line(d, 300, 46 + fh / 2, 300, 46 + 4 * (fh + 4) + fh / 2, ORANGE, 2.5)
    for k in range(5):
        y = 46 + k * (fh + 4) + fh / 2
        line(d, fx + fw, y, 300, y, ORANGE, 1.6, dash=[3, 2])
    T(d, 306, 210, "fibre /", 7, anchor="start", bold=True, color=ORANGE)
    T(d, 306, 201, "Cat6 riser", 7, anchor="start", bold=True, color=ORANGE)
    # server room
    box(d, 8, 4, 400, 36, "", fill=LTEAL, stroke=TEAL)
    T(d, 14, 26, "Ground floor", 7.5, anchor="start", bold=True, color=TEAL)
    T(d, 14, 16, "server room", 7.5, anchor="start", bold=True, color=TEAL)
    switch(d, 300, 22, "", w=54, fill=NAVY, inside="CORE SWITCH")
    line(d, 300, 46, 300, 30, ORANGE, 2.5)
    server(d, 140, 22)
    server(d, 168, 22)
    T(d, 182, 26, "DHCP / file servers", 6.5, anchor="start", color=TEAL)
    line(d, 177, 16, 273, 16, NAVY, 1)
    firewall(d, 356, 22, "", w=30, hh=20)
    line(d, 327, 22, 341, 22, NAVY, 1.2)
    router(d, 396, 22, "", r=11)
    line(d, 371, 22, 385, 22, NAVY, 1.2)
    line(d, 407, 22, 430, 22, NAVY, 1.2)
    line(d, 430, 22, 430, 160, NAVY, 1.2)
    cloud(d, 432, 190, 90, 56, "INTERNET", fs=8)
    T(d, 356, 46, "Firewall", 6.5, bold=True)
    T(d, 396, 40, "Router", 6.5, bold=True)
    box(d, 330, 70, 145, 66, "Star on every floor\n+ all floor switches to core\n= extended star (tree)\nWi-Fi AP on each floor",
        fill=LYEL, stroke=YEL, fs=7.3)
    return d


# ------------------------------------------------------------------ topic 2
NAMES = {7: "Application", 6: "Presentation", 5: "Session", 4: "Transport", 3: "Network",
         2: "Data Link", 1: "Physical"}
PDU = {7: "Data", 6: "Data", 5: "Data", 4: "Segment", 3: "Packet", 2: "Frame", 1: "Bits"}


def osi_peer():
    d = Drawing(W, 262)
    lh, gap, top = 26, 3, 252
    lx, rx, cw = 46, W - 46 - 140, 140
    T(d, lx + cw / 2, top - 2, "SENDER (Host A)", 9, bold=True, color=NAVY)
    T(d, rx + cw / 2, top - 2, "RECEIVER (Host B)", 9, bold=True, color=NAVY)
    for i, L in enumerate(range(7, 0, -1)):
        y = top - 12 - (i + 1) * (lh + gap)
        for x in (lx, rx):
            box(d, x, y, cw, lh, "%d   %s" % (L, NAMES[L]), fill=LAYER[L], stroke=WHITE, sw=1.5, bold=True, fs=9)
        arrow(d, lx + cw + 4, y + lh / 2, rx - 4, y + lh / 2, GREY, 0.8, 4, both=True, dash=[3, 2])
        cbox(d, W / 2, y + lh / 2, 58, 13, PDU[L], fill=WHITE, stroke=GREY, fs=7.5, bold=True)
    yb = top - 12 - 7 * (lh + gap)
    # medium
    poly(d, [lx + cw / 2, yb, lx + cw / 2, 12, rx + cw / 2, 12, rx + cw / 2, yb], ORANGE, 3)
    T(d, W / 2, 16, "transmission medium (cable / radio)", 8, bold=True, color=ORANGE)
    # encapsulation arrows
    arrow(d, 22, top - 30, 22, yb + 6, BLUE, 2.5, 8)
    VT(d, 12, (top + yb) / 2 - 8, "ENCAPSULATION - headers added going down", 7.5, BLUE, True)
    arrow(d, W - 22, yb + 6, W - 22, top - 30, TEAL, 2.5, 8)
    VT(d, W - 8, (top + yb) / 2 - 8, "DECAPSULATION - headers removed going up", 7.5, TEAL, True)
    T(d, W / 2, top - 2, "PDU name", 8, bold=True, color=GREY)
    return d


def encapsulation():
    d = Drawing(W, 168)
    rows = [
        ("L7-5  Data", [("DATA", 120, LAYER[7])]),
        ("L4  Segment", [("TCP hdr", 52, LAYER[4]), ("DATA", 120, LAYER[7])]),
        ("L3  Packet", [("IP hdr", 52, LAYER[3]), ("TCP hdr", 52, LAYER[4]), ("DATA", 120, LAYER[7])]),
        ("L2  Frame", [("MAC hdr", 52, LAYER[2]), ("IP hdr", 52, LAYER[3]), ("TCP hdr", 52, LAYER[4]),
                       ("DATA", 120, LAYER[7]), ("FCS", 40, LAYER[2])]),
    ]
    y = 140
    for lab, parts in rows:
        T(d, 4, y + 6, lab, 8, anchor="start", bold=True, color=NAVY)
        tot = sum(p[1] for p in parts)
        x = W - 8 - tot - (0 if lab.startswith("L2") else 40)
        for t, w, f in parts:
            box(d, x, y, w, 20, t, fill=f, stroke=WHITE, sw=1.5, r=2, bold=True, fs=8)
            x += w
        y -= 30
    T(d, 4, y + 6, "L1  Bits", 8, anchor="start", bold=True, color=NAVY)
    box(d, W - 8 - 356, y, 356, 20, "0 1 1 0 1 0 0 1 1 1 0 1 0 1 1 0 0 1 0 1 1 1 0 0 1 0 1 1 0 1 0 0", fill=LAYER[1], stroke=WHITE, fs=8, bold=True)
    arrow(d, 96, 150, 96, 30, BLUE, 2, 7)
    T(d, W / 2 + 40, 4, "each layer wraps the one above: header added in front (Data Link also adds a trailer = FCS/CRC)", 7.3, italic=True, color=GREY)
    return d


def osi_tcpip():
    d = Drawing(W, 212)
    lh, gap, top = 25, 3, 200
    lx, mx = 10, 186
    T(d, lx + 75, top + 2, "OSI MODEL (7 layers)", 9, bold=True, color=NAVY)
    T(d, mx + 70, top + 2, "TCP/IP MODEL (4 layers)", 9, bold=True, color=NAVY)
    T(d, 400, top + 2, "Protocols", 9, bold=True, color=NAVY)
    ys = {}
    for i, L in enumerate(range(7, 0, -1)):
        y = top - 8 - (i + 1) * (lh + gap) + gap
        ys[L] = y
        box(d, lx, y, 150, lh, "%d  %s" % (L, NAMES[L]), fill=LAYER[L], stroke=WHITE, sw=1.5, bold=True, fs=8.5)
    groups = [("Application", 7, 5, LAYER[6], "HTTP, HTTPS, FTP, SMTP,\nPOP3, DNS, DHCP, SSH, SNMP"),
              ("Transport", 4, 4, LAYER[4], "TCP, UDP, SCTP"),
              ("Internet", 3, 3, LAYER[3], "IP (v4/v6), ICMP, ARP, IGMP"),
              ("Network Access\n(Host-to-Network)", 2, 1, LAYER[2], "Ethernet, Wi-Fi (802.11),\nPPP, DSL")]
    for name, a, b, f, prot in groups:
        y0, y1 = ys[b], ys[a] + lh
        box(d, mx, y0, 140, y1 - y0, name, fill=f, stroke=NAVY, sw=1, bold=True, fs=9)
        d.add(Polygon([lx + 150, ys[a] + lh, mx, y1, mx, y0, lx + 150, ys[b]], fillColor=h("#eef3fa"), strokeColor=None))
        box(d, 336, y0 + 2, W - 340, y1 - y0 - 4, prot, fill=WHITE, stroke=MGREY, fs=7.6)
        line(d, mx + 140, (y0 + y1) / 2, 336, (y0 + y1) / 2, MGREY, 0.8, dash=[2, 2])
    return d


FIGS = dict(components=components, topologies=topologies, building=building,
            osi_peer=osi_peer, encapsulation=encapsulation, osi_tcpip=osi_tcpip)
