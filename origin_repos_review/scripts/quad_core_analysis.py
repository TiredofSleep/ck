"""Python port of the Crystal Bug 'quadratic core' (crystal_bug_v1_matrix.jsx / test_engine_v2.js)
and tests of whether its 7 'bands' are features of the dynamics or artifacts of thresholds.
Read-only analysis; writes nothing outside this scratch folder."""
import math, random, collections
import numpy as np

SIG, SIGS, TS = 0.991, 0.009, 0.714
COLS, ROWS = 18, 14
NC = COLS * ROWS
BANDS = ['VOID', 'QUANTUM', 'ATOMIC', 'MOLECULR', 'CELLULAR', 'ORGANIC', 'CRYSTAL']


def classify(a, b, c, x0=0.5, N=28, esc=80.0, eps=5e-4):
    """Exact port of classify() in the JSX / test harness."""
    orb = [x0]
    for i in range(N):
        x = orb[-1]
        xn = a * x * x + b * x + c
        orb.append(xn)
        if not math.isfinite(xn) or abs(xn) > esc:
            if i < 3:
                return 0, orb
            if i < 9:
                return 1, orb
            return 2, orb
    t = orb[-8:]
    if abs(t[7] - t[6]) < eps:
        ci = -1
        for i in range(len(orb)):
            if i > 2 and abs(orb[i] - orb[i - 1]) < eps * 5:
                ci = i
                break
        return (6 if 0 < ci < 10 else 5), orb
    if abs(t[7] - t[5]) < eps * 3 and abs(t[6] - t[4]) < eps * 3:
        return 4, orb
    for p in range(3, 7):
        if len(orb) > p + 2 and abs(t[7] - t[7 - p]) < eps * 8:
            return 4, orb
    return 3, orb


def mkcell(col, row):
    u, v = col / (COLS - 1), row / (ROWS - 1)
    cu, cv = u - 0.5, v - 0.5
    r = math.sqrt(cu * cu + cv * cv)
    th = math.atan2(cv, cu)
    a = 0.8 * math.cos(r * 3.5) * (1 + 0.5 * math.sin(v * 7 * math.pi))
    b = (cu * 3.5 + cv * 2.0) * (1 + 0.3 * math.cos(u * 5 * math.pi))
    c = 0.5 * math.exp(-r * 2) + 0.15 * math.sin(th * 4 + r * 3) + 0.1
    return dict(col=col, row=row, a0=a, b0=b, c0=c, a=a, b=b, c=c)


def fp_stable(a, b, c):
    A, B, C = a, b - 1, c
    if abs(A) < 1e-12:
        return (B != 0) and abs(b) < 1
    d = B * B - 4 * A * C
    if d < 0:
        return False
    s = math.sqrt(d)
    x1, x2 = (-B + s) / (2 * A), (-B - s) / (2 * A)
    l = min(abs(2 * a * x1 + b), abs(2 * a * x2 + b))
    return l < 1


def lattice():
    return [mkcell(c, r) for r in range(ROWS) for c in range(COLS)]


def conj_C(a, b, c):
    """x -> a x^2 + b x + c is affinely conjugate (y = a x + b/2) to y -> y^2 + C."""
    return a * c + b / 2 - b * b / 4


def lyapunov(a, b, c, x0=0.5, n_trans=2000, n=20000):
    x = x0
    for _ in range(n_trans):
        x = a * x * x + b * x + c
        if abs(x) > 1e6:
            return float('nan')
    s = 0.0
    for _ in range(n):
        d = abs(2 * a * x + b)
        s += math.log(d) if d > 0 else -50
        x = a * x * x + b * x + c
        if abs(x) > 1e6:
            return float('nan')
    return s / n


def attractor_period(a, b, c, x0=0.5, n_trans=20000, tol=1e-9, pmax=64):
    x = x0
    for _ in range(n_trans):
        x = a * x * x + b * x + c
        if abs(x) > 1e6:
            return 'esc'
    orb = [x]
    for _ in range(pmax):
        x = a * x * x + b * x + c
        orb.append(x)
    for p in range(1, pmax + 1):
        if abs(orb[p] - orb[0]) < tol * max(1, abs(orb[0])):
            return p
    return 'aperiodic/slow'


def section(t):
    print('\n' + '=' * 78 + '\n' + t + '\n' + '=' * 78)


# ---------------------------------------------------------------- 1. reproduce Test 1
section('1. Reproduce committed Test 1 (initial lattice) with the Python port')
cells = lattice()
bands = [classify(c['a'], c['b'], c['c'])[0] for c in cells]
cnt = collections.Counter(bands)
for i, n in enumerate(BANDS):
    print(f'  {n:9s} {cnt[i]:4d}')
D = [c['b'] ** 2 - 4 * c['a'] * c['c'] for c in cells]
print('  click (|D|<0.15):', sum(abs(d) < 0.15 for d in D), ' stable FP:', sum(fp_stable(c['a'], c['b'], c['c']) for c in cells),
      f' D range [{min(D):.3f}, {max(D):.3f}]')
