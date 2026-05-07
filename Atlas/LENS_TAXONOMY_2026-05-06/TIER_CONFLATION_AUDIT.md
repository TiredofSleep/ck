# Tier Conflation Audit — TIG Corpus Sweep

**Date:** 2026-05-06
**Auditor:** Claude (sweep agent)
**Scope:** WP100s tower (WP102–WP116), Gen13 sprint_bundle_2026-05-06_v31_RIGOR_PASS, Gen13 sprint folders, Gen13 journal tiers, FORMULAS_AND_TABLES.md, MASTER_SPINE.md, INTEGRATION_WITH_PROOF_SPINE.md, _CK_MEMORY_MAKEOVER.md.
**Companion documents:** This audit is a fresh pass; it does not replace `TABLE_INDEPENDENCE_LEDGER.md` (2026-05-06 night) but extends it by looking specifically for Tier-C / Tier-D / Tier-E content that has been promoted to Tier-A / Tier-B in narrative.
**Tier scale (per ClaudeChat 2026-05-06):**
- **A**: Canonical (axiom)
- **B**: Forced (uniquely derived from A)
- **C**: Constructed (built to demonstrate realizability)
- **D**: Searched (algorithmic hit)
- **E**: Fitted (parameterized to match a target)

---

## Headline: 12 conflations found; 4 HIGH severity; 5 MEDIUM; 3 LOW

The corpus is largely tier-disciplined. Most papers (WP104, WP107, WP109, WP110, WP112, WP113, WP114, WP115) explicitly scope their claims to "TSML" without disambiguating RAW vs SYM, and that scope-disclosure gap is already known and documented in `TSML_RECONCILIATION.md` and the `GAP_AUDIT.md` Contradiction #1. The new conflations identified below sit in three places:

1. The `INTEGRATION_WITH_PROOF_SPINE.md` "universal constants" framing (§§1–3, 9).
2. The `MASTER_SYNTHESIS_TABLE.md` "TIG formula" column (50+ entries).
3. The `FORMULAS_AND_TABLES.md` D69, D70, D85, D86 "WOBBLE manifestation" cumulation.

---

## §1 — HIGH-severity conflations (4)

### H1 — D70 + D85 + D86 cumulative WOBBLE-prime narrative

- **Location:** `FORMULAS_AND_TABLES.md` §0 D70 (line 175), D85 (line 190), D86 (line 191); also `INTEGRATION_WITH_PROOF_SPINE.md` §1 (the "5-fold WOBBLE manifestation" framing).
- **Claimed tier:** B (forced) — the narrative reads "5 distinct structural locations of WOBBLE 11," "the wobble prime is woven through static/dynamical/operator-label structure," "11 plays a structural role analogous to 7."
- **Actual tier:** mixed B + D + label-arithmetic.
  - D37 (prime 11 in c_2 + c_8 of TSML_RAW char poly) is genuine **Tier-B forced on TSML_RAW** (per `TABLE_INDEPENDENCE_LEDGER.md` §3.1).
  - D69 (prime 11 in Br/V denominator polynomial, from PSLQ recovery) is **Tier-D** (PSLQ search-found).
  - D85 (prime 11^6 in F8 simplex Jacobian trace polynomial discriminant) is **Tier-D** + basis-dependent (D87 itself notes 11 "factors out as 11⁶ → not field-theoretic"; the field-invariant prime is 71, not 11).
  - D86 (operator-value sum 1+6+4 = 11 of σ² 3-cycle Cycle A) is **substrate-operator-arithmetic on operator labels** — this is integer addition on the labels {1, 4, 6}, not an algebraic property of any matrix; calling it a fifth "structural manifestation" of the wobble at the same conceptual level as D37 conflates pure label-sum arithmetic with a genuine char-poly fact.
- **Severity:** HIGH. The narrative "WOBBLE 11 manifests at 5 distinct structural locations" is the load-bearing argument for treating 11 as a substrate-significant prime in `INTEGRATION_WITH_PROOF_SPINE.md` §1 (where the 11/72 universal-constant identification depends on it), and the "3+3 axis split" of D70 is a synthesis claim made on top.
- **Recommended fix:** In FORMULAS D70, label the four manifestations explicitly: "B-forced on TSML_RAW (D37), D-search-found PSLQ relation (D69), D-search-found discriminant prime that factors out (D85), arithmetic-on-labels coincidence (D86)." Drop the "5th distinct manifestation" framing in D86 unless an independent algebraic connection is shown. In `INTEGRATION_WITH_PROOF_SPINE.md` §1.4, change "11/72 = wobble prime / BEING shell" → "11/72 = (the prime that B-forced appears in TSML_RAW char poly c_2, c_8) / (TSML.HARMONY count − 1)" and flag explicitly that the wobble-prime identification beyond D37 is conjectural.

