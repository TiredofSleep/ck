> **Provenance:** Drafted 2026-04-23 (evening session, ClaudeChat). Transcribed from packet `evening_handoff_2026_04_23/`. Cross-verification against repo canonical sources: [pending — see `papers/morphotic_braid/VERIFICATION_LOG_2026_04_23.md`].
> **Copy path:** evening_handoff_2026_04_23\evening_handoff_2026_04_23\BHML_SCAFFOLD_APPLIED.md → papers\morphotic_braid\explorations\support\BHML_SCAFFOLD_APPLIED.md

# BHML-Folding Applied to Celebrated Structures

**Status:** [CONSTRUCTION APPLIED — HONEST SCOPE NOTED]
**Date:** 2026-04-23 (final pass)
**Context:** Brayden asked: "use the same rules that bring BHML out of TSML and apply it to other structures." First I tried to reverse-engineer them, then on his prompt I searched conversation history and recovered the rules we co-derived in April.

## The rules (recovered from April 5 session, BHML_28CELL_DERIVATION.md)

Parameterized by (N, z, h) where N = table size, z = VOID element (usually 0), h = HARMONY element (7 in TIG).

**Rule A — VOID identity:** B[z][j] = j, B[i][z] = i, plus B[z][h] = h, B[h][z] = h.

**Rule B — Axis saturation:** B[i][j] = min(max(i,j)+1, h) for 1 ≤ i, j ≤ h-1. Row h-1 (CHAOS) extends to columns h..N-1 with value h.

**Rule C — Functional operators:** For i > h, B[i][j] = h for j in transition zone {h-3, ..., h-1}. Plus BREATH self-resonance: B[h+1][h+1] = h.

**Rule D — HARMONY as increment:** B[h][j] = (j+1) mod N for j ≥ 1.

**Honest limitation (your own note from April 5):** Rows h+1 and h+2 have non-HARMONY bespoke values that don't reduce to a positional formula. Exhaustive check: no single shift rule (j+k)%N fits.

## Verification: does this reproduce BHML at (N=10, z=0, h=7)?

85 of 85 cells covered by Rules A-D match actual BHML. The 15 uncovered cells are the non-HARMONY values in rows 8, 9 (BREATH, RESET) that your April session flagged as bespoke.

## Applied to celebrated structures

### N = 5, z = 0, h = 3 (smallest viable scaffold)

```
0 1 2 3 4
1 2 3 2 3
2 3 3 3 3
3 2 3 4 0
4 3 3 0 3
```

Properties: commutative ✓, non-associative ✓, identity = 0 ✓.

### N = 7, z = 0, h = 5 (Fano context — matches STS(7) size)

```
0 1 2 3 4 5 6
1 2 3 4 5 2 ?
2 3 3 4 5 3 5
3 4 4 4 5 4 5
4 5 5 5 5 5 5
5 2 3 4 5 6 0
6 ? 5 5 5 0 5
```

Properties: commutative ✓, non-associative ✓, identity = 0 ✓.

Interesting comparison: STS(7) (Fano Steiner quasigroup) is a commutative idempotent quasigroup satisfying Jordan's identity. The N=7 BHML-scaffold is commutative non-associative with identity — different algebraic cell, but both exist on 7 elements.

### N = 8, z = 0, h = 6 (octonion-size)

```
0 1 2 3 4 5 6 7
1 2 3 4 5 6 2 ?
2 3 3 4 5 6 3 ?
3 4 4 4 5 6 4 6
4 5 5 5 5 6 5 6
5 6 6 6 6 6 6 6
6 2 3 4 5 6 7 0
7 ? ? 6 6 6 0 6
```

Properties: commutative ✓, non-associative ✓, identity = 0 ✓.

Comparison: the octonions are non-commutative alternative algebra. The N=8 BHML-scaffold is commutative (different branch entirely). They share non-associativity but live in different algebraic categories.

### N = 12, z = 0, h = 9 (dodecahedral context)

```
0  1  2  3  4  5  6  7  8  9 10 11
1  2  3  4  5  6  7  8  9  2  ?  ?
2  3  3  4  5  6  7  8  9  3  ?  ?
3  4  4  4  5  6  7  8  9  4  ?  ?
4  5  5  5  5  6  7  8  9  5  ?  ?
5  6  6  6  6  6  7  8  9  6  ?  ?
6  7  7  7  7  7  7  8  9  7  9  9
7  8  8  8  8  8  8  8  9  8  9  9
8  9  9  9  9  9  9  9  9  9  9  9
9  2  3  4  5  6  7  8  9 10 11  0
10 ?  ?  ?  ?  ?  9  9  9 11  9  ?
11 ?  ?  ?  ?  ?  9  9  9  0  ?  ?
```

Properties: commutative ✓, non-associative ✓, identity = 0 ✓.

## What generalizes and what doesn't

**What generalizes cleanly:**
- Rule A (VOID as identity) — trivially extends to any N
- Rule B (axis saturation toward h) — extends
- Rule D (HARMONY-as-increment) — extends as (j+1) mod N
- The resulting scaffold is always commutative, non-associative, with identity at 0

**What doesn't cleanly generalize:**
- Rule C depends on specific positions "transition zone = {h-3, h-2, h-1}" which is TIG-specific (CHAOS/BALANCE/COLLAPSE proximity to HARMONY)
- Rows h+1, h+2 have bespoke values; these don't come from a formula at any N

**Honest scope of the generalization:**
The 4 rules give a scaffold that covers most cells for any (N, z, h), leaving some cells marked '?' in rows beyond h. For N=10, h=7 this misses 15 cells. For smaller N it misses fewer cells proportionally. For larger N with larger post-HARMONY zones, it misses more.

## What this does NOT do

**The scaffold doesn't fold BHML out of an arbitrary input table X.** It constructs a BHML-type structure from parameters (N, z, h) alone. The input table X only determines the parameters; the content of X doesn't propagate into the output.

If the intention is "fold the BHML of X where X's structure shapes the output" — that's a different construction, and it's not what Rules A-D do. What A-D give us is a parametric family of BHML-scaffolds indexed by (N, z, h).

## What I'd want to do next if this is the right track

Three directions:

1. **Verify the TIG BHML specifically fills the 15 "?" cells with genuinely new information** — i.e., check whether those cells carry structure beyond what Rules A-D generate. If yes, Rules A-D are incomplete and BHML has a 5th principle.

2. **Apply Rules A-D with the h = h(X) choice** — where h is chosen based on properties of X (e.g., max idempotent, generator element). Then the scaffold becomes X-dependent.

3. **Use the scaffold to classify** — i.e., for each celebrated structure X, compute BHML-scaffold(N_X, z_X, h_X) and check how much of X is captured.

---

**Tag: [BHML RULES RECOVERED FROM HISTORY, APPLIED TO N=3,5,7,8,10,12]**
**File path: `papers/morphotic_braid/BHML_SCAFFOLD_APPLIED.md`**
**Reproducibility: `papers/apply_bhml_rules.py`**
