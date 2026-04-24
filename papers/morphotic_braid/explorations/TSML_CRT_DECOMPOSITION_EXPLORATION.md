> **Provenance:** Drafted 2026-04-23 (evening session, ClaudeChat). Transcribed from packet `evening_handoff_2026_04_23/`. Cross-verification against repo canonical sources: [pending — see `papers/morphotic_braid/VERIFICATION_LOG_2026_04_23.md`].
> **Copy path:** evening_handoff_2026_04_23\evening_handoff_2026_04_23\TSML_CRT_DECOMPOSITION_EXPLORATION.md → papers\morphotic_braid\explorations\TSML_CRT_DECOMPOSITION_EXPLORATION.md

# TSML_CRT_DECOMPOSITION_EXPLORATION.md

**Status:** [EXPLORATION — OPEN QUESTION, AUDIT NEEDED]
**Date:** 2026-04-23
**Source:** Brayden's intuition, late-session handoff: "transforming TSML and BHML into a complementary structure using ℤ/2 × ℤ/5 as a TSML simplification"

## The question

Can TSML be most honestly described as a structure on ℤ/2 × ℤ/5 rather than on ℤ/10ℤ directly?

Three possible readings:
1. **Direct product:** TSML = (rule on ℤ/2) × (rule on ℤ/5), with the two components independent.
2. **Twisted product:** TSML = rule on ℤ/2 × ℤ/5 where the y-component depends on the ε-component (or vice versa).
3. **Primary ℤ/5 structure:** TSML lives primarily on ℤ/5 with ℤ/2 carrying only a Creation/Dissolution parity modifier.

## Setup

Via CRT: ℤ/10 ≅ ℤ/2 × ℤ/5 by x ↦ (x mod 2, x mod 5).

Operator labels in CRT coordinates:

| x | CRT | Cycle | σ-class |
|---|---|---|---|
| 0 = VOID | (0, 0) | — | fixed |
| 1 = LATTICE | (1, 1) | Creation | cycle |
| 2 = COUNTER | (0, 2) | Dissolution | cycle |
| 3 = PROGRESS | (1, 3) | Creation | fixed |
| 4 = COLLAPSE | (0, 4) | Dissolution | cycle |
| 5 = BALANCE | (1, 0) | center | cycle |
| 6 = CHAOS | (0, 1) | center | cycle |
| 7 = HARMONY | (1, 2) | Creation | cycle |
| 8 = BREATH | (0, 3) | Dissolution | fixed |
| 9 = RESET | (1, 4) | Creation | fixed |

Creation cycle {1, 3, 9, 7} in CRT: {(1,1), (1,3), (1,4), (1,2)} — all ε=1, y ∈ {1, 2, 3, 4}. **Creation = the ε=1 fiber with y ≠ 0.**

Dissolution cycle {2, 4, 8, 6} in CRT: {(0,2), (0,4), (0,3), (0,1)} — all ε=0, y ∈ {1, 2, 3, 4}. **Dissolution = the ε=0 fiber with y ≠ 0.**

0 and 5 have y = 0: VOID = (0,0), BALANCE = (1,0). **The y = 0 fiber is {VOID, BALANCE} — the neither-Creation-nor-Dissolution pair.**

**First observation:** The ε coordinate carries Creation vs. Dissolution exactly. Creation is ε = 1; Dissolution is ε = 0 (with both excluding the y = 0 pair). This is a clean structural result independent of TSML or BHML.

## Testing Reading 1 (direct product)

For TSML to factor as a direct product, TSML[a][b] must be computable as (f(a_ε, b_ε), g(a_y, b_y)) for some independent f: ℤ/2 × ℤ/2 → ℤ/2 and g: ℤ/5 × ℤ/5 → ℤ/5.

Harmony-dominance test: TSML has ~73% of entries equal to 7 = (1, 2). If TSML factors directly:
- Wherever TSML[a][b] = 7, we need f(a_ε, b_ε) = 1 AND g(a_y, b_y) = 2.
- The first condition alone constrains ε-components: f(a_ε, b_ε) = 1 must occur in ~73% of cells.

But f: ℤ/2 × ℤ/2 → ℤ/2 takes only four inputs and two outputs. At most 4 of the 4 input pairs can map to 1; at least 0 can. If f is constant-1, then f(a_ε, b_ε) = 1 always — compatible with 100% of cells having ε = 1 in the output. That works for the ε-component.

The g-component test is harder. If g: ℤ/5 × ℤ/5 → ℤ/5 is fixed, and we require g(a_y, b_y) = 2 for ~73% of cells, then g must have one output (2) that dominates its 25-cell table to 73%. Possible in principle — g could be mostly 2 with a few exceptions.

