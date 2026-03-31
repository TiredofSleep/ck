# WP38 — Navier-Stokes Through the TIG Lens
## The BREATH Criterion and Zero-Width Phase Transitions in Vorticity Fields

*Brayden Ross Sanders (7Site LLC) & C. A. Luther*
*March 2026 | DOI: 10.5281/zenodo.18852047*
*Status: Structural framing — analogical connections, not a proof of NS regularity*

---

## Abstract

CK's BREATH operator measures coherence across the TIG pipeline — when BREATH collapses
below T* = 5/7, the system enters a turbulent dissipation regime. This paper argues the
NS regularity problem maps onto a question about whether the BREATH criterion can maintain
itself under vorticity accumulation. The zero-width phase transition (WP35) — proved across
70 worlds with zero exceptions — provides the sharpest available analogy: a single algebraic
event (the First-G Law, WP34) triggers irreversible field distortion. The Luther Dispersion
Conjecture frames concentrated vs spread vorticity as the geometric variable governing the
transition. All NS connections stated here are structural analogies; no proved map from TIG
algebra to NS dynamics is claimed.

---

## §1. The NS Regularity Problem in TIG Terms

The Clay Millennium Problem asks: given smooth, finite-energy initial data u₀ on ℝ³, does
the Navier-Stokes system

    ∂u/∂t + (u·∇)u = ν∆u − ∇p,    ∇·u = 0

admit a smooth global solution, or can finite-time blowup occur?

In TIG terms, the question is structurally parallel to whether the CK coherence field
remains above T* = 5/7, or whether it collapses irreversibly.

### 1.1 The BREATH Operator

> *BREATH, T*, TSML, BHML, D2, CK, and the TIG framework are the exclusive intellectual
> property of Brayden Ross Sanders / 7Site LLC, developed over 18 months prior to this
> sprint. C. A. Luther's contribution is the dispersion conjecture applied to the number
> theory; he has no claim to the CK architecture or its derived constants.*

The BREATH operator (operator index 8 in the TIG table) is CK's coherence-measurement
primitive. It measures D2 curvature across the full TIG pipeline. From the TSML operator
table:

    BRT ∘ COL  = BRT    ← persists (one surviving context)
    BRT ∘ x    ∈ {HAR, VOID}   for all other x ∈ {0..9}

BREATH persists in exactly one context: COLLAPSE (operator 4, the viscous dissipation
analog). Every other context destroys smooth structure in a single step. This is a
one-table algebraic fact, not a hypothesis.

### 1.2 The B_local Split

Define two coherence quantities:

    B_local(x, r, t) = ||ω(·,t)||_{L³(B(x,r))} · r/ν

    B_global(t)      = ||ω(·,t)||_{L³} · L/ν

where B(x,r) is the ball of radius r centred at x, L is the global domain scale, and ω = ∇×u.

**Key correction from NS_TIG_FRAME reality check (Sprint 4):** B_global fails as a
threshold. For the Taylor-Green vortex at Re = 1600, B_global >> 7/2 at peak enstrophy
— yet no blowup occurs. A global threshold at C = 7/2 would predict blowup for ordinary
turbulence, which is false. The correct TIG prediction is local:

    Prediction (structural): any potential blowup point x* requires
        limsup_{t → T⁻} B_local(x*, r(t), t) ≥ 7/2
    where r(t) is the appropriate local scale (e.g., r(t) = (T−t)^{1/2}).

Below 7/2 locally, no sustainable singularity can form. This is consistent with turbulence:
high global vorticity but no sustained local singularities.

### 1.3 The TIG Reframing Table

| Classical NS statement                | TIG analog                                       |
|---------------------------------------|--------------------------------------------------|
| Does smooth solution exist for all t? | Does BREATH persist for all t?                   |
| Does finite-time blowup occur?        | Does context permanently leave COLLAPSE column?  |
| Serrin regularity conditions          | E(t)·Δt ≤ (2/7)·ν (BREATH-COLLAPSE criterion)  |
| Local regularity at potential blowup  | B_local < 7/2 at every potential singular point  |

The constant 2/7 = T* + S* − 1 is the TIG dual-threshold overlap. It is not tuned — it
emerges from the algebraic structure of the coherence table.

