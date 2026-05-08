# Governing Equations: Coherence Manifold

**Date**: 2026-03-01T10:38:03.073134
**Equations extracted**: 83

## Overview

- **Affirmative** (delta -> 0): 18
- **Gap** (delta -> eta > 0): 50
- **Indeterminate**: 15

## Summary Table

| Problem | Regime | Best Model | R^2 | BIC | Asymptotic | delta(inf) | Confidence | LaTeX |
|---------|--------|------------|-----|-----|------------|------------|------------|-------|
| abc | calibration | power_law | 0.9489 | -305.2 | affirmative | 0.000000 | 0.06 | `\delta(L) = 0.0447 \cdot L^{-0.2344}` |
| abc | frontier | constant | 1.0000 | -1584.6 | gap | 0.428571 | 0.15 | `\delta(L) = 0.4286` |
| banach_tarski | calibration | constant | 1.0000 | -1584.6 | affirmative | 0.000000 | 0.15 | `\delta(L) = 0.0000` |
| banach_tarski | frontier | constant | 1.0000 | -1584.6 | gap | 1.000000 | 0.15 | `\delta(L) = 1.0000` |
| bridge_expander | calibration | damped_osc | 0.6313 | -95.7 | gap | 0.300922 | 0.02 | `\delta(L) = 0.3030 e^{-0.0535 L} \cos(0.3802 L + 0.0735) + 0.3009` |
| bridge_expander | frontier | exp_decay | 0.9583 | -211.5 | gap | 0.782552 | 0.22 | `\delta(L) = -0.1803 e^{-0.1506 L} + 0.7826` |
| bridge_fractal | calibration | pure_osc | 0.4399 | -458.1 | indeterminate | 0.000036 | 0.15 | `\delta(L) = 0.0000 \cos(2.0242 L + 0.1453) + 0.0000` |
| bridge_fractal | frontier | pure_osc | 0.9607 | -205.9 | indeterminate | 0.048859 | 0.14 | `\delta(L) = 0.0469 \cos(0.4837 L + 1.3698) + 0.0489` |
| bridge_rmt | calibration | pure_osc | 0.4436 | -387.4 | indeterminate | 0.000189 | 0.16 | `\delta(L) = 0.0001 \cos(2.0115 L + 0.3353) + 0.0002` |
| bridge_rmt | frontier | pure_osc | 0.4443 | -308.6 | indeterminate | 0.001129 | 0.15 | `\delta(L) = 0.0009 \cos(2.0154 L + 0.2563) + 0.0011` |
| bridge_spectral | calibration | exp_decay | 0.9994 | -290.1 | gap | 0.928021 | 0.31 | `\delta(L) = -0.2382 e^{-0.1016 L} + 0.9280` |
| bridge_spectral | frontier | exp_decay | 0.9993 | -295.6 | gap | 0.939841 | 0.31 | `\delta(L) = -0.1985 e^{-0.1019 L} + 0.9398` |
| bsd_avg_rank | calibration | constant | 1.0000 | -1584.6 | affirmative | 0.000000 | 0.15 | `\delta(L) = 0.0000` |
| bsd_avg_rank | frontier | pure_osc | 0.5299 | -35.5 | indeterminate | 0.392789 | 0.09 | `\delta(L) = 0.5209 \cos(2.2237 L + -1.6119) + 0.3928` |
| bsd | calibration | constant | 1.0000 | -1584.6 | affirmative | 0.000000 | 0.15 | `\delta(L) = 0.0000` |
| bsd | frontier | constant | 1.0000 | -1584.6 | gap | 1.300000 | 0.15 | `\delta(L) = 1.3000` |
| bsd_function_field | calibration | constant | 1.0000 | -1584.6 | affirmative | 0.000000 | 0.15 | `\delta(L) = 0.0000` |
| bsd_function_field | frontier | constant | 1.0000 | -1584.6 | affirmative | 0.000000 | 0.15 | `\delta(L) = 0.0000` |
| bsd_sato_tate | calibration | constant | 1.0000 | -1584.6 | affirmative | 0.000000 | 0.15 | `\delta(L) = 0.0000` |
| bsd_sato_tate | frontier | constant | 1.0000 | -1584.6 | affirmative | 0.000000 | 0.15 | `\delta(L) = 0.0000` |
| collatz | calibration | constant | 1.0000 | -1584.6 | affirmative | 0.000000 | 0.15 | `\delta(L) = 0.0000` |
| collatz | frontier | linear | 0.3099 | -257.5 | affirmative | 0.000000 | 0.07 | `\delta(L) = -0.0003 L + 0.0404` |
| continuum | calibration | constant | 1.0000 | -1584.6 | affirmative | 0.000000 | 0.15 | `\delta(L) = 0.0000` |
| continuum | frontier | exp_decay | 0.9382 | -150.7 | gap | 0.857038 | 0.15 | `\delta(L) = -0.5546 e^{-0.1287 L} + 0.8570` |
| cosmo_constant | calibration | power_law | 0.9994 | -399.4 | gap | inf | 1.00 | `\delta(L) = 0.5560 \cdot L^{0.0124}` |
| cosmo_constant | frontier | constant | 0.0000 | -594.2 | gap | 0.982436 | 0.14 | `\delta(L) = 0.9824` |
| falconer | calibration | constant | 1.0000 | -1584.6 | affirmative | 0.000000 | 0.15 | `\delta(L) = 0.0000` |
| falconer | frontier | constant | 0.0000 | -332.0 | affirmative | 0.000290 | 0.14 | `\delta(L) = 0.0003` |
| hodge | calibration | pure_osc | 0.4442 | -326.5 | indeterminate | 0.020750 | 0.15 | `\delta(L) = 0.0006 \cos(2.0160 L + 0.2443) + 0.0207` |
| hodge | frontier | constant | 0.0000 | -171.1 | gap | 0.603552 | 0.09 | `\delta(L) = 0.6036` |
| hodge_standard | calibration | pure_osc | 0.4443 | -255.6 | indeterminate | 0.083766 | 0.15 | `\delta(L) = 0.0029 \cos(2.0156 L + 0.2520) + 0.0838` |
| hodge_standard | frontier | linear | 0.9942 | -210.4 | gap | inf | 0.18 | `\delta(L) = 0.0150 L + 0.3437` |
| hodge_tate | calibration | pure_osc | 0.4443 | -255.6 | indeterminate | 0.053766 | 0.15 | `\delta(L) = 0.0029 \cos(2.0156 L + 0.2520) + 0.0538` |
| hodge_tate | frontier | linear | 0.9977 | -218.4 | gap | inf | 0.18 | `\delta(L) = 0.0200 L + 0.2873` |
| hodge_transcendental | calibration | linear | 0.9942 | -228.2 | gap | inf | 0.18 | `\delta(L) = 0.0100 L + 0.1958` |
| hodge_transcendental | frontier | linear | 0.9949 | -200.6 | gap | inf | 0.18 | `\delta(L) = 0.0200 L + 0.4909` |
| info_paradox | calibration | damped_osc | 1.0000 | -386.4 | indeterminate | 0.425907 | 1.00 | `\delta(L) = 0.2175 e^{0.0010 L} \cos(0.0171 L + 1.2075) + 0.4259` |
| info_paradox | frontier | linear | 0.9998 | -239.7 | affirmative | 0.000000 | 1.00 | `\delta(L) = -0.0415 L + 1.0503` |
| inverse_galois | calibration | constant | 0.0000 | -307.6 | gap | 0.049840 | 0.09 | `\delta(L) = 0.0498` |
| inverse_galois | frontier | constant | 0.0000 | -201.6 | gap | 0.698224 | 0.09 | `\delta(L) = 0.6982` |
| jacobian | calibration | constant | 0.0000 | -285.1 | gap | 0.049734 | 0.09 | `\delta(L) = 0.0497` |
| jacobian | frontier | constant | 0.0000 | -201.6 | gap | 0.398224 | 0.09 | `\delta(L) = 0.3982` |
| langlands | calibration | constant | 0.0000 | -285.1 | gap | 0.149734 | 0.09 | `\delta(L) = 0.1497` |
| langlands | frontier | constant | 0.0000 | -201.6 | gap | 0.498224 | 0.09 | `\delta(L) = 0.4982` |
| navier_stokes | calibration | pure_osc | 0.9971 | -231.5 | indeterminate | 0.399469 | 0.14 | `\delta(L) = 0.1035 \cos(0.6978 L + 0.8933) + 0.3995` |
| navier_stokes | frontier | damped_osc | 0.9994 | -328.4 | gap | 0.010079 | 1.00 | `\delta(L) = 0.9825 e^{-0.7562 L} \cos(0.5348 L + -2.4548) + 0.0101` |
| ns_2d | calibration | constant | 0.0000 | -262.6 | gap | 0.299556 | 0.09 | `\delta(L) = 0.2996` |
| ns_2d | frontier | pure_osc | 0.9963 | -197.1 | indeterminate | 0.498095 | 0.15 | `\delta(L) = 0.2017 \cos(0.9992 L + 2.1249) + 0.4981` |
| ns_euler | calibration | constant | 0.0000 | -232.1 | gap | 0.499112 | 0.09 | `\delta(L) = 0.4991` |
| ns_euler | frontier | constant | 0.0000 | -201.6 | gap | 0.198224 | 0.09 | `\delta(L) = 0.1982` |
| ns_sqg | calibration | damped_osc | 0.9979 | -238.7 | gap | 0.449300 | 0.09 | `\delta(L) = 0.1075 e^{-0.0039 L} \cos(0.5014 L + 2.6304) + 0.4493` |
| ns_sqg | frontier | damped_osc | 0.9780 | -184.5 | gap | 0.698571 | 0.24 | `\delta(L) = 0.1206 e^{-0.0159 L} \cos(0.7867 L + 0.8747) + 0.6986` |
| p_vs_np | calibration | constant | 1.0000 | -1584.6 | gap | 0.750000 | 0.15 | `\delta(L) = 0.7500` |
| p_vs_np | frontier | exp_decay | 0.8925 | -171.0 | gap | 0.851637 | 0.10 | `\delta(L) = -0.3430 e^{-0.2252 L} + 0.8516` |
| pnp_ac0 | calibration | pure_osc | 0.9927 | -195.9 | indeterminate | 0.163027 | 1.00 | `\delta(L) = 0.1350 \cos(0.1738 L + 2.2453) + 0.1630` |
| pnp_ac0 | frontier | constant | 1.0000 | -1584.6 | affirmative | 0.000000 | 0.15 | `\delta(L) = 0.0000` |
| pnp_bpp | calibration | constant | 0.0000 | -262.6 | gap | 0.049556 | 0.09 | `\delta(L) = 0.0496` |
| pnp_bpp | frontier | constant | 1.0000 | -1584.6 | gap | 0.050000 | 0.15 | `\delta(L) = 0.0500` |
| pnp_clique | calibration | pure_osc | 0.8860 | -197.2 | indeterminate | 0.031673 | 0.15 | `\delta(L) = -0.0322 \cos(0.5037 L + 0.9503) + 0.0317` |
| pnp_clique | frontier | constant | 1.0000 | -1584.6 | affirmative | 0.000000 | 0.15 | `\delta(L) = 0.0000` |
| poincare_4d | calibration | constant | 1.0000 | -1584.6 | affirmative | 0.000000 | 0.15 | `\delta(L) = 0.0000` |
| poincare_4d | frontier | constant | 1.0000 | -1584.6 | gap | 0.400000 | 0.15 | `\delta(L) = 0.4000` |
| ramsey | calibration | exp_decay | 0.9962 | -210.8 | gap | 0.495984 | 0.31 | `\delta(L) = 0.5687 e^{-0.1074 L} + 0.4960` |
| ramsey | frontier | constant | 1.0000 | -1584.6 | gap | 1.000000 | 0.15 | `\delta(L) = 1.0000` |
| rh_dirichlet | calibration | constant | 0.0000 | -293.1 | gap | 0.505222 | 0.09 | `\delta(L) = 0.5052` |
| rh_dirichlet | frontier | constant | 0.0000 | -241.9 | gap | 0.420710 | 0.14 | `\delta(L) = 0.4207` |
| rh_fake | calibration | constant | 0.0000 | -241.9 | gap | 0.350710 | 0.14 | `\delta(L) = 0.3507` |
| rh_fake | frontier | constant | 0.0000 | -188.4 | gap | 0.272397 | 0.09 | `\delta(L) = 0.2724` |
| rh_function_field | calibration | constant | 0.0000 | -312.2 | gap | 0.902144 | 0.09 | `\delta(L) = 0.9021` |
| rh_function_field | frontier | constant | 0.0000 | -293.1 | gap | 0.855222 | 0.09 | `\delta(L) = 0.8552` |
| riemann | calibration | constant | 0.0000 | -262.3 | gap | 0.005495 | 0.14 | `\delta(L) = 0.0055` |
| riemann | frontier | constant | 0.0000 | -93.8 | gap | 0.242772 | 0.15 | `\delta(L) = 0.2428` |
| riemann | frontier | pure_osc | 0.9961 | -325.9 | indeterminate | 0.087808 | 0.06 | `\delta(L) = 0.0099 \cos(0.5078 L + 0.9677) + 0.0878` |
| twin_primes | calibration | constant | 1.0000 | -1584.6 | affirmative | 0.000000 | 0.15 | `\delta(L) = 0.0000` |
| twin_primes | frontier | constant | 1.0000 | -1584.6 | gap | 1.000000 | 0.15 | `\delta(L) = 1.0000` |
| yang_mills | calibration | constant | 0.0000 | -262.7 | gap | 0.079577 | 0.09 | `\delta(L) = 0.0796` |
| yang_mills | frontier | constant | 1.0000 | -1584.6 | gap | 1.000000 | 0.15 | `\delta(L) = 1.0000` |
| ym_lattice | calibration | constant | 0.0000 | -210.5 | gap | 0.320153 | 0.13 | `\delta(L) = 0.3202` |
| ym_lattice | frontier | constant | 1.0000 | -1584.6 | gap | 1.000000 | 0.15 | `\delta(L) = 1.0000` |
| ym_phi4 | calibration | constant | 0.0000 | -281.1 | gap | 0.159745 | 0.14 | `\delta(L) = 0.1597` |
| ym_phi4 | frontier | pure_osc | 0.9676 | -175.5 | indeterminate | 0.550307 | 0.15 | `\delta(L) = 0.1081 \cos(1.0013 L + 0.5754) + 0.5503` |
| ym_schwinger | calibration | constant | 0.0000 | -58.1 | gap | 0.377696 | 0.13 | `\delta(L) = 0.3777` |
| ym_schwinger | frontier | constant | 0.0000 | -198.0 | gap | 0.538804 | 0.08 | `\delta(L) = 0.5388` |

