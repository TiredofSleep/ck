# CK Meta-Classification Axes — DoF Kinds × UOP Types × WP61 Categories

**Branch:** `ck`
**Status:** `[RUNTIME ARCHITECTURE]` + `[POSITIONING]`
**Authors:** Brayden Sanders (7Site LLC), in collaboration with Claude (Anthropic)
**Date:** 2026-04-24
**Companion to:** [`DOF_CLASSIFICATION.md`](./DOF_CLASSIFICATION.md)

---

## Part 0 — What this file is

This is the **single file CK consults** when asked to classify a result, a paradox, or a conjecture. It names three independent classification axes, gives the dual-classification matrix at their intersection, and carries a **concrete registry** of TIG results labelled on every axis that applies to them.

Three axes:

- **Axis I — DoF Kinds (K1..K5):** what kind of motion or structure does the object admit? Canonical home: [`DOF_CLASSIFICATION.md`](./DOF_CLASSIFICATION.md).
- **Axis II — UOP Types (I..IV):** if the object is a paradox, why does measurement fail? Canonical home: [`PARADOX_CLASSIFICATION_MEMO.md`](../Gen12/targets/clay/papers/sprint11_tig_bundle_2026_04_08/sprints/PARADOX_CLASSIFICATION_MEMO.md), atlas-level synthesis in [`META_LENS_ATLAS.md`](../papers/meta_lens/META_LENS_ATLAS.md).
- **Axis III — WP61 Categories (I..V):** what kind of *score* does a candidate conjecture earn? Canonical home: [`WP61_PRODUCTIVE_INCOMPLETENESS.md`](../Gen12/targets/clay/papers/sprint12_uop_gut_arc_2026_04_08/WP61_PRODUCTIVE_INCOMPLETENESS.md).

The three axes are **orthogonal.** A single result can carry a DoF Kind (always), a UOP Type (only if it's a paradox), and a WP61 Category (only if it's a conjecture being scored). The registry in §3 shows how they compose on existing TIG material.

**How CK uses this file.** Phase 2 of the meta-level rebuild will create a YAML catalog at `Gen13/targets/ck/brain/catalog/` keyed by the same structure; the cortex will read the catalog at boot and consult it inside `speak()`. This markdown is the human-readable source-of-truth; the YAML is the machine-readable consequence. Editing the YAML is how Brayden and future-Claudes teach CK new classifications without touching code.

---

## Part 1 — The three axes, stated cleanly

### Axis I — DoF Kinds (K1..K5)

Five kinds of degree of freedom, exhaustive over `D1–D30` (proved in [`DOF_CLASSIFICATION.md`](./DOF_CLASSIFICATION.md) §3.2). Each kind answers "what kind of motion, if any, does this object admit?":

| Kind | Name | Diagnostic question | Canonical TIG exemplar |
|---|---|---|---|
| **K1** | Structural / frozen-coordinate | Can its value change without invalidating what it *is*? If no → K1. | σ-diagonal `[0,7,1,3,2,4,5,6,8,9]`; TSML 73 cells |
| **K2** | Reversible symplectic flow | Does the flow preserve a volume form? Is it invertible by a conjugate generator? | `so(8) = D₄` closure (WP102); `so(10) = D₅` (WP103) |
| **K3** | Irreversible dissipative flow | Does the flow monotonically increase an entropy? Is it one-way? | σ-rate spectral gap γ(b) = 1 − 1/φ(b) (WP101); Crossing Lemma (WP57) — at boundary with K2 |
| **K4** | Discrete climbing | Is there an integer index parameterising a ladder of instances? | ac-spectrum `s_n = (2n−3)!!`; TSML_Idempotent rank 9 → 10 upgrade |
| **K5** | Degenerative / limiting | Does taking `N → ∞` change the *category* of the object? | Mag^com → Com as `N → ∞`; BB bridge □ξ = 1 + log ξ |

**Cross-kind constants** (K1 by default, with structural role across K1–K5): T* = 5/7; S* = 4/7; ξ₀ = e⁻¹; 4/π² = sinc²(1/2); α̂ = 2. See [`DOF_CLASSIFICATION.md`](./DOF_CLASSIFICATION.md) §3.3.1 + Finding 4 in Pass-2 verification.

### Axis II — UOP Types (I..IV)

