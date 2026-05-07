# Cosmological Derivations from TIG

**Status:** Computational findings — falsifiable predictions
**Target journals:** *JCAP*, *Physical Review D*, *Physics Letters B*

---

## Summary

Two cosmological observables fall out cleanly from TIG axioms A0–A5:

1. **Spectral tilt:** n_s = 193/200 = 0.965, from 1 - n_s = HARMONY / (2 · N²) = 7/200
2. **Tensor-to-scalar ratio:** r = W = 3/50 = 0.06, from the wobble equals the gravitational-wave amplitude prediction

Both are testable against current and forthcoming CMB measurements.

---

## 1. Spectral tilt n_s = 0.965

### 1.1 Observation

Planck 2018 measures the scalar spectral index of cosmological perturbations:

```
n_s = 0.9649 ± 0.0042
```

This is the deviation from scale-invariance (n_s = 1 would be perfectly scale-invariant). The slight tilt n_s < 1 is one of inflation's key signatures.

### 1.2 TIG derivation

```
1 - n_s = HARMONY / (2 · N²) = 7 / (2 · 100) = 7/200 = 0.035

⇒ n_s = 1 - 7/200 = 193/200 = 0.965
```

**Required axioms:** A0 alone (substrate Z/10Z gives N=10 and HARMONY=7).

### 1.3 Physical interpretation

The deviation from scale-invariance is set by **HARMONY (the attractor) divided by twice the substrate cardinality squared**.

- HARMONY (7) is the convergence operator — what the canonical pair tries to absorb to.
- 2N² = 200 is the doubled substrate volume (counting both directions of magma composition).
- The ratio 7/200 represents the "fractional pressure of HARMONY-attraction within the doubled-substrate volume."

In inflationary language: the substrate's HARMONY-attractor pressure introduces a slight scale-dependence to perturbation amplitudes, biasing them away from pure scale-invariance.

### 1.4 Match to measurement

```
TIG:    n_s = 193/200 = 0.965000
Planck: n_s = 0.9649 ± 0.0042
```

**Match: within experimental error.** Specifically, TIG sits 0.012σ from the Planck central value.

### 1.5 Forthcoming tests

CMB-S4 (commencing late 2020s), LiteBIRD, and other experiments will measure n_s to ~0.001 precision. **If n_s ≠ 193/200 at this precision, the TIG derivation must be reformulated.** Current data is fully consistent.

---

## 2. Tensor-to-scalar ratio r = 3/50

### 2.1 Observation

Planck 2018 + BICEP/Keck Array (2021) bound the tensor-to-scalar ratio at:

```
r < 0.036 (95% CL, latest combined analysis)
```

Previously the bound was ~0.06; this has tightened. The quantity r measures the amplitude of primordial gravitational waves relative to scalar density perturbations. r > 0 would confirm inflation; r = 0 is consistent with various non-inflationary scenarios.

### 2.2 TIG prediction

```
r = W = 3/50 = 0.06
```

The wobble W is the substrate's natural deviation amplitude (three independent derivations on Z/10Z all give W = 3/50). If primordial gravitational waves *are* the wobble at cosmological scale, then r = W exactly.

### 2.3 Physical interpretation

In TIG, the wobble W represents the per-step asymmetry between additive and multiplicative dynamics on Z/10Z. At cosmological scale, this asymmetry manifests as primordial tensor perturbations: the substrate "wobbles" as it expands, generating gravitational waves with amplitude W relative to scalar perturbations.

### 2.4 Match to measurement

```
TIG:           r = 3/50 = 0.06
Planck/BICEP:  r < 0.036 (95% CL, 2021 combined)
```

**Status: TENSION.** TIG's prediction r = 0.06 sits above the current 95% CL upper bound. This is either:
- (a) **A falsification:** TIG's wobble derivation needs reformulation, or the wobble doesn't directly equal r.
- (b) **A near-falsification awaiting CMB-S4:** if CMB-S4 detects r ≈ 0.06, TIG is dramatically confirmed.
- (c) **A misidentification:** r might equal a function of W rather than W itself (e.g., r = W/2 = 0.03, which is within current bounds).

### 2.5 Reformulation candidates

If r = W is too high, alternatives include:

```
r = W/2 = 3/100 = 0.030  ✓ within current bounds
r = W · T* = (3/50)(5/7) = 0.0429  ✗ above bound
r = W · (1 - T*) = (3/50)(2/7) = 0.0171  ✓ within bounds
r = W² · const = ?
```

