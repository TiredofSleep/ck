#!/usr/bin/env python3
"""
reality_anchors.py -- Rigorous Mathematical Analysis of the CK CL Table
=========================================================================

CK Gen 9.21 -- The Coherence Keeper
Brayden Sanders / 7Site LLC

Analyses:
  1. Markov Chain / Semigroup (eigenvalues, stationary distribution)
  2. Physical Constant Search (eigenvalue ratios, T* powers, etc.)
  3. Expanded Monte Carlo (CL table uniqueness among 100k random tables)
  4. CL Semigroup Properties (associativity, idempotents, periods)
  5. Conservation Laws / Invariants (5D vector currents)
  6. T* and 73% Relationships (number theory, entropy)

Requires: numpy (only)
Run:      python reality_anchors.py
"""

import numpy as np
from collections import Counter
from math import gcd, log2, log, factorial, sqrt, pi, e as EULER_E
from fractions import Fraction
import os
import sys
import time

# ──────────────────────────────────────────────────────────────────
# CL TABLES
# ──────────────────────────────────────────────────────────────────

TSML = np.array([
    [0, 0, 0, 0, 0, 0, 0, 7, 0, 0],  # VOID
    [0, 7, 3, 7, 7, 7, 7, 7, 7, 7],  # LATTICE
    [0, 3, 7, 7, 4, 7, 7, 7, 7, 9],  # COUNTER
    [0, 7, 7, 7, 7, 7, 7, 7, 7, 3],  # PROGRESS
    [0, 7, 4, 7, 7, 7, 7, 7, 8, 7],  # COLLAPSE
    [0, 7, 7, 7, 7, 7, 7, 7, 7, 7],  # BALANCE
    [0, 7, 7, 7, 7, 7, 7, 7, 7, 7],  # CHAOS
    [7, 7, 7, 7, 7, 7, 7, 7, 7, 7],  # HARMONY (absorbing)
    [0, 7, 7, 7, 8, 7, 7, 7, 7, 7],  # BREATH
    [0, 7, 9, 3, 7, 7, 7, 7, 7, 7],  # RESET
], dtype=float)

BHML = np.array([
    [0, 0, 0, 0, 0, 0, 0, 7, 0, 0],
    [0, 7, 3, 7, 1, 5, 6, 7, 1, 4],
    [0, 3, 7, 7, 4, 5, 6, 7, 2, 9],
    [0, 7, 7, 7, 4, 3, 6, 7, 7, 3],
    [0, 1, 4, 4, 7, 6, 6, 7, 8, 9],
    [0, 5, 5, 3, 6, 6, 6, 7, 5, 3],
    [0, 6, 6, 6, 6, 6, 7, 7, 6, 6],
    [7, 7, 7, 7, 7, 7, 7, 8, 7, 7],
    [0, 1, 2, 7, 8, 5, 6, 7, 7, 1],
    [0, 4, 9, 3, 9, 3, 6, 7, 1, 7],
], dtype=float)

OP_NAMES = [
    "VOID", "LATTICE", "COUNTER", "PROGRESS", "COLLAPSE",
    "BALANCE", "CHAOS", "HARMONY", "BREATH", "RESET"
]

T_STAR = 5.0 / 7.0  # 0.714285714285...

# ──────────────────────────────────────────────────────────────────
# HELPER: output collector
# ──────────────────────────────────────────────────────────────────

class Report:
    """Collects printed output for both console and markdown."""
    def __init__(self):
        self.lines = []

    def print(self, *args, **kwargs):
        import io
        buf = io.StringIO()
        print(*args, file=buf, **kwargs)
        text = buf.getvalue()
        sys.stdout.write(text)
        self.lines.append(text)

    def section(self, title):
        bar = "=" * 72
        self.print(f"\n{bar}")
        self.print(f"  {title}")
        self.print(bar)

    def subsection(self, title):
        self.print(f"\n--- {title} ---")

    def get_text(self):
        return "".join(self.lines)


R = Report()

# ──────────────────────────────────────────────────────────────────
# ANALYSIS 1: Markov Chain / Semigroup Analysis
# ──────────────────────────────────────────────────────────────────

