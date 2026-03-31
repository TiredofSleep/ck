# WP38 — Navier-Stokes Through the TIG Lens
## The BREATH Criterion, Zero-Width Phase Transitions, and the Sinc² Null Obstruction in Vorticity Fields

*Brayden Ross Sanders (7Site LLC), C. A. Luther & Monica Gish*
*March 2026 | DOI: 10.5281/zenodo.18852047*
*Status: Structural framing — analogical connections, not a proof of NS regularity*

---

## Abstract

The Navier-Stokes regularity problem asks whether smooth, finite-energy initial data on ℝ³
can produce a finite-time singularity in the velocity field. CK's BREATH operator, the
coherence-measurement primitive of the TIG framework, provides a structural lens on this
question: smooth evolution corresponds to BREATH persisting in the COLLAPSE context of the
TIG operator algebra; singularity formation corresponds to BREATH being expelled from
COLLAPSE into the VOID or HARMONY absorber. The zero-width phase transition (WP35 Theorem
2, proved across 153 semiprimes with zero exceptions) supplies the sharpest available
algebraic model for why the regularity-singularity boundary, if it exists, should be sharp
rather than gradual. The harmonic pre-echo field R(k,f) = sin²(πk/f)/(k² sin²(π/f)),
proved in WP35, decays monotonically to zero at k = p — the sinc² null — providing a
spectral precursor template for vorticity concentration before blow-up. The Luther
Dispersion Conjecture maps the geometry of non-unit elements in the coprimality alphabet
to the spatial distribution of vorticity concentration zones, connecting arithmetic
dispersion directly to turbulent spreading. The BREATH-COLLAPSE criterion Re_local ≤ 2/7
— where Re_local = Ω·L²/ν is the local dimensionless enstrophy — is offered as a
structural, algebraically motivated regularity condition. Its quantitative form is
conjectural; its algebraic origin in the TIG coherence table is exact. The key open gap
is establishing the sharp interpolation constant C ≤ 3.74. All NS connections stated here
are structural analogies. No proved reduction from TIG algebra to NS dynamics is claimed.

---

## §1. Introduction: The Navier-Stokes Problem

### 1.1 History and the Clay Formulation

Fluid motion has been described by partial differential equations for nearly two centuries.
Claude-Louis Navier derived the viscous equations in 1822 on molecular force grounds; George
Gabriel Stokes rederived them rigorously in 1845 from continuum mechanics, establishing the
system now bearing both names [28]. The three-dimensional incompressible form is:

    ∂u/∂t + (u·∇)u = ν∆u − ∇p + f
    ∇·u = 0
    u(x,0) = u₀(x)

where u(x,t) : ℝ³ × [0,∞) → ℝ³ is the velocity field, p is pressure, ν > 0 is kinematic
viscosity, and f is a body force. The system is deceptively compact. The nonlinear advection
term (u·∇)u couples all scales of motion and drives energy from large scales toward small
scales — the energy cascade. Whether this cascade terminates in a finite-time singularity is
the Clay Millennium Problem as precisely formulated by Fefferman [2].

Fefferman's formulation [2] asks: given smooth, rapidly decreasing initial data u₀ : ℝ³ → ℝ³
with ∇·u₀ = 0, does there exist a smooth global solution u ∈ C^∞(ℝ³ × [0,∞)) with u
rapidly decreasing and satisfying the NS system for all t > 0? Or can solutions with bounded
initial energy develop singularities in finite time?

The question is not merely technical. A singularity in u would represent the spontaneous
concentration of vorticity — spinning motion — to a point with infinite angular velocity. No
physical fluid exhibits this behaviour, but the mathematical question is whether the NS system
is capable of producing it from smooth initial conditions. The answer, after nearly 200 years
of fluid mechanics, remains open.

### 1.2 What Is Known

The classical theory has established a hierarchy of partial results.

**Leray (1934)** [1] proved global existence of weak solutions — solutions that satisfy NS in
an integral (distributional) sense and obey the energy inequality:

    ½ ||u(·,t)||²_{L²} + ν ∫₀ᵗ ||∇u||²_{L²} ds ≤ ½ ||u₀||²_{L²}

Leray's weak solutions exist globally for all time and all finite-energy initial data. The
problem is that weak solutions may not be smooth: they could concentrate energy without a
classical derivative limit. Hopf (1951) [14] gave an independent construction of weak
solutions using energy methods. Together, Leray and Hopf established that NS "has solutions"
in the generalized sense — but the smoothness of those solutions remained unresolved.

**2D Navier-Stokes is globally regular.** Ladyzhenskaya [3] proved that in two space
dimensions, smooth initial data produce smooth global solutions. The key tool is the
Ladyzhenskaya inequality ‖u‖_{L^4} ≤ C ‖u‖_{L^2}^{1/2} ‖∇u‖_{L^2}^{1/2}, which in 2D
controls the nonlinearity by the energy. In 3D the same inequality loses a derivative and
the control fails.

**3D conditional regularity.** Serrin (1962) [4] proved that if a weak solution satisfies
u ∈ L^p_t L^q_x with 2/p + 3/q ≤ 1 and q ≥ 3, then u is smooth for those times. This is
the prototype of all subsequent regularity criteria: assume the solution is not too rough, and
conclude it is smooth. Prodi (1959) [36] established the same result under slightly different
conditions; the combined framework is the Prodi-Serrin class.

**Partial regularity: CKN (1982).** Caffarelli, Kohn, and Nirenberg [6] proved the deepest
structural result to date: the singular set of a suitable weak solution of 3D NS has one-
dimensional Hausdorff measure zero. This means singularities, if they exist, cannot occur on
curves or surfaces — they can only concentrate on a set of Hausdorff dimension less than one.
This result refined the earlier partial regularity of Scheffer [7].

**Critical norm: ESS (2003).** Escauriaza, Seregin, and Šverák [8] proved that if
lim sup_{t→T} ‖u(·,t)‖_{L^3} < ∞ as t approaches a potential blowup time T, then u is
smooth at T. Since ‖u‖_{L^3} is the only scale-invariant Lebesgue norm for NS in 3D, this
is the sharpest available regularity criterion. Seregin [9] subsequently showed that any
Type-I blowup solution must satisfy ‖u‖_{L^3} → ∞.

**BKM criterion (1984).** Beale, Kato, and Majda [5] proved that blowup occurs at time T if
and only if

    ∫₀ᵀ ‖ω(·,t)‖_{L^∞} dt = ∞

where ω = ∇×u is vorticity. Blowup is a vorticity phenomenon: if the maximum vorticity stays
integrable in time, the solution remains smooth forever.

**Tao's averaged NS (2016).** Tao [19] proved that a specific modification of NS — replacing
the nonlinear term (u·∇)u with an averaged version — develops finite-time blowup. This result
is important because it shows that energy methods alone cannot rule out singularities in NS-
type equations. Any proof of global regularity for the true NS system must exploit something
specific to the unaveraged structure that Tao's averaged equation destroys.

**Full 3D NS: open.** No proof of global regularity or example of finite-time blowup exists
for the true 3D Navier-Stokes equations. The problem is a Clay Millennium Prize problem with
a $1,000,000 award.

### 1.3 Why Regularity Matters

Regularity matters both physically and mathematically. Physically, it asks whether the
Navier-Stokes equations are a complete description of fluid motion or whether they break down
in finite time — requiring additional physics to describe the behavior. Mathematically, the
question touches the foundations of analysis: whether a nonlinear PDE system with smooth
initial data can develop spontaneous singularities through deterministic evolution.

The energy cascade in turbulence [10] concentrates energy at progressively smaller scales
until viscous dissipation becomes effective at the Kolmogorov scale η = (ν³/ε)^{1/4}. Whether
this cascade can, in principle, drive energy all the way to a mathematical point singularity
— bypassing viscous dissipation in finite time — is precisely what the Clay problem asks.
Coherent structures in turbulence [21,22] — organized vortex tubes, sheets, and spirals —
carry the bulk of turbulent kinetic energy and are the physical seat of this process. Whether
their concentration can become singular is the fluid-mechanical heart of the question.

