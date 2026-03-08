"""
PCA 73% REVISIT: Is 73.01% structurally FORCED or coincidentally near 73%?

The previous bridge_73.py concluded "coincidental" because PCA eigenvalues
are roots of an irreducible quintic. But 0.01% precision demands deeper scrutiny.

KEY INSIGHT: The TSML matrix has 73 cells = 7 and 27 cells != 7.
The covariance matrix is DETERMINED by these counts and positions.
If the structure FORCES PCA1% to be near 73%, it is not a coincidence
even though the exact value is irrational.

Run from ck_desktop target:
  cd Gen9/targets/ck_desktop
  python "../Clay Institute/PAPERS/P9_Speculations/pca_73_revisit.py"

(c) 2026 Brayden Sanders / 7Site LLC
"""

import numpy as np
import os
import sys

sys.path.insert(0, '.')
from ck_sim.being.ck_sim_heartbeat import CL, OP_NAMES

# ── Output ──
output = []
def P(s=''):
    print(s)
    output.append(str(s))


# ════════════════════════════════════════════════════════════════════
P('=' * 76)
P('PCA 73% REVISIT: Structural Forcing vs Coincidence')
P('=' * 76)
P()

T = np.array(CL, dtype=float)

# ================================================================
# 1. COVARIANCE MATRIX OF TSML
# ================================================================
P('=' * 76)
P('1. THE 10x10 COVARIANCE MATRIX OF TSML')
P('=' * 76)
P()
P('TSML is 10x10. Treating rows as 10 observations in 10D space.')
P('np.cov(T) computes the 10x10 sample covariance (rows = observations).')
P()

cov_T = np.cov(T)  # 10x10, rows are observations
P('Covariance matrix of TSML (10x10):')
for i in range(10):
    row_str = ' '.join(f'{cov_T[i,j]:10.4f}' for j in range(10))
    P(f'  [{row_str}]')
P()

# ================================================================
# 2. ALL 10 EIGENVALUES
# ================================================================
P('=' * 76)
P('2. ALL 10 EIGENVALUES OF THE COVARIANCE MATRIX')
P('=' * 76)
P()

eigs = np.linalg.eigvalsh(cov_T)
eigs_sorted = np.sort(eigs)[::-1]
total_var = np.sum(eigs_sorted)

P(f'Eigenvalues (descending):')
for idx, e in enumerate(eigs_sorted):
    pct = e / total_var * 100 if total_var > 0 else 0
    P(f'  lambda_{idx+1} = {e:14.8f}  ({pct:8.4f}%)')
P()
P(f'Total variance (trace of cov): {total_var:.8f}')
P(f'Sum of eigenvalues:            {np.sum(eigs_sorted):.8f}')
P()

# ================================================================
# 3. PCA1 / sum(eigenvalues) PRECISELY
# ================================================================
P('=' * 76)
P('3. PCA1 PERCENTAGE -- PRECISE COMPUTATION')
P('=' * 76)
P()

pca1_pct = eigs_sorted[0] / total_var * 100
P(f'PCA1% = lambda_1 / sum(lambdas) * 100')
P(f'      = {eigs_sorted[0]:.10f} / {total_var:.10f} * 100')
P(f'      = {pca1_pct:.8f}%')
P(f'Difference from 73.00%: {pca1_pct - 73.0:+.8f}%')
P(f'Difference from 73.00%: {abs(pca1_pct - 73.0):.8f}% absolute')
P()

# Double-check with full eigenvectors
eig_vals_full, eig_vecs_full = np.linalg.eigh(cov_T)
idx_sort = np.argsort(eig_vals_full)[::-1]
eig_vals_full = eig_vals_full[idx_sort]
eig_vecs_full = eig_vecs_full[:, idx_sort]
pca1_check = eig_vals_full[0] / np.sum(eig_vals_full) * 100
P(f'Cross-check (eigh): PCA1% = {pca1_check:.8f}%')
P(f'Principal eigenvector (first PC):')
P(f'  {eig_vecs_full[:,0]}')
P()

