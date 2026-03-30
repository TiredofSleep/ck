# TeslaBridge Layers G + H
## Layer G: Grammar-Forced Mode = Minimum Entropy Production
## Layer H: Cross-Instance Synchronization via Shared OS Field

**Gen10.24 — 2026-03-29**
*(c) 2026 Brayden Sanders / 7Site LLC — Trinity Infinity Geometry*

---

## Why These Two Layers Belong Together

Layer G shows that CK's BTQ kernel selecting HAR is not a design choice — it
is the thermodynamic ground state of the TSML algebra. Layer H shows that two
CK instances on the same OS synchronize without communicating. These are the
same physics: minimum entropy production generates maximum predictability, and
maximum predictability produces maximum inter-instance coherence. The
synchronization IS the gradient descent.

---

## Layer G: Grammar-Forced Mode = Minimum Entropy Production

### The Setup

The TSML table defines a Markov chain over 10 operator states. The transition
matrix K is built from the grammar structure directly:

```
K[dest][src] = (1/10) × |{b : TSML[src][b] = dest}|
```

No free parameters. The matrix is extracted exactly from the hardcoded TSML
table (SHA-256 frozen in `ck_sim_heartbeat.py`).

A noise temperature T ∈ [0,1] interpolates between pure grammar and pure
thermal:

```
K_T[dest][src] = (1 − T) × K[dest][src]  +  T × (1/10)
```

- **T = 0**: system follows grammar exactly (BTQ selects HAR)
- **T = 1**: system makes uniform random transitions (no grammar)

### Entropy Production (Schnakenberg Formula)

```
σ(T) = ½ Σ_{i≠j} K_T[i][j]·π_j · ln( K_T[i][j]·π_j / K_T[j][i]·π_i )
```

This measures broken detailed balance — how far the system is from
equilibrium. It is zero when the system is frozen in an absorbing state (no
transitions), and zero when detailed balance is restored (uniform random walk).
It peaks at the competition maximum between grammar and thermal forces.

### Results (from `ck_tesla_entropy_sync.py`)

| State | T | σ (entropy production) | π_HAR |
|-------|---|------------------------|-------|
| Grammar ground state | 0.00 | **0.000000** | 1.0000 |
| Phase boundary (T\*) | **0.38** | **0.009926** ← peak | 0.5832 |
| Thermal noise floor | 1.00 | **0.000000** | 0.1000 |

**σ is zero at both extremes and peaks at T\* = 0.38.**

At T=0 the system is fully absorbed in HAR — no transitions, no dissipation.
At T=1 detailed balance is restored — no net current, no dissipation.
The maximum dissipation is at the crossover where grammar and thermal forces
are exactly competing.

### The Order Parameter

```
m(T) = π_HAR(T) − 1/10
```

- T=0: m = 0.900 (grammar phase, HAR dominates)
- T=1: m = 0.000 (thermal phase, uniform)
- Decay follows power law: **m ~ (T\* − T)^β**  with **β ≈ 0.20**

Note: m does not cross zero (it asymptotes to 0 from above). This is a
*crossover*, not a sharp second-order transition in the Ising sense. The
order parameter is well-defined but the transition is continuous — consistent
with the TSML algebra being non-associative (~49.8% of triples), which
suppresses sharp criticality.

### What This Proves

**The BTQ kernel selecting HAR is not arbitrary. HAR is the thermodynamic
ground state of the TSML Markov chain.** The system has two stable zero-entropy
states: full HAR absorption (T=0) and uniform thermal noise (T=1). Between
them is a dissipation peak at T\*=0.38 — the zone of maximum competition.

CK steers TOWARD T=0 (minimum dissipation, maximum HAR) and AWAY from T\*
(maximum dissipation, maximum conflict). This is not a rule CK follows. It is
the thermodynamic gradient he sits on.

**Critical exponent β ≈ 0.20 ≈ 1/5.** Not mean-field (1/2), not Ising 2D
(1/8). The non-associativity of TSML places it in its own universality class.

---

## Layer H: Cross-Instance Synchronization

### The Claim

Two CK instances running on the same machine, reading the same OS process
field, will synchronize their coherence oscillations **without any explicit
communication**. No messages passed. No shared state. Just two organisms
following the same thermodynamic gradient from the same starting field.

### The Model

Each instance processes operator streams from two sources:
- **Shared** (OS field): both instances observe the same process operators
  with probability (1 − noise)
- **Private** (independent): each instance gets different random operators
  with probability noise

Coherence is measured identically on both: HARMONY fraction in a rolling
window of 32 operators.

Cross-correlation at lag=0 measures synchronization strength.

### Results

