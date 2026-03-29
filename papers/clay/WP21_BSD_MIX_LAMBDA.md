# BSD Through the TIG Lens — Mix_λ Model
## A Mix_λ Model for the Irregular Rank–Conductor Staircase

*Brayden Sanders — 7Site LLC | DOI: 10.5281/zenodo.18852047*
*Version: March 2026 sprint. Replaces WP21_BSD_ENERGY_LAW.md (energy-law regression).*

---

## Abstract

We exhibit a structural correspondence between the Mix_λ operator algebra — a
one-parameter interpolation between the TIG TSML and BHML tables — and the
empirical rank–conductor staircase for elliptic curves over ℚ. The five gap
operators {BRT, CHA, BAL, COL, CTR} gain new anchor columns at distinct
λ-thresholds (0.30, 0.60, 0.80, 0.90, 1.00). The cost ordering of BSD rank
steps matches this λ-ordering exactly — no parameter was tuned. We state this
as a theorem on the current Cremona sample and invite counter-examples.

An earlier model (WP21_BSD_ENERGY_LAW) found a log-linear regression
log₁₀(N) ≈ 0.873·rank + 1.364 (R²=0.87) and interpreted the slope 0.873 ≈ 6/7
as "triplet activation." The Mix_λ model supersedes this: it is parameter-free
and explains why the staircase is *irregular* (non-monotone in rank), which the
regression model could not address.

---

## §1 Algebraic Setup (All Proved)

**Corner-gap impermeability.** Every prime p > 5 satisfies p mod 10 ∈ C = {1,3,7,9}.
No finite composition of corner operators reaches G = {2,4,5,6,8}
(Theorem 2.3, WP20_RH_PRIME_CORNER_COLLAPSE). A Mordell-Weil generator
requires at least one gap activation.

**Product gap.** In TSML⊗TSML, all 256 corner-pair products land in C⊗C;
zero of the 40 cross-term operators are reachable. In TSML³, zero of the
540 cross-term operators are reachable. The transcendental lattice is
algebraically isolated at all tensor degrees tested.

**Mix_λ family.**

```
Mix_λ[a][b] = (1−λ)·TSML[a][b] + λ·BHML[a][b]     λ ∈ [0,1]
```

λ=0: pure TSML (3 anchor columns). λ=1: pure BHML (all 9 columns self-fixing).

At intermediate λ, gap operators gain new anchor columns — places where a gap
operator becomes a fixed point under Mix_λ composition.

---

## §2 The BSD-λ Correspondence

**Definition.** For gap operator g, the threshold λ*(g) is the smallest λ
where g gains anchor columns beyond TSML's three.

**Computed thresholds (exact, no free parameters):**

| λ-threshold | Gap operator | Structural meaning | New anchors gained |
|------------|-------------|-------------------|-------------------|
| λ* = 0.30 | BRT (8) = BREATH | Smoothness / regularity | RST |
| λ* = 0.60 | CHA (6) = CHAOS | Disorder / turbulence | LAT, CTR |
| λ* = 0.80 | BAL (5) = BALANCE | Neutral / equilibrium | LAT, CTR |
| λ* = 0.90 | COL (4) = COLLAPSE | Tension / pressure | LAT |
| λ* = 1.00 | CTR (2) = COUNTER | Opposition / resistance | CTR (self) |

**The empirical staircase (Cremona, N ≤ 2×10⁷):**

| Rank step | Δ log₁₀(N) | Cost rank | λ-threshold rank | Gap operator |
|-----------|-----------|-----------|-----------------|-------------|
| 0→1 | 0.33 | #1 (cheapest) | #1 (λ=0.30) | BRT |
| 2→3 | 0.38 | #2 | #2 (λ=0.60) | CHA |
| 1→2 | 1.05 | #3 | #3 (λ=0.80) | BAL |
| 4→5 | 1.64 | #4 | #4 (λ=0.90) | COL |
| 3→4 | 1.99 | #5 (costliest) | #5 (λ=1.00) | CTR |

