#!/usr/bin/env python3
"""verify_j61_closures.py -- all eight of J61's size-14 closures have a finite type specimen.

    python verify_j61_closures.py                # about 2 minutes
    python verify_j61_closures.py --minimality   # + the searches behind the smallest orders (~1 more minute)

Needs only numpy. J61 section 6 lists the eight implication-closures of size 14 in the catalog of Tao's
Equational Theories Project (ETP). It calls C1 and C2 realized, C5 a proved "fossil variety" (its Theorem
5), C8 a fossil variety, and C3, C4, C6, C7 open, and it conjectures that none of C3-C8 has a finite type
specimen (a magma whose ETP profile is exactly the closure). Every one of the eight has one:

    closure  anchor  specimen                                    smallest order
    C1       #40     a 3-element magma                           3
    C2       #43     a 3-element magma                           3
    C3       #1312   32 elements: the affine mean over GF(8)     unknown; between 7 and 32
                     times a 4-element model
    C4       #2241   the transpose of C3's                       as C3
    C5       #4295   a 6-element magma (see verify_4295_...)     6
    C6       #4303   a 5-element magma                           5
    C7       #4610   the transpose of C5's                       6
    C8       #4637   the transpose of C6's                       5

The transposes work because the opposite magma (x*y := y◇x) turns the laws a magma satisfies into their
mirror images, and J61's closures pair up under that mirror: C3-C4, C5-C7, C6-C8 (C1 and C2 are their own
mirrors).
"""
import itertools
import sys

import numpy as np

# ---------------------------------------------------------------- the ETP catalog, rebuilt (no download)


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


def ops(t):
    return 0 if isinstance(t, int) else 1 + ops(t[0]) + ops(t[1])


def relabel(t, mp):
    return mp[t] if isinstance(t, int) else (relabel(t[0], mp), relabel(t[1], mp))


def canon(lhs, rhs):
    mp = {}
    for v in leaves(lhs) + leaves(rhs):
        mp.setdefault(v, len(mp))
    return relabel(lhs, mp), relabel(rhs, mp)


def key(lhs, rhs):
    if ops(lhs) > ops(rhs):
        lhs, rhs = rhs, lhs
    if ops(lhs) == ops(rhs):
        return frozenset((repr(canon(lhs, rhs)), repr(canon(rhs, lhs))))
    return repr(canon(lhs, rhs))


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
                        k = key(lhs, rhs)
                        if k not in seen:
                            seen.add(k)
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
NVARS = [max(leaves(l) + leaves(r)) + 1 for l, r in LAWS]
GRIDS = {}


def grid(n, k):
    if (n, k) not in GRIDS:
        GRIDS[n, k] = [g.ravel() for g in np.indices((n,) * k)]
    return GRIDS[n, k]


def holds(i, T):
    lhs, rhs = LAWS[i - 1]
    env = grid(len(T), NVARS[i - 1])
    return bool(np.array_equal(ev(lhs, T, env), ev(rhs, T, env)))


def profile(T):
    T = np.asarray(T)
    return {i for i in range(1, len(LAWS) + 1) if holds(i, T)}


def canonical(T):
    """a fixed representative of T's isomorphism class"""
    T = np.asarray(T)
    n = len(T)
    perms = np.array(list(itertools.permutations(range(n))))
    inv = np.argsort(perms, axis=1)
    B = perms[np.arange(len(perms))[:, None, None], T[inv[:, :, None], inv[:, None, :]]].reshape(len(perms), n * n)
    return tuple(B[np.lexsort(B.T[::-1])[0]])


def classes(models):
    return {canonical(T) for T in models}


def ok(name, cond):
    print(f"  [{'PASS' if cond else 'FAIL'}] {name}")
    assert cond, name


print("0 -- the ETP catalog, rebuilt without downloading")
ok(f"{len(LAWS)} laws", len(LAWS) == 4694)
anchors = {1: "x = x", 14: "x = y◇(x◇y)", 40: "x◇x = y◇y", 43: "x◇y = y◇x", 1312: "x = y◇(((y◇x)◇x)◇x)",
           2241: "x = (x◇(x◇(x◇y)))◇y", 4295: "x◇(x◇y) = y◇(z◇x)", 4303: "x◇(x◇y) = z◇(y◇x)",
           4512: "x◇(y◇z) = (x◇y)◇z", 4610: "(x◇x)◇y = (y◇z)◇x", 4637: "(x◇y)◇x = (y◇x)◇z"}
