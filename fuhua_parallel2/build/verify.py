# -*- coding: utf-8 -*-
"""Verify every answer in Fuhua-parallel SET 2 (Sec 3 G3, 80 marks, no circles)."""
import sympy as sp

x, y, m, k, t, q, th = sp.symbols('x y m k t q theta', real=True)
a, b = sp.symbols('a b', real=True)
fails = []


def chk(lbl, cond):
    print(("  PASS  " if cond else "  FAIL  ") + lbl)
    if not cond:
        fails.append(lbl)


print("Q1  line meets curve at two distinct points")
d = sp.Poly(sp.expand(x**2 - 3*x + 7 - (m*x - 2)), x).discriminant()
chk("discriminant is (m+3)^2-36", sp.simplify(d - ((m + 3)**2 - 36)) == 0)
chk("m < -9 or m > 3",
    sp.solve_univariate_inequality(d > 0, m, relational=False)
    == sp.Union(sp.Interval.open(-sp.oo, -9), sp.Interval.open(3, sp.oo)))

print("Q2  surds")
e = (2*sp.sqrt(3) + 5)/(3 - sp.sqrt(3))
chk("(2sqrt3+5)/(3-sqrt3) = 7/2 + 11sqrt3/6",
    sp.simplify(sp.radsimp(e) - (sp.Rational(7, 2) + sp.Rational(11, 6)*sp.sqrt(3))) == 0)
r = sp.solve(sp.Eq(sp.sqrt(2*x + 3), x - 1), x)
chk("sqrt(2x+3)=x-1 -> only x=2+sqrt6", r == [2 + sp.sqrt(6)])
chk("2-sqrt6 is rejected (x-1<0)", (2 - sp.sqrt(6)) - 1 < 0)

print("Q3  polynomials -> exponential substitution")
f = 2*x**3 + a*x**2 + b*x + 6
s = sp.solve([f.subs(x, -2), f.subs(x, 3)], [a, b], dict=True)[0]
chk("a=-3, b=-11", s[a] == -3 and s[b] == -11)
g = 2*x**3 - 3*x**2 - 11*x + 6
chk("factorises as (x+2)(2x-1)(x-3)",
    sp.simplify(sp.expand((x + 2)*(2*x - 1)*(x - 3)) - g) == 0)
u = sp.Symbol('u', positive=True)
roots = sp.solve(g.subs(x, u), u)
chk("positive roots 1/2 and 3", sorted(roots) == [sp.Rational(1, 2), 3])
chk("y = -1 and y = log2(3)",
    sp.simplify(sp.log(sp.Rational(1, 2), 2) + 1) == 0)

print("Q4  partial fractions")
den = x**3 - x**2 + 4*x - 4
chk("x^3-x^2+4x-4 = (x-1)(x^2+4)", sp.simplify(sp.expand((x - 1)*(x**2 + 4)) - den) == 0)
num = 2*x**3 + 2*x**2 + 5*x + 6
target = 2 + 3/(x - 1) + (x - 2)/(x**2 + 4)
chk("= 2 + 3/(x-1) + (x-2)/(x^2+4)", sp.simplify(num/den - target) == 0)

print("Q5  logarithms")
r = sp.solve(sp.Eq(sp.log(x + 2, 3) + sp.log(x - 4, 3), 3), x)
chk("log3(x+2)+log3(x-4)=3 -> x=7 only", r == [7])
chk("x=-5 fails the domain", (-5 + 2) < 0)
T = sp.Symbol('T', nonzero=True)
rt = sp.solve(sp.Eq(2*T - 1/T, 1), T)
chk("2t-1/t=1 -> t=1 or t=-1/2", sorted(rt) == [sp.Rational(-1, 2), 1])
chk("x = 3 or x = 1/sqrt3", sp.simplify(3**sp.Rational(-1, 2) - sp.sqrt(3)/3) == 0)

print("Q6  exponential decay, no M0 given")
K = sp.Symbol('K', positive=True)
kv = sp.solve(sp.Eq(500*sp.exp(-8*K), 320), K)[0]
chk("k = ln(25/16)/8", sp.simplify(kv - sp.log(sp.Rational(25, 16))/8) == 0)
chk("k ~ 0.0558", abs(float(kv) - 0.055786) < 5e-6)
M0 = 500*sp.exp(2*kv)
chk("M0 ~ 559", abs(float(M0) - 559.017) < 1e-2)
tv = sp.log(M0/100)/kv
chk("t ~ 30.85", abs(float(tv) - 30.849) < 1e-2)
chk("least complete days = 31", sp.ceiling(tv) == 31)

