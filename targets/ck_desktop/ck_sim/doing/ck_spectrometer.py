# Copyright (c) 2025-2026 Brayden Sanders / 7Site LLC
# Licensed under the 7Site Human Use License v1.0
# See LICENSE file in project root for full terms.
#
# FREE for humans for personal/recreational use.
# NO commercial or government use without written agreement.

"""
ck_spectrometer.py -- TIG-Delta Universal Coherence Spectrometer
================================================================
Operator: HARMONY (7) -- The alignment operator IS the measurement.

The Delta-Spectrometer: a system that ingests arbitrary mathematical
structures (PDE fields, logic instances, L-functions, Yang-Mills
lattices, elliptic curves, Hodge data) and computes the universal
defect functional Delta using TIG operators + SDV.

A machine-level instrument that measures coherence the way a
voltmeter measures charge.

Architecture:
  SpectrometerInput -> DeltaSpectrometer.scan() -> SpectrometerResult
  Internally wraps: ClayProbe(ProbeConfig) -> ProbeResult -> projection

CK measures. CK does not prove.

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import cmath
import math

from dataclasses import dataclass, field
from enum import Enum, IntEnum
from typing import Dict, List, Optional, Tuple

from ck_sim.doing.ck_clay_protocol import (
    ClayProbe, ProbeConfig, ProbeResult, ProbeStepResult,
)
from ck_sim.being.ck_tig_bundle import (
    CLAY_PROBLEMS, ALL_PROBLEMS, DUAL_LENSES, OP_NAMES, NUM_OPS,
    HARMONY, RESET,
)
from ck_sim.being.ck_sdv_safety import safe_div, safe_sqrt


# ================================================================
#  ENUMS
# ================================================================

class ScanMode(IntEnum):
    """Fractal scan depth. Value = n_levels for ProbeConfig."""
    SURFACE = 3    # Bare minimum: D2 warm-up + minimal trajectory
    SHALLOW = 6    # Light probing (RATE depth 6)
    MEDIUM = 9     # Intermediate depth (RATE depth 9)
    DEEP = 12      # Standard research depth
    EXTENDED = 15  # Beyond standard (RATE depth 15)
    THOROUGH = 18  # High-resolution probing (RATE depth 18)
    INTENSIVE = 21 # Near-full structural (RATE depth 21)
    OMEGA = 24     # Full vOmega structural coherence profile


class ProblemType(str, Enum):
    """All problems in the coherence manifold (6 Clay + 35 expansion)."""
    # ── Original 6 Clay Millennium Problems ──
    NAVIER_STOKES = 'navier_stokes'
    P_VS_NP = 'p_vs_np'
    RIEMANN = 'riemann'
    YANG_MILLS = 'yang_mills'
    BSD = 'bsd'
    HODGE = 'hodge'

    # ── NS Neighbors ──
    NS_2D = 'ns_2d'
    NS_SQG = 'ns_sqg'
    NS_EULER = 'ns_euler'

    # ── PvNP Neighbors ──
    PNP_AC0 = 'pnp_ac0'
    PNP_CLIQUE = 'pnp_clique'
    PNP_BPP = 'pnp_bpp'

    # ── RH Neighbors ──
    RH_DIRICHLET = 'rh_dirichlet'
    RH_FUNCTION_FIELD = 'rh_function_field'
    RH_FAKE = 'rh_fake'

    # ── YM Neighbors ──
    YM_SCHWINGER = 'ym_schwinger'
    YM_LATTICE = 'ym_lattice'
    YM_PHI4 = 'ym_phi4'

    # ── BSD Neighbors ──
    BSD_FUNCTION_FIELD = 'bsd_function_field'
    BSD_AVG_RANK = 'bsd_avg_rank'
    BSD_SATO_TATE = 'bsd_sato_tate'

    # ── Hodge Neighbors ──
    HODGE_TATE = 'hodge_tate'
    HODGE_STANDARD = 'hodge_standard'
    HODGE_TRANSCENDENTAL = 'hodge_transcendental'

    # ── Standalone ──
    COLLATZ = 'collatz'
    ABC = 'abc'
    LANGLANDS = 'langlands'
    CONTINUUM = 'continuum'
    RAMSEY = 'ramsey'
    TWIN_PRIMES = 'twin_primes'
    POINCARE_4D = 'poincare_4d'
    COSMO_CONSTANT = 'cosmo_constant'
    FALCONER = 'falconer'
    JACOBIAN = 'jacobian'
    INVERSE_GALOIS = 'inverse_galois'
    BANACH_TARSKI = 'banach_tarski'
    INFO_PARADOX = 'info_paradox'

    # ── Bridges ──
    BRIDGE_RMT = 'bridge_rmt'
    BRIDGE_EXPANDER = 'bridge_expander'
    BRIDGE_FRACTAL = 'bridge_fractal'
    BRIDGE_SPECTRAL = 'bridge_spectral'


class Verdict(str, Enum):
    """Instrument confidence classification.

    Classifies measurement confidence, NOT mathematical truth.
    ProbeResult.measurement_verdict remains the mathematical classification.
    """
    STABLE = 'stable'        # Trajectory consistent with predicted class
    UNSTABLE = 'unstable'    # Trajectory contradicts predicted class or unclear
    CRITICAL = 'critical'    # Near threshold, class assignment uncertain
    SINGULAR = 'singular'    # Safety rails triggered, measurement unreliable


class SkeletonClass(str, Enum):
    """Fractal skeleton classification across scale levels.

    Classifies how Delta behaves as fractal depth varies from 3 to 24.
    The categories are field-dependent fractal invariants -- not noise.
    """
    FROZEN = 'frozen'            # range < 0.001: identical at every scale
    STABLE = 'stable'            # range < 0.02: near-constant, tiny wobble
    BOUNDED = 'bounded'          # range < 0.10: confined, non-trivial CV
    OSCILLATING = 'oscillating'  # range < 0.25: visible periodicity
    WILD = 'wild'                # range >= 0.25: broad, no stable pattern


class MacroClass(str, Enum):
    """Coarse skeleton classification for robustness.

    Groups adjacent SkeletonClass values so boundary transitions
    (FROZEN<->STABLE, BOUNDED<->OSCILLATING) don't count as breaks.
    """
    GROUND = 'ground'            # {FROZEN, STABLE} -- near-constant patterns
    STRUCTURED = 'structured'    # {BOUNDED, OSCILLATING} -- patterned, bounded range
    TURBULENT = 'turbulent'      # {WILD} -- no stable pattern


class GateVerdict(str, Enum):
    """Fractal gate classification for Sanders Attack.

    The fractal atlas acts as a pre-classifier: only configurations
    whose skeleton leaves the expected regime get the expensive
    Sanders Flow analysis.  This narrows the search space massively.
    """
    PASS = 'pass'                # Anomalous: merits deep investigation
    SKIP = 'skip'                # Expected pattern: skip expensive flow


# ================================================================
#  INPUT
# ================================================================

# Calibration and frontier test cases per problem
CALIBRATION_CASES = {
    # ── Original 6 Clay ──
    'navier_stokes': 'lamb_oseen',
    'riemann': 'known_zero',
    'p_vs_np': 'easy',
    'yang_mills': 'bpst_instanton',
    'bsd': 'rank0_match',
    'hodge': 'algebraic',

    # ── NS Neighbors ──
    'ns_2d': 'vortex_patch',
    'ns_sqg': 'smooth_theta',
    'ns_euler': 'vortex_ring',

    # ── PvNP Neighbors ──
    'pnp_ac0': 'small_circuit',
    'pnp_clique': 'sparse_graph',
    'pnp_bpp': 'low_error',

    # ── RH Neighbors ──
    'rh_dirichlet': 'trivial_character',
    'rh_function_field': 'small_genus',
    'rh_fake': 'near_axis',

    # ── YM Neighbors ──
    'ym_schwinger': 'weak_coupling',
    'ym_lattice': 'coarse_lattice',
    'ym_phi4': 'ordered_phase',

    # ── BSD Neighbors ──
    'bsd_function_field': 'rank0_ff',
    'bsd_avg_rank': 'small_family',
    'bsd_sato_tate': 'cm_curve',

    # ── Hodge Neighbors ──
    'hodge_tate': 'abelian_variety',
    'hodge_standard': 'smooth_projective',
    'hodge_transcendental': 'k3_surface',

    # ── Standalone ──
    'collatz': 'small_orbit',
    'abc': 'low_quality',
    'langlands': 'gl2_case',
    'continuum': 'constructible',
    'ramsey': 'small_colors',
    'twin_primes': 'small_gap',
    'poincare_4d': 'standard_sphere',
    'cosmo_constant': 'low_cutoff',
    'falconer': 'high_dimension',
    'jacobian': 'degree_2',
    'inverse_galois': 'cyclic_group',
    'banach_tarski': 'dimension_2',
    'info_paradox': 'large_bh',

    # ── Bridges ──
    'bridge_rmt': 'low_zeros',
    'bridge_expander': 'regular_graph',
    'bridge_fractal': 'k41_cascade',
    'bridge_spectral': 'laplacian',
}

FRONTIER_CASES = {
    # ── Original 6 Clay ──
    'navier_stokes': 'high_strain',
    'riemann': ['off_line', 'rh_singularity'],
    'p_vs_np': 'hard',
    'yang_mills': 'excited',
    'bsd': 'rank_mismatch',
    'hodge': 'analytic_only',

    # ── NS Neighbors ──
    'ns_2d': 'vortex_merger',
    'ns_sqg': 'singular_front',
    'ns_euler': 'blowup_candidate',

    # ── PvNP Neighbors ──
    'pnp_ac0': 'parity_circuit',
    'pnp_clique': 'dense_graph',
    'pnp_bpp': 'high_error',

    # ── RH Neighbors ──
    'rh_dirichlet': 'quadratic_character',
    'rh_function_field': 'high_genus',
    'rh_fake': 'off_line_fake',

    # ── YM Neighbors ──
    'ym_schwinger': 'strong_coupling',
    'ym_lattice': 'fine_lattice',
    'ym_phi4': 'critical_point',

    # ── BSD Neighbors ──
    'bsd_function_field': 'high_rank_ff',
    'bsd_avg_rank': 'large_family',
    'bsd_sato_tate': 'non_cm_curve',

    # ── Hodge Neighbors ──
    'hodge_tate': 'higher_codimension',
    'hodge_standard': 'singular_variety',
    'hodge_transcendental': 'high_dimension_class',

    # ── Standalone ──
    'collatz': 'large_orbit',
    'abc': 'high_quality',
    'langlands': 'gl3_case',
    'continuum': 'forcing_extension',
    'ramsey': 'many_colors',
    'twin_primes': 'large_gap',
    'poincare_4d': 'exotic_candidate',
    'cosmo_constant': 'planck_cutoff',
    'falconer': 'threshold_dimension',
    'jacobian': 'degree_5',
    'inverse_galois': 'sporadic_group',
    'banach_tarski': 'dimension_3',
    'info_paradox': 'small_bh',

    # ── Bridges ──
    'bridge_rmt': 'high_zeros',
    'bridge_expander': 'ramanujan_graph',
    'bridge_fractal': 'intermittent_cascade',
    'bridge_spectral': 'dirac_operator',
}

# Seeds for the 108-run stability matrix
MATRIX_SEEDS = [42, 137, 2718]


def _frontier_cases_for(problem_id: str) -> List[str]:
    """Return list of frontier test cases for a problem.

    Normalizes FRONTIER_CASES entries (str or list) to always return a list.
    """
    entry = FRONTIER_CASES.get(problem_id, 'default')
    if isinstance(entry, list):
        return entry
    return [entry]


@dataclass
class SpectrometerInput:
    """Unified input to the Delta-Spectrometer.

    Wraps all information needed to run a single measurement.
    Internally bridges to ClayProbe via to_probe_config().
    """
    problem: ProblemType
    test_case: str = 'default'
    scan_mode: ScanMode = ScanMode.DEEP
    seed: int = 42
    label: str = ''

    def to_probe_config(self) -> ProbeConfig:
        """Bridge to existing ClayProbe configuration."""
        return ProbeConfig(
            problem_id=self.problem.value,
            test_case=self.test_case,
            seed=self.seed,
            n_levels=int(self.scan_mode),
        )

    @property
    def key(self) -> str:
        """Unique identifier for this input configuration."""
        return f'{self.problem.value}_{self.test_case}_s{self.seed}_L{int(self.scan_mode)}'


# ================================================================
#  RESULT
# ================================================================

@dataclass
class SpectrometerResult:
    """Structured output of a Delta-Spectrometer measurement.

    This is the clean, publication-ready projection of the internal
    ProbeResult into the spectrometer's output format.
    """
    # ── Identity ──
    input_key: str
    problem: str
    test_case: str
    scan_mode: str              # 'SURFACE' | 'DEEP' | 'OMEGA'
    seed: int
    n_levels: int

    # ── Primary measurement ──
    delta_value: float          # = ProbeResult.final_defect
    verdict: str                # Verdict enum value
    reason: str                 # Human-readable verdict explanation

    # ── 10-element operator defect contributions ──
    defect_vector: List[float]  # defect_vector[op] = avg defect at levels classified as op

    # ── Operator event log ──
    tig_trace: List[dict]       # [{level, operator, operator_name, defect, action, band, d2_magnitude}]

    # ── Dual void structure ──
    sdv_map: dict               # {problem_class, lens_a, lens_b, dual_fixed_point_proximity, ...}

    # ── Trajectory ──
    defect_trajectory: List[float]
    action_trajectory: List[float]
    defect_trend: str
    defect_slope: float

    # ── Sub-measurements ──
    harmony_fraction: float = 0.0
    commutator_persistence: float = 0.0
    sca_progress: float = 0.0
    spine_fraction: float = 0.0
    vortex_class: str = 'unknown'

    # ── Mathematical verdict (from ClayProbe) ──
    problem_class: str = 'unknown'
    measurement_verdict: str = 'unknown'

    # ── Determinism + Safety ──
    final_hash: str = ''
    anomaly_count: int = 0
    halted: bool = False


# ================================================================
#  DELTA-SPECTROMETER
# ================================================================

class DeltaSpectrometer:
    """TIG-Delta Universal Coherence Spectrometer.

    A stateless instrument. Each scan creates its own ClayProbe
    internally and returns a SpectrometerResult.

    Usage:
        spec = DeltaSpectrometer()
        result = spec.scan(SpectrometerInput(ProblemType.NAVIER_STOKES))
        results = spec.scan_all(ScanMode.DEEP, seed=42)
        matrix = spec.stability_matrix()
    """

    # ────────────────────────────────────────────────────────────
    #  PUBLIC: scan
    # ────────────────────────────────────────────────────────────

    def scan(self, inp: SpectrometerInput) -> SpectrometerResult:
        """Run a single Delta measurement.

        SpectrometerInput -> ClayProbe -> ProbeResult -> SpectrometerResult
        """
        config = inp.to_probe_config()
        probe = ClayProbe(config)
        pr = probe.run()
        return self._project(inp, pr)

    # ────────────────────────────────────────────────────────────
    #  PUBLIC: scan_all
    # ────────────────────────────────────────────────────────────

    def scan_all(
        self,
        scan_mode: ScanMode = ScanMode.DEEP,
        seed: int = 42,
        suite: str = 'calibration',
    ) -> Dict[str, SpectrometerResult]:
        """Scan all 6 Clay problems with one mode and seed.

        Args:
            scan_mode: SURFACE, DEEP, or OMEGA
            seed: Random seed
            suite: 'calibration' or 'frontier'

        Returns:
            Dict mapping problem_id -> SpectrometerResult
        """
        results = {}
        for pid in CLAY_PROBLEMS:
            pt = ProblemType(pid)
            if suite == 'calibration':
                tc = CALIBRATION_CASES.get(pid, 'default')
                inp = SpectrometerInput(
                    problem=pt, test_case=tc,
                    scan_mode=scan_mode, seed=seed,
                    label=f'{suite}_{scan_mode.name}',
                )
                results[pid] = self.scan(inp)
            else:
                ftcs = _frontier_cases_for(pid)
                for ftc in ftcs:
                    inp = SpectrometerInput(
                        problem=pt, test_case=ftc,
                        scan_mode=scan_mode, seed=seed,
                        label=f'{suite}_{scan_mode.name}',
                    )
                    key = pid if len(ftcs) == 1 else f'{pid}_{ftc}'
                    results[key] = self.scan(inp)
        return results

    # ────────────────────────────────────────────────────────────
    #  PUBLIC: stability_matrix (108 runs)
    # ────────────────────────────────────────────────────────────

    def stability_matrix(self) -> List[SpectrometerResult]:
        """Execute the full 108-run stability matrix.

        12 inputs (2 per problem) x 3 modes x 3 seeds = 108 runs.
        """
        results = []
        for pid in CLAY_PROBLEMS:
            pt = ProblemType(pid)
            # Calibration
            cal_tc = CALIBRATION_CASES[pid]
            for mode in ScanMode:
                for seed in MATRIX_SEEDS:
                    inp = SpectrometerInput(
                        problem=pt, test_case=cal_tc,
                        scan_mode=mode, seed=seed,
                        label='matrix_calibration',
                    )
                    results.append(self.scan(inp))
            # Frontier(s)
            for ftc in _frontier_cases_for(pid):
                for mode in ScanMode:
                    for seed in MATRIX_SEEDS:
                        inp = SpectrometerInput(
                            problem=pt, test_case=ftc,
                            scan_mode=mode, seed=seed,
                            label='matrix_frontier',
                        )
                        results.append(self.scan(inp))
        return results

    # ────────────────────────────────────────────────────────────
    #  PUBLIC: chaos_scan (noise resilience)
    # ────────────────────────────────────────────────────────────

    def chaos_scan(
        self,
        problem: ProblemType,
        test_case: str,
        scan_mode: ScanMode = ScanMode.DEEP,
        seed: int = 42,
        noise_sigmas: Optional[List[float]] = None,
    ) -> List[SpectrometerResult]:
        """Probe noise resilience at multiple sigma levels.

        For each noise sigma, runs a probe with NoisyGenerator injected
        and projects into SpectrometerResult.
        """
        if noise_sigmas is None:
            noise_sigmas = [0.0, 0.01, 0.05, 0.1, 0.2, 0.5]

        results = []
        for sigma in noise_sigmas:
            # Build probe config
            config = ProbeConfig(
                problem_id=problem.value,
                test_case=test_case,
                seed=seed,
                n_levels=int(scan_mode),
            )
            probe = ClayProbe(config)

            # Inject noise into generator if sigma > 0
            if sigma > 0:
                probe.generator = _NoisyGeneratorWrapper(
                    probe.generator, sigma, seed)

            pr = probe.run()
            inp = SpectrometerInput(
                problem=problem, test_case=test_case,
                scan_mode=scan_mode, seed=seed,
                label=f'chaos_sigma={sigma:.3f}',
            )
            results.append(self._project(inp, pr))
        return results

    # ────────────────────────────────────────────────────────────
    #  PUBLIC: consistency_sweep
    # ────────────────────────────────────────────────────────────

    def consistency_sweep(
        self,
        problem: ProblemType,
        test_case: str,
        scan_mode: ScanMode = ScanMode.DEEP,
        n_seeds: int = 100,
        base_seed: int = 1,
    ) -> dict:
        """Run N-seed consistency sweep, check for falsifications.

        Returns aggregate statistics: mean delta, CI, falsification count,
        and per-seed verdicts.
        """
        deltas = []
        verdicts = []
        hashes = []

        for i in range(n_seeds):
            seed = base_seed + i
            inp = SpectrometerInput(
                problem=problem, test_case=test_case,
                scan_mode=scan_mode, seed=seed,
                label=f'consistency_{i}',
            )
            r = self.scan(inp)
            deltas.append(r.delta_value)
            verdicts.append(r.verdict)
            hashes.append(r.final_hash)

        # Statistics
        n = len(deltas)
        mean_d = sum(deltas) / n if n > 0 else 0.0
        var_d = sum((d - mean_d) ** 2 for d in deltas) / n if n > 1 else 0.0
        std_d = var_d ** 0.5

        # 99.9% CI (z = 3.291)
        se = std_d / (n ** 0.5) if n > 0 else 0.0
        ci_lower = mean_d - 3.291 * se
        ci_upper = mean_d + 3.291 * se

        # Falsification = verdict flip to UNSTABLE
        singular_count = sum(1 for v in verdicts if v == Verdict.SINGULAR.value)
        unstable_count = sum(1 for v in verdicts if v == Verdict.UNSTABLE.value)

        return {
            'problem': problem.value,
            'test_case': test_case,
            'scan_mode': scan_mode.name,
            'n_seeds': n_seeds,
            'base_seed': base_seed,
            'delta_mean': mean_d,
            'delta_std': std_d,
            'delta_ci_lower': ci_lower,
            'delta_ci_upper': ci_upper,
            'delta_min': min(deltas) if deltas else 0.0,
            'delta_max': max(deltas) if deltas else 0.0,
            'singular_count': singular_count,
            'unstable_count': unstable_count,
            'falsifications': singular_count + unstable_count,
            'all_hashes_unique': len(set(hashes)) == len(hashes),
        }

    # ────────────────────────────────────────────────────────────
    #  PUBLIC: fractal_scan (Fractal Skeleton Fingerprint)
    # ────────────────────────────────────────────────────────────

    def fractal_scan(
        self,
        problem: ProblemType,
        test_case: str,
        regime: str = 'calibration',
        seed: int = 42,
        max_level: int = 24,
    ) -> 'FractalFingerprint':
        """Probe a single (problem, test_case) at every fractal level 3→max_level.

        Returns a FractalFingerprint with delta_by_level, classification,
        spectral analysis, and cross-problem features.

        This is the core of the Fractal Attack: the TIG skeleton as a
        cross-domain fractal spectrometer on PDE, complexity, number
        theory, gauge theory, arithmetic, and geometry.
        """
        min_level = int(ScanMode.SURFACE)
        levels = list(range(min_level, max_level + 1))
        delta_by_level = []

        for lvl in levels:
            config = ProbeConfig(
                problem_id=problem.value,
                test_case=test_case,
                seed=seed,
                n_levels=lvl,
            )
            pr = ClayProbe(config).run()
            delta_by_level.append(pr.final_defect)

        # Statistics
        n = len(delta_by_level)
        mean_d = sum(delta_by_level) / n if n > 0 else 0.0
        var_d = sum((d - mean_d) ** 2 for d in delta_by_level) / n if n > 1 else 0.0
        std_d = var_d ** 0.5
        cv = safe_div(std_d, abs(mean_d)) if abs(mean_d) > 1e-15 else 0.0
        min_d = min(delta_by_level) if delta_by_level else 0.0
        max_d = max(delta_by_level) if delta_by_level else 0.0
        rng = max_d - min_d

        # Classification
        skel = classify_skeleton(delta_by_level)
        macro = classify_macro(skel)
        s_norm = compute_slope_norm(delta_by_level)

        # Spectral analysis
        magnitudes = _dft_magnitudes(delta_by_level)
        entropy = _spectral_entropy(magnitudes)
        period = _dominant_period(magnitudes, n)

        # Cross-problem features
        dev_level = _first_deviation_level(levels, delta_by_level)
        n_transitions = _count_phase_transitions(delta_by_level)

        return FractalFingerprint(
            problem=problem.value,
            regime=regime,
            test_case=test_case,
            seed=seed,
            levels=levels,
            delta_by_level=delta_by_level,
            delta_mean=mean_d,
            delta_std=std_d,
            delta_cv=cv,
            delta_min=min_d,
            delta_max=max_d,
            delta_range=rng,
            skeleton_class=skel,
            macro_class=macro,
            slope_norm=s_norm,
            spectral_magnitudes=magnitudes,
            dominant_period=period,
            spectral_entropy=entropy,
            first_deviation_level=dev_level,
            n_phase_transitions=n_transitions,
        )

    # ────────────────────────────────────────────────────────────
    #  PUBLIC: fractal_atlas (Full Cross-Problem Atlas)
    # ────────────────────────────────────────────────────────────

    def fractal_atlas(
        self,
        seed: int = 42,
        max_level: int = 24,
    ) -> Dict[str, 'FractalFingerprint']:
        """Build the full Fractal Coherence Atlas.

        All 6 problems x 2 regimes (calibration + frontier) = 12 fingerprints.
        Each fingerprint scans levels 3→max_level.

        Returns dict mapping '{problem}_{regime}' -> FractalFingerprint.
        """
        atlas = {}
        for pid in CLAY_PROBLEMS:
            pt = ProblemType(pid)
            # Calibration
            cal_tc = CALIBRATION_CASES[pid]
            fp = self.fractal_scan(
                problem=pt, test_case=cal_tc,
                regime='calibration', seed=seed, max_level=max_level,
            )
            atlas[f'{pid}_calibration'] = fp
            # Frontier(s)
            ftcs = _frontier_cases_for(pid)
            for ftc in ftcs:
                fp = self.fractal_scan(
                    problem=pt, test_case=ftc,
                    regime='frontier', seed=seed, max_level=max_level,
                )
                suffix = f'_{ftc}' if len(ftcs) > 1 else ''
                atlas[f'{pid}_frontier{suffix}'] = fp
        return atlas

    # ────────────────────────────────────────────────────────────
    #  PUBLIC: equation_extract (single trajectory -> equation)
    # ────────────────────────────────────────────────────────────

    def equation_extract(
        self,
        problem: ProblemType,
        test_case: str,
        regime: str = 'calibration',
        seed: int = 42,
        max_level: int = 24,
    ) -> 'GoverningEquation':
        """Extract the governing equation for one (problem, test_case) pair.

        Runs a fractal scan, then fits parametric models via BIC selection.
        Returns the best-fit GoverningEquation.
        """
        from ck_sim.doing.ck_governing_equations import extract_governing_equation

        fp = self.fractal_scan(problem, test_case, regime, seed, max_level)
        return extract_governing_equation(
            levels=fp.levels,
            delta_by_level=fp.delta_by_level,
            problem=fp.problem,
            regime=fp.regime,
            test_case=fp.test_case,
        )

    # ────────────────────────────────────────────────────────────
    #  PUBLIC: equation_atlas (all problems -> equation atlas)
    # ────────────────────────────────────────────────────────────

    def equation_atlas(
        self,
        seed: int = 42,
        max_level: int = 24,
        problem_set: str = 'clay',
    ) -> 'EquationAtlasResult':
        """Extract governing equations for every (problem, regime) pair.

        Args:
            seed: Random seed
            max_level: Max fractal depth
            problem_set: 'clay' (original 6) or 'all' (41 problems)

        Returns:
            EquationAtlasResult with all equations and classification counts.
        """
        from ck_sim.doing.ck_governing_equations import extract_equation_atlas

        problems = CLAY_PROBLEMS if problem_set == 'clay' else ALL_PROBLEMS
        atlas = {}
        for pid in problems:
            if pid not in CALIBRATION_CASES:
                continue
            pt = ProblemType(pid)
            # Calibration
            cal_tc = CALIBRATION_CASES[pid]
            fp = self.fractal_scan(
                problem=pt, test_case=cal_tc,
                regime='calibration', seed=seed, max_level=max_level,
            )
            atlas[f'{pid}_calibration'] = fp
            # Frontier(s)
            ftcs = _frontier_cases_for(pid)
            for ftc in ftcs:
                fp = self.fractal_scan(
                    problem=pt, test_case=ftc,
                    regime='frontier', seed=seed, max_level=max_level,
                )
                suffix = f'_{ftc}' if len(ftcs) > 1 else ''
                atlas[f'{pid}_frontier{suffix}'] = fp

        return extract_equation_atlas(atlas)

    # ────────────────────────────────────────────────────────────
    #  PUBLIC: fractal_gate (pre-classifier for Sanders Attack)
    # ────────────────────────────────────────────────────────────

    def fractal_gate(
        self, fp: 'FractalFingerprint',
    ) -> Tuple[str, str]:
        """Apply the fractal pre-classifier gate.

        The Fractal Attack recommendation: only treat a configuration as
        a "candidate singularity" when its skeleton leaves the expected
        regime.  Anomalous patterns that merit investigation:

        Calibration regime (expected: frozen/stable/bounded):
          PASS if skeleton is WILD or OSCILLATING -- unexpected turbulence
               in what should be a well-behaved calibration case.

        Frontier regime (expected: problem-dependent):
          PASS if skeleton is WILD -- extreme disorder beyond what the
               problem's frontier should produce.
          PASS if skeleton is FROZEN at high delta (delta >= 0.8) --
               saturated pattern, like YM excited or BSD rank_mismatch.
               These are structurally different and merit investigation.

        Returns:
            Tuple of (gate_verdict, reason) where gate_verdict is a
            GateVerdict value.
        """
        skel = fp.skeleton_class
        regime = fp.regime

        if regime == 'calibration':
            # Calibration should be calm: frozen, stable, or bounded.
            if skel in (SkeletonClass.WILD.value, SkeletonClass.OSCILLATING.value):
                return GateVerdict.PASS.value, (
                    f'Calibration case shows {skel.upper()} skeleton '
                    f'(range={fp.delta_range:.4f}) -- unexpected turbulence'
                )
            return GateVerdict.SKIP.value, (
                f'Calibration case has expected {skel.upper()} skeleton '
                f'(range={fp.delta_range:.4f})'
            )

        # Frontier regime
        if skel == SkeletonClass.WILD.value:
            return GateVerdict.PASS.value, (
                f'Frontier shows WILD skeleton (range={fp.delta_range:.4f}, '
                f'entropy={fp.spectral_entropy:.3f}) -- extreme disorder'
            )

        if skel == SkeletonClass.FROZEN.value and fp.delta_mean >= 0.8:
            return GateVerdict.PASS.value, (
                f'Frontier shows saturated FROZEN at delta={fp.delta_mean:.4f} '
                f'-- structural gap or phase saturation'
            )

        if skel == SkeletonClass.OSCILLATING.value and fp.spectral_entropy > 0.01:
            return GateVerdict.PASS.value, (
                f'Frontier shows OSCILLATING skeleton with non-trivial entropy '
                f'({fp.spectral_entropy:.3f}) -- scale-emergent structure'
            )

        return GateVerdict.SKIP.value, (
            f'Frontier has expected {skel.upper()} skeleton '
            f'(mean={fp.delta_mean:.4f}, range={fp.delta_range:.4f})'
        )

    # ────────────────────────────────────────────────────────────
    #  PUBLIC: sanders_attack (gated flow for one configuration)
    # ────────────────────────────────────────────────────────────

    def sanders_attack(
        self,
        problem: ProblemType,
        test_case: str,
        regime: str = 'calibration',
        seed: int = 42,
        max_level: int = 24,
        flow_strategy: str = 'scale',
        n_flow_steps: int = 10,
    ) -> 'SandersAttackResult':
        """Run a gated Sanders Attack on one (problem, regime) pair.

        Phase 1: Compute fractal fingerprint (skeleton classification).
        Phase 2: Apply fractal gate (PASS = investigate, SKIP = expected).
        Phase 3: If PASS, run Sanders Flow and classify result.

        Args:
            problem: Which Clay problem
            test_case: Test case name
            regime: 'calibration' or 'frontier'
            seed: Random seed
            max_level: Max fractal depth for fingerprint
            flow_strategy: 'noise' or 'scale' for Sanders Flow
            n_flow_steps: Number of flow refinement steps

        Returns:
            SandersAttackResult with fingerprint, gate verdict, and
            optional flow result.
        """
        # Phase 1: Fractal fingerprint
        fp = self.fractal_scan(
            problem=problem, test_case=test_case,
            regime=regime, seed=seed, max_level=max_level,
        )

        # Phase 2: Fractal gate
        gate_v, gate_reason = self.fractal_gate(fp)

        # Phase 3: Conditional Sanders Flow
        flow = None
        candidate = False
        summary = ''

        if gate_v == GateVerdict.PASS.value:
            flow = self.flow_scan(
                problem=problem, test_case=test_case,
                scan_mode=ScanMode.DEEP, seed=seed,
                n_steps=n_flow_steps,
                flow_strategy=flow_strategy,
            )

            # Assess: is this a candidate singularity?
            # For affirmative problems: flow not converging = anomaly
            # For gap problems: flow converging = anomaly
            if flow.problem_class == 'affirmative':
                candidate = not flow.lyapunov_confirmed
                if candidate:
                    summary = (
                        f'CANDIDATE: {fp.skeleton_class.upper()} skeleton + '
                        f'flow NOT Lyapunov-confirmed '
                        f'(mono={flow.monotonicity_score:.1%}, '
                        f'delta={flow.delta_final:.4f})'
                    )
                else:
                    summary = (
                        f'CLEARED: Anomalous skeleton but flow is Lyapunov '
                        f'(mono={flow.monotonicity_score:.1%}, '
                        f'delta={flow.delta_final:.4f})'
                    )
            elif flow.problem_class == 'gap':
                candidate = flow.flow_class == 'convergent'
                if candidate:
                    summary = (
                        f'CANDIDATE: {fp.skeleton_class.upper()} skeleton + '
                        f'flow converges to zero (delta={flow.delta_final:.4f}) '
                        f'-- potential gap violation'
                    )
                else:
                    summary = (
                        f'CONFIRMED GAP: {fp.skeleton_class.upper()} skeleton + '
                        f'flow preserves gap '
                        f'(delta={flow.delta_final:.4f})'
                    )
            else:
                summary = f'Flow complete, class unknown'
        else:
            summary = f'SKIPPED: {gate_reason}'

        return SandersAttackResult(
            problem=problem.value,
            regime=regime,
            test_case=test_case,
            seed=seed,
            fingerprint=fp,
            gate_verdict=gate_v,
            gate_reason=gate_reason,
            flow_result=flow,
            candidate_singularity=candidate,
            attack_summary=summary,
        )

    # ────────────────────────────────────────────────────────────
    #  PUBLIC: sanders_attack_full (all 12 configurations)
    # ────────────────────────────────────────────────────────────

    def sanders_attack_full(
        self,
        seed: int = 42,
        max_level: int = 24,
        flow_strategy: str = 'scale',
        n_flow_steps: int = 10,
    ) -> Dict[str, 'SandersAttackResult']:
        """Run the full Sanders Attack across all 6 problems x 2 regimes.

        12 candidates enter the fractal gate.  Only those that PASS
        get the expensive Sanders Flow analysis.

        Returns:
            Dict mapping '{problem}_{regime}' -> SandersAttackResult
        """
        results = {}
        for pid in CLAY_PROBLEMS:
            pt = ProblemType(pid)
            # Calibration
            tc = CALIBRATION_CASES[pid]
            results[f'{pid}_calibration'] = self.sanders_attack(
                problem=pt, test_case=tc,
                regime='calibration', seed=seed,
                max_level=max_level,
                flow_strategy=flow_strategy,
                n_flow_steps=n_flow_steps,
            )
            # Frontier(s)
            ftcs = _frontier_cases_for(pid)
            for ftc in ftcs:
                suffix = f'_{ftc}' if len(ftcs) > 1 else ''
                key = f'{pid}_frontier{suffix}'
                results[key] = self.sanders_attack(
                    problem=pt, test_case=ftc,
                    regime='frontier', seed=seed,
                    max_level=max_level,
                    flow_strategy=flow_strategy,
                    n_flow_steps=n_flow_steps,
                )
        return results

    # ────────────────────────────────────────────────────────────
    #  PRIVATE: _fractal_scan_perturbed (helper for robustness)
    # ────────────────────────────────────────────────────────────

    def _fractal_scan_perturbed(
        self,
        problem: ProblemType,
        test_case: str,
        regime: str = 'calibration',
        seed: int = 42,
        max_level: int = 24,
        tig_path_override=None,
        generator_wrapper_fn=None,
    ) -> 'FractalFingerprint':
        """Like fractal_scan but with optional perturbation hooks.

        Args:
            tig_path_override: Replace the default TIG path for this problem.
            generator_wrapper_fn: Callable(base_generator) -> wrapped_generator.
        """
        min_level = int(ScanMode.SURFACE)
        levels = list(range(min_level, max_level + 1))
        delta_by_level = []

        for lvl in levels:
            config = ProbeConfig(
                problem_id=problem.value,
                test_case=test_case,
                seed=seed,
                n_levels=lvl,
            )
            if tig_path_override is not None:
                config.tig_path = list(tig_path_override)

            probe = ClayProbe(config)

            if generator_wrapper_fn is not None:
                probe.generator = generator_wrapper_fn(probe.generator)

            pr = probe.run()
            delta_by_level.append(pr.final_defect)

        # Statistics (same logic as fractal_scan)
        n = len(delta_by_level)
        mean_d = sum(delta_by_level) / n if n > 0 else 0.0
        var_d = sum((d - mean_d) ** 2 for d in delta_by_level) / n if n > 1 else 0.0
        std_d = var_d ** 0.5
        cv = safe_div(std_d, abs(mean_d)) if abs(mean_d) > 1e-15 else 0.0
        min_d = min(delta_by_level) if delta_by_level else 0.0
        max_d = max(delta_by_level) if delta_by_level else 0.0
        rng = max_d - min_d

        skel = classify_skeleton(delta_by_level)
        macro = classify_macro(skel)
        s_norm = compute_slope_norm(delta_by_level)
        magnitudes = _dft_magnitudes(delta_by_level)
        entropy = _spectral_entropy(magnitudes)
        period = _dominant_period(magnitudes, n)
        dev_level = _first_deviation_level(levels, delta_by_level)
        n_transitions = _count_phase_transitions(delta_by_level)

        return FractalFingerprint(
            problem=problem.value, regime=regime, test_case=test_case,
            seed=seed, levels=levels, delta_by_level=delta_by_level,
            delta_mean=mean_d, delta_std=std_d, delta_cv=cv,
            delta_min=min_d, delta_max=max_d, delta_range=rng,
            skeleton_class=skel, macro_class=macro, slope_norm=s_norm,
            spectral_magnitudes=magnitudes,
            dominant_period=period, spectral_entropy=entropy,
            first_deviation_level=dev_level,
            n_phase_transitions=n_transitions,
        )

    # ────────────────────────────────────────────────────────────
    #  PRIVATE: _make_trial (helper for robustness)
    # ────────────────────────────────────────────────────────────

    def _make_trial(self, ptype, label, params, baseline, perturbed):
        """Create a PerturbationTrial from baseline vs perturbed fingerprints."""
        b_macro = classify_macro(baseline.skeleton_class)
        p_macro = classify_macro(perturbed.skeleton_class)
        return PerturbationTrial(
            perturbation_type=ptype,
            perturbation_label=label,
            perturbation_params=params,
            baseline_skeleton=baseline.skeleton_class,
            perturbed_skeleton=perturbed.skeleton_class,
            skeleton_preserved=(baseline.skeleton_class == perturbed.skeleton_class),
            delta_mean_shift=perturbed.delta_mean - baseline.delta_mean,
            delta_range_shift=perturbed.delta_range - baseline.delta_range,
            entropy_shift=perturbed.spectral_entropy - baseline.spectral_entropy,
            baseline_macro=b_macro,
            perturbed_macro=p_macro,
            macro_preserved=(b_macro == p_macro),
        )

    # ────────────────────────────────────────────────────────────
    #  PUBLIC: robustness_permutation (TIG path shuffle)
    # ────────────────────────────────────────────────────────────

    def robustness_permutation(
        self,
        problem: ProblemType,
        test_case: str,
        regime: str = 'calibration',
        seed: int = 42,
        max_level: int = 24,
        n_trials: int = 5,
    ) -> List['PerturbationTrial']:
        """Test skeleton robustness under TIG path permutation.

        Shuffles the expected operator sequence and re-runs the fractal
        scan.  The skeleton should be invariant to operator ordering if
        the pattern is intrinsic to the mathematical structure.
        """
        from ck_sim.being.ck_tig_bundle import TIG_PATHS

        baseline = self.fractal_scan(problem, test_case, regime, seed, max_level)
        orig_path = list(TIG_PATHS.get(problem.value, []))

        trials = []
        for i in range(n_trials):
            # Deterministic Fisher-Yates shuffle using LCG
            perm_path = list(orig_path)
            rng_state = seed * 31 + i * 7 + 1000
            for j in range(len(perm_path) - 1, 0, -1):
                rng_state = (rng_state * 6364136223846793005 + 1) & 0xFFFFFFFF
                k = rng_state % (j + 1)
                perm_path[j], perm_path[k] = perm_path[k], perm_path[j]

            perturbed = self._fractal_scan_perturbed(
                problem, test_case, regime, seed, max_level,
                tig_path_override=perm_path,
            )

            trials.append(self._make_trial(
                PerturbationType.TIG_PERMUTATION.value,
                f'perm_{i}',
                {'original_path': [OP_NAMES[o] for o in orig_path],
                 'permuted_path': [OP_NAMES[o] for o in perm_path]},
                baseline, perturbed,
            ))

        return trials

    # ────────────────────────────────────────────────────────────
    #  PUBLIC: robustness_jitter (generator output scaling)
    # ────────────────────────────────────────────────────────────

    def robustness_jitter(
        self,
        problem: ProblemType,
        test_case: str,
        regime: str = 'calibration',
        seed: int = 42,
        max_level: int = 24,
        jitter_levels: Optional[List[float]] = None,
    ) -> List['PerturbationTrial']:
        """Test skeleton robustness under multiplicative generator jitter.

        Each numeric field is scaled by (1 ± jitter%).  Tests whether the
        fingerprint pattern is an artefact of exact numerical values.
        """
        if jitter_levels is None:
            jitter_levels = [0.05, 0.10, 0.25, 0.50]

        baseline = self.fractal_scan(problem, test_case, regime, seed, max_level)

        trials = []
        for jitter in jitter_levels:
            wrapper_fn = lambda gen, j=jitter, s=seed: \
                _JitteredGeneratorWrapper(gen, j, s)

            perturbed = self._fractal_scan_perturbed(
                problem, test_case, regime, seed, max_level,
                generator_wrapper_fn=wrapper_fn,
            )

            trials.append(self._make_trial(
                PerturbationType.GENERATOR_JITTER.value,
                f'jitter_{int(jitter * 100)}pct',
                {'jitter_fraction': jitter},
                baseline, perturbed,
            ))

        return trials

    # ────────────────────────────────────────────────────────────
    #  PUBLIC: robustness_ablation (TIG channel removal)
    # ────────────────────────────────────────────────────────────

    def robustness_ablation(
        self,
        problem: ProblemType,
        test_case: str,
        regime: str = 'calibration',
        seed: int = 42,
        max_level: int = 24,
    ) -> List['PerturbationTrial']:
        """Test skeleton robustness under TIG channel ablation.

        For each non-bookend operator in the problem's TIG path,
        removes it and re-runs the fractal scan.  Identifies which
        operators are structurally necessary for the skeleton pattern.
        """
        from ck_sim.being.ck_tig_bundle import TIG_PATHS, VOID, RESET

        baseline = self.fractal_scan(problem, test_case, regime, seed, max_level)
        orig_path = list(TIG_PATHS.get(problem.value, []))

        # Ablation candidates: non-bookend operators (skip VOID, RESET)
        candidates = []
        for i, op in enumerate(orig_path):
            if op not in (VOID, RESET) and 0 < i < len(orig_path) - 1:
                candidates.append((i, op))

        trials = []
        for idx, op in candidates:
            ablated_path = [o for i, o in enumerate(orig_path) if i != idx]

            perturbed = self._fractal_scan_perturbed(
                problem, test_case, regime, seed, max_level,
                tig_path_override=ablated_path,
            )

            trials.append(self._make_trial(
                PerturbationType.CHANNEL_ABLATION.value,
                f'ablate_{OP_NAMES[op]}',
                {'ablated_operator': OP_NAMES[op], 'ablated_index': idx,
                 'remaining_path': [OP_NAMES[o] for o in ablated_path]},
                baseline, perturbed,
            ))

        return trials

    # ────────────────────────────────────────────────────────────
    #  PUBLIC: robustness_noise (distribution swap)
    # ────────────────────────────────────────────────────────────

    def robustness_noise(
        self,
        problem: ProblemType,
        test_case: str,
        regime: str = 'calibration',
        seed: int = 42,
        max_level: int = 24,
        sigma: float = 0.1,
    ) -> List['PerturbationTrial']:
        """Test skeleton robustness under different noise distributions.

        Injects uniform, Cauchy, and high-sigma uniform noise.  If the
        skeleton class survives all distributions, patterns are
        distribution-independent.
        """
        baseline = self.fractal_scan(problem, test_case, regime, seed, max_level)

        trials = []

        # Trial 1: Uniform noise (existing wrapper)
        wrapper_uniform = lambda gen: _NoisyGeneratorWrapper(gen, sigma, seed)
        perturbed = self._fractal_scan_perturbed(
            problem, test_case, regime, seed, max_level,
            generator_wrapper_fn=wrapper_uniform,
        )
        trials.append(self._make_trial(
            PerturbationType.NOISE_DISTRIBUTION.value,
            f'uniform_sigma={sigma}',
            {'distribution': 'uniform', 'sigma': sigma},
            baseline, perturbed,
        ))

        # Trial 2: Cauchy noise (heavy tails)
        wrapper_cauchy = lambda gen: _CauchyNoiseWrapper(gen, sigma, seed)
        perturbed = self._fractal_scan_perturbed(
            problem, test_case, regime, seed, max_level,
            generator_wrapper_fn=wrapper_cauchy,
        )
        trials.append(self._make_trial(
            PerturbationType.NOISE_DISTRIBUTION.value,
            f'cauchy_sigma={sigma}',
            {'distribution': 'cauchy', 'sigma': sigma},
            baseline, perturbed,
        ))

        # Trial 3: High-sigma uniform (3x)
        wrapper_high = lambda gen: _NoisyGeneratorWrapper(gen, sigma * 3, seed)
        perturbed = self._fractal_scan_perturbed(
            problem, test_case, regime, seed, max_level,
            generator_wrapper_fn=wrapper_high,
        )
        trials.append(self._make_trial(
            PerturbationType.NOISE_DISTRIBUTION.value,
            f'uniform_sigma={sigma * 3:.2f}',
            {'distribution': 'uniform', 'sigma': sigma * 3},
            baseline, perturbed,
        ))

        return trials

    # ────────────────────────────────────────────────────────────
    #  PUBLIC: robustness_deep_seeds (multi-seed stability)
    # ────────────────────────────────────────────────────────────

    def robustness_deep_seeds(
        self,
        problem: ProblemType,
        test_case: str,
        regime: str = 'calibration',
        seeds: Optional[List[int]] = None,
        max_level: int = 24,
    ) -> List['PerturbationTrial']:
        """Test skeleton stability across many random seeds.

        If the skeleton class is preserved across all seeds, the
        pattern is seed-invariant (intrinsic to the mathematical
        structure, not a random artefact).
        """
        if seeds is None:
            seeds = list(range(1, 101))  # 100 seeds

        # First seed = baseline
        baseline = self.fractal_scan(
            problem, test_case, regime, seeds[0], max_level)

        trials = []
        for s in seeds[1:]:
            perturbed = self.fractal_scan(
                problem, test_case, regime, s, max_level)

            trials.append(self._make_trial(
                PerturbationType.MULTI_SEED.value,
                f'seed_{s}',
                {'seed': s},
                baseline, perturbed,
            ))

        return trials

    # ────────────────────────────────────────────────────────────
    #  PUBLIC: robustness_sweep (all perturbations, one config)
    # ────────────────────────────────────────────────────────────

    def robustness_sweep(
        self,
        problem: ProblemType,
        test_case: str,
        regime: str = 'calibration',
        seed: int = 42,
        max_level: int = 24,
        n_deep_seeds: int = 20,
    ) -> 'RobustnessResult':
        """Run all 5 perturbation types for one (problem, regime) config.

        Returns a RobustnessResult with survival rate across all trials.
        """
        baseline = self.fractal_scan(problem, test_case, regime, seed, max_level)

        all_trials = []
        all_trials.extend(self.robustness_permutation(
            problem, test_case, regime, seed, max_level, n_trials=5))
        all_trials.extend(self.robustness_jitter(
            problem, test_case, regime, seed, max_level))
        all_trials.extend(self.robustness_ablation(
            problem, test_case, regime, seed, max_level))
        all_trials.extend(self.robustness_noise(
            problem, test_case, regime, seed, max_level))

        # Reduced seed count for sweep (full deep dive is separate)
        deep_seeds = list(range(1, n_deep_seeds + 1))
        all_trials.extend(self.robustness_deep_seeds(
            problem, test_case, regime, deep_seeds, max_level))

        n_preserved = sum(1 for t in all_trials if t.skeleton_preserved)
        n_total = len(all_trials)
        survival = n_preserved / n_total if n_total > 0 else 0.0

        macro_n_preserved = sum(1 for t in all_trials if t.macro_preserved)
        macro_survival = macro_n_preserved / n_total if n_total > 0 else 0.0

        return RobustnessResult(
            problem=problem.value,
            regime=regime,
            test_case=test_case,
            seed=seed,
            baseline_skeleton=baseline.skeleton_class,
            baseline_delta_mean=baseline.delta_mean,
            baseline_delta_range=baseline.delta_range,
            baseline_entropy=baseline.spectral_entropy,
            trials=all_trials,
            n_trials=n_total,
            n_preserved=n_preserved,
            survival_rate=survival,
            robust=macro_survival >= ROBUSTNESS_THRESHOLD,
            macro_n_preserved=macro_n_preserved,
            macro_survival_rate=macro_survival,
            macro_robust=macro_survival >= ROBUSTNESS_THRESHOLD,
        )

    # ────────────────────────────────────────────────────────────
    #  PUBLIC: robustness_full (all 12 configs)
    # ────────────────────────────────────────────────────────────

    def robustness_full(
        self,
        seed: int = 42,
        max_level: int = 24,
        n_deep_seeds: int = 20,
    ) -> Dict[str, 'RobustnessResult']:
        """Run full robustness sweep across all 6 problems x 2 regimes.

        Returns dict mapping '{problem}_{regime}' -> RobustnessResult.
        """
        results = {}
        for pid in CLAY_PROBLEMS:
            pt = ProblemType(pid)
            # Calibration: single case
            tc = CALIBRATION_CASES[pid]
            results[f'{pid}_calibration'] = self.robustness_sweep(
                pt, tc, 'calibration', seed, max_level, n_deep_seeds)
            # Frontier: may have multiple test cases
            ftcs = _frontier_cases_for(pid)
            for ftc in ftcs:
                suffix = f'_{ftc}' if len(ftcs) > 1 else ''
                key = f'{pid}_frontier{suffix}'
                results[key] = self.robustness_sweep(
                    pt, ftc, 'frontier', seed, max_level, n_deep_seeds)
        return results

    # ────────────────────────────────────────────────────────────
    #  PUBLIC: flow_scan (Sanders Flow -- Lyapunov verification)
    # ────────────────────────────────────────────────────────────

    def flow_scan(
        self,
        problem: ProblemType,
        test_case: str,
        scan_mode: ScanMode = ScanMode.DEEP,
        seed: int = 42,
        n_steps: int = 20,
        sigma_max: float = 1.0,
        flow_strategy: str = 'noise',
    ) -> 'FlowResult':
        """Execute a Sanders Flow measurement.

        Two strategies:
          'noise'  -- Refine from noisy (high sigma) to clean (sigma=0).
                      Approximates Sanders Flow as denoising sweep.
          'scale'  -- Refine from coarse (few levels) to fine (many levels).
                      The fractal levels ARE the flow parameter.  Tracks how
                      TIG operators, gates, resets, and coherence structure
                      evolve with depth.  The physically correct proxy for
                      problems where noise acts as regularisation (NS, YM).

        Args:
            problem: Which Clay problem
            test_case: Test case name
            scan_mode: Target fractal depth (max levels for scale strategy)
            seed: Random seed
            n_steps: Number of refinement steps (default: 20)
            sigma_max: Starting noise level for noise strategy (default: 1.0)
            flow_strategy: 'noise' or 'scale' (default: 'noise')

        Returns:
            FlowResult with monotonicity analysis
        """
        delta_trajectory = []
        verdict_trajectory = []
        step_results = []

        if flow_strategy == 'scale':
            # ── Scale refinement flow ──
            # The fractal levels ARE the Sanders Flow parameter.
            # As depth increases, TIG resolves more structure:
            #   operators stabilise, gates fire, resets land, harmony locks.
            # Lyapunov = Delta converges (or decreases) as depth grows.
            max_levels = int(scan_mode)
            min_levels = int(ScanMode.SURFACE)  # 3

            # Build unique ascending level schedule
            level_set = set()
            for i in range(n_steps):
                if n_steps <= 1:
                    lvl = max_levels
                else:
                    frac = i / (n_steps - 1)
                    lvl = min_levels + (max_levels - min_levels) * frac
                level_set.add(max(min_levels, int(round(lvl))))
            level_steps = sorted(level_set)

            # sigma_steps stores n_levels values for scale strategy
            sigma_steps = [float(lvl) for lvl in level_steps]

            for n_lvl in level_steps:
                config = ProbeConfig(
                    problem_id=problem.value,
                    test_case=test_case,
                    seed=seed,
                    n_levels=n_lvl,
                )
                probe = ClayProbe(config)
                pr = probe.run()
                inp = SpectrometerInput(
                    problem=problem, test_case=test_case,
                    scan_mode=scan_mode, seed=seed,
                    label=f'flow_levels={n_lvl}',
                )
                result = self._project(inp, pr)
                delta_trajectory.append(result.delta_value)
                verdict_trajectory.append(result.verdict)
                step_results.append(result)

        else:
            # ── Noise refinement flow (original) ──
            sigma_steps = []
            for i in range(n_steps):
                if i == n_steps - 1:
                    sigma_steps.append(0.0)  # Final step is always clean
                else:
                    ratio = i / (n_steps - 1)
                    sigma = sigma_max * (1.0 - ratio) ** 2  # Quadratic decay
                    sigma_steps.append(sigma)

            for sigma in sigma_steps:
                config = ProbeConfig(
                    problem_id=problem.value,
                    test_case=test_case,
                    seed=seed,
                    n_levels=int(scan_mode),
                )
                probe = ClayProbe(config)

                if sigma > 0:
                    probe.generator = _NoisyGeneratorWrapper(
                        probe.generator, sigma, seed)

                pr = probe.run()
                inp = SpectrometerInput(
                    problem=problem, test_case=test_case,
                    scan_mode=scan_mode, seed=seed,
                    label=f'flow_sigma={sigma:.4f}',
                )
                result = self._project(inp, pr)
                delta_trajectory.append(result.delta_value)
                verdict_trajectory.append(result.verdict)
                step_results.append(result)

        # ── Monotonicity analysis ──
        violations = []
        mono_count = 0
        for i in range(1, len(delta_trajectory)):
            if delta_trajectory[i] <= delta_trajectory[i - 1] + 1e-9:
                mono_count += 1
            else:
                violations.append(i)

        n_pairs = len(delta_trajectory) - 1
        is_monotone = len(violations) == 0
        monotonicity_score = mono_count / n_pairs if n_pairs > 0 else 1.0

        # ── Asymptotic analysis ──
        delta_initial = delta_trajectory[0]
        delta_final = delta_trajectory[-1]
        delta_drop = delta_initial - delta_final

        # ── Flow classification ──
        problem_class = step_results[-1].problem_class if step_results else 'unknown'
        asymptotic_value = delta_final

        # Convergent = Delta -> near 0; Gap = Delta -> eta > 0
        CONVERGENCE_THRESHOLD = 0.05
        if delta_final < CONVERGENCE_THRESHOLD:
            flow_class = 'convergent'
        else:
            flow_class = 'gap'

        # ── Lyapunov determination ──
        if problem_class == 'affirmative':
            class_consistent = (flow_class == 'convergent')
        elif problem_class == 'gap':
            class_consistent = (flow_class == 'gap')
        else:
            class_consistent = True  # Unknown class: no constraint

        if flow_strategy == 'scale':
            # Scale flow: the fractal levels resolve TIG structure.
            # Lyapunov evidence comes in three forms:
            #   1. Monotone decrease (strongest)
            #   2. Convergence (tail values stabilise)
            #   3. Boundedness (defect doesn't diverge with depth)
            #
            # For affirmative problems, BOUNDED defect = regularity.
            # A blow-up would show defect growing without bound.
            # For gap problems, positive floor = gap evidence.

            # Convergence: tail values within tolerance
            converged = False
            if len(delta_trajectory) >= 3:
                tail = delta_trajectory[-3:]
                spread = max(tail) - min(tail)
                converged = spread < 0.02

            # Boundedness: defect doesn't grow between halves
            bounded = False
            if len(delta_trajectory) >= 6:
                mid = len(delta_trajectory) // 2
                first_half = delta_trajectory[:mid]
                second_half = delta_trajectory[mid:]
                mean_1 = sum(first_half) / len(first_half)
                mean_2 = sum(second_half) / len(second_half)
                # Bounded = second half mean no more than 50% above first
                bounded = mean_2 < mean_1 * 1.5 + 0.01
            elif len(delta_trajectory) >= 2:
                bounded = True  # Too few points to judge divergence

            # Class consistency for scale flow
            if problem_class == 'affirmative':
                # Bounded OR convergent defect = regularity evidence.
                # A true singularity would show unbounded defect growth.
                class_consistent = bounded or (flow_class == 'convergent')
            elif problem_class == 'gap':
                class_consistent = (flow_class == 'gap')
            else:
                class_consistent = True

            lyapunov_confirmed = (
                is_monotone or converged or bounded
            ) and class_consistent
        else:
            # Noise flow: strict monotone required
            lyapunov_confirmed = is_monotone and class_consistent

        return FlowResult(
            problem=problem.value,
            test_case=test_case,
            scan_mode=scan_mode.name,
            seed=seed,
            sigma_steps=sigma_steps,
            delta_trajectory=delta_trajectory,
            verdict_trajectory=verdict_trajectory,
            is_monotone=is_monotone,
            monotonicity_score=monotonicity_score,
            violations=violations,
            delta_initial=delta_initial,
            delta_final=delta_final,
            delta_drop=delta_drop,
            asymptotic_value=asymptotic_value,
            flow_class=flow_class,
            problem_class=problem_class,
            lyapunov_confirmed=lyapunov_confirmed,
            step_results=step_results,
            flow_strategy=flow_strategy,
        )

    # ────────────────────────────────────────────────────────────
    #  PRIVATE: _project (ProbeResult -> SpectrometerResult)
    # ────────────────────────────────────────────────────────────

    def _project(
        self, inp: SpectrometerInput, pr: ProbeResult
    ) -> SpectrometerResult:
        """Project a ProbeResult into the clean SpectrometerResult format."""
        verdict, reason = self._compute_verdict(pr)
        defect_vector = self._compute_defect_vector(pr)
        tig_trace = self._build_tig_trace(pr)
        sdv_map = self._build_sdv_map(pr)

        return SpectrometerResult(
            # Identity
            input_key=inp.key,
            problem=pr.problem_id,
            test_case=pr.test_case,
            scan_mode=inp.scan_mode.name,
            seed=pr.seed,
            n_levels=pr.n_levels,
            # Primary
            delta_value=pr.final_defect,
            verdict=verdict.value,
            reason=reason,
            # Vectors
            defect_vector=defect_vector,
            tig_trace=tig_trace,
            sdv_map=sdv_map,
            # Trajectory
            defect_trajectory=list(pr.defect_trajectory),
            action_trajectory=list(pr.action_trajectory),
            defect_trend=pr.defect_trend,
            defect_slope=pr.defect_slope,
            # Sub-measurements
            harmony_fraction=pr.harmony_fraction,
            commutator_persistence=pr.commutator_persistence,
            sca_progress=pr.sca_progress,
            spine_fraction=pr.spine_fraction,
            vortex_class=pr.vortex_fingerprint.get('vortex_class', 'unknown'),
            # Math verdict
            problem_class=pr.problem_class,
            measurement_verdict=pr.measurement_verdict,
            # Safety
            final_hash=pr.final_hash,
            anomaly_count=pr.anomaly_count,
            halted=pr.halted,
        )

    # ────────────────────────────────────────────────────────────
    #  PRIVATE: _compute_verdict
    # ────────────────────────────────────────────────────────────

    def _compute_verdict(
        self, pr: ProbeResult
    ) -> Tuple[Verdict, str]:
        """Classify instrument confidence from ProbeResult.

        STABLE:   Trajectory consistent with predicted class.
        UNSTABLE: Trajectory contradicts or oscillates.
        CRITICAL: Near decision boundary.
        SINGULAR: Safety rails triggered.
        """
        # Step 1: Safety
        if pr.halted:
            return Verdict.SINGULAR, f'Safety halt: {pr.anomaly_count} anomalies detected'
        if pr.anomaly_count > 10:
            return Verdict.SINGULAR, f'Excessive anomalies: {pr.anomaly_count}'

        pclass = pr.problem_class
        slope = pr.defect_slope
        delta = pr.final_defect

        # Step 2: Affirmative class (NS, RH, BSD, Hodge)
        if pclass == 'affirmative':
            if pr.defect_converges and slope < -0.005:
                return Verdict.STABLE, (
                    f'Defect converges (slope={slope:.4f}), '
                    f'consistent with conjecture'
                )
            if pr.defect_bounded_below and slope > 0.01:
                return Verdict.UNSTABLE, (
                    f'Defect trending UP (slope={slope:.4f}), '
                    f'contradicts convergence'
                )
            if abs(slope) < 0.005 and 0.05 < delta < 0.15:
                return Verdict.CRITICAL, (
                    f'Near threshold (delta={delta:.4f}, slope={slope:.4f}), '
                    f'class uncertain'
                )
            # Default for affirmative: check if measurement verdict is positive
            if pr.measurement_verdict == 'supports_conjecture':
                return Verdict.STABLE, (
                    f'Measurement supports conjecture (delta={delta:.4f})'
                )
            return Verdict.UNSTABLE, (
                f'No clear convergence pattern (delta={delta:.4f}, slope={slope:.4f})'
            )

        # Step 3: Gap class (PNP, YM)
        if pclass == 'gap':
            if pr.defect_bounded_below and slope >= -0.005:
                return Verdict.STABLE, (
                    f'Defect bounded below (delta={delta:.4f}, slope={slope:.4f}), '
                    f'supports gap'
                )
            if pr.defect_converges and slope < -0.01:
                return Verdict.UNSTABLE, (
                    f'Defect converging (slope={slope:.4f}), '
                    f'would undermine gap'
                )
            if abs(slope) < 0.005 and 0.05 < delta < 0.15:
                return Verdict.CRITICAL, (
                    f'Near threshold (delta={delta:.4f}, slope={slope:.4f}), '
                    f'gap uncertain'
                )
            if pr.measurement_verdict == 'supports_gap':
                return Verdict.STABLE, (
                    f'Measurement supports gap (delta={delta:.4f})'
                )
            return Verdict.UNSTABLE, (
                f'No clear gap pattern (delta={delta:.4f}, slope={slope:.4f})'
            )

        # Step 4: Unknown class
        return Verdict.CRITICAL, f'Unknown problem class: {pclass}'

    # ────────────────────────────────────────────────────────────
    #  PRIVATE: _compute_defect_vector
    # ────────────────────────────────────────────────────────────

    def _compute_defect_vector(self, pr: ProbeResult) -> List[float]:
        """Distribute defect across 10 operators.

        defect_vector[op] = average master_lemma_defect at levels
        where the classified operator was op.
        """
        sums = [0.0] * NUM_OPS
        counts = [0] * NUM_OPS
        for step in pr.steps:
            op = step.operator
            if 0 <= op < NUM_OPS:
                sums[op] += step.master_lemma_defect
                counts[op] += 1
        return [safe_div(sums[i], counts[i]) for i in range(NUM_OPS)]

    # ────────────────────────────────────────────────────────────
    #  PRIVATE: _build_tig_trace
    # ────────────────────────────────────────────────────────────

    def _build_tig_trace(self, pr: ProbeResult) -> List[dict]:
        """Extract operator event log from per-level steps."""
        trace = []
        for step in pr.steps:
            trace.append({
                'level': step.level,
                'operator': step.operator,
                'operator_name': step.operator_name,
                'defect': step.master_lemma_defect,
                'action': step.coherence_action,
                'band': step.coherence_band,
                'd2_magnitude': step.d2_magnitude,
            })
        return trace

    # ────────────────────────────────────────────────────────────
    #  PRIVATE: _build_sdv_map
    # ────────────────────────────────────────────────────────────

    def _build_sdv_map(self, pr: ProbeResult) -> dict:
        """Build dual-void structure from DUAL_LENSES + ProbeResult."""
        lens_info = DUAL_LENSES.get(pr.problem_id, {})
        return {
            'problem_class': pr.problem_class,
            'lens_a': lens_info.get('lens_a', ''),
            'lens_b': lens_info.get('lens_b', ''),
            'generator': lens_info.get('generator', ''),
            'dual': lens_info.get('dual', ''),
            'tau_9': lens_info.get('tau_9', ''),
            'dual_fixed_point_proximity': pr.dual_fixed_point_proximity,
            'lens_mismatch_final': (
                pr.lens_mismatches[-1] if pr.lens_mismatches else 0.0
            ),
            'decision_verdict': pr.decision_verdict,
        }

    # ================================================================
    #  META-LENS METHODS (Sprint 5: TopologyLens + Russell + SSA + RATE)
    # ================================================================

    def topology_scan(self, problem: 'ProblemType', test_case: str = 'default',
                      seed: int = 42) -> dict:
        """Run TopologyLens on a problem. Returns I/0/flow decomposition."""
        from ck_sim.being.ck_topology_lens import create_topology_lens
        from ck_sim.being.ck_clay_codecs import create_codec
        from ck_sim.doing.ck_clay_generators import create_generator

        pid = problem.value
        codec = create_codec(pid)
        gen = create_generator(pid, seed)
        raw = gen.generate(level=6, test_case=test_case)
        lens = create_topology_lens(pid, codec)
        return lens.standardized_output(raw)

    def russell_scan(self, problem: 'ProblemType', test_case: str = 'default',
                     seed: int = 42) -> dict:
        """Run Russell codec on a problem. Returns 6D coords + delta_R."""
        from ck_sim.being.ck_russell_codec import RussellCodec

        topo = self.topology_scan(problem, test_case, seed)
        rc = RussellCodec()
        return rc.full_analysis(topo)

    def ssa_analyze(self, problem: 'ProblemType', seeds: list = None,
                    test_case: str = 'default') -> dict:
        """Run SSA trilemma. Returns C1/C2/C3 results."""
        from ck_sim.doing.ck_ssa_engine import SSAEngine

        if seeds is None:
            seeds = list(range(42, 52))

        engine = SSAEngine(self)
        pid = problem.value

        # Collect deltas across seeds
        deltas = []
        for s in seeds:
            inp = SpectrometerInput(
                problem=problem, test_case=test_case,
                scan_mode=ScanMode.SURFACE, seed=s)
            result = self.scan(inp)
            deltas.append(result.delta_value)

        tr = engine.trilemma(pid, deltas)
        return {
            'problem_id': pid,
            'c1_holds': tr.c1.holds, 'c1_description': tr.c1.description,
            'c2_holds': tr.c2.holds, 'c2_description': tr.c2.description,
            'c3_holds': tr.c3.holds, 'c3_description': tr.c3.description,
            'breaking': tr.breaking,
            'interpretation': tr.interpretation,
            'deltas': deltas,
        }

    def rate_scan(self, problem: 'ProblemType', seed: int = 42,
                  test_case: str = 'default', max_depth: int = 24) -> dict:
        """Run RATE R_inf iteration. Returns convergence trace."""
        from ck_sim.doing.ck_rate_engine import RATEEngine

        engine = RATEEngine(self)
        trace = engine.r_iterate(problem.value, seed, test_case, max_depth)
        return engine.trace_to_dict(trace)

    def meta_lens_atlas(self, problem_set: list = None,
                        seeds: list = None) -> dict:
        """Full meta-lens: topology + russell + ssa for all problems.

        RATE is excluded from atlas (too expensive for all 41 problems).
        Run rate_scan individually for specific problems.
        """
        from ck_sim.being.ck_russell_codec import RussellCodec
        from ck_sim.doing.ck_ssa_engine import SSAEngine, SIGAClassifier

        if problem_set is None:
            problem_set = ALL_PROBLEMS
        if seeds is None:
            seeds = list(range(42, 47))  # 5 seeds for atlas

        rc = RussellCodec()
        ssa_engine = SSAEngine(self)
        siga = SIGAClassifier()
        results = {}

        for pid in problem_set:
            pt = ProblemType(pid)
            tc = CALIBRATION_CASES.get(pid, 'default')

            # Topology
            topo = self.topology_scan(pt, tc, seeds[0])

            # Russell
            russell = rc.full_analysis(topo)

            # SSA (across seeds)
            deltas = []
            for s in seeds:
                inp = SpectrometerInput(
                    problem=pt, test_case=tc,
                    scan_mode=ScanMode.SURFACE, seed=s)
                r = self.scan(inp)
                deltas.append(r.delta_value)
            tr = ssa_engine.trilemma(pid, deltas)

            # SIGA
            siga_result = siga.classify(pid, topo, topo.get('defect', 0.0))

            results[pid] = {
                'topology': topo,
                'russell': russell,
                'ssa': {
                    'breaking': tr.breaking,
                    'interpretation': tr.interpretation,
                    'c1': tr.c1.holds, 'c2': tr.c2.holds, 'c3': tr.c3.holds,
                },
                'siga': siga_result,
            }

        return results

    # ================================================================
    #  FOO + PHI(KAPPA) METHODS
    # ================================================================

    def foo_scan(self, problem: 'ProblemType', seed: int = 42,
                 test_case: str = 'default') -> dict:
        """Run FOO iteration. Returns fractal optimality trace."""
        from ck_sim.doing.ck_foo_engine import FOOEngine, foo_trace_to_dict

        engine = FOOEngine(self)
        trace = engine.foo_iterate(problem.value, seed, test_case)
        return foo_trace_to_dict(trace)

    def phi_estimate(self, problem: 'ProblemType', seeds: list = None,
                     test_case: str = 'default') -> dict:
        """Estimate Phi(kappa) for a problem. Returns complexity horizon."""
        from ck_sim.doing.ck_foo_engine import FOOEngine, phi_estimate_to_dict

        if seeds is None:
            seeds = list(range(42, 47))

        engine = FOOEngine(self)
        est = engine.estimate_phi(problem.value, seeds, test_case)
        return phi_estimate_to_dict(est)

    def phi_atlas(self, problem_set: list = None,
                  seeds: list = None) -> dict:
        """Full Phi(kappa) curve across all problems.

        Returns complexity horizon estimates + curve analysis.
        """
        from ck_sim.doing.ck_foo_engine import (
            FOOEngine, phi_estimate_to_dict, analyze_phi_curve
        )

        if problem_set is None:
            problem_set = list(CLAY_PROBLEMS)
        if seeds is None:
            seeds = list(range(42, 45))  # 3 seeds for atlas

        engine = FOOEngine(self)
        atlas = engine.foo_atlas(problem_set, seeds)
        curve = analyze_phi_curve(atlas)

        return {
            'estimates': {pid: phi_estimate_to_dict(est)
                          for pid, est in atlas.items()},
            'curve': curve,
        }

    # ================================================================
    #  BREATH-DEFECT FLOW METHODS
    # ================================================================

    def breath_scan(self, problem: 'ProblemType', seed: int = 42,
                    test_case: str = 'default') -> dict:
        """Run breath analysis on a problem's defect trajectory."""
        from ck_sim.doing.ck_breath_engine import (
            BreathEngine, breath_result_to_dict
        )
        engine = BreathEngine(self)
        result = engine.breath_from_scan(problem.value, seed, test_case)
        return breath_result_to_dict(result)

    def breath_rate_scan(self, problem: 'ProblemType', seed: int = 42,
                         test_case: str = 'default') -> dict:
        """Run breath analysis on a RATE trace."""
        from ck_sim.doing.ck_breath_engine import (
            BreathEngine, breath_result_to_dict
        )
        engine = BreathEngine(self)
        result = engine.breath_from_rate(problem.value, seed, test_case)
        return breath_result_to_dict(result)

    def breath_estimate(self, problem: 'ProblemType', seeds: list = None,
                        test_case: str = 'default') -> dict:
        """Estimate breath health across multiple seeds."""
        from ck_sim.doing.ck_breath_engine import BreathEngine
        if seeds is None:
            seeds = list(range(42, 47))
        engine = BreathEngine(self)
        return engine.breath_estimate(problem.value, seeds, test_case)

    def breath_atlas(self, problem_set: list = None,
                     seeds: list = None) -> dict:
        """Breath atlas across all problems."""
        from ck_sim.doing.ck_breath_engine import BreathEngine
        if problem_set is None:
            problem_set = list(CLAY_PROBLEMS)
        if seeds is None:
            seeds = list(range(42, 45))
        engine = BreathEngine(self)
        return engine.breath_atlas(problem_set, seeds)


