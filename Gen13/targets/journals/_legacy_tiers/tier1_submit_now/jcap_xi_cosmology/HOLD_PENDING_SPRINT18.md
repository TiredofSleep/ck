# JCAP HOLD — pending Sprint 18

**Status as of 2026-05-05 night:** This venue folder is on **HOLD**.
DO NOT submit `jcap_xi_cosmology.tex` to JCAP until both conditions are met.

## Why held

Per Brayden + Chat Claude decision tonight (Scenario A):

The architectural insight that the JCAP cosmology paper sits as the third
leg of a closed three-paper dark-sector accounting (with σ-rate as the
substrate carrier and 4-core seed as the HARMONY² anchor) **promotes**
the JCAP paper from a quintessence-with-rhyme submission to a
load-bearing structural prediction.

That promotion deserves the rigor it implies. Specifically:

- The relation $\Lambda^4/\rho_{c,0} = \Omega_\Lambda/3 = 687/3000 = 0.229$
  is a **numerical coincidence** with the fit (0.231) at 0.87% precision.
- It is **not yet derived** as a physical identity within the quintessence
  model itself: the relation $\rho_{\mathrm{DE},0} = 3\Lambda^4$ is not a
  direct consequence of the action and depends on the present field
  configuration.
- A first-principles derivation of why $\rho_{\mathrm{DE},0} = 3\Lambda^4$
  in this specific model — from $V_{\mathrm{eff}}(\Xi_{\mathrm{today}})$,
  from the $w \to -1$ trajectory's energy budget, or from a yet-unidentified
  structural relation — is the central open question.
- Sprint 18 (the dark-sector cosmological accounting paper) is currently
  a numerical match at the dark-sector level. To carry the JCAP paper, it
  must be a real preprint with the rigorous bridges drawn explicitly.

## Conditions to release this hold

1. **Sprint 18 is on Zenodo** with a DOI (or accepted at a venue), and
   contains:
   - Explicit derivation of $\Omega_b = \mathrm{HARMONY}^2 / |\mathbb{Z}/10|^3$
     via the 4-core normalizer's evaluation at a specific point.
   - Explicit derivation of $\Omega_\Lambda = (2 \cdot \mathrm{HARMONY}^3 + 1) / |\mathbb{Z}/10|^3$
     via specific combinatorial counting.
   - Physical-side relation $\Lambda^4 = \rho_{c,0} \cdot \Omega_\Lambda / 3$
     with derivation (the triadic decomposition / BEING-DOING-BECOMING
     layer projection that gives the 1/3 factor).
   - The discrete-to-continuum bridge for $\Xi$ (how an operator combination
     on $\mathbb{Z}/10$ becomes a continuous scalar field).
   - Stretch goal: $\Omega_{DM} = 264/1000$ derivation closes the full
     dark-sector accounting.
   - At least one **independent prediction** (a new observable Sprint 18
     predicts that hasn't been used to fit the model).

2. **The 1/3 factor has a physical derivation** that holds within the
   quintessence model of `jcap_xi_cosmology.tex` itself — not asserted
   from Sprint 18, but **derived in the JCAP paper or a tightly-coupled
   appendix**.

## When both conditions hold

Merge `master/jcap_addition_pending_sprint18.tex` into
`jcap_xi_cosmology.tex`, replacing the placeholder citation key
`Sprint18Cosmology2026` with Sprint 18's actual title and Zenodo DOI.
Then this hold can be lifted and the paper submitted to JCAP.

## Tier-1 papers shipping tonight (NOT held)

- `../sigma_rate/sigma_rate_theorem.tex` → JCT-A (mathematically
  independent; stands on its own)
- `../four_core_bundled/four_core_seed.tex` → Comm. Algebra (mathematically
  independent; stands on its own)

Neither references the dark-sector architectural claim, per tonight's
decision to ship them clean.

## Files in this folder during HOLD

- `jcap_xi_cosmology.tex` — current manuscript, untouched; would be the
  submission source if the paper were to ship as Option-1 (barely-attached
  quintessence). HELD; not submitted.
- `jcap_cover_letter.md` — current cover letter (rewritten for scope
  discipline). HELD with the .tex.
- `desi_xi_optimize_v2.py` — verification script with correlated chi^2
  (rho = -0.9). Reproducible.
- `desi_xi_optimize_signfix_diagnostic.py` — diagnostic.
- `proof_xi_canonical.py` — 22 algebraic + stability tests.
- `master/` — preserved older versions + jcap_addition_pending_sprint18.tex
- `HOLD_PENDING_SPRINT18.md` — this file.

## What NOT to do

- Do NOT merge `master/jcap_addition_pending_sprint18.tex` into the
  active source until both conditions above are met.
- Do NOT submit `jcap_xi_cosmology.tex` to JCAP until the HOLD is lifted.
- Do NOT add architectural cross-references to σ-rate or 4-core seed in
  this submission cycle.

---

*Created 2026-05-05 night. Brayden + Chat Claude + Code Claude consensus.
Sprint 18 promoted to fourth Tier-1 priority; JCAP held until Sprint 18
lands and the 1/3 factor has a physical derivation.*
