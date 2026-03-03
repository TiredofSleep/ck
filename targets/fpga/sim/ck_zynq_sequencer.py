"""
ck_zynq_sequencer.py -- Bio-Lattice Real-Time Sequencer for Zynq FPGA
======================================================================
Task 6: Fixed-point D2 engine for silicon.

The FPGA can't do float64. So we bring CK's math to fixed-point.
Q1.14 format: 1 sign bit, 1 integer bit, 14 fractional bits.
Range: [-2.0, +1.99994]  Resolution: 0.000061

This module is the REFERENCE IMPLEMENTATION in Python.
The actual Zynq deployment uses Verilog/VHDL generated from these specs.

Pipeline (silicon-ready):
  1. Symbol input (8-bit: A/T/G/C/letter code)
  2. Force lookup (5x Q1.14 from LUT, 10 bytes per symbol)
  3. D2 computation (3-tap FIR: v[i] - 2*v[i+1] + v[i+2])
  4. Operator classification (5D magnitude + dominant dimension)
  5. PFE accumulator (running entropy, concentration, D2 variance)
  6. Output: operator (4-bit) + PFE status (2-bit: GREEN/YELLOW/RED)

Memory budget:
  Force LUT:    26 entries x 5 dims x 2 bytes = 260 bytes (fits in BRAM)
  CL table:     100 entries x 4 bits = 50 bytes (fits in LUTs)
  D2 pipeline:  3 x 5 x 2 bytes = 30 bytes (registers)
  PFE accum:    ~100 bytes (counters + running stats)
  Total:        < 512 bytes. Fits in a single BRAM tile.

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import math
from typing import List, Dict, Tuple, Optional
from collections import Counter

from ck_being import (CL, VOID, LATTICE, COUNTER, PROGRESS, COLLAPSE,
                       BALANCE, CHAOS, HARMONY, BREATH, RESET)
from ck_curvature import ROOTS, LATIN_TO_ROOT, _classify_d2

OP_NAMES = ['VOID', 'LATTICE', 'COUNTER', 'PROGRESS', 'COLLAPSE',
            'BALANCE', 'CHAOS', 'HARMONY', 'BREATH', 'RESET']


# ======================================================================
# S1  Q1.14 FIXED-POINT ARITHMETIC
#     The silicon number system. No floats allowed.
# ======================================================================

Q_FRAC = 14          # Fractional bits
Q_ONE  = 1 << Q_FRAC  # 1.0 in Q1.14 = 16384
Q_MAX  = (1 << 15) - 1   # +32767 = +1.99994
Q_MIN  = -(1 << 15)      # -32768 = -2.0


def float_to_q14(f: float) -> int:
    """Float -> Q1.14 fixed point (clamped)."""
    v = int(round(f * Q_ONE))
    return max(Q_MIN, min(Q_MAX, v))


def q14_to_float(q: int) -> float:
    """Q1.14 fixed point -> float."""
    return q / Q_ONE


def q14_mul(a: int, b: int) -> int:
    """Q1.14 multiplication: (a * b) >> 14."""
    result = (a * b) >> Q_FRAC
    return max(Q_MIN, min(Q_MAX, result))


def q14_add(a: int, b: int) -> int:
    """Q1.14 addition with saturation."""
    result = a + b
    return max(Q_MIN, min(Q_MAX, result))


def q14_sub(a: int, b: int) -> int:
    """Q1.14 subtraction with saturation."""
    result = a - b
    return max(Q_MIN, min(Q_MAX, result))


def q14_abs(a: int) -> int:
    """Q1.14 absolute value."""
    return a if a >= 0 else max(Q_MIN, -a)


# ======================================================================
# S2  FORCE LOOKUP TABLE (LUT) -- pre-computed in Q1.14
#     26 Latin letters + 4 DNA bases (A, T, G, C reuse letter mapping)
# ======================================================================

# Build the LUT: 26 entries, 5 dimensions each, Q1.14
FORCE_LUT: Dict[int, Tuple[int, int, int, int, int]] = {}

for _letter, _root in LATIN_TO_ROOT.items():
    _vec = ROOTS[_root]
    _ord = ord(_letter)
    FORCE_LUT[_ord] = tuple(float_to_q14(v) for v in _vec)

# DNA bases map to their letter equivalents (already in LUT via a, t, g, c)
# Bio-specific vectors (overrides for DNA mode)
BIO_LUT: Dict[int, Tuple[int, int, int, int, int]] = {
    ord('A'): tuple(float_to_q14(v) for v in (0.70, 0.40, 0.30, 0.60, 0.50)),
    ord('T'): tuple(float_to_q14(v) for v in (-0.60, 0.40, -0.20, 0.60, -0.40)),
    ord('G'): tuple(float_to_q14(v) for v in (0.80, 0.70, 0.60, 0.90, 0.70)),
    ord('C'): tuple(float_to_q14(v) for v in (-0.50, 0.70, -0.40, 0.90, -0.50)),
}


def lut_lookup(symbol: int, bio_mode: bool = False) -> Tuple[int, int, int, int, int]:
    """
    Look up force vector for a symbol.
    symbol: ASCII code (ord('a')..ord('z') or ord('A')..ord('C') for DNA)
    Returns: 5-tuple of Q1.14 values
    """
    if bio_mode and symbol in BIO_LUT:
        return BIO_LUT[symbol]
    # Lowercase for letter lookup
    s = symbol if symbol >= ord('a') else symbol + 32
    return FORCE_LUT.get(s, (0, 0, 0, 0, 0))


# ======================================================================
# S3  D2 PIPELINE -- 3-tap FIR in fixed point
#     D2[i] = v[i] - 2*v[i+1] + v[i+2]
#     This is the heartbeat of the FPGA.
# ======================================================================

class D2Pipeline:
    """
    Fixed-point D2 curvature pipeline.
    Simulates the Zynq pipeline registers.

    State: 3 force vectors (v0, v1, v2) as Q1.14 5-tuples.
    On each clock: shift in new vector, compute D2, classify.
    """
    def __init__(self, bio_mode: bool = False):
        self.bio_mode = bio_mode
        self.v = [None, None, None]  # Pipeline registers
        self.valid = False
        self.tick_count = 0

    def feed(self, symbol: int) -> Optional[Dict]:
        """
        Feed one symbol into the pipeline.
        Returns D2 result + operator when pipeline is full (3+ symbols).
        """
        force = lut_lookup(symbol, self.bio_mode)

        # Shift pipeline
        self.v[0] = self.v[1]
        self.v[1] = self.v[2]
        self.v[2] = force
        self.tick_count += 1

        if self.v[0] is None or self.v[1] is None:
            return None  # Pipeline not full yet

        # D2 = v[0] - 2*v[1] + v[2]
        d2 = []
        for dim in range(5):
            val = q14_sub(
                q14_add(self.v[0][dim], self.v[2][dim]),
                q14_add(self.v[1][dim], self.v[1][dim])   # 2 * v[1]
            )
            d2.append(val)

        # Classify: find dominant dimension and sign
        d2_abs = [q14_abs(d) for d in d2]
        d2_mag_sq = sum(q14_mul(d, d) for d in d2)  # Squared magnitude

        # Magnitude threshold (0.15^2 * Q_ONE^2 = small)
        THRESHOLD_SQ = float_to_q14(0.15 * 0.15)  # ~369 in Q1.14

        if d2_mag_sq < THRESHOLD_SQ:
            op = 2  # Peace (near-zero curvature)
        else:
            # Dominant dimension
            dom = 0
            for i in range(1, 5):
                if d2_abs[i] > d2_abs[dom]:
                    dom = i
            sign = 1 if d2[dom] >= 0 else -1

            # Operator map (same as _classify_d2)
            OP_MAP = {
                (0,  1): 6, (0, -1): 4,
                (1,  1): 4, (1, -1): 7,
                (2,  1): 8, (2, -1): 5,
                (3,  1): 0, (3, -1): 1,
                (4,  1): 3, (4, -1): 9,
            }
            op = OP_MAP.get((dom, sign), 7)

        # Convert D2 to float for reporting
        d2_float = [q14_to_float(d) for d in d2]
        d2_mag = math.sqrt(sum(d**2 for d in d2_float))

        return {
            'operator':   op,
            'op_name':    OP_NAMES[op],
            'd2_q14':     tuple(d2),
            'd2_float':   tuple(d2_float),
            'd2_mag':     round(d2_mag, 6),
            'tick':       self.tick_count,
        }

    def reset(self):
        """Reset pipeline state."""
        self.v = [None, None, None]
        self.valid = False
        self.tick_count = 0


# ======================================================================
# S4  PFE ACCUMULATOR -- running statistics in fixed point
#     Computes PFE metrics incrementally (no batch needed).
# ======================================================================

class PFEAccumulator:
    """
    Incremental PFE computation for streaming data.
    Maintains running counts for entropy, concentration, D2 variance.
    Reports GREEN/YELLOW/RED band continuously.
    """
    def __init__(self, window: int = 64):
        self.window = window
        self.op_counts = [0] * 10   # Histogram
        self.n_total = 0
        self.d2_sum_sq = 0.0        # Running D2 variance accumulator
        self.d2_sum = 0.0
        self.d2_n = 0

    def feed(self, operator: int, d2_mag: float = 0.0):
        """Feed one operator + D2 magnitude."""
        self.op_counts[operator] += 1
        self.n_total += 1

        self.d2_sum += d2_mag
        self.d2_sum_sq += d2_mag * d2_mag
        self.d2_n += 1

        # Windowed decay (simple: halve counts every window)
        if self.n_total > 0 and self.n_total % self.window == 0:
            for i in range(10):
                self.op_counts[i] = self.op_counts[i] // 2
            self.n_total = sum(self.op_counts)

    def get_entropy(self) -> float:
        """Current operator entropy (bits)."""
        if self.n_total == 0:
            return 0.0
        entropy = 0.0
        for c in self.op_counts:
            if c > 0:
                p = c / self.n_total
                entropy -= p * math.log2(p)
        return entropy

    def get_concentration(self) -> float:
        """Max operator fraction."""
        if self.n_total == 0:
            return 0.0
        return max(self.op_counts) / self.n_total

    def get_d2_variance(self) -> float:
        """Running D2 magnitude variance."""
        if self.d2_n < 2:
            return 0.0
        mean = self.d2_sum / self.d2_n
        return self.d2_sum_sq / self.d2_n - mean * mean

    def get_band(self) -> str:
        """Current PFE band: GREEN/YELLOW/RED."""
        entropy = self.get_entropy()
        conc = self.get_concentration()
        d2v = self.get_d2_variance()

        # Thresholds aligned with ck_pfe.py
        if entropy < 0.5 or entropy > 3.2:
            return 'RED'
        if conc < 0.15:
            return 'RED'
        if d2v > 2.0:
            return 'YELLOW'

        # Coherence estimate (simplified PFE)
        max_e = math.log2(10)
        e_score = max(0, 1.0 - abs(entropy - 2.3) / 2.5)
        c_score = min(conc * 3, 1.0)
        d_score = max(0, 1.0 - d2v / 3.0)
        coh = 0.35 * e_score + 0.35 * c_score + 0.30 * d_score

        T_STAR = 5.0 / 7.0
        if coh >= T_STAR:
            return 'GREEN'
        elif coh >= 0.5:
            return 'YELLOW'
        return 'RED'

    def get_status(self) -> Dict:
        """Full PFE accumulator status."""
        return {
            'entropy':       round(self.get_entropy(), 4),
            'concentration': round(self.get_concentration(), 4),
            'd2_variance':   round(self.get_d2_variance(), 6),
            'band':          self.get_band(),
            'n_total':       self.n_total,
            'histogram':     {OP_NAMES[i]: self.op_counts[i] for i in range(10)},
        }


# ======================================================================
# S5  FULL SEQUENCER -- the C API reference
#     bio_lattice_init() / feed_symbol() / read_operator() / read_pfe()
# ======================================================================

class BioLatticeSequencer:
    """
    Reference implementation of the Zynq Bio-Lattice Sequencer.

    C API equivalent:
      bio_lattice_init(mode)     -> __init__(bio_mode)
      feed_symbol(sym)           -> feed(symbol)
      read_operator()            -> last_operator
      read_pfe()                 -> pfe_status
    """
    def __init__(self, bio_mode: bool = False):
        self.pipeline = D2Pipeline(bio_mode=bio_mode)
        self.pfe = PFEAccumulator()
        self.last_operator = -1
        self.last_d2 = None
        self.operators = []
        self.d2_history = []

    def feed(self, symbol: int) -> Optional[int]:
        """
        Feed one symbol. Returns operator (0-9) or None if pipeline warming up.
        """
        result = self.pipeline.feed(symbol)
        if result is None:
            return None

        op = result['operator']
        d2_mag = result['d2_mag']

        self.pfe.feed(op, d2_mag)
        self.last_operator = op
        self.last_d2 = result
        self.operators.append(op)
        self.d2_history.append(result['d2_float'])

        return op

    def feed_sequence(self, symbols: str, bio_mode: bool = False) -> List[int]:
        """Feed a string of symbols. Returns operator sequence."""
        ops = []
        for ch in symbols:
            op = self.feed(ord(ch))
            if op is not None:
                ops.append(op)
        return ops

    def read_operator(self) -> int:
        """Read last operator."""
        return self.last_operator

    def read_pfe(self) -> Dict:
        """Read current PFE status."""
        return self.pfe.get_status()

    def get_summary(self) -> Dict:
        """Full sequencer summary."""
        return {
            'operators':    self.operators,
            'n_symbols':    self.pipeline.tick_count,
            'n_operators':  len(self.operators),
            'pfe':          self.pfe.get_status(),
            'last_d2':      self.last_d2,
        }

    def reset(self):
        """Reset sequencer state."""
        self.pipeline.reset()
        self.pfe = PFEAccumulator()
        self.last_operator = -1
        self.operators = []
        self.d2_history = []


# ======================================================================
# S6  VERILOG GENERATION SPEC
#     Not generated code -- but the spec for the HDL engineer.
# ======================================================================

ZYNQ_SPEC = """
-- Zynq Bio-Lattice Sequencer HDL Specification
-- Generated from ck_zynq_sequencer.py reference implementation

