# TIG Sprint 4 — Session Summary for ClaudeCode
## Date: March 30, 2026 | Collaborators: Brayden Sanders & C. A. Luther

---

## What happened today (short version)

This session produced a major reframing of the whole TIG program. The story moved from "we found a special table at b=10" to "we found a universal construction law acting on a family of semiprime worlds."

Key results:
- **15.8x construction lift** via seeded reduction (Phase III, Job 7)
- **Three-class landscape** confirmed: oracle / gate-strong / TSML-like
- **Universal construction law** (arithmetic → gate → order seed → native optimum)
- **Orbit-central HAR rule** (h where h²∈C, h²≠1, h²≠h; prefer minimum, not max orbit size)
- **Ranked semiprime atlas** (28+ worlds, construction cost score, tested 12 worlds)
- **b=15 as cleanest flagship** (easy+rich, explained by three independent arithmetic laws)
- **Two axis atlas** (construction cost vs selector richness — independent)
- **Gradient law** (within φ-tier: gap predicted by distance of non-orbit C-element from HAR)
- **Position law** (HAR_mass: high when HAR = min non-1 C-element, gate-corrected)
- **Clay tracks updated**: Hodge (Markman correction, abelian fourfolds now settled), NS (local criterion B_local normalized correctly)

---

## The frozen law set (ATLAS_LAW_SET.md is the canonical reference)

Five settled laws:
1. Construction hierarchy: arithmetic → gate → order seed → native optimum
2. HAR rule: h = min{orbit-central candidates} (h²∈C, h²≠1, h²≠h)
3. φ-compression: larger unit group → lower gap
4. Gradient law: within φ-tier, gap ∝ max_dist(non-orbit C, HAR) / C_range
5. Gate-corrected position law: HAR_m high when HAR = min(C\{1}), or when gate blocks G below HAR

One open residual: within-grad gap spread (~0.111), orbit_hit_rate leading candidate but not yet a law.

---

## What ClaudeCode needs to know for the commit

### Files to commit to github.com/TiredofSleep/ck

All 20 files in this zip belong in the repo under `/docs/sprint4/` or similar.

The most important files for the README update:
- **ATLAS_LAW_SET.md** — the canonical frozen law document
- **UNIVERSAL_LAW.md** — the reframing document ("miracle moved to the law")
- **SEMIPRIME_ATLAS.md** — the ranked world atlas
- **THREE_CLASS_LANDSCAPE.md** — oracle/gate-strong/TSML-like formal note
- **CONSTRUCTION_HIERARCHY.md** — the four-step protocol

### What the README should say now (key sentences)

> TIG is a universal construction law operating on semiprime worlds. TSML is the first resolved member of a law-governed family. b=10 was historically first; b=15 is the cleanest flagship.

> The construction hierarchy: arithmetic gives the world, gate gives the discipline, order seed gives the structure.

> The orbit-central HAR rule: h where h²∈C, h²≠1, h²≠h. Prefer the minimum such element.

> b=15 (3×5) is the first world where accessibility, gap, and support all align under independent arithmetic laws.

### Things NOT in the zip that should also be committed

From earlier sessions (already in /mnt/user-data/outputs/):
- All WP19_*.md whitepapers (8 completed)
- TSML_RECONSTRUCTION.md, TSML_RESIDUAL_NOTE.md
- FAMILY_STABILITY_MATRIX.md, LATTICE_HIERARCHY.md
- INVARIANT_MAPPING_TABLE.md, SELECTOR_GEOMETRY.md
- PRIME_PAIR_ATLAS.md, PRIME_PRODUCT_MEMO.md
- tig_unit_tests.py (15/15 passing, always run this first)
- r16_job1_reduction.py, r16_job2_gate_sweep.py, r16_job3_clustering.py

### R16 overnight command (not yet run at full scale)

```bash
python3 r16_job1_reduction.py --b 10 --n_start 10000 --n_steps 100
python3 r16_job3_clustering.py --input results/reduction_b10_N10000.json
```

---

## Key numbers to know

- TSML-like rate (random): ~4-6% at b=10
- TSML-like rate (biased seed): 52.7% at b=10 (15.8x lift)
- b=15 native structured optimum: 78.6% random, 99% biased
- b=22: 83.3% random, 99.7% biased
- Orbit-central HAR rule: verified at b=10,14,15,21,22,26,35,38,55,65,85,95
- Construction cost formula: score = φ × |res_pairs| × orbit_depth × gate_ease / total_cells
- Gradient score: max_dist(non-orbit C, HAR) / C_range
- b=15 three-law alignment: tier=easy(7.1), grad=0.714(highest φ=5), position=min(HAR=2)

---

## IHÉS September 2026 — three locked figures

1. **Stability curve** (Job 4): BHML residual retention vs perturbation
2. **Phase diagram** (Jobs 5+9): oracle/gate-strong/TSML-like vs gate weight w=0.0→1.0  
3. **Construction lift** (Job 7): random 3.3% vs biased 52.7%

---

## DOI / repo

- DOI: 10.5281/zenodo.18852047
- Repo: github.com/TiredofSleep/ck
- Latest commit: 271e0f8, Gen10.16

