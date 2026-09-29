# -*- coding: utf-8 -*-
"""Blank axes for Q11(c): degrees 0 to 360, y marked at the max and min."""
import os
import pymupdf

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1700, 1080
OX, OY = 140.0, 760.0                     # origin
SX = (1520.0 - OX) / 360.0                # px per degree
SY = 90.0                                 # px per unit of y

o = ['<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" '
     'viewBox="0 0 %d %d" font-family="Liberation Serif, Georgia, serif" '
     'font-size="44">' % (W, H, W, H),
     '<rect width="100%" height="100%" fill="#ffffff"/>',
     '<defs><marker id="ah" markerWidth="10" markerHeight="10" refX="8" refY="3" '
     'orient="auto"><path d="M0,0 L9,3 L0,6 z" fill="#000"/></marker></defs>']


def line(x1, y1, x2, y2, w=4, arrow=False):
    o.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#000" '
             'stroke-width="%g"%s/>'
             % (x1, y1, x2, y2, w, ' marker-end="url(#ah)"' if arrow else ''))


def text(x, y, s, anchor="middle", italic=False):
    o.append('<text x="%.1f" y="%.1f" text-anchor="%s"%s>%s</text>'
             % (x, y, anchor, ' font-style="italic"' if italic else '', s))


line(60, OY, 1610, OY, 4, True)                       # x-axis
line(OX, 1010, OX, 90, 4, True)                       # y-axis
text(1655, OY + 15, "x", italic=True)
text(OX + 3, 60, "y", italic=True)

for d in (90, 180, 270, 360):
    x = OX + d * SX
    line(x, OY - 16, x, OY + 16, 4)
    text(x, OY + 78, "%d&#176;" % d)
for v, lab in ((5, "5"), (-1, "&#8722;1")):
    y = OY - v * SY
    line(OX - 16, y, OX + 16, y, 4)
    text(OX - 30, y + 15, lab, anchor="end")
text(OX - 30, OY - 8, "0", anchor="end")

o.append('</svg>')
svg = os.path.join(HERE, "assets", "q11axes_deg.svg")
open(svg, "w").write("\n".join(o))
d = pymupdf.open(svg)
pdf = pymupdf.open("pdf", d.convert_to_pdf())
png = os.path.join(HERE, "assets", "q11axes_deg.png")
pdf[0].get_pixmap(dpi=150).save(png)
print("wrote", png)