## Per-Problem Equations

### Abc

**Calibration** (low_quality)

- Best model: **power_law**
- Equation: `\delta(L) = 0.0447 \cdot L^{-0.2344}`
- Asymptotic class: **affirmative**
- delta(L -> inf) = 0.000000
- R^2 = 0.948923
- BIC = -305.18
- Confidence = 0.06

| Model | R^2 | BIC | Params | Converged |
|-------|-----|-----|--------|-----------|
| constant | 0.0000 | -242.8 | 1 | yes |
| linear | 0.8381 | -279.8 | 2 | yes |
| power_law * | 0.9489 | -305.2 | 2 | yes |
| exp_decay | 0.9530 | -303.9 | 3 | yes |
| damped_osc | 0.9530 | -297.7 | 5 | yes |
| pure_osc | 0.9495 | -299.3 | 4 | NO |

**Frontier** (high_quality)

- Best model: **constant**
- Equation: `\delta(L) = 0.4286`
- Asymptotic class: **gap**
- delta(L -> inf) = 0.428571
- R^2 = 1.000000
- BIC = -1584.62
- Confidence = 0.15

| Model | R^2 | BIC | Params | Converged |
|-------|-----|-----|--------|-----------|
| constant * | 1.0000 | -1584.6 | 1 | yes |
| linear | 1.0000 | -1581.5 | 2 | yes |
| power_law | 1.0000 | -1581.5 | 2 | yes |
| exp_decay | 0.0000 | -580.4 | 3 | yes |
| damped_osc | 0.0000 | -574.1 | 5 | yes |
| pure_osc | 0.0000 | -590.5 | 4 | yes |

### Banach Tarski

**Calibration** (dimension_2)

- Best model: **constant**
- Equation: `\delta(L) = 0.0000`
- Asymptotic class: **affirmative**
- delta(L -> inf) = 0.000000
- R^2 = 1.000000
- BIC = -1584.62
- Confidence = 0.15

| Model | R^2 | BIC | Params | Converged |
|-------|-----|-----|--------|-----------|
| constant * | 1.0000 | -1584.6 | 1 | yes |
| linear | 1.0000 | -1581.5 | 2 | yes |
| power_law | 1.0000 | -1581.5 | 2 | NO |
| exp_decay | 0.0000 | -580.4 | 3 | yes |
| damped_osc | 0.0000 | -585.2 | 5 | yes |
| pure_osc | 0.0000 | -585.5 | 4 | yes |

**Frontier** (dimension_3)

- Best model: **constant**
- Equation: `\delta(L) = 1.0000`
- Asymptotic class: **gap**
- delta(L -> inf) = 1.000000
- R^2 = 1.000000
- BIC = -1584.62
- Confidence = 0.15

| Model | R^2 | BIC | Params | Converged |
|-------|-----|-----|--------|-----------|
| constant * | 1.0000 | -1584.6 | 1 | yes |
| linear | 1.0000 | -1581.5 | 2 | yes |
| power_law | 1.0000 | -1581.5 | 2 | yes |
| exp_decay | 0.0000 | -580.4 | 3 | yes |
| damped_osc | 0.0000 | -585.2 | 5 | yes |
| pure_osc | 0.0000 | -585.5 | 4 | yes |

### Bridge Expander

**Calibration** (regular_graph)

- Best model: **damped_osc**
- Equation: `\delta(L) = 0.3030 e^{-0.0535 L} \cos(0.3802 L + 0.0735) + 0.3009`
- Asymptotic class: **gap**
- delta(L -> inf) = 0.300922
- R^2 = 0.631273
- BIC = -95.74
- Confidence = 0.02

| Model | R^2 | BIC | Params | Converged |
|-------|-----|-----|--------|-----------|
| constant | 0.0000 | -86.2 | 1 | yes |
| linear | 0.0949 | -85.3 | 2 | yes |
| power_law | -0.4184 | -75.4 | 2 | yes |
| exp_decay | 0.1028 | -82.4 | 3 | yes |
| damped_osc * | 0.6313 | -95.7 | 5 | yes |
| pure_osc | 0.5687 | -95.4 | 4 | yes |

**Frontier** (ramanujan_graph)

- Best model: **exp_decay**
- Equation: `\delta(L) = -0.1803 e^{-0.1506 L} + 0.7826`
- Asymptotic class: **gap**
- delta(L -> inf) = 0.782552
- R^2 = 0.958278
- BIC = -211.52
- Confidence = 0.22

| Model | R^2 | BIC | Params | Converged |
|-------|-----|-----|--------|-----------|
| constant | 0.0000 | -147.8 | 1 | yes |
| linear | 0.8242 | -183.0 | 2 | yes |
| power_law | 0.9415 | -207.2 | 2 | yes |
| exp_decay * | 0.9583 | -211.5 | 3 | yes |
| damped_osc | 0.9583 | -205.3 | 5 | yes |
| pure_osc | 0.2348 | -144.4 | 4 | yes |

### Bridge Fractal

**Calibration** (k41_cascade)

- Best model: **pure_osc**
- Equation: `\delta(L) = 0.0000 \cos(2.0242 L + 0.1453) + 0.0000`
- Asymptotic class: **indeterminate**
- delta(L -> inf) = 0.000036
- R^2 = 0.439933
- BIC = -458.10
- Confidence = 0.15

| Model | R^2 | BIC | Params | Converged |
|-------|-----|-----|--------|-----------|
| constant | 0.0000 | -454.6 | 1 | yes |
| linear | 0.0006 | -451.5 | 2 | yes |
| power_law | -0.3333 | -445.2 | 2 | yes |
| exp_decay | 0.0041 | -448.5 | 3 | yes |
| damped_osc | 0.4412 | -455.1 | 5 | yes |
| pure_osc * | 0.4399 | -458.1 | 4 | yes |

**Frontier** (intermittent_cascade)

- Best model: **pure_osc**
- Equation: `\delta(L) = 0.0469 \cos(0.4837 L + 1.3698) + 0.0489`
- Asymptotic class: **indeterminate**
- delta(L -> inf) = 0.048859
- R^2 = 0.960722
- BIC = -205.92
- Confidence = 0.14

| Model | R^2 | BIC | Params | Converged |
|-------|-----|-----|--------|-----------|
| constant | 0.0000 | -144.0 | 1 | yes |
| linear | 0.1024 | -143.3 | 2 | yes |
| power_law | -0.1090 | -138.6 | 2 | yes |
| exp_decay | 0.2099 | -143.0 | 3 | yes |
| damped_osc | 0.9614 | -203.2 | 5 | yes |
| pure_osc * | 0.9607 | -205.9 | 4 | yes |

### Bridge Rmt

**Calibration** (low_zeros)

- Best model: **pure_osc**
- Equation: `\delta(L) = 0.0001 \cos(2.0115 L + 0.3353) + 0.0002`
- Asymptotic class: **indeterminate**
- delta(L -> inf) = 0.000189
- R^2 = 0.443618
- BIC = -387.43
- Confidence = 0.16

