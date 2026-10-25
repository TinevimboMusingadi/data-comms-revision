"""Diagrams for Topics 5-8."""
import math
from dg import *

C1, C2, C3, C4, C5 = h("#f6c9c4"), h("#fbdcb0"), h("#bfe5cf"), h("#b8d7f5"), h("#cfc8f0")


# ------------------------------------------------------------------ topic 5
def ipv4_header():
    return fields([
        (1, [("Version", 4, C1), ("IHL", 4, C1), ("DSCP / Type of Service", 8, C2), ("Total Length", 16, C3)]),
        (1, [("Identification", 16, C4), ("Flags", 3, C4), ("Fragment Offset", 13, C4)]),
        (1, [("Time to Live", 8, C5), ("Protocol", 8, C5), ("Header Checksum", 16, C2)]),
        (1, [("Source IP Address (32 bits)", 32, h("#9fd3b3"))]),
        (1, [("Destination IP Address (32 bits)", 32, h("#93c1ec"))]),
        (1, [("Options (variable)", 24, LGREY), ("Padding", 8, LGREY)]),
    ], note="20 bytes minimum (5 rows x 32 bits), 60 bytes maximum.  Blue row = used for fragmentation.")


def ipv6_header():
    return fields([
        (1, [("Version", 4, C1), ("Traffic Class", 8, C2), ("Flow Label (20 bits)", 20, C3)]),
        (1, [("Payload Length (16)", 16, C4), ("Next Header", 8, C5), ("Hop Limit", 8, C5)]),
        (2.2, [("Source Address  (128 bits)", 32, h("#9fd3b3"))]),
        (2.2, [("Destination Address  (128 bits)", 32, h("#93c1ec"))]),
    ], ruler=(0, 4, 12, 16, 24, 31), note="FIXED 40-byte header - no checksum, no fragmentation fields, no options (extension headers instead)")


def slaac():
    return seq(["HOST (new device)", "ROUTER"], [
        (0, 1, "1. Router Solicitation (RS) to FF02::2"),
        (1, 0, "2. Router Advertisement (RA): prefix 2001:DB8:1::/64, M = 0"),
        ("note", "3. Host makes its OWN interface ID (EUI-64 from MAC or random) -> 2001:DB8:1::21A:2BFF:FE3C:4D5E"),
        (0, 1, "4. DAD: Neighbour Solicitation - is anyone using this address?", "dash"),
        ("note", "no reply = address is unique and used.  No server keeps any record = STATELESS"),
    ], colors_=[NAVY, TEAL])


def dhcpv6():
    return seq(["HOST", "ROUTER", "DHCPv6 SERVER"], [
        (0, 1, "RS"),
        (1, 0, "RA: M flag = 1 (use DHCPv6)"),
        (0, 2, "SOLICIT  (to FF02::1:2)"),
        (2, 0, "ADVERTISE"),
        (0, 2, "REQUEST"),
        (2, 0, "REPLY: full address + DNS + lease"),
        ("note", "server records which host has which address = STATEFUL.  Gateway still comes from the RA"),
    ], colors_=[NAVY, TEAL, PURPLE])


def dora():
    return seq(["DHCP CLIENT", "DHCP SERVER"], [
        (0, 1, "1. DHCPDISCOVER  (broadcast 255.255.255.255) - is there a server?", "dash"),
        (1, 0, "2. DHCPOFFER  - 192.168.1.50, mask, gateway, DNS, lease time"),
        (0, 1, "3. DHCPREQUEST  (broadcast) - I accept 192.168.1.50", "dash"),
        (1, 0, "4. DHCPACK  - confirmed, lease starts"),
        ("note", "client now uses 192.168.1.50/24.  Renews at 50% of the lease.  UDP ports 67 (server) / 68 (client)"),
    ], states={0: ("IP 0.0.0.0", "UDP 67"), 3: ("192.168.1.50", "")}, colors_=[NAVY, TEAL])


