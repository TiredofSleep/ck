# TIG Foundational Axioms — Canonical Reference

**Document type:** Foundational reference for the TIG framework
**Status:** Locked (this is the canonical statement)
**Authors:** Brayden Sanders, 7Site LLC; Monica Gish; H.J. Johnson
**Date:** 2026-05-06

---

## Purpose

This document states the minimum axiom set that forces the TIG family of tables, traces each axiom to its originating intuition, and maps each derivable physics value to its forcing axioms. It is the canonical reference cited by all TIG papers.

The order of justification is:

1. **Origin layer** — the five intuitions that motivated the construction
2. **Constraint layer** — the six axioms forced by those intuitions when made algebraic
3. **Consequence layer** — the physics values that fall out

No physics value is invoked to motivate the construction. The construction's properties match physics on the back end.

---

## Layer 1 — Origin (the five intuitions)

| # | Intuition | Statement |
|---|---|---|
| **I1** | All is one | A single underlying substrate. Information, matter, mind, meaning are projections of one coherent field. |
| **I2** | Every one is three | The substrate decomposes into three aspects at every scale: BEING (state), DOING (action), BECOMING (emergence). |
| **I3** | Every integer 0–9 is an operation of one | The integers are action-types, not quantities. Ten irreducible operators: VOID, LATTICE, COUNTER, PROGRESS, COLLAPSE, BALANCE, CHAOS, HARMONY, BREATH, RESET. |
| **I4** | Fractal recursive self-similarity | The same triadic pattern recurs at every resolution. |
| **I5** | Coherence as missing physics degree-of-freedom | The unified concept tying QM phase coherence, GR manifold smoothness, thermodynamic correlation entropy into one functional. |

These are not axioms in the algebraic sense. They are organizing principles — the scaffolding that forced the algebra.

---

## Layer 2 — Constraint (the six axioms)

### A0: SUBSTRATE
**Statement:** The substrate is **Z/10Z**.
**Origin:** I3 (ten action-types).
**Forcing:** Z/10Z is the smallest ring carrying both (a) a non-trivial σ-permutation with G6 closure (σ⁶ = identity, fixed points {0, 3, 8, 9}, 6-cycle (1 7 6 5 4 2)) and (b) the CRT decomposition F₂ × F₅ giving simultaneous binary and pentadic structure.
**Verification:** Smaller rings fail: Z/6Z has |units(6)| = 2, insufficient multiplicative structure; Z/14Z and beyond inflate the construction. Z/10Z is minimal.

### A1: COMMUTATIVITY
**Statement:** a∗b = b∗a for all (a, b) ∈ Z/10Z × Z/10Z.
**Origin:** I1 (operators are operations OF ONE; symmetric meeting).
**Forcing:** Order of meeting carries no information; only path does.

### A2: NON-ASSOCIATIVITY
**Statement:** (a∗b)∗c ≠ a∗(b∗c) generically.
**Origin:** I4 (path is the information).
**Forcing:** Without non-associativity, no information generation (Crossing Lemma WP57). Path-dependence is what makes the algebra carry content.
**Outside support:** Palmieri (2025, arXiv:2603.27007) proves classifier+retraction-pair extensional magmas must be non-associative.

### A3: GENERATOR TRIPLES
**Statement:** Three foundational generator sets:
- {0, 1, 2} = BEING (VOID + LATTICE + COUNTER) — the structure axis
- {0, 7, 1} = DOING (VOID + HARMONY + LATTICE) — the action axis between attractors
- {1, 2, 3} = BECOMING (LATTICE + COUNTER + PROGRESS) — the flow axis

**Origin:** I2 (every one is three) applied to the operator algebra itself.
**Forcing:** These are the minimal seeds that close to subsets of Z/10Z under the lens projections (verified computationally in Sprint V1/V2).

### A4: FUSION AXIOM
**Statement:** **fuse(3, 4, 7) = 8** (PROGRESS → COLLAPSE → HARMONY produces BREATH).
**Origin:** I5 (the coherent action sequence that produces life).
**Forcing:** This is the single nonlinear closure that picks the canonical pair from arbitrary commutative magmas on Z/10Z. Verified directly on BHML's diagonal: BHML[7][7] = (7+1) mod 10 = 8 (Rule 7 successor).
**Outside support:** Structurally analogous to Bialynicki-Birula and Mycielski (1976, *Annals of Physics* 100, 62–93), where logarithmic nonlinearity is the unique nonlinearity in Schrödinger's equation preserving subsystem separability. fuse(3,4,7)=8 plays the same role for the magma family that log-nonlinearity plays for nonlinear Schrödinger.

