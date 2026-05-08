# J39 — Two Roads to Pati-Salam: Path A (54 irrep) and Path B (su(4)⊕u(1))

**Status:** DRAFT (manuscript finalized 2026-05-07; awaiting referee-rigor pass)
**Phase:** Phase 4
**Target venue:** Adv Math
**Author lane:** Sanders + Mayes
**Tier:** B
**WP source:** WP104
**Lens scope:** TSML_SYM (annotated; correction notice prominent)

---

## §1 — Manuscript

**Local path:** `manuscript/manuscript.md`

The J39 paper is **Two Roads to Pati-Salam: Path A (54 irrep) and Path B (su(4)⊕u(1))** (WP104). Two parallel routes from the J38 / WP103 so(10) closure to the Pati-Salam gauge content $\mathrm{SU}(4)\times\mathrm{SU}(2)_L\times\mathrm{SU}(2)_R$:

- **Path A.** BHML's $\sigma_{\mathrm{outer}}$-breaking content lives **100%** in the symmetric-traceless $\mathbf{54}$ irrep of $\mathfrak{so}(10)$. The 9-vector direction inside the $\mathbf{54}$ has six components at $-1/\sqrt{2}$ on $\{V,L,C,P,X,H\}$, two zeros at BREATH and RESET, and one component at $-1/2$ on the symmetric pair $(B+S)/\sqrt{2}$. Squared norm $\|v\|^2 = 13/4$ exactly. Breaks $\mathrm{SO}(10)\to\mathrm{SO}(9)$.
- **Path B.** The doubly-invariant subalgebra of $\mathfrak{so}(10)$ under $D_4 = \langle P_{56},\sigma^3\rangle$ is exactly $\mathfrak{su}(4)\oplus\mathfrak{u}(1)$, the Pati-Salam $\oplus$ B-L gauge content. Killing form spectrum $(-4)^{15}\oplus(0)^1$. Verified at machine precision.

Files in this J-folder's `manuscript/`:

- `manuscript.md` — the J39 paper (WP104 corpus, finalized 2026-05-07)
- `verification/find_higgs_irrep.py`, `find_higgs_direction.py`
- `SIGMA_OUTER_FINDING.md`, `HIGGS_IDENTIFICATION_FINDING.md`, `HIGGS_DIRECTION_FINDING.md` (supporting findings)

## §2 — Verification script

**Local path:** `manuscript/verification/find_higgs_direction.py` and `find_higgs_irrep.py`

Run order: `find_higgs_irrep.py` (verifies BHML's σ_outer-breaking is 100% in the $\mathbf{54}$), `find_higgs_direction.py` (extracts the 9-vector with explicit components and zeros). Numpy + sympy. Total wall-clock under 1 minute.

## §3 — Dependencies (J-papers cited as already-submitted companions)

J38

## §4 — Cover letter

See `cover_letter.md` in this folder. (Bones laid; finalize after Brayden's referee-rigor pass.)

## §5 — Notes

**Status: DRAFT** — manuscript built from corpus `papers/wp104_higgs_pati_salam/WP104_TWO_ROADS_TO_PATI_SALAM.md` on 2026-05-07. **Correction notice prominent** in the manuscript per round-3 audit: Path A and Path B are independent intermediate routes giving the same Pati-Salam target, not derivations of each other. Lens scope **TSML_SYM** explicit. Cites J38 (so(10) = D₅, *Israel J Math*) as already-submitted companion.

## §6 — Submission checklist

- [x] Manuscript .md finalized
- [x] Verification scripts present
- [x] Tier-classified central claim explicit
- [x] Lens-scope annotation (TSML_SYM)
- [x] Correction notice prominent
- [ ] Cover letter finalized (bones laid; awaits referee-rigor pass)
- [x] Dependencies → cite each J-companion as "submitted to [venue]"
- [ ] Brayden's referee-rigor pass complete
- [ ] Per-venue cap check: this is the 1st paper to *Adv Math* this quarter
- [ ] Submitted

---

## §7 — Citation footprint (for downstream J's to cite this one)

Sanders, B.R., Mayes. (2026). "Two Roads to Pati-Salam: Path A (54 irrep) and Path B (su(4)⊕u(1))." Submitted to *Adv Math*.
