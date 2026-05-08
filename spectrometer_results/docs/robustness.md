# Robustness / Ablation Report

**Date**: 2026-03-01T09:17:12.380509
**Configurations**: 13

## Overview

- **Total configurations**: 13
- **Fine-robust**: 13 (skeleton survived >= 75% of perturbations)
- **Macro-robust**: 13 (macro class survived >= 75% of perturbations)
- **Fragile**: 0

## Survival Rates

| Problem | Regime | Skeleton | Trials | Preserved | Survival | Robust | Macro | Macro Survival | Macro Robust |
|---------|--------|----------|--------|-----------|----------|--------|-------|----------------|--------------|
| bsd | calibration | frozen | 114 | 113 | 99% | YES | 113 | 99% | YES |
| bsd | frontier | frozen | 114 | 113 | 99% | YES | 113 | 99% | YES |
| hodge | calibration | stable | 114 | 72 | 63% | YES | 113 | 99% | YES |
| hodge | frontier | bounded | 114 | 102 | 89% | YES | 102 | 89% | YES |
| navier_stokes | calibration | oscillating | 115 | 113 | 98% | YES | 114 | 99% | YES |
| navier_stokes | frontier | bounded | 115 | 110 | 96% | YES | 113 | 98% | YES |
| p_vs_np | calibration | frozen | 115 | 114 | 99% | YES | 114 | 99% | YES |
| p_vs_np | frontier | bounded | 115 | 114 | 99% | YES | 114 | 99% | YES |
| riemann | calibration | stable | 116 | 111 | 96% | YES | 115 | 99% | YES |
| riemann | frontier | oscillating | 116 | 89 | 77% | YES | 107 | 92% | YES |
| riemann | frontier | stable | 116 | 115 | 99% | YES | 115 | 99% | YES |
| yang_mills | calibration | stable | 115 | 113 | 98% | YES | 114 | 99% | YES |
| yang_mills | frontier | frozen | 115 | 114 | 99% | YES | 114 | 99% | YES |

## Per-Perturbation-Type Breakdown

### Tig Permutation

| Problem | Regime | Trials | Preserved | Breaks |
|---------|--------|--------|-----------|--------|
| bsd | calibration | 5 | 5 | 0 |
| bsd | frontier | 5 | 5 | 0 |
| hodge | calibration | 5 | 5 | 0 |
| hodge | frontier | 5 | 5 | 0 |
| navier_stokes | calibration | 5 | 5 | 0 |
| navier_stokes | frontier | 5 | 5 | 0 |
| p_vs_np | calibration | 5 | 5 | 0 |
| p_vs_np | frontier | 5 | 5 | 0 |
| riemann | calibration | 5 | 5 | 0 |
| riemann | frontier | 5 | 5 | 0 |
| riemann | frontier | 5 | 5 | 0 |
| yang_mills | calibration | 5 | 5 | 0 |
| yang_mills | frontier | 5 | 5 | 0 |

### Generator Jitter

| Problem | Regime | Trials | Preserved | Breaks |
|---------|--------|--------|-----------|--------|
| bsd | calibration | 4 | 4 | 0 |
| bsd | frontier | 4 | 4 | 0 |
| hodge | calibration | 4 | 3 | 1 |
| hodge | frontier | 4 | 4 | 0 |
| navier_stokes | calibration | 4 | 3 | 1 |
| navier_stokes | frontier | 4 | 4 | 0 |
| p_vs_np | calibration | 4 | 4 | 0 |
| p_vs_np | frontier | 4 | 4 | 0 |
| riemann | calibration | 4 | 4 | 0 |
| riemann | frontier | 4 | 4 | 0 |
| riemann | frontier | 4 | 4 | 0 |
| yang_mills | calibration | 4 | 3 | 1 |
| yang_mills | frontier | 4 | 4 | 0 |

### Channel Ablation

| Problem | Regime | Trials | Preserved | Breaks |
|---------|--------|--------|-----------|--------|
| bsd | calibration | 3 | 3 | 0 |
| bsd | frontier | 3 | 3 | 0 |
| hodge | calibration | 3 | 3 | 0 |
| hodge | frontier | 3 | 3 | 0 |
| navier_stokes | calibration | 4 | 4 | 0 |
| navier_stokes | frontier | 4 | 4 | 0 |
| p_vs_np | calibration | 4 | 4 | 0 |
| p_vs_np | frontier | 4 | 4 | 0 |
| riemann | calibration | 5 | 5 | 0 |
| riemann | frontier | 5 | 5 | 0 |
| riemann | frontier | 5 | 5 | 0 |
| yang_mills | calibration | 4 | 4 | 0 |
| yang_mills | frontier | 4 | 4 | 0 |

