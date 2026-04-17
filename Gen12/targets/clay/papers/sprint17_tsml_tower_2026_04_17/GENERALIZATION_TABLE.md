# Exact / Observed / Generalization Status Table
## What Scales, What Doesn't

---

## Master Table

| Object / Claim | Exact on Z/10 | Observed in family | Candidate generalization | Broken / False |
|---|---|---|---|---|
| Canonical construction $C(R, h, \sigma)$ — 3-rule definition | Yes — definable | Yes — 35 rings in compatibility family (up to n=300) | Produces a projection-type table on any compatible ring | — |
| $C_0$ recovers 92/100 TSML entries | Yes — verified | — | Recovery fraction for other rings is open (no reference TSML) | — |
| $C_1$ (MAX) rule | Yes — covers 6/100 | — | Well-defined on any $\mathbb{Z}/n\mathbb{Z}$ | — |
| $C_2$ (ADD mod $n$) rule | Yes — covers 2/100 | — | Well-defined (ring addition) on any $\mathbb{Z}/n\mathbb{Z}$ | — |
| Tower termination: residue = ∅ after 3 layers | Yes — verified | — | Conjectured for compatibility family | — |
| Domain disjointness | Yes — Lemma 1, 2 | Construction is domain-disjoint by definition | Applies to any ring | — |
| Seam residue $S$ is specific 8-element set | Yes — given data | — | $S$ is ring-specific | — |
| Seam topology: tree with hub and 3 branches | Yes — verified | Unknown | Pattern may generalize; specific edges will not | — |
| Branch-rule mapping (identity→ADD, others→MAX) | Yes — verified | Unknown | Conjectured consistent across family | — |
| Strict shell-order coarsening | Yes (Z/10 in set {Z/4, Z/6, Z/10}) | Only 3 rings in family | — | Fails at Z/14 and all larger |
| Divisibility-compatibility of shell with orders | Yes | 35 rings up to n=300 | — | Fails at Z/26, Z/38, ... |
| Z/10 is unique max-score ring (score 10 on rubric) | Yes | — | — | — |
| Z/10 has 2-shell partition exactly | Yes | Only Z/4, Z/6 share this | — | All other rings have 3+ shells |
| TSML and BHML share carrier | Yes | — | — | — |
| BHML has det = 70 | Yes — from image | — | — | — |
| TSML has det = 0 | Yes — matrix rank deficiency | — | — | — |
| (T, B) pair as structural concept (projection + transport) | Yes — conceptual | — | Applies to any compatible ring as concept | — |
| Specific TSML values | Yes — known | — | — | Do not generalize |
| Specific BHML values | Yes — known | — | — | Do not generalize |
| "2×2 admissible skeleton" language | Yes — specific to Z/10 | — | — | Does not generalize (2-shell is Z/10-specific) |
| Primorial lift hypothesis | — | — | — | False — Z/30, Z/210 break alignment |
| Last-digit-7 as invariant marker | Local to 2-digit room | Fails at room 3 and room 6 | — | False as law |
| Stop-apex compositeness universal | — | — | — | False — 45127 in 5-digit room is prime |
| ECHO tree has a single-rule generator | — | — | — | False — tested MAX/ADD/MULT/MIN individually |
| The 3-layer tower is the unique minimal decomposition | Unknown (minimum among tested) | — | Open | — |

## Rules vs Domains — Clean Separation

| Item | Generalization status |
|---|---|
| DEFAULT rule ($x,y \mapsto h$) | **Rule generalizes:** applies to any ring with a chosen $h$. |
| V0 rule ($0$ absorbs except at $(0,h)$) | **Rule generalizes:** applies to any ring. |
| Shell-stability rule | **Rule generalizes;** requires shell partition $\sigma$ and attractor $h$ as input. |
| MAX rule | **Rule is universal;** applies to any $\{0, 1, \ldots, n-1\}$ with integer order. |
| ADD mod $n$ rule | **Rule is universal;** applies to any $\mathbb{Z}/n\mathbb{Z}$. |
| — | — |
| $D_0$ (complement of seam) | **Domain is ring-specific.** Depends on which pairs fall into $S$. |
| $D_1 = S_{\text{MAX}}$ | **Domain is ring-specific.** Depends on seam structure. |
| $D_2 = S_{\text{ADD}}$ | **Domain is ring-specific.** Depends on seam structure. |
| — | — |
| Seam topology (hub + branches) | **Pattern may generalize** as a type-class organization. Specific vertices do not. |
| Branch-rule mapping | **Pattern may generalize** (identity-branch → ADD, other-branches → MAX). Unverified. |

## Why This Separation Matters

The rules of the tower are **ring-agnostic operations**: DEFAULT, V0, shell-stability, MAX, ADD. They apply uniformly to any ring with the required inputs (attractor, shell partition).

The domains of application are **ring-specific data**: $S$, $S_{\text{MAX}}$, $S_{\text{ADD}}$. These are determined by comparing $C_0$ output to a reference TSML, which exists only for Z/10Z.

To extend the tower framework to another ring, one needs either:

1. A reference TSML for that ring (currently unavailable for any ring other than Z/10).
2. A principled definition of what $S$ should be in that ring, derived from ring structure alone.

Neither is currently available. The tower framework is thus:

- **Fully generalized as a construction procedure** (given $S$ as input).
- **Not yet generalized as a predictive theory** (cannot predict $S$ for other rings without TSML reference).

## Family-Scale Observations

Within the 35-ring compatibility family:

| Claim | Status |
|---|---|
| Family has 35 members up to n=300 | Exact |
| Z/10 uniquely maximal in strict-coarsening sub-tier | Exact |
| Powers of 2 (Z/2^k) all belong to family | Observed (up to k=8) |
| Primes in family's "compatible set" include {3, 5, 7, 11, 17} | Observed |
| Primes {13, 19, 23, 29} produce incompatible rings via 2p | Observed |
| Family closed under multiplication by compatible primes | Conjecture |
| Algebraic characterization of compatibility | Open |

## What This Table Does Not Include

Deliberately excluded from the generalization table:

- Physics or cosmology claims.
- Semantic interpretation of TSML/BHML operators.
- Claims about observer, reality, or consciousness derived from the ring structure.
- Claims about primes, Collatz, or other open problems as consequences.

These are kept out of the status table to maintain clarity of what is a finite, verifiable result.