# ================================================================
#  FLOW RESULT
# ================================================================

@dataclass
class FlowResult:
    """Structured output of a Sanders Flow scan.

    The Sanders Flow refines a noisy input (high sigma) toward the
    clean signal (sigma=0), tracking whether Delta decreases
    monotonically -- empirical evidence that Delta is a Lyapunov
    functional for the refinement flow.
    """
    # ── Identity ──
    problem: str
    test_case: str
    scan_mode: str
    seed: int

    # ── Flow trajectory ──
    sigma_steps: List[float]            # Noise levels (descending: rough -> refined)
    delta_trajectory: List[float]       # Delta at each sigma step
    verdict_trajectory: List[str]       # Verdict at each step

    # ── Monotonicity analysis ──
    is_monotone: bool                   # True if Delta never increases step-to-step
    monotonicity_score: float           # Fraction of steps where Delta decreased or held
    violations: List[int]               # Indices where Delta increased

    # ── Asymptotic analysis ──
    delta_initial: float                # Delta at highest sigma (roughest)
    delta_final: float                  # Delta at sigma=0 (cleanest)
    delta_drop: float                   # delta_initial - delta_final
    asymptotic_value: float             # = delta_final (what survives sanding)

    # ── Classification ──
    flow_class: str                     # 'convergent' (Delta->0) or 'gap' (Delta->eta>0)
    problem_class: str                  # 'affirmative' or 'gap'
    lyapunov_confirmed: bool            # is_monotone AND class-consistent

    # ── Per-step SpectrometerResults (for deep inspection) ──
    step_results: List[SpectrometerResult] = field(default_factory=list)

    # ── Flow strategy ──
    flow_strategy: str = 'noise'  # 'noise' (sigma sweep) or 'scale' (fractal depth)