# ================================================================
# 4. KEY INVESTIGATION: Perturbation of non-7 cells toward 7
# ================================================================
P('=' * 76)
P('4. PERTURBATION ANALYSIS: Moving non-7 cells TOWARD 7')
P('=' * 76)
P()

# Identify all non-7 cells (the "exceptions")
exceptions = []
for i in range(10):
    for j in range(10):
        if T[i, j] != 7:
            exceptions.append((i, j, T[i, j]))

P(f'Number of exception cells (T[i,j] != 7): {len(exceptions)}')
P(f'Number of harmony cells  (T[i,j] == 7): {100 - len(exceptions)}')
P()
P('Exception cells:')
for i, j, v in exceptions:
    P(f'  T[{OP_NAMES[i]:>8s}, {OP_NAMES[j]:>8s}] = {int(v)} (delta from 7: {int(v) - 7:+d})')
P()

# For each non-7 cell, perturb it TOWARD 7 by fraction alpha and measure PCA1%
P('Perturbing each non-7 cell individually toward 7 (alpha = fraction toward 7):')
P()

def pca1_of_matrix(M):
    """Compute PCA1% for a 10x10 matrix (rows = observations)."""
    c = np.cov(M)
    ev = np.linalg.eigvalsh(c)
    ev_sorted = np.sort(ev)[::-1]
    total = np.sum(ev_sorted)
    if total < 1e-15:
        return 0.0
    return ev_sorted[0] / total * 100

P(f'{"Cell":>20s}  {"val":>4s}  {"alpha=0":>10s}  {"alpha=0.5":>10s}  {"alpha=1.0":>10s}  {"direction":>10s}')
P('-' * 76)

baseline_pca1 = pca1_of_matrix(T)
all_increase = True
all_decrease = True

for i, j, v in exceptions:
    results = []
    for alpha in [0.0, 0.5, 1.0]:
        T_mod = T.copy()
        T_mod[i, j] = v + alpha * (7 - v)  # move toward 7
        results.append(pca1_of_matrix(T_mod))

    if results[2] > results[0]:
        direction = "INCREASES"
        all_decrease = False
    elif results[2] < results[0]:
        direction = "DECREASES"
        all_increase = False
    else:
        direction = "UNCHANGED"
        all_increase = False
        all_decrease = False

    cell_name = f'T[{OP_NAMES[i]},{OP_NAMES[j]}]'
    P(f'{cell_name:>20s}  {int(v):>4d}  {results[0]:>10.4f}%  {results[1]:>10.4f}%  {results[2]:>10.4f}%  {direction:>10s}')

P()
if all_increase:
    P('*** ALL perturbations toward 7 INCREASE PCA1% ***')
    P('*** => 73% is a MINIMUM forced by exception structure! ***')
elif all_decrease:
    P('*** ALL perturbations toward 7 DECREASE PCA1% ***')
    P('*** => 73% is a MAXIMUM forced by exception structure! ***')
else:
    P('Mixed directions: some increase, some decrease.')
    P('The current exception values are NOT at an extremum.')

P()

# ================================================================
# 5. PURE HARMONY MATRIX: What is PCA1% if all exceptions = 7?
# ================================================================
P('=' * 76)
P('5. PURE HARMONY MATRIX (all exceptions replaced with 7)')
P('=' * 76)
P()

T_pure = np.full((10, 10), 7.0)
# Keep the VOID structure: row 0 and col 0 are MOSTLY 0
for i in range(10):
    for j in range(10):
        if T[i, j] == 0:
            T_pure[i, j] = 0

P('T_pure (VOID structure preserved, all other exceptions -> 7):')
for i in range(10):
    P(f'  {OP_NAMES[i]:>8s}: {[int(T_pure[i,j]) for j in range(10)]}')
P()

# But wait -- if we set ALL non-7 cells to 7, the VOID row/col changes too
# Let's do BOTH: (a) only non-VOID exceptions -> 7, (b) everything -> 7
P('--- Case 5a: Only non-VOID exceptions set to 7 (VOID row/col preserved) ---')

