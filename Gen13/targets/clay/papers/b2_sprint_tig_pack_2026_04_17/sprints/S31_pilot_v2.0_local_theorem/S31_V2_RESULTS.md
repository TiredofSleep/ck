# S31 v2 Results — Local Theorem Path Recovery
## S31-pilot-v2.0, Z/10, h_thm = 7

---

## Scope Declaration (Reproduced)

**Path:** Local Theorem
**Attractor convention:** $h_{\text{thm}} = 7$
**Claim class:** theorem-level
**Canonical construction source:** published Z/10 TSML
**Relation to prior sprints:** Inherits B1 (Path 1, ground-truth calibration). Does not inherit any Path 2 sprint. Does not inherit S31-pilot-v1.0 (cross-path error).

---

## Pre-Run Sanity Checks (Both Passed)

- Canonical $C_0(R_{10}, h = 7, \sigma)$ matches the published Z/10 TSML on all 92 non-overlay cells (audit: 92/92).
- The MAX+ADD overlay applied on top of $C_0$ reproduces the full published Z/10 TSML table bit-exactly.

These sanity checks confirm the spec is internally consistent before any data is scored.

---

## Per-Condition Results

| Overlay | $p$ | $\|S_\text{planted}\|$ | $\|S_\text{persistent}\|$ | $\|\cap\|$ | $J$ | $R$ | $P$ | $A$ |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| NONE | 0.02 | 0 | 0 | 0 | 1.0000 | — | 1.0000 | — |
| NONE | 0.10 | 0 | 0 | 0 | 1.0000 | — | 1.0000 | — |
| NONE | 0.20 | 0 | 0 | 0 | 1.0000 | — | 1.0000 | — |
| MAX | 0.02 | 6 | 6 | 6 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| MAX | 0.10 | 6 | 6 | 6 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| MAX | 0.20 | 6 | 6 | 6 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| ADD | 0.02 | 2 | 2 | 2 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| ADD | 0.10 | 2 | 2 | 2 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| ADD | 0.20 | 2 | 2 | 2 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| MAX+ADD | 0.02 | 8 | 8 | 8 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| MAX+ADD | 0.10 | 8 | 8 | 8 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| MAX+ADD | 0.20 | 8 | 8 | 8 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |

**Every planted cell recovered on every seed at every noise level. Zero false positives. Perfect type agreement.**

---

## Observations from the Data

### Recovery is perfect across the entire grid

- All 8 overlay cells in MAX+ADD are recovered at all three noise levels.
- All 6 MAX cells recovered. All 2 ADD cells recovered. None missed.
- Persistence size equals planted size exactly: no spurious cells enter the persistent seam.
- Modal empirical values match planted overlay values at every recovered cell.

### The control (NONE) behaves cleanly

Empty persistent seam at all three noise levels, as expected for a generator that equals $C_0$ exactly. Noise does not generate spurious persistent cells at these parameters.

### Comparison to v1.0

S31-pilot-v1.0 under $h = 9$ produced:
- MAX Jaccard = 0.6667 (4/6 recovered; $(2,9)$ and $(9,2)$ invisible).
- MAX+ADD Jaccard = 0.7500 (6/8 recovered).

S31-pilot-v2.0 under $h = 7$ produces:
- MAX Jaccard = 1.0000 at all noise levels.
- MAX+ADD Jaccard = 1.0000 at all noise levels.

The difference is entirely attributable to the attractor convention. Under $h = 7$, the cells $(2,9)$ and $(9,2)$ have $C_0(x, y) = 7$ while the MAX overlay assigns them value 9 — visible. Under $h = 9$, both $C_0$ and the overlay assigned them value 9 — invisible. This confirms the reconciliation in `ATTRACTOR_RECONCILIATION.md`.

---

## Aggregate Metrics Summary

| Regime | Mean $J$ | Mean $R$ | Mean $P$ | Mean $A$ |
|---|---|---|---|---|
| Clean ($p = 0.02$) across non-NONE overlays | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| Reference ($p = 0.10$) across non-NONE overlays | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| Stress ($p = 0.20$) across non-NONE overlays | 1.0000 | 1.0000 | 1.0000 | 1.0000 |

All thresholds passed with room to spare on $J$, $P$, $A$. All thresholds passed at the ceiling on $R$.

---

## What the Data Shows, Stated Narrowly

Under the frozen spec of S31-pilot-v2.0 (Local Theorem Path, $h_\text{thm} = 7$, $N = 1{,}000$, $K = 10$, $\pi = 0.50$, noise levels $\{0.02, 0.10, 0.20\}$), the extractor recovers the published Z/10 TSML's seam exactly on every condition, with no false positives and perfect type agreement across every noise level tested.

At $N = 1{,}000$ (10 observations per cell on average), the mode operator is robust enough to correctly identify each overlay cell's value against $C_0$'s background, and the persistence filter correctly eliminates any transient noise-driven disagreements.

---

## What This Data Cannot Say

- Nothing about carriers other than Z/10.
- Nothing about Path 2 canonical constructions.
- Nothing about transport of any invariant.
- Nothing about bridge claims between paths.

This is a Path 1 validation result only.

Verdict follows in `S31_V2_VERDICT.md`.
