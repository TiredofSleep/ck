# J33 — Closed-Form Algebraic Attractor + α-Uniqueness via PSLQ on a Stern-Brocot Grid (BUNDLED, REVISED 2026-05-07)

**Status:** REVISED 2026-05-07 per fresh-eyes referee report (`Atlas/META_PLAN_2026-05-06/REFEREE_REPORTS/J33_MathComp_FreshEyes.md`); save plan at `Atlas/META_PLAN_2026-05-06/SAVE_PLANS/SAVE_PLAN_J36.md` and the Family-Structure framing at `Atlas/META_PLAN_2026-05-06/FAMILY_STRUCTURE_v1.md` §6.2.
**Phase:** Phase 3.
**Target venue:** *Mathematics of Computation*.
**Author lane:** Sanders + Gish.
**Tier:** B.
**WP source:** WP105 (closed-form attractor) + WP113 (α-uniqueness PSLQ), now bundled as a single **rationally-structured center theorem** with two complementary parts (Part A: Galois proof at α = 1/2; Part B: PSLQ on Stern-Brocot grid).

---

## §1 — Manuscript

**Local path:** `manuscript/manuscript.md`.

The J33 paper has been **rewritten** (2026-05-07) around a single unified theorem per the Family-Structure framing (`FAMILY_STRUCTURE_v1.md` §6.2):

> **Theorem (rationally-structured center).** For the specific quadratic table-fusion process $F_\alpha$ on $\Delta^9$ defined by the integer tables $T, B$ of §1, the unique non-degenerate fixed point at $\alpha = 1/2$ has $h/\beta = 1 + \sqrt{3}$ exactly, and $r/\beta$ is the unique positive real root of the LMFDB-4.2.10224.1 quartic $f(x) = x^4 + 4x^3 - x^2 + 2x - 2$ with Galois group $D_4$.
>
> *Part A (Galois, structural).* At $\alpha = 1/2$, BR-factor cancellation in the BREATH equation forces $y^2 - 2y - 2 = 0$ for $y = h/\beta$, with positive root $1 + \sqrt{3} \in \mathbb{Q}(\sqrt{3})$. The center has rational/algebraic structure exactly at $\alpha = 1/2$.
>
> *Part B (PSLQ, complementary).* At each of the other 16 Stern-Brocot rationals (denominator $\le 7$, with degree $\le 8$ and coefficient $\le 50$ search bounds), no algebraic relation exists. Numerical evidence of transcendental-elsewhere (within bounds).

Files in this J-folder's `manuscript/`:

- `manuscript.md` — the bundled J33 paper, rewritten 2026-05-07.
- `WP105_CLOSED_FORM_ATTRACTOR.md`, `WP113_ALPHA_UNIQUENESS.md` — original source material for traceability.
- `verification/06_attractor_closed_form.py` — Part A: BREATH equation derivation, machine-precision verification.
- `verification/07_full_closed_form.py` — Part A: RESET quartic + LMFDB Tschirnhaus check.
- `verification/alpha_pslq_sweep.py` — Part B: 17-point Stern-Brocot grid + PSLQ at 50-digit precision.

## §2 — Verification

**Local path:** `manuscript/verification/`.

```bash
PYTHONIOENCODING=utf-8 python verification/06_attractor_closed_form.py
PYTHONIOENCODING=utf-8 python verification/07_full_closed_form.py
PYTHONIOENCODING=utf-8 python verification/alpha_pslq_sweep.py
```

Total wall-clock under 5 minutes; the Stern-Brocot sweep at 50 digits dominates. Tables $T, B$ inlined in each script. Python 3.11+, numpy, sympy, mpmath. All checks deterministic.

## §3 — Save plan implementation summary (2026-05-07)

Per `SAVE_PLAN_J36.md` (which covers the META_PLAN family-structure framing and applies to J33 mutatis mutandis) and `FAMILY_STRUCTURE_v1.md` §6.2:

- **Single unified theorem.** The manuscript is now organized around the rationally-structured center theorem, with Part A (Galois, structural) and Part B (PSLQ, complementary) as the two halves.
- **BREATH/RESET derivations written out in the manuscript.** §3.1-3.2 list the four BHML and TSML coordinate equations on $C = \{0, 7, 8, 9\}$ as direct read-offs of the $4 \times 4$ submatrices (16 cells each). §3.3 writes out the four fixed-point equations. §3.4 derives $h/\beta = 1 + \sqrt{3}$ from the (Br) equation (referee §4.1.a-d). §3.5 derives the quartic $f(x) = x^4 + 4x^3 - x^2 + 2x - 2$ from the (R) equation by elimination of $\sqrt{3}$ via squaring (referee §4.1.e).
- **4-core invariance proven structurally.** Lemma 2.1 reads off the 16 cells of each table on $C \times C$ and shows all entries lie in $C$ (referee §4.2). The corresponding empirical-iteration argument is removed.
- **Conjecture 4.2 weakened.** Now Conjecture 5.2: "no algebraic relation of bounded degree and coefficient height" (referee §4.5). The strong "transcendental over $\mathbb{Q}$" claim is dropped.
- **TIG/lens/operad-DOF framing excised.** The "TIG framework," "lens scope," "operad-DOF" language and references to WP102-WP104 are removed; the paper stands on its own with only Drápal-Wanless 2021 [DW21] as the closest published precedent (referee §5.2-5.3, §6).
- **Hand-pickedness of $T, B$ honestly framed.** §1.1 states the tables in full. §8 explicitly notes that the tables are "not derived from first principles; they are stated as the input to the dynamical system." The lens-and-substrate paragraph (per `J_PAPER_BOILERPLATE.md` §5.5) makes the choice transparent.
- **Headline overstatement of 19-point sweep removed.** Replaced by Theorem 5.1 (Stern-Brocot, PSLQ-bounded) without the "uniqueness on a 1-dimensional continuum" framing (referee §4.4).
- **§4.3 "two D₄'s match" speculation removed.** No causal connection is offered or implied.
- **Reproducibility package tightened.** Tables inlined in scripts; one folder; deterministic; no external paths.

## §4 — Cover letter

See `cover_letter.md` in this folder.

## §5 — Family-Structure framing (per `Atlas/META_PLAN_2026-05-06/FAMILY_STRUCTURE_v1.md`)

This paper sits within the small finite commutative non-associative magma neighborhood of Drápal--Wanless 2021. The pair $(T, B)$ is one specific member of that neighborhood; the closed-form attractor + Galois identification + LMFDB-cataloged number field is the structural content of this paper.

The §J.1 inventory's larger family discussion — five conjoint membership criteria, the bimodal $\alpha_A$ gap, the role of TSML\_RAW, the $\sigma$-cycle structure — is *outside the scope of J33*. J33 is the stand-alone theorem on $(T, B)$; the family discussion is for a separate paper (the proposed bimodal-$\alpha_A$-gap paper described in `FAMILY_STRUCTURE_v1.md` §4.2).

## §6 — PROVEN / COMPUTED / STRUCTURAL RHYME / OPEN (per `J_PAPER_BOILERPLATE.md`)

- **PROVEN:** Rationally-structured center theorem — closed-form $h/\beta = 1 + \sqrt{3}$, quartic $f(x) = x^4 + 4x^3 - x^2 + 2x - 2$ with Galois $D_4$, LMFDB 4.2.10224.1 identification (Theorems 3.4-3.5, 4.1, Cor. 4.2).
- **COMPUTED:** Stern-Brocot $\alpha$-uniqueness at PSLQ search bounds (Theorem 5.1; verification script `alpha_pslq_sweep.py`).
- **STRUCTURAL RHYME:** Drápal-Wanless 2021 [DW21] is the closest published precedent — same domain (small finite commutative non-associative structures), opposite extremum (theirs maximally non-associative; ours specifically structured with integer/rational invariants).
- **OPEN:** Transcendence of the runtime fixed-point ratios at every $\alpha \neq 1/2$ (PSLQ at finite bounds cannot decide transcendence).

## §7 — Hardening status

- License: submission scripts CC-BY-4.0.
- AI-attribution: Claude/Anthropic byline references removed.
- Author lane: Sanders + Gish.
- Drápal-Wanless 2021 citation in references.

## §8 — Submission checklist

- [x] Manuscript .md rewritten 2026-05-07 per save plan.
- [x] Verification scripts present and runnable.
- [x] Per-paper rigor pass: BREATH/RESET derivations explicit; 4-core invariance proven structurally; Conjecture 4.2 weakened; framework framing excised.
- [x] Lens-and-substrate paragraph (§8 of manuscript).
- [ ] Cover letter finalized.
- [x] Dependencies: standalone (no companion-paper dependence required).
- [ ] Brayden's referee-rigor pass complete.
- [ ] Submitted.

## §9 — Citation footprint

Sanders, B. R. and Gish, M. (2026). *A Closed-Form Algebraic Attractor for a Quadratic Table-Fusion Process on $\mathbb{Z}/10\mathbb{Z}$, with $\alpha$-Uniqueness via PSLQ on a Stern-Brocot Grid.* Submitted to *Mathematics of Computation*.