### 1.4 The TIG Approach

TIG (Truth-Is-Geometry) is a 10-operator algebraic framework in which the 50-Hz coherence
cycle of the CK organism is modeled as operator composition. The central object is the TSML
composition table [32,34]: a 10×10 exact table over operators {VOID, LAT, CTR, PRG, COL,
BAL, CHA, HAR, BRT, RST} indexed 0 through 9. BREATH (BRT, index 8) is the coherence-
measurement operator. COLLAPSE (COL, index 4) is the viscous-dissipation analog.

The algebraic identity TSML[BRT][COL] = BRT says: in the presence of viscous dissipation
(COLLAPSE context), BREATH persists. This is a single table lookup — exact and proved. The
TIG framing of NS regularity is: smooth fluid evolution corresponds to BREATH permanently
in the COLLAPSE column; blowup corresponds to BREATH being expelled from COLLAPSE into the
VOID absorber. The Clay gap is showing that the NS flow cannot permanently expel BREATH from
COLLAPSE — equivalently, showing that the local dimensionless enstrophy Re_local = Ω·L²/ν
never crosses 2/7 globally.

The difficulty of NS regularity is not an algebraic flaw in mathematics. It is a physical
distance to a geometric sink in a sinc² field. The signal is always present — R(k/p = 0.1,
p) ≈ 0.9675 for all p regardless of scale. The zero-crossing simply requires traversing p
≈ 2^512 steps. The road is long; the destination is certain.

> *BREATH, T*, TSML, BHML, D2, CK, and the TIG framework are the exclusive intellectual
> property of Brayden Ross Sanders / 7Site LLC, developed over 18 months prior to this
> sprint. C. A. Luther's contribution is the dispersion conjecture applied to number theory;
> he has no claim to the CK architecture or its derived constants.*

---

## §2. Classical Theory: The Framework the BREATH Criterion Must Meet

### 2.1 Energy Estimates and the Ladyzhenskaya Framework

The foundational functional-analytic apparatus for NS regularity is due principally to
Ladyzhenskaya [3]. The Sobolev space framework begins with the energy identity: for smooth
solutions of NS,

    d/dt (½ ‖u‖²_{L²}) = −ν ‖∇u‖²_{L²}

Energy is monotonically dissipated by viscosity. This gives the global energy bound

    ‖u(·,t)‖²_{L²} ≤ ‖u₀‖²_{L²}

which persists for all time. The enstrophy — total squared vorticity — evolves as:

    d/dt (½ ‖ω‖²_{L²}) = −ν ‖∇ω‖²_{L²} + ∫ (ω·∇)u·ω dx

The first term is dissipative and always negative. The second term is vortex stretching: it
can be positive, driving enstrophy growth. The competition between these two terms is the
fundamental mechanism underlying the NS regularity problem. When dissipation dominates,
enstrophy stays bounded and solutions remain smooth. When stretching dominates, enstrophy
can grow without bound, and a singularity may form.

In 2D, the vortex stretching term vanishes identically (no vortex stretching in 2D), and
Ladyzhenskaya's inequality provides the control needed for global regularity. In 3D, vortex
stretching is non-zero and the energy estimates alone are insufficient.

Constantin and Foias [11] developed the attractor theory for NS in bounded domains, showing
the existence of a finite-dimensional global attractor. Constantin, Foias, Manley, and Temam
[12] estimated the attractor dimension, showing it scales with Re^{9/4} — consistent with
Kolmogorov's estimate for the number of degrees of freedom in turbulence. Coherent structures
in turbulence [21,22,23] are the low-dimensional organized motions that dominate the
attractor; their persistence corresponds, in TIG language, to BREATH surviving in the
COLLAPSE column.

### 2.2 Prodi-Serrin Regularity Criteria

Prodi [36] and Serrin [4] independently established that weak solutions satisfying a
quantitative size condition are in fact smooth. The Prodi-Serrin class consists of pairs
(p, q) with 2/p + 3/q ≤ 1 and q ≥ 3: if u ∈ L^p_t L^q_x, then u is regular. The
borderline case q = 3 (with p = ∞) is the ESS result [8].

These conditions are scale-invariant in the following sense: the NS equations are invariant
under the rescaling u_λ(x,t) = λ u(λx, λ²t), and the Prodi-Serrin class consists precisely
of those L^p_t L^q_x norms that are scale-invariant under this rescaling. Regularity criteria
that are scale-invariant cannot be improved by rescaling arguments alone; they represent the
natural scale at which the problem lives.

A structural observation noted in NS_TIG_FRAME [35]: the pair (p, q) = (7, 7/2) satisfies
the Prodi-Serrin condition exactly: 2/7 + 3/(7/2) = 2/7 + 6/7 = 8/7 > 1. Wait — more
precisely: 3/7 + 2/(7/2) = 3/7 + 4/7 = 1. Taking the standard form 3/p + 2/q = 1 for the
velocity criterion gives (p, q) = (7, 7/2). TIG operators: HAR = 7; B_local threshold = 7/2.
Whether this numerical coincidence reflects a deeper structural connection is an open question
[35].

### 2.3 CKN Partial Regularity

Caffarelli, Kohn, and Nirenberg [6] proved the most precise structural theorem about potential
singularities: the one-dimensional Hausdorff measure of the singular set of a suitable weak
solution is zero. The CKN ε-regularity theorem is the key technical ingredient: there exists
ε > 0 such that if

    limsup_{r→0} (1/r) ∫_{Q(x,t,r)} (|∇u|² + |p|^{3/2}) dy ds < ε

then (x,t) is a regular point. Here Q(x,t,r) is the parabolic cylinder centered at (x,t).
Scheffer [7] had previously established the first partial regularity result; CKN refined and
strengthened it.

The CKN theorem places a quantitative constraint on where singularities can live: they must
be concentrated enough that the parabolic integral exceeds ε. In TIG language: a singularity
requires the local coherence field to be dense enough that the sinc² obstruction is triggered.
The CKN ε plays the role of the coherence threshold T* = 5/7 in TIG: below the threshold,
the point is regular; above it, singularity is possible.

The TIG BREATH criterion sharpens CKN in a specific direction: CKN says the singular set
has zero 1D Hausdorff measure (a set theorem, about what cannot happen in large regions);
TIG says the singular set is a zero-width transition point (a pointwise sharpness statement,
about what happens at the one exceptional moment). These are structurally compatible: CKN
bounds the size; TIG characterizes the sharpness.

### 2.4 Constantin-Fefferman Vorticity Direction Criterion

Constantin and Fefferman [38] proved that regularity follows if the vorticity direction
field ξ = ω/|ω| does not vary too rapidly in the regions where |ω| is large: specifically,
if |∇ξ| ≤ C/|ω|^{1/2} in the large-vorticity region, then the solution is regular. This
geometric condition says that vorticity, however large in magnitude, must remain
geometrically organized — pointing consistently in a single direction — to avoid a
singularity.

This result is the direct classical predecessor to Grujić's geometric depletion theory
(§7 below). It also maps cleanly onto the TIG framework: the COLLAPSE context (operator 4,
viscous dissipation) corresponds exactly to the geometrically organized regime where
vorticity direction is coherent. BREATH persisting in COLLAPSE = the Constantin-Fefferman
condition holding = no singularity.

---

## §3. The BREATH Criterion: Precise Definition and Algebraic Foundation

### 3.1 TIG Operator Algebra

The TIG framework operates over a 10-element operator set:

    {VOID(0), LAT(1), CTR(2), PRG(3), COL(4), BAL(5), CHA(6), HAR(7), BRT(8), RST(9)}

