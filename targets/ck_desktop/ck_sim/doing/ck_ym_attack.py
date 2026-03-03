# Copyright (c) 2025-2026 Brayden Sanders / 7Site LLC
# Licensed under the 7Site Human Use License v1.0
# See LICENSE file in project root for full terms.
#
# FREE for humans for personal/recreational use.
# NO commercial or government use without written agreement.

"""
ck_ym_attack.py -- YM-3/YM-4 Deep Probes: Weak Coupling + Spectral Gap Persistence
====================================================================================
Operator: CHAOS (6) -- Probe the boundary. Shake the measurement.

Deep probes for Yang-Mills Gap YM-3 (weak coupling continuum limit)
and Gap YM-4 (mass gap persistence at all scales).

YM-3: Does the mass gap survive the continuum limit?
  - Sweep beta from 5.0 to 7.0 (weak coupling regime)
  - At each beta: fractal scan at OMEGA depth, N seeds
  - Fit delta(beta) = A * exp(-B * beta) + C
  - If C > 0, mass gap survives continuum limit

YM-4: Does the mass gap persist at infinite volume?
  - Sweep lattice size L from 8 to 128
  - At each L: fractal scan at OMEGA depth, N seeds
  - Fit delta_min(L) = A * L^alpha + floor
  - If floor > 0, mass gap persists in thermodynamic limit

CK measures. CK does not prove.

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import math
import sys
import time
from typing import Dict, List, Optional, Tuple

from ck_sim.being.ck_sdv_safety import (
    clamp, safe_div, safe_sqrt, safe_log, DeterministicRNG,
)
from ck_sim.doing.ck_clay_protocol import ClayProbe, ProbeConfig, ProbeResult
from ck_sim.being.ck_tig_bundle import CLAY_PROBLEMS


# ================================================================
#  HELPERS
# ================================================================

def _list_mean(vals):
    # type: (List[float]) -> float
    """Mean of a list, safe against empty."""
    if not vals:
        return 0.0
    return sum(vals) / len(vals)


def _list_std(vals):
    # type: (List[float]) -> float
    """Sample standard deviation, safe against <2 values."""
    n = len(vals)
    if n < 2:
        return 0.0
    m = sum(vals) / n
    var = sum((v - m) ** 2 for v in vals) / (n - 1)
    return safe_sqrt(var)


def _list_min(vals):
    # type: (List[float]) -> float
    """Min of a list, safe against empty."""
    return min(vals) if vals else 0.0


def _list_max(vals):
    # type: (List[float]) -> float
    """Max of a list, safe against empty."""
    return max(vals) if vals else 0.0


def _linspace(start, stop, n):
    # type: (float, float, int) -> List[float]
    """Pure Python linspace. Returns n evenly spaced values [start, stop]."""
    if n <= 1:
        return [start]
    step = (stop - start) / (n - 1)
    return [start + i * step for i in range(n)]


# ================================================================
#  YM-3 DEEP PROBE: Weak Coupling Continuum Limit
# ================================================================

class YM3DeepProbe:
    """YM-3 Gap Attack: Weak coupling continuum limit extrapolation.

    The weak_coupling test case parametrizes beta = 5.5 + level * 0.15.
    fractal_scan runs levels 3..max_level, so beta sweeps from
    5.95 (level=3) to 5.5 + 0.15*max_level (level=max_level).

    At each seed, we get the full delta_by_level trajectory.
    Across N seeds, we aggregate mean/std at each level.
    Then fit delta(level) = A * exp(-B * level) + C.

    If C > 0, the mass gap defect has a floor: it survives the
    continuum limit (beta -> infinity).
    """

    def __init__(self, n_seeds=100, max_level=24):
        # type: (int, int) -> None
        self.n_seeds = n_seeds
        self.max_level = max_level

    def run(self):
        # type: () -> dict
        """Execute weak_coupling fractal scan at multiple seeds.

        Returns dict with:
          - levels, betas, mean_by_level, std_by_level
          - fit_params (A, B, C, residual, floor)
          - continuum (floor_C, floor_positive, mass_gap_survives, ...)
          - timing, n_seeds, n_probes
        """
        # Deferred import to avoid circular deps at module level
        from ck_sim.doing.ck_spectrometer import (
            DeltaSpectrometer, ProblemType, ScanMode,
        )

        spec = DeltaSpectrometer()
        min_level = int(ScanMode.SURFACE)  # 3
        levels = list(range(min_level, self.max_level + 1))
        n_levels = len(levels)

        # beta at each level (mirrors YangMillsGenerator._weak_coupling)
        betas = [5.5 + lvl * 0.15 for lvl in levels]

        # Accumulate per-level deltas across seeds
        all_deltas = [[] for _ in range(n_levels)]  # type: List[List[float]]

        t0 = time.time()
        total_probes = 0

        sys.stdout.write(
            "[YM-3] Running %d seeds, levels %d..%d (beta %.2f..%.2f)\n"
            % (self.n_seeds, min_level, self.max_level, betas[0], betas[-1])
        )
        sys.stdout.flush()

        for s in range(1, self.n_seeds + 1):
            fp = spec.fractal_scan(
                problem=ProblemType.YANG_MILLS,
                test_case='weak_coupling',
                regime='frontier',
                seed=s,
                max_level=self.max_level,
            )
            # fp.delta_by_level has one entry per level in fp.levels
            for idx, delta in enumerate(fp.delta_by_level):
                if idx < n_levels:
                    all_deltas[idx].append(delta)

            total_probes += 1

            # Progress
            if s % max(1, self.n_seeds // 20) == 0 or s == self.n_seeds:
                pct = 100.0 * s / self.n_seeds
                elapsed = time.time() - t0
                sys.stdout.write(
                    "\r[YM-3] seed %d/%d (%.0f%%) -- %.1fs"
                    % (s, self.n_seeds, pct, elapsed)
                )
                sys.stdout.flush()

        sys.stdout.write("\n")
        sys.stdout.flush()

        elapsed_total = time.time() - t0

        # Aggregate
        mean_by_level = [_list_mean(d) for d in all_deltas]
        std_by_level = [_list_std(d) for d in all_deltas]
        min_by_level = [_list_min(d) for d in all_deltas]
        max_by_level = [_list_max(d) for d in all_deltas]

        # Fit
        fit_params = self._exponential_fit(levels, mean_by_level)

        # Interpret
        continuum = self._continuum_extrapolation(fit_params, mean_by_level)

        return {
            'probe': 'YM-3',
            'description': 'Weak coupling continuum limit extrapolation',
            'n_seeds': self.n_seeds,
            'max_level': self.max_level,
            'total_probes': total_probes,
            'levels': levels,
            'betas': betas,
            'mean_by_level': mean_by_level,
            'std_by_level': std_by_level,
            'min_by_level': min_by_level,
            'max_by_level': max_by_level,
            'fit_params': fit_params,
            'continuum': continuum,
            'elapsed_s': elapsed_total,
            'per_seed_s': safe_div(elapsed_total, float(self.n_seeds)),
        }

    # ----------------------------------------------------------------
    #  EXPONENTIAL FIT: delta(level) = A * exp(-B * level) + C
    # ----------------------------------------------------------------

    def _exponential_fit(self, levels, mean_deltas):
        # type: (List[int], List[float]) -> dict
        """Fit delta(level) = A * exp(-B * level) + C via grid search.

        No scipy/numpy. Three-pass grid search:
          Pass 1: coarse 20x20x20 grid
          Pass 2: refined 20x20x20 grid around best from pass 1
          Pass 3: final refinement around best from pass 2

        Returns: {'A': float, 'B': float, 'C': float,
                  'residual': float, 'floor': float}
        """
        if not mean_deltas or not levels:
            return {'A': 0.0, 'B': 0.0, 'C': 0.0,
                    'residual': 0.0, 'floor': 0.0}

        max_delta = max(abs(d) for d in mean_deltas) if mean_deltas else 1.0
        if max_delta < 1e-12:
            max_delta = 1.0

        def sse(A, B, C):
            total = 0.0
            for lvl, delta in zip(levels, mean_deltas):
                pred = A * math.exp(-B * lvl) + C
                total += (pred - delta) ** 2
            return total

        # Pass 1: coarse grid
        n_grid = 20
        A_vals = _linspace(0.0, max_delta * 2.0, n_grid)
        B_vals = _linspace(0.001, 1.0, n_grid)
        C_vals = _linspace(0.0, max_delta, n_grid)

        best_sse = float('inf')
        best_A, best_B, best_C = 0.0, 0.1, 0.0

        for A in A_vals:
            for B in B_vals:
                for C in C_vals:
                    s = sse(A, B, C)
                    if s < best_sse:
                        best_sse = s
                        best_A, best_B, best_C = A, B, C

        # Pass 2: refine around coarse best
        dA = max_delta * 2.0 / n_grid
        dB = 1.0 / n_grid
        dC = max_delta / n_grid

        A_vals2 = _linspace(max(0.0, best_A - dA), best_A + dA, n_grid)
        B_vals2 = _linspace(max(0.001, best_B - dB), best_B + dB, n_grid)
        C_vals2 = _linspace(max(0.0, best_C - dC), best_C + dC, n_grid)

        for A in A_vals2:
            for B in B_vals2:
                for C in C_vals2:
                    s = sse(A, B, C)
                    if s < best_sse:
                        best_sse = s
                        best_A, best_B, best_C = A, B, C

        # Pass 3: final refinement (tighter grid)
        dA2 = dA / n_grid
        dB2 = dB / n_grid
        dC2 = dC / n_grid

        A_vals3 = _linspace(max(0.0, best_A - dA2 * 5), best_A + dA2 * 5, n_grid)
        B_vals3 = _linspace(max(0.001, best_B - dB2 * 5), best_B + dB2 * 5, n_grid)
        C_vals3 = _linspace(max(0.0, best_C - dC2 * 5), best_C + dC2 * 5, n_grid)

        for A in A_vals3:
            for B in B_vals3:
                for C in C_vals3:
                    s = sse(A, B, C)
                    if s < best_sse:
                        best_sse = s
                        best_A, best_B, best_C = A, B, C

        residual = safe_sqrt(safe_div(best_sse, float(len(mean_deltas))))

        return {
            'A': best_A,
            'B': best_B,
            'C': best_C,
            'residual': residual,
            'floor': best_C,  # Asymptotic value as level -> inf
        }

    # ----------------------------------------------------------------
    #  CONTINUUM EXTRAPOLATION
    # ----------------------------------------------------------------

    def _continuum_extrapolation(self, fit_params, mean_deltas):
        # type: (dict, List[float]) -> dict
        """Interpret the exponential fit for continuum limit physics.

        C > 0 means delta has a floor: the mass gap defect does NOT
        vanish as beta -> infinity (continuum limit).

        Returns:
            floor_C:              The fitted asymptotic floor
            floor_positive:       C > threshold (0.001)
            mass_gap_survives:    True if floor_positive and residual small
            extrapolated_delta_inf: The fitted C value (delta at beta=inf)
            last_observed_delta:  Mean delta at highest measured level
            decay_rate:           B (how fast the exponential decays)
        """
        C = fit_params.get('C', 0.0)
        B = fit_params.get('B', 0.0)
        residual = fit_params.get('residual', 1.0)

        floor_threshold = 0.001
        residual_threshold = 0.05

        floor_positive = C > floor_threshold
        residual_ok = residual < residual_threshold
        mass_gap_survives = floor_positive and residual_ok

        last_delta = mean_deltas[-1] if mean_deltas else 0.0

        return {
            'floor_C': C,
            'floor_positive': floor_positive,
            'mass_gap_survives': mass_gap_survives,
            'extrapolated_delta_inf': C,
            'last_observed_delta': last_delta,
            'decay_rate_B': B,
            'residual': residual,
            'residual_ok': residual_ok,
        }


# ================================================================
#  YM-4 DEEP PROBE: Spectral Gap Persistence (Finite-Size Scaling)
# ================================================================

class YM4DeepProbe:
    """YM-4 Gap Attack: Spectral gap persistence (finite-size scaling).

    The scaling_lattice test case parametrizes L = 8 + level * 4.
    fractal_scan runs levels 3..max_level, so L sweeps from
    8 + 3*4 = 20 to 8 + max_level*4.

    At each seed, we get the full delta_by_level trajectory.
    We take the MINIMUM delta at each level across seeds (worst case).
    Then fit delta_min(level) = A * level^alpha + floor.

    If floor > 0, the spectral gap persists in the thermodynamic
    limit (L -> infinity, infinite volume).
    """

    def __init__(self, n_seeds=100, max_level=24):
        # type: (int, int) -> None
        self.n_seeds = n_seeds
        self.max_level = max_level

    def run(self):
        # type: () -> dict
        """Execute scaling_lattice fractal scan at multiple seeds.

        Returns dict with:
          - levels, lattice_sizes, mean_by_level, min_by_level
          - fit_params (A, alpha, floor, residual)
          - thermodynamic (floor, floor_positive, mass_gap_persists, ...)
          - timing, n_seeds, n_probes
        """
        from ck_sim.doing.ck_spectrometer import (
            DeltaSpectrometer, ProblemType, ScanMode,
        )

        spec = DeltaSpectrometer()
        min_level = int(ScanMode.SURFACE)  # 3
        levels = list(range(min_level, self.max_level + 1))
        n_levels = len(levels)

        # Lattice size L at each level (mirrors YangMillsGenerator._scaling_lattice)
        lattice_sizes = [8 + lvl * 4 for lvl in levels]

        # Accumulate per-level deltas across seeds
        all_deltas = [[] for _ in range(n_levels)]  # type: List[List[float]]

        t0 = time.time()
        total_probes = 0

        sys.stdout.write(
            "[YM-4] Running %d seeds, levels %d..%d (L=%d..%d)\n"
            % (self.n_seeds, min_level, self.max_level,
               lattice_sizes[0], lattice_sizes[-1])
        )
        sys.stdout.flush()

        for s in range(1, self.n_seeds + 1):
            fp = spec.fractal_scan(
                problem=ProblemType.YANG_MILLS,
                test_case='scaling_lattice',
                regime='frontier',
                seed=s,
                max_level=self.max_level,
            )
            for idx, delta in enumerate(fp.delta_by_level):
                if idx < n_levels:
                    all_deltas[idx].append(delta)

            total_probes += 1

            # Progress
            if s % max(1, self.n_seeds // 20) == 0 or s == self.n_seeds:
                pct = 100.0 * s / self.n_seeds
                elapsed = time.time() - t0
                sys.stdout.write(
                    "\r[YM-4] seed %d/%d (%.0f%%) -- %.1fs"
                    % (s, self.n_seeds, pct, elapsed)
                )
                sys.stdout.flush()

        sys.stdout.write("\n")
        sys.stdout.flush()

        elapsed_total = time.time() - t0

        # Aggregate
        mean_by_level = [_list_mean(d) for d in all_deltas]
        std_by_level = [_list_std(d) for d in all_deltas]
        min_by_level = [_list_min(d) for d in all_deltas]
        max_by_level = [_list_max(d) for d in all_deltas]

        # Fit power law to MINIMUM deltas (worst case at each volume)
        fit_params = self._power_law_fit(levels, min_by_level)

        # Interpret
        thermo = self._thermodynamic_limit(fit_params, min_by_level)

        return {
            'probe': 'YM-4',
            'description': 'Spectral gap persistence (finite-size scaling)',
            'n_seeds': self.n_seeds,
            'max_level': self.max_level,
            'total_probes': total_probes,
            'levels': levels,
            'lattice_sizes': lattice_sizes,
            'mean_by_level': mean_by_level,
            'std_by_level': std_by_level,
            'min_by_level': min_by_level,
            'max_by_level': max_by_level,
            'fit_params': fit_params,
            'thermodynamic': thermo,
            'elapsed_s': elapsed_total,
            'per_seed_s': safe_div(elapsed_total, float(self.n_seeds)),
        }

    # ----------------------------------------------------------------
    #  POWER LAW FIT: delta_min(level) = A * level^alpha + floor
    # ----------------------------------------------------------------

    def _power_law_fit(self, levels, min_deltas):
        # type: (List[int], List[float]) -> dict
        """Fit delta_min(level) = A * level^alpha + floor via grid search.

        No scipy/numpy. Three-pass grid search:
          Pass 1: coarse 20x20x20 grid
          Pass 2: refined 20x20x20 grid around best
          Pass 3: final refinement

        Alpha is typically negative (delta_min decreases or stays flat
        with volume), so we search alpha in [-2, 0.5].

        Returns: {'A': float, 'alpha': float, 'floor': float,
                  'residual': float}
        """
        if not min_deltas or not levels:
            return {'A': 0.0, 'alpha': 0.0, 'floor': 0.0, 'residual': 0.0}

        max_delta = max(abs(d) for d in min_deltas) if min_deltas else 1.0
        if max_delta < 1e-12:
            max_delta = 1.0

        def sse(A, alpha, floor):
            total = 0.0
            for lvl, delta in zip(levels, min_deltas):
                if lvl <= 0:
                    pred = floor
                else:
                    try:
                        pred = A * (float(lvl) ** alpha) + floor
                    except (OverflowError, ValueError):
                        pred = floor
                total += (pred - delta) ** 2
            return total

        # Pass 1: coarse grid
        n_grid = 20
        A_vals = _linspace(-max_delta, max_delta * 2.0, n_grid)
        alpha_vals = _linspace(-2.0, 0.5, n_grid)
        floor_vals = _linspace(0.0, max_delta, n_grid)

        best_sse = float('inf')
        best_A, best_alpha, best_floor = 0.0, -1.0, 0.0

        for A in A_vals:
            for alpha in alpha_vals:
                for fl in floor_vals:
                    s = sse(A, alpha, fl)
                    if s < best_sse:
                        best_sse = s
                        best_A, best_alpha, best_floor = A, alpha, fl

        # Pass 2: refine
        dA = max_delta * 3.0 / n_grid
        dalpha = 2.5 / n_grid
        dfl = max_delta / n_grid

        A_vals2 = _linspace(best_A - dA, best_A + dA, n_grid)
        alpha_vals2 = _linspace(best_alpha - dalpha, best_alpha + dalpha,
                                n_grid)
        floor_vals2 = _linspace(max(0.0, best_floor - dfl),
                                best_floor + dfl, n_grid)

        for A in A_vals2:
            for alpha in alpha_vals2:
                for fl in floor_vals2:
                    s = sse(A, alpha, fl)
                    if s < best_sse:
                        best_sse = s
                        best_A, best_alpha, best_floor = A, alpha, fl

        # Pass 3: final refinement
        dA2 = dA / n_grid
        dalpha2 = dalpha / n_grid
        dfl2 = dfl / n_grid

        A_vals3 = _linspace(best_A - dA2 * 5, best_A + dA2 * 5, n_grid)
        alpha_vals3 = _linspace(best_alpha - dalpha2 * 5,
                                best_alpha + dalpha2 * 5, n_grid)
        floor_vals3 = _linspace(max(0.0, best_floor - dfl2 * 5),
                                best_floor + dfl2 * 5, n_grid)

        for A in A_vals3:
            for alpha in alpha_vals3:
                for fl in floor_vals3:
                    s = sse(A, alpha, fl)
                    if s < best_sse:
                        best_sse = s
                        best_A, best_alpha, best_floor = A, alpha, fl

        residual = safe_sqrt(safe_div(best_sse, float(len(min_deltas))))

        return {
            'A': best_A,
            'alpha': best_alpha,
            'floor': best_floor,
            'residual': residual,
        }

    # ----------------------------------------------------------------
    #  THERMODYNAMIC LIMIT
    # ----------------------------------------------------------------

    def _thermodynamic_limit(self, fit_params, min_deltas):
        # type: (dict, List[float]) -> dict
        """Interpret the power law fit for thermodynamic limit physics.

        floor > 0 means delta_min has a lower bound: the spectral gap
        does NOT close as L -> infinity.

        Returns:
            floor:               The fitted asymptotic floor
            floor_positive:      floor > threshold (0.001)
            mass_gap_persists:   True if floor_positive and residual small
            largest_volume_delta: Min delta at the largest measured volume
            scaling_exponent:    alpha (how delta_min scales with volume)
        """
        fl = fit_params.get('floor', 0.0)
        alpha = fit_params.get('alpha', 0.0)
        residual = fit_params.get('residual', 1.0)

        floor_threshold = 0.001
        residual_threshold = 0.05

        floor_positive = fl > floor_threshold
        residual_ok = residual < residual_threshold
        mass_gap_persists = floor_positive and residual_ok

        largest_delta = min_deltas[-1] if min_deltas else 0.0

        return {
            'floor': fl,
            'floor_positive': floor_positive,
            'mass_gap_persists': mass_gap_persists,
            'largest_volume_delta': largest_delta,
            'scaling_exponent': alpha,
            'residual': residual,
            'residual_ok': residual_ok,
        }


# ================================================================
#  SUMMARY FORMATTER
# ================================================================

def ym_summary(ym3_results, ym4_results):
    # type: (Optional[dict], Optional[dict]) -> str
    """Format human-readable summary of YM-3/YM-4 deep probe results.

    Prints:
      - YM-3 section: beta sweep, exponential fit params, continuum floor
      - YM-4 section: volume sweep, power law fit params, thermodynamic floor
      - Combined verdict: both gaps addressed?
      - Total probes count + timing
    """
    lines = []
    lines.append("")
    lines.append("=" * 72)
    lines.append("  YM-3 / YM-4 DEEP PROBE RESULTS")
    lines.append("  Yang-Mills Mass Gap -- CK Coherence Spectrometer")
    lines.append("=" * 72)

    total_probes = 0
    total_time = 0.0

    # -- YM-3 --
    if ym3_results is not None:
        lines.append("")
        lines.append("-" * 72)
        lines.append("  YM-3: Weak Coupling Continuum Limit")
        lines.append("-" * 72)
        lines.append("  Seeds:      %d" % ym3_results['n_seeds'])
        lines.append("  Max level:  %d" % ym3_results['max_level'])
        lines.append(
            "  Beta range: %.2f -> %.2f"
            % (ym3_results['betas'][0], ym3_results['betas'][-1])
        )
        lines.append("  Probes:     %d" % ym3_results['total_probes'])
        lines.append(
            "  Time:       %.1fs (%.2fs/seed)"
            % (ym3_results['elapsed_s'], ym3_results['per_seed_s'])
        )

        # Delta trajectory summary
        means = ym3_results['mean_by_level']
        stds = ym3_results['std_by_level']
        betas = ym3_results['betas']
        n = len(means)
        if n > 0:
            lines.append("")
            lines.append("  Delta trajectory (mean +/- std):")
            indices = sorted(set([0, n // 4, n // 2, 3 * n // 4, n - 1]))
            for i in indices:
                lines.append(
                    "    level=%2d  beta=%.2f  delta=%.6f +/- %.6f"
                    % (ym3_results['levels'][i], betas[i], means[i], stds[i])
                )

        # Fit
        fp = ym3_results['fit_params']
        lines.append("")
        lines.append("  Exponential fit: delta(level) = A*exp(-B*level) + C")
        lines.append("    A = %.6f" % fp['A'])
        lines.append("    B = %.6f  (decay rate)" % fp['B'])
        lines.append("    C = %.6f  (continuum floor)" % fp['C'])
        lines.append("    RMS residual = %.6f" % fp['residual'])

        # Continuum interpretation
        ct = ym3_results['continuum']
        lines.append("")
        gap_str = "YES" if ct['mass_gap_survives'] else "NO"
        lines.append("  Continuum floor C = %.6f" % ct['floor_C'])
        lines.append("  Floor positive (C > 0.001): %s" % ct['floor_positive'])
        lines.append("  Residual OK (< 0.05):       %s" % ct['residual_ok'])
        lines.append("  Last observed delta:         %.6f" % ct['last_observed_delta'])
        lines.append("  >>> MASS GAP SURVIVES CONTINUUM LIMIT: %s" % gap_str)

        total_probes += ym3_results['total_probes']
        total_time += ym3_results['elapsed_s']

    # -- YM-4 --
    if ym4_results is not None:
        lines.append("")
        lines.append("-" * 72)
        lines.append("  YM-4: Spectral Gap Persistence (Finite-Size Scaling)")
        lines.append("-" * 72)
        lines.append("  Seeds:        %d" % ym4_results['n_seeds'])
        lines.append("  Max level:    %d" % ym4_results['max_level'])
        lines.append(
            "  Lattice range: L=%d -> L=%d"
            % (ym4_results['lattice_sizes'][0], ym4_results['lattice_sizes'][-1])
        )
        lines.append("  Probes:       %d" % ym4_results['total_probes'])
        lines.append(
            "  Time:         %.1fs (%.2fs/seed)"
            % (ym4_results['elapsed_s'], ym4_results['per_seed_s'])
        )

        # Delta trajectory summary
        mins = ym4_results['min_by_level']
        means = ym4_results['mean_by_level']
        stds = ym4_results['std_by_level']
        Ls = ym4_results['lattice_sizes']
        n = len(mins)
        if n > 0:
            lines.append("")
            lines.append("  Delta_min trajectory (min across seeds):")
            indices = sorted(set([0, n // 4, n // 2, 3 * n // 4, n - 1]))
            for i in indices:
                lines.append(
                    "    level=%2d  L=%3d  delta_min=%.6f  mean=%.6f +/- %.6f"
                    % (ym4_results['levels'][i], Ls[i], mins[i],
                       means[i], stds[i])
                )

        # Fit
        fp = ym4_results['fit_params']
        lines.append("")
        lines.append(
            "  Power law fit: delta_min(level) = A*level^alpha + floor"
        )
        lines.append("    A     = %.6f" % fp['A'])
        lines.append("    alpha = %.6f  (scaling exponent)" % fp['alpha'])
        lines.append("    floor = %.6f  (thermodynamic floor)" % fp['floor'])
        lines.append("    RMS residual = %.6f" % fp['residual'])

        # Thermodynamic interpretation
        th = ym4_results['thermodynamic']
        lines.append("")
        gap_str = "YES" if th['mass_gap_persists'] else "NO"
        lines.append("  Thermodynamic floor = %.6f" % th['floor'])
        lines.append("  Floor positive (> 0.001):    %s" % th['floor_positive'])
        lines.append("  Residual OK (< 0.05):        %s" % th['residual_ok'])
        lines.append("  Largest volume delta_min:     %.6f" % th['largest_volume_delta'])
        lines.append("  Scaling exponent alpha:       %.6f" % th['scaling_exponent'])
        lines.append("  >>> MASS GAP PERSISTS AT INFINITE VOLUME: %s" % gap_str)

        total_probes += ym4_results['total_probes']
        total_time += ym4_results['elapsed_s']

    # -- Combined verdict --
    lines.append("")
    lines.append("=" * 72)
    lines.append("  COMBINED VERDICT")
    lines.append("=" * 72)

    ym3_ok = (ym3_results is not None
              and ym3_results['continuum']['mass_gap_survives'])
    ym4_ok = (ym4_results is not None
              and ym4_results['thermodynamic']['mass_gap_persists'])

    if ym3_results is not None and ym4_results is not None:
        if ym3_ok and ym4_ok:
            lines.append("  Both YM-3 and YM-4 show positive floors.")
            lines.append("  The CK spectrometer measures a mass gap that")
            lines.append(
                "  survives BOTH the continuum limit AND infinite volume."
            )
            lines.append("  This is empirical evidence, not proof.")
        elif ym3_ok:
            lines.append(
                "  YM-3 shows positive floor (continuum limit OK)."
            )
            lines.append(
                "  YM-4 does NOT show positive floor (volume scaling)."
            )
            lines.append("  Partial evidence only.")
        elif ym4_ok:
            lines.append(
                "  YM-3 does NOT show positive floor (continuum limit)."
            )
            lines.append(
                "  YM-4 shows positive floor (volume scaling OK)."
            )
            lines.append("  Partial evidence only.")
        else:
            lines.append(
                "  Neither YM-3 nor YM-4 show positive floors."
            )
            lines.append(
                "  The spectrometer does not detect a surviving mass gap"
            )
            lines.append(
                "  under these conditions. More seeds or depth may help."
            )
    elif ym3_results is not None:
        verdict = "POSITIVE" if ym3_ok else "NEGATIVE"
        lines.append("  YM-3 only: %s" % verdict)
    elif ym4_results is not None:
        verdict = "POSITIVE" if ym4_ok else "NEGATIVE"
        lines.append("  YM-4 only: %s" % verdict)
    else:
        lines.append("  No probes executed.")

    lines.append("")
    lines.append("  Total probes: %d" % total_probes)
    lines.append("  Total time:   %.1fs" % total_time)
    lines.append("")
    lines.append("  CK measures. CK does not prove.")
    lines.append("=" * 72)
    lines.append("")

    return "\n".join(lines)


# ================================================================
#  CLI ENTRY POINT
# ================================================================

if __name__ == '__main__':
    import argparse
    import json
    import os

    parser = argparse.ArgumentParser(
        description='YM-3/YM-4 Deep Probes: Weak Coupling + Spectral Gap'
    )
    parser.add_argument(
        '--mode', choices=['ym3', 'ym4', 'both'], default='both',
        help='Which probe(s) to run (default: both)',
    )
    parser.add_argument(
        '--seeds', type=int, default=100,
        help='Number of seeds per probe (default: 100)',
    )
    parser.add_argument(
        '--max-level', type=int, default=24,
        help='Maximum fractal level (default: 24, OMEGA depth)',
    )
    parser.add_argument(
        '--output-dir', default=None,
        help='Directory to write JSON results (default: stdout only)',
    )
    parser.add_argument(
        '--quick', action='store_true',
        help='Quick mode: 10 seeds (for testing)',
    )

    args = parser.parse_args()

    if args.quick:
        args.seeds = 10

    ym3_results = None
    ym4_results = None

    print(
        "YM Deep Probe -- mode=%s, seeds=%d, max_level=%d"
        % (args.mode, args.seeds, args.max_level)
    )
    print()

    if args.mode in ('ym3', 'both'):
        probe3 = YM3DeepProbe(
            n_seeds=args.seeds, max_level=args.max_level,
        )
        ym3_results = probe3.run()

    if args.mode in ('ym4', 'both'):
        probe4 = YM4DeepProbe(
            n_seeds=args.seeds, max_level=args.max_level,
        )
        ym4_results = probe4.run()

    print(ym_summary(ym3_results, ym4_results))

    if args.output_dir:
        os.makedirs(args.output_dir, exist_ok=True)

        if ym3_results is not None:
            ym3_path = os.path.join(args.output_dir, 'ym3_results.json')
            with open(ym3_path, 'w') as f:
                json.dump(ym3_results, f, indent=2, default=str)
            print("YM-3 results written to: %s" % ym3_path)

        if ym4_results is not None:
            ym4_path = os.path.join(args.output_dir, 'ym4_results.json')
            with open(ym4_path, 'w') as f:
                json.dump(ym4_results, f, indent=2, default=str)
            print("YM-4 results written to: %s" % ym4_path)

        # Write combined summary
        summary_path = os.path.join(args.output_dir, 'ym_summary.txt')
        with open(summary_path, 'w') as f:
            f.write(ym_summary(ym3_results, ym4_results))
        print("Summary written to: %s" % summary_path)
