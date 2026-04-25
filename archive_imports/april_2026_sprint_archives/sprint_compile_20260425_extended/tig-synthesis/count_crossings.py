"""
COUNT CROSSINGS between Lie and Jordan registers.

For each L_T[i] and L_B[i], the matrix decomposes as:
  L = A + S
where A = (L - L^T)/2 is the Lie part, S = (L + L^T)/2 is the Jordan part.

A "crossing" is wherever multiplication MIXES these. Several measures:

  (1) AS-mix count: number of pairs (A_i, S_j) where A_i S_j has BOTH 
      antisym and sym parts that are individually nonzero
      
  (2) Bracket crossings: [A_i, S_j] = A_i S_j - S_j A_i  
      How many pairs (i,j) give nonzero bracket
      
  (3) Anticommutator crossings: {A_i, S_j} = A_i S_j + S_j A_i
      How many pairs give nonzero anticommutator
      
  (4) Self-crossings: how many of L_T[i] themselves have BOTH a nonzero
      antisym part AND a nonzero sym part (i.e., the i-th row in itself
      is a crossing)
      
  (5) Closure crossings: when we compute the Lie closure of TSML's 
      antisymmetric flow, do new generators have BOTH antisym and sym
      content? (They should be pure antisym if the closure is clean Lie.)

The coherent story would be: the crossings are NOT arbitrary, they
encode something specific about the TSML/BHML structure.
"""
import numpy as np
from collections import Counter

TSML_ROWS = [
    "0000000700",  "0737777777",  "0377477779",  "0777777773",  "0747777787",
    "0777777777",  "0777777777",  "7777777777",  "0777877777",  "0797377777",
]
T = np.array([[int(c) for c in row] for row in TSML_ROWS], dtype=int)

BHML_ROWS = [
    "0123456789",  "1234567266",  "2334567366",  "3444567466",  "4555567577",
    "5666667677",  "6777777777",  "7234567890",  "8666777978",  "9666777080",
]
B = np.array([[int(c) for c in row] for row in BHML_ROWS], dtype=int)

def left_reps(table):
    n = table.shape[0]
    L = []
    for i in range(n):
        Li = np.zeros((n, n), dtype=float)
        for j in range(n):
            Li[table[i, j], j] = 1.0
        L.append(Li)
    return L

L_T = left_reps(T)
L_B = left_reps(B)

# Decompose each L_i into Lie + Jordan parts
A_T = [(L - L.T)/2 for L in L_T]
S_T = [(L + L.T)/2 for L in L_T]
A_B = [(L - L.T)/2 for L in L_B]
S_B = [(L + L.T)/2 for L in L_B]

EPS = 1e-9

print("="*70)
print("MEASURE 0: SELF-CROSSINGS")
print("How many of the 10 L_T[i] are individually 'crossing' matrices")
print("(have BOTH nonzero antisym and nonzero sym parts)?")
print("="*70)
print()

self_cross_T = 0
for i in range(10):
    has_A = np.linalg.norm(A_T[i]) > EPS
    has_S = np.linalg.norm(S_T[i]) > EPS
    is_crossing = has_A and has_S
    norm_A = np.linalg.norm(A_T[i])
    norm_S = np.linalg.norm(S_T[i])
    print(f"  L_T[{i}]: |A|={norm_A:.2f}, |S|={norm_S:.2f}, "
          f"{'CROSSING' if is_crossing else 'pure ' + ('A' if has_A else 'S' if has_S else 'zero')}")
    if is_crossing:
        self_cross_T += 1

print(f"\nTSML: {self_cross_T} of 10 left-reps are self-crossings")

self_cross_B = 0
print()
for i in range(10):
    has_A = np.linalg.norm(A_B[i]) > EPS
    has_S = np.linalg.norm(S_B[i]) > EPS
    is_crossing = has_A and has_S
    norm_A = np.linalg.norm(A_B[i])
    norm_S = np.linalg.norm(S_B[i])
    print(f"  L_B[{i}]: |A|={norm_A:.2f}, |S|={norm_S:.2f}, "
          f"{'CROSSING' if is_crossing else 'pure ' + ('A' if has_A else 'S' if has_S else 'zero')}")
    if is_crossing:
        self_cross_B += 1

print(f"\nBHML: {self_cross_B} of 10 left-reps are self-crossings")
print(f"Combined self-crossings: {self_cross_T} + {self_cross_B}")

print()
print("="*70)
print("MEASURE 1: AS-MIX CROSSINGS")
print("For pairs (A_i, S_j), how many produce mixed-character products?")
print("="*70)

