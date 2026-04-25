"""
ck_calibration.py — Empirical threshold calibration for DOFProfileMonitor

The base monitor uses arbitrary thresholds (0.7 for diffuseness and
concentration). This module provides a calibration utility that derives
thresholds from a baseline distribution provided by the caller.

WHAT THE CALLER MUST PROVIDE:

    A representative sample of "honest" 10×10 matrices for the workload.
    What "honest" means depends on the deployment context:

      • For activation monitoring during inference: collect activations
        from a corpus of trusted, non-drifting inferences.
      • For training diagnostics: collect activations from a converged
        baseline checkpoint operating on validation data.
      • For static analysis: use a reference set of structured TIG
        operators known to be in the desired regime.

    We do NOT pick a baseline for you. A wrong baseline produces wrong
    thresholds. This is the most important hygiene rule in this module.

WHAT THIS MODULE DOES:

    1. Runs profile() on each baseline matrix.
    2. Records the empirical distribution of:
         • diffuseness scores
         • concentration scores
         • orthogonal_profile shares per DOF
    3. Returns suggested thresholds at user-specified percentiles, plus
       per-DOF distribution statistics for diagnostic display.

WHAT THIS MODULE DOES NOT DO:

    • Generate baseline data. (Caller's job — domain-specific.)
    • Decide what "drift" means. (Threshold is a policy choice.)
    • Re-tune the monitor's internal projection bases. (Those are
      verified canonical math; they don't depend on calibration data.)

USAGE:

    from ck_dof_profile_monitor import DOFProfileMonitor
    from ck_calibration import calibrate_thresholds

    baseline_matrices = collect_baseline_activations(n=1000)  # caller's job
    monitor = DOFProfileMonitor()
    cal = calibrate_thresholds(monitor, baseline_matrices)

    # Apply suggested thresholds
    monitor.diffuse_threshold = cal.suggested_diffuse_threshold
    monitor.concentrated_threshold = cal.suggested_concentrated_threshold

    # Or inspect the full distribution
    print(cal.report())
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Sequence
import numpy as np

from ck_dof_profile_monitor import DOFProfileMonitor, DOFProfile


@dataclass
class CalibrationReport:
    """Result of calibrating a DOFProfileMonitor against a baseline sample."""

    n_samples: int
    """Number of baseline matrices processed."""

    diffuseness_distribution: List[float]
    """Sorted diffuseness scores across the baseline."""

    concentration_distribution: List[float]
    """Sorted concentration scores across the baseline."""

    per_dof_share_distribution: Dict[str, List[float]]
    """For each orthogonal-partition DOF, the sorted distribution of
    share values across the baseline."""

    suggested_diffuse_threshold: float
    """Suggested threshold for is_diffuse: at the requested percentile of
    the baseline diffuseness distribution. Inferences with diffuseness
    above this threshold are 'unusually diffuse' relative to baseline."""

    suggested_concentrated_threshold: float
    """Suggested threshold for is_concentrated: at the requested
    percentile of baseline concentration. Inferences below this are
    'unusually unconcentrated' relative to baseline."""

    diffuse_percentile: float
    """The percentile used (e.g., 95.0 for 95th percentile)."""

    concentrated_percentile: float
    """The percentile used for concentration (lower tail, e.g., 5th
    percentile = "drift if less concentrated than 95% of baseline")."""

    notes: List[str] = field(default_factory=list)

    def report(self, max_lines: int = 40) -> str:
        """Human-readable summary."""
        lines = []
        lines.append(f"Calibration report ({self.n_samples} samples)")
        lines.append("=" * 60)
        lines.append("")
        lines.append("Diffuseness distribution:")
        lines.append(f"  min:    {self.diffuseness_distribution[0]:.4f}")
        lines.append(f"  median: {_median(self.diffuseness_distribution):.4f}")
        lines.append(f"  p75:    {_percentile(self.diffuseness_distribution, 75):.4f}")
        lines.append(f"  p95:    {_percentile(self.diffuseness_distribution, 95):.4f}")
        lines.append(f"  p99:    {_percentile(self.diffuseness_distribution, 99):.4f}")
        lines.append(f"  max:    {self.diffuseness_distribution[-1]:.4f}")
        lines.append("")
        lines.append("Concentration distribution:")
        lines.append(f"  min:    {self.concentration_distribution[0]:.4f}")
        lines.append(f"  p1:     {_percentile(self.concentration_distribution, 1):.4f}")
        lines.append(f"  p5:     {_percentile(self.concentration_distribution, 5):.4f}")
        lines.append(f"  median: {_median(self.concentration_distribution):.4f}")
        lines.append(f"  max:    {self.concentration_distribution[-1]:.4f}")
        lines.append("")
        lines.append("Suggested thresholds:")
        lines.append(f"  diffuse_threshold        = {self.suggested_diffuse_threshold:.4f}  "
                     f"(at p{self.diffuse_percentile:g} of diffuseness)")
        lines.append(f"  concentrated_threshold   = {self.suggested_concentrated_threshold:.4f}  "
                     f"(at p{self.concentrated_percentile:g} of concentration)")
        lines.append("")
        lines.append("Per-DOF share statistics (orthogonal partition):")
        for dof, dist in self.per_dof_share_distribution.items():
            mean = sum(dist) / len(dist)
            lines.append(f"  {dof:25s}: mean={mean:.3f}, "
                         f"p50={_percentile(dist, 50):.3f}, "
                         f"p95={_percentile(dist, 95):.3f}")
        if self.notes:
            lines.append("")
            lines.append("Notes:")
            for note in self.notes:
                lines.append(f"  - {note}")
        return "\n".join(lines)


def calibrate_thresholds(
    monitor: DOFProfileMonitor,
    baseline_matrices: Sequence[np.ndarray],
    *,
    diffuse_percentile: float = 95.0,
    concentrated_percentile: float = 5.0,
) -> CalibrationReport:
    """Calibrate diffuse/concentrated thresholds from baseline matrices.

    Args:
        monitor: A DOFProfileMonitor instance. Its bases are used; thresholds
            on the monitor itself are NOT modified by this function. The caller
            decides whether to apply the suggested thresholds.
        baseline_matrices: A sequence of 10×10 numpy matrices representing
            "honest" / non-drifting / in-distribution behavior. Caller's
            responsibility to define and collect.
        diffuse_percentile: Percentile at which to set the diffuse threshold.
            Default 95 means "anything more diffuse than 95% of baseline is
            flagged."
        concentrated_percentile: Percentile at which to set the concentrated
            threshold. Default 5 means "anything LESS concentrated than 95%
            of baseline is flagged as drift."

    Returns:
        CalibrationReport with full distributions and suggested thresholds.

    Raises:
        ValueError: if baseline is empty or contains wrong-shape matrices.
    """
    if not baseline_matrices:
        raise ValueError("baseline_matrices is empty; need at least 1 sample")
    if not (0.0 <= diffuse_percentile <= 100.0):
        raise ValueError(f"diffuse_percentile must be in [0, 100], got {diffuse_percentile}")
    if not (0.0 <= concentrated_percentile <= 100.0):
        raise ValueError(f"concentrated_percentile must be in [0, 100], got {concentrated_percentile}")

    notes = []
    if len(baseline_matrices) < 100:
        notes.append(
            f"Baseline has {len(baseline_matrices)} samples; recommend ≥100 "
            f"for stable percentile estimates and ≥1000 for tail accuracy."
        )

    # Shape validation
    for i, M in enumerate(baseline_matrices):
        if M.shape != (10, 10):
            raise ValueError(f"Baseline matrix {i} has shape {M.shape}, expected (10, 10)")

    # Run profiles
    diffuseness_vals: List[float] = []
    concentration_vals: List[float] = []
    per_dof_shares: Dict[str, List[float]] = {}

    skipped_zero = 0
    for M in baseline_matrices:
        p = monitor.profile(M)
        if p.dominant_dof is None:
            # zero or near-zero matrix; skip from distribution
            skipped_zero += 1
            continue
        diffuseness_vals.append(p.diffuseness)
        concentration_vals.append(p.concentration)
        for dof, share in p.orthogonal_profile.items():
            per_dof_shares.setdefault(dof, []).append(share)

    if skipped_zero > 0:
        notes.append(f"Skipped {skipped_zero} zero-norm matrices from distribution")

    if not diffuseness_vals:
        raise ValueError("All baseline matrices had zero norm; no calibration possible")

    diffuseness_vals.sort()
    concentration_vals.sort()
    for k in per_dof_shares:
        per_dof_shares[k].sort()

    suggested_diffuse = _percentile(diffuseness_vals, diffuse_percentile)
    suggested_concentrated = _percentile(concentration_vals, concentrated_percentile)

    return CalibrationReport(
        n_samples=len(diffuseness_vals),
        diffuseness_distribution=diffuseness_vals,
        concentration_distribution=concentration_vals,
        per_dof_share_distribution=per_dof_shares,
        suggested_diffuse_threshold=suggested_diffuse,
        suggested_concentrated_threshold=suggested_concentrated,
        diffuse_percentile=diffuse_percentile,
        concentrated_percentile=concentrated_percentile,
        notes=notes,
    )


# ---------------------------------------------------------------------
# Helpers (no scipy dep)
# ---------------------------------------------------------------------

def _percentile(sorted_data: List[float], p: float) -> float:
    """Linear-interpolation percentile, no scipy dependency."""
    if not sorted_data:
        return 0.0
    if len(sorted_data) == 1:
        return sorted_data[0]
    rank = (p / 100.0) * (len(sorted_data) - 1)
    lo = int(np.floor(rank))
    hi = int(np.ceil(rank))
    if lo == hi:
        return sorted_data[lo]
    frac = rank - lo
    return sorted_data[lo] * (1 - frac) + sorted_data[hi] * frac


def _median(sorted_data: List[float]) -> float:
    return _percentile(sorted_data, 50)


# ---------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------

def _demo():
    """Demo using a synthetic baseline mix.

    NOTE: this baseline is for DEMO ONLY. It is not a real CK runtime
    baseline. In production, the caller provides real activations.
    """
    print("=" * 70)
    print("CALIBRATION DEMO")
    print("=" * 70)
    print()
    print("WARNING: this demo uses a synthetic baseline. Real CK calibration")
    print("requires actual runtime activations as baseline.")
    print()

    from ck_dof_profile_monitor import _left_reps, _TSML

    # Build a synthetic baseline that is mostly Lie-flow with some noise.
    # In a real deployment, this would come from monitoring honest activations.
    L_T = _left_reps(_TSML)
    A_flow = [(L_T[i] - L_T[i].T) for i in [1, 2, 3, 4, 6, 8]]

    rng = np.random.RandomState(42)
    baseline = []
    for _ in range(500):
        # Mix flow operators with small noise, simulating a "structured" workload
        coeffs = rng.randn(6) * 1.0
        M = sum(c * A for c, A in zip(coeffs, A_flow))
        M = M + rng.randn(10, 10) * 0.05  # small noise
        baseline.append(M)

    monitor = DOFProfileMonitor()
    cal = calibrate_thresholds(monitor, baseline,
                                diffuse_percentile=95.0,
                                concentrated_percentile=5.0)
    print(cal.report())
    print()
    print("To apply suggested thresholds:")
    print(f"  monitor.diffuse_threshold      = {cal.suggested_diffuse_threshold:.4f}")
    print(f"  monitor.concentrated_threshold = {cal.suggested_concentrated_threshold:.4f}")


if __name__ == "__main__":
    _demo()