ok("anchors, as the ETP numbers them: " + "; ".join(f"#{i} {s}" for i, s in anchors.items()),
   all(f"{show(LAWS[i - 1][0])} = {show(LAWS[i - 1][1])}" == s for i, s in anchors.items()))
j61 = [(np.zeros((3, 3), int), 1556), (np.tile(np.arange(3), (3, 1)), 1214),
       (np.add.outer(np.arange(5), np.arange(5)) % 5, 32), ((-np.add.outer(np.arange(4), np.arange(4))) % 4, 294),
       (np.tile(np.array([1, 2, 2]), (3, 1)), 261)]
ok("profile counts J61 computed on the real catalog: 1556, 1214, 32, 294, 261",
   all(len(profile(T)) == want for T, want in j61))

# ---------------------------------------------------------------- 1. the mirror


def mirror_term(t):
    return t if isinstance(t, int) else (mirror_term(t[1]), mirror_term(t[0]))


INDEX = {key(l, r): i for i, (l, r) in enumerate(LAWS, start=1)}
MIRROR = {i: INDEX[key(mirror_term(l), mirror_term(r))] for i, (l, r) in enumerate(LAWS, start=1)}


def mirror(S):
    return {MIRROR[i] for i in S}


print("\n1 -- the mirror: the opposite magma x*y := y◇x satisfies exactly the mirror images of the laws")
ok("mirroring is a flip on the 4694 laws (doing it twice changes nothing)", all(MIRROR[MIRROR[i]] == i for i in MIRROR))
fixed = sum(MIRROR[i] == i for i in MIRROR)
ok(f"{fixed} laws are their own mirror image (the edge); the other {len(LAWS) - fixed} form "
   f"{(len(LAWS) - fixed) // 2} mirror pairs (the two sides)", fixed == 84)
rng = np.random.default_rng(0)
ok("for 5 random magmas, the profile of the transpose is the mirror of the profile",
   all(profile(T.T) == mirror(profile(T)) for T in (rng.integers(0, 3, (3, 3)) for _ in range(5))))

# ---------------------------------------------------------------- 2. the eight closures

C = {"C1": {1, 40, 3659, 3662, 3665, 3677, 3684, 3688, 3692, 3700, 4270, 4341, 4590, 4622},
     "C2": {1, 43, 4283, 4358, 4380, 4398, 4405, 4435, 4442, 4482, 4531, 4544, 4635, 4677},
     "C3": {1, 8, 411, 1020, 1223, 1312, 1629, 1832, 2035, 3253, 3319, 3862, 3915, 4065},
     "C5": {1, 4269, 4284, 4287, 4290, 4293, 4295, 4316, 4340, 4343, 4345, 4360, 4369, 4371},
     "C6": {1, 4272, 4283, 4291, 4293, 4300, 4303, 4321, 4328, 4330, 4351, 4358, 4374, 4376}}
C["C4"], C["C7"], C["C8"] = mirror(C["C3"]), mirror(C["C5"]), mirror(C["C6"])
J61_ANCHORS = {"C1": [40, 3688, 3692, 3700], "C2": [43], "C3": [1312], "C4": [2241], "C5": [4295, 4345, 4371],
               "C6": [4303, 4328, 4376], "C7": [4610, 4660, 4686], "C8": [4637, 4659, 4678]}

print("\n2 -- the eight closures, each 14 laws (x = x included)")
ok("each closure has 14 laws and contains J61's anchors for it",
   all(len(C[c]) == 14 and set(a) <= C[c] for c, a in J61_ANCHORS.items()))
ok("the mirror pairs them: C3 <-> C4, C5 <-> C7, C6 <-> C8; C1 and C2 are their own mirrors",
   mirror(C["C1"]) == C["C1"] and mirror(C["C2"]) == C["C2"] and mirror(C["C4"]) == C["C3"]
   and C["C4"] == mirror(C["C3"]) and 2241 in C["C4"] and 4610 in C["C7"] and 4637 in C["C8"])


def normal(t, rule):
    """rewrite a term to a normal form that is valid in every model of the anchor"""
    if isinstance(t, int):
        return t
    a, b = normal(t[0], rule), normal(t[1], rule)
    return rule(a, b)


def squares(a, b):          # #40: all squares are equal -- call the common value c
    return "c" if a == b else (a, b)


def commute(a, b):          # #43: the two factors can be swapped
    return tuple(sorted((a, b), key=repr))


