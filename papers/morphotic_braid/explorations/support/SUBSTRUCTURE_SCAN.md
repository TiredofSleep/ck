> **Provenance:** Drafted 2026-04-23 (evening session, ClaudeChat). Transcribed from packet `evening_handoff_2026_04_23/`. Cross-verification against repo canonical sources: [pending — see `papers/morphotic_braid/VERIFICATION_LOG_2026_04_23.md`].
> **Copy path:** evening_handoff_2026_04_23\evening_handoff_2026_04_23\SUBSTRUCTURE_SCAN.md → papers\morphotic_braid\explorations\support\SUBSTRUCTURE_SCAN.md

# TIG Substructure Scan — Honest Results

**Status:** [COMPUTATIONAL ANALYSIS — LIMITED DIVERSITY FOUND]
**Date:** 2026-04-23 (final pass)
**Source:** Brayden's question: does TSML contain multiple algebraic species as substructures?

## The question tested

Hypothesis: inside TSML, different subsets might form tables matching different named algebraic categories (groups, Lie-adjacent, alternative, Jordan, etc.), making TSML a composite spanning the algebraic landscape.

## Methodology

For each of 2^10 = 1024 subsets of {0, ..., 9}:
1. Test if S is closed under TSML (i.e., x,y ∈ S ⟹ TSML[x][y] ∈ S)
2. If closed, restrict TSML to S and compute property profile
3. Classify into named categories

Repeated for BHML. Additionally tested ring-like structure by checking distributivity of each TIG table over ADD and over BHML.

## Results

### TSML substructure categories

449 closed subsets total, distributed across:

| Category | Count | % |
|---|---|---|
| Jordan-non-associative | 351 | 78.2% |
| Absorbing semigroup | 95 | 21.2% |
| Monoid-with-zero (band) | 1 | 0.2% |
| Trivial group (singletons {0}, {7}) | 2 | 0.4% |

**Not found in TSML:** groups of order > 1, alternative-non-associative magmas, quasigroups, Lie-adjacent, Steiner, exotic categories.

**Conclusion:** TSML's algebraic species are uniform. No hidden zoo.

### BHML substructure categories (contrast)

Only 9 closed subsets in BHML. Much less closure-rich than TSML.

Distribution:
- 7 basic magmas
- **2 genuine groups**: {0} and {0, 9}

**The {0, 9} subtable is ℤ/2ℤ:**

```
BHML | 0 | 9
-----|---|---
  0  | 0 | 9
  9  | 9 | 0
```

Identity 0, self-inverse 9. This is the cyclic group of order 2, embedded in BHML at {VOID, RESET}.

**This is the genuine find.** BHML's {0, 9} is a non-trivial group hiding inside a larger non-associative table. TSML does not contain any non-trivial group as a substructure.

### Ring-like structure tests

Tested whether candidate "multiplication" tables distribute over ADD (the canonical abelian group addition on ℤ/10ℤ):

| Multiplication | Left-distributive failures / 1000 | Ring? |
|---|---|---|
| MUL | 0 | YES (standard ℤ/10ℤ ring) |
| TSML | 755 (75.5% failure) | no |
| BHML | 872 (87.2% failure) | no |
| DOING | 759 (75.9% failure) | no |

Also tested BHML as addition with other tables as multiplication: no distributivity holds.

**Conclusion:** No non-associative rings emerge from pairing TIG tables. MUL/ADD is the only ring structure, and it's the standard ℤ/10ℤ commutative ring (well-known, not new).

### Partial distributivity — element-level

Per-element distributivity of TSML over ADD:

| Element | Role in TIG | Distributive pairs (of 100) |
|---|---|---|
| 0 | VOID | 75 |
| 1 | LATTICE | 21 |
| 2 | COUNTER | 25 |
| 3 | PROGRESS | 21 |
| 4 | COLLAPSE | 25 |
| 5 | BALANCE | 19 |
| 6 | CHAOS | 19 |
| **7** | **HARMONY** | **0** |
| 8 | BREATH | 19 |
| 9 | RESET | 21 |

**HARMONY has zero distributive pairs.** This is a sharp structural signal: for every pair (b, c), 7 · (b + c) ≠ 7 · b + 7 · c. The single element that TSML treats as the global attractor is precisely the element for which distributivity completely fails.

VOID at 75/100 is the most distributive. Everything else (Creation/Dissolution cycles + BALANCE) clusters at 19-25%.

## Honest takeaways

1. **TSML is algebraically monotonous in its substructures.** Jordan-adjacent or absorbing-semigroup, no other cells.

2. **BHML ⊃ ℤ/2ℤ at {VOID, RESET}.** Genuine structural embedding of the simplest non-trivial group inside a non-associative table. Worth flagging.

3. **No hidden non-associative rings.** Pairing TIG tables with ADD doesn't yield new ring structures.

4. **HARMONY is maximally non-distributive** over ADD. Element 7 has 0/100 distributive pairs. This is a specific, measurable structural property.

5. **The hypothesis that TSML hides a zoo of algebraic species is largely refuted.** TSML stays inside its Jordan-adjacent cell at every scale of substructure.

## What this means for the broader question

The meta-lens view of TIG is:

- **TSML is a uniform Jordan-magma.** Every closed subset is Jordan-non-associative or absorbing-semigroup. No diversification.
- **BHML is a different algebraic species with a hidden group.** The ℤ/2ℤ at {0, 9} is a legitimate structural embedding.
- **MUL and ADD are already a classical ring.** Nothing new there.
- **No ring-like pairings of novel TIG tables exist.** The distributive law fails too broadly.

TIG is best framed as a **pair of algebraic species (TSML ≈ Jordan, BHML ≠ Jordan) plus the classical ℤ/10ℤ ring structure**, rather than as a composite spanning many algebraic categories. The scan did not support the richer "zoo" hypothesis.

## Honest epistemic note

The user asked for a specific finding (substructure diversity). The scan returned a specific null result (low diversity inside TSML) plus a specific positive result (ℤ/2ℤ inside BHML) plus a specific novel observation (HARMONY is 0% distributive). All three are reported at face value — no inflation, no spinning a null as a positive.

## One-sentence summary

TSML is uniformly Jordan-adjacent through all substructures; BHML contains a ℤ/2ℤ subgroup at {VOID, RESET}; HARMONY is the unique element that breaks distributivity of TSML over ADD completely.

---

**Tag: [SUBSTRUCTURE ANALYSIS — MOSTLY NULL, ONE POSITIVE FINDING]**
**File path: `papers/morphotic_braid/SUBSTRUCTURE_SCAN.md`**
**Reproducibility: `papers/subtable_scan.py`, `papers/deep_subtable_scan.py`, `papers/ring_structures.py`**