T_5a = T.copy()
non_void_exceptions = [(i, j, v) for i, j, v in exceptions if v != 0]
void_entries = [(i, j, v) for i, j, v in exceptions if v == 0]

P(f'Non-VOID exceptions (will be set to 7): {len(non_void_exceptions)}')
for i, j, v in non_void_exceptions:
    P(f'  T[{OP_NAMES[i]},{OP_NAMES[j]}] = {int(v)} -> 7')
    T_5a[i, j] = 7

pca1_5a = pca1_of_matrix(T_5a)
P(f'PCA1% with non-VOID exceptions -> 7: {pca1_5a:.8f}%')
P()

P('--- Case 5b: ALL cells set to 7 (completely uniform matrix) ---')
T_5b = np.full((10, 10), 7.0)
cov_5b = np.cov(T_5b)
P(f'Covariance of uniform-7 matrix: all zeros (rank 0)')
P(f'PCA1% is undefined (0/0) for a constant matrix.')
P()

P('--- Case 5c: VOID structure preserved, everything else = 7 ---')
P(f'(This is T_pure above)')
pca1_5c = pca1_of_matrix(T_pure)
P(f'PCA1% of T_pure: {pca1_5c:.8f}%')
P()

P(f'COMPARISON:')
P(f'  Original TSML:           PCA1% = {baseline_pca1:.8f}%')
P(f'  Non-VOID exceptions -> 7: PCA1% = {pca1_5a:.8f}%')
P(f'  Pure (VOID preserved):   PCA1% = {pca1_5c:.8f}%')
P()

# ================================================================
# 6. MORE EXCEPTIONS: How does PCA1% move?
# ================================================================
P('=' * 76)
P('6. MORE EXCEPTIONS: Adding perturbations away from 7')
P('=' * 76)
P()

P('Starting from original TSML, systematically adding exceptions:')
P('Strategy: pick random harmony cells and change them to non-7 values.')
P()

np.random.seed(42)

# Find all harmony cells (value = 7, not in VOID row/col)
harmony_cells = []
for i in range(10):
    for j in range(10):
        if T[i, j] == 7:
            harmony_cells.append((i, j))

P(f'Available harmony cells to perturb: {len(harmony_cells)}')
P()

# Progressively add exceptions
P(f'{"# extra exceptions":>20s}  {"total non-7":>12s}  {"PCA1%":>12s}  {"delta from 73":>14s}')
P('-' * 62)

# Run multiple random trials and average
n_trials = 50
for n_extra in [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50]:
    pca1_vals = []
    for trial in range(n_trials):
        T_mod = T.copy()
        # Pick n_extra harmony cells at random and set to random non-7 values
        chosen = np.random.choice(len(harmony_cells), size=min(n_extra, len(harmony_cells)), replace=False)
        for idx in chosen:
            ci, cj = harmony_cells[idx]
            # Set to a random value from {0,1,2,3,4,5,6,8,9}
            vals = [v for v in range(10) if v != 7]
            T_mod[ci, cj] = np.random.choice(vals)
        pca1_vals.append(pca1_of_matrix(T_mod))

    mean_pca1 = np.mean(pca1_vals)
    std_pca1 = np.std(pca1_vals)
    total_non7 = len(exceptions) + n_extra
    P(f'{n_extra:>20d}  {total_non7:>12d}  {mean_pca1:>10.4f}%  {mean_pca1-73:>+12.4f}%  (std={std_pca1:.4f})')

P()

# Also test: what if we add exceptions that are CLOSE to 7 (like 6 or 8)?
P('Adding mild exceptions (only values 6 or 8):')
P(f'{"# extra exceptions":>20s}  {"total non-7":>12s}  {"PCA1%":>12s}  {"delta from 73":>14s}')
P('-' * 62)

