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
    _detect_shift,
    _format_question,
    CuriosityState,
    _CuriosityDaemon,
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


# ---------------------------------------------------------------------------
# hydrate-from-disk session continuity
# ---------------------------------------------------------------------------


def test_hydrate_preserves_last_tick_suppresses_first_observation() -> None:
    """After hydrating prior entries, the next _detect_shift call must
    NOT return 'first_observation'.  This locks the restart-continuity
    fix: a daemon reboot is not CK's first observation of himself.
    """
    import json
    import tempfile
    import time
    import ck_curiosity as _cc

    # Point the daemon's persistence path at a tmp file with one fake
    # prior entry, then construct a daemon and assert post-hydrate state
    # has last_tick != 0.0 (the sentinel value that triggers
    # first_observation).
    tmp_dir = tempfile.mkdtemp(prefix="ck_curiosity_test_")
    tmp_path = os.path.join(tmp_dir, "curiosity_history.json")
    prior_ts = int(time.time()) - 300  # 5 min ago
    fake_blob = {
        "saved_at": prior_ts,
        "count": 1,
        "entries": [{
            "ts": prior_ts,
            "shift": "idle:180s@BALANCE",
            "question": "what's the texture of my rest?",
            "answer": "a quiet plateau.",
            "source": "math_first",
            "coherence": 0.82,
            "gate_pass": True,
            "dominant_op": "BALANCE",
            "organism": "BALANCE",
            "bridges": ["HARMONY->TSML_synthesis_arc_73_cells"],
            "dt_ms": 120,
        }],
    }
    with open(tmp_path, "w", encoding="utf-8") as f:
        json.dump(fake_blob, f)

    # Monkey-patch the module path so the daemon hydrates from our tmp.
    old_path = _cc._CURIOSITY_HISTORY_PATH
    try:
        _cc._CURIOSITY_HISTORY_PATH = tmp_path

        class _StubEngine:
            sensorium = None
        d = _cc._CuriosityDaemon(
            api=None, engine=_StubEngine(), period=60.0,
            session_id="ck_test_hydrate",
        )
    finally:
        _cc._CURIOSITY_HISTORY_PATH = old_path

    assert len(d.history) == 1, (
        f"hydrate should load 1 entry, got {len(d.history)}"
    )
    assert d.state.last_tick == float(prior_ts), (
        f"last_tick not restored: got {d.state.last_tick}, "
        f"expected {prior_ts}"
    )
    assert d.state.organism == "BALANCE", (
        f"prev organism not restored: {d.state.organism!r}"
    )
    # Now simulate the next tick's detect_shift call with prev=d.state
    # and a cur that matches prev -- no real shift.  Must NOT return
    # 'first_observation'.
    cur = CuriosityState()
    cur.organism = "BALANCE"
    cur.coherence = 0.82
    cur.active_layers = d.state.active_layers
    cur.last_tick = time.time()
    shift = _detect_shift(d.state, cur)
    assert shift != "first_observation", (
        f"hydrated daemon still fires first_observation: {shift!r}"
    )
    # Recent windows should be populated from the one hydrated entry.
    assert list(d.recent_kinds) == ["idle"], (
        f"recent_kinds not rehydrated: {list(d.recent_kinds)!r}"
    )
    assert list(d.recent_dom_ops) == ["BALANCE"], (
        f"recent_dom_ops not rehydrated: {list(d.recent_dom_ops)!r}"
    )
    assert list(d.recent_bridges) == [
        ["HARMONY->TSML_synthesis_arc_73_cells"]
    ], f"recent_bridges not rehydrated: {list(d.recent_bridges)!r}"
    print("PASS: hydrate preserves last_tick + organism + meta-windows; "
          "no spurious first_observation after restart")


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
        test_hydrate_preserves_last_tick_suppresses_first_observation,
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
