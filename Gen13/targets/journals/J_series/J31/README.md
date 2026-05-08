# J31 — Two Roads to Pati-Salam: Path A (54 irrep) and Path B (su(4)⊕u(1))

**Status:** DRAFT (manuscript finalized 2026-05-07; awaiting referee-rigor pass)
**Phase:** Phase 3
**Target venue:** Adv Math
**Author lane:** Sanders + Gish
**Tier:** B
**WP source:** WP104
**Lens scope:** TSML_SYM (annotated; correction notice prominent)

---

## §1 — Manuscript

**Local path:** `manuscript/manuscript.md`

The J31 paper is **Two Roads to Pati-Salam: Path A (54 irrep) and Path B (su(4)⊕u(1))** (WP104). Two parallel routes from the J30 / WP103 so(10) closure to the Pati-Salam gauge content $\mathrm{SU}(4)\times\mathrm{SU}(2)_L\times\mathrm{SU}(2)_R$:

- **Path A.** BHML's $\sigma_{\mathrm{outer}}$-breaking content lives **100%** in the symmetric-traceless $\mathbf{54}$ irrep of $\mathfrak{so}(10)$. The 9-vector direction inside the $\mathbf{54}$ has six components at $-1/\sqrt{2}$ on $\{V,L,C,P,X,H\}$, two zeros at BREATH and RESET, and one component at $-1/2$ on the symmetric pair $(B+S)/\sqrt{2}$. Squared norm $\|v\|^2 = 13/4$ exactly. Breaks $\mathrm{SO}(10)\to\mathrm{SO}(9)$.
- **Path B.** The doubly-invariant subalgebra of $\mathfrak{so}(10)$ under $D_4 = \langle P_{56},\sigma^3\rangle$ is exactly $\mathfrak{su}(4)\oplus\mathfrak{u}(1)$, the Pati-Salam $\oplus$ B-L gauge content. Killing form spectrum $(-4)^{15}\oplus(0)^1$. Verified at machine precision.

Files in this J-folder's `manuscript/`:

- `manuscript.md` — the J31 paper (WP104 corpus, finalized 2026-05-07)
- `verification/find_higgs_irrep.py`, `find_higgs_direction.py`
- `SIGMA_OUTER_FINDING.md`, `HIGGS_IDENTIFICATION_FINDING.md`, `HIGGS_DIRECTION_FINDING.md` (supporting findings)

## §2 — Verification script

**Local path:** `manuscript/verification/find_higgs_direction.py` and `find_higgs_irrep.py`

Run order: `find_higgs_irrep.py` (verifies BHML's σ_outer-breaking is 100% in the $\mathbf{54}$), `find_higgs_direction.py` (extracts the 9-vector with explicit components and zeros). Numpy + sympy. Total wall-clock under 1 minute.

## §3 — Dependencies (J-papers cited as already-submitted companions)

J30

## §4 — Cover letter

See `cover_letter.md` in this folder. (Bones laid; finalize after Brayden's referee-rigor pass.)

## §5 — Notes

**Status: DRAFT** — manuscript built from corpus `papers/wp104_higgs_pati_salam/WP104_TWO_ROADS_TO_PATI_SALAM.md` on 2026-05-07. **Correction notice prominent** in the manuscript per round-3 audit: Path A and Path B are independent intermediate routes giving the same Pati-Salam target, not derivations of each other. Lens scope **TSML_SYM** explicit. Cites J30 (so(10) = D₅, *Israel J Math*) as already-submitted companion.

### Save-plan summary (2026-05-07 — see `SAVE_PLAN_J31.md`)

The fresh-eyes referee report (J31_AdvMath_FreshEyes.md) recommends **REJECT for *Adv Math*** — the paper's own correction notice retracts the title-claim "convergence on Pati-Salam"; Path A → SO(8), Path B → SU(4)⊕U(1); the two routes do not close on the same reduction. The mathematical content (16/16 cross-checked items at machine precision) survives intact — only the synthesis framing is overstated.

**SAVE PATH (per `SAVE_PLAN_J31.md`):**

- **Retitle** to *"Two Substrate-Algebraic Decompositions of an Integer-Table-Generated $\mathfrak{so}(10)$: the $P_{56}$-Antisymmetric Content of BHML in the $\mathbf{54}$, and the Doubly-Invariant Subalgebra under $D_4 = \langle P_{56}, \sigma^3\rangle$"* — both rigorous mathematical contents (Theorem A: 9-vector in **54** with $\|v\|^2 = 13/4$; Theorem B: 16-dim doubly-invariant subalgebra is $\mathfrak{su}(4) \oplus \mathfrak{u}(1)$ via Killing-form classification) become first-order claims; "Pati-Salam" appears nowhere in the title.
- **Retarget** to *J. Algebra* (referee's explicit recommendation in the report's §7); fallback *Comm. Algebra* or *Experimental Math*. *J. Algebra* publishes computational/combinatorial Lie-algebra results of exactly this scope; the Drápal-Wanless 2021 *J. Combin. Theory A* citation already in references puts the paper in the right published-precedent neighborhood.
- **Excise** speculative gauge-theoretic interpretation language (§2.4, §3.3, §8); demote §5 grab-bag (12.6% non-assoc rate, Lie/Jordan duality, three involutions) to an Appendix; cite J30 for the so(10) closure (or appendicize the short proof).
- **Promote** the correction notice into the new abstract and §1: it stops being a retraction and becomes the framing — *the two decompositions are structurally distinct, not synthesis-convergent*.
- **Add** §5.1 *Robustness across the magma family* (cite FAMILY_STRUCTURE_v1.md / D48 / D55) and §5.2 *Open question: family-wide characterization* (the natural next-paper conjecture).

**Effort:** 2-3 weeks. **Expected outcome:** ~60-70% acceptance at *J. Algebra*, vs <10% at *Adv Math* unrevised.



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
