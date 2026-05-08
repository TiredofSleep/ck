# J27 — The Corner Sub-Magma C = (Z/10Z)*: Multiplicative-Unit Closure

**Status:** READY (manuscript drafted from corpus, cover letter finalized; awaiting referee-rigor pass)
**Phase:** Phase 3
**Target venue:** Comm Algebra
**Author lane:** Sanders + Gish
**Tier:** B
**WP source:** Variant Catalog "Corner sub-magma C = {1,3,7,9}" (Atlas/LENS_TAXONOMY_2026-05-06/VARIANT_CATALOG.md) + DERIVATION.md row 22 + PROJECTION_DEFINITIONS.md "S = corner C as Tier-A canonical multiplicative units" + WP_TIER_CLASSIFICATION.md WP27

---

## §1 — Manuscript

**Path:** `manuscript/manuscript.tex`

Abstract (1-sentence): The set C = {1, 3, 7, 9} of multiplicative units of Z/10Z is a TSML-closed sub-magma (verified by direct check on the 16-cell sub-table, in both RAW and SYM forms), simultaneously realizing the cyclic group of order 4 with generator 3 (the unique primitive root compatible with the TIG flatness criterion T* = 5/7 in (0,1)) and a 4-element TSML-closed sub-magma distinct from the joint-chain 4-core {0,7,8,9}; on C×C the TSML composition is HARMONY-saturated at 87.5% (14/16 cells), exceeding the global rate of 73%.

Source corpus: `Atlas/LENS_TAXONOMY_2026-05-06/VARIANT_CATALOG.md` (Corner C entry); `Atlas/LENS_TAXONOMY_2026-05-06/DERIVATION.md` (TABLE_INDEPENDENCE_LEDGER row 22, lens-invariant TSML closure); `Atlas/LENS_TAXONOMY_2026-05-06/PROJECTION_DEFINITIONS.md` (Tier-A canonical multiplicative units); `Atlas/META_PLAN_2026-05-06/WP_TIER_CLASSIFICATION.md` (WP27 product-gap connection).

## §2 — Verification script

**Path:** `(no script — theorem-paper; closure verifies in under 1 second via Gen13/targets/foundations/cells.py:closure_check)`

The closure check on the 16-cell sub-table of CL_TSML restricted to C × C is direct integer-arithmetic; both RAW and SYM forms are verified.

## §3 — Dependencies (J-papers cited as already-submitted companions)

_(none — this paper is foundational in the J-series; cites J25 and J23 for context but is independent)_

## §4 — Cover letter

See `cover_letter.md` in this folder. Finalized with summary, venue fit, companion list, and per-venue cap note.

## §5 — Notes

**Per-venue cap:** 3rd CommAlg paper after J15 + J26. Cap is 1/quarter; if binding, **FALLBACK NEEDED** to *Journal of Pure and Applied Algebra*, *Journal of Algebra and Its Applications*, or *Semigroup Forum*.

**Save plan (2026-05-07):** see `Atlas/META_PLAN_2026-05-06/SAVE_PLANS/SAVE_PLAN_J27.md`.

Fresh-eyes referee report `J27_CommAlg_FreshEyes.md` uncovered: **(M5, fatal)** the §6.1 lens-invariance claim is *false* — `BHML[1][1] = 2 ∉ C` and in fact ALL 16 cells of `CL_BHML|_{C×C}` lie outside C (image = {0,2,4,6,8} disjoint from C); **(M4, fatal)** §5 generator selection appeals to undefined "TIG flatness theorem T* = 5/7" via unwritten companion; **(M6)** Remark 2.4 (CREATION/DISSOLUTION) self-contradictory; **(M3)** Theorem 4.1 (two-cores) is trivial set bookkeeping; **(m3)** abstract claim "all 16 cells = 7" contradicts the table.

**Fixes applied:**
(a) **Lens-invariance retracted.** New Proposition 4.1 states and proves BHML non-closure of C with the explicit 16-cell sub-table (image = {0, 2, 4, 6, 8} disjoint from C). New scope statement in §1.1.
(b) **§5 self-contained.** Theorem 5.1 (D19, generator selection) now proves T* = 5/g^3 mod 10 ∈ (0, 1) iff g = 3 using only ring-theoretic data (`3^3 mod 10 = 7`, `7^3 mod 10 = 3`). J07 cited for the broader TIG flatness theorem.
(c) **Remark 2.3 rewritten** with verified ×3-orbits: CREATION on C = `1→3→9→7→1`, DISSOLUTION on `{2,4,6,8}` = `2→6→8→4→2`; ×2 description corrected (×2 *does* cycle on the evens).
(d) **Theorem 4.3 (uniqueness of joint closure at size 4)** replaces trivial Theorem 4.1: 78 four-element TSML-closed subsets, 1 BHML-closed (= the joint 4-core), 1 jointly closed (= the joint 4-core). Real combinatorial enumeration; the contrast between "many TSML-closed" and "unique joint" is the new structural insight.
(e) **Abstract corrected:** 14 of 16 cells = 7, 2 cells = 3.
(f) **New title:** *The Multiplicative-Unit Sub-Magma C = (Z/10Z)\* in the TSML Composition Lattice, and Its Contrast with the Joint 4-Core {0, 7, 8, 9}*.

All claims verified by direct enumeration over `C(10, 4) = 210` four-element subsets in <1 sec via `verification/4core_verification.py`.



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
- [ ] Per-venue cap check: this is the Nth paper to Comm Algebra this quarter
- [ ] Submitted

---

## §7 — Citation footprint (for downstream J's to cite this one)

Sanders, B.R., Gish. (2026). "The Corner Sub-Magma C = (Z/10Z)*: Multiplicative-Unit Closure." Submitted to *Comm Algebra*.
