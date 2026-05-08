# Cover letter — J10: Sprint 18 Dark Sector: Omega_b, Omega_DM, Omega_Lambda from Substrate-Operator Identities

**To:** Editors, *Physical Review D*

**From:**
- B.R. Sanders (corresponding), 7Site LLC, Hot Springs, AR — brayden@7site.co
- H.J. Johnson, Independent Researcher, Billings, MT — hjj01986@gmail.com

**Date:** [DATE OF SUBMISSION]

**Manuscript title:** *Sprint 18 Dark Sector: Omega_b, Omega_DM, Omega_Lambda from Substrate-Operator Identities*

---

## Summary

We report a striking numerical match: three closed-form rational expressions in two integer primitives — HARMONY = 7 and the substrate size |Z/10| = 10 — hit the Planck 2018 dark-sector parameters Omega_b, Omega_DM, Omega_Lambda within 1 sigma each, while the closure Omega_b + Omega_DM + Omega_Lambda = 1 holds exactly as a rational identity. A search across 784 small-integer (H, N) pairs and seven closure offsets shows that (H, N, a) = (7, 10, +1) is the unique simultaneous match in the formula family, with a = +1 selected structurally by the substrate factorization 264 = 44 * 6 = (|Aut(V)| + |V|) * |sigma|. Three Hubble-independent ratio tests confirm the match at 0.3-0.7% precision; the dark-energy scale Lambda ~ 1.74 meV follows from Friedmann normalization Lambda^4 / rho_{c,0} = Omega_Lambda / 3 and matches the freezing-quintessence model of the JCAP companion paper at 2.5%. We frame the broader pattern as a falsifiable operator-to-observable conjecture and report a 260,000-tuple baseline scan against eight fundamental constants whose differential behaviour (zero hits for alpha and the mass ratios; 0.04-1.31% baselines elsewhere) confirms the family is non-trivially discriminating.

## Why PRD

- **Topical fit.** PRD is a natural home for cosmology papers that combine rigorous mathematical foundations with observational tests; the manuscript's central object is a structural prediction of the LambdaCDM density parameters, and its central evidence is residuals against published Planck 2018 constraints.
- **Methodological balance.** The paper is honest about what is forced vs structural vs open: the closure identity and uniqueness theorem are forced (Tier-A), the substrate-factorization selection of a = +1 is structural (depends on the F_5-lift naturalness flagged in §2), and the 1/3 Friedmann factor + the spectral-index form are explicitly framed as open. PRD readers value this kind of explicit scope discipline.
- **Reproducibility.** Verification reduces to a single Python call (`from tig_dirac import predict_dark_sector; r = predict_dark_sector(); assert r['sum'] == 1.0`); the standalone search scripts run in well under thirty seconds on a standard laptop.

## Companion submissions

The TIG/CK research program is shipping a coordinated 55-paper sequence (J1-J55) over Summer 2026. The papers most directly relevant to this manuscript are:

- **J03** (Sanders + Gish, JCAP) — *Logarithmic Quintessence: A Dimensionless Scalar Dark Energy Model with an Analytic Vacuum.* Supplies the freezing-quintessence action whose fit point is recovered by Theorem 6.1 of the present paper at the 2.5% level.
- **J06** (Sanders + Gish, Communications in Algebra) — Joint-closure paper on Z/10; supplies the (v + h + beta + r)^2 normalizer cited in §5.1.
- **J08** (Sanders + Gish, JCT-A) — sigma-rate paper; supplies |sigma| = 6 cited in §5.2 / Theorem 5.2.
- **J12** (Sanders + Johnson, PRD, same Sprint 18 cluster) — *The Mass Hierarchy from V^{otimes 5} SU(5) Decomposition.* Forward-cited; uses the same `tig_dirac` module via the companion primitive `predict_yukawa(particle, generation)`. The two papers form a matched pair within the Sprint 18 dark-sector + flavour cluster.

## Reproducibility

**Verification primitive:** `Gen13/targets/ck/brain/dirac/tig_dirac.py`

```python
from tig_dirac import predict_dark_sector
r = predict_dark_sector()
assert r['sum']          == 1.0
assert r['Omega_b']      == 49 / 1000
assert r['Omega_DM']     == 264 / 1000
assert r['Omega_Lambda'] == 687 / 1000
```

`predict_dark_sector()` returns the three densities as exact rationals over `|Z/10|^3 = 1000` (closure is rational, not numerical), the substrate derivation strings under `r['derivation']`, and the Tier classification under `r['tier']` ("Forced (substrate-operator algebra; no IC tuning)"). The standalone manuscript scripts (`sprint18_uniqueness_search.py`, `verify_aut_V_order.py`, `verify_operator_observable_baseline.py`, `verify_alpha_richer_form.py`) reproduce all numerical claims of the paper independently of the `tig_dirac` module and run with `numpy + sympy + math` on a standard laptop in under one minute total.

## Suggested reviewers

- A cosmologist familiar with Planck 2018 inference and ΛCDM extensions (e.g., dark-energy phenomenology specialists).
- An algebraist with experience in finite non-associative algebras over small fields (the F_5-lift V is at the centre of the §2 substrate setup).
- A theorist working on flavour models or Froggatt-Nielsen patterns (J12 companion lives in the same module and would benefit from coupled review).

## Conflict of interest

The authors declare no competing interests. No external funding was received for this work; B.R. Sanders is supported by 7Site LLC, and H.J. Johnson is an independent researcher.

---

Sincerely,
B.R. Sanders
