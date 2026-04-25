"""
ck_gradient_profile.py — Gradient-profile diagnostic for training hygiene

A thin wrapper around DOFProfileMonitor specialized for gradient updates.

The math is identical: project a 10×10 matrix onto verified DOF subspaces.
The interpretation is different:

    • For activations: "is the model's current state drifting?"
    • For gradients:   "is the optimizer pushing this layer in the right
                        DOF direction, or is it shoving foreign content
                        into a DOF-tagged layer?"

WHEN TO USE:

    During training, after computing gradients but before applying them,
    project the gradient ΔW for each DOF-tagged layer. Check that the
    dominant DOF in the gradient profile matches the layer's tagged DOF.

    A mismatch indicates one of:
      • The architectural assumption is wrong (this layer doesn't actually
        carry the DOF you tagged it with)
      • The loss function is pushing the layer in a non-canonical direction
      • The data distribution is exercising the layer in an unexpected way
      • The previous training step has destabilized the layer's DOF identity

    None of these are automatically "bad" — they're diagnostic signals.
    Whether to act on them depends on the deployment.

WHAT THIS MODULE DOES NOT DO:

    • Modify gradients (no clipping, no projection-correction).
    • Decide whether mismatches are problems.
    • Handle non-(10×10) gradients. For larger weight matrices, the caller
      must reshape, downsample, or block-decompose to a 10×10 view first.
      We provide a helper for the simplest case (extracting a 10×10 slice).

USAGE:

    from ck_dof_profile_monitor import DOFProfileMonitor
    from ck_gradient_profile import GradientProfiler, profile_gradient

    monitor = DOFProfileMonitor()
    profiler = GradientProfiler(monitor)

    # Per training step, per DOF-tagged layer:
    grad_10x10 = extract_10x10_view(layer.weight.grad)  # caller's reshape
    result = profiler.profile(grad_10x10, expected_dof="lie")

    if result.mismatch:
        log_mismatch(layer.name, result)
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Optional
import numpy as np

from ck_dof_profile_monitor import DOFProfileMonitor, DOFProfile


@dataclass
class GradientProfileResult:
    """Result of profiling a gradient update."""

    profile: DOFProfile
    """Full DOF profile of the gradient (same structure as activations)."""

    expected_dof: Optional[str]
    """The DOF this layer was tagged with, if provided."""

    actual_dominant: Optional[str]
    """The DOF the gradient actually concentrated on."""

    mismatch: bool
    """True iff expected_dof was provided AND it differs from actual_dominant."""

    expected_share: Optional[float]
    """Share of the gradient's norm that fell in the expected DOF (if any)."""

    notes: List[str] = field(default_factory=list)


class GradientProfiler:
    """Profiles gradient updates against expected DOF tags.

    Wraps a DOFProfileMonitor. The monitor's bases (canonical TSML/BHML
    subspaces) are used as-is.
    """

    # Mapping from raw DOF name to its corresponding orthogonal-partition piece
    # (where the "primary" content for that DOF lives).
    _RAW_TO_ORTHO = {
        "lie": "lie",
        "jordan": "jordan_extra",       # most Jordan content (excludes Lattice)
        "clifford": "clifford_extra",   # Clifford content NOT also in Lie
        "permutation_vector": "permutation_vector",
        "lattice": "lattice",
    }

    def __init__(self, monitor: DOFProfileMonitor):
        self.monitor = monitor

    def profile(
        self,
        gradient: np.ndarray,
        expected_dof: Optional[str] = None,
    ) -> GradientProfileResult:
        """Profile a 10×10 gradient and check against expected DOF.

        Args:
            gradient: 10×10 numpy matrix representing a gradient slice.
                For larger weight matrices, the caller must reduce to 10×10
                first (see extract_10x10_slice helper).
            expected_dof: optional DOF tag for the layer. If provided,
                triggers the mismatch check.

        Returns:
            GradientProfileResult with profile, dominant DOF, and mismatch flag.
        """
        if gradient.shape != (10, 10):
            raise ValueError(
                f"Expected 10×10 gradient, got {gradient.shape}. "
                f"For larger gradients, use extract_10x10_slice() or "
                f"a domain-appropriate reduction first."
            )

        notes = []
        profile = self.monitor.profile(gradient)
        actual_dominant = profile.dominant_dof

        mismatch = False
        expected_share = None

        if expected_dof is not None:
            # Validate
            if expected_dof not in self._RAW_TO_ORTHO:
                raise ValueError(
                    f"Unknown DOF '{expected_dof}'. "
                    f"Valid: {sorted(self._RAW_TO_ORTHO.keys())}"
                )

            expected_ortho = self._RAW_TO_ORTHO[expected_dof]
            expected_share = profile.orthogonal_profile.get(expected_ortho, 0.0)

            # Mismatch if the gradient's strongest DOF is not the expected one
            # (Note: actual_dominant comes from orthogonal_profile dominant key)
            if actual_dominant != expected_ortho:
                mismatch = True
                notes.append(
                    f"Expected dominant DOF '{expected_dof}' (ortho '{expected_ortho}'), "
                    f"got '{actual_dominant}'"
                )

            # Even if dominant matches, flag if expected share is unusually low
            # (this is a soft signal; threshold is intentionally loose)
            if not mismatch and expected_share < 0.5:
                notes.append(
                    f"Dominant DOF matches but expected share is only "
                    f"{expected_share:.3f} (<0.5). Gradient is weakly aligned."
                )

        return GradientProfileResult(
            profile=profile,
            expected_dof=expected_dof,
            actual_dominant=actual_dominant,
            mismatch=mismatch,
            expected_share=expected_share,
            notes=notes,
        )


