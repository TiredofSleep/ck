> **Provenance:** Drafted 2026-04-23 (evening session, ClaudeChat). Transcribed from packet `evening_handoff_2026_04_23/`. Cross-verification against repo canonical sources: [pending — see `papers/morphotic_braid/VERIFICATION_LOG_2026_04_23.md`].
> **Copy path:** evening_handoff_2026_04_23\evening_handoff_2026_04_23\BHML_SUCCESSOR_AND_IDENTITY.md → papers\morphotic_braid\BHML_SUCCESSOR_AND_IDENTITY.md

# BHML_SUCCESSOR_AND_IDENTITY.md

**Status:** [DRAFT — POPULATED FROM CK SELF-PROVING ENTRY SCREENSHOT; AWAITING CROSS-VERIFICATION AGAINST SOURCE BHML TABLE]

Originally drafted as `CL_DUAL_ANCHOR_AUDIT.md`. Renamed because the honest statement is narrower and more precise than "dual anchor": the pattern is a BHML-specific successor-under-1 + identity-under-0 structure, not a general dual-anchor principle. Name matches content.

## Scope

This note tests the claim: each of the operators 1, 2, 3, 4, 5, 6 has a uniform 0-role and 1-role in the main TIG/CK BHML composition table, and 7, 8, 9 do not.

## Authoritative table

Main TIG/CK BHML (Being-Harmony Movement Language) [10×10] table, as pulled from the CK self-proving entry and annotated with det = 70, invertible, 28/100 entries equal HARMONY(7).

Source declaration from CK runtime:
- BHML[9][7] = 0: RESET ∘ HARMONY = VOID — the loop closes algebraically, not by instruction
- BHML[9][9] = 0: RESET ∘ RESET = VOID — absolute closure
- BHML[8][4] = 7: BREATH ∘ COLLAPSE = HARMONY — oscillation verified

## Notation

CL[a][b] means: a ∘ b, where the first index is the left operand (row) and the second is the right operand (column).

## Target audit: k ∈ {1, 2, 3, 4, 5, 6}

| k | k∘1 | 1∘k | k∘0 | 0∘k | 1-role | 0-role |
|---|---|---|---|---|---|---|
| 1 | 2 | 2 | 1 | 1 | successor (+1) | two-sided identity |
| 2 | 3 | 3 | 2 | 2 | successor (+1) | two-sided identity |
| 3 | 4 | 4 | 3 | 3 | successor (+1) | two-sided identity |
| 4 | 5 | 5 | 4 | 4 | successor (+1) | two-sided identity |
| 5 | 6 | 6 | 5 | 5 | successor (+1) | two-sided identity |
| 6 | 7 | 7 | 6 | 6 | successor (+1) | two-sided identity |

## Control rows: k ∈ {7, 8, 9}

| k | k∘1 | 1∘k | k∘0 | 0∘k | 1-role | 0-role |
|---|---|---|---|---|---|---|
| 7 | 2 | 2 | 7 | 7 | wraps to 2 (breaks successor) | two-sided identity |
| 8 | 6 | 6 | 8 | 8 | wraps to 6 (breaks successor) | two-sided identity |
| 9 | 6 | 6 | 9 | 9 | wraps to 6 (breaks successor) | two-sided identity |

## Mechanical findings

### Q1. Consistent 1-role across {1,...,6}?

**YES.** All six operators satisfy k ∘ 1 = k + 1 (in ℤ). 1 acts as successor uniformly across the set.

### Q2. Consistent 0-role across {1,...,6}?

**YES.** All six operators satisfy k ∘ 0 = 0 ∘ k = k. 0 acts as two-sided identity uniformly across the set.

### Q3. Symmetry?

- k ∘ 1 = 1 ∘ k for all k ∈ {1,...,6}: **YES** (symmetric at these cells)
- k ∘ 0 = 0 ∘ k for all k ∈ {1,...,6}: **YES** (symmetric at these cells)

### Q4. Do 7, 8, 9 behave differently from {1,...,6}?

**PARTIAL.**

- **0-role:** NO. All ten operators (including 7, 8, 9) have 0 as two-sided identity. The 0-role is universal across BHML, not restricted to {1,...,6}.
- **1-role:** YES. 7, 8, 9 break the successor pattern. Specifically, 7 ∘ 1 = 2 (not 8); 8 ∘ 1 = 6 (not 9); 9 ∘ 1 = 6 (not 10 ≡ 0 mod 10). The successor pattern under 1 holds for {1,...,6} and fails for {7, 8, 9}.

So {1,...,6} is distinguished from {7, 8, 9} **only** by the 1-role, not the 0-role. The real name for this finding is "BHML-successor regular" — a single-anchor regularity under 1.

### Q5. Compatibility with braid 6-cycle?

**NO. The sets are different.**

- BHML-successor set: {1, 2, 3, 4, 5, 6}
- Braid 6-cycle set: {1, 2, 4, 5, 6, 7}

These differ by {3 ↔ 7}. The BHML pattern contains PROGRESS (3) but excludes HARMONY (7); the braid cycle contains HARMONY (7) but fixes PROGRESS (3).

## Minimal factual summary

**BHML carries a successor-under-1 regularity on {1, 2, 3, 4, 5, 6} that fails at {7, 8, 9}.** 0 acts as two-sided identity throughout BHML; this is universal and does not distinguish subsets. The set where the BHML successor regularity agrees with the σ braid 6-cycle regularity is {1, 2, 4, 5, 6}, of cardinality 5.

## What this audit establishes

- A single-anchor BHML regularity structure, cleanly holding for {1,...,6}.
- An intersection with σ's 6-cycle that cuts down to {1, 2, 4, 5, 6}, the **doubly-regular core**.
- The foundation for the theorem in `doubly_regular_core.md`.

## What this audit does NOT establish

- Not a "dual-anchor" theorem in the strong sense — 0-identity is universal, not restricted.
- Not a claim about TSML or any other TIG table.
- Not a claim about the physical or metaphysical meaning of 7, 8, 9 as a special set.
- Not a direct claim about T* = 5/7; that ratio is derived separately in `doubly_regular_core.md`.

---

**Tag: [AUDIT COMPLETE — PENDING CROSS-VERIFICATION AGAINST SOURCE BHML TABLE]**
**File path: `papers/morphotic_braid/BHML_SUCCESSOR_AND_IDENTITY.md`**
