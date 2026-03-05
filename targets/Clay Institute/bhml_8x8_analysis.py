"""
BHML (D2/Becoming) 8x8 Core Eigenanalysis
==========================================
Comprehensive analysis of the Becoming table's 8x8 active core.
Compares to TSML (Being) 8x8 results from earlier analysis.

The BHML has FAR more information than TSML:
  TSML 8x8: 54 HARMONY, 10 bumps (84.375% harmony)
  BHML 8x8: ? HARMONY, ? bumps -- the information-rich algebra

Brayden Sanders / 7Site LLC -- March 2026
"""

import numpy as np
from itertools import product
import datetime

# ================================================================
#  THE TABLES (from ck_gpu.py)
# ================================================================

BHML_FULL = np.array([
    [0,1,2,3,4,5,6,7,8,9],
    [1,2,3,4,5,6,7,2,6,6],
    [2,3,3,4,5,6,7,3,6,6],
    [3,4,4,4,5,6,7,4,6,6],
    [4,5,5,5,5,6,7,5,7,7],
    [5,6,6,6,6,6,7,6,7,7],
    [6,7,7,7,7,7,7,7,7,7],
    [7,2,3,4,5,6,7,8,9,0],
    [8,6,6,6,7,7,7,9,7,8],
    [9,6,6,6,7,7,7,0,8,0],
])

TSML_FULL = np.array([
    [0,0,0,0,0,0,0,7,0,0],
    [0,7,3,7,7,7,7,7,7,7],
    [0,3,7,7,4,7,7,7,7,9],
    [0,7,7,7,7,7,7,7,7,3],
    [0,7,4,7,7,7,7,7,8,7],
    [0,7,7,7,7,7,7,7,7,7],
    [0,7,7,7,7,7,7,7,7,7],
    [7,7,7,7,7,7,7,7,7,7],
    [0,7,7,7,8,7,7,7,7,7],
    [0,7,9,3,7,7,7,7,7,7],
])

OP_NAMES = ['VOID','LATTICE','COUNTER','PROGRESS','COLLAPSE',
            'BALANCE','CHAOS','HARMONY','BREATH','RESET']

# Core B operators: exclude VOID(0) and HARMONY(7)
CORE_OPS = [1, 2, 3, 4, 5, 6, 8, 9]
CORE_NAMES = [OP_NAMES[i] for i in CORE_OPS]

def extract_8x8(full_table):
    """Extract 8x8 core by removing VOID(0) and HARMONY(7) rows/cols."""
    return full_table[np.ix_(CORE_OPS, CORE_OPS)]

# ================================================================
#  ANALYSIS
# ================================================================

