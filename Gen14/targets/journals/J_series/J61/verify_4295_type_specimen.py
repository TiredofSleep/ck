#!/usr/bin/env python3
"""verify_4295_type_specimen.py -- J61's Theorem 5 is false: ETP equation 4295 has a finite type specimen.

    python verify_4295_type_specimen.py                # ~1 minute
    python verify_4295_type_specimen.py --minimality   # + exhaustive search of orders 2-5 (~5 more minutes)

Needs only numpy. The ETP catalog of 4694 laws is rebuilt here from its definition (no download) and
checked against known anchors and against six profile counts that J61 itself computed on the real
catalog. Then:
  1. the implication-closure of #4295 is exactly 14 laws (13 follow from #4295 by renaming; the 6-element
     specimen below violates every other law);
  2. a 6-element magma satisfies #4295 and has ETP profile exactly that closure -- a type specimen;
  3. J61's bound "every finite model has profile >= 261" already fails at order 3 (profile 122);
  4. (--minimality) no model of order 2-5 has profile 14, so 6 is the smallest order of a specimen.
"""
import itertools
import sys

import numpy as np

# ---------------------------------------------------------------- the ETP catalog, rebuilt


def shapes(m):
    if m == 0:
        return [None]
    return [(l, r) for i in range(m) for l in shapes(i) for r in shapes(m - 1 - i)]


def n_leaves(s):
    return 1 if s is None else n_leaves(s[0]) + n_leaves(s[1])


def fill(s, it):
    return next(it) if s is None else (fill(s[0], it), fill(s[1], it))


def rg_strings(k):
    out = []

    def rec(prefix, mx):
        if len(prefix) == k:
            out.append(tuple(prefix))
            return
        for v in range(mx + 2):
            rec(prefix + [v], max(mx, v))
    rec([], -1)
    return out


def leaves(t):
    return [t] if isinstance(t, int) else leaves(t[0]) + leaves(t[1])


def relabel(t, mp):
    return mp[t] if isinstance(t, int) else (relabel(t[0], mp), relabel(t[1], mp))


def canon(lhs, rhs):
    mp = {}
    for v in leaves(lhs) + leaves(rhs):
        mp.setdefault(v, len(mp))
    return relabel(lhs, mp), relabel(rhs, mp)


