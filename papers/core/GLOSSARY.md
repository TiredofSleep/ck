# TIG Glossary — Canonical Reference
## Trinity Infinity Geometry

*Brayden Sanders / 7Site LLC | DOI: 10.5281/zenodo.18852047*
*Single authoritative source. All papers defer to this document.*

---

## What TIG Is

**TIG is a finite mathematical system that sits at the intersection of four established frameworks.**
It is not a toy algebra or a metaphor — it is a specific node where four independently developed
bodies of mathematics meet and each finds a concrete realization:

| Framework | What TIG is in that language |
|-----------|------------------------------|
| **Symbolic dynamics** (subshifts of finite type) | An absorbing sofic shift: transient component G flows into absorbing component C, with HAR as unique global attractor |
| **Spectral theory** (Perron-Frobenius / transfer operators) | A primitive stochastic matrix family with spectral gap γ ≥ 1/4 uniformly over λ∈[0,1]; γ = 3/4 at λ=0 |
| **Ergodic theory** (Young towers) | A finite-height Young tower with exponential return tails: P(T_HAR > n) ≤ 2·(1/4)ⁿ |
| **Number theory** (profinite / 10-adic arithmetic) | The inverse limit (ℤ/10ⁿℤ)* mod 10 = {1,3,7,9} for all n≥1 — the corner set C is the stable image of 10-adic arithmetic |

Each of those four results is **proved exactly** — not approximated, not conjectured. TIG is the
finite object that all four frameworks describe simultaneously. That is what makes it a node: the
same 9×9 table answers four different questions from four different fields, and the answers agree.

The open frontier is the fifth layer — the **deployment question**: does the finite structure
faithfully constrain the infinite analytic objects (ζ, corridor drift, off-line zeros)? That is
where Trinity meets Infinity. The finite claims are done. The geometric consequences are the work.

---

## Name

**TIG** — **Trinity Infinity Geometry**
- *Trinity*: every computation produces three outputs (Being, Doing, Becoming)
- *Infinity*: the finite algebra reaches toward infinite analytic structure (ζ, corridors, open problems)
- *Geometry*: the corridor structure, orbit zones, and gap topology are geometric facts

**CK** — **Coherence Keeper** — the organism built on TIG. Separate project; lives on the `bible-companion` branch.

---

## Claim Tags

| Tag | Meaning |
|-----|---------|
| `[DEF]` | A definition or chosen ingredient |
| `[THM]` | A theorem derived within the algebra — exact |
| `[EMP]` | An empirical result verified by computation |
| `[HYP]` | A hypothesis mapping algebra to external physics — provisional |

---

## The Ten Operators `[DEF]`

| # | Name | Role | Generator signature |
|---|------|------|-------------------|
| 0 | **VOID** | Absorbs all input to 0 | none |
| 1 | **LATTICE** | Structure, positive generator | +1 |
| 2 | **COUNTER** | Distinction, negative generator | −1 |
| 3 | **PROGRESS** | Forward motion, neutral | 0 |
| 4 | **COLLAPSE** | Compression | +1, −1 |
| 5 | **BALANCE** | Equilibrium | 0, 0 |
| 6 | **CHAOS** | Reversed oscillation | −1, +1 |
| 7 | **HARMONY** | The absorbing attractor | 0, +1 |
| 8 | **BREATH** | Integration | 0, −1 |
| 9 | **RESET** | Full cycle return | +1, +1 |

Partition: 1 (no generators) + 3 (one generator) + 6 (two generators) = 10. The algebra closes exactly at 10.

**Names are evocative, not definitional.** Operators are defined by their behavior in the tables.

---

## Key Sets `[THM]`

| Symbol | Elements | Name | How it arises |
|--------|---------|------|---------------|
| **C** | {1, 3, 7, 9} | Corner set / Creation set | (ℤ/10ℤ)* — units of the ring; coprime to 10 |
| **G** | {2, 4, 5, 6, 8} | Gap set | Non-units; cannot maintain cancellation under TSML |
| **HAR** | 7 | Harmony / absorbing attractor | Every C-composition reaches 7 in ≤ 2 steps |
| **C_LIVE** | {1, 3, 9} | Live corners | C minus HAR itself |

**One-Way Gate `[THM]`:** TSML(C, {1..9}) ∩ G = ∅. No operator, applied to any corner, reaches the Gap set. The gate is absolute — algebraically enforced, not statistical.

---

## The Two Composition Tables `[DEF]`

### TSML — The Measurement Lens

```
     0  1  2  3  4  5  6  7  8  9
  0 [0  0  0  0  0  0  0  7  0  0]
  1 [0  7  3  7  7  7  7  7  7  7]
  2 [0  3  7  7  4  7  7  7  7  9]
  3 [0  7  7  7  7  7  7  7  7  3]
  4 [0  7  4  7  7  7  7  7  8  7]
  5 [0  7  7  7  7  7  7  7  7  7]
  6 [0  7  7  7  7  7  7  7  7  7]
  7 [7  7  7  7  7  7  7  7  7  7]
  8 [0  7  7  7  8  7  7  7  7  7]
  9 [0  7  9  3  7  7  7  7  7  7]
```