def extract_10x10_slice(W: np.ndarray, *, method: str = "leading") -> np.ndarray:
    """Helper: reduce a larger 2D matrix to a 10×10 view.

    Provided as a starting point for cases where weight/gradient matrices
    are larger than 10×10. The "right" reduction is domain-specific —
    caller should consider whether their canonical 10-dim TIG basis
    corresponds to specific input/output channels.

    Args:
        W: 2D numpy array.
        method: one of:
            "leading" — top-left 10×10 block (works for visualization,
                NOT structurally meaningful in general).
            "svd" — top-10 singular vectors compressed to 10×10 diagonal
                (preserves principal directions but loses geometry).
            "random" — uniform random 10×10 sub-block (sanity baseline).

    Returns:
        10×10 numpy array.

    Caveat:
        These reductions are not algebraically canonical. A real deployment
        should reduce gradients to 10×10 in a way aligned with the layer's
        DOF tagging — typically by selecting the 10 input/output indices
        that correspond to the TIG basis directions for that layer.
    """
    if W.ndim != 2:
        raise ValueError(f"Expected 2D matrix, got shape {W.shape}")
    if W.shape[0] < 10 or W.shape[1] < 10:
        raise ValueError(f"Matrix {W.shape} is smaller than 10×10")

    if method == "leading":
        return W[:10, :10].copy()
    elif method == "svd":
        U, S, Vt = np.linalg.svd(W, full_matrices=False)
        # Top-10 singular components, projected to 10×10
        k = min(10, len(S))
        return U[:10, :k] @ np.diag(S[:k]) @ Vt[:k, :10]
    elif method == "random":
        rng = np.random.RandomState(0)
        rows = rng.choice(W.shape[0], 10, replace=False)
        cols = rng.choice(W.shape[1], 10, replace=False)
        return W[np.ix_(rows, cols)].copy()
    else:
        raise ValueError(f"Unknown method '{method}'. "
                         f"Choose from: leading, svd, random.")


# ---------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------

def _demo():
    print("=" * 70)
    print("GRADIENT PROFILER DEMO")
    print("=" * 70)
    print()

    from ck_dof_profile_monitor import _left_reps, _TSML

    monitor = DOFProfileMonitor()
    profiler = GradientProfiler(monitor)

    # Build a few representative "gradients" with known DOF character
    L_T = _left_reps(_TSML)
    L1f = L_T[1].astype(float)
    A1 = (L_T[1] - L_T[1].T)
    S1 = (L1f + L1f.T) / 2

    print("--- Test 1: pure-Lie gradient on a Lie-tagged layer (good) ---")
    result = profiler.profile(A1, expected_dof="lie")
    print(f"  Expected: lie, Actual dominant: {result.actual_dominant}")
    print(f"  Expected share: {result.expected_share:.3f}")
    print(f"  Mismatch: {result.mismatch}")
    if result.notes:
        for n in result.notes:
            print(f"  NOTE: {n}")

    print()
    print("--- Test 2: pure-Lie gradient on a Jordan-tagged layer (bad) ---")
    result = profiler.profile(A1, expected_dof="jordan")
    print(f"  Expected: jordan, Actual dominant: {result.actual_dominant}")
    print(f"  Expected share: {result.expected_share:.3f}")
    print(f"  Mismatch: {result.mismatch}")
    if result.notes:
        for n in result.notes:
            print(f"  NOTE: {n}")

    print()
    print("--- Test 3: symmetric gradient on a Jordan-tagged layer (good) ---")
    result = profiler.profile(S1, expected_dof="jordan")
    print(f"  Expected: jordan, Actual dominant: {result.actual_dominant}")
    print(f"  Expected share: {result.expected_share:.3f}")
    print(f"  Mismatch: {result.mismatch}")

    print()
    print("--- Test 4: random gradient on a Lie-tagged layer (likely mismatch) ---")
    rng = np.random.RandomState(0)
    R = rng.randn(10, 10) * 0.3
    result = profiler.profile(R, expected_dof="lie")
    print(f"  Expected: lie, Actual dominant: {result.actual_dominant}")
    print(f"  Expected share: {result.expected_share:.3f}")
    print(f"  Mismatch: {result.mismatch}")
    if result.notes:
        for n in result.notes:
            print(f"  NOTE: {n}")

    print()
    print("--- Test 5: extract_10x10_slice helper on larger matrix ---")
    W_big = rng.randn(64, 64)
    sliced = extract_10x10_slice(W_big, method="leading")
    print(f"  Reduced 64×64 to {sliced.shape} via 'leading' method")
    sliced_svd = extract_10x10_slice(W_big, method="svd")
    print(f"  Reduced 64×64 to {sliced_svd.shape} via 'svd' method")


if __name__ == "__main__":
    _demo()
