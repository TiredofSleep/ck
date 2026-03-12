#!/usr/bin/env python3
"""
clay_rom_gen.py -- Generate Clay force vectors for FPGA ROM
============================================================

Creates force vectors for 6 Clay Millennium Problems at 12 fractal
levels each, quantized to Q1.14 fixed-point, output as Verilog
$readmemh hex file.

PHASE 1 (current): Synthetic test vectors using analytical patterns
  - Problem 0: Guaranteed HARMONY (binding curvature, constant others)
  - Problem 1: Guaranteed VOID (pressure curvature, negative)
  - Problem 2: Mixed operators (depth oscillation)
  - Problem 3: Guaranteed LATTICE (aperture curvature, negative)
  - Problem 4: Guaranteed BALANCE (continuity curvature, positive)
  - Problem 5: Sweep pattern (all dims active)

PHASE 2 (future): Real Clay generators from ck_sim package
  - Replace generate_synthetic() with generate_clay()
  - Requires: numpy, scipy, mpmath, ck_sim

Output: clay_vectors.hex (72 lines, 80-bit hex per line)
Format: AAAAPPPPDDDDBBBBCCCC (5 x 16-bit Q1.14, MSB first)

(c) 2026 Brayden Sanders / 7Site LLC
"""

import math
import os
import sys

# ============================================================
# Q1.14 Fixed-Point Encoding
# ============================================================
Q_FRAC  = 14
Q_SCALE = 1 << Q_FRAC   # 16384

N_PROBLEMS = 6
N_LEVELS   = 12
N_VECTORS  = N_PROBLEMS * N_LEVELS  # 72


def float_to_q14(f):
    """Float -> Q1.14 signed 16-bit integer."""
    val = int(round(f * Q_SCALE))
    return max(-32768, min(32767, val))


def q14_to_hex4(val):
    """16-bit signed integer -> 4-digit hex (unsigned representation)."""
    return f"{val & 0xFFFF:04x}"


# ============================================================
# PHASE 1: Synthetic Test Vectors
# ============================================================

def convex_curve(n, start, end):
    """Generate n-point convex curve from start to end.
    D2 will be positive (curvature bending upward).
    Uses quadratic: f(t) = start + (end-start)*t^2, t in [0,1]."""
    return [start + (end - start) * (i / (n - 1)) ** 2 for i in range(n)]


def concave_curve(n, start, end):
    """Generate n-point concave curve. D2 negative."""
    return [start + (end - start) * (1 - ((n - 1 - i) / (n - 1)) ** 2) for i in range(n)]


def oscillating(n, center, amplitude, phase=0.0):
    """Generate n-point sine wave. D2 varies in sign."""
    return [center + amplitude * math.sin(2 * math.pi * i / n + phase)
            for i in range(n)]


def constant(n, value):
    """Constant sequence. D2 = 0."""
    return [value] * n


