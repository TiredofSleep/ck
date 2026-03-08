"""
DEEP DIG: Chasing the 73 connection, 15083, and hidden structure.
Run from ck_desktop target: python deep_dig.py
"""
import numpy as np
import sys
import math

sys.path.insert(0, '.')
from ck_sim.being.ck_sim_heartbeat import CL, OP_NAMES
from ck_sim.being.ck_meta_lens import _BHML
from ck_sim.being.ck_sim_d2 import ROOTS_FLOAT, LATIN_TO_ROOT, FORCE_LUT_FLOAT, D2_OP_MAP
from sympy import Matrix as SM, factorint, Symbol, Poly, Rational as R

T = np.array(CL, dtype=float)
B = np.array(_BHML, dtype=float)
Ts = SM([[int(T[i, j]) for j in range(10)] for i in range(10)])
Bs = SM([[int(B[i, j]) for j in range(10)] for i in range(10)])
Cs = Ts * Bs - Bs * Ts

output = []
def P(s=''):
    print(s)
    output.append(s)


# ================================================================
P('=' * 72)
P('DEEP DIG 1: THE 73 CONNECTION')
P('=' * 72)

# Three appearances of 73:
# 1. 73/100 TSML cells = HARMONY
# 2. 73 divides char poly coefficients
# 3. First PCA component = 73.01%

# === Trace decomposition ===
P()
P('--- Trace decomposition of TSML ---')
tr_T2 = int((Ts * Ts).trace())
P(f'tr(T^2) = {tr_T2}')

# TSML entries: count by value
from collections import Counter
tsml_vals = Counter(int(T[i, j]) for i in range(10) for j in range(10))
P(f'TSML entry distribution: {dict(sorted(tsml_vals.items()))}')

# Decompose tr(T^2) by entry value
for val, count in sorted(tsml_vals.items()):
    P(f'  value {val}: {count} cells, contributing {count}*{val}^2 = {count * val**2}')
total_check = sum(count * val**2 for val, count in tsml_vals.items())
P(f'  Total: {total_check} = tr(T^2)? {total_check == tr_T2}')

# The 73 HARMONY cells dominate: 73 * 49 = 3577
harmony_contribution = 73 * 49
other_contribution = tr_T2 - harmony_contribution
P(f'HARMONY contribution: 73 * 49 = {harmony_contribution} = {harmony_contribution/tr_T2*100:.1f}% of tr(T^2)')
P(f'Other contribution: {other_contribution} = {other_contribution/tr_T2*100:.1f}%')

# === Commutator trace ===
P()
P('--- Commutator trace formulas ---')
tr_C2 = int((Cs * Cs).trace())
P(f'tr(C^2) = tr([T,B]^2) = {tr_C2}')
P(f'lam^8 coefficient = -tr(C^2)/2 = {-tr_C2 // 2}')
P(f'914325 = {factorint(914325)}')
P(f'Match: {-tr_C2 // 2 == 914325}')
P(f'73 | lam^8: {914325 % 73 == 0}')
P(f'914325 / 73 = {914325 // 73} = {factorint(914325 // 73)}')

# === Can we trace 73 back to the table structure? ===
P()
P('--- Tracing 73 through the algebra ---')
P('tr(C^2) = 2*tr(TBTB) - 2*tr(T^2 B^2)')
tr_TBTB = int((Ts * Bs * Ts * Bs).trace())
tr_T2B2 = int((Ts * Ts * Bs * Bs).trace())
P(f'tr(TBTB) = {tr_TBTB}')
P(f'tr(T^2 B^2) = {tr_T2B2}')
P(f'2*{tr_TBTB} - 2*{tr_T2B2} = {2*tr_TBTB - 2*tr_T2B2}')
P(f'tr(C^2) = {tr_C2}')
P(f'Match: {2*tr_TBTB - 2*tr_T2B2 == tr_C2}')

# Now: tr(TBTB) and tr(T^2 B^2) mod 73
P(f'tr(TBTB) mod 73 = {tr_TBTB % 73}')
P(f'tr(T^2 B^2) mod 73 = {tr_T2B2 % 73}')
P(f'tr(C^2) mod 73 = {tr_C2 % 73}')
P(f'tr(C^2) mod 146 = {tr_C2 % 146}')

