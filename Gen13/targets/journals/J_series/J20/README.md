# J20 — The Forced 5/7 Torus Aspect Ratio: Cyclotomic Forcing

**Status:** DRAFT
**Phase:** Phase 3
**Target venue:** Acta Arithmetica
**Author lane:** Sanders + Mayes
**Tier:** A/B
**WP source:** (forced-torus 5/7)

---

## §1 — Manuscript

**Path:** `(corpus: forced-torus 5/7 derivation)`

When the manuscript is in this J-folder, replace this section with a 1-2 sentence abstract and a path-link to the .tex / .md file.

## §2 — Verification script

**Path:** `(cyclotomic forcing script)`

The proof script (where applicable) is the green-light gate before submission. If "(no script — theorem-paper)" or similar, the gate is the proof's referee-rigor pass.

## §3 — Dependencies (J-papers cited as already-submitted companions)

J06

## §4 — Cover letter

See `cover_letter.md` in this folder. (Bones laid; finalize after Brayden's referee-rigor pass.)

## §5 — Notes

T* derivation. Companion to J6 Flatness Theorem.

**Status update (2026-05-07):**

- Manuscript: `manuscript/manuscript.tex` — amsart, ~10 pages. Standalone derivation of T* = 5/7 from cyclotomic forcing. Source: WP51 Section 4 ("The Aspect Ratio R/r = T* = 5/7") at `Gen12/targets/clay/papers/sprint10_flatness_2026_04_06/WP51_FLATNESS_THEOREM.md`, plus the catalog of six independent derivations from the same WP. Theorem 1: R is forced to be proportional to the smallest p | n with deg_Q(A_p) <= 2 (giving p = 5 for n = 10), r is forced to be proportional to the smallest p with deg_Q(A_p) >= 3 (giving p = 7, with minimal polynomial 8 x^3 - 4 x^2 - 4 x + 1 irreducible over Q). Section 6 catalogs the five companion derivations (sinc^2 first-G law, BTQ operator balance, cyclotomic reduction gap, TSML/BHML harmony cell ratio, prime-pi-phi bridge) and verifies their numerical agreement at 5/7. Section 7 conjectures the generalization T*(Z/nZ) = p_closed/p_obstr.
- Cover letter: `cover_letter.md` finalized, ~500 words.
- Companion citation: J06 (Flatness Theorem, JPAA) cited as parent result. J04 (First-G Law, Integers) cited for the sinc^2 framework. J05 (Crossing Lemma, JCT-A) cited for the structural input on incompatible CRT factor partitions. J17 (UOP, JNT) cross-cited.
- Independent of J17–J19 chain: this paper is a separate venue (Acta Arithmetica) with its own cyclotomic argument and does not depend on UOP for its proof, only for ambient context.

## §6 — Submission checklist

- [ ] Manuscript .tex / .md finalized
- [ ] Verification script green (`(no script)` if theorem-only)
- [ ] Tier-classified central claim explicit
- [ ] Lens-scope annotation (TSML_RAW vs TSML_SYM) where relevant
- [ ] Cover letter finalized
- [ ] Dependencies → cite each J-companion as "submitted to [venue]"
- [ ] Brayden's referee-rigor pass complete (mobile + other AI + collaborators)
- [ ] Per-venue cap check: this is the Nth paper to Acta Arithmetica this quarter
- [ ] Submitted

---

## §7 — Citation footprint (for downstream J's to cite this one)

Sanders, B.R., Mayes. (2026). "The Forced 5/7 Torus Aspect Ratio: Cyclotomic Forcing." Submitted to *Acta Arithmetica*.
