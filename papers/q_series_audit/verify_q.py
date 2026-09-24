#!/usr/bin/env python3
"""verify_q.py -- the algebra checks behind Q_SERIES_AUDIT_2026-09-24.md (standard library only).

    python verify_q.py

Sections 1-19 check the Q series' claims about sigma = (0)(3)(8)(9)(1 7 6 5 4 2), the three table
renderings (TSML, BHML, CL_STD -- the same tables as the September foundation audit), the polynomial
forms, the trajectory and spectral tables, and the Q17 notes, with null models where a claim needs one.
Each section prints what it finds; the audit note says what each finding means.
"""
import itertools, math, cmath, random
from math import comb, gcd

S = [0, 7, 1, 3, 2, 4, 5, 6, 8, 9]          # sigma as list
SINV = [S.index(i) for i in range(10)]
N = ['VOID','LATT','CNTR','PROG','COLL','BAL','CHAOS','HARM','BRTH','RESET']

# renderings (from Gen14/.../J61/manuscript/verification/verify_J61.py)
BHML = [[0,1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,2,6,6],[2,3,3,4,5,6,7,3,6,6],
        [3,4,4,4,5,6,7,4,6,6],[4,5,5,5,5,6,7,5,7,7],[5,6,6,6,6,6,7,6,7,7],
        [6,7,7,7,7,7,7,7,7,7],[7,2,3,4,5,6,7,8,9,0],[8,6,6,6,7,7,7,9,7,8],
        [9,6,6,6,7,7,7,0,8,0]]
CL_STD = [[0,1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,7,8,1],[2,3,4,5,6,7,7,8,7,2],
          [3,4,5,6,7,7,7,7,7,3],[4,5,6,7,7,7,7,8,7,4],[5,6,7,7,7,8,7,7,7,5],
          [6,7,7,7,7,7,8,7,7,6],[7,7,8,7,8,7,7,8,7,7],[8,8,7,7,7,7,7,7,7,8],
          [9,1,2,3,4,5,6,7,8,0]]
TSML = [[0,0,0,0,0,0,0,7,0,0],[0,7,3,7,7,7,7,7,7,7],[0,3,7,7,4,7,7,7,7,9],
        [0,7,7,7,7,7,7,7,7,3],[0,7,4,7,7,7,7,7,8,7],[0,7,7,7,7,7,7,7,7,7],
        [0,7,7,7,7,7,7,7,7,7],[7,7,7,7,7,7,7,7,7,7],[0,7,7,7,8,7,7,7,7,7],
        [0,7,9,3,7,7,7,7,7,7]]

def hdr(t): print('\n=== ' + t + ' ===')

def cycles(p):
    seen, out = set(), []
    for i in range(len(p)):
        if i in seen: continue
        c, j = [], i
        while j not in seen:
            seen.add(j); c.append(j); j = p[j]
        out.append(c)
    return out

def power(p, k):
    q = list(range(len(p)))
    for _ in range(k): q = [p[x] for x in q]
    return q

hdr('1. sigma basics')
print('cycles:', cycles(S))
print('order:', next(k for k in range(1, 100) if power(S, k) == list(range(10))))
print('fixed:', [i for i in range(10) if S[i] == i])
print('sigma^6 == id:', power(S, 6) == list(range(10)))

hdr('2. Is sigma a polynomial function over Z/10? (needs x mod2 -> s(x) mod2 and x mod5 -> s(x) mod5)')
mod2_ok = all(len({S[x] % 2 for x in range(10) if x % 2 == e}) == 1 for e in (0, 1))
mod5_ok = all(len({S[x] % 5 for x in range(10) if x % 5 == y}) == 1 for y in range(5))
print('parity respected:', mod2_ok, ' mod-5 respected:', mod5_ok)
print('even inputs map to', sorted(S[x] for x in range(0, 10, 2)))

# CRT coords
phi = lambda e, y: (5 * e + 6 * y) % 10
inv = {phi(e, y): (e, y) for e in (0, 1) for y in range(5)}
assert all(inv[x] == (x % 2, x % 5) for x in range(10))

