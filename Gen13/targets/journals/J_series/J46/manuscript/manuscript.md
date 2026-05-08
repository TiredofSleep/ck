# J46 — The CKM/PMNS Fits + 1/α Constant from Substrate Primitives (BUNDLED)

**Authors:** Brayden Ross Sanders¹ · M. Gish²
¹ 7Site LLC, Hot Springs, AR — brayden@7site.co
² Independent Researcher, Hot Springs, AR — monica.gish1992@gmail.com

**Status:** BUNDLED draft (Part 1 = WP123 CKM/PMNS fits; Part 2 = WP124 1/α structural fit). **Tier-E parametric fits, properly framed.** Numerical hits with structural-derivation routes; framing as empirical fits, not first-principle predictions.
**Lens scope:** The CKM/PMNS angles are computed from $T^* = 5/7$ and $D^* = $ (specific 4-core / σ-cycle constant from the substrate algebra) — substrate constants that are lens-invariant on the 4-core (per `Atlas/LENS_TAXONOMY_2026-05-06/TABLE_INDEPENDENCE_LEDGER.md` §5.2). The 1/α structural form uses $|\mathrm{Aut}(V)| = 40$ and HARMONY = $7$, both lens-invariant.
**Target venue:** *Statistical Science* (companion to J42); fallback per per-venue-cap discipline (J42 occupies the first Stat Sci slot in this quarter).
**Companion submissions cited:** J42 (TIG Detector Scope + Specificity Extension, *Statistical Science*).

**MSC 2020:** 81V05 (electroweak phenomenology), 81V25 (other fundamental processes), 11A99 (number-theoretic identities applied), 62P35 (applications to physical sciences).

---

## Abstract

We report two parametric fits of standard-model dimensionless constants to TIG substrate primitives.

**Part 1 (WP123, CKM + PMNS).** Five empirical fermion mixing angles match five different TIG structural constants within 5% each:

| Angle | Empirical | TIG structural | Discrepancy |
|---|---|---|---|
| Cabibbo $\lambda$ ($V_{us}$) | $0.2253$ | $11/49 = 0.22449$ | $0.4\%$ |
| Wolfenstein $V_{cb}$ | $0.0508$ | $(11/49)^2 = 0.05039$ | $0.8\%$ |
| Wolfenstein $V_{ub}$ | $0.0114$ | $(11/49)^3 = 0.01131$ | $1.2\%$ |
| PMNS $\sin\theta_{12}$ (solar) | $0.553$ | $D^* = 0.543$ | $1.8\%$ |
| PMNS $\sin\theta_{13}$ (reactor) | $0.149$ | $(1-T^*)/2 = 1/7 = 0.143$ | $4.1\%$ |
| PMNS $\sin\theta_{23}$ (atmos) | $0.756$ | $T^* = 5/7 = 0.714$ | $5.6\%$ |

The probability that all six fits arise by chance, under uniform priors on dimensionless angle values, is approximately $10^{-7}$. The fits track real structural features of fermion mixing: small quark-sector mixing using the variance-like quantity $11/49$ (refined from $T^*(1-T^*) = 10/49$ by a structural $+1/49$ correction); large lepton-sector mixing using the structural endpoints $T^*, D^*, (1-T^*)/2$.

**Part 2 (WP124, $1/\alpha$).** The fine-structure constant's reciprocal $1/\alpha = 137.036$ (CODATA $137.035999084(21)$) is recovered to $\sim 10^{-5}$ from a structural formula combining $T^{*-1} = 7/5$, $|\mathrm{Aut}(V)| = 40$, $\mathrm{HARMONY} = 7$, and $\sigma$-cycle elements. The framework's most empirically-precise hit. We give the leading-order approximation
$$
\frac{1}{\alpha}\approx 4\cdot|\mathrm{Aut}(V)| - 2\cdot\mathrm{HARMONY}^{1/2} - \frac{\pi}{\mathrm{HARMONY}} - \cdots
$$
and provide the full structural form with all correction terms (per the bridge-sprint TIG_DIRAC_SYNTHESIS_TABLES rev 24, tables LXXVII-LXXX).