def outer_pair(a, b):       # #4295: a◇(v◇w) = F(a, w) with F symmetric (derivation in the note)
    return ("F",) + tuple(sorted((a, b[1]), key=repr)) if isinstance(b, tuple) and len(b) == 2 else (a, b)


def inner_pair(a, b):       # #4303: a◇(v◇w) = G(v, w) with G symmetric (derivation in the note)
    return ("G",) + tuple(sorted(b, key=repr)) if isinstance(b, tuple) and len(b) == 2 else (a, b)


def implied(c, rule):
    return all(normal(LAWS[i - 1][0], rule) == normal(LAWS[i - 1][1], rule) for i in C[c] - {1})


ok("every law of C1 follows from #40 (rewrite every square to one constant: both sides agree)", implied("C1", squares))
ok("every law of C2 follows from #43 (sort the two factors of every product: both sides agree)", implied("C2", commute))
ok("every law of C5 follows from #4295 (a◇(v◇w) depends only on {a, w}: both sides agree)", implied("C5", outer_pair))
ok("every law of C6 follows from #4303 (a◇(v◇w) depends only on {v, w}: both sides agree)", implied("C6", inner_pair))
print("  (C3: the ETP proves, in Lean, that #1312 implies the other 12 non-trivial laws listed; C4, C7, C8 follow")
print("   by mirroring. That no further law follows from any anchor is shown by the specimens below.)")

# ---------------------------------------------------------------- 3. the specimens