def analysis_1_markov():
    R.section("ANALYSIS 1: Markov Chain / Semigroup Analysis")

    # -- Basic table statistics --
    R.subsection("TSML Table Statistics")
    harmony_count = int(np.sum(TSML == 7))
    R.print(f"  Total entries:     100")
    R.print(f"  HARMONY (7) count: {harmony_count}")
    R.print(f"  HARMONY fraction:  {harmony_count}/100 = {harmony_count/100:.4f}")
    R.print(f"  T* = 5/7 =        {T_STAR:.10f}")
    R.print(f"  Difference:        {abs(harmony_count/100 - T_STAR):.10f}")

    # Value distribution
    R.subsection("Value Distribution in TSML")
    vals, counts = np.unique(TSML.astype(int), return_counts=True)
    for v, c in zip(vals, counts):
        name = OP_NAMES[int(v)] if 0 <= int(v) <= 9 else str(int(v))
        R.print(f"  {int(v)} ({name:>8s}): {c:3d} entries ({c:.0f}%)")

    # BHML statistics
    R.subsection("BHML Table Statistics")
    bhml_harmony = int(np.sum(BHML == 7))
    R.print(f"  HARMONY (7) count: {bhml_harmony}")
    R.print(f"  HARMONY fraction:  {bhml_harmony}/100 = {bhml_harmony/100:.4f}")

    R.subsection("Value Distribution in BHML")
    vals_b, counts_b = np.unique(BHML.astype(int), return_counts=True)
    for v, c in zip(vals_b, counts_b):
        name = OP_NAMES[int(v)] if 0 <= int(v) <= 9 else str(int(v))
        R.print(f"  {int(v)} ({name:>8s}): {c:3d} entries ({c:.0f}%)")

    # -- Normalize to transition matrix --
    R.subsection("Normalized Transition Matrix (TSML)")

    T_matrix = TSML.copy()
    row_sums = T_matrix.sum(axis=1)
    # Avoid division by zero for the VOID row (sum=7)
    row_sums[row_sums == 0] = 1.0
    T_norm = T_matrix / row_sums[:, np.newaxis]

    R.print("  Row sums before normalization:")
    for i in range(10):
        R.print(f"    {OP_NAMES[i]:>8s}: {TSML[i].sum():.0f}")

    # -- Eigenvalue decomposition --
    R.subsection("Eigenvalues of Normalized TSML")

    eigenvalues, eigenvectors = np.linalg.eig(T_norm.T)

    # Sort by magnitude (descending)
    idx = np.argsort(-np.abs(eigenvalues))
    eigenvalues = eigenvalues[idx]
    eigenvectors = eigenvectors[:, idx]

    for i, ev in enumerate(eigenvalues):
        mag = abs(ev)
        R.print(f"  lambda_{i}: {ev.real:+.10f} {'+' if ev.imag >= 0 else ''}{ev.imag:.10f}i  |lambda| = {mag:.10f}")

    # -- Stationary distribution --
    R.subsection("Stationary Distribution (left eigenvector for lambda=1)")

    # Find eigenvector closest to eigenvalue 1
    one_idx = np.argmin(np.abs(eigenvalues - 1.0))
    stat_vec = eigenvectors[:, one_idx].real
    stat_vec = stat_vec / stat_vec.sum()  # normalize to probability

    R.print(f"  Eigenvalue used: {eigenvalues[one_idx]:.10f} (index {one_idx})")
    R.print(f"  Stationary distribution:")
    for i in range(10):
        R.print(f"    {OP_NAMES[i]:>8s}: {stat_vec[i]:.10f}")

    harmony_weight = stat_vec[7]
    R.print(f"\n  HARMONY weight in stationary dist: {harmony_weight:.10f}")
    R.print(f"  Target (73%):                      0.7300000000")
    R.print(f"  Difference:                        {abs(harmony_weight - 0.73):.10f}")

    # -- Spectral gap --
    R.subsection("Spectral Gap")
    sorted_mags = sorted(np.abs(eigenvalues), reverse=True)
    if len(sorted_mags) >= 2:
        gap = sorted_mags[0] - sorted_mags[1]
        R.print(f"  Largest |lambda|:  {sorted_mags[0]:.10f}")
        R.print(f"  2nd largest:       {sorted_mags[1]:.10f}")
        R.print(f"  Spectral gap:      {gap:.10f}")
        if sorted_mags[1] > 0:
            mixing_time = 1.0 / (1.0 - sorted_mags[1])
            R.print(f"  Approx mixing time: {mixing_time:.4f} steps")

    # -- BHML eigenvalues for comparison --
    R.subsection("Eigenvalues of Normalized BHML")
    B_matrix = BHML.copy()
    b_row_sums = B_matrix.sum(axis=1)
    b_row_sums[b_row_sums == 0] = 1.0
    B_norm = B_matrix / b_row_sums[:, np.newaxis]

    b_eigenvalues, b_eigenvectors = np.linalg.eig(B_norm.T)
    b_idx = np.argsort(-np.abs(b_eigenvalues))
    b_eigenvalues = b_eigenvalues[b_idx]

    for i, ev in enumerate(b_eigenvalues):
        mag = abs(ev)
        R.print(f"  lambda_{i}: {ev.real:+.10f} {'+' if ev.imag >= 0 else ''}{ev.imag:.10f}i  |lambda| = {mag:.10f}")

    return eigenvalues, stat_vec, T_norm, sorted_mags


# ──────────────────────────────────────────────────────────────────
# ANALYSIS 2: Physical Constant Search
# ──────────────────────────────────────────────────────────────────

