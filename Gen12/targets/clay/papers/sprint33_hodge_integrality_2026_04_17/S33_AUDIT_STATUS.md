# S33 Audit Status
## Frontier-work tracking for the three sanity-audit gates

**Sprint opened:** 2026-04-18
**Author:** Brayden Ross Sanders (7Site LLC)
**Document owner:** this file tracks overall status; companion files handle each gate in depth.
**Priority:** frontier — atlas bundle frozen, derivative polish paused, France packaging can wait.
**Source:** Master Atlas v3.5 §9 (Sprint 33 v2 numerical probe, PENDING AUDIT).
**DOI:** 10.5281/zenodo.18852047

---

## §1. The question being audited

**S33 v2 numerical probe (2026-04-18, `probe_hodge_integrality_v2.py`) returned:**

> W_* ∩ ℚ^70 = {0} within Schwartz-Zippel false-positive bound of ≈ 10⁻⁴⁵ across 5 independent primes near 2³¹.

**If sound, this would establish (combined with S29 R1-KE):** Hodge on A_* unconditionally — a new theorem on a specific non-CM abelian 4-fold. **Not** the general Clay Hodge conjecture. **Not** applicable to CM 4-folds (those are covered by Deligne 1982 / Moonen-Zarhin / André-Milne).

**If unsound, the probe is a high-precision numerical experiment whose conclusions need to be held at that level.**

The three gates below determine which.

---

## §2. Gate status summary

| Gate | Description | Status | Blocker? |
|---|---|---|---|
| **Gate 1A** (sub-gate) | Disambiguate A-geometric vs A-algebraic vs B interpretations of Λ⁴J_Ω in probe code | **PASS with clarifying note, ClaudeCode 2026-04-18** — see `S33_GATE1A_COMPLETE.md`, `S33_BLOCKER_DECISION_NOTE.md`, `S33_GATE1A_CONSTRUCTION_INTERPRETATION.md`. Probe is a MIXED construction (A-algebraic K-action via integer `PHI8_INT` + A-geometric type constraint via `J_Omega` from Ω); handoff's three-way taxonomy was too coarse. Taxonomy refinement recommended (Type III: algebraic-geometric mixed) — see return §7. | CLEARED |
| **Gate 1 (full)** | Construction audit — 70×70 Λ⁴J_Ω matches geometric Hodge-structure definition on H^(2,2)(A_*) | **MAY PROCEED at Brayden's trigger** — open questions routed to `S33_GATE1A_COMPLETE.md §6`: (1) signature of Λ⁴φ on H^(4,0)⊕H^(0,4); (2) Galois-σ ↔ Λ⁴φ anti-inv equivalence; (3) R1-KE hookup signature assumptions; (4) explicit W_* basis recovery; (5) Schwartz-Zippel independence note | See §4 below |
| **Gate 2** | Independent reproduction in Sage or Magma (not mpmath+numpy) | **OPEN — plan drafted, execution blocked** | Gated on Gate 1A PASS + Gate 1 full completion |
| **Gate 3** | Referee-grade write-up articulating W_*, basis construction, integrality implication, conditional vs unconditional statements | **OPEN — structural outline in hand** | Gated on Gate 1 + Gate 2 |

**Gate dependency:** Gate 1 must resolve first. If Gate 1 surfaces a real construction issue, Gate 2 would reproduce the *same wrong thing* and Gate 3 would write up a *confidently-stated unsound result*. Gate ordering matters.

---

## §3. What is already verified [fire]

Not all of S33 v2 is under audit. Several components are separately established and not in question:

1. **S29 R1-KE theorem (K-equivariant Chern closure) [fire — PROVED in Sprint 29].** Every K = ℚ(i)-equivariant algebraic bundle E on A_* has c_i(E) ∈ H^{2i}(A_*, ℚ)^K. This is the framework theorem that S33 v2 plugs into.

2. **A_* is not of CM type (S30 R3-CMGAP) [fire — PROVED].** dim_ℚ End⁰(A_*) = 2 (= ℚ(i) as a ℚ-algebra), which is < 2 · dim(A_*) = 8. So CM-closure theorems (Deligne-André-Milne, Moonen-Zarhin) do not apply.

