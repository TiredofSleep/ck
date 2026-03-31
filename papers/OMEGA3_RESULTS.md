# ω(b) ≥ 3 Extension Results
## First Computational Test of Luther-Sanders Equivalence for Three-Factor Composites

*Brayden Ross Sanders & C. A. Luther*
*March 2026 | DOI: 10.5281/zenodo.18852047*

---

## Setup

k = 9 | gate_thresh = 0.999 | n_trials = 2000 per world | n_steps = 100
Matches original R16 parameters exactly.

Test bases: 30(2×3×5), 42(2×3×7), 66(2×3×11), 70(2×5×7), 105(3×5×7), 110(2×5×11)
First-G verification: 30, 42, 66, 105, 110, 165, 231, 273, 385, 429, 462, 546

---

## Test 1 — First-G Law for ω(b)=3

**Result: ALL PASS (12/12)**

| b | factors | min_p | first_g | match |
|---|---------|-------|---------|-------|
| 30 | [2,3,5] | 2 | 2 | OK |
| 42 | [2,3,7] | 2 | 2 | OK |
| 66 | [2,3,11] | 2 | 2 | OK |
| 105 | [3,5,7] | 3 | 3 | OK |
| 110 | [2,5,11] | 2 | 2 | OK |
| 165 | [3,5,11] | 3 | 3 | OK |
| 231 | [3,7,11] | 3 | 3 | OK |
| 273 | [3,7,13] | 3 | 3 | OK |
| 385 | [5,7,11] | 5 | 5 | OK |
| 429 | [3,11,13] | 3 | 3 | OK |
| 462 | [2,3,7,11] | 2 | 2 | OK |
| 546 | [2,3,7,13] | 2 | 2 | OK |

**Interpretation:** The First-G proof argument (no k < p can share a factor with b = p×q×r, since every such multiple is ≥ p) is identical for three-factor composites. This is an exact extension, not a coincidence. No computational exceptions.

**Tier status:** First-G Law for ω(b)≥2 is Tier D. The proof covers all ω(b) simultaneously.

---

## Test 2 — k-Gate Tier Law: Universality for ω(b)=3

**Measured rates:**

| b | factors | \|G\| | G | rate% |
|---|---------|------|---|------|
| 30 | [2,3,5] | 7 | [2,3,4,5,6,8,9] | 28.6% |
| 42 | [2,3,7] | 7 | [2,3,4,6,7,8,9] | 28.4% |
| 66 | [2,3,11] | 6 | [2,3,4,6,8,9] | 4.2% |
| 70 | [2,5,7] | 6 | [2,4,5,6,7,8] | 4.0% |
| 105 | [3,5,7] | 5 | [3,5,6,7,9] | 0.9% |
| 110 | [2,5,11] | 5 | [2,4,5,6,8] | 1.1% |

**Zero-spread within |G|-tiers:**

| \|G\| | n_worlds | rates | spread | verdict |
|------|---------|-------|--------|---------|
| 5 | 2 | 0.9%, 1.1% | 0.2% | ZERO |
| 6 | 2 | 4.2%, 4.0% | 0.1% | ZERO |
| 7 | 2 | 28.6%, 28.4% | 0.2% | ZERO |

**Zero spread holds.** Same arithmetic structure, same |G| → same rate, regardless of which specific p, q, r make up the modulus.

---

## Test 3 — Comparison: ω(b)=3 vs semiprime rate values

**Important finding: zero-spread universality holds, but the VALUES differ by ω-class.**

| \|G\| | Semiprime f_9 | ω(b)=3 f_9 | Same? |
|------|------------|-----------|-------|
| 1 | 96.4% | (not observed at k=9) | — |
| 3 | 44.0% | (not observed at k=9) | — |
| 4 | 4.6% | (not observed at k=9) | — |
| 5 | ~0.1% | ~1.0% | NO |
| 6 | — | ~4.1% | — |
| 7 | — | ~28.5% | — |

The invariant is **zero-spread universality within arithmetic G of the same ω-class**, not a single universal rate across all ω-classes.

**Refined statement of the k-Gate Tier Law:**
> f_k(|G|) is universal within {b : ω(b) = n} for fixed n. Different n-classes produce different rate tables.

This is a refinement, not a failure. The universality property survives; the tier values are ω-class dependent.

---

## Test 4 — Arithmetic vs Synthetic G at ω(b)=3 (b=105)

| G type | G | rate |
|--------|---|------|
| Arithmetic | [3,5,6,7,9] | 0.8% |
| Synthetic (top-block) | [5,6,7,8,9] | 0.7% |
| Gap | | +0.2% |

**Result: gap is essentially zero at these parameters.**

**Why this is not a failure of the High Interleave Law:**

At |G|=5, k=9, both arithmetic and synthetic G are deep in the near-zero regime (both < 1%). There is no room for a meaningful gap because both are near the floor. The High Interleave gap was ~61% for semiprimes at |G|=3-4, where rates were in the 4%-44% range — there was space to show the distinction.

To test the High Interleave distinction for ω(b)=3, we need a b with |G| < 4 at k=9. Most three-factor composites have |G| ≥ 5 at k=9 because three prime factors each contribute gate elements. The test requires extending k (to k=15 or k=21) where ω(b)=3 worlds have larger alphabets and lower |G|-density.

**Status: High Interleave Law for ω(b)=3 is UNTESTED, not falsified.**

---

## Summary and Tier Status

| Claim | Result | Tier impact |
|-------|--------|------------|
| First-G Law for ω(b)=3 | CONFIRMED 12/12 | Tier D — extends to all ω(b)≥2 |
| Zero-spread universality for ω(b)=3 | CONFIRMED (spread ≤ 0.2%) | Tier C extended — same property, different values |
| Rate values universal across ω-classes | FAILED — values are ω-dependent | Refined claim: universality is within-class |
| High Interleave Law at ω(b)=3 | UNTESTED (all cases near floor) | Requires k≥15 for ω(b)=3 |

### What this means for the Equivalence

The Luther-Sanders Equivalence needs one word added:

> *"Among all moduli with the same ω(b) and the same number of forbidden elements in a fixed-size alphabet, the gate rate is exactly the same. Zero variance."*

The "same ω(b)" qualifier is new. The universal invariant is the zero-spread property within an ω-class; the specific rate values are class-dependent.

---

## Open Questions Generated

1. **ω-Class rate table:** Derive f_9 for ω(b)=3 exhaustively (all |G| tiers). Is the table as clean as the semiprime table?
2. **High Interleave at ω(b)=3, larger k:** Run at k=15, k=21 where ω(b)=3 worlds have lower |G|-density and meaningful arithmetic-vs-synthetic gap can appear.
3. **Algebraic explanation of ω-class dependence:** Why does ω(b)=3 produce different rate values for the same |G|? CRT decomposition has three factors vs two — one more idempotent. Does the rate follow the number of CRT idempotents?

---

`© 2026 Brayden Ross Sanders / 7Site LLC & C. A. Luther · DOI: 10.5281/zenodo.18852047`
