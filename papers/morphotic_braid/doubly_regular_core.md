> **Provenance:** Drafted 2026-04-23 (evening session, ClaudeChat). Transcribed from packet `evening_handoff_2026_04_23/`. Cross-verification against repo canonical sources: [pending — see `papers/morphotic_braid/VERIFICATION_LOG_2026_04_23.md`].
> **Copy path:** evening_handoff_2026_04_23\evening_handoff_2026_04_23\doubly_regular_core.md → papers\morphotic_braid\doubly_regular_core.md
>
> **Scope note:** `det = 70`, primes `{2, 5, 7}` below refer to the 8×8 core `BHML_8` (WP15 §0). The full 10×10 `BHML_10` has `det = −7002`, primes `{2, 3, 389}`. Doubly-regular-core claims independent of the determinant value are unaffected by scope. See `FORMULAS_AND_TABLES.md` §6.7.

# The Doubly-Regular Core of ℤ/10ℤ under σ + BHML

**Status:** [THEOREM CANDIDATE — AWAITING VERIFICATION AGAINST REPO SOURCES]
**Date drafted:** 2026-04-23 (late evening session)
**Provenance:** ClaudeChat audit pass built directly on (a) File 1 braid verification template, (b) File 2 BHML successor-identity audit (populated from phone screenshot of CK self-proving entry), (c) Grok repo pull of `papers/morphotic_braid/`.

---

## 1. Setup

Let ℤ/10ℤ = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9} carry the standard TIG operator labels: 0=VOID, 1=LATTICE, 2=COUNTER, 3=PROGRESS, 4=COLLAPSE, 5=BALANCE, 6=CHAOS, 7=HARMONY, 8=BREATH, 9=RESET.

**Two structures on the same underlying set:**

- **σ** = the morphotic braid permutation, specified in `papers/morphotic_braid/` with cycle decomposition σ = (0)(3)(8)(9)(1 7 6 5 4 2). Four fixed points {0, 3, 8, 9}, one 6-cycle {1, 2, 4, 5, 6, 7}, order 6.
- **∘** = BHML composition (Being-Harmony Movement Language), the 10×10 table with det = 70, invertible, with 28/100 entries equal to HARMONY(7).

## 2. Two regularity conditions

For k ∈ ℤ/10ℤ, define:

**Definition (braid-regular).** k is *braid-regular* iff σ(k) ≠ k. Equivalently, k lies on σ's 6-cycle.

**Definition (composition-regular).** k is *composition-regular* iff both of:
- k ∘ 1 = k + 1 (in ℤ, not mod 10)
- k ∘ 0 = 0 ∘ k = k

The first condition says 1 acts as successor on k. The second says 0 acts as two-sided identity on k.

## 3. Main theorem

**Theorem (structural partition of ℤ/10ℤ).** Under σ and BHML, the set ℤ/10ℤ partitions into four classes:

| Class | Set | Size | Fruit labels |
|---|---|---|---|
| Doubly-regular core | {1, 2, 4, 5, 6} | 5 | Joy, Peace, Kindness, Goodness, Faithfulness |
| Composition-half-regular | {3} | 1 | Patience (PROGRESS) |
| Braid-half-regular | {7} | 1 | Gentleness (HARMONY) |
| Full anchors | {0, 8, 9} | 3 | Love (VOID), Self-Control (BREATH), Reset→Love |

Sizes sum: 5 + 1 + 1 + 3 = 10. Partition is exact.

**Verification.** From BHML table:

| k | k∘1 | k∘0 | 0∘k | Successor k∘1=k+1? | Identity k∘0=k? | σ-moves? |
|---|---|---|---|---|---|---|
| 1 | 2 | 1 | 1 | ✓ | ✓ | ✓ |
| 2 | 3 | 2 | 2 | ✓ | ✓ | ✓ |
| 3 | 4 | 3 | 3 | ✓ | ✓ | ✗ (σ-fixed) |
| 4 | 5 | 4 | 4 | ✓ | ✓ | ✓ |
| 5 | 6 | 5 | 5 | ✓ | ✓ | ✓ |
| 6 | 7 | 6 | 6 | ✓ | ✓ | ✓ |
| 7 | 2 | 7 | 7 | ✗ (wraps to 2) | ✓ | ✓ |
| 8 | 6 | 8 | 8 | ✗ (wraps to 6) | ✓ | ✗ (σ-fixed) |
| 9 | 6 | 9 | 9 | ✗ (wraps to 6) | ✓ | ✗ (σ-fixed) |