def generate_synthetic():
    """Generate 72 synthetic force vectors (6 problems x 12 levels).

    Each vector = [aperture, pressure, depth, binding, continuity]
    All values in [0.0, 1.0].

    Problem designs:
      0: binding curves up (convex) -> HARMONY (binding+)
      1: pressure curves down (concave, then levels) -> VOID (pressure-)
      2: depth oscillates -> mix of PROGRESS/RESET
      3: aperture curves down -> LATTICE (aperture-)
      4: continuity curves up -> BALANCE (continuity+)
      5: all dims oscillate with different phases -> mixed
    """
    vectors = []

    # Problem 0: HARMONY guaranteed
    # binding has positive curvature, all others flat
    ap0 = constant(N_LEVELS, 0.50)
    pr0 = constant(N_LEVELS, 0.30)
    dp0 = constant(N_LEVELS, 0.60)
    bn0 = convex_curve(N_LEVELS, 0.10, 0.95)  # D2 > 0 -> HARMONY
    cn0 = constant(N_LEVELS, 0.50)

    # Problem 1: VOID guaranteed
    # pressure has negative curvature (concave), all others flat
    ap1 = constant(N_LEVELS, 0.40)
    pr1 = concave_curve(N_LEVELS, 0.10, 0.90)  # D2 < 0 -> VOID (pressure-)
    dp1 = constant(N_LEVELS, 0.50)
    bn1 = constant(N_LEVELS, 0.40)
    cn1 = constant(N_LEVELS, 0.60)

    # Problem 2: Mixed (depth oscillates)
    ap2 = constant(N_LEVELS, 0.50)
    pr2 = constant(N_LEVELS, 0.50)
    dp2 = oscillating(N_LEVELS, 0.50, 0.35)  # PROGRESS/RESET alternating
    bn2 = constant(N_LEVELS, 0.40)
    cn2 = constant(N_LEVELS, 0.50)

    # Problem 3: LATTICE guaranteed
    # aperture has negative curvature
    ap3 = concave_curve(N_LEVELS, 0.05, 0.90)  # D2 < 0 -> LATTICE (aperture-)
    pr3 = constant(N_LEVELS, 0.50)
    dp3 = constant(N_LEVELS, 0.40)
    bn3 = constant(N_LEVELS, 0.50)
    cn3 = constant(N_LEVELS, 0.50)

    # Problem 4: BALANCE guaranteed
    # continuity has positive curvature
    ap4 = constant(N_LEVELS, 0.50)
    pr4 = constant(N_LEVELS, 0.40)
    dp4 = constant(N_LEVELS, 0.50)
    bn4 = constant(N_LEVELS, 0.50)
    cn4 = convex_curve(N_LEVELS, 0.10, 0.95)  # D2 > 0 -> BALANCE (continuity+)

    # Problem 5: Full sweep (all dims oscillate, different phases)
    ap5 = oscillating(N_LEVELS, 0.50, 0.30, phase=0.0)
    pr5 = oscillating(N_LEVELS, 0.50, 0.30, phase=math.pi / 3)
    dp5 = oscillating(N_LEVELS, 0.50, 0.30, phase=2 * math.pi / 3)
    bn5 = oscillating(N_LEVELS, 0.50, 0.30, phase=math.pi)
    cn5 = oscillating(N_LEVELS, 0.50, 0.30, phase=4 * math.pi / 3)

    problems = [
        (ap0, pr0, dp0, bn0, cn0),
        (ap1, pr1, dp1, bn1, cn1),
        (ap2, pr2, dp2, bn2, cn2),
        (ap3, pr3, dp3, bn3, cn3),
        (ap4, pr4, dp4, bn4, cn4),
        (ap5, pr5, dp5, bn5, cn5),
    ]

    for prob_idx, (ap, pr, dp, bn, cn) in enumerate(problems):
        for level in range(N_LEVELS):
            vec = [
                max(0.0, min(1.0, ap[level])),
                max(0.0, min(1.0, pr[level])),
                max(0.0, min(1.0, dp[level])),
                max(0.0, min(1.0, bn[level])),
                max(0.0, min(1.0, cn[level])),
            ]
            vectors.append((prob_idx, level, vec))

    return vectors


# ============================================================
# D2 Verification (software reference)
# ============================================================

OP_NAMES = [
    "VOID", "LATTICE", "COUNTER", "PROGRESS", "COLLAPSE",
    "BALANCE", "CHAOS", "HARMONY", "BREATH", "RESET"
]

D2_OP_MAP = [
    (6, 1),   # aperture:   + = CHAOS,    - = LATTICE
    (4, 0),   # pressure:   + = COLLAPSE, - = VOID
    (3, 9),   # depth:      + = PROGRESS, - = RESET
    (7, 2),   # binding:    + = HARMONY,  - = COUNTER
    (5, 8),   # continuity: + = BALANCE,  - = BREATH
]


def compute_d2_operators(vectors):
    """Compute D2 operators in software for verification.
    Returns list of (prob_idx, level_triple, operator, op_name)."""
    results = []

    for prob_idx in range(N_PROBLEMS):
        prob_vecs = [v[2] for v in vectors if v[0] == prob_idx]

        for i in range(len(prob_vecs) - 2):
            v0 = prob_vecs[i]      # oldest
            v1 = prob_vecs[i + 1]  # middle
            v2 = prob_vecs[i + 2]  # newest

            # D2 = v0 - 2*v1 + v2  (per dimension)
            d2 = [v0[d] - 2 * v1[d] + v2[d] for d in range(5)]

            # Argmax |D2|
            abs_d2 = [abs(x) for x in d2]
            max_dim = abs_d2.index(max(abs_d2))
            sign = 0 if d2[max_dim] >= 0 else 1
            op = D2_OP_MAP[max_dim][sign]

            results.append((prob_idx, (i, i + 1, i + 2), op, OP_NAMES[op]))

    return results


