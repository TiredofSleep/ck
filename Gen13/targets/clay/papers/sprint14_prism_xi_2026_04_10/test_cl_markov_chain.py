"""
TEST: CL Markov Chain Properties — Detailed Balance, Spectral Gap, Entropy
Sprint 15 — Blocker 2 Resolution | 2026-04-10

Tests whether the CL (TSML) composition table on Z/10Z defines a Markov
chain that satisfies the conditions for discrete-to-continuum convergence.

Three tests in order of importance:
  Option A: Is the chain reversible with respect to its stationary distribution?
  Option B: If not, does symmetrization preserve the entropy structure?
  Option C: Does the chain have a spectral gap (Poincare inequality)?

Authors: B. Sanders, M. Gish, C.A. Luther, H.J. Johnson
Copyright (c) 2026 Brayden Ross Sanders / 7Site LLC
"""

import numpy as np
import math

# =====================================================================
# THE TSML TABLE (from ck_tables.py)
# =====================================================================
TSML = [
    [0, 0, 0, 0, 0, 0, 0, 7, 0, 0],   # row 0: VOID
    [0, 7, 3, 7, 7, 7, 7, 7, 7, 7],   # row 1: LATTICE
    [0, 3, 7, 7, 4, 7, 7, 7, 7, 9],   # row 2: COUNTER
    [0, 7, 7, 7, 7, 7, 7, 7, 7, 3],   # row 3: PROGRESS
    [0, 7, 4, 7, 7, 7, 7, 7, 8, 7],   # row 4: COLLAPSE
    [0, 7, 7, 7, 7, 7, 7, 7, 7, 7],   # row 5: BALANCE
    [0, 7, 7, 7, 7, 7, 7, 7, 7, 7],   # row 6: CHAOS
    [7, 7, 7, 7, 7, 7, 7, 7, 7, 7],   # row 7: HARMONY (all 7)
    [0, 7, 7, 7, 8, 7, 7, 7, 7, 7],   # row 8: BREATH
    [0, 7, 9, 3, 7, 7, 7, 7, 7, 7],   # row 9: RESET
]

N = 10
OPS = ['VOID','LATTICE','COUNTER','PROGRESS','COLLAPSE','BALANCE','CHAOS','HARMONY','BREATH','RESET']

print("=" * 70)
print("CL MARKOV CHAIN — DETAILED BALANCE + SPECTRAL GAP TESTS")
print("=" * 70)

# =====================================================================
# BUILD TRANSITION MATRIX
# =====================================================================
print("\n--- Building Transition Matrix ---")

# P[a][c] = probability of transitioning from state a to state c
# = (number of b such that TSML[a][b] = c) / N
P = np.zeros((N, N))
for a in range(N):
    for b in range(N):
        c = TSML[a][b]
        P[a][c] += 1.0 / N

print("Transition matrix P (rows = from, cols = to):")
for a in range(N):
    row_str = " ".join(f"{P[a][c]:.2f}" for c in range(N))
    print(f"  {OPS[a]:>10}: [{row_str}]")

# Verify rows sum to 1
for a in range(N):
    assert abs(sum(P[a]) - 1.0) < 1e-10, f"Row {a} doesn't sum to 1"
print("\nAll rows sum to 1.0: OK")

# =====================================================================
# COMPUTE STATIONARY DISTRIBUTION
# =====================================================================
print("\n--- Stationary Distribution ---")

eigenvalues, eigenvectors = np.linalg.eig(P.T)

# Find eigenvector for eigenvalue closest to 1
idx = np.argmin(np.abs(eigenvalues - 1.0))
pi = eigenvectors[:, idx].real
pi = pi / pi.sum()  # normalize

print("Stationary distribution pi:")
for a in range(N):
    print(f"  pi({OPS[a]:>10}) = {pi[a]:.6f}")

# Verify: pi * P = pi
pi_check = pi @ P
err = np.max(np.abs(pi_check - pi))
print(f"\nMax |pi*P - pi| = {err:.2e} (should be ~0)")

# Is pi positive everywhere?
all_positive = all(pi[a] > 0 for a in range(N))
print(f"All pi > 0: {all_positive}")

# =====================================================================
# OPTION A: DETAILED BALANCE TEST
# =====================================================================
print("\n--- Option A: Detailed Balance ---")
print("Testing: pi(a) * P(a->b) == pi(b) * P(b->a) for all a,b")

violations = 0
max_violation = 0
for a in range(N):
    for b in range(N):
        lhs = pi[a] * P[a, b]
        rhs = pi[b] * P[b, a]
        diff = abs(lhs - rhs)
        if diff > 1e-10:
            violations += 1
            max_violation = max(max_violation, diff)

