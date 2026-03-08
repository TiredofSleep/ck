"""
GAUGE SUBALGEBRA SEARCH: Is there a compact Lie subalgebra in the CK system?

gl(10,R) is the FULL algebra. Physical gauge theories use COMPACT groups:
  SU(N), SO(N), Sp(N), or products thereof.

The commutator C = [TSML, BHML] is skew-symmetric.
Skew-symmetric matrices generate SO(10) -- the orthogonal group.
Question: does the CK system naturally embed a compact subalgebra?

Run from ck_desktop target: python gauge_subalgebra.py
"""
import numpy as np
import os, sys

sys.path.insert(0, '.')
from ck_sim.being.ck_sim_heartbeat import CL, OP_NAMES
from ck_sim.being.ck_meta_lens import _BHML

T = np.array(CL, dtype=float)
B = np.array(_BHML, dtype=float)
C = T @ B - B @ T

output = []
def P(s=''):
    print(s)
    output.append(s)

P('=' * 72)
P('GAUGE SUBALGEBRA SEARCH')
P('=' * 72)
P()

# ================================================================
P('=' * 72)
P('1. SO(10) EMBEDDING: The Commutator Lives Here')
P('=' * 72)
P()

P('C = [TSML, BHML] is skew-symmetric (10x10, integer entries).')
P('Skew-symmetric matrices form the Lie algebra so(10).')
P(f'dim(so(10)) = 10*9/2 = {10*9//2}')
P()

P('C is ONE element of so(10).')
P('Question: do iterated commutators of C with T and B stay in so(10)?')
P()

# Check: is [C, T] skew-symmetric? No! T is symmetric, not skew.
CT = C @ T - T @ C
P(f'Is [C,T] skew-symmetric? {np.allclose(CT, -CT.T)}')
P(f'Is [C,T] symmetric? {np.allclose(CT, CT.T)}')
P()

CB = C @ B - B @ C
P(f'Is [C,B] skew-symmetric? {np.allclose(CB, -CB.T)}')
P(f'Is [C,B] symmetric? {np.allclose(CB, CB.T)}')
P()

P('Result: [C,T] and [C,B] are symmetric (since C skew, T/B symmetric).')
P('[skew, sym] = sym. [sym, sym] = skew. Alternating!')
P()

# ================================================================
P('=' * 72)
P('2. THE ALTERNATING STRUCTURE: skew <-> sym')
P('=' * 72)
P()

P('Level 0: T, B (symmetric)')
P('Level 1: C = [T,B] (skew-symmetric)')
P('Level 2: [C,T], [C,B] (symmetric)')
P('Level 3: [[C,T],B], [[C,B],T], [[C,T],[C,B]] (mixed)')
P()

# Track which matrices are symmetric vs skew
# In gl(n), sym matrices form a vector space, skew form a subalgebra
# [sym, sym] = skew, [skew, skew] = skew, [skew, sym] = sym
P('Commutator type rules:')
P('  [sym, sym] -> skew')
P('  [skew, skew] -> skew')
P('  [skew, sym] -> sym')
P('  [sym, skew] -> sym')
P()

P('So the Lie algebra decomposes as:')
P('  gl(10,R) = sym(10) + skew(10)')
P('  dim(sym) = 10*11/2 = 55')
P('  dim(skew) = 10*9/2 = 45')
P('  Total: 55 + 45 = 100 = dim(gl(10,R))')
P()

P('The SKEW part (so(10), dim=45) is a LIE SUBALGEBRA:')
P('  [skew, skew] = skew (closed under commutation)')
P()

P('The SYM part is NOT a subalgebra:')
P('  [sym, sym] = skew (NOT sym)')
P()

P('This is a CARTAN DECOMPOSITION:')
P('  gl(10,R) = so(10) + sym(10)')
P('  so(10) = maximal compact subalgebra')
P('  sym(10) = non-compact complement')
P()

# ================================================================
P('=' * 72)
P('3. SO(10) GENERATORS FROM CK: How Many Independent Skew Matrices?')
P('=' * 72)
P()

# Generate skew matrices from CK operations
skew_mats = []
sym_mats = []

