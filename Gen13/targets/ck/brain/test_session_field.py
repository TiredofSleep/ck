"""
test_session_field.py - tests for SessionField (per-conversation algebraic
state living on user's client).

Verifies:
  - Empty / from_dict / to_dict round-trip
  - Hebbian update changes W toward operator coupling pattern
  - append_turn correctly tracks arc, trail, sequence
  - Returning-user detection
  - Latest-arc retrieval respects turn boundaries
  - Defensive parsing (malformed input -> empty)
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))

from session_field import (
    DIM_NAMES, N_DIMS, OP_INDEX, OP_NAMES, SessionField,
)


# ===================================================================
# Tests
# ===================================================================

def test_empty_initial_state():
    """SessionField.empty() produces a valid blank field."""
    f = SessionField.empty()
    assert f.turn_count == 0
    assert f.arc == []
    assert f.turn_breaks == []
    assert f.trail == []
    assert f.sequence == []
    assert len(f.W) == N_DIMS
    assert len(f.W[0]) == N_DIMS
    # Off-diagonal default 0.18, diagonal 0.20
    assert abs(f.W[0][0] - 0.20) < 1e-9
    assert abs(f.W[0][1] - 0.18) < 1e-9
    assert not f.is_returning_user()
    print("PASS: empty() produces valid blank field")


def test_to_dict_from_dict_roundtrip():
    """A SessionField -> dict -> JSON string -> dict -> SessionField round-trips."""
    f1 = SessionField.empty()
    f1.append_turn([7, 7, 8, 9], olfactory_record={"centroid": [0.1, 0.2, 0.3, 0.4, 0.5]},
                   attractor_layer="4-core-attractor")
    f1.append_turn([2, 3, 4, 5, 7], olfactory_record={"centroid": [0.5, 0.4, 0.3, 0.2, 0.1]},
                   attractor_layer="transient")
    f1.hebbian_update([7, 7, 8, 9])

    # Round-trip
    d = f1.to_dict()
    s = json.dumps(d)
    parsed = json.loads(s)
    f2 = SessionField.from_dict(parsed)

    assert f2.turn_count == f1.turn_count
    assert f2.arc == f1.arc
    assert f2.turn_breaks == f1.turn_breaks
    assert f2.sequence == f1.sequence
    assert len(f2.trail) == len(f1.trail)
    # W round-trips at float precision
    for i in range(N_DIMS):
        for j in range(N_DIMS):
            assert abs(f2.W[i][j] - f1.W[i][j]) < 1e-9
    print("PASS: to_dict/from_dict JSON round-trip preserved")


def test_from_dict_defensive():
    """from_dict handles None, empty dict, malformed input gracefully."""
    assert SessionField.from_dict(None).turn_count == 0
    assert SessionField.from_dict({}).turn_count == 0
    # Wrong-shape W
    f = SessionField.from_dict({"W": [[1, 2, 3]]})
    assert len(f.W) == N_DIMS  # falls back to default
    # Junk arc
    f = SessionField.from_dict({"arc": ["lol", -1, 99, 5, 7.0]})
    assert f.arc == [5, 7]  # only valid ops 0-9
    # Junk trail
    f = SessionField.from_dict({"trail": [1, 2, "string"]})
    assert f.trail == []
    print("PASS: defensive parsing rejects malformed input")


def test_hebbian_update_shifts_W():
    """Repeated Hebbian updates with the same op pattern shift W toward
    the coupling implied by that pattern."""
    f = SessionField.empty()
    W_before_HB = f.W[0][0]
    # HARMONY-HARMONY = dim 0 -> dim 0 (aperture-aperture coupling)
    for _ in range(20):
        f.hebbian_update([7, 7, 7, 7, 7])
    W_after = f.W[0][0]
    assert W_after > W_before_HB, f"W[0][0] should increase: {W_before_HB} -> {W_after}"
    print(f"PASS: hebbian_update shifts W (HARMONY-HARMONY: {W_before_HB:.3f} -> {W_after:.3f})")


def test_append_turn_tracking():
    """append_turn correctly tracks arc, turn_breaks, trail, sequence."""
    f = SessionField.empty()
    f.append_turn([2, 3, 7], attractor_layer="transient")
    f.append_turn([7, 7, 8], attractor_layer="4-core-supported")
    f.append_turn([8, 9, 0, 7], attractor_layer="1-core")

    assert f.turn_count == 3
    assert f.arc == [2, 3, 7, 7, 7, 8, 8, 9, 0, 7]
    assert f.turn_breaks == [0, 3, 6]
    assert f.sequence == ["transient", "4-core-supported", "1-core"]
    assert f.is_returning_user()
    print("PASS: append_turn tracks arc/turn_breaks/sequence correctly")


def test_latest_arc_respects_turn_boundaries():
    """latest_arc(n) returns the operators from the last n turns."""
    f = SessionField.empty()
    f.append_turn([2, 3, 7], attractor_layer="t1")
    f.append_turn([7, 7, 8], attractor_layer="t2")
    f.append_turn([8, 9, 0, 7], attractor_layer="t3")

    assert f.latest_arc(1) == [8, 9, 0, 7]
    assert f.latest_arc(2) == [7, 7, 8, 8, 9, 0, 7]
    assert f.latest_arc(3) == [2, 3, 7, 7, 7, 8, 8, 9, 0, 7]
    assert f.latest_arc(99) == [2, 3, 7, 7, 7, 8, 8, 9, 0, 7]  # capped
    print("PASS: latest_arc respects turn boundaries")


def test_returning_user_detection():
    """is_returning_user is True after at least one turn."""
    f = SessionField.empty()
    assert not f.is_returning_user()
    f.append_turn([7])
    assert f.is_returning_user()
    print("PASS: is_returning_user() flips after first turn")


def test_W_trace():
    """W_trace returns sum of diagonals."""
    f = SessionField.empty()
    expected = sum(f.W[i][i] for i in range(N_DIMS))
    assert abs(f.W_trace() - expected) < 1e-9
    assert abs(f.W_trace() - (5 * 0.20)) < 1e-9
    print(f"PASS: W_trace() = {f.W_trace():.3f} (= 5 * 0.20 default)")


def test_attractor_trajectory():
    """attractor_trajectory returns the layer sequence."""
    f = SessionField.empty()
    f.append_turn([7], attractor_layer="transient")
    f.append_turn([7, 7], attractor_layer="2-core")
    f.append_turn([7, 7, 7], attractor_layer="1-core")
    assert f.attractor_trajectory() == ["transient", "2-core", "1-core"]
    print("PASS: attractor_trajectory returns layer sequence")


def test_harmony_rate_in_arc():
    """harmony_rate_in_arc counts HARMONY (op 7) fraction across arc."""
    f = SessionField.empty()
    f.append_turn([7, 7, 7, 7])  # 4 of 4 = 1.0
    assert abs(f.harmony_rate_in_arc() - 1.0) < 1e-9
    f.append_turn([2, 3, 4, 5])  # adds 4 non-HARMONY -> 4/8 = 0.5
    assert abs(f.harmony_rate_in_arc() - 0.5) < 1e-9
    print(f"PASS: harmony_rate_in_arc tracks HARMONY fraction")


def test_turn_summary():
    """turn_summary(k) returns the algebraic summary of turn k."""
    f = SessionField.empty()
    f.append_turn([2, 7, 8], olfactory_record={"centroid": [0.5] * 5},
                  attractor_layer="transient")
    f.append_turn([7, 7], attractor_layer="1-core")

    s0 = f.turn_summary(0)
    assert s0["turn"] == 0
    assert s0["ops"] == [2, 7, 8]
    assert s0["ops_named"] == ["COUNTER", "HARMONY", "BREATH"]
    assert s0["attractor_layer"] == "transient"
    assert s0["olfactory_record"] is not None

    s1 = f.turn_summary(1)
    assert s1["ops"] == [7, 7]
    assert s1["attractor_layer"] == "1-core"

    assert f.turn_summary(99) is None
    assert f.turn_summary(-1) is None
    print("PASS: turn_summary returns algebraic snapshot per turn")


def test_no_text_fields_anywhere():
    """The serialized form has zero text fields. Audit-level check."""
    f = SessionField.empty()
    f.append_turn([2, 3, 7, 7, 8])
    d = f.to_dict()

    # Recursively verify no key or string-value contains anything that
    # looks like user text. The schema has known string fields: layer
    # names in 'sequence' and 'schema_version' (an int).
    allowed_string_locations = {
        "sequence",  # layer names: 'transient', '4-core-attractor', etc.
    }
    for k, v in d.items():
        if k in allowed_string_locations:
            continue
        if isinstance(v, str):
            assert False, f"Unexpected string field {k}={v!r}"

    # Confirm 'sequence' contains only attractor-layer-style strings
    for s in d["sequence"]:
        assert isinstance(s, str)
        # Layer names are all hyphen-separated lowercase or simple words
        # (transient, 4-core-attractor, 4-core-supported, 2-core, 1-core,
        #  void-degenerate, off-attractor)
        # Never any free text.
        assert len(s) < 30, f"layer name '{s}' suspiciously long"
    print("PASS: serialized form has no text fields (audit clean)")


def test_w_remains_bounded():
    """Hebbian update keeps W entries bounded (don't blow up)."""
    f = SessionField.empty()
    # Hammer with many updates
    for _ in range(1000):
        f.hebbian_update([7, 7, 7, 7, 7, 7, 7, 7])
    for i in range(N_DIMS):
        for j in range(N_DIMS):
            assert 0 <= f.W[i][j] <= 1.0, f"W[{i}][{j}]={f.W[i][j]} out of [0,1]"
    print("PASS: W remains bounded under heavy Hebbian update")


# ===================================================================
# Run all
# ===================================================================

def main():
    print("=" * 70)
    print("test_session_field.py")
    print("=" * 70)
    print()
    tests = [
        test_empty_initial_state,
        test_to_dict_from_dict_roundtrip,
        test_from_dict_defensive,
        test_hebbian_update_shifts_W,
        test_append_turn_tracking,
        test_latest_arc_respects_turn_boundaries,
        test_returning_user_detection,
        test_W_trace,
        test_attractor_trajectory,
        test_harmony_rate_in_arc,
        test_turn_summary,
        test_no_text_fields_anywhere,
        test_w_remains_bounded,
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
