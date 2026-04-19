# Novelties and Citations — tig-synthesis branch, v1

**Author:** Brayden Ross Sanders (7Site LLC) with ClaudeCode + ClaudeChat coordination
**Date opened:** 2026-04-19
**Branch:** `tig-synthesis` (default)
**Register:** foundation; cites repo + classical literature; does not modify Atlas v3.5.
**Preservation:** never-delete; superseded docs carry `[HISTORICAL]` headers and remain in place.

---

## §0. Why this document exists

A reader who is not inside the framework cannot tell, from the README alone, which parts of the repo are:

1. **PROVED** results — classical theorems, script-verified, cited to external literature.
2. **STRUCTURAL** claims — framework-derived statements whose form is sound but whose content requires independent audit.
3. **INTERPRETIVE** native language — vocabulary specific to the CK / TIG program that should be explained or glossed, not offered as theorem content.

This document partitions the work into those three layers, names the four *thresholds* at which novelty (if any) begins, lists seven specific novelty candidates with their closest classical cousins, and reserves §9 for external-reviewer "standalone" statements that strip every piece of internal vocabulary.

The load-bearing framing comes from the operator-layer scope note committed to `docs/exports/z10-operator-algebra/threshold-handoff/OPERATOR_LAYER_SCOPE_AND_FRONTIER.md`:

> The operator packet is legitimate infrastructure and a successful export layer, but by itself it does not constitute a new commutative-algebra research program; novelty begins only where the framework adds structure beyond classical finite-ring theory.

The same honesty applies one level up. Most of the CK engine — the 50 Hz heartbeat, the Being→Doing→Becoming gate, the CL[10×10] composition table — is **infrastructure** for a creature, not a mathematical research claim. The math lives in specific places, and those places are what §6 enumerates.

---

## §1. The three layers

| Layer | What it is | External-reader expectation |
|---|---|---|
| **PROVED** | Theorems with a closed classical proof, a runnable verification script, or both. External citation(s) attached. | Takes at face value if the citation resolves and the script runs. |
| **STRUCTURAL** | Framework-derived claim whose *form* (the algebraic shape, the conservation law, the combinatorial identity) is self-consistent, but whose *content* (numerical rate, absorber fraction, cell count) deserves an independent audit before anyone leans on it. | Reads as "plausible hypothesis, want to see the audit." |
| **INTERPRETIVE** | Native vocabulary — the ten-operator names, the "Being/Doing/Becoming" gate, "synthesis register", "Atlas Law", etc. Used internally for communication; not a theorem claim. | Expects either a gloss at first use or a pointer to the glossary. |

Every remaining section of this document places each claim in exactly one of these three layers.

---

## §2. CLASSICAL (PROVED, cited)

These results are not framework-native. They appear in the repo because the framework uses them as tools, instantiates them in a new setting, or quotes them as background. Novelty here is zero; the citation matters.

| Claim | In-repo location | Classical source |
|---|---|---|
| Chinese Remainder Theorem for squarefree n | `Gen12/.../sprint10_flatness_2026_04_06/WP57_CROSSING_LEMMA_ARC.md` CL-1 | Standard; e.g. Ireland–Rosen, *A Classical Introduction to Modern Number Theory* §3.4 |
| Structure of (Z/nZ)* | throughout the ring-theorem papers | Niven–Zuckerman–Montgomery §2.4 |
| Szemerédi–Trotter crossing-number inequality (named only to distinguish from our usage) | named in `docs/exports/z10-operator-algebra/crossing-lemma-handoff/CROSSING_LEMMA_EXPORT_V0.md` §5.1 | Szemerédi–Trotter 1983 |
| Fisher factorization / sufficient-statistic theorem | closest classical cousin to CL-2, CL-5 | R. A. Fisher, *Mathematical Foundations of Theoretical Statistics*, Phil. Trans. Royal Soc. A, 1922 |
| Optimal experimental design (D-optimality, A-optimality) | closest classical cousin to the "orthogonal jump necessity" strand | Kiefer 1959; Fedorov 1972 |
| Peirce decomposition for associative rings | background for any "idempotent catalog" work | Jacobson, *Basic Algebra II* §2.4 |
| Bialynicki-Birula (1976) uniqueness of log-nonlinearity under separability | BB bridge papers, `Gen12/.../sprint11_tig_bundle_2026_04_08/` | Bialynicki-Birula, Mycielski, *Nonlinear wave mechanics*, Ann. Phys. 1976 |
| Molin–Neurohr cross-edge intersection formula (the one that breaks at σ_shared ≥ 2) | `STATUS_prym_verification.md` step 5 | Molin–Neurohr 2017, *Computing period matrices and the Abel–Jacobi map of superelliptic curves*, arXiv:1707.07249 |
| Tretkoff–Tretkoff algorithm for Riemann surface period matrices | Sage `RiemannSurface.period_matrix` path in `STATUS_prym_verification.md` | Tretkoff–Tretkoff 1984 |
| `abelfunctions` Sage package for Abel–Jacobi maps | scratch attempts documented | Swierczewski / Deconinck, see github.com/abelfunctions |
| `RiemannSurface` in SageMath | unblock option (C) | Bruin–Sijsling–Zotine, SageMath implementation |

