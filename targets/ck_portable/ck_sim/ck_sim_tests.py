"""
ck_sim_tests.py -- Parity Tests for CK Coherence Machine Simulation
=====================================================================
Operator: COUNTER (2) -- measuring correctness.

Every test validates that the Python simulation produces
identical outputs to the C/Verilog code for the same inputs.

Run: python -m ck_sim.ck_sim_tests

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import os
import sys
import math
import struct
import tempfile

# ── Test Framework ──

passed = 0
failed = 0
total = 0


def test(name: str, condition: bool, detail: str = ""):
    global passed, failed, total
    total += 1
    if condition:
        passed += 1
        print(f"  PASS  {name}")
    else:
        failed += 1
        print(f"  FAIL  {name}  {detail}")


def section(name: str):
    print(f"\n{'='*60}")
    print(f"  {name}")
    print(f"{'='*60}")


# ═══════════════════════════════════════════════════════════
#  TEST 1: CL Composition (ck_heartbeat.v)
# ═══════════════════════════════════════════════════════════

def test_cl_composition():
    section("CL Composition Table")
    from ck_sim.ck_sim_heartbeat import CL, compose, HARMONY, VOID, NUM_OPS

    # Verify table dimensions
    test("CL is 10x10", len(CL) == 10 and all(len(row) == 10 for row in CL))

    # Count HARMONY entries (should be 73/100)
    harmony_count = sum(1 for i in range(10) for j in range(10) if CL[i][j] == HARMONY)
    test("73 HARMONY entries (73/100)", harmony_count == 73,
         f"got {harmony_count}")

    # VOID row: all VOID except HARMONY column
    test("CL[VOID][HARMONY] = HARMONY", compose(0, 7) == HARMONY)
    test("CL[VOID][VOID] = VOID", compose(0, 0) == VOID)

    # HARMONY row: ALL HARMONY
    all_harmony = all(CL[7][j] == HARMONY for j in range(10))
    test("HARMONY row is all HARMONY", all_harmony)

    # Non-HARMONY entries: (1,2)=3, (2,1)=3, (2,4)=4, (2,9)=9, etc.
    test("CL[1][2] = PROGRESS(3)", compose(1, 2) == 3)
    test("CL[2][1] = PROGRESS(3)", compose(2, 1) == 3)
    test("CL[2][4] = COLLAPSE(4)", compose(2, 4) == 4)
    test("CL[2][9] = RESET(9)", compose(2, 9) == 9)
    test("CL[3][9] = PROGRESS(3)", compose(3, 9) == 3)
    test("CL[4][8] = BREATH(8)", compose(4, 8) == 8)
    test("CL[9][2] = RESET(9)", compose(9, 2) == 9)
    test("CL[9][3] = PROGRESS(3)", compose(9, 3) == 3)

    # Out of range
    test("compose out of range = VOID", compose(10, 5) == VOID)


# ═══════════════════════════════════════════════════════════
#  TEST 2: Bump Detection (ck_heartbeat.v)
# ═══════════════════════════════════════════════════════════

def test_bump_detection():
    section("Bump Pair Detection")
    from ck_sim.ck_sim_heartbeat import is_bump, BUMP_PAIRS

    # 5 bump pairs, both orderings
    for p0, p1 in BUMP_PAIRS:
        test(f"bump ({p0},{p1})", is_bump(p0, p1))
        test(f"bump ({p1},{p0})", is_bump(p1, p0))

    # Non-bump pairs
    test("(0,0) not bump", not is_bump(0, 0))
    test("(7,7) not bump", not is_bump(7, 7))
    test("(1,3) not bump", not is_bump(1, 3))
    test("(6,8) not bump", not is_bump(6, 8))


# ═══════════════════════════════════════════════════════════
#  TEST 3: Coherence Window (ck_heartbeat.v)
# ═══════════════════════════════════════════════════════════

def test_coherence_window():
    section("Coherence Window (32-entry ring)")
    from ck_sim.ck_sim_heartbeat import HeartbeatFPGA, HARMONY, VOID, HISTORY_SIZE

    hb = HeartbeatFPGA()

    # Feed 32 HARMONY-producing pairs (HARMONY row: anything with 7)
    for _ in range(32):
        hb.tick(7, 0)  # CL[7][0] = HARMONY
    test("32 HARMONY ticks: coh = 1.0", hb.coherence == 1.0,
         f"got {hb.coherence}")
    test("coh_num = 32", hb.coh_num == 32)
    test("coh_den = 32", hb.coh_den == 32)

    # Feed 32 VOID ticks to flush window
    for _ in range(32):
        hb.tick(0, 0)  # CL[0][0] = VOID
    test("32 VOID ticks: coh = 0.0", hb.coherence == 0.0,
         f"got {hb.coherence}")

    # Mixed: 16 HARMONY + 16 VOID
    hb2 = HeartbeatFPGA()
    for _ in range(16):
        hb2.tick(7, 0)  # HARMONY
    for _ in range(16):
        hb2.tick(0, 0)  # VOID
    test("16H+16V: coh = 0.5", hb2.coherence == 0.5,
         f"got {hb2.coherence}")


# ═══════════════════════════════════════════════════════════
#  TEST 4: Brain Sovereignty Pipeline (ck_brain.c)
# ═══════════════════════════════════════════════════════════

def test_brain_sovereignty():
    section("Brain Sovereignty Pipeline")
    from ck_sim.ck_sim_brain import (
        brain_init, brain_tick, brain_tl_observe,
        brain_crystallize, above_t_star, BrainState, T_STAR_F
    )
    from ck_sim.ck_sim_heartbeat import HeartbeatFPGA, HARMONY

    # T* check
    test("above_t_star(5,7) = True", above_t_star(5, 7))
    test("above_t_star(4,7) = False", not above_t_star(4, 7))
    test("above_t_star(32,32) = True", above_t_star(32, 32))
    test("above_t_star(0,32) = False", not above_t_star(0, 32))

    # Mode transitions
    state = brain_init()
    hb = HeartbeatFPGA()
    test("Initial mode = 0 (OBSERVE)", state.mode == 0)

    # Feed 100 transitions to reach CLASSIFY
    for _ in range(100):
        hb.tick(7, 1)  # produces HARMONY
        brain_tick(state, hb)
    test("After 100 ticks: mode = 1 (CLASSIFY)", state.mode == 1,
         f"got mode={state.mode}, total={state.tl_total}")

    # Feed more with varied transitions to reach CRYSTALLIZE
    # Use HARMONY row (all produce HARMONY phase_bc) so coherence stays high
    # but vary the D input so TL has multiple entries (nonzero entropy)
    for i in range(500):
        d_val = i % 5  # Vary: 0,1,2,3,4
        hb.tick(7, d_val)  # CL[7][*] = HARMONY always
        brain_tick(state, hb)
    test("After 600 ticks: mode >= 2", state.mode >= 2,
         f"got mode={state.mode}")

    # Entropy should be nonzero with varied transitions
    test("Entropy > 0", state.tl_entropy > 0.0,
         f"got {state.tl_entropy}")


# ═══════════════════════════════════════════════════════════
#  TEST 5: Crystallization (ck_brain.c)
# ═══════════════════════════════════════════════════════════

def test_crystallization():
    section("Crystal Formation")
    from ck_sim.ck_sim_brain import BrainState, brain_init, brain_tl_observe, brain_crystallize

    state = brain_init()
    # Feed 100 of (7->1) and scatter others
    for _ in range(60):
        brain_tl_observe(state, 7, 1)
    for _ in range(40):
        brain_tl_observe(state, 0, 0)

    brain_crystallize(state)
    dom = state.domains[0]

    # (7,1) has 60% > 5% threshold, should crystallize
    found = any(cr.ops[0] == 7 and cr.ops[1] == 1 for cr in dom.crystals)
    test("Crystal (7->1) formed", found)
    test("At least 1 crystal", len(dom.crystals) >= 1)

    # (0,0) has 40% > 5%, should also crystallize
    found_void = any(cr.ops[0] == 0 and cr.ops[1] == 0 for cr in dom.crystals)
    test("Crystal (0->0) formed", found_void)


# ═══════════════════════════════════════════════════════════
#  TEST 6: Body Rhythms (ck_body.c)
# ═══════════════════════════════════════════════════════════

def test_body_rhythms():
    section("Body Rhythms (E/A/K, Breath, Pulse)")
    from ck_sim.ck_sim_body import (
        body_init, body_tick, body_feed_eak,
        T_STAR_F, BAND_GREEN, BAND_YELLOW, BAND_RED,
        BREATH_INHALE, BREATH_EXHALE, RATIO_CALM, RATIO_FRACTAL,
        BodyState
    )

    body = body_init()

    # Initial state
    test("Initial E = 0.0", body.heartbeat.E == 0.0)
    test("Initial A = 0.3", body.heartbeat.A == 0.3)
    test("Initial K = 0.5", body.heartbeat.K == 0.5)

    # E decay test
    body_feed_eak(body, 1.0, 0.0, 0.0)  # Spike E to max
    test("E spiked to 1.0", body.heartbeat.E == 1.0)

    for _ in range(10):
        body_tick(body)
    expected_e = 1.0 * (0.95 ** 10)
    test(f"E decayed after 10 ticks (~{expected_e:.4f})",
         abs(body.heartbeat.E - expected_e) < 0.01,
         f"got {body.heartbeat.E:.4f}")

    # Breath adapts to coherence
    # Need high brain_coherence AND high body C for blended > T*
    body2 = body_init()
    body2.brain_coherence = 0.95
    body2.heartbeat.E = 0.0
    body2.heartbeat.A = 0.0
    body2.heartbeat.K = 0.9  # High K -> high body C
    for _ in range(20):
        body_tick(body2)
    test("High coherence -> CALM breath (10 beats)",
         body2.breath.beats_per_cycle == RATIO_CALM,
         f"got {body2.breath.beats_per_cycle}, body C={body2.heartbeat.C:.3f}")

    body3 = body_init()
    body3.brain_coherence = 0.2  # Well below yellow
    body3.heartbeat.E = 0.8     # High entropy
    for _ in range(20):
        body_tick(body3)
    test("Low coherence -> FRACTAL breath (2 beats)",
         body3.breath.beats_per_cycle == RATIO_FRACTAL)

    # Pulse gating
    body4 = body_init()
    body4.brain_coherence = 0.8
    found_receive = False
    found_express = False
    for _ in range(50):
        body_tick(body4)
        if body4.pulse.can_receive:
            found_receive = True
        if body4.pulse.can_express:
            found_express = True
    test("Pulse: found can_receive (INHALE)", found_receive)
    test("Pulse: found can_express (EXHALE)", found_express)


# ═══════════════════════════════════════════════════════════
#  TEST 7: Binary TL Format (ck_sd.c)
# ═══════════════════════════════════════════════════════════

def test_sd_persistence():
    section("Binary TL Save/Load (ck_sd.c)")
    from ck_sim.ck_sim_sd import save_tl, load_tl, crc8, TL_MAGIC
    from ck_sim.ck_sim_brain import brain_init, brain_tl_observe, brain_crystallize

    # Build a state with known values
    state = brain_init()
    for _ in range(60):
        brain_tl_observe(state, 7, 1)
    for _ in range(40):
        brain_tl_observe(state, 3, 5)
    brain_crystallize(state)

    # Save
    tmpfile = os.path.join(tempfile.gettempdir(), 'ck_tl_test.bin')
    save_tl(state, tmpfile)

    # Verify file starts with magic
    with open(tmpfile, 'rb') as f:
        data = f.read()
    test("File starts with 'CKTL'", data[:4] == TL_MAGIC)
    test("Version = 1", data[4] == 1)

    # Verify CRC
    stored_crc = data[-1]
    computed_crc = crc8(data[:-1])
    test("CRC matches", stored_crc == computed_crc,
         f"stored={stored_crc:#x} computed={computed_crc:#x}")

    # Load into fresh state
    state2 = brain_init()
    ok = load_tl(state2, tmpfile)
    test("Load succeeds", ok)
    test("Total preserved", state2.tl_total == state.tl_total,
         f"got {state2.tl_total}, expected {state.tl_total}")
    test("Entry (7,1) count preserved",
         state2.tl_entries[7][1].count == state.tl_entries[7][1].count)
    test("Entry (3,5) count preserved",
         state2.tl_entries[3][5].count == state.tl_entries[3][5].count)

    # Cleanup
    os.unlink(tmpfile)


# ═══════════════════════════════════════════════════════════
#  TEST 8: UART Protocol (ck_uart.c + ck_serial.py)
# ═══════════════════════════════════════════════════════════

def test_uart_protocol():
    section("UART Packet Protocol")
    from ck_sim.ck_sim_uart import (
        make_packet, make_state_packet, make_crystal_packet,
        PacketParser, parse_state_payload, parse_crystal_payload,
        PKT_STATE, PKT_CRYSTAL, PKT_PING, PKT_PONG, crc8
    )

    # Basic round-trip
    pkt = make_packet(PKT_PING, b'\x01\x02\x03')
    parser = PacketParser()
    results = list(parser.feed_bytes(pkt))
    test("PING round-trip: 1 packet", len(results) == 1)
    if results:
        pkt_type, payload = results[0]
        test("PING type correct", pkt_type == PKT_PING)
        test("PING payload correct", payload == b'\x01\x02\x03')

    # State packet
    state_pkt = make_state_packet(
        phase_b=7, phase_d=1, phase_bc=7, fuse_op=7, bump=True,
        tick_count=12345, coh_num=28, coh_den=32,
        brain_ticks=500, mode=2, domain_count=1
    )
    parser2 = PacketParser()
    results2 = list(parser2.feed_bytes(state_pkt))
    test("STATE round-trip: 1 packet", len(results2) == 1)
    if results2:
        pkt_type, payload = results2[0]
        state = parse_state_payload(payload)
        test("STATE phase_b = 7", state['phase_b'] == 7)
        test("STATE phase_bc = 7", state['phase_bc'] == 7)
        test("STATE bump = True", state['bump'] == True)
        test("STATE tick_count = 12345", state['tick_count'] == 12345)
        test("STATE coherence ~0.875", abs(state['coherence'] - 28/32) < 0.01)
        test("STATE mode = 2", state['mode'] == 2)

    # Crystal packet
    crystal_pkt = make_crystal_packet(
        ops=[7, 1], length=2, fuse=7, confidence=0.625, seen=500
    )
    parser3 = PacketParser()
    results3 = list(parser3.feed_bytes(crystal_pkt))
    test("CRYSTAL round-trip: 1 packet", len(results3) == 1)
    if results3:
        pkt_type, payload = results3[0]
        cr = parse_crystal_payload(payload)
        test("CRYSTAL pattern = [7,1]", cr['pattern'] == [7, 1])
        test("CRYSTAL fuse = 7", cr['fuse'] == 7)
        test("CRYSTAL seen = 500", cr['seen'] == 500)

    # Corrupted CRC
    bad_pkt = bytearray(state_pkt)
    bad_pkt[-1] ^= 0xFF  # Flip CRC
    parser4 = PacketParser()
    results4 = list(parser4.feed_bytes(bytes(bad_pkt)))
    test("Corrupted CRC: rejected", len(results4) == 0)
    test("CRC error counted", parser4.crc_errors == 1)

    # Byte-at-a-time parsing
    parser5 = PacketParser()
    found = False
    for byte in state_pkt:
        result = parser5.feed_byte(byte)
        if result is not None:
            found = True
    test("Byte-at-a-time parsing works", found)


# ═══════════════════════════════════════════════════════════
#  TEST 9: D2 Pipeline (d2_pipeline.v)
# ═══════════════════════════════════════════════════════════

def test_d2_pipeline():
    section("D2 Pipeline (Q1.14 Fixed-Point)")
    from ck_sim.ck_sim_d2 import (
        D2Pipeline, float_to_q14, q14_to_float,
        FORCE_LUT_Q14, classify_force_d2
    )
    from ck_sim.ck_sim_heartbeat import VOID, HARMONY

    # Q1.14 conversion
    test("float_to_q14(0.8) = 13107", float_to_q14(0.8) == 13107)
    test("float_to_q14(1.0) = 16384", float_to_q14(1.0) == 16384)
    test("float_to_q14(0.0) = 0", float_to_q14(0.0) == 0)
    test("q14_to_float(13107) ~ 0.8", abs(q14_to_float(13107) - 0.8) < 0.001)

    # Force LUT has 26 entries
    test("Force LUT has 26 entries", len(FORCE_LUT_Q14) == 26)

    # D2 pipeline: 3 identical symbols -> D2 = 0
    pipe = D2Pipeline()
    pipe.feed_symbol(0)  # 'a'
    pipe.feed_symbol(0)  # 'a'
    valid = pipe.feed_symbol(0)  # 'a'
    test("3 identical -> D2 valid", valid)
    test("3 identical -> D2 ~= zero", all(abs(d) < 10 for d in pipe.d2),
         f"got {pipe.d2}")
    test("3 identical -> VOID operator", pipe.operator == VOID)

    # Pipeline with varying input
    pipe2 = D2Pipeline()
    pipe2.feed_symbol(0)   # a (ALEPH)
    pipe2.feed_symbol(7)   # h (CHET)
    valid2 = pipe2.feed_symbol(0)  # a (ALEPH)
    test("Varying input -> D2 valid", valid2)
    test("Varying input -> D2 nonzero", any(abs(d) > 10 for d in pipe2.d2))

    # Classify zero D2 -> VOID
    test("classify zero = VOID", classify_force_d2([0,0,0,0,0], 0.0) == VOID)


# ═══════════════════════════════════════════════════════════
#  TEST 10: LED Colors (ck_led.c)
# ═══════════════════════════════════════════════════════════

def test_led_colors():
    section("LED Operator Colors")
    from ck_sim.ck_sim_led import (
        get_op_color, breathe_color, get_op_color_float,
        OP_COLORS, SOVEREIGN_COLOR
    )
    from ck_sim.ck_sim_heartbeat import VOID, HARMONY, CHAOS

    test("VOID = black", get_op_color(VOID) == (0, 0, 0))
    test("HARMONY = blue-cyan", get_op_color(HARMONY) == (80, 200, 255))
    test("CHAOS = hot red", get_op_color(CHAOS) == (255, 0, 60))
    test("SOVEREIGN = gold", SOVEREIGN_COLOR == (255, 200, 50))

    # Breath modulation
    dim = breathe_color(HARMONY, 0.0)  # Min breath
    bright = breathe_color(HARMONY, 1.0)  # Max breath
    test("Breath mod=0 dimmer than mod=1",
         sum(dim) < sum(bright))

    # Float colors in 0-1 range
    r, g, b = get_op_color_float(HARMONY)
    test("Float colors in [0,1]", 0 <= r <= 1 and 0 <= g <= 1 and 0 <= b <= 1)


# ═══════════════════════════════════════════════════════════
#  RUN ALL TESTS
# ═══════════════════════════════════════════════════════════

def main():
    print("\n" + "=" * 60)
    print("  CK COHERENCE MACHINE -- PARITY TESTS")
    print("  Every algorithm must match the C/Verilog code")
    print("=" * 60)

    test_cl_composition()
    test_bump_detection()
    test_coherence_window()
    test_brain_sovereignty()
    test_crystallization()
    test_body_rhythms()
    test_sd_persistence()
    test_uart_protocol()
    test_d2_pipeline()
    test_led_colors()

    print(f"\n{'='*60}")
    print(f"  RESULTS: {passed}/{total} passed, {failed} failed")
    print(f"{'='*60}\n")

    return 0 if failed == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