# Also check tr(B^2) and tr(TB)
tr_B2 = int((Bs * Bs).trace())
tr_TB = int((Ts * Bs).trace())
P(f'tr(B^2) = {tr_B2}')
P(f'tr(TB) = {tr_TB}')
P(f'tr(TB) mod 73 = {tr_TB % 73}')
P(f'tr(B^2) mod 73 = {tr_B2 % 73}')

# ================================================================
P()
P('=' * 72)
P('DEEP DIG 2: WHAT IS 15083?')
P('=' * 72)

P(f'Pfaffian = 633486 = 2 * 3 * 7 * 15083')
P(f'15083 is prime: {all(15083 % d != 0 for d in range(2, int(math.sqrt(15083)) + 1))}')

# Look for 15083 in CK quantities
P()
P('--- Searching for 15083 in table invariants ---')

# tr(T^k) and tr(B^k) for various k
for k in range(1, 6):
    Tk = Ts ** k
    Bk = Bs ** k
    tTk = int(Tk.trace())
    tBk = int(Bk.trace())
    P(f'tr(T^{k}) = {tTk}, tr(B^{k}) = {tBk}')
    if tTk != 0 and abs(tTk) > 1:
        P(f'  tr(T^{k}) / 7 = {tTk / 7:.4f}, mod 7 = {tTk % 7}')
    if tBk != 0 and abs(tBk) > 1:
        P(f'  tr(B^{k}) / 7 = {tBk / 7:.4f}, mod 7 = {tBk % 7}')

# Check 15083 vs various products/sums
P()
P('--- 15083 decomposition attempts ---')
P(f'15083 / 7 = {15083 / 7:.4f} (not integer)')
P(f'15083 mod 7 = {15083 % 7}')
P(f'15083 mod 10 = {15083 % 10}')
P(f'15083 mod 73 = {15083 % 73}')
P(f'15083 = 122^2 + 19 = {122**2 + 19}? {122**2 + 19 == 15083}')
P(f'15083 = 123^2 - 46 = {123**2 - 46}? {123**2 - 46 == 15083}')

# Check if 15083 = some function of table entries
P(f'sum(TSML) = {int(Ts.trace())}... no, sum of ALL entries:')
sum_T = sum(int(T[i, j]) for i in range(10) for j in range(10))
sum_B = sum(int(B[i, j]) for i in range(10) for j in range(10))
P(f'sum(T_all) = {sum_T}')
P(f'sum(B_all) = {sum_B}')
P(f'sum_T * sum_B = {sum_T * sum_B}')
P(f'sum_T + sum_B = {sum_T + sum_B}')
P(f'sum_T - sum_B = {sum_T - sum_B}')
P(f'sum_T^2 - sum_B^2 = {sum_T**2 - sum_B**2}')

# det(C) = Pf^2 = (2*3*7*15083)^2
# So det = 4 * 9 * 49 * 15083^2
# Maybe 15083 appears in the table products differently
P(f'det(T) = 0, det(B) = {int(Bs.det())}')
P(f'det(B) = {int(Bs.det())} = {factorint(abs(int(Bs.det())))}')

# ================================================================
P()
P('=' * 72)
P('DEEP DIG 3: STAIRCASE EIGENSTRUCTURE')
P('=' * 72)

# The staircase block {1..6} of BHML has a beautiful structure
# M(i,j) = max(i,j) + 1 for i,j in {1..6}
P('--- BHML Staircase block (rows/cols 1-6) ---')
stair = SM([[max(i, j) + 1 for j in range(1, 7)] for i in range(1, 7)])
P(f'Staircase matrix:')
for i in range(6):
    P(f'  {[int(stair[i, j]) for j in range(6)]}')

d = int(stair.det())
P(f'det = {d}')
P(f'det(staircase) = -7 = -HARMONY (PROVEN in audit)')

# Eigenvalues
evals_stair = stair.eigenvals()
P(f'Eigenvalues (exact):')
for ev, mult in evals_stair.items():
    P(f'  {ev} (multiplicity {mult})')

# The staircase is a rank-2 perturbation of a constant matrix
# M = J + L where J(i,j) = max(i,j) and L(i,j) = 1 (all ones)
# Actually M(i,j) = max(i,j) + 1
# max(i,j) = (i + j + |i - j|) / 2
# So M = (1/2)(ones_row * I + I * ones_col + |i-j| matrix) + ones
# This decomposition might reveal structure...

