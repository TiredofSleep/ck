# Catch 4 — W=25.2 Arithmetic Error
## Fourth Synthesis Framework Catch (March 31, 2026)

*Proof-Synthesis Ladder — Framework Operational Record*
*DOI: 10.5281/zenodo.18852047*

> This document records the fourth catch by the Proof-Synthesis framework
> in the March 2026 development session. The catch, correction, and reframe
> are all documented here. The framework's track record of operational catches
> is a primary source of evidence for the tier assignments in SYNTHESIS_TABLE.md.

---

## The Claim That Was Caught

**Source:** LutherTask3.31.26 — DERIVATION_SCAFFOLDS_GAP1.md (original version)

**Claim:** A single weight W ≈ 25.2 reproduces all five empirical gate rates at k=9:

```
R(|G|) = ((9 − |G|) / 9)^W    with W = 25.2
```

Verification table as originally presented:

| |G| | (9−|G|)/9 | ((9−|G|)/9)^25.2 | Empirical | Match? |
|----|---------|-------------------|-----------|--------|
| 1 | 8/9 ≈ 0.889 | 0.964 | 96.4% | ✓ |
| 2 | 7/9 ≈ 0.778 | 0.837 | 83.7% | ✓ |
| 3 | 6/9 ≈ 0.667 | 0.440 | 44.0% | ✓ |
| 4 | 5/9 ≈ 0.556 | 0.046 | 4.6% | ✓ |
| 5 | 4/9 ≈ 0.444 | 0.001 | 0.1% | ✓ |

**The claim: all five match.** "This is a discovery. All five empirical rates
collapse to a single real number W."

---

## The Catch

**Framework action:** Layer 2 test (Exhaustive Computation) requires numerical
verification before accepting any quantitative claim. Direct computation:

```
(8/9)^25.2 = exp(25.2 × ln(8/9)) = exp(25.2 × (−0.1178)) = exp(−2.968) ≈ 0.0514
```

**Result: 0.0514 ≠ 0.964.** Error of 18.8x at tier |G|=1.

All five tiers fail. (Only |G|=5 gives a superficially plausible result because
(4/9)^25.2 ≈ 0.000 ≈ 0.001, but this is coincidental — the exponent is too large
and pushes any base < 1 toward zero.)

The "match?" column in the original table was not computed — it was asserted.
The framework caught this by computing.

---

## The Correction

**Correct finding:** The power law R(|G|) = (n_C/k)^W is real. W is tier-specific.

```
W(|G|) = ln(R(|G|)) / ln((9 − |G|) / 9)
```

Correct per-tier W values at k=9, ω=2:

| |G| | n_C/k | W (solved) | (n_C/k)^W | Empirical | Match? |
|----|---------|------------|-----------|-----------|--------|
| 1 | 8/9 ≈ 0.889 | **0.311** | 96.4% | 96.4% | ✓ |
| 2 | 7/9 ≈ 0.778 | **0.708** | 83.7% | 83.7% | ✓ |
| 3 | 6/9 ≈ 0.667 | **2.025** | 44.0% | 44.0% | ✓ |
| 4 | 5/9 ≈ 0.556 | **5.238** | 4.6% | 4.6% | ✓ |
| 5 | 4/9 ≈ 0.444 | **8.518** | 0.1% | 0.1% | ✓ |

The formula structure is correct. The single-parameter claim is not.

---

## The Mechanistic Reframe

**Why W is tier-specific: trap density, not constraint count.**

The original framing interpreted W as an "effective constraint count" — the number
of independent constraints the MCMC must satisfy. Under this reading, W should be
a fixed geometric quantity derivable from the CRT structure, the same for all tiers.

The per-tier W values reveal a different mechanism: **W(|G|) measures trap density
in the MCMC objective landscape, not literal constraint count.**

The MCMC optimizes a combined objective: 0.50×gate + 0.25×har_col + 0.25×(1−g_stay).
The greedy chain only accepts improvements. As |G| increases:

- |G|=1,2 (W < 1): The forbidden set is small (1–2 elements). The combined
  objective is dominated by the gate term. The MCMC landscape has few traps —
  the chain almost always reaches gate=1.0. W < 1 means the success rate is
  *higher* than naive (n_C/k)^1 expectation.

- |G|=3,4,5 (W >> 1): The forbidden set grows. The g_stay term (fraction of
  G-rows mapping to G) gains weight relative to gate. The landscape develops
  local maxima where gate < 1.0 but g_stay + har_col are strong — the MCMC
  gets stuck. W >> 1 means the success rate is *lower* than naive expectation.
  At |G|=5, 99.9% of trials get trapped.

**The algebraic path to Tier D is now reframed:** Derive W(|G|) by counting
local maxima of the combined objective as a function of (n_G/n_C, objective
weights, HAR coverage). This is a combinatorial problem about the geometry of
the objective function, not a CRT fiber weight calculation.

---

## What This Changes

**Files corrected:**
- `DERIVATION_SCAFFOLDS_GAP1.md`: Single-W table replaced with per-tier table;
  Steps 4–6 revised to treat c as a tier function c(|G|), not a universal constant.
- `LUTHER_SANDERS_MANUSCRIPT.md` §3.8 and §4.4: W=25.2 claim replaced with
  per-tier values; Formula 1 updated.
- `SYNTHESIS_TABLE.md` A10: W=25.2 reference corrected to W(|G|) per-tier.
- `PROOF_SYNTHESIS_LADDER.md`: Catch 4 added to the framework operational record.

**What is preserved:**
- The power law formula R = (n_C/k)^W is confirmed valid.
- The zero-spread universality within ω-class (C6) is not affected.
- The W-discontinuity observation (A10) is not affected (just clarified to be
  between ω-class per-tier W values, not a single W).
- The CRT fiber weight structure (W = c(|G|) × ω) is still the algebraic target.

**Gap 1 after the reframe:** Derive each tier's c(|G|) = W(|G|)/2 from the
trap density of the MCMC combined objective. The structural formula is:
```
R(|G|, b, k) = (n_C(b,k)/k)^{c(|G|) × ω(b)}
```
where c(|G|) is determined by the balance of gate/har_col/g_stay weights and
the geometry of local maxima as a function of |G|/k.

---

## The Framework's Diagnosis

The Proof-Synthesis framework caught this error by applying Layer 2 (numerical
verification before promotion) to a specific numerical claim. The catch is not
a criticism of Luther's geometric intuition — the CRT fiber weight interpretation
is still the correct framing for the algebraic target. The catch corrects the
specific numerical value and forces a more honest description of what is known
(per-tier W values, empirical) versus what is conjectured (algebraic formula for W).

This is the fourth operational catch in the March 2026 session. Each catch
produced a specific diagnosis and a specific correction, neither rejecting the
underlying work nor uncritically accepting an inflated claim.

---

`© 2026 Brayden Ross Sanders / 7Site LLC & C. A. Luther · DOI: 10.5281/zenodo.18852047`