# ------------------------------------------------------------------ topic 6
def rip_topo():
    d = Drawing(W, 150)
    y = 100
    box(d, 4, y - 14, 58, 28, "Net A\n10.1.0.0", fill=LGREEN, stroke=GREEN, bold=True, fs=7.5)
    box(d, W - 62, y - 14, 58, 28, "Net C\n10.3.0.0", fill=LGREEN, stroke=GREEN, bold=True, fs=7.5)
    xs = [120, 241, 362]
    line(d, 62, y, xs[0], y, NAVY, 2)
    line(d, xs[2], y, W - 62, y, NAVY, 2)
    line(d, xs[0], y, xs[2], y, NAVY, 2)
    for x, n in zip(xs, ("R1", "R2", "R3")):
        router(d, x, y, n, r=14)
    T(d, (xs[0] + xs[1]) / 2, y + 6, "Net B", 7.5, bold=True, color=GREEN)
    T(d, (xs[1] + xs[2]) / 2, y + 6, "Net D", 7.5, bold=True, color=GREEN)
    for a, b in ((xs[0], xs[1]), (xs[1], xs[2])):
        arrow(d, a + 18, y + 26, b - 18, y + 26, ORANGE, 1.2, 5, both=True, dash=[3, 2])
    T(d, W / 2, y + 36, "every 30 s each router sends its FULL table to neighbours (multicast 224.0.0.9), +1 hop per router", 7.5, bold=True, color=ORANGE)
    tx = 290
    box(d, tx, 6, 186, 62, "", fill=WHITE, stroke=NAVY)
    box(d, tx, 54, 186, 14, "R3 routing table (learned by RIP)", fill=NAVY, stroke=None, tc=WHITE, bold=True, fs=7.5, r=0)
    for k, (n, v, m) in enumerate((("Network", "via", "hops"), ("Net D", "connected", "0"), ("Net B", "R2", "1"), ("Net A", "R2", "2"))):
        b = k == 0
        T(d, tx + 10, 43 - k * 11, n, 7.3, anchor="start", bold=True if b else False)
        T(d, tx + 100, 43 - k * 11, v, 7.3, bold=b)
        T(d, tx + 170, 43 - k * 11, m, 7.3, bold=True, color=ORANGE if not b else INK)
    box(d, 4, 6, 270, 62, "Loop prevention:\nsplit horizon  -  route poisoning (metric 16)\npoison reverse  -  hold-down timers  -  triggered updates\nmax 15 hops: 16 = unreachable",
        fill=LYEL, stroke=YEL, fs=7.5)
    return d


def cwnd():
    d = Drawing(W, 200)
    ox, oy, sx, sy = 40, 26, 24.5, 6.6
    arrow(d, ox, oy, ox + 18 * sx, oy, GREY, 1, 6)
    arrow(d, ox, oy, ox, oy + 26 * sy, GREY, 1, 6)
    T(d, ox + 18 * sx, oy - 14, "time (round-trip times)", 7.5, anchor="end", color=GREY)
    VT(d, ox - 14, oy + 12 * sy, "congestion window (cwnd, segments)", 7.5, GREY)
    pts1 = [(0, 1), (1, 2), (2, 4), (3, 8), (4, 16)]
    pts2 = [(4, 16), (5, 17), (6, 18), (7, 19), (8, 20), (9, 21), (10, 22)]
    pts3 = [(10, 1), (11, 2), (12, 4), (13, 8), (13.4, 11)]
    pts4 = [(13.4, 11), (14, 11.6), (15, 12.6), (16, 13.6), (17, 14.6)]
    P = lambda L: sum([[ox + a * sx, oy + b * sy] for a, b in L], [])
    line(d, ox, oy + 16 * sy, ox + 10 * sx, oy + 16 * sy, ORANGE, 0.9, dash=[4, 3])
    T(d, ox + 4, oy + 16 * sy + 4, "ssthresh = 16", 7, anchor="start", bold=True, color=ORANGE)
    line(d, ox + 10 * sx, oy + 11 * sy, ox + 18 * sx, oy + 11 * sy, ORANGE, 0.9, dash=[4, 3])
    T(d, ox + 17.5 * sx, oy + 11 * sy - 10, "new ssthresh = 22 / 2 = 11", 7, anchor="end", bold=True, color=ORANGE)
    poly(d, P(pts1), BLUE, 2.4)
    poly(d, P(pts2), GREEN, 2.4)
    line(d, ox + 10 * sx, oy + 22 * sy, ox + 10 * sx, oy + 1 * sy, RED, 1.6, dash=[3, 2])
    poly(d, P(pts3), BLUE, 2.4)
    poly(d, P(pts4), GREEN, 2.4)
    for L, c in ((pts1, BLUE), (pts2, GREEN), (pts3, BLUE), (pts4, GREEN)):
        for a, b in L:
            d.add(Circle(ox + a * sx, oy + b * sy, 2.2, fillColor=c, strokeColor=WHITE, strokeWidth=0.5))
    xmark(d, ox + 10 * sx, oy + 22 * sy + 6, 5)
    T(d, ox + 10 * sx + 9, oy + 22 * sy + 3, "TIMEOUT (loss)", 7.5, anchor="start", bold=True, color=RED)
    T(d, ox + 1.6 * sx, oy + 9 * sy, "SLOW START", 8, bold=True, color=BLUE)
    T(d, ox + 1.6 * sx, oy + 7.5 * sy, "doubles every RTT", 7, italic=True, color=BLUE)
    T(d, ox + 6 * sx, oy + 23.5 * sy, "CONGESTION AVOIDANCE", 8, bold=True, color=GREEN)
    T(d, ox + 6 * sx, oy + 22 * sy - 2, "+1 per RTT (additive)", 7, italic=True, color=GREEN)
    T(d, ox + 12.2 * sx, oy + 4 * sy, "slow start\nagain from 1", 7, italic=True, color=BLUE, anchor="start")
    return d