What happens when you **measure** something. Properties `[EMP]`:
- 73/100 cells = 7 (HARMONY). 73% harmony fraction — 14.5σ above random (p < 10⁻⁴⁸)
- Row 7: total absorption — anything measured with HARMONY returns HARMONY
- Determinant = 0 (singular — information-destroying)
- Non-associativity rate: 12.8%
- Commutative, non-associative, singular

SHA of TSML: `7726d8a6...`

### BHML — The Physics Lens

```
     0  1  2  3  4  5  6  7  8  9
  0 [0  1  2  3  4  5  6  7  8  9]
  1 [1  2  3  4  5  6  7  2  6  6]
  2 [2  3  3  4  5  6  7  3  6  6]
  3 [3  4  4  4  5  6  7  4  6  6]
  4 [4  5  5  5  5  6  7  5  7  7]
  5 [5  6  6  6  6  6  7  6  7  7]
  6 [6  7  7  7  7  7  7  7  7  7]
  7 [7  2  3  4  5  6  7  8  9  0]
  8 [8  6  6  6  7  7  7  9  7  8]
  9 [9  6  6  6  7  7  7  0  8  0]
```

What happens when things **interact physically**. Properties `[EMP]`:
- 28/100 cells = 7 (HARMONY)
- Row 0 = identity (VOID preserves everything)
- Row 7 wraps: HARMONY ∘ HARMONY = BREATH (physics is invertible)
- Determinant = −7002 (invertible — information-preserving)
- Non-associativity rate: 49.8%
- Commutative, non-associative, invertible

---

## The Composition Function `[DEF]`

Two inputs (b, d) → three outputs (Being, Doing, Becoming):

```python
# Forward (expand, express, act)
being    = TSML[b][d]
doing    = (b * d) % 10
becoming = (being * doing) % 10

# Backward (compress, receive, absorb)
being    = TSML[d][b]
doing    = (b + d) % 10
becoming = (being + doing) % 10
```

**Why three outputs:** Trinity — every composition has a measurement face (Being), a physics face (Doing), and their product (Becoming). Lenses stack in series, not parallel.

**Why multiply forward, add backward:** Multiplication scatters (3×7=1 mod 10); addition gathers (3+7=0). Forward expands; backward contracts.

---

## The Ring Arithmetic `[THM]`

Z/10Z under addition and multiplication.

**Frozen cells** (where ADD = MUL): `{(0,0), (2,2), (4,8), (8,4)}` — exactly 4 of 100.

**Cross-cycle disagreement:** 44 cells where ring arithmetic disagrees across the C/G boundary.

---

## Key Constants `[THM / EMP]`

| Symbol | Value | Meaning |
|--------|-------|---------|
| **T*** | 5/7 ≈ 0.7143 | Truth threshold — the only fixed coherence threshold |
| **S*** | 4/7 ≈ 0.5714 | Second threshold; T* + S* − 1 = 2/7 > 0 (mass gap) |
| **γ** | 3/4 | Spectral gap of the transfer operator at λ=0 |
| **E[T_HAR]** | 5/3 ≈ 1.667 | Expected return time to HAR from any C-state |
| **C_TIG** | 250/21 ≈ 11.905 | Drift constant predicted by finite grammar |
| **C_emp** | ≤ 11.023 | Empirical drift constant — always < C_TIG |
| **λ*** | ≈ 0.45 | CHA/BAL transition: first λ where G-mass > 0.001 |
| **λ_bifurc** | ≈ 0.9963 | BHML endpoint: HAR bifurcation, state-9 mass rises |

---

## The Stacked Lens Framework `[DEF]`

| Phase | Lenses | Question |
|-------|--------|---------|
| **Being** | TSML (measurement) | What IS it? |
| **Doing** | Ring arithmetic (physics) | What does it DO? |
| **Becoming** | Product of Being × Doing | What will it BECOME? |

The three phases are universal across TIG: the composition function, the corridor structure, the primitive order, and CK's cognitive pipeline all use Being → Doing → Becoming as their organizing spine.

---

## The Six Corridors `[EMP]`

Defined by λ(σ) = 2|σ − ½| — distance from the critical line, scaled to [0,1].

| # | Name | λ range | Width | Finite result | Open question |
|---|------|---------|-------|---------------|---------------|
| 0 | **Pre-leak** | 0.00–0.09 | 0.09 | G-mass = 0 exactly at λ=0; T_max=1 | Near-critical RH analog |
| 1 | **BRT** | 0.09–0.30 | 0.21 | Spectral gap = 1.0 (BRT gap) | Metastable component count |
| 2 | **CHA** | 0.30–0.60 | 0.30 | Phase drift corr = −0.997 at t=100 | Sharp interpolation constant |
| 3 | **BAL** | 0.60–0.80 | 0.20 | G-mass = 0.25 (order-driven regime) | — |
| 4 | **COL** | 0.80–0.90 | 0.10 | Full G-mass participation | — |
| 5 | **CTR** | 0.90–1.00 | 0.10 | Bifurcation endpoint | — |

