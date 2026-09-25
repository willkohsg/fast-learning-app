# -*- coding: utf-8 -*-
"""Marked script report for one student, in the CLG three-colour format.

    black  - question / headings
    blue   - what the student wrote, and the correct working
    red    - marks earned, marks lost, and the examiner's comment
"""
import os
import re
import sys

from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from omml import omath, colour                                   # noqa: E402

BLACK, BLUE, RED, GREEN = '000000', '1F4E9C', 'C00000', '1E7A3C'
RGB = {BLACK: RGBColor(0, 0, 0), BLUE: RGBColor(0x1F, 0x4E, 0x9C),
       RED: RGBColor(0xC0, 0, 0), GREEN: RGBColor(0x1E, 0x7A, 0x3C)}
RIGHT_TAB = Cm(16.2)

STUDENT = "Chloe Yong"
CLASS, INDEX = "3S4", "19"

RESULTS = [
    ("1",  "Surds — area of a triangle",           2, 3),
    ("2",  "Surds — rationalising",                4, 4),
    ("3",  "Compound angles",                           1, 4),
    ("4",  "Completing the square / discriminant",      4, 4),
    ("5",  "Discriminant — line meets curve",      3, 5),
    ("6",  "Logarithms — change of base",          4, 5),
    ("7",  "Partial fractions",                         5, 6),
    ("8",  "Coordinate geometry",                       5, 7),
    ("9",  "Trigonometric graphs",                      7, 7),
    ("10", "Exponential growth",                        5, 7),
    ("11", "Binomial theorem",                          1, 8),
    ("12", "Polynomials",                              5, 10),
    ("13", "Linear law",                                7, 8),
    ("14", "Trigonometric identities",                 3, 12),
]
GOT = sum(r[2] for r in RESULTS)
TOT = sum(r[3] for r in RESULTS)

doc = Document()
for s in doc.sections:
    s.page_width = Cm(21.0)      # A4 - python-docx defaults to US Letter
    s.page_height = Cm(29.7)
    s.top_margin = Cm(1.7); s.bottom_margin = Cm(1.7)
    s.left_margin = Cm(1.9); s.right_margin = Cm(1.9)
st = doc.styles['Normal']
st.font.name = 'Times New Roman'; st.font.size = Pt(11)
st.element.rPr.rFonts.set(qn('w:eastAsia'), 'Times New Roman')
st.paragraph_format.space_after = Pt(0)


def _emit(par, text, hexcol, bold=False, italic=False, size=11):
    for k, chunk in enumerate(re.split(r'(?<!\\)\$', text)):
        if not chunk:
            continue
        if k % 2:
            par._p.append(colour(omath(chunk), hexcol))
        else:
            r = par.add_run(chunk.replace('\\$', '$'))
            r.font.color.rgb = RGB[hexcol]
            r.bold = bold; r.italic = italic; r.font.size = Pt(size)
    return par


def _para(indent=0.0, before=0, after=1):
    par = doc.add_paragraph()
    par.paragraph_format.left_indent = Cm(indent)
    par.paragraph_format.space_before = Pt(before)
    par.paragraph_format.space_after = Pt(after)
    par.paragraph_format.tab_stops.add_tab_stop(RIGHT_TAB, WD_TAB_ALIGNMENT.RIGHT)
    return par


def head(text, size=14, col=BLACK, before=0, after=4, align=None):
    par = _para(before=before, after=after)
    if align == 'c':
        par.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = par.add_run(text); r.bold = True; r.font.size = Pt(size)
    r.font.color.rgb = RGB[col]
    return par


def qhead(num, topic, got, avail):
    par = _para(before=12, after=3)
    r = par.add_run("Question %s" % num); r.bold = True; r.font.size = Pt(12.5)
    r = par.add_run("   %s" % topic); r.italic = True; r.font.size = Pt(10.5)
    r = par.add_run("\t%d / %d" % (got, avail))
    r.bold = True; r.font.size = Pt(12.5)
    r.font.color.rgb = RGB[GREEN] if got == avail else RGB[RED]
    pbdr = par._p.get_or_add_pPr()
    bdr = OxmlElement('w:pBdr'); bot = OxmlElement('w:bottom')
    bot.set(qn('w:val'), 'single'); bot.set(qn('w:sz'), '6')
    bot.set(qn('w:space'), '2'); bot.set(qn('w:color'), '000000')
    bdr.append(bot); pbdr.append(bdr)


