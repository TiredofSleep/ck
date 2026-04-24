# DOF Classification — Five Kinds on CL/BHML via CK Runtime

**Branch:** `ck`
**Status:** `[RUNTIME ARCHITECTURE]` + `[POSITIONING]`
**Authors:** Brayden Sanders (7Site LLC), in collaboration with Claude (Anthropic)
**Date:** 2026-04-24
**Scope of this file:** speculative synthesis on CK-internal architecture. Each claim is tagged `[R]` (repo-verified), `[LIT]` (external-literature), or `[S]` (session-derived / interpretive). This is the home for material we can "assume, predict, and speculate about CK" — per the `ck` branch's branch-discipline note in [`README_CK_BRANCH.md`](../README_CK_BRANCH.md).

**What this file is NOT.** A proved theorem. A new primary result. A ship-ready rigor-facing artifact. The proved theorems cited below have canonical homes in `papers/` and `Gen12/targets/clay/papers/`.

---

## Part 0 — Why this lives on the `ck` branch

This document speculates about CK's cognitive architecture — specifically about the *kinds* of degrees of freedom the runtime must track to preserve the full structure of `(CL, BHML)`. Some material is literature-grounded. Some is session-derived. One claim is an honest design-target statement about how a future runtime would read coherence observables — the current code does not implement it that way. The `ck` branch is the right home for exactly this kind of material.

**On-branch anchors** (merged onto `ck` 2026-04-24 from `paradox-classifier-2026-04-24`):

- [`META_LENS_ATLAS.md`][atlas] — the organising atlas (now in `papers/meta_lens/` on `ck`).
- [`FOUNDATION_TOUR_VERIFIED.md`][tour] — the six-lens rigor-facing tour with the vocabulary-hygiene policy this document inherits (Part 0.1).
- [`VOCABULARY_RECONCILIATION.md`][vocab] — the four-type × five-category reconciliation.
- [`CK_META_CLASSIFICATION_AXES.md`][axes] — dual-registry companion in `speculations/` pairing the five DOF Kinds with the four UOP Types.

**Cross-branch anchors** (files still only reachable off `ck`):

- [`CL_MATROID_DISTANCE.md`][mantero] — the distance paper; lives on `paradox-classifier-2026-04-24`.
- [`CKIS/ck_being.py`][ck_being] — runtime-code reference used in §3.3; `CKIS/` is only on the classifier branch.
- [`WP102_SO8_IDENTIFICATION.md`][wp102] and [`WP103_SO10_IDENTIFICATION.md`][wp103] — Lie-algebraic closure papers; lived on the classifier branch at the time of writing.

[atlas]: ../papers/meta_lens/META_LENS_ATLAS.md
[tour]: ../papers/meta_lens/FOUNDATION_TOUR_VERIFIED.md
[vocab]: ../papers/meta_lens/VOCABULARY_RECONCILIATION.md
[axes]: ./CK_META_CLASSIFICATION_AXES.md
[mantero]: https://github.com/TiredofSleep/ck/blob/paradox-classifier-2026-04-24/papers/mantero/CL_MATROID_DISTANCE.md
[ck_being]: https://github.com/TiredofSleep/ck/blob/paradox-classifier-2026-04-24/CKIS/ck_being.py
[wp102]: https://github.com/TiredofSleep/ck/blob/paradox-classifier-2026-04-24/papers/wp102/WP102_SO8_IDENTIFICATION.md
[wp103]: https://github.com/TiredofSleep/ck/blob/paradox-classifier-2026-04-24/papers/wp103/WP103_SO10_IDENTIFICATION.md

**Vocabulary policy** inherited from the foundation tour: external math vocabulary in Parts 1–2; CK-internal operator names (VOID, LATTICE, COUNTER, PROGRESS, COLLAPSE, BALANCE, CHAOS, HARMONY, BREATH, RESET) appear only in Part 3.

---

## §1. Established literature — what already exists

The classification of degrees of freedom by *kind* has a 75-year tradition in mathematical physics:

