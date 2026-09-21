# -*- coding: utf-8 -*-
"""Render a small LaTeX subset as OMML (Office Math Markup Language).

Word and LibreOffice both consume OMML natively, so equations produced here are
real, editable equation objects rather than styled text.

Supported: \\frac, \\sqrt (with optional index), ^ and _ (including stacked
sub-superscripts), \\text, bracket groups, function names and a symbol table.
"""
import re

from docx.oxml.ns import qn
from docx.oxml import OxmlElement

M = 'http://schemas.openxmlformats.org/officeDocument/2006/math'

SYMBOLS = {
    'pi': 'π', 'theta': 'θ', 'alpha': 'α', 'beta': 'β',
    'Delta': 'Δ', 'infty': '∞', 'times': '×', 'cdot': '·',
    'pm': '±', 'mp': '∓', 'le': '≤', 'leq': '≤',
    'ge': '≥', 'geq': '≥', 'neq': '≠', 'approx': '≈',
    'circ': '°', 'ldots': '…', 'to': '→', 'in': '∈',
    'Rightarrow': '⇒', 'implies': '⇒', 'Leftarrow': '⇐',
    'Leftrightarrow': '⇔', 'iff': '⇔', 'ne': '≠', 'equiv': '≡',
    'therefore': '∴', 'div': '÷', 'perp': '⊥', 'angle': '∠',
}

# An oMath opening with a relation has no left operand, which LibreOffice's
# StarMath converter renders as an error glyph. A leading zero-width space
# gives it something to bind to and renders identically.
_LEADING_RELATION = set('=<>+≤≥≈≠⇒')
_RELATION_MACROS = ('le', 'leq', 'ge', 'geq', 'approx', 'neq', 'ne',
                    'Rightarrow', 'implies', 'Leftrightarrow', 'iff', 'equiv')
FUNCS = {'sin', 'cos', 'tan', 'cot', 'sec', 'cosec', 'csc',
         'log', 'ln', 'lg', 'exp'}


def _el(tag):
    return OxmlElement('m:' + tag)


def _run(text, upright=False):
    """A math run. upright=True suppresses Word's automatic italicising."""
    r = _el('r')
    if upright:
        # m:nor is what LibreOffice honours; m:sty is what Word writes. Emit
        # both so function names stay upright in either renderer.
        rpr = _el('rPr')
        rpr.append(_el('nor'))
        sty = _el('sty'); sty.set(qn('m:val'), 'p')
        rpr.append(sty)
        r.append(rpr)
    t = _el('t')
    t.set(qn('xml:space'), 'preserve')
    t.text = text
    r.append(t)
    return r


def _plain_runs(text):
    """Split a plain chunk so that letter clusters become one run per letter."""
    runs, buf = [], ''
    for ch in text:
        if ch.isalpha():
            if buf:
                runs.append(_run(buf)); buf = ''
            runs.append(_run(ch))
        else:
            buf += ch
    if buf:
        runs.append(_run(buf))
    return runs


def _delim(child, left='(', right=')'):
    """Wrap an element in auto-sized brackets."""
    d = _el('d')
    dpr = _el('dPr')
    b = _el('begChr'); b.set(qn('m:val'), left)
    e2 = _el('endChr'); e2.set(qn('m:val'), right)
    dpr.append(b); dpr.append(e2)
    d.append(dpr)
    e = _el('e'); e.append(child); d.append(e)
    return d