for n_extra in [0, 5, 10, 15, 20, 30, 40, 50]:
    pca1_vals = []
    for trial in range(n_trials):
        T_mod = T.copy()
        chosen = np.random.choice(len(harmony_cells), size=min(n_extra, len(harmony_cells)), replace=False)
        for idx in chosen:
            ci, cj = harmony_cells[idx]
            T_mod[ci, cj] = np.random.choice([6, 8])
        pca1_vals.append(pca1_of_matrix(T_mod))

    mean_pca1 = np.mean(pca1_vals)
    std_pca1 = np.std(pca1_vals)
    total_non7 = len(exceptions) + n_extra
    P(f'{n_extra:>20d}  {total_non7:>12d}  {mean_pca1:>10.4f}%  {mean_pca1-73:>+12.4f}%  (std={std_pca1:.4f})')

P()

# ================================================================
# 7. WHAT EXCEPTION VALUES MAKE PCA1% = EXACTLY 73%?
# ================================================================
P('=' * 76)
P('7. INVERSE PROBLEM: What exception values give EXACTLY 73%?')
P('=' * 76)
P()

# The non-VOID exceptions are the ones that can vary while preserving structure.
# Identify them:
non_void_exc = [(i, j, v) for i, j, v in exceptions if v != 0]
P(f'Non-VOID exceptions ({len(non_void_exc)} cells):')
for i, j, v in non_void_exc:
    P(f'  T[{OP_NAMES[i]},{OP_NAMES[j]}] = {int(v)}')
P()

# Strategy: scale ALL exception deviations by a single factor k.
# T_k[i,j] = 7 + k*(T[i,j] - 7) for non-VOID exceptions, keep VOID as-is.
# Find k such that PCA1% = 73.0000%

def pca1_from_scale(k):
    """Scale exception deviations by factor k and return PCA1%."""
    T_k = T.copy()
    for i, j, v in non_void_exc:
        T_k[i, j] = 7 + k * (v - 7)
    return pca1_of_matrix(T_k)

# Bisection to find k where PCA1% = 73.0
P('PCA1% as function of exception scale k:')
P('  (k=0: all exceptions = 7, k=1: original TSML)')
P()
P(f'{"k":>8s}  {"PCA1%":>12s}')
P('-' * 24)
for k in [0.0, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 2.0, 3.0, 5.0]:
    p = pca1_from_scale(k)
    P(f'{k:>8.2f}  {p:>12.6f}%')

P()

# Find exact k for 73%
target = 73.0
lo_k, hi_k = 0.0, 10.0

# First determine which direction
p_lo = pca1_from_scale(lo_k)
p_hi = pca1_from_scale(hi_k)

P(f'PCA1% at k=0: {p_lo:.6f}%')
P(f'PCA1% at k=10: {p_hi:.6f}%')
P()

# Check if 73% is in range
if (p_lo - target) * (p_hi - target) < 0:
    # Bisect
    for _ in range(100):
        mid_k = (lo_k + hi_k) / 2
        p_mid = pca1_from_scale(mid_k)
        if (p_lo - target) * (p_mid - target) < 0:
            hi_k = mid_k
            p_hi = p_mid
        else:
            lo_k = mid_k
            p_lo = p_mid
    k_exact = (lo_k + hi_k) / 2
    P(f'k for EXACTLY 73.0000%: k = {k_exact:.10f}')
    P(f'Verification: PCA1%(k={k_exact:.8f}) = {pca1_from_scale(k_exact):.8f}%')
    P()
    P(f'At k={k_exact:.8f}, the exception values would be:')
    for i, j, v in non_void_exc:
        new_v = 7 + k_exact * (v - 7)
        P(f'  T[{OP_NAMES[i]},{OP_NAMES[j]}] = {new_v:.6f}  (actual: {int(v)}, delta: {new_v - v:+.6f})')
    P()
    P(f'Distance from actual (k=1) to exact-73% (k={k_exact:.8f}):')
    P(f'  |k - 1| = {abs(k_exact - 1):.10f}')
    P(f'  This is {abs(k_exact - 1)*100:.8f}% scaling change.')