hdr('3. Q9 alpha / Q10 beta reproduce sigma?')
def alpha(e, y):
    a = (1 - pow(y*y + 2*y + 2, 4, 5) - e * (pow(y*y + 3*y, 4, 5) - pow(y*y + 2*y + 2, 4, 5))) % 5
    return a
def beta(e, y):
    return (-alpha(e, y) + e * 4*y*(y-2)*(y-3)*(y-4) - 2*(1-e) * 4*y*(y-1)*(y-2)*(y-3)) % 5
ok = True
for x in range(10):
    e, y = inv[x]
    a = alpha(e, y); assert a in (0, 1)
    img = phi((e + a) % 2, (y + beta(e, y)) % 5)
    ok &= (img == S[x])
print('Q10 boxed (alpha,beta) reproduces sigma on all 10:', ok)
# Q9 lines 191-196 version: y' = y - alpha + 2*[ (1,1) ] - 1*[ (0,4) ]
bad = []
for x in range(10):
    e, y = inv[x]
    a = alpha(e, y)
    yp = (y - a + 2 * (e == 1 and y == 1) - 1 * (e == 0 and y == 4)) % 5
    img = phi((e + a) % 2, yp)
    if img != S[x]: bad.append((x, img, S[x]))
print('Q9 "complete sigma-action" (lines 191-196) mismatches (x, formula, sigma):', bad)

hdr('4. Genericity: same alpha/beta construction for random permutations')
def build_ab(p):
    # alpha: F5 Lagrange per eps-slice of the parity-flip indicator; beta likewise for delta-y
    def lag(vals):  # vals[y] in F5 -> coefficient-free evaluator via Lagrange
        def f(y):
            s = 0
            for yi in range(5):
                num, den = 1, 1
                for yj in range(5):
                    if yj != yi: num *= (y - yj); den *= (yi - yj)
                s += vals[yi] * num * pow(den % 5, 3, 5)
            return s % 5
        return f
    A = {e: lag([int((p[phi(e, y)] % 2) != e) for y in range(5)]) for e in (0, 1)}
    B = {e: lag([(p[phi(e, y)] % 5 - y) % 5 for y in range(5)]) for e in (0, 1)}
    return (lambda e, y: ((1 - e) * A[0](y) + e * A[1](y)) % 5,
            lambda e, y: ((1 - e) * B[0](y) + e * B[1](y)) % 5)
random.seed(1)
allok = True
for _ in range(2000):
    p = list(range(10)); random.shuffle(p)
    a, b = build_ab(p)
    for x in range(10):
        e, y = inv[x]
        if phi((e + a(e, y)) % 2, (y + b(e, y)) % 5) != p[x]: allok = False
print('2000 random permutations all get an exact (alpha,beta) "polynomial" form:', allok)

hdr('5. Q13 boxed TIG (= sigma^-1) polynomial')
def bTIG(e, y):
    return (1 - pow(y*y + 4, 4, 5) - e * (pow(y*y + 4*y, 4, 5) - pow(y*y + 4, 4, 5))) % 5
def gTIG(e, y):
    d = 4*y*(y-1)*(y-3)*(y-4)
    return (bTIG(e, y) + (1 - e) * d - 2 * e * d) % 5
flipok = all(((SINV[x] % 2) != (x % 2)) == (bTIG(*inv[x]) == 1) for x in range(10))
print('beta_TIG flip condition correct on all 10:', flipok)
res = []
for x in range(10):
    e, y = inv[x]
    img = phi((e + bTIG(e, y)) % 2, (y + gTIG(e, y)) % 5)
    res.append(img)
print('boxed TIG map:', res)
print('sigma^-1     :', SINV)
print('mismatches (x, formula, true):', [(x, res[x], SINV[x]) for x in range(10) if res[x] != SINV[x]])
print('boxed TIG map is a permutation?', sorted(res) == list(range(10)))

