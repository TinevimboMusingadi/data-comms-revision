import sys, importlib, os
import render

# (pack, index of its n-th "pre" block) -> graphics that replace that text diagram
FIGMAP = {
    ("t1", 0): [("components", "the 5 components of a data communication system")],
    ("t1", 1): [("topologies", "the six network topologies")],
    ("t1", 2): [("building", "network design for a 5-floor building, 20 PCs per floor")],
    ("t2", 0): [("osi_peer", "the OSI model - peer layers, PDUs and encapsulation"),
                ("encapsulation", "encapsulation - each layer adds its header")],
    ("t2", 1): [("osi_tcpip", "OSI layers mapped to the TCP/IP model")],
    ("t3", 0): [("switching", "circuit vs message vs packet switching")],
    ("t3", 1): [("media_tree", "classification of transmission media")],
    ("t3", 2): [("fibre", "how light travels through a fibre optic cable")],
    ("t3", 3): [("signals", "analogue vs digital signals")],
    ("t3", 4): [("mux", "multiplexer and demultiplexer sharing one link")],
    ("t3", 5): [("fdm_tdm", "FDM vs TDM")],
    ("t3", 6): [("adsl", "ADSL frequency bands and splitters")],
    ("t4", 0): [("dll_stack", "the two sub-layers of the data link layer")],
    ("t4", 1): [("csma_cd", "CSMA/CD flowchart (and what a collision looks like)")],
    ("t4", 2): [("aloha", "pure ALOHA vs slotted ALOHA")],
    ("t4", 4): [("stop_wait", "stop-and-wait ARQ with a lost frame")],
    ("t4", 5): [("mac_addr", "structure of a 48-bit MAC address")],
    ("t4", 6): [("bridge", "a learning bridge filtering and forwarding frames")],
    ("t5", 6): [("ipv4_header", "the IPv4 header")],
    ("t5", 8): [("ipv6_header", "the IPv6 header (40 bytes)")],
    ("t5", 9): [("slaac", "SLAAC - the host builds its own address"),
                ("dhcpv6", "stateful DHCPv6 - the server assigns and records the address")],
    ("t5", 10): [("dora", "DHCP DORA process")],
    ("t6", 0): [("rip_topo", "RIP: hop counts, updates and loop prevention")],
    ("t6", 1): [("cwnd", "TCP congestion control - slow start, AIMD and timeout")],
    ("t6", 2): [("sdn", "SDN architecture")],
    ("t6", 3): [("isp_tiers", "hierarchical structure of the Internet")],
    ("t7", 0): [("udp_seq", "UDP: connectionless transmission"), ("udp_header", "the 8-byte UDP header")],
    ("t7", 1): [("tcp_reliable", "how TCP recovers a lost segment")],
    ("t7", 2): [("handshake", "TCP 3-way handshake and 4-way close with connection states")],
    ("t7", 3): [("dns_tree", "the DNS hierarchy"), ("dns_lookup", "a recursive DNS lookup step by step")],
    ("t8", 0): [("crypto", "symmetric vs asymmetric encryption")],
    ("t8", 1): [("vpn", "how a VPN tunnel works")],
}

OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)
for name in sys.argv[2:]:
    m = importlib.import_module(name)
    content, k = [], 0
    for item in m.C:
        if item[0] == "pre":
            figs = FIGMAP.get((name, k))
            k += 1
            if figs:
                content += [("fig", f, cap) for f, cap in figs]
                continue
        content.append(item)
    render.build(os.path.join(OUT, m.FILE), m.TITLE, m.SUB, content)
    print("built", m.FILE)