Four types of paradox, classified by the mechanism through which measurement fails to pin down the object. Canonical definitions from [`PARADOX_CLASSIFICATION_MEMO.md`](../Gen12/targets/clay/papers/sprint11_tig_bundle_2026_04_08/sprints/PARADOX_CLASSIFICATION_MEMO.md):

| Type | Name | Mechanism | UOP applies? | Canonical exemplar |
|---|---|---|---|---|
| **I** | Injectivity Failure | `F ⊂ Valid(𝒳)`, `R(F) ≠ ∅`, `∃ fₙₑₓₜ` with positive score | Directly applies — adding maps from the allowed family resolves it | Zeno's paradox (add geometric series sum map) |
| **II** | Missing Invariant | `F ⊂ Valid(𝒳)`, `R(F) ≠ ∅`, but no allowed `fₙₑₓₜ` has positive score | Classifies but does not resolve — the invariant isn't in the allowed family | Banach–Tarski (measure not in orbit family); Gödel II incompleteness |
| **III** | Admissibility Failure | Proposed `𝒳` or `f` is not well-defined | Identifies but does not repair — the domain itself is invalid | Russell's paradox, Liar paradox, Cantor on set of all sets, Berry's paradox |
| **IV** | Time-Consistency Failure | `𝒳` or `F` is observer-state-dependent — static UOP setting breaks down | Does not apply — requires dynamic framework | Unexpected Hanging; Schrödinger's cat (measurement-entangled observer) |

**Mutual distinctness** (*Theorem 1 of the memo*): I ≠ III proved formally; I ≠ II, II ≠ III, III ≠ IV proved via UOP-applicability grouping. **Four-type exhaustiveness** is a structural schema, not a formal theorem — see **OQ-6** in §4.

### Axis III — WP61 Categories (I..V)

Five categories of score outcome for a candidate conjecture, sorted by what the score does to the knowledge base. Canonical definitions from [`WP61_PRODUCTIVE_INCOMPLETENESS.md`](../Gen12/targets/clay/papers/sprint12_uop_gut_arc_2026_04_08/WP61_PRODUCTIVE_INCOMPLETENESS.md):

| Category | Name | Score outcome | Knowledge-base effect |
|---|---|---|---|
| **I** | Complete | `score = 1` and bounded | Conjecture resolves `R` to a singleton; add to theorem list |
| **II** | Partial | `0 < score < 1` | Reduces `R`, does not resolve it; add to refinement queue |
| **III** | Refinement-Only | `score > 0` only after redefining observables | Forces restatement; bookkeeping update, not new theorem |
| **IV** | Invariant-Isolating | `score = 0` but identifies what invariant is missing | Meta-contribution: tells you what to look for next |
| **V** | Invalid | Conjecture ill-formed under UOP admissibility | Rejected at the door; same as Type III |

**Relation to Axis II:** Category V ≡ Type III in outcome (both reject the conjecture as ill-formed). Other categories are orthogonal to UOP types. See [`VOCABULARY_RECONCILIATION.md`](../papers/meta_lens/VOCABULARY_RECONCILIATION.md) for the full reconciliation.

---

## Part 2 — The DoF × UOP matrix (5 × 4)

Replicated inline from [`DOF_CLASSIFICATION.md`](./DOF_CLASSIFICATION.md) §3.5 so the reader (CK) doesn't have to jump to another file. Row = DoF Kind; column = UOP Type. Cell content = characteristic obstruction at that crossing, plus a TIG exemplar when known. Empty cells are research invitations — see §4 OQ-5.