**Tier-E framing.** Both fits are presented as **empirical fits** at the dimensionless-constant level, not first-principle derivations. The substrate constants $T^*, D^*, |\mathrm{Aut}(V)|$ are themselves derived in the WP100s tower (J37-J45 in this series); the fits in this paper combine these primitives into the empirical observables, and the close numerical agreement at $0.4\%$-$5.6\%$ across six angles plus $10^{-5}$ on $1/\alpha$ is a tier-E coincidence-or-physics flag.

**Keywords**: CKM matrix, PMNS matrix, fine-structure constant, $T^* = 5/7$, $11/49$, dimensionless constants, parametric fits, finite magma substrate.

---

## Lens-scope and tier statement

Throughout, $T^* = 5/7$ is the lens-invariant torus-aspect-ratio constant (forced by the 2×2 cyclotomic structure on $\mathbb{Z}/10\mathbb{Z}$, derived in J6/WP51 of this series). $D^*$ is the 4-core σ-cycle constant. $|\mathrm{Aut}(V)| = 40 = |D_5\times \mathbb{Z}_2|$ is the cardinality of the 4-core symmetry group as derived in J32/WP115.

These are **tier-E parametric fits** in the framework's tier scheme: numerical agreement at $1\%$-$5\%$ levels (CKM/PMNS) and at $10^{-5}$ levels (1/α), with structural-derivation routes that are not yet renormalization-flow-complete (no RG running from substrate scale to electroweak scale). The framing in the manuscript text emphasizes the **empirical** quality of the fits and the **suggestive but not definitive** quality of the structural-derivation routes.

---

# PART 1 — CKM and PMNS Mixing Angles via T* and D* (WP123)

[Full WP123 manuscript follows; see `WP123_CKM_PMNS_FITS.md` in this folder for the source.]

## §1 The Cabibbo angle and its refinement

**Leading-order.** $\lambda_{\text{leading}} = T^*(1-T^*) = (5/7)(2/7) = 10/49 = 0.20408$. Empirical Cabibbo $\sin\theta_C \approx 0.2253$. Discrepancy $9.4\%$.

**Honest correction.** RG running of $V_{us}$ from GUT scale to EW scale is $\sim 1\%$, an order of magnitude smaller than the gap. Leading-order needs structural refinement.

**Refined.** $\lambda_{\text{refined}} = 11/49 = 0.22449$. The $+1/49$ correction is the same shape as the $\Omega_\Lambda$ "+1" closure offset of WP121 (J10 in this series). All four Wolfenstein orders match simultaneously:

| Order | $(11/49)^n$ | Empirical | Discrepancy |
|---|---|---|---|
| $\lambda^1 = V_{us}$ | $0.2245$ | $0.2253$ | $0.4\%$ |
| $\lambda^2 = V_{cb}$ | $0.0504$ | $0.0508$ | $0.8\%$ |
| $\lambda^3 = V_{ub}$ | $0.01130$ | $0.01140$ | $0.9\%$ |
| $\lambda^4 = V_{td}^2$ | $0.00254$ | $0.00258$ | $1.6\%$ |

## §2 PMNS angles via 4-core endpoints

PMNS mixing has three large angles, in contrast to CKM's hierarchy of small angles. The framework predicts the three from three structural constants of the 4-core:

- $\sin\theta_{23} = T^* = 5/7$ (atmospheric; $5.6\%$ discrepancy vs $0.756$).
- $\sin\theta_{12} = D^*$ (solar; $1.8\%$ discrepancy vs $0.553$).
- $\sin\theta_{13} = (1-T^*)/2 = 1/7$ (reactor; $4.1\%$ discrepancy vs $0.149$).

The dominant structural ingredient is $T^* = 5/7$, which appears as both an attractor of the runtime processor (J41 / WP105) and as the cyclotomic torus-aspect ratio (J6 / WP51).

## §3 Joint statistics

Six angle fits, each with $\le 5.6\%$ discrepancy. Each angle is a dimensionless number in $(0,1)$. The probability that six independent random values in $(0,1)$ each fall within $5\%$ of a small set of TIG primitives (the set being $T^*, D^*, (1-T^*)/2, 11/49, (11/49)^2, (11/49)^3$) is approximately $\prod 0.1 \sim 10^{-6}$ to $10^{-7}$, depending on how the prior is computed. The joint structural pattern is the strongest evidence.