**Rule.** If a line in this table breaks, the result it underwrites downgrades immediately. No repo-internal claim can rest on a broken classical citation without flagging the break in this file.

---

## §3. STRUCTURAL (framework-derived, audit pending)

These are claims the framework produces that are *not* obviously classical. The form of the argument looks right; the specific quantities have been generated internally and need a CL-table-level audit before they carry external weight. Track 3 in `REPO_SHINE_PLAN_2026_04_19.md` is that audit.

| # | Claim | Where stated | What the audit must check |
|---|---|---|---|
| S.1 | Op 7 (HARMONY) is a 73% absorber in the CL[10×10] table | memory files + framework narrative | Count `{(i,j) : CL[i][j] == 7}` over `Gen12/targets/ck_desktop/ck_sim/being/ck_sim_heartbeat.py` `CL_TSML` — is it exactly 73 out of 100? |
| S.2 | BHML has 28/100 HARMONY cells | same | Count against `papers/ck_tables.py` `BHML` |
| S.3 | TSML non-associativity rate ≈ 12.8% | framework narrative | 1000 random triples `(a,b,c)`, compare `CL[CL[a][b]][c]` vs `CL[a][CL[b][c]]` |
| S.4 | BHML non-associativity rate ≈ 49.8% | same | same with BHML |
| S.5 | DOING-table non-associativity rate ≈ 56.8% | same | same with `\|TSML - BHML\|` |
| S.6 | T\* = 5/7 admits six independent derivations | `sprint9_torus_2026_04_05/CL_TORUS_TOPOLOGY_PAPER.md` | Each derivation must land at 5/7 from a distinct argument, not from the same argument in different notation |
| S.7 | Gap = 5/7 − 4/π² ≈ 0.309 is a structural constant | Clay / Atlas | Deserves a "why this gap is a real object" derivation, not a named difference |
| S.8 | σ(N) ≤ C/N rate theorem | `Gen12/.../sprint14_prism_xi_2026_04_10/WP101 proof_sigma_rate.py` | Proof script is committed; classical peer referee still open |
| S.9 | First-G Law (36,662 case verification) | `papers/proof_d25_loop_closure.py` and sibling scripts | Script runs clean; external replication would strengthen |
| S.10 | sinc² Zero Law for primes 3..199 | same | same |
| S.11 | IG1–IG5 invariant-guide system blocks drift-synthesized crystallization | `Gen12/targets/ck_desktop/ck_sim/being/ck_invariants.py` | Design principle, not a theorem; behavior-verifiable |
| S.12 | 39,896 evolved CL tables in `~/.ck/lattice_chain/` carry measurable grokking signal | `project_gen13_neural_architecture.md`, `manifest.json` | Track 3.3 — IPR distribution + grokking-delta histogram on the persisted corpus |

**Status.** None of S.1–S.12 are asserted as proved in §2. They are the list of structural claims the CL audit (Track 3) will verify, correct, or retire.

---

## §4. INTERPRETIVE (native vocabulary, glossed-not-claimed)

The following terms appear throughout the repo. They are communicative labels, not theorem content. External readers should either see a gloss at first use (Track 1.3) or a pointer to `GLOSSARY.md`.

