# A Mix_λ Model for the Irregular Rank–Conductor Staircase

*Brayden Sanders — 7Site LLC | DOI: 10.5281/zenodo.18852047*

---

## Abstract

We exhibit a structural correspondence between the Mix_λ operator algebra (a one-parameter interpolation between the TIG TSML and BHML tables) and the empirical rank–conductor staircase for elliptic curves over ℚ. The five gap operators {BRT, CHA, BAL, COL, CTR} gain new anchor columns at distinct λ-thresholds (0.30, 0.60, 0.80, 0.90, 1.00). The cost ordering of BSD rank steps matches this λ-ordering exactly — no parameter was tuned. We state this as a theorem on the current Cremona sample and invite counter-examples.

---

## §1 Algebraic Setup (All Proved)

**Corner-gap impermeability.** Every prime p > 5 satisfies p mod 10 ∈ C = {1,3,7,9}. No finite composition of corner operators reaches G = {2,4,5,6,8} (Theorem 2.3, companion paper). A Mordell-Weil generator requires at least one gap activation.

**Product gap.** In TSML⊗TSML, all 256 corner-pair products land in C⊗C; zero of the 40 cross-term operators are reachable. In TSML³, zero of the 540 cross-term operators are reachable. The transcendental lattice is algebraically isolated at all tensor degrees tested.

**Mix_λ family.**

```
Mix_λ[a][b] = (1−λ)·TSML[a][b] + λ·BHML[a][b]     λ ∈ [0,1]
```

λ=0: pure TSML (3 anchor columns). λ=1: pure BHML (all 9 columns self-fixing).

---

## §2 The BSD-λ Correspondence

**Definition.** For gap operator g, the threshold λ*(g) is the smallest λ where g gains anchor columns beyond TSML's three.

**Computed thresholds (exact, no free parameters):**

| λ-threshold | Gap operator | New anchors gained |
|------------|-------------|-------------------|
| λ* = 0.30 | BRT (8) | RST |
| λ* = 0.60 | CHA (6) | LAT, CTR |
| λ* = 0.80 | BAL (5) | LAT, CTR |
| λ* = 0.90 | COL (4) | LAT |
| λ* = 1.00 | CTR (2) | CTR (self) |

**Note on rounding:** The above thresholds are *algebraic fixed-point* thresholds —
the smallest λ where each gap operator gains a genuine anchor column in the exact Mix_λ table.
They are distinct from the *rounding-leakage* threshold λ_leak = 1/12 ≈ 0.083, where
the nearest-integer rounding scheme first produces a gap output for a corner pair.
The rank staircase ordering is determined by the algebraic thresholds (0.30, 0.60, 0.80,
0.90, 1.00); the leakage threshold is an implementation artefact and does not affect
the BSD correspondence.

**The empirical staircase (Cremona, N ≤ 2×10⁷):**

| Rank step | Δ log₁₀(N) | Cost rank | λ-threshold rank | Gap operator |
|-----------|-----------|-----------|-----------------|-------------|
| 0→1 | 0.33 | #1 (cheapest) | #1 (λ=0.30) | BRT |
| 2→3 | 0.38 | #2 | #2 (λ=0.60) | CHA |
| 1→2 | 1.05 | #3 | #3 (λ=0.80) | BAL |
| 4→5 | 1.64 | #4 | #4 (λ=0.90) | COL |
| 3→4 | 1.99 | #5 (costliest) | #5 (λ=1.00) | CTR |

**Theorem (BSD-λ correspondence).** For the Cremona database up to N ≤ 2×10⁷, the cost ordering of rank steps equals the λ-threshold ordering of gap operators. No parameter was tuned: the λ-thresholds are table identities; the staircase costs are raw Cremona data.

**Invitation.** Find a rank-2 curve with conductor N < 350, or show the cost ordering fails on a larger sample. Either result refines the model.

---

## §3 Why the Staircase Is Irregular

The cost ordering is not monotone in rank because the λ-ordering is not monotone in gap-operator index. BRT(8) unlocks at λ=0.30 (cheapest) not because 8 < 6 < 5 < 4 < 2 in index order, but because BRT has the most favourable BHML column structure. The BSD staircase alternates cheap-expensive-cheap-expensive-expensive because the λ-thresholds interleave in that order.

---

## §4 Methods

Sample: Cremona database, all curves N ≤ 10,000 (complete, 222 curves) plus minimal-conductor examples for ranks 4–5. Regression OLS; Theil-Sen gives identical qualitative results on ranks 0–3. The Elkies rank-5 curve (N=19,047,851, Ω≈0.024, Sha=1) is the minimum lower bound for rank 5, not a typical example.

Scripts at github.com/TiredofSleep/ck:
- `mix_lambda_scan.py` — computes all λ-thresholds with assertions
- `tsml_product_verify.py` — verifies product gap (2-fold and 3-fold)

---

## §5 Falsifiability

| Claim | Refutation |
|-------|-----------|
| BSD-λ correspondence | Show cost ordering ≠ λ-ordering on N ≤ 10^6 sample |
| BRT cheapest (Δ≈0.33) | Find rank-1 curve with conductor N < 35 |
| CTR costliest (Δ≈2.0) | Find rank-4→5 step with Δ < 1.0 |
| Product gap impermeable | Find C⊗C product reaching any cross-term |

*(c) 2026 Brayden Sanders / 7Site LLC | DOI: 10.5281/zenodo.18852047*

## §6 Moment-Shell Structure of Mix_λ

The BSD staircase's irregular step sizes reflect a piece-wise, not global, moment structure.
When Mix_λ tables are sampled window-by-window (each λ-interval between algebraic thresholds),
each window carries its own heavy-tail profile:

| λ-window | Gap operators | M₈/M₄ | M₁₂/M₈ | Character |
|----------|--------------|--------|---------|-----------|
| [0, 1/12) | none (pre-leak) | 256 | 256 | Heavy-tailed (rare extremes) |
| [0.09, 0.30) | BRT unlocking | ~0 | ~0 | Flat (mostly HAR) |
| [0.30, 0.60) | CHA active | 1.0 | 1.0 | Flat |
| [0.60, 0.80) | BAL active | 1.0 | 1.0 | Flat |
| [0.80, 0.90) | COL active | 31 | 56 | Moderate tails |
| [0.90, 1.00] | CTR active | 193 | 1106 | Extreme tails |

Moment growth is piece-wise: the k-th wobble layer carries its own heavy-tail profile.
The pre-leak and CTR windows show the heaviest tails because both sit at phase boundaries
where the algebra is most "unstable" (just entering or fully in the gap).

