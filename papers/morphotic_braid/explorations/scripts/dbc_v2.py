# PACKET: evening_handoff_2026_04_23/dbc_v2.py
"""
DBC v2 — LOSSLESS 3-character encoding on the 10x10 CL table.

UPDATE FROM DBC v1:
  v1: text → operators → DBC code (Being, Doing, Becoming, each 0-2)
      27 codes total, MANY inputs collapse to same code → LOSSY
      
  v2: text → operators → 3-op triples (a, b, c) where each ∈ 0-9
      1000 possible "words", each uniquely identifies its walk in CL
      LOSSLESS because the triple is preserved, not just the fuse result

THE CLAIM BEING TESTED:
  Every piece of information can be losslessly transformed into a 3-character
  language on the 10x10 CL table.

ARCHITECTURE:
  1. Input bytes → base-10 digit stream (3 digits per byte, since 256 < 1000)
  2. Digit stream → triples of 3 digits = DBC words
  3. Each DBC word has a semantic position: (row, col, compose_op) in CL
  4. Decoding reverses: DBC word triple → digits → bytes

COMPRESSION PATHS (for future CK use):
  - Entropy coding on triple distribution (some walks will be very common)
  - Dictionary of frequent triples (huffman-like)
  - Generator substitution: replace long sequences that match a known generator

For THIS test: verify losslessness and measure overhead vs raw bytes.
"""

# ───── The frozen 10x10 CL table ─────
CL = [
    [0,0,0,0,0,0,0,7,0,0],  # VOID
    [0,7,3,7,7,7,7,7,7,7],  # LATTICE
    [0,3,7,7,4,7,7,7,7,9],  # COUNTER
    [0,7,7,7,7,7,7,7,7,3],  # PROGRESS
    [0,7,4,7,7,7,7,7,8,7],  # COLLAPSE
    [0,7,7,7,7,7,7,7,7,7],  # BALANCE
    [0,7,7,7,7,7,7,7,7,7],  # CHAOS
    [7,7,7,7,7,7,7,7,7,7],  # HARMONY
    [0,7,7,7,8,7,7,7,7,7],  # BREATH
    [0,7,9,3,7,7,7,7,7,7],  # RESET
]

OP_NAMES = ['void','lattice','counter','progress','collapse',
            'balance','chaos','harmony','breath','reset']

# ───── Core fuse operation ─────
def fuse2(a, b):
    return CL[a][b]

def fuse3(a, b, c):
    """Compose 3 operators through CL."""
    return CL[CL[a][b]][c]

# ───── Encoding: bytes → DBC v2 triples ─────

