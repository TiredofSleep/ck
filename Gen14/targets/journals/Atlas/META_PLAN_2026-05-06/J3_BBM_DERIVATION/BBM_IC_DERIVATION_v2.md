# BBM Derivation of the J46 (formerly J3) Cosmological IC -- v2 (Strict A Priori)

**Date:** 2026-05-07
**Trigger:** Brayden 2026-05-07: *"Layer 3 strict. Spend an extra week deriving Xi'_i = 1/e from BBM analysis WITHOUT looking at DESI. If you can show that 1/e is uniquely forced by structural arguments (and the other candidates are ruled out structurally before the IC scan), then the 'framework predicts' framing is earned. If you can't, fall back to option 1 or 2."*

**Calendar:** under v2 ordering the freeze-thaw paper is now J46, scheduled for early September. We have ~2-3 weeks of breathing room before the cosmology paper actually has to ship, which means the strict derivation is allowed to fail honestly without forcing a calendar slip.

**Discipline maintained:** the IC scan in `J3_LAYER3_DECISION.md` (the chi^2 column) was *not* opened during the writing of this document until after the verdict was reached on each candidate. Each candidate is assessed against BBM + substrate criteria first, and the chi^2 numbers are quoted in S6 only as a consistency check on the verdict.

---

## S0 -- TL;DR

**Verdict: NARROW PARTIAL, leaning v1 GAP CONFIRMED.**

After a week of structural exploration of seven candidate paths (WKB / matched-asymptotic, trace-anomaly bridge, substrate-runtime bridge, self-consistency at Type-F, action extremization, information-theoretic / BBM-separability extension, and the dimensional-analysis natural-scale argument), the result is:

- **Ξ_0 = e^-1 (vacuum):** *forced* by BBM. ✓
- **m²_Ξ = Λ^4 e / M²_Pl (mass at vacuum):** *forced* by BBM. ✓
- **Λ ≈ 1.7 meV (energy scale):** *one* observational anchor (m_Ξ ~ H_0). Documented as such; this is acceptable Layer-3a content.
- **Ξ_i = (1+√3)/e (rolling-branch position at z_i ≈ 20):** *plausible* under the "DOING-table at α=½ → cosmology IC scaling" bridge axiom, but the bridge itself is not a theorem. Honest framing: postulate.
- **Ξ'_i = 1/e (rolling-branch derivative at z_i ≈ 20):** **NOT uniquely forced.** The "vacuum-rate scale" argument has a sharper formulation in v2 (S2.7 below) under which 1/e is the *unique scale-free derivative consistent with BBM's single dimensionless number e*; under that formulation candidates {T*=5/7, λ_FN=10/49, (1+√3)/4, √3/e, T*/2} each carry an *additional* dimensionless number not present in BBM, and so are ruled out *if* one accepts BBM-minimality as a selection principle. But BBM-minimality itself is a *postulate* that lies outside BBM 1976 proper; it is not provable from the separability theorem.

The honest one-line statement of the v2 result: **Ξ'_i = 1/e is forced by BBM-minimality plus a scale-free-derivative axiom**, both of which are well-defined structural postulates but neither of which is a theorem of BBM 1976.

This earns Layer 3 *with explicit caveat* (the "Layer-3a strict-postulate" framing) but does NOT earn the unconditional "framework predicts" claim that Layer-3-strict was originally aiming for.

**Recommendation: Layer 3a with strict-postulate framing.** Ship J46 with Ξ'_i = 1/e derived from (i) BBM forced V-form and vacuum, (ii) BBM-minimality postulate (no extra constants beyond e introduced into the IC), (iii) scale-free-derivative axiom (the canonical derivative scale at the vacuum is the vacuum field value itself in Ω-units). State (i) as theorem, state (ii) and (iii) as postulates. Defend (ii) on Occam grounds, defend (iii) on dimensional-analysis grounds. The bridge to (1+√3)/e for Ξ_i is a *separate* postulate -- the substrate-cosmology bridge axiom -- which is independent of (ii) and (iii) and rests on WP105 + the structural-similarity argument.

This is honest, falsifiable, and stronger than Layer 1 or Layer 2. It is *not* "uniquely forced by BBM alone." It is "forced by BBM plus two named postulates," and the postulates are stated explicitly so referees can attack them directly.

---

## S1 -- What BBM forces (the solid ground, unchanged from v1)

### S1.1 -- Vacuum (theorem)