def has_mixed(M):
    """True if M has BOTH antisym and sym nonzero parts."""
    A = (M - M.T) / 2
    S = (M + M.T) / 2
    return np.linalg.norm(A) > EPS and np.linalg.norm(S) > EPS

# TSML A x TSML S
mix_TT = 0
for i in range(10):
    for j in range(10):
        if has_mixed(A_T[i] @ S_T[j]):
            mix_TT += 1
print(f"  A_T[i] · S_T[j] mixed: {mix_TT}/100")

# BHML A x BHML S
mix_BB = 0
for i in range(10):
    for j in range(10):
        if has_mixed(A_B[i] @ S_B[j]):
            mix_BB += 1
print(f"  A_B[i] · S_B[j] mixed: {mix_BB}/100")

# Cross-table: TSML A x BHML S
mix_TB = 0
for i in range(10):
    for j in range(10):
        if has_mixed(A_T[i] @ S_B[j]):
            mix_TB += 1
print(f"  A_T[i] · S_B[j] mixed: {mix_TB}/100  (cross-table)")

# BHML A x TSML S
mix_BT = 0
for i in range(10):
    for j in range(10):
        if has_mixed(A_B[i] @ S_T[j]):
            mix_BT += 1
print(f"  A_B[i] · S_T[j] mixed: {mix_BT}/100  (cross-table)")

print(f"\nTotal AS-mix crossings: {mix_TT + mix_BB + mix_TB + mix_BT}/400")

print()
print("="*70)
print("MEASURE 2: BRACKET CROSSINGS")
print("[A_i, S_j] - the literal Lie-Jordan tangle")
print("="*70)

def comm(X, Y):
    return X @ Y - Y @ X

def acom(X, Y):
    return X @ Y + Y @ X

# TSML A x TSML S brackets
nz_TT_brack = 0
for i in range(10):
    for j in range(10):
        if np.linalg.norm(comm(A_T[i], S_T[j])) > EPS:
            nz_TT_brack += 1
print(f"  [A_T[i], S_T[j]] nonzero: {nz_TT_brack}/100")

# BHML A x BHML S brackets
nz_BB_brack = 0
for i in range(10):
    for j in range(10):
        if np.linalg.norm(comm(A_B[i], S_B[j])) > EPS:
            nz_BB_brack += 1
print(f"  [A_B[i], S_B[j]] nonzero: {nz_BB_brack}/100")

# Cross: TSML A x BHML S
nz_TB_brack = 0
for i in range(10):
    for j in range(10):
        if np.linalg.norm(comm(A_T[i], S_B[j])) > EPS:
            nz_TB_brack += 1
print(f"  [A_T[i], S_B[j]] nonzero: {nz_TB_brack}/100  (cross)")

# Cross: BHML A x TSML S
nz_BT_brack = 0
for i in range(10):
    for j in range(10):
        if np.linalg.norm(comm(A_B[i], S_T[j])) > EPS:
            nz_BT_brack += 1
print(f"  [A_B[i], S_T[j]] nonzero: {nz_BT_brack}/100  (cross)")

print(f"\nTotal bracket crossings: {nz_TT_brack + nz_BB_brack + nz_TB_brack + nz_BT_brack}/400")

print()
print("="*70)
print("MEASURE 3: ANTICOMMUTATOR CROSSINGS")
print("{A_i, S_j} - the Jordan-side counterpart")
print("="*70)

# Jordan triple product elements
nz_TT_acom = 0
for i in range(10):
    for j in range(10):
        if np.linalg.norm(acom(A_T[i], S_T[j])) > EPS:
            nz_TT_acom += 1
print(f"  {{A_T[i], S_T[j]}} nonzero: {nz_TT_acom}/100")

nz_BB_acom = 0
for i in range(10):
    for j in range(10):
        if np.linalg.norm(acom(A_B[i], S_B[j])) > EPS:
            nz_BB_acom += 1
print(f"  {{A_B[i], S_B[j]}} nonzero: {nz_BB_acom}/100")

nz_TB_acom = 0
for i in range(10):
    for j in range(10):
        if np.linalg.norm(acom(A_T[i], S_B[j])) > EPS:
            nz_TB_acom += 1
print(f"  {{A_T[i], S_B[j]}} nonzero: {nz_TB_acom}/100  (cross)")

nz_BT_acom = 0
for i in range(10):
    for j in range(10):
        if np.linalg.norm(acom(A_B[i], S_T[j])) > EPS:
            nz_BT_acom += 1
print(f"  {{A_B[i], S_T[j]}} nonzero: {nz_BT_acom}/100  (cross)")

