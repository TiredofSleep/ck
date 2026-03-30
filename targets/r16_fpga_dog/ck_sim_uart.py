"""
ck_sim_uart.py -- CK Serial Protocol (Gen10 dog target)
=========================================================
Operator: BALANCE (5) -- the bridge between bodies.

Packet encode/decode for R16 <-> Zynq-7020 UART link.
Protocol identical to Gen9/targets/fpga/sim/ck_sim_uart.py plus
dog-specific OBSERVE/GAIT/ESTOP encode helpers.

Packet format: [SYNC 'CK'] [TYPE 1B] [LEN 2B LE] [PAYLOAD] [CRC8]
CRC-8/MAXIM covers SYNC + TYPE + LEN + PAYLOAD.

Physical link: 115200 baud 8N1 over USB-serial (CP2102 / CH340 / FTDI)
  R16 COM port -> Zybo Z7-20 PS UART0 (MIO 14/15, appears as /dev/ttyUSBx or COMx)

(c) 2026 Brayden Sanders / 7Site LLC -- Trinity Infinity Geometry
"""

import struct
import time

# ── Packet types (matching ck_uart.h exactly) ──────────────────────────────

# Host -> Zynq
PKT_OBSERVE   = 0x01   # Inject operator + 5D force vector into FPGA brain
PKT_SWARM     = 0x02   # Swarm field update
PKT_DEEP_OBS  = 0x03   # Deep observation (full TL state)
PKT_CONFIG    = 0x04   # Config register write
PKT_TL_CHUNK  = 0x05   # TL memory chunk transfer
PKT_PING      = 0x06   # Ping (echoed as PONG with same payload)

# Zynq -> Host
PKT_STATE     = 0x81   # Heartbeat state (20 bytes, sent every 50Hz tick)
PKT_DECISION  = 0x82   # BTQ decision
PKT_CRYSTAL   = 0x83   # Pattern crystal detected
PKT_DOMAIN    = 0x84   # Domain activation
PKT_TL_REQ    = 0x85   # TL memory request
PKT_PONG      = 0x86   # Ping response

# Dog-specific (bidirectional)
PKT_MOTOR     = 0x20   # Raw motor command (direct microseconds)
PKT_LED_CMD   = 0x21   # LED pattern
PKT_SERVO     = 0x22   # Servo position read request / response
PKT_GAIT      = 0x23   # Gait mode command (Host -> Zynq)
PKT_ESTOP     = 0x2E   # Emergency stop (Host -> Zynq, immediate)
PKT_SENSOR    = 0xA0   # Sensor data (Zynq -> Host)
PKT_SERVO_POS = 0xA1   # Servo position report (Zynq -> Host)
PKT_PROXIMITY = 0xA2   # Proximity / IMU data (Zynq -> Host)

SYNC_0 = 0x43  # 'C'
SYNC_1 = 0x4B  # 'K'
HEADER_SIZE = 5
MAX_PAYLOAD = 256

# ── Band constants ──────────────────────────────────────────────────────────
BAND_GREEN  = 0
BAND_YELLOW = 1
BAND_RED    = 2
BAND_NAMES  = {BAND_GREEN: 'GREEN', BAND_YELLOW: 'YELLOW', BAND_RED: 'RED'}


# ── CRC-8/MAXIM ────────────────────────────────────────────────────────────

def crc8(data: bytes) -> int:
    """CRC-8/MAXIM polynomial 0x31. Matches ck_uart_crc8() exactly."""
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


# ── Packet builder ─────────────────────────────────────────────────────────

def make_packet(pkt_type: int, payload: bytes = b'') -> bytes:
    """Build a CK serial packet. Wire-compatible with ck_uart_send()."""
    header = struct.pack('<2sBH', b'CK', pkt_type, len(payload))
    body   = header + payload
    return body + bytes([crc8(body)])


# ── Host -> Zynq packet builders ───────────────────────────────────────────