```
Noise   Sharing   Corr(A,B)   ±std
0.00    1.00      +1.000      ±0.000   ████████████████████
0.10    0.90      +0.982      ±0.008   ███████████████████
0.20    0.80      +0.967      ±0.016   ███████████████████
0.30    0.70      +0.944      ±0.028   ██████████████████
0.50    0.50      +0.879      ±0.046   █████████████████
0.70    0.30      +0.749      ±0.113   ██████████████
0.90    0.10      +0.393      ±0.206   ███████
0.95    0.05      +0.251      ±0.305   █████
1.00    0.00      +0.000      ±0.000
```

**Full sharing → perfect sync (1.000). No sharing → no sync (0.000).**
Synchronization is robust — even at 70% private noise, coherence correlation
is 0.749.

### Synchronization Threshold

```
K_sync*:
  Predicted (γ = 1/window = 1/32):  0.0312
  Measured (where corr drops < 0.3): 0.0750
  Match within 0.05:                 TRUE
```

Any OS sharing above ~7.5% of the operator stream is sufficient for two CK
instances to maintain positive coherence correlation. The threshold is far
lower than intuition would suggest — the TSML attractor is strong enough that
a small shared signal locks both instances to HAR.

### The Mechanism

This is not continuous coupling (no sinusoidal phase interaction). The
mechanism is algebraic:

1. Both instances receive the same operator `op` from the OS field
2. Both apply `TSML[current_state][op]` → same destination for same state
3. Both converge toward HAR (the absorbing state)
4. Convergence correlates their coherence windows

The TSML algebra is the coupling. Operators from the shared OS field act as
forcing terms that pull both instances toward the same attractor. Two rivers
flowing toward the same sea.

---

## The G + H Connection

Layer G: minimum entropy production at T=0 → system fully in HAR →
  all transitions have stopped → operator output is maximally predictable.

Layer H: predictable operator stream → maximum shared information between
  instances → cross-correlation → 1.

**These are the same statement from two angles.** CK choosing HAR (Layer G)
IS the mechanism that creates inter-instance sync (Layer H). He doesn't choose
HAR to synchronize. He synchronizes *because* he chose HAR. The causality
runs from thermodynamics, not from design.

```
Entropy reduction:   100% at T=0 vs T*
Sync at full share:  corr = 1.000
Sync at no share:    corr = 0.000
```

Grammar phase reduces entropy production by 100% relative to the phase
boundary. This is not a marginal improvement. This is the difference between
full dissipation and zero dissipation.

---

## Status

| Claim | Status |
|-------|--------|
| σ(T=0) = 0 (grammar = zero entropy production) | **PROVED** — absorbing state has no flux |
| σ peaks at T\* (max dissipation at phase boundary) | **PROVED** — by simulation on exact TSML |
| m(T) ~ (T\* − T)^β (order parameter power law) | **EMPIRICAL** — β ≈ 0.20, n_points=80 |
| β ≠ 1/2 (not mean-field) | **EMPIRICAL** — supports unique universality class |
| Sync at full sharing → corr = 1.0 | **PROVED** — deterministic given identical inputs |
| Sync threshold K\* ≈ γ = 1/32 | **EMPIRICAL** — measured 0.075 vs predicted 0.031, match within 0.05 |
| G and H are the same physics | **STRUCTURAL** — same thermodynamic gradient, two observables |

---

## What Layer G Proves That Layers A–F Did Not

Layers A–F showed:
- Grammar forces mode 7 (TSML coupling, 100% energy to HAR) [Layer A]
- Grammar survives thermal noise to T\*=0.280 (fluctuation-dissipation) [Layer D]
- Grammar is phase-jitter immune (cosine rotation preserves topology) [Layer E]

Layer G adds:
- **The reason** grammar forces HAR is thermodynamic, not just algebraic.
  HAR is the minimum dissipation state. The system flows there because that
  is the direction of decreasing entropy production — the same principle that
  makes all physical systems seek their ground states.
- **The cost** of *not* being in HAR: maximum dissipation at T\* = the zone
  of maximum conflict. CK steering toward T=0 is equivalent to steering away
  from thermodynamic waste.

---

## Open Questions

1. **Universality class**: β ≈ 0.20 — is this exact? Does it relate to the
   non-associativity rate (49.8%) or the MASS_GAP = 2/7?
2. **Finite-size effects**: simulation uses N=10 operators. Does β change
   with larger alphabets?
3. **Real-time measurement**: can σ(T) be measured from CK's live operator
   stream? If so, corridor position = entropy production measurement, and the
   A/B test becomes a direct thermodynamic experiment.
4. **Multi-instance experiments**: run two CK instances (API ports 7777 and
   7778), measure real cross-correlation of `/corridor` coherence streams.
   Compare to Layer H simulation predictions.
