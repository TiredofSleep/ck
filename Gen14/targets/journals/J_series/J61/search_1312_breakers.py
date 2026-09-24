#!/usr/bin/env python3
"""search_1312_breakers.py -- every model of #1312, x = y◇(((y◇x)◇x)◇x), of order n that breaks
x = y◇(y◇x), with its ETP profile. A type specimen of C3 must break that law, so this bounds the smallest
specimen from below.

    python search_1312_breakers.py 6            # seconds: 10 models up to renaming, profiles >= 29
    python search_1312_breakers.py 7 16         # order 7 on 16 processes

Needs only numpy. In a finite model of #1312 every row of the table is a permutation (x = y◇(...) makes
each left multiplication onto, hence one-to-one). A model that breaks x = y◇(y◇x) at (y, x) can be
renamed so that y = 0, and x = 1 (or x = 0 if x = y). The search fixes that witness, then uses the
least-number heuristic and propagation; it is split into subproblems that run in parallel.
"""
import itertools
import sys
import time
from multiprocessing import Pool

import numpy as np


# ---------------------------------------------------------------- the ETP catalog (as in verify_j61_closures.py)

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


def ev(t, T, env):
    return env[t] if isinstance(t, int) else T[ev(t[0], T, env), ev(t[1], T, env)]


LAWS, GRIDS = None, {}


def profile_size(T):
    """the number of catalog laws the table satisfies (the catalog is built once per process)"""
    global LAWS
    if LAWS is None:
        LAWS = [(l, r, max(leaves(l) + leaves(r)) + 1) for l, r in build_catalog()]
    T = np.asarray(T)
    n = len(T)
    if n not in GRIDS:
        GRIDS[n] = {k: [g.ravel() for g in np.indices((n,) * k)] for k in range(1, 7)}
    g = GRIDS[n]
    return sum(np.array_equal(ev(l, T, g[k]), ev(r, T, g[k])) for l, r, k in LAWS)


def canonical(T):
    T = np.asarray(T)
    n = len(T)
    perms = np.array(list(itertools.permutations(range(n))))
    inv = np.argsort(perms, axis=1)
    B = perms[np.arange(len(perms))[:, None, None], T[inv[:, :, None], inv[:, None, :]]].reshape(len(perms), n * n)
    return tuple(B[np.lexsort(B.T[::-1])[0]])


# ---------------------------------------------------------------- the search

class Search:
    def __init__(self, n, w):
        self.n, self.w = n, w                      # witness: 0◇(0◇w) != w
        self.T, self.inv, self.cnt = [-1] * n * n, [-1] * n * n, [0] * n
        self.order = sorted(range(n * n), key=lambda c: (max(divmod(c, n)), c))
        self.trail, self.found, self.nodes = [], [], 0

    def assign(self, cell, v, queue):
        n, T, inv = self.n, self.T, self.inv
        y, col = divmod(cell, n)
        if T[cell] >= 0:
            return T[cell] == v
        if inv[y * n + v] >= 0:
            return False
        T[cell], inv[y * n + v] = v, col
        self.cnt[y] += 1
        self.trail.append(cell)
        queue.extend((yy, col) for yy in range(n))
        queue.append((y, v))
        if self.cnt[y] == n - 1:
            c = next(c for c in range(n) if T[y * n + c] < 0)
            return self.assign(y * n + c, next(u for u in range(n) if inv[y * n + u] < 0), queue)
        return True

    def propagate(self, queue):
        n, T, inv = self.n, self.T, self.inv
        while queue:
            y, x = queue.pop()
            a = T[y * n + x]
            b = T[a * n + x] if a >= 0 else -1
            c = T[b * n + x] if b >= 0 else -1
            if b >= 0 and c < 0 and inv[y * n + x] >= 0:
                if not self.assign(b * n + x, inv[y * n + x], queue):
                    return False
            elif c >= 0 and not self.assign(y * n + c, x, queue):
                return False
        return not (T[self.w] >= 0 and T[T[self.w]] == self.w)

    def undo(self, mark):
        n, T = self.n, self.T
        while len(self.trail) > mark:
            cell = self.trail.pop()
            self.inv[cell // n * n + T[cell]] = -1
            T[cell] = -1
            self.cnt[cell // n] -= 1

    def start(self):
        return self.propagate([(y, x) for y in range(self.n) for x in range(self.n)])

    def replay(self, path):
        for cell, v in path:
            q = []
            if not (self.assign(cell, v, q) and self.propagate(q)):
                return False
        return True

    def search(self, path, depth_limit=None, frontier=None):
        n = self.n
        self.nodes += 1
        cell = next((c for c in self.order if self.T[c] < 0), None)
        if cell is None:
            self.found.append(tuple(self.T))
            return
        if depth_limit is not None and len(path) == depth_limit:
            frontier.append(list(path))
            return
        m = max([self.w] + [max(*divmod(c, n), self.T[c]) for c in self.trail])
        i, j = divmod(cell, n)
        for v in range(min(n - 1, max(m, i, j) + 1) + 1):
            mark, q = len(self.trail), []
            if self.assign(cell, v, q) and self.propagate(q):
                path.append((cell, v))
                self.search(path, depth_limit, frontier)
                path.pop()
            self.undo(mark)


def work(args):
    n, w, path = args
    s = Search(n, w)
    if not (s.start() and s.replay(path)):
        return [], 0
    s.search(list(path))
    return s.found, s.nodes


if __name__ == "__main__":
    n = int(sys.argv[1])
    workers = int(sys.argv[2]) if len(sys.argv) > 2 and sys.argv[2].isdigit() else 1
    save = sys.argv[sys.argv.index("--save") + 1] if "--save" in sys.argv else None
    t0 = time.time()
    found, nodes = [], 0
    for w in (1, 0):
        s = Search(n, w)
        frontier = []
        if s.start():
            s.search([], depth_limit=7 if n >= 7 else 3, frontier=frontier)
        found += s.found
        nodes += s.nodes
        with Pool(workers) as pool:
            for k, (f, nd) in enumerate(pool.imap_unordered(work, [(n, w, p) for p in frontier]), 1):
                found += f
                nodes += nd
                if k % max(1, len(frontier) // 10) == 0:
                    print(f"  witness (0, {w}): {k}/{len(frontier)} subproblems, {nodes:,} nodes, "
                          f"{time.time() - t0:.0f}s", flush=True)
    with Pool(workers) as pool:
        classes = sorted(set(pool.map(canonical, [np.array(t).reshape(n, n) for t in found], chunksize=64)))
    print(f"order {n}: {len(found)} tables found, {len(classes)} up to renaming ({nodes:,} nodes, "
          f"{time.time() - t0:.0f}s)", flush=True)
    if save:
        np.save(save, np.array(classes, dtype=np.int8).reshape(-1, n, n))
    if classes:
        assert len(build_catalog()) == 4694
        with Pool(workers) as pool:
            sizes = pool.map(profile_size, [np.array(c).reshape(n, n) for c in classes], chunksize=8)
        print(f"  their ETP profiles have {min(sizes)} to {max(sizes)} laws; C3 has 14, so "
              + ("none of them is a type specimen" if min(sizes) > 14 else "SOME ARE TYPE SPECIMENS"))
        print("  the smallest profiles belong to:")
        low = [c for c, z in zip(classes, sizes) if z == min(sizes)][:3]
        for c in low:
            print("   ", np.array(c).reshape(n, n).tolist())