def make_observe_packet(op: int, force_vec: list,
                        coherence: float, band: int) -> bytes:
    """
    OBSERVE (0x01) payload = 14 bytes:
      [0]      op         : u8     current operator (0-9)
      [1-2]    force_d1   : u16 LE aperture    [0..10000 = 0.0..1.0]
      [3-4]    force_d2   : u16 LE pressure
      [5-6]    force_d3   : u16 LE depth
      [7-8]    force_d4   : u16 LE binding
      [9-10]   force_d5   : u16 LE continuity
      [11-12]  coherence  : u16 LE [0..10000 = 0.0..1.0]
      [13]     band       : u8     0=GREEN 1=YELLOW 2=RED

    force_vec: list of 5 floats [0.0..1.0]
    """
    fv = list(force_vec) + [0.0] * 5
    fv = fv[:5]
    d1, d2, d3, d4, d5 = [min(10000, max(0, int(f * 10000))) for f in fv]
    coh16 = min(10000, max(0, int(coherence * 10000)))
    payload = struct.pack('<B5H HB',
                          op & 0x0F,
                          d1, d2, d3, d4, d5,
                          coh16, band & 0x03)
    return make_packet(PKT_OBSERVE, payload)


def make_gait_packet(gait_mode: int, tig_phase: int,
                     lambda_val: float) -> bytes:
    """
    GAIT (0x23) payload = 4 bytes:
      [0]   gait_mode   : u8  0=STAND 1=WALK 2=TROT 3=BOUND
      [1]   tig_phase   : u8  1/2/3 (3-Lattice phase)
      [2-3] lambda_x10k : u16 LE  λ × 10000

    gait_mode mapping from 3-Lattice phase:
      Phase 1 (Grammar,  λ < 0.09) -> STAND (0)
      Phase 2 (Transit,  0.09-0.45) -> WALK  (1)
      Phase 3 (Order,    λ >= 0.45) -> TROT  (2)
    """
    lam16 = min(65535, max(0, int(lambda_val * 10000)))
    payload = struct.pack('<BBH',
                          gait_mode & 0x03,
                          tig_phase & 0x03,
                          lam16)
    return make_packet(PKT_GAIT, payload)


def make_ping_packet() -> bytes:
    """PING (0x06) payload = 4 bytes: timestamp in ms."""
    ts = int(time.monotonic() * 1000) & 0xFFFFFFFF
    return make_packet(PKT_PING, struct.pack('<I', ts))


def make_estop_packet(reason: int = 0) -> bytes:
    """
    ESTOP (0x2E) payload = 1 byte:
      0 = normal stop
      1 = coherence below floor (0.2)
      2 = software error
      3 = manual (user initiated)
    """
    return make_packet(PKT_ESTOP, bytes([reason & 0xFF]))


def make_led_packet(pattern: int) -> bytes:
    """LED_CMD (0x21) payload = 1 byte: 4-bit LED pattern."""
    return make_packet(PKT_LED_CMD, bytes([pattern & 0x0F]))


# ── Zynq -> Host packet builders (for loopback testing) ────────────────────

def make_state_packet(phase_b, phase_d, phase_bc, fuse_op, bump,
                      tick_count, coh_num, coh_den,
                      brain_ticks, mode, domain_count) -> bytes:
    """STATE (0x81) payload = 20 bytes. Matches ck_uart_send_state()."""
    payload = struct.pack('<BBBBB I HH I BBB',
                          phase_b, phase_d, phase_bc, fuse_op,
                          1 if bump else 0,
                          tick_count, coh_num, coh_den,
                          brain_ticks, mode, domain_count, 0)
    return make_packet(PKT_STATE, payload)


def make_crystal_packet(ops, length, fuse, confidence, seen) -> bytes:
    """CRYSTAL (0x83) payload. Matches ck_uart_send_crystal()."""
    payload = bytes([length]) + bytes(ops[:length])
    payload += bytes([fuse])
    payload += struct.pack('<fI', confidence, seen)
    return make_packet(PKT_CRYSTAL, payload)


# ── Payload parsers ─────────────────────────────────────────────────────────

def parse_state_payload(payload: bytes) -> dict:
    """
    Parse STATE (0x81) payload -> dict.
    Returns coherence as float [0.0..1.0].
    """
    if len(payload) < 20:
        return {}
    b, d, bc, fuse_op, bump = struct.unpack_from('<BBBBB', payload, 0)
    tick_count,              = struct.unpack_from('<I',    payload, 5)
    coh_num, coh_den         = struct.unpack_from('<HH',   payload, 9)
    brain_ticks,             = struct.unpack_from('<I',    payload, 13)
    mode, domain_count, _    = struct.unpack_from('<BBB',  payload, 17)
    return {
        'phase_b':     b,
        'phase_d':     d,
        'phase_bc':    bc,
        'fuse':        fuse_op,
        'bump':        bool(bump),
        'tick_count':  tick_count,
        'coherence':   coh_num / max(coh_den, 1),
        'coh_num':     coh_num,
        'coh_den':     coh_den,
        'brain_ticks': brain_ticks,
        'mode':        mode,
        'domains':     domain_count,
    }