hdr('6. Flip sets; Q13.2 "exception pair swap"')
flip = lambda p: {x for x in range(10) if (p[x] % 2) != (x % 2)}
print('Flip(sigma)=', sorted(flip(S)), ' Flip(sigma^-1)=', sorted(flip(SINV)),
      ' sigma(Flip(sigma))=', sorted(S[x] for x in flip(S)))
cyc = [1, 7, 6, 5, 4, 2]
print('sigma non-flips in cycle:', [x for x in cyc if x not in flip(S)],
      ' TIG non-flips in cycle:', [x for x in cyc if x not in flip(SINV)])

hdr('7. Q14 1_C = eps*y^4 ; Q15 anchor indicator A and tau = 6-5A')
print('1_C ok:', all((e * pow(y, 4, 5)) % 5 == (1 if gcd(phi(e, y), 10) == 1 else 0)
                     for e in (0, 1) for y in range(5)))
def A(e, y):
    return (4*y*(y-1)*(y-2)*(y-4) + (1-e)*4*(y-1)*(y-2)*(y-3)*(y-4) + e*4*y*(y-1)*(y-2)*(y-3)) % 5
tau = [6 - 5 * A(*inv[x]) for x in range(10)]
true_tau = [next(k for k in range(1, 7) if power(S, k)[x] == x) for x in range(10)]
print('tau from A:', tau, ' true periods:', true_tau, ' equal:', tau == true_tau)
print('6-5A reduced mod 5 (as an F5 polynomial):', sorted({t % 5 for t in tau}))

hdr('8. Q11/Q14 trajectory gate score (C={1,3,7,9}), Q15 sigma^3')
C10 = {1, 3, 7, 9}
for s in range(1, 10):
    traj = [power(S, j)[s] for j in range(9)]
    print(s, traj, 'C-hits', sum(t in C10 for t in traj), '/9', ' sigma^3 =', power(S, 3)[s])

hdr('9. G8 coherence integral G(s) and null model')
w = cmath.exp(2j * math.pi / 9)
def chi_of(p):
    fl = flip(p)
    return [0 if p[x] == x else (1 if x not in fl else -1) for x in range(10)]
def Gvals(p, chi=None, K=9, om=w):
    chi = chi if chi is not None else chi_of(p)
    out = []
    for s in range(10):
        z, x = 0, s
        for j in range(K):
            z += om**j * chi[x]; x = p[x]
        out.append(round(abs(z)**2, 6))
    return out
g = Gvals(S)
print('chi:', chi_of(S))
print('G(s):', g)
print('distinct:', sorted(set(g)), ' ratio high/low:', round(max(g) / min(v for v in g if v > 0), 3))
print('argmax states:', [s for s in range(10) if abs(g[s] - max(g)) < 1e-6])
# CLAY_SPECTRAL_BRIDGE literal chi: +1 at {1,6}, -1 at {7,4,5,2}
chi_clay = [0, 1, -1, 0, -1, -1, 1, -1, 0, 0]
print('G with CLAY paper literal chi (+1 at digits 1,6):', Gvals(S, chi_clay))
# window 6 with omega = e^{2 pi i/6}
print('G with window 6, omega=e^(2pi i/6):', Gvals(S, K=6, om=cmath.exp(2j*math.pi/6)))
print('G with window 6, omega=e^(2pi i/9):', Gvals(S, K=6))

# null: all permutations of cycle type (6,1,1,1,1) on {0..9}, same chi rule
from collections import Counter
cnt_vals, cnt_two_nonflip, cnt_swap, cnt_high_is_TIGexc, tot = Counter(), 0, 0, 0, 0
cnt_same_pattern = 0
for fixed in itertools.combinations(range(10), 4):
    rest = [x for x in range(10) if x not in fixed]
    first = rest[0]
    for perm in itertools.permutations(rest[1:]):
        order = [first] + list(perm)
        p = list(range(10))
        for i in range(6): p[order[i]] = order[(i + 1) % 6]
        tot += 1
        gv = Gvals(p)
        cycv = sorted({gv[x] for x in order})
        cnt_vals[len(cycv)] += 1
        pinv = [p.index(i) for i in range(10)]
        nf = [x for x in order if x not in flip(p)]
        if len(nf) == 2:
            cnt_two_nonflip += 1
            tig_nf = [x for x in order if x not in flip(pinv)]
            tig_only = [x for x in order if x in flip(pinv) and x not in flip(p)]
            if set(tig_only) == set(nf): cnt_swap += 1
            top = [x for x in order if abs(gv[x] - max(gv)) < 1e-6]
            if set(top) == set(tig_nf): cnt_high_is_TIGexc += 1
            if len(cycv) == 2: cnt_same_pattern += 1