def product(A, B):
    nb = len(B)
    return np.array([[A[i // nb][j // nb] * nb + B[i % nb][j % nb] for j in range(len(A) * nb)]
                     for i in range(len(A) * nb)])


def gf8_mul(a, b):
    """multiplication in GF(8) = GF(2)[t]/(t^3 + t^2 + 1); an element is a 3-bit integer"""
    r = 0
    for i in range(3):
        if b >> i & 1:
            r ^= a << i
    for d in (4, 3):
        if r >> d & 1:
            r ^= 0b1101 << (d - 3)
    return r


G8 = np.array([[gf8_mul(2, x) ^ gf8_mul(3, y) for y in range(8)] for x in range(8)])    # x◇y = t·x + (1+t)·y
# the ETP's witness for "1312 does not imply 16" (Equation Explorer, pair 1312,16)
ETP_WITNESS = np.array([[0, 2, 3, 4, 5, 6, 7, 1], [4, 1, 6, 0, 7, 3, 5, 2], [5, 3, 2, 7, 0, 1, 4, 6],
                        [6, 7, 4, 3, 1, 0, 2, 5], [7, 6, 1, 5, 4, 2, 0, 3], [1, 4, 7, 2, 6, 5, 3, 0],
                        [2, 0, 5, 1, 3, 7, 6, 4], [3, 5, 0, 6, 2, 4, 1, 7]])
M4 = np.array([[0, 1, 3, 2], [1, 0, 3, 2], [0, 1, 3, 2], [1, 0, 3, 2]])

SPECIMENS = {
    "C1": np.array([[0, 0, 1], [1, 0, 2], [1, 1, 0]]),
    "C2": np.array([[0, 0, 1], [0, 2, 0], [1, 0, 0]]),
    "C5": np.array([[0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 0, 2],
                    [0, 0, 0, 0, 0, 2], [0, 0, 0, 0, 0, 2], [0, 3, 3, 0, 3, 4]]),
    "C6": np.array([[0, 0, 0, 1, 1], [0, 0, 0, 0, 1], [0, 0, 4, 0, 1], [0, 0, 0, 0, 1], [0, 0, 0, 0, 1]]),
}
SPECIMENS["C7"], SPECIMENS["C8"] = SPECIMENS["C5"].T.copy(), SPECIMENS["C6"].T.copy()

print("\n3 -- a type specimen for every closure")
for c in ("C1", "C2", "C5", "C6", "C7", "C8"):
    T = SPECIMENS[c]
    ok(f"{c}: a {len(T)}-element magma satisfies #{J61_ANCHORS[c][0]} and its ETP profile is exactly {c}",
       holds(J61_ANCHORS[c][0], T) and profile(T) == C[c])


def exact_product(A, B, closure):
    """the profile of A x B is exactly `closure`, checked directly on the product: every law of the closure
    holds at every assignment, and every other law fails at a lifted failing assignment of a factor"""
    P, nb = product(A, B), len(B)
    if not all(holds(i, P) for i in closure):
        return False
    for i in range(1, len(LAWS) + 1):
        if i in closure:
            continue
        lhs, rhs = LAWS[i - 1]
        for F, lift in ((A, lambda e: e * nb), (B, lambda e: e)):
            env = grid(len(F), NVARS[i - 1])
            bad = np.flatnonzero(ev(lhs, F, env) != ev(rhs, F, env))
            if len(bad):
                e = [lift(g[bad[0]]) for g in env]
                if ev(lhs, P, e) != ev(rhs, P, e):
                    break
        else:
            return False
    return True


ok("C3: x◇y = t·x + (1+t)·y over GF(8) (t^3 = t^2 + 1) satisfies #1312 and breaks x = y◇(y◇x); it is "
   "the ETP's own 8-element witness for '#1312 does not imply #16', up to renaming",
   holds(1312, G8) and not holds(16, G8) and canonical(G8) == canonical(ETP_WITNESS))
ok("C3: a 4-element model of #1312 kills the rest: profile(GF(8) mean) ∩ profile(4-element model) = C3",
   holds(1312, M4) and profile(G8) & profile(M4) == C["C3"])
ok("C3: so their 32-element product is a type specimen -- checked directly on the product", exact_product(G8, M4, C["C3"]))
ok("C4: the transpose of that product (= the product of the transposes) is a type specimen of C4",
   holds(2241, product(G8.T, M4.T)) and exact_product(G8.T.copy(), M4.T.copy(), C["C4"]))

print("\n4 -- two claims J61 makes along the way")
ok("'At order 3, no magma realizes Family C [the commutativity closure C2] exactly' -- false: the 3-element "
   "specimen above does", profile(SPECIMENS["C2"]) == C["C2"])
count = 0
for cells in itertools.product(range(3), repeat=6):
    T = np.zeros((3, 3), int)
    T[np.triu_indices(3)] = cells
    T = T + np.triu(T, 1).T
    count += profile(T) == C["C2"]
ok(f"realizing C2 is the ordinary case, not a mark of a special table: {count} of the 729 commutative "
   "magmas of order 3 do", count == 120)
rng = np.random.default_rng(1)
tens = [rng.integers(0, 10, (10, 10)) for _ in range(10)]
tens = [np.triu(U) + np.triu(U, 1).T for U in tens]
ok("and all 10 of 10 random commutative magmas of order 10 do (J59/J61 present this as a property of the "
   "sigma-magma)", all(profile(T) == C["C2"] for T in tens))

# ---------------------------------------------------------------- 5. smallest orders (--minimality)

if "--minimality" in sys.argv:
    print("\n5 -- the smallest orders")
    ok("C1, C2: no magma of order 2 has either profile (all 16 checked)",
       all(profile(np.array(c).reshape(2, 2)) not in (C["C1"], C["C2"]) for c in itertools.product(range(2), repeat=4)))

    def c6_models(n):
        """every model of #4303 of order n (least-number heuristic; isomorphic copies may repeat)"""
        N, T = n * n, [-1] * (n * n)
        triples = [(x, y, z) for x in range(n) for y in range(n) for z in range(n)]
        order = sorted(range(N), key=lambda c: (max(divmod(c, n)), c))
        found = []

        def propagate(trail):
            changed = True
            while changed:
                changed = False
                for x, y, z in triples:
                    a, b = T[x * n + y], T[y * n + x]
                    if a < 0 or b < 0:
                        continue
                    li, ri = x * n + a, z * n + b
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
                found.append(np.array(T).reshape(n, n))
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
        return found

    brute = [np.array(c).reshape(3, 3) for c in itertools.product(range(3), repeat=9)]
    ok("C6: the search is complete -- at order 3 it finds every isomorphism class that brute force finds "
       "(all 19,683 magmas)", classes(c6_models(3)) == classes(T for T in brute if holds(4303, T)))
    for n in (2, 3, 4):
        ms = c6_models(n)
        # if every right-nested product u◇(v◇w) is equal, all 112 laws u◇(v◇w) = u'◇(v'◇w') hold: profile >= 113
        small = [T for T in ms if len({T[u, T[v, w]] for u in range(n) for v in range(n) for w in range(n)}) > 1]
        low = min([len(profile(T)) for T in (ms if n < 4 else small)] + ([113] if n == 4 else []))
        ok(f"C6: the smallest profile of a model of #4303 of order {n} is {low} > 14", low > 14)

    def c3_models(n, witness=None):
        """models of #1312 of order n. In a finite model every row is a permutation: x = y◇(...) makes each
        left multiplication onto, hence one-to-one. With witness (0, w), only models where 0◇(0◇w) != w: a
        model that breaks x = y◇(y◇x) can be renamed so that its witness is (0, 1), or (0, 0) if y = x."""
        N = n * n
        T, inv, cnt = [-1] * N, [-1] * N, [0] * n
        order = sorted(range(N), key=lambda c: (max(divmod(c, n)), c))
        found = []

        def assign(cell, v, trail, queue):
            y, col = divmod(cell, n)
            if T[cell] >= 0:
                return T[cell] == v
            if inv[y * n + v] >= 0:
                return False
            T[cell], inv[y * n + v] = v, col
            cnt[y] += 1
            trail.append(cell)
            queue.extend((yy, col) for yy in range(n))
            queue.append((y, v))
            if cnt[y] == n - 1:
                c = next(c for c in range(n) if T[y * n + c] < 0)
                return assign(y * n + c, next(w for w in range(n) if inv[y * n + w] < 0), trail, queue)
            return True

        def propagate(trail, queue):
            while queue:
                y, x = queue.pop()
                a = T[y * n + x]
                b = T[a * n + x] if a >= 0 else -1
                c = T[b * n + x] if b >= 0 else -1
                if b >= 0 and c < 0 and inv[y * n + x] >= 0:
                    if not assign(b * n + x, inv[y * n + x], trail, queue):
                        return False
                elif c >= 0 and not assign(y * n + c, x, trail, queue):
                    return False
            if witness is None:
                return True
            w = witness[1]
            return not (T[w] >= 0 and T[T[w]] == w)

        def undo(trail, mark):
            while len(trail) > mark:
                cell = trail.pop()
                inv[cell // n * n + T[cell]] = -1
                T[cell] = -1
                cnt[cell // n] -= 1

        trail = []

        def search(m0):
            cell = next((c for c in order if T[c] < 0), None)
            if cell is None:
                found.append(np.array(T).reshape(n, n))
                return
            m = max([m0] + [max(*divmod(c, n), T[c]) for c in trail])
            i, j = divmod(cell, n)
            for v in range(min(n - 1, max(m, i, j) + 1) + 1):
                mark, queue = len(trail), []
                if assign(cell, v, trail, queue) and propagate(trail, queue):
                    search(m0)
                undo(trail, mark)

        if propagate(trail, [(y, x) for y in range(n) for x in range(n)]):
            search(-1 if witness is None else max(witness))
        return found

    def brute_1312(n):
        """every n x n table satisfying #1312, by brute force: all n^(n*n) tables for n <= 3, and all tables
        with permutation rows for n = 4"""
        rows = np.array(list(itertools.product(range(n), repeat=n)) if n <= 3 else list(itertools.permutations(range(n))))
        Ts = rows[np.array(list(itertools.product(range(len(rows)), repeat=n)))]
        ar, good = np.arange(len(Ts)), np.ones(len(Ts), bool)
        for y in range(n):
            for x in range(n):
                good &= Ts[ar, y, Ts[ar, Ts[ar, Ts[:, y, x], x], x]] == x
        return Ts[good]

    ok("C3: the search is complete -- at orders 2, 3 and 4 it finds every isomorphism class that brute force "
       "finds (3, 8 and 54 classes)",
       all(classes(c3_models(n)) == classes(brute_1312(n)) for n in (2, 3, 4))
       and [len(classes(brute_1312(n))) for n in (2, 3, 4)] == [3, 8, 54])
    for n in (2, 3, 4, 5):
        ok(f"C3: every model of #1312 of order {n} satisfies x = y◇(y◇x), which is not in C3 -- no specimen",
           not c3_models(n, (0, 1)) and not c3_models(n, (0, 0)))
    b6 = c3_models(6, (0, 1)) + c3_models(6, (0, 0))
    low6 = min(len(profile(T)) for T in b6)
    ok(f"C3: at order 6, {len(classes(b6))} magmas (up to renaming) satisfy #1312 and break x = y◇(y◇x) -- smaller "
       f"than the ETP's 8-element witness -- and their profiles have at least {low6} > 14 laws: no specimen",
       low6 > 14 and len(classes(b6)) == 10)
    print("  => smallest orders -- C1, C2: 3. C6, C8: 5. C5, C7: 6 (see verify_4295_type_specimen.py")
    print("     --minimality). C3, C4: at least 7; the smallest known specimen has 32 elements.")

print("\nALL CHECKS PASS.")
