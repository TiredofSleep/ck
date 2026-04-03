# GLOSSARY.md
## CK Framework — Algebraic Dictionary
*Author: Brayden Ross Sanders / 7Site LLC — 2026-04-03*
*Every term used in the Gen11 Clay documentation is defined here.*
*If a doc says "Earth" and you don't know what that means: start here.*

---

## Core Algebraic Objects

| Term | Algebraic Definition | Numeric Value | Notes |
|------|---------------------|---------------|-------|
| **T*** | CREATE / HARMONY = 5 / 7 | 0.71428... | The coherence threshold. Unique forced fixed point of the complement-equivariant map on Z/10Z. All regime splits are measured relative to T*. |
| **CREATE** | The unique complement-equivariant odd fixed point of Z/10Z | 5 | x → (10−x) fixes x=5. Also: n=5 in the K*(n) cascade. Also: the eternal bridge state. |
| **HARMONY** | Generator-inverse of (Z/10Z)* under primitive root g=3 | 7 | 3^3 = 27 ≡ 7 mod 10. HARMONY generates (Z/10Z)* = {1,3,7,9}. |
| **n*** | Foundation index = CREATE + 1 = HARMONY − 1 | 6 | The smallest n that can satisfy T* with finite data. Below n*: permanently sub-threshold. At n* and above: eventually crosses T*. |
| **K*(n)** | The minimum number of Riemann zeros (ordered by imaginary part) such that λ_n(K) ≥ T* | 99 (n=6), 14 (n=7), ... 1 (n≥13) | The threshold-crossing count at frequency n. Decreases monotonically for n ≥ n*. NEVER for n ≤ 5. |
| **PROGRESS** | N_operators − HARMONY = 10 − 7 | 3 | The gap in Z/14Z: gap = PROGRESS / (2 × HARMONY) = 3/14. |
| **N_operators** | Total operator count in Z/10Z | 10 | The modulus. |
| **λ_n(K)** | Li coefficient at index n, truncated at K zeros | computed | λ_n(K) = 2·Σ_{k=1}^{K} (1 − cos(n·θ_k)). RH iff λ_n ≥ 0 for all n. |
| **θ_k** | Zero angle for k-th Riemann zero | computed | θ_k = π − 2·arctan(2·γ_k), where γ_k = Im(k-th Riemann zero). ∈ (0,π) for on-line zeros. |

---

## The Ternary States {0, 1/2, 5/7}

These are the three states of the ternary partition. Every algebraic and physical object in the framework falls into exactly one.

| State | Algebraic Condition | Range | Name Used in Docs | Elemental Name | Meaning |
|-------|--------------------|----|---|---|---|
| **State 0** | λ_n < 1/2 | [0, 1/2) | RECYCLED | **Void** | No coherence. Force insufficient. Sub-threshold permanently (n≤5) or pre-threshold (n≥6, K < K_enter). |
| **State 1/2** | λ_n ∈ [1/2, 5/7) | [1/2, 5/7) | FLOW / BRIDGE | **Flow** | 5D force recursion active. Opposing-phase zone — all zeros resist threshold crossing. Time is made here. n=5=CREATE lives here permanently. |
| **State 5/7** | λ_n ≥ 5/7 = T* | [5/7, ∞) | STRUCTURE / HELD | **Earth** | Self-sustaining. Stands on the foundation T*. Generator regime. |

**"Earth" = algebraic shorthand for STATE 5/7 = {λ_n ≥ T*} = the held/generator/structure regime.**
**"Earth stands on CREATE" = {λ ≥ T*} stands on T* = CREATE/HARMONY, where CREATE = n=5 = eternal flow.**

---

## Structural Terms

| Term | Definition |
|------|-----------|
| **Bridge zone** | The interval [1/2, 5/7) in λ-space. The zone of 5D force recursion (flow). Every zero encountered here is in opposing phase: cos(n·θ_k) > 0, so each zero adds force but resists the crossing. |
| **Bridge width** | K*(n) − K_enter(n): number of zeros inside the bridge before threshold crossing. INF for n=5. 87 for n=6. 9 for n=7. 0 for n≥13. |
| **Shadow** | The K*(n)−1 state: one zero short of threshold crossing. The last point the ruler resolves before the held state. K=98 for n=6 (at 99.9984% T*). K=13 for n=7 (at 98.40% T*). |
| **Bandwidth floor** | n = n* + HARMONY = 6 + 7 = 13. At n≥13: K*(n)=1. One zero is sufficient to cross T*. The maximum compression of the measurement. |
| **Eternal flow** | n=5=CREATE. Enters bridge at K=106. Force per zero = 0.0000142 (decelerating asymptotically). Never exits. IS the flow, not a structure in the flow. |
| **Opposing phase** | cos(n·θ_k) > 0 for a zero inside the bridge. The zero adds force (Δ_k > 0) but less than the neutral maximum (Δ_k < 2). ALL zeros inside the bridge are in opposing phase. |
| **Harmonic series** | Σ 1/k. The marginal return of the k-th zero is ~1/k. The K*(n) cascade is the harmonic series hitting T* at different frequencies. Counting's own diminishing return structure. |

---

## The Five Rules (brief)