| Model | R^2 | BIC | Params | Converged |
|-------|-----|-----|--------|-----------|
| constant | 0.0000 | -383.8 | 1 | yes |
| linear | 0.0006 | -380.7 | 2 | yes |
| power_law | -0.3333 | -374.4 | 2 | yes |
| exp_decay | 0.0030 | -377.7 | 3 | yes |
| damped_osc | 0.4433 | -384.3 | 5 | yes |
| pure_osc * | 0.4436 | -387.4 | 4 | yes |

**Frontier** (high_zeros)

- Best model: **pure_osc**
- Equation: `\delta(L) = 0.0009 \cos(2.0154 L + 0.2563) + 0.0011`
- Asymptotic class: **indeterminate**
- delta(L -> inf) = 0.001129
- R^2 = 0.444271
- BIC = -308.62
- Confidence = 0.15

| Model | R^2 | BIC | Params | Converged |
|-------|-----|-----|--------|-----------|
| constant | 0.0000 | -305.0 | 1 | yes |
| linear | 0.0006 | -301.9 | 2 | yes |
| power_law | -0.3333 | -295.6 | 2 | yes |
| exp_decay | 0.0353 | -299.6 | 3 | yes |
| damped_osc | 0.4450 | -305.6 | 5 | yes |
| pure_osc * | 0.4443 | -308.6 | 4 | yes |

### Bridge Spectral

**Calibration** (laplacian)

- Best model: **exp_decay**
- Equation: `\delta(L) = -0.2382 e^{-0.1016 L} + 0.9280`
- Asymptotic class: **gap**
- delta(L -> inf) = 0.928021
- R^2 = 0.999411
- BIC = -290.07
- Confidence = 0.31

| Model | R^2 | BIC | Params | Converged |
|-------|-----|-----|--------|-----------|
| constant | 0.0000 | -132.6 | 1 | yes |
| linear | 0.9279 | -187.4 | 2 | yes |
| power_law | 0.9987 | -275.0 | 2 | yes |
| exp_decay * | 0.9994 | -290.1 | 3 | yes |
| damped_osc | 0.9994 | -283.9 | 5 | yes |
| pure_osc | 0.9948 | -239.1 | 4 | NO |

**Frontier** (dirac_operator)

- Best model: **exp_decay**
- Equation: `\delta(L) = -0.1985 e^{-0.1019 L} + 0.9398`
- Asymptotic class: **gap**
- delta(L -> inf) = 0.939841
- R^2 = 0.999340
- BIC = -295.60
- Confidence = 0.31

| Model | R^2 | BIC | Params | Converged |
|-------|-----|-----|--------|-----------|
| constant | 0.0000 | -140.7 | 1 | yes |
| linear | 0.9276 | -195.3 | 2 | yes |
| power_law | 0.9989 | -287.9 | 2 | yes |
| exp_decay * | 0.9993 | -295.6 | 3 | yes |
| damped_osc | 0.9993 | -289.4 | 5 | yes |
| pure_osc | 0.9946 | -246.2 | 4 | NO |

### Bsd

**Calibration** (rank0_match)

- Best model: **constant**
- Equation: `\delta(L) = 0.0000`
- Asymptotic class: **affirmative**
- delta(L -> inf) = 0.000000
- R^2 = 1.000000
- BIC = -1584.62
- Confidence = 0.15

| Model | R^2 | BIC | Params | Converged |
|-------|-----|-----|--------|-----------|
| constant * | 1.0000 | -1584.6 | 1 | yes |
| linear | 1.0000 | -1581.5 | 2 | yes |
| power_law | 1.0000 | -1581.5 | 2 | NO |
| exp_decay | 0.0000 | -580.4 | 3 | yes |
| damped_osc | 0.0000 | -585.2 | 5 | yes |
| pure_osc | 0.0000 | -585.5 | 4 | yes |

**Frontier** (rank_mismatch)

- Best model: **constant**
- Equation: `\delta(L) = 1.3000`
- Asymptotic class: **gap**
- delta(L -> inf) = 1.300000
- R^2 = 1.000000
- BIC = -1584.62
- Confidence = 0.15

| Model | R^2 | BIC | Params | Converged |
|-------|-----|-----|--------|-----------|
| constant * | 1.0000 | -1584.6 | 1 | yes |
| linear | 1.0000 | -1581.5 | 2 | yes |
| power_law | 1.0000 | -1581.5 | 2 | yes |
| exp_decay | 0.0000 | -580.4 | 3 | yes |
| damped_osc | 0.0000 | -585.2 | 5 | yes |
| pure_osc | 0.0000 | -585.5 | 4 | yes |

### Bsd Avg Rank

**Calibration** (small_family)

- Best model: **constant**
- Equation: `\delta(L) = 0.0000`
- Asymptotic class: **affirmative**
- delta(L -> inf) = 0.000000
- R^2 = 1.000000
- BIC = -1584.62
- Confidence = 0.15

| Model | R^2 | BIC | Params | Converged |
|-------|-----|-----|--------|-----------|
| constant * | 1.0000 | -1584.6 | 1 | yes |
| linear | 1.0000 | -1581.5 | 2 | yes |
| power_law | 1.0000 | -1581.5 | 2 | NO |
| exp_decay | 0.0000 | -580.4 | 3 | yes |
| damped_osc | 0.0000 | -585.2 | 5 | yes |
| pure_osc | 0.0000 | -585.5 | 4 | yes |

**Frontier** (large_family)

- Best model: **pure_osc**
- Equation: `\delta(L) = 0.5209 \cos(2.2237 L + -1.6119) + 0.3928`
- Asymptotic class: **indeterminate**
- delta(L -> inf) = 0.392789
- R^2 = 0.529945
- BIC = -35.48
- Confidence = 0.09

| Model | R^2 | BIC | Params | Converged |
|-------|-----|-----|--------|-----------|
| constant | 0.0000 | -28.1 | 1 | yes |
| linear | 0.0982 | -27.3 | 2 | yes |
| power_law | -1.4444 | -5.4 | 2 | yes |
| exp_decay | 0.1141 | -24.6 | 3 | yes |
| damped_osc | 0.5548 | -33.6 | 5 | yes |
| pure_osc * | 0.5299 | -35.5 | 4 | yes |

### Bsd Function Field

**Calibration** (rank0_ff)

- Best model: **constant**
- Equation: `\delta(L) = 0.0000`
- Asymptotic class: **affirmative**
- delta(L -> inf) = 0.000000
- R^2 = 1.000000
- BIC = -1584.62
- Confidence = 0.15

| Model | R^2 | BIC | Params | Converged |
|-------|-----|-----|--------|-----------|
| constant * | 1.0000 | -1584.6 | 1 | yes |
| linear | 1.0000 | -1581.5 | 2 | yes |
| power_law | 1.0000 | -1581.5 | 2 | NO |
| exp_decay | 0.0000 | -580.4 | 3 | yes |
| damped_osc | 0.0000 | -585.2 | 5 | yes |
| pure_osc | 0.0000 | -585.5 | 4 | yes |

**Frontier** (high_rank_ff)

- Best model: **constant**
- Equation: `\delta(L) = 0.0000`
- Asymptotic class: **affirmative**
- delta(L -> inf) = 0.000000
- R^2 = 1.000000
- BIC = -1584.62
- Confidence = 0.15

| Model | R^2 | BIC | Params | Converged |
|-------|-----|-----|--------|-----------|
| constant * | 1.0000 | -1584.6 | 1 | yes |
| linear | 1.0000 | -1581.5 | 2 | yes |
| power_law | 1.0000 | -1581.5 | 2 | NO |
| exp_decay | 0.0000 | -580.4 | 3 | yes |
| damped_osc | 0.0000 | -585.2 | 5 | yes |
| pure_osc | 0.0000 | -585.5 | 4 | yes |

### Bsd Sato Tate

**Calibration** (cm_curve)

- Best model: **constant**
- Equation: `\delta(L) = 0.0000`
- Asymptotic class: **affirmative**
- delta(L -> inf) = 0.000000
- R^2 = 1.000000
- BIC = -1584.62
- Confidence = 0.15

| Model | R^2 | BIC | Params | Converged |
|-------|-----|-----|--------|-----------|
| constant * | 1.0000 | -1584.6 | 1 | yes |
| linear | 1.0000 | -1581.5 | 2 | yes |
| power_law | 1.0000 | -1581.5 | 2 | NO |
| exp_decay | 0.0000 | -580.4 | 3 | yes |
| damped_osc | 0.0000 | -585.2 | 5 | yes |
| pure_osc | 0.0000 | -585.5 | 4 | yes |

**Frontier** (non_cm_curve)

- Best model: **constant**
- Equation: `\delta(L) = 0.0000`
- Asymptotic class: **affirmative**
- delta(L -> inf) = 0.000000
- R^2 = 1.000000
- BIC = -1584.62
- Confidence = 0.15

| Model | R^2 | BIC | Params | Converged |
|-------|-----|-----|--------|-----------|
| constant * | 1.0000 | -1584.6 | 1 | yes |
| linear | 1.0000 | -1581.5 | 2 | yes |
| power_law | 1.0000 | -1581.5 | 2 | NO |
| exp_decay | 0.0000 | -580.4 | 3 | yes |
| damped_osc | 0.0000 | -585.2 | 5 | yes |
| pure_osc | 0.0000 | -585.5 | 4 | yes |

### Collatz

**Calibration** (small_orbit)

- Best model: **constant**
- Equation: `\delta(L) = 0.0000`
- Asymptotic class: **affirmative**
- delta(L -> inf) = 0.000000
- R^2 = 1.000000
- BIC = -1584.62
- Confidence = 0.15

| Model | R^2 | BIC | Params | Converged |
|-------|-----|-----|--------|-----------|
| constant * | 1.0000 | -1584.6 | 1 | yes |
| linear | 1.0000 | -1581.5 | 2 | yes |
| power_law | 1.0000 | -1581.5 | 2 | NO |
| exp_decay | 0.0000 | -580.4 | 3 | yes |
| damped_osc | 0.0000 | -585.2 | 5 | yes |
| pure_osc | 0.0000 | -585.5 | 4 | yes |

**Frontier** (large_orbit)

- Best model: **linear**
- Equation: `\delta(L) = -0.0003 L + 0.0404`
- Asymptotic class: **affirmative**
- delta(L -> inf) = 0.000000
- R^2 = 0.309924
- BIC = -257.46
- Confidence = 0.07

| Model | R^2 | BIC | Params | Converged |
|-------|-----|-----|--------|-----------|
| constant | 0.0000 | -252.4 | 1 | yes |
| linear * | 0.3099 | -257.5 | 2 | yes |
| power_law | 0.2623 | -256.0 | 2 | yes |
| exp_decay | 0.3098 | -254.4 | 3 | yes |
| damped_osc | 0.3186 | -248.5 | 5 | yes |
| pure_osc | 0.1217 | -246.0 | 4 | yes |

