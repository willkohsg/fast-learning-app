# -*- coding: utf-8 -*-
"""Verify every numerical answer in the Sec 3 EOY A-Math P1 marking scheme."""
import sympy as sp

x, n, k, m, t, th, a, b, c, p = sp.symbols('x n k m t theta a b c p', real=True)
ok = lambda lbl, cond: print(("  PASS  " if cond else "  FAIL  ") + lbl) or bool(cond)
fails = []
def chk(lbl, cond):
    print(("  PASS  " if cond else "  FAIL  ") + lbl)
    if not cond: fails.append(lbl)

print("Q1  surds - triangle")
DF = sp.symbols('DF', positive=True)
sol = sp.solve(sp.Rational(1,4)*(7*sp.sqrt(3)+9)
               - sp.Rational(1,2)*(sp.sqrt(3)+2)*DF*sp.sin(sp.pi/3), DF)
chk("DF = 5 - sqrt3", sp.simplify(sol[0] - (5-sp.sqrt(3))) == 0)

print("Q2  surds")
chk("7/(3-sqrt2) = 3+sqrt2", sp.simplify(7/(3-sp.sqrt(2)) - (3+sp.sqrt(2))) == 0)
chk("x = -2+3sqrt3", sp.simplify(sp.solve((2+sp.sqrt(3))*x - (5+4*sp.sqrt(3)), x)[0]
                                 - (-2+3*sp.sqrt(3))) == 0)

print("Q3  compound angle (both in quadrant 3)")
sinA, cosA = -1/sp.sqrt(5), -2/sp.sqrt(5)
sinB, cosB = sp.Rational(-3,5), sp.Rational(-4,5)
chk("sin^2+cos^2 = 1 for A", sp.simplify(sinA**2+cosA**2) == 1)
chk("tanB = 3/4", sp.simplify(sinB/cosB - sp.Rational(3,4)) == 0)
chk("p = 11/25", sp.simplify((cosA*cosB+sinA*sinB) - sp.Rational(11,25)*sp.sqrt(5)) == 0)

print("Q4  completing the square / discriminant")
chk("-2(x+3)^2+23", sp.expand(-2*(x+3)**2+23) == sp.expand(-2*x**2-12*x+5))
chk("no two distinct roots <=> k>=23",
    sp.solve_univariate_inequality(sp.Poly(-2*x**2-12*x+5-k, x).discriminant() <= 0,
                                   k, relational=False) == sp.Interval(23, sp.oo))

print("Q5  line meets curve")
disc = sp.Poly(n*x**2 + 2*x + (1-n), x).discriminant()
chk("discriminant = 4(n^2-n+1)", sp.simplify(disc - 4*(n**2-n+1)) == 0)
chk("n^2-n+1 > 0 for all real n", sp.Poly(n**2-n+1, n).discriminant() < 0)

print("Q6  logarithms")
r = sp.solve(sp.Eq(sp.log(x-2,2) + 2*sp.log(x-3,4), sp.Rational(1,2)*sp.log(9,3)), x)
chk("x = 4 only (x>3)", [s for s in r if s.is_real and s > 3] == [4])

print("Q7  partial fractions")
expr = (3*x**2+3*x+10)/((x+1)*(x**2+4))
chk("= 2/(x+1) + (x+2)/(x^2+4)",
    sp.simplify(expr - (2/(x+1) + (x+2)/(x**2+4))) == 0)

print("Q8  coordinate geometry")
A, B, C = sp.Matrix([2,3]), sp.Matrix([-1,-1]), sp.Matrix([3,1])
mAC = (A[1]-C[1])/(A[0]-C[0]); mBC = (B[1]-C[1])/(B[0]-C[0])
chk("mAC * mBC = -1", sp.simplify(mAC*mBC) == -1)
D = A + C - B                       # diagonals bisect: midAC = midBD
chk("D = (6,5)", list(D) == [6,5])
area = sp.Abs((C-A).row_join(B-A).det())
chk("area = 10", sp.simplify(area) == 10)

print("Q9  trig graph")
s = sp.solve([sp.Eq(a+b,4), sp.Eq(-a+b,-10)], [a,b], dict=True)[0]
chk("a=7, b=-3", s[a] == 7 and s[b] == -3)
chk("period = pi", sp.simplify(2*sp.pi/2 - sp.pi) == 0)

print("Q10 exponential growth")
kv = sp.log(sp.Rational(10,9))
chk("k = 0.10536 (5sf)", round(float(kv), 5) == 0.10536)
tv = sp.log(3)/kv
chk("t = 10.43 -> during 2025", sp.floor(tv) == 10 and 10 < tv < 11)

print("Q11 binomial")
r_ = sp.symbols('r', integer=True, nonnegative=True)
term = sp.binomial(12,r_)*(2*x)**(12-r_)*(-1/(4*x**2))**r_
chk("r = 5 gives power 0", sp.simplify(sp.expand(3*x**3*term.subs(r_,5))).is_number)
chk("term independent = -297",
    sp.simplify(3*x**3*term.subs(r_,5) + 297) == 0)
c7 = sp.binomial(15,7)*2**8*m**7
c9 = sp.binomial(15,9)*2**6*m**9
chk("m = +/-3", sorted(sp.solve(sp.Eq(c7/c9, sp.Rational(4,7)), m)) == [-3, 3])

print("Q12 polynomials")
f = x**3 + x**2 + a*x + 2*b
g = x**3 - 4*x**2 - a*x - b
s = sp.solve([f.subs(x,-3), sp.Eq(g.subs(x,5), 42)], [a,b], dict=True)[0]
chk("a=-4, b=3", s[a] == -4 and s[b] == 3)
chk("roots 1, +/-sqrt7",
    set(sp.solve(x**3-x**2-7*x+7, x)) == {1, sp.sqrt(7), -sp.sqrt(7)})

print("Q13 linear law")
ds = [9,50,200,400,900]; Ls = [8,15,25,32,43]
X = [sp.log(d,10) for d in ds]; Y = [sp.log(L,10) for L in Ls]
grad = (Y[-1]-Y[0])/(X[-1]-X[0])
chk("k ~ 0.365", abs(float(grad) - 0.365) < 0.005)
lgA = Y[0] - grad*X[0]
chk("A ~ 3.59", abs(float(10**lgA) - 3.59) < 0.05)
chk("model reproduces L(200)=25",
    abs(float(10**lgA * 200**float(grad)) - 25) < 0.6)

print("Q14 identities")
lhs = sp.cos(th)/(1-sp.sin(th)) - (1-sp.sin(th))/sp.cos(th)
chk("identity = 2 tan", sp.simplify(lhs - 2*sp.tan(th)) == 0)
sols = sp.solve(sp.Eq(2*sp.tan(th), 1/sp.tan(th)), th)
want = [0.6155, 2.5261, 3.7571, 5.6677]
got = sorted(float(v) for s_ in sols
             for v in [s_, s_+sp.pi, s_+2*sp.pi] if 0 <= float(v) <= float(2*sp.pi))
chk("four roots in [0,2pi]", len(got) == 4 and
    all(abs(gv-wv) < 1e-3 for gv, wv in zip(got, want)))
T = sp.symbols('T', real=True)
chk("no solutions <=> |k|>1",
    sp.solve_univariate_inequality(sp.Poly(k*T**2-2*T+k, T).discriminant() < 0,
                                   k, relational=False)
    == sp.Union(sp.Interval.open(-sp.oo,-1), sp.Interval.open(1, sp.oo)))

print()
print("FAILURES:", fails if fails else "none")
assert not fails, fails
