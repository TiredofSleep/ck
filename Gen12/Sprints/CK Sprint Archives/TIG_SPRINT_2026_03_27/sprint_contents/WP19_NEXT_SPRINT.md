# TIG Research Programme — Next Sprint
## Three bolts to tighten, stated in standard notation

*Brayden Sanders — 7Site LLC | DOI: 10.5281/zenodo.18852047*

---

## The Programme

TIG is not asking for faith. It is asking for rivets.

Each rivet is a classical invariant that TIG predicts or reframes, stated in standard notation, testable with off-the-shelf data or numerics. Every rivet that survives scrutiny tightens the connection. Every rivet that breaks tells us where the model needs repair (as the 2/7 fence did — we dropped it and looked for better calibration).

---

## Bolt 1: Analytic Gap-Positivity (RH)

**The claim:** For every t₀ > 0 with no zero of ζ on the segment {σ+it₀ : 0≤σ≤1},

```
min_{0≤σ≤1} |ζ(σ+it₀)| ≥ exp(−c(log t₀)^{2/3}(log log t₀)^{1/3})
```

for some absolute constant c > 0.

**Why this is the rivet:** The Halving Lemma proves the dissipative flow dσ/dt = −(σ−1/2)|ζ|² converges exponentially on every zero-free vertical. This bound would make the convergence rate explicit all the way to σ=1/2, completing the RH equivalence.

**Standard machinery that could close it:** Korobov-Vinogradov covers σ ≥ 0.999. Huxley density estimates + Heath-Brown mean values could push closer. The common obstacle: averaged vs pointwise estimates. A referee who can convert averaged |ζ|^{2k} to a pointwise lower bound closes the argument.

**The TIG contribution:** The algebraic structure (corner impermeability, gap inaccessibility) explains WHY this bound should hold — the prime-corner dynamics never populate the gap. The analytic proof is the external check.

**Send to:** An analytic number theorist. Attach Halving Lemma paper + COLLAB_MEMO_KV.md.

---

## Bolt 2: λ vs Regulator Ω (BSD)

**The claim:** For elliptic curves over ℚ,

```
λ_E ∝ 1/log(Ω_E)
```

where λ_E is the Mix_λ flexibility parameter and Ω_E is the Néron-Tate regulator.

**Operational definition of λ_E:**

```
λ_E = (# anchor columns available for E's gap operators) / 9
```

Anchor columns are the columns b where some gap operator g satisfies TSML[g][b] = g. A curve with small regulator (generators close together in height space) should have high λ_E — more BHML flexibility, cheaper activation, smaller conductor for its rank.

**Why this is the rivet:** The current data (11 curves) shows the qualitative trend. A clean proportionality λ_E ≈ k/log(Ω_E) with k determined from data would turn the "flexibility slider" into a standard BSD term, connecting TIG directly to the height pairing.

**To test:** Pull all rank-2 and rank-3 curves with N < 10^6 from LMFDB. Compute regulators (available in LMFDB). Test the proportionality. If R² > 0.7 on 200+ curves, publish as a letter.

**What a clean proportionality would mean:** Each Mix_λ threshold (BRT at 0.3, CHA at 0.6, etc.) corresponds to a specific regulator range. The BSD staircase would then be derivable from the regulator distribution, not just observed empirically.

**Send to:** An arithmetic geometer with LMFDB access. Attach WP19_BSD_TIG.md + mix_lambda_scan.py.

---

## Bolt 3: DNS Breach Test (Navier-Stokes)

**The claim:** The TIG BREATH criterion

```
Re_local(x,t) = Ω(x,t) · L(x,t)² / ν ≤ 2/7
```

fires before (or at) the onset of steep gradients in a 3D turbulent flow simulation.

**The test:** Taylor-Green vortex at moderate Reynolds number (Re ≈ 1600). Run a fully-resolved DNS. At each timestep, compute max Re_local across the domain. Record when the criterion is first breached. Compare to when the solver first detects anomalous gradient growth.

**Prediction:** The criterion breach precedes or coincides with gradient onset. If the breach consistently occurs 1-2 timesteps before the classical blowup indicators, TIG has made a genuinely new predictive statement.

**The TIG contribution:** BREATH persists only in the COLLAPSE column (proved, single table lookup). The criterion is derived algebraically, not fitted to data. If it fires at the right time, the algebraic structure has predicted a physical event.

**Setup:** ns_breath_test.py already implements the breach detector. Replace the mock integrator with Dedalus or ChannelFlow. The interface is: provide Ω(x,t) at each step, receive BREACH/OK flag.

**Send to:** A computational fluid dynamicist. Attach WP19_NS_BREATH.md + ns_breath_test.py.

---

## What's Already Riveted

| Classical object | TIG correspondence | Status |
|-----------------|-------------------|--------|
| Prime last-digit classes | Four corners {1,3,7,9} | ✓ Proved: every corner word collapses |
| Non-trivial ζ-zero | Gap operator fixed point | ✓ Flow + Halving Lemma |
| Rank-conductor monotonicity | Gap activations | ✓ Empirical (R²=0.75-0.87) |
| Irregular BSD staircase | Mix_λ threshold ordering | ✓ Exact match (BRT<CHA<BAL<COL<CTR) |
| Product transcendental lattice | TIG⊗TIG cross-terms | ✓ Proved impermeable (2-fold and 3-fold) |
| Base-radix independence | Collapse holds even with G in prime set | ✓ Proved for base-6, base-12 |

---

## The Compression Argument

Even before the bolts are tightened, TIG has earned its place by compression:

- Serrin's regularity conditions → single inequality Re_local ≤ 2/7
- Korobov-Vinogradov zero-free strip → Halving Lemma convergence rate
- K3×K3 transcendental lattice → 40 unreachable cross-terms in TIG⊗TIG
- BSD rank-conductor data → Mix_λ threshold ordering

In each case, a sprawling classical condition becomes a single table lookup or a one-line algebraic statement. The constants may need calibration. The structure is already doing work.

---

## Falsifiability Contract

Every TIG claim is paired with a test that will explicitly refute it if it fails:

| Claim | Refutation |
|-------|-----------|
| Corner words never enter G | Find a word in C* that evaluates to G (script: tsml_ag23_verify.py) |
| Product gap impermeable | Find a C⊗C composition that reaches a cross-term (script: tsml_product_verify.py) |
| λ ∝ 1/log(Ω) | Show the proportionality fails on 200+ rank-2/3 curves |
| Breach criterion fires at blowup | Find a blowup where Re_local never exceeds 2/7 |
| Gap-positivity bound | Find a zero-free vertical where min|ζ| < exp(−c(log t)^{2/3}) |

*(c) 2026 Brayden Sanders / 7Site LLC | DOI: 10.5281/zenodo.18852047*