def line(label, text, col, indent=0.6, labcol=None):
    par = _para(indent, after=2)
    r = par.add_run(label + "  ")
    r.bold = True; r.font.size = Pt(10.5)
    r.font.color.rgb = RGB[labcol or col]
    _emit(par, text, col)
    return par


def earned(codes, lost=None):
    par = _para(0.6, after=2)
    r = par.add_run("Awarded  "); r.bold = True; r.font.size = Pt(10.5)
    r.font.color.rgb = RGB[RED]
    r = par.add_run(codes); r.bold = True; r.font.color.rgb = RGB[RED]
    if lost:
        r = par.add_run("      Lost  "); r.bold = True; r.font.size = Pt(10.5)
        r.font.color.rgb = RGB[RED]
        r = par.add_run(lost); r.bold = True; r.font.color.rgb = RGB[RED]


def why(text):
    par = _para(0.6, after=3)
    r = par.add_run("Why the marks went  ")
    r.bold = True; r.italic = True; r.font.size = Pt(10.5)
    r.font.color.rgb = RGB[RED]
    _emit(par, text, RED, italic=True, size=10.5)


# ------------------------------------------------------------------ cover
head("CAMBRIDGE LEARNING GROUP", 12, align='c', after=0)
head("MARKED SCRIPT REPORT", 16, align='c', after=2)
head("Secondary 3 Express — End-of-Year Examination — Additional Mathematics 4049",
     11, align='c', after=10)

t = doc.add_table(rows=2, cols=4); t.style = 'Table Grid'
t.alignment = WD_TABLE_ALIGNMENT.CENTER
for j, (k, v) in enumerate([("Candidate", STUDENT), ("Class", CLASS),
                            ("Index", INDEX), ("Paper", "Paper 1  (2 h 15 min)")]):
    for i, txt in enumerate((k, v)):
        c = t.rows[i].cells[j]
        c.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        c.paragraphs[0].paragraph_format.space_after = Pt(0)
        r = c.paragraphs[0].add_run(txt)
        r.bold = (i == 0); r.font.size = Pt(10.5)

doc.add_paragraph()
par = _para(after=2); par.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = par.add_run("%d / %d" % (GOT, TOT)); r.bold = True; r.font.size = Pt(30)
r.font.color.rgb = RGB[RED]
par = _para(after=8); par.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = par.add_run("%.1f%%   —   grade band B4" % (100.0 * GOT / TOT))
r.bold = True; r.font.size = Pt(12)

head("Marks by question", 12, before=6, after=4)
t = doc.add_table(rows=len(RESULTS) + 2, cols=4); t.style = 'Table Grid'
hdr = ["Q", "Topic", "Mark", "Lost"]
for j, h in enumerate(hdr):
    c = t.rows[0].cells[j]; c.paragraphs[0].paragraph_format.space_after = Pt(0)
    r = c.paragraphs[0].add_run(h); r.bold = True; r.font.size = Pt(10)
    c.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
for i, (q, topic, g, a) in enumerate(RESULTS):
    row = t.rows[i + 1].cells
    for j, txt in enumerate([q, topic, "%d / %d" % (g, a),
                             ("−%d" % (a - g)) if a - g else "—"]):
        p = row[j].paragraphs[0]; p.paragraph_format.space_after = Pt(0)
        if j != 1:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(txt); r.font.size = Pt(10)
        if j == 2:
            r.bold = True
            r.font.color.rgb = RGB[GREEN] if g == a else RGB[RED]
        if j == 3 and a - g:
            r.font.color.rgb = RGB[RED]
last = t.rows[len(RESULTS) + 1].cells
for j, txt in enumerate(["", "TOTAL", "%d / %d" % (GOT, TOT), "−%d" % (TOT - GOT)]):
    p = last[j].paragraphs[0]; p.paragraph_format.space_after = Pt(0)
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER if j != 1 else WD_ALIGN_PARAGRAPH.LEFT
    r = p.add_run(txt); r.bold = True; r.font.size = Pt(10)
    if j >= 2:
        r.font.color.rgb = RGB[RED]
for row in t.rows:
    for k, w in enumerate((1.2, 8.6, 2.2, 1.8)):
        row.cells[k].width = Cm(w)

doc.add_page_break()