# ================================================================
#  SANDERS ATTACK RESULT
# ================================================================

@dataclass
class SandersAttackResult:
    """Result of a Sanders Attack: fractal gate + conditional flow.

    The Sanders Attack feeds the Fractal Coherence Atlas back into the
    Sanders Flow.  The fractal fingerprint acts as a pre-classifier:

    1. Compute the fractal skeleton fingerprint.
    2. Apply the fractal gate:
       - PASS = anomalous pattern, merits deep flow analysis.
       - SKIP = expected pattern, no expensive computation needed.
    3. If PASS, run the Sanders Flow and record the result.

    This narrows the search space massively.  For NS, only configurations
    whose skeleton leaves the bounded/oscillatory regime (and starts
    resembling the WILD off-line RH or saturated YM frontier pattern)
    get flagged as "candidate singularity."
    """
    # ── Identity ──
    problem: str
    regime: str                          # 'calibration' or 'frontier'
    test_case: str
    seed: int

    # ── Phase 1: Fractal fingerprint ──
    fingerprint: 'FractalFingerprint'

    # ── Phase 2: Fractal gate ──
    gate_verdict: str                    # GateVerdict value
    gate_reason: str                     # Why PASS or SKIP

    # ── Phase 3: Sanders Flow (only if gate_verdict == 'pass') ──
    flow_result: Optional['FlowResult'] = None

    # ── Combined assessment ──
    candidate_singularity: bool = False  # True = anomalous AND flow supports
    attack_summary: str = ''             # Human-readable combined verdict

    @property
    def was_investigated(self) -> bool:
        """Whether this configuration passed the gate and was flow-tested."""
        return self.flow_result is not None