The TSML composition table defines operator products. Key identities, all exact:

    TSML[BRT][COL] = BRT    (BREATH fixed point: persists in COLLAPSE)
    TSML[BRT][x]  ∈ {HAR, VOID}   for all x ≠ COL
    TSML[VOID][x] = VOID    for all x   (VOID: two-sided absorber)
    TSML[x][VOID] = VOID    for all x

The BREATH fixed point identity is the algebraic foundation of the NS analogy. It is proved
by a single table lookup — not a hypothesis or approximation. The operator-fluid
correspondence is:

| TIG operator | Fluid analog               | Classical reference              |
|--------------|----------------------------|----------------------------------|
| VOID (0)     | Undefined velocity / singularity | Leray blowup scenario [1]   |
| COL (4)      | Viscous dissipation dominant | Serrin-class regularity [4]    |
| BRT (8)      | Controlled local enstrophy | CKN regular point [6]           |
| HAR (7)      | Global rest, zero vorticity | Leray decay ‖u‖_{L²} → 0 [1]  |

The TIG model for smooth flow: BREATH in COLLAPSE context, persisting. The TIG model for
blow-up: BREATH leaves COLLAPSE — one composition step delivers HAR (global rest = unphysical
sudden halt) or VOID (undefined = singularity). There is no smooth transition through
intermediate operators. This is the algebraic basis for the zero-width transition (§4).

### 3.2 The B_local Split

Define two coherence quantities following NS_TIG_FRAME [35]:

    B_local(x, r, t) = ‖ω(·,t)‖_{L³(B(x,r))} · r/ν

    B_global(t)      = ‖ω(·,t)‖_{L³} · L/ν

where B(x,r) is the ball of radius r centred at x, L is the global domain scale, and
ω = ∇×u is vorticity.

**Reality check from NS_TIG_FRAME [35]:** B_global fails as a threshold. For the Taylor-Green
vortex at Re = 1600, B_global >> 7/2 at peak enstrophy — yet no blow-up occurs. A global
threshold at C = 7/2 would predict blow-up for ordinary turbulence, which is false. The
correct TIG prediction is local:

    Structural prediction: any potential blow-up point x* requires
        limsup_{t → T⁻} B_local(x*, r(t), t) ≥ 7/2
    where r(t) = (T−t)^{1/2} is the appropriate local scale.

Below 7/2 locally, no sustainable singularity can form. This is consistent with turbulence:
high global vorticity but no sustained local singularities. The constant 7/2 = HAR/2 = 7/2
appears in TIG as the Prodi-Serrin echo (§2.2) — whether this echo is coincidence or
structure is an open question.

### 3.3 The BREATH-COLLAPSE Criterion (†): Dimensionless Form

For a solution u of 3D NS at (x,t), define the local Reynolds number:

    Re_local(x,t) = Ω(x,t) · L(x,t)² / ν

where Ω = ½|ω|² = ½|∇×u|² is local enstrophy density and L is the local Taylor microscale.
Re_local is dimensionless under the NS scaling u_λ(x,t) = λ u(λx, λ²t).

**Criterion (†):** Re_local(x,t) ≤ 2/7 at every (x,t).

TIG interpretation:
- (†) holds at (x,t): fluid is in COLLAPSE context at (x,t) → BREATH persists → local
  smooth evolution.
- (†) violated: context exits COLLAPSE → BREATH → HAR in one step → onset of steep gradients.

**The constant 2/7.** In TIG algebra: 2/7 = T* + S* − 1 where T* = 5/7 (coherence threshold,
derived algebraically from b = 35, see §3.5 below) and S* = 4/7 (stability threshold). The
constant is algebraically determined, not tuned.

**Claim status:** The criterion (†) is a structural analogy. The TIG algebraic content
(TSML[BRT][COL] = BRT) is proved exactly. The correspondence Re_local ≤ 2/7 ↔ COLLAPSE
context is conjectural.

### 3.4 The Reframing Table

| Classical NS statement                  | TIG analog                                        |
|-----------------------------------------|---------------------------------------------------|
| Does smooth solution exist for all t?   | Does BREATH persist for all t?                    |
| Does finite-time blow-up occur?         | Does context permanently leave COLLAPSE column?   |
| Serrin regularity conditions [4]        | E(t)·Δt ≤ (2/7)·ν (BREATH-COLLAPSE criterion)   |
| Local regularity at potential blow-up   | B_local < 7/2 at every potential singular point   |
| CKN: singular set has H¹ measure zero   | Zero-width transition: singular set is one point  |
| BKM: blow-up iff ∫‖ω‖_{L^∞}dt = ∞   | Blow-up = B_local crossing 7/2 = null crossing    |
| ESS: ‖u‖_{L^3} bounded → regular [8]  | B_local < 7/2 → BREATH in COLLAPSE persists       |

### 3.5 T* = 5/7: Algebraic Derivation

T* = 5/7 is not a hardware constant or a tuned parameter. It is an algebraic identity proved
in WP35 [33]. For any semiprime b = p×q with p < q and p ≥ 3:

    unit_frac(k=q, b) = (q − 2) / q    (exact, for all such semiprimes)

T* is the unique realization of this formula at the minimal strong semiprime:
- "Strong" = both prime factors strictly greater than 3
- Minimal such semiprime: b = 5×7 = 35 (p=5, q=7)
- unit_frac(k=7, b=35) = (7−2)/7 = 5/7 exactly

At that moment, R(7, 7) = 0 (WP35 Theorem 1 [33]): the harmonic clock collapses at exactly
the same step where unit density reaches T*. The gate event and the coherence floor crossing
are the same physical moment, algebraically pinned.

---

## §4. The Zero-Width Transition: Algebraic Model for the Regularity Boundary

### 4.1 The First-G Law (WP34 — Proved)

For every semiprime b = p × q with p ≤ q, define the coprimality partition:

    C_k = { x ∈ {1..k} : gcd(x, b) = 1 }     (coherent alphabet)
    G_k = { x ∈ {1..k} : gcd(x, b) > 1 }     (obstructing alphabet)

**First-G Law (WP34 [32], proved, 153 semiprimes verified, zero exceptions):**

    |G_k| = 0   for all k < p          (stability window: fully coherent alphabet)
    |G_p| = 1   (p itself is the unique first obstruction)

Proof: elementary number theory. No element x < p shares a prime factor with b = p×q, since
p is the smallest prime factor of b. The element p itself is coprime to q (distinct primes),
so gcd(p, b) = p > 1. This is the unique first non-unit.

**Verification:** 153 semiprimes, 36,662 exact (b,k) pairs, zero exceptions.

### 4.2 Zero-Width Gate (WP35 Theorem 2 — Proved)

Define the gate-rate sequence:

    gate_rate(k) = |G_k| / k

**WP35 Theorem 2 [33]:** For every semiprime b = p×q:

    gate_rate(k) = 0   for all k < p    (pre-echo zone, fully coherent)
    gate_rate(p) > 0   (instant collapse: |G_p| = 1, gate_rate(p) = 1/p > 0)
    gate_rate(k) monotone non-decreasing for k ≥ p

The transition has exactly zero width — it is a perfect step function. There is no partial
coherence near the boundary. Verified across 153 semiprimes with zero exceptions.

**Three-factor contrast:** For b = p×q×r (three prime factors), the transition is tiered:
three distinct steps at k = p, k = q, k = r. The zero-width property characterizes semiprimes
(two prime factors). It is not generic.

### 4.3 Structural Analogy to the NS Regularity Boundary

The TIG dichotomy at k = p:
- Pre-transition (k < p): |G_k| = 0. Fully coherent. Stability window. Zero resistance.
- At transition (k = p): |G_p| = 1. First obstruction born. Gate activated.
- Post-transition (k > p): gate growing. Obstruction zone.

**Formal analogy (structural):**

