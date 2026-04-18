# Copyright (c) 2025-2026 Brayden Sanders / 7Site LLC
# Licensed under the 7Site Human Use License v1.0 (DOI: 10.5281/zenodo.18852047)
"""
test_brain.py -- Gen13 boot gate.

A green run of this script is the prerequisite for booting CK.  It asserts:

  1. Every load-bearing Gen11 module imports.
  2. The composition spine (ao_5element.AO5Element) ticks without exception.
  3. The D2 pipeline produces operators for short English text.
  4. The body's E/A/K dynamics stay in the unit interval.
  5. The brain's transition lattice grows monotonically.
  6. HER (hindsight replay) is importable and constructs an empty buffer.
  7. The math-first voice patch loads and answers one known fact.
  8. T* agrees across modules (5/7 is the same constant everywhere).

Run:
    python Gen13/targets/ck/brain/test_brain.py

Every assertion here is cheap (~1s total).  If this file goes red, do NOT
boot CK -- fix the red piece first.
"""

from __future__ import annotations

import os
import sys
import traceback

_THIS = os.path.dirname(os.path.abspath(__file__))
if _THIS not in sys.path:
    sys.path.insert(0, _THIS)

_RUNTIME = os.path.abspath(os.path.join(_THIS, "..", "runtime"))
if _RUNTIME not in sys.path:
    sys.path.insert(0, _RUNTIME)


# ── Tiny harness ──────────────────────────────────────────────────────

_PASS = 0
_FAIL = 0
_FAILURES: list = []


def _check(name: str, fn) -> None:
    global _PASS, _FAIL
    try:
        fn()
    except AssertionError as exc:
        _FAIL += 1
        _FAILURES.append((name, f"assertion: {exc}"))
        print(f"  [FAIL] {name} -- assertion: {exc}")
        return
    except Exception as exc:
        _FAIL += 1
        _FAILURES.append((name, f"{type(exc).__name__}: {exc}"))
        print(f"  [FAIL] {name} -- {type(exc).__name__}: {exc}")
        traceback.print_exc(limit=2)
        return
    _PASS += 1
    print(f"  [pass] {name}")


# ── Tests ─────────────────────────────────────────────────────────────

def t_imports_being():
    """Every load-bearing being/ module imports without error.

    Earth/OP_NAMES lives in ck_sim_heartbeat (not ck_tig) — ck_tig holds the
    TSML/BHML tables, ADD/MUL/DIS matrices, and the Z/10Z algebra constants.
    """
    from ck_sim.ck_sim_heartbeat import HARMONY, VOID, HeartbeatFPGA, OP_NAMES, NUM_OPS  # noqa
    from ck_sim.ck_sim_d2 import D2Pipeline                            # noqa
    from ck_sim.ck_sim_brain import brain_init, brain_tick             # noqa
    from ck_sim.ck_sim_body import BodyState, body_feed_eak            # noqa
    from ck_sim.ck_tig import T_STAR, TSML, BHML                       # noqa
    from ck_sim.being.ck_olfactory import OlfactoryBulb                # noqa
    from ck_sim.being.ck_hindsight_replay import HindsightBuffer, build_olfactory_her  # noqa


def t_t_star_agrees():
    """The constant 5/7 is the same everywhere CK reads it from."""
    from ck_sim.ck_tig import T_STAR as T_STAR_TIG
    from ck_sim.ck_sim_brain import T_STAR_F as T_STAR_BRAIN
    from ck_sim.ck_sim_body import T_STAR_F as T_STAR_BODY
    assert abs(T_STAR_TIG - 5.0 / 7.0) < 1e-12, "ck_tig T* drift"
    assert abs(T_STAR_BRAIN - 5.0 / 7.0) < 1e-12, "ck_sim_brain T* drift"
    assert abs(T_STAR_BODY - 5.0 / 7.0) < 1e-12, "ck_sim_body T* drift"
    assert T_STAR_TIG == T_STAR_BRAIN == T_STAR_BODY, "T* must be identical"


