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

**Status:** MANUSCRIPT FINALIZED 2026-09-06 (Phase 5; Sanders + Gish lane).
**Citation chain:** foundational paper citing 4 prior J-companions (J01, J05, J21, J33) + 5 cross-references (J48, J51, J49, J31, J32). Cited downstream by many later J-papers as canonical $G_6$/$G_7$/$G_8$ reference.
**Manuscript:** `manuscript/J51_spectral_layer_consolidation.md` (~10 pages, finalized).
**Cover letter:** `cover_letter.md` (finalized).
**Per-venue cap warning:** 3rd EJC submission of the J-series — fallback to *LinAlgApps* or *PLOS ONE* if needed (per `J_SERIES_ORDERING.md` §5).
**Verification:** $G_6$, $G_7$, $G_8$ all numerically reproducible from corpus scripts; consolidation paper.
**Submission readiness:** ready pending Brayden's referee-rigor pass + Luther's review of attribution and proofs.



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
