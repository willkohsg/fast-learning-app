# -*- coding: utf-8 -*-
from docx import Document
from docx.shared import Pt, Cm, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT
from docx.enum.section import WD_SECTION
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import os
IMGDIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")

doc = Document()
for s in doc.sections:
    s.top_margin = Cm(2); s.bottom_margin = Cm(2)
    s.left_margin = Cm(2.2); s.right_margin = Cm(2.2)

st = doc.styles['Normal']
st.font.name = 'Times New Roman'; st.font.size = Pt(12)
st.element.rPr.rFonts.set(qn('w:eastAsia'), 'Times New Roman')
st.paragraph_format.space_after = Pt(0)

def p(text="", bold=False, italic=False, align=None, size=12, space_after=0, indent=None, hang=None):
    par = doc.add_paragraph()
    par.paragraph_format.space_after = Pt(space_after)
    if align == 'c': par.alignment = WD_ALIGN_PARAGRAPH.CENTER
    if align == 'r': par.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    if indent is not None: par.paragraph_format.left_indent = Cm(indent)
    if hang is not None: par.paragraph_format.first_line_indent = Cm(-hang)
    r = par.add_run(text); r.bold = bold; r.italic = italic; r.font.size = Pt(size)
    return par

def gap(n=1):
    for _ in range(n):
        doc.add_paragraph().paragraph_format.space_after = Pt(0)

def img(name, width_cm):
    par = doc.add_paragraph()
    par.alignment = WD_ALIGN_PARAGRAPH.CENTER
    par.paragraph_format.space_after = Pt(0)
    par.add_run().add_picture(os.path.join(IMGDIR, name), width=Cm(width_cm))
    return par

def q(num, text, marks, indent=1.5):
    """Numbered question with right-aligned mark allocation."""
    par = doc.add_paragraph()
    par.paragraph_format.space_after = Pt(0)
    par.paragraph_format.left_indent = Cm(indent)
    par.paragraph_format.first_line_indent = Cm(-indent)
    tabs = par.paragraph_format.tab_stops
    tabs.add_tab_stop(Cm(indent))
    tabs.add_tab_stop(Cm(16.0), WD_TAB_ALIGNMENT.RIGHT)
    par.add_run(("%s\t" % num) if num else "\t")
    par.add_run(text)
    if marks: par.add_run("\t[%s]" % marks)
    return par

def part(label, text, marks, indent=2.6):
    par = doc.add_paragraph()
    par.paragraph_format.space_after = Pt(0)
    par.paragraph_format.left_indent = Cm(indent)
    par.paragraph_format.first_line_indent = Cm(-1.1)
    tabs = par.paragraph_format.tab_stops
    tabs.add_tab_stop(Cm(indent))
    tabs.add_tab_stop(Cm(16.0), WD_TAB_ALIGNMENT.RIGHT)
    r = par.add_run("%s\t" % label); r.bold = True
    par.add_run(text)
    if marks: par.add_run("\t[%s]" % marks)
    return par

def pagebreak():
    doc.add_page_break()

# ---------------- COVER ----------------
p("SECONDARY 3 EXPRESS", bold=True, align='c', size=15)
p("END-OF-YEAR EXAMINATION", bold=True, align='c', size=15)
gap(1)
p("ADDITIONAL MATHEMATICS", bold=True, align='c', size=14)
p("4049", bold=True, align='c', size=14)
par = doc.add_paragraph(); par.paragraph_format.space_after = Pt(0)
par.paragraph_format.tab_stops.add_tab_stop(Cm(16.0), WD_TAB_ALIGNMENT.RIGHT)
r = par.add_run("Paper 1\t2 hours 15 minutes"); r.bold = True
gap(2)
p("CANDIDATE NAME:  ______________________________________________")
gap(1)
p("CLASS:  3 ________________            INDEX NUMBER:  ____________")
gap(1)
p("READ THESE INSTRUCTIONS FIRST", bold=True)
p("Write your full name, class and index number in the spaces above.")
p("Write in dark blue or black pen in the space provided for each question.")
p("You may use a HB pencil for any diagrams or graphs.")
p("Do not use staples, paper clips, highlighters, glue or correction fluid.")
gap(1)
p("Answer all the questions.")
p("The number of marks is given in brackets [ ] at the end of each question or part question.")
p("If working is needed for any question, it must be shown in the space below the question.")
p("Omission of essential working will result in loss of marks.")
p("The total of the marks for this paper is 90.")
gap(1)
p("The use of an approved scientific calculator is expected, where appropriate.")
p("If the degree of accuracy is not specified in the question and if the answer is not exact, give the answer to three significant figures. Give answers in degrees to one decimal place.")
p("For π, use either your calculator value or 3.142.")
gap(2)