def sdn():
    d = Drawing(W, 200)
    bands = [(140, "APPLICATION LAYER", LPURP, PURPLE), (76, "CONTROL LAYER", LBLUE, BLUE), (6, "INFRASTRUCTURE\n(DATA) LAYER", LTEAL, TEAL)]
    for y, t, f, c in bands:
        box(d, 4, y, W - 8, 52, "", fill=f, stroke=c)
        box(d, 4, y, 86, 52, t, fill=c, stroke=None, tc=WHITE, bold=True, fs=7.6)
    for k, a in enumerate(("Firewall app", "Load balancer", "Monitoring / QoS")):
        cbox(d, 150 + k * 112, 166, 98, 28, a, fill=WHITE, stroke=PURPLE, bold=True, fs=8)
    cbox(d, 286, 102, 250, 32, "SDN CONTROLLER  (centralised 'brain' - control plane)", fill=NAVY, stroke=None, tc=WHITE, bold=True, fs=8.5)
    for k in range(4):
        switch(d, 150 + k * 90, 34, "", w=54, inside="switch")
        line(d, 150 + k * 90, 42, 286, 86, TEAL, 0.9, dash=[3, 2])
    for k in range(3):
        line(d, 177 + k * 90, 34, 213 + k * 90, 34, NAVY, 1.5)
    T(d, 286, 12, "only forward packets (data plane)", 7.3, italic=True, color=TEAL)
    arrow(d, 470, 120, 470, 150, PURPLE, 1.6, both=True)
    T(d, 464, 132, "Northbound API (REST)", 7.3, anchor="end", bold=True, color=PURPLE)
    arrow(d, 470, 54, 470, 84, TEAL, 1.6, both=True)
    T(d, 464, 79, "Southbound API (OpenFlow)", 7.3, anchor="end", bold=True, color=TEAL)
    return d


