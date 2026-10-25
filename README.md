# ISS 2103 Data Communications & Networks: Exam Revision

My study material for the HIT data comms exam, made by King Tine, the AI Engineer.

## What's here

| Folder / file | Contents |
|---|---|
| `Exam Revision PDFs/` | **Start here.** 9 revision packs: an exam map plus 8 topics, with past questions, model answers and diagrams |
| `Exam Revision LaTeX/` | LaTeX version of the same packs (`src/*.tex`, built with `build.ps1`) |
| `pdf-builder/` | Python source that generates the PDFs in `Exam Revision PDFs/` |
| `DataCommunic ation.docx` | Course outline (ISE 2103) |
| `Data Communications 2018.pdf`, `DCN 2023.pdf`, `DCN 2024.pdf`, `Scanned_20251120_084126.pdf` (2025), `2.1.pdf` (ISA 2024 + other subjects) | Past exam papers |
| `datacomms notes.pdf` | Course notes |

## Topics

0. Exam map: question frequency per topic and paper, exam strategy, last-minute facts
1. Fundamentals: components, transmission modes, LAN/MAN/WAN, topologies, client-server
2. OSI & TCP/IP models
3. Physical layer: media, fibre, multiplexing, switching, ADSL
4. Data link & MAC: CSMA/CD/CA, ALOHA, error detection, bridges, switches, VLANs
5. IP addressing: subnetting/VLSM, IPv4/IPv6 headers, SLAAC vs DHCPv6, DHCP
6. Routing, congestion control, QoS, SDN, ISPs
7. Transport & application layers: TCP/UDP, handshake, DNS, troubleshooting
8. Security & emerging technologies

## Rebuilding the PDFs

Needs Python with `reportlab` (and `pymupdf` for `preview.py`). It uses the Windows Arial and Consolas fonts.

```bash
cd pdf-builder
python main.py "../Exam Revision PDFs" t0 t1 t2 t3 t4 t5 t6 t7 t8
```

- `t0.py` to `t8.py`: content of each pack
- `figs1.py` to `figs3.py`: diagrams (drawn with `dg.py` primitives)
- `render.py`: page layout
- `preview.py figs2 csma_cd`: renders a single diagram to `prev/` for checking