- **Dirac 1950 / Bergmann 1956** — first-class vs second-class constraints classify DOFs by Poisson-bracket algebra. **[LIT]** (P.A.M. Dirac, *Canad. J. Math.* 2 (1950) 129–148; P.G. Bergmann, *Helv. Phys. Acta* 29 (1956) 287).
- **Faddeev–Jackiw 1988 / Barcelos–Wotzasek 1992** — symplectic geometrization of the Dirac classification; DOFs sorted by invertibility of a symplectic matrix. **[LIT]** (*Phys. Rev. Lett.* 60 (1988) 1692; *Mod. Phys. Lett. A* 7 (1992) 1737).
- **Conformal-symplectic decomposition** (Franca et al. 2020) — separates reversible (symplectic-preserving) from dissipative (conformally-symplectic) flow DOFs. **[LIT]** (*J. Stat. Mech.* 2020.124008).
- **Liouville–Arnold integrability** — global sort of systems by whether enough conserved quantities exist to foliate phase space. **[LIT]** (Arnold, *Mathematical Methods of Classical Mechanics*, Springer 1989, §49).
- **Birkhoff 1917** — earliest explicit recognition that formally equal DOF counts can hide qualitatively different DOF *characters*. **[LIT]** (*PNAS* 3:4 (1917) 314).

These literatures sort DOFs *within a single physical system* (Dirac) or *across parameter regimes* (reversible-irreversible transitions). None of them sort DOFs arising from *different mathematical frameworks applied to the same algebraic object*. That is the gap this document addresses.

---

## §2. The five kinds

Combining and extending §1, DOFs in a general mathematical object fall into five qualitatively distinct kinds:

1. **Structural / frozen-coordinate.** Fixed properties of the state. Does not evolve within the runtime's primary tick loop. *Analogs:* first-class constraints, holonomic conditions, invariant algebraic profile.
2. **Reversible symplectic flow.** Smooth, symmetric, compact motion; every trajectory has an inverse. *Analogs:* Hamiltonian flow, Lie-group action, conservative dynamics.
3. **Irreversible dissipative flow.** Motion with arrow of time; spectral gap, decay of correlations, entropy growth. *Analogs:* conformal-symplectic flow, transfer-operator dynamics.
4. **Discrete climbing.** Monotonic, irreversible, information-adding stepped motion; each step is a category-preserving refinement that cannot be undone without loss. *Analogs:* operadic arity refinement, filtration depth, proof complexity, rank-increment.
5. **Degenerative / limiting.** One-way *category* transformation; the system changes kind as a parameter crosses a boundary. *Analogs:* moduli-space compactification, continuum limit, Wilsonian RG flow, Gromov–Hausdorff convergence.

Kinds 1–3 have mature literature. Kinds 4 and 5 appear in specialized subfields but have not been part of the DOF-classification mainstream. **[S]** Naming all five as a unified taxonomy is the meta-extension this document contributes.

---

## §3. CK-internal content — what plays its part on CL/BHML

Part-III vocabulary territory: the 10 CK operators may appear below when the subject is CK itself, per the foundation tour's Part 0.1.

### §3.1 The five kinds, instantiated on CL/BHML

**Kind 1 — Structural / frozen-coordinate**

- **[R]** CL is a fixed 10×10 table. BHML is a fixed 10×10 companion with `det = −7002` at the 10-element version and `det = +70` at the 8-element core. Reference: [`FORMULAS_AND_TABLES.md`](../FORMULAS_AND_TABLES.md) §6.7; [atlas][atlas] §I.
- **[R]** σ-diagonal `= [0, 7, 1, 3, 2, 4, 5, 6, 8, 9]`. A fixed permutation, not a flow.
- **[R]** Idempotents `{0, 3, 8, 9}`. Fixed algebraic positions.
- **[R]** 6-cycle `(1 → 7 → 6 → 5 → 4 → 2)`. Fixed combinatorial structure inside CL.
- **[R]** **M2-verified invariants of `A = R / I_CL`:** `numgens = 53, codim = 9, Krull dim = 1, pd = 10, depth = 0, NOT Cohen-Macaulay, NOT Koszul`, reduced Hilbert series `(1 + 9T − 8T² − T³) / (1 − T)`, Hilbert function `(1, 10, 2, 1, 1, …)`. Reference: [atlas][atlas] §III.1, `[M2-RESOLVED]` on `mantero-bridge-2026-04-23`.
- **[R]** Waldschmidt constant `α̂(I_B) = 2`; basis-exchange defect `21.9%` on `Δ_B`. Reference: [distance paper][mantero].