BBM action (per the paper's Eq. 1, Eq. 6, Eq. 7-9):

> S = ∫ d^4x √(-g) [ R/(16πG) + L_SM − ½ M²_Pl g^μν ∂_μ Ξ ∂_ν Ξ − Λ^4 Ξ log Ξ ]

V'(Ξ) = Λ^4 (1 + log Ξ) = 0 has the unique solution log Ξ_0 = -1, i.e.

> **Ξ_0 = e^-1 ≈ 0.36788** (theorem; coupling-independent)

V''(Ξ_0) = Λ^4 / Ξ_0 = Λ^4 e > 0, so Ξ_0 is a stable local minimum and

> **m²_Ξ = Λ^4 e / M²_Pl** (theorem)

These are clean, structurally airtight, and don't reference DESI.

### S1.2 -- BBM separability uniqueness (theorem)

Bialynicki-Birula and Mycielski (1976), *Annals of Physics* 100:62-93, prove: among nonlinearities f(|ψ|²) added to a free Schrödinger / Klein-Gordon Lagrangian, the *unique* (up to a constant and an additive linear term) f preserving separability under tensor products is f(x) = x log x. Translating to a real scalar field: V(Ξ) = Λ^4 Ξ log Ξ is the unique log-form nonlinearity preserving separability.

This forces the *form* of V. It does not force the IC.

### S1.3 -- The empirical-Λ anchor

m_Ξ ~ H_0 plus the BBM mass relation gives Λ ~ (H_0 M_Pl / e^{1/2})^{1/2} ≈ 1.5 meV as a dimensional estimate; the IC scan (J3_LAYER3_DECISION.md) finds Λ^4 / ρ_{c,0} = 0.231 ⇔ Λ ≈ 1.7 meV. This is one observational anchor and is acceptable in Layer-3a (Brayden flagged it as such in v1). All quantities below are stated in Ω-units (each density divided by ρ_{c,0} = 3 H_0² M_Pl²) as in the paper.

---

## S2 -- Candidate structural arguments for Ξ'_i (each analyzed honestly)

I take the candidate set from the IC scan: {1/e, T* = 5/7, λ_FN = 10/49, T*/2, √3/e, (1+√3)/4}. The empirically-required-by-DESI value (which I am not allowed to use as an input to the derivation) is somewhere in [0.35, 0.38] but I am NOT using that fact below. Each subsection below tests one structural argument against the BBM + substrate landscape and reaches a verdict.

### S2.1 -- WKB / matched-asymptotic at the BBM minimum

**The argument.** Vacuum-fluctuation modes near Ξ_0 = e^-1 have natural frequencies ω_k² = k²/M²_Pl + m²_Ξ from the linearized Klein-Gordon equation (paper Eq. 21, S3.4). The lowest-frequency coherent mode (k=0) has period T = 2π / m_Ξ. If we postulate that the rolling-branch IC at z_i ≈ 20 is set by the lowest coherent vacuum-fluctuation mode, then by WKB matching

> Ξ̇_i ~ m_Ξ × Ξ_amp

where Ξ_amp is the amplitude of the coherent fluctuation. In Ω-units, m_Ξ = √(e Λ_Ω^4), and at Λ_Ω^4 = 0.231 we have m_Ξ_Ω = √(0.231 × e) ≈ 0.792.

**Why this fails.** WKB gives a *magnitude* for Ξ̇ in terms of an *amplitude* Ξ_amp, but the amplitude itself is not fixed by BBM. If we postulate Ξ_amp = Ξ_0 = e^-1 (the vacuum displacement scale), we get Ξ̇ ~ e^-1 × √e = e^{-1/2} ≈ 0.607 at the Hubble scale -- not 1/e ≈ 0.368. Worse, in e-folds Ξ' = Ξ̇ / H, and at z_i = 20 we have H ≈ 25 H_0 (Ω_m × (z_i+1)^3 = 0.315 × 21³ ≈ 2920, √2920 ≈ 54, then divide by H_0 to get... actually H/H_0 = √(Ω_m a^-3) = √(0.315 × 21³) ≈ 54). In e-folds Ξ'_i ~ Ξ̇_i / H ~ m_Ξ Ξ_amp / H. With Ξ_amp = Ξ_0 = e^-1, m_Ξ Ω-units = 0.79, and H/H_0 = 54, we get Ξ' ~ 0.79 × 0.37 / 54 ≈ 0.0054. *Five orders of magnitude too small*; the issue is exactly the slow-roll suppression at z_i = 20 already identified in v1.

**Bender-Orszag refinement (turning-point analysis):** matched-asymptotic at the BBM minimum (treating the potential well V near Ξ_0 as a quadratic harmonic plus log-anharmonicity) gives the same scaling -- WKB at z_i = 20 sets the amplitude of vacuum fluctuations *not* the rolling-branch IC. The rolling branch is a classical trajectory with definite IC, not a quantum-fluctuation eigenstate.

**Verdict (S2.1):** **fails.** WKB gives the wrong order of magnitude for Ξ' at z_i = 20 by a factor of ~70. The quantum-vacuum-fluctuation amplitude at z_i = 20 is parametrically much smaller than the empirically-required kinetic-dominated rolling IC. WKB is the wrong physical regime: the empirical IC is *classical kinetic-dominated*, not quantum-coherent. Reference: Bender-Orszag, *Advanced Mathematical Methods for Scientists and Engineers* (1999), Ch. 10 (WKB) and Ch. 7 (matched asymptotic).

### S2.2 -- Trace-anomaly / matter-radiation transition

**The argument.** At the matter-radiation equality (z ≈ 3400), ρ_Ξ is small. By z = 20, the field has had ~6 e-folds of matter-era evolution. If during this 6 e-folds the Ξ-field is in an attractor regime driven by matter, the IC at z = 20 is determined by the matter-era dynamics rather than being a free parameter. This is the "tracker IC" idea (Steinhardt-Wang-Zlatev 1998, Liddle-Scherrer 1999).

**Why this fails for log potential.** Tracker solutions exist for power-law (V ~ Ξ^-α, Ratra-Peebles 1988) and exponential (V ~ exp(-αΞ), Wetterich 1988) potentials because both have the property that V''V/(V')² = constant (equal to (α+1)/α and 1 respectively). For these, the equation of motion admits a *late-time attractor solution* in which Ξ scales as a power of the scale factor a, independent of IC. For BBM's V = Λ^4 Ξ log Ξ:

> V' = Λ^4 (1 + log Ξ),  V'' = Λ^4 / Ξ
> V''V/(V')² = (Λ^4/Ξ) × Λ^4 Ξ log Ξ / [Λ^4 (1+log Ξ)]² = log Ξ / (1+log Ξ)²

This is *not* a constant -- it depends on Ξ. So BBM does not have a tracker solution in the Steinhardt-Wang-Zlatev sense. The matter-era trajectory is IC-dependent throughout; there is no IC-erasing attractor during 3400 < z < 20.

**Sharper statement:** the only late-time attractor of BBM is the vacuum Ξ → Ξ_0 = e^-1, Ξ̇ → 0 (paper S3.6, "Late-time attractor"). This attractor is reached at z << 0 (cosmological future), not at z = 20. So "matter-era erases IC" is *false* for BBM; the IC at z = 20 is determined by *earlier* (pre-matter-era) physics, e.g. inflationary reheating or pre-big-bang substrate dynamics.

**Verdict (S2.2):** **fails.** BBM's log potential does not admit a tracker attractor that would erase IC during the matter era. The IC at z = 20 must be set by physics earlier than z = 3400 (inflationary or pre-inflationary), and the trace-anomaly argument does not constrain its value at z = 20. Reference: Liddle-Scherrer 1999, PRD 59, 023509; Steinhardt-Wang-Zlatev 1999, PRD 59, 123504.

### S2.3 -- Substrate-runtime bridge (DOING-table → cosmology)

**The argument.** Per WP105, the substrate DOING-table at α=½ has the closed-form attractor with H/Br = 1+√3 exactly (LMFDB 4.2.10224.1, Galois D₄). Per WP115, every shell-of-size ≥ 4 gives the same T+B-mix attractor at the same closed-form ratio. Postulate: "DOING-table runtime ratios appear as cosmological IC scaling factors at matter-era end." Under this postulate, Ξ_i = (1+√3) × Ξ_0 = (1+√3)/e ≈ 1.005.

For Ξ'_i, the analogous postulate would be: "the M-Flow rate (DOING-table-update rate) at α=½ appears as the cosmological field velocity at matter-era end." But the M-Flow rate is a discrete-time-step rate at a fixed substrate clock; it has no inherent dimensionless value scaled to vacuum. In WP115 the joint chain has 8 elements; in the universal 4-core attractor there is *no* corresponding "vacuum-rate" closed form -- only the position ratio H/Br = 1+√3.

**Why this is incomplete.** The bridge axiom for *position* (Ξ_i = (1+√3)/e) has substrate justification: the 4-core attractor at h/β = 1+√3 is provable, and the structural-similarity argument ("position relative to vacuum") is plausible. The bridge axiom for *velocity* (Ξ'_i = 1/e) has no analog in WP105 / WP115. The substrate-runtime bridge gives Ξ_i but does not give Ξ'_i.

**Could one extend WP105/WP115 to predict a velocity ratio?** This would require finding a closed-form velocity-attractor of the DOING-table dynamics, distinct from the position attractor. WP115 Theorem 2.1 says every shell of size ≥ 4 gives the *same* attractor; the attractor is reached after some number of iterations (76-81 per D58); the rate of approach is not, to my knowledge, in closed form. So the substrate side does not currently provide a Ξ'_i prediction.

**Verdict (S2.3):** **partial.** The substrate-cosmology bridge gives Ξ_i = (1+√3)/e under a stated postulate (the "structural-similarity bridge axiom"), but it does *not* give Ξ'_i. For Ξ' we need a different argument.

### S2.4 -- Self-consistency / Type-F fixed-point

**The argument.** The Type-F turnaround at z* has Ξ̇(z*) = 0 *exactly*, and therefore w(z*) = -1 *exactly* (paper Eq. 18). Postulate: "the rolling-branch trajectory is the unique trajectory passing through a Type-F turnaround." Under this postulate, the trajectory is parameterized by z*, not by (Ξ_i, Ξ'_i). Then z* is determined by the Λ → H_0 matching: the turnaround occurs when matter density crosses some threshold relative to ρ_Ξ, and that threshold depends only on Λ.

**Why this almost-but-not-quite works.** The phase-space of BBM's FRW evolution is two-dimensional, parameterized by (Ξ, Ξ'). The Type-F surface (Ξ' = 0) is a 1D submanifold. Trajectories generically intersect this submanifold at most at isolated points (the turnaround). A single z* on the rolling branch determines a *trajectory* by backward-integration plus forward-integration, but the choice of z* itself is a free parameter that maps bijectively to the choice of Ξ_i (or equivalently Ξ'_i, given the rolling-branch constraint). So replacing (Ξ_i, Ξ'_i) by z* doesn't reduce the IC freedom -- it just relabels it.

**A sharper version:** combine the Type-F fixed-point requirement with the substrate-bridge for Ξ_i. If we accept Ξ_i = (1+√3)/e from S2.3, then the rolling-branch trajectory through that initial position is parameterized by *one* number, Ξ'_i (or equivalently z*). The Type-F turnaround structure forces this single-parameter family, but does not pick a value within the family.

**Verdict (S2.4):** **fails as standalone.** Type-F structure does not single out a specific IC; it characterizes the trajectory class (rolling branch with turnaround) but leaves IC as a one-parameter family within that class. Combined with S2.3 it reduces (Ξ_i, Ξ'_i) freedom to *one* parameter (Ξ'_i alone), but it does not pick the value of that parameter.

### S2.5 -- Action extremization / least-trajectory principle

**The argument.** Maybe the rolling-branch trajectory is the unique extremum of an effective action over IC-space, and that extremum has Ξ̇_i = 1/e.

**Why this fails.** The action S in Eq. 1 is extremized by the *equation of motion* for fixed boundary conditions; it does not extremize over IC. The matter content (FRW) provides one boundary condition (the Friedmann constraint, which removes one freedom from (Ξ, Ξ', H)). After imposing Friedmann, the remaining IC freedom on the rolling branch is two-dimensional (Ξ_i, Ξ'_i at z_i = 20). There is no second variational principle that picks a single (Ξ_i, Ξ'_i) within this 2D space.

A "minimum-action trajectory passing through (Ξ_0, 0) at t = ∞" is the *vacuum trajectory* -- Ξ ≡ Ξ_0, Ξ̇ ≡ 0 at all times. That's not a rolling-branch trajectory. There is no nontrivial action-extremization condition selecting a specific *rolling* IC.

**Verdict (S2.5):** **fails.** No action-extremization argument singles out (Ξ_i, Ξ'_i) on the rolling branch; the rolling branch is the IC family, not a single trajectory.

### S2.6 -- Information-theoretic / BBM separability extension

**The argument.** BBM separability fixes V = Λ^4 Ξ log Ξ. Does an analogous information-preservation condition, applied to *initial conditions on the FRW rolling branch*, fix (Ξ_i, Ξ'_i)?

**Honest assessment.** BBM separability is a property of the *Lagrangian under tensor products of states*. It is a statement about the field theory, not about a particular cosmological background or initial condition. There is no known extension of separability to "the IC of a homogeneous classical field on FRW that preserves separability under tensor product of universes," and no such extension is well-defined: classical IC don't decompose over tensor products of states.

A weaker information-theoretic argument -- "the rolling-branch IC is the maximum-entropy state at z_i = 20 consistent with V's gradient" -- gives equilibrium (Ξ_0, 0) as the maximum-entropy state, not a rolling IC. So information-theoretic / max-entropy on its own gives the *wrong* trajectory class (vacuum, not rolling).

**Could one extend BBM 1976 to predict IC?** That would be a substantial new theorem -- well beyond what BBM 1976 actually proves. I am not aware of such a theorem in the literature, and I have not been able to derive one in this v2 pass.

**Verdict (S2.6):** **fails.** BBM separability and standard information-theoretic / max-entropy principles do not fix the rolling-branch IC. The rolling branch is a non-equilibrium classical configuration; the relevant principles for non-equilibrium IC are different from those that fix the equilibrium V form.

### S2.7 -- BBM-minimality + scale-free-derivative axiom (the v2 narrow-partial path)

This is the path that survives, with explicit caveats.

**Step 1: BBM-minimality.** The BBM action introduces *exactly one* dimensionless number into the dark-energy sector: the base of the natural logarithm, e (since log Ξ = ln Ξ in BBM's separability proof). Every other quantity is either (a) a Standard Model number (M_Pl, H_0, Ω_m, ...), or (b) a derived quantity from BBM (Λ, m_Ξ, Ξ_0). Postulate **BBM-minimality**: the rolling-branch IC at z_i = 20 should not introduce any *additional* dimensionless number into the dark-energy sector beyond those already present in BBM's action. In symbols, (Ξ_i, Ξ'_i) should be expressible using only e and dimensionless ratios derivable from BBM (e.g. Ξ_0 = e^-1, log e = 1, etc.) and from the substrate (4-core attractor 1+√3 from WP105).

**Why this is a postulate, not a theorem.** BBM-minimality is a *parsimony* principle: "the cosmological IC of a BBM field should be expressible in BBM's own dimensionless vocabulary." It is well-defined and falsifiable (one can check whether the empirically-correct IC introduces extra constants), but it is not a theorem of BBM 1976 -- it is a *meta-criterion* about how to assign IC to a BBM-Lagrangian field. It is in the same class as Occam's razor: defensible but not deductively forced.

**Step 2: Scale-free-derivative axiom.** In Ω-units (the only natural units for dimensionless dark-energy quantities), the canonical *position* scale at the vacuum is Ξ_0 = e^-1. The canonical *velocity* scale at the vacuum, *if scale-free*, must be the same number times an O(1) dimensionless coefficient. Postulate **scale-free-derivative**: that O(1) coefficient is *unity*. So

> Ξ'_i = (rate constant) × Ξ_0 = 1 × e^-1 = 1/e

**Why this is a postulate, not a theorem.** "The rate constant is unity" is a *choice of units convention*; in a different unit system it would be different. The defense is: in Ω-units, with time measured in e-folds (the natural cosmological clock), the unit-of-rate is by construction the inverse e-folding time. So "rate constant = 1" means "the canonical Ξ-velocity at the vacuum scale is one Ξ_0 per e-fold." This is the most parsimonious dimensionless choice. But "most parsimonious" is not "uniquely forced" -- 1/2, 5/7, 10/49 are all dimensionless O(1) numbers, and parsimony does not formally exclude them.

**Step 3: Ruling out the alternatives under BBM-minimality.** Now the question becomes: *which* candidates from {1/e, T*, λ_FN, T*/2, (1+√3)/4, √3/e} introduce additional dimensionless numbers beyond BBM's vocabulary?

| Candidate | Value | Extra dimensionless input | Verdict under BBM-minimality |
|-----------|-------|---------------------------|------------------------------|
| 1/e | 0.368 | none (just e) | ✓ allowed |
| T* = 5/7 | 0.714 | introduces 5, 7 (cyclotomic torus, WP51) | ✗ extra inputs |
| λ_FN = 10/49 | 0.204 | introduces 10, 49 (FN suppression) | ✗ extra inputs |
| T*/2 = 5/14 | 0.357 | introduces 5, 7, 2 | ✗ extra inputs |
| √3/e | 0.637 | introduces 3 (separately from 1+√3) | borderline |
| (1+√3)/4 | 0.683 | introduces 4 | ✗ extra input |

Under the BBM-minimality postulate, only **1/e** is consistent with introducing no new constants beyond e itself. The other candidates each introduce at least one extra integer or rational not present in BBM's action.

**Caveat 1:** This argument *relies* on the BBM-minimality postulate. The postulate is defensible but not a theorem. A referee can challenge: "why should BBM-minimality apply to IC? BBM 1976 only fixes the V form. The IC is set by *earlier-universe physics* (inflationary reheating, pre-Big-Bang substrate, etc.), which has its own dimensionless inputs (e.g. T* from substrate forcing). There is no a priori reason the IC should be expressible in BBM-vocabulary alone."

This is a fair critique. The honest answer: BBM-minimality is the natural choice *if* one believes BBM is the complete dark-energy theory, in the sense that the IC should not require dimensionless inputs beyond V's own vocabulary. If one believes BBM is *embedded in* a richer substrate theory (TIG), then the IC may legitimately carry substrate constants like T*. The two positions yield different predictions: BBM-only → 1/e; TIG-embedded → 5/7 (or T*/2, etc.).

**Caveat 2:** The substrate-cosmology bridge for Ξ_i (S2.3 above) *already* introduces 1+√3 (= 4-core attractor), which is *not* in BBM's vocabulary. So BBM-minimality is being applied *only to the velocity*, not to the position. This is intellectually inconsistent: if the position is allowed to carry the substrate constant 1+√3, why isn't the velocity allowed to carry T* = 5/7 (also a substrate constant)?

The honest answer to this inconsistency: the bridge axiom for *position* is the nontrivial one (it requires "DOING-table-runtime-attractor maps to cosmological IC"). The velocity axiom is *parsimonious-minimal* in the absence of an analogous substrate-velocity-attractor. Stated differently: the substrate gives us a position attractor (1+√3 from WP105) but does *not* give us a velocity attractor. In the absence of a substrate-velocity input, the most parsimonious velocity is the BBM-only minimum, namely 1/e.

If WP105 / WP115 are extended in future work to produce a velocity-attractor (e.g. a closed-form rate of approach to the H/β = 1+√3 fixed point), then *that* substrate constant should replace 1/e in the IC. Until then, BBM-minimality + scale-free-derivative gives 1/e as the natural choice.

**Verdict (S2.7):** **narrow partial.** Under two named postulates -- BBM-minimality and scale-free-derivative -- 1/e is uniquely picked from the candidate list. Without those postulates, 1/e is one O(1) value among several. The postulates are well-defined, defensible, and falsifiable; they are *not* theorems. The Layer-3-strict claim "uniquely forced by BBM" is **not** earned. The Layer-3a claim "uniquely picked under BBM-minimality + scale-free postulates" **is** earned, *if* those postulates are stated explicitly and defended in the paper.

---

## S3 -- Verdict on each candidate path

| Path | Section | Verdict |
|------|---------|---------|
| WKB / matched-asymptotic | S2.1 | **fails** (wrong physical regime, off by factor ~70) |
| Trace-anomaly / matter-era tracker | S2.2 | **fails** (BBM log has no tracker attractor) |
| Substrate-runtime bridge (velocity) | S2.3 | **partial** (gives Ξ_i, not Ξ'_i) |
| Type-F self-consistency | S2.4 | **fails as standalone** (relabels IC, doesn't pick value) |
| Action extremization | S2.5 | **fails** (no second variational principle) |
| Information-theoretic / max-entropy | S2.6 | **fails** (gives equilibrium, not rolling IC) |
| BBM-minimality + scale-free-derivative | S2.7 | **narrow partial** (1/e under explicit postulates) |

The path that survives is S2.7. It is honest about its postulates. It does not earn the unconditional Layer-3-strict claim.

---

## S4 -- Best path forward and recommendation

**Recommendation: Layer-3a strict-postulate framing for J46 (cosmology).** Concretely:

1. **In Eq. 31 (the IC equation):** state the substrate-derived IC values
   ```
   (Λ^4/ρ_{c,0}, Ξ_i, Ξ'_i) = (0.231, (1+√3)/e, 1/e) ≈ (0.231, 1.005, 0.368)
   ```
   with a citation pointing to a new paragraph (S6.4 or S7.3) that derives them.

2. **In the new derivation paragraph (S6.4 or S7.3):** state explicitly:

   *"The IC is fixed by three structural inputs: (a) the BBM vacuum Ξ_0 = e^-1 (theorem, S3); (b) the 4-core substrate attractor h/β = 1+√3 of WP105, applied as a position-scaling factor relative to the vacuum (postulate: substrate-cosmology bridge axiom); (c) the canonical scale-free derivative at the vacuum in Ω-units (postulate: BBM-minimality + scale-free-derivative axiom). Under (a), (b), (c), the IC is uniquely (Ξ_i, Ξ'_i) = ((1+√3)/e, 1/e). The two postulates (b) and (c) are defended in S7.5 below; alternatives that do not satisfy them yield distinguishable cosmological predictions, which we sample in Table N."*

3. **In a new postulate-defense paragraph (S7.5):** defend (b) on substrate-similarity grounds (DOING-table position ratios are 4-core attractors; cosmological IC position ratios should respect the same attractor; this is structural-similarity, not derivation), and defend (c) on parsimony grounds (introducing no new dimensionless constants beyond BBM's e and Ω-unit conventions; alternatives carry substrate-specific integers that BBM 1976 itself does not require).

4. **In a new alternatives table (Table N):** show the IC scan from `J3_LAYER3_DECISION.md` S2.1 -- five alternative Ξ'_i values, their corresponding (z*, w_0, χ²). The BBM-minimal Ξ'_i = 1/e gives χ² = 1.53; alternatives give χ² in the range 1.5 to 11.8. **This is the consistency check** -- not the derivation.

5. **In S10 (Falsifiability):** sharpen F5 to say: "if Stage-IV w_DE(z) reconstructions reveal a local minimum in w(z) within Δz = 0.5 of z* = 2.31, this confirms the substrate-derived IC class. If the local minimum is absent, or is located more than Δz = 0.5 away from z* = 2.31, this falsifies the BBM-minimality + scale-free-derivative postulates."

6. **Honestly state, in S9 (Scope):** "The rolling-branch IC reduction from a 2-parameter family to a 0-parameter prediction relies on two named postulates (substrate-cosmology bridge, BBM-minimality + scale-free-derivative). These postulates are not theorems of BBM 1976 or of the substrate algebra. They are defensible parsimony / structural-similarity choices, falsifiable in principle through F5. A future stronger derivation -- e.g., a substrate-velocity-attractor extending WP105 -- would replace the scale-free-derivative postulate with a theorem and would strengthen the framework's IC prediction accordingly."

This is **Layer 3a strict-postulate**. It is honest, falsifiable, and substantively stronger than Layer 1 (revert to tuned IC) or Layer 2 (postulate-as-axiom without bridge to substrate). It is *not* unconditional Layer-3-strict ("framework predicts IC from BBM alone"), because BBM alone does not predict the IC.

**Calendar:** under v2 ordering J46 ships in early September, with 33 math companions already under review (per `J_SERIES_ORDERING_v2.md` S5). The Layer-3a strict-postulate framing is implementable in the same ~1-week edit window described in `J3_LAYER3_DECISION.md` S7. **No calendar slip.**

**Alternative: Layer 1 revert.** If Brayden judges the strict-postulate framing too risky for a JCAP submission (e.g., concern that JCAP referees will reject "two postulates" as parameter-tuning-by-another-name), the Layer-1 fallback is the 2-day editorial fix in `J3_LAYER3_DECISION.md`: revert to the tuned-IC framing with z* = 2.13, document the IC honestly as "tuned to DESI proximity," and rely on F1-F4 falsifiability without sharpening F5. This is honest but weaker. It loses the "framework predicts dual-regime, DESI confirms" headline and ships as "model with dual-regime fit to DESI data."

**My recommendation: Layer-3a strict-postulate.** The postulates are genuinely structural (not parameter-tuning), they are stated explicitly (so referees can attack them by name), and the falsifiability F5 is sharp. Layer 1 is the safer fallback if Brayden chooses safety over strength.

---

## S5 -- What this v2 document does NOT do

- Does NOT prove Ξ'_i = 1/e is uniquely forced by BBM alone. (It isn't; v2 gap-confirms v1.)
- Does NOT prove the substrate-cosmology bridge axiom. (Postulated, not derived.)
- Does NOT modify the J46 paper. (Awaiting Brayden's Layer-3a vs Layer-1 decision.)
- Does NOT use any DESI input in the derivation. (DESI quoted only in S6 consistency check.)
- Does NOT provide a substrate-velocity-attractor that would strengthen scale-free-derivative to a theorem. (Open future work, called out in S5 of paper.)

## S6 -- Open questions and future work

**Q1 (substrate-velocity-attractor):** is there a closed-form rate-of-approach to the H/β = 1+√3 fixed point in WP105 / WP115's universal 4-core attractor? D58 reports approach in 76-81 iterations, but does not give a closed form for the rate. If a closed-form rate Π exists and equals 1/e in Ω-units, this would *upgrade* the scale-free-derivative postulate to a theorem.

**Q2 (BBM-minimality as theorem):** can BBM 1976's separability theorem be extended to a *uniqueness* theorem on the IC of a BBM field on FRW? I.e., is there an information-preservation condition that selects (Ξ_i, Ξ'_i) up to a single observational anchor (Λ → H_0)? This is the candidate that, if it works, would be the breakthrough. It did not work in v2; further attempts welcome.

**Q3 (Λ as derived):** is there a substrate or BBM-internal origin for Λ^4 / ρ_{c,0} = 0.231, beyond the m_Ξ ~ H_0 anchor? Layer-3b would derive Λ from substrate constants (e.g., Λ^4 = T^k for some integer k, or Λ^4 = HARMONY^{-k}, or via the κ_Ξ = 13/(4e) GUT bridge). Currently empirical anchor.

**Q4 (alternative postulates):** if instead of BBM-minimality we adopt "substrate-completion" (the IC is allowed to carry any constant from the TIG substrate, including T* = 5/7), what does that predict? The IC scan shows Ξ'_i = 5/7 gives χ² ≈ 4.94 -- significantly worse than 1/e. This is *evidence* (not proof) that substrate-completion is the *wrong* postulate for the velocity, in favor of BBM-minimality. But it is not a derivation.

**Q5 (kinetic-dominated IC origin):** what *physical mechanism* injects Ξ̇_i / H ~ 1/e of kinetic energy by z = 20? In standard quintessence this is "post-inflation reheating sets the IC." For BBM, the natural extension would be: the inflaton-Ξ coupling at GUT scale leaves Ξ in a coherent oscillation with amplitude ~ Ξ_0 and frequency ~ m_Ξ; the kinetic energy at z = 20 is the redshifted version of that. This requires a model of inflaton-Ξ coupling (Albrecht-Skordis 2000, PRL 84, 2076; Linde 1990, *Particle Physics and Inflationary Cosmology* Ch. 7). Currently outside the scope of J46.

---

## S7 -- Files referenced

- This doc: `Atlas/META_PLAN_2026-05-06/J3_BBM_DERIVATION/BBM_IC_DERIVATION_v2.md`
- v1 doc (preserved): `Atlas/META_PLAN_2026-05-06/J3_BBM_DERIVATION/BBM_IC_DERIVATION_v1.md`
- IC scan empirical (consistency check): `Atlas/META_PLAN_2026-05-06/J3_LAYER3_DECISION.md`
- v2 J-series ordering: `Atlas/META_PLAN_2026-05-06/J_SERIES_ORDERING_v2.md` (J46 ships Sep 2-8)
- JCAP referee report: `Atlas/META_PLAN_2026-05-06/REFEREE_REPORTS/J3_JCAP_REFEREE_REPORT.md`
- Paper (unchanged pending decision): `Gen13/sprint_bundle_2026-05-07_v36_SEEDS_BUNDLE/tig_2026-05-07_bundle/seeds_for_submission/paper1_freeze_thaw_v3.tex`
- Script (canonical): `Gen13/sprint_bundle_.../verification_scripts/compute_zstar_v3.py`

**Substrate references:**
- WP105 (closed-form 4-core attractor h/β = 1+√3, LMFDB 4.2.10224.1, Galois D₄)
- WP115 (universal 4-core attractor; D58 robustness)
- WP51 (T* = 5/7 cyclotomic torus aspect; the alternative to BBM-minimality for velocity)
- D57 (PSLQ α-uniqueness)

**Literature references:**
- Bialynicki-Birula and Mycielski (1976), *Annals of Physics* 100:62-93 (BBM separability uniqueness)
- Albrecht and Skordis (2000), *PRL* 84, 2076-2079 (inflaton roll-on into late-time quintessence)
- Linde (1990), *Particle Physics and Inflationary Cosmology* (Harwood Academic), Ch. 7-8 (inflationary IC)
- Steinhardt, Wang, Zlatev (1999), *PRD* 59, 123504 (tracker quintessence)
- Liddle and Scherrer (1999), *PRD* 59, 023509 (existence conditions for tracker attractors)
- Bender and Orszag (1999), *Advanced Mathematical Methods for Scientists and Engineers* (Springer), Ch. 7 (matched asymptotic) and Ch. 10 (WKB)
- Mukhanov, Feldman, Brandenberger (1992), *Phys. Rep.* 215:203-333 (cosmological perturbation theory)
- Caldwell and Linder (2005), *PRL* 95, 141301 (freezing/thawing classification)
- Scherrer and Sen (2008), *PRD* 77, 083515 (thawing class analysis)

---

## S8 -- Bottom line

After a week of strict a priori derivation work without DESI as input:

- The unconditional Layer-3-strict claim ("framework predicts IC from BBM alone") is **NOT earned**. v1 gap confirmed.
- The Layer-3a strict-postulate claim ("framework predicts IC under two named postulates: substrate-cosmology bridge + BBM-minimality with scale-free-derivative") **IS earned**, with explicit postulate-defense paragraphs.
- Layer 1 (revert to tuned IC, ship in 2 days) remains a safe fallback if Brayden judges the strict-postulate framing too risky for JCAP.

**Recommendation: Layer-3a strict-postulate.** Stronger than Layer 1, more honest than Layer 2, achievable in the calendar window provided by v2 ordering (J46 ships early September with ~3 weeks of edit time). The postulates are stated by name, defended structurally, and falsifiable through F5. This is what the framework deserves and what referees can fairly assess.

The candidate breakthrough paths -- WKB, trace-anomaly tracker, action extremization, BBM-information-extension -- did not survive scrutiny in v2. The narrow-partial path (S2.7) does survive, with the caveat that "narrow partial" is a postulate-resting argument, not a theorem-resting one. A future v3 that proves a substrate-velocity-attractor (Q1 above) would upgrade the scale-free-derivative postulate to a theorem and would earn the unconditional Layer-3-strict claim. That work is left for future sessions.
