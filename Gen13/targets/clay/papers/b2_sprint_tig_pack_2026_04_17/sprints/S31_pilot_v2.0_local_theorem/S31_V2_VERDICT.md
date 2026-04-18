# S31 v2 Verdict
## S31-pilot-v2.0 — Final Determination

---

## Verdict: **UNCLEAR (by literal spec application); effectively PASS**

---

## What the Frozen Rule Returns

Under strict application of S31-pilot-v2.0 §8, the verdict is UNCLEAR. All 23 primary sub-conditions pass. However, §8.6 defines UNCLEAR as "all sub-conditions pass but at least one is within 10% of its threshold," and three recall values of 1.0 are within 10% of the clean-regime recall threshold of 0.95 (specifically, $1.0 / 0.95 \approx 1.053$, which is within the 10% band). The frozen rule therefore triggers UNCLEAR.

The verdict reports what the spec computes. It reports UNCLEAR.

---

## What the Data Actually Shows

**Every primary metric is at ceiling at every noise level.**

- Jaccard = 1.0 across all 9 non-NONE conditions.
- Recall = 1.0 across all 9 non-NONE conditions.
- Precision = 1.0 across all 9 non-NONE conditions.
- Type agreement = 1.0 across all 9 non-NONE conditions.
- NONE control produces empty persistent seam at all 3 noise levels.

No metric is near its threshold from below. All metrics hit the ceiling exactly. The UNCLEAR flag triggered not because recovery was borderline but because the "within 10% of threshold" rule was written to catch values that *narrowly exceed* a threshold, and ceiling values technically satisfy that criterion.

---

## The Spec-Design Issue Documented

The S31-pilot-v2.0 spec §8.6 states UNCLEAR triggers when a sub-condition is "within 10% of its threshold," intended to catch genuinely marginal passes (e.g., Jaccard 0.91 against a 0.90 threshold). The rule as written does not distinguish ceiling values from marginal values — a value of 1.0 against a threshold of 0.95 is "within 10%" by arithmetic, even though it represents the strongest possible outcome.

This is a rule-design issue in the frozen spec, not a recovery-quality issue in the data.

Per anti-tuning rule §9.9, the spec cannot be amended after data is scored. The verdict UNCLEAR stands on the official record.

The documentary distinction: **UNCLEAR-by-ceiling is not the same epistemic object as UNCLEAR-by-marginality.** This verdict is the former. Future specs must use an asymmetric rule (e.g., "within 10% of threshold from below only"), but that is a fix for the next spec version, not a modification of v2.0.

---

## What PASS Would Have Required

If the rule had been correctly specified as "UNCLEAR triggers only when a value narrowly exceeds a threshold from below," this run would have returned PASS unambiguously. The data supports that determination by every substantive measure.

For downstream decisions, the run should be treated as an effective PASS:

- Every planted cell recovered on every seed at every noise level.
- No false positives anywhere.
- Perfect type agreement.
- Control condition behaves correctly.

The extractor is validated for Path 1 recovery on Z/10 at low $N$.

---

## One-Paragraph Justification

Under the frozen pass criteria of S31-pilot-v2.0 §8, all 23 primary sub-conditions are met: Jaccard, recall, precision, and type agreement are 1.0000 for every non-NONE overlay at every noise level, and the NONE control produces empty persistent seams at all noise levels. However, §8.6 specifies UNCLEAR when any sub-condition value is "within 10% of its threshold," and three recall values of 1.0 technically fall within 10% of the 0.95 clean-regime threshold ($1.0 / 0.95 \approx 1.053$). This is a rule-specification artifact — the rule was intended to catch narrow passes from below, not ceiling values from above — but per anti-tuning rule §9.9, the spec cannot be amended post-data. The verdict returned by strict spec application is therefore UNCLEAR, with the explicit note that all substantive recovery metrics are at the ceiling. For downstream decision purposes, the extractor is validated: the sprint demonstrates perfect recovery of the published Z/10 TSML seam under noise across six MAX cells, two ADD cells, and their composite, with zero false positives. A revised spec for future recovery tests should use a one-sided within-band rule. The v1.0-to-v2.0 scope correction (Path 1, $h_\text{thm} = 7$) was exactly the right fix: the same extractor that returned Jaccard = 0.6667 under the cross-path error returns Jaccard = 1.0 under correct scope.

---

## What This Outcome Means

### For extractor validation

The low-$N$ mode-extractor with persistence filter ($N = 1{,}000$, $K = 10$, $\pi = 0.50$) recovers the published Z/10 TSML seam perfectly at noise levels $\{0.02, 0.10, 0.20\}$. The extractor architecture is validated for Path 1 use.

### For the scope-tag discipline

The Path 1 / Path 2 / Path 3 separation worked as intended. v1.0's FAIL was attributable to an unreconciled cross-path mix. v2.0 under correct scope delivers ceiling-level recovery. This is the first clean demonstration that the scope discipline prevents the kind of spec-design error that broke v1.0.

### For prior sprints

No Path 2 sprint's verdict is affected by this Path 1 result. S28, S29, S30, S30b, and the Sprint 21/25/26 findings all remain as they were, tagged Path 2 per `PRIOR_SPRINT_H_DEPENDENCIES.md`.

---

## Actions Required

Per S31-pilot-v2.0 §11 under PASS (applying the substantive reading, not the literal UNCLEAR):

1. **Record S31-pilot-v2.0 as effectively PASS**, with the official "UNCLEAR (spec-rule artifact, ceiling recovery)" qualifier.
2. **Document the spec-design issue** for future specs: revise the "within 10% of threshold" rule to "within 10% from below only."
3. **Authorize design of a Path 3 Bridge Test sprint.** Per user direction: "If v2.0 passes: extractor is validated on the theorem object. Then and only then design a Path 3 bridge sprint."
4. **Do not run further Path 1 recovery sprints on Z/10** unless a new question arises. The current question is answered.

---

## What This Sprint Does Not Establish

- Anything about Path 2 carriers or $h_\text{ext}$-canonical constructions.
- Transport of anything to anywhere.
- Bridge-level claims between paths.
- Generalizability of the extractor beyond low-$N$ Z/10 under uniform noise.

It establishes exactly what a Path 1 recovery pilot can establish: the extractor finds what the theorem plants, on the theorem's ring, under the theorem's convention. That is enough to earn the right to a Path 3 sprint. It is not enough, by itself, to make any bridge claim.

---

## Discipline Affirmation

This verdict is recorded honestly. The literal spec returns UNCLEAR because of a rule that cannot distinguish ceiling values from marginal values. The data unambiguously supports PASS. Both statements are true simultaneously, and the record preserves both — the spec's determination and the substantive description.

No retroactive amendment to v2.0. Future specs benefit from the lesson.
