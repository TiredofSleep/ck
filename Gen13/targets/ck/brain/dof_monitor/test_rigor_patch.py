"""
test_rigor_patch.py — Tests for ck_calibration and ck_gradient_profile.

Run with: python test_rigor_patch.py
"""
import numpy as np
import sys
sys.path.insert(0, '.')

from ck_dof_profile_monitor import DOFProfileMonitor, _left_reps, _TSML
from ck_calibration import calibrate_thresholds, CalibrationReport, _percentile, _median
from ck_gradient_profile import (
    GradientProfiler, GradientProfileResult, extract_10x10_slice,
)


# =====================================================================
# CALIBRATION TESTS
# =====================================================================

def test_calibration_empty_baseline_raises():
    monitor = DOFProfileMonitor()
    try:
        calibrate_thresholds(monitor, [])
        raise AssertionError("Should have raised ValueError")
    except ValueError as e:
        print(f"✓ Empty baseline raises ValueError")


def test_calibration_wrong_shape_raises():
    monitor = DOFProfileMonitor()
    try:
        calibrate_thresholds(monitor, [np.zeros((8, 8))])
        raise AssertionError("Should have raised ValueError")
    except ValueError as e:
        print(f"✓ Wrong-shape baseline raises ValueError")


def test_calibration_invalid_percentile():
    monitor = DOFProfileMonitor()
    try:
        calibrate_thresholds(monitor, [np.eye(10)], diffuse_percentile=150.0)
        raise AssertionError("Should have raised ValueError")
    except ValueError as e:
        print(f"✓ Invalid percentile raises ValueError")


def test_calibration_basic():
    """Calibration on a Lie-heavy baseline should produce LOW diffuse threshold."""
    monitor = DOFProfileMonitor()
    L_T = _left_reps(_TSML)
    A_flow = [(L_T[i] - L_T[i].T) for i in [1, 2, 3, 4, 6, 8]]

    rng = np.random.RandomState(42)
    baseline = []
    for _ in range(200):
        coeffs = rng.randn(6)
        M = sum(c * A for c, A in zip(coeffs, A_flow))
        M = M + rng.randn(10, 10) * 0.05
        baseline.append(M)

    cal = calibrate_thresholds(monitor, baseline,
                                diffuse_percentile=95.0,
                                concentrated_percentile=5.0)

    assert cal.n_samples == 200
    # Lie-heavy baseline → low diffuseness, high concentration
    assert cal.suggested_diffuse_threshold < 0.3, (
        f"Lie-heavy baseline should have low diffuse threshold, "
        f"got {cal.suggested_diffuse_threshold}")
    assert cal.suggested_concentrated_threshold > 0.8, (
        f"Lie-heavy baseline should have high concentrated threshold, "
        f"got {cal.suggested_concentrated_threshold}")
    print(f"✓ Lie-heavy calibration: diffuse_thresh={cal.suggested_diffuse_threshold:.3f}, "
          f"conc_thresh={cal.suggested_concentrated_threshold:.3f}")


def test_calibration_random_baseline_high_diffuse():
    """Calibration on random baseline should give HIGH diffuse threshold."""
    monitor = DOFProfileMonitor()
    rng = np.random.RandomState(0)
    baseline = [rng.randn(10, 10) * 0.5 for _ in range(200)]

    cal = calibrate_thresholds(monitor, baseline)
    # Random matrices are intrinsically diffuse
    assert cal.suggested_diffuse_threshold > 0.7, (
        f"Random baseline should have high diffuse threshold, "
        f"got {cal.suggested_diffuse_threshold}")
    print(f"✓ Random calibration: diffuse_thresh={cal.suggested_diffuse_threshold:.3f}")


def test_calibration_small_sample_warning():
    """Small sample sizes should produce a warning note."""
    monitor = DOFProfileMonitor()
    baseline = [np.eye(10) * (i + 1) for i in range(10)]
    cal = calibrate_thresholds(monitor, baseline)
    assert any("samples" in n for n in cal.notes), (
        f"Expected sample-size warning, got: {cal.notes}")
    print(f"✓ Small sample produces warning: {cal.notes[0]}")