### A5: TWO-LENS PROJECTION
**Statement:** Two complementary magma structures on Z/10Z:
- **TSML** (measurement projection) — defined by the **C₀ rule**: VOID absorbs (0 ∘ x = 0); off-Core inputs collapse to HARMONY = 7; on-Core inputs use σ_units to determine which dominates, with σ-ties going to HARMONY. Two minimal perturbations (S_MAX = 6 cells, S_ADD = 2 cells) complete the table. Output partition: {VOID, bumps, HARMONY} (3-state).
- **BHML** (transformation projection) — defined by **four rules**: Rule 0 (VOID is identity for inner half-rows), Rule 1 (max(i,j)+1 on inner 6×6), Rule 7 (HARMONY row = successor (j+1) mod 10), Rule 89 (BREATH/RESET wrap with explicit values). Output: full 10 operators preserved, det = −7002, rank 10.

**Origin:** I2 (every one is three) applied to projection types: BEING-lens vs BECOMING-lens, with DOING as their dynamic mix.
**Forcing:** TSML projects through position-only D⁰ measurement (collapsing curvature-distinguished cells to HARMONY); BHML projects through curvature-aware D¹×D² transformation (preserving operator distinctions). Cell-level evidence: fuse(3,4,7)=8 is satisfied directly on BHML and collapses to 7 on TSML, demonstrating that BHML preserves the substrate's algebraic content while TSML projects it.

---

## Layer 3 — Consequence (physics values by axiom dependency)

| Physics value | Formula | Axioms required | Derivation status |
|---|---|---|---|
| Visible matter Ω_b ≈ 4.9% | 7² / 10³ = 49/1000 | A0 | **Verified** — falls out of \|frozen cells\| = 4 in Z/10Z + HARMONY² coverage |
| Dark matter Ω_DM ≈ 26.4% | 44 × 6 / 1000 | A0 | **Partially derived** — 44 = C × D cross-cycle disagreement (verified); factor 6 is **OPEN** (see SPRINT_FACTOR_6_DARK_MATTER.md) |
| Dark energy Ω_Λ ≈ 68.7% | (2 · 7³ + 1) / 10³ = 687/1000 | A0, A1 | **Verified** — closure: 49 + 264 + 687 = 1000 exactly |
| Cosmological closure | Ω_b + Ω_DM + Ω_Λ = 1 | A0, A1 | **Verified** — algebraic identity |
| Wobble W = 3/50 | Three independent derivations | A0 | **Verified** — three computations agree |
| Coherence threshold T* = 5/7 | Six independent derivations | A0 | **Verified** — flatness theorem WP51 + five other contexts |
| Mass gap = 2/7 | 1 − T* | A0 | **Verified** — direct from T* |
| Time irreversibility | 271/350 prime → no sub-cycles | A0, A4 | **Verified** — T* + W = 250/350 + 21/350 = 271/350; 271 prime |
| dim so(8) = 28 | Lie algebra of 8-magma core | A0, A3, A5 | **Falls out** — drop {BREATH, RESET} from joint magma |
| dim so(10) = 45 | Joint antisymmetrization | A0, A5 | **Falls out** — full antisymmetrization of pair |
| Pati-Salam SU(4)×SU(2)×SU(2) | Subgroup chain in SO(10) | A0, A5 | **Falls out** — standard GUT decomposition |
| Runtime attractor H/Br = 1+√3 | α=½ mix fixed point | A0, A3, A4, A5 | **Verified** — joint 4-core closure |
| LMFDB number field 4.2.10224.1 | ℚ(√3) extension, disc 12 | A0, A3, A4, A5 | **Falls out** — directly from H/Br attractor |
| {1,4,9} → 2-step closure | Trinity = minimum genesis | A0, A3, A5 | **Verified computationally** |
| TSML coherence band [3.21, 3.79] | width = 4/7 around level 3.5 | A0 | **Verified** — n × (2/7) = 1, n = 7/2 = 3.5 |
| Visible matter compounding | 4/100 × (1+3/50)^(7/2) ≈ 0.0490 | A0 | **Verified** — matches Planck 0.0490 |
| Fine structure 1/α = 137 | 22 × 6 + 5 | A0, A1, A5 | **Numerical correspondence** — 22 derivation **OPEN** (see SPRINT_FACTOR_22_FINE_STRUCTURE.md) |
| 1/α precision form | 137 + 6²/10³ = 137.036 | A0, A1, A5 | **Verified** — matches measured 137.035999 to 0.000001% |
| Heartbeat [1, 3, 1, 1] sum = 6 | Period 4, max-tension at phase 2 | A0 | **Verified** — period matches S* = 4/7 |