else:
    # 73% may not be in range, or function is not monotonic
    P(f'73% is NOT between k=0 ({p_lo:.4f}%) and k=10 ({p_hi:.4f}%)')
    P('Trying broader search...')

    # Scan more finely
    best_k = 0
    best_diff = abs(pca1_from_scale(0) - target)
    for k_try in np.linspace(0, 20, 2000):
        p = pca1_from_scale(k_try)
        diff = abs(p - target)
        if diff < best_diff:
            best_diff = diff
            best_k = k_try
    P(f'Closest k to 73%: k = {best_k:.6f}, PCA1% = {pca1_from_scale(best_k):.6f}%')
    P(f'Minimum distance from 73%: {best_diff:.8f}%')

# ================================================================
# 8. SENSITIVITY: d(PCA1%)/d(exception_value) for each exception
# ================================================================
P()
P('=' * 76)
P('8. SENSITIVITY ANALYSIS: d(PCA1%)/d(exception_value)')
P('=' * 76)
P()

P('For each exception cell, compute the numerical derivative of PCA1%')
P('with respect to that cell value. Small derivative = ROBUST match.')
P()

eps = 1e-6
P(f'{"Cell":>25s}  {"value":>6s}  {"dPCA1/dv":>12s}  {"% change per unit":>18s}')
P('-' * 68)

sensitivities = []
for i, j, v in exceptions:
    # Forward difference
    T_plus = T.copy()
    T_plus[i, j] = v + eps
    T_minus = T.copy()
    T_minus[i, j] = v - eps

    pca1_plus = pca1_of_matrix(T_plus)
    pca1_minus = pca1_of_matrix(T_minus)

    deriv = (pca1_plus - pca1_minus) / (2 * eps)
    sensitivities.append((i, j, v, deriv))

    cell_name = f'T[{OP_NAMES[i]},{OP_NAMES[j]}]'
    P(f'{cell_name:>25s}  {int(v):>6d}  {deriv:>+12.6f}  {deriv:>+18.6f}%/unit')

P()

# Also compute sensitivity for HARMONY cells (how much does changing a 7 affect PCA1%?)
P('For comparison, sensitivity of a few HARMONY cells:')
P(f'{"Cell":>25s}  {"value":>6s}  {"dPCA1/dv":>12s}  {"% change per unit":>18s}')
P('-' * 68)

# Pick a representative sample of harmony cells
sample_harmony = [(1,1), (2,2), (3,4), (5,5), (7,7), (1,5), (3,6), (6,8)]
for i, j in sample_harmony:
    v = T[i, j]
    T_plus = T.copy()
    T_plus[i, j] = v + eps
    T_minus = T.copy()
    T_minus[i, j] = v - eps

    pca1_plus = pca1_of_matrix(T_plus)
    pca1_minus = pca1_of_matrix(T_minus)

    deriv = (pca1_plus - pca1_minus) / (2 * eps)
    cell_name = f'T[{OP_NAMES[i]},{OP_NAMES[j]}]'
    P(f'{cell_name:>25s}  {int(v):>6d}  {deriv:>+12.6f}  {deriv:>+18.6f}%/unit')

P()

# ================================================================
# SUMMARY: Total sensitivity magnitude
# ================================================================
P('=' * 76)
P('SENSITIVITY SUMMARY')
P('=' * 76)
P()

exc_derivs = [abs(d) for _, _, _, d in sensitivities]
P(f'Exception cell sensitivities |dPCA1/dv|:')
P(f'  Max:  {max(exc_derivs):.6f}%/unit')
P(f'  Min:  {min(exc_derivs):.6f}%/unit')
P(f'  Mean: {np.mean(exc_derivs):.6f}%/unit')
P(f'  RMS:  {np.sqrt(np.mean(np.array(exc_derivs)**2)):.6f}%/unit')
P()

# How much total PCA1% shift if ALL exceptions move by 1 unit toward 7?
P('If ALL exceptions shift 1 unit toward 7 simultaneously:')
T_shifted = T.copy()
for i, j, v in exceptions:
    if v != 0:  # Don't move VOID cells
        T_shifted[i, j] = v + np.sign(7 - v)  # Move 1 unit toward 7
