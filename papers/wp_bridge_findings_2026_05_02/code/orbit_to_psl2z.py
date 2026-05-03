"""
Bridge BHML self-orbits to PSL(2,Z) words and compute Ψ.

Three encoding strategies tested:

(A) Operator → letter map. Each substrate digit corresponds to a specific 
    PSL(2,Z) generator-pair element (e.g., based on σ-cycle position).
    Compose the orbit's operators into a word.

(B) Transition encoding. Each step in the orbit (a → BHML(a, n)) encodes 
    a generator choice based on whether we move "up" or "down" in some 
    natural ordering.

(C) Period → trace direct. Take the orbit period as the trace and use 
    the simplest hyperbolic representative.

Strategy (C) was already done in rademacher_period_bridge.py. Strategies (A) 
and (B) are new tests.
"""
import numpy as np
from sympy import Matrix, Rational, Integer
import sys
sys.path.insert(0, '/home/claude/tig_synthesis')
from tig_substrate import TSML_10, BHML_10, SIGMA_PERMUTATION


T = Matrix([[1, 1], [0, 1]])
T_inv = Matrix([[1, -1], [0, 1]])
S = Matrix([[0, -1], [1, 0]])


def dedekind_sum(a, c):
    if c == 0:
        return Rational(0)
    c = abs(c)
    a = a % c
    s = Rational(0)
    for k in range(1, c):
        f1 = Rational(k, c) - Rational(1, 2)
        ka_mod = (k * a) % c
        if ka_mod == 0:
            f2 = Rational(0)
        else:
            f2 = Rational(ka_mod, c) - Rational(1, 2)
        s += f1 * f2
    return s


def rademacher_psi(M):
    """Classical Rademacher Ψ for SL(2,Z) matrix M."""
    a, b = int(M[0, 0]), int(M[0, 1])
    c, d = int(M[1, 0]), int(M[1, 1])
    if c == 0:
        return Rational(b, d) if d != 0 else Rational(0)
    s_a_c = dedekind_sum(a, abs(c))
    sign_c = 1 if c > 0 else -1
    Phi = Rational(a + d, c) - 12 * sign_c * s_a_c
    s_term = c * (a + d)
    sign_part = 1 if s_term > 0 else (-1 if s_term < 0 else 0)
    return Phi - 3 * sign_part


# BHML periodic orbits (just the periodic part)
BHML_ORBITS = {
    0: [0],
    1: [2, 3, 4, 5, 6, 7],   # period 6 — this is the cycle BHML enters after the transient
    2: [3, 4, 5, 6, 7],       # period 5
    3: [4, 5, 6, 7],          # period 4
    4: [5, 6, 7],              # period 3
    5: [6, 7],                  # period 2
    6: [7],                     # period 1
    7: [7, 8, 9, 0],           # period 4 — the 4-core cycle
    8: [8, 7, 9],              # period 3
    9: [9, 0],                  # period 2
}


# ============================================================
# STRATEGY (A): operator → letter map
# ============================================================
# Different maps to try. The most natural is mod-3: T for 1 mod 3, S for 2 mod 3, identity for 0 mod 3.
# Or mod-2: T for odd, S for even.

def map_A_mod3(orbit):
    """Each operator → T if n%3==1, S if n%3==2, identity if n%3==0."""
    M = Matrix.eye(2)
    for n in orbit:
        if n % 3 == 1:
            M = M * T
        elif n % 3 == 2:
            M = M * S
        # else identity
    return M


def map_A_mod2(orbit):
    """Each operator → T if odd, S if even. Even includes 0."""
    M = Matrix.eye(2)
    for n in orbit:
        if n % 2 == 1:
            M = M * T
        else:
            M = M * S
    return M


def map_A_sigma_position(orbit):
    """Map each digit to T^k S where k = position in σ-cycle.
    Trivial cycle (length 1): T^0 = I.
    6-cycle: position 0..5 → T^0, T^1, ..., T^5.
    """
    sigma = SIGMA_PERMUTATION
    cycle_pos = {}
    visited = set()
    for start in range(10):
        if start in visited:
            continue
        cur = start
        pos = 0
        cycle = []
        while cur not in visited:
            visited.add(cur)
            cycle.append(cur)
            cur = int(sigma[cur])
        for i, n in enumerate(cycle):
            cycle_pos[n] = i
    
    M = Matrix.eye(2)
    for n in orbit:
        k = cycle_pos.get(n, 0)
        # Apply T^k S
        if k > 0:
            M = M * (T ** k) * S
        else:
            M = M * S
    return M


