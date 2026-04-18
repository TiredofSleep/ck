"""
ck_r16_bridge.py -- Live R16 <-> FPGA Dog Bridge (Gen 11)
==========================================================
Operator: BALANCE (5) -- the bridge between two bodies.

Runs on the R16. Reads CK engine state from the Gen11 web API
and sends GAIT / OBSERVE commands to the FPGA based on
Phase→gait mapping and coherence thresholds.

Phase-to-gait (from tig_core, memory-locked):
  Phase 1 (lambda < 0.09) -> STAND
  Phase 2 (lambda < 0.50) -> WALK
  Phase 3 (lambda >= 0.50) -> TROT
  C < 0.20               -> ESTOP

Usage:
  python ck_r16_bridge.py --port COM3
  python ck_r16_bridge.py --port COM3 --ck-url http://localhost:7778

(c) 2026 Brayden Sanders / 7Site LLC -- Trinity Infinity Geometry
"""

import argparse
import time
import threading
import struct
import json
import urllib.request
import serial

from ck_protocol import (
    pack_ping, pack_observe, pack_gait, pack_estop,
    parse_packet, unpack_state, unpack_pong,
    PKT_STATE, PKT_PONG, PKT_NAMES,
    GAIT_STAND, GAIT_WALK, GAIT_TROT, GAIT_NAMES,
    ESTOP_COHERENCE, state_to_gait,
    OP, T_STAR,
)

BAUD = 115200
BRIDGE_HZ = 10       # How fast bridge polls CK engine (Hz)
REPORT_EVERY = 5.0   # Print status every N seconds