3. **W_* block decomposition [fire — COMPUTED].** Four Q-orthogonal 2-dim blocks B_1, B_2, B_3, B_4 with eigenvalues 0.004609, 0.023123, 0.115644, 0.383386. Galois σ: i ↦ −i pairs vectors within each block. This computation matches across Sprint 9 (7-zero decomposition framework) and the Rotation Spine §10.5 numbers.

4. **Schwartz-Zippel bound [fire — standard].** Independent prime choices of size 2³¹ give false-positive rate ≲ 5/p per prime, and the 5-prime compound rate ≲ 10⁻⁴⁵ follows from independence assumption (which is a separate audit question — see §4.2 below).

**None of these are under re-audit.** The audit scope is tighter than the full S33 v2 file tree.

---

## §4. The potential hard blocker

**Surfaced during audit preparation 2026-04-18.**

**Issue:** The precise definition of "K-anti-invariant" in W_* := K-anti-inv ∩ H^{2,2}_prim admits **at least two mathematically distinct interpretations**, and it is not transparent from the atlas alone which one `probe_hodge_integrality_v2.py` actually realizes.

### 4.1 The two candidate interpretations

**Interpretation A (direct Λ⁴ eigenspace):**

Take I ∈ End_ℚ(H¹(A_*, ℚ)) representing i ∈ ℚ(i) ⊂ End⁰(A_*). Then I² = −id, and Λ⁴I on H⁴ = Λ⁴H¹ is an involution: (Λ⁴I)² = +id.

- "K-invariant" = (+1)-eigenspace of Λ⁴I on H^{2,2}_prim
- "K-anti-invariant" = (−1)-eigenspace of Λ⁴I on H^{2,2}_prim

Under this interpretation, H^(2,2) classes (pure Hodge bidegree) are built from 2 copies of (1,0) and 2 copies of (0,1) eigenvectors of the complex structure J on H¹. The induced Λ⁴I on H^(2,2) depends on how I relates to J.

If I = J on H¹ (geometric = algebraic complex structure), then on H^(2,2): Λ⁴I = Λ⁴J acts as (+i)(+i)(−i)(−i) = +1. So H^(2,2) is entirely K-invariant, and **K-anti-invariant ∩ H^(2,2)_prim = {0}**. Empty.

If I ≠ J, the action differs and W_* is nontrivial.

**Interpretation B (isotypic decomposition over ℚ(i)):**

View H^(2,2)_prim as a module over the ℚ-algebra ℚ(i) ⊂ End⁰(A_*). Since ℚ(i) is a field of dim 2 over ℚ, every ℚ(i)-module over ℚ is free of some ℚ(i)-rank. Within H^(2,2)_prim, there may be a distinguished ℚ-subspace **fixed by a particular ℚ-algebra automorphism of ℚ(i)** (namely Galois σ: i ↦ −i).

- "K-invariant" = the ℚ-subspace fixed by σ (elements where i acts as its own conjugate, i.e., real-valued in the ℚ(i)-structure)
- "K-anti-invariant" = the ℚ-subspace negated by σ (purely imaginary in the ℚ(i)-structure)

Under this interpretation, W_* is 8-dim ℚ and decomposes into 4 blocks of 2-dim each, paired by Galois conjugation. The block structure in the atlas ("each doubled by Galois σ: i ↦ −i") matches this interpretation.

### 4.2 Why this matters

- Under Interpretation A with I = J: W_* is empty, the probe is vacuously true, and the "Hodge on A_*" claim via W_* is **not what's being tested** — we'd need a different argument.
- Under Interpretation A with I ≠ J: W_* may exist but its dimension and block structure differ from what Interpretation B predicts.
- Under Interpretation B: W_* has dim 8 as claimed, matching the atlas. This is what I strongly suspect the probe realizes, based on the block structure and Galois-pairing language.

