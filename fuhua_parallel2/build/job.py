# -*- coding: utf-8 -*-
import os
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.abspath(os.path.join(
    HERE, "..", "..", "Fuhua_Parallel_Set2_Sec3_G3_EOY_AMath_2026_Paper.pdf"))
OUT = os.path.abspath(os.path.join(HERE, "..", "..", "fuhua_parallel2_ms_out"))

META = dict(
    layout="overlay", source_pdf=SRC, out_dir=OUT, total_marks=80,
    filename="CLG Fuhua-Parallel Set 2 Sec 3 G3 2026 EOY A-Math P1 - Marking Scheme",
    header="CLG FUHUA-PARALLEL SET 2 · SEC 3 G3 A-MATH EOY 2026 · PAPER 1",
    title="Fuhua-Parallel Set 2 · Sec 3 G3 EOY 2026 Paper 1 — Marking Scheme",
    source="Cambridge Learning Group · Fuhua-parallel practice paper, Set 2 · Paper 1 · 2026",
)

BX, BW = 85, 210
RX, RW = 312, 222


def blue(y, lines):
    return dict(kind="blue", x=BX, y=y, w=BW, lines=lines)


def red(y, lines):
    return dict(kind="red", x=RX, y=y, w=RW, lines=lines)


PAGES = [
 dict(page=3, notes=[
  blue(135, [
    r"At the points of intersection:",
    r"$x^{2}-3x+7=mx-2$",
    r"$x^{2}-(3+m)x+9=0$",
    r"Two distinct points, so the discriminant is positive:",
    r"$(3+m)^{2}-4(1)(9)>0$",
    r"$(m+3)^{2}>36$",
    r"$m+3>6$ or $m+3<-6$",
    r"$\therefore m>3$ or $m<-9$"]),
  red(135, [
    "Key concept: TWO DISTINCT points means $b^{2}-4ac>0$ — not $\\ge 0$, and not $b^{2}-4ac=0$.",
    ("M1", r"equates the two expressions and collects to $x^{2}-(3+m)x+9=0$"),
    ("M1", r"applies $b^{2}-4ac>0$ with $a=1,\ b=-(3+m),\ c=9$"),
    ("M1", r"solves the quadratic inequality in $m$"),
    ("A1", r"$m>3$ or $m<-9$"),
    ("Trap", r"writing $-9<m<3$ reverses the inequality — the parabola in $m$ opens "
             r"upwards, so the solution is the OUTSIDE pair of intervals."),
    ("Note", r"$c=9$, not $-9$: the $-2$ moves across as $+2$ onto the $+7$."),
  ]),
 ]),
 dict(page=4, notes=[
  blue(115, [
    r"$\dfrac{2\sqrt{3}+5}{3-\sqrt{3}}\times\dfrac{3+\sqrt{3}}{3+\sqrt{3}}$",
    r"numerator $N=\left(2\sqrt{3}+5\right)\left(3+\sqrt{3}\right)$",
    r"$N=6\sqrt{3}+2(3)+15+5\sqrt{3}$",
    r"$N=21+11\sqrt{3}$",
    r"denominator: $9-3=6$",
    r"$\therefore \dfrac{21+11\sqrt{3}}{6}=\dfrac{7}{2}+\dfrac{11}{6}\sqrt{3}$"]),
  red(115, [
    "Key concept: the conjugate of $3-\\sqrt{3}$ is $3+\\sqrt{3}$ — change the sign "
    "of the SURD term only.",
    ("M1", r"multiplies by the conjugate $\dfrac{3+\sqrt{3}}{3+\sqrt{3}}$"),
    ("M1", r"expands the numerator, using $\sqrt{3}\times\sqrt{3}=3$"),
    ("A1", r"$a=\dfrac{7}{2},\ b=\dfrac{11}{6}$"),
    ("Note", r"the question says RATIONAL, not integer — a fractional answer is "
             r"expected here and must not be rounded."),
  ]),
  blue(283, [
    r"$\sqrt{2x+3}=x-1$",
    r"squaring both sides: $2x+3=x^{2}-2x+1$",
    r"$x^{2}-4x-2=0$",
    r"$x=\dfrac{4\pm\sqrt{16+8}}{2}=2\pm\sqrt{6}$",
    r"check: $x-1\ge 0$, so $x\ge 1$",
    r"$2-\sqrt{6}\approx-0.449$, which is rejected",
    r"$\therefore x=2+\sqrt{6}$"]),
  red(283, [
    "Key concept: squaring can create a root that does not satisfy the original "
    "equation — every answer must be checked.",
    ("M1", r"squares correctly to $2x+3=x^{2}-2x+1$"),
    ("M1", r"formula or completing the square on $x^{2}-4x-2=0$"),
    ("A1", r"$x=2\pm\sqrt{6}$"),
    ("A1", r"rejects $2-\sqrt{6}$ with a reason, giving $x=2+\sqrt{6}$"),
    ("Trap", r"the right-hand side is $x-1$, so the condition is $x\ge 1$ — checking "
             r"only $2x+3\ge 0$ keeps the wrong root."),
  ]),
 ]),
 dict(page=5, notes=[
  blue(135, [
    r"$f(-2)=0$:  $-16+4a-2b+6=0$",
    r"$2a-b=5$   ... (1)",
    r"$f(3)=0$:  $54+9a+3b+6=0$",
    r"$3a+b=-20$   ... (2)",
    r"$(1)+(2)$:  $5a=-15$, so $a=-3$",
    r"from (1): $b=2(-3)-5=-11$",
    r"$f(x)=2x^{3}-3x^{2}-11x+6$",
    r"$f(x)=(x+2)\left(2x^{2}-7x+3\right)$",
    r"$\therefore f(x)=(x+2)(2x-1)(x-3)$"]),
  red(135, [
    "Key concept: two conditions of DIFFERENT kinds — a factor and a stated value — "
    "but both give a linear equation in $a$ and $b$.",
    ("M1", r"uses $f(-2)=0$ correctly"),
    ("M1", r"uses $f(3)=0$ and solves the pair simultaneously"),
    ("A1", r"$a=-3,\ b=-11$"),
    ("A1", r"$(x+2)(2x-1)(x-3)$"),
    ("Note", r"long division or comparing coefficients both earn the factorising mark."),
  ]),
  blue(325, [
    r"let $u=2^{y}$, so $2^{3y}=u^{3}$ and $2^{2y}=u^{2}$",
    r"$2u^{3}-3u^{2}-11u+6=0$, which is $f(u)=0$",
    r"$(u+2)(2u-1)(u-3)=0$",
    r"$u=-2$ (rejected: $2^{y}>0$),  $u=\dfrac{1}{2}$,  $u=3$",
    r"$2^{y}=\dfrac{1}{2}=2^{-1}$, so $y=-1$",
    r"$2^{y}=3$, so $y=\log_{2}3$",
    r"$\therefore y=-1$ or $y=\log_{2}3$"]),
  red(325, [
    "Key concept: the SAME cubic, with $2^{y}$ in place of $x$ — spot the substitution "
    "rather than starting again.",
    ("M1", r"substitutes $u=2^{y}$ and recognises $f(u)=0$"),
    ("A1", r"rejects $u=-2$, stating that a power of $2$ is always positive"),
    ("A1", r"$y=-1$ and $y=\log_{2}3$"),
    ("Trap", r"giving $y=\log_{2}(-2)$ as a third answer — it does not exist."),
    ("Note", r"exact form is demanded, so $\log_{2}3$ must not be written as $1.58$."),
  ]),
 ]),
 dict(page=6, notes=[
  blue(100, [
    r"let $g(x)=x^{3}-x^{2}+4x-4$ and group in pairs:",
    r"$g(x)=x^{2}(x-1)+4(x-1)$",
    r"$g(x)=(x-1)\left(x^{2}+4\right)$   (shown)"]),
  red(100, [
    "Key concept: factorising by grouping — the common bracket $(x-1)$ appears twice.",
    ("M1", r"groups as $x^{2}(x-1)+4(x-1)$"),
    ("A1", r"reaches $(x-1)\left(x^{2}+4\right)$ with the working shown"),
    ("Note", r"$x^{2}+4$ has no real factors, so it stays whole — this is the "
             r"irreducible quadratic used in part (b)."),
  ]),
  blue(232, [
    r"degree $3$ over degree $3$, so the fraction is improper:",
    r"$\dfrac{2x^{3}+2x^{2}+5x+6}{x^{3}-x^{2}+4x-4}=2+\dfrac{R(x)}{(x-1)\left(x^{2}+4\right)}$",
    r"$R(x)=\left(2x^{3}+2x^{2}+5x+6\right)$",
    r"$\qquad -2\left(x^{3}-x^{2}+4x-4\right)$",
    r"$R(x)=4x^{2}-3x+14$",
    r"$\dfrac{4x^{2}-3x+14}{(x-1)\left(x^{2}+4\right)}"
    r"\equiv\dfrac{A}{x-1}+\dfrac{Bx+C}{x^{2}+4}$",
    r"$4x^{2}-3x+14\equiv A\left(x^{2}+4\right)+(Bx+C)(x-1)$",
    r"$x=1$:  $15=5A$, so $A=3$",
    r"compare $x^{2}$:  $4=A+B$, so $B=1$",
    r"compare constants: $14=4A-C$, so $C=-2$",
    r"$\therefore 2+\dfrac{3}{x-1}+\dfrac{x-2}{x^{2}+4}$"]),
  red(232, [
    "Key concept: divide FIRST — an improper fraction has a quotient before any "
    "partial fraction is written.",
    ("M1", r"identifies the fraction as improper and extracts the quotient $2$"),
    ("A1", r"remainder $4x^{2}-3x+14$"),
    ("M1", r"correct form $\dfrac{A}{x-1}+\dfrac{Bx+C}{x^{2}+4}$"),
    ("M1", r"substitution or comparison to find the constants"),
    ("A1", r"$A=3,\ B=1,\ C=-2$"),
    ("A1", r"$2+\dfrac{3}{x-1}+\dfrac{x-2}{x^{2}+4}$"),
    ("Trap", r"writing $\dfrac{B}{x^{2}+4}$ instead of $\dfrac{Bx+C}{x^{2}+4}$ loses "
             r"the form mark and makes the system inconsistent."),
  ]),
 ]),
 dict(page=7, notes=[
  blue(100, [
    r"$\log_{3}(x+2)+\log_{3}(x-4)=3$",
    r"$\log_{3}\left[(x+2)(x-4)\right]=3$",
    r"$(x+2)(x-4)=3^{3}=27$",
    r"$x^{2}-2x-8=27$",
    r"$x^{2}-2x-35=0$",
    r"$(x-7)(x+5)=0$",
    r"$x=7$ or $x=-5$",
    r"$x=-5$ makes $\log_{3}(x-4)$ undefined, so it is rejected",
    r"$\therefore x=7$"]),
  red(100, [
    "Key concept: the product law first, then undo the logarithm with the base as "
    "a power.",
    ("M1", r"combines to a single logarithm"),
    ("M1", r"writes $(x+2)(x-4)=3^{3}$"),
    ("A1", r"$x^{2}-2x-35=0$"),
    ("A1", r"$x=7$ only, with $x=-5$ rejected and a reason given"),
    ("Trap", r"keeping $x=-5$: both brackets must be POSITIVE, so the domain is $x>4$."),
  ]),
  blue(262, [
    r"let $t=\log_{3}x$",
    r"$\log_{9}x=\dfrac{\log_{3}x}{\log_{3}9}=\dfrac{t}{2}$",
    r"$\log_{x}3=\dfrac{1}{\log_{3}x}=\dfrac{1}{t}$",
    r"$4\left(\dfrac{t}{2}\right)-\dfrac{1}{t}=1$",
    r"$2t-\dfrac{1}{t}=1$",
    r"$2t^{2}-t-1=0$",
    r"$(2t+1)(t-1)=0$",
    r"$t=1$ or $t=-\dfrac{1}{2}$",
    r"$\therefore x=3$ or $x=3^{-\frac{1}{2}}=\dfrac{\sqrt{3}}{3}$"]),
  red(262, [
    "Key concept: change EVERYTHING to base $3$ — two different bases cannot be "
    "combined until they match.",
    ("M1", r"$\log_{9}x=\dfrac{1}{2}\log_{3}x$"),
    ("M1", r"$\log_{x}3=\dfrac{1}{\log_{3}x}$  (the reciprocal law)"),
    ("M1", r"forms and solves $2t^{2}-t-1=0$"),
    ("A1", r"$x=3$ and $x=\dfrac{\sqrt{3}}{3}$"),
    ("Note", r"both roots are valid: $x>0$ and $x\ne 1$ are the only restrictions."),
    ("Trap", r"discarding $t=-\dfrac{1}{2}$ as impossible — a logarithm may be "
             r"negative; it is the ARGUMENT that cannot be."),
  ]),
 ]),
 dict(page=8, notes=[
  blue(150, [
    r"$500=M_{0}e^{-2k}$   ... (1)",
    r"$320=M_{0}e^{-10k}$   ... (2)",
    r"$\dfrac{(2)}{(1)}$:  $\dfrac{320}{500}=e^{-8k}$",
    r"$e^{-8k}=0.64$",
    r"$-8k=\ln 0.64$",
    r"$k=0.055786\ldots\approx 0.0558$",
    r"from (1): $M_{0}=500e^{2k}=500e^{0.111572}$",
    r"$\therefore M_{0}\approx 559$ g"]),
  red(150, [
    "Key concept: $M_{0}$ is unknown AND the readings are not at $t=0$ — divide the "
    "two equations to eliminate it.",
    ("M1", r"two correct equations from the two readings"),
    ("M1", r"divides to eliminate $M_{0}$, reaching $e^{-8k}=0.64$"),
    ("A1", r"$k\approx 0.0558$"),
    ("A1", r"$M_{0}\approx 559$"),
    ("Trap", r"assuming $M_{0}=500$ — that is the mass at $t=2$, not at $t=0$."),
    ("Note", r"keep the unrounded $k$ in the calculator for part (b)."),
  ]),
  blue(340, [
    r"$100=M_{0}e^{-kt}$",
    r"$e^{-kt}=\dfrac{100}{559.017}$",
    r"$-kt=\ln\left(0.178884\right)$",
    r"$t=\dfrac{1.720898}{0.055786}=30.849\ldots$",
    r"the mass is still above $100$ g at $t=30$",
    r"$\therefore$ least number of complete days: $t=31$"]),
  red(340, [
    "Key concept: a CEILING answer — the decimal is not the answer, the next whole "
    "day is.",
    ("M1", r"sets $M=100$ and takes logarithms"),
    ("A1", r"$t=30.8$ (accept $30.8$ to $30.9$)"),
    ("A1", r"$31$ days"),
    ("Trap", r"rounding $30.849$ to $31$ by ordinary rounding is luck, not method — "
             r"state that the mass first drops below $100$ g DURING day $31$."),
    ("Note", r"using the rounded $k=0.0558$ gives $30.84$, still $31$ — but marks "
             r"for accuracy follow through only if the method is shown."),
  ]),
 ]),
 dict(page=9, notes=[
  blue(118, [
    r"general term: $\binom{6}{r}2^{6-r}(kx)^{r}$",
    r"coefficient of $x^{2}$:  $\binom{6}{2}2^{4}k^{2}=15(16)k^{2}=240k^{2}$",
    r"coefficient of $x^{3}$:  $\binom{6}{3}2^{3}k^{3}=20(8)k^{3}=160k^{3}$",
    r"$160k^{3}=2\left(240k^{2}\right)$",
    r"$k\ne 0$, so divide by $160k^{2}$: $\therefore k=3$"]),
  red(118, [
    "Key concept: form BOTH coefficients in terms of $k$, then let the stated "
    "relation give the equation.",
    ("M1", r"correct general term with both the power of $2$ and the power of $k$"),
    ("A1", r"$240k^{2}$ and $160k^{3}$"),
    ("M1", r"forms $160k^{3}=2\left(240k^{2}\right)$ and divides by $k^{2}$"),
    ("A1", r"$k=3$"),
    ("Trap", r"dropping the $2^{6-r}$ factor — the coefficients are then $15k^{2}$ "
             r"and $20k^{3}$ and $k$ comes out as $\dfrac{3}{2}$."),
  ]),
  blue(295, [
    r"from (a) the bracket is $\left(2+3x\right)^{6}$",
    r"coefficient of $x$:  $\binom{6}{1}2^{5}(3)=6(32)(3)=576$",
    r"coefficient of $x^{2}$:  $\binom{6}{2}2^{4}\left(3^{2}\right)=15(16)(9)=2160$",
    r"$\left(1-2x\right)\left(2+3x\right)^{6}$ gives $x^{2}$ from:",
    r"$1\times 2160$ and $(-2x)\times 576x$",
    r"$1(2160)+(-2)(576)=2160-1152$",
    r"$\therefore$ coefficient of $x^{2}$ is $1008$"]),
  red(295, [
    "Key concept: TWO terms contribute — the $x^{2}$ term times $1$, and the $x$ "
    "term times $-2x$.",
    ("M1", r"both coefficients $576$ and $2160$ from the expansion"),
    ("M1", r"combines $1\times 2160$ with $(-2)\times 576$"),
    ("A1", r"$1008$"),
    ("Trap", r"quoting $2160$ alone ignores the bracket in front — one slip in (a) "
             r"carries through both marks here."),
  ]),
 ]),
 dict(page=10, notes=[
  blue(132, [
    r"midpoint of $AB$: $\left(\dfrac{-2+6}{2},\ \dfrac{3+7}{2}\right)=(2,\ 5)$",
    r"gradient of $AB$: $\dfrac{7-3}{6-(-2)}=\dfrac{4}{8}=\dfrac{1}{2}$",
    r"perpendicular gradient: $-2$",
    r"$y-5=-2(x-2)$",
    r"$\therefore y=-2x+9$"]),
  red(132, [
    "Key concept: a perpendicular bisector needs BOTH the midpoint and the negative "
    "reciprocal gradient.",
    ("B1", r"midpoint $(2,\ 5)$"),
    ("M1", r"gradient $\dfrac{1}{2}$, then perpendicular gradient $-2$"),
    ("A1", r"$y=-2x+9$"),
    ("Note", r"$m_{1}m_{2}=-1$ is the test; $\dfrac{1}{2}\times(-2)=-1$ ✓"),
  ]),
  blue(292, [
    r"on the $x$-axis, $y=0$:",
    r"$0=-2x+9$",
    r"$x=\dfrac{9}{2}$",
    r"$\therefore C\left(\dfrac{9}{2},\ 0\right)$"]),
  red(292, [
    "Key concept: the $x$-axis is the line $y=0$.",
    ("M1", r"substitutes $y=0$ into the bisector"),
    ("A1", r"$C\left(\dfrac{9}{2},\ 0\right)$"),
    ("Note", r"leave it as $\dfrac{9}{2}$ — $4.5$ is accepted, $4$ is not."),
  ]),
 ]),
 dict(page=11, notes=[
  blue(84, [
    r"$C$ lies on the perpendicular bisector of $AB$.",
    r"Every point on the perpendicular bisector of $AB$ is equidistant from "
    r"$A$ and $B$.",
    r"$\therefore CA=CB$, so triangle $ABC$ is isosceles."]),
  red(84, [
    "Key concept: this is the REASONING mark — quote the equidistance property, "
    "do not merely compute.",
    ("B1", r"states that $C$ lies on the perpendicular bisector of $AB$"),
    ("B1", r"concludes $CA=CB$, hence isosceles"),
    ("Note", r"a full distance calculation showing $CA=CB$ scores both marks, but "
             r"the one-line property argument is what the examiner wants."),
  ]),
  blue(212, [
    r"$AB=\sqrt{8^{2}+4^{2}}=\sqrt{80}=4\sqrt{5}$",
    r"$\text{area}=\dfrac{1}{2}\times AB\times h=30$",
    r"$h=\dfrac{60}{4\sqrt{5}}=\dfrac{15}{\sqrt{5}}=3\sqrt{5}$",
    r"$D$ is on the bisector, so $h$ is measured from the midpoint $M(2,\ 5)$",
    r"along the bisector, whose direction is $\dfrac{(1,\ -2)}{\sqrt{5}}$",
    r"$D=(2,\ 5)\pm 3\sqrt{5}\times\dfrac{(1,\ -2)}{\sqrt{5}}=(2,\ 5)\pm 3(1,\ -2)$",
    r"$\therefore D(5,\ -1)$ or $D(-1,\ 11)$"]),
  red(212, [
    "Key concept: the perpendicular bisector is already perpendicular to $AB$, so "
    "the distance from $D$ to $AB$ is just $MD$.",
    ("M1", r"$AB=4\sqrt{5}$"),
    ("M1", r"uses $\text{area}=\dfrac{1}{2}\times AB\times h$ to get $h=3\sqrt{5}$"),
    ("M1", r"measures $3\sqrt{5}$ from $M(2,\ 5)$ along the bisector"),
    ("A1", r"$D(5,\ -1)$"),
    ("A1", r"$D(-1,\ 11)$"),
    ("Trap", r"giving only one point — POSSIBLE coordinates means both sides of "
             r"$AB$ must be given."),
    ("Note", r"the shoelace formula with $D(x,\ -2x+9)$ also works and earns the "
             r"same marks."),
  ]),
 ]),
 dict(page=12, notes=[
  blue(695, [
    r"$y=ax^{b}$",
    r"$\lg y=\lg a+b\lg x$",
    r"plot $\lg y$ against $\lg x$: gradient $b$, vertical intercept $\lg a$.",
    r"$\lg x$:  $0,\ 0.602,\ 1.204,\ 1.556,\ 2.000$",
    r"$\lg y$:  $0.477,\ 0.778,\ 1.079,\ 1.255,\ 1.477$"]),
  red(695, [
    "Key concept: take logarithms of BOTH variables — a power law needs $\\lg x$, "
    "not $x$.",
    ("B1", r"$\lg y=\lg a+b\lg x$"),
    ("B1", r"states: plot $\lg y$ against $\lg x$, gradient $b$, intercept $\lg a$"),
    ("B1", r"both logarithm rows computed and a ruled straight line drawn"),
    ("Trap", r"plotting $\lg y$ against $x$ suits $y=ab^{x}$, not $y=ax^{b}$."),
  ]),
 ]),
 dict(page=13, notes=[
  blue(90, [
    r"gradient $b=\dfrac{1.477-0.477}{2.000-0}=\dfrac{1.000}{2.000}$",
    r"$b\approx 0.5$",
    r"$\text{vertical intercept}=\lg a=0.477$",
    r"$a=10^{0.477}$",
    r"$\therefore a\approx 3,\ b\approx 0.5$"]),
  red(90, [
    "Key concept: the intercept is $\\lg a$, NOT $a$ — one more step is needed.",
    ("M1", r"gradient from two points on the drawn line"),
    ("A1", r"$b\approx 0.5$"),
    ("M1", r"reads the intercept and applies $a=10^{\text{intercept}}$"),
    ("A1", r"$a\approx 3$"),
    ("Note", r"accept $a$ from $2.8$ to $3.2$ and $b$ from $0.47$ to $0.53$."),
    ("Note", r"check: $y=3\sqrt{x}$ gives $y=12$ at $x=16$ ✓"),
  ]),
 ]),
 dict(page=14, notes=[
  blue(122, [
    r"$180^{\circ}<C<270^{\circ}$, so $C$ is in quadrant 3",
    r"in quadrant 3 both sine and cosine are negative",
    r"$\sin^{2}C+\cos^{2}C=1$",
    r"$\cos^{2}C=1-q^{2}$",
    r"$\therefore \cos C=-\sqrt{1-q^{2}}$"]),
  red(122, [
    "Key concept: the quadrant fixes the SIGN; the identity fixes only the size.",
    ("M1", r"uses $\sin^{2}C+\cos^{2}C=1$"),
    ("A1", r"$\cos C=-\sqrt{1-q^{2}}$, negative sign justified by quadrant 3"),
    ("Note", r"$q$ is itself negative here, since $\sin C<0$ in quadrant 3."),
  ]),
  blue(250, [
    r"$\tan C=\dfrac{\sin C}{\cos C}$",
    r"$\tan C=\dfrac{q}{-\sqrt{1-q^{2}}}$",
    r"$\therefore \tan C=-\dfrac{q}{\sqrt{1-q^{2}}}$"]),
  red(250, [
    "Key concept: build $\\tan$ from the two ratios already found — no new triangle.",
    ("M1", r"$\tan C=\dfrac{\sin C}{\cos C}$ with both substituted"),
    ("A1", r"$-\dfrac{q}{\sqrt{1-q^{2}}}$"),
    ("Note", r"this is POSITIVE, because $q<0$ — tangent is positive in quadrant 3, "
             r"a useful check."),
  ]),
  blue(378, [
    r"$\cos\left(360^{\circ}-C\right)=\cos C$",
    r"$\sec\left(360^{\circ}-C\right)=\dfrac{1}{\cos C}$",
    r"$\sec\left(360^{\circ}-C\right)=\dfrac{1}{-\sqrt{1-q^{2}}}$",
    r"$\therefore \sec\left(360^{\circ}-C\right)=-\dfrac{1}{\sqrt{1-q^{2}}}$"]),
  red(378, [
    "Key concept: $360^{\\circ}-C$ is a quadrant-4 angle, where cosine keeps its "
    "sign — so the value is simply $\\cos C$.",
    ("M1", r"$\cos\left(360^{\circ}-C\right)=\cos C$"),
    ("A1", r"$-\dfrac{1}{\sqrt{1-q^{2}}}$"),
    ("Trap", r"writing $\sec\left(360^{\circ}-C\right)=\sec C$ and then leaving it "
             r"there — the answer must be in terms of $q$."),
  ]),
 ]),
 dict(page=15, notes=[
  blue(110, [
    r"$\text{LHS}=\dfrac{(1-\cos\theta)^{2}+\sin^{2}\theta}{\sin\theta(1-\cos\theta)}$",
    r"using $\cos^{2}\theta+\sin^{2}\theta=1$:",
    r"$\text{LHS}=\dfrac{2-2\cos\theta}{\sin\theta(1-\cos\theta)}"
    r"=\dfrac{2(1-\cos\theta)}{\sin\theta(1-\cos\theta)}$",
    r"$\text{LHS}=\dfrac{2}{\sin\theta}=2\cosec\theta=\text{RHS}$   (proved)"]),
  red(110, [
    "Key concept: work on ONE side only, and let $\\sin^{2}\\theta+\\cos^{2}\\theta=1$ "
    "collapse the numerator.",
    ("M1", r"single fraction over $\sin\theta(1-\cos\theta)$"),
    ("M1", r"applies $\cos^{2}\theta+\sin^{2}\theta=1$ to reach $2-2\cos\theta$"),
    ("A1", r"cancels $(1-\cos\theta)$ and concludes $2\cosec\theta$"),
    ("Trap", r"cross-multiplying both sides is not a proof — it assumes the result."),
  ]),
  blue(300, [
    r"by part (a): $2\cosec\theta=4$",
    r"$\cosec\theta=2$",
    r"$\sin\theta=\dfrac{1}{2}$",
    r"$\text{basic angle}=30^{\circ}$; sine is positive in quadrants 1 and 2",
    r"$\theta=30^{\circ}$ or $\theta=180^{\circ}-30^{\circ}$",
    r"$\therefore \theta=30^{\circ}$ or $\theta=150^{\circ}$"]),
  red(300, [
    "Key concept: HENCE — use the identity, do not restart from the fraction.",
    ("M1", r"$\cosec\theta=2$, hence $\sin\theta=\dfrac{1}{2}$"),
    ("A1", r"$\theta=30^{\circ}$"),
    ("A1", r"$\theta=150^{\circ}$"),
    ("Note", r"$\theta=0^{\circ}$ and $\theta=180^{\circ}$ are excluded anyway — "
             r"the original expression is undefined there."),
  ]),
 ]),
 dict(page=16, notes=[
  blue(382, [
    r"$y=2+3\sin 2x$",
    r"$\text{amplitude}=3$",
    r"$\text{period}=\dfrac{360^{\circ}}{2}=180^{\circ}$",
    r"$\text{maximum}=2+3=5$",
    r"$\text{minimum}=2-3=-1$",
    r"the curve starts at $(0,\ 2)$, rising",
    r"two complete cycles on $0^{\circ}\le x\le 360^{\circ}$",
    r"maxima at $x=45^{\circ}$ and $x=225^{\circ}$",
    r"minima at $x=135^{\circ}$ and $x=315^{\circ}$"]),
  red(382, [
    "Key concept: $\\sin 2x$ halves the period, and the $+2$ lifts the whole curve — "
    "the amplitude is unchanged.",
    ("B1", r"amplitude $3$"),
    ("B1", r"period $180^{\circ}$"),
    ("B1", r"two complete cycles drawn, starting and ending at $y=2$"),
    ("B1", r"maximum $5$ and minimum $-1$ correctly placed"),
    ("Trap", r"drawing one cycle — the period is $180^{\circ}$, so $360^{\circ}$ "
             r"holds exactly two."),
  ]),
 ]),
]
