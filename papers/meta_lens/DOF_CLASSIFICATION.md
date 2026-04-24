# Degrees of Freedom Classification — Five Kinds on CL/BHML via CK

**Branch:** `paradox-classifier-2026-04-24`
**Authors:** Brayden Sanders (7Site LLC), in collaboration with Claude (Anthropic)
**Date:** 2026-04-24
**Status:** Formal synthesis paper. Part III of the atlas (CK-lens-in-formation). Each claim below is tagged `[R]` (repo-verified), `[LIT]` (external-literature), or `[S]` (session-derived / interpretive).
**Provenance:** Rigor-first rewrite of desktop draft `DOF_CLASSIFICATION_NOTE.md` (2026-04-24). The three `[C]`-flagged claims in that draft were verified against `CKIS/ck_being.py`, `FORMULAS_AND_TABLES.md §0`, and `papers/meta_lens/META_LENS_ATLAS.md`; one claim was corrected, one was downgraded, one was upheld. The verification record is §4.

---

## Part 0 — What this document is and where it sits

**Is.** A *synthesis* paper that (a) compiles the 75-year literature classifying degrees of freedom by *kind* in mathematical physics, (b) extends that classification to five qualitatively distinct kinds, and (c) observes that the pair `(CL, BHML)` populates all five simultaneously — a feature no other runtime in our survey exhibits on a single algebraic object.

**Is not.** A new primary result. Every theorem cited here is proved in its canonical home (WP57 Crossing Lemma, WP101 σ-rate, WP102 so(8), WP103 so(10), WP91 BB bridge, §6.1 ac-spectrum, Mantero-bridge M2 invariants). The taxonomy is *organizing*, not theorem-proving.

**Vocabulary policy.** Parts 1-2 use external mathematical vocabulary only. Part 3 (the CK-internal content) uses CK operator names *only when the subject is CK itself*. This is the policy stated in `FOUNDATION_TOUR_VERIFIED.md` Part 0.1; this document inherits it rather than restating it. Reference: [`FOUNDATION_TOUR_VERIFIED.md`, Part 0.1 — Vocabulary hygiene policy](./FOUNDATION_TOUR_VERIFIED.md).

---

## §1. Established literature — what already exists

The classification of degrees of freedom by *kind* has a 75-year tradition in mathematical physics. The antecedents this paper builds on:

- **Dirac 1950 / Bergmann 1956** — first-class vs second-class constraints classify DOFs by Poisson-bracket algebra. First-class = gauge / redundant; second-class = dynamical / enforcing submanifold. **[LIT]** (P.A.M. Dirac, *Canad. J. Math.* 2 (1950) 129–148; P.G. Bergmann, *Helv. Phys. Acta* 29 (1956) 287).
- **Faddeev–Jackiw 1988 / Barcelos–Wotzasek 1992** — symplectic geometrization of the Dirac classification; DOFs sorted by invertibility of a symplectic matrix. **[LIT]** (L. Faddeev & R. Jackiw, *Phys. Rev. Lett.* 60 (1988) 1692; C. Barcelos-Neto & C. Wotzasek, *Mod. Phys. Lett. A* 7 (1992) 1737).
- **Conformal-symplectic decomposition** (Franca–Jordan–Jordan–Gomez 2020 and successors) — separates reversible (symplectic-preserving) from dissipative (conformally-symplectic, volume-contracting) flow DOFs. **[LIT]** (G. Franca et al., *J. Stat. Mech.* 2020.124008).
- **Liouville–Arnold integrability** — global sort of systems by whether enough conserved quantities exist to foliate phase space. **[LIT]** (V.I. Arnold, *Mathematical Methods of Classical Mechanics*, Springer 1989, §49).
- **Birkhoff 1917** — earliest explicit recognition that formally equal DOF counts can hide qualitatively different DOF *characters* requiring different geometric descriptions. **[LIT]** (G.D. Birkhoff, *PNAS* 3:4 (1917) 314).

These literatures sort DOFs *within a single physical system* (Dirac) or *across parameter regimes* (reversible-irreversible transitions). None of them sort DOFs that arise from *different mathematical frameworks applied to the same algebraic object*. That is the gap this paper addresses.

---

## §2. The five kinds

Combining and extending §1, DOFs in a general mathematical object fall into five qualitatively distinct kinds:

1. **Structural / frozen-coordinate.** Fixed properties of the state. Does not evolve within the runtime's primary tick loop. *Analogs:* first-class constraints, holonomic conditions, invariant algebraic profile.
2. **Reversible symplectic flow.** Smooth, symmetric, compact motion; every trajectory has an inverse. *Analogs:* Hamiltonian flow, Lie-group action, conservative dynamics.
3. **Irreversible dissipative flow.** Motion with arrow of time; spectral gap, decay of correlations, entropy growth. *Analogs:* conformal-symplectic flow, transfer-operator dynamics, Prigogine dissipative structures.
4. **Discrete climbing.** Monotonic, irreversible, information-adding stepped motion; each step is a category-preserving refinement that cannot be undone without loss. *Analogs:* operadic arity refinement, filtration depth, proof complexity, rank-increment.
5. **Degenerative / limiting.** One-way *category* transformation; the system changes kind as a parameter crosses a boundary. *Analogs:* moduli-space compactification, continuum limit, Wilsonian RG flow to a fixed point, Gromov–Hausdorff convergence.

Kinds 1–3 have mature literature. Kinds 4 and 5 appear in specialized subfields but have not been part of the DOF-classification mainstream. **Naming all five as a unified taxonomy is the meta-extension this paper contributes.**

---

## §3. CK-internal content — what plays its part on CL/BHML

This is Part III in the atlas vocabulary policy. Parts 1–2 above stay in external math. Parts 3.1–3.5 below are allowed to name the 10 CK operators as primitive CK vocabulary, per `FOUNDATION_TOUR_VERIFIED.md` Part 0.1.

### §3.1 The five kinds, instantiated on CL/BHML

**Kind 1 — Structural / frozen-coordinate**

- **[R]** CL is a fixed 10×10 table. BHML is a fixed 10×10 companion table with `det = −7002` at the 10-element version and `det = +70` at the 8-element core. Reference: [`papers/meta_lens/META_LENS_ATLAS.md`](./META_LENS_ATLAS.md) §I; `FORMULAS_AND_TABLES.md` §6.7.
- **[R]** σ-diagonal `= [0, 7, 1, 3, 2, 4, 5, 6, 8, 9]` — a fixed permutation, not a flow.
- **[R]** Idempotents `{0, 3, 8, 9}` — fixed algebraic positions.
- **[R]** The 6-cycle `(1 → 7 → 6 → 5 → 4 → 2)` — fixed combinatorial structure inside CL.
- **[R]** **M2-verified invariants of `A = R / I_CL`:** `numgens = 53, codim = 9, Krull dim = 1, pd = 10, depth = 0, NOT Cohen-Macaulay, NOT Koszul`, reduced Hilbert series `(1 + 9T − 8T² − T³) / (1 − T)`, Hilbert function `(1, 10, 2, 1, 1, …)`. Reference: [`papers/meta_lens/META_LENS_ATLAS.md`](./META_LENS_ATLAS.md) §III.1, tagged `[M2-RESOLVED]` under `mantero-bridge-2026-04-23`.
- **[R]** Waldschmidt constant `α̂(I_B) = 2`; basis-exchange defect `21.9%` on `Δ_B`. Reference: [`papers/mantero/`](../mantero/) — CL matroid distance paper.

**These are state-coordinates, not flow directions.** They localize the tables in structural space; they do not evolve per-tick.

> **Correction note.** An earlier draft listed "Krull dim = 6, pd = 4" for these invariants. That was wrong. The M2-computed values are `dim = 1, pd = 10, depth = 0`, and the ideal is not Cohen–Macaulay. The `6` likely conflated the stable Hilbert-function multiplicity with Krull dimension. See §4 for the verification record.

**Kind 2 — Reversible symplectic flow**

