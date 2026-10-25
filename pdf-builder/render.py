"""Tiny markup -> PDF renderer for the revision packs.

Content is a list of tuples:
  ("h", text)                 section heading
  ("h3", text)                sub heading
  ("p", text)                 paragraph (**bold**, *italic*)
  ("b", [items])              bullet list
  ("n", [items])              numbered list
  ("t", [[row], ...])         table, first row = header
  ("pre", text)               monospace block (diagrams / working)
  ("q", text, source, marks)  exam question box
  ("tip", text)               exam tip box
  ("key", text)               key-facts / memory box
  ("pb",)                     page break
"""
import re
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                TableStyle, Preformatted, PageBreak, KeepTogether,
                                ListFlowable, ListItem)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.fonts import addMapping

F = "C:/Windows/Fonts/"
pdfmetrics.registerFont(TTFont("Arial", F + "arial.ttf"))
pdfmetrics.registerFont(TTFont("Arial-B", F + "arialbd.ttf"))
pdfmetrics.registerFont(TTFont("Arial-I", F + "ariali.ttf"))
pdfmetrics.registerFont(TTFont("Arial-BI", F + "arialbi.ttf"))
pdfmetrics.registerFont(TTFont("Mono", F + "consola.ttf"))
addMapping("Arial", 0, 0, "Arial")
addMapping("Arial", 1, 0, "Arial-B")
addMapping("Arial", 0, 1, "Arial-I")
addMapping("Arial", 1, 1, "Arial-BI")

NAVY = colors.HexColor("#1f3a5f")
ACC = colors.HexColor("#2e6fb7")
QBG = colors.HexColor("#eaf1fb")
TBG = colors.HexColor("#fff4e0")
KBG = colors.HexColor("#e8f6ec")
GRID = colors.HexColor("#b8c4d4")

base = ParagraphStyle("base", fontName="Arial", fontSize=10, leading=14, spaceAfter=4)
S = {
    "title": ParagraphStyle("title", parent=base, fontName="Arial-B", fontSize=22, leading=27, textColor=NAVY, spaceAfter=4),
    "sub": ParagraphStyle("sub", parent=base, fontSize=11, textColor=colors.HexColor("#555555"), spaceAfter=10),
    "h": ParagraphStyle("h", parent=base, fontName="Arial-B", fontSize=14, leading=18, textColor=NAVY, spaceBefore=12, spaceAfter=6),
    "h3": ParagraphStyle("h3", parent=base, fontName="Arial-B", fontSize=11.5, leading=15, textColor=ACC, spaceBefore=8, spaceAfter=3),
    "p": base,
    "cell": ParagraphStyle("cell", parent=base, fontSize=9, leading=12, spaceAfter=0),
    "cellh": ParagraphStyle("cellh", parent=base, fontName="Arial-B", fontSize=9, leading=12, spaceAfter=0, textColor=colors.white),
    "box": ParagraphStyle("box", parent=base, spaceAfter=0),
    "cap": ParagraphStyle("cap", parent=base, fontSize=8.5, leading=11, alignment=1, textColor=colors.HexColor("#666666"), spaceBefore=3),
    "pre": ParagraphStyle("pre", fontName="Mono", fontSize=8.6, leading=10.8),
}


def md(text):
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<i>\1</i>", text)
    return text.replace("\n", "<br/>")


def box(flowables, bg, border):
    t = Table([[flowables]], colWidths=[170 * mm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), bg),
        ("LINEBEFORE", (0, 0), (0, -1), 3, border),
        ("LEFTPADDING", (0, 0), (-1, -1), 8), ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    return t


def lst(items, numbered=False):
    return ListFlowable(
        [ListItem(Paragraph(md(i), base), leftIndent=14) for i in items],
        bulletType="1" if numbered else "bullet", start=1 if numbered else None,
        bulletFontName="Arial", bulletFontSize=9 if not numbered else 10, leftIndent=14,
        bulletColor=ACC)


