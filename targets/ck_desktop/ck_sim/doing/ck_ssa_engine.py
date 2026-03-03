# Copyright (c) 2025-2026 Brayden Sanders / 7Site LLC
# Licensed under the 7Site Human Use License v1.0
# See LICENSE file in project root for full terms.
#
# FREE for humans for personal/recreational use.
# NO commercial or government use without written agreement.

"""
ck_ssa_engine.py -- Sanders Singularity Axiom Engine + SIGA Classifier
========================================================================
Operator: COLLAPSE (9) -- Self-referential closure generates singularities.

Implements the Sanders Singularity Axiom (SSA):
  A self-referentially closed, expressive system CANNOT simultaneously satisfy:
    (C1) Total Coherence: every internal description extends perfectly (delta=0)
    (C2) Internal Completeness: the system can decide which states are coherent
    (C3) Non-Singularity: self-closure has no singularities

At least one must break. This engine tests which condition breaks for each
problem in the coherence manifold.

Also implements the Sanders Information-Geometry Axiom (SIGA) classifier:
  Information = geometry only. Topology requires coherence/gluing.
  Every Clay problem is a topology restoration problem on a geometric base.

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import math
from typing import Dict, List, Optional

from ck_sim.being.ck_sdv_safety import clamp, safe_div, safe_sqrt


# ================================================================
#  SSA DATA STRUCTURES
# ================================================================

class C1Result:
    """Result of testing C1: Total Coherence."""
    __slots__ = ('holds', 'mean_delta', 'max_delta', 'min_delta',
                 'zero_count', 'total_count', 'description')

    def __init__(self, holds: bool, mean_delta: float, max_delta: float,
                 min_delta: float, zero_count: int, total_count: int):
        self.holds = holds
        self.mean_delta = mean_delta
        self.max_delta = max_delta
        self.min_delta = min_delta
        self.zero_count = zero_count
        self.total_count = total_count
        threshold = 0.01
        if holds:
            self.description = f'C1 HOLDS: all deltas < {threshold} ({zero_count}/{total_count} near-zero)'
        else:
            self.description = f'C1 BREAKS: mean delta = {mean_delta:.4f}, max = {max_delta:.4f}'


class C2Result:
    """Result of testing C2: Internal Completeness."""
    __slots__ = ('holds', 'consistency_rate', 'majority_class',
                 'class_counts', 'description')

    def __init__(self, holds: bool, consistency_rate: float,
                 majority_class: str, class_counts: dict):
        self.holds = holds
        self.consistency_rate = consistency_rate
        self.majority_class = majority_class
        self.class_counts = class_counts
        if holds:
            self.description = f'C2 HOLDS: {consistency_rate:.1%} consistent ({majority_class})'
        else:
            self.description = f'C2 BREAKS: only {consistency_rate:.1%} consistent, split across classes'


class C3Result:
    """Result of testing C3: Non-Singularity of Self-Closure."""
    __slots__ = ('holds', 'max_variance', 'divergence_count',
                 'singular_seeds', 'description')

    def __init__(self, holds: bool, max_variance: float,
                 divergence_count: int, singular_seeds: list):
        self.holds = holds
        self.max_variance = max_variance
        self.divergence_count = divergence_count
        self.singular_seeds = singular_seeds
        if holds:
            self.description = f'C3 HOLDS: max variance = {max_variance:.4f}, no divergences'
        else:
            self.description = f'C3 BREAKS: {divergence_count} divergences, variance = {max_variance:.4f}'


class TrilemmaResult:
    """Full SSA trilemma result for one problem."""
    __slots__ = ('problem_id', 'c1', 'c2', 'c3', 'breaking',
                 'interpretation')

    def __init__(self, problem_id: str, c1: C1Result, c2: C2Result,
                 c3: C3Result):
        self.problem_id = problem_id
        self.c1 = c1
        self.c2 = c2
        self.c3 = c3

        # Determine which condition(s) break
        breaks = []
        if not c1.holds:
            breaks.append('C1')
        if not c2.holds:
            breaks.append('C2')
        if not c3.holds:
            breaks.append('C3')
        self.breaking = '+'.join(breaks) if breaks else 'NONE'

        # Interpret the breaking pattern
        if not breaks:
            self.interpretation = 'All conditions hold -- trivial or non-self-referential system'
        elif breaks == ['C1']:
            self.interpretation = 'Incompleteness of coherence: defects exist but are manageable (affirmative-type)'
        elif breaks == ['C2']:
            self.interpretation = 'Internal undecidability: system cannot determine its own coherence (Godel-type)'
        elif breaks == ['C3']:
            self.interpretation = 'Topological singularity: self-closure creates irreducible obstruction (gap-type)'
        elif 'C1' in breaks and 'C3' in breaks:
            self.interpretation = 'Defects + singularity: both coherence and closure break (deep gap)'
        else:
            self.interpretation = f'Multiple conditions break: {self.breaking}'


# ================================================================
#  SSA ENGINE
# ================================================================

class SSAEngine:
    """Sanders Singularity Axiom trilemma analyzer.

    Tests C1/C2/C3 for each problem using the spectrometer's existing
    scan infrastructure. Does not replace the spectrometer -- uses it.
    """

    # Thresholds
    ZERO_DELTA_THRESHOLD = 0.01  # Delta below this counts as "zero"
    CONSISTENCY_THRESHOLD = 0.85  # Classification consistency above this = C2 holds
    VARIANCE_THRESHOLD = 0.1     # Delta variance above this = potential singularity
    DIVERGENCE_THRESHOLD = 0.5   # Delta jump above this between adjacent depths = divergence

    def __init__(self, spectrometer):
        self.spec = spectrometer

    def test_c1_coherence(self, problem_id: str, deltas: List[float]) -> C1Result:
        """C1: Total Coherence -- can every internal description extend perfectly?

        Tests whether delta = 0 everywhere (all views are coherent).
        C1 breaks when there exist non-zero deltas.
        """
        if not deltas:
            return C1Result(True, 0.0, 0.0, 0.0, 0, 0)

        n = len(deltas)
        mean_d = sum(deltas) / n
        max_d = max(deltas)
        min_d = min(deltas)
        zero_count = sum(1 for d in deltas if d < self.ZERO_DELTA_THRESHOLD)

        # C1 holds only if ALL deltas are near zero
        holds = (max_d < self.ZERO_DELTA_THRESHOLD)
        return C1Result(holds, mean_d, max_d, min_d, zero_count, n)

    def test_c2_completeness(self, problem_id: str,
                              deltas: List[float]) -> C2Result:
        """C2: Internal Completeness -- can the system decide coherence?

        Tests whether the spectrometer consistently classifies the problem
        the same way across all measurements. If classification flips between
        seeds/depths, the system cannot "decide" its own coherence.
        """
        if not deltas:
            return C2Result(True, 1.0, 'unknown', {})

        # Classify each delta
        classes = []
        for d in deltas:
            if d < self.ZERO_DELTA_THRESHOLD:
                classes.append('affirmative')
            elif d > 0.5:
                classes.append('gap')
            else:
                classes.append('indeterminate')

        # Count classes
        counts = {}
        for c in classes:
            counts[c] = counts.get(c, 0) + 1

        majority = max(counts, key=counts.get)
        consistency = counts[majority] / len(classes)

        holds = (consistency >= self.CONSISTENCY_THRESHOLD)
        return C2Result(holds, consistency, majority, counts)

    def test_c3_singularity(self, problem_id: str,
                             delta_traces: List[List[float]]) -> C3Result:
        """C3: Non-Singularity -- does self-closure have singularities?

        Tests whether delta diverges, oscillates wildly, or becomes
        undefined at any seed/depth combination. Uses delta traces
        (delta at each depth level) to detect divergence.
        """
        if not delta_traces:
            return C3Result(True, 0.0, 0, [])

        max_var = 0.0
        divergence_count = 0
        singular_seeds = []

        for seed_idx, trace in enumerate(delta_traces):
            if len(trace) < 2:
                continue

            # Variance of this trace
            mean = sum(trace) / len(trace)
            var = sum((d - mean) ** 2 for d in trace) / len(trace)
            max_var = max(max_var, var)

            # Check for divergence: large jumps between adjacent depths
            for i in range(1, len(trace)):
                jump = abs(trace[i] - trace[i - 1])
                if jump > self.DIVERGENCE_THRESHOLD:
                    divergence_count += 1
                    if seed_idx not in singular_seeds:
                        singular_seeds.append(seed_idx)
                    break

            # Check for oscillation: sign changes in derivative
            if len(trace) >= 3:
                sign_changes = 0
                for i in range(2, len(trace)):
                    d1 = trace[i - 1] - trace[i - 2]
                    d2 = trace[i] - trace[i - 1]
                    if d1 * d2 < 0:
                        sign_changes += 1
                # Many sign changes = wild oscillation
                if sign_changes > len(trace) * 0.6:
                    if seed_idx not in singular_seeds:
                        singular_seeds.append(seed_idx)

        holds = (max_var < self.VARIANCE_THRESHOLD and divergence_count == 0)
        return C3Result(holds, max_var, divergence_count, singular_seeds)

    def trilemma(self, problem_id: str, deltas: List[float],
                 delta_traces: Optional[List[List[float]]] = None) -> TrilemmaResult:
        """Run all three tests, determine which condition(s) break.

        Args:
            problem_id: Problem identifier
            deltas: Flat list of delta values across seeds
            delta_traces: List of delta-vs-depth traces (one per seed).
                         If None, C3 test uses deltas as a single trace.
        """
        c1 = self.test_c1_coherence(problem_id, deltas)
        c2 = self.test_c2_completeness(problem_id, deltas)

        if delta_traces is None:
            delta_traces = [deltas] if deltas else []
        c3 = self.test_c3_singularity(problem_id, delta_traces)

        return TrilemmaResult(problem_id, c1, c2, c3)

    def ssa_atlas(self, problem_deltas: Dict[str, List[float]],
                  problem_traces: Optional[Dict[str, List[List[float]]]] = None
                  ) -> Dict[str, TrilemmaResult]:
        """Run trilemma for all problems. Returns cross-domain SSA map.

        Args:
            problem_deltas: {problem_id: [delta_values]}
            problem_traces: {problem_id: [[delta_at_depth_3, delta_at_depth_6, ...]]}
        """
        results = {}
        for pid, deltas in problem_deltas.items():
            traces = (problem_traces or {}).get(pid)
            results[pid] = self.trilemma(pid, deltas, traces)
        return results


# ================================================================
#  SIGA CLASSIFIER
# ================================================================

# Geometry bases and coherence operators per domain
SIGA_DOMAINS = {
    # ── 6 Clay Millennium Problems ──
    'navier_stokes': {
        'geometry_base': 'vorticity and strain fields',
        'coherence_operator': 'viscous diffusion (Laplacian)',
        'topology_target': 'coherent vortex tube persistence',
        'failure_mode': 'pressure breaks gluing -> blow-up',
    },
    'p_vs_np': {
        'geometry_base': 'CNF clauses as hypergraph',
        'coherence_operator': 'resolution / unit propagation',
        'topology_target': 'global satisfying assignment (gluing)',
        'failure_mode': 'local geometry cannot produce global topology',
    },
    'riemann': {
        'geometry_base': 'primes and oscillations',
        'coherence_operator': 'functional equation symmetry',
        'topology_target': 'zeros glued to critical line',
        'failure_mode': 'off-line zeros break gluing',
    },
    'yang_mills': {
        'geometry_base': 'gauge curvature',
        'coherence_operator': 'confinement / reflection positivity',
        'topology_target': 'vacuum-excitation gap',
        'failure_mode': 'failure of glue gives massless excitations',
    },
    'bsd': {
        'geometry_base': 'rational points on elliptic curves',
        'coherence_operator': 'analytic/algebraic duality (height pairing)',
        'topology_target': 'rank = order of vanishing',
        'failure_mode': 'Sha = failed gluing',
    },
    'hodge': {
        'geometry_base': 'cohomology classes',
        'coherence_operator': 'motivic correspondence',
        'topology_target': 'algebraic cycle = gluing',
        'failure_mode': 'non-algebraic Hodge classes are unglued',
    },
    # ── 13 Standalone Problems ──
    'collatz': {
        'geometry_base': 'orbit iteration graph (3n+1 / n/2)',
        'coherence_operator': 'descent via even steps',
        'topology_target': 'universal convergence to 1',
        'failure_mode': 'divergent orbit or nontrivial cycle',
    },
    'abc': {
        'geometry_base': 'radical product of coprime triples',
        'coherence_operator': 'additive-multiplicative balance',
        'topology_target': 'quality bounded by 1+epsilon',
        'failure_mode': 'radical too small for sum',
    },
    'langlands': {
        'geometry_base': 'automorphic representations',
        'coherence_operator': 'functorial transfer (L-group)',
        'topology_target': 'reciprocity: Galois = automorphic',
        'failure_mode': 'non-functorial representation',
    },
    'continuum': {
        'geometry_base': 'cardinal hierarchy (aleph_0, 2^aleph_0)',
        'coherence_operator': 'forcing (Cohen)',
        'topology_target': 'CH determination',
        'failure_mode': 'ZFC-independent: no coherent gluing exists',
    },
    'ramsey': {
        'geometry_base': 'partition colorings of complete graphs',
        'coherence_operator': 'pigeonhole / density increment',
        'topology_target': 'monochromatic substructure',
        'failure_mode': 'combinatorial explosion exceeds bounds',
    },
    'twin_primes': {
        'geometry_base': 'prime gap sequence',
        'coherence_operator': 'sieve methods (GPY/Maynard)',
        'topology_target': 'infinitely many gaps <= 2',
        'failure_mode': 'sieve remainder too large',
    },
    'poincare_4d': {
        'geometry_base': 'smooth 4-manifold structure',
        'coherence_operator': 'surgery / handle decomposition',
        'topology_target': 'unique smooth structure on S^4',
        'failure_mode': 'exotic smooth structure obstructs surgery',
    },
    'cosmo_constant': {
        'geometry_base': 'vacuum energy density',
        'coherence_operator': 'quantum-classical gravity bridge',
        'topology_target': 'predicted = observed Lambda',
        'failure_mode': '120 order-of-magnitude hierarchy gap',
    },
    'falconer': {
        'geometry_base': 'fractal dimension of compact sets',
        'coherence_operator': 'Fourier decay / projection theory',
        'topology_target': 'distance set has positive measure',
        'failure_mode': 'dimension drop in projection',
    },
    'jacobian': {
        'geometry_base': 'polynomial endomorphism with det(J)=1',
        'coherence_operator': 'degree bounds / Newton polytope',
        'topology_target': 'global bijectivity',
        'failure_mode': 'non-invertible in dimension >= 2',
    },
    'inverse_galois': {
        'geometry_base': 'finite groups',
        'coherence_operator': 'Hilbert irreducibility / Noether',
        'topology_target': 'every group realized over Q',
        'failure_mode': 'obstruction to realization',
    },
    'banach_tarski': {
        'geometry_base': 'solid ball decomposition',
        'coherence_operator': 'axiom of choice (free group action)',
        'topology_target': 'paradoxical duplication',
        'failure_mode': 'non-measurable sets (proved, pathological)',
    },
    'info_paradox': {
        'geometry_base': 'Hawking radiation quanta',
        'coherence_operator': 'AdS/CFT unitarity / ER=EPR',
        'topology_target': 'information preserved through evaporation',
        'failure_mode': 'unitarity violation at horizon',
    },
    # ── 4 Bridge Problems ──
    'bridge_rmt': {
        'geometry_base': 'random matrix eigenvalue distribution',
        'coherence_operator': 'GUE universality (Montgomery-Odlyzko)',
        'topology_target': 'zeta zeros = GUE eigenvalues',
        'failure_mode': 'spectral statistics deviate',
    },
    'bridge_expander': {
        'geometry_base': 'expander graph spectral gap',
        'coherence_operator': 'Cheeger inequality',
        'topology_target': 'expansion = spectral gap = hardness',
        'failure_mode': 'expansion fails to bridge circuit/gauge',
    },
    'bridge_fractal': {
        'geometry_base': 'turbulent energy cascade',
        'coherence_operator': 'Kolmogorov scaling / zeta regularity',
        'topology_target': 'cascade spectrum = zero distribution',
        'failure_mode': 'intermittency breaks spectral match',
    },
    'bridge_spectral': {
        'geometry_base': 'universal spectral operator',
        'coherence_operator': 'cross-domain trace formula',
        'topology_target': 'all 6 Clay connected via spectrum',
        'failure_mode': 'spectral transfer incoherent across domains',
    },
}


class SIGAClassifier:
    """Classifies each problem's geometry/topology status per SIGA.

    SIGA: Information is geometry only. Topology requires coherence/gluing.
    Every Clay problem is a topology restoration problem on a geometric base.
    """

    def classify(self, problem_id: str, topo_output: dict,
                 delta: float) -> dict:
        """Classify a problem's geometry/topology status.

        Returns dict with:
          geometry_base:     What the pure information pattern is
          coherence_operator: What TIG operator acts as glue
          gluing_status:     'complete' | 'partial' | 'broken'
          topology_status:   'restored' | 'emerging' | 'absent'
          siga_domain:       Full SIGA domain info if available
        """
        # Look up domain info (direct first, then parent for neighbors)
        domain_info = SIGA_DOMAINS.get(problem_id)
        if not domain_info:
            from ck_sim.being.ck_topology_lens import NEIGHBOR_TOPOLOGY_PARENT
            parent = NEIGHBOR_TOPOLOGY_PARENT.get(problem_id, problem_id)
            domain_info = SIGA_DOMAINS.get(parent)

        # Determine gluing status from delta
        if delta < 0.05:
            gluing_status = 'complete'
            topology_status = 'restored'
        elif delta < 0.3:
            gluing_status = 'partial'
            topology_status = 'emerging'
        else:
            gluing_status = 'broken'
            topology_status = 'absent'

        result = {
            'problem_id': problem_id,
            'geometry_base': domain_info['geometry_base'] if domain_info else 'unknown',
            'coherence_operator': domain_info['coherence_operator'] if domain_info else 'unknown',
            'gluing_status': gluing_status,
            'topology_status': topology_status,
            'delta': delta,
        }

        if domain_info:
            result['topology_target'] = domain_info['topology_target']
            result['failure_mode'] = domain_info['failure_mode']

        return result