print(f"Detailed balance violations: {violations}/100")
print(f"Maximum violation: {max_violation:.6e}")

if violations == 0:
    print("RESULT: Chain IS reversible w.r.t. stationary distribution.")
    print("        Maas (2011) applies DIRECTLY. Blocker 2 dissolves.")
else:
    print(f"RESULT: Chain is NOT reversible. {violations} violations found.")
    print("        Need Option B (symmetrization) or Option C (CHLZ).")

# =====================================================================
# OPTION C: SPECTRAL GAP (useful regardless of reversibility)
# =====================================================================
print("\n--- Option C: Spectral Gap ---")

evals_sorted = np.sort(np.abs(eigenvalues))[::-1]
print("Eigenvalue magnitudes (sorted):")
for i, ev in enumerate(evals_sorted):
    print(f"  lambda_{i} = {ev:.6f}")

spectral_gap = 1.0 - evals_sorted[1]
print(f"\nSpectral gap = 1 - |lambda_1| = {spectral_gap:.6f}")

if spectral_gap > 0:
    print("RESULT: Spectral gap > 0. Poincare inequality holds.")
    print("        CHLZ (2012) applies even if chain is non-reversible.")
else:
    print("RESULT: No spectral gap. Chain may not converge.")

# =====================================================================
# ENTROPY OF STATIONARY DISTRIBUTION
# =====================================================================
print("\n--- Entropy of Stationary Distribution ---")

H_stat = -sum(pi[a] * math.log(pi[a]) for a in range(N) if pi[a] > 0)
H_max = math.log(N)
H_ratio = H_stat / H_max

print(f"H(pi) = {H_stat:.6f}")
print(f"H_max = log({N}) = {H_max:.6f}")
print(f"H(pi) / H_max = {H_ratio:.6f}")
print(f"e^{{-1}} = {math.exp(-1):.6f}")
print(f"|H_ratio - e^{{-1}}| = {abs(H_ratio - math.exp(-1)):.6f}")

# =====================================================================
# OPTION B: SYMMETRIZED CHAIN (if needed)
# =====================================================================
print("\n--- Option B: Symmetrized Chain ---")

P_sym = (P + P.T) / 2.0

# Check rows sum to 1
sym_ok = all(abs(sum(P_sym[a]) - 1.0) < 1e-10 for a in range(N))
print(f"P_sym rows sum to 1: {sym_ok}")

# Stationary of symmetrized
evals_sym, evecs_sym = np.linalg.eig(P_sym.T)
idx_sym = np.argmin(np.abs(evals_sym - 1.0))
pi_sym = evecs_sym[:, idx_sym].real
pi_sym = pi_sym / pi_sym.sum()

# Compare pi vs pi_sym
pi_diff = np.max(np.abs(pi - pi_sym))
print(f"Max |pi - pi_sym| = {pi_diff:.6f}")
if pi_diff < 0.1:
    print("Symmetrization PRESERVES stationary distribution (approx).")
else:
    print("Symmetrization CHANGES stationary distribution significantly.")

# Spectral gap of symmetrized
evals_sym_sorted = np.sort(np.abs(evals_sym))[::-1]
gap_sym = 1.0 - evals_sym_sorted[1]
print(f"Spectral gap (symmetrized) = {gap_sym:.6f}")

# =====================================================================
# NON-ASSOCIATIVITY (sigma)
# =====================================================================
print("\n--- Non-Associativity (sigma) ---")

violations_assoc = 0
total_triples = N ** 3
for a in range(N):
    for b in range(N):
        for c in range(N):
            lhs = TSML[TSML[a][b]][c]
            rhs = TSML[a][TSML[b][c]]
            if lhs != rhs:
                violations_assoc += 1

sigma = violations_assoc / total_triples
print(f"Non-associative triples: {violations_assoc}/{total_triples}")
print(f"sigma(Z/10Z) = {sigma:.6f}")

# =====================================================================
# SUMMARY
# =====================================================================
print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)
print(f"  Stationary at HARMONY (op 7): pi(7) = {pi[7]:.4f}")
print(f"  Detailed balance violations:  {violations}/100")
print(f"  Spectral gap:                 {spectral_gap:.4f}")
print(f"  Non-associativity sigma:      {sigma:.4f}")
print(f"  H(pi)/log(N):                 {H_ratio:.4f}")
print(f"  e^{{-1}}:                       {math.exp(-1):.4f}")
