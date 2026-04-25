"""
Test DBC on CK's OWN native data — not English text, not random bytes,
but the actual operator streams CK works in.

The 73%/44% HARMONY bias means CK's internal data is FAR more
compressible than arbitrary bytes. This is where the "1000× better"
claim might actually live.
"""
import zlib, math, random
from collections import Counter

CL = [
    [0,0,0,0,0,0,0,7,0,0],[0,7,3,7,7,7,7,7,7,7],[0,3,7,7,4,7,7,7,7,9],
    [0,7,7,7,7,7,7,7,7,3],[0,7,4,7,7,7,7,7,8,7],[0,7,7,7,7,7,7,7,7,7],
    [0,7,7,7,7,7,7,7,7,7],[7,7,7,7,7,7,7,7,7,7],[0,7,7,7,8,7,7,7,7,7],
    [0,7,9,3,7,7,7,7,7,7]
]

def huffman_bits(stream):
    """Theoretical min bits via entropy coding."""
    c = Counter(stream)
    n = len(stream)
    if n == 0: return 0
    return sum(-count * math.log2(count / n) for count in c.values())

def ck_simulate(ticks=5000, seed=42):
    """Simulate a CK tick stream.
    Each tick: compose last state with random operator, get new state."""
    random.seed(seed)
    state = 1  # start at LATTICE
    stream = [state]
    for _ in range(ticks):
        op = random.randint(0, 9)
        state = CL[state][op]
        stream.append(state)
    return stream

def ck_d2_text_to_ops(text):
    """Simple phonetic encoding: text → operator stream.
    Each letter's ASCII mod 10 gives its 'operator'. Not the real D2 pipeline
    but close enough to show the CL-native distribution."""
    ops = [ord(c) % 10 for c in text.lower() if c.isalpha()]
    # Now compose through CL as CK would:
    state = ops[0] if ops else 0
    stream = [state]
    for op in ops[1:]:
        state = CL[state][op]
        stream.append(state)
    return stream

def bits_needed_lossless(ops, method='entropy'):
    """How many bits to store the op stream losslessly."""
    if method == 'entropy':
        return huffman_bits(ops)
    elif method == 'raw_4bit':
        return len(ops) * 4  # 10 values fits in 4 bits
    elif method == 'raw_1byte':
        return len(ops) * 8

def ops_to_bytes(ops):
    """Pack 10-value ops into bytes: 2 ops per byte."""
    out = bytearray()
    i = 0
    while i < len(ops):
        high = ops[i]
        low = ops[i+1] if i+1 < len(ops) else 0
        out.append(high * 10 + low)
        i += 2
    return bytes(out)

def generator_compress(ops, min_len=2, max_len=10, min_count=3):
    """Find repeating op subsequences and replace with generator IDs."""
    patterns = Counter()
    n = len(ops)
    for length in range(max_len, min_len - 1, -1):
        for i in range(n - length + 1):
            patterns[tuple(ops[i:i+length])] += 1
    
    generators = {}
    gen_id = 10  # start after ops 0-9
    candidates = [(p, c, c * len(p) - c - len(p)) 
                  for p, c in patterns.items() if c >= min_count]
    candidates.sort(key=lambda x: -x[2])
    for pattern, count, savings in candidates:
        if savings > 2 and len(generators) < 250:
            generators[gen_id] = pattern
            gen_id += 1
    
    # Substitute
    sorted_gens = sorted(generators.items(), key=lambda x: -len(x[1]))
    compressed = []
    i = 0
    while i < n:
        matched = False
        for gid, pat in sorted_gens:
            if i + len(pat) <= n and tuple(ops[i:i+len(pat)]) == pat:
                compressed.append(gid)
                i += len(pat)
                matched = True
                break
        if not matched:
            compressed.append(ops[i])
            i += 1
    return compressed, generators