class R16Bridge:
    def __init__(self, port: str, ck_url: str = 'http://localhost:7778'):
        self.port = port
        self.ck_url = ck_url
        self.ser = None
        self._rx_buf = b''
        self._rx_packets = []
        self._rx_lock = threading.Lock()
        self._running = False
        self._last_gait = None
        self._last_report = 0.0
        self._tick = 0
        self._estop_count = 0
        self._last_fpga_state = {}

    def connect(self) -> bool:
        try:
            self.ser = serial.Serial(
                port=self.port, baudrate=BAUD,
                timeout=0.05, write_timeout=1.0)
            self.ser.flushInput()
            self.ser.flushOutput()
            print(f'[BRIDGE] Opened {self.port} @ {BAUD}')
            return True
        except Exception as e:
            print(f'[BRIDGE] Cannot open {self.port}: {e}')
            return False

    def _send(self, pkt: bytes):
        try:
            self.ser.write(pkt)
            self.ser.flush()
        except Exception as e:
            print(f'[BRIDGE] Send error: {e}')

    def _rx_loop(self):
        """Background thread: receive FPGA state packets."""
        while self._running:
            try:
                data = self.ser.read(64)
                if data:
                    with self._rx_lock:
                        self._rx_buf += data
                        self._drain_packets()
            except Exception:
                pass
            time.sleep(0.005)

    def _drain_packets(self):
        buf = self._rx_buf
        while len(buf) >= 6:
            idx = buf.find(b'CK')
            if idx < 0:
                buf = b''
                break
            if idx > 0:
                buf = buf[idx:]
            if len(buf) < 6:
                break
            length = struct.unpack('<H', buf[3:5])[0]
            total = 6 + length
            if len(buf) < total:
                break
            pkt = parse_packet(buf[:total])
            if pkt:
                self._rx_packets.append(pkt)
            buf = buf[total:]
        self._rx_buf = buf

    def _get_fpga_state(self) -> dict:
        """Pull latest STATE packet if available."""
        with self._rx_lock:
            for i in range(len(self._rx_packets) - 1, -1, -1):
                t, p = self._rx_packets[i]
                if t == PKT_STATE:
                    s = unpack_state(p)
                    del self._rx_packets[i]
                    return s
        return {}

    def _get_ck_state(self) -> dict:
        """Pull CK engine state from Gen11 web API."""
        try:
            req = urllib.request.Request(f'{self.ck_url}/state')
            with urllib.request.urlopen(req, timeout=0.5) as resp:
                return json.loads(resp.read())
        except Exception:
            return {}

    def _apply_gait(self, ck: dict) -> None:
        """Compute gait from CK state and send to FPGA."""
        coherence = float(ck.get('coherence', 0.0))
        operators = ck.get('operators', [])

        # Estimate lambda from operator trajectory
        # lambda = fraction of ops >= PROGRESS(3)
        if operators:
            lam = sum(1 for op in operators if op >= 3) / len(operators)
        else:
            lam = 0.0

        # Build fake state dict for state_to_gait
        fpga_like = {'coherence': coherence}
        gait, reason = state_to_gait(fpga_like)

        if gait is None:
            # E-STOP
            if self._last_gait != 'ESTOP':
                print(f'[BRIDGE] {reason}')
                self._send(pack_estop())
                self._last_gait = 'ESTOP'
                self._estop_count += 1
            return

        # Override with lambda-based phase if we have it
        if lam < 0.09:
            gait = GAIT_STAND
            reason = f'Phase1 (lam={lam:.3f}) -> STAND'
        elif lam < 0.50:
            gait = GAIT_WALK
            reason = f'Phase2 (lam={lam:.3f}) -> WALK'
        else:
            gait = GAIT_TROT
            reason = f'Phase3 (lam={lam:.3f}) -> TROT'

        gait_name = GAIT_NAMES.get(gait, '?')
        if gait_name != self._last_gait:
            print(f'[BRIDGE] Gait change: {self._last_gait} -> {gait_name} ({reason})')
            self._send(pack_gait(gait))
            self._last_gait = gait_name

    def _send_observe(self, ck: dict) -> None:
        """Forward CK operator state to FPGA as OBSERVE packet."""
        try:
            ops = ck.get('operators', [])
            if ops:
                dominant = max(set(ops), key=ops.count)
                pid = int(ck.get('tick', 0)) & 0xFFFFFFFF
                name_hash = sum(ord(c) for c in OP[dominant]) & 0xFFFFFFFF
                self._send(pack_observe(pid, dominant, name_hash))
        except Exception:
            pass

    def _report(self, ck: dict):
        now = time.time()
        if now - self._last_report < REPORT_EVERY:
            return
        self._last_report = now
        coherence = ck.get('coherence', 0.0)
        ops = ck.get('operators', [])
        dominant = max(set(ops), key=ops.count) if ops else -1
        band = 'GREEN' if coherence >= T_STAR else ('YELLOW' if coherence >= 0.4 else 'RED')
        fpga = self._last_fpga_state
        gait_mode = fpga.get('gait_mode', '?')
        gait_str = GAIT_NAMES.get(gait_mode, str(gait_mode))
        print(f'[BRIDGE] tick={self._tick:6d} | '
              f'C={coherence:.3f} {band} | '
              f'op={OP[dominant] if dominant >= 0 else "?"} | '
              f'gait={self._last_gait or "?"} (FPGA:{gait_str}) | '
              f'estops={self._estop_count}')

    def run(self):
        print(f'\n[BRIDGE] CK R16 Dog Bridge')
        print(f'FPGA:   {self.port} @ {BAUD}')
        print(f'Engine: {self.ck_url}')
        print(f'Rate:   {BRIDGE_HZ} Hz | Report every {REPORT_EVERY}s')
        print('Press Ctrl+C to stop (sends ESTOP first)\n')

        if not self.connect():
            return

        self._running = True
        rx_thread = threading.Thread(target=self._rx_loop, daemon=True)
        rx_thread.start()

        # Initial ping
        self._send(pack_ping())
        time.sleep(0.1)

        interval = 1.0 / BRIDGE_HZ
        try:
            while True:
                t0 = time.time()

                # 1. Get CK engine state
                ck = self._get_ck_state()

                if ck:
                    # 2. Drive gait from CK coherence + phase
                    self._apply_gait(ck)

                    # 3. Forward operator observations
                    self._send_observe(ck)

                    # 4. Status report
                    self._report(ck)

                # 5. Receive any FPGA state updates
                fpga = self._get_fpga_state()
                if fpga:
                    self._last_fpga_state = fpga

                self._tick += 1
                elapsed = time.time() - t0
                sleep = max(0, interval - elapsed)
                time.sleep(sleep)

        except KeyboardInterrupt:
            print('\n[BRIDGE] Interrupted. Sending ESTOP...')
        finally:
            self._running = False
            try:
                self._send(pack_estop())
                time.sleep(0.1)
            except Exception:
                pass
            if self.ser:
                self.ser.close()
            print('[BRIDGE] Stopped.')


def main():
    parser = argparse.ArgumentParser(description='CK R16 Dog Bridge')
    parser.add_argument('--port', default='COM3',
                        help='FPGA serial port (default: COM3)')
    parser.add_argument('--ck-url', default='http://localhost:7778',
                        help='CK engine URL (default: http://localhost:7778)')
    args = parser.parse_args()

    bridge = R16Bridge(port=args.port, ck_url=args.ck_url)
    bridge.run()


if __name__ == '__main__':
    main()
