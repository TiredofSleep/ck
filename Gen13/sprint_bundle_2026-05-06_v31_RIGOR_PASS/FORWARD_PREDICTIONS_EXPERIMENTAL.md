# TIG Forward Predictions — Experimentalist's Reference

**Status:** Falsifiable predictions for forthcoming and improving experiments
**Date:** 2026-05-06 — keeping the ropes pulling
**Audience:** experimentalists evaluating TIG against measurements

---

## Why this document

The TIG framework predicts ~140 numerical correspondences with measured Standard Model parameters. To be falsifiable, it must also predict **values of forthcoming or improving measurements**. This document catalogues TIG's bounded predictions for experiments planned in the next 5-15 years.

Each prediction is given with:
- **TIG attractor** (the predicted central value)
- **Coherence band** (allowed deviation)
- **Measurement timeline** (which experiment will test)
- **Falsification criterion** (what would refute TIG)

---

## 1. Higgs sector (HL-LHC, FCC-ee, FCC-hh)

### Higgs cubic self-coupling κ_3 = λ_3/λ_3_SM

```
TIG attractor:    κ_3 = 1.000   (LATTICE = substrate-fundamental)
Coherence band:   ±W_BHML = ±0.030 (3.0%)
Allowed range:    [0.970, 1.030]
Layer:            BHML (alive, gauge-mediated)

Current bound:    -0.4 < κ_3 < 6.1 (HL-LHC projected ~5%)
FCC-ee precision: ±1%
FCC-hh precision: ±5%
```

**Falsification:** HL-LHC measurement κ_3 outside [0.97, 1.03] would indicate BSM Higgs sector beyond TIG's BHML-band prediction.

### Higgs quartic coupling κ_4 = λ_4/λ_4_SM

```
TIG attractor:    κ_4 = 1.000
Coherence band:   ±W_BHML  
Allowed range:    [0.970, 1.030]
Currently:        Unconstrained
FCC-hh expected:  ±50% (still loose)
```

### λ_H value

```
TIG attractor:    λ_H = 13/N² = 0.130 (DOING layer)
Coherence band:   ±W_DOING = ±0.0044 (3.4%)
Allowed range:    [0.126, 0.134]
Currently measured: 0.1294 ± ~30%
FCC sensitivity:    ±5%
```

Within band currently; tightening test ahead.

---

## 2. Muon g-2 (Fermilab final + Future BNL)

```
TIG attractor:    Δa_μ = BALANCE²/N^N = 25/10¹⁰ = 2.5 × 10⁻⁹
Coherence band:   ±W_DOING = ±3.4%
Allowed range:    [2.41, 2.59] × 10⁻⁹

Current Fermilab+BNL: (2.51 ± 0.59) × 10⁻⁹
Final Fermilab E821 will reach: ±0.20 × 10⁻⁹
```

**Falsification:** Final Fermilab measurement falling outside [2.4, 2.6] × 10⁻⁹ would refute the BALANCE²/N^N attractor. Within current uncertainty TIG matches at 0.4%.

---

## 3. CMB sector (CMB-S4, Simons Observatory)

### Tensor-scalar ratio r

```
TIG attractor band: r ∈ [0.017, 0.06]
Current bound:      r < 0.036 (BICEP/Keck/Planck 2022)
CMB-S4 sensitivity: r ~ 0.001
```

**Two-sided falsification:**
- Lower bound: if CMB-S4 measures r < 0.017 cleanly, TIG is constrained
- Upper bound: if r > 0.06 is measured, TIG is constrained

Either falsifies the framework's r prediction band.

### Tensor spectral tilt n_t

```
TIG prediction: n_t = -r/8 (single-field consistency)
For r = 0.017-0.06: n_t = -0.0021 to -0.0075
CMB-S4 sensitivity: ~0.001
```

**Falsification:** any n_t outside [-0.008, -0.002] would refute TIG inflation.

### Σm_ν (cosmological neutrino sum)

```
TIG prediction (NO): Σm_ν = m_1 + m_2 + m_3 ≈ 0.001 + 0.009 + 0.05 ≈ 0.060 eV
Coherence band:     ±W_DOING ≈ ±0.002 eV
Allowed range:      [0.058, 0.062] eV

Current bound:      Σm_ν < 0.12 eV (Planck+BAO)
CMB-S4 sensitivity: 0.04 eV
```

**Falsification:** if CMB-S4 + DESI + Euclid measure Σm_ν > 0.10 eV (which would imply IO), TIG NO prediction fails.

---

## 4. Neutrino sector (DUNE, JUNO, KamLAND-Zen)

### Mass ordering

