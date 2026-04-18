# S28 Verdict
## Sprint 28, S28-v1.0 — Final Determination

---

## Verdict: **FAIL**

---

## One-Paragraph Justification

Under the pre-registered pass criteria of S28-v1.0 §5.1, Sprint 28 fails. Three of the five sub-conditions pass unambiguously: the attractor rule "max odd unit of $U(n)$" matches on every one of the 29 carriers ($A = 1.0$); every carrier's basin ratio $\beta(R_n)$ lies in the pre-specified band [0.60, 0.95] ($B_\text{band} = 1.0$); the mean adjacent-carrier step in $\beta$ is 0.056, below the 0.10 cap ($C_\text{smooth}$ within threshold); and the real attractor rule exceeds the null by an advantage of 0.9769, well above the 0.40 requirement. The fourth condition fails: the pre-registration (§5.1 condition 4) requires real $C_\text{smooth}$ to be at least 3σ **below** the null mean — i.e., smoother than random — and the measured value is 3.35σ **above** the null mean, meaning the real canonical curve is rougher, not smoother, than the scrambled-ring null. This is not a marginal miss; the sign is reversed from what the frozen spec required. The pre-registered FAIL trigger in §5.2 ("the sprint fails if $C_\text{smooth}$ is within 3 std devs of the null mean") fires. Per the anti-tuning rules in §6, the threshold is not adjusted, the null model is not modified, and no alternative interpretation is substituted. The sprint returns FAIL as specified.

---

## What This FAIL Means (Per S28-v1.0 §8)

From the frozen outcome interpretation:

> **Outcome 2: FAIL.** The invariant does NOT transport under this deformation family. It is demoted to "Z/10-local," and the `INVARIANTS_BEYOND_TSML.md` entry for "attractor emerges as structural position" is moved to the left column of `LOCAL_CHART_VS_TRANSFERRED_GRAMMAR.md`.

The frozen demotion action follows. The attractor rule and basin-ratio structure are moved from the transportable-grammar column to the local-chart column until and unless a subsequent pre-registered test rehabilitates them.

---

## What FAIL Does NOT Mean

- It does not mean the rule "$h = \max$ odd unit" is wrong for the 29 carriers. It matches perfectly on all of them. The issue is that the null model produces smoother curves, so the matching rule does not beat the null on the pre-registered smoothness metric.
- It does not mean the basin ratios are anomalous — all 29 are in band.
- It does not mean the canonical construction is broken on the family.
- It does not invalidate B1 or B2 results.

It means, narrowly: **the particular smoothness-based test pre-registered in S28-v1.0, applied to this 29-carrier family with this scrambled-ring null model, does not earn the "transport confirmed" tag.**

---

## What Was Observed Structurally (Not a Verdict Claim)

The null model produces smoother $\beta$-curves than the canonical construction. This inversion was not anticipated in the pre-registration and is a structural observation about how the null behaves when $h$ is drawn uniformly from $\{0, \ldots, n-1\}$. For details see `S28_NULL_COMPARISON.md` §"Why the Null Is Smoother."

This observation does not alter the verdict under the frozen rules.

---

## Actions Required by the Verdict

Per the pre-registration outcome rule:

1. **Move entries in `LOCAL_CHART_VS_TRANSFERRED_GRAMMAR.md`:** "Attractor emerges as structural position" moves from right column to left.
2. **Update `INVARIANTS_BEYOND_TSML.md`:** the invariant "Attractor emerges from data (without canonical prior)" is demoted from "confirmed" to "Z/10-local."
3. **No modification to the pre-registration or re-running with new parameters.** A subsequent sprint (S29) may use a different null model or expanded family, but that is a new sprint, not a S28-v1.0 revision.

---

## No Interpretation Beyond the Frozen Claim

The frozen claim tested was: *does the specific attractor + basin-ratio curve invariant, under the specific smoothness metric and scrambled-ring null, transport across the specific 29-carrier family?*

The answer, under the pre-registered rules: **No, not by this test.**

No inference is drawn about physics, broader grammar transport, the overall TSML/BHML program, or any other invariant. Sprint 28 tested one thing; it returned FAIL; the record stands.
