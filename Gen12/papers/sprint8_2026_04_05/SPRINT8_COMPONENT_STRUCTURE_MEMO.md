# SPRINT 8: COMPONENT STRUCTURE vs SELECTOR MEMO
## What f(n) = α/β Actually Encodes

**Date:** 2026-04-05  
**Status:** Definitive structural answer reached. All claims verified.  
**Builds on:** Sprint 7 hardened selector memo

---

## FINDING IN ONE SENTENCE

f(n) = α/β is the ratio between a CRT complement-product (α, determined purely by the factorization of n) and the nearest cyclic generator of (ℤ/nℤ)* above it in the standard ordered residue model (β). It is an arithmetic positional ratio, not a dynamical, spectral, or probabilistic quantity.

---

## PART 1 — EXACT STRUCTURAL IDENTITY FOR α

**Theorem (exact):** In the standard residue model of ℤ/nℤ, α — the smallest non-trivial idempotent — equals the complement product of the prime-power factor it selects via the CRT decomposition.

Formally: write n = m₁·m₂ where gcd(m₁,m₂)=1 and α ≡ 0(mod m₁), α ≡ 1(mod m₂). Then:

$$\alpha = m_2 = \frac{n}{m_1}$$

α is the product of all prime-power factors of n **except** the one prime-power factor m₁ that α projects to zero on.

**Verified for all test moduli:**

| n | factorization | α | selected factor m₁ | α = n/m₁ |
|---|---|---|---|---|
| 6 | 2·3 | 3 | 2 = 2¹ | 6/2 = 3 ✓ |
| 10 | 2·5 | 5 | 2 = 2¹ | 10/2 = 5 ✓ |
| 12 | 4·3 | 4 | 3 = 3¹ | 12/3 = 4 ✓ |
| 18 | 2·9 | 9 | 2 = 2¹ | 18/2 = 9 ✓ |
| 20 | 4·5 | 5 | 4 = 2² | 20/4 = 5 ✓ |
| 30 | 2·3·5 | 6 | 5 = 5¹ | 30/5 = 6 ✓ |

**What α "is" structurally:** α is the unique CRT projector whose zero-projection is onto the "selected" prime-power factor m₁, and whose value is the complementary product n/m₁. The selection of m₁ (and hence the value of α) is determined by which idempotent is smallest in the standard ordering — this ordering dependency cannot be eliminated.

**Absorbing property:** α is fixed by all units in (ℤ/nℤ)* if and only if α·(u−1) ≡ 0 (mod n) for all units u. This holds exactly when n/(n,α) divides (u−1) for all units u. For n=6,10,18: α absorbs all units. For n=12,20,30: α absorbs only a subgroup of units. The absorbing property is **not** universal to all α — it depends on the arithmetic relationship between α and the unit group.

---

## PART 2 — EXACT STRUCTURAL IDENTITY FOR β

**Definition (exact):** β is the smallest max-order element of (ℤ/nℤ)* that exceeds α in value.

- The max-order elements of (ℤ/nℤ)* are the generators of that cyclic group (when (ℤ/nℤ)* is cyclic, which occurs for n = 1, 2, 4, pᵏ, 2pᵏ)
- β is the nearest such generator *above* α in the standard ordering

**Verified:**

| n | α | max-order units | generators above α | β |
|---|---|---|---|---|
| 6 | 3 | {5} (order 2) | {5} | 5 |
| 10 | 5 | {3,7} (order 4) | {7} | 7 |
| 12 | 4 | {5,7,11} (order 2) | {5,7,11} | 5 |
| 18 | 9 | {5,11} (order 6) | {11} | 11 |
| 20 | 5 | {3,7,13,17} (order 4) | {7,13,17} | 7 |
| 30 | 6 | {7,13,17,23} (order 4) | {7,13,17,23} | 7 |

---

## PART 3 — COMPONENT SEPARATION ANALYSIS

Under multiplication by all units of (ℤ/nℤ)*, the set ℤ/nℤ decomposes into invariant components. α and β always lie in **distinct** components.

| n | α's component | β's component | |α_comp| | |β_comp| | α·β mod n | = α? |
|---|---|---|---|---|---|---|
| 6 | {3} | {1,5} | 1 | 2 | 15≡3 | ✓ |
| 10 | {5} | {1,3,7,9} | 1 | 4 | 35≡5 | ✓ |
| 12 | {4,8} | {1,5,7,11} | 2 | 4 | 20≡8 | ✗ |
| 18 | {9} | {1,5,7,11,13,17} | 1 | 6 | 99≡9 | ✓ |
| 20 | {5,15} | {1,3,7,9,11,13,17,19} | 2 | 8 | 35≡15 | ✗ |
| 30 | {6,12,18,24} | {1,7,11,13,17,19,23,29} | 4 | 8 | 42≡12 | ✗ |

