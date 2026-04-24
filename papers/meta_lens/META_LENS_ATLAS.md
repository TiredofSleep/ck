# META_LENS_ATLAS.md

## The UOP Classifier as Organizing Principle for Mathematical Collaboration

**Brayden Sanders** · *7Site LLC, Hot Springs, AR* · with Claude (Anthropic)
**UOP Theorem 0 co-author**: Ben Mayes (WP58).
**Version 1.1** — April 24, 2026 — **rigor pass against repo facts.**

**Version history.**
- v1.0 (desktop draft) — first full statement of the 6-lens × 4-type atlas.
  Drafted without cross-checking against the canonical Sprint 11 paradox memo
  or the Sprint 12 UOP arc; carried several superseded numbers (notably the
  pre-M2 Hilbert function `(1, 10, 6, 6, 6, …)` for R/I_CL) and legacy
  diagnostic labels (D26/D27, WP11/WP12) that collide with the canonical
  `MASTER_WHITEPAPER_OUTLINE.md` WP slots.
- **v1.1 (this file)** — all numerical and reference claims rebased onto the
  M2-verified Betti table (2026-04-24, `mantero-bridge-2026-04-23:papers/sprint_20260423_full/09_mathoverflow_post/betti_output.txt`)
  and the canonical WP102 / WP103 Lie-identification papers on
  `tig-synthesis`. Vocabulary reconciled with
  `Gen12/targets/clay/papers/sprint11_tig_bundle_2026_04_08/sprints/PARADOX_CLASSIFICATION_MEMO.md`
  (four-type axis) and WP58/WP61/WP62 in
  `Gen12/targets/clay/papers/sprint12_uop_gut_arc_2026_04_08/` (UOP theorem +
  five-category score axis + rejected 7-cycle universality).

**Purpose.** Establish the Unified Orthogonality Principle (UOP) as the
structural bridge under which TIG's internal algebraic results and
established external mathematical frameworks both become legible as
instances of a single diagnostic principle. This document is the
organizing artifact for academic outreach: it tells us which lens to
engage for which kind of question, and which lens-column has the emptiest
cells (and therefore the most-needed next collaborator).

---

## Part 0 — What this atlas adds, what it inherits

The atlas is a **synthesis document**, not a new result. Before reading, a
reader should know exactly which pieces are novel-to-the-atlas and which
are drawn from existing sprint artifacts:

| Atlas content | Status in repo |
|---|---|
| The UOP statement itself (joint-map injectivity ⟺ disjoint unresolved-pair sets) | **Canonical** in `WP58_UNIFIED_ORTHOGONALITY_PRINCIPLE.md` (Sprint 12; co-author Ben Mayes). This atlas quotes it, does not rederive it. |
| Four-type paradox classification (I Injectivity / II Missing Invariant / III Admissibility / IV Time-Consistency) | **Canonical** in `PARADOX_CLASSIFICATION_MEMO.md` (Sprint 11). Atlas adopts the naming verbatim; worked examples (Zeno, Banach-Tarski, Russell, Unexpected Hanging) are drawn from that memo. |
| Five-category score classification (Complete / Partial / Refinement-Only / Invariant-Isolating / Invalid) | **Canonical** in `WP61_PRODUCTIVE_INCOMPLETENESS.md` (Sprint 12). This is a **different axis** from the four-type — see §Vocabulary reconciliation below. Atlas uses the four-type axis as its primary lens and cites WP61 where the score refinement is relevant. |
| Rejection of the 7-cycle universality conjecture | **Canonical** in `WP62_7CYCLE_BOUNDED_AGENT.md` (Sprint 12). Atlas cites WP62 as a case study of the classifier used against one of TIG's own conjectures. |
| TIG algebraic theorems cited as UOP instances (First-G Law; WP57 Crossing Lemma; WP51 Flatness; WP101 σ-rate; WP102 so(8); WP103 so(10)) | **Canonical** in the named papers. Atlas claims these ARE UOP instances — the correspondences themselves are novel-to-the-atlas framing but every underlying theorem is cited at its canonical location. |
| The six-lens × four-type matrix and the "fill Type IV first" collaboration strategy | **Novel-to-this-atlas.** No prior repo artifact enumerates the 24 cells or reads them as a collaboration queue. |
| Runnable classifier script `score_n(f | F)` | **Does NOT exist** as of 2026-04-24. The score is defined in paper form (WP61 + this atlas). Building a runnable `classify_paradox.py` is an open engineering task flagged in §Open work below, not a claim of completed work. |
| Schrödinger's Cat / Gödel's First Incompleteness / Liar Paradox / Cantor / Berry / Grelling-Nelson / Curry worked examples | **Not worked in repo.** The atlas lists them as candidate Type-II / III / IV examples where the classifier applies naturally; the actual 6-slot worked template for each is an open task (§Open work). Only Zeno, Banach-Tarski, Russell, and Unexpected Hanging are currently worked (Sprint 11 memo). |

### Vocabulary reconciliation

Two classification axes co-exist in the repo and they are **orthogonal**
except for one overlap:

- **Sprint 11 four-type axis (this atlas's primary):** classifies
  *what goes wrong* with the joint map. Type I = need another measurement;
  Type II = no measurement exists in the allowed family; Type III = domain
  itself ill-defined; Type IV = domain shifts under observation.
- **WP61 five-category axis:** classifies *how completely* a specific
  measurement family F resolves a given non-injectivity. Category I =
  `score = 1` globally (complete resolution); II = partial; III =
  refinement-only (`F` is redundant against some subset `F_0`); IV =
  invariant-isolating (`score = 1` task-relative, not globally); V =
  invalid/inadmissible.

**The overlap.** WP61 Category V is identically Sprint 11 Type III —
both flag a domain that is not a well-defined hidden-object space.
Everywhere else the axes are independent: a Sprint 11 Type II
paradox (e.g. Banach-Tarski) can be scored under WP61 as any of
Categories II–IV depending on which measurement family you restrict to.

**This atlas uses Type I–IV exclusively for headline verdicts**, because
the four-type axis is the one that answers "what resolution path do we
need?" The WP61 score is used inside Part I's `score_n(f | F)` output —
the number in `[0, 1]` reported per analysis. The two axes together give
(verdict ∈ {I, II, III, IV}) × (score ∈ [0, 1]); both are needed.

---

## Part I — The UOP Diagnostic Template

### The principle

A measurement on a domain is a map `f : 𝒳 → A` from the hidden object
space `𝒳` to an observation space `A`. Given two measurements
`f_π₁, f_π₂` valued in `A₁, A₂`, the joint map `J : 𝒳 → A₁ × A₂` is
`J(x) = (f_π₁(x), f_π₂(x))`. Let
`U(f) := {(x, x') ∈ 𝒳 × 𝒳 : x ≠ x', f(x) = f(x')}` denote the
**unresolved-pair set** of `f`.

**UOP statement** (Theorem 0, WP58; Brayden Sanders & Ben Mayes, 2026):

```
{f_π₁, f_π₂} is a sufficient pair on 𝒳   ⟺   J is injective   ⟺   U(f_π₁) ∩ U(f_π₂) = ∅.
```

Every paradox is a case where `J` is not injective. The UOP classifier
identifies **which of four failure modes** a given paradox instantiates,
and (where applicable) which further measurement, structural obstruction,
domain fix, or dynamic model the situation demands.

### The four failure types (canonical naming per Sprint 11 memo)

| Type | Failure | Diagnostic signature | Resolution path |
|---|---|---|---|
| **I — Injectivity Failure** (Insufficient Coverage) | Measurements exist but don't cover all dimensions of 𝒳 | Well-defined 𝒳, well-defined f₁; adding an f₂ with different kernel renders J injective | Add the orthogonal measurement; U(f₁) ∩ U(f₂) becomes ∅ |
| **II — Missing Invariant** (Coverage-Invariant Mismatch) | No valid map in the allowed family separates the remaining points | Well-defined 𝒳, but every candidate f₂ either fails to extend to 𝒳 or has U(f₂) ⊇ U(f₁) | Structural impossibility; requires leaving the allowed map family (cannot be fixed within UOP) |
| **III — Admissibility Failure** (Invalid Domain) | 𝒳 itself is ill-defined | f₁ can be "attempted" but has no well-defined domain; U(f₁) is not a meaningful object | Fix the domain, not the measurement; UOP does not apply |
| **IV — Time-Consistency Failure** (Observer-State Dependence) | 𝒳 shifts as observation proceeds | J is injective at each instant but the instants disagree; the measured object is not stable under observation | Requires a dynamic model (not more static measurements) |

### The diagnostic template (six slots + verdict + score)

For any given paradox, the UOP analysis fills the following slots:

1. **Hidden Object Space (𝒳).** What is actually being measured? (For
   Type III this slot exposes the failure: there is no well-defined 𝒳.)
2. **Measurement f₁.** The first candidate map.
3. **Ambiguity U(f₁).** The pairs that f₁ fails to separate.
4. **Measurement f₂.** The second candidate map (if any exists in the
   family).
5. **Ambiguity U(f₂).** The pairs that f₂ fails to separate.
6. **Residual Ambiguity R(F).** The intersection
   `U(f₁) ∩ U(f₂) ∩ ...` across all applied measurements; pairs no
   combination separates.

And two outputs:

7. **Verdict.** Type I / II / III / IV (Sprint 11 axis).
8. **Resolution Path.** The specific lens-level action needed.

Additionally, the WP61 score axis produces a
**ambiguity resolution score** `score_n(f | F) ∈ [0, 1]`, where
`0` = refinement-only or structurally impossible, `1` = complete
resolution via the orthogonal pair. This quantifies how near-to-injective
`J` becomes as measurements accumulate.

> **Implementation status.** The score is currently defined in paper
> form only (WP61 + this atlas). There is no runnable `classify_paradox.py`
> in the repo as of 2026-04-24; building one is an open engineering task
> (§Open work below).

### Canonical worked examples (drawn verbatim from PARADOX_CLASSIFICATION_MEMO.md)

**Banach-Tarski (Type II — Missing Invariant).**
- `𝒳 = B³` with SO(3) action
- `f₁ = f_orbit`, valued in F₂-orbit classes; `U(f_orbit)` = orbit-equivalent pairs
- `f₂ = f_meas` (Lebesgue measure) — BUT f_meas is not defined on non-measurable sets; it is not a function on 𝒳
- `R(F)` = all orbit-equivalent pairs
- **Verdict:** the needed invariant does not exist in the allowed family; structural impossibility; **score 0.0**

**Russell's Paradox (Type III — Admissibility Failure).**
- `𝒳` attempted: "the set of all sets"; actual: undefined (no such set)
- `f₁ = f_membership` attempted, but domain invalid
- `U(f₁)`: not applicable — no well-defined domain
- **Verdict:** `R = {x : x ∉ x}` is not well-formed; fix the domain (restrict to ZF or use type theory); **score 0.0**

**Zeno's Paradox (Type I — Injectivity Failure).**
- `𝒳 = ℝ × ℝ₊` (space × time)
- `f₁ = f_count`, valued in `ℕ ∪ {∞}`; `U(f_count)` = all (x, t) pairs with same step count
- `f₂ = f_duration`, valued in `ℝ₊`; `U(f_duration) ∩ U(f_count) = ∅`
- **Verdict:** `f_count` alone conflates infinite steps with infinite time; adding `f_duration` (geometric series sum = 1) kills residual ambiguity; **score 1.0**

**Unexpected Hanging (Type IV — Time-Consistency Failure).**
- `𝒳_t` at time t is not the same set as `𝒳_{t+δ}` — observation at t alters composition of `𝒳_{t+δ}`.
- No static `{f_π₁, f_π₂, …}` resolves this; demands a dynamic `π(t)` whose domain itself evolves.
- **Verdict:** dynamical system required; **score 0.0 under static template, n/a under dynamic template.**

**Type IV is the register where dynamical systems, stochastic processes,
and quantum measurement live** — this is where a full treatment of
Schrödinger's Cat would go when worked (§Open work). The atlas lists
Schrödinger as a candidate Type-IV example, but the 6-slot template has
not been filled; only the Unexpected Hanging is worked in that register
today.

### Why UOP organizes TIG's own results

Every Tier D theorem in `FORMULAS_AND_TABLES.md §0` is a UOP
instantiation inside a specific algebraic or geometric substrate:

- **D1 First-G Law** (the first non-coprime element in `{1, …, b}`
  for semiprime `b = p·q` is exactly `k = p`): a Type I resolution
  where `f₁` = "divisibility by b" and `f₂` = SPF(b) together form a
  sufficient pair on `{1, …, b − 1}`.
- **WP57 Crossing Lemma** (for squarefree `n`, `d | n`,
  `g ∈ (ℤ/nℤ)*`: `{A_d, π_DYN(g)}` sufficient ⟺ `M_g` crosses the
  fibers of `A_{n/d}`): the UOP statement at the level of partitions
  of `ℤ/nℤ`.
- **WP51 Flatness Theorem** (`ℤ/10ℤ` carries four irreducible
  structures; the minimum surface holding them is a torus with
  `R/r = T* = 5/7`): a Type I statement — the four structures need the
  torus as the domain on which all four become simultaneously injective
  measurements.
- **WP102 (so(8) = D₄) and WP103 (so(10) = D₅) Lie-algebraic lifts**
  (flow antisymmetrization closes to so(8); CL ∪ BHML closes to
  so(10)): Type II statements in Lie-algebraic classification — within
  the allowed family (compact real simple Lie algebras), the unique
  dimension-28 member is `D₄` and the unique dimension-45 member is
  `D₅`. No alternative exists.
- **WP101 σ-rate theorem** (`σ(N) ≤ C/N` for squarefree `N`): a
  Type IV statement — the magma's non-associativity rate is the rate at
  which `Mag^com` degenerates to `Com` as `N → ∞`; a time-consistency
  statement for a family indexed by `N`.
- **WP62 rejected 7-cycle universality** — a case study in the
  classifier used *against* one of TIG's own conjectures. The original
  "bounded agents universally converge to 7-cycles" claim was a Type IV
  statement (observer-state-dependent); simulation under the classifier
  rejected it. The atlas takes this as evidence the classifier is used
  honestly, not just to confirm favorite results.

The lesson: UOP is not a framework *next to* TIG's algebraic work. UOP
is the principle TIG's algebraic work **obeys**.

---

## Part II — The Lens Supply Catalog

For each of six established mathematical lenses, we document what the
lens supplies in each of the four UOP failure-type slots. Each cell
states: (a) the specific invariant, construction, or technique the lens
provides for that failure type; (b) the specific TIG result (if any)
that instantiates it; (c) an open question or collaborator target that
would fill out the cell.

### Lens 1 — Commutative algebra (Mantero toolkit)

The commutative-algebra lens supplies structural tools for ideals,
modules, and coordinate rings. Its natural subjects are separability
failures that present as unresolved prime decompositions, module
obstructions, or scheme non-reducedness.

| Type | What commutative algebra supplies |
|---|---|
| **I** | **Symbolic powers `I^(ℓ)` as orthogonal measurements.** When an ideal `I` fails to separate two primary components, passing to `I^(ℓ)` refines the measurement. **TIG instance:** WP34 First-G Law is of this form — the coprime window `f = {x : gcd(x, b) = 1}` is separated from its complement by a secondary measurement (SPF). **Open question for Mantero (post-M2):** given the M2-verified non-Cohen-Macaulay result below, what is the shape of the full linear strand `β_{i, i+1}` for `I_CL`, and does this linear strand fit the Mantero-Nguyen focal-matroid framework? |
| **II** | **Hochster-Huneke graph and focal matroid invariants as obstruction detectors.** When the `S₂`-condition fails for a module, no refinement of the ideal family will restore separability. **TIG instance:** the pure-but-not-matroidal bump complex `Δ_B` with 21.9% basis-exchange defect is a Type-II candidate — the focal matroid framework may confirm no matroid completion exists within the allowed family. **Open question:** does `Δ_B` have a focal matroid in the Mantero-Nguyen 2024/2025/2026 sense? |
| **III** | **Primary decomposition and radical ideal construction as domain rebuilders.** When a scheme is non-reduced or has embedded components, primary decomposition fixes the object. **TIG instance:** the reduced coordinate ring `R/√I_CL` of the canonical magma embedding is well-defined and matroidal in the lower half of its Hilbert function, despite the magma's non-associativity. |
| **IV** | **Gröbner degenerations and Rees algebras as dynamic-family handlers.** Ideals evolving under filtration parameter `ℓ` (symbolic powers), `t` (Gröbner degeneration), or `n` (family carrier) are Type-IV objects. **TIG instance:** WP101 σ-rate `σ(N) ≤ C/N` is a Type-IV statement about the magma family indexed by `N`. **Open question:** can Mantero's tools characterize the asymptotic behavior of `pd(A_N)` as `N → ∞` through the compatibility family `{10, 14, 22, 34, …}`? |

**[M2 closure, 2026-04-24]** The v1.0 draft of this atlas said
"Current Hilbert function stabilizes at Krull dim 6 with pd = 4
predicted". Macaulay2 1.22 (compute_betti.m2, betti_output.txt on
`mantero-bridge-2026-04-23`) has now verified the actual invariants:
`numgens = 53`, `codim = 9`, `dim R/I_CL = 1`, `pd = 10`, `depth = 0`,
**not Cohen-Macaulay**, **not Koszul**; reduced Hilbert series
`(1 + 9T − 8T² − T³)/(1 − T)`, i.e. Hilbert function
`(1, 10, 2, 1, 1, …)` stabilising at 1. The Cell-I question is therefore
narrower than v1.0 claimed — the CM property is NOT available, so
symbolic-power arguments that hinge on CM cannot apply; the live
question is the linear-strand structure and its match to Mantero-Nguyen's
framework.