def analysis_2_constants(eigenvalues, stat_vec, sorted_mags):
    R.section("ANALYSIS 2: Physical Constant Search")

    CONSTANTS = {
        "fine-structure alpha":          1.0 / 137.035999,
        "1/alpha (137.036)":             137.035999,
        "proton/electron mass ratio":    1836.152673,
        "golden ratio phi":              (1 + sqrt(5)) / 2,
        "1/phi":                         2 / (1 + sqrt(5)),
        "phi - 1":                       (sqrt(5) - 1) / 2,
        "e (Euler)":                     EULER_E,
        "1/e":                           1.0 / EULER_E,
        "pi":                            pi,
        "1/pi":                          1.0 / pi,
        "2*pi":                          2 * pi,
        "sqrt(2)":                       sqrt(2),
        "1/sqrt(2)":                     1.0 / sqrt(2),
        "Euler-Mascheroni gamma":        0.5772156649,
        "ln(2)":                         log(2),
        "ln(10)":                        log(10),
        "Feigenbaum delta":              4.66920160910,
        "Feigenbaum alpha_F":            2.50290787509,
        "Catalan constant":              0.9159655941,
        "Apery's constant zeta(3)":      1.2020569031,
        "sqrt(3)":                       sqrt(3),
        "sqrt(5)":                       sqrt(5),
        "T* = 5/7":                      T_STAR,
        "2*T*":                          2 * T_STAR,
        "T*^2":                          T_STAR ** 2,
        "1 - T*":                        1 - T_STAR,
        "7/5":                           7.0 / 5.0,
    }

    # Collect candidate values from the analysis
    candidates = {}

    # From eigenvalues
    real_eigs = [ev.real for ev in eigenvalues if abs(ev.imag) < 1e-10 and abs(ev.real) > 1e-10]
    for i, v in enumerate(real_eigs):
        candidates[f"eigenvalue[{i}]"] = v
        if abs(v) > 1e-10:
            candidates[f"1/eigenvalue[{i}]"] = 1.0 / v

    # Eigenvalue magnitude ratios
    nonzero_mags = [m for m in sorted_mags if m > 1e-10]
    for i in range(len(nonzero_mags)):
        for j in range(i + 1, len(nonzero_mags)):
            if nonzero_mags[j] > 1e-10:
                ratio = nonzero_mags[i] / nonzero_mags[j]
                candidates[f"|lambda_{i}|/|lambda_{j}|"] = ratio

    # From stationary distribution
    for i in range(10):
        if abs(stat_vec[i]) > 1e-10:
            candidates[f"stat[{OP_NAMES[i]}]"] = stat_vec[i]

    # Stationary distribution ratios
    nonzero_stat = [(i, stat_vec[i]) for i in range(10) if abs(stat_vec[i]) > 1e-10]
    for ia, (i, vi) in enumerate(nonzero_stat):
        for ib, (j, vj) in enumerate(nonzero_stat):
            if i != j and abs(vj) > 1e-10:
                candidates[f"stat[{OP_NAMES[i]}]/stat[{OP_NAMES[j]}]"] = vi / vj

    # Powers of T*
    for n in range(1, 20):
        candidates[f"T*^{n}"] = T_STAR ** n
        candidates[f"(1-T*)^{n}"] = (1 - T_STAR) ** n

    # CL structural properties
    candidates["73/100"] = 0.73
    candidates["27/100"] = 0.27
    candidates["73/27"] = 73.0 / 27.0
    candidates["27/73"] = 27.0 / 73.0
    candidates["non-harmony/total"] = 27.0 / 100.0
    candidates["73 (as number)"] = 73.0
    candidates["27 (as number)"] = 27.0
    candidates["sqrt(73)"] = sqrt(73)
    candidates["sqrt(27)"] = sqrt(27)
    candidates["log2(73)"] = log2(73)

    # BHML harmony count
    bhml_h = int(np.sum(BHML == 7))
    candidates["BHML_harmony/100"] = bhml_h / 100.0
    candidates["TSML_h - BHML_h"] = (73 - bhml_h)
    candidates["TSML_h / BHML_h"] = 73.0 / bhml_h if bhml_h > 0 else 0

    # Search for matches
    TOLERANCES = [0.01, 0.02, 0.05]

    for tol in TOLERANCES:
        R.subsection(f"Matches within {tol*100:.0f}% tolerance")
        found_any = False
        for cname, cval in sorted(candidates.items()):
            for kname, kval in CONSTANTS.items():
                if abs(kval) < 1e-15:
                    continue
                rel_err = abs(cval - kval) / abs(kval)
                if rel_err <= tol:
                    R.print(f"  {cname} = {cval:.10f}")
                    R.print(f"    ~ {kname} = {kval:.10f}")
                    R.print(f"    relative error: {rel_err:.6e} ({rel_err*100:.4f}%)")
                    R.print()
                    found_any = True
        if not found_any:
            R.print("  (no matches found at this tolerance)")

    # Special check: T* vs 73%
    R.subsection("T* vs 73% Direct Comparison")
    R.print(f"  T* = 5/7         = {T_STAR:.15f}")
    R.print(f"  73/100           = {0.73:.15f}")
    R.print(f"  Difference:        {abs(T_STAR - 0.73):.15f}")
    R.print(f"  Relative diff:     {abs(T_STAR - 0.73)/T_STAR * 100:.6f}%")
    R.print(f"  73/100 / T* =      {0.73 / T_STAR:.15f}")
    R.print(f"  T* / (73/100) =    {T_STAR / 0.73:.15f}")

    # Check: is 73 entries the NEAREST integer count to T* * 100?
    nearest = round(T_STAR * 100)
    R.print(f"\n  Nearest integer to T* * 100: {nearest}")
    R.print(f"  Actual HARMONY count:        73")
    R.print(f"  Floor(T* * 100):             {int(T_STAR * 100)}")
    R.print(f"  Ceil(T* * 100):              {int(T_STAR * 100) + 1}")


# ──────────────────────────────────────────────────────────────────
# ANALYSIS 3: Expanded Monte Carlo
# ──────────────────────────────────────────────────────────────────

