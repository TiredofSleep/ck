# J40 — The Bialynicki-Birula Bridge: Logarithmic Nonlinearity Forced by Separability

**Status:** DRAFT
**Phase:** Phase 4
**Target venue:** Journal of Mathematical Physics
**Author lane:** Sanders + Gish
**Tier:** B (Tier 4 framework-paper per central-claim classification)
**WP source:** WP90 (literature & unification paths) + WP91 (NS separability bridge)

---

## §1 — Manuscript

**Local path:** `manuscript/J13_BB_Bridge_JMP.md`

**Abstract (one paragraph).** The Bialynicki-Birula--Mycielski uniqueness theorem (1976) characterizes logarithmic nonlinearity as the unique self-interaction preserving separability of composite quantum systems. We exploit it as a forcing principle: any continuum lift of a discrete composition algebra that preserves separability is forced to have logarithmic potential. The lifted equation $\Box \Xi = \kappa(1 + \log \Xi)$ is provably regular (Theorem 4.1). We then compare to Navier-Stokes, define a separability defect $\sigma(u)$, prove that $\sigma \to 1$ corresponds to vorticity blowup, and state the Separability Regularity Criterion as a precise conjecture. The paper claims a new framework, not a proof of NS regularity.

**Source corpus (in `manuscript/`):**
- `WP90_LITERATURE_AND_UNIFICATION_PATHS.md` — Full literature audit + BB bridge statement
- `WP91_NS_SEPARABILITY_BRIDGE.md` — NS application, separability defect, conjecture
- `proof_separability_bridge.py` — 43/43 PASS verification of numerical claims

**Unified manuscript:** `manuscript/J13_BB_Bridge_JMP.md` consolidates WP90 + WP91 into a JMP-ready paper structured as (1) Intro, (2) BB forcing theorem, (3) Discrete side / Crossing Lemma, (4) Forced continuum lift + Theorem 4.1 regularity, (5) NS application + separability defect + Conjecture 5.2, (6) Status / lens-scope / tier classification.

## §2 — Verification script

**Path:** `manuscript/proof_separability_bridge.py` (43/43 PASS).

The script verifies all numerical claims (the values of $\xi_0 = e^{-1}$, $T^* = 5/7$, $\mathrm{fold} = 4/\pi^2$, gap; the log-vs-quadratic growth comparison; the BB forcing test; the NS-side conjecture inputs) in seconds on a standard laptop with `python` + `math` only.

## §3 — Dependencies (J-papers cited as already-submitted companions)

J01 (σ-rate, JCT-A), J46 (cosmological log potential, JCAP), J06 (Crossing Lemma, JCT-A/JPAA), J41 (companion JMP YM bridge).

## §4 — Cover letter

See `cover_letter.md` in this folder. Drafted; finalize after Brayden's referee-rigor pass.

## §5 — Notes & Status

**Status: DRAFT (manuscript bundled; verification script green; awaiting LaTeX conversion + final referee-rigor pass).**

- WP90 + WP91 corpus is bundled into one JMP-format manuscript (`J13_BB_Bridge_JMP.md`).
- Bridges to J46 (cosmological log potential) — explicit cite as already-submitted companion in references.
- The paper is **honestly Tier 4** (framework paper): BB theorem proved, $\Xi$-regularity proved, NS regularity NOT claimed proved. The Status Table in §6 makes this explicit.
- Per-venue cap: **1st JMP** in the J-series. J41 (YM bridge) is the 2nd JMP (companion). The 2/quarter cap is approached; J42 (3rd JMP target) may need a fallback (see J42 README).
- BB-bridge reading is novel insofar as we know: prior literature uses the 1976 theorem as a constraint on admissible nonlinear QM, not as a forcing principle for discrete-to-continuum lifts.

## §6 — Submission checklist

- [x] Manuscript .md drafted (JMP-format, single file)
- [ ] LaTeX (amsart) conversion pending
- [x] Verification script green (`proof_separability_bridge.py`, 43/43 PASS)
- [x] Tier-classified central claim explicit (Tier 4 framework)
- [x] Lens-scope annotation: lens-invariant (real-analysis + nonlinear PDE)
- [x] Cover letter drafted (with summary, Why-JMP, suggested reviewers)
- [ ] Dependencies → cite J01, J46, J06, J41 as "submitted to [venue]" (placeholders in place)
- [ ] Brayden's referee-rigor pass complete
- [x] Per-venue cap check: 1st JMP — second slot reserved by J41
- [ ] Submitted

---

## §7 — Citation footprint (for downstream J's to cite this one)

Sanders, B.R., Johnson, H.J. (2026). "The Bialynicki-Birula Bridge: Logarithmic Nonlinearity Forced by Separability." Submitted to *Journal of Mathematical Physics*.