**Lens health:** Cell I now has a sharp, specific open question (the
linear strand) rather than a conjectural one. Cell II open. Cell III
established. Cell IV requires a bridge from symbolic-power theory to
asymptotic combinatorics that neither community has fully built. This
is the specific frontier for the Mantero collaboration.

### Lens 2 — Lie theory (Cartan classification, root systems)

The Lie-theoretic lens supplies algebraic structure at the
infinitesimal level: simple algebras, root systems, invariant bilinear
forms, stabilizer chains. Its natural subjects are
symmetry-classification failures and rigidity statements.

| Type | What Lie theory supplies |
|---|---|
| **I** | **The Killing form as a canonical orthogonal measurement.** When the adjoint representation `f_ad` fails to separate elements of an algebra, the Killing form `K(X, Y) = tr(ad_X ad_Y)` is the canonical second map. **TIG instance:** WP102 Diagnostic 3 — CL's flow antisymmetrization closes to a 28-dim Lie algebra whose Killing form has signature `(0, 28, 0)`, identifying it uniquely as the compact real `so(8)`. The Killing form IS the `f₂` that closes the UOP pair. |
| **II** | **The Cartan classification as a Type-II impossibility certificate.** The classical theorem "the only compact simple Lie algebra of dimension N is [such and such]" is a Type-II argument: no other algebra in the allowed family can have this dimension. **TIG instance:** WP103 §4.6 — dim 45 forces `D₅ = so(10)` uniquely; no alternative classical or exceptional algebra has dim 45. The structural bound of WP103 §7 (`e₈ = 248` unreachable within `gl(10)`) is a further Type-II impossibility. |
| **III** | **The Jacobi identity as a domain validator.** Any alleged "Lie algebra" is a valid object only if Jacobi holds; otherwise 𝒳 is ill-defined. **TIG instance:** Diagnostic 2 in WP102 and WP103 verifies Jacobi numerically with residual `0.00e+00` — the domain is confirmed valid. |
| **IV** | **Lie-group-vs-Lie-algebra correspondence as the dynamic register.** The infinitesimal object (algebra) and the integrated object (group) are Type-IV dual registers. **TIG instance:** none yet explicit. **Open question:** does the SO(10) GUT embedding of Standard Model fermions (via the 16-dim spinor, which requires Clifford algebra `Cl(10)`) live in a Type-IV register where the integrated SO(10) group acts on a space the `so(10)` algebra alone cannot describe? This would formalize why WP103's in-substrate `so(10)` doesn't automatically deliver the 16-spinor — it's a Type-IV jump. |

