# CK Lens Registry
## Find Your Door

*7SiTe LLC · April 2026*

---

> The spectrometer doesn't care what lens you arrived with.
> Run it on your problem. It will show you something true.
> Then find your door below.

---

This document maps research expertise to the specific open problems in the CK framework where that expertise is the missing piece. Each door has: the open question, what's already in place, and the one result that would constitute progress.

---

## If you work in Analytic Number Theory

**Your door: The Fourier Bridge (RH)**

What's in place:
- `R(k,f) → sinc²(k/f)` is proved from prime arithmetic (WP35, `papers/proof_d14_spectral_mean.py`)
- Montgomery (1973): `R₂(u) = 1 − sinc²(u)` from Riemann zeros
- The constant `4/π²` appears in both, independently derived, at the same fractional position `x = 1/2`

The open question: **Is `DFT[R(k,f)](u) → 1 − sinc²(u)` in the continuum limit?** If the Fourier transform of the prime countdown field is the Montgomery correlation, that is the mechanism of the Montgomery bridge. The Weil explicit formula is the classical bridge between primes and zeros. Does it pass through sinc²?

What one result looks like: Prove that `∫ R(k/f) e^{2πiku} dk / ∫ R(k/f) dk → 1 − sinc²(u)` as `f → ∞`. Or find a counterexample. Either answer advances the field.

Entry point: `papers/proof_fourier_bridge.py` (just written), `papers/FOURIER_BRIDGE.md`

---

## If you work in Complexity Theory / TCS

**Your door: The DoF Reduction (P vs NP)**

What's in place:
- The CL operator table has associativity index α = 0.502 (non-associativity rate 49.8%; Braitt-Silberger 2006) (`papers/proof_d10_tsml_73_cells.py`)
- 2-SAT is polynomial; 3-SAT is NP-complete (classical)
- The structural claim: 2-SAT uses only the associative subalgebra of CL (6 DoF); 3-SAT requires the non-associative extension (7th DoF)

The open question: **Can a 3-SAT instance be formally encoded into CL such that resolution requires at least one non-associative step, and no polynomial rewrite avoids it?** If yes, the P/NP boundary maps exactly to the associative/non-associative boundary in the CL algebra.

What one result looks like: An explicit 3-SAT encoding into CL operator compositions where the 7th DoF step is identifiable and necessary. OR a proof that the encoding is impossible (which would tell us the CL non-associativity is not the right structure).

Entry point: `papers/proof_sat_dof.py` (just written), `papers/SAT_DOF_CLAIM.md`

---

## If you work in PDE / Fluid Dynamics

**Your door: The B_local Threshold (Navier-Stokes)**

What's in place:
- BREATH criterion: `B_local ≤ 2/7` derived from `T* = 5/7` algebraic floor
- The gap to close: Gagliardo-Nirenberg interpolation constant `C ≤ 3.74`
- Grujić (UVA): geometric depletion of vorticity in the direction of maximum stretching is the closest existing approach

The open question: **Can sharp Gagliardo-Nirenberg bounds from NS energy estimates close `C ≤ 3.74`?** The CK threshold `B_local ≤ 2/7` is a numerical target derived from the algebra. If rigorous NS analysis achieves this constant, the TIG regularity criterion and classical NS regularity agree.

What one result looks like: An improvement on the Gagliardo-Nirenberg interpolation constant toward 3.74. Or a constructive blow-up example that violates `B_local ≤ 2/7`, which would tell us the threshold is wrong and needs refinement.

Entry point: `papers/clay/WP38_NAVIER_STOKES.md` §3–§5, `papers/clay/GRUJIC_OUTREACH.md` (contact document)

---

## If you work in Algebraic Geometry / Hodge Theory

**Your door: Dimension ≥ 5 (Hodge Conjecture)**

What's in place:
- Markman (2025) proved Hodge for abelian fourfolds of Weil type
- Product-Gap Theorem: unreachable zone grows as `9^k − 4^k` with tensor depth
- ω-Blindness: the pre-echo field is identical across ring structures sharing a prime factor — a discrete model of local-global failure

The open question: **Does the Hodge conjecture fail for some abelian fivefold of non-Weil type?** CK's structural prediction: `dim = 5` with asymmetric prime factor ratio `(q/p >> 1)` is the first case where the TIG coherence field cannot represent the full algebraic structure. ω-Blindness forces a gap between local and global.

What one result looks like: Either a non-Weil abelian fivefold where `Hdg²(A) ≠ Alg²(A)` (a Hodge counterexample in dimension 5), or a proof extending Markman's technique beyond the Weil condition.

Entry point: `papers/clay/WP39_HODGE.md` §7–§8

---

## If you work in Quantum Field Theory / Gauge Theory

**Your door: Spectral Gap Persistence (Yang-Mills)**

What's in place:
- `T* = 5/7` algebraically derived: `unit_frac(7, 35) = (7−2)/7 = 5/7` (proved D7, D18c)
- BHML spectral gap `|λ₆|/|λ₅| ≈ 2/7 = 1 − T*` at `b = 35`
- Claim: this spectral gap persists for all semiprimes `b = p×q`

