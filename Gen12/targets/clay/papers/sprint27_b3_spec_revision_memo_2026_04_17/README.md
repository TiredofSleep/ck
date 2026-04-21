# Sprint 27 — B3 Spec Revision Memo

**Date:** 2026-04-17
**To:** Author of `SHELL_NATIVE_BENCHMARKS.md` §B3 (LBTP Layered Basin-Transport Pair)
**From:** Implementation team (Sprint 20 honest implementation; Sprints 21-26 follow-on findings)
**Re:** B3 LBTP returns FAIL on any honest implementation under the spec as written. Two minimal revisions would make it well-formed.
**Status:** Memo only — no spec changes proposed without author sign-off.

---

## Executive summary

B3 LBTP, implemented to spec in Sprint 20, returns **FAIL** with mean
`(paired joint accuracy) − max(singleton accuracy) = −4.31 pp` across
all 5 seeds. The FAIL is **structural, not implementational**:

- Joint accuracy of two independent ~95% events is necessarily `≈ 0.95²
  = 0.9025`, which is below either marginal (~0.955) by ≈ 5pp.
- The spec criterion "paired > max(singleton) + 5pp" requires joint to
  *exceed* either marginal, but joint cannot exceed the smaller marginal
  when streams are independent.
- The 5pp window is mathematically unmeetable in the spec's noise regime.

This memo proposes two minimal, mutually exclusive revisions that
preserve B3's **intent** (paired discrimination buys structural
information) while making the criterion **meetable**.

---

## What B3 was meant to test (our reading)

From `SHELL_NATIVE_BENCHMARKS.md` §B3:

> "Test that fitting the (T, B) pair jointly recovers more structural
> information than fitting either operator in isolation."

The intent is: **paired structure should reveal information unavailable
from either layer alone.** A passing B3 would witness the structural
coherence claim — that T and B together encode something neither does
solo.

This is a meaningful structural-coherence claim. The pass criterion as
written does not test it.

---

## Why the spec criterion fails

Spec §B3 PASS condition:

> "(paired_acc − max(T_only_acc, B_only_acc)) ≥ 0.05 on held-out;
> AND individual recovery ≥ 90%."

**Implementation result (Sprint 20):**

| Seed | T_only acc | B_only acc | joint acc | paired − max(singleton) |
|---|---|---|---|---|
| 0 | 0.9546 | 0.9548 | 0.9120 | −4.29 pp |
| 1 | 0.9545 | 0.9531 | 0.9098 | −4.46 pp |
| 2 | 0.9554 | 0.9554 | 0.9126 | −4.27 pp |
| 3 | 0.9560 | 0.9559 | 0.9143 | −4.17 pp |
| 4 | 0.9547 | 0.9546 | 0.9112 | −4.35 pp |

Joint accuracy = `acc_T × acc_B = 0.955² = 0.9120` (matches observation
exactly).

Under the spec's noise model (5% independent flips on each stream), the
joint mode's marginal predictions equal the single-stream modes, and the
joint event "both correct" equals their product. Thus:

```
joint_acc = acc_T × acc_B
          ≤ min(acc_T, acc_B)   (since accuracies ≤ 1)
          ≤ max(acc_T, acc_B)
```

The 5pp window is unachievable because joint cannot exceed either
marginal, let alone outpace the larger by 5pp.

---

## Proposed revision A: correlated noise

**Spec change:** introduce a single noise event per sample that perturbs
*both* streams (instead of two independent flips).

```python
# Current (independent):
if u_T < p_w: z_T = (z_T + delta_T) % n
if u_B < p_w: z_B = (z_B + delta_B) % n

# Proposed (correlated):
if u_pair < p_w:
    delta = rng_choice([-1, 0, +1])
    z_T = (z_T + delta) % n
    z_B = (z_B + delta) % n
```

Under correlated noise, paired observation gives the fitter access to
"both wrong together" vs "one wrong, one right" patterns. The joint mode
can then leverage one stream's signal to denoise the other.

Predicted result: `joint_acc > max(singleton_acc)`, with the gap
proportional to noise correlation strength.

This preserves "5% noise per stream" (each stream still has 5% flip rate
marginally) but eliminates the structural ceiling.