# ================================================================
#  ROBUSTNESS / ABLATION TYPES
# ================================================================

ROBUSTNESS_THRESHOLD = 0.75  # Skeleton must survive 75% of perturbations


class PerturbationType(str, Enum):
    """Types of perturbation for robustness testing."""
    TIG_PERMUTATION = 'tig_permutation'
    GENERATOR_JITTER = 'generator_jitter'
    CHANNEL_ABLATION = 'channel_ablation'
    NOISE_DISTRIBUTION = 'noise_distribution'
    MULTI_SEED = 'multi_seed'


@dataclass
class PerturbationTrial:
    """Result of one perturbation trial against a baseline fingerprint."""
    perturbation_type: str
    perturbation_label: str
    perturbation_params: dict
    baseline_skeleton: str
    perturbed_skeleton: str
    skeleton_preserved: bool
    delta_mean_shift: float
    delta_range_shift: float
    entropy_shift: float
    baseline_macro: str = ''        # MacroClass of baseline
    perturbed_macro: str = ''       # MacroClass of perturbed
    macro_preserved: bool = True    # baseline_macro == perturbed_macro


@dataclass
class RobustnessResult:
    """Aggregated robustness result for one (problem, regime) configuration."""
    problem: str
    regime: str
    test_case: str
    seed: int
    baseline_skeleton: str
    baseline_delta_mean: float
    baseline_delta_range: float
    baseline_entropy: float
    trials: list           # List[PerturbationTrial]
    n_trials: int
    n_preserved: int
    survival_rate: float
    robust: bool           # macro_survival_rate >= ROBUSTNESS_THRESHOLD
    macro_n_preserved: int = 0
    macro_survival_rate: float = 0.0
    macro_robust: bool = False


