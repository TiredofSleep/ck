"""
Verify WP104's main claims:
1. P_56 acts as outer automorphism in spinor rep of so(10)
2. BHML σ_outer-breaking is 100% in the 54 irrep
3. Doubly-invariant subalgebra under D_4 = <P_56, σ^3> is 16-dim
4. Killing form spectrum on g_0 is (-4)^15 ⊕ (0)^1
5. The 9-vector direction has BREATH=RESET=0, ||v||^2 = 13/4
6. 26 σ_outer-asymmetric BHML cells
7. TSML non-associativity is 12.6% (126/1000)

Also check the κ_Ξ claim: |VEV|² = 13/4 → m²_Ξ = κ_Ξ·e → κ_Ξ = 13/(4e)
This requires the assumption m²_Ξ = |VEV|².
"""
import numpy as np
from itertools import product

# Tables from WP104 §1.1 / FORMULAS §5,6
TSML = np.array([
    [0,0,0,0,0,0,0,7,0,0],
    [0,7,3,7,7,7,7,7,7,7],
    [0,3,7,7,4,7,7,7,7,9],
    [0,7,7,7,7,7,7,7,7,3],
    [0,7,4,7,7,7,7,7,8,7],
    [0,7,7,7,7,7,7,7,7,7],
    [0,7,7,7,7,7,7,7,7,7],
    [7,7,7,7,7,7,7,7,7,7],
    [0,7,7,7,8,7,7,7,7,7],
    [0,7,9,7,3,7,7,7,7,7],
])

BHML = np.array([
    [0,1,2,3,4,5,6,7,8,9],
    [1,2,3,4,5,6,7,2,6,6],
    [2,3,3,4,5,6,7,3,6,6],
    [3,4,4,4,5,6,7,4,6,6],
    [4,5,5,5,5,6,7,5,7,7],
    [5,6,6,6,6,6,7,6,7,7],
    [6,7,7,7,7,7,7,7,7,7],
    [7,2,3,4,5,6,7,8,9,0],
    [8,6,6,6,7,7,7,9,7,8],
    [9,6,6,6,7,7,7,0,8,0],
])

print("="*70)
print("CLAIM 7: TSML non-associativity is 12.6% (126/1000)")
print("="*70)
nonassoc = 0
for a, b, c in product(range(10), repeat=3):
    left = TSML[TSML[a,b], c]
    right = TSML[a, TSML[b,c]]
    if left != right:
        nonassoc += 1
print(f"Non-associative triples: {nonassoc}/1000 = {nonassoc/1000:.3f}")
print(f"Match WP104 claim: {nonassoc == 126}")

# Check the structural claims about the 126
involves_7_in_bracket = 0
distinct_LR = set()
void_in_middle = 0
for a, b, c in product(range(10), repeat=3):
    left = TSML[TSML[a,b], c]
    right = TSML[a, TSML[b,c]]
    if left != right:
        if left == 7 or right == 7:
            involves_7_in_bracket += 1
        distinct_LR.add(frozenset([left, right]))
        if b == 0:
            void_in_middle += 1

print(f"Triples where one bracketing = HARMONY: {involves_7_in_bracket}/126")
print(f"Distinct {{L,R}} pairs: {distinct_LR}")
print(f"Triples with b=VOID (middle): {void_in_middle}")

print("\n" + "="*70)
print("CLAIM 6: 26 σ_outer-asymmetric BHML cells")
print("="*70)
# σ_outer = P_56 acting on indices: swap 5 and 6
# A cell (i,j) is σ_outer-symmetric if BHML[i,j] is preserved under σ on rows AND cols.
# Asymmetric cells: BHML[σ(i), σ(j)] ≠ σ(BHML[i,j])
# σ_outer is just the (5 6) transposition.
def sigma_outer(x):
    if x == 5: return 6
    if x == 6: return 5
    return x

asymmetric_cells = 0
for i in range(10):
    for j in range(10):
        if BHML[sigma_outer(i), sigma_outer(j)] != sigma_outer(BHML[i,j]):
            asymmetric_cells += 1
print(f"σ_outer-asymmetric cells: {asymmetric_cells}")
print(f"Match WP104 claim of 26: {asymmetric_cells == 26}")

# Try alternate interpretation: cells where row-i has different values at cols 5,6
print("\nAlternate: rows where BHML[i,5] != BHML[i,6]:")
for i in range(10):
    sym = BHML[i,5] == BHML[i,6]
    print(f"  Row {i}: BHML[{i},5]={BHML[i,5]}, BHML[{i},6]={BHML[i,6]}, symmetric={sym}")

print("\n" + "="*70)
print("CLAIM 1: P_56 spinor and chirality flip")
print("="*70)

# Build Cl(0,10) gamma matrices via Pauli tensor products
# Standard construction: 32-dim spinor space, 10 gamma matrices
def kron(*ms):
    res = ms[0]
    for m in ms[1:]:
        res = np.kron(res, m)
    return res