---

## Proposed revision B: drop N to make singletons sub-perfect

**Spec change:** reduce `N` from 200,000 to ~5,000 per config.

At N=5,000 with n=10 (2,500 obs/cell), per-cell mode is no longer
noise-immune. Singleton accuracy drops to ~0.75-0.85, leaving headroom
for joint mode to exploit cross-stream redundancy.

Predicted result: paired joint accuracy could plausibly equal
`max(singleton)` or modestly exceed it — the cross-validation effect of
having two correlated noisy estimates of the same underlying state.

This is the simpler of the two revisions, but it changes the test
character: it becomes more about "small-sample paired denoising" than
about "structural information shared across operators."

---

## Comparison

| Property | Current spec | Revision A (correlated noise) | Revision B (small N) |
|---|---|---|---|
| 5pp window meetable? | Never | Yes, if correlation > threshold | Plausibly |
| Tests structural coherence? | No | Yes, directly | No, tests denoising |
| Implementation cost | (already done) | ~50 LOC change in generator | ~2 LOC change in spec |
| Disruption to spec text | n/a | one paragraph in §B3 noise model | one number in §B3 sample table |
| Honest read of result | "criterion unmeetable" | "structural info detected" | "small-sample paired denoising" |

**Recommendation:** Revision A. It preserves the *intent* of B3 most
faithfully — testing whether paired structure carries information beyond
either marginal. Revision B is acceptable as a fallback if A is too
intrusive.

---

## What we did, what we didn't

**Did:** Sprint 20 implemented B3 honestly to the spec as written.
Result: 5/5 individual recovery PASS (T-table and B-table both 1.000
vs sealed truth), 5/5 joint criterion FAIL (joint − max < 0).

**Did not:** Modify the spec or weaken the criterion to force a PASS.
The honest output is: "the spec criterion as written is unmeetable in
this regime; here is why; here are two fixes."

**Did not:** Proceed to Stage 1B (cross-domain benchmarks). Pausing per
sprint20/README.md recommendation, awaiting spec author decision.

---

## Adjacent findings (Sprints 21-26) that strengthen the case

After B3 surfaced as structurally FAIL, the team built five follow-on
sprints to extract real structural invariants from the B-series data:

- **Sprint 21:** Prior-free discovery on all 39 B1+B2 datasets. Six
  invariants survive canonical-prior stripping.
- **Sprint 22:** N-stress; the collapse signature is two-tier
  (attractor first, corridor block second) across every system.
- **Sprint 23:** Walks on `T_emp` to recover σ partition; partial
  signal at small `n` with noise.
- **Sprint 25:** Algebraic proof that canonical `C₀` corridor closure
  is `{MAX, MIN}` for all `n` in extended family up to n=230.
- **Sprint 26:** ARI scaling — on analytic `C₀`, W3-freq achieves
  PERFECT σ-recovery (ARI=1.0) for many `n ≥ 38`. Sprint 23's
  "no walk recovers σ" was noise-limited, not structural.

These results suggest the **right** B3-style pair test would compare:

> "How much faster does (T, B) paired discovery converge to the
> 6-invariant fingerprint, vs T-only or B-only discovery?"

That formulation is intrinsically structural and meetable; we offer it
as a third potential revision for consideration.

---

## Ask

1. Confirm whether Revision A, Revision B, or a different revision is
   preferred.
2. If preferred revision is A, confirm we may amend the B3 generator's
   noise draw in `impl/generator/generate_lbtp.py`.
3. If preferred revision is B, confirm the new `N` value (~5000?) for
   the spec.
4. Sign-off (or rejection) of "B3 FAIL accepted as design observation"
   for closing Stage 1A while the revision is decided.

We will not modify the spec or rerun B3 with weakened criteria without
explicit go-ahead.

---

## Files

```
sprint27_b3_spec_revision_memo_2026_04_17/
└── README.md      ← this memo
```

No code changes are part of this memo. Implementation changes await
spec author approval.

---

*© 2026 Brayden Ross Sanders / 7Site LLC*
*Sprint 27 — B3 spec is unmeetable as written; two minimal revisions proposed; awaiting spec author.*
