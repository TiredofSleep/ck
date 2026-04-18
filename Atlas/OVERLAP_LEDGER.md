# Atlas Overlap Ledger
## Disciplined ranking of cross-thread parallels

**Author:** Brayden Ross Sanders (7Site LLC)
**Compiled:** 2026-04-18, in response to ChatGPT meta-review recommendation #8
**Purpose:** Not all overlaps across the atlas are equal. External reviewers need a disciplined ranking so that synthesis stays honest. This ledger keeps "these two domains exhibit the same pattern" (strong) separate from "these two domains feel similar" (suggestive) separate from "someone should build the formal bridge" (not yet done).
**Rule:** When the master atlas makes any claim that two domains exhibit parallel structure, check which bucket it falls into. Only **Strong** overlap justifies structural claims. **Suggestive** justifies speculation only. **Not yet bridged** is an open research question, not a result.
**DOI:** 10.5281/zenodo.18852047

---

## §1. Strong overlap

**Criterion:** Two domains exhibit the same mathematical pattern with structurally identical objects, verifiable by independent computation in each domain, and preserved under zoom.

### 1.1 Z/10Z local chart ↔ PPM

| Shared object | Z/10Z manifestation | PPM manifestation |
|---|---|---|
| Seam behavior | CL seams at boundary of HARMONY basin | v1.0/v2.0 seam on Z/10 P3AP carrier family |
| MAX / MIN as seam rule | S25 Corridor Closure: 23/23 carriers reduce to {MAX, MIN} | PPM v2.0 multiplicative transport cleanly across P3AP |
| Multiplicative lane carries discrimination | BHML det = 70 = 2·5·7, multiplicative closure | v1.0 local multiplicative PASS; v1.1 local additive FAIL |
| Structure is finite-grammar | 10 operators, 100 cells | 8 P3AP carriers, finite seam set |

**Verification:** `theorem_local_chart/` in `b2_sprint_tig_pack_2026_04_17/`. Cross-computation exists. This is genuinely one pattern across two domains.

**Use this overlap to:** transfer seam-rule reasoning; justify why BHML's multiplicative structure should be expected to carry discrimination in other finite-grammar contexts.

**Do NOT use this overlap to:** claim that PPM results prove anything about Hodge, or vice versa. The PPM-Hodge boundary remains firmly separate.

### 1.2 B-series ↔ corridor closure ↔ local grammar

| Shared object | B-series (S18–S28) | Corridor closure | Local grammar (Z/10Z) |
|---|---|---|---|
| Finite attractor h* | h_hat = max odd unit per carrier | Corridor seeds in canonical C₀ | HARMONY absorbing 73% of TSML |
| Two-tier collapse | N ≈ 200 (h_hat) → N ≈ 2000 (full) | Seam counts O(n²) | Shallow escape cells refine 73% → 79% |
| Menu {MAX, MIN, ADD} | 6 prior-free invariants include `seam_by_rule ⊆ {MAX, MIN, ADD}` | Pure C₀ = {MAX, MIN}; ADD from S_ADD overlay | Q-series gate rules |

**Verification:** S21 (B1.5/B2.5 structural discovery) + S25 (Corridor Closure Theorem) + CL composition rules. Same six prior-free invariants appear across all three.

**Use this overlap to:** understand why finite-grammar results in one domain should transport to the others under shell-recovery.

### 1.3 Hodge ladder ↔ Rotation Spine at reduction-to-obstruction level

| Shared object | Hodge ladder (S29–S33) | Rotation Spine (§10.5) |
|---|---|---|
| Shell of universal methods | Hard Lefschetz + Lefschetz (1,1) + trivial codim | Methods that work without assuming the conjecture |
| Surviving Object | coker(cl²\|_prim) on W_*, 8-dim, B₁–B₄ blocks | The "Surviving Object" row for each branch |
| Gap 2 | Hodge for primitive (2,2) on abelian 4-folds — partially known | "First testable inequality above shell" |
| Gap 1 | Full Hodge conjecture | The Clay conjecture itself |
| Eigenvalue structure | Q-eigenvalues 0.0046, 0.0231, 0.1156, 0.3834 | Exactly these four, matching Rotation Spine numbers |