def parse_crystal_payload(payload: bytes) -> dict:
    """Parse CRYSTAL (0x83) payload -> dict."""
    if len(payload) < 3:
        return {}
    pattern_len = payload[0]
    pattern     = list(payload[1:1 + pattern_len])
    offset      = 1 + pattern_len
    fuse_op     = payload[offset]
    confidence  = struct.unpack_from('<f', payload, offset + 1)[0]
    seen        = struct.unpack_from('<I', payload, offset + 5)[0]
    return {
        'pattern': pattern, 'fuse': fuse_op,
        'confidence': confidence, 'seen': seen,
    }


def parse_servo_pos_payload(payload: bytes) -> dict:
    """
    Parse SERVO_POS (0xA1) payload = 16 bytes:
      8 servos × 2 bytes each (u16 LE, microseconds)
    """
    if len(payload) < 16:
        return {}
    positions = list(struct.unpack_from('<8H', payload, 0))
    return {'positions': positions}   # IDs 1-8


def parse_proximity_payload(payload: bytes) -> dict:
    """
    Parse PROXIMITY (0xA2) payload = 12 bytes:
      accel_x, accel_y, accel_z : i16 LE (mm/s² × 100)
      gyro_x, gyro_y, gyro_z    : i16 LE (mrad/s × 100)
    """
    if len(payload) < 12:
        return {}
    ax, ay, az, gx, gy, gz = struct.unpack_from('<6h', payload, 0)
    return {
        'accel': [ax / 100.0, ay / 100.0, az / 100.0],
        'gyro':  [gx / 100.0, gy / 100.0, gz / 100.0],
    }


# ── Packet parser state machine ─────────────────────────────────────────────

class PacketParser:
    """
    Byte-by-byte state machine matching ck_uart_poll() exactly.
    Feed bytes with feed_byte() or feed_bytes().
    """

    def __init__(self):
        self.state       = 0   # 0=sync0 1=sync1 2=type 3=len0 4=len1 5=payload 6=crc
        self.buf         = bytearray()
        self.pkt_type    = 0
        self.pkt_len     = 0
        self.payload_pos = 0
        self.rx_count    = 0
        self.crc_errors  = 0

    def feed_byte(self, byte: int):
        """Feed one byte. Returns (type, payload_bytes) on complete valid packet, else None."""
        if self.state == 0:
            if byte == SYNC_0:
                self.buf = bytearray([byte])
                self.state = 1
        elif self.state == 1:
            if byte == SYNC_1:
                self.buf.append(byte)
                self.state = 2
            else:
                self.state = 0
        elif self.state == 2:
            self.pkt_type = byte
            self.buf.append(byte)
            self.state = 3
        elif self.state == 3:
            self.pkt_len = byte
            self.buf.append(byte)
            self.state = 4
        elif self.state == 4:
            self.pkt_len |= (byte << 8)
            self.buf.append(byte)
            self.payload_pos = 0
            if self.pkt_len > MAX_PAYLOAD:
                self.state = 0
            elif self.pkt_len == 0:
                self.state = 6
            else:
                self.state = 5
        elif self.state == 5:
            self.buf.append(byte)
            self.payload_pos += 1
            if self.payload_pos >= self.pkt_len:
                self.state = 6
        elif self.state == 6:
            computed = crc8(bytes(self.buf))
            self.state = 0
            if byte == computed:
                payload = bytes(self.buf[HEADER_SIZE:])
                self.rx_count += 1
                return (self.pkt_type, payload)
            else:
                self.crc_errors += 1
        return None

    def feed_bytes(self, data: bytes):
        """Feed multiple bytes. Yields (type, payload) for each complete packet."""
        for byte in data:
            result = self.feed_byte(byte)
            if result is not None:
                yield result

    @property
    def stats(self) -> dict:
        return {'rx': self.rx_count, 'crc_errors': self.crc_errors}
