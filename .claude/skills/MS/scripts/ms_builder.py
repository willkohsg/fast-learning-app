# -*- coding: utf-8 -*-
"""Template: build a CLG three-colour marking scheme.

House format (CLG marking scheme):
    black  - question text
    blue   - step-by-step working
    red    - M/A/B mark allocation and examiner's notes

Copy this file, set PAPER_TITLE / PAPER_TOTAL, and replace the example
question with the real ones. Keep the helpers as they are.

Mathematics is emitted as real OMML equation objects via omml.py.
"""
import os
import sys

from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT
from docx.oxml.ns import qn

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from omml import omath, colour                                  # noqa: E402

BLACK, BLUE, RED = '000000', '1F4E9C', 'C00000'
RGB = {BLACK: RGBColor(0, 0, 0), BLUE: RGBColor(0x1F, 0x4E, 0x9C),
       RED: RGBColor(0xC0, 0, 0)}
RIGHT_TAB = Cm(16.0)

doc = Document()
for s in doc.sections:
    s.top_margin = Cm(1.8); s.bottom_margin = Cm(1.8)
    s.left_margin = Cm(2.0); s.right_margin = Cm(2.0)

st = doc.styles['Normal']
st.font.name = 'Times New Roman'; st.font.size = Pt(11.5)
st.element.rPr.rFonts.set(qn('w:eastAsia'), 'Times New Roman')
st.paragraph_format.space_after = Pt(0)

PAPER_TITLE = "SCHOOL \u2014 EXAMINATION"
PAPER_SUBTITLE = "SUBJECT AND SYLLABUS CODE"
PAPER_TOTAL = 3          # set to the real paper total; the assert at the
                         # bottom checks the mark codes add up to it

_total = 0


def _emit(par, text, hexcol, bold=False, italic=False, size=11.5):
    """Write text into par; $...$ spans become OMML, all of it in hexcol."""
    import re
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


def _para(indent=0.0, space_before=0, space_after=0):
    par = doc.add_paragraph()
    par.paragraph_format.left_indent = Cm(indent)
    par.paragraph_format.space_before = Pt(space_before)
    par.paragraph_format.space_after = Pt(space_after)
    par.paragraph_format.tab_stops.add_tab_stop(RIGHT_TAB, WD_TAB_ALIGNMENT.RIGHT)
    return par


def qhead(num, topic, marks):
    par = _para(space_before=14, space_after=3)
    r = par.add_run("Question %s" % num)
    r.bold = True; r.font.size = Pt(13); r.font.color.rgb = RGB[BLACK]
    r = par.add_run("   —   %s" % topic)
    r.bold = False; r.italic = True; r.font.size = Pt(11); r.font.color.rgb = RGB[BLACK]
    r = par.add_run("\t[%d]" % marks)
    r.bold = True; r.font.size = Pt(12); r.font.color.rgb = RGB[BLACK]
    # rule under the heading
    pbdr = par._p.get_or_add_pPr()
    from docx.oxml import OxmlElement
    bdr = OxmlElement('w:pBdr'); bot = OxmlElement('w:bottom')
    bot.set(qn('w:val'), 'single'); bot.set(qn('w:sz'), '6')
    bot.set(qn('w:space'), '2'); bot.set(qn('w:color'), '000000')
    bdr.append(bot); pbdr.append(bdr)


def qtext(text, indent=0.0):
    """Question wording - black."""
    _emit(_para(indent, space_after=4), text, BLACK)


def part(label):
    par = _para(0.3, space_before=6, space_after=2)
    _emit(par, label, BLACK, bold=True)


def work(text, mark=None, indent=0.9):
    """A working step - blue - with an optional red mark code at the margin."""
    global _total
    par = _para(indent, space_after=2)
    _emit(par, text, BLUE)
    if mark:
        r = par.add_run("\t%s" % mark)
        r.bold = True; r.font.color.rgb = RGB[RED]; r.font.size = Pt(11)
        for code in mark.split():
            if code[:1] in "MAB" and code[1:].isdigit():
                _total += int(code[1:])


