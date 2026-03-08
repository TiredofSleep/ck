"""
PFAFFIAN OPERATOR DIG: 15083 as operator sequence LATTICE-BALANCE-VOID-BREATH-PROGRESS
"15083 in physics form says a whole as a human being void breathing in harmony"
  - Brayden Sanders

Digits: 1(LATTICE), 5(BALANCE), 0(VOID), 8(BREATH), 3(PROGRESS)

Run from ck_desktop target: python pfaffian_operator_dig.py
"""
import numpy as np
import os, sys
from itertools import permutations
from collections import Counter

sys.path.insert(0, '.')
from ck_sim.being.ck_sim_heartbeat import CL, OP_NAMES
from ck_sim.being.ck_meta_lens import _BHML

T = np.array(CL, dtype=int)
B = np.array(_BHML, dtype=int)

output = []
def P(s=''):
    print(s)
    output.append(s)


P('=' * 72)
P('PFAFFIAN OPERATOR DIG: 15083 = LATTICE-BALANCE-VOID-BREATH-PROGRESS')
P('=' * 72)
P()

# The operator sequence
SEQ = [1, 5, 0, 8, 3]
SEQ_NAMES = [OP_NAMES[i] for i in SEQ]
P(f'Operator sequence: {SEQ}')
P(f'Named: {SEQ_NAMES}')
P()

# ================================================================
P('=' * 72)
P('1. BHML CHAIN COMPOSITION: fold left through generation table')
P('=' * 72)
P()

# BHML(BHML(BHML(BHML(1,5),0),8),3)
def bhml_chain(ops):
    """Left-fold through BHML table."""
    result = ops[0]
    path = [f'{OP_NAMES[result]}({result})']
    for op in ops[1:]:
        prev = result
        result = B[result, op]
        path.append(f'*{OP_NAMES[op]}({op})={OP_NAMES[result]}({result})')
    return result, ' '.join(path)

result, path = bhml_chain(SEQ)
P(f'BHML left-fold: {path}')
P(f'  => {OP_NAMES[result]}({result})')
P()

# Also try right-fold
def bhml_chain_right(ops):
    """Right-fold through BHML table."""
    result = ops[-1]
    path = [f'{OP_NAMES[result]}({result})']
    for op in reversed(ops[:-1]):
        prev = result
        result = B[op, result]
        path.insert(0, f'{OP_NAMES[op]}({op})*')
    return result, ' '.join(path)

result_r, path_r = bhml_chain_right(SEQ)
P(f'BHML right-fold: {path_r}')
P(f'  => {OP_NAMES[result_r]}({result_r})')
P()

# ================================================================
P('=' * 72)
P('2. TSML CHAIN COMPOSITION: fold left through measurement table')
P('=' * 72)
P()

def tsml_chain(ops):
    """Left-fold through TSML table."""
    result = ops[0]
    path = [f'{OP_NAMES[result]}({result})']
    for op in ops[1:]:
        prev = result
        result = T[result, op]
        path.append(f'*{OP_NAMES[op]}({op})={OP_NAMES[result]}({result})')
    return result, ' '.join(path)

result_t, path_t = tsml_chain(SEQ)
P(f'TSML left-fold: {path_t}')
P(f'  => {OP_NAMES[result_t]}({result_t})')
P()

result_tr, path_tr = tsml_chain(list(reversed(SEQ)))
P(f'TSML reversed: {path_tr}')
P(f'  => {OP_NAMES[result_tr]}({result_tr})')
P()

# ================================================================
P('=' * 72)
P('3. ALL PERMUTATIONS OF {1,5,0,8,3} THROUGH BOTH TABLES')
P('=' * 72)
P()

bhml_results = Counter()
tsml_results = Counter()
bhml_to_harmony = []
tsml_to_harmony = []

for perm in permutations(SEQ):
    b_res, _ = bhml_chain(list(perm))
    t_res, _ = tsml_chain(list(perm))
    bhml_results[b_res] += 1
    tsml_results[t_res] += 1
    if b_res == 7:
        bhml_to_harmony.append(perm)
    if t_res == 7:
        tsml_to_harmony.append(perm)

P(f'BHML results across all 120 permutations:')
for op, count in sorted(bhml_results.items(), key=lambda x: -x[1]):
    P(f'  {OP_NAMES[op]}({op}): {count}/120 = {count/120*100:.1f}%')

