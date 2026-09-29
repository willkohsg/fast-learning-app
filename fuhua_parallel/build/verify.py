# -*- coding: utf-8 -*-
"""Verify every answer in the Fuhua-parallel Sec 3 EOY A-Math paper (80 marks)."""
import sympy as sp
x, y, k, n, t, u, A, a, b, p = sp.symbols('x y k n t u A a b p', real=True)
fails = []
def chk(lbl, cond):
    print(("  PASS  " if cond else "  FAIL  ") + lbl)
    if not cond: fails.append(lbl)

print("Q1  curve above line -> discriminant")
# x^2+(k-2)x+4 > 2x-k for all x
q = sp.expand(x**2 + (k-2)*x + 4 - (2*x - k))
chk("reduces to x^2+(k-4)x+(4+k)", sp.simplify(q - (x**2+(k-4)*x+(4+k))) == 0)
sol = sp.solve_univariate_inequality(sp.Poly(q, x).discriminant() < 0, k, relational=False)
chk("0 < k < 12", sol == sp.Interval.open(0, 12))

print("Q2  surds")
e = (5 - 2*sp.sqrt(3))/(2*sp.sqrt(3) - 3)
chk("(5-2sqrt3)/(2sqrt3-3) = 1 + 4sqrt3/3",
    sp.simplify(sp.radsimp(e) - (1 + sp.Rational(4,3)*sp.sqrt(3))) == 0)
r = sp.solve(sp.Eq(sp.sqrt(3*x+7) - sp.sqrt(x+1), 2), x)
chk("sqrt(3x+7)-sqrt(x+1)=2 has BOTH x=-1 and x=3", sorted(r) == [-1, 3])

print("Q3  polynomials")
f = 2*x**3 + a*x**2 + b*x - 6
s = sp.solve([f.subs(x,2), sp.Eq(f.subs(x,-1), -12)], [a,b], dict=True)[0]
chk("a=-3, b=1", s[a] == -3 and s[b] == 1)
F = f.subs(s)
chk("f(x) = (x-2)(2x^2+x+3)", sp.simplify(F - (x-2)*(2*x**2+x+3)) == 0)
chk("2x^2+x+3 has no real root", sp.Poly(2*x**2+x+3, x).discriminant() < 0)
chk("x=2 is the only real root",
    [r_ for r_ in sp.solve(F, x) if r_.is_real] == [2])

print("Q4  partial fractions (improper, repeated + irreducible)")
expr = (2*x**4 + 2*x**3 + 6*x**2 + 4*x + 4)/(x**2*(x**2+4))
target = 2 + 1/x + 1/x**2 + (x-3)/(x**2+4)
chk("= 2 + 1/x + 1/x^2 + (x-3)/(x^2+4)", sp.simplify(expr - target) == 0)
chk("numerator degree 4 = denominator degree 4 (improper)",
    sp.degree(sp.numer(sp.together(expr)), x) == sp.degree(sp.denom(sp.together(expr)), x))

print("Q5  indices and logarithms")
r = sp.solve(sp.Eq(3*(3**x)**2 - 10*3**x + 3, 0), x)
chk("3^(2x+1)-10*3^x+3=0 -> x=-1,1", sorted(sp.nsimplify(v) for v in r) == [-1, 1])
sx, sy = sp.symbols('sx sy', positive=True)
s = sp.solve([sp.Eq(sp.log(sx,2)+sp.log(sy,2), 5),
              sp.Eq(sp.log(sx,4)-sp.log(sy,4), sp.Rational(1,2))], [sx,sy], dict=True)[0]
chk("x=8, y=4", s[sx] == 8 and s[sy] == 4)

print("Q6  exponential model")
kv = sp.log(sp.Rational(3,2))
M0 = 8/sp.exp(kv)
chk("k = ln(3/2)", sp.simplify(sp.exp(3*kv) - sp.Rational(27,8)) == 0)
chk("M0 = 16/3", sp.simplify(M0 - sp.Rational(16,3)) == 0)
chk("M(4) = 27", sp.simplify(M0*sp.exp(4*kv) - 27) == 0)
tv = sp.log(sp.Rational(200*3,16))/kv
chk("t = 8.94 -> least complete hour 9", sp.ceiling(tv) == 9 and 8 < tv < 9)

