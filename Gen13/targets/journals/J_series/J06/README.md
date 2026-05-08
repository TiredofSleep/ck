# J06 — Crossing Lemma: Non-Associativity as Information Generation in Finite Magmas

**Status:** DRAFT-FINALIZED (manuscript complete; pending Brayden's referee-rigor pass)
**Phase:** Phase 1
**Target venue:** JCT-A OR JPAA (theorem rigor)
**Author lane:** Sanders + Gish
**Tier:** A/B
**WP source:** WP57

---

## §1 — Manuscript

**Local path:** `manuscript/WP57_CROSSING_LEMMA.md`

Single theorem-paper draft built from CROSSING_LEMMA.md (Sprint 10) and WP57 (Sprint 10). Abstract: For squarefree $n$ and $\mathbb{Z}/n\mathbb{Z}$, we prove a single elementary equivalence — the Crossing Lemma — characterizing when a pair of partitions $\{A_d, \pi_{\mathrm{DYN}}(g)\}$ is jointly injective. The condition is: $g$ acts nontrivially on every prime of $n/d$. We unify CRT, $A{+}M$/$M{+}M$/SPEC$+$DYN classifications, orthogonal-jump necessity, and the $p$-kernel obstruction (negative case) under one structure-vs-dynamics template.

## §2 — Verification script

**Path:** `(no script — theorem-paper)`

The proof of Theorem 1 is finite-combinatorial (CRT + cyclic-group orders). Each step is hand-checkable. The gate is referee-rigor pass.

## §3 — Dependencies (J-papers cited as already-submitted companions)

J01, J02, J03 (foundational predecessor — squarefree-stability is the hypothesis we lean on)

## §4 — Cover letter

See `cover_letter.md` in this folder. (Finalized — Summary, Why-venue, Companions, Reproducibility, Reviewers all populated.)

## §5 — Notes

**Status (2026-05-07):** Manuscript draft built in `manuscript/WP57_CROSSING_LEMMA.md`. Cover letter finalized. Per-J-series correction held: NOT expository; theorem rigor venue (JCT-A primary, JPAA backup). The paper is the algebraic spine of the J01–J06 chain.

**What was done:**
- Built `manuscript/WP57_CROSSING_LEMMA.md` from CROSSING_LEMMA.md and WP57 source. Theorem-paper format: 1 main theorem (Crossing Lemma), 1 negative theorem (Theorem 3, $p$-kernel obstruction), 5 corollaries (C1–C5: CRT, $A{+}M$, $M{+}M$, SPEC$+$DYN, orthogonal-jump necessity). Proofs are finite-combinatorial.
- Cited J03 (First-G) as foundational predecessor — squarefree hypothesis used throughout.
- Cited J01, J02, J06 as companions; J06 cites *this* paper as algebraic ground for the torus geometry.
- Cover letter: Summary, Why-JCT-A/JPAA, Companions, Reproducibility, Suggested-reviewers, COI all populated.

**Open issues:**
- Theorem 1's proof has a long case-by-case section (§3.2) that includes a "restart" mid-proof. Reviewer-pass should consolidate this — the corrected version (after Remark 3.1) is the canonical one. Pre-submission cleanup recommended.
- Proof of Corollary C3 ($M{+}M$) is sketched, not fully written. If JCT-A reviewer asks, full proof is in the joint-closure literature and can be added in revision.
- J03 status (Integers) currently FORMAT, not yet submitted — verify J03 is at least submission-ready before this paper goes out, since the cover letter cites it as a companion.

## §6 — Submission checklist

- [ ] Manuscript .tex / .md finalized
- [ ] Verification script green (`(no script)` if theorem-only)
- [ ] Tier-classified central claim explicit
- [ ] Lens-scope annotation (TSML_RAW vs TSML_SYM) where relevant
- [ ] Cover letter finalized
- [ ] Dependencies → cite each J-companion as "submitted to [venue]"
- [ ] Brayden's referee-rigor pass complete (mobile + other AI + collaborators)
- [ ] Per-venue cap check: this is the Nth paper to JCT-A OR JPAA (theorem rigor) this quarter
- [ ] Submitted

---

## §7 — Citation footprint (for downstream J's to cite this one)

Sanders, B.R., Mayes. (2026). "Crossing Lemma: Non-Associativity as Information Generation in Finite Magmas." Submitted to *JCT-A OR JPAA (theorem rigor)*.