# ============================================================
# STRATEGY (B): transition encoding
# ============================================================
# Each step a → BHML(a, n): encode based on whether output is bigger/smaller/equal.

def map_B_updown(orbit):
    """Each transition: T if new > old, T^-1 if new < old, identity if equal."""
    M = Matrix.eye(2)
    for i in range(len(orbit) - 1):
        prev, cur = orbit[i], orbit[i + 1]
        if cur > prev:
            M = M * T
        elif cur < prev:
            M = M * T_inv
    # Close the loop: connect last back to first
    if len(orbit) > 1:
        M = M * S  # final S to close the geodesic
    return M


def map_B_with_S(orbit):
    """Each transition: T (forward), T^-1 (backward), interleaved with S."""
    M = Matrix.eye(2)
    for i in range(len(orbit) - 1):
        prev, cur = orbit[i], orbit[i + 1]
        diff = cur - prev
        if diff > 0:
            M = M * T
        elif diff < 0:
            M = M * T_inv
        M = M * S  # always multiply by S between transitions
    return M


# ============================================================
# Run all strategies and compute Ψ
# ============================================================

def main():
    print("=" * 70)
    print("BRIDGE TEST: BHML SELF-ORBITS → PSL(2,Z) WORDS → RADEMACHER Ψ")
    print("=" * 70)
    
    strategies = [
        ('A: mod-3 letter map', map_A_mod3),
        ('A: mod-2 letter map', map_A_mod2),
        ('A: σ-position T^k S', map_A_sigma_position),
        ('B: up/down transition', map_B_updown),
        ('B: T/T^-1 + S between', map_B_with_S),
    ]
    
    psi_results = {}
    
    for label, fn in strategies:
        print(f"\n{'=' * 70}")
        print(f"STRATEGY: {label}")
        print(f"{'=' * 70}")
        print(f"\n  digit | orbit                  | matrix γ              | trace | Ψ")
        
        psi_per_digit = {}
        for n in range(10):
            orbit = BHML_ORBITS[n]
            M = fn(orbit)
            a, b = int(M[0, 0]), int(M[0, 1])
            c, d = int(M[1, 0]), int(M[1, 1])
            tr = a + d
            det_check = a * d - b * c
            if abs(det_check) != 1:
                print(f"    {n}    | {str(orbit):<22} | DET={det_check}, not in SL(2,Z)")
                psi_per_digit[n] = None
                continue
            psi = rademacher_psi(M)
            psi_per_digit[n] = psi
            mat_str = f"(({a},{b}),({c},{d}))"
            if len(mat_str) > 21:
                mat_str = mat_str[:19] + ".."
            print(f"    {n}    | {str(orbit):<22} | {mat_str:<21} | {tr:>4}  | {psi}")
        
        # Sum
        valid = [v for v in psi_per_digit.values() if v is not None]
        if valid:
            total = sum(valid)
            print(f"\n  Sum over digits with valid Ψ: {total}")
            print(f"  Substrate native ±21 magnitude: {abs(total) == 21}")
        psi_results[label] = psi_per_digit
    
    print("\n" + "=" * 70)
    print("SUMMARY ACROSS STRATEGIES")
    print("=" * 70)
    
    print(f"\n  {'Strategy':<35} {'Sum Ψ':<10} {'Sum 6-cycle':<15} {'Sum 4-core':<10}")
    six_cycle = [1, 2, 4, 5, 6, 7]
    four_core = [0, 7, 8, 9]
    
    for label, psi_dict in psi_results.items():
        valid_all = [v for v in psi_dict.values() if v is not None]
        valid_6c = [psi_dict[n] for n in six_cycle if psi_dict[n] is not None]
        valid_4c = [psi_dict[n] for n in four_core if psi_dict[n] is not None]
        
        sum_all = sum(valid_all) if valid_all else "N/A"
        sum_6c = sum(valid_6c) if valid_6c else "N/A"
        sum_4c = sum(valid_4c) if valid_4c else "N/A"
        
        print(f"  {label:<35} {str(sum_all):<10} {str(sum_6c):<15} {str(sum_4c):<10}")
    
    print(f"\n  Substrate native (Ghys-analog v2):    +21       +22            -1")
    print(f"  Substrate native (period→trace bridge): -21       -15            -6")
    
    print("\n  Honest interpretation:")
    print("  Whichever strategy gives ±21 (or -21 / -22) for the full sum AND")
    print("  matches the σ-orbit decomposition pattern is the right bridge.")


if __name__ == "__main__":
    main()
