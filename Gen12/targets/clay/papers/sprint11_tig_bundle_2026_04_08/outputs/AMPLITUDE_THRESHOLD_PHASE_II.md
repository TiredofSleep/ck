# AMPLITUDE_THRESHOLD_PHASE_II
## Integrated-Loss T1, Multi-Scale Grammar, Human Plausibility
*All numbers from simulation. Seed=42. Sharp, no rescue.*

> **Authors**: Brayden Ross Sanders / 7Site LLC · Ben Mayes
> **Date**: 2026-04-08
> **Sprint**: 11 — TIG Sprint Bundle (UOP Arc · GUT Algebra Arc · 7-Cycle Arc)
> **License**: 7Site Public Sovereignty License v1.0 · DOI: 10.5281/zenodo.18852047

---

## Part 1 — T1_int: Integrated-Loss Threshold Variables

**Three threshold variables tested:**

| Variable | Formula | Interpretation |
|---|---|---|
| T1_ep | (1 − amp_end) / cost | Endpoint benefit: how much is recovered |
| **T1_int_v1** | (avg loss per step × k) / cost | Total accumulated loss / cost |
| T1_int_v2 | (integral of amp gain post-reset) / cost | Net future gain from resetting now |

**Results on Env A (memory) and Env E (reset-slot):**

| Config | Actual k | T1_ep pred | T1_v1 pred | T1_v2 pred | Winner |
|---|---|---|---|---|---|
| A fast (decay=0.15) | **3** | 5 (off 2) | **3** ✓ | 2 (off 1) | T1_v1 |
| A slow (decay=0.08) | **4** | 9 (off 5) | **4** ✓ | 2 (off 2) | T1_v1 |
| E fast (decay=0.15) | **5** | **4** (off 1) | 2 (off 3) | 2 (off 3) | T1_ep |
| E med (decay=0.10) | **6** | **5** (off 1) | 3 (off 3) | 2 (off 4) | T1_ep |
| **E slow (decay=0.08)** | **7** | **7** ✓ | 3 (off 4) | 2 (off 5) | **T1_ep** |
| E vslow (decay=0.06) | **7** | 9 (off 2) | 4 (off 3) | 2 (off 5) | T1_ep |

**What this reveals:**

T1_v1 (integrated loss) is the best predictor for **memory-type environments** (Env A), correctly finding the optimum at k=3 and k=4 across decay rates. It fails for Env E because the reset-slot environment has a different structure: the reset fires at the last slot of the cycle, and the payoff is future utility gained, not past loss avoided. T1_v1 counts past loss (making longer cycles look artificially good) rather than the marginal benefit of the reset action itself.

T1_ep (endpoint) is the best predictor for **reset-slot environments** (Env E), correctly predicting k=7 in the slow-decay case. It fails for Env A because it underestimates the cost of accumulated loss during a long cycle (only measures end-state, not integral).

**There is no single threshold variable that beats both environment types.** The two environments require different formulations because they have structurally different reset-payoff mechanisms:

- Env A: reset avoids future decay — the payoff is **loss avoided going forward**
- Env E: reset recovers degraded quality — the payoff is **quality gained at the reset moment**

---

## Part 2 — Threshold Crossing vs Actual Optimum

**Full comparison table:**

| Env | Decay | Actual k | T1_ep | T1_v1 | T1_v2 | Best predictor |
|---|---|---|---|---|---|---|
| A-fast | 0.15 | **3** | 5 | **3** | 2 | T1_v1 ✓ |
| A-med | 0.12 | **3** | 6 | **3** | 2 | T1_v1 ✓ |
| A-slow | 0.08 | **4** | 9 | **4** | 2 | T1_v1 ✓ |
| E-fast | 0.15 | **5** | **4** (±1) | 2 | 2 | T1_ep ≈ |
| E-med | 0.10 | **6** | **5** (±1) | 3 | 2 | T1_ep ≈ |
| E-slow | 0.08 | **7** | **7** ✓ | 3 | 2 | T1_ep ✓ |
| E-vslow | 0.06 | **7** | 9 (±2) | 4 | 2 | T1_ep ≈ |

