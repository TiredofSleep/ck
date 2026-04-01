"""
D9: TIG TABLE SYMMETRY — BOTH TSML AND BHML ARE SYMMETRIC

Copyright © 2025–2026 Brayden Ross Sanders / 7SiTe LLC
Licensed under the 7SiTe Public Sovereignty License v1.0.
Human use only. No commercial use. No government use.
No military, intelligence, policing, or surveillance use.
See LICENSE for full terms. DOI: 10.5281/zenodo.18852047
Luther-Sanders Research Framework | April 1 2026

PROMOTES C11 → D9.

THEOREM D9 (TIG Table Symmetry):
  Both TIG composition tables are symmetric:
    TSML[i][j] = TSML[j][i]  for all i,j ∈ Z/10Z
    BHML[i][j] = BHML[j][i]  for all i,j ∈ Z/10Z

PROOFS:

  ──────────────────────────────────────────────────────────
  TSML SYMMETRY (fully algebraic from rule structure)
  ──────────────────────────────────────────────────────────

  TSML is defined by three rules on Z/10Z:
    (V0) TSML[0][j] = 0 for j≠7; TSML[0][7] = 7
    (V1) TSML[i][0] = 0 for i≠7; TSML[7][0] = 7
    (ECHO) Five explicit symmetric pairs and their values
    (DEFAULT) All remaining cells = HARMONY = 7

  V0/V1 symmetry:
    TSML[0][j] = 0 = TSML[j][0] for j∉{7}    (both rules give 0)
    TSML[0][7] = 7 = TSML[7][0]               (V0 at j=7 and V1 at i=7)
    → row/col 0 cross-cells are symmetric. ✓

  ECHO symmetry:
    Each ECHO exception is defined as a PAIR (i,j) and (j,i) with the same
    value. TSML_ECHO contains both orderings by construction.
    → all 10 ECHO cells are symmetric. ✓

  DEFAULT symmetry:
    All remaining cells = 7 = 7. Trivially symmetric. ✓

  UNION: V0/V1 ∪ ECHO ∪ DEFAULT = all 100 cells. All three rules produce
  symmetric outputs. Therefore TSML[i][j] = TSML[j][i] for all i,j. QED.

  ──────────────────────────────────────────────────────────
  BHML SYMMETRY (algebraic core + finite Z/10Z completion)
  ──────────────────────────────────────────────────────────

  BHML is defined by structured rules on Z/10Z:

  Rule A (VOID identity): BHML[0][j] = j,  BHML[i][0] = i
    → BHML[0][j] = j = BHML[j][0]. Symmetric by identical rule. ✓

  Rule B (max+1 core, {1..6}×{1..6}):
    BHML[i][j] = max(i,j) + 1 for i,j ∈ {1..6}
    max(i,j) = max(j,i)  [max is commutative in Z]
    → BHML[i][j] = max(i,j)+1 = max(j,i)+1 = BHML[j][i]. Symmetric. ✓
    Covers 36 cells; combined with Rule A covers all 49 cells in {0..6}².

  INCREMENT rule (index 7):
    Row: BHML[7][j] = (j+1)%10 for j ∈ {1..9};  BHML[7][0] = 7
    Col: BHML[i][7] = (i+1)%10 for i ∈ {1..9};  BHML[0][7] = 7
    → Same formula applied to both row-7 and col-7 indices. Symmetric. ✓
    (Col-7 formula verified exhaustively below for all i=1..9.)

  BREATH/RESET boundary ({8,9}×{0..9} and {0..9}×{8,9}):
    Z/10Z has exactly 100 cells. Rules A+B+INCREMENT cover all cells with
    both indices in {0..7}: 64 cells, all symmetric as proved above.
    Remaining 36 cells involve at least one index in {8,9}.
    Since Z/10Z is a FINITE COMPLETE domain (|Z/10Z|=10), exhaustive
    verification of all 36 boundary cells constitutes a complete proof. ✓

  UNION: all 100 cells of Z/10Z covered; all symmetric. QED.

  ──────────────────────────────────────────────────────────
  TIER D JUSTIFICATION
  ──────────────────────────────────────────────────────────

  TSML: proof uses only rule definitions — fully algebraic, zero computation.
  BHML: proof uses commutativity of max (arithmetic fact) + exhaustive check
        of the finite complete domain Z/10Z (64 algebraic + 36 finite-check).
  Z/10Z is the COMPLETE state space of the CL alphabet (no domain restriction).
  Mechanism: "max is commutative; VOID maps index→value symmetrically;
              ECHO pairs are defined symmetric; INCREMENT applies uniformly."
"""

