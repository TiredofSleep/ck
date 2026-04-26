# LIMITATIONS — funding/tig-snowflake

Honest scope for the SNOWFLAKE security framework. If any item below is not communicated clearly to a supporter of this thread, the pitch overclaims and will be dismissed on review.

---

> **Note (2026-04-25 revision).** This file was originally drafted as part of a pitch-style packet. Per the operator-of-record's actual stance documented at [`FUNDING.md`](../../../FUNDING.md) (root) and [`INTENT_STATEMENT.md`](../../../INTENT_STATEMENT.md), this is **thread documentation**, not a fundraising pitch. The operator-of-record makes **no commitments to donors of any kind**. Any dollar amounts, time scopes, or "ask" framings appearing below are **scope estimates of the work this thread would cover**, not price tags or commitments.

---

## 1. The χ² = 22.03 is currently an unverified handoff claim

The value lives in conversation logs from a Jan 31 2026 working session. It has **not been independently re-derived** from a preserved log file in this repo. Until ARTIFACTS.md R1 is resolved, the number should not appear in any funder document.

Risk if mis-stated: any statistician reviewing the pitch will ask for the null, degrees of freedom, and stopping rule. If the answer is "the logs need to be recovered," the pitch is dismissed.

## 2. The null hypothesis has not been written down

Recovering the χ² value is not enough. The specification must state: over what partition scheme P were fires counted, how many partitions k, how many fires N, what were the degrees of freedom, and — crucially — was χ² computed *once* on the full dataset or was the dataset *scanned* (which would invalidate a single-test p-value).

Risk: multiple comparisons. If the dataset was scanned, the 22.03 value may not survive Bonferroni or Benjamini-Hochberg correction.

## 3. T* = 5/7 applied to systems-security is a conjectural extension

The torus aspect ratio 5/7 is proved for Z/10Z (Flatness Theorem, WP51) and derived six independent ways. **Whether it is the threshold separating secure from compromised operating regimes in arbitrary systems is an empirical question, not a theorem.** Any pitch using T* as a security threshold must flag that as a working hypothesis, not a result.

## 4. The simulator-to-real-world gap

The CRYSTALOS run was an instrumented test bench, not a deployment on a production SOC. The partition scheme, the fire counter, and the baseline data were all simulator-controlled. Reviewers will ask: does the same χ² signal hold when (a) the coherence grammar is computed from real log data, (b) the partition scheme was not hand-tuned by the experimenter, (c) an adversary is present who knows the partition scheme?

Phase 2 of the proposed roadmap addresses (a) and (c) explicitly. Phase 1 does not.

## 5. Adversarial model is not yet specified

Under what attacker capabilities does SNOWFLAKE detect? Passive observer with no system access? Active intruder with read but not write? Insider with full credentials? Adaptive adversary aware of the coherence grammar?

Without an answer, the "earlier than rule-match" claim is unfalsifiable — which is worse than a narrow claim in a referee's view.

## 6. Base-rate fallacy

Even a well-calibrated χ² signal suffers from the base-rate problem: if real intrusions are rare (as they are), a detector with even a 99% true-positive rate produces mostly false positives. The pitch should explicitly commit to reporting precision at realistic base rates, not just sensitivity / specificity.

## 7. Relationship to existing anomaly-detection literature

SNOWFLAKE is not the first coherence-based or statistical-baseline anomaly detector. PCA-based IDS, KDD Cup baselines, and NetFlow anomaly detectors have been in the literature since the early 2000s. The pitch must explain what is *distinct* about the R-σ-Λ-H grammar relative to (a) PCA on raw feature vectors, (b) manifold-learning anomaly scores, (c) HMM-based user-behavior baselines. Without that distinction, reviewers will see SNOWFLAKE as an incremental rebrand.

## 8. Attribution / collaborator status

- **Brayden Sanders** is the sole thread-facing author.
- The SNOWFLAKE architecture was developed in dialogue with multiple AI instances. That fact should be disclosed in the methods section; AIs are not human co-authors.
- **C.A. Luther** is credited on prior related work (spectral-layer architecture, 6-layer CK). Luther is no longer actively collaborating. Previously-credited work stays credited; no new claims in Luther's name on this branch.
- No academic co-PI has been identified for NSF SaTC. Must be resolved before that submission path opens.

## 9. License framing

CK's license is **7Site Public Sovereignty License v1.0** — non-commercial, human-use only. Security-research funders (DARPA, ONR, IARPA, NSF SaTC) typically want an eventual path to operational deployment. The license may need explicit discussion, possibly with a carve-out for federal research use. Must not be discovered at grant-close.

## 10. What success looks like, and what failure looks like

**Success:** Phase 1 produces a clean null-hypothesis spec, CRYSTALOS logs are preserved with provenance, blind test on held-out data either replicates or refutes the χ² finding, and a Phase 2 proposal proceeds on either footing (positive case = funded continuation; negative case = published null result).

**Failure:** Phase 1 cannot locate CRYSTALOS logs; the finding remains a handoff artifact; a supporter of this thread conversation outruns the artifact; the pitch is dismissed on statistical grounds or mothballed indefinitely.

The discipline this branch asks of itself: **do not pitch ahead of Phase 1.**