### Noise Distribution

| Problem | Regime | Trials | Preserved | Breaks |
|---------|--------|--------|-----------|--------|
| bsd | calibration | 3 | 2 | 1 |
| bsd | frontier | 3 | 2 | 1 |
| hodge | calibration | 3 | 2 | 1 |
| hodge | frontier | 3 | 2 | 1 |
| navier_stokes | calibration | 3 | 2 | 1 |
| navier_stokes | frontier | 3 | 0 | 3 |
| p_vs_np | calibration | 3 | 2 | 1 |
| p_vs_np | frontier | 3 | 2 | 1 |
| riemann | calibration | 3 | 0 | 3 |
| riemann | frontier | 3 | 2 | 1 |
| riemann | frontier | 3 | 2 | 1 |
| yang_mills | calibration | 3 | 2 | 1 |
| yang_mills | frontier | 3 | 2 | 1 |

### Multi Seed

| Problem | Regime | Trials | Preserved | Breaks |
|---------|--------|--------|-----------|--------|
| bsd | calibration | 99 | 99 | 0 |
| bsd | frontier | 99 | 99 | 0 |
| hodge | calibration | 99 | 59 | 40 |
| hodge | frontier | 99 | 88 | 11 |
| navier_stokes | calibration | 99 | 99 | 0 |
| navier_stokes | frontier | 99 | 97 | 2 |
| p_vs_np | calibration | 99 | 99 | 0 |
| p_vs_np | frontier | 99 | 99 | 0 |
| riemann | calibration | 99 | 97 | 2 |
| riemann | frontier | 99 | 73 | 26 |
| riemann | frontier | 99 | 99 | 0 |
| yang_mills | calibration | 99 | 99 | 0 |
| yang_mills | frontier | 99 | 99 | 0 |

## Skeleton Breaks (Perturbations That Changed Class)

