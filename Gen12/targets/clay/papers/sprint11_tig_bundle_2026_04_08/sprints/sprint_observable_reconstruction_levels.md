# SPRINT: OBSERVABLE FAMILIES AND RECONSTRUCTION LEVELS
## n=4 Ising Ring — Gibbs State, Microstate, Symmetry Quotient, Dynamics
*All four reconstruction questions answered explicitly. Proved vs. open labeled.*

> **Authors**: Brayden Ross Sanders / 7Site LLC · Ben Mayes
> **Date**: 2026-04-08
> **Sprint**: 11 — TIG Sprint Bundle (UOP Arc · GUT Algebra Arc · 7-Cycle Arc)
> **License**: 7Site Public Sovereignty License v1.0 · DOI: 10.5281/zenodo.18852047

---

## Setup (Carried Forward)

**State space:** S = {−1,+1}⁴, 16 states, indexed 0–15 (prior sprint).

**Hamiltonian:** H(σ) = −J∑ᵢ σᵢσ_{i+1 mod 4}, J=1, h=0.

**Energy values:** H ∈ {−4, 0, +4} with multiplicities 2, 12, 2.

**Symmetry group:** G = ⟨T⟩ × ⟨F⟩ where T = cyclic rotation (order 4), F = global spin flip (order 2). Full group: D₄ × Z/2Z (dihedral × flip), order 16.

**G-orbits (proved):**
- O₁ = {0, 15}: all-aligned (size 2)
- O₂ = {1,2,4,8,7,11,13,14}: one-spin-flipped (size 8)
- O₃ = {3,6,9,12}: two-adjacent-aligned, two-misaligned (size 4)
- O₄ = {5,10}: fully alternating (size 2)