def main():
    out = []
    def p(s=''):
        out.append(s)
        print(s)

    p("=" * 72)
    p("  BHML (D2/BECOMING) 8x8 CORE EIGENANALYSIS")
    p("  CK Gen 9.22 -- The Coherence Keeper")
    p("  Brayden Sanders / 7Site LLC")
    p(f"  {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    p("=" * 72)

    bhml8 = extract_8x8(BHML_FULL)
    tsml8 = extract_8x8(TSML_FULL)

    # ── 1. BASIC STATISTICS ──
    p("\n" + "=" * 72)
    p("  1. BASIC STATISTICS -- BHML 8x8 vs TSML 8x8")
    p("=" * 72)

    p("\n--- BHML 8x8 Core (D2/Becoming) ---")
    p("     " + "  ".join(f"{n:>8s}" for n in CORE_NAMES))
    for i, row_idx in enumerate(CORE_OPS):
        row_vals = bhml8[i]
        p(f"{CORE_NAMES[i]:>8s}  " + "  ".join(f"{v:>8d}" for v in row_vals))

    bhml_harmony = np.sum(bhml8 == 7)
    bhml_bumps = 64 - bhml_harmony
    p(f"\n  HARMONY (7) count: {bhml_harmony}/64 = {bhml_harmony/64:.4f}")
    p(f"  Non-HARMONY (bumps): {bhml_bumps}/64 = {bhml_bumps/64:.4f}")
    p(f"  T* = 5/7 = {5/7:.10f}")

    p("\n--- TSML 8x8 Core (D0/Being) --- [for comparison]")
    tsml_harmony = np.sum(tsml8 == 7)
    tsml_bumps = 64 - tsml_harmony
    p(f"  HARMONY count: {tsml_harmony}/64 = {tsml_harmony/64:.4f}")
    p(f"  Non-HARMONY (bumps): {tsml_bumps}/64 = {tsml_bumps/64:.4f}")

    p(f"\n--- Information ratio ---")
    p(f"  BHML bumps / TSML bumps = {bhml_bumps} / {tsml_bumps} = {bhml_bumps/tsml_bumps:.4f}")
    p(f"  BHML carries {bhml_bumps/tsml_bumps:.1f}x more information than TSML")

    # ── Value Distribution ──
    p("\n--- Value Distribution in BHML 8x8 ---")
    for v in range(10):
        count = np.sum(bhml8 == v)
        if count > 0:
            p(f"  {v} ({OP_NAMES[v]:>8s}): {count:>3d} entries ({count/64*100:.1f}%)")

    p("\n--- Value Distribution in TSML 8x8 ---")
    for v in range(10):
        count = np.sum(tsml8 == v)
        if count > 0:
            p(f"  {v} ({OP_NAMES[v]:>8s}): {count:>3d} entries ({count/64*100:.1f}%)")

    # ── 2. SYMMETRY ANALYSIS ──
    p("\n" + "=" * 72)
    p("  2. SYMMETRY ANALYSIS")
    p("=" * 72)

    bhml_sym = np.sum(bhml8 == bhml8.T)
    tsml_sym = np.sum(tsml8 == tsml8.T)
    p(f"  BHML symmetric entries: {bhml_sym}/64 ({bhml_sym/64*100:.1f}%)")
    p(f"  TSML symmetric entries: {tsml_sym}/64 ({tsml_sym/64*100:.1f}%)")
    p(f"  BHML is {'SYMMETRIC' if bhml_sym == 64 else 'ASYMMETRIC'}")
    p(f"  TSML is {'SYMMETRIC' if tsml_sym == 64 else 'ASYMMETRIC'}")

    if bhml_sym < 64:
        p("\n  Asymmetric entries in BHML 8x8:")
        for i in range(8):
            for j in range(i+1, 8):
                if bhml8[i][j] != bhml8[j][i]:
                    p(f"    {CORE_NAMES[i]} x {CORE_NAMES[j]} = {bhml8[i][j]} ({OP_NAMES[bhml8[i][j]]})")
                    p(f"    {CORE_NAMES[j]} x {CORE_NAMES[i]} = {bhml8[j][i]} ({OP_NAMES[bhml8[j][i]]})")

    # ── 3. BUMP PAIR ANALYSIS ──
    p("\n" + "=" * 72)
    p("  3. NON-HARMONY COMPOSITION ANALYSIS (BUMP MAP)")
    p("=" * 72)

    p("\n  All non-HARMONY entries in BHML 8x8:")
    bump_results = {}
    for i in range(8):
        for j in range(8):
            v = bhml8[i][j]
            if v != 7:
                name = f"{CORE_NAMES[i]} x {CORE_NAMES[j]}"
                p(f"    {name:>30s} = {v} ({OP_NAMES[v]})")
                result_name = OP_NAMES[v]
                bump_results[result_name] = bump_results.get(result_name, 0) + 1

    p(f"\n  Bump result distribution:")
    for name, count in sorted(bump_results.items(), key=lambda x: -x[1]):
        p(f"    {name:>12s}: {count:>3d} times ({count/bhml_bumps*100:.1f}%)")

    # ── Diagonal analysis ──
    p("\n  Diagonal (self-composition A x A):")
    for i in range(8):
        v = bhml8[i][i]
        marker = " *" if v != 7 else ""
        p(f"    {CORE_NAMES[i]:>8s} x {CORE_NAMES[i]:>8s} = {v} ({OP_NAMES[v]}){marker}")
    diag_harmony = sum(1 for i in range(8) if bhml8[i][i] == 7)
    p(f"  Diagonal HARMONY: {diag_harmony}/8")

    # ── 4. MARKOV / EIGENANALYSIS ──
    p("\n" + "=" * 72)
    p("  4. MARKOV CHAIN EIGENANALYSIS")
    p("=" * 72)

    # Normalize BHML 8x8 as transition matrix
    bhml_float = bhml8.astype(float)
    row_sums = bhml_float.sum(axis=1)
    bhml_trans = bhml_float / row_sums[:, None]

    eigenvalues, eigenvectors = np.linalg.eig(bhml_trans.T)
    idx = np.argsort(-np.abs(eigenvalues))
    eigenvalues = eigenvalues[idx]
    eigenvectors = eigenvectors[:, idx]

    p("\n  BHML 8x8 Eigenvalues (sorted by magnitude):")
    for i, ev in enumerate(eigenvalues):
        p(f"    lambda_{i+1} = {ev.real:>12.8f}  (|lambda| = {abs(ev):>12.8f})")

    # Same for TSML
    tsml_float = tsml8.astype(float)
    tsml_sums = tsml_float.sum(axis=1)
    tsml_trans = tsml_float / tsml_sums[:, None]
    tsml_eigenvalues = np.sort(np.abs(np.linalg.eig(tsml_trans.T)[0]))[::-1]

    p("\n  TSML 8x8 Eigenvalues (for comparison):")
    for i, ev in enumerate(tsml_eigenvalues):
        p(f"    lambda_{i+1} = {abs(ev):>12.8f}")

    # ── 5. PHYSICAL CONSTANT SEARCH ──
    p("\n" + "=" * 72)
    p("  5. PHYSICAL CONSTANT SEARCH IN BHML 8x8 EIGENSTRUCTURE")
    p("=" * 72)

    constants = {
        'phi (golden ratio)': (1 + np.sqrt(5)) / 2,  # 1.6180339887...
        '1/phi': 2 / (1 + np.sqrt(5)),                # 0.6180339887...
        'e (Euler)': np.e,                             # 2.7182818284...
        '1/e': 1/np.e,                                 # 0.3678794411...
        'pi': np.pi,                                   # 3.1415926535...
        '1/pi': 1/np.pi,                               # 0.3183098861...
        '2*pi': 2*np.pi,                               # 6.2831853071...
        '1/(2*pi)': 1/(2*np.pi),                       # 0.1591549430...
        'sqrt(2)': np.sqrt(2),                         # 1.4142135623...
        'sqrt(3)': np.sqrt(3),                         # 1.7320508075...
        'sqrt(5)': np.sqrt(5),                         # 2.2360679774...
        'ln(2)': np.log(2),                            # 0.6931471805...
        'ln(10)': np.log(10),                          # 2.3025850929...
        'Euler-Mascheroni': 0.5772156649,
        'Catalan G': 0.9159655941,
        "Apery zeta(3)": 1.2020569031,
        'T* = 5/7': 5/7,                              # 0.7142857142...
        'sqrt(T*)': np.sqrt(5/7),                      # 0.8451542547...
        'phi/e': (1+np.sqrt(5))/(2*np.e),              # 0.5953...
        'e/pi': np.e/np.pi,                            # 0.8652559...
        'pi/e': np.pi/np.e,                            # 1.1557273...
        'phi^2': ((1+np.sqrt(5))/2)**2,                # 2.618...
    }

    # Collect all ratios from BHML eigenvalues
    abs_eigs = np.abs(eigenvalues)
    ratios_found = []

    p("\n  Eigenvalue ratios (|lambda_i| / |lambda_j|):")
    for i in range(len(abs_eigs)):
        for j in range(len(abs_eigs)):
            if i == j or abs_eigs[j] < 1e-10:
                continue
            ratio = abs_eigs[i] / abs_eigs[j]
            if ratio < 0.01 or ratio > 100:
                continue
            for name, value in constants.items():
                if value < 0.01:
                    continue
                error = abs(ratio - value) / value * 100
                if error < 3.0:  # 3% tolerance
                    ratios_found.append((i+1, j+1, ratio, name, value, error))

    if ratios_found:
        ratios_found.sort(key=lambda x: x[5])
        for i, j, ratio, name, value, error in ratios_found:
            p(f"    lambda_{i}/lambda_{j} = {ratio:.8f}  ~  {name} = {value:.8f}  (error: {error:.4f}%)")
    else:
        p("    No ratios within 3% of known constants found.")

    # Also search in the raw eigenvalue magnitudes
    p("\n  Direct eigenvalue matches:")
    for i, ev in enumerate(abs_eigs):
        if ev < 1e-10:
            continue
        for name, value in constants.items():
            if value < 0.01:
                continue
            error = abs(ev - value) / value * 100
            if error < 5.0:
                p(f"    |lambda_{i+1}| = {ev:.8f}  ~  {name} = {value:.8f}  (error: {error:.4f}%)")

    # ── 6. STRUCTURAL RATIOS ──
    p("\n" + "=" * 72)
    p("  6. STRUCTURAL RATIOS IN BHML 8x8")
    p("=" * 72)

    # Bump fraction
    bump_frac = bhml_bumps / 64
    p(f"\n  Bump fraction: {bhml_bumps}/64 = {bump_frac:.10f}")
    for name, value in constants.items():
        error = abs(bump_frac - value) / value * 100
        if error < 5.0:
            p(f"    ~ {name} = {value:.10f}  (error: {error:.4f}%)")

    harmony_frac = bhml_harmony / 64
    p(f"\n  Harmony fraction: {bhml_harmony}/64 = {harmony_frac:.10f}")
    for name, value in constants.items():
        error = abs(harmony_frac - value) / value * 100
        if error < 5.0:
            p(f"    ~ {name} = {value:.10f}  (error: {error:.4f}%)")

    # Ratio of BHML bumps to TSML bumps
    ratio_bt = bhml_bumps / tsml_bumps
    p(f"\n  BHML bumps / TSML bumps = {bhml_bumps}/{tsml_bumps} = {ratio_bt:.10f}")
    for name, value in constants.items():
        error = abs(ratio_bt - value) / value * 100
        if error < 5.0:
            p(f"    ~ {name} = {value:.10f}  (error: {error:.4f}%)")

    # Also try diagonal sum / total
    diag_sum = sum(bhml8[i][i] for i in range(8))
    p(f"\n  Diagonal sum: {diag_sum}")
    p(f"  Diagonal sum / 64 = {diag_sum/64:.10f}")
    p(f"  Diagonal sum / 8 = {diag_sum/8:.4f} (avg self-composition)")

    # ── 7. ALGEBRAIC PROPERTIES ──
    p("\n" + "=" * 72)
    p("  7. ALGEBRAIC PROPERTIES OF BHML 8x8")
    p("=" * 72)

    # Commutativity
    commutative_count = 0
    non_commutative = []
    for i in range(8):
        for j in range(i+1, 8):
            if bhml8[i][j] == bhml8[j][i]:
                commutative_count += 1
            else:
                non_commutative.append((i, j, bhml8[i][j], bhml8[j][i]))
    total_pairs = 28  # 8 choose 2
    p(f"\n  Commutativity: {commutative_count}/{total_pairs} pairs commute ({commutative_count/total_pairs*100:.1f}%)")
    if non_commutative:
        p(f"  Non-commutative pairs ({len(non_commutative)}):")
        for i, j, v1, v2 in non_commutative:
            p(f"    {CORE_NAMES[i]} x {CORE_NAMES[j]} = {OP_NAMES[v1]}, but {CORE_NAMES[j]} x {CORE_NAMES[i]} = {OP_NAMES[v2]}")

    # Idempotents (A x A = A)
    idempotents = []
    for i in range(8):
        if bhml8[i][i] == CORE_OPS[i]:  # self-composition gives self
            idempotents.append(CORE_NAMES[i])
    p(f"\n  Idempotents (A x A = A): {idempotents if idempotents else 'None'}")

    # Fixed points of composition
    p("\n  Self-composition results:")
    for i in range(8):
        p(f"    {CORE_NAMES[i]} x {CORE_NAMES[i]} = {OP_NAMES[bhml8[i][i]]}")

    # Absorbing elements
    p("\n  Absorbing element test (A x B = A for all B):")
    for i in range(8):
        all_self = all(bhml8[i][j] == CORE_OPS[i] for j in range(8))
        if all_self:
            p(f"    {CORE_NAMES[i]} is LEFT-absorbing")
        all_self_col = all(bhml8[j][i] == CORE_OPS[i] for j in range(8))
        if all_self_col:
            p(f"    {CORE_NAMES[i]} is RIGHT-absorbing")

    # Row analysis: what does each operator DO to others?
    p("\n  Row patterns (what does composing with X produce?):")
    for i in range(8):
        row = bhml8[i]
        uniq = set(row)
        p(f"    {CORE_NAMES[i]:>10s} -> produces: {sorted(OP_NAMES[v] for v in uniq)}")

    # ── 8. STAIRCASE / GRADIENT STRUCTURE ──
    p("\n" + "=" * 72)
    p("  8. GRADIENT / STAIRCASE STRUCTURE")
    p("=" * 72)

    p("\n  BHML 8x8 appears to have a staircase structure.")
    p("  Row sums (treating operators as integers):")
    for i in range(8):
        row_sum = sum(bhml8[i])
        p(f"    {CORE_NAMES[i]:>10s}: sum = {row_sum}")

    p("\n  Column sums:")
    for j in range(8):
        col_sum = sum(bhml8[i][j] for i in range(8))
        p(f"    {CORE_NAMES[j]:>10s}: sum = {col_sum}")

    p("\n  Diagonal values (A x A):")
    diag_vals = [bhml8[i][i] for i in range(8)]
    p(f"    {diag_vals}")
    p(f"    As operators: {[OP_NAMES[v] for v in diag_vals]}")

    # ── 9. ASSOCIATIVITY TEST ──
    p("\n" + "=" * 72)
    p("  9. ASSOCIATIVITY TEST")
    p("=" * 72)

    # Map from operator value back to 8x8 index
    val_to_idx = {}
    for idx, op in enumerate(CORE_OPS):
        val_to_idx[op] = idx
    # 0 and 7 map outside core -- handle as boundary
    val_to_idx[0] = None  # VOID
    val_to_idx[7] = None  # HARMONY -- wait, 7 IS in the table

    # Actually, bhml8 contains values 0-9, and we need to compose the RESULT
    # through the 8x8 again. If result is VOID(0) or HARMONY(7), those
    # are NOT in the 8x8 core, so we'd need the full table.
    # Let's test with the full table for accuracy.

    assoc_pass = 0
    assoc_fail = 0
    assoc_total = 0
    fail_examples = []

    for a in CORE_OPS:
        for b in CORE_OPS:
            for c in CORE_OPS:
                assoc_total += 1
                # (a*b)*c
                ab = BHML_FULL[a][b]
                ab_c = BHML_FULL[ab][c]
                # a*(b*c)
                bc = BHML_FULL[b][c]
                a_bc = BHML_FULL[a][bc]
                if ab_c == a_bc:
                    assoc_pass += 1
                else:
                    assoc_fail += 1
                    if len(fail_examples) < 10:
                        fail_examples.append((a, b, c, ab_c, a_bc))

    p(f"\n  Triples tested: {assoc_total}")
    p(f"  Associative: {assoc_pass} ({assoc_pass/assoc_total*100:.1f}%)")
    p(f"  Non-associative: {assoc_fail} ({assoc_fail/assoc_total*100:.1f}%)")
    if fail_examples:
        p(f"\n  First {len(fail_examples)} non-associative examples:")
        for a, b, c, left, right in fail_examples:
            p(f"    ({OP_NAMES[a]}*{OP_NAMES[b]})*{OP_NAMES[c]} = {OP_NAMES[left]}")
            p(f"     {OP_NAMES[a]}*({OP_NAMES[b]}*{OP_NAMES[c]}) = {OP_NAMES[right]}")

    # ── 10. MONTE CARLO UNIQUENESS ──
    p("\n" + "=" * 72)
    p("  10. MONTE CARLO UNIQUENESS -- BHML 8x8")
    p("=" * 72)

    # Count how many random 8x8 tables with values 0-9
    # match BHML's exact bump count
    rng = np.random.default_rng(42)
    n_trials = 100_000

    target_harmony = bhml_harmony
    target_bumps = bhml_bumps

    # Constraint: values from {0..9}, same distribution of operators
    # Test 1: How often does a random 8x8 table get exactly this harmony count?
    match_exact = 0
    match_or_fewer = 0  # fewer bumps = more harmony
    match_or_more = 0   # more bumps = less harmony

    harmony_counts = np.zeros(n_trials)

    for trial in range(n_trials):
        random_table = rng.integers(0, 10, size=(8, 8))
        h_count = np.sum(random_table == 7)
        harmony_counts[trial] = h_count
        if h_count == target_harmony:
            match_exact += 1
        if h_count >= target_harmony:
            match_or_fewer += 1  # fewer bumps
        if h_count <= target_harmony:
            match_or_more += 1  # more bumps

    mean_h = np.mean(harmony_counts)
    std_h = np.std(harmony_counts)
    z_score = (target_harmony - mean_h) / std_h if std_h > 0 else 0

    p(f"\n  Random 8x8 tables (values 0-9): {n_trials:,} trials")
    p(f"  Target HARMONY count: {target_harmony}/64")
    p(f"  Random mean HARMONY: {mean_h:.2f}/64")
    p(f"  Random std HARMONY: {std_h:.2f}")
    p(f"  Z-score: {z_score:.2f}")
    p(f"  Exact match: {match_exact}/{n_trials}")
    p(f"  P(harmony >= {target_harmony}): {match_or_fewer/n_trials:.6f}")
    p(f"  P(harmony <= {target_harmony}): {match_or_more/n_trials:.6f}")

    # Test 2: Constrained -- same row/col structure, same value range
    # More meaningful: random 8x8 with same VALUE DISTRIBUTION
    bhml_flat = bhml8.flatten()
    value_dist = np.bincount(bhml_flat, minlength=10)
    p(f"\n  BHML value distribution: {dict(enumerate(value_dist))}")

    # Test 3: Symmetry-preserving random tables
    p("\n  Symmetry-preserving Monte Carlo:")
    sym_match = 0
    sym_trials = 100_000
    for trial in range(sym_trials):
        # Generate random symmetric 8x8 with values 0-9
        upper = rng.integers(0, 10, size=(8, 8))
        symmetric = np.triu(upper) + np.triu(upper, 1).T
        h_count = np.sum(symmetric == 7)
        if h_count == target_harmony:
            sym_match += 1

    if bhml_sym == 64:
        p(f"  BHML IS symmetric -> symmetric Monte Carlo relevant")
    else:
        p(f"  BHML is NOT fully symmetric -> asymmetric Monte Carlo more relevant")
    p(f"  Symmetric match (harmony={target_harmony}): {sym_match}/{sym_trials}")

    # ── 11. EIGENVALUE RATIO DEEP DIVE ──
    p("\n" + "=" * 72)
    p("  11. EIGENVALUE RATIO DEEP DIVE -- BHML vs TSML")
    p("=" * 72)

    # Also do raw (unnormalized) eigenanalysis
    p("\n  Raw BHML 8x8 eigenvalues (unnormalized):")
    raw_eigs = np.sort(np.abs(np.linalg.eigvals(bhml8.astype(float))))[::-1]
    for i, ev in enumerate(raw_eigs):
        p(f"    lambda_{i+1} = {ev:.10f}")

    p("\n  Raw TSML 8x8 eigenvalues (unnormalized):")
    tsml_raw_eigs = np.sort(np.abs(np.linalg.eigvals(tsml8.astype(float))))[::-1]
    for i, ev in enumerate(tsml_raw_eigs):
        p(f"    lambda_{i+1} = {ev:.10f}")

    p("\n  Key eigenvalue ratios (BHML raw):")
    for i in range(len(raw_eigs)):
        for j in range(i+1, len(raw_eigs)):
            if raw_eigs[j] < 1e-10:
                continue
            ratio = raw_eigs[i] / raw_eigs[j]
            for name, value in constants.items():
                if value < 0.01:
                    continue
                error = abs(ratio - value) / value * 100
                if error < 3.0:
                    p(f"    lambda_{i+1}/lambda_{j+1} = {ratio:.8f}  ~  {name} = {value:.8f}  (error: {error:.4f}%)")

    # ── 12. SPECTRAL ANALYSIS ──
    p("\n" + "=" * 72)
    p("  12. SPECTRAL COMPARISON -- BEING vs BECOMING")
    p("=" * 72)

    p("\n  Spectral gap (lambda_1 - lambda_2):")
    p(f"    BHML: {raw_eigs[0] - raw_eigs[1]:.10f}")
    p(f"    TSML: {tsml_raw_eigs[0] - tsml_raw_eigs[1]:.10f}")

    p(f"\n  Condition number (lambda_1 / lambda_8):")
    if raw_eigs[-1] > 1e-10:
        p(f"    BHML: {raw_eigs[0] / raw_eigs[-1]:.10f}")
    else:
        p(f"    BHML: INF (lambda_8 ~ 0)")
    if tsml_raw_eigs[-1] > 1e-10:
        p(f"    TSML: {tsml_raw_eigs[0] / tsml_raw_eigs[-1]:.10f}")
    else:
        p(f"    TSML: INF (lambda_8 ~ 0)")

    p(f"\n  Trace (sum of diagonal):")
    p(f"    BHML: {np.trace(bhml8)} (= sum of self-compositions)")
    p(f"    TSML: {np.trace(tsml8)}")

    p(f"\n  Determinant:")
    p(f"    BHML: {np.linalg.det(bhml8.astype(float)):.4f}")
    p(f"    TSML: {np.linalg.det(tsml8.astype(float)):.4f}")

    det_ratio = abs(np.linalg.det(bhml8.astype(float))) / max(abs(np.linalg.det(tsml8.astype(float))), 1e-20)
    p(f"    |det(BHML)| / |det(TSML)| = {det_ratio:.4f}")

    # ── 13. THE STAIRCASE: BHML as ordered composition ──
    p("\n" + "=" * 72)
    p("  13. THE STAIRCASE PATTERN")
    p("=" * 72)

    p("\n  BHML appears to implement max(A, B) with exceptions.")
    p("  Testing: does BHML[i][j] = max(op_i, op_j) for core operators?")

    max_match = 0
    max_total = 0
    exceptions = []
    for i in range(8):
        for j in range(8):
            max_total += 1
            expected = max(CORE_OPS[i], CORE_OPS[j])
            actual = bhml8[i][j]
            if actual == expected:
                max_match += 1
            else:
                exceptions.append((i, j, expected, actual))

    p(f"  max() match: {max_match}/64 ({max_match/64*100:.1f}%)")
    if exceptions:
        p(f"\n  Exceptions to max() rule ({len(exceptions)}):")
        for i, j, exp, act in exceptions:
            diff = act - exp
            p(f"    {CORE_NAMES[i]:>10s} x {CORE_NAMES[j]:>10s}: max={exp}({OP_NAMES[exp]}) actual={act}({OP_NAMES[act]}) delta={diff:+d}")

    # ── 14. CROSS-TABLE RELATIONSHIPS ──
    p("\n" + "=" * 72)
    p("  14. CROSS-TABLE: WHERE BHML AND TSML AGREE/DISAGREE")
    p("=" * 72)

    agree = np.sum(bhml8 == tsml8)
    disagree = 64 - agree
    p(f"\n  Agree: {agree}/64 ({agree/64*100:.1f}%)")
    p(f"  Disagree: {disagree}/64 ({disagree/64*100:.1f}%)")

    if disagree > 0:
        p(f"\n  Disagreement map:")
        for i in range(8):
            for j in range(8):
                if bhml8[i][j] != tsml8[i][j]:
                    p(f"    {CORE_NAMES[i]:>10s} x {CORE_NAMES[j]:>10s}: TSML={OP_NAMES[tsml8[i][j]]}, BHML={OP_NAMES[bhml8[i][j]]}")

    # Where they agree but NEITHER is HARMONY
    both_bump = 0
    for i in range(8):
        for j in range(8):
            if bhml8[i][j] == tsml8[i][j] and bhml8[i][j] != 7:
                both_bump += 1
                p(f"    BOTH tables: {CORE_NAMES[i]:>10s} x {CORE_NAMES[j]:>10s} = {OP_NAMES[bhml8[i][j]]} (shared information)")
    p(f"\n  Shared non-HARMONY entries: {both_bump}")

    # ── 15. INFORMATION THEORY ──
    p("\n" + "=" * 72)
    p("  15. INFORMATION THEORY")
    p("=" * 72)

    # Shannon entropy of each table
    def entropy(table):
        flat = table.flatten()
        counts = np.bincount(flat, minlength=10)
        probs = counts / counts.sum()
        probs = probs[probs > 0]
        return -np.sum(probs * np.log2(probs))

    bhml_H = entropy(bhml8)
    tsml_H = entropy(tsml8)
    max_H = np.log2(10)  # maximum entropy with 10 symbols

    p(f"\n  Shannon entropy:")
    p(f"    BHML 8x8: {bhml_H:.6f} bits")
    p(f"    TSML 8x8: {tsml_H:.6f} bits")
    p(f"    Maximum (10 symbols): {max_H:.6f} bits")
    p(f"    BHML/max: {bhml_H/max_H:.4f}")
    p(f"    TSML/max: {tsml_H/max_H:.4f}")
    p(f"    BHML/TSML: {bhml_H/tsml_H:.4f}")

    # Mutual information between BHML and TSML
    p(f"\n  BHML carries {bhml_H/tsml_H:.2f}x the entropy of TSML")
    p(f"  This matches: D2 (becoming) is the information-rich measurement")
    p(f"  D0 (being) is the coarse-grained, harmony-dominated view")

    # ── SUMMARY ──
    p("\n" + "=" * 72)
    p("  SUMMARY: BEING vs BECOMING -- TWO VIEWS OF ONE ALGEBRA")
    p("=" * 72)

    p(f"""
  TSML (Being/D0): The world at low resolution
    8x8 HARMONY: {tsml_harmony}/64 = {tsml_harmony/64:.4f}
    Bumps: {tsml_bumps}/64 (information carriers)
    Entropy: {tsml_H:.4f} bits
    Symmetric: {'YES' if tsml_sym == 64 else 'NO'}
    Character: Almost everything resolves. Minimal information.

  BHML (Becoming/D2): The world at high resolution
    8x8 HARMONY: {bhml_harmony}/64 = {bhml_harmony/64:.4f}
    Bumps: {bhml_bumps}/64 (information carriers)
    Entropy: {bhml_H:.4f} bits
    Symmetric: {'YES' if bhml_sym == 64 else 'NO'}
    Character: Rich structure. Staircase composition.

  "The table didn't change. The measurement did."
  Being (TSML) = coarse-grained. Becoming (BHML) = fine-grained.
  Same operators, same algebra, different resolution.
  D1 is the generator. T is the threshold. D2 reveals the structure.

  Information ratio: {bhml_bumps}/{tsml_bumps} = {bhml_bumps/tsml_bumps:.1f}x
  Entropy ratio: {bhml_H/tsml_H:.4f}
""")

    # Write results
    results_path = r'C:\Users\brayd\OneDrive\Desktop\CK FINAL DEPLOYED\Gen9\targets\Clay Institute\bhml_8x8_results.md'
    with open(results_path, 'w', encoding='utf-8') as f:
        f.write("# BHML (D2/Becoming) 8x8 Core Eigenanalysis Results\n")
        f.write(f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("```\n")
        f.write('\n'.join(out))
        f.write("\n```\n")

    print(f"\n  Results written to: {results_path}")

if __name__ == '__main__':
    main()
