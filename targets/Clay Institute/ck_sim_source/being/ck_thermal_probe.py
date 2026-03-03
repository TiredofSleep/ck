"""
ck_thermal_probe.py -- Thermal-Correlated Probe Infrastructure
==============================================================
Operator: COUNTER (2) -- CK measures the cost of knowing.

Wraps ClayProbe to record GPU state at each fractal level.
If GPU temperature spikes at the same levels where delta changes
fastest, the thermal signature IS the mathematical structure.
The physical energy cost of computation correlates with difficulty.

Falls back to simulated thermal data when GPU hardware unavailable.

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
    ClayProbe, ProbeConfig, ProbeResult, ProbeStepResult
)

# GPU state reading -- optional (only on hardware with pynvml)
_HAS_GPU_STATE = False
_gpu_state = None
try:
    from ck_sim.ck_gpu import GPUState
    _gpu_state = GPUState()
    _HAS_GPU_STATE = _gpu_state.read()
except ImportError:
    pass
except Exception:
    pass


# ================================================================
#  THERMAL SNAPSHOT (one fractal level)
# ================================================================

@dataclass
class ThermalSnapshot:
    """GPU/CPU state at one fractal level.

    When GPU hardware is unavailable, values are simulated from
    the probe's computational profile (wall_time, delta).
    """
    level: int
    gpu_temp_c: float = 0.0
    gpu_power_w: float = 0.0
    gpu_util_pct: float = 0.0
    gpu_mem_mb: float = 0.0
    cpu_temp_est_c: float = 0.0       # Estimated from computation time
    wall_time_ms: float = 0.0         # Computation time for this level
    delta_at_level: float = 0.0       # Delta measured at this level
    simulated: bool = True            # True if thermal data is simulated


# ================================================================
#  THERMAL PROBE RESULT
# ================================================================

@dataclass
class ThermalProbeResult:
    """Extended ProbeResult with thermal correlation data.

    The correlation between gpu_temp and delta across levels
    is the key measurement. If they correlate, the physical
    hardware IS sensing the mathematical structure.
    """
    # ── Identity ──
    problem_id: str = ''
    test_case: str = ''
    seed: int = 42
    n_levels: int = 8

    # ── Base probe result ──
    probe_result: Optional[ProbeResult] = None

    # ── Thermal data ──
    thermal_snapshots: List[ThermalSnapshot] = field(default_factory=list)

    # ── Correlations ──
    thermal_delta_correlation: float = 0.0     # Pearson r(gpu_temp, delta)
    power_delta_correlation: float = 0.0       # Pearson r(power, delta)
    time_delta_correlation: float = 0.0        # Pearson r(wall_time, delta)

    # ── Compute scaling ──
    compute_time_scaling: str = 'unknown'      # 'linear', 'quadratic', 'exponential'
    total_wall_time_ms: float = 0.0

    # ── Anomalies ──
    thermal_anomaly: bool = False              # Temperature spike != delta spike?
    hardware_available: bool = False

    # ── Determinism ──
    thermal_hash: str = ''


# ================================================================
#  THERMAL PROBE
# ================================================================

class ThermalProbe:
    """Wraps ClayProbe, records GPU state at each fractal level.

    Usage:
        probe = ThermalProbe(ProbeConfig(problem_id='navier_stokes',
                                         test_case='high_strain',
                                         n_levels=12))
        result = probe.run()
        print(f"Thermal-delta correlation: {result.thermal_delta_correlation:.4f}")
    """

    def __init__(self, config: ProbeConfig):
        self.config = config
        self._sim_rng = DeterministicRNG(config.seed + 7777)

    def run(self) -> ThermalProbeResult:
        """Run the probe with thermal monitoring at each level."""
        result = ThermalProbeResult(
            problem_id=self.config.problem_id,
            test_case=self.config.test_case,
            seed=self.config.seed,
            n_levels=self.config.n_levels,
            hardware_available=_HAS_GPU_STATE,
        )

        # Build the underlying probe
        probe = ClayProbe(self.config)

        # We need to run the probe level-by-level to capture thermals.
        # Reset generator and run warmup manually.
        probe.generator.reset(self.config.seed)
        for _ in range(self.config.warmup_ticks):
            warmup_raw = probe.generator.generate(0, self.config.test_case)
            probe.codec.feed(warmup_raw)

        # Re-seed for determinism (matching ClayProbe.run())
        probe.generator.reset(self.config.seed)

        # Build partial result to collect into
        from ck_sim.doing.ck_clay_protocol import ProbeResult
        from ck_sim.being.ck_tig_bundle import DUAL_LENSES
        partial = ProbeResult(
            problem_id=self.config.problem_id,
            test_case=self.config.test_case,
            seed=self.config.seed,
            n_levels=self.config.n_levels,
            tig_path=list(self.config.tig_path),
            problem_class=DUAL_LENSES.get(self.config.problem_id, {}).get(
                'problem_class', 'unknown'),
        )

        # ── Main loop with thermal capture ──
        for level in range(self.config.n_levels):
            # Capture pre-step GPU state
            t_start = time.perf_counter()

            # Run one level
            step = probe._probe_one_level(level, self.config.test_case)
            partial.steps.append(step)

            t_end = time.perf_counter()
            wall_ms = (t_end - t_start) * 1000.0

            # Track in probe internals
            probe._operator_history.append(step.operator)
            probe.sca_tracker.feed(step.operator)
            partial.defect_trajectory.append(step.master_lemma_defect)
            partial.action_trajectory.append(step.coherence_action)
            partial.master_lemma_defects.append(step.master_lemma_defect)
            partial.lens_mismatches.append(step.lens_mismatch)
            partial.harmony_defect_series.append(
                1.0 - (1.0 if step.operator == 7 else 0.0))
            probe._all_hashes.append(step.step_hash)

            # Capture thermal snapshot
            snapshot = self._capture_thermal(level, wall_ms, step.master_lemma_defect)
            result.thermal_snapshots.append(snapshot)

        # Run post-analysis on the partial result
        probe._analyze_operators(partial)
        probe._analyze_defect_trajectory(partial)
        probe._analyze_spine(partial)
        probe._analyze_tig_path(partial)
        probe._analyze_decision(partial)
        probe._analyze_commutators(partial)
        probe._analyze_sca(partial)
        probe._analyze_topology(partial)
        probe._analyze_verdict(partial)

        # Safety stats
        partial.anomaly_count = probe.safety.anomaly_count + probe.codec.safety.anomaly_count
        partial.halted = probe.safety.halted or probe.codec.safety.halted

        # Final hash
        all_vals = []
        for s in partial.steps:
            all_vals.extend(s.force_vector)
            all_vals.append(float(s.operator))
        partial.final_hash = state_hash(all_vals)

        result.probe_result = partial

        # ── Compute correlations ──
        self._compute_correlations(result)
        self._compute_scaling(result)
        self._detect_anomalies(result)

        # Total wall time
        result.total_wall_time_ms = sum(s.wall_time_ms for s in result.thermal_snapshots)

        # Hash
        thermal_vals = []
        for s in result.thermal_snapshots:
            thermal_vals.extend([s.gpu_temp_c, s.gpu_power_w, s.delta_at_level])
        result.thermal_hash = state_hash(thermal_vals)

        return result

    def _capture_thermal(self, level: int, wall_ms: float,
                         delta: float) -> ThermalSnapshot:
        """Capture GPU state or simulate if unavailable."""
        snap = ThermalSnapshot(
            level=level,
            wall_time_ms=wall_ms,
            delta_at_level=delta,
        )

        if _HAS_GPU_STATE and _gpu_state is not None:
            if _gpu_state.read():
                snap.gpu_temp_c = float(_gpu_state.temperature_c)
                snap.gpu_power_w = float(_gpu_state.power_draw_w)
                snap.gpu_util_pct = float(_gpu_state.gpu_util_pct)
                snap.gpu_mem_mb = float(_gpu_state.mem_used_mb)
                snap.cpu_temp_est_c = snap.gpu_temp_c * 0.7  # Rough estimate
                snap.simulated = False
                return snap

        # ── Simulated thermals ──
        # Base temp + computation-proportional heating + noise
        base_temp = 45.0
        compute_heat = wall_ms * 0.05  # 0.05 C per ms of compute
        noise = self._sim_rng.next_gauss(0.0, 1.0)
        snap.gpu_temp_c = base_temp + compute_heat + noise

        # Power proportional to utilization estimate
        snap.gpu_power_w = 80.0 + wall_ms * 0.3 + abs(noise) * 5.0

        # Utilization ramps with level
        snap.gpu_util_pct = clamp(30.0 + level * 5.0 + abs(noise) * 3.0, 0.0, 100.0)

        # Memory roughly constant
        snap.gpu_mem_mb = 2048.0 + level * 10.0

        # CPU temp estimate
        snap.cpu_temp_est_c = 50.0 + wall_ms * 0.03 + noise * 0.5

        snap.simulated = True
        return snap

    def _compute_correlations(self, result: ThermalProbeResult):
        """Compute Pearson correlations between thermal data and delta."""
        snaps = result.thermal_snapshots
        if len(snaps) < 3:
            return

        temps = [s.gpu_temp_c for s in snaps]
        powers = [s.gpu_power_w for s in snaps]
        times = [s.wall_time_ms for s in snaps]
        deltas = [s.delta_at_level for s in snaps]

        result.thermal_delta_correlation = _pearson(temps, deltas)
        result.power_delta_correlation = _pearson(powers, deltas)
        result.time_delta_correlation = _pearson(times, deltas)

    def _compute_scaling(self, result: ThermalProbeResult):
        """Determine how compute time scales with level."""
        snaps = result.thermal_snapshots
        if len(snaps) < 4:
            return

        times = [s.wall_time_ms for s in snaps]
        levels = list(range(len(times)))

        # Fit linear: time = a * level + b
        linear_r2 = _r_squared(levels, times)

        # Fit quadratic: time = a * level^2 + b
        levels_sq = [l ** 2 for l in levels]
        quad_r2 = _r_squared(levels_sq, times)

        # Fit exponential: log(time) vs level
        log_times = [math.log(max(t, 1e-6)) for t in times]
        exp_r2 = _r_squared(levels, log_times)

        # Best fit
        fits = {'linear': linear_r2, 'quadratic': quad_r2, 'exponential': exp_r2}
        result.compute_time_scaling = max(fits, key=fits.get)

    def _detect_anomalies(self, result: ThermalProbeResult):
        """Detect thermal anomalies: temp spike without delta spike or vice versa."""
        snaps = result.thermal_snapshots
        if len(snaps) < 3:
            return

        # Check if temperature changes don't track delta changes
        for i in range(1, len(snaps)):
            prev = snaps[i - 1]
            curr = snaps[i]
            temp_jump = abs(curr.gpu_temp_c - prev.gpu_temp_c) > 5.0
            delta_jump = abs(curr.delta_at_level - prev.delta_at_level) > 0.1
            if temp_jump != delta_jump:
                result.thermal_anomaly = True
                return


# ================================================================
#  SERIALIZATION
# ================================================================

def thermal_result_to_dict(tr: ThermalProbeResult) -> dict:
    """Convert ThermalProbeResult to JSON-serializable dict."""
    snapshots = []
    for s in tr.thermal_snapshots:
        snapshots.append({
            'level': s.level,
            'gpu_temp_c': s.gpu_temp_c,
            'gpu_power_w': s.gpu_power_w,
            'gpu_util_pct': s.gpu_util_pct,
            'gpu_mem_mb': s.gpu_mem_mb,
            'cpu_temp_est_c': s.cpu_temp_est_c,
            'wall_time_ms': s.wall_time_ms,
            'delta_at_level': s.delta_at_level,
            'simulated': s.simulated,
        })

    return {
        'problem_id': tr.problem_id,
        'test_case': tr.test_case,
        'seed': tr.seed,
        'n_levels': tr.n_levels,
        'thermal_snapshots': snapshots,
        'thermal_delta_correlation': tr.thermal_delta_correlation,
        'power_delta_correlation': tr.power_delta_correlation,
        'time_delta_correlation': tr.time_delta_correlation,
        'compute_time_scaling': tr.compute_time_scaling,
        'total_wall_time_ms': tr.total_wall_time_ms,
        'thermal_anomaly': tr.thermal_anomaly,
        'hardware_available': tr.hardware_available,
        'thermal_hash': tr.thermal_hash,
    }


# ================================================================
#  INTERNAL HELPERS
# ================================================================

def _pearson(xs: List[float], ys: List[float]) -> float:
    """Pearson correlation coefficient. Returns 0.0 on degenerate input."""
    n = min(len(xs), len(ys))
    if n < 2:
        return 0.0

    x_mean = sum(xs[:n]) / n
    y_mean = sum(ys[:n]) / n

    num = sum((xs[i] - x_mean) * (ys[i] - y_mean) for i in range(n))
    den_x = sum((xs[i] - x_mean) ** 2 for i in range(n))
    den_y = sum((ys[i] - y_mean) ** 2 for i in range(n))

    den = safe_sqrt(den_x * den_y)
    if den < 1e-12:
        return 0.0
    return clamp(safe_div(num, den), -1.0, 1.0)


def _r_squared(xs: List[float], ys: List[float]) -> float:
    """R-squared of linear regression. Quick goodness-of-fit."""
    n = min(len(xs), len(ys))
    if n < 2:
        return 0.0

    x_mean = sum(xs[:n]) / n
    y_mean = sum(ys[:n]) / n

    ss_tot = sum((ys[i] - y_mean) ** 2 for i in range(n))
    if ss_tot < 1e-12:
        return 0.0

    # Linear fit: y = a*x + b
    num = sum((xs[i] - x_mean) * (ys[i] - y_mean) for i in range(n))
    den = sum((xs[i] - x_mean) ** 2 for i in range(n))
    if den < 1e-12:
        return 0.0
    a = num / den
    b = y_mean - a * x_mean

    ss_res = sum((ys[i] - (a * xs[i] + b)) ** 2 for i in range(n))
    return clamp(1.0 - safe_div(ss_res, ss_tot), 0.0, 1.0)