```
TIG prediction:   NORMAL ordering (m_1 < m_2 < m_3)
Reasoning:        σ-cycle ascending direction = generation order
Confidence:       Determined by axiom A0 (substrate ordering)
DUNE/JUNO will resolve: by 2030
```

**Falsification:** if DUNE measures inverted ordering at 5σ, TIG axiom A0's σ-orientation must be revisited.

### 0νββ effective mass m_ββ

```
TIG prediction (NO): m_ββ ~ 0.001 eV ~ 1 meV
KamLAND-Zen current: < 36-156 meV (90% CL)
Future (LEGEND-1000): ~10 meV sensitivity

If TIG is correct, 0νββ won't be discovered until next-next-generation experiments.
```

### CP phase δ_CP (PMNS)

```
Current measurement (T2K): δ_CP ≈ -π/2 (~−90°)
TIG attractor: δ_CP = arctan(η̄/ρ̄) = arctan(36/16) ≈ 66° (different sign convention)

Need to standardize convention before comparing
DUNE will measure to ~5° precision
```

---

## 5. Right-handed neutrino sector (LHC, future colliders)

```
TIG prediction:   M_R ~ 10^15 GeV (log_10 M_R = 3·BALANCE = 15)
Mechanism:        Type-I seesaw with y_ν ~ y_t and m_ν ~ 0.05 eV
Direct discovery: not possible at any current collider
Indirect signatures: leptogenesis-induced baryon asymmetry
```

**Falsification:** if a right-handed neutrino is discovered at much lower scale (e.g., TeV), TIG seesaw mass prediction fails.

---

## 6. Strong CP / Axion (ADMX, HAYSTAC, IAXO)

### θ_QCD bound

```
TIG attractor: θ_QCD = 0 (VOID = substrate fundamental for QCD)
Current bound: |θ_QCD| < 10⁻¹⁰ (n EDM)
Future (proton storage ring EDM): ~10⁻¹³ sensitivity
```

**Reading:** TIG predicts θ_QCD is exactly zero up to substrate-wobble corrections. If the next-generation EDM experiments measure |θ_QCD| > 10⁻¹², TIG must accommodate via dynamical PQ relaxation.

### Axion mass m_a

```
TIG window:    m_a ~ 1/N^σ-cycle to 1/N^PROGRESS eV = 10⁻⁶ to 10⁻³ eV
Specific:      m_a ~ 1/N^5 = 10⁻⁵ eV
ADMX:          probing 2-25 μeV (m_a ~ 10⁻⁶ to 10⁻⁵ eV)
HAYSTAC:       18-50 μeV
```

**Falsification:** if axion is found outside [10⁻⁶, 10⁻³] eV, TIG axion-mass prediction fails. If never found despite full coverage, axion solution is ruled out (TIG may need different strong-CP solution).

---

## 7. Dark matter (XENONnT, LZ, DARWIN)

```
TIG candidates:   m_DM = 264 GeV (44·σ-cycle in GeV) or 54 GeV (lighter)
Direct detection: σ_SI ~ ?  (TIG doesn't predict cross-section directly yet)

Current bound:    σ_SI < 10⁻⁴⁷ cm² for ~30 GeV WIMP (XENONnT)
DARWIN sensitivity: 10⁻⁴⁹ cm²
```

**Falsification:** DARWIN excluding 264 GeV WIMP at all couplings would refute TIG heavy-WIMP candidate. 54 GeV candidate is harder to exclude.

---

## 8. Coupling identity (HL-LHC, FCC-ee, MOLLER, P2)

The coupling identity:
```
α_em⁻¹(0) - α_em⁻¹(M_Z) - α_s(M_Z) = RESET = 9
```

Currently holds at sub-0.001%. Future improved measurements should preserve:

```
α_em⁻¹(M_Z) precision target: 0.01 (current 0.018)
α_s(M_Z) precision target:     0.0005 (current 0.0009)

If improved values give RESET-side ≠ 9.000 ± 0.005, TIG identity fails.
```

This is the **single sharpest falsifiable prediction** of the entire framework, because three independent measurements must combine to give an integer.

---

## 9. Higgs precision (FCC-ee)

The flagship Higgs values predicted by TIG:

```
m_H:     125 GeV (BALANCE³)        | current 125.25 ± 0.17
v:       246 GeV (N² + 146)         | current 246.22 (essentially exact)
m_W:     80 GeV (BREATH·N)          | current 80.379 ± 0.012
m_Z:     91 GeV (HARMONY·13)        | current 91.188 ± 0.002
sin²θ_W: 7/30 (MS-bar)              | current 0.23129 ± 0.00005
```