| Problem | Regime | Perturbation | Baseline | Perturbed | Delta Shift | Entropy Shift |
|---------|--------|--------------|----------|-----------|-------------|---------------|
| navier_stokes | calibration | jitter_50pct | oscillating | bounded | +0.2984 | -0.0780 |
| navier_stokes | calibration | cauchy_sigma=0.1 | oscillating | wild | -0.0944 | +0.4482 |
| navier_stokes | frontier | uniform_sigma=0.1 | bounded | stable | -0.0447 | +0.6553 |
| navier_stokes | frontier | cauchy_sigma=0.1 | bounded | oscillating | +0.0063 | +0.5400 |
| navier_stokes | frontier | uniform_sigma=0.30 | bounded | frozen | -0.0457 | -0.4433 |
| navier_stokes | frontier | seed_32 | bounded | oscillating | +0.0083 | +0.1475 |
| navier_stokes | frontier | seed_38 | bounded | oscillating | +0.0069 | +0.1439 |
| p_vs_np | calibration | cauchy_sigma=0.1 | frozen | wild | -0.2840 | +0.2168 |
| p_vs_np | frontier | cauchy_sigma=0.1 | bounded | wild | +0.2840 | +0.0429 |
| riemann | calibration | uniform_sigma=0.1 | stable | frozen | -0.0052 | +0.8670 |
| riemann | calibration | cauchy_sigma=0.1 | stable | oscillating | +0.5415 | -0.1744 |
| riemann | calibration | uniform_sigma=0.30 | stable | frozen | -0.0052 | -0.2316 |
| riemann | calibration | seed_6 | stable | frozen | +0.0009 | -0.1364 |
| riemann | calibration | seed_14 | stable | frozen | -0.0012 | -0.1170 |
| riemann | frontier | cauchy_sigma=0.1 | oscillating | wild | +0.4603 | -0.1077 |
| riemann | frontier | seed_2 | oscillating | bounded | -0.0482 | -0.1208 |
| riemann | frontier | seed_5 | oscillating | bounded | -0.0082 | -0.2147 |
| riemann | frontier | seed_6 | oscillating | wild | +0.0789 | +0.1066 |
| riemann | frontier | seed_7 | oscillating | bounded | -0.0032 | -0.1281 |
| riemann | frontier | seed_12 | oscillating | wild | +0.0121 | +0.2038 |
| riemann | frontier | seed_13 | oscillating | bounded | -0.0284 | -0.1261 |
| riemann | frontier | seed_21 | oscillating | bounded | +0.0122 | -0.2031 |
| riemann | frontier | seed_23 | oscillating | wild | -0.0161 | +0.2754 |
| riemann | frontier | seed_30 | oscillating | bounded | -0.0096 | -0.1828 |
| riemann | frontier | seed_32 | oscillating | wild | +0.0456 | +0.4016 |
| riemann | frontier | seed_37 | oscillating | bounded | +0.0087 | -0.1930 |
| riemann | frontier | seed_38 | oscillating | wild | +0.0527 | +0.1350 |
| riemann | frontier | seed_51 | oscillating | bounded | +0.0445 | -0.1562 |
| riemann | frontier | seed_53 | oscillating | bounded | -0.0009 | -0.1894 |
| riemann | frontier | seed_55 | oscillating | wild | -0.0466 | +0.5223 |
| riemann | frontier | seed_58 | oscillating | bounded | +0.0338 | -0.1481 |
| riemann | frontier | seed_59 | oscillating | wild | +0.0208 | +0.0945 |
| riemann | frontier | seed_71 | oscillating | bounded | -0.0722 | -0.1297 |
| riemann | frontier | seed_72 | oscillating | bounded | +0.0330 | -0.1560 |
| riemann | frontier | seed_77 | oscillating | bounded | -0.0149 | -0.1703 |
| riemann | frontier | seed_85 | oscillating | bounded | -0.0057 | -0.1328 |
| riemann | frontier | seed_87 | oscillating | wild | -0.0011 | +0.3816 |
| riemann | frontier | seed_91 | oscillating | bounded | -0.0171 | -0.1537 |
| riemann | frontier | seed_92 | oscillating | bounded | -0.0376 | -0.1493 |
| riemann | frontier | seed_95 | oscillating | bounded | -0.0057 | -0.1439 |
| riemann | frontier | seed_100 | oscillating | bounded | -0.0745 | -0.0447 |
| riemann | frontier | cauchy_sigma=0.1 | stable | oscillating | +0.3569 | +0.0644 |
| yang_mills | calibration | jitter_50pct | stable | frozen | +0.9198 | -0.0072 |
| yang_mills | calibration | cauchy_sigma=0.1 | stable | wild | +0.4252 | +0.6858 |
| yang_mills | frontier | uniform_sigma=0.30 | frozen | oscillating | -0.1872 | +0.0174 |
| bsd | calibration | cauchy_sigma=0.1 | frozen | wild | +0.5622 | +0.3486 |
| bsd | frontier | cauchy_sigma=0.1 | frozen | wild | +0.2691 | +0.1894 |
| hodge | calibration | jitter_50pct | stable | frozen | -0.0097 | +0.0000 |
| hodge | calibration | cauchy_sigma=0.1 | stable | wild | +0.1095 | +1.0939 |
| hodge | calibration | seed_2 | stable | frozen | -0.0002 | -0.0037 |
| hodge | calibration | seed_5 | stable | frozen | -0.0005 | -0.0047 |
| hodge | calibration | seed_7 | stable | frozen | -0.0004 | -0.0036 |
| hodge | calibration | seed_9 | stable | frozen | -0.0000 | -0.0032 |
| hodge | calibration | seed_10 | stable | frozen | +0.0002 | -0.0041 |
| hodge | calibration | seed_15 | stable | frozen | -0.0001 | -0.0039 |
| hodge | calibration | seed_16 | stable | frozen | -0.0000 | -0.0032 |
| hodge | calibration | seed_17 | stable | frozen | +0.0002 | -0.0039 |
| hodge | calibration | seed_20 | stable | frozen | -0.0002 | -0.0038 |
| hodge | calibration | seed_21 | stable | frozen | -0.0004 | -0.0035 |
| hodge | calibration | seed_28 | stable | frozen | +0.0002 | -0.0026 |
| hodge | calibration | seed_30 | stable | frozen | -0.0003 | -0.0031 |
| hodge | calibration | seed_33 | stable | frozen | -0.0001 | -0.0040 |
| hodge | calibration | seed_37 | stable | frozen | -0.0004 | -0.0040 |
| hodge | calibration | seed_39 | stable | frozen | +0.0002 | -0.0035 |
| hodge | calibration | seed_41 | stable | frozen | +0.0001 | -0.0042 |
| hodge | calibration | seed_43 | stable | frozen | -0.0001 | -0.0045 |
| hodge | calibration | seed_44 | stable | frozen | +0.0000 | -0.0037 |
| hodge | calibration | seed_45 | stable | frozen | -0.0003 | -0.0026 |
| hodge | calibration | seed_46 | stable | frozen | -0.0002 | -0.0044 |
| hodge | calibration | seed_48 | stable | frozen | +0.0004 | -0.0042 |
| hodge | calibration | seed_50 | stable | frozen | -0.0002 | -0.0045 |
| hodge | calibration | seed_52 | stable | frozen | +0.0000 | -0.0034 |
| hodge | calibration | seed_53 | stable | frozen | -0.0006 | -0.0045 |
| hodge | calibration | seed_55 | stable | frozen | +0.0007 | -0.0031 |
| hodge | calibration | seed_58 | stable | frozen | -0.0001 | -0.0035 |
| hodge | calibration | seed_65 | stable | frozen | +0.0001 | -0.0035 |
| hodge | calibration | seed_67 | stable | frozen | -0.0000 | -0.0034 |
| hodge | calibration | seed_71 | stable | frozen | +0.0001 | -0.0035 |
| hodge | calibration | seed_75 | stable | frozen | +0.0001 | -0.0041 |
| hodge | calibration | seed_77 | stable | frozen | -0.0004 | -0.0044 |
| hodge | calibration | seed_81 | stable | frozen | +0.0002 | -0.0015 |
| hodge | calibration | seed_82 | stable | frozen | -0.0002 | -0.0029 |
| hodge | calibration | seed_85 | stable | frozen | -0.0004 | -0.0041 |
| hodge | calibration | seed_91 | stable | frozen | -0.0004 | -0.0041 |
| hodge | calibration | seed_95 | stable | frozen | -0.0003 | -0.0035 |
| hodge | calibration | seed_96 | stable | frozen | +0.0001 | -0.0035 |
| hodge | calibration | seed_97 | stable | frozen | +0.0006 | -0.0027 |
| hodge | calibration | seed_98 | stable | frozen | -0.0005 | -0.0044 |
| hodge | calibration | seed_99 | stable | frozen | -0.0001 | -0.0038 |
| hodge | frontier | cauchy_sigma=0.1 | bounded | wild | -0.1885 | +0.8239 |
| hodge | frontier | seed_2 | bounded | stable | +0.0140 | -0.0060 |
| hodge | frontier | seed_5 | bounded | stable | +0.0024 | -0.0059 |
| hodge | frontier | seed_21 | bounded | stable | -0.0025 | -0.0059 |
| hodge | frontier | seed_37 | bounded | stable | -0.0015 | -0.0059 |
| hodge | frontier | seed_39 | bounded | stable | +0.0202 | -0.0059 |
| hodge | frontier | seed_53 | bounded | stable | +0.0013 | -0.0063 |
| hodge | frontier | seed_67 | bounded | stable | -0.0106 | -0.0058 |
| hodge | frontier | seed_71 | bounded | stable | +0.0195 | -0.0059 |
| hodge | frontier | seed_77 | bounded | stable | +0.0041 | -0.0054 |
| hodge | frontier | seed_85 | bounded | stable | +0.0025 | -0.0052 |
| hodge | frontier | seed_98 | bounded | stable | +0.0012 | -0.0057 |