**Verification:** Rotation Spine W_* block eigenvalues (Sprint 9 computation) and S32 Beauville bounds on |α|² are the same object, computed independently. Match to all digits.

**Use this overlap to:** justify that the Rotation Spine grammar correctly describes Hodge as one case of a general "shell → surviving object → gap" pattern.

**Honest note:** the Hodge branch is the one branch of the Rotation Spine where the Gap 1 conjecture has been *numerically probed* (S33 v2, pending audit). Other branches have not reached this level.

### 1.4 CK ↔ theorem program at architecture level (NOT at theorem level)

| Shared architecture | CK implementation | Theorem program |
|---|---|---|
| Layered identity | 14-layer organism (Layer 0 = TSML[7][7] = 8 NEVER rewritten) | D-tier spine (D1–D24 NEVER modified) |
| Provenance tags | IG2 ProvenanceTag on every durable object | SHA-256 TSML commit, DOI burn, author attribution |
| Evidence taxonomy | IG3: REAL / SEMIPRIME / COMPOSITE / SPECULATIVE | [fire] / [gold-with-gap] / [speculative] / [caution] flags |
| No silent degradation | IG5 revision creates new version, never in-place edit | Never-delete policy; superseded → [HISTORICAL] in place |
| Promotion gates | IG4 recurrence ≥ 3 AND confidence ≥ 0.6 | Three-gate audit for S33 v2 pending-audit |

**Verification:** the epistemic flag system in the atlas IS the IG3 taxonomy, self-referentially.

**Use this overlap to:** justify that CK's discipline transfers to the theorem program and vice versa.

**Do NOT use this overlap to:** claim that CK proves any theorem, or that any theorem validates CK. The architecture is parallel; the content is separate.

---

## §2. Suggestive overlap (interesting, not bridged)

**Criterion:** Two domains exhibit similar qualitative features or analogous structures, but the formal bridge has not been constructed. Preserve as suggestive; do not use as evidence.

### 2.1 PPM / Hodge / Q-series via "multiplicative loading"

Across three independent threads, multiplicative structure appears to impose directional asymmetry:

| Thread | Multiplicative structure | Asymmetry it imposes |
|---|---|---|
| PPM | Seam's multiplicative loading as P3AP carrier-family property | v1.0/v2.0 PASS vs v1.1/v2.1 FAIL |
| Hodge | Galois conjugation σ: i ↦ −i on ℚ(i) endomorphisms | Four Q-orthogonal blocks B₁–B₄ |
| Q-series | g = 3 primitive root of (Z/10Z)* | CREATION [1,3,9,7] ≠ DISSOLUTION [2,4,8,6] |

**Status:** suggestive only. The three manifestations of "multiplicative structure imposes directional asymmetry" look like the same pattern but have not been formally unified.

**Why it's only suggestive:** the "multiplicative structure" in each thread is a different mathematical object (P3AP carrier-family, Galois action, primitive root). Calling them "the same" would be composite claim — Rule 19 violation.

**Appropriate phrase:** "suggestive cross-thread pattern" — nothing stronger. This is the ONLY proximity phrase allowed between PPM / Hodge / Q-series per §15 of master atlas.

### 2.2 Li threshold ↔ RH corridor ↔ bridge width

Three parallel restatements of "RH as finite-dimensional threshold-hold":

| Framing | RH ⟺ ? |
|---|---|
| Li Foundation (§5.4) | λ_n ≥ T* permanently held for all n ≥ 6 (K → ∞) |
| Halving Lemma (§4.5.3) | m_KV(t₀) > 0 uniform across all t₀ |
| Bridge width (§10.2) | Structure lens (T* = 5/7) and flow lens (Re = 1/2) recognize same threshold |