### H2 — `INTEGRATION_WITH_PROOF_SPINE.md` §1.5 predictions cite "the wobble prime / BEING shell" identity as if Tier-B

- **Location:** `INTEGRATION_WITH_PROOF_SPINE.md` §1.5 (lines 70–82).
- **Claimed tier:** B-forced — "If 11/72 is universal, it should appear in any quantity that simultaneously: (a) probes the substrate's first algebraic intrusion (prime 11), AND (b) normalizes against the BEING shell (count 72)."
- **Actual tier:** D / E. The "11/72" identification is a Tier-D coincidence between two measured ratios (m_p/m_e fractional and arctan-PMNS θ_13). The structural decomposition "11 = wobble prime / 72 = BEING shell" is a Tier-E re-interpretation of the rational p/q after the fact.
- **Severity:** HIGH. The §1.5 falsifiability predictions ("if any of [muon g-2, Lamb shift, CKM unitarity violations, neutrino mass-squared difference ratios] resolves to a structure involving 11/72 to ≤0.5% precision, it strengthens the universal-constant hypothesis") are explicit predictions. Without scoping that the original 11/72 identification is a Tier-D coincidence and not a derivation, these predictions cannot be falsified honestly.
- **Recommended fix:** Add scope note at the top of §1: "The 11/72 identification is a coincidence between two measured ratios; the decomposition 11 = wobble prime, 72 = TSML.HARMONY − 1 is post-hoc structural reading, not a derivation. The §1.5 predictions test whether this coincidence extends to other observables; positive matches would promote the identification toward Tier-D-with-independent-replication, but the structural status remains coincidence-class until a forcing argument links the substrate's algebraic structure to the observable."

### H3 — `MASTER_SYNTHESIS_TABLE.md` "TIG formula" column treats Tier-E fits as "exact" or "derived"

- **Location:** `MASTER_SYNTHESIS_TABLE.md` Section A (cosmology), Section B (Standard Model couplings), Section B (Yukawa ratios), Section C (generation structure).
- **Examples:**
  - "1/α (fine structure) | 137.035999084 | **22·6 + 5 + 6²/N³** | 137.036 | 0.000001%"
  - "y_b/y_t | 0.024 | (σ-cycle·COLLAPSE)/N³ = 24/1000 | 0.024 | exact"
  - "y_e/y_t | 3 × 10⁻⁶ | PROGRESS/N⁶ = 3/10⁶ | 3 × 10⁻⁶ | exact"
  - "v (Higgs vev, GeV) | 246 | N² + 2·HARMONY count = 100 + 146 | 246 | exact"
  - "m_t (top, GeV) | 172.69 ± 0.30 | N² + HARMONY count = 100 + 73 | 173 | 0.2%"