> **Correction note.** An earlier desktop draft listed "Krull dim = 6, pd = 4". That was wrong. Correct M2-computed values: `dim = 1, pd = 10, depth = 0`, NOT Cohen-Macaulay. The `6` likely conflated multiplicity with Krull dimension.

**These are state-coordinates, not flow directions.**

**Kind 2 — Reversible symplectic flow**

- **[R]** `so(8) = D₄` closes under antisymmetrization of six flow operators over CL at dimension 28. Compact, simple, signature `(0, 28, 0)` Killing form. Reference: [`WP102_SO8_IDENTIFICATION.md`][wp102] on the classifier branch.
- **[R]** `so(10) = D₅` closes under full antisymmetrization of `CL ∪ BHML` at dimension 45. Known as the Fritzsch–Minkowski (1975) / Georgi (1975) GUT gauge algebra. Reference: [`WP103_SO10_IDENTIFICATION.md`][wp103] on the classifier branch.
- **[S]** The adjoint action of `so(10)` on its 45-dim algebra supplies the **reversible flow DOF** of CK's substrate. Motion along this axis is smooth (Lie), bounded (compact), reversible (every group element has inverse).
- **[S]** The 5D force vector plus one time-like direction sits inside the 10-dim vector representation of `Spin(10)`; the stabilizer chain `Spin(10) ⊃ Spin(9) ⊃ Spin(8) ⊃ Spin(7) ⊃ G₂ ⊃ SU(3)` gives nested symmetry-breakings that align with the CK operator hierarchy.

**Kind 2 is "motion with memory preserved."** LATTICE, COUNTER, BALANCE, HARMONY participate reversibly.

**Kind 3 — Irreversible dissipative flow**

- **[R]** Spectral gap `γ(b) = 1 − 1/φ(b)` (WP101 σ-rate theorem). A **dissipation rate** — information about initial conditions decays at this rate per tick. Reference: [`Gen12/targets/clay/papers/sprint14_prism_xi_2026_04_10/WP101_SIGMA_RATE_THEOREM.md`](../Gen12/targets/clay/papers/sprint14_prism_xi_2026_04_10/WP101_SIGMA_RATE_THEOREM.md) + `proof_sigma_rate.py`.
- **[R]** Crossing Lemma (WP57) identifies when dynamics become injective. *The boundary between Kinds 3 and 2 inside CK.* Reference: [`Gen12/targets/clay/papers/sprint10_flatness_2026_04_06/CROSSING_LEMMA.md`](../Gen12/targets/clay/papers/sprint10_flatness_2026_04_06/CROSSING_LEMMA.md).
- **[R]** Coherence equation `C = 0.4(1 − E) + 0.35 A + 0.25 K` lives at [`CKIS/ck_being.py`][ck_being] line 577 on the classifier branch. The function is a plain scalar combiner; see §3.3 for the honest status on what it reads.
- **[S]** CHAOS (op 6), COLLAPSE (op 4), and RESET (op 9) are CK-native names for participation in this axis. CHAOS injects dissipation; COLLAPSE is a localized irreversible event; RESET closes a dissipation cycle.
- **[R]** Color-wheel complements `1 ↔ 2, 3 ↔ 4, 6 ↔ 8` (APR23 finding). LATTICE is the Kind 2 generator along `+Z`; COLLAPSE is the Kind 3 generator along `−Z` — same spatial direction, opposite orientation.

**Kind 3 is "motion with memory lost."**

