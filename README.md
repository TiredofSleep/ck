# funding/desi-xi-cosmology

**Track I — ξ-Field Cosmology + DESI DR2 Fit**
**Primary funder pool:** NSF PHY · Templeton (Mathematical & Physical Sciences) · Simons Foundation · Heising-Simons · Sloan Research Fellowship
**Status:** **Mature.** Sprint 14 PRISM-XI papers complete; JCAP LaTeX bundle (TRACK 7.3) assembled; DESI DR1/DR2 placeholders tightened. Funded deliverable = empirical MCMC numerical fit to DESI DR2.
**Branch accumulates to:** `master` (every commit cherry-picked) · **Rigor base:** `tig-synthesis` (the GitHub default branch)

---

## One-paragraph pitch

Late-time cosmology has an anomaly: DESI DR1 (and the emerging DR2 signal) prefers $w(z)$ evolution over a pure cosmological constant. **The ξ-field cosmology program proposes a specific, exactly-soluble freezing-quintessence candidate** whose only free parameters are $\kappa_\Xi$ (coupling) and the initial ξ field value, with the ground state fixed at $\xi_0 = e^{-1}$ by the logarithmic potential. This is a falsifiable prediction: the ξ model either fits DESI DR2 within the reported uncertainty envelope, or it does not. The mathematical framework is complete: WP81 establishes the canonical action; WP82 audits the novelty against arXiv; WP83/84 audits internal consistency; WP101 provides the σ-rate theorem; `proof_xi_canonical.py` verifies the vacuum numerically. Sprint 14's JCAP LaTeX bundle (TRACK 7.3) is ready to submit. **The proposed work is the 6–12 month MCMC fit against DESI DR2, JCAP publication, and follow-on work on the $\kappa_\Xi$-DES/Euclid cross-check.**

## The canonical action

$$S = \int d^4x\,\sqrt{-g}\left[\frac{R}{16\pi G} + \mathcal{L}_\text{SM} + \kappa_\Xi\!\left(\tfrac{1}{2}g^{\mu\nu}\partial_\mu\Xi\,\partial_\nu\Xi + \Xi\log\Xi\right)\right]$$

Euler–Lagrange: $\Box\xi = 1 + \log\xi$. Exact vacuum: $\xi_0 = e^{-1}$. Mass²: $m_\xi^2 = \kappa_\Xi \cdot e$ on-shell. Late-time departure from ΛCDM shows up in DESI as sub-percent-level $w(z)$ deviation.

## Runnable artifacts

1. **`proof_xi_canonical.py`** — verifies $\Box\xi = 1 + \log\xi$ and $\xi_0 = e^{-1}$ numerically, confirms the EL equation, computes $m^2 = \kappa_\Xi \cdot e$. 22/22 internal tests pass.
2. **`proof_separability_bridge.py`** — Bialynicki-Birula 1976 separability argument that forces the log-nonlinearity uniquely.
3. **`WP81_CANONICAL_XI_THEORY.md`** — canonical action + EL + stress-energy + FRW cosmology + formal/interpretive split.
4. **`WP82_LOG_QUINTESSENCE_NOVELTY.md`** — arXiv literature search for ξ log ξ potentials, novelty report.
5. **`WP83_PRISM_CONSISTENCY_AUDIT.md`** + **`WP84_PRISM_CONSISTENCY_AUDIT_V2.md`** — internal consistency audits.
6. **`WP86_XI_CORE_CANONICAL_FORM.md`** — canonical form + dimensional analysis.
7. **`WP87_CROSS_BRANCH_ANALYSIS.md`** — relationship to TIG / Crossing Lemma / σ framework.
8. **`WP101_SIGMA_RATE_THEOREM.md`** + `proof_sigma_rate.py` — σ(N) ≤ C/N rate theorem (relevant for vacuum-relaxation timescale).
9. **JCAP TRACK 7.3 bundle** — LaTeX source assembled 2026-04-19; submission-ready for JCAP venue 7.
10. **All 20+ Sprint 14 PRISM-XI papers** at `Gen12/targets/clay/papers/sprint14_prism_xi_2026_04_10/`.

## What's in this branch

Branch-specific funder-pitch files under [`Gen13/targets/funding_desi_xi_cosmology/`](Gen13/targets/funding_desi_xi_cosmology/):

- [`README.md`](Gen13/targets/funding_desi_xi_cosmology/README.md) — deep pitch document
- [`FUNDERS.md`](Gen13/targets/funding_desi_xi_cosmology/FUNDERS.md) — prioritized funder list
- [`ARTIFACTS.md`](Gen13/targets/funding_desi_xi_cosmology/ARTIFACTS.md) — proof scripts + papers + LaTeX bundle
- [`PITCH_DRAFT.md`](Gen13/targets/funding_desi_xi_cosmology/PITCH_DRAFT.md) — full pitch draft
- [`LIMITATIONS.md`](Gen13/targets/funding_desi_xi_cosmology/LIMITATIONS.md) — honest-scope items (requires MCMC-infrastructure collaborator)
- [`STATUS.md`](Gen13/targets/funding_desi_xi_cosmology/STATUS.md) — readiness checklist

## Ask sizes

| Phase | Scope | Ask |
|---|---|---|
| **Phase 1 — DESI DR2 MCMC fit** | Joint BAO + CMB + SN likelihood; $\kappa_\Xi$ posterior; published comparison to ΛCDM | $60K–$180K, 6–12 months |
| **Phase 2 — JCAP submission + Euclid/DES cross-check** | JCAP-submission manuscript + cross-survey consistency | $100K–$200K, 6 months |

## The project this branch is a track of

Branch I of the 10-branch funding architecture. For the full project overview, see **`tig-synthesis`**:

→ https://github.com/TiredofSleep/ck/tree/tig-synthesis

## License

7Site Public Sovereignty License v1.0 — human use only, no commercial, no military, free forever. Full text in [`LICENSE`](LICENSE).

---

*Branch maintained as part of the 10-branch funding architecture. Commits here get cherry-picked to master per the trunk workflow. Branch-level changes do not propagate to `tig-synthesis` unless they are referee-ready.*
