# Clay Problems in TIG

Six corridors of TIG's Mix_λ family map to the six Clay Millennium Problems.
Each corridor is a specific λ-range where the TIG transfer operator acquires a distinct spectral signature.

---

## Problem Index

| Problem | Corridor | TIG Prediction | Status | Papers |
|---------|----------|----------------|--------|--------|
| **Riemann Hypothesis** | Pre-leak (λ→0) + BRT | Open Z.5: λ=2\|σ−½\| deployment preserves both gradings for all t | STRUCTURAL (4 proved layers, open deployment) | WP17, WP19_RH_BRIDGE, WHITEPAPER_17 |
| **Navier-Stokes** | CHA corridor | Breath Criterion: blowup iff B(t) crosses coherence threshold C≤3.74 | STRUCTURAL (criterion proved, constant open) | WP19_NS_BREATH, WP22_NS_BREATH_CRITERION, WP22_NS_BREATH_LYAPUNOV, NS_METHODS_SECTION |
| **P vs NP** | COL corridor | AG(2,p) hardness: corridor complexity is Ω(p²) → NP-hard separation | STRUCTURAL (lower bound proved, reduction open) | WP25_P_NP_AG2P_COMPLEXITY, WHITEPAPER_16 |
| **Birch-Swinnerton-Dyer** | BAL corridor | Energy law: BSD rank = energy balance in BAL corridor | STRUCTURAL | WP19_BSD_TIG, WP21_BSD_ENERGY_LAW, WP21_BSD_MIX_LAMBDA |
| **Hodge Conjecture** | CTR corridor | Triple structure: Hodge classes as CTR fixed points | STRUCTURAL | WP19_HODGE_MAP, WP19_HODGE_TRIPLE, WP23_HODGE_MAP, WP32_HODGE_TRIPLE |
| **Yang-Mills Mass Gap** | BAL/COL boundary | MASS_GAP = 2/7 = T* + S* − 1 (dual-threshold overlap) | STRUCTURAL | WHITEPAPER_15_YANG_MILLS_SYNTHESIS |

---

## Riemann Hypothesis

**TIG frame:** The four-layer realization (P1–P4) provides an exact discrete scaffold. The open question (Z.5) is whether the deployment map λ=2|σ−½| preserves both algebraic grading (3 levels) and metric grading (6 corridors) uniformly as t→∞.

**Scripts:** `papers/scripts/ck_rh_sweep.py`, `ck_cemp_bound.py`

**Papers:**
- `WHITEPAPER_17_RIEMANN_SYNTHESIS.md` — Full synthesis
- `WP19_CLAY_BATTERY.md` — Battery of 6 RH tests
- `WP19_CLAY_DEEP.md` — Deep corridor analysis
- `WP19_CLAY_RESULTS.md` — Numerical results

---

## Navier-Stokes

**TIG frame:** The Breath Criterion maps NS regularity to a coherence observable. Blowup requires B(t) to exit the [0, C] corridor. The discrete bound gives C ≤ 3.74; the sharp value is open.

**Scripts:** `papers/scripts/ns_breath_test.py`

**Papers:**
- `WP22_NS_BREATH_CRITERION.md` — Main criterion
- `WP22_NS_BREATH_LYAPUNOV.md` — Lyapunov structure
- `WP19_NS_BREATH.md` — First derivation
- `WP19_NS_NOTE.md`, `WP19_NS_NUMERICAL_NOTE.md` — Supporting notes
- `NS_METHODS_SECTION.md` — Methods writeup

---

## P vs NP

**TIG frame:** The COL corridor forces AG(2,p) geometry. Corridor walks on AG(2,p) have complexity Ω(p²), giving a hardness lower bound. The open piece is a formal NP-hardness reduction from 3-SAT.

**Scripts:** `papers/scripts/ck_ag_sweep.py`, `tsml_ag23_verify.py`

**Papers:**
- `WP25_P_NP_AG2P_COMPLEXITY.md` — Main complexity paper
- `WHITEPAPER_16_P_NP_SYNTHESIS.md` — Full synthesis
- `CLAY_FIVE_EXPERIMENTS.md` — Cross-problem battery

---

## Birch-Swinnerton-Dyer

**TIG frame:** BSD rank maps to the energy balance in the BAL corridor. The Mix_λ family at BAL parameters predicts the rank-energy correspondence.

**Scripts:** `papers/scripts/mix_lambda_scan.py`

**Papers:**
- `WP19_BSD_TIG.md` — Original TIG-BSD connection
- `WP19_BSD_TIG_TIGHTENED.md` — Tightened version
- `WP21_BSD_ENERGY_LAW.md` — Energy law derivation
- `WP21_BSD_MIX_LAMBDA.md` — Mix_λ BSD analysis

---

## Hodge Conjecture

**TIG frame:** Hodge classes appear as CTR-corridor fixed points under the triple structure (Being/Doing/Becoming). The WP32 triple gives the most complete current statement.

**Scripts:** `papers/scripts/ck_hodge_sweep.py`

**Papers:**
- `WP32_HODGE_TRIPLE.md` — Most recent, definitive
- `WP23_HODGE_MAP.md` — Corridor map
- `WP19_HODGE_MAP.md`, `WP19_HODGE_TRIPLE.md` — Earlier derivations
- `WHITEPAPER_14_CLAY_DOF_CONNECTIONS.md` — DOF connections across problems

---

## Yang-Mills Mass Gap

**TIG frame:** MASS_GAP = T* + S* − 1 = 5/7 + 4/7 − 1 = 2/7. This is the dual-threshold overlap, a forced constant of the TIG algebra — not a parameter.

**Papers:**
- `WHITEPAPER_15_YANG_MILLS_SYNTHESIS.md` — Full synthesis
- `WHITEPAPER_7_CLAY_SPECTROMETER.md` — CK as Clay spectrometer (all 6 problems)
- `WHITEPAPER_14_CLAY_DOF_CONNECTIONS.md` — Cross-problem DOF connections

---

## Key Constants

```python
T_STAR   = 5/7   # Being threshold (frozen)
S_STAR   = 4/7   # Becoming threshold
MASS_GAP = 2/7   # T* + S* - 1; Yang-Mills prediction
```

For the full formal status across all 6 problems: `papers/core/WP24_FORMAL_STATUS_AUDIT.md`