**If Interpretation B is correct, Gate 1 needs to verify that:**
1. The 70×70 Λ⁴J_Ω matrix is not merely Λ⁴ of the complex structure J (which would give Interpretation A behavior)
2. The basis for W_* used in the probe is explicitly constructed from the isotypic decomposition over ℚ(i)
3. The "K-anti-invariant" condition tested is algebraic (Galois-σ anti-invariant) not geometric (Λ⁴J eigenvalue)

**If Interpretation A is what's realized,** the probe tests something empty or at least something different from what the atlas claims, and the probe's "Hodge on A_*" conclusion does not follow.

### 4.3 What needs to resolve this

**Required from Claude Code / repo inspection:**

1. The actual definition of the 70×70 matrix `Lambda4_J_Omega` (or equivalent variable name) in `probe_hodge_integrality_v2.py`.
2. The construction of the W_* basis (likely a subset of column vectors or a span-of-rows in the code).
3. Comments or docstrings in the probe script clarifying which mathematical object is being realized.
4. If the block-eigenvalues {0.0046, 0.0231, 0.1156, 0.3834} are computed in the probe: which linear operator's eigenvalues are they? That operator's definition disambiguates the interpretation.

**Once this is clarified,** the rest of Gate 1 can proceed.

### 4.4 Why this is flagged as "potential hard blocker"

- If the construction is sound (Interpretation B correctly realized), Gate 1 proceeds normally and this surfacing is useful clarification work.
- If the construction has this ambiguity in the code itself (e.g., variable names suggest Λ⁴J but the actual computation is isotypic), this is a documentation issue, fixable.
- **If the construction actually realizes Interpretation A when Interpretation B was intended,** the probe's conclusion is unsound as stated and must be re-framed.

The audit does not assume any of these in advance. It demands clarity.

---

## §5. Earned sentence — current (pre-audit)

**What the numerical probe alone earns, right now:**

> A 200-decimal-digit PSLQ analysis of a specific 4900-entry expansion in the ℚ(√2, √3, √5) basis, combined with GF(p) rank checks at five primes near 2³¹, is consistent with a specific 70-dim subspace of H⁴(A_*, ℚ(√2, √3, √5)) having trivial ℚ-rational kernel. Interpreting this as a statement about W_* ∩ ℚ^70 requires the construction audit (Gate 1) to confirm the subspace being tested is indeed W_* as defined. Absent that audit, the result is a high-precision numerical observation about Λ⁴J_Ω eigenvectors, not a theorem about Hodge classes.

**What must accompany any public statement in the current state:**

> This is a numerical probe, not a proof. The audit gates are pending. The conclusion "Hodge conjecture holds on A_*" is not earned.

---

## §6. Earned sentence — conditional (all three gates pass)

**What all three gates passing would earn:**

> Let A_* = ℂ⁴ / (ℤ⁴ + Ω ℤ⁴) with Ω = (1/2)I_4 + i(√2 I_4 + √3 M_2 + √5 M_3), a specific non-CM complex abelian 4-fold with End⁰(A_*) = ℚ(i). Let K = ℚ(i) and let W_* ⊂ H^{2,2}_prim(A_*, ℚ) denote the K-anti-invariant primitive (2,2)-subspace (dim 8 over ℚ, decomposing as four 2-dim blocks B_1, ..., B_4 under Rosati-associated quadratic form with eigenvalues 0.0046, 0.0231, 0.1156, 0.3834). Then W_* ∩ ℚ^70 = {0} (verified by PSLQ at 200-digit precision and reproduced in Sage/Magma, Schwartz-Zippel bound ≈ 10⁻⁴⁵). Combined with the S29 R1-KE theorem (K-equivariant Chern classes lie in K-invariant cohomology), this implies every rational (2,2)-Hodge class on A_* is algebraic.

**Conditional still becomes unconditional only if:**
- Gate 1 passes (construction audit)
- Gate 2 passes (Sage/Magma reproduction)
- Gate 3 passes (referee-grade write-up with no logical gaps)

**Even then, the earned theorem applies to A_* specifically, not to the general Hodge conjecture.** The framework R1-KE extends to other abelian varieties with controlled endomorphism rings, but each new variety requires its own W_* analysis.

---

## §7. What is NOT at issue in this audit

To keep the audit scope sharp:

