# Shell-Native Synthetic Benchmarks
## Three Generators for Stage 1A Testing

---

## Purpose

These three generators produce data with **known ground truth** in the TSML category. Each is built from the theorem's own primitives: modular carrier, shell partition, canonical construction, seam exceptions, optional transport companion.

The test is: **can the instrument recover the known generating structure from data?**

If yes for all three: the instrument passes Stage 1A and we can move on to ring-native tests.
If no for any: we must diagnose whether the fit algorithm, the encoding procedure, or the instrument itself is at fault.

---

## Benchmark B1: Nested Shell Collapse Generator (NSCG)

### Generative specification

**Carrier:** $R = \mathbb{Z}/10\mathbb{Z}$.

**Ground-truth attractor:** $h_{\text{true}} = 7$.

**Ground-truth shell partition:** $\sigma_{\text{true}}$ on $U(R) = \{1, 3, 7, 9\}$:
- $\sigma_{\text{true}}(1) = 2$, $\sigma_{\text{true}}(3) = 1$, $\sigma_{\text{true}}(7) = 1$, $\sigma_{\text{true}}(9) = 2$.

**Ground-truth seam:** $S_{\text{true}} = \{(1,2), (2,1), (2,4), (4,2), (2,9), (9,2), (4,8), (8,4)\}$ (8 ordered pairs).

**Ground-truth operator $T_{\text{true}}$:** exactly the Z/10Z TSML tower (C₀ + MAX on $S_{\text{MAX}}$ + ADD on $S_{\text{ADD}}$).

**Data generation:**

For each trial, sample $(x, y)$ uniformly from $R \times R$, then:
- With probability $1 - p_{\text{noise}}$: output $z = T_{\text{true}}(x, y)$.
- With probability $p_{\text{noise}}$: output $z$ uniformly random from $R$.

Collect $N$ triples $(x, y, z)$ per benchmark run.

### Parameter sweep

Run at three noise levels:
- Low: $p_{\text{noise}} = 0.05$, $N = 100{,}000$.
- Medium: $p_{\text{noise}} = 0.15$, $N = 500{,}000$.
- High: $p_{\text{noise}} = 0.30$, $N = 1{,}000{,}000$.

### Recovery task

The instrument, seeing only the triples, must recover:

1. **Attractor $\hat{h}$**: the modal $z$ output across the kernel.
   *Pass:* $\hat{h} = 7$.

2. **Shell partition $\hat{\sigma}$** on units of $R$: which partition of $\{1, 3, 7, 9\}$ into shells is consistent with the data?
   *Pass:* $\hat{\sigma}(3) = \hat{\sigma}(7)$ AND $\hat{\sigma}(1) = \hat{\sigma}(9)$ AND $\hat{\sigma}(3) \neq \hat{\sigma}(1)$ (i.e., the partition $\{\{3,7\}, \{1,9\}\}$ is recovered, labels modulo relabeling).

3. **Seam set $\hat{S}$**: pairs where canonical construction disagrees with empirical $E$.
   *Pass:* $|\hat{S} \cap S_{\text{true}}| / |S_{\text{true}}| \geq 0.90$ (recall) AND $|\hat{S} \cap S_{\text{true}}| / |\hat{S}| \geq 0.75$ (precision).

4. **Seam rule classification**: which seam entries follow MAX, which follow ADD.
   *Pass:* all seam entries correctly classified.

### Fail conditions

- Wrong $\hat{h}$.
- Shell partition not consistent with $\{\{3,7\}, \{1,9\}\}$.
- Seam recall $< 90\%$.
- At any noise level $\leq 0.15$, if total coverage of $(x, y)$ by tower $< 90\%$.

---

## Benchmark B2: Wobble-Reset Generator (WRG)

### Generative specification

**Carrier:** $R = \mathbb{Z}/n\mathbb{Z}$ for $n \in \{10, 14, 22, 34\}$ (chosen from the compatibility family).

**Attractor:** $h_n$ = the largest shell-1 element in $U(R_n)$:
- $h_{10} = 7, h_{14} = 11, h_{22} = 19, h_{34} = 31$ (to be verified during spec).

**Collapse kernel $K_c$:** the canonical construction $C_0(R_n, h_n, \sigma_n)$ where $\sigma_n$ is $v_2(3u+1)$.

**Wobble perturbation:** after generating $z = K_c(x, y)$, with probability $p_w$, replace $z$ with $z' = (z + \delta) \bmod n$ where $\delta \in \{-1, 0, +1\}$ chosen uniformly.

**Reset edges:** a pre-specified set $R_{\text{edges}}$ of pairs $(x, y)$ that force $z = h_n$ (reset to attractor) regardless of the collapse kernel. Include at least the pairs $(x, 0)$ and $(0, x)$ for $x = h_n$, plus 2-4 additional pairs for each carrier.

**Transport companion $B_{\text{true}}$:** a simple invertible operator, e.g., $B_{\text{true}}(x, y) = (x + y) \bmod n$.