print("Q7  binomial")
# coeff x = 2n ; coeff x^2 = 4*C(n,2) = 2n(n-1);  difference 96
sols = sp.solve(sp.Eq(2*n*(n-1), 2*n + 96), n)
chk("n = 8", [v for v in sols if v.is_integer and v > 0] == [8])
chk("coeff x=16, coeff x^2=112, difference 96",
    sp.expand((1+2*x)**8).coeff(x,1) == 16 and
    sp.expand((1+2*x)**8).coeff(x,2) == 112 and 112-16 == 96)
c5 = sp.expand((2-x)*(1+2*x)**8).coeff(x,5)
chk("coeff x^5 in (2-x)(1+2x)^8 = 2464", c5 == 2464)

print("Q8  circle and tangent")
Ap, Bp = sp.Matrix([-1,2]), sp.Matrix([5,4])
C = (Ap+Bp)/2
r2 = ((Bp-Ap).dot(Bp-Ap))/4
chk("centre (2,3), r^2 = 10", list(C) == [2,3] and r2 == 10)
m_rad = sp.Rational(2-3, -1-2)
m_tan = -1/m_rad
Pp = sp.Matrix([0, 2 + m_tan*(0-(-1))])
chk("tangent gradient -3 and P(0,-1)", m_tan == -3 and list(Pp) == [0,-1])
d2 = (Pp-C).dot(Pp-C)
chk("P outside: d^2 = 20 > 10", d2 == 20)
chk("tangent length = sqrt(10)", sp.sqrt(d2 - r2) == sp.sqrt(10))
area = sp.Rational(1,2)*sp.Abs((Ap-Pp).row_join(Bp-Pp).det())
chk("area PAB = 10", area == 10)

print("Q9  linear law  y = x/(ax+b)")
av, bv = 2, 3
xs = [1, 2, 4, 5, 10]
ys = [sp.Rational(v, av*v+bv) for v in xs]
chk("1/y = a + b(1/x) exactly for every data point",
    all(sp.simplify(1/ys[i] - (av + bv*sp.Rational(1, xs[i]))) == 0 for i in range(5)))
chk("y values are 1/5, 2/7, 4/11, 5/13, 10/23",
    ys == [sp.Rational(1,5), sp.Rational(2,7), sp.Rational(4,11),
           sp.Rational(5,13), sp.Rational(10,23)])

print("Q10 trig ratios, A obtuse, cos A = -p")
pp = sp.Symbol('pp', positive=True)
Aval = sp.acos(-pp)
chk("sin A = sqrt(1-p^2)", sp.simplify(sp.sin(Aval) - sp.sqrt(1-pp**2)) == 0)
chk("tan(180-A) = sqrt(1-p^2)/p",
    sp.simplify(sp.tan(sp.pi - Aval) - sp.sqrt(1-pp**2)/pp) == 0)
chk("cosec(90+A) = -1/p",
    sp.simplify(1/sp.sin(sp.pi/2 + Aval) - (-1/pp)) == 0)

print("Q11 trig graph  f(x) = a - b cos(x/2)")
s = sp.solve([sp.Eq(a+b,7), sp.Eq(a-b,-1)], [a,b], dict=True)[0]
chk("a=3, b=4", s[a] == 3 and s[b] == 4)
chk("period 4pi", sp.simplify(2*sp.pi/sp.Rational(1,2) - 4*sp.pi) == 0)
f11 = 3 - 4*sp.cos(x/2)
chk("f(0) = -1 (minimum)", sp.simplify(f11.subs(x,0) + 1) == 0)
chk("f(2pi) = 7 (maximum)", sp.simplify(f11.subs(x,2*sp.pi) - 7) == 0)
roots = [v for v in sp.solveset(sp.Eq(f11, 5), x, sp.Interval(0, 4*sp.pi))]
chk("f(x)=5 at 4pi/3 and 8pi/3",
    sorted(roots) == [sp.Rational(4,3)*sp.pi, sp.Rational(8,3)*sp.pi])

MARKS = [("1",4),("2",6),("3",7),("4",8),("5",7),("6",7),
         ("7",7),("8",12),("9",6),("10",6),("11",10)]
tot = sum(m for _, m in MARKS)
print()
print("paper total:", tot, "marks over 2 hours  (%.2f min/mark)" % (120/tot))
chk("total is 80", tot == 80)
print()
print("FAILURES:", fails if fails else "none")
assert not fails, fails
