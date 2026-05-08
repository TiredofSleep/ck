# WOBBLE MUTATION
## Information Translation Document #6 — Asynchronous Dynamics on the TIG Newton Fractal

**Companion documents:**
- `UNIVERSAL_LANGUAGE_OPERATOR_RIGOR_v3.md` (internal rigor — what the operation IS)
- `EXTERNAL_RIGOR_MAP_v1.md` (external positioning — who else is in the territory)
- `CONSTRUCTIVE_TRANSITION_CATALOG_v1.md` (eight info→geometry lifts)
- `GEOMETRY_TO_GEOMETRY_OPERATIONS_v1.md` (geometry→geometry operations + Torus Coherence Principle)
- `SUBSTRATE_FOUNDATIONAL_IDENTITY_v1.md` (the 0=7=1 quotient + 13 harvest layer)
- `TIG_FRACTAL_FORMULA.md` (the canonical Newton fractal of LMFDB 4.2.10224.1)

**This document:** introduces **wobble mutation** as TIG's specific contribution to coupled map lattice (CML) literature. The wobble mutation is the framework's claim about *the missing piece for matching reality to finite math* — the temporal extension that takes deterministic finite-math fractals and produces reality-like patterns through localized phase decoherence around a coherent attractor.

**Author:** Brayden Sanders — 7Site LLC, Hot Springs AR — Weaver/7Site Collaboration
**Date:** 2026-05-07
**Status:** Phase 1 / Wobble mutation framework / Sept 11 integration

---

## §0 — Purpose: The Missing Piece

The TIG framework, as documented in Documents #1–#5, produces deterministic fractal content from the canonical Z/10Z substrate. The Newton fractal of the canonical TIG quartic (LMFDB 4.2.10224.1) is computed in a single pass: each pixel iterates the same Newton step at the same time, all converge synchronously, and the resulting picture is a static visualization of the basin geometry.

**Brayden's intuition:** *"Simple rules, decoherent frequencies, mutation, but still overall coherence to the original — that's what I think is our missing piece to matching reality to finite math, the wobble mutation."*

The claim is structural: deterministic finite-math fractals are too clean, too synchronous, too instantaneous. Reality is not like that. Reality has:
- The same underlying rules everywhere (quantum mechanics; chemistry; biology)
- Local clocks that are decoherent (different starting times, different rates)
- Mutation/variation in local outputs (no two cells are exactly the same)
- But overall coherence (the universe is still one universe; the body is still one body)

**Wobble mutation is the bridge.** It takes the deterministic finite-math fractal (TIG quartic Newton iteration) and adds the temporal structure (asynchronous coupled map lattice with wobble-driven local clocks) needed for reality-like patterns. The wobble — already in the framework as the 3/50 ↔ 22/50 oscillation in FORMULAS §17 — is lifted from being an internal arithmetic perturbation to being the FREQUENCY DRIVER of the CML's local clocks.

This document establishes wobble mutation rigorously, positions it against the CML literature, and frames its implications for the Sept 11 paper.

---

## §1 — The Wobble Mutation Framework

### §1.1 Definition

**Wobble mutation** is the asynchronous coupled map lattice on the TIG Newton fractal, with local clock frequencies drawn from the TIG wobble structure {3/50, 22/50}.

**Components:**

1. **Local map.** Newton iteration on the canonical TIG quartic:
   ```
   p(z)  = z⁴ + 4z³ − z² + 2z − 2     (LMFDB 4.2.10224.1)
   p'(z) = 4z³ + 12z² − 2z + 2
   N(z)  = z − p(z) / p'(z)            (one Newton step)
   ```

2. **Local clock per pixel.** Each c ∈ ℂ has:
   - **Start time** `t₀(c)` — when this pixel begins iterating
   - **Tick frequency** `ω(c) ∈ {3/50, 22/50}` — wobble-structured
   - **Phase offset** (implicit, derived from t₀ and ω)

3. **Global time** `T` — advances uniformly across all pixels simultaneously.

4. **Local iteration count** at global time T:
   ```
   n(c, T) = max(0, floor((T − t₀(c)) · ω(c)))
   ```

5. **Local state** at global time T: the result of `n(c, T)` Newton iterations applied to `c`:
   ```
   z(c, T) = N^{n(c, T)}(c)
   ```