| Rule | Name | One-line |
|------|------|----------|
| Rule 0 | Counting | Marginal return of k-th item = 1/k. All rules are corollaries. |
| Rule 1 | Gate | T* = M/G forced. In Z/10Z: T*=5/7. |
| Rule 2 | Foundation | n*=6 is the unique boundary: below = never holds, at/above = eventually holds. |
| Rule 3 | Recycling | Sub-threshold contributions carry forward as remainder. K*(6)=7×14+1=99. Sha=the +1. |
| Rule 4 | Two-Regime | T* is the unique complement fixed point. Exactly two orbits: below and above. |
| Rule 5 | Cascade | K*(n) decreases monotonically for n≥n*. Direction algebraically forced. |

---

## Elemental / Physical Names and Their Algebraic Bindings

*These names appear in the philosophical/synthesis sections of the docs.*
*They are NOT vague metaphors. Each has an exact algebraic referent.*

| Elemental Name | Algebraic Object | Where Defined |
|----------------|-----------------|---------------|
| **Earth** | State 5/7: {λ_n ≥ T*}. The held/structure/generator regime. | TERNARY_REDUCTION.md, RESOLUTION_LIMIT.md |
| **Flow** | State [1/2, 5/7): the bridge zone. 5D force recursion. | TERNARY_REDUCTION.md, BRIDGE_ENTANGLEMENT.md |
| **Void** | State 0: {λ_n < 1/2}. Recycled, sub-threshold. | TERNARY_REDUCTION.md |
| **Foundation** | T* = 5/7. The threshold Earth stands above. | UNIVERSAL_RULES.md Rule 1 |
| **CREATE** | n=5. The eternal flow. Numerator of T*. The thing Earth stands on. | All documents. |
| **HARMONY** | n=7. The generator. Denominator of T*. What measures Earth. | All documents. |
| **Counting** | The harmonic series Σ 1/k applied to zero force accumulation. | FINITE_MEASUREMENT.md, UNIVERSAL_RULES.md Rule 0 |
| **Time** | The dwell time inside the bridge [1/2, 5/7): bridge width × (average force per zero)^{-1}. Made by the opposition of zeros against threshold crossing. | BRIDGE_ENTANGLEMENT.md |
| **Ruler** | The T*-calibrated measurement framework. Made of T*. Cannot measure past T* with a ruler made of T*. | RESOLUTION_LIMIT.md |
| **Gap** | 3/14 = T* − 1/2 = PROGRESS / (2 × HARMONY). A named object in Z/14Z (element 3). Not a floating distance. | TERNARY_REDUCTION.md, FINITE_MEASUREMENT.md |

---

## Why These Names Are Used

The algebraic objects in Z/10Z are operators with physical/linguistic derivations (from Hebrew root D2 encoding, see Gen9 papers). The names CREATE, HARMONY, VOID etc. are NOT ornamental — they are the operator names from the CK language system that generated the framework. The elemental names (Earth, Flow, Void) follow from the ternary partition matching the classical physical elements:

- **Void** (State 0): no force, no structure, no time
- **Flow** (State [1/2, 5/7)): force active, structure absent, time being made
- **Earth** (State [5/7, ∞)): force held, structure standing, time resolved

A reader who finds "Earth stands on CREATE" confusing should read: **{λ≥T*} stands on T*=CREATE/HARMONY, where CREATE=5 is the unique complement-equivariant fixed point of Z/10Z and HARMONY=7 is the generator-inverse under g=3.**

That is the grounded version. Both are correct.

---

## Index of All Gen11 Documents

| Document | What it contains |
|----------|-----------------|
| `GLOSSARY.md` | **This file.** All term definitions. Start here. |
| `UNIVERSAL_RULES.md` | The five rules (+ Rule 0) that generate all Clay arguments. |
| `FRACTAL_PATH_MAP.md` | The K*(n) cascade, three-layer gap structure, bandwidth floor. Computed from K=5000 zeros. |
| `TERNARY_REDUCTION.md` | The {0, 1/2, 5/7} partition. Bridge widths. All five Clay problems reduced to one question. |
| `RESOLUTION_LIMIT.md` | Final position. What the framework can and cannot see. The ruler made of T*. |
| `BRIDGE_ENTANGLEMENT.md` | Forces inside the bridge [1/2, 5/7). Opposing phase. Time from fighting. Fractal residual. |
| `FINITE_MEASUREMENT.md` | Why finite consequence = measurement. Z/2Z×Z/3Z minimal case. Consciousness analog. |
| `FORMAL_RH.md` | Riemann Hypothesis: what's proved, what's structural argument, what's open. |
| `FORMAL_BSD.md` | BSD: Sha as carried remainder. Bridges tested and falsified. |
| `FORMAL_NS_PNP.md` | Navier-Stokes + P vs NP formal positions. |
| `FORMAL_HODGE.md` | Hodge: BSD→Hodge chain. Markman 2025 cited. |
| `CLAY_FORMAL_RECORD.md` | Full 25-part formal record. All computations, all positions, Parts I-XXV. |
| `FINITE_MEASUREMENT.md` | Finite consequence axiom. Measurement requires bandwidth. |
| `riemann_zeros_5000.json` | 5000 mpmath-precision Riemann zeros. Source data for all computations. |
| `gap_forces_study.py` | Study of 5D forces inside the bridge zone. |
| `bandwidth_floor_bridge.py` | Bandwidth floor as bridge location. Off-line zero robustness test. |

---

*(c) 2026 Brayden Ross Sanders / 7Site LLC*
*7Site Public Sovereignty License v1.0 — Human use only. Free forever.*
*DOI: 10.5281/zenodo.18852047*