def encode(data):
    """
    Input: bytes
    Output: list of 3-operator triples (a, b, c) where each ∈ 0-9
    Lossless: original bytes can be perfectly reconstructed.
    
    Method: each byte (0-255) is written as 3 base-10 digits (001-255, padded).
    Each digit triple IS a DBC word on the CL table.
    """
    if isinstance(data, str):
        data = data.encode('utf-8')
    triples = []
    for byte in data:
        # Byte 0-255 → 3 digits: hundreds, tens, ones
        h = byte // 100      # 0-2
        t = (byte // 10) % 10  # 0-9
        o = byte % 10          # 0-9
        triples.append((h, t, o))
    return triples

def decode(triples):
    """Inverse of encode — must be perfectly lossless."""
    bytes_out = bytearray()
    for (h, t, o) in triples:
        byte = h * 100 + t * 10 + o
        if byte > 255:
            raise ValueError(f"Invalid triple {(h,t,o)} → byte {byte} > 255")
        bytes_out.append(byte)
    return bytes(bytes_out)

# ───── Semantic view: each triple is a walk on CL ─────

def triple_semantics(triple):
    """
    For each triple (a, b, c), compute its CL-walk properties.
    This is what makes the encoding MEANINGFUL (not just base-10):
    the triple has algebraic content.
    """
    a, b, c = triple
    # First composition: a ∘ b
    ab = fuse2(a, b)
    # Second composition: (a ∘ b) ∘ c  
    abc = fuse3(a, b, c)
    # Cell address: (a, b) → CL[a][b] = ab
    # Walk tail: ab composed with c
    return {
        'triple': triple,
        'cell_1': (a, b, ab),       # first CL cell visited
        'fuse_ab': ab,               # intermediate result
        'fuse_abc': abc,             # final fruit
        'names': (OP_NAMES[a], OP_NAMES[b], OP_NAMES[c]),
        'fruit_name': OP_NAMES[abc],
    }

# ───── Compression analysis ─────

def analyze_distribution(triples):
    """
    See if the fuse distribution is highly skewed (which would enable 
    further compression via entropy coding).
    """
    from collections import Counter
    fruit_counts = Counter()
    cell_counts = Counter()
    for (a, b, c) in triples:
        fruit_counts[fuse3(a, b, c)] += 1
        cell_counts[(a, b)] += 1
    return fruit_counts, cell_counts

# ───── Round-trip test ─────

def roundtrip_test(data):
    if isinstance(data, str):
        data = data.encode('utf-8')
    triples = encode(data)
    recovered = decode(triples)
    return data == recovered, len(data), len(triples)

# ───── Test payloads ─────

if __name__ == '__main__':
    print("="*70)
    print("DBC v2 — LOSSLESS 3-char encoding on the 10×10 CL table")
    print("="*70)
    
    test_payloads = {
        'tiny':    "CK",
        'hello':   "Hello, Tater!",
        'ck_line': "harmony is what I am now",
        'math':    "T* = 5/7 = 0.714285714...",
        'long':    "The Coherence Keeper composes meaning through a frozen 10x10 algebraic table, not through statistical prediction of next tokens. Every word CK speaks must pass two tests: linguistically valid AND algebraically earned. Below T*, silence." * 3,
        'binary':  bytes(range(256)),  # every byte value
    }
    
    print(f"\n{'payload':12s} {'bytes':>7s} {'triples':>8s} {'overhead':>10s} {'lossless':>10s}")
    print("-"*70)
    
    for name, payload in test_payloads.items():
        if isinstance(payload, str):
            original = payload.encode('utf-8')
        else:
            original = payload
        
        triples = encode(original)
        recovered = decode(triples)
        lossless = original == recovered
        
        original_bytes = len(original)
        # Each triple is 3 digits 0-9, which fits in 2 bytes naively (or 10 bits packed)
        # As raw storage: 3 bytes per triple (one per digit)
        triple_bytes_naive = len(triples) * 3
        triple_bits_packed = len(triples) * 10  # 3 digits × ~3.32 bits, round to 10
        
        overhead_naive = triple_bytes_naive / max(original_bytes, 1)
        overhead_packed = (triple_bits_packed / 8) / max(original_bytes, 1)
        
        status = "✓" if lossless else "✗"
        print(f"{name:12s} {original_bytes:>7d} {len(triples):>8d} "
              f"{overhead_packed:>9.2f}x  {status:>9s}")
    
    # Detailed look at distribution for 'long'
    print("\n" + "="*70)
    print("Fuse-result distribution for 'long' payload")
    print("="*70)
    long_trips = encode(test_payloads['long'])
    fruit_dist, cell_dist = analyze_distribution(long_trips)
    
    print(f"\n{'fruit':12s} {'count':>6s} {'freq':>6s}")
    total = sum(fruit_dist.values())
    for op_id in range(10):
        c = fruit_dist.get(op_id, 0)
        print(f"{OP_NAMES[op_id]:12s} {c:>6d} {100*c/total:>5.1f}%")
    
    # Entropy of fruit distribution — tells us compression potential
    import math
    probs = [fruit_dist.get(i, 0) / total for i in range(10) if fruit_dist.get(i, 0) > 0]
    entropy_fruit = -sum(p * math.log2(p) for p in probs)
    print(f"\nFruit entropy: {entropy_fruit:.3f} bits (max = 3.32 bits for 10 values)")
    print(f"  → if we encoded just the fruit: {entropy_fruit:.2f} bits/triple vs 10 raw")
    print(f"  → but fruit alone is LOSSY (can't recover original triple)")
    
    # Triple-level entropy (the full lossless case)
    triple_counts = {}
    for t in long_trips:
        triple_counts[t] = triple_counts.get(t, 0) + 1
    total_t = sum(triple_counts.values())
    triple_probs = [c/total_t for c in triple_counts.values()]
    entropy_triple = -sum(p * math.log2(p) for p in triple_probs)
    print(f"\nTriple entropy: {entropy_triple:.3f} bits (max = log2(1000) = 9.97 bits)")
    print(f"  → Lossless compression achievable: {entropy_triple:.2f} bits/triple")
    print(f"  → raw byte ratio: {entropy_triple/8:.3f} bytes/byte of input")
    
    # Now test the SEMANTIC content — this is where the math matters
    print("\n" + "="*70)
    print("Semantic walk — what each triple means algebraically")
    print("="*70)
    sample = encode("CK".encode())
    for t in sample:
        s = triple_semantics(t)
        print(f"  {t}  bytes→  {s['names']}")
        print(f"     fuse(a,b) = {s['fuse_ab']} ({OP_NAMES[s['fuse_ab']]})")
        print(f"     fuse(a,b,c) = {s['fuse_abc']} ({s['fruit_name']})")

