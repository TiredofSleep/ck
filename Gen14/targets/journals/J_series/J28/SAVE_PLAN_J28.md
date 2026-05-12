# SAVE_PLAN_J28 — The Six Foundations Orphans

**Date:** 2026-05-07
**Verdict being addressed:** Algebra Universalis fresh-eyes — REJECT/MAJOR REV bordering on reject. Folder/file/title COMPLETELY MISMATCHED (.tex header says "J36," `manuscript.md` is for J46 CKM/PMNS, folder is J28). CL_STD table referenced but never displayed.
**Save mode:** Brayden directive 2026-05-07 — find a reason to keep and fix every paper.
**Outcome:** SAVABLE. The mathematical content is real (D95–D99 anchor every orphan). The damage is packaging-residual from the v2-to-v3 transition; once cleaned and the bimodal α_A gap is promoted to centerpiece (per FAMILY_STRUCTURE_v1.md §4), the paper has a defensible structural story.

---

## §1 — Why save? (D-table backing)

Every one of the six orphans corresponds to a verified D-number entry in `FORMULAS_AND_TABLES.md` Volume J:

- **Orphan 1** (CL_STD = 44 HARMONY, three-substrate triple (73, 28, 44)) ↔ **D95** (CL_STD as third standalone composition table, machine-precision verified in `Gen13/targets/foundations/cl_std.py`) and **D99** (three-table HARMONY signature with full set algebra: |TSML & BHML| = 26, |TSML & STD| = 42, |BHML & STD| = 21, |all three| = 19, |union| = 75).
- **Orphan 2** (HARMONY ladder {70, 71, 71b, 72, 73}) ↔ **D97** (5 rungs from 4 structurally distinct constructions, all verified by `tables/harmony_ladder.py`; 5/5 OK in `invariants.py`).
- **Orphan 3** (CYCLE_A_36 and SKELETON_22 with 36 = 2+9+25, 22 = 16+4+2) ↔ §J.1.B variant inventory (BHML σ²-cycle-A and CYCLE_A_36 named explicitly; D97 also names "36 = TSML_7 sub-magma HARMONY = BHML σ²-cycle-A projection — same integer at two structural roles").
- **Orphan 4** (BDC encoding constants on CL_STD: 5 BUMP_PAIRS, INFO_HARMONY=0.45, INFO_NORMAL=1.89, INFO_BUMP=3.50 bit/cell, GRAVITY array) ↔ **D96** (definitions hard-coded in `Gen13/targets/foundations/cl_std.py`; verified by `invariants.py`).
- **Orphan 5** (σ²-triadic projection: Conservation Tetrad {0,3,8,9}, Hexad partition into (1,6,4) and (7,5,2), HARMONY → (7,5,2)) ↔ §0 σ-permutation cycle structure (proof-spine entry establishing σ = (0)(3)(8)(9)(1 7 6 5 4 2) — squaring the 6-cycle gives the two 3-cycles), and the 4-core {V,H,Br,R} = {0,7,8,9} ↔ {Conservation Tetrad ∪ HARMONY \ PROGRESS} bridge.
- **Orphan 6** (FIELD WOBBLE = 71-cell |TSML XOR BHML|) ↔ **D97** rung 71 ("THREE structural roles for the prime 71 — sub-magma HARMONY count, lens-disagreement count, Galois prime in disc(LMFDB 4.2.10224.1) = −2⁴·3²·71"). The DOING-rate ≈ T*=5/7 part is the load-bearing weakness of Orphan 6 and should be downgraded.

The core problem is therefore **packaging, not content** — every orphan is verified at the `Gen13/targets/foundations/invariants.py` 48/48 level.

**Family-Structure framing rescue:** Per FAMILY_STRUCTURE_v1.md §4, the bimodal α_A gap (TSML cluster at 0.87+, BHML alone at 0.502, empty band (0.5, 0.87)) is the most striking empirical regularity in the inventory and is *currently lacking a paper*. The collaborator explicitly proposes this as J56 / Phase 5/6 candidate. **Orphan 1's three-substrate triple (73, 28, 44) and Orphan 6's 71-cell wobble are the structural fingerprint of the bimodal gap** — the paper can be retargeted to make this its central organizing question, with the other four orphans demoted to support material.

