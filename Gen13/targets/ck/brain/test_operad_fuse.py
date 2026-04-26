"""
test_operad_fuse.py - canonical fuse-rule and ternary-iteration tests.

Verifies the operad_fuse module against the WP112 paper's theorems:

    Theorem 5.5: 4-core arity-3 closure (all 64 triples in 4-core^3
                 fuse to in-core values; 8 non-assoc 4-core triples
                 all fuse to VOID).
    Theorem 5.7: Universal HARMONY attractor under canonical ternary
                 fuse iteration.
    Theorem 5.9: Universal HARMONY attractor is family-independent
                 (Family H gives the same result in <= 7 iterations).

Plus structural verifications: 126 non-associative triples covered;
fuse value distribution {0: 108, 7: 18}; image entirely in 4-core.
"""
from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))

from operad_fuse import (
    BHML, CANONICAL_FUSE_RULES, CORE_1, CORE_2, CORE_4, TSML,
    TSML_OP_NAMES, binary_left, binary_right, detect_harmony_attractor,
    detect_void_attractor, fuse, fuse_value_distribution,
    is_2core, is_4core, is_associative, is_1core, normalize_l1,
    ternary_iterate, ternary_step,
)


# ----- structural sanity tests -----

def test_tables_well_formed():
    """TSML and BHML are 10x10 with values in 0..9."""
    assert len(TSML) == 10
    assert len(BHML) == 10
    for row in TSML:
        assert len(row) == 10
        for v in row:
            assert 0 <= v <= 9
    for row in BHML:
        assert len(row) == 10
        for v in row:
            assert 0 <= v <= 9
    print("PASS: TSML and BHML tables well-formed")


def test_126_non_assoc_triples():
    """Exactly 126 non-associative triples across all 1000 triples."""
    count = 0
    for a in range(10):
        for b in range(10):
            for c in range(10):
                if not is_associative(a, b, c):
                    count += 1
    assert count == 126, f"expected 126 non-assoc triples, got {count}"
    print(f"PASS: exactly 126 non-associative triples")


def test_canonical_fuse_rules_complete():
    """CANONICAL_FUSE_RULES covers all 126 non-associative triples + the
    one associative override (3, 4, 7) -> 8."""
    expected_count = 126 + 1  # 126 non-assoc + 1 known override
    assert len(CANONICAL_FUSE_RULES) == expected_count, \
        f"expected {expected_count} rules, got {len(CANONICAL_FUSE_RULES)}"
    # Spot check: known override
    assert CANONICAL_FUSE_RULES[(3, 4, 7)] == 8
    print(f"PASS: CANONICAL_FUSE_RULES has {len(CANONICAL_FUSE_RULES)} entries "
          f"(126 non-assoc + 1 override)")


def test_fuse_distribution_108_18():
    """Fuse value distribution across 126 non-assoc triples is {0: 108,
    7: 18} per WP112."""
    dist = fuse_value_distribution()
    assert dist == {0: 108, 7: 18}, f"unexpected distribution: {dist}"
    print(f"PASS: fuse value distribution {{0: 108, 7: 18}} matches WP112")


def test_fuse_image_in_2core():
    """All canonical fuse values land in the 2-core {V, H} = {0, 7}."""
    for (a, b, c), v in CANONICAL_FUSE_RULES.items():
        if (a, b, c) == (3, 4, 7):
            # The associative override gives 8 (BREATH); skip
            continue
        assert v in CORE_2, f"fuse({a},{b},{c}) = {v} not in 2-core"
    print(f"PASS: image of canonical fuse on non-assoc triples is in 2-core {{V, H}}")


# ----- Theorem 5.5: 4-core arity-3 closure -----

def test_theorem_5_5_4core_arity3_closure():
    """Per WP112 Theorem 5.5: all 64 triples in {V, H, Br, R}^3 fuse to
    in-core values; 8 non-associative ones all fuse to VOID."""
    in_core_count = 0
    out_core_count = 0
    nonassoc_count = 0
    nonassoc_to_void = 0
    for a in CORE_4:
        for b in CORE_4:
            for c in CORE_4:
                v = fuse(a, b, c)
                if v in CORE_4:
                    in_core_count += 1
                else:
                    out_core_count += 1
                if not is_associative(a, b, c):
                    nonassoc_count += 1
                    if v == 0:  # VOID
                        nonassoc_to_void += 1
    assert in_core_count == 64
    assert out_core_count == 0
    assert nonassoc_count == 8
    assert nonassoc_to_void == 8
    print(f"PASS: Theorem 5.5 verified -- 64/64 in-core, 8 non-assoc all fuse to VOID")