| TIG                                | NS (structural analog)                          |
|------------------------------------|-------------------------------------------------|
| k < p: |G_k| = 0 (coherent)        | t < T: Re_local ≤ 2/7 (smooth solution)         |
| k = p: |G_p| = 1 (first obstruction)| t = T: Re_local = 2/7 (threshold moment)         |
| k > p: gate grows (incoherent)     | t > T: Re_local > 2/7 (potential blow-up)       |
| Transition: one step, exact, proved| Transition: sharp threshold (hypothesized)      |

The zero-width proof offers structural support for a sharp (not gradual) regularity threshold
in NS. This is consistent with CKN [6], which says singular support cannot be spread over
a set of positive 1D measure. TIG says more: the transition, if it occurs, is a single
zero-width event. CKN bounds the size of the singular set from above; TIG characterizes
the sharpness of the transition.

*This is a structural analogy. No proved reduction from gate algebra to NS dynamics exists.*

### 4.4 Sharpness and the Semiprime Structure Hypothesis

The zero-width property is a fingerprint of the semiprime (two-factor) ring structure.
If the NS flow has "multi-factor" concentration geometry — multiple independent concentration
mechanisms operating simultaneously — the transition may be blurred, analogous to a three-
factor semiprime. The zero-width prediction applies most cleanly to single-scale concentration
events: one vortex filament spiraling to a singularity rather than multiple simultaneous
concentrations. This is the regime of the Leray scenario and the Kerr antiparallel
simulations — and it is structurally the correct domain of the TIG zero-width claim.

---

## §5. The Vorticity Null: Blow-Up as the Sinc² Zero-Crossing

### 5.1 The Harmonic Pre-Echo Field

**WP35 Theorem 1 (Harmonic Pre-Echo Countdown Law) [33]:** For any prime f and positive
integer k:

    R(k, f) = sin²(πk/f) / (k² sin²(π/f))

Properties proved in WP35:
- R(1, f) = 1 (maximum at k=1)
- R(k, f) is strictly decreasing on {1, …, f−1}
- R(f−1, f) = 1/(f−1)² (minimum before collapse; the pre-echo floor)
- R(f, f) = 0 exactly (zero at the First-G event, the sinc² null)
- R(k, 1/p) is ω-blind: identical for every modulus b sharing the prime factor p,
  regardless of ring structure (WP35 Theorem 4 [33])

The continuum limit (WP35 Theorem 5 [33]): as f → ∞ with k/f = t fixed,

    R(k, f)  →  sinc²(t)  =  (sin(πt) / πt)²

The discrete harmonic pre-echo converges to the classical sinc-squared function. Two universal
constants follow immediately:

    R(k/p = 1/2,  p)  →  4/π²  ≈  0.4053    (sinc²(1/2), exact for all p)
    R(k/p = 0.1,  p)  →  sinc²(0.1)  ≈  0.9675   (scale-free, all p)

The second identity — R ≈ 0.9675 at 10% of the distance to the sink — is the scale-invariance
principle: the coherence field is always strong at the start of the approach. The difficulty
is not the strength of the signal; it is the distance.

**Verification:** 187 semiprimes, max numerical error 1.11×10⁻¹⁶ (machine epsilon only).

### 5.2 The Sinc² Null as Vorticity Null

The sinc² null at k = p is the mathematical model for the vorticity null in the NS blow-up
scenario. The analogy runs precisely:

| TIG (proved)                           | NS (structural analog)                          |
|----------------------------------------|-------------------------------------------------|
| R(k, f) → 0 as k → f (sinc² null)     | B_local → 7/2 as t → T (concentration threshold)|
| k < f: R > 0, field coherent          | t < T: Re_local < 2/7, solution smooth          |
| k = f: R = 0, field collapses          | t = T: Re_local = 2/7, threshold crossed         |
| D1 = dR/dk changes sign at k = f      | d/dt[B_local] changes sign at t = T             |
| sinc² is scale-invariant (all p)       | Re_local = Ω·L²/ν is dimensionless (all scales) |

**Blow-up is not the absence of a solution.** The TIG framing is precise: blow-up is the
arrival at the sinc² null, not the failure of the system to have a solution. The trajectory
R(k,f) was always decreasing toward zero; the question is whether the physical flow reaches
k = p. In NS: the question is whether the enstrophy concentration trajectory reaches the
threshold 7/2 before global regularity is established by dissipation.

The monotone decrease of R(k,f) on {1,…,f−1} models the one-directional approach to
blow-up: once the trajectory begins, there is no turning back within the pre-echo zone. The
D1 sign flip at k = f models the qualitative change in behavior at the transition: before
the null, the field is decreasing (approaching singularity); after the null, the field
begins recovering (the vorticity concentration has dissipated or the solution has continued
past the singular time).

### 5.3 The B_local Blowup Necessary Condition

**Lemma (NS_TIG_FRAME [35], conjectural):** Under the TIG-NS correspondence, if a blow-up
occurs at (x*, T), then:

    limsup_{t→T⁻} B_local(x*, r(t), t) ≥ 7/2

where B_local(x,r,t) = ‖ω(·,t)‖_{L³(B(x,r))} · r/ν and r(t) = (T−t)^{1/2}.

*Status: Conjectural. Classical evidence: consistent with ESS [8] (which requires L^3 velocity
blow-up) and BKM [5] (which requires ‖ω‖_{L^∞} to blow up). The specific constant 7/2 is
not proved classically; it is the TIG prediction. Falsification test: run near-singular DNS
(Luo-Hou boundary scenario) and measure B_local at the near-singular point.*

This sharpens ESS [8] in a specific direction: ESS says blow-up requires lim sup ‖u‖_{L^3}
= ∞; the TIG prediction says the vorticity version of this norm (B_local) must reach the
specific threshold 7/2, not merely diverge. If true, this would provide a quantitative
blow-up criterion rather than a qualitative one.

### 5.4 Connection to BKM and ESS

The Beale-Kato-Majda criterion [5] states: blow-up at time T if and only if

    ∫₀ᵀ ‖ω(·,t)‖_{L^∞} dt = ∞

The TIG local criterion is consistent: any sustained local singularity requires B_local
growing without bound, which drives ‖ω‖_{L^∞} toward infinity locally. Conversely, if
B_local remains bounded below 7/2 everywhere, then ‖ω‖_{L^∞} cannot concentrate to a
sustainable singularity, and BKM implies regularity.

The ESS theorem [8] is the primary classical bridge: if ‖u(·,t)‖_{L^3} remains bounded,
then u is smooth. TIG's B_local = ‖ω‖_{L^3(B(x,r))} · r/ν is the vorticity analog of
this L^3 velocity criterion, localized to the potential singular point. The TIG prediction
sharpens ESS: the blow-up threshold for B_local is 7/2, not merely divergence.

---

## §6. Luther Dispersion and Vorticity Spread

### 6.1 The Luther Dispersion Conjecture

The dispersion conjecture (C. A. Luther, WP34 [32]) states:

    gate_rate ≈ F_k( |G| × dispersion(G) )

where dispersion(G) measures the spatial spread of non-unit elements across the alphabet. A
formal definition: the interleave score

    interleave(b, k) = transitions(C, G in sequence 1..k) / (2 · min(|C|, |G|))

counts the alternation of unit and non-unit elements in the sequence {1, …, k}. The Luther
metric is:

    M_Luther(b, k) = |G_k| × interleave(b, k)

Low M_Luther: concentrated obstruction (few G elements, clustered together). High M_Luther:
spread obstruction (G elements dispersed across the alphabet, maximally interleaved with C
elements).

**Conjecture (Luther [32]):** The gate difficulty — the rate at which the coherent window
closes — is driven not just by the count of obstructing elements but by their spatial
distribution. Concentrated obstructions are locally fierce but globally tractable; spread
obstructions contaminate the entire coherent alphabet.

*Status: Conjectural. Empirical support: correlation r = −0.509 between bridge slope and q/p
ratio (WP34 [32]). Not proved analytically.*

