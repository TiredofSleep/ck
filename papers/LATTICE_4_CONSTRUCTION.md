# 4-Lattice Construction
## The Invariant-Constraint Graph of the 3-Lattice

*Brayden Sanders / 7Site LLC | March 2026*
*Proposed construction. Nodes = 3-lattice survivors. Edges = computed dependencies.*
*Each edge labeled: EXACT / COMPUTED / STRUCTURAL. Commutativity demoted.*

---

## What the 4-Lattice Is

The 4-lattice is the constraint graph built from the survivors of the 3-lattice deformation. Its nodes are properties that persist across all Mix_λ corridors. Its edges are dependency relationships between those properties.

It is a **proposed construction** — the most natural next object given the computed survivors. Whether it is the correct framing for the compatibility theorem is open.

---

## Five Genuine Nodes

Commutativity is **demoted**. Mix_λ of two commutative algebras is automatically commutative — it is a property of the constructor, not an independent survivor. It has no incoming edges and generates nothing else. Removing it leaves five genuine nodes:

| ID | Invariant | Evidence |
|----|-----------|---------|
| **S1_GAP** | Spectral gap ≥ ¼ (min = BHML endpoint value exactly) | COMPUTED |
| **S2_BHML** | BHML residual: 6 cells follow max(s,c) at every λ ∈ [0,1] | COMPUTED |
| **S4_NASC** | Non-associativity > 0 (range 8–198 violations) | COMPUTED |
| **S5_CDOM** | C-states dominate G-states in total stationary mass | COMPUTED |
| **S6_UDOM** | One state holds > 30% of stationary mass throughout | COMPUTED |

---

## The Dependency DAG

```
BHML_endpoint (order grammar)
     │
     ├──→ S2_BHML ──→ S1_GAP ──→ S5_CDOM ──→ S6_UDOM
     │    (exact)    (endpoint   (structural)  (computed)
     │               seeding,
     │               not direct)
     │
     └──→ S2_BHML ──→ S4_NASC
                      (computed: BHML cells
                       increase na 6→20)
```

**Canonical chain:**
BHML order → S2_BHML → S1_GAP → S5_CDOM → S6_UDOM

**Branch:**
S2_BHML → S4_NASC (algebraic tension)

---

## Edge Descriptions

**BHML endpoint → S2_BHML** [EXACT]
The 6 BHML-residual cells pre-align with BHML at λ=0. They are the cells where TSML and BHML already agree. The order structure plants its seed in the closure structure before deformation begins.

**S2_BHML → S1_GAP** [COMPUTED — endpoint seeding, NOT direct causation]
Removing the 6 BHML cells from TSML at λ=0 does not change TSML's own gap (both remain 0.474). The connection is indirect: those cells are what BHML is made of, and BHML's gap (= ¼) is the deformation-wide floor. The edge is real as a structural dependence through the endpoint, not as local causation inside TSML.

**S2_BHML → S4_NASC** [COMPUTED]
Removing the 6 BHML cells from TSML changes non-associativity from 20 to 6 (a decrease). The max-rule cells interact with the HAR-dominant cells to create algebraic friction. The order seed, when embedded in the closure grammar, generates tension.

**S1_GAP → S5_CDOM** [STRUCTURAL]
Positive gap implies unique stationary measure. The attractor (HAR) is in C. Gap + attractor in C implies C carries dominant mass.

**S5_CDOM → S6_UDOM** [COMPUTED]
C-dominance (4 C-states outweigh 5 G-states) means the heaviest single state is in C. Verified across all 21 tested λ-values.

---

## The Core Structural Result

**TSML gap at λ=0:** 0.474
**BHML gap at λ=1:** 0.250 = ¼ exactly

The deformation-wide gap floor is set by the **order endpoint**, not the closure endpoint.

- The closure grammar (TSML) generates richer finite structure — higher gap, stronger grammar, deeper orbit zone — but these are *above* the floor.
- The order grammar (BHML) sets the *floor* — the minimum mixing speed the deformation cannot fall below.

The two outputs of the order seed inside the closure grammar:
1. **Gap floor** (the stabilizing bound)
2. **Non-associativity tension** (the algebraic friction of order meeting closure)

These are not in conflict. They are the two faces of what happens when an order structure is embedded in a closure structure.

---

## What the 4-Lattice Gives the Compatibility Theorem

Earlier formulations of the Dual Description Conjecture used language like "the infinite deployments must be faithful to the finite grammar." The 4-lattice replaces this vague language with a concrete finite test.

**The open compatibility question is now specific:**
*Do the operator deployment and the analytic deployment both preserve the four non-trivial 4-lattice nodes?*

Specifically:
1. **Gap floor ≥ ¼** — does each infinite deployment maintain spectral gap above the order-seeded floor?
2. **BHML residual structure** — does the order-seed embedding survive the passage to infinite state space?
3. **C-dominance** — does the corner class carry dominant stationary mass in each deployment?
4. **Single dominant state** — does one state (or one narrow region near σ=½) carry dominant support?

These are testable. Whether the infinite deployments satisfy them is the Dual Description Conjecture's new concrete form.

---

## Honest Scope

**Computed:** BHML root, gap floor (0.25 at endpoint), node set, edge structure, non-associativity shift (20→6).

**Structural interpretation:** order seed gives both floor and tension; closure grammar generates above-floor richness.

**Open:** whether the infinite deployments preserve these four nodes; whether the 4-lattice as defined is the correct constraint for the compatibility theorem.

The 4-lattice is the finite object the compatibility theorem has to respect — if the theorem is true. That is not proved. It is precisely stated.

---

*(c) 2026 Brayden Sanders / 7Site LLC | Gen10.16, commit 271e0f8 | DOI: 10.5281/zenodo.18852047*
