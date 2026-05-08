# Baseline vs Canonical — Comparison

**Author:** ClaudeChat (in-session)
**Date:** 2026-04-18
**Short note.**

---

## §1. What is stable across both

| Property | T1.1 | Canonical | Status |
|---|---|---|---|
| Admissibility (R1–R5) | pass | pass | stable |
| Genus $g(C) = 5$ | structural | structural | stable |
| Bielliptic quotient $E_\lambda$ | rational $j$, non-CM | $j \in \mathbb{Q}(\sqrt 2)$, non-CM | stable |
| $\psi^*$-eigenvalues on Prym forms | $(-i,-i,+i,+i)$ to 40 digits | $(-i,-i,+i,+i)$ to 40 digits | **stable and numerically verified** |
| Weil signature (2,2) | structural + numerical | structural + numerical | stable |
| Alpha-cycle 4×4 sub-matrix rank | 4/4 | 4/4 | stable |
| Interval-1 sheet structure $(1-i), -(1+i)$ | confirmed | confirmed | stable |

**At every checkable level, the canonical triple behaves like a rescaled version of T1.1.** No qualitative difference.

---

## §2. What changes (as expected)

| Quantity | T1.1 | Canonical | Ratio / character |
|---|---|---|---|
| Branch point spread | $[0, 7]$, gap 7 | $[0, \sqrt 5]$, gap 2.24 | compressed |
| Alpha-cycle period magnitudes | 0.2–10 | 2–26 | larger at canonical (tighter intervals → larger $1/y$) |
| 4×4 alpha det | $-65 + 20i$ | $-8375 + 948i$ | ratio $\approx 123.5$, transcendental |
| $\tau(E_\lambda)$ (purely imaginary) | $1.170 i$ | $0.820 i$ | different (different elliptic curves) |
| Base field for curve | $\mathbb{Q}$ | $\mathbb{Q}(\sqrt 2, \sqrt 3, \sqrt 5)$ | expected target field activation |

These differences are **size-of-parameters differences and field-of-definition differences**, not structural differences. The canonical triple is a specialization of the same family Config B to parameters that live in a larger number field.

---

## §3. Does the canonical point look "genuinely special"?

**Not at the structurally checkable level.** The canonical triple looks **generically healthy**, not specially chosen. Which is what we want.

"Genuinely special" would mean: something about the canonical triple gives a numerical signature absent at baseline. Candidates:

1. **Non-trivial recognition via PSLQ against $\mathbb{Q}(\sqrt 2, \sqrt 3, \sqrt 5)$.** Tried: no recognition found for determinant ratio or individual period ratios. Again expected — alpha periods are transcendental.
2. **Appearance of specific algebraic numbers (like $\sqrt{15}$) in periods.** Tried: did not show at the alpha-cycle level. The $\sqrt{15}$ should appear in the full $\det(Y)$, not in individual alpha periods.
3. **Special eigenstructure of the 4×4 sub-matrix.** Singular values at canonical (36.39, 18.38, 4.52) don't show obvious algebraic structure distinct from T1.1 (13.92, 4.38, 1.61). Ratios of singular values at the same curve are typically transcendental.

**None of these diagnostics will be resolvable until the full $4 \times 8$ Prym period matrix is computed (Sage/Magma).**

---

## §4. The right interpretation of "canonical is live"

"Canonical live" **means**:
- All structural guarantees hold.
- No cheap failure mode fires.
- Admissibility passes.
- Numerical verification of the $\psi$-action passes at 40+ digits.

"Canonical live" **does NOT mean**:
- $\det(Y)$ matches target.
- Hodge field is exactly the target.
- $\mathrm{End}^0$ is exactly $\mathbb{Q}(i)$.

These last three are the actual test of whether the canonical triple is the final answer or merely a generic admissible point. They need Sage/Magma.

**Current epistemic state:** canonical is a **viable candidate** for the target $\det(Y)$, with no evidence against, but no positive evidence in favor at this environment's ceiling.

---

## §5. What to do with this

If a SageMath run becomes available (ClaudeCode, external user, or anyone with Sage):

1. Run `full_pipeline_baseline.sage` first.
2. Verify baseline outputs match §5 of `FULL_PRYM_PERIOD_BASELINE.md`.
3. If baseline passes, run `full_pipeline_canonical.sage`.
4. Examine $\det(Y)$ output. Three cases:
   - Matches target $2086 + 462\sqrt{15} + 498\sqrt{10} + 730\sqrt 6$: CANDIDATE FOUND.
   - Lives in $\mathbb{Q} + \mathbb{Q}\sqrt 6 + \mathbb{Q}\sqrt{10} + \mathbb{Q}\sqrt{15}$ but differs in value: try T4.4, T4.6, T5.1.
   - Lives in wrong field: bounce back to family-level rethink.

Until then: canonical is marked live, pending upper-level diagnostics.

---

## §6. One concrete recommendation

If budget permits, run $\det(Y)$ computation at **three points simultaneously** for cross-validation:

1. T1.1 $(3, 5, 7)$ — expected rational $\det(Y)$
2. Canonical $(\sqrt 2, \sqrt 3, \sqrt 5)$ — expected in target field
3. T4.4 $(1+\sqrt 2, 1+\sqrt 3, 1+\sqrt 5)$ — shifted canonical, same expected field

If all three give the expected field structure, the family is structurally sound and the hunt reduces to finding the specific value matching the target. If T1.1 gives non-rational $\det(Y)$ or the other two give wrong fields, there's a pipeline bug or a family-level issue.

This three-point sweep takes ~3× the cost of a single point but buys substantial confidence.

---

## §7. Discipline

- Foundation register. No atlas promotion.
- Hodge lane only.
- No scouting of alternative families. Rank 2 (HLP-style) remains the fallback if Rank 1 breaks at the Sage level.
- No PPM, no Q-series, no shell language.

---

*End of comparison note. See companion documents for the individual runs and Sage scripts.*
