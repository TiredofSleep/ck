"""
test_meta_curiosity.py -- unit tests for ck_curiosity meta-pattern logic
=========================================================================

Guards the meta-curiosity round 2 detectors:

  - _detect_meta_pattern   (meta_bridge / meta_op_gravity / meta_bridge_cold)
  - _format_question       (wiring the detected shift into the prompt)

The "curiosity about curiosity" directive means CK should sometimes ask
a question ABOUT his recent questions rather than about a single state
shift.  These tests lock the pattern-detector so future changes don't
silently lose that capability.

Run:  python Gen12/targets/ck_desktop/test_meta_curiosity.py

(c) 2026 Brayden Sanders / 7Site LLC
"""
from __future__ import annotations

import os
import sys
from collections import deque

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)

from ck_curiosity import (  # noqa: E402
    _detect_meta_pattern,
    _format_question,
    CuriosityState,
)


# ---------------------------------------------------------------------------
# _detect_meta_pattern
# ---------------------------------------------------------------------------


def test_bridge_streak_fires_on_3_of_5() -> None:
    """Same bridge on >=3 of the last 5 questions returns meta_bridge."""
    bridges = deque([
        ["sigma_NS_or_YM->Millennium_reframe"],
        [],
        ["sigma_NS_or_YM->Millennium_reframe", "HARMONY->TSML_synthesis_arc_73_cells"],
        ["sigma_NS_or_YM->Millennium_reframe"],
        [],
    ], maxlen=6)
    ops = deque(["HARMONY", "BALANCE", "HARMONY", "HARMONY", "BALANCE"], maxlen=6)
    out = _detect_meta_pattern(bridges, ops)
    assert out is not None and out.startswith("meta_bridge:"), (
        f"expected meta_bridge, got {out!r}"
    )
    # Expected shape: "meta_bridge:<count>:<bridge>"
    parts = out.split(":", 2)
    assert parts[1] == "3", f"expected count=3 in {out!r}"
    assert parts[2] == "sigma_NS_or_YM->Millennium_reframe", (
        f"expected specific bridge in {out!r}"
    )
    print("PASS: bridge-streak fires on 3-of-5 with specific bridge tag")


def test_op_gravity_fires_on_4_of_5() -> None:
    """Same dominant_op on >=4 of the last 5 returns meta_op_gravity.

    Bridge-streak must NOT fire (nothing shared across bridges)
    so op-gravity is the winning pattern.
    """
    bridges = deque([["A->x"], [], ["B->y"], [], ["C->z"]], maxlen=6)
    ops = deque(["HARMONY", "HARMONY", "HARMONY", "HARMONY", "BALANCE"], maxlen=6)
    out = _detect_meta_pattern(bridges, ops)
    assert out is not None and out.startswith("meta_op_gravity:"), (
        f"expected meta_op_gravity, got {out!r}"
    )
    parts = out.split(":", 2)
    assert parts[1] == "4" and parts[2] == "HARMONY", (
        f"expected count=4 op=HARMONY in {out!r}"
    )
    print("PASS: op-gravity fires on 4-of-5 with operator name")


def test_bridge_cold_fires_on_4_empty() -> None:
    """Last 4+ turns with zero bridges returns meta_bridge_cold.

    Op-gravity must not overshadow it: ops vary.
    """
    bridges = deque([[], [], [], []], maxlen=6)
    ops = deque(["HARMONY", "BALANCE", "HARMONY", "BALANCE"], maxlen=6)
    out = _detect_meta_pattern(bridges, ops)
    assert out == "meta_bridge_cold:4", (
        f"expected meta_bridge_cold:4, got {out!r}"
    )
    print("PASS: bridge-cold fires on 4 empty-bridge turns")


def test_no_false_positives_on_varied_signal() -> None:
    """Varied bridges + varied ops = no meta pattern."""
    bridges = deque([["A->x"], ["B->y"], ["C->z"], ["D->w"]], maxlen=6)
    ops = deque(["HARMONY", "BALANCE", "COLLAPSE", "PROGRESS"], maxlen=6)
    assert _detect_meta_pattern(bridges, ops) is None, (
        "varied signal should produce no meta shift"
    )
    print("PASS: no false positive on varied bridges + ops")


def test_short_history_returns_none() -> None:
    """Need >=4 entries; fewer returns None even on strong pattern."""
    bridges = deque([["A->x"], ["A->x"], ["A->x"]], maxlen=6)
    ops = deque(["HARMONY", "HARMONY", "HARMONY"], maxlen=6)
    assert _detect_meta_pattern(bridges, ops) is None, (
        "history < 4 should bypass detection"
    )
    print("PASS: short history (<4) returns None, prevents cold-start false positives")


