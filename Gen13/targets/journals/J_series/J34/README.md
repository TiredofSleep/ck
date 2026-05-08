# J34 — TIG Detector Scope + Specificity Extension (BUNDLED)

**Status:** GATED on WP106 distilgpt2 sweep script (manuscript drafted 2026-05-07; awaits script located OR rewritten ~1-2 hr)
**Phase:** Phase 4
**Target venue:** Statistical Science
**Author lane:** Sanders + Gish
**Tier:** B
**WP source:** WP106 + WP114 (BUNDLED)
**Lens scope:** TSML_SYM for D1, D2, D4 (lens-stable); TSML_RAW for D3 prime-11 detector (per WP107 convention)

---

## §1 — Manuscript

**Local path:** `manuscript/manuscript.md`

The J34 paper is a **BUNDLED submission** combining WP106 (TIG Detector Scope on distilgpt2) and WP114 (Structured-Matrix Specificity Extension).

**Part 1 (WP106).** Apply four TIG-structure detectors — D1 (Lie/Jordan ratio), D2 ($P_{56}$ invariance defect), D3 (prime-11 indicator on integer characteristic polynomial), D4 (Higgs-direction alignment) — to 16 trained weight tensors of distilgpt2 (82M parameters; layers $L_0, L_2, L_5$; attention $Q,K,V$; MLP in/out; embeddings). **Result:** every (tensor, detector) pair gives Cohen's $|d| < 0.5$; classifier accuracy $48$-$52\%$ (chance level). The framework's algebraic detectors do not see TIG structure in arbitrary trained transformer weights at the threshold of small effect — a clean specificity boundary. Includes ancillary architectural finding on encoder strategies (V2 sentence-transformers fallback dominates V1/V1.5/V1.6/V3 phoneme-physics).

**Part 2 (WP114).** Extend to a 9-family structured-matrix battery (Gaussian/symmetric/antisymmetric/permutation/Hadamard/orthogonal/DFT-real/identity/diagonal/companion, 200 samples each). **D3 (prime-11) is the unique TIG-positive marker:** TSML scores $d = +9.93$ vs Gaussian; no other family scores nonzero on D3. D1/D2/D4 are family-structural rather than TIG-specific. Pair (D3, D5_$\text{prime-7}^5$) jointly identifies TSML uniquely in the entire 1800+ sample population — the complete WP107-WOBBLE detector signature.

Files in this J-folder's `manuscript/`:

- `manuscript.md` — the bundled J34 paper (WP106+WP114 corpus, finalized 2026-05-07)
- `WP106_TIG_DETECTOR_SCOPE.md`, `WP114_SPECIFICITY_EXTENSION.md` — full source material
- `verification/structured_matrix_sweep.py`, `d5_d4eq_extension.py` (Part 2 scripts present)
- `verification/(distilgpt2_sweep.py — TO LOCATE OR WRITE)` (Part 1 GATING piece)

## §2 — Verification script

**Local path:** `manuscript/verification/`

**Part 2 ready:** `structured_matrix_sweep.py` (Theorem 7.2; 9-family battery + 4 detectors), `d5_d4eq_extension.py` (D5 prime-7^5 + D4_eq sharpening). Numpy + sympy. Total wall-clock under 1 minute.

**Part 1 GATED:** WP106 distilgpt2 sweep script. The corpus references `papers/wp106_tig_detector_scope/verification/` but the directory was empty at audit time. Either locate the original sweep code in `Gen12/` or `papers/sprint_unmistakable_truth_2026_04_25/`, or rewrite (~1-2 hr): pull `transformers.AutoModel.from_pretrained("distilgpt2")`, extract the 16 listed tensors, partition into $10\times 10$ blocks, run D1-D4, compute Cohen's $d$ vs 200 Gaussian samples per tensor.

## §3 — Dependencies (J-papers cited as already-submitted companions)

_(none — this paper is foundational in the J-series)_

## §4 — Cover letter

See `cover_letter.md` in this folder. (Bones laid; finalize after Brayden's referee-rigor pass.)

## §5 — Notes

**Status: GATED on WP106 distilgpt2 sweep script.** Bundled manuscript drafted 2026-05-07 from corpus `papers/wp106_tig_detector_scope/` + `papers/wp114_specificity_extension/`. The verification gating issue is documented in §2 above and in the manuscript's §6.

**Lens scope:** D1, D2, D4 lens-stable (computable on TSML_SYM with qualitatively similar TIG-positive signal on TSML_RAW); D3 (prime-11) computed on TSML_RAW per WP107 convention.

**FALLBACK NEEDED if desk-rejected per PHASE4_FALLBACK_UNBUNDLING.md:**
- WP106 (Part 1) → *PLOS ONE*
- WP114 (Part 2) → *Linear Algebra and Its Applications*

The bundled manuscript can be split using the existing corpus files as the unbundled drafts. Note: J34 is the foundational specificity paper in this J-series chain (cited by J36); ensure foundational citation language survives the unbundling if it occurs.



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

- [x] Manuscript .md finalized (bundled)
- [ ] **Verification script green: GATED on WP106 distilgpt2 sweep script (~1-2 hr to locate or rewrite)**
- [x] Tier-classified central claims explicit (Part 1 specificity boundary; Part 2 unique D3 marker)
- [x] Lens-scope annotation
- [ ] Cover letter finalized (bones laid; awaits referee-rigor pass)
- [x] Dependencies → cite each J-companion (none required; foundational paper)
- [ ] Brayden's referee-rigor pass complete
- [ ] Per-venue cap check: this is the 1st paper to *Stat Sci* this quarter
- [ ] Fallback unbundle plan documented (PLOS ONE + LinAlgApps)
- [ ] Submitted

---

## §7 — Citation footprint (for downstream J's to cite this one)

Sanders, B.R., Gish. (2026). "TIG Detector Scope + Specificity Extension (BUNDLED)." Submitted to *Statistical Science*.