| | **Type I** (Injectivity) | **Type II** (Missing Invariant) | **Type III** (Admissibility) | **Type IV** (Time-Consistency) |
|---|---|---|---|---|
| **K1 Structural** | Add a structural coordinate that distinguishes the currently-indistinguishable states | Invariant living outside the structural-coordinate family is needed | Proposed coordinate set is not a valid chart | *empty* |
| **K2 Reversible flow** | **Crossing Lemma at boundary (WP57).** Dynamics become injective above threshold; below, orbit + rotation-family insufficient | Measure-preserving invariant missing from the Lie-bracket family. **Banach–Tarski at K2 × II** | Proposed flow generator is not in the Lie algebra | *empty* |
| **K3 Irreversible flow** | σ-rate theorem at K3 × I — `σ(N) ≤ C/N` forces injectivity above threshold | Entropy is the only invariant in the allowed dissipative family; no further invariant exists | Proposed dissipation kernel is not positive-semidefinite | *empty* |
| **K4 Climbing** | Index climbs past injectivity boundary; ac-spectrum reveals fix. **D3 sinc²(1/2) = 4/π² at K4 × I** | Ladder is invariant-free beyond some step; no scoring climb exists | Proposed step not in the climbing family | *empty* |
| **K5 Limiting** | Object resolves only in `N → ∞` limit; finite truncation insufficient | The limit-category's invariant is not in the finite-N family. **Mag^com → Com at K5 × II** | Proposed limit does not exist in the category | **Unexpected Hanging at K5 × IV**; Schrödinger's cat (quantum observer-state dependence) |

**Column IV is nearly empty** because Type IV paradoxes require a dynamic observer — most TIG results fix the object-set before analysis. The two non-empty K5×IV cells are the "classic" Type IV paradoxes inherited from the literature; TIG-native K1..K4 × IV examples are an open search (**OQ-8**).

**Row K2 is the densest** because the Lie-algebraic closures (WP102, WP103) saturate the Type I–III columns under the so(8)/so(10) flow generators — one concrete example per column.

---

## Part 3 — Dual-classification registry

Each row is a TIG object (result, paradox, claim, or conjecture) with its labels on every axis that applies. Empty cells use `—`. For theorems, Axis II (UOP Type) is `n/a (theorem)` because UOP types classify *paradoxes*, not proved results.

