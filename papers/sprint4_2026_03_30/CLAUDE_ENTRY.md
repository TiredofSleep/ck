# Sprint 4 — Claude Entry Point
## Start Here for Fresh Session | 2026-03-30

*(c) 2026 Brayden Ross Sanders (7Site LLC) & C. A. Luther — Trinity Infinity Geometry*

---

## What happened in Sprint 4

Sprint 4 (Brayden + C. A. Luther, March 30 2026) produced a major reframing:

> **TIG is not a framework built around one special table. It is a universal construction law operating on the class of semiprimes with orbit-central HAR elements.**

b=10 was historically first. The law is the result.

---

## The Frozen Law Set (read ATLAS_LAW_SET.md for full details)

**Five settled laws:**

| Law | Statement | Status |
|-----|-----------|--------|
| Construction hierarchy | arithmetic → gate → order seed → native optimum | PROVED, 11+ bases |
| HAR rule (revised) | h = min{h∈C : h²∈C, h²≠1, h²≠h} | SETTLED, overrides orbit-size rule |
| φ-compression | larger unit groups → lower gap, r=−0.605 | SETTLED |
| Gradient law | within φ-tier: gap ∝ max_dist(non-orbit C, HAR)/C_range | r=0.749, CONJECTURAL |
| Gate-corrected position law | HAR_m high when HAR=min(C\{1}) OR gate blocks G below HAR | SETTLED |

**One open residual:** within-grad gap spread (~0.111). Leading candidate: orbit_hit_rate. Not yet a law.

---

## b=15 is the Cleanest Flagship

b=15 = 3×5, C={1,2,4,7,8}, G={3,5,6,9}, HAR=2, φ=5

**Three laws align at b=15 (only world where all three do):**
- Tier: 7.057 (easy tier, 78.6% random → 99% biased)
- Gradient: 0.714 (highest in φ=5 tier — tied with T*=5/7)
- Position: HAR=2=min(C\{1}) → high HAR_m cluster

b=10 is first-resolved (rank 9). b=15 is cleanest. b=14 is richest but hardest.

---

## The Three-Class Landscape Maps to CK Engine

The three reduction attractors (THREE_CLASS_LANDSCAPE.md) are:

| Class | b=10 stats | CK engine | Dog gait |
|-------|-----------|-----------|---------|
| Oracle | G-reach=0.076, gap=0.781, residual=0.42 | Phase 3, Order | TROT |
| Gate-strong | G-reach=0.018, gap=0.710, residual=0.40 | Phase 2, Transitional | WALK |
| TSML-like | G-reach=0.024, gap=0.709, residual=1.00 | Phase 1, Grammar, T*=5/7 | STAND |

**The dog physically walks through the construction hierarchy as coherence shifts.**
This is not a metaphor. The gait_mode[1:0] signal sent to the FPGA IS the class selector.

---

## Semiprime Atlas (5 tested worlds)

| b | Score | rnd% | HAR_m | gap | Quadrant |
|---|-------|------|-------|-----|---------|
| 55 | 10.045 | — | — | — | *predicted easiest* |
| 35 | 8.265 | 76.2% | 0.722 | 0.569 | easy + moderate |
| **15** | **7.057** | **78.6%** | **0.756** | **0.677** | **easy + rich** |
| 10 | 6.857 | 4.0% | 0.650 | 0.474 | hard + moderate |
| **14** | **2.500** | **0.0%** | **0.778** | **0.944** | **hard + rich** |
| 22 | 5.464 | 83.3% | 0.604 | 0.551 | easy + moderate |

**Two axes are independent**: ease (construction cost) and richness (selector quality) don't trade off.
b=35 out-of-sample confirmed (76.2% vs predicted "easy tier"). Formula is a tier predictor.

---

## Key HAR Rule Revision (from b=38)

**Old rule:** max orbit size wins.
**Revised rule:** min orbit-central element wins.

h = min{h∈C : h²∈C, h²≠1, h²≠h}

b=38 is the decisive case: orbit-size selects HAR=9 → HAR_m=0.059 (near zero).
Min orbit-central selects HAR=3 → HAR_m=0.584, 86% rate. Position law takes priority.

---

## Clay Tracks Updated

**Hodge (abelian fourfolds — SETTLED):**
Markman (2025, arXiv:2502.03415) proved Hodge conjecture for ALL abelian fourfolds of Weil type.
P3 (gap floor) is vacuously true for abelian fourfolds: Hdg²(A) = Alg²(A) exactly.
The real frontier: abelian varieties dim ≥ 5, general projective varieties.
Contact: Eyal Markman (UMass), Claire Voisin (Jussieu).