class _Parser:
    def __init__(self, s):
        self.s = s
        self.i = 0

    def eof(self):
        return self.i >= len(self.s)

    def peek(self):
        return self.s[self.i] if not self.eof() else ''

    def group(self):
        """Read one argument: a {...} group, a \\command, or a single char."""
        while self.peek() == ' ':
            self.i += 1
        if self.peek() == '{':
            depth, start = 0, self.i
            while not self.eof():
                c = self.s[self.i]
                if c == '{':
                    depth += 1
                elif c == '}':
                    depth -= 1
                    if depth == 0:
                        self.i += 1
                        return self.s[start + 1:self.i - 1]
                self.i += 1
            return self.s[start + 1:]
        if self.peek() == '\\':
            start = self.i
            self.i += 1
            while not self.eof() and self.s[self.i].isalpha():
                self.i += 1
            return self.s[start:self.i]
        c = self.peek()
        self.i += 1
        return c

    def parse(self):
        out = []
        while not self.eof():
            c = self.s[self.i]

            if c == '\\':
                self.i += 1
                name = ''
                while not self.eof() and self.s[self.i].isalpha():
                    name += self.s[self.i]
                    self.i += 1
                if name == 'frac':
                    num, den = self.group(), self.group()
                    f = _el('f')
                    fpr = _el('fPr'); ty = _el('type'); ty.set(qn('m:val'), 'bar')
                    fpr.append(ty); f.append(fpr)
                    n = _el('num'); n.extend(parse_nodes(num)); f.append(n)
                    d = _el('den'); d.extend(parse_nodes(den)); f.append(d)
                    out.append(f)
                elif name == 'sqrt':
                    deg_src = None
                    if self.peek() == '[':
                        j = self.s.index(']', self.i)
                        deg_src = self.s[self.i + 1:j]
                        self.i = j + 1
                    body = self.group()
                    rad = _el('rad')
                    rpr = _el('radPr')
                    hide = _el('degHide')
                    hide.set(qn('m:val'), '0' if deg_src else '1')
                    rpr.append(hide); rad.append(rpr)
                    deg = _el('deg')
                    if deg_src:
                        deg.extend(parse_nodes(deg_src))
                    rad.append(deg)
                    e = _el('e'); e.extend(parse_nodes(body)); rad.append(e)
                    out.append(rad)
                elif name == 'binom':
                    top, bot = self.group(), self.group()
                    f = _el('f')
                    fpr = _el('fPr'); ty = _el('type'); ty.set(qn('m:val'), 'noBar')
                    fpr.append(ty); f.append(fpr)
                    n = _el('num'); n.extend(parse_nodes(top)); f.append(n)
                    d = _el('den'); d.extend(parse_nodes(bot)); f.append(d)
                    out.append(_delim(f))
                elif name in ('left', 'right'):
                    if self.peek() in '()[]{}|.':
                        ch = self.peek(); self.i += 1
                        if ch != '.':
                            out.append(_run(ch))
                elif name in ('quad', 'qquad'):
                    out.append(_run('\u2003' * (1 if name == 'quad' else 2)))
                elif name == 'text':
                    out.append(_run(self.group(), upright=True))
                elif name in FUNCS:
                    out.append(_run(name, upright=True))
                elif name in SYMBOLS:
                    out.append(_run(SYMBOLS[name]))
                elif name == '':
                    ch = self.peek()
                    if ch == ',':                       # \, thin space
                        out.append(_run('\u2009'))
                    elif ch:                            # \$ \% \& ... literal
                        out.append(_run(ch, upright=True))
                    self.i += 1
                else:
                    out.append(_run(name, upright=True))
                continue

            if c in '^_':
                self.i += 1
                arg = self.group()
                if not out:                       # no base, e.g. a bare "^2"
                    out.extend(_plain_runs(arg))
                    continue
                base = out.pop()
                # a script binds only to the last symbol, so split a trailing
                # text run: "y = ax" ^2  ->  "y = a" and base "x"
                # ...but an upright run is a whole name (sec, log, text), so the
                # script attaches to all of it: sec^2, log_2.
                if base.tag == '{%s}r' % M and base.find(qn('m:rPr')) is None:
                    tnode = base.find(qn('m:t'))
                    txt = tnode.text or ''
                    if len(txt) > 1:
                        tnode.text = txt[-1]
                        out.append(_run(txt[:-1]))
                # a sub immediately followed by a sup (or vice versa) stacks
                other = None
                if self.peek() and self.peek() in '^_' and self.peek() != c:
                    kind = self.peek()
                    self.i += 1
                    other = (kind, self.group())
                if other:
                    node = _el('sSubSup')
                    e = _el('e'); e.append(base); node.append(e)
                    sub_src = arg if c == '_' else other[1]
                    sup_src = arg if c == '^' else other[1]
                    sub = _el('sub'); sub.extend(parse_nodes(sub_src)); node.append(sub)
                    sup = _el('sup'); sup.extend(parse_nodes(sup_src)); node.append(sup)
                else:
                    node = _el('sSup' if c == '^' else 'sSub')
                    e = _el('e'); e.append(base); node.append(e)
                    tag = 'sup' if c == '^' else 'sub'
                    part = _el(tag); part.extend(parse_nodes(arg)); node.append(part)
                out.append(node)
                continue

            # plain text: accumulate until something structural turns up
            buf = ''
            while not self.eof() and self.s[self.i] not in '\\^_':
                buf += self.s[self.i]
                self.i += 1
            if buf:
                out.extend(_plain_runs(buf))
        return out


def parse_nodes(src):
    return _Parser(src).parse()


def _needs_pad(latex):
    t = latex.lstrip()
    if not t:
        return False
    if t[0] in _LEADING_RELATION:
        return True
    if t[0] == '\\':
        name = ''
        for ch in t[1:]:
            if not ch.isalpha():
                break
            name += ch
        return name in _RELATION_MACROS
    return False


def omath(latex):
    """Build an <m:oMath> element from a LaTeX-subset string."""
    m = _el('oMath')
    if _needs_pad(latex):
        latex = '\u200b' + latex
    m.extend(parse_nodes(latex))
    return m


def colour(node, hex_rgb):
    """Recolour every run inside an OMML element.

    An m:r accepts a w:rPr for character formatting, which must sit after
    m:rPr and before m:t.
    """
    for r in node.iter(qn('m:r')):
        wrpr = OxmlElement('w:rPr')
        col = OxmlElement('w:color')
        col.set(qn('w:val'), hex_rgb)
        wrpr.append(col)
        mrpr = r.find(qn('m:rPr'))
        r.insert(1 if mrpr is not None else 0, wrpr)
    return node


def add_math(paragraph, latex):
    paragraph._p.append(omath(latex))
    return paragraph


def add_mixed(paragraph, text, run_kwargs=None):
    """Add text where $...$ spans become real OMML equations.

    A literal dollar sign is written \\$ and never opens a math span, so
    currency and mathematics can share a line.
    """
    run_kwargs = run_kwargs or {}
    for k, chunk in enumerate(re.split(r'(?<!\\)\$', text)):
        if not chunk:
            continue
        if k % 2:
            paragraph._p.append(omath(chunk))
        else:
            r = paragraph.add_run(chunk.replace('\\$', '$'))
            for attr, val in run_kwargs.items():
                setattr(r, attr, val)
    return paragraph