---

## §2. The Zero-Width Transition as Structural Support

WP34 (First-G Law) and WP35 (Prime Phase Transition) together prove that in the TIG finite
ring model, the coherence-to-incoherence transition is a perfect step function.

### 2.1 The First-G Law (WP34 — Proved)

For every semiprime b = p × q with p ≤ q, the coprimality partition

    C_k = { x ∈ {1..k} : gcd(x, b) = 1 }     (coherent elements)
    G_k = { x ∈ {1..k} : gcd(x, b) > 1 }     (obstructing elements)

transitions at exactly k = p:

    |G_k| = 0   for all k < p          (fully coherent alphabet)
    |G_p| = 1   (p itself, first obstruction)

Proof is elementary and complete (see WP34 §3). Verified against 36,662 cases.

### 2.2 Zero-Width Gate Rate (WP35 — Proved, 70 worlds)

The gate rate sequence derived from the First-G Law collapses at exactly k = p:

    gate_rate = 1.0   for all k < p    (pre-echo zone, fully coherent)
    gate_rate = 0.0   at k = p         (instant collapse, zero transition width)
    gate_rate = 0.0   for all k > p    (post-gate zone, incoherent)

Verified across 70 semiprime worlds with zero exceptions. The gate has exactly zero width
— it is not a steep gradient, it is a true step function.

**NS analog (structural):** If NS blowup exists, the TIG framework predicts it would be a
zero-width event — the solution is smooth everywhere, then singular at one point in time.
There is no predicted partial coherence near the boundary. This is not an assumption; it
is a consequence of TIG's gate algebra. The zero-width proof supports framing the NS
regularity-singularity boundary as sharp rather than gradual.

*This is a structural analogy. No proved reduction from gate algebra to NS dynamics exists.*

---

## §3. Luther Dispersion → Vorticity Spread

### 3.1 The Luther Dispersion Conjecture

The dispersion conjecture (C. A. Luther, WP34 §9) states:

    gate_rate ≈ F_k( |G| × dispersion(G) )

where dispersion(G) is the spread of non-unit elements across the alphabet. Luther metric:

    M_Luther = |G| × dispersion(G)

Low M_Luther (concentrated obstruction): high gate coherence, smooth flow analog.
High M_Luther (spread obstruction): low gate coherence, turbulent analog.

### 3.2 NS Translation

In fluid dynamics, vorticity is not uniformly distributed — it concentrates in coherent
structures or disperses across the flow. The Luther metric translates as:

    |G|           →  number of active high-vorticity regions
    dispersion(G) →  their spatial spread across the domain

**Prediction (structural):** Flows with concentrated vorticity (few tight cores, low
M_Luther analog) are harder to drive to singularity than flows with dispersed turbulence
(high M_Luther analog). This is consistent with physical intuition — concentrated vorticity
in a single filament is less dangerous than distributed vorticity with strong local
concentrations.

*This analogy is untested in NS. No formal reduction from M_Luther to NS regularity criteria
exists. It is noted as structural motivation for the local concentration framing of B_local.*

### 3.3 Connection to Classical Theory

The Prodi-Serrin class (3/p + 2/q = 1) contains the pair (p=7, q=7/2). This is a
structural observation — whether it connects to the B_local threshold at 7/2 requires
classical analysis. The connection is noted, not claimed.

Beale-Kato-Majda: blowup iff ∫₀ᵀ ||ω||_{L^∞} dt = ∞. The TIG local criterion is
consistent: any sustained local singularity requires B_local growing, which drives
||ω||_{L^∞} toward infinity.

Escauriaza-Seregin-Šverák: regularity if lim sup ||u||_{L³} < ∞ as t → T. The velocity
L³ criterion is structurally related to the B_local vorticity concentration measure.

---

## §4. The Pre-Echo Countdown as Spectral Precursor

### 4.1 The Harmonic Resonance Formula (WP35 — Proved)

WP35 Theorem 5 establishes a closed-form spectral precursor before the First-G transition.
For modulus b with prime factor f, the harmonic resonance in the unit alphabet at size k is:

    R(k, f) = sin²(πk/f) / (k² sin²(π/f))

