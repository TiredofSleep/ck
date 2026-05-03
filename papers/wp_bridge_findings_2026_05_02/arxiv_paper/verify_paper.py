"""
verify_paper.py — Reproduce every numerical claim in main.tex.

This is a standalone script. It does not depend on the broader handoff
package code. It reproduces the canonical tables inline, then verifies
each theorem, proposition, lemma, and corollary in the paper.

Run:
    python3 verify_paper.py

Returns 0 on full pass, 1 on any failure.

If you don't trust the paper or the script, you can verify the canonical
tables independently against the data DOI:
    https://doi.org/10.5281/zenodo.18852047
The two tables C^B and tilde-C^T should match Definition 2.1 and 2.2 of
the paper.
"""
import sys
from collections import Counter
from itertools import product
import numpy as np

# ============================================================
# CANONICAL TABLES (reproduced inline from the paper)
# ============================================================

# C^B (the arithmetic operation B)
C_B = np.array([
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
    [1, 2, 3, 4, 5, 6, 7, 2, 6, 6],
    [2, 3, 3, 4, 5, 6, 7, 3, 6, 6],
    [3, 4, 4, 4, 5, 6, 7, 4, 6, 6],
    [4, 5, 5, 5, 5, 6, 7, 5, 7, 7],
    [5, 6, 6, 6, 6, 6, 7, 6, 7, 7],
    [6, 7, 7, 7, 7, 7, 7, 7, 7, 7],
    [7, 2, 3, 4, 5, 6, 7, 8, 9, 0],
    [8, 6, 6, 6, 7, 7, 7, 9, 7, 8],
    [9, 6, 6, 6, 7, 7, 7, 0, 8, 0],
])

# tilde-C^T (the geometric operation T's underlying table; T is restricted to I)
C_T_full = np.array([
    [0, 0, 0, 0, 0, 0, 0, 7, 0, 0],
    [0, 7, 3, 7, 7, 7, 7, 7, 7, 7],
    [0, 3, 7, 7, 4, 7, 7, 7, 7, 9],
    [0, 7, 7, 7, 7, 7, 7, 7, 7, 3],
    [0, 7, 4, 7, 7, 7, 7, 7, 8, 7],
    [0, 7, 7, 7, 7, 7, 7, 7, 7, 7],
    [0, 7, 7, 7, 7, 7, 7, 7, 7, 7],
    [7, 7, 7, 7, 7, 7, 7, 7, 7, 7],
    [0, 7, 7, 7, 8, 7, 7, 7, 7, 7],
    [0, 7, 9, 3, 7, 7, 7, 7, 7, 7],
])

# σ permutation
SIGMA = [0, 7, 1, 3, 2, 4, 5, 6, 8, 9]

# Partition Π
FLOW = {1, 3, 5, 7, 9}
STRUCT = {2, 4, 8}
MID = {6}
VOID = {0}

# Geometric domain I
I_DOMAIN = [1, 2, 3, 4, 5, 6, 8, 9]


def role(n):
    if n in FLOW: return 'F'
    if n in STRUCT: return 'S'
    if n in MID: return 'M'
    if n in VOID: return 'V'
    return '?'


# ============================================================
# VERIFICATION INFRASTRUCTURE
# ============================================================

failures = []
passes = []


def check(condition, name, detail=""):
    if condition:
        print(f"  [PASS] {name}")
        passes.append(name)
        return True
    else:
        print(f"  [FAIL] {name}")
        if detail:
            print(f"         {detail}")
        failures.append(name)
        return False


def section(title):
    print(f"\n{'=' * 70}\n{title}\n{'=' * 70}")


# ============================================================
# THEOREM-BY-THEOREM VERIFICATION
# ============================================================

print("=" * 70)
print("VERIFICATION OF main.tex")
print("=" * 70)

# ------------------------------------------------------------
# Section 2: Definitions
# ------------------------------------------------------------
section("Section 2: Definitions and preliminaries")

check(C_B.shape == (10, 10), "C^B is 10x10")
check(np.array_equal(C_B, C_B.T), "C^B is symmetric")
check(C_T_full.shape == (10, 10), "tilde-C^T is 10x10")
check(np.array_equal(C_T_full, C_T_full.T), "tilde-C^T is symmetric")

# Both magmas are non-associative
# B(B(2,4),8) = B(5,8) = 7, B(2,B(4,8)) = B(2,7) = 3
val_left = int(C_B[int(C_B[2, 4]), 8])
val_right = int(C_B[2, int(C_B[4, 8])])
check(val_left == 7 and val_right == 3,
      "B is non-associative at (2,4,8)",
      f"B(B(2,4),8)={val_left}, B(2,B(4,8))={val_right}")

