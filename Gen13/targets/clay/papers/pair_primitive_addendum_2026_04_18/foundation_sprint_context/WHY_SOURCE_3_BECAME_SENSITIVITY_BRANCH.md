# Why Source 3 Became A Sensitivity Branch
## Short Note on the v3.0 Revision

---

## The Original Problem

The first v3.0 draft specified Source 3 ("attractor-privilege reading") with a single frozen argument direction: attractor privilege on V0 reads as "hold at boundary," which maps to the excluded-side under the pair-primitive framework's vocabulary. Under that reading, Source 3 scored Map-V0-I +1 and Map-V0-II −1.

The direction was defensible — it connects the framework's attractor treatment (`ATTRACTOR_RECONCILIATION.md`) to its hold/gap vocabulary (`GAP_AS_BOUNDARY_NOTHINGNESS.md`) via a plausible reading of boundary-survival. But the alternative direction was equally defensible: attractor privilege as "where structure gathers" maps to the persistent-side (backbone of structural survival), which would invert the source's score.

Both readings are internally coherent. The choice between them was load-bearing because it would have been one of four scored sources, and under the ±1 scoring a single source swing changes aggregate by 2 — enough to flip the verdict if the other sources are less unanimous than predicted.

## Why This Was A Rubric-Loading Risk

A single frozen argument direction on a contested source makes the sprint's verdict depend on which reading the scorer committed to before looking at the data. Two failure modes were possible:

1. **Hidden selection effect.** If the scorer picked the direction that favored the preferred map (Map-V0-I), the sprint would report a PASS that is partly earned by scoring discipline and partly earned by the argument-direction choice. The PASS sentence would not distinguish these two contributions.

2. **Hidden fragility.** If the scorer picked the direction honestly but the alternative would have flipped the verdict, the sprint's PASS would be structurally unstable — a different honest scorer could produce the opposite verdict. The pre-reg's ostensible reproducibility (deterministic rubric on frozen data) would be undermined by the argument-direction dependency.

Neither failure mode is caught by the standard anti-tuning rules, because both happen *before* scoring begins — at the rubric-design level.

## What The Revision Does Instead

Source 3 becomes a **sensitivity branch**: the same checkpoint is scored twice, once under S3a (attractor privilege → excluded-side) and once under S3b (attractor privilege → persistent-side). Sources 1, 2, 4 are unchanged and fixed.

Two aggregate scores are produced per map (one per S3 branch). Two cleanness gaps. Two per-map verdicts.

The final verdict is decided by a **robustness rule**:

- If the same map wins under both S3a and S3b at cleanness, the sprint returns a **robust PASS** (or robust FAIL if neither wins under either branch).
- If the verdict changes with the S3 direction, the sprint returns **UNCLEAR by sensitivity**, with the specific disagreement documented.

This converts the argument-direction problem from a hidden rubric choice into an explicit sprint output. Whatever the scorer commits to, the reader can see.

## What This Costs

The sensitivity branch costs two things worth naming:

**1. Less discriminating power per scored source.** Under the original design, a uniform +1/−1 across four sources gave aggregate +4/−4, gap 8. Under the revised design, if Sources 1, 2, 4 produce +3/−3 and Source 3 is the tiebreaker, a disagreement between S3a and S3b produces aggregate (+4/−2) vs (+2/−4), with the verdict determined by where the +3 and +2 fall relative to the ≥+3 threshold. The sprint can now return UNCLEAR-by-sensitivity in cases where the original design would have returned PASS — but the PASS would have been rubric-loaded.

**2. Slightly more complex verdict language.** "Robust PASS" and "UNCLEAR by sensitivity" are new verdict categories the prior PPM sprints did not need. The pre-reg has to specify these explicitly.

The cost is worth paying. An UNCLEAR-by-sensitivity result is more informative than a fragile PASS, because it tells the program exactly where the structural ambiguity lies: in Source 3's argument direction. That is a specific diagnostic finding future work can address.

## What This Preserves

The revision keeps everything load-bearing about the original design:

- V0 as the checkpoint target.
- V0-specific map labels (Map-V0-I / Map-V0-II).
- Sources 1, 2, 4 unchanged and fixed.
- Inherited thresholds (winner ≥ +3, loser ≤ +1, gap ≥ 2) applied per S3 branch.
- Prohibited substitutions rule.
- No composite claim with prior PPM verdicts.
- DRAFT-approve-freeze-execute workflow.

## Why This Is The Right Move Here And Not In Prior PPM Sprints

The prior PPM rubric sources (seam-graph structural split, identity-edge reading under multiplicative v1.0, leaf-edge placement, topology-family dominance) each had a specific single-direction argument that was structurally anchored: the argument was about majority edge counts, about identity being a multiplicative-trivialization point, about degree-1 placement, about edge-count majority. Each argument direction was determined by an algebraic fact about Z/n, not by a vocabulary choice inside the pair-primitive framework.

Source 3 under v3.0 is different. "Attractor privilege reads as hold-at-boundary" is a vocabulary argument inside the framework, not an algebraic fact about Z/10. The pair-primitive framework uses hold/gap/excluded language; which of V0's subtypes lands in which vocabulary slot is a choice the framework has not forced.

This is where sensitivity analysis is structurally appropriate. Prior PPM sources did not need it because their arguments were algebraically anchored. v3.0 Source 3 is not.

## The One-Sentence Framing

Source 3 is converted to a sensitivity branch because its argument direction is a vocabulary-level choice rather than an algebraically-anchored inference; scoring the checkpoint under both S3 directions converts a load-bearing rubric decision into an explicit sprint output, preserving reproducibility and producing more honest verdict language.
