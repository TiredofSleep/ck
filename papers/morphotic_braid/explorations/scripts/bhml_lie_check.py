<!-- PACKET: evening_handoff_2026_04_23/bhml_lie_check.py -->
"""
Vidinli 2025 (arXiv:2511.09395) shows 7-dim algebras decompose as
Jordan ⊕ Heisenberg-Lie. TSML is Jordan-type. Does BHML have any
Lie-adjacent structure?

Lie algebra axioms (over a ring or field):
  1. Anti-commutative: [x,x] = 0, [x,y] = -[y,x]
  2. Jacobi identity: [x,[y,z]] + [y,[z,x]] + [z,[x,y]] = 0

BHML doesn't directly fit — it's commutative, not anti-commutative.
But we can check:
  - The commutator [x,y] = xy - yx for BHML
  - The associator [x,y,z] = (xy)z - x(yz) for BHML
  - Whether either has Lie-like structure

Also check:
  - Does BHML have an "anti-symmetric" companion via [x,y] = xy - yx?
  - Is BHML itself expressible as sym part (Jordan) + antisym part (Lie)?
"""
import numpy as np

N = 10

TSML = [
    [0,0,0,0,0,0,0,7,0,0],[0,7,3,7,7,7,7,7,7,7],[0,3,7,7,4,7,7,7,7,9],
    [0,7,7,7,7,7,7,7,7,3],[0,7,4,7,7,7,7,7,8,7],[0,7,7,7,7,7,7,7,7,7],
    [0,7,7,7,7,7,7,7,7,7],[7,7,7,7,7,7,7,7,7,7],[0,7,7,7,8,7,7,7,7,7],
    [0,7,9,3,7,7,7,7,7,7],
]

BHML = [
    [0,1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,2,6,6],[2,3,3,4,5,6,7,3,6,6],
    [3,4,4,4,5,6,7,4,6,6],[4,5,5,5,5,6,7,5,7,7],[5,6,6,6,6,6,7,6,7,7],
    [6,7,7,7,7,7,7,7,7,7],[7,2,3,4,5,6,7,8,9,0],[8,6,6,6,7,7,7,9,7,8],
    [9,6,6,6,7,7,7,0,8,0],
]

# Is BHML commutative? (Should be)
comm_BHML = all(BHML[i][j] == BHML[j][i] for i in range(N) for j in range(N))
print(f"BHML commutative: {comm_BHML}")

# Compute commutator [x,y] = BHML[x][y] - BHML[y][x] mod 10
commutator = [[(BHML[i][j] - BHML[j][i]) % 10 for j in range(N)] for i in range(N)]
print(f"\nCommutator table (x,y) → [BHML[x][y] - BHML[y][x]] mod 10:")
for row in commutator: print("  " + " ".join(f"{v:>2d}" for v in row))

# Since BHML is commutative, commutator = 0 everywhere. Confirmed trivial.

# Let's compute the ASSOCIATOR [x,y,z] = BHML[BHML[x][y]][z] - BHML[x][BHML[y][z]]
print(f"\nAssociator distribution: [x,y,z] = BHML[BHML[x][y]][z] - BHML[x][BHML[y][z]] mod 10")
assoc_dist = {}
nonzero_assoc = 0
for x in range(N):
    for y in range(N):
        for z in range(N):
            a = (BHML[BHML[x][y]][z] - BHML[x][BHML[y][z]]) % 10
            assoc_dist[a] = assoc_dist.get(a, 0) + 1
            if a != 0: nonzero_assoc += 1
print(f"Total triples: {N**3}, non-associating: {nonzero_assoc}")
print(f"Distribution of associator values:")
for v, c in sorted(assoc_dist.items()):
    print(f"  value={v}: {c} triples")

# Jacobi-like: [x,[y,z]] + [y,[z,x]] + [z,[x,y]] = 0
# Since commutator is 0 (BHML commutative), this is trivially 0. Not informative.