# σ permutation
check(set(SIGMA) == set(range(10)), "σ is a permutation")
fixed = [n for n in range(10) if SIGMA[n] == n]
check(set(fixed) == {0, 3, 8, 9}, "σ-fixed = {0,3,8,9}")

# σ 6-cycle
cycle = [1]
cur = SIGMA[1]
while cur != 1 and len(cycle) < 10:
    cycle.append(cur)
    cur = SIGMA[cur]
check(set(cycle) == {1, 2, 4, 5, 6, 7},
      "σ 6-cycle = {1,2,4,5,6,7}",
      f"got {set(cycle)}")

# Remark 2.4: B and T agreement count on I x I
agree = 0
disagree = 0
for i in I_DOMAIN:
    for j in I_DOMAIN:
        if int(C_B[i, j]) == int(C_T_full[i, j]):
            agree += 1
        else:
            disagree += 1
check(agree == 24 and disagree == 40,
      "B and T agree on 24/64 cells of I x I",
      f"agree={agree}, disagree={disagree}")

# ------------------------------------------------------------
# Section 3: Diagonal successor theorem
# ------------------------------------------------------------
section("Section 3: Diagonal successor theorem")

# Theorem 3.1
expected_diag = {0: 0, 1: 2, 2: 3, 3: 4, 4: 5, 5: 6, 6: 7, 7: 8, 8: 7, 9: 0}
all_pass = True
for n, expected in expected_diag.items():
    actual = int(C_B[n, n])
    if actual != expected:
        all_pass = False
        print(f"    B({n},{n}) = {actual}, expected {expected}")
check(all_pass, "Theorem 3.1: B(n,n) follows the stated successor structure")


# Corollary 3.3: period law
def period(n):
    seen = {n: 0}
    x = n
    for k in range(1, 30):
        x = int(C_B[x, n])
        if x in seen:
            return k - seen[x]
        seen[x] = k
    return None

expected_periods = {0: 1, 1: 6, 2: 5, 3: 4, 4: 3, 5: 2, 6: 1, 7: 4, 8: 3, 9: 2}
all_pass = True
periods = {}
for n in range(10):
    p = period(n)
    periods[n] = p
    if p != expected_periods[n]:
        all_pass = False
        print(f"    π({n}) = {p}, expected {expected_periods[n]}")
check(all_pass, "Corollary 3.3: B-periods match stated values")

# ------------------------------------------------------------
# Section 4: Trefoil characterization
# ------------------------------------------------------------
section("Section 4: Trefoil characterization")

# Theorem 4.1: 9 trefoils, 2 multiset classes
# Runtime processor inlined here (was previously imported from handoff/code/
# trefoil_corrected_frame.py).  Brayden 2026-05-03: arXiv submission requires
# self-contained verification; no external imports beyond stdlib + numpy.

TSML_8_INDICES = [1, 2, 3, 4, 5, 6, 8, 9]
FLOW_CELLS = {0, 7}  # V, H — flow cells between tables
C_T_8 = C_T_full[np.ix_(TSML_8_INDICES, TSML_8_INDICES)]


def _runtime_step_corrected(p, alpha=0.5):
    """One step of the iterated mass-distribution map (paper §2.5)."""
    pt = np.zeros(10)
    pb = np.zeros(10)
    for i in range(10):
        for j in range(10):
            if i not in FLOW_CELLS and j not in FLOW_CELLS:
                i_loc = TSML_8_INDICES.index(i)
                j_loc = TSML_8_INDICES.index(j)
                pt[int(C_T_8[i_loc, j_loc])] += p[i] * p[j]
            pb[int(C_B[i, j])] += p[i] * p[j]
    pt = pt / pt.sum() if pt.sum() > 0 else pt
    pb = pb / pb.sum() if pb.sum() > 0 else pb
    p_new = alpha * pt + (1 - alpha) * pb
    return p_new / p_new.sum() if p_new.sum() > 0 else p_new


def _triple_initial_dist(a, b, c, eps=1e-3):
    p = np.full(10, eps)
    p[a] += 1.0; p[b] += 1.0; p[c] += 1.0
    return p / p.sum()