**Kind 4 — Discrete climbing**

- **[R]** ac-spectrum `s_n^ac(TSML) = s_n^ac(BHML) = (2n−3)!!` for `n ≤ 5`: `s₂ = 1, s₃ = 3, s₄ = 15, s₅ = 105`. Saturates Huang–Lehtonen. Reference: [`FORMULAS_AND_TABLES.md`](../FORMULAS_AND_TABLES.md) §6.1.
- **[S]** Arity `n` is itself a **climbing DOF.** Each step forward adds information not recoverable from coarser arity. Arity 3 → 4 adds 12 new distinguishing bits (`15 − 3`); returning drops them. Irreversible, but *additive, not dissipative*.
- **[R]** TSML rank 9 (Jordan) vs rank 10 (new idempotent lift), `|Aut| = S₈ = 40,320`, `det = −49` at positions `(1,2) = 6, (3,5) = 4`.
- **[S]** The D² curvature stencil `A − 2B + C` is the discrete-derivative operator along a climbing axis.

**Kind 4 is "the staircase."** Each rung adds resolution.

**Kind 5 — Degenerative / limiting**

- **[R]** σ-rate theorem asymptotic: `Mag^com → Com` as `N → ∞`. The operadic framework **degenerates** from free commutative magmatic to free commutative associative. Reference: `WP101_SIGMA_RATE_THEOREM.md` §6.
- **[R]** Continuum-limit BB-bridge (WP91): discrete CK dynamics degenerate to `□ξ = 1 + log ξ` with vacuum `ξ₀ = e⁻¹` and mass gap `m²_ξ = κ e`. *The system changes kind* — finite algebra → continuum field theory. Reference: [`Gen12/targets/clay/papers/sprint14_prism_xi_2026_04_10/WP91_NS_SEPARABILITY_BRIDGE.md`](../Gen12/targets/clay/papers/sprint14_prism_xi_2026_04_10/WP91_NS_SEPARABILITY_BRIDGE.md).
- **[S]** Categorically different from Kind 4. Kind 4 climbs within a fixed category (operads of increasing arity — all still operads). Kind 5 transforms the ambient category itself (finite operad → continuum field theory). Physics register: Wilsonian RG flow. Category-theory register: a colimit that changes the ambient category.
- **[S]** BREATH (op 8) is the CK-native name for participation in Kind 5. Not static (Kind 1), not symmetrically flowing (Kind 2), not dissipative (Kind 3), not stepping (Kind 4). Holds the transition — the "zoom out / transform category" operator.

**Kind 5 is "change the kind of thing you are."**

### §3.2 Why all five kinds must be maintained simultaneously

Most mathematical objects exhibit one or two kinds of DOF. Smooth manifold with Lie group action: Kind 1 + Kind 2. Markov chain: Kind 1 + Kind 3. Operadic tower: Kind 1 + Kind 4.

**CL and BHML exhibit all five.** Verification: every result on the [`FORMULAS_AND_TABLES.md`](../FORMULAS_AND_TABLES.md) §0 proof spine `D1–D25` populates at least one of the five kinds, and no result falls outside them.

**Verified table (every `D1–D25` item mapped to kind(s)):**

