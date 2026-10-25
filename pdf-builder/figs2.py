"""Diagrams for Topics 3-4."""
import math
from dg import *


# ------------------------------------------------------------------ topic 3
def _net(d, ox, oy, hi=None, col=ORANGE):
    P = dict(A=(ox + 16, oy + 62), S1=(ox + 56, oy + 92), S2=(ox + 100, oy + 92),
             S3=(ox + 56, oy + 32), S4=(ox + 100, oy + 32), B=(ox + 138, oy + 62))
    links = [("A", "S1"), ("A", "S3"), ("S1", "S2"), ("S3", "S4"), ("S1", "S4"), ("S2", "B"), ("S4", "B")]
    for a, b in links:
        on = hi and ((a, b) in hi or (b, a) in hi)
        line(d, *P[a], *P[b], col if on else MGREY, 4 if on else 1.2)
    for k, (x, y) in P.items():
        if k in "AB":
            node(d, x, y, k, r=9, fill=GREEN)
        else:
            node(d, x, y, k, r=9, fill=NAVY)
    return P


def switching():
    d = Drawing(W, 210)
    pw, g = 152, 13
    titles = ["CIRCUIT SWITCHING", "MESSAGE SWITCHING", "PACKET SWITCHING"]
    for i, t in enumerate(titles):
        panel(d, i * (pw + g), 40, pw, 168, t)
    # circuit
    _net(d, 0, 52, hi=[("A", "S1"), ("S1", "S2"), ("S2", "B")])
    T(d, pw / 2, 166, "dedicated path reserved", 7.5, bold=True, color=ORANGE)
    # message
    ox = pw + g
    P = _net(d, ox, 52, hi=[("A", "S3"), ("S3", "S4"), ("S4", "B")], col=PURPLE)
    for k in ("S3", "S4"):
        x, y = P[k]
        d.add(Rect(x - 13, y + 12, 26, 15, fillColor=LYEL, strokeColor=YEL))
        poly(d, [x - 13, y + 27, x, y + 19, x + 13, y + 27], YEL, 0.8)
    T(d, ox + pw / 2, 166, "whole message stored at each", 7.5, bold=True, color=PURPLE)
    T(d, ox + pw / 2, 157, "node, then forwarded", 7.5, bold=True, color=PURPLE)
    # packet
    ox = 2 * (pw + g)
    P = _net(d, ox, 52)
    routes = [(["A", "S1", "S2", "B"], BLUE, "1"), (["A", "S3", "S4", "B"], RED, "2"), (["A", "S1", "S4", "B"], GREEN, "3")]
    for path, c, lab in routes:
        for a, b in zip(path, path[1:]):
            (x1, y1), (x2, y2) = P[a], P[b]
            line(d, x1, y1, x2, y2, c, 1.6)
        (x1, y1), (x2, y2) = P[path[1]], P[path[2]]
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        box(d, mx - 6, my - 6, 12, 12, lab, fill=c, stroke=WHITE, tc=WHITE, bold=True, fs=7, r=1)
    for k, (x, y) in P.items():
        node(d, x, y, k, r=9, fill=GREEN if k in "AB" else NAVY)
    T(d, ox + pw / 2, 166, "packets take different routes,", 7.5, bold=True, color=BLUE)
    T(d, ox + pw / 2, 157, "reassembled at B", 7.5, bold=True, color=BLUE)
    rows = [("e.g. telephone (PSTN), ISDN", "e.g. telegraph, early e-mail", "e.g. the Internet (IP), X.25"),
            ("setup -> data -> teardown", "store-and-forward, big delay", "store-and-forward, shares links")]
    for i in range(3):
        T(d, i * (pw + g) + pw / 2, 26, rows[0][i], 7.5, bold=True, color=NAVY)
        T(d, i * (pw + g) + pw / 2, 15, rows[1][i], 7.3, italic=True, color=GREY)
    return d