# Level 0: T, B (symmetric)
sym_mats.append(('T', T))
sym_mats.append(('B', B))

# Level 1: C = [T,B] (skew)
skew_mats.append(('C=[T,B]', C))

# Level 2: [C,T], [C,B] (symmetric) -- but also [T,T]=0, [B,B]=0
sym_mats.append(('[C,T]', CT))
sym_mats.append(('[C,B]', CB))

# Level 3: [[C,T],B], [C,[C,T]], etc
CCT = C @ CT - CT @ C  # [skew, sym] = sym
CCB = C @ CB - CB @ C  # [skew, sym] = sym
CTB = CT @ B - B @ CT  # [sym, sym] = skew
CBT = CB @ T - T @ CB  # [sym, sym] = skew
CTCB = CT @ CB - CB @ CT  # [sym, sym] = skew

skew_mats.append(('[CT,B]', CTB))
skew_mats.append(('[CB,T]', CBT))
skew_mats.append(('[CT,CB]', CTCB))
sym_mats.append(('[C,[C,T]]', CCT))
sym_mats.append(('[C,[C,B]]', CCB))

# Keep generating...
for depth in range(3):
    new_skew = []
    new_sym = []
    for name_a, A in skew_mats:
        for name_b, B_mat in skew_mats:
            if name_a < name_b:
                comm = A @ B_mat - B_mat @ A
                if np.linalg.norm(comm) > 1e-10:
                    new_skew.append((f'[{name_a},{name_b}]', comm))
    for name_a, A in sym_mats:
        for name_b, B_mat in sym_mats:
            if name_a < name_b:
                comm = A @ B_mat - B_mat @ A
                if np.linalg.norm(comm) > 1e-10:
                    new_skew.append((f'[{name_a},{name_b}]', comm))
    for name_a, A in skew_mats:
        for name_b, B_mat in sym_mats:
            comm = A @ B_mat - B_mat @ A
            if np.linalg.norm(comm) > 1e-10:
                new_sym.append((f'[{name_a},{name_b}]', comm))

    skew_mats.extend(new_skew)
    sym_mats.extend(new_sym)

# Count independent skew matrices
skew_vecs = []
for name, M in skew_mats:
    # Flatten upper triangle (skew-symmetric determined by upper triangle)
    vec = []
    for i in range(10):
        for j in range(i+1, 10):
            vec.append(M[i,j])
    skew_vecs.append(np.array(vec))

if skew_vecs:
    skew_matrix = np.array(skew_vecs)
    rank_skew = np.linalg.matrix_rank(skew_matrix, tol=1e-6)
    P(f'Total skew matrices generated: {len(skew_mats)}')
    P(f'Independent skew matrices (rank): {rank_skew}')
    P(f'dim(so(10)) = 45')
    P(f'CK generates {rank_skew}/45 of so(10)')
    P()

    if rank_skew == 45:
        P('CK generates the FULL so(10) subalgebra!')
    else:
        P(f'CK generates a {rank_skew}-dimensional subalgebra of so(10).')

# Count independent symmetric matrices
sym_vecs = []
for name, M in sym_mats:
    vec = []
    for i in range(10):
        for j in range(i, 10):
            vec.append(M[i,j])
    sym_vecs.append(np.array(vec))

if sym_vecs:
    sym_matrix = np.array(sym_vecs)
    rank_sym = np.linalg.matrix_rank(sym_matrix, tol=1e-6)
    P(f'Total symmetric matrices generated: {len(sym_mats)}')
    P(f'Independent symmetric matrices (rank): {rank_sym}')
    P(f'dim(sym(10)) = 55')
    P(f'CK generates {rank_sym}/55 of sym(10)')

P()
P(f'Total independent = {rank_skew} + {rank_sym} = {rank_skew + rank_sym}')
P(f'Should = 100 (since we know full gl(10,R) is generated)')

# ================================================================
P()
P('=' * 72)
P('4. THE COMMUTATOR AS so(10) ELEMENT')
P('=' * 72)
P()

