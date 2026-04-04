"""
ck_protocol.py -- CK Binary Packet Protocol (R16 <-> FPGA)
===========================================================
Operator: BALANCE (5) -- the bridge between bodies.

Full CK serial packet protocol plus dog-specific extensions.
Used by ck_leash_test.py and ck_r16_bridge.py.

Packet format:
  [SYNC 'CK'] [TYPE 1B] [LEN 2B LE] [PAYLOAD] [CRC8]

(c) 2026 Brayden Sanders / 7Site LLC -- Trinity Infinity Geometry
"""

import struct
import time

# ── Operators ──
OP = ['VOID', 'LATTICE', 'COUNTER', 'PROGRESS', 'COLLAPSE',
      'BALANCE', 'CHAOS', 'HARMONY', 'BREATH', 'RESET']
OP_IDX = {name: i for i, name in enumerate(OP)}

T_STAR = 5.0 / 7.0  # 0.714285... algebraically forced coherence threshold

# ── Packet Types ──
# Host -> FPGA
PKT_OBSERVE  = 0x01   # Process observation (pid, op, name_hash)
PKT_SWARM    = 0x02   # Swarm summary
PKT_DEEP_OBS = 0x03   # Deep kernel metrics
PKT_CONFIG   = 0x04   # Configuration
PKT_TL_CHUNK = 0x05   # TL data
PKT_PING     = 0x06   # Heartbeat check
PKT_GAIT     = 0x23   # Dog gait command (mode, speed)
PKT_ESTOP    = 0x2E   # Dog emergency stop

# FPGA -> Host
PKT_STATE    = 0x81   # Full heartbeat state
PKT_DECISION = 0x82   # Scheduling decision
PKT_CRYSTAL  = 0x83   # New crystal formed
PKT_DOMAIN   = 0x84   # Domain sovereignty change
PKT_TL_REQ   = 0x85   # TL data request
PKT_PONG     = 0x86   # Heartbeat response

# Gait modes (maps to gait_vortex.v modes)
GAIT_STAND = 0x00
GAIT_WALK  = 0x01
GAIT_TROT  = 0x02
GAIT_BOUND = 0x03

GAIT_NAMES = {GAIT_STAND: 'STAND', GAIT_WALK: 'WALK',
              GAIT_TROT: 'TROT', GAIT_BOUND: 'BOUND'}

# Phase -> gait mapping (from memory: Phase1/lambda<0.09 -> STAND etc.)
# lambda = BTQ lambda (gate score). Low lambda = low doing energy.
PHASE_TO_GAIT = {
    1: GAIT_STAND,   # Phase1: lambda < 0.09, field still settling
    2: GAIT_WALK,    # Phase2: lambda 0.09-0.50, building momentum
    3: GAIT_TROT,    # Phase3: lambda > 0.50, full doing energy
}
LAMBDA_THRESHOLDS = {
    'phase1': 0.09,
    'phase2': 0.50,
}
ESTOP_COHERENCE = 0.20   # Below this coherence: emergency stop

PKT_NAMES = {
    PKT_OBSERVE: 'OBSERVE', PKT_SWARM: 'SWARM', PKT_DEEP_OBS: 'DEEP_OBS',
    PKT_CONFIG: 'CONFIG', PKT_TL_CHUNK: 'TL_CHUNK', PKT_PING: 'PING',
    PKT_GAIT: 'GAIT', PKT_ESTOP: 'ESTOP',
    PKT_STATE: 'STATE', PKT_DECISION: 'DECISION', PKT_CRYSTAL: 'CRYSTAL',
    PKT_DOMAIN: 'DOMAIN', PKT_TL_REQ: 'TL_REQ', PKT_PONG: 'PONG',
}


def crc8(data: bytes) -> int:
    """CRC-8/MAXIM polynomial 0x31. Matches ARM firmware."""
    crc = 0x00
    for byte in data:
        crc ^= byte
        for _ in range(8):
            crc = ((crc << 1) ^ 0x31) if (crc & 0x80) else (crc << 1)
            crc &= 0xFF
    return crc


def make_packet(pkt_type: int, payload: bytes = b'') -> bytes:
    """Build a CK binary packet."""
    header = struct.pack('<2sBH', b'CK', pkt_type, len(payload))
    body = header + payload
    return body + struct.pack('B', crc8(body))


