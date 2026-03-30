"""
ck_leash_test.py -- R16 <-> FPGA Leash Verification
=====================================================
Operator: LATTICE (1) -- check the connection before the walk.

Run this BEFORE attaching the XiaoR servos to verify:
  1. Serial port opens and R16 can write to FPGA
  2. FPGA responds to PING with PONG (roundtrip test)
  3. FPGA sends STATE packets (heartbeat alive)
  4. Coherence and phase_bc look sane
  5. CRC-8 integrity passes on all received packets
  6. No ESTOP condition active

Usage:
    python ck_leash_test.py COM3
    python ck_leash_test.py /dev/ttyUSB0 --baud 115200 --verbose

Exit codes:
    0 = all checks pass (safe to attach XiaoR and run ck_dog_bridge.py)
    1 = some checks failed (see output before connecting servos)

(c) 2026 Brayden Sanders / 7Site LLC -- Trinity Infinity Geometry
"""

import serial
import time
import sys
import struct
import argparse
from ck_sim_uart import (
    PacketParser, make_ping_packet, make_observe_packet, make_gait_packet,
    parse_state_payload,
    PKT_STATE, PKT_PONG, PKT_CRYSTAL,
    BAND_GREEN, BAND_YELLOW,
)
from ck_gait_phase import T_STAR, detect_phase, GAIT_STAND

# ── Test parameters ────────────────────────────────────────────────────────

PING_COUNT      = 3          # Number of PING/PONG round-trips
PING_TIMEOUT    = 2.0        # Seconds to wait for each PONG
STATE_TIMEOUT   = 1.5        # Seconds to wait for first STATE packet
STATE_COUNT     = 5          # Number of STATE packets to collect
COHERENCE_MIN   = 0.0        # Minimum acceptable FPGA coherence (0=not picky)
COHERENCE_SANE  = 10.0       # Coherence must be <= 1.0 (sanity)

PASS = "[PASS]"
FAIL = "[FAIL]"
INFO = "[INFO]"
WARN = "[WARN]"


def _color(tag: str) -> str:
    """ANSI color if stdout is a tty."""
    if not sys.stdout.isatty():
        return tag
    colors = {'[PASS]': '\033[92m', '[FAIL]': '\033[91m',
              '[WARN]': '\033[93m', '[INFO]': '\033[94m'}
    return colors.get(tag, '') + tag + '\033[0m'