def media_tree():
    d = Drawing(W, 175)
    cbox(d, W / 2, 158, 170, 24, "TRANSMISSION MEDIA", fill=NAVY, stroke=None, tc=WHITE, bold=True, fs=10)
    kids = [(W * 0.26, "GUIDED  (bounded / wired)", BLUE, LBLUE,
             [("Twisted pair", "UTP / STP, RJ-45, LANs"), ("Coaxial cable", "cable TV, CCTV"), ("Fibre optic", "light, backbones, WAN")]),
            (W * 0.74, "UNGUIDED  (unbounded / wireless)", TEAL, LTEAL,
             [("Radio waves", "Wi-Fi, FM, omnidirectional"), ("Microwaves", "line of sight, satellite"), ("Infrared", "short range, TV remote")])]
    for x, t, c, lc, leaves in kids:
        poly(d, [W / 2, 146, W / 2, 132, x, 132, x, 122], NAVY, 1.2)
        cbox(d, x, 110, 200, 22, t, fill=c, stroke=None, tc=WHITE, bold=True, fs=9)
        for i, (a, b) in enumerate(leaves):
            lx = x - 75 + i * 75
            poly(d, [x, 99, x, 90, lx, 90, lx, 80], c, 1)
            box(d, lx - 35, 34, 70, 46, "", fill=lc, stroke=c)
            T(d, lx, 66, a, 8, bold=True, color=c, maxw=66)
            T(d, lx, 52, b.replace(", ", ",\n", 1), 6.8, color=INK, maxw=66)
    T(d, W * 0.26, 18, "more secure, faster, less interference", 7.5, italic=True, color=BLUE)
    T(d, W * 0.74, 18, "mobility, easy to install, less secure", 7.5, italic=True, color=TEAL)
    return d


def fibre():
    d = Drawing(W, 175)
    x0, x1, yc = 92, W - 92, 92
    d.add(Rect(x0, yc - 34, x1 - x0, 68, rx=10, ry=10, fillColor=h("#3d4b5c"), strokeColor=None))
    d.add(Rect(x0, yc - 25, x1 - x0, 50, fillColor=h("#9fc3e7"), strokeColor=None))
    d.add(Rect(x0, yc - 13, x1 - x0, 26, fillColor=h("#eaf6ff"), strokeColor=None))
    pts, x, up, n = [], x0, False, 9
    step = (x1 - x0) / n
    for k in range(n + 1):
        pts += [x0 + k * step, yc + (12 if up else -12)]
        up = not up
    poly(d, pts, ORANGE, 2)
    for k in range(1, n):
        xx, yy = pts[2 * k], pts[2 * k + 1]
        d.add(Circle(xx, yy, 2, fillColor=ORANGE, strokeColor=None))
    arrow(d, x1 - 40, yc, x1 - 6, yc, ORANGE, 0.1, 7)
    # source + detector
    box(d, 8, yc - 26, 78, 52, "LED / LASER\nelectrical -> light", fill=LOR, stroke=ORANGE, bold=True, fs=7.6)
    box(d, W - 86, yc - 26, 78, 52, "PHOTO-\nDETECTOR\nlight -> electrical", fill=LGREEN, stroke=GREEN, bold=True, fs=7.6)
    # input pulses
    T(d, 47, yc + 44, "1 0 1 1 0 1", 8, bold=True, color=NAVY)
    T(d, W - 47, yc + 44, "1 0 1 1 0 1", 8, bold=True, color=NAVY)
    # labels
    lab = [(140, yc + 34, 156, "Jacket (protection)", GREY), (285, yc + 25, 168, "Cladding - LOWER refractive index", BLUE)]
    line(d, 340, yc - 10, 340, 52, NAVY, 0.8)
    T(d, 340, 44, "Core (glass) - HIGHER refractive index", 7.5, bold=True, color=NAVY)
    for xx, yy, ty, s, c in lab:
        line(d, xx, yy, xx, ty - 4, c, 0.8)
        T(d, xx, ty, s, 7.5, bold=True, color=c)
    xx = pts[8]
    line(d, xx, pts[9], xx - 10, 34, RED, 0.8)
    T(d, xx - 10, 24, "Total internal reflection: ray hits the core/cladding boundary above the critical angle and bounces back", 7.5, bold=True, color=RED)
    T(d, W / 2, 8, "Single-mode: thin core, one path, laser, very long distance  |  Multi-mode: thicker core, many paths, LED", 7.2, italic=True, color=GREY)
    return d