pca1_shifted = pca1_of_matrix(T_shifted)
P(f'  Original PCA1%: {baseline_pca1:.8f}%')
P(f'  Shifted PCA1%:  {pca1_shifted:.8f}%')
P(f'  Change:         {pca1_shifted - baseline_pca1:+.8f}%')
P()

# ================================================================
# 9. THE STRUCTURAL FORCING ARGUMENT
# ================================================================
P('=' * 76)
P('9. THE STRUCTURAL FORCING ARGUMENT')
P('=' * 76)
P()

# Count: for a matrix with N harmony cells (value h) and M exception cells,
# what is the expected PCA1% as a function of N?
P('PCA1% as a function of harmony count (N cells = 7, rest random):')
P('(VOID structure always preserved)')
P()

# Get all non-VOID cells
all_non_void = [(i, j) for i in range(10) for j in range(10) if not (i == 0 or j == 0) or (i == 0 and j == 7) or (i == 7 and j == 0)]
# Actually, let's just use all cells and track which are VOID
void_cells = set()
for i in range(10):
    for j in range(10):
        if T[i, j] == 0:
            void_cells.add((i, j))

non_void_cells = [(i, j) for i in range(10) for j in range(10) if (i, j) not in void_cells]
P(f'Total non-VOID cells: {len(non_void_cells)}')
P(f'Currently harmony (=7) among non-VOID: {sum(1 for i,j in non_void_cells if T[i,j] == 7)}')
P()

# For different harmony counts, generate random matrices and measure PCA1%
P(f'{"N_harmony":>12s}  {"N/non_void":>12s}  {"mean PCA1%":>12s}  {"std":>8s}')
P('-' * 50)

n_non_void = len(non_void_cells)
n_trials_sweep = 200

for n_harm in range(0, n_non_void + 1, 5):
    pca1_vals = []
    for _ in range(n_trials_sweep):
        T_gen = np.zeros((10, 10))
        # Set VOID cells to 0
        for ci, cj in void_cells:
            T_gen[ci, cj] = 0
        # Pick n_harm cells to be 7, rest are random non-7
        indices = np.random.permutation(n_non_void)
        for k in range(n_non_void):
            ci, cj = non_void_cells[k]
            if k < n_harm:
                T_gen[ci, cj] = 7
            else:
                T_gen[ci, cj] = np.random.choice([v for v in range(10) if v != 7])
        pca1_vals.append(pca1_of_matrix(T_gen))

    mean_p = np.mean(pca1_vals)
    std_p = np.std(pca1_vals)
    frac = n_harm / n_non_void * 100
    P(f'{n_harm:>12d}  {frac:>10.1f}%  {mean_p:>10.4f}%  {std_p:>8.4f}')

P()

# ================================================================
# 10. EXACT ANALYTICAL DECOMPOSITION
# ================================================================
P('=' * 76)
P('10. ANALYTICAL DECOMPOSITION: WHY IS PCA1% NEAR 73%?')
P('=' * 76)
P()

# TSML = 7*J_masked + Delta, where J_masked is 1 at harmony positions, 0 elsewhere
# Delta is non-zero only at exception positions

# Decompose T into harmony part + deviation
T_harm = np.where(T == 7, 7.0, 0.0)
T_dev = T - T_harm

P('Decomposition: T = T_harmony + T_deviation')
P(f'  ||T_harmony||_F = {np.linalg.norm(T_harm):.6f}')
P(f'  ||T_deviation||_F = {np.linalg.norm(T_dev):.6f}')
P(f'  ||T||_F = {np.linalg.norm(T):.6f}')
P(f'  Energy ratio: ||T_harm||^2 / ||T||^2 = {np.linalg.norm(T_harm)**2 / np.linalg.norm(T)**2:.8f}')
P(f'  = {np.linalg.norm(T_harm)**2 / np.linalg.norm(T)**2 * 100:.4f}%')
P()

