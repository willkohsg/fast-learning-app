# -*- coding: utf-8 -*-
import os
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.abspath(os.path.join(HERE, "..", "..", "Sec3_EOY_AMath_Paper.pdf"))
OUT = os.path.abspath(os.path.join(HERE, "..", "..", "marking_scheme_out"))

META = dict(
    layout="overlay", source_pdf=SRC, out_dir=OUT, total_marks=90,
    filename="CLG Sec 3 Express 2026 EOY A-Math Paper 1 - Marking Scheme",
    header="CLG SEC 3 EXPRESS · ADDITIONAL MATHEMATICS EOY · PAPER 1",
    title="Sec 3 Express End-of-Year Paper 1 — Marking Scheme",
    source="Cambridge Learning Group · Sec 3 Express EOY · Paper 1 · 2026",
)

BX, BW = 85, 210          # blue column
RX, RW = 312, 222         # red column


def blue(y, lines, x=BX, w=BW):
    return dict(kind="blue", x=x, y=y, w=w, lines=lines)


def red(y, lines, x=RX, w=RW):
    return dict(kind="red", x=x, y=y, w=w, lines=lines)


PAGES = [
 # ------------------------------------------------------------------ p3
 dict(page=3, notes=[
  blue(158, [
    r"$\text{Area}=\dfrac{1}{2}(DE)(DF)\sin 60^{\circ}$",
    r"$\dfrac{1}{4}\left(7\sqrt{3}+9\right)=\dfrac{1}{2}\left(\sqrt{3}+2\right)(DF)\times\dfrac{\sqrt{3}}{2}$",
    r"$7\sqrt{3}+9=\left(3+2\sqrt{3}\right)(DF)$",
    r"$DF=\dfrac{7\sqrt{3}+9}{3+2\sqrt{3}}\times\dfrac{3-2\sqrt{3}}{3-2\sqrt{3}}$",
    r"$DF=\dfrac{3\sqrt{3}-15}{-3}$",
    r"$\therefore DF=5-\sqrt{3}\text{ cm}$"]),
  red(158, [
    "Key concept: area with the included angle, then rationalise.",
    ("M1", r"$\dfrac{1}{2}(DE)(DF)\sin 60^{\circ}$ used, with $\sin 60^{\circ}=\dfrac{\sqrt{3}}{2}$"),
    ("M1", r"multiplying by the conjugate $3-2\sqrt{3}$"),
    ("A1", r"$DF=5-\sqrt{3}$, so $a=5$ and $b=-1$"),
    ("Note", r"$(3)^{2}-\left(2\sqrt{3}\right)^{2}=9-12=-3$ is negative. Dropping that sign gives $\sqrt{3}-5$."),
    ("Trap", r"$\sqrt{3}\times\sqrt{3}=3$, not $\sqrt{3}$.")]),
  blue(395, [
    r"$\dfrac{7}{3-\sqrt{2}}\times\dfrac{3+\sqrt{2}}{3+\sqrt{2}}=\dfrac{7\left(3+\sqrt{2}\right)}{9-2}$",
    r"$\dfrac{7\left(3+\sqrt{2}\right)}{9-2}=\dfrac{7\left(3+\sqrt{2}\right)}{7}=3+\sqrt{2}$"]),
  red(395, [
    "Key concept: multiply by the conjugate of the denominator.",
    ("M1", r"conjugate $3+\sqrt{2}$ used and denominator $9-2=7$"),
    ("A1", r"$3+\sqrt{2}$, so $a=3$ and $b=1$")]),
  blue(555, [
    r"$x=\dfrac{5+4\sqrt{3}}{2+\sqrt{3}}\times\dfrac{2-\sqrt{3}}{2-\sqrt{3}}$",
    r"$\text{denominator}=4-3=1$",
    r"$x=10-5\sqrt{3}+8\sqrt{3}-12$",
    r"$\therefore x=-2+3\sqrt{3}$"]),
  red(555, [
    ("M1", r"conjugate $2-\sqrt{3}$ used"),
    ("A1", r"$x=-2+3\sqrt{3}$, so $a=-2$ and $b=3$"),
    ("Note", r"the denominator rationalises to exactly $1$ — the product must still be expanded.")]),
 ]),
 # ------------------------------------------------------------------ p4
 dict(page=4, notes=[
  blue(112, [
    r"$\sin A<0\Rightarrow A$ in quadrant 3 or 4",
    r"$\tan B>0\Rightarrow B$ in quadrant 1 or 3",
    r"same quadrant $\Rightarrow$ both in quadrant 3",
    r"$\cos A=-\dfrac{2}{\sqrt{5}}$",
    r"$\sin B=-\dfrac{3}{5},\ \cos B=-\dfrac{4}{5}$",
    r"$\cos(A-B)=\cos A\cos B+\sin A\sin B$",
    r"$\cos(A-B)=\left(-\dfrac{2}{\sqrt{5}}\right)\left(-\dfrac{4}{5}\right)+\left(-\dfrac{1}{\sqrt{5}}\right)\left(-\dfrac{3}{5}\right)$",
    r"$\cos(A-B)=\dfrac{11}{5\sqrt{5}}=\dfrac{11\sqrt{5}}{25}$",
    r"$\therefore p=\dfrac{11}{25}$"]),
  red(112, [
    "Key concept: find the quadrant first; both ratios are then negative.",
    ("B1", r"both $A$ and $B$ placed in quadrant 3"),
    ("B1", r"$\sin B=-\dfrac{3}{5}$ and $\cos B=-\dfrac{4}{5}$ from the right-angled triangle with sides $3,\ 4,\ 5$"),
    ("M1", r"$\cos A\cos B+\sin A\sin B$ used"),
    ("A1", r"$p=\dfrac{11}{25}$"),
    ("Note", r"a CAST diagram alone earns the first B1 only — the ratios must be written down.")]),
 ]),
 # ------------------------------------------------------------------ p5
 dict(page=5, notes=[
  blue(112, [
    r"$-2x^{2}-12x+5=-2\left(x^{2}+6x\right)+5$",
    r"$-2\left(x^{2}+6x\right)+5=-2\left[(x+3)^{2}-9\right]+5$",
    r"$-2\left[(x+3)^{2}-9\right]+5=-2(x+3)^{2}+18+5$",
    r"$\therefore y=-2(x+3)^{2}+23$"]),
  red(112, [
    ("M1", r"$-2$ factorised out and the square completed inside"),
    ("A1", r"$a=2,\ b=3,\ c=23$")]),
  blue(305, [
    r"$-2(x+3)^{2}+23=k$",
    r"$(x+3)^{2}=\dfrac{23-k}{2}$",
    r"two distinct roots need $\dfrac{23-k}{2}>0$",
    r"none when $\dfrac{23-k}{2}\le 0$",
    r"$\therefore k\ge 23$"]),
  red(305, [
    "Key concept: equal roots are not two distinct roots, so the boundary is included.",
    ("M1", r"$b^{2}-4ac\le 0$ or $(x+3)^{2}\le 0$ used"),
    ("A1", r"$k\ge 23$"),
    ("Note", r"by discriminant: $2x^{2}+12x+(k-5)=0$ gives $184-8k\le 0$."),
    ("Trap", r"writing $k>23$ loses the A1.")]),
 ]),
 # ------------------------------------------------------------------ p6
 dict(page=6, notes=[
  blue(95, [
    r"$x-1=nx^{2}+3x-n$",
    r"$nx^{2}+2x+(1-n)=0$",
    r"$\text{discriminant}=2^{2}-4(n)(1-n)$",
    r"$\text{discriminant}=4-4n+4n^{2}=4\left(n^{2}-n+1\right)$",
    r"$n^{2}-n+1=\left(n-\dfrac{1}{2}\right)^{2}+\dfrac{3}{4}$",
    r"$\left(n-\dfrac{1}{2}\right)^{2}\ge 0$, so $n^{2}-n+1\ge\dfrac{3}{4}>0$",
    "discriminant is positive for all real $n$, so the line meets the curve at two distinct points."]),
  red(95, [
    "Key concept: show the discriminant is POSITIVE, not merely non-zero.",
    ("M1", r"the two equations set equal"),
    ("A1", r"$nx^{2}+2x+(1-n)=0$"),
    ("M1", r"discriminant $4\left(n^{2}-n+1\right)$ formed"),
    ("M1", r"square completed, or discriminant of $n^{2}-n+1$ shown to be $-3<0$"),
    ("A1", r"concludes $\text{discriminant}>0$, hence two distinct points"),
    ("Note", r"asserting positivity without justification scores the M marks only.")]),
 ]),
 # ------------------------------------------------------------------ p7
 dict(page=7, notes=[
  blue(95, [
    r"$\log_{3}9=2$, so $\text{RHS}=\dfrac{1}{2}\times 2=1$",
    r"$2\log_{4}(x-3)=\dfrac{2\log_{2}(x-3)}{\log_{2}4}=\log_{2}(x-3)$",
    r"$\log_{2}\left[(x-2)(x-3)\right]=1$",
    r"$(x-2)(x-3)=2$",
    r"$x^{2}-5x+4=0$",
    r"$(x-1)(x-4)=0$",
    r"$x=1$ or $x=4$",
    r"need $x-2>0$ and $x-3>0$, so $x>3$",
    r"$\therefore x=4$"]),
  red(95, [
    "Key concept: change base to 2, combine, then test the domain.",
    ("B1", r"$\text{RHS}=1$"),
    ("M1", r"$\log_{4}$ changed to base 2"),
    ("M1", r"logs combined and the equation made quadratic"),
    ("A1", r"$x=1$ and $x=4$"),
    ("A1", r"$x=1$ rejected because $x>3$; $x=4$"),
    ("Trap", r"rejecting with $x>0$ is not a reason — $x=1$ satisfies it.")]),
 ]),
 # ------------------------------------------------------------------ p8
 dict(page=8, notes=[
  blue(146, [
    r"$x^{2}+4$ is an irreducible quadratic — $x^{2}=-4$ has no real root, so it has no real linear factor.",
    r"A factor of degree $2$ needs a numerator of degree $1$, i.e. $Bx+C$.",
    r"With only $A$ and $B$ there are $2$ unknowns but $3$ coefficients to match."]),
  red(146, [
    ("B1", r"states $x^{2}+4$ is irreducible / has no real linear factors"),
    ("B1", r"states the numerator over $x^{2}+4$ must be linear, $Bx+C$"),
    ("Note", r"writing the correct form without a reason earns the second B1 only.")]),
  blue(323, [
    r"$\dfrac{3x^{2}+3x+10}{(x+1)\left(x^{2}+4\right)}=\dfrac{A}{x+1}+\dfrac{Bx+C}{x^{2}+4}$",
    r"$3x^{2}+3x+10=A\left(x^{2}+4\right)+(Bx+C)(x+1)$",
    r"$x=-1$:  $10=5A$, so $A=2$",
    r"compare $x^{2}$:  $3=A+B$, so $B=1$",
    r"compare constants:  $10=4A+C$, so $C=2$",
    r"$\therefore\dfrac{2}{x+1}+\dfrac{x+2}{x^{2}+4}$"]),
  red(323, [
    ("M1", r"correct form with $Bx+C$ written down"),
    ("M1", r"$x=-1$ substituted to give $A=2$"),
    ("A1", r"$B=1$"),
    ("A1", r"$C=2$"),
    ("Note", r"check: $2\left(x^{2}+4\right)+(x+2)(x+1)=3x^{2}+3x+10$.")]),
 ]),
 # ------------------------------------------------------------------ p9
 dict(page=9, notes=[
  blue(110, [
    r"$m_{AC}=\dfrac{1-3}{3-2}=-2$",
    r"$m_{BC}=\dfrac{1-(-1)}{3-(-1)}=\dfrac{2}{4}=\dfrac{1}{2}$",
    r"$m_{AC}\times m_{BC}=-2\times\dfrac{1}{2}=-1$",
    r"$\therefore AC$ is perpendicular to $BC$."]),
  red(110, [
    ("M1", r"$m_{AC}=-2$"),
    ("M1", r"$m_{BC}=\dfrac{1}{2}$"),
    ("A1", r"$\text{product}=-1$ and the conclusion stated")]),
  blue(252, [
    r"diagonals bisect: $\text{midpoint }AC=\text{midpoint }BD$",
    r"midpoint $AC=\left(\dfrac{5}{2},\,2\right)$",
    r"$\dfrac{-1+x_{D}}{2}=\dfrac{5}{2},\ \dfrac{-1+y_{D}}{2}=2$",
    r"$\therefore D(6,\,5)$"]),
  red(252, [
    ("M1", r"$\text{midpoint }AC=\text{midpoint }BD$ used"),
    ("A1", r"$D(6,\,5)$"),
    ("Trap", r"$\text{midpoint }AB=\text{midpoint }DC$ is false — those are opposite sides.")]),
  blue(364, [
    r"right angle at $C$, so $\text{area}=2\times\dfrac{1}{2}(AC)(BC)$",
    r"$AC=\sqrt{1^{2}+(-2)^{2}}=\sqrt{5}$",
    r"$BC=\sqrt{4^{2}+2^{2}}=2\sqrt{5}$",
    r"$\text{area}=\sqrt{5}\times 2\sqrt{5}=10$ units$^{2}$"]),
  red(364, [
    ("M1", r"a correct area method (perpendicular sides, or the shoelace formula)"),
    ("A1", r"$10$ units$^{2}$"),
    ("Note", r"part (i) makes $AC\perp BC$ available — that is the short route.")]),
 ]),
 # ------------------------------------------------------------------ p10
 dict(page=10, notes=[
  blue(125, [
    r"maximum: $a+b=4$",
    r"minimum: $-a+b=-10$",
    r"adding: $2b=-6$, so $b=-3$",
    r"$\therefore a=7,\ b=-3$"]),
  red(125, [
    ("M1", r"both $a+b=4$ and $-a+b=-10$ formed"),
    ("A1", r"$b=-3$"), ("A1", r"$a=7$")]),
  blue(253, [
    r"$\text{period}=\dfrac{2\pi}{2}=\pi$",
    r"$\text{amplitude}=7$"]),
  red(253, [
    ("B1", r"period $\pi$"), ("B1", r"amplitude $7$"),
    ("Trap", r"the amplitude is $a=7$, not $14$, and $b$ does not change it.")]),
  blue(602, [
    r"$y=7\cos 2x-3$: cosine shape, $2$ complete cycles on $0\le x\le 2\pi$",
    r"maximum $4$ at $x=0,\ \pi,\ 2\pi$; minimum $-10$ at $x=\dfrac{\pi}{2},\ \dfrac{3\pi}{2}$",
    r"oscillates about $y=-3$, crossing it at $x=\dfrac{\pi}{4},\dfrac{3\pi}{4},\dfrac{5\pi}{4},\dfrac{7\pi}{4}$"]),
  red(602, [
    ("B1", r"correct shape, starting at a maximum, $2$ equal cycles"),
    ("B1", r"maximum $4$ and minimum $-10$ shown at the right values of $x$")]),
 ]),
 # ------------------------------------------------------------------ p11
 dict(page=11, notes=[
  blue(158, [
    r"$t=1,\ P=50\,000$:",
    r"$50\,000=45\,000e^{k}$",
    r"$e^{k}=\dfrac{50\,000}{45\,000}=\dfrac{10}{9}$",
    r"$k=\ln\dfrac{10}{9}=0.1053605\ldots$",
    r"$\therefore k=0.10536$ ($5$ s.f.)"]),
  red(158, [
    ("M1", r"$t=1$ and $P=50\,000$ substituted"),
    ("M1", r"$e^{k}=\dfrac{10}{9}$"),
    ("A1", r"$k=0.10536$ correct to $5$ s.f.")]),
  blue(317, [
    r"tripled: $P=3\times 45\,000=135\,000$",
    r"$135\,000=45\,000e^{kt}$",
    r"$e^{kt}=3$",
    r"$t=\dfrac{\ln 3}{0.1053605}=\dfrac{1.098612}{0.1053605}$",
    r"$t=10.427\ldots\approx 10.43$ years",
    r"$10.43$ years after the start of $2015$ falls in $2025$."]),
  red(317, [
    "Key concept: triple the ORIGINAL investment, then read off the calendar year.",
    ("M1", r"$P=3\times 45\,000=135\,000$"),
    ("M1", r"$e^{kt}=3$"),
    ("M1", r"$t=\dfrac{\ln 3}{k}$"),
    ("A1", r"the year $2025$"),
    ("Trap", r"tripling the $\$50\,000$ valuation, or stopping at $t=10.4$ without naming the year.")]),
 ]),
 # ------------------------------------------------------------------ p12
 dict(page=12, notes=[
  blue(110, [
    r"general term of $\left(2x-\dfrac{1}{4x^{2}}\right)^{12}$:",
    r"$\binom{12}{r}(2x)^{12-r}\left(-\dfrac{1}{4x^{2}}\right)^{r}$",
    r"$\text{i.e. }\binom{12}{r}2^{12-r}(-1)^{r}4^{-r}x^{12-3r}$",
    r"with $3x^{3}$ the power of $x$ is $3+12-3r=15-3r$",
    r"$15-3r=0\Rightarrow r=5$",
    r"$\text{term}=3\binom{12}{5}2^{7}(-1)^{5}4^{-5}$",
    r"$\text{term}=3\times 792\times\dfrac{128}{1024}\times(-1)$",
    r"$\therefore\text{term}=-297$"]),
  red(110, [
    "Key concept: write the GENERAL term, then set the power of $x$ to zero.",
    ("M1", r"general term $\binom{12}{r}(2x)^{12-r}\left(-\dfrac{1}{4x^{2}}\right)^{r}$"),
    ("M1", r"$15-3r=0$ giving $r=5$"),
    ("A1", r"$-297$"),
    ("Trap", r"$(-1)^{5}$ makes it negative; $\binom{12}{5}=792$ and $\dfrac{128}{1024}=\dfrac{1}{8}$.")]),
  blue(333, [
    r"coefficient of $x^{7}$: $\binom{15}{7}2^{8}m^{7}$",
    r"coefficient of $x^{9}$: $\binom{15}{9}2^{6}m^{9}$",
    r"$\dfrac{\binom{15}{7}2^{8}m^{7}}{\binom{15}{9}2^{6}m^{9}}=\dfrac{4}{7}$",
    r"$\dfrac{6435}{5005}=\dfrac{9}{7}$, so $\dfrac{9}{7}\times\dfrac{4}{m^{2}}=\dfrac{4}{7}$",
    r"$\dfrac{36}{7m^{2}}=\dfrac{4}{7}$",
    r"$m^{2}=9$",
    r"$\therefore m=3$ or $m=-3$"]),
  red(333, [
    ("M1", r"coefficient of $x^{7}$ as $\binom{15}{7}2^{8}m^{7}$"),
    ("M1", r"coefficient of $x^{9}$ as $\binom{15}{9}2^{6}m^{9}$"),
    ("M1", r"ratio formed and equated to $\dfrac{4}{7}$"),
    ("M1", r"simplified to $m^{2}=9$"),
    ("A1", r"$m=\pm 3$"),
    ("Trap", r"both signs are needed — the ratio depends on $m^{2}$.")]),
 ]),
 # ------------------------------------------------------------------ p13
 dict(page=13, notes=[
  blue(160, [
    r"$(x+3)$ a factor $\Rightarrow f(-3)=0$",
    r"$-27+9-3a+2b=0$",
    r"$2b=3a+18$  …(1)",
    r"$g(5)=42$: $125-100-5a-b=42$",
    r"$b=-5a-17$  …(2)",
    r"(2) into (1): $2(-5a-17)=3a+18$",
    r"$-13a=52$",
    r"$\therefore a=-4,\ b=3$"]),
  red(160, [
    ("M1", r"$f(-3)=0$ used"), ("A1", r"$2b=3a+18$"),
    ("M1", r"$g(5)=42$ used"), ("A1", r"$b=-5a-17$"),
    ("A1", r"$a=-4$ and $b=3$"),
    ("Trap", r"$(-3)^{3}=-27$ and $(-3)^{2}=9$; a fractional $a$ is the signal of a slip.")]),
  blue(353, [
    r"$x^{3}-x^{2}-7x+7=0$",
    r"$x^{2}(x-1)-7(x-1)=0$",
    r"$(x-1)\left(x^{2}-7\right)=0$",
    r"$x^{2}=7$",
    r"$\therefore x=1,\ x=\sqrt{7},\ x=-\sqrt{7}$"]),
  red(353, [
    ("M1", r"grouping, or the factor theorem with $x=1$"),
    ("A1", r"$(x-1)\left(x^{2}-7\right)$"),
    ("M1", r"$x^{2}=7$ solved"),
    ("A1", r"$x=1$"), ("A1", r"$x=\pm\sqrt{7}$"),
    ("Trap", r"exact form means $\pm\sqrt{7}$, not $\pm 2.65$.")]),
 ]),
 # ------------------------------------------------------------------ p14
 dict(page=14, notes=[
  blue(250, [
    r"$L=Ad^{\,k}$",
    r"$\lg L=\lg A+k\lg d$",
    r"$\lg L=k\lg d+\lg A$",
    r"Comparing with $Y=mX+c$: plot $\lg L$ (vertical) against $\lg d$ (horizontal).",
    r"The graph is a straight line of gradient $k$ and vertical intercept $\lg A$.",
    r"$\lg d$:  $0.954,\ 1.699,\ 2.301,\ 2.602,\ 2.954$",
    r"$\lg L$:  $0.903,\ 1.176,\ 1.398,\ 1.505,\ 1.633$"]),
  red(250, [
    "Key concept: take logs of both sides to linearise a power law.",
    ("B1", r"$\lg$ taken of both sides: $\lg L=\lg A+k\lg d$"),
    ("B1", r"compares with $Y=mX+c$; gradient $k$, intercept $\lg A$"),
    ("M1", r"both $\lg$ rows computed"),
    ("A1", r"points plotted correctly and a straight line drawn")]),
 ]),
 # ------------------------------------------------------------------ p16
 dict(page=16, notes=[
  blue(78, [
    r"gradient $k=\dfrac{1.633-0.903}{2.954-0.954}=\dfrac{0.730}{2.000}$",
    r"$k\approx 0.365$",
    r"intercept: $\lg A=\lg L-k\lg d$",
    r"$\lg A=0.903-0.365(0.954)=0.555$",
    r"$A=10^{0.555}$",
    r"$\therefore A\approx 3.59,\ k\approx 0.365$"]),
  red(78, [
    "Key concept: read two points off the DRAWN LINE, as far apart as it allows.",
    ("M1", r"gradient from two points on the line"),
    ("A1", r"$k\approx 0.365$"),
    ("M1", r"intercept used to find $\lg A$"),
    ("A1", r"$A\approx 3.59$"),
    ("Note", r"accept $k$ from $0.35$ to $0.38$ and $A$ from $3.3$ to $3.9$."),
    ("Note", r"check: $3.59\times 200^{0.365}\approx 24.8$ against the tabulated $L=25$.")]),
 ]),
 # ------------------------------------------------------------------ p17
 dict(page=17, notes=[
  blue(125, [
    r"$\text{LHS}=\dfrac{\cos^{2}\theta-(1-\sin\theta)^{2}}{(1-\sin\theta)\cos\theta}$",
    r"$(1-\sin\theta)^{2}=1-2\sin\theta+\sin^{2}\theta$",
    r"$\text{numerator}=\cos^{2}\theta-1+2\sin\theta-\sin^{2}\theta$",
    r"using $\cos^{2}\theta=1-\sin^{2}\theta$:",
    r"$\text{numerator}=2\sin\theta-2\sin^{2}\theta=2\sin\theta(1-\sin\theta)$",
    r"$\text{LHS}=\dfrac{2\sin\theta(1-\sin\theta)}{(1-\sin\theta)\cos\theta}=\dfrac{2\sin\theta}{\cos\theta}$",
    r"$\text{LHS}=2\tan\theta=\text{RHS}$"]),
  red(125, [
    "Key concept: one common denominator, then $\\cos^{2}\\theta=1-\\sin^{2}\\theta$.",
    ("M1", r"single fraction $\dfrac{\cos^{2}\theta-(1-\sin\theta)^{2}}{(1-\sin\theta)\cos\theta}$"),
    ("M1", r"$(1-\sin\theta)^{2}$ expanded"),
    ("M1", r"$\cos^{2}\theta$ replaced by $1-\sin^{2}\theta$"),
    ("M1", r"numerator factorised as $2\sin\theta(1-\sin\theta)$"),
    ("A1", r"cancels to $2\tan\theta$"),
    ("Trap", r"combining as $\dfrac{\cos\theta-(1-\sin\theta)}{\cos\theta(1-\sin\theta)}$ — the numerators must be cross-multiplied.")]),
  blue(362, [
    r"by (a): $2\tan\theta=\cot\theta=\dfrac{1}{\tan\theta}$",
    r"$2\tan^{2}\theta=1$",
    r"$\tan\theta=\pm\dfrac{1}{\sqrt{2}}$",
    r"basic angle $\alpha=0.6155$ rad",
    r"$\tan\theta>0$: $\theta=0.6155,\ \pi+0.6155=3.757$",
    r"$\tan\theta<0$: $\theta=\pi-0.6155=2.526,\ 2\pi-0.6155=5.668$",
    r"$\therefore\theta=0.615,\ 2.53,\ 3.76,\ 5.67$ rad"]),
  red(362, [
    ("M1", r"result of (a) used: $2\tan\theta=\cot\theta$"),
    ("M1", r"$\tan^{2}\theta=\dfrac{1}{2}$"),
    ("A1", r"two correct values"),
    ("A1", r"all four values, in radians to $3$ s.f."),
    ("Trap", r"the range $0\le\theta\le 2\pi$ is in radians — degrees score at most 3.")]),
 ]),
 # ------------------------------------------------------------------ p18
 dict(page=18, notes=[
  blue(125, [
    r"by (a) the equation becomes $2\tan\theta=k\left(1+\tan^{2}\theta\right)$",
    r"let $t=\tan\theta$:",
    r"$kt^{2}-2t+k=0$",
    r"no real $t$ needs $\text{discriminant}<0$",
    r"$(-2)^{2}-4(k)(k)<0$",
    r"$4-4k^{2}<0$",
    r"$k^{2}>1$",
    r"$\therefore k<-1$ or $k>1$"]),
  red(125, [
    "Key concept: the identity turns it into a quadratic in $\\tan\\theta$.",
    ("M1", r"$kt^{2}-2t+k=0$ with $t=\tan\theta$"),
    ("M1", r"$\text{discriminant}<0$ used"),
    ("A1", r"$k<-1$ or $k>1$, i.e. $k^{2}>1$"),
    ("Note", r"$k=0$ gives $t=0$, which does have solutions — consistent, since $0^{2}<1$.")]),
 ]),
]