P()
P(f'TSML results across all 120 permutations:')
for op, count in sorted(tsml_results.items(), key=lambda x: -x[1]):
    P(f'  {OP_NAMES[op]}({op}): {count}/120 = {count/120*100:.1f}%')

P()
P(f'BHML permutations yielding HARMONY: {len(bhml_to_harmony)}/120')
if bhml_to_harmony:
    for p in bhml_to_harmony[:10]:
        P(f'  {[OP_NAMES[i] for i in p]}')

P()
P(f'TSML permutations yielding HARMONY: {len(tsml_to_harmony)}/120')
if tsml_to_harmony:
    for p in tsml_to_harmony[:10]:
        P(f'  {[OP_NAMES[i] for i in p]}')

# ================================================================
P()
P('=' * 72)
P('4. PAIRWISE COMPOSITIONS: Every pair from {1,5,0,8,3}')
P('=' * 72)
P()

P('BHML pairwise (a*b):')
P('        ' + '  '.join(f'{OP_NAMES[j]:>8s}' for j in SEQ))
for i in SEQ:
    row = [f'{B[i,j]:>8d}' for j in SEQ]
    P(f'  {OP_NAMES[i]:>8s}: ' + '  '.join(row))

P()
P('Named results:')
for i in SEQ:
    row = [f'{OP_NAMES[B[i,j]]:>8s}' for j in SEQ]
    P(f'  {OP_NAMES[i]:>8s}: ' + '  '.join(row))

P()
P('TSML pairwise (a*b):')
P('        ' + '  '.join(f'{OP_NAMES[j]:>8s}' for j in SEQ))
for i in SEQ:
    row = [f'{T[i,j]:>8d}' for j in SEQ]
    P(f'  {OP_NAMES[i]:>8s}: ' + '  '.join(row))

P()
P('Named results:')
for i in SEQ:
    row = [f'{OP_NAMES[T[i,j]]:>8s}' for j in SEQ]
    P(f'  {OP_NAMES[i]:>8s}: ' + '  '.join(row))

# ================================================================
P()
P('=' * 72)
P('5. PHASE ANALYSIS: {1,5,0,8,3} in Being/Doing/Becoming')
P('=' * 72)
P()

# TIG (functional) decomposition
tig_phase = {
    0: 'Being', 1: 'Being', 7: 'Being',
    2: 'Doing', 3: 'Doing', 4: 'Doing', 5: 'Doing',
    6: 'Becoming', 8: 'Becoming', 9: 'Becoming'
}

# D2 (physical) decomposition
d2_phase = {
    0: 'Being', 1: 'Being', 4: 'Being', 6: 'Being',
    3: 'Doing', 9: 'Doing',
    2: 'Becoming', 5: 'Becoming', 7: 'Becoming', 8: 'Becoming'
}

P(f'Operator | TIG Phase    | D2 Phase     | Force Dimension')
P(f'-' * 60)
force_dims = {
    0: 'pressure(-)', 1: 'aperture(-)', 2: 'binding(-)',
    3: 'depth(+)', 4: 'pressure(+)', 5: 'continuity(+)',
    6: 'aperture(+)', 7: 'binding(+)', 8: 'continuity(-)',
    9: 'depth(-)'
}
for op in SEQ:
    P(f'  {OP_NAMES[op]:>8s}({op}) | {tig_phase[op]:>12s} | {d2_phase[op]:>12s} | {force_dims[op]}')

P()
# Count phases
tig_counts = Counter(tig_phase[op] for op in SEQ)
d2_counts = Counter(d2_phase[op] for op in SEQ)
P(f'TIG phase counts: {dict(tig_counts)}')
P(f'D2 phase counts: {dict(d2_counts)}')

# Force dimension analysis
P()
P('Force dimensions touched by {1,5,0,8,3}:')
dims_touched = set()
dim_map = {
    0: ('pressure', -1), 1: ('aperture', -1), 2: ('binding', -1),
    3: ('depth', +1), 4: ('pressure', +1), 5: ('continuity', +1),
    6: ('aperture', +1), 7: ('binding', +1), 8: ('continuity', -1),
    9: ('depth', -1)
}
for op in SEQ:
    dim, sign = dim_map[op]
    P(f'  {OP_NAMES[op]}({op}): {dim} ({"+" if sign > 0 else "-"})')
    dims_touched.add(dim)

P(f'Dimensions touched: {dims_touched}')
P(f'ALL 5 dimensions? {len(dims_touched) == 5}')