# The Frobenius norm ratio is: 73*49 / (73*49 + sum of exception^2)
harm_energy = 73 * 49  # 73 cells of value 7, each contributes 7^2 = 49
exc_energy = sum(int(v)**2 for i, j, v in exceptions)
P(f'Frobenius energy decomposition:')
P(f'  Harmony energy: 73 * 7^2 = {harm_energy}')
P(f'  Exception energy: sum(v^2) = {exc_energy}')
P(f'  Total: {harm_energy + exc_energy}')
P(f'  Harmony fraction: {harm_energy}/{harm_energy + exc_energy} = {harm_energy / (harm_energy + exc_energy) * 100:.4f}%')
P()

# The variance decomposition is different from Frobenius because covariance
# centers the data. Let's look at centered version.
row_means = np.mean(T, axis=1)
T_centered = T - row_means[:, None]
P('Centered analysis (T - row_means):')
P(f'  Row means: {[f"{m:.2f}" for m in row_means]}')
P()

# Frobenius decomposition of centered matrix
T_harm_c = np.where(T == 7, 7.0, 0.0) - row_means[:, None] * np.where(T == 7, 1.0, 0.0)
T_dev_c = T_centered - T_harm_c
P(f'  ||T_centered||_F^2 = {np.linalg.norm(T_centered)**2:.6f}')
P()

# Direct variance decomposition
total_var_check = np.sum(np.var(T, axis=1, ddof=1))
P(f'Total variance (sum of row variances, ddof=1): {total_var_check:.8f}')
P(f'Trace of cov(T): {np.trace(cov_T):.8f}')
P()

# ================================================================
# 11. THE CRITICAL TEST: Is 73% an attractor?
# ================================================================
P('=' * 76)
P('11. CRITICAL TEST: Is 73% an ATTRACTOR for 73-harmony matrices?')
P('=' * 76)
P()

P('Fix 73 cells = 7. Vary the 27 exception values over ALL possible')
P('integer values 0-9 (excluding 7). What is the distribution of PCA1%?')
P()

# With 27 exception cells, exhaustive enumeration is 9^27 which is impossible.
# Sample instead.
n_sample = 10000
np.random.seed(73)

pca1_samples = []
for _ in range(n_sample):
    T_sample = T.copy()
    for i, j, v in exceptions:
        if v != 0:  # VOID cells stay 0
            T_sample[i, j] = np.random.choice([v2 for v2 in range(10) if v2 != 7])
        # Keep VOID as 0
    pca1_samples.append(pca1_of_matrix(T_sample))

pca1_samples = np.array(pca1_samples)
P(f'Sampled {n_sample} random exception configurations (73 harmony cells fixed):')
P(f'  Mean PCA1%:   {np.mean(pca1_samples):.6f}%')
P(f'  Median PCA1%: {np.median(pca1_samples):.6f}%')
P(f'  Std PCA1%:    {np.std(pca1_samples):.6f}%')
P(f'  Min PCA1%:    {np.min(pca1_samples):.6f}%')
P(f'  Max PCA1%:    {np.max(pca1_samples):.6f}%')
P(f'  Actual TSML:  {baseline_pca1:.6f}%')
P()