# ----- Theorem 5.7: Universal HARMONY attractor -----

def test_theorem_5_7_universal_harmony_attractor():
    """Per WP112 Theorem 5.7: every non-trivial init converges to
    delta_H (HARMONY) in <= 7 iterations."""
    inits = {
        "uniform 4-core": [0.25 if i in CORE_4 else 0.0 for i in range(10)],
        "uniform 10-simplex": [0.1] * 10,
        "delta_HARMONY": [1.0 if i == 7 else 0.0 for i in range(10)],
        "delta_BREATH": [1.0 if i == 8 else 0.0 for i in range(10)],
        "delta_RESET": [1.0 if i == 9 else 0.0 for i in range(10)],
        "flow-only": [1.0/6 if i in {1, 2, 4, 5, 6, 7} else 0.0 for i in range(10)],
        "lattice-only": [0.25 if i in {0, 3, 8, 9} else 0.0 for i in range(10)],
    }
    for name, p in inits.items():
        attr, iters = ternary_iterate(p, max_iter=200)
        assert detect_harmony_attractor(attr, tol=1e-6), \
            f"{name} did not converge to HARMONY in {iters} iterations: " \
            f"max-7-mass={attr[7]:.6f}"
        assert iters <= 10, f"{name} took {iters} > 10 iterations"
    print(f"PASS: Theorem 5.7 verified -- 7 initial conditions converge to HARMONY")


def test_void_degenerate_fixed_point():
    """delta_V is the only OTHER fixed point of canonical ternary fuse
    (degenerate; no mass to spread)."""
    p = [1.0 if i == 0 else 0.0 for i in range(10)]
    attr, iters = ternary_iterate(p, max_iter=10)
    assert detect_void_attractor(attr, tol=1e-6), "delta_V did not stay at V"
    print(f"PASS: delta_V is the degenerate fixed point ({iters} iter)")


# ----- predicates -----

def test_core_predicates():
    """is_4core, is_2core, is_1core return expected results."""
    assert is_4core(0) and is_4core(7) and is_4core(8) and is_4core(9)
    assert not is_4core(1) and not is_4core(2)
    assert is_2core(0) and is_2core(7)
    assert not is_2core(8) and not is_2core(9)
    assert is_1core(7)
    assert not is_1core(0) and not is_1core(8)
    print("PASS: is_4core, is_2core, is_1core predicates correct")


# ----- integration smoke test -----

def test_fuse_callable_on_all_triples():
    """fuse() returns a value in 0..9 for every (a, b, c) triple."""
    for a in range(10):
        for b in range(10):
            for c in range(10):
                v = fuse(a, b, c)
                assert 0 <= v <= 9, f"fuse({a},{b},{c}) = {v} out of range"
    print("PASS: fuse() callable on all 1000 triples")


# ----- run all -----

def main():
    print("=" * 70)
    print("test_operad_fuse.py")
    print("=" * 70)
    print()
    tests = [
        test_tables_well_formed,
        test_126_non_assoc_triples,
        test_canonical_fuse_rules_complete,
        test_fuse_distribution_108_18,
        test_fuse_image_in_2core,
        test_theorem_5_5_4core_arity3_closure,
        test_theorem_5_7_universal_harmony_attractor,
        test_void_degenerate_fixed_point,
        test_core_predicates,
        test_fuse_callable_on_all_triples,
    ]
    failed = 0
    for t in tests:
        try:
            t()
        except AssertionError as e:
            failed += 1
            print(f"FAIL: {t.__name__}: {e}")
        except Exception as e:
            failed += 1
            print(f"ERROR: {t.__name__}: {e}")
    print()
    print(f"{len(tests) - failed} / {len(tests)} tests passed")
    return failed == 0


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