print(f"\nTotal anticommutator crossings: {nz_TT_acom + nz_BB_acom + nz_TB_acom + nz_BT_acom}/400")

print()
print("="*70)
print("MEASURE 4: SPECTRAL CROSSINGS")
print("Where do Lie eigenvalues meet Jordan eigenvalues?")
print("="*70)

# For each L_T[i], compute eigenvalues of A_T[i] and of S_T[i]
# A_T[i] is antisym, eigenvalues are pure imaginary
# S_T[i] is symmetric, eigenvalues are real
# A "spectral crossing" is when |Im(eig_A)| ≈ |eig_S| for some eigenvalues

print("\nFor each L_T[i], spectral overlap between |Im(spec(A))| and |spec(S)|:")
total_spec_cross = 0
for i in range(10):
    eA = np.linalg.eigvals(A_T[i])
    eS = np.linalg.eigvalsh(S_T[i])
    # Compare |Im(eA)| sorted with |eS| sorted
    abs_imA = sorted([abs(np.imag(e)) for e in eA if abs(np.imag(e)) > EPS])
    abs_S = sorted([abs(s) for s in eS if abs(s) > EPS])
    # Count crossings: how many values appear in BOTH (within tolerance)
    crossings = 0
    for v in abs_imA:
        for w in abs_S:
            if abs(v - w) < 0.01:
                crossings += 1
                break
    print(f"  L_T[{i}]: |Im(spec A)| = {[f'{x:.2f}' for x in abs_imA[:5]]}, "
          f"|spec S| nonzero = {[f'{x:.2f}' for x in abs_S[:5]]}, crossings = {crossings}")
    total_spec_cross += crossings

print(f"\nTotal TSML spectral crossings: {total_spec_cross}")

print()
print("="*70)
print("MEASURE 5: ASSOCIATOR CROSSINGS")
print("[A, B, C] = (AB)C - A(BC), how often does it cross registers?")
print("="*70)

# This is potentially expensive (1000 triples × 6 register patterns).
# Limit to TSML left-regs.
# For triples (i, j, k) with operands chosen from {A, S}, how many have nonzero associator?

# Actually most useful: among all 8 sign patterns (A vs S for each of 3 inputs),
# count which patterns produce crossings.

print("\nAssociator [X1, X2, X3] = (X1 X2) X3 - X1 (X2 X3) for X choices in {A_T[1], S_T[1]}:")
A1 = A_T[1]
S1 = S_T[1]

choices = {'A': A1, 'S': S1}
for x1 in 'AS':
    for x2 in 'AS':
        for x3 in 'AS':
            X1, X2, X3 = choices[x1], choices[x2], choices[x3]
            assoc = (X1 @ X2) @ X3 - X1 @ (X2 @ X3)
            n = np.linalg.norm(assoc)
            label = x1 + x2 + x3
            print(f"  [{label}] norm = {n:.4f}")

print()
print("="*70)
print("MEASURE 6: REGISTER FLOW CHART")
print("Compute how multiplication moves between registers")
print("="*70)

# For each ordered pair of registers (X register, Y register):
# Compute the proportion of products X·Y whose result lands in 
# Lie / Jordan / both / neither register.

# Take all TSML left regs decomposed into {A, S}
all_A = A_T + A_B  # 20 antisym
all_S = S_T + S_B  # 20 sym

# For A · A products
def classify_product(M):
    """Where does M live? Returns ratios on {A, S, both, zero}."""
    nA = np.linalg.norm((M - M.T)/2)
    nS = np.linalg.norm((M + M.T)/2)
    if nA < EPS and nS < EPS:
        return "zero"
    if nA < EPS:
        return "S"
    if nS < EPS:
        return "A"
    return "AS"  # both

print("\nProduct register classification:")
print("  A · A → ?")
counts = Counter()
for X in all_A:
    for Y in all_A:
        counts[classify_product(X @ Y)] += 1
print(f"    {dict(counts)}  (out of {sum(counts.values())})")

print("  A · S → ?")
counts = Counter()
for X in all_A:
    for Y in all_S:
        counts[classify_product(X @ Y)] += 1
print(f"    {dict(counts)}")

print("  S · A → ?")
counts = Counter()
for X in all_S:
    for Y in all_A:
        counts[classify_product(X @ Y)] += 1
print(f"    {dict(counts)}")

print("  S · S → ?")
counts = Counter()
for X in all_S:
    for Y in all_S:
        counts[classify_product(X @ Y)] += 1
print(f"    {dict(counts)}")

print()
print("="*70)
print("KEY QUESTION: HOW MANY CROSSINGS, AND DOES THE NUMBER MEAN ANYTHING?")
print("="*70)