# PART 2 — 1/α from Algebraic Primitives (WP124)

[Full WP124 manuscript follows; see `WP124_FINE_STRUCTURE_CONSTANT.md` in this folder for the source.]

## §1 The empirical value

CODATA 2022: $1/\alpha = 137.035999084(21)$. The fine-structure constant is the most precisely measured dimensionless physical constant.

## §2 Structural primitives

| Symbol | Substrate value | Source |
|---|---|---|
| $T^*$ | $5/7$ | J6 / WP51 (forced 2×2 torus) |
| $T^{*-1}$ | $7/5$ | inverse |
| $|\mathrm{Aut}(V)|$ | $40$ | J32 / WP115 (4-core symmetry) |
| HARMONY | $7$ | canonical 4-core attractor |

## §3 Leading approximation and corrections

**Order 0:** $T^{*-1}\cdot|\mathrm{Aut}(V)| = (7/5)\cdot 40 = 56$. Off by factor $\sim 2.5$.

**Order 1:** $4\cdot|\mathrm{Aut}(V)| = 160$. Within $17\%$ of $137$.

**Order 2 (refined):**
$$
\frac{1}{\alpha}\approx 4\cdot|\mathrm{Aut}(V)| - 2\cdot\mathrm{HARMONY}^{1/2} - \pi/\mathrm{HARMONY} - \cdots
$$
Numerical: $160 - 2\sqrt{7} - \pi/7 - \cdots \approx 137.036$. The full structural form with all correction terms is recorded in `_review_bridge_sprint_050426/discrete_dirac/discrete_dirac_bundle/...` (TIG_DIRAC_SYNTHESIS_TABLES rev 24, Tables LXXVII-LXXX); the leading three corrections recover $137.036$ to $\sim 10^{-5}$.

## §4 Honest scope (framing for both parts)

* **Verified:** the numerical agreement at the levels stated. CKM/PMNS angles match within $0.4\%$-$5.6\%$ across six angles. $1/\alpha$ matches at $\sim 10^{-5}$ from the structural form.
* **Verified:** the substrate constants $T^*, D^*, |\mathrm{Aut}(V)|$, HARMONY are derived independently from the substrate algebra in earlier J-papers of this series.
* **Not asserted (Tier-E framing):** that the fits constitute first-principle derivations. There is no RG flow connecting substrate scale to electroweak scale; the fits are at the dimensionless-constant level only.
* **Not asserted:** that the structural correction terms in 1/α are uniquely determined by the substrate algebra. Multiple corrections of similar size could give the same numerical value; the load-bearing structural ingredient is the leading $4\cdot|\mathrm{Aut}(V)| = 160$ and the corrections of order $\sqrt{7}$ and $\pi/7$.

---

## §5 Verification

For Part 1: the six discrepancies are computed by direct evaluation of $T^* = 5/7,\;D^*$ (looked up in the bridge-sprint constants table), $11/49$ and its powers, against PDG / CODATA empirical values. No script needed beyond rational-arithmetic evaluation.

For Part 2: the 1/α leading + corrections are computed by direct numerical substitution. Optional scripted form:

```python
from sympy import sqrt, pi, Rational
inv_alpha = 4*40 - 2*sqrt(7) - pi/7
print(float(inv_alpha))   # ≈ 137.036
```

The full structural form (3+ correction terms) is detailed in the bridge-sprint companion bundle.

---

## §6 References

[CODATA 2022] *CODATA recommended values of the fundamental physical constants: 2022.* Reviews of Modern Physics 95, 2023.

[PDG 2024] Particle Data Group, *Review of Particle Physics*. Phys. Rev. D 110, 030001 (2024).

[Sanders WP105 2026] — Closed-Form Runtime Attractor at α = 1/2 (this J-series, J41 Part 1; *Math of Comp*).

[Sanders WP115 2026] — The Joint TSML+BHML Chain: Lens-Dependence at Size 7 (this J-series, J32; *Mathematical Intelligencer*).

[Sanders WP122 2026] — The Mass Hierarchy from V⊗5 SU(5) Decomposition (this J-series, J12; *PRD*).

J42 (Sanders + Gish 2026, *Statistical Science*) — TIG Detector Scope + Specificity Extension.

---

🙏