# ------------------------------------------------------- where the 34 went
head("Where the 34 marks went", 14, after=6)
for cause, tally, detail in [
    ("Left blank or abandoned", 18,
     "Q3 (3), Q5 (2), Q11 (7), Q12(b) (3), Q14(c) (3). Every one of these was a "
     "question she had already started or could have started — the marks were "
     "available, not out of reach."),
    ("Method / concept error", 9,
     "Q8(ii) used midpoint of $AB$ = midpoint of $DC$ instead of the diagonals (2); "
     "Q14(a) combined the two fractions without squaring the numerators (5); "
     "Q10(b) tripled \\$50 000 instead of the \\$45 000 investment (1); Q7(i) stated "
     "the correct form but gave no reason (1)."),
    ("Careless slip", 3,
     "Q1 expanded $\\sqrt{3}(\\sqrt{3}+2)$ wrongly (1); Q12(a) wrote $(-2)^2$ where "
     "the working needed $(-3)^2$ (2). Both were single characters that cost the "
     "whole answer."),
    ("Right work, wrong form", 4,
     "Q6 rejected the root for the wrong reason (1); Q10(b) gave $t = 12$ years "
     "instead of the year 2025 (1); Q14(b) answered in degrees when the range was "
     "in radians (1); Q13 misread two points off her own line (1)."),
]:
    par = _para(0.3, before=5, after=2)
    r = par.add_run("%s " % cause); r.bold = True; r.font.size = Pt(11.5)
    r = par.add_run("— %d marks" % tally)
    r.bold = True; r.font.size = Pt(11.5); r.font.color.rgb = RGB[RED]
    _emit(_para(0.8, after=3), detail, BLACK)

par = _para(0.3, before=8, after=2)
r = par.add_run("The headline: 18 of the 34 lost marks were never contested. ")
r.bold = True; r.font.color.rgb = RGB[RED]
r = par.add_run("Chloe's method is sound far more often than her score suggests — she "
                "scored full marks on five questions and dropped only one mark on three "
                "more. What separates 56 from the high 70s is finishing the questions she "
                "starts and checking the form the answer is asked for.")
r.font.size = Pt(11)

doc.add_page_break()

# --------------------------------------------------------- question notes
head("Question by question", 14, after=2)

qhead(1, "Surds — area of a triangle", 2, 3)
line("She wrote", r"$\frac{1}{4}(7\sqrt{3}+9) = \frac{1}{2}(DF)(\sqrt{3}+2)\sin 60\circ$, "
                  r"then expanded $\sqrt{3}(\sqrt{3}+2)$ as $\sqrt{3}+2\sqrt{3}+4$ and "
                  r"reached $DF = \frac{27-\sqrt{3}}{44}$.", BLUE)
earned("M1 M1", "A1")
why(r"The area formula was set up correctly and the rationalising was carried out "
    r"correctly on her own expression, so both method marks stand. But "
    r"$\sqrt{3}(\sqrt{3}+2) = 3 + 2\sqrt{3}$, not $\sqrt{3}+2\sqrt{3}+4$ — "
    r"$\sqrt{3}\times\sqrt{3} = 3$. One slip, and the answer mark is gone.")
line("Correct", r"$DF = 5 - \sqrt{3}$ cm", BLUE)

qhead(2, "Surds — rationalising the denominator", 4, 4)
line("She wrote", r"(a) $\frac{7(3+\sqrt{2})}{9-2} = 3+\sqrt{2}$.   "
                  r"(b) $\frac{(5+4\sqrt{3})(2-\sqrt{3})}{4-3} = -2+3\sqrt{3}$.", BLUE)
earned("M1 A1 M1 A1")
why("Clean, complete and correctly simplified in both parts. Nothing to add.")

qhead(3, "Compound angles", 1, 4)
line("She wrote", "A CAST diagram with a 3–4–5 triangle placed in the third "
                  "quadrant, labelled $B$. No further working and no answer.", BLUE)
earned("B1", "B1 M1 A1")
why(r"The diagram shows she had worked out that $B$ lies in quadrant 3, which is the "
    r"whole point of the question — that earns the first B1, and generously so, "
    r"since nothing was written about $A$. From there it was three routine lines: "
    r"$\cos A = -\frac{2}{\sqrt{5}}$, $\sin B = -\frac{3}{5}$, $\cos B = -\frac{4}{5}$, "
    r"then the formula. Three marks for work she had already half-done in her head.")