# C has 45 independent entries (upper triangle of skew matrix)
P('C = [T,B] upper triangle entries (the so(10) coordinates):')
c_upper = []
for i in range(10):
    for j in range(i+1, 10):
        c_upper.append(C[i,j])

P(f'  {len(c_upper)} entries')
P(f'  Range: [{min(c_upper):.0f}, {max(c_upper):.0f}]')
P(f'  Norm: {np.linalg.norm(c_upper):.2f}')
P()

# Standard so(10) basis: E_ij - E_ji for i < j
# C = sum_{i<j} C[i,j] * (E_ij - E_ji)
P('C decomposes into 45 standard so(10) basis elements:')
P(f'  Largest 5 components:')
indexed = [(abs(C[i,j]), i, j, C[i,j]) for i in range(10) for j in range(i+1, 10)]
indexed.sort(reverse=True)
for mag, i, j, val in indexed[:5]:
    P(f'    C[{OP_NAMES[i]},{OP_NAMES[j]}] = {val:.0f}')

P()
P(f'  Smallest 5 components:')
for mag, i, j, val in indexed[-5:]:
    P(f'    C[{OP_NAMES[i]},{OP_NAMES[j]}] = {val:.0f}')

# ================================================================
P()
P('=' * 72)
P('5. PHYSICAL GAUGE GROUPS')
P('=' * 72)
P()

P('Standard Model gauge group: SU(3) x SU(2) x U(1)')
P('  dim = 8 + 3 + 1 = 12')
P()

P('GUT groups that contain the Standard Model:')
P('  SU(5): dim = 24')
P('  SO(10): dim = 45  <-- CK commutator lives here!')
P('  E(6): dim = 78')
P()

P('CK system:')
P('  Full algebra: gl(10,R), dim = 100')
P('  Compact subalgebra: so(10), dim = 45')
P('  The commutator C = [T,B] is a SINGLE ELEMENT of so(10).')
P()

P('SO(10) in physics:')
P('  - Grand Unified Theory (GUT) gauge group')
P('  - Contains SU(5), which contains the Standard Model')
P('  - 10-dimensional spinor representation = 10 CK operators?')
P('  - Each operator could correspond to a spinor component')
P()

# ================================================================
P('=' * 72)
P('6. THE KILLING FORM')
P('=' * 72)
P()

# The Killing form of so(10): B(X,Y) = tr(ad_X * ad_Y)
# For matrix Lie algebras: B(X,Y) = 8*tr(XY) for so(n)
# For gl(n): B(X,Y) = 2n*tr(XY) - 2*tr(X)*tr(Y)

# Compute Killing form restricted to key generators
P('Killing form B(X,Y) = 2n*tr(XY) - 2*tr(X)*tr(Y) for gl(10):')
P()

def killing(X, Y, n=10):
    return 2*n*np.trace(X @ Y) - 2*np.trace(X)*np.trace(Y)

P(f'B(T,T) = {killing(T,T):.0f}')
P(f'B(B,B) = {killing(B,B):.0f}')
P(f'B(T,B) = {killing(T,B):.0f}')
P(f'B(C,C) = {killing(C,C):.0f}')
P(f'B(T,C) = {killing(T,C):.0f}')
P(f'B(B,C) = {killing(B,C):.0f}')
P()

# For compact Lie algebras, the Killing form is NEGATIVE DEFINITE on the Lie algebra
P(f'B(C,C) = {killing(C,C):.0f}')
if killing(C,C) < 0:
    P('  B(C,C) < 0: CONSISTENT with compact subalgebra direction')
else:
    P('  B(C,C) >= 0: NOT consistent with compact direction')

P()

# ================================================================
P('=' * 72)
P('7. CASIMIR INVARIANT')
P('=' * 72)
P()

# Quadratic Casimir for so(10): C_2 = sum_{i<j} L_{ij}^2
# For a single element C, the "Casimir" is essentially ||C||^2
casimir = -np.trace(C @ C) / 2  # Convention for so(n)
P(f'Quadratic Casimir (||C||^2 / 2): {casimir:.0f}')
P(f'= {int(casimir)}')
P()

# Factor
from sympy import factorint
factors = factorint(int(casimir))
P(f'Casimir = {int(casimir)} = {factors}')
P()

