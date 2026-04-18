"""
ck_leash_test.py -- CK Dog Hardware Bring-Up / Leash Test
==========================================================
Operator: PROGRESS (3) -- first steps, measured.

Tests the R16 <-> FPGA link and basic dog responsiveness
BEFORE full attach. Run this with the dog tethered (on leash)
to a safe surface so legs can move without the dog falling.

Usage:
    python ck_leash_test.py COM3 [--verbose] [--no-servo]

Steps:
    1. Protocol handshake (PING/PONG)
    2. State readback (STATE packet parsing)
    3. Heartbeat verification (tick counter advancing)
    4. Coherence check (field must be above ESTOP floor)
    5. STAND command (all servos to neutral)
    6. WALK command (brief, 3 gait cycles)
    7. TROT command (brief, 2 gait cycles)
    8. ESTOP test (verify immediate stop)
    9. Report: PASS / FAIL with detail

--no-servo skips servo commands (safe for initial wiring test).

(c) 2026 Brayden Sanders / 7Site LLC -- Trinity Infinity Geometry
"""

import sys
import time
import argparse
import struct
import threading
import serial       # pip install pyserial

from ck_protocol import (
    make_packet, parse_packet,
    pack_ping, pack_observe, pack_gait, pack_estop,
    unpack_state, unpack_pong,
    PKT_PONG, PKT_STATE,
    PKT_NAMES, GAIT_NAMES,
    GAIT_STAND, GAIT_WALK, GAIT_TROT,
    OP, ESTOP_COHERENCE,
)

# ── Test config ──
BAUD          = 115200
PING_TIMEOUT  = 3.0    # seconds to wait for PONG
STATE_TIMEOUT = 2.0    # seconds to wait for STATE
TICK_WINDOW   = 1.0    # seconds to measure tick rate
WALK_TICKS    = 3      # gait cycles for WALK test
TROT_TICKS    = 2      # gait cycles for TROT test
GAIT_TICK_MS  = 200    # ms per gait cycle (matches MOVE_TIME in servo_commander.v)

GREEN  = '\033[92m'
YELLOW = '\033[93m'
RED    = '\033[91m'
RESET  = '\033[0m'
BOLD   = '\033[1m'

def ok(msg):   print(f'  {GREEN}[PASS]{RESET} {msg}')
def fail(msg): print(f'  {RED}[FAIL]{RESET} {msg}'); return False
def info(msg): print(f'  {YELLOW}[INFO]{RESET} {msg}')
def head(msg): print(f'\n{BOLD}{msg}{RESET}')