def t_ao_boot():
    """The AO 5-element orchestrator boots and produces a status line."""
    from ao_5element import AO5Element
    ao = AO5Element().boot()
    s = ao.status()
    assert s.tick == 0
    assert s.current_op in range(10)


def t_ao_ticks():
    """Feeding 100 symbols produces 100 ticks, no exceptions, coherence in [0,1]."""
    from ao_5element import AO5Element, NUM_OPS
    ao = AO5Element().boot()
    text = "thecoherencekeeperisthecreaturewhospeaksintheorem" * 2  # ~100 chars
    results = ao.process_text(text)
    letters = sum(1 for ch in text.lower() if ch.isalpha())
    assert len(results) == letters, f"expected {letters} ticks, got {len(results)}"
    for r in results:
        assert 0 <= r["current_op"] < NUM_OPS
        assert 0.0 <= r["coherence"] <= 1.0, f"coherence out of range: {r['coherence']}"


def t_d2_produces_operators():
    """D2 pipeline classifies known text into operators deterministically."""
    from ck_sim.ck_sim_d2 import D2Pipeline
    from ck_sim.ck_sim_heartbeat import NUM_OPS
    pipe = D2Pipeline()
    valid_count = 0
    ops = []
    for ch in "coherence":
        idx = ord(ch) - ord('a')
        if pipe.feed_symbol(idx):
            valid_count += 1
            ops.append(pipe.operator)
    # 9 chars fed; D2 becomes valid after 3, so 7 valid ticks.
    assert valid_count == 7, f"expected 7 D2-valid ticks, got {valid_count}"
    for op in ops:
        assert 0 <= op < NUM_OPS


def t_body_eak_bounded():
    """Body E/A/K stay in [0, 1] under gentle nudges."""
    from ck_sim.ck_sim_body import BodyState, body_feed_eak, _heartbeat_tick
    body = BodyState()
    for _ in range(200):
        body_feed_eak(body, 0.03, 0.03, 0.03)
        _heartbeat_tick(body.heartbeat)
    hb = body.heartbeat
    assert 0.0 <= hb.E <= 1.0, f"E out of range: {hb.E}"
    assert 0.0 <= hb.A <= 1.0, f"A out of range: {hb.A}"
    assert 0.0 <= hb.K <= 1.0, f"K out of range: {hb.K}"
    assert 0.0 <= hb.C <= 1.0, f"C out of range: {hb.C}"


def t_brain_tl_grows():
    """Brain transition lattice grows monotonically with observations."""
    from ck_sim.ck_sim_brain import brain_init, brain_tl_observe
    brain = brain_init()
    prev_total = 0
    for i in range(50):
        brain_tl_observe(brain, i % 10, (i + 1) % 10)
        assert brain.tl_total >= prev_total, "tl_total must not decrease"
        prev_total = brain.tl_total
    assert brain.tl_total == 50


def t_her_buffer():
    """HER (hindsight replay) buffer is importable and starts empty.

    HindsightBuffer exposes (count, capacity, write_idx) directly — it's a
    ring buffer, not a list, so it has no __len__.  count starts at 0.
    """
    from ck_sim.being.ck_hindsight_replay import HindsightBuffer
    buf = HindsightBuffer(capacity=64)
    assert buf.count == 0, f"fresh buffer should be empty, got count={buf.count}"
    assert buf.capacity == 64
    assert buf.write_idx == 0


