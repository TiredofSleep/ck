"""
ck_sim_uart.py -- Port of ck_uart.c + ck_serial.py
====================================================
Operator: BALANCE (5) -- the bridge between bodies.

Packet encode/decode matching both the ARM C code and
the Python serial bridge. Loopback testing validates
protocol correctness.

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import struct

# Packet types (matching ck_uart.h)
PKT_OBSERVE   = 0x01
PKT_SWARM     = 0x02
PKT_DEEP_OBS  = 0x03
PKT_CONFIG    = 0x04
PKT_TL_CHUNK  = 0x05
PKT_PING      = 0x06
PKT_STATE     = 0x81
PKT_DECISION  = 0x82
PKT_CRYSTAL   = 0x83
PKT_DOMAIN    = 0x84
PKT_TL_REQ    = 0x85
PKT_PONG      = 0x86

# Dog-specific
PKT_MOTOR     = 0x20
PKT_LED_CMD   = 0x21
PKT_SERVO     = 0x22
PKT_GAIT      = 0x23
PKT_ESTOP     = 0x2E
PKT_SENSOR    = 0xA0
PKT_SERVO_POS = 0xA1
PKT_PROXIMITY = 0xA2

SYNC_0 = 0x43  # 'C'
SYNC_1 = 0x4B  # 'K'
HEADER_SIZE = 5
MAX_PAYLOAD = 256


def crc8(data: bytes) -> int:
    """CRC-8/MAXIM."""
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
    """Build a CK serial packet. Matches both ck_uart_send() and ck_serial.py."""
    header = struct.pack('<2sBH', b'CK', pkt_type, len(payload))
    packet = header + payload
    return packet + bytes([crc8(packet)])


def make_state_packet(phase_b, phase_d, phase_bc, fuse_op, bump,
                      tick_count, coh_num, coh_den,
                      brain_ticks, mode, domain_count) -> bytes:
    """Build STATE packet. Matches ck_uart_send_state()."""
    payload = struct.pack('<BBBBB I HH I BBB',
                          phase_b, phase_d, phase_bc, fuse_op, 1 if bump else 0,
                          tick_count, coh_num, coh_den,
                          brain_ticks, mode, domain_count, 0)
    return make_packet(PKT_STATE, payload)


def make_crystal_packet(ops, length, fuse, confidence, seen) -> bytes:
    """Build CRYSTAL packet. Matches ck_uart_send_crystal()."""
    payload = bytes([length]) + bytes(ops[:length])
    payload += bytes([fuse])
    payload += struct.pack('<fI', confidence, seen)
    return make_packet(PKT_CRYSTAL, payload)


class PacketParser:
    """State machine packet parser. Matches ck_uart_poll() byte-by-byte."""

    def __init__(self):
        self.state = 0  # 0=sync0, 1=sync1, 2=type, 3=len0, 4=len1, 5=payload, 6=crc
        self.buf = bytearray()
        self.pkt_type = 0
        self.pkt_len = 0
        self.payload_pos = 0
        self.rx_count = 0
        self.crc_errors = 0

    def feed_byte(self, byte: int):
        """Feed one byte. Returns (type, payload) when a complete packet is parsed,
        or None if more data needed."""
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
            # CRC check
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


def parse_state_payload(payload: bytes) -> dict:
    """Parse STATE packet payload. Matches ck_serial.py unpack_state()."""
    if len(payload) < 20:
        return {}
    b, d, bc, fuse_op, bump = struct.unpack_from('<BBBBB', payload, 0)
    tick_count, = struct.unpack_from('<I', payload, 5)
    coh_num, coh_den = struct.unpack_from('<HH', payload, 9)
    brain_ticks, = struct.unpack_from('<I', payload, 13)
    mode, domain_count, _ = struct.unpack_from('<BBB', payload, 17)
    return {
        'phase_b': b, 'phase_d': d, 'phase_bc': bc,
        'fuse': fuse_op, 'bump': bool(bump),
        'tick_count': tick_count,
        'coherence': coh_num / max(coh_den, 1),
        'brain_ticks': brain_ticks,
        'mode': mode, 'domains': domain_count,
    }


def parse_crystal_payload(payload: bytes) -> dict:
    """Parse CRYSTAL packet payload. Matches ck_serial.py unpack_crystal()."""
    if len(payload) < 3:
        return {}
    pattern_len = payload[0]
    pattern = list(payload[1:1+pattern_len])
    offset = 1 + pattern_len
    fuse_op = payload[offset]
    confidence = struct.unpack_from('<f', payload, offset+1)[0]
    seen = struct.unpack_from('<I', payload, offset+5)[0]
    return {
        'pattern': pattern, 'fuse': fuse_op,
        'confidence': confidence, 'seen': seen,
    }
