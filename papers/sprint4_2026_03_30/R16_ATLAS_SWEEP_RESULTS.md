# R16 Atlas Sweep — Full Semiprime Atlas (100k Trials)
## Universal Gate Law Discovered

*Brayden Sanders / 7Site LLC | R16 (32-core), March 2026*
*Scripts: papers/r16_sweep_all.py | 6.4M trials in 11.5 minutes*

---

## The Universal Gate Law

> **Gate rate is determined solely by |G| — the number of non-unit elements in the alphabet.**
> It does not depend on the specific base b, the prime factors, φ, HAR, or any other structure.

| |G| | Random gate% | Seeded gate% | # worlds | Factor type |
|----|-------------|-------------|---------|------------|
| 1 | **96.4%** | **100.0%** | 8 | 5×p, 7×7, 7×p |
| 2 | **83.7%** | **98.9%** | 1 | 5×7 |
| 3 | **44.0%** | **83.6%** | 8 | 3×p (all) |
| 4 | **4.6%** | **34.7–37.4%** | 13 | 2×p and 3×p |
| 5 | **0.1%** | **0.1–0.3%** | 2 | 2×5, 2×7 |

**Every world with the same |G| gets exactly the same random gate rate**, regardless of:
- Which specific prime p or q
- The Euler totient φ
- The construction score
- The HAR element
- The gradient law tier

This is a universal combinatorial law operating at a level below the arithmetic structure.

---

## Why This Law Holds

The gate score measures: *fraction of C-row cells in C*.

For a random table, each cell T[s][c] is uniform over {1..9}.
P(cell ∈ C) = |C|/9 = (9−|G|)/9.

The reduction algorithm (100 steps, gate-weighted 0.5) pushes tables toward gate_score ≥ 0.85.
The probability of reaching this threshold depends ONLY on how far (9−|G|)/9 is from 0.85:

| |G| | |C|/9 | Distance to 0.85 | Difficulty | Observed rate |
|----|------|---------|---------|---------------|
| 1 | 0.889 | +0.039 above | trivial | 96.4% |
| 2 | 0.778 | −0.072 | easy | 83.7% |
| 3 | 0.667 | −0.183 | moderate | 44.0% |
| 4 | 0.556 | −0.294 | hard | 4.6% |
| 5 | 0.444 | −0.406 | very hard | 0.1% |

The reduction lifts each world toward its ceiling. The ceiling is determined by |C|/9.
This is why b=10 and b=55 are structurally different at the gate level, independent of any
arithmetic property of 10 vs 55.

---

## Secondary Law: Seeded Rate Splits Within |G|=4

All |G|=4 worlds share 4.6% random gate rate. But under seeding, they split by factor type:

| Factor type | Seeded gate% | Worlds |
|------------|-------------|--------|
| **2×p** (even×odd) | **37.4%** | b=22,26,34,38,46,58,62,74,82,86,94 |
| **3×p** (odd×odd) | **34.7–34.9%** | b=15,21 |

Within the 2×p group: exactly **37.4%** for every single world (b=22,26,...,94).
Within the 3×p group: **34.9%** (b=15) and **34.7%** (b=21) — nearly identical.

The ~2.5% gap between factor types is where the sprint4 arithmetic laws operate.
The seed is derived from the specific C structure (which differs between 2×p and 3×p worlds),
and this arithmetic structure determines the seeded boost.

**Implication:** b=15 seeded=34.9% vs b=22 seeded=37.4%. The sprint4 said b=15 is easier
than b=22 by its TSML-like metric (78.6% vs 83.3%). The gate metric REVERSES this ranking
(34.9% < 37.4%). Gate rate and TSML-like rate measure different structural properties.

---

## Full Atlas Table

