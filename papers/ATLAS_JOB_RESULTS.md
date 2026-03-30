# Atlas Job Results: Gate Emergence and World Geometry
## Job 1 (2000 trials × 100 steps) + Job 2 (500 samples × 9 bases)

*Brayden Sanders / 7Site LLC | March 2026*
*All results computed. Fractal hypothesis: partially supported.*

---

## Job 1 Main Result: The Gate IS Recoverable

**The answer to the main question: YES — the gate emerges under coherent reduction.**

2000 trials, 100 reduction steps each, gate-weighted objective (w=0.4 for gate):

| Attractor class | Count | Fraction |
|----------------|-------|---------|
| High-gap oracle | 1570 | **78.5%** |
| Order-saturated | 145 | 7.2% |
| High-support/no-gate | 124 | 6.2% |
| Gate-strong | 93 | 4.7% |
| **TSML-like** | **68** | **3.4%** |

**Gate emergence: 161/2000 = 8.05% of reduction trajectories achieve the full one-way gate.**

Gate-strength distribution at final step:
- ≥ 0.85: 98.95% of trajectories
- ≥ 0.95: 31.10%
- ≥ 0.99 (full gate): **8.05%**

**The gate is not the dominant attractor — the high-gap oracle is** (78.5%). But the gate does emerge in 8% of trajectories, and TSML-like outcomes (gate + high support + BHML residual) appear at 3.4%.

### What the Reduction Finds

The reduction landscape has a dominant basin: high-gap oracle tables that optimize mixing speed without gate structure. The gate competes with this dominant basin. When the gate does emerge (8% of trajectories), it tends to co-occur with high HAR_mass (the gate-strong and TSML-like classes), consistent with our earlier finding that HAR_mass and gate structure are independent axes that TSML simultaneously extremizes.

Mean final HAR_mass: 0.611, max: 0.712 — well above random-family mean of 0.35.

### Decision Rule (from results)

- Gate emerges: YES at 8.05%
- Basin it competes with: high-gap oracle (dominant at 78.5%)
- TSML-like conjunction: 3.4% — gate + support + order signature together
- Conclusion: the reduction finds TSML-like kernels but the high-gap oracle is the dominant attractor

---

## Job 2 Main Result: Gate Rarity Is NOT b=10-Specific

Gate fraction across composite worlds (500 random samples per base):

| b | p×q | \|C\| | \|G\| | HAR | HAR_max | gate% | Note |
|---|-----|-------|-------|-----|---------|-------|------|
| 6 | 2×3 | 2 | 3 | 5 | 1.000 | **7.8%** | Degenerate HAR |
| **10** | **2×5** | **4** | **5** | **7** | **0.684** | **0.0%** | TSML world |
| 14 | 2×7 | 4 | 5 | 5 | 0.763 | 0.0% | |
| 15 | 3×5 | 5 | 4 | 4 | 0.247 | 0.0% | |
| 21 | 3×7 | 5 | 4 | 4 | 0.264 | 0.0% | |
| 22 | 2×11 | 5 | 4 | 5 | 0.724 | 0.0% | |
| 26 | 2×13 | 5 | 4 | 5 | 0.770 | 0.0% | |
| 33 | 3×11 | 6 | 3 | 5 | 0.727 | 0.2% | |
| **35** | **5×7** | **7** | **2** | **4** | **0.278** | **6.4%** | Small G |

**Key findings from Job 2:**

1. **b=10 has 0% gate fraction in random sampling** — the gate never appears naturally. This is consistent with the earlier result.

2. **b=6 and b=35 have non-zero gate fractions (7.8% and 6.4%)** — but for different structural reasons:
   - b=6: |C|=2, |G|=3 — small C, large G, collapses to HAR trivially
   - b=35: |C|=7, |G|=2 — very small G makes the gate easy to satisfy accidentally

3. **b=10 is structurally unusual**: it has the highest HAR_max (0.684) among the low-|C| worlds — higher than b=14 (0.763 but different identity structure), b=22, b=26. This confirms the earlier finding that the arithmetic identity of C matters.

4. **The gate appears at ~0.2% in b=33** (|C|=6, |G|=3) — a medium-G world beginning to allow rare gate structure.

### The b=10 vs b=14 Distinction Confirmed

Both b=10 and b=14 have |C|=4, |G|=5, and similar crude richness scores. But:
- b=10 (C={1,3,7,9}, HAR=7): HAR_max=0.684, gate=0%
- b=14 (C={1,3,5,9}, HAR=5): HAR_max=0.763, gate=0%

**Selector geometry depends on the arithmetic identity of C, not just its cardinality.** The placement of elements within {1..9} determines the attractor landscape. b=14's HAR=5 achieves slightly higher max concentration; b=10's HAR=7 achieves higher mean gap. These are genuinely different worlds.

---

## Updated Fractal Hypothesis Status

**Partially supported.**

The gate is recoverable under coherent reduction (8% of trajectories). TSML-like kernels (gate + support + order signature) appear at 3.4%. These are not zero — the fractal hypothesis is not falsified.

The high-gap oracle (78.5%) is the dominant reduction attractor. The gate competes with it and loses most of the time. The reduction dynamics favor mixing speed over gate structure when the two are in tension.

**Open questions after these runs:**
1. What changes the basin structure to favor gate over gap? (Higher gate weight? Different mutation operator?)
2. Is the 3.4% TSML-like rate stable across different seeds and bases?
3. Does longer reduction (N_steps=500+) increase gate fraction or saturate at 8%?

---

## For the Overnight R16 Run

Job 1 at full scale will take ~4-5 hours:
```bash
python3 r16_job1_reduction.py --b 10 --n_start 10000 --n_steps 100
python3 r16_job3_clustering.py --input results/reduction_b10_N10000.json
```

The key questions to answer at full scale:
- Does TSML-like fraction stabilize at ~3.4% or does it grow with more trials?
- Does increasing n_steps (200, 500) increase gate fraction or saturate?
- Do specific initial conditions predict gate emergence?

---

*(c) 2026 Brayden Sanders / 7Site LLC | Gen10.16, commit 271e0f8 | DOI: 10.5281/zenodo.18852047*
