TITLE = "Topic 4: Data Link Layer, MAC Sub-layer & LAN Devices"
SUB = "Course outline weeks 3-4: medium access sub-layer, channel allocation, LAN protocols, ALOHA, IEEE standards, elementary data link protocols, sliding window, error handling + data link layer switching, bridges & routers."
FILE = "04_Data_Link_MAC_Error_Control_LAN_Devices.pdf"

C = [
("h", "How often this topic is examined"),
("t", [
 ["Question asked", "Paper(s)", "Marks"],
 ["CSMA/CD (define / explain with diagram / in Ethernet)", "2018 Q3b, 2023 Q4a, SE2024 Q2b, ISA2024 Q4a", "3-5"],
 ["CSMA/CA; CSMA/CD vs CSMA/CA table", "2018 Q3b, 2023 Q4a", "3-5"],
 ["LLC and MAC sub-layers", "2023 Q5a [6], ISA2024 Q1c [6]", "6"],
 ["Error types (single-bit, burst) + detection methods; 3 error-detection strategies", "2023 Q4b [4], SE2024 Q3a [3]", "3-4"],
 ["FEC, Hamming distance, piggybacking", "2018 Q1b", "9"],
 ["Stop-and-wait protocol", "2018 Q4b", "4"],
 ["Pure ALOHA and slotted ALOHA (diagram)", "ISA2024 Q4c", "8"],
 ["Structure of a MAC address", "2018 Q4d", "5"],
 ["ARP", "2018 Q3b.iii", "3"],
 ["Corrupted destination address on a bus LAN", "2025 Q5b", "6"],
 ["Bridge function in data-link switching", "2025 Q4c", "7"],
 ["Router vs switch (layers & functionality)", "2025 Q5d", "10"],
 ["Hub vs switch; repeater vs bridge; why a switch is intelligent", "SE2024 Q4f [5], Q1b.ii [2], 2018 Q5d [3]", "2-5"],
 ["VLAN; network segmentation", "2018 Q5c [4], ISA2024 Q1b [3]", "3-4"],
]),
("tip", "CSMA/CD is in 4 of 5 papers - learn the flowchart. LLC/MAC is in 2 papers at 6 marks each."),

("h", "1. The data link layer and its two sub-layers (IEEE 802)"),
("q", "The data link layer in the IEEE standard is divided into two sub-layers. Discuss the functions performed by: i) LLC  ii) MAC.", "2023 Q5a [3+3], ISA2024 Q1c [6]", "6"),
("pre", """
   +-------------------------------------------+
   |  Network layer (IP)                       |
   +-------------------------------------------+
   |  LLC - Logical Link Control (IEEE 802.2)  |   upper sub-layer, same for all LANs
   |-------------------------------------------|   DATA LINK LAYER
   |  MAC - Media Access Control (802.3, 802.11)|  lower sub-layer, specific to each LAN
   +-------------------------------------------+
   |  Physical layer                           |
   +-------------------------------------------+
"""),
("h3", "LLC - Logical Link Control (upper)"),
("b", [
 "Interface with the **network layer** - identifies which network-layer protocol (IPv4, IPv6...) is carried, using **SAPs** (service access points) - allows multiplexing of protocols.",
 "**Flow control** - controls the rate at which data is sent (e.g. sliding window).",
 "**Error control** - acknowledgements and retransmission of lost/damaged frames (in connection-oriented LLC).",
 "Provides connectionless or connection-oriented services; it is **independent of the physical medium**, so the same LLC works over Ethernet, Wi-Fi, Token Ring.",
]),
("h3", "MAC - Media Access Control (lower)"),
("b", [
 "**Framing** - builds frames (preamble, destination & source MAC, type/length, data, FCS).",
 "**Physical (MAC) addressing** - adds 48-bit source/destination hardware addresses; recognises frames addressed to the station.",
 "**Media access control** - decides who may transmit on a shared medium and when: **CSMA/CD** (Ethernet 802.3), **CSMA/CA** (Wi-Fi 802.11), token passing.",
 "**Error detection** - computes/checks the **CRC (FCS)** and discards damaged frames.",
 "Interfaces with the physical layer; specific to each LAN technology.",
]),
("p", "**Data link layer overall functions:** framing, physical addressing, flow control, error control, access control - **node-to-node (hop-to-hop) delivery**."),

("h", "2. Media access: CSMA/CD"),
("q", "With the aid of a supporting diagram, explain the concept of CSMA/CD used by Ethernet. / In the description of the Ethernet architecture, explain the function and operation of CSMA/CD.", "ISA2024 Q4a [5], SE2024 Q2b [5], 2018 Q3b.i [3]", "3-5"),
("p", "**CSMA/CD = Carrier Sense Multiple Access with Collision Detection.** Used by classic (half-duplex, shared/bus/hub) **Ethernet IEEE 802.3** so that many stations can share one cable."),
("b", [
 "**Carrier Sense** - a station listens to the medium before sending ('listen before talk').",
 "**Multiple Access** - many stations share the same medium; any can transmit when it is free.",
 "**Collision Detection** - while transmitting, the station keeps listening ('listen while talk'); if the signal it sees differs from what it sent, a collision has happened.",
]),
("pre", """
                    [ Station has a frame ]
                              |
                  +--> Sense carrier: is the medium idle? --No--> wait (keep sensing)
                  |           | Yes
                  |    Transmit frame and monitor the medium
                  |           |
                  |    Collision detected? --No--> Transmission successful
                  |           | Yes
                  |    Stop, send 32-bit JAM signal (tell everyone)
                  |           |
                  |    attempts = attempts + 1; if attempts > 15 -> abort
                  |           |
                  +-- Wait random backoff time = R x slot time,
                      R chosen from 0 .. 2^k - 1 (binary exponential backoff, k = min(n,10))

     A ----------> <---------- D        signals overlap in the middle = COLLISION
     ========================================  bus   -> both detect, jam, back off
"""),
("p", "Important: a frame must be long enough (minimum 64 bytes in Ethernet) that the sender is still transmitting when the collision news returns (frame transmission time >= 2 x propagation delay). In modern **full-duplex switched Ethernet** there are no collisions, so CSMA/CD is not needed."),

("h", "3. CSMA/CA and CSMA/CD vs CSMA/CA"),
("p", "**CSMA/CA = Carrier Sense Multiple Access with Collision Avoidance**, used in **wireless LANs (IEEE 802.11 Wi-Fi)**. Wireless stations cannot detect collisions reliably (they cannot send and listen at once, and the *hidden station* problem exists), so they try to **avoid** them:"),
("n", [
 "Sense the channel; if idle wait an interframe space (**DIFS**).",
 "Wait a random **backoff** (contention window) counting down only while idle.",
 "Optionally send **RTS (Request To Send)**; the access point replies **CTS (Clear To Send)** - all other stations defer (NAV).",
 "Send the data frame; receiver waits **SIFS** and returns an **ACK**. No ACK = assume collision -> retransmit with bigger backoff.",
]),
("q", "Using a table, differentiate CSMA/CD from CSMA/CA.", "2023 Q4a", "5"),
("t", [
 ["CSMA/CD", "CSMA/CA"],
 ["Collision **Detection** - deals with collisions **after** they happen", "Collision **Avoidance** - tries to prevent collisions **before** they happen"],
 ["Used in **wired** Ethernet LANs (IEEE 802.3)", "Used in **wireless** LANs (IEEE 802.11 Wi-Fi)"],
 ["Station transmits and listens at the same time", "Wireless stations can't listen while sending; uses waiting times (IFS) & backoff"],
 ["Jam signal + binary exponential backoff on collision", "RTS/CTS handshake and ACK for every frame"],
 ["No acknowledgement at MAC layer", "Positive ACK required for each frame"],
 ["Efficient on wired, less overhead", "More overhead (IFS, RTS/CTS, ACK), lower efficiency"],
]),

("h", "4. ALOHA"),
("q", "In the Aloha system, the basic idea is applicable to any system in which uncoordinated users are competing for a single shared channel. Explain using a diagram the functionality of: i) Pure ALOHA ii) Slotted ALOHA.", "ISA2024 Q4c", "4 + 4"),
("p", "ALOHA was developed at the **University of Hawaii (1970)** for radio packet networks. It is a **random access** protocol."),
("h3", "Pure ALOHA"),
("b", [
 "A station **sends whenever it has a frame** - no carrier sensing.",
 "It waits for an **ACK**; if no ACK arrives within a timeout (2 x max propagation time), it assumes a collision, waits a **random backoff** time and resends.",
 "A frame collides if any other frame starts within one frame time before or after it - **vulnerable time = 2 x Tfr**.",
 "**Maximum throughput = 1/(2e) = 18.4%** (at G = 0.5).",
]),
("h3", "Slotted ALOHA"),
("b", [
 "Time is divided into **slots** equal to one frame time (Tfr); stations are synchronised by a clock.",
 "A station may only start transmitting **at the beginning of a slot**.",
 "Collisions happen only if two stations pick the same slot, so **vulnerable time = Tfr** (half of pure ALOHA).",
 "**Maximum throughput = 1/e = 36.8%** (at G = 1) - double pure ALOHA. Needs synchronisation.",
]),
("pre", """
 PURE ALOHA (frames start any time)
 Station A: [==A1==]                 [==A2==]
 Station B:      [==B1==]                           [==B2==]
 Station C:                          [==C1==]
                 ^ A1,B1 overlap = collision   ^ A2,C1 overlap = collision     B2 OK
 ----------------------------------------------------------------------> time

 SLOTTED ALOHA (frames start only at slot boundaries)
 |  slot1  |  slot2  |  slot3  |  slot4  |  slot5  |
 |[==A1==] |         |[==A2==] |         |[==B2==] |
 |[==B1==] |         |         |[==C1==] |         |
   collision            OK         OK        OK
"""),
("p", "Related channel-allocation schemes: **static** (FDM, TDM) vs **dynamic** (ALOHA, CSMA, token passing). Controlled access: reservation, **polling**, **token passing** (Token Ring 802.5, **FDDI** - Fibre Distributed Data Interface: 100 Mbps dual counter-rotating fibre token ring, up to 200 km, the second ring gives fault tolerance)."),

("h", "5. Error detection and correction"),
("q", "Copy and complete the table (Type of error | Description | Detection method).", "2023 Q4b", "4"),
("t", [
 ["Type of error", "Description", "Detection method"],
 ["Single-bit error", "Only **one bit** of a data unit (byte/frame) changes from 0 to 1 or 1 to 0. e.g. 00000010 -> 00001010", "**Parity check** (VRC - simple even/odd parity) - detects all single-bit errors; also CRC, checksum"],
 ["Burst error", "**Two or more bits** in the data unit change (not necessarily consecutive); the burst length is from the first to the last corrupted bit. More common, caused by noise lasting longer than one bit time", "**CRC (Cyclic Redundancy Check)** - detects all bursts shorter than the CRC length; also 2-D parity (LRC), checksum"],
]),
("q", "Explain any three error detection strategies used to control data transmission.", "SE2024 Q3a", "3"),
("b", [
 "**Parity check (VRC)** - one extra bit added so the total number of 1s is even (even parity) or odd. Receiver recounts; a mismatch shows an error. Detects single-bit and odd-numbered errors, misses even numbers of errors. **2-D parity (LRC)** adds a parity row too, catching more bursts.",
 "**CRC (Cyclic Redundancy Check)** - the sender divides the data (with n zeros appended) by an agreed generator polynomial using modulo-2 (XOR) division; the n-bit remainder (CRC) is appended. The receiver divides the whole frame by the same divisor: remainder 0 = no error. Used in Ethernet FCS. Very powerful.",
 "**Checksum** - data split into k-bit sections, added using 1's complement arithmetic; the complement of the sum is sent. Receiver adds all sections + checksum: result all 1s (complement = 0) = OK. Used in IP, TCP, UDP headers.",
]),
("pre", """
 CRC worked example: data 1001, generator 1011 (n = 3 -> append 000)
     1001000 / 1011 (modulo-2 / XOR division):
       1001 XOR 1011 = 010 -> bring down 0 -> 0100 (top bit 0: XOR 0000) = 100
       -> bring down 0 -> 1000 XOR 1011 = 011 -> bring down 0 -> 0110 (top bit 0) = 110
     remainder = 110  ->  transmitted codeword = 1001 110
     Receiver: 1001110 / 1011 -> remainder 000 = no error
 Even-parity example: 1100001 has three 1s -> parity bit 1 -> sent 11000011
"""),
("h3", "Key terms (2018 Q1b - 3 marks each)"),
("b", [
 "**Forward Error Correction (FEC)** - the sender adds enough **redundant bits** that the **receiver can detect AND correct errors itself without asking for retransmission**. Used when retransmission is impossible or too slow: real-time audio/video, satellite links, deep-space, simplex links. Example: **Hamming code**, Reed-Solomon. (Opposite: **ARQ** - Automatic Repeat reQuest - detect and retransmit.)",
 "**Hamming distance** - the number of bit positions in which two codewords of equal length **differ**. Found by XORing them and counting the 1s: d(10101, 11110) -> 01011 -> **3**. The **minimum Hamming distance** (d_min) of a code determines power: to **detect** s errors d_min = s + 1; to **correct** t errors d_min = 2t + 1.",
 "**Piggybacking** - in bidirectional (full duplex) communication, the receiver does not send a separate ACK frame; instead it **attaches the acknowledgement to its next outgoing data frame** (ack field in the header). Improves efficiency/bandwidth use; disadvantage: if there is no data to send, the ACK is delayed (a timer forces a separate ACK).",
]),

("h", "6. Flow control: stop-and-wait & sliding window"),
("q", "Explain the working principle of the stop and wait protocol.", "2018 Q4b", "4"),
("pre", """
   SENDER                         RECEIVER
     |---- Frame 0 ------------------>|
     |<--------------------- ACK 1 ---|
     |---- Frame 1 ------X (lost)     |
     |   (timer expires)              |
     |---- Frame 1 (resent) --------->|
     |<--------------------- ACK 0 ---|
"""),
("b", [
 "Sender transmits **one frame** and keeps a copy, starts a **timer**, then **stops and waits** for an acknowledgement.",
 "The receiver checks the frame; if correct it sends an **ACK**; only then does the sender send the next frame.",
 "If the timer expires (frame or ACK lost/damaged), the sender **retransmits** the frame (Stop-and-Wait **ARQ**).",
 "Frames and ACKs are numbered alternately **0 and 1** (modulo-2 sequence numbers) so duplicates can be detected.",
 "Simple, but **inefficient** on long/fast links because the line is idle while waiting (window size = 1).",
]),
("p", "**Sliding window protocols** (outline topic): the sender may send **several frames (up to window size W)** before needing an ACK. **Go-Back-N ARQ**: sender window up to 2^m - 1, receiver window 1; on error the sender resends the damaged frame and **all frames after it**. **Selective Repeat ARQ**: windows up to 2^(m-1); only the damaged/lost frame is resent; receiver buffers out-of-order frames. Much better link utilisation than stop-and-wait."),

("h", "7. MAC address structure"),
("q", "With the aid of an example, describe the structure of a MAC address.", "2018 Q4d", "5"),
("pre", """
        00 : 1A : 2B   :   3C : 4D : 5E          (48 bits = 6 bytes = 12 hex digits)
        |<-- OUI -->|     |<-- NIC specific -->|
        24 bits            24 bits
        Organisationally   assigned by the manufacturer
        Unique Identifier  (serial number of the card)
        (from IEEE, e.g. Cisco, Intel)

   First byte bits:  b0 (least significant) = I/G : 0 = unicast, 1 = multicast
                     b1                     = U/L : 0 = globally unique, 1 = locally administered
   Broadcast address = FF:FF:FF:FF:FF:FF
"""),
("p", "Written as 00-1A-2B-3C-4D-5E (Windows), 00:1A:2B:3C:4D:5E (Linux) or 001A.2B3C.4D5E (Cisco). Burned into the NIC ROM, used for delivery within a LAN; view with `ipconfig /all`."),

("h", "8. ARP"),
("p", "**ARP (Address Resolution Protocol)** maps a known **IP address (Layer 3) to a MAC address (Layer 2)** on a local network. Host A wants to send to 192.168.1.20 but needs its MAC: (1) checks its **ARP cache**; (2) if absent, **broadcasts** an ARP Request to FF:FF:FF:FF:FF:FF: 'Who has 192.168.1.20? Tell 192.168.1.10'; (3) the owner replies with a **unicast ARP Reply** containing its MAC; (4) A stores it in the cache and sends the frame. **RARP** does the reverse (MAC -> IP)."),

("h", "9. Corrupted destination address on a bus"),
("q", "Suppose a computer sends a frame to another computer on a bus topology LAN. The physical destination address of the frame is corrupted during transmission: i) Explain what happens to the frame. ii) Explain how the sender can be informed about the situation.", "2025 Q5b", "3 + 3"),
("p", "**i)** On a bus every station receives the frame. Each station compares the destination MAC address with its own. Because the address is corrupted, the **intended receiver will not recognise the frame** as its own and ignores it. Also, the corruption changes the bits, so the **CRC/FCS check fails** at every station and the frame is **discarded** (even if the corrupted address happened to match another station). The frame is effectively lost; it eventually reaches the terminators and is absorbed."),
("p", "**ii)** The data link layer of Ethernet does not send error messages for a discarded frame, so the sender is informed **indirectly** through the **lack of an acknowledgement**: in protocols using ACKs (Stop-and-Wait / sliding window ARQ, or TCP at the transport layer) the sender's **timer expires** without an ACK, so it concludes the frame/segment was lost and **retransmits** it. (A NAK can be used if the receiver can recognise the frame.)"),

("h", "10. LAN devices: hub, repeater, bridge, switch, router"),
("q", "Describe the function of a network bridge and how it operates in a Data Link Layer switching environment.", "2025 Q4c", "7"),
("b", [
 "A **bridge** is a **Layer 2** device that connects two (or more) LAN segments and **filters and forwards frames based on MAC addresses**. It divides the network into separate **collision domains** while remaining one broadcast domain.",
 "**Learning:** when a frame arrives, the bridge records the **source MAC** and the port it arrived on in its **MAC/forwarding table** (transparent/learning bridge - no configuration needed).",
 "**Filtering:** if the destination MAC is on the **same port** the frame came from, the bridge drops it (traffic stays local).",
 "**Forwarding:** if the destination is known on another port, the frame is sent **only to that port**.",
 "**Flooding:** if the destination is unknown, or it is a broadcast/multicast, the frame is sent out all ports except the incoming one.",
 "**Ageing:** table entries time out (~300 s) so moved hosts are relearned.",
 "**Spanning Tree Protocol (STP, IEEE 802.1D)** prevents loops when bridges are connected redundantly by blocking some ports.",
 "A **switch** is a multi-port bridge doing this in hardware (ASICs) at wire speed.",
]),
("pre", """
     Segment 1                            Segment 2
  [A]   [B]                             [C]    [D]
   |     |                               |      |
 ==+=====+======[ port1  BRIDGE  port2 ]=+======+==
                  MAC table: A-p1, B-p1, C-p2, D-p2
  A -> B : stays on segment 1 (filtered)     A -> C : forwarded to port 2
"""),
("q", "Differentiate between hub and switch on the basis of layer, ports, device type, speed.", "SE2024 Q4f", "5"),
("t", [
 ["Basis", "Hub", "Switch"],
 ["OSI layer", "Layer 1 - Physical", "Layer 2 - Data Link (L3 switches also exist)"],
 ["Ports", "Typically 4/8/12; all ports share one collision domain", "24/48 ports; **each port is its own collision domain**"],
 ["Device type", "**Passive/dumb** - broadcasts every frame to all ports", "**Intelligent/active** - uses a MAC table to send frames only to the destination port"],
 ["Speed / duplex", "Shared bandwidth (10/100 Mbps), **half duplex**", "Dedicated bandwidth per port (100 Mbps - 10 Gbps), **full duplex**"],
 ["Addressing", "No addresses used", "Uses MAC addresses"],
 ["Security / collisions", "Many collisions; anyone can sniff traffic", "No collisions in full duplex; more secure"],
]),
("p", "**Why a switch is said to be intelligent (2018 Q5d, 3 marks):** it **learns** MAC addresses and builds a MAC address table, **forwards frames only to the port of the destination** (not to everyone like a hub), filters local traffic, checks frames for errors (store-and-forward), supports **VLANs**, full duplex and QoS, and (managed switches) can be configured and monitored."),
("p", "**Repeater vs bridge (SE2024 Q1b.ii, 2 marks):** a **repeater** (Layer 1) simply **regenerates/amplifies** the signal bit by bit to extend the cable distance - it does not filter and forwards everything including collisions. A **bridge** (Layer 2) reads MAC addresses and **filters/forwards frames** between segments, reducing traffic and separating collision domains."),
("q", "Discuss the purpose of a router and a switch in a network. Which OSI layers do they operate on, and what is the difference between them in terms of functionality?", "2025 Q5d", "10"),
("t", [
 ["Point", "Switch", "Router"],
 ["Purpose", "Connects devices **within the same network (LAN)**", "Connects **different networks** (LAN to LAN, LAN to WAN/Internet)"],
 ["OSI layer", "**Layer 2 - Data Link** (multilayer switch also L3)", "**Layer 3 - Network**"],
 ["Address used", "**MAC** addresses, MAC address table", "**IP** addresses, routing table"],
 ["Data unit", "Frames", "Packets"],
 ["Decision", "Forwards frames to the correct port", "Determines the **best path** using routing protocols (RIP, OSPF, EIGRP)"],
 ["Broadcasts", "Forwards broadcasts - one broadcast domain (unless VLANs)", "**Blocks broadcasts** - each interface is a separate broadcast domain"],
 ["Extra features", "VLANs, port security, PoE", "NAT, DHCP, firewall/ACLs, VPN, WAN interfaces"],
 ["Example", "Lab switch connecting 24 PCs", "Home/office router connecting the LAN to the ISP"],
]),

("h", "11. VLANs & network segmentation"),
("p", "**VLAN (Virtual LAN)** (2018 Q5c, 4 marks) - a **logical grouping of devices into a separate broadcast domain on a switch, regardless of physical location** (configured in software, IEEE **802.1Q** tagging). **Uses:** separate departments (Accounts, HR, IT) on the same switches; **security** (sensitive traffic isolated); **reduce broadcast traffic** and improve performance; flexibility - move users without recabling; separate voice and data traffic (voice VLAN, QoS). Inter-VLAN traffic needs a router or Layer 3 switch."),
("p", "**Network segmentation** (ISA2024 Q1b, 3 marks) - dividing a large network into smaller **segments/subnets** (with routers, switches, VLANs, subnetting or firewalls). **Benefits:** reduces congestion & broadcast/collision domains -> better **performance**; improves **security** (contains attacks/malware, limits lateral movement, applies access control between zones e.g. DMZ); easier **management** and troubleshooting."),

("h", "12. IEEE 802 standards overview (outline)"),
("t", [
 ["Standard", "Technology"],
 ["802.1", "Bridging, VLANs (802.1Q), STP (802.1D)"],
 ["802.2", "LLC"],
 ["802.3", "Ethernet (CSMA/CD)"],
 ["802.5", "Token Ring"],
 ["802.11", "Wireless LAN / Wi-Fi (CSMA/CA)"],
 ["802.15", "WPAN - Bluetooth (802.15.1), Zigbee (802.15.4)"],
 ["802.16", "WiMAX (wireless MAN)"],
]),
("key", "Detection: Parity, CRC, Checksum. Correction: Hamming code (FEC) or retransmit (ARQ: Stop-and-Wait, Go-Back-N, Selective Repeat). CD = wired, react after; CA = wireless, prevent before. Pure ALOHA 18.4%, Slotted 36.8%."),
]