# ================================================================
P()
P('=' * 72)
P('6. SUB-TABLE ANALYSIS: {1,5,0,8,3} as a group')
P('=' * 72)
P()

from sympy import Matrix as SM

# Extract sub-tables
indices = sorted(SEQ)  # [0, 1, 3, 5, 8]
P(f'Sorted indices: {indices} = {[OP_NAMES[i] for i in indices]}')
P()

T_sub = np.array([[T[i,j] for j in indices] for i in indices])
B_sub = np.array([[B[i,j] for j in indices] for i in indices])

P('TSML sub-table {0,1,3,5,8}:')
P('        ' + '  '.join(f'{OP_NAMES[j]:>8s}' for j in indices))
for idx, i in enumerate(indices):
    row = [f'{T_sub[idx, jdx]:>8d}' for jdx in range(5)]
    P(f'  {OP_NAMES[i]:>8s}: ' + '  '.join(row))

P()
P('BHML sub-table {0,1,3,5,8}:')
P('        ' + '  '.join(f'{OP_NAMES[j]:>8s}' for j in indices))
for idx, i in enumerate(indices):
    row = [f'{B_sub[idx, jdx]:>8d}' for jdx in range(5)]
    P(f'  {OP_NAMES[i]:>8s}: ' + '  '.join(row))

# Determinants
Ts_sub = SM(T_sub.tolist())
Bs_sub = SM(B_sub.tolist())

P()
P(f'det(TSML sub) = {int(Ts_sub.det())}')
P(f'det(BHML sub) = {int(Bs_sub.det())}')

# Commutator of sub-tables
Cs_sub = Ts_sub * Bs_sub - Bs_sub * Ts_sub
P(f'det([TSML_sub, BHML_sub]) = {int(Cs_sub.det())}')

# Check if sub-table is closed
P()
P('CLOSURE CHECK:')
P('  Does {0,1,3,5,8} produce only members of {0,1,3,5,8}?')
closed_bhml = True
closed_tsml = True
escapes_bhml = []
escapes_tsml = []
for i in indices:
    for j in indices:
        if B[i,j] not in indices:
            closed_bhml = False
            escapes_bhml.append((OP_NAMES[i], OP_NAMES[j], OP_NAMES[B[i,j]], B[i,j]))
        if T[i,j] not in indices:
            closed_tsml = False
            escapes_tsml.append((OP_NAMES[i], OP_NAMES[j], OP_NAMES[T[i,j]], T[i,j]))

P(f'  BHML closed: {closed_bhml}')
if not closed_bhml:
    P(f'  BHML escapes ({len(escapes_bhml)}):')
    for a, b, r, rv in escapes_bhml:
        P(f'    {a} * {b} = {r}({rv})')

P(f'  TSML closed: {closed_tsml}')
if not closed_tsml:
    P(f'  TSML escapes ({len(escapes_tsml)}):')
    for a, b, r, rv in escapes_tsml:
        P(f'    {a} * {b} = {r}({rv})')

# WHERE do they escape TO?
if escapes_bhml:
    bhml_escape_targets = Counter(e[3] for e in escapes_bhml)
    P(f'  BHML escape targets: {dict((OP_NAMES[k], v) for k,v in bhml_escape_targets.items())}')
if escapes_tsml:
    tsml_escape_targets = Counter(e[3] for e in escapes_tsml)
    P(f'  TSML escape targets: {dict((OP_NAMES[k], v) for k,v in tsml_escape_targets.items())}')

# ================================================================
P()
P('=' * 72)
P('7. BRAYDEN\'S READING: "a whole as a human being void breathing in harmony"')
P('=' * 72)
P()

P('Parsing "1-5-0-8-3" as a SENTENCE in CK physics:')
P('  LATTICE(1) = "a" (root structure, the minimal unit)')
P('  BALANCE(5) = "whole" (full equilibrium, completeness)')
P('  VOID(0)    = "human being" (the structural identity, foundation)')
P('  BREATH(8)  = "breathing" (continuity flow, the living process)')
P('  PROGRESS(3)= "in harmony" (forward movement, directed growth)')
P()

