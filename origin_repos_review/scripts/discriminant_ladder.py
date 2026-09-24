"""Smallest concrete test for the re-lit 'quadratic core':
claim: for x -> a x^2 + b x + c, the attractor of the critical orbit depends only on D' = (b-1)^2 - 4ac
(equivalently the logistic parameter r = 1 + sqrt(D')), with bifurcations at D' = 0 (fold), 4 (flip), 6 (2nd flip),
~6.6046 (Feigenbaum accumulation), 8 (period-3 fold, r = 1 + 2*sqrt(2)), 9 (end of bounded dynamics, r = 4).
Also: the ghost/bottleneck just past the fold: escape time ~ pi / sqrt(C - 1/4)."""
import math, random

def period_of_critical_orbit(a, b, c, n_trans=100000, pmax=64, tol=1e-7):
    x = -b / (2 * a)          # critical point
    for _ in range(n_trans):
        x = a * x * x + b * x + c
        if not math.isfinite(x) or abs(x) > 1e8:
            return 'escape'
    ref = x
    xs = [x]
    for _ in range(pmax):
        x = a * x * x + b * x + c
        xs.append(x)
    scale = max(1.0, abs(ref))
    for p in range(1, pmax + 1):
        if abs(xs[p] - ref) < tol * scale:
            return p
    return 'aperiodic'

def lyap(a, b, c, n_trans=20000, n=50000):
    x = -b / (2 * a) + 1e-9
    for _ in range(n_trans):
        x = a * x * x + b * x + c
    s = 0.0
    for _ in range(n):
        d = abs(2 * a * x + b)
        s += math.log(d) if d > 0 else -50
        x = a * x * x + b * x + c
    return s / n

rng = random.Random(7)
targets = [-0.5, 2.0, 3.9, 4.1, 5.0, 5.9, 6.1, 6.5, 7.0, 7.9, 8.01, 8.5, 8.99, 9.2]
print("D'      r=1+sqrt(D')  canonical(a=1,b=1)  |  30 random (a,b) with c solved for the same D'")
for Dp in targets:
    r = 1 + math.sqrt(Dp) if Dp >= 0 else float('nan')
    # canonical representative: a=1, b=1 -> D' = -4c
    can = period_of_critical_orbit(1.0, 1.0, -Dp / 4)
    res = {}
    lams = []
    for _ in range(30):
        a = rng.choice([-1, 1]) * rng.uniform(0.2, 3.0)
        b = rng.uniform(-3, 3)
        c = ((b - 1) ** 2 - Dp) / (4 * a)
        p = period_of_critical_orbit(a, b, c)
        res[str(p)] = res.get(str(p), 0) + 1
        if p == 'aperiodic':
            lams.append(lyap(a, b, c))
    extra = f"  lyap(aperiodic) min={min(lams):.3f}" if lams else ""
    print(f"{Dp:5.2f}   r={r:6.4f}      {str(can):10s}          |  {res}{extra}")

print("\nGhost / bottleneck past the fold (C slightly above 1/4): escape iteration vs pi/sqrt(C-1/4)")
for eps in (1e-2, 1e-3, 1e-4, 1e-5):
    C = 0.25 + eps
    y, n = 0.0, 0
    while abs(y) < 10 and n < 10**7:
        y = y * y + C
        n += 1
    print(f"  C-1/4={eps:.0e}: escape after {n:6d} steps; pi/sqrt(eps) = {math.pi/math.sqrt(eps):8.1f}")