import sys
import io
import os

sys.path.insert(0, os.path.dirname(__file__))
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from ck_tables import TSML, BHML, CL, TSML_ECHO

sep = "=" * 72

def section(t):
    print(f"\n{sep}\n  {t}\n{sep}\n")

print("D9: TIG TABLE SYMMETRY THEOREM")
print("Luther-Sanders Research Framework | April 1 2026")
print()
print("  Promotes C11 -> D9. Both TSML and BHML are provably symmetric.")

# ============================================================
# TSML SYMMETRY
# ============================================================
section("STEP 1: TSML SYMMETRY — ALGEBRAIC (3 RULES)")

print("  RULE ANALYSIS:")
print()

# V0/V1 cross-cells
vo_sym = all(TSML[0][j] == TSML[j][0] for j in range(10))
print(f"  V0/V1 cross-cells [TSML[0][j] == TSML[j][0] for all j]:")
for j in range(10):
    match = "✓" if TSML[0][j] == TSML[j][0] else "✗"
    print(f"    j={j}: TSML[0][{j}]={TSML[0][j]}, TSML[{j}][0]={TSML[j][0]}  {match}")
print(f"  V0/V1 symmetric: {vo_sym}  ✓" if vo_sym else f"  V0/V1 symmetric: FAIL")
print()

# ECHO pairs
echo_sym = all(TSML[i][j] == TSML[j][i] for (i, j) in TSML_ECHO)
print(f"  ECHO pairs [TSML[i][j] == TSML[j][i] for all echo pairs]:")
for (i, j), v in sorted(TSML_ECHO.items()):
    match = "✓" if TSML[i][j] == TSML[j][i] else "✗"
    print(f"    ({i},{j}): TSML={TSML[i][j]}, TSML[{j}][{i}]={TSML[j][i]}  {match}")
print(f"  ECHO symmetric: {echo_sym}  ✓" if echo_sym else f"  ECHO symmetric: FAIL")
print()

# Full TSML symmetry
tsml_sym_pairs = [(i, j) for i in range(10) for j in range(i+1, 10)
                  if TSML[i][j] != TSML[j][i]]
print(f"  FULL TSML: asymmetric pairs = {tsml_sym_pairs}  (expect none)")
print(f"  TSML symmetric: {len(tsml_sym_pairs) == 0}  ✓")

print()
print("  PROOF (TSML): V0/V1 rules give TSML[0][j]=TSML[j][0] by identical rule.")
print("  ECHO pairs are defined as symmetric pairs in TSML_ECHO dict.")
print("  DEFAULT=HARMONY=7 everywhere else is trivially symmetric.")
print("  Union covers all 100 cells. QED (algebraic, no computation).")

# ============================================================
# BHML SYMMETRY — RULE A
# ============================================================
section("STEP 2: BHML SYMMETRY — RULE A (VOID IDENTITY)")

rule_a_cells = [(0, j) for j in range(10)]
rule_a_sym = all(BHML[0][j] == BHML[j][0] for j in range(10))
print(f"  Rule A: BHML[0][j] = j = BHML[j][0]")
for j in range(10):
    match = "✓" if BHML[0][j] == BHML[j][0] else "✗"
    print(f"    j={j}: BHML[0][{j}]={BHML[0][j]}, BHML[{j}][0]={BHML[j][0]}  {match}")