print('  committed: VOID 0, QUAN 58, ATOM 26, MOLE 34, CELL 19, ORGA 28, CRYS 87; click 24; stable 137; [-2.633, 13.016]')

# ---------------------------------------------------------------- 2. which discriminant predicts the bands?
section('2. Does the "binding kernel" D = b^2-4ac predict escape vs bounded? vs fixed-point discriminant D\' = (b-1)^2-4ac = 1-4C')
tab = collections.Counter()
tab2 = collections.Counter()
for c, bd in zip(cells, bands):
    d = c['b'] ** 2 - 4 * c['a'] * c['c']
    dp = (c['b'] - 1) ** 2 - 4 * c['a'] * c['c']
    fam = 'escape' if bd <= 2 else 'bounded'
    tab[('D>0' if d > 0 else 'D<=0', fam)] += 1
    tab2[("D'>=0" if dp >= 0 else "D'<0", fam)] += 1
print('  code kernel D   :', dict(tab))
print("  fixed-point D'  :", dict(tab2))
print("  theory: D'<0 means O(x)-x never changes sign -> no real fixed point -> every real orbit escapes.")

# ---------------------------------------------------------------- 3. conjugacy: bands vs the single invariant C
section('3. All quadratics are one: C = ac + b/2 - b^2/4 (y = a x + b/2 gives y -> y^2 + C). Bands of bounded cells vs C-interval')
known = [(0.25, 9, 'C>1/4: no real fixed pt, all escape'),
         (-0.75, 0.25, 'fixed-point cardioid (-3/4,1/4)'),
         (-1.25, -0.75, 'period-2 (-5/4,-3/4)'),
         (-1.3680989, -1.25, 'period-4'),
         (-1.4011552, -1.3680989, 'period 8,16,.. cascade'),
         (-2.0, -1.4011552, 'chaotic region + windows (period-3 at ~-1.75)'),
         (-99, -2.0, 'C<-2: Cantor Julia set, a.e. escape')]
bytab = collections.defaultdict(collections.Counter)
for c, bd in zip(cells, bands):
    C = conj_C(c['a'], c['b'], c['c'])
    for lo, hi, name in known:
        if (lo < C <= hi) if lo != 0.25 else (C > 0.25):
            bytab[name][BANDS[bd]] += 1
            break
for lo, hi, name in known:
    print(f'  {name:48s}', dict(bytab[name]))

# ---------------------------------------------------------------- 4. is MOLECULR 'chaotic'? Lyapunov + true period
section('4. Band 3 "MOLECULR: bounded chaotic" and band 4 "periodic": check against Lyapunov exponent and true attractor period')
for target in (3, 4, 5, 6):
    lam, per = [], collections.Counter()
    for c, bd in zip(cells, bands):
        if bd != target:
            continue
        L = lyapunov(c['a'], c['b'], c['c'])
        lam.append(L)
        per[str(attractor_period(c['a'], c['b'], c['c']))] += 1
    lam = np.array([x for x in lam if not math.isnan(x)])
    print(f'  band {target} {BANDS[target]:9s} n={len(lam):3d}  lyap>0: {int((lam > 1e-3).sum()):3d}   lyap<0: {int((lam < -1e-3).sum()):3d}   '
          f'|lyap|<=1e-3: {int((abs(lam) <= 1e-3).sum()):3d}   true periods: {dict(per)}')

# ---------------------------------------------------------------- 5. sensitivity of band populations to iteration count / tolerance
section('5. Band populations vs iteration budget N and tolerance eps (committed: N=28, eps=5e-4)')
for N in (28, 60, 200, 1000):
    for eps in (5e-4, 1e-6):
        bb = [classify(c['a'], c['b'], c['c'], N=N, eps=eps)[0] for c in cells]
        cc = collections.Counter(bb)
        print(f'  N={N:5d} eps={eps:.0e}: ' + ' '.join(f'{BANDS[i][:4]}={cc[i]:3d}' for i in range(7)))

# ---------------------------------------------------------------- 6. canonical line: where the bands fall on y -> y^2 + C
section('6. Canonical family y -> y^2 + C, critical seed y0=0, committed thresholds: band intervals along C')
Cs = np.round(np.arange(-2.2, 0.4001, 0.0005), 6)
prev, start = None, None
runs = []
for C in Cs:
    bd = classify(1.0, 0.0, float(C), x0=0.0)[0]
    if bd != prev:
        if prev is not None:
            runs.append((start, prevC, prev))
        start, prev = C, bd
    prevC = C
runs.append((start, prevC, prev))
for s0, s1, bd in runs:
    if s1 - s0 >= 0.004 or bd in (4,):
        print(f'  C in [{s0:+.4f}, {s1:+.4f}]  -> {BANDS[bd]}')
print('  known: fixed pt (-0.75,0.25); period-2 (-1.25,-0.75); period-4 (-1.368,-1.25); Feigenbaum pt -1.40116; period-3 window (-1.7549,-1.75); escape C>0.25 or C<-2')

