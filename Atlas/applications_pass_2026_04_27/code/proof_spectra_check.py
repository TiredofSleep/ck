"""
Run the proof_spectra script from 4 days ago and check what TSML it uses.
Compare against the FORMULAS §5 published table to see which is canonical.
"""

# The TSML from the proof_spectra file (4 days ago)
TSML_proof = [
    [0, 0, 0, 0, 0, 0, 0, 7, 0, 0],
    [0, 7, 3, 7, 7, 7, 7, 7, 7, 7],
    [0, 3, 7, 7, 4, 7, 7, 7, 7, 9],
    [0, 7, 7, 7, 7, 7, 7, 7, 7, 3],
    [0, 7, 4, 7, 7, 7, 7, 7, 8, 7],
    [0, 7, 7, 7, 7, 7, 7, 7, 7, 7],
    [0, 7, 7, 7, 7, 7, 7, 7, 7, 7],
    [7, 7, 7, 7, 7, 7, 7, 7, 7, 7],
    [0, 7, 7, 7, 8, 7, 7, 7, 7, 7],
    [0, 7, 9, 3, 7, 7, 7, 7, 7, 7],   # row 9: differs from FORMULAS!
]

# The TSML from FORMULAS_AND_TABLES.md §5 (what I've been using)
TSML_formulas = [
    [0,0,0,0,0,0,0,7,0,0],
    [0,7,3,7,7,7,7,7,7,7],
    [0,3,7,7,4,7,7,7,7,9],
    [0,7,7,7,7,7,7,7,7,3],
    [0,7,4,7,7,7,7,7,8,7],
    [0,7,7,7,7,7,7,7,7,7],
    [0,7,7,7,7,7,7,7,7,7],
    [7,7,7,7,7,7,7,7,7,7],
    [0,7,7,7,8,7,7,7,7,7],
    [0,7,9,7,3,7,7,7,7,7],   # row 9: differs from proof_spectra!
]

import numpy as np
T_proof = np.array(TSML_proof)
T_formulas = np.array(TSML_formulas)

print("Comparing the two versions of TSML row 9:")
print(f"  proof_spectra row 9:    {T_proof[9].tolist()}")
print(f"  FORMULAS §5 row 9:      {T_formulas[9].tolist()}")
print()

# Diffs
print("Cells where they differ:")
for i in range(10):
    for j in range(10):
        if T_proof[i,j] != T_formulas[i,j]:
            print(f"  [{i}][{j}]: proof_spectra={T_proof[i,j]}, FORMULAS={T_formulas[i,j]}")

# Check commutativity of each
print("\nCommutativity check:")
print(f"  proof_spectra TSML symmetric: {np.array_equal(T_proof, T_proof.T)}")
print(f"  FORMULAS    TSML symmetric: {np.array_equal(T_formulas, T_formulas.T)}")

# Check non-assoc rate of each
from itertools import product
def na_count(T):
    n = 10
    count = 0
    for a, b, c in product(range(n), repeat=3):
        if T[T[a,b], c] != T[a, T[b,c]]:
            count += 1
    return count

print(f"\nNon-associativity rates:")
print(f"  proof_spectra TSML: {na_count(T_proof)}/1000 = {na_count(T_proof)/10:.1f}%")
print(f"  FORMULAS    TSML: {na_count(T_formulas)}/1000 = {na_count(T_formulas)/10:.1f}%")