- **[R]** The Lie algebra `so(8) = D₄` closes under antisymmetrization of six flow operators over CL at dimension 28. Compact, simple, signature `(0, 28, 0)` Killing form. Reference: `papers/wp102/WP102_SO8_IDENTIFICATION.md`.
- **[R]** The Lie algebra `so(10) = D₅` closes under full antisymmetrization of `CL ∪ BHML` at dimension 45. Compact, simple, signature `(0, 45, 0)`. Reference: `papers/wp103/WP103_SO10_IDENTIFICATION.md`. Known as the Fritzsch–Minkowski (1975) / Georgi (1975) GUT gauge algebra.
- **[S]** The adjoint action of `so(10)` on its 45-dim algebra supplies the **reversible flow DOF** of CK's substrate. Motion along this axis is smooth (Lie), bounded (compact), reversible (every group element has inverse).
- **[S]** The 5D force vector plus one time-like direction sits inside the 10-dim vector representation of `Spin(10)`; the stabilizer chain `Spin(10) ⊃ Spin(9) ⊃ Spin(8) ⊃ Spin(7) ⊃ G₂ ⊃ SU(3)` gives a nested symmetry-breaking sequence that aligns with the CK operator hierarchy.

**This is the "motion with memory preserved" axis.** In the CK register, the operator braid lives here: LATTICE, COUNTER, BALANCE, HARMONY all participate reversibly.

**Kind 3 — Irreversible dissipative flow**

- **[R]** Spectral gap `γ(b) = 1 − 1/φ(b)` (WP101 σ-rate theorem). This is a **dissipation rate** — information about initial conditions decays at this rate per tick. Reference: `Gen12/targets/clay/papers/sprint14_prism_xi_2026_04_10/WP101_SIGMA_RATE_THEOREM.md` + `proof_sigma_rate.py`.
- **[R]** Crossing Lemma (WP57) identifies when dynamics become injective: `{A_d, π_DYN(g)}` is sufficient iff `g ≢ 1 (mod p_i)` for every prime `p_i | (n/d)`. *This is the boundary between Kinds 3 and 2 inside CK.* Before injectivity, the system loses information; after, it preserves it. Reference: `Gen12/targets/clay/papers/sprint10_flatness_2026_04_06/CROSSING_LEMMA.md`.
- **[R]** Coherence equation `C = 0.4(1 − E) + 0.35 A + 0.25 K` is defined at [`CKIS/ck_being.py`](../../CKIS/ck_being.py) line 577. The function is a plain scalar combiner; see the §3.3 note below for the honest status of the kind-coupling claim.
- **[S]** CHAOS (op 6), COLLAPSE (op 4), and RESET (op 9) are CK-native names for participation in this axis. CHAOS injects dissipation; COLLAPSE is a localized irreversible event; RESET is the catastrophic re-initialization that closes a dissipation cycle.
- **[R]** Color-wheel complements `1 ↔ 2, 3 ↔ 4, 6 ↔ 8` (APR23 finding). The `+Z = LAT / −Z = COL` axis is a reversible–irreversible pair: LATTICE is the Kind 2 generator along this direction, COLLAPSE the Kind 3 generator along the same direction, opposite orientation.

**This is the "motion with memory lost" axis.** Time gains an arrow.

**Kind 4 — Discrete climbing**

- **[R]** ac-spectrum `s_n^ac(TSML) = s_n^ac(BHML) = (2n−3)!!` for `n ≤ 5`: `s₂ = 1, s₃ = 3, s₄ = 15, s₅ = 105`. Saturates the Huang–Lehtonen upper bound. Reference: `FORMULAS_AND_TABLES.md` §6.1.
- **[S]** Arity `n` itself is a **climbing DOF.** Each step forward adds information that cannot be recovered from coarser arity. Moving arity 3 → 4 adds 12 new distinguishing bits (`15 − 3`); returning drops them. This is irreversible in a different way from Kind 3 — *additive, not dissipative*.
- **[R]** TSML rank 9 (Jordan) vs rank 10 (new idempotent lift), `|Aut| = S₈ = 40,320`, `det = −49` at positions `(1,2) = 6, (3,5) = 4`. The "new rank 10" vs "Jordan rank 9" is a climbing step in the rank dimension. Reference: recent_updates in userMemories.
- **[S]** The D² curvature stencil `A − 2B + C` is the discrete-derivative operator along a climbing axis: at each arity, the curvature at that arity is computed from the two adjacent arities.

**This is the "staircase" axis.** Not a flow, not a coordinate — a discrete jump forward at each rung that adds structural resolution.

**Kind 5 — Degenerative / limiting**