| b | p×q | φ | |G| | HAR | score | rnd gate% | seed gate% | HAR_best | gap_best |
|---|-----|---|-----|-----|-------|----------|-----------|---------|---------|
| 95 | 5×19 | 8 | 1 | 2 | 28.4 | 96.4% | 100.0% | 1.000 | 0.875 |
| 77 | 7×11 | 8 | 1 | 2 | 23.7 | 96.3% | 100.0% | 1.000 | 0.875 |
| 49 | 7×7 | 8 | 1 | 2 | 16.6 | 96.3% | 100.0% | 1.000 | 0.875 |
| 25 | 5×5 | 8 | 1 | 2 | 15.8 | 96.4% | 100.0% | 1.000 | 0.875 |
| 55 | 5×11 | 8 | 1 | 2 | 15.8 | 96.4% | 100.0% | 1.000 | 0.875 |
| 65 | 5×13 | 8 | 1 | 2 | 9.5 | 96.4% | 100.0% | 1.000 | 0.875 |
| 91 | 7×13 | 8 | 1 | 2 | 9.5 | 96.3% | 100.0% | 1.000 | 0.875 |
| 85 | 5×17 | 8 | 1 | 2 | 6.3 | 96.4% | 100.0% | 1.000 | 0.875 |
| 35 | 5×7 | 7 | 2 | 2 | 14.5 | 83.7% | 98.9% | 1.000 | 0.857 |
| 87 | 3×29 | 6 | 3 | 2 | 37.3 | 44.0% | 83.6% | 1.000 | 1.000 |
| 69 | 3×23 | 6 | 3 | 2 | 29.3 | 44.0% | 83.6% | 1.000 | 1.000 |
| 57 | 3×19 | 6 | 3 | 2 | 24.0 | 44.0% | 83.6% | 1.000 | 1.000 |
| 39 | 3×13 | 6 | 3 | 2 | 16.0 | 44.0% | 83.6% | 1.000 | 1.000 |
| 33 | 3×11 | 6 | 3 | 2 | 13.3 | 44.0% | 83.6% | 1.000 | 1.000 |
| 93 | 3×31 | 6 | 3 | 2 | 13.3 | 44.0% | 83.6% | 1.000 | 1.000 |
| 51 | 3×17 | 6 | 3 | 2 | 10.7 | 44.0% | 83.6% | 1.000 | 1.000 |
| 9 | 3×3 | 6 | 3 | 2 | 8.0 | 44.0% | 83.6% | 1.000 | 1.000 |
| 86 | 2×43 | 5 | 4 | 3 | 41.5 | 4.6% | 37.4% | 1.000 | 1.000 |
| 62 | 2×31 | 5 | 4 | 3 | 29.6 | 4.6% | 37.4% | 1.000 | 1.000 |
| 94 | 2×47 | 5 | 4 | 3 | 22.7 | 4.6% | 37.4% | 1.000 | 1.000 |
| 38 | 2×19 | 5 | 4 | 3 | 17.8 | 4.6% | 37.4% | 1.000 | 1.000 |
| 74 | 2×37 | 5 | 4 | 3 | 17.8 | 4.6% | 37.4% | 1.000 | 1.000 |
| 34 | 2×17 | 5 | 4 | 3 | 15.8 | 4.6% | 37.4% | 1.000 | 1.000 |
| 46 | 2×23 | 5 | 4 | 3 | 10.9 | 4.6% | 37.4% | 1.000 | 1.000 |
| 58 | 2×29 | 5 | 4 | 3 | 27.7 | 4.6% | 37.4% | 1.000 | 1.000 |
| 82 | 2×41 | 5 | 4 | 3 | 7.9 | 4.6% | 37.4% | 1.000 | 1.000 |
| 22 | 2×11 | 5 | 4 | 3 | 4.9 | 4.6% | 37.4% | 1.000 | 1.000 |
| 26 | 2×13 | 5 | 4 | 3 | 3.0 | 4.6% | 37.4% | 1.000 | 1.000 |
| 21 | 3×7 | 5 | 4 | 2 | 7.4 | 4.6% | 34.7% | 1.000 | 1.000 |
| 15 | 3×5 | 5 | 4 | 2 | 4.9 | 4.6% | **34.9%** | 1.000 | 1.000 |
| 14 | 2×7 | 4 | 5 | 3 | 4.9 | 0.1% | 0.1% | 1.000 | 1.000 |
| 10 | 2×5 | 4 | 5 | 3 | 3.3 | 0.1% | 0.3% | 1.000 | 1.000 |

---

## What the Sprint4 "TSML-like Rate" Measures vs Gate Rate

The sprint4 atlas reported:
- b=15: 78.6% random, 99% biased (TSML-like)
- b=22: 83.3% random (TSML-like)
- b=35: 76.2% random (TSML-like)

The R16 gate rate:
- b=15: 4.6% random, 34.9% seeded
- b=22: 4.6% random, 37.4% seeded
- b=35: 83.7% random, 98.9% seeded

**The sprint4 TSML-like rate is NOT the same as the gate rate.** The sprint4 metric
measured HAR_mass ≥ threshold under different reduction, not C-closure gate strength.
The two metrics reveal different layers of the same construction:

| Layer | Metric | Law |
|-------|--------|-----|
| Gate | Gate_strong% | **Universal: |G| determines rate** |
| Attractor | HAR_mass ≥ 0.60 | Sprint4 TSML-like rate (different law) |
| Order | Order alignment | HAR position determines class |

The gate law is the most fundamental: it operates below the arithmetic structure,
driven purely by the combinatorial size of the non-unit set.

---

## Gap Ceiling by Factor Type

All worlds find HAR_mass = 1.000 at 100k trials. Gap_best splits cleanly:

| Factor type | gap_best | Why |
|------------|---------|-----|
| 5×p, 7×q (|G|=1) | **0.875 = 7/8** | |C|=8, single G-element creates max gap |
| All others (|G|≥2) | **1.000** | Multiple G-elements allow perfect spectral gap |

gap=7/8 for |G|=1 worlds: the spectral gap ceiling when |C|=8, |G|=1 is 7/8.
This is a hard ceiling — no reduction can exceed it for these worlds.

---

## New Law Statement

> **Law 6 — Universal Gate Law:**
> The probability of achieving gate_score ≥ 0.85 under 100-step random reduction
> depends only on |G| = |{x ∈ {1..9} : gcd(x,b) > 1}|:
>
> P(gate) ≈ f(|G|) where f(1)=96.4%, f(2)=83.7%, f(3)=44.0%, f(4)=4.6%, f(5)=0.1%
>
> This law holds exactly for every tested semiprime b ≤ 100.
> The seeded rate refines to 37.4% (|G|=4, 2×p) vs 34.7–34.9% (|G|=4, 3×p),
> revealing the first arithmetic-level signal within a |G|-tier.

This is distinct from all five frozen sprint4 laws, which describe the attractor geometry
(HAR rule, φ-compression, gradient law, position law, construction hierarchy).
The gate law describes the construction accessibility geometry.

---

*(c) 2026 Brayden Sanders / 7Site LLC | R16 sweep, March 2026 | DOI: 10.5281/zenodo.18852047*