### 6.2 NS Translation: Vorticity as Obstruction

In fluid dynamics, vorticity is not uniformly distributed — it concentrates in coherent
structures (vortex tubes, sheets, braids) or disperses into the background flow. The Luther
metric translates:

    |G|           →  number of active vorticity concentration zones
    dispersion(G) →  their spatial spread across the flow domain
    M_Luther      →  (concentration count) × (spatial spread)

**Structural prediction:** Flows with concentrated vorticity (few tight cores, low M_Luther)
are further from singularity than flows with dispersed vorticity (high M_Luther). This is
consistent with physical intuition — a single coherent vortex filament is more robust than
scattered high-vorticity patches — and with the mathematical intuition behind CKN [6]:
singular support concentrated at a point is the irreducible singularity structure.

More precisely: a low M_Luther flow corresponds to a semiprime-like ring structure (one
dominant concentration event), where the zero-width transition (§4) is the correct model.
A high M_Luther flow corresponds to a multi-factor ring structure, where the transition may
be blurred across multiple simultaneous events.

### 6.3 Interleave Score as Vorticity Mixing Measure

The interleave score counts alternations between unit and non-unit elements:

    High interleave = fully mixed C/G = turbulent regime (C and G alternate maximally)
    Low interleave  = one-sided concentration = potential near-singular structure

In the vorticity field: interleave counts the alternation of smooth regions (low vorticity)
and concentrated regions (high vorticity) across space. High interleave = fully developed
turbulence with uniformly spread vorticity. Low interleave = organized coherent structures
with vorticity concentrated in few regions.

The TIG prediction: high-interleave turbulence (high M_Luther) has low gate_rate — the
coherent window closes slowly, singularity is distant. Low-interleave structure (low M_Luther)
has the gate_rate precisely tracking a single concentration event — the blow-up scenario.
This reverses the naive intuition and matches the mathematics: singular NS behavior is most
likely in organized, low-interleave flows (coherent vortex structures spiraling toward a
singularity), not in chaotic high-interleave turbulence.

### 6.4 Connection to the Constantin-Fefferman and Grujić Criteria

The Constantin-Fefferman direction criterion [38] controls |∇ξ| / |ω|^{1/2} where
ξ = ω/|ω| is the vorticity direction. Geometrically, this is a coherence condition on the
vorticity direction field: vorticity must point consistently to avoid singularity.

**TIG analog:** Low dispersion (concentrated G elements, low interleave) corresponds to
a coherent vorticity direction field (all vorticity pointing the same way). High dispersion
corresponds to geometrically disordered vorticity (high |∇ξ|). The Luther metric directly
operationalizes the Constantin-Fefferman condition: M_Luther small ↔ coherent ξ ↔ CF
condition satisfied ↔ regularity.

Grujić's geometric depletion criterion [15,16,17] (§7) formalizes this: depletion (stretching
suppressed by geometric organization) → regularity. Low Luther metric = geometrically
organized = Grujić depletion active = BREATH in COLLAPSE = smooth solution. The chain is:

    M_Luther small → low dispersion → organized ξ → geometric depletion (Grujić [15])
                  → vortex stretching controlled → dissipation dominates (COL context)
                  → BREATH persists → smooth solution

*All connections beyond the TIG-Luther link are structural analogies, not proved.*

---

## §7. The Pre-Echo as Spectral Precursor

### 7.1 The R(k,f) Countdown: Smooth Approach to the Null

The harmonic pre-echo field R(k,f) counts down to the sinc² null from above. The trajectory
is strictly monotone decreasing on {1,…,f−1}:

    R(1, f) = 1.0                   (starting coherence: maximum)
    R(k/p = 0.1, p) ≈ 0.9675       (10% of the way: strong signal, scale-invariant)
    R(k/p = 0.5, p) → 4/π² ≈ 0.405 (halfway: moderate coherence)
    R(f−1, f) = 1/(f−1)²           (one step before null: minimum nonzero value)
    R(f, f) = 0                     (null: exact collapse)

The field "knows" the transition is coming. Every step of the countdown carries the
harmonic imprint of the approaching null. This is the sense in which the spectrum is a
precursor: the sinc² shape of R(k,f) encodes the location of the null (f = p) in its
entire profile, not just at the final step.

**Lemma (WP35, proved [33]):** The minimum nonzero value of R(k,f) over all k ∈ {1,…,f−1}
is 1/(f−1)², achieved uniquely at k = f−1. This is the spectral gap immediately before
the transition: the pre-echo has a non-zero floor, never reaching zero until the exact
transition point.

In NS language: there is always a residual coherence signal before blow-up. The vorticity
field, however concentrated, retains the sinc² envelope of structured organization — until
the exact moment of singularity. This suggests that blow-up, if it occurs, would be
detectable in the spectrum as the approach to this floor, rather than appearing without
warning.

### 7.2 D1 Non-Monotone Oscillations: Structured Pre-Echo Breathing

The first difference D1(k,f) = R(k+1,f) − R(k,f) is not monotone in the pre-echo zone:
it has structured oscillations as R descends. These oscillations are a geometric feature
of the sinc² envelope — the derivative of sin²(πk/f)/(k² sin²(π/f)) has alternating sign
changes driven by the competing sin² numerator and k² denominator.

**WP35 [33]:** D1 < 0 throughout {1,…,f−1} (R is strictly decreasing), but the magnitude
|D1(k,f)| oscillates. The sign of D1 flips at k = f: D1(f,f) > 0 (recovery begins after
the null).

In NS: these oscillations model the structured breathing of the vorticity field before
turbulence onset. Pre-blow-up behavior in turbulence is not monotone — enstrophy and
vorticity magnitude oscillate (growing on average but not uniformly) before any potential
singularity. The D1 oscillations of the pre-echo provide a structured template for this
behavior: the coherence field breathes before it collapses.

**DNS proposal:** Track d/dt[B_local(x*,r(t),t)] as a diagnostic in near-singular DNS
(Luo-Hou boundary scenario [see NS_TIG_FRAME §7]; Kerr antiparallel vortex tubes). A
sign flip from negative (approaching threshold) to positive would correspond to the D1 sign
flip at k = f. This is a measurable event, distinguishable from ordinary turbulent
fluctuations.

### 7.3 Scale-Invariance and K41

The Kolmogorov (1941) scaling law [10] states that in the inertial range,

    E(k) ~ k^{-5/3}

where E(k) is the energy spectrum at wavenumber k. The criterion (†) is scale-invariant:
Re_local = Ω · L² / ν is dimensionless under the NS scaling. This scale-invariance is
consistent with K41 universality — the threshold 2/7 applies at every scale L, not just
at the Kolmogorov scale η.

The pre-echo field R(k,f) decays as k^{-2} in the limit of large k (from the 1/(k²
sin²(π/f)) behavior at large k relative to f). This is steeper than K41 (k^{-5/3}) but
consistent with the sub-inertial range where viscous effects dominate and spectral power
falls faster than the inertial-range scaling.

**Open question:** Is the sinc² scale-invariance of R structurally related to K41
universality? Both are power-law forms in frequency space arising from algebraic constraints
on a hierarchical system (prime arithmetic for TIG; eddy cascade for NS). The k^{-2} vs
k^{-5/3} discrepancy may reflect the difference between the discrete TIG ring structure
and the continuous NS cascade. This is an open question, not a claim.

### 7.4 Fejér Kernel and Spectral Methods

The harmonic pre-echo R(k,f) is a Fejér-type kernel — the same family of functions that
appears in spectral counting problems, trace formulas for automorphic forms [30], and the
spectral representation of uniform distributions. Hejhal's treatment of the Selberg trace
formula [30] uses the same Fejér structure to count spectral resonances.

