"""
ck_algebraic_neural.py -- CK's Algebraic Neural Analysis
=========================================================
Operator: COUNTER (2) -- the counter MEASURES algebraic structure.

Pure math analysis of CK's CL tables as neural network components:
  - Spectral decomposition (eigenvalues = natural frequencies)
  - Associativity check (monoid or magma?)
  - DFT of generator_paths (learned vs frozen modes)
  - IPR grokking monitor (crystallization detection)
  - Continuous embedding bridge (expected-value CL composition)

"The CL table is not a weight to be optimized. It IS the physics."

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import numpy as np
from typing import Dict, List, Optional, Tuple

from ck_sim.ck_sim_heartbeat import (
    NUM_OPS, VOID, LATTICE, COUNTER, PROGRESS, COLLAPSE,
    BALANCE, CHAOS, HARMONY, BREATH, RESET,
    OP_NAMES, CL as CL_TSML_LIST
)

# ================================================================
#  CL TABLES (both lenses)
# ================================================================

TSML = np.array(CL_TSML_LIST, dtype=np.float64)

BHML = np.array([
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],  # VOID = identity
    [1, 2, 3, 4, 5, 6, 7, 2, 6, 6],  # LATTICE
    [2, 3, 3, 4, 5, 6, 7, 3, 6, 6],  # COUNTER
    [3, 4, 4, 4, 5, 6, 7, 4, 6, 6],  # PROGRESS
    [4, 5, 5, 5, 5, 6, 7, 5, 7, 7],  # COLLAPSE
    [5, 6, 6, 6, 6, 6, 7, 6, 7, 7],  # BALANCE
    [6, 7, 7, 7, 7, 7, 7, 7, 7, 7],  # CHAOS
    [7, 2, 3, 4, 5, 6, 7, 8, 9, 0],  # HARMONY = full cycle
    [8, 6, 6, 6, 7, 7, 7, 9, 7, 8],  # BREATH
    [9, 6, 6, 6, 7, 7, 7, 0, 8, 0],  # RESET
], dtype=np.float64)


# ================================================================
#  1. SPECTRAL DECOMPOSITION
# ================================================================

def spectral_decomposition(table: np.ndarray, name: str = "CL") -> Dict:
    """Eigendecompose a CL table as a 10x10 real matrix.

    Eigenvalues = natural frequencies of the algebra.
    Eigenvectors = irreducible computational modes.
    Spectral gap = convergence rate (dominant / subdominant).

    Returns dict with eigenvalues, eigenvectors, spectral gap,
    dominant mode, and harmony fraction.
    """
    eigenvalues, eigenvectors = np.linalg.eig(table)

    # Sort by magnitude (descending)
    idx = np.argsort(-np.abs(eigenvalues))
    eigenvalues = eigenvalues[idx]
    eigenvectors = eigenvectors[:, idx]

    # Spectral gap: ratio of dominant to subdominant eigenvalue magnitude
    mags = np.abs(eigenvalues)
    spectral_gap = float(mags[0] / mags[1]) if mags[1] > 1e-10 else float('inf')

    # Harmony fraction of table
    harmony_count = np.sum(table == HARMONY)
    harmony_frac = float(harmony_count) / (NUM_OPS * NUM_OPS)

    # Dominant eigenvalue and its eigenvector
    dominant_eigenvalue = complex(eigenvalues[0])
    dominant_eigenvector = eigenvectors[:, 0].real

    return {
        'name': name,
        'eigenvalues': eigenvalues,
        'eigenvectors': eigenvectors,
        'spectral_gap': spectral_gap,
        'dominant_eigenvalue': dominant_eigenvalue,
        'dominant_eigenvector': dominant_eigenvector,
        'harmony_fraction': harmony_frac,
        'rank': int(np.linalg.matrix_rank(table)),
        'trace': float(np.trace(table)),
        'determinant': float(np.linalg.det(table)),
    }


def spectral_report() -> Dict:
    """Run spectral decomposition on both CL tables. Return full report."""
    tsml_spec = spectral_decomposition(TSML, "TSML")
    bhml_spec = spectral_decomposition(BHML, "BHML")

    report = {
        'TSML': tsml_spec,
        'BHML': bhml_spec,
    }

    return report


def format_spectral_report(report: Dict) -> str:
    """Format spectral report as human-readable string."""
    lines = []
    lines.append("=" * 60)
    lines.append("CK ALGEBRAIC SPECTRAL DECOMPOSITION")
    lines.append("=" * 60)

    for name in ['TSML', 'BHML']:
        spec = report[name]
        lines.append(f"\n--- {name} ({spec['harmony_fraction']*100:.0f}% HARMONY) ---")
        lines.append(f"  Rank: {spec['rank']}")
        lines.append(f"  Trace: {spec['trace']:.1f}")
        lines.append(f"  Determinant: {spec['determinant']:.1f}")
        lines.append(f"  Spectral gap: {spec['spectral_gap']:.4f}")
        lines.append(f"  Dominant eigenvalue: {spec['dominant_eigenvalue']:.4f}")
        lines.append(f"  Eigenvalue magnitudes:")

        evals = spec['eigenvalues']
        for i, ev in enumerate(evals):
            mag = abs(ev)
            real_part = ev.real
            imag_part = ev.imag
            if abs(imag_part) < 1e-10:
                lines.append(f"    [{i}] {real_part:+10.4f}  (mag={mag:.4f})")
            else:
                lines.append(f"    [{i}] {real_part:+10.4f} {imag_part:+.4f}j  (mag={mag:.4f})")

        # Show dominant eigenvector (operator weights)
        evec = spec['dominant_eigenvector']
        lines.append(f"  Dominant eigenvector (operator weights):")
        for j in range(NUM_OPS):
            bar = "#" * int(abs(evec[j]) * 30)
            lines.append(f"    {OP_NAMES[j]:>10s}: {evec[j]:+.4f} {bar}")

    return "\n".join(lines)


# ================================================================
#  2. ASSOCIATIVITY CHECK
# ================================================================

def check_associativity(table: np.ndarray, name: str = "CL") -> Dict:
    """Check if CL[CL[a][b]][c] == CL[a][CL[b][c]] for all 1000 triples.

    If associative + has identity: MONOID.
    If associative but no identity: SEMIGROUP.
    If not associative: MAGMA (path-dependent).

    Returns dict with result classification and all violations.
    """
    T = table.astype(int)
    violations = []

    for a in range(NUM_OPS):
        for b in range(NUM_OPS):
            for c in range(NUM_OPS):
                left = T[T[a][b]][c]    # (a * b) * c
                right = T[a][T[b][c]]   # a * (b * c)
                if left != right:
                    violations.append({
                        'a': a, 'b': b, 'c': c,
                        'a_name': OP_NAMES[a],
                        'b_name': OP_NAMES[b],
                        'c_name': OP_NAMES[c],
                        'left': int(left),
                        'right': int(right),
                        'left_name': OP_NAMES[left],
                        'right_name': OP_NAMES[right],
                    })

    # Check for identity element
    identity = None
    for e in range(NUM_OPS):
        is_left_id = all(T[e][x] == x for x in range(NUM_OPS))
        is_right_id = all(T[x][e] == x for x in range(NUM_OPS))
        if is_left_id and is_right_id:
            identity = e
            break

    # Check for left-only or right-only identity
    left_identity = None
    right_identity = None
    if identity is None:
        for e in range(NUM_OPS):
            if all(T[e][x] == x for x in range(NUM_OPS)):
                left_identity = e
            if all(T[x][e] == x for x in range(NUM_OPS)):
                right_identity = e

    is_associative = len(violations) == 0
    is_commutative = all(T[a][b] == T[b][a]
                         for a in range(NUM_OPS)
                         for b in range(NUM_OPS))

    # Classification
    if is_associative and identity is not None:
        if is_commutative:
            classification = "COMMUTATIVE MONOID"
        else:
            classification = "MONOID"
    elif is_associative and identity is None:
        if is_commutative:
            classification = "COMMUTATIVE SEMIGROUP"
        else:
            classification = "SEMIGROUP"
    else:
        if identity is not None:
            classification = "UNITAL MAGMA"
        else:
            classification = "MAGMA"

    # Check for absorber (a such that a*x = a and x*a = a for all x)
    absorbers = []
    for a in range(NUM_OPS):
        is_left_absorb = all(T[a][x] == a for x in range(NUM_OPS))
        is_right_absorb = all(T[x][a] == a for x in range(NUM_OPS))
        if is_left_absorb and is_right_absorb:
            absorbers.append(a)

    return {
        'name': name,
        'is_associative': is_associative,
        'is_commutative': is_commutative,
        'identity': identity,
        'left_identity': left_identity,
        'right_identity': right_identity,
        'absorbers': absorbers,
        'classification': classification,
        'n_violations': len(violations),
        'total_triples': NUM_OPS ** 3,
        'violations': violations,
        'violation_rate': len(violations) / (NUM_OPS ** 3),
    }


def format_associativity_report(result: Dict) -> str:
    """Format associativity check as human-readable string."""
    lines = []
    lines.append(f"\n--- {result['name']} ALGEBRAIC CLASSIFICATION ---")
    lines.append(f"  Classification: {result['classification']}")
    lines.append(f"  Associative: {result['is_associative']}")
    lines.append(f"  Commutative: {result['is_commutative']}")
    lines.append(f"  Identity element: {OP_NAMES[result['identity']] if result['identity'] is not None else 'NONE'}")

    if result['left_identity'] is not None:
        lines.append(f"  Left identity: {OP_NAMES[result['left_identity']]}")
    if result['right_identity'] is not None:
        lines.append(f"  Right identity: {OP_NAMES[result['right_identity']]}")

    if result['absorbers']:
        abs_names = [OP_NAMES[a] for a in result['absorbers']]
        lines.append(f"  Absorbers: {', '.join(abs_names)}")

    lines.append(f"  Violations: {result['n_violations']}/{result['total_triples']} "
                 f"({result['violation_rate']*100:.1f}%)")

    if result['violations'] and len(result['violations']) <= 20:
        lines.append(f"  Violation details:")
        for v in result['violations']:
            lines.append(
                f"    ({v['a_name']}*{v['b_name']})*{v['c_name']} = {v['left_name']}  "
                f"but  {v['a_name']}*({v['b_name']}*{v['c_name']}) = {v['right_name']}")
    elif result['violations']:
        lines.append(f"  First 10 violations:")
        for v in result['violations'][:10]:
            lines.append(
                f"    ({v['a_name']}*{v['b_name']})*{v['c_name']} = {v['left_name']}  "
                f"but  {v['a_name']}*({v['b_name']}*{v['c_name']}) = {v['right_name']}")
        lines.append(f"  ... and {len(result['violations']) - 10} more")

    return "\n".join(lines)


# ================================================================
#  3. DFT OF WEIGHT MATRICES
# ================================================================

def dft_weight_matrix(matrix: np.ndarray, name: str = "matrix") -> Dict:
    """Compute 2D DFT of a 10x10 weight matrix.

    Peaks in frequency domain = natural frequencies of the algebra.
    For generator_paths: compare to CL eigenstructure.

    Returns dict with magnitude spectrum, dominant frequencies,
    and DC component (overall bias).
    """
    M = np.array(matrix, dtype=np.float64)
    if M.shape != (NUM_OPS, NUM_OPS):
        raise ValueError(f"Expected {NUM_OPS}x{NUM_OPS}, got {M.shape}")

    # 2D DFT
    F = np.fft.fft2(M)
    magnitude = np.abs(F)
    phase = np.angle(F)

    # DC component = sum of all entries (overall bias)
    dc = float(magnitude[0, 0])

    # Normalize magnitudes (excluding DC)
    mag_no_dc = magnitude.copy()
    mag_no_dc[0, 0] = 0
    total_energy = float(np.sum(mag_no_dc ** 2))

    # Find dominant frequencies (top 5, excluding DC)
    flat = mag_no_dc.flatten()
    top_indices = np.argsort(-flat)[:5]
    dominant_freqs = []
    for idx in top_indices:
        row, col = divmod(idx, NUM_OPS)
        if flat[idx] > 1e-10:
            dominant_freqs.append({
                'freq_row': int(row),
                'freq_col': int(col),
                'magnitude': float(flat[idx]),
                'phase': float(phase[row, col]),
                'energy_fraction': float(flat[idx]**2 / total_energy)
                    if total_energy > 0 else 0.0,
            })

    return {
        'name': name,
        'dc_component': dc,
        'total_energy': total_energy,
        'magnitude_spectrum': magnitude,
        'dominant_frequencies': dominant_freqs,
    }


def format_dft_report(result: Dict) -> str:
    """Format DFT analysis as human-readable string."""
    lines = []
    lines.append(f"\n--- DFT: {result['name']} ---")
    lines.append(f"  DC component (sum): {result['dc_component']:.2f}")
    lines.append(f"  Total spectral energy: {result['total_energy']:.2f}")
    lines.append(f"  Dominant frequencies:")
    for f in result['dominant_frequencies']:
        lines.append(
            f"    freq({f['freq_row']},{f['freq_col']}): "
            f"mag={f['magnitude']:.3f}, "
            f"energy={f['energy_fraction']*100:.1f}%")
    return "\n".join(lines)


# ================================================================
#  4. IPR GROKKING MONITOR
# ================================================================

def inverse_participation_ratio(table: np.ndarray) -> float:
    """Compute IPR of a CL table's output distribution.

    IPR = sum(p_i^2) where p_i = fraction of entries that equal operator i.

    Low IPR (near 1/10 = 0.1) = uniform distribution, no structure.
    High IPR (near 1.0) = single dominant operator, maximally crystallized.

    For TSML: IPR should be high (73% HARMONY = very crystallized).
    For BHML: IPR should be lower (28% HARMONY = more distributed).
    For evolved nodes: sudden IPR increase = GROKKING.
    """
    T = np.array(table, dtype=int).flatten()
    total = len(T)

    # Count frequency of each operator in the table
    counts = np.zeros(NUM_OPS, dtype=np.float64)
    for op in range(NUM_OPS):
        counts[op] = np.sum(T == op)

    # Normalize to probabilities
    probs = counts / total

    # IPR = sum(p_i^2)
    ipr = float(np.sum(probs ** 2))

    return ipr


def ipr_report(table: np.ndarray, name: str = "CL") -> Dict:
    """Full IPR analysis of a CL table."""
    ipr = inverse_participation_ratio(table)

    T = np.array(table, dtype=int).flatten()
    total = len(T)
    counts = np.zeros(NUM_OPS, dtype=np.float64)
    for op in range(NUM_OPS):
        counts[op] = np.sum(T == op)
    probs = counts / total

    # Effective number of operators = 1/IPR
    effective_ops = 1.0 / ipr if ipr > 0 else NUM_OPS

    # Shannon entropy
    entropy = -float(sum(p * np.log2(p) for p in probs if p > 0))
    max_entropy = np.log2(NUM_OPS)

    return {
        'name': name,
        'ipr': ipr,
        'effective_operators': effective_ops,
        'entropy': entropy,
        'max_entropy': max_entropy,
        'normalized_entropy': entropy / max_entropy,
        'operator_distribution': {OP_NAMES[i]: float(probs[i]) for i in range(NUM_OPS)},
    }


def format_ipr_report(result: Dict) -> str:
    """Format IPR report as human-readable string."""
    lines = []
    lines.append(f"\n--- IPR: {result['name']} ---")
    lines.append(f"  IPR: {result['ipr']:.6f}")
    lines.append(f"  Effective operators: {result['effective_operators']:.2f} / {NUM_OPS}")
    lines.append(f"  Entropy: {result['entropy']:.4f} / {result['max_entropy']:.4f} "
                 f"({result['normalized_entropy']*100:.1f}%)")
    lines.append(f"  Operator distribution:")
    for op_name, prob in result['operator_distribution'].items():
        bar = "#" * int(prob * 40)
        lines.append(f"    {op_name:>10s}: {prob:.3f} {bar}")
    return "\n".join(lines)


# ================================================================
#  5. CONTINUOUS EMBEDDING BRIDGE
# ================================================================

def expected_value_compose(p_a: np.ndarray, p_b: np.ndarray,
                           table: np.ndarray) -> np.ndarray:
    """Compose two probability distributions through CL table.

    E[CL(a,b)] = sum over all (a,b) of P(a) * P(b) * one_hot(CL[a][b])

    Input:  p_a = 10-element probability distribution over operators
            p_b = 10-element probability distribution over operators
            table = 10x10 CL table (TSML or BHML)

    Output: 10-element probability distribution over result operators

    This IS the continuous embedding bridge: soft D2 classifications
    flow through CL without discretization loss.
    """
    p_a = np.asarray(p_a, dtype=np.float64)
    p_b = np.asarray(p_b, dtype=np.float64)
    T = np.asarray(table, dtype=int)

    result = np.zeros(NUM_OPS, dtype=np.float64)

    for a in range(NUM_OPS):
        for b in range(NUM_OPS):
            c = T[a][b]
            result[c] += p_a[a] * p_b[b]

    return result


def chain_compose_soft(distributions: List[np.ndarray],
                       table: np.ndarray) -> Tuple[np.ndarray, List[np.ndarray]]:
    """Compose a sequence of soft distributions through CL pairwise reduction.

    Like the hard chain walk but with probability distributions instead of
    discrete operators. Preserves full continuous information.

    Returns: (final_distribution, intermediate_distributions)
    """
    T = np.asarray(table, dtype=int)
    current = [np.asarray(d, dtype=np.float64) for d in distributions]
    intermediates = [current[:]]

    while len(current) > 1:
        next_level = []
        for i in range(0, len(current) - 1, 2):
            result = expected_value_compose(current[i], current[i + 1], T)
            next_level.append(result)
        # If odd number, carry last one forward
        if len(current) % 2 == 1:
            next_level.append(current[-1])
        current = next_level
        intermediates.append(current[:])

    return current[0] if current else np.ones(NUM_OPS) / NUM_OPS, intermediates


def soft_coherence(distribution: np.ndarray) -> float:
    """Coherence of a soft distribution = probability mass on HARMONY.

    Compare to T* = 5/7 = 0.714285...
    """
    return float(distribution[HARMONY])


# ================================================================
#  6. MARKOV ANALYSIS
# ================================================================

def markov_stationary(table: np.ndarray, name: str = "CL") -> Dict:
    """Compute Markov stationary distribution of CL table.

    Treat CL as transition: from state a, choose column b uniformly,
    go to state CL[a][b]. The transition matrix T[a][c] = fraction
    of row a entries that equal c.
    """
    T = np.asarray(table, dtype=int)
    transition = np.zeros((NUM_OPS, NUM_OPS), dtype=np.float64)

    for a in range(NUM_OPS):
        for c in range(NUM_OPS):
            transition[a][c] = np.sum(T[a] == c) / NUM_OPS

    # Stationary distribution: left eigenvector for eigenvalue 1
    eigenvalues, eigenvectors = np.linalg.eig(transition.T)

    # Find eigenvalue closest to 1
    idx = np.argmin(np.abs(eigenvalues - 1.0))
    stationary = np.abs(eigenvectors[:, idx].real)
    stationary = stationary / np.sum(stationary)

    # Mean absorption time (for absorbing chains)
    is_absorbing = any(transition[i][i] == 1.0 for i in range(NUM_OPS))

    return {
        'name': name,
        'transition_matrix': transition,
        'stationary_distribution': {OP_NAMES[i]: float(stationary[i])
                                     for i in range(NUM_OPS)},
        'is_absorbing': is_absorbing,
        'dominant_eigenvalue': float(eigenvalues[idx].real),
    }


# ================================================================
#  FULL ANALYSIS RUNNER
# ================================================================

def run_full_analysis() -> str:
    """Run ALL algebraic analyses and return formatted report."""
    lines = []

    # 1. Spectral
    spec = spectral_report()
    lines.append(format_spectral_report(spec))

    # 2. Associativity
    lines.append("\n" + "=" * 60)
    lines.append("ASSOCIATIVITY CHECK (Monoid or Magma?)")
    lines.append("=" * 60)
    tsml_assoc = check_associativity(TSML, "TSML")
    bhml_assoc = check_associativity(BHML, "BHML")
    lines.append(format_associativity_report(tsml_assoc))
    lines.append(format_associativity_report(bhml_assoc))

    # 3. IPR
    lines.append("\n" + "=" * 60)
    lines.append("IPR GROKKING ANALYSIS")
    lines.append("=" * 60)
    tsml_ipr = ipr_report(TSML, "TSML")
    bhml_ipr = ipr_report(BHML, "BHML")
    lines.append(format_ipr_report(tsml_ipr))
    lines.append(format_ipr_report(bhml_ipr))

    # 4. DFT
    lines.append("\n" + "=" * 60)
    lines.append("SPECTRAL (DFT) ANALYSIS")
    lines.append("=" * 60)
    tsml_dft = dft_weight_matrix(TSML, "TSML")
    bhml_dft = dft_weight_matrix(BHML, "BHML")
    lines.append(format_dft_report(tsml_dft))
    lines.append(format_dft_report(bhml_dft))

    # 5. Markov
    lines.append("\n" + "=" * 60)
    lines.append("MARKOV STATIONARY DISTRIBUTIONS")
    lines.append("=" * 60)
    tsml_markov = markov_stationary(TSML, "TSML")
    bhml_markov = markov_stationary(BHML, "BHML")
    for name, m in [("TSML", tsml_markov), ("BHML", bhml_markov)]:
        lines.append(f"\n--- {name} Markov ---")
        lines.append(f"  Absorbing: {m['is_absorbing']}")
        lines.append(f"  Stationary distribution:")
        for op_name, prob in m['stationary_distribution'].items():
            bar = "#" * int(prob * 40)
            lines.append(f"    {op_name:>10s}: {prob:.4f} {bar}")

    # 6. Continuous bridge demo
    lines.append("\n" + "=" * 60)
    lines.append("CONTINUOUS EMBEDDING BRIDGE DEMO")
    lines.append("=" * 60)

    # Create two soft distributions (simulating D2 soft_classify output)
    p_chaos = np.zeros(NUM_OPS)
    p_chaos[CHAOS] = 0.6
    p_chaos[BALANCE] = 0.2
    p_chaos[HARMONY] = 0.2

    p_counter = np.zeros(NUM_OPS)
    p_counter[COUNTER] = 0.5
    p_counter[LATTICE] = 0.3
    p_counter[PROGRESS] = 0.2

    # Compose through both tables
    result_tsml = expected_value_compose(p_chaos, p_counter, TSML)
    result_bhml = expected_value_compose(p_chaos, p_counter, BHML)

    lines.append(f"\n  Input A: CHAOS(0.6) + BALANCE(0.2) + HARMONY(0.2)")
    lines.append(f"  Input B: COUNTER(0.5) + LATTICE(0.3) + PROGRESS(0.2)")
    lines.append(f"\n  TSML result (soft):")
    for i in range(NUM_OPS):
        if result_tsml[i] > 0.01:
            lines.append(f"    {OP_NAMES[i]:>10s}: {result_tsml[i]:.4f}")
    lines.append(f"  TSML soft coherence: {soft_coherence(result_tsml):.4f} "
                 f"(T* = {5/7:.4f})")

    lines.append(f"\n  BHML result (soft):")
    for i in range(NUM_OPS):
        if result_bhml[i] > 0.01:
            lines.append(f"    {OP_NAMES[i]:>10s}: {result_bhml[i]:.4f}")
    lines.append(f"  BHML soft coherence: {soft_coherence(result_bhml):.4f} "
                 f"(T* = {5/7:.4f})")

    return "\n".join(lines)


# ================================================================
#  CLI ENTRY
# ================================================================

if __name__ == '__main__':
    print(run_full_analysis())