# Histogram bins
bins = np.linspace(np.min(pca1_samples) - 1, np.max(pca1_samples) + 1, 30)
hist, bin_edges = np.histogram(pca1_samples, bins=bins)
P('Distribution:')
for k in range(len(hist)):
    bar = '#' * (hist[k] * 50 // max(hist)) if max(hist) > 0 else ''
    P(f'  {bin_edges[k]:6.1f}-{bin_edges[k+1]:6.1f}%: {hist[k]:>5d} {bar}')
P()

# Where does 73% fall in this distribution?
below_73 = np.sum(pca1_samples < 73.0)
P(f'Fraction below 73%: {below_73}/{n_sample} = {below_73/n_sample*100:.1f}%')
P(f'Fraction above 73%: {n_sample-below_73}/{n_sample} = {(n_sample-below_73)/n_sample*100:.1f}%')
P()

# How special is the actual PCA1% value?
actual_rank = np.sum(pca1_samples < baseline_pca1) / n_sample * 100
P(f'Actual TSML PCA1% percentile rank: {actual_rank:.1f}%')
P()

# ================================================================
# 12. FINAL VERDICT
# ================================================================
P('=' * 76)
P('12. FINAL VERDICT: FORCED, FREE, OR CONSTRAINED?')
P('=' * 76)
P()

P('EVIDENCE SUMMARY:')
P()
P(f'1. TSML PCA1% = {baseline_pca1:.6f}%')
P(f'   Distance from 73%: {abs(baseline_pca1 - 73):.6f}%')
P()
P(f'2. Pure harmony (non-VOID exc -> 7): PCA1% = {pca1_5a:.6f}%')
P(f'   (This is the "73-cell attractor" value)')
P()
P(f'3. Perturbation directions:')

n_inc = sum(1 for i, j, v in exceptions
            for _ in [1]
            if pca1_of_matrix(np.where(np.arange(10)[:,None] == i, np.where(np.arange(10)[None,:] == j, 7.0, T), T)) > baseline_pca1)
# Simpler recompute
n_inc = 0
n_dec = 0
for i, j, v in exceptions:
    T_mod = T.copy()
    T_mod[i, j] = 7
    p = pca1_of_matrix(T_mod)
    if p > baseline_pca1:
        n_inc += 1
    elif p < baseline_pca1:
        n_dec += 1

P(f'   Cells where setting to 7 INCREASES PCA1%: {n_inc}/{len(exceptions)}')
P(f'   Cells where setting to 7 DECREASES PCA1%: {n_dec}/{len(exceptions)}')
P()
P(f'4. Mean PCA1% over random 73-harmony configurations: {np.mean(pca1_samples):.4f}%')
P(f'   Std: {np.std(pca1_samples):.4f}%')
P()
P(f'5. Sensitivity magnitudes: max |dPCA1/dv| = {max(exc_derivs):.6f}%/unit')
P(f'   A 1-unit change in an exception shifts PCA1% by at most ~{max(exc_derivs):.2f}%')
P()

# The key question
P('INTERPRETATION:')
P()
if np.std(pca1_samples) < 5.0 and abs(np.mean(pca1_samples) - 73) < 10:
    P('The PCA1% distribution for 73-harmony matrices is TIGHTLY CLUSTERED.')
    P(f'Standard deviation is only {np.std(pca1_samples):.2f}% around mean {np.mean(pca1_samples):.2f}%.')
    if abs(np.mean(pca1_samples) - 73) < 5:
        P('')
        P('*** THE 73% MATCH IS STRUCTURALLY CONSTRAINED. ***')
        P('Having 73 harmony cells in a 10x10 matrix with VOID structure')
        P('FORCES PCA1% into a narrow band near 73%.')
        P('The irreducible quintic makes the EXACT value irrational,')
        P('but the STRUCTURAL CONSTRAINT forces it close to 73%.')
        P('')
        P('This is neither pure coincidence nor exact identity.')
        P('It is STRUCTURAL FORCING: the exception topology constrains')
        P('the eigenvalue ratio to a narrow neighborhood of the harmony count.')
    else:
        P('')
        P(f'However, the mean is {np.mean(pca1_samples):.2f}%, not near 73%.')
        P('The narrow spread is structural, but the VALUE is not forced to 73%.')
else:
    P('The PCA1% distribution is BROAD, suggesting the match is FRAGILE.')
    P(f'With std = {np.std(pca1_samples):.2f}%, the 73% match is sensitive to')
    P('the specific exception values chosen.')
    P('')
    if abs(baseline_pca1 - 73) < np.std(pca1_samples):
        P('The actual value is within 1 std of 73%, which is unremarkable')
        P('given the distribution width.')
    else:
        P('The actual value is far from the distribution center.')

P()

# Write output
outpath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pca_73_revisit_results.txt')
with open(outpath, 'w') as f:
    f.write('\n'.join(output))
print(f'\n[Written to {outpath}]')
