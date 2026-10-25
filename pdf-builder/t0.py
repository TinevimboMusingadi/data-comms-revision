TITLE = "ISS 2103 Data Communications & Networks - Exam Map"
SUB = "Built from the course outline (ISE 2103, Mr S. Murove) and 5 past papers: ISS222 May/Jun 2018, ICS/ISE2103 Nov/Dec 2023, ISE2103 Nov/Dec 2024 (SE2024), ISS2103 Nov/Dec 2024 (ISA2024), ISS2103 Nov/Dec 2025. Start here."
FILE = "00_Exam_Map_START_HERE.pdf"

C = [
("h", "Exam format (same every year)"),
("b", [
 "**3 hours, 100 marks. FIVE questions of 25 marks - answer any FOUR.** Start each question on a fresh page.",
 "That is **45 minutes per question** - roughly **1.8 minutes per mark**. Leave 10 minutes to check.",
 "Read all 5 questions first; drop the one with the most parts you can't do. Do your strongest question first.",
 "Questions mix topics - a single question can have OSI, subnetting and CSMA/CD - so you must cover all topics, not just 4.",
]),

("h", "Your revision packs"),
("t", [
 ["PDF", "Topic", "Outline weeks", "Priority"],
 ["01", "Fundamentals: components, transmission modes, LAN/MAN/WAN, topologies, client-server, protocols", "1-2", "HIGH"],
 ["02", "OSI & TCP/IP models, IP vs MAC, internetworking", "1-2, 5-9", "VERY HIGH"],
 ["03", "Physical layer: media, fibre, signals, impairments, modulation, multiplexing, switching, ADSL", "1-2", "HIGH"],
 ["04", "Data link & MAC: LLC/MAC, CSMA/CD/CA, ALOHA, error detection, flow control, MAC address, bridges, switches, VLANs", "3-4", "VERY HIGH"],
 ["05", "Network layer: IPv4 classes, SUBNETTING/VLSM, IPv4 & IPv6 headers, IPv6, SLAAC vs DHCPv6, DHCP", "5-7", "VERY HIGH"],
 ["06", "Routing (RIP, EIGRP, OSPF), congestion control, QoS, SDN, ISPs, SLA, WAN protocols", "5-7", "HIGH"],
 ["07", "Transport & application: TCP vs UDP, handshake, DNS, troubleshooting, RPC, compression, FTP, email", "8-11", "MEDIUM-HIGH"],
 ["08", "Security & emerging tech: threats, malware, DES vs AES, KDC, CA, VPN", "8-9, 12", "MEDIUM"],
]),

("h", "Where every past question falls (topic x paper)"),
("t", [
 ["Topic", "2018", "2023", "SE 2024", "ISA 2024", "2025"],
 ["01 Fundamentals", "Q1a, Q1c", "Q4e", "Q1a, Q2e-f, Q3d-e, Q4a-b, Q4d-e, Q5c-d", "Q2c, Q3b", "Q1b, Q2a, Q2c"],
 ["02 OSI / TCP-IP", "Q5b", "Q1c", "Q1e, Q3b", "Q3c", "Q1a, Q5a, Q5c"],
 ["03 Physical / switching", "-", "Q1e, Q3a-b, Q5b", "Q1b, Q1d, Q2a, Q2c, Q3c, Q4c, Q5b", "Q2d, Q5b", "Q2b, Q3a"],
 ["04 Data link / MAC", "Q1b, Q3b, Q4b, Q4d, Q5c-d", "Q4a-b, Q5a", "Q1b.ii, Q2b, Q3a, Q4f", "Q1b-c, Q4a, Q4c", "Q4c, Q5b, Q5d"],
 ["05 IP / subnetting / IPv6", "Q1d, Q3a, Q4a", "Q1a-b, Q1d, Q3c, Q5e", "Q1b.iv", "Q1a, Q1d, Q2b, Q3a, Q5d", "Q3b, Q4a-b"],
 ["06 Routing / QoS / WAN", "Q4c", "Q2a-e, Q3d-e, Q5d", "Q1c", "Q4b, Q4d, Q5c", "Q3c"],
 ["07 Transport / application", "Q2a-c, Q3c, Q5a", "Q5c", "Q5e", "Q5a", "-"],
 ["08 Security", "-", "Q4c-d", "Q2d, Q5a", "Q2a", "-"],
]),
("tip", "Your paper is the **ISS (Information Security & Assurance)** version - the ISA2024 and 2025 papers are the closest to what you will get. They are heavy on OSI, subnetting, switching, CSMA/CD, LLC/MAC, IPv6/SLAAC, routing and congestion."),

("h", "Most repeated questions - the 'bankers'"),
("t", [
 ["#", "Question", "Times seen", "Pack"],
 ["1", "Subnetting / VLSM calculation", "5 of 5 papers (7 parts)", "05"],
 ["2", "OSI layers + functions (often with diagram); OSI vs TCP/IP", "5 of 5", "02"],
 ["3", "Network topologies (describe 3-4; ring vs bus)", "3 papers", "01"],
 ["4", "Circuit vs packet (vs message) switching + examples", "4 papers", "03"],
 ["5", "CSMA/CD (and CSMA/CD vs CSMA/CA)", "4 papers", "04"],
 ["6", "TCP vs UDP / how UDP sends data / why TCP reliable", "5 papers", "07"],
 ["7", "IPv4 header fields (TTL, protocol, version, DS, addresses)", "2 papers", "05"],
 ["8", "IPv6: shorten addresses; advantages; header", "3 papers", "05"],
 ["9", "SLAAC vs DHCPv6", "2 papers (the last two!)", "05"],
 ["10", "LLC and MAC sub-layers", "2 papers", "04"],
 ["11", "Transmission media types; fibre optic", "4 papers", "03"],
 ["12", "Error detection (parity, CRC, checksum; single-bit vs burst)", "2 papers", "04"],
 ["13", "Client-server vs P2P", "2 papers", "01"],
 ["14", "Routing: DV vs LS, RIP/RIPv2/EIGRP/OSPF", "2 papers", "06"],
 ["15", "Multiplexing (concept, FDM vs TDM)", "2 papers", "03"],
 ["16", "LAN/MAN/WAN; categories of networks", "2 papers", "01"],
]),

("h", "Likely 'new' questions (in the outline but not yet asked much)"),
("b", [
 "Sliding window protocols (Go-Back-N vs Selective Repeat) - Pack 04.",
 "FDDI, IEEE 802 standards overview, channel allocation - Pack 04.",
 "Remote Procedure Call; data compression techniques; session layer design issues - Pack 07.",
 "FTP, email protocols (SMTP/POP3/IMAP), virtual terminals - Pack 07.",
 "ISDN; terminal handling; backbone & local-access network design - Packs 03 & 01.",
 "Emerging technologies (5G, IoT, cloud, SDN) - Pack 08.",
 "Lab content: network commands (ipconfig, ping, tracert, netstat), straight-through vs crossover cables, Packet Tracer - Pack 07.",
]),

("h", "How to write answers that score"),
("t", [
 ["Command word", "What the examiner wants"],
 ["List / state / name", "Short points only, one per mark"],
 ["Define / explain the term", "Clear definition + one example (or how it works)"],
 ["Describe / explain", "Definition + how it works step by step + example; a diagram earns marks"],
 ["Differentiate / distinguish / compare", "A **table** with matching rows (e.g. 4 rows for 4 marks); 'compare' also wants similarities"],
 ["With the aid of a diagram", "The diagram must be **labelled** - usually ~half the marks"],
 ["Calculate / show working", "Show every step: binary mask, borrowed bits, block size, then a results table"],
 ["Discuss", "Several points, each explained, with advantages/disadvantages or examples"],
]),

("h", "One-page last-minute facts"),
("pre", """
 OSI 7->1: Application, Presentation, Session, Transport, Network, Data Link, Physical
           (All People Seem To Need Data Processing)
 PDUs: data / segment / packet / frame / bits      Devices: L1 hub+repeater, L2 switch+bridge, L3 router
 Delivery: L2 hop-to-hop (MAC), L3 host-to-host (IP), L4 process-to-process (port)
 TCP/IP: Application | Transport | Internet | Network Access

 Hosts = 2^h - 2   Subnets = 2^borrowed   Block = 256 - mask octet
 /24 254  /25 126  /26 62  /27 30  /28 14  /29 6  /30 2
 Class A 1-126 /8, B 128-191 /16, C 192-223 /24.  Private: 10/8, 172.16-31, 192.168/16
 IPv4 header 20 B (TTL, Protocol 6=TCP 17=UDP 1=ICMP).  IPv6: 128-bit, header 40 B, hop limit, flow label
 IPv6 shorten: drop leading zeros, '::' once for the longest zero run
 SLAAC: host builds address from RA prefix (stateless).  DHCPv6: server assigns & tracks (stateful)
 DHCP: Discover, Offer, Request, Ack (UDP 67/68)

 CSMA/CD wired (detect, jam, backoff) vs CSMA/CA wireless (avoid, RTS/CTS, ACK)
 Pure ALOHA 18.4% (vulnerable 2T), Slotted ALOHA 36.8% (vulnerable T)
 Errors: single-bit -> parity; burst -> CRC; checksum in IP/TCP/UDP.  FEC = receiver corrects (Hamming)
 Hamming distance = number of differing bits; detect s: d=s+1; correct t: d=2t+1
 MAC = 48-bit: 24-bit OUI + 24-bit NIC.  ARP: IP -> MAC (broadcast request, unicast reply)

 Circuit = dedicated path (phone, ISDN). Packet = shared, independent packets (IP, X.25, Frame Relay)
 FDM = frequency bands (analogue), TDM = time slots (digital), WDM = light wavelengths
 Media: twisted pair, coax, fibre (guided) | radio, microwave, infrared (unguided)
 Impairments: attenuation, distortion, noise

 RIP: DV, hop count (max 15), 30 s updates, v2 = classless + multicast 224.0.0.9 + auth
 EIGRP: advanced DV, DUAL, bandwidth+delay, successor/feasible successor.  OSPF: LS, Dijkstra, cost
 QoS: bandwidth, latency, jitter, packet loss.  VoIP: <150 ms, <30 ms jitter, <1% loss
 TCP: SYN -> SYN/ACK -> ACK.  UDP: 8-byte header, no connection, no ACK.  DNS UDP 53
 DES 56-bit key 64-bit block 16 rounds; AES 128/192/256-bit key 128-bit block 10/12/14 rounds
"""),
]