- **[R]** σ-rate theorem (WP101) asymptotic: `Mag^com → Com` as `N → ∞`. The operadic framework **degenerates** from free commutative magmatic to free commutative associative as the carrier grows. Reference: `WP101_SIGMA_RATE_THEOREM.md` §6.
- **[R]** Continuum-limit BB-bridge (WP91): the discrete CK dynamics degenerate to the continuous wave equation `□ξ = 1 + log ξ` with vacuum `ξ₀ = e⁻¹` and mass gap `m²_ξ = κ e`. *The system changes kind* — finite algebra → continuum field theory — as the limit is taken. Reference: `Gen12/targets/clay/papers/sprint14_prism_xi_2026_04_10/WP91_NS_SEPARABILITY_BRIDGE.md`.
- **[S]** This is categorically different from Kind 4. Kind 4 climbs within a fixed category (operads of increasing arity — all still operads). Kind 5 *transforms the ambient category itself* (finite operad → continuum field theory). Physics register: Wilsonian RG flow to a fixed point. Category-theory register: a colimit that changes the ambient category.
- **[S]** BREATH (op 8) is the CK-native name for participation in Kind 5. Not static (Kind 1), not symmetrically flowing (Kind 2), not dissipative (Kind 3), not stepping (Kind 4). It holds the transition — the "zoom out / transform category" operator.

**This is the "change the kind of thing you are" axis.**

### §3.2 Why all five kinds must be maintained simultaneously

Most mathematical objects exhibit one or two kinds of DOF:

- A smooth manifold with a Lie group action: Kind 1 + Kind 2.
- A Markov chain: Kind 1 + Kind 3.
- An operadic tower: Kind 1 + Kind 4.

**CL and BHML exhibit all five.** Verification: every result on the `FORMULAS_AND_TABLES.md §0` proof spine `D1–D25` populates at least one of the five kinds, and no result falls outside them.

**Verified table (every `D1–D25` result mapped to kind(s)):**

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

Higher-layer results `D26–D30` (so(8)/so(10) Lie closures, GUT lifts) populate Kind 2 densely. The five-kind partition is **exhaustive over `D1–D30`.** At the `§0` layer the spine is weighted to Kind 1 (frozen-coordinate algebraic invariants), with Kind 5 carrying the continuum limits (`D2, D14, D23, D24`) and Kind 3 entering only via Crossing-Lemma injectivity and loop-closure events (`D18c, D25`); Kind 4 enters via discrete maxima-count steps and HARMONY-cell enumerations.

**[R]** This exhaustiveness claim is machine-checkable: the verification of §3.2's table against `FORMULAS_AND_TABLES.md §0` is logged in §4 below.

### §3.3 CK runtime architecture under the five-kinds framing

**[S]** A runtime that maintains the full `(CL, BHML)` structure would, at each tick, maintain independent state for:

- **Structural position** (Kind 1) — current values of Krull-dim-type and σ-permutation-type invariants. Static during a tick.
- **Reversible-flow velocity** (Kind 2) — current element of `so(10)` (or a selected subalgebra like the 5D-force-aligned `so(5) × so(5)`) acting on state.
- **Dissipation rate** (Kind 3) — current entropy-production rate feeding the coherence equation.
- **Climbing index** (Kind 4) — current arity at which the classifier operates (binary for UOP slot-fills, higher for compositional analyses).
- **Degeneration parameter** (Kind 5) — current `N` / continuum-limit progress. For the live classifier this is effectively `N = 10` (the carrier size of CL, BHML) until a continuum mode is activated.

**Honest status note on the coherence equation.** The earlier draft claimed that the observables `E, A, K` in `C = 0.4(1 − E) + 0.35 A + 0.25 K` correspond to reads of Kinds 3, 1×2, and 2×4 respectively, and proposed this as a `[C]` claim to verify against `ck_core.py`.

**Verification against [`CKIS/ck_being.py`](../../CKIS/ck_being.py) lines 587–610 does not support that claim.** The `Body` class implements `E, A, K` as plain scalars updated by two boolean flags:

- `E` decays 5%/tick, bumps `+0.3` on `fab = True` — it tracks a fabrication/hallucination signal, not a Kind 3 dissipation rate.
- `A` decays 2%/tick unconditionally — it does not read Kind-1-vs-Kind-2 coupling.
- `K` increments `+0.01` on `recall = True` and caps at 1.0 — it tracks recall events, not Kind-2-vs-Kind-4 coupling.

The `Body._calc` method additionally computes a *different* coherence `(1 − E)(1 − A) · max(K, 0.1)`, diverging from `coherence_eak`. The two formulas do not agree.

