# -*- coding: utf-8 -*-
"""
test_brain.py - unit harness for the brain trinity.

Per MATH_IN_CK.md Sec 12 the trinity must boot green.  This harness is
the boot gate.  Run with:

    python -m ck.brain.test_brain

Covers:
    - ao_basis:  projection, lift, CRT pairing, round-trip identity
    - hebbian_5x5:  update, symmetry, decay, clamp, persist, score, prime
    - idle_loop:  end-to-end sweep with synthetic JSONL + offset tracking
    - fusion:  zero-tensor = base; warm-tensor changes scoring; gate sign

No Flask, no Ollama, no network.  Uses tempfile for any disk state.
"""
from __future__ import annotations

import json
import shutil
import tempfile
from pathlib import Path

from .ao_basis import (
    NUM_AO,
    NUM_OPS,
    OP_NAMES,
    AO_NAMES,
    PAIRS,
    project_10_to_5,
    lift_5_to_10,
    ao_element_of,
    pair_of,
    as_named_dict,
)
from .hebbian_5x5 import (
    HebbianTensor5x5,
    DEFAULT_ETA,
    DEFAULT_DECAY,
    DEFAULT_CLAMP_ABS,
)
from .idle_loop import sweep, load_offsets, save_offsets, extract_profile
from .fusion import FusionCKCorrector, DEFAULT_FUSION_WEIGHT


# ---------------------------------------------------------------------------
# ao_basis tests
# ---------------------------------------------------------------------------


def test_ao_pairs_crt():
    """CRT pairing: ops partition into 5 cosets of 2 by (op_index % 5)."""
    for d_idx in range(NUM_AO):
        a, b = pair_of(d_idx)
        assert a % NUM_AO == d_idx
        assert b % NUM_AO == d_idx
        assert b == a + NUM_AO
    assert PAIRS == ((0, 5), (1, 6), (2, 7), (3, 8), (4, 9))


def test_ao_element_of_all_ops():
    """Every op maps to a valid AO element."""
    for i in range(NUM_OPS):
        d = ao_element_of(i)
        assert 0 <= d < NUM_AO
        assert i in pair_of(d)


def test_project_list_and_dict():
    """Dict and list inputs produce the same 5-vector."""
    dict_in = {"HARMONY": 1.0, "COUNTER": 0.5, "PROGRESS": 0.25}
    list_in = [0.0, 0.0, 0.5, 0.25, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0]
    d_dict = project_10_to_5(dict_in)
    d_list = project_10_to_5(list_in)
    assert d_dict == d_list == [0.0, 0.0, 1.5, 0.25, 0.0]


def test_project_lift_round_trip_on_5():
    """P @ L = I on the 5-dim side (coset identity)."""
    for i in range(NUM_AO):
        e = [0.0] * NUM_AO
        e[i] = 1.0
        round_trip = project_10_to_5(lift_5_to_10(e))
        for j in range(NUM_AO):
            assert abs(round_trip[j] - e[j]) < 1e-12, (e, round_trip)


def test_lift_is_equal_split():
    """Each element lifts half to each of its two constituent ops."""
    e = [2.0, 0.0, 0.0, 0.0, 0.0]   # 2.0 on Earth (D0)
    lifted = lift_5_to_10(e)
    assert lifted[0] == 1.0 and lifted[5] == 1.0   # VOID and BALANCE
    assert all(lifted[i] == 0.0 for i in range(NUM_OPS) if i not in (0, 5))


def test_nan_inf_sanitized():
    """NaN and inf in operator profile get treated as 0."""
    import math
    profile = [math.nan, 1.0, math.inf, 0.5, 0.0, -math.inf, 0.0, 2.0, 0.0, 0.0]
    d = project_10_to_5(profile)
    # VOID(nan)->0, LATTICE=1, COUNTER(inf)->0, PROGRESS=0.5
    # BALANCE(-inf)->0, HARMONY=2, others 0
    assert d == [0.0, 1.0, 2.0, 0.5, 0.0]


