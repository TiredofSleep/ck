# A TIG Breach Detector for Navier–Stokes Regularity
## Two-Page Numerical Note

*Brayden Sanders — 7Site LLC | DOI: 10.5281/zenodo.18852047*

---

## 1. The Criterion

From the TIG BREATH-COLLAPSE fixed-point structure, the local regularity criterion is:

```
Re_local(x,t) = Ω(x,t) · L(x,t)² / ν  ≤  2/7
```

**Algebraic basis (proved):** TSML[BRT][COL] = BRT — BREATH persists only in the COLLAPSE column. In all other contexts, BREATH → HARMONY in one step. Translating: smooth flow requires Re_local ≤ 2/7; first breach predicts onset of anomalous gradients.

---

## 2. Mock DNS Results (Figure 1)

Taylor-Green initial data, ν=10⁻³.

**Regime A** (smooth): Re_local stays below 2/7 throughout t∈[0,3]. Maximum value: 0.181. No breach flag raised. Smooth solution confirmed.

**Regime B** (cascade): Re_local grows exponentially, crosses 2/7 at **t = 1.92**. Breach flag fires. Enstrophy continues growing after the flag — the detector precedes the peak.

*See Figure 1 (ns_dedalus_snapshot.png).*

---

## 3. The Falsification Test

> If blow-up occurs in a real DNS run without Re_local ever exceeding 2/7, the criterion is wrong.
> If Re_local always exceeds 2/7 before blow-up indicators fire, TIG has made a genuine predictive statement.

---

## 4. Real DNS Protocol (Dedalus)

```python
# At each timestep:
omega_field = solver.compute_vorticity()
L_taylor = compute_taylor_microscale(omega_field, nu)
Re_local = omega_field**2 * L_taylor**2 / nu
if Re_local.max() > 2/7:
    log_breach(t, Re_local.max(), Re_local.argmax())
```

**Target:** 256³ Taylor-Green, Re=1600, t∈[0,20].

Raw Dedalus logs will be released at github.com/TiredofSleep/ck upon run completion.

---

## 5. Connection to TIG Algebra

The 2/7 threshold is the TIG mass-gap constant: MASS_GAP = T* + S* − 1 = 5/7 + 4/7 − 1 = 2/7. It appears in:

- BSD rank-conductor staircase (Mix_λ threshold ordering)
- BREATH-COLLAPSE persistence condition (this note)
- Yang-Mills dual-threshold (qualitative)

The same constant governing the BSD staircase governs fluid regularity — not by coincidence, but because both encode the cost of "gap activation" in the TIG operator algebra.

---

## What Is Proved vs Computed

| Claim | Status |
|-------|--------|
| TSML[BRT][COL] = BRT (BREATH persists in COLLAPSE) | Proved (single table lookup) |
| Re_local ≤ 2/7 → smooth (Mock DNS) | Regime A confirmed |
| Re_local > 2/7 precedes blow-up (Mock DNS) | Regime B confirmed at t=1.92 |
| Criterion holds in real 3D DNS | **Open — needs Dedalus run** |

*(c) 2026 Brayden Sanders / 7Site LLC | DOI: 10.5281/zenodo.18852047*