def isp_tiers():
    d = Drawing(W, 215)
    rows = [(182, "TIER 1\nglobal backbone", NAVY), (128, "TIER 2\nregional / national", BLUE), (74, "TIER 3\nlocal access ISP", TEAL), (20, "END USERS", GREY)]
    for y, t, c in rows:
        box(d, 4, y - 16, 84, 32, t, fill=c, stroke=None, tc=WHITE, bold=True, fs=7.5)
    t1 = [(200, 182, "AT&T"), (380, 182, "NTT")]
    t2 = [(150, 128, "Liquid"), (290, 128, "Seacom"), (430, 128, "Tier 2 ISP")]
    t3 = [(130, 74, "TelOne"), (230, 74, "ZOL"), (330, 74, "Econet"), (430, 74, "Utande")]
    links = [(t1[0], t1[1]), (t1[0], t2[0]), (t1[0], t2[1]), (t1[1], t2[1]), (t1[1], t2[2]),
             (t2[0], t3[0]), (t2[0], t3[1]), (t2[1], t3[2]), (t2[2], t3[3]), (t2[1], t3[1])]
    for a, b in links:
        line(d, a[0], a[1], b[0], b[1], MGREY, 1.4)
    arrow(d, 240, 182, 340, 182, ORANGE, 1.6, 5, both=True)
    T(d, 290, 188, "peering (free)", 7.3, bold=True, color=ORANGE)
    for x, y, n in t1:
        cbox(d, x, y, 76, 24, n, fill=NAVY, stroke=None, tc=WHITE, bold=True)
    for x, y, n in t2:
        cbox(d, x, y, 76, 24, n, fill=BLUE, stroke=None, tc=WHITE, bold=True)
    for x, y, n in t3:
        cbox(d, x, y, 70, 22, n, fill=TEAL, stroke=None, tc=WHITE, bold=True)
    d.add(Circle(220, 128, 14, fillColor=ORANGE, strokeColor=WHITE))
    T(d, 220, 125.5, "IXP", 7, bold=True, color=WHITE)
    line(d, 188, 128, 206, 128, ORANGE, 1.4)
    line(d, 234, 128, 252, 128, ORANGE, 1.4)
    for k, x in enumerate((130, 230, 330, 430)):
        for dx in (-22, 0, 22):
            line(d, x, 63, x + dx, 32, MGREY, 0.8)
            pc(d, x + dx, 26, "", s=0.7)
    T(d, 300, 154, "Tier 2 buys TRANSIT from Tier 1 (pays)", 7.3, italic=True, color=GREY)
    T(d, 300, 100, "Tier 3 buys transit from Tier 2", 7.3, italic=True, color=GREY)
    return d


# ------------------------------------------------------------------ topic 7
def udp_seq():
    return seq(["HOST A  (app, port 50000)", "HOST B  (DNS server, port 53)"], [
        ("note", "NO handshake - just send"),
        (0, 1, "UDP datagram 1  [8-byte header | data]"),
        (0, 1, "UDP datagram 2", "lost"),
        (1, 0, "UDP reply datagram"),
        ("note", "no ACK, no retransmission, no ordering - the APPLICATION must cope with loss"),
    ], colors_=[NAVY, TEAL])


def udp_header():
    return fields([
        (1, [("Source Port (16)", 16, C3), ("Destination Port (16)", 16, C4)]),
        (1, [("Length (16)", 16, C2), ("Checksum (16)", 16, C1)]),
        (1.4, [("DATA (application message)", 32, LGREY)]),
    ], ruler=(0, 16, 31), note="UDP header = only 8 bytes (TCP header = 20-60 bytes)")


def tcp_reliable():
    return seq(["SENDER", "RECEIVER"], [
        (0, 1, "Seq = 1     (bytes 1-1000)"),
        (1, 0, "ACK = 1001   'send me byte 1001 next'"),
        (0, 1, "Seq = 1001  (bytes 1001-2000)", "lost"),
        (0, 1, "Seq = 2001  (bytes 2001-3000)  - buffered"),
        (1, 0, "ACK = 1001   (duplicate - still missing 1001)"),
        ("note", "timer expires / duplicate ACKs  ->  RETRANSMIT the missing segment"),
        (0, 1, "Seq = 1001  (resent)"),
        (1, 0, "ACK = 3001   all data received, in order"),
    ], colors_=[NAVY, TEAL])


def handshake():
    return seq(["CLIENT", "SERVER  (port 80)"], [
        (0, 1, "1.  SYN   seq = x"),
        (1, 0, "2.  SYN + ACK   seq = y,  ack = x + 1"),
        (0, 1, "3.  ACK   ack = y + 1"),
        ("note", "connection ESTABLISHED - full-duplex data transfer"),
        (0, 1, "FIN"),
        (1, 0, "ACK"),
        (1, 0, "FIN"),
        (0, 1, "ACK"),
    ], states={0: ("SYN-SENT", "LISTEN"), 1: ("", "SYN-RECEIVED"), 2: ("ESTABLISHED", "ESTABLISHED"),
               4: ("FIN-WAIT-1", ""), 5: ("FIN-WAIT-2", "CLOSE-WAIT"), 6: ("TIME-WAIT", "LAST-ACK"),
               7: ("", "CLOSED")}, colors_=[NAVY, TEAL])