print('null over', tot, 'perms of type 6+1^4: #distinct G values on the cycle ->', dict(cnt_vals))
print('  perms with exactly 2 non-flips in the cycle:', cnt_two_nonflip,
      '; of these, exception-pair-swap holds:', cnt_swap,
      '; two-valued G on cycle:', cnt_same_pattern,
      '; G_high set == TIG non-flip set:', cnt_high_is_TIGexc)

# all sign patterns on a 6-cycle (chi in {+1,-1}^6), window 9, omega_9
pat_vals = Counter()
for signs in itertools.product([1, -1], repeat=6):
    vals = set()
    for p0 in range(6):
        z = sum(w**j * signs[(p0 + j) % 6] for j in range(9))
        vals.add(round(abs(z)**2, 6))
    pat_vals[len(vals)] += 1
print('all 64 sign patterns on a 6-cycle -> #distinct G over start positions:', dict(pat_vals))

hdr('10. G7: E[tau], Var[tau]; which cycle types give E[tau]=4')
E = sum(true_tau) / 10; V = sum((t - E)**2 for t in true_tau) / 10
print('E', E, 'Var', V, ' phi(10)*(1+1/5)=', 4 * 1.2)
def partitions(n, m=None):
    m = n if m is None else m
    if n == 0: yield []; return
    for k in range(min(n, m), 0, -1):
        for rest in partitions(n - k, k): yield [k] + rest
good = [pt for pt in partitions(10) if sum(k*k for k in pt) == 40]
def count_type(pt):
    c = math.factorial(10)
    for k, m in Counter(pt).items(): c //= (k**m) * math.factorial(m)
    return c
print('cycle types with sum L^2 = 40 (E[tau]=4):', good,
      ' fraction of S_10:', sum(count_type(pt) for pt in good) / math.factorial(10))

hdr('11. CL definitions: P1 (CL[j][j]=sigma(j)) vs Architecture CL[t][s]=sigma^t(s) vs CL_STD')
arch = [power(S, t) for t in range(10)]
print('diag sigma          :', S)
print('diag sigma^j(j)     :', [arch[j][j] for j in range(10)])
print('diag CL_STD         :', [CL_STD[j][j] for j in range(10)])
print('diag BHML           :', [BHML[j][j] for j in range(10)])
print('diag TSML           :', [TSML[j][j] for j in range(10)])
print('[7][7]: TSML', TSML[7][7], 'BHML', BHML[7][7], 'CL_STD', CL_STD[7][7], 'sigma(7)', S[7])
def gate_score(T, C):
    return sum(1 for s in C for c in range(1, 10) if T[s][c] in C) / (len(C) * 9)
def g_stay(T, C):
    G = [x for x in range(1, 10) if x not in C]
    return sum(1 for s in G for c in range(1, 10) if T[s][c] in G) / (len(G) * 9)
for nm, T in [('CL[t][s]=sigma^t(s)', arch), ('CL_STD', CL_STD), ('BHML', BHML), ('TSML', TSML)]:
    print(f'{nm:22s} gate_score(b=10) = {gate_score(T, C10):.3f}   G_stay(b=10) = {g_stay(T, C10):.3f}')

hdr('12. Q6 table: |G| = p+q-2 vs the claimed 1..5; |G cap {1..9}|')
for b, p, q, claimed in [(6,2,3,1),(10,2,5,2),(15,3,5,3),(21,3,7,4),(35,5,7,5)]:
    G = [x for x in range(1, b) if gcd(x, b) > 1]
    print(b, 'claimed', claimed, ' |G| =', len(G), '= p+q-2 =', p+q-2, ' |G cap 1..9| =', sum(1 for x in G if x <= 9))

