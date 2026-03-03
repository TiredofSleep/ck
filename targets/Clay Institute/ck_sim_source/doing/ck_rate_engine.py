"""
ck_rate_engine.py -- Sanders Axiom of Recursive Topological Emergence (RATE)
=============================================================================
Operator: FRUIT (8) -- Topology emerges from recursive information.

Implements the R_inf operator:
  Let S_0 be a finite information-bearing structure.
  Let R = information-of-information operator.
  Define: S_0, S_1 = R(S_0), S_2 = R(S_1), ...

  RATE axiom: The limit R_inf(S_0) = lim_{n->inf} R^n(S_0)
  is a topological space whose structure is determined entirely
  by the fixed points and stable manifolds of R.

In the spectrometer: R_inf maps to fractal depth iteration.
  - At depth d, compute delta(d)
  - Feed delta(d) as sensitivity parameter for depth d+1
  - Track convergence of the delta sequence
  - Fixed points = where delta stabilizes
  - Convergence = topology has emerged
  - Divergence = topology absent

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import math
from typing import Dict, List, Optional, Tuple

from ck_sim.being.ck_sdv_safety import clamp, safe_div, safe_sqrt


# ================================================================
#  RATE DATA STRUCTURES
# ================================================================

class RATEStep:
    """Single step of the R_inf iteration."""
    __slots__ = ('depth', 'delta', 'delta_change', 'sensitivity')

    def __init__(self, depth: int, delta: float, delta_change: float,
                 sensitivity: float):
        self.depth = depth
        self.delta = delta
        self.delta_change = delta_change
        self.sensitivity = sensitivity


class RATETrace:
    """Full R_inf iteration trace for one problem."""
    __slots__ = ('problem_id', 'seed', 'steps', 'converged',
                 'fixed_point_delta', 'convergence_depth',
                 'topology_emerged', 'rate_defect')

    def __init__(self, problem_id: str, seed: int, steps: list,
                 converged: bool, fixed_point_delta: float,
                 convergence_depth: int, topology_emerged: bool,
                 rate_defect: float):
        self.problem_id = problem_id
        self.seed = seed
        self.steps = steps
        self.converged = converged
        self.fixed_point_delta = fixed_point_delta
        self.convergence_depth = convergence_depth
        self.topology_emerged = topology_emerged
        self.rate_defect = rate_defect


class RATEFixedPoint:
    """Fixed point analysis across seeds."""
    __slots__ = ('problem_id', 'mean_fixed_delta', 'std_fixed_delta',
                 'stability', 'convergence_rate', 'seeds_converged',
                 'seeds_total')

    def __init__(self, problem_id: str, mean_fixed_delta: float,
                 std_fixed_delta: float, stability: str,
                 convergence_rate: float, seeds_converged: int,
                 seeds_total: int):
        self.problem_id = problem_id
        self.mean_fixed_delta = mean_fixed_delta
        self.std_fixed_delta = std_fixed_delta
        self.stability = stability
        self.convergence_rate = convergence_rate
        self.seeds_converged = seeds_converged
        self.seeds_total = seeds_total


# ================================================================
#  RATE ENGINE
# ================================================================

class RATEEngine:
    """Sanders Axiom of Recursive Topological Emergence.

    The R_inf operator iterates information-of-information:
      Step 1: Measure delta at fractal depth d
      Step 2: Use delta(d) to modulate sensitivity at depth d+1
      Step 3: Measure delta at depth d+1
      Step 4: Track convergence of delta sequence

    Piggybacks on the spectrometer's existing fractal depth levels (3-24).
    """

    # Convergence criteria
    CONVERGENCE_THRESHOLD = 0.005  # Delta change below this = converged
    CONVERGENCE_WINDOW = 3         # Must be stable for this many consecutive steps
    MAX_DEPTH = 24                  # Maximum fractal depth

    # Depth levels matching the spectrometer's fractal scan
    DEPTH_LEVELS = [3, 6, 9, 12, 15, 18, 21, 24]

    def __init__(self, spectrometer):
        self.spec = spectrometer

    # Map depth levels to ScanMode enums for true depth granularity
    _DEPTH_TO_MODE = {3: 'SURFACE', 6: 'SHALLOW', 9: 'MEDIUM',
                      12: 'DEEP', 15: 'EXTENDED', 18: 'THOROUGH',
                      21: 'INTENSIVE', 24: 'OMEGA'}

    def r_step(self, problem_id: str, prev_delta: float,
               depth: int, seed: int, test_case: str) -> RATEStep:
        """Single step of R_inf: compute information-of-information.

        Real feedback loop:
        1. Previous delta modulates the seed (delta-dependent exploration)
        2. Each depth uses its own ScanMode (true depth granularity)
        3. Sensitivity scales the final measurement (meta-weighting)

        This makes each step genuinely dependent on the previous
        measurement -- the "information-of-information" operator.
        """
        from ck_sim.doing.ck_spectrometer import ProblemType, SpectrometerInput, ScanMode

        # Sensitivity: previous delta affects weight of this step
        sensitivity = clamp(0.5 + prev_delta * 0.5, 0.1, 1.0)

        # Delta-modulated seed: previous measurement changes exploration path
        # Quantize prev_delta to 1000 bins for deterministic integer seed
        delta_hash = int(prev_delta * 1000) % 997  # prime modulus
        modulated_seed = seed + delta_hash * (depth + 1)

        # Use exact ScanMode for this depth level
        mode_name = self._DEPTH_TO_MODE.get(depth, 'DEEP')
        scan_mode = ScanMode[mode_name]

        inp = SpectrometerInput(
            problem=ProblemType(problem_id),
            test_case=test_case,
            scan_mode=scan_mode,
            seed=modulated_seed,
        )
        result = self.spec.scan(inp)

        # Extract delta -- real value flowing through
        delta = result.delta_value * sensitivity

        delta_change = abs(delta - prev_delta)

        return RATEStep(
            depth=depth,
            delta=delta,
            delta_change=delta_change,
            sensitivity=sensitivity,
        )

    def r_iterate(self, problem_id: str, seed: int,
                  test_case: str = 'default',
                  max_depth: int = None) -> RATETrace:
        """Iterate R until convergence or max_depth.

        Returns a full trace of the R_inf iteration.
        """
        if max_depth is None:
            max_depth = self.MAX_DEPTH

        steps = []
        prev_delta = 0.5  # Initial delta (no prior information)
        converged = False
        convergence_depth = max_depth
        stable_count = 0

        for depth in self.DEPTH_LEVELS:
            if depth > max_depth:
                break

            step = self.r_step(problem_id, prev_delta, depth, seed, test_case)
            steps.append(step)

            # Check convergence
            if step.delta_change < self.CONVERGENCE_THRESHOLD:
                stable_count += 1
                if stable_count >= self.CONVERGENCE_WINDOW:
                    converged = True
                    convergence_depth = depth
                    break
            else:
                stable_count = 0

            prev_delta = step.delta

        # Fixed point delta = final stable value
        fixed_point_delta = steps[-1].delta if steps else 0.0

        # RATE defect = how much the sequence is still changing at termination
        rate_defect = steps[-1].delta_change if steps else 0.0

        # Topology emerged if converged to a stable manifold
        topology_emerged = converged

        return RATETrace(
            problem_id=problem_id,
            seed=seed,
            steps=steps,
            converged=converged,
            fixed_point_delta=fixed_point_delta,
            convergence_depth=convergence_depth,
            topology_emerged=topology_emerged,
            rate_defect=rate_defect,
        )

    def find_fixed_points(self, problem_id: str, seeds: List[int],
                          test_case: str = 'default') -> RATEFixedPoint:
        """Find R_inf fixed points across seeds.

        Runs r_iterate for each seed and analyzes the fixed point
        distribution.
        """
        traces = []
        for seed in seeds:
            trace = self.r_iterate(problem_id, seed, test_case)
            traces.append(trace)

        # Extract fixed point deltas from converged traces
        fixed_deltas = [t.fixed_point_delta for t in traces if t.converged]
        all_deltas = [t.fixed_point_delta for t in traces]

        if not all_deltas:
            return RATEFixedPoint(problem_id, 0.0, 0.0, 'unknown', 0.0, 0, 0)

        mean_fd = sum(all_deltas) / len(all_deltas)
        var_fd = sum((d - mean_fd) ** 2 for d in all_deltas) / len(all_deltas)
        std_fd = safe_sqrt(var_fd)

        seeds_converged = sum(1 for t in traces if t.converged)
        convergence_rate = safe_div(seeds_converged, len(seeds))

        # Stability classification
        if convergence_rate >= 0.9 and std_fd < 0.01:
            stability = 'frozen'      # Fixed point is stable across all seeds
        elif convergence_rate >= 0.7 and std_fd < 0.05:
            stability = 'stable'      # Fixed point exists with small variance
        elif convergence_rate >= 0.5:
            stability = 'bounded'     # Converges sometimes, moderate variance
        elif convergence_rate > 0.0:
            stability = 'oscillating'  # Rarely converges
        else:
            stability = 'wild'         # Never converges -- no fixed point

        return RATEFixedPoint(
            problem_id=problem_id,
            mean_fixed_delta=mean_fd,
            std_fixed_delta=std_fd,
            stability=stability,
            convergence_rate=convergence_rate,
            seeds_converged=seeds_converged,
            seeds_total=len(seeds),
        )

    def rate_defect_from_trace(self, trace: RATETrace) -> float:
        """RATE-defect: ||R^n(S) - R^{n-1}(S)|| at final iteration.

        Convergence (rate_defect -> 0) = topology emerged.
        Divergence (rate_defect large) = topology absent.
        """
        return trace.rate_defect

    def rate_atlas(self, problem_ids: List[str], seeds: List[int],
                   test_cases: Optional[Dict[str, str]] = None
                   ) -> Dict[str, RATEFixedPoint]:
        """Full RATE analysis across all problems.

        Returns fixed point analysis for each problem.
        """
        if test_cases is None:
            test_cases = {}

        results = {}
        for pid in problem_ids:
            tc = test_cases.get(pid, 'default')
            results[pid] = self.find_fixed_points(pid, seeds, tc)
        return results

    def trace_to_dict(self, trace: RATETrace) -> dict:
        """Serialize a RATE trace for JSON output."""
        return {
            'problem_id': trace.problem_id,
            'seed': trace.seed,
            'converged': trace.converged,
            'fixed_point_delta': trace.fixed_point_delta,
            'convergence_depth': trace.convergence_depth,
            'topology_emerged': trace.topology_emerged,
            'rate_defect': trace.rate_defect,
            'steps': [
                {
                    'depth': s.depth,
                    'delta': s.delta,
                    'delta_change': s.delta_change,
                    'sensitivity': s.sensitivity,
                }
                for s in trace.steps
            ],
        }

    def fixed_point_to_dict(self, fp: RATEFixedPoint) -> dict:
        """Serialize a RATE fixed point for JSON output."""
        return {
            'problem_id': fp.problem_id,
            'mean_fixed_delta': fp.mean_fixed_delta,
            'std_fixed_delta': fp.std_fixed_delta,
            'stability': fp.stability,
            'convergence_rate': fp.convergence_rate,
            'seeds_converged': fp.seeds_converged,
            'seeds_total': fp.seeds_total,
        }