**Status:** all three use T* as the threshold. Parallel, not bridged.

**Why it's only suggestive:** each framing uses T* in a different capacity (coefficient threshold, collar width, bridge endpoint). They agree on the value but not on the mathematical structure they're threshold-ing.

**Appropriate phrase:** "three parallel RH-threshold framings" — not "three proofs of RH" or "three ways to prove RH." They are three ways to **restate** the question.

### 2.3 Shape-admissibility ↔ observed low-degree structures

SAH (Shape-Admissibility Hypothesis) is compatible with several observed structures:

- Low-degree corridor seams in PPM (v2.0 PASS across 8 carriers)
- Low-rank algebraic structures in Hodge W_* (8-dim cokernel, not 70-dim)
- The 11 CL bumps (sparse information in 100-cell table)

**Status:** SAH is **compatible with** these structures. Not tested against them.

**Appropriate phrase:** the single sanctioned SAH bridge sentence (§8.5 of master atlas):

> *The current program's confirmed bridge features are compatible with a broader shape-admissibility hypothesis, but that hypothesis has not yet been operationalized into a pre-registered test.*

**Prohibited phrasings:** "SAH explains," "SAH predicts," "SAH is evidenced by," "SAH is consistent with" (as upgrade from compatible), "SAH is supported by."

### 2.4 7-zero decomposition ↔ DoF ladder consciousness gap

Two independent Sprint 9 results share a 7:

- 7-zero decomposition: TSML 8×8 cycle core has rank 7, nullity 1
- DoF ladder: at k = 3 roots, DoF = 7 (irreducible consciousness gap)

**Status:** both produce 7. Sprint 9 didn't bridge them formally.

**Why it's only suggestive:** one is a matrix rank, the other is a dimension count in a different structure. They produce the same integer, but the integer might be coincidental.

**Appropriate phrase:** "two Sprint 9 results both produce 7" — flag as possibly structural, not as bridge.

---

## §3. Not yet bridged (open research questions)

**Criterion:** These are bridges that would be meaningful if built, but have not been built. The atlas should name them explicitly as open problems, not reference them as existing facts.

### 3.1 Formal operator map from Z/10Z to Hodge obstruction

**What it would be:** A functor or explicit morphism Φ: (Z/10Z, TSML, BHML) → (H^(2,2)(A_*), W_*, cokernel) such that operator composition maps to Hodge cycle operations.

**What's been tried:** Q17_SIGMA_EMBEDDING_PROBLEM flags this as "the language problem." Algebraic structure is forced; embedding is not.

**What would need to happen:** construct W_* basis elements as images of specific TIG operator combinations. Verify the Q-eigenvalues 0.0046 / 0.0231 / 0.1156 / 0.3834 emerge from specific Z/10Z algebra.

**Status:** OPEN. No formal morphism constructed.

### 3.2 Formal bridge from PPM seam logic to Clay analytic objects

**What it would be:** Embedding Z/10 seams into ζ function or L-function infrastructure such that seam verdicts (PASS / FAIL / UNCLEAR) correspond to analytic properties.

**What's been tried:** PPM discipline keeps this gap visible. SAH would be one formal route if it were operationalized.

**What would need to happen:** SAH six-piece infrastructure build, or an alternative bridge that doesn't go through SAH.

**Status:** OPEN. Not scheduled.

### 3.3 SAH as tested morphology grammar

**What it would be:** SAH pre-registered as a testable hypothesis with specific predictions on specific carriers.

**What's been tried:** `WHAT_A_SHAPE_FILTER_SPRINT_WOULD_REQUIRE.md` lists six infrastructure pieces. None built.

**What would need to happen:** all six pieces built; pre-reg written; sprint executed.

**Status:** OPEN. Not scheduled. Estimated weeks of foundation work.