def signals():
    d = Drawing(W, 112)
    for i, t in enumerate(["ANALOGUE - continuous, infinite values", "DIGITAL - discrete, limited values (0/1)"]):
        x = i * 248
        panel(d, x, 4, 234, 104, t)
        line(d, x + 14, 46, x + 222, 46, GREY, 0.7)
        line(d, x + 14, 12, x + 14, 84, GREY, 0.7)
    pts = []
    for k in range(201):
        t = k / 200
        pts += [14 + t * 206, 46 + 30 * math.sin(t * 6 * math.pi)]
    poly(d, pts, BLUE, 2)
    bits = [1, 0, 1, 1, 0, 1, 0, 0]
    pts, x = [], 248 + 14
    bw = 206 / len(bits)
    for b in bits:
        y = 76 if b else 20
        pts += [x, y, x + bw, y]
        x += bw
    poly(d, pts, TEAL, 2)
    for k, b in enumerate(bits):
        T(d, 262 + k * bw + bw / 2, 80, str(b), 7.5, bold=True, color=TEAL)
    return d


def mux():
    d = Drawing(W, 130)
    cols = [BLUE, RED, GREEN]
    for k, c in enumerate(cols):
        y = 98 - k * 34
        box(d, 4, y - 11, 64, 22, "Source %d" % (k + 1), fill=c, stroke=None, tc=WHITE, bold=True)
        line(d, 68, y, 130, 64, c, 1.6)
        box(d, W - 68, y - 11, 64, 22, "Dest %d" % (k + 1), fill=c, stroke=None, tc=WHITE, bold=True)
        line(d, W - 130, 64, W - 68, y, c, 1.6)
    d.add(Polygon([130, 102, 170, 84, 170, 44, 130, 26], fillColor=NAVY, strokeColor=None))
    T(d, 150, 61, "MUX", 9, bold=True, color=WHITE)
    d.add(Polygon([W - 130, 102, W - 170, 84, W - 170, 44, W - 130, 26], fillColor=NAVY, strokeColor=None))
    T(d, W - 150, 61, "DEMUX", 8, bold=True, color=WHITE)
    d.add(Rect(170, 50, W - 340, 28, rx=14, ry=14, fillColor=LGREY, strokeColor=NAVY, strokeWidth=1.2))
    for k, c in enumerate(cols):
        line(d, 180, 57 + k * 7, W - 180, 57 + k * 7, c, 2)
    T(d, W / 2, 86, "ONE shared link carrying n channels", 8.5, bold=True, color=NAVY)
    T(d, 150, 14, "many-to-one", 7.5, italic=True, color=GREY)
    T(d, W - 150, 14, "one-to-many", 7.5, italic=True, color=GREY)
    T(d, W / 2, 2, "FDM (frequency)  |  TDM (time)  |  WDM (light wavelengths)", 7.5, italic=True, color=GREY)
    return d


def fdm_tdm():
    d = Drawing(W, 132)
    panel(d, 0, 4, 234, 124, "FDM - split the FREQUENCY")
    panel(d, 248, 4, 234, 124, "TDM - split the TIME")
    cols = [BLUE, RED, GREEN]
    arrow(d, 22, 14, 222, 14, GREY, 0.8, 5)
    arrow(d, 22, 14, 22, 104, GREY, 0.8, 5)
    T(d, 214, 18, "time", 7, color=GREY, anchor="end")
    VT(d, 14, 60, "frequency", 7, GREY)
    for k, c in enumerate(cols):
        y = 24 + k * 26
        box(d, 30, y, 186, 18, "Channel %d (all the time)" % (k + 1), fill=c, stroke=None, tc=WHITE, bold=True, r=2)
        if k < 2:
            T(d, 123, y + 20, "guard band", 6, italic=True, color=GREY)
    arrow(d, 270, 14, 470, 14, GREY, 0.8, 5)
    T(d, 462, 18, "time", 7, color=GREY, anchor="end")
    x = 272
    for f in range(2):
        for k, c in enumerate(cols):
            box(d, x, 28, 31, 54, "ABC"[k], fill=c, stroke=WHITE, sw=1.5, tc=WHITE, bold=True, fs=10, r=1)
            x += 31
        brace_h(d, x - 93, x, 84, "frame %d" % (f + 1), up=True)
        x += 4
    T(d, 365, 20, "each source gets the FULL bandwidth in its slot", 6.8, italic=True, color=GREY)
    return d


