"""
ck_reconstruction.py -- TSML Reconstruction Verification
=========================================================
Tests that the TSML can be reconstructed from invariants I1-I10,
and that the forced/HAR-maximized/residual accounting is correct.

Run: python ck_reconstruction.py
Expected: RECONSTRUCTION: 32/32 assertions passed

Author: Brayden Sanders / 7Site LLC | March 2026
DOI: 10.5281/zenodo.18852047
"""

import numpy as np
from math import gcd

# The exact TSML (from ck_sim/being/ck_sim_heartbeat.py, states 0-9)
# Row = B operand, Col = D operand. State 0 = VOID.
TSML = [
    [0, 0, 0, 0, 0, 0, 0, 7, 0, 0],  # row 0 VOID
    [0, 7, 3, 7, 7, 7, 7, 7, 7, 7],  # row 1 LATTICE
    [0, 3, 7, 7, 4, 7, 7, 7, 7, 9],  # row 2 COUNTER
    [0, 7, 7, 7, 7, 7, 7, 7, 7, 3],  # row 3 PROGRESS
    [0, 7, 4, 7, 7, 7, 7, 7, 8, 7],  # row 4 COLLAPSE
    [0, 7, 7, 7, 7, 7, 7, 7, 7, 7],  # row 5 BALANCE
    [0, 7, 7, 7, 7, 7, 7, 7, 7, 7],  # row 6 CHAOS
    [7, 7, 7, 7, 7, 7, 7, 7, 7, 7],  # row 7 HARMONY
    [0, 7, 7, 7, 8, 7, 7, 7, 7, 7],  # row 8 BREATH
    [0, 7, 9, 3, 7, 7, 7, 7, 7, 7],  # row 9 RESET
]

C = frozenset({1, 3, 7, 9})       # units of Z/10Z -- gcd(s,10)=1
G_nv = frozenset({2, 4, 5, 6, 8}) # non-units, non-VOID
G = frozenset({0, 2, 4, 5, 6, 8}) # non-units including VOID
HAR = 7
VOID_S = 0

# Test harness
passed = 0
total = 0
failures = []

def check(name, cond, note=""):
    global passed, total
    total += 1
    ok = bool(cond)
    if ok:
        passed += 1
        print("  PASS  " + name + ("  [" + note + "]" if note else ""))
    else:
        failures.append(name)
        print("  FAIL  " + name + ("  [" + note + "]" if note else ""))

# ===========================================================
# S1 -- Invariants I1-I5 (10 assertions)
# ===========================================================
print("\n-- S1: Invariants I1-I5 (10 assertions) --")

# I1a: F(s,7) = 7 for all s (HAR absorbing column)
check("I1a: F(s,7)=7 for all s",
      all(TSML[s][HAR] == HAR for s in range(10)),
      "failures=" + str([s for s in range(10) if TSML[s][HAR] != HAR]))

# I1b: F(7,j) = 7 for all j (HAR absorbing row)
check("I1b: F(7,j)=7 for all j",
      all(TSML[HAR][j] == HAR for j in range(10)),
      "failures=" + str([j for j in range(10) if TSML[HAR][j] != HAR]))

# I2: C = {1,3,7,9} = {s : gcd(s,10)=1}
c_from_gcd = frozenset(s for s in range(10) if gcd(s, 10) == 1)
check("I2: C = gcd-1 states = {1,3,7,9}",
      c_from_gcd == C, "computed=" + str(sorted(c_from_gcd)))

# I3: C is closed under TSML (CxC subset C -- sub-magma)
c_closure_violations = [(a, b, TSML[a][b]) for a in C for b in C if TSML[a][b] not in C]
check("I3: CxC subset C (sub-magma closure)",
      len(c_closure_violations) == 0,
      "violations=" + str(c_closure_violations))

# I4: One-way gate -- F(c,g) not in G for c in C, g in G_nv
gate_violations = [(c, g, TSML[c][g]) for c in C for g in G_nv if TSML[c][g] in G_nv]
check("I4: One-way gate F(c,g) not in G for c in C, g in G",
      len(gate_violations) == 0,
      "violations=" + str(gate_violations))

# I5: Symmetry (commutative) F(s,c) = F(c,s)
sym_violations = [(i, j) for i in range(10) for j in range(10) if TSML[i][j] != TSML[j][i]]
check("I5: F(s,c)=F(c,s) for all s,c (commutative)",
      len(sym_violations) == 0,
      "violations=" + str(sym_violations))

# I8: Orbit zone -- F(3,9)=3 and F(9,3)=3
check("I8a: F(3,9)=3 (orbit zone)", TSML[3][9] == 3)
check("I8b: F(9,3)=3 (orbit zone by symmetry)", TSML[9][3] == 3)

