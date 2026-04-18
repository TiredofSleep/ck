# What Counts as a Good $C_*$
## Short checklist for evaluating candidate Beauville curves

**Author:** ClaudeChat (foundation side)
**Date:** 2026-04-18
**Companion to:** `HODGE_CSTAR_TARGET_NOTE.md` (conceptual version)
**Use:** when a candidate family comes back from the scout, run through this checklist.

---

## Checklist

| # | Criterion | Pass | Fail |
|---|---|---|---|
| 1 | **Genus** | $g(C_*) = 5$ | $g \neq 5$ |
| 2 | **Quotient structure** | Has involution $\iota$ with $C_*/\iota = E$ elliptic (degree-2 map to genus-1) | No such quotient, or quotient is not elliptic |
| 3 | **Prym dimension** | $\dim \mathrm{Prym}(C_*/\iota) = 4$ | $\neq 4$ |
| 4 | **Order-4 automorphism** | $\exists \psi: C_* \to C_*$ order 4 with $\psi^2 = \iota$ | Only involution, no order-4 structure |
| 5 | **Endomorphism equality** | $\mathrm{End}^0(\mathrm{Prym}) = \mathbb{Q}(i)$ exactly | Strictly larger (full CM) or strictly smaller (just $\mathbb{Z}$) |
| 6 | **Weil signature** | $(2, 2)$ on $\mathrm{Lie}(\mathrm{Prym}) \otimes \mathbb{C}$ under $\mathbb{Q}(i)$-action | $(4,0), (3,1), (1,3), (0,4)$, or non-Weil |
| 7 | **Prym polarization type** | Principal (type $(1,1,1,1)$) | Non-principal (e.g., $(1,1,1,2)$) |
| 8 | **Hodge field** | $\mathbb{Q}(i, \sqrt{2}, \sqrt{3}, \sqrt{5})$, degree exactly 16 | Smaller or larger |
| 9 | **Descent field** | Definable over $\mathbb{Q}(\sqrt{2}, \sqrt{3}, \sqrt{5})$ | Only over a larger extension |
| 10 | **Riemann form det** | $\det(Y) = 2086 + 462\sqrt{15} + 498\sqrt{10} + 730\sqrt{6}$ exact | Different value |
| 11 | **Explicit equations** | Polynomial equations with coefficients in the descent field | Only moduli point, no equations |
| 12 | **BSD usefulness** | $L(J(C_*), s)$ factors through $L(A_*, s)$ compatibly | No compatible factorization |

---

## Order of checking (fastest elimination first)

1. **Genus** (#1) — trivial to check from equation or genus formula
2. **Quotient structure** (#2) — visible from automorphism group
3. **Order-4 automorphism** (#4) — visible from automorphism group
4. **Prym dimension** (#3) — follows from 1 and 2 by Riemann-Hurwitz
5. **Descent field** (#9) — check coefficients of equations
6. **Explicit equations** (#11) — either available in literature or not
7. **Polarization type** (#7) — compute via Beauville's Prym formula
8. **Endomorphism equality** (#5) — more work, requires computing $\mathrm{End}^0$
9. **Weil signature** (#6) — requires period-matrix computation
10. **Hodge field** (#8) — requires period-integral analysis
11. **Riemann form det** (#10) — requires full exact period-matrix computation
12. **BSD usefulness** (#12) — final check, requires Beauville synthesis to go through

---

## Notes

- A candidate passing all 12 is a full match.
- Criteria 1–4 are "topological" (visible from curve structure).
- Criteria 5–8 are "Hodge-theoretic" (require period analysis).
- Criteria 9–11 are "arithmetic" (require field/form computation).
- Criterion 12 is "output" (requires Beauville application).
- Failing criterion 9 (descent) is the most common silent killer per the target note.

---

*© 2026 Brayden Ross Sanders / 7Site LLC. 7Site Human Use License v1.0. DOI: 10.5281/zenodo.18852047.*