hdr('13. Q12 idempotents')
for b, p, q in [(6,2,3),(10,2,5),(15,3,5),(21,3,7),(35,5,7)]:
    ep = q * pow(q, -1, p) % b; eq = p * pow(p, -1, q) % b
    print(b, ep, eq, ep*ep % b == ep, eq*eq % b == eq, (ep+eq) % b == 1, gcd(ep, b) > 1, gcd(eq, b) > 1)

hdr('14. Q17_5D distances in R^5 (canonical digits, eps=x mod 2, y=x mod 5)')
def v(x):
    e, y = x % 2, x % 5
    return [e, math.cos(2*math.pi*y/5), math.sin(2*math.pi*y/5), math.cos(4*math.pi*y/5), math.sin(4*math.pi*y/5)]
D = [[math.dist(v(a), v(b)) for b in range(10)] for a in range(10)]
print('distinct pairwise distances:', sorted({round(D[a][b], 4) for a in range(10) for b in range(10) if a != b}))
for s in (5, 7, 4):
    print('nearest to', s, ':', min((round(D[s][b], 4), b) for b in range(10) if b != s))
print('cos(2pi y/5), cos(4pi y/5) for y=0..4:', [(round(math.cos(2*math.pi*y/5), 3), round(math.cos(4*math.pi*y/5), 3)) for y in range(5)])

hdr('15. Q5 TSML escape cells (this TSML rendering) and a crude null')
esc = [(i, j, TSML[i][j]) for i in range(1, 10) for j in range(1, 10) if TSML[i][j] != 7]
print('escape cells:', esc)
print('symmetric?', all(TSML[i][j] == TSML[j][i] for i, j, _ in esc))
outs_pairs = sorted({(min(i, j), max(i, j), o) for i, j, o in esc})
print('independent (unordered) escapes:', outs_pairs, ' outputs in Fix(sigma):', sum(o in (0,3,8,9) for _,_,o in outs_pairs))
p0 = 4/9
print('P(>=4 of 5 in Fix | each out ~ uniform over 9 non-7 values):', round(sum(comb(5,k)*p0**k*(1-p0)**(5-k) for k in (4,5)), 3))
# Q5 conjecture coverage
def conj(i, j, o):
    return (j in (3,8,9) and o == j) or (i in (3,8,9) and o == i) or ((i, j) in ((1,2),(2,1)))
print('escape cells NOT covered by Conjecture Q5:', [(i,j,o) for i,j,o in esc if not conj(i,j,o)])

hdr('16. Q7 BHML harmony count and symmetry')
print('7-cells:', sum(r.count(7) for r in BHML), ' symmetric:', all(BHML[i][j] == BHML[j][i] for i in range(10) for j in range(10)))

hdr('17. Q16 independence estimate')
pc = 0.292 * 4/9 + 0.708 * 0.667
print('p_cell', round(pc, 3), ' P(Bin(36,p)>=31) =', sum(comb(36, k) * pc**k * (1-pc)**(36-k) for k in range(31, 37)))

hdr('18. Q17_CLAY Hodge claim: C-elements reachable from HAR=3 via sigma?')
orb3 = {power(S, k)[3] for k in range(6)}
print('sigma-orbit of 3:', orb3, ' C={1,3,7,9} reachable:', C10 <= orb3)

hdr('19. G6: remove one beta correction -> is the map still a permutation?')
for drop in ('LATT', 'COLL'):
    img = []
    for x in range(10):
        e, y = inv[x]
        a = alpha(e, y)
        b = -a + (0 if drop == 'LATT' else e*4*y*(y-2)*(y-3)*(y-4)) - (0 if drop == 'COLL' else 2*(1-e)*4*y*(y-1)*(y-2)*(y-3))
        img.append(phi((e + a) % 2, (y + b) % 5))
    print('drop', drop, '->', img, ' permutation?', sorted(img) == list(range(10)))