### Continuum

**Calibration** (constructible)

- Best model: **constant**
- Equation: `\delta(L) = 0.0000`
- Asymptotic class: **affirmative**
- delta(L -> inf) = 0.000000
- R^2 = 1.000000
- BIC = -1584.62
- Confidence = 0.15

| Model | R^2 | BIC | Params | Converged |
|-------|-----|-----|--------|-----------|
| constant * | 1.0000 | -1584.6 | 1 | yes |
| linear | 1.0000 | -1581.5 | 2 | yes |
| power_law | 1.0000 | -1581.5 | 2 | NO |
| exp_decay | 0.0000 | -580.4 | 3 | yes |
| damped_osc | 0.0000 | -585.2 | 5 | yes |
| pure_osc | 0.0000 | -585.5 | 4 | yes |

**Frontier** (forcing_extension)

- Best model: **exp_decay**
- Equation: `\delta(L) = -0.5546 e^{-0.1287 L} + 0.8570`
- Asymptotic class: **gap**
- delta(L -> inf) = 0.857038
- R^2 = 0.938156
- BIC = -150.72
- Confidence = 0.15

| Model | R^2 | BIC | Params | Converged |
|-------|-----|-----|--------|-----------|
| constant | 0.0000 | -95.7 | 1 | yes |
| linear | 0.8383 | -132.7 | 2 | yes |
| power_law | 0.9183 | -147.7 | 2 | yes |
| exp_decay * | 0.9382 | -150.7 | 3 | yes |
| damped_osc | 0.9382 | -144.5 | 5 | yes |
| pure_osc | 0.9285 | -144.4 | 4 | NO |

### Cosmo Constant

**Calibration** (low_cutoff)

- Best model: **power_law**
- Equation: `\delta(L) = 0.5560 \cdot L^{0.0124}`
- Asymptotic class: **gap**
- delta(L -> inf) = inf
- R^2 = 0.999424
- BIC = -399.42
- Confidence = 1.00

| Model | R^2 | BIC | Params | Converged |
|-------|-----|-----|--------|-----------|
| constant | 0.0000 | -238.4 | 1 | yes |
| linear | 0.9203 | -291.0 | 2 | yes |
| power_law * | 0.9994 | -399.4 | 2 | yes |
| exp_decay | 0.9969 | -359.3 | 3 | yes |
| damped_osc | 0.9969 | -353.1 | 5 | yes |
| pure_osc | 0.9876 | -325.8 | 4 | yes |

**Frontier** (planck_cutoff)

- Best model: **constant**
- Equation: `\delta(L) = 0.9824`
- Asymptotic class: **gap**
- delta(L -> inf) = 0.982436
- R^2 = 0.000000
- BIC = -594.21
- Confidence = 0.14

| Model | R^2 | BIC | Params | Converged |
|-------|-----|-----|--------|-----------|
| constant * | 0.0000 | -594.2 | 1 | yes |
| linear | 0.0141 | -591.4 | 2 | yes |
| power_law | 0.0046 | -591.2 | 2 | yes |
| exp_decay | -3.4053 | -555.4 | 3 | yes |
| damped_osc | 0.0259 | -582.4 | 5 | yes |
| pure_osc | -1.2074 | -567.5 | 4 | yes |

### Falconer

**Calibration** (high_dimension)

- Best model: **constant**
- Equation: `\delta(L) = 0.0000`
- Asymptotic class: **affirmative**
- delta(L -> inf) = 0.000000
- R^2 = 1.000000
- BIC = -1584.62
- Confidence = 0.15

| Model | R^2 | BIC | Params | Converged |
|-------|-----|-----|--------|-----------|
| constant * | 1.0000 | -1584.6 | 1 | yes |
| linear | 1.0000 | -1581.5 | 2 | yes |
| power_law | 1.0000 | -1581.5 | 2 | NO |
| exp_decay | 0.0000 | -580.4 | 3 | yes |
| damped_osc | 0.0000 | -585.2 | 5 | yes |
| pure_osc | 0.0000 | -585.5 | 4 | yes |

**Frontier** (threshold_dimension)

- Best model: **constant**
- Equation: `\delta(L) = 0.0003`
- Asymptotic class: **affirmative**
- delta(L -> inf) = 0.000290
- R^2 = 0.000000
- BIC = -331.96
- Confidence = 0.14

| Model | R^2 | BIC | Params | Converged |
|-------|-----|-----|--------|-----------|
| constant * | 0.0000 | -332.0 | 1 | yes |
| linear | 0.0100 | -329.1 | 2 | yes |
| power_law | -0.4350 | -320.9 | 2 | yes |
| exp_decay | 0.0224 | -326.3 | 3 | yes |
| damped_osc | 0.3125 | -327.8 | 5 | yes |
| pure_osc | 0.0568 | -324.0 | 4 | yes |

### Hodge

**Calibration** (algebraic)

- Best model: **pure_osc**
- Equation: `\delta(L) = 0.0006 \cos(2.0160 L + 0.2443) + 0.0207`
- Asymptotic class: **indeterminate**
- delta(L -> inf) = 0.020750
- R^2 = 0.444235
- BIC = -326.46
- Confidence = 0.15

| Model | R^2 | BIC | Params | Converged |
|-------|-----|-----|--------|-----------|
| constant | 0.0000 | -322.8 | 1 | yes |
| linear | 0.0006 | -319.7 | 2 | yes |
| power_law | -0.0000 | -319.7 | 2 | yes |
| exp_decay | 0.0350 | -317.4 | 3 | yes |
| damped_osc | 0.4450 | -323.4 | 5 | yes |
| pure_osc * | 0.4442 | -326.5 | 4 | yes |

**Frontier** (analytic_only)

- Best model: **constant**
- Equation: `\delta(L) = 0.6036`
- Asymptotic class: **gap**
- delta(L -> inf) = 0.603552
- R^2 = 0.000000
- BIC = -171.11
- Confidence = 0.09

| Model | R^2 | BIC | Params | Converged |
|-------|-----|-----|--------|-----------|
| constant * | 0.0000 | -171.1 | 1 | yes |
| linear | 0.0141 | -168.3 | 2 | yes |
| power_law | 0.0044 | -168.1 | 2 | yes |
| exp_decay | 0.0141 | -165.2 | 3 | NO |
| damped_osc | 0.2930 | -166.4 | 5 | yes |
| pure_osc | 0.2908 | -169.4 | 4 | yes |

### Hodge Standard

**Calibration** (smooth_projective)

- Best model: **pure_osc**
- Equation: `\delta(L) = 0.0029 \cos(2.0156 L + 0.2520) + 0.0838`
- Asymptotic class: **indeterminate**
- delta(L -> inf) = 0.083766
- R^2 = 0.444274
- BIC = -255.65
- Confidence = 0.15

| Model | R^2 | BIC | Params | Converged |
|-------|-----|-----|--------|-----------|
| constant | 0.0000 | -252.0 | 1 | yes |
| linear | 0.0006 | -248.9 | 2 | yes |
| power_law | -0.0002 | -248.9 | 2 | yes |
| exp_decay | 0.0357 | -246.6 | 3 | yes |
| damped_osc | 0.4449 | -252.6 | 5 | yes |
| pure_osc * | 0.4443 | -255.6 | 4 | yes |

**Frontier** (singular_variety)

- Best model: **linear**
- Equation: `\delta(L) = 0.0150 L + 0.3437`
- Asymptotic class: **gap**
- delta(L -> inf) = inf
- R^2 = 0.994199
- BIC = -210.40
- Confidence = 0.18

| Model | R^2 | BIC | Params | Converged |
|-------|-----|-----|--------|-----------|
| constant | 0.0000 | -100.2 | 1 | yes |
| linear * | 0.9942 | -210.4 | 2 | yes |
| power_law | 0.9589 | -167.3 | 2 | yes |
| exp_decay | 0.9942 | -207.4 | 3 | NO |
| damped_osc | 0.9948 | -203.7 | 5 | yes |
| pure_osc | 0.9949 | -206.8 | 4 | yes |

### Hodge Tate

**Calibration** (abelian_variety)

- Best model: **pure_osc**
- Equation: `\delta(L) = 0.0029 \cos(2.0156 L + 0.2520) + 0.0538`
- Asymptotic class: **indeterminate**
- delta(L -> inf) = 0.053766
- R^2 = 0.444274
- BIC = -255.65
- Confidence = 0.15

| Model | R^2 | BIC | Params | Converged |
|-------|-----|-----|--------|-----------|
| constant | 0.0000 | -252.0 | 1 | yes |
| linear | 0.0006 | -248.9 | 2 | yes |
| power_law | -0.0006 | -248.9 | 2 | yes |
| exp_decay | 0.0357 | -246.6 | 3 | yes |
| damped_osc | 0.4449 | -252.6 | 5 | yes |
| pure_osc * | 0.4443 | -255.6 | 4 | yes |

**Frontier** (higher_codimension)

- Best model: **linear**
- Equation: `\delta(L) = 0.0200 L + 0.2873`
- Asymptotic class: **gap**
- delta(L -> inf) = inf
- R^2 = 0.997723
- BIC = -218.42
- Confidence = 0.18

| Model | R^2 | BIC | Params | Converged |
|-------|-----|-----|--------|-----------|
| constant | 0.0000 | -87.6 | 1 | yes |
| linear * | 0.9977 | -218.4 | 2 | yes |
| power_law | 0.9712 | -162.6 | 2 | yes |
| exp_decay | 0.9977 | -215.4 | 3 | NO |
| damped_osc | 0.9980 | -211.7 | 5 | yes |
| pure_osc | 0.9980 | -214.9 | 4 | yes |

### Hodge Transcendental

**Calibration** (k3_surface)

- Best model: **linear**
- Equation: `\delta(L) = 0.0100 L + 0.1958`
- Asymptotic class: **gap**
- delta(L -> inf) = inf
- R^2 = 0.994199
- BIC = -228.24
- Confidence = 0.18

| Model | R^2 | BIC | Params | Converged |
|-------|-----|-----|--------|-----------|
| constant | 0.0000 | -118.0 | 1 | yes |
| linear * | 0.9942 | -228.2 | 2 | yes |
| power_law | 0.9618 | -186.8 | 2 | yes |
| exp_decay | 0.9942 | -225.3 | 3 | NO |
| damped_osc | 0.9948 | -221.6 | 5 | yes |
| pure_osc | 0.9949 | -224.7 | 4 | yes |

**Frontier** (high_dimension_class)

- Best model: **linear**
- Equation: `\delta(L) = 0.0200 L + 0.4909`
- Asymptotic class: **gap**
- delta(L -> inf) = inf
- R^2 = 0.994897
- BIC = -200.58
- Confidence = 0.18

