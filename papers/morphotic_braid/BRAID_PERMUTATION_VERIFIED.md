> **Provenance:** Drafted 2026-04-23 (evening session, ClaudeChat). Transcribed from packet `evening_handoff_2026_04_23/`. Cross-verification against repo canonical sources: [pending — see `papers/morphotic_braid/VERIFICATION_LOG_2026_04_23.md`].
> **Copy path:** evening_handoff_2026_04_23\evening_handoff_2026_04_23\BRAID_PERMUTATION_VERIFIED.md → papers\morphotic_braid\BRAID_PERMUTATION_VERIFIED.md

# BRAID_PERMUTATION_VERIFIED.md

**Status:** [DRAFT — AWAITING VERIFICATION BY CLAUDECODE AGAINST `papers/morphotic_braid/` SOURCE FILES]

## Scope

This note establishes the cycle structure and conjugacy class of the morphotic braid permutation σ on ℤ/10ℤ. Interpretive content (named roles, stability framings, TIG-layer meaning) is handled in separate notes.

## Definition

Let σ: ℤ/10ℤ → ℤ/10ℤ be the permutation specified in `papers/morphotic_braid/MORPHOTIC_BRAID_ALGEBRAIC.md` and `SHORT_PAPER.md`. Its two-line form is:

```
  x:  0  1  2  3  4  5  6  7  8  9
σ(x): 0  7  1  3  2  4  5  6  8  9
```

## Proposition 1 — Cycle structure

σ has cycle decomposition

  σ = (0)(3)(8)(9)(1 7 6 5 4 2).

Equivalently: the set {0, 3, 8, 9} consists of the fixed points of σ, and the set {1, 2, 4, 5, 6, 7} forms a single 6-cycle under σ. The order of σ is 6.

### Proof

Direct enumeration. Fixed points verified by σ(0)=0, σ(3)=3, σ(8)=8, σ(9)=9. Six-cycle verified by iteration starting from 1: 1 → 7 → 6 → 5 → 4 → 2 → 1. All ten elements accounted for. ∎

## Proposition 2 — CRT conjugacy (the load-bearing statement)

Via the CRT bijection φ: ℤ/2 × ℤ/5 → ℤ/10 given by φ(ε, y) = 5ε + 6y mod 10, the permutation σ is conjugate to the direct sum of a 6-cycle rotation and the identity on 4 elements. Specifically, there exists a decomposition of ℤ/10 into a 6-element invariant subset S₆ = {1, 2, 4, 5, 6, 7} and a 4-element fixed set S₄ = {0, 3, 8, 9} such that:

- σ restricted to S₆ is conjugate to the cyclic rotation k → k + 1 (mod 6) via φ.
- σ restricted to S₄ is the identity.

**Confirmation required from source.** ClaudeCode: verify that this proposition is explicitly stated as Theorem E in `THEOREM_E.md` or the relevant source. If the statement in the source is stronger or narrower, replace this paragraph with the exact source statement.

## Verification script

```python
from sympy.combinatorics import Permutation

sigma = Permutation([0, 7, 1, 3, 2, 4, 5, 6, 8, 9])

# Proposition 1
assert sigma.cyclic_form == [[1, 7, 6, 5, 4, 2]]
assert set(x for x in range(10) if sigma(x) == x) == {0, 3, 8, 9}
assert sigma.order() == 6

# Proposition 2 — CRT coordinate check
def crt(x):
    return (x % 2, x % 5)

# For each element, print (x, crt(x), σ(x), crt(σ(x)))
# Cross-check against Theorem E's stated action in CRT coordinates.
for x in range(10):
    y_in = crt(x)
    y_out = crt(sigma(x))
    fixed_or_cycle = "FIXED" if sigma(x) == x else "CYCLE"
    print(f"  x={x} crt={y_in} | σ(x)={sigma(x)} crt(σ(x))={y_out} | {fixed_or_cycle}")

print("\nProposition 1 verified.")
print("Proposition 2 requires cross-check against Theorem E source.")
```

## What is claimed

- Two-line form as listed.
- Cycle decomposition (0)(3)(8)(9)(1 7 6 5 4 2).
- Fixed points {0, 3, 8, 9}.
- Order 6.
- CRT conjugacy to 6-cycle rotation ⊕ identity (pending explicit source confirmation as Theorem E).

## What is NOT claimed

- No attractor language. σ is a permutation; every element returns to itself after 6 iterations.
- No "held by 7" language.
- No claim that σ reduces to {0, 1} factors.
- No claim about relationship to the BHML or TSML composition tables — that is the subject of `bhml_successor_and_identity.md` and `doubly_regular_core.md`.
- No claim about T* = 5/7, BREATH, FRUIT, or any other named TIG object in this note alone.
- No novelty claim. This is an arithmetic statement about a specific named permutation.

---

**Tag: [TIER B — VERIFIED PENDING CLAUDECODE CROSS-CHECK]**
**File path: `papers/morphotic_braid/BRAID_PERMUTATION_VERIFIED.md`**