## Robust Patterns -- Fine (The "Deeper Code")

These skeleton classifications survived all five perturbation types:

- **navier_stokes (calibration)**: OSCILLATING (98% survival)
- **navier_stokes (frontier)**: BOUNDED (96% survival)
- **p_vs_np (calibration)**: FROZEN (99% survival)
- **p_vs_np (frontier)**: BOUNDED (99% survival)
- **riemann (calibration)**: STABLE (96% survival)
- **riemann (frontier)**: OSCILLATING (77% survival)
- **riemann (frontier)**: STABLE (99% survival)
- **yang_mills (calibration)**: STABLE (98% survival)
- **yang_mills (frontier)**: FROZEN (99% survival)
- **bsd (calibration)**: FROZEN (99% survival)
- **bsd (frontier)**: FROZEN (99% survival)
- **hodge (calibration)**: STABLE (63% survival)
- **hodge (frontier)**: BOUNDED (89% survival)

## Robust Patterns -- Macro

These macro classifications survived all five perturbation types:

- **navier_stokes (calibration)**: OSCILLATING (99% macro survival)
- **navier_stokes (frontier)**: BOUNDED (98% macro survival)
- **p_vs_np (calibration)**: FROZEN (99% macro survival)
- **p_vs_np (frontier)**: BOUNDED (99% macro survival)
- **riemann (calibration)**: STABLE (99% macro survival)
- **riemann (frontier)**: OSCILLATING (92% macro survival)
- **riemann (frontier)**: STABLE (99% macro survival)
- **yang_mills (calibration)**: STABLE (99% macro survival)
- **yang_mills (frontier)**: FROZEN (99% macro survival)
- **bsd (calibration)**: FROZEN (99% macro survival)
- **bsd (frontier)**: FROZEN (99% macro survival)
- **hodge (calibration)**: STABLE (99% macro survival)
- **hodge (frontier)**: BOUNDED (89% macro survival)

---
_Generated 2026-03-01T09:17:12.381216 by Robustness Sweep v1.0_
_Features that survive all perturbations are the "deeper code."_