def adsl():
    d = Drawing(W, 200)
    # spectrum (not to scale)
    y0 = 128
    arrow(d, 20, y0, W - 10, y0, GREY, 0.8, 5)
    T(d, W - 14, y0 - 24, "frequency ->", 7, anchor="end", color=GREY)
    box(d, 24, y0, 48, 44, "VOICE\n(phone)", fill=GREEN, stroke=None, tc=WHITE, bold=True)
    box(d, 96, y0, 96, 44, "UPSTREAM\ndata (slow)", fill=ORANGE, stroke=None, tc=WHITE, bold=True)
    box(d, 192, y0, 270, 44, "DOWNSTREAM data (fast)  ->  more bandwidth = ASYMMETRIC", fill=BLUE, stroke=None, tc=WHITE, bold=True)
    for x, s in ((24, "0"), (72, "4 kHz"), (96, "25 kHz"), (192, "138 kHz"), (462, "1.1 MHz")):
        line(d, x, y0, x, y0 - 4, GREY, 0.8)
        T(d, x, y0 - 13, s, 7, bold=True, color=GREY)
    T(d, 84, y0 + 50, "guard", 6.5, italic=True, color=GREY)
    T(d, W / 2, 190, "Different frequency bands = no interference (FDM on one copper pair)  -  not to scale", 7.5, bold=True, color=NAVY)
    # wiring
    yw = 52
    box(d, 4, 4, 196, 92, "", fill=LGREY, stroke=MGREY)
    T(d, 10, 86, "HOME", 7.5, anchor="start", bold=True, color=NAVY)
    box(d, W - 196, 4, 192, 92, "", fill=LGREY, stroke=MGREY)
    T(d, W - 190, 86, "TELEPHONE EXCHANGE", 7.5, anchor="start", bold=True, color=NAVY)
    box(d, 20, 64, 58, 18, "Telephone", fill=GREEN, stroke=None, tc=WHITE, bold=True, fs=7.5)
    box(d, 20, 22, 58, 18, "ADSL modem", fill=BLUE, stroke=None, tc=WHITE, bold=True, fs=7.5)
    pc(d, 108, 36, "PC", s=0.9)
    line(d, 78, 31, 96, 34, NAVY, 1)
    cbox(d, 160, yw, 52, 30, "SPLITTER\n/ filter", fill=YEL, stroke=None, tc=WHITE, bold=True, fs=7)
    line(d, 78, 73, 134, yw + 6, GREEN, 1.5)
    line(d, 78, 31, 134, yw - 6, BLUE, 1.5)
    line(d, 186, yw, W - 186, yw, ORANGE, 3)
    T(d, W / 2, yw + 6, "one copper pair", 7.5, bold=True, color=ORANGE)
    T(d, W / 2, yw - 13, "voice + data together", 7, italic=True, color=GREY)
    cbox(d, W - 160, yw, 52, 30, "SPLITTER", fill=YEL, stroke=None, tc=WHITE, bold=True, fs=7)
    box(d, W - 100, 64, 90, 18, "PSTN voice switch", fill=GREEN, stroke=None, tc=WHITE, bold=True, fs=7.5)
    box(d, W - 100, 22, 90, 18, "DSLAM -> ISP", fill=BLUE, stroke=None, tc=WHITE, bold=True, fs=7.5)
    line(d, W - 134, yw + 6, W - 100, 73, GREEN, 1.5)
    line(d, W - 134, yw - 6, W - 100, 31, BLUE, 1.5)
    return d


# ------------------------------------------------------------------ topic 4
def dll_stack():
    d = Drawing(W, 138)
    x, w = 20, 200
    box(d, x, 108, w, 24, "Network layer (IP)", fill=LAYER[3], stroke=WHITE, bold=True, fs=9)
    box(d, x, 72, w, 32, "LLC - Logical Link Control\n(IEEE 802.2)  upper sub-layer", fill=h("#b9a9ea"), stroke=WHITE, bold=True, fs=8.3)
    box(d, x, 36, w, 32, "MAC - Media Access Control\n(802.3 / 802.11)  lower sub-layer", fill=LAYER[2], stroke=WHITE, bold=True, fs=8.3)
    box(d, x, 6, w, 26, "Physical layer", fill=LAYER[1], stroke=WHITE, bold=True, fs=9)
    poly(d, [x + w + 6, 104, x + w + 14, 104, x + w + 14, 36, x + w + 6, 36], PURPLE, 1.5)
    VT(d, x + w + 24, 70, "DATA LINK LAYER", 8, PURPLE, True)
    box(d, 262, 72, 216, 32, "flow control, error control (ACKs), identifies\nnetwork protocol, same for every LAN type", fill=WHITE, stroke=h("#b9a9ea"), fs=7.4)
    box(d, 262, 36, 216, 32, "framing, MAC addresses, CRC check, decides who\ntransmits: CSMA/CD (wired), CSMA/CA (Wi-Fi)", fill=WHITE, stroke=LAYER[2], fs=7.4)
    line(d, 236, 88, 262, 88, MGREY, 0.8, dash=[2, 2])
    line(d, 236, 52, 262, 52, MGREY, 0.8, dash=[2, 2])
    return d


