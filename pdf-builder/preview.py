"""Render named figures into a test PDF and PNGs: python preview.py figs1 [name ...]"""
import sys, importlib, os
import render  # registers fonts
from reportlab.platypus import SimpleDocTemplate, Spacer, Paragraph
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
import fitz
mod = importlib.import_module(sys.argv[1])
names = sys.argv[2:] or list(mod.FIGS)
os.makedirs("prev", exist_ok=True)
for n in names:
    path = "prev/%s.pdf" % n
    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=20*mm, rightMargin=20*mm, topMargin=10*mm, bottomMargin=10*mm)
    doc.build([Paragraph(n, render.base), mod.FIGS[n]()])
    pg = fitz.open(path)[0]
    pg.get_pixmap(dpi=110, clip=fitz.Rect(0, 0, 595, 420)).save("prev/%s.png" % n)
    print("ok", n)