Properties (all proved in WP35):
- Decays smoothly as k → f: R(f−1, f) = 1/(f−1)²
- Collapses to exactly 0 at k = f (the First-G event)
- R(k, 1/p) is ω-blind: identical for b = p², b = p×q, b = p×q×r
- Scale-invariant: the same sinc² structure appears at every scale

The field "counts down" to the gate — the spectrum knows the transition is coming before
it activates.

### 4.2 NS Analog

In turbulent flows, pre-singularity behavior — growing ||ω||_{L^∞}, tightening coherent
structures, narrowing vortex filaments — corresponds structurally to this countdown.

**Structural conjecture:** If NS blowup has a spectral precursor, it should appear as a
scale-invariant signal consistent with the sinc² template above. The decay profile

    R(k, f): smooth → 1/(f−1)² → 0    (step at k=f)

is a candidate shape for the spectral precursor near a potential singularity.

The sinc² scale-invariance of the pre-echo field raises a further question: is this
structure related to Kolmogorov's k^{-5/3} energy cascade scaling? Both are power-law
forms in frequency space. This is an open question, not a claim.

*All pre-echo/NS connections here are structural analogies. The finite ring model and NS
dynamics are distinct mathematical systems.*

---

## §5. The Lyapunov Approach and the Clay Gap

### 5.1 The Dimensionless Criterion

The BREATH-COLLAPSE criterion from WP22 becomes dimensionless via the local Reynolds number:

    Re_local(x, t) = Ω(x, t) · L(x, t)² / ν   ≤   2/7

where L(x, t) is the local length scale and Ω is local enstrophy density.

**TIG prediction:** Re_local ≤ 2/7 everywhere ⟹ BREATH persists in COLLAPSE context
⟹ smooth solution continues.

### 5.2 The Lyapunov Functional

Define the supremum Lyapunov functional:

    V(t) = sup_{x ∈ domain} Re_local(x, t)

For V to be self-reinforcing (a true Lyapunov function), need dV/dt ≤ 0 when V = 2/7.

The enstrophy equation is:

    ∂Ω/∂t = −2ν|∇ω|² + S     where S = 2(ω·∇)u·ω

Dissipation (−2ν|∇ω|²) is always negative. Vortex stretching (S = 2(ω·∇)u·ω) can be
positive — this is the obstacle.

### 5.3 The Interpolation Target

At the threshold V = 2/7, scaling gives:

    S ≤ 2ν|∇ω|²   ⟺   Re_shear(x, t) ≤ 2

The two conditions relate through the interpolation inequality:

    Re_shear ≤ C · Re_local^{1/2}

If Re_local ≤ 2/7, then Re_shear ≤ C · √(2/7) ≈ 0.535·C.

**For C ≤ 3.74: dissipation dominates stretching at the threshold → V is a Lyapunov
function → global regularity follows.**

### 5.4 The Open Gap

| Step                                              | Status                        |
|---------------------------------------------------|-------------------------------|
| BREATH persists iff V ≤ 2/7                       | Proved (TIG table lookup)     |
| V = Re_local is dimensionless and scale-invariant | Fixed (Sprint 4)              |
| V ≤ 2/7 ⟹ Re_shear ≤ 2                          | Derived (scaling at threshold)|
| Re_shear ≤ C · Re_local^{1/2}                    | Standard interpolation form   |
| C ≤ 3.74 → Lyapunov closes                        | **Open — this is the Clay gap**|

TIG specifies the target constant (2/7) and the proof structure. The analytic work
remaining is establishing the sharp interpolation constant C from NS energy estimates.
This is the same family of sharp inequalities Ladyzhenskaya, Serrin, and
Caffarelli-Kohn-Nirenberg were after. TIG gives a numerical target; the classical analysis
must confirm or refute it.

---

## §6. Contact: Grujić (UVA)

Zoran Grujić (University of Virginia) works on the local-to-global regularity problem in
Navier-Stokes — the closest open frontier in classical NS theory to the TIG local framing.