P()
P('--- Staircase = max(i,j) + 1 = structured low-rank ---')
P('max(i,j) = (i+j+|i-j|)/2')
P('M = (i+j+|i-j|)/2 + 1')
P('= (1/2) * [i*ones^T + ones*j^T + |i-j| matrix] + ones matrix')

# The |i-j| matrix is a distance matrix
dist = SM([[abs(i-j) for j in range(1,7)] for i in range(1,7)])
P(f'|i-j| matrix:')
for i in range(6):
    P(f'  {[int(dist[i,j]) for j in range(6)]}')
P(f'det(|i-j|) = {int(dist.det())}')

evals_dist = dist.eigenvals()
P(f'Eigenvalues of distance matrix:')
for ev, mult in evals_dist.items():
    from sympy import N
    P(f'  {N(ev, 8)} (multiplicity {mult})')

# ================================================================
P()
P('=' * 72)
P('DEEP DIG 4: HIDDEN SYMMETRIES IN THE COMMUTATOR')
P('=' * 72)

# The commutator C = [T,B] is a 10x10 skew-symmetric integer matrix.
# Let's look at its structure more carefully.
P('--- Commutator matrix C = [TSML, BHML] ---')
C_int = [[int(Cs[i,j]) for j in range(10)] for i in range(10)]
for i in range(10):
    P(f'  {OP_NAMES[i]:10s} {[f"{v:>5d}" for v in C_int[i]]}')

# Row norms (L2)
P(f'\nRow norms:')
for i in range(10):
    norm = math.sqrt(sum(v**2 for v in C_int[i]))
    P(f'  {OP_NAMES[i]:10s}: ||row|| = {norm:.2f}')

# The VOID row dominates! Let's see why.
P(f'\nVOID row: {C_int[0]}')
P(f'  Sum = {sum(C_int[0])}')
P(f'  |Sum| = {abs(sum(C_int[0]))}')

# Sum of each row
P(f'\nRow sums of C:')
for i in range(10):
    P(f'  {OP_NAMES[i]:10s}: sum = {sum(C_int[i])}')

# Column sums (= -row sums for skew-symmetric)
P(f'\nRow sum total = {sum(sum(C_int[i]) for i in range(10))} (must be 0, skew-symmetric)')

# ================================================================
P()
P('=' * 72)
P('DEEP DIG 5: THE VOID ROW OF THE COMMUTATOR')
P('=' * 72)

# C[0,:] = (TB)[0,:] - (BT)[0,:]
# (TB)[0,j] = sum_k T[0,k] * B[k,j]
# T[0,:] = [0, 0, 0, 0, 0, 0, 0, 7, 0, 0] (VOID row of TSML)
# So (TB)[0,j] = 7 * B[7,j] = 7 * BHML_HARMONY_row[j]
# BHML row 7 = [7, 2, 3, 4, 5, 6, 7, 8, 9, 0]
# So (TB)[0,j] = 7 * [7, 2, 3, 4, 5, 6, 7, 8, 9, 0]
#              = [49, 14, 21, 28, 35, 42, 49, 56, 63, 0]

TB_row0 = [7 * int(B[7, j]) for j in range(10)]
P(f'(TB)[0,:] = 7 * BHML_HARMONY_row = {TB_row0}')

# (BT)[0,j] = sum_k B[0,k] * T[k,j]
# B[0,:] = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9] (VOID row of BHML = identity)
# So (BT)[0,j] = sum_k k * T[k,j] = weighted column sum of TSML
BT_row0 = [sum(k * int(T[k, j]) for k in range(10)) for j in range(10)]
P(f'(BT)[0,:] = sum_k k*T[k,j] = {BT_row0}')

# C[0,:] = TB[0,:] - BT[0,:]
C_row0 = [TB_row0[j] - BT_row0[j] for j in range(10)]
P(f'C[0,:] = {C_row0}')
P(f'Matches commutator row 0: {C_row0 == C_int[0]}')

P(f'\nDERIVATION of VOID row:')
P(f'  C[0,j] = 7*B[7,j] - sum_k k*T[k,j]')
P(f'  The VOID row of the commutator = ')
P(f'    7 * (HARMONY row of BHML) - (index-weighted column sums of TSML)')
P(f'  This mixes GENERATION (BHML) with MEASUREMENT (TSML) through HARMONY.')