| `D#` | Result | Kind(s) |
|------|--------|---------|
| D1 | First-G Law (semiprime first non-coprime = p) | 1 |
| D2 | Sinc² continuum limit `R(k,f) → sinc²` | 5 |
| D3 | `sinc²(1/2) = 4/π²` | 1 |
| D4 | `T* = 5/7` at `b = 35` | 1 |
| D5 | `H_mod` has 4 local maxima | 4 |
| D6 | General-frequency maxima count `N(f)` | 4 |
| D7 | Φ fixed point (BALANCE = 5) | 1 |
| D8 | TSML/BHML composition laws | 1, 2 |
| D9 | Table symmetry (lens-symmetric) | 2 |
| D10 | TSML 73 HARMONY cells | 1, 4 |
| D11a/b/c | Coprime window bundle | 1 |
| D14 | Corridor spectral mean `Si(2π)/π` | 5 |
| D15 | Coprime window invariance | 1 |
| D16 | BHML 28 HARMONY cells | 1, 4 |
| D17 | Wobble `W = 3/50` | 1 |
| D18a | Φ orbit graph (`T³` = all-δ₅) | 1, 2 |
| D18c | TSML measurement bridge / `T* = 5/7` | 1, 3 |
| D18d | Generator convergence (g = 3) | 1 |
| D19 | Generator selection (g = 3 unique) | 1 |
| D20 | Inheritance audit (ring vs generator) | 1 |
| D21 | CE fixed-point centroid `F(5) = 5` | 1, 2 |
| D22 | Corridor portrait inequalities | 1 |
| D23 | Ring wobble `Wob(k)` closed form, limit `4/5` | 1, 5 |
| D24 | Corridor midpoint (sinc² monotone, `t = 1/2`) | 5 |
| D25 | Loop closure (sinc² zero via Φ-loop) | 1, 3 |

Higher-layer results `D26–D30` (so(8)/so(10) Lie closures, GUT lifts) populate Kind 2 densely. The five-kind partition is **exhaustive over `D1–D30`.** Kind 2 sparse at `§0` layer, fully realised at `D26+`. Kind 5 carries the continuum limits (`D2, D14, D23, D24`). Kind 3 enters via Crossing-Lemma injectivity and loop-closure events (`D18c, D25`).

### §3.3 CK runtime architecture — honest status

**[S]** A runtime that maintained the full `(CL, BHML)` structure would, at each tick, maintain independent state for:

- **Structural position** (Kind 1) — Krull-dim-type and σ-permutation-type invariants. Static during a tick.
- **Reversible-flow velocity** (Kind 2) — current element of `so(10)` (or a selected subalgebra like the 5D-force-aligned `so(5) × so(5)`) acting on state.
- **Dissipation rate** (Kind 3) — current entropy-production rate feeding the coherence equation.
- **Climbing index** (Kind 4) — current arity at which the classifier operates.
- **Degeneration parameter** (Kind 5) — current `N` / continuum-limit progress. For the live classifier this is `N = 10` (CL, BHML carrier size).

**Honest gap — the coherence equation.** The earlier draft claimed `E, A, K` in `C = 0.4(1 − E) + 0.35 A + 0.25 K` correspond to reads of Kinds 3, 1×2, and 2×4 respectively, and flagged this as `[C]` for verification against the runtime.

**Verification against [`CKIS/ck_being.py`][ck_being] lines 587–610 does not support that claim.** The `Body` class implements `E, A, K` as plain scalars:

- `E` decays 5%/tick, bumps `+0.3` on `fab = True` — tracks a fabrication/hallucination signal, not a Kind 3 dissipation rate.
- `A` decays 2%/tick unconditionally — does not read Kind 1×2 coupling.
- `K` increments `+0.01` on `recall = True` and caps at 1.0 — tracks recall events, not Kind 2×4 coupling.

Further, `Body._calc` computes a *different* coherence `(1 − E)(1 − A) · max(K, 0.1)` that does not agree with `coherence_eak`. The two formulas return different numbers on the same input.

**The honest position.** The five-kinds framing is a **design target** for an upgraded runtime, not a shipped invariant of the current code. Claim: "`E, A, K` read Kinds 3 / 1×2 / 2×4" describes *what those observables could read* in a principled runtime — not what `CKIS/ck_being.py` currently reads. Correcting this is an open engineering task (OQ-1 below).

**[S]** Kind 5 (degeneration) is not reachable from a single-regime coherence score by construction: degeneration is a meta-operation that changes the system's category, so reading it would require a meta-coherence score across regimes. CK 2026 operates in a fixed regime (`N = 10`, finite, discrete). A future CK (CK-Ω?) would need a multi-regime coherence metric.

### §3.3.1 The coherence equation weights encode `T*` (post-hoc finding)