# ---------------------------------------------------------------- 7. band flicker from the 10-phase spine vs reclassify every 12 ticks
section('7. Spine dynamics: sign flips absorbed by |.|, aliasing of reclassify (every 12 ticks) with the 10-tick cycle, and long-run relaxation')


def adv_spine(spine, ph, tick, rng):
    i = ph
    p, o = spine[(i + 9) % 10], spine[i]
    if i == 0: v = p * (1 - SIG) * 0.1
    elif i == 1: v = o * SIG + p * (1 - SIG)
    elif i == 2: v = abs(o - p) * SIG + o * (1 - SIG)
    elif i == 3: v = o + (1 - o) * (1 - SIG)
    elif i == 4: v = o * SIG
    elif i == 5: v = (o + sum(spine) / 10) / 2
    elif i == 6: v = o * SIG + (rng.random() - .5) * .003
    elif i == 7: v = math.sqrt(max(.001, o * p))
    elif i == 8: v = o * (1 + .008 * math.sin(tick * .1))
    else: v = o * SIG + TS * (1 - SIG)
    spine[i] = max(.001, min(1, v))
    return (i + 1) % 10


def mod_cells(cells, spine, ph, tick, rng):
    sv = spine[ph]
    for cl in cells:
        a, b, c = cl['a'], cl['b'], cl['c']
        if ph == 0:
            k = 1 - SIGS * sv; a *= k; b *= k; c *= k
        elif ph == 1: c = c * SIG + (c + sv * 0.05) * SIGS
        elif ph == 2: b = -b
        elif ph == 3: b = abs(b)
        elif ph == 4: a = -a
        elif ph == 5: a = abs(a)
        elif ph == 6:
            a += (rng.random() - .5) * sv * 0.006; b += (rng.random() - .5) * sv * 0.006
        elif ph == 7: a = a * SIG + sv * 0.2 * SIGS
        elif ph == 8: b *= 1 + 0.004 * math.sin(tick * 0.08)
        else:
            a = a * SIG + cl['a0'] * SIGS; b = b * SIG + cl['b0'] * SIGS; c = c * SIG + cl['c0'] * SIGS
        cl['a'], cl['b'], cl['c'] = a, b, c


def census(cells):
    cc = collections.Counter(classify(c['a'], c['b'], c['c'])[0] for c in cells)
    return [cc[i] for i in range(7)]


rng = random.Random(1)
cells = lattice()
spine, ph, tick = [TS] * 10, 0, 0
print('  JSX/harness order: tick t applies case (t mod 10); reclassify when t % 12 == 0 -> phases 2,4,6,8,0 in rotation.')
by_phase = {}
snap = {}
for t in range(1, 20001):
    tick += 1
    ph = adv_spine(spine, ph, tick, rng)
    mod_cells(cells, spine, ph, tick, rng)
    if 10000 < t <= 10010:
        by_phase[ph] = census(cells)
    if t % 10 == 0 and (t // 10) in (1, 20, 50, 100, 200, 500, 1000, 2000):
        Dm = np.mean([c['b'] ** 2 - 4 * c['a'] * c['c'] for c in cells])
        clk = sum(abs(c['b'] ** 2 - 4 * c['a'] * c['c']) < 0.15 for c in cells)
        nega = sum(c['a'] < 0 for c in cells)
        negb = sum(c['b'] < 0 for c in cells)
        snap[t // 10] = (census(cells), round(float(Dm), 3), clk, nega, negb)
print('  epoch-end census (after phase 0), long run  [VOID QUAN ATOM MOLE CELL ORGA CRYS], mean D, click, #a<0, #b<0:')
for ep in sorted(snap):
    print(f'    epoch {ep:5d}: {snap[ep][0]}  meanD={snap[ep][1]:7.3f} click={snap[ep][2]:3d}  a<0:{snap[ep][3]:3d} b<0:{snap[ep][4]:3d}')
print('  census within ONE late epoch, by phase just applied (what the UI shows if reclassify lands there):')
for p in sorted(by_phase):
    print(f'    after phase {p}: {by_phase[p]}')

# ---------------------------------------------------------------- 8. Test 7 'root-proximity topology'
section('8. Test 7: is the "root-proximity topology" different from the grid topology?')
print('  wireNeighbors() weights exactly the 8 grid neighbours (gN) and sorts them; the neighbour SET is the grid set for every cell.')
print('  Test 7 compares the weight-sorted top-3 with the first 3 grid neighbours in loop order (dr,dc = -1..1).')
rng2 = random.Random(0)
diff = 0
for cl in lattice():
    col, row = cl['col'], cl['row']
    ns = [(row + dr) * COLS + (col + dc) for dr in (-1, 0, 1) for dc in (-1, 0, 1)
          if not (dr == 0 and dc == 0) and 0 <= row + dr < ROWS and 0 <= col + dc < COLS]
    shuffled = ns[:]
    rng2.shuffle(shuffled)
    if shuffled[:3] != ns[:3]:
        diff += 1
print(f'  a RANDOM ordering of the same neighbours also "differs from grid priority" in {diff}/{NC} cells ({100*diff/NC:.1f}%) - the 99.6% is a readout.')
