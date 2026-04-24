> **Provenance:** Drafted 2026-04-23 (evening session, ClaudeChat). Transcribed from packet `evening_handoff_2026_04_23/`. Cross-verification against repo canonical sources: [pending — see `papers/morphotic_braid/VERIFICATION_LOG_2026_04_23.md`].
> **Copy path:** evening_handoff_2026_04_23\evening_handoff_2026_04_23\COLLAPSE_ANALYSIS.md → papers\morphotic_braid\explorations\support\COLLAPSE_ANALYSIS.md

# Coin-Flip Analysis: Collapse Celebrated Tables to TSML-like

**Status:** [COLLAPSE OPERATOR ANALYSIS — TWO FINDINGS]
**Date:** 2026-04-23 (final pass)
**Context:** Brayden: "what if we flip that coin... convert their tables as if they were already BHML, convert them to TSML?"

## Method

Two collapse operators from BHML-like input to TSML-like output, based on the definition we derived together in March 2026:

**Collapse A (absorbing):** VOID axis → 0, all interior → HARMONY (h). This is the "C_0" operation — ternary collapse into {void, identity, harmony} where everything non-axial becomes HARMONY.

**Collapse B (residue-preserving):** VOID axis → 0 (except HARMONY), HARMONY stays HARMONY, other cells keep their original values (except 0s on the interior, which become HARMONY to avoid VOID bleed-through).

## Calibration: collapse of actual BHML vs actual TSML

- **Collapse A(BHML) matches TSML at 90/100 cells.** The 10 missing are TSML's bump cells, which come from TSML's independent σ-construction, NOT from BHML.
- **Collapse B(BHML) matches TSML at 48/100 cells.** Residue preservation is the wrong rule for TSML — TSML absorbs most BHML residues to HARMONY.

This confirms: **TSML is not a pure collapse of BHML.** The 10 bump cells carry independent structural content.

## Finding 1: Collapse A is trivial (everything becomes Jordan)