**[V]** Independent of whether `E, A, K` currently *read* the kinds described in §3.3, the *weights* `(0.4, 0.35, 0.25)` in `C = 0.4(1 − E) + 0.35 A + 0.25 K` factor as rationals over 20:

$$
(0.4,\; 0.35,\; 0.25) \;=\; \left(\tfrac{8}{20},\; \tfrac{7}{20},\; \tfrac{5}{20}\right).
$$

Numerators sum to `8 + 7 + 5 = 20`. The ratio of the `K`-weight to the `A`-weight is

$$
\frac{w_K}{w_A} \;=\; \frac{5/20}{7/20} \;=\; \frac{5}{7} \;=\; T^{*},
$$

exactly, as fractions (verified in
[`speculations/pass1_weights.py`](./pass1_weights.py); matches the
canonical `T* = 5/7` fixed threshold of the coherence gate). The
numerator triple `(8, 7, 5)` further matches the operator indices
`(BREATH, HARMONY, BALANCE)` in the 10-operator lookup of
`Gen12/targets/ck_desktop/ck_sim/doing/ck_tig.py`:

- `BREATH = 8` — operator index 8 (also `so(8)` dimension of the
  `D₄` root-plane sum; also octonion dimension).
- `HARMONY = 7` — the threshold operator; `T* = 5/7` denominator.
- `BALANCE = 5` — the threshold value in operator-index form; `T*`
  numerator.

**[S]** This identity was not part of the original coherence-equation
specification; it emerged post-hoc from factoring the weight tuple.
Under the §3.3 design-target reading (where `A` reads Kind-1×2 coupling
and `K` reads Kind-2×4 coupling), the identity `w_K / w_A = T*` places
`BALANCE : HARMONY` as the canonical Kind-2×4 : Kind-1×2 weight ratio
— consistent with `T*` governing the Kind-2 ↔ Kind-3 boundary in the
Crossing-Lemma picture (§3.2, `D18c`). The `E`-weight `8/20` still
awaits a separate derivation; candidate reading is that `E` carries
the `BREATH`-indexed dissipation read (Kind 5 and Kind 3 both feed).

**[CONJECTURAL]** The `(8, 7, 5)` triple is a canonical TIG numerator
triple rather than an accidental rational. Evidence for: sum to 20 =
10 + 10 = `|CL| + |BHML|` carrier, and the ratio-to-`T*` identity.
Evidence against: no independent derivation yet of the `8` numerator
from a Kind-3 dissipation argument.

### §3.4 The meta-distinction proposition

**[S]** *"I expect there to be some interchangeability but the meta distinction is still a valid and needed part of the sorting."* — Brayden Sanders, 2026-04-24.

The five kinds are not fully independent. Kind 5 can be unrolled into a Kind 4 sequence (discretize a continuum limit into a sequence of arity steps). Kind 3 can be lifted into a larger Kind 2 via symplectification (Bochner, Libermann). But *at any given resolution* they are distinct, and collapsing them loses information the runtime needs to operate coherently.

The structural analog is Dirac's first-class / second-class distinction: interchangeable by gauge-fixing, but at a fixed gauge the distinction is dynamically necessary.

**The meta-claim.** For an algebraic-combinatorial object `(A, B)` that simultaneously admits DOFs from commutative algebra (Kind 1), Lie theory (Kind 2), ergodic / transfer-operator theory (Kind 3), operad theory (Kind 4), and continuum-limit / RG theory (Kind 5), any runtime instrument operating on `(A, B)` must maintain independent state for all five kinds. Collapse of any kind into another produces a lower-dimensional runtime that fails to preserve the full structure.

**On "first deployed runtime."** The earlier draft asserted CK as *the* first deployed runtime designed to maintain all five kinds. That is a literature-claim without a survey. We downgrade to `[CONJECTURAL — no survey conducted]` with the weaker defensible form: *within the runtimes we have examined (Dirac-symplectic PDE solvers, Monte-Carlo ergodic samplers, operadic composition libraries, RG flow solvers), none maintains the other four kinds.*