| Model | R^2 | BIC | Params | Converged |
|-------|-----|-----|--------|-----------|
| constant | 0.0000 | -87.6 | 1 | yes |
| linear * | 0.9949 | -200.6 | 2 | yes |
| power_law | 0.9584 | -154.4 | 2 | yes |
| exp_decay | 0.9949 | -197.6 | 3 | NO |
| damped_osc | 0.9955 | -193.9 | 5 | yes |
| pure_osc | 0.9955 | -197.0 | 4 | yes |

### Info Paradox

**Calibration** (large_bh)

- Best model: **damped_osc**
- Equation: `\delta(L) = 0.2175 e^{0.0010 L} \cos(0.0171 L + 1.2075) + 0.4259`
- Asymptotic class: **indeterminate**
- delta(L -> inf) = 0.425907
- R^2 = 0.999979
- BIC = -386.36
- Confidence = 1.00

| Model | R^2 | BIC | Params | Converged |
|-------|-----|-----|--------|-----------|
| constant | 0.0000 | -162.2 | 1 | yes |
| linear | 0.9998 | -350.8 | 2 | yes |
| power_law | 0.9103 | -212.1 | 2 | yes |
| exp_decay | 0.9997 | -335.0 | 3 | NO |
| damped_osc * | 1.0000 | -386.4 | 5 | yes |
| pure_osc | 0.9998 | -344.0 | 4 | NO |

**Frontier** (small_bh)

- Best model: **linear**
- Equation: `\delta(L) = -0.0415 L + 1.0503`
- Asymptotic class: **affirmative**
- delta(L -> inf) = 0.000000
- R^2 = 0.999798
- BIC = -239.68
- Confidence = 1.00

| Model | R^2 | BIC | Params | Converged |
|-------|-----|-----|--------|-----------|
| constant | 0.0000 | -55.7 | 1 | yes |
| linear * | 0.9998 | -239.7 | 2 | yes |
| power_law | 0.2658 | -59.4 | 2 | yes |
| exp_decay | 0.9997 | -225.2 | 3 | NO |
| damped_osc | 1.0000 | -296.8 | 5 | NO |
| pure_osc | 1.0000 | -291.7 | 4 | NO |

### Inverse Galois

**Calibration** (cyclic_group)

- Best model: **constant**
- Equation: `\delta(L) = 0.0498`
- Asymptotic class: **gap**
- delta(L -> inf) = 0.049840
- R^2 = 0.000000
- BIC = -307.56
- Confidence = 0.09

| Model | R^2 | BIC | Params | Converged |
|-------|-----|-----|--------|-----------|
| constant * | 0.0000 | -307.6 | 1 | yes |
| linear | 0.0141 | -304.8 | 2 | yes |
| power_law | 0.0045 | -304.6 | 2 | yes |
| exp_decay | 0.0668 | -302.9 | 3 | yes |
| damped_osc | 0.2930 | -302.8 | 5 | yes |
| pure_osc | 0.2908 | -305.8 | 4 | yes |

**Frontier** (sporadic_group)

- Best model: **constant**
- Equation: `\delta(L) = 0.6982`
- Asymptotic class: **gap**
- delta(L -> inf) = 0.698224
- R^2 = 0.000000
- BIC = -201.61
- Confidence = 0.09

| Model | R^2 | BIC | Params | Converged |
|-------|-----|-----|--------|-----------|
| constant * | 0.0000 | -201.6 | 1 | yes |
| linear | 0.0141 | -198.8 | 2 | yes |
| power_law | 0.0046 | -198.6 | 2 | yes |
| exp_decay | 0.0670 | -197.0 | 3 | yes |
| damped_osc | 0.2930 | -196.9 | 5 | yes |
| pure_osc | 0.2908 | -199.9 | 4 | yes |

### Jacobian

**Calibration** (degree_2)

- Best model: **constant**
- Equation: `\delta(L) = 0.0497`
- Asymptotic class: **gap**
- delta(L -> inf) = 0.049734
- R^2 = 0.000000
- BIC = -285.08
- Confidence = 0.09

| Model | R^2 | BIC | Params | Converged |
|-------|-----|-----|--------|-----------|
| constant * | 0.0000 | -285.1 | 1 | yes |
| linear | 0.0141 | -282.3 | 2 | yes |
| power_law | 0.0044 | -282.1 | 2 | yes |
| exp_decay | 0.0670 | -280.4 | 3 | yes |
| damped_osc | 0.2930 | -280.3 | 5 | yes |
| pure_osc | 0.2908 | -283.4 | 4 | yes |

**Frontier** (degree_5)

- Best model: **constant**
- Equation: `\delta(L) = 0.3982`
- Asymptotic class: **gap**
- delta(L -> inf) = 0.398224
- R^2 = 0.000000
- BIC = -201.61
- Confidence = 0.09

| Model | R^2 | BIC | Params | Converged |
|-------|-----|-----|--------|-----------|
| constant * | 0.0000 | -201.6 | 1 | yes |
| linear | 0.0141 | -198.8 | 2 | yes |
| power_law | 0.0045 | -198.6 | 2 | yes |
| exp_decay | 0.0670 | -197.0 | 3 | yes |
| damped_osc | 0.2930 | -196.9 | 5 | yes |
| pure_osc | 0.2908 | -199.9 | 4 | yes |

### Langlands

**Calibration** (gl2_case)

- Best model: **constant**
- Equation: `\delta(L) = 0.1497`
- Asymptotic class: **gap**
- delta(L -> inf) = 0.149734
- R^2 = 0.000000
- BIC = -285.08
- Confidence = 0.09

| Model | R^2 | BIC | Params | Converged |
|-------|-----|-----|--------|-----------|
| constant * | 0.0000 | -285.1 | 1 | yes |
| linear | 0.0141 | -282.3 | 2 | yes |
| power_law | 0.0046 | -282.1 | 2 | yes |
| exp_decay | 0.0670 | -280.4 | 3 | yes |
| damped_osc | 0.2930 | -280.3 | 5 | yes |
| pure_osc | 0.2908 | -283.4 | 4 | yes |

**Frontier** (gl3_case)

- Best model: **constant**
- Equation: `\delta(L) = 0.4982`
- Asymptotic class: **gap**
- delta(L -> inf) = 0.498224
- R^2 = 0.000000
- BIC = -201.61
- Confidence = 0.09

| Model | R^2 | BIC | Params | Converged |
|-------|-----|-----|--------|-----------|
| constant * | 0.0000 | -201.6 | 1 | yes |
| linear | 0.0141 | -198.8 | 2 | yes |
| power_law | 0.0045 | -198.6 | 2 | yes |
| exp_decay | 0.0670 | -197.0 | 3 | yes |
| damped_osc | 0.2930 | -196.9 | 5 | yes |
| pure_osc | 0.2908 | -199.9 | 4 | yes |

### Navier Stokes

**Calibration** (lamb_oseen)

- Best model: **pure_osc**
- Equation: `\delta(L) = 0.1035 \cos(0.6978 L + 0.8933) + 0.3995`
- Asymptotic class: **indeterminate**
- delta(L -> inf) = 0.399469
- R^2 = 0.997088
- BIC = -231.48
- Confidence = 0.14

| Model | R^2 | BIC | Params | Converged |
|-------|-----|-----|--------|-----------|
| constant | 0.0000 | -112.3 | 1 | yes |
| linear | 0.0002 | -109.2 | 2 | yes |
| power_law | -0.0030 | -109.1 | 2 | yes |
| exp_decay | 0.1253 | -109.1 | 3 | yes |
| damped_osc | 0.9971 | -228.6 | 5 | yes |
| pure_osc * | 0.9971 | -231.5 | 4 | yes |

**Frontier** (high_strain)

- Best model: **damped_osc**
- Equation: `\delta(L) = 0.9825 e^{-0.7562 L} \cos(0.5348 L + -2.4548) + 0.0101`
- Asymptotic class: **gap**
- delta(L -> inf) = 0.010079
- R^2 = 0.999422
- BIC = -328.43
- Confidence = 1.00

| Model | R^2 | BIC | Params | Converged |
|-------|-----|-----|--------|-----------|
| constant | 0.0000 | -176.8 | 1 | yes |
| linear | 0.3505 | -183.2 | 2 | yes |
| power_law | 0.6104 | -194.4 | 2 | yes |
| exp_decay | 0.9813 | -258.1 | 3 | yes |
| damped_osc * | 0.9994 | -328.4 | 5 | yes |
| pure_osc | 0.6976 | -193.8 | 4 | NO |

### Ns 2D

**Calibration** (vortex_patch)

- Best model: **constant**
- Equation: `\delta(L) = 0.2996`
- Asymptotic class: **gap**
- delta(L -> inf) = 0.299556
- R^2 = 0.000000
- BIC = -262.60
- Confidence = 0.09

| Model | R^2 | BIC | Params | Converged |
|-------|-----|-----|--------|-----------|
| constant * | 0.0000 | -262.6 | 1 | yes |
| linear | 0.0141 | -259.8 | 2 | yes |
| power_law | 0.0046 | -259.6 | 2 | yes |
| exp_decay | 0.0670 | -257.9 | 3 | yes |
| damped_osc | 0.2930 | -257.9 | 5 | yes |
| pure_osc | 0.2908 | -260.9 | 4 | yes |

**Frontier** (vortex_merger)

- Best model: **pure_osc**
- Equation: `\delta(L) = 0.2017 \cos(0.9992 L + 2.1249) + 0.4981`
- Asymptotic class: **indeterminate**
- delta(L -> inf) = 0.498095
- R^2 = 0.996340
- BIC = -197.07
- Confidence = 0.15

| Model | R^2 | BIC | Params | Converged |
|-------|-----|-----|--------|-----------|
| constant | 0.0000 | -82.9 | 1 | yes |
| linear | 0.0000 | -79.8 | 2 | yes |
| power_law | -0.0146 | -79.5 | 2 | yes |
| exp_decay | 0.0431 | -77.7 | 3 | yes |
| damped_osc | 0.9964 | -194.1 | 5 | yes |
| pure_osc * | 0.9963 | -197.1 | 4 | yes |

### Ns Euler

**Calibration** (vortex_ring)

- Best model: **constant**
- Equation: `\delta(L) = 0.4991`
- Asymptotic class: **gap**
- delta(L -> inf) = 0.499112
- R^2 = 0.000000
- BIC = -232.11
- Confidence = 0.09

| Model | R^2 | BIC | Params | Converged |
|-------|-----|-----|--------|-----------|
| constant * | 0.0000 | -232.1 | 1 | yes |
| linear | 0.0141 | -229.3 | 2 | yes |
| power_law | 0.0046 | -229.1 | 2 | yes |
| exp_decay | 0.0670 | -227.5 | 3 | yes |
| damped_osc | 0.2930 | -227.4 | 5 | yes |
| pure_osc | 0.2908 | -230.4 | 4 | yes |