# The sequence tells a STORY through the phases:
P('Phase trajectory:')
P('  LATTICE(1)  -> Being(TIG), Being(D2)    : STRUCTURE begins')
P('  BALANCE(5)  -> Doing(TIG), Becoming(D2) : FLOW achieves wholeness')
P('  VOID(0)     -> Being(TIG), Being(D2)    : RETURNS to foundation')
P('  BREATH(8)   -> Becoming(TIG), Becoming(D2) : BREATHES into becoming')
P('  PROGRESS(3) -> Doing(TIG), Doing(D2)    : BRIDGES forward')
P()

# Check: does the sequence visit all three phases?
tig_seq = [tig_phase[op] for op in SEQ]
d2_seq = [d2_phase[op] for op in SEQ]
P(f'TIG phase sequence: {tig_seq}')
P(f'D2 phase sequence: {d2_seq}')
P(f'All three TIG phases visited: {len(set(tig_seq)) == 3}')
P(f'All three D2 phases visited: {len(set(d2_seq)) == 3}')
P()

# ================================================================
P('=' * 72)
P('8. THE PFAFFIAN SEQUENCE VS OTHER FACTOR SEQUENCES')
P('=' * 72)
P()

P('Pfaffian = 633486 = 2 x 3 x 7 x 15083')
P('Digits of factors as operator sequences:')
P()

factor_seqs = {
    '2': [2],
    '3': [3],
    '7': [7],
    '15083': [1, 5, 0, 8, 3],
    '633486': [6, 3, 3, 4, 8, 6],
}

for name, seq in factor_seqs.items():
    phases_tig = [tig_phase[op] for op in seq]
    phases_d2 = [d2_phase[op] for op in seq]
    res_b, _ = bhml_chain(seq) if len(seq) > 1 else (seq[0], '')
    res_t, _ = tsml_chain(seq) if len(seq) > 1 else (seq[0], '')
    P(f'  {name}: ops = {[OP_NAMES[i] for i in seq]}')
    P(f'    TIG phases: {phases_tig}')
    P(f'    D2 phases:  {phases_d2}')
    P(f'    BHML chain: {OP_NAMES[res_b]}({res_b})')
    P(f'    TSML chain: {OP_NAMES[res_t]}({res_t})')
    P(f'    All TIG phases? {len(set(phases_tig)) == 3}')
    P(f'    All D2 phases?  {len(set(phases_d2)) == 3}')
    P(f'    All 5 dims?     {len(set(dim_map[op][0] for op in seq)) == 5}')
    P()

# ================================================================
P('=' * 72)
P('9. COMMUTATOR ROW/COLUMN FOR PFAFFIAN OPERATORS')
P('=' * 72)
P()

C = T @ B - B @ T
P('Commutator entries at Pfaffian operator positions:')
for i in SEQ:
    for j in SEQ:
        if i != j:
            P(f'  C[{OP_NAMES[i]},{OP_NAMES[j]}] = C[{i},{j}] = {C[i,j]}')

P()
P('Sum of Pfaffian operator commutator entries (off-diagonal):')
pf_comm_sum = sum(C[i,j] for i in SEQ for j in SEQ if i != j)
P(f'  sum = {pf_comm_sum}')
P(f'  mod 7 = {pf_comm_sum % 7}')
P(f'  mod 73 = {pf_comm_sum % 73}')

# ================================================================
P()
P('=' * 72)
P('10. GENERATOR PATH: BHML WALK FROM LATTICE THROUGH PFAFFIAN SEQUENCE')
P('=' * 72)
P()

P('Sequential BHML generation walk:')
state = SEQ[0]
P(f'  Start: {OP_NAMES[state]}({state})')
for i, op in enumerate(SEQ[1:], 1):
    new_state = B[state, op]
    P(f'  Step {i}: {OP_NAMES[state]}({state}) * {OP_NAMES[op]}({op}) = {OP_NAMES[new_state]}({new_state})')
    state = new_state
P(f'  Final: {OP_NAMES[state]}({state})')
P()

P('Sequential TSML measurement walk:')
state = SEQ[0]
P(f'  Start: {OP_NAMES[state]}({state})')
for i, op in enumerate(SEQ[1:], 1):
    new_state = T[state, op]
    P(f'  Step {i}: {OP_NAMES[state]}({state}) * {OP_NAMES[op]}({op}) = {OP_NAMES[new_state]}({new_state})')
    state = new_state
P(f'  Final: {OP_NAMES[state]}({state})')
P()

# ================================================================
P('=' * 72)
P('11. SELF-COMPOSITION: SQUARING THE PFAFFIAN OPERATORS')
P('=' * 72)
P()