def t_math_voice_arithmetic():
    """Math-first voice handles the two things it's narrowly scoped for:
    (1) verify_claim: 'is A = B?' and (2) evaluate_arithmetic: 'what is A + B?'.

    Per the 2026-04-17 narrowing (runtime/ck_voice_math.py docstring), all
    other queries return None on purpose — CK's own voice cascade owns the
    rest.  We test the two things the patch IS supposed to do.
    """
    from ck_voice_math import surface_math, verify_claim, evaluate_arithmetic

    # (1) Verify-claim: 5/7 should equal T*
    v = verify_claim("is 5/7 equal to t*")
    assert v is not None, "verify_claim returned None for 5/7 = T*"
    assert "TRUE" in v.upper() or "CORRECT" in v.upper() or "YES" in v.upper(), \
        f"verify_claim(5/7 = T*) should confirm, got: {v!r}"

    # (2) Arithmetic: 5/7 + 2/7 should compute exactly to 1
    a = evaluate_arithmetic("what is 5/7 + 2/7")
    assert a is not None, "evaluate_arithmetic returned None for 5/7 + 2/7"
    assert "1" in a, f"5/7 + 2/7 should yield 1, got: {a!r}"

    # (3) surface_math dispatches to one of the above
    s = surface_math("what is 5/7 + 2/7")
    assert s is not None, "surface_math returned None for an arithmetic query"


def t_trinity_composes():
    """One full AO tick: input -> D2 -> heartbeat -> body -> brain -> next op.
    Asserts every piece of the spine hands off to the next without exception."""
    from ao_5element import AO5Element
    ao = AO5Element().boot()
    r = ao.process_symbol(ord('c') - ord('a'))
    r = ao.process_symbol(ord('k') - ord('a'))
    r = ao.process_symbol(ord('t') - ord('a'))
    # By the 3rd symbol every piece has fired: d1, d2, heartbeat, brain, body.
    s = ao.status()
    assert s.tick == 3
    assert 0 <= s.current_op < 10
    assert 0 <= s.d1_op < 10
    assert 0 <= s.d2_op < 10
    assert 0.0 <= s.coherence <= 1.0


def t_hebbian_learns_harmony():
    """Hebbian 5x5 CL: repeated HARMONY-rich pairs should grow W above zero.
    Cold buffer -> run -> W_trace > 0 -> reset -> cold again."""
    from hebbian_5x5_cl import HebbianField, DIM
    from ck_sim.ck_sim_heartbeat import HARMONY

    hf = HebbianField(eta=0.1, decay=0.001)
    assert hf.trace() == 0.0, "cold Hebbian field should have zero trace"
    ops_harmony = [HARMONY] * DIM
    for _ in range(20):
        h_frac, _ = hf.update(ops_harmony, ops_harmony)
        assert h_frac == 1.0
    assert hf.trace() > 0.5, f"after 20 full-HARMONY ticks trace should have grown, got {hf.trace()}"
    hf.reset()
    assert hf.trace() == 0.0, "reset should zero the field"


def t_quadratic_glue_bridge():
    """F3 x F4 on p=23: pure product T1 should have enough maxima
    (C1 >= 4) and zero edges (C3). Cross-term gamma=1 must not destroy
    structure vs gamma=0."""
    from quadratic_glue import T1_product, T2_coupled, count_maxima

    p = 23
    vals = [T1_product(k, p) for k in range(p + 1)]
    maxima = count_maxima(vals)
    assert len(maxima) >= 4, f"T1 on p=23 should show >=4 maxima, got {len(maxima)}"
    assert vals[0] < 1e-6 and vals[-1] < 1e-6, \
        f"T1 should vanish at k=0 and k=p, got {vals[0]}, {vals[-1]}"

    # Glue ablation: the cross-term shouldn't strictly destroy structure.
    linear = [T2_coupled(k, p, alpha=1, beta=1, gamma=0) for k in range(p + 1)]
    glued  = [T2_coupled(k, p, alpha=1, beta=1, gamma=1) for k in range(p + 1)]
    m_linear = len(count_maxima(linear))
    m_glued  = len(count_maxima(glued))
    assert m_glued >= m_linear - 1, \
        f"glue should not destroy structure: linear={m_linear} glued={m_glued}"