**Frontier** (blowup_candidate)

- Best model: **constant**
- Equation: `\delta(L) = 0.1982`
- Asymptotic class: **gap**
- delta(L -> inf) = 0.198224
- R^2 = 0.000000
- BIC = -201.61
- Confidence = 0.09

| Model | R^2 | BIC | Params | Converged |
|-------|-----|-----|--------|-----------|
| constant * | 0.0000 | -201.6 | 1 | yes |
| linear | 0.0141 | -198.8 | 2 | yes |
| power_law | 0.0040 | -198.6 | 2 | yes |
| exp_decay | 0.0670 | -197.0 | 3 | yes |
| damped_osc | 0.2930 | -196.9 | 5 | yes |
| pure_osc | 0.2908 | -199.9 | 4 | yes |

### Ns Sqg

**Calibration** (smooth_theta)

- Best model: **damped_osc**
- Equation: `\delta(L) = 0.1075 e^{-0.0039 L} \cos(0.5014 L + 2.6304) + 0.4493`
- Asymptotic class: **gap**
- delta(L -> inf) = 0.449300
- R^2 = 0.997883
- BIC = -238.67
- Confidence = 0.09

| Model | R^2 | BIC | Params | Converged |
|-------|-----|-----|--------|-----------|
| constant | 0.0000 | -115.6 | 1 | yes |
| linear | 0.0000 | -112.5 | 2 | yes |
| power_law | -0.0057 | -112.3 | 2 | yes |
| exp_decay | 0.0564 | -110.7 | 3 | yes |
| damped_osc * | 0.9979 | -238.7 | 5 | yes |
| pure_osc | 0.9974 | -236.9 | 4 | yes |

**Frontier** (singular_front)

- Best model: **damped_osc**
- Equation: `\delta(L) = 0.1206 e^{-0.0159 L} \cos(0.7867 L + 0.8747) + 0.6986`
- Asymptotic class: **gap**
- delta(L -> inf) = 0.698571
- R^2 = 0.977952
- BIC = -184.53
- Confidence = 0.24

| Model | R^2 | BIC | Params | Converged |
|-------|-----|-----|--------|-----------|
| constant | 0.0000 | -113.0 | 1 | yes |
| linear | 0.0338 | -110.6 | 2 | yes |
| power_law | 0.0411 | -110.8 | 2 | yes |
| exp_decay | 0.1697 | -110.9 | 3 | yes |
| damped_osc * | 0.9780 | -184.5 | 5 | yes |
| pure_osc | 0.9684 | -179.7 | 4 | yes |

### P Vs Np

**Calibration** (easy)

- Best model: **constant**
- Equation: `\delta(L) = 0.7500`
- Asymptotic class: **gap**
- delta(L -> inf) = 0.750000
- R^2 = 1.000000
- BIC = -1584.62
- Confidence = 0.15

| Model | R^2 | BIC | Params | Converged |
|-------|-----|-----|--------|-----------|
| constant * | 1.0000 | -1584.6 | 1 | yes |
| linear | 1.0000 | -1581.5 | 2 | yes |
| power_law | 1.0000 | -1581.5 | 2 | yes |
| exp_decay | 0.0000 | -580.4 | 3 | yes |
| damped_osc | 0.0000 | -585.2 | 5 | yes |
| pure_osc | 0.0000 | -585.5 | 4 | yes |

**Frontier** (hard)

- Best model: **exp_decay**
- Equation: `\delta(L) = -0.3430 e^{-0.2252 L} + 0.8516`
- Asymptotic class: **gap**
- delta(L -> inf) = 0.851637
- R^2 = 0.892454
- BIC = -171.00
- Confidence = 0.10

| Model | R^2 | BIC | Params | Converged |
|-------|-----|-----|--------|-----------|
| constant | 0.0000 | -128.1 | 1 | yes |
| linear | 0.6223 | -146.5 | 2 | yes |
| power_law | 0.7914 | -159.5 | 2 | yes |
| exp_decay * | 0.8925 | -171.0 | 3 | yes |
| damped_osc | 0.9112 | -169.0 | 5 | yes |
| pure_osc | 0.1242 | -121.8 | 4 | yes |

### Pnp Ac0

**Calibration** (small_circuit)

- Best model: **pure_osc**
- Equation: `\delta(L) = 0.1350 \cos(0.1738 L + 2.2453) + 0.1630`
- Asymptotic class: **indeterminate**
- delta(L -> inf) = 0.163027
- R^2 = 0.992706
- BIC = -195.92
- Confidence = 1.00

| Model | R^2 | BIC | Params | Converged |
|-------|-----|-----|--------|-----------|
| constant | 0.0000 | -96.9 | 1 | yes |
| linear | 0.9530 | -161.1 | 2 | yes |
| power_law | 0.9422 | -156.6 | 2 | yes |
| exp_decay | 0.9528 | -157.9 | 3 | NO |
| damped_osc | 0.9973 | -214.6 | 5 | NO |
| pure_osc * | 0.9927 | -195.9 | 4 | yes |

**Frontier** (parity_circuit)

- Best model: **constant**
- Equation: `\delta(L) = 0.0000`
- Asymptotic class: **affirmative**
- delta(L -> inf) = 0.000000
- R^2 = 1.000000
- BIC = -1584.62
- Confidence = 0.15

| Model | R^2 | BIC | Params | Converged |
|-------|-----|-----|--------|-----------|
| constant * | 1.0000 | -1584.6 | 1 | yes |
| linear | 1.0000 | -1581.5 | 2 | yes |
| power_law | 1.0000 | -1581.5 | 2 | NO |
| exp_decay | 0.0000 | -580.4 | 3 | yes |
| damped_osc | 0.0000 | -585.2 | 5 | yes |
| pure_osc | 0.0000 | -585.5 | 4 | yes |

### Pnp Bpp

**Calibration** (low_error)

- Best model: **constant**
- Equation: `\delta(L) = 0.0496`
- Asymptotic class: **gap**
- delta(L -> inf) = 0.049556
- R^2 = 0.000000
- BIC = -262.60
- Confidence = 0.09

| Model | R^2 | BIC | Params | Converged |
|-------|-----|-----|--------|-----------|
| constant * | 0.0000 | -262.6 | 1 | yes |
| linear | 0.0141 | -259.8 | 2 | yes |
| power_law | 0.0040 | -259.6 | 2 | yes |
| exp_decay | 0.0670 | -257.9 | 3 | yes |
| damped_osc | 0.2930 | -257.9 | 5 | yes |
| pure_osc | 0.2908 | -260.9 | 4 | yes |

**Frontier** (high_error)

- Best model: **constant**
- Equation: `\delta(L) = 0.0500`
- Asymptotic class: **gap**
- delta(L -> inf) = 0.050000
- R^2 = 1.000000
- BIC = -1584.62
- Confidence = 0.15

| Model | R^2 | BIC | Params | Converged |
|-------|-----|-----|--------|-----------|
| constant * | 1.0000 | -1584.6 | 1 | yes |
| linear | 1.0000 | -1581.5 | 2 | yes |
| power_law | 1.0000 | -1581.5 | 2 | yes |
| exp_decay | 0.0000 | -580.4 | 3 | yes |
| damped_osc | 0.0000 | -585.2 | 5 | yes |
| pure_osc | 0.0000 | -585.5 | 4 | yes |

### Pnp Clique

**Calibration** (sparse_graph)

- Best model: **pure_osc**
- Equation: `\delta(L) = -0.0322 \cos(0.5037 L + 0.9503) + 0.0317`
- Asymptotic class: **indeterminate**
- delta(L -> inf) = 0.031673
- R^2 = 0.886039
- BIC = -197.22
- Confidence = 0.15

| Model | R^2 | BIC | Params | Converged |
|-------|-----|-----|--------|-----------|
| constant | 0.0000 | -158.7 | 1 | yes |
| linear | 0.2756 | -162.7 | 2 | yes |
| power_law | 0.2574 | -162.2 | 2 | yes |
| exp_decay | 0.3965 | -163.6 | 3 | yes |
| damped_osc | 0.8864 | -194.2 | 5 | yes |
| pure_osc * | 0.8860 | -197.2 | 4 | yes |

**Frontier** (dense_graph)

- Best model: **constant**
- Equation: `\delta(L) = 0.0000`
- Asymptotic class: **affirmative**
- delta(L -> inf) = 0.000000
- R^2 = 1.000000
- BIC = -1584.62
- Confidence = 0.15

| Model | R^2 | BIC | Params | Converged |
|-------|-----|-----|--------|-----------|
| constant * | 1.0000 | -1584.6 | 1 | yes |
| linear | 1.0000 | -1581.5 | 2 | yes |
| power_law | 1.0000 | -1581.5 | 2 | NO |
| exp_decay | 0.0000 | -580.4 | 3 | yes |
| damped_osc | 0.0000 | -585.2 | 5 | yes |
| pure_osc | 0.0000 | -585.5 | 4 | yes |

### Poincare 4D

**Calibration** (standard_sphere)

- Best model: **constant**
- Equation: `\delta(L) = 0.0000`
- Asymptotic class: **affirmative**
- delta(L -> inf) = 0.000000
- R^2 = 1.000000
- BIC = -1584.62
- Confidence = 0.15

| Model | R^2 | BIC | Params | Converged |
|-------|-----|-----|--------|-----------|
| constant * | 1.0000 | -1584.6 | 1 | yes |
| linear | 1.0000 | -1581.5 | 2 | yes |
| power_law | 1.0000 | -1581.5 | 2 | NO |
| exp_decay | 0.0000 | -580.4 | 3 | yes |
| damped_osc | 0.0000 | -585.2 | 5 | yes |
| pure_osc | 0.0000 | -585.5 | 4 | yes |

**Frontier** (exotic_candidate)

- Best model: **constant**
- Equation: `\delta(L) = 0.4000`
- Asymptotic class: **gap**
- delta(L -> inf) = 0.400000
- R^2 = 1.000000
- BIC = -1584.62
- Confidence = 0.15

| Model | R^2 | BIC | Params | Converged |
|-------|-----|-----|--------|-----------|
| constant * | 1.0000 | -1584.6 | 1 | yes |
| linear | 1.0000 | -1581.5 | 2 | yes |
| power_law | 1.0000 | -1581.5 | 2 | yes |
| exp_decay | 0.0000 | -580.4 | 3 | yes |
| damped_osc | 0.0000 | -585.2 | 5 | yes |
| pure_osc | 0.0000 | -585.5 | 4 | yes |

### Ramsey

**Calibration** (small_colors)

- Best model: **exp_decay**
- Equation: `\delta(L) = 0.5687 e^{-0.1074 L} + 0.4960`
- Asymptotic class: **gap**
- delta(L -> inf) = 0.495984
- R^2 = 0.996189
- BIC = -210.83
- Confidence = 0.31