**Lens health:** Cells I, II, III have sharp TIG instances with
published theorems (WP102 + WP103 verification scripts pass). Cell IV
is genuinely open and would benefit from a representation theorist
(Garibaldi, Baez) who works natively in the group-algebra
correspondence.

### Lens 3 — Operad theory (Huang-Lehtonen, Loday-Vallette)

The operadic lens supplies combinatorial structure at the composition
level: arity-graded spaces of operations, Hilbert series, freeness
criteria. Its natural subjects are separability failures in composition
algebras.

| Type | What operad theory supplies |
|---|---|
| **I** | **ac-spectrum refinement `s_n^ac` as an arity-graded measurement.** When an arity-n composition fails to distinguish two bracketings, passing to arity `n+1` or adding permutation symmetry refines. **TIG instance:** §6.1 of `FORMULAS_AND_TABLES.md` — both CL and BHML saturate `s_n^ac = (2n-3)!!` through `n = 5`, meaning the symmetric operad never collapses under refinement. |
| **II** | **Operadic freeness / saturation as a Type-II maximum.** When an operad generated by a binary operation equals the free commutative magmatic operad `Mag^com`, no additional relations are imposed by the algebra — the operad is structurally maximal within its family. **TIG instance:** §6.1 — CL and BHML are ac-free on 10 elements, placing them in a class with very few finite members (rock-paper-scissors on 3 elements being the only other previously documented finite case). |
| **III** | **Magma-definition checks as domain validators.** Is the binary operation a total function with a closed carrier? A non-closed "operation" yields an ill-defined operad. **TIG instance:** CL and BHML are manifestly total (every cell filled) and closed (values in the carrier); the domain is valid. |
| **IV** | **Asymptotic degeneration as a dynamic model.** The σ-rate theorem `σ(N) ≤ C/N` describes how the operad `Mag^com(N)` generated by the canonical magma on `ℤ/NℤZ` degenerates to `Com` as `N → ∞`. **TIG instance:** WP101. **Open question:** is there an operadic analog of a "thermodynamic limit" that quantifies this degeneration precisely in terms of Hilbert-series convergence? This would be a joint Huang-Lehtonen / Loday-Vallette question. |

**Lens health:** Cells I, II, III are fully populated with published or
pipeline results. Cell IV has the σ-rate theorem as a concrete TIG
instance but no external operadic framework yet identifies it as a
standard asymptotic. This is a clean open question for the
operad-theory community.

### Lens 4 — Ergodic dynamics and transfer operators (Farey spin chains, primon gas)

The ergodic lens supplies spectral structure at the
statistical-mechanics level: partition functions, transfer operators,
spectral gaps, critical temperatures. Its natural subjects are
separability failures at the level of long-time / large-N asymptotic
behavior.

| Type | What ergodic theory supplies |
|---|---|
| **I** | **Generating partitions as refinement measurements.** When a partition `π` of a dynamical system fails to separate orbits, refining to `π ∨ T⁻¹π ∨ T⁻²π ∨ …` is the canonical orthogonal-measurement construction. **TIG instance:** the Crossing Lemma (WP57) is of exactly this form — `{A_d, π_DYN(g)}` becomes sufficient precisely when `M_g` crosses the fibers of `A_{n/d}`, i.e., when the two partitions have disjoint unresolved-pair sets. |
| **II** | **Spectral gap bounds as Type-II obstructions.** When a transfer operator's spectral gap `γ` is bounded below the threshold needed for convergence, no finite composition of observables can restore the missing information. **TIG instance:** WP101 identifies `γ(b) = 1 − 1/φ(b)` as the transfer-operator spectral gap underlying σ-rate; this quantifies the obstruction. |
| **III** | **Ergodic-hypothesis validators as domain checks.** Is the proposed invariant measure actually well-defined and preserved? If not, the domain `𝒳` is ill-defined for ergodic methods. **TIG instance:** §6.5's identity `sinc²(1/2) = (2/3)/ζ(2)` places TIG in the fermionic primon-gas regime, where the invariant measure is the Möbius / squarefree density — well-defined and classical. Domain valid. |
| **IV** | **Thermodynamic limits and critical temperatures as dynamic models.** `β_c` in the Farey spin chain is a Type-IV object: the behavior at `β_c` is qualitatively different from `β < β_c` or `β > β_c`, and the critical phenomenon IS the dynamic signature. **TIG instance:** `T* = 5/7` as a candidate `β_c` in a TIG-specific partition function — currently Tier 3 (structural kinship established via Kleban-Özlük / Fiala-Kleban-Özlük / Technau, but the TIG partition function is open). **Open question:** can a partition function `Z_TIG(β)` over TSML or BHML states be defined whose thermodynamic limit produces a zeta-function ratio with `β_c = T*`? |