| Object | Canonical home | Axis I: DoF Kind(s) | Axis II: UOP Type | Axis III: WP61 Cat | Notes |
|---|---|---|---|---|---|
| **Crossing Lemma** (WP57) | [`sprint10_flatness_2026_04_06`](../Gen12/targets/clay/papers/sprint10_flatness_2026_04_06/) | K3 → K2 (boundary) | I (at threshold) | I | Injectivity threshold of dissipative dynamics |
| **σ-rate theorem** (WP101) | [`sprint14_prism_xi_2026_04_10`](../Gen12/targets/clay/papers/sprint14_prism_xi_2026_04_10/) | K3 + K5 | n/a (theorem) | I | `σ(N) ≤ C/N` — spectral gap + asymptotic |
| **Flatness Theorem** (WP51) | [`sprint10_flatness_2026_04_06`](../Gen12/targets/clay/papers/sprint10_flatness_2026_04_06/) | K1 + K5 | n/a (theorem) | I | Four irreducibles can't coexist flat → degeneration |
| **UOP Theorem 0** (WP58) | [`sprint12_uop_gut_arc_2026_04_08`](../Gen12/targets/clay/papers/sprint12_uop_gut_arc_2026_04_08/WP58_UNIFIED_ORTHOGONALITY_PRINCIPLE.md) | Meta-level (classifies measurement) | n/a (meta-theorem) | I | Joint-injectivity ⟺ sufficiency; 5 classical theorems fall out |
| **WP61 Productive Incompleteness** | [`sprint12_uop_gut_arc_2026_04_08`](../Gen12/targets/clay/papers/sprint12_uop_gut_arc_2026_04_08/WP61_PRODUCTIVE_INCOMPLETENESS.md) | Meta-level (classifies scores) | n/a (classification schema) | — | Defines Axis III itself |
| **WP62 7-cycle bounded agent** | [`sprint12_uop_gut_arc_2026_04_08`](../Gen12/targets/clay/papers/sprint12_uop_gut_arc_2026_04_08/WP62_7CYCLE_BOUNDED_AGENT.md) | *rejected* | IV → rejected | V (Invalid) | Universal-attractor claim failed UOP admissibility |
| **First-G Law** (D1) | [`FORMULAS_AND_TABLES.md`](../FORMULAS_AND_TABLES.md) §0 | K1 | n/a | I | Proved over 36,662 semiprime cases |
| **Sinc² Zero Law** (D3 / D25) | [`FORMULAS_AND_TABLES.md`](../FORMULAS_AND_TABLES.md) §0 | K1 (identity) + K5 (continuum) | n/a | I | `sinc²(1/2) = 4/π²`; Φ-loop closure |
| **TSML 73 HARMONY cells** (D10) | [`ck_olfactory.py`](../Gen12/targets/ck_desktop/ck_sim/being/ck_olfactory.py) + [`CL_TABLE_EXPLICIT.md`](../papers/CL_TABLE_EXPLICIT.md) | K1 | n/a | I | Verified independently in Pass-2 |
| **BHML 28 HARMONY cells** (D16) | [`BHML_TABLE_EXPLICIT.md`](../papers/BHML_TABLE_EXPLICIT.md) | K1 | n/a | I | Analogous static count |
| **Coherence equation `C = 0.4(1−E) + 0.35A + 0.25K`** | [`CKIS/ck_being.py`][ck_being] §3.3 | K3 (E read) + K1×K2 design-target (A) + K2×K4 design-target (K) | n/a (runtime formula) | — | §3.3.1: `K_weight/A_weight = 5/7 = T*` exactly |
| **WP102 so(8) = D₄ closure** | [`WP102_SO8_IDENTIFICATION.md`][wp102] | K2 | n/a (theorem) | I | Antisymmetrization of 6 CL flow operators |
| **WP103 so(10) = D₅ closure** | [`WP103_SO10_IDENTIFICATION.md`][wp103] | K2 | n/a (theorem) | I | Fritzsch–Minkowski / Georgi GUT algebra |
| **Waldschmidt α̂(I_B) = 2** | [`CL_MATROID_DISTANCE.md`][mantero] | K1 (asymptotic invariant, fixed value) | n/a | I | Proved on the bump complex |
| **Bottom-strand Betti `β_{8,10}=1, β_{9,11}=2, β_{10,12}=1`** | [MO #510662](https://mathoverflow.net/questions/510662) + [`04_mantero_bridge/`][mantero-bridge] | K1 (structural invariant of `A = R/I_CL`) | n/a | — | M2-verified; structural explanation is open |
| **Zeno's paradox** | [`PARADOX_CLASSIFICATION_MEMO.md`](../Gen12/targets/clay/papers/sprint11_tig_bundle_2026_04_08/sprints/PARADOX_CLASSIFICATION_MEMO.md) §4 | K4 (stepping through intervals) | I | I (resolved by adding duration map) | Canonical Type I exemplar |
| **Banach–Tarski** | [`PARADOX_CLASSIFICATION_MEMO.md`](../Gen12/targets/clay/papers/sprint11_tig_bundle_2026_04_08/sprints/PARADOX_CLASSIFICATION_MEMO.md) §4 | K2 (orbit-group flow) | II | II (no measure in allowed family) | Canonical Type II exemplar |
| **Russell's paradox** | [`PARADOX_CLASSIFICATION_MEMO.md`](../Gen12/targets/clay/papers/sprint11_tig_bundle_2026_04_08/sprints/PARADOX_CLASSIFICATION_MEMO.md) §4 | — (domain ill-formed) | III | V | Canonical Type III exemplar |
| **Unexpected Hanging** | [`PARADOX_CLASSIFICATION_MEMO.md`](../Gen12/targets/clay/papers/sprint11_tig_bundle_2026_04_08/sprints/PARADOX_CLASSIFICATION_MEMO.md) §4 | K5 (object set depends on observer state) | IV | — (non-scored — observer-dependent) | Canonical Type IV exemplar |
| **Gödel incompleteness** | [`paradox_godel_type2.md`](../papers/meta_lens/worked_paradoxes/paradox_godel_type2.md) | — (meta-level) | II | IV (invariant-isolating) | Self-reference blocks decidability |
| **Liar paradox** | [`paradox_liar_type3.md`](../papers/meta_lens/worked_paradoxes/paradox_liar_type3.md) | — | III | V | Semantic self-reference |
| **Cantor on set of all sets** | [`paradox_cantor_type3.md`](../papers/meta_lens/worked_paradoxes/paradox_cantor_type3.md) | — | III | V | Domain ill-formed |
| **Berry's paradox** | [`paradox_berry_type3.md`](../papers/meta_lens/worked_paradoxes/paradox_berry_type3.md) | — | III | V | Referential circularity |
| **Schrödinger's cat** | [`paradox_schrodinger_type4.md`](../papers/meta_lens/worked_paradoxes/paradox_schrodinger_type4.md) | K5 (quantum limit) | IV | — | Observer-entangled state |
| **Twin Primes conjecture** | — | K4 (climbing through prime pairs) | I *or* II, undetermined until conjecture resolved | II or III depending on resolution | **Conditional-Type paradox** — see OQ-9 |

**Reading the registry.**

1. Where Axis II is `n/a (theorem)`, the object is a proved result, not a paradox. It still earns a DoF Kind and a WP61 Category (usually I = Complete).
2. Where Axis I is `—`, the object is meta-level (classifies or scores other objects) rather than being itself a DoF-bearing object.
3. Where Axis III is `—`, the object was not scored under the WP61 schema (e.g., an observer-state-dependent paradox whose score depends on dynamic framework).
4. Empty cells across all three axes do not exist — the registry only lists objects with at least one live label.

**Observation** (cf. Pass-2 Finding 2). The TIG-native theorems (Crossing Lemma, σ-rate, Flatness, so(8)/so(10)) are **multi-kind but single-type-or-none** — the UOP Type axis mostly marks paradoxes, while DoF Kinds span the theorems richly. This is consistent with the §3.2 claim that CL/BHML are distinguished by exhibiting all five DoF kinds simultaneously.

---

## Part 4 — Open questions (OQ-1 through OQ-9)

Carried forward from DOF note §5 and extended with the cross-axis questions Pass-2 surfaced:

**OQ-1 — Coherence-equation runtime wiring.** Current `ck_being.py` reads `E, A, K` as plain scalar bookkeeping (lines 577–610); the design-target "K3 read / K1×K2 read / K2×K4 read" is not implemented. Pass 1 verified the **weight identity** `K_weight / A_weight = 5/7 = T*` — the structural significance of the weights is real; the runtime wiring is still TODO.

**OQ-2 — E weight derivation.** The numerator `8` in `E = 8/20` is structurally significant (matches BREATH index, so(8) dimension, octonion dimension) but no independent derivation has been produced. See [`pass1_weights.py`](./pass1_weights.py) for the current state.

**OQ-3 — D26–D30 classification.** The Lie-algebraic tower is claimed to populate Kind 2 densely. Each of D26, D27, D28, D29, D30 needs an explicit (Kind(s), Type if paradox, Category) label filed against the registry.

**OQ-4 — Runtime multi-kind survey.** The claim "first deployed runtime that tracks all five kinds simultaneously" is marked `[CONJECTURAL — no survey conducted]`. A systematic pass over ancient and modern runtimes would either confirm the uniqueness or relativize it.

**OQ-5 — 5×4 matrix cells with no named example.** 15 of 20 cells in §2 are empty. Some may be genuinely empty (structural impossibility); others are research invitations. Specifically: K1 × II, K1 × III, K1 × IV, K3 × II, K3 × III, K3 × IV, K4 × II, K4 × III, K4 × IV, K5 × I, K5 × III.

**OQ-6 — UOP four-type exhaustiveness.** The Sprint 11 memo explicitly states the four-type classification is "a structural schema, not a formal theorem." Types I and III admit formal separation; Types II and IV require fixing the "allowed family" and "observer-state independence" notions. A fully formal exhaustiveness theorem would either require those fixings or admit a genuine **Type V** (see OQ-7 below for a candidate).

**OQ-7 — Cross-kind constants meta-category.** `{T*, S*, ξ₀ = e⁻¹, 4/π² = sinc²(1/2), α̂ = 2}` are all K1 by default (fixed values) but structurally span K1–K5. Worth formalising as a named meta-category with its own axis? Proposed sub-registry: each constant carries (value, appearance contexts, kinds it bridges). Phase 2 will put this in `cross_kind_constants.yaml`.

**OQ-8 — TIG-native Type IV paradoxes.** Column IV of the §2 matrix is nearly empty because TIG results fix the object-set before analysis. Are there TIG-native objects where the object-set genuinely depends on the observer state? Candidate: the σ-rate measurement itself under a running CK that learns `σ` during measurement. Unclear whether this is Type IV or just Type I with a delayed observable.

**OQ-9 — Conditional-Type paradoxes.** Twin Primes conjecture: if true, Type I (resolution adds a density estimate to the allowed family); if false, Type II (no density exists in the allowed family). Its UOP-Type is **undetermined until the conjecture is resolved**. This suggests a genuine new category of paradox whose type *depends on the resolution of an open mathematical question*. Worth atlas §5 addendum per [`twin_primes.md`](../papers/meta_lens/worked_paradoxes/) (file delivery pending, per VERIFICATION_PASSES_MASTER_HANDOFF.md).

---

## Part 5 — How CK uses this file at runtime (Phase 2 design)

This file is the **human-readable source of truth.** Phase 2 produces the machine-readable consequences:

1. `Gen13/targets/ck/brain/catalog/dof_kinds.yaml` — K1..K5 with diagnostic questions and TIG exemplars from Part 1 Axis I.
2. `Gen13/targets/ck/brain/catalog/paradoxes.yaml` — 6-slot templates (Objects / Observables / UOP verdict / Type / Fix / Cite) for each paradox, migrated from `papers/meta_lens/worked_paradoxes/`.
3. `Gen13/targets/ck/brain/catalog/cross_kind_constants.yaml` — T*, S*, ξ₀, 4/π², α̂, sinc²(1/2).
4. `Gen13/targets/ck/brain/catalog/registry.yaml` — the Part 3 dual-classification registry.

The cortex's loader (Phase 2 Step 4, `cortex_catalog.py`) reads all four YAMLs at boot and exposes:

- `classify(text) → {kind, type, category, confidence}` — rule-based dispatch via [`classify_paradox.py`](../papers/meta_lens/classify_paradox.py).
- `lookup_dof(name) → kind_entry` — return the entry for a named DoF kind.
- `lookup_paradox(name) → six_slot_entry` — return the 6-slot template for a named paradox.
- `registry_for(object_name) → (kind, type, category)` — return the dual-classification triple for a TIG object.
- `list_cross_kind_constants() → [constant_entry...]` — enumerate the constants with their bridging kinds.

Website endpoints (Phase 3):

- `/paradox/classify?text=...` — hits the loader's `classify()`.
- `/dof/taxonomy` — returns the K1..K5 table as JSON.
- `/meta/registry` — returns the full Part 3 registry as JSON.

**The workflow Brayden will use.** Add a new paradox or result by editing one of the YAML catalogs (not code). Restart the server. CK loads the new entry and can classify queries against it. Every addition is a small, diff-reviewable, git-tracked data change. The engine remains untouched.

---

## Part 6 — Provenance

- **Pass 1** (2026-04-23 → 2026-04-24): coherence-equation weight identity verified in [`pass1_weights.py`](./pass1_weights.py). Finding: `K_weight / A_weight = 5/7 = T*` exactly.
- **Pass 2** (2026-04-24): exhaustiveness over D1–D25 confirmed against the five-kind taxonomy. Finding: UOP Types are orthogonal to DoF Kinds; multi-kind results are the majority among important theorems. See [`DOF_CLASSIFICATION.md`](./DOF_CLASSIFICATION.md) §3.2.
- **Pass 3** (2026-04-24): overlap with Foundation Tour Part 0.1 resolved — DOF note stays in `speculations/`, vocabulary-hygiene policy inherited. See [`FOUNDATION_TOUR_VERIFIED.md`](../papers/meta_lens/FOUNDATION_TOUR_VERIFIED.md) Part 0.1.
- **Registry construction** (this file, 2026-04-24): dual-classification triples constructed from existing TIG papers; entries labelled `n/a (theorem)` where UOP Type does not apply, `—` where an axis is silent.

[ck_being]: https://github.com/TiredofSleep/ck/blob/paradox-classifier-2026-04-24/CKIS/ck_being.py
[wp102]: https://github.com/TiredofSleep/ck/blob/paradox-classifier-2026-04-24/papers/wp102/WP102_SO8_IDENTIFICATION.md
[wp103]: https://github.com/TiredofSleep/ck/blob/paradox-classifier-2026-04-24/papers/wp103/WP103_SO10_IDENTIFICATION.md
[mantero]: https://github.com/TiredofSleep/ck/blob/paradox-classifier-2026-04-24/papers/mantero/CL_MATROID_DISTANCE.md
[mantero-bridge]: https://github.com/TiredofSleep/ck/tree/mantero-bridge-2026-04-23/papers/sprint_20260423_full/04_mantero_bridge