def _count_crossings(history, mass_threshold=0.01):
    crossings = 0
    for t in range(len(history) - 1):
        p_now, p_next = history[t], history[t + 1]
        rank_now = list(np.argsort(-p_now))
        rank_next = list(np.argsort(-p_next))
        for i in range(10):
            for j in range(i + 1, 10):
                if max(p_now[i], p_next[i]) < mass_threshold: continue
                if max(p_now[j], p_next[j]) < mass_threshold: continue
                pos_i_now, pos_j_now = rank_now.index(i), rank_now.index(j)
                pos_i_nx, pos_j_nx = rank_next.index(i), rank_next.index(j)
                if (pos_i_now < pos_j_now) != (pos_i_nx < pos_j_nx):
                    crossings += 1
    return crossings


def trajectory_corrected(a, b, c, max_iter=50, eps=1e-3, mass_threshold=0.01):
    p = _triple_initial_dist(a, b, c, eps=eps)
    history = [p.copy()]
    for _ in range(max_iter):
        p_new = _runtime_step_corrected(p, alpha=0.5)
        history.append(p_new.copy())
        if np.max(np.abs(p_new - p)) < 1e-8:
            break
        p = p_new
    history = np.array(history)
    return {
        "triple": (a, b, c),
        "crossings": _count_crossings(history, mass_threshold=mass_threshold),
        "iters": len(history),
    }

if trajectory_corrected is not None:
    trefoils = []
    for a, b, c in product(range(10), repeat=3):
        r = trajectory_corrected(a, b, c)
        if r['crossings'] == 3:
            trefoils.append((a, b, c))

    check(len(trefoils) == 9,
          "Theorem 4.1: exactly 9 trefoil triples",
          f"got {len(trefoils)}")

    multisets = Counter(tuple(sorted(t)) for t in trefoils)
    check(set(multisets.keys()) == {(0, 7, 8), (0, 8, 8)},
          "Theorem 4.1: trefoil multisets are {0,7,8} and {0,8,8}")
    check(multisets.get((0, 7, 8)) == 6 and multisets.get((0, 8, 8)) == 3,
          "Theorem 4.1: multiset multiplicities (6 and 3)")

    # B-associativity for each trefoil triple
    all_assoc = True
    for (a, b, c) in trefoils:
        left = int(C_B[int(C_B[a, b]), c])
        right = int(C_B[a, int(C_B[b, c])])
        if left != right:
            all_assoc = False
            print(f"    Non-associative: ({a},{b},{c}): {left} vs {right}")
    check(all_assoc, "Theorem 4.1: all 9 trefoils are B-associative")

    # Lemma 4.2: BREATH-uniqueness
    min_crossings = {2: float('inf'), 4: float('inf'), 8: float('inf')}
    for s in [2, 4, 8]:
        for x in range(10):
            for triple in [(0, s, x), (s, 0, x), (s, x, 0),
                           (0, x, s), (x, 0, s), (x, s, 0)]:
                r = trajectory_corrected(*triple)
                if r['crossings'] < min_crossings[s]:
                    min_crossings[s] = r['crossings']

    check(min_crossings[2] == 26, "Lemma 4.2: min crossings for s=2 is 26",
          f"got {min_crossings[2]}")
    check(min_crossings[4] == 17, "Lemma 4.2: min crossings for s=4 is 17",
          f"got {min_crossings[4]}")
    check(min_crossings[8] == 3, "Lemma 4.2: min crossings for s=8 is 3",
          f"got {min_crossings[8]}")

# ------------------------------------------------------------
# Section 5: Image structure
# ------------------------------------------------------------
section("Section 5: Image structure and role-determinism")

# Theorem 5.1: T image
T_image = set()
for i in I_DOMAIN:
    for j in I_DOMAIN:
        T_image.add(int(C_T_full[i, j]))
check(T_image == {3, 4, 7, 8, 9},
      "Theorem 5.1: T image = {3,4,7,8,9}",
      f"got {T_image}")

# T output role distribution: 60/64 F, 4/64 S
T_role_outputs = Counter()
for i in I_DOMAIN:
    for j in I_DOMAIN:
        T_role_outputs[role(int(C_T_full[i, j]))] += 1
check(T_role_outputs['F'] == 60 and T_role_outputs['S'] == 4,
      "Theorem 5.1: T output distribution (60F, 4S)",
      f"got {dict(T_role_outputs)}")

# B image is full
B_image = set(int(C_B[i, j]) for i in range(10) for j in range(10))
check(B_image == set(range(10)), "Theorem 5.1: B image is full")

# Theorem 5.2: T role-determinism
T_class_outputs = {}
for i in I_DOMAIN:
    for j in I_DOMAIN:
        ri, rj = role(i), role(j)
        ro = role(int(C_T_full[i, j]))
        T_class_outputs.setdefault((ri, rj), set()).add(ro)
