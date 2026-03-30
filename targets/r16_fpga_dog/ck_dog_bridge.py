"""
ck_dog_bridge.py -- R16 <-> FPGA UART Bridge
=============================================
Operator: BALANCE (5) -- the bridge between bodies.

Runs as a background thread on the R16 machine.
Connects the 50Hz CK engine to the Zynq-7020 FPGA via USB-serial.

Data flow:
  R16 Engine (50Hz)
    -> OBSERVE packets: current operator + 5D force vector + coherence
    -> GAIT packets:    gait_mode from 3-Lattice phase detector (5Hz)
    -> LED packets:     operator visualization (1Hz)
  Zynq-7020 FPGA
    -> STATE packets:   phase_bc, coherence, health_flags (50Hz)
    -> CRYSTAL packets: pattern notifications (on event)
    -> SERVO_POS:       joint positions (2Hz)

The bridge also enforces the ESTOP invariant:
  if coherence < 0.20 for ESTOP_HOLD_TICKS consecutive ticks:
    -> send ESTOP packet -> FPGA centers all servos

Usage:
    bridge = CKDogBridge(port='COM3', baud=115200)
    bridge.attach_engine(engine)  # pass CKSimEngine instance
    bridge.start()                # starts background thread

    # From main thread:
    state = bridge.last_state     # latest STATE packet from FPGA
    bridge.stop()                 # graceful shutdown

(c) 2026 Brayden Sanders / 7Site LLC -- Trinity Infinity Geometry
"""

import serial
import threading
import time
import queue
import struct
import sys
from typing import Optional

from ck_sim_uart import (
    PacketParser,
    make_observe_packet, make_gait_packet, make_ping_packet,
    make_estop_packet, make_led_packet,
    parse_state_payload, parse_crystal_payload,
    parse_servo_pos_payload, parse_proximity_payload,
    PKT_STATE, PKT_CRYSTAL, PKT_SERVO_POS, PKT_PROXIMITY,
    PKT_PONG, PKT_DECISION,
    BAND_GREEN, BAND_YELLOW, BAND_RED,
)
from ck_gait_phase import GaitPhaseState, coherence_to_corridor

# ── Constants ──────────────────────────────────────────────────────────────

TICK_HZ         = 50       # Engine tick rate
GAIT_EVERY      = 10       # Send GAIT every N ticks (5Hz)
LED_EVERY       = 50       # Send LED every N ticks  (1Hz)
PING_EVERY      = 250      # PING every N ticks       (0.2Hz / 5s)
SERVO_POS_EVERY = 100      # Request servo positions every N ticks (0.5Hz)

ESTOP_COHERENCE = 0.20     # Absolute floor
ESTOP_HOLD      = 10       # Ticks below floor before ESTOP (0.2s)

# Operator -> LED pattern (4-bit, matching ck_top_zynq7020.v LED logic)
OP_LED = {
    0: 0x0,   # VOID    -> off
    1: 0x1,   2: 0x3,   3: 0x5,   # LATTICE, COUNTER, PROGRESS
    4: 0x6,   5: 0x8,   6: 0xA,   # COLLAPSE, BALANCE, CHAOS
    7: 0xF,   8: 0xC,   9: 0xE,   # HARMONY -> full, BREATH, RESET
}

BAND_MAP = {'GREEN': BAND_GREEN, 'YELLOW': BAND_YELLOW, 'RED': BAND_RED}


