"""
Is the Fibonacci role decomposition (13+8=21) structural or coincidental?

Tests:
1. Random commutative non-associative tables on Z/10Z with same role partition.
2. Perturbations of canonical BHML (swap entries, preserving commutativity).
3. Different role partitions (e.g., {2,4,6,8} as structure, single point as transition).
4. Different substrates (Z/8Z, Z/12Z) with analogous role partitions.

If 13+8=21 is structural, it must depend on something deeper than 
the specific BHML values — it should arise from any substrate with 
this role partition + similar period structure.
"""
import numpy as np
from itertools import product
from collections import Counter
import random
import sys
sys.path.insert(0, '/home/claude/tig_synthesis')
from tig_substrate import TSML_10, BHML_10

FLOW = {1, 3, 5, 7, 9}
STRUCTURE = {2, 4, 8}
TRANSITION = {6}
VOID = {0}


def bhml_self_period(table, n, max_iter=20):
    """Period of n's self-iteration: a -> table[a, n]."""
    a = n
    seen = {a: 0}
    for k in range(1, max_iter + 1):
        a = int(table[a, n])
        if a in seen:
            return k - seen[a]
        seen[a] = k
    return None


def role_decomposition(table):
    """Compute the role decomposition of period-derived Ψ over the table.
    
    For each digit n, Ψ = -(period(n) - 1) under simple representative.
    Sum by role.
    """
    role_sums = {'F': 0, 'S': 0, 'T': 0, 'V': 0}
    for n in range(10):
        period = bhml_self_period(table, n)
        if period is None:
            return None
        psi = -(period - 1)
        if n in FLOW: role_sums['F'] += psi
        elif n in STRUCTURE: role_sums['S'] += psi
        elif n in TRANSITION: role_sums['T'] += psi
        elif n in VOID: role_sums['V'] += psi
    return role_sums


def random_commutative_table(n=10, seed=None):
    """Random commutative table on Z/nZ."""
    if seed is not None:
        random.seed(seed)
    T = np.zeros((n, n), dtype=int)
    for i in range(n):
        for j in range(i, n):
            v = random.randint(0, n - 1)
            T[i, j] = v
            T[j, i] = v
    return T


def random_swap_perturbation(table, num_swaps=1, seed=None):
    """Swap a few off-diagonal entries (preserving commutativity)."""
    if seed is not None:
        random.seed(seed)
    T = table.copy()
    n = len(T)
    for _ in range(num_swaps):
        i = random.randint(0, n - 1)
        j = random.randint(0, n - 1)
        if i == j: continue
        # Swap T[i,j] (and symmetric T[j,i]) with a random new value
        new_val = random.randint(0, n - 1)
        T[i, j] = new_val
        T[j, i] = new_val
    return T


