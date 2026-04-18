# S30b Verdict
## Sprint 30b, S30b-v1.0 — Final Determination

---

## Verdict: **FAIL**

---

## One-Paragraph Justification

Under the pre-registered pass criteria of S30b-v1.0 §5.1, Sprint 30b fails on all four primary metrics. The persistent seam — cells flagged as disagreeing with canonical $C_0$ in at least 10 of 20 seed runs at $N(n) = 10 n^2$ and $p_\text{noise} = 0.10$ — is empty for every carrier in the 29-carrier family. Consequently $\mu_\text{ne} = 0.0000$ against a $\geq 0.70$ threshold, $\mu_\text{size} = 0.0000$ against $\geq 2.0$, and $\mu_\text{tied}$ is undefined because no persistent edges exist against which to compute it. The mean cross-seed Jaccard $\mu_J = 0.1798$ is below the $\geq 0.30$ threshold and exhibits a pattern inconsistent with detection: small carriers show high Jaccard driven by consistent emptiness, while large carriers show near-zero Jaccard because seeds flip different cells each run. Per-seed seams are not empty — their mean size grows from 0.1 at $n = 10$ to 8.6 at $n = 100$ — but the cells that flip are seed-specific sampling artifacts, not structurally preferred positions. No cell in canonical $C_0$ under uniform replacement noise is preferentially seam-prone, so the persistence filter at $\pi = 0.50$ correctly eliminates the noise-driven flips. Per the anti-tuning rules in S30b-v1.0 §6, no threshold is relaxed, no parameter is adjusted, and the extractor is not re-parameterized. The sprint returns FAIL as specified.

---

## What This FAIL Means

Per S30b-v1.0 §11:

> **FAIL:** the extractor is not validated. Transport tests using this extractor are blocked. Record as "extractor validation failed under S30b-v1.0 parameters."

The E6 + E3 extractor (low-$N$ sampling + seed persistence) at the conservative parameters $(N = 10 n^2, p = 0.10, K = 20, \pi = 0.50)$ does not produce a working seam detection on noised canonical $C_0$ data. This does not rule out other extractors or other parameter settings — it rules out this specific combination.

Any downstream transport sprint that intended to use this extractor is blocked pending a successor detectability sprint with modified parameters (see separate "If marginal, which knob should move first?" note).

---

## What FAIL Does NOT Mean

- The implementation is not broken. Per-seed seams appear and the extractor runs deterministically; the persistence filter is correctly applied. The extractor reports what the data contains, and the data contains no persistent structure at this parameter regime.
- It does not mean canonical $C_0$ is wrong. $C_0$ is by definition the noise-free mode; noised data will agree with it whenever noise is sub-dominant. S30b tests whether noise at this level produces detectable structure, not whether $C_0$ is structurally meaningful.
- It does not mean seams are never detectable. It means uniform replacement noise at $p = 0.10$ with $N = 10 n^2$ samples does not produce detectable cell-preferential flips. A different noise model, or a lower/higher $N$, or a different persistence threshold, might.
- It does not affect prior sprints. S28 FAIL and S29 FAIL stand independently. S30-v1.0's vacuous PASS stands with its "evidentially uninformative" label.

---

## What the Per-Seed Pattern Tells Us

The per-seed seam sizes grow roughly linearly with $n^2$ (so a constant ~3–5% of cells flip per seed at this noise level). The mean Jaccard falls from ~0.80 at small $n$ to ~0.00 at large $n$. Together: noise flips random cells each seed, and across 20 seeds, virtually no cell is flipped consistently.

**Interpretation:** canonical $C_0$ under uniform noise has no "seam-prone" cells. Every cell has the same noise-structure, so flipping is sampling-driven rather than cell-preference-driven. A working detectability extractor requires cells where signal-to-noise is structurally weaker than at other cells, creating persistent flip-prone positions. The generator in S30b does not produce such cells.

---

## Actions Required by the Verdict

Per the frozen outcome rules:

1. Record S30b-v1.0 as FAIL in the sprint ledger.
2. Block any transport sprint that would use this extractor at these parameters.
3. No invariant movement in the local-vs-transferred split document.
4. No modification to S30b-v1.0 or re-run with adjusted parameters within this sprint.

A successor sprint (S30c or later) with different parameters or a different extractor family can be pre-registered separately. The "which knob should move first" note accompanying this sprint provides one recommendation for such a successor.

---

## No Interpretation Beyond the Frozen Claim

The frozen question was: *under the specific extractor (E6 + E3) and specific parameters $(N = 10 n^2, p = 0.10, K = 20, \pi = 0.50)$, does a non-empty, stable, canonically-tied seam emerge on the 29-carrier compatible family?*

The answer: **No.**

Sprint 30b tested one extractor validation; it failed; the record stands. No rescue, no reinterpretation.