**Lens health:** Cells I, II, III have TIG instances with external
citations. Cell IV is the sharpest open question and aligns with
published Riemann-adjacent research programs.

### Lens 5 — Wave mechanics and PDE (BB log-nonlinearity, ξ-field)

The PDE lens supplies analytic structure at the continuum level: wave
equations, nonlinearities, separability, well-posedness. Its natural
subjects are separability failures in composite physical systems.

| Type | What wave mechanics supplies |
|---|---|
| **I** | **Direct maps between wavefunctions and observables as orthogonal measurements.** Position and momentum are the canonical orthogonal pair; their non-commutativity is a Type-I non-injectivity with a rigorous (non-trivial) resolution via Fourier duality. |
| **II** | **The Bialynicki-Birula–Mycielski theorem as a Type-II structural selection.** Among all wave-mechanical nonlinearities, only `V(ξ) = ξ log ξ` preserves separability of composite-system wavefunctions. Any other nonlinearity is a Type-II obstruction: it cannot describe multi-particle systems without violating factorization. **TIG instance:** WP91 deploys this directly — the log-nonlinearity is the unique allowed nonlinearity compatible with the σ-rate continuum limit. |
| **III** | **Well-posedness conditions (Hadamard) as domain validators.** A PDE is a valid object only if existence, uniqueness, and continuous dependence on initial data all hold. **TIG instance:** the ξ-field equation `□ξ = 1 + log ξ` requires Hadamard checks at the derivation level; these are pending proper PDE analysis. |
| **IV** | **The PDE itself as a dynamic model.** A partial differential equation IS a Type-IV diagnostic — it specifies how the domain evolves. **TIG instance:** the ξ-field equation with vacuum `ξ₀ = e⁻¹` and mass-gap `m²_ξ = κ·e` is a complete Type-IV object. DESI 2024 DR1 fit currently `χ² = 15.7` vs `ΛCDM 14.1` (Sprint 14). **Open question:** does Hadamard well-posedness hold rigorously? A PDE analyst would be the right collaborator. |

**Lens health:** Cells I, II fully populated with classical content;
cells III, IV have TIG instances pending rigorous PDE analysis. Open
collaborator target: a mathematical physicist in the Zloshchastiev /
Cazenave-Haraux tradition working on logarithmic Schrödinger /
Klein-Gordon equations.

### Lens 6 — Proof theory and reverse mathematics

The proof-theoretic lens supplies meta-structural tools for formal
systems themselves: consistency, provability, comprehension axioms,
type hierarchies. Its natural subjects are Type-III admissibility
failures involving self-reference or ill-founded objects.

| Type | What proof theory supplies |
|---|---|
| **I** | **Conservativity results as orthogonal-measurement refinements.** A conservative extension of a theory adds new measurements (new symbols, new axioms) without changing the truth values of old statements. **TIG instance:** none yet explicit. |
| **II** | **Incompleteness theorems as Type-II structural obstructions.** Gödel's First Incompleteness Theorem is a Type-II statement in this lens: for any sufficiently expressive consistent formal system, there exist true sentences unprovable within the system. No extension of the allowed proof-family separates true-unprovable from false-unprovable. **TIG instance:** *none yet worked* — a full 6-slot treatment of Gödel is an atlas-new candidate and is listed in §Open work. |
| **III** | **Axiomatic restrictions (ZF, type theory, predicative comprehension) as domain rebuilders.** Russell's Paradox is a Type-III failure resolved by restricting the domain. **TIG instance:** `PARADOX_CLASSIFICATION_MEMO.md` works Russell with the 6-slot template; resolution path = "Restrict to well-founded sets (ZF axioms). Use type theory or predicative comprehension. The paradox dissolves when the domain is properly bounded." The **Liar Paradox** and **Cantor's naive-set-theoretic paradoxes** are widely understood to fit the same pattern but are *not yet worked* in the repo under the full template (§Open work). |
| **IV** | **Ordinal analysis and proof-theoretic strength as dynamic models.** The proof-theoretic ordinal of a system measures how far its consistency can be "climbed." Systems of increasing strength form a Type-IV hierarchy. **TIG instance:** none yet explicit. **Open question:** is there a TIG-internal analog of proof-theoretic strength — e.g., a hierarchy of magmas indexed by their ac-spectrum or σ-rate behavior that mirrors the ordinal hierarchy? |

**Lens health:** Cell III is anchored by the classifier's worked
treatment of Russell. Cells I, II, IV are open — in particular, the
Gödel / Liar / Cantor / Berry examples commonly invoked alongside
Russell are *listed as candidates in the right cells*, but the 6-slot
worked template for each is an atlas-new engineering task, not a
completed repo artifact.

---

## Part III — The CK Runtime: a UOP classifier in formation

The Unified Orthogonality Principle admits a (currently partial) computable
implementation under the name **CK** (Coherence Keeper). This part of the
atlas establishes CK's positioning honestly — what it is, what it isn't, and
what accretion path promotes it to a full lens on its own later.

> **Why CK is in Part III, not Part II row 7.** The six lenses in Part II
> each have (i) a primitive vocabulary, (ii) a toolkit of invariants and
> theorems, and (iii) an **independent research community** that verifies
> and extends results in that vocabulary without the framework's author in
> the loop. CK has (i) and (ii) substantially; it does **not** yet have
> (iii). Placing CK as a seventh row in Part II would invite the correct
> referee critique that the rows are not of the same epistemic kind.
> A dedicated Part III instead says CK is a computable instantiation of
> UOP and a lens-in-formation — a true and defensible framing.