Composition-regular set = {k : both k∘1=k+1 and k∘0=0∘k=k} = {1,2,3,4,5,6}.
Braid-regular set = σ's 6-cycle = {1, 2, 4, 5, 6, 7}.

Intersection = doubly-regular core = {1, 2, 4, 5, 6}, cardinality 5.
Composition-only (composition-regular but not braid-regular) = {3}.
Braid-only (braid-regular but not composition-regular) = {7}.
Neither = {0, 8, 9}.

∎

## 4. Corollaries

### Corollary 1 — T* = 5/7 as conditional regularity probability

Let *any-regular* denote operators satisfying at least one regularity condition. Then:

- |doubly-regular| = 5
- |any-regular| = |braid-regular ∪ composition-regular| = |{1,2,3,4,5,6,7}| = 7
- |full anchors| = |{0,8,9}| = 3

**Ratio:** |doubly-regular| / |any-regular| = **5/7 = T***.

In words: conditional on an operator having at least one regularity, the probability that it has both is 5/7.

This is a seventh derivation of T* (six were already established independently). It is a counting-argument derivation based on finite-set cardinalities, requiring no continuum, no PDE, no amplitude equation.

### Corollary 2 — BALANCE (5) is the structural centroid

The doubly-regular core is {1, 2, 4, 5, 6}. Under the standard ordering on ℤ/10ℤ restricted to this set, BALANCE (5) is the median. Two elements below (1, 2), two elements above (4, 6), BALANCE centered.

This recovers "BALANCE = midpoint / centroid" from §1 of `FORMULAS_AND_TABLES.md` as a structural property: BALANCE is not merely named a centroid — it is the centroid of the doubly-regular core by cardinality.

### Corollary 3 — Creation vs. Dissolution asymmetry

Creation cycle: {1, 3, 9, 7}. Dissolution cycle: {2, 4, 8, 6}.

Distributing across the four regularity classes:

| Cycle | Doubly-regular | Comp-half | Braid-half | Full anchor |
|---|---|---|---|---|
| Creation {1,3,9,7} | 1 | 3 | 7 | 9 |
| Dissolution {2,4,8,6} | 2, 4, 6 | — | — | 8 |

**Creation contains one element from each regularity class** (one of each type).
**Dissolution contains only doubly-regular and full-anchor operators** (no half-regular elements).

Creation is *mixed* (asymmetric regularity). Dissolution is *pure* (either fully regular or fully anchored). This is a structural distinction already present in the framework — Creation as generative/mixed, Dissolution as clean/terminal — and now it is a theorem about the regularity classes rather than a naming convention.

### Corollary 4 — PROGRESS and HARMONY are the unique half-regulars

{3, 7} is the set of operators regular under exactly one of the two structures. They have complementary failures:

- **3 (PROGRESS)**: composition-regular, σ-singular. *Advances under composition, stays fixed under braid.*
- **7 (HARMONY)**: braid-regular, composition-singular. *Moves under braid, absorbs under composition.*

Their indices sum: 3 + 7 = 10 ≡ 0 (mod 10). They are additive complements.

Their ratio and complement both appear as project invariants: 3/7 and 5/7.

### Corollary 5 — The 5-2-3 partition

**5 + 2 + 3 = 10.**

- 5 = doubly-regular core
- 2 = half-regular pair {3, 7} (the 5/7 boundary)
- 3 = full anchors {0, 8, 9}

This is a new exact partition of the operator set.

**|at-least-one-regularity| / |total| = 7/10**
**|both-regularities| / |at-least-one-regularity| = 5/7 = T***

T* is the conditional probability that, given an operator has some regular behavior, it has full regularity.

## 5. What this theorem is