def note(text, indent=0.9):
    """Examiner's note - red."""
    par = _para(indent, space_after=3)
    r = par.add_run("Note:  ")
    r.bold = True; r.italic = True; r.font.size = Pt(10.5); r.font.color.rgb = RGB[RED]
    _emit(par, text, RED, italic=True, size=10.5)


def ans(text, mark=None, indent=0.9):
    global _total
    par = _para(indent, space_before=2, space_after=2)
    r = par.add_run("Answer:  ")
    r.bold = True; r.font.color.rgb = RGB[BLUE]
    _emit(par, text, BLUE, bold=True)
    if mark:
        r = par.add_run("\t%s" % mark)
        r.bold = True; r.font.color.rgb = RGB[RED]; r.font.size = Pt(11)
        for code in mark.split():
            if code[:1] in "MAB" and code[1:].isdigit():
                _total += int(code[1:])


# ----------------------------------------------------------------- cover
p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("SECONDARY 3 EXPRESS  —  END-OF-YEAR EXAMINATION")
r.bold = True; r.font.size = Pt(15)
p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run(PAPER_SUBTITLE); r.bold = True; r.font.size = Pt(13)
p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("WORKED SOLUTIONS & MARKING SCHEME"); r.bold = True; r.font.size = Pt(14)
doc.add_paragraph()

p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
for label, col in (("Question", BLACK), ("  •  ", BLACK),
                   ("Working", BLUE), ("  •  ", BLACK),
                   ("Marks & examiner's notes", RED)):
    r = p.add_run(label); r.bold = True; r.font.color.rgb = RGB[col]
doc.add_paragraph()

p = doc.add_paragraph()
r = p.add_run("Mark codes:   "); r.bold = True
for code, meaning in (("M", "method mark — awarded for a correct method, even if the "
                            "arithmetic that follows is wrong"),
                      ("A", "accuracy mark — awarded for a correct answer or correct "
                            "intermediate value; dependent on the preceding M mark"),
                      ("B", "independent mark — awarded for a correct statement, value or "
                            "result on its own, with no method required")):
    q = doc.add_paragraph()
    q.paragraph_format.left_indent = Cm(1.2)
    q.paragraph_format.first_line_indent = Cm(-0.8)
    q.paragraph_format.space_after = Pt(2)
    r = q.add_run("%s   " % code); r.bold = True; r.font.color.rgb = RGB[RED]
    r = q.add_run(meaning); r.font.size = Pt(11)
p = doc.add_paragraph(); p.paragraph_format.space_before = Pt(6)
r = p.add_run("Total: %d marks.  Follow-through (ft) applies throughout: a correct "
              "method applied to a candidate's own earlier incorrect value still "
              "earns the M mark." % PAPER_TOTAL)
r.italic = True; r.font.size = Pt(11)

doc.add_page_break()

# ===================================================================
# Replace everything below with the real questions.
# One work() call per step; the mark codes must sum to PAPER_TOTAL.
# ===================================================================

qhead(1, "Topic \u2014 what is being tested", 3)
qtext(r"The question wording goes here, with maths inline: solve $2x^2 + 5x - 3 = 0$.")
work(r"Factorise: $(2x - 1)(x + 3) = 0$", "M1")
ans(r"$x = \frac{1}{2}$  or  $x = -3$", "A2")
note(r"Both roots are needed for the second A mark. A candidate who solves by formula "
     r"and reaches the same pair scores full marks \u2014 the method is not prescribed.")

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "marking_scheme.docx")
doc.save(out)
print("saved", out)
print("marks accounted for:", _total)
assert _total == PAPER_TOTAL, (
    "mark codes sum to %d but the paper is %d \u2014 fix the allocation, "
    "not this assertion" % (_total, PAPER_TOTAL))