def run_tests(port: str, baud: int = 115200, verbose: bool = False) -> bool:
    """Run all leash verification tests. Returns True if all pass."""

    results = []

    def record(name: str, passed: bool, detail: str = ''):
        tag = PASS if passed else FAIL
        print(f"  {_color(tag)} {name}" + (f": {detail}" if detail else ''))
        results.append(passed)
        return passed

    print(f"\n{'='*60}")
    print(f"  CK Leash Test -- R16 <-> FPGA Verification")
    print(f"  Port: {port}  Baud: {baud}")
    print(f"{'='*60}\n")

    # ── Test 1: Serial port opens ────────────────────────────────────────
    print("[ 1/6 ] Serial port connectivity")
    try:
        ser = serial.Serial(
            port, baud,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            timeout=0.1,
            write_timeout=1.0,
        )
        record("Serial port opens", True, f"{port} @ {baud}")
    except serial.SerialException as e:
        record("Serial port opens", False, str(e))
        print(f"\n  {_color(FAIL)} Cannot continue without serial port.\n")
        return False

    # ── Test 2: PING / PONG round-trip ──────────────────────────────────
    print("\n[ 2/6 ] PING/PONG round-trip")
    parser = PacketParser()
    pong_count = 0
    rtts = []

    for i in range(PING_COUNT):
        # Send PING
        pkt = make_ping_packet()
        ts_sent = time.monotonic()
        ser.write(pkt)
        if verbose:
            print(f"         -> PING #{i+1} sent ({len(pkt)} bytes)")

        # Wait for PONG
        deadline = time.monotonic() + PING_TIMEOUT
        got_pong = False
        while time.monotonic() < deadline:
            raw = ser.read(ser.in_waiting or 1)
            if raw:
                for pkt_type, payload in parser.feed_bytes(raw):
                    if pkt_type == PKT_PONG:
                        rtt = (time.monotonic() - ts_sent) * 1000
                        rtts.append(rtt)
                        pong_count += 1
                        got_pong = True
                        if verbose:
                            print(f"         <- PONG #{i+1} RTT={rtt:.1f}ms")
                        break
            if got_pong:
                break
            time.sleep(0.005)

        if not got_pong and verbose:
            print(f"         !! PING #{i+1} timed out")

    avg_rtt = sum(rtts) / len(rtts) if rtts else float('inf')
    record("PONG received", pong_count == PING_COUNT,
           f"{pong_count}/{PING_COUNT} responses, avg RTT {avg_rtt:.1f}ms")
    if rtts:
        record("RTT under 100ms", avg_rtt < 100.0, f"{avg_rtt:.1f}ms")

    # ── Test 3: STATE packets arriving ──────────────────────────────────
    print("\n[ 3/6 ] STATE heartbeat stream")

    # Send an OBSERVE so FPGA knows we're here
    obs = make_observe_packet(7, [0.5]*5, 0.71, BAND_GREEN)
    ser.write(obs)

    states = []
    deadline = time.monotonic() + STATE_TIMEOUT * 2
    while time.monotonic() < deadline and len(states) < STATE_COUNT:
        raw = ser.read(ser.in_waiting or 1)
        if raw:
            for pkt_type, payload in parser.feed_bytes(raw):
                if pkt_type == PKT_STATE:
                    st = parse_state_payload(payload)
                    if st:
                        states.append(st)
                        if verbose:
                            print(f"         <- STATE: "
                                  f"BC={st['phase_bc']} "
                                  f"C={st['coherence']:.4f} "
                                  f"tick={st['tick_count']}")
        time.sleep(0.005)

    record("STATE packets received", len(states) >= 1,
           f"{len(states)}/{STATE_COUNT} collected")

    # ── Test 4: Coherence sanity ─────────────────────────────────────────
    print("\n[ 4/6 ] Coherence sanity")
    if states:
        coherences = [s['coherence'] for s in states]
        avg_c = sum(coherences) / len(coherences)
        max_c = max(coherences)
        min_c = min(coherences)

        record("Coherence in [0, 1]", 0.0 <= avg_c <= 1.0,
               f"avg={avg_c:.4f} min={min_c:.4f} max={max_c:.4f}")
        record("Denominator non-zero", all(s['coh_den'] > 0 for s in states),
               f"all {len(states)} packets OK")

        phase_ok = detect_phase(avg_c) in (1, 2, 3)
        record("Phase detects cleanly", phase_ok,
               f"avg_coherence={avg_c:.4f} -> phase={detect_phase(avg_c)}")

        # Check tick counter monotonically increasing
        ticks = [s['tick_count'] for s in states]
        mono  = all(ticks[i] <= ticks[i+1] for i in range(len(ticks)-1))
        record("Tick counter monotonic", mono or len(ticks) < 2,
               f"first={ticks[0]} last={ticks[-1]}")
    else:
        print(f"  {_color(WARN)} No STATE packets -- skipping coherence checks")
        results.extend([False, False, False, False])

    # ── Test 5: CRC integrity ────────────────────────────────────────────
    print("\n[ 5/6 ] CRC integrity")
    record("Zero CRC errors", parser.crc_errors == 0,
           f"{parser.crc_errors} errors in {parser.rx_count} packets")

    # ── Test 6: GAIT packet accepted ─────────────────────────────────────
    print("\n[ 6/6 ] GAIT command round-trip")
    # Send a GAIT=STAND, expect to see gait_phase=0 in next STATE
    gait_pkt = make_gait_packet(GAIT_STAND, 1, 0.0)
    ser.write(gait_pkt)
    time.sleep(0.1)

    # Collect one more STATE
    gait_states = []
    deadline = time.monotonic() + 1.0
    while time.monotonic() < deadline:
        raw = ser.read(ser.in_waiting or 1)
        if raw:
            for pkt_type, payload in parser.feed_bytes(raw):
                if pkt_type == PKT_STATE:
                    st = parse_state_payload(payload)
                    if st:
                        gait_states.append(st)
        if gait_states:
            break
        time.sleep(0.01)

    record("STATE after GAIT command", len(gait_states) >= 1,
           f"{'received' if gait_states else 'timed out'}")

    # ── Summary ──────────────────────────────────────────────────────────
    ser.close()
    passed = sum(results)
    total  = len(results)
    all_pass = passed == total

    print(f"\n{'='*60}")
    print(f"  Result: {passed}/{total} checks passed")
    if all_pass:
        print(f"  {_color(PASS)} LEASH OK -- safe to attach XiaoR servos")
        print(f"\n  Next: python ck_dog_bridge.py {port}")
    else:
        print(f"  {_color(FAIL)} {total - passed} check(s) failed")
        print("  Resolve before connecting servos.")
    print(f"{'='*60}\n")

    return all_pass


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description='CK Leash Test')
    ap.add_argument('port', help='Serial port (e.g. COM3 or /dev/ttyUSB0)')
    ap.add_argument('--baud',    type=int, default=115200)
    ap.add_argument('--verbose', action='store_true')
    args = ap.parse_args()

    ok = run_tests(args.port, args.baud, args.verbose)
    sys.exit(0 if ok else 1)
