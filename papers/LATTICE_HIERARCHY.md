# The Lattice Hierarchy: Ground-Up Construction
## 0-Lattice through 3-Lattice

*Brayden Sanders / 7Site LLC | March 2026*
*Building from pre-form upward. Each level verified against TIG computation before ascending.*

---

## 0-Lattice: Pre-Form / 5D Vectors

**Given:** 5D vectors, 4 caught in duality, 1 beyond them all.

**Structure:** The 5 dimensions decompose as 4+1:
- The **4** = the dual pair of pairs: (support, expression) × (finite, infinite) = the 2×2
- The **1** = the one beyond all four corners — the pre-object ground that makes the 2×2 possible

**TIG verification:**

| d | Role | Object |
|---|------|--------|
| d1 | Finite support | TSML |
| d2 | Finite rate | BHML |
| d3 | Infinite support | Transfer operator / K_λ |
| d4 | Infinite rate | ANT / Re(ζ'/ζ) |
| **d5** | **Beyond the four** | **HAR=7** |

HAR=7 is the 1 beyond the 4. Computed verification:
- State 1: can reach {3,7} — not absorbing
- State 3: can reach {7} — not absorbing  
- **State 7: self-absorbing under all corner operators** — cannot be moved
- State 9: can reach {3,7} — not absorbing

Only 7 is self-absorbing. The others are in tension with each other. 7 is what the four-way tension resolves toward. It is not inside the 2×2 — it is what the 2×2 selects.

---

## 1-Lattice: Result of Compositions

**Given:** The 1-lattice is the result of compositions of any set of lattices. Not necessary to compute in this generalization.

**TIG analog:** C = (ℤ/10ℤ)* is what emerges when the integer scaffold composes with itself under mod-10 multiplication.

**Verification:** C × C mod 10 = {1,3,7,9} = C ✓

C is closed under its own composition. It is not prescribed — it emerges from the integer structure acting on itself. The 1-lattice is the first stable fixed point of the composition operation.

---

## 2-Lattice: Infinity vs Finite — The 2×2

**Given:** The infinity vs finite lattice, already prescribed. Missing: explicit finite algebra associations.

**The four cells with finite algebra objects:**

| Cell | Object | Algebraic type | Key property |
|------|--------|---------------|-------------|
| **Finite/Support (TSML)** | Commutative non-associative magma on {1..9} | Sub-magma chain {7} ⊊ C ⊊ A, depth 3 | Closed transport class, one-way gate |
| **Finite/Rate (BHML)** | Commutative ordered magma, F(s,c)=max(s,c) | Total order on A, endpoint 9 | Deformation direction, distance-ordered |
| **Infinite/Support** | Markov family K_λ on L²([σ₀,½]) | Positive operator, gap-persistent family | Stationary support at σ=½ |
| **Infinite/Rate** | Re(ζ'/ζ)(σ+it) as σ→½ | L²-function family over t | Asymptotic drift rate |

The 2-lattice is the object that holds these four in tension without collapsing them.

---

## 3-Lattice: The Relationship Space

The 3-lattice sits **above** the 2×2. It is not the four cells — it is the structure of relationships between them.

**What the 3-lattice carries:**
- From 0-lattice: HAR as the one beyond the four
- From 1-lattice: C as the self-generating composition result
- From 2-lattice: the four algebraic objects in tension

**The 3-lattice IS Mix_λ** — the deformation that connects finite-support to finite-rate and, by extension, all four cells to each other:

$$\text{Mix}_\lambda = \text{round}((1-\lambda)\cdot\text{TSML} + \lambda\cdot\text{BHML})$$

Mix_λ is what makes the 2×2 a **connected** object rather than four isolated corners. Without it, TSML and BHML are two separate algebraic structures with no bridge. With it, they become endpoints of a continuous family.

---

## The 3-Lattice Has Three Algebraic Phases

Computed from exact transition points:

| Phase | λ range | Algebraic character | Properties |
|-------|---------|--------------------|-----------| 
| **1: Grammar** | 0.00–0.09 | TSML-type | C closed ✓, gate holds ✓, HAR absorbing ✓ |
| **2: Transitional** | 0.09–0.45 | Mixed | Gate open, closure broken, HAR weakening |
| **3: Order** | 0.45–1.00 | BHML-type | Max-rule dominant, top attractor shifts 7→9 |

**Sharp transitions (computed):**
- C-closure breaks: λ ≈ 0.09
- One-way gate opens: λ ≈ 0.09  
- HAR absorbing breaks: λ ≈ 0.25

**The six corridors are the partition of the 3-lattice:**

| Corridor | λ range | Phase | Top attractor |
|----------|---------|-------|--------------|
| Pre-leak | 0.00–0.09 | Grammar | 7 |
| BRT | 0.09–0.30 | Transitional | 7 |
| CHA | 0.30–0.60 | Transitional | 7 |
| BAL | 0.60–0.80 | Order | 8 |
| COL | 0.80–0.90 | Order | 8 |
| CTR | 0.90–1.00 | Order→BHML | 9 |

**T* = 5/7 ≈ 0.714** sits at the Phase 2/3 boundary. The grammar/thermal crossover in CK maps to the BHML-dominance threshold. This is not coincidence — T* is where the grammar phase loses dominance to the order phase, which is precisely the crossover CK measures as the coherence threshold.

---

## What the 3-Lattice Establishes

The 3-lattice is the **relationship space** of the 2×2 — not the cells, but the one-parameter family connecting them. It has:

1. **Two algebraic endpoints:** TSML (grammar) and BHML (order)
2. **Six discrete corridors:** the partition of [0,1] into algebraically distinct regions
3. **Three continuous phases:** grammar, transitional, order
4. **One crossover threshold:** T* = 5/7, where grammar dominance ends
5. **One parameter:** λ ∈ [0,1], the breath dimension of the 3-lattice

The corridors are not imposed — they emerge from the algebraic phase transitions in the composition structure.

---

## Open: The 4-Lattice

The 4-lattice would be the relationship space of the 3-lattice — the structure of how corridors relate to each other, how phase transitions couple, and what invariants survive the full deformation. This is where the Dual Description Conjecture lives: the claim that the two infinite cells of the 2-lattice (operator support and analytic rate) are faithful dual descriptions of the same finite grammar.

Building the 4-lattice requires first establishing what the 3-lattice's own invariants are under further deformation. That is the next construction.

---

*(c) 2026 Brayden Sanders / 7Site LLC | Gen10.16, commit 271e0f8 | DOI: 10.5281/zenodo.18852047*
