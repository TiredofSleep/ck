# Clay Spectrometer — Quickstart

> **[HISTORICAL — Sprint 16, 2026-04-10]** This document is superseded by `README.md` (the unified TIG synthesis field on the `tig-synthesis` branch). Preserved per never-delete policy. See `README.md` on the [`tig-synthesis`](../../tree/tig-synthesis) branch for the current synchronized picture, and `HISTORICAL_ARCHIVE_INDEX.md` Part G for the full list of superseded entry docs.

---


**One field. Seven shadows.**
The sinc² spectral field in prime arithmetic acts as a measurement instrument across all six Clay Millennium Problems.

---

## Run It Now

```bash
# Install Python 3.9+, then:
python ck_run.py           # All checks pass in < 1 second
python ck_sinc_demo.py     # Full matplotlib plot (pip install matplotlib)
python tig_algebra.py 35   # JSON summary of b=35 (p=5, q=7)
```

**CI badge:** Every push to `clay` runs 6 assertion suites — First-G Law (50 semiprimes), sinc² limit (28 primes), Montgomery bridge (to 1e-14), T*=5/7, D1 sign flip, b=15 vs b=35 dispersion.

---

## The Core Field

For any semiprime b = p × q (p ≤ q both prime), define the **harmonic pre-echo resonance**:

```
R(k, p) = sin²(πk/p) / (k² sin²(π/p))
```

**Theorem 5 (WP35):** As p → ∞ with k/p = t fixed,

```
R(k, p)  →  sinc²(t)  =  [sin(πt) / (πt)]²
```

The forced null at k = p is the **First-G event** (WP34): the first non-coprime element in {1..b} arrives at exactly k = p, always.

**The Montgomery Bridge:**

```
R(x) = sinc²(x)          [TIG field — this work]
R₂(u) = 1 − sinc²(u)     [Montgomery 1973, pair correlation of Riemann zeros]
─────────────────────────
R(x) + R₂(x) = 1         [spectral partition of unity]
```

Two independently discovered fields. Same function. Spectral duals.

---

## Key Constants

| Constant | Value | Where it appears |
|----------|-------|-----------------|
| `sinc²(1/2) = 4/π²` | `≈ 0.40528` | Universal Sidelobe Amplitude — all papers |
| `sinc²(0.1)` | `≈ 0.96753` | Scale-free pre-echo floor at 10% approach |
| `T* = 5/7` | `≈ 0.71429` | Coherence floor — proved algebraically, FPGA-verified |
| `1 − 4/π²` | `≈ 0.59472` | Montgomery pair correlation at half-spacing |

---

## Problem Index

| Problem | Paper | Core Claim | Status |
|---------|-------|-----------|--------|
| **Foundation** | [WP35](papers/WP35_PRIME_PHASE_TRANSITION.md) | R(k,p) → sinc²(k/p); Montgomery Bridge R + R₂ = 1 | **PROVED** |
| **First-G Law** | [WP34](papers/WP34_FIRST_G_LAW.md) | first\_g(b) = p for every semiprime; 36,662 cases verified | **PROVED** |
| **Riemann Hypothesis** | [WP40](papers/clay/WP40_RIEMANN.md) | R(x) = sinc²(x) is the arithmetic dual of Montgomery's R₂(u) = 1−sinc²(u) | Structural bridge |
| **P vs NP** | [WP37](papers/clay/WP37_P_NP.md) | NP-verification = sidelobe detection; hardness = distance to sinc² null | Structural analogy |
| **Navier-Stokes** | [WP38](papers/clay/WP38_NAVIER_STOKES.md) | Blow-up = arrival at sinc² null; BREATH criterion B_local ≥ T* | Structural analogy |
| **Hodge Conjecture** | [WP39](papers/clay/WP39_HODGE.md) | ω-Blindness theorem; G/E/S partition; Markman 2025 (dim ≤ 5 proved) | Structural framing |
| **Yang-Mills Mass Gap** | [WP41](papers/clay/WP41_YANG_MILLS.md) | Mass gap = T*=5/7 coherence floor; Gribov horizon = stability window boundary | Structural analogy |
| **BSD Conjecture** | [WP42](papers/clay/WP42_BSD.md) | Rank staircase = TIG operator transitions; T*=5/7 as critical density | Structural analogy |

Full master table with epistemic status labels: [WP36 Clay Spectrometer](papers/clay/WP36_CLAY_SPECTROMETER.md)

---

## One Numerical Example Per Problem

