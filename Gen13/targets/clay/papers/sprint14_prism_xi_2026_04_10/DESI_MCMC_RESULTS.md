# DESI DR1 BAO MCMC Fit — Results and Honest Reading

**Date:** 2026-04-17
**Script:** `desi_xi_mcmc.py` (this folder)
**Data:** DESI Collaboration / Adame+ 2024, "DESI 2024 VI: Cosmological Constraints from BAO", arXiv:2404.03002, Table 1 (DR1, 12 BAO measurements).
**Infrastructure:** emcee 3.1.6; scipy RK45 background solver; Eisenstein-Hu (1998) r_d fitting formula; BBN prior on ω_b (Cooke+ 2014, ω_b = 0.02235 ± 0.00037, Aubourg+ 2015 convention).

---

## Result

| Model | parameters | χ² | dof | χ²/dof | best-fit |
|-------|------------|-----|-----|--------|----------|
| **ΛCDM baseline** | (Ωm, ωb, h) | **14.127** | 9 | 1.57 | Ωm = 0.303, ωb = 0.0224, h = 0.653, r_d = 154.85 Mpc |
| **ξ field** (log quintessence) | (Ωm, ωb, h, κ, ξ_init, ξ'_init) | **15.715** | 6 | 2.62 | Ωm = 0.586, ωb = 0.0225, h = 0.484, κ = 2.40, ξ_init = 1.37, ξ'_init = 0.052, r_d = 152.40 Mpc |

**Δχ² = −1.59** (ΛCDM preferred). **Δdof = +3** (ξ has three more parameters). No AIC/BIC advantage to ξ either way. **The data do not distinguish the two models; in the direct comparison, ΛCDM wins marginally.**

---

## Comparison with the earlier "χ² = 3.06 vs ΛCDM 15.3" claim

The earlier preliminary result (in `desi_xi_optimize.py`, grid search, README §2):

> "χ² = 3.06 vs ΛCDM 15.3"

was **not** a fit of the BAO data points. It was a fit of the **CPL summary statistics** (w₀, wa) as reported by DESI, against the ξ model's extracted (w₀, wa). That is:

- **Old comparison:** `|(w₀_model − w₀_DESI)/σ_w₀|² + |(wa_model − wa_DESI)/σ_wa|²` — 2 numbers.
- **New comparison:** `Σᵢ |(observable_i_model − observable_i_data)/σᵢ|²` over 12 BAO observables.

The CPL comparison is a much easier likelihood surface: the ξ model can tune its three free parameters to hit two summary statistics; the actual BAO data points are more constraining.

**The correct read of the earlier number:** ξ *can produce a w(z) that is consistent with DESI's reported CPL fit*. That is a necessary but not sufficient condition. The sufficient condition is that it fits the actual data points, and this sprint shows it does not — at least not better than ΛCDM.

---

## What this means for the README / primary papers

The §2 claim in README:

> "produces freezing quintessence with w(z) → −1 — a falsifiable dark energy prediction that fits DESI DR2 better than ΛCDM in our preliminary scan (χ² = 3.06 vs 15.3)."

**needs correction**. The proper reading is:

- ξ is falsifiable — PROVED, has been falsified-if on full MCMC.
- ξ reproduces DESI's CPL summary (w₀, wa) to within ~1.7σ — TRUE and restated correctly.
- ξ fits the raw BAO data points better than ΛCDM — **NOT SUPPORTED** by this sprint's analysis.
- ξ fits the raw BAO data points comparably to ΛCDM (Δχ² within ~1–2) — the defensible statement.

Proposed README edit: replace the "χ² = 3.06 vs 15.3" parenthetical with the accurate statement that *on the raw DESI DR1 BAO data, ΛCDM and ξ fit comparably, with ΛCDM mildly preferred (Δχ² = −1.59); the earlier 3.06 compared against CPL summary statistics only*.

---

## Caveats (scope of this result)

This is a **background-level fit**, not publication-grade. Things not included:

1. **r_d via Eisenstein-Hu fitting formula** (good to ~1% in standard models where dark energy is negligible at recombination — true here). A full Boltzmann solver (CAMB / CLASS) would tighten this by ~1% in r_d, which translates to ~1% shifts in best-fit h and Ωm. Not enough to flip the Δχ² verdict.

2. **Only BAO.** No CMB likelihood (Planck 2018), no Type Ia SNe (Pantheon+ / DES-SN5YR), no weak-lensing. A full joint analysis is what DESI+CMB+SN papers do. With Planck CMB added, ΛCDM fit tightens further (matter-density is pinned); ξ might recover some advantage in modeling low-z tension, but that requires the actual joint likelihood.

3. **Massless neutrinos** (Σmν = 0) assumed.

4. **Chain length short.** ΛCDM: 24 walkers × 2000 steps. ξ: 24 walkers × 600 steps. Publication work would use 10× more for posterior convergence; the best-fit χ² is reliable though, since emcee finds the mode quickly.

5. **ξ posterior is poorly behaved.** Acceptance rate = 0.20 (low) and Ωm hit 0.586 / h = 0.484 (unrealistic values far from Planck). This suggests the ξ model is trading matter density for dark-energy behavior to fit the data — which is exactly what model-comparison studies expose. A tighter prior from Planck on (Ωm, h) would pin these down and likely worsen ξ's fit further. The "ξ beats ΛCDM" story does not survive that tightening.

---

## Three honest conclusions

1. **The ξ model is not ruled out by DESI DR1 BAO.** It fits to χ² = 15.7 — worse than ΛCDM's 14.1, but not wildly so. The freezing quintessence behavior is compatible with the data, just not preferred.

2. **The ξ model does not *beat* ΛCDM on DESI BAO alone.** The earlier "χ² = 3.06" was against CPL summary statistics, not raw data. On raw data, ΛCDM is slightly preferred.

3. **To make the cosmological case for ξ, the next analysis needs joint CMB + BAO + SN, with a real Boltzmann solver.** The BAO-only background analysis cannot distinguish the models at a level useful for a JCAP submission. If that joint analysis also favors ΛCDM, the physical-test case for ξ needs to shift from "preferred over ΛCDM" to "consistent with data with a specific falsifiable equation-of-state curve" — which is still a real result, just a different one.

---

## Reproducibility

```bash
cd Gen12/targets/clay/papers/sprint14_prism_xi_2026_04_10/
pip install emcee corner
python desi_xi_mcmc.py
```

Runtime: ~3–4 minutes on a laptop. Chains saved to `desi_xi_mcmc_chains.npz`.

---

## Files in this sprint

- `desi_xi_mcmc.py` — the MCMC script (this result)
- `desi_xi_optimize.py` — the earlier grid search against (w₀, wa)
- `desi_xi_fit.py` — the original forward-model solver
- `DESI_MCMC_RESULTS.md` — this document
- `desi_xi_mcmc_chains.npz` — saved chains (git-ignored if large)

---

*© 2026 Brayden Ross Sanders / 7Site LLC*
*Part of Sprint 14 (PRISM-XI cosmology) closeout with Sprint 17 discipline layered on top.*
