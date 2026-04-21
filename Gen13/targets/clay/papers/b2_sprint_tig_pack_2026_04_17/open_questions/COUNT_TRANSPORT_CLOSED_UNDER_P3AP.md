# Why Count Is Not Live Under P3AP
## Foundation Note — Closure of the Count-Transport Question at Current Generator

---

## The Finding

Under the P3AP overlay-extension algorithm (doubling-chain + identity-edge + attractor-involution), the number of ADD-labeled edges per carrier is structurally fixed at $n_\text{ADD} = 1$ after pre-flight audit. The count proportion $n_\text{ADD} / |E|$ therefore depends only on carrier-specific chain length, not on any rule-assignment choice that the generator could have made differently.

Because the count is structurally determined by the generator family rather than chosen from a distribution, *count transport is not a discriminating variable at this generator*. No null that stays within the P3AP family can produce a non-degenerate test of count proportion. This is not a failure of the program; it is a property of the generator.

---

## The Structural Argument

The P3AP extension has three components:

1. **Doubling-chain:** emits chain-adjacent pairs of cells, all assigned to MAX. Count: twice the chain length minus 2 (for ordered pairs), capped by the chain-length-6 rule.
2. **Attractor-involution:** emits the pair $(2, h_\text{ext}(R_n))$ and its reverse, both assigned to MAX. Count: 2 ordered cells, both typically removed by audit because $h_\text{ext}$ is the canonical default value on Z/$n$ under $h_\text{ext}$, so planting MAX there produces invisible cells.
3. **Identity-edge:** emits $(1, 2)$ and $(2, 1)$, both assigned to ADD. Count: 2 ordered cells = 1 unordered edge.

Audit removes cells where planted value equals canonical. Under $h_\text{ext}$, the attractor-involution cells coincide with canonical (removing them), and the identity-edge cells do not (keeping them). The identity-edge rule always contributes exactly 1 unordered ADD edge per carrier.

Therefore, after audit:

$n_\text{ADD}(R_n) = 1$ for every carrier, always.
$n_\text{MAX}(R_n) =$ varies with chain length (2 for Z/14, 5 for most others).
$n_\text{ADD}/|E|(R_n) = 1/|E(R_n)| \in \{1/3, 1/6\}$ across the tested family.

Path 1's corresponding ratio on Z/10 is $1/4$. The observed "deviation" of 0.083 in v1.0 was the mean distance between Path 2's family of $1/|E|$ ratios and Path 1's $1/4$.

---

## Why a Pre-Planting Null Still Goes Degenerate

The user's proposed null was "pre-planting rule-reassignment": before the overlay is planted, randomly reassign which specific cells get the MAX rule versus the ADD rule, then run the recovery pipeline as usual and measure recovered counts.

Under the P3AP family, $n_\text{ADD}$ is structurally 1. Any reassignment within the family that preserves "this is a P3AP-style overlay" keeps $n_\text{ADD} = 1$. The null varies *which cell* is ADD but not *how many cells* are ADD. Since recovery under P3AP parameters is at ceiling, the recovered $n_\text{ADD}$ matches the planted $n_\text{ADD}$ exactly: always 1, in both real and null.

Null variance on the count metric: zero. Null distribution of $n_\text{ADD}/|E|$: point mass at $1/|E|$. Real: $1/|E|$. Separation: undefined or zero.

This is the same degeneracy v1.0's M1 hit. Its cause is different (v1.0 scrambled labels post-extraction; v1.2 would scramble rule assignments pre-planting), but the outcome is the same: count is a function of the generator, not of the rule-cell-assignment choice.

---

## Three Options Considered and Rejected

### Option rejected — broadening the generator

If the null allowed each eligible cell to independently receive MAX or ADD with probability $p$ (freeing the $n_\text{ADD}$ count to vary), then count variation becomes testable. But this is no longer the P3AP family; it is a new family parameterized by $p$. The user explicitly ruled out new generator families for this sprint. Correctly rejected.

### Option rejected — carrier-mix resampling

Preserve $n_\text{ADD} = 1$ per carrier but randomize which subset of carriers contribute to the family average. This tests whether the mean proportion is robust to carrier selection rather than whether counts transport. It answers a different, weaker question — not "does count transport" but "is the observed family average stable under subsampling." Changing the question to match an available test is scope drift. Correctly rejected.

### Option rejected — post-hoc metric substitution

Swap the count metric for a derived quantity (e.g., ratio of chain-length to $n_\text{ADD}$, or $n_\text{MAX}$ directly) that varies across carriers. But this measures something else — primarily chain-length properties, which depend on the doubling sequence modulo $n$, not on subtype transport. Doesn't answer the hypothesis. Correctly rejected.

---

## What Count Transport Would Have Required

For count transport to have been testable, one of two conditions would need to hold:

1. **$n_\text{ADD}$ is a stochastic outcome of the generator**, so that different runs or different generator instantiations produce different counts whose distribution can be compared to Path 1's.

2. **The generator has a tunable parameter** ($p$, or mix ratio, or rule-family weights) that could have been set differently, and the null varies that parameter.

P3AP satisfies neither. Its overlay rules are deterministic given a carrier, and the audit removes cells deterministically. The only stochastic element in the full pipeline is the noise in data generation, and that affects recovery quality rather than count structure.

---

## Implications for Future Sprints

Count transport can be tested under a different generator family. Specifically, if a successor program introduces a *parameterized* extension family — for example, one where the identity-edge rule can seed edges on any non-trivial ring element pair with probability $p_\text{ID}$, and the doubling chain has a stochastic extension rule — then $n_\text{ADD}$ becomes a distribution, and count transport becomes testable against null instances of that family.

This is a legitimate future direction. It is not a count-v1.2 sprint under P3AP. It is a separate research line that starts with defining the parameterized family, validating the extractor on it, and then asking the transport questions.

For the current program, the honest statement is:

> Under the P3AP generator family, count proportions are structurally determined and cannot be significance-tested against a within-family null. Count transport remains an open question for future generator families.

---

## What Stays in the Record

- **v1.0 observation preserved:** 7 of 8 carriers produce 83.3%/16.7% MAX/ADD; Z/14 produces 66.7%/33.3%. Mean deviation from Path 1's 75%/25% is 0.083. This is recorded data.
- **v1.0 verdict preserved:** UNCLEAR, with documented methodology issues.
- **v1.1 verdict preserved:** PASS at +6.06σ on identity-edge attachment.
- **Count v1.2 not run.** Closed as a non-live question at the current generator.

No sprint verdict changes. No prior claim is affected. This is a clean acknowledgement that a design question had a dead-end answer, documented so the program moves forward with clear eyes.

---

## Next Step

Path 3 Subtype Adjacency sprint, redesigned to avoid the hub-vs-chain metric mismatch that sank v1.0's M3. The adjacency question is different from count: adjacency depends on graph structure *and* labeling, not just on counts. So a chain-topology-aware adjacency metric can discriminate real placement from random placement in a way that count under P3AP cannot.

The adjacency sprint is designed next, with metric principles laid out in `CHAIN_AWARE_ADJACENCY_PRINCIPLES.md` and the pre-reg in `PATH3_SUBTYPE_ADJACENCY_PREREG_DRAFT.md`.