# ============================================================
# Output
# ============================================================

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    hdl_dir = os.path.join(script_dir, '..', 'hdl')
    build_dir = os.path.join(script_dir, '..', 'build')

    print()
    print("  ========================================")
    print("  CLAY ROM GENERATOR -- Phase 1 (Synthetic)")
    print("  ========================================")
    print(f"  Problems:  {N_PROBLEMS}")
    print(f"  Levels:    {N_LEVELS}")
    print(f"  Vectors:   {N_VECTORS}")
    print(f"  Format:    Q1.14 (16-bit signed)")
    print(f"  ROM width: 80 bits (5 x 16)")
    print()

    # Generate vectors
    vectors = generate_synthetic()
    assert len(vectors) == N_VECTORS, f"Expected {N_VECTORS} vectors, got {len(vectors)}"

    # Write hex file
    hex_path = os.path.join(hdl_dir, 'clay_vectors.hex')
    with open(hex_path, 'w') as f:
        f.write("// Clay Force Vector ROM -- Phase 1 (Synthetic)\n")
        f.write(f"// {N_PROBLEMS} problems x {N_LEVELS} levels = {N_VECTORS} vectors\n")
        f.write("// Format: AAAA_PPPP_DDDD_BBBB_CCCC (Q1.14 x 5)\n")
        f.write("// (c) 2026 Brayden Sanders / 7Site LLC\n")
        for prob_idx, level, vec in vectors:
            q14 = [float_to_q14(v) for v in vec]
            hex_str = ''.join(q14_to_hex4(v) for v in q14)
            f.write(f"{hex_str}  // P{prob_idx} L{level:2d}: "
                    f"({vec[0]:.3f}, {vec[1]:.3f}, {vec[2]:.3f}, {vec[3]:.3f}, {vec[4]:.3f})\n")

    print(f"  Hex file: {hex_path}")
    print(f"  Size:     {os.path.getsize(hex_path)} bytes")

    # Write info file
    info_path = os.path.join(hdl_dir, 'clay_vectors_info.txt')
    with open(info_path, 'w') as f:
        f.write("Clay Force Vector ROM -- Detailed Info\n")
        f.write("=" * 70 + "\n\n")

        for prob_idx, level, vec in vectors:
            q14 = [float_to_q14(v) for v in vec]
            name = ["NavierStokes", "Riemann", "PvsNP",
                    "YangMills", "BSD", "Hodge"][prob_idx]
            f.write(f"[{prob_idx}] {name:12s} L{level:2d}: "
                    f"({vec[0]:.4f}, {vec[1]:.4f}, {vec[2]:.4f}, {vec[3]:.4f}, {vec[4]:.4f}) "
                    f"Q14: ({q14[0]:6d}, {q14[1]:6d}, {q14[2]:6d}, {q14[3]:6d}, {q14[4]:6d})\n")

    print(f"  Info file: {info_path}")

    # Compute and display expected D2 operators
    results = compute_d2_operators(vectors)

    print()
    print("  ========================================")
    print("  EXPECTED D2 OPERATORS (software ref)")
    print("  ========================================")

    prob_names = ["NavierStokes", "Riemann", "PvsNP",
                  "YangMills", "BSD", "Hodge"]
    harmony_counts = [0] * N_PROBLEMS
    total_harmony = 0

    for prob_idx, triple, op, op_name in results:
        star = " ***" if op == 7 else ""
        print(f"  P{prob_idx} ({prob_names[prob_idx]:12s}) "
              f"L({triple[0]:2d},{triple[1]:2d},{triple[2]:2d}) -> "
              f"{op_name:10s} ({op}){star}")
        if op == 7:
            harmony_counts[prob_idx] += 1
            total_harmony += 1

    print()
    print("  ----------------------------------------")
    print(f"  Total D2 results:   {len(results)}")
    print(f"  Total HARMONY ops:  {total_harmony}")
    t_frac = total_harmony / len(results) if results else 0
    t_star = 5 / 7
    print(f"  Harmony fraction:   {t_frac:.4f}  (T* = {t_star:.4f})")
    print(f"  T* reached:         {'YES' if t_frac >= t_star else 'NO'}")
    print()
    for i, name in enumerate(prob_names):
        print(f"    {name:12s}: {harmony_counts[i]:2d}/10 HARMONY")
    print()

    # Write expected results for FPGA comparison
    ref_path = os.path.join(build_dir, 'clay_expected.txt')
    with open(ref_path, 'w') as f:
        f.write(f"Total HARMONY: {total_harmony}\n")
        f.write(f"Harmony fraction: {t_frac:.4f}\n")
        f.write(f"T* reached: {'YES' if t_frac >= t_star else 'NO'}\n\n")
        for i, name in enumerate(prob_names):
            f.write(f"{name}: {harmony_counts[i]}/10\n")
        f.write(f"\nOperator sequence:\n")
        for prob_idx, triple, op, op_name in results:
            f.write(f"P{prob_idx} L{triple[0]:2d}-{triple[2]:2d}: {op} ({op_name})\n")

    print(f"  Reference: {ref_path}")
    print()

    return 0


if __name__ == '__main__':
    sys.exit(main())