marks_list = [3,4,4,4,4,5,5,7,7,7,8,10,10,12]
tbl = doc.add_table(rows=9, cols=6)
tbl.style = 'Table Grid'
tbl.alignment = WD_ALIGN_PARAGRAPH.CENTER
hdr = tbl.rows[0].cells
hdr[0].merge(hdr[5])
hp = tbl.rows[0].cells[0].paragraphs[0]
hp.add_run("For Examiner's Use").bold = True
hp.alignment = WD_ALIGN_PARAGRAPH.CENTER

def fill(cell, text, bold=False):
    pp = cell.paragraphs[0]
    pp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    pp.paragraph_format.space_after = Pt(0)
    r = pp.add_run(text); r.bold = bold; r.font.size = Pt(10)

for i in range(7):
    cells = tbl.rows[i+1].cells
    fill(cells[0], "Q%d" % (i+1), bold=True)
    fill(cells[1], str(marks_list[i]))
    fill(cells[2], "")
    if i < 7:
        j = i + 7
        if j < 14:
            fill(cells[3], "Q%d" % (j+1), bold=True)
            fill(cells[4], str(marks_list[j]))
        else:
            fill(cells[3], "Total", bold=True)
            fill(cells[4], "90", bold=True)
        fill(cells[5], "")
fill(tbl.rows[8].cells[3], "Total", bold=True)
fill(tbl.rows[8].cells[4], "90", bold=True)
fill(tbl.rows[8].cells[0], "")
fill(tbl.rows[8].cells[1], "")
fill(tbl.rows[8].cells[2], "")
fill(tbl.rows[8].cells[5], "")
for row in tbl.rows:
    for k, w in enumerate((2.0, 1.8, 2.4, 2.0, 1.8, 2.4)):
        row.cells[k].width = Cm(w)

gap(1)
p("This document consists of 18 printed pages including the cover page.", align='c', size=10)

pagebreak()

# ---------------- FORMULA SHEET ----------------
p("Mathematical Formulae", bold=True, italic=True, align='c')
gap(1)
p("1.  ALGEBRA", bold=True, align='c')
gap(1)
p("Quadratic Equation", italic=True)
p("For the equation  ax² + bx + c = 0,", align='c')
p("x = [ −b ± √(b² − 4ac) ] / 2a", align='c')
gap(1)
p("Binomial Expansion", italic=True)
p("(a + b)ⁿ = aⁿ + C(n,1)aⁿ⁻¹b + C(n,2)aⁿ⁻²b² + … + C(n,r)aⁿ⁻ʳbʳ + … + bⁿ", align='c')
p("where n is a positive integer and  C(n,r) = n! / [ r!(n − r)! ] = n(n−1)…(n−r+1) / r!", align='c')
gap(2)
p("2.  TRIGONOMETRY", bold=True, align='c')
gap(1)
p("Identities", italic=True)
p("sin²A + cos²A = 1", align='c')
p("sec²A = 1 + tan²A", align='c')
p("cosec²A = 1 + cot²A", align='c')
p("sin(A ± B) = sin A cos B ± cos A sin B", align='c')
p("cos(A ± B) = cos A cos B ∓ sin A sin B", align='c')
p("tan(A ± B) = (tan A ± tan B) / (1 ∓ tan A tan B)", align='c')
p("sin 2A = 2 sin A cos A", align='c')
p("cos 2A = cos²A − sin²A = 2cos²A − 1 = 1 − 2sin²A", align='c')
p("tan 2A = 2 tan A / (1 − tan²A)", align='c')
gap(1)
p("Formulae for ΔABC", italic=True)
p("a / sin A = b / sin B = c / sin C", align='c')
p("a² = b² + c² − 2bc cos A", align='c')
p("Δ = ½ ab sin C", align='c')