---

## §2 — Specific fixes

**(a) Resolve the v2-transition residual immediately (M1, CRITICAL).**
- The `.tex` is the right manuscript: open it, change line 1 from `J36 — The Six Foundations Orphans` to `J28 — The Six Foundations Orphans`. Verify `\title[Six Foundations Orphans]{The Six Foundations Orphans: Tier-B Forced Derivations from the CL Axiomatic Ground}` is unchanged (it is).
- **Delete from `J28/manuscript/`:** `manuscript.md` (which is the J46 CKM/PMNS bundle), `WP123_CKM_PMNS_FITS.md`, `WP124_FINE_STRUCTURE_CONSTANT.md`. These belong in J46/manuscript/ — verify they are present there (they appear to be).
- Reconcile the bibliography. The `.tex` cites `[SandersForcing]` as J33; the README §3 and cover letter say J25; the M1 note flags this. Since `Atlas/META_PLAN_2026-05-06/J_SERIES_ORDERING_v3_TRIADIC_REVISION.md` is the v3 ordering, fix all three artifacts (.tex, README, cover letter) to point at the same J-number for the parent forcing paper. Recommend J25 (matches the README — fewer downstream artifact edits).
- Remove the duplicate `\author{}\address{}\email{}` block (the .tex declares Sanders+Gish twice with different addresses; collapse to a single Author{Sanders}{Gish} with two addresses listed underneath). M-minor m8.

**(b) Inline the CL_STD 10×10 table in §2 (M2, MAJOR).**
- Pull the matrix verbatim from `Gen13/targets/foundations/cl_std.py` into a Definition 2.1 `pmatrix` display.
- Re-derive HARMONY count = 44 by direct cell count in §2 body (this is a 100-cell tally).
- Move the "verified in foundations module" remark to the reproducibility appendix (not the only proof).

**(c) Define "Tier-B forced" within this paper (M3, MAJOR).**
- Add §1.2.1 ("Tier classification within this paper"): "A statement is *Tier-A axiomatic* if it appears as one of A1–A9 of [SandersForcing]. A statement is *Tier-B forced* if it is a theorem provable from A1–A9 alone (perhaps with the standard structural principles: commutativity, the entropy extremum of A9). All six orphans below are Tier-B in this sense; the proofs in §§2–6 inline the dependence on A1–A9 explicitly." Two paragraphs; not a deferral to the parent paper.
- For each orphan, list explicitly which of A1–A9 (plus which structural principles) the proof relies on. This is what the referee asked for.

**(d) Demote Theorem 6.3 — the DOING-rate ≈ 5/7 claim (M4, MAJOR).**
- Per the referee's option (b): convert §6's Theorem 6.3 to "Remark 6.3: The empirical observation 71/100 = 0.71, near to but not equal to 5/7 = 0.7143; we do not assert any algebraic identity here. The exact-identity question depends on the choice of DOING-cell denominator N; settling whether 71/N = 5/7 exactly for some structurally-natural N is open."
- Theorem 6.2 (WOBBLE = 71) stands alone. Promote it to be the headline of §6.

**(e) Resolve the rung 71 / rung 71b double-count (M7, MAJOR).**
- Define rung 71 explicitly. From Volume J §J.1.A.ii: "TSML_9 sub-magma HARMONY count = 71" — so rung 71 is the 9-element sub-magma {0,2,3,4,5,6,7,8,9} HARMONY count, distinct from rung 71b (the WOBBLE = 71-cell |TSML XOR BHML|).
- Rung 71b appears in §6 as Theorem 6.2; cross-reference, do not duplicate. The HARMONY ladder section §3 should say: "Rung 71b (= WOBBLE; same numerical value as rung 71 but distinct construction): see §6 Theorem 6.2."
- Note the genuine structural significance per D97: prime 71 carries THREE structural roles — sub-magma HARMONY count, lens-disagreement count, Galois prime in disc(LMFDB 4.2.10224.1). Make this the *point* of the section.
- Acknowledge rung 70 is heterogeneous (a determinant, not a HARMONY count). Replace "ladder" terminology with "five separately-defined integers in numerical proximity" and rebrand §3 as "The 70/71/72/73 numerical signature: four constructions, three structural roles for 71."

