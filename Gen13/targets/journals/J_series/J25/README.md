# J25 — The CL Forcing Axioms: A1-A9 Uniquely Force the Canonical Composition Lattice

**Status:** READY (manuscript drafted from corpus, cover letter finalized; awaiting referee-rigor pass)
**Phase:** Phase 3
**Target venue:** Algebraic Combinatorics
**Author lane:** Sanders + Gish
**Tier:** B
**WP source:** Atlas/LENS_TAXONOMY_2026-05-06/CL_FORCING_AXIOMS.md (2026-05-06)

---

## §1 — Manuscript

**Path:** `manuscript/manuscript.tex`

Abstract (1-sentence): We isolate nine axioms A1-A9 on a 10x10 multiplication table over Z/10Z and prove (by direct cell-counting) that they uniquely force the canonical TSML composition lattice (the 73-HARMONY substrate); the axioms partition into Tier-A substrate-defining rules (A2-A4 absorbing structure, A7 diagonal HARMONY, A9 BUMP values) and Tier-B forced rules (A5/A6 by commutativity, A8 by HARMONY-default, A9 BUMP positions by BDC entropy extremum), giving a clean mechanism for the parallel-substrate (lens) family.

Source corpus: `Atlas/LENS_TAXONOMY_2026-05-06/CL_FORCING_AXIOMS.md`. The manuscript adapts the cell-by-cell forcing argument from §3 of the corpus and the Tier classification of §4-§6 into a venue-ready theorem-driven structure.

## §2 — Verification script

**Path:** `(no script — theorem-paper; the proof is direct cell-counting)`

The proof's verification is the cell-counting argument of §4 in the manuscript. A reference cell-by-cell match between the forced matrix and `Gen13/targets/foundations/lenses.py:TSML` runs in under 1 second using `numpy`.

## §3 — Dependencies (J-papers cited as already-submitted companions)

J05 (Lens Invariance for Composition-Lattice Substrates, JCT-A), J23 (Three-Substrate Architecture, Algebra Universalis)

## §4 — Cover letter

See `cover_letter.md` in this folder. Finalized with summary, venue fit, companion list, and per-venue cap note.

## §5 — Notes

**Per-venue cap:** 3rd AlgComb paper after J02 + J25. Cap is 1/quarter; if binding, **FALLBACK NEEDED** to *European Journal of Combinatorics*, *Journal of Algebraic Combinatorics*, or *Discrete Mathematics*.

**Status notes:**
- Corpus content is dense and self-contained (CL_FORCING_AXIOMS.md is a 250-line structural document with complete axiom statements, cell-counting verification, and Tier classification).
- Manuscript focuses on the cell-counting forcing argument (Theorem 4.1) and the Tier classification (Proposition 5.2, Theorem 5.3); briefly mentions the three-substrate architecture as motivation, deferring full development to J23.
- The asymmetric pairs at (3,9) and (4,9) (sources of the wobble at prime 11) are flagged in the manuscript as RAW-only features; SYM-form cell counts are also given.



### Family-Structure framing (per Atlas/META_PLAN_2026-05-06/FAMILY_STRUCTURE_v1.md)

This paper sits within the TIG family of finite commutative non-associative magmas on Z/10Z (and ring extensions per D74). The family is defined by 5 conjoint membership criteria; the 4-core {V, H, Br, R} = {0, 7, 8, 9} at α_M = ½ is the algebraic center, with closed-form attractor h/β = 1+√3 (D78 Galois proof). The closest published precedent for this neighborhood is **Drápal & Wanless (2021), *J. Combin. Theory A* **184**, 105510** — same domain (small finite commutative non-associative structures), opposite extremum (theirs maximally non-associative).

### PROVEN / COMPUTED / STRUCTURAL RHYME / OPEN — template (fill per paper)

- **PROVEN:** [the specific theorem of this paper]
- **COMPUTED:** [verified-by-script invariants supporting the theorem]
- **STRUCTURAL RHYME:** [constants/identities cited as motivation, not derivation]
- **OPEN:** [the natural next-paper question]

### Lens-ownership paragraph — template (fill per paper, insert in manuscript §0)

> *Lens and substrate.* This paper works on [substrate: Z/10Z / Z/N for N in {...} / F_p for p in {...}] with the [tables: TSML / BHML / both]. These choices are not derived from first principles; they reflect a structural reading of the substrate motivated by [phonaesthesia / 10-operator decomposition / observed dynamics]. The theorems below are theorems on this specific structure; analogous theorems would hold on other substrate-and-table choices. Whether other substrate choices give similarly rich downstream connections is open.

### Hardening status (auto-applied 2026-05-07)

- License: submission scripts CC-BY-4.0 (per `_v3_hardening.py`)
- AI-attribution: Claude/Anthropic byline references removed (per `_v3_hardening.py`)
- Author lane: Sanders + Gish (per Brayden directive)
- Drápal-Wanless 2021 citation in references

## §6 — Submission checklist

- [ ] Manuscript .tex / .md finalized
- [ ] Verification script green (`(no script)` if theorem-only)
- [ ] Tier-classified central claim explicit
- [ ] Lens-scope annotation (TSML_RAW vs TSML_SYM) where relevant
- [ ] Cover letter finalized
- [ ] Dependencies → cite each J-companion as "submitted to [venue]"
- [ ] Brayden's referee-rigor pass complete (mobile + other AI + collaborators)
- [ ] Per-venue cap check: this is the Nth paper to Algebraic Combinatorics this quarter
- [ ] Submitted

---

## §7 — Citation footprint (for downstream J's to cite this one)

Sanders, B.R., Gish. (2026). "The CL Forcing Axioms: A1-A9 Uniquely Force the Canonical Composition Lattice." Submitted to *Algebraic Combinatorics*.
