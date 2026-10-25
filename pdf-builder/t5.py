TITLE = "Topic 5: Network Layer - IPv4, Subnetting/VLSM, IPv6 & DHCP"
SUB = "Course outline weeks 5-7: internetworking, TCP/IP, the IP packet, IP address, IPv6. A subnetting calculation appears in EVERY paper (6-12 marks) - this is the topic that wins or loses the exam."
FILE = "05_IP_Addressing_Subnetting_IPv6.pdf"

C = [
("h", "How often this topic is examined"),
("t", [
 ["Question asked", "Paper(s)", "Marks"],
 ["Subnetting calculation (subnets, hosts, ranges, broadcast)", "2018 Q3a [10], 2023 Q1d [6] + Q3c [4], ISA2024 Q1d [6], 2025 Q4a [12]", "4-12"],
 ["IPv4 header: draw it + purpose of fields", "2023 Q1a [6], ISA2024 Q1a [7]", "6-7"],
 ["IPv6 header diagram", "2018 Q1d", "5"],
 ["Advantages of IPv6 over IPv4", "2023 Q1b", "5"],
 ["Shorten IPv6 addresses", "2023 Q5e [2], ISA2024 Q3a [1]", "1-2"],
 ["SLAAC vs DHCPv6", "2025 Q3b [6], ISA2024 Q5d [8]", "6-8"],
 ["Purpose & benefits of subnetting; concept of IP addressing & subnetting", "2025 Q4b [6], ISA2024 Q2b [5]", "5-6"],
 ["DHCP four-step (DORA) process with diagrams", "2018 Q4a", "10"],
 ["Static vs dynamic IP address", "SE2024 Q1b.iv", "2"],
]),
("tip", "Practise the method on page 3 until you can do a subnetting question in under 10 minutes. ALWAYS show working (binary of the mask, block size, table) - most of the marks are for the working."),

("h", "1. IPv4 addressing basics"),
("p", "An **IPv4 address** is a **32-bit logical address** written in **dotted-decimal** notation as four octets, e.g. 192.168.1.10 = 11000000.10101000.00000001.00001010. It has a **network part** (identifies the network) and a **host part** (identifies the device). The **subnet mask** shows which bits are network (1s) and which are host (0s). Address space = 2^32 = ~4.3 billion."),
("t", [
 ["Class", "First octet", "Leading bits", "Default mask", "Networks / hosts", "Private range"],
 ["A", "1 - 126", "0", "255.0.0.0 (/8)", "126 nets, 16,777,214 hosts", "10.0.0.0 - 10.255.255.255"],
 ["B", "128 - 191", "10", "255.255.0.0 (/16)", "16,384 nets, 65,534 hosts", "172.16.0.0 - 172.31.255.255"],
 ["C", "192 - 223", "110", "255.255.255.0 (/24)", "2,097,152 nets, 254 hosts", "192.168.0.0 - 192.168.255.255"],
 ["D", "224 - 239", "1110", "-", "Multicast", "-"],
 ["E", "240 - 255", "1111", "-", "Reserved/experimental", "-"],
]),
("p", "127.x.x.x = loopback (127.0.0.1). **Network address** = all host bits 0; **broadcast address** = all host bits 1; neither can be given to a host, hence **usable hosts = 2^h - 2**."),
("b", [
 "**Classful vs classless (CIDR):** CIDR drops fixed classes; the prefix length (/n) says how many bits are network, e.g. 14.24.74.0/24. Allows efficient allocation and route aggregation (supernetting).",
 "**NAT (Network Address Translation):** router translates private addresses to a public address so many hosts share one public IP; conserves IPv4 and hides internal hosts.",
]),
("h3", "Static vs dynamic IP (SE2024 Q1b.iv)"),
("t", [
 ["Static IP", "Dynamic IP"],
 ["Manually configured; **does not change**", "Assigned automatically by a **DHCP server** for a lease period; **may change**"],
 ["Used for servers, printers, routers - things others must find", "Used for client PCs, phones"],
 ["More admin effort, risk of conflicts; good for hosting/remote access", "Easy to manage, efficient reuse of addresses"],
]),
("q", "Explain the purpose of subnetting and the benefits it provides to network administrators. / Discuss the concept of IP addressing and subnetting.", "2025 Q4b [6], ISA2024 Q2b [5]", "5-6"),
("p", "**Subnetting** = dividing one large network into smaller logical networks (**subnets**) by **borrowing bits from the host part** to make a longer subnet mask."),
("b", [
 "**Reduces broadcast traffic** - each subnet is its own broadcast domain -> better performance and less congestion.",
 "**Efficient use of addresses** - allocate the right size block to each department (VLSM), less waste.",
 "**Security** - traffic between subnets passes through a router/firewall where ACLs can be applied; isolates sensitive departments.",
 "**Easier management & troubleshooting** - problems are confined to a subnet; logical organisation by department/floor/location.",
 "**Scalability** - easy to add new subnets as the organisation grows; route summarisation keeps routing tables small.",
]),

("h", "2. The subnetting method (learn this)"),
("pre", """
 Mask value per borrowed bit in an octet:
   bits:   1    2    3    4    5    6    7    8
   mask: 128  192  224  240  248  252  254  255
   block: 128   64   32   16    8    4    2    1      block size = 256 - mask octet

 Prefix ->  hosts (2^h - 2):   /24 254 | /25 126 | /26 62 | /27 30 | /28 14 | /29 6 | /30 2

 STEP 1  Find the class / default mask and the given mask -> number of borrowed bits (s)
 STEP 2  Number of subnets = 2^s
 STEP 3  Host bits h = 32 - prefix ;  usable hosts = 2^h - 2
 STEP 4  Block size = 256 - (interesting octet of the mask)
 STEP 5  Subnets go up in block sizes: network = multiple of block;
         broadcast = next network - 1 ; first host = network + 1 ; last host = broadcast - 1
"""),

("h", "3. Worked past-paper calculations"),
("q", "Given the network 172.16.0.0 with a subnet mask of 255.255.252.0: i) Which class? ii) Number of possible subnets. iii) Usable hosts per subnet. iv) Network & broadcast addresses for the first two subnets. v) Valid host ranges for the first three subnets.", "2025 Q4a", "12"),
("pre", """
 255.255.252.0 = 11111111.11111111.11111100.00000000  = /22
 i)   First octet 172 is in 128-191  ->  CLASS B  (default /16)
 ii)  Borrowed bits s = 22 - 16 = 6   ->  2^6 = 64 subnets
 iii) Host bits h = 32 - 22 = 10      ->  2^10 - 2 = 1024 - 2 = 1022 usable hosts per subnet
      Block size = 256 - 252 = 4  (in the THIRD octet)

 | Subnet | Network address | First host    | Last host      | Broadcast       |
 |   1    | 172.16.0.0      | 172.16.0.1    | 172.16.3.254   | 172.16.3.255    |
 |   2    | 172.16.4.0      | 172.16.4.1    | 172.16.7.254   | 172.16.7.255    |
 |   3    | 172.16.8.0      | 172.16.8.1    | 172.16.11.254  | 172.16.11.255   |
 iv)  Subnet 1: network 172.16.0.0, broadcast 172.16.3.255
      Subnet 2: network 172.16.4.0, broadcast 172.16.7.255
 v)   172.16.0.1 - 172.16.3.254 ; 172.16.4.1 - 172.16.7.254 ; 172.16.8.1 - 172.16.11.254
"""),
("q", "You have sub-netted your class C network 192.168.1.0 with a subnet mask of 255.255.255.240. Calculate: i) number of networks ii) hosts per network iii) the full range of the first three networks iv) the usable address ranges of those first three networks.", "ISA2024 Q1d", "6"),
("pre", """
 255.255.255.240 = /28  -> last octet 11110000 : borrowed 4 bits, 4 host bits
 i)   Networks = 2^4 = 16
 ii)  Hosts per network = 2^4 - 2 = 14
      Block size = 256 - 240 = 16
 | Net | Full range (network - broadcast)   | Usable host range            |
 |  1  | 192.168.1.0  - 192.168.1.15        | 192.168.1.1  - 192.168.1.14  |
 |  2  | 192.168.1.16 - 192.168.1.31        | 192.168.1.17 - 192.168.1.30  |
 |  3  | 192.168.1.32 - 192.168.1.47        | 192.168.1.33 - 192.168.1.46  |
"""),
("q", "A host was given the IP address 198.168.4.121/27. Indicate: i) the network address ii) the broadcast address iii) the total number of hosts available iv) whether 192.168.4.93 can be the default gateway of the host. Explain.", "2023 Q3c", "4"),
("pre", """
 /27 -> mask 255.255.255.224, block size = 256 - 224 = 32
 Subnets in last octet: 0, 32, 64, 96, 128 ...   121 lies between 96 and 127
 i)   Network address   = 198.168.4.96
 ii)  Broadcast address = 198.168.4.127
 iii) Hosts = 2^5 - 2 = 30   (usable 198.168.4.97 - 198.168.4.126)
 iv)  NO. A default gateway must be in the SAME subnet as the host.
      192.168.4.93 is not in 198.168.4.96/27: its network part is different (192 vs 198),
      and even in the last octet, .93 falls in the .64 - .95 subnet, not .96 - .127.
      The gateway should be e.g. 198.168.4.97 or 198.168.4.126.
"""),
("q", "Considering IPv4 classless addressing, an organization is granted a block 14.24.74.0/24. It needs 3 subnets: one of 120 addresses, one of 60, one of 10. Show the network address and subnet mask of each subnet using VLSM. Show all working.", "2023 Q1d", "6"),
("pre", """
 VLSM RULE: sort the requirements LARGEST first, give each the smallest block that fits.
 Need 120 -> 2^7 = 128 (>=120+2) -> 7 host bits -> /25 -> mask 255.255.255.128
 Need 60  -> 2^6 = 64  (>=60+2)  -> 6 host bits -> /26 -> mask 255.255.255.192
 Need 10  -> 2^4 = 16  (>=10+2)  -> 4 host bits -> /28 -> mask 255.255.255.240

 | Subnet | Network        | Mask             | Range              | Usable hosts           |
 | 120    | 14.24.74.0/25  | 255.255.255.128  | .0   - .127        | 14.24.74.1   - .126    |
 | 60     | 14.24.74.128/26| 255.255.255.192  | .128 - .191        | 14.24.74.129 - .190    |
 | 10     | 14.24.74.192/28| 255.255.255.240  | .192 - .207        | 14.24.74.193 - .206    |
 Unused for future growth: 14.24.74.208 - 14.24.74.255 (48 addresses)
"""),
("q", "Company ABC: Accounts 10, HR 4, IT 4, Sales & Marketing 20 employees. Using 192.168.0.0/24, design a subnetting scheme that does not waste addresses and caters for an additional two members in each subnet.", "2018 Q3a", "10"),
("pre", """
 Hosts needed (+2 each):  Sales 22 | Accounts 12 | HR 6 | IT 6     (sort largest first)
 Sales    22 -> 2^5=32 -> 30 usable -> /27  255.255.255.224  block 32
 Accounts 12 -> 2^4=16 -> 14 usable -> /28  255.255.255.240  block 16
 HR        6 -> 2^3=8  ->  6 usable -> /29  255.255.255.248  block 8
 IT        6 -> 2^3=8  ->  6 usable -> /29  255.255.255.248  block 8

 | Dept     | Network          | Mask             | Usable hosts                   | Broadcast     |
 | Sales    | 192.168.0.0/27   | 255.255.255.224  | 192.168.0.1  - 192.168.0.30    | 192.168.0.31  |
 | Accounts | 192.168.0.32/28  | 255.255.255.240  | 192.168.0.33 - 192.168.0.46    | 192.168.0.47  |
 | HR       | 192.168.0.48/29  | 255.255.255.248  | 192.168.0.49 - 192.168.0.54    | 192.168.0.55  |
 | IT       | 192.168.0.56/29  | 255.255.255.248  | 192.168.0.57 - 192.168.0.62    | 192.168.0.63  |
 Total used 64 addresses; 192.168.0.64 - 192.168.0.255 left free for future subnets.
 (Note: if you must also reserve one address per subnet for the router/gateway, HR and IT
  need 7 -> use /28 each: HR 192.168.0.48/28, IT 192.168.0.64/28. State your assumption.)
"""),
("tip", "VLSM: always start with the BIGGEST subnet, and always check '2^h - 2 >= hosts needed'. Write the assumption you make (e.g. 'gateway included')."),

("h", "4. The IPv4 header"),
("q", "Draw the typical structure of an IP header and state the purpose of the fields: Time to live, Protocol, Source and Destination IP addresses. / State the purpose of: Version, Differentiated services, TTL, Protocol, Source IP, Destination IP.", "ISA2024 Q1a [7], 2023 Q1a [6]", "6-7"),
("pre", """
  0        4        8                16    19                         31
 +--------+--------+-----------------+-------------------------------+
 |Version |  IHL   | DSCP / ToS (8)  |        Total Length (16)      |
 |  (4)   |  (4)   |                 |                               |
 +--------+--------+-----------------+-----+-------------------------+
 |       Identification (16)         |Flags|  Fragment Offset (13)   |
 |                                   | (3) |                         |
 +-----------------+-----------------+-----+-------------------------+
 | Time to Live (8)|  Protocol (8)   |      Header Checksum (16)     |
 +-----------------+-----------------+-------------------------------+
 |                    Source IP Address (32)                         |
 +-------------------------------------------------------------------+
 |                  Destination IP Address (32)                      |
 +-------------------------------------------------------------------+
 |              Options (variable)            |      Padding         |
 +-------------------------------------------------------------------+
            Header = 20 bytes minimum, 60 bytes maximum
"""),
("t", [
 ["Field", "Purpose"],
 ["Version (4 bits)", "IP version number - 4 for IPv4, so the router knows how to interpret the header"],
 ["Header Length / IHL (4)", "Length of the header in 32-bit words (5 = 20 bytes, max 15 = 60 bytes)"],
 ["Differentiated Services / ToS (8)", "Packet **priority / class of service** for QoS (DSCP 6 bits + ECN 2 bits) - e.g. VoIP marked high priority"],
 ["Total Length (16)", "Length of the whole datagram (header + data), max 65,535 bytes"],
 ["Identification, Flags, Fragment Offset", "Used for **fragmentation and reassembly**: ID groups fragments, flags DF (don't fragment) & MF (more fragments), offset gives position"],
 ["Time to Live (8)", "Maximum number of **hops** (routers) the packet may pass; each router decrements it by 1 and **discards the packet at 0** (sending ICMP Time Exceeded) - stops packets looping forever"],
 ["Protocol (8)", "Identifies the **upper-layer protocol** the data belongs to so it is delivered correctly: 1 = ICMP, 6 = TCP, 17 = UDP, 89 = OSPF"],
 ["Header Checksum (16)", "Error detection on the header only; recomputed at each router"],
 ["Source IP address (32)", "Logical address of the **original sender**; used by the receiver to reply"],
 ["Destination IP address (32)", "Logical address of the **final receiver**; routers use it to make **forwarding/routing decisions**"],
 ["Options + Padding", "Optional: security, record route, source routing, timestamp; padding makes header a multiple of 32 bits"],
]),

("h", "5. IPv6"),
("p", "**IPv6** uses **128-bit** addresses written as **8 groups of 4 hex digits** separated by colons, e.g. 2001:0DB8:0000:1470:0000:0000:0000:0200. Types: **unicast** (global unicast 2000::/3, link-local FE80::/10, unique local FC00::/7), **multicast** (FF00::/8), **anycast**. There is **no broadcast**."),
("h3", "Shortening rules"),
("n", [
 "Remove **leading zeros** in any group (0DB8 -> DB8, 0000 -> 0, 0200 -> 200).",
 "Replace **one** run of consecutive all-zero groups with **::** (only once per address - use it on the longest run).",
]),
("q", "Express in shortened form: i) 2001:0DB8:0000:1470:0000:0000:0000:0200  ii) F380:0000:0000:0000:0123:4567:89AB:CDEF  iii) 2001:0DB8:0000:1470:0000:0000:0000:0300", "2023 Q5e [2], ISA2024 Q3a [1]", "1-2"),
("pre", """
 i)   2001:0DB8:0000:1470:0000:0000:0000:0200
      -> 2001:DB8:0:1470:0:0:0:200  ->  2001:DB8:0:1470::200
 ii)  F380:0000:0000:0000:0123:4567:89AB:CDEF
      -> F380:0:0:0:123:4567:89AB:CDEF  ->  F380::123:4567:89AB:CDEF
 iii) 2001:0DB8:0000:1470:0000:0000:0000:0300  ->  2001:DB8:0:1470::300
 (NOT 2001:DB8::1470::300 - you may use :: only once)
"""),
("q", "Draw a fully labelled diagram of the IPv6 header.", "2018 Q1d", "5"),
("pre", """
  0        4               12                                       31
 +--------+----------------+-----------------------------------------+
 |Version | Traffic Class  |              Flow Label (20)            |
 |  (4)   |     (8)        |                                         |
 +--------+----------------+-------------+--------------+------------+
 |        Payload Length (16)            | Next Header  | Hop Limit  |
 |                                       |    (8)       |    (8)     |
 +---------------------------------------+--------------+------------+
 |                                                                   |
 |                  Source Address (128 bits)                        |
 |                                                                   |
 +-------------------------------------------------------------------+
 |                                                                   |
 |                Destination Address (128 bits)                     |
 |                                                                   |
 +-------------------------------------------------------------------+
         Fixed header = 40 bytes (extension headers follow if needed)
"""),
("b", [
 "**Version** = 6. **Traffic class** = priority/QoS (like IPv4 DSCP). **Flow label** = identifies packets of the same flow needing special handling (real-time audio/video).",
 "**Payload length** = length of data after the 40-byte header. **Next header** = type of the next (extension or upper-layer) header (like IPv4 Protocol). **Hop limit** = like TTL.",
 "Removed from IPv4: header length, checksum, fragmentation fields (moved to extension headers), options.",
]),
("q", "Indicate five advantages of IPv6 over IPv4.", "2023 Q1b", "5"),
("n", [
 "**Huge address space** - 128 bits = 3.4 x 10^38 addresses; solves IPv4 exhaustion, every device can have a global address (no need for NAT -> true end-to-end connectivity).",
 "**Simplified, fixed 40-byte header** - fewer fields, no header checksum, no router fragmentation -> **faster routing/processing**.",
 "**Built-in security** - IPsec support (authentication & encryption) is part of the design.",
 "**Auto-configuration** - SLAAC lets hosts configure their own address (plug-and-play); also stateful DHCPv6.",
 "**Better QoS** - flow label and traffic class for real-time traffic.",
 "Also: efficient **multicast & anycast**, no broadcast storms; better **mobility** (Mobile IPv6); extension headers make it extensible; hierarchical addressing gives smaller routing tables.",
]),

("h", "6. SLAAC vs DHCPv6"),
("q", "Global unicast IPv6 addresses can be assigned dynamically using SLAAC and DHCPv6. Compare and contrast them, explaining the key differences in how they assign IPv6 addresses.", "2025 Q3b [6], ISA2024 Q5d [8]", "6-8"),
("pre", """
 SLAAC                                          STATEFUL DHCPv6
 Host --RS (Router Solicitation, FF02::2)-->R   Host --RS--> Router
 Host <--RA: prefix 2001:DB8:1::/64, M=0 ---R   Host <--RA: M flag = 1 ("use DHCPv6")
 Host builds Interface ID (EUI-64 / random)     Host --SOLICIT--> DHCPv6 server (FF02::1:2)
 2001:DB8:1:: + 021A:2BFF:FE3C:4D5E             Host <--ADVERTISE--
 Host runs DAD (Duplicate Address Detection)    Host --REQUEST-->
 No server keeps a record                       Host <--REPLY: address + DNS, lease --
"""),
("t", [
 ["Point", "SLAAC (Stateless Address Auto-Configuration)", "DHCPv6 (stateful)"],
 ["Who creates the address", "**The host itself**: takes the /64 **prefix from the router's RA** message and generates its own 64-bit **interface ID** (EUI-64 from its MAC, or random for privacy)", "A **DHCPv6 server** assigns the complete address from its pool"],
 ["Server needed?", "**No server** - only a router sending Router Advertisements", "Requires a DHCPv6 server (or router acting as one)"],
 ["State / tracking", "**Stateless** - nobody records which host has which address", "**Stateful** - server keeps a lease database (who has what) - better for auditing/accounting"],
 ["Messages", "ICMPv6 Router Solicitation (RS) & Router Advertisement (RA); DAD via Neighbour Solicitation", "Solicit, Advertise, Request, Reply (UDP ports 546/547)"],
 ["Other info (DNS, domain)", "Limited - DNS via RA option (RDNSS) or **stateless DHCPv6** (RA O-flag = 1)", "Can provide DNS servers, domain name and other options"],
 ["RA flags", "M = 0 (O = 0 SLAAC only; O = 1 SLAAC + stateless DHCPv6)", "M = 1 (managed address configuration)"],
 ["Control", "Less admin control, simple, plug-and-play, scales easily", "More control over addressing, easier to manage/secure in enterprises"],
 ["Default gateway", "Learned from RA (router's link-local address)", "Also learned from RA - DHCPv6 does **not** give a gateway"],
]),

("h", "7. DHCP (IPv4) - the DORA process"),
("q", "Describe the DHCP four step process with the aid of diagrams.", "2018 Q4a", "10"),
("p", "**DHCP (Dynamic Host Configuration Protocol)** automatically gives hosts an IP address, subnet mask, default gateway, DNS server and lease time. It uses **UDP - server port 67, client port 68**."),
("pre", """
   CLIENT (no IP yet, 0.0.0.0)                          DHCP SERVER
      |                                                      |
  1   |---- DHCPDISCOVER  (broadcast 255.255.255.255) ------>|  "Is there a DHCP server?"
      |                                                      |
  2   |<--- DHCPOFFER  (offers 192.168.1.50, mask, GW, DNS,--|  server reserves the address
      |                 lease time)                          |
  3   |---- DHCPREQUEST (broadcast: "I accept 192.168.1.50 --|  broadcast so other servers
      |                   from server X")                    |  withdraw their offers
  4   |<--- DHCPACK  (confirms lease, client configures IP)--|
      |                                                      |
   Client checks address with ARP; renews at 50% of lease (T1); DHCPNAK if request invalid
"""),
("n", [
 "**Discover** - a new client broadcasts a DHCPDISCOVER message to find any DHCP server on the network (source 0.0.0.0, destination 255.255.255.255).",
 "**Offer** - each server that receives it replies with a DHCPOFFER containing an available IP address, subnet mask, gateway, DNS and lease duration.",
 "**Request** - the client chooses one offer and broadcasts a DHCPREQUEST asking for that address (broadcast so other servers know their offers were declined).",
 "**Acknowledge** - the chosen server sends a DHCPACK confirming the lease; the client now configures its interface. (If the address is no longer available, a DHCPNAK is sent and the client restarts.)",
]),
("p", "Extra marks: lease renewal at 50% (unicast DHCPREQUEST), rebinding at 87.5%; DHCPRELEASE when shutting down; **DHCP relay agent** (ip helper-address) forwards broadcasts to a server on another subnet; static reservations by MAC address."),
("key", "Hosts = 2^h - 2. Subnets = 2^borrowed. Block = 256 - mask octet. /25=128 /26=64 /27=32 /28=16 /29=8 /30=4. IPv4 header 20 bytes, IPv6 header 40 bytes. TTL = hops; Protocol 6 = TCP, 17 = UDP. DORA. SLAAC = host makes its own address; DHCPv6 = server gives & remembers."),
]