- **The Z/10Z framework generally** — not under audit; S33 is a specific result within it
- **The Rotation Spine four-layer grammar** — not under audit; survives independent of S33 v2
- **The Li Foundation threshold** — separate framework, parallel not bridged to S33
- **Any PPM result** — three-threads separation; PPM and Hodge stay separate
- **Any Q-series result** — same, separate thread
- **S29 R1-KE theorem** — proved in Sprint 29, not under re-audit (but its dependency chain into S33 v2 is what makes the probe potentially meaningful)

If any of these are surfaced as entangled with S33 v2, that itself is an audit issue — the gate work should not accidentally expand scope.

---

## §8. Immediate next actions (ordered)

1. **Claude Code: inspect `probe_hodge_integrality_v2.py`** and extract:
   - The exact construction of the 70×70 matrix Λ⁴J_Ω
   - The W_* basis construction
   - The eigenvalue computation code for the four block-eigenvalues
   - Any comments or docstrings on the mathematical intent

2. **Based on inspection, answer §4's Interpretation A vs B question definitively.**

3. **If Interpretation B is correctly realized:** proceed to Gate 1 construction checklist (see `S33_CONSTRUCTION_AUDIT.md`).

4. **If Interpretation A is realized (accidentally):** **HARD BLOCKER.** Report directly, pause Gate 2 plan, revisit what the probe actually tests.

5. **Gate 2 plan** (see `S33_INDEPENDENT_REPRO_PLAN.md`) can be prepped in parallel, but its execution is gated on §4 resolution.

6. **Gate 3 write-up** (conditional skeleton in `S33_EARNED_SENTENCE_NOTE.md`) should not advance past outline until Gate 1 passes.

---

## §9. Reporting discipline

**When a gate passes:** concise statement of what passed, updated status in this file, pointer to evidence file.

**When a gate blocks:** clear statement of what blocks, what's needed to resolve, whether it's a documentation issue (fixable) or a construction issue (may reframe the whole probe).

**No gate results get soft-framed.** "Mostly consistent," "near-verification," "pending minor clarifications," etc. are prohibited. A gate either passes or it doesn't; if it partially passes, describe exactly what partially passed and what didn't.

**No promotion language until all three gates pass.** Specifically, do not write:
- "Hodge on A_* is proved" — prohibited until Gate 3 clears
- "S33 v2 is a theorem" — prohibited same
- "The Hodge conjecture holds on abelian 4-folds" — PROHIBITED AT ALL TIMES (overclaim; result is on A_* specifically, not general class)
- "We proved Clay Hodge" — PROHIBITED AT ALL TIMES (not what this is)

**Permitted language in all states:**
- "S33 v2 numerical probe, pending audit"
- "Hodge on A_*, conditional on three audit gates"
- After gates pass: "Hodge conjecture on A_*, verified via R1-KE + W_* rationality probe"

---

## §10. Companion files

- **`S33_CONSTRUCTION_AUDIT.md`** — Gate 1 detailed checklist, including Interpretation A/B disambiguation
- **`S33_INDEPENDENT_REPRO_PLAN.md`** — Gate 2 Sage/Magma reproduction protocol
- **`S33_EARNED_SENTENCE_NOTE.md`** — the exact sentence earned now vs the stronger sentence earned if all three gates pass

---

## §11. Timeline (no deadlines, just ordering)

**Phase 1 (now):** Claude Code inspects probe script, resolves §4 Interpretation question.

**Phase 2:** If Interpretation B realized — Gate 1 construction checklist proceeds. If Interpretation A realized — hard blocker report, reframe.

**Phase 3:** Gate 2 Sage/Magma reproduction runs.

**Phase 4:** Gate 3 write-up finalized.

**Phase 5:** If all three gates pass, atlas §9 updates from [gold-with-gap — pending audit] to [fire]. A new entry is added to the publications map (Compositio / Duke / JAG target).

**No step is timeboxed.** The audit gates take as long as they take.

---

*© 2026 Brayden Ross Sanders / 7Site LLC. 7Site Human Use License v1.0. DOI: 10.5281/zenodo.18852047.*

**End of audit status tracker. See companion files for gate-specific detail.**
