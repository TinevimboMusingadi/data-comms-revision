TITLE = "Topic 8: Network Security, Cryptography & Emerging Technologies"
SUB = "Course learning outcome 7 (network security & algorithms), presentation-layer cryptography (weeks 8-9) and week 12 emerging technologies."
FILE = "08_Network_Security_and_Emerging_Tech.pdf"

C = [
("h", "How often this topic is examined"),
("t", [
 ["Question asked", "Paper(s)", "Marks"],
 ["Four network security threats", "SE2024 Q2d", "3"],
 ["Harm caused by Trojans, worms, ransomware, spam", "SE2024 Q5a", "4"],
 ["DES vs AES", "2023 Q4c", "4"],
 ["Key Distribution Centre; Certification Authority", "2023 Q4d", "6"],
 ["How a VPN works", "ISA2024 Q2a", "3"],
 ["Emerging technologies (week 12)", "Course outline", "possible"],
]),

("h", "1. Security goals (use in any security answer)"),
("b", [
 "**Confidentiality** - only authorised people can read the data (encryption).",
 "**Integrity** - data is not altered in transit (hashes, MACs, digital signatures).",
 "**Availability** - services are available when needed (protection against DoS).",
 "Plus **authentication** (proving identity) and **non-repudiation** (sender can't deny sending).",
]),

("h", "2. Network security threats"),
("q", "Discuss any four network security threats you are familiar with.", "SE2024 Q2d", "3"),
("t", [
 ["Threat", "Explanation"],
 ["Malware", "Malicious software - viruses, worms, Trojans, ransomware, spyware - that damages systems or steals data"],
 ["Phishing / social engineering", "Fake emails/websites/calls trick users into revealing passwords or card details or installing malware"],
 ["Denial of Service (DoS/DDoS)", "Flooding a server/network with traffic (e.g. SYN flood, botnet) so legitimate users cannot access it - attacks availability"],
 ["Man-in-the-middle / eavesdropping (sniffing)", "Attacker intercepts and possibly alters traffic between two parties (ARP spoofing, rogue Wi-Fi) - attacks confidentiality & integrity"],
 ["Spoofing", "Faking an IP/MAC/email address or DNS response to impersonate a trusted host"],
 ["Password attacks / unauthorised access", "Brute-force, dictionary attacks, stolen credentials"],
 ["SQL injection / insider threats / zero-day exploits", "Exploiting application flaws or trusted employees misusing access"],
]),
("q", "Explain the harm caused by: Trojans, Worms, Ransomware, Spam.", "SE2024 Q5a", "4 x 1"),
("b", [
 "**Trojan (horse)** - malware disguised as legitimate software; once installed it opens a **backdoor**, giving attackers remote control, stealing data (passwords, banking details) or downloading more malware. It does **not self-replicate**.",
 "**Worm** - **self-replicating** malware that spreads across networks **without user action** by exploiting vulnerabilities; it consumes bandwidth and system resources (slowing/crashing networks) and can carry payloads (e.g. WannaCry, Conficker).",
 "**Ransomware** - **encrypts the victim's files** (or locks the system) and **demands a ransom** (usually cryptocurrency) for the decryption key; causes data loss, downtime and financial loss.",
 "**Spam** - unsolicited bulk email; wastes bandwidth, storage and time, reduces productivity, and is a common carrier of **phishing** links and malware.",
]),

("h", "3. Cryptography basics"),
("pre", """
  Plaintext --[ Encrypt with key ]--> Ciphertext ===network===> [ Decrypt with key ]--> Plaintext

  SYMMETRIC (secret key):   same key K to encrypt and decrypt     e.g. DES, 3DES, AES
       problem: how to share K securely  ->  Key Distribution Centre / Diffie-Hellman
  ASYMMETRIC (public key):  encrypt with receiver's PUBLIC key, decrypt with PRIVATE key  e.g. RSA, ECC
       problem: is this really Bob's public key?  ->  Certification Authority (certificates)
"""),
("q", "Highlight the major differences between DES and AES encryption methods.", "2023 Q4c", "4"),
("t", [
 ["Feature", "DES (Data Encryption Standard)", "AES (Advanced Encryption Standard)"],
 ["Adopted", "1977 by NIST (from IBM's Lucifer)", "2001 by NIST (Rijndael algorithm) - replaced DES"],
 ["Key length", "**56 bits** (64 with parity bits)", "**128, 192 or 256 bits**"],
 ["Block size", "**64-bit** blocks", "**128-bit** blocks"],
 ["Structure", "**Feistel network**", "**Substitution-permutation network** (SubBytes, ShiftRows, MixColumns, AddRoundKey)"],
 ["Rounds", "**16** rounds", "**10 / 12 / 14** rounds (for 128/192/256-bit keys)"],
 ["Security", "**Insecure** - broken by brute force (1998-99, under 24 h); 3DES used as stop-gap", "**Secure** - no practical attack; used worldwide (Wi-Fi WPA2/3, HTTPS, disk encryption)"],
 ["Speed", "Slower in software", "Faster and efficient in hardware and software"],
]),
("q", "Define the following terms as applied in network security: i) Key distribution center ii) Certification authority.", "2023 Q4d", "3 + 3"),
("p", "**i) Key Distribution Centre (KDC):** a **trusted third party** in **symmetric-key** systems that shares a secret key with every user and **creates and distributes temporary session keys** so two users can communicate securely without having met before. Instead of n(n-1)/2 keys, each user only needs one key with the KDC. Example: **Kerberos** (Authentication Server + Ticket-Granting Server issue tickets). Steps: Alice asks the KDC for a session key with Bob -> KDC sends the session key encrypted with Alice's key, plus a 'ticket' (the session key encrypted with Bob's key) -> Alice forwards the ticket to Bob."),
("p", "**ii) Certification Authority (CA):** a **trusted organisation that issues and signs digital certificates** binding a **public key to an identity** (person, server, domain) in a **Public Key Infrastructure (PKI)**. The CA verifies the identity, then signs the certificate (X.509) with its own private key so anyone can verify it with the CA's public key. It also **revokes** compromised certificates (CRL/OCSP). Examples: DigiCert, Let's Encrypt, GlobalSign - used for HTTPS/TLS."),

("h", "4. VPN"),
("q", "VPN can be essential in network security, briefly explain how VPN works.", "ISA2024 Q2a", "3"),
("pre", """
  [Remote user]==== encrypted TUNNEL over the public Internet ====[VPN gateway]--[Company LAN]
   VPN client         (original packet encrypted and encapsulated    firewall     file server
                       inside a new packet: | new IP hdr | ESP | encrypted original packet |)
"""),
("b", [
 "A **Virtual Private Network** creates a **secure, encrypted 'tunnel'** across a public network (the Internet) so remote users/branches can use the private network as if they were directly connected.",
 "The VPN client and VPN server/gateway **authenticate** each other (passwords, certificates, pre-shared keys) and agree encryption keys.",
 "Each original packet is **encrypted and encapsulated** (tunnelled) inside a new packet addressed to the VPN gateway; the gateway decrypts it and forwards it into the LAN.",
 "Provides **confidentiality** (encryption), **integrity** (hashing) and **authentication**; hides the user's real IP.",
 "Protocols: **IPsec** (AH/ESP, site-to-site), **SSL/TLS VPN**, **OpenVPN**, **WireGuard**, L2TP/IPsec. Types: **remote-access** and **site-to-site**.",
]),

("h", "5. Other security controls (good extra points)"),
("b", [
 "**Firewall** - filters traffic between networks using rules (packet filtering, stateful inspection, application/next-gen firewalls).",
 "**IDS/IPS** - detects/prevents intrusions by signature or anomaly.",
 "**DMZ** - separate zone for public servers (web, mail) between Internet and internal LAN.",
 "**Access control & authentication** - strong passwords, multi-factor authentication, 802.1X, ACLs on routers.",
 "**Encryption** - HTTPS/TLS, WPA3 for Wi-Fi, SSH instead of Telnet.",
 "**Patching, antivirus, backups, user awareness training, network segmentation/VLANs.**",
 "**Hashing / digital signatures** - MD5, SHA-256 for integrity; signature = hash encrypted with sender's private key (non-repudiation).",
]),

("h", "6. Emerging technologies (week 12 - 'discussion of modern trends')"),
("t", [
 ["Technology", "What it is / why it matters"],
 ["5G", "Mobile networks with very high speed (up to ~10 Gbps), ultra-low latency (~1 ms) and massive device density - enables IoT, smart cities, remote surgery"],
 ["Internet of Things (IoT)", "Billions of sensors/devices connected to the Internet (smart meters, agriculture sensors) - needs IPv6, low-power protocols (Zigbee, LoRaWAN), raises security issues"],
 ["Cloud computing", "On-demand computing & storage over the Internet: IaaS, PaaS, SaaS (AWS, Azure, Google Cloud)"],
 ["SDN & NFV", "Software-defined, programmable networks; Network Function Virtualisation runs routers/firewalls as software on standard servers"],
 ["Edge / fog computing", "Processing data near where it is generated to cut latency and bandwidth"],
 ["Wi-Fi 6/6E/7", "802.11ax/be: higher throughput, OFDMA, better performance in crowded areas"],
 ["Satellite Internet (LEO)", "Low-Earth-orbit constellations e.g. Starlink - broadband in rural areas (now in Zimbabwe)"],
 ["AI in networking, Zero Trust, IPv6 adoption, blockchain", "AI-driven network monitoring/automation; 'never trust, always verify' security model"],
]),
("key", "Trojan = disguised, backdoor, no self-copy. Worm = self-copies over the network. Ransomware = encrypts and demands payment. DES 56-bit key/64-bit block/16 rounds - broken; AES 128/192/256-bit key/128-bit block/10-14 rounds. KDC = symmetric session keys (Kerberos). CA = signs certificates for public keys (PKI). VPN = encrypted tunnel over the Internet."),
]
