"""
test_attractor_detector.py - tests for attractor_detector.py.

Verifies that detect_attractor() correctly classifies CK runtime
distributions against the canonical attractor hierarchy:
  1-core (delta_H), 2-core, 4-core-attractor, 4-core-supported,
  void-degenerate, transient.
"""
from __future__ import annotations

import sys
from math import sqrt
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))

from attractor_detector import (
    AttractorState, H_OVER_BR_EXACT, UNIVERSAL_4CORE_ATTRACTOR,
    closed_form_h_over_br, detect_attractor, joint_chain_shells,
    universal_attractor_distribution,
)


def test_universal_attractor_distribution():
    """The universal-attractor 10-vector is normalized."""
    p = universal_attractor_distribution()
    assert len(p) == 10
    assert abs(sum(p) - 1.0) < 1e-10
    # Mass entirely on 4-core
    for i in range(10):
        if i not in {0, 7, 8, 9}:
            assert p[i] == 0.0, f"non-4-core idx {i} has mass {p[i]}"
    # H/Br matches closed form
    assert abs(p[7] / p[8] - H_OVER_BR_EXACT) < 1e-9
    print("PASS: universal_attractor_distribution() normalized + matches closed form")


def test_detect_universal_4core_attractor():
    """detect_attractor on the universal 4-core attractor returns
    layer='4-core-attractor' and is_universal_4core=True."""
    p = universal_attractor_distribution()
    state = detect_attractor(p, tol=1e-3)
    assert state.layer == "4-core-attractor", f"got layer={state.layer}"
    assert state.is_universal_4core
    assert state.is_4core_supported
    assert not state.is_2core_supported  # has Br, R mass
    assert not state.is_harmony_attractor
    assert not state.is_void_degenerate
    assert state.h_over_br_residual < 1e-9
    print(f"PASS: detect_attractor on universal 4-core: {state.summary()}")


def test_detect_pure_harmony():
    """detect_attractor on delta_H returns layer='1-core' and
    is_harmony_attractor=True."""
    p = [0.0] * 10
    p[7] = 1.0
    state = detect_attractor(p)
    assert state.layer == "1-core", f"got layer={state.layer}"
    assert state.is_harmony_attractor
    assert state.is_2core_supported
    assert state.is_4core_supported
    assert not state.is_universal_4core
    print(f"PASS: detect_attractor on delta_H: {state.summary()}")


def test_detect_pure_void():
    """detect_attractor on delta_V returns layer='void-degenerate'."""
    p = [0.0] * 10
    p[0] = 1.0
    state = detect_attractor(p)
    assert state.layer == "void-degenerate", f"got layer={state.layer}"
    assert state.is_void_degenerate
    print(f"PASS: detect_attractor on delta_V: {state.summary()}")


def test_detect_2core_mixed():
    """detect_attractor on 50/50 V+H returns layer='2-core'."""
    p = [0.0] * 10
    p[0] = 0.5
    p[7] = 0.5
    state = detect_attractor(p)
    assert state.layer == "2-core", f"got layer={state.layer}"
    assert state.is_2core_supported
    assert state.is_4core_supported
    print(f"PASS: detect_attractor on V+H mix: {state.summary()}")


def test_detect_4core_supported_non_attractor():
    """detect_attractor on 4-core uniform (NOT the universal attractor
    coordinates) returns layer='4-core-supported'."""
    p = [0.0] * 10
    for i in {0, 7, 8, 9}:
        p[i] = 0.25
    state = detect_attractor(p)
    assert state.layer == "4-core-supported", f"got layer={state.layer}"
    assert state.is_4core_supported
    assert not state.is_universal_4core  # uniform != universal coords
    print(f"PASS: detect_attractor on 4-core uniform: {state.summary()}")


def test_detect_transient():
    """detect_attractor on uniform 10-simplex returns layer='transient'."""
    p = [0.1] * 10
    state = detect_attractor(p)
    assert state.layer == "transient", f"got layer={state.layer}"
    assert not state.is_4core_supported
    print(f"PASS: detect_attractor on uniform 10-simplex: {state.summary()}")


def test_closed_form_h_over_br():
    """closed_form_h_over_br() returns 1 + sqrt(3)."""
    assert abs(closed_form_h_over_br() - (1.0 + sqrt(3.0))) < 1e-15
    print(f"PASS: closed_form_h_over_br() = 1 + sqrt(3) = {closed_form_h_over_br():.10f}")


def test_joint_chain_shells():
    """joint_chain_shells() returns 7 shells, strictly increasing in
    inclusion, with sizes {1, 4, 5, 6, 8, 9, 10}."""
    shells = joint_chain_shells()
    assert len(shells) == 7
    sizes = [len(s) for s in shells]
    assert sizes == [1, 4, 5, 6, 8, 9, 10], f"got sizes {sizes}"
    for i in range(len(shells) - 1):
        assert set(shells[i]).issubset(set(shells[i + 1]))
    print(f"PASS: joint_chain_shells() = 7 strict shells, sizes {sizes}")


# ----- run all -----

def main():
    print("=" * 70)
    print("test_attractor_detector.py")
    print("=" * 70)
    print()
    tests = [
        test_universal_attractor_distribution,
        test_detect_universal_4core_attractor,
        test_detect_pure_harmony,
        test_detect_pure_void,
        test_detect_2core_mixed,
        test_detect_4core_supported_non_attractor,
        test_detect_transient,
        test_closed_form_h_over_br,
        test_joint_chain_shells,
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