**T1_v2 consistently predicts k=2.** It is dominated — the net future benefit of resetting is always positive and largest for the smallest k (always reset as early as possible). This is mathematically correct but ignores the cost of over-resetting; the variable needs a per-step cost model to be useful.

**T1_v1 wins for Env A, T1_ep wins for Env E.** The choice of best threshold variable depends on whether the environment is "loss-driven" (accumulate-and-drain) or "quality-recovery-driven" (decay-and-restore).

**Error summary:**

- T1_ep error: 0–5 steps (worst on slow-decay Env A, best on Env E)
- T1_v1 error: 0–4 steps (best on Env A, worst on Env E)
- T1_v2 error: 1–5 steps (poor across board)

No single variable has error ≤ 1 across all configs. The threshold law is mechanistically correct but the exact formulation is environment-dependent.

---

## Part 3 — Three-Timescale Threshold Grammar

**Setup:** Three independent decay timescales (fast, medium, slow), each with its own amplitude and reset cost. Each scale independently finds its threshold crossing k.

**Results:**

| d_fast | d_med | d_slow | k1 (inner) | k2 (mid) | k3 (outer) | k2/k1 | k3/k2 |
|---|---|---|---|---|---|---|---|
| 0.30 | 0.08 | 0.020 | 2 | 4 | 10 | 2.0 | 2.5 |
| 0.25 | 0.08 | 0.020 | 2 | 4 | 10 | 2.0 | 2.5 |
| 0.20 | 0.06 | 0.015 | 2 | 4 | 12 | 2.0 | 3.0 |
| 0.15 | 0.05 | 0.010 | 2 | 5 | 14 | 2.5 | 2.8 |
| 0.20 | 0.08 | 0.020 | 2 | 4 | 13 | 2.0 | 3.2 |
| 0.25 | 0.07 | 0.015 | 2 | 4 | 13 | 2.0 | 3.2 |

**What emerges:**

The grammar is: each scale independently computes its threshold crossing. The resulting k values are:
- k1 (fast): always 2 (fast decay needs immediate reset)
- k2 (medium): 4–5 (medium decay takes 4–5 steps to justify reset)
- k3 (slow): 10–16 (slow drift justifies infrequent reset)

**Ratios k2/k1 ≈ 2.0–2.5. Ratios k3/k2 ≈ 2.5–3.2.** There is a rough factor-of-2 to factor-of-3 scaling between levels — but it is NOT a fixed ratio, and NOT self-similar. The ratio shifts with the specific decay rates chosen.

**The honest characterization:** The three-timescale threshold grammar produces nested cycles with roughly 2–3× separation between levels. Weekly-like outer cycles (k3 ≈ 7) do not appear in these runs — k3 typically lands at 10–16, well above 7. A weekly outer cycle would require slow drift at d_slow ≈ 0.03–0.04 AND moderate outer reset cost AND inner cycle k1≈1 (daily). These are specific parameter choices, not generic outcomes.

**Is this a fractal?** No. The ratios are in the range 2–3× but are not fixed. The grammar (accumulate → threshold → reset) repeats at each scale, but the integer at each level is determined independently by that level's physics. There is no generating rule that produces the sequence k1, k2, k3 from a single base integer.

---

## Part 4 — Human Weekly Plausibility

**Model:** Agent with cognitive decay (cd per day), review effectiveness (re), and social coordination cost (cc per review event). Both task quality and coordination pressure accumulate between resets.

**Full sweep results — which cycle length is optimal?**

