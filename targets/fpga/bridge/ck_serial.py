"""
ck_serial.py -- USB Serial Bridge: Zybo <-> Windows Host
=========================================================
Operator: BALANCE (5) -- the bridge between two bodies.

This runs on the WINDOWS side. It talks to CK on the Zybo
over USB serial (the Zybo's micro-USB shows up as a COM port).

Protocol: binary packets, minimal overhead.
  - Host -> Zybo: commands, observations from Windows, process data
  - Zybo -> Host: heartbeat state, sovereignty decisions, scheduling actions

Packet format:
  [SYNC 0xCK] [TYPE 1B] [LEN 2B little-endian] [PAYLOAD LEN bytes] [CRC8 1B]

Packet types:
  Host -> Zybo:
    0x01  OBSERVE     Process observation (pid, op, name_hash)
    0x02  SWARM       Swarm summary (total, hot, cold, coherence)
    0x03  DEEP_OBS    Deep kernel metrics (io, ctx, mem, interrupts)
    0x04  CONFIG      Configuration update
    0x05  TL_CHUNK    TL data transfer (for loading master_tl)
    0x06  PING        Heartbeat check

  Zybo -> Host:
    0x81  STATE       Full heartbeat state (phases, coherence, tick, fuse)
    0x82  DECISION    Scheduling decision (pid, action, priority)
    0x83  CRYSTAL     New crystal formed (pattern, fuse, confidence)
    0x84  DOMAIN      Domain sovereignty change
    0x85  TL_REQUEST  Request TL data from host
    0x86  PONG        Heartbeat response

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import struct
import time
import threading
from collections import deque

# Packet sync bytes
SYNC = b'\\xCK'  # 0x43, 0x4B = "CK" in ASCII
SYNC_BYTES = b'\\x43\\x4B'

# Packet types
# Host -> Zybo
PKT_OBSERVE   = 0x01
PKT_SWARM     = 0x02
PKT_DEEP_OBS  = 0x03
PKT_CONFIG    = 0x04
PKT_TL_CHUNK  = 0x05
PKT_PING      = 0x06

# Zybo -> Host
PKT_STATE     = 0x81
PKT_DECISION  = 0x82
PKT_CRYSTAL   = 0x83
PKT_DOMAIN    = 0x84
PKT_TL_REQ    = 0x85
PKT_PONG      = 0x86

# Operator names for display
OP = ['VOID','LATTICE','COUNTER','PROGRESS','COLLAPSE',
      'BALANCE','CHAOS','HARMONY','BREATH','RESET']


def crc8(data: bytes) -> int:
    """CRC-8/MAXIM -- simple, fast, good for short packets."""
    crc = 0x00
    for byte in data:
        crc ^= byte
        for _ in range(8):
            if crc & 0x80:
                crc = (crc << 1) ^ 0x31
            else:
                crc = crc << 1
            crc &= 0xFF
    return crc


def make_packet(pkt_type: int, payload: bytes = b'') -> bytes:
    """Build a CK serial packet."""
    length = len(payload)
    header = struct.pack('<2sBH', b'CK', pkt_type, length)
    packet = header + payload
    crc = crc8(packet)
    return packet + struct.pack('B', crc)


def parse_packet(data: bytes):
    """Parse a CK serial packet. Returns (type, payload) or None."""
    if len(data) < 6:  # minimum: sync(2) + type(1) + len(2) + crc(1)
        return None
    if data[0:2] != b'CK':
        return None

    pkt_type = data[2]
    length = struct.unpack('<H', data[3:5])[0]

    if len(data) < 5 + length + 1:
        return None

    payload = data[5:5 + length]
    crc_received = data[5 + length]
    crc_computed = crc8(data[:5 + length])

    if crc_received != crc_computed:
        return None

    return (pkt_type, payload)


# ── Packet builders (Host -> Zybo) ──

def pack_observe(pid: int, op: int, name_hash: int) -> bytes:
    """Pack a process observation."""
    payload = struct.pack('<IBI', pid, op, name_hash)
    return make_packet(PKT_OBSERVE, payload)


def pack_swarm(total: int, hot: int, cold: int, coherence: float) -> bytes:
    """Pack swarm summary."""
    payload = struct.pack('<IIIf', total, hot, cold, coherence)
    return make_packet(PKT_SWARM, payload)


def pack_deep_obs(io_ops: int, ctx_switches: int, page_faults: int,
                  interrupts: int, mem_used_mb: int) -> bytes:
    """Pack deep kernel observation."""
    payload = struct.pack('<IIIII', io_ops, ctx_switches, page_faults,
                          interrupts, mem_used_mb)
    return make_packet(PKT_DEEP_OBS, payload)


def pack_ping() -> bytes:
    """Pack ping."""
    payload = struct.pack('<d', time.time())
    return make_packet(PKT_PING, payload)


# ── Packet parsers (Zybo -> Host) ──

def unpack_state(payload: bytes) -> dict:
    """Unpack heartbeat state from Zybo."""
    if len(payload) < 20:
        return {}
    b, d, bc, fuse_op, bump = struct.unpack('<BBBBB', payload[0:5])
    tick_count, = struct.unpack('<I', payload[5:9])
    coh_num, coh_den = struct.unpack('<HH', payload[9:13])
    brain_ticks, = struct.unpack('<I', payload[13:17])
    mode, domain_count, _ = struct.unpack('<BBB', payload[17:20])
    return {
        'phase_b': b, 'phase_d': d, 'phase_bc': bc,
        'fuse': fuse_op, 'bump': bool(bump),
        'tick_count': tick_count,
        'coherence': coh_num / max(coh_den, 1),
        'brain_ticks': brain_ticks,
        'mode': mode,
        'domains': domain_count,
    }


def unpack_decision(payload: bytes) -> dict:
    """Unpack scheduling decision from Zybo."""
    if len(payload) < 9:
        return {}
    pid, action, priority = struct.unpack('<IBf', payload[0:9])
    return {'pid': pid, 'action': action, 'priority': priority}


def unpack_crystal(payload: bytes) -> dict:
    """Unpack new crystal notification."""
    if len(payload) < 13:
        return {}
    pattern_len = payload[0]
    pattern = list(payload[1:1 + pattern_len])
    offset = 1 + pattern_len
    fuse_op = payload[offset]
    confidence = struct.unpack('<f', payload[offset+1:offset+5])[0]
    seen = struct.unpack('<I', payload[offset+5:offset+9])[0]
    return {
        'pattern': pattern,
        'fuse': fuse_op,
        'confidence': confidence,
        'seen': seen,
    }


# ── Bridge class ──

class ZyboBridge:
    """USB serial bridge between Windows CK and Zybo CK.

    Usage:
        bridge = ZyboBridge('COM3')  # or whatever port Zybo shows up as
        bridge.connect()
        bridge.send_swarm(swarm.latest)
        state = bridge.read_state()
    """

    def __init__(self, port: str, baudrate: int = 115200):
        self.port = port
        self.baudrate = baudrate
        self.serial = None
        self.connected = False
        self.rx_buffer = bytearray()
        self.rx_queue = deque(maxlen=1000)
        self.tx_count = 0
        self.rx_count = 0
        self.last_state = None
        self.last_ping_rtt = 0.0

    def connect(self):
        """Open serial connection to Zybo."""
        import serial
        self.serial = serial.Serial(
            port=self.port,
            baudrate=self.baudrate,
            timeout=0.01,     # 10ms read timeout
            write_timeout=0.1,
        )
        self.connected = True
        print(f"  [ZYBO] Connected on {self.port} @ {self.baudrate} baud")

    def disconnect(self):
        """Close serial connection."""
        if self.serial:
            self.serial.close()
        self.connected = False
        print(f"  [ZYBO] Disconnected")

    def send(self, packet: bytes):
        """Send a packet to the Zybo."""
        if not self.connected:
            return
        self.serial.write(packet)
        self.tx_count += 1

    def send_swarm_summary(self, swarm_latest: dict):
        """Send swarm summary to Zybo."""
        self.send(pack_swarm(
            total=swarm_latest.get('total_processes', 0),
            hot=swarm_latest.get('hot', 0),
            cold=swarm_latest.get('cold', 0),
            coherence=swarm_latest.get('system_coherence', 0.5),
        ))

    def send_observation(self, pid: int, op: int, name: str):
        """Send a process observation to Zybo."""
        name_hash = hash(name) & 0xFFFFFFFF
        self.send(pack_observe(pid, op, name_hash))

    def send_deep_obs(self, deep_latest: dict):
        """Send deep kernel observation to Zybo."""
        self.send(pack_deep_obs(
            io_ops=int(deep_latest.get('io_data_ops', 0)),
            ctx_switches=int(deep_latest.get('ctx_switches', 0)),
            page_faults=int(deep_latest.get('page_faults', 0)),
            interrupts=int(deep_latest.get('interrupts', 0)),
            mem_used_mb=int(deep_latest.get('mem_used_mb', 0)),
        ))

    def ping(self) -> float:
        """Send ping, wait for pong, return RTT in ms."""
        t0 = time.perf_counter()
        self.send(pack_ping())
        # Wait for pong (up to 100ms)
        deadline = t0 + 0.1
        while time.perf_counter() < deadline:
            self._read_available()
            for pkt_type, payload in self._drain_queue():
                if pkt_type == PKT_PONG:
                    rtt = (time.perf_counter() - t0) * 1000
                    self.last_ping_rtt = rtt
                    return rtt
        return -1.0  # timeout

    def read_state(self) -> dict:
        """Read latest heartbeat state from Zybo."""
        self._read_available()
        for pkt_type, payload in self._drain_queue():
            if pkt_type == PKT_STATE:
                self.last_state = unpack_state(payload)
                return self.last_state
        return self.last_state or {}

    def read_decisions(self) -> list:
        """Read all pending scheduling decisions from Zybo."""
        self._read_available()
        decisions = []
        for pkt_type, payload in self._drain_queue():
            if pkt_type == PKT_DECISION:
                decisions.append(unpack_decision(payload))
        return decisions

    def _read_available(self):
        """Read available bytes from serial into buffer."""
        if not self.connected:
            return
        try:
            data = self.serial.read(self.serial.in_waiting or 1)
            if data:
                self.rx_buffer.extend(data)
                self._parse_buffer()
        except Exception:
            pass

    def _parse_buffer(self):
        """Parse complete packets from rx_buffer."""
        while len(self.rx_buffer) >= 6:
            # Find sync
            idx = self.rx_buffer.find(b'CK')
            if idx < 0:
                self.rx_buffer.clear()
                return
            if idx > 0:
                self.rx_buffer = self.rx_buffer[idx:]

            if len(self.rx_buffer) < 6:
                return

            pkt_type = self.rx_buffer[2]
            length = struct.unpack('<H', bytes(self.rx_buffer[3:5]))[0]
            total_len = 5 + length + 1  # header + payload + crc

            if len(self.rx_buffer) < total_len:
                return  # wait for more data

            packet_data = bytes(self.rx_buffer[:total_len])
            result = parse_packet(packet_data)
            self.rx_buffer = self.rx_buffer[total_len:]

            if result:
                self.rx_queue.append(result)
                self.rx_count += 1

    def _drain_queue(self):
        """Yield all queued packets."""
        while self.rx_queue:
            yield self.rx_queue.popleft()

    def report_line(self) -> str:
        """One-line status for daemon verbose output."""
        state = self.last_state or {}
        return (f"    [ZYBO] ticks={state.get('tick_count', 0)} "
                f"B={OP[state.get('phase_b', 0)]} "
                f"D={OP[state.get('phase_d', 0)]} "
                f"BC={OP[state.get('phase_bc', 0)]} "
                f"coh={state.get('coherence', 0):.4f} "
                f"mode={state.get('mode', 0)} "
                f"rtt={self.last_ping_rtt:.1f}ms "
                f"tx={self.tx_count} rx={self.rx_count}")