def csma_cd():
    d = Drawing(W, 300)
    L, R = 130, 345
    r = [272, 210, 150, 92, 30]

    def proc(cx, cy, t, fill=LBLUE, stroke=BLUE, w=150):
        cbox(d, cx, cy, w, 30, t, fill=fill, stroke=stroke, bold=True, fs=8)

    cbox(d, L, r[0], 150, 28, "Station has a frame to send", fill=NAVY, stroke=None, tc=WHITE, bold=True, r=14)
    diamond(d, L, r[1], 150, 48, "Medium idle?\n(carrier sense)")
    proc(L, r[2], "Transmit frame and keep\nlistening (collision detect)")
    diamond(d, L, r[3], 150, 48, "Collision\ndetected?")
    cbox(d, L, r[4], 150, 28, "SUCCESS - frame sent", fill=GREEN, stroke=None, tc=WHITE, bold=True, r=14)
    arrow(d, L, r[0] - 14, L, r[1] + 24)
    arrow(d, L, r[1] - 24, L, r[2] + 15)
    T(d, L + 8, r[1] - 36, "Yes", 7.5, anchor="start", bold=True, color=GREEN)
    arrow(d, L, r[2] - 15, L, r[3] + 24)
    arrow(d, L, r[3] - 24, L, r[4] + 14)
    T(d, L + 8, r[3] - 36, "No", 7.5, anchor="start", bold=True, color=GREEN)
    # idle? no -> wait loop
    parrow(d, [L - 75, r[1], 22, r[1], 22, r[1] + 42, L - 4, r[1] + 42], ORANGE)
    T(d, 26, r[1] + 6, "No: wait", 7.5, anchor="start", bold=True, color=ORANGE)
    # collision -> right column
    proc(R, r[3], "Stop and send a JAM signal", fill=LRED, stroke=RED)
    arrow(d, L + 75, r[3], R - 75, r[3], RED)
    T(d, (L + R) / 2, r[3] + 5, "Yes", 7.5, bold=True, color=RED)
    proc(R, r[2], "attempts = attempts + 1", fill=LRED, stroke=RED)
    arrow(d, R, r[3] + 15, R, r[2] - 15, RED)
    diamond(d, R, r[1], 140, 48, "attempts > 15 ?")
    arrow(d, R, r[2] + 15, R, r[1] - 24, RED)
    cbox(d, 448, r[1], 60, 26, "ABORT", fill=RED, stroke=None, tc=WHITE, bold=True, r=13)
    arrow(d, R + 70, r[1], 418, r[1], RED)
    T(d, R + 76, r[1] + 5, "Yes", 7.5, anchor="start", bold=True, color=RED)
    proc(R, r[0], "Wait random BACKOFF time\nR x slot, R in 0 .. 2^k - 1", fill=LOR, stroke=ORANGE, w=160)
    arrow(d, R, r[1] + 24, R, r[0] - 15, ORANGE)
    T(d, R + 6, r[1] + 32, "No", 7.5, anchor="start", bold=True, color=ORANGE)
    parrow(d, [R - 80, r[0], 225, r[0], 225, r[1] + 42, L + 4, r[1] + 42], ORANGE)
    # small collision picture
    box(d, 236, 4, 242, 44, "", fill=LGREY, stroke=MGREY)
    line(d, 248, 18, 466, 18, NAVY, 2.5)
    pc(d, 262, 34, "", s=0.8)
    pc(d, 452, 34, "", s=0.8)
    T(d, 280, 31, "A", 8, bold=True, color=NAVY)
    T(d, 434, 31, "D", 8, bold=True, color=NAVY)
    arrow(d, 270, 22, 345, 22, BLUE, 1.5)
    arrow(d, 444, 22, 369, 22, TEAL, 1.5)
    d.add(Polygon([357, 32, 361, 25, 368, 27, 363, 21, 368, 14, 360, 17, 357, 10, 354, 17, 346, 14, 351, 21, 346, 27, 353, 25],
                  fillColor=RED, strokeColor=None))
    T(d, 357, 36, "COLLISION", 7, bold=True, color=RED)
    return d