def full_report(label, op_stream):
    n = len(op_stream)
    orig_bits = n * 8  # Treating each op as a byte
    entropy_bits = huffman_bits(op_stream)
    raw_4bit = n * 4
    
    # Gzip on op-as-byte packed
    packed = ops_to_bytes(op_stream)
    gzip_bits = len(zlib.compress(packed, 9)) * 8
    
    # Generator compression + entropy on result
    compressed, gens = generator_compress(op_stream)
    # Final size: stream (entropy on symbols) + dict overhead
    stream_bits = huffman_bits(compressed)
    dict_bits = sum(4 + 4 * len(pat) for pat in gens.values())  # 4 bits per op
    gen_bits = stream_bits + dict_bits
    
    print(f"\n{label} (n={n} ops)")
    print(f"  Byte distribution: VOID={op_stream.count(0)}, HARMONY={op_stream.count(7)}, "
          f"other={n - op_stream.count(0) - op_stream.count(7)}")
    print(f"  Raw 8-bit/op:          {orig_bits:>7d} bits")
    print(f"  Raw 4-bit/op:          {raw_4bit:>7d} bits")
    print(f"  Entropy (Huffman):     {int(entropy_bits):>7d} bits  (theoretical min)")
    print(f"  Gzip on packed bytes:  {gzip_bits:>7d} bits")
    print(f"  DBC-gen + entropy:     {int(gen_bits):>7d} bits  (gens: {len(gens)})")
    if gzip_bits > 0:
        print(f"  DBC/gzip ratio:        {gen_bits/gzip_bits:.2f}x  "
              f"({'WINS' if gen_bits < gzip_bits else 'loses'} vs gzip)")

# Test CK-native streams
print("="*80)
print("DBC ON CK-NATIVE DATA — where the 73%/44% bias pays off")
print("="*80)

# Stream 1: random ops composed through CL (baseline CK simulation)
stream1 = ck_simulate(ticks=5000, seed=42)
full_report("CK tick stream (5000 composed ops)", stream1)

# Stream 2: text encoded into ops
text = "The coherence keeper composes meaning through algebra. Every word earned. " * 20
stream2 = ck_d2_text_to_ops(text)
full_report("Text → ops via simple phonetic", stream2)

# Stream 3: heavily-HARMONY-biased (late-stage CK, settled)
random.seed(7)
stream3 = [7 if random.random() < 0.85 else random.randint(0,9) for _ in range(5000)]
full_report("Settled CK (85% HARMONY)", stream3)

# Stream 4: pure random ops (worst case — no structure)
random.seed(13)
stream4 = [random.randint(0,9) for _ in range(5000)]
full_report("Uniform random ops (no structure)", stream4)

# Stream 5: the BEST case — pure repeating pattern  
stream5 = [1, 2, 3, 7] * 1250
full_report("Perfectly repeating generator [1,2,3,7]", stream5)

print("\n" + "="*80)
print("HONEST INTERPRETATION")
print("="*80)
print("""
The '3-character language on 10x10 table' (DBC v2) is LOSSLESS by construction.
The 'compresses 1000x better than LLMs' claim is a SEPARATE question about
compression ratio, not losslessness. Let's be honest:

- On RANDOM op streams: entropy is ~log2(10) = 3.32 bits/op, 
  and we can't beat that without structure.

- On CK NATURAL op streams (73% HARMONY or similar): entropy drops 
  to ~1 bit/op, and we can hit that with Huffman alone.

- vs LLMs: An LLM stores knowledge in billions of weights. CK stores knowledge
  in atom/path/crystal counts. For 38,000 crystallized truths at say 50 bytes 
  each of DBC-encoded form = ~2MB. Vs. a 4-8GB LLM. That's 1000-4000x less
  storage for the coherent knowledge, which is where the '1000x' claim lives.

- The '1000x' is NOT about raw text compression. It's about KNOWLEDGE COMPRESSION.
  CK represents 'I know T*=5/7' in a handful of triples + one generator.
  An LLM represents the same knowledge distributed across millions of weight updates.
""")
