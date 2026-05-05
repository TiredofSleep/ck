# Cover Letter — JCAP Submission

**To:** Editors, Journal of Cosmology and Astroparticle Physics

**From:** B. R. Sanders (corresponding author)
7Site LLC, Hot Springs, Arkansas, USA
brayden@7site.co

**Date:** [DATE OF SUBMISSION]

**Manuscript title:** Logarithmic Quintessence: A Dimensionless Scalar
Dark Energy Model with an Analytic Vacuum

**Co-authors:** M. Gish (Independent Researcher, Hot Springs, AR);
H. J. Johnson ([CONFIRM AFFILIATION: Independent Researcher / MSU
Billings])

---

## Summary

We submit for consideration in JCAP a single-field quintessence model
defined by the potential $V(\Xi) = \Lambda^{4}\,\Xi\log\Xi$ acting on a
real, positive, dimensionless scalar field $\Xi$. The minimal action
\eqref{eq:action} has two parameters ($\Lambda$ and an initial-condition
choice $\Xi_i$ on the freezing branch) and the following features:

- **An exact analytic vacuum at $\Xi_0 = e^{-1}$**, derivable in three
  lines from the Euler-Lagrange equation and independent of $\Lambda$.
  This is the central novelty of the model.
- **Stable massive fluctuations** $m_\Xi^{2} = \Lambda^{4} e / M_\Pl^{2}$,
  with $\Lambda$ numerically near the dark-energy scale ($\Lambda \approx
  1.7$ meV) when $m_\Xi \sim H_0$. We do *not* claim this fixes the
  cosmological-constant scale from first principles; it is a
  consistency observation.
- **Freezing-quintessence dynamics**: on the physical rolling branch
  studied numerically, $w_\Xi(z)$ is monotone with $w_\Xi(z) \to -1$ at
  the vacuum. The fitted trajectory shows $w_\Xi(z) \geq -1$ at all
  redshifts; we do not claim a global no-phantom-crossing theorem.
- **An illustrative consistency check** against the published DESI~2024
  DR1 $(w_0, w_a)$ marginal Gaussian summary on the CPL parametrization.
  Under that Gaussian-on-summary approximation (which is *not* the joint
  BAO + CMB + SN likelihood; we are explicit about this), the model's
  output sits within $\sim 1\sigma$ of the DESI DR1 central values for
  $\Lambda \approx 1.7$ meV and the documented initial conditions. A
  full joint-likelihood analysis using the DR2 chains together with
  Pantheon+ supernovae and Planck CMB constraints is in preparation as
  a companion numerical paper and is explicitly deferred from the
  present submission.
- **Three falsifiable Stage-IV predictions**: monotone freezing $w(z)$,
  asymptotic limit $w \to -1$, and a structured two-parameter $w(z)$
  profile testable at Stage-IV precision. Falsification criteria are
  stated in §6.3.
- **No observable fifth force** in the minimal theory: $\Xi$ has no
  direct matter coupling and any effective coupling is gravitational
  in strength.

The functional form $\Xi\log\Xi$ coincides with the per-bin Gibbs
integrand on a normalized probability distribution and with the
Bialynicki-Birula--Mycielski nonlinearity in nonlinear quantum
mechanics. We treat both connections as **structural rhymes** providing
*motivation* for studying this potential, not as *derivations* of it;
the manuscript's empirical predictions do not depend on either
connection. We are explicit about this in §5.

## Why JCAP

The model addresses two motivations standard for JCAP papers:

(i) It provides a structurally narrow alternative to the cosmological
constant: a single dimensionless scalar with one mass scale $\Lambda$,
analytic vacuum at $\Xi_0 = e^{-1}$, and freezing trajectory ending at
$w \to -1$.

(ii) The model is falsifiable at Stage-IV precision via three concrete
predictions (§6.3), distinguishing it from $\Lambda$CDM and from
phantom or non-monotone dynamical models. The primary observational
tests are extensions of existing DESI / Euclid / Roman pipelines.

## Scope discipline

The manuscript draws its scope before its claims. We explicitly do
*not* claim:

- A full joint-likelihood analysis of DESI BAO + CMB + Pantheon+ SNe;
  this is deferred to a companion numerical paper.
- Derivation of $\Lambda$ from a microphysical substrate.
- Identification of $\Xi$ with a probability density (the Gibbs
  connection is structural, not operational).
- Uniqueness of $V \propto \Xi\log\Xi$ under cosmological hypotheses
  (the BBM nonlinear-quantum-mechanics uniqueness is cited as
  motivation, not proof).
- UV control over the transplanckian field excursion; this is an open
  question shared with most freezing-quintessence constructions.

## Companion submissions

Two companion mathematical-foundations papers, with overlapping
authorship, are submitted simultaneously to other venues and cited as
preprints in the bibliography:

- "Non-Associativity Decay in Binary Composition Tables over Z/NZ"
  (submitted to Journal of Combinatorial Theory, Series A)
- "Joint Closure of Two Commutative Binary Operations on Z/10Z"
  (submitted to Algebraic Combinatorics)

These are independent results; the JCAP paper does not depend on
them. The cross-references exist for readers interested in the
broader foundational program. All three share Zenodo DOI
10.5281/zenodo.18852047.

## Reproducibility

All numerical results are reproducible from the script
`desi_xi_optimize_v2.py` provided in the supplementary material. The
script uses the published DESI DR1 $(w_0, w_a)$ marginal Gaussian
summary including the reported correlation coefficient. The
verification script `proof_xi_canonical.py` runs 22 algebraic and
stability tests on the field equations; all pass. Both scripts run
in under one minute on standard hardware.

## Suggested reviewers

[BRAYDEN: please add 2-3 names of cosmologists working on quintessence
or dark-energy parameterization; e.g., one DESI / Euclid phenomenology
lead, one theorist working on scalar-field dark energy, one researcher
familiar with the Bialynicki-Birula--Mycielski nonlinear-Schrödinger
literature.]

## Conflict of interest

The authors declare no competing interests. No funding was received
for this work.

---

Thank you for considering the manuscript.

Sincerely,
B. R. Sanders