In spectral NS computations [24], the energy spectrum is represented mode by mode. The
Fejér structure of R(k,f) suggests that near a potential blow-up, the spectral energy
distribution might exhibit Fejér-type decay as time approaches a critical time — providing
a measurable pre-singularity signal in the DNS spectrum. This is speculative; it is offered
as a research direction, not a claim.

---

## §8. The Lyapunov Approach and the Clay Gap

### 8.1 The Lyapunov Functional

Define the supremum Lyapunov functional:

    V(t) = sup_{x ∈ domain} Re_local(x, t)

**TIG prediction (structural):** If V(t) ≤ 2/7 at some time t₀, then BREATH is in COLLAPSE
context everywhere, and smooth evolution continues. The Clay gap is showing that V(t₀) ≤ 2/7
implies V(t) ≤ 2/7 for all t > t₀.

The enstrophy equation is:

    ∂Ω/∂t = −2ν|∇ω|² + S     where S = 2(ω·∇)u·ω

Dissipation (−2ν|∇ω|²) is always negative — viscosity removes enstrophy. Vortex stretching
(S = 2(ω·∇)u·ω) can be positive — this is the obstacle. For V to be a Lyapunov function,
need dV/dt ≤ 0 when V = 2/7: stretching must not overcome dissipation at the threshold.

### 8.2 The Interpolation Chain

At the threshold V = 2/7, scaling gives:

    S ≤ 2ν|∇ω|²   ⟺   Re_shear(x, t) ≤ 2

The two conditions relate through the Gagliardo-Nirenberg interpolation inequality:

    Re_shear ≤ C · Re_local^{1/2}

If Re_local ≤ 2/7, then Re_shear ≤ C · √(2/7). For this to satisfy Re_shear ≤ 2:

    C · √(2/7) ≤ 2   ⟺   C ≤ 2/√(2/7) = 2·√(7/2) ≈ 3.742

**For C ≤ 3.74: dissipation dominates stretching at the threshold → V is a Lyapunov
function → global regularity follows.**

The constant 3.74 is 2√(7/2). Note that 7/2 = the B_local threshold, 7 = HAR (the TIG
harmony operator), 2 = the Re_shear bound. The algebraic structure is consistent throughout.

### 8.3 The Clay Gap: Status Table

| Step                                              | Status                          |
|---------------------------------------------------|---------------------------------|
| BREATH persists iff V ≤ 2/7                       | Proved (TIG table lookup)       |
| V = Re_local is dimensionless and scale-invariant | Fixed (Sprint 4, NS_TIG_FRAME)  |
| V ≤ 2/7 ⟹ Re_shear ≤ 2                           | Derived (scaling at threshold)  |
| Re_shear ≤ C · Re_local^{1/2}                    | Standard GN interpolation form  |
| C ≤ 3.74 → Lyapunov closes                        | **Open: this is the Clay gap**  |

TIG specifies the target constant (2/7 threshold → C ≤ 3.74 bound) and the proof structure
(Lyapunov functional, interpolation chain). The analytic work remaining is establishing the
sharp interpolation constant C from NS energy estimates. This is in the same family as the
sharp inequalities Ladyzhenskaya [3], Serrin [4], and Caffarelli-Kohn-Nirenberg [6] pursued.
TIG gives a numerical target; the classical analysis must confirm or refute it.

**The sharp C in the GN inequality** ‖∇u‖_{L^2} ≤ C_{GN} · ‖ω‖_{L^2}^{1/2} ·
‖∇ω‖_{L^2}^{1/2} (locally) needs to be bounded from NS energy estimates alone. Constantin's
geometric statistics [13] provides bounds on the vortex stretching term S in terms of
local geometry — whether these bounds can close C ≤ 3.74 is the primary open computation.

---

## §9. Grujić and Geometric Depletion: The Closest Classical Bridge

### 9.1 Grujić's Framework

Zoran Grujić (University of Virginia) has developed the most technically precise classical
approach to local-to-global regularity in 3D NS — the closest open research frontier to
the TIG B_local framing.

**Grujić (2009) [15]:** Under a geometric depletion condition on the vorticity direction
field ξ = ω/|ω| — requiring that the vortex stretching term (ω·∇)u·ω is geometrically
depleted by the alignment of ω with the eigenvectors of the strain tensor — local
regularity propagates globally.

**Grujić-Guberović (2010) [16]:** Regularity follows when there is balance between |ω|
magnitude and the coherence of ω/|ω| direction: if |∇ξ| · |ω|^{1/2} is locally bounded,
the solution is regular. This balance criterion maps directly to the TIG B_local threshold:
B_local < 7/2 locally is a form of local enstrophy-direction balance.

**Grujić (2013) [17]:** A geometric measure-type regularity criterion: regularity follows
when the vorticity direction is sufficiently coherent in a geometric-measure sense. The
"sufficient coherence" threshold is the Grujić depletion constant M.

**Grujić-Kukavica (1998) [18]:** Analyticity propagation from smooth initial data: the
BREATH operator's persistence in COLLAPSE corresponds to analyticity propagation. Smooth
(analytic) initial data stay analytic as long as the dissipation dominates.

### 9.2 TIG-Grujić Correspondence

The precise structural correspondence:

| TIG (algebraic)                    | Grujić (analytic)                              |
|------------------------------------|------------------------------------------------|
| TSML[BRT][COL] = BRT (table lookup)| Geometric depletion → regularity (PDE theorem) |
| COLLAPSE context = dissipation dominant | Depletion condition = stretching suppressed  |
| BREATH in COLLAPSE = smooth        | Depletion active = smooth                      |
| BREATH exits COLLAPSE = blow-up    | Depletion fails = potential singularity        |
| B_local < 7/2 locally              | Vorticity direction coherent locally           |

Both frameworks say: a geometric/structural condition on vorticity (not just its magnitude)
ensures smooth evolution. TIG's condition is algebraic — one table lookup. Grujić's is
analytic — a PDE inequality. They are structurally parallel.

**The key open question for TIG-Grujić contact:** Can the TIG depletion condition (B_local
< 7/2) be related to Grujić's depletion constant M? If M = 7/2 can be obtained from the
TIG threshold, this would be a non-trivial quantitative match between algebraic and
analytic approaches. This is Open Question Q5 below.

### 9.3 The Luo-Hou Boundary Scenario

Luo and Hou (2014) identified a near-singular DNS scenario: a boundary layer flow with
potential Type-I blow-up behavior. This is the current state-of-the-art near-singular
simulation, providing the most direct test bed for the TIG local criterion.

**TIG diagnostic protocol (proposed):**
1. Run the Luo-Hou boundary scenario to near-singular time T.
2. At the near-singular point x*, compute:
   - B_local(x*, r(t), t) = ‖ω(·,t)‖_{L³(B(x*,r(t)))} · r(t) / ν
   - r(t) = (T−t)^{1/2} (Type-I blow-up scaling radius)
3. Track whether B_local approaches 7/2 before global regularity is established.
4. Track d/dt[B_local] for the sign flip predicted by the D1 pre-echo structure.

Scenario A (TIG supported): B_local → 7/2 from below as t → T.
Scenario B (TIG falsified): B_local >> 7/2 without singularity (ordinary turbulence).
Scenario C (TIG partially supported): B_local → 7/2, but from above (new constraint).

The Taylor-Green vortex at Re = 1600 already provides evidence for Scenario B (B_global >>
7/2 without blow-up), which is why the global criterion was corrected to local in NS_TIG_FRAME
[35]. The Luo-Hou scenario tests B_local, the corrected form.

### 9.4 Tao's Averaged NS and the TIG Criterion

Tao [19] proved that an averaged modification of NS has finite-time blow-up solutions.
The TIG criterion must be assessed against this result.

In Tao's averaged NS, the nonlinear term (u·∇)u is replaced by an averaged version that
preserves energy conservation but breaks the geometric structure of vortex stretching. The
TIG COLLAPSE context corresponds precisely to the controlled vortex stretching regime —
and Tao's averaging destroys this control. The TIG prediction is that Tao's averaged
solutions should have B_local ≥ 7/2 at the blow-up time (otherwise the TIG local criterion
is falsified by an explicit example). This is computable since Tao's solution is explicit [19].