### §III.1 — What CK supplies today

| Piece | Location | Status |
|---|---|---|
| **UOP classifier spec paper** | `papers/WP_PARADOX_CLASSIFIER.md` (on `tig-synthesis`) | **Exists.** Full whitepaper: four types, decision procedure, worked examples. DOI 10.5281/zenodo.18852047. |
| **Web UI** at `coherencekeeper.com/paradox.html` | `Gen12/targets/ck_website/website/paradox.html` | **Exists, client-side.** Hardcodes 8 paradox cases (Zeno, Banach-Tarski, Russell, Unexpected Hanging, Twin Primes, Schrödinger, Gödel, Liar); renders the 6-slot template and verdict in-browser. There is no backend endpoint that accepts free-form input; the UI is presentation-only. |
| **Canonical 6-slot worked examples** | `Gen12/targets/clay/papers/sprint11_tig_bundle_2026_04_08/sprints/PARADOX_CLASSIFICATION_MEMO.md` | **4 of 8 worked** (Zeno I, Banach-Tarski II, Russell III, Unexpected Hanging IV). The other 4 (Twin Primes, Schrödinger, Gödel, Liar) appear in the web UI as aspirational rendering; their full 6-slot templates are [O-2]–[O-4] in §Open work. |
| **D² curvature primitive** | `Gen12/targets/ck_desktop/ck_algebra.c` (CKA_FORCE_LUT, 5D force vector `[aperture, pressure, depth, binding, continuity]`); `ck_d2_dictionary_expander.py` | **Exists.** The 5-dim force vector and D² second-derivative stencil are real runtime primitives. |
| **Operator-activation mapping** | `Gen12/targets/ck_website/website/paradox.html` (hardcoded per paradox); `ck_algebra.c` D2_OP_MAP (dimension-sign → operator) | **Partial.** The web UI pins a specific operator set per hardcoded paradox (e.g., Zeno → `[LATTICE, HARMONY]`; Russell → `[VOID, RESET]`). The generic `d2_vector → operator` mapping is in `ck_algebra.c`. A **dynamic pipeline that takes arbitrary paradox text → d2_vector → operator activation → Type verdict** is **not yet wired end-to-end**; the web UI's activations are display-layer, not a live computation. |
| **`ck_diagnose.py`** at repo root | `ck_diagnose.py` | **Exists, but is not the paradox classifier.** It diagnoses quadrant balance, corridor leakage, and σ non-associativity for arbitrary input against `T* = 5/7`. The paradox classifier is a separate, not-yet-implemented artifact. |

### §III.2 — What CK supplies beyond the abstract classifier

Assuming the CK pipeline is wired end-to-end (§Open work [O-1]), CK would
supply three invariants **not produced by the abstract UOP diagnostic**:

**(i) D² curvature** — a scalar computed via the second-derivative stencil
on the 5D force vector, giving a continuous field-tension reading
orthogonal to the discrete Type verdict. Empirically (from present
hardcoded per-paradox assignments):

- Low D² → clean resolution (Type I)
- Moderate D² → dynamic shift register (Type IV)
- High D² → structural obstruction or ill-defined domain (Type II or III)

**(ii) Operator activation.** A subset of the 10 TIG operators (VOID,
LATTICE, HARMONY, BALANCE, CHAOS, COUNTER, COLLAPSE, BREATH, RESET,
PROGRESS) lights up for each paradox. Two paradoxes of the same Type
can activate different operator sets, revealing finer structural
distinctions than the Type verdict alone. Present hardcoded activations
from `paradox.html` (reported faithfully; these are UI display values,
not computed dynamically):

- Zeno → `LATTICE, HARMONY`
- Russell → `VOID, RESET`
- Liar → `VOID, RESET`
- Twin Primes → `VOID, COLLAPSE, CHAOS`

**(iii) Coherence score `C ∈ [0, 1]`** with three-band colorization
(GREEN ≥ 0.7, YELLOW 0.3–0.7, RED < 0.3). This is CK's headline
human-readable output, orthogonal to but related to the WP61 score
(score_n(f | F) is the UOP-internal number; `C` is the runtime's overall
field-state summary).

These three invariants are **CK-native** — defined within the TIG
framework, without direct analogs in the six established lenses. They
are not unverifiable (each is computable from the input if the pipeline
is wired) but they do require independent validation before they
become externally standard.

### §III.3 — CK as a lens-in-formation (the three criteria)

**Criterion 1 — primitive vocabulary.** CK has it: the 10 operators, the
two canonical tables CL (= TSML_10) and BHML, the 5D force vector,
the T* = 5/7 threshold, the resonance kernel `R(k, f)`, and the D²
curvature primitive. Internally consistent; demonstrably usable on the
8 hardcoded paradox cases.

**Criterion 2 — toolkit of invariants and theorems.** CK has it
substantially. `FORMULAS_AND_TABLES.md §0` (Volumes A–E) catalogs 24+
Tier-D results each with a proof script: First-G Law (D1), Phi fixed
point (D7), 73/28 HARMONY cell counts (D10, D16), sinc² zero law,
Crossing Lemma (WP57), Flatness Theorem (WP51), σ-rate theorem
(WP101), ac-spectrum saturation (§6.1), BB bridge (WP91), and the
Lie-algebraic closures `so(8) = D₄` (WP102) and `so(10) = D₅` (WP103).
External citations connect these to Huang-Lehtonen,
Csákány-Waldhauser, Bialynicki-Birula–Mycielski, Kleban-Özlük,
Fritzsch-Minkowski, and Georgi via
`papers/morphotic_braid/synthesis/RIGOR_MAPPING.md`.

**Criterion 3 — independent research community.** **CK does not yet
have it.** The current CK-engaged research community is: Brayden
Sanders, C. A. Luther, Ben Mayes (WP58 UOP co-author), H. J. Johnson
(Sprint 14 ξ cosmology co-author), M. Gish (Sprint 14 co-author),
and three AI systems (Claude, Claude Code, Grok). Dr. Paolo Mantero
is in warm contact via `mantero-bridge-2026-04-23` but has not yet
published independently on CK's specific claims. No external
researcher has published verification or extension of CK's specific
results outside this loop. This atlas is one explicit step toward
changing that: it is offered as the framework in which established
mathematical lenses can engage CK's results on their own terms.