**Data generation:**

For each trial, sample $(x, y)$ uniformly, then:
- Compute $z_T = K_c(x, y)$ with wobble (above).
- Compute $z_B = B_{\text{true}}(x, y)$.
- Output triple $((x, y), z_T, z_B)$.

### Parameter sweep

Run at two wobble levels for each $n$:
- Low wobble: $p_w = 0.05$.
- Medium wobble: $p_w = 0.20$.

### Recovery task

1. **Attractor recovery:** recover $\hat{h}_n$ for each carrier.
2. **Shell partition recovery:** verify that $\hat{\sigma}_n$ matches $\sigma_n$ on units.
3. **Seam/reset edges:** identify the set of pairs where $z_T$ deviates from $K_c$ systematically (i.e., resets or wobble structure).
4. **Transport recovery:** identify $B_{\text{true}}$ from $z_B$ values (simple: check if $z_B = (x+y) \bmod n$ matches at high rate).

### Pass / Fail

*Pass:* all four recoveries at rates $\geq 90\%$ for $p_w = 0.05$, $\geq 80\%$ for $p_w = 0.20$.
*Fail:* any recovery fails in the low-wobble case, OR recovery degrades to below 60% in the medium-wobble case.

---

## Benchmark B3: Layered Basin-Transport Pair (LBTP)

### Generative specification

**Carrier:** $R = \mathbb{Z}/10\mathbb{Z}$.

**Explicit T-map:** exactly the Z/10Z TSML (same as B1's $T_{\text{true}}$).

**Explicit B-map:** a commutative, invertible-over-$\mathbb{Z}$ operator on $R$. Candidate: a symmetrized multiplication table that is non-degenerate. For concreteness:
$$B_{\text{true}}(x, y) = \begin{cases} \max(x, y) & \text{if } xy \neq 0 \\ \min(x, y) & \text{if } xy = 0 \end{cases}$$

(This is illustrative; the key requirement is that $B_{\text{true}}$ is commutative, has non-zero integer determinant, and is distinct from $T_{\text{true}}$.)

**Data generation:**

Generate two streams simultaneously:
- Collapse stream: pairs $(x, y)$ with outputs from $T_{\text{true}}$.
- Transport stream: pairs $(x, y)$ with outputs from $B_{\text{true}}$.

Add 5% noise to each stream.

### Recovery task

1. Fit T-only, B-only, and paired (T, B) models to the combined data.
2. Measure prediction accuracy for each.
3. Test whether paired fit outperforms either singleton.

### Pass / Fail

*Pass:* paired (T, B) fit has prediction accuracy $> \max(\text{T-only}, \text{B-only}) + 5\text{ pp}$ on held-out pairs, AND both operators individually recovered at $\geq 90\%$.

*Fail:* paired fit is indistinguishable from the better of T-only or B-only, OR individual operator recovery is $< 80\%$ in low-noise condition.

---

## Implementation Requirements

**Each benchmark must provide:**

1. **Reference code** that generates data given a seed and parameters.
2. **Ground-truth file** stating the true $(h, \sigma, S)$ or $(T, B)$ used in generation.
3. **Fit algorithm** run against the generated data, producing $(\hat{h}, \hat{\sigma}, \hat{S})$ or $(\hat{T}, \hat{B})$.
4. **Comparison metric** computing recovery rates.
5. **Null comparisons:** run the same fit algorithm on randomized data (same $z$-marginal, shuffled pairs) and report null match rates.

**The ground-truth file is closed during fitting:** the fit algorithm must not read it. This prevents accidental overfitting to ground truth.

---

## Sequencing

1. Implement B1 first. Run at low, medium, high noise. Evaluate.
2. If B1 passes: implement B2. Run across carriers and wobble levels.
3. If B2 passes: implement B3.
4. All three passing = Stage 1A complete. Proceed to Stage 1B.
5. Any failure = diagnose and revise BEFORE proceeding.

---

## What This Suite Tests

- **B1 tests instrument fidelity:** can the instrument read back its own primitives?
- **B2 tests instrument robustness:** can it tolerate controlled perturbations while preserving structure detection?
- **B3 tests the pair concept:** is (T, B) empirically more informative than T alone?

All three use ground truth that is either the Z/10Z tower itself (B1, B3) or a natural extension to the compatibility family (B2).

---

## What This Suite Does Not Test

- Generalization beyond the compatibility family (that is Stage 1C and later).
- Real physical systems (that is Stage 3).
- Domains where shell/attractor structure is absent (that is outside instrument scope by design).

---

## Expected Outcomes

**If the instrument is correct in its stated scope:** all three benchmarks should pass at low noise. The recovery should degrade gracefully with increasing noise.

**If the instrument has hidden semantic dependencies:** B1 or B2 may fail even in low-noise settings, revealing that some recovery step depends on information not present in the data.

**If the paired concept is genuine:** B3 should show the pair (T, B) outperforming singletons. If not, "pair as invariant" becomes weaker than previously claimed.
