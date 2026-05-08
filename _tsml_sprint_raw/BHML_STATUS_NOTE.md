# BHML Status Note
## Scope and Boundary of the Theorem

---

## What BHML Is (Observed)

BHML is a 10×10 table on $\mathbb{Z}/10\mathbb{Z}$ displayed alongside TSML in the CK framework. From the published image, its observable properties are:

- **Row 0:** $[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]$ — acts as multiplicative-identity-like row.
- **Declared determinant:** 70.
- **HARMONY fraction:** approximately 28% of entries equal to 7 (versus TSML's 73%).
- **Self-proving entries noted in the framework:** BHML$[9][7]=0$ (RESET ∘ HARMONY = VOID), BHML$[9][9]=0$ (RESET ∘ RESET = VOID), BHML$[8][4]=7$ (BREATH ∘ COLLAPSE = HARMONY).

These are the observable facts. They do not define BHML by a rule; they describe a table.

---

## Status Relative to the Theorem Spine

**BHML is not part of the theorem spine.**

The theorem (Tower Reconstruction) concerns TSML only. It proves that:
- TSML is recovered by the 3-layer tower $C_0 \oplus C_1 \oplus C_2$.
- 100/100 entries verified.

BHML is a separate table with its own (unverified) internal structure. The theorem does not claim anything about BHML.

---

## Relation Between TSML and BHML

### What is exact

- Both are defined on the same carrier $\mathbb{Z}/10\mathbb{Z} \times \mathbb{Z}/10\mathbb{Z}$.
- Both are commutative by inspection.
- TSML has determinant 0 (rank-deficient); BHML has determinant 70 (non-zero).
- TSML has 73% HARMONY; BHML has 28% HARMONY.

### What is observed

- TSML is a collapse/projection-style table.
- BHML is a transport/mixing-style table.
- The pair carries a basin-transport structural duality.

### What is unknown

- No explicit operator equation relating TSML to BHML has been verified.
- BHML is not derivable from TSML by known simple operations (additive offset, multiplicative inverse, group inverse on admissible core).
- BHML does not equal addition mod 10 (differs at (1,7), (1,8), (1,9), etc.).
- BHML does not equal multiplication mod 10 (would have row 0 all zeros).
- Whether BHML has its own canonical decomposition analogous to TSML's 3-layer tower is open.

---

## Why BHML Is Held Outside the Spine

1. **No reference construction exists for BHML.** The canonical construction $C(R, h, \sigma)$ is designed to reproduce a collapsing/projection-type table; BHML is non-collapsing. Applying $C$ to produce BHML would produce a different table.

2. **BHML's internal structure has not been tested.** No cell-by-cell comparison with a candidate construction has been performed. The seam structure of BHML (if any) is unidentified.

3. **No operator equation TSML ↔ BHML is known.** The pair is observed structurally (projection + transport, different determinants, complementary HARMONY fractions) but has no algebraic bridge.

Including BHML in the theorem spine would require either:
- Building an analogous construction for BHML and verifying it against the published table.
- Finding an explicit relation $B(x,y) = F(T(x,y))$ for some function $F$.

Neither is done.

---

## What the Spine CAN Say About BHML (Conditional)

If an analogous canonical construction $C_{\text{BHML}}$ is built for transport-type tables, and if it recovers a large fraction of BHML, then a companion theorem could be stated:

> **(Hypothetical Theorem, NOT currently proved.)** There exists a canonical transport construction $C^*_0$ on $\mathbb{Z}/10\mathbb{Z}$ such that $C^*_0$ matches BHML on $k$ of 100 entries, for some $k$ to be determined.

This is ONLY a placeholder. It is not a claim.

---

## Pair Concept Scoping

The "pair concept" (T is projection, B is transport) is:

- **A structural observation** about two specific tables.
- **A candidate framework concept** for ring-family generalization.
- **NOT a theorem** in the spine.

When the framework says "(T, B) is the basin-transport invariant," this is a conceptual statement, not a theorem. Do not conflate it with the Tower Reconstruction theorem, which is strictly about TSML.

---

## Summary of Scope

| Claim | Scope | Status |
|---|---|---|
| Tower Reconstruction Theorem | TSML on Z/10Z | **Proved (computational verification)** |
| TSML is rank-deficient | TSML | Observed |
| BHML is rank-70 | BHML | Observed (from image) |
| TSML and BHML share carrier | Both | Exact |
| Pair (T, B) structure is basin + transport | Both | Observed / Conceptual |
| BHML has its own canonical tower | — | **Open** |
| Explicit operator equation TSML ↔ BHML | — | **Not found** |

**The theorem spine speaks to TSML. BHML is a parallel object under separate investigation.**