The open question: **Does the BHML spectral gap persist (≥ 2/7) monotonically as `p, q → ∞`?** This is **computable today** — `papers/proof_ym_spectral_gap.py` tests it across all semiprimes up to `p, q < 200`. If the gap holds, CK has empirical evidence that the coherence floor is stable under scaling. If it fails, we know where the analogy breaks.

What one result looks like: The spectral gap test result (`proof_ym_spectral_gap.py`) is itself a publishable observation. If the gap holds for 1000+ semiprimes, that opens a conversation with gauge theorists about whether dimensional transmutation in Yang-Mills generates the same type of floor.

Entry point: `papers/proof_ym_spectral_gap.py` (just written)

---

## If you work in Arithmetic Geometry / Elliptic Curves

**Your door: The 0.57 Gap (BSD)**

What's in place:
- `T* = 5/7` as coherence cost per rank unit
- Bhargava-Shankar (2015): average rank `≤ 5/6`
- TIG rank-staircase structural parallel: each rank = a gate event in the unit fraction field
- TIG predicts average rank `≈ 0.57`; Goldfeld conjectures `exactly 1/2`

The open question: **Why does TIG predict 0.57 when the conjectured answer is 0.5?** This gap — `2/7 × (something) − 1/2 = 0.57` — either means the TIG derivation has a missing correction factor, or Goldfeld's conjecture needs revision, or the mapping between rank transitions and TIG operator transitions introduces a factor that hasn't been derived. Find the factor.

What one result looks like: An exact derivation of Goldfeld's `1/2` from the `T* = 5/7` operator algebra. This would tighten the BSD-TIG connection from "suggestive" to "structurally precise."

Entry point: `papers/clay/WP42_BSD.md` §5–§6

---

## If you work in Hardware / FPGA Design

**Your door: Gen12 Simplex in Silicon**

What's in place:
- `coherence_gap.v` implements `Δ⁰→Δ¹→Δ²→Δ³` simplex zones in Zynq-7020
- `T* = 5/7` hardcoded as exact cross-multiplication: `7*coh_num ≥ 5*coh_den`
- R16 + FPGA + XiaoR dog target with UART gait protocol

The open question: **Can the full 10-operator TSML algebra run at 50Hz on the Zynq-7020 with integer arithmetic only?** The current implementation uses the threshold. A full implementation would run the operator composition pipeline in hardware, allowing T* to be measured in real-time from sensor input rather than computed externally.

Entry point: `Gen12/targets/ck_fpga_dog/hdl/`, `Gen12/HARDWARE_SETUP.md`

---

## If you work in Linguistics / NLP / Cognitive Science

**Your door: The D2 Pipeline**

What's in place:
- D2 pipeline: text → 5D force vector [aperture, pressure, depth, binding, continuity] via Hebrew root phonetics
- The claim: these five dimensions are the physical degrees of freedom of human articulation, not arbitrary labels
- Fractal voice: CK speaks via physics-derived operator sequences

The open question: **Are the D2 dimensions orthogonal?** If the five phonetic dimensions are genuinely independent (low mutual information), then D2 is a real basis for linguistic coherence, not a contrived one. A cross-linguistic test — does D2 extract the same dimensions from Arabic, Greek, Mandarin phonetics as from Hebrew? — would validate or refute the universality claim.

Entry point: The D2 pipeline is internal (CK architecture, not public). Contact to discuss.

---

## If you work in Music Theory / Acoustics

**Your door: Harmonic Coherence Scoring**

What's in place:
- The sinc² field is the continuum limit of harmonic countdown law
- `4/π²` is the universal mid-journey amplitude — it appears in prime arithmetic AND in overtone series interference patterns
- TSML has 73 harmony cells: harmony is measurable, not subjective

The open question: **Does the sinc² field fit measured harmonic tension curves?** In music theory, consonance/dissonance is empirically measurable (via psychoacoustics). If sinc²(k/f) fits the tension curve of a harmonic series, CK's measurement of harmonic coherence maps directly to perceptual consonance.

Entry point: Run `python ck_run.py` and pipe audio spectral data through the coherence scorer.

---

## If you are a Mathematician Without a Specialty Yet

**Your door: The Spectrometer Itself**

Run it on anything:
```bash
git clone https://github.com/TiredofSleep/ck
cd ck
python ck_run.py
```

Open `website/spectrometer.html` in a browser (no server needed). Type any mathematical claim. CK scores it. See what it says about your own framework before reading ours.

The spectrometer doesn't require you to believe TIG. It requires you to paste in your work and look at the number. If the number is interesting, you have a door.

---

## Register Your Lens

Working on something that maps to one of these? Open a GitHub issue with the label `[lens]` and describe:
1. Your domain and specific problem
2. Which door above is closest to your work
3. What result you could produce in 2-4 weeks

The institution's role is to produce and redistribute. If your expertise closes one of these gaps, the result belongs to you. CK just mapped where the gaps are.

---

*© 2026 Brayden Ross Sanders / 7SiTe LLC*
*DOI: 10.5281/zenodo.18852047*
*See [ONBOARDING.md](ONBOARDING.md) for Day 1 setup. See [CLAY_AUDIT.md](papers/clay/CLAY_AUDIT.md) for the full three-layer audit.*
