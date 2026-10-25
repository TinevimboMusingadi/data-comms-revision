TITLE = "Topic 3: Physical Layer - Media, Signals, Multiplexing & Switching"
SUB = "Course outline weeks 1-2: physical layer transmission media, switching methods, ISDN, terminal handling. Switching appears in 4 of 5 papers."
FILE = "03_Physical_Layer_Media_Multiplexing_Switching.pdf"

C = [
("h", "How often this topic is examined"),
("t", [
 ["Question asked", "Paper(s)", "Marks"],
 ["Circuit vs packet (vs message) switching; examples; latency & jitter", "2023 Q5b [10], ISA2024 Q2d [8], SE2024 Q2c [4], 2025 Q3a [9]", "4-10"],
 ["Types of transmission media (list / explain / diagram for enterprise)", "2023 Q1e [4], 2025 Q2b.i [4], SE2024 Q4c [4]", "4"],
 ["Bounded vs unbounded media", "SE2024 Q1b.i", "2"],
 ["How fibre optic transmits data (diagram) + why fibre beats copper", "2023 Q3a [5], Q3b [6]", "11"],
 ["Multiplexing: concept & importance; components of a multiplexer; FDM vs TDM", "2025 Q2b.ii [4], SE2024 Q1b [4], Q2a [5]", "4-5"],
 ["Transmission impairments (attenuation, distortion, noise)", "SE2024 Q1d", "3"],
 ["Analogue vs digital signals", "SE2024 Q3c.ii", "2"],
 ["Modulation vs encoding with examples", "SE2024 Q5b", "6"],
 ["ADSL: why asymmetric; data + voice on the same line", "ISA2024 Q5b", "7"],
 ["GSM vs CDMA", "SE2024 Q1b.iii", "3"],
]),

("h", "1. Switching"),
("q", "Explain the concept of switching in networks. Differentiate between message switching, packet switching, and circuit switching.", "2025 Q3a", "9"),
("p", "**Switching** is the technique of directing data from a source to a destination through intermediate nodes (switches/routers) when there is no direct link between every pair of devices. It avoids the cost of a full mesh."),
("pre", """
 CIRCUIT SWITCHING            MESSAGE SWITCHING             PACKET SWITCHING
 1. Setup  A----S1----S2----B  A ==[whole msg]==> S1        A: msg split into P1 P2 P3
 2. Data   A====S1====S2====B     S1 stores, then           P1 --> S1 --> S3 --> B
           (dedicated path)       forwards ==> S2 ==> B     P2 --> S2 --> S3 --> B
 3. Teardown                   (store-and-forward,          P3 --> S1 --> S2 --> B
                                  no size limit)            (each may take a different route,
                                                             reassembled at B)
"""),
("t", [
 ["Feature", "Circuit switching", "Message switching", "Packet switching"],
 ["Path", "Dedicated physical path set up before data transfer and held for the whole call", "No dedicated path; whole message stored at each node then forwarded", "No dedicated path; message split into small packets, each routed independently (datagram) or along a virtual circuit"],
 ["Phases", "Setup -> data transfer -> teardown", "Store-and-forward", "Store-and-forward of packets"],
 ["Resource use", "Bandwidth reserved even when idle - wasteful", "Better use of links, but nodes need large storage", "Very efficient - links shared by many users (statistical multiplexing)"],
 ["Delay", "Setup delay, then constant low delay; no jitter", "High delay (whole message waits at every node)", "Variable delay (queuing) -> jitter; packets may arrive out of order"],
 ["Failure", "Link failure drops the call", "Message can be rerouted", "Packets rerouted around failure - robust"],
 ["Charging", "By time/distance", "By message", "By volume of data"],
 ["Example", "Traditional telephone (PSTN), ISDN", "Telegraph, early email systems", "Internet (IP), X.25, Frame Relay"],
]),
("q", "i) Explain the main difference between a circuit-switched network and a packet-switched network. ii) Give two examples of packet-switched protocols and two examples of circuit-switched protocols. iii) Indicate which one would have higher latency and jitter and explain why.", "2023 Q5b [4+4+2]; ISA2024 Q2d [4+4]", "10"),
("p", "**i)** In a **circuit-switched** network a dedicated end-to-end path with fixed bandwidth is established before communication and reserved for the whole session. In a **packet-switched** network no path is reserved: data is broken into packets that share links with other traffic and are forwarded independently (store-and-forward), possibly along different routes."),
("p", "**ii)** Packet-switched protocols: **IP (IPv4/IPv6)**, **X.25**, **Frame Relay**, ATM, Ethernet, MPLS. Circuit-switched: **ISDN**, **PSTN/POTS signalling (SS7)**, **GSM (2G voice)**, T1/E1 (TDM), SONET/SDH."),
("p", "**iii)** **Packet switching** has higher (variable) latency and jitter, because packets wait in router queues of different lengths, can take different routes and each node must store-and-forward them; so the delay changes from packet to packet. Circuit switching has a fixed dedicated path, so after setup the delay is constant (low jitter)."),
("p", "**Circuit switching (SE2024 Q2c.i, 2 marks):** dedicated path established for the duration of communication, e.g. telephone call. **Packet switching (Q2c.ii):** data split into packets with headers that travel independently and are reassembled at destination, e.g. the Internet."),

("h", "2. Transmission media"),
("q", "List any four types of transmission media. / Explain two types of transmission media. / Outline the difference between bounded and unbounded transmission media.", "2023 Q1e [4], 2025 Q2b.i [4], SE2024 Q1b.i [2]", "2-4"),
("pre", """
                     TRANSMISSION MEDIA
               _____________|_____________
              |                           |
      GUIDED (bounded/wired)      UNGUIDED (unbounded/wireless)
      |-- Twisted pair (UTP, STP)    |-- Radio waves (Wi-Fi, FM, 3 kHz-1 GHz, omnidirectional)
      |-- Coaxial cable              |-- Microwaves (1-300 GHz, line of sight, satellite, terrestrial)
      |-- Fibre optic cable          |-- Infrared (300 GHz-400 THz, short range, TV remote)
"""),
("t", [
 ["Bounded (guided)", "Unbounded (unguided)"],
 ["Signal travels along a **physical conductor** (copper/glass)", "Signal travels through **air/space/vacuum** as electromagnetic waves"],
 ["E.g. twisted pair, coaxial, fibre", "E.g. radio, microwave, infrared, satellite"],
 ["More secure, less interference, higher speed over the cable", "Mobility, easy to install over long distances/difficult terrain; less secure, affected by weather & interference"],
]),
("t", [
 ["Medium", "Description", "Use / features"],
 ["Twisted pair (UTP/STP)", "Pairs of insulated copper wires twisted to cancel crosstalk/EMI; RJ-45. Cat5e/Cat6", "LANs, telephone lines; cheap, easy; max ~100 m; susceptible to noise"],
 ["Coaxial cable", "Central copper core, insulator, braided metal shield, outer jacket", "Cable TV, older Ethernet (10Base2/5), CCTV; better shielding than UTP"],
 ["Fibre optic", "Thin glass/plastic core carries **light pulses** by total internal reflection; single-mode or multi-mode", "Backbones, WANs, undersea cables; very high bandwidth, long distance, immune to EMI; expensive, fragile"],
 ["Radio / microwave / satellite", "Electromagnetic waves through air", "Wi-Fi, mobile networks, point-to-point microwave links, VSAT"],
]),
("p", "**Media used in enterprise networks (SE2024 Q4c):** UTP Cat6 for horizontal cabling to desks; **fibre** for the backbone between floors/buildings and to the ISP; **wireless (Wi-Fi 802.11)** for mobile users; draw a building with fibre risers, UTP to PCs and an access point."),

("h", "3. Fibre optic cable"),
("q", "Using a diagram, explain how data is transmitted along a fibre optic cable. / Identify three physical characteristics of fibre optic cables that make them more suitable for high-speed digital data transmission over copper cables.", "2023 Q3a [5], Q3b [6]", "11"),
("pre", """
      +-----------------------------------------------------------+  outer jacket
      |  cladding (lower refractive index)                        |
      |   \\    /\\    /\\    /\\    /\\    /   <- light ray bounces  |
 LED/ |----\\--/--\\--/--\\--/--\\--/--\\--/------- CORE (glass) ----|---> photodetector
 LASER|     \\/    \\/    \\/    \\/    \\/       (higher index)      |    converts light
 (E->O)|  cladding                                                 |    back to electrical
      +-----------------------------------------------------------+       (O->E)
         Total internal reflection keeps light inside the core
"""),
("n", [
 "At the transmitter the electrical digital signal (1s and 0s) is converted into **light pulses** by an LED or laser diode (light ON = 1, OFF = 0).",
 "The light enters the **core** (glass with a high refractive index) at an angle greater than the **critical angle**.",
 "It is surrounded by **cladding** with a lower refractive index, so the light undergoes **total internal reflection** and bounces along the core with very little loss.",
 "Buffer coating and outer jacket protect the fibre.",
 "At the receiver a **photodetector (photodiode)** converts the light pulses back into electrical signals.",
 "Types: **single-mode** (thin core, one light path, laser, very long distance) and **multi-mode** (thicker core, many paths, LED, shorter distances).",
]),
("p", "**Why fibre is better than copper for high-speed data:**"),
("b", [
 "**Very high bandwidth** - light has extremely high frequency, giving Gbps-Tbps data rates.",
 "**Low attenuation** - signals travel tens of km without repeaters (copper UTP ~100 m).",
 "**Immune to electromagnetic interference (EMI) and crosstalk** because it carries light, not electricity - fewer errors.",
 "**Thin, light, and secure** - hard to tap without detection; no electrical sparks/ground loops.",
]),

("h", "4. Signals: analogue vs digital; impairments"),
("t", [
 ["Analogue signal", "Digital signal"],
 ["Continuous wave with **infinite** values in a range", "Discrete - **limited** number of values (e.g. 0 and 1)"],
 ["Described by amplitude, frequency, phase", "Described by bit rate & bit interval/level"],
 ["E.g. human voice, analogue telephone, AM/FM radio", "E.g. computer data, Ethernet signal"],
 ["More affected by noise; noise is hard to remove", "Can be regenerated by repeaters; more noise-immune"],
]),
("pre", """
  Analogue:   _      _      _          Digital:   ___     ___
            /  \\   /  \\   /  \\                   |   |   |   |
           /    \\_/    \\_/    \\             ____|   |___|   |___
"""),
("q", "Signals pick up unwanted random energy; discuss three such transmission impairments.", "SE2024 Q1d", "3"),
("b", [
 "**Attenuation** - loss of signal energy/strength as it travels through the medium (resistance). Fixed with **amplifiers/repeaters**. Measured in decibels (dB).",
 "**Distortion** - the signal changes shape because its different frequency components travel at different speeds and arrive at different times (common in composite signals/fibre = dispersion).",
 "**Noise** - unwanted random energy added to the signal: **thermal** (random electron motion), **induced** (motors, appliances), **crosstalk** (one wire affecting another), **impulse** (spikes from lightning, power lines). Signal-to-noise ratio (SNR) measures quality.",
]),
("p", "Extra: **Shannon capacity** C = B log2(1 + SNR); **Nyquist** (noiseless) bit rate = 2 x B x log2(L). Bandwidth = range of frequencies a channel passes (Hz)."),

("h", "5. Modulation vs encoding"),
("q", "Distinguish between modulation techniques versus encoding. Give two examples of each.", "SE2024 Q5b", "6"),
("t", [
 ["Modulation", "Encoding (line coding)"],
 ["Converts digital (or analogue) data into an **analogue signal** by varying a **carrier wave**'s amplitude, frequency or phase", "Converts digital data into a **digital signal** (pattern of voltage levels)"],
 ["Used for long-distance / wireless / telephone lines (bandpass channels)", "Used for short-distance baseband transmission (LAN cables)"],
 ["Examples: **ASK** (amplitude shift keying), **FSK** (frequency), **PSK** (phase), **QAM**; analogue: AM, FM", "Examples: **NRZ** (Non-Return-to-Zero), **Manchester** (Ethernet), Differential Manchester, AMI, RZ"],
 ["Device: modem (modulator-demodulator)", "Device: NIC / line coder"],
]),

("h", "6. Multiplexing"),
("q", "Describe the concept of multiplexing and its importance in data communication. / Describe the two components that make up a multiplexer.", "2025 Q2b.ii [4], SE2024 Q1b [4]", "4"),
("p", "**Multiplexing** is a technique that combines **multiple signals** from several sources into **one composite signal** so they can share a **single link/medium**. A **demultiplexer** at the other end separates them."),
("pre", """
   Source 1 ---\\                                      /--- Dest 1
   Source 2 ----[ MUX ] ===== one shared link ===== [ DEMUX ]---- Dest 2
   Source 3 ---/        (n channels on 1 link)       \\--- Dest 3
"""),
("b", [
 "**Two components:** (1) the **multiplexer (MUX)** - many-to-one: combines n input lines into one output stream; (2) the **demultiplexer (DEMUX)** - one-to-many: separates the stream and delivers each signal to its correct output line. (Between them is the shared link carrying n channels.)",
 "**Importance:** efficient use of expensive bandwidth; reduces cost (one cable instead of many); allows many users/calls to share a link (telephone trunks, cable TV, fibre backbones); simpler infrastructure.",
 "**Types:** **FDM**, **TDM** (synchronous & statistical), **WDM** (wavelength - for fibre), CDM.",
]),
("q", "Differentiate between Frequency Division Multiplexing (FDM) and Time Division Multiplexing (TDM).", "SE2024 Q2a", "5"),
("t", [
 ["FDM", "TDM"],
 ["Link bandwidth is divided into **frequency bands**; each signal gets its own band all the time", "Link time is divided into **time slots**; each signal uses the whole bandwidth for its slot in turn"],
 ["Mainly for **analogue** signals", "Mainly for **digital** signals"],
 ["Needs **guard bands** between channels to prevent overlap", "Needs **synchronisation** (framing bits); guard time between slots"],
 ["All signals transmitted **simultaneously**", "Signals transmitted **one after the other** in rotation"],
 ["Example: radio & TV broadcasting, cable TV, ADSL", "Example: digital telephone T1/E1 lines, GSM (time slots)"],
 ["Susceptible to crosstalk between bands", "Wasted slots if a source has nothing to send (synchronous TDM) - fixed by **statistical TDM**"],
]),
("pre", """
 FDM:  freq ^  | ch3 ================            TDM:  | A | B | C | A | B | C | ...
            |  | ch2 ================                   +---+---+---+---+---+---+--> time
            |  | ch1 ================                   frame 1     frame 2
            +--------------------> time
"""),

("h", "7. ADSL"),
("q", "i) Explain why ADSL is called asymmetric. ii) Describe how ADSL transmits both data and telephone calls over the same twisted pair without the two signals interfering.", "ISA2024 Q5b", "2 + 5"),
("p", "**i)** It is **asymmetric** because the **download (downstream) rate is much higher than the upload (upstream) rate** (e.g. 8-24 Mbps down vs ~1 Mbps up) - more bandwidth is allocated downstream because home users download far more than they upload."),
("p", "**ii)** ADSL uses **frequency division multiplexing** on the copper pair:"),
("b", [
 "**0-4 kHz**: ordinary voice telephone (POTS).",
 "**~25-138 kHz**: upstream data; **~138 kHz-1.1 MHz**: downstream data (DMT - discrete multitone - splits this into many 4 kHz sub-channels).",
 "Because voice and data occupy **different frequency bands**, they do not interfere.",
 "A **splitter / microfilter** at the home separates low frequencies (to the phone) from high frequencies (to the ADSL modem); at the exchange a **DSLAM** splits them again: voice to the telephone switch (PSTN), data to the ISP/Internet.",
]),
("pre", """
  |voice|  guard | upstream data |            downstream data              |
  0    4kHz     25kHz          138kHz                                     1.1MHz
  Phone <--[splitter]--> twisted pair <--> [splitter] -- voice -> PSTN switch
  Modem <--/                                          \\- data -> DSLAM -> ISP
"""),

("h", "8. GSM vs CDMA (SE2024 Q1b.iii)"),
("t", [
 ["GSM (Global System for Mobile communication)", "CDMA (Code Division Multiple Access)"],
 ["Uses **TDMA + FDMA**: each frequency channel split into time slots (8 users per carrier)", "All users share the **same frequency at the same time**; each separated by a unique **code** (spread spectrum)"],
 ["Uses a **SIM card** - easy to switch phones/networks", "Traditionally handset-bound (no SIM in early systems)"],
 ["Worldwide standard (Europe, Africa - Econet, NetOne)", "Used mainly in USA (Verizon, Sprint), parts of Asia"],
 ["Hard handoff; simpler; can't use voice & data together on 2G", "Soft handoff, better capacity and security; resistant to interference"],
]),
("p", "Similarity: both are 2G/3G multiple-access digital cellular technologies; both superseded by 4G LTE (OFDMA)."),

("h", "9. ISDN & terminal handling (outline topics - may be asked)"),
("b", [
 "**ISDN (Integrated Services Digital Network)** - a circuit-switched digital telephone network that carries voice, data, fax and video over ordinary copper lines. **BRI** = 2B + D (2 x 64 kbps bearer + 16 kbps signalling = 144 kbps). **PRI** = 23B + D (T1) or 30B + D (E1).",
 "**Terminal handling** - connecting many dumb terminals to a host cheaply using **multiplexers, concentrators** and **polling/selection** (the host asks each terminal in turn whether it has data).",
]),
("key", "Switching = 'how the path is found'; Multiplexing = 'how one link is shared'. Circuit = phone, Packet = Internet, Message = telegraph. FDM = frequency bands (radio), TDM = time slots (E1), WDM = colours of light (fibre)."),
]
