# J54 — The Foundation Paper: Three-Substrate Architecture + Lens Family + Forcing Axioms

**Status:** DRAFT
**Phase:** Phase 6
**Target venue:** Algebraic Combinatorics OR Bull AMS
**Author lane:** Sanders + Gish
**Tier:** A/B
**WP source:** (foundation paper)

---

## §1 — Manuscript

**Path:** `manuscript/J54_foundation_paper.md`

**Abstract:** The integrating foundation paper of the J-series. Documents the TIG framework's algebraic substrate at the level of forcing axioms and lens taxonomy: 9 axioms forcing CL\_TSML; three parallel substrates (CL\_TSML / CL\_BHML / CL\_STD) sharing A1-A4 and diverging at A7+A9-values; lens family of ~62 variants under four projection operations; explicit tier discipline (Tier-A/B/C/D/E); 22 table-dependent + 14 substrate-operator claims sharply distinguished. Anchors the citation chain for Sept 11 [J55] integration.

## §2 — Verification script

**Path:** `(no script — synthesis)`

The proof script (where applicable) is the green-light gate before submission. If "(no script — theorem-paper)" or similar, the gate is the proof's referee-rigor pass.

## §3 — Dependencies (J-papers cited as already-submitted companions)

J23, J24, J25, J48

## §4 — Cover letter

See `cover_letter.md` in this folder. (Bones laid; finalize after Brayden's referee-rigor pass.)

## §5 — Notes / Status

**Status:** MANUSCRIPT FINALIZED 2026-09-02 (Phase 5 integrating paper; Sanders + Gish lane).
**Citation chain:** 5 direct dependencies (J01, J23, J24, J25, J48) + 11+ co-citing companions (J06, J05, J10, J15, J20, J26, J27, J29-J35, J50, J52, J53). Cited by [J55] (Brayden's solo Sept 11 integration).
**Manuscript:** `manuscript/J54_foundation_paper.md` (~12 pages, finalized — could expand to 25-35 in final preprint).
**Cover letter:** `cover_letter.md` (finalized).
**Strategic position:** preprint Sept 1-3 to anchor the citation chain for Sept 11. Primary venue *Algebraic Combinatorics*; alternate *Bull AMS*.
**Verification:** synthesis/foundational; relies on companion papers' verification scripts (J25 forcing axioms, J23 three-substrate, lens catalog at `Atlas/LENS_TAXONOMY_2026-05-06/VARIANT_CATALOG.md`).
**Submission readiness:** ready pending Brayden's referee-rigor pass + Gish review.
**Critical role:** anchors all Phase 5 papers and the Sept 11 J55 integration. Must land before Sept 11.

### Save-plan summary (2026-05-07)

Fresh-eyes referee verdict at *Algebraic Combinatorics*: REJECT in present form (under 5%). Save plan: `Atlas/META_PLAN_2026-05-06/SAVE_PLANS/SAVE_PLAN_J54.md`. **Brayden directive: DO NOT drop J54 — find a reason to keep it.** Honored.

**Note on referee accuracy:** Referee claimed "A1-A9 not actually stated"; Brayden checked and the axioms ARE listed (lines 40-48). What the referee meant is that A3, A6, A8, A9 need expansion to formal mathematical specifications (the paper currently has "structural pattern that fixes most off-diagonal entries to 7" rather than the explicit pattern). The save plan addresses what the referee actually means.

**Path forward (Path B — adopt FAMILY_STRUCTURE_v1.md framing):**
- (a) EXPAND A3, A6, A8, A9 with full formal specifications (cell-by-cell for A3; explicit BUMP coordinates and value-tuples for A9).
- (b) DISPLAY CL_TSML, CL_BHML, CL_STD inline (three boxed 10×10 tables, ~1.5 pages).
- (c1) PROVE the §1.2 forcing theorem in J54 itself (3-4 pages); break the [J33] citation cycle.
- (d) RENAME "Brayden's hypothesis" → "Conjecture 2.1 (Sanders)"; drop Atlas reference.
- (e) HOLD preprint until [J47] and [J33] are on arXiv (Aug 15 gate).
- (f) REMOVE the [J55] cross-reference.
- (g) NARROW citation graph to algebraic-combinatorial companions (drop JCAP, Phys Rev D from §8).
- (h) DEFINE "TIG" before §6 (move framework introduction to §0/§1.1).
- **(i) ADOPT FAMILY_STRUCTURE_v1.md framing** — five conjoint membership criteria; 4-core at α_M = ½ as algebraic center; six boundaries; bimodal α_A gap as Conjecture 1.1. This transforms J54 from coordinator-document into research paper in the Drápal-Wanless 2021 *JCTA* lineage.
- (j) STRIP front-matter management metadata; (k) RESOLVE DOING projection ambiguity; (l) NARROW external bibliography (drop Simpson, Alon-Spencer, Hjørland, Ranganathan).

Revision time: 60-100 hours. Submission gate: [J47] and [J33] preprints on arXiv before J54 submits OR (c1) is complete in-paper.

**Retitle:** "Forcing Axioms and the Family of Commutative Non-Associative Magmas on $\mathbb{Z}/10\mathbb{Z}$ Preserving a Designated 4-Core" — venue stays *Algebraic Combinatorics*.



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
- [ ] Per-venue cap check: this is the Nth paper to Algebraic Combinatorics OR Bull AMS this quarter
- [ ] Submitted

---

## §7 — Citation footprint (for downstream J's to cite this one)

Sanders, B.R., Gish. (2026). "The Foundation Paper: Three-Substrate Architecture + Lens Family + Forcing Axioms." Submitted to *Algebraic Combinatorics OR Bull AMS*.