# ================================================================
#  NOISY GENERATOR WRAPPER (for chaos_scan)
# ================================================================

class _NoisyGeneratorWrapper:
    """Wraps a ClayGenerator, injecting calibrated Gaussian noise.

    Used internally by DeltaSpectrometer.chaos_scan().
    """

    def __init__(self, base_generator, sigma: float, seed: int = 42):
        self._base = base_generator
        self._sigma = sigma
        self._rng_seed = seed
        self._counter = 0

    def generate(self, level: int, test_case: str) -> dict:
        """Generate noisy reading: clean + N(0, sigma^2) per field."""
        raw = self._base.generate(level, test_case)
        if self._sigma <= 0:
            return raw

        noisy = {}
        for k, v in raw.items():
            if isinstance(v, (int, float)):
                # Simple LCG for deterministic noise
                self._counter += 1
                noise_seed = (self._rng_seed * 6364136223846793005
                              + self._counter) & 0xFFFFFFFF
                # Box-Muller approximation: use fractional part as uniform [0,1)
                u = (noise_seed & 0xFFFF) / 65536.0
                # Simple noise: (u - 0.5) * 2 * sigma gives uniform in [-sigma, sigma]
                noise = (u - 0.5) * 2.0 * self._sigma
                noisy[k] = float(v) + noise
            else:
                noisy[k] = v
        return noisy

    def reset(self, seed=None):
        """Reset underlying generator."""
        if seed is not None:
            self._rng_seed = seed
        self._counter = 0
        self._base.reset(seed)

    @property
    def problem_id(self):
        return self._base.problem_id