det_T = sum(1 for outs in T_class_outputs.values() if len(outs) == 1)
check(det_T == 8 and len(T_class_outputs) == 9,
      "Theorem 5.2(1): T deterministic on 8 of 9 input class pairs",
      f"got {det_T}/{len(T_class_outputs)}")
check(T_class_outputs.get(('S', 'S')) == {'F', 'S'},
      "Theorem 5.2(1): only (S,S) branches, to {F, S}",
      f"got {T_class_outputs.get(('S','S'))}")

# Theorem 5.2(2): B role-determinism
B_class_outputs = {}
for i in range(10):
    for j in range(10):
        ri, rj = role(i), role(j)
        ro = role(int(C_B[i, j]))
        B_class_outputs.setdefault((ri, rj), Counter())
        B_class_outputs[(ri, rj)][ro] += 1

# All non-(F/S × F/S) pairs should be deterministic
boundary_pairs_det = True
for (ri, rj), c in B_class_outputs.items():
    if ri in ('V', 'M') or rj in ('V', 'M'):
        if len(c) > 1:
            boundary_pairs_det = False
            print(f"    Branching at {(ri,rj)}: {dict(c)}")
check(boundary_pairs_det,
      "Theorem 5.2(2): B deterministic on all V/M-touching pairs")

# Branching pairs verified
expected_branching = {('F', 'F'), ('F', 'S'), ('S', 'F'), ('S', 'S')}
actual_branching = set(p for p, c in B_class_outputs.items() if len(c) > 1)
check(actual_branching == expected_branching,
      "Theorem 5.2(2): branching pairs are exactly {FF, FS, SF, SS}",
      f"got {actual_branching}")

# Specific distributions
ff = B_class_outputs[('F', 'F')]
check(ff == Counter({'M': 11, 'S': 9, 'V': 3, 'F': 2}),
      "Theorem 5.2(2): (F,F) distribution (2F, 9S, 11M, 3V)",
      f"got {dict(ff)}")

# ------------------------------------------------------------
# Section 6: Integer invariant decompositions
# ------------------------------------------------------------
section("Section 6: Integer invariant and decompositions")

# Definition 6.1: ψ(n) = -(π(n) - 1)
psi = {n: -(periods[n] - 1) for n in range(10)}
expected_psi = {0: 0, 1: -5, 2: -4, 3: -3, 4: -2, 5: -1, 6: 0, 7: -3, 8: -2, 9: -1}
check(psi == expected_psi, "Definition 6.1: ψ values match")

# Theorem 6.2: total sum = -21
check(sum(psi.values()) == -21,
      "Theorem 6.2: Σψ = -21",
      f"got {sum(psi.values())}")

# Theorem 6.3: σ-orbit decomposition
six_cycle_sum = sum(psi[n] for n in [1, 2, 4, 5, 6, 7])
fixed_sum = sum(psi[n] for n in [0, 3, 8, 9])
check(six_cycle_sum == -15, "Theorem 6.3: σ 6-cycle sum = -15 = -T_5")
check(fixed_sum == -6, "Theorem 6.3: σ-fixed sum = -6 = -T_3")
check(six_cycle_sum + fixed_sum == -21, "Theorem 6.3: decomposition sums to -21")

# Theorem 6.4: partition decomposition
flow_sum = sum(psi[n] for n in FLOW)
struct_sum = sum(psi[n] for n in STRUCT)
mid_sum = sum(psi[n] for n in MID)
void_sum = sum(psi[n] for n in VOID)
check(flow_sum == -13, "Theorem 6.4: flow sum = -13 = -F_7")
check(struct_sum == -8, "Theorem 6.4: structure sum = -8 = -F_6")
check(mid_sum == 0, "Theorem 6.4: middle sum = 0")
check(void_sum == 0, "Theorem 6.4: void sum = 0")
check(flow_sum + struct_sum == -21, "Theorem 6.4: F+S sum = -21 = -F_8")

# ------------------------------------------------------------
# Section 7: Role-quotient magma
# ------------------------------------------------------------
section("Section 7: Role-quotient magma")

# Build mode-based magma
magma = {}
for ri in 'VFSM':
    for rj in 'VFSM':
        outs = []
        for i in range(10):
            for j in range(10):
                if role(i) == ri and role(j) == rj:
                    outs.append(role(int(C_B[i, j])))
        if outs:
            magma[(ri, rj)] = Counter(outs).most_common(1)[0][0]