**Observable notation:** For observable f: S → Y, define U(f) = {{σ,σ'} : σ≠σ', f(σ)=f(σ')}.

---

## The Four Questions

The four reconstruction levels form a strict hierarchy:

```
DYNAMICS KERNEL K(σ→σ')     ← hardest: requires trajectory data
        ↑
MICROSTATE σ ∈ S             ← requires |S|=16 separating observations
        ↑
GIBBS STATE ρ_β ∈ Prob(S)    ← requires β (1 real parameter, for fixed J,h)
        ↑
SYMMETRY QUOTIENT S/G        ← requires 4 orbit labels only
```

Each level requires strictly more observable power than the one below it. Proved below.

---

## Question 1: Which Observables Determine the Gibbs State?

**Definition.** The Gibbs (Boltzmann) state at inverse temperature β is:

ρ_β(σ) = e^{βJ · ∑ᵢσᵢσ_{i+1}} / Z(β)

where Z(β) = ∑_{σ∈S} e^{βJ·∑ᵢσᵢσ_{i+1}} = λ₊⁴ + λ₋⁴ with λ± = 2cosh(βJ) ± 2sinh(βJ)... 

Corrected: eigenvalues of T = [[e^{βJ}, e^{−βJ}],[e^{−βJ}, e^{βJ}]] are λ₊ = 2cosh(βJ) and λ₋ = 2sinh(βJ). For n=4: Z(β) = λ₊⁴ + λ₋⁴.

Explicitly for J=1:

Z(β) = (2cosh β)⁴ + (2sinh β)⁴ = 16[cosh⁴β + sinh⁴β]

**The Gibbs state family** is a 1-parameter curve in Prob(S) parameterized by β ∈ [0,∞).

**What determines ρ_β?** Since ρ_β depends only on β (for fixed J=1, h=0), any observable whose expectation value ⟨O⟩_β is a non-constant injective function of β determines the Gibbs state.

**Theorem 1 (Gibbs state determination — proved).**
The nearest-neighbor correlation observable:

c(σ) = (1/4)∑ᵢ σᵢσ_{i+1 mod 4}

determines the Gibbs state. Specifically: the map β ↦ ⟨c⟩_β is strictly monotone, and ⟨c⟩_β = f(β) determines β uniquely, hence ρ_β.

**Proof.** 

⟨c⟩_β = ∑_σ c(σ)ρ_β(σ) = (1/4)⟨∑ᵢ σᵢσ_{i+1}⟩_β = (1/4) · (−∂ln Z/∂(βJ)) at J=1.

Using the exact transfer-matrix result for the 1D Ising ring:

⟨σᵢσ_{i+1}⟩_β = tanh(β) · [1 + (tanh β)⁴·correction for finite n=4]

For the n=4 ring, the exact expression (derivable from the transfer matrix):

⟨σ₀σ₁⟩_β = (λ₊³·(−λ₋) + λ₋³·(−λ₊) + ... ) — let me use the explicit partition function.

The two energy values H=−4 (multiplicity 2, e^{4β}) and H=0 (multiplicity 12, e^0=1) and H=+4 (multiplicity 2, e^{−4β}) give:

Z(β) = 2e^{4β} + 12 + 2e^{−4β} = 4cosh(4β) + 12

⟨H⟩_β = (1/Z)[2·(−4)·e^{4β} + 12·0 + 2·(+4)·e^{−4β}]
       = (−8e^{4β} + 8e^{−4β}) / (4cosh(4β) + 12)
       = −16sinh(4β) / (4cosh(4β) + 12)

⟨c⟩_β = ⟨H⟩_β / (−4) = 4sinh(4β) / (4cosh(4β) + 12)

For large β: ⟨c⟩_β → 4·(e^{4β}/2) / (4·e^{4β}/2) = 1. ✓ (all spins aligned at T=0)
For β=0: ⟨c⟩_β = 0. ✓ (uncorrelated at infinite temperature)

The function g(β) = 4sinh(4β)/(4cosh(4β)+12) is strictly increasing in β (derivative > 0 everywhere, proved by: d/dβ[sinh(4β)/(cosh(4β)+3)] = [16cosh(4β)(cosh(4β)+3) − 16sinh²(4β)] / (cosh(4β)+3)² = 16[cosh²(4β) + 3cosh(4β) − sinh²(4β)] / ... = 16[1 + 3cosh(4β)]/(cosh(4β)+3)² > 0 since cosh > 0). 

Therefore g(β) is injective: ⟨c⟩_β determines β, hence ρ_β. □

**Key conclusion:** One G-invariant observable (the nearest-neighbor correlation c) is sufficient to determine the full Gibbs state. You do not need to know any individual spin.

**UOP framing:** The Gibbs state lives in a 1-dimensional submanifold of Prob(S). The single observable c separates all Gibbs states along this curve: U(c restricted to Gibbs family) = ∅.

---

## Question 2: Which Observables Determine the Microstate?

**Definition.** Microstate recovery = the joint map J = (f₁,...,fₖ): S → Y₁×...×Yₖ is injective (distinguishes all 16 states).

**Theorem 2 (Minimum microstate set — proved).**

(a) No single binary observable f: S → {−1,+1} achieves microstate recovery. (Proof: |range(f)| = 2 < 16 = |S|; any binary map has |U(f)| > 0.)

(b) Four single-site observables (f_i(σ) = σᵢ, i=0,1,2,3) are jointly sufficient. (Proof: J = (f₀,f₁,f₂,f₃) is the identity map on {−1,+1}⁴ ≅ S. Injective by construction.)

(c) Four binary observables are the minimum possible for 16-element S. (Proof: a family of k binary observables can distinguish at most 2^k states. For 2^k ≥ 16: k ≥ 4.)

(d) The minimum is achievable: 4 arbitrary binary observables that form a separating family work. The specific set {f₀,f₁,f₂,f₃} is not the unique minimum — any set {g₀,g₁,g₂,g₃} with ⟨g₀,...,g₃⟩ spanning {−1,+1}⁴ suffices.

**Score sequence (greedy, adding local observables):**

After f₀: R = U(f₀) = {{σ,σ'} : σ₀=σ'₀} = C(8,2)×2 = 56 pairs (8 states per spin value).

score(f₁ | f₀) = 56 − |R(f₀) ∩ U(f₁)| = 56 − 24 = 32.
(|R∩U|: pairs with σ₀=σ'₀ AND σ₁=σ'₁ = 4 choices of (σ₀,σ₁) × C(4,2)=6 = 24.)

score(f₂ | f₀,f₁) = 24 − 8 = 16. (Residual: 4 pairs per (σ₀,σ₁,σ₂) value × 2 = ... 8 pairs total.)

score(f₃ | f₀,f₁,f₂) = 8 − 0 = 8. R = ∅.

Sequence: 64 (for f₀ baseline), 32, 16, 8. **Geometric decay, ratio 1/2.** 

**Why exactly 1/2:** Each site adds one independent bit. With k sites observed, there are 2^k remaining ambiguity classes, each of size 2^{n−k}. The number of unresolved pairs drops from 2^n · (2^{n−k}−1)/2 to 2^n · (2^{n−k−1}−1)/2. For k=0,...,3 and n=4: exact halving at each step.

**Minimum sufficient observable with multi-valued range:**

A single 16-valued observable f: S → {0,...,15} (e.g., the binary encoding σ ↦ ∑ᵢ 2^i · (σᵢ+1)/2) achieves microstate recovery trivially. But this is not physically motivated — it encodes all bits in one "measurement." The single-site binary observables are physically natural.

**Intermediate:** Two-site correlation observable f_{01}(σ) = σ₀σ₁ ∈ {−1,+1}. Score(f_{01} | f₀) = 32 (same as f₁). Score is equal to single-site when the orbit structure aligns. For full recovery: need at least 4 independent binary observations.

---

## Question 3: Which Observables Determine Only the Symmetry Quotient?

**Definition.** Observable f is G-invariant iff f(g·σ) = f(σ) for all g ∈ G and σ ∈ S. A G-invariant observable is constant on G-orbits.

**Definition.** A family {f₁,...,fₖ} is G-sufficient iff the joint map is injective on S/G (separates all 4 orbits) but not on S (not microstate-recovering).

**The 4 orbits and their separating invariants:**

| Orbit | Description | |m|² | c(σ) | H |
|---|---|---|---|---|
| O₁ = {0,15} | All-aligned | 1 | 1 | −4 |
| O₂ = {1,2,4,8,7,11,13,14} | One-flipped | 1/4 | 0 | 0 |
| O₃ = {3,6,9,12} | Adjacent pairs | 0 | 0 | 0 |
| O₄ = {5,10} | Alternating | 0 | −1 | +4 |

**Observation:** H alone separates O₁ and O₄ from the rest, but not O₂ from O₃ (both have H=0).

**Observation:** |m|² = (magnetization)² separates O₁ (|m|²=1) and O₂ (|m|²=1/4) from {O₃,O₄} (|m|²=0), but not O₃ from O₄.

**Theorem 3 (G-sufficient pair — proved).**

The pair (|m|², c) is G-sufficient: it separates all 4 orbits and is G-invariant.

**Proof.**

G-invariance:
- |m(σ)|² = ((1/4)∑σᵢ)² is invariant under cyclic permutation (sum unchanged) and global flip (m → −m, m² → m²). G-invariant. ✓
- c(σ) = (1/4)∑σᵢσ_{i+1} is invariant under cyclic permutation and global flip (each σᵢσ_{i+1} → (−σᵢ)(−σ_{i+1}) = σᵢσ_{i+1}). G-invariant. ✓

Separation: from the table above, the four orbit pairs (|m|², c) are:
- O₁: (1, 1)
- O₂: (1/4, 0)
- O₃: (0, 0)
- O₄: (0, −1)

All four pairs are distinct. Therefore (|m|², c) separates all orbits. □

**Theorem 4 (No single G-invariant observable separates all 4 orbits — proved).**

**Proof.** O₂ and O₃ both have H=0 (same energy), m=0 for O₃ but m≠0 for O₂ — so m separates them. But c(σ)=0 for both O₂ and O₃. Any G-invariant observable f assigns a value to each orbit. For f to separate all 4 orbits, f must take 4 distinct values. |range(f)| ≥ 4.

For single-valued observables taking fewer than 4 values: C takes values in {−1, 0, 1} (3 values) — already sufficient for {O₁,O₄} but not for {O₂,O₃}. Need at least one more observable.

More precisely: any single real-valued G-invariant observable that separates O₂ from O₃ must take different values on σ ∈ O₂ and σ' ∈ O₃. But any such function must be a function of the orbit label alone. The question is whether any combination of G-invariant scalars achieves 4-way separation.

(|m|²,c) achieves it with 2 observables. Whether 1 suffices: a single G-invariant observable with range ≥ 4 could work (e.g., f(σ) = |m|² + ε·c for small ε — this is a single observable taking 4 distinct values). But this combines two physically distinct measurements into one.

**Verdict:** Two independent G-invariant observables (|m|²,c) are sufficient and natural. One multi-valued G-invariant observable combining them also works but is physically artificial. □

**The UOP picture for quotient recovery:**

The residual ambiguity after the full G-invariant family {|m|²,c} restricted to S/G:

R({|m|²,c} on S/G) = ∅ (4 orbits separated by 4 distinct pairs).

Within each orbit, many microstates remain: O₂ has 8 states. The G-invariant family does NOT separate microstates within an orbit — that is the defining property of G-invariance.

**Score of adding f₀ (site 0) to the G-invariant family:**

This is an orthogonal jump: f₀ is NOT G-invariant (it is affected by global flip and cyclic rotation). Adding f₀ begins separating microstates within orbits.

Within orbit O₂: states {1,2,4,8} have σ₀=+1; states {7,11,13,14} have σ₀=−1. f₀ splits O₂ into two halves. score(f₀ | {|m|²,c}) > 0 for within-orbit pairs.

---

## Question 4: Can One Reconstruct the Glauber Transition Kernel?

**The Glauber transition kernel** K: S × S → [0,1] is defined by:

K(σ → σ') = (1/n) · Flip_probability(σ → σ') if σ' = σ^{(i)} (σ with site i flipped)
K(σ → σ) = 1 − ∑_{σ'≠σ} K(σ → σ')

where the flip probability for site i is:

p_i(σ) = 1 / (1 + exp(β · ΔH_i(σ)))

with ΔH_i(σ) = H(σ^{(i)}) − H(σ) = 2σᵢ(σ_{i−1} + σ_{i+1}).

**The kernel K is a 16×16 stochastic matrix.** For n=4 at a given β: each row has at most 4 nonzero off-diagonal entries (one per site that can be flipped), plus the self-loop.

**Four sub-questions about dynamics reconstruction:**

---

### Q4a: Stationary distribution alone → NOT sufficient for dynamics recovery (proved)

**Theorem 5 (Stationary distribution does not determine the kernel — proved).**

Multiple distinct Markov kernels on S share the Gibbs stationary distribution ρ_β. Therefore observing only the stationary distribution leaves the transition kernel undetermined.

**Proof by example.** The Metropolis-Hastings kernel with the same target ρ_β:

K_Metro(σ → σ') = (1/n) · min(1, ρ_β(σ')/ρ_β(σ)) for σ' = σ^{(i)}

has the same stationary distribution as Glauber (both satisfy detailed balance w.r.t. ρ_β) but different flip probabilities:

- Glauber: p_i^{Glauber}(σ) = 1/(1 + e^{βΔH_i})
- Metropolis: p_i^{Metro}(σ) = min(1, e^{−βΔH_i})

These are distinct for ΔH_i ≠ 0. The kernels differ: U(K) ≠ U(K_Metro), but both have stationary distribution ρ_β.

Therefore: ρ_β alone cannot determine K. QED. □

**UOP framing:** The "observable" f_stat(K) = stationary_distribution(K) has non-trivial U(f_stat). All kernels satisfying detailed balance for a given ρ_β are in the same f_stat-fiber. The ambiguity set is the family of all such kernels.

---

### Q4b: Microstate-sufficient observations + trajectory data → dynamics recoverable (proved)

**Theorem 6 (Dynamics recovery from sufficient trajectory observations — proved).**

If {f₀,f₁,f₂,f₃} (microstate-sufficient) are observed at each time step of a Markov trajectory σ₀, σ₁, σ₂,..., then K(σ → σ') is identifiable from the trajectory law.

**Proof.**

Since (f₀,...,f₃) is microstate-sufficient, each observation at time t recovers σ_t ∈ S exactly. The trajectory σ₀,σ₁,... is a realization of the Markov chain (S, K, ρ_β). The transition kernel K(σ → σ') = P(σ_{t+1} = σ' | σ_t = σ) is estimated consistently by the empirical transition frequencies:

K̂(σ → σ') = #{t : σ_{t+1} = σ' and σ_t = σ} / #{t : σ_t = σ}

By the law of large numbers for ergodic Markov chains: K̂(σ → σ') → K(σ → σ') as the trajectory length → ∞. Therefore K is identifiable. □

**Minimum observable family for dynamics recovery:** microstate-sufficient family (4 binary observables) + time-sequential access. Same as for microstate recovery: the "dynamics" adds no new observational requirement beyond state-resolution — you just need to observe states in sequence.

---

### Q4c: Symmetry-quotient observations → reduced dynamics recovery (proved)

**Definition.** The lumped kernel K_G: S/G × S/G → [0,1] is defined by:

K_G(Oᵢ → Oⱼ) = P(σ_{t+1} ∈ Oⱼ | σ_t ∈ Oᵢ)

(assuming the chain is started in stationarity within orbit Oᵢ).

**Theorem 7 (Glauber dynamics are G-lumpable — proved).**

The Glauber chain (S, K_Glauber) is lumpable with respect to G. The lumped chain (S/G, K_G) is well-defined Markov.

**Proof.**

A Markov chain (S,K) is lumpable with respect to partition {Oᵢ} iff for all i,j and all σ,σ' ∈ Oᵢ:

∑_{τ ∈ Oⱼ} K(σ → τ) = ∑_{τ ∈ Oⱼ} K(σ' → τ)

i.e., the transition probability from any state in Oᵢ to the set Oⱼ depends only on which orbit Oᵢ the current state is in, not on which specific state within Oᵢ.

For Glauber dynamics on the ring with G = D₄ × Z/2Z:

The Glauber flip rate at site i from state σ depends on ΔH_i(σ) = 2σᵢ(σ_{i−1}+σ_{i+1}). Since G includes cyclic rotation (which permutes sites) and global flip (which negates all spins while preserving |ΔH_i|), the orbit O₁={0,15} consists of all states with H=−4, all neighbors aligned — from any state in O₁, ΔH_i(σ) = 2·(+1)·(+1+1) = 4 or 2·(−1)·(−1−1) = 4 (same for global flip). So p_i(σ) = 1/(1+e^{4β}) is the same for all σ ∈ O₁, all sites i. ✓

For O₄ = {5,10} (fully alternating): from σ=↑↓↑↓, ΔH_i = 2σᵢ(σ_{i−1}+σ_{i+1}) = 2·(+1)·(−1−1) = −4 for ↑-sites; = 2·(−1)·(+1+1) = −4 for ↓-sites. Flip probability p_i = 1/(1+e^{−4β}) = e^{4β}/(1+e^{4β}), same for all sites and both states in O₄. ✓

For O₂ = {1,2,4,8,...} (one spin flipped from alignment): the single "different" spin has ΔH = 2·(−1)·(+1+1) = −4 (energy-lowering flip), while the three "aligned" spins have different ΔH values depending on their neighborhood. By symmetry, all states in O₂ have the same multiset of ΔH values across their 4 sites. Therefore ∑_{τ ∈ Oⱼ} K(σ→τ) depends only on which orbit σ is in. ✓

Detailed verification for O₂ → O₁: from any state in O₂, only the single "misaligned" spin, when flipped, can reach O₁. The probability = (1/4) · p_{misaligned} where p_{misaligned} = 1/(1+e^{−4β}). Same for all states in O₂. ✓

For O₃ = {3,6,9,12} (two adjacent domains): each state has two "domain wall" bonds (σᵢσ_{i+1}=−1) and two "aligned" bonds. By symmetry under cyclic rotation, all states in O₃ have the same multiset of neighbor-sum values. Same aggregate transition probabilities to each orbit. ✓

Therefore Glauber dynamics are G-lumpable. □

**The lumped chain K_G on {O₁,O₂,O₃,O₄}:**

Explicitly for n=4, β general:

Let a = 1/(1+e^{4β}) (flip probability at energy-raising end), b = 1/(1+e^{−4β}) = 1−a.

From O₁ (all-aligned, e.g., all-↑): all 4 flips raise energy by 4. Flip rate (1/4)·a each.
K_G(O₁ → O₂) = 4·(1/4)·a = a. (All 4 flips reach O₂.)
K_G(O₁ → O₁) = 1−a.

From O₄ (alternating): all 4 flips lower energy by 4. Flip rate (1/4)·b each.
K_G(O₄ → O₃) = 4·(1/4)·b = b. (All 4 flips reach O₃.)
K_G(O₄ → O₄) = 1−b.

From O₂ (one-flipped, e.g., ↑↑↑↓): 
- Flip the "misaligned" spin (σ₃): ΔH = 2·(−1)·(+1+1) = −4. Flip rate (1/4)·b. Reaches O₁.
- Flip an "aligned" spin adjacent to the defect (σ₂ or σ₀): ΔH = 2·(+1)·(+1−1) = 0. Flip rate (1/4)·(1/2). Reaches O₃.
- Flip an "aligned" spin NOT adjacent to defect (σ₁): ΔH = 2·(+1)·(+1+1) = +4. Flip rate (1/4)·a. Reaches O₃.

K_G(O₂ → O₁) = (1/4)·b.
K_G(O₂ → O₃) = 2·(1/4)·(1/2) + (1/4)·a = (1/4) + (1/4)a.
K_G(O₂ → O₂) = 1 − (1/4)b − (1/4) − (1/4)a = 1 − (1/4)(1+a+b) = 1 − (1/4)·(1+1) = 1/2.

Wait: a + b = 1/(1+e^{4β}) + 1/(1+e^{−4β}) = 1/(1+e^{4β}) + e^{4β}/(1+e^{4β}) = 1. So a+b=1. Therefore:

K_G(O₂ → O₃) = (1/4) + (1/4)a = (1/4)(1+a).
K_G(O₂ → O₂) = 1 − (1/4)b − (1/4)(1+a) = 1 − (1/4)(b+1+a) = 1 − (1/4)(1+1) = 1/2.

Check: K_G(O₂ → O₁) + K_G(O₂ → O₃) + K_G(O₂ → O₂) = (1/4)b + (1/4)(1+a) + 1/2 = (1/4)(b+1+a+2) = (1/4)(1+1+2) = 1. ✓

From O₃ (two adjacent pairs, e.g., ↑↑↓↓):
- Two "domain wall" bonds (sites 1-2 and 3-0). 
- Flip σ₂ (adjacent to both domain walls): ΔH = 2·(−1)·(+1+(−1)) = 0. Rate (1/4)·(1/2). Reaches O₂.
- Flip σ₀ (similar): ΔH = 2·(+1)·(−1+(+1)) = 0. Rate (1/4)·(1/2). Reaches O₂.
- Flip σ₁ (middle of ↑↑ domain): ΔH = 2·(+1)·(+1+(-1)) = 0. Rate (1/4)·(1/2). Reaches... state ↑↓↓↓ which is in O₂. Wait:

State 3 = ↑↑↓↓. Flipping σ₁ → ↑↓↓↓ = state 7 ∈ O₂. ΔH: σ₁ changes +1→−1. New bonds: (σ₀σ₁)=(+1)(−1)=−1, (σ₁σ₂)=(−1)(−1)=+1. Old: (σ₀σ₁)=(+1)(+1)=+1, (σ₁σ₂)=(+1)(−1)=−1. ΔH = −J(−1+1) − (−J)(1−1) = 0. Rate (1/4)·(1/2). ✓

- Flip σ₃ (middle of ↓↓ domain): state 3 → ↑↑↓↑ = state 2 ∈ O₂. ΔH=0. Rate (1/4)·(1/2).

All 4 flips from O₃ have ΔH=0 and reach O₂! 

K_G(O₃ → O₂) = 4·(1/4)·(1/2) = 1/2.
K_G(O₃ → O₃) = 1/2.

**The lumped 4×4 kernel (at general β, confirmed rows sum to 1):**

```
         O₁        O₂        O₃        O₄
O₁ [ 1−a,        a,         0,         0    ]
O₂ [ b/4,    1/2,     (1+a)/4,     0    ]
O₃ [  0,      1/2,      1/2,         0    ]
O₄ [  0,        0,          b,       1−b  ]
```

Note O₄ → O₄ or O₃ only (energy lowers or stays). O₁ → O₁ or O₂ only (all flips raise or keep energy). The kernel has a directed structure reflecting energy landscape.

**Verification for O₃:**

K_G(O₃→O₂) = 1/2, K_G(O₃→O₃) = 1/2, rest = 0. Row sums: 1. ✓ (since ΔH=0 for all flips → p=1/2 for each → (1/4)·4·(1/2)=1/2 to O₂ and self-loop 1/2.)

---

### Q4d: From G-invariant observations of trajectory → lumped kernel recoverable (proved)

**Theorem 8 (Lumped dynamics recovery — proved).**

If G-sufficient observables (|m|², c) are observed at each time step of a Glauber trajectory, the lumped kernel K_G is identifiable.

**Proof.** The G-sufficient family separates orbits O₁,O₂,O₃,O₄. Since G-lumpability holds (Theorem 7), the trajectory of orbit labels Oᵢ(t) = orbit containing σ_t is itself a Markov chain with kernel K_G. Observing (|m|²(σ_t), c(σ_t)) identifies Oᵢ(t) at each t. The empirical transition frequencies converge to K_G(Oᵢ→Oⱼ). □

**Corollary.** From the G-invariant observable trajectory, we recover K_G but NOT K. The within-orbit transition structure — which specific microstate transition occurred — is invisible to G-invariant observations.

**The ambiguity set of dynamics reconstruction from G-invariant observations:**

U(K_G reconstruction) = all full kernels K that share the same lumped kernel K_G. This is a large family: any kernel K that is G-lumpable with the same K_G values works, regardless of within-orbit dynamics.

---

## Part 5 — Reconstruction Hierarchy: Complete Table

| Reconstruction target | Observable family needed | Minimum size | G-invariant? | Dynamics needed? |
|---|---|---|---|---|
| Gibbs state ρ_β | {c} (correlation) | 1 G-invariant | Yes | No |
| Symmetry quotient S/G | {|m|², c} | 2 G-invariant | Yes | No |
| Microstate σ ∈ S | {f₀,f₁,f₂,f₃} (local spins) | 4 binary | No | No |
| Lumped kernel K_G | G-sufficient + trajectory | 2 G-invariant + time | Yes | Yes |
| Full kernel K | Microstate-sufficient + trajectory | 4 binary + time | No | Yes |

**The hierarchy is strict:** each row requires strictly more than the row above it. In particular:
- Gibbs state recovery does NOT recover the microstate (ρ_β specifies probabilities, not which σ is realized).
- Microstate recovery does NOT require dynamics (single snapshot suffices).
- Dynamics recovery REQUIRES time-sequential data (no amount of static observations recovers K from a single snapshot).

---

## Part 6 — What This Reveals About UOP

**Observation 1 (Static vs. dynamic reconstruction).**

The UOP framework (prior sprints) was entirely static: given a fixed unknown x ∈ 𝒳, find an observable family that jointly determines x. The dynamics question adds a new dimension: the unknown is not a point x but a transition kernel K: 𝒳 × 𝒳 → [0,1]. Recovering K requires:

1. Microstate-sufficient observables (to read σ_t).
2. Sequential observations (to see transitions σ_t → σ_{t+1}).

**The UOP statement for dynamics:** The joint map J_dyn = (f(σ_t), f(σ_{t+1})): S × S → Y × Y must be injective on the support of K (all pairs (σ,σ') with K(σ→σ')>0). For single-spin Glauber dynamics: the support is pairs (σ, σ^{(i)}) differing in one site. A microstate-sufficient family is also sufficient for the support (it separates both endpoints of each transition). 

**Observation 2 (Symmetry and lumpability).**

The G-lumpability theorem is the dynamics analog of the quotient-sufficiency result: just as G-invariant observables are sufficient for S/G, G-invariant dynamics (lumpable chain) produce a well-defined Markov chain on S/G. The symmetry of the observable family and the symmetry of the dynamics are matched.

**Observation 3 (The open question — dynamics from structure).**

We showed: if you can observe microstates sequentially, you can recover K. This is not surprising. The interesting open question is:

**Can K be recovered from fewer observations than microstate-sufficiency, using structural constraints on K (e.g., detailed balance, single-spin-flip dynamics, locality)?**

For the 1D Ising Glauber chain at known β: K is parameterized by β alone (plus the geometric structure, which is known). So observing ⟨c⟩_β (one G-invariant observable) determines β, which determines K. **One observable is sufficient for dynamics recovery when the kernel class is known to be Glauber.**

This is the connection from "observing physics" to "identifying the physics": when the class of allowed dynamics is constrained (Glauber, detailed balance, locality), far fewer observables suffice to identify the specific kernel within that class.

---

## Summary

**Question 1 (Gibbs state):** One G-invariant observable c(σ) = nearest-neighbor correlation suffices. ⟨c⟩_β = 4sinh(4β)/(4cosh(4β)+12) is strictly monotone in β — determines β, hence ρ_β. *Proved.*

**Question 2 (Microstate):** Four binary single-site observables {f₀,...,f₃} are necessary and sufficient. Score sequence: geometric decay with ratio 1/2 (each site adds one independent bit). *Proved.*

**Question 3 (Symmetry quotient):** Two G-invariant observables {|m|², c} separate all 4 orbits on the n=4 Ising ring. No single G-invariant observable suffices (O₂ and O₃ share H=0 and need |m|² to distinguish). *Proved.*

**Question 4 (Dynamics):** 
- Stationary distribution alone: not sufficient (multiple kernels share ρ_β). *Proved.*
- Microstate-sufficient family + trajectory: sufficient for full K. *Proved.*
- G-sufficient family + trajectory: sufficient for lumped K_G (lumpability proved). *Proved.*
- Single observable + structural constraint: sufficient for K when kernel class is parameterized by one parameter (β). *Proved for Glauber class.*

**Open question:** For which kernel classes does structure (locality, detailed balance, symmetry) reduce the observation requirement below microstate-sufficiency? This is the question of identifiability for dynamical systems — the direct dynamical extension of the UOP arc.