This criterion is the atlas's most important honesty move. It is not
softened anywhere in this document, and it remains intact even as
CK's other two criteria strengthen.

### §III.4 — How CK relates to the six lenses of Part II

CK is neither a competitor to nor a superset of the six lenses. Its
relationship is specific:

- **CK generates specific instances in each lens's cells.** WP57
  (Crossing Lemma) is the TIG instantiation of Type I for
  ergodic/transfer-operator theory. WP102 and WP103 are TIG
  instantiations of Type I + II for Lie theory. The §6.1 ac-spectrum
  saturation of CL and BHML is the TIG instantiation of Type II for
  operad theory. WP91 is the TIG instantiation of Type II for wave
  mechanics.
- **CK does not claim to supersede any lens.** Each lens in Part II
  supplies tools and theorems that CK invokes, not replaces. CK's
  contribution is to produce specific instances within each lens, not
  to produce new versions of the lens's machinery.
- **CK provides cross-lens organization.** The unique contribution of
  CK inside this atlas is the UOP classifier itself — the organizing
  principle that makes the six lenses comparable and makes concrete
  TIG results legible as instances of a common taxonomy rather than
  as disjoint outputs.

### §III.5 — The path from lens-in-formation to lens

The historical pattern is instructive. Category theory (Eilenberg–Mac
Lane 1945) and operad theory (May 1972, Boardman–Vogt 1973) each
existed as one- or two-person frameworks with vocabulary and toolkit
fully present for decades before they became communities. The
accretion of an independent research community required:

1. Problems from established fields being reformulated in the new
   vocabulary.
2. Those reformulations yielding results unavailable in the original
   fields.
3. Independent researchers adopting the vocabulary to extend those
   results.
4. Journals beginning to accept papers whose primary contribution is
   in the new vocabulary.
5. Graduate students being trained in the new vocabulary.

CK has reached step 1 inside this atlas: the UOP classifier
reformulates paradox analysis in a vocabulary different from proof
theory, set theory, or classical measurement theory. Step 2 is
partially achieved via the specific results cited in Part I's "Why UOP
organizes TIG's own results." Steps 3–5 are future work, dependent on
outreach to — and engagement from — researchers in the Part II
communities.

This atlas is CK's structured invitation to that engagement.

---

## Part IV — The atlas as collaboration map

### Reading the matrix

The six lenses × four types gives 24 cells. Current state (`●` =
filled with a worked repo instance + external citation; `◐` = partial —
filled on paper but implementation or full worked example pending; `○` =
open + specific collaborator target identified):

| Lens | Type I | Type II | Type III | Type IV |
|---|---|---|---|---|
| Commutative algebra | ● (Mantero pipeline, M2 linear strand open) | ◐ (focal matroid, open) | ● (valid reduced domain) | ○ (Mantero-adjacent, open) |
| Lie theory | ● (Killing form, WP102) | ● (Cartan classification, WP102 + WP103) | ● (Jacobi verified, WP102 + WP103) | ○ (spinor/Clifford extension, open) |
| Operad theory | ● (ac-spectrum, §6.1) | ● (ac-free saturation, §6.1) | ● (magma domain valid) | ● (σ-rate, WP101) |
| Ergodic / transfer operator | ● (Crossing Lemma, WP57) | ● (spectral gap γ, WP101) | ● (primon-gas regime, §6.5) | ○ (TIG partition function, open) |
| Wave mechanics / PDE | ● (position-momentum Fourier) | ● (BB separability, WP91) | ◐ (Hadamard for ξ pending) | ● (ξ-field, PRISM-XI, fit pending) |
| Proof theory / reverse math | ○ (no TIG instance yet) | ◐ (Gödel = candidate, not worked) | ● (Russell worked; Liar / Cantor candidates) | ○ (no TIG instance yet) |

### What the empty and partial cells tell us about who to approach next

1. **Lie theory / Type IV** → spinor-Clifford extension. Target:
   **Skip Garibaldi** (exceptional Lie groups, octonions, triality)
   or **John Baez** (octonions, foundations).
2. **Ergodic / Type IV** → TIG partition function with `β_c = T*`.
   Target: a dynamicist in the Kleban-Fiala or Bandtlow tradition; or
   **Giovanni Gallavotti**'s descendants working on transfer operators.
3. **PDE / Type III** → Hadamard well-posedness for the ξ-field
   equation. Target: a PDE analyst in the **Thierry Cazenave /
   Alain Haraux** tradition on logarithmic nonlinear Schrödinger; or
   **Konstantin Zloshchastiev** directly.
4. **Proof theory / Types I, II, IV** → write the 6-slot worked
   templates for Gödel, Liar, Cantor (Type III candidates), and Berry
   (Type I/III borderline). Target: a reverse mathematician
   (**Stephen Simpson** or descendants). The Gödel/Liar/Cantor work
   would also anchor Cell II/III more firmly.
5. **Commutative algebra / Type IV** → asymptotic behavior of
   `pd(A_N)`. Already a candidate extension of Mantero's pipeline;
   ask him directly now that the M2 Cohen-Macaulay question is closed
   (negatively) and the linear-strand question is sharp.

### What the filled cells tell us about who we already have

1. **Paolo Mantero** — commutative-algebra Types I/II/III anchored,
   Type IV adjacent. Warm contact, 3-email exchange, dedicated branch
   `mantero-bridge-2026-04-23`. Primary active collaborator. The M2
   closure reframes the open Cell-I question as "linear-strand shape"
   rather than "is A Cohen-Macaulay?"
2. **Huang–Lehtonen program** — operad theory fully anchored. No
   direct contact yet but the citation chain is established and the
   ac-spectrum paper is the natural bridge.
3. **Fritzsch–Minkowski / Georgi GUT program** — Lie theory
   Types I/II/III anchored via WP102/WP103. The SO(10) physics
   community is the natural downstream.
