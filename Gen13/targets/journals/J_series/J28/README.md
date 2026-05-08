# J28 — The Six Foundations Orphans: Tier-B Forced Derivations from CL Axiomatic Ground

**Status:** READY (manuscript drafted from corpus, cover letter finalized; awaiting referee-rigor pass; FALLBACK route to PLOS ONE primary if AlgUni cap binding)
**Phase:** Phase 3
**Target venue:** Algebra Universalis (primary) — PLOS ONE / LinAlgApps (fallback, see §5)
**Author lane:** Sanders + Gish
**Tier:** B
**WP source:** Atlas/META_PLAN_2026-05-06/GAP_AUDIT.md §1 (8 foundations orphans listed; bundle 6)

---

## §1 — Manuscript

**Path:** `manuscript/manuscript.tex`

Abstract (1-sentence): We bundle six structural facts from the Z/10Z canonical composition-lattice substrate that have been verified in our Gen13 foundations 48-invariant module but lacked standalone publication: (1) the third canonical lattice CL_STD (44 HARMONY) and the three-substrate triple (73, 28, 44); (2) the HARMONY ladder {70, 71, 71b, 72, 73} of five algebraically distinct rungs; (3) the CYCLE_A_36 and SKELETON_22 derived tables with exact triadic decompositions; (4) the BDC encoding constants on CL_STD (INFO_HARMONY/NORMAL/BUMP = 0.45/1.89/3.50 bit/cell); (5) the σ²-triadic projection structure; (6) the 71-cell field WOBBLE between TSML and BHML, with associated DOING-rate ≈ T* = 5/7. Each is a Tier-B forced derivation from the CL forcing axioms of J25; bundling honors editorial economy while making each fact citable.

Source corpus: `Atlas/META_PLAN_2026-05-06/GAP_AUDIT.md` §1 (lists 8 foundations orphans; we bundle 6, deferring two — PathPair/LensTrace API and eight-shell chain enumeration — to companion papers per the cover letter).

## §2 — Verification script

**Path:** `Gen13/targets/foundations/invariants.py` — runs in under 30 seconds; reports all 48/48 invariants passing as of 2026-05-06.

The six orphans correspond to specific invariants in the harness; they are verified each time the harness runs.

## §3 — Dependencies (J-papers cited as already-submitted companions)

J25 (CL Forcing Axioms, Algebraic Combinatorics — parent axiomatic framework); J23 (Three-Substrate Architecture, Algebra Universalis — provides parallel-substrate background); J22 (HARMONY Ladder, JCT-A — closely related to Orphan 2); J26 (F_p Extensions of CL_BHML, Comm Algebra — provides BHML_8_YM=70 identity used in Orphan 2).

## §4 — Cover letter

See `cover_letter.md` in this folder. Finalized with summary, venue fit, companion list, per-venue cap note, and explicit fallback routing.

## §5 — Notes

**Per-venue cap:** 4th AlgUni paper after J14 + J09 + J23. Cap is 1/quarter and is **BINDING**. **FALLBACK NEEDED**: primary fallback to **PLOS ONE** (broad-scope, tolerant of bundled-result papers; appropriate given orphan heterogeneity); secondary fallback to **Linear Algebra and its Applications** (for the matrix-algebra content of Orphans 2 and 3); tertiary to **International Journal of Algebra and Computation**.

The corresponding author will route to **PLOS ONE** as the primary fallback if Algebra Universalis is unavailable.

**Status notes:**
- Two further orphans (PathPair/LensTrace API and the eight-shell chain enumeration) are deferred to companion papers because they require runtime infrastructure beyond a short note; this is documented in §8.4 of the manuscript.
- The DOING-rate ≈ T* = 5/7 connection (Orphan 6, Theorem 6.3) is presented as an empirical match (rate within 1% of T*) rather than as an exact identity; sharpening to an exact statement is open.
- All six orphans have been verified in the foundations module; the bundle paper does not introduce new computational content but makes existing verified facts citable.

## §6 — Submission checklist

- [ ] Manuscript .tex / .md finalized
- [ ] Verification script green (`(no script)` if theorem-only)
- [ ] Tier-classified central claim explicit
- [ ] Lens-scope annotation (TSML_RAW vs TSML_SYM) where relevant
- [ ] Cover letter finalized
- [ ] Dependencies → cite each J-companion as "submitted to [venue]"
- [ ] Brayden's referee-rigor pass complete (mobile + other AI + collaborators)
- [ ] Per-venue cap check: this is the Nth paper to Algebra Universalis this quarter
- [ ] Submitted

---

## §7 — Citation footprint (for downstream J's to cite this one)

Sanders, B.R., Gish. (2026). "The Six Foundations Orphans: Tier-B Forced Derivations from CL Axiomatic Ground." Submitted to *Algebra Universalis*.