# ================================================================
#  JITTERED GENERATOR WRAPPER (for robustness_jitter)
# ================================================================

class _JitteredGeneratorWrapper:
    """Multiplies each numeric field by (1 + jitter * deterministic_noise).

    Tests whether the fractal skeleton is sensitive to exact input values.
    Used internally by DeltaSpectrometer.robustness_jitter().
    """

    def __init__(self, base_generator, jitter: float, seed: int = 42):
        self._base = base_generator
        self._jitter = jitter
        self._rng_seed = seed
        self._counter = 0

    def generate(self, level: int, test_case: str) -> dict:
        raw = self._base.generate(level, test_case)
        if self._jitter <= 0:
            return raw

        jittered = {}
        for k, v in raw.items():
            if isinstance(v, (int, float)):
                self._counter += 1
                noise_seed = (self._rng_seed * 2862933555777941757
                              + self._counter) & 0xFFFFFFFF
                u = (noise_seed & 0xFFFF) / 65536.0
                factor = 1.0 + self._jitter * (u - 0.5) * 2.0
                jittered[k] = float(v) * factor
            else:
                jittered[k] = v
        return jittered

    def reset(self, seed=None):
        if seed is not None:
            self._rng_seed = seed
        self._counter = 0
        self._base.reset(seed)

    @property
    def problem_id(self):
        return self._base.problem_id