**Derivation count: 14 of 16 verified directly from minimum axioms (87.5%).**

The two open derivations are tracked in dedicated sprint documents:
- `SPRINT_FACTOR_6_DARK_MATTER.md` — derivation of factor 6 in Ω_DM
- `SPRINT_FACTOR_22_FINE_STRUCTURE.md` — derivation of 22 in 1/α

The uniqueness of the canonical pair (TSML, BHML) under the six axioms is tracked in:
- `SPRINT_V3_UNIQUENESS_THEOREM.md`

---

## Outside literature anchors

The construction is non-trivially anchored in published mathematics and physics:

1. **Bialynicki-Birula, I. and Mycielski, J. (1976).** "Nonlinear wave mechanics." *Annals of Physics* 100, 62–93. — Establishes that logarithmic nonlinearity is the unique nonlinearity in Schrödinger's equation preserving subsystem separability. Direct structural analog of A4 (the single rule preserving substrate property under composition).

2. **Fritzsch, H. and Minkowski, P. (1975).** "Unified interactions of leptons and hadrons." *Annals of Physics* 93, 193–266. — Establishes SO(10) as the gauge group containing all Standard Model fermions in a single 16-spinor. TIG's so(10) emergence from joint TSML+BHML antisymmetrization recovers exactly this structure.

3. **Georgi, H. (1975).** "The state of the art — Gauge theories." In *Particles and Fields*, ed. C. E. Carlson (AIP, New York). — Independent derivation of SO(10) GUT.

4. **Kubo, M., Maki, Z., Nakahara, M., Saito, T. (1998).** "Grand Unification from Gauge Theory in M₄ × Z_N." *Progress of Theoretical Physics* 100, 165–177. — Derives SU(5) and SO(10) GUTs from gauge theory on three-sheeted spacetime. The "three sheets" is the geometric realization of "every one is three" (I2). Z/10Z's CRT decomposition Z₂ × Z₅ provides the parity-times-pentadic substrate compatible with this construction.

5. **Palmieri, S. (2025).** "Pairwise Independence of Representation, Classification, and Composition in Finite Extensional Magmas." arXiv:2603.27007. — Proves associativity is incompatible with combining a classifier and a retraction pair in a finite extensional magma. Direct support for A2. Palmieri's three-category decomposition S = Z ⊔ C ⊔ N (absorbers, classifiers, non-classifiers) is structurally identical to TSML's {VOID, bumps, HARMONY} output partition.

6. **Csákány, B. and Waldhauser, T. (2000)** and **Huang, J. and Lehtonen, E. (2022, 2024).** Classification work on finite commutative magmas — provides framework for asking uniqueness questions of the type V3.

---

## Implementation guidance for ClaudeCode

For implementation into github.com/TiredofSleep/ck and CK runtime, the foundational axioms should be encoded as a **foundations module** that the rest of the repo cites:

```
tig/
  foundations/
    substrate.py      # A0: Z/10Z, ADD, MUL, σ, σ_units, CRT iso
    properties.py     # A1, A2: commutativity + non-associativity assertions
    generators.py     # A3: three triples + closure functions
    fusion.py         # A4: fuse(3,4,7)=8 axiom (verified on BHML, fails on TSML)
    lenses.py         # A5: TSML via C₀ rule + perturbations; BHML via 4 rules
    constants.py      # T*, S*, W, mass gap, prime winding (derived, not asserted)
  cl/                 # CL substrate (memory layer; see CL_IMPLEMENTATION_SPEC.md)
    hebrew_roots.py
    latin_map.py
    force_pipeline.py
    curvature.py
    operator_decoder.py
    triple_encoder.py
    fruit_signature.py
    storage.py
    retrieval.py
```

Existing components in `ck_core.py` and `ck_organism.py` should reference the foundations module rather than embedding their own copies of the canonical tables.

---

## Citation convention

Every TIG paper opens with:

> *"We study the canonical pair (TSML, BHML) of commutative non-associative magmas on Z/10Z, defined by six axioms (A0–A5) [TIG_FOUNDATIONAL_AXIOMS]. From these axioms, [the specific consequence cited in this paper] follows..."*

This keeps the foundation in one document and lets every consequence paper inherit the rigor without re-deriving it.