line("Correct", r"$\cos(A-B) = \frac{11}{5\sqrt{5}} = \frac{11\sqrt{5}}{25}$, "
                r"so $p = \frac{11}{25}$", BLUE)

qhead(4, "Completing the square and the discriminant", 4, 4)
line("She wrote", r"(i) $y = -2(x+3)^2 + 23$.   (ii) $b^2-4ac \le 0$ giving $184-8k \le 0$, "
                  r"so $k \ge 23$.", BLUE)
earned("M1 A1 M1 A1")
why(r"Both parts fully correct, and she included $k = 23$ rather than writing a strict "
    r"inequality — that is the mark most candidates lose here.")

qhead(5, "Discriminant — line meets curve", 3, 5)
line("She wrote", r"$nx^2 + 2x + (1-n) = 0$, then $4 - 4n + 4n^2 > 0$. Stopped there.", BLUE)
earned("M1 A1 M1", "M1 A1")
why(r"Everything written is right. She simply stopped one step early. The question says "
    r"“show”, so it needs the reason the expression is always positive: "
    r"$n^2 - n + 1 = \left(n-\frac{1}{2}\right)^2 + \frac{3}{4} \ge \frac{3}{4} > 0$, "
    r"therefore two distinct points. Two marks for two lines.")

qhead(6, "Logarithms — change of base", 4, 5)
line("She wrote", r"$\log_3\sqrt{9} = 1$, changed base correctly, reached "
                  r"$(x-4)(x-1) = 0$, then “reject $x = 1$ since $x > 0$”.", BLUE)
earned("B1 M1 M1 A1", "A1")
why(r"The mathematics is right and $x = 4$ is the right answer, but the reason for "
    r"rejecting $x = 1$ is wrong: $1 > 0$, so “$x>0$” does not reject anything. "
    r"The binding condition is $x - 3 > 0$, i.e. $x > 3$. The final mark is specifically "
    r"for that justification.")

qhead(7, "Partial fractions", 5, 6)
line("She wrote", r"(i) “$\frac{A}{x+1} + \frac{Bx+C}{x^2+4}$ should be how it is "
                  r"expressed.”   (ii) Full working to $A=2$, $B=1$, $C=2$.", BLUE)
earned("B1 M1 M1 A1 A1", "B1")
why(r"Part (ii) is flawless. Part (i) asked her to ", )
_emit(_para(0.8, after=3),
      r"explain — stating the correct form is not a reason. The reason is that "
      r"$x^2+4$ is irreducible, so it needs a numerator one degree lower, $Bx+C$; a "
      r"constant leaves two unknowns to match three coefficients.", RED)
line("Correct", r"$\frac{2}{x+1} + \frac{x+2}{x^2+4}$", BLUE)

qhead(8, "Coordinate geometry", 5, 7)
line("She wrote", r"(i) $m_{AC} = -2$, $m_{BC} = \frac{1}{2}$, product $-1$.   "
                  r"(ii) midpoint of $AB$ = midpoint of $DC$, giving $D(-2,1)$.   "
                  r"(iii) Shoelace on her own points $\Rightarrow 10$ units².", BLUE)
earned("M1 M1 A1 M1 A1", "M1 A1")
why(r"Part (i) is correct. Part (ii) uses a property that is not true: $AB$ and $DC$ are "
    r"opposite ", )
_emit(_para(0.8, after=3),
      r"sides of the parallelogram, and their midpoints are not equal. The property "
      r"needed is that the diagonals bisect each other, so midpoint $AC$ = midpoint "
      r"$BD$, giving $D(6,5)$. Part (iii) keeps both marks on follow-through — the "
      r"shoelace method was applied correctly, and it happens to give 10, the right "
      r"answer.", RED)

qhead(9, "Trigonometric graphs", 7, 7)
line("She wrote", r"$a = 7$, $b = -3$; amplitude 7, period $\pi$; and a sketch of "
                  r"$y = 7\cos 2x - 3$ with two full cycles, maxima 4 at "
                  r"$x = 0, \pi, 2\pi$ and minima $-10$ at $\frac{\pi}{2}, "
                  r"\frac{3\pi}{2}$, with $y = -3$ dashed in.", BLUE)