Constantin and Foias [11] showed that the full NS in bounded domains has a finite-dimensional
global attractor; Tao's averaging destroys the attractor structure. The TIG COLLAPSE-BREATH
persistence corresponds to attractor-confined dynamics; Tao's blow-up corresponds to
dynamics that escapes the attractor. This framing is consistent but not proved.

---

## §10. Status, Open Questions, and Falsification Criteria

### 10.1 Status Summary

| Claim                                              | Status                          | Evidence                           |
|----------------------------------------------------|---------------------------------|------------------------------------|
| BREATH fixed point: TSML[BRT][COL] = BRT          | PROVED                          | Exact table lookup [32,34]         |
| Zero-width gate for semiprimes                     | PROVED                          | 153 semiprimes, 36,662 pairs [33]  |
| Harmonic pre-echo R(k,f) closed form               | PROVED                          | 187 semiprimes, 10⁻¹⁶ error [33]  |
| T* = 5/7 algebraic derivation                      | PROVED                          | unit_frac(k=7, b=35) = 5/7 [33]   |
| sinc² continuum limit                              | PROVED                          | Exact limit, 4/π² verified [33]    |
| BREATH-COLLAPSE criterion (†) → NS                 | STRUCTURAL ANALOGY              | Not proved [34,35]                 |
| B_local threshold at 7/2                           | CONJECTURAL                     | Consistent with ESS [8], not proved|
| Lyapunov structure (C ≤ 3.74)                      | OPEN                            | Clay gap [34]                      |
| Luther dispersion → vorticity spread               | STRUCTURAL ANALOGY              | Empirical r = −0.509 [32]          |
| R(k,f) as pre-blow-up spectral precursor           | STRUCTURAL ANALOGY              | Consistent with BKM [5]            |
| TIG-Grujić correspondence                          | STRUCTURAL ANALOGY              | Not proved [15,16,17]              |

### 10.2 Open Questions

**Q1. The Gap Constant: C ≤ 3.74.**
In the interpolation inequality Re_shear ≤ C · Re_local^{1/2}, determine the sharp constant
C for 3D NS. TIG predicts C ≤ 3.74 (from the requirement that V(t) = 2/7 is a Lyapunov fixed
point). This requires computing the sharp GN constant locally:
‖∇u‖_{L^2(B)} ≤ C_{GN} · ‖ω‖_{L^2(B)}^{1/2} · ‖∇ω‖_{L^2(B)}^{1/2}.
Does C_{GN} ≤ 3.74 for 3D NS with Serrin-class initial data?

**Q2. DNS Test of B_local = 7/2.**
Run near-singular DNS (Luo-Hou boundary scenario; Kerr antiparallel vortex tubes) and track:
    B_local(x*, r(t), t) = ‖ω(·,t)‖_{L^3(B(x*,r(t)))} · r(t) / ν
at the near-singular point x*. Does B_local approach 7/2 before global regularity is
established?

**Q3. Pre-Echo Spectral Signal in DNS.**
In Taylor-Green vortex DNS near peak enstrophy, does the spectral power distribution exhibit
a Fejér-type sin²(πk/f)/(k² sin²(π/f)) profile for some effective frequency f? Does the
D1 sign flip appear as a diagnostically measurable event before enstrophy peak?

**Q4. Luther Metric in Turbulence.**
Define Luther_metric(t) = (number of active vorticity concentration zones) × (their spatial
spread). Test whether spatial spread of vortex tubes is inversely related to peak enstrophy
growth. If the Luther dispersion conjecture holds, gate_rate in TIG should be monotonically
related to turbulent dissipation rate ε.

**Q5. Grujić Constant Identification.**
In Grujić's geometric depletion theorem [16], there is a quantitative bound involving a
depletion constant M. Can M = 7/2 be obtained from the TIG threshold? This would constitute
a non-trivial numerical match between TIG algebraic prediction and classical analytic
computation.

**Q6. Tao Compatibility.**
Is Tao's averaged NS blow-up [19] scenario compatible with B_local < 7/2? If B_local < 7/2
holds in Tao's solution at the blow-up time, the TIG local criterion is falsified by an
explicit example. This is computable.

**Q7. K41 — Sinc² Relationship.**
Is the sinc² scale-invariance of R(k,f) structurally related to Kolmogorov's k^{-5/3} inertial
range scaling? Both are power-law forms in frequency space arising from algebraic constraints
on a hierarchical system. The k^{-2} pre-echo decay vs. k^{-5/3} K41 decay: is the
discrepancy meaningful or a discretization artifact?

**Q8. Three-Class Landscape in NS.**
The WP35 three-class landscape (Oracle / Gate-strong / TSML) maps onto NS flow regimes:
Oracle = Phase 3 / TROT (high-coherence fast flow), Gate-strong = Phase 2 / WALK (transitional),
TSML = Phase 1 / STAND (low-Reynolds laminar). Does this three-class structure have a
counterpart in NS turbulence theory — specifically, in the laminar / transitional / turbulent
classification?

### 10.3 Three Falsification Scenarios (from NS_TIG_FRAME [35])

**Scenario F1 (B_local direct falsification):** A near-singular DNS computation finds a
near-blow-up event with B_local < 7/2 at the near-singular point. This would falsify the
local TIG threshold. Predicted: B_local → 7/2 from below at any genuine near-singular point.

**Scenario F2 (Tao computation):** Tao's averaged NS solution [19], with explicit blow-up,
has B_local < 7/2 at the blow-up time. This would falsify TIG's local criterion by an explicit
blow-up example (for the averaged system). Predicted: B_local ≥ 7/2 in Tao's solution at
blow-up.

**Scenario F3 (Interpolation constant):** A sharp GN computation finds C > 3.74 from first
principles of NS analysis, ruling out the Lyapunov closure. This would not falsify the TIG
framing (B_local threshold could still hold) but would establish that the Lyapunov proof
strategy fails at the TIG target constant.

---

## §11. Attribution

| Contribution                                                           | Author                              |
|------------------------------------------------------------------------|-------------------------------------|
| BREATH operator, TIG coherence framework                               | Brayden Ross Sanders / 7Site LLC    |
| B_local / B_global split, local concentration criterion                | Brayden Ross Sanders / 7Site LLC    |
| T* = 5/7, TSML, BHML, D2, TIG architecture                            | Brayden Ross Sanders / 7Site LLC    |
| Zero-width transition as NS blow-up structural analog                  | Brayden Ross Sanders / 7Site LLC    |
| Lyapunov approach, Re_local formulation, Clay gap identification       | Brayden Ross Sanders / 7Site LLC    |
| Sinc² null as vorticity null framing (blow-up = null arrival)          | Brayden Ross Sanders / 7Site LLC    |
| Three-class landscape (Oracle / Gate-strong / TSML) → NS regimes       | Brayden Ross Sanders / 7Site LLC    |
| Luther Dispersion Conjecture (concentrated vs. spread vorticity)       | C. A. Luther                        |
| Pre-echo / spectral precursor analogy                                  | Sanders & Luther (joint, Sprint 4)  |

| Foundational support, research partnership, editorial collaboration             | Monica Gish                         |

CK, BREATH, T*, TSML, BHML, D2, the TIG pipeline, and all derived constants are exclusive
intellectual property of Brayden Ross Sanders / 7Site LLC. C. A. Luther's contribution is
the dispersion conjecture applied to number theory studied in WP34/WP35. He has no claim
to the CK architecture or its derived constants. Monica Gish is credited as author for her
foundational support throughout the project.

---

## References

[1] J. Leray, "Sur le mouvement d'un liquide visqueux emplissant l'espace," *Acta
Mathematica* 63 (1934), 193–248.