FCC-ee precision targets:
```
m_W: ±0.5 MeV (currently ±12 MeV) — 25× improvement
m_Z: ±0.05 MeV (currently ±2 MeV) — 40× improvement  
sin²θ_W: ±0.00001 (currently ±0.00005) — 5× improvement
m_H: ±10 MeV (currently ±170 MeV) — 17× improvement
```

**TIG falsification:** if any of these tightening measurements lands cleanly *outside* its TIG band, the framework's gauge-Higgs sector fails.

---

## 10. Cosmological constant (next-gen surveys)

```
TIG: log_10(Λ_QFT/Λ_obs) = N² + skeleton + COUNTER = 122 + 2 = 124
Currently ~120-124 (estimate-dependent)
```

This is a hierarchy match, not a measurement. If improved theoretical estimates of Λ_QFT and Λ_obs combine to exponent ≠ 124, TIG cosmological constant reading fails.

---

## 11. Summary table

| Quantity | TIG attractor | Band | Experiment | Timeline |
|---|---|---|---|---|
| κ_3 (Higgs cubic) | 1.000 | ±0.030 | HL-LHC, FCC | 2030-2040 |
| λ_H | 0.130 | ±0.004 | FCC | 2040+ |
| Δa_μ × 10⁹ | 2.5 | ±0.085 | Fermilab final | 2025-2027 |
| r (tensor) | [0.017, 0.06] | — | CMB-S4 | 2030 |
| n_t | [-0.008, -0.002] | — | CMB-S4 | 2030 |
| Σm_ν | 0.060 eV | ±0.002 | CMB-S4+Euclid | 2030 |
| ν ordering | NORMAL | — | DUNE, JUNO | 2030 |
| m_ββ (NO) | ~1 meV | factor 5 | LEGEND-1000 | 2035+ |
| M_R | 10^15 GeV | factor 3 | leptogenesis | 2030+ |
| θ_QCD | 0 | substrate VOID | EDM upgrades | ongoing |
| m_a | 10^-5 eV | factor 10 | ADMX/HAYSTAC | 2025+ |
| m_DM | 264 GeV or 54 | within 3% | DARWIN | 2030 |
| m_W | 80 GeV | ±2.4 GeV | FCC-ee | 2040+ |
| m_Z | 91 GeV | ±2.7 GeV | FCC-ee | 2040+ |
| sin²θ_W | 0.2333 | ±0.008 | FCC-ee | 2040+ |
| Cross-coupling identity | RESET = 9 | ±0.005 | combined | 2035+ |

---

## 12. Single sharpest falsifier

If forced to pick **one** experiment whose outcome would most cleanly determine TIG's fate:

> **The combined precision measurement of α^-1(0), α^-1(M_Z), and α_s(M_Z) at FCC-ee.**

If they combine to:
- α^-1(0) - α^-1(M_Z) - α_s(M_Z) = 9.000 ± 0.005 → strong confirmation
- α^-1(0) - α^-1(M_Z) - α_s(M_Z) = ≠ 9 cleanly → TIG cross-coupling identity fails

This single combined measurement settles the framework's structural identity claim.

---

## 13. What success would imply

If a substantial fraction of these predictions hold at the TIG-required precision, the framework will have demonstrated:

- A 10-element finite substrate generates Standard Model parameters
- Particle counts, coupling values, and RG flows are algebraically determined
- Standard Model is not random; it sits at substrate attractors

This would represent **a structural derivation of the Standard Model from first principles** — the goal that has eluded high-energy physics for half a century.

---

## 14. What failure would imply

If multiple predictions cleanly fail at TIG precision, the framework needs:

- Either revision of the substrate axioms (likely A4 or A5)
- Or extension to a different ring than Z/10Z
- Or rejection as a fitted-numerology framework

The honest path is to **test, document, and revise based on outcomes**.

---

## References

All measurement and experimental references from prior bundle documents. Key forthcoming experiments:

- HL-LHC: ATLAS-CONF-2022-074, CMS-FTR-22-009.
- FCC-ee: Abada, A. et al., *Eur. Phys. J. C* **79**, 474 (2019).
- CMB-S4: Abazajian, K. et al., arXiv:1907.04473 (2019).
- DUNE: Abi, B. et al., *J. High Energy Phys.* **2020**, 173 (2020).
- KamLAND-Zen: Gando, A. et al., *Phys. Rev. Lett.* **130**, 051801 (2023).
- ADMX: Du, N. et al., *Phys. Rev. Lett.* **120**, 151301 (2018).
- DARWIN: Aalbers, J. et al., *J. Cosmol. Astropart. Phys.* **11**, 017 (2016).
- LEGEND-1000: Abgrall, N. et al., arXiv:2107.11462 (2021).