def table(rows):
    ncol = len(rows[0])
    data = [[Paragraph(md(c), S["cellh"]) for c in rows[0]]]
    data += [[Paragraph(md(str(c)), S["cell"]) for c in r] for r in rows[1:]]
    # width per column ~ sqrt of its average text length, so long-text columns get more room
    weights = [max(sum(len(str(r[i])) for r in rows) / len(rows), 4) ** 0.5 for i in range(ncol)]
    total = sum(weights)
    t = Table(data, colWidths=[170 * mm * w / total for w in weights], repeatRows=1)
    style = [
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("GRID", (0, 0), (-1, -1), 0.5, GRID),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]
    for i in range(2, len(data), 2):
        style.append(("BACKGROUND", (0, i), (-1, i), colors.HexColor("#f3f6fa")))
    t.setStyle(TableStyle(style))
    return t


def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Arial", 8)
    canvas.setFillColor(colors.grey)
    canvas.drawString(20 * mm, 10 * mm, doc.title)
    canvas.drawRightString(190 * mm, 10 * mm, "Page %d" % doc.page)
    canvas.setFont("Arial-B", 8)
    canvas.setFillColor(NAVY)
    canvas.drawCentredString(105 * mm, 5.5 * mm, "Made by King Tine, the AI Engineer")
    canvas.restoreState()


def build(path, title, subtitle, content):
    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm,
                            topMargin=18 * mm, bottomMargin=18 * mm, title=title,
                            author="ISS2103 revision pack")
    story = [Paragraph(md(title), S["title"]), Paragraph(md(subtitle), S["sub"])]
    for item in content:
        k = item[0]
        if k in ("h", "h3", "p"):
            story.append(Paragraph(md(item[1]), S[k]))
        elif k == "b":
            story += [lst(item[1]), Spacer(1, 4)]
        elif k == "n":
            story += [lst(item[1], True), Spacer(1, 4)]
        elif k == "t":
            story += [table(item[1]), Spacer(1, 8)]
        elif k == "pre":
            text = item[1].strip("\n")
            # shrink the font so the widest line fits the 154mm text width (Consolas ~0.55em/char)
            widest = max(len(l) for l in text.split("\n"))
            size = min(8.6, 154 * mm / (0.55 * widest))
            st = ParagraphStyle("pre_fit", parent=S["pre"], fontSize=size, leading=size * 1.25)
            story += [box([Preformatted(text, st)], colors.HexColor("#f6f6f6"), colors.HexColor("#999999")), Spacer(1, 8)]
        elif k == "q":
            _, text, src, marks = item
            p = Paragraph("<b>EXAM QUESTION</b>  <font color='#2e6fb7'>%s</font>  <b>[%s]</b><br/>%s" % (md(src), md(marks), md(text)), S["box"])
            story += [Spacer(1, 4), KeepTogether(box([p], QBG, ACC)), Spacer(1, 6)]
        elif k == "fig":
            import figs1, figs2, figs3
            figs = {**figs1.FIGS, **figs2.FIGS, **figs3.FIGS}
            parts = [figs[item[1]]()]
            if len(item) > 2 and item[2]:
                parts.append(Paragraph("<i>Figure: %s</i>" % md(item[2]), S["cap"]))
            story += [Spacer(1, 4), KeepTogether(parts), Spacer(1, 8)]
        elif k == "tip":
            story += [box([Paragraph("<b>EXAM TIP:</b> " + md(item[1]), S["box"])], TBG, colors.HexColor("#e39a1c")), Spacer(1, 8)]
        elif k == "key":
            story += [box([Paragraph("<b>REMEMBER:</b> " + md(item[1]), S["box"])], KBG, colors.HexColor("#2f9a4f")), Spacer(1, 8)]
        elif k == "pb":
            story.append(PageBreak())
        else:
            raise ValueError(k)
    doc.build(story, onFirstPage=footer, onLaterPages=footer)
