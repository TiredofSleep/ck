"""test_ck_rhythm.py -- regression tests for the phase-clock module.

What we test:
  T1 -- canonical constants have expected values (φ, π, √2)
  T2 -- rhythm_at(t) is pure (same input -> same output)
  T3 -- beat values stay in [-1, 1]
  T4 -- phase_op cycles 0..9 once per 10 seconds
  T5 -- phase_fraction is in [0, 1)
  T6 -- composite_beat is the mean of the three individual beats
  T7 -- hint_for_op_class returns a non-empty string for each operator
  T8 -- is_up_beat / is_down_beat respect their threshold
  T9 -- daemon start/stop is clean
  T10 -- daemon history grows over time
  T11 -- daemon respects buffer_size (circular)
"""
from __future__ import annotations

import math
import sys
import time
from pathlib import Path

HERE = Path(__file__).parent.resolve()
sys.path.insert(0, str(HERE))

from ck_rhythm import (  # noqa: E402
    OP_NAMES,
    PHI,
    PI,
    SQRT2,
    RhythmDaemon,
    RhythmSnapshot,
    current_rhythm,
    hint_for_op_class,
    is_down_beat,
    is_up_beat,
    rhythm_at,
)


def test_constants():
    assert abs(PHI - 1.6180339887498949) < 1e-15
    assert abs(PI - math.pi) < 1e-15
    assert abs(SQRT2 - math.sqrt(2.0)) < 1e-15
    print("T1 PASS: PHI, PI, SQRT2 match canonical values to 1e-15")


def test_purity():
    """rhythm_at(t) is a pure function."""
    a = rhythm_at(1779000000.0)
    b = rhythm_at(1779000000.0)
    assert a == b, "rhythm_at must be pure"
    print("T2 PASS: rhythm_at is pure (same t -> same snapshot)")


def test_beat_bounds():
    """Beats are sine-wave outputs, must be in [-1, 1]."""
    for t in (0.0, 1.0, 100.0, 1779000000.0, 1779000123.456):
        s = rhythm_at(t)
        for beat_name, beat_val in (
            ("phi_beat", s.phi_beat),
            ("pi_beat", s.pi_beat),
            ("sqrt2_beat", s.sqrt2_beat),
            ("composite_beat", s.composite_beat),
        ):
            assert -1.0 <= beat_val <= 1.0, (
                f"{beat_name} out of [-1, 1] at t={t}: {beat_val}")
    print("T3 PASS: all four beat values in [-1, 1] across 5 test times")


def test_phase_cycle():
    """phase_op = floor(t) mod 10 — advances 1/sec, wraps after 10."""
    for t_int in range(0, 100):
        s = rhythm_at(float(t_int))
        assert s.phase_op == t_int % 10, (
            f"phase_op mismatch at t={t_int}: {s.phase_op} != {t_int % 10}")
        assert s.phase_op_name == OP_NAMES[s.phase_op]
    print("T4 PASS: phase_op cycles 0..9 once per 10 seconds")


def test_phase_fraction():
    """phase_fraction = t - floor(t), in [0, 1)."""
    for t in (0.0, 0.5, 1.0, 1.7, 1779000000.123):
        s = rhythm_at(t)
        assert 0.0 <= s.phase_fraction < 1.0, (
            f"phase_fraction out of [0, 1) at t={t}: {s.phase_fraction}")
        # Should equal t - floor(t) (within rounding)
        expected = t - int(t)
        assert abs(s.phase_fraction - expected) < 1e-3, (
            f"phase_fraction {s.phase_fraction} != t - floor(t) {expected}")
    print("T5 PASS: phase_fraction in [0, 1)")


def test_composite_is_mean():
    """composite_beat = mean of phi/pi/sqrt2 beats."""
    for t in (1.0, 5.0, 100.0, 1779000000.0):
        s = rhythm_at(t)
        computed = (s.phi_beat + s.pi_beat + s.sqrt2_beat) / 3.0
        # Rounded to 6 places, so allow a small epsilon
        assert abs(s.composite_beat - round(computed, 6)) < 1e-5, (
            f"composite mismatch at t={t}: "
            f"{s.composite_beat} vs mean({s.phi_beat}, "
            f"{s.pi_beat}, {s.sqrt2_beat}) = {computed}")
    print("T6 PASS: composite_beat = mean of three individual beats")