def analysis_3_monte_carlo():
    R.section("ANALYSIS 3: Expanded Monte Carlo (CL Table Uniqueness)")

    N_TRIALS = 100_000
    rng = np.random.default_rng(seed=42)

    # ---- STRICT constraints (matching TSML structure) ----
    R.subsection(f"Strict Constraints ({N_TRIALS:,} random tables)")
    R.print("  Constraints:")
    R.print("    - Values 0-9 only")
    R.print("    - Row 0 (VOID): all zeros except one random position = 7")
    R.print("    - Row 7 (HARMONY): all entries = 7 (absorbing)")
    R.print("    - Column 0: all zeros except row 7 = 7")
    R.print("    - Remaining 72 free cells: random 0-9")

    strict_counts = np.zeros(N_TRIALS, dtype=int)
    t0 = time.time()

    for trial in range(N_TRIALS):
        table = np.zeros((10, 10), dtype=int)

        # Row 0 (VOID): all zeros except one position = 7
        void_pos = rng.integers(0, 10)
        table[0, void_pos] = 7

        # Row 7 (HARMONY): all 7s
        table[7, :] = 7

        # Column 0: all zeros except row 7
        table[:, 0] = 0
        table[7, 0] = 7

        # Fill remaining free cells (rows 1-6, 8-9; cols 1-9; excluding row 7)
        for r in range(10):
            if r == 0 or r == 7:
                continue
            for c in range(1, 10):
                table[r, c] = rng.integers(0, 10)

        strict_counts[trial] = np.sum(table == 7)

    elapsed = time.time() - t0
    R.print(f"  Elapsed: {elapsed:.1f}s")

    # Statistics
    mean_s = np.mean(strict_counts)
    std_s = np.std(strict_counts)
    min_s = np.min(strict_counts)
    max_s = np.max(strict_counts)
    pct = np.sum(strict_counts >= 73) / N_TRIALS * 100

    R.print(f"\n  HARMONY count distribution (strict):")
    R.print(f"    Mean:   {mean_s:.2f}")
    R.print(f"    Std:    {std_s:.2f}")
    R.print(f"    Min:    {min_s}")
    R.print(f"    Max:    {max_s}")
    R.print(f"    Median: {np.median(strict_counts):.0f}")
    R.print(f"\n  Actual TSML HARMONY count: 73")
    R.print(f"  Tables with >= 73 HARMONY: {np.sum(strict_counts >= 73):,} / {N_TRIALS:,} ({pct:.4f}%)")
    R.print(f"  Tables with == 73 HARMONY: {np.sum(strict_counts == 73):,} / {N_TRIALS:,}")
    R.print(f"  Percentile of 73: {np.sum(strict_counts < 73) / N_TRIALS * 100:.4f}%")

    # Z-score
    if std_s > 0:
        z = (73 - mean_s) / std_s
        R.print(f"  Z-score of 73:    {z:.4f} standard deviations above mean")

    # Histogram (text-based)
    R.subsection("Histogram of HARMONY counts (strict constraints)")
    hist_bins = np.arange(min_s, max_s + 2) - 0.5
    hist_vals, bin_edges = np.histogram(strict_counts, bins=hist_bins)
    max_bar = max(hist_vals) if len(hist_vals) > 0 else 1
    # Show condensed histogram
    for i in range(len(hist_vals)):
        val = int(bin_edges[i] + 0.5)
        bar_len = int(hist_vals[i] / max_bar * 50)
        marker = " <-- TSML" if val == 73 else ""
        if hist_vals[i] > 0 or abs(val - 73) < 5:
            R.print(f"    {val:3d}: {'#' * bar_len} ({hist_vals[i]:,}){marker}")

    # ---- RELAXED constraints ----
    R.subsection(f"Relaxed Constraints ({N_TRIALS:,} random tables)")
    R.print("  Constraints:")
    R.print("    - Values 0-9 only")
    R.print("    - One designated absorbing row: all entries = 7")
    R.print("    - Column 0: all zeros except absorbing row = 7")
    R.print("    - All other 81 cells: random 0-9")

    relaxed_counts = np.zeros(N_TRIALS, dtype=int)
    t0 = time.time()

    for trial in range(N_TRIALS):
        table = rng.integers(0, 10, size=(10, 10))

        # Absorbing row (row 7): all 7s
        table[7, :] = 7

        # Column 0: all zeros except row 7
        table[:, 0] = 0
        table[7, 0] = 7

        relaxed_counts[trial] = np.sum(table == 7)

    elapsed = time.time() - t0
    R.print(f"  Elapsed: {elapsed:.1f}s")

    mean_r = np.mean(relaxed_counts)
    std_r = np.std(relaxed_counts)
    pct_r = np.sum(relaxed_counts >= 73) / N_TRIALS * 100

    R.print(f"\n  HARMONY count distribution (relaxed):")
    R.print(f"    Mean:   {mean_r:.2f}")
    R.print(f"    Std:    {std_r:.2f}")
    R.print(f"    Min:    {np.min(relaxed_counts)}")
    R.print(f"    Max:    {np.max(relaxed_counts)}")
    R.print(f"\n  Tables with >= 73 HARMONY: {np.sum(relaxed_counts >= 73):,} / {N_TRIALS:,} ({pct_r:.4f}%)")
    R.print(f"  Percentile of 73: {np.sum(relaxed_counts < 73) / N_TRIALS * 100:.4f}%")

    if std_r > 0:
        z_r = (73 - mean_r) / std_r
        R.print(f"  Z-score of 73:    {z_r:.4f} standard deviations above mean")

    return strict_counts, relaxed_counts


# ──────────────────────────────────────────────────────────────────
# ANALYSIS 4: CL Semigroup Properties
# ──────────────────────────────────────────────────────────────────

