# J43 — Spectral Layer Consolidation: G6 + G7 + G8 from Q-series Architecture

**Status:** DRAFT
**Phase:** Phase 4
**Target venue:** European J Combin
**Author lane:** Sanders + Gish
**Tier:** B
**WP source:** (Luther spectral catalog)

---

## §1 — Manuscript

**Path:** `manuscript/J51_spectral_layer_consolidation.md`

**Abstract:** Consolidation paper establishing the canonical reference for three spectral results in Luther's lane: $G_6$ ($\sigma^6 = \mathrm{id}$, Tier-A), $G_7$ (period distribution bimodal $2/5, 3/5$, Tier-B), $G_8$ (three-valued spectral coherence integral $G(s)$, Tier-B). Together they form Layer 4 of the 6-layer Q-series architecture. Canonical citation reference going forward.

## §2 — Verification script

**Path:** `(spectral consolidation script)`

The proof script (where applicable) is the green-light gate before submission. If "(no script — theorem-paper)" or similar, the gate is the proof's referee-rigor pass.

## §3 — Dependencies (J-papers cited as already-submitted companions)

_(none — this paper is foundational in the J-series)_

## §4 — Cover letter

See `cover_letter.md` in this folder. (Bones laid; finalize after Brayden's referee-rigor pass.)

## §5 — Notes / Status

**Status:** REVISED 2026-05-07 in response to fresh-eyes referee report (`Atlas/META_PLAN_2026-05-06/REFEREE_REPORTS/J43_EJC_FreshEyes.md`). Save plan: `Atlas/META_PLAN_2026-05-06/SAVE_PLANS/SAVE_PLAN_J43.md`.

**Math-fix summary (2026-05-07):**
- **G8 partition error fixed.** §4.2 originally claimed high-locus = {5,7}, low-locus = {1,2,4,6}. Direct numpy computation with the manuscript's stated σ and χ gives high-locus = **{4, 7}**, low-locus = **{1, 2, 5, 6}** — i.e., elements 4 and 5 swap roles. Partition table corrected.
- **σ²-Galois explanation replaced with σ³-pairing argument.** The original "σ²-Galois action permutes {1,4,6} and {2,5,7}" is wrong: σ² has 3-cycles `(1 6 4)` and `(2 7 5)` on those sets, not pair-actions. The correct invariance is the σ³-action: σ³ has order 2 on the 6-cycle, partitioning {1,2,4,5,6,7} into the three 2-cycles {1,5}, {2,6}, **{4,7}**. The G-values pair within these σ³-orbits because the orbit at σ³(s) is the same 6-element cycle traversed with a 3-step phase offset; combined with ω⁹=1 and the 6-periodic χ-sequence, |G(s)|² = |G(σ³(s))|² (the complex amplitudes satisfy G_cplx(σ³(s)) = -G_cplx(s)).
- **High/low discriminator clarified.** The high-locus σ³-orbit {4,7} is uniquely the one where the χ-content of the orbit's first three positions is *imbalanced* (ν₊ ∈ {0, 2}, rather than ν₊ = 1 on the other two σ³-orbits). This is the load-bearing combinatorial fact behind the spectral concentration.
- **Verification script added:** `manuscript/verify_G6_G7_G8.py` confirms G6 (σ⁶=id), G7 (period bimodal 2/5, 3/5), and G8 (corrected three-valued partition); also verifies the σ³-pairing algebraically.
- **Architecture framing scope-tightened.** §1 now states up-front that the paper covers Layers 1, 3, 4 (Layer 2 trivial; Layers 5, 6 deferred to companions).

**Citation chain:** foundational paper citing 4 prior J-companions (J01, J05, J21, J33) + 5 cross-references (J48, J51, J49, J31, J32). Cited downstream by many later J-papers as canonical G₆/G₇/G₈ reference.
**Manuscript:** `manuscript/J51_spectral_layer_consolidation.md` (~10 pages; revised 2026-05-07). Filename retains `J51_*` for now; rename to `J43_*` at camera-ready.
**Cover letter:** `cover_letter.md` (finalized).
**Per-venue cap warning:** 3rd EJC submission of the J-series — fallback to *LinAlgApps* or *PLOS ONE* if needed (per `J_SERIES_ORDERING.md` §5).
**Verification:** `manuscript/verify_G6_G7_G8.py` runs all three theorems.
**Submission readiness:** ready for resubmission to EJC after Brayden's referee-rigor pass.



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
- [ ] Per-venue cap check: this is the Nth paper to European J Combin this quarter
- [ ] Submitted

---

## §7 — Citation footprint (for downstream J's to cite this one)

Sanders, B.R., Luther. (2026). "Spectral Layer Consolidation: G6 + G7 + G8 from Q-series Architecture." Submitted to *European J Combin*.
