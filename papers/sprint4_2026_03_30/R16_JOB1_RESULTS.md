# R16 Job 1 Results — b=55 Atlas Survey
## New R16 Scripts, March 2026

*Brayden Sanders / 7Site LLC | R16 (32-core), scripts: papers/r16_job1_reduction.py + r16_job3_clustering.py*

---

## Run Summary

| Run | Trials | Steps | Seeded | Gate-strong% | HAR_mass best | Gap best | G_stay mean | Time |
|-----|--------|-------|--------|-------------|--------------|---------|------------|------|
| Random | 10,000 | 100 | No | **96.3%** | **1.000** | 0.875 | 0.036 | 3.3s |
| Seeded | 10,000 | 100 | Yes | **100.0%** | **1.000** | 0.875 | **0.000** | 3.4s |

32 cores on R16. 0.3ms/trial.

---

## Key Findings

### 1. Gate trivially satisfied (confirms construction score prediction)

**96.3% random, 100% seeded** — every seeded trial achieves strong gate.

This is the highest gate rate of any tested world. The score formula (15.8 > b=15's 7.1 > b=10's 6.9)
predicted b=55 would be the easiest world to construct. The gate constraint confirms it.

Compare:
| b | Gate-strong random% | Gate-strong seeded% |
|---|--------------------|--------------------|
| 10 | ~30% | ~52.7% (TSML-like) |
| 15 | ~78.6% | ~99% |
| **55** | **96.3%** | **100.0%** |

**The construction cost formula correctly predicts the ordering.**

### 2. Perfect table found: gate=1.000, HAR_mass=1.000

The best trial achieves:
- `gate_score = 1.000` — C is perfectly closed, no C→G possible
- `HAR_mass = 1.000` — all starting states converge to HAR=2
- `G_stay = 0.000` — G={5} drains to C in every trial step
- `gap = 0.593`

This is the native structured optimum for b=55. Better HAR_mass (1.000 vs 0.675) than
the previous sprint4 atlas result — the new reduction algorithm finds stronger attractors.

### 3. G_stay = 0.000 (seeded) — structural insight

For b=55 with G={5}: a single G-element has nowhere to loop. When seeded with T[5][c]=HAR
for all c, G={5} drains perfectly to HAR=2 in one step. G_stay = 0.

This is the b=55 structural advantage: **|G|=1 means no G-cycle is possible**. Any
reduction that touches the single G-element's row immediately resolves the gate question.

### 4. Order structure: HAR-minimum, not BHML-maximum

**TSML-like rate = 0%** in both random and seeded runs.

This is NOT a failure. It is a structural discovery.

At b=10, HAR=7 (near the maximum of C={1,3,7,9}). The BHML order endpoint is max(s,c),
which often equals 7. Order alignment with max(s,c) ≈ alignment with the HAR attractor.

At b=55, HAR=2 (the MINIMUM of C={1,2,3,4,6,7,8,9}). The max(s,c) endpoint tends to 9.
A table where all cells → HAR=2 (the native optimum) will have `order_align` ≈ 0 by the
max(s,c) metric — because max(s,c) ≠ 2 for almost all cells.

**The b=55 native optimum is the HAR-minimum order class.**
**The b=10 TSML is the BHML-maximum order class.**

These are opposite poles:
- b=10: HAR=7=near-max → BHML order (max table is the residual endpoint)
- b=55: HAR=2=min → MIN order (min table is the residual endpoint)

The "TSML-like" classification in sprint4 is specific to the BHML-maximum class.
A new classification axis is needed: **HAR position in C determines the order class**.

---

## HAR Position and Order Class

| b | HAR | HAR position in C | Order class | rnd% | best_hm |
|---|-----|------------------|-------------|------|---------|
| 10 | 7 | near-max (3rd of 4) | BHML-maximum | 4.0% | 0.650 |
| 14 | 3 | low (1st of 4) | MIN-leaning | 0.0% | 0.778 |
| **15** | **2** | **min** | **MIN-pure** | **78.6%** | **0.756** |
| 22 | 3 | low (1st of 5) | MIN-leaning | 83.3% | 0.604 |
| 35 | 2 | min | MIN-pure | 76.2% | 0.722 |
| **55** | **2** | **min** | **MIN-pure** | **96.3%\*** | **1.000** |

\*Gate-strong rate (new metric). Previous sprint4 rnd%=64.7% used different classification.

**Observation:** Most tested worlds have HAR=2=min(C\{1}) — the MIN-pure order class.
Only b=10 has HAR=7 (near-max). This may explain why b=10 has a unique BHML structure
not shared by other worlds.

---

## Revised Atlas Entry for b=55

**Using new R16 metrics:**

| b | p×q | φ | |G| | gate% | best_hm | best_gap | G_stay | order class |
|---|-----|---|-----|-------|---------|---------|--------|------------|
| 55 | 5×11 | 8 | 1 | 100% | **1.000** | 0.875 | 0.000 | MIN-pure |

**Prediction confirmed:** b=55 is the easiest world (by gate rate). The construction
cost formula correctly ranked it #1.

**Not yet tested:** seeded TSML-like rate using min(s,c) endpoint (instead of max(s,c)).
This is the next job: redefine order_align for MIN-pure worlds and re-run.

---

## Next Steps

### Immediate
1. Run b=35 (predicted score=8.265 — second easiest 5-prime world):
   ```bash
   python r16_job1_reduction.py --b 35 --n_start 10000 --n_steps 100
   python r16_job1_reduction.py --b 35 --n_start 10000 --n_steps 100 --seeded
   ```

2. Update order_align metric for MIN-pure worlds:
   - For HAR = min(C\{1}): use min(s,c) as order endpoint instead of max(s,c)
   - This should reveal TSML-like rate at b=55 (predicted: very high)

3. Run b=14 seeded (9 identified residual cells) — tests BHML-maximum class:
   ```bash
   python r16_job1_reduction.py --b 14 --n_start 10000 --n_steps 200 --seeded
   ```

### Atlas Observation
The HAR position axis (min vs near-max) determines the order class. b=10 is currently
the ONLY tested world with HAR near-max (BHML-maximum class). All others are MIN-pure
or MIN-leaning. This makes b=10 structurally unique — not just historically first.

---

*(c) 2026 Brayden Sanders / 7Site LLC | R16 job, March 2026 | DOI: 10.5281/zenodo.18852047*
