TITLE = "Topic 2: Network Models - OSI & TCP/IP"
SUB = "Course outline weeks 1-2 (OSI reference model, services) + weeks 5-9 (layers). The single MOST examined topic: in all 5 papers, often 9-15 marks."
FILE = "02_OSI_and_TCPIP_Models.pdf"

C = [
("h", "How often this topic is examined"),
("t", [
 ["Question asked", "Paper(s)", "Marks"],
 ["List the 7 OSI layers in order (from layer 7)", "2025 Q1a.i", "9"],
 ["Purpose of the OSI model + functions of Layer 3 and Layer 4", "2025 Q1a.ii", "8"],
 ["Labelled OSI diagram + function of each layer", "SE2024 Q3b [9], ISA2024 Q3c [15]", "9-15"],
 ["OSI vs TCP/IP (compare & contrast)", "2018 Q5b [12], 2023 Q1c [4]", "4-12"],
 ["Significance of TCP/IP and its implementation", "SE2024 Q1e", "4"],
 ["IP vs MAC address - which OSI layer each belongs to", "2025 Q5c", "6"],
 ["Router vs switch - OSI layers and functionality", "2025 Q5d", "10 (see Topic 4)"],
 ["Internetworking principles; how TCP/IP and IP packets help", "2025 Q5a", "3"],
]),
("tip", "Learn the OSI table on page 2 by heart: layer number, name, PDU, function, protocols, devices. With that one table you can answer 9, 12 or 15-mark questions."),

("h", "1. The OSI reference model"),
("p", "The **Open Systems Interconnection (OSI)** model was developed by **ISO** (1984). It is a 7-layer **conceptual framework** that describes how data moves from an application on one computer, across a network, to an application on another computer."),
("h3", "Purpose of the OSI model (2025 Q1a.ii)"),
("b", [
 "Provides a **standard** so that equipment and software from different vendors can **interoperate**.",
 "**Divides the complex** communication process into smaller, manageable layers - each layer has a defined job and only talks to the layer above and below (modularity).",
 "A change in one layer does not affect the others (e.g. move from copper to fibre without changing the applications).",
 "Helps **troubleshooting** (work layer by layer: 'is it a Layer 1 cable problem or a Layer 3 IP problem?') and **teaching**.",
]),
("key", "Mnemonic top-down (7->1): **All People Seem To Need Data Processing** = Application, Presentation, Session, Transport, Network, Data Link, Physical. Bottom-up (1->7): **Please Do Not Throw Sausage Pizza Away**."),
("pre", """
   SENDER                                                       RECEIVER
 +-------------------+                                 +-------------------+
 | 7 Application     |  <------ data -------------->   | 7 Application     |
 | 6 Presentation    |  <------ data -------------->   | 6 Presentation    |
 | 5 Session         |  <------ data -------------->   | 5 Session         |
 | 4 Transport       |  <------ segment ----------->   | 4 Transport       |
 | 3 Network         |  <------ packet ------------>   | 3 Network         |
 | 2 Data Link       |  <------ frame ------------->   | 2 Data Link       |
 | 1 Physical        |  <------ bits -------------->   | 1 Physical        |
 +---------+---------+                                 +---------+---------+
           |================ transmission medium ===================|

 ENCAPSULATION going DOWN:  Data -> [TH|Data] -> [NH|TH|Data] -> [DH|NH|TH|Data|DT] -> 0101..
 (each layer adds its own header; Data Link also adds a trailer (FCS); receiver strips them going UP)
"""),
("h3", "The OSI table - learn this"),
("t", [
 ["Layer", "PDU", "Main functions", "Protocols / examples", "Devices"],
 ["7 Application", "Data", "Interface between user/applications and the network; network services: file transfer, email, web, remote login, directory services", "HTTP, HTTPS, FTP, SMTP, POP3, IMAP, DNS, DHCP, Telnet, SSH, SNMP", "Gateway, hosts"],
 ["6 Presentation", "Data", "Translation (data formats, ASCII/EBCDIC), **encryption/decryption**, **compression**; 'syntax and semantics' of data", "SSL/TLS, JPEG, GIF, MPEG, ASCII", "-"],
 ["5 Session", "Data", "Establish, maintain & terminate sessions (dialog control - half/full duplex); **synchronisation/checkpoints** so a long transfer can resume; RPC", "NetBIOS, RPC, PPTP, SQL sessions", "-"],
 ["4 Transport", "Segment (TCP) / Datagram (UDP)", "**Process-to-process (end-to-end)** delivery using **port numbers**; segmentation & reassembly; connection control; **flow control**; **error control** (end-to-end) & retransmission", "TCP, UDP, SCTP", "Firewalls (L4)"],
 ["3 Network", "Packet", "**Logical addressing (IP)**; **routing** - choosing the best path across networks (source-to-destination, host-to-host delivery); fragmentation; congestion control", "IPv4, IPv6, ICMP, ARP*, OSPF, RIP, EIGRP", "**Router**, L3 switch"],
 ["2 Data Link", "Frame", "**Framing**; **physical (MAC) addressing**; **hop-to-hop (node-to-node)** delivery; error detection (CRC); flow control; **media access control** (CSMA/CD). Sub-layers LLC + MAC", "Ethernet, Wi-Fi (802.11), PPP, HDLC", "**Switch**, bridge, NIC"],
 ["1 Physical", "Bits", "Transmits raw **bits** over the medium: physical characteristics of interfaces & media, signal/encoding, data rate, bit synchronisation, line configuration, topology, transmission mode", "RJ45, Ethernet cabling, DSL, USB, Bluetooth radio", "**Hub**, repeater, cables, modem"],
]),
("p", "*ARP sits between layers 2 and 3 (it maps a Layer-3 IP address to a Layer-2 MAC address)."),

("h", "2. Model answer: Functions of Layer 3 and Layer 4 (2025 Q1a.ii)"),
("h3", "Layer 3 - Network layer"),
("b", [
 "**Logical addressing** - adds source and destination IP addresses to every packet so hosts on different networks can be identified.",
 "**Routing** - routers use routing tables/protocols (RIP, OSPF) to select the best path from source network to destination network.",
 "**Source-to-destination delivery** of packets across multiple networks (internetworking).",
 "**Fragmentation & reassembly** of packets to fit the MTU of each link.",
 "**Congestion control** and error reporting (ICMP).",
]),
("h3", "Layer 4 - Transport layer"),
("b", [
 "**Process-to-process delivery** - uses **port numbers** (e.g. HTTP 80, HTTPS 443) to deliver data to the correct application.",
 "**Segmentation and reassembly** - splits messages into segments with sequence numbers, reassembles them in order at the receiver.",
 "**Connection control** - connection-oriented (TCP 3-way handshake) or connectionless (UDP).",
 "**Flow control** - stops a fast sender from overwhelming a slow receiver (sliding window).",
 "**Error control** - end-to-end; detects lost/damaged segments using checksums & ACKs and retransmits them.",
]),

("h", "3. The TCP/IP model (Internet model)"),
("pre", """
        OSI MODEL                     TCP/IP MODEL            Protocols
   +------------------+          +---------------------+
   | 7 Application    |          |                     |   HTTP, FTP, SMTP, DNS,
   | 6 Presentation   |  ----->  |   Application       |   DHCP, Telnet, SSH, SNMP
   | 5 Session        |          |                     |
   +------------------+          +---------------------+
   | 4 Transport      |  ----->  |   Transport         |   TCP, UDP, SCTP
   +------------------+          +---------------------+
   | 3 Network        |  ----->  |   Internet          |   IP, ICMP, ARP, IGMP
   +------------------+          +---------------------+
   | 2 Data Link      |  ----->  |   Network Access    |   Ethernet, Wi-Fi, PPP
   | 1 Physical       |          |  (Host-to-Network)  |
   +------------------+          +---------------------+
   (Some books use a 5-layer TCP/IP: Application, Transport, Network, Data Link, Physical)
"""),
("h3", "Significance of TCP/IP and its implementation (SE2024 Q1e)"),
("b", [
 "It is **the protocol suite of the Internet** - any device that runs TCP/IP can talk to any other on the Internet regardless of hardware or OS (**interoperability**, open standard, vendor-neutral).",
 "**Routable & scalable** - IP addressing and routing let millions of networks interconnect.",
 "**Reliable delivery** via TCP (ACKs, retransmission) and fast delivery via UDP for real-time traffic.",
 "**Implementation:** built into every OS's network stack; each host is configured with an **IP address, subnet mask, default gateway and DNS server** (manually or via DHCP); applications use **sockets** (IP + port) to communicate.",
]),

("h", "4. OSI vs TCP/IP - compare and contrast"),
("q", "Differentiate between the OSI model and the TCP/IP protocol suite. / Compare and contrast the key differences between the OSI Layer model and the TCP/IP Reference model.", "2018 Q5b [12], 2023 Q1c [4]", "4-12"),
("t", [
 ["Point", "OSI model", "TCP/IP model"],
 ["Developed by", "ISO (International Organization for Standardization)", "US Department of Defense (DARPA) / IETF"],
 ["Number of layers", "7 layers", "4 layers (or 5)"],
 ["Nature", "Theoretical / **reference model** - a generic, protocol-independent standard", "**Practical**, implemented model - the protocols came first and the model describes them"],
 ["Approach", "Model defined **before** protocols (top-down)", "Protocols defined first, model fitted later"],
 ["Separate presentation & session layers", "Yes", "No - merged into the Application layer"],
 ["Physical & data link", "Two separate layers", "Combined into Network Access layer"],
 ["Transport layer", "Connection-oriented service guaranteed", "Both connection-oriented (TCP) and connectionless (UDP)"],
 ["Network layer", "Supports connection-oriented and connectionless", "Connectionless only (IP)"],
 ["Distinction of service, interface, protocol", "Clearly defined", "Not clearly separated"],
 ["Usage", "Used for teaching and troubleshooting", "Used on the real Internet"],
 ["Flexibility", "Protocols are better hidden, easy to replace", "Hard to replace protocols"],
]),
("p", "**Similarities (for 'compare'):** both are layered; both have application, transport and network layers with similar functions; both use packet switching; both use encapsulation; transport layer provides end-to-end delivery in both."),
("tip", "For 12 marks give ~6 differences in a table (2 marks each: one for OSI side, one for TCP/IP side) + draw the two models side by side."),

("h", "5. IP address vs MAC address"),
("q", "Explain the difference between IP addresses and MAC addresses. Which OSI layers does each address belong to?", "2025 Q5c", "6"),
("t", [
 ["Feature", "IP address", "MAC address"],
 ["OSI layer", "**Layer 3 - Network**", "**Layer 2 - Data Link (MAC sub-layer)**"],
 ["Type", "**Logical** address", "**Physical / hardware** address"],
 ["Size", "IPv4 32 bits (e.g. 192.168.1.10); IPv6 128 bits", "48 bits, 12 hex digits (e.g. 00:1A:2B:3C:4D:5E)"],
 ["Assigned by", "Network admin / DHCP / ISP; can change when you move networks", "Burned into the NIC by the manufacturer (OUI from IEEE); normally permanent"],
 ["Scope / purpose", "Identifies a host **and its network**; used for **routing** between networks (end-to-end)", "Identifies a NIC on the **local** network; used for **hop-to-hop** delivery in a LAN"],
 ["Changes during the journey?", "Source & destination IP stay the same end-to-end", "Changes at every hop (each router rewrites the frame)"],
 ["Resolved by", "DNS maps names -> IP", "ARP maps IP -> MAC"],
]),
("p", "Third type for completeness: **port address** (Layer 4, 16-bit) identifies the process/application, e.g. 80 for HTTP."),

("h", "6. Internetworking principles (2025 Q5a, outline weeks 5-7)"),
("p", "**Internetworking** = connecting separate, possibly different networks (Ethernet LANs, Wi-Fi, WAN links) so they act as one large network (the Internet = network of networks)."),
("b", [
 "**Universal addressing** - every host gets a unique IP address independent of the underlying LAN technology.",
 "**Routers** connect networks and forward packets hop-by-hop using routing tables.",
 "**Common protocol (IP)** - every network carries the same IP packet format, hiding hardware differences; **TCP** above it provides reliable end-to-end delivery.",
 "**Encapsulation** - the IP packet is placed inside whatever frame each network uses (Ethernet, PPP); **fragmentation** adapts packet size to each network's MTU.",
 "**Connectionless, best-effort datagram delivery** - each IP packet is routed independently.",
]),
("key", "Delivery types: **Data Link = hop-to-hop (node-to-node)**, **Network = host-to-host (source-to-destination)**, **Transport = process-to-process (end-to-end)**. Examiners love this distinction."),
]