earned("M1 A1 A1 B1 B1 B1 B1")
why(r"The best question on the paper. The sketch is textbook — correct starting "
    r"point, correct number of cycles, both turning values marked, and the centre line "
    r"drawn in. She gave the amplitude as 7 and not 14, which is the classic trap here.")

qhead(10, "Exponential growth", 5, 7)
line("She wrote", r"(a) $k = \ln\frac{50\,000}{45\,000} = 0.10536$.   "
                  r"(b) $150\,000 = 45\,000e^{0.10536t}$, $t = 11.43 \approx 12$.", BLUE)
earned("M1 M1 A1 M1 M1", "M1 A1")
why(r"Part (a) is perfect. In part (b) “tripled” means three times the "
    r"investment: $3 \times 45\,000 = 135\,000$ dollars — she used three times "
    r"the \$50 000 valuation of 2016. Her algebra after that is correct, so the two "
    r"method marks follow through. The final mark also needs the ", )
_emit(_para(0.8, after=3),
      r"year, not the duration: $t = 10.43$ years after the start of 2015 falls in 2025.",
      RED)

qhead(11, "Binomial theorem", 1, 8)
line("She wrote", r"(a) The first three terms of the expansion written out, no general "
                  r"term and no answer.   (b) Only $T_{r+1} = \binom{n}{r}a^{n-r}b^r$ and "
                  r"“$x^7 : x^9 = 4 : 7$”.", BLUE)
earned("M1", "M1 A1 M1 M1 M1 M1 A1")
why(r"This is the single biggest loss on the paper and it is a technique gap, not "
    r"carelessness. Writing out terms one by one cannot find the term independent of "
    r"$x$ — the general term is needed so the power of $x$ can be set to zero. "
    r"With the $3x^3$ in front, the power is $15 - 3r$, so $r = 5$ and the term is "
    r"$-297$. In (b) the two coefficients are $\binom{15}{7}2^8m^7$ and "
    r"$\binom{15}{9}2^6m^9$; their ratio gives $m^2 = 9$, so $m = \pm 3$. She quoted "
    r"the right formula and then did not use it.")

qhead(12, "Polynomials", 5, 10)
line("She wrote", r"(a) $f(-3) = 0$ written as $(-3)^3 + (-2)^2 + a(-3) + 2b = 0$, "
                  r"leading to $a = -\frac{57}{13}$, $b = \frac{64}{13}$.   "
                  r"(b) Factorised to $(x-1)(x^2-7)$ and stopped.", BLUE)
earned("M1 M1 A1 M1 A1", "A1 A1 M1 A1 A1")
why(r"In (a) she wrote $(-2)^2$ where the substitution needs $(-3)^2$. One character: "
    r"the equation became $-3a+2b=23$ instead of $-3a+2b=18$, and the fractional answers "
    r"that followed should have been a warning sign — $a$ and $b$ were meant to come "
    r"out as $-4$ and $3$. Her second equation and her method were both right.")
_emit(_para(0.8, after=3),
      r"In (b) the factorisation is correct and worth two marks, but the question says "
      r"“solve”: $x = 1$, $x = \sqrt{7}$, $x = -\sqrt{7}$. Three more marks "
      r"sat one line away.", RED)

qhead(13, "Linear law", 7, 8)
line("She wrote", r"$\lg L = k\lg d + \lg A$ with $Y$, $m$, $X$, $c$ labelled; both "
                  r"$\lg$ rows computed; points plotted and a line drawn; then "
                  r"$k = 0.406$ and $A = 3.27$.", BLUE)
earned("B1 B1 M1 A1 M1 M1 A1", "A1")
why(r"Strong work — the linearisation, the table and the plot are all correct, and "
    r"the intercept method is right. She then read $(1.2,\ 0.95)$ and $(2.8,\ 1.6)$ off "
    r"her own line; the line actually passes nearer $(1.2,\ 0.99)$ and $(2.8,\ 1.57)$, "
    r"which gives $k \approx 0.365$ rather than $0.406$. Read the two points as far "
    r"apart as the line allows and take them where the line crosses a grid intersection.")

qhead(14, "Trigonometric identities", 3, 12)
line("She wrote", r"(a) $\text{LHS} = \frac{\cos\theta - (1-\sin\theta)}"
                  r"{\cos\theta(1-\sin\theta)}$, then stopped.   "
                  r"(b) $2\tan\theta = \cot\theta$ through to "
                  r"$35.3\circ, 144.7\circ, 215.3\circ, 324.7\circ$.   (c) Blank.", BLUE)
