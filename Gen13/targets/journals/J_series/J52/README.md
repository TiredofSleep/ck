# J52 — The TSML Lens Family: A Pedagogical Exposition

**Status:** DRAFT
**Phase:** Phase 6
**Target venue:** Mathematical Intelligencer
**Author lane:** Sanders + Gish
**Tier:** B
**WP source:** (lens-taxonomy expository)

---

## §1 — Manuscript

**Path:** `manuscript/J52_tsml_lens_family.md`

**Abstract:** Pedagogical exposition organizing the 12+ variants of the canonical TSML table on $\mathbb{Z}/10\mathbb{Z}$ — three parallel substrates (CL\_TSML / CL\_BHML / CL\_STD) × three lens-symmetrization projections (RAW / SYM\_upper / SYM\_lower) × $\sigma^2$-triadic rotations and sub-magma restrictions — into one walking-tour for the working mathematician. Three reader exercises illustrate the lens family in action.

## §2 — Verification script

**Path:** `(no script — exposition)`

The proof script (where applicable) is the green-light gate before submission. If "(no script — theorem-paper)" or similar, the gate is the proof's referee-rigor pass.

## §3 — Dependencies (J-papers cited as already-submitted companions)

J24, J48

## §4 — Cover letter

See `cover_letter.md` in this folder. (Bones laid; finalize after Brayden's referee-rigor pass.)

## §5 — Notes / Status

**Status:** MANUSCRIPT FINALIZED 2026-09-09 (Phase 5; Sanders + Gish lane). **REJECT R&R verdict from Math Intelligencer fresh-eyes referee 2026-05-07 (~10% acceptance in present form, 40–55% with M1–M6 addressed); SAVE PLAN written 2026-05-07.**
**Citation chain:** 2 direct dependencies (J24 chain lens-dependence, J48 6-DOF synthesis) + 11 co-citing companions (J05, J23, J25, J26, J27, J30, J31, J33, J37, J35).
**Manuscript:** `manuscript/J52_tsml_lens_family.md` (~10 pages, finalized).
**Cover letter:** `cover_letter.md` (finalized).
**Per-venue cap:** 2nd *Math Intelligencer* submission of the J-series after J24 — at maximum permitted. No further Math Intelligencer.
**Verification:** three reader exercises reproducible from corpus scripts.
**Submission readiness:** **NOT submission-ready in current form.** Hold for substantive rewrite per save plan.

### §5.1 — Save-plan summary (per `Atlas/META_PLAN_2026-05-06/SAVE_PLANS/SAVE_PLAN_J52.md`)

**Save path:** the referee identifies the paper as "a memo to insiders dressed in expository syntax" with 40–55% acceptance probability if M1–M6 are addressed. The mathematical content is real; the rewrite is mechanical. Six fixes:

- **M1 (CRITICAL): DISPLAY THE TABLES.** Insert §1.5 *The canonical objects* with the **CL_TSML 10×10 matrix in full** (~half-page boxed display). Show CL_BHML and CL_STD as diff-tables to CL_TSML. Highlight the two asymmetric cells $(3,9)$ and $(4,9)$ (the wobble carriers per FAMILY_STRUCTURE_v1 §3) in a sidebar. Without the tables, Exercises 7.1–7.2 are uncomputable from the page; this is the single most important fix.
- **M2: STATE A1–A9.** Add §1.5 *Substrate-defining axioms* stating A1–A9 informally but completely; mark the substrate-defining axioms (A7 HARMONY-count, A9-values per FAMILY_STRUCTURE_v1 §1) explicitly. Cite J33 for the formal version.
- **M3: TIER DISCIPLINE.** Rewrite §2 opening with a single consistent statement: CL_TSML is Tier-A; TSML_RAW = $\pi_\mathrm{RAW}$(CL_TSML) is Tier-A (no projection); TSML_SYM and TSML_LOWERTRI are Tier-B projections. Do not contradict elsewhere.
- **M4: REDUCE COMPANION DEPENDENCE.** Absorb three punch-line facts inline with proof sketches: 4-core attractor $H/Br = 1+\sqrt{3}$ (D78 BR-factor cancellation); 8-element joint chain at sizes $\{1, 4, 5, 6, 7, 8, 9, 10\}$ (D64 corrected); wobble localization $c_2 = 33 = 3 \cdot 11$ in TSML_RAW char poly (D37 / J43).
- **M5: POPULATE THE 62-VARIANT CATALOG INLINE.** §6 becomes a two-page landscape table (variant name | one-line distinguishing fact); drop "$\sim$" qualifiers; reconcile the per-tier counts (referee notes 5+21+9+7+8 = 50, not 62). The catalog cannot be deferred to an Atlas markdown file.
- **M6: FIX LENS-DEPENDENCE EXAMPLE.** The current chain-at-size-7 framing conflates a *historical correction* (size 7 was thought forbidden, now known allowed) with *structural lens-dependence*. Replace with the wobble-localization example (referee's own suggestion): TSML_RAW has prime 11 in $c_2$; TSML_SYM does not. This is the cleanest lens-dependence in the corpus. Move chain enumeration to §6.5 *Lens-invariant facts* with the corrected D64 chain stated cleanly.

§8 over-hedging compresses to 2 sentences. Front-matter phase metadata + per-venue cap notes stripped. ASCII-art diagram replaced by TikZ/figure. **Estimated revision: 30–40 person-hours.**

**Retarget option (per referee §8):** if *Math Intelligencer* per-venue cap (J32 already there) blocks, **American Mathematical Monthly** is the strongest fallback. *AMM* takes 10×10 table papers when they have a clean punch line; the wobble-at-prime-11 (M6 fix) is exactly that. *Mathematics Magazine* (MAA) is a strong tertiary option for table-based pedagogical pieces.

**Submission gate:** (a) M1 tables displayed; (b) M2 axioms stated; (c) M3 tier rewrite propagated; (d) M4 three punch-line facts absorbed inline; (e) M5 catalog populated; (f) M6 lens-dependence switched to wobble; (g) Brayden's referee-rigor pass complete; (h) per-venue cap check vs J32.



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

Sanders, B.R., Mayes. (2026). "The TSML Lens Family: A Pedagogical Exposition." Submitted to *Mathematical Intelligencer*.