I2 = np.eye(2, dtype=complex)
sx = np.array([[0,1],[1,0]], dtype=complex)
sy = np.array([[0,-1j],[1j,0]], dtype=complex)
sz = np.array([[1,0],[0,-1]], dtype=complex)

# Standard 5-fold tensor construction for Cl(0,10) with signature (+,+,+,...,+)
# Use γ_{2k-1} and γ_{2k} for k=1..5 in pairs.
gammas = []
for k in range(5):
    # γ_{2k} = σ_x ⊗ σ_z^k... build via standard recursion
    pass

# Use known construction: γ_a for a=1..10, all squaring to +I, anticommuting
# Construction: 5 pairs, each (X, Y) on a tensor factor, sandwiched with Z's
gammas = []
for k in range(5):
    factors_x = []
    factors_y = []
    for j in range(5):
        if j < k:
            factors_x.append(sz)
            factors_y.append(sz)
        elif j == k:
            factors_x.append(sx)
            factors_y.append(sy)
        else:
            factors_x.append(I2)
            factors_y.append(I2)
    gammas.append(kron(*factors_x))
    gammas.append(kron(*factors_y))

# Now γ[0..9] are the 10 gamma matrices. Verify {γ_a, γ_b} = 2 δ_ab I
all_anticomm = True
for a in range(10):
    for b in range(10):
        anticomm = gammas[a] @ gammas[b] + gammas[b] @ gammas[a]
        expected = 2*np.eye(32, dtype=complex) if a == b else np.zeros((32,32), dtype=complex)
        if not np.allclose(anticomm, expected, atol=1e-12):
            all_anticomm = False
            break
print(f"All 100 anticommutation relations satisfied: {all_anticomm}")

# Volume element ω = γ_1 γ_2 ... γ_10
omega = np.eye(32, dtype=complex)
for g in gammas:
    omega = omega @ g
omega_sq = omega @ omega
print(f"ω² = -I: {np.allclose(omega_sq, -np.eye(32, dtype=complex), atol=1e-12)}")

# P_56^spin = (γ_5 - γ_6) / sqrt(2)  -- but in WP104 notation γ_5 means index 5 (0-based)
# WP104 uses indices 1..10 for gammas. Their γ_5 corresponds to my gammas[4], γ_6 to gammas[5]
# Let me use 1-based for clarity.
# So P_56 swaps indices 5,6 in the so(10) action; spinor lift is (γ_5 - γ_6)/√2
P56 = (gammas[4] - gammas[5]) / np.sqrt(2)
P56_sq = P56 @ P56
print(f"(γ_5 - γ_6)² = 2I: {np.allclose(gammas[4]@gammas[4] - gammas[4]@gammas[5] - gammas[5]@gammas[4] + gammas[5]@gammas[5], 2*np.eye(32, dtype=complex), atol=1e-12)}")
print(f"P56^2 = I: {np.allclose(P56_sq, np.eye(32, dtype=complex), atol=1e-12)}")

# Anticommute with omega?
ac_omega = P56 @ omega + omega @ P56
print(f"P56 anticommutes with ω: {np.allclose(ac_omega, np.zeros((32,32), dtype=complex), atol=1e-12)}")

# Conjugation action: P56 γ_a P56 should send γ_5 → γ_6, γ_6 → γ_5
P56_inv = P56  # since P56^2 = I
g5_conj = P56 @ gammas[4] @ P56_inv
print(f"P56 γ_5 P56 = γ_6: {np.allclose(g5_conj, gammas[5], atol=1e-12)}")
g6_conj = P56 @ gammas[5] @ P56_inv
print(f"P56 γ_6 P56 = γ_5: {np.allclose(g6_conj, gammas[4], atol=1e-12)}")
g1_conj = P56 @ gammas[0] @ P56_inv
print(f"P56 γ_1 P56 = γ_1: {np.allclose(g1_conj, gammas[0], atol=1e-12)}")

# Chirality projectors: P_± = (I ± iω)/2
I32 = np.eye(32, dtype=complex)
P_plus = (I32 + 1j*omega) / 2
P_minus = (I32 - 1j*omega) / 2
# Check projector property
print(f"P_+ projector: {np.allclose(P_plus @ P_plus, P_plus, atol=1e-12)}")
print(f"P_- projector: {np.allclose(P_minus @ P_minus, P_minus, atol=1e-12)}")
print(f"P_+ + P_- = I: {np.allclose(P_plus + P_minus, I32, atol=1e-12)}")

# Chirality flip: P56 should send chirality+ entirely to chirality-
# i.e., P_minus @ P56 @ P_plus has full action, but P_plus @ P56 @ P_plus = 0
flip_plus_to_plus = P_plus @ P56 @ P_plus
flip_plus_to_minus = P_minus @ P56 @ P_plus
print(f"Chirality flip: ||P_+ P56 P_+|| = {np.linalg.norm(flip_plus_to_plus):.3e}")
print(f"               ||P_- P56 P_+|| = {np.linalg.norm(flip_plus_to_minus):.3e}")
print(f"Confirms chirality flip: {np.linalg.norm(flip_plus_to_plus) < 1e-12}")