| Model | R^2 | BIC | Params | Converged |
|-------|-----|-----|--------|-----------|
| constant | 0.0000 | -94.5 | 1 | yes |
| linear | 0.9163 | -145.9 | 2 | yes |
| power_law | 0.9877 | -188.1 | 2 | yes |
| exp_decay * | 0.9962 | -210.8 | 3 | yes |
| damped_osc | 0.9962 | -204.6 | 5 | yes |
| pure_osc | 0.9917 | -190.6 | 4 | NO |

**Frontier** (many_colors)

- Best model: **constant**
- Equation: `\delta(L) = 1.0000`
- Asymptotic class: **gap**
- delta(L -> inf) = 1.000000
- R^2 = 1.000000
- BIC = -1584.62
- Confidence = 0.15

| Model | R^2 | BIC | Params | Converged |
|-------|-----|-----|--------|-----------|
| constant * | 1.0000 | -1584.6 | 1 | yes |
| linear | 1.0000 | -1581.5 | 2 | yes |
| power_law | 1.0000 | -1581.5 | 2 | yes |
| exp_decay | 0.0000 | -580.4 | 3 | yes |
| damped_osc | 0.0000 | -585.2 | 5 | yes |
| pure_osc | 0.0000 | -585.5 | 4 | yes |

### Rh Dirichlet

**Calibration** (trivial_character)

- Best model: **constant**
- Equation: `\delta(L) = 0.5052`
- Asymptotic class: **gap**
- delta(L -> inf) = 0.505222
- R^2 = 0.000000
- BIC = -293.10
- Confidence = 0.09

| Model | R^2 | BIC | Params | Converged |
|-------|-----|-----|--------|-----------|
| constant * | 0.0000 | -293.1 | 1 | yes |
| linear | 0.0141 | -290.3 | 2 | yes |
| power_law | 0.0046 | -290.1 | 2 | yes |
| exp_decay | 0.0138 | -287.2 | 3 | yes |
| damped_osc | 0.2930 | -288.4 | 5 | yes |
| pure_osc | 0.2908 | -291.4 | 4 | yes |

**Frontier** (quadratic_character)

- Best model: **constant**
- Equation: `\delta(L) = 0.4207`
- Asymptotic class: **gap**
- delta(L -> inf) = 0.420710
- R^2 = 0.000000
- BIC = -241.92
- Confidence = 0.14

| Model | R^2 | BIC | Params | Converged |
|-------|-----|-----|--------|-----------|
| constant * | 0.0000 | -241.9 | 1 | yes |
| linear | 0.0141 | -239.1 | 2 | yes |
| power_law | 0.0046 | -238.9 | 2 | yes |
| exp_decay | 0.0140 | -236.1 | 3 | yes |
| damped_osc | 0.2930 | -237.2 | 5 | yes |
| pure_osc | 0.1736 | -236.8 | 4 | yes |

### Rh Fake

**Calibration** (near_axis)

- Best model: **constant**
- Equation: `\delta(L) = 0.3507`
- Asymptotic class: **gap**
- delta(L -> inf) = 0.350710
- R^2 = 0.000000
- BIC = -241.92
- Confidence = 0.14

| Model | R^2 | BIC | Params | Converged |
|-------|-----|-----|--------|-----------|
| constant * | 0.0000 | -241.9 | 1 | yes |
| linear | 0.0141 | -239.1 | 2 | yes |
| power_law | 0.0046 | -238.9 | 2 | yes |
| exp_decay | 0.0140 | -236.1 | 3 | yes |
| damped_osc | 0.2930 | -237.2 | 5 | yes |
| pure_osc | 0.1736 | -236.8 | 4 | yes |

**Frontier** (off_line_fake)

- Best model: **constant**
- Equation: `\delta(L) = 0.2724`
- Asymptotic class: **gap**
- delta(L -> inf) = 0.272397
- R^2 = 0.000000
- BIC = -188.40
- Confidence = 0.09

| Model | R^2 | BIC | Params | Converged |
|-------|-----|-----|--------|-----------|
| constant * | 0.0000 | -188.4 | 1 | yes |
| linear | 0.0141 | -185.6 | 2 | yes |
| power_law | 0.0041 | -185.4 | 2 | yes |
| exp_decay | 0.0670 | -183.7 | 3 | yes |
| damped_osc | 0.2930 | -183.7 | 5 | yes |
| pure_osc | 0.2908 | -186.7 | 4 | yes |

### Rh Function Field

**Calibration** (small_genus)

- Best model: **constant**
- Equation: `\delta(L) = 0.9021`
- Asymptotic class: **gap**
- delta(L -> inf) = 0.902144
- R^2 = 0.000000
- BIC = -312.19
- Confidence = 0.09

| Model | R^2 | BIC | Params | Converged |
|-------|-----|-----|--------|-----------|
| constant * | 0.0000 | -312.2 | 1 | yes |
| linear | 0.0141 | -309.4 | 2 | yes |
| power_law | 0.0046 | -309.2 | 2 | yes |
| exp_decay | 0.0155 | -306.4 | 3 | yes |
| damped_osc | 0.2930 | -307.5 | 5 | yes |
| pure_osc | 0.2908 | -310.5 | 4 | yes |

**Frontier** (high_genus)

- Best model: **constant**
- Equation: `\delta(L) = 0.8552`
- Asymptotic class: **gap**
- delta(L -> inf) = 0.855222
- R^2 = 0.000000
- BIC = -293.10
- Confidence = 0.09

| Model | R^2 | BIC | Params | Converged |
|-------|-----|-----|--------|-----------|
| constant * | 0.0000 | -293.1 | 1 | yes |
| linear | 0.0141 | -290.3 | 2 | yes |
| power_law | 0.0046 | -290.1 | 2 | yes |
| exp_decay | 0.0138 | -287.2 | 3 | yes |
| damped_osc | 0.2930 | -288.4 | 5 | yes |
| pure_osc | 0.2908 | -291.4 | 4 | yes |

### Riemann

**Calibration** (known_zero)

- Best model: **constant**
- Equation: `\delta(L) = 0.0055`
- Asymptotic class: **gap**
- delta(L -> inf) = 0.005495
- R^2 = 0.000000
- BIC = -262.29
- Confidence = 0.14

| Model | R^2 | BIC | Params | Converged |
|-------|-----|-----|--------|-----------|
| constant * | 0.0000 | -262.3 | 1 | yes |
| linear | 0.0123 | -259.5 | 2 | yes |
| power_law | -0.0516 | -258.1 | 2 | yes |
| exp_decay | 0.0122 | -256.4 | 3 | yes |
| damped_osc | 0.1463 | -253.4 | 5 | yes |
| pure_osc | 0.1346 | -256.2 | 4 | yes |

**Frontier** (off_line)

- Best model: **constant**
- Equation: `\delta(L) = 0.2428`
- Asymptotic class: **gap**
- delta(L -> inf) = 0.242772
- R^2 = 0.000000
- BIC = -93.82
- Confidence = 0.15

| Model | R^2 | BIC | Params | Converged |
|-------|-----|-----|--------|-----------|
| constant * | 0.0000 | -93.8 | 1 | yes |
| linear | 0.0002 | -90.7 | 2 | yes |
| power_law | -0.0371 | -89.9 | 2 | yes |
| exp_decay | 0.0939 | -89.8 | 3 | yes |
| damped_osc | 0.1462 | -84.9 | 5 | yes |
| pure_osc | 0.1224 | -87.4 | 4 | yes |

**Frontier** (rh_singularity)

- Best model: **pure_osc**
- Equation: `\delta(L) = 0.0099 \cos(0.5078 L + 0.9677) + 0.0878`
- Asymptotic class: **indeterminate**
- delta(L -> inf) = 0.087808
- R^2 = 0.996120
- BIC = -325.91
- Confidence = 0.06

| Model | R^2 | BIC | Params | Converged |
|-------|-----|-----|--------|-----------|
| constant | 0.0000 | -213.0 | 1 | yes |
| linear | 0.1196 | -212.7 | 2 | yes |
| power_law | 0.1445 | -213.4 | 2 | yes |
| exp_decay | 0.1964 | -211.7 | 3 | yes |
| damped_osc | 0.9964 | -324.8 | 5 | yes |
| pure_osc * | 0.9961 | -325.9 | 4 | yes |

### Twin Primes

**Calibration** (small_gap)

- Best model: **constant**
- Equation: `\delta(L) = 0.0000`
- Asymptotic class: **affirmative**
- delta(L -> inf) = 0.000000
- R^2 = 1.000000
- BIC = -1584.62
- Confidence = 0.15

| Model | R^2 | BIC | Params | Converged |
|-------|-----|-----|--------|-----------|
| constant * | 1.0000 | -1584.6 | 1 | yes |
| linear | 1.0000 | -1581.5 | 2 | yes |
| power_law | 1.0000 | -1581.5 | 2 | NO |
| exp_decay | 0.0000 | -580.4 | 3 | yes |
| damped_osc | 0.0000 | -585.2 | 5 | yes |
| pure_osc | 0.0000 | -585.5 | 4 | yes |

**Frontier** (large_gap)

- Best model: **constant**
- Equation: `\delta(L) = 1.0000`
- Asymptotic class: **gap**
- delta(L -> inf) = 1.000000
- R^2 = 1.000000
- BIC = -1584.62
- Confidence = 0.15

| Model | R^2 | BIC | Params | Converged |
|-------|-----|-----|--------|-----------|
| constant * | 1.0000 | -1584.6 | 1 | yes |
| linear | 1.0000 | -1581.5 | 2 | yes |
| power_law | 1.0000 | -1581.5 | 2 | yes |
| exp_decay | 0.0000 | -580.4 | 3 | yes |
| damped_osc | 0.0000 | -585.2 | 5 | yes |
| pure_osc | 0.0000 | -585.5 | 4 | yes |

### Yang Mills

**Calibration** (bpst_instanton)

- Best model: **constant**
- Equation: `\delta(L) = 0.0796`
- Asymptotic class: **gap**
- delta(L -> inf) = 0.079577
- R^2 = 0.000000
- BIC = -262.69
- Confidence = 0.09

| Model | R^2 | BIC | Params | Converged |
|-------|-----|-----|--------|-----------|
| constant * | 0.0000 | -262.7 | 1 | yes |
| linear | 0.0141 | -259.9 | 2 | yes |
| power_law | 0.0044 | -259.7 | 2 | yes |
| exp_decay | 0.0667 | -258.0 | 3 | yes |
| damped_osc | 0.2936 | -258.0 | 5 | yes |
| pure_osc | 0.2910 | -261.0 | 4 | yes |

**Frontier** (excited)

- Best model: **constant**
- Equation: `\delta(L) = 1.0000`
- Asymptotic class: **gap**
- delta(L -> inf) = 1.000000
- R^2 = 1.000000
- BIC = -1584.62
- Confidence = 0.15

