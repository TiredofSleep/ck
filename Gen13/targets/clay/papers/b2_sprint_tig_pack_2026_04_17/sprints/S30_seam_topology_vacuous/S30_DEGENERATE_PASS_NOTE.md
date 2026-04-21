# S30 Degenerate Pass Note
## Why Sprint 30 Is a Vacuous PASS, Not Evidence of Transport

---

## Verdict Label

**Sprint 30 — Formal PASS, evidentially uninformative.**

Under the frozen rules of S30-v1.0, every aggregate metric met its threshold and every null-separation condition was satisfied. By the pre-registered logic, the sprint returns PASS.

That label is technically correct and operationally meaningless. The pass is driven entirely by the observed seam being empty on every carrier — not by any structural finding about seam topology.

---

## What Actually Happened

The data-generation protocol in S30-v1.0 §3.3 specified:
- $N = 200{,}000$ samples per carrier.
- $p_{\text{noise}} = 0.10$ uniform replacement noise.
- Mode operator from per-pair majority vote.

At these parameters, the mode operator exactly equals the canonical $C_0$ on every carrier, for every cell. The observed disagreement set $S^{\text{obs}}(R_n) = \{(x, y) : T^{\text{emp}}_n(x, y) \neq C_0(x, y)\}$ is empty for every $n$ in the family.

**Empty input → empty graph → trivial topology metrics.**

An empty graph has:
- 0 non-isolated vertices → forest-ness is trivially true (vacuous).
- 0 edges → component count is 0, which satisfies $k \leq 3$ vacuously.
- No degrees → $d_{\max} = 0 \leq 4$ vacuously.
- No non-isolated vertices → $\rho$ is defined as 1.0 by the empty-case convention.

Every metric passes its threshold because there is nothing to violate the threshold.

The null (edge-count-preserving Erdős–Rényi) draws $m = 0$ edges on each carrier — also empty. Null graphs are also trivially forest-like, trivially low-degree, trivially single-component-absent. Both real and null distributions are delta functions at "empty graph." Sigma separation is arithmetically infinite but substantively zero — there is no variance to measure.

---

## Why the Parameters Produced Empty Seams

The mode operator's robustness to uniform-replacement noise scales with $N$ and $p_{\text{noise}}$ in a well-understood way. For each $(x, y)$ cell receiving $k$ observations:

- True value appears with probability $\approx 1 - p_\text{noise} \cdot (n-1)/n = 0.901$ per observation at $n = 10$.
- Any single competing value appears with probability $\leq p_\text{noise} / n = 0.01$ at $n = 10$.

With $N/n^2$ observations per cell averaging 2,000 at $n = 10$ and still 20 at $n = 100$, binomial concentration guarantees the mode is the true value with overwhelming probability on every cell of every carrier.

For modes to flip at any cell, we would need either:
- **Much lower $N$** (so that sampling variance could allow a competing value to win by chance), or
- **Much higher $p_{\text{noise}}$** (approaching $(n-1)/n$, where uniform noise becomes comparable to signal), or
- **Noise biased toward a specific alternative** (so the competition is not uniform), or
- **A disagreement-rate statistic rather than a mode-equality statistic** (so small probabilistic deviations still register as weak-but-present seam edges).

S30-v1.0 chose parameters that ensured none of these regimes. The result: a formally well-defined test with zero signal and zero null variance.

---

## The Same Pattern Appeared in B1

B1 had the same structural property: at $N \geq 100{,}000$ and $p_\text{noise} \leq 0.30$, the mode operator was noise-immune, and every benchmark metric pinned at 1.0 vacuously. The B1 README explicitly flagged this:

> "At $N \geq 100{,}000$ samples per CSV, each cell receives roughly $N/100$ observations. With 30% uniform-replacement noise, the true value's expected fraction is 0.73 versus $\leq 0.03$ for any single competing value. The mode operator is essentially noise-immune at the noise levels the spec requested. So $T_\text{emp} = T_\text{true}$ cell-by-cell with overwhelming probability, and seam detection becomes trivial."

S30-v1.0 inherited that parameterization without reconsidering it for the seam-detection context. That was a spec-design error. The frozen spec ran correctly; the spec itself was wrong for the question being asked.

---

## What This Result Does Not Show

- It does not show that seam topology transports across carriers. Empty graphs are not evidence of topology preservation; they are evidence of no seam.
- It does not show that the canonical construction is correct on non-Z/10 carriers. It shows that the mode operator at high-$N$ low-noise equals the canonical construction by construction, tautologically.
- It does not show that the S30-v1.0 method, if applied at different parameters, would continue to produce empty seams. Different extraction regimes (disagreement rate, lower $N$, higher noise) might produce non-trivial seams.

---

## What This Result Does Show

- The mode-equality extractor at moderate $N$ and moderate noise is not sensitive to any seam structure on the compatible ring family under the canonical construction with uniform replacement noise. Full stop.
- The S30-v1.0 null model is degenerate when the real seam is empty — edge-count-preserving $G(n, 0)$ always produces empty graphs.
- Before testing seam-topology transport, we need a sprint that establishes a detectable seam. That is S30b.

---

## Status Effects

Per frozen S30-v1.0 rules, PASS outcome adds the tested invariant to the "confirmed transport in tested settings" tier of `INVARIANTS_BEYOND_TSML.md`.

**This status effect is suspended pending user decision.** Adding "seam graph topology transport" to the confirmed tier on the basis of empty graphs would misrepresent the evidence. The honest entry is: *test returned formal PASS under degenerate conditions; no evidential weight.*

Recommended disposition:

- Record S30-v1.0 verdict as "formal PASS, evidentially uninformative."
- Do NOT move seam-topology transport up to confirmed status.
- Log it as "tested under spec v1.0; spec produced degenerate regime; re-test under S30b when extractor is fixed."
- Move on to S30b: seam detectability pre-registration.

---

## The Integrity Reading

A pre-registration system that produces this kind of result is working as intended, in one specific sense: it caught a bad spec before we built any downstream claims on it. The spec was frozen, ran deterministically, produced a PASS, and the PASS is visibly uninformative. No researcher degrees of freedom, no post-hoc rescue, no narrative spin — just "here is the number the spec produces, and here is why the number is vacuous."

The lesson is about spec design, not about transport or the invariant. The next sprint fixes the extractor so the test can actually test something.