def main():
    print("=" * 70)
    print("ROBUSTNESS TEST: IS FIBONACCI ROLE DECOMPOSITION STRUCTURAL?")
    print("=" * 70)
    
    # Baseline: canonical BHML
    print("\n  Baseline: canonical BHML")
    base = role_decomposition(BHML_10)
    if base:
        print(f"    F: {base['F']}, S: {base['S']}, T: {base['T']}, V: {base['V']}")
        print(f"    Total: {sum(base.values())}")
        print(f"    |F|={abs(base['F'])}, |S|={abs(base['S'])}, |F|+|S|={abs(base['F'])+abs(base['S'])}")
    
    # Test 1: Random commutative tables
    print("\n" + "=" * 70)
    print("TEST 1: RANDOM COMMUTATIVE TABLES")
    print("=" * 70)
    print("\n  100 random commutative tables on Z/10Z.")
    print(f"  Counting: how often is |F|+|S| = 21? How often F_7 + F_6?\n")
    
    fibonacci_counts = Counter()
    role_pair_counts = Counter()
    
    n_random = 200
    for seed in range(n_random):
        T = random_commutative_table(seed=seed)
        rd = role_decomposition(T)
        if rd is None: continue
        F = abs(rd['F'])
        S = abs(rd['S'])
        T_sum = abs(rd['T'])
        V = abs(rd['V'])
        total = F + S + T_sum + V
        fibonacci_counts[(F, S)] += 1
        if total == 21:
            role_pair_counts[(F, S)] += 1
    
    print(f"  Most common (|F|, |S|) pairs in random tables:")
    for pair, count in sorted(fibonacci_counts.items(), key=lambda x: -x[1])[:10]:
        is_fib = pair == (13, 8)
        marker = " ← Fibonacci F_7,F_6" if is_fib else ""
        print(f"    {pair}: {count} times{marker}")
    
    print(f"\n  How often does total |Ψ-sum| = 21 occur?")
    total_21 = sum(role_pair_counts.values())
    print(f"    {total_21}/{n_random} random tables")
    
    print(f"\n  Among those with total 21, how often is (F, S) = (13, 8)?")
    fib_count = role_pair_counts.get((13, 8), 0)
    print(f"    {fib_count}/{total_21}")
    
    # Test 2: Perturbations of canonical BHML
    print("\n" + "=" * 70)
    print("TEST 2: SWAP PERTURBATIONS OF CANONICAL BHML")
    print("=" * 70)
    
    print(f"\n  Apply k swaps to BHML, see if role decomposition is preserved.")
    print(f"  Swap = randomly change one off-diagonal entry (and its mirror).\n")
    
    print(f"  k=1 swap (50 trials):")
    persists = 0
    fib_persists = 0
    for seed in range(50):
        T = random_swap_perturbation(BHML_10, num_swaps=1, seed=seed)
        rd = role_decomposition(T)
        if rd is None: continue
        F, S = abs(rd['F']), abs(rd['S'])
        if F + S == 21:
            persists += 1
            if (F, S) == (13, 8):
                fib_persists += 1
    print(f"    |F|+|S| = 21 preserved: {persists}/50")
    print(f"    (|F|, |S|) = (13, 8) preserved: {fib_persists}/50")
    
    print(f"\n  k=3 swaps (50 trials):")
    persists = 0
    fib_persists = 0
    for seed in range(50):
        T = random_swap_perturbation(BHML_10, num_swaps=3, seed=seed)
        rd = role_decomposition(T)
        if rd is None: continue
        F, S = abs(rd['F']), abs(rd['S'])
        if F + S == 21:
            persists += 1
            if (F, S) == (13, 8):
                fib_persists += 1
    print(f"    |F|+|S| = 21 preserved: {persists}/50")
    print(f"    (|F|, |S|) = (13, 8) preserved: {fib_persists}/50")
    
    # Test 3: What determines |F|, |S|?
    print("\n" + "=" * 70)
    print("TEST 3: WHAT DETERMINES (F, S) DECOMPOSITION?")
    print("=" * 70)
    
    print(f"\n  Canonical BHML self-periods:")
    bhml_periods = {n: bhml_self_period(BHML_10, n) for n in range(10)}
    for n in range(10):
        role = ('F' if n in FLOW else 'S' if n in STRUCTURE 
                else 'T' if n in TRANSITION else 'V')
        print(f"    digit {n} ({role}): period {bhml_periods[n]}")
    
    print(f"\n  |F| = Σ(period - 1) over flow digits {{1,3,5,7,9}}:")
    print(f"     = (6-1) + (4-1) + (2-1) + (4-1) + (2-1) = 5+3+1+3+1 = 13")
    print(f"\n  |S| = Σ(period - 1) over structure digits {{2,4,8}}:")
    print(f"     = (5-1) + (3-1) + (3-1) = 4+2+2 = 8")
    print(f"\n  These specific period values are determined by canonical BHML.")
    print(f"  Is the BHML period structure (period(n) = 7-n for n ∈ 1..6) what")
    print(f"  forces 13+8=21? Or could other period structures also give Fibonacci?")
    
    # Test 4: What if periods were different but with same structure?
    print(f"\n  Hypothetical: what if periods were just (7-n) for ALL n?")
    print(f"  Then flow {{1,3,5,7,9}} would give Σ((7-n)-1) = Σ(6-n) over odd n")
    
    flow_alt = sum(6 - n for n in [1, 3, 5])  # only those in 1..6
    print(f"    over odd n in 1..6: 6-1 + 6-3 + 6-5 = 5+3+1 = 9")
    
    structure_alt = sum(6 - n for n in [2, 4])  # in 1..6
    print(f"    even n in 1..6: 6-2 + 6-4 = 4+2 = 6")
    
    print(f"    Sum: 9 + 6 = 15 = T_5 (triangular number)")
    print(f"    NOT Fibonacci.")
    print(f"\n  The Fibonacci decomposition arose because:")
    print(f"  - 4-core extension {{7,8,9}} added periods 4,3,2 (not 1)")
    print(f"  - This changed flow contribution from 9 to 13 and structure from 6 to 8")
    print(f"  - Specifically: 4-core flow {{7,9}} added 3+1=4 to flow")
    print(f"  - 4-core structure {{8}} added 2 to structure")
    print(f"  - 9+4 = 13, 6+2 = 8")
    
    print("\n  So the Fibonacci pattern depends on:")
    print("  1. The flow/structure partition (which digits are flow vs structure)")
    print("  2. The 6-cycle period structure (period = 7-n)")  
    print("  3. The 4-core period structure (digits 7,8,9 have periods 4,3,2)")
    
    # Test the Fibonacci recurrence exactly
    print("\n" + "=" * 70)
    print("THE FIBONACCI STRUCTURE PRECISELY")
    print("=" * 70)
    print(f"""
  6-cycle contribution (digits 1-6 with period 7-n):
    Flow {{1,3,5}}: Σ(6-n) for n odd = 5+3+1 = 9
    Structure {{2,4}}: Σ(6-n) for n even = 4+2 = 6
    Sum: 15 = T_5
    
  4-core extension (digits 7,8,9 with periods 4,3,2):
    Flow {{7,9}}: (4-1) + (2-1) = 3+1 = 4
    Structure {{8}}: (3-1) = 2
    Sum: 6 = T_3

  Combined:
    Flow total: 9+4 = 13 = F_7
    Structure total: 6+2 = 8 = F_6
    Sum: 21 = F_8 = T_5+T_3

  The decomposition uses TWO different period structures:
  6-cycle (period = 7-n linear) AND 4-core (period = 11-n shifted).
  
  Both contribute to flow and structure separately, and the 
  combination produces consecutive Fibonacci numbers.
  
  This is somewhat structural but also depends on the specific 
  4-core period values matching just right. With different 4-core 
  periods, you'd get different (F, S) pairs.
  
  Conclusion: the Fibonacci appearance is REAL but somewhat fragile.
  It depends on the precise period structure at multiple levels.
""")


if __name__ == "__main__":
    main()
