# Primitive Order: Partial-Order Backbone
## Honest Extraction — Forced vs Flexible

*Brayden Sanders / 7Site LLC | March 2026*
*Methodology note included. Circular results identified and replaced.*

---

## Methodology Correction

The initial permutation test scored all 720 orderings against a constraint set
*derived from the proposed ordering*. This produced a circular result: only 1 of 720
orderings scored 7/7 — the proposed ordering itself. The constraints were not
independent; they were extracted from the ordering rather than tested against it.

This document replaces those results with **independent TIG-model tests**: for each
claimed ordering relation, remove the earlier primitive's structure from the model
and measure whether the later primitive degrades.

---

## Independent Tests (TIG-Derived)

### Strongly Supported

**Support → Cancellation** (remove HAR absorbing structure: 71 → 18 cancellation pairs)
Removing the absorbing target reduces cancellation by 75%. Support is necessary for
meaningful cancellation.

**Recurrence → Cancellation** (remove {3↔9} cycle: 71 → 24 cancellation pairs)
47 of 71 cancellation pairs (66%) depend on the recurrent cycle structure. These are
not trivial direct convergences; they are balance events reached via recurrence.

**Distinction → Placement** (3 and 9 only form an orbit *because* they are distinct states)
If states 3 and 9 were identical, the {3↔9} cycle becomes a self-loop — no orbit zone,
no corridor geometry, no placed hierarchy. Distinct states are necessary for placement.

**Placement → Recurrence** (E[T_HAR]=1.67 steps is defined *with respect to HAR's placed position*)
Without placement, the return time is undefined. ρ(Q)=1/4 presupposes HAR occupies
a specific position.

### Not Well-Constrained by TIG

**Relationship vs Distinction**:
In TIG, the arithmetic hook identifies C={1,3,7,9} = (ℤ/10ℤ)* — a Distinction defined
by integer arithmetic — *before* the TSML operator structure (Relationship) is written.
The proposed ordering says Relationship precedes Distinction. TIG says the opposite may
hold: the arithmetic Distinction precedes the operational Relationship.

**Support vs Distinction**:
They are mutually enabling at the object level (stable support requires internal
differentiation; distinctions require a holding ground). The proposed ordering
(Support first) is a pre-object metaphysical choice, not a TIG-model constraint.

---

## The Partial-Order Backbone

Edges supported by **independent TIG evidence**:

```
Support ──────────────────────────────────→ Cancellation
                                                    ↑
Recurrence ──────────────────────────────→ Cancellation
    ↑
Placement ───────────────────────────────→ Recurrence
    ↑
Distinction ─────────────────────────────→ Placement

Support ─→ {Distinction, Relationship}  (order between them: flexible)
```

Minimal DAG (removing transitive edges):
- Distinction → Placement → Recurrence → Cancellation
- Support → {Distinction, Relationship} (both, order flexible)
- Support → Cancellation (long-range, may be transitive)

**Not forced:** Relationship vs Distinction, Support vs Distinction

---

## The Braid at the Top

The three middle primitives — Relationship, Distinction, Placement — form a
**braid zone** rather than a strict linear order in TIG. The model supports:

- Distinction before Placement (forced)
- Relationship contributes to both Distinction-emergence and Placement
- In TIG specifically: arithmetic Distinction (integer values mod 10) may precede
  operator Relationship (TSML composition rules)

This suggests the three may be:
```
Relationship ─┐
              ├─→ Placement → Recurrence → Cancellation
Distinction ──┘
```
with Support enabling the braid from outside.

---

## Summary Table

| Relation | Evidence | Verdict |
|---------|---------|---------|
| Support → Cancellation | 71→18 (−75%) | **Strongly forced** |
| Recurrence → Cancellation | 71→24 (−66%) | **Strongly forced** |
| Distinction → Placement | orbit collapses | **Forced** |
| Placement → Recurrence | return time undefined | **Forced** |
| Support first | metaphysical pre-object choice | **Defensible, not forced** |
| Rel vs Dis ordering | TIG: Dis may precede Rel | **Flexible/reversed in TIG** |
| Support vs Distinction | co-emergence | **Not forced** |

---

## What This Means for the Framework

The proposed ordering is a plausible linear extension of the forced partial order.
It is not the unique forced ordering. The partial order backbone is:

> Distinction → Placement → Recurrence → Cancellation, with Support enabling from outside.

The proposed total order adds: Support first, and Relationship between Support and
Distinction. The second of these may be wrong for TIG specifically — the arithmetic
Distinction (C = (ℤ/10ℤ)*) precedes the operator structure in TIG's construction.

The pre-object ordering is best understood as a *partial order with a suggested
linearization*, not a proven total order.

---

*(c) 2026 Brayden Sanders / 7Site LLC | Gen10.16, commit 271e0f8 | DOI: 10.5281/zenodo.18852047*