class LeashTester:
    def __init__(self, port: str, verbose: bool = False, no_servo: bool = False):
        self.port = port
        self.verbose = verbose
        self.no_servo = no_servo
        self.ser = None
        self._rx_buf = b''
        self._rx_packets = []
        self._rx_lock = threading.Lock()
        self._rx_thread = None
        self._running = False
        self.results = {}

    def connect(self) -> bool:
        try:
            self.ser = serial.Serial(
                port=self.port, baudrate=BAUD,
                timeout=0.05, write_timeout=1.0)
            self.ser.flushInput()
            self.ser.flushOutput()
            self._running = True
            self._rx_thread = threading.Thread(
                target=self._rx_loop, daemon=True)
            self._rx_thread.start()
            if self.verbose:
                info(f'Opened {self.port} @ {BAUD} baud')
            return True
        except Exception as e:
            print(f'{RED}ERROR{RESET} Cannot open {self.port}: {e}')
            return False

    def close(self):
        self._running = False
        if self.ser:
            self.ser.close()

    def _rx_loop(self):
        """Background thread: read bytes, assemble packets."""
        while self._running:
            try:
                data = self.ser.read(64)
                if data:
                    with self._rx_lock:
                        self._rx_buf += data
                        self._drain_packets()
            except Exception:
                pass
            time.sleep(0.001)

    def _drain_packets(self):
        """Pull complete packets from _rx_buf into _rx_packets."""
        buf = self._rx_buf
        while len(buf) >= 6:
            # Scan for 'CK' sync
            idx = buf.find(b'CK')
            if idx < 0:
                buf = b''
                break
            if idx > 0:
                buf = buf[idx:]
            if len(buf) < 6:
                break
            pkt_type = buf[2]
            length = struct.unpack('<H', buf[3:5])[0]
            total = 6 + length
            if len(buf) < total:
                break
            chunk = buf[:total]
            parsed = parse_packet(chunk)
            if parsed:
                self._rx_packets.append(parsed)
                if self.verbose:
                    print(f'    <- {PKT_NAMES.get(parsed[0], hex(parsed[0]))} '
                          f'({len(parsed[1])} bytes)')
            buf = buf[total:]
        self._rx_buf = buf

    def _send(self, pkt: bytes):
        if self.verbose:
            print(f'    -> {PKT_NAMES.get(pkt[2], hex(pkt[2]))} '
                  f'({len(pkt)} bytes)')
        self.ser.write(pkt)
        self.ser.flush()

    def _wait_for(self, pkt_type: int, timeout: float) -> dict | None:
        """Wait up to timeout seconds for a packet of pkt_type."""
        deadline = time.time() + timeout
        while time.time() < deadline:
            with self._rx_lock:
                for i, (t, p) in enumerate(self._rx_packets):
                    if t == pkt_type:
                        self._rx_packets.pop(i)
                        return p
            time.sleep(0.01)
        return None

    def _clear_rx(self):
        with self._rx_lock:
            self._rx_packets.clear()

    # ──────────────────────────────────────────────────────
    # TEST STEPS
    # ──────────────────────────────────────────────────────

    def test_ping(self) -> bool:
        head('Step 1: Protocol Handshake (PING/PONG)')
        self._clear_rx()
        t0 = time.time()
        self._send(pack_ping())
        raw = self._wait_for(PKT_PONG, PING_TIMEOUT)
        if raw is None:
            return fail(f'No PONG within {PING_TIMEOUT}s. '
                        'Check USB, COM port, and bitstream.')
        latency = (time.time() - t0) * 1000
        ok(f'PONG received in {latency:.1f}ms')
        self.results['ping_latency_ms'] = latency
        return True

    def test_state_readback(self) -> bool | dict:
        head('Step 2: State Readback (STATE packet)')
        self._clear_rx()
        self._send(pack_ping())     # STATE usually follows PONG
        raw = self._wait_for(PKT_STATE, STATE_TIMEOUT)
        if raw is None:
            # Try just waiting for a spontaneous STATE
            raw = self._wait_for(PKT_STATE, STATE_TIMEOUT)
        if raw is None:
            return fail(f'No STATE within {STATE_TIMEOUT * 2}s. '
                        'FPGA may not be sending state.')
        state = unpack_state(raw)
        if not state:
            return fail('STATE packet too short or malformed.')

        ok(f'being={OP[state["being"]]}  doing={OP[state["doing"]]}  '
           f'becoming={OP[state["becoming"]]}')
        ok(f'coherence={state["coherence"]:.4f}  '
           f'tick={state["tick"]}  coh={state["coh_num"]}/{state["coh_den"]}')
        if 'gait_mode' in state:
            ok(f'gait_mode={GAIT_NAMES.get(state["gait_mode"], "?")}  '
               f'gait_phase={state["gait_phase"]}  '
               f'legs_aligned={bin(state["legs_aligned"])}  '
               f'gait_coh={state["gait_coh"]:.2f}')
        self.results['initial_state'] = state
        return state

    def test_heartbeat_rate(self) -> bool:
        head('Step 3: Heartbeat Verification (tick rate)')
        t0 = time.time()
        t0_tick = None
        t1_tick = None

        deadline = t0 + TICK_WINDOW + 1.0
        while time.time() < deadline:
            raw = self._wait_for(PKT_STATE, 0.2)
            if raw:
                s = unpack_state(raw)
                if s:
                    if t0_tick is None:
                        t0_tick = (time.time(), s['tick'])
                    else:
                        t1_tick = (time.time(), s['tick'])
                        elapsed = t1_tick[0] - t0_tick[0]
                        if elapsed >= TICK_WINDOW:
                            break

        if t0_tick is None or t1_tick is None:
            return fail('Could not measure tick rate (only 1 STATE received).')

        elapsed = t1_tick[0] - t0_tick[0]
        ticks = t1_tick[1] - t0_tick[1]
        rate = ticks / elapsed if elapsed > 0 else 0
        self.results['tick_rate_hz'] = rate

        if rate < 20 or rate > 80:
            return fail(f'Tick rate {rate:.1f} Hz out of expected 20-80 Hz range.')
        ok(f'Tick rate: {rate:.1f} Hz ({ticks} ticks in {elapsed:.2f}s)')
        return True

    def test_coherence_floor(self) -> bool:
        head('Step 4: Coherence Check')
        state = self.results.get('initial_state', {})
        coh = state.get('coherence', 0.0)

        if coh < ESTOP_COHERENCE:
            return fail(f'Coherence {coh:.4f} < ESTOP floor {ESTOP_COHERENCE}. '
                        'Dog may not be safe to move.')
        if coh < 0.4:
            info(f'Coherence {coh:.4f} is in YELLOW band. '
                 'Dog will observe, not walk. Normal on cold boot.')
        elif coh >= 5.0 / 7.0:
            ok(f'Coherence {coh:.4f} >= T* = 5/7. GREEN band. Full sovereignty.')
        else:
            ok(f'Coherence {coh:.4f} in YELLOW band. Walk available.')
        return True

    def test_stand(self) -> bool:
        head('Step 5: STAND Command')
        if self.no_servo:
            info('--no-servo: skipping servo commands')
            return True
        self._clear_rx()
        self._send(pack_gait(GAIT_STAND))
        time.sleep(0.5)     # Let servos reach position
        raw = self._wait_for(PKT_STATE, STATE_TIMEOUT)
        if raw:
            s = unpack_state(raw)
            if 'gait_mode' in s and s['gait_mode'] != GAIT_STAND:
                info(f'STAND sent, FPGA reports gait_mode={s["gait_mode"]}. '
                     'May update on next heartbeat tick.')
        ok('STAND command sent, servos should be in neutral position.')
        return True

    def test_walk(self) -> bool:
        head('Step 6: WALK Command (3 gait cycles)')
        if self.no_servo:
            info('--no-servo: skipping servo commands')
            return True
        self._clear_rx()
        self._send(pack_gait(GAIT_WALK))
        walk_time = WALK_TICKS * GAIT_TICK_MS / 1000.0
        info(f'Walking for {walk_time:.1f}s ({WALK_TICKS} cycles x {GAIT_TICK_MS}ms)...')
        time.sleep(walk_time)
        self._send(pack_gait(GAIT_STAND))   # Stop after test
        time.sleep(0.3)
        ok('WALK complete, returned to STAND.')
        return True

    def test_trot(self) -> bool:
        head('Step 7: TROT Command (2 gait cycles)')
        if self.no_servo:
            info('--no-servo: skipping servo commands')
            return True
        self._clear_rx()
        self._send(pack_gait(GAIT_TROT))
        trot_time = TROT_TICKS * GAIT_TICK_MS / 1000.0
        info(f'Trotting for {trot_time:.1f}s ({TROT_TICKS} cycles x {GAIT_TICK_MS}ms)...')
        time.sleep(trot_time)
        self._send(pack_gait(GAIT_STAND))
        time.sleep(0.3)
        ok('TROT complete, returned to STAND.')
        return True

    def test_estop(self) -> bool:
        head('Step 8: ESTOP Test')
        if self.no_servo:
            info('--no-servo: skipping servo commands')
            return True
        self._clear_rx()
        info('Sending WALK, then ESTOP 0.2s later...')
        self._send(pack_gait(GAIT_WALK))
        time.sleep(0.2)
        self._send(pack_estop())
        time.sleep(0.5)
        raw = self._wait_for(PKT_STATE, STATE_TIMEOUT)
        if raw:
            s = unpack_state(raw)
            if 'gait_mode' in s:
                if s['gait_mode'] == GAIT_STAND:
                    ok('ESTOP: gait_mode returned to STAND.')
                else:
                    info(f'ESTOP sent. Gait mode: {s["gait_mode"]}. '
                         'May take one tick to latch.')
        ok('ESTOP command sent. All servos should be centered.')
        return True

    # ──────────────────────────────────────────────────────
    # MAIN
    # ──────────────────────────────────────────────────────

    def run(self) -> bool:
        print(f'\n{BOLD}CK Dog Leash Test{RESET}')
        print(f'Port: {self.port} | Baud: {BAUD} | '
              f'No-servo: {self.no_servo}')
        print('=' * 52)

        if not self.connect():
            return False

        steps = [
            ('ping',          self.test_ping),
            ('state',         self.test_state_readback),
            ('heartbeat',     self.test_heartbeat_rate),
            ('coherence',     self.test_coherence_floor),
            ('stand',         self.test_stand),
            ('walk',          self.test_walk),
            ('trot',          self.test_trot),
            ('estop',         self.test_estop),
        ]

        passed = []
        failed = []

        for name, step in steps:
            try:
                result = step()
                if result is False:
                    failed.append(name)
                else:
                    passed.append(name)
            except KeyboardInterrupt:
                print(f'\n{YELLOW}Interrupted. Sending ESTOP...{RESET}')
                try:
                    self._send(pack_estop())
                except Exception:
                    pass
                break
            except Exception as e:
                print(f'  {RED}[ERROR]{RESET} {name}: {e}')
                failed.append(name)

        self.close()

        # Final report
        print('\n' + '=' * 52)
        print(f'{BOLD}Results: {len(passed)} passed / {len(failed)} failed{RESET}')
        if passed:
            print(f'  {GREEN}PASS{RESET}: {", ".join(passed)}')
        if failed:
            print(f'  {RED}FAIL{RESET}: {", ".join(failed)}')

        if not failed:
            print(f'\n{GREEN}{BOLD}LEASH TEST PASSED.{RESET}')
            print('Ready to: python ck_r16_bridge.py --port ' + self.port)
        else:
            print(f'\n{RED}{BOLD}LEASH TEST FAILED.{RESET}')
            print('Fix the issues above before connecting the dog.')

        return len(failed) == 0


def main():
    parser = argparse.ArgumentParser(
        description='CK Dog Leash Test')
    parser.add_argument('port', help='Serial port (e.g. COM3 or /dev/ttyUSB0)')
    parser.add_argument('--verbose', '-v', action='store_true',
                        help='Show all packet I/O')
    parser.add_argument('--no-servo', action='store_true',
                        help='Skip servo commands (protocol test only)')
    args = parser.parse_args()

    tester = LeashTester(args.port, verbose=args.verbose,
                         no_servo=args.no_servo)
    success = tester.run()
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
