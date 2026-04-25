"""
test_modules.py — Sanity tests for the two CK modules.

Run with: python test_modules.py
Exits with non-zero status if any assertion fails.
"""
import numpy as np
import sys
sys.path.insert(0, '.')

from ck_dimension_mapper import (
    DOF_DIMENSIONS, compute_lora_ranks, check_dof_coverage,
    SO10_PLUS_DIM, SO10_MINUS_DIM, SO10_TOTAL,
)
from ck_dof_profile_monitor import (
    DOFProfileMonitor, _BASES, _left_reps, _TSML,
)


def test_dimension_constants():
    """Canonical dimensions match verified findings."""
    assert DOF_DIMENSIONS['lie'] == 28
    assert DOF_DIMENSIONS['jordan'] == 55
    assert DOF_DIMENSIONS['clifford'] == 36
    assert DOF_DIMENSIONS['permutation_vector'] == 9
    assert DOF_DIMENSIONS['lattice'] == 4
    assert SO10_PLUS_DIM == 36
    assert SO10_MINUS_DIM == 9
    assert SO10_TOTAL == 45
    print("✓ Canonical dimensions correct")


def test_dimension_mapper_basic():
    """Basic LoRA rank computation."""
    config = compute_lora_ranks(
        {"layer1": "lie", "layer2": "jordan"},
        total_rank_budget=83,  # = 28 + 55
        min_rank=1,
    )
    # Check both layers present
    assert "layer1" in config.layer_ranks
    assert "layer2" in config.layer_ranks
    # Lie should have smaller rank than Jordan (28 < 55)
    assert config.layer_ranks["layer1"] < config.layer_ranks["layer2"]
    # Total should be approximately budget
    total = sum(config.layer_ranks.values())
    assert abs(total - 83) <= 2  # rounding tolerance
    print(f"✓ Dimension mapper: lie={config.layer_ranks['layer1']}, "
          f"jordan={config.layer_ranks['layer2']}, total={total}")


def test_dimension_mapper_unknown_dof():
    """Unknown DOF raises ValueError."""
    try:
        compute_lora_ranks({"layer1": "nonsense"})
        raise AssertionError("Should have raised ValueError")
    except ValueError as e:
        print(f"✓ Unknown DOF raises ValueError: {e}")


def test_dimension_mapper_min_rank():
    """min_rank floor is respected."""
    config = compute_lora_ranks(
        {"l": "lattice"},  # canonical dim 4
        total_rank_budget=2,  # smaller than min_rank
        min_rank=4,
    )
    assert config.layer_ranks["l"] >= 4
    print(f"✓ min_rank floor respected: rank={config.layer_ranks['l']}")


def test_coverage_check():
    """Coverage check identifies missing DOFs."""
    coverage = check_dof_coverage({"l1": "lie", "l2": "jordan"})
    assert "lie" in coverage["covered_dofs"]
    assert "jordan" in coverage["covered_dofs"]
    assert "clifford" in coverage["missing_dofs"]
    assert "lattice" in coverage["missing_dofs"]
    print(f"✓ Coverage check: covered={coverage['covered_dofs']}, "
          f"missing={coverage['missing_dofs']}")


def test_monitor_orthogonal_partition_sums_to_one():
    """Orthogonal partition correctly sums to 1.0 for any input."""
    monitor = DOFProfileMonitor()
    np.random.seed(42)
    for trial in range(10):
        M = np.random.randn(10, 10)
        p = monitor.profile(M)
        s = sum(p.orthogonal_profile.values())
        assert abs(s - 1.0) < 0.01, f"Trial {trial}: sum = {s}"
    print(f"✓ Orthogonal partition sums to 1.0 over 10 random trials")


def test_monitor_concentrated_lie():
    """A pure Lie generator is concentrated, not diffuse."""
    monitor = DOFProfileMonitor()
    L_T = _left_reps(_TSML)
    A1 = (L_T[1] - L_T[1].T)
    p = monitor.profile(A1)
    assert p.is_concentrated, f"Lie generator should be concentrated, got {p.concentration}"
    assert not p.is_diffuse, f"Lie generator should not be diffuse, got {p.diffuseness}"
    assert p.dominant_dof == "lie", f"Expected dominant 'lie', got {p.dominant_dof}"
    assert abs(p.orthogonal_profile['lie'] - 1.0) < 0.01
    print(f"✓ Pure Lie generator: concentration={p.concentration:.3f}, dominant={p.dominant_dof}")