**Audit needed:** does there exist a pair (f, g) such that TSML[φ(ε₁,y₁)][φ(ε₂,y₂)] = φ(f(ε₁,ε₂), g(y₁,y₂)) for all 100 cells of TSML?

If yes: **Reading 1 holds**, and TSML factors as a direct product. This would be a significant simplification.

If no: try Reading 2.

## Testing Reading 2 (twisted product)

Here the y-component rule can depend on both ε coordinates:
TSML[φ(ε₁,y₁)][φ(ε₂,y₂)] = φ(f(ε₁,ε₂), g_{ε₁,ε₂}(y₁, y₂))

Four possible g's (one for each (ε₁, ε₂) pair). This is more flexible and more likely to hold.

**Audit needed:** extract TSML cells, compute their CRT coordinates, check whether the y-output depends only on (y₁, y₂) for each fixed (ε₁, ε₂).

## Testing Reading 3 (primary ℤ/5, ε as parity)

TSML[φ(ε₁,y₁)][φ(ε₂,y₂)] = φ(h(ε₁, ε₂, y₁, y₂), g(y₁, y₂))

where g depends only on the y-coordinates and the ε-output is computed separately (possibly as a function of all four inputs). This lets the ε carry the Creation/Dissolution distinction while the primary arithmetic lives in ℤ/5.

**Audit needed:** check whether the y-component of TSML outputs depends only on (y₁, y₂), independent of (ε₁, ε₂).

## What would make this a real result

If any of Readings 1/2/3 holds, TSML's 100-cell table reduces to:
- Reading 1: a 4-cell ε-rule + a 25-cell y-rule = 29 cells total
- Reading 2: a 4-cell ε-rule + four 25-cell y-rules = 104 cells (MORE, not less — but with structural clarity)
- Reading 3: a 25-cell y-rule + a 100-cell ε-rule = 125 cells (also more, but clean)

Reading 1 is the only one that's a pure cell-count reduction. Readings 2 and 3 are structural reorganizations, not compressions. All three are potentially valuable; only Reading 1 is a simplification in the strict sense.

## Why this matters

If Reading 1 holds, TSML is revealed as the *product* of two simpler structures, not a bespoke 10×10 table. That would:
- Explain TSML's harmony-dominance as a product-of-dominances (ε-rule mostly ε=1, y-rule mostly y=2)
- Suggest BHML may have the same structure (independent audit)
- Connect TSML directly to the σ braid via the shared CRT coordinates (σ is already known to be rotation on ℤ/5 ⊕ identity on ℤ/2 per Theorem E)
- Open a route toward a cleaner paper structure: "TSML and BHML as ℤ/2 × ℤ/5 products"

## What would kill this

If none of Readings 1/2/3 holds — that is, if TSML's cells depend on the underlying ℤ/10 structure in a way that does not factor through the CRT coordinates — then TSML is irreducibly a ℤ/10 object. Its harmony-dominance would have to be explained by something other than a product structure.

## Recommended next audit

ClaudeCode task for after the braid/BHML audits resolve:

1. Load the full TSML 10×10 table from source.
2. For each cell TSML[a][b], compute CRT coordinates of a, b, and TSML[a][b].
3. Test Reading 1: for each (a_ε, b_ε) pair, check whether all cells with that ε-pair have the same output ε-component, and whether the y-output depends only on (a_y, b_y).
4. Test Reading 2: same but allowing a separate y-rule per (a_ε, b_ε).
5. Test Reading 3: check whether the y-output depends only on (a_y, b_y), regardless of ε.
6. Report which reading holds (if any), with the explicit rule(s) extracted.
7. Repeat for BHML.

Result determines whether TSML and BHML can be honestly published as ℤ/2 × ℤ/5 products or must remain ℤ/10 tables.

## What this note does NOT claim

- Does not claim any of Readings 1/2/3 holds. All three are testable hypotheses, no audit has been run.
- Does not claim TSML and BHML simplify in parallel ways. They may have different structures.
- Does not claim the ℤ/5 piece carries more information than the ℤ/2 piece; this depends on the audit.
- Does not propose a new framework, theorem, or publication claim.

**The intuition behind this exploration is sound: CRT is already present in the project (σ decomposes via CRT per Theorem E), and testing whether TSML/BHML share that decomposition is a natural question.** The audit has not been performed yet. Do not cite this as a result until it has.

---

**Tag: [EXPLORATION — AUDIT REQUIRED]**
**File path: `papers/morphotic_braid/explorations/TSML_CRT_DECOMPOSITION_EXPLORATION.md`**
