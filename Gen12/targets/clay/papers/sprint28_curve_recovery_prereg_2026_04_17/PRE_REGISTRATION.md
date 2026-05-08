# Sprint 28 — PRE-REGISTRATION: Curve-Based σ-Label Recovery

**Date pre-registered:** 2026-04-17
**Status:** PROTOCOL ONLY — no run, no results, no code execution.
**Sign-off required before execution.**

---

## Why pre-register

Sprint 26 left a sharp open question: σ-class **shape** (number of classes
and their sizes) is shell-recoverable via W3-freq histogram, perfectly so
for n ≥ 38 on analytic `C_0`. But σ-class **labeling** (which specific
units belong to which class) was not recovered by any of Sprint 23's
8 walks at small `n` with noisy data.

Sprint 28 asks: does **richer curve-based dynamics** on `T_emp` recover
the labeling?

This question has three a-priori-distinguishable outcomes (per
claudechat's framing). To make them honestly distinguishable, we
register the protocol **before** running, fix the methods, fix the
thresholds, and commit to one execution.

This document is the pre-registration. It is committed to `tig-synthesis`
*before* any Sprint 28 implementation file exists. The Sprint 28
implementation will reference this commit hash.

---

## Hypothesis space (the 3 outcomes)

After execution, exactly one of the following will be reported:

### Outcome A — Curve adds real information
> Curve-based clustering on analytic `C_0` recovers canonical σ partition
> with ARI ≥ 0.99 on all `n ≥ 38`, **strictly better** than W3-freq alone
> (defined as: at least 3 carriers where curve ARI = 1.0 but W3 ARI < 1.0,
> AND mean curve ARI > mean W3 ARI by ≥ 0.01).
>
> **Interpretation:** The shell/curve decomposition holds. σ labeling
> requires information beyond histogram. Confirms current synthesis
> framing.

### Outcome B — Curve is redundant with histogram
> Curve-based clustering ARI is statistically indistinguishable from
> W3-freq ARI on the same carriers (defined as: |mean curve ARI − mean
> W3 ARI| < 0.005, AND set of perfect-recovery carriers differs by ≤ 1).
>
> **Interpretation:** σ-labeling was always shell-recoverable; Sprint 26's
> partial recovery was a feature-richness limitation, not a
> shell/curve boundary. The synthesis framing simplifies: shell carries
> everything; "curve" was a description of the same projection at higher
> resolution.

### Outcome C — Curve still cannot recover labels
> Curve-based clustering ARI < 0.95 on at least half of carriers `n ≥ 38`
> at analytic `C_0` (where W3-freq is ≥ 0.985 everywhere).
>
> **Interpretation:** Something genuinely curve-invisible is in σ. The
> 2-adic Z-lift information may be irrecoverable from any `Z/nZ`-internal
> dynamics. Opens new question: what *external* observable would close
> the recovery?

If results fall outside all three (e.g., curve ARI better on some
carriers, worse on others, no clear pattern), report as **Outcome D —
ambiguous**, document the pattern, and do not retroactively assign one
of A/B/C.

---

## Method (FIXED in advance — no method shopping post-hoc)

### Test substrate
- Analytic `T = C_0(R_n, h_n, σ_n)` from Sprint 25 construction.
- No data generation, no noise. Pure asymptotic / infinite-data limit.
- Carriers: same 32-element family from Sprint 26
  (n ∈ {10, 14, 22, 34, 38, 46, 50, 58, 62, 70, 74, 82, 94, 106, 110,
  118, 122, 130, 134, 142, 158, 166, 170, 178, 190, 194, 202, 206, 214,
  218, 226, 230}).
- Universe for ARI scoring: `units(n) ∩ units_hat(T)` (same as Sprint 23/26).

### Strategies (exactly four, fixed before run)

These are the methods we will run. We will NOT add or remove strategies
after seeing results.

**C1 — Self-orbit full trajectory**
- For each unit `u`, compute orbit `O(u) = (u, T[u][u], T[T[u][u]][T[u][u]], ...)` until cycle.
- Label `u` by the full sequence (as a tuple).
- Cluster by label equality.

**C2 — Ensemble orbit signature**
- For each unit `u`, for each unit `b` in `units_hat`, compute orbit
  `O(u, b) = (u, T[u][b], T[T[u][b]][b], ...)` until cycle.
- Label `u` by the sorted multiset of `(orbit_length, terminal_value)`
  pairs across all `b`.
- Cluster by label equality.

**C3 — Meeting-time signature**
- For each pair `(u, v)`, compute the meeting time `m(u, v)` = smallest
  `k ≥ 0` such that `T^k(u, 1) == T^k(v, 1)`, where `T^k(x, 1)` denotes
  the k-th iterate of `x → T[x][1]`. Cap at `k = 4n` (no meeting → ∞).
- Label `u` by the sorted tuple `(m(u, v) for v in units_hat)`.
- Cluster by label equality.

**C4 — Composition-orbit signature**
- For each unit `u`, build `f_u(x) = T[u][x]` as a unary map.
- Compute orbit of any seed (use `1`) under `f_u`: `(1, f_u(1), f_u(f_u(1)), ...)` until cycle.
- Label `u` by `(orbit_length, cycle_length, sorted_set_of_visited_values)`.
- Cluster by label equality.

These four span the natural design space:
- C1: u-as-state, T as binary self-map (closest to Sprint 23 W4).
- C2: u-as-state, parameterized over second arg.
- C3: pairwise rendezvous (relational structure).
- C4: u-as-operator (acts on others), inverts the role.

### Scoring metric
- Adjusted Rand Index (same implementation as Sprint 23 / Sprint 26).
- Compared against `canonical_partition(n) = group units by v_2(3u+1)`.
- Per-strategy and per-carrier.

### Aggregate metrics (all reported)

For each of C1, C2, C3, C4 and for the W3-freq baseline:

1. Mean ARI over carriers `n ≥ 38`.
2. Number of carriers with ARI = 1.0 in `n ≥ 38`.
3. Set of carriers where strategy beats W3-freq (ARI strictly higher).
4. Set of carriers where strategy is beaten by W3-freq.

### Outcome decision rule
Apply the criteria of Outcomes A / B / C / D in the order listed.
Report the first that matches. No tie-breaking by re-running, no
parameter sweeps after the fact.

---

## What we will NOT do

- We will not add strategies C5, C6, ... after seeing the results, then
  re-classify the outcome.
- We will not adjust the ARI thresholds in Outcomes A/B/C after seeing
  the numbers.
- We will not change the carrier set after seeing which carriers
  recovery succeeds on.
- We will not change the clustering metric (always exact label equality
  on the strategy's defined feature, then ARI vs canonical).
- We will not run on noisy data instead of analytic `C_0` to "rescue" a
  failing strategy. (Noise introduces a confound; Sprint 26 already
  established the noise-free baseline.)
- We will not change the canonical σ partition definition.
- If results don't fit A, B, or C, we report Outcome D honestly.

---

## What is left intentionally open

- We have **not** chosen a "best" strategy a priori. C1-C4 are run
  independently; we report all four results without weighting.
- We have **not** specified post-hoc analysis (e.g., "which σ-class did
  C2 confuse with which?") — that is allowed as exploratory secondary
  analysis after the primary outcome is reported, but cannot be used to
  re-classify the outcome.
- We have **not** committed to follow-on sprints based on outcome.
  Outcome A / B / C will each suggest different follow-ons; those
  decisions are not pre-registered.

---

## Implementation contract (post-sign-off)

Once this pre-registration is signed off:

1. Write `impl/curve_recovery.py` implementing exactly the four
   strategies C1-C4 above, no more, no less.
2. Run once on the 32-carrier set.
3. Write `RESULTS.md` reporting:
   - Per-strategy per-carrier ARI table.
   - Aggregate metrics as defined.
   - Outcome A / B / C / D classification.
   - The pre-registration commit hash.
4. Commit + push to `tig-synthesis`.

No iteration on the implementation after the first run. If a strategy is
ill-defined for some carrier (e.g., empty `units_hat`), report ARI = N/A
for that (strategy, carrier) and exclude from aggregate.

---

## Authorization needed

Brayden, please confirm:

1. The four strategies (C1-C4) are the right pre-registration set, OR
   propose one substitution before sign-off.
2. The outcome decision rule (Outcomes A/B/C with their numeric
   thresholds) is acceptable.
3. The "no method shopping" constraints are accepted.

On confirmation, this document will be committed to `tig-synthesis` as
the pre-registration record. Sprint 28 implementation begins only after
that commit is on the remote.

---

*© 2026 Brayden Ross Sanders / 7Site LLC*
*Sprint 28 — pre-registration only; awaiting authorization before run.*