def test_monitor_concentrated_lattice():
    """A pure σ-fixed projector is concentrated on Lattice."""
    monitor = DOFProfileMonitor()
    M = np.diag([1, 0, 0, 1, 0, 0, 0, 0, 1, 1.0])  # σ-fixed indices only
    p = monitor.profile(M)
    assert p.is_concentrated
    assert p.dominant_dof == "lattice"
    assert abs(p.orthogonal_profile['lattice'] - 1.0) < 0.01
    print(f"✓ σ-fixed projector: concentration={p.concentration:.3f}, dominant={p.dominant_dof}")


def test_monitor_diffuse_random():
    """A random matrix is diffuse, not concentrated."""
    monitor = DOFProfileMonitor()
    np.random.seed(0)
    M = np.random.randn(10, 10) * 0.3
    p = monitor.profile(M)
    assert p.is_diffuse, f"Random should be diffuse, got diffuseness={p.diffuseness}"
    print(f"✓ Random matrix: diffuseness={p.diffuseness:.3f}")


def test_monitor_zero():
    """A zero matrix returns zero norm and no flags."""
    monitor = DOFProfileMonitor()
    p = monitor.profile(np.zeros((10, 10)))
    assert not p.is_concentrated
    assert not p.is_diffuse
    assert p.dominant_dof is None
    print(f"✓ Zero matrix handled cleanly")


def test_monitor_shape_validation():
    """Wrong shape raises ValueError."""
    monitor = DOFProfileMonitor()
    try:
        monitor.profile(np.zeros((8, 8)))
        raise AssertionError("Should have raised ValueError")
    except ValueError as e:
        print(f"✓ Wrong shape raises ValueError")


def test_monitor_drift_trajectory():
    """Concentration decreases monotonically as we add noise to a clean signal."""
    monitor = DOFProfileMonitor()
    L_T = _left_reps(_TSML)
    A1 = (L_T[1] - L_T[1].T)
    np.random.seed(0)
    R = np.random.randn(10, 10) * 0.3

    diffusenesses = []
    for alpha in np.linspace(0, 1, 6):
        M = (1 - alpha) * A1 + alpha * R
        p = monitor.profile(M)
        diffusenesses.append(p.diffuseness)

    # Should be monotonically increasing (or close to it)
    for i in range(len(diffusenesses) - 1):
        # Allow tiny non-monotonicity due to noise interaction
        assert diffusenesses[i + 1] >= diffusenesses[i] - 0.05, (
            f"Diffuseness should not decrease: {diffusenesses}")
    print(f"✓ Drift trajectory monotonic: {[round(d,3) for d in diffusenesses]}")


def test_dimension_consistency():
    """Verify that monitor and mapper agree on canonical dimensions."""
    dims = _BASES.dimensions()
    assert dims['raw']['lie'] == DOF_DIMENSIONS['lie']
    assert dims['raw']['jordan'] == DOF_DIMENSIONS['jordan']
    assert dims['raw']['clifford'] == DOF_DIMENSIONS['clifford']
    assert dims['raw']['permutation_vector'] == DOF_DIMENSIONS['permutation_vector']
    assert dims['raw']['lattice'] == DOF_DIMENSIONS['lattice']
    print(f"✓ Mapper and Monitor agree on dimensions")


def test_monitor_concentration_below_threshold_for_diffuse():
    """A diffuse signal has concentration below threshold."""
    monitor = DOFProfileMonitor()
    np.random.seed(0)
    M = np.random.randn(10, 10) * 0.3
    p = monitor.profile(M)
    assert p.concentration < monitor.concentrated_threshold
    print(f"✓ Diffuse signal has concentration={p.concentration:.3f} "
          f"< threshold={monitor.concentrated_threshold}")


def main():
    tests = [
        test_dimension_constants,
        test_dimension_mapper_basic,
        test_dimension_mapper_unknown_dof,
        test_dimension_mapper_min_rank,
        test_coverage_check,
        test_monitor_orthogonal_partition_sums_to_one,
        test_monitor_concentrated_lie,
        test_monitor_concentrated_lattice,
        test_monitor_diffuse_random,
        test_monitor_zero,
        test_monitor_shape_validation,
        test_monitor_drift_trajectory,
        test_dimension_consistency,
        test_monitor_concentration_below_threshold_for_diffuse,
    ]

    print("=" * 70)
    print(f"Running {len(tests)} tests")
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
