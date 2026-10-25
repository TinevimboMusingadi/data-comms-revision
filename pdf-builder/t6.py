TITLE = "Topic 6: Routing, Congestion Control, QoS & WANs"
SUB = "Course outline weeks 5-7: point-to-point networks, routing, congestion control, internetworking; plus SLA, SDN and Internet structure. Big-mark questions (6-10 marks)."
FILE = "06_Routing_Congestion_QoS_WAN.pdf"

C = [
("h", "How often this topic is examined"),
("t", [
 ["Question asked", "Paper(s)", "Marks"],
 ["Sources of routing-table information", "2023 Q2a", "3"],
 ["Link-state vs distance-vector (table)", "2023 Q2b", "6"],
 ["Complete table: RIPv1 / EIGRP / OSPF - type & metric", "2023 Q2c", "6"],
 ["How EIGRP works and selects the best path", "2023 Q2d", "5"],
 ["How RIPv2 works", "ISA2024 Q5c", "6"],
 ["Congestion control + two mechanisms", "2025 Q3c", "10"],
 ["QoS: VoIP vs video; QoS parameters; 'best effort network'", "2023 Q2e [5], Q3e [6], Q3d [4]", "4-6"],
 ["Network performance optimisation scenario", "ISA2024 Q4d", "7"],
 ["Software-defined networking (SDN)", "ISA2024 Q4b", "5"],
 ["Hierarchical structure of the Internet (ISPs)", "2018 Q4c", "6"],
 ["SLA - purpose & contents", "2023 Q5d", "3"],
 ["Two WAN protocols", "SE2024 Q1c", "2"],
]),

("h", "1. Routing basics"),
("p", "**Routing** is the process by which a **router** selects the **best path** for a packet from the source network to the destination network, using the destination IP address and its **routing table** (network/prefix, next hop, outgoing interface, metric, administrative distance)."),
("q", "Natalie has forgotten how routing tables work. Describe three different sources a router can use to put/maintain information in a routing table.", "2023 Q2a", "3"),
("n", [
 "**Directly connected networks** - when an interface is configured with an IP address and is up, the router automatically adds that network (code **C** in Cisco).",
 "**Static routes** - manually entered by the administrator (`ip route 10.0.0.0 255.0.0.0 192.168.1.2`), code **S**. Includes the **default route** (0.0.0.0/0) for 'everything else', e.g. towards the ISP.",
 "**Dynamic routing protocols** - routers learn routes automatically by exchanging updates with neighbours using **RIP (R), OSPF (O), EIGRP (D)**, BGP; they adapt when the topology changes.",
]),
("p", "When several sources offer the same route, the router prefers the lowest **administrative distance**: connected 0, static 1, EIGRP 90, OSPF 110, RIP 120."),

("h", "2. Distance vector vs link state"),
("q", "Tabulate at least three main differences between link-state and distance-vector routing protocols.", "2023 Q2b", "6"),
("t", [
 ["Distance vector", "Link state"],
 ["Router knows only **distance (metric) and direction (next hop)** to each network - 'routing by rumour'", "Every router builds a **complete map (topology) of the network** and calculates paths itself"],
 ["Sends its **whole routing table periodically** (e.g. RIP every 30 s) to **directly connected neighbours** only", "Sends small **Link-State Advertisements (LSAs)** to **all routers** (flooding) only **when a change occurs** (+ hellos)"],
 ["Algorithm: **Bellman-Ford**", "Algorithm: **Dijkstra's Shortest Path First (SPF)**"],
 ["**Slow convergence**; prone to **routing loops** / count-to-infinity (needs split horizon, poison reverse, hold-down)", "**Fast convergence**, loop-free"],
 ["Simple, low CPU & memory", "Needs more CPU and memory (LSDB, SPF calculations)"],
 ["Suitable for small, simple networks", "Scales to large hierarchical networks (areas)"],
 ["Examples: **RIPv1, RIPv2**, IGRP (EIGRP = advanced DV)", "Examples: **OSPF, IS-IS**"],
]),
("q", "Copy and complete the table: Routing protocol | Distance-vector or link-state? | Metric used.", "2023 Q2c", "6"),
("t", [
 ["Routing protocol", "Distance-vector or Link-state?", "Metric used"],
 ["RIPv1", "Distance-vector (classful)", "**Hop count** (max 15; 16 = unreachable)"],
 ["EIGRP", "**Advanced distance-vector** (also called hybrid)", "**Composite metric**: bandwidth and delay by default (can include load and reliability)"],
 ["OSPF", "Link-state", "**Cost** - based on bandwidth (cost = reference bandwidth 100 Mbps / interface bandwidth)"],
]),

("h", "3. EIGRP"),
("q", "Describe the workings of the EIGRP routing protocol, clearly highlighting how it selects the best path for transmission of packets.", "2023 Q2d", "5"),
("b", [
 "**Enhanced Interior Gateway Routing Protocol** - Cisco-developed **advanced distance-vector** protocol (published as RFC 7868); classless (supports VLSM/CIDR); administrative distance 90.",
 "**Neighbour discovery:** sends **Hello** packets (multicast 224.0.0.10) to form adjacencies with neighbours; uses RTP (Reliable Transport Protocol) for reliable updates.",
 "**Three tables:** **neighbour table**, **topology table** (all routes learned from all neighbours), **routing table** (best routes).",
 "**Partial, bounded updates** - only sends changes, only to routers that need them (not periodic full tables) -> low bandwidth use.",
 "**Metric:** composite of **bandwidth (slowest link on the path) + delay (sum of delays)** by default; formula metric = 256 x (10^7 / slowest bandwidth in kbps + total delay in tens of microseconds). Lowest metric = best.",
 "**Best-path selection with DUAL (Diffusing Update Algorithm):** for every destination the route with the **lowest Feasible Distance (FD)** becomes the **Successor** and is put in the routing table. A backup route whose **Reported (Advertised) Distance < FD of the successor** (the *feasibility condition*) becomes the **Feasible Successor**, kept in the topology table.",
 "If the successor fails, the feasible successor is used **immediately** - very **fast convergence, loop-free**. If none exists, the router sends queries to neighbours.",
 "Supports equal and **unequal-cost load balancing** (variance command).",
]),

("h", "4. RIP version 2"),
("q", "Explain in detail the working of the RIP v2 routing algorithm.", "ISA2024 Q5c", "6"),
("b", [
 "**Routing Information Protocol v2** - a **distance-vector** protocol using the **Bellman-Ford** algorithm; metric = **hop count**; maximum **15 hops** (16 = unreachable) so suits small networks. AD 120, runs over **UDP port 520**.",
 "Each router starts with its directly connected networks, then **every 30 seconds** sends its **entire routing table** to neighbours using **multicast 224.0.0.9** (RIPv1 used broadcast).",
 "When a router receives an update it adds **1 hop** to each route; if the route is new or better (fewer hops) it updates its table with the neighbour as next hop.",
 "**Improvements over RIPv1:** **classless** - sends the **subnet mask** with each route (supports VLSM & CIDR); **authentication** (plain text / MD5); **next-hop** field; **route tags**; multicast updates.",
 "**Timers:** update 30 s; invalid 180 s (route marked unreachable if not heard); hold-down 180 s; flush 240 s (removed).",
 "**Loop prevention:** **split horizon** (don't advertise a route back out the interface it was learned on), **route poisoning** (advertise failed route with metric 16), **poison reverse**, **hold-down timers**, **triggered updates** (send immediately on change).",
 "Disadvantages: slow convergence, hop count ignores bandwidth, periodic updates waste bandwidth.",
]),
("pre", """
  [Net A]--R1------R2------R3--[Net C]       R3's table learned via RIP:
                                               Net A  via R2  metric 2 hops
                                               Net B  via R2  metric 1 hop
"""),

("h", "5. Congestion control"),
("q", "A network is experiencing a high volume of traffic, leading to delays and dropped packets. Explain the concept of congestion control and describe at least two mechanisms used to manage network congestion.", "2025 Q3c", "10"),
("p", "**Congestion** occurs when the **load (number of packets) offered to the network exceeds its capacity** - router buffers/queues fill up, causing long **delays**, **packet loss** and retransmissions that make it even worse (congestion collapse). **Congestion control** is the set of techniques that **prevent congestion or remove it** once it happens, keeping the load below capacity."),
("h3", "A. Open-loop (prevention) policies"),
("b", [
 "**Retransmission policy** - good timers so senders don't retransmit too early.",
 "**Window policy** - Selective Repeat instead of Go-Back-N (fewer duplicates).",
 "**Acknowledgement policy** - cumulative/delayed ACKs reduce extra traffic.",
 "**Discard policy** - routers drop less important packets first (e.g. in audio).",
 "**Admission control** - a new flow/virtual circuit is refused if the network cannot support it (used in QoS, ATM).",
 "**Traffic shaping** - **Leaky bucket**: packets leave at a constant rate regardless of bursts (smooths traffic; overflow dropped). **Token bucket**: tokens added at a fixed rate; a packet needs a token to be sent, allowing controlled bursts.",
]),
("h3", "B. Closed-loop (removal) mechanisms"),
("b", [
 "**Backpressure** - a congested node stops accepting packets from upstream nodes, which in turn slow down, back to the source.",
 "**Choke packet** - the congested router sends a special packet directly to the source telling it to slow down (e.g. ICMP source quench).",
 "**Implicit signalling** - the source infers congestion from missing ACKs / delay (TCP).",
 "**Explicit signalling** - routers mark packets (**ECN** bits in IP header, Frame Relay FECN/BECN) to tell sender/receiver.",
 "**Random Early Detection (RED)** - router drops/marks packets randomly before the queue is full so TCP senders slow down early.",
]),
("h3", "C. TCP congestion control"),
("b", [
 "**Slow start** - congestion window (cwnd) starts at 1 MSS and **doubles each RTT** (exponential) until the threshold (ssthresh).",
 "**Congestion avoidance (AIMD)** - after the threshold cwnd grows by 1 MSS per RTT (additive increase).",
 "**On loss**: timeout -> ssthresh = cwnd/2, cwnd = 1 (back to slow start); 3 duplicate ACKs -> **fast retransmit & fast recovery** (cwnd halved - multiplicative decrease).",
]),
("pre", """
 cwnd ^                         x timeout
      |                  _____/|            ssthresh halved
      |            _____/      |          /
      |       ____/ (additive) |     ____/
      |     /   congestion      |   /
      |   /  avoidance          |  / slow start again
      | / slow start (x2/RTT)   | /
      +---------------------------------------------> time (RTTs)
"""),
("tip", "For 10 marks: define congestion + causes (2), define congestion control (1), then explain 2-3 mechanisms in detail (leaky/token bucket, choke packet, TCP slow start) with a diagram (6-7)."),

("h", "6. Quality of Service (QoS)"),
("q", "The Internet is often described as a 'best effort network'. Explain what is meant by this term.", "2023 Q3d", "4"),
("p", "In a **best-effort network** the network **tries its best to deliver every packet but gives no guarantees**: no guarantee of delivery, of delivery time (delay), of bandwidth, of order or of no duplication. All packets are treated **equally** (first-come-first-served); when routers are congested packets are simply **dropped**. IP is best-effort and connectionless - reliability, if needed, is provided by the end hosts (TCP). Advantage: simple, cheap and scalable; disadvantage: unpredictable performance for real-time applications, which is why QoS mechanisms (DiffServ, IntServ/RSVP, MPLS) were added."),
("q", "List three QoS parameters that are often measured to characterise the behaviour of a network or network connection.", "2023 Q3e", "6"),
("b", [
 "**Bandwidth / throughput** - the amount of data successfully transferred per second (bps).",
 "**Latency (delay)** - time for a packet to travel from source to destination (propagation + transmission + queuing + processing).",
 "**Jitter** - **variation in delay** between packets of the same flow; harms real-time audio/video.",
 "**Packet loss** - percentage of packets that never arrive (caused by congestion/errors).",
 "(Also reliability/error rate and availability.)",
]),
("q", "Discuss the quality-of-service requirements of a VoIP application and how they differ from those of a video-based application.", "2023 Q2e", "5"),
("t", [
 ["Parameter", "VoIP (voice)", "Video application"],
 ["Bandwidth", "**Low** - ~30-100 kbps per call (G.711 ~87 kbps, G.729 ~30 kbps)", "**High** - 1-25 Mbps (HD/4K), bursty"],
 ["Latency", "Very sensitive: one-way delay < **150 ms**", "Streaming (YouTube/Netflix) tolerant - **buffering** hides delay (seconds); video conferencing needs < 150-200 ms like voice"],
 ["Jitter", "Must be low (< **30 ms**); jitter buffers used", "Streaming tolerant (buffer); conferencing sensitive"],
 ["Packet loss", "< **1%**; lost packets are not retransmitted (UDP/RTP)", "Sensitive (< 0.1-1%) - loss causes pixelation/freezing"],
 ["Traffic pattern", "Smooth, constant small packets, interactive two-way", "Large packets, variable rate, mostly one-way (streaming)"],
 ["QoS treatment", "Highest priority (DSCP EF 46), priority/low-latency queuing", "Lower priority (AF41 conferencing, AF31 streaming)"],
]),
("q", "A large enterprise network is experiencing slow data transfer rates, high latency and frequent packet losses. Describe network performance optimisation and how you would achieve it to improve efficiency, speed and reliability.", "ISA2024 Q4d", "7"),
("p", "**Network performance optimisation** = monitoring, analysing and tuning the network (hardware, configuration and traffic) so that it delivers the maximum throughput with the minimum latency, jitter and loss for business applications."),
("n", [
 "**Monitor & baseline** - use SNMP/NetFlow tools (PRTG, Wireshark, SolarWinds) to find bottlenecks, top talkers, error counters, overloaded links.",
 "**Upgrade bandwidth & hardware** - faster links (1 -> 10 Gbps), replace hubs with switches, upgrade old routers/NICs and faulty cables (fixes CRC errors & loss).",
 "**Segment the network** - VLANs/subnetting to reduce broadcast traffic and collision domains.",
 "**Implement QoS** - classify and prioritise critical traffic (VoIP, ERP) over bulk downloads; traffic shaping/policing.",
 "**Load balancing & redundancy** - multiple links (EtherChannel), redundant routers (HSRP), dynamic routing (OSPF/EIGRP) for fast failover -> reliability.",
 "**Caching, CDN & WAN optimisation** - proxy caches, compression, deduplication; move apps closer to users.",
 "**Security hygiene** - block malware/broadcast storms, unauthorised streaming with firewall policies; keep firmware updated; document and review regularly.",
]),

("h", "7. Software-Defined Networking (SDN)"),
("q", "Elaborate on software-defined networking (SDN).", "ISA2024 Q4b", "5"),
("pre", """
     +-----------------------------------------------+
     |  APPLICATION LAYER  (firewall, load balancer, |
     |                      monitoring apps)          |
     +-------------------- Northbound API (REST) -----+
     |  CONTROL LAYER  = SDN CONTROLLER (centralised  |
     |                   'brain', network-wide view)  |
     +-------------------- Southbound API (OpenFlow) -+
     |  INFRASTRUCTURE / DATA LAYER                   |
     |  [switch]   [switch]   [switch]   [router]     |  just forward packets
     +-----------------------------------------------+
"""),
("b", [
 "SDN is an architecture that **separates the control plane (decides where traffic goes) from the data plane (forwards the packets)**.",
 "Control is **centralised in software (an SDN controller)**, e.g. OpenDaylight, ONOS, Cisco ACI; devices become simple forwarding elements.",
 "The controller programs devices through **southbound APIs** (e.g. **OpenFlow**); applications ask the controller for services through **northbound APIs**.",
 "**Benefits:** network is **programmable** and automated; central management and visibility; faster provisioning; vendor independence; easier to apply policies/QoS/security network-wide; supports cloud and virtualisation.",
 "**Challenges:** the controller is a single point of failure/attack, scalability, skills needed.",
]),

("h", "8. Hierarchical structure of the Internet (ISPs)"),
("q", "Draw and explain the hierarchical structure of the Internet (ISPs).", "2018 Q4c", "6"),
("pre", """
                 [ Tier 1 ISP ]=====peering=====[ Tier 1 ISP ]      global backbone
                   /        \\                      |
           [ Tier 2 ISP ]--[IXP]--[ Tier 2 ISP ]  [ Tier 2 ISP ]    regional / national
             /     \\              |
     [Tier 3 ISP] [Tier 3 ISP] [Tier 3 ISP]                         local access ISPs
       |   |          |            |
     homes businesses  campus     mobile users                      end users
"""),
("b", [
 "**Tier 1 ISPs** - global backbone networks that reach the whole Internet **without paying for transit**; they **peer** with each other (settlement-free). E.g. AT&T, NTT, Tata, Lumen.",
 "**Tier 2 ISPs** - regional/national providers; **buy transit from Tier 1** and peer with other Tier 2s at **IXPs (Internet Exchange Points)**. E.g. Liquid Intelligent Technologies, Seacom.",
 "**Tier 3 ISPs** - local/access ISPs that buy transit from Tier 2 and connect end users (homes, businesses). E.g. ZOL, TelOne, Econet, Utande.",
 "Connections happen at **POPs (points of presence)** and **IXPs**; content providers (Google, Netflix) also connect directly. Traffic flows up the hierarchy and back down.",
]),

("h", "9. Service Level Agreement (SLA)"),
("q", "Telcos define the services they offer within an SLA. i) Explain the purpose of an SLA. ii) Give two examples of what it might contain.", "2023 Q5d", "1 + 2"),
("p", "**i)** An SLA is a **formal contract between a service provider and a customer that defines the level and quality of service** to be delivered, how it is measured and what happens (penalties/credits) if it is not met."),
("p", "**ii)** Contents: **guaranteed availability/uptime** (e.g. 99.9%); **bandwidth/throughput** guaranteed; **maximum latency, jitter and packet loss**; **response and repair (fault resolution) times**; support hours/contact; **penalties/service credits**; security and data protection responsibilities; reporting/monitoring."),

("h", "10. WAN protocols & point-to-point networks"),
("q", "Explain two WAN protocols.", "SE2024 Q1c", "2"),
("b", [
 "**PPP (Point-to-Point Protocol)** - Layer 2 protocol for direct links between two routers/nodes (serial, DSL - PPPoE); provides framing, authentication (**PAP/CHAP**), error detection and multi-protocol support via LCP/NCP.",
 "**HDLC (High-level Data Link Control)** - bit-oriented synchronous data-link protocol for point-to-point/multipoint links; Cisco default on serial interfaces; uses flags 01111110 and bit stuffing.",
 "**Frame Relay** - packet-switched WAN using virtual circuits (PVCs, DLCI numbers); cheaper than leased lines (now legacy).",
 "**MPLS (Multiprotocol Label Switching)** - routers forward packets based on short **labels** instead of IP lookups; fast, supports QoS and VPNs - used by telcos today.",
 "Others: **ATM** (fixed 53-byte cells), **X.25** (old, error-checked packet switching), ISDN, leased lines (E1/T1).",
]),
("key", "Routing table sources: Connected, Static, Dynamic. DV = Bellman-Ford, periodic full tables, hop count (RIP). LS = Dijkstra, LSAs on change, cost (OSPF). EIGRP = DUAL, successor & feasible successor, bandwidth + delay. QoS = bandwidth, latency, jitter, loss."),
]