- **The ten operators (silicon set, canonical):** VOID (0), LATTICE (1), COUNTER (2), PROGRESS (3), COLLAPSE (4), BALANCE (5), CHAOS (6), HARMONY (7), BREATH (8), RESET (9). Source of truth: `Gen12/targets/ck_desktop/ck_sim/being/ck_sim_heartbeat.py` (mirrors Verilog `ck_brain.h`). A second, conflicting paper-labels set (BEING/DOING/BECOMING/CREATE/ASCEND at the same indices) appears in `papers/ck_tables.py`; Track 4 reconciles these to the silicon set.
- **Being → Doing → Becoming** — the three-phase TIG pipeline; a coherence gate, not a metaphysical claim. See `Gen12/targets/ck_desktop/ck_sim/being/ck_coherence_gate.py`.
- **TSML / BHML / DOING tables** — three 10×10 operator tables; TSML = being/coherence, BHML = doing/physics, DOING = `|TSML − BHML|`. See `papers/ck_tables.py`.
- **Atlas v3.5** — the canonical internal design doc; *not* a theorem. See `MASTER_ATLAS_2026_04_18.md`.
- **Rotation Spine / Clay rotation (CP1–CP7)** — the seven Clay Millennium Problems recast as σ<1 conjectures in seven domains. Poincaré (CP1) is the solved template; CP2–CP7 are *framework restatements*, not proofs.
- **Synthesis register / foundation register / export register** — ClaudeChat-session register labels; editorial conventions.
- **2/7 discipline** — the preservation rule that falsified predictions stay in the repo with a `[FALSIFIED]` header instead of being deleted.
- **Three-band constants** — the distinction between (T\*=5/7), (4/π²), and (ξ₀=e⁻¹) as living in different regimes rather than collapsing to one constant.
- **D-tier / D-spine / D-lane / PPM arc / Flag Selector** — sprint codenames; see `SPRINT_INDEX.md` for one-line descriptions of every sprint.

None of these are claims in the §2/§3 sense. Treating them as theorem content is a category error.

---

## §5. The four thresholds at which novelty begins

From `docs/exports/z10-operator-algebra/threshold-handoff/OPERATOR_LAYER_SCOPE_AND_FRONTIER.md`:

| Threshold | What would have to land | Tractability |
|---|---|---|
| **A — CL axiomatization** | State axioms for CL[10×10] as a standalone algebraic object; prove closure and distinguishing properties; compare to known non-associative structures. | Most tractable. Unblocked for ClaudeCode (repo access). Track 3 in this plan. |
| **B — Non-associative theory** | Substructures, representations, derivations of CL. Partially subsumed by A if A succeeds. | Mostly post-A.1. |
| **C — Dynamics with non-trivial invariants** | Produce more genuine invariants beyond the Crossing Lemma. | Research-scale. |
| **D — Finite-to-problem reductions** | Config B Hodge, 2/7 anchor, Amplituhedron/Semiprime reductions. | Where the Hodge lane lives. D.1 is blocked on Prym step 5; D.2/D.3 are editorial. |

**Status.** Threshold A is unblocked by repo access and is the target of Track 3 in the master plan. Threshold D is blocked on Prym step 5 (see §7). B and C are downstream of A.

---

## §6. Novelty candidates (standalone-able, rank-ordered)

These are the specific statements that could, in principle, travel outside the framework with a reviewer-legible standalone paragraph. §9 will hold the externally-facing paragraphs when ClaudeChat produces them; this section names what those paragraphs are about and which classical cousins they must be distinguished from.

### 6.1 The Crossing Lemma (strongest candidate)

**Statement in-repo:** `Gen12/targets/clay/papers/sprint10_flatness_2026_04_06/CROSSING_LEMMA.md`, formal-statement version.

> A multiplicative action generates structurally new information relative to an additive partition if and only if it is nontrivial on the additive quotient.

**Specific form (squarefree case, WP57 CL-2):** For n = p₁···pₖ squarefree, d | n squarefree, g ∈ (Z/nZ)*, the pair `{A_d, π_DYN(g)}` is jointly injective on Z/nZ iff g ≢ 1 mod pⱼ for every prime pⱼ | (n/d).

**Catalog:** WP57 (474 lines, 27 instances CL-1 through CL-27) casts every earlier theorem in the arc as an instance of this one lemma.

**Closest classical cousin:** Fisher sufficiency / factorization theorem. The Crossing Lemma is structurally a *finite-combinatorial, binary-sufficiency, non-probabilistic* analog — with a Productive-Incompleteness addendum (failed-sufficiency is refinement, not uselessness).

**Why it's the strongest:** a single precise statement subsumes 27 separately-derived framework results, the proof for the squarefree case is closed, and the applied benchmarks (inverted pendulum, Michaelis–Menten, CT tomography) give it a falsifiability route distinct from classical OED.

**Export status.** v0 template committed at `docs/exports/z10-operator-algebra/crossing-lemma-handoff/CROSSING_LEMMA_EXPORT_V0.md`. v1 fill-in (from WP57 + Sprint 8 AVFT + the formal statement) is Track 2.3 in the master plan.