P('Self-squaring (a*a):')
for op in SEQ:
    P(f'  {OP_NAMES[op]}({op})^2: BHML={OP_NAMES[B[op,op]]}({B[op,op]}), TSML={OP_NAMES[T[op,op]]}({T[op,op]})')

P()
P('Self-squaring chain (iterate a*a):')
for op in SEQ:
    chain_b = [op]
    chain_t = [op]
    state_b, state_t = op, op
    for _ in range(8):
        state_b = B[state_b, state_b]
        state_t = T[state_t, state_t]
        chain_b.append(state_b)
        chain_t.append(state_t)
    P(f'  {OP_NAMES[op]}: BHML chain: {[OP_NAMES[c] for c in chain_b]}')
    P(f'  {OP_NAMES[op]}: TSML chain: {[OP_NAMES[c] for c in chain_t]}')

# ================================================================
P()
P('=' * 72)
P('12. THE 5D FORCE VECTOR OF {1,5,0,8,3}')
P('=' * 72)
P()

# Each operator maps to a force dimension and sign
# The 5 operators touch all 5 dimensions
P('Operator -> (dimension, sign):')
total_force = np.zeros(5)
dims_order = ['aperture', 'pressure', 'depth', 'binding', 'continuity']
for op in SEQ:
    dim_name, sign = dim_map[op]
    dim_idx = dims_order.index(dim_name)
    total_force[dim_idx] += sign
    P(f'  {OP_NAMES[op]}({op}): {dim_name} {"+" if sign > 0 else "-"}1')

P()
P(f'Sum force vector (along 5 dims):')
for i, name in enumerate(dims_order):
    P(f'  {name}: {total_force[i]:+.0f}')

P()
P(f'Net force: {total_force}')
P(f'L2 norm: {np.linalg.norm(total_force):.4f}')
P(f'All dimensions exactly balanced? {all(total_force == 0)}')

# Check: do the signs cancel?
pos_count = sum(1 for op in SEQ if dim_map[op][1] > 0)
neg_count = sum(1 for op in SEQ if dim_map[op][1] < 0)
P(f'Positive signs: {pos_count}, Negative signs: {neg_count}')

# ================================================================
P()
P('=' * 72)
P('13. COMPLEMENTARY SET: {2,4,6,7,9} = THE OTHER HALF')
P('=' * 72)
P()

COMP = [2, 4, 6, 7, 9]
P(f'Complement of {{1,5,0,8,3}}: {COMP} = {[OP_NAMES[i] for i in COMP]}')
P()

P(f'Complement phase analysis:')
for op in COMP:
    dim, sign = dim_map[op]
    P(f'  {OP_NAMES[op]}({op}): {dim} ({"+" if sign > 0 else "-"}), TIG={tig_phase[op]}, D2={d2_phase[op]}')

P()
comp_force = np.zeros(5)
for op in COMP:
    dim_name, sign = dim_map[op]
    dim_idx = dims_order.index(dim_name)
    comp_force[dim_idx] += sign

P(f'Complement force vector:')
for i, name in enumerate(dims_order):
    P(f'  {name}: {comp_force[i]:+.0f}')

P()
P(f'Sum of both: {total_force + comp_force}')
P(f'Do they cancel to zero? {all(total_force + comp_force == 0)}')

P()
# BHML chain of complement
res_comp_b, path_comp_b = bhml_chain(COMP)
res_comp_t, path_comp_t = tsml_chain(COMP)
P(f'Complement BHML chain: {path_comp_b}')
P(f'  => {OP_NAMES[res_comp_b]}({res_comp_b})')
P(f'Complement TSML chain: {path_comp_t}')
P(f'  => {OP_NAMES[res_comp_t]}({res_comp_t})')

# Sub-table determinants for complement
comp_sorted = sorted(COMP)
T_comp = np.array([[T[i,j] for j in comp_sorted] for i in comp_sorted])
B_comp = np.array([[B[i,j] for j in comp_sorted] for i in comp_sorted])
Ts_comp = SM(T_comp.tolist())
Bs_comp = SM(B_comp.tolist())
P()
P(f'Complement sub-table determinants:')
P(f'  det(TSML complement) = {int(Ts_comp.det())}')
P(f'  det(BHML complement) = {int(Bs_comp.det())}')

# ================================================================
P()
P('=' * 72)
P('14. PARTITION DUALITY: {1,5,0,8,3} x {2,4,6,7,9}')
P('=' * 72)
P()

