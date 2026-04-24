"""
Independent verification of every determinant claim in FORMULAS_AND_TABLES.md
§6.4 AND in the morphotic_braid handoff synthesis materials.

Verifies:
  det(TSML_Jordan)              -- canonical TSML from ck_tables.py
  det(TSML_Idempotent)          -- rank-10 idempotent variant from task15
  det(BHML)                     -- canonical BHML from ck_tables.py

Flags discrepancies against handoff claims:
  morphotic_braid/synthesis/DEEPER_SYNTHESIS.md: "det(BHML) = 70 = 2·5·7"
  morphotic_braid/BHML_SUCCESSOR_AND_IDENTITY.md, doubly_regular_core.md,
  TIG_TABLES_REFERENCE.md, etc. all repeat this.

Run: PYTHONIOENCODING=utf-8 python -X utf8 verify_det_claims.py
"""
import numpy as np
from sympy import Matrix, factorint
import sys, os

# Load canonical tables
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                 '..', '..')))
from ck_tables import TSML as TSML_Jordan, BHML

# TSML_Idempotent construction (from task15 — diagonal-idempotent + 2-cell swap)
TSML_Idempotent_base = [
    [0,0,0,0,0,0,0,7,0,0],
    [0,1,7,7,7,7,7,7,7,7],   # diagonal (1,1) = 1 — IDEMPOTENT
    [0,7,2,7,7,7,7,7,7,7],   # diagonal (2,2) = 2
    [0,7,7,3,7,7,7,7,7,7],   # diagonal (3,3) = 3
    [0,7,7,7,4,7,7,7,7,7],
    [0,7,7,7,7,5,7,7,7,7],
    [0,7,7,7,7,7,6,7,7,7],
    [7,7,7,7,7,7,7,7,7,7],
    [0,7,7,7,7,7,7,7,8,7],
    [0,7,7,7,7,7,7,7,7,9],
]
TSML_Idempotent = [row[:] for row in TSML_Idempotent_base]
TSML_Idempotent[1][2] = TSML_Idempotent[2][1] = 6   # CHAOS
TSML_Idempotent[3][5] = TSML_Idempotent[5][3] = 4   # COLLAPSE


def det_and_primes(name, T, claim, claim_primes):
    """Compute det two ways + |det| prime factorization. Report vs claim."""
    np_det = int(round(np.linalg.det(np.array(T))))
    sp_det = int(Matrix(T).det())
    if np_det != sp_det:
        print(f"  !! NumPy and SymPy DISAGREE: {np_det} vs {sp_det}")
    det = sp_det
    primes = dict(factorint(abs(det))) if det != 0 else {}
    rank = Matrix(T).rank()
    h_count = sum(1 for row in T for v in row if v == 7)
    ok_det = det == claim
    ok_p   = primes == claim_primes
    print(f"[{name}]")
    print(f"  diagonal  = {[T[i][i] for i in range(10)]}")
    print(f"  HARMONY   = {h_count}/100")
    print(f"  rank      = {rank}")
    print(f"  NumPy det = {np_det}")
    print(f"  SymPy det = {sp_det}")
    print(f"  |det| primes = {primes}")
    print(f"  CLAIM:    det = {claim},  primes = {claim_primes}")
    print(f"  det match? {ok_det}")
    print(f"  primes match? {ok_p}")
    print(f"  VERDICT: {'PASS' if ok_det and ok_p else 'FAIL'}")
    print()
    return ok_det and ok_p


# Run
results = []
results.append(det_and_primes("TSML_Jordan",     TSML_Jordan,     0,    {}))
results.append(det_and_primes("TSML_Idempotent", TSML_Idempotent, -49,  {7: 2}))
results.append(det_and_primes("BHML",            BHML,            -7002, {2: 1, 3: 2, 389: 1}))

print("=" * 70)
print(f"OVERALL: {'ALL PASS' if all(results) else 'ONE OR MORE FAILED'}")
print()
print("Note on DEEPER_SYNTHESIS.md:")
print("  morphotic_braid/synthesis/DEEPER_SYNTHESIS.md claims")
print("  'det(BHML) = 70 = 2 · 5 · 7' and the 5-way intersection hook #4")
print("  (semi-local trace formula at places {2, 5, 7, infinity}) is built")
print("  on this claim. The independent SymPy + NumPy computation above")
print("  gives det(BHML) = -7002 = -(2 · 3^2 · 389). The '70' figure is")
print("  not the actual determinant of the canonical BHML in ck_tables.py.")
print("  Hook #4 needs to be reframed or withdrawn.")