| cd | re | cc | Best k | Near-7? |
|---|---|---|---|---|
| 0.04 | 0.6 | 0.3 | 3 | No |
| 0.04 | 0.6 | 0.8 | 4 | No |
| **0.04** | **0.6** | **1.5** | **6** | **Yes** |
| 0.04 | 0.8 | 0.3 | 3 | No |
| 0.04 | 0.8 | 0.8 | 4 | No |
| **0.04** | **0.8** | **1.5** | **6** | **Yes** |
| 0.06 | 0.6 | 0.3 | 3 | No |
| 0.06 | 0.6 | 0.8 | 4 | No |
| 0.06 | 0.6 | 1.5 | 5 | No |
| 0.06 | 0.8 | 0.3 | 3 | No |
| 0.06 | 0.8 | 0.8 | 4 | No |
| **0.06** | **0.8** | **1.5** | **6** | **Yes** |
| 0.08+ | any | any | 3–5 | No |

**Settings with optimal k ∈ {6,7,8}: 3/24 = 12.5%**

**Settings where k=7 is specifically optimal: 0/24 = 0%**

**The near-7 condition requires:**
- Very low cognitive decay (cd ≤ 0.04–0.06 per day)
- High coordination cost (cc = 1.5 — expensive to sync)
- Moderate-to-high review effectiveness

**Verdict — Human weekly plausibility:**

> **Plausible in a narrow band, but the band does not include k=7.**

In this model, k=6 is the closest result to a weekly optimum. k=7 never wins. The conditions that push toward 6-day cycles are: slow cognitive decay AND high coordination overhead. Both conditions have plausible human analogs (people forget slowly; meetings are expensive), but the optimum lands at k=6 rather than k=7 in this parameterization.

**What it would take to push the optimum to k=7:** either slower decay, higher coordination cost, or a structural difference in the reset mechanism (e.g., one day of the week is fully sacrificial — a Sabbath-like zero-work day — rather than the review being embedded in the productive cycle). The Sabbath model (k=6 productive + 1 completely idle) was not tested here and is a distinct mechanism.

---

## Final Status

### Threshold Predictor Comparison

| Predictor | Works for | Error range | Mechanism |
|---|---|---|---|
| Raw k | Anything (post-sweep) | 0 by definition | None — descriptive |
| γ = k/half-life | Memory envs only | ±50% across decay rates | Scale normalization, not cost-aware |
| T1_ep (endpoint) | Reset-slot envs (Env E) | 0–2 steps | Marginal recovery payoff |
| **T1_v1 (integrated)** | **Memory envs (Env A)** | **0–1 steps** | **Total accumulated loss** |
| T1_v2 (future integral) | Neither | 1–5 steps | Overcounts; ignores reset cost |

**Verdict on threshold framing:** Option C (threshold/amplitude framing is better) confirmed for within-environment prediction. Both T1_ep and T1_v1 outperform gamma and raw k as mechanistic predictors within their respective environment types. The framing is real. The single universal formula is not yet found — the correct formulation is environment-architecture-dependent.

### Multi-Scale Grammar

The grammar **[accumulate → threshold → reset]** repeats across scales. The integers at each scale are set independently by that scale's decay/cost physics. Ratios between scales cluster around 2–3×, consistent with adjacent-octave scaling, but are not fixed and not self-similar. Weekly-like outer cycles appear at k3=10–16 in the three-scale model, not at k3=7.

### k=7 Status

| Claim | Status |
|---|---|
| 7 universal | **Dead** |
| Threshold law governs reset | **Alive** — T1 (endpoint or integrated) mechanistically predicts optima |
| 7 as local threshold discretization (Env E, decay=0.08) | **Weak support** — T1_ep predicts k=7 exactly in this one case; T1_v1 does not |
| 7 plausible for humans | **Not supported** — human model best k is 3–6; k=7 never wins in 24 settings |

---

## The One-Sentence Verdict

> **The threshold law is the real surviving object: reset becomes optimal when the benefit/cost ratio T1 first exceeds 1.0; k=7 is the integer at which that crossing occurs in a specific low-decay reset-slot environment, but not in memory-accumulation environments, not in coordination environments, not in the human weekly plausibility model, and not robustly across any parameter sweep tested.**