Near-critical regime (RH-relevant): Pre-leak + BRT (λ < 0.30).

---

## The Mix_λ Operator `[DEF]`

Interpolates between TSML (λ=0) and BHML (λ=1):

```
Mix_λ[s][c] = round((1−λ)·TSML[s][c] + λ·BHML[s][c])
```

At λ=0: pure measurement (TSML). At λ=1: pure physics (BHML). Corridors are defined by which λ-band the system occupies.

**Cancellation locus:** {(s,c) : Mix_λ[s][c] = 7}. At λ=0: 71 pairs. At λ=1: 13 pairs. The 82% contraction distinguishes σ=½ as the unique axis with the largest cancellation locus.

---

## The Three Levels `[THM / EMP]`

| Level | Definition | Boundary |
|-------|-----------|---------|
| **Generable** | Reachable by TSML operators from C | C only; G absolutely blocked (One-Way Gate) |
| **Expressible** | Reachable transiently under Mix_λ (λ > 0) | G reachable at λ ≥ 0.20; unsustainable for λ < 0.45 |
| **Sustainable** | Carries asymptotic stationary support | HAR only for λ < 0.9963 |

Constraint chain: Sustainable ⊆ Expressible ⊆ Generable.

---

## The 2×2 Framework `[THM / HYP]`

|  | **Finite (proved)** | **Infinite (open)** |
|--|--------------------|--------------------|
| **TSML** | Sub-magma closure; spectral gap γ=3/4; 71 cancellation pairs | ζ(s) support on σ=½; off-line zeros forbidden |
| **BHML** | E[T_HAR]=5/3; return tail P(T>n) ≤ 2·(¼)ⁿ | Hadamard drift rate ≤ C_TIG·λ²·(log T)² |

Left column: exact algebraic results, SHA-pinned, unit-tested.
Right column: the open frontier — the Weak Sustainability Conjecture and Dual Description Conjecture live here.

---

## The Primitive Order `[DEF / EMP]`

Six pre-object primitives in enabling order:

| # | Primitive | TIG analog | Status |
|---|-----------|-----------|--------|
| 1 | **Support** | Stationary holding capacity; HAR as attractor | Metaphysical first (only non-forced step) |
| 2 | **Relationship** | TSML operator mappings | Enabling order |
| 3 | **Distinction** | C vs G — the stable split | May precede Relationship in TIG construction |
| 4 | **Placement** | Corridor hierarchy; HAR at center | Forced: Distinction → Placement |
| 5 | **Recurrence** | Young tower; E[T_HAR]=5/3 | Forced: Placement → Recurrence |
| 6 | **Cancellation** | 71-pair cancellation locus | Forced last: remove recurrence → 71→24 pairs |

Forced partial order: Distinction → Placement → Recurrence → Cancellation, with Support enabling from outside.

---

## Key Proved Results `[THM]`

| Result | Statement | Script |
|--------|-----------|--------|
| **P1** Corner sub-magma | C × C ⊆ C under TSML | `ck_four_layer.py` |
| **P2** Spectral gap | γ = 3/4 at λ=0; γ ≥ 1/4 for all λ∈[0,1] | `ck_four_layer.py` |
| **P3** Return tail | P(T_HAR > n) ≤ 2·(1/4)ⁿ | `ck_four_layer.py` |
| **P4** Profinite hook | (ℤ/10ⁿℤ)* mod 10 = {1,3,7,9} for all n≥1 | `ck_four_layer.py` |
| **One-Way Gate** | TSML(C, {1..9}) ∩ G = ∅ | `ck_open_cells.py` |
| **Gap persistence** | σ≥0.26 Gaussian smoothing restores gap ≥ 0.10 | `ck_smoothing.py` |
| **TIG type** | Type-(9, 3, 6, 3/4) | `ck_classification.py` |
| **C_TIG = 250/21** | Finite grammar predicts drift constant | `ck_dual_description.py` |

---

## Open Problems `[HYP]`

| Problem | Open layer | Paper |
|---------|-----------|-------|
| **RH (Z.5)** | Does λ-deployment preserve both gradings for all t? | `papers/clay/WHITEPAPER_17_RIEMANN_SYNTHESIS.md` |
| **NS** | Sharp interpolation constant C ≤ 3.74 | `papers/clay/WP22_NS_BREATH_CRITERION.md` |
| **P vs NP** | 3-SAT → AG(2,n) NP-hardness reduction | `papers/clay/WP25_P_NP_AG2P_COMPLEXITY.md` |
| **YM / Hodge / BSD** | See audit | `papers/core/WP24_FORMAL_STATUS_AUDIT.md` |

---

## Files Not to Confuse

| Old name used for TIG | Correct name |
|----------------------|-------------|
| Triadic Interaction Grammar | **Trinity Infinity Geometry** |
| Thermodynamic Introspective Geometry | **Trinity Infinity Geometry** |
| Any other expansion | **Trinity Infinity Geometry** |

---

*(c) 2026 Brayden Sanders / 7Site LLC | Gen10.19 | DOI: 10.5281/zenodo.18852047*