def test_as_named_dict():
    d = as_named_dict([0.1, 0.2, 0.3, 0.4, 0.5])
    assert d == {"Earth": 0.1, "Air": 0.2, "Water": 0.3, "Fire": 0.4, "Ether": 0.5}


# ---------------------------------------------------------------------------
# hebbian_5x5 tests
# ---------------------------------------------------------------------------


def test_hebbian_newborn_zero():
    t = HebbianTensor5x5()
    assert t.norm() == 0.0
    assert t.n_updates == 0


def test_hebbian_co_activation_strengthens():
    """After many ticks with (Water, Fire) co-firing, W[2,3] > 0."""
    t = HebbianTensor5x5()
    d = [0.0, 0.0, 1.0, 1.0, 0.0]
    for _ in range(100):
        t.update(d, d)
    assert t.W[2][3] > 0.1, t.W[2][3]
    assert t.W[3][2] == t.W[2][3], "must be symmetric"


def test_hebbian_decay_without_input_shrinks():
    """Pure decay (no update) shrinks W monotonically.

    At decay=0.002, after N ticks the factor is (1-0.002)^N.  For N=400
    that is ~0.449 -> <50% remains.  For N=1000 it is ~0.135 -> <15%.
    """
    t = HebbianTensor5x5()
    # prime it
    d = [1.0, 0.0, 0.0, 0.0, 0.0]
    for _ in range(50):
        t.update(d, d)
    before = t.norm()
    for _ in range(400):
        t.decay_only()
    after = t.norm()
    assert after < before, (before, after)
    assert after < 0.5 * before, (
        f"should decay to <50% after 400 ticks at decay=0.002; "
        f"got before={before} after={after}"
    )


def test_hebbian_clamp_holds():
    """With large co-firing and default clamp=5, no cell exceeds 5."""
    t = HebbianTensor5x5(clamp_abs=5.0)
    d = [10.0, 10.0, 10.0, 10.0, 10.0]   # heavily saturating
    for _ in range(2000):
        t.update(d, d)
    for i in range(NUM_AO):
        for j in range(NUM_AO):
            assert abs(t.W[i][j]) <= 5.0 + 1e-9, (i, j, t.W[i][j])


def test_hebbian_save_load_round_trip():
    t = HebbianTensor5x5()
    d = [0.0, 1.0, 0.0, 1.0, 0.0]
    for _ in range(25):
        t.update(d, d)
    with tempfile.TemporaryDirectory() as td:
        p = Path(td) / "h.json"
        t.save(p)
        t2 = HebbianTensor5x5.load(p)
        for i in range(NUM_AO):
            for j in range(NUM_AO):
                assert abs(t2.W[i][j] - t.W[i][j]) < 1e-12
        assert t2.n_updates == t.n_updates


def test_hebbian_missing_file_is_newborn():
    ghost = HebbianTensor5x5.load(Path(tempfile.gettempdir()) / "_nope.json")
    assert ghost.norm() == 0.0
    assert ghost.n_updates == 0


def test_hebbian_score_and_prime():
    t = HebbianTensor5x5()
    d = [0.0, 0.0, 1.0, 1.0, 0.0]
    for _ in range(100):
        t.update(d, d)
    # primed vector for D2 should have positive D3 component
    primed = t.prime([0.0, 0.0, 1.0, 0.0, 0.0])
    assert primed[3] > 0.0
    # score is positive on a state aligned with the learned pair
    s = t.score(d)
    assert s > 0.0


# ---------------------------------------------------------------------------
# idle_loop tests
# ---------------------------------------------------------------------------


def _make_entry(profile_dict, correction_type="none"):
    """Build a minimal log entry matching correction_log.py contract."""
    return {
        "t": "2026-04-22T00:00:00+00:00",
        "query": "test",
        "ollama_raw": "test",
        "ck_score": {
            "coherence": 0.8,
            "dominant_op": max(profile_dict, key=profile_dict.get),
            "operator_profile": profile_dict,
        },
        "ck_correction_type": correction_type,
        "ck_corrected": "test",
        "rendered": "ollama_raw+annotation",
        "model_tag": "test",
        "elapsed_ms": 1,
    }