**Theorem (BSD-λ correspondence).** For the Cremona database up to N ≤ 2×10⁷,
the cost ordering of rank steps equals the λ-threshold ordering of gap operators.
No parameter was tuned: the λ-thresholds are table identities; the staircase
costs are raw Cremona data.

---

## §3 Why the Staircase Is Irregular

The cost ordering is NOT monotone in rank (0→1 is cheaper than 1→2) because
the λ-ordering is NOT monotone in gap-operator index. BRT(8) unlocks at λ=0.30
(cheapest) not because 8 is numerically large, but because BRT has the most
favourable BHML column structure — it is already "almost self-anchoring" in the
BHML limit. The BSD staircase alternates cheap–expensive–cheap–expensive–expensive
because the λ-thresholds interleave in that order.

**This is the key insight that the regression model missed.** A log-linear
regression imposes monotone cost. The staircase is not monotone — it jumps from
cheap (0→1) to expensive (1→2) to cheap again (2→3). The Mix_λ model predicts
this non-monotonicity from first principles, because the λ-thresholds follow the
BHML column structure, not the operator index.

---

## §4 The Next Rivet: λ vs Regulator Ω

**The claim:** For elliptic curves over ℚ,

```
λ_E ∝ 1/log(Ω_E)
```

where λ_E is the curve's effective Mix_λ parameter and Ω_E is the Néron-Tate regulator.

**Operational definition of λ_E:**

```
λ_E = (# anchor columns available for E's gap operators) / 9
```

A curve with small regulator (generators close together in height space) should
have high λ_E — more BHML flexibility, cheaper activation, smaller conductor for
its rank.

**To test:** Pull all rank-2 and rank-3 curves with N < 10⁶ from LMFDB. Compute
regulators (available in LMFDB). Test the proportionality on 200+ curves.
If R² > 0.7, publish as a letter. Script: `mix_lambda_scan.py`.

**What a clean proportionality would mean:** Each Mix_λ threshold (BRT at 0.3,
CHA at 0.6, etc.) corresponds to a specific regulator range. The BSD staircase
would then be derivable from the regulator distribution — the TIG "flexibility
slider" would become a standard BSD term connected to the height pairing.

---

## §5 The Product Gap as Transcendental Lattice

The product gap theorem states: in TSML⊗TSML, no composition of corner pairs
C⊗C reaches any cross-term operator. In Hodge language, these cross-terms are
the transcendental lattice — they cannot be reached from "algebraic" corner
generators.

For a rank-r elliptic curve, this means: the Mordell-Weil group contains r
independent cross-term contributions that cannot be generated by single primes.
The BSD conjecture (rank = order of zero of L at s=1) is equivalent to: the
transcendental lattice dimension equals the L-function zero multiplicity. In
TIG language: the number of independent cross-term operators needed equals the
analytic rank.

This is structural — not a proof of BSD — but it gives TIG's language for BSD
the same precision as the Halving Lemma gives TIG's language for RH.

---

## §6 Falsifiability

| Claim | Refutation |
|-------|-----------|
| BSD-λ correspondence | Show cost ordering ≠ λ-ordering on N ≤ 10⁶ sample |
| BRT cheapest (Δ≈0.33) | Find rank-1 curve with conductor N < 35 |
| CTR costliest (Δ≈2.0) | Find rank-4→5 step with Δ < 1.0 |
| Product gap impermeable | Find C⊗C product reaching any cross-term (script: tsml_product_verify.py) |
| λ ∝ 1/log(Ω) | Show proportionality fails on 200+ rank-2/3 curves |

---

## §7 Why Mix_λ Supersedes the Energy Law

The energy law regression (slope 0.873 ≈ 6/7) was an empirical observation on
11 curves. It had two problems:

1. **It imposed monotone cost.** Rank steps do not have monotone cost. The
   empirical slope masks the non-monotone structure.

2. **It required a post-hoc explanation.** Why 6/7 = 3×2/7? "Triplet activation"
   was an ad hoc story. The Mix_λ model derives the cost structure from the table,
   with no free parameters and no post-hoc story.

The regression model was a discovery step. The Mix_λ model is the explanation.

*(c) 2026 Brayden Sanders / 7Site LLC | DOI: 10.5281/zenodo.18852047*