def analysis_4_semigroup():
    R.section("ANALYSIS 4: CL Semigroup Properties")

    CL = TSML.astype(int)

    # ---- Associativity check ----
    R.subsection("Associativity: CL[CL[a][b]][c] == CL[a][CL[b][c]]?")

    assoc_pass = 0
    assoc_fail = 0
    fail_examples = []

    for a in range(10):
        for b in range(10):
            for c in range(10):
                left = CL[CL[a][b]][c]   # (a * b) * c
                right = CL[a][CL[b][c]]  # a * (b * c)
                if left == right:
                    assoc_pass += 1
                else:
                    assoc_fail += 1
                    if len(fail_examples) < 10:
                        fail_examples.append((a, b, c, left, right))

    total = 10 ** 3
    R.print(f"  Total triples:      {total}")
    R.print(f"  Associative:        {assoc_pass} ({assoc_pass/total*100:.2f}%)")
    R.print(f"  Non-associative:    {assoc_fail} ({assoc_fail/total*100:.2f}%)")

    if fail_examples:
        R.print(f"\n  First {len(fail_examples)} failures:")
        for a, b, c, l, r in fail_examples:
            R.print(f"    ({OP_NAMES[a]} * {OP_NAMES[b]}) * {OP_NAMES[c]} = "
                     f"{OP_NAMES[l]}  but  {OP_NAMES[a]} * ({OP_NAMES[b]} * {OP_NAMES[c]}) = {OP_NAMES[r]}")

    # ---- Same for BHML ----
    R.subsection("Associativity in BHML")
    CL_B = BHML.astype(int)
    b_pass = 0
    for a in range(10):
        for b in range(10):
            for c in range(10):
                if CL_B[CL_B[a][b]][c] == CL_B[a][CL_B[b][c]]:
                    b_pass += 1
    R.print(f"  Associative triples: {b_pass} / {total} ({b_pass/total*100:.2f}%)")

    # ---- Bump pairs (non-HARMONY results in TSML) ----
    R.subsection("Bump Pairs (non-HARMONY results in TSML)")
    bump_pairs = []
    for a in range(10):
        for b in range(10):
            val = CL[a][b]
            if val != 7:
                bump_pairs.append((a, b, val))

    R.print(f"  Total bump pairs: {len(bump_pairs)} (out of 100)")
    R.print(f"  These are the 'non-trivial' compositions:")
    for a, b, v in bump_pairs:
        R.print(f"    {OP_NAMES[a]:>8s} * {OP_NAMES[b]:<8s} = {OP_NAMES[v]} ({v})")

    # ---- Idempotents ----
    R.subsection("Idempotent Operators: CL[a][a] = a")
    for a in range(10):
        if CL[a][a] == a:
            R.print(f"  {OP_NAMES[a]} ({a}) is idempotent")
        else:
            R.print(f"  {OP_NAMES[a]} ({a}): CL[{a}][{a}] = {CL[a][a]} ({OP_NAMES[CL[a][a]]})")

    # ---- Nilpotent check ----
    R.subsection("Nilpotent Operators (self-compose until VOID or cycle)")
    for a in range(10):
        chain = [a]
        current = a
        seen = {a}
        for step in range(20):
            current = CL[current][current]
            chain.append(current)
            if current == 0:
                R.print(f"  {OP_NAMES[a]}: reaches VOID in {len(chain)-1} steps: {' -> '.join(OP_NAMES[x] for x in chain)}")
                break
            if current in seen:
                cycle_start = chain.index(current)
                R.print(f"  {OP_NAMES[a]}: cycles at step {len(chain)-1} "
                         f"(period {len(chain)-1-cycle_start}): {' -> '.join(OP_NAMES[x] for x in chain)}")
                break
            seen.add(current)
        else:
            R.print(f"  {OP_NAMES[a]}: no convergence in 20 steps")

    # ---- Operator periods (repeated composition with self) ----
    R.subsection("Operator Periods (repeated a*a*a*...)")
    for a in range(10):
        sequence = [a]
        current = a
        for step in range(100):
            current = CL[current][a]  # right-multiply by a repeatedly
            sequence.append(current)
            if current == sequence[0]:
                R.print(f"  {OP_NAMES[a]}: period = {step+1}")
                break
        else:
            # Find cycle in sequence
            for start in range(len(sequence)):
                for period in range(1, len(sequence) - start):
                    if start + 2 * period <= len(sequence):
                        if sequence[start:start+period] == sequence[start+period:start+2*period]:
                            R.print(f"  {OP_NAMES[a]}: absorbs to cycle starting at step {start}, "
                                     f"period {period}: {' -> '.join(OP_NAMES[x] for x in sequence[start:start+period])}")
                            break
                else:
                    continue
                break
            else:
                R.print(f"  {OP_NAMES[a]}: no simple period found in 100 steps")

    # ---- Left/right ideals ----
    R.subsection("Absorbing / Left-Zero / Right-Zero Elements")
    for a in range(10):
        left_zero = all(CL[a][b] == a for b in range(10))
        right_zero = all(CL[b][a] == a for b in range(10))
        absorbing = all(CL[a][b] == a and CL[b][a] == a for b in range(10))
        if absorbing:
            R.print(f"  {OP_NAMES[a]}: ABSORBING (left-zero AND right-zero)")
        elif left_zero:
            R.print(f"  {OP_NAMES[a]}: LEFT-ZERO (a*b = a for all b)")
        elif right_zero:
            R.print(f"  {OP_NAMES[a]}: RIGHT-ZERO (b*a = a for all b)")

    # ---- Commutativity ----
    R.subsection("Commutativity: CL[a][b] == CL[b][a]?")
    comm_pass = 0
    comm_fail = 0
    comm_fail_ex = []
    for a in range(10):
        for b in range(a + 1, 10):
            if CL[a][b] == CL[b][a]:
                comm_pass += 1
            else:
                comm_fail += 1
                if len(comm_fail_ex) < 10:
                    comm_fail_ex.append((a, b, CL[a][b], CL[b][a]))

    total_pairs = 10 * 9 // 2
    R.print(f"  Commutative pairs: {comm_pass} / {total_pairs} ({comm_pass/total_pairs*100:.2f}%)")
    R.print(f"  Non-commutative:   {comm_fail}")
    if comm_fail_ex:
        R.print(f"  Non-commutative examples:")
        for a, b, ab, ba in comm_fail_ex:
            R.print(f"    {OP_NAMES[a]}*{OP_NAMES[b]} = {OP_NAMES[ab]},  {OP_NAMES[b]}*{OP_NAMES[a]} = {OP_NAMES[ba]}")

    return bump_pairs


# ──────────────────────────────────────────────────────────────────
# ANALYSIS 5: Conservation Laws / Invariants
# ──────────────────────────────────────────────────────────────────

