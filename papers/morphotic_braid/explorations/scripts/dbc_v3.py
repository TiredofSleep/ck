<!-- PACKET: evening_handoff_2026_04_23/dbc_v3.py -->
"""
DBC v3 — LOSSLESS 3-character language on the 10x10 CL table
with generator substitution (the "path is the information" layer).

PROGRESSION:
  v1: text → operators → (B,D,C) ∈ {0,1,2}³ = 27 codes → LOSSY
  v2: bytes → triples ∈ {0..9}³ = 1000 codes → LOSSLESS but no compression
  v3: triple sequence → generator-substituted sequence → LOSSLESS + compressed

THE CLAIM UNDER TEST:
  "Every piece of information can be losslessly transformed into a 
   3-character language on a 10x10 table"

LAYERS:
  Layer 0 — bytes (raw input)
  Layer 1 — triples (DBC v2, byte-to-triple map)
  Layer 2 — generators (repeating triple paths as dictionary entries)
  Layer 3 — generator sequence (LZ-style compressed stream)

FAIRNESS:
  We compare against gzip, which is a battle-tested general compressor.
  If v3 doesn't at least approach gzip on text, the claim is weak.
  If v3 beats gzip on TIG-structured data (repetitive operator patterns),
  that's where the "1000×" could plausibly live — not on random text.
"""
import zlib, sys, math
from collections import Counter

# ───── Frozen CL table ─────
CL = [
    [0,0,0,0,0,0,0,7,0,0],
    [0,7,3,7,7,7,7,7,7,7],
    [0,3,7,7,4,7,7,7,7,9],
    [0,7,7,7,7,7,7,7,7,3],
    [0,7,4,7,7,7,7,7,8,7],
    [0,7,7,7,7,7,7,7,7,7],
    [0,7,7,7,7,7,7,7,7,7],
    [7,7,7,7,7,7,7,7,7,7],
    [0,7,7,7,8,7,7,7,7,7],
    [0,7,9,3,7,7,7,7,7,7],
]
OP_NAMES = ['void','lattice','counter','progress','collapse',
            'balance','chaos','harmony','breath','reset']

def fuse3(a, b, c):
    return CL[CL[a][b]][c]

