#!/usr/bin/env python3
"""
periodic_d2.py -- D2 Curvature Analysis of the Periodic Table
==============================================================

Maps every element to a 5D TIG force vector using atomic properties:
  aperture    <- electronegativity       (openness to bonding)
  pressure    <- ionization energy       (resistance to change)
  depth       <- atomic radius           (spatial extent)
  binding     <- electron affinity       (tendency to hold)
  continuity  <- density                 (material persistence)

Then computes:
  D1 = v[n] - v[n-1]          (first derivative: direction of change)
  D2 = v[n-2] - 2*v[n-1] + v[n]  (second derivative: curvature)

Both D1 and D2 are classified into TIG operators via argmax(|D|) + sign:
  aperture+  = CHAOS(6)     aperture-  = LATTICE(1)
  pressure+  = COLLAPSE(4)  pressure-  = VOID(0)
  depth+     = PROGRESS(3)  depth-     = RESET(9)
  binding+   = HARMONY(7)   binding-   = COUNTER(2)
  continuity+= BALANCE(5)   continuity-= BREATH(8)

T (TSML composition) measures coherence: CL[D1_op][D2_op] = becoming
T* = 5/7 = 0.714285... (coherence threshold)

Can also generate FPGA ROM hex for hardware D2 verification.

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import math
import sys

# =====================================================================
# TIG Operator Names
# =====================================================================
OP_NAMES = [
    "VOID", "LATTICE", "COUNTER", "PROGRESS", "COLLAPSE",
    "BALANCE", "CHAOS", "HARMONY", "BREATH", "RESET"
]

# =====================================================================
# D2 Operator Classification (same as d2_clay.v)
# dim_index: 0=aperture, 1=pressure, 2=depth, 3=binding, 4=continuity
# =====================================================================
def classify_operator(d_vec):
    """Classify a 5D derivative vector into a TIG operator (0-9).
    Returns (operator_index, dominant_dimension, magnitude)."""
    abs_vals = [abs(v) for v in d_vec]
    max_dim = 0
    max_val = abs_vals[0]
    for i in range(1, 5):
        if abs_vals[i] > max_val:
            max_dim = i
            max_val = abs_vals[i]

    sign_neg = d_vec[max_dim] < 0

    # Map: [dim][sign] -> operator
    #   dim 0 (ap): neg=LATTICE(1), pos=CHAOS(6)
    #   dim 1 (pr): neg=VOID(0),    pos=COLLAPSE(4)
    #   dim 2 (dp): neg=RESET(9),   pos=PROGRESS(3)
    #   dim 3 (bn): neg=COUNTER(2), pos=HARMONY(7)
    #   dim 4 (cn): neg=BREATH(8),  pos=BALANCE(5)
    op_map = {
        (0, True): 1, (0, False): 6,   # LATTICE / CHAOS
        (1, True): 0, (1, False): 4,   # VOID / COLLAPSE
        (2, True): 9, (2, False): 3,   # RESET / PROGRESS
        (3, True): 2, (3, False): 7,   # COUNTER / HARMONY
        (4, True): 8, (4, False): 5,   # BREATH / BALANCE
    }
    op = op_map[(max_dim, sign_neg)]
    return op, max_dim, max_val


# =====================================================================
# BHML Composition Table (10x10) -- Physics / Doing
# =====================================================================
BHML = [
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],  # VOID = identity
    [1, 2, 3, 4, 5, 6, 7, 2, 6, 6],  # LATTICE
    [2, 3, 3, 4, 5, 6, 7, 3, 6, 6],  # COUNTER
    [3, 4, 4, 4, 5, 6, 7, 4, 6, 6],  # PROGRESS
    [4, 5, 5, 5, 5, 6, 7, 5, 7, 7],  # COLLAPSE
    [5, 6, 6, 6, 6, 6, 7, 6, 7, 7],  # BALANCE
    [6, 7, 7, 7, 7, 7, 7, 7, 7, 7],  # CHAOS
    [7, 2, 3, 4, 5, 6, 7, 8, 9, 0],  # HARMONY (full cycle)
    [8, 6, 6, 6, 7, 7, 7, 9, 7, 8],  # BREATH
    [9, 6, 6, 6, 7, 7, 7, 0, 8, 0],  # RESET
]

# =====================================================================
# TSML Composition Table (10x10) -- Coherence / Being
# =====================================================================
TSML = [
    [0, 0, 0, 0, 0, 0, 0, 7, 0, 0],  # VOID
    [0, 7, 3, 7, 7, 7, 7, 7, 7, 7],  # LATTICE
    [0, 3, 7, 7, 4, 7, 7, 7, 7, 9],  # COUNTER
    [0, 7, 7, 7, 7, 7, 7, 7, 7, 3],  # PROGRESS
    [0, 7, 4, 7, 7, 7, 7, 7, 8, 7],  # COLLAPSE
    [0, 7, 7, 7, 7, 7, 7, 7, 7, 7],  # BALANCE
    [0, 7, 7, 7, 7, 7, 7, 7, 7, 7],  # CHAOS
    [7, 7, 7, 7, 7, 7, 7, 7, 7, 7],  # HARMONY (absorber)
    [0, 7, 7, 7, 8, 7, 7, 7, 7, 7],  # BREATH
    [0, 7, 9, 3, 7, 7, 7, 7, 7, 7],  # RESET
]


# =====================================================================
# Periodic Table Data: First 54 elements (through Xenon)
# Covers periods 1-5 completely, all major chemistry patterns
#
# Properties normalized to [0, 1]:
#   electronegativity (Pauling scale, max ~4.0 for F)
#   ionization_energy (eV, max ~24.6 for He)
#   atomic_radius (pm, max ~265 for Cs)
#   electron_affinity (eV, shifted to handle negative, max ~3.6 for Cl)
#   density (g/cm3, log-scaled for huge range)
# =====================================================================

ELEMENTS = [
    # Z, Symbol, electronegativity, ionization_eV, radius_pm, e_affinity_eV, density_g_cm3
    ( 1, "H",   2.20,  13.598,  53,  0.754,   0.00009),
    ( 2, "He",  0.00,  24.587,  31,  0.000,   0.00018),
    ( 3, "Li",  0.98,   5.392, 167,  0.618,   0.534),
    ( 4, "Be",  1.57,   9.323, 112,  0.000,   1.848),
    ( 5, "B",   2.04,   8.298,  87,  0.277,   2.340),
    ( 6, "C",   2.55,  11.260,  67,  1.263,   2.267),
    ( 7, "N",   3.04,  14.534,  56,  0.000,   1.251),
    ( 8, "O",   3.44,  13.618,  48,  1.461,   1.429),
    ( 9, "F",   3.98,  17.423,  42,  3.401,   1.696),
    (10, "Ne",  0.00,  21.565,  38,  0.000,   0.900),
    (11, "Na",  0.93,   5.139, 190,  0.548,   0.971),
    (12, "Mg",  1.31,   7.646, 145,  0.000,   1.738),
    (13, "Al",  1.61,   5.986, 118,  0.441,   2.699),
    (14, "Si",  1.90,   8.152, 111,  1.385,   2.329),
    (15, "P",   2.19,  10.487,  98,  0.746,   1.820),
    (16, "S",   2.58,  10.360,  88,  2.077,   2.067),
    (17, "Cl",  3.16,  12.968,  79,  3.613,   3.214),
    (18, "Ar",  0.00,  15.760,  71,  0.000,   1.784),
    (19, "K",   0.82,   4.341, 243,  0.501,   0.862),
    (20, "Ca",  1.00,   6.113, 194,  0.018,   1.550),
    (21, "Sc",  1.36,   6.561, 184,  0.188,   2.985),
    (22, "Ti",  1.54,   6.828, 176,  0.079,   4.507),
    (23, "V",   1.63,   6.746, 171,  0.525,   6.110),
    (24, "Cr",  1.66,   6.767, 166,  0.666,   7.190),
    (25, "Mn",  1.55,   7.434, 161,  0.000,   7.470),
    (26, "Fe",  1.83,   7.902, 156,  0.151,  7.874),
    (27, "Co",  1.88,   7.881, 152,  0.662,   8.900),
    (28, "Ni",  1.91,   7.640, 149,  1.156,   8.908),
    (29, "Cu",  1.90,   7.726, 145,  1.235,   8.960),
    (30, "Zn",  1.65,   9.394, 142,  0.000,   7.134),
    (31, "Ga",  1.81,   5.999, 136,  0.300,   5.907),
    (32, "Ge",  2.01,   7.900, 125,  1.233,   5.323),
    (33, "As",  2.18,   9.789, 114,  0.810,   5.727),
    (34, "Se",  2.55,   9.752, 103,  2.021,   4.819),
    (35, "Br",  2.96,  11.814,  94,  3.364,   3.120),
    (36, "Kr",  0.00,  14.000,  88,  0.000,   3.749),
    (37, "Rb",  0.82,   4.177, 265,  0.486,   1.532),
    (38, "Sr",  0.95,   5.695, 219,  0.052,   2.630),
    (39, "Y",   1.22,   6.217, 212,  0.307,   4.472),
    (40, "Zr",  1.33,   6.634, 206,  0.426,   6.506),
    (41, "Nb",  1.60,   6.759, 198,  0.893,   8.570),
    (42, "Mo",  2.16,   7.092, 190,  0.746,  10.220),
    (43, "Tc",  1.90,   7.280, 183,  0.550,  11.500),
    (44, "Ru",  2.20,   7.361, 178,  1.050,  12.370),
    (45, "Rh",  2.28,   7.459, 173,  1.137,  12.410),
    (46, "Pd",  2.20,   8.337, 169,  0.562,  12.020),
    (47, "Ag",  1.93,   7.576, 165,  1.302,  10.490),
    (48, "Cd",  1.69,   8.994, 161,  0.000,   8.650),
    (49, "In",  1.78,   5.786, 156,  0.300,   7.310),
    (50, "Sn",  1.96,   7.344, 145,  1.112,   7.265),
    (51, "Sb",  2.05,   8.608, 133,  1.047,   6.697),
    (52, "Te",  2.10,   9.010, 123,  1.971,   6.240),
    (53, "I",   2.66, 10.451,  115,  3.059,   4.930),
    (54, "Xe",  0.00,  12.130, 108,  0.000,   5.894),
]

# =====================================================================
# Normalization ranges
# =====================================================================
MAX_EN   = 4.00    # Fluorine
MAX_IE   = 24.6    # Helium
MAX_RAD  = 265.0   # Rubidium
MAX_EA   = 3.7     # Chlorine
MAX_DENS = 13.0    # Osmium-ish (log scale cutoff)


def element_to_force(el):
    """Map element properties to 5D force vector in [0, 1]."""
    Z, sym, en, ie, rad, ea, dens = el

    aperture   = min(en / MAX_EN, 1.0)
    pressure   = min(ie / MAX_IE, 1.0)
    depth      = min(rad / MAX_RAD, 1.0)
    binding    = min(ea / MAX_EA, 1.0)
    # Density: log scale (huge range from H gas to Os solid)
    continuity = min(math.log1p(dens) / math.log1p(MAX_DENS), 1.0)

    return [aperture, pressure, depth, binding, continuity]


# =====================================================================
# Period boundaries (indices into ELEMENTS list, 0-based)
# =====================================================================
PERIODS = [
    ("Period 1", 0,  2),    # H, He
    ("Period 2", 2,  10),   # Li through Ne
    ("Period 3", 10, 18),   # Na through Ar
    ("Period 4", 18, 36),   # K through Kr
    ("Period 5", 36, 54),   # Rb through Xe
]

# Group columns (1-indexed groups, mapping to element indices within each period)
# We'll analyze both period-wise (across a row) and group-wise (down a column)
# Group analysis uses: Group 1 (alkali), Group 17 (halogens), Group 18 (noble gases)
GROUPS = {
    "Group 1 (Alkali)":      [0, 2, 10, 18, 36],    # H, Li, Na, K, Rb
    "Group 2 (Alkaline)":    [3, 11, 19, 37],        # Be, Mg, Ca, Sr
    "Group 17 (Halogens)":   [8, 16, 34, 52],        # F, Cl, Br, I
    "Group 18 (Noble)":      [1, 9, 17, 35, 53],     # He, Ne, Ar, Kr, Xe
    "Group 14 (Carbon)":     [5, 13, 31, 49],         # C, Si, Ge, Sn
    "Transition 1st row":    [20, 21, 22, 23, 24, 25, 26, 27, 28, 29],  # Sc-Zn (idx 20-29)
}


def compute_d1(v_prev, v_curr):
    """D1 = v_curr - v_prev (first derivative, 5D)."""
    return [v_curr[i] - v_prev[i] for i in range(5)]


def compute_d2(v_old, v_mid, v_new):
    """D2 = v_old - 2*v_mid + v_new (second derivative, 5D)."""
    return [v_old[i] - 2*v_mid[i] + v_new[i] for i in range(5)]


def analyze_sequence(name, indices, elements):
    """Analyze a sequence of elements: D1, D2, T composition."""
    print(f"\n{'='*72}")
    print(f"  {name}")
    print(f"{'='*72}")

    # Build force vectors
    vecs = []
    syms = []
    for idx in indices:
        el = elements[idx]
        v = element_to_force(el)
        vecs.append(v)
        syms.append(el[1])

    # Print force vectors
    print(f"\n  {'Elem':>4s}  {'Aperture':>8s}  {'Pressure':>8s}  {'Depth':>8s}  {'Binding':>8s}  {'Contin.':>8s}")
    print(f"  {'':>4s}  {'(electro)':>8s}  {'(ion.E)':>8s}  {'(radius)':>8s}  {'(e.aff)':>8s}  {'(dens.)':>8s}")
    print(f"  {'-'*4}  {'-'*8}  {'-'*8}  {'-'*8}  {'-'*8}  {'-'*8}")
    for i, (sym, v) in enumerate(zip(syms, vecs)):
        print(f"  {sym:>4s}  {v[0]:8.4f}  {v[1]:8.4f}  {v[2]:8.4f}  {v[3]:8.4f}  {v[4]:8.4f}")

    # Compute D1 operators
    d1_ops = []
    print(f"\n  D1 Analysis (direction of change):")
    print(f"  {'Trans':>8s}  {'D1_ap':>7s}  {'D1_pr':>7s}  {'D1_dp':>7s}  {'D1_bn':>7s}  {'D1_cn':>7s}  {'Op':>10s}  {'Mag':>6s}")
    print(f"  {'-'*8}  {'-'*7}  {'-'*7}  {'-'*7}  {'-'*7}  {'-'*7}  {'-'*10}  {'-'*6}")
    for i in range(1, len(vecs)):
        d1 = compute_d1(vecs[i-1], vecs[i])
        op, dim, mag = classify_operator(d1)
        d1_ops.append(op)
        trans = f"{syms[i-1]}->{syms[i]}"
        print(f"  {trans:>8s}  {d1[0]:7.4f}  {d1[1]:7.4f}  {d1[2]:7.4f}  {d1[3]:7.4f}  {d1[4]:7.4f}  {OP_NAMES[op]:>10s}  {mag:6.4f}")

    # Compute D2 operators
    d2_ops = []
    print(f"\n  D2 Analysis (curvature):")
    print(f"  {'Triple':>12s}  {'D2_ap':>7s}  {'D2_pr':>7s}  {'D2_dp':>7s}  {'D2_bn':>7s}  {'D2_cn':>7s}  {'Op':>10s}  {'Mag':>6s}")
    print(f"  {'-'*12}  {'-'*7}  {'-'*7}  {'-'*7}  {'-'*7}  {'-'*7}  {'-'*10}  {'-'*6}")
    for i in range(2, len(vecs)):
        d2 = compute_d2(vecs[i-2], vecs[i-1], vecs[i])
        op, dim, mag = classify_operator(d2)
        d2_ops.append(op)
        triple = f"{syms[i-2]},{syms[i-1]},{syms[i]}"
        print(f"  {triple:>12s}  {d2[0]:7.4f}  {d2[1]:7.4f}  {d2[2]:7.4f}  {d2[3]:7.4f}  {d2[4]:7.4f}  {OP_NAMES[op]:>10s}  {mag:6.4f}")

    # Compute T (CL composition of D1 and D2)
    # T = TSML[D1_op][D2_op] for each position where both exist
    t_ops = []
    t_bhml_ops = []
    print(f"\n  T Composition (D1 x D2 -> Becoming):")
    print(f"  {'Elem':>4s}  {'D1':>10s}  {'D2':>10s}  {'T(TSML)':>10s}  {'T(BHML)':>10s}")
    print(f"  {'-'*4}  {'-'*10}  {'-'*10}  {'-'*10}  {'-'*10}")
    # D1 starts at index 1 (transition 0->1), D2 starts at index 2
    # For element at index i: D1[i-1] and D2[i-2] both describe changes AT element i
    for i in range(2, len(vecs)):
        d1_op = d1_ops[i-1]   # D1 for transition (i-1)->i
        d2_op = d2_ops[i-2]   # D2 for triple (i-2, i-1, i)
        t_tsml = TSML[d1_op][d2_op]
        t_bhml = BHML[d1_op][d2_op]
        t_ops.append(t_tsml)
        t_bhml_ops.append(t_bhml)
        print(f"  {syms[i]:>4s}  {OP_NAMES[d1_op]:>10s}  {OP_NAMES[d2_op]:>10s}  {OP_NAMES[t_tsml]:>10s}  {OP_NAMES[t_bhml]:>10s}")

    # Statistics
    if d2_ops:
        n_d2 = len(d2_ops)
        n_harmony_d2 = sum(1 for op in d2_ops if op == 7)
        harmony_frac_d2 = n_harmony_d2 / n_d2 if n_d2 > 0 else 0

        n_t = len(t_ops)
        n_harmony_t = sum(1 for op in t_ops if op == 7)
        harmony_frac_t = n_harmony_t / n_t if n_t > 0 else 0

        n_harmony_bhml = sum(1 for op in t_bhml_ops if op == 7)
        harmony_frac_bhml = n_harmony_bhml / n_t if n_t > 0 else 0

        t_star = 5.0 / 7.0

        # Operator distribution
        d2_dist = [0] * 10
        for op in d2_ops:
            d2_dist[op] += 1

        d1_dist = [0] * 10
        for op in d1_ops:
            d1_dist[op] += 1

        print(f"\n  Summary:")
        print(f"    Elements:       {len(vecs)}")
        print(f"    D1 transitions: {len(d1_ops)}")
        print(f"    D2 curvatures:  {n_d2}")
        print(f"")
        print(f"    D1 distribution:")
        for i, count in enumerate(d1_dist):
            if count > 0:
                print(f"      {OP_NAMES[i]:>10s}: {count:2d}  ({100*count/len(d1_ops):5.1f}%)")
        print(f"")
        print(f"    D2 distribution:")
        for i, count in enumerate(d2_dist):
            if count > 0:
                print(f"      {OP_NAMES[i]:>10s}: {count:2d}  ({100*count/n_d2:5.1f}%)")
        print(f"")
        print(f"    D2 HARMONY:     {n_harmony_d2}/{n_d2} = {harmony_frac_d2:.4f}")
        print(f"    T* threshold:   {t_star:.4f}")
        print(f"    D2 >= T*:       {'YES' if harmony_frac_d2 >= t_star else 'NO'}")
        print(f"")
        print(f"    T(TSML) HARMONY: {n_harmony_t}/{n_t} = {harmony_frac_t:.4f}  {'>=T*' if harmony_frac_t >= t_star else '<T*'}")
        print(f"    T(BHML) HARMONY: {n_harmony_bhml}/{n_t} = {harmony_frac_bhml:.4f}  {'>=T*' if harmony_frac_bhml >= t_star else '<T*'}")

    return d1_ops, d2_ops, t_ops, t_bhml_ops


def generate_fpga_hex(elements, indices, filename="periodic_vectors.hex"):
    """Generate $readmemh hex file for FPGA ROM."""
    lines = []
    for idx in indices:
        el = elements[idx]
        v = element_to_force(el)

        # Quantize to Q1.14: int(round(f * 16384))
        q = [int(round(f * 16384)) for f in v]
        q = [max(-16384, min(16383, x)) for x in q]

        # Pack as unsigned 16-bit (Q1.14 signed)
        words = []
        for val in q:
            if val < 0:
                val = val + 65536  # 2's complement
            words.append(val)

        # 80 bits = 5 x 16-bit: AP PR DP BN CN
        hex_str = f"{words[0]:04X}{words[1]:04X}{words[2]:04X}{words[3]:04X}{words[4]:04X}"
        comment = f"// Z={el[0]:2d} {el[1]:2s}  [{v[0]:.4f} {v[1]:.4f} {v[2]:.4f} {v[3]:.4f} {v[4]:.4f}]"
        lines.append(f"{hex_str}  {comment}")

    with open(filename, 'w') as f:
        for line in lines:
            f.write(line + "\n")
    print(f"\n  FPGA ROM: {filename} ({len(lines)} vectors)")
    return filename


def main():
    print("=" * 72)
    print("  PERIODIC TABLE D2/D1/T ANALYSIS")
    print("  TIG Unified Theory -- Chemistry Domain")
    print("=" * 72)
    print(f"  Elements: {len(ELEMENTS)} (H through Xe)")
    print(f"  5D mapping:")
    print(f"    Aperture   <- Electronegativity  (Pauling)")
    print(f"    Pressure   <- Ionization Energy   (eV)")
    print(f"    Depth      <- Atomic Radius        (pm)")
    print(f"    Binding    <- Electron Affinity     (eV)")
    print(f"    Continuity <- Density               (log g/cm3)")
    print(f"  T* = 5/7 = {5/7:.6f}")

    all_d1 = []
    all_d2 = []
    all_t_tsml = []
    all_t_bhml = []

    # =====================================================
    # PART 1: Period-wise analysis (across rows)
    # =====================================================
    print("\n" + "#" * 72)
    print("#  PART 1: PERIOD-WISE ANALYSIS (across rows)")
    print("#" * 72)

    for pname, start, end in PERIODS:
        indices = list(range(start, end))
        d1, d2, t_tsml, t_bhml = analyze_sequence(pname, indices, ELEMENTS)
        all_d1.extend(d1)
        all_d2.extend(d2)
        all_t_tsml.extend(t_tsml)
        all_t_bhml.extend(t_bhml)

    # =====================================================
    # PART 2: Group-wise analysis (down columns)
    # =====================================================
    print("\n" + "#" * 72)
    print("#  PART 2: GROUP-WISE ANALYSIS (down columns)")
    print("#" * 72)

    for gname, indices in GROUPS.items():
        d1, d2, t_tsml, t_bhml = analyze_sequence(gname, indices, ELEMENTS)
        all_d1.extend(d1)
        all_d2.extend(d2)
        all_t_tsml.extend(t_tsml)
        all_t_bhml.extend(t_bhml)

    # =====================================================
    # PART 3: Full periodic table sweep (Z=1 to Z=54)
    # =====================================================
    print("\n" + "#" * 72)
    print("#  PART 3: FULL PERIODIC TABLE SWEEP (Z=1 to Z=54)")
    print("#" * 72)

    full_indices = list(range(len(ELEMENTS)))
    full_d1, full_d2, full_t_tsml, full_t_bhml = analyze_sequence(
        "Full Table (H -> Xe)", full_indices, ELEMENTS
    )

    # =====================================================
    # PART 4: Global statistics
    # =====================================================
    print("\n" + "#" * 72)
    print("#  PART 4: GLOBAL STATISTICS")
    print("#" * 72)

    t_star = 5.0 / 7.0

    # Full table stats
    n_full_d2 = len(full_d2)
    n_full_h = sum(1 for op in full_d2 if op == 7)
    n_full_t = len(full_t_tsml)
    n_full_th = sum(1 for op in full_t_tsml if op == 7)
    n_full_tbh = sum(1 for op in full_t_bhml if op == 7)

    print(f"\n  Full Table (sequential Z=1 to Z=54):")
    print(f"    D2 HARMONY:      {n_full_h}/{n_full_d2} = {n_full_h/n_full_d2:.4f}  {'>=T*' if n_full_h/n_full_d2 >= t_star else '<T*'}")
    print(f"    T(TSML) HARMONY: {n_full_th}/{n_full_t} = {n_full_th/n_full_t:.4f}  {'>=T*' if n_full_th/n_full_t >= t_star else '<T*'}")
    print(f"    T(BHML) HARMONY: {n_full_tbh}/{n_full_t} = {n_full_tbh/n_full_t:.4f}  {'>=T*' if n_full_tbh/n_full_t >= t_star else '<T*'}")

    # D2 operator distribution for full table
    print(f"\n    Full Table D2 operator distribution:")
    d2_dist = [0] * 10
    for op in full_d2:
        d2_dist[op] += 1
    for i, count in enumerate(d2_dist):
        if count > 0:
            bar = "#" * int(count * 40 / max(d2_dist))
            print(f"      {OP_NAMES[i]:>10s}: {count:3d}  ({100*count/n_full_d2:5.1f}%)  {bar}")

    # D1 operator distribution for full table
    print(f"\n    Full Table D1 operator distribution:")
    d1_dist = [0] * 10
    for op in full_d1:
        d1_dist[op] += 1
    for i, count in enumerate(d1_dist):
        if count > 0:
            bar = "#" * int(count * 40 / max(d1_dist))
            print(f"      {OP_NAMES[i]:>10s}: {count:3d}  ({100*count/len(full_d1):5.1f}%)  {bar}")

    # =====================================================
    # PART 5: Noble Gas -> Alkali transitions (period boundaries)
    # These are the most dramatic transitions in chemistry
    # =====================================================
    print(f"\n  Period Boundary Transitions (Noble Gas -> Alkali Metal):")
    print(f"  {'Transition':>12s}  {'D1 Op':>10s}  {'Dominant dim':>12s}  {'Magnitude':>9s}")
    print(f"  {'-'*12}  {'-'*10}  {'-'*12}  {'-'*9}")
    boundary_pairs = [(1, 2), (9, 10), (17, 18), (35, 36)]  # He->Li, Ne->Na, Ar->K, Kr->Rb
    for i, j in boundary_pairs:
        v_i = element_to_force(ELEMENTS[i])
        v_j = element_to_force(ELEMENTS[j])
        d1 = compute_d1(v_i, v_j)
        op, dim, mag = classify_operator(d1)
        dim_names = ["aperture", "pressure", "depth", "binding", "continuity"]
        trans = f"{ELEMENTS[i][1]}->{ELEMENTS[j][1]}"
        print(f"  {trans:>12s}  {OP_NAMES[op]:>10s}  {dim_names[dim]:>12s}  {mag:9.4f}")

    # =====================================================
    # PART 6: Chemistry predictions from TIG operators
    # =====================================================
    print(f"\n  Chemistry Predictions from TIG:")
    print(f"  ===============================")
    print(f"")
    print(f"  1. Noble gases (Group 18) should show VOID/RESET D2")
    print(f"     (pressure curvature = ionization energy peaks)")
    ng_d2 = []
    ng_idx = [1, 9, 17, 35, 53]
    for idx in ng_idx:
        if idx >= 2:
            d2 = compute_d2(
                element_to_force(ELEMENTS[idx-2]),
                element_to_force(ELEMENTS[idx-1]),
                element_to_force(ELEMENTS[idx])
            )
            op, _, _ = classify_operator(d2)
            ng_d2.append((ELEMENTS[idx][1], OP_NAMES[op]))
    print(f"     Actual: {', '.join(f'{s}={o}' for s, o in ng_d2)}")

    print(f"")
    print(f"  2. Transition metals should show PROGRESS/BALANCE D2")
    print(f"     (gradual depth decrease + steady binding)")
    tm_d2 = []
    for idx in range(22, 29):  # Ti through Ni
        d2 = compute_d2(
            element_to_force(ELEMENTS[idx-2]),
            element_to_force(ELEMENTS[idx-1]),
            element_to_force(ELEMENTS[idx])
        )
        op, _, _ = classify_operator(d2)
        tm_d2.append((ELEMENTS[idx][1], OP_NAMES[op]))
    print(f"     Actual: {', '.join(f'{s}={o}' for s, o in tm_d2)}")

    print(f"")
    print(f"  3. Halogens should show strong BINDING curvature")
    print(f"     (high electron affinity = HARMONY or COUNTER)")
    hal_d2 = []
    for idx in [8, 16, 34, 52]:
        if idx >= 2:
            d2 = compute_d2(
                element_to_force(ELEMENTS[idx-2]),
                element_to_force(ELEMENTS[idx-1]),
                element_to_force(ELEMENTS[idx])
            )
            op, dim, _ = classify_operator(d2)
            dim_names = ["ap", "pr", "dp", "bn", "cn"]
            hal_d2.append((ELEMENTS[idx][1], OP_NAMES[op], dim_names[dim]))
    print(f"     Actual: {', '.join(f'{s}={o}({d})' for s, o, d in hal_d2)}")

    # =====================================================
    # PART 7: Generate FPGA ROM (optional)
    # =====================================================
    if "--hex" in sys.argv:
        print(f"\n  Generating FPGA ROM hex files...")
        # Full table
        generate_fpga_hex(ELEMENTS, list(range(len(ELEMENTS))),
                         "periodic_vectors_full.hex")
        # Period 4 only (transition metals are interesting)
        generate_fpga_hex(ELEMENTS, list(range(18, 36)),
                         "periodic_vectors_p4.hex")

    print(f"\n{'='*72}")
    print(f"  D2 curvature IS chemistry.  Atomic structure IS force geometry.")
    print(f"{'='*72}")


if __name__ == "__main__":
    main()