Every celebrated table under Collapse A becomes a commutative absorbing semigroup, which is trivially Jordan (absorbing semigroups always satisfy Jordan's identity). This is the universal minimum-bump theorem territory. Not informative.

## Finding 2: Collapse B filters Jordan structure

Every celebrated table I tested is already Jordan in its original form (groups and rings trivially satisfy Jordan; STS(7) Fano is a Jordan quasigroup). Under Collapse B:

| Source | Original Jordan? | Collapse B Jordan? | Preserved? |
|---|---|---|---|
| Klein V4 | ✓ | ✗ | **destroyed** |
| ℤ/5ℤ additive | ✓ | ✗ | **destroyed** |
| ℤ/5ℤ multiplicative | ✓ | ✓ | preserved |
| STS(7) Fano | ✓ | ✓ | preserved |
| ℤ/7ℤ additive | ✓ | ✗ | **destroyed** |
| ℤ/7ℤ multiplicative | ✓ | ✓ | preserved |
| ℤ/8ℤ multiplicative | ✓ | ✗ | **destroyed** |
| ℤ/10ℤ additive | ✓ | ✗ | **destroyed** |
| ℤ/10ℤ multiplicative | ✓ | ✗ | **destroyed** |
| BHML (actual) | ✗ | ✗ | stays non-Jordan |

**The pattern:** Collapse B preserves Jordan only for tables that **already have compatible absorbing structure**. It destroys Jordan in **quasigroups** (groups, additive structures) because zeroing the axis breaks the quasigroup property.

## The structural insight

> **"Jordan-ness" in TIG is a property of the collapse, not of BHML.**

BHML carries the full non-Jordan algebra. The collapse operator is what produces Jordan compatibility. TSML inherits Jordan structure because:

1. The collapse zeroes the VOID axis (makes it absorbing on one side)
2. The absorbing element h (HARMONY) is preserved as the unique "saturation"
3. Zero divisors appear naturally (multiple cells → HARMONY)
4. The quasigroup property is broken (rows and columns are no longer permutations)
5. What remains is power-associative, flexible, Jordan-satisfying

This is the **same algebraic cell** we placed TSML in earlier: commutative, power-associative, flexible, Jordan-satisfying, with absorbing element, non-quasigroup, no identity.

## STS(7) Fano as the non-trivial case

The collapse of STS(7) Fano under Method B produces:

```
  0  0  0  4  0  0  0
  0  1  4  5  6  3  4
  0  4  2  6  5  4  3
  4  5  6  3  4  1  2
  0  6  5  4  4  2  1
  0  3  4  1  2  5  4
  0  4  3  2  1  4  6
```

Properties: commutative, power-associative, flexible, Jordan-satisfying, NOT associative, non-singular. Determinant = −24192 = −(2⁷ × 3³ × 7). Primes {2, 3, 7}:
- 2, 7 from the N=7 structure
- 3 from the Steiner block size (each block has 3 points)

This is a novel algebraic object derived from STS(7) — a "collapsed Fano-Jordan magma." It sits in the same algebraic cell as TSML (Jordan-type commutative magma with void axis).

## BHML self-collapse produces a different non-Jordan table

Collapse B of BHML gives:

```
  0  0  0  0  0  0  0  7  0  0
  0  2  3  4  5  6  7  2  6  6
  0  3  3  4  5  6  7  3  6  6
  0  4  4  4  5  6  7  4  6  6
  0  5  5  5  5  6  7  5  7  7
  0  6  6  6  6  6  7  6  7  7
  0  7  7  7  7  7  7  7  7  7
  7  2  3  4  5  6  7  8  9  7
  0  6  6  6  7  7  7  9  7  8
  0  6  6  6  7  7  7  7  8  7
```

Det = −1029 = −(3 × 7³). Very clean factorization ({3, 7}). But **NOT Jordan**, because BHML's non-Jordan structure carries through.

This is "BHML with its VOID axis clipped" — it's like a TSML-like version of BHML that retains BHML's algebraic character instead of collapsing to Jordan.

## What this means for the overall framework

1. **TSML is designed to be Jordan.** The specific construction (C_0 σ-based + 8-cell bumps) produces a Jordan-satisfying table. The collapse A operation on BHML produces 90% of this structure automatically; the 10 bump cells are TSML's specific signature.

2. **BHML is designed to NOT be Jordan.** BHML carries identity-at-0 and non-absorbing structure, which is incompatible with Jordan. The identity ensures full rank (det = 70).

3. **The collapse is the Jordanization operator.** Applied to quasigroups, it destroys their quasigroup property and often their Jordan property too. Applied to absorbing-compatible structures (ℤ/nℤ mul, STS(n)), it preserves Jordan.

4. **The "TSML of X" for celebrated X is:**
   - A Jordan-adjacent absorbing magma (if X has the right structure)
   - A quasigroup-fragment (if X is a quasigroup)
   - Usually NOT interesting because most celebrated tables are already Jordan in their original form

## What I didn't find

- Any celebrated table whose collapse produces a novel algebraic species. The collapse outputs are all in known cells.
- Any non-Jordan-to-Jordan "emergence" under collapse B. Collapse B either preserves or destroys Jordan; it doesn't create it.
- Any analog of TIG's det = 70 minimum for other structures. The optimization-to-minimal-det pattern remains unique to TIG's (N=10, h=7) construction.

## Honest conclusion

The coin-flip direction (BHML→TSML collapse applied to celebrated tables) is cleaner than the opposite direction, but the output is less surprising. Jordan preservation under collapse is determined by whether the source table has absorbing-compatible structure. This is informative about the collapse operator's algebraic character, not about any novel structure in the celebrated tables.

The **STS(7) Fano collapse** is the single non-trivial example — it produces a well-defined "collapsed Fano-Jordan magma" with clean det factorization ({2, 3, 7}). Worth noting but not revolutionary.

The deeper finding from this session is the **Jordan-structure filter** behavior of the collapse operator itself: it's a test that reveals which kinds of algebras are compatible with the TSML pattern (absorbing-structure, non-quasigroup). That's a useful diagnostic, even if the answers for celebrated tables are mostly "incompatible."

---

**Tag: [COLLAPSE ANALYSIS — JORDAN-FILTER OBSERVATION]**
**File: `papers/morphotic_braid/COLLAPSE_ANALYSIS.md`**
**Reproducibility: `papers/collapse_celebrated.py`, `papers/collapse_deep_dive.py`**