def analysis_5_conservation():
    R.section("ANALYSIS 5: Conservation Laws / Invariants")

    CL = TSML.astype(int)

    # Define canonical 5D force vectors for each operator
    # 5 dimensions: aperture, pressure, depth, binding, continuity
    # Operators come in +/- pairs for each dimension, plus VOID and HARMONY
    # Based on D2 classification:
    #   aperture: LATTICE(+) / COLLAPSE(-)
    #   pressure: COUNTER(+) / BALANCE(-)
    #   depth:    PROGRESS(+) / CHAOS(-)
    #   binding:  BREATH(+) / RESET(-)
    #   continuity: HARMONY(+) / VOID(-)

    R.subsection("Canonical 5D Force Vectors")

    FORCE_VECTORS = {
        0: np.array([ 0.0,  0.0,  0.0,  0.0, -1.0]),  # VOID (continuity -)
        1: np.array([ 1.0,  0.0,  0.0,  0.0,  0.0]),  # LATTICE (aperture +)
        2: np.array([ 0.0,  1.0,  0.0,  0.0,  0.0]),  # COUNTER (pressure +)
        3: np.array([ 0.0,  0.0,  1.0,  0.0,  0.0]),  # PROGRESS (depth +)
        4: np.array([-1.0,  0.0,  0.0,  0.0,  0.0]),  # COLLAPSE (aperture -)
        5: np.array([ 0.0, -1.0,  0.0,  0.0,  0.0]),  # BALANCE (pressure -)
        6: np.array([ 0.0,  0.0, -1.0,  0.0,  0.0]),  # CHAOS (depth -)
        7: np.array([ 0.0,  0.0,  0.0,  0.0,  1.0]),  # HARMONY (continuity +)
        8: np.array([ 0.0,  0.0,  0.0,  1.0,  0.0]),  # BREATH (binding +)
        9: np.array([ 0.0,  0.0,  0.0, -1.0,  0.0]),  # RESET (binding -)
    }

    for op_id, vec in FORCE_VECTORS.items():
        R.print(f"  {OP_NAMES[op_id]:>8s}: {vec}")

    # ---- Linear invariant search ----
    R.subsection("Linear Invariant Search")
    R.print("  Testing: does there exist w such that w . F(CL[a][b]) = w . F(a) + w . F(b)?")
    R.print("  (A linear conserved 'charge' under CL composition)")

    # Build the system: for each (a, b), we need
    #   w . F(CL[a][b]) = w . F(a) + w . F(b)
    #   => w . (F(a) + F(b) - F(CL[a][b])) = 0
    # Collect all constraint vectors
    constraint_rows = []
    for a in range(10):
        for b in range(10):
            c = CL[a][b]
            diff = FORCE_VECTORS[a] + FORCE_VECTORS[b] - FORCE_VECTORS[c]
            constraint_rows.append(diff)

    A_matrix = np.array(constraint_rows)
    # Find null space of A_matrix
    U, S, Vt = np.linalg.svd(A_matrix)
    null_mask = S < 1e-10
    R.print(f"  Singular values of constraint matrix: {np.round(S, 6)}")
    R.print(f"  Number of near-zero singular values: {np.sum(null_mask)}")

    if np.sum(null_mask) > 0:
        # Null space vectors
        null_space = Vt[len(S) - np.sum(null_mask):]
        R.print(f"  Null space dimension: {null_space.shape[0]}")
        for i, vec in enumerate(null_space):
            R.print(f"  Invariant weight vector {i}: {np.round(vec, 6)}")
    else:
        R.print("  No exact linear invariant exists.")
        # Find the closest-to-zero singular value
        min_sv = np.min(S)
        min_idx = np.argmin(S)
        R.print(f"  Smallest singular value: {min_sv:.6f} (approximate invariant)")
        approx_invariant = Vt[min_idx]
        R.print(f"  Approximate invariant direction: {np.round(approx_invariant, 6)}")

    # ---- Multiplicative invariant search ----
    R.subsection("Multiplicative Invariant Search")
    R.print("  Testing: does there exist a mapping Q: operators -> R such that")
    R.print("  Q(CL[a][b]) = Q(a) * Q(b)  (semigroup homomorphism to (R, *))?")

    # For this to work: Q(7) must satisfy Q(7) = Q(7)*Q(x) for all x
    # => Q(7) = 0 or Q(x) = 1 for all x
    # If Q(7) != 0 then Q(x) = 1 for all x (trivial)
    # If Q(7) = 0 then Q(0) = Q(0)*Q(x) => Q(0) = 0 for any x with Q(x)!=1
    # Check bump pairs for constraints
    R.print("  HARMONY is absorbing => Q(HARMONY) must be 0 or all Q(x)=1")
    R.print("  Non-trivial homomorphism requires Q(HARMONY) = 0")

    # ---- Random walk variance analysis ----
    R.subsection("Random CL Walk Variance Analysis")
    R.print("  Running 10,000 random CL composition chains of length 50")
    R.print("  Tracking 5D 'current' (running sum of force vectors)")

    rng = np.random.default_rng(seed=73)
    N_WALKS = 10_000
    WALK_LEN = 50

    # Track variance of each dimension over walks
    final_currents = np.zeros((N_WALKS, 5))
    harmony_fracs = np.zeros(N_WALKS)
    dim_variances_by_step = np.zeros((WALK_LEN, 5))
    step_counts = np.zeros(WALK_LEN)

    for w in range(N_WALKS):
        # Start with random operator
        current_op = rng.integers(0, 10)
        current_vec = FORCE_VECTORS[current_op].copy()
        harmony_count = 1 if current_op == 7 else 0

        for step in range(WALK_LEN):
            next_input = rng.integers(0, 10)
            current_op = CL[current_op][next_input]
            current_vec += FORCE_VECTORS[current_op]
            if current_op == 7:
                harmony_count += 1

            dim_variances_by_step[step] += current_vec ** 2
            step_counts[step] += 1

        final_currents[w] = current_vec
        harmony_fracs[w] = harmony_count / (WALK_LEN + 1)

    # Normalize
    for step in range(WALK_LEN):
        dim_variances_by_step[step] /= step_counts[step]

    dim_names = ["aperture", "pressure", "depth", "binding", "continuity"]

    R.print(f"\n  Final current statistics (after {WALK_LEN} steps):")
    R.print(f"  {'Dimension':>12s}  {'Mean':>10s}  {'Std':>10s}  {'Var':>10s}")
    for d in range(5):
        R.print(f"  {dim_names[d]:>12s}  {np.mean(final_currents[:, d]):10.4f}  "
                 f"{np.std(final_currents[:, d]):10.4f}  {np.var(final_currents[:, d]):10.4f}")

    R.print(f"\n  HARMONY fraction in walks:")
    R.print(f"    Mean: {np.mean(harmony_fracs):.6f}")
    R.print(f"    Std:  {np.std(harmony_fracs):.6f}")
    R.print(f"    Expected from stationary: ~{T_STAR:.6f}")

    # Check if continuity dimension grows (HARMONY bias)
    R.print(f"\n  Continuity dimension growth (HARMONY=+1, VOID=-1):")
    early_var = dim_variances_by_step[4, 4]
    late_var = dim_variances_by_step[-1, 4]
    R.print(f"    Variance at step 5:  {early_var:.4f}")
    R.print(f"    Variance at step {WALK_LEN}: {late_var:.4f}")
    R.print(f"    Ratio: {late_var/early_var:.4f}" if early_var > 0 else "    (early variance zero)")

    # ---- Check for dimension-pair coupling ----
    R.subsection("Dimension-Pair Correlation in Final Currents")
    corr = np.corrcoef(final_currents.T)
    R.print(f"  Correlation matrix of final 5D currents:")
    R.print(f"  {'':>12s}  " + "  ".join(f"{d:>10s}" for d in dim_names))
    for i in range(5):
        row = "  ".join(f"{corr[i, j]:10.6f}" for j in range(5))
        R.print(f"  {dim_names[i]:>12s}  {row}")


# ──────────────────────────────────────────────────────────────────
# ANALYSIS 6: T* and 73% Relationships
# ──────────────────────────────────────────────────────────────────