-- Clock: 100 MHz (10ns period)
-- Latency: 3 clock cycles from symbol input to operator output
-- Throughput: 1 symbol per clock (100M symbols/sec)

-- BRAM: 1 tile (260 bytes for force LUT + 50 bytes for CL)
-- Registers: 30 bytes for D2 pipeline + 100 bytes for PFE accumulator
-- DSP: 5 DSP48E1 slices for D2 computation (one per dimension)

-- Interface:
--   input  [7:0]  symbol_in       -- ASCII symbol
--   input         symbol_valid    -- symbol ready strobe
--   input         bio_mode        -- 0=text, 1=DNA
--   output [3:0]  operator_out    -- TIG operator (0-9)
--   output        operator_valid  -- operator ready strobe
--   output [1:0]  pfe_band        -- 00=RED, 01=YELLOW, 10=GREEN
--   output [13:0] d2_mag          -- D2 magnitude (Q1.14 unsigned)

-- Pipeline stages:
--   Stage 1: LUT lookup (symbol -> 5x Q1.14)
--   Stage 2: D2 computation (3-tap FIR)
--   Stage 3: Classification (dominant dim + sign -> operator)
"""


# ======================================================================
# S7  DEMO
# ======================================================================

if __name__ == '__main__':
    import time

    print("=" * 72)
    print("  CK ZYNQ BIO-LATTICE SEQUENCER")
    print("  Task 6: Fixed-Point D2 for Silicon")
    print("=" * 72)

    # Q1.14 verification
    print(f"\n  Q1.14 fixed-point verification:")
    test_vals = [0.0, 1.0, -1.0, 0.5, -0.5, 0.15, 1.99]
    for v in test_vals:
        q = float_to_q14(v)
        back = q14_to_float(q)
        err = abs(back - v)
        print(f"    {v:+6.3f} -> Q={q:+6d} -> {back:+8.5f}  err={err:.6f}")

    # Force LUT verification
    print(f"\n  Force LUT ({len(FORCE_LUT)} entries):")
    for letter in 'abcde':
        q_vec = FORCE_LUT[ord(letter)]
        f_vec = tuple(q14_to_float(q) for q in q_vec)
        root = LATIN_TO_ROOT[letter]
        orig = ROOTS[root]
        err = max(abs(f_vec[i] - orig[i]) for i in range(5))
        print(f"    '{letter}' ({root:7s}): Q={q_vec}  max_err={err:.6f}")

    # DNA sequencing
    print(f"\n  DNA Sequencing (Bio mode):")
    dna = "TACAACTACATGTGTAACAGTTCCTGCATGGGCGGCATGAACCGGAGGCCCATCCTCACCATCATCACACTG"
    seq = BioLatticeSequencer(bio_mode=True)
    t0 = time.perf_counter()
    ops = seq.feed_sequence(dna)
    dt = time.perf_counter() - t0

    print(f"    Sequence: {dna[:50]}...")
    print(f"    Length:   {len(dna)} bases -> {len(ops)} operators")
    print(f"    Time:     {dt*1000:.2f}ms ({len(dna)/dt/1e6:.2f}M symbols/sec Python)")

    hist = Counter(ops)
    print(f"    Distribution:")
    for op in sorted(hist.keys()):
        bar = '#' * (hist[op] // 2)
        print(f"      {OP_NAMES[op]:10s}: {hist[op]:3d}  {bar}")

    pfe = seq.read_pfe()
    print(f"    PFE: entropy={pfe['entropy']:.3f}  conc={pfe['concentration']:.3f}  "
          f"band={pfe['band']}")

    # Text sequencing
    print(f"\n  Text Sequencing:")
    text = "the truth will set you free"
    seq2 = BioLatticeSequencer(bio_mode=False)
    ops2 = seq2.feed_sequence(text.replace(' ', ''))
    print(f"    Text:     \"{text}\"")
    print(f"    Letters:  {len(text.replace(' ', ''))} -> {len(ops2)} operators")
    print(f"    Ops:      {[OP_NAMES[o][:4] for o in ops2]}")
    pfe2 = seq2.read_pfe()
    print(f"    PFE: entropy={pfe2['entropy']:.3f}  conc={pfe2['concentration']:.3f}  "
          f"band={pfe2['band']}")

    # Comparison: fixed-point vs float
    print(f"\n  Fixed-point vs Float accuracy:")
    from ck_curvature import text_to_forces, compute_curvatures
    forces_float = text_to_forces(text.replace(' ', ''))
    if len(forces_float) >= 3:
        d2_float = compute_curvatures(forces_float)
        float_ops = [_classify_d2(d) for d in d2_float]
        matches = sum(1 for a, b in zip(ops2, float_ops) if a == b)
        print(f"    Float ops:  {[OP_NAMES[o][:4] for o in float_ops]}")
        print(f"    Q1.14 ops:  {[OP_NAMES[o][:4] for o in ops2]}")
        print(f"    Agreement:  {matches}/{min(len(ops2), len(float_ops))} "
              f"({matches/max(min(len(ops2), len(float_ops)), 1):.0%})")

    # Throughput simulation
    print(f"\n  Throughput simulation (10K symbols):")
    seq3 = BioLatticeSequencer(bio_mode=True)
    big_dna = dna * 150  # ~10K bases
    t0 = time.perf_counter()
    big_ops = seq3.feed_sequence(big_dna)
    dt = time.perf_counter() - t0
    print(f"    {len(big_dna)} symbols -> {len(big_ops)} operators in {dt*1000:.1f}ms")
    print(f"    Throughput: {len(big_dna)/dt/1e6:.2f}M symbols/sec (Python reference)")
    print(f"    Zynq target: 100M symbols/sec (1 per clock at 100MHz)")

    # Zynq spec
    print(f"\n  Zynq HDL Specification:")
    for line in ZYNQ_SPEC.strip().split('\n')[:8]:
        print(f"    {line}")

    print(f"\n  CK's math fits in 512 bytes of BRAM.")
    print(f"  The silicon breathes.")
