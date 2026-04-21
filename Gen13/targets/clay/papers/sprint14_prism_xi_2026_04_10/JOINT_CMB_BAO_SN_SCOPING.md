# Joint CMB + BAO + SN Analysis — Scoping for ξ Field Cosmology

**Date:** 2026-04-17
**Status:** `[SCOPING]` — design document, no fits performed yet
**Triggered by:** `DESI_MCMC_RESULTS.md` showed Δχ² = −1.59 (ΛCDM mildly preferred) on DESI DR1 BAO alone, with ξ best-fit drifting to unrealistic Ω_m = 0.586, h = 0.484. The ξ model needs CMB and SN constraints to pin Ω_m, h, ω_b before its w(z) signature can be fairly evaluated.

---

## 1. The honest problem

The current ξ analysis state:

- **ξ predictions (analytic):** w(z) → −1 at low z, "freezing quintessence" with controllable thawing rate κ. Gives ξ_vac = e⁻¹ from V = ξ log ξ minimization.
- **ξ vs DESI BAO alone:** ξ fits to χ² = 15.7 vs ΛCDM 14.1 (Δχ² = −1.6). Best-fit hits Ω_m = 0.586, h = 0.484 — **way outside Planck constraints** (Ω_m = 0.315 ± 0.007, h = 0.674 ± 0.005). The fit is trading matter density to mimic dark-energy behavior.
- **Diagnosis:** BAO alone cannot pin Ω_m and h. The ξ model has 6 free parameters (Ω_m, ω_b, h, κ, ξ_init, ξ'_init) vs 12 BAO observables. The likelihood surface has flat directions that ξ exploits.

The proper test: does ξ survive when **CMB + BAO + SN** all constrain (Ω_m, ω_b, h) simultaneously, leaving only (κ, ξ_init, ξ'_init) to fit dark-energy behavior? If ξ can match ΛCDM under that joint constraint, the freezing-quintessence prediction is real. If it cannot, ξ as currently parameterized is ruled out.

---

## 2. Three deliverables, ordered by escalation cost

### Tier 1 — Minimum viable joint analysis (MVJA)

**Purpose:** Fast sanity check using compressed likelihoods. Tells us whether ξ is even in the right ballpark when CMB + SN constraints are imposed.

**Inputs (no Boltzmann solver needed):**

1. **CMB compressed likelihood** (Planck 2018 distance priors): ℓ_A (acoustic scale), R (shift parameter), Ω_b h². This compresses Planck's full TT/TE/EE+lowE chains into a 3D Gaussian on (ℓ_A, R, Ω_b h²). Reference: Chen, Huang & Wang 2019 (arXiv:1808.05724) for the Planck 2018 distance-prior covariance.
2. **DESI DR1 BAO** (already implemented in `desi_xi_mcmc.py` — 12 measurements).
3. **Pantheon+ SH0ES** Hubble diagram (1701 supernovae, z ∈ [0.001, 2.26]). Use the public covariance matrix from Scolnic+ 2022 (arXiv:2202.04077).

**ξ background already coded.** The MVJA adds two log-likelihood functions to the existing `desi_xi_mcmc.py`:
- `log_lik_cmb_compressed(theta)` — computes (ℓ_A, R, ω_b) from ξ background, evaluates against Planck 2018 distance-prior covariance.
- `log_lik_pantheon(theta)` — computes μ(z) = 5 log₁₀(d_L(z) / 10 pc) for each SN, evaluates against Pantheon+ covariance.

**Total chi-squared:** χ² = χ²_BAO + χ²_CMB,compressed + χ²_SN.

**Implementation cost:** ~1 day. New script: `desi_xi_joint_compressed.py`. Adds ~250 lines on top of the existing MCMC harness. emcee with 64 walkers × 4000 steps for 6 params.

**What it tells us:**
- If ξ joint χ² > ΛCDM joint χ² by Δχ² > +6 → ξ is **disfavored** at >2σ, even before Boltzmann-level analysis. Stop.
- If Δχ² ∈ [-2, +2] → ξ is **competitive**. Escalate to Tier 2.
- If Δχ² < -2 → ξ is **preferred** by joint distance data. Worth Tier 3 publication push.

**Honest limit:** Compressed CMB throws away early-universe physics constraints (most importantly, the integrated Sachs-Wolfe effect, which is sensitive to dark-energy behavior). It gives the right answer for distance-only models but can be misleading for models that affect CMB sourcing. ξ enters classical Friedmann at low z, so distance priors should be adequate — but this is a known caveat.

---

### Tier 2 — Full Boltzmann joint analysis

**Purpose:** Publication-grade fit using a real Boltzmann solver. Resolves Tier 1's compressed-CMB limitations.

**Tooling choice (two viable paths):**

#### Path A — CAMB + Cobaya
- **Pros:** Most widely used in cosmology community. Cobaya has built-in Planck 2018 likelihood, BAO, SN modules. Easier to add ξ as a custom dark-energy fluid via Cobaya's `theory.cosmo` interface.
- **Cons:** Adding ξ background to CAMB requires writing a Fortran patch OR using CAMB's `DarkEnergyFluid` Python interface with custom w(z) tabulation. The latter is cleaner.
- **Effort:** ~3–5 days. Steps:
  1. Install CAMB + Cobaya in a venv (pip install camb cobaya).
  2. Write `xi_cosmology/__init__.py` exporting w(z), ρ_DE(z) tables computed from ξ background.
  3. Configure Cobaya YAML pointing CAMB to use the tabulated w(z).
  4. Add likelihoods: planck_2018_lowl.TT_clik, planck_2018_lowl.EE_clik, planck_2018_highl_plik.TTTEEE, bao.desi_dr1, sn.pantheon_plus_shoes.
  5. Run MCMC, ≥10× walkers compared to Tier 1, ≥50k steps. Posterior convergence required (Gelman-Rubin R-1 < 0.05).

#### Path B — CLASS + MontePython
- **Pros:** CLASS has cleaner native support for non-standard dark-energy models via its `fluid` module. MontePython has the right likelihoods bundled.
- **Cons:** MontePython is in maintenance, less actively developed than Cobaya. Steeper learning curve.
- **Effort:** ~5–7 days.

**Recommendation:** Path A (CAMB + Cobaya). Wider adoption means easier review, and CAMB's tabulated-w(z) interface is sufficient for ξ since we don't need to modify perturbation equations (ξ is sub-dominant at recombination by construction).

**What it tells us:**
- Same Δχ² verdict as Tier 1, but with full early-universe physics. Resolves any ambiguity from compressed-CMB.
- Posteriors on (κ, ξ_init, ξ'_init) under joint constraint. If these are tightly bounded and the resulting w(z) is distinctive from ΛCDM at z ~ 0.1–0.5, this becomes the headline plot for the paper.
- σ⁸ tension check: ξ cosmology might either alleviate or worsen the σ⁸ tension between Planck and weak-lensing surveys (KiDS-1000, DES Y3). Worth computing as a side metric.

**Honest limit:** Tier 2 still treats ξ at the background level (homogeneous). Full perturbation theory (the ξ field's effect on growth of structure) is Tier 3.

---

### Tier 3 — Perturbation-level analysis + weak lensing

**Purpose:** Complete the analytical chain. Fit ξ against full LSS data (KiDS-1000, DES Y3) using perturbed Klein-Gordon equation for δξ.

**Effort:** Substantial — ~2–3 weeks. Requires:
1. Linearized perturbation equations for ξ around the cosmological background. The field is light (m²_ξ = κe ~ 10⁻³³ eV² for κ ~ 1) so it propagates with c_s ≈ 1 sound speed. Standard light-scalar treatment.
2. CAMB modification or CLASS scalar-field module to evolve δξ alongside CDM and baryons.
3. Joint fit with weak-lensing 2-point data (ξ_+ and ξ_- correlation functions, or angular power spectra C_ℓ^κκ).

**This is the "JCAP-grade ξ paper" target.** Tier 1 tells you whether to even attempt Tier 3.

---

## 3. Recommended sequencing

| Phase | Deliverable | Decision point |
|---|---|---|
| **Now → +1d** | Tier 1 MVJA. New script `desi_xi_joint_compressed.py`. | If Δχ²_joint > +6: STOP, ξ as currently parameterized is ruled out. Document negative result. |
| **+1d → +1w** | If Tier 1 gives Δχ² ∈ [-2, +2]: Tier 2 (CAMB + Cobaya). | If Tier 2 gives Δχ²_joint < +2: ξ is publishable as "consistent with joint distance data with falsifiable w(z)." |
| **+1w → +3w** | If Tier 2 looks clean: Tier 3 perturbations + weak-lensing. | The full JCAP submission. |

**The negative result is also publishable.** If Tier 1 rules out ξ at >2σ joint, the right paper is "ξ field with V = ξ log ξ falsified at the joint distance-data level." That clears the ground for the next dark-energy proposal and demonstrates the falsifiability discipline.

---

## 4. Concrete first step (this week)

Implement Tier 1 in the existing sprint folder:

```
Gen12/targets/clay/papers/sprint14_prism_xi_2026_04_10/
├── desi_xi_mcmc.py                 (existing — BAO only)
├── DESI_MCMC_RESULTS.md            (existing — Δχ² = -1.6 result)
├── desi_xi_joint_compressed.py     (NEW — Tier 1 MVJA)
├── JOINT_RESULTS.md                (NEW — Tier 1 outcome)
└── JOINT_CMB_BAO_SN_SCOPING.md     (this document)
```

Code skeleton for `desi_xi_joint_compressed.py`:

```python
# 1. Import existing background solver from desi_xi_mcmc.py
from desi_xi_mcmc import solve_xi_background, r_d_eisenstein_hu, DESI_DR1, BAO_observable

# 2. Add Planck 2018 distance-prior likelihood
PLANCK_DP_MEAN = np.array([301.471, 1.7502, 0.02236])  # (l_A, R, omega_b) — Chen+ 2019
PLANCK_DP_COV  = np.array([[...], [...], [...]])        # 3x3 from same paper

def chi2_cmb_distance_priors(theta):
    omega_m, omega_b, h, kappa, xi_i, xi_di = theta
    # compute z_star (decoupling), then l_A, R from background
    # ...
    pred = np.array([l_A, R, omega_b])
    delta = pred - PLANCK_DP_MEAN
    return delta @ inv(PLANCK_DP_COV) @ delta

# 3. Add Pantheon+ SH0ES likelihood
PANTHEON_DATA = np.loadtxt('data/Pantheon+SH0ES.dat')   # zHD, m_b_corr columns
PANTHEON_COV  = np.loadtxt('data/Pantheon+SH0ES_STAT+SYS.cov')  # 1701x1701

def chi2_sn(theta):
    omega_m, omega_b, h, kappa, xi_i, xi_di = theta
    # mu_pred = 5*log10(d_L(z)/10pc) for each SN z
    # ...
    delta = mu_pred - mu_obs
    return delta @ inv(PANTHEON_COV) @ delta

# 4. Joint log-likelihood
def log_prob_joint(theta):
    # priors (BBN omega_b, ranges)
    lp = log_prior(theta)
    if not np.isfinite(lp): return -np.inf
    return lp - 0.5 * (chi2_bao(theta) + chi2_cmb_distance_priors(theta) + chi2_sn(theta))

# 5. Same emcee harness as desi_xi_mcmc.py with 6 params, ~64 walkers x 4000 steps
```

**Required data files (~200 MB):**
- `Pantheon+SH0ES.dat` and `.cov` — public from https://github.com/PantheonPlusSH0ES/DataRelease
- Planck 2018 distance priors — covariance matrix from Chen+ 2019 Table 4 (small, can be hardcoded)

**Runtime estimate:** ~10–15 minutes on a laptop. Background ODE solve dominates; SN likelihood is one matrix-vector op per step.

---

## 5. Honest framing for the paper

Whatever Tier 1 returns, the framing in the paper draft (Sprint 14 PRISM-XI) should change from:

> "ξ produces freezing quintessence that fits DESI DR2 better than ΛCDM"

to:

> "ξ produces freezing quintessence with a specific w(z) curve. On joint CMB + BAO + SN distance data, the ξ model fits to χ²_joint = X vs ΛCDM's Y, giving Δχ² = X − Y over 3 additional parameters. The model is [favored / disfavored / indistinguishable from] ΛCDM at the [...]σ level. Falsifiable predictions remain at z ∈ [0.1, 0.5] for DESI DR3 and the Roman Space Telescope."

This is the discipline §11 of the README requires: state the result, state the data, state the comparison, state what's left to test.

---

## 6. Risk register

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Pantheon+ covariance load fails | Low | High | Use Pantheon+ released `.cov` — well-tested format. |
| Background ODE diverges for some (κ, ξ_init) | Med | Med | Add prior bounds on (κ, ξ_init, ξ'_init); reject samples with non-finite log-prob. |
| ξ model degenerate with Ω_m | High | High | This IS the question Tier 1 answers. If true, ξ is ruled out by CMB+SN. |
| CAMB API changes (Tier 2) | Low | Med | Pin CAMB version in requirements.txt. |
| Compressed-CMB caveat hides perturbation effect | Med | Med | Tier 2 resolves this. Document as caveat in Tier 1 results. |

---

## 7. What this document does NOT do

- Does not perform any fit. This is scoping only.
- Does not modify the existing DESI BAO-only result. The Δχ² = −1.6 stands.
- Does not commit to a publication target. Decision deferred until Tier 1 or Tier 2 verdict.
- Does not claim ξ will pass joint analysis. The honest expectation, given the Ω_m = 0.586 drift in BAO-only, is that joint analysis will pin Ω_m near Planck's 0.315 and worsen ξ's fit. The point of doing the analysis is to confirm or refute this expectation cleanly.

---

*© 2026 Brayden Ross Sanders / 7Site LLC*
*Part of Sprint 14 (PRISM-XI cosmology) closeout, Sprint 17 discipline applied.*