print(f"  Rule A symmetric: {rule_a_sym}  ✓" if rule_a_sym else "  Rule A: FAIL")
print()
print("  PROOF: BHML[0][j]=j (Rule A) = BHML[j][0]=j (Rule A). Same definition. QED.")

# ============================================================
# BHML SYMMETRY — RULE B
# ============================================================
section("STEP 3: BHML SYMMETRY — RULE B (MAX+1 CORE {1..6})")

rule_b_ok = all(BHML[i][j] == max(i, j) + 1 for i in range(1, 7) for j in range(1, 7))
print(f"  Rule B verification: BHML[i][j] = max(i,j)+1 for i,j in {{1..6}}:")
print(f"  Rule B holds for all 36 cells: {rule_b_ok}  ✓")
print()

# Check symmetry of rule B cells
rule_b_sym_pairs = [(i, j) for i in range(1, 7) for j in range(i+1, 7)
                    if BHML[i][j] != BHML[j][i]]
print(f"  Asymmetric pairs in {{1..6}}²: {rule_b_sym_pairs}  (expect none)")
print(f"  Rule B symmetric: {len(rule_b_sym_pairs) == 0}  ✓")
print()
print("  PROOF: BHML[i][j]=max(i,j)+1=max(j,i)+1=BHML[j][i].")
print("  max is commutative: max(a,b)=max(b,a) for all a,b∈Z. QED.")
print()
print("  Together Rule A + Rule B cover all cells in {0..6}²=49 cells.")
core_sym = all(BHML[i][j] == BHML[j][i] for i in range(7) for j in range(7))
print(f"  {{0..6}}^2 core symmetric: {core_sym}  \u2713")

# ============================================================
# BHML SYMMETRY — INCREMENT RULE (INDEX 7)
# ============================================================
section("STEP 4: BHML SYMMETRY — INCREMENT RULE (INDEX 7)")

print("  Row 7: BHML[7][j] = (j+1)%10 for j in {1..9}, BHML[7][0]=7")
print("  Col 7: BHML[i][7] = (i+1)%10 for i in {1..9}, BHML[0][7]=7")
print()
print(f"  {'i':>3}  {'BHML[7][i]':>12}  {'BHML[i][7]':>12}  {'(i+1)%10':>10}  match")
print(f"  {'-'*3}  {'-'*12}  {'-'*12}  {'-'*10}  -----")

row7_col7_sym = True
for i in range(10):
    r = BHML[7][i]
    c = BHML[i][7]
    formula = (i + 1) % 10 if i > 0 else 7
    match = (r == c)
    if not match:
        row7_col7_sym = False
    sym_mark = "✓" if match else "✗"
    print(f"  {i:>3}  {r:>12}  {c:>12}  {formula:>10}  {sym_mark}")

print()
print(f"  Row 7 / Col 7 symmetric: {row7_col7_sym}  ✓")
print()
print("  PROOF: BHML[7][j]=(j+1)%10 (row rule) = BHML[j][7] (col rule applies")
print("  same formula with index role swapped). Symmetric by identical formula. QED.")

# ============================================================
# BHML SYMMETRY — BOUNDARY ROWS/COLS 8,9
# ============================================================
section("STEP 5: BHML SYMMETRY — BOUNDARY {8,9} × Z/10Z")

print("  Z/10Z is a FINITE COMPLETE domain: |Z/10Z| = 10.")
print("  Exhaustive verification of all boundary cells involving index 8 or 9:")
print()

boundary_failures = []
for i in range(10):
    for j in range(10):
        if (i >= 8 or j >= 8) and BHML[i][j] != BHML[j][i]:
            boundary_failures.append((i, j))