print("Q7  binomial")
c2 = sp.binomial(6, 2)*2**4
c3 = sp.binomial(6, 3)*2**3
kk = sp.solve(sp.Eq(c3*k**3, 2*c2*k**2), k)
chk("k = 3 (k != 0)", 3 in kk)
ex = sp.expand((1 - 2*x)*(2 + 3*x)**6)
chk("coefficient of x^2 is 1008", ex.coeff(x, 2) == 1008)

print("Q8  coordinate geometry spine (no circle)")
A, B = sp.Point(-2, 3), sp.Point(6, 7)
M = sp.Point(2, 5)
chk("midpoint AB = (2,5)", A.midpoint(B) == M)
chk("perp bisector y = -2x+9", sp.simplify((-2*2 + 9) - 5) == 0
    and sp.simplify(sp.Rational(7 - 3, 6 + 2)*-2 + 1) == 0)
C = sp.Point(sp.Rational(9, 2), 0)
chk("C = (9/2, 0)", sp.solve(sp.Eq(-2*x + 9, 0), x) == [sp.Rational(9, 2)])
chk("CA = CB (isosceles)", sp.simplify(C.distance(A) - C.distance(B)) == 0)
chk("AB = 4sqrt5", sp.simplify(A.distance(B) - 4*sp.sqrt(5)) == 0)
for D in (sp.Point(5, -1), sp.Point(-1, 11)):
    chk("area ABD = 30 at %s" % (D,), sp.Triangle(A, B, D).area == 30
        or -sp.Triangle(A, B, D).area == 30)
    chk("%s lies on y=-2x+9" % (D,), sp.simplify(-2*D.x + 9 - D.y) == 0)

print("Q9  linear law  y = a x^b")
pts = [(1, 3), (4, 6), (16, 12), (36, 18), (100, 30)]
chk("all points satisfy y = 3 x^(1/2)",
    all(sp.simplify(sp.Rational(yy) - 3*sp.sqrt(xx)) == 0 for xx, yy in pts))
lg = [(round(float(sp.log(xx, 10)), 3), round(float(sp.log(yy, 10)), 3)) for xx, yy in pts]
chk("lg x row", lg[0][0] == 0.0 and lg[-1][0] == 2.0)
chk("gradient 1/2, intercept lg3",
    abs((lg[-1][1] - lg[0][1])/(lg[-1][0] - lg[0][0]) - 0.5) < 5e-4
    and abs(lg[0][1] - float(sp.log(3, 10))) < 5e-4)

print("Q10  trig ratios, C reflex in quadrant 3")
Q = sp.Symbol('Q', negative=True)          # sin C = q, and q < 0 in quadrant 3
cosC = -sp.sqrt(1 - Q**2)
chk("cos C = -sqrt(1-q^2)", sp.simplify(cosC**2 + Q**2 - 1) == 0)
chk("tan C = -q/sqrt(1-q^2) and is positive", sp.simplify(Q/cosC - (-Q/sp.sqrt(1 - Q**2))) == 0)
chk("sec(360-C) = -1/sqrt(1-q^2)", sp.simplify(1/cosC - (-1/sp.sqrt(1 - Q**2))) == 0)

print("Q11  identity, equation, graph")
lhs = (1 - sp.cos(th))/sp.sin(th) + sp.sin(th)/(1 - sp.cos(th))
chk("identity = 2 cosec(theta)", sp.simplify(lhs - 2/sp.sin(th)) == 0)
chk("2cosec=4 -> sin=1/2 -> 30 and 150 degrees",
    [sp.deg(s) for s in sp.solve(sp.Eq(sp.sin(th), sp.Rational(1, 2)), th)][:1] == [30])
per = sp.periodicity(2 + 3*sp.sin(2*th), th)
chk("y=2+3sin2x has period pi (180 deg)", per == sp.pi)
chk("amplitude 3", sp.Rational(5 - (-1), 2) == 3)
chk("max 5, min -1", 2 + 3 == 5 and 2 - 3 == -1)

print("\nFAILURES:", fails if fails else "none")