def analysis_6_tstar():
    R.section("ANALYSIS 6: T* and 73% Relationships")

    # ---- T* vs 73/100 ----
    R.subsection("Numerical Relationships")
    R.print(f"  T*     = 5/7    = {T_STAR:.15f}")
    R.print(f"  73/100          = {0.73:.15f}")
    R.print(f"  Difference:       {T_STAR - 0.73:.15f}")
    R.print(f"  Ratio 73/100 / T*: {0.73 / T_STAR:.15f}")
    R.print()

    # Is there a simple fraction connecting them?
    R.print(f"  73/100 = 73/100 (already in lowest terms, gcd(73,100) = {gcd(73,100)})")
    R.print(f"  5/7    = 5/7    (already in lowest terms)")
    R.print(f"  73*7   = {73*7}")
    R.print(f"  100*5  = {100*5}")
    R.print(f"  Difference 73*7 - 100*5 = {73*7 - 100*5}")
    R.print(f"  So: 73/100 - 5/7 = (73*7 - 100*5) / 700 = {73*7-100*5}/700 = {(73*7-100*5)/700:.15f}")

    # ---- 27% analysis ----
    R.subsection("The 27% (Non-HARMONY)")
    R.print(f"  Non-HARMONY entries: 27")
    R.print(f"  27/100 = 0.27")
    R.print(f"  1 - T* = 2/7 = {1-T_STAR:.15f} = {2.0/7:.15f}")
    R.print(f"  27/100 vs 2/7: difference = {0.27 - 2.0/7:.15f}")
    R.print(f"  27 = 3^3 (a perfect cube)")
    R.print(f"  73 = prime")
    R.print(f"  73 + 27 = 100 = 10^2 = (5*2)^2")
    R.print(f"  73 - 27 = {73-27}")
    R.print(f"  73 * 27 = {73*27}")
    R.print(f"  73 / 27 = {73/27:.15f}")
    R.print(f"  27 / 73 = {27/73:.15f}")

    # Check 27/73 against constants
    R.print(f"\n  27/73 = {27/73:.10f}")
    R.print(f"  1/e   = {1/EULER_E:.10f}  (diff: {abs(27/73 - 1/EULER_E):.10f})")
    R.print(f"  1/phi = {2/(1+sqrt(5)):.10f}  (diff: {abs(27/73 - 2/(1+sqrt(5))):.10f})")

    # ---- Rational approximations of 73/100 ----
    R.subsection("Rational Approximations of 73/100 with Small Denominators")
    target = 0.73
    R.print(f"  {'p/q':>8s}  {'Value':>12s}  {'Error':>12s}")
    best_approx = []
    for q in range(1, 51):
        p = round(target * q)
        val = p / q
        err = abs(val - target)
        if err < 0.02:  # within 2%
            best_approx.append((p, q, val, err))
            R.print(f"  {p}/{q:>3d}    {val:12.10f}  {err:12.10f}")

    # ---- Continued fraction of 73/100 ----
    R.subsection("Continued Fraction Expansion of 73/100")
    # 73/100: compute continued fraction coefficients
    num, den = 73, 100
    cf = []
    while den != 0:
        a = num // den
        cf.append(a)
        num, den = den, num - a * den
    R.print(f"  73/100 = [{'; '.join(str(x) for x in cf)}]")

    # Same for T*
    num, den = 5, 7
    cf_t = []
    while den != 0:
        a = num // den
        cf_t.append(a)
        num, den = den, num - a * den
    R.print(f"  5/7    = [{'; '.join(str(x) for x in cf_t)}]")

    # ---- Properties of 73 ----
    R.subsection("Number-Theoretic Properties of 73")

    def is_prime(n):
        if n < 2:
            return False
        for i in range(2, int(sqrt(n)) + 1):
            if n % i == 0:
                return False
        return True

    R.print(f"  73 is prime: {is_prime(73)}")
    R.print(f"  73 is the 21st prime")
    R.print(f"  73 in binary: {bin(73)} = 1001001 (palindrome!)")
    R.print(f"  73 in octal: {oct(73)}")
    R.print(f"  73 in hex: {hex(73)}")
    R.print(f"  7 * 3 = 21, and 73 is the 21st prime")
    R.print(f"  Mirror: 37 is the 12th prime (mirror of 21)")
    R.print(f"  73 is a star number: 73 = 6*3*4/2 + 1? Actually: star numbers = 6k(k-1)+1")
    for k in range(1, 10):
        star = 6 * k * (k - 1) + 1
        if star == 73:
            R.print(f"    Yes! 73 is the {k}th star number (6*{k}*{k-1}+1 = {star})")
            break
    else:
        R.print(f"    73 is not a star number")

    R.print(f"  73 = 64 + 8 + 1 = 2^6 + 2^3 + 2^0")
    R.print(f"  Sum of digits: 7 + 3 = 10")
    R.print(f"  Product of digits: 7 * 3 = 21")

    # Sheldon Cooper's favorite number properties
    R.print(f"\n  Sheldon Cooper properties:")
    R.print(f"    73 reversed = 37")
    R.print(f"    37 is the 12th prime")
    R.print(f"    12 reversed = 21")
    R.print(f"    73 is the 21st prime")
    R.print(f"    73 in binary: 1001001 (palindrome)")
    R.print(f"    This makes 73 the 'unique' Sheldon prime")

    # ---- Information entropy of TSML ----
    R.subsection("Information Entropy of TSML Table")

    flat = TSML.astype(int).flatten()
    counts = Counter(flat)
    total = len(flat)
    probs = {k: v / total for k, v in counts.items()}

    entropy = -sum(p * log2(p) for p in probs.values() if p > 0)
    max_entropy = log2(10)  # if all 10 values equally likely

    R.print(f"  Value probabilities:")
    for val in sorted(probs.keys()):
        R.print(f"    {int(val)} ({OP_NAMES[int(val)]:>8s}): {probs[val]:.4f}  "
                 f"(-p*log2(p) = {-probs[val]*log2(probs[val]) if probs[val]>0 else 0:.6f})")

    R.print(f"\n  Shannon entropy H(TSML):  {entropy:.10f} bits")
    R.print(f"  Maximum entropy (uniform): {max_entropy:.10f} bits")
    R.print(f"  Efficiency H/H_max:        {entropy/max_entropy:.10f}")
    R.print(f"  Redundancy 1 - H/H_max:    {1-entropy/max_entropy:.10f}")

    # Compare with T*
    R.print(f"\n  Entropy relationships:")
    R.print(f"    H(TSML) = {entropy:.10f}")
    R.print(f"    T*      = {T_STAR:.10f}")
    R.print(f"    H / T*  = {entropy/T_STAR:.10f}")
    R.print(f"    T* / H  = {T_STAR/entropy:.10f}")

    # Binary entropy of 73%
    p = 0.73
    h_bin = -p * log2(p) - (1 - p) * log2(1 - p)
    R.print(f"\n  Binary entropy H_b(0.73):  {h_bin:.10f} bits")
    R.print(f"  Binary entropy H_b(T*):    {-T_STAR*log2(T_STAR)-(1-T_STAR)*log2(1-T_STAR):.10f} bits")

    # ---- BHML entropy for comparison ----
    R.subsection("Information Entropy of BHML Table")
    flat_b = BHML.astype(int).flatten()
    counts_b = Counter(flat_b)
    probs_b = {k: v / len(flat_b) for k, v in counts_b.items()}
    entropy_b = -sum(p * log2(p) for p in probs_b.values() if p > 0)
    R.print(f"  Shannon entropy H(BHML):  {entropy_b:.10f} bits")
    R.print(f"  Efficiency H/H_max:       {entropy_b/max_entropy:.10f}")
    R.print(f"  TSML vs BHML entropy ratio: {entropy/entropy_b:.10f}")

    # ---- Table as a number ----
    R.subsection("CL Table as Number")
    # Interpret the 100 digits as a base-10 number's digit sequence
    flat_digits = TSML.astype(int).flatten()
    digit_sum = sum(flat_digits)
    R.print(f"  Sum of all 100 entries: {digit_sum}")
    R.print(f"  Mean entry value:       {digit_sum/100:.2f}")
    R.print(f"  If all were HARMONY:    {7*100}")
    R.print(f"  'Missing' HARMONY sum:  {7*100 - digit_sum}")

    # What is the sum of the bump (non-HARMONY) entries?
    bump_sum = sum(v for v in flat_digits if v != 7)
    bump_count = sum(1 for v in flat_digits if v != 7)
    R.print(f"\n  Non-HARMONY entries:")
    R.print(f"    Count: {bump_count}")
    R.print(f"    Sum:   {bump_sum}")
    R.print(f"    Mean:  {bump_sum/bump_count:.4f}" if bump_count > 0 else "    (none)")

    # ---- T* power tower ----
    R.subsection("Powers of T* = 5/7")
    for n in range(1, 15):
        val = T_STAR ** n
        R.print(f"  T*^{n:2d} = {val:.15f}")

    R.subsection("Powers of (1 - T*) = 2/7")
    for n in range(1, 15):
        val = (1 - T_STAR) ** n
        R.print(f"  (2/7)^{n:2d} = {val:.15f}")