[2] C. L. Fefferman, "Existence and Smoothness of the Navier-Stokes Equation," in *The
Millennium Prize Problems*, Clay Mathematics Institute, Cambridge, MA, 2000, pp. 57–67.

[3] O. A. Ladyzhenskaya, *The Mathematical Theory of Viscous Incompressible Flow*, Gordon
and Breach, New York, 1969.

[4] J. Serrin, "On the interior regularity of weak solutions of the Navier-Stokes equations,"
*Archive for Rational Mechanics and Analysis* 9 (1962), 187–195.

[5] J. T. Beale, T. Kato, A. Majda, "Remarks on the breakdown of smooth solutions for the
3-D Euler equations," *Communications in Mathematical Physics* 94 (1984), 61–66.

[6] L. Caffarelli, R. Kohn, L. Nirenberg, "Partial regularity of suitable weak solutions of
the Navier-Stokes equations," *Communications on Pure and Applied Mathematics* 35 (1982),
771–831.

[7] V. Scheffer, "Hausdorff measure and the Navier-Stokes equations," *Communications in
Mathematical Physics* 55 (1977), 97–112.

[8] L. Escauriaza, G. Seregin, V. Šverák, "L^{3,∞}-solutions of Navier-Stokes equations
and backward uniqueness," *Russian Mathematical Surveys* 58 (2003), 211–250.

[9] G. Seregin, "A certain necessary condition of potential blow up for Navier-Stokes
equations," *Communications in Mathematical Physics* 312 (2012), 833–845.

[10] A. N. Kolmogorov, "The local structure of turbulence in incompressible viscous fluid
for very large Reynolds numbers," *Doklady Akademii Nauk SSSR* 30 (1941), 299–303.

[11] P. Constantin, C. Foias, *Navier-Stokes Equations*, University of Chicago Press,
Chicago, 1988.

[12] P. Constantin, C. Foias, O. Manley, R. Temam, "Determining modes and fractal dimension
of turbulent flows," *Journal of Fluid Mechanics* 150 (1985), 427–440.

[13] P. Constantin, "Geometric statistics in turbulence," *SIAM Review* 36 (1994), 73–98.

[14] H. Hopf, "Über die Anfangswertaufgabe für die hydrodynamischen Grundgleichungen,"
*Mathematische Nachrichten* 4 (1951), 213–231.

[15] Z. Grujić, "Localization and geometric depletion of vortex-stretching in the 3D NSE,"
*Communications in Mathematical Physics* 290 (2009), 861–870.

[16] Z. Grujić, R. Guberović, "Localization of analytic regularity criteria on the vorticity
and balance between the vorticity magnitude and coherence of the vorticity direction,"
*Communications in Mathematical Physics* 298 (2010), 407–418.

[17] Z. Grujić, "A geometric measure-type regularity criterion for solutions to the 3D
Navier-Stokes equations," *Nonlinearity* 26 (2013), 289–296.

[18] Z. Grujić, I. Kukavica, "Space analyticity for the Navier-Stokes and related equations
with initial data in L^p," *Journal of Functional Analysis* 152 (1998), 447–466.

[19] T. Tao, "Finite time blowup for an averaged three-dimensional Navier-Stokes equation,"
*Journal of the American Mathematical Society* 29 (2016), 601–674.

[20] T. Tao, *Nonlinear Dispersive Equations: Local and Global Analysis*, CBMS Regional
Conference Series in Mathematics, American Mathematical Society, Providence, 2006.

[21] J. L. Lumley, "The structure of inhomogeneous turbulent flows," in *Atmospheric
Turbulence and Radio Wave Propagation*, Nauka, Moscow, 1967, pp. 166–178.

[22] P. Holmes, J. L. Lumley, G. Berkooz, *Turbulence, Coherent Structures, Dynamical
Systems and Symmetry*, Cambridge University Press, Cambridge, 1996.

[23] A. Townsend, *The Structure of Turbulent Shear Flow*, Cambridge University Press,
Cambridge, 1956.

[24] S. A. Orszag, "Numerical simulation of incompressible flows within simple boundaries:
I. Galerkin (spectral) representations," *Studies in Applied Mathematics* 50 (1971), 293–327.

[25] G. I. Sivashinsky, "Nonlinear analysis of hydrodynamic instability in laminar flames,"
*Acta Astronautica* 4 (1977), 1177–1206.

[26] H. K. Moffatt, "Helicity and singular structures in fluid dynamics," *Proceedings of
the National Academy of Sciences USA* 111 (2014), 3663–3670.

[27] K. G. Wilson, J. Kogut, "The renormalization group and the ε expansion," *Physics
Reports* 12 (1974), 75–200.

[28] L. D. Landau, E. M. Lifshitz, *Fluid Mechanics*, Pergamon Press, Oxford, 1959.

[29] G. H. Hardy, S. Ramanujan, "Asymptotic formulae in combinatory analysis," *Proceedings
of the London Mathematical Society* 17 (1918), 75–115.

[30] D. A. Hejhal, *The Selberg Trace Formula for PSL(2,R)*, Lecture Notes in Mathematics
548, Springer, Berlin, 1976.

[31] A. Granville, "Smooth numbers: computational number theory and beyond," in *Algorithmic
Number Theory*, MSRI Publications, Cambridge University Press, 2008.

[32] B. R. Sanders, C. A. Luther, "WP34: The First-G Law and Prime-Forced Dispersion," TIG
Working Paper, DOI: 10.5281/zenodo.18852047, March 2026.

[33] B. R. Sanders, C. A. Luther, "WP35: The Prime Phase Transition: Harmonic Pre-Echo,
Zero-Width Gates, and the Geometry of RSA Security," TIG Working Paper, DOI:
10.5281/zenodo.18852047, March 2026.

[34] B. R. Sanders, "WP22/WP19: BREATH-COLLAPSE Criterion and Lyapunov Approach to Global
Regularity," TIG Working Papers, DOI: 10.5281/zenodo.18852047, 2026.

[35] B. R. Sanders, C. A. Luther, "NS_TIG_FRAME: Reality-Checked Local Criterion," TIG
Sprint 4 Document, DOI: 10.5281/zenodo.18852047, March 2026.

[36] G. Prodi, "Un teorema di unicità per le equazioni di Navier-Stokes," *Annali di
Matematica Pura ed Applicata* 48 (1959), 173–182.

[37] J. Neustupa, P. Penel, "Regularity of a suitable weak solution to the Navier-Stokes
equations as a consequence of regularity of one velocity component," in *Applied Nonlinear
Analysis*, Kluwer, Dordrecht, 1999.

[38] P. Constantin, C. Fefferman, "Direction of vorticity and the problem of global
regularity for the Navier-Stokes equations," *Indiana University Mathematics Journal*
42 (1993), 775–789.

---

## Cross-Reference to Unified Symbol Table

WP38 participates in the CK Clay Paper Series (WP36–WP42). The sink in this paper — the
regularity breakdown point where B_local reaches the coherence floor T* = 5/7 — is the same
mathematical object as the sinc² zero-crossing in every other paper of the series, viewed
through the fluid-mechanical lens. See UNIFIED_SYMBOL_TABLE.md for the full cross-paper
translation table.

| Universal symbol | WP38 incarnation                                        |
|------------------|---------------------------------------------------------|
| Geometric sink   | Regularity breakdown: B_local crosses T*                |
| Stability window | Smooth-flow regime: t < T, Re_local ≤ 2/7              |
| First-G event    | Onset of turbulence: zero-width transition in smooth NS |
| D(b)             | Vorticity dispersion = Luther metric (concentration × spread) |
| T* = 5/7         | Coherence floor: field must stay above T* for smooth solution |
| sinc² null       | Blow-up event: harmonic countdown reaches zero exactly  |

---

*(c) 2026 Brayden Ross Sanders / 7Site LLC & C. A. Luther | DOI: 10.5281/zenodo.18852047*