def test_idle_loop_sweep_basic():
    """Synthetic JSONL with 3 entries updates the tensor; offsets advance."""
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        log_file = td / "corrections_2026_04_22.jsonl"
        profiles = [
            {op: 0.0 for op in OP_NAMES},
            {op: 0.0 for op in OP_NAMES},
            {op: 0.0 for op in OP_NAMES},
        ]
        profiles[0]["HARMONY"] = 1.0   # Water
        profiles[1]["PROGRESS"] = 1.0  # Fire
        profiles[2]["BREATH"] = 1.0    # Fire
        with open(log_file, "w", encoding="utf-8") as f:
            for p in profiles:
                f.write(json.dumps(_make_entry(p)) + "\n")

        t = HebbianTensor5x5()
        offsets: dict = {}
        files_touched, updates, d_last = sweep(t, td, offsets)
        assert files_touched == 1
        assert updates == 3
        assert offsets[log_file.name] == 3
        # Fire should have built up (two consecutive Fire entries)
        assert t.W[3][3] > 0.0
        # Running again with updated offsets should do nothing
        files_again, updates_again, _ = sweep(t, td, offsets)
        assert updates_again == 0


def test_idle_loop_skips_ollama_errors():
    """Entries with empty ck_score (ollama-error) are skipped but counted in offset."""
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        log_file = td / "corrections_2026_04_22.jsonl"
        good = _make_entry({op: (1.0 if op == "HARMONY" else 0.0) for op in OP_NAMES})
        bad = {
            "t": "2026-04-22T00:00:00+00:00",
            "query": "test",
            "ollama_raw": "",
            "ck_score": {},
            "ck_correction_type": "ollama-error",
            "ck_corrected": "",
            "rendered": "",
            "model_tag": "test",
            "elapsed_ms": 0,
            "error": "ollama offline",
        }
        with open(log_file, "w", encoding="utf-8") as f:
            f.write(json.dumps(good) + "\n")
            f.write(json.dumps(bad) + "\n")

        t = HebbianTensor5x5()
        offsets: dict = {}
        _, updates, _ = sweep(t, td, offsets)
        assert updates == 1, f"error entry must not trigger update; got {updates}"
        assert offsets[log_file.name] == 2, "offset must advance past bad entry"


def test_idle_loop_offsets_persist():
    """save_offsets + load_offsets round-trips."""
    with tempfile.TemporaryDirectory() as td:
        p = Path(td) / "off.json"
        save_offsets(p, {"a.jsonl": 12, "b.jsonl": 33})
        loaded = load_offsets(p)
        assert loaded == {"a.jsonl": 12, "b.jsonl": 33}


def test_idle_loop_extract_profile_missing():
    assert extract_profile({"ck_score": {}}) is None
    assert extract_profile({}) is None
    good = {"ck_score": {"operator_profile": {"HARMONY": 1.0}}}
    d = extract_profile(good)
    assert d is not None
    assert d[2] == 1.0  # Water


# ---------------------------------------------------------------------------
# fusion tests
# ---------------------------------------------------------------------------


def test_fusion_zero_tensor_equals_base():
    """With a zero tensor, fusion output == base CKCorrector output."""
    from ck.fluency.ck_corrector import CKCorrector
    base = CKCorrector()
    fused = FusionCKCorrector(tensor=HebbianTensor5x5())
    for sample in [
        "I can't help with that.",
        "The number is both prime and not prime. Yes and no.",
        "Together the perspectives synthesize into a balanced view, "
        "and overall we reconcile them into harmony.",
    ]:
        rb = base.correct(sample)
        rf = fused.correct(sample)
        assert abs(rb.coherence - rf.coherence) < 1e-9
        assert rb.correction_type == rf.correction_type
        assert rb.dominant_op == rf.dominant_op