pagebreak()

# ---------------- QUESTIONS ----------------
p("Answer all the questions.", bold=True, align='c')
gap(1)

q("1", "The triangle DEF has an area of  ¼(7√3 + 9) cm². The length of DE is (√3 + 2) cm and angle EDF is 60°. Find, without using a calculator, the length of DF, in cm, in the form (a + b√3) where a and b are integers.", 3)
gap(11)

q("2", "Do not use a calculator in this question.", None)
part("(a)", "Simplify  7 / (3 \u2212 \u221a2), giving your answer in the form  a + b\u221a2, where a and b are integers.", 2)
gap(8)
part("(b)", "Given that  (2 + \u221a3)x = 5 + 4\u221a3, find the value of x in the form  a + b\u221a3, where a and b are integers.", 2)
pagebreak()

q("3", "It is given that  sin A = − 1/√5  and  tan B = 3/4, where A and B are in the same quadrant. Find the value of p if  cos(A − B) = p√5.", 4)
pagebreak()

q("4", "", None)
part("(i)", "Express  y = −2x² − 12x + 5  in the form  y = −a(x + b)² + c, where a, b and c are constants.", 2)
gap(10)
part("(ii)", "Hence find the range of values of the constant k for which the equation  −2x² − 12x + 5 = k  does not have two distinct roots.", 2)
pagebreak()

q("5", "The diagram below shows a plaque designed in the shape of an equilateral triangle sitting on top of a rectangle. The rectangle has height p m and width q m, and the equilateral triangle has side q m.", None)
gap(1)
img("plaque.png", 5.6)
gap(1)
part("(i)", "Given that the perimeter of the plaque is 10 m, express p in terms of q.", 2)
gap(9)
part("(ii)", "Show that the area of the plaque, A m², is given by  A = 5q − (3/2)q² + (√3/4)q².", 2)
pagebreak()

q("6", "Show that the line  y = x − 1  intersects the curve  y = nx² + 3x − n  at two distinct points for all real values of n.", 5)
pagebreak()

q("7", "Solve the equation   log₂(x − 2) + 2 log₄(x − 3) = ½ log₃ 9 .", 5)
pagebreak()

q("8", "The coordinates of the points A, B and C are (2, 3), (−1, −1) and (3, 1) respectively.", None)
gap(1)
part("(i)", "Show that AC is perpendicular to BC.", 3)
gap(8)
part("(ii)", "Given that ABCD is a parallelogram, find the coordinates of the point D.", 2)
gap(6)
part("(iii)", "Find the area of the parallelogram ABCD.", 2)
pagebreak()

q("9", "The curve  y = a cos 2x + b, where a > 0, has a maximum value of 4 and a minimum value of −10, for 0 ≤ x ≤ 2π.", None)
gap(1)
part("(i)", "Find the value of a and of b.", 3)
gap(7)
part("(ii)", "State the period and the amplitude of the curve  y = a cos 2x + b.", 2)
gap(5)
part("(iii)", "Sketch the curve of  y = a cos 2x + b  for 0 ≤ x ≤ 2π on the axes provided below.", 2)
gap(1)
img("trigaxes.png", 13.5)
pagebreak()