class CKDogBridge:
    """
    Background thread: syncs R16 CK engine to Zynq-7020 FPGA.

    Thread safety: engine is read-only from bridge thread (no writes).
    last_state, last_crystal are written by bridge thread, readable by main.
    Use bridge.lock if atomicity matters for multi-field reads.
    """

    def __init__(self, port: str, baud: int = 115200, verbose: bool = False):
        self.port    = port
        self.baud    = baud
        self.verbose = verbose

        self._engine   = None
        self._serial   = None
        self._thread   = None
        self._running  = False
        self._tx_queue = queue.Queue(maxsize=64)

        self.lock          = threading.Lock()
        self.last_state    = {}       # Latest parsed STATE from FPGA
        self.last_crystal  = {}       # Latest CRYSTAL event
        self.last_servo_pos= []       # Latest servo positions (8 values)
        self.last_imu      = {}       # Latest IMU data

        self.fpga_coherence = 0.0     # Smoothed coherence from FPGA
        self.fpga_alive     = False   # True if FPGA is responding

        self._gait    = GaitPhaseState()
        self._estop_count = 0
        self._estopped    = False

        # Stats
        self.tx_count   = 0
        self.rx_count   = 0
        self.crc_errors = 0
        self._ping_sent = 0
        self._pong_recv = 0
        self._start_time = 0.0

    def attach_engine(self, engine) -> 'CKDogBridge':
        """Attach CKSimEngine for reading state. Returns self for chaining."""
        self._engine = engine
        return self

    # ── Public control ──────────────────────────────────────────────────────

    def start(self):
        """Open serial port and start bridge thread."""
        try:
            self._serial = serial.Serial(
                self.port, self.baud,
                bytesize=serial.EIGHTBITS,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                timeout=0.005,     # 5ms read timeout (non-blocking feel)
                write_timeout=0.1,
            )
            print(f"[BRIDGE] Serial {self.port} @ {self.baud} baud: OK")
        except serial.SerialException as e:
            print(f"[BRIDGE] Cannot open {self.port}: {e}")
            raise

        self._running    = True
        self._start_time = time.monotonic()
        self._thread = threading.Thread(
            target=self._run, daemon=True, name='ck-dog-bridge')
        self._thread.start()
        print(f"[BRIDGE] Bridge thread started -> FPGA at {self.port}")

    def stop(self, send_estop: bool = True):
        """Graceful shutdown. Optionally sends ESTOP before closing."""
        self._running = False
        if send_estop and self._serial and self._serial.is_open:
            try:
                self._serial.write(make_estop_packet(reason=0))
                time.sleep(0.05)
            except Exception:
                pass
        if self._thread:
            self._thread.join(timeout=2.0)
        if self._serial:
            try:
                self._serial.close()
            except Exception:
                pass
        print("[BRIDGE] Bridge stopped.")

    def send_estop(self, reason: int = 3):
        """Send ESTOP immediately (thread-safe, non-blocking)."""
        pkt = make_estop_packet(reason)
        self._enqueue(pkt, priority=True)

    # ── Internal ────────────────────────────────────────────────────────────

    def _enqueue(self, pkt: bytes, priority: bool = False):
        """Put packet in TX queue. Drops if full (non-blocking)."""
        try:
            if priority:
                # Drain queue and put at front isn't trivially possible
                # with queue.Queue; just put it in (ESTOP is small, fast)
                self._tx_queue.put_nowait(pkt)
            else:
                self._tx_queue.put_nowait(pkt)
        except queue.Full:
            pass  # Drop non-critical packets under overload

    def _send_now(self, pkt: bytes):
        """Write packet directly to serial (call only from bridge thread)."""
        try:
            self._serial.write(pkt)
            self.tx_count += 1
        except serial.SerialException as e:
            print(f"[BRIDGE] TX error: {e}")

    def _run(self):
        """Bridge thread main loop."""
        parser   = PacketParser()
        tick     = 0
        deadline = time.monotonic()

        while self._running:
            # ── Tick timing (50Hz) ──
            deadline += 1.0 / TICK_HZ
            now = time.monotonic()
            sleep_t = deadline - now
            if sleep_t > 0:
                time.sleep(sleep_t)
            tick += 1

            # ── Read from serial (RX) ──
            try:
                waiting = self._serial.in_waiting
                if waiting > 0:
                    raw = self._serial.read(min(waiting, 256))
                    for pkt_type, payload in parser.feed_bytes(raw):
                        self._handle_rx(pkt_type, payload)
            except serial.SerialException as e:
                print(f"[BRIDGE] RX error: {e}")
                break

            # ── Build and send packets (TX) ──
            self._build_tx(tick)

            # ── Flush TX queue ──
            while not self._tx_queue.empty():
                try:
                    pkt = self._tx_queue.get_nowait()
                    self._send_now(pkt)
                except queue.Empty:
                    break

        self.crc_errors = parser.crc_errors
        print(f"[BRIDGE] Loop ended. TX={self.tx_count} "
              f"RX={self.rx_count} CRC_err={parser.crc_errors}")

    def _build_tx(self, tick: int):
        """Build outgoing packets for this tick."""
        eng = self._engine

        # Read engine state (read-only, no lock needed for individual fields)
        op         = self._read_op(eng)
        force_vec  = self._read_force(eng)
        coherence  = self._read_coherence(eng)
        band       = self._read_band(eng)
        corridor   = self._read_corridor(eng)

        # Update gait phase state
        gait_state = self._gait.update(coherence, corridor)

        # ── OBSERVE every tick (50Hz) ──
        obs = make_observe_packet(op, force_vec, coherence, band)
        self._enqueue(obs)

        # ── GAIT every GAIT_EVERY ticks (5Hz) ──
        if tick % GAIT_EVERY == 0:
            if gait_state['estop'] and not self._estopped:
                self._estop_count += 1
                if self._estop_count >= ESTOP_HOLD:
                    print(f"[BRIDGE] ESTOP: coherence={coherence:.4f} "
                          f"< floor {ESTOP_COHERENCE}")
                    self._enqueue(make_estop_packet(reason=1), priority=True)
                    self._estopped = True
            else:
                if not gait_state['estop']:
                    self._estop_count = 0
                    if self._estopped:
                        print(f"[BRIDGE] ESTOP cleared: coherence={coherence:.4f}")
                        self._estopped = False
                gait_pkt = make_gait_packet(
                    gait_state['gait_mode'],
                    gait_state['phase'],
                    gait_state['lambda'],
                )
                self._enqueue(gait_pkt)

            if self.verbose:
                print(f"[BRIDGE] tick={tick:5d} "
                      f"C={coherence:.4f} "
                      f"op={op} "
                      f"phase={gait_state['phase']} "
                      f"gait={gait_state['gait_name']} "
                      f"corridor={corridor or '?'}")

        # ── LED every LED_EVERY ticks (1Hz) ──
        if tick % LED_EVERY == 0:
            led_pattern = OP_LED.get(op, 0x5)
            self._enqueue(make_led_packet(led_pattern))

        # ── PING every PING_EVERY ticks (~5s) ──
        if tick % PING_EVERY == 0:
            self._enqueue(make_ping_packet())
            self._ping_sent += 1

    def _handle_rx(self, pkt_type: int, payload: bytes):
        """Handle received packet from FPGA."""
        self.rx_count += 1
        self.fpga_alive = True

        if pkt_type == PKT_STATE:
            state = parse_state_payload(payload)
            if state:
                with self.lock:
                    self.last_state   = state
                    self.fpga_coherence = state['coherence']
                if self.verbose:
                    print(f"[BRIDGE] STATE: BC={state['phase_bc']} "
                          f"C={state['coherence']:.4f} "
                          f"mode={state['mode']}")

        elif pkt_type == PKT_CRYSTAL:
            crystal = parse_crystal_payload(payload)
            if crystal:
                with self.lock:
                    self.last_crystal = crystal
                print(f"[BRIDGE] CRYSTAL: pattern={crystal['pattern']} "
                      f"fuse={crystal['fuse']} conf={crystal['confidence']:.3f}")

        elif pkt_type == PKT_SERVO_POS:
            pos = parse_servo_pos_payload(payload)
            if pos:
                with self.lock:
                    self.last_servo_pos = pos['positions']

        elif pkt_type == PKT_PROXIMITY:
            imu = parse_proximity_payload(payload)
            if imu:
                with self.lock:
                    self.last_imu = imu

        elif pkt_type == PKT_PONG:
            self._pong_recv += 1
            if len(payload) >= 4:
                sent_ts = struct.unpack_from('<I', payload, 0)[0]
                rtt_ms  = (time.monotonic() * 1000 - sent_ts) % 0x100000000
                if self.verbose:
                    print(f"[BRIDGE] PONG: RTT ~{rtt_ms:.1f}ms")

    # ── Engine state readers (safe defaults when engine is None) ───────────

    def _read_op(self, eng) -> int:
        if eng is None:
            return 7  # HARMONY default
        try:
            hb = getattr(eng, 'heartbeat', None)
            if hb:
                return int(getattr(hb, 'phase_bc', 7))
        except Exception:
            pass
        return 7

    def _read_force(self, eng) -> list:
        if eng is None:
            return [0.5] * 5
        try:
            sens = getattr(eng, 'sensorium', None)
            if sens:
                fv = getattr(sens, 'force_vec', None)
                if fv and len(fv) >= 5:
                    return list(fv[:5])
            lc = getattr(eng, 'lcodec', None)
            if lc:
                fv = getattr(lc, 'last_force_vec', None)
                if fv and len(fv) >= 5:
                    return list(fv[:5])
        except Exception:
            pass
        return [0.5] * 5

    def _read_coherence(self, eng) -> float:
        if eng is None:
            return 0.5
        try:
            return float(getattr(eng, 'coherence', 0.5))
        except Exception:
            return 0.5

    def _read_band(self, eng) -> int:
        if eng is None:
            return BAND_YELLOW
        try:
            band_name = getattr(eng, 'band', 'YELLOW')
            if isinstance(band_name, str):
                return BAND_MAP.get(band_name.upper(), BAND_YELLOW)
            return int(band_name)
        except Exception:
            return BAND_YELLOW

    def _read_corridor(self, eng) -> Optional[str]:
        if eng is None:
            return None
        try:
            steer = getattr(eng, 'steering', None)
            if steer:
                return str(getattr(steer, 'corridor', None))
        except Exception:
            pass
        return None

    # ── Status ──────────────────────────────────────────────────────────────

    @property
    def status(self) -> dict:
        uptime = time.monotonic() - self._start_time if self._start_time else 0
        with self.lock:
            st = dict(self.last_state)
        return {
            'port':          self.port,
            'alive':         self._running,
            'fpga_alive':    self.fpga_alive,
            'fpga_coherence':self.fpga_coherence,
            'estopped':      self._estopped,
            'gait':          self._gait.state,
            'tx':            self.tx_count,
            'rx':            self.rx_count,
            'crc_errors':    self.crc_errors,
            'ping_sent':     self._ping_sent,
            'pong_recv':     self._pong_recv,
            'uptime_s':      uptime,
            'last_state':    st,
        }

    def __repr__(self) -> str:
        s = self.status
        return (f"CKDogBridge({self.port} "
                f"alive={s['fpga_alive']} "
                f"C_fpga={s['fpga_coherence']:.4f} "
                f"gait={s['gait']['gait_name']} "
                f"TX={s['tx']} RX={s['rx']})")


# ── CLI entry point ─────────────────────────────────────────────────────────

if __name__ == '__main__':
    """
    Standalone bridge: runs without a CK engine.
    Useful for testing the FPGA link before the full engine is up.

    Usage: python ck_dog_bridge.py COM3 [--verbose]
    """
    import argparse
    p = argparse.ArgumentParser(description='CK Dog Bridge (standalone)')
    p.add_argument('port', help='Serial port (COM3, /dev/ttyUSB0, etc.)')
    p.add_argument('--baud',    type=int, default=115200)
    p.add_argument('--verbose', action='store_true')
    args = p.parse_args()

    bridge = CKDogBridge(args.port, args.baud, verbose=args.verbose)
    bridge.start()

    print(f"\n[BRIDGE] Running standalone on {args.port}")
    print("[BRIDGE] No engine attached -- sending HARMONY defaults")
    print("[BRIDGE] Ctrl+C to stop\n")

    try:
        while True:
            time.sleep(5)
            print(bridge)
    except KeyboardInterrupt:
        pass
    finally:
        bridge.stop()