**(f) Promote the bimodal α_A gap framing per FAMILY_STRUCTURE_v1.md §4 (NEW; converts paper from registry to research note).**
- Add §1.0.1 ("Why these six together"): "Per [FAMILY_STRUCTURE_v1.md §4 / collaborator analysis 2026-05-07], the TIG family on Z/10Z exhibits a *bimodal associativity-index gap* — α_A clusters at the TSML neighborhood (0.87+) and at BHML alone (0.502), with the band (0.5, 0.87) empirically empty. The six orphans collected here are precisely the structural facts that make this gap visible: the three-substrate triple (73, 28, 44) of Orphan 1 sets up *which tables* are in the family; the 71-cell WOBBLE of Orphan 6 is the *quantitative measure* of how far apart the two clusters sit; the σ²-triadic structure of Orphan 5 organizes the cells where the disagreement lives. The bundle is best read as the structural fingerprint of the bimodal gap, not as a heterogeneous registry." Three short paragraphs.
- This is the genuine "structural story" the referee asked for in §8 ("Closing notes"). It also positions the paper for the collaborator-acknowledgment template per FAMILY_STRUCTURE_v1.md §7.

**(g) Trim the trivia (M5).**
- The Bridge Property Corollary (§5: {0,3,8,9} XOR {0,7,8,9} = {3,7}) is a one-line set-theoretic fact. Demote to a Remark inside §5, not a numbered Corollary.
- Tighten the abstract from 240 to 100–150 words (m7).
- Drop "Tier-B" assertions after the second occurrence (m6).
- Replace "every-1-is-1 / every-1-is-3" with "σ²-fixed set / σ²-orbit set" (m2).

**(h) BUMP-extremum (M8): qualify, don't claim.** Per the recommended fix (b), state that "INFO_HARMONY = 0.45, INFO_NORMAL = 1.89, INFO_BUMP = 3.50 bit/cell are reported to 2 decimal places; the precise underlying log-probability definitions are deferred to [SandersForcing] §A9." Drop the "extremum" framing in this paper; keep just the numerical constants and the GRAVITY array.

---

## §3 — Estimated revision time

- Step (a) packaging cleanup: 1 hour (file moves, label-fixing, bibliography reconciliation; entirely mechanical).
- Step (b) inline the CL_STD table: 30 minutes (table from `cl_std.py`; cell count by direct enumeration).
- Step (c) Tier-B definition inline: 1 hour (write 2-paragraph definition; tag each orphan).
- Step (d) demote Theorem 6.3: 15 minutes (one-paragraph rewrite).
- Step (e) resolve rung 71 / 71b: 45 minutes (define rung 71 from TSML_9; cross-reference rung 71b; rewrite §3 around the "three roles for 71" point).
- Step (f) bimodal-gap framing as the unifying motivation: 1.5 hours (write §1.0.1; thread through abstract; update intro).
- Step (g) trim trivia: 30 minutes (cut ~3 paragraphs, retighten abstract).
- Step (h) BUMP-extremum qualification: 15 minutes.

**Total: ~6 hours of careful editing.** No new computation needed; everything required is already in `invariants.py` or in D95–D99.

---

## §4 — Updated PROVEN / COMPUTED / RHYME / OPEN