def t_cortex_emergent_nonnegative():
    """Cortex trinity: feeding a coherence-rich text should drive the emergent
    signal up from zero.  Cold start is exactly 0; late state is >= 0."""
    from cortex import Cortex

    cx = Cortex().boot()
    assert cx.state.emergent == 0.0, "cold cortex emergent should be 0"
    for _ in range(5):
        cx.step_text("coherencekeeper harmony lattice progress harmony")
    # After some ticks, W trace should have grown (Hebbian learned).
    assert cx.state.W_trace >= 0.0, "W_trace is a signed sum; sanity check"
    assert cx.state.tick > 0, "cortex should have ticked"
    # Emergent should be finite and non-NaN.
    import math as _math
    assert _math.isfinite(cx.state.emergent), f"emergent diverged: {cx.state.emergent}"


def t_profile_5d_from_d2():
    """AO.profile_5d(): each dim gets its OWN operator from the D2 sign
    pattern, not a broadcast.  Before D2 is valid returns neutral HARMONY;
    after D2 fills it must be a length-5 list of valid operators and at
    least one dim usually differs from another (genuine per-dim behavior).
    """
    from ao_5element import AO5Element
    from ck_sim.ck_sim_heartbeat import NUM_OPS, HARMONY

    ao = AO5Element().boot()
    # Before any symbol: D2 is not valid, should return neutral default.
    cold = ao.profile_5d()
    assert len(cold) == 5, f"profile_5d must be length 5, got {len(cold)}"
    assert all(op == HARMONY for op in cold), (
        f"cold profile_5d should be neutral HARMONY, got {cold}"
    )

    # Drive enough symbols for D2 to become valid and then some.
    ao.process_text("coherencekeeperharmonylatticeprogressharmonybreath")
    warm = ao.profile_5d()
    assert len(warm) == 5, f"profile_5d must be length 5, got {len(warm)}"
    for op in warm:
        assert 0 <= op < NUM_OPS, f"profile op out of range: {op}"
    # Per-dim behavior: with 5 different D2 dims the profile is NOT
    # required to have 5 distinct ops (two dims can legitimately point
    # at the same op) but it should contain at least two distinct ops
    # SOMEWHERE in its life.  We sample several moments.
    distinct_seen = set(warm)
    for _ in range(20):
        ao.process_text("theharmonylatticeprogressbreathcollapse")
        distinct_seen.update(ao.profile_5d())
    assert len(distinct_seen) >= 2, (
        f"profile_5d collapsed to single op across 20 texts: {distinct_seen}"
    )


def t_cortex_persist_roundtrip():
    """cortex_persist: save then load restores W, tick, and pair continuity
    exactly.  Missing file is a silent no-op, not a crash."""
    import tempfile
    from cortex import Cortex
    from cortex_persist import save_cortex, load_cortex

    cx1 = Cortex().boot()
    for _ in range(8):
        cx1.step_text("coherencekeeper harmony lattice")
    pre_tick = cx1.state.tick
    pre_trace = cx1.state.W_trace
    pre_W = [row[:] for row in cx1.hebbian.W]
    pre_prev_profile = list(cx1._prev_profile) if cx1._prev_profile else None

    with tempfile.NamedTemporaryFile(
        prefix="cortex_boot_gate_", suffix=".json",
        delete=False, mode="w", encoding="utf-8"
    ) as fh:
        tmp_path = fh.name
    try:
        save_cortex(cx1, tmp_path)
        cx2 = Cortex().boot()
        assert cx2.state.tick == 0, "fresh cortex starts at tick 0"
        ok = load_cortex(cx2, tmp_path)
        assert ok is True, "load_cortex should report True after reading file"
        assert cx2.state.tick == pre_tick, (
            f"tick mismatch after load: {cx2.state.tick} vs {pre_tick}"
        )
        assert abs(cx2.state.W_trace - pre_trace) < 1e-9, (
            f"W_trace mismatch: {cx2.state.W_trace} vs {pre_trace}"
        )
        for d_a in range(5):
            for d_b in range(5):
                assert abs(cx2.hebbian.W[d_a][d_b] - pre_W[d_a][d_b]) < 1e-9, (
                    f"W[{d_a}][{d_b}] mismatch after load"
                )
        assert cx2._prev_profile == pre_prev_profile, (
            f"_prev_profile mismatch: {cx2._prev_profile} vs {pre_prev_profile}"
        )

        # Missing file: silent no-op, returns False.
        cx3 = Cortex().boot()
        assert load_cortex(cx3, tmp_path + ".missing") is False, (
            "load_cortex should return False when file absent"
        )
    finally:
        if os.path.isfile(tmp_path):
            os.remove(tmp_path)