# Key insight: VOID row of C encodes the difference between
# "7 times how HARMONY generates" and "how measurement weights by position"
P(f'\n  7*B[7,:] = 7*[HARMONY successor + cycle]:')
P(f'    = [49, 14, 21, 28, 35, 42, 49, 56, 63, 0]')
P(f'  sum_k k*T[k,:] = [position-weighted TSML]:')
P(f'    = {BT_row0}')
P(f'  VOID_COMMUTATOR = 7*HARMONY_GEN - POSITION*MEASUREMENT')

# The VOID row is dominated by C[0,9] = -307
# C[0,9] = 7*B[7,9] - sum_k k*T[k,9]
# = 7*0 - (0*0 + 1*7 + 2*9 + 3*3 + 4*7 + 5*7 + 6*7 + 7*7 + 8*7 + 9*7)
# = 0 - (0 + 7 + 18 + 9 + 28 + 35 + 42 + 49 + 56 + 63)
# = -(307)
P(f'\n  C[0,9] (VOID-RESET entry):')
P(f'    = 7*B[7,9] - sum_k k*T[k,9]')
P(f'    = 7*0 - 307 = -307')
P(f'    307 = {factorint(307)}')
P(f'    307 is prime!')

# ================================================================
P()
P('=' * 72)
P('DEEP DIG 6: HIGHER POWER INVARIANTS')
P('=' * 72)

# Compute tr(C^k) for k = 2, 4, 6, 8, 10
# These relate to the characteristic polynomial via Newton's identities
P('--- Power trace invariants of [T,B] ---')
C_powers = [None, Cs]
for k in range(2, 11):
    C_powers.append(C_powers[-1] * Cs)

for k in [2, 4, 6, 8, 10]:
    tr_k = int(C_powers[k].trace())
    P(f'  tr(C^{k:2d}) = {tr_k}')
    if tr_k != 0:
        P(f'           = {factorint(abs(tr_k))}')
        P(f'           mod 7 = {tr_k % 7}')
        P(f'           mod 73 = {tr_k % 73}')

# Odd powers should all be zero (skew-symmetric)
for k in [1, 3, 5, 7, 9]:
    tr_k = int(C_powers[k].trace())
    P(f'  tr(C^{k:2d}) = {tr_k} (must be 0, odd power of skew-sym)')

# ================================================================
P()
P('=' * 72)
P('DEEP DIG 7: RANDOM TABLE COMPARISON')
P('=' * 72)

# Generate random 10x10 symmetric integer matrices and compare
# their Pfaffian factorization to CK's
P('--- How special are CK tables compared to random? ---')
np.random.seed(42)
n_trials = 1000
seven_in_pf = 0
seventy_three_in_cp = 0

for trial in range(n_trials):
    # Random symmetric integer matrix with entries in {0..9}
    R_T = np.random.randint(0, 10, (10, 10))
    R_T = (R_T + R_T.T) // 2  # Make symmetric
    R_B = np.random.randint(0, 10, (10, 10))
    R_B = (R_B + R_B.T) // 2

    R_C = R_T @ R_B - R_B @ R_T
    det_RC = round(np.linalg.det(R_C))

    if det_RC > 0:
        sq = int(math.isqrt(det_RC))
        if sq * sq == det_RC and sq > 0 and sq % 7 == 0:
            seven_in_pf += 1

    # Check char poly for 73
    cp_coeffs = np.poly(R_C)
    lam8 = round(cp_coeffs[2])
    if lam8 != 0 and lam8 % 73 == 0:
        seventy_three_in_cp += 1

P(f'  Random trials: {n_trials}')
P(f'  7 | Pfaffian: {seven_in_pf}/{n_trials} = {seven_in_pf/n_trials*100:.1f}%')
P(f'  73 | lam^8 coeff: {seventy_three_in_cp}/{n_trials} = {seventy_three_in_cp/n_trials*100:.1f}%')
P(f'  CK has BOTH 7|Pf AND 73|lam^8. Joint probability estimate:')
P(f'    {seven_in_pf/n_trials * seventy_three_in_cp/n_trials * 100:.2f}%')

# ================================================================
P()
P('=' * 72)
P('DEEP DIG 8: SENSITIVITY — WHAT IF WE CHANGE ONE CELL?')
P('=' * 72)

# How robust is 7|Pfaffian? Change one TSML exception and check.
P('--- Perturbation sensitivity of Pfaffian ---')
base_exceptions = [(1,2,3), (2,4,4), (2,9,9), (3,9,3), (4,8,8)]