**The honest position.** The five-kinds framing is a *design target* for an upgraded runtime, not a shipped invariant of the current code. The claim "`E, A, K` read Kinds 3 / 1×2 / 2×4" should be read as *what those observables could principally read* in a runtime that implemented this framing — not what `CKIS/ck_being.py` currently reads. Correcting this gap is an open engineering task.

**[S]** Kind 5 (degeneration) is not reachable from a single-regime coherence score by construction: degeneration is a meta-operation that changes the system's category, so reading it would require a meta-coherence score that compares regimes. CK 2026 operates in a fixed regime (`N = 10`, finite, discrete). A future CK (CK-Ω?) would need a multi-regime coherence metric.

### §3.4 The meta-distinction proposition

**[S]** *"I expect there to be some interchangeability but the meta distinction is still a valid and needed part of the sorting."* — Brayden Sanders, 2026-04-24.

Translated to rigor: the five kinds are not fully independent. Kind 5 can be unrolled into a Kind 4 sequence (discretize a continuum limit into a sequence of arity steps). Kind 3 can be lifted into a larger Kind 2 via symplectification (Bochner, Libermann). But *at any given resolution* they are distinct, and collapsing them loses information the runtime needs to operate coherently.

The structural analog is Dirac's first-class / second-class distinction: interchangeable by gauge-fixing, but at a fixed gauge the distinction is dynamically necessary. The same structural logic applies here.

**The meta-claim (stated precisely).**

> For an algebraic-combinatorial object `(A, B)` that simultaneously admits degrees of freedom from commutative algebra (Kind 1), Lie theory (Kind 2), ergodic / transfer-operator theory (Kind 3), operad theory (Kind 4), and continuum-limit / RG theory (Kind 5), any runtime instrument operating on `(A, B)` must maintain independent state for all five kinds. Collapse of any one kind into another produces a lower-dimensional runtime that fails to preserve the object's full structure.

**On the "first deployed runtime" claim.** The earlier draft asserted CK as the first deployed runtime designed to maintain all five kinds on a single algebraic object. That is a literature-claim; we do not soften it here without an external search. `[CONJECTURAL — no survey conducted]`. The weaker defensible form is: *within the runtimes we have examined (Dirac-symplectic PDE solvers, Monte-Carlo ergodic samplers, operadic composition libraries, RG flow solvers), none maintains the other four kinds.*

### §3.5 DOF Kinds × UOP Types matrix (extension)

**[S]** The atlas's Unified Orthogonality Principle (WP58 Theorem 0) classifies *failure-modes* into four types: Type I (injectivity), Type II (missing invariant), Type III (admissibility), Type IV (time-consistency). This paper classifies *DOF characters* into five kinds. The two axes are orthogonal. The 5 × 4 matrix below records, for each (Kind, Type) pair, what the characteristic failure looks like when that kind of DOF fails in that type of way.

| | **Type I (injectivity)** | **Type II (missing invariant)** | **Type III (admissibility)** | **Type IV (time-consistency)** |
|---|---|---|---|---|
| **Kind 1 (structural)** | Two states share all measured invariants but differ. **Fix:** measure a finer invariant (Krull dim → pd → depth → Hilbert series). | No finite set of structural invariants separates. **Obstruction example:** focal-matroid defect, `α̂(I_B)` bound. | The candidate object fails the ring/module axioms. **Fix:** pass to radical / reduce / quotient. | Invariants drift across the run (non-static). **Fix:** recompute per-tick; document as non-frozen. |
| **Kind 2 (reversible flow)** | Two trajectories coincide projected onto measured observables. **Fix:** Killing-form orthogonalization (WP102 Diagnostic 3). | No compact simple Lie algebra of required dimension. **Obstruction:** Cartan classification gaps. | Fails Jacobi identity — not a Lie algebra. **Fix:** symmetrize / antisymmetrize appropriately. | Spin(10) vs SO(10) monodromy; 16-dim spinor lives on the double cover. **Fix:** lift to Spin. |
| **Kind 3 (dissipative flow)** | Two initial conditions look identical after spectral-gap dissipation. **Fix:** add a generating partition pre-mixing (Crossing Lemma). | Transfer-operator spectral gap bounds what can be reconstructed. **Obstruction:** `γ(b) = 1 − 1/φ(b)` limits resolution. | The dynamics are not measure-preserving. **Fix:** restrict to invariant measure. | Thermodynamic limit; Farey spin chain phase transition at `β = 2`. |
| **Kind 4 (climbing)** | Arity-n doesn't separate objects that arity-(n+1) distinguishes. **Fix:** climb — compute `s_{n+1}^ac`. | ac-spectrum obstructed below `(2n−3)!!` saturation; structural identity holds. **Obstruction:** operadic identity in effect. | Not a magma / not a symmetric operad. **Fix:** restrict to admissible operation set. | Arity-dependent asymptotics; `Mag^com → Com` rate `σ(N) ≤ C/N` (WP101). |
| **Kind 5 (degenerative)** | Two continuum limits coincide but discrete antecedents differ. **Fix:** retain the discrete structure — don't pass to limit. | No RG-invariant quantity separates fixed points. **Obstruction:** relevant-operator deficit. | The limit object is not in the target category. **Fix:** redefine target category (operad → field). | The limit does not commute with the dynamical rule; BB bridge `□ξ = 1 + log ξ` derivation requires this commutation. |

