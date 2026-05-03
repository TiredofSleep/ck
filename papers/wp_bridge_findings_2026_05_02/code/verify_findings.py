"""
verify_findings.py — One-script verification of all five findings.

Run this BEFORE integrating anything from this handoff into the repo or CK.

Returns 0 on full pass, 1 on any failure.
"""
import sys
import numpy as np
sys.path.insert(0, '.')

failures = []
warnings = []


def check(condition, name, detail=""):
    if condition:
        print(f"  [PASS] {name}")
        return True
    else:
        print(f"  [FAIL] {name}")
        if detail:
            print(f"         {detail}")
        failures.append(name)
        return False


def warn(message):
    warnings.append(message)
    print(f"  [WARN] {message}")


print("=" * 70)
print("TIG BRIDGE FINDINGS VERIFICATION")
print("=" * 70)

# Load canonical substrate
print("\n--- Loading canonical substrate ---")
try:
    from tig_substrate import TSML_10, BHML_10, SIGMA_PERMUTATION
    print("  Loaded TSML_10, BHML_10, SIGMA_PERMUTATION")
except Exception as e:
    print(f"  ERROR loading substrate: {e}")
    sys.exit(1)

# Verify substrate dimensions
check(TSML_10.shape == (10, 10), "TSML_10 is 10x10")
check(BHML_10.shape == (10, 10), "BHML_10 is 10x10")
check(len(SIGMA_PERMUTATION) == 10, "σ has 10 elements")

# Verify σ-cycle structure
sigma = SIGMA_PERMUTATION
fixed = [n for n in range(10) if int(sigma[n]) == n]
check(set(fixed) == {0, 3, 8, 9}, "σ-fixed points are {0, 3, 8, 9}",
      f"got {set(fixed)}")

# Trace σ 6-cycle starting from 1
cycle = [1]
cur = int(sigma[1])
while cur != 1 and len(cycle) < 10:
    cycle.append(cur)
    cur = int(sigma[cur])
check(set(cycle) == {1, 2, 4, 5, 6, 7}, "σ 6-cycle is {1, 2, 4, 5, 6, 7}",
      f"got {set(cycle)}")

# === FINDING 1: BHML diagonal = integer successor on {1..7} ===
print("\n--- Finding 1: BHML diagonal ---")
expected_diag = {1: 2, 2: 3, 3: 4, 4: 5, 5: 6, 6: 7, 7: 8}
for n, expected in expected_diag.items():
    actual = int(BHML_10[n, n])
    check(actual == expected, f"BHML({n},{n}) = {expected}",
          f"got {actual}")

check(int(BHML_10[8, 8]) == 7, "BHML(8,8) = 7 (return)",
      f"got {int(BHML_10[8, 8])}")
check(int(BHML_10[9, 9]) == 0, "BHML(9,9) = 0 (collapse)",
      f"got {int(BHML_10[9, 9])}")
check(int(BHML_10[0, 0]) == 0, "BHML(0,0) = 0 (VOID fixed)",
      f"got {int(BHML_10[0, 0])}")

# === FINDING 2: TSML_8 image and role distribution ===
print("\n--- Finding 2: TSML_8 image and role distribution ---")
TSML_8_INDICES = [1, 2, 3, 4, 5, 6, 8, 9]
TSML_8 = TSML_10[np.ix_(TSML_8_INDICES, TSML_8_INDICES)]

# Image
image = set()
for i in range(8):
    for j in range(8):
        image.add(int(TSML_8[i, j]))
check(image == {3, 4, 7, 8, 9}, "TSML_8 image = {3, 4, 7, 8, 9}",
      f"got {image}")

# Role distribution (94% flow expected)
FLOW = {1, 3, 5, 7, 9}
STRUCTURE = {2, 4, 8}
flow_count = 0
struct_count = 0
total = 0
for i in range(8):
    for j in range(8):
        out = int(TSML_8[i, j])
        total += 1
        if out in FLOW: flow_count += 1
        elif out in STRUCTURE: struct_count += 1

check(flow_count == 60, "TSML_8 outputs flow 60/64",
      f"got {flow_count}/64")
check(struct_count == 4, "TSML_8 outputs structure 4/64",
      f"got {struct_count}/64")

# === FINDING 3: Trefoil characterization on corrected frame ===
print("\n--- Finding 3: Trefoil characterization ---")
print("  (Running trajectory simulation, may take ~10 seconds...)")

try:
    from trefoil_corrected_frame import trajectory_corrected
    
    # Compute trefoils
    from itertools import product
    trefoils = []
    for a, b, c in product(range(10), repeat=3):
        r = trajectory_corrected(a, b, c)
        if r['crossings'] == 3:
            trefoils.append((a, b, c))
    
    check(len(trefoils) == 9, "Exactly 9 trefoils on corrected frame",
          f"got {len(trefoils)}")
    
    # Multiset analysis
    from collections import Counter
    multisets = Counter(tuple(sorted(t)) for t in trefoils)
    
    check(len(multisets) == 2, "Exactly 2 multiset classes",
          f"got {len(multisets)}: {list(multisets.keys())}")
    
    expected_multisets = {(0, 7, 8): 6, (0, 8, 8): 3}
    for ms, count in expected_multisets.items():
        actual = multisets.get(ms, 0)
        check(actual == count, f"Multiset {ms}: {count} permutations",
              f"got {actual}")
    
    # All BHML-associative?
    bhml_assoc_count = 0
    for t in trefoils:
        a, b, c = t
        left = int(BHML_10[int(BHML_10[a, b]), c])
        right = int(BHML_10[a, int(BHML_10[b, c])])
        if left == right:
            bhml_assoc_count += 1
    check(bhml_assoc_count == 9, "All 9 trefoils are BHML-associative",
          f"got {bhml_assoc_count}/9")
    
