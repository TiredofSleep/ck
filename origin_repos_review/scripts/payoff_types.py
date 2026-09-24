import sympy as sp
s, pen = sp.symbols('s pen', nonnegative=True)
m = 1 + 2*s
R = sp.Rational(15,100)*(1-s) - pen      # mutual cooperation (pen = 0.05 polarization penalty when both isolated)
T = sp.Rational(1,10)*m                  # defect against cooperator
P = -sp.Rational(1,10)*m                 # mutual defection
S = -sp.Rational(2,10)*m                 # cooperate against defector
print("T = R  at s =", sp.solve(sp.Eq(T, R.subs(pen, 0)), s), " (no polarization penalty)")
print("T = R  at s =", sp.solve(sp.Eq(T, R.subs(pen, sp.Rational(5,100))), s), " (penalty 0.05, both isolated)")
print("P > S always:", sp.simplify(P - S), "> 0")
print("R > P always for s<1:", sp.simplify(R.subs(pen,0) - P))
for sv in [0, sp.Rational(1,10), sp.Rational(1,7), sp.Rational(2,10), sp.Rational(4,10), sp.Rational(8,10)]:
    vals = {k: float(v.subs({s: sv, pen: 0})) for k, v in dict(T=T, R=R, P=P, S=S).items()}
    order = ''.join(sorted(vals, key=lambda k: -vals[k]))
    kind = {'TRPS': "Prisoner's Dilemma", 'RTPS': 'Stag Hunt', 'RTSP': 'Harmony'}.get(order, order)
    print(f"  s={str(sv):5s}: " + ', '.join(f'{k}={v:+.3f}' for k, v in vals.items()) + f"  order {order} -> {kind}")