4. **Kleban–Özlük–Fiala / Technau** — ergodic Types I/II/III
   anchored via §6.5 and the Farey spin chain citation chain.
5. **Bialynicki-Birula / Mycielski / Cazenave / Zloshchastiev** —
   PDE Types II/IV anchored via WP91.

### The strategy this enables

Instead of "chase Paolo until stuck, then open the Lie door," the
strategy becomes:

> *Fill Type-IV cells across all lenses first.* Type-IV is the
> most-open column and is where TIG has the most novel contributions
> (the σ-rate theorem, the Crossing Lemma, the ξ-field equation, the
> asymptotic magma degenerations). Collaborators who can verify
> Type-IV work are the rarest and most valuable.

Then:

> *Fill the remaining ○ cells in order of how easy the collaborator
> handshake is.* Garibaldi and Baez for Lie-IV are approachable via
> the octonions + triality community. Zloshchastiev for PDE-III/IV
> is approachable via citing his recent work. Simpson (or a
> descendant) for Proof-theory-I/IV is the hardest reach.

Each filled cell is a tight, specific pitch — "here's what I have in
your language, here's the open question I want your eyes on." The
atlas organizes these as a queue, not a priority list.

---

## Part V — Open questions as a discrete list

1. **[M2-RESOLVED, 2026-04-24]** ~~Is `A = R/I_CL` Cohen-Macaulay?~~
   *No*. M2 1.22 gives `codim = 9`, `dim = 1`, `pd = 10`, `depth = 0`;
   A is neither Cohen-Macaulay nor Koszul. The replacement open
   question: what is the shape of the full linear strand
   `β_{i, i+1}` for `i = 1, …, 9`? (Commutative algebra, Type I.)
2. Does `Δ_B` have a focal matroid in the Mantero-Nguyen sense?
   (Commutative algebra, Type II.)
3. What is the asymptotic behavior of `pd(A_N)` through the
   compatibility family? (Commutative algebra, Type IV.)
4. Does the SO(10) GUT spinor/Clifford extension realize a Type-IV
   Lie register? (Lie theory, Type IV.)
5. Is there an operadic "thermodynamic limit" formalism for
   `σ(N) → 0`? (Operad theory, Type IV.)
6. Does a TIG-specific partition function `Z_TIG(β)` exist with
   `β_c = T*` and thermodynamic limit equal to a ζ-function ratio?
   (Ergodic, Type IV.)
7. Is the ξ-field equation `□ξ = 1 + log ξ` Hadamard well-posed?
   (PDE, Type III.)
8. Is there a TIG-internal proof-theoretic ordinal for the magma
   family? (Proof theory, Type IV.)

Each question is standalone, addressable by a specific external
expert, and opens a defensible publication path.

### Open work (atlas-new engineering tasks, not yet completed)

These are tasks the atlas *flags* but does not claim are done; they
are the discipline boundary between "what the atlas asserts" and
"what still has to be built":

- [O-1] **Runnable classifier script.** `classify_paradox.py` that
  takes a 6-slot description and outputs `(verdict ∈ {I, II, III, IV},
  score ∈ [0, 1])`. Does not exist in the repo today. Would
  operationalize the paper classifier.
- [O-2] **Schrödinger's Cat 6-slot worked template** — Type IV
  candidate. Not yet worked.
- [O-3] **Gödel's First Incompleteness 6-slot worked template** —
  Type II candidate. Not yet worked.
- [O-4] **Liar Paradox 6-slot worked template** — Type III
  candidate. Not yet worked.
- [O-5] **Cantor's naive-set-theoretic paradox 6-slot worked
  template** — Type III candidate. Not yet worked.
- [O-6] **Berry / Grelling-Nelson / Curry worked templates** —
  atlas-listed Type III candidates. Not yet worked.

---

## Closing note

**The UOP classifier is not a pitch. It is the organizing principle
under which TIG's internal results and external mathematical tools
are co-legible.** The meta-lens atlas is the operational artifact
this principle generates — a map of what we have, what's open, and
whom to approach.

The M2 closure on `I_CL` (2026-04-24) is the first live example of
the atlas functioning as a queue: a v1.0-draft open question ("is A
Cohen-Macaulay?") got pre-empted by a verified answer, and the
queue moved cleanly to the sharper replacement question (the linear
strand). That is exactly how this atlas is meant to operate.

Paolo was the first entry. He is not the whole strategy. The atlas
shows what comes next.

🙏 LATTICE.

— Brayden Sanders & Claude, April 24, 2026

---

## Citations (short form — see referenced files for full proofs)

- **WP58** — `Gen12/targets/clay/papers/sprint12_uop_gut_arc_2026_04_08/WP58_UNIFIED_ORTHOGONALITY_PRINCIPLE.md` — Brayden Sanders & Ben Mayes. UOP Theorem 0.
- **WP61** — `Gen12/targets/clay/papers/sprint12_uop_gut_arc_2026_04_08/WP61_PRODUCTIVE_INCOMPLETENESS.md` — five-category score axis.
- **WP62** — `Gen12/targets/clay/papers/sprint12_uop_gut_arc_2026_04_08/WP62_7CYCLE_BOUNDED_AGENT.md` — 7-cycle universality rejected.
- **Sprint 11 memo** — `Gen12/targets/clay/papers/sprint11_tig_bundle_2026_04_08/sprints/PARADOX_CLASSIFICATION_MEMO.md` — four-type axis, worked examples.
- **WP102** — `papers/wp102/WP102_SO8_IDENTIFICATION.md` — so(8) = D₄.
- **WP103** — `papers/wp103/WP103_SO10_IDENTIFICATION.md` — so(10) = D₅.
- **WP57** — Crossing Lemma.
- **WP51** — Flatness Theorem.
- **WP101** — σ-rate theorem.
- **WP91** — BB log-nonlinearity bridge.
- **WP34 / D1** — First-G Law.
- **M2 betti table** — `mantero-bridge-2026-04-23:papers/sprint_20260423_full/09_mathoverflow_post/betti_output.txt`.
- **FORMULAS_AND_TABLES.md §0, §6.1, §6.5, §19** — root-level tables registry.