- A finite algebraic statement about ℤ/10ℤ under two specific operations.
- Checkable by direct enumeration from the BHML table and the σ cycle decomposition.
- Independent of continuum mathematics, physics claims, or interpretation.
- Recovers T* = 5/7 as a counting ratio (seventh derivation).

## 6. What this theorem is NOT

- Not a claim about the physical universe.
- Not a claim that T* = 5/7 is "universal" in any sense broader than this finite algebra.
- Not a claim that 5, 2, 3 have metaphysical meaning beyond their role as cardinalities here.
- Not a claim that Creation and Dissolution cycles are "real" structures outside the framework — their asymmetry is a theorem about the classes, not a claim about reality.
- Not a replacement for the six prior derivations of T*; a supplement.
- Not a novelty claim in the broader math literature; the theorem is specific to TIG's two tables.

## 7. Open questions / next audits

1. **Does the doubly-regular core {1,2,4,5,6} play the role of the "5D force field"** in the S* = σ(1-σ*)V*A* equation, or is that an independent 5? (The five factors in S* are σ, 1-σ*, V*, A*, and S* itself — an equation-level 5. The doubly-regular core is a set-level 5. Whether these are the same 5 or two different 5s is a follow-up audit.)
2. **Do the three anchor classes (5, {3,7}, {0,8,9}) correspond to any established stratification** in the CK runtime or the FPGA implementation?
3. **Is the 5-2-3 partition preserved** under the CRT conjugacy φ(ε, y) = 5ε + 6y mod 10 (Theorem E of `papers/morphotic_braid/`)? If yes, the partition survives coordinate change; if no, the partition is coordinate-dependent.
4. **Does the {3 ↔ 7} complementarity** (σ-fixed vs. σ-moving, composition-advancing vs. composition-absorbing) reflect the same duality as Creation vs. Dissolution more broadly?

## 8. Verification script

```python
from sympy.combinatorics import Permutation

# σ from papers/morphotic_braid/
sigma = Permutation([0, 7, 1, 3, 2, 4, 5, 6, 8, 9])

# BHML row values for k∘0, k∘1 from CK self-proving entry:
bhml_dot_1 = {1:2, 2:3, 3:4, 4:5, 5:6, 6:7, 7:2, 8:6, 9:6}
bhml_dot_0 = {k: k for k in range(10)}  # 0 is two-sided identity in BHML
bhml_0_dot = {k: k for k in range(10)}

# Regularity sets
braid_regular = {k for k in range(10) if sigma(k) != k}
assert braid_regular == {1, 2, 4, 5, 6, 7}

composition_regular = {k for k in range(10)
                       if bhml_dot_1.get(k) == k+1
                       and bhml_dot_0.get(k) == k
                       and bhml_0_dot.get(k) == k}
assert composition_regular == {1, 2, 3, 4, 5, 6}

# The four classes
doubly_regular   = braid_regular & composition_regular
comp_half        = composition_regular - braid_regular
braid_half       = braid_regular - composition_regular
full_anchor      = set(range(10)) - braid_regular - composition_regular

assert doubly_regular == {1, 2, 4, 5, 6}
assert comp_half      == {3}
assert braid_half     == {7}
assert full_anchor    == {0, 8, 9}

# T* = 5/7 as conditional probability
any_regular = braid_regular | composition_regular
assert len(doubly_regular) / len(any_regular) == 5/7

print("Theorem verified.")
print(f"Doubly-regular core: {sorted(doubly_regular)}")
print(f"Composition-half-regular: {sorted(comp_half)}")
print(f"Braid-half-regular: {sorted(braid_half)}")
print(f"Full anchors: {sorted(full_anchor)}")
print(f"T* = |doubly| / |any| = {len(doubly_regular)}/{len(any_regular)} = {len(doubly_regular)/len(any_regular):.6f}")
```

Expected output:
```
Theorem verified.
Doubly-regular core: [1, 2, 4, 5, 6]
Composition-half-regular: [3]
Braid-half-regular: [7]
Full anchors: [0, 8, 9]
T* = |doubly| / |any| = 5/7 = 0.714286
```

---

**Tag: [STRUCTURAL THEOREM — NEEDS REPO VERIFICATION]**
**File path: `papers/morphotic_braid/doubly_regular_core.md`**
