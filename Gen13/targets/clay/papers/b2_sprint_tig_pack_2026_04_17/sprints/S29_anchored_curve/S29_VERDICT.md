# S29 Verdict
## Sprint 29, S29-v1.0 — Final Determination

---

## Verdict: **FAIL**

---

## One-Paragraph Justification

Under the pre-registered pass criteria of S29-v1.0 §5.1, Sprint 29 fails. One of the five sub-conditions passes (M3: all 29 carriers have basin-ratio deviation $D \leq 0.25$, but the null shows M3 also holds for 100% of scrambles, so this metric carries no signal). The other four fail by wide margins: real Kendall tau is 0.063 against a threshold of 0.35 (not even one-fifth of the required monotonicity); real linear $R^2$ is 0.000046 against a threshold of 0.40 (essentially no linear trend); real tau separation from the unit-valued-attractor null is 0.60σ against a 2σ requirement; real $R^2$ separation is −0.79σ, meaning the real value sits *below* the null mean — random unit-valued scrambles produce marginally better linear fits of $D$ on $d_1$ than the canonical rule does. Across the 29 tested carriers, basin-ratio deviation from the anchor does not correlate with unit-group-size depth in any detectable way. Per the anti-tuning rules of S29-v1.0 §7, no threshold is adjusted, no alternative metric is substituted, no depth coordinate is swapped, and no interpretation beyond the frozen hypothesis is applied. The sprint returns FAIL as specified.

---

## What This FAIL Means (Per S29-v1.0 §12)

From the frozen outcome rules:

> **Outcome 2: FAIL.** `LOCAL_CHART_VS_TRANSFERRED_GRAMMAR.md` gains a line under "Attempted transport, not confirmed" documenting this specific failure.

The required action is to add a single entry to the split document:

> *"Anchored deviation curve of basin ratio vs unit-group-size depth: attempted S29-v1.0, failed. Real Kendall tau 0.063 (threshold 0.35); real $R^2$ 0.000046 (threshold 0.40); null separation below 2σ on both primary metrics."*

S28's FAIL verdict remains independently recorded. No movement of entries between split columns in either direction as a result of S29.

---

## What FAIL Does NOT Mean

- It does not mean Z/10Z's invariants are wrong. The Z/10 tower theorem is unchanged.
- It does not mean the attractor rule "$h = \max$ odd unit" is wrong — it holds perfectly on all 29 carriers; the issue is that the *deviation* this rule produces does not organize by depth.
- It does not mean no anchored-curve invariant exists. It means this specific invariant ($\beta$), measured against this specific depth ($d_1$), on this specific family, with this specific null, does not support the anchored-curve hypothesis.
- It does not invalidate prior sprints.
- It does not imply anything about physics or broader grammar transport.

---

## What Was Observed Structurally (Not a Verdict Claim)

Basin ratios on the compatible ring subfamily vary carrier-by-carrier in a way that is not organized by unit-group size. At fixed $d_1$, $\beta$ values spread significantly (e.g., at $d_1 = 8$ across four carriers, $\beta$ ranges from 0.824 to 0.909). The spread is larger than any linear or monotone trend would predict. This observation is structural data, not a verdict modifier.

---

## Actions Required by the Verdict

1. **Append one line to `LOCAL_CHART_VS_TRANSFERRED_GRAMMAR.md`** under the "Attempted transport, not confirmed" heading, using the language above.
2. **No reversal of S28 demotions.**
3. **No modification of the S29 pre-registration or the metrics used.**
4. **No immediate follow-up sprint.** A decision on whether to run S30 (e.g., with a different response quantity, or a different depth coordinate) is left to the human investigator, not this sprint.

---

## No Interpretation Beyond the Frozen Claim

The frozen claim tested was: *does the specific deviation $D(R_n) = |\beta(R_n) - 0.79|$, measured against the specific depth $d_1(R_n) = |U(n)| - 4$, under the unit-valued attractor scramble null, support an anchored monotone trend on the 29-carrier family?*

The answer, under the pre-registered rules: **No.**

Sprint 29 tested one thing; it returned FAIL; the record stands.