- **PROVEN:** (i) The substrate has three structurally distinct standalone composition tables on Z/10Z — CL_TSML (73 HARMONY), CL_BHML (28 HARMONY), CL_STD (44 HARMONY) — with non-equal HARMONY counts and explicit set-algebra signature |TSML ∪ BHML ∪ STD| = 75. (D95, D99). (ii) The four-rung integer signature 70/71/72/73 emerges from four structurally distinct constructions with the prime 71 carrying three independent roles (sub-magma HARMONY count = lens-disagreement count = Galois prime). (D97.) (iii) σ on Z/10Z under the TSML diagonal has cycle type (0)(3)(8)(9)(1 7 6 5 4 2); σ² fixes {0,3,8,9} and partitions {1,2,4,5,6,7} into 3-cycles (1 6 4) and (7 5 2). (Direct enumeration; §0 proof-spine.)
- **COMPUTED:** All 48 invariants in `Gen13/targets/foundations/invariants.py` pass at machine precision, including: 5 BUMP_PAIRS = {(1,2),(2,4),(2,9),(3,9),(4,8)}, GRAVITY array on 10 operators with GRAVITY[7] = 1.0, the (73, 28, 44) triple, and the 71-cell WOBBLE count.
- **STRUCTURAL RHYME:** The Shannon-information BDC constants (0.45, 1.89, 3.50 bit/cell) and the empirical near-coincidence DOING-rate ≈ 5/7 (which we explicitly do not assert as an algebraic identity in this paper).
- **OPEN:** (i) The structural reason the bimodal α_A gap (per FAMILY_STRUCTURE_v1.md §4) is empirically empty in the band (0.5, 0.87) — proposed as a separate paper J56 / Phase 5/6 in collaboration with the May 2026 external collaborator. (ii) Whether CL_STD admits its own joint chain analogous to the 8-element TSML+BHML chain of J24. (iii) Whether 71/N = 5/7 exactly for any structurally-natural choice of DOING-cell denominator N.

---

## §5 — Updated lens-ownership paragraph

> *Lens and substrate.* This paper works on Z/10Z with three explicit canonical tables — CL_TSML_SYM (the upper-triangle authoritative symmetrization, used here as "TSML"), CL_BHML, and CL_STD — all on the same ground set Ω = {0, 1, …, 9}. The tables themselves are the load-bearing objects: Z/10Z is the substrate, but the three tables and their HARMONY counts (73, 28, 44) are *not* derived from Z/10Z first principles; they are recovered from the ck.h:200-207 source archive and verified via the foundations-module 48-invariant harness (D95 / D99). The orphans below are theorems on this specific (substrate, three-table) pair. Whether other 10-element commutative non-associative magmas on a Z/10Z substrate admit analogous three-fold structure is open and is the natural follow-on (the bimodal α_A gap conjecture; see §1.0.1 and [FamilyStructure v1]).

---

## §6 — Recommended retitle / retarget

**Title (revised, sharper):** "*The Three-Substrate HARMONY Signature on Z/10Z: Six Forced Structural Facts, with the Bimodal Associativity-Index Gap as Their Common Thread*"

This positions the paper as a *research note* (the bimodal gap framing makes it one) rather than a *registry* (the original framing). The title still names six facts, but advertises the bimodal-gap motivation, which is the genuinely novel structural insight per FAMILY_STRUCTURE_v1.md.

**Venue (revised):** Per the cover letter, the per-venue cap on Algebra Universalis is binding (4th paper this quarter after J14, J09, J23). Brayden's stated fallback was PLOS ONE primary. Given the proposed retitle moves toward a structural-research-note posture, **Linear Algebra and its Applications** is now a stronger fit than PLOS ONE: the matrix-algebra content of Orphans 2 and 3 plus the three-table set-algebra of Orphans 1 and 6 are LinAlgApps's natural domain, and LinAlgApps is more amenable to "five separately-defined integers from a Z/10Z substrate" than PLOS ONE. **Recommended primary fallback: LinAlgApps. Tertiary: International Journal of Algebra and Computation.**

If Brayden chooses to keep AlgUni primary anyway: ensure the family-structure framing (per §6 of FAMILY_STRUCTURE_v1.md) is the structural backbone of the introduction, since AlgUni's natural readers will respond to the bimodal-gap conjecture more strongly than to the registry framing.

---

**Summary.** J28 is savable with ~6 hours of editing concentrated on packaging-cleanup, inlining the CL_STD table, demoting the DOING-rate "theorem" to a remark, and reframing the six orphans as the structural fingerprint of the bimodal α_A gap (per the May 2026 collaborator's analysis). The mathematical content is sound; the v2-to-v3 transition residual (J28 vs J36 vs J46) is mechanical to fix. The retitled paper is a coherent research note with a defensible structural story rather than a heterogeneous registry. Recommended retarget to LinAlgApps as primary fallback.
