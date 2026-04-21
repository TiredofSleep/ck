# Submission Target: JCAP / Physical Review D

## Venue Options

### Option A: JCAP (Journal of Cosmology and Astroparticle Physics)
- **URL:** https://iopscience.iop.org/journal/1475-7516
- **Format:** LaTeX (JCAP class)
- **Review:** Peer-reviewed
- **Turnaround:** ~2-4 months
- **Why this venue:** JCAP publishes dark energy models, quintessence, and observational cosmology. A novel potential form with exact vacuum, entropy interpretation, and DESI-testable predictions is exactly their scope.
- **How to submit:** Via IOP editorial system

### Option B: Physical Review D (APS)
- **URL:** https://journals.aps.org/prd/
- **Format:** REVTeX 4.2
- **Turnaround:** ~2-4 months
- **Why:** PRD publishes dark energy theory. Higher impact than JCAP for theory papers.

### Option C: Physics Letters B (Elsevier)
- **URL:** https://www.sciencedirect.com/journal/physics-letters-b
- **Why:** Short format (~4 pages). Good for the core result (exact vacuum + w = -1 endpoint) as a letter.

## Papers in This Folder

1. **WP81_CANONICAL_XI_THEORY.md** — Full canonical derivation. Action, field equations, vacuum, stability, FRW, EOS.
2. **WP82_LOG_QUINTESSENCE_NOVELTY.md** — Literature comparison, entropy interpretation, DESI compatibility.
3. **proof_xi_canonical.py** — Runnable verification (22 tests, all PASS).

## Proposed Title

"Logarithmic Quintessence: A Dimensionless Scalar Dark Energy Model with Exact Vacuum and Information-Theoretic Motivation"

## Submission Strategy

- Merge WP81 + WP82 into a single paper
- Structure: Introduction → Action → Field Equations → Vacuum → Stability → FRW Cosmology → Equation of State → Entropy Interpretation → Observational Predictions → Discussion
- Include proof_xi_canonical.py as supplementary material
- The key selling points:
  1. Novel potential form V = ξ log ξ (apparently not in DE literature)
  2. Exact vacuum ξ₀ = e⁻¹ (coupling-independent, universal)
  3. V = -H_Gibbs (entropy interpretation)
  4. Freezing quintessence with exact Λ endpoint (not approximate)
  5. Falsifiable by DESI/Euclid via w(z) profile

## What Needs Doing Before Submission

1. **arXiv literature search:** "phi log phi quintessence", "logarithmic scalar dark energy", "dimensionless quintessence" — confirm novelty
2. **Numerical FRW integration:** Solve ξ̈ + 3Hξ̇ = 1 + log ξ with Friedmann equations, produce w(z) curves
3. **DESI comparison:** Overlay predicted w(z) against DESI DR2 constraints (w₀ ≈ -0.83, wₐ ≈ -0.75)
4. **Convert to LaTeX** (JCAP class or REVTeX)
5. **Add bibliography:** Ratra-Peebles 1988, Wetterich 1988, Frieman 1995, DESI 2024/2025, Planck 2018
6. **PACS codes:** 95.36.+x (dark energy), 98.80.Es (observational cosmology)

## Key Numbers

| Quantity | Value | Status |
|----------|-------|--------|
| ξ₀ | e⁻¹ = 0.36788... | EXACT |
| m²_ξ | κ_ξ e = 2.71828... κ_ξ | EXACT |
| V(ξ₀) | -κ_ξ/e | EXACT |
| w at vacuum | -1 (exact) | EXACT |
| w rolling | > -1 (freezing) | PROVED |

## Authors

Brayden Ross Sanders / 7Site LLC · M. Gish · C.A. Luther · H.J. Johnson