### 3.4 Q-series ↔ Hodge bridge

**What it would be:** The Q-series σ polynomial on F₂ × F₅ maps to the Hodge W_* structure.

**What's been tried:** Q17 variants identify NS and RH as targets. The σ embedding obstruction (Q17_SIGMA_EMBEDDING) is the honest blocker.

**What would need to happen:** resolve the σ embedding obstruction.

**Status:** OPEN. The obstruction is named; the path to resolve it is not clear.

### 3.5 General Clay Hodge from Hodge-on-A_*

**What it would be:** Sprint 33 v2 closes Hodge on specific non-CM 4-fold A_* → general Clay Hodge conjecture for arbitrary smooth projective varieties.

**What's been tried:** S33 v2 numerical probe, pending three audit gates. Even if audit passes, result applies to A_* specifically.

**What would need to happen:** extend the R1-KE theorem framework to varieties with other endomorphism rings; handle CM-type varieties separately (already covered by Deligne 1982 / Moonen-Zarhin / André-Milne for CM Hodge).

**Status:** OPEN. S33 v2 is step 1 of many.

### 3.6 2/7 structural mechanism ↔ QCD physics (if ever revisited)

**What it would be:** Identify which physical system, if any, realizes the "zero-gap in coherence system with dual thresholds ≥ 1/2" pattern.

**What's been tried:** The identification with Yang-Mills √σ/m(0++) was falsified at 16.5σ (§15 caution #10).

**What would need to happen:** a different physical realization that isn't YM lattice QCD. Or the acknowledgment that the 2/7 structural mechanism is abstract-algebra only and has no physics instantiation.

**Status:** falsification-preserved. The physical identity does not survive. The abstract-algebra mechanism does. These should not be conflated.

---

## §4. How to use this ledger

**When reading the master atlas:**

1. Any claim of structural parallel between two domains → check this ledger.
2. If it's in §1 (Strong overlap) → can be used as structural evidence.
3. If it's in §2 (Suggestive) → can be discussed but not used as evidence.
4. If it's in §3 (Not yet bridged) → should be named as an open research question, not as existing.

**When writing new atlas content:**

1. Any new parallel claim needs to fall in one of the three buckets.
2. A claim that doesn't fit any bucket needs to be flagged as a new entry here, OR discarded as unjustified.
3. Upgrading a claim from §3 → §2 or §2 → §1 requires explicit justification — a new computation, a new theorem, a new construction. Not a rhetorical argument.

**For external reviewers (ChatGPT, IHÉS, Clay):**

1. This ledger is the atlas's internal ranking of its own cross-thread claims.
2. You should feel free to challenge any entry: "this belongs in §3, not §1."
3. The purpose of the ledger is to make the atlas's synthesis honesty checkable.

---

## §5. Meta-pattern

Looking across §1, §2, §3, one meta-pattern appears:

> **The strongest overlaps are between finite grammars (Z/10Z, B-series, Rotation Spine shell structures). The suggestive overlaps are between threshold restatements (Li, Halving, bridge width). The not-yet-bridged problems are all about embedding Z/10Z-derived structure into classical analytic infrastructure.**

**Implication:** the atlas's strongest work so far is at the **finite-grammar level.** The bridge from finite-grammar to continuous-analytic is where most open problems live. This is the structural-geography of the program as a whole.

---

## §6. Maintenance

This ledger should be updated whenever:

- A new sprint establishes a new parallel claim
- An existing parallel is promoted (§3 → §2 or §2 → §1) via explicit work
- An existing parallel is demoted (§1 → §2 or §2 → §3) via discovered weakness
- An external reviewer challenges an entry

Version this document alongside the master atlas. Every atlas version should have a corresponding overlap ledger snapshot.

---

*© 2026 Brayden Ross Sanders / 7Site LLC. 7Site Human Use License v1.0. DOI: 10.5281/zenodo.18852047.*

**End of overlap ledger.**
