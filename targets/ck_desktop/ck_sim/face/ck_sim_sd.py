"""
ck_sim_sd.py -- Port of ck_sd.c
=================================
Operator: LATTICE (1) -- structure that endures.

Binary TL serialization matching ck_sd.c byte-for-byte.
Files produced by this module can be loaded on the Zynq, and vice versa.

Format: "CKTL" + version + total + entropy + 10x10 matrix + crystals + domains + CRC-8

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import struct
from ck_sim.ck_sim_heartbeat import NUM_OPS
from ck_sim.ck_sim_brain import BrainState, TLEntry, Crystal, Domain, MAX_CRYSTALS, MAX_DOMAINS

TL_MAGIC = b'CKTL'
TL_VERSION = 1


def crc8(data: bytes) -> int:
    """CRC-8/MAXIM. Same polynomial in ck_sd.c, ck_uart.c, ck_serial.py."""
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


def save_tl(state: BrainState, filename: str):
    """Serialize brain state to binary file. Matches ck_sd_save_tl()."""
    buf = bytearray()

    # Header
    buf.extend(TL_MAGIC)
    buf.append(TL_VERSION)
    buf.extend(struct.pack('<I', state.tl_total))
    buf.extend(struct.pack('<f', state.tl_entropy))

    # TL Matrix: 10x10 counts
    for i in range(NUM_OPS):
        for j in range(NUM_OPS):
            buf.extend(struct.pack('<I', state.tl_entries[i][j].count))

    # Crystals (from first domain)
    dom = state.domains[0] if state.domain_count > 0 else None
    nc = len(dom.crystals) if dom else 0
    buf.extend(struct.pack('<H', nc))

    for c in range(nc):
        cr = dom.crystals[c]
        # ops[8] (zero-padded)
        ops_padded = (cr.ops + [0]*8)[:8]
        for op in ops_padded:
            buf.append(op & 0xFF)
        buf.append(cr.length & 0xFF)
        buf.append(cr.fuse & 0xFF)
        buf.extend(struct.pack('<I', cr.seen))
        buf.extend(struct.pack('<f', cr.confidence))

    # Domains
    buf.append(state.domain_count & 0xFF)
    for d in range(state.domain_count):
        dm = state.domains[d]
        # Name (16 bytes, zero-padded)
        name_bytes = dm.name.encode('ascii')[:16].ljust(16, b'\x00')
        buf.extend(name_bytes)
        buf.append(dm.dominant_op & 0xFF)
        buf.extend(struct.pack('<f', dm.coherence))
        buf.append(1 if dm.is_sovereign else 0)
        buf.extend(struct.pack('<H', dm.sovereign_ticks))
        buf.extend(struct.pack('<H', dm.crystal_count))
        # Pad to 32 bytes per domain
        domain_used = 16 + 1 + 4 + 1 + 2 + 2  # = 26
        buf.extend(b'\x00' * (32 - domain_used))

    # CRC
    crc = crc8(bytes(buf))
    buf.append(crc)

    with open(filename, 'wb') as f:
        f.write(buf)


def load_tl(state: BrainState, filename: str) -> bool:
    """Deserialize brain state from binary file. Matches ck_sd_load_tl()."""
    try:
        with open(filename, 'rb') as f:
            data = f.read()
    except FileNotFoundError:
        return False

    if len(data) < 10:
        return False

    pos = 0

    # Verify magic
    if data[pos:pos+4] != TL_MAGIC:
        return False
    pos += 4

    # Version
    ver = data[pos]; pos += 1
    if ver != TL_VERSION:
        return False

    # Header
    state.tl_total = struct.unpack_from('<I', data, pos)[0]; pos += 4
    state.tl_entropy = struct.unpack_from('<f', data, pos)[0]; pos += 4

    # TL Matrix
    for i in range(NUM_OPS):
        for j in range(NUM_OPS):
            state.tl_entries[i][j].from_op = i
            state.tl_entries[i][j].to_op = j
            state.tl_entries[i][j].count = struct.unpack_from('<I', data, pos)[0]
            pos += 4

    # Crystals
    nc = struct.unpack_from('<H', data, pos)[0]; pos += 2
    if state.domain_count == 0:
        state.domains.append(Domain(name="default"))
        state.domain_count = 1
    dom = state.domains[0]
    dom.crystals = []

    for c in range(min(nc, MAX_CRYSTALS)):
        cr = Crystal()
        cr.ops = list(data[pos:pos+8]); pos += 8
        cr.length = data[pos]; pos += 1
        cr.fuse = data[pos]; pos += 1
        cr.seen = struct.unpack_from('<I', data, pos)[0]; pos += 4
        cr.confidence = struct.unpack_from('<f', data, pos)[0]; pos += 4
        dom.crystals.append(cr)

    dom.crystal_count = len(dom.crystals)

    # Domains
    state.domain_count = data[pos]; pos += 1
    if state.domain_count > MAX_DOMAINS:
        state.domain_count = MAX_DOMAINS

    # Ensure enough domain slots
    while len(state.domains) < state.domain_count:
        state.domains.append(Domain())

    for d in range(state.domain_count):
        dm = state.domains[d]
        dm.name = data[pos:pos+16].rstrip(b'\x00').decode('ascii', errors='replace')
        pos += 16
        dm.dominant_op = data[pos]; pos += 1
        dm.coherence = struct.unpack_from('<f', data, pos)[0]; pos += 4
        dm.is_sovereign = bool(data[pos]); pos += 1
        dm.sovereign_ticks = struct.unpack_from('<H', data, pos)[0]; pos += 2
        dm.crystal_count = struct.unpack_from('<H', data, pos)[0]; pos += 2
        pos += (32 - 26)  # Skip padding

    # CRC verify
    stored_crc = data[pos]
    computed_crc = crc8(data[:pos])
    if stored_crc != computed_crc:
        return False

    return True