def aloha():
    d = Drawing(W, 228)
    tl, tw = 60, W - 72

    def lane(y0, slotted):
        for k, s in enumerate("ABC"):
            y = y0 + 64 - k * 24
            T(d, tl - 8, y - 3, "Station " + s, 7.5, anchor="end", bold=True, color=NAVY)
            line(d, tl, y - 8, tl + tw, y - 8, MGREY, 0.6)
        arrow(d, tl, y0 + 6, tl + tw, y0 + 6, GREY, 0.8, 5)
        T(d, tl + tw, y0 - 4, "time", 7, anchor="end", color=GREY)
        if slotted:
            for k in range(8):
                line(d, tl + k * 50, y0 + 6, tl + k * 50, y0 + 84, GREY, 0.6, dash=[2, 2])
                T(d, tl + k * 50 + 25, y0 - 4, "slot %d" % (k + 1), 6.5, color=GREY)

    def frame(y0, row, x, lab, bad):
        y = y0 + 64 - row * 24 - 8
        box(d, tl + x, y, 50, 15, lab, fill=RED if bad else BLUE, stroke=WHITE, tc=WHITE, bold=True, fs=7.5, r=2)

    panel(d, 0, 118, W, 108, "PURE ALOHA - send any time   (vulnerable time = 2 x Tfr,  max throughput 18.4%)")
    lane(124, False)
    for xa, xb in ((38, 60), (182, 200)):
        d.add(Rect(tl + xa, 124 + 10, xb - xa, 70, fillColor=h("#f8cfc9"), strokeColor=None))
    frame(124, 0, 10, "A1", True)
    frame(124, 1, 38, "B1", True)
    frame(124, 0, 150, "A2", True)
    frame(124, 2, 182, "C1", True)
    frame(124, 1, 290, "B2", False)
    T(d, tl + 49, 138, "collision!", 7, bold=True, color=RED)
    T(d, tl + 191, 160, "collision!", 7, bold=True, color=RED)
    panel(d, 0, 2, W, 108, "SLOTTED ALOHA - send only at slot start   (vulnerable time = Tfr,  max throughput 36.8%)")
    lane(8, True)
    frame(8, 0, 0, "A1", True)
    frame(8, 1, 0, "B1", True)
    frame(8, 0, 100, "A2", False)
    frame(8, 2, 150, "C1", False)
    frame(8, 1, 250, "B2", False)
    T(d, tl + 25, 22, "collision!", 7, bold=True, color=RED)
    return d


def stop_wait():
    return seq(["SENDER", "RECEIVER"], [
        (0, 1, "Frame 0  (start timer)"),
        (1, 0, "ACK 1"),
        (0, 1, "Frame 1", "lost"),
        ("note", "timer expires - no ACK received - resend the copy"),
        (0, 1, "Frame 1  (retransmitted)"),
        (1, 0, "ACK 0"),
    ], colors_=[NAVY, TEAL])


def mac_addr():
    d = Drawing(W, 170)
    bytes_ = ["00", "1A", "2B", "3C", "4D", "5E"]
    bw, x0, y = 60, 61, 62
    for k, b in enumerate(bytes_):
        box(d, x0 + k * bw, y, bw - 4, 34, b, fill=ORANGE if k < 3 else BLUE, stroke=None, tc=WHITE, bold=True, fs=14, r=3)
        if k < 5:
            T(d, x0 + k * bw + bw - 2, y + 13, ":", 12, bold=True, color=NAVY)
    brace_h(d, x0, x0 + 3 * bw - 4, y - 4, "OUI - 24 bits  (manufacturer ID from IEEE)", color=ORANGE)
    brace_h(d, x0 + 3 * bw, x0 + 6 * bw - 4, y - 4, "NIC specific - 24 bits  (serial no.)", color=BLUE)
    T(d, W / 2, 16, "48 bits = 6 bytes = 12 hex digits    |    broadcast = FF:FF:FF:FF:FF:FF", 8, bold=True, color=NAVY)
    T(d, W / 2, 5, "written 00-1A-2B-3C-4D-5E (Windows)  or  001A.2B3C.4D5E (Cisco)", 7.3, italic=True, color=GREY)
    # zoom on first byte
    zx, zy = 252, 132
    for i in range(8):
        lab = "b%d" % (7 - i)
        f = LOR if i < 6 else (YEL if i == 6 else RED)
        box(d, zx + i * 26, zy, 25, 20, "0" if i != 6 else "0", fill=f, stroke=WHITE, bold=True, fs=8, r=1)
        T(d, zx + i * 26 + 12.5, zy + 24, lab, 6.5, color=GREY)
    T(d, zx + 6 * 26 + 12.5, zy - 9, "U/L", 7, bold=True, color=YEL)
    T(d, zx + 7 * 26 + 12.5, zy - 9, "I/G", 7, bold=True, color=RED)
    parrow(d, [x0 + 28, y + 36, x0 + 28, zy + 10, zx - 4, zy + 10], GREY, 1)
    T(d, x0 + 34, zy + 14, "zoom on the first byte", 7.5, anchor="start", bold=True, color=NAVY)
    T(d, zx, zy - 21, "b0 I/G: 0 = unicast, 1 = multicast      b1 U/L: 0 = global (burned-in), 1 = locally set", 6.8, anchor="start", color=GREY)
    return d