def dns_tree():
    d = Drawing(W, 160)
    cbox(d, W / 2, 146, 60, 20, ".  (root)", fill=NAVY, stroke=None, tc=WHITE, bold=True)
    tl = [(110, ".com"), (W / 2, ".zw"), (W - 110, ".org")]
    for x, n in tl:
        line(d, W / 2, 136, x, 112, NAVY, 1)
        cbox(d, x, 104, 64, 18, n, fill=BLUE, stroke=None, tc=WHITE, bold=True)
    for x, n in ((W / 2 - 60, ".ac.zw"), (W / 2 + 60, ".co.zw")):
        line(d, W / 2, 95, x, 76, BLUE, 1)
        cbox(d, x, 68, 64, 18, n, fill=TEAL, stroke=None, tc=WHITE, bold=True)
    line(d, W / 2 - 60, 59, W / 2 - 60, 46, TEAL, 1)
    cbox(d, W / 2 - 60, 38, 80, 18, "hit.ac.zw", fill=ORANGE, stroke=None, tc=WHITE, bold=True)
    line(d, W / 2 - 60, 29, W / 2 - 60, 20, ORANGE, 1)
    cbox(d, W / 2 - 60, 12, 160, 18, "www.hit.ac.zw  ->  A record (IP)", fill=LOR, stroke=ORANGE, bold=True, fs=7.6)
    for y, t, c in ((146, "ROOT servers", NAVY), (104, "TLD servers", BLUE), (68, "second level", TEAL), (38, "AUTHORITATIVE server", ORANGE)):
        T(d, 4, y - 3, t, 7.5, anchor="start", bold=True, color=c)
    return d


def dns_lookup():
    d = Drawing(W, 205)
    pc(d, 30, 116, "", s=1.4)
    T(d, 30, 88, "CLIENT", 8, bold=True, color=NAVY)
    T(d, 30, 78, "(stub resolver)", 7, color=GREY)
    box(d, 150, 30, 96, 170, "", fill=NAVY, stroke=None)
    T(d, 198, 124, "LOCAL / ISP\nRECURSIVE\nRESOLVER", 8.5, bold=True, color=WHITE)
    T(d, 198, 80, "caches the answer\nfor its TTL", 7, italic=True, color=h("#c9d8ea"))
    arrow(d, 52, 124, 148, 124, GREEN, 1.6)
    T(d, 100, 129, "1. www.hit.ac.zw ?", 7.3, bold=True, color=GREEN)
    arrow(d, 148, 104, 52, 104, GREEN, 1.6)
    T(d, 100, 92, "8. answer 196.x.x.x", 7.3, bold=True, color=GREEN)
    T(d, 100, 60, "RECURSIVE query:", 7.3, bold=True, color=GREEN)
    T(d, 100, 50, "'you do the work, give", 7, italic=True, color=GREEN)
    T(d, 100, 41, "me the final answer'", 7, italic=True, color=GREEN)
    srv = [(176, "ROOT server", NAVY, "2. where is www.hit.ac.zw?", "3. referral: ask the .zw TLD"),
           (116, ".zw TLD server", BLUE, "4. where is www.hit.ac.zw?", "5. referral: ask hit.ac.zw NS"),
           (56, "hit.ac.zw AUTHORITATIVE", ORANGE, "6. where is www.hit.ac.zw?", "7. A record = 196.x.x.x")]
    for y, n, c, q, a in srv:
        cbox(d, 412, y, 132, 34, n, fill=c, stroke=None, tc=WHITE, bold=True, fs=8)
        arrow(d, 248, y + 7, 344, y + 7, BLUE, 1.3)
        T(d, 296, y + 12, q, 6.8, bold=True, color=BLUE)
        arrow(d, 344, y - 7, 248, y - 7, TEAL, 1.3, dash=[3, 2])
        T(d, 296, y - 18, a, 6.8, bold=True, color=TEAL)
    T(d, 330, 12, "resolver -> each server = ITERATIVE queries (server replies with a referral, not the answer)", 7, italic=True, color=GREY)
    return d