q("10", "Mr Goh bought an antique vase at the beginning of 2015 as an investment. According to the seller, the vase's value, $P, increases over time, t years, after purchase. The value of the vase is given by  P = 45 000eᵏᵗ, where k is a constant. An evaluation at the beginning of 2016 valued the vase at $50 000.", None)
gap(1)
part("(a)", "Show that  k = 0.10536, correct to 5 significant figures.", 3)
gap(8)
part("(b)", "Assuming that the value of the vase continues to increase at the same rate, calculate the year in which Mr Goh's investment becomes tripled.", 4)
pagebreak()

q("11", "", None)
part("(a)", "Find the term independent of x in the expansion of  3x³(2x − 1/(4x²))¹².", 3)
gap(11)
part("(b)", "In the expansion of  (2 + mx)¹⁵, where m is a constant, the ratio of the coefficient of x⁷ to the coefficient of x⁹ is 4/7. Find the possible values of m.", 5)
pagebreak()

q("12", "", None)
part("(a)", "It is given that  f(x) = x³ + x² + ax + 2b  and  g(x) = x³ − 4x² − ax − b, where a and b are constants.", None)
p("(x + 3) is a factor of f(x).", indent=3.7)
p("g(x) leaves a remainder of 42 when divided by (x − 5).", indent=3.7)
par = doc.add_paragraph(); par.paragraph_format.left_indent = Cm(3.7); par.paragraph_format.space_after = Pt(0)
par.paragraph_format.tab_stops.add_tab_stop(Cm(16.0), WD_TAB_ALIGNMENT.RIGHT)
par.add_run("Find the values of a and of b."); par.add_run("\t[5]")
gap(11)
part("(b)", "Solve the equation  x³ − x² − 7x + 7 = 0, expressing the roots in an exact form.", 5)
pagebreak()

q("13", "A marine monitoring buoy transmits data via Wi-Fi to a receiving station on shore. As the signal travels over the sea, it experiences a loss in strength. The signal loss, L (in dB), depends on the distance, d m, from the buoy and can be modelled by the formula  L = Adᵏ, where A and k are constants.", None)
gap(1)
p("The table below shows corresponding values of d and L.", indent=1.5)
gap(1)
t2 = doc.add_table(rows=2, cols=6); t2.style = 'Table Grid'; t2.alignment = WD_ALIGN_PARAGRAPH.CENTER
vals = [["d","9","50","200","400","900"],["L","8","15","25","32","43"]]
for i,row in enumerate(vals):
    for j,v in enumerate(row):
        c = t2.rows[i].cells[j]; c.text = v
        c.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        c.paragraphs[0].runs[0].italic = (j == 0)
gap(1)
part("(a)", "Explain how a straight line graph can be drawn to represent the formula, and draw it for the given data on the grid below.", 4)
gap(5)
img("graphpaper.png", 14.5)
pagebreak()
part("(b)", "Use your graph to estimate the value of A and of k.", 4)
gap(8)
part("(c)", "Use your graph to estimate the distance from the buoy when the signal loss is 30 dB. Leave your answer to the nearest metre.", 2)
pagebreak()

q("14", "", None)
part("(a)", "Prove the identity   cos θ / (1 − sin θ)  −  (1 − sin θ) / cos θ  =  2 tan θ .", 5)
gap(13)
part("(b)", "Hence, solve the equation   cos θ / (1 − sin θ)  −  (1 − sin θ) / cos θ  =  cot θ   for 0 ≤ θ ≤ 2π.", 4)
pagebreak()
part("(c)", "Use the result in part (a) to find the set of values of the constant k for which there are no solutions to the equation   cos θ / (1 − sin θ)  −  (1 − sin θ) / cos θ  =  k(1 + tan²θ).", 3)
gap(22)
p("----- End of Paper -----", bold=True, align='c')

import os
out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "Sec3_EOY_AMath_Paper.docx")
doc.save(out)
print("saved", out)