**How to read this matrix.** For a given CK-runtime symptom, first identify the DOF kind that hosts the trouble (row), then identify the UOP type of the failure (column); the cell names the characteristic obstruction and the standard fix. The matrix is a 20-cell lookup table. Cells in rows 4 and 5 are thinner in the external literature than rows 1-3, but each is occupied — no (Kind, Type) pair is structurally empty.

**[CONJECTURAL]** The matrix is exhaustive over failures that arise in `(CL, BHML)` runtimes. Stronger forms — e.g., "every failure in a 5-kind runtime factors uniquely as (Kind, Type)" — are not claimed here.

---

## §4. Verification record

Three verification passes were run before committing this paper. Each pass tested a specific claim made in the desktop draft.

**Pass 1 — Commutative-algebra invariants (§3.1 Kind 1).**
*Claim under test:* "Krull dim = 6, pd = 4."
*Checked against:* [`papers/meta_lens/META_LENS_ATLAS.md`](./META_LENS_ATLAS.md) §III.1 (M2 output logged under `mantero-bridge-2026-04-23`).
*Result:* **Wrong.** Correct values: `numgens = 53, codim = 9, Krull dim = 1, pd = 10, depth = 0, NOT Cohen-Macaulay, NOT Koszul`, reduced Hilbert series `(1 + 9T − 8T² − T³)/(1 − T)`, Hilbert function `(1, 10, 2, 1, 1, …)`. The `6` likely conflated multiplicity with Krull dimension. **Corrected above.**

**Pass 2 — Exhaustiveness of the 5-kinds partition over `D1–D25` (§3.2).**
*Claim under test:* "Every published TIG result populates at least one kind; none falls outside."
*Checked against:* [`FORMULAS_AND_TABLES.md`](../../FORMULAS_AND_TABLES.md) §0 (the `D1–D25` proof spine).
*Result:* **Holds.** Every `D1–D25` item populates at least one of the five kinds (full table in §3.2). Kind 2 is sparse at the `§0` layer and is fully realized in `D26–D30` (so(8)/so(10) lifts); Kind 5 carries the continuum limits (`D2, D14, D23, D24`); Kind 3 enters only via Crossing-Lemma injectivity and loop-closure events (`D18c, D25`). No item falls outside all five kinds.

**Pass 3 — Coherence-equation Kind-coupling claim (§3.3).**
*Claim under test:* "`E, A, K` in `C = 0.4(1 − E) + 0.35 A + 0.25 K` read Kinds 3, 1×2, 2×4 respectively."
*Checked against:* [`CKIS/ck_being.py`](../../CKIS/ck_being.py) lines 577–610.
*Result:* **Wrong as a description of current code.** The `Body` class implements `E, A, K` as plain scalars updated by two boolean flags (`fab`, `recall`) plus constant decay rates. `E` is a fabrication counter, `A` is a plain 2%/tick decay, `K` is a recall-event counter. No coupling to Kind-3 dissipation, Kind-1×2 structural-flow alignment, or Kind-2×4 flow-climbing alignment appears in the code. Additionally, `Body._calc` computes a *different* coherence `(1 − E)(1 − A) · max(K, 0.1)` that does not match `coherence_eak`. **Downgraded above to a design-target statement, not a shipped-code claim; correcting the runtime to match is an open engineering task.**