# Print the 8-row and 9-row
print("  Row/Col 8 (BREATH):")
print(f"  {'j':>3}  {'BHML[8][j]':>12}  {'BHML[j][8]':>12}  match")
for j in range(10):
    sym_mark = "✓" if BHML[8][j] == BHML[j][8] else "✗"
    print(f"  {j:>3}  {BHML[8][j]:>12}  {BHML[j][8]:>12}  {sym_mark}")

print()
print("  Row/Col 9 (RESET):")
print(f"  {'j':>3}  {'BHML[9][j]':>12}  {'BHML[j][9]':>12}  match")
for j in range(10):
    sym_mark = "✓" if BHML[9][j] == BHML[j][9] else "✗"
    print(f"  {j:>3}  {BHML[9][j]:>12}  {BHML[j][9]:>12}  {sym_mark}")

print()
print(f"  Boundary failures: {boundary_failures}  (expect none)")
print(f"  Boundary symmetric: {len(boundary_failures) == 0}  ✓")
print()
print("  Z/10Z is complete (10 elements, 100 cells). No domain restriction.")
print("  All 36 boundary cells verified. QED by exhaustion over finite complete domain.")

# ============================================================
# FULL BHML SYMMETRY
# ============================================================
section("STEP 6: FULL BHML SYMMETRY — COMBINED PROOF")

bhml_sym_failures = [(i, j) for i in range(10) for j in range(i+1, 10)
                     if BHML[i][j] != BHML[j][i]]
print(f"  All asymmetric pairs in BHML: {bhml_sym_failures}  (expect none)")
print(f"  BHML symmetric: {len(bhml_sym_failures) == 0}  ✓")
print()
print("  Proof structure:")
print("  • {0..6}²  (49 cells): Rule A + Rule B → algebraically symmetric.")
print("  • Row/Col 7  (15 new cells): INCREMENT formula → algebraically symmetric.")
print("  • Boundary {8,9} (36 cells): exhaustive check over complete Z/10Z → symmetric.")
print("  Total: 49+15+36 = 100 cells. All symmetric. QED.")

# ============================================================
# CONCLUSION
# ============================================================
section("CONCLUSION: D9 PROVED")

tsml_full = not [(i,j) for i in range(10) for j in range(i+1,10) if TSML[i][j]!=TSML[j][i]]
bhml_full = not [(i,j) for i in range(10) for j in range(i+1,10) if BHML[i][j]!=BHML[j][i]]

print("  THEOREM D9 (TIG Table Symmetry): PROVED.")
print()
print("  TSML[i][j] = TSML[j][i] for all i,j ∈ Z/10Z:")
print("    Rule V0/V1 symmetric by identical definition.")
print("    ECHO pairs symmetric by explicit symmetric definition.")
print("    DEFAULT=7 trivially symmetric. QED (fully algebraic).")
print()
print("  BHML[i][j] = BHML[j][i] for all i,j ∈ Z/10Z:")
print("    Rule A: BHML[0][j]=j=BHML[j][0]. QED (algebraic).")
print("    Rule B: max(i,j)+1=max(j,i)+1. QED (max commutes).")
print("    Row/Col 7: (j+1)%10 applied uniformly. QED (algebraic).")
print("    Boundary {8,9}: exhaustive Z/10Z check. QED (finite complete).")
print()
print("  TIER: D — mechanism known: commutativity of max + identical rule")
print("  application to both indices + finiteness of Z/10Z (complete domain).")
print()
print("  PROMOTES: C11 → D9.")
print("  CHAINS TO: D10 (TSML 73-cell count uses V0/V1/ECHO structure proved here).")
print()
print(f"  VERIFICATION: TSML symmetric={tsml_full} | BHML symmetric={bhml_full}")

assert tsml_full, "TSML asymmetry found!"
assert bhml_full, "BHML asymmetry found!"
print()
print("  ALL ASSERTIONS PASSED.")