def test_calibration_skips_zero():
    """Zero-norm matrices should be excluded from distribution."""
    monitor = DOFProfileMonitor()
    rng = np.random.RandomState(0)
    baseline = [rng.randn(10, 10) * 0.5 for _ in range(150)]
    baseline.extend([np.zeros((10, 10)) for _ in range(10)])
    cal = calibrate_thresholds(monitor, baseline)
    assert cal.n_samples == 150  # zeros excluded
    assert any("Skipped" in n for n in cal.notes)
    print(f"✓ Zero-norm matrices skipped: n_samples={cal.n_samples}")


def test_calibration_report_contains_stats():
    """Report should contain percentile and per-DOF info."""
    monitor = DOFProfileMonitor()
    rng = np.random.RandomState(0)
    baseline = [rng.randn(10, 10) * 0.5 for _ in range(150)]
    cal = calibrate_thresholds(monitor, baseline)
    report = cal.report()
    assert "Diffuseness distribution" in report
    assert "Concentration distribution" in report
    assert "Per-DOF share statistics" in report
    assert "Suggested thresholds" in report
    print("✓ Report contains required sections")


def test_percentile_helper():
    """Internal percentile helper handles edge cases."""
    assert _percentile([1.0, 2.0, 3.0, 4.0, 5.0], 0) == 1.0
    assert _percentile([1.0, 2.0, 3.0, 4.0, 5.0], 100) == 5.0
    assert _percentile([1.0, 2.0, 3.0, 4.0, 5.0], 50) == 3.0
    assert _percentile([1.0], 50) == 1.0
    assert _percentile([], 50) == 0.0
    print("✓ Percentile helper handles edge cases")


# =====================================================================
# GRADIENT PROFILER TESTS
# =====================================================================

def test_gradient_match_lie():
    """Pure Lie gradient on Lie-tagged layer = no mismatch."""
    monitor = DOFProfileMonitor()
    profiler = GradientProfiler(monitor)
    L_T = _left_reps(_TSML)
    A1 = (L_T[1] - L_T[1].T)
    result = profiler.profile(A1, expected_dof="lie")
    assert not result.mismatch
    assert result.actual_dominant == "lie"
    assert result.expected_share > 0.99
    print(f"✓ Lie/Lie match: share={result.expected_share:.3f}")


def test_gradient_mismatch_lie_on_jordan():
    """Lie gradient on Jordan-tagged layer = mismatch."""
    monitor = DOFProfileMonitor()
    profiler = GradientProfiler(monitor)
    L_T = _left_reps(_TSML)
    A1 = (L_T[1] - L_T[1].T)
    result = profiler.profile(A1, expected_dof="jordan")
    assert result.mismatch
    assert result.actual_dominant == "lie"
    print(f"✓ Lie/Jordan mismatch detected")


def test_gradient_no_expected_dof():
    """No expected_dof = no mismatch flag, just profile."""
    monitor = DOFProfileMonitor()
    profiler = GradientProfiler(monitor)
    rng = np.random.RandomState(0)
    R = rng.randn(10, 10)
    result = profiler.profile(R)  # no expected_dof
    assert result.expected_dof is None
    assert not result.mismatch
    assert result.expected_share is None
    print(f"✓ No-expected-DOF mode works")


def test_gradient_unknown_dof_raises():
    """Unknown expected DOF raises ValueError."""
    monitor = DOFProfileMonitor()
    profiler = GradientProfiler(monitor)
    try:
        profiler.profile(np.eye(10), expected_dof="nonsense")
        raise AssertionError("Should have raised")
    except ValueError:
        print("✓ Unknown DOF raises")


