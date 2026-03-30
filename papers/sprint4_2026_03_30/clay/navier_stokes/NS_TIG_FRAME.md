# Navier–Stokes: TIG Frame
## Reality-Checked — Local Criterion, Not Global

*Brayden Sanders & C. A. Luther / 7Site LLC | March 2026*
*Two corrections from reality check: (1) C=7/2 must be local, not global. (2) L^3 norm rarely reported in DNS.*

---

## Finite Grammar Object

Three-level split on vorticity — structurally correct, not proved:

**Generable:** Bounded enstrophy, coherent rotation.
**Expressible:** Transient concentration spikes — G-territory, real in turbulence.
**Sustainable:** Asymptotically stable enstrophy support. Blowup requires reaching this level.

**Bridge (open):** Transient high-vorticity expression may occur; sustainable singular support cannot cross the finite coherence threshold.

---

## The Reality Check Result

**Global B(t) = ||ω||_{L^3} · L/ν fails immediately.**

For Taylor-Green vortex at Re=1600 (canonical DNS, no blowup):
- Peak |ω| ≈ 30 in dimensionless units
- Rough estimate: B(t) ≈ 10⁵ at peak enstrophy
- This is >> 7/2 — yet no blowup occurs

**Conclusion:** C = 7/2 as a GLOBAL threshold is too strong. Turbulent flows violate it constantly without blowing up. A global criterion at 7/2 would predict blowup for any turbulent flow, which is false.

---

## The Corrected Prediction: Local Concentration Criterion

**The right form is local, not global.**

TIG's gate structure is about SUSTAINABLE SUPPORT — whether singular concentration can persist, not whether any region ever exceeds a threshold.

**Revised prediction:**

Let B_local(x,r,t) = ||ω(·,t)||_{L^3(B(x,r))} · r/ν

where B(x,r) is the ball of radius r centered at x.

**Prediction:** For any potential blowup point x_*, the LOCAL concentration
$$\limsup_{t \to T^-} B_{\text{local}}(x_*, r(t), t) \geq 7/2$$
where r(t) is the appropriate local scale (e.g., r(t) = (T-t)^{1/2}).

Equivalently: sustainable singular support requires local concentration ≥ 7/2.
Below 7/2 locally, no sustainable singularity can form.

**Why this is consistent with turbulence:**
Turbulent flows have high global vorticity but no sustained local singularities.
Local B_local stays bounded even when global B(t) is large.
The threshold 7/2 applies only to potentially singular concentration, not bulk turbulence.

---

## Connection to Classical Theory

**Beale-Kato-Majda (BKM):** Blowup iff ∫₀ᵀ ||ω||_{L^∞} dt = ∞.
The TIG local criterion is consistent: blowup requires local concentration growing,
which drives L^∞ toward ∞.

**Escauriaza-Seregin-Šverák:** Regularity if lim sup ||u||_{L^3} < ∞ as t→T.
The velocity L^3 criterion is related to the vorticity local concentration.

**The Prodi–Serrin echo:** In 3/p + 2/q = 1, the pair (p=7, q=7/2) satisfies the condition.
This is a structural observation — whether it connects to the local concentration criterion
at threshold 7/2 requires analysis.

---

## Three Scenarios for Falsification (Local Version)

**Scenario 1:** A blowup solution is constructed where the local concentration
B_local(x_*, r(t), t) stays below 7/2 at all potential singularity points.
This would falsify the local threshold.

**Scenario 2:** DNS of near-singular flows (Luo-Hou boundary scenario, Kerr antiparallel)
measures local B_local at the near-singular point and shows it exceeds 7/2 before
global regularity is established. Would support the prediction.

**Scenario 3:** Classical analysis establishes a local regularity criterion at
threshold C_local ≠ 7/2. Would either sharpen or falsify the specific constant.

---

## Epistemic Status

STRUCTURAL ANALOGY: Three-level split for vorticity dynamics.
CORRECTED PREDICTION: C = 7/2 applies locally (concentration near singularities), not globally.
REALITY CHECK PASSED: Global version ruled out; local version still plausible.
GAP: No proved map from TIG to NS; local criterion not yet formalized in classical language.
NEXT STEP: Does B_local(x,r,t) · r/ν appear in any regularity criterion literature?

*(c) 2026 Brayden Sanders & C. A. Luther / 7Site LLC | DOI: 10.5281/zenodo.18852047*