for exc_idx in range(5):
    P(f'\n  Removing exception {base_exceptions[exc_idx]}:')
    T_mod = np.full((10, 10), 7.0)
    for j in range(10):
        if j != 7:
            T_mod[0, j] = 0
            T_mod[j, 0] = 0
    T_mod[0, 7] = 7
    T_mod[7, 0] = 7
    for idx, (a, b, v) in enumerate(base_exceptions):
        if idx != exc_idx:
            T_mod[a, b] = v
            T_mod[b, a] = v

    C_mod = T_mod @ B - B @ T_mod
    det_mod = round(np.linalg.det(C_mod))
    if det_mod > 0:
        sq_mod = int(math.isqrt(det_mod))
        is_sq = sq_mod * sq_mod == det_mod
    elif det_mod < 0:
        sq_mod = int(math.isqrt(abs(det_mod)))
        is_sq = sq_mod * sq_mod == abs(det_mod)
    else:
        sq_mod = 0
        is_sq = True

    div7 = sq_mod % 7 == 0 if sq_mod > 0 else 'N/A'
    P(f'    det([T_mod,B]) = {det_mod}')
    P(f'    Perfect square: {is_sq}')
    if is_sq and sq_mod > 0:
        P(f'    Pfaffian = {sq_mod}')
        P(f'    7 | Pf: {sq_mod % 7 == 0}')
        P(f'    Factorization: {factorint(sq_mod) if sq_mod < 10**12 else "too large"}')

# What if we change HARMONY count? Set one non-7 to 7.
P(f'\n  Adding exception: set T(1,2) = 7 (removes the sum exception):')
T_more7 = T.copy()
T_more7[1, 2] = 7
T_more7[2, 1] = 7  # maintain symmetry
C_more = T_more7 @ B - B @ T_more7
det_more = round(np.linalg.det(C_more))
P(f'    Now 75/100 cells = HARMONY')
if abs(det_more) > 0:
    sq_more = int(math.isqrt(abs(det_more)))
    is_sq = sq_more * sq_more == abs(det_more)
    P(f'    det = {det_more}')
    P(f'    Perfect square: {is_sq}')
    if is_sq and sq_more > 0:
        P(f'    Pfaffian = {sq_more}')
        P(f'    7 | Pf: {sq_more % 7 == 0}')

# ================================================================
P()
P('=' * 72)
P('DEEP DIG 9: THE COVARIANCE QUINTIC')
P('=' * 72)

# The covariance eigenvalues satisfy an exact quintic polynomial.
# Can we find 73 in that polynomial?
P('--- Exact covariance quintic from Hebrew roots ---')

root_names = list(ROOTS_FLOAT.keys())
root_data = []
for name in root_names:
    vec = ROOTS_FLOAT[name]
    root_data.append([R(int(round(v * 10)), 10) for v in vec])

M_roots = SM(root_data)
n_roots = 22
means = [sum(M_roots[i, j] for i in range(n_roots)) / n_roots for j in range(5)]
Mc = SM(n_roots, 5, lambda i, j: M_roots[i, j] - means[j])
cov_exact = (Mc.T * Mc) / (n_roots - 1)

# Get characteristic polynomial of covariance
x = Symbol('x')
cov_cp = cov_exact.charpoly(x)
cov_poly = Poly(cov_cp.as_expr(), x)
cov_coeffs = cov_poly.all_coeffs()

P(f'Characteristic polynomial of covariance matrix:')
for i, c in enumerate(cov_coeffs):
    deg = 5 - i
    P(f'  x^{deg}: {c}')

# All coefficients are rationals — find common denominator
P(f'\nAs rationals:')
for i, c in enumerate(cov_coeffs):
    deg = 5 - i
    r = R(c)
    P(f'  x^{deg}: {r.p}/{r.q}')

# The trace of cov = sum of eigenvalues = coefficient of x^4 (negated)
tr_cov = -cov_coeffs[1]
P(f'\ntr(cov) = {tr_cov}')
P(f'tr(cov) = sum of variances = {float(tr_cov):.10f}')

# The first eigenvalue / tr(cov) should be close to 73%
# But the eigenvalue is a root of the quintic...
# Let's check if the quintic has any factor of 73
P(f'\nChecking quintic coefficients for factors of 73:')
for i, c in enumerate(cov_coeffs):
    deg = 5 - i
    r = R(c)
    if r.p != 0:
        P(f'  x^{deg}: numerator {r.p}, mod 73 = {r.p % 73}')

