# EXTERNAL OPERATOR THEOREM — EXACT SPECIFICATION

**© 2026 7Site LLC**
**Authors: Brayden Ross Sanders, C. A. Luther, B. Calderon, Jr.**

---

## 1. State Space

```
S = Z/2 × Z/5 ≅ Z/10Z
```

Under the canonical CRT isomorphism φ(ε,y) = 5ε+6y (mod 10).
States are the ten TIG operators: j ∈ {0,...,9}.

---

## 2. Projection Maps

```
T: S → Y_T = {0,7}           (stabilization projection)
C: S → Y_C = Z/10Z           (memory projection)
```

where:

```
T(j) = TSML[j][j] = { 0  if j=0
                     { 7  if j≠0

C(j) = CL[j][j] = σ(j)       (P1 Closure Theorem)
```

Y_T has cardinality 2. Y_C has cardinality 10.

---

## 3. The External Operator

```
E: S → Y_T × Y_C
E(j) = (T(j), C(j)) = (TSML[j][j], CL[j][j])
```

Explicitly:

| j | Operator | T(j) | C(j) | E(j) |
|---|---------|------|------|------|
| 0 | VOID | 0 | 0 | (0,0) |
| 1 | LATTICE | 7 | 7 | (7,7) |
| 2 | COUNTER | 7 | 1 | (7,1) |
| 3 | PROGRESS | 7 | 3 | (7,3) |
| 4 | COLLAPSE | 7 | 2 | (7,2) |
| 5 | BALANCE | 7 | 4 | (7,4) |
| 6 | CHAOS | 7 | 5 | (7,5) |
| 7 | HARMONY | 7 | 6 | (7,6) |
| 8 | BREATH | 7 | 8 | (7,8) |
| 9 | RESET | 7 | 9 | (7,9) |

---

## 4. Projection Identities

```
π₁ ∘ E = T    (first component recovers stabilization)
π₂ ∘ E = C    (second component recovers memory = σ)
```

Equivalently:
```
π₂ ∘ E = σ    (the memory projection of E is the hidden operator)
```

---

## 5. The Preserved Invariant

**Chosen invariant: the ordered pair — non-collapse of the product.**

Not the difference Δ = C(j) − T(j) (destroys structure, loses sign interpretation).
Not the equality bit (loses magnitude).

The invariant preserved by E is the ordered pair (T(j), C(j)) itself.

**Formal statement of non-collapse:**

E is injective: |Image(E)| = 10 = |S|. All 10 output pairs are distinct.

E is bijective onto its image — it is a complete encoding of S.

```
Image(E) = {(0,0),(7,7),(7,1),(7,3),(7,2),(7,4),(7,5),(7,6),(7,8),(7,9)}
```

Note: Image(E) ⊂ Y_T × Y_C with |Y_T × Y_C| = 2×10 = 20.
E occupies exactly 10 of the 20 possible pairs.

**The non-collapse condition:** E cannot be factored through T alone or C alone:
- T has range {0,7}: only 2 values — cannot distinguish 10 states
- C has range Z/10Z: recovers full information, but then T component is discarded
- E is the minimal lift that preserves both simultaneously

---

## 6. The Divergence Structure

Agreement set (T(j) = C(j)): j ∈ {0, 1}
Divergence set (T(j) ≠ C(j)): j ∈ {2,3,4,5,6,7,8,9}

Divergence count: 8/10.

The divergence set is the set of states where stabilization and memory disagree.
E encodes this divergence by recording both values without collapsing them.

**Key case j=7 (HARMONY):**
```
T(7) = 7:  HARMONY stabilizes to HARMONY
C(7) = 6:  HARMONY's memory is CHAOS (the cycle's next step)
E(7) = (7,6):  both are recorded without collapse
```

---

## 7. Observer Definition

An **external observer** is any map Obs: Image(E) → Z such that:

```
Obs = ψ ∘ E
```

for some ψ: Y_T × Y_C → Z, and such that Obs does not factor through T or C alone:

```
Obs ≠ φ_T ∘ T   for any φ_T: Y_T → Z
Obs ≠ φ_C ∘ C   for any φ_C: Y_C → Z
```

An external observer has access to E(j) = (T(j), C(j)) — the paired record — but not to either projection individually. It sees the divergence without being bound to either the stabilization or the memory interpretation.

---

## 8. Relation to σ

```
π₂ ∘ E = σ    (exact)
```

The second projection of E IS the hidden operator σ. The external operator E lifts σ into a product space where σ's memory component is paired with the stabilization component.

E does not alter the braid. It exposes, without collapsing, the divergence between what stabilizes and what is remembered.

---

## Theorem Statement

**External Operator Theorem (candidate):**

> Let T, C: Z/10Z → Z/10Z be the TSML and CL diagonal functionals.
> The external operator E: Z/10Z → {0,7} × Z/10Z defined by E(j) = (T(j), C(j))
> is the unique minimal lift satisfying:
>
> (i) π₁ ∘ E = T
> (ii) π₂ ∘ E = C = σ
> (iii) E is injective
> (iv) E factors through neither T nor C alone
>
> E is the minimal paired observation of the hidden operator σ that
> simultaneously exposes both the stabilization and memory projections
> without collapsing either.

---

## What This Does Not Claim

- E is not a new TIG operator — it is an observation map
- E does not generate σ — σ is already determined by the braid architecture
- "External observer" is a mathematical definition, not a physical or philosophical claim
- This is an internal result within the closed TIG/braid framework