# Expected table from Section 7
expected_magma = {
    ('V', 'V'): 'V', ('V', 'F'): 'F', ('V', 'S'): 'S', ('V', 'M'): 'M',
    ('F', 'V'): 'F', ('F', 'F'): 'M', ('F', 'S'): 'F', ('F', 'M'): 'F',
    ('S', 'V'): 'S', ('S', 'F'): 'F', ('S', 'S'): 'F', ('S', 'M'): 'F',
    ('M', 'V'): 'M', ('M', 'F'): 'F', ('M', 'S'): 'F', ('M', 'M'): 'F',
}
all_match = all(magma[k] == v for k, v in expected_magma.items())
check(all_match, "Section 7: role-quotient magma matches table")

# Proposition 7.2: V is identity
all_id = all(magma[('V', x)] == x and magma[(x, 'V')] == x for x in 'VFSM')
check(all_id, "Proposition 7.2: V is two-sided identity")

# Proposition 7.2: only V is idempotent
idempotents = [x for x in 'VFSM' if magma[(x, x)] == x]
check(idempotents == ['V'], "Proposition 7.2: V is the only idempotent",
      f"got {idempotents}")

# Proposition 7.2: non-associativity at (F, F, S)
left = magma[(magma[('F', 'F')], 'S')]   # bar_B(bar_B(F,F), S) = bar_B(M,S) = F
right = magma[('F', magma[('F', 'S')])]  # bar_B(F, bar_B(F,S)) = bar_B(F,F) = M
check(left == 'F' and right == 'M' and left != right,
      "Proposition 7.2: non-associative at (F,F,S)",
      f"left={left}, right={right}")

# ------------------------------------------------------------
# Section 8: Limitations
# ------------------------------------------------------------
section("Section 8: Limitations")

# σ-automorphism mismatch
sigma_match = sum(1 for i in range(10) for j in range(10)
                  if int(C_B[SIGMA[i], SIGMA[j]]) == SIGMA[int(C_B[i, j])])
check(sigma_match == 48,
      "σ-automorphism match for B is 48/100 (not 100)",
      f"got {sigma_match}/100")

# Note: Proposition 8.1 (Fibonacci fragility) and Proposition 8.4 (PSL(2,Z)
# lifts) are computational results that take longer to reproduce. They are
# in the handoff package. We do a quick spot check here.

# Random-table spot check (smaller sample for speed)
import random
random.seed(42)


def random_commutative_table(n=10):
    T = np.zeros((n, n), dtype=int)
    for i in range(n):
        for j in range(i, n):
            v = random.randint(0, n - 1)
            T[i, j] = v
            T[j, i] = v
    return T


def role_decomposition(table):
    role_sums = {'F': 0, 'S': 0, 'M': 0, 'V': 0}
    for n in range(10):
        a, x = n, n
        seen = {a: 0}
        period_n = None
        for k in range(1, 20):
            x = int(table[x, n])
            if x in seen:
                period_n = k - seen[x]
                break
            seen[x] = k
        if period_n is None:
            return None
        psi_n = -(period_n - 1)
        if n in FLOW: role_sums['F'] += psi_n
        elif n in STRUCT: role_sums['S'] += psi_n
        elif n in MID: role_sums['M'] += psi_n
        elif n in VOID: role_sums['V'] += psi_n
    return role_sums


fibonacci_count = 0
total_random = 50  # smaller for speed; full Proposition 8.1 used 200
for _ in range(total_random):
    T = random_commutative_table()
    rd = role_decomposition(T)
    if rd is None:
        continue
    if (abs(rd['F']), abs(rd['S'])) == (13, 8):
        fibonacci_count += 1
check(fibonacci_count == 0,
      f"Proposition 8.1 spot check: 0 of {total_random} random tables produce (13,8)",
      f"got {fibonacci_count}/{total_random}")

# ============================================================
# FINAL REPORT
# ============================================================

print(f"\n{'=' * 70}")
print("VERIFICATION SUMMARY")
print('=' * 70)
print(f"\n  Passes:   {len(passes)}")
print(f"  Failures: {len(failures)}")

if failures:
    print("\n  ❌ VERIFICATION FAILED")
    print("  Failed checks:")
    for f in failures:
        print(f"    - {f}")
    print("\n  DO NOT submit to arXiv until all checks pass.")
    sys.exit(1)
else:
    print("\n  ✓ ALL CHECKS PASS")
    print("  Paper's numerical claims are reproducible from canonical tables.")
    sys.exit(0)