**Key finding on component separation:** α and β lie in distinct components for all moduli tested. This is exact and structurally guaranteed: α is an idempotent (not a unit), and β is a unit. No idempotent and unit share a multiplicative orbit in ℤ/nℤ unless the idempotent is 1.

However: the **ratio** of component sizes |α_comp|/|β_comp| does NOT equal f(n). For n=10: 1/4 ≠ 5/7. Component size ratio is a different quantity from the positional ratio α/β.

**The absorbing product:** α·β ≡ α holds for n=6,10,18 but fails for n=12,20,30. So the "absorbs β" property is not universal. It holds when α is a true fixed point of the full unit group, which requires stronger arithmetic conditions.

---

## PART 4 — WHAT f(n) ACTUALLY MEASURES

The four candidate answers, ranked:

**(a) Position — YES, trivially**

f(n) = α/β = (α/n)/(β/n) is the ratio of the normalized ordinal positions of α and β in the set {0,...,n−1}. This is exact and complete. It is trivially true by definition and says nothing beyond "f is the ratio of two residue values."

**(b) Component separation — PARTIALLY, but not cleanly**

α and β always live in distinct invariant components under unit multiplication. In that sense, f measures something about cross-component separation. But "separation" normally means a metric quantity (like distance), and the component size ratio is different from f. What f measures is not the *gap* between components but the *relative position* of their respective members.

**(c) Orbit structure — NO**

f ≠ any orbit-length ratio. Component size ratios (1/4, 1/2, etc.) do not equal f(n). f is not an orbit measure.

**(d) CRT factorization structure — THE MOST STRUCTURAL ANSWER**

α is precisely n/m₁ where m₁ is the prime-power factor that α "selects" in the CRT decomposition. β is the nearest cyclic generator of (ℤ/nℤ)* above α. Therefore:

$$f(n) = \frac{n/m_1}{\beta} = \frac{\text{CRT complement of selected factor}}{\text{nearest cyclic generator above it}}$$

This is the most structurally honest description. It expresses f as a ratio between two objects with clear ring-theoretic origins — one from the multiplicative-semigroup structure (the idempotent CRT projector), one from the unit-group structure (the cyclic generator). Their ratio is not forced to equal any particular dynamical or spectral quantity, but it is determined by the factorization of n and the ordering on its residues.

---

## PART 5 — WHAT f(n) DOES NOT ENCODE

| Quantity | f(n) = this? |
|---|---|
| Stationary probability under any natural Markov chain | **NO** — confirmed by exhaustive search (Sprint 7) |
| Eigenvalue or spectral gap of any natural operator on ℤ/nℤ | **NO** — confirmed by exhaustive search (Sprint 7) |
| Component size ratio |α_comp|/|β_comp| | **NO** — differs at all tested moduli |
| Orbit-length ratio | **NO** |
| Absorption probability | **NO** — P(α absorbs β) ≠ f uniformly |
| Carmichael exponent ratio | **NO** — S4 = α/λ(n) > 1 for most moduli |

---

## PART 6 — OPEN THEOREM (UNCHANGED, SHARPENED)

**What would turn f into a derivation of T\*:**

A theorem of the form: "For a CK-type coherence system on ℤ/nℤ, the stability threshold equals the ratio (n/m₁)/β where m₁ is the prime-power factor selected by α and β is the nearest cyclic generator of (ℤ/nℤ)* above α."

This theorem would be more structurally honest than "α/β" because it names what α and β *are* rather than just citing their values. But the core gap remains the same: no physical or dynamical definition of "stability threshold" has been connected to this ratio.

---

## PART 7 — FINAL STATEMENT

**Structural interpretation of f(n) = α/β:**

f(n) is the ratio between the CRT complement product of n's factorization (α) and the nearest cyclic generator of (ℤ/nℤ)* in the standard ordered residue model above α (β). It is an arithmetic positional ratio between a ring-theoretic idempotent and a group-theoretic generator. It is not a dynamical, spectral, or probabilistic quantity. The arithmetic ordering is essential: the selection of both α and β depends on which residue representatives are smallest in the standard ordering.