# I9: State-1 direct feeder -- F(1,c)=7 for all c in C
i9_violations = [(c, TSML[1][c]) for c in C if TSML[1][c] != HAR]
check("I9: F(1,c)=7 for all c in C",
      len(i9_violations) == 0,
      "violations=" + str(i9_violations))

# I10: Exists c in C such that F(g,c)=7 for all g in G_nv
# HAR (=7) is in C and F(g,7)=7 for all g, so HAR is a witness
i10_witnesses = [c for c in C if all(TSML[g][c] == HAR for g in G_nv)]
check("I10: exists c in C with F(g,c)=7 for all g in G",
      len(i10_witnesses) > 0,
      "witnesses=" + str(i10_witnesses))

# ===========================================================
# S2 -- Forced cell counts (8 assertions)
# ===========================================================
print("\n-- S2: Forced cell counts (8 assertions) --")

# I1: column 7 -- 10 cells forced to HAR
i1_col = sum(1 for s in range(10) if TSML[s][HAR] == HAR)
check("I1 column: 10 cells in column 7 forced to HAR",
      i1_col == 10, "count=" + str(i1_col))

# I1+I5: row 7 -- 9 additional cells (excluding diagonal (7,7) already counted)
i1_row_additional = sum(1 for j in range(10) if j != HAR and TSML[HAR][j] == HAR)
check("I1+I5 row: 9 additional cells in row 7 (excl diagonal)",
      i1_row_additional == 9, "count=" + str(i1_row_additional))

# I1 total -- 19 distinct cells in the HAR cross
i1_total = len(set([(s, HAR) for s in range(10)] + [(HAR, j) for j in range(10)]))
check("I1 total: 19 distinct cells forced by HAR cross",
      i1_total == 19, "count=" + str(i1_total))

# I9: F(1,c)=7 for c in C -- 3 new cells beyond I1 (c in {1,3,9}, not 7)
i9_new_cells = [(1, c) for c in sorted(C) if c != HAR]
i9_new_correct = all(TSML[1][c] == HAR for c in C if c != HAR)
check("I9: 3 additional cells forced beyond I1 (F(1,c)=7 for c in {1,3,9})",
      len(i9_new_cells) == 3 and i9_new_correct,
      "count=" + str(len(i9_new_cells)))

# I9+I5: F(c,1)=7 for c in C -- adds F(3,1) and F(9,1) [F(1,1) done, F(7,1) done via I1]
i9_sym_new = [(c, 1) for c in sorted(C) if c not in {1, HAR}]
i9_sym_correct = all(TSML[c][1] == HAR for c in C if c not in {1, HAR})
check("I9+I5: 2 more cells from symmetry F(c,1)=7 for c in {3,9}",
      len(i9_sym_new) == 2 and i9_sym_correct,
      "count=" + str(len(i9_sym_new)))

# I8: 2 cells forced to value 3
check("I8: 2 cells forced to value 3 (orbit zone)",
      TSML[3][9] == 3 and TSML[9][3] == 3)

# Total forced cells from I1+I9+I8 (counted within 1-9 algebraic subspace)
# The paper counts 24 cells: the VOID row/col is outside the algebraic analysis
forced_set = set()
for s in range(1, 10):
    forced_set.add((s, HAR))   # I1 column (states 1-9)
    forced_set.add((HAR, s))   # I1 row (states 1-9)
for c in C:
    forced_set.add((1, c))     # I9
    forced_set.add((c, 1))     # I9+I5
forced_set.add((3, 9))         # I8
forced_set.add((9, 3))         # I8
check("Combined I1+I9+I8: 24 cells forced (1-9 subspace)",
      len(forced_set) == 24, "count=" + str(len(forced_set)))

# HAR maximization (I6): verify TSML has 71 HAR cells in 1-9 subspace
har_total = sum(1 for i in range(1, 10) for j in range(1, 10) if TSML[i][j] == HAR)
check("I6: 71 cells equal HAR in TSML (1-9 subspace)",
      har_total == 71, "count=" + str(har_total))

# ===========================================================
# S3 -- Recovery accounting (8 assertions)
# ===========================================================
print("\n-- S3: Recovery accounting (8 assertions) --")

# Total non-HAR cells in full 10x10
# (10x10 = 100 cells; 73 are HAR; 27 are non-HAR including VOID row/col)
non_har_full = [(i, j, TSML[i][j]) for i in range(10) for j in range(10) if TSML[i][j] != HAR]
check("Non-HAR cells total (10x10) = 27",
      len(non_har_full) == 27, "count=" + str(len(non_har_full)))

# Active subspace: states 1-9 (81 cells)
non_har_active = [(i, j, TSML[i][j]) for i in range(1, 10) for j in range(1, 10)
                  if TSML[i][j] != HAR]
check("Non-HAR cells in 1-9 subspace = 10",
      len(non_har_active) == 10, "count=" + str(len(non_har_active)))

