# J33 — Closed-Form Attractor + α-Uniqueness PSLQ (BUNDLED)

**Status:** DRAFT (manuscript finalized 2026-05-07; awaiting referee-rigor pass)
**Phase:** Phase 3
**Target venue:** Mathematics of Computation
**Author lane:** Sanders + Gish
**Tier:** B
**WP source:** WP105 + WP113 (BUNDLED — Part 1 and Part 2 sections in single manuscript)
**Lens scope:** TSML_SYM 4-core LENS-INVARIANT (4-core sub-magma agrees on TSML_RAW and TSML_SYM)

---

## §1 — Manuscript

**Local path:** `manuscript/manuscript.md`

The J33 paper is a **BUNDLED submission** combining WP105 (Closed-Form Runtime Attractor) and WP113 (α-Uniqueness via PSLQ).

**Part 1 (WP105).** The runtime processor $\mathrm{ck\_process}(p;\alpha,K) = \text{iterate } p\mapsto Z^{-1}[\alpha\widehat{T}(p)+(1-\alpha)\widehat{B}(p)]$ on $\Delta^9$ has a unique attracting fixed point at $\alpha=1/2$ supported entirely on the 4-core $\{V,H,Br,R\}$. **Closed form:** $H^*/Br^* = 1+\sqrt{3}$ exactly; $\xi^* = R^*/Br^*$ is the unique positive real root of the irreducible monic integer quartic $x^4 + 4x^3 - x^2 + 2x - 2 = 0$. The Galois group is $D_4$; the number field is **LMFDB 4.2.10224.1** with discriminant $-10224 = -2^4\cdot 3^2\cdot 71$, class number 1. The quartic factors over $\mathbb{Q}(\sqrt{3})$, anchoring the $\sqrt{3}$ in the H/Br ratio.

**Part 2 (WP113).** A 17-point Stern-Brocot grid + 50-digit mpmath + PSLQ at degree $\le 8$, coefficient $\le 50$ shows: $\alpha = 1/2$ is the **unique rational** in the grid where the runtime attractor admits algebraic relations for both ratios. PSLQ recovers $x^2 - 2x - 2 = 0$ and the LMFDB quartic exactly at $\alpha = 1/2$; finds no relation at the other 16 rationals. Sharpens WP105's D42 from 19-point linspace + brute-force to a stronger empirical test. Conjecture 4.2 (strong α-uniqueness) stated.

Files in this J-folder's `manuscript/`:

- `manuscript.md` — the bundled J33 paper (WP105+WP113 corpus, finalized 2026-05-07)
- `WP105_CLOSED_FORM_ATTRACTOR.md`, `WP113_ALPHA_UNIQUENESS.md` — full source material
- `verification/` — `06_attractor_closed_form.py`, `07_full_closed_form.py`, `alpha_pslq_sweep.py`, `task5_alpha_sweep.py`, plus PSLQ supporting scripts (depth-2/3 primitives, Jacobian checks, LMFDB depth analysis, etc.)

## §2 — Verification script

**Local path:** `manuscript/verification/`

Run order: `06_attractor_closed_form.py` (Part 1, Theorems 3.1, 5.1), `07_full_closed_form.py` (Part 1, Galois identities), `alpha_pslq_sweep.py` (Part 2, PSLQ uniqueness). Total wall-clock under 5 minutes (Stern-Brocot sweep at 50 digits dominates). Numpy + sympy + mpmath. All checks deterministic.

## §3 — Dependencies (J-papers cited as already-submitted companions)

J02

## §4 — Cover letter

See `cover_letter.md` in this folder. (Bones laid; finalize after Brayden's referee-rigor pass.)

## §5 — Notes

**Status: DRAFT** — bundled manuscript built from corpus `papers/wp105_closed_form_attractor/` + `papers/wp113_alpha_uniqueness/` on 2026-05-07. Lens scope **TSML_SYM derivation, 4-core LENS-INVARIANT** (per `Atlas/LENS_TAXONOMY_2026-05-06/TABLE_INDEPENDENCE_LEDGER.md` §5.2 claim #47). Bundled as Part 1 + Part 2 in single .md per J_SERIES_ORDERING.md §4.

**FALLBACK NEEDED if desk-rejected per PHASE4_FALLBACK_UNBUNDLING.md:**
- WP105 (Part 1) → *Communications in Algebra*
- WP113 (Part 2) → *Experimental Mathematics*

The bundled manuscript can be split using the existing corpus files (`WP105_CLOSED_FORM_ATTRACTOR.md`, `WP113_ALPHA_UNIQUENESS.md`) as the unbundled drafts.

## §6 — Submission checklist

- [x] Manuscript .md finalized (bundled)
- [x] Verification script green (3 main scripts; PSLQ deterministic at 50 digits)
- [x] Tier-classified central claims explicit (Part 1 closed form; Part 2 α-uniqueness on Stern-Brocot)
- [x] Lens-scope annotation (4-core LENS-INVARIANT)
- [ ] Cover letter finalized (bones laid; awaits referee-rigor pass)
- [x] Dependencies → cite each J-companion as "submitted to [venue]"
- [ ] Brayden's referee-rigor pass complete
- [ ] Per-venue cap check: this is the 1st paper to *Math of Comp* this quarter
- [ ] Fallback unbundle plan documented (Comm Algebra + Exp Math)
- [ ] Submitted

---

## §7 — Citation footprint (for downstream J's to cite this one)

Sanders, B.R., Gish. (2026). "Closed-Form Attractor + α-Uniqueness PSLQ (BUNDLED)." Submitted to *Mathematics of Computation*.