**NS (local criterion):**
B_local(x,r,t) = ||ω||_{L³(B(x,r))} · r/ν is structurally aligned with CKN-type local criteria.
7/2 threshold not in literature, not contradicted.
Contact: Zoran Grujić (UVA), Vladimír Šverák (Minnesota).

Full collaborator outreach pack: `clay/COLLABORATOR_TASK_PACK.md`

---

## What Needs to Happen Next (Priority Order)

### 1. R16 Atlas Jobs (compute, ~4-5 hours)

Run overnight on R16. The atlas has 7 untested predictions above b=15.
Start with b=55 (predicted easiest, score=10.045):

```bash
cd Gen10/papers
python r16_job1_reduction.py --b 55 --n_start 10000 --n_steps 100
python r16_job3_clustering.py --input results/reduction_b55_N10000.json
```

Then try b=35 with seeded reduction to get the 15.8x lift:
```bash
python r16_job1_reduction.py --b 35 --n_start 10000 --n_steps 100 --seeded
```

### 2. Test Within-Grad Gap Residual

Need same-φ worlds with differing grad_score to test gradient law cross-φ.
Find 2×prime bases at φ=4 with differing C structures.
Collect orbit_hit_rate at b=22, b=26, b=38 to test two-predictor model.

### 3. b=14 Order Seed

b=14 has 9 residual seed cells identified:
(2,7),(4,6),(4,8),(4,9),(5,9),(6,8),(6,9),(7,8),(7,9)

Run seeded reduction at b=14 to test whether TSML-like rate rises above 0%.

### 4. GitHub Commit Sprint4 Docs

```bash
cd Gen10
git add papers/sprint4_2026_03_30/
git commit -m "Sprint 4: universal construction law, 5-world atlas, three-class landscape, Clay updates"
git push
```

### 5. Dog Hardware (paused, resume when sprint4 work is settled)

See `Gen10/targets/r16_fpga_dog/PAUSE_NOTES.md`.
Next: flash ck_full.bit → leash test → attach XiaoR servo bus wires → LAUNCH_DOG.bat.

---

## Files in This Sprint4 Folder

| File | What it is |
|------|-----------|
| `CLAUDE_ENTRY.md` | **This file** — start here |
| `ATLAS_LAW_SET.md` | Canonical frozen law document (start here for the math) |
| `UNIVERSAL_LAW.md` | The reframing: "miracle moved to the law" |
| `SEMIPRIME_ATLAS.md` | Ranked atlas, 28+ worlds, 5 tested |
| `THREE_CLASS_LANDSCAPE.md` | Oracle/gate-strong/TSML-like formal note |
| `CONSTRUCTION_HIERARCHY.md` | Four-step pipeline + b=14 native TSML |
| `ORBIT_HAR_CONJECTURE.md` | HAR orbit-central selection rule |
| `GRADIENT_LAW.md` | Within-tier gap prediction |
| `GRADIENT_LAW_TEST.md` | b=38 decisive test, HAR rule revision |
| `HAR_MASS_PREDICTOR.md` | Position law for HAR_mass cluster |
| `SECOND_GAP_PREDICTOR.md` | Honest residual — within-grad spread |
| `SECOND_FLAGSHIP.md` | b=22 as generous flagship |
| `NATIVE_BASE_ATLAS.md` | Base-specific TSML discovery |
| `ATLAS_JOB_RESULTS.md` | Job results: Phase 1 (atlas sweep) |
| `PHASE2_JOB_RESULTS.md` | Job results: Phase 2 (Jobs 4,5,6) |
| `PHASE3_JOB_RESULTS.md` | Job results: Phase 3 (Jobs 7,8,9) — 15.8x lift |
| `PHASE4_JOB_RESULTS.md` | Job results: Phase 4 (Jobs 10,11) |
| `clay/COLLABORATOR_TASK_PACK.md` | Hodge + NS + outreach contacts |
| `clay/hodge/HODGE_GAP_FLOOR.md` | d_Hodge metric definition |
| `clay/hodge/HODGE_TIG_FRAME.md` | Full Hodge TIG frame |
| `clay/navier_stokes/NS_TIG_FRAME.md` | NS local criterion (corrected) |
| `CLAUDECODE_README.md` | Session summary from C. A. Luther |

---

## Key Numbers

- TSML-like rate (random, b=10): 4-6%
- TSML-like rate (biased seed, b=10): 52.7% → **15.8x lift**
- b=15 native: 78.6% random → 99% biased
- b=22 native: 83.3% random → 99.7% biased
- b=35 native: 76.2% random (out-of-sample validation)
- HAR rule verified at 12 bases: b=10,14,15,21,22,26,35,38,55,65,85,95
- T* = 5/7 = 0.714285... = Phase 2/3 boundary = walk-to-run threshold = b=15 grad_score
- b=6 is degenerate (no orbit-central HAR element)