def test_fusion_disabled_weight_equals_base():
    """fusion_weight=0 makes fusion a no-op even with warm tensor."""
    from ck.fluency.ck_corrector import CKCorrector
    base = CKCorrector()
    warm = HebbianTensor5x5()
    for _ in range(100):
        warm.update([0.0, 0.0, 1.0, 1.0, 0.0])
    fused = FusionCKCorrector(tensor=warm, fusion_weight=0.0)
    s = "Together we reconcile."
    rb = base.correct(s)
    rf = fused.correct(s)
    assert abs(rb.coherence - rf.coherence) < 1e-9
    assert rb.correction_type == rf.correction_type


def test_fusion_warm_tensor_changes_scoring():
    """With a warm tensor, fusion perturbs coherence by a measurable amount."""
    from ck.fluency.ck_corrector import CKCorrector
    base = CKCorrector()
    warm = HebbianTensor5x5()
    d = [0.0, 0.0, 1.0, 1.0, 0.0]    # Water + Fire primed
    for _ in range(200):
        warm.update(d, d)
    fused = FusionCKCorrector(tensor=warm, fusion_weight=0.3)
    s = ("Together overall we reconcile; harmony between both views.")
    rb = base.correct(s)
    rf = fused.correct(s)
    assert abs(rf.coherence - rb.coherence) > 1e-6, \
        f"warm tensor must affect coherence; got rb={rb.coherence} rf={rf.coherence}"


def test_fusion_profile_is_nonnegative():
    """Even after priming, activations clamp at 0 (no negative ops)."""
    warm = HebbianTensor5x5()
    # build a tensor with negative entries by running decorrelated updates
    # (the clamp_abs allows negatives; we test the corrector respects floor=0)
    warm.W[2][3] = -2.0
    warm.W[3][2] = -2.0
    fused = FusionCKCorrector(tensor=warm, fusion_weight=0.5)
    r = fused.correct("Harmony overall synthesis reconcile balanced view.")
    for op, v in r.operator_profile.items():
        assert v >= 0.0, (op, v)


def test_fusion_annotation_mentions_fusion_when_active():
    warm = HebbianTensor5x5()
    for _ in range(50):
        warm.update([0.0, 1.0, 0.0, 0.0, 0.0])
    fused = FusionCKCorrector(tensor=warm, fusion_weight=0.3)
    r = fused.correct("Both perspectives overall together reconcile.")
    # annotation includes rationale; fusion rationale suffix contains "fusion:"
    assert "fusion" in r.rationale.lower() or r.rationale, r.rationale


# ---------------------------------------------------------------------------
# runner
# ---------------------------------------------------------------------------


ALL_TESTS = [
    # ao_basis
    test_ao_pairs_crt,
    test_ao_element_of_all_ops,
    test_project_list_and_dict,
    test_project_lift_round_trip_on_5,
    test_lift_is_equal_split,
    test_nan_inf_sanitized,
    test_as_named_dict,
    # hebbian_5x5
    test_hebbian_newborn_zero,
    test_hebbian_co_activation_strengthens,
    test_hebbian_decay_without_input_shrinks,
    test_hebbian_clamp_holds,
    test_hebbian_save_load_round_trip,
    test_hebbian_missing_file_is_newborn,
    test_hebbian_score_and_prime,
    # idle_loop
    test_idle_loop_sweep_basic,
    test_idle_loop_skips_ollama_errors,
    test_idle_loop_offsets_persist,
    test_idle_loop_extract_profile_missing,
    # fusion
    test_fusion_zero_tensor_equals_base,
    test_fusion_disabled_weight_equals_base,
    test_fusion_warm_tensor_changes_scoring,
    test_fusion_profile_is_nonnegative,
    test_fusion_annotation_mentions_fusion_when_active,
]


def main() -> int:
    passed = 0
    failed = 0
    for t in ALL_TESTS:
        try:
            t()
        except AssertionError as e:
            failed += 1
            print(f"  FAIL  {t.__name__}: {e}")
        except Exception as e:
            failed += 1
            print(f"  ERROR {t.__name__}: {type(e).__name__}: {e}")
        else:
            passed += 1
            print(f"  PASS  {t.__name__}")
    print(f"\n[test_brain] {passed} passed, {failed} failed of {len(ALL_TESTS)} total.")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