def build_catalog():
    laws, seen = [], set()
    for total in range(5):
        for lo in range(total // 2 + 1):
            for ls in shapes(lo):
                for rs in shapes(total - lo):
                    for pat in rg_strings(n_leaves(ls) + n_leaves(rs)):
                        it = iter(pat)
                        lhs, rhs = fill(ls, it), fill(rs, it)
                        if lhs == rhs and total > 0:
                            continue
                        key = (frozenset((repr(canon(lhs, rhs)), repr(canon(rhs, lhs))))
                               if lo == total - lo else repr(canon(lhs, rhs)))
                        if key not in seen:
                            seen.add(key)
                            laws.append((lhs, rhs))
    return laws


def show(t):
    if isinstance(t, int):
        return "xyzwuv"[t]
    a, b = show(t[0]), show(t[1])
    return f"{a if isinstance(t[0], int) else '(' + a + ')'}◇{b if isinstance(t[1], int) else '(' + b + ')'}"


def ev(t, T, env):
    return env[t] if isinstance(t, int) else T[ev(t[0], T, env), ev(t[1], T, env)]


LAWS = build_catalog()
GRIDS = {}


def profile(T):
    T = np.asarray(T)
    n = len(T)
    if n not in GRIDS:
        GRIDS[n] = {k: [g.ravel() for g in np.indices((n,) * k)] for k in range(1, 7)}
    out = set()
    for i, (lhs, rhs) in enumerate(LAWS, start=1):
        k = max(leaves(lhs) + leaves(rhs)) + 1
        if np.array_equal(ev(lhs, T, GRIDS[n][k]), ev(rhs, T, GRIDS[n][k])):
            out.add(i)
    return out


def ok(name, cond):
    print(f"  [{'PASS' if cond else 'FAIL'}] {name}")
    assert cond, name


print("0 -- the ETP catalog, rebuilt without downloading")
ok(f"{len(LAWS)} laws", len(LAWS) == 4694)
anchors = {1: "x = x", 14: "x = y◇(x◇y)", 43: "x◇y = y◇x", 4512: "x◇(y◇z) = (x◇y)◇z", 4295: "x◇(x◇y) = y◇(z◇x)"}
ok("anchors: " + "; ".join(f"#{i} {s}" for i, s in anchors.items()),
   all(f"{show(LAWS[i - 1][0])} = {show(LAWS[i - 1][1])}" == s for i, s in anchors.items()))
j61 = [(np.zeros((3, 3), int), 1556), (np.tile(np.arange(3), (3, 1)), 1214),
       (np.add.outer(np.arange(5), np.arange(5)) % 5, 32), ((-np.add.outer(np.arange(4), np.arange(4))) % 4, 294),
       (np.tile(np.array([1, 2, 2]), (3, 1)), 261)]
ok("profile counts J61 computed on the real catalog: constant 1556, right projection 1214, Z/5 32, "
   "negation mod 4 294, f = (1,2,2) 261", all(len(profile(T)) == want for T, want in j61))

CLOSURE = {1, 4269, 4284, 4287, 4290, 4293, 4295, 4316, 4340, 4343, 4345, 4360, 4369, 4371}
print("\n1 -- the implication-closure of #4295 has exactly 14 laws")


def pair_of(t):
    """x◇(y◇z) = z◇(z◇x) by #4295 (renamed), and a◇(a◇b) = b◇(b◇a) by #4295 with z = y: a right-nested
    term u◇(v◇w) equals P(w, u) with P symmetric -- so it is determined by the unordered pair {u, w}"""
    if isinstance(t, tuple) and isinstance(t[0], int) and isinstance(t[1], tuple) and all(isinstance(s, int) for s in t[1]):
        return frozenset([(t[0], 1), (t[1][1], 2)]) if t[0] != t[1][1] else frozenset([(t[0], 3)])
    return None


def implied(lhs, rhs):
    a, b = pair_of(lhs), pair_of(rhs)
    norm = lambda p: sorted(v for v, _ in p) if p and len(p) == 2 else ([next(iter(p))[0]] * 2 if p else None)
    return a is not None and b is not None and norm(a) == norm(b)


ok("each of the 13 non-trivial closure laws follows from #4295: both sides are right-nested products with "
   "the same unordered pair {outer-left, inner-right}", all(implied(*LAWS[i - 1]) for i in CLOSURE - {1}))

SPECIMEN = np.array([[0, 0, 0, 0, 0, 1],
                     [0, 0, 0, 0, 0, 1],
                     [0, 0, 0, 0, 0, 2],
                     [0, 0, 0, 0, 0, 2],
                     [0, 0, 0, 0, 0, 2],
                     [0, 3, 3, 0, 3, 4]])
n = len(SPECIMEN)
print("\n2 -- a type specimen of order 6")
ok("#4295 holds in the specimen (all 216 triples)",
   all(SPECIMEN[x, SPECIMEN[x, y]] == SPECIMEN[y, SPECIMEN[z, x]] for x in range(n) for y in range(n) for z in range(n)))
prof = profile(SPECIMEN)
ok(f"its ETP profile is exactly {{1}} + closure(4295): {len(prof)} laws, the 14 above -- every other law "
   "fails in it (so, with part 1, the closure is exactly these 14)", prof == CLOSURE)
print("  => the variety of #4295 has a finite type specimen. J61's Theorem 5 is false.")

print("\n3 -- J61's lower bound")
m3 = np.array([[0, 0, 0], [0, 0, 1], [0, 0, 1]])
ok("the order-3 model [[0,0,0],[0,0,1],[0,0,1]] satisfies #4295 and has profile 122, not >= 261",
   all(m3[x, m3[x, y]] == m3[y, m3[z, x]] for x in range(3) for y in range(3) for z in range(3))
   and len(profile(m3)) == 122)

if "--minimality" in sys.argv:
    print("\n4 -- minimality: every model of order 2-5, up to isomorphism")

    def models(n):
        N, T = n * n, [-1] * (n * n)
        triples = [(x, y, z) for x in range(n) for y in range(n) for z in range(n)]
        order = sorted(range(N), key=lambda c: (max(divmod(c, n)), c))
        found = []

        def propagate(trail):
            changed = True
            while changed:
                changed = False
                for x, y, z in triples:
                    a, b = T[x * n + y], T[z * n + x]
                    if a < 0 or b < 0:
                        continue
                    li, ri = x * n + a, y * n + b
                    l, r = T[li], T[ri]
                    if l >= 0 and r >= 0 and l != r:
                        return False
                    if l >= 0 > r:
                        T[ri] = l
                        trail.append(ri)
                        changed = True
                    elif r >= 0 > l:
                        T[li] = r
                        trail.append(li)
                        changed = True
            return True

        def search():
            cell = next((c for c in order if T[c] < 0), None)
            if cell is None:
                found.append(tuple(T))
                return
            m = max([-1] + [max(*divmod(c, n), T[c]) for c in range(N) if T[c] >= 0])
            i, j = divmod(cell, n)
            for v in range(min(n - 1, max(m, i, j) + 1) + 1):
                trail = [cell]
                T[cell] = v
                if propagate(trail):
                    search()
                for c in trail:
                    T[c] = -1
        search()
        perms = np.array(list(itertools.permutations(range(n))))
        inv = np.argsort(perms, axis=1)
        classes = set()
        for t in found:
            A = np.array(t).reshape(n, n)
            Bm = perms[np.arange(len(perms))[:, None, None], A[inv[:, :, None], inv[:, None, :]]].reshape(len(perms), N)
            classes.add(tuple(Bm[np.lexsort(Bm.T[::-1])[0]]))
        return [np.array(c).reshape(n, n) for c in sorted(classes)]

    for n in (2, 3, 4, 5):
        cls = models(n)
        # a model where all right-nested products are equal satisfies all 112 laws u(vw) = u'(v'w'): profile >= 113
        breakers = [T for T in cls if len({int(T[a][T[a][b]]) for a in range(n) for b in range(n)}) > 1]
        low = min([len(profile(T)) for T in breakers] or [10 ** 9])
        full = min(len(profile(T)) for T in cls) if n <= 4 else min(low, 113)
        ok(f"order {n}: {len(cls)} models up to isomorphism, smallest profile {full} > 14", full > 14)
    print("  => no type specimen below order 6: the specimen above has the smallest possible order.")

print("\nALL CHECKS PASS.")