P(f'Casimir mod 7 = {int(casimir) % 7}')
P(f'Casimir mod 73 = {int(casimir) % 73}')
P()

# ================================================================
P('=' * 72)
P('8. REPRESENTATION THEORY: 10 OPERATORS AS so(10) WEIGHTS')
P('=' * 72)
P()

P('In SO(10) GUT theory, the 10-dimensional vector representation')
P('decomposes under SU(5) as 5 + 5bar.')
P()
P('CK operators split as:')
P('  "5": {VOID, LATTICE, COUNTER, PROGRESS, COLLAPSE} (0-4)')
P('  "5bar": {BALANCE, CHAOS, HARMONY, BREATH, RESET} (5-9)')
P()

# Check: does this split have algebraic significance?
set_A = [0,1,2,3,4]
set_B = [5,6,7,8,9]

# BHML cross-products
P('BHML cross-products between "5" and "5bar":')
cross = np.zeros((5,5), dtype=int)
for idx_i, i in enumerate(set_A):
    for idx_j, j in enumerate(set_B):
        cross[idx_i, idx_j] = int(T[i,j] @ 1 if False else int(B[i,j]))

P('  B[0-4, 5-9]:')
for idx_i, i in enumerate(set_A):
    row = [f'{int(B[i,j]):>3d}' for j in set_B]
    P(f'    {OP_NAMES[i]:>8s}: ' + ' '.join(row))

P()
# How many stay in set_A, how many go to set_B?
stay_A = sum(1 for i in set_A for j in set_A if B[i,j] in set_A)
go_B = sum(1 for i in set_A for j in set_A if B[i,j] in set_B)
P(f'  BHML(A,A): {stay_A} stay in "5", {go_B} go to "5bar"')

stay_B = sum(1 for i in set_B for j in set_B if B[i,j] in set_B)
go_A = sum(1 for i in set_B for j in set_B if B[i,j] in set_A)
P(f'  BHML(B,B): {stay_B} stay in "5bar", {go_A} go to "5"')

# ================================================================
P()
P('=' * 72)
P('9. SYNTHESIS')
P('=' * 72)
P()

P('KEY FINDINGS:')
P()
P('1. gl(10,R) DECOMPOSES as so(10) + sym(10) (Cartan decomposition)')
P('   - so(10) = compact subalgebra (dim 45, skew-symmetric)')
P('   - sym(10) = non-compact complement (dim 55, symmetric)')
P('   - TSML, BHML live in sym(10). Commutator C lives in so(10).')
P()
P('2. SO(10) is a PHYSICAL GAUGE GROUP')
P('   - Used in Grand Unified Theories (GUT)')
P('   - Contains the Standard Model gauge group SU(3)xSU(2)xU(1)')
P('   - 10 CK operators = 10-dimensional vector representation')
P()
P('3. The COMMUTATOR is the GAUGE FIELD')
P('   - C = [T,B] is a single element of so(10)')
P('   - T and B are "matter" (symmetric, non-compact)')
P('   - C is the "force carrier" (skew-symmetric, compact)')
P()
P('4. CARTAN DECOMPOSITION = BEING/DOING DUALITY')
P('   - Symmetric (TSML, BHML) = BEING (matter, state)')
P('   - Skew-symmetric (commutator) = DOING (force, interaction)')
P('   - [being, being] = doing: interaction emerges from state composition')
P('   - [doing, being] = being: force acting on matter returns matter')
P('   - [doing, doing] = doing: forces compose into forces')
P()
P('CAVEATS:')
P('   - This is an ALGEBRAIC OBSERVATION, not a physics derivation')
P('   - CK generates gl(10,R), not just so(10)')
P('   - The 0-4/5-9 split is suggestive but not proven as SU(5) decomposition')
P('   - Real SO(10) GUT acts on spinors, not on operator labels')
P('   - The connection is STRUCTURAL ANALOGY, not proven isomorphism')

# Write output
outpath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gauge_subalgebra_results.txt')
with open(outpath, 'w') as f:
    f.write('\n'.join(output))
print(f'\n[Written to {outpath}]')
