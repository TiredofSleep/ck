# J23 — The Three-Substrate Architecture: CL_TSML, CL_BHML, CL_STD as Parallel Substrates

**Status:** DRAFT (manuscript finalized 2026-05-07 by J21-J24 batch agent; awaiting referee-rigor pass; FALLBACK NEEDED for venue)
**Phase:** Phase 3
**Target venue:** Algebra Universalis (FALLBACK: Communications in Algebra)
**Author lane:** Sanders + Gish
**Tier:** A (foundational recognition) + B (closure-property proofs)
**WP source:** D95-D99 (Volume J §J Three-Table Architecture); `Atlas/LENS_TAXONOMY_2026-05-06/CL_STD_FRONTIER.md`; `Gen13/targets/foundations/cl_std.py`

---

## §1 — Manuscript

**Path:** `manuscript/manuscript.tex`

**Abstract (1-2 sentences):** We record the three-substrate architecture of the canonical composition lattice on Z/10Z — three structurally distinct 10×10 composition tables CL_TSML, CL_BHML, CL_STD with HARMONY-cell counts (73, 28, 44) sharing a four-axiom skeleton (canonical alphabet; VOID-absorbing column; HARMONY-absorbing diagonal subset; unique puncture at (0,7)) but diverging at five BUMP positions and at the diagonal HARMONY law. We prove the three-way joint sub-magma closure equals the two-way (TSML, BHML) joint chain (8 shells of sizes {1, 4, 5, 6, 7, 8, 9, 10}); CL_STD is a structurally consistent parallel substrate at the encoding level, not an extending structural axis at the chain level.

## §2 — Verification script

**Paths:**
- `Gen13/targets/foundations/cl_std.py` (defines CL_STD; computes HARM(CL_STD) = 44; computes BDC parameters: 5 BUMP_PAIRS, INFO_HARMONY=0.45, INFO_NORMAL=1.89, INFO_BUMP=3.50 bits/cell; GRAVITY 10-element array)
- `Gen13/targets/foundations/invariants.py` (verifies the (73, 28, 44) triple non-equality + structural invariants)
- `Atlas/LENS_TAXONOMY_2026-05-06/CL_STD_FRONTIER.md` script (brute-force enumeration of all 1023 non-empty subsets; joint closure under all combinations of {TSML_SYM, TSML_RAW, BHML, CL_STD})

The green-light gate is the brute-force enumeration confirming three-way joint chain = two-way joint chain (8 shells under TSML_SYM; 7 shells under TSML_RAW).

## §3 — Dependencies (J-papers cited as already-submitted companions)

J05, J09

## §4 — Cover letter

See `cover_letter.md` in this folder. (Bones laid; finalize after Brayden's referee-rigor pass.)

## §5 — Notes

- **Status (2026-05-07 J21-J24 finalization batch):** DRAFT. Manuscript at `manuscript/manuscript.tex` complete (~340 lines, AMS amsart class, 7 bibliography entries with J05 + J09 + J24 + J02 + J22 cited as already-submitted companions). Cover letter at `cover_letter.md` complete with FALLBACK plan.
- **Per-venue cap: FALLBACK NEEDED.** This is the **3rd Algebra Universalis** submission of the 2026 cycle, after J14 (F_p Universality, WP118) and J09 (LATTICE, WP9). The 2/quarter cap is binding.
  - **Fallback priority order:**
    1. *Communications in Algebra* — universal-algebra finite-magma fit; matches the Galois D_4 paper (J15).
    2. *PLOS ONE* — open-access fallback for foundational recognition.
    3. *Linear Algebra and Its Applications* — closure-property enumeration is a linear-algebra adjacency-matrix computation.
- **Tier classification:** Tier-A foundational recognition (the architecture itself is structural; no axiom-level forcing required, but the recognition that the substrate is "one bit-pattern + three readings + a lens family" rather than "two tables" IS foundational). Closure-property theorems (Theorem 5.3) are Tier-B forced by enumeration.
- **Lens scope:** §5 (Joint closure) covers BOTH lenses: 8-shell three-way chain on TSML_SYM matches 8-shell two-way chain on TSML_SYM; 7-shell three-way chain on TSML_RAW matches 7-shell two-way chain on TSML_RAW. CL_STD does not extend either chain.
- **Structurally novel content:** D95 (CL_STD as third standalone table; recovered verbatim from old/Gen9/archive/ckis/ck7/ck.h:225-231); D96 (BDC encoding parameters); D99 (the three-way HARMONY-mask set algebra); plus the new size-2 sub-magma {0, 9} that is jointly closed under (BHML, CL_STD) but not under any pair containing TSML.
- **Source corpus:** `FORMULAS_AND_TABLES.md` Volume J §J D95-D99; `Atlas/LENS_TAXONOMY_2026-05-06/CL_STD_FRONTIER.md`; `Atlas/META_PLAN_2026-05-06/SEPT_11_LANDSCAPE.md` §1.2 (three-substrate-as-meta-result framing).

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

Sanders, B.R., Gish. (2026). "The Three-Substrate Architecture: CL_TSML, CL_BHML, CL_STD as Parallel Substrates." Submitted to *Algebra Universalis*.