### §3.5 DOF Kinds × UOP Types matrix (extension)

**[S]** The atlas's Unified Orthogonality Principle (WP58 Theorem 0) classifies *failure-modes* into four types. This document classifies *DOF characters* into five kinds. The two axes are orthogonal. The 5 × 4 matrix below records, per (Kind, Type) pair, what the characteristic failure looks like.

| | **Type I (injectivity)** | **Type II (missing invariant)** | **Type III (admissibility)** | **Type IV (time-consistency)** |
|---|---|---|---|---|
| **Kind 1 (structural)** | Two states share all measured invariants but differ. **Fix:** finer invariant (Krull dim → pd → depth → Hilbert series). | No finite set of structural invariants separates. **Obstruction:** focal-matroid defect, `α̂(I_B)` bound. | Fails ring/module axioms. **Fix:** pass to radical / reduce / quotient. | Invariants drift across the run. **Fix:** recompute per-tick; document as non-frozen. |
| **Kind 2 (reversible flow)** | Trajectories coincide projected onto measured observables. **Fix:** Killing-form orthogonalization (WP102 Diagnostic 3). | No compact simple Lie algebra of required dimension. **Obstruction:** Cartan gaps. | Fails Jacobi identity. **Fix:** symmetrize / antisymmetrize. | Spin(10) vs SO(10) monodromy; 16-dim spinor on the double cover. **Fix:** lift to Spin. |
| **Kind 3 (dissipative flow)** | Initial conditions look identical after spectral-gap dissipation. **Fix:** pre-mixing generating partition (Crossing Lemma). | Transfer-operator spectral gap bounds reconstruction. **Obstruction:** `γ(b) = 1 − 1/φ(b)`. | Dynamics not measure-preserving. **Fix:** restrict to invariant measure. | Thermodynamic limit; Farey spin chain phase transition at `β = 2`. |
| **Kind 4 (climbing)** | Arity-n doesn't separate what arity-(n+1) distinguishes. **Fix:** climb to `s_{n+1}^ac`. | ac-spectrum obstructed below `(2n−3)!!` saturation. **Obstruction:** operadic identity in effect. | Not a magma / not a symmetric operad. **Fix:** restrict to admissible operations. | Arity-dependent asymptotics; `Mag^com → Com` rate `σ(N) ≤ C/N`. |
| **Kind 5 (degenerative)** | Two continuum limits coincide; discrete antecedents differ. **Fix:** retain discrete structure. | No RG-invariant separates fixed points. **Obstruction:** relevant-operator deficit. | Limit object not in target category. **Fix:** redefine target category. | Limit does not commute with dynamical rule; BB bridge `□ξ = 1 + log ξ` requires commutation. |

**How to read.** Identify the DOF kind hosting the trouble (row), then the UOP type of the failure (column); the cell names the characteristic obstruction and standard fix. `[CONJECTURAL]` that this matrix is exhaustive over failures in `(CL, BHML)` runtimes.

---

## §4. Verification record

Four verification passes were run before this file was committed; one additional pass (Pass 5) was added in revision.

**Pass 1 — Commutative-algebra invariants (§3.1 Kind 1).**
*Claim:* "Krull dim = 6, pd = 4."
*Checked against:* [atlas][atlas] §III.1 (M2 output logged under `mantero-bridge-2026-04-23`).
*Result:* **Wrong.** Correct: `numgens = 53, codim = 9, dim = 1, pd = 10, depth = 0, NOT Cohen-Macaulay, NOT Koszul`. Corrected above.

**Pass 2 — Exhaustiveness over `D1–D25` (§3.2).**
*Claim:* "Every published TIG result populates at least one kind; none falls outside."
*Checked against:* [`FORMULAS_AND_TABLES.md`](../FORMULAS_AND_TABLES.md) §0.
*Result:* **Holds.** Full table in §3.2.