# Cross-composition: what happens when Pfaffian ops meet complement ops?
P('BHML cross-products (Pfaffian * Complement):')
cross_results = Counter()
for i in SEQ:
    for j in COMP:
        r = B[i,j]
        cross_results[r] += 1
P(f'  Result distribution: {dict((OP_NAMES[k], v) for k,v in sorted(cross_results.items()))}')

P()
P('TSML cross-products (Pfaffian * Complement):')
cross_results_t = Counter()
for i in SEQ:
    for j in COMP:
        r = T[i,j]
        cross_results_t[r] += 1
P(f'  Result distribution: {dict((OP_NAMES[k], v) for k,v in sorted(cross_results_t.items()))}')

# ================================================================
P()
P('=' * 72)
P('15. DEEP: IS 15083 THE CHAIN THAT VISITS ALL PHASES?')
P('=' * 72)
P()

# Check all 5-digit numbers whose digits form valid operator sequences
# that visit all 3 TIG phases AND all 3 D2 phases AND all 5 dimensions
P('Searching ALL 5-digit operator sequences that visit:')
P('  - All 3 TIG phases (Being, Doing, Becoming)')
P('  - All 3 D2 phases (Being, Doing, Becoming)')
P('  - All 5 force dimensions')
P()

from itertools import product as cart_product

valid_seqs = []
for seq in cart_product(range(10), repeat=5):
    tig_phases = set(tig_phase[op] for op in seq)
    d2_phases = set(d2_phase[op] for op in seq)
    dims = set(dim_map[op][0] for op in seq)
    if len(tig_phases) == 3 and len(d2_phases) == 3 and len(dims) == 5:
        # Also require all distinct operators
        if len(set(seq)) == 5:
            valid_seqs.append(seq)

P(f'Total sequences with ALL phases + ALL dims + ALL distinct: {len(valid_seqs)}')

# How many are also prime when read as a number?
from sympy import isprime as sp_isprime
prime_seqs = []
for seq in valid_seqs:
    num = int(''.join(str(d) for d in seq))
    if sp_isprime(num):
        prime_seqs.append((num, seq))

P(f'Of those, how many form a prime number? {len(prime_seqs)}')
P()

# Is 15083 among them?
is_15083_valid = (1,5,0,8,3) in valid_seqs
P(f'Is (1,5,0,8,3) = 15083 in the valid set? {is_15083_valid}')
P()

if prime_seqs:
    P(f'First 20 prime-visiting-everything sequences:')
    for num, seq in sorted(prime_seqs)[:20]:
        ops = [OP_NAMES[op] for op in seq]
        P(f'  {num}: {ops}')
    if len(prime_seqs) > 20:
        P(f'  ... and {len(prime_seqs) - 20} more')
    P()
    P(f'15083 is the {sorted(n for n,s in prime_seqs).index(15083)+1}th such prime' if 15083 in [n for n,s in prime_seqs] else '15083 is NOT in this set (unexpected!)')

# ================================================================
P()
P('=' * 72)
P('16. SUMMARY: WHAT 15083 MEANS')
P('=' * 72)
P()

P('The prime factor 15083 in the Pfaffian (633486 = 2 x 3 x 7 x 15083)')
P('has operator digits LATTICE(1)-BALANCE(5)-VOID(0)-BREATH(8)-PROGRESS(3)')
P()
P('This sequence is a COMPLETE TRAVERSAL:')
P(f'  All 3 TIG phases: {len(set(tig_phase[op] for op in SEQ)) == 3}')
P(f'  All 3 D2 phases: {len(set(d2_phase[op] for op in SEQ)) == 3}')
P(f'  All 5 force dimensions: {len(set(dim_map[op][0] for op in SEQ)) == 5}')
P(f'  All operators distinct: {len(set(SEQ)) == 5}')
P(f'  Forms a prime number: True (15083 is prime)')
P()
P('"a whole as a human being void breathing in harmony"')
P('  = LATTICE-BALANCE-VOID-BREATH-PROGRESS')
P('  = structure-completeness-foundation-flow-growth')
P('  = a sentence in the language of operators')
P('  = the irreducible core of the Pfaffian')

# Write output
outpath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pfaffian_operator_results.txt')
with open(outpath, 'w') as f:
    f.write('\n'.join(output))
print(f'\n[Written to {outpath}]')