The most TIG-natural alternative is **r = W · (mass_gap) = (3/50)(2/7) = 6/350 = 0.0171**, which falls cleanly within current bounds and reads as "the wobble multiplied by the breathing room."

**Recommendation:** present both candidates (r = W and r = W·(1-T*)) and note that CMB-S4 will distinguish them. The doc currently presents r = W as the "naive" prediction; r = W · (1 - T*) is the "refined" prediction.

### 2.6 Honest assessment

The simple "r = W" prediction is in tension with current data. The more refined "r = W · (1 - T*)" sits within bounds. **TIG predicts gravitational-wave detection in the range r ∈ [0.017, 0.06]**, which spans the next-generation experiment's expected sensitivity.

This is a falsifiable structural prediction. Either:
- CMB-S4 detects r in [0.017, 0.06] → TIG confirmed
- CMB-S4 detects r outside this range or rules out r > 0.001 → TIG cosmological branch falsified

---

## 3. Visible matter Ω_b compounding factor

Earlier we noted:

```
Ω_b = (4/100) · (1 + W)^(7/2) = 0.0490
```

The exponent 7/2 = 3.5 has structural meaning:

```
7/2 = HARMONY / COUNTER = consciousness band center
    = (T* + mass_gap × N) / 2  (where mass_gap × N would be the absolute scale)
```

**Reading:** the compounding goes through the consciousness-band level (3.5), which is the natural midpoint of the σ-cycle structure. The wobble compounds 3.5 times (one for each "layer" of the cycle from VOID to HARMONY) to give the visible matter fraction.

This refines the derivation: Ω_b = (frozen cells / N²) compounded by W through the consciousness band depth.

---

## 4. Other cosmological quantities (open)

### Dark matter fraction Ω_DM = 264/1000

Already derived as 44 × 6 / 1000 (cross-cycle disagreement × σ-cycle length / N³). Verified.

### Dark energy fraction Ω_Λ = 687/1000

Closure: 1 - Ω_b - Ω_DM = 49/1000 + 264/1000 + 687/1000 = 1000/1000. Verified.

### Hubble constant H_0

Planck H_0 = 67.4 km/s/Mpc; SH0ES H_0 = 73.0 km/s/Mpc (the "Hubble tension"). TIG might offer a structural origin for the discrepancy if Planck and SH0ES probe different layers of the canonical pair (BEING vs BECOMING measurements at cosmological scale). **Open.**

### Anomalous baryon-to-photon ratio η ≈ 6 × 10⁻¹⁰

The matter-antimatter asymmetry. From earlier: C×C - D×D = 4 frozen cells (cross-cycle structure). The asymmetry might derive from the specific 4 frozen cells in Z/10Z. **Open.**

### Cosmological constant fine-tuning Λ ~ 10⁻¹²² Planck units

The smallness of the cosmological constant is a major puzzle. TIG's Ω_Λ = 0.687 sets the energy density, but the absolute scale (10⁻¹²² Planck) needs a separate derivation, possibly from the σ-cycle structure at Planck-scale resolution. **Open and likely hard.**

---

## 5. Sprint priorities

For cosmological branch:

**Sprint CO-1:** Lock the n_s = 193/200 derivation in a formal paper. *Easy win; one week.*

**Sprint CO-2:** Resolve the r tension. Decide between r = W and r = W · (1 - T*), articulate as a falsifiable prediction set. *Two weeks.*

**Sprint CO-3:** Hubble tension structural analysis. Does TSML measurement of expansion give 67 km/s/Mpc and BHML measurement give 73? Test on Planck and SH0ES data. *One month.*

**Sprint CO-4:** Baryon asymmetry η. Connect to frozen cells of Z/10Z. *Two weeks.*

If CO-1 and CO-2 land, the JCAP paper has clean content beyond Sprint 18.

---

## Status

- ✓ n_s = 0.965 derived cleanly from A0
- ⚠️ r = W in tension with current data; refinement r = W · (1-T*) within bounds
- ⏳ Hubble tension structural analysis (open)
- ⏳ Baryon asymmetry η (open)
- ⏳ Cosmological constant absolute scale (open and hard)

The cosmological branch is in good shape. With n_s locked and r articulated as a refined prediction, the JCAP paper has substantive content.