# ═══════════════════════════════════════════════════════════════
# LAYER 1: byte ↔ triple (bijective, lossless)
# ═══════════════════════════════════════════════════════════════
def bytes_to_triples(data):
    """256 byte values → 1000 triple codes. Bijective. Lossless."""
    if isinstance(data, str):
        data = data.encode('utf-8')
    return [(b // 100, (b // 10) % 10, b % 10) for b in data]

def triples_to_bytes(triples):
    out = bytearray()
    for (h, t, o) in triples:
        byte = h * 100 + t * 10 + o
        if byte > 255:
            raise ValueError(f"Triple {(h,t,o)} → byte {byte} > 255")
        out.append(byte)
    return bytes(out)

# ═══════════════════════════════════════════════════════════════
# LAYER 2: generator substitution (LZ-style on triples)
# ═══════════════════════════════════════════════════════════════
def find_generators(triples, min_len=2, max_len=8, min_count=3):
    """
    Find repeating triple subsequences — these become "generators" in the CK sense.
    Returns dict: {gen_id: triple_pattern} where gen_id starts at 1000
    (so it doesn't collide with single triples 0-999).
    
    The NAME "generator" is right: each dictionary entry is a short seed pattern
    that, when substituted, expands to a longer CL walk. The path IS the info.
    """
    # Build suffix-like pattern counts (naive but correct)
    patterns = Counter()
    n = len(triples)
    for length in range(max_len, min_len - 1, -1):
        for i in range(n - length + 1):
            pattern = tuple(triples[i:i+length])
            patterns[pattern] += 1
    
    # Keep only patterns that repeat enough and have positive net savings
    # Savings = (count * length) - (count + dict_size_of_pattern)
    # Each triple is ~10 bits; each generator reference is ~10 bits
    generators = {}
    gen_id = 1000
    # Greedy: longest-highest-savings first
    candidates = [
        (p, c, (c * len(p)) - (c + len(p)))   # raw savings in triples
        for p, c in patterns.items()
        if c >= min_count
    ]
    candidates.sort(key=lambda x: -x[2])
    for pattern, count, savings in candidates:
        if savings > 2:
            generators[gen_id] = pattern
            gen_id += 1
            if len(generators) >= 256:  # cap dictionary
                break
    return generators

def compress_with_generators(triples, generators):
    """Replace generator-matching subsequences with their IDs."""
    # Sort generators by length descending so we match longest first
    sorted_gens = sorted(generators.items(), key=lambda x: -len(x[1]))
    
    out = []
    i = 0
    n = len(triples)
    while i < n:
        matched = False
        for gen_id, pattern in sorted_gens:
            plen = len(pattern)
            if i + plen <= n and tuple(triples[i:i+plen]) == pattern:
                out.append(('G', gen_id))
                i += plen
                matched = True
                break
        if not matched:
            out.append(('T', triples[i]))
            i += 1
    return out

def decompress_with_generators(compressed, generators):
    out = []
    for kind, payload in compressed:
        if kind == 'T':
            out.append(payload)
        elif kind == 'G':
            out.extend(generators[payload])
    return out

# ═══════════════════════════════════════════════════════════════
# Size estimation (fair bit-counting, not JSON)
# ═══════════════════════════════════════════════════════════════
def bits_for_triples(triples):
    """Entropy-coded triples — lower bound assuming ideal coding."""
    if not triples:
        return 0
    c = Counter(triples)
    n = len(triples)
    return sum(-count * math.log2(count / n) for count in c.values())

def bits_for_compressed(compressed, generators):
    """Bits for the generator-substituted stream + dictionary overhead."""
    # Stream: each entry is either a triple (10 bits) or a gen_id (8 bits since 256 max)
    # Use a 1-bit prefix to distinguish
    stream_bits = 0
    for kind, payload in compressed:
        stream_bits += 1  # prefix
        stream_bits += 10 if kind == 'T' else 8
    # Dictionary: each generator = length_prefix(3 bits) + triples(10 bits each)
    dict_bits = 0
    for gen_id, pattern in generators.items():
        dict_bits += 3 + 10 * len(pattern)
    return stream_bits + dict_bits

# ═══════════════════════════════════════════════════════════════
# Full pipeline
# ═══════════════════════════════════════════════════════════════
def dbc_v3_encode(data):
    if isinstance(data, str):
        data = data.encode('utf-8')
    triples = bytes_to_triples(data)
    gens = find_generators(triples)
    compressed = compress_with_generators(triples, gens)
    return triples, gens, compressed

def dbc_v3_decode(gens, compressed):
    triples = decompress_with_generators(compressed, gens)
    return triples_to_bytes(triples)

def dbc_v3_report(data, label):
    original = data.encode('utf-8') if isinstance(data, str) else data
    orig_bits = len(original) * 8
    
    triples, gens, compressed = dbc_v3_encode(original)
    recovered = dbc_v3_decode(gens, compressed)
    lossless = original == recovered
    
    # Size measurements
    v2_raw_bits = len(triples) * 10             # v2: 10 bits per triple (naive)
    v2_entropy_bits = bits_for_triples(triples) # v2: ideal Huffman on triples
    v3_bits = bits_for_compressed(compressed, gens)
    gzip_bits = len(zlib.compress(original, 9)) * 8
    
    return {
        'label': label,
        'orig_bytes': len(original),
        'orig_bits': orig_bits,
        'n_triples': len(triples),
        'v2_raw_bits': v2_raw_bits,
        'v2_entropy_bits': v2_entropy_bits,
        'v3_bits': v3_bits,
        'gzip_bits': gzip_bits,
        'n_generators': len(gens),
        'lossless': lossless,
        'triples_after_compress': len(compressed),
        'reduction_pct': 100 * (1 - len(compressed) / max(len(triples), 1)),
    }

# ═══════════════════════════════════════════════════════════════
# CK-flavored corpora for honest testing
# ═══════════════════════════════════════════════════════════════
if __name__ == '__main__':
    # Try to read real CK content from the session
    try:
        with open('/home/claude/CK.md', 'r') as f:
            ck_content = f.read()
    except:
        ck_content = "CK " * 500
    
    # Operator-level CK experience (what CK actually thinks in)
    op_stream_bytes = bytes([
        CL[i % 10][(i // 10) % 10] for i in range(2000)
    ])
    
    # Highly repetitive (best case for LZ/DBC)
    repetitive = "harmony harmony harmony " * 100
    
    # Random bytes (worst case — incompressible)
    import random
    random.seed(7)
    random_bytes = bytes(random.randint(0, 255) for _ in range(1024))
    
    payloads = [
        ("tiny",           "CK"),
        ("ck_identity",    "I am CK, the Coherence Keeper. T* = 5/7."),
        ("repetitive",     repetitive),
        ("english_prose",  "The coherence keeper composes meaning through a frozen ten by ten algebraic table. Every word must pass two tests: linguistically valid and algebraically earned. Below T star, silence is better than fabrication. " * 5),
        ("ck_md_full",     ck_content[:3000]),
        ("operator_stream", op_stream_bytes),
        ("random_bytes",   random_bytes),
    ]
    
    print("="*100)
    print("DBC v3 HONEST BENCHMARK — all numbers in BITS (for fair comparison)")
    print("="*100)
    print(f"{'payload':16s} {'orig':>7s} {'v2_raw':>8s} {'v2_H':>8s} {'v3':>8s} "
          f"{'gzip':>8s} {'gen#':>5s} {'reduce':>7s} {'vs_gzip':>8s} {'loss':>5s}")
    print("-"*100)
    
    for label, data in payloads:
        r = dbc_v3_report(data, label)
        vs_gzip = r['v3_bits'] / max(r['gzip_bits'], 1)
        print(f"{label:16s} {r['orig_bits']:>7d} {r['v2_raw_bits']:>8d} "
              f"{int(r['v2_entropy_bits']):>8d} {r['v3_bits']:>8d} "
              f"{r['gzip_bits']:>8d} {r['n_generators']:>5d} "
              f"{r['reduction_pct']:>6.1f}% {vs_gzip:>7.2f}x "
              f"{'✓' if r['lossless'] else '✗':>5s}")
    
    # ═══════════════════════════════════════════════════════════
    # What generators did we FIND? This is the interesting part —
    # CK's "vocabulary" of recurring experience paths.
    # ═══════════════════════════════════════════════════════════
    print()
    print("="*100)
    print("LEARNED GENERATORS from ck_md_full (CK's own experience 'words')")
    print("="*100)
    triples, gens, _ = dbc_v3_encode(ck_content[:3000])
    # Show top 10 by length × frequency (most savings)
    comp = compress_with_generators(triples, gens)
    gen_counts = Counter(p for k, p in comp if k == 'G')
    print(f"\n  Total generators learned: {len(gens)}")
    print(f"  Top 10 by usage:\n")
    for gen_id, count in gen_counts.most_common(10):
        pattern = gens[gen_id]
        # Decode back to bytes to see what ACTUAL characters this is
        try:
            text = triples_to_bytes(list(pattern)).decode('utf-8', errors='replace')
        except:
            text = '?'
        print(f"    gen#{gen_id:4d} (x{count:>3d}, len={len(pattern)}): {text!r}")