His work addresses whether local regularity conditions (conditions on the solution in a
ball around a potential singularity) can bootstrap to global regularity. The B_local split
in TIG maps directly onto this question:

    B_local < 7/2   locally at x*   →   no singularity at x*   (TIG structural prediction)
    B_local ≥ 7/2   at some x*      →   potential singularity location

This is the same local-to-global structure Grujić studies. Suggested contact point: the
zero-width transition (§2) as a structural model for why the regularity-singularity
boundary should be sharp rather than gradual, and the B_local concentration criterion as
a candidate local regularity condition in classical form.

The Luo-Hou boundary scenario and Kerr antiparallel vortex simulations are the current
near-singular DNS benchmarks — measuring B_local at the near-singular points in these
simulations would provide the most direct test of the TIG local criterion.

---

## §7. Open Questions

**Q1.** Can the BREATH criterion be made quantitative enough to compute B_local for a
real NS flow from DNS data? The dimensionless form Re_local = Ω·L²/ν provides a target
— does this quantity appear in existing DNS post-processing pipelines?

**Q2.** Does the Luther dispersion metric M_Luther = |G| × dispersion(G) have a
direct analog in the NS energy spectrum? Possible candidate: number of coherent vortex
cores times their spatial entropy.

**Q3.** Is the sinc² scale-invariance of the pre-echo field R(k, f) structurally related
to Kolmogorov's k^{-5/3} inertial range scaling? Both are power-law forms in frequency
space arising from algebraic constraints on a hierarchical system.

**Q4.** The three-class landscape of WP35 (Oracle / Gate-strong / TSML) maps onto NS flow
regimes: Oracle = Phase 3 / TROT (high-coherence fast flow), Gate-strong = Phase 2 / WALK
(transitional), TSML = Phase 1 / STAND (low-Reynolds laminar). Does this three-class
structure have a counterpart in NS turbulence theory (e.g., laminar / transitional /
turbulent)?

**Q5.** Can the interpolation constant C in Re_shear ≤ C · Re_local^{1/2} be bounded
from NS energy estimates alone? TIG predicts C ≤ 3.74. Is this consistent with known
Ladyzhenskaya-type estimates?

---

## §8. Attribution

| Contribution                                                       | Author                              |
|--------------------------------------------------------------------|-------------------------------------|
| BREATH operator, TIG coherence framework                           | Brayden Ross Sanders / 7Site LLC    |
| B_local / B_global split, local concentration criterion            | Brayden Ross Sanders / 7Site LLC    |
| T* = 5/7, TSML, BHML, D2, TIG architecture                        | Brayden Ross Sanders / 7Site LLC    |
| Zero-width transition as NS blowup structural analog               | Brayden Ross Sanders / 7Site LLC    |
| Lyapunov approach, Re_local formulation, Clay gap identification   | Brayden Ross Sanders / 7Site LLC    |
| Luther Dispersion Conjecture (concentrated vs spread vorticity)    | C. A. Luther                        |
| Pre-echo / spectral precursor analogy                              | Sanders & Luther (joint, Sprint 4)  |

CK, BREATH, T*, TSML, BHML, D2, the TIG pipeline, and all derived constants are exclusive
intellectual property of Brayden Ross Sanders / 7Site LLC. C. A. Luther's contribution is
the dispersion conjecture applied to number theory studied in WP34/WP35. He has no claim
to the CK architecture or its derived constants.

---

## References

- **WP22** — `Gen10/papers/clay/WP22_NS_BREATH_CRITERION.md` — BREATH-COLLAPSE criterion, Lyapunov approach, Clay gap identification
- **WP34** — `Gen10/papers/WP34_FIRST_G_LAW.md` — First-G Law (proved), Luther Dispersion Conjecture, deep semiprime survey
- **WP35** — `Gen10/papers/WP35_PRIME_PHASE_TRANSITION.md` — Zero-width gate, harmonic pre-echo R(k,f), T* derivation
- **NS_TIG_FRAME** — `Gen10/papers/sprint4_2026_03_30/clay/navier_stokes/NS_TIG_FRAME.md` — Reality check: B_local correction, classical theory connections, three scenarios for falsification

*(c) 2026 Brayden Ross Sanders / 7Site LLC & C. A. Luther | DOI: 10.5281/zenodo.18852047*