except Exception as e:
    print(f"  [ERROR] Trefoil verification failed: {e}")
    failures.append("Trefoil verification crashed")

# === FINDING 4: ±21 invariant decompositions ===
print("\n--- Finding 4: ±21 invariant decompositions ---")

# Period-based Ψ values
def bhml_self_period(n, max_iter=20):
    a = n
    seen = {a: 0}
    for k in range(1, max_iter + 1):
        a = int(BHML_10[a, n])
        if a in seen:
            return k - seen[a]
        seen[a] = k
    return None

periods = {n: bhml_self_period(n) for n in range(10)}
expected_periods = {0:1, 1:6, 2:5, 3:4, 4:3, 5:2, 6:1, 7:4, 8:3, 9:2}

for n, exp_p in expected_periods.items():
    check(periods[n] == exp_p, f"BHML period of digit {n} = {exp_p}",
          f"got {periods[n]}")

# Period→trace Ψ values: Ψ(n) = -(period(n) - 1)
psi = {n: -(periods[n] - 1) for n in range(10)}
total_psi = sum(psi.values())
check(total_psi == -21, "Sum of period-based Ψ = -21",
      f"got {total_psi}")

# Role decomposition
flow_psi = sum(psi[n] for n in FLOW)
struct_psi = sum(psi[n] for n in STRUCTURE)
check(flow_psi == -13, "Flow contribution to Ψ = -13",
      f"got {flow_psi}")
check(struct_psi == -8, "Structure contribution to Ψ = -8",
      f"got {struct_psi}")

# σ-orbit decomposition: 6-cycle + σ-fixed
six_cycle_psi = sum(psi[n] for n in [1, 2, 4, 5, 6, 7])
sigma_fixed_psi = sum(psi[n] for n in [0, 3, 8, 9])
check(six_cycle_psi == -15, "σ 6-cycle Ψ sum = -15 (= -T_5)",
      f"got {six_cycle_psi}")
check(sigma_fixed_psi == -6, "σ-fixed Ψ sum = -6 (= -T_3)",
      f"got {sigma_fixed_psi}")
check(six_cycle_psi + sigma_fixed_psi == -21,
      "σ 6-cycle + σ-fixed = -21",
      f"got {six_cycle_psi} + {sigma_fixed_psi}")

# Confirm Fibonacci structure
check((abs(flow_psi), abs(struct_psi)) == (13, 8),
      "Role decomposition: |F|=13, |S|=8 (Fibonacci F_7, F_6)",
      f"got |F|={abs(flow_psi)}, |S|={abs(struct_psi)}")

# === FINDING 5: Role magma identity ===
print("\n--- Finding 5: Role magma with VOID identity ---")

def role(n):
    if n in FLOW: return 'F'
    if n in STRUCTURE: return 'S'
    if n == 6: return 'T'
    if n == 0: return 'V'
    return '?'

# Build role magma (mode-based)
from collections import defaultdict
role_pair_outputs = defaultdict(Counter)
for a in range(10):
    for b in range(10):
        ra = role(a)
        rb = role(b)
        ro = role(int(BHML_10[a, b]))
        role_pair_outputs[(ra, rb)][ro] += 1

role_magma = {pair: counts.most_common(1)[0][0] 
              for pair, counts in role_pair_outputs.items()}

# Test V is identity
v_identity = all(role_magma.get(('V', x)) == x and 
                 role_magma.get((x, 'V')) == x
                 for x in 'VFST')
check(v_identity, "V is identity element of role magma",
      f"V row: {[role_magma.get(('V', x)) for x in 'VFST']}")

# Test commutativity
is_comm = all(role_magma.get((a, b)) == role_magma.get((b, a))
              for a in 'VFST' for b in 'VFST')
check(is_comm, "Role magma is commutative")

# Test V·V = V (only idempotent)
check(role_magma.get(('V', 'V')) == 'V', "V·V = V (idempotent)")

# Verify V/T inputs are deterministic
v_t_deterministic = True
for pair, counts in role_pair_outputs.items():
    if 'V' in pair or 'T' in pair:
        if len(counts) > 1:
            v_t_deterministic = False
            warn(f"Non-deterministic: {pair} has multiple outputs {dict(counts)}")
            break
check(v_t_deterministic, "V/T inputs make BHML role-deterministic")

# Verify F-F, F-S, S-F, S-S branch
branching_pairs = [p for p, c in role_pair_outputs.items() if len(c) > 1]
expected_branching = {('F', 'F'), ('F', 'S'), ('S', 'F'), ('S', 'S')}
check(set(branching_pairs) == expected_branching,
      "Branching pairs are exactly {F-F, F-S, S-F, S-S}",
      f"got {set(branching_pairs)}")

# === FINAL REPORT ===
print("\n" + "=" * 70)
print("VERIFICATION SUMMARY")
print("=" * 70)
print(f"\n  Failures: {len(failures)}")
for f in failures:
    print(f"    - {f}")

print(f"\n  Warnings: {len(warnings)}")
for w in warnings:
    print(f"    - {w}")

if failures:
    print("\n  ❌ VERIFICATION FAILED — DO NOT INTEGRATE")
    print("  Investigate failures before proceeding.")
    sys.exit(1)
else:
    print("\n  ✓ ALL FIVE FINDINGS VERIFIED")
    print("  Safe to proceed with integration.")
    sys.exit(0)