def test_hints_present():
    """All 10 operators have a non-empty hint string."""
    for op in range(10):
        hint = hint_for_op_class(op)
        assert hint and len(hint) > 5, (
            f"empty/short hint for op {op}: {hint!r}")
        # Hint should mention the operator name
        assert OP_NAMES[op] in hint or OP_NAMES[op].lower() in hint.lower(), (
            f"hint for op {op} ({OP_NAMES[op]}) doesn't name the operator: {hint!r}")
    print("T7 PASS: all 10 operators have non-empty named hints")


def test_up_down_beat():
    """is_up_beat and is_down_beat respect threshold."""
    # Build a snapshot with known composite_beat
    s_up = RhythmSnapshot(ts=0.0, phi_beat=0.9, pi_beat=0.9, sqrt2_beat=0.9,
                            composite_beat=0.9, phase_op=0, phase_op_name="VOID",
                            phase_fraction=0.0)
    s_down = RhythmSnapshot(ts=0.0, phi_beat=-0.9, pi_beat=-0.9, sqrt2_beat=-0.9,
                              composite_beat=-0.9, phase_op=0, phase_op_name="VOID",
                              phase_fraction=0.0)
    s_mid = RhythmSnapshot(ts=0.0, phi_beat=0.0, pi_beat=0.0, sqrt2_beat=0.0,
                             composite_beat=0.0, phase_op=0, phase_op_name="VOID",
                             phase_fraction=0.0)
    assert is_up_beat(s_up)
    assert not is_up_beat(s_down)
    assert not is_up_beat(s_mid)
    assert is_down_beat(s_down)
    assert not is_down_beat(s_up)
    assert not is_down_beat(s_mid)
    print("T8 PASS: is_up_beat / is_down_beat respect threshold (±0.3)")


def test_daemon_lifecycle():
    d = RhythmDaemon(poll_hz=5.0, buffer_size=20)
    assert d.latest() is None
    d.start()
    time.sleep(1.0)
    assert d.latest() is not None
    d.stop()
    print("T9 PASS: daemon start/stop is clean")


def test_daemon_history_grows():
    d = RhythmDaemon(poll_hz=10.0, buffer_size=50)
    d.start()
    time.sleep(0.3)
    n_a = len(d.history())
    time.sleep(0.5)
    n_b = len(d.history())
    d.stop()
    assert n_b > n_a, f"history should grow: {n_a} then {n_b}"
    print(f"T10 PASS: daemon history grew {n_a} -> {n_b} in 0.5s")


def test_daemon_circular_buffer():
    d = RhythmDaemon(poll_hz=20.0, buffer_size=5)
    d.start()
    time.sleep(0.6)  # ~12 ticks into 5-slot buffer
    d.stop()
    assert len(d.history()) <= 5
    print(f"T11 PASS: daemon respects buffer_size=5 "
          f"({len(d.history())} kept)")


def run_all():
    print("=" * 64)
    print("ck_rhythm regression tests")
    print("=" * 64)
    print()
    tests = [
        test_constants,
        test_purity,
        test_beat_bounds,
        test_phase_cycle,
        test_phase_fraction,
        test_composite_is_mean,
        test_hints_present,
        test_up_down_beat,
        test_daemon_lifecycle,
        test_daemon_history_grows,
        test_daemon_circular_buffer,
    ]
    n_pass = 0
    n_fail = 0
    for t in tests:
        try:
            t()
            n_pass += 1
        except AssertionError as e:
            print(f"  {t.__name__} FAIL: {e}")
            n_fail += 1
        except Exception as e:
            print(f"  {t.__name__} ERROR: {type(e).__name__}: {e}")
            n_fail += 1
    print()
    print("=" * 64)
    print(f"RESULT: {n_pass}/{len(tests)} tests passed")
    print("=" * 64)
    return n_fail == 0


if __name__ == "__main__":
    ok = run_all()
    sys.exit(0 if ok else 1)