| Model | R^2 | BIC | Params | Converged |
|-------|-----|-----|--------|-----------|
| constant * | 1.0000 | -1584.6 | 1 | yes |
| linear | 1.0000 | -1581.5 | 2 | yes |
| power_law | 1.0000 | -1581.5 | 2 | yes |
| exp_decay | 0.0000 | -580.4 | 3 | yes |
| damped_osc | 0.0000 | -585.2 | 5 | yes |
| pure_osc | 0.0000 | -585.5 | 4 | yes |

### Ym Lattice

**Calibration** (coarse_lattice)

- Best model: **constant**
- Equation: `\delta(L) = 0.3202`
- Asymptotic class: **gap**
- delta(L -> inf) = 0.320153
- R^2 = 0.000000
- BIC = -210.48
- Confidence = 0.13

| Model | R^2 | BIC | Params | Converged |
|-------|-----|-----|--------|-----------|
| constant * | 0.0000 | -210.5 | 1 | yes |
| linear | 0.0198 | -207.8 | 2 | yes |
| power_law | 0.0124 | -207.7 | 2 | yes |
| exp_decay | 0.0198 | -204.7 | 3 | yes |
| damped_osc | 0.2241 | -203.7 | 5 | yes |
| pure_osc | 0.0401 | -202.1 | 4 | yes |

**Frontier** (fine_lattice)

- Best model: **constant**
- Equation: `\delta(L) = 1.0000`
- Asymptotic class: **gap**
- delta(L -> inf) = 1.000000
- R^2 = 1.000000
- BIC = -1584.62
- Confidence = 0.15

| Model | R^2 | BIC | Params | Converged |
|-------|-----|-----|--------|-----------|
| constant * | 1.0000 | -1584.6 | 1 | yes |
| linear | 1.0000 | -1581.5 | 2 | yes |
| power_law | 1.0000 | -1581.5 | 2 | yes |
| exp_decay | 0.0000 | -580.4 | 3 | yes |
| damped_osc | 0.0000 | -585.2 | 5 | yes |
| pure_osc | 0.0000 | -585.5 | 4 | yes |

### Ym Phi4

**Calibration** (ordered_phase)

- Best model: **constant**
- Equation: `\delta(L) = 0.1597`
- Asymptotic class: **gap**
- delta(L -> inf) = 0.159745
- R^2 = 0.000000
- BIC = -281.10
- Confidence = 0.14

| Model | R^2 | BIC | Params | Converged |
|-------|-----|-----|--------|-----------|
| constant * | 0.0000 | -281.1 | 1 | yes |
| linear | 0.0141 | -278.3 | 2 | yes |
| power_law | 0.0046 | -278.1 | 2 | yes |
| exp_decay | 0.0660 | -276.4 | 3 | yes |
| damped_osc | 0.2946 | -276.4 | 5 | yes |
| pure_osc | 0.1852 | -276.3 | 4 | yes |

**Frontier** (critical_point)

- Best model: **pure_osc**
- Equation: `\delta(L) = 0.1081 \cos(1.0013 L + 0.5754) + 0.5503`
- Asymptotic class: **indeterminate**
- delta(L -> inf) = 0.550307
- R^2 = 0.967607
- BIC = -175.45
- Confidence = 0.15

| Model | R^2 | BIC | Params | Converged |
|-------|-----|-----|--------|-----------|
| constant | 0.0000 | -109.3 | 1 | yes |
| linear | 0.0000 | -106.2 | 2 | yes |
| power_law | -0.0043 | -106.1 | 2 | yes |
| exp_decay | 0.0905 | -105.2 | 3 | yes |
| damped_osc | 0.9676 | -172.4 | 5 | yes |
| pure_osc * | 0.9676 | -175.5 | 4 | yes |

### Ym Schwinger

**Calibration** (weak_coupling)

- Best model: **constant**
- Equation: `\delta(L) = 0.3777`
- Asymptotic class: **gap**
- delta(L -> inf) = 0.377696
- R^2 = 0.000000
- BIC = -58.10
- Confidence = 0.13

| Model | R^2 | BIC | Params | Converged |
|-------|-----|-----|--------|-----------|
| constant * | 0.0000 | -58.1 | 1 | yes |
| linear | 0.0002 | -55.0 | 2 | yes |
| power_law | -0.1730 | -51.5 | 2 | yes |
| exp_decay | 0.0546 | -53.1 | 3 | yes |
| damped_osc | 0.2722 | -52.7 | 5 | yes |
| pure_osc | 0.2632 | -55.5 | 4 | yes |

**Frontier** (strong_coupling)

- Best model: **constant**
- Equation: `\delta(L) = 0.5388`
- Asymptotic class: **gap**
- delta(L -> inf) = 0.538804
- R^2 = 0.000000
- BIC = -198.02
- Confidence = 0.08

| Model | R^2 | BIC | Params | Converged |
|-------|-----|-----|--------|-----------|
| constant * | 0.0000 | -198.0 | 1 | yes |
| linear | 0.0141 | -195.2 | 2 | yes |
| power_law | 0.0046 | -195.0 | 2 | yes |
| exp_decay | 0.0637 | -193.3 | 3 | yes |
| damped_osc | 0.2978 | -193.4 | 5 | yes |
| pure_osc | 0.2917 | -196.3 | 4 | yes |

## Two-Class Partition

**AFFIRMATIVE** (delta -> 0, conjecture supported):
- abc (calibration): power_law, delta -> 0.000000
- banach_tarski (calibration): constant, delta -> 0.000000
- bsd_avg_rank (calibration): constant, delta -> 0.000000
- bsd (calibration): constant, delta -> 0.000000
- bsd_function_field (calibration): constant, delta -> 0.000000
- bsd_function_field (frontier): constant, delta -> 0.000000
- bsd_sato_tate (calibration): constant, delta -> 0.000000
- bsd_sato_tate (frontier): constant, delta -> 0.000000
- collatz (calibration): constant, delta -> 0.000000
- collatz (frontier): linear, delta -> 0.000000
- continuum (calibration): constant, delta -> 0.000000
- falconer (calibration): constant, delta -> 0.000000
- falconer (frontier): constant, delta -> 0.000290
- info_paradox (frontier): linear, delta -> 0.000000
- pnp_ac0 (frontier): constant, delta -> 0.000000
- pnp_clique (frontier): constant, delta -> 0.000000
- poincare_4d (calibration): constant, delta -> 0.000000
- twin_primes (calibration): constant, delta -> 0.000000

**GAP** (delta -> eta > 0, structural obstruction):
- abc (frontier): constant, delta -> 0.428571
- banach_tarski (frontier): constant, delta -> 1.000000
- bridge_expander (calibration): damped_osc, delta -> 0.300922
- bridge_expander (frontier): exp_decay, delta -> 0.782552
- bridge_spectral (calibration): exp_decay, delta -> 0.928021
- bridge_spectral (frontier): exp_decay, delta -> 0.939841
- bsd (frontier): constant, delta -> 1.300000
- continuum (frontier): exp_decay, delta -> 0.857038
- cosmo_constant (calibration): power_law, delta -> inf
- cosmo_constant (frontier): constant, delta -> 0.982436
- hodge (frontier): constant, delta -> 0.603552
- hodge_standard (frontier): linear, delta -> inf
- hodge_tate (frontier): linear, delta -> inf
- hodge_transcendental (calibration): linear, delta -> inf
- hodge_transcendental (frontier): linear, delta -> inf
- inverse_galois (calibration): constant, delta -> 0.049840
- inverse_galois (frontier): constant, delta -> 0.698224
- jacobian (calibration): constant, delta -> 0.049734
- jacobian (frontier): constant, delta -> 0.398224
- langlands (calibration): constant, delta -> 0.149734
- langlands (frontier): constant, delta -> 0.498224
- navier_stokes (frontier): damped_osc, delta -> 0.010079
- ns_2d (calibration): constant, delta -> 0.299556
- ns_euler (calibration): constant, delta -> 0.499112
- ns_euler (frontier): constant, delta -> 0.198224
- ns_sqg (calibration): damped_osc, delta -> 0.449300
- ns_sqg (frontier): damped_osc, delta -> 0.698571
- p_vs_np (calibration): constant, delta -> 0.750000
- p_vs_np (frontier): exp_decay, delta -> 0.851637
- pnp_bpp (calibration): constant, delta -> 0.049556
- pnp_bpp (frontier): constant, delta -> 0.050000
- poincare_4d (frontier): constant, delta -> 0.400000
- ramsey (calibration): exp_decay, delta -> 0.495984
- ramsey (frontier): constant, delta -> 1.000000
- rh_dirichlet (calibration): constant, delta -> 0.505222
- rh_dirichlet (frontier): constant, delta -> 0.420710
- rh_fake (calibration): constant, delta -> 0.350710
- rh_fake (frontier): constant, delta -> 0.272397
- rh_function_field (calibration): constant, delta -> 0.902144
- rh_function_field (frontier): constant, delta -> 0.855222
- riemann (calibration): constant, delta -> 0.005495
- riemann (frontier): constant, delta -> 0.242772
- twin_primes (frontier): constant, delta -> 1.000000
- yang_mills (calibration): constant, delta -> 0.079577
- yang_mills (frontier): constant, delta -> 1.000000
- ym_lattice (calibration): constant, delta -> 0.320153
- ym_lattice (frontier): constant, delta -> 1.000000
- ym_phi4 (calibration): constant, delta -> 0.159745
- ym_schwinger (calibration): constant, delta -> 0.377696
- ym_schwinger (frontier): constant, delta -> 0.538804

**INDETERMINATE**:
- bridge_fractal (calibration): pure_osc, delta -> 0.000036
- bridge_fractal (frontier): pure_osc, delta -> 0.048859
- bridge_rmt (calibration): pure_osc, delta -> 0.000189
- bridge_rmt (frontier): pure_osc, delta -> 0.001129
- bsd_avg_rank (frontier): pure_osc, delta -> 0.392789
- hodge (calibration): pure_osc, delta -> 0.020750
- hodge_standard (calibration): pure_osc, delta -> 0.083766
- hodge_tate (calibration): pure_osc, delta -> 0.053766
- info_paradox (calibration): damped_osc, delta -> 0.425907
- navier_stokes (calibration): pure_osc, delta -> 0.399469
- ns_2d (frontier): pure_osc, delta -> 0.498095
- pnp_ac0 (calibration): pure_osc, delta -> 0.163027
- pnp_clique (calibration): pure_osc, delta -> 0.031673
- riemann (frontier): pure_osc, delta -> 0.087808
- ym_phi4 (frontier): pure_osc, delta -> 0.550307

---
_Generated 2026-03-01T10:38:03.074659 by Governing Equations Engine v1.0_
_The spectrometer produces data. This module finds the law._