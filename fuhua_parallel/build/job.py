# -*- coding: utf-8 -*-
import os
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.abspath(os.path.join(HERE, "..", "..",
                                   "Fuhua_Parallel_Sec3_EOY_AMath_2026_Paper.pdf"))
OUT = os.path.abspath(os.path.join(HERE, "..", "..", "fuhua_parallel_ms_out"))

META = dict(
    layout="overlay", source_pdf=SRC, out_dir=OUT, total_marks=80,
    filename="CLG Fuhua-Parallel Sec 3 Express 2026 EOY A-Math P1 - Marking Scheme",
    header="CLG FUHUA-PARALLEL · SEC 3 EXPRESS A-MATH EOY 2026 · PAPER 1",
    title="Fuhua-Parallel Sec 3 Express EOY 2026 Paper 1 — Marking Scheme",
    source="Cambridge Learning Group · Fuhua-parallel practice paper · Paper 1 · 2026",
)

BX, BW = 85, 210
RX, RW = 312, 222


def blue(y, lines):
    return dict(kind="blue", x=BX, y=y, w=BW, lines=lines)


def red(y, lines):
    return dict(kind="red", x=RX, y=y, w=RW, lines=lines)


PAGES = [
 dict(page=3, notes=[
  blue(126, [
    r"Curve above line for all $x$:",
    r"$x^{2}+(k-2)x+4>2x-k$ for all $x$",
    r"$x^{2}+(k-4)x+(4+k)>0$ for all $x$",
    r"A positive quadratic is always above the $x$-axis when it has no real root:",
    r"$(k-4)^{2}-4(4+k)<0$",
    r"$k^{2}-8k+16-16-4k<0$",
    r"$k^{2}-12k<0$",
    r"$k(k-12)<0$",
    r"$\therefore 0<k<12$"]),
  red(126, [
    "Key concept: above for ALL $x$ means the difference is a positive quadratic with no real root.",
    ("M1", r"forms the difference and gets $x^{2}+(k-4)x+(4+k)>0$"),
    ("M1", r"uses $\text{discriminant}<0$ (not $\le 0$, and not $0<\text{discriminant}$)"),
    ("M1", r"reduces to $k^{2}-12k<0$"),
    ("A1", r"$0<k<12$"),
    ("Trap", r"$k<0$ or $k>12$ comes from solving $k(k-12)>0$; sketch the parabola in $k$."),
  ]),
 ]),
 dict(page=4, notes=[
  blue(108, [
    r"$\dfrac{5-2\sqrt{3}}{2\sqrt{3}-3}\times\dfrac{2\sqrt{3}+3}{2\sqrt{3}+3}$",
    r"$\text{denominator}=\left(2\sqrt{3}\right)^{2}-3^{2}=12-9=3$",
    r"$\text{numerator}=10\sqrt{3}+15-4(3)-6\sqrt{3}$",
    r"$\text{numerator}=4\sqrt{3}+3$",
    r"$\dfrac{3+4\sqrt{3}}{3}=1+\dfrac{4}{3}\sqrt{3}$",
    r"$\therefore a=1,\ b=\dfrac{4}{3}$"]),
  red(108, [
    "Key concept: the conjugate of $2\\sqrt{3}-3$ is $2\\sqrt{3}+3$.",
    ("M1", r"multiplies by the conjugate $2\sqrt{3}+3$"),
    ("M1", r"denominator $12-9=3$"),
    ("A1", r"$a=1$ and $b=\dfrac{4}{3}$"),
    ("Note", r"the question says RATIONAL, not integer — $\dfrac{4}{3}$ is acceptable."),
  ]),
  blue(268, [
    r"$\sqrt{3x+7}=2+\sqrt{x+1}$",
    r"$3x+7=4+4\sqrt{x+1}+x+1$",
    r"$2x+2=4\sqrt{x+1}$",
    r"$x+1=2\sqrt{x+1}$",
    r"let $w=\sqrt{x+1}$:  $w^{2}=2w$",
    r"$w(w-2)=0$, so $w=0$ or $w=2$",
    r"$x+1=0$ or $x+1=4$",
    r"check $x=-1$: $\sqrt{4}-\sqrt{0}=2$  ✓",
    r"check $x=3$: $\sqrt{16}-\sqrt{4}=4-2=2$  ✓",
    r"$\therefore x=-1$ or $x=3$"]),
  red(268, [
    "Key concept: isolate one surd, square, then isolate the surd that remains.",
    ("M1", r"squares after isolating one surd"),
    ("M1", r"reaches $x+1=2\sqrt{x+1}$ and squares again"),
    ("A1", r"BOTH $x=-1$ and $x=3$"),
    ("Trap", r"both roots satisfy the original equation — neither may be rejected. "
             r"Discarding one loses the A1."),
  ]),
 ]),
 dict(page=5, notes=[
  blue(127, [
    r"$(x-2)$ a factor $\Rightarrow f(2)=0$:",
    r"$16+4a+2b-6=0$",
    r"$2a+b=-5$  …(1)",
    r"$f(-1)=-12$:  $-2+a-b-6=-12$",
    r"$a-b=-4$  …(2)",
    r"(1)+(2): $3a=-9$, so $a=-3$",
    r"from (2): $b=a+4=1$",
    r"$\therefore a=-3,\ b=1$"]),
  red(127, [
    ("M1", r"$f(2)=0$ used"), ("A1", r"$2a+b=-5$"),
    ("M1", r"$f(-1)=-12$ used"), ("A1", r"$a=-3$ and $b=1$"),
    ("Trap", r"remainder $-12$ means $f(-1)=-12$, not $f(-1)=0$."),
  ]),
  blue(302, [
    r"$f(x)=2x^{3}-3x^{2}+x-6$",
    r"$f(x)=(x-2)\left(2x^{2}+x+3\right)$",
    r"$x-2=0$ gives $x=2$",
    r"for $2x^{2}+x+3=0$:",
    r"$\text{discriminant}=1^{2}-4(2)(3)=1-24=-23<0$",
    r"so the quadratic factor has no real root",
    r"$\therefore x=2$ is the only real root"]),
  red(302, [
    "Key concept: a cubic with one real root has an irreducible quadratic factor.",
    ("M1", r"divides out $(x-2)$ to get $2x^{2}+x+3$"),
    ("A1", r"discriminant $-23<0$ computed"),
    ("A1", r"states $x=2$ is the only real root, because the quadratic has no real root"),
    ("Note", r"the explanation is required — quoting $x=2$ alone scores at most M1 A1."),
  ]),
 ]),
 dict(page=6, notes=[
  blue(140, [
    r"Numerator $\text{degree}=4$; denominator $x^{2}\left(x^{2}+4\right)$ has degree $4$.",
    r"The fraction is improper (degree of top $\ge$ degree of bottom).",
    r"The given form is a sum of proper fractions, so it can only represent a proper fraction.",
    r"A constant term must be included first, by division."]),
  red(140, [
    ("B1", r"identifies both degrees as $4$, so the fraction is improper"),
    ("B1", r"states that a constant (the quotient) is needed before the proper fractions"),
    ("Note", r"saying only “the powers are the same” without the conclusion scores B1."),
  ]),
  blue(304, [
    r"$\dfrac{2x^{4}+2x^{3}+6x^{2}+4x+4}{x^{4}+4x^{2}}=2+\dfrac{2x^{3}-2x^{2}+4x+4}{x^{2}\left(x^{2}+4\right)}$",
    r"$\dfrac{2x^{3}-2x^{2}+4x+4}{x^{2}\left(x^{2}+4\right)}=\dfrac{A}{x}+\dfrac{B}{x^{2}}+\dfrac{Cx+D}{x^{2}+4}$",
    r"$2x^{3}-2x^{2}+4x+4=Ax\left(x^{2}+4\right)+B\left(x^{2}+4\right)+(Cx+D)x^{2}$",
    r"$x=0$:  $4=4B$, so $B=1$",
    r"$x^{3}$:  $2=A+C$;  $x^{2}$:  $-2=B+D$, so $D=-3$",
    r"$x$:  $4=4A$, so $A=1$, hence $C=1$",
    r"$\therefore 2+\dfrac{1}{x}+\dfrac{1}{x^{2}}+\dfrac{x-3}{x^{2}+4}$"]),
  red(304, [
    "Key concept: divide first, then split; $x^{2}$ needs TWO terms and $x^{2}+4$ needs $Cx+D$.",
    ("M1", r"divides to get the quotient $2$"),
    ("M1", r"correct form with $\dfrac{A}{x}+\dfrac{B}{x^{2}}+\dfrac{Cx+D}{x^{2}+4}$"),
    ("M1", r"clears denominators and substitutes or compares"),
    ("A1", r"$B=1$ and $A=1$"), ("A1", r"$C=1$"), ("A1", r"$D=-3$"),
    ("Note", r"check at $x=1$: $\text{LHS}=\dfrac{18}{5}$, $\text{RHS}=2+1+1-\dfrac{2}{5}=\dfrac{18}{5}$ ✓"),
  ]),
 ]),
 dict(page=7, notes=[
  blue(94, [
    r"$3^{\,2x+1}=3\left(3^{\,x}\right)^{2}$",
    r"let $u=3^{\,x}$:  $3u^{2}-10u+3=0$",
    r"$(3u-1)(u-3)=0$",
    r"$u=\dfrac{1}{3}$ or $u=3$",
    r"$3^{\,x}=3^{-1}$ or $3^{\,x}=3^{1}$",
    r"$\therefore x=-1$ or $x=1$"]),
  red(94, [
    "Key concept: $3^{2x+1}=3\\cdot\\left(3^{x}\\right)^{2}$ turns it into a quadratic.",
    ("M1", r"writes $3^{\,2x+1}$ as $3\left(3^{\,x}\right)^{2}$ and substitutes $u=3^{\,x}$"),
    ("M1", r"solves the quadratic in $u$"),
    ("A1", r"$x=-1$ and $x=1$"),
    ("Trap", r"$3^{\,2x+1}\ne\left(3^{\,x}\right)^{2}$ — the extra factor of $3$ is what makes it work."),
  ]),
  blue(290, [
    r"$\log_2 x+\log_2 y=5\Rightarrow\log_2(xy)=5$",
    r"$xy=32$  …(1)",
    r"$\log_4 x-\log_4 y=\dfrac{1}{2}\Rightarrow\log_4\dfrac{x}{y}=\dfrac{1}{2}$",
    r"$\dfrac{x}{y}=4^{\frac{1}{2}}=2$, so $x=2y$  …(2)",
    r"(2) into (1): $2y^{2}=32$",
    r"$y^{2}=16$, and $y>0$, so $y=4$",
    r"$\therefore x=8,\ y=4$"]),
  red(290, [
    "Key concept: combine each equation into a single log, then remove the log.",
    ("M1", r"$\log_2(xy)=5$ giving $xy=32$"),
    ("M1", r"$\log_4\dfrac{x}{y}=\dfrac{1}{2}$ giving $\dfrac{x}{y}=2$"),
    ("A1", r"$y=4$"), ("A1", r"$x=8$"),
    ("Trap", r"$y=-4$ must be rejected: $\log_2 y$ requires $y>0$."),
  ]),
 ]),
 dict(page=8, notes=[
  blue(140, [
    r"$t=1$: $8=M_0e^{\,k}$;  $t=4$: $27=M_0e^{\,4k}$",
    r"dividing: $\dfrac{27}{8}=e^{\,3k}$",
    r"$3k=\ln\dfrac{27}{8}=3\ln\dfrac{3}{2}$",
    r"$\therefore k=\ln\dfrac{3}{2}$  (shown)",
    r"$e^{\,k}=\dfrac{3}{2}$, so $8=M_0\left(\dfrac{3}{2}\right)$",
    r"$\therefore M_0=\dfrac{16}{3}$ g"]),
  red(140, [
    "Key concept: divide the two equations to eliminate $M_0$.",
    ("M1", r"both equations written and divided"),
    ("M1", r"$e^{\,3k}=\dfrac{27}{8}$"),
    ("A1", r"$k=\ln\dfrac{3}{2}$ shown, using $\ln\dfrac{27}{8}=3\ln\dfrac{3}{2}$"),
    ("A1", r"$M_0=\dfrac{16}{3}$"),
    ("Note", r"exact value required — $5.33$ alone loses the A1."),
  ]),
  blue(318, [
    r"$\dfrac{16}{3}\left(\dfrac{3}{2}\right)^{t}>200$",
    r"$\left(\dfrac{3}{2}\right)^{t}>\dfrac{600}{16}=37.5$",
    r"$t\ln\dfrac{3}{2}>\ln 37.5$",
    r"$t>\dfrac{3.6243}{0.40546}=8.938\ldots$",
    r"$\therefore$ the least number of complete hours is $9$"]),
  red(318, [
    ("M1", r"forms the inequality and isolates $\left(\dfrac{3}{2}\right)^{t}$"),
    ("M1", r"takes logs correctly"),
    ("A1", r"$9$ hours"),
    ("Trap", r"$t=8.94$ rounds to $8.9$, but the mass has not yet exceeded $200$ g at "
             r"$t=8$ — the answer is the next whole hour, $9$."),
  ]),
 ]),
 dict(page=9, notes=[
  blue(108, [
    r"coefficient of $x$: $\binom{n}{1}2=2n$",
    r"coefficient of $x^{2}$: $\binom{n}{2}2^{2}=2n(n-1)$",
    r"$2n(n-1)=2n+96$",
    r"$2n^{2}-4n-96=0$",
    r"$n^{2}-2n-48=0$",
    r"$(n-8)(n+6)=0$",
    r"$n>0$, so $\therefore n=8$"]),
  red(108, [
    ("M1", r"both coefficients written in terms of $n$"),
    ("M1", r"forms $2n(n-1)=2n+96$ and reduces to a quadratic"),
    ("A1", r"$n=8$, rejecting $n=-6$"),
    ("Trap", r"$\binom{n}{2}$ must carry the factor $2^{2}$ from $(2x)^{2}$."),
  ]),
  blue(304, [
    r"$(1+2x)^{8}$: coefficient of $x^{5}=\binom{8}{5}2^{5}=56(32)=1792$",
    r"coefficient of $x^{4}=\binom{8}{4}2^{4}=70(16)=1120$",
    r"In $\left(2-x\right)\left(1+2x\right)^{8}$ the $x^{5}$ term comes from",
    r"$2\times\left(x^{5}\text{ term}\right)$ and $(-x)\times\left(x^{4}\text{ term}\right)$",
    r"$\text{coefficient}=2(1792)-1(1120)$",
    r"$\text{coefficient}=3584-1120$",
    r"$\therefore$ coefficient of $x^{5}=2464$"]),
  red(304, [
    "Key concept: with a bracket in front, TWO terms of the expansion contribute.",
    ("M1", r"coefficient of $x^{5}$ in $(1+2x)^{8}$ as $\binom{8}{5}2^{5}$"),
    ("M1", r"coefficient of $x^{4}$ as $\binom{8}{4}2^{4}$"),
    ("M1", r"combines as $2\times1792-1\times1120$"),
    ("A1", r"$2464$"),
    ("Trap", r"forgetting the $x^{4}$ contribution gives $3584$; the sign of $-x$ matters."),
  ]),
 ]),
 dict(page=10, notes=[
  blue(110, [
    r"$AB$ a diameter, so the centre is the midpoint of $AB$:",
    r"$\text{centre}=\left(\dfrac{-1+5}{2},\ \dfrac{2+4}{2}\right)=(2,\ 3)$",
    r"$AB^{2}=(5+1)^{2}+(4-2)^{2}=36+4=40$",
    r"$\text{radius}=\dfrac{\sqrt{40}}{2}$, so $r^{2}=10$",
    r"$\therefore (x-2)^{2}+(y-3)^{2}=10$"]),
  red(110, [
    ("M1", r"centre as the midpoint of the diameter"),
    ("M1", r"$r^{2}=10$ from $\left(\dfrac{AB}{2}\right)^{2}$ or from centre to $A$"),
    ("A1", r"$(x-2)^{2}+(y-3)^{2}=10$"),
  ]),
  blue(254, [
    r"gradient of radius $CA=\dfrac{2-3}{-1-2}=\dfrac{1}{3}$",
    r"tangent $\perp$ radius, so gradient of $\text{tangent}=-3$",
    r"at $A(-1,\ 2)$:  $y-2=-3(x+1)$",
    r"$y=-3x-1$",
    r"at the $y$-axis, $x=0$, so $y=-1$",
    r"$\therefore P(0,\ -1)$"]),
  red(254, [
    "Key concept: the tangent at a point is perpendicular to the radius there.",
    ("M1", r"gradient of the $\text{radius}=\dfrac{1}{3}$"),
    ("M1", r"uses $m_1m_2=-1$ to get $-3$ and forms the tangent"),
    ("A1", r"$P(0,\ -1)$"),
  ]),
 ]),
 dict(page=11, notes=[
  blue(78, [
    r"distance from $P(0,-1)$ to the centre $(2,\ 3)$:",
    r"$d^{2}=(2-0)^{2}+(3+1)^{2}=4+16=20$",
    r"$d^{2}=20>10=r^{2}$, so $P$ lies outside $C_1$",
    r"tangent $\text{length}=\sqrt{d^{2}-r^{2}}$",
    r"$\text{tangent length}=\sqrt{20-10}$",
    r"$\therefore$ tangent $\text{length}=\sqrt{10}$"]),
  red(78, [
    "Key concept: the tangent, the radius and the line to the centre form a right triangle.",
    ("M1", r"$d^{2}=20$ computed"),
    ("A1", r"compares $d^{2}=20$ with $r^{2}=10$ and concludes $P$ is outside"),
    ("A1", r"$\sqrt{10}$, exact"),
    ("Trap", r"comparing $d$ with $r^{2}$, or leaving $\sqrt{10}$ as $3.16$ when "
             r"EXACT is asked for."),
  ]),
  blue(270, [
    r"$P(0,-1)$, $A(-1,\ 2)$, $B(5,\ 4)$",
    r"$\text{area}=\dfrac{1}{2}\left|x_P(y_A-y_B)+x_A(y_B-y_P)+x_B(y_P-y_A)\right|$",
    r"$\text{area}=\dfrac{1}{2}\left|0(2-4)+(-1)(4+1)+5(-1-2)\right|$",
    r"$\text{area}=\dfrac{1}{2}\left|0-5-15\right|$",
    r"$\text{area}=\dfrac{1}{2}(20)$",
    r"$\therefore$ $\text{area}=10$ units$^{2}$"]),
  red(270, [
    ("M1", r"a correct area method (shoelace, or $\dfrac{1}{2}\times$ base $\times$ height)"),
    ("M1", r"correct substitution of all three points"),
    ("A1", r"$10$ units$^{2}$"),
    ("Note", r"$PA\perp AB$ (the tangent), so $\dfrac{1}{2}(PA)(AB)=\dfrac{1}{2}\sqrt{10}\sqrt{40}=10$ "
             r"is a neat check."),
  ]),
 ]),
 dict(page=12, notes=[
  blue(222, [
    r"$y=\dfrac{x}{ax+b}$",
    r"taking reciprocals: $\dfrac{1}{y}=\dfrac{ax+b}{x}$",
    r"$\dfrac{1}{y}=a+b\left(\dfrac{1}{x}\right)$",
    r"Comparing with $Y=mX+c$: plot $\dfrac{1}{y}$ against $\dfrac{1}{x}$;",
    r"the graph is a straight line of gradient $b$ and vertical intercept $a$.",
    r"$\dfrac{1}{x}$:  $1,\ 0.5,\ 0.25,\ 0.2,\ 0.1$",
    r"$\dfrac{1}{y}$:  $5.00,\ 3.50,\ 2.75,\ 2.60,\ 2.30$"]),
  red(222, [
    "Key concept: invert BOTH sides first — the linear pair is $\\dfrac{1}{y}$ against $\\dfrac{1}{x}$.",
    ("B1", r"takes reciprocals to reach $\dfrac{1}{y}=a+b\left(\dfrac{1}{x}\right)$"),
    ("B1", r"states: plot $\dfrac{1}{y}$ against $\dfrac{1}{x}$, gradient $b$, intercept $a$"),
    ("B1", r"both reciprocal rows computed, points plotted and a straight line drawn"),
    ("Trap", r"plotting $y$ against $\dfrac{1}{x}$, or $\dfrac{1}{y}$ against $x$, gives a curve."),
  ]),
 ]),
 dict(page=13, notes=[
  blue(78, [
    r"gradient $b=\dfrac{5.00-2.30}{1.0-0.1}=\dfrac{2.70}{0.9}$",
    r"$b\approx 3$",
    r"intercept: $\dfrac{1}{y}=a$ when $\dfrac{1}{x}=0$",
    r"$a=5.00-3(1.0)$",
    r"$\therefore a\approx 2,\ b\approx 3$"]),
  red(78, [
    "Key concept: read two points off the DRAWN LINE, as far apart as it allows.",
    ("M1", r"gradient from two points on the line"),
    ("A1", r"$b\approx 3$"),
    ("M1", r"intercept read at $\dfrac{1}{x}=0$, or substitution into the line"),
    ("A1", r"$a\approx 2$"),
    ("Note", r"accept $a$ from $1.8$ to $2.2$ and $b$ from $2.8$ to $3.2$."),
    ("Note", r"check: $y=\dfrac{x}{2x+3}$ gives $y=0.364$ at $x=4$ ✓"),
  ]),
 ]),
 dict(page=14, notes=[
  blue(112, [
    r"$A$ obtuse, so $A$ is in quadrant 2: $\sin A>0$",
    r"$\sin^{2}A=1-\cos^{2}A=1-(-p)^{2}=1-p^{2}$",
    r"$\therefore\sin A=\sqrt{1-p^{2}}$"]),
  red(112, [
    ("M1", r"uses $\sin^{2}A+\cos^{2}A=1$"),
    ("A1", r"$\sqrt{1-p^{2}}$, positive because $A$ is obtuse"),
    ("Trap", r"$\pm\sqrt{1-p^{2}}$ loses the A1 — the quadrant decides the sign."),
  ]),
  blue(240, [
    r"$\tan\left(180^{\circ}-A\right)=-\tan A$",
    r"$\tan A=\dfrac{\sin A}{\cos A}=\dfrac{\sqrt{1-p^{2}}}{-p}$",
    r"$\therefore\tan\left(180^{\circ}-A\right)=\dfrac{\sqrt{1-p^{2}}}{p}$"]),
  red(240, [
    ("M1", r"$\tan\left(180^{\circ}-A\right)=-\tan A$"),
    ("A1", r"$\dfrac{\sqrt{1-p^{2}}}{p}$"),
    ("Note", r"two negatives cancel: the answer is positive."),
  ]),
  blue(368, [
    r"$\sin\left(90^{\circ}+A\right)=\cos A=-p$",
    r"$\cosec\left(90^{\circ}+A\right)=\dfrac{1}{\sin\left(90^{\circ}+A\right)}$",
    r"$\therefore\cosec\left(90^{\circ}+A\right)=-\dfrac{1}{p}$"]),
  red(368, [
    ("M1", r"$\sin\left(90^{\circ}+A\right)=\cos A$"),
    ("A1", r"$-\dfrac{1}{p}$"),
    ("Trap", r"$90^{\circ}+A$, not $90^{\circ}-A$: the sine of $90^{\circ}+A$ is $+\cos A$, "
             r"and $\cos A$ is negative here."),
  ]),
 ]),
 dict(page=15, notes=[
  blue(138, [
    r"$-\cos\dfrac{x}{2}$ is greatest when $\cos\dfrac{x}{2}=-1$, so $\text{maximum}=a+b=7$",
    r"least when $\cos\dfrac{x}{2}=1$, so $\text{minimum}=a-b=-1$",
    r"adding: $2a=6$, so $a=3$",
    r"$\therefore a=3,\ b=4$"]),
  red(138, [
    "Key concept: the minus sign in front of $b$ swaps where the maximum and minimum occur.",
    ("M1", r"$a+b=7$ and $a-b=-1$ formed"),
    ("A1", r"$a=3$"), ("A1", r"$b=4$"),
    ("Trap", r"$a-b=7$ comes from ignoring the minus sign in $-b\cos\dfrac{x}{2}$."),
  ]),
  blue(282, [
    r"$\text{period}=\dfrac{2\pi}{\frac{1}{2}}=4\pi$, so exactly one cycle on $0\le x\le 4\pi$",
    r"$f(0)=3-4(1)=-1$  (minimum at $x=0$)",
    r"$f(2\pi)=3-4(-1)=7$  (maximum at $x=2\pi$)",
    r"$f(4\pi)=-1$;  curve crosses $y=3$ at $x=\pi$ and $x=3\pi$"]),
  red(282, [
    ("B1", r"period $4\pi$"),
    ("B1", r"one complete cycle, starting and ending at the MINIMUM $-1$"),
    ("B1", r"maximum $7$ marked at $x=2\pi$"),
  ]),
 ]),
 dict(page=16, notes=[
  blue(78, [
    r"$3-4\cos\dfrac{x}{2}=5$",
    r"$-4\cos\dfrac{x}{2}=2$",
    r"$\cos\dfrac{x}{2}=-\dfrac{1}{2}$",
    r"$0\le x\le 4\pi$, so $0\le\dfrac{x}{2}\le 2\pi$",
    r"$\text{basic angle}=\dfrac{\pi}{3}$; cosine is negative in quadrants 2 and 3",
    r"$\dfrac{x}{2}=\pi-\dfrac{\pi}{3}=\dfrac{2\pi}{3}$ or $\dfrac{x}{2}=\pi+\dfrac{\pi}{3}=\dfrac{4\pi}{3}$",
    r"$\therefore x=\dfrac{4\pi}{3}$ or $x=\dfrac{8\pi}{3}$"]),
  red(78, [
    "Key concept: transform the RANGE as well as the angle — $\\dfrac{x}{2}$ runs to $2\\pi$ only.",
    ("M1", r"$\cos\dfrac{x}{2}=-\dfrac{1}{2}$"),
    ("M1", r"converts the range to $0\le\dfrac{x}{2}\le 2\pi$"),
    ("A1", r"$\dfrac{x}{2}=\dfrac{2\pi}{3},\ \dfrac{4\pi}{3}$"),
    ("A1", r"$x=\dfrac{4\pi}{3},\ \dfrac{8\pi}{3}$"),
    ("Trap", r"working in the original range gives four answers, two of which are outside; "
             r"doubling must come last."),
  ]),
 ]),
]