def bridge():
    d = Drawing(W, 185)
    yb = 110
    for x1, x2, lab in ((14, 200, "Segment 1"), (282, 468, "Segment 2")):
        line(d, x1, yb, x2, yb, NAVY, 3)
        T(d, (x1 + x2) / 2, yb + 62, lab + "  (own collision domain)", 7.5, bold=True, color=NAVY)
    for x, n in ((50, "A"), (140, "B"), (330, "C"), (420, "D")):
        line(d, x, yb, x, yb + 22, NAVY, 1)
        pc(d, x, yb + 32, "")
        T(d, x, yb + 42, n, 8, bold=True, color=NAVY)
    box(d, 200, yb - 16, 82, 32, "BRIDGE", fill=PURPLE, stroke=None, tc=WHITE, bold=True, fs=10)
    T(d, 206, yb - 26, "port 1", 7, anchor="start", bold=True, color=PURPLE)
    T(d, 276, yb - 26, "port 2", 7, anchor="end", bold=True, color=PURPLE)
    # traffic
    arrow(d, 56, yb - 8, 134, yb - 8, GREEN, 1.6)
    T(d, 95, yb - 20, "A -> B : FILTERED", 7.3, bold=True, color=GREEN)
    T(d, 95, yb - 29, "(same port, not forwarded)", 6.5, italic=True, color=GREEN)
    parrow(d, [56, yb + 6, 56, yb + 6, 186, yb + 6], ORANGE, 1.4)
    arrow(d, 296, yb - 8, 324, yb - 8, ORANGE, 1.6)
    T(d, 360, yb - 20, "A -> C : FORWARDED to port 2", 7.3, bold=True, color=ORANGE)
    # MAC table
    tx, ty = 172, 6
    box(d, tx, ty, 138, 66, "", fill=WHITE, stroke=PURPLE)
    box(d, tx, ty + 52, 138, 14, "MAC address table (learned)", fill=PURPLE, stroke=None, tc=WHITE, bold=True, fs=7.3, r=0)
    for k, (m, p) in enumerate((("A  00:1A:..:01", "port 1"), ("B  00:1A:..:02", "port 1"), ("C  00:1A:..:03", "port 2"), ("D  00:1A:..:04", "port 2"))):
        T(d, tx + 8, ty + 42 - k * 11, m, 7, anchor="start", color=INK)
        T(d, tx + 130, ty + 42 - k * 11, p, 7, anchor="end", bold=True, color=PURPLE)
    line(d, 241, yb - 16, 241, ty + 66, PURPLE, 1, dash=[2, 2])
    T(d, 14, 40, "LEARN source MAC + port", 7.3, anchor="start", bold=True, color=NAVY)
    T(d, 14, 29, "FILTER if same segment", 7.3, anchor="start", bold=True, color=NAVY)
    T(d, 14, 18, "FORWARD if known elsewhere", 7.3, anchor="start", bold=True, color=NAVY)
    T(d, 14, 7, "FLOOD if unknown / broadcast", 7.3, anchor="start", bold=True, color=NAVY)
    return d


FIGS = dict(switching=switching, media_tree=media_tree, fibre=fibre, signals=signals, mux=mux,
            fdm_tdm=fdm_tdm, adsl=adsl, dll_stack=dll_stack, csma_cd=csma_cd, aloha=aloha,
            stop_wait=stop_wait, mac_addr=mac_addr, bridge=bridge)