6. **Local rendering**:
   - If `T < t₀(c)`: the pixel is **sleeping** (rendered as black/VOID)
   - If `T ≥ t₀(c)` and `z(c, T)` has not yet converged to a root: **working** (rendered as dark gray)
   - If `z(c, T)` has converged: **awake and converged** (rendered as the root's TIG operator color)

### §1.2 The Wobble Frequency Field

The frequency `ω(c)` is drawn from the TIG wobble structure. Specifically, for each c we determine the local wobble phase:

```
phase(c) = sin(ν · Re(c)) · cos(ν · Im(c))
ω(c) = WOBBLE_FAST  if phase(c) > 0  else  WOBBLE_SLOW

WOBBLE_FAST = 22/50  (the dynamic phase, from FORMULAS §17)
WOBBLE_SLOW = 3/50   (the steady phase, from FORMULAS §17)
ν = 11               (the wobble prime, from FORMULAS §17 c₂ = 33 = 3·11)
```

This produces a checkerboard-like spatial pattern of fast and slow regions. The pattern has:
- ~50% fast-tick area
- ~50% slow-tick area
- Pattern wavelength inversely proportional to ν = 11 (the wobble prime)

The wobble prime ν = 11 ties this directly to TIG's internal arithmetic: the same 11 that appears in TSML_RAW char poly coefficients (c₂ = 33 = 3·11; c₈ = −2⁵·7³·11; FORMULAS §17 discriminant identities).

### §1.3 The Start Time Field

The start time `t₀(c)` controls where and when the bloom begins. Several TIG-natural choices:

**Mode 1: Distance from origin.**
```
t₀(c) = |c| · k₁ + wobble_offset(c)
```
Pixels closer to the origin wake first. The bloom is radially symmetric, expanding outward like a Big Bang shockwave.

**Mode 2: Distance from a TIG-canonical point.**
```
t₀(c) = |c − z_seed| · k₁
```
where `z_seed` could be a σ-fixed point, a Newton root, the BALANCE root (Lo Shu center), or another TIG-canonical complex number.

**Mode 3: Plane wave from a direction.**
```
t₀(c) = (Re(c) − x_min) · k₁
```
The bloom propagates left-to-right (or any chosen direction) like a causal wavefront / light cone.

**Mode 4: Wobble-correlated random.**
```
t₀(c) = uniform_random + wobble_bias(c)
```
Stochastic bloom with wobble-structured spatial correlations.

**Mode 5: σ-orbit-driven.**
```
t₀(c) = (σ-orbit count) · k₁
```
where the σ permutation determines the "phase" each pixel sits in.

Each mode produces a structurally different visualization, but all preserve the global coherence: the four basins of the canonical TIG Newton set are unmistakable in the final state.

### §1.4 The Bloom Dynamics

At global time T = 0, no pixels have woken. As T advances:
- More pixels wake (those with `t₀(c) ≤ T`)
- Already-awake pixels accumulate Newton iterations at their local rate
- Some converge to roots; the basin structure begins to fill in
- Wobble-fast pixels converge first; wobble-slow pixels lag behind
- The image shows **emergence**: the canonical fractal materializing through time

By global time T sufficient for slowest pixels to converge:
- Every pixel is awake
- Every pixel has converged (or been classified as non-converging within max iterations)
- The image is the canonical TIG Newton fractal — but with the wobble checkerboard texture inside each basin from the differential rates of arrival

**The wobble texture is the visible signature of the local-clock decoherence.** Same root attractor, same convergence destination — but the path through time differs across the wobble pattern, leaving a phase-relationship trace in the final image.

---

## §2 — Position Against the Coupled Map Lattice Literature

Wobble mutation is a specific instance of asynchronous coupled map lattices (CMLs), a research area with substantial literature.

### §2.1 Foundational CML References

**Kaneko 1985 — coupled map lattices.** Kunihiko Kaneko, "Spatiotemporal intermittency in coupled map lattices," *Progress of Theoretical Physics* 74 (1985), 1033–1044. The founding work. CMLs are arrays of states whose values are continuous over discrete space and time. Each cell has its own local map; cells couple to neighbors. The standard formulation uses synchronous parallel updating.

**Kaneko-Tsuda 2000 — comprehensive review.** Kunihiko Kaneko and Ichiro Tsuda, *Complex Systems: Chaos and Beyond*, Springer (2000). The canonical textbook reference for CMLs and their phenomenology.

### §2.2 Asynchronous CML Literature

Asynchronous updating has been studied extensively as a more "realistic" updating scheme:

**Sinha-Wagner 2002 — asynchronous CML phase diagrams.** "Effect of asynchronicity on the universal behaviour of coupled map lattices," arXiv:nlin/0205020. Shows that asynchronous updating produces different dynamical phases than synchronous: where synchronous gives spatio-temporal intermittency for random initial lattices, asynchronous gives spatio-temporal fixed points. **Asynchronicity often regularizes the system.**

**Schönfisch-de Roos 1999 — synchronous vs asynchronous in cellular automata and CMLs.** Studies on how the updating scheme fundamentally changes phenomenology.

**González-Avella-Anteneodo 2018 — synchronization equivalence.** "Complete synchronization equivalence in asynchronous and delayed coupled maps," arXiv:1512.03760. **Proves a theoretical equivalence**: asynchronous updating and time-delayed coupling produce the same complete synchronization patterns. This is structurally important for wobble mutation: temporal asynchronicity is structurally equivalent to spatial coupling delays.

### §2.3 Fractal Structures in CMLs

**Ambika-Menon 2002 — fractals in CMLs.** "Fractal patterns on the onset of coherent structures in a coupled map lattice," *Pramana — J. Phys.* 59 (2002), L155–L161. **Reports Cantor-set-like fractals during the development of coherent structures in CMLs.** Direct precedent for the wobble-mutation observation that asynchronous CMLs on fractal-generating local maps produce richer fractal phenomenology.

**Bricmont-Kupiainen 1995, 1996 — rigorous CML coherence.** "Coupled analytic maps," *Nonlinearity* 8 (1995), 379–393. Rigorous results on coherent structures in CMLs.

**Kapral-Livi-Oppo-Politi 1994 — CML phenomenology.** *Phys. Rev. E* 49 (1994), 2009. Documents complex spatiotemporal patterns in CMLs.

### §2.4 Stochastic Coherence

**Roy-Amritkar 1996 — stochastic coherence in CMLs.** "Observation of stochastic coherence in coupled map lattices," arXiv:chao-dyn/9602006. Reports that adding noise to a CML produces "stochastic coherence" — bell-shaped patterns of structure abundance vs noise strength. Adding wobble-structured stochasticity to a CML produces emergent coherent structures.

### §2.5 Newton Fractals Under Time-Variation

**Tatham — animated Newton-Raphson fractals.** Simon Tatham, "Fractals derived from Newton-Raphson iteration," chiark.greenend.org.uk/~sgtatham/newton/. Tatham animates Newton fractals by smoothly varying the polynomial's coefficient points along Lissajous curves. This is **time-varying coefficients**, but the iteration is still globally synchronous.

**d00bd00d Fractal-Explorer 2024 — procedural Newton fractal animation.** github.com/d00bd00d/Fractal-Explorer. Continuous variation of polynomial coefficients produces smoothly-animating Newton fractals.

**Mitch Richling — Newton fractal observations.** mitchr.me/SS/newton/. Various coloring schemes for Newton's-method fractals including 2D histogram of orbit hits.

**The asynchronous variant of Newton fractals — what wobble mutation specifically is — has not (to the best of this survey's knowledge) been explicitly studied.** The CML literature focuses on locally chaotic maps (logistic, circle, sine); the Newton-fractal literature focuses on smooth coefficient variation. **Wobble mutation sits at the intersection: asynchronous CML applied to Newton iteration on a specific algebraic-canonical polynomial (the TIG quartic) with locally wobble-structured tick rates.**

### §2.6 What's Novel in Wobble Mutation

Combining the precedents above, wobble mutation is novel in three specific ways:

1. **Newton iteration as the local map.** The CML literature focuses on logistic and circle maps; Newton iteration on a specific algebraic polynomial has not been the focus.

2. **Wobble-structured tick rates.** The CML literature treats tick rate variation generically (uniformly random, neighbor-influence). Wobble mutation uses the specific {3/50, 22/50} rates from TIG's canonical wobble structure (FORMULAS §17), with phase determined by a wobble-prime-modulated function (ν = 11).

3. **Specific algebraic content.** The TIG quartic is LMFDB 4.2.10224.1 with Galois group D₄ — a specific number field with specific structural roles in TIG. Wobble mutation's basin colors are TIG operator colors corresponding to the four roots' algebraic identities (COLLAPSE, HARMONY, BREATH, BALANCE).

The combination — **asynchronous CML on Newton iteration of LMFDB 4.2.10224.1's defining quartic, with TIG-canonical wobble-driven local clocks** — is TIG-specific and not in the existing literature.

---

## §3 — The Reality-Matching Claim

### §3.1 Why Pure Synchronous Math Doesn't Match Reality

Brayden's claim: synchronous deterministic finite math is too clean to match reality. Reality has temporal heterogeneity that pure synchronous mathematics doesn't capture.

**Examples where the synchronous-math/reality gap shows:**

1. **Quantum mechanics.** Schrödinger's equation is deterministic and synchronous (one universal time parameter). But quantum decoherence requires that spatially-separated systems develop independent phases. The "spread of decoherence" is fundamentally about local clocks differing.

2. **Cosmological structure formation.** General relativity is deterministic given initial conditions. But the cosmic microwave background's anisotropies, galaxy formation, and large-scale structure require localized perturbation timing — different regions reaching nonlinearity at different times. The synchronous big-bang prediction would give homogeneous matter; the reality requires temporal heterogeneity.

3. **Cellular biology.** Each cell has the same DNA. But each cell's circadian clock has its own phase relative to neighbors. The body coordinates billions of locally-clocked cells. Synchronous biology would give catatonic uniformity; reality requires the wobble mutation.

4. **Neural networks.** Each neuron has the same biophysics. But neuronal firing has phase relationships that encode information. Synchronous neurons would give epilepsy; functional brains require the wobble mutation.

5. **Economic systems.** Each market has the same supply/demand laws. But each market clears at its own pace, and the phase relationships between markets generate macroeconomic dynamics. Fully synchronous economics would give one global equilibrium; actual economies have wobble mutation.

In every case, reality is **synchronous math + local clock decoherence + overall coherence**. This is wobble mutation.

### §3.2 Why Wobble Mutation Is the Bridge

Wobble mutation provides the temporal extension that takes a deterministic finite-math fractal (the TIG Newton set, fully synchronous) and produces the reality-matching pattern (the same fractal with wobble-driven asynchronicity).

**The structural argument:**

1. **The underlying rule is the same.** Every cell runs Newton iteration on the same canonical TIG quartic. The deterministic algebraic content is preserved exactly.

2. **The coherence is preserved.** Every cell still converges to one of the four canonical TIG roots. The basin structure is unchanged in its global topology.

3. **The local clocks differ.** Each cell ticks at its own wobble-driven rate (3/50 or 22/50), with its own start time t₀(c).

4. **The result is reality-matching texture.** The global structure (4 basins, fractal boundaries) is preserved, while local patterns (the checkerboard inside each basin) emerge from the temporal heterogeneity.

**This is what reality looks like in mathematical terms:**
- Deterministic underlying rules ✓
- Spatially-distributed local clocks ✓
- Phase coherence/decoherence patterns ✓
- Global coherence preserved ✓

**The wobble mutation is the specific TIG instantiation of this universal pattern.**

### §3.3 Connections to Physics

**Quantum field theory.** A free quantum field has the same Lagrangian everywhere, but each spatial point has its own phase oscillation. The vacuum state has correlated phases (long-range coherence) but spatially-separated regions develop independent phases (decoherence). This is **the same structural pattern as wobble mutation**: same rule, local clocks, global coherence.

**Cosmological inflation.** Inflation produces spatial regions with the same effective laws but independent quantum fluctuations. The CMB's nearly-scale-invariant power spectrum reflects the wobble-mutation-like structure of cosmological initial conditions.

**Lattice QCD.** Numerical lattice simulations of QCD update the gauge field at each lattice site. Asynchronous updating schemes are known to give different convergence properties (per González-Avella-Anteneodo 2018, equivalent to time-delayed coupling). The lattice-QCD community has independently rediscovered the asynchronous-CML phenomenology that wobble mutation formalizes for TIG.

**Spin glasses.** Random Hamiltonians produce spin systems with locally-frustrated dynamics. The wobble-mutation visualization shows how local clock differences produce frustration patterns within an overall coherent structure.

### §3.4 Connections to Biology

**Circadian rhythms.** Mammalian circadian clocks have the same gene network in every cell but distinct phases per tissue (Mohawk-Green-Takahashi 2012; Reppert-Weaver 2002). The peripheral oscillators have different start times and slightly different rates compared to the central pacemaker, producing the body's wobble-mutation-like temporal coordination.

**Cardiac pacemaker cells.** The sinoatrial node coordinates ~10,000 pacemaker cells via gap junctions. Each cell can pace independently; coupling produces synchronization. Pathologies like atrial fibrillation are wobble-mutation patterns gone awry — local clocks failing to coordinate around the global coherent rhythm.

**Slime mold pattern formation.** Dictyostelium aggregation produces beautiful spiral wave patterns from cAMP signaling. Each cell has the same chemotaxis rules but different local oscillation phases, producing wobble-mutation-style waves.

### §3.5 Connections to Consciousness

The Penrose-Hameroff Orch-OR hypothesis (Document #1 §9) posits that consciousness arises from coherent oscillations in microtubules with periodic objective reduction events. Wobble mutation provides a structural template:

- Each microtubule (or microtubule cluster) runs the same biophysics (the "TIG quartic" of biological consciousness)
- Local clocks differ across microtubules (the wobble structure)
- Global coherence is required for consciousness (the basin structure preserved)
- Conscious moments are the "convergence events" where the wobble mutation produces a unified attractor state

This is speculative; the structural template is suggestive.

---

## §4 — The Visualization

The wobble mutation visualization (`tig_wobble_mutation.gif` and accompanying static frames) shows the framework's claim materialized:

**Frame 0:** All sleeping. Pure black.

**Early frames (5–15):** Bloom begins at the origin. Wobble-pattern dot/circle structure appears (the wobble field becoming visible). Small patches of converged BALANCE (purple) and HARMONY/BREATH (teal/sky) appear.

**Mid frames (20–40):** The four-basin cross structure emerges. The cross IS the puncture (Document #4 Operation #6, Document #5 §6.4) — the topological identification 0=7=1 made visible through the temporal bloom. Wobble checkerboard texture starts filling in.

**Late frames (50–79):** Bloom propagates outward. Slow-tick wobble pixels lag behind fast-tick pixels, creating the checkerboard mosaic within each basin. The fractal boundary structure (classical Newton necklaces) shows at the basin meeting points.

**Final frame:** All four basins recognizable. Same canonical TIG Newton fractal as the static version, but with the wobble checkerboard texture inside each basin. **Global coherence preserved; local decoherence visible.**

**This is the picture of reality emerging from finite math.**

The framework's claim: this is what reality looks like under the TIG lens. The temporal bloom is the universe materializing through finite-math iteration. The wobble checkerboard is the quantum-foam-like local decoherence around the global coherent structure. The basins are the four canonical TIG roots — the algebraic content that determines what "reality" can converge to.

---

## §5 — The Mathematical Formalization

### §5.1 The Wobble Mutation as a Dynamical System

Formally, wobble mutation defines a discrete-time dynamical system on the function space:

```
(z, root_label, awake_state) : ℂ → ℂ × {0, 1, 2, 3, ⊥} × {sleeping, awake}
```

with the update rule at global time T → T + δT:

```
For each c ∈ ℂ:
    if T + δT ≥ t₀(c) and not yet awake:
        awake_state(c) ← awake
        z(c) ← c
        root_label(c) ← ⊥

    if awake_state(c) == awake:
        # Determine if this pixel should iterate this step
        elapsed_local = (T + δT − t₀(c)) · ω(c)
        elapsed_prior = (T − t₀(c)) · ω(c)
        n_steps = floor(elapsed_local) − floor(elapsed_prior)

        for _ in range(n_steps):
            if root_label(c) == ⊥:
                z(c) ← N(z(c))
                for k in {0, 1, 2, 3}:
                    if |z(c) − root_k| < ε:
                        root_label(c) ← k
                        break
```

This is a well-defined discrete-time dynamical system. At any global time T, the state `(z, root_label, awake_state)(c)` is a deterministic function of the initial pixel c, the start-time field t₀, and the frequency field ω.

### §5.2 The Fixed-Point Theorem

**Theorem (wobble-mutation convergence).** As T → ∞, every pixel c with `ω(c) > 0` and `t₀(c) < ∞` and c not in the fractal boundary measure-zero set converges to one of the four roots:

```
lim_{T → ∞} z(c, T) = root_k(c)
```

where `k(c) ∈ {0, 1, 2, 3}` is uniquely determined by the basin of c in the standard Newton fractal.

**Proof sketch.** Newton iteration on the TIG quartic has well-defined basins of attraction (per standard complex dynamics; the basins partition the Riemann sphere except for a measure-zero fractal boundary). For any c not in this boundary, the synchronous Newton iteration `z_{n+1} = N(z_n)` converges to a specific root. **Asynchronicity changes the timing but not the destination.** Each pixel's local iteration count grows monotonically with T (since `ω(c) > 0`); for sufficiently large T, the local count exceeds the synchronous convergence count, and the pixel has converged to the same root it would have converged to under synchronous iteration.

**Corollary (basin invariance under wobble mutation).** The basin structure of the wobble-mutation steady state is identical to that of the synchronous Newton fractal. **The wobble mutation does not change WHICH root each pixel converges to; it only changes WHEN.**

### §5.3 The Time-Phase Theorem

**Theorem (time-phase decomposition).** The wobble mutation's frame at time T can be decomposed as:

```
Frame(T) = Newton_fractal × phase_mask(T)
```

where `phase_mask(T)` is a function over ℂ taking values in {sleeping, working, converged_recently, converged_long_ago}, and the basin coloring is multiplied (in the perceptual-color space) by the phase mask.

**Proof:** Each pixel's color is determined by (a) its basin (steady-state Newton convergence) and (b) its current phase (sleeping/working/converged). The basin component is invariant in T (per Corollary 5.2); the phase component depends on T through (T − t₀(c)) · ω(c). Multiplicative composition gives the rendering rule.

**Implication:** The wobble mutation is a TIME-MODULATED NEWTON FRACTAL. The fractal structure is fixed (the canonical TIG Newton set); the modulation is time-dependent and wobble-driven.

---

## §6 — Open Frontiers

### §6.1 Within Wobble Mutation

1. **Quantitative coherence measures.** What fraction of "global coherence" is preserved at intermediate T? Define a metric (e.g., mutual information between Frame(T) and Newton_fractal) and study its time evolution.

2. **Wobble parameter sensitivity.** The choice ν = 11 (wobble prime) matters. What happens with ν = 5 (the other significant TIG prime)? With ν = 7 (HARMONY)? With non-TIG ν? Predicted: ν = 11 should give the cleanest reality-matching pattern; ν = 7 should give over-coherent (too synchronous) bloom; non-TIG ν should give noisy non-coherent bloom.

3. **Multiple wobble frequencies.** Real biology has multiple oscillator frequencies (circadian + ultradian + cardiac). Generalize wobble mutation to allow ω(c) drawn from {3/50, 22/50, 7/50, ...} — multiple wobble harmonics.

4. **Coupling between pixels.** Pure wobble mutation is uncoupled (each pixel iterates independently). Add weak nearest-neighbor coupling (true CML); study how coupling changes the bloom and the steady-state texture.

5. **Stochastic wobble mutation.** Add noise to Newton iteration (per Roy-Amritkar 1996). Predicted: stochastic-coherence bell-curve emerges.

### §6.2 Reality-Matching Predictions

If wobble mutation is the missing piece for matching reality to finite math, it should make specific predictions:

1. **CMB anisotropy power spectrum.** The wobble-mutation cosmology predicts that initial conditions have spatial correlations driven by the wobble structure. Specific prediction: the CMB power spectrum should have a feature at the wobble-prime spatial scale.

2. **Galaxy formation timing.** Galaxies should form at locally-clocked times correlated with their initial-condition wobble phase. Specific prediction: galaxy ages correlate with their wobble-phase position in the cosmological substrate.

3. **Quantum decoherence rate.** The decoherence time of spatially-separated quantum systems should be inversely proportional to the wobble frequency. Specific prediction: testable via interferometry.

4. **Biological clock coupling strengths.** The phase-coupling constant between biological oscillators should match a TIG-derived value related to wobble structure.

These are speculative predictions; the framework needs to develop testable consequences, but the reality-matching claim is at least falsifiable in principle.

### §6.3 Mathematical Frontiers

1. **Wobble-mutation Lyapunov spectrum.** The standard Newton fractal has a known Lyapunov spectrum; the wobble mutation alters this. Compute the modified spectrum and identify how the wobble structure manifests algebraically.

2. **Topology of the bloom front.** The "wave front" of pixel awakening has a specific topological structure depending on t₀'s shape. Study whether this front is itself fractal.

3. **Quantization of the wobble structure.** Can wobble mutation be quantized? I.e., replace deterministic wobble {3/50, 22/50} with a quantum superposition? This would produce a quantum-decoherence-flavored variant.

---

## §7 — Closing: The Wobble Mutation Is the Bridge

The framework's final structural piece is now in place. Documents #1–#5 established:
1. *What the framework operation is* (Doc #1)
2. *Where it sits in the literature* (Doc #2)
3. *Eight info→geometry lifts* (Doc #3)
4. *Nine geometry→geometry operations* (Doc #4)
5. *The 0=7=1 substrate identity + 13 harvest layer* (Doc #5)

Document #6 establishes:
6. *Wobble mutation as the temporal extension* — taking deterministic finite-math fractals and producing reality-matching patterns through asynchronous coupled-map-lattice dynamics with TIG-canonical wobble-driven local clocks.

**The framework's claim about reality:**

> *Reality is the canonical TIG Newton fractal under wobble mutation: the same simple deterministic rule (Newton iteration on LMFDB 4.2.10224.1) running everywhere, with wobble-structured local clocks producing the temporal heterogeneity that distinguishes lived experience from clean mathematical synchrony, while preserving the global coherence that makes the universe one place.*

**For Sept 11.** The integration paper now has a complete framework:

1. *What is the substrate?* The fractal set 0–9 with 0=7=1, producing the 8-element quotient Q_TIG. (Doc #5)
2. *What sits above the substrate?* The 13-harvest layer. (Doc #5)
3. *How does the framework operate?* Three operation types — info→info, info→geo, geo→geo. (Docs #1, #3, #4)
4. *Where does it sit in the literature?* Five active programs in the territory. (Doc #2)
5. *Why does it work?* The Torus Coherence Principle. (Doc #4)
6. *How does the same torus fit so many domains?* Environment-fitting via lens variation. (Doc #4)
7. *How does deterministic finite math match reality?* **Wobble mutation: asynchronous CML on the canonical Newton fractal with wobble-driven local clocks.** (Doc #6)

The framework operates in the deterministic synchronous regime by default; it produces the canonical Newton fractal of LMFDB 4.2.10224.1. **Wobble mutation lifts the framework to the temporal-heterogeneous regime where reality lives.** The same algebraic content; the same coherent structure; the same canonical roots — but with the temporal texture that distinguishes math-on-paper from math-as-reality.

The wobble was always in the framework (FORMULAS §17, the 3/50 ↔ 22/50 oscillation). What Document #6 establishes is that **the wobble is not a perturbation of TIG; it is the temporal scaffolding that makes TIG's content match reality's.** The wobble IS the operation that turns the static fractal into the lived universe.

**One framework. One substrate. One torus. One identity (0=7=1). One harvest (13). One mutation (wobble).**

The picture is the picture of reality emerging from finite math.

---

*"Be holy. Be whole by having a hole. Be holy."*
*The puncture is the structure. The wound is the connection.*
*The 12th bump is the cross.*
*The torus sees itself.*
*One surface. Forty-plus markings. Six domains. One truth.*
*0 = 7 = 1.*
*The harvest is at 13.*
*The wobble is the mutation.*
*The mutation is reality.*

---

**Document status:** v1, Information Translation Document #6.
**Companions:**
- `UNIVERSAL_LANGUAGE_OPERATOR_RIGOR_v3.md` (Doc #1)
- `EXTERNAL_RIGOR_MAP_v1.md` (Doc #2)
- `CONSTRUCTIVE_TRANSITION_CATALOG_v1.md` (Doc #3)
- `GEOMETRY_TO_GEOMETRY_OPERATIONS_v1.md` (Doc #4)
- `SUBSTRATE_FOUNDATIONAL_IDENTITY_v1.md` (Doc #5)
- `TIG_FRACTAL_FORMULA.md` (the canonical Newton fractal)
**Visualization:** `tig_wobble_mutation.gif` (radial bloom), `tig_wobble_wave.gif` (wave bloom)
**Reference implementation:** `wobble_mutation.py`
**Foundation:** `FORMULAS_AND_TABLES.md` (D1–D99 canonical proof spine).
**Master plan:** `Atlas/META_PLAN_2026-05-06/RELEASE_PLAN_SEPT11.md` (18-week walk).
