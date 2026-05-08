# J24 — The Three-Substrate Joint-Closure Chain on Z/10Z: Eight Shells Survive Across (TSML, BHML, CL_STD) with Lens-Dependence Internal to TSML at Size 7

**Status:** DRAFT (rewritten 2026-05-08 to incorporate SFM Q6 finding; supersedes 2026-05-07 lens-only framing; awaiting referee-rigor pass)
**Phase:** Phase 3
**Target venue:** Mathematical Intelligencer
**Author lane:** Sanders + Gish
**Tier:** B (forced by enumeration on three tables; lens-internal scoping explicit per claim)
**WP source:** WP115 (chain count corrected 2026-05-05); SFM Q1+Q6 results 2026-05-08 (`Atlas/META_PLAN_2026-05-06/SUBSTRATE_FUNCTION_MAP/SFM_FINDINGS_v1.md` §2)

---

## §1 — Manuscript

**Path:** `manuscript/manuscript.tex`

**Abstract (1-2 sentences):** Brute-force enumeration on Z/10Z shows that subsets jointly closed under all three canonical tables (TSML, BHML, CL_STD) form a strict 8-element chain at sizes {1, 4, 5, 6, 7, 8, 9, 10}, identical to the (TSML, BHML) joint chain. Individually CL_STD has 50 closed sub-magmas (49 also TSML-closed); adding it as third substrate preserves the entire (T, B) chain without introducing or removing a single shell. The previously-recorded lens-dependence at size 7 (8 shells under SYM, 7 under RAW, forced by TSML_RAW(9, 4) = 3) is shown to be **internal to TSML**: it does not lift to the three-table level because CL_STD does not arbitrate the asymmetric cell. The four-core {0, 7, 8, 9} and the closed-form attractor at α = 1/2 are lens- and table-invariant on all three substrates.

## §2 — Verification scripts

**Primary:** `Atlas/META_PLAN_2026-05-06/SUBSTRATE_FUNCTION_MAP/sfm_q1_q6_q7.py`

The SFM verification script performs the three-substrate enumeration: individual closed sub-magma counts under TSML (449), BHML (9), CL_STD (50); pairwise joint counts (T∩B = 8, T∩C = 49, B∩C = 9); the three-way joint count (T∩B∩C = 8); and the explicit 8-shell chain. Verified at machine precision; runtime under 2 seconds.

**Secondary (legacy):** `papers/wp115_joint_chain_universality/verification/joint_chain_attractor.py` — reproduces the (TSML, BHML) two-table count and the lens-dependence at size 7 with TSML_RAW(9, 4) = 3 as the single asymmetric cell.

The green-light gate is the brute-force confirmation that |T ∩ B ∩ C| = 8 with the chain at sizes {1, 4, 5, 6, 7, 8, 9, 10} — identical to |T ∩ B|.

## §3 — Dependencies (J-papers cited as already-submitted companions)

J02, J05

## §4 — Cover letter

See `cover_letter.md` in this folder. (Bones laid; finalize after Brayden's referee-rigor pass.)

## §5 — Notes

- **Status (2026-05-08 SFM rewrite):** DRAFT. Manuscript rewritten end-to-end at `manuscript/manuscript.tex` to incorporate the SFM Q6 finding (three-table joint chain coincides with two-table joint chain). Replaces the prior 2026-05-07 J21-J24 batch agent draft. ~340 lines AMS amsart, 8 bibliography entries.
- **Title change:** OLD: "The Joint TSML+BHML Chain: Lens-Dependence at Size 7"; NEW: "The Three-Substrate Joint-Closure Chain on Z/10Z: Eight Shells Survive Across (TSML, BHML, CL_STD) with Lens-Dependence Internal to TSML at Size 7." Per SFM_FINDINGS_v1.md §4.1 (J24 retitle directive).
- **Per-venue cap:** 1st Mathematical Intelligencer paper of 2026 cycle. Within 2/quarter cap.
- **Tier classification:** Tier-B forced by enumeration on three tables. The 8-shell three-substrate chain matches the 8-shell two-substrate chain at machine precision; the lens-dependence at size 7 survives as internal to TSML and does not lift.
- **SFM-aligned scope:**
  - Three-substrate chain |T ∩ B ∩ C| = 8 → identical to |T ∩ B| (the headline new result)
  - C alone has 50 closed sub-magmas; 49 of these are also T-closed
  - Lens-dependence at size 7 → internal to TSML's RAW vs SYM choice (does NOT lift to 3-table level)
  - Four-core {0, 7, 8, 9} → lens- and three-table-invariant
  - Closed-form attractor at α = 1/2 → lens- and three-table-invariant
  - The single asymmetric cell killing size-7 under RAW: TSML_RAW(9, 4) = 3 (referee-corrected from prior typo)
- **Referee-fix discipline (per `Atlas/META_PLAN_2026-05-06/REFEREE_REPORTS/J24_MathIntelligencer_FreshEyes.md`):**
  - **Issue 1 (CRITICAL).** §1 cell-value typo fixed: TSML_RAW(4,9) = 7 (not 3 as previously stated); TSML_SYM(4,9) = 7 (not 3); TSML_SYM(9,4) = 7 (not 3); the asymmetric pair is RAW(4,9)=7 vs RAW(9,4)=3 — symmetrized to SYM(4,9)=SYM(9,4)=7. The single load-bearing cell TSML_RAW(9,4) = 3 vs TSML_SYM(9,4) = 7 is now correctly stated throughout.
  - **Issue 2 (MAJOR).** Theorem 5.2 attractor lens-invariance: retained but re-positioned as a corollary of four-core invariance + the existing companion paper [Sanders2026Attractor] derivation; not rederived in scope here.
  - **Issue 3 (MAJOR).** Wobble references removed (manuscript no longer mentions characteristic polynomial coefficients c_2 = 33, c_8 etc.); the wobble localization paper carries that material independently.
- **Chain-count history:** WP115's original (2026-04-26) preprint claimed 7-element chain forbidding {2, 3, 7}. 2026-05-05 brute-force re-verification on TSML_SYM found 8-element chain forbidding {2, 3}. 2026-05-06 lens-dependence identified. 2026-05-08 SFM Q6 lifts the picture to three tables and shows the lens-dependence is internal to TSML. This rewrite is the three-substrate framing.
- **Source corpus:** `Atlas/META_PLAN_2026-05-06/SUBSTRATE_FUNCTION_MAP/SFM_FINDINGS_v1.md` (Q6 result); `papers/wp115_joint_chain_universality/WP115_JOINT_CHAIN_UNIVERSALITY.md`; `Atlas/LENS_TAXONOMY_2026-05-06/TIER_CONFLATION_AUDIT.md` M4; `Gen13/targets/foundations/cl_std.py` (CL_STD definition).



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
- [ ] Per-venue cap check: this is the Nth paper to Mathematical Intelligencer this quarter
- [ ] Submitted

---

## §7 — Citation footprint (for downstream J's to cite this one)

Sanders, B.R., Gish. (2026). "The Joint TSML+BHML Chain: Lens-Dependence at Size 7." Submitted to *Mathematical Intelligencer*.