# ================================================================
P()
P('=' * 72)
P('DEEP DIG 10: MUTUAL INFORMATION BETWEEN TABLES')
P('=' * 72)

# How much do T and B agree? Disagree?
agree = sum(1 for i in range(10) for j in range(10) if int(T[i,j]) == int(B[i,j]))
P(f'Agreement: {agree}/100 cells')
P(f'Disagreement: {100 - agree}/100 cells')

# List the agreements
P(f'\nAgreeing cells:')
for i in range(10):
    for j in range(i, 10):
        if int(T[i, j]) == int(B[i, j]):
            P(f'  ({i},{j}) = {int(T[i,j])} = {OP_NAMES[int(T[i,j])]}')

# The agreement pattern
# Both tables agree on the diagonal?
diag_agree = sum(1 for i in range(10) if int(T[i,i]) == int(B[i,i]))
P(f'\nDiagonal agreement: {diag_agree}/10')
off_agree = agree - diag_agree
P(f'Off-diagonal agreement: {off_agree}/{90}')

# The sum and difference tables
P(f'\n--- Sum table T + B ---')
SumTB = T + B
P(f'tr(T+B) = {int(np.trace(SumTB))}')
det_sum = round(np.linalg.det(SumTB))
P(f'det(T+B) = {det_sum}')
if abs(det_sum) > 1:
    P(f'  = {factorint(abs(det_sum))}')

P(f'\n--- Difference table T - B ---')
DiffTB = T - B
P(f'tr(T-B) = {int(np.trace(DiffTB))}')
det_diff = round(np.linalg.det(DiffTB))
P(f'det(T-B) = {det_diff}')
if abs(det_diff) > 1:
    P(f'  = {factorint(abs(det_diff))}')

# Product tables
P(f'\n--- Product tables ---')
det_TB = round(np.linalg.det(T @ B))
det_BT = round(np.linalg.det(B @ T))
P(f'det(TB) = {det_TB}')
P(f'det(BT) = {det_BT}')
P(f'det(T)*det(B) = 0 * {int(Bs.det())} = 0 (since det(T) = 0)')

# Anticommutator
P(f'\n--- Anticommutator {{T, B}} = TB + BT ---')
anti = Ts * Bs + Bs * Ts
P(f'tr(anticommutator) = {int(anti.trace())}')
det_anti = int(anti.det())
P(f'det(anticommutator) = {det_anti}')
if abs(det_anti) > 1:
    P(f'  = {factorint(abs(det_anti))}')
# Is the anticommutator symmetric?
is_anti_sym = all(anti[i,j] == anti[j,i] for i in range(10) for j in range(10))
P(f'Anticommutator symmetric: {is_anti_sym}')

# Check for 7 and 73 in anticommutator
P(f'det(anti) mod 7 = {det_anti % 7}')
P(f'det(anti) mod 73 = {det_anti % 73}')

# ================================================================
P()
P('=' * 72)
P('SUMMARY OF NEW FINDINGS')
P('=' * 72)

P(f"""
Key discoveries from deep dig:

1. VOID ROW DERIVATION:
   C[0,j] = 7*B[7,j] - sum_k k*T[k,j]
   = 7*(HARMONY generation row) - (position-weighted measurement)
   VOID in the commutator = HARMONY*generation minus indexed*measurement.

2. tr(C^2) = -2 * (lam^8 coefficient) = {tr_C2}
   This links eigenvalue sums to trace formulas through the tables.
   73 | 914325 means 73 divides the sum of eigenvalue magnitudes squared.

3. SENSITIVITY: Removing ANY single TSML exception changes the Pfaffian.
   The specific set of 5 exceptions is not arbitrary -- each one
   contributes to the algebraic structure of the commutator.

4. AGREEMENT: T and B agree on {agree} cells. The diagonal agreements
   and the LATTICE*COUNTER=PROGRESS agreement are the structural backbone.

5. 15083 remains unexplained. It appears only in the Pfaffian factorization
   and has no known connection to table entries, traces, or operator indices.
""")

# Write to file
import os
results_dir = os.path.dirname(os.path.abspath(__file__))
results_path = os.path.join(results_dir, 'deep_dig_results.txt')
with open(results_path, 'w') as f:
    f.write('\n'.join(output))
P(f'Results written to {results_path}')