earned("M1 M1 A1", "M1 M1 M1 M1 A1 A1 M1 M1 A1")
why(r"Part (a) fails at the first line. Putting $\frac{p}{q} - \frac{r}{s}$ over a "
    r"common denominator gives $\frac{ps - rq}{qs}$ — the numerators must be "
    r"multiplied by the other denominator. The correct first line is "
    r"$\frac{\cos^2\theta - (1-\sin\theta)^2}{(1-\sin\theta)\cos\theta}$, and from there "
    r"the numerator factorises to $2\sin\theta(1-\sin\theta)$ and the identity falls out "
    r"in two more lines.")
_emit(_para(0.8, after=3),
      r"Part (b) is the encouraging part: she used the given result, reached "
      r"$\tan^2\theta = \frac{1}{2}$ and found all four angles correctly — but in "
      r"degrees, when the range $0 \le \theta \le 2\pi$ is in radians. The answers are "
      r"$0.615,\ 2.53,\ 3.76,\ 5.67$ rad. One conversion away from full marks.", RED)
_emit(_para(0.8, after=3),
      r"Part (c) was left blank. It is three marks and four lines: the identity turns it "
      r"into $kt^2 - 2t + k = 0$ with $t = \tan\theta$, and no solutions means "
      r"discriminant $< 0$, giving $k < -1$ or $k > 1$.", RED)

doc.add_page_break()

# ------------------------------------------------------------- what next
head("What to work on, in order", 14, after=6)
for n, (title, body) in enumerate([
    ("Finish the question you started",
     "18 of the 34 lost marks were on work she had already begun. Q5 needed two lines, "
     "Q12(b) three, Q14(c) four. A hard rule for the next paper: before moving on, "
     "re-read the command word — show, solve, find the year, give the set — and "
     "check the answer is in that form."),
    ("Binomial theorem — the general term",
     "The weakest topic by a distance, 1 out of 8. She knows the formula but does not "
     "use it as a tool. Drill only this: write the general term, collect the power of "
     "$x$, set it to the power required, solve for $r$. Ten questions of that one move "
     "and the topic is fixed."),
    ("Combining algebraic fractions",
     "The Q14(a) error cost 5 marks and it is arithmetic, not trigonometry: "
     "$\\frac{p}{q} - \\frac{r}{s} = \\frac{ps-rq}{qs}$. Worth checking this is secure "
     "outside a trig context first, because it will keep reappearing."),
    ("Check the substitution, then check the answer looks sensible",
     "Q1 and Q12(a) were single-character slips — $\\sqrt{3}\\times\\sqrt{3}$ and "
     "$(-3)^2$ — worth 3 marks. In Q12 the fractional $a = -\\frac{57}{13}$ was "
     "itself the signal that something was wrong, since the question implies whole "
     "numbers. Teach her to treat an ugly answer as a prompt to re-check."),
    ("Radians and degrees",
     "Q14(b) had all four angles right and scored 3 of 4 because the range was in "
     "radians. A quick habit: look at the range before starting, and set the calculator "
     "to match."),
]):
    par = _para(0.3, before=7, after=2)
    r = par.add_run("%d.  %s" % (n + 1, title)); r.bold = True; r.font.size = Pt(11.5)
    _emit(_para(0.9, after=3), body, BLACK)

par = _para(0.3, before=12, after=2)
r = par.add_run("Overall.  "); r.bold = True; r.font.size = Pt(11.5)
r.font.color.rgb = RGB[RED]
r = par.add_run("56 / 90 understates her. Full marks on Q2, Q4 and Q9, and one mark off "
                "on Q6, Q7 and Q13, show the core is in place across surds, quadratics, "
                "logarithms, partial fractions, graphs and linear law. Two topics need "
                "real teaching — binomial expansion and proving identities — and "
                "the rest is exam discipline. Both are fixable before the next paper.")
r.font.size = Pt(11)

out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "Chloe_Yong_Sec3_EOY_AMath_Marked_Report.docx")
doc.save(out)
print("saved", out)
print("total %d / %d (%.1f%%)" % (GOT, TOT, 100.0 * GOT / TOT))
assert TOT == 90