# ------------------------------------------------------------------ topic 8
def crypto():
    d = Drawing(W, 190)
    for y0, title, col, ek, dk, kc1, kc2 in (
            (100, "SYMMETRIC (secret key) - DES, 3DES, AES", BLUE, "same key K", "same key K", ORANGE, ORANGE),
            (6, "ASYMMETRIC (public key) - RSA, ECC", PURPLE, "Bob's PUBLIC key", "Bob's PRIVATE key", GREEN, RED)):
        panel(d, 0, y0, W, 84, title, tfill=col)
        yc = y0 + 32
        cbox(d, 48, yc, 76, 26, "Plaintext\n'Hello'", fill=WHITE, stroke=GREY, bold=True, fs=7.6)
        cbox(d, 150, yc, 76, 26, "ENCRYPT", fill=col, stroke=None, tc=WHITE, bold=True)
        cbox(d, W / 2 + 10, yc, 86, 26, "Ciphertext\n'x9#Lq2'", fill=LGREY, stroke=GREY, bold=True, fs=7.6)
        cbox(d, W - 150, yc, 76, 26, "DECRYPT", fill=col, stroke=None, tc=WHITE, bold=True)
        cbox(d, W - 48, yc, 76, 26, "Plaintext\n'Hello'", fill=WHITE, stroke=GREY, bold=True, fs=7.6)
        for a, b in ((86, 112), (188, W / 2 - 33), (W / 2 + 53, W - 188), (W - 112, W - 86)):
            arrow(d, a, yc, b, yc, NAVY, 1.4, 5)
        key(d, 136, yc + 26, kc1, 0.8)
        T(d, 158, yc + 23, ek, 7, anchor="start", bold=True, color=kc1)
        key(d, W - 164, yc + 26, kc2, 0.8)
        T(d, W - 142, yc + 23, dk, 7, anchor="start", bold=True, color=kc2)
        T(d, W / 2 + 10, yc - 20, "travels over the network", 6.8, italic=True, color=GREY)
    T(d, W / 2, 96, "", 6)
    return d


def vpn():
    d = Drawing(W, 175)
    pc(d, 34, 110, "", s=1.4)
    T(d, 34, 82, "Remote user", 7.5, bold=True, color=NAVY)
    T(d, 34, 72, "+ VPN client", 7, color=GREY)
    cloud(d, W / 2 - 10, 112, 260, 96, "", fill=h("#eef4fb"), stroke=MGREY)
    T(d, W / 2 - 10, 150, "PUBLIC INTERNET (untrusted)", 8, bold=True, color=GREY)
    d.add(Rect(62, 100, 300, 22, rx=11, ry=11, fillColor=h("#bfe8cd"), strokeColor=GREEN, strokeWidth=1.5))
    T(d, 212, 108, "ENCRYPTED TUNNEL (IPsec / SSL-TLS)", 8, bold=True, color=GREEN)
    lock(d, 90, 111, GREEN, 0.9)
    lock(d, 335, 111, GREEN, 0.9)
    firewall(d, 384, 111, "", w=30, hh=24)
    T(d, 384, 88, "VPN gateway", 7, bold=True, color=NAVY)
    switch(d, 432, 111, "", w=30, inside="SW")
    server(d, 466, 138, "")
    pc(d, 466, 92, "", s=0.8)
    line(d, 447, 111, 457, 132, NAVY, 0.8)
    line(d, 447, 111, 458, 96, NAVY, 0.8)
    T(d, 448, 72, "Company LAN", 7.5, bold=True, color=NAVY)
    # packet structure
    y = 16
    T(d, 4, y + 30, "Tunnel packet:", 7.5, anchor="start", bold=True, color=NAVY)
    parts = [("NEW IP header\n(to VPN gateway)", 92, LGREY), ("ESP\nheader", 46, LOR),
             ("ENCRYPTED original packet\n(original IP header + data)", 214, h("#bfe8cd")), ("ESP trailer\n+ auth", 66, LOR)]
    x = 34
    for t, w, f in parts:
        box(d, x, y, w, 26, t, fill=f, stroke=WHITE, sw=1.5, r=1, bold=True, fs=7.2)
        x += w
    return d


FIGS = dict(ipv4_header=ipv4_header, ipv6_header=ipv6_header, slaac=slaac, dhcpv6=dhcpv6, dora=dora,
            rip_topo=rip_topo, cwnd=cwnd, sdn=sdn, isp_tiers=isp_tiers, udp_seq=udp_seq,
            udp_header=udp_header, tcp_reliable=tcp_reliable, handshake=handshake, dns_tree=dns_tree,
            dns_lookup=dns_lookup, crypto=crypto, vpn=vpn)
