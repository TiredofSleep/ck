"""
ck_clay_attack.py -- Statistical & Noise-Resilience Attack Infrastructure
=========================================================================
Operator: CHAOS (6) -- Probe the boundary. Shake the measurement.

Hardware Attack infrastructure for Clay SDV Protocol:
  1. StatisticalSweep:  N-seed probes with confidence intervals
  2. NoisyGenerator:    Calibrated noise injection wrapper
  3. NoiseResilienceSweep: Structural depth measurement via noise tolerance

CK measures on real hardware. Thermals and noise ARE data.
The physical cost of computation correlates with mathematical structure.

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import math
import time
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

from ck_sim.being.ck_sdv_safety import (
    DeterministicRNG, clamp, safe_div, safe_sqrt, state_hash
)
from ck_sim.doing.ck_clay_protocol import (
    ClayProbe, ProbeConfig, ProbeResult
)
from ck_sim.being.ck_tig_bundle import CLAY_PROBLEMS


# ================================================================
#  SWEEP RESULT (statistical aggregate of N probes)
# ================================================================

@dataclass
class SweepResult:
    """Aggregated result from N independent probes with distinct seeds.

    CK measures. CK does not prove. But CK CAN establish empirical
    bounds with statistical confidence. If delta >= eta with p < epsilon,
    that is an empirical fact about the measurement.
    """
    problem_id: str
    test_case: str
    n_seeds: int
    n_levels: int

    # ── Aggregate statistics ──
    delta_mean: float = 0.0
    delta_std: float = 0.0
    delta_ci_lower: float = 0.0       # 99.9% CI lower bound
    delta_ci_upper: float = 0.0       # 99.9% CI upper bound
    delta_min: float = 1.0            # Minimum delta across all seeds
    delta_max: float = 0.0            # Maximum delta across all seeds
    empirical_bound: float = 0.0      # Conservative lower bound

    # ── Convergence ──
    convergence_rate: float = 0.0     # How fast mean stabilizes with N
    bound_confidence: float = 0.0     # 1 - 1/N (Bonferroni)

    # ── Per-seed data ──
    per_seed_finals: List[float] = field(default_factory=list)
    per_seed_hashes: List[str] = field(default_factory=list)

    # ── Trajectory statistics ──
    mean_trajectory: List[float] = field(default_factory=list)
    std_trajectory: List[float] = field(default_factory=list)

    # ── Verdict statistics ──
    supports_conjecture_count: int = 0
    supports_gap_count: int = 0
    inconclusive_count: int = 0

    # ── Timing ──
    total_time_s: float = 0.0
    per_probe_time_s: float = 0.0

    # ── Determinism ──
    all_hashes_unique: bool = True
    sweep_hash: str = ''


# ================================================================
#  STATISTICAL SWEEP
# ================================================================

class StatisticalSweep:
    """Run N probes with distinct seeds, compute statistical bounds.

    Usage:
        sweep = StatisticalSweep('navier_stokes', 'high_strain', n_seeds=100)
        result = sweep.run()
        print(f"delta = {result.delta_mean:.4f} +/- {result.delta_std:.4f}")
        print(f"99.9% CI: [{result.delta_ci_lower:.4f}, {result.delta_ci_upper:.4f}]")
    """

    def __init__(self, problem_id: str, test_case: str,
                 n_seeds: int = 100, n_levels: int = 12,
                 base_seed: int = 1):
        self.problem_id = problem_id
        self.test_case = test_case
        self.n_seeds = n_seeds
        self.n_levels = n_levels
        self.base_seed = base_seed

    def run(self) -> SweepResult:
        """Execute the full statistical sweep."""
        result = SweepResult(
            problem_id=self.problem_id,
            test_case=self.test_case,
            n_seeds=self.n_seeds,
            n_levels=self.n_levels,
        )

        t0 = time.time()

        # Collect per-level trajectories for mean/std
        all_trajectories: List[List[float]] = []

        for i in range(self.n_seeds):
            seed = self.base_seed + i

            config = ProbeConfig(
                problem_id=self.problem_id,
                test_case=self.test_case,
                seed=seed,
                n_levels=self.n_levels,
            )
            probe = ClayProbe(config)
            probe_result = probe.run()

            # Record final defect
            result.per_seed_finals.append(probe_result.final_defect)
            result.per_seed_hashes.append(probe_result.final_hash)

            # Record trajectory
            all_trajectories.append(list(probe_result.defect_trajectory))

            # Count verdicts
            if probe_result.measurement_verdict == 'supports_conjecture':
                result.supports_conjecture_count += 1
            elif probe_result.measurement_verdict == 'supports_gap':
                result.supports_gap_count += 1
            else:
                result.inconclusive_count += 1

        elapsed = time.time() - t0
        result.total_time_s = elapsed
        result.per_probe_time_s = safe_div(elapsed, self.n_seeds)

        # ── Compute statistics ──
        finals = result.per_seed_finals
        n = len(finals)
        if n == 0:
            return result

        # Mean and std
        result.delta_mean = sum(finals) / n
        if n > 1:
            var = sum((f - result.delta_mean) ** 2 for f in finals) / (n - 1)
            result.delta_std = safe_sqrt(var)
        result.delta_min = min(finals)
        result.delta_max = max(finals)

        # 99.9% CI (z = 3.291 for 99.9%)
        z = 3.291
        se = safe_div(result.delta_std, safe_sqrt(float(n)))
        result.delta_ci_lower = result.delta_mean - z * se
        result.delta_ci_upper = result.delta_mean + z * se

        # Conservative empirical bound: minimum observed delta
        result.empirical_bound = result.delta_min

        # Bonferroni-corrected confidence
        result.bound_confidence = 1.0 - safe_div(1.0, float(n))

        # ── Convergence rate ──
        # How fast the running mean stabilizes
        if n >= 4:
            running_means = []
            running_sum = 0.0
            for i, f in enumerate(finals):
                running_sum += f
                running_means.append(running_sum / (i + 1))
            # Rate = std of second half of running means vs first half
            half = n // 2
            first_half_std = _list_std(running_means[:half])
            second_half_std = _list_std(running_means[half:])
            if first_half_std > 0:
                result.convergence_rate = clamp(
                    1.0 - safe_div(second_half_std, first_half_std))
            else:
                result.convergence_rate = 1.0

        # ── Mean trajectory ──
        if all_trajectories:
            max_len = max(len(t) for t in all_trajectories)
            mean_traj = []
            std_traj = []
            for level in range(max_len):
                vals = [t[level] for t in all_trajectories if level < len(t)]
                if vals:
                    m = sum(vals) / len(vals)
                    mean_traj.append(m)
                    if len(vals) > 1:
                        v = sum((x - m) ** 2 for x in vals) / (len(vals) - 1)
                        std_traj.append(safe_sqrt(v))
                    else:
                        std_traj.append(0.0)
            result.mean_trajectory = mean_traj
            result.std_trajectory = std_traj

        # ── Hash uniqueness (different seeds should produce different hashes) ──
        result.all_hashes_unique = len(set(result.per_seed_hashes)) == n

        # ── Sweep hash ──
        all_vals = list(finals)
        result.sweep_hash = state_hash(all_vals)

        return result


# ================================================================
#  NOISY GENERATOR (wraps any ClayGenerator)
# ================================================================

class NoisyGenerator:
    """Wraps any ClayGenerator, injects calibrated Gaussian noise.

    The noise resilience curve IS the measurement: a mathematically
    deep truth should be resilient to noise. A shallow coincidence
    should break easily. The sigma at which delta first deviates
    quantifies structural depth.
    """

    def __init__(self, base_generator, noise_sigma: float, noise_seed: int = 9999):
        self.base = base_generator
        self.noise_sigma = noise_sigma
        self.noise_rng = DeterministicRNG(noise_seed)
        self.problem_id = base_generator.problem_id
        self.seed = base_generator.seed

    def generate(self, level: int, test_case: str = 'default') -> dict:
        """Generate a noisy reading: base + N(0, sigma^2) per field."""
        clean = self.base.generate(level, test_case)
        noisy = {}
        for key, value in clean.items():
            if isinstance(value, (int, float)):
                perturbation = self.noise_rng.next_gauss(0.0, self.noise_sigma)
                noisy_val = value + perturbation
                # Clamp [0,1] fields, leave unbounded fields as-is
                if isinstance(value, float) and 0.0 <= value <= 1.0:
                    noisy[key] = clamp(noisy_val)
                elif isinstance(value, int):
                    # Integer fields: round and keep non-negative
                    noisy[key] = max(0, round(noisy_val))
                else:
                    noisy[key] = noisy_val
            else:
                noisy[key] = value
        return noisy

    def reset(self, seed=None):
        """Reset both base and noise generators."""
        self.base.reset(seed)
        self.noise_rng = DeterministicRNG(9999)


# ================================================================
#  NOISE RESILIENCE RESULT
# ================================================================

@dataclass
class NoiseResult:
    """Result of a noise resilience sweep.

    The critical_noise sigma where delta first deviates > 10%
    quantifies structural depth. Higher = deeper mathematical truth.
    """
    problem_id: str
    test_case: str
    noise_levels: List[float] = field(default_factory=list)
    delta_at_noise: List[float] = field(default_factory=list)
    critical_noise: float = 0.0           # sigma where delta deviates > 10%
    structural_depth: float = 0.0         # = critical_noise
    resilience_curve: List[Tuple[float, float]] = field(default_factory=list)
    base_delta: float = 0.0               # delta at sigma=0
    noise_hash: str = ''


# ================================================================
#  NOISE RESILIENCE SWEEP
# ================================================================

class NoiseResilienceSweep:
    """Sweep noise from 0 to max, measure delta stability.

    Usage:
        sweep = NoiseResilienceSweep('navier_stokes', 'high_strain')
        result = sweep.run()
        print(f"Structural depth: {result.structural_depth:.4f}")
    """

    DEFAULT_SIGMAS = [0.0, 0.01, 0.05, 0.1, 0.2, 0.5]

    def __init__(self, problem_id: str, test_case: str,
                 sigmas: Optional[List[float]] = None,
                 seed: int = 42, n_levels: int = 8):
        self.problem_id = problem_id
        self.test_case = test_case
        self.sigmas = sigmas if sigmas is not None else list(self.DEFAULT_SIGMAS)
        self.seed = seed
        self.n_levels = n_levels

    def run(self) -> NoiseResult:
        """Execute the noise resilience sweep."""
        from ck_sim.doing.ck_clay_generators import create_generator

        result = NoiseResult(
            problem_id=self.problem_id,
            test_case=self.test_case,
        )

        for sigma in self.sigmas:
            # Create base generator
            base_gen = create_generator(self.problem_id, self.seed)

            if sigma == 0.0:
                # Clean probe
                config = ProbeConfig(
                    problem_id=self.problem_id,
                    test_case=self.test_case,
                    seed=self.seed,
                    n_levels=self.n_levels,
                )
                probe = ClayProbe(config)
                probe_result = probe.run()
            else:
                # Wrap generator with noise
                noisy_gen = NoisyGenerator(base_gen, sigma, noise_seed=int(sigma * 10000) + 1)
                # Run probe with noisy generator manually
                probe_result = self._run_noisy_probe(noisy_gen, sigma)

            delta = probe_result.final_defect
            result.noise_levels.append(sigma)
            result.delta_at_noise.append(delta)
            result.resilience_curve.append((sigma, delta))

        # Base delta (at sigma=0)
        if result.delta_at_noise:
            result.base_delta = result.delta_at_noise[0]

        # Find critical noise: first sigma where delta deviates > 10% from base
        if result.base_delta > 0:
            for sigma, delta in result.resilience_curve:
                if sigma == 0.0:
                    continue
                deviation = abs(delta - result.base_delta) / max(result.base_delta, 1e-10)
                if deviation > 0.1:
                    result.critical_noise = sigma
                    break
            else:
                # Never deviated: structural depth is beyond our sweep
                result.critical_noise = max(self.sigmas) if self.sigmas else 0.0
        else:
            # Base delta is 0 -- any noise that produces delta > 0.05 is critical
            for sigma, delta in result.resilience_curve:
                if sigma == 0.0:
                    continue
                if delta > 0.05:
                    result.critical_noise = sigma
                    break
            else:
                result.critical_noise = max(self.sigmas) if self.sigmas else 0.0

        result.structural_depth = result.critical_noise
        result.noise_hash = state_hash(result.delta_at_noise)

        return result

    def _run_noisy_probe(self, noisy_gen: NoisyGenerator, sigma: float) -> ProbeResult:
        """Run a probe with a noisy generator injected."""
        from ck_sim.being.ck_clay_codecs import create_codec
        from ck_sim.being.ck_sdv_safety import CompressOnlySafety

        config = ProbeConfig(
            problem_id=self.problem_id,
            test_case=self.test_case,
            seed=self.seed,
            n_levels=self.n_levels,
        )

        # Build a probe but replace its generator with the noisy one
        probe = ClayProbe(config)
        probe.generator = noisy_gen

        return probe.run()


# ================================================================
#  SERIALIZATION HELPERS
# ================================================================

def sweep_result_to_dict(sr: SweepResult) -> dict:
    """Convert SweepResult to JSON-serializable dict."""
    return {
        'problem_id': sr.problem_id,
        'test_case': sr.test_case,
        'n_seeds': sr.n_seeds,
        'n_levels': sr.n_levels,
        'delta_mean': sr.delta_mean,
        'delta_std': sr.delta_std,
        'delta_ci_lower': sr.delta_ci_lower,
        'delta_ci_upper': sr.delta_ci_upper,
        'delta_min': sr.delta_min,
        'delta_max': sr.delta_max,
        'empirical_bound': sr.empirical_bound,
        'convergence_rate': sr.convergence_rate,
        'bound_confidence': sr.bound_confidence,
        'per_seed_finals': sr.per_seed_finals,
        'mean_trajectory': sr.mean_trajectory,
        'std_trajectory': sr.std_trajectory,
        'supports_conjecture_count': sr.supports_conjecture_count,
        'supports_gap_count': sr.supports_gap_count,
        'inconclusive_count': sr.inconclusive_count,
        'total_time_s': sr.total_time_s,
        'per_probe_time_s': sr.per_probe_time_s,
        'all_hashes_unique': sr.all_hashes_unique,
        'sweep_hash': sr.sweep_hash,
    }


def noise_result_to_dict(nr: NoiseResult) -> dict:
    """Convert NoiseResult to JSON-serializable dict."""
    return {
        'problem_id': nr.problem_id,
        'test_case': nr.test_case,
        'noise_levels': nr.noise_levels,
        'delta_at_noise': nr.delta_at_noise,
        'critical_noise': nr.critical_noise,
        'structural_depth': nr.structural_depth,
        'base_delta': nr.base_delta,
        'resilience_curve': nr.resilience_curve,
        'noise_hash': nr.noise_hash,
    }


# ================================================================
#  INTERNAL HELPERS
# ================================================================

def _list_std(values: List[float]) -> float:
    """Standard deviation of a list of floats."""
    n = len(values)
    if n < 2:
        return 0.0
    mean = sum(values) / n
    var = sum((v - mean) ** 2 for v in values) / (n - 1)
    return safe_sqrt(var)