# ================================================================
#  CAUCHY NOISE WRAPPER (for robustness_noise)
# ================================================================

class _CauchyNoiseWrapper:
    """Injects Cauchy (heavy-tail) noise into generator output.

    Tests distribution independence: if the skeleton survives Cauchy
    noise (heavier tails than uniform), patterns are distribution-robust.
    Used internally by DeltaSpectrometer.robustness_noise().
    """

    def __init__(self, base_generator, gamma: float, seed: int = 42):
        self._base = base_generator
        self._gamma = gamma  # Scale parameter
        self._rng_seed = seed
        self._counter = 0

    def generate(self, level: int, test_case: str) -> dict:
        raw = self._base.generate(level, test_case)
        if self._gamma <= 0:
            return raw

        noisy = {}
        for k, v in raw.items():
            if isinstance(v, (int, float)):
                self._counter += 1
                noise_seed = (self._rng_seed * 1103515245
                              + self._counter * 12345) & 0xFFFFFFFF
                u = (noise_seed & 0xFFFF) / 65536.0
                # Clamp away from 0 and 1 to avoid infinity
                u = max(0.001, min(0.999, u))
                # Cauchy quantile: gamma * tan(pi * (u - 0.5))
                cauchy_noise = self._gamma * math.tan(math.pi * (u - 0.5))
                # Clamp to ±5 gamma to prevent extreme outliers
                cauchy_noise = max(-5.0 * self._gamma,
                                   min(5.0 * self._gamma, cauchy_noise))
                noisy[k] = float(v) + cauchy_noise
            else:
                noisy[k] = v
        return noisy

    def reset(self, seed=None):
        if seed is not None:
            self._rng_seed = seed
        self._counter = 0
        self._base.reset(seed)

    @property
    def problem_id(self):
        return self._base.problem_id


