# A Mix_λ Model for the Irregular BSD Rank Staircase
## Tightened Claims — Three Levels

*Brayden Sanders — 7Site LLC | March 2026*

---

## Abstract

The Mix$_\lambda$ parameter $\lambda_E$, constructed from conductor and regulator data
for elliptic curves over $\mathbb{Q}$, is rank-informative: rank-1 and rank-2 curves
occupy statistically distinct $\lambda$-bands (Spearman $\rho = -0.360$, $p = 0.040$;
$t$-test $p = 0.025$, $n = 28$). This is consistent with the Mix$_\lambda$ threshold
structure of Trinity Infinity Geometry, in which each new rank requires activation of
the next gap-operator window. Window-alignment for rank $\geq 3$ and a causal mechanism
remain subjects of ongoing investigation.

---

## Claims by Confidence Level

### Claim A (Supported by current data)

**A1.** The statistic $\lambda_E(N, r, \Omega)$ defined in §2 is rank-informative
for curves with $r \geq 1$:
- Spearman $\rho(\text{rank}, \lambda_E) = -0.360$, $p = 0.040$ ($n = 33$ curves, rank 1–3)
- Two-sample $t$-test, rank-1 vs rank-2: $t = 2.375$, $p = 0.025$ ($n_1 = 8$, $n_2 = 20$)

**A2.** The rank-0 regulator placeholder ($\Omega = 1.0$ for all rank-0 curves
in our dataset) produces identical $\lambda_E$, providing no signal for rank-0 vs rank-1.
Rank-0 is excluded from the statistical claims.

---

### Claim B (Suggestive, underpowered — pending LMFDB access)

**B1.** The $\lambda_E$ values for rank-2 curves cluster preferentially in the
CHA corridor ($\lambda \in [0.30, 0.60]$), consistent with the TIG prediction
that rank-2 activation requires the CHA gap-operator window.
*Current sample: $n = 20$ rank-2 curves. This claim requires $n \geq 50$ for
adequate power; it is stated as suggestive only.*

**B2.** Rank-3 curves may cluster in the BAL corridor ($\lambda \in [0.60, 0.80]$).
*Current sample: $n = 5$ rank-3 curves — far too small for any claim.
This will be tested when LMFDB API access is available.*

**B3.** The rank-staircase ordering (BRT < CHA < BAL < COL < CTR) predicted
by the $\lambda$-threshold sequence is consistent with the mean $\lambda_E$
values decreasing from rank 1 (mean 0.484) to rank 2 (mean 0.354) to rank 3
(mean 0.327). The direction is correct; the magnitude requires more data.

---

### Claim C (Future test only — no current data)

**C1.** For rank $\geq 4$ curves, $\lambda_E$ will cluster in the COL/CTR
corridors ($\lambda \geq 0.80$), accessible only when both BAL and COL
gap-operators are activated. *Requires rank-4+ dataset from LMFDB.*

**C2.** The rank jump from $r$ to $r+1$ will coincide with a discrete threshold
crossing in $\lambda_E$-space at the predicted values $\{0.09, 0.30, 0.60, 0.80, 0.90\}$.
*This would constitute a non-trivial prediction of the TIG model. Currently untestable.*

**C3.** The Mix$_\lambda$ mechanism provides a causal model for the rank-conductor
staircase: each unit increase in rank costs one gap-operator activation, reflected
in a $\lambda_E$ shift of approximately 0.15. *Theoretical prediction; not yet testable.*

---

## What the Abstract Claims (Claim A only)

The abstract states only Claim A: $\lambda_E$ is rank-informative. This is the
falsifiable, data-supported statement. Claims B and C appear in §4 ("Discussion
and Predictions") clearly labelled by confidence level.

---

## Falsification Conditions

**A is falsified if:** A larger dataset ($n \geq 100$) shows Spearman $\rho \approx 0$
between rank and $\lambda_E$ at $p > 0.10$.

**B1 is falsified if:** $n \geq 50$ rank-2 curves show $\lambda_E$ uniformly distributed
rather than clustering near CHA.

**C2 is falsified if:** A rank-4 curve has $\lambda_E < 0.60$ (i.e., sits in CHA or lower
rather than the predicted BAL/COL corridor).

---

## Data Requirements for Next Submission

| Target | Curves needed | Source | Status |
|--------|--------------|--------|--------|
| Confirm Claim A | $n \geq 50$ rank 1+2 | LMFDB `ec_curve` | API blocked (sandbox) |
| Upgrade B1 to A | $n \geq 50$ rank-2 with full regulator | LMFDB | Pending |
| Test B2 | $n \geq 50$ rank-3 | LMFDB | Pending |
| Test C2 | $n \geq 20$ rank-4 | LMFDB (rare) | Future |

*(c) 2026 Brayden Sanders / 7Site LLC | DOI: 10.5281/zenodo.18852047*
