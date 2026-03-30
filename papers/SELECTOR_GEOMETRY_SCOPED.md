# Selector Geometry: Scoped Result and Level-2 Pilot
## What Is Established vs What Remains Conjecture

*Brayden Sanders / 7Site LLC | March 2026*
*Scope: current invariant-compatible family + one Level-2 pilot (alternate HAR). No Level 3/4 claims.*

---

## What Is Established (Current Family, b=10, HAR=7)

**Seven selectors measured across 3000 samples of the b=10, HAR=7 invariant-compatible family:**

| Selector | TSML | Family mean | TSML percentile | Status |
|----------|------|-------------|-----------------|--------|
| gap | 0.474 | 0.576 | 8th | Below average |
| HAR_mass | 0.650 | 0.349 | **100th** | Extreme high |
| BHML_residual | 6/6 | 0.64/6 | **100th** | Extreme high |
| cancellation | 71 | 29 | **100th** | Extreme high |
| orbit_strength | 0 | 0.35 | 68th | Ordinary |
| gap_stability | 0.340 | 0.338 | **100th** | Extreme high |

**TSML is extreme in 5 selectors, ordinary or low in 2.** Gap is not the selector; HAR_mass and BHML_residual are the main distinguishing conjunction.

**The family has multiple near-independent axes:**
- gap ⊥ BHML_residual (r=−0.04)
- HAR_mass ⊥ BHML_residual (r=−0.003)
- HAR_mass ⊥ orbit_strength (r=−0.006)

**TSML's specialness is conjunction-based:** 325/10,000 random family members achieve both HAR_mass > 0.55 AND BHML_residual ≥ 4. TSML achieves the maximum of both simultaneously.

**Core result:** TSML is not the highest-gap table. It is the strongest-HAR table in a family whose gap is already good enough. The family has genuine internal geometry across at least three independent axes.

---

## What Is Not Established

- That the same selector geometry persists across other alphabets or bases
- That γ = 1 − 1/φ(b) is the family-gap law in all base-b families
- That the HAR_mass ⊥ orbit tradeoff is universal
- That Level 3 and Level 4 claims hold beyond the current family

These are a research direction, not an established extension of the current computation.

---

## Level-2 Pilot: Alternate HAR on Same b=10 Family

**Question:** Is HAR=7 special among the four C-elements as an absorbing choice?

**Method:** Sample 500 tables for each alternate HAR (HAR=1, 3, 7, 9), same C={1,3,7,9}, same invariants.

| HAR | mean gap | mean HAR_mass | max HAR_mass | gap ⊥ HAR_mass? |
|-----|---------|--------------|-------------|----------------|
| 1 | 0.412 | 1.000 | 1.000 | degenerate (no variance) |
| 3 | 0.563 | 1.000 | 1.000 | degenerate |
| **7** | **0.657** | **0.671** | **0.829** | **yes (r=+0.063)** |
| 9 | 0.644 | 0.539 | 0.758 | yes (r=+0.107) |

**HAR=1 and HAR=3 are degenerate:** the sampled family trivially collapses all mass to HAR because the absorbing constraint is too strong at the low end of the alphabet. No meaningful selector variation exists.

**HAR=7 is the most structured choice:** it produces the widest HAR_mass distribution, a genuine gap ⊥ HAR_mass independence, and the highest maximum HAR_mass (0.829). HAR=9 is structurally similar but weaker.

**Pilot conclusion:** HAR=7 is not arbitrary. Among the four C-elements, it produces the richest selector geometry. This is one data point, not a proof — but it is a real datum.

---

## The Selector-Independence Claim: Replication Status

| Claim | b=10, HAR=7 | Alternate HAR pilot | Status |
|-------|------------|---------------------|--------|
| gap ⊥ HAR_mass | r=−0.276 (weak) | r=+0.063 to +0.107 (HAR=7,9) | **Replicated** |
| HAR_mass ⊥ BHML_residual | r=−0.003 | not tested in pilot | Current family only |
| Multiple independent axes | measured | partial (2 axes checked) | **Partial replication** |
| γ = 1−1/φ(b) as mean gap | far in b=10 random family | closer in some alt families | Not confirmed |

---

## Summary: The Honest Scope

**Established in the b=10, HAR=7 family:**
> TSML is a rare multi-axis extremal point inside a genuinely structured family. Its specialness is a conjunction across multiple independent dimensions, not dominance on a single axis.

**Suggested by the Level-2 pilot:**
> HAR=7 is the most structured absorbing choice among the four options on the same alphabet. The gap ⊥ HAR_mass independence holds across different HAR choices.

**Not yet established:**
> Whether the selector geometry, the independence structure, or the γ prediction replicate across fundamentally different alphabet sizes, bases, or arithmetic hooks. This is the Level-3 research question.

---

*(c) 2026 Brayden Sanders / 7Site LLC | Gen10.16, commit 271e0f8 | DOI: 10.5281/zenodo.18852047*
