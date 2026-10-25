TITLE = "Topic 1: Data Communication & Networking Fundamentals"
SUB = "Course outline weeks 1-2: introduction concepts, goals & applications, network structure, topology design. Appears in EVERY past paper."
FILE = "01_Fundamentals_Components_Topologies.pdf"

C = [
("h", "How often this topic is examined"),
("t", [
 ["Question asked", "Paper(s)", "Marks"],
 ["Components of a data communication system (with diagram)", "2018 Q1a, SE2024 Q2f", "5"],
 ["Transmission modes: simplex / half duplex / full duplex", "2023 Q4e, SE2024 Q1a", "1-6"],
 ["Categories of networks (LAN, MAN, WAN...)", "2018 Q1c, ISA2024 Q3b", "6-9"],
 ["Network topologies (describe 3 or 4, ring vs bus)", "2025 Q2c, ISA2024 Q2c, SE2024 Q2e", "3-12"],
 ["Logical vs physical topology", "SE2024 Q3c", "2"],
 ["Client-server vs peer-to-peer", "2025 Q1b, SE2024 Q4b/Q5d", "4-8"],
 ["What is a protocol (with examples)", "2025 Q2a", "5"],
 ["Point-to-point communication / configurations of networks (relationships among nodes)", "SE2024 Q1a, Q3d", "1-4"],
 ["Internet vs WWW; internet services", "SE2024 Q4a, Q5c", "4"],
 ["Hardware, software & protocols of a basic network", "SE2024 Q4d", "4"],
 ["Network design scenario (5 floors x 20 PCs)", "SE2024 Q3e", "5"],
 ["Competencies: network admin, engineer, hacker", "SE2024 Q4e", "4"],
]),
("tip", "Topologies + components + client/server are 'free marks' questions. Always DRAW a diagram even when not asked - the 2024 ISA paper says 'illustrate your answer with large clearly labelled diagrams'."),

("h", "1. Components of a data communication system"),
("q", "With the aid of a fully labelled diagram, explain all the components involved in a data communication system.", "2018 Q1a / SE2024 Q2f", "5"),
("pre", """
                 +------------------- PROTOCOL (rules) -------------------+
                 |                                                         |
   +--------+    |   Rule 1 ... Rule n              Rule 1 ... Rule n      |   +----------+
   | SENDER | ---+-->  [ MESSAGE ] =====  TRANSMISSION MEDIUM  =====> ----+-->| RECEIVER |
   +--------+         (text, numbers, image, audio, video)                    +----------+
   e.g. PC            e.g. twisted pair, fibre, radio waves                   e.g. server
"""),
("n", [
 "**Message** - the information (data) to be communicated: text, numbers, pictures, audio or video.",
 "**Sender** - the device that sends the message, e.g. computer, phone, video camera.",
 "**Receiver** - the device that receives the message, e.g. computer, printer, TV.",
 "**Transmission medium** - the physical path the message travels: twisted-pair, coaxial, fibre-optic cable or radio waves.",
 "**Protocol** - a set of rules that govern the communication. Without a protocol two devices may be connected but not communicating (like a Shona speaker and a French speaker).",
]),
("key", "5 components = **M-S-R-T-P**: Message, Sender, Receiver, Transmission medium, Protocol. Characteristics of a good system: **Delivery, Accuracy, Timeliness, Jitter**."),

("h", "2. Transmission modes (data flow)"),
("q", "The transmission mode defines the direction of signal flow between two connected devices. State the three transmission modes, giving examples for each.", "2023 Q4e", "6"),
("t", [
 ["Mode", "Meaning", "Example"],
 ["Simplex", "One direction only. One device transmits, the other only receives.", "Keyboard -> computer, TV/radio broadcast, monitor"],
 ["Half duplex", "Both directions but **not at the same time**. Whole channel capacity used by whichever device is sending.", "Walkie-talkie / two-way radio, CB radio"],
 ["Full duplex", "Both directions **simultaneously**. Channel capacity is shared (or two separate paths).", "Telephone call, mobile phone, video call"],
]),
("p", "**Half duplex transmission** (SE2024 Q1a.i, 1 mark): communication in both directions but only one direction at a time, e.g. walkie-talkie."),
("p", "**Point-to-point communication** (SE2024 Q1a.ii): a dedicated link between exactly two devices; the whole capacity of the link is reserved for those two, e.g. a TV remote and TV, or a leased line between two routers. Opposite = **multipoint (multidrop)**, where more than two devices share one link."),
("p", "**Synchronous transmission** (SE2024 Q1a.iii): data sent as a continuous stream of bits in blocks/frames with sender and receiver clocks synchronised (timing signal), no start/stop bits per byte. Faster/efficient. Opposite is **asynchronous** - each byte framed by start and stop bits, gaps between bytes allowed (e.g. keyboard)."),

("h", "3. Categories / types of networks"),
("q", "There are various categories of networks. Explain any three. / Describe the differences between LAN, WAN and MAN.", "2018 Q1c [6], ISA2024 Q3b [9]", "6-9"),
("t", [
 ["Feature", "LAN", "MAN", "WAN"],
 ["Full name", "Local Area Network", "Metropolitan Area Network", "Wide Area Network"],
 ["Coverage", "Single room, building or campus (up to ~ a few km)", "A city / town (~5-50 km)", "Country, continent, the whole world"],
 ["Ownership", "Privately owned by one organisation", "Usually a company or municipality / ISP", "Public carriers, telcos (e.g. TelOne, Liquid), leased"],
 ["Speed", "Very high (100 Mbps - 10 Gbps)", "High", "Lower than LAN, depends on link"],
 ["Error rate / delay", "Low errors, low delay", "Moderate", "Higher errors and propagation delay"],
 ["Cost / setup", "Cheap, easy to set up", "Expensive", "Very expensive"],
 ["Technology", "Ethernet, Wi-Fi", "Fibre rings, WiMAX, cable TV", "MPLS, leased lines, satellite, the Internet"],
 ["Example", "HIT computer lab", "Network linking Harare city council offices", "The Internet, bank branches across Zimbabwe"],
]),
("p", "Others you can mention: **PAN** (Personal Area Network, ~10 m, Bluetooth), **CAN** (Campus Area Network), **SAN** (Storage Area Network), **WLAN** (wireless LAN)."),

("h", "4. Network topologies"),
("q", "Describe any four (4) network topologies that can be used to connect devices.", "2025 Q2c [12]  (also ISA2024 Q2c - three topologies [9])", "12"),
("pre", """
   BUS                         STAR                       RING
 [A]  [B]  [C]               [A]   [B]                 [A]----[B]
  |    |    |                  \\   /                    |        |
 =+====+====+==  <-terminator  [HUB/SWITCH]            [D]----[C]
     backbone                  /   \\                  (data travels one way,
                             [C]   [D]                  token passed round)

   MESH (full)                 TREE (hierarchical)        HYBRID = mix e.g. star-bus
 [A]-----[B]                       [Core]
  | \\   / |                       /      \\
  |   X   |                   [Sw1]      [Sw2]
  | /   \\ |                  /   \\      /   \\
 [D]-----[C]               PC    PC    PC    PC
 links = n(n-1)/2
"""),
("t", [
 ["Topology", "How it works", "Advantages", "Disadvantages"],
 ["Bus", "All devices attach to one backbone cable with terminators at both ends; a signal is broadcast to every node.", "Cheap, little cable, easy to extend", "Backbone fault brings network down; collisions; hard to troubleshoot; performance drops as nodes increase"],
 ["Star", "Each device has its own cable to a central hub/switch.", "Easy install & fault isolation; one cable failure affects only one node; easy to add nodes", "Central device is a single point of failure; more cable than bus"],
 ["Ring", "Each device connects to two neighbours forming a closed loop; data passes in one direction, usually using a token.", "No collisions (token); equal access; good under heavy load", "One break/one faulty node can stop the whole ring; adding/removing nodes disrupts network; slower (each node repeats data)"],
 ["Mesh", "Every device has a dedicated point-to-point link to every other device. Needs n(n-1)/2 links.", "Very reliable/fault tolerant; dedicated links = no traffic problems; secure/private", "Very expensive; lots of cable & I/O ports; hard to install"],
 ["Tree", "Hierarchy of star networks connected to a backbone.", "Scalable, easy to manage in sections", "If the root/backbone fails, segments are cut off"],
 ["Hybrid", "Combination of two or more topologies (e.g. star-bus, star-ring).", "Flexible, uses strengths of each", "Complex design, expensive"],
]),
("q", "Explain the limitations of a ring network topology compared to a bus network topology.", "SE2024 Q2e", "3"),
("b", [
 "A single break in the cable or failure of one node can break the whole ring (unless a dual ring is used); in a bus, a failed node does not affect others.",
 "Adding or removing a device requires breaking the ring, which disrupts the network; in a bus you simply tap into the backbone.",
 "Every node must receive and regenerate the data, so delay grows with the number of nodes; it is also more expensive/complex (token management) than a bus.",
]),
("h3", "Logical vs physical topology (SE2024 Q3c.i, 2 marks)"),
("p", "**Physical topology** = the actual physical layout of cables and devices (how it looks). **Logical topology** = how data actually flows between devices (how it works). Example: Ethernet using a switch is a physical **star** but logically behaves like a **bus**; Token Ring wired to a MAU is a physical star but a logical **ring**."),

("h", "5. Network configurations by relationship among nodes"),
("q", "Describe in detail four possible configurations of computer networks as categorized by relationships among nodes.", "SE2024 Q3d", "4"),
("n", [
 "**Peer-to-peer** - every computer is equal; each can act as client and server and share its own resources. No central server.",
 "**Client-server** - dedicated servers provide services (files, mail, web, database) to clients that request them.",
 "**Point-to-point** - a dedicated link joins exactly two nodes.",
 "**Multipoint / broadcast** - many nodes share one link/channel; a message sent by one is received by all (e.g. bus, Wi-Fi).",
]),
("p", "(If the lecturer means line configuration only, point-to-point and multipoint are the two main ones; give the client/server and P2P as the 'relationship' models.)"),

("h", "6. Client-server vs peer-to-peer"),
("q", "With the aid of proper examples, differentiate between the Client-Server model and the Peer-to-Peer model for network applications.", "2025 Q1b [8]; SE2024 Q4b - four benefits of client-server [4]", "8"),
("t", [
 ["Point", "Client-Server", "Peer-to-Peer (P2P)"],
 ["Structure", "Central, powerful server(s) serve many clients", "All nodes are equal peers; each is both client and server"],
 ["Control & security", "Centralised administration, user accounts, access control", "Each user manages own machine; weak security"],
 ["Data storage / backup", "Data stored centrally, easy backup", "Data scattered across peers, backup difficult"],
 ["Scalability", "Scales well (add servers)", "Performance falls as peers grow (for small nets) - but file-sharing P2P scales because each peer adds capacity"],
 ["Cost", "Expensive: server hardware, NOS, admin staff", "Cheap, no dedicated server"],
 ["Failure", "Server is a single point of failure", "No single point of failure"],
 ["Examples", "Web (browser <-> web server), email (Outlook <-> mail server), HIT e-learning portal, online banking", "BitTorrent, Skype (original), Windows workgroup file sharing, blockchain/Bitcoin"],
]),
("p", "**Four benefits of client-server over P2P:** (1) centralised security & user authentication, (2) centralised backup and data integrity, (3) easier management/updates of resources, (4) better scalability and performance with dedicated servers."),
("q", "With reference to the client-server paradigm, explain how Harare Institute of Technology students are able to access online learning resources remotely from home.", "SE2024 Q5d", "7"),
("n", [
 "The student's device (laptop/phone with a browser = **client**) connects to the Internet through their ISP (Wi-Fi/mobile data).",
 "The student types the URL of the HIT e-learning portal (e.g. Moodle). The client asks a **DNS** server to resolve the domain name to the server's IP address.",
 "The client opens a **TCP** connection (3-way handshake) to the web server on port 443 (HTTPS); TLS encrypts the session.",
 "The client sends an **HTTP request** (GET login page). The student logs in; the server **authenticates** the credentials against a database/directory.",
 "The **server** processes requests, fetches notes, videos, assignments from its database/file storage and sends **HTTP responses** back.",
 "The browser renders the resources; uploads (assignments) travel the opposite way (HTTP POST).",
 "The server handles many clients at once; resources are stored centrally so every student sees the same updated material. Firewalls / VPN protect the campus network.",
]),

("h", "7. Protocols"),
("q", "Protocol is usually associated with the software components of the network, explain with the aid of examples what a protocol is.", "2025 Q2a", "5"),
("p", "A **protocol** is a set of rules that govern data communication - it defines **what** is communicated, **how** it is communicated and **when**. Key elements:"),
("b", [
 "**Syntax** - structure/format of the data (e.g. first 8 bits = source address).",
 "**Semantics** - meaning of each section of bits and what action to take.",
 "**Timing** - when data should be sent and how fast.",
]),
("p", "Examples: **HTTP/HTTPS** (web pages), **SMTP/POP3/IMAP** (email), **FTP** (file transfer), **TCP/UDP** (transport), **IP** (addressing & routing), **DNS** (name resolution), **DHCP** (automatic IP configuration), **Ethernet** (LAN framing)."),
("p", "**Standards**: de facto (by convention) vs de jure (by law/official body). Bodies: ISO, ITU-T, ANSI, IEEE, EIA, IETF."),

("h", "8. Internet vs World Wide Web; Internet services"),
("q", "Distinguish between the internet and the World Wide Web.", "SE2024 Q4a", "4"),
("t", [
 ["Internet", "World Wide Web (WWW)"],
 ["Global network of interconnected networks (hardware + infrastructure)", "A service/application that runs ON the Internet"],
 ["Uses TCP/IP", "Uses HTTP/HTTPS, HTML, URLs"],
 ["Carries email, FTP, VoIP, gaming, WWW...", "Collection of linked web pages / hypertext documents"],
 ["Started 1969 (ARPANET)", "Invented by Tim Berners-Lee, 1989-1991"],
]),
("q", "The internet offers a variety of services to users. List and explain any four.", "SE2024 Q5c", "4"),
("b", [
 "**World Wide Web** - browsing web pages and web apps (HTTP).",
 "**Email** - sending/receiving electronic mail (SMTP, POP3, IMAP).",
 "**File transfer** - uploading/downloading files (FTP, SFTP), cloud storage.",
 "**Communication** - VoIP calls, video conferencing (Zoom), instant messaging (WhatsApp).",
 "Others: remote login (Telnet/SSH), e-commerce & e-banking, online learning, social media, streaming.",
]),

("h", "9. Basic network requirements: hardware, software, protocols"),
("q", "A basic computer network must consist of at least hardware, software and protocols. Give examples of each and explain their implementation.", "SE2024 Q4d", "4"),
("t", [
 ["Requirement", "Examples", "Implementation / role"],
 ["Hardware", "NICs, cables (UTP, fibre), switches, routers, access points, servers, PCs", "Physically connect devices and move signals; switch connects LAN devices, router connects networks"],
 ["Software", "Network OS (Windows Server, Linux), drivers, browsers, email clients, firewall software", "Manage resources, users and applications that use the network"],
 ["Protocols", "TCP/IP, Ethernet, HTTP, DHCP, DNS", "Rules so devices can understand each other: addressing, delivery, error control"],
]),

("h", "10. Network design scenario"),
("q", "Identify appropriate network topology and network connecting devices. Draw a network design for an organisation having its office in a building of 5 floors. Each floor needs 20 machines.", "SE2024 Q3e", "5"),
("pre", """
                         INTERNET
                            |
                       [ ISP modem ]
                            |
                     [ Router + Firewall ]
                            |
                 [ Core / distribution switch ]   <- ground floor server room (+ servers)
          ________|_______|_______|_______|_______
         |        |       |       |       |
    [Sw F1]   [Sw F2]  [Sw F3]  [Sw F4]  [Sw F5]   24-port access switch per floor
     |...|     |...|    |...|    |...|    |...|     (fibre or Cat6 uplink to core)
    20 PCs    20 PCs   20 PCs   20 PCs   20 PCs    + 1 Wi-Fi access point per floor
"""),
("b", [
 "**Topology:** extended / hierarchical **star (tree)** - a star on each floor, all floor switches connected to a core switch.",
 "**Devices:** one 24-port switch per floor (20 PCs + AP + uplink), core switch, router (connects to ISP/Internet), firewall, wireless access points, Cat6 UTP to desks, fibre/Cat6 vertical backbone.",
 "Use one **VLAN/subnet per floor** (e.g. 192.168.10.0/27 ... 192.168.50.0/27 - each /27 gives 30 hosts for 20 PCs + growth). DHCP server for addressing.",
 "Why: easy to manage, one failed floor switch only affects that floor, easy to expand.",
]),

("h", "11. Competencies of professionals (SE2024 Q4e)"),
("b", [
 "**Network administrator** [1] - day-to-day running: configuring and monitoring the network, user accounts, backups, troubleshooting, patching, keeping it available.",
 "**Network engineer** [2] - designs and plans networks (topology, addressing, routing), selects and installs equipment (routers, switches, firewalls), optimises performance and security; certifications such as CCNA/CCNP.",
 "**Hacker** [1] - person with deep technical skills who finds and exploits vulnerabilities in systems; ethical (white-hat) hackers do this legally for penetration testing, black-hat hackers do it maliciously.",
]),

("h", "12. Goals & applications of networks (outline week 1)"),
("b", [
 "**Resource sharing** - printers, files, Internet connection.",
 "**Communication** - email, messaging, video conferencing.",
 "**Reliability** - multiple copies of data/alternative paths.",
 "**Cost reduction** - share expensive hardware/software.",
 "**Centralised management, scalability, remote access.**",
 "Applications: e-banking, e-learning, e-commerce, cloud services, IoT, telemedicine.",
]),
("key", "In a 25-mark question, examiners award ~1 mark per correct point + 1 for an example. 'Explain' = definition + how it works + example. 'Differentiate' = use a TABLE."),
]
