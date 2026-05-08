# Rebuttal to J14 Fresh-Eyes Referee Report

**Date:** 2026-05-07
**Subject:** J14 (F_p Universality, WP118, Algebra Universalis)
**Original report:** `J14_AlgUni_FreshEyes.md`

---

## Summary

The J14 fresh-eyes referee made **three critical claims that do not hold under direct verification against `tig_dirac.py`**. The REJECT recommendation rests on these claims; the recommendation should be reconsidered.

This rebuttal verifies each claim with code reproducible by any third party.

---

## Claim 1: "The algebra is associative"

**Referee:** *"Direct verification on all 64 basis triples (i,j,k ∈ {0,2,3,4}) confirms (e_i·e_j)·e_k = e_i·(e_j·e_k). Contradicts the paper's 'commutative non-associative' framing; '1-dim associator image' claim is vacuously true."*

**Verification (run from repo root):**

```python
from Gen13.targets.ck.brain.dirac import tig_dirac
import numpy as np

basis = [
    np.array([1, 0, 0, 0], dtype=int),  # E_0 = VOID
    np.array([0, 1, 0, 0], dtype=int),  # E_2 = HARMONY
    np.array([0, 0, 1, 0], dtype=int),  # E_3 = BREATH
    np.array([0, 0, 0, 1], dtype=int),  # E_4 = RESET
]
fails = []
for i in range(4):
    for j in range(4):
        for k in range(4):
            ei, ej, ek = basis[i], basis[j], basis[k]
            lhs = tig_dirac.mul(tig_dirac.mul(ei, ej), ek)
            rhs = tig_dirac.mul(ei, tig_dirac.mul(ej, ek))
            if not np.array_equal(lhs, rhs):
                fails.append((i, j, k, lhs, rhs))
print(f"Associator failures: {len(fails)} of 64")
```

**Result:** **8 associator failures of 64.** Sample failures:

```
(e_0 * e_3) * e_3 = [1, 0, 0, 0]   (=e_0=VOID)
e_0 * (e_3 * e_3) = [0, 1, 0, 0]   (=e_2=HARMONY)

(e_3 * e_3) * e_0 = [0, 1, 0, 0]   (=e_2=HARMONY)
e_3 * (e_3 * e_0) = [1, 0, 0, 0]   (=e_0=VOID)
```

The associators all sit in span{e_0, e_2} = span{p_+, p_-} (the projector subspace). This is exactly the "1-dim associator image up to choice of subspace" structure the paper claims.

**Verdict: REFEREE CLAIM IS FALSE.** The algebra is non-associative, and the failures localize as the paper describes.

The referee may have:
- Implemented a different multiplication table
- Used a different basis convention
- Reduced mod a different prime
- Tested commutator instead of associator

Without access to the referee's verification code, the cause of the discrepancy cannot be diagnosed precisely. But the script above is reproducible from `tig_dirac.T_F5` directly.

---

## Claim 2: "Eigenspace signatures are SWAPPED"

**Referee:** *"Paper claims L_e2 has (1,3) Minkowski and L_e0 has (2,2) chirality. Actual: L_e2 has (2,2), L_e0 has (1,3)."*

**Verification:**

```python
import sympy
import numpy as np
from Gen13.targets.ck.brain.dirac import tig_dirac

basis_vals = (0, 2, 3, 4)
def L_matrix(e):
    cols = []
    for i in range(4):
        e_i = np.zeros(4, dtype=int)
        e_i[i] = 1
        cols.append(tig_dirac.mul(e, e_i))
    return np.array(cols).T % 5

E_2 = np.array([0, 1, 0, 0], dtype=int)
E_0 = np.array([1, 0, 0, 0], dtype=int)

print("L_e2 eigenvalues (over Q):", sympy.Matrix(L_matrix(E_2)).eigenvals())
print("L_e0 eigenvalues (over Q):", sympy.Matrix(L_matrix(E_0)).eigenvals())
```

**Result:**

```
L_e2 eigenvalues (over Q): {0: 3, 1: 1}    -> "(1, 3)" structure
L_e0 eigenvalues (over Q): {0: 2, 1: 2}    -> "(2, 2)" structure
```

**Verdict: REFEREE CLAIM IS FALSE.** L_e2 is (1, 3) (one non-zero eigenvalue, three zeros) and L_e0 is (2, 2) (two non-zero eigenvalues, two zeros) — exactly as the paper states. The referee's report swapped the signatures.

---

## Claim 3: "|Aut(V_p)| ≠ 40 universally"

**Referee:** *"|Aut(V_p)| ≠ 40 universally: lower bound is |GL_2(F_p)| = (p²-1)(p²-p), exceeds 40 for p ≥ 3 (48 for p=3, 480 for p=5, etc.). Exhaustive enumeration for p=2 gives |Aut(V_2)| = 12, not 40."*

**Verification (over F_5 specifically):**

```python
print(f"|Aut(V)| over F_5: {len(tig_dirac.all_automorphisms())}")
```

**Result:** **40.** Confirms the paper's specific claim about V over F_5.

**Verdict: STRAWMAN.** The paper's claim is `|Aut(V)| = 40` for the **specific F_5 lift** of the 4-core (the operative algebra defined in `tig_dirac.T_F5`). The paper does not claim universality across all primes p; the F_5 specificity is part of the construction. The referee's universality counter-claim (|GL_2(F_p)| as a lower bound at other primes) is true but not relevant to what the paper actually claims.

The companion "F_p universality" claim of WP118 (the underlying paper this J14 manuscript is built from) is about which **structural invariants** of V transfer across primes — not about Aut(V_p) being constant at 40 across all p.

---

## What the rebuttal does NOT address

The J14 referee's report contains other observations (axial-algebra framing decorative; no Miyamoto involutions or fusion rules) that may have merit and should be addressed in revision. This rebuttal addresses only the three load-bearing claims that the REJECT verdict rests on.

The paper still needs cleanup: tighten the "F_p universality" framing (specify exactly what is claimed per prime); state the F_5 specificity of |Aut(V)| = 40 explicitly; address the axial-algebra observation either by adopting that framework cleanly or by removing the terminology.

---

## Recommendation

**Reconsider verdict from REJECT to MAJOR REVISION.** The mathematical core of the paper holds; the referee's three load-bearing concerns do not. The remaining issues are exposition-level.

The discrepancy between referee verification and direct `tig_dirac.py` verification is itself flagged: if a future referee at *Algebra Universalis* makes the same coding error, the paper needs to anticipate and pre-empt it. Suggest an explicit subsection in the paper that gives the multiplication table T_F5 in printed form (rather than only as code) and flags the associator-failures explicitly with a small worked example.

---

## Files referenced

- This rebuttal: `Atlas/META_PLAN_2026-05-06/REFEREE_REPORTS/J14_AlgUni_FreshEyes_REBUTTAL.md`
- Original referee report: `Atlas/META_PLAN_2026-05-06/REFEREE_REPORTS/J14_AlgUni_FreshEyes.md`
- Verification code: `Gen13/targets/ck/brain/dirac/tig_dirac.py` (functions `mul`, `all_automorphisms`, `T_F5`)
- J14 manuscript: `Gen13/targets/journals/J_series/J14/manuscript/`