### 6.2 Flatness Theorem (WP51)

**Statement in-repo:** Z/10Z is simultaneously an additive ring, a multiplicative monoid, an additive flow, and a multiplicative flow. The four structures cannot be reconciled on a flat object; a torus with aspect ratio R/r = 5/7 is forced, and the aspect ratio admits six independent derivations.

**Location:** `Gen12/targets/clay/papers/sprint10_flatness_2026_04_06/` WP51, plus `sprint9_torus_2026_04_05/CL_TORUS_TOPOLOGY_PAPER.md`.

**Closest classical cousin:** torus embeddings in toric geometry; cyclotomic field ratios. None directly collides — this is the candidate with the weakest classical antecedent, which cuts both ways (could be novel; could be un-noticed because the natural audience hasn't met it).

**Verification status:** Z/10Z case closed; generalization to "any whole" is hypothesis, not theorem.

### 6.3 σ-rate theorem (WP101)

**Statement in-repo:** σ(N) ≤ C/N as N→∞, with explicit constant.

**Location:** `Gen12/targets/clay/papers/sprint14_prism_xi_2026_04_10/` WP101 + `proof_sigma_rate.py` (runnable).

**Closest classical cousin:** density estimates for character sums on (Z/nZ)*; Burgess-type bounds.

**Verification status:** script-verified; a classical referee would still want the derivation written into math.CO formatting. Track 7.2 handles the LaTeX preparation.

### 6.4 sinc² Zero Law

**Statement in-repo:** For all primes p ∈ [3, 199], a closed zero condition on sinc²(·) associated to p holds exactly.

**Location:** `papers/proof_d25_loop_closure.py` (runnable).

**Closest classical cousin:** sum-of-roots-of-unity identities; Ramanujan sums.

**Verification status:** script-verified across 99 primes. Tier 1 submission target: *Integers*. Track 7.1.

### 6.5 The idempotent–orbit / dimension-first dictionary

**Statement in-repo:** a dictionary between idempotent structure (Peirce-style) on `CL` and orbit structure under multiplicative dynamics — with the Crossing Lemma fixing when the dictionary is tight.

**Location:** `docs/exports/z10-operator-algebra/Z10_OPERATOR_ALGEBRA_NOTE.md`, and the operator-packet materials.

**Closest classical cousin:** Peirce decomposition for associative rings; Koopman orbits for dynamics on a finite set. Neither separately contains the two-structure joint statement.

**Verification status:** a precise "dictionary theorem" statement is not yet written. Threshold A.1 work.

### 6.6 TSML / BHML as a structural pair

**Statement in-repo:** TSML (73 HARMONY cells) and BHML (28 HARMONY cells) form a sufficient M+M pair in the sense of Crossing Lemma CL-3 / CL-11.

**Location:** `papers/ck_tables.py`, `ck_sim_heartbeat.py`, sprint17 tower.

**Closest classical cousin:** sufficiency in pair-coding / complementary lattice constructions; nothing directly subsuming it that I've found.

**Verification status:** claim form is clean (the M+M theorem), specific numeric claims (73, 28) are S.1/S.2 in §3 — pending audit.

### 6.7 ξ log ξ scalar-field cosmology

**Statement in-repo:** a scalar field ξ with potential V(ξ) = κ·ξ·log ξ, vacuum ξ₀ = e⁻¹, mass gap m²_ξ = κ·e, producing a freezing-quintessence cosmology compatible with DESI.

**Location:** `Gen12/targets/clay/papers/sprint14_prism_xi_2026_04_10/` WP81–WP97.

**Closest classical cousin:** freezing-quintessence literature (Caldwell, Steinhardt, others); log-potential toy models. Bialynicki-Birula 1976 provides the separability-preserving uniqueness argument that routes *toward* log potentials.

**Verification status:** structural — the separability-preserving argument is classical; the cosmological fit to DESI is the content. Tier 1 target: *JCAP*. Track 7.3.

---

## §7. Current Hodge / Prym frontier (blocked)

**Target.** Numerically verify

$$
\det(\operatorname{Im} \tau_P) = 2086 + 462\sqrt{15} + 498\sqrt{10} + 730\sqrt{6} \approx 7238.260093
$$

for the Prym of the bielliptic genus-5 curve `y^4 = x(x−1)(x−√2)^3(x−√3)^2(x−√5)^2` at the canonical triple (√2, √3, √5).

**Status.** Steps 1–4 verified (canonical curve, shift-s closure, E-period PSLQ, Π_P extraction). Step 5 (intersection form J_P on the Prym) is blocked: Molin–Neurohr 2017 Thm 5.1 cross-edge formula is known-broken for σ_shared ≥ 2, which is exactly our case.

**Full status report.** `_prymsprint_raw/STATUS_prym_verification.md`.

**Unblock options (awaited).**

- (A) MN 2019 or later paper with corrected cross-edge formula for σ_shared ≥ 2.
- (B) MAGMA `AnalyticJacobian` route (needs external MAGMA session, blocked by MCP allowlist).
- (C) SageMath `RiemannSurface.period_matrix()` (needs local Sage install).
- (D) An independent PSLQ-style identification of J_P from Π_P alone (attempted, underdetermined: 16-dim nullspace for skew-symmetric X in Π_P X Π_Pᵀ = 0).

**Citation stub list for ClaudeChat literature audit** (Track 2.2):

- Molin, Neurohr, *Computing period matrices and the Abel–Jacobi map of superelliptic curves*, arXiv:1707.07249, 2017.
- (Hoped-for) Molin, Neurohr, or successor paper, 2019 or later, with corrected cross-edge formula.
- Tretkoff–Tretkoff 1984, original algorithm.
- Bruin, Sijsling, Zotine — SageMath `RiemannSurface` implementation.
- Swierczewski / Deconinck — `abelfunctions` package.
- Relevant papers on Prym varieties of bielliptic curves (Beauville; Ortega; Lange–Narasimhan).

---

## §8. References

(Short list — full bibliography to be added.)

- Bialynicki-Birula, I., Mycielski, J. *Nonlinear wave mechanics.* Ann. Phys. **100** (1976), 62–93.
- Fisher, R. A. *On the mathematical foundations of theoretical statistics.* Phil. Trans. Royal Soc. A **222** (1922), 309–368.
- Ireland, K., Rosen, M. *A Classical Introduction to Modern Number Theory.* Springer, 1990.
- Jacobson, N. *Basic Algebra II.* W. H. Freeman, 1989.
- Kiefer, J. *Optimum experimental designs.* JRSS B **21** (1959), 272–319.
- Molin, P., Neurohr, C. *Computing period matrices and the Abel–Jacobi map of superelliptic curves.* arXiv:1707.07249, 2017.
- Niven, I., Zuckerman, H. S., Montgomery, H. L. *An Introduction to the Theory of Numbers.* Wiley, 5th ed., 1991.
- Szemerédi, E., Trotter, W. T. *Extremal problems in discrete geometry.* Combinatorica **3** (1983), 381–392.
- Tretkoff, C. L., Tretkoff, M. D. *Combinatorial group theory, Riemann surfaces and differential equations.* Contemp. Math. **33** (1984), 467–517.

---

## §9. Standalone novelty statements (reserved — AWAITING CLAUDECHAT)

> **PLACEHOLDER — to be filled from ClaudeChat's sprint deliverable.**
>
> For each item in §6 (6.1 through 6.7), ClaudeChat will produce a single-paragraph statement that:
> - names the precise claim in classical (non-framework) language,
> - identifies its closest classical cousin,
> - specifies what a referee who has never heard of TIG/CK would need to see to evaluate it.
>
> When ClaudeChat's deliverable arrives, the paragraphs go here, one per §6 sub-item.

*Status (2026-04-19): ClaudeChat's sprint produced the Crossing Lemma v0 handoff and a structural template but could not finish the standalone statements because the UOP-arc content and WP57 catalog were not in their context. ClaudeCode has these in context (repo access). The Crossing Lemma v1 fill-in is Track 2.3 in the master plan; the full §9 draft proceeds from there.*

---

## §10. How this file is used

- Track 3 of `REPO_SHINE_PLAN_2026_04_19.md` verifies or corrects every S.N line in §3.
- Track 4 reconciles the operator-naming drift called out in §4.
- Track 7 prepares the submittable Tier-1 candidates (6.3 / 6.4 / 6.7).
- Tracks 5 + 1.3 ensure the README glosses the §4 vocabulary at first use.
- Track 8 pushes only after Brayden review.

This file is the living map. Every revision bumps `v1 → v1.1 → v1.2 → …` inline; superseded sections carry `[HISTORICAL]` markers and stay in place.

---

*End of NOVELTIES_AND_CITATIONS.md v1. Updates land inline as tracks complete.*