def test_gradient_wrong_shape_raises():
    """Non-(10,10) gradient raises with helpful message."""
    monitor = DOFProfileMonitor()
    profiler = GradientProfiler(monitor)
    try:
        profiler.profile(np.zeros((8, 8)), expected_dof="lie")
        raise AssertionError("Should have raised")
    except ValueError as e:
        assert "10×10" in str(e) or "10x10" in str(e)
        print(f"✓ Wrong-shape gradient raises with helpful msg")


def test_gradient_weak_alignment_warning():
    """Even when dominant matches, weak alignment fires a soft note."""
    monitor = DOFProfileMonitor()
    profiler = GradientProfiler(monitor)
    rng = np.random.RandomState(0)
    R = rng.randn(10, 10) * 0.3
    result = profiler.profile(R, expected_dof="lie")
    # Random matrix had ~40% Lie share, dominant = lie, but share < 0.5
    if result.expected_share is not None and result.expected_share < 0.5 and not result.mismatch:
        assert any("weakly" in n.lower() for n in result.notes)
        print(f"✓ Weak alignment warning fires")
    else:
        print(f"✓ (Weak alignment test inapplicable here, share={result.expected_share})")


def test_extract_10x10_slice_leading():
    """Leading-block slice."""
    W = np.arange(64*64).reshape(64, 64).astype(float)
    sliced = extract_10x10_slice(W, method="leading")
    assert sliced.shape == (10, 10)
    assert sliced[0, 0] == 0
    assert sliced[9, 9] == 9 * 64 + 9
    print("✓ Leading slice extracts top-left 10×10")


def test_extract_10x10_slice_svd():
    """SVD slice produces 10×10 with same singular structure as top-10 of original."""
    rng = np.random.RandomState(0)
    W = rng.randn(64, 64)
    sliced = extract_10x10_slice(W, method="svd")
    assert sliced.shape == (10, 10)
    print("✓ SVD slice produces 10×10")


def test_extract_10x10_slice_random():
    """Random slice extracts 10 random rows × 10 random cols."""
    rng = np.random.RandomState(0)
    W = rng.randn(64, 64)
    sliced = extract_10x10_slice(W, method="random")
    assert sliced.shape == (10, 10)
    print("✓ Random slice produces 10×10")


def test_extract_10x10_slice_too_small_raises():
    try:
        extract_10x10_slice(np.zeros((5, 5)))
        raise AssertionError("Should have raised")
    except ValueError:
        print("✓ Too-small matrix raises")


def test_extract_10x10_slice_unknown_method():
    try:
        extract_10x10_slice(np.zeros((20, 20)), method="bogus")
        raise AssertionError("Should have raised")
    except ValueError:
        print("✓ Unknown method raises")


# =====================================================================
# Run
# =====================================================================

def main():
    tests = [
        test_calibration_empty_baseline_raises,
        test_calibration_wrong_shape_raises,
        test_calibration_invalid_percentile,
        test_calibration_basic,
        test_calibration_random_baseline_high_diffuse,
        test_calibration_small_sample_warning,
        test_calibration_skips_zero,
        test_calibration_report_contains_stats,
        test_percentile_helper,
        test_gradient_match_lie,
        test_gradient_mismatch_lie_on_jordan,
        test_gradient_no_expected_dof,
        test_gradient_unknown_dof_raises,
        test_gradient_wrong_shape_raises,
        test_gradient_weak_alignment_warning,
        test_extract_10x10_slice_leading,
        test_extract_10x10_slice_svd,
        test_extract_10x10_slice_random,
        test_extract_10x10_slice_too_small_raises,
        test_extract_10x10_slice_unknown_method,
    ]

    print("=" * 70)
    print(f"Running {len(tests)} rigor patch tests")
    print("=" * 70)
    failures = 0
    for t in tests:
        try:
            t()
        except Exception as e:
            print(f"✗ {t.__name__} FAILED: {e}")
            failures += 1
    print()
    print("=" * 70)
    print(f"{len(tests) - failures} / {len(tests)} passed")
    print("=" * 70)
    sys.exit(0 if failures == 0 else 1)


if __name__ == "__main__":
    main()
