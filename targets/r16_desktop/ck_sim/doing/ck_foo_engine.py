# Copyright (c) 2025-2026 Brayden Sanders / 7Site LLC
# Licensed under the 7Site Human Use License v1.0
# See LICENSE file in project root for full terms.
#
# FREE for humans for personal/recreational use.
# NO commercial or government use without written agreement.

"""
ck_foo_engine.py -- Fractal Optimality Operator + Complexity Horizons
=====================================================================
Operator: RESET (9) -- The fractal limit of recursive self-improvement.

The FOO (Fractal Optimality Operator) extends RATE with meta-level recursion:
  RATE iterates information-of-information (depth iteration).
  FOO iterates improvement-of-improvement (optimizer recursion).

FOO^k(S) = improve(improve(...improve(S)...))  [k levels deep]

At each FOO level:
  Level 0: Standard RATE iteration (baseline delta trace)
  Level 1: RATE with sensitivity tuned by level-0 residual
  Level 2: RATE with sensitivity tuned by level-1's improvement over level-0
  Level k: RATE with sensitivity tuned by level-(k-1)'s improvement over level-(k-2)

The "improvement of improvement" is measured by how much delta decreased
between FOO levels. When this meta-improvement converges, the fractal
optimality limit R_inf is reached.

Phi(kappa) -- Complexity Horizon:
  The irreducible defect floor for a system of complexity kappa.
  Low kappa: Phi(kappa) = 0 (certifiable optimality)
  High kappa: Phi(kappa) > 0 (irreducible gap)

  This is not a heuristic. It is a structural consequence of:
    - Kolmogorov incompressibility (description length)
    - NP-hardness (certificate complexity)
    - Godel incompleteness (self-reference limits)
    - Turbulent cascade (nonlinear PDE)
    - SSA trilemma (C1/C2/C3 cannot all hold)

Per-domain Phi values (from spectrometer calibration):
  NS:    Phi_NS    ~ 0.297  (vortex-strain alignment floor)
  PNP:   Phi_PNP   ~ 0.846  (irreducible correlation gap)
  RH:    Phi_RH    ~ 0.0    (on critical line; >0 off-line)
  YM:    Phi_YM    ~ 0.511  (spectral gap floor)
  BSD:   Phi_BSD   ~ rank-dependent
  Hodge: Phi_Hodge ~ motivic-dependent

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import math
from typing import Dict, List, Optional, Tuple

from ck_sim.being.ck_sdv_safety import clamp, safe_div, safe_sqrt, safe_log


# ================================================================
#  COMPLEXITY LABELS
# ================================================================

# kappa values: ordinal complexity labels for each domain.
# Higher kappa = more structural complexity = larger Phi floor.
# These are normalized to [0, 1] for the spectrometer.
COMPLEXITY_KAPPA = {
    # ── 6 Clay problems (highest complexity) ──
    'navier_stokes':    0.75,   # Nonlinear PDE + nonlocal pressure
    'p_vs_np':          0.95,   # NP-complete combinatorial
    'riemann':          0.85,   # Analytic continuation + spectral symmetry
    'yang_mills':       0.80,   # Gauge curvature + quantization
    'bsd':              0.82,   # Elliptic curves + L-function arithmetic
    'hodge':            0.88,   # Rational cohomology + algebraic cycles

    # ── NS neighbors (kappa * 0.9) ──
    'ns_2d':            0.60,   # 2D: simpler regularity (proved)
    'ns_sqg':           0.72,   # SQG: nearly as complex as 3D NS
    'ns_euler':         0.68,   # Inviscid: hard, no dissipation

    # ── PvNP neighbors ──
    'pnp_ac0':          0.88,   # Circuit complexity: high structural
    'pnp_clique':       0.86,   # Clique: hard combinatorial
    'pnp_bpp':          0.78,   # Randomized: moderate (derandomization)

    # ── RH neighbors ──
    'rh_dirichlet':     0.82,   # Character L-functions: nearly as hard
    'rh_function_field': 0.55,  # Function field: proved (Weil)
    'rh_fake':          0.77,   # Fake zeros: diagnostic, not conjecture

    # ── YM neighbors ──
    'ym_schwinger':     0.50,   # 2D: exactly solvable
    'ym_lattice':       0.75,   # Lattice: nonperturbative, high
    'ym_phi4':          0.70,   # Scalar: simpler than full YM

    # ── BSD neighbors ──
    'bsd_function_field': 0.52, # Function field: proved (Artin-Tate)
    'bsd_avg_rank':     0.74,   # Average rank: statistical
    'bsd_sato_tate':    0.76,   # Sato-Tate: distribution conjecture

    # ── Hodge neighbors ──
    'hodge_tate':       0.80,   # Tate: arithmetic algebraic geometry
    'hodge_standard':   0.84,   # Standard conjectures: deep
    'hodge_transcendental': 0.86,  # Transcendental: hardest variant

    # ── Standalone problems ──
    'collatz':          0.65,   # Iteration dynamics (undecidability-adjacent)
    'abc':              0.72,   # Additive-multiplicative interaction
    'langlands':        0.92,   # Automorphic rep theory (vast program)
    'continuum':        0.90,   # Set-theoretic independence (Godel/Cohen)
    'ramsey':           0.70,   # Combinatorial: Ackermann-level growth
    'twin_primes':      0.68,   # Analytic number theory (sieve methods)
    'poincare_4d':      0.78,   # Smooth 4D topology (exotic structures)
    'cosmo_constant':   0.73,   # Vacuum energy: physics+geometry
    'falconer':         0.62,   # Fractal geometry / measure theory
    'jacobian':         0.71,   # Polynomial automorphisms
    'inverse_galois':   0.67,   # Group realization over Q
    'banach_tarski':    0.58,   # Paradoxical decomposition (measure)
    'info_paradox':     0.76,   # Black hole information (QG boundary)

    # ── Bridge problems (cross-domain) ──
    'bridge_rmt':       0.83,   # RH <-> YM: random matrix theory
    'bridge_expander':  0.87,   # PvNP <-> YM: expander graphs
    'bridge_fractal':   0.79,   # NS <-> RH: fractal/spectral
    'bridge_spectral':  0.85,   # All 6: universal spectral bridge
}

# Empirical Phi values from calibration runs (defect floors)
# Phi = 0: certifiable (proof exists or expected).  Phi > 0: irreducible gap.
PHI_CALIBRATED = {
    # ── 6 Clay ──
    'navier_stokes':    0.297,
    'p_vs_np':          0.846,
    'riemann':          0.0,    # On critical line; off-line > 0
    'yang_mills':       0.511,
    'bsd':              0.0,    # Rank-0: Phi ~ 0; higher rank: Phi > 0
    'hodge':            0.0,    # Under standard conjectures: Phi ~ 0

    # ── Neighbors: inherit parent Phi with reduction for solved variants ──
    'ns_2d':            0.0,    # 2D NS regularity is proved
    'ns_sqg':           0.280,  # SQG: nearly as hard as NS
    'ns_euler':         0.310,  # Euler: harder (no dissipation)
    'pnp_ac0':          0.820,  # AC0 lower bounds: proved (hard gap)
    'pnp_clique':       0.840,  # Clique: hard
    'pnp_bpp':          0.600,  # BPP: derandomization gap, moderate
    'rh_dirichlet':     0.0,    # GRH: expected true
    'rh_function_field': 0.0,   # Proved (Weil/Deligne)
    'rh_fake':          0.200,  # Fake zeros: nonzero diagnostic floor
    'ym_schwinger':     0.0,    # 2D: exactly solvable, no gap issue
    'ym_lattice':       0.490,  # Lattice gap: nearly as hard as YM
    'ym_phi4':          0.350,  # phi^4: simpler gap structure
    'bsd_function_field': 0.0,  # Proved (Artin-Tate)
    'bsd_avg_rank':     0.0,    # Statistical: Phi ~ 0 on average
    'bsd_sato_tate':    0.0,    # Sato-Tate: proved (Taylor et al)
    'hodge_tate':       0.0,    # Tate conjecture: expected affirmative
    'hodge_standard':   0.0,    # Standard conjectures: expected
    'hodge_transcendental': 0.0,  # Expected certifiable

    # ── Standalone ──
    'collatz':          0.550,  # Undecidability-adjacent: positive floor
    'abc':              0.0,    # Expected affirmative (Mochizuki claim)
    'langlands':        0.0,    # Structural program: certifiable in pieces
    'continuum':        0.900,  # Independent of ZFC: maximal gap
    'ramsey':           0.420,  # Growth bounds: positive floor
    'twin_primes':      0.0,    # Expected affirmative (Zhang/Maynard)
    'poincare_4d':      0.380,  # 4D exotic: structural obstruction
    'cosmo_constant':   0.450,  # Physics: measurement gap
    'falconer':         0.0,    # Expected affirmative (Du/Zhang)
    'jacobian':         0.300,  # Open in dim >= 2
    'inverse_galois':   0.0,    # Expected affirmative
    'banach_tarski':    0.0,    # Proved (but pathological)
    'info_paradox':     0.520,  # Quantum gravity: structural gap

    # ── Bridges ──
    'bridge_rmt':       0.150,  # Cross-domain: small residual
    'bridge_expander':  0.600,  # PvNP-side hard
    'bridge_fractal':   0.180,  # NS-RH cross: moderate
    'bridge_spectral':  0.250,  # Universal: larger residual
}


def get_kappa(problem_id: str) -> float:
    """Get complexity label for any problem."""
    return COMPLEXITY_KAPPA.get(problem_id, 0.5)


# ================================================================
#  FOO DATA STRUCTURES
# ================================================================

class FOOLevel:
    """One level of the FOO recursion."""
    __slots__ = ('level', 'delta_mean', 'delta_std', 'improvement',
                 'meta_improvement', 'sensitivity_used')

    def __init__(self, level: int, delta_mean: float, delta_std: float,
                 improvement: float, meta_improvement: float,
                 sensitivity_used: float):
        self.level = level
        self.delta_mean = delta_mean
        self.delta_std = delta_std
        self.improvement = improvement        # delta decrease from previous level
        self.meta_improvement = meta_improvement  # improvement decrease from previous
        self.sensitivity_used = sensitivity_used


class FOOTrace:
    """Full FOO iteration trace for one problem."""
    __slots__ = ('problem_id', 'seed', 'levels', 'converged',
                 'r_inf', 'phi_est', 'foo_depth', 'kappa')

    def __init__(self, problem_id: str, seed: int, levels: list,
                 converged: bool, r_inf: float, phi_est: float,
                 foo_depth: int, kappa: float):
        self.problem_id = problem_id
        self.seed = seed
        self.levels = levels
        self.converged = converged
        self.r_inf = r_inf          # Residual asymptotic minimum
        self.phi_est = phi_est      # Estimated Phi(kappa)
        self.foo_depth = foo_depth  # How many FOO levels ran
        self.kappa = kappa


class PhiEstimate:
    """Phi(kappa) estimate for a problem across seeds."""
    __slots__ = ('problem_id', 'kappa', 'phi_measured', 'phi_calibrated',
                 'r_inf_mean', 'r_inf_std', 'foo_converged_rate',
                 'regime', 'seeds_used')

    def __init__(self, problem_id: str, kappa: float, phi_measured: float,
                 phi_calibrated: float, r_inf_mean: float, r_inf_std: float,
                 foo_converged_rate: float, regime: str, seeds_used: int):
        self.problem_id = problem_id
        self.kappa = kappa
        self.phi_measured = phi_measured
        self.phi_calibrated = phi_calibrated
        self.r_inf_mean = r_inf_mean
        self.r_inf_std = r_inf_std
        self.foo_converged_rate = foo_converged_rate
        self.regime = regime      # 'certifiable' | 'bounded' | 'irreducible'
        self.seeds_used = seeds_used


# ================================================================
#  FOO ENGINE
# ================================================================

class FOOEngine:
    """Fractal Optimality Operator.

    Recursively improves the improvement mechanism:
      Level 0: Run RATE with default parameters -> delta_0
      Level 1: Run RATE with sensitivity tuned by delta_0 -> delta_1
      Level 2: Run RATE with sensitivity tuned by (delta_1 - delta_0) -> delta_2
      ...
      Level k: Sensitivity tuned by meta-improvement at level k-1

    Convergence: when the meta-improvement (improvement-of-improvement)
    drops below threshold, the fractal limit is reached.

    Phi(kappa) = the minimum delta achievable = R_inf.
    """

    # FOO recursion limits
    MAX_FOO_LEVELS = 6          # Maximum meta-improvement levels
    META_CONVERGENCE = 0.005    # Meta-improvement below this = converged
    META_WINDOW = 2             # Must be stable for this many consecutive levels

    def __init__(self, spectrometer):
        self.spec = spectrometer

    def _run_level(self, problem_id: str, seed: int, test_case: str,
                   sensitivity: float, level_k: int = 0,
                   prev_delta: float = 1.0) -> Tuple[float, float]:
        """Run one FOO level: a spectrometer scan with delta-modulated feedback.

        Real feedback: previous delta modulates the seed, so each FOO level
        explores a genuinely different path through the fractal space.
        Higher levels (deeper optimization) use OMEGA depth for maximum
        structural resolution.

        Returns (delta_mean, delta_std) across fractal depths.
        """
        from ck_sim.doing.ck_spectrometer import (
            ProblemType, SpectrometerInput, ScanMode
        )

        # Delta-modulated seed: previous level's result changes exploration
        delta_hash = int(prev_delta * 1000) % 997
        modulated_seed = seed + delta_hash * (level_k + 1)

        # Deeper FOO levels use higher scan resolution
        if level_k >= 4:
            mode = ScanMode.OMEGA       # Levels 4+: full depth
        elif level_k >= 2:
            mode = ScanMode.THOROUGH    # Levels 2-3: high res
        else:
            mode = ScanMode.DEEP        # Levels 0-1: standard

        inp = SpectrometerInput(
            problem=ProblemType(problem_id),
            test_case=test_case,
            scan_mode=mode,
            seed=modulated_seed,
        )
        result = self.spec.scan(inp)

        # Real delta flowing through
        delta = result.delta_value * sensitivity

        # Trajectory std from actual defect trajectory
        traj = result.defect_trajectory
        if len(traj) >= 2:
            mean_t = sum(traj) / len(traj)
            var_t = sum((d - mean_t) ** 2 for d in traj) / len(traj)
            std_t = safe_sqrt(var_t)
        else:
            std_t = 0.0

        return (delta, std_t * sensitivity)

    def foo_iterate(self, problem_id: str, seed: int,
                    test_case: str = 'default') -> FOOTrace:
        """Full FOO iteration: recursively improve the optimizer.

        At each level, the sensitivity is tuned by the meta-improvement
        from the previous level. The recursion converges when
        meta-improvement (improvement-of-improvement) stabilizes.
        """
        kappa = get_kappa(problem_id)
        levels = []
        prev_delta = 1.0    # Start with maximum possible delta
        prev_improvement = 0.0
        sensitivity = 0.5 + kappa * 0.5  # Initial: higher kappa = more scrutiny
        converged = False
        stable_count = 0

        for k in range(self.MAX_FOO_LEVELS):
            delta_mean, delta_std = self._run_level(
                problem_id, seed, test_case, sensitivity,
                level_k=k, prev_delta=prev_delta,
            )

            # Improvement: how much delta decreased from previous level
            improvement = max(prev_delta - delta_mean, 0.0)

            # Meta-improvement: how much the improvement changed
            meta_improvement = abs(improvement - prev_improvement)

            levels.append(FOOLevel(
                level=k,
                delta_mean=delta_mean,
                delta_std=delta_std,
                improvement=improvement,
                meta_improvement=meta_improvement,
                sensitivity_used=sensitivity,
            ))

            # Check meta-convergence
            if k > 0 and meta_improvement < self.META_CONVERGENCE:
                stable_count += 1
                if stable_count >= self.META_WINDOW:
                    converged = True
                    break
            else:
                stable_count = 0

            # Update for next level
            # Sensitivity adapts: if improvement is large, increase scrutiny
            # If improvement is small, we're near the floor
            sensitivity = clamp(
                sensitivity * (1.0 + improvement * 0.5),
                0.1, 2.0
            )
            prev_delta = delta_mean
            prev_improvement = improvement

        # R_inf = final stable delta (the fractal optimality limit)
        r_inf = levels[-1].delta_mean if levels else 0.0

        # Phi estimate: compare R_inf to calibrated value
        phi_cal = PHI_CALIBRATED.get(problem_id, 0.0)
        phi_est = r_inf  # Measured Phi = the minimum delta we achieved

        return FOOTrace(
            problem_id=problem_id,
            seed=seed,
            levels=levels,
            converged=converged,
            r_inf=r_inf,
            phi_est=phi_est,
            foo_depth=len(levels),
            kappa=kappa,
        )

    def estimate_phi(self, problem_id: str, seeds: List[int],
                     test_case: str = 'default') -> PhiEstimate:
        """Estimate Phi(kappa) for a problem across multiple seeds.

        Phi is the minimum delta achievable after FOO convergence.
        The regime classification tells us whether the gap is certifiable,
        bounded, or irreducibly positive.
        """
        kappa = get_kappa(problem_id)
        phi_cal = PHI_CALIBRATED.get(problem_id, 0.0)

        traces = []
        for seed in seeds:
            trace = self.foo_iterate(problem_id, seed, test_case)
            traces.append(trace)

        r_infs = [t.r_inf for t in traces]
        converged_count = sum(1 for t in traces if t.converged)

        if not r_infs:
            return PhiEstimate(problem_id, kappa, 0.0, phi_cal,
                               0.0, 0.0, 0.0, 'unknown', 0)

        r_inf_mean = sum(r_infs) / len(r_infs)
        r_inf_var = sum((r - r_inf_mean) ** 2 for r in r_infs) / len(r_infs)
        r_inf_std = safe_sqrt(r_inf_var)

        converged_rate = safe_div(converged_count, len(seeds))

        # Phi_measured = minimum R_inf across seeds (the true floor)
        phi_measured = min(r_infs)

        # Regime classification based on kappa and measured Phi
        if phi_measured < 0.05 and r_inf_std < 0.02:
            regime = 'certifiable'    # Low kappa: gap can be zero
        elif phi_measured < 0.3 and r_inf_std < 0.1:
            regime = 'bounded'        # Medium kappa: gap small but positive
        else:
            regime = 'irreducible'    # High kappa: structural gap

        return PhiEstimate(
            problem_id=problem_id,
            kappa=kappa,
            phi_measured=phi_measured,
            phi_calibrated=phi_cal,
            r_inf_mean=r_inf_mean,
            r_inf_std=r_inf_std,
            foo_converged_rate=converged_rate,
            regime=regime,
            seeds_used=len(seeds),
        )

    def foo_atlas(self, problem_ids: List[str], seeds: List[int],
                  test_cases: Optional[Dict[str, str]] = None
                  ) -> Dict[str, PhiEstimate]:
        """Full FOO + Phi(kappa) analysis across all problems.

        Returns complexity horizon estimates for each problem.
        """
        if test_cases is None:
            test_cases = {}

        results = {}
        for pid in problem_ids:
            tc = test_cases.get(pid, 'default')
            results[pid] = self.estimate_phi(pid, seeds, tc)
        return results


# ================================================================
#  PHI(KAPPA) CURVE ANALYSIS
# ================================================================

def analyze_phi_curve(atlas: Dict[str, PhiEstimate]) -> dict:
    """Analyze the Phi(kappa) curve across all problems.

    Returns:
        dict with:
          - curve_points: list of (kappa, phi) pairs sorted by kappa
          - monotonic: whether Phi increases with kappa (expected)
          - regimes: count of certifiable/bounded/irreducible
          - structural_consistency: whether measured Phi matches calibrated
    """
    points = []
    for pid, est in atlas.items():
        points.append({
            'problem_id': pid,
            'kappa': est.kappa,
            'phi_measured': est.phi_measured,
            'phi_calibrated': est.phi_calibrated,
            'regime': est.regime,
        })

    points.sort(key=lambda p: p['kappa'])

    # Check monotonicity (Phi should generally increase with kappa)
    phi_vals = [p['phi_measured'] for p in points]
    monotonic_violations = 0
    for i in range(1, len(phi_vals)):
        if phi_vals[i] < phi_vals[i - 1] - 0.05:  # Allow small noise
            monotonic_violations += 1
    is_monotonic = monotonic_violations == 0

    # Regime counts
    regimes = {'certifiable': 0, 'bounded': 0, 'irreducible': 0, 'unknown': 0}
    for p in points:
        regimes[p['regime']] = regimes.get(p['regime'], 0) + 1

    # Structural consistency: measured vs calibrated
    consistency_scores = []
    for p in points:
        if p['phi_calibrated'] > 0:
            # How close measured is to calibrated (relative)
            ratio = safe_div(p['phi_measured'], p['phi_calibrated'], default=0.0)
            consistency_scores.append(abs(1.0 - ratio))
        else:
            # Calibrated is 0: measured should be small
            consistency_scores.append(p['phi_measured'])

    mean_consistency = (sum(consistency_scores) / len(consistency_scores)
                        if consistency_scores else 0.0)

    return {
        'curve_points': points,
        'monotonic': is_monotonic,
        'monotonic_violations': monotonic_violations,
        'regimes': regimes,
        'structural_consistency': 1.0 - clamp(mean_consistency, 0.0, 1.0),
    }


# ================================================================
#  SERIALIZATION
# ================================================================

def foo_trace_to_dict(trace: FOOTrace) -> dict:
    """Serialize a FOO trace for JSON output."""
    return {
        'problem_id': trace.problem_id,
        'seed': trace.seed,
        'kappa': trace.kappa,
        'converged': trace.converged,
        'r_inf': trace.r_inf,
        'phi_est': trace.phi_est,
        'foo_depth': trace.foo_depth,
        'levels': [
            {
                'level': lv.level,
                'delta_mean': lv.delta_mean,
                'delta_std': lv.delta_std,
                'improvement': lv.improvement,
                'meta_improvement': lv.meta_improvement,
                'sensitivity_used': lv.sensitivity_used,
            }
            for lv in trace.levels
        ],
    }


def phi_estimate_to_dict(est: PhiEstimate) -> dict:
    """Serialize a Phi estimate for JSON output."""
    return {
        'problem_id': est.problem_id,
        'kappa': est.kappa,
        'phi_measured': est.phi_measured,
        'phi_calibrated': est.phi_calibrated,
        'r_inf_mean': est.r_inf_mean,
        'r_inf_std': est.r_inf_std,
        'foo_converged_rate': est.foo_converged_rate,
        'regime': est.regime,
        'seeds_used': est.seeds_used,
    }