# ================================================================
#  FRACTAL FINGERPRINT (Fractal Attack Data Structure)
# ================================================================

@dataclass
class FractalFingerprint:
    """Fractal skeleton fingerprint for a single (problem, regime) pair.

    Records delta(L) for L=3→max_level, statistical summary,
    skeleton classification, and spectral analysis.

    The fractal fingerprint is a field-dependent invariant -- not noise.
    Each Clay problem has its own fractal truth structure, and the TIG
    skeleton is the first tool that measures it.
    """
    # ── Identity ──
    problem: str
    regime: str                      # 'calibration' or 'frontier'
    test_case: str
    seed: int
    levels: List[int]                # [3, 4, ..., 24]
    delta_by_level: List[float]      # delta(L) at each level

    # ── Statistics ──
    delta_mean: float
    delta_std: float
    delta_cv: float                  # coefficient of variation
    delta_min: float
    delta_max: float
    delta_range: float

    # ── Skeleton classification ──
    skeleton_class: str              # SkeletonClass value

    # ── Spectral analysis ──
    spectral_magnitudes: List[float] # DFT magnitude spectrum (positive freq)
    dominant_period: Optional[float] # period of strongest non-DC frequency
    spectral_entropy: float          # Shannon entropy of power spectrum

    # ── Cross-problem features ──
    first_deviation_level: int       # level where delta first deviates from L=3
    n_phase_transitions: int         # significant slope sign changes

    # ── Macro classification (defaults for backward compat) ──
    macro_class: str = ''            # MacroClass value (GROUND/STRUCTURED/TURBULENT)
    slope_norm: float = 0.0          # RMS of level-to-level slopes


# ================================================================
#  FRACTAL SKELETON HELPERS
# ================================================================

def classify_skeleton(delta_values: List[float]) -> str:
    """Classify a delta sequence into a SkeletonClass.

    FROZEN:      range < 0.001  -- identical at every scale
    STABLE:      range < 0.02   -- near-constant, tiny wobble
    BOUNDED:     range < 0.10   -- confined, non-trivial CV
    OSCILLATING: range < 0.25   -- visible periodicity
    WILD:        range >= 0.25  -- broad, no stable pattern
    """
    if not delta_values:
        return SkeletonClass.WILD.value

    rng = max(delta_values) - min(delta_values)
    if rng < 0.001:
        return SkeletonClass.FROZEN.value
    elif rng < 0.02:
        return SkeletonClass.STABLE.value
    elif rng < 0.10:
        return SkeletonClass.BOUNDED.value
    elif rng < 0.25:
        return SkeletonClass.OSCILLATING.value
    else:
        return SkeletonClass.WILD.value


# Mapping from fine skeleton class to macro class
_SKELETON_TO_MACRO = {
    SkeletonClass.FROZEN.value: MacroClass.GROUND.value,
    SkeletonClass.STABLE.value: MacroClass.GROUND.value,
    SkeletonClass.BOUNDED.value: MacroClass.STRUCTURED.value,
    SkeletonClass.OSCILLATING.value: MacroClass.STRUCTURED.value,
    SkeletonClass.WILD.value: MacroClass.TURBULENT.value,
}


def classify_macro(skeleton_class: str) -> str:
    """Map a SkeletonClass value to its MacroClass.

    GROUND     = {FROZEN, STABLE}
    STRUCTURED = {BOUNDED, OSCILLATING}
    TURBULENT  = {WILD}
    """
    return _SKELETON_TO_MACRO.get(skeleton_class, MacroClass.TURBULENT.value)


def compute_slope_norm(delta_values: List[float]) -> float:
    """RMS of level-to-level slopes in a delta sequence.

    slope_norm = sqrt(mean(s_i^2)) where s_i = delta[i+1] - delta[i].
    Second classification dimension: small range AND small slope_norm
    firmly places a sequence in GROUND.
    """
    n = len(delta_values)
    if n < 2:
        return 0.0
    slopes = [delta_values[i + 1] - delta_values[i] for i in range(n - 1)]
    mean_sq = sum(s * s for s in slopes) / len(slopes)
    return mean_sq ** 0.5


def _dft_magnitudes(values: List[float]) -> List[float]:
    """Compute DFT magnitude spectrum (positive frequencies only).

    Uses a straightforward O(N^2) DFT since sequences are short (~22 points).
    Returns magnitudes normalised by N for each frequency bin k=0..N//2.
    """
    N = len(values)
    if N == 0:
        return []
    mags = []
    for k in range(N // 2 + 1):
        s = sum(
            values[n] * cmath.exp(-2j * cmath.pi * k * n / N)
            for n in range(N)
        )
        mags.append(abs(s) / N)
    return mags


def _spectral_entropy(magnitudes: List[float]) -> float:
    """Shannon entropy of the normalised power spectrum.

    High entropy = energy spread across many frequencies (noisy/wild).
    Low entropy = energy concentrated at few frequencies (frozen/periodic).
    """
    powers = [m * m for m in magnitudes]
    total = sum(powers)
    if total <= 0:
        return 0.0
    probs = [p / total for p in powers]
    return -sum(p * math.log(p + 1e-30) for p in probs if p > 0)


def _dominant_period(magnitudes: List[float], N: int) -> Optional[float]:
    """Period of the strongest non-DC frequency component.

    Skips k=0 (the DC/mean component).
    Returns N/k_max in units of levels, or None if flat spectrum.
    """
    if len(magnitudes) < 2:
        return None
    # Skip k=0 (DC component)
    ac_mags = magnitudes[1:]
    if not ac_mags or max(ac_mags) < 1e-10:
        return None
    k_max = ac_mags.index(max(ac_mags)) + 1  # +1 because we skipped k=0
    return N / k_max if k_max > 0 else None


def _first_deviation_level(
    levels: List[int], deltas: List[float], epsilon: float = 0.01,
) -> int:
    """Level where delta first deviates by > epsilon from its initial value."""
    if not deltas:
        return levels[0] if levels else 0
    base = deltas[0]
    for lvl, d in zip(levels, deltas):
        if abs(d - base) > epsilon:
            return lvl
    return levels[-1] if levels else 0


def _count_phase_transitions(
    deltas: List[float], threshold: float = 0.03,
) -> int:
    """Count significant slope sign changes in the delta sequence.

    A phase transition = slope sign reversal where both slopes
    exceed the threshold. Filters out tiny jitter.
    """
    if len(deltas) < 3:
        return 0
    transitions = 0
    prev_slope = deltas[1] - deltas[0]
    for i in range(2, len(deltas)):
        curr_slope = deltas[i] - deltas[i - 1]
        if abs(curr_slope) > threshold and abs(prev_slope) > threshold:
            if (curr_slope > 0) != (prev_slope > 0):
                transitions += 1
        if abs(curr_slope) > threshold:
            prev_slope = curr_slope
    return transitions