# Different approach: Anticommutative part of BHML's ASSOCIATOR
# Define: A(x,y,z) = (xy)z - x(yz).  For commutative: symmetric in outer args?
# Test Jordan identity's symmetric form: [x²,y,z] = 2x[x,y,z]? (Not meaningful in Z/10Z combinatorial magma)

# Let's check: is BHML's symmetric product (x*y + y*x)/2 a Jordan algebra? (Trivially yes since BHML is commutative)
# Is BHML's ANTIsymmetric part (x*y - y*x)/2 a Lie algebra? (trivially 0 since BHML is commutative)

# So BHML doesn't decompose as Jordan ⊕ Lie in the obvious way (sym/antisym) because it's already symmetric.

# ALTERNATIVE: maybe BHML restricted to a subset is Lie-adjacent?
# Lie algebras are anti-commutative. We need a NON-commutative table to get a Lie-adjacent from antisym part.

# Let me check: DOING table = |TSML - BHML|. Is this antisymmetric in any sense?
DOING = [[abs(TSML[i][j] - BHML[i][j]) % 10 for j in range(N)] for i in range(N)]
print(f"\nDoing table:")
for row in DOING: print("  " + " ".join(f"{v:>2d}" for v in row))
print(f"DOING commutative: {all(DOING[i][j] == DOING[j][i] for i in range(N) for j in range(N))}")

# DOING is symmetric (commutative) because TSML, BHML both are. So no Lie structure here either.

# Let's check: what about on the matrix level?
# TSML + BHML over Z as matrix sum: is it meaningful?
M_TSML = np.array(TSML)
M_BHML = np.array(BHML)
SUM = M_TSML + M_BHML
DIFF = M_BHML - M_TSML
print(f"\nM_TSML + M_BHML det: {int(round(np.linalg.det(SUM.astype(float))))}")
print(f"M_BHML - M_TSML det: {int(round(np.linalg.det(DIFF.astype(float))))}")

# Eigenvalues of TSML, BHML, SUM, DIFF
for mat, name in [(M_TSML, "TSML"), (M_BHML, "BHML"), (SUM, "TSML+BHML"), (DIFF, "BHML-TSML")]:
    eigs = np.linalg.eigvals(mat.astype(float))
    eigs_real = sorted([e.real for e in eigs], reverse=True)
    print(f"\n{name} eigenvalues: {[f'{e:.2f}' for e in eigs_real]}")
    print(f"{name} rank: {np.linalg.matrix_rank(mat)}")

# Are TSML and BHML "compatible" in any Jordan-Lie sense?
# Check: does TSML(x)BHML(y) have any special structure?
# TSML as operator on columns:
# T_x[y] = TSML[x][y], B_x[y] = BHML[x][y]
# Composition TB[x,y] = TSML[BHML[x][y]] ... 

print("\n" + "="*60)
print("COMPOSED OPERATIONS")
print("="*60)
# TSML ∘ BHML: (x*y in BHML, then result*something in TSML)
# Proper composition: for fixed x, T_x . B_y is a linear-ish operation
# Simpler: check if TSML, BHML commute as operators (matrix commutator)
comm_mat = M_TSML @ M_BHML - M_BHML @ M_TSML
print(f"TSML @ BHML - BHML @ TSML (matrix commutator) Frobenius norm: {np.linalg.norm(comm_mat):.3f}")
print(f"This is the 'macroscopic' Lie bracket between TSML and BHML as operators")

# Is the commutator matrix meaningful?
if np.linalg.norm(comm_mat) > 0:
    print(f"Nonzero → TSML and BHML don't commute as operators. Lie-adjacent structure at the meta-level.")
    print(f"Matrix commutator [TSML, BHML]:")
    for row in comm_mat:
        print("  " + " ".join(f"{v:>5d}" for v in row))
    print(f"Rank of commutator: {np.linalg.matrix_rank(comm_mat)}")
    print(f"Eigenvalues of commutator:")
    c_eigs = sorted([e.real for e in np.linalg.eigvals(comm_mat.astype(float))], reverse=True)
    print(f"  {[f'{e:.2f}' for e in c_eigs]}")