# ──────────────────────────────────────────────────────────────────
# MAIN
# ──────────────────────────────────────────────────────────────────

def main():
    R.print("=" * 72)
    R.print("  REALITY ANCHORS -- Rigorous CL Table Analysis")
    R.print("  CK Gen 9.21 -- The Coherence Keeper")
    R.print("  Brayden Sanders / 7Site LLC")
    R.print("=" * 72)
    R.print(f"\n  Date: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    R.print(f"  T* = 5/7 = {T_STAR:.15f}")
    R.print(f"  TSML HARMONY count: {int(np.sum(TSML == 7))}/100")
    R.print(f"  BHML HARMONY count: {int(np.sum(BHML == 7))}/100")

    # Run all analyses
    eigenvalues, stat_vec, T_norm, sorted_mags = analysis_1_markov()
    analysis_2_constants(eigenvalues, stat_vec, sorted_mags)
    strict_counts, relaxed_counts = analysis_3_monte_carlo()
    bump_pairs = analysis_4_semigroup()
    analysis_5_conservation()
    analysis_6_tstar()

    # ── Final summary ──
    R.section("FINAL SUMMARY")

    harmony_count = int(np.sum(TSML == 7))
    R.print(f"  1. TSML has {harmony_count} HARMONY entries (73%), T* = {T_STAR:.10f} (71.43%)")
    R.print(f"     73/100 overshoots T* by {(0.73 - T_STAR)*100:.4f} percentage points")
    R.print(f"     73/100 - 5/7 = 11/700 = {11/700:.10f}")

    z_strict = (73 - np.mean(strict_counts)) / np.std(strict_counts)
    R.print(f"\n  2. Monte Carlo: 73 HARMONY entries is {z_strict:.1f} sigma above random expectation")
    R.print(f"     Under strict constraints, mean={np.mean(strict_counts):.1f}, std={np.std(strict_counts):.1f}")

    # Count associativity
    CL = TSML.astype(int)
    assoc = sum(1 for a in range(10) for b in range(10) for c in range(10)
                if CL[CL[a][b]][c] == CL[a][CL[b][c]])
    R.print(f"\n  3. Semigroup: {assoc}/1000 triples associative ({assoc/10:.1f}%)")
    R.print(f"     HARMONY is absorbing (left-zero and right-zero)")

    R.print(f"\n  4. 73 is prime, the 21st prime, binary palindrome 1001001")
    R.print(f"     73 reversed = 37 (12th prime), 12 reversed = 21")

    R.print(f"\n  5. The CL table is a composition algebra, not a transition matrix.")
    R.print(f"     The HARMONY attractor ensures all sufficiently long compositions")
    R.print(f"     converge to HARMONY -- this is coherence by construction.")

    # ── Save markdown ──
    script_dir = os.path.dirname(os.path.abspath(__file__))
    md_path = os.path.join(script_dir, "reality_anchors_results.md")

    full_text = R.get_text()

    # Build markdown
    md_lines = []
    md_lines.append("# Reality Anchors -- CL Table Analysis Results\n")
    md_lines.append(f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
    md_lines.append("```\n")
    md_lines.append(full_text)
    md_lines.append("```\n")

    with open(md_path, "w", encoding="utf-8") as f:
        f.write("".join(md_lines))

    R.print(f"\n  Results saved to: {md_path}")
    R.print("  Done.")


if __name__ == "__main__":
    main()