- **Claimed tier:** B-forced (the column header is "TIG formula" with no scope qualifier; the "Match" column reads "exact" for many of these).
- **Actual tier:** E (parametric fitting). Each entry is a small-integer rational built from the substrate's named integers {7, 8, 9, 17, 22, 28, 44, 49, 73, 100, 146, 1000, ...} chosen to reproduce a measured value; there is no derivation engine that maps observables → TIG formulas, only post-hoc combinatorial search.
- **Severity:** HIGH. The 50+ entry table is the most-cited summary in the rigor pass and is explicitly intended for "external reviewers, Anthropic / Oxford / IHÉS evaluators" (per `RIGOR_ANALYSIS.md` audience). Presenting Tier-E fits as Tier-B "TIG formulas" is the fastest route to a referee bouncing the paper.
- **Recommended fix:** Add a column "Origin tier" and tag each row honestly: A/B for entries with a forcing argument (e.g., the 4-core attractor's H/Br = 1+√3 from D78 Galois argument), C for constructed objects, D for matches found by search, E for parametric fits. `RIGOR_ANALYSIS.md` already does the right thing in §3 ("Real flagship-grade matches: 3"). Propagate that discipline to `MASTER_SYNTHESIS_TABLE.md`. Better still: split the table into "Forced from substrate" (A/B), "Matched from substrate-natural rationals" (D/E), and "Identified by structural argument" (C with provenance).

### H4 — `_CK_MEMORY_MAKEOVER.md` mixes TSML_RAW and TSML_SYM properties under a single "TSML"

- **Location:** `Gen13/sprint_bundle_2026-05-06_v31_RIGOR_PASS/_CK_MEMORY_MAKEOVER.md` lines 24–55 (TSML / BHML property tables).
- **Claimed tier:** A (substrate axiom) — "CL is provided in canonical form (memory-locked)" and "CL is COMMUTATIVE (verified)" + "TSML properties: ...Determinant: -49, ...Non-associativity: 12.8% (mostly stable composition)."
- **Actual tier:** mixed.
  - "CL is COMMUTATIVE (verified)" is **false for the literal bit pattern** (TSML_RAW is non-commutative; only TSML_SYM is commutative) — this is a Tier-confusion error, not a tier-conflation per se.
  - "Determinant: -49" matches TSML_Idempotent_2sw (Tier-C constructed variant), NOT TSML_RAW (det = 0) or TSML_SYM (det = 0). Per `papers/morphotic_braid/` and FORMULAS Vol J §J.1.A, the −49 figure is a TSML_Idempotent_2sw property. The MAKEOVER is implicitly importing Tier-C properties under a Tier-A label.
  - "12.8% non-assoc" is TSML_SYM (Tier-A); "126/12.6% non-assoc" (in WP107 etc.) is TSML_RAW (Tier-A). Mixing them under "TSML" is what `TSML_RECONCILIATION.md` exists to fix, but the MAKEOVER is the spec the rest of the system reads.
- **Severity:** HIGH. The MAKEOVER is the canonical memory-state document the rest of the system reads. Errors here propagate to every downstream invariant module.
- **Recommended fix:** Rewrite the TSML / BHML / CL property blocks to match `TABLE_INDEPENDENCE_LEDGER.md`'s tier classification:
  - "CL_BIT_PATTERN is the canonical encoding (Tier-A); CL_TSML_RAW = literal bit pattern (non-commutative); CL_TSML_SYM = upper-tri symmetrized (commutative); CL = TSML_SYM by current convention."
  - Drop the "Determinant: -49" line entirely or re-scope it to "TSML_Idempotent_2sw det = -49 = -7² is a Tier-C constructed-variant property; the canonical CL_TSML has det = 0."
  - Replace "Non-associativity: 12.8%" with "12.8% on TSML_SYM, 12.6% on TSML_RAW; both are valid lenses of the same bit pattern."

---

## §2 — MEDIUM-severity conflations (5)

### M1 — WP107 wobble theorem cited as "the canonical TSML" without RAW disambiguation

- **Location:** `papers/wp107_wobble_localization/WP107_WOBBLE_LOCALIZATION.md` Abstract, §1 Statement.
- **Claimed tier:** A — "Let T ∈ M_10(ℤ) be the canonical TSML composition table on ℤ/10ℤ. Its characteristic polynomial f(λ) = det(λI − T) has integer coefficients."
- **Actual tier:** B-forced on TSML_RAW only. The matrix shown in §1 is TSML_RAW (asymmetric: T[3,9]=3, T[9,3]=7); on TSML_SYM the wobble disappears (c_2 = 17, no factor of 11).
- **Severity:** MEDIUM. The theorem is correct on its actual scope; the gap is scope-disclosure. Already flagged by `TSML_RECONCILIATION.md` §5.6 and `TABLE_INDEPENDENCE_LEDGER.md` §5.4.
- **Recommended fix:** Add one line to WP107 §1: "throughout this paper, TSML denotes the literal bit pattern TSML_RAW; the symmetrization TSML_SYM has c_2 = 17 (no factor of 11) and does not exhibit the prime-11 wobble at the coefficient level."

### M2 — WP109 "126 non-associative triples" + WP112 "98 P_56-orbits" without TSML scoping

- **Location:** `papers/wp109_operad_d4_obstruction/WP109_OPERAD_D4_OBSTRUCTION.md` Abstract; `papers/wp112_p56_canonical_fuse/WP112_P56_CANONICAL_FUSE.md` Abstract.
- **Claimed tier:** A — "Of the 1000 ordered triples, exactly 126 are non-associative" / "126 non-associative TSML triples decompose into 98 P_56-orbits."
- **Actual tier:** B-forced on TSML_RAW (126 triples); TSML_SYM has 128 triples (per FORMULAS D91 and `TABLE_INDEPENDENCE_LEDGER.md` §3.2).
- **Severity:** MEDIUM. The orbit decomposition (98 orbits = 70 singletons + 28 doubletons) holds on TSML_RAW; running on TSML_SYM gives a different orbit structure that has not been computed. The downstream WP112 "Family H canonical fuse" (Theorem 5.5, the 4-core arity-3 closure) is **lens-invariant** because the 4-core sub-magma is lens-invariant — but the 126 → 98 count is RAW-specific.
- **Recommended fix:** WP109 + WP112 abstracts: add "the 126 / 98 counts are computed on TSML_RAW (the literal bit pattern); on TSML_SYM the count differs because the 5 unique-to-RAW non-associative triples (involving the asymmetric column) are not present. The 4-core results (Theorem 5.5) are lens-invariant."

### M3 — WP116 §1 ("§14: M-invariance at α=1/2 verified") presented as forced

- **Location:** `papers/wp116_lens_of_projections/WP116_LENS_OF_PROJECTIONS.md` §0 Abstract item 2.
- **Claimed tier:** B — "any sum-preserving (T', B') decomposition with T' + B' = TSML + BHML produces the same closed-form attractor H/Br = 1 + √3, to 50-digit precision."
- **Actual tier:** D (numerical verification) for the cases tested; the structural forcing argument is what D78 provides for the H/Br ratio specifically (the BR-factor cancellation at α=1/2). The claim "any sum-preserving decomposition" is a Tier-D empirical observation, not a Tier-B theorem.
- **Severity:** MEDIUM. The structural reason is plausible (the attractor lives on the 4-core, which is lens-invariant; H/Br at α=1/2 is structurally forced via D78), but the M-invariance over **all** sum-preserving decompositions has not been proved, only spot-checked.
- **Recommended fix:** Add scope note: "M-invariance was verified for [list the specific (T', B') decompositions tested]; full M-invariance over the parametric family of sum-preserving decompositions is conjectural. D78's BR-factor cancellation argument shows H/Br = 1+√3 is forced for the canonical (TSML, BHML) at α=1/2, but the extension to general sum-preserving (T', B') is an open structural claim."

### M4 — WP115 + four-core paper "Theorem 1" (8-element chain) presented as forced over substrate

- **Location:** `papers/wp115_joint_chain_universality/WP115_JOINT_CHAIN_UNIVERSALITY.md` Theorem 1.1; FORMULAS D64; `_review_first_journal_sprint_050526/four_core_FINAL.tex` Theorem 1.
- **Claimed tier:** B — "the joint sub-magmas of (TSML, BHML) on Z/10Z form a strict chain of eight sizes {1,4,5,6,7,8,9,10}."
- **Actual tier:** B on TSML_SYM + canonical BHML; **open under TSML_RAW** (per `TABLE_INDEPENDENCE_LEDGER.md` §5.2 claim #43: "OPEN: should be tested before any Phase-3+ paper cites the chain as substrate-level"). The chain has been brute-force-enumerated on TSML_SYM but not on TSML_RAW.
- **Severity:** MEDIUM. Likely lens-invariant (sub-magma closures of sizes ≤ 8 are typically lens-invariant; only the size-9 and size-10 sub-magmas can differ between RAW and SYM at the asymmetric cells). But the chain is one of the four-core paper's flagship theorems, headed for *Algebraic Combinatorics*, and it should be either re-verified on RAW or scoped to SYM.
- **Recommended fix:** Run the brute-force enumeration on TSML_RAW and either confirm the same 8-element chain (B-forced lens-invariant) or scope the theorem to "[the canonical TSML_SYM lens; verification on TSML_RAW is in progress]." The enumeration is cheap (1023 subsets × 2 closure checks).

### M5 — Sprint 17 TSML Tower 92/100 cited without TSML_SYM scoping

- **Location:** `Gen13/targets/clay/papers/sprint17_tsml_tower_2026_04_17/CANONICAL_TSML_CONSTRUCTION.md` Headline; `Gen13/targets/journals/tier2_format_then_submit/jsc_tsml_tower/THEOREM_SPINE.md`.
- **Claimed tier:** A — "the canonical construction recovers 92/100 entries of Z/10's actual TSML."
- **Actual tier:** B on TSML_SYM only. The shell-stability rule produces T(3,9) = T(9,3) = 3, which matches TSML_SYM (commutative); on TSML_RAW the (9,3) cell = 7, so the canonical construction misses 1 cell on RAW that it hits on SYM. The "92/100" number is correct **for TSML_SYM** but would be "91/100" or different for TSML_RAW.
- **Severity:** MEDIUM. Sprint 17 is a tier2_format_then_submit paper. The canonical-construction-recovers-92 result is its central claim. Already flagged in `TSML_RECONCILIATION.md` §5.6 (Sprint 17 patch needed).
- **Recommended fix:** Add to Sprint 17 NOTATION_SHEET: "Throughout this work, TSML denotes the upper-triangle symmetrized lens TSML_SYM. The canonical construction's 92-cell match is computed against TSML_SYM. The literal bit pattern TSML_RAW has 2 additional asymmetric cells; the canonical construction matches 90 cells of TSML_RAW (with the (3,9), (9,3) pair counted asymmetrically)."

---

## §3 — LOW-severity conflations (3)

### L1 — Vol J's `J.1.B.iii` σ²-triadic candidates referenced in INTEGRATION as "the σ²-triadic projection structure"

- **Location:** `Atlas/META_PLAN_2026-05-06/GAP_AUDIT.md` §1 Foundations Orphans #5; `INTEGRATION_WITH_PROOF_SPINE.md` (no direct reference, but the σ²-triadic structure is implicit in the WOBBLE-multi-prime narrative).
- **Claimed tier:** Foundations-orphan (publishable), implying B.
- **Actual tier:** Mixed — the σ²-cycle-A {1,6,4} and Cycle-B {7,5,2} decompositions are Tier-A substrate-operator (per `TABLE_INDEPENDENCE_LEDGER.md` §1 #5–#8), but the BHML_BEING/DOING/BECOMING candidates are Tier-D (per FORMULAS §J.1.B.iii: "exploratory; not yet canonical").
- **Severity:** LOW — FORMULAS Vol J already labels J.1.B.iii as "exploratory; not yet canonical," so the scoping is correct in the canonical reference. The GAP_AUDIT statement that the σ²-triadic projection structure is foundation-canonical is correct for Cycle A/B (Tier-A) but should not extend to the BHML candidates.
- **Recommended fix:** In `GAP_AUDIT.md` #5, separate the two: "Cycle A {1,6,4} = 11 and Cycle B {7,5,2} = 14 substrate-operator decompositions are Tier-A foundation-canonical; the BHML_BEING/DOING/BECOMING value-rotation candidates are Tier-D (search-found, not yet promoted)."

### L2 — `MASTER_ATLAS` and various sprint READMEs reference "the canonical TSML" loosely

- **Location:** Multiple files including `MASTER_ATLAS_2026_04_18.md`, `Atlas/MASTER_ATLAS_v3_5_2026_04_18.md`, sprint READMEs.
- **Claimed tier:** A.
- **Actual tier:** Lens-invariant for many properties (HARMONY count 73, VOID count 17, trace 63, det 0, 4-core, 4-core attractor); but RAW-specific or SYM-specific for the wobble theorem and 12.6% / 12.8% non-assoc rate.
- **Severity:** LOW. Most of these are summary-level documents that do not anchor a specific theorem. The disambiguation matters at the paper level (M1, M2, M5) but not at the synthesis level.
- **Recommended fix:** No urgent action needed. When updating any of these documents, prefer "the canonical CL bit pattern" (Tier-A), or "TSML (lens choice as scoped in [paper X])" rather than "the canonical TSML" un-scoped.

### L3 — WP104 "Path A vs Path B" framing — already corrected, but original framing persists in some downstream summaries

- **Location:** `papers/wp104_higgs_pati_salam/WP104_TWO_ROADS_TO_PATI_SALAM.md` was updated with a CORRECTION NOTICE in 2026-04-27. But sister papers and the integration document still summarize WP104 as "two paths converge on Pati-Salam" without flagging the post-2026-04-27 audit.
- **Claimed tier:** B — "Path A and Path B both land on Pati-Salam ⊕ B−L."
- **Actual tier:** B on **structural alignment** (16-dim doubly-invariant content = su(4) ⊕ u(1) is the Pati-Salam factor + B−L; Path B); **B on incomplete structural alignment** for Path A (the 9-vector VEV breaks SO(10) → SO(8), not SO(10) → SU(4) × SU(2) × SU(2)). Per WP104's own correction notice and D72.
- **Severity:** LOW. WP104 itself has the correction notice prominently. The downstream framing in sister papers and integration documents has not propagated the correction.
- **Recommended fix:** Anywhere "two paths to Pati-Salam" appears in sister papers or summaries, link to WP104's correction notice. Re-frame as "two structurally distinct observations about TIG's so(10), one of which (Path B's doubly-invariant subalgebra) corresponds to a Pati-Salam factor + B−L, the other (Path A's Higgs VEV) breaks to SO(8); they do NOT close on the same reduction."

---

## §4 — Verification: claims that are honestly tier-disciplined and should NOT be flagged

The following pre-existing scoping is correct and should not be touched:

- **WP113 abstract**: "EMPIRICAL (sharpened); structural uniqueness theorem remains open." This properly scopes the PSLQ result as Tier-D-with-density-improved, and §4.1 explicitly states "this is NOT a proof that the runtime attractor is transcendental at every rational α ≠ 1/2."
- **WP114 abstract**: "EMPIRICAL. Extends WP106 (distilgpt2 negative) to a 9-family battery of structured 10×10 matrices." Scope is honestly stated.
- **D78 promotion of α-uniqueness from Tier-D to Tier-B**: This is the model promotion. The Galois argument provides explicit forcing for the H/Br projection at α=1/2; the promotion is documented, scoped (per-projection), and verified.
- **WP104 correction notice (2026-04-27)**: Already does the right work. The correction is prominent at the top of the paper.
- **FORMULAS §J.1.B.iii**: "σ²-triadic candidates for 'three BHMLs' (exploratory; not yet canonical)" is the correct scoping.
- **`TABLE_INDEPENDENCE_LEDGER.md`**: Already classifies every load-bearing claim and identifies 0 critical Tier-D-as-Tier-B violations. The two open scope-tightening items (claims #43, #47) are M-severity, captured here as M4.
- **`RIGOR_ANALYSIS.md`**: Honestly identifies "Real flagship-grade matches: 3" out of the 50+ table entries and scopes the rest by precision tier.
- **MASTER_SPINE.md (D1–D17)**: Each entry has a "Does NOT claim:" guard line; this is the discipline pattern that should propagate to FORMULAS.

---

## §5 — Recommended next steps

1. **(One paragraph fix; do today)** Patch `_CK_MEMORY_MAKEOVER.md` to remove the contradiction between "CL is COMMUTATIVE (verified)" and the WP100s tower's TSML_RAW usage. This is the fastest one-edit fix that closes Contradiction #1 from `GAP_AUDIT.md`.
2. **(One-line annotations; do this week)** Add scope notes to WP107, WP109, WP112, WP115 abstracts per M1, M2, M4. Sprint 17 NOTATION_SHEET fix per M5.
3. **(Audit + decide; do before any Phase 4 paper)** Re-classify the `MASTER_SYNTHESIS_TABLE.md` entries with an explicit "Origin tier" column. This is the H3 fix and the most labor-intensive — but it is also the single highest-leverage edit for "going public" credibility.
4. **(Synthesis pass; do before WP116 finalizes)** Resolve the H1 narrative around "5 manifestations of WOBBLE 11" by either separating the three Tier-D items from the Tier-B item, or finding a forcing argument that connects them (a single proof showing all four arise from the same algebraic source would promote them collectively to Tier-B).
5. **(Brute-force enumeration; cheap)** Verify the joint TSML+BHML 8-shell chain on TSML_RAW. If lens-invariant, claim #43 is closed. If not, the four-core paper needs to scope the chain explicitly to TSML_SYM.

---

## §6 — Bottom line

The corpus has a **discipline ceiling** problem more than a discipline floor problem. The base layer (`TABLE_INDEPENDENCE_LEDGER.md`, FORMULAS proof-spine D-rows with their "PROVED / EMPIRICAL / SYNTHESIS / SPECULATIVE" tags, the WP papers themselves, and `MASTER_SPINE.md`'s "Does NOT claim:" pattern) is already largely tier-disciplined. The conflations identified above sit in the **synthesis layer** — `MASTER_SYNTHESIS_TABLE.md`, `INTEGRATION_WITH_PROOF_SPINE.md`, `_CK_MEMORY_MAKEOVER.md` — where the cumulative narrative across multiple findings is presented at a lower scope-discipline standard than each individual finding.

This is the right diagnosis: the substrate-and-papers are already at publication-grade tier discipline; the synthesis documents need to be brought up to that standard before going public.

**Estimated revision scope:** Minor scoping fixes (4–5 hours of editorial work) for M1–M5, plus a substantive re-classification pass on `MASTER_SYNTHESIS_TABLE.md` (1 work-day) for H3, plus the `_CK_MEMORY_MAKEOVER.md` patch (30 min) for H4. The H1 + H2 narrative fix can be deferred to the methodology paper (Sept 11 anchor) since it requires the tier framework itself to be settled.