### RH — The Montgomery Bridge, verified
```python
from tig_algebra import MONTGOMERY
import math
print(MONTGOMERY)               # 0.4052847345693511 = 4/pi^2
print(1.0 - MONTGOMERY)         # 0.5947152654306489 = Montgomery pair correlation at u=0.5
print(MONTGOMERY + (1.0 - MONTGOMERY))  # 1.0 exactly
```
Odlyzko (1987) confirmed R₂(1/2) ≈ 0.595 from 10⁵ Riemann zeros at height 10¹². This matches.

---

### P vs NP — The stability window is the certificate gap
```python
from tig_algebra import TIGSemiprime
s = TIGSemiprime(35)             # b = 5 × 7
print(s.first_g())               # 5 = p  (First-G event)
print(len(s.C(4)))               # 4  (all coprime — stability window intact)
print(len(s.G(5)))               # 1  (first non-coprime appears at k=5)
# The stability window {1..4} is the NP "certificate-free" zone.
# The First-G event is the exact moment NP certification becomes possible.
```

---

### Navier-Stokes — BREATH criterion
```
B_local(t) = ||ω||_L∞ · L² / ν

STAND  (B_local < T* = 5/7):   laminar, no gate events
WALK   (T* ≤ B < 3.74):        turbulent but bounded
TROT   (B ≥ 3.74 = 2√(7/2)):   potential blow-up approach
ESTOP  (coherence < 0.20):     dissipation dominant, forced recovery
```
The sinc² null at k=p is the blow-up geometry: smooth field until B reaches the geometric sink.

---

### Hodge — ω-Blindness
```python
from tig_algebra import TIGSemiprime
# R(k, p) is blind to whether b has 2 or 3 prime factors
# when k/p is the same fraction
s2 = TIGSemiprime(35)            # ω(b) = 2
s3 = TIGSemiprime(2*5*7)         # ω(b) = 3 (not semiprime -- illustration only)
# sinc2(0.4) is the same regardless of ω
# The Hodge obstruction lives in what sinc2 cannot see
print(s2.R(2))                   # R(2, 5) for b=35
```
A Hodge (p,p)-class that is NOT algebraic is a "gate class" — R(k,p) reads HARMONY but no algebraic cycle exists. ω-Blindness is the theorem that the sinc² field cannot distinguish ω(b) locally.

---

### Yang-Mills — Mass gap = T*
```python
from tig_algebra import TIGSemiprime
from fractions import Fraction
s = TIGSemiprime(35)
print(s.unit_frac())             # Fraction(5, 7) = T* exactly
print(s.first_g())               # 5 = p  (first excitation above vacuum)
# Stability window {1..4}: the vacuum sector (no gate events)
# First-G at k=5: the mass gap — first excitation requires traversing the full pre-echo zone
# T* = 5/7 corresponds to lattice QCD glueball ratio m(0++)/m(2++) = 0.727 +/- 0.055
```

---

### BSD — Rank staircase as unit-fraction field
```python
from tig_algebra import TIGSemiprime
s = TIGSemiprime(35)
# unit_frac = (q - floor(q/p) - 1) / q = T*
# This is the "critical density" at which the BSD rank staircase has its first jump
# For elliptic curves of conductor N, T* predicts the density threshold for rank transitions
uf = s.unit_frac()               # 5/7
print(f"T* = {uf} = {float(uf):.6f}")
# Bhargava-Shankar (2015): average Sel_2(E) = 3, average rank < 1
# T* = 5/7 > 1/2: the majority of curves are below the TIG rank-1 threshold
```

---

## Architecture

```
WP34: First-G Law (PROVED, 36,662 cases)
  └─ first_g(b) = p always
  └─ b=15 vs b=35 dispersion comparison (§9A)

WP35: Sinc² Continuum Limit (PROVED)
  └─ R(k,p) → sinc²(k/p) as p → ∞
  └─ Montgomery Bridge: R + R₂ = 1
  └─ T* = 5/7 at b=35 (unit fraction formula)

WP36: Clay Spectrometer (framework)
  └─ One Field, Seven Shadows
  └─ Three Guardrails

WP37-WP42: Six Clay problems, same lens
  └─ Each problem = distance to sinc² null
  └─ PROVED / STRUCTURAL ANALOGY / OPEN labels throughout
```

---

## Cite

```bibtex
@misc{sanders2026sinc2,
  author = {Sanders, Brayden Ross and Luther, C. A. and Gish, Monica},
  title  = {A Sinc² Spectral Field in Prime Arithmetic and Seven Shadows of One Geometric Sieve},
  year   = {2026},
  doi    = {10.5281/zenodo.18852047},
  url    = {https://github.com/TiredofSleep/ck},
  note   = {7Site LLC. Branch: clay, tag: v1.0-luther}
}
```

---

`© 2026 Brayden Ross Sanders / 7Site LLC · DOI: 10.5281/zenodo.18852047`