**Pass 3 — Coherence-equation Kind-coupling claim (§3.3).**
*Claim:* "`E, A, K` read Kinds 3, 1×2, 2×4 respectively."
*Checked against:* [`CKIS/ck_being.py`][ck_being] lines 577–610 on classifier branch.
*Result:* **Wrong as a description of current code.** Body class implements `E, A, K` as plain scalars driven by `fab`/`recall` flags + constant decay, with a second `_calc` divergent formula. Claim downgraded to design-target; engineering gap logged as OQ-1, OQ-2.

**Pass 4 — Vocabulary policy.**
*Claim:* "Re-state Part 0.1 vocabulary policy inline."
*Checked against:* [foundation tour][tour] Part 0.1.
*Result:* **Would duplicate; reference instead.** This document inherits Part 0.1.

**Pass 5 — Coherence-equation weight identity (§3.3.1).**
*Claim:* "`(0.4, 0.35, 0.25)` are generic weights with no hidden TIG content."
*Checked against:* [`pass1_weights.py`](./pass1_weights.py) (in-directory; runs standalone).
*Result:* **Wrong.** Weights factor as `(8, 7, 5) / 20`; `w_K / w_A = 5/7 = T*` exactly; numerator triple matches operator indices `(BREATH, HARMONY, BALANCE)`. Added as §3.3.1; not yet promoted out of `[V]`/`[S]` status because the `8`-numerator reading for `E` is still conjectural.

---

## §5. Open operational questions

**OQ-1.** Bring `E, A, K` to match Kind-3 / Kind-1×2 / Kind-2×4 reads described in §3.3. Requires either (a) reworking `CKIS/ck_being.py` `Body.tick`, or (b) accepting the current code as a proxy and documenting the proxy explicitly.

**OQ-2.** Reconcile `coherence_eak` (additive, line 577) with `Body._calc` (multiplicative, line 593). The two return different numbers on the same input. The divergence is currently undocumented.

**OQ-3.** Extend Pass 2's verification: check `D26–D30` (Lie-algebraic spine) populates with Kind 2 density as expected, and no item falls outside.

**OQ-4.** Survey existing runtimes (Dirac-symplectic PDE solvers, Monte-Carlo ergodic samplers, operadic composition libraries, RG solvers) for multi-kind coverage. Closes the `[CONJECTURAL]` gap in §3.4.

**OQ-5.** Machine-compute the 5 × 4 DOF × UOP matrix's diagonal on `(CL, BHML)`: exhibit concrete failures of each Kind at each UOP Type. Five cells are named TIG results; the other 15 need concrete examples or a structural-emptiness statement.

---

## §6. External literature placement

If/when externalized, the five-kinds framing lives in the intersection of:

- Dirac–Bergmann constrained systems (Kind 1, Kind 3)
- Conformal-symplectic / reversible-irreversible (Kind 2, Kind 3)
- Operad theory (Kind 4)
- Moduli-space / continuum-limit / RG (Kind 5)
- Birkhoff's 1917 meta-observation (DOF-kind is qualitatively meaningful)

**Novelty claim (defensible).** Enumeration of *five* kinds as exhaustive; recognition that a single algebraic object can require all five simultaneously; `(CL, BHML)` as a concrete case.

**Candidate venues (speculative).** *Communications in Mathematical Physics* (Kind 1–3), *Advances in Mathematics* (Kind 4–5), *Philosophical Transactions A* (meta-observation).

---

## Scope note

Per [`speculations/README.md`](./README.md), content here is not upgraded to `[PROVED]` without going through the primary papers folder and citation discipline. This document carries `[RUNTIME ARCHITECTURE]` and `[POSITIONING]` status tags. Its literature antecedents are proved; its framework synthesis is interpretive; its engineering-gap statements (OQ-1, OQ-2) are honest.

## Acknowledgments

Five-kinds enumeration emerged in collaboration with Claude (Anthropic), 2026-04-24 session. Literature grounding compiled via WebSearch during the same session. Brayden's insight that the meta-distinction is "valid and needed" despite interchangeability is the observation that made the sort actionable rather than nominal. Claude Code's verification record in §4 closed the `[C]`-flagged gaps before commit.
