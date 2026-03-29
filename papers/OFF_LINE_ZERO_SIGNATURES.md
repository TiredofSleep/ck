# Off-Line Zero Signatures: The Delay Trace
## Measuring the Wake of Temporary Zeros in Operator Chain History

*Brayden Sanders / 7Site LLC | March 2026*
*Classification: exact computation on 9-state model. Interpretation structural.*

---

## The Core Insight

The off-line zero cannot be observed directly. It exists during the collapse tick — the instant when the operator chain is in perfect tension between extension and collapse. By the time the next operator fires, it has resolved.

But the **chain history carries a trace**. A chain that passed close enough to an off-line zero had to traverse G-territory (Gap operators {2,4,5,6,8}) before the collapse fired. That traversal takes steps. Those steps are measurable.

**The delay signature** = mean sojourn of extended chains (those touching G before HAR) minus mean sojourn of clean chains (direct to HAR without G). This is the observable wake of the temporary zero.

---

## The Measurement

**Setup:** 50 values of λ ∈ [0,1], 50,000 chains each. For each chain, record:
- Whether it passed through G-territory before reaching HAR
- Total sojourn length (steps to HAR)
- G-depth (number of G-steps taken)

**Results:**

| λ | G-traversal rate | Delay signature | G-depth |
|---|-----------------|----------------|---------|
| 0.00 | 55.7% | **+0.028 steps** | 1.10 |
| 0.15 | 61.3% | +0.221 steps | 1.15 |
| 0.30 (CHA edge) | 82.7% | **+0.883 steps** | 1.53 |
| 0.50 | 88.8% | **+37.4 steps** | 37.9 |
| 0.70 | 86.2% | +37.5 steps | 38.1 |
| 0.88 (peak) | ~87% | **+37.8 steps** (max) | ~38 |

---

## What This Means

**At λ=0 (TSML):** Delay signature ≈ 0.028 steps. The algebra collapses almost instantly. The zero has barely any room to form — 71 cancellation pairs, but they resolve in less than one extra step. On-line zeros are abundant (71 pairs) precisely because the system has *maximum cancellation room* at λ=0. The chain doesn't need to wander to find balance.

**At λ=0.30 (CHA edge):** Delay ≈ 0.88 steps. The chain that approaches an off-line zero now takes nearly a full extra step in G-territory before collapsing. This is the CHA corridor boundary — the hardest corridor to seal. The zero exists during that extra step.

**At λ=0.50:** Delay ≈ 37 steps. The chain sustained a 37-step extension through G-territory before collapse. The zero existed across all 37 steps — a long temporary chain, fully measurable in its wake, never directly observable.

**The peak at λ=0.88:** Maximum delay signature. This is deep in the BAL corridor where the deformation is pulling hardest toward BHML order structure. Off-line zeros here leave the longest wakes.

---

## The Structural Reading

The delay signature measures **how far extension went before collapse fired**. This is the inverse recursive experience of the zero gap:

- The chain aims for HAR (collapse, the algebraic ground)
- To approach HAR from G-territory, it must first extend outward (toward 9, toward BHML)
- At the furthest point of extension, the chain is nearest to the off-line zero
- The zero exists at that furthest point — the exact tick before the reversal
- Then collapse fires and the chain returns

The zero is not at HAR and not at the boundary. It is at the **turning point of the extension** — the moment before the chain knows which direction wins.

---

## Connection to the Corridor Argument

In ζ language: off-line zeros (σ ≠ ½) would correspond to chains that spent anomalously long in G-territory before collapsing back to the critical line. The frequency×duration argument proves these extended chains become measure-zero as t → ∞ — the delay signatures are real but the frequency of chains that take them vanishes.

**The corridor argument doesn't say extended chains don't exist. It says they become negligible.** The delay signature is the finite-time trace of what the zero did during its existence. The infinite deployment argument is why it couldn't sustain.

---

## What Claude Code Should Test Next

1. **Delay signature vs λ² scaling:** Does the delay grow as λ²? If so, this connects directly to the mean-square bound on Re(ζ'/ζ) — the delay is the operator-model proxy for the analytic drift.

2. **G-depth distribution:** Is the distribution of G-depths geometric (exponential tails) or heavy-tailed? Heavy tails would indicate some chains sustain very long temporary zeros — relevant to the support gap question.

3. **Corridor-conditional delay:** Within each corridor (Pre-leak, BRT, CHA, BAL), what is the delay signature? Does it respect the corridor boundaries?

4. **Two-tick vs longer wakes:** The sub-magma theorem guarantees collapse in ≤2 steps *from C*. But chains entering from G can take longer. Map exactly which starting states produce long-delay wakes.

---

## The Key Observable for Future Scans

When scanning ζ for corridor behavior, look not just for:
- σ_min > 0.5 (gap-positivity direct)

But also for:
- **Anomalous sojourn clustering:** Heights t where Re(ζ'/ζ) spends extended time in G-equivalent territory before returning to σ=½ behavior
- **Delay concentration:** The delay should concentrate near specific λ values matching the corridor boundaries (0.09, 0.30, 0.60)

These are the ζ-side observables corresponding to the operator-chain delay signatures.

---

*SHA-256(TSML): 7726d8a620c24b1e461ff03742f7cd4f775baed772f8357db913757cf4945787*
*(c) 2026 Brayden Sanders / 7Site LLC | Gen10.16, commit 271e0f8 | DOI: 10.5281/zenodo.18852047*