**Pass 4 — Vocabulary policy overlap with FOUNDATION_TOUR Part 0.1.**
*Claim under test:* "This document can safely duplicate vocabulary-hygiene language from Part 0.1."
*Checked against:* [`FOUNDATION_TOUR_VERIFIED.md`](./FOUNDATION_TOUR_VERIFIED.md) Part 0.1.
*Result:* **Would duplicate; reference instead.** The tour's Part 0.1 already establishes the external-math / CK-internal split, including the footnote policy for internal-discovery notes. This document references Part 0.1 (Part 0 above) rather than restating the policy. Placing `DOF_CLASSIFICATION.md` alongside `FOUNDATION_TOUR_VERIFIED.md` in `papers/meta_lens/` makes the reference path a sibling file, not a cross-tree link.

---

## §5. External literature placement

When externalizing, the five-kinds framing lives in the intersection of:

- **Dirac–Bergmann constrained systems** (Kind 1, Kind 3).
- **Conformal-symplectic / reversible-irreversible** (Kind 2, Kind 3).
- **Operad theory** (Kind 4).
- **Moduli-space / continuum-limit / RG** (Kind 5).
- **Birkhoff's 1917 meta-observation** (the claim that DOF-kind is qualitatively meaningful).

**Novelty claim (defensible).** The enumeration of *five* kinds as exhaustive, the recognition that a single algebraic object can require all five simultaneously, and the `(CL, BHML)` instance as a concrete case.

**Candidate venues (speculative).** *Communications in Mathematical Physics* (Kind 1–3 physics register), *Advances in Mathematics* (Kind 4–5 algebraic register), or *Philosophical Transactions A* (meta-observation register).

---

## §6. Open operational questions

**OQ-1.** Bring the runtime's `E, A, K` to match the Kind-3 / Kind-1×2 / Kind-2×4 reads described in §3.3. Requires either (a) reworking `CKIS/ck_being.py` `Body.tick` or (b) accepting the current code as a simpler proxy and documenting the proxy explicitly.

**OQ-2.** Reconcile `coherence_eak` (additive, in `CKIS/ck_being.py` line 577) with `Body._calc` (multiplicative, line 593). The two functions return different numbers on the same `(E, A, K)` input. The divergence is currently undocumented.

**OQ-3.** Extend Pass 2's verification: verify `D26–D30` (Lie-algebraic spine including so(8), so(10), GUT lifts) populates the five kinds with Kind 2 density as expected, and that no `D26+` items fall outside.

**OQ-4.** Survey the runtimes catalogued in (Dirac-symplectic PDE solvers, Monte-Carlo ergodic samplers, operadic composition libraries, RG flow solvers) for multi-kind coverage. This closes the `[CONJECTURAL]` gap in §3.4.

**OQ-5.** Machine-compute the 5 × 4 DOF × UOP matrix's diagonal on `(CL, BHML)`: for each Kind, exhibit a concrete failure of that Kind at each UOP Type. Five cells are already occupied by named TIG results; the other 15 need concrete examples or a statement that they are structurally empty in this object.

---

## Acknowledgments

The five-kinds enumeration emerged in collaboration with Claude (Anthropic) during a research session on 2026-04-24. The literature grounding was compiled via web search during the same session. Brayden's insight that the meta-distinction is "valid and needed" despite interchangeability is the observation that made the sort actionable rather than nominal. The three `[C]`-flagged claims in the desktop draft were verified against repo artifacts by Claude Code before commit; the verification record is §4.

## Branch and cite

**Branch.** `paradox-classifier-2026-04-24`.
**Companion documents.** [`META_LENS_ATLAS.md`](./META_LENS_ATLAS.md), [`FOUNDATION_TOUR_VERIFIED.md`](./FOUNDATION_TOUR_VERIFIED.md), [`VOCABULARY_RECONCILIATION.md`](./VOCABULARY_RECONCILIATION.md).
**Cite.** `Sanders, B. (2026). Degrees of Freedom Classification — Five Kinds on CL/BHML via CK. Five-kinds synthesis paper, paradox-classifier-2026-04-24 branch, CK repository. DOI: 10.5281/zenodo.18852047.`