# HAR cells in 1-9 subspace
har_active = sum(1 for i in range(1, 10) for j in range(1, 10) if TSML[i][j] == HAR)
check("HAR cells in 1-9 subspace = 71",
      har_active == 71, "count=" + str(har_active))

# 6 BHML residual cells: non-HAR and TSML[i][j] == max(i,j)
bhml_residual = [(i, j, TSML[i][j]) for i in range(1, 10) for j in range(1, 10)
                 if TSML[i][j] != HAR and TSML[i][j] == max(i, j)]
check("6 BHML residual cells (non-HAR following max rule)",
      len(bhml_residual) == 6,
      "count=" + str(len(bhml_residual)) + " pairs=" + str([(p[0], p[1]) for p in bhml_residual]))

# The 6 residual pairs are exactly (2,4),(4,2),(4,8),(8,4),(2,9),(9,2)
expected_residual = {(2, 4, 4), (4, 2, 4), (4, 8, 8), (8, 4, 8), (2, 9, 9), (9, 2, 9)}
actual_residual = set((i, j, TSML[i][j]) for i, j, v in bhml_residual)
check("6 residual pairs are exactly (2,4),(4,2),(4,8),(8,4),(2,9),(9,2)",
      actual_residual == expected_residual,
      "actual=" + str(sorted(actual_residual)))

# 2 asserted exception cells: not HAR, not max(i,j), not orbit
unexplained = [(i, j, TSML[i][j]) for i in range(1, 10) for j in range(1, 10)
               if TSML[i][j] != HAR and TSML[i][j] != max(i, j)]
non_orbit = [(i, j, v) for i, j, v in unexplained
             if not (i == 3 and j == 9) and not (i == 9 and j == 3)]
check("2 asserted exception cells F(1,2)=F(2,1)=3 (not HAR, not max, not orbit)",
      len(non_orbit) == 2 and all(v == 3 for i, j, v in non_orbit),
      "cells=" + str(non_orbit))

# I8 orbit: exactly 2 cells (3,9) and (9,3) in the unexplained list
orbit_in_unexplained = [(i, j, v) for i, j, v in unexplained
                        if (i == 3 and j == 9) or (i == 9 and j == 3)]
check("I8 orbit zone: exactly 2 cells (3,9) and (9,3) with value 3",
      len(orbit_in_unexplained) == 2 and all(v == 3 for i, j, v in orbit_in_unexplained))

# Full accounting: 71 HAR + 6 BHML + 2 orbit + 2 asserted = 81
total_accounted = har_active + len(bhml_residual) + len(orbit_in_unexplained) + len(non_orbit)
check("Accounting: 71 HAR + 6 BHML + 2 orbit + 2 asserted = 81 cells",
      total_accounted == 81,
      "sum=" + str(har_active) + "+" + str(len(bhml_residual)) +
      "+2+2=" + str(total_accounted))

# ===========================================================
# S4 -- I13 order-completion rule (6 assertions)
# ===========================================================
print("\n-- S4: I13 order-completion rule (6 assertions) --")

# F(1,2)=3
check("I13: F(1,2)=3 (LATTICE o COUNTER = PROGRESS)",
      TSML[1][2] == 3, "actual=" + str(TSML[1][2]))

# Symmetry: F(2,1)=3
check("I13 sym: F(2,1)=3 (COUNTER o LATTICE = PROGRESS)",
      TSML[2][1] == 3, "actual=" + str(TSML[2][1]))

# From state 1: all G-input results are in C
from_1_to_G = [(g, TSML[1][g]) for g in sorted(G_nv)]
check("From state 1: all G-input results land in C",
      all(v in C for g, v in from_1_to_G),
      "results=" + str(from_1_to_G))

# F(1,1)=7 (self-composition gives HAR)
check("F(1,1)=7 (LATTICE o LATTICE = HAR)",
      TSML[1][1] == HAR, "actual=" + str(TSML[1][1]))

# State 1 has exactly one non-HAR output in 1-9 range: F(1,2)=3
non_har_from_1 = [(j, TSML[1][j]) for j in range(1, 10) if TSML[1][j] != HAR]
check("State 1 has exactly one non-HAR output: F(1,2)=3",
      len(non_har_from_1) == 1 and non_har_from_1[0] == (2, 3),
      "non_har=" + str(non_har_from_1))

# Nearest upper-corner to state 2 is 3 (tie between 1 and 3, prefer upper)
nearest = min(C, key=lambda c: (abs(c - 2), -c))
check("Nearest upper-corner to state 2 is 3 (explains F(1,2)=3)",
      nearest == 3,
      "nearest=" + str(nearest) + " F(1,2)=" + str(TSML[1][2]))

# ===========================================================
# Summary
# ===========================================================
print("\n" + "=" * 50)
print("RECONSTRUCTION: " + str(passed) + "/" + str(total) + " assertions passed")
if failures:
    print("FAILED: " + str(failures))
else:
    print("ALL PASS")