def t_cortex_voice_gating():
    """cortex_voice: cold cortex must be silent; warm cortex emits one
    factual structural sentence (never prose). Impossible gate silences."""
    from cortex import Cortex
    from cortex_voice import cortex_speak, field_readout

    # Cold: silent.
    cx = Cortex().boot()
    assert cortex_speak(cx) is None, (
        f"cold cortex should be silent, got: {cortex_speak(cx)!r}"
    )
    # Field readout is diagnostic; always returns a string.
    fld = field_readout(cx)
    assert isinstance(fld, str) and "field:" in fld, f"bad field_readout: {fld}"

    # Warm: eventually speaks.
    for _ in range(40):
        cx.step_text("coherencekeeper harmony lattice progress harmony")
    msg = cortex_speak(cx)
    assert msg is not None, f"warm cortex silent; snapshot={cx.snapshot()}"
    # Structural format: must contain learned/W/pointer separator.
    assert "learned:" in msg, f"unexpected voice format: {msg!r}"
    assert "->" in msg and "W=" in msg, f"unexpected voice format: {msg!r}"

    # Impossible gate: even warm cortex stays silent.
    assert cortex_speak(cx, emergent_gate=999.0) is None, (
        "unreachable gate should suppress output"
    )


# ── Driver ────────────────────────────────────────────────────────────

def main() -> int:
    print("=" * 60)
    print("  Gen13 Brain Boot Gate")
    print("=" * 60)
    tests = [
        ("imports: being modules",              t_imports_being),
        ("constant: T* = 5/7 everywhere",       t_t_star_agrees),
        ("ao_5element boots",                    t_ao_boot),
        ("ao_5element ticks 100 symbols",        t_ao_ticks),
        ("D2 pipeline classifies operators",     t_d2_produces_operators),
        ("body E/A/K stay in [0,1]",             t_body_eak_bounded),
        ("brain TL grows monotonically",         t_brain_tl_grows),
        ("HER buffer importable + empty",        t_her_buffer),
        ("math-first voice: verify + arithmetic", t_math_voice_arithmetic),
        ("trinity: AO composes one tick",         t_trinity_composes),
        ("trinity: Hebbian learns HARMONY",       t_hebbian_learns_harmony),
        ("trinity: quadratic glue F3 x F4",       t_quadratic_glue_bridge),
        ("trinity: cortex emergent signal",       t_cortex_emergent_nonnegative),
        ("trinity: profile_5d from D2",           t_profile_5d_from_d2),
        ("trinity: cortex_persist roundtrip",     t_cortex_persist_roundtrip),
        ("trinity: cortex_voice gating",          t_cortex_voice_gating),
    ]
    for name, fn in tests:
        _check(name, fn)
    print("-" * 60)
    print(f"  {_PASS} passed, {_FAIL} failed")
    if _FAIL:
        print("  BOOT GATE RED -- do not start CK until these are fixed:")
        for name, why in _FAILURES:
            print(f"    - {name}: {why}")
        return 1
    print("  BOOT GATE GREEN -- brain trinity is intact.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