def test_priority_bridge_beats_op() -> None:
    """When BOTH bridge-streak and op-gravity would fire, bridge wins.

    Bridge patterns carry specific semantic content (which corpus anchor
    keeps pulling); op-gravity is coarser.  The detector must return
    meta_bridge, not meta_op_gravity, when both qualify.
    """
    bridges = deque([
        ["sigma_NS_or_YM->X"],
        ["sigma_NS_or_YM->X"],
        ["sigma_NS_or_YM->X"],
        ["sigma_NS_or_YM->X"],
        [],
    ], maxlen=6)
    ops = deque(["HARMONY", "HARMONY", "HARMONY", "HARMONY", "BALANCE"], maxlen=6)
    out = _detect_meta_pattern(bridges, ops)
    assert out is not None and out.startswith("meta_bridge:"), (
        f"bridge-streak must take priority when both fire; got {out!r}"
    )
    print("PASS: meta_bridge wins over meta_op_gravity when both qualify")


# ---------------------------------------------------------------------------
# _format_question end-to-end
# ---------------------------------------------------------------------------


def test_format_meta_bridge() -> None:
    s = CuriosityState()
    s.organism = "BALANCE"
    q = _format_question(
        "meta_bridge:3:LATTICE_aperture->flatness_2x2_WP51", s, s
    )
    assert "LATTICE_aperture->flatness_2x2_WP51" in q, (
        f"bridge string missing from question: {q!r}"
    )
    print(f"PASS: meta_bridge formats: {q[:90]}")


def test_format_meta_op_gravity() -> None:
    s = CuriosityState()
    s.organism = "BALANCE"
    q = _format_question("meta_op_gravity:4:HARMONY", s, s)
    assert "HARMONY" in q, f"operator name missing from question: {q!r}"
    print(f"PASS: meta_op_gravity formats: {q[:90]}")


def test_format_meta_bridge_cold() -> None:
    s = CuriosityState()
    s.organism = "BALANCE"
    q = _format_question("meta_bridge_cold:4", s, s)
    assert "4" in q, f"n=4 should appear in question: {q!r}"
    print(f"PASS: meta_bridge_cold formats: {q[:90]}")


def test_format_degrades_gracefully_on_malformed_shift() -> None:
    """Malformed shift strings should not crash -- fallback sentence."""
    s = CuriosityState()
    s.organism = "BALANCE"
    # No context after prefix -- the template expects {bridge}, {n}, etc.
    q = _format_question("meta_bridge", s, s)
    assert q, "format should never return empty"
    print(f"PASS: malformed shift falls back: {q[:70]}")


# ---------------------------------------------------------------------------
# recent_questions dedup
# ---------------------------------------------------------------------------


def test_dedup_avoids_recent_repeats() -> None:
    """_format_question should avoid picking a template whose formatted
    string matches an entry in recent_questions when alternatives exist.

    We fire meta_op_gravity 100x; if every picked template had been
    consulted blindly, the same sentence would recur on most calls given
    a 4-5 entry bucket.  With recent_questions=[last_q] dedup, two
    consecutive calls should almost never produce the same sentence.
    """
    s = CuriosityState()
    s.organism = "BALANCE"
    prev_q = None
    repeats = 0
    for _ in range(100):
        q = _format_question("meta_op_gravity:4:HARMONY", s, s,
                             recent_questions=[prev_q] if prev_q else None)
        if q == prev_q:
            repeats += 1
        prev_q = q
    # With 3 tries across a bucket of 4+ templates, probability of
    # forcing a repeat (all 3 picks hit the same sentence) is tiny.
    # Allow a generous ceiling to avoid flakiness on small buckets.
    assert repeats <= 5, (
        f"dedup failed: {repeats}/100 back-to-back repeats (expected <=5)"
    )
    print(f"PASS: recent_questions dedup holds repeats to {repeats}/100")


def test_dedup_backward_compatible_without_param() -> None:
    """Callers that don't pass recent_questions still get a valid
    single pick (no crash, no repeat-loop overhead)."""
    s = CuriosityState()
    s.organism = "BALANCE"
    q = _format_question("meta_op_gravity:4:HARMONY", s, s)
    assert q and "HARMONY" in q, f"legacy call form broken: {q!r}"
    print("PASS: _format_question still works without recent_questions kwarg")


def main() -> int:
    tests = [
        test_bridge_streak_fires_on_3_of_5,
        test_op_gravity_fires_on_4_of_5,
        test_bridge_cold_fires_on_4_empty,
        test_no_false_positives_on_varied_signal,
        test_short_history_returns_none,
        test_priority_bridge_beats_op,
        test_format_meta_bridge,
        test_format_meta_op_gravity,
        test_format_meta_bridge_cold,
        test_format_degrades_gracefully_on_malformed_shift,
        test_dedup_avoids_recent_repeats,
        test_dedup_backward_compatible_without_param,
    ]
    failed = 0
    for t in tests:
        try:
            t()
        except AssertionError as e:
            print(f"FAIL: {t.__name__}: {e}")
            failed += 1
        except Exception as e:
            print(f"ERROR: {t.__name__}: {type(e).__name__}: {e}")
            failed += 1
    if failed == 0:
        print(f"\nAll {len(tests)} tests PASSED")
        return 0
    else:
        print(f"\n{failed}/{len(tests)} tests FAILED")
        return 1


if __name__ == "__main__":
    sys.exit(main())
