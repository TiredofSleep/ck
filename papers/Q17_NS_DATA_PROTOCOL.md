**© 2026 7Site LLC**
**Authors: Brayden Ross Sanders, C. A. Luther, B. Calderon, Jr.**

*Filed: 2026-04-02 | Tier B — Structural Conjecture*

# Q17 — NS Data Protocol for σ-Grammar Testing

## Purpose

The analytic questions in Q17_NS_TARGET_REFORMULATION.md are hard. Before attempting a proof, numerical experiments can determine whether the σ-grammar hypothesis is even consistent with known NS solution data. This paper specifies the exact protocol for testing the hypothesis computationally.

---

## Protocol Overview

Given a known NS solution (numerical or exact), compute the five-force coding at each timestep and test whether the resulting operator sequence exhibits σ-grammar behavior. Correlate grammar behavior with regularity indicators.

---

## Step-by-Step Protocol

### Step 1: Choose a Test Solution

Select a well-studied NS solution with known regularity properties:

- **Primary target:** Taylor-Green vortex, Re = 1600 (spectral DNS, standard benchmark, well-documented enstrophy data)
- **Secondary target:** Orszag-Tang vortex (2D case, exact statistics available)
- **Tertiary target:** Exact Beltrami solutions (ABC flows, globally smooth, useful as null-hypothesis where no blowup occurs)

The Taylor-Green vortex is preferred because it exhibits near-blowup-like enstrophy accumulation at moderate Re, providing the full range from smooth to nearly-singular behavior.

### Step 2: Compute Five-Force Components

At each timestep t_k, extract from the DNS data:

    aperture(t_k)      = ||∇·(u⊗u)||_{L²(R³)}   or suitable spectral proxy
    pressure(t_k)      = ||p||_{L²(R³)}
    depth(t_k)         = ||Δu||_{L²(R³)}   (biharmonic measure)
    binding(t_k)       = ||ω||_{L²(R³)}    (enstrophy = square of L² vorticity)
    continuity(t_k)    = ||u||_{H^{1/2}(R³)}   or helicity integral ∫ u·ω dx

These are L² norms of natural NS quantities. They are dimensionally consistent with NS scaling and can be computed directly from spectral DNS output.

**Note:** These formulas are proposals, not definitions. The assignment of CK's five force dimensions to these specific NS quantities must be justified by the D2 map structure. See Q17_NS_TARGET_REFORMULATION.md Step 1. The protocol can be run with any explicit assignment; the choice should be recorded and included in the analysis.

### Step 3: Compute D²F

Form the discrete second difference of the five-force vector:

    D²F(t_k) = F(t_k) - 2·F(t_{k-1}) + F(t_{k-2})

where F(t_k) = [aperture, pressure, depth, binding, continuity] at time t_k.

**Timestep choice:** Use τ such that t_k = kτ with τ small enough to resolve the NS dynamics but large enough that the D² signal is not dominated by numerical noise. A natural choice is τ = 10 × DNS timestep (10 coarse steps per coding step).

### Step 4: Apply the Coding Map

Compute:

    s_k = argmax_i |D²F(t_k)_i|,   i ∈ {0,1,2,3,4}

Map the argmax index to an operator in Z/10Z using the assignment:

    0 → VOID(0), 1 → LATTICE(1), 2 → COUNTER(2), ...

(Exact assignment to be specified and frozen before running the protocol.)

This produces an operator sequence {s_0, s_1, s_2, ...}.

### Step 5: Test 6-Step Near-Return

For each starting index n, compute the 6-step return distance:

    d_6(n) = distance_Z10(s_{n+6}, s_n)

where distance_Z10 is the circular distance on Z/10Z. Test:

- **Mean d_6:** Is the average near-return distance significantly smaller than random? (Random baseline: expected circular distance ≈ 2.5 on Z/10Z.)
- **Exact return rate:** What fraction of steps satisfy s_{n+6} = s_n exactly?
- **Near-return rate:** What fraction satisfy s_{n+6} = s_n or s_{n+6} ∈ {neighbors of s_n}?

**Expected finding for Beltrami (smooth, no near-blowup):** Near-return rate should be elevated if the σ-grammar hypothesis has merit.

**Expected finding for Taylor-Green at late time:** Near-return rate should decrease as enstrophy accumulates, if the coding breaks down in singular regimes (consistent with Example 3 in Q17_C2_COUNTEREXAMPLE_SEARCH.md).

### Step 6: Correlate with Regularity Indicators

Compute the following regularity indicators at each timestep:

    Enstrophy:   Z(t_k) = ∫ |ω(x,t_k)|² dx
    Palinstrophy: P(t_k) = ∫ |∇ω(x,t_k)|² dx
    L³ proxy:    ||u(t_k)||_{L³}   (if available from DNS)

Test: Does the 6-step near-return distance d_6(n) anticorrelate with enstrophy Z(t_k)?

**Hypothesis:** d_6 is small (good near-return) when Z is moderate (regular regime). d_6 is large (grammar breakdown) when Z is accumulating rapidly (near-singular regime). This would be empirical support for the σ-grammar as a regularity indicator.

### Step 7: Test Pre-Blowup Signature

Identify timesteps where enstrophy growth rate dZ/dt is maximal (the most singular-like behavior in the data). Test whether:

- The operator sequence {s_k} exits the 6-cycle {1,2,4,5,6,7} and enters anchors or VOID in these windows.
- The argmax coding becomes ill-defined or jumps erratically.
- The D² signal amplitude diverges (indicating one force component dominates).

**Expected finding:** Grammar exits precede enstrophy peaks by a few steps. If confirmed, this establishes a causal direction: grammar breakdown predicts (not just correlates with) near-singular behavior.

---

## Output and Reporting

For each test solution, report:

1. The five-force assignment formulas used (frozen before running)
2. The operator sequence {s_k} as a time series
3. Mean and distribution of d_6(n)
4. Correlation coefficient between d_6 and Z (enstrophy)
5. Timing of grammar exits relative to enstrophy peaks
6. Comparison to random baseline

---

## Significance

If Steps 5–7 show positive correlation between grammar quality and regularity, this motivates the coercive control conjecture in Q17_NS_TARGET_REFORMULATION.md and justifies further analytic work on the five-force norm inequality. If no correlation is found, the five-force assignment formulas should be reconsidered before analytic work proceeds. The protocol provides an empirical filter before expensive proof attempts.