def parse_packet(data: bytes):
    """Parse one CK packet. Returns (type, payload) or None."""
    if len(data) < 6:
        return None
    if data[0:2] != b'CK':
        return None
    pkt_type = data[2]
    length = struct.unpack('<H', data[3:5])[0]
    if len(data) < 5 + length + 1:
        return None
    payload = data[5:5 + length]
    if data[5 + length] != crc8(data[:5 + length]):
        return None
    return (pkt_type, payload)


# ── Packet Builders (Host -> FPGA) ──

def pack_ping() -> bytes:
    return make_packet(PKT_PING, struct.pack('<d', time.time()))


def pack_observe(pid: int, op: int, name_hash: int) -> bytes:
    return make_packet(PKT_OBSERVE, struct.pack('<IBI', pid, op, name_hash))


def pack_swarm(total: int, hot: int, cold: int, coherence: float) -> bytes:
    return make_packet(PKT_SWARM, struct.pack('<IIIf', total, hot, cold, coherence))


def pack_gait(mode: int, speed: int = 100) -> bytes:
    """Send gait command. mode=GAIT_*, speed=0-255."""
    return make_packet(PKT_GAIT, struct.pack('<BB', mode & 0x03, speed & 0xFF))


def pack_estop() -> bytes:
    """Emergency stop: centers all servos immediately."""
    return make_packet(PKT_ESTOP, b'')


# ── Packet Parsers (FPGA -> Host) ──

def unpack_state(payload: bytes) -> dict:
    """Unpack full heartbeat state from FPGA."""
    if len(payload) < 17:
        return {}
    b_op, d_op, bc_op, fuse_op, bump = struct.unpack('<BBBBB', payload[0:5])
    tick_count, = struct.unpack('<I', payload[5:9])
    coh_num, coh_den = struct.unpack('<HH', payload[9:13])
    brain_ticks, = struct.unpack('<I', payload[13:17])

    coherence = coh_num / max(coh_den, 1)
    result = {
        'being':       b_op,
        'doing':       d_op,
        'becoming':    bc_op,
        'fuse':        fuse_op,
        'bump':        bool(bump),
        'tick':        tick_count,
        'coherence':   coherence,
        'brain_ticks': brain_ticks,
        'coh_num':     coh_num,
        'coh_den':     coh_den,
    }

    # Optional: gait state appended after base fields
    if len(payload) >= 21:
        gait_mode, gait_phase, aligned_mask, gait_coh = \
            struct.unpack('<BBBB', payload[17:21])
        result.update({
            'gait_mode':    gait_mode,
            'gait_phase':   gait_phase,
            'legs_aligned': aligned_mask,
            'gait_coh':     gait_coh / 4.0,
        })

    return result


def unpack_pong(payload: bytes) -> dict:
    """Unpack PONG response."""
    if len(payload) < 8:
        return {'latency_ms': -1}
    ts_sent, = struct.unpack('<d', payload[:8])
    latency_ms = (time.time() - ts_sent) * 1000
    return {'latency_ms': latency_ms}


def classify_phase(coherence: float, lambda_val: float = 0.0) -> int:
    """Classify CK state into TIG phase 1/2/3."""
    if lambda_val > 0:
        if lambda_val < LAMBDA_THRESHOLDS['phase1']:
            return 1
        elif lambda_val < LAMBDA_THRESHOLDS['phase2']:
            return 2
        else:
            return 3
    # Fallback: use coherence only
    if coherence < 0.35:
        return 1
    elif coherence < T_STAR:
        return 2
    else:
        return 3


def state_to_gait(state: dict) -> tuple:
    """Map FPGA state to gait command. Returns (gait_mode, reason)."""
    coherence = state.get('coherence', 0.0)

    if coherence < ESTOP_COHERENCE:
        return (None, f'ESTOP: coherence {coherence:.3f} < {ESTOP_COHERENCE}')

    phase = classify_phase(coherence)
    gait = PHASE_TO_GAIT.get(phase, GAIT_STAND)
    reason = f'Phase{phase} -> {GAIT_NAMES[gait]} (C={coherence:.3f})'

    return (gait, reason)